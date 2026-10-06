#!/usr/bin/env bash
# Cambia la "capa" de los botones 7/8/9 del mouse (M1/M2/M3, por software) y avisa.
# Uso: mouse-modo.sh 1|2|3
. "$(dirname "$0")/mouse-lib.sh"
m="${1:-1}"
mkdir -p "$(dirname "$MODO_FILE")"; echo "$m" > "$MODO_FILE"
case $m in 1) n="M1 · Estudio";; 2) n="M2 · Programación";; 3) n="M3 · Redes";; esac
notify-send -t 1200 -u low "Mouse" "$n"
