#!/bin/bash
# SUPER+ALT+P: retomar los apuntes/capturas tras un reinicio o un corte.
# La cola (cola-capturas.sh) guarda lo pendiente en ~/.cache/auto-captura/cola.txt y lo que
# estaba en marcha en actual.txt. Si el trabajador murió (reinicio, apagón, cancelar), este script:
#   1) devuelve al frente de la cola lo que estaba en marcha (las clases ya hechas se saltean solas),
#   2) despierta al trabajador para seguir con todo lo pendiente.
SCRIPTS="$HOME/.config/hypr/scripts"
DIR_COLA="${DIR_COLA:-$HOME/.cache/auto-captura}"
ACTUAL="$DIR_COLA/actual.txt"
COLA="$DIR_COLA/cola.txt"
avisar() { notify-send -a "Auto-captura" "$@" 2>/dev/null || true; }
mkdir -p "$DIR_COLA"; touch "$ACTUAL" "$COLA"

# ¿hay un trabajador vivo? (tiene tomado trabajador.lock)
vivo() { ( flock -n 9 || exit 0; exit 1 ) 9>"$DIR_COLA/trabajador.lock"; }

if vivo; then
    avisar "Ya se está procesando" "$(cut -f5 "$ACTUAL" | head -1)\nPendientes en cola: $(wc -l < "$COLA")"
    exit 0
fi

# Trabajador muerto: lo que quedó "en marcha" vuelve al frente de la cola.
if [ -s "$ACTUAL" ]; then
    cat "$ACTUAL" "$COLA" | awk -F'\t' '!visto[$1]++' > "$COLA.nuevo" && mv "$COLA.nuevo" "$COLA"
    : > "$ACTUAL"
fi

n=$(wc -l < "$COLA")
if [ "$n" -eq 0 ]; then
    avisar "Nada que retomar" "La cola está vacía. Para empezar un curso: SUPER+ALT+A."
    exit 0
fi

setsid bash "$SCRIPTS/cola-capturas.sh" trabajar </dev/null >>"$DIR_COLA/cola.log" 2>&1 &
avisar "▶ Retomando apuntes" "$n pedido(s) en cola. Las clases ya hechas se saltean."
