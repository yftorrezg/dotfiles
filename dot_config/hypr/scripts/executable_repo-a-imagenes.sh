#!/bin/bash
# SUPER+ALT+G: toma el link de GitHub/GitLab/Codeberg copiado (Ctrl+C) y arma UNA carpeta con
# imágenes del código de todo el repo, en orden, para pasarlas con Gwenview (D/A).
# No usa IA ni cuota: renderiza el texto real (repo-a-imagenes.py), tarda segundos.
# Uso desde la terminal: repo-a-imagenes.sh [link] [opciones de repo-a-imagenes.py, ej. --md]
SCRIPTS="$HOME/.config/hypr/scripts"
URL=${1:-$(wl-paste --no-newline 2>/dev/null)}
URL=$(tr -d '[:space:]' <<<"$URL")
[ $# -gt 0 ] && shift
if ! [[ "$URL" =~ ^https?://(www\.)?(github\.com|gitlab\.com|codeberg\.org)/[^/]+/[^/]+ ]]; then
    notify-send -t 6000 "Código del repo → imágenes" "Primero copiá el link del repositorio (Ctrl+C).\nLo copiado no es de GitHub, GitLab ni Codeberg."
    exit 1
fi
notify-send -t 4000 "💻 Código del repo → imágenes" "Clonando y armando las imágenes…"
SAL=$(mktemp)
python3 -I "$SCRIPTS/repo-a-imagenes.py" "$URL" "$@" >"$SAL" 2>&1
COD=$?
if [ $COD -eq 0 ]; then
    CARPETA=$(tail -n 1 "$SAL")
    RES=$(grep -m1 '^Listo' "$SAL")
    notify-send -t 8000 "✅ Código listo" "$RES"
    PRIMERA=$(find "$CARPETA" -maxdepth 1 -name '*.webp' | sort | head -n 1)
    [ -n "$PRIMERA" ] && setsid gwenview "$PRIMERA" >/dev/null 2>&1 &
elif [ $COD -eq 2 ]; then
    CUANTAS=$(head -n 1 "$SAL")
    notify-send -u critical -t 12000 "Código del repo: son muchas imágenes" \
        "$CUANTAS\nUsá un link a una subcarpeta (/tree/main/carpeta) o repo-a-imagenes.sh <link> --si"
else
    notify-send -u critical -t 12000 "Código del repo: falló" "$(tail -n 3 "$SAL" | cut -c1-200)"
fi
rm -f "$SAL"
