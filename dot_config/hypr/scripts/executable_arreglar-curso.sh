#!/bin/bash
# arreglar-curso.sh <carpeta del curso> [--ver]
# Deja un curso YA PROCESADO como el piloto (Oracle PL/SQL, 08/11/2026), sin IA ni cuota:
#   1. normalizar-curso.py  estructura: copias "(1)" repetidas, carpetas Tema/Tema, nombres de Apuntes/ al día
#   2. ordenar-curso.py     capturas/→Apuntes/, capturas clave/esenciales, sin todas-las-capturas ni basura, .srt ocultos, colores
#   3. rearmar-curso.py     apuntes y tarjetas con el presupuesto de lectura (desde el JSON guardado de la IA)
#   4. codigo-curso-a-imagenes.py + INDICE.md
# Se puede correr las veces que haga falta. --ver: solo los pasos 1 y 2 en simulación.
SCRIPTS="$HOME/.config/hypr/scripts"
CURSO=$(realpath "${1:?Uso: $0 <carpeta del curso> [--ver]}")
[ -d "$CURSO" ] || { echo "No existe: $CURSO"; exit 1; }
if [ "${2:-}" = --ver ]; then
    python3 "$SCRIPTS/normalizar-curso.py" "$CURSO" --ver
    python3 "$SCRIPTS/ordenar-curso.py" "$CURSO" --ver
    exit 0
fi
echo "===== $(basename "$CURSO") ($(date +%H:%M))"
python3 "$SCRIPTS/normalizar-curso.py" "$CURSO" || echo "⚠️ normalizar falló"
python3 "$SCRIPTS/ordenar-curso.py" "$CURSO" || echo "⚠️ ordenar falló"
python3 "$SCRIPTS/rearmar-curso.py" "$CURSO" 2>&1 | grep -v "sobre el presupuesto:" || echo "⚠️ rearmar falló"
python3 "$SCRIPTS/codigo-curso-a-imagenes.py" "$CURSO" 2>&1 | tail -2
[ -d "$CURSO/Apuntes" ] && python3 "$SCRIPTS/cuadernillo.py" --indice "$CURSO/Apuntes" >/dev/null 2>&1
python3 "$SCRIPTS/ordenar-curso.py" "$CURSO" >/dev/null  # colores y .hidden de lo que se acaba de crear
echo "===== listo $(basename "$CURSO") ($(date +%H:%M))"
