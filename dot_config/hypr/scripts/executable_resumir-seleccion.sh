#!/usr/bin/env bash
# Punto de entrada del resumen de selección para Hyprland y OpenDeck.
set -uo pipefail

export PATH="$HOME/.local/bin:$PATH"
export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}"

exec python3 "$HOME/.config/hypr/scripts/resumir_seleccion.py" "$@"
