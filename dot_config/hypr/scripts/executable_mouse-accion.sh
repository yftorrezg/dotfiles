#!/usr/bin/env bash
# Acción de los botones 7/8/9 según la memoria actual del mouse.
# Uso: mouse-accion.sh 7|8|9
. "$(dirname "$0")/mouse-lib.sh"
b="$1"; m=$(cat "$MODO_FILE" 2>/dev/null || echo 1)
S="$HOME/.config/hypr/scripts"
case "$m:$b" in
  1:7) exec bash "$S/leer-seleccion.sh" ;;                 # leer (SUPER+R)
  1:8) exec bash "$S/captura-guardar.sh" ;;                # captura guardada (CTRL+SHIFT+S)
  1:9) exec python3 "$S/estudiar.py" ;;                    # modo estudiar (SUPER+I)
  # M2 programacion (VS Code): guardar, abrir archivo, terminal
  2:7) exec ydotool key 29:1 31:1 31:0 29:0 ;;             # CTRL+S
  2:8) exec ydotool key 29:1 25:1 25:0 29:0 ;;             # CTRL+P
  2:9) exec ydotool key 29:1 41:1 41:0 29:0 ;;             # CTRL+` (terminal)
  # M3 redes
  3:7) exec bash "$S/app-web.sh" youtube ;;
  3:8) exec bash "$S/app-web.sh" telegram ;;
  3:9) exec bash "$S/app-web.sh" instagram ;;
  *) notify-send -t 1000 -u low "Mouse" "M$m · botón $b sin asignar" ;;
esac
