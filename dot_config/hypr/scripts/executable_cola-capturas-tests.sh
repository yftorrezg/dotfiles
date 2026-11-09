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

esperar_parado() {  # el trabajador arrancó y terminó; $1 = clave que tiene que haber salido de la cola
    for _ in $(seq 120); do
        if ( flock -n 9 ) 9>"$DIR_COLA/trabajador.lock" && [ ! -s "$DIR_COLA/actual.txt" ] \
           && ! cut -f1 "$DIR_COLA/cola.txt" | grep -qxF -- "${1:-}"; then return 0; fi
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

# 4) Reordenar lo que espera (mover): por clave, sin tocar lo demás
printf 'curso:A\tcurso\t-\tA\t📚 A\ncurso:B\tcurso\t-\tB\t📚 B\ncurso:C\tcurso\t-\tC\t📚 C\n' > "$DIR_COLA/cola.txt"
orden() { cut -f1 "$DIR_COLA/cola.txt" | sed 's/^curso://' | tr '\n' ' '; }
bash "$COLA_SH" mover "curso:C" 1 >/dev/null
[ "$(orden)" = "C A B " ] && bien "mover: C pasa al frente" || falla "mover al frente: '$(orden)'"
bash "$COLA_SH" mover "curso:C" 3 >/dev/null
[ "$(orden)" = "A B C " ] && bien "mover: C pasa al final" || falla "mover al final: '$(orden)'"
bash "$COLA_SH" mover "curso:A" 99 >/dev/null
[ "$(orden)" = "B C A " ] && bien "mover: posición fuera de rango = al final" || falla "mover fuera de rango: '$(orden)'"
bash "$COLA_SH" mover "curso:Z" 1 >/dev/null
[ "$(orden)" = "B C A " ] && bien "mover: clave que no está no cambia nada" || falla "mover clave inexistente: '$(orden)'"
[ "$(cut -f5 "$DIR_COLA/cola.txt" | head -n 1)" = "📚 B" ] && bien "mover: conserva etiqueta y campos" || falla "mover: campos alterados"

# 5) Pausar / reanudar / quitar lo que espera
: > "$REG"; : > "$DIR_COLA/pausados.txt"
printf 'curso:A\tcurso\t-\tA\t📚 A\ncurso:B\tcurso\t-\tB\t📚 B\ncurso:C\tcurso\t-\tC\t📚 C\n' > "$DIR_COLA/cola.txt"
bash "$COLA_SH" pausar "curso:B" >/dev/null
bash "$COLA_SH" quitar "curso:C" >/dev/null
EST=$(bash "$COLA_SH" estado)
grep -q "B \[curso\] ⏸" <<<"$EST" && bien "pausar: B queda marcado" || falla "estado pausado: $EST"
grep -q "C" <<<"$EST" && falla "quitar: C sigue en la cola" || bien "quitar: C fuera"
[ "$(orden)" = "A B " ] && bien "quitar: solo se fue C" || falla "quitar dejó '$(orden)'"
[ "$(cat "$DIR_COLA/pausados.txt")" = "curso:B" ] && bien "pausar: anotado en pausados.txt" || falla "pausados: '$(cat "$DIR_COLA/pausados.txt")'"
ESPERA_FALSA=0.3 bash "$COLA_SH" encolar video "https://youtu.be/pausa000001" >/dev/null
esperar_parado "video:pausa000001" || falla "pausa: el trabajador no terminó"
grep -q "^inicio A" "$REG" && grep -q "^inicio https://youtu.be/pausa000001" "$REG" && bien "pausa: procesó A y el video nuevo" || { falla "pausa: registro incompleto"; cat "$REG"; }
grep -q "^inicio B" "$REG" && falla "pausa: B se procesó igual" || bien "pausa: B se saltó"
[ "$(orden)" = "B " ] && bien "pausa: B sigue esperando en su lugar" || falla "pausa: cola '$(orden)'"
bash "$COLA_SH" reanudar "curso:B" >/dev/null
esperar_fin || falla "reanudar: el trabajador no terminó"
grep -q "^inicio B" "$REG" && bien "reanudar: B se procesó" || falla "reanudar: B no se procesó"
[ -s "$DIR_COLA/pausados.txt" ] && falla "reanudar: quedó pausados.txt" || bien "reanudar: limpia la pausa"
bash "$COLA_SH" pausar "curso:Z" >/dev/null 2>&1
[ -s "$DIR_COLA/pausados.txt" ] && falla "pausar inexistente: anotó algo" || bien "pausar: clave que no está no hace nada"
printf 'curso:X\tcurso\t-\tX\t📚 X\n' > "$DIR_COLA/cola.txt"; printf 'curso:X\n' > "$DIR_COLA/pausados.txt"
bash "$COLA_SH" vaciar >/dev/null
[ -s "$DIR_COLA/pausados.txt" ] && falla "vaciar: no limpió pausados" || bien "vaciar: limpia pausados"

rm -f -- "${T:?}"/scripts/* "${T:?}"/bin/* "${T:?}"/cache/* "${T:?}"/registro "${T:?}"/notificaciones
rmdir "$T/scripts" "$T/bin" "$T/cache" "$T"
[ "$FALLOS" -eq 0 ] && echo "OK" || { echo "FALLARON $FALLOS"; exit 1; }
