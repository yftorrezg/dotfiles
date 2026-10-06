#!/bin/bash
# Pruebas de playlist-a-apuntes.sh (+ video-a-capturas.sh con DESTINO/TITULO) sin YouTube ni
# Claude: un yt-dlp falso entrega la lista y un video generado con ffmpeg; auto-captura.py y
# cuadernillo.py (--sin-ia) son los de verdad. Todo queda en una carpeta temporal.
# Uso: bash playlist-a-apuntes-tests.sh     (termina con "OK" o dice qué falló)
SCRIPTS="$(dirname "$(realpath "$0")")"
T=$(mktemp -d)
export BASE_CAPTURAS="$T/salida" PATH="$T/bin:$PATH" SIN_IA=1 ESPERA_BLOQUEO=1 XDG_RUNTIME_DIR="$T"
mkdir -p "$T/bin" "$BASE_CAPTURAS"
FALLOS=0
falla() { echo "❌ $*"; FALLOS=$((FALLOS + 1)); }
bien() { echo "✔ $*"; }

# Video de prueba: 3 "pantallas de código" distintas -> 3 capturas
F=/usr/share/fonts/TTF/DejaVuSansMono.ttf
ffmpeg -loglevel error -y -f lavfi -i color=c=0x1e1e1e:s=1280x720:d=18:r=10 -vf \
"drawtext=fontfile=$F:fontcolor=white:fontsize=40:x=60:y=60:text='function hola() {',\
drawtext=fontfile=$F:fontcolor=white:fontsize=40:x=60:y=120:text='  console.log(1)':enable='gte(t,6)',\
drawtext=fontfile=$F:fontcolor=white:fontsize=40:x=60:y=180:text='}':enable='gte(t,12)'" \
    -c:v libx264 -pix_fmt yuv420p "$T/video.mp4" || { echo "no se pudo generar el video"; exit 1; }

# Lista: 1 ok · 2 privado · 3 ok (título con "/" y ":") · 4 se cae · 5 bloqueado 1 vez · 6 ok
printf '%s\n' \
    $'1\tvid00000001\t18\tIntro al curso' \
    $'2\tvid00000002\tNA\t[Private video]' \
    $'3\tvid00000003\t18\tHooks: useState/useEffect' \
    $'4\tvid00000004\t18\tVideo que se cae' \
    $'5\tvid00000005\t18\tVideo con bloqueo' \
    $'6\tvid00000006\t18\tFinal' \
    $'TITULO\tCurso: Prueba\t6' > "$T/listado"
cat > "$T/bin/yt-dlp" <<EOF
#!/bin/bash
echo "\$*" >> "$T/llamadas"
args="\$*"
[[ "\$args" == *--flat-playlist* ]] && { cat "$T/listado"; exit 0; }
[[ "\$args" == *--skip-download* ]] && exit 0           # subtítulos: no hay
url="\${@: -1}"; id=\${url##*v=}
case "\$id" in
    vid00000004) echo "ERROR: [youtube] \$id: Video unavailable"; exit 1 ;;
    vid0000000X) echo "ERROR: [youtube] \$id: Sign in to confirm you’re not a bot"; exit 1 ;;
    vid00000005) if [ ! -f "$T/ya-bloqueado" ]; then touch "$T/ya-bloqueado"
                     echo "ERROR: [youtube] \$id: Sign in to confirm you’re not a bot"; exit 1; fi ;;
esac
while [ \$# -gt 0 ]; do [ "\$1" = -o ] && salida=\$2; shift; done
cp "$T/video.mp4" "\${salida/\%(ext)s/mp4}"
echo "PROGRESO 100%"
EOF
printf '#!/bin/bash\nexit 0\n' > "$T/bin/notify-send"
chmod +x "$T/bin/yt-dlp" "$T/bin/notify-send"

CURSO="$BASE_CAPTURAS/Curso- Prueba"
URL="https://www.youtube.com/watch?v=vid00000001&list=PLprueba"

# 1) Primera corrida
bash "$SCRIPTS/playlist-a-apuntes.sh" "$URL" > "$T/log1" 2>&1
C1=$?
[ -d "$CURSO/capturas" ] && bien "carpeta del curso: $(basename "$CURSO")" || { falla "no está $CURSO"; ls -R "$T/salida"; }
for d in "001 - Intro al curso" "003 - Hooks- useState-useEffect" "005 - Video con bloqueo" "006 - Final"; do
    if [ -f "$CURSO/capturas/$d/apuntes.md" ] && [ -f "$CURSO/capturas/$d/0001.webp" ] \
        && [ -f "$CURSO/capturas/$d/.minutos.tsv" ] && [ -f "$CURSO/capturas/$d/.youtube-id" ]; then
        bien "$d: capturas + .minutos.tsv + apuntes.md"
    else
        falla "$d incompleta: $(ls -A "$CURSO/capturas/$d" 2>&1 | tr '\n' ' ')"
    fi
    ls "$CURSO/capturas/$d"/video.* >/dev/null 2>&1 && falla "$d: no se borró el video"
done
[ -e "$CURSO/capturas/002 - [Private video]" ] && falla "se creó carpeta del video privado" || bien "privado salteado"
grep -q "No disponible" "$T/log1" && bien "log avisa el no disponible" || falla "no avisa el privado"
[ -f "$CURSO/capturas/004 - Video que se cae/apuntes.md" ] && falla "004 no debería tener apuntes" || bien "004 falló sin frenar el resto"
grep -q "Fallaron: 004" "$T/log1" && bien "resumen: 'Fallaron: 004'" || falla "resumen sin 'Fallaron: 004': $(tail -1 "$T/log1")"
grep -q "frenó la descarga (vez 1)" "$T/log1" && bien "bloqueo de YouTube: esperó y reintentó 005" || falla "no reintentó 005"
N=$(grep -c "apuntes.md>" "$CURSO/capturas/INDICE.md" 2>/dev/null)
[ "$N" = 4 ] && bien "INDICE.md con 4 clases" || falla "INDICE.md con '$N' clases"
[ $C1 -eq 0 ] || falla "código de salida $C1"

# 2) Relanzar: saltea lo hecho (aunque YouTube cambie el título), reintenta solo 004
sed -i 's/Intro al curso/Course intro (traducido)/' "$T/listado"
: > "$T/llamadas"
bash "$SCRIPTS/playlist-a-apuntes.sh" "https://www.youtube.com/playlist?list=PLprueba" > "$T/log2" 2>&1
[ "$(grep -c 'se saltea' "$T/log2")" = 5 ] && bien "relanzar: 4 hechas + privado salteados" || { falla "relanzar:"; grep "=====\|saltea" "$T/log2"; }
DESCARGAS=$(grep -v -e --flat-playlist -e --skip-download "$T/llamadas" | grep -c .)
[ "$DESCARGAS" = 1 ] && bien "relanzar: solo reintentó bajar 004" || falla "relanzar bajó $DESCARGAS videos"
[ -e "$CURSO/capturas/001 - Course intro (traducido)" ] && falla "título traducido creó otra carpeta" || bien "título cambiado: reconoce la clase por .youtube-id"

# 3) MAX_VIDEOS y lock
rm -f -- "$CURSO"/capturas/006\ -\ Final/apuntes.md
MAX_VIDEOS=3 bash "$SCRIPTS/playlist-a-apuntes.sh" "$URL" > "$T/log3" 2>&1
grep -q "\[3/3\]" "$T/log3" && ! grep -q "006" "$T/log3" && bien "MAX_VIDEOS=3 procesa solo 3" || falla "MAX_VIDEOS"
( exec 9>"$T/playlist-a-apuntes.lock"; flock 9; sleep 3 ) & sleep 0.5
bash "$SCRIPTS/playlist-a-apuntes.sh" "$URL" > "$T/log4" 2>&1
[ $? -eq 1 ] && bien "lock: una segunda playlist a la vez no arranca" || falla "lock no funcionó"
wait

# 4) video-a-capturas.sh solo (sin DESTINO) sigue guardando donde siempre
bash "$SCRIPTS/video-a-capturas.sh" "$T/video.mp4" > "$T/log5" 2>&1
[ -f "$T/capturas/video/apuntes.md" ] && bien "video-a-capturas.sh sin DESTINO: <carpeta>/capturas/<nombre>/" || falla "video-a-capturas por defecto"

# 5) YouTube bloquea siempre: reintenta 3 veces y corta (código 2) sin marcar el resto como fallado
printf '%s\n' $'1\tvid0000000X\t18\tBloqueado' $'2\tvid00000006\t18\tNo llega' $'TITULO\tOtro curso\t2' > "$T/listado"
bash "$SCRIPTS/playlist-a-apuntes.sh" "https://www.youtube.com/playlist?list=PLotro" > "$T/log6" 2>&1
C6=$?
[ $C6 -eq 2 ] && grep -q "YouTube frenó las descargas" "$T/log6" && ! grep -q "No llega" "$T/log6" \
    && bien "bloqueo persistente: corta y pide reanudar más tarde" || { falla "bloqueo persistente ($C6)"; tail -3 "$T/log6"; }

case "$T" in /tmp/tmp.*) rm -r -- "$T" ;; esac   # solo la carpeta temporal de esta prueba
[ "$FALLOS" -eq 0 ] && echo "OK" || { echo "FALLARON $FALLOS"; exit 1; }
