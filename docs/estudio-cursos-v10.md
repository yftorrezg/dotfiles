# Estudio de cursos (v10, 08-09/11/2026) — cómo funciona y cómo usarlo en la laptop

**Atajos (iguales en la PC y la laptop):** SUPER+ALT+A = carpeta de un curso con videos · SUPER+ALT+Y = link de YouTube/playlist ·
SUPER+ALT+S = clase en vivo · SUPER+I = centro de estudio. La IA de los apuntes es **OpenCode Go** (`opencode-go/claude-haiku-5-5`
primero), Claude haiku solo de respaldo, **Codex apagado por defecto** (`APUNTES_CODEX=1` lo enciende).

**Un curso queda así:** temas con videos/PDF (los .srt ocultos con `.hidden`), `Apuntes/<clase>/` (rojo: apuntes.md, tarjetas.md,
transcripcion.md; resumen.md solo ≥20 min), `capturas-clave/` y `capturas-esenciales/` (amarillo), `codigo-en-imagenes/` (verde, solo si el curso
trae código/PDF), `codigo-del-curso.md`, `MAPA.md`. No hay `capturas/` ni `todas-las-capturas/`.

**Scripts (`~/.config/hypr/scripts/`)**: `arreglar-curso.sh <curso>` (todo lo siguiente, gratis y sin IA) = `normalizar-curso.py` (copias "(1)", carpetas
Tema/Tema, nombres) + `ordenar-curso.py` (capturas, basura, .srt ocultos, colores) + `rearmar-curso.py` (apuntes cortos desde el JSON guardado) +
`codigo-curso-a-imagenes.py`. `separar-curso.py <padre>` separa un padre con varios cursos. Todos aceptan `--ver` o son idempotentes.
Para REHACER con IA clases que ya tienen apuntes: `touch Apuntes/<clase>/.rehacer` y `APUNTES_MOTOR=opencode cola-capturas.sh encolar curso <ruta>`.

**mpv:** `~/.config/mpv/scripts/curso.lua` carga el curso entero en la lista al abrir un video (`>`/`<` cruzan de capítulo; Shift+H los agrupa).

## En la laptop
1. `dotsync bajar` (o espera al timer) y `bash ~/.local/share/chezmoi/laptop/verificar-estudio.sh` → dice qué falta (programas, OCR español,
   modelos de Whisper, sesión de OpenCode: `opencode auth login`, pruebas del sistema).
2. Los **cursos NO viajan por git**: se copian (USB/disco). El USB exFAT no admite enlaces simbólicos ni `? : " * < > |` en nombres, y los enlaces duros
   (capturas-clave/esenciales) se duplican. Los enlaces dentro de los apuntes son relativos: funcionan en cualquier ruta.
3. Procesar con IA (SUPER+ALT+A) funciona igual, pero la laptop es más lenta (OCR, Whisper sin la GTX 980); lo cómodo es procesar en la PC y copiar.
4. Windows 11 de la laptop: solo ver (Obsidian/mpv); lo pesado queda en CachyOS.
