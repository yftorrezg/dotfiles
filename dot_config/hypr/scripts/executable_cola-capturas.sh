#!/bin/bash
# Cola de trabajos de capturas + apuntes: links de YouTube (SUPER+ALT+Y), playlists y cursos
# descargados (SUPER+ALT+A). Se procesan de a UNO, en orden, así no compiten por la CPU.
# Si aprietan el atajo mientras ya hay algo en marcha, el pedido queda en cola y avisa la posición.
# Uso:
#   cola-capturas.sh encolar <video|playlist|curso> <url o carpeta> [etiqueta]
#   cola-capturas.sh estado          # qué se está procesando y qué espera
#   cola-capturas.sh vaciar          # borra lo que espera (lo que está en marcha sigue)
#   cola-capturas.sh cancelar        # vaciar + cortar lo que está en marcha (se puede reanudar)
#   cola-capturas.sh trabajar        # (interno) el único trabajador; sale cuando la cola queda vacía
# Archivos en ~/.cache/auto-captura/: cola.txt (lo que espera, una línea por pedido),
# actual.txt (lo que se está procesando), cola.lock / trabajador.lock (flock) y logs.
# Línea de la cola: clave<TAB>tipo<TAB>opciones<TAB>argumento<TAB>etiqueta
#   clave: id del video / id de la playlist / ruta del curso (para no repetir el mismo pedido)
#   opciones: SIN_IA=1 MAX_VIDEOS=2 APUNTES_MOTOR=opencode… del momento de encolar (cada pedido
#   lleva las suyas); "-" si no hay (un campo vacío no sirve: "read" con IFS=tab junta dos tabs
#   seguidos en uno)
SCRIPTS="${SCRIPTS_COLA:-$HOME/.config/hypr/scripts}"  # SCRIPTS_COLA: para las pruebas
DIR_COLA="${DIR_COLA:-$HOME/.cache/auto-captura}"   # DIR_COLA: para las pruebas y para colas en paralelo (…/cola-1, cola-2)
export DIR_COLA   # curso-a-apuntes.sh lo usa para tener un candado por cola
COLA="$DIR_COLA/cola.txt"
ACTUAL="$DIR_COLA/actual.txt"
OPCIONES="SIN_IA SIN_APUNTES MAX_VIDEOS APUNTES_MOTOR APUNTES_MODELO_OPENCODE"   # variables que viajan con cada pedido
mkdir -p "$DIR_COLA"
touch "$COLA" "$ACTUAL"

bloquear_cola() { exec 7>"$DIR_COLA/cola.lock"; flock 7; }   # secciones cortas: leer/escribir cola
soltar_cola() { flock -u 7; exec 7>&-; }
avisar() { notify-send -a "Auto-captura" "$@" 2>/dev/null || true; }

clave_de() {  # clave <tipo> <arg>: identifica el pedido aunque el link cambie un poco
    local tipo=$1 arg=$2 id
    case "$tipo" in
        playlist) id=$(sed -nE 's/.*[?&]list=([A-Za-z0-9_-]+).*/\1/p' <<<"$arg") ;;
        video) id=$(sed -nE 's#.*([?&]v=|youtu\.be/|/shorts/|/live/|/embed/)([A-Za-z0-9_-]{11}).*#\2#p' <<<"$arg") ;;
        curso) id=$(realpath -m "$arg") ;;
    esac
    echo "$tipo:${id:-$arg}"
}

trabajador_vivo() {  # ¿hay un trabajador corriendo? (tiene tomado trabajador.lock)
    ( flock -n 9 || exit 0; exit 1 ) 9>"$DIR_COLA/trabajador.lock"
}

encolar() {
    local tipo=$1 arg=$2 etiqueta=${3:-$2} clave opciones="" v pos
    [[ "$tipo" =~ ^(video|playlist|curso)$ ]] && [ -n "$arg" ] || { echo "Uso: $0 encolar <video|playlist|curso> <arg> [etiqueta]"; exit 1; }
    clave=$(clave_de "$tipo" "$arg")
    for v in $OPCIONES; do [ -n "${!v}" ] && opciones+="$v=${!v} "; done
    opciones=${opciones% }
    bloquear_cola
    # actual.txt de un trabajador que ya no existe (se cortó, reinicio…): se descarta
    trabajador_vivo || : > "$ACTUAL"
    if [ "$(cut -f1 "$ACTUAL")" = "$clave" ]; then
        soltar_cola; avisar -t 6000 "Ya se está procesando" "$etiqueta"; echo "ya en proceso"; return 0
    fi
    if cut -f1 "$COLA" | grep -qxF -- "$clave"; then
        pos=$(cut -f1 "$COLA" | grep -nxF -- "$clave" | cut -d: -f1)
        soltar_cola; avisar -t 6000 "Ya estaba en la cola (posición $pos)" "$etiqueta"; echo "ya en cola $pos"; return 0
    fi
    printf '%s\t%s\t%s\t%s\t%s\n' "$clave" "$tipo" "${opciones:--}" "$arg" "${etiqueta//$'\t'/ }" >> "$COLA"
    pos=$(wc -l < "$COLA")
    local ocupado=0
    [ -s "$ACTUAL" ] || [ "$pos" -gt 1 ] && ocupado=1  # pos > 1: quedaron pedidos de antes
    soltar_cola
    if [ "$ocupado" = 1 ]; then
        avisar -t 6000 "⏳ En cola (posición $pos)" "$etiqueta\nEmpieza cuando termine lo que se está procesando."
        echo "en cola $pos"
    else
        echo "empieza ya"
    fi
    # Despertar al trabajador (si ya hay uno, este sale solo al no poder tomar el lock)
    setsid bash "$0" trabajar </dev/null >>"$DIR_COLA/cola.log" 2>&1 &
}

trabajar() {
    exec 8>"$DIR_COLA/trabajador.lock"
    # -w 3 y no -n: "estado" o "encolar" toman este lock un instante para ver si hay trabajador;
    # si justo coincide no hay que rendirse. Un trabajador de verdad lo tiene por horas.
    flock -w 3 8 || exit 0  # ya hay un trabajador: él va a tomar lo nuevo
    echo $$ > "$DIR_COLA/trabajador.pid"
    trap ': > "$ACTUAL"' EXIT
    local linea clave tipo opciones arg etiqueta log codigo
    while true; do
        bloquear_cola
        linea=$(head -n 1 "$COLA")
        if [ -z "$linea" ]; then
            # Cola vacía: soltar el lock de trabajador ANTES que el de la cola. Así, un pedido que
            # llegue justo ahora o lo ve este trabajador o encuentra el lock libre y arranca otro.
            : > "$ACTUAL"
            flock -u 8; exec 8>&-
            soltar_cola
            echo "$(date '+%F %T') cola vacía: el trabajador termina"
            exit 0
        fi
        sed -i '1d' "$COLA"
        printf '%s\n' "$linea" > "$ACTUAL"
        soltar_cola
        IFS=$'\t' read -r clave tipo opciones arg etiqueta <<<"$linea"
        [ "$opciones" = - ] && opciones=""
        log=$(mktemp "$DIR_COLA/${tipo}_$(date +%Y%m%d_%H%M%S)_XXX.log")
        echo "$(date '+%F %T') empieza $tipo: $arg (log: $log)"
        case "$tipo" in
            video) avisar -t 4000 "📥 Capturas de YouTube" "Leyendo el link… en unos segundos aparece la barrita de progreso."
                   set -- bash "$SCRIPTS/video-a-capturas.sh" "$arg" ;;
            playlist) set -- bash "$SCRIPTS/playlist-a-apuntes.sh" "$arg" ;;
            curso) set -- bash "$SCRIPTS/curso-a-apuntes.sh" "$arg" ;;
            *) echo "tipo desconocido: $tipo"; continue ;;
        esac
        # 7>&- 8>&-: los hijos no heredan los locks (si no, un hijo colgado trabaría la cola)
        # env -u: las opciones son las del pedido, no las que heredó el trabajador del primero
        # shellcheck disable=SC2086
        env $(printf -- '-u %s ' $OPCIONES) $opciones "$@" > "$log" 2>&1 < /dev/null 7>&- 8>&-
        codigo=$?
        echo "$(date '+%F %T') terminó $tipo (código $codigo)"
        if [ $codigo -ne 0 ] && [ "$tipo" = video ]; then  # playlist/curso avisan por su cuenta
            avisar -u critical -t 10000 "Capturas de YouTube: falló" "Revisá el detalle en:\n$log"
        fi
    done
}

estado() {
    if trabajador_vivo && [ -s "$ACTUAL" ]; then
        echo "▶ Procesando: $(cut -f5 "$ACTUAL") [$(cut -f2 "$ACTUAL")]"
    else
        echo "▶ Nada en proceso"
    fi
    if [ -s "$COLA" ]; then
        echo "⏳ En cola:"; cut -f2,5 "$COLA" | awk -F'\t' '{ printf "  %d. %s [%s]\n", NR, $2, $1 }'
    else
        echo "⏳ Cola vacía"
    fi
}

case "$1" in
    encolar) shift; encolar "$@" ;;
    trabajar) trabajar ;;
    estado) estado ;;
    vaciar) bloquear_cola; : > "$COLA"; soltar_cola; echo "Cola vaciada" ;;
    cancelar)
        bloquear_cola; : > "$COLA"; soltar_cola
        PID=$(cat "$DIR_COLA/trabajador.pid" 2>/dev/null)
        if [ -n "$PID" ] && trabajador_vivo; then
            kill -TERM -- "-$PID" 2>/dev/null  # todo el grupo: trabajador + script + yt-dlp…
            echo "Cancelado (se retoma volviendo a pedir el mismo link o curso)"
        else
            echo "No había nada en proceso"
        fi ;;
    estado-todo)  # la cola principal y las colas paralelas (…/auto-captura/cola-N)
        for d in "$HOME/.cache/auto-captura" "$HOME"/.cache/auto-captura/cola-*/; do
            [ -d "$d" ] || continue; echo "── $(basename "${d%/}")"; DIR_COLA="${d%/}" bash "$0" estado
        done ;;
    *) sed -n '2,13p' "$0"; exit 1 ;;
esac
