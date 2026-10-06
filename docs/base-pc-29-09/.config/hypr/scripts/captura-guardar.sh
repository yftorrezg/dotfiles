#!/bin/bash
# Ctrl+Shift+S: selección de región en 1 paso -> guarda en la carpeta configurada + copia al portapapeles.
# Sin ventana de confirmación, sin abrir editor.

CONFIG_FILE="$HOME/.config/hypr/scripts/carpeta-capturas.conf"
DEST_DIR=$(cat "$CONFIG_FILE" 2>/dev/null)
[ -z "$DEST_DIR" ] && DEST_DIR="$HOME/Imágenes/Capturas"
mkdir -p "$DEST_DIR"

geom=$(slurp) || exit 0  # Esc cancela sin hacer nada

FILE="$DEST_DIR/captura_$(date +%Y%m%d_%H%M%S).png"
grim -g "$geom" "$FILE" || exit 1
wl-copy < "$FILE"
notify-send -t 2000 "Captura guardada" "$FILE"
