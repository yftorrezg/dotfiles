#!/usr/bin/env bash
# Fuerza el cierre de LibreOffice cuando se cuelga (SIGKILL directo, sin pasar por btop).

if pkill -9 -f 'soffice\.bin'; then
    notify-send -a "LibreOffice" "Proceso matado" "Se forzó el cierre de LibreOffice."
else
    notify-send -a "LibreOffice" "Nada que matar" "No había ningún proceso de LibreOffice corriendo."
fi
