#!/usr/bin/env bash
# Abre la pantalla del celular (scrcpy por USB/WiFi). Si ya está abierta, la enfoca.
# Usado por la tecla "Celular" del Stream Deck XL.

dir=$(hyprctl clients -j | jq -r '.[] | select(.class == "scrcpy") | .address' | head -1)
if [[ -n $dir ]]; then
    hyprctl dispatch "hl.dsp.focus({ window = \"address:$dir\" })" >/dev/null
    exit 0
fi

adb start-server >/dev/null 2>&1
estado=$(adb get-state 2>&1)
case $estado in
    device) ;;
    *unauthorized*)
        notify-send -i scrcpy "Celular" "Acepta «¿Permitir depuración USB?» en el teléfono (marca «Permitir siempre»)."
        exit 1 ;;
    *)
        notify-send -i scrcpy "Celular" "No veo el celular. Conecta el cable y activa la Depuración USB."
        exit 1 ;;
esac

# --stay-awake: no se bloquea mientras está conectado; --turn-screen-off ahorra batería
# (la pantalla del teléfono se apaga pero sigue viéndose en la PC).
exec scrcpy --window-title "Celular" --stay-awake --turn-screen-off --shortcut-mod=lalt
