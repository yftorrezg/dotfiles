#!/usr/bin/env python3
"""Prepara para rehacer las clases cuyos apuntes se hicieron SIN la voz del profe (sin subtítulos:
solo con el OCR de la pantalla). Ahora cuadernillo.py transcribe con Whisper (GPU) y lee los
subtítulos de Udemy (clase-es.srt), así que rehacerlas da apuntes mucho mejores.

    rehacer-con-voz.py <curso> [más cursos…]          # marca las clases (con respaldo) y dice cuántas
    rehacer-con-voz.py --ver <curso> [más cursos…]    # solo cuenta, no toca nada

No borra nada: copia apuntes.md, resumen.md y los .json de la IA a <clase>/.sin-voz/ (Obsidian no
muestra las carpetas con punto) y marca la clase con .rehacer. Los apuntes viejos siguen en su lugar
(el panel y tus casillas no cambian) hasta que cuadernillo.py los reemplaza y borra la marca. Las
capturas no se rehacen y tarjetas.md se regenera conservando tu repaso (<!--SR:…-->).
Después: curso-a-apuntes.sh <curso> (o encolarlo) rehace solo esas clases.
Se saltean las hechas a propósito sin IA (.sin-ia) y las ya marcadas.
"""
import os
import shutil
import sys

COPIAR = ("apuntes.md", "resumen.md", ".apuntes-ia.json", ".resumen-ia.json")
VOZ = "Lo que dice el profe"


def sin_voz(carpeta_capturas):
    for d in sorted(os.listdir(carpeta_capturas)):
        c = os.path.join(carpeta_capturas, d)
        a = os.path.join(c, "apuntes.md")
        if os.path.isfile(a) and not os.path.exists(os.path.join(c, ".sin-ia")):
            if VOZ not in open(a, encoding="utf-8", errors="replace").read() or os.path.exists(os.path.join(c, ".rehacer")):
                yield c


def main():
    args = sys.argv[1:]
    ver = bool(args) and args[0] == "--ver"
    args = args[1:] if ver else args
    if not args:
        sys.exit(__doc__)
    for curso in args:
        cap = os.path.join(os.path.abspath(curso), "capturas")
        if not os.path.isdir(cap):
            print(f"(no es un curso con capturas/: {curso})")
            continue
        clases = list(sin_voz(cap))
        if not ver:
            for c in clases:
                dst = os.path.join(c, ".sin-voz")
                os.makedirs(dst, exist_ok=True)
                for f in COPIAR:
                    if os.path.exists(os.path.join(c, f)) and not os.path.exists(os.path.join(dst, f)):
                        shutil.copy2(os.path.join(c, f), os.path.join(dst, f))
                open(os.path.join(c, ".rehacer"), "w").close()
        print(f"{'🔍' if ver else '♻️ marcadas'} {len(clases)} clases sin voz · {os.path.basename(os.path.abspath(curso))}")


if __name__ == "__main__":
    main()
