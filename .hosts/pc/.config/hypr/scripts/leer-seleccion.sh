#!/bin/bash
# SUPER+R: lee en voz alta el texto seleccionado (con el mouse) en cualquier app.
# Si ya está leyendo, apretar de nuevo interrumpe.
# Voz/velocidad se eligen con SUPER+ALT+R (ver actualizar-voz.sh) y quedan en voz.conf.
# Si el motor elegido es "edge" (online) y falla (sin internet), cae automáticamente a Piper (offline).

export PATH="$HOME/.local/bin:$PATH"

CONFIG="$HOME/.config/hypr/scripts/voz.conf"
PIPER_FALLBACK="/usr/share/piper-voices/es/es_AR/daniela/high/es_AR-daniela-high.onnx"
CHATTERBOX_SCRIPT="$HOME/.config/hypr/scripts/chatterbox-hablar.py"
CHATTERBOX_VENV="$HOME/.local/share/piper-voz/chatterbox-venv"
PIPER_DAEMON="$HOME/.config/hypr/scripts/piper-daemon.py"
PIPER_CLIENT="$HOME/.config/hypr/scripts/piper-client.py"
PIPER_DAEMON_SOCK="${PIPER_DAEMON_SOCK:-$HOME/.cache/piper-voz.sock}"
LIMPIAR_TEXTO="$HOME/.config/hypr/scripts/limpiar-texto.py"
TEXT_FILE=""
STOP_ONLY=0

case "${1:-}" in
    --texto-archivo)
        if [ -z "${2:-}" ]; then
            notify-send -t 2000 "Lectura en voz alta" "Falta el archivo de texto para leer"
            exit 2
        fi
        TEXT_FILE="$2"
        ;;
    --stop)
        STOP_ONLY=1
        ;;
esac

ENGINE="piper"
VOICE="$PIPER_FALLBACK"
SPEED_MULT="1.0"
# shellcheck disable=SC1090
[ -f "$CONFIG" ] && source "$CONFIG"
[ -z "$SPEED_MULT" ] && SPEED_MULT="1.0"

# SPEED_MULT es un multiplicador de velocidad (1.0x = normal, 3.0x = el tope de la barra).
# Se deriva a la tasa de edge-tts y al length-scale de Piper (inverso: más rápido = más chico).
RATE=$(awk -v m="$SPEED_MULT" 'BEGIN{printf "%+d%%", (m-1)*100}')
LENGTH_SCALE=$(awk -v m="$SPEED_MULT" 'BEGIN{printf "%.3f", 1/m}')
PITCH="+0Hz"
VOLUME="+0%"

# Toggle: si ya hay algo sonando/generándose, lo corta y listo.
if pgrep -x piper-tts >/dev/null || pgrep -x edge-tts >/dev/null || pgrep -x ffplay >/dev/null \
    || pgrep -x pw-play >/dev/null || pgrep -f "$CHATTERBOX_SCRIPT" >/dev/null; then
    pkill -x piper-tts 2>/dev/null
    pkill -x edge-tts 2>/dev/null
    pkill -x ffplay 2>/dev/null
    pkill -x pw-play 2>/dev/null
    pkill -f "$CHATTERBOX_SCRIPT" 2>/dev/null
    if [ -z "$TEXT_FILE" ] || [ "$STOP_ONLY" -eq 1 ]; then
        exit 0
    fi
fi
[ "$STOP_ONLY" -eq 1 ] && exit 0

if [ -n "$TEXT_FILE" ]; then
    if [ ! -r "$TEXT_FILE" ]; then
        notify-send -t 2000 "Lectura en voz alta" "No se puede leer el archivo de texto"
        exit 2
    fi
    TEXT=$(cat -- "$TEXT_FILE" 2>/dev/null)
else
    WIN_CLASS=$(hyprctl activewindow -j 2>/dev/null | jq -r '[.class // empty, .initialClass // empty, .title // empty] | join(" ")')
    SUMMARY_TEXT_FILE="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}/resumidor-seleccion.txt"
    SUMMARY_PID_FILE="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}/resumidor-seleccion.pid"
    SUMMARY_PID=$(cat -- "$SUMMARY_PID_FILE" 2>/dev/null)
    SUMMARY_LAYER_ACTIVE=0
    if [[ "$SUMMARY_PID" =~ ^[0-9]+$ ]] \
        && hyprctl layers 2>/dev/null | grep -Fq "namespace: resumen-seleccion, pid: $SUMMARY_PID"; then
        SUMMARY_LAYER_ACTIVE=1
    fi
    case "$WIN_CLASS" in
        *org.yafer.ResumenSeleccion*|*"Resumen de selección"*)
            if [ -s "$SUMMARY_TEXT_FILE" ]; then
                TEXT=$(cat -- "$SUMMARY_TEXT_FILE" 2>/dev/null)
            else
                TEXT=$(wl-paste --primary --no-newline 2>/dev/null)
            fi
            ;;
        *)
            TEXT=$(wl-paste --primary --no-newline 2>/dev/null)
            ;;
    esac
    if [ "$SUMMARY_LAYER_ACTIVE" -eq 1 ] && [ -s "$SUMMARY_TEXT_FILE" ]; then
        TEXT=$(cat -- "$SUMMARY_TEXT_FILE" 2>/dev/null)
    fi
fi
if [ -z "$TEXT_FILE" ] && [ -z "$(echo "$TEXT" | tr -d '[:space:]')" ]; then
    # Apps Chromium/Electron (Brave, VSCode) no exponen la selección de mouse como
    # primary selection en Wayland (limitación conocida de Chromium, no del script).
    # Para que siga siendo UN solo atajo, se simula Ctrl+C (wtype) y se lee el
    # portapapeles normal. Se excluyen terminales: ahí Ctrl+C no copia, manda
    # SIGINT y podría cortar un proceso corriendo (por ejemplo, Claude Code).
    case "$WIN_CLASS" in
        kitty|Alacritty|alacritty|foot|footclient|wezterm|org.wezfurlong.wezterm|kate|konsole|org.kde.konsole|gnome-terminal|gnome-terminal-server|terminator|tilix|contour|xterm|urxvt|st|wterm)
            TEXT=$(wl-paste --no-newline 2>/dev/null)
            ;;
        *)
            # Guarda lo que ya había en el portapapeles para restaurarlo después
            # (en background, no bloquea la lectura) y así no "ensuciarlo" en cada uso.
            CLIP_BACKUP=$(mktemp)
            wl-paste --no-newline > "$CLIP_BACKUP" 2>/dev/null

            wl-copy --clear 2>/dev/null
            # wtype (protocolo virtual-keyboard) no llega a los webviews de VSCode
            # (ej. Markdown Preview): el Ctrl+C sintético no dispara el copy ahí.
            # ydotool inyecta el evento a nivel de kernel (/dev/uinput), como un
            # teclado real, y ahí sí funciona. Si ydotool no está, cae a wtype.
            if command -v ydotool >/dev/null 2>&1; then
                YDOTOOL_SOCKET="${YDOTOOL_SOCKET:-/run/user/$(id -u)/.ydotool_socket}" \
                    ydotool key 29:1 46:1 46:0 29:0 2>/dev/null \
                    || wtype -M ctrl -k c -m ctrl 2>/dev/null
            else
                wtype -M ctrl -k c -m ctrl 2>/dev/null
            fi
            # Polling en vez de sleep fijo: arranca apenas el portapapeles tiene
            # contenido en lugar de esperar siempre el máximo (tope 300ms).
            for _ in $(seq 1 15); do
                TEXT=$(wl-paste --no-newline 2>/dev/null)
                [ -n "$(echo "$TEXT" | tr -d '[:space:]')" ] && break
                sleep 0.02
            done

            if [ -s "$CLIP_BACKUP" ]; then
                (wl-copy < "$CLIP_BACKUP"; rm -f "$CLIP_BACKUP") &
                disown
            else
                rm -f "$CLIP_BACKUP"
            fi
            ;;
    esac
fi
if [ -z "$(echo "$TEXT" | tr -d '[:space:]')" ]; then
    notify-send -t 2000 "Lectura en voz alta" "No hay texto seleccionado"
    exit 0
fi

# Limpieza: saca ruido de markdown/código sin verbalizarlo, deja intacta la puntuación normal
# (. , ; ¿ ? ¡ !) que es la que le da el ritmo natural a la voz. El % sí se dicta ("por ciento").
# Primer paso (limpiar-texto.py, en Python porque sed no maneja bien Unicode/URLs): saca los
# emojis (no aportan nada al escucharlos) y cambia URLs completas y rutas de archivo por "este
# enlace" / "esta ruta" en vez de deletrear cada segmento — más info en el propio script.
# Operadores de comparación (!=, ==, <=, >=, =>) se pasan a palabras ANTES de sacar < > , porque
# si no, "<=" perdía el "<" y quedaba como "=" solo: cambiaba el significado (saldo<=0 -> "saldo=0").
# La barra (/), las rayas (— –), los "delimitadores de inciso" ( ) [ ] { } ` ' y las tiras de
# guiones de tablas/separadores Markdown (---, ------, :---:) se cambian por una coma o un
# espacio: no se pronuncian, solo dejan una pausa breve antes/después de lo que encierran, así
# no se lee "barra diagonal barra diagonal" ni "guion guion guion guion" cortando la comprensión,
# y una aclaración entre paréntesis/corchetes/backticks/comillas no se lee pegada al resto.
# Los ":" quedan + se les agrega una coma detrás para reforzar la pausa (Piper, el motor offline,
# pausa poco en ":" solo). "&&"/"&" se pasan a "y" (una sola vez) para no duplicarlo como "y y".
# Nota: la comilla simple ' también dispara pausa aunque sea un apóstrofo de contracción en
# inglés (don't, it's) — decisión consciente del usuario, prioriza la pausa en incisos/código
# sobre leer bien esas contracciones (caso raro en los textos que lee habitualmente).
# El salto de línea también debe sonar como una pausa (si no, dos líneas/párrafos seguidos se
# leen pegados como si fueran una sola oración). sed no ve saltos de línea (procesa línea por
# línea, nunca los mete en el pattern space), así que el join lo hace awk: junta todas las
# líneas con " , " en el medio. Una línea en blanco entre párrafos deja DOS "," seguidas (línea
# vacía = un salto que se une solo, más el que la separa del párrafo siguiente) — pausa un poco
# más larga, lo cual está bueno para separar párrafos. Va al final, justo antes del squeeze de
# espacios, para no interferir con las reglas de arriba (todas ya operan línea por línea).
CLEAN=$(printf '%s' "$TEXT" \
    | python3 "$LIMPIAR_TEXTO" \
    | sed -E 's/!==|!=/ no es igual a /g' \
    | sed -E 's/===|==/ es igual a /g' \
    | sed -E 's/=>/ entonces /g' \
    | sed -E 's/<=/ menor o igual a /g' \
    | sed -E 's/>=/ mayor o igual a /g' \
    | sed -E 's/&+/ y /g' \
    | sed -E 's/%/ por ciento /g' \
    | sed -E 's/[—–]/ , /g' \
    | sed -E 's/[][(){}'"'"'`]/ , /g' \
    | sed -E 's/:?-{3,}:?/ /g' \
    | sed -E 's/:/: ,/g' \
    | sed -E 's#/+# , #g' \
    | sed -E 's/[_*#~^|<>\\]+/ /g' \
    | awk 'BEGIN{ORS=""} {print (NR>1 ? " , " : "") $0}' \
    | tr -s ' \t\n' ' ')

if [ -z "$(echo "$CLEAN" | tr -d '[:space:]')" ]; then
    notify-send -t 2000 "Lectura en voz alta" "No hay texto seleccionado"
    exit 0
fi

TMPMP3=$(mktemp --suffix=.mp3)
TMPWAV=$(mktemp --suffix=.wav)
trap 'rm -f "$TMPMP3" "$TMPWAV"' EXIT

if [ "$ENGINE" = "edge" ]; then
    if timeout 12 edge-tts --voice "$VOICE" --rate "$RATE" --pitch "$PITCH" --volume "$VOLUME" \
        --text "$CLEAN" --write-media "$TMPMP3" 2>/dev/null && [ -s "$TMPMP3" ]; then
        ffplay -nodisp -autoexit -loglevel quiet "$TMPMP3" 2>/dev/null
        exit 0
    fi
    notify-send -t 2500 "Sin internet" "edge-tts no respondió, uso Piper (offline) como respaldo"
    ENGINE="piper"
    VOICE="$PIPER_FALLBACK"
fi

if [ "$ENGINE" = "chatterbox" ]; then
    if [ -x "$CHATTERBOX_VENV/bin/python" ] && [ -f "$CHATTERBOX_SCRIPT" ]; then
        notify-send -t 2500 "Generando audio (Chatterbox)" "Calidad máxima, offline — puede tardar unos segundos"
        "$CHATTERBOX_VENV/bin/python" "$CHATTERBOX_SCRIPT" "$CLEAN" "$TMPWAV" 2>/dev/null
        if [ -s "$TMPWAV" ]; then
            paplay "$TMPWAV" 2>/dev/null
            exit 0
        fi
        notify-send -t 2500 "Chatterbox falló" "Uso Piper (offline) como respaldo"
    else
        notify-send -t 2500 "Chatterbox no instalado" "Uso Piper (offline) como respaldo"
    fi
    ENGINE="piper"
    VOICE="$PIPER_FALLBACK"
fi

# Camino rápido: pedirle el audio al daemon (modelo ya cargado en memoria,
# ver piper-daemon.py). Si no está corriendo, cae a invocar piper-tts directo
# (más lento, recarga el modelo) y de paso levanta el daemon para la próxima vez.
if [ -S "$PIPER_DAEMON_SOCK" ]; then
    echo "$CLEAN" | python3 "$PIPER_CLIENT" "$VOICE" "$LENGTH_SCALE" 2>/dev/null \
        | pw-play --rate=22050 --format=s16 --channels=1 --raw - 2>/dev/null
    DAEMON_OK=${PIPESTATUS[1]}
else
    DAEMON_OK=1
fi

if [ "$DAEMON_OK" -ne 0 ]; then
    (systemctl --user start piper-voz-daemon.service 2>/dev/null &) 2>/dev/null
    echo "$CLEAN" | piper-tts --model "$VOICE" --length-scale "$LENGTH_SCALE" --output-raw 2>/dev/null \
        | pw-play --rate=22050 --format=s16 --channels=1 --raw - 2>/dev/null
fi
