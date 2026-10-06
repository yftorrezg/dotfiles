#!/bin/bash
# Ctrl+Shift+D: crear/actualizar la carpeta donde se guardan las capturas (captura-guardar.sh la lee de acá).

CONFIG_FILE="$HOME/.config/hypr/scripts/carpeta-capturas.conf"
CURRENT=$(cat "$CONFIG_FILE" 2>/dev/null)
[ -z "$CURRENT" ] && CURRENT="$HOME/Imágenes/Capturas"
mkdir -p "$CURRENT"

if ! command -v zenity >/dev/null 2>&1; then
    notify-send -t 4000 "Falta zenity" "Instalá con: sudo pacman -S zenity"
    exit 1
fi

NEW=$(zenity --file-selection --directory --title="Carpeta para guardar capturas" --filename="$CURRENT/")

if [ -n "$NEW" ]; then
    mkdir -p "$NEW"
    echo "$NEW" > "$CONFIG_FILE"
    notify-send -t 2500 "Carpeta de capturas actualizada" "$NEW"
fi
