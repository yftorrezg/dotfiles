#!/usr/bin/env bash
# Tarea única: dobla "Zero to Hero" mientras se descarga y al final lo mueve a ~/Vídeos.
# Ver progreso: journalctl --user -u doblar-karpathy -f
VIEJA="$HOME/Videos/Descargas"
CURSO="$VIEJA/Neural Networks： Zero to Hero"

doblar --seguir "$CURSO"

# Esperar a que no quede ninguna descarga ni doblaje en curso antes de mover.
while pgrep -f "bin/yt-dlp" >/dev/null || pgrep -f "doblar.py" >/dev/null; do sleep 30; done
V="$(xdg-user-dir VIDEOS)"
mkdir -p "$V"
if [ -d "$VIEJA" ]; then
    if [ -e "$V/Descargas" ]; then
        cp -rn "$VIEJA/." "$V/Descargas/" && rm -rf "$VIEJA"
    else
        mv "$VIEJA" "$V/"
    fi
fi
[ -f "$HOME/Videos/prueba-doblaje-3blue1brown.es.mp4" ] && mv -n "$HOME/Videos/prueba-doblaje-3blue1brown.es.mp4" "$V/"
rmdir "$HOME/Videos" 2>/dev/null && echo "✔ Carpeta ~/Videos eliminada" || { echo "⚠ ~/Videos no quedó vacía:"; ls -la "$HOME/Videos"; }
echo "✔ Todo en $V/Descargas"
notify-send -a "doblar" -i video-x-generic "🎙️ Karpathy doblado" "Zero to Hero está listo en español, en Vídeos/Descargas"
