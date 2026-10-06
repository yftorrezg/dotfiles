#!/bin/bash
# SUPER+SHIFT+S: selección de región en 1 paso -> solo copia al portapapeles, no guarda archivo.

geom=$(slurp) || exit 0  # Esc cancela sin hacer nada

grim -g "$geom" - | wl-copy
notify-send -t 1500 "Captura copiada al portapapeles"
