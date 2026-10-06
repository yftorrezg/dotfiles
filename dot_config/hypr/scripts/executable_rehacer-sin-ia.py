#!/usr/bin/env python3
"""Rehace con IA los apuntes de las clases que quedaron sin resumen de Claude.

    rehacer-sin-ia.py <carpeta> [<carpeta> ...]

Una clase "quedó sin IA" si tiene apuntes.md pero no .apuntes-ia.json (p. ej. se agotó la
cuota de Claude o no respondió). No hace falta el video: los subtítulos quedan guardados en
la carpeta y el código se lee de las capturas (OCR). Se saltean las hechas a propósito con
SIN_IA=1 (tienen el archivo .sin-ia). Después arma tarjetas, INDICE.md y el panel.
"""
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))


def pendientes(base):
    for raiz, _, archivos in os.walk(os.path.abspath(base)):
        if "apuntes.md" in archivos and ".apuntes-ia.json" not in archivos and ".sin-ia" not in archivos:
            yield raiz


def titulo_de(carpeta):
    try:
        primera = open(os.path.join(carpeta, "apuntes.md"), encoding="utf-8").readline()
        return primera.removeprefix("# 📓 ").strip() or os.path.basename(carpeta)
    except OSError:
        return os.path.basename(carpeta)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    clases = sorted(c for base in sys.argv[1:] for c in pendientes(base))
    if not clases:
        print("✅ No hay clases sin IA")
        return 0
    print(f"🔁 {len(clases)} clases sin IA: se rehacen")
    fallas = 0
    for c in clases:
        print(f"===== {os.path.basename(c)} =====")
        subprocess.run([sys.executable, os.path.join(AQUI, "cuadernillo.py"), c, "--forzar", "--titulo", titulo_de(c)])
        if os.path.exists(os.path.join(c, ".apuntes-ia.json")):
            subprocess.run([sys.executable, os.path.join(AQUI, "tarjetas.py"), c, "--forzar"])
        else:
            fallas += 1
        padre = os.path.dirname(c)
        if os.path.basename(padre) == "capturas":
            subprocess.run([sys.executable, os.path.join(AQUI, "cuadernillo.py"), "--indice", padre],
                           stdout=subprocess.DEVNULL)
    subprocess.run([sys.executable, os.path.join(AQUI, "panel-cursos.py")], stdout=subprocess.DEVNULL)
    print(f"Listo: {len(clases) - fallas} de {len(clases)} rehechas con IA")
    return 1 if fallas else 0


if __name__ == "__main__":
    sys.exit(main())
