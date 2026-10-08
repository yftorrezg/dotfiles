#!/bin/bash
# Procesa una playlist de YouTube entera (un curso): para cada video, en orden, capturas +
# cuadernillo de apuntes, y el INDICE.md del curso. Mismo diseño que curso-a-apuntes.sh:
# se puede cortar y volver a lanzar (con el mismo link) y sigue donde quedó; prioridad baja.
# Uso: playlist-a-apuntes.sh <url de la playlist>   (sirve watch?v=…&list=… o playlist?list=…)
# Salida: ~/Vídeos/Capturas de YouTube/<título de la playlist>/capturas/<NNN - título>/
#   NNN = posición en la playlist (001, 002…: así se ordenan solas). Cada clase guarda el id del
#   video en .youtube-id: aunque YouTube cambie el título o el orden, se reconoce lo ya hecho.
# Variables: MAX_VIDEOS=N (solo los primeros N, para probar) · SIN_IA=1 · SIN_APUNTES=1
#   (para las pruebas: BASE_CAPTURAS=<carpeta> · ESPERA_BLOQUEO=<segundos> en vez de 10 min)
SCRIPTS="$HOME/.config/hypr/scripts"
URL="${1:?Uso: $0 <url de la playlist>}"
LISTA=$(sed -nE 's/.*[?&]list=([A-Za-z0-9_-]+).*/\1/p' <<<"$URL")
[ -z "$LISTA" ] && { echo "El link no tiene list=: no es una playlist"; exit 1; }
URL="https://www.youtube.com/playlist?list=$LISTA"
BASE="${BASE_CAPTURAS:-$(xdg-user-dir VIDEOS 2>/dev/null || echo "$HOME/Vídeos")/Capturas de YouTube}"
limpiar() { sed 's@[]/\\:*?"<>|#[^]@-@g; s/^[ .-]*//; s/[ .]*$//'; }  # igual que video-a-capturas.sh
avisar() { notify-send -a "Auto-captura" "$@" 2>/dev/null || true; }

# Una sola playlist a la vez (la cola de cola-capturas.sh ya lo asegura; esto cubre la terminal)
exec 9>"${XDG_RUNTIME_DIR:-/tmp}/playlist-a-apuntes.lock"
if ! flock -n 9; then
    avisar -t 6000 "Apuntes de la playlist" "Ya hay una playlist procesándose. Esperá a que termine."
    exit 1
fi

# Lista de videos (sin bajar nada). lang=es: YouTube a veces devuelve los títulos traducidos
# al inglés ("React Course…"); así vienen en español si el autor los puso en español.
T=$'\t'
LISTADO=""
for intento in 1 2 3; do
    LISTADO=$(yt-dlp --flat-playlist --extractor-args "youtube:lang=es" \
        --print "%(playlist_index)s$T%(id)s$T%(duration)s$T%(title).80B" \
        --print "playlist:TITULO$T%(title).80B$T%(playlist_count)s" "$URL" 2>/dev/null) && [ -n "$LISTADO" ] && break
    echo "No se pudo leer la playlist (intento $intento); reintento en 30 s"; sleep 30
done
[ -z "$LISTADO" ] && { avisar -u critical "Apuntes de la playlist" "No se pudo leer la playlist:\n$URL"; exit 1; }
NOMBRE_CURSO=$(grep "^TITULO$T" <<<"$LISTADO" | cut -f2 | limpiar)
[ -z "$NOMBRE_CURSO" ] && NOMBRE_CURSO="Playlist $LISTA"
CURSO="$BASE/$NOMBRE_CURSO"
mkdir -p "$CURSO/capturas"
grep -v "^TITULO$T" <<<"$LISTADO" > "$CURSO/.playlist.tsv"   # posición, id, duración, título
echo "$URL" > "$CURSO/.playlist-url"
mapfile -t ENTRADAS < "$CURSO/.playlist.tsv"
[ -n "$MAX_VIDEOS" ] && ENTRADAS=("${ENTRADAS[@]:0:$MAX_VIDEOS}")
TOTAL=${#ENTRADAS[@]}
[ "$TOTAL" -eq 0 ] && { avisar "Apuntes de la playlist" "La playlist está vacía"; exit 1; }

# Carpetas ya existentes por id de video (de una corrida anterior)
declare -A CARPETA_DE
for f in "$CURSO"/capturas/*/.youtube-id; do
    [ -f "$f" ] && CARPETA_DE[$(< "$f")]=$(dirname "$f")
done

# Una sola barrita para toda la playlist ("clase 3/41")
export PROGRESO_ARCHIVO="${XDG_RUNTIME_DIR:-/tmp}/playlist-a-apuntes-progreso.$$"
python3 "$SCRIPTS/progreso.py" poner 0 descarga "empezando"
# 9>&-: que la barrita (vive unos segundos más) no se quede con el lock
setsid python3 "$SCRIPTS/progreso.py" seguir "$PROGRESO_ARCHIVO" "$NOMBRE_CURSO" >/dev/null 2>&1 9>&- &
TERMINADO=0
al_salir() {  # si se corta (error, cancelar), que la barrita no quede colgada
    [ "$TERMINADO" = 1 ] && return
    export PROGRESO_RANGO="0 100" PROGRESO_CLASE=""
    python3 "$SCRIPTS/progreso.py" poner 100 error "Cortado. Volvé a pedir el mismo link: sigue donde quedó." 2>/dev/null
}
trap al_salir EXIT
extras() {  # índice + tarjetas + panel (los dos últimos, si existen: los arma otro script)
    python3 "$SCRIPTS/cuadernillo.py" --indice "$CURSO/capturas" >/dev/null
    [ -f "$SCRIPTS/panel-cursos.py" ] && python3 "$SCRIPTS/panel-cursos.py" >/dev/null 2>&1 || true
}

LISTO=apuntes.md; [ "${SIN_APUNTES:-0}" = 1 ] && LISTO=.cantidad  # qué archivo = "clase hecha"
HECHAS=0; FALLARON=(); SALTEADAS=0; BLOQUEOS=0; CORTE=""
TMP=$(mktemp)
for i in "${!ENTRADAS[@]}"; do
    IFS=$'\t' read -r POS ID DURACION TITULO <<<"${ENTRADAS[$i]}"
    export PROGRESO_CLASE="$((i + 1))/$TOTAL"
    TITULO_ORIGINAL="$TITULO"   # sin limpiar: limpiar() cambia [ ] por "-" y ya no se vería "[Private video]"
    TITULO=$(limpiar <<<"$TITULO")
    DIR="${CARPETA_DE[$ID]:-$CURSO/capturas/$(printf '%03d' "$((10#$POS))") - $TITULO}"
    echo "===== [$((i + 1))/$TOTAL] $(basename "$DIR") ($(date +%H:%M)) ====="
    if [ -f "$DIR/$LISTO" ]; then
        echo "Ya tiene apuntes: se saltea"
        HECHAS=$((HECHAS + 1)); continue
    fi
    # Videos privados/eliminados: en la lista aparecen como "[Private video]" sin duración
    if [ "$DURACION" = NA ] && [[ "$TITULO_ORIGINAL" =~ ^\[.*\]$ ]]; then
        echo "No disponible ($TITULO): se saltea"
        SALTEADAS=$((SALTEADAS + 1)); continue
    fi
    mkdir -p "$DIR" && echo "$ID" > "$DIR/.youtube-id"
    while true; do
        # DESTINO/TITULO: video-a-capturas.sh guarda en esta carpeta y no vuelve a pedir el título
        DESTINO="$DIR" TITULO="$TITULO" nice -n 19 ionice -c 3 \
            bash "$SCRIPTS/video-a-capturas.sh" "https://www.youtube.com/watch?v=$ID" 2>&1 | tee "$TMP"
        if [ "${PIPESTATUS[0]}" -eq 0 ] && [ -f "$DIR/$LISTO" ]; then
            HECHAS=$((HECHAS + 1)); BLOQUEOS=0
            extras
            break
        fi
        # ¿YouTube nos frenó (anti-bot / demasiados pedidos)? Esperar y reintentar el MISMO video;
        # si sigue, cortar todo: seguir sería marcar como fallados todos los que quedan.
        if grep -qiE "not a bot|no eres un bot|HTTP Error 429|Too Many Requests|rate.?limit" "$TMP" \
           && ! [ -f "$DIR/.cantidad" ]; then
            BLOQUEOS=$((BLOQUEOS + 1))
            if [ "$BLOQUEOS" -gt 3 ]; then CORTE="YouTube frenó las descargas"; break 2; fi
            ESPERA=$((BLOQUEOS * ${ESPERA_BLOQUEO:-600}))  # 10, 20, 30 min
            echo "YouTube frenó la descarga (vez $BLOQUEOS): espero $((ESPERA / 60)) min y reintento"
            python3 "$SCRIPTS/progreso.py" poner 0 descarga "YouTube frenó: espero $((ESPERA / 60)) min"
            sleep "$ESPERA"
            continue
        fi
        # Otro error (video no disponible, caído a la mitad…): se anota y se sigue con el próximo
        FALLARON+=("$(printf '%03d' "$((10#$POS))")")
        avisar -u critical -t 8000 "Apuntes: falló una clase" "$(basename "$DIR")"
        break
    done
done
rm -f -- "$TMP"

extras
# Clases que quedaron sin resumen de IA (Claude no respondió): se rehacen ahora, sin bajar nada
[ "${SIN_IA:-0}" = 1 ] || python3 "$SCRIPTS/rehacer-sin-ia.py" "$CURSO/capturas" || true
python3 "$SCRIPTS/cuadernillo.py" --indice "$CURSO/capturas"
python3 "$SCRIPTS/todas-las-capturas.py" "$CURSO/capturas" || true
MSG="$HECHAS de $TOTAL clases con apuntes."
[ "$SALTEADAS" -gt 0 ] && MSG="$MSG $SALTEADAS no disponibles."
[ ${#FALLARON[@]} -gt 0 ] && MSG="$MSG Fallaron: ${FALLARON[*]}"
export PROGRESO_RANGO="0 100" PROGRESO_CLASE=""
TERMINADO=1
if [ -n "$CORTE" ]; then
    MSG="$CORTE. $MSG Volvé a apretar SUPER+ALT+Y con el mismo link más tarde (sigue donde quedó)."
    python3 "$SCRIPTS/progreso.py" poner 100 error "$MSG"
    echo "$MSG"; exit 2
fi
python3 "$SCRIPTS/progreso.py" poner 100 fin "🎓 $MSG Índice: capturas/INDICE.md"
echo "$MSG"
