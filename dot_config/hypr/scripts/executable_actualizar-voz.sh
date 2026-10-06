#!/bin/bash
# SUPER+ALT+R: elegir voz y velocidad en una sola ventanita (elegir-voz.py, GTK4/libadwaita).
# Arranca mostrando la última configuración guardada. Config en voz.conf.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if ! python3 -c "import gi; gi.require_version('Gtk','4.0'); gi.require_version('Adw','1')" 2>/dev/null; then
    notify-send -t 4000 "Falta GTK4/libadwaita" "Instalá con: sudo pacman -S python-gobject gtk4 libadwaita"
    exit 1
fi

exec python3 "$SCRIPT_DIR/elegir-voz.py"
