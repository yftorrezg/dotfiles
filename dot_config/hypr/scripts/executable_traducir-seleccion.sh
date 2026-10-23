#!/usr/bin/env bash
# Punto de entrada común para Hyprland y el botón Run Command de OpenDeck.
set -uo pipefail

export PATH="$HOME/.local/bin:$PATH"
export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}"

exec python3 "$HOME/.config/hypr/scripts/traducir_seleccion.py" "$@"
