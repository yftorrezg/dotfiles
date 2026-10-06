#!/bin/bash
# SUPER+ALT+S: activa/desactiva la auto-captura del monitor donde está el foco (el del curso).
# Guarda solo cuando la pantalla cambia (ver auto-captura.py). Carpeta base: carpeta-capturas.conf.
PIDFILE="/tmp/auto-captura.pid"
DIRFILE="/tmp/auto-captura.dir"
SCRIPTS="$HOME/.config/hypr/scripts"

if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
    PID=$(cat "$PIDFILE")
    kill "$PID"
    while kill -0 "$PID" 2>/dev/null; do sleep 0.2; done
    DIR=$(cat "$DIRFILE")
    rm -f "$PIDFILE" "$DIRFILE"
    notify-send -t 4000 "Auto-captura OFF" "$(cat "$DIR/.cantidad" 2>/dev/null || echo 0) capturas en $DIR"
    exit 0
fi

BASE=$(cat "$SCRIPTS/carpeta-capturas.conf" 2>/dev/null)
if [ -z "$BASE" ] || ! mkdir -p "$BASE" 2>/dev/null || [ ! -w "$BASE" ]; then
    BASE="$HOME/Imágenes/Capturas"
fi

MONITOR=$(hyprctl monitors -j | python3 -c "import json,sys; print(next(m['name'] for m in json.load(sys.stdin) if m['focused']))")
TITULO=$(hyprctl activewindow -j | python3 -c "
import json,sys,re
t = json.load(sys.stdin).get('title','') or ''
t = re.sub(r' [-–|] (YouTube|Brave|Udemy|Platzi).*$', '', t)
print(re.sub(r'[^\w]+', '-', t).strip('-')[:40])" 2>/dev/null)
DIR="$BASE/auto_$(date +%Y%m%d_%H%M)${TITULO:+_$TITULO}"

python3 "$SCRIPTS/auto-captura.py" --monitor "$MONITOR" --out "$DIR" &
echo $! > "$PIDFILE"
echo "$DIR" > "$DIRFILE"
notify-send -t 3000 "Auto-captura ON ($MONITOR)" "$DIR"
