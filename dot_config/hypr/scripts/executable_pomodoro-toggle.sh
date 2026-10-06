#!/bin/bash
# Pomodoro simple: un toque arranca 25 min de foco, otro toque lo cancela.
PIDFILE="/tmp/pomodoro.pid"

if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
    kill "$(cat "$PIDFILE")" 2>/dev/null
    rm -f "$PIDFILE"
    notify-send "Pomodoro" "Cancelado"
else
    (
        notify-send "Pomodoro" "Arrancó: 25 minutos de foco"
        sleep 1500
        notify-send "Pomodoro" "¡Terminó! Tomate 5 minutos de descanso"
        rm -f "$PIDFILE"
    ) &
    echo $! > "$PIDFILE"
fi
