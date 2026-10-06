#!/usr/bin/env python3
"""Abre un .md con doble clic: en Obsidian si está dentro de una bóveda (vault), si no en VS Code.

Es la app por defecto para text/markdown (abrir-markdown.desktop). Obsidian solo abre
archivos que estén dentro de una bóveda registrada; por eso ~/Vídeos (cursos, apuntes y
resúmenes) está registrada como bóveda. Un README suelto de un proyecto va a VS Code.
"""
import json
import os
import subprocess
import sys
import urllib.parse


def bovedas():
    try:
        datos = json.load(open(os.path.expanduser("~/.config/obsidian/obsidian.json"), encoding="utf-8"))
        return [os.path.realpath(v["path"]) for v in datos.get("vaults", {}).values() if v.get("path")]
    except (OSError, ValueError):
        return []


def main():
    if len(sys.argv) < 2:
        return 1
    archivo = sys.argv[1]
    if archivo.startswith("file://"):
        archivo = urllib.parse.unquote(urllib.parse.urlparse(archivo).path)
    archivo = os.path.realpath(archivo)
    if any(archivo.startswith(b + os.sep) for b in bovedas()):
        # path= : Obsidian busca solo la bóveda más específica que contiene el archivo
        uri = "obsidian://open?path=" + urllib.parse.quote(archivo, safe="")
        subprocess.Popen(["obsidian", uri], start_new_session=True,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        subprocess.Popen(["code", "--open-url", "vscode://file" + archivo], start_new_session=True,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return 0


if __name__ == "__main__":
    sys.exit(main())
