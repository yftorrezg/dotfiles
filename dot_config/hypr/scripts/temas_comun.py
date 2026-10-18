"""temas_comun.py — catálogo de temas compartido por escritorios-vivos.py y estilos.py.

Un tema = un video en ~/Imágenes/Wallpapers/Temas/{Oscuros,Claros}/*.mp4 (se descubren
solos: copia un .mp4 ahí y aparece en el selector). Además hay dos temas "por escritorio"
que usan los fondos de escritorios-temas.toml (uno distinto en cada SUPER+1..5):
  escritorios:fijo   imágenes fijas      escritorios:video   videos por escritorio

Para cada video se prepara en ~/.cache/escritorios-vivos/temas/:
  <slug>.jpg (póster 1920 px: fondo de respaldo bajo el video), <slug>.mini.jpg (tarjeta),
  <slug>.clip.mp4 (vista previa de 6 s) y <slug>.acento (color dominante, para destellos y aviso).
"""
import colorsys
import json
import re
import subprocess
from pathlib import Path

CARPETA = Path.home() / "Imágenes/Wallpapers/Temas"
CACHE = Path.home() / ".cache/escritorios-vivos/temas"
ESTADO = Path.home() / ".local/state/escritorios-vivos"
ESTILO = ESTADO / "estilo.json"
GRUPOS = (("Oscuros", "dark"), ("Claros", "light"))
POR_ESCRITORIO = {
    "escritorios:fijo": ("Por escritorio", "Un fondo fijo distinto en cada escritorio", "🖼️"),
    "escritorios:video": ("Por escritorio animado", "Un video distinto en cada escritorio", "🎞️"),
}
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


def leer_estilo():
    """{"tema", "destellos", "ultimo": {"dark": id, "light": id}} (convierte el formato viejo)."""
    try:
        d = json.loads(ESTILO.read_text())
    except (OSError, ValueError):
        d = {}
    if "tema" not in d:  # formato anterior: {"fondo": "estatico|video|aurora"}
        d["tema"] = "escritorios:video" if d.get("fondo") == "video" else "escritorios:fijo"
    if not (d["tema"] in POR_ESCRITORIO or buscar(d["tema"])):
        d["tema"] = "escritorios:fijo"
    return {"tema": d["tema"], "destellos": bool(d.get("destellos", False)),
            "ultimo": d.get("ultimo") or {}}


def guardar_estilo(d):
    ESTADO.mkdir(parents=True, exist_ok=True)
    tmp = ESTILO.with_suffix(".tmp")
    tmp.write_text(json.dumps({"tema": d["tema"], "destellos": d["destellos"], "ultimo": d.get("ultimo", {})}))
    tmp.replace(ESTILO)


if __name__ == "__main__":  # python3 temas_comun.py → prepara todo (lo usa escritorios-vivos al iniciar)
    for tema in catalogo():
        preparar(tema)
