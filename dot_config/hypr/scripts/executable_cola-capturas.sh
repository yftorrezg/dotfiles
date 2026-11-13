#!/bin/bash
# Cola de trabajos de capturas + apuntes: links de YouTube (SUPER+ALT+Y), playlists y cursos
# descargados (SUPER+ALT+A). Se procesan de a UNO, en orden, así no compiten por la CPU.
# Si aprietan el atajo mientras ya hay algo en marcha, el pedido queda en cola y avisa la posición.
# Uso:
#   cola-capturas.sh encolar <video|playlist|curso> <url o carpeta> [etiqueta]
#   cola-capturas.sh estado          # qué se está procesando y qué espera
#   cola-capturas.sh mover <clave> <posición>   # reordena lo que espera (1 = el próximo)
#   cola-capturas.sh pausar <clave>  # la salta hasta reanudarla (sigue en su lugar)
#   cola-capturas.sh reanudar <clave>
#   cola-capturas.sh quitar <clave>  # la saca de la cola (si no está en marcha)
#   cola-capturas.sh vaciar          # borra lo que espera (lo que está en marcha sigue)
#   cola-capturas.sh cancelar        # vaciar + cortar lo que está en marcha (se puede reanudar)
#   cola-capturas.sh trabajar        # (interno) el único trabajador; sale cuando la cola queda vacía
# Archivos en ~/.cache/auto-captura/: cola.txt (lo que espera, una línea por pedido),
# actual.txt (lo que se está procesando), pausados.txt (claves que se saltean), cola.lock /
# trabajador.lock (flock) y logs.
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
PAUSADOS="$DIR_COLA/pausados.txt"   # una clave por línea: el trabajador las saltea sin sacarlas de la cola
OPCIONES="SIN_IA SIN_APUNTES MAX_VIDEOS APUNTES_MOTOR APUNTES_MODELO_OPENCODE APUNTES_CODEX_MODELO APUNTES_CODEX_EFFORT APUNTES_RESPALDO_EFFORT"   # variables que viajan con cada pedido
mkdir -p "$DIR_COLA"
touch "$COLA" "$ACTUAL" "$PAUSADOS"

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
    local ocupado=0 delante
    if [ -s "$ACTUAL" ]; then
        ocupado=1
    else
        # Los pausados no cuentan: si todos los de antes están en pausa, este empieza ya.
        delante=$(head -n -1 "$COLA" | cut -f1 | grep -vxF -f "$PAUSADOS" | wc -l)
        [ "$delante" -gt 0 ] && ocupado=1
    fi
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
    local linea clave tipo opciones arg etiqueta log codigo n i l
    while true; do
        bloquear_cola
        # Primer pedido que no esté en pausa (los pausados quedan en su lugar, se saltean).
        linea=""; n=0; i=0
        while IFS= read -r l; do
            i=$((i + 1))
            if ! grep -qxF -- "${l%%$'\t'*}" "$PAUSADOS"; then linea=$l; n=$i; break; fi
        done < "$COLA"
        if [ -z "$linea" ]; then
            # Cola vacía o todo pausado: soltar el lock de trabajador ANTES que el de la cola. Así,
            # un pedido que llegue justo ahora o lo ve este trabajador o encuentra el lock libre y
            # arranca otro. Si todo estaba pausado, reanudar vuelve a despertar al trabajador.
            : > "$ACTUAL"
            flock -u 8; exec 8>&-
            soltar_cola
            if [ -s "$COLA" ]; then
                echo "$(date '+%F %T') todo en pausa: el trabajador termina"
            else
                echo "$(date '+%F %T') cola vacía: el trabajador termina"
            fi
            exit 0
        fi
        sed -i "${n}d" "$COLA"
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
        echo "⏳ En cola:"
        local i=0 k tipo opciones arg etiqueta pausa
        while IFS=$'\t' read -r k tipo opciones arg etiqueta; do
            i=$((i + 1))
            if grep -qxF -- "$k" "$PAUSADOS"; then pausa=" ⏸"; else pausa=""; fi
            printf '  %d. %s [%s]%s\n' "$i" "$etiqueta" "$tipo" "$pausa"
        done < "$COLA"
        if [ "$(cut -f1 "$COLA" | grep -vxF -f "$PAUSADOS" | wc -l)" -eq 0 ]; then
            echo "⏸ Todo en pausa: reanudá una desde la barrita o con: $0 reanudar <clave>"
        fi
    else
        echo "⏳ Cola vacía"
    fi
}

mover() {  # mover <clave> <posición>: el pedido que espera pasa a esa posición (1 = el próximo)
    local clave=$1 nueva=$2 total
    [[ "$nueva" =~ ^[0-9]+$ ]] && [ "$nueva" -ge 1 ] || { echo "Uso: $0 mover <clave> <posición>"; return 1; }
    bloquear_cola
    if ! cut -f1 "$COLA" | grep -qxF -- "$clave"; then
        soltar_cola; echo "Ya no está en cola"; return 1
    fi
    total=$(wc -l < "$COLA")
    [ "$nueva" -gt "$total" ] && nueva=$total
    CLAVE="$clave" NUEVA="$nueva" awk -F'\t' '
        { if ($1 == ENVIRON["CLAVE"]) que = $0; else otras[++m] = $0 }
        END { j = 0; for (i = 1; i <= NR; i++) { if (i == ENVIRON["NUEVA"] + 0) print que; else print otras[++j] } }
    ' "$COLA" > "$COLA.tmp" && mv "$COLA.tmp" "$COLA"
    soltar_cola
    echo "Movido a la posición $nueva"
}

pausar() {  # pausar <clave>: la cola la saltea hasta reanudarla; sigue en su lugar
    local clave=$1
    [ -n "$clave" ] || { echo "Uso: $0 pausar <clave>"; return 1; }
    bloquear_cola
    if [ "$(cut -f1 "$ACTUAL")" = "$clave" ]; then
        soltar_cola; echo "Está en proceso; no se puede pausar desde la cola"; return 1
    fi
    if ! cut -f1 "$COLA" | grep -qxF -- "$clave"; then
        soltar_cola; echo "No está en cola"; return 1
    fi
    grep -qxF -- "$clave" "$PAUSADOS" || printf '%s\n' "$clave" >> "$PAUSADOS"
    soltar_cola
    echo "Pausado"
}

reanudar() {  # reanudar <clave>: vuelve a entrar en el turno; despierta al trabajador
    local clave=$1
    [ -n "$clave" ] || { echo "Uso: $0 reanudar <clave>"; return 1; }
    bloquear_cola
    if [ -s "$PAUSADOS" ]; then
        grep -vxF -- "$clave" "$PAUSADOS" > "$PAUSADOS.tmp" || :
        mv "$PAUSADOS.tmp" "$PAUSADOS"
    fi
    soltar_cola
    echo "Reanudado"
    # Siempre despertar: si ya hay trabajador, este sale solo al no poder tomar el lock. Así no
    # queda nadie esperando si el trabajador anterior se retiró justo al ver todo en pausa.
    setsid bash "$0" trabajar </dev/null >>"$DIR_COLA/cola.log" 2>&1 &
}

quitar() {  # quitar <clave>: la saca de la cola (la que está en marcha no se toca)
    local clave=$1
    [ -n "$clave" ] || { echo "Uso: $0 quitar <clave>"; return 1; }
    bloquear_cola
    if [ "$(cut -f1 "$ACTUAL")" = "$clave" ]; then
        soltar_cola; echo "Está en proceso; usá cancelar si querés cortarlo"; return 1
    fi
    if ! cut -f1 "$COLA" | grep -qxF -- "$clave"; then
        soltar_cola; echo "No está en cola"; return 1
    fi
    awk -F'\t' -v c="$clave" '$1 != c' "$COLA" > "$COLA.tmp" && mv "$COLA.tmp" "$COLA"
    grep -vxF -- "$clave" "$PAUSADOS" > "$PAUSADOS.tmp" || :
    mv "$PAUSADOS.tmp" "$PAUSADOS"
    soltar_cola
    echo "Quitado de la cola"
}

case "$1" in
    encolar) shift; encolar "$@" ;;
    trabajar) trabajar ;;
    estado) estado ;;
    mover) shift; mover "$@" ;;
    pausar) shift; pausar "$@" ;;
    reanudar) shift; reanudar "$@" ;;
    quitar) shift; quitar "$@" ;;
    vaciar) bloquear_cola; : > "$COLA"; : > "$PAUSADOS"; soltar_cola; echo "Cola vaciada" ;;
    cancelar)
        bloquear_cola; : > "$COLA"; : > "$PAUSADOS"; soltar_cola
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
    *) sed -n '2,16p' "$0"; exit 1 ;;
esac
