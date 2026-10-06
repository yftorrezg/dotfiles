#!/bin/bash
# Saca las capturas de un video sin reproducirlo (YouTube u otro sitio de yt-dlp, o archivo local)
# y arma el cuadernillo de apuntes (apuntes.md) con cuadernillo.py y el repaso corto
# (resumen.md) con resumen-corto.py.
# Uso: video-a-capturas.sh <url|archivo>
# Archivo local -> <carpeta del video>/capturas/<nombre>/ ; URL -> ~/Vídeos/Capturas de YouTube/<título>/
# Mismo criterio que la auto-captura; capturas 0001.webp, 0002.webp… y el minuto del video de
# cada una en .minutos.tsv.
# Si las capturas ya están (.cantidad) no se rehacen; si el cuadernillo ya está, tampoco.
# Muestra una barrita de progreso en una notificación (progreso.py). Si la llama
# curso-a-apuntes.sh, la barrita es la del curso (PROGRESO_ARCHIVO ya viene puesto).
# Variables: SIN_APUNTES=1 (solo capturas) · SIN_IA=1 (apuntes sin resumen de Claude)
#   DESTINO=<carpeta>: guardar ahí en vez de la carpeta de siempre (lo usa playlist-a-apuntes.sh)
#   TITULO=<título>: no pedírselo a YouTube (un pedido menos; playlist-a-apuntes.sh ya lo tiene)
set -e
SCRIPTS="$HOME/.config/hypr/scripts"
[ -z "$1" ] && { echo "Uso: $0 <url|archivo>"; exit 1; }

etapa() {  # etapa <inicio> <fin>: la próxima parte ocupa ese tramo de la barrita
    export PROGRESO_RANGO="$1 $2"
}
poner() { python3 "$SCRIPTS/progreso.py" poner "$@" 2>/dev/null || true; }

PROPIA=0
if [ -z "$PROGRESO_ARCHIVO" ]; then  # barrita propia (no viene de un curso)
    PROPIA=1
    export PROGRESO_ARCHIVO="${XDG_RUNTIME_DIR:-/tmp}/auto-captura-progreso.$$"
    poner 0 descarga "preparando"
fi
terminar() {  # al salir: avisar "listo" o "falló" en la misma notificación
    local codigo=$?
    if [ "$PROPIA" = 1 ]; then
        export PROGRESO_RANGO="0 100"
        if [ $codigo -eq 0 ]; then poner 100 fin "${MENSAJE_FIN:-Capturas y apuntes listos}"
        else poner 100 error "Revisá el log en ~/.cache/auto-captura/"; fi
    fi
}
trap terminar EXIT

if [[ "$1" =~ ^https?:// ]]; then
    # Link: capturas en ~/Vídeos/Capturas de YouTube/<título>/ (+ subtítulos para repasar)
    BASE="$(xdg-user-dir VIDEOS 2>/dev/null || echo "$HOME/Vídeos")/Capturas de YouTube"
    NOMBRE=${TITULO:-$(yt-dlp --no-playlist --print "%(title).80B" "$1" || true)}  # (set -e)
    NOMBRE=$(sed 's@[]/\\:*?"<>|#[^]@-@g; s/^[ .-]*//; s/[ .]*$//' <<<"$NOMBRE")
    [ -z "$NOMBRE" ] && { echo "No se pudo leer el título del video"; exit 1; }
    [ "$PROPIA" = 1 ] && setsid python3 "$SCRIPTS/progreso.py" seguir "$PROGRESO_ARCHIVO" "$NOMBRE" >/dev/null 2>&1 &
    DIR="${DESTINO:-$BASE/$NOMBRE}"
    if [ -z "$DESTINO" ]; then
        # Dos videos distintos con el mismo título no comparten carpeta: se distinguen por el
        # id del video (.youtube-id). Las carpetas viejas sin .youtube-id se toman como propias.
        ID=""
        [[ "$1" =~ (v=|youtu\.be/|shorts/)([A-Za-z0-9_-]{11}) ]] && ID=${BASH_REMATCH[2]}
        if [ -n "$ID" ] && [ -f "$DIR/.youtube-id" ] && [ "$(cat "$DIR/.youtube-id")" != "$ID" ]; then
            DIR="$DIR [$ID]"
        fi
        mkdir -p "$DIR"
        [ -n "$ID" ] && echo "$ID" > "$DIR/.youtube-id"
    fi
    mkdir -p "$DIR"
    etapa 0 25
    if [ ! -f "$DIR/.cantidad" ]; then
        # 1) Solo el video (sin audio), hasta 1080p. El avance va a la barrita.
        #    -S proto,vcodec:h264: el archivo https (DASH) en H.264, no el HLS "m3u8": misma
        #    resolución pero hasta 18 veces más pesado (6 GB vs 335 MB en un video de 4:42 h).
        ULT=-1
        #    --print-to-file: anota el idioma original del video (lo dice YouTube, sin otro pedido)
        yt-dlp --no-playlist -f "bv*[height<=1080]" -S "proto,vcodec:h264" -o "$DIR/video.%(ext)s" \
            --print-to-file "%(language)s" "$DIR/.idioma" --newline --progress-template "download:PROGRESO %(progress._percent_str)s" "$1" |
        while IFS= read -r l; do
            if [[ "$l" == PROGRESO* ]]; then
                p=${l#PROGRESO }; p=${p%\%}; p=${p// /}
                if [[ "$p" =~ ^[0-9.]+$ ]] && [ "${p%.*}" != "$ULT" ]; then  # solo si cambió el % entero
                    ULT=${p%.*}; poner "$p" descarga "video"
                fi
            else
                echo "$l"
            fi
        done
    fi
    # 2) Subtítulos originales en español/inglés (no las traducciones automáticas). Opcionales:
    #    si YouTube los niega (error 429, pasa seguido) las capturas se hacen igual.
    if ! ls "$DIR"/subtitulos.*.srt >/dev/null 2>&1; then
        poner 100 descarga "subtítulos"
        # Solo los del idioma original: en un curso en español el "inglés" es una traducción
        # automática (peor para Claude que el original) y YouTube la niega seguido con 429.
        # En uno en inglés se piden los originales + el español traducido (para leer).
        case "$(cat "$DIR/.idioma" 2>/dev/null)" in
            es*) IDIOMAS="es,es-orig" ;;
            en*) IDIOMAS="en,en-orig,es" ;;
            # idioma desconocido (NA, pasa seguido): los "-orig" solo existen en el idioma
            # original del video, así que no se pide la traducción al inglés de un video en español
            *)   IDIOMAS="es-orig,en-orig,es" ;;
        esac
        # --sleep-subtitles: una pausa entre idioma e idioma, para que YouTube no conteste 429
        yt-dlp --no-playlist --skip-download --sleep-subtitles 2 --write-subs --write-auto-subs \
            --sub-langs "$IDIOMAS" --convert-subs srt -o "$DIR/subtitulos.%(ext)s" "$1" \
            || echo "(no se pudieron bajar los subtítulos; sigo con las capturas)"
    fi
    VIDEO=$(ls "$DIR"/video.* 2>/dev/null | grep -v -E '\.(srt|vtt|part|ytdl)$' | head -1 || true)
    BORRAR=1
    CAPTURAS_DESDE=25
else
    # Video descargado: las capturas quedan al lado, en capturas/<nombre del video>/
    VIDEO=$(realpath "$1")
    NOMBRE=$(basename "${VIDEO%.*}" | sed -E 's/\.(es|en)$//')  # "clase.es.mp4" (doblado) = misma clase
    [ "$PROPIA" = 1 ] && setsid python3 "$SCRIPTS/progreso.py" seguir "$PROGRESO_ARCHIVO" "$NOMBRE" >/dev/null 2>&1 &
    DIR="${DESTINO:-$(dirname "$VIDEO")/capturas/$NOMBRE}"
    BORRAR=0
    CAPTURAS_DESDE=0
fi

if [ ! -f "$DIR/.cantidad" ]; then
    [ -f "$VIDEO" ] || { echo "No se pudo obtener el video"; exit 1; }
    rm -f -- "${DIR:?}"/[0-9]*.png "${DIR:?}"/[0-9]*.webp  # restos de una corrida cortada a la mitad
    etapa "$CAPTURAS_DESDE" 85
    poner 0 capturas ""
    python3 "$SCRIPTS/auto-captura.py" --video "$VIDEO" --out "$DIR"
    APUNTES_DESDE=85
else
    echo "Capturas ya hechas ($(cat "$DIR/.cantidad")): no se rehacen"
    APUNTES_DESDE=$CAPTURAS_DESDE
fi

if [ "${SIN_APUNTES:-0}" != 1 ]; then
    etapa "$APUNTES_DESDE" 100
    poner 0 apuntes ""
    python3 "$SCRIPTS/cuadernillo.py" "$DIR" ${VIDEO:+--video "$VIDEO"} --titulo "$NOMBRE" \
        $([ "${SIN_IA:-0}" = 1 ] && echo --sin-ia) || echo "(no se pudo armar el cuadernillo)"
    # Segunda versión, más resumida (resumen.md); no toca apuntes.md
    [ "${SIN_IA:-0}" = 1 ] || python3 "$SCRIPTS/resumen-corto.py" "$DIR" || echo "(no se pudo armar el resumen corto)"
    # sin IA a propósito: que rehacer-sin-ia.py no la tome por una clase que falló
    [ "${SIN_IA:-0}" = 1 ] && touch "$DIR/.sin-ia" || true
    # Tarjetas de repaso y panel de cursos (los arma otro script; si no están, no pasa nada).
    # El panel solo acá si la barrita es propia: en un curso/playlist lo regenera el de afuera.
    [ "${SIN_IA:-0}" != 1 ] && [ -f "$SCRIPTS/tarjetas.py" ] && python3 "$SCRIPTS/tarjetas.py" "$DIR" || true
    [ "$PROPIA" = 1 ] && [ -f "$SCRIPTS/panel-cursos.py" ] && python3 "$SCRIPTS/panel-cursos.py" || true
fi
if [ "$BORRAR" = 1 ] && [ -n "$VIDEO" ]; then
    rm -f "$VIDEO"  # el video ya está en YouTube; quedan capturas + subtítulos + apuntes
fi
MENSAJE_FIN="📓 $(cat "$DIR/.cantidad" 2>/dev/null || echo 0) capturas · apuntes en $(basename "$DIR")/apuntes.md"
