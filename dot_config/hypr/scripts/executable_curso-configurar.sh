#!/bin/bash
# SUPER+ALT+C: configura/actualiza los links o comandos de la sesión de estudio.
# Cada campo acepta una URL (se abre en Brave, ventana nueva) o un comando
# cualquiera (ej: code ~/proyecto, xdg-open ~/archivo.pdf).

CONFIG_FILE="$HOME/.config/hypr/scripts/curso.conf"

if ! command -v zenity >/dev/null 2>&1; then
    notify-send -t 4000 "Falta zenity" "Instalá con: sudo pacman -S zenity"
    exit 1
fi

RESULT=$(zenity --forms \
    --title="Configurar sesión de estudio" \
    --text="Pegá una URL (curso, Drive, Obsidian web...) o un comando (ej: code ~/proyecto). Dejá vacío lo que no uses." \
    --add-entry="Curso (izquierda)" \
    --add-entry="Apuntes (derecha)" \
    --add-entry="Extra 1 (opcional)" \
    --add-entry="Extra 2 (opcional)" \
    --separator="|")

[ $? -ne 0 ] && exit 0

SLOT1=$(echo "$RESULT" | cut -d'|' -f1)
SLOT2=$(echo "$RESULT" | cut -d'|' -f2)
SLOT3=$(echo "$RESULT" | cut -d'|' -f3)
SLOT4=$(echo "$RESULT" | cut -d'|' -f4)

{
    printf 'SLOT1=%q\n' "$SLOT1"
    printf 'SLOT2=%q\n' "$SLOT2"
    printf 'SLOT3=%q\n' "$SLOT3"
    printf 'SLOT4=%q\n' "$SLOT4"
} > "$CONFIG_FILE"

notify-send -t 2500 "Sesión de estudio actualizada" "Usá SUPER+C para abrirla"
