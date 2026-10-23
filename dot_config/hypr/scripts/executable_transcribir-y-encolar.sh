#!/bin/bash
# Transcribe con Whisper local (GPU, Vulkan) los videos sin subtítulos de una carpeta y, carpeta por
# carpeta, encola los apuntes (motor OpenCode). Así la GPU transcribe la sección N+1 mientras la cola
# hace los apuntes de la N. Se puede cortar y relanzar: lo ya transcrito/hecho se saltea.
# Uso: transcribir-y-encolar.sh <carpeta raíz>     (cada subcarpeta con videos = un curso/sección)
# Los .es.srt quedan junto al video (cuadernillo.py los busca ahí).
SCRIPTS="$HOME/.config/hypr/scripts"
RAIZ=$(realpath "${1:?Uso: $0 <carpeta raíz>}")
MODELO="$HOME/.local/share/doblar/whisper/ggml-large-v3-turbo-q8_0.bin"
VAD="$HOME/.local/share/doblar/whisper/ggml-silero-v5.1.2.bin"
TMP=$(mktemp -d "${XDG_RUNTIME_DIR:-/tmp}/whisper.XXXXXX"); trap 'rm -rf "$TMP"' EXIT
export APUNTES_MOTOR=opencode   # modelos: la cadena por defecto de cuadernillo.py (APUNTES_MODELO_OPENCODE="a,b,c" para cambiarla)

exec 9>"${XDG_RUNTIME_DIR:-/tmp}/transcribir.lock"
flock -n 9 || { echo "Ya hay una transcripción en marcha"; exit 1; }

# carpetas que tienen videos directamente, en orden natural
mapfile -t CARPETAS < <(find "$RAIZ" -type d ! -name capturas ! -path '*/capturas/*' -print0 |
    while IFS= read -r -d '' d; do
        find "$d" -maxdepth 1 -type f \( -iname '*.mp4' -o -iname '*.mkv' -o -iname '*.ts' \) -print -quit | grep -q . && echo "$d"
    done | sort -V)

# COLAS_PARALELAS=N: reparte las carpetas entre N colas (…/cola-1..N), cada una con su trabajador, para
# usar los núcleos libres (las capturas son de 1 hilo y la IA espera). 0 = la cola principal.
COLAS=${COLAS_PARALELAS:-0}; IDX=0
for D in "${CARPETAS[@]}"; do
    echo "===== $(date +%H:%M) $D ====="
    while IFS= read -r -d '' V; do
        BASE="${V%.*}"; CLASE=$(basename "$BASE")
        [ -f "$BASE.es.srt" ] && continue
        [ -f "$D/capturas/$CLASE/apuntes.md" ] && continue
        ffmpeg -nostdin -v error -y -i "$V" -vn -ac 1 -ar 16000 "$TMP/a.wav" || { echo "sin audio: $V"; continue; }
        if nice -n 10 whisper-cli -m "$MODELO" -f "$TMP/a.wav" -l es -osrt -of "$TMP/a" -np -t 4 --vad -vm "$VAD" >/dev/null 2>&1 </dev/null \
            && [ -s "$TMP/a.srt" ]; then
            mv "$TMP/a.srt" "$BASE.es.srt.tmp" && mv "$BASE.es.srt.tmp" "$BASE.es.srt"
            echo "  ✓ $CLASE"
        else
            echo "  ✗ falló: $CLASE"
        fi
    done < <(find "$D" -maxdepth 1 -type f \( -iname '*.mp4' -o -iname '*.mkv' -o -iname '*.ts' \) ! -name '*.es.mp4' -print0 | sort -zV)
    COLA_DIR="$HOME/.cache/auto-captura"; [ "$COLAS" -gt 0 ] && COLA_DIR="$COLA_DIR/cola-$((IDX % COLAS + 1))"; IDX=$((IDX + 1))
    # 9>&-: el trabajador de la cola es un proceso largo y no debe heredar el candado de la transcripción
    DIR_COLA="$COLA_DIR" bash "$SCRIPTS/cola-capturas.sh" encolar curso "$D" "📚 $(basename "$(dirname "$D")")/$(basename "$D")" >/dev/null 9>&-
done
echo "===== terminado $(date +%H:%M) ====="
notify-send "Transcripción terminada" "$(basename "$RAIZ"): todo transcrito y encolado"
