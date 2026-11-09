#!/usr/bin/env bash
# verificar-estudio.sh — comprueba que ESTE equipo puede correr el flujo de estudio (SUPER+ALT+A / SUPER+ALT+Y / SUPER+ALT+S):
# programas, idioma del OCR, modelos de Whisper, sesión de OpenCode Go y las pruebas del sistema. No cambia nada.
# Uso (en la laptop):  bash ~/.local/share/chezmoi/laptop/verificar-estudio.sh
S="$HOME/.config/hypr/scripts"
ok=0; mal=0
bien() { printf "  ✔ %s\n" "$1"; ok=$((ok+1)); }
falla() { printf "  ✘ %s\n      → %s\n" "$1" "$2"; mal=$((mal+1)); }
echo "== Programas"
for par in "opencode:opencode (npm/AUR: opencode-bin)" "tesseract:sudo pacman -S tesseract tesseract-data-spa tesseract-data-eng" "ffmpeg:sudo pacman -S ffmpeg" \
           "ffprobe:sudo pacman -S ffmpeg" "yt-dlp:sudo pacman -S yt-dlp" "zenity:sudo pacman -S zenity" "notify-send:sudo pacman -S libnotify" \
           "unrar:sudo pacman -S unrar p7zip (cursos en .rar)" "7z:sudo pacman -S p7zip"; do
    c="${par%%:*}"; command -v "$c" >/dev/null && bien "$c" || falla "$c no está" "${par#*:}"
done
command -v whisper-cli >/dev/null && bien "whisper-cli" || falla "whisper-cli (sin él los videos sin subtítulos no se transcriben)" "paquete whisper.cpp con Vulkan (AUR: whisper.cpp-vulkan)"
echo "== OCR"
tesseract --list-langs 2>/dev/null | grep -qx spa && bien "tesseract español" || falla "falta el idioma spa de tesseract" "sudo pacman -S tesseract-data-spa"
echo "== Whisper (modelos; no van en git)"
for m in ggml-large-v3-turbo-q8_0.bin ggml-silero-v5.1.2.bin; do
    [ -f "$HOME/.local/share/doblar/whisper/$m" ] && bien "$m" || falla "falta ~/.local/share/doblar/whisper/$m" "cópialo de la PC (rsync/USB) — solo hace falta para videos SIN subtítulos"
done
echo "== Python"
python3 -c "import numpy, PIL" 2>/dev/null && bien "numpy + pillow" || falla "faltan numpy/pillow" "sudo pacman -S python-numpy python-pillow"
python3 -c "import gi; gi.require_version('Gtk','4.0')" 2>/dev/null && bien "GTK4 (barrita de progreso)" || falla "sin GTK4 para la barrita" "sudo pacman -S python-gobject gtk4 gtk4-layer-shell (si no, sale una notificación)"
echo "== OpenCode Go (la IA de los apuntes)"
if command -v opencode >/dev/null; then
    if opencode models 2>/dev/null | grep -qx "opencode-go/claude-haiku-5-5"; then bien "modelo opencode-go/claude-haiku-5-5 disponible"
    else falla "no aparece opencode-go/claude-haiku-5-5" "inicia sesión: opencode auth login  (plan Go) y revisa 'opencode models | grep opencode-go'"; fi
fi
echo "== Scripts y pruebas del sistema"
for f in cuadernillo.py normalizar-curso.py ordenar-curso.py arreglar-curso.sh rearmar-curso.py separar-curso.py curso-a-apuntes.sh progreso.py; do
    [ -f "$S/$f" ] && bien "$f" || falla "falta $S/$f" "dotsync bajar && chezmoi apply (el repo aún no los trajo)"
done
if [ -f "$S/pruebas-cursos.sh" ]; then
    out=$(timeout 400 bash "$S/pruebas-cursos.sh" 2>&1 | tail -1)
    [ "$out" = "TODO OK" ] && bien "pruebas-cursos.sh: TODO OK" || falla "pruebas-cursos.sh no dio TODO OK ($out)" "bash $S/pruebas-cursos.sh | tail -30"
fi
echo; echo "Resultado: $ok bien, $mal por arreglar."
[ $mal -eq 0 ]
