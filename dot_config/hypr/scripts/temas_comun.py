"""temas_comun.py — catálogo de temas compartido por escritorios-vivos.py y estilos.py.

Un FONDO = un video en ~/Imágenes/Wallpapers/Temas/{Oscuros,Claros}/*.mp4 (se descubren
solos: copia un .mp4 ahí y aparece en la Galería). Su id es "Oscuros/<nombre sin .mp4>".
Un TEMA pone un fondo distinto en cada escritorio (SUPER+1..5):
  col:<nombre>       colección de ~/.config/hypr/temas-colecciones.toml (5 fondos, uno por escritorio)
  mezcla:dark|light  "Mi selección": la armas tú en la Galería con las teclas 1-5
  escritorios:fijo   imágenes fijas      escritorios:video   videos 1080p   (escritorios-temas.toml)

Para cada video se prepara en ~/.cache/escritorios-vivos/temas/:
  <slug>.jpg (póster 1920 px: fondo de respaldo bajo el video), <slug>.mini.jpg (tarjeta),
  <slug>.clip.mp4 (vista previa de 6 s) y <slug>.acento (color dominante, para destellos y aviso).
"""
import colorsys
import json
import re
import subprocess
import tomllib
import unicodedata
from pathlib import Path

CARPETA = Path.home() / "Imágenes/Wallpapers/Temas"
CACHE = Path.home() / ".cache/escritorios-vivos/temas"
ESTADO = Path.home() / ".local/state/escritorios-vivos"
ESTILO = ESTADO / "estilo.json"
COLECCIONES = Path.home() / ".config/hypr/temas-colecciones.toml"
GRUPOS = (("Oscuros", "dark"), ("Claros", "light"))
POR_ESCRITORIO = {
    "escritorios:fijo": ("Clásico", "Imágenes fijas, una por escritorio", "🖼️"),
    "escritorios:video": ("Clásico animado", "Videos suaves, uno por escritorio", "🎞️"),
}
ESCRITORIOS = 5
ACENTO_POR_DEFECTO = "#c9a7ff"


def nombre_bonito(slug):
    return slug.replace("-", " ").strip().capitalize()


def catalogo():
    """Lista de temas de video: dict(id, nombre, modo, video, slug)."""
    temas = []
    for carpeta, modo in GRUPOS:
        for video in sorted((CARPETA / carpeta).glob("*.mp4")):
            if ".tmp" in video.name:
                continue
            temas.append({"id": f"{carpeta}/{video.stem}", "nombre": nombre_bonito(video.stem),
                          "modo": modo, "video": video, "slug": f"{carpeta.lower()}-{video.stem}"})
    return temas


def buscar(tema_id):
    return next((t for t in catalogo() if t["id"] == tema_id), None)


def rutas(t):
    base = CACHE / t["slug"]
    return {"poster": base.with_suffix(".jpg"), "mini": Path(f"{base}.mini.jpg"),
            "clip": Path(f"{base}.clip.mp4"), "acento": Path(f"{base}.acento")}


def _vigente(destino, origen):
    return destino.exists() and destino.stat().st_mtime >= origen.stat().st_mtime


def preparar(t):
    """Crea póster, miniatura, clip y color del tema si faltan o el video cambió."""
    CACHE.mkdir(parents=True, exist_ok=True)
    r, v = rutas(t), t["video"]
    ff = ["ffmpeg", "-v", "error", "-y"]
    if not _vigente(r["poster"], v):
        subprocess.run(ff + ["-ss", "1", "-i", str(v), "-frames:v", "1", "-vf", "scale=1920:-2",
                             "-q:v", "3", str(r["poster"])])
    if not _vigente(r["mini"], v) and r["poster"].exists():
        subprocess.run(ff + ["-i", str(r["poster"]), "-vf",
                             "scale=480:270:force_original_aspect_ratio=increase,crop=480:270",
                             "-q:v", "4", str(r["mini"])])
    if not _vigente(r["clip"], v):
        tmp = Path(f"{r['clip']}.tmp.mp4")
        ok = subprocess.run(ff + ["-i", str(v), "-t", "6", "-an", "-vf",
                                  "scale=480:270:force_original_aspect_ratio=increase,crop=480:270,fps=30",
                                  "-c:v", "libx264", "-preset", "veryfast", "-crf", "26",
                                  "-pix_fmt", "yuv420p", str(tmp)]).returncode == 0
        if ok:
            tmp.replace(r["clip"])
    if not _vigente(r["acento"], v) and r["poster"].exists():
        r["acento"].write_text(color_dominante(r["poster"], t["modo"]))


def poster_video(video):
    """Fotograma (480 px) de cualquier video, en caché: para las tiras de miniaturas del selector."""
    video = Path(video)
    destino = CACHE / f"v-{video.parent.name}-{video.stem}.jpg"
    if not _vigente(destino, video):
        CACHE.mkdir(parents=True, exist_ok=True)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "1", "-i", str(video), "-frames:v", "1",
                        "-vf", "scale=480:-2", "-q:v", "4", str(destino)])
    return destino


def color_dominante(imagen, modo):
    """El color más vivo y abundante de la imagen, ajustado para verse bien como acento."""
    salida = subprocess.run(["magick", str(imagen), "-resize", "96x96", "-colors", "12",
                             "-format", "%c", "histogram:info:-"], capture_output=True, text=True).stdout
    mejor, puntos = None, -1.0
    for cuenta, hexa in re.findall(r"^\s*(\d+):.*?(#[0-9A-Fa-f]{6})", salida, re.M):
        r, g, b = (int(hexa[i:i + 2], 16) / 255 for i in (1, 3, 5))
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        valor = s * (1 - abs(l - 0.5) * 1.4) * (int(cuenta) ** 0.5)
        if valor > puntos:
            mejor, puntos = (h, l, s), valor
    if not mejor:
        return ACENTO_POR_DEFECTO
    h, l, s = mejor
    l = 0.66 if modo == "dark" else 0.58           # brillante pero no chillón
    s = max(0.55, min(0.9, s))
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return "#{:02x}{:02x}{:02x}".format(round(r * 255), round(g * 255), round(b * 255))


def acento(t):
    try:
        return rutas(t)["acento"].read_text().strip()
    except OSError:
        return ACENTO_POR_DEFECTO


# --- temas: colecciones y "Mi selección" ------------------------------------------------------
MEZCLA_INICIAL = {  # punto de partida de "Mi selección" (luego la cambias en la Galería)
    "dark": ["Oscuros/hina-blue-archive", "Oscuros/levi-blanco-negro", "Oscuros/itachi-sharingan",
             "Oscuros/gojo-purpura", "Oscuros/goku-ultra-instinto"],
    "light": ["Claros/miku-bajo-el-cielo", "Claros/rem-verano", "Claros/frieren-dorado",
              "Claros/blue-archive-ventana", "Claros/zero-two-calle"],
}


def _slug(texto):
    sin_tildes = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", sin_tildes.lower()).strip("-")


def colecciones(estilo=None):
    """Temas por escritorio: "Mi selección" (oscura y clara) + las de temas-colecciones.toml."""
    mezcla = (estilo or leer_estilo())["mezcla"]
    lista = [{"id": f"mezcla:{modo}", "nombre": "Mi selección", "icono": "💖", "modo": modo,
              "desc": "Tus favoritos · teclas 1-5 en la Galería", "fondos": mezcla.get(modo, [])}
             for modo in ("dark", "light")]
    try:
        with open(COLECCIONES, "rb") as f:
            datos = tomllib.load(f)
    except (OSError, tomllib.TOMLDecodeError):
        datos = {}
    for c in datos.get("coleccion", []):
        lista.append({"id": f"col:{_slug(c['nombre'])}", "nombre": c["nombre"], "icono": c.get("icono", "🎨"),
                      "modo": c.get("modo", "dark"), "desc": c.get("detalle", "Un fondo en cada escritorio"),
                      "fondos": list(c.get("fondos", []))})
    return lista


def buscar_coleccion(tema_id, estilo=None):
    return next((c for c in colecciones(estilo) if c["id"] == tema_id), None)


def fondos_de(col, cat=None):
    """Los 5 fondos (dicts de catalogo()) de una colección, uno por escritorio; los que falten
    (borraste el video) se rellenan repitiendo los que sí están."""
    por_id = {t["id"]: t for t in (cat or catalogo())}
    hay = [por_id[i] if i in por_id else None for i in col["fondos"][:ESCRITORIOS]]
    validos = [t for t in hay if t]
    if not validos:
        return []
    hay += [None] * (ESCRITORIOS - len(hay))
    return [t or validos[i % len(validos)] for i, t in enumerate(hay)]


def fondo_para(estilo, escritorio):
    """El fondo de video (dict) del tema activo en el escritorio 1..5, o None (temas clásicos)."""
    tema = estilo["tema"]
    if tema.startswith(("col:", "mezcla:")):
        col = buscar_coleccion(tema, estilo)
        fondos = fondos_de(col) if col else []
        return fondos[(escritorio - 1) % len(fondos)] if fondos else None
    return buscar(tema)  # tema de un solo video (formato anterior)


def modo_de(tema_id, estilo=None):
    """Modo al que pertenece un tema ("dark"/"light"), o None si sirve para los dos (clásicos)."""
    if tema_id.startswith(("col:", "mezcla:")):
        col = buscar_coleccion(tema_id, estilo)
        return col["modo"] if col else None
    t = buscar(tema_id)
    return t["modo"] if t else None


def leer_estilo():
    """{"tema", "destellos", "ultimo": {"dark": id, "light": id}, "modo": modo para el que se eligió,
    "mezcla": {"dark": [5 ids], "light": [5 ids]}} (convierte el formato viejo)."""
    try:
        d = json.loads(ESTILO.read_text())
    except (OSError, ValueError):
        d = {}
    if "tema" not in d:  # formato anterior: {"fondo": "estatico|video|aurora"}
        d["tema"] = "escritorios:video" if d.get("fondo") == "video" else "escritorios:fijo"
    mezcla = {m: list((d.get("mezcla") or {}).get(m) or MEZCLA_INICIAL[m]) for m in ("dark", "light")}
    estilo = {"tema": d["tema"], "destellos": bool(d.get("destellos", False)),
              "ultimo": d.get("ultimo") or {}, "modo": d.get("modo"), "mezcla": mezcla}
    # Antes un tema era un solo video para todos los escritorios: ahora pasa a "Mi selección"
    for clave in [estilo["tema"]] + list(estilo["ultimo"].values()):
        t = buscar(clave) if "/" in clave else None
        if t:
            nuevo = f"mezcla:{t['modo']}"
            if estilo["tema"] == clave:
                estilo["tema"] = nuevo
            estilo["ultimo"] = {m: (nuevo if v == clave else v) for m, v in estilo["ultimo"].items()}
    t = estilo["tema"]
    valido = (t in POR_ESCRITORIO or t.startswith("mezcla:")
              or (t.startswith("col:") and buscar_coleccion(t, estilo)) or buscar(t))
    if not valido:
        estilo["tema"] = "escritorios:fijo"
    return estilo


def guardar_estilo(d):
    ESTADO.mkdir(parents=True, exist_ok=True)
    tmp = ESTILO.with_suffix(".tmp")
    tmp.write_text(json.dumps({"tema": d["tema"], "destellos": d["destellos"], "ultimo": d.get("ultimo", {}),
                               "modo": d.get("modo"), "mezcla": d.get("mezcla")}, ensure_ascii=False))
    tmp.replace(ESTILO)


if __name__ == "__main__":  # python3 temas_comun.py → prepara todo (lo usa escritorios-vivos al iniciar)
    for tema in catalogo():
        preparar(tema)
    for video in (Path.home() / "Imágenes/Wallpapers/Animados").glob("*/*.mp4"):  # temas clásicos
        poster_video(video)
