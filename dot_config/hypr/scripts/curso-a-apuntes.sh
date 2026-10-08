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


# Nombre de la carpeta de una clase dentro de capturas/ (nombre_largo = el de la versión anterior,
# solo para renombrar lo ya hecho).
nombre_largo() {
    local sub="$1" clase="$2"
    if [ "$sub" = . ]; then echo "$clase"
    elif [ "$clase" = "$(basename "$sub")" ]; then echo "${sub//\// - }"
    else echo "${sub//\// - } - $clase"; fi
}
nombre_corto() {
    python3 -I - "$PREFIJO_COMUN" "$1" "$2" <<'PY'
import re, sys
prefijo, sub, clase = sys.argv[1:4]
def limpia(t):
    t = re.sub(r"@\w+\s*", "", t)               # "@RecursosCompartidos"
    t = re.sub(r"^\s*(\d+)\s*[.)]\s+", r"\1 ", t)  # "001. X" -> "001 X" (el número ordena las clases)
    t = re.sub(r"[\s/]*-\s*$", "", t)
    return re.sub(r"\s{2,}", " ", t).strip()
if prefijo and (sub + "/").startswith(prefijo):
    sub = (sub + "/")[len(prefijo):].rstrip("/") or "."
partes = [limpia(x) for x in sub.split("/")] if sub != "." else []
partes = [x for x in partes if x]
c = limpia(clase) or clase
sin_num = lambda t: re.sub(r"^\d+(\s*[-.]\s*|\s+)", "", t).strip().lower()
if partes and (sin_num(c) == sin_num(partes[-1]) or c.lower() == partes[-1].lower()):
    nom = " - ".join(partes)                       # la clase se llama como el tema
else:
    nom = " - ".join(partes + [c])
nom = nom.replace("/", "-")
if len(nom.encode()) > 120:                        # tope de largo (el sistema admite 255 bytes)
    nom = nom.encode()[:120].decode(errors="ignore").rstrip(" -.")
print(nom)
PY
}

# Videos del curso, una vez por clase, buscando también en las subcarpetas (un curso suele tener
# una carpeta por tema). Rutas relativas al curso. Si están "clase.mp4" y "clase.es.mp4" (doblado)
# se usa el doblado (trae subtítulos adentro). Se ignoran descargas a medias (.part) y las carpetas
# capturas/ (salida de este mismo script).
mapfile -t VIDEOS < <(
    find "$CURSO" -type d -name capturas -prune -o -type f \( -iname '*.mp4' -o -iname '*.mkv' -o -iname '*.webm' -o -iname '*.mov' -o -iname '*.ts' \) \
        ! -name '*.part' ! -name '*.temp.*' -printf '%P\n' |
    awk '{ clase=$0; sub(/\.[^.\/]*$/, "", clase); es = (clase ~ /\.(es|en)$/); sub(/\.(es|en)$/, "", clase);
           if (!(clase in elegido) || es) elegido[clase]=$0 }
         END { for (c in elegido) print elegido[c] }' | LC_ALL=C.UTF-8 sort -V)
TOTAL=${#VIDEOS[@]}
# Tramo de carpetas común a todas las clases (ej. "Universidad Desarrollo Web - FrontEnd Web Developer!/")
PREFIJO_COMUN=$(printf '%s\n' "${VIDEOS[@]}" | python3 -I -c '
import os, sys
d = [os.path.dirname(l.rstrip("\n")).split("/") for l in sys.stdin if l.strip()]
d = [x for x in d if x != [""]]
c = os.path.commonprefix(d) if d else []
print("/".join(c) + "/" if c and len(d) == sum(1 for _ in d) else "")')
declare -A USADOS=()
[ "$TOTAL" -eq 0 ] && { notify-send "Apuntes del curso" "No hay videos en $CURSO"; exit 1; }

# Una sola barrita de progreso para todo el curso ("clase 3/10")
export PROGRESO_ARCHIVO="${XDG_RUNTIME_DIR:-/tmp}/curso-a-apuntes-progreso.$$"
python3 "$SCRIPTS/progreso.py" poner 0 capturas "empezando"
# 9>&-: que la barrita (vive unos segundos más) no se quede con el lock
setsid python3 "$SCRIPTS/progreso.py" seguir "$PROGRESO_ARCHIVO" "$NOMBRE_CURSO" >/dev/null 2>&1 9>&- &
HECHAS=0; FALLARON=()
for i in "${!VIDEOS[@]}"; do
    V="${VIDEOS[$i]}"
    SUB=$(dirname "$V")
    CLASE=$(basename "${V%.*}" | sed -E 's/\.(es|en)$//')
    # Salida: todas las clases en $CURSO/capturas/ (así el índice y el panel ven el curso entero).
    # Nombre corto: sin los tramos de ruta comunes a todo el curso, sin "@Canal"/"NNN." de los
    # nombres de Telegram, sin repetir el título de la subcarpeta, tope de largo (ver nombre_corto).
    NOM=$(nombre_corto "$SUB" "$CLASE")
    # Dos clases que quedan con el mismo nombre corto: la segunda lleva " (2)", etc.
    BASE_NOM="$NOM"; n=2
    while [ -n "${USADOS[$NOM]:-}" ] && [ "${USADOS[$NOM]}" != "$V" ]; do NOM="$BASE_NOM ($n)"; n=$((n + 1)); done
    USADOS[$NOM]="$V"
    DEST="$CURSO/capturas/$NOM"
    # Apuntes hechos con una versión anterior: se renombran/mueven a su lugar
    VIEJO="$CURSO/$SUB/capturas/$CLASE"
    if [ "$SUB" != . ] && [ -d "$VIEJO" ] && [ ! -e "$DEST" ]; then
        mkdir -p "$CURSO/capturas" && mv "$VIEJO" "$DEST"
        # el índice viejo de esa subcarpeta ya no corresponde (el panel lo tomaría por otro curso)
        [ -f "$CURSO/$SUB/capturas/INDICE.md" ] && mv -f "$CURSO/$SUB/capturas/INDICE.md" "$CURSO/$SUB/capturas/.INDICE-viejo.md"
    fi
    VIEJO2="$CURSO/capturas/$(nombre_largo "$SUB" "$CLASE")"
    [ "$VIEJO2" != "$DEST" ] && [ -d "$VIEJO2" ] && [ ! -e "$DEST" ] && mv "$VIEJO2" "$DEST"
    export PROGRESO_CLASE="$((i + 1))/$TOTAL"
    echo "===== [$((i + 1))/$TOTAL] $CLASE ($(date +%H:%M)) ====="
    if [ -f "$DEST/apuntes.md" ]; then
        echo "Ya tiene apuntes: se saltea"
        HECHAS=$((HECHAS + 1)); continue
    fi
    if DESTINO="$DEST" nice -n 19 ionice -c 3 bash "$SCRIPTS/video-a-capturas.sh" "$CURSO/$V" \
        && [ -f "$DEST/apuntes.md" ]; then
        HECHAS=$((HECHAS + 1))
        python3 "$SCRIPTS/cuadernillo.py" --indice "$CURSO/capturas" >/dev/null
        panel
    else
        FALLARON+=("$NOM")
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
