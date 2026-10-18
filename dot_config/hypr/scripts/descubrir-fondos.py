#!/usr/bin/env python3
"""descubrir-fondos.py — catálogo de fondos animados para elegir (pestaña "Descubrir" de SUPER+SHIFT+A).

  python3 descubrir-fondos.py actualizar      busca en motionbgs.com (solo 4K) y baja miniatura + vista
                                               previa pequeña (960x540, ~1 MB) de cada uno
  python3 descubrir-fondos.py bajar <id>      baja el video 4K de ese fondo a Temas/Oscuros|Claros
                                               (convierte HEVC a H.264: la GTX 980 no decodifica HEVC)
  python3 descubrir-fondos.py poner <id> <n> <dark|light>
                                               lo baja y lo pone en el escritorio n de "Mi selección"
                                               (lo usa la Galería al pulsar 1-5; avisa con notificaciones)

Así eliges viendo la animación real sin descargar cientos de videos 4K (~60 MB cada uno):
el 4K se baja solo cuando un fondo te gusta. Oscuro/Claro se decide por el brillo de la imagen.
"""
import json
import re
import subprocess
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import temas_comun as tc  # noqa: E402

SITIO = "https://motionbgs.com"
CARPETA = Path.home() / ".cache/escritorios-vivos/descubrir"
CATALOGO = CARPETA / "catalogo.json"
DESCARTADOS = tc.ESTADO / "descartados.json"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) escritorios-vivos"}

# (etiqueta de motionbgs, categoría que verás en el selector, cuántos traer como máximo)
CATEGORIAS = [
    ("?itachi", "Naruto", 10), ("?sasuke", "Naruto", 8), ("?kakashi", "Naruto", 6), ("naruto-art", "Naruto", 10),
    ("?levi", "Attack on Titan", 8), ("?gojo", "Jujutsu Kaisen", 8), ("?goku", "Dragon Ball", 8),
    ("?luffy", "One Piece", 8), ("?hina", "Blue Archive", 6), ("?robot", "Robots y mechas", 10),
    ("?mecha", "Robots y mechas", 8), ("one-piece", "One Piece", 16), ("dragon-ball", "Dragon Ball", 16),
    ("jujutsu-kaisen", "Jujutsu Kaisen", 16), ("demon-slayer", "Demon Slayer", 16),
    ("attack-on-titan", "Attack on Titan", 16), ("solo-leveling", "Solo Leveling", 16),
    ("bleach", "Bleach", 8), ("chainsaw-man", "Chainsaw Man", 8), ("hxh", "Hunter x Hunter", 8),
    ("berserk", "Berserk", 8), ("tokyo-ghoul", "Tokyo Ghoul", 8), ("death-note", "Death Note", 8),
    ("samurai", "Samuráis", 8), ("blue-archive", "Blue Archive", 16), ("hatsune-miku", "Hatsune Miku", 16),
    ("frieren", "Frieren", 8), ("genshin-impact", "Genshin Impact", 16), ("honkai-star-rail", "Honkai Star Rail", 8),
    ("zenless-zone-zero", "Zenless Zone Zero", 8), ("wuthering-waves", "Wuthering Waves", 8),
    ("rezero", "Re:Zero", 8), ("zero-two", "Zero Two", 8), ("spy-x-family", "Spy x Family", 8),
    ("nier-automata", "NieR Automata", 8), ("gundam", "Robots y mechas", 8),
    ("goddess-of-victory-nikke", "Nikke", 8), ("hololive", "Hololive", 8),
    ("ghibli", "Ghibli", 8), ("your-name", "Your Name", 8), ("anime-nature", "Paisajes anime", 16),
    ("girl", "Chicas anime", 16), ("cyberpunk", "Cyberpunk", 8), ("coding", "Programación", 8),
]


def get(url, tries=3):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40) as r:
                return r.read()
        except Exception:  # red inestable: reintenta
            if i == tries - 1:
                raise
            time.sleep(2 + i * 3)


def leer_json(ruta, defecto):
    try:
        return json.loads(ruta.read_text())
    except (OSError, ValueError):
        return defecto


def guardar_json(ruta, datos):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    tmp = ruta.with_suffix(".tmp")
    tmp.write_text(json.dumps(datos, ensure_ascii=False, indent=1))
    tmp.replace(ruta)


ENTRADA = re.compile(r'<a title="([^"]+?) live wallpaper" href=/([a-z0-9-]+)>.*?/media/(\d+)/([a-z0-9-]+)\.(\d+)x(\d+)\.jpg'
                     r'.*?<span class=frm>([^<]*)</span>', re.S)


def buscar_pagina(etiqueta, pagina):
    if etiqueta.startswith("?"):  # búsqueda de texto (una sola página)
        if pagina > 1:
            return
        url = f"{SITIO}/search?q={etiqueta[1:]}"
    else:
        url = f"{SITIO}/tag:{etiqueta}/" + (f"{pagina}/" if pagina > 1 else "")
    html = get(url).decode("utf-8", "replace")
    for titulo, slug, mid, base, w, h, formato in ENTRADA.findall(html):
        if "4K" in formato:
            yield {"id": mid, "slug": slug, "titulo": titulo.replace("&amp;", "&").replace("&#39;", "'"),
                   "thumb": f"{SITIO}/i/c/364x205/media/{mid}/{base}.{w}x{h}.jpg",
                   "preview": f"{SITIO}/media/{mid}/{base}.960x540.mp4"}


def brillo(jpg):
    """Luminancia media 0-1 de la miniatura (decide si va a Oscuros o Claros)."""
    from PIL import Image, ImageStat
    with Image.open(jpg) as im:
        return ImageStat.Stat(im.convert("L").resize((64, 36))).mean[0] / 255


def huella(img):
    """dHash de 64 bits: dos imágenes casi iguales dan huellas casi iguales."""
    from PIL import Image
    with Image.open(img) as im:
        g = im.convert("L").resize((9, 8))
        px = list(g.get_flattened_data()) if hasattr(g, "get_flattened_data") else list(g.getdata())
    return sum(1 << i for i in range(64) if px[(i // 8) * 9 + i % 8] > px[(i // 8) * 9 + i % 8 + 1])


def ya_tengo(listos):
    """Marca con "tengo" los del catálogo que ya están en tu carpeta de temas (aunque con otro nombre)."""
    mios = []
    for t in tc.catalogo():
        poster = tc.rutas(t)["poster"]
        if poster.exists():
            mios.append((huella(poster), t["id"]))
    for e in listos:
        h = huella(CARPETA / f"{e['id']}.jpg")
        e["tengo"] = next((tid for hm, tid in mios if bin(h ^ hm).count("1") <= 5), None)
        if not e["tengo"]:
            e.pop("tengo")


def bajar_archivos(e):
    base = CARPETA / e["id"]
    jpg, mp4 = base.with_suffix(".jpg"), base.with_suffix(".mp4")
    try:
        if not jpg.exists():
            jpg.write_bytes(get(e["thumb"]))
        if not mp4.exists():
            tmp = base.with_suffix(".part")
            tmp.write_bytes(get(e["preview"]))
            tmp.replace(mp4)
        e["brillo"] = round(brillo(jpg), 3)
        e["modo"] = "light" if e["brillo"] >= 0.5 else "dark"
        return e
    except Exception as err:
        print("falló", e["slug"], err, file=sys.stderr)
        return None


def actualizar():
    CARPETA.mkdir(parents=True, exist_ok=True)
    viejos = {e["id"]: e for e in leer_json(CATALOGO, [])}
    nuevos, vistos = [], set()
    for etiqueta, categoria, maximo in CATEGORIAS:
        n = 0
        for p in range(1, 4):
            if n >= maximo:
                break
            try:
                lista = list(buscar_pagina(etiqueta, p))
            except Exception as err:
                if p == 1:  # en páginas siguientes un 404 solo significa "no hay más"
                    print("no se pudo leer", etiqueta, err, file=sys.stderr)
                break
            for e in lista:
                if n >= maximo:
                    break
                if e["id"] in vistos:
                    continue
                vistos.add(e["id"])
                e["categoria"] = categoria
                nuevos.append({**viejos.get(e["id"], {}), **e})
                n += 1
        print(f"{categoria} ({etiqueta}): {n}", flush=True)
    with ThreadPoolExecutor(6) as ex:
        listos = [e for e in ex.map(bajar_archivos, nuevos) if e]
    ya_tengo(listos)
    guardar_json(CATALOGO, listos)
    print(f"catálogo: {len(listos)} fondos 4K")


def nombre_archivo(e):
    return re.sub(r"-+", "-", e["slug"].replace("live-wallpaper", "")).strip("-")[:60]


def bajar(mid, carpeta=None):
    e = next((x for x in leer_json(CATALOGO, []) if x["id"] == mid), None)
    if not e:
        sys.exit(f"{mid} no está en el catálogo")
    carpeta = carpeta or ("Claros" if e.get("modo") == "light" else "Oscuros")
    destino = tc.CARPETA / carpeta / f"{nombre_archivo(e)}.mp4"
    if e.get("tengo") and tc.buscar(e["tengo"]):
        print(tc.buscar(e["tengo"])["video"])
        return tc.buscar(e["tengo"])["video"]
    if destino.exists():
        print(destino)
        return destino
    destino.parent.mkdir(parents=True, exist_ok=True)
    crudo = destino.with_name(destino.stem + ".tmp-dl.mp4")
    subprocess.run(["curl", "-sL", "--retry", "3", "-A", UA["User-Agent"], "-o", str(crudo),
                    f"{SITIO}/dl/4k/{mid}/"], check=True)
    codec = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                            "stream=codec_name", "-of", "csv=p=0", str(crudo)],
                           capture_output=True, text=True).stdout.strip()
    if codec == "h264":
        crudo.replace(destino)
    else:  # HEVC/AV1 → H.264 (lo único que la GPU decodifica en 4K); tarda unos minutos
        conv = destino.with_name(destino.stem + ".tmp-conv.mp4")
        subprocess.run(["nice", "-n", "15", "ffmpeg", "-v", "error", "-y", "-i", str(crudo), "-an",
                        "-vf", "fps=30", "-c:v", "libx264", "-preset", "faster", "-crf", "20",
                        "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(conv)], check=True)
        conv.replace(destino)
        crudo.unlink(missing_ok=True)
    tema = tc.buscar(f"{carpeta}/{destino.stem}")
    if tema:
        tc.preparar(tema)
    print(destino)
    return destino


def avisar(titulo, texto, icono=None):
    args = ["notify-send", "-a", "Escritorios", titulo, texto]
    if icono:
        args += ["-i", str(icono)]
    subprocess.run(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def poner(mid, n, modo):
    e = next((x for x in leer_json(CATALOGO, []) if x["id"] == mid), None)
    if not e:
        sys.exit(f"{mid} no está en el catálogo")
    miniatura = CARPETA / f"{mid}.jpg"
    avisar(f"Descargando {e['titulo']}", f"En 4K · irá al escritorio {n} cuando termine", miniatura)
    try:
        destino = bajar(mid)
    except (subprocess.CalledProcessError, OSError) as err:
        avisar("No se pudo descargar", f"{e['titulo']}: {err}")
        sys.exit(1)
    fondo_id = f"{destino.parent.name}/{destino.stem}"
    estilo = tc.leer_estilo()
    estilo["mezcla"][modo][int(n) - 1] = fondo_id
    estilo["tema"], estilo["modo"] = f"mezcla:{modo}", modo
    estilo["ultimo"][modo] = estilo["tema"]
    tc.guardar_estilo(estilo)
    avisar(f"{e['titulo']} listo", f"Ya está en el escritorio {n} (SUPER+{n})", miniatura)


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "actualizar":
        actualizar()
    elif len(sys.argv) == 5 and sys.argv[1] == "poner":
        poner(sys.argv[2], sys.argv[3], sys.argv[4])
    elif len(sys.argv) >= 3 and sys.argv[1] == "bajar":
        bajar(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
    else:
        print(__doc__)
