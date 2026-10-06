#!/bin/bash
# SUPER+ALT+Y: toma el link de YouTube copiado (Ctrl+C) y saca las capturas + apuntes del video
# sin reproducirlo (video-a-capturas.sh). Si el link es de una playlist, pregunta si procesar
# solo ese video o la playlist entera (playlist-a-apuntes.sh).
# Todo pasa por la cola (cola-capturas.sh): si ya se está procesando algo, el link espera su
# turno ("En cola (posición N)"); el mismo link dos veces no se duplica. Corre en segundo plano;
# el avance se ve en una notificación con barrita de progreso que se actualiza sola.
# Uso desde la terminal: youtube-capturas.sh [link]   (sin link, usa el portapapeles)
SCRIPTS="$HOME/.config/hypr/scripts"

URL=${1:-$(wl-paste --no-newline 2>/dev/null)}
URL=$(tr -d '[:space:]' <<<"$URL")
if ! [[ "$URL" =~ ^https?://(www\.|m\.|music\.)?(youtube\.com|youtu\.be)/ ]]; then
    notify-send -t 5000 "Capturas de YouTube" "Primero copiá el link del video (Ctrl+C).\nLo copiado no es un link de YouTube."
    exit 1
fi

LISTA=$(sed -nE 's/.*[?&]list=([A-Za-z0-9_-]+).*/\1/p' <<<"$URL")
VIDEO=$(sed -nE 's#.*([?&]v=|youtu\.be/|/shorts/|/live/|/embed/)([A-Za-z0-9_-]{11}).*#\2#p' <<<"$URL")
# Mixes automáticos (RD…, infinitos) y listas personales (WL = ver más tarde, LL = me gusta,
# necesitan cuenta): no son cursos, se toma solo el video.
[[ "$LISTA" =~ ^(RD|WL$|LL$) ]] && [ -n "$VIDEO" ] && LISTA=""

if [ -n "$LISTA" ]; then
    notify-send -t 3000 "📚 Capturas de YouTube" "Leyendo la playlist…"
    # Cantidad de videos y horas totales, sin bajar nada (~2-5 s)
    INFO=$(yt-dlp --flat-playlist --extractor-args "youtube:lang=es" \
        --print "%(duration)s" --print "playlist:TITULO	%(title)s	%(playlist_count)s" \
        "https://www.youtube.com/playlist?list=$LISTA" 2>/dev/null)
    TITULO_LISTA=$(grep '^TITULO	' <<<"$INFO" | cut -f2)
    N=$(grep '^TITULO	' <<<"$INFO" | cut -f3)
    HORAS=$(grep -E '^[0-9.]+$' <<<"$INFO" | awk '{ s += $1 } END { printf "%.1f", s / 3600 }' | tr . ,)
    if [ -z "$N" ]; then
        if [ -z "$VIDEO" ]; then
            notify-send -u critical -t 8000 "Capturas de YouTube" "No se pudo leer la playlist (¿privada?)."
            exit 1
        fi
        notify-send -t 6000 "Capturas de YouTube" "No se pudo leer la playlist: proceso solo este video."
        LISTA=""
    elif [ -n "$VIDEO" ]; then
        ELECCION=$(zenity --question --no-markup --title="Capturas de YouTube" \
            --text="Este video es parte de una playlist:

$TITULO_LISTA
$N videos · $HORAS h de video

¿Proceso solo este video o la playlist entera?
(La playlist se puede cortar y retomar: volvé a apretar SUPER+ALT+Y con el mismo link.)" \
            --ok-label="Solo este video" --extra-button="Playlist entera ($N videos, $HORAS h)" \
            --cancel-label="Cancelar")
        CODIGO=$?
        if [ $CODIGO -eq 0 ]; then LISTA=""                 # solo este video
        elif [ -z "$ELECCION" ]; then exit 0; fi           # Cancelar / cerrar la ventana
        # (con el botón extra zenity devuelve 1 e imprime su texto: playlist entera)
    fi
fi

if [ -n "$LISTA" ]; then
    bash "$SCRIPTS/cola-capturas.sh" encolar playlist "https://www.youtube.com/playlist?list=$LISTA" \
        "📚 ${TITULO_LISTA:-Playlist} ($N videos)"
else
    bash "$SCRIPTS/cola-capturas.sh" encolar video "$URL" "🎬 $URL"
fi
# El resultado lo avisa la barrita ("✅ Listo" con la carpeta) o una notificación si falla
