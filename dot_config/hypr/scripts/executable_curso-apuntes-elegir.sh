#!/bin/bash
# SUPER+ALT+A: elegir la carpeta de un curso descargado y procesarlo entero en segundo plano
# (capturas + apuntes de cada clase + índice). Va a la misma cola que los links de YouTube
# (cola-capturas.sh): si ya se está procesando algo, espera su turno en vez de competir por la
# CPU. El detalle queda en ~/.cache/auto-captura/.
SCRIPTS="$HOME/.config/hypr/scripts"
INICIO="$(xdg-user-dir VIDEOS 2>/dev/null || echo "$HOME")/Descargas/"
[ -d "$INICIO" ] || INICIO="$HOME/"
# Los cursos en disco se apuntan con OpenCode (suscripción Go); los links de YouTube
# (SUPER+ALT+Y) siguen con Claude. El modelo se elige con APUNTES_MODELO_OPENCODE.
export APUNTES_MOTOR=opencode
CURSO=$(zenity --file-selection --directory --title="📚 Carpeta del curso para sacar apuntes" --filename="$INICIO") || exit 0
# Rechaza rutas vacías o demasiado amplias (p. ej. "/" cuando el disco no estaba montado).
CURSO="${CURSO%/}"
case "$CURSO" in
    ""|"$HOME"|/|/run|/run/media|/run/media/*/|/mnt|/home|/media)
        notify-send -u critical "Auto Captura" "Carpeta no válida: «${CURSO:-/}». Elige la carpeta de un curso." ; exit 1 ;;
esac
[ -d "$CURSO" ] || { notify-send -u critical "Auto Captura" "La carpeta no existe: $CURSO"; exit 1; }
bash "$SCRIPTS/cola-capturas.sh" encolar curso "$CURSO" "📚 $(basename "$CURSO")" >/dev/null
