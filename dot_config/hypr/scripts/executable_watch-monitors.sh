#!/usr/bin/env bash
# Reaplica la config de monitores cada vez que nwg-displays guarda cambios.
# Vigila la carpeta (no el archivo directo) para funcionar incluso antes
# de que nwg-monitors.conf exista por primera vez.
DIR="$HOME/.config/hypr/config"
TARGET="nwg-monitors.conf"
echo "Watching $DIR/$TARGET — Ctrl+C para salir"
inotifywait -m -e close_write -e create --format '%f' "$DIR" | while read -r file; do
    if [ "$file" = "$TARGET" ]; then
        echo "[reload] cambio detectado, aplicando..."
        hyprctl reload
    fi
done
