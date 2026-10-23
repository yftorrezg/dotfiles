#!/usr/bin/env python3
"""Capturas clave de los videos SUELTOS de ~/Vídeos/Capturas de YouTube (una carpeta = un video,
con las capturas al lado de apuntes.md). capturas_clave.py trabaja sobre cursos con clases en
subcarpetas; este arma lo mismo para una carpeta plana.

Uso: capturas-clave-sueltos.py [--forzar] <carpeta de video> [más carpetas…]
     capturas-clave-sueltos.py --todos [<carpeta "Capturas de YouTube">]

Por video deja:
  .ocr-capturas.json, .clave.txt   (los mismos que usa cuadernillo.py para elegir las pantallas)
  capturas-clave/                  enlaces duros (0 espacio extra) con nombre "NNNN · hh-mm-ss.webp"
  capturas-clave/RESUMEN.md        cuántas quedaron de cuántas
Lo que borres de capturas-clave/ no vuelve a agregarse (manifiesto .ya-agregadas.txt).
"""
import importlib.util
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("capturas_clave", os.path.join(AQUI, "capturas_clave.py"))
cc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cc)

SALIDA = "capturas-clave"
MANIFIESTO = ".ya-agregadas.txt"


def minutos(carpeta):
    """{captura: hh-mm-ss} desde .minutos.tsv (0001.webp<TAB>01-23-45)."""
    ruta = os.path.join(carpeta, ".minutos.tsv")
    out = {}
    if os.path.isfile(ruta):
        for linea in open(ruta, encoding="utf-8"):
            partes = linea.rstrip("\n").split("\t")
            if len(partes) == 2:
                out[partes[0]] = partes[1]
    return out


def procesar(carpeta, forzar=False):
    carpeta = os.path.abspath(carpeta)
    todas = cc.imagenes(carpeta)
    if not todas:
        print(f"(sin capturas en {carpeta})")
        return None
    clave = cc.elegir(carpeta, forzar=forzar)
    if clave is None:
        sys.exit("Falta tesseract (pacman -S tesseract tesseract-data-spa)")
    mins = minutos(carpeta)
    esenc = cc.esenciales(carpeta, forzar=forzar)
    for salida, lista, titulo in ((SALIDA, clave, "🔑 Capturas clave"), (cc.SALIDA_ESENCIALES, esenc, "⭐ Capturas esenciales")):
        destino = os.path.join(carpeta, salida)
        os.makedirs(destino, exist_ok=True)
        manif = os.path.join(destino, MANIFIESTO)
        ya = set(open(manif, encoding="utf-8").read().splitlines()) if os.path.exists(manif) else set()
        nuevas, esperados = [], set()
        for f in lista:
            base, ext = os.path.splitext(f)
            m = re.match(r"\d+", base)
            numero = f"{int(m.group()):04d}" if m else base
            minuto = mins.get(f)
            nombre = f"{numero}" + (f" · {minuto}" if minuto else "") + ext.lower()
            esperados.add(nombre)
            if f in ya:
                continue
            dst = os.path.join(destino, nombre)
            if not os.path.exists(dst):
                try:
                    os.link(os.path.join(carpeta, f), dst)
                except OSError:
                    import shutil
                    shutil.copy2(os.path.join(carpeta, f), dst)
            nuevas.append(f)
        if nuevas:
            with open(manif, "a", encoding="utf-8") as h:
                h.write("\n".join(nuevas) + "\n")
        for f in os.listdir(destino):  # lo que dejó de corresponder (regla nueva): sale, nunca la única copia
            ruta = os.path.join(destino, f)
            if f.lower().endswith(cc.EXT) and f not in esperados and os.stat(ruta).st_nlink >= 2:
                os.remove(ruta)
        with open(os.path.join(destino, "RESUMEN.md"), "w", encoding="utf-8") as h:
            h.write(f"# {titulo} · {os.path.basename(carpeta)}\n\n"
                    f"**{len(lista)} de {len(todas)}** capturas ({100 * len(lista) // max(1, len(todas))} %). "
                    + ("Se quitaron los pasos intermedios (código a medio escribir, cursor que se movió); queda el "
                       "estado final de cada cosa, el resultado en el navegador y las diapositivas. "
                       if salida == SALIDA else "La mitad de las clave: las que más contenido nuevo traen, más el estado final. ")
                    + "Todas las capturas siguen en la carpeta del video.\n")
        print(f"{titulo.split()[0]} {os.path.basename(carpeta)}: {len(lista)} de {len(todas)} (+{len(nuevas)} nuevas)", flush=True)
    return len(clave), len(todas)


def sueltos(base):
    for d in sorted(os.listdir(base)):
        c = os.path.join(base, d)
        if os.path.isfile(os.path.join(c, "apuntes.md")) and cc.imagenes(c):
            yield c


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    forzar = "--forzar" in args
    args = [a for a in args if a != "--forzar"]
    if args and args[0] == "--todos":
        base = args[1] if len(args) > 1 else os.path.expanduser("~/Vídeos/Capturas de YouTube")
        args = list(sueltos(base))
    for c in args:
        procesar(c, forzar)
