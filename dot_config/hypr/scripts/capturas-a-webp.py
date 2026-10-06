#!/usr/bin/env python3
"""Pasa las capturas viejas (PNG) a WebP SIN pérdida: mismos píxeles, ~43 % menos de espacio.

    capturas-a-webp.py <carpeta> [<carpeta> ...]

Recorre las carpetas (y subcarpetas) buscando capturas con nombre de minuto
(0012_01-23-45.png). Cada una se convierte, se vuelve a abrir y se compara píxel por
píxel con la original; SOLO si es idéntica se borra el PNG. Después corrige los links
de apuntes.md / resumen.md de esa carpeta. Se saltea las carpetas sin .cantidad
(capturas a medio hacer: puede haber un video procesándose ahí).
"""
import multiprocessing
import os
import re
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(line_buffering=True)  # que el log se vea al momento

CAPTURA = re.compile(r"^(\d+(?:_\d\d-\d\d-\d\d)?)\.png$")  # 0012.png o 0012_01-23-45.png


def convertir(ruta_png):
    """-> (bytes antes, bytes después) o None si algo no coincidió (el PNG queda)."""
    os.nice(19)
    webp = ruta_png[:-4] + ".webp"
    tmp = webp + ".tmp"
    try:
        with Image.open(ruta_png) as im:
            im.load()
            modo = "RGBA" if im.mode in ("RGBA", "LA", "P") else "RGB"
            original = im.convert(modo)
        original.save(tmp, "WEBP", lossless=True, method=1, quality=50)
        with Image.open(tmp) as nueva:
            if not np.array_equal(np.asarray(nueva.convert(modo)), np.asarray(original)):
                os.remove(tmp)
                return None
        antes = os.path.getsize(ruta_png)
        os.replace(tmp, webp)
        os.remove(ruta_png)
        return antes, os.path.getsize(webp)
    except Exception as e:  # noqa: BLE001 - una imagen rota no frena al resto
        print(f"  ⚠️ {ruta_png}: {e}", file=sys.stderr)
        if os.path.exists(tmp):
            os.remove(tmp)
        return None


def corregir_links(carpeta):
    """](0012_01-23-45.png) -> .webp en los .md, solo si el .webp ya existe."""
    for md in ("apuntes.md", "resumen.md"):
        ruta = os.path.join(carpeta, md)
        if not os.path.isfile(ruta):
            continue
        texto = open(ruta, encoding="utf-8").read()
        nuevo = re.sub(r"\]\((\d+(?:_\d\d-\d\d-\d\d)?)\.png\)",
                       lambda m: f"]({m.group(1)}.webp)" if os.path.exists(os.path.join(carpeta, m.group(1) + ".webp"))
                       else m.group(0), texto)
        if nuevo != texto:
            with open(ruta, "w", encoding="utf-8") as f:
                f.write(nuevo)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    carpetas, salteadas = [], []
    for base in sys.argv[1:]:
        for raiz, _, archivos in os.walk(os.path.abspath(base)):
            pngs = [os.path.join(raiz, f) for f in sorted(archivos) if CAPTURA.match(f)]
            if not pngs:
                continue
            (carpetas if ".cantidad" in archivos else salteadas).append((raiz, pngs))
    for raiz, _ in salteadas:
        print(f"⏭️ Salteada (sin .cantidad, puede estar procesándose): {raiz}")
    total = sum(len(p) for _, p in carpetas)
    print(f"🖼️ {total} capturas PNG en {len(carpetas)} carpetas")
    antes = despues = hechas = fallas = 0
    with multiprocessing.Pool(os.cpu_count()) as pool:
        for raiz, pngs in carpetas:
            for r in pool.imap_unordered(convertir, pngs, chunksize=8):
                if r:
                    antes += r[0]; despues += r[1]; hechas += 1
                else:
                    fallas += 1
            corregir_links(raiz)
            print(f"  ✅ {os.path.basename(raiz)}: {len(pngs)} · llevo {hechas}/{total}"
                  f" · ahorro {(antes - despues) / 2**30:.2f} GB")
    print(f"Listo: {hechas} convertidas, {fallas} sin tocar · {antes / 2**30:.2f} GB → {despues / 2**30:.2f} GB")
    return 1 if fallas else 0


if __name__ == "__main__":
    sys.exit(main())
