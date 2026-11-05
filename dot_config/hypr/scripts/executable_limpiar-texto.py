#!/usr/bin/env python3
"""Preprocesa el texto ANTES de la limpieza de símbolos de leer-seleccion.sh.

Saca emojis (no aportan nada al escucharlos) y reemplaza URLs completas y
rutas de archivo por una frase corta ("este enlace" / "esta ruta") en vez de
deletrear cada segmento — leer un dominio o un path largo carácter por
carácter no ayuda a entender, solo confirma que ahí había un link/una ruta.
Borra también la actividad de herramientas de Claude y OpenCode que aparece en
la terminal (resúmenes "Ran 3 shell commands", llamadas como "Web Search(...)"
o "Fetch(...)", resultados "└ Did 1 search in 8s", comandos "$ ..." con su
salida, "+ Thought · 11.9s"): no es contenido de la respuesta.
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


_TOOL_ACTIVITY_RE = re.compile(
    r"[ \t]*(?:"
    r"Ran \d+ shell commands?\b"
    r"|[→←✱%◈][ \t]*(?:Explored|Read|Searched|Edit|Edited|Write|Wrote|Fetched|WebFetch|Web ?Search|Exa|Glob|Grep|List|Listed|Task)\b"
    r"|[+✻✢✳∴][ \t]*(?:Thought|Thinking)\b"
    r"|[●⏺][ \t]*(?:Web ?Search|Web ?Fetch|Fetch|Search|Bash|Read|Write|Edit|MultiEdit|Update|Grep|Glob|LS|List|Task|TodoWrite|NotebookEdit)\("
    r"|\$ (?!\d)"
    r"|[└⎿╰⎣][ \t]"
    r"|Allowed by\b"
    r"|Did \d+ \w+ in \d+(?:\.\d+)?s\b"
    r"|Received \d[\d.]*[ \t]?[KMGT]?B\b"
    r"|\(\d+ earlier lines?\)"
    r")"
)


# Un bloque de herramienta sigue hasta la primera línea de texto sin sangría; uno de
# comando ($ ...), hasta la siguiente línea en blanco.
def _strip_tool_activity(text):
    kept = []
    mode = None
    for line in text.split("\n"):
        blank = not line.strip()
        if mode == "shell":
            if not blank:
                continue
            mode = None
            continue
        if _TOOL_ACTIVITY_RE.match(line):
            mode = "shell" if line.lstrip().startswith("$") else "tool"
            continue
        if mode == "tool" and (blank or line[:1].isspace()):
            continue
        mode = None
        kept.append(line)
    return "\n".join(kept)


def main():
    text = sys.stdin.read()
    text = _strip_tool_activity(text)
    text = _EMOJI_RE.sub(" ", text)
    text = _URL_RE.sub(_replace_url, text)
    text = _PATH_RE.sub(_replace_path, text)
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
