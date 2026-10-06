#!/bin/bash
# Ctrl+Shift+S: selección de región en 1 paso -> guarda en la carpeta configurada + copia al portapapeles.
# Sin ventana de confirmación, sin abrir editor.

CONFIG_FILE="$HOME/.config/hypr/scripts/carpeta-capturas.conf"
DEST_DIR=$(cat "$CONFIG_FILE" 2>/dev/null)
DEST_DIR="${DEST_DIR/#\~/$HOME}"
# Si la carpeta no se puede usar (p. ej. un disco externo sin montar), cae a la local y avisa.
if [ -z "$DEST_DIR" ] || ! mkdir -p "$DEST_DIR" 2>/dev/null || [ ! -w "$DEST_DIR" ]; then
    [ -n "$DEST_DIR" ] && notify-send -t 4000 "Carpeta de capturas no disponible" "$DEST_DIR → uso ~/Imágenes/Capturas"
    DEST_DIR="$HOME/Imágenes/Capturas"
    mkdir -p "$DEST_DIR"
fi

geom=$(slurp) || exit 0  # Esc cancela sin hacer nada

FILE="$DEST_DIR/captura_$(date +%Y%m%d_%H%M%S).png"
grim -g "$geom" "$FILE" || exit 1
wl-copy < "$FILE"
notify-send -t 2000 "Captura guardada" "$FILE"
