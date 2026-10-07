#!/usr/bin/env python3
"""Renombra capturas viejas al nombre corto: 0012_01-23-45.webp -> 0012.webp.

    capturas-nombre-corto.py <carpeta> [<carpeta> ...]

El minuto no se pierde: primero se anota en .minutos.tsv (lo lee cuadernillo.py) y recién
después se renombra. Si se corta a la mitad no pasa nada: cuadernillo.py entiende los dos
nombres, y al volver a correrlo termina. Corrige los links de apuntes.md. Se saltea las
carpetas sin .cantidad (puede haber un video procesándose ahí).
"""
import os
import re
import sys

VIEJO = re.compile(r"^(\d+)_(\d\d-\d\d-\d\d)\.(webp|png)$")
MINUTOS = ".minutos.tsv"


def carpeta(raiz, archivos):
    viejos = [(f, VIEJO.match(f)) for f in sorted(archivos)]
    viejos = [(f, m) for f, m in viejos if m]
    if not viejos:
        return 0
    minutos = {}
    ruta_min = os.path.join(raiz, MINUTOS)
    if os.path.exists(ruta_min):
        for linea in open(ruta_min, encoding="utf-8"):
            nombre, _, marca = linea.rstrip("\n").partition("\t")
            if marca:
                minutos[nombre] = marca
    cambios = {}
    for f, m in viejos:
        nuevo = f"{m.group(1)}.{m.group(3)}"
        if nuevo in archivos and nuevo not in cambios.values():
            print(f"  ⚠️ ya existe {nuevo}, dejo {f} como está")
            continue
        cambios[f] = nuevo
        minutos[nuevo] = m.group(2)
    # 1) el minuto queda anotado antes de tocar ningún nombre
    tmp = ruta_min + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        for nombre in sorted(minutos, key=lambda n: int(re.match(r"\d+", n).group())):
            fh.write(f"{nombre}\t{minutos[nombre]}\n")
    os.replace(tmp, ruta_min)
    # 2) renombrar
    for f, nuevo in cambios.items():
        os.rename(os.path.join(raiz, f), os.path.join(raiz, nuevo))
    # 3) links de los apuntes
    for md in ("apuntes.md", "resumen.md"):
        ruta = os.path.join(raiz, md)
        if os.path.isfile(ruta):
            texto = open(ruta, encoding="utf-8").read()
            nuevo_texto = re.sub(r"\]\((\d+_\d\d-\d\d-\d\d\.(?:webp|png))\)",
                                 lambda m: f"]({cambios.get(m.group(1), m.group(1))})", texto)
            if nuevo_texto != texto:
                with open(ruta, "w", encoding="utf-8") as fh:
                    fh.write(nuevo_texto)
    return len(cambios)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    total = 0
    for base in sys.argv[1:]:
        for raiz, _, archivos in os.walk(os.path.abspath(base)):
            if not any(VIEJO.match(f) for f in archivos):
                continue
            if ".cantidad" not in archivos:
                print(f"⏭️ Salteada (sin .cantidad, puede estar procesándose): {raiz}")
                continue
            n = carpeta(raiz, set(archivos))
            total += n
            print(f"  ✅ {os.path.basename(raiz)}: {n} renombradas")
    print(f"Listo: {total} capturas con nombre corto")
    return 0


if __name__ == "__main__":
    sys.exit(main())
