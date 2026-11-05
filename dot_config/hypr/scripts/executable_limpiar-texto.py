#!/usr/bin/env python3
"""Preprocesa el texto ANTES de la limpieza de símbolos de leer-seleccion.sh.

Saca emojis (no aportan nada al escucharlos) y reemplaza URLs completas y
rutas de archivo por una frase corta ("este enlace" / "esta ruta") en vez de
deletrear cada segmento — leer un dominio o un path largo carácter por
carácter no ayuda a entender, solo confirma que ahí había un link/una ruta.
Borra también las líneas de resumen de herramientas de la terminal
("Ran 1 shell command", "Ran 3 shell commands"): no son contenido y no
aportan nada al escucharlas.
Corre primero en el pipeline para operar sobre el texto "crudo", antes de que
las reglas de sed conviertan las barras en pausas.
"""
import re
import sys

_EMOJI_RE = re.compile(
    "["
    "\U0001F1E6-\U0001F1FF"
    "\U0001F300-\U0001FAFF"
    "\U00002600-\U000027BF"
    "\U0000FE00-\U0000FE0F"
    "\U0000200D"
    "]+"
)

_URL_RE = re.compile(r"https?://\S+")
_TRAILING_PUNCT = ".,;:!?)]}'\"`"


def _replace_url(match):
    url = match.group(0)
    trimmed = url.rstrip(_TRAILING_PUNCT)
    trailing = url[len(trimmed):]
    return " este enlace " + trailing


_PATH_RE = re.compile(r"~?/[\w.~-]+(?:/[\w.~-]+)+")


def _looks_like_real_path(path):
    segments = path.strip("~/").split("/")
    return any(re.search(r"[A-Za-z]", seg) for seg in segments)


def _replace_path(match):
    path = match.group(0)
    if _looks_like_real_path(path):
        return " esta ruta "
    return path


_TOOL_SUMMARY_RE = re.compile(
    r"^[ \t\r\u00a0]*Ran \d+ shell commands?[ \t\r\u00a0]*(?:\n|$)",
    re.IGNORECASE | re.MULTILINE,
)


def main():
    text = sys.stdin.read()
    text = _TOOL_SUMMARY_RE.sub("", text)
    text = _EMOJI_RE.sub(" ", text)
    text = _URL_RE.sub(_replace_url, text)
    text = _PATH_RE.sub(_replace_path, text)
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
