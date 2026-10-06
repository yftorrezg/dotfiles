#!/bin/bash
# Pruebas de cola-capturas.sh sin red ni Claude: los scripts de verdad se reemplazan por unos
# falsos que solo anotan "inicio/fin" y esperan un poco; notify-send también es falso.
# Uso: bash cola-capturas-tests.sh     (termina con "OK" o dice qué falló)
COLA_SH="$(dirname "$(realpath "$0")")/cola-capturas.sh"
T=$(mktemp -d)
export DIR_COLA="$T/cache" SCRIPTS_COLA="$T/scripts" PATH="$T/bin:$PATH"
REG="$T/registro"
mkdir -p "$T/scripts" "$T/bin" "$DIR_COLA"
FALLOS=0
falla() { echo "❌ $*"; FALLOS=$((FALLOS + 1)); }
bien() { echo "✔ $*"; }

cat > "$T/bin/notify-send" <<EOF
#!/bin/bash
echo "\$*" >> "$T/notificaciones"
EOF
for s in video-a-capturas playlist-a-apuntes curso-a-apuntes; do
    cat > "$T/scripts/$s.sh" <<EOF
#!/bin/bash
echo "inicio \$1 SIN_IA=\${SIN_IA:-} MAX_VIDEOS=\${MAX_VIDEOS:-}" >> "$REG"
sleep \${ESPERA_FALSA:-1}
echo "fin \$1" >> "$REG"
EOF
done
chmod +x "$T/bin/notify-send"

esperar_fin() {  # hasta que no quede trabajador ni cola (máx. 60 s)
    for _ in $(seq 120); do
        if ( flock -n 9 ) 9>"$DIR_COLA/trabajador.lock" && [ ! -s "$DIR_COLA/cola.txt" ]; then return 0; fi
        sleep 0.5
    done
    return 1
}

# 1) Dos pulsaciones seguidas + repetidos
A="https://www.youtube.com/watch?v=AAAAAAAAAAA"
B="https://youtu.be/BBBBBBBBBBB?si=xyz"
P="https://www.youtube.com/watch?v=CCCCCCCCCCC&list=PLprueba123"
R1=$(ESPERA_FALSA=2 SIN_IA=1 bash "$COLA_SH" encolar video "$A")
sleep 0.5  # que el trabajador tome A
R2=$(bash "$COLA_SH" encolar video "$B")
R3=$(bash "$COLA_SH" encolar video "https://www.youtube.com/watch?v=AAAAAAAAAAA&list=PLotra&t=30")
R4=$(bash "$COLA_SH" encolar video "https://www.youtube.com/watch?v=BBBBBBBBBBB")
R5=$(MAX_VIDEOS=2 bash "$COLA_SH" encolar playlist "$P")
R6=$(bash "$COLA_SH" encolar playlist "https://www.youtube.com/playlist?list=PLprueba123")
R7=$(bash "$COLA_SH" encolar curso "$T/mi curso/")
EST=$(bash "$COLA_SH" estado)
[ "$R1" = "empieza ya" ] && bien "A empieza ya" || falla "A: '$R1'"
[ "$R2" = "en cola 1" ] && bien "B en cola posición 1" || falla "B: '$R2'"
[ "$R3" = "ya en proceso" ] && bien "A repetido (otro formato de link): no se duplica" || falla "A repetido: '$R3'"
[ "$R4" = "ya en cola 1" ] && bien "B repetido: no se duplica" || falla "B repetido: '$R4'"
[ "$R5" = "en cola 2" ] && bien "playlist en cola posición 2" || falla "playlist: '$R5'"
[ "$R6" = "ya en cola 2" ] && bien "misma playlist con otro link: no se duplica" || falla "playlist repetida: '$R6'"
[ "$R7" = "en cola 3" ] && bien "curso en cola posición 3" || falla "curso: '$R7'"
grep -q "Procesando" <<<"$EST" && grep -q "3\." <<<"$EST" && bien "estado muestra lo actual y 3 en cola" || falla "estado: $EST"
esperar_fin || falla "el trabajador no terminó"
ESPERADO="inicio $A SIN_IA=1 MAX_VIDEOS=
fin $A
inicio $B SIN_IA= MAX_VIDEOS=
fin $B
inicio $P SIN_IA= MAX_VIDEOS=2
fin $P
inicio $T/mi curso/ SIN_IA= MAX_VIDEOS=
fin $T/mi curso/"
[ "$(cat "$REG")" = "$ESPERADO" ] && bien "orden correcto, de a uno, cada uno con sus opciones" \
    || { falla "registro distinto:"; cat "$REG"; }
grep -q "En cola (posición 1)" "$T/notificaciones" && bien "avisó 'En cola (posición 1)'" || falla "sin aviso de cola"
sleep 0.5
pgrep -f "cola-capturas.sh trabajar" >/dev/null && ps -o args= -p "$(pgrep -f 'cola-capturas.sh trabajar')" | grep -q "$T" \
    && falla "quedó un trabajador vivo" || bien "el trabajador terminó al vaciarse la cola"

# 2) Carrera: 8 pulsaciones a la vez con links distintos -> cada uno una sola vez, nunca dos juntos
: > "$REG"
for k in 1 2 3 4 5 6 7 8; do
    ESPERA_FALSA=0.3 bash "$COLA_SH" encolar video "https://youtu.be/carrera000$k" >/dev/null &
done
wait
esperar_fin || falla "carrera: el trabajador no terminó"
[ "$(grep -c '^inicio' "$REG")" = 8 ] && bien "carrera: los 8 procesados una sola vez" || { falla "carrera:"; cat "$REG"; }
awk '/^inicio/{ if (abierto) bad=1; abierto=1 } /^fin/{ abierto=0 } END{ exit bad }' "$REG" \
    && bien "carrera: nunca dos a la vez" || falla "carrera: se solaparon"

# 3) actual.txt viejo (el trabajador murió) no bloquea volver a pedir lo mismo
: > "$REG"
printf 'video:ZZZZZZZZZZZ\tvideo\t\thttps://youtu.be/ZZZZZZZZZZZ\tviejo\n' > "$DIR_COLA/actual.txt"
R=$(bash "$COLA_SH" encolar video "https://youtu.be/ZZZZZZZZZZZ")
esperar_fin
[ "$R" = "empieza ya" ] && grep -q ZZZZ "$REG" && bien "actual.txt viejo se ignora: se reanuda" || falla "reanudar: '$R'"

rm -f -- "${T:?}"/scripts/* "${T:?}"/bin/* "${T:?}"/cache/* "${T:?}"/registro "${T:?}"/notificaciones
rmdir "$T/scripts" "$T/bin" "$T/cache" "$T"
[ "$FALLOS" -eq 0 ] && echo "OK" || { echo "FALLARON $FALLOS"; exit 1; }
