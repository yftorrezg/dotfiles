#!/usr/bin/env bash
# Muestra / oculta el panel de notas al lado de mpv (Hyprland): mpv ~80 %, panel ~20 % a la derecha.
# Lo llama notas.lua con la tecla h (o con H y el argumento «lista», que abre en la vista de lista). Si el panel ya está abierto, lo cierra.
DIR="$(dirname "$(readlink -f "$0")")"
URL="${NOTAS_URL:-http://127.0.0.1:47831/}"
PORCENTAJE=20
CLASE='^brave-127\.0\.0\.1__'

despachar() { hyprctl dispatch "$1" >/dev/null; }
panel_addr() { hyprctl clients -j | jq -r --arg c "$CLASE" 'map(select(.class|test($c)))|first|.address // empty'; }

addr=$(panel_addr)
if [[ -n $addr ]]; then
    despachar "hl.dsp.window.close({ window = \"address:$addr\" })"
    exit 0
fi

# ventana de mpv que tiene el foco (la que pulsó h)
mpv_addr=$(hyprctl activewindow -j | jq -r 'select(.class=="mpv") | .address // empty')

# servidor del panel (se queda en segundo plano; se apaga solo tras 20 min sin uso)
if ! curl -fs --max-time 1 "${URL}api/videos" >/dev/null; then
    setsid -f python3 "$DIR/servidor.py" serve >/dev/null 2>&1 </dev/null
    for _ in $(seq 30); do curl -fs --max-time 1 "${URL}api/videos" >/dev/null && break; sleep 0.1; done
fi

VISTA=""; [[ ${1:-} == lista ]] && VISTA="#lista"
setsid -f brave --app="$URL$VISTA" >/dev/null 2>&1 </dev/null
for _ in $(seq 80); do addr=$(panel_addr); [[ -n $addr ]] && break; sleep 0.1; done
[[ -z $addr ]] && exit 1

# reparto 80/20: el panel a la derecha con PORCENTAJE % del ancho que ocupan ambos
if [[ -n $mpv_addr ]]; then
    sleep 0.2
    pos() { hyprctl clients -j | jq -r --arg a "$1" '.[]|select(.address==$a)|"\(.at[0]) \(.size[0]) \(.size[1])"'; }
    read -r px pw ph <<<"$(pos "$addr")"
    read -r mx mw _ <<<"$(pos "$mpv_addr")"
    if (( px < mx )); then   # salió a la izquierda: intercambiar lugares
        despachar "hl.dsp.focus({ window = \"address:$addr\" })"
        despachar 'hl.dsp.window.swap({ direction = "r" })'
        sleep 0.15
        read -r px pw ph <<<"$(pos "$addr")"
        read -r mx mw _ <<<"$(pos "$mpv_addr")"
    fi
    total=$(( pw + mw ))
    ancho_mpv=$(( total - total * PORCENTAJE / 100 ))
    # se redimensiona mpv (el de la izquierda): con el panel a la derecha, Hyprland aplica el tamaño exacto al primer nodo
    despachar "hl.dsp.window.resize({ x = $ancho_mpv, y = $ph, exact = true, window = \"address:$mpv_addr\" })"
    despachar "hl.dsp.focus({ window = \"address:$mpv_addr\" })"
fi
