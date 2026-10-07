#!/bin/bash
# Procesa un curso entero: para cada video de la carpeta (en orden), capturas + cuadernillo de
# apuntes, y al final el INDICE.md del curso. Se puede cortar y volver a lanzar: sigue donde quedó
# (las clases ya hechas se saltean). Corre con prioridad baja para no molestar.
# Uso: curso-a-apuntes.sh <carpeta del curso>
SCRIPTS="$HOME/.config/hypr/scripts"
CURSO=$(realpath "${1:?Uso: $0 <carpeta del curso>}")
[ -d "$CURSO" ] || { echo "No existe la carpeta: $CURSO"; exit 1; }
NOMBRE_CURSO=$(basename "$CURSO")
# Panel de cursos (lo arma otro script; si no está, no pasa nada). Las tarjetas de cada clase
# las hace video-a-capturas.sh al terminar sus apuntes.
panel() { [ -f "$SCRIPTS/panel-cursos.py" ] && python3 "$SCRIPTS/panel-cursos.py" >/dev/null 2>&1 || true; }

# Un solo procesamiento a la vez (si ya hay uno, avisar y salir)
# Un procesamiento por cola: las colas paralelas (DIR_COLA=…/cola-N) tienen su propio candado
SUF=""; [[ "${DIR_COLA:-}" == */cola-* ]] && SUF=".$(basename "$DIR_COLA")"
exec 9>"${XDG_RUNTIME_DIR:-/tmp}/curso-a-apuntes$SUF.lock"
if ! flock -n 9; then
    notify-send -t 6000 "Apuntes del curso" "Ya hay un curso procesándose. Esperá a que termine."
    exit 1
fi

# Videos del curso, una vez por clase: si están "clase.mp4" y "clase.es.mp4" (doblado), se usa
# el doblado (trae subtítulos adentro). Se ignoran descargas a medias (.part).
mapfile -t VIDEOS < <(
    find "$CURSO" -maxdepth 1 -type f \( -iname '*.mp4' -o -iname '*.mkv' -o -iname '*.webm' -o -iname '*.mov' -o -iname '*.ts' \) \
        ! -name '*.part' ! -name '*.temp.*' -printf '%f\n' |
    awk '{ clase=$0; sub(/\.[^.]*$/, "", clase); es = (clase ~ /\.(es|en)$/); sub(/\.(es|en)$/, "", clase);
           if (!(clase in elegido) || es) elegido[clase]=$0 }
         END { for (c in elegido) print elegido[c] }' | sort -V)
TOTAL=${#VIDEOS[@]}
[ "$TOTAL" -eq 0 ] && { notify-send "Apuntes del curso" "No hay videos en $CURSO"; exit 1; }

# Una sola barrita de progreso para todo el curso ("clase 3/10")
export PROGRESO_ARCHIVO="${XDG_RUNTIME_DIR:-/tmp}/curso-a-apuntes-progreso.$$"
python3 "$SCRIPTS/progreso.py" poner 0 capturas "empezando"
# 9>&-: que la barrita (vive unos segundos más) no se quede con el lock
setsid python3 "$SCRIPTS/progreso.py" seguir "$PROGRESO_ARCHIVO" "$NOMBRE_CURSO" >/dev/null 2>&1 9>&- &
HECHAS=0; FALLARON=()
for i in "${!VIDEOS[@]}"; do
    V="${VIDEOS[$i]}"
    CLASE=$(basename "${V%.*}" | sed -E 's/\.(es|en)$//')
    export PROGRESO_CLASE="$((i + 1))/$TOTAL"
    echo "===== [$((i + 1))/$TOTAL] $CLASE ($(date +%H:%M)) ====="
    if [ -f "$CURSO/capturas/$CLASE/apuntes.md" ]; then
        echo "Ya tiene apuntes: se saltea"
        HECHAS=$((HECHAS + 1)); continue
    fi
    if nice -n 19 ionice -c 3 bash "$SCRIPTS/video-a-capturas.sh" "$CURSO/$V" \
        && [ -f "$CURSO/capturas/$CLASE/apuntes.md" ]; then
        HECHAS=$((HECHAS + 1))
        python3 "$SCRIPTS/cuadernillo.py" --indice "$CURSO/capturas" >/dev/null
        panel
    else
        FALLARON+=("$CLASE")
        notify-send -u critical -t 8000 "Apuntes: falló una clase" "$CLASE"
    fi
done

python3 "$SCRIPTS/cuadernillo.py" --indice "$CURSO/capturas"
panel
# Clases que quedaron sin resumen de IA (Claude no respondió): se rehacen ahora, sin bajar nada
[ "${SIN_IA:-0}" = 1 ] || python3 "$SCRIPTS/rehacer-sin-ia.py" "$CURSO/capturas" || true
MSG="$HECHAS de $TOTAL clases con apuntes."
[ ${#FALLARON[@]} -gt 0 ] && MSG="$MSG Fallaron: ${FALLARON[*]}"
export PROGRESO_RANGO="0 100" PROGRESO_CLASE=""
python3 "$SCRIPTS/progreso.py" poner 100 fin "🎓 $MSG Índice: capturas/INDICE.md"
echo "$MSG"
