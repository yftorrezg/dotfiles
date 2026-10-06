#!/bin/bash
# SUPER+C: abre la sesión de estudio (curso + apuntes + extras opcionales)
# en el workspace dedicado "estudio". Los slots se configuran con SUPER+ALT+C.

CONFIG_FILE="$HOME/.config/hypr/scripts/curso.conf"

if [ ! -f "$CONFIG_FILE" ]; then
    notify-send -t 4000 "Sesión de estudio" "Todavía no configuraste nada. Usá SUPER+ALT+C primero."
    exit 1
fi

# shellcheck disable=SC1090
source "$CONFIG_FILE"

abrir_slot() {
    local target="$1"
    [ -z "$target" ] && return
    target="${target/#\~/$HOME}"
    if [[ "$target" =~ ^https?:// ]]; then
        brave --new-window "$target" &
    elif [[ "$target" == /* && -e "$target" ]]; then
        xdg-open "$target" &
    else
        eval "$target" &
    fi
}

# Hyprland con config Lua: la sintaxis vieja "dispatch workspace name:estudio" ya no anda.
hyprctl dispatch 'hl.dsp.focus({ workspace = "name:estudio" })' >/dev/null

abrir_slot "$SLOT1"
sleep 0.4
abrir_slot "$SLOT2"
sleep 0.4
abrir_slot "$SLOT3"
sleep 0.4
abrir_slot "$SLOT4"
