#!/usr/bin/env bash
# Enfocar-o-abrir apps web como "ventanas de app" de Brave (sin pestañas, clase propia).
# Uso: app-web.sh <youtube|whatsapp|telegram|facebook|instagram|tiktok|drive|code>
#  - Apps con escritorio fijo: si ya está abierta, salta a su escritorio virtual
#    (ambos monitores) y la enfoca; si no, va a ese escritorio y la abre ahí
#    (las reglas de windowrules.lua la ubican en el workspace correcto).
#  - (09/10/2026) Solo las redes (facebook, instagram, tiktok, whatsapp, telegram) tienen escritorio fijo.
#  - YouTube, Drive y VS Code son libres: enfoca la ventana de YouTube del escritorio virtual actual
#    o abre una nueva ahí.
# Escritorio virtual i = workspace i (cara principal, interna) + (i + NUM_WPM) (cara secundaria / Arzopa).

NUM_WPM=5

# (24/10/2026) Chats según pantallas: 1 pantalla -> ws 1 (junto a redes); 2 pantallas -> ws 6 (cara secundaria).
n_mon=$(hyprctl monitors -j 2>/dev/null | jq 'length' 2>/dev/null)
ws_chats=1; [[ "${n_mon:-1}" -ge 2 ]] && ws_chats=6

case "$1" in
    youtube)   url="https://www.youtube.com/";       clase="^brave-www\.youtube\.com__";   ws="" ;;
    whatsapp)  url="https://web.whatsapp.com/";      clase="^brave-web\.whatsapp\.com__";  ws=$ws_chats ;;
    telegram)  url="https://web.telegram.org/";      clase="^brave-web\.telegram\.org__";  ws=$ws_chats ;;
    facebook)  url="https://www.facebook.com/";      clase="^brave-www\.facebook\.com__";  ws=1 ;;
    instagram) url="https://www.instagram.com/";     clase="^brave-www\.instagram\.com__"; ws=1 ;;
    tiktok)    url="https://www.tiktok.com/";        clase="^brave-www\.tiktok\.com__";    ws=1 ;;
    drive)     url="https://drive.google.com/";      clase="^brave-drive\.google\.com__";  ws="" ;;
    code)      url="";                               clase="^(code|Code|code-oss)$";       ws="" ;;
    *) echo "uso: $0 <youtube|whatsapp|telegram|facebook|instagram|tiktok|drive|code>" >&2; exit 1 ;;
esac

despachar() { hyprctl dispatch "$1" >/dev/null; }

# Muestra el escritorio virtual que contiene el workspace $1 y enfoca ese workspace.
# LAPTOP: usa la lógica de config/escritorios.lua (VD.mostrarWorkspace) vía `hyprctl eval`:
#  - solo la interna: salta directo a la cara correcta (p. ej. ws 6 = chats);
#  - con la Arzopa: cambia las dos pantallas al escritorio i y enfoca la del ws.
# Si eval fallara (config sin VD), cae al comportamiento de la PC.
ir_a_workspace() {
    local w=$1
    if ! hyprctl eval "VD.mostrarWorkspace($w)" 2>/dev/null | grep -qx ok; then
        local i; i=$(indice_de "$w")
        despachar "hl.dsp.focus({ workspace = \"$((i + NUM_WPM))\" })"
        despachar "hl.dsp.focus({ workspace = \"$i\" })"
    fi
}

indice_de() { local w=$1; (( w > NUM_WPM )) && echo $((w - NUM_WPM)) || echo "$w"; }

abrir() {
    if [[ -n $url ]]; then
        setsid brave --app="$url" >/dev/null 2>&1 < /dev/null &
    else
        setsid code >/dev/null 2>&1 < /dev/null &
    fi
}

clientes=$(hyprctl clients -j)

if [[ -n $ws ]]; then
    ventana=$(jq -r --arg c "$clase" 'map(select(.class | test($c))) | first | "\(.address) \(.workspace.id)" // empty' <<<"$clientes")
    if [[ -n $ventana && $ventana != "null null" ]]; then
        read -r dir wid <<<"$ventana"
        (( wid > 0 )) && ir_a_workspace "$wid"
        despachar "hl.dsp.focus({ window = \"address:$dir\" })"
    else
        ir_a_workspace "$ws"
        abrir
    fi
else
    actual=$(hyprctl activeworkspace -j | jq -r '.id')
    i=$(indice_de "$actual")
    dir=$(jq -r --arg c "$clase" --argjson a "$i" --argjson b "$((i + NUM_WPM))" \
        'map(select((.class | test($c)) and (.workspace.id == $a or .workspace.id == $b))) | first | .address // empty' <<<"$clientes")
    if [[ -n $dir ]]; then
        despachar "hl.dsp.focus({ window = \"address:$dir\" })"
    else
        abrir
    fi
fi
