#!/bin/bash
# Abre un .md en VS Code en modo Preview y lo trae al escritorio donde estás,
# en vez de saltar al escritorio donde VS Code ya estaba abierto.
FILE="$1"
CURRENT_WS=$(hyprctl activeworkspace -j | python3 -c "import json,sys;print(json.load(sys.stdin)['id'])")

code --open-url "vscode://file${FILE}"

sleep 0.6

ADDR=$(hyprctl clients -j | python3 -c "
import json,sys
wins = [w for w in json.load(sys.stdin) if w['class']=='code']
wins.sort(key=lambda w: w['focusHistoryID'])
print(wins[0]['address'] if wins else '')
")

if [ -n "$ADDR" ]; then
    # Sintaxis Lua 0.56: la ventana se indica con window = "address:0x..." (antes usaba
    # address = "...", que no es un argumento válido y podía mover la ventana activa).
    hyprctl dispatch "hl.dsp.window.move({ workspace = \"${CURRENT_WS}\", window = \"address:${ADDR}\", follow = false })"
fi
