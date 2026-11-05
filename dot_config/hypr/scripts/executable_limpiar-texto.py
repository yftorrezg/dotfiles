#!/usr/bin/env python3
"""Preprocesa el texto ANTES de la limpieza de símbolos de leer-seleccion.sh.

Saca emojis (no aportan nada al escucharlos) y reemplaza URLs completas y
rutas de archivo por una frase corta ("este enlace" / "esta ruta") en vez de
deletrear cada segmento — leer un dominio o un path largo carácter por
carácter no ayuda a entender, solo confirma que ahí había un link/una ruta.
Borra también lo que Claude y OpenCode muestran entre medio de la respuesta:
resúmenes de herramientas ("Ran 3 shell commands", "Searched for 1 pattern"),
llamadas y resultados de herramientas ("● Web Search(...)", "└ Did 1 search in
8s"), pensamientos ("+ Thought · 11.9s"), tiempos de turno ("Cooked for 50s"),
pistas ("· summary", "ctrl+o to expand"), tu prompt ("❯ ...") y los comandos
"$ ..." con su salida. El listado completo está en _TOOL_LINE_RE.
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


_TOOL_LINE_RE = re.compile(
    r"[ \t]*(?:"
    # resúmenes de grupo: "Ran 3 shell commands", "Searched for 1 pattern, read 1 file", "→ Explored: 2 reads"
    r"[→←●⏺]?[ \t]*(?:Ran|Running) \d+ shell commands?\b"
    r"|[→←●⏺]?[ \t]*(?:Searched|Searching|searched|searching) for \d+ patterns?\b"
    r"|[→←●⏺]?[ \t]*(?:Read|Reading|Listed|Listing) \d+ (?:files?|directory|directories)\b"
    r"|[→←●⏺]?[ \t]*(?:Explored|Exploring):"
    # llamadas a herramientas: "● Web Search(...)", "⏺ Bash(ls)", "● Fetch(https://...)"
    r"|[●⏺][ \t]*(?:Web Search|[A-Za-z_][A-Za-z0-9_]*)\("
    # herramientas de OpenCode: "→ Read src/a.ts", "← Edit src/a.ts"
    r"|[→←✱%◈][ \t]*(?:Read|Write|Edit|Glob|Grep|List|WebFetch|WebSearch|Exa|Task|Todos?)\b"
    # pensamiento: "+ Thought · 11.9s", "- Thought", "+ Thinking: ...", "✻ Thinking…"
    r"|[+\-][ \t]*Thought(?:[ \t]*·|[ \t\r]*$)"
    r"|[+\-✻✢✳∴][ \t]*Thinking(?::|…)"
    # tiempo de turno "* Cooked for 50s · done 3:37 a. m.", indicadores de carga "✻ Pondering…"
    r"|[*✻✢✳∴·•]?[ \t]*(?:Baked|Brewed|Churned|Cogitated|Cooked|Crunched|Sautéed|Worked) for \d"
    r"|[✻✢✳✶∴][ \t]*[A-Z][a-z]+…"
    # prompt del usuario en Claude y menús: "❯ sigue con la fase 3"
    r"|❯[ \t]"
    # resultados de herramientas: "└ Did 1 search in 8s", "⎿ Allowed by auto mode", "Received 31.8KB (200 OK)"
    r"|[└⎿╰⎣][ \t]"
    r"|(?:Allowed by|Did \d+ \w+ in \d+(?:\.\d+)?s|Received \d[\d.]*[ \t]?[KMGT]?B)\b"
    r"|…[ \t]*\+\d+ lines?"
    r"|\(\d+ earlier lines?\)"
    # comandos de OpenCode: "$ python3 - <<'EOF'" (su salida la saltea _strip_tool_activity)
    r"|\$ (?!\d)"
    # pie de mensaje de OpenCode: "▣ Build · modelo · 3.2s"
    r"|▣"
    r")"
)
# Pistas dentro de una línea de estado: "✻ Thinking… (esc to interrupt)".
_HINT_RE = re.compile(r"to interrupt|ctrl\+o to expand|\? for shortcuts")
# Pista al final de un bloque colapsado de Claude: "a. · summary".
_SUMMARY_HINT_RE = re.compile(r"[ \t]*·[ \t]*summar(?:y|ized)\b.*")


# Un bloque de herramienta sigue hasta la primera línea de texto sin sangría; uno de
# comando ($ ...), hasta la siguiente línea en blanco.
def _strip_tool_activity(text):
    text = _SUMMARY_HINT_RE.sub("", text)
    kept = []
    mode = None
    for line in text.split("\n"):
        blank = not line.strip()
        if mode == "shell":
            if not blank:
                continue
            mode = None
            continue
        if _TOOL_LINE_RE.match(line) or _HINT_RE.search(line):
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
