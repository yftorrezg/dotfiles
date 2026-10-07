#!/bin/bash
# SUPER+D: menú para descargar el link copiado (Ctrl+C). Se abre en una ventanita flotante
# (kitty, clase "descargar-menu") y se elige con UNA tecla. La descarga sigue sola en segundo
# plano con barrita de progreso (descargar --aviso); aquí no hay que esperar nada.
if [ "$1" != "--dentro" ]; then
    exec kitty --class descargar-menu --title "Descargar" -o confirm_os_window_close=0 bash "$0" --dentro
fi

C=$'\e[1;36m'; D=$'\e[2m'; R=$'\e[0m'; V=$'\e[1;32m'
URL=$(wl-paste --no-newline 2>/dev/null | tr -d '[:space:]')
clear
printf '\n  %s📥 Descargar%s\n\n' "$C" "$R"
if ! [[ "$URL" =~ ^https?:// ]]; then
    printf '  Lo copiado no es un link.\n  Pegalo aquí (Ctrl+Shift+V) y Enter, o Esc para salir:\n\n  '
    read -r -e URL || exit 0
    URL=$(tr -d '[:space:]' <<<"$URL")
    [[ "$URL" =~ ^https?:// ]] || exit 0
    clear; printf '\n  %s📥 Descargar%s\n\n' "$C" "$R"
fi
printf '  %s%s%s\n\n' "$D" "${URL:0:70}" "$R"

# ¿es un video dentro de una lista (o una lista entera)?
EN_LISTA=0
if [[ "$URL" =~ [?\&]list= ]] && ! [[ "$URL" =~ [?\&]list=(RD|WL|LL) ]]; then EN_LISTA=1; fi

printf '   %s1%s  🎬 Video          %smejor calidad%s\n' "$V" "$R" "$D" "$R"
printf '   %s2%s  🎬 Video 720p     %smás liviano%s\n' "$V" "$R" "$D" "$R"
printf '   %s3%s  🎵 MP3            %sa ~/Música/<artista>%s\n' "$V" "$R" "$D" "$R"
if [ "$EN_LISTA" = 1 ]; then
    printf '   %s4%s  📚 Lista entera en video\n' "$V" "$R"
    printf '   %s5%s  📚 Lista entera en MP3\n' "$V" "$R"
fi
printf '\n  %sEnter = 1 · Esc = cancelar%s ' "$D" "$R"
read -r -s -n1 K || exit 0
case "$K" in
    ""|1) OPC=() ;;
    2) OPC=(--720) ;;
    3) OPC=(--mp3) ;;
    4) [ "$EN_LISTA" = 1 ] && OPC=(--lista) || exit 0 ;;
    5) [ "$EN_LISTA" = 1 ] && OPC=(--lista --mp3) || exit 0 ;;
    *) exit 0 ;;
esac
# Primero se lanza la descarga (desprendida de esta ventana, que se cierra al terminar el menú)
# y se anota en el log del menú; luego se confirma en pantalla un instante.
mkdir -p "$HOME/.cache/descargar"
echo "$(date +%T) opción=${K:-Enter} ${OPC[*]} $URL" >>"$HOME/.cache/descargar/menu.log"
setsid -f "$HOME/.local/bin/descargar" --aviso "${OPC[@]}" "$URL" >/dev/null 2>&1 </dev/null
notify-send -t 2500 -- "📥 Descargando…" "Aparece una barrita de progreso en unos segundos." &
printf '\n\n  %s✅ Descargando…%s\n' "$V" "$R"
sleep 0.8
