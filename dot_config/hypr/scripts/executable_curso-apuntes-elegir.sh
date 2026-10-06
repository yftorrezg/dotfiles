#!/bin/bash
# SUPER+ALT+A: elegir la carpeta de un curso descargado y procesarlo entero en segundo plano
# (capturas + apuntes de cada clase + índice). Va a la misma cola que los links de YouTube
# (cola-capturas.sh): si ya se está procesando algo, espera su turno en vez de competir por la
# CPU. El detalle queda en ~/.cache/auto-captura/.
SCRIPTS="$HOME/.config/hypr/scripts"
INICIO="$(xdg-user-dir VIDEOS 2>/dev/null || echo "$HOME")/Descargas/"
[ -d "$INICIO" ] || INICIO="$HOME/"
CURSO=$(zenity --file-selection --directory --title="📚 Carpeta del curso para sacar apuntes" --filename="$INICIO") || exit 0
bash "$SCRIPTS/cola-capturas.sh" encolar curso "$CURSO" "📚 $(basename "$CURSO")" >/dev/null
