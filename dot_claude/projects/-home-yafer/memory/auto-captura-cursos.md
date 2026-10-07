---
name: auto-captura-cursos
description: "Sistema de capturas + cuadernillo de apuntes automáticos de cursos (SUPER+ALT+S/Y/A), algoritmos, trade-offs y dónde está la guía"
metadata:
  node_type: memory
  type: project
  originSessionId: be8fa871-184d-403c-978d-e9d1843bd89f
  modified: 2026-09-27T04:19:34.430Z
---

Scripts en `~/.config/hypr/scripts/`:
- `auto-captura.py`: guarda una captura solo cuando la pantalla cambia.
- `cuadernillo.py`: arma `apuntes.md` con Claude y el `INDICE.md` del curso.
- `resumen-corto.py`: segunda versión corta (`resumen.md`: chuleta, código mínimo, autoevaluación) a partir de `.apuntes-ia.json`; `--todos` para cursos ya hechos. El usuario pidió que se AGREGUE sin tocar `apuntes.md`.
- `curso-a-apuntes.sh`: procesa un curso entero; tiene lock, se puede reanudar, usa nice y prefiere el `.es.mp4` doblado.
- `video-a-capturas.sh`, `youtube-capturas.sh`, `curso-apuntes-elegir.sh`, `progreso.py` (barrita de progreso en una notificación que se actualiza sola; noctalia no dibuja la barra gráfica, por eso se usan caracteres ▰▱). Para cambiar un `.sh` mientras corre, escribirlo aparte y hacer `mv`.

Nombres cortos `0001.webp` (pedido del usuario 28/09/2026); el minuto va en `.minutos.tsv` (`0001.webp<TAB>01-23-45`), que escribe `Guardador` y lee `cuadernillo.listar_capturas` (también entiende nombres viejos `0012_01-23-45`). `capturas-nombre-corto.py` renombra las viejas. Ojo: esperar procesos con `pgrep -f nombre.py` desde un bash cuyo comando contiene ese texto se encuentra a sí mismo y no termina nunca; esperar por PID.

Capturas en WebP sin pérdida (`lossless=True, method=1, quality=50`, ~57 % del PNG, píxeles idénticos); cuadernillo acepta .webp y .png; `capturas-a-webp.py` convierte las viejas (verifica píxeles, corrige links, saltea carpetas sin `.cantidad`). El usuario lo eligió (28/09/2026) por espacio sin perder calidad; con pérdida no, por el OCR.

yt-dlp usa `-f "bv*[height<=1080]" -S "proto,vcodec:h264"`: sin `-S` elegía el HLS m3u8 (6 GB en vez de 335 MB, misma resolución). La descarga ocupa el tramo 0-25 % de la barrita.

Atajos: SUPER+ALT+S (en vivo), SUPER+ALT+Y (link de YouTube copiado; con `list=` pregunta con zenity si procesar la playlist entera), SUPER+ALT+A (elegir la carpeta de un curso con zenity). Y y A pasan por `cola-capturas.sh` (un pedido por vez, sin duplicados; `estado`/`vaciar`/`cancelar`, archivos en `~/.cache/auto-captura/cola*`).

Agregado el 28/09/2026 (a pedido del usuario, hecho con 3 agentes en paralelo):
- `playlist-a-apuntes.sh`: playlist → `Capturas de YouTube/<playlist>/capturas/NNN - título/` con `.youtube-id` (se puede retomar), `MAX_VIDEOS`, espera ante el anti-bot de YouTube. Los videos sueltos también guardan `.youtube-id`: si hay dos títulos iguales, el segundo va a `<título> [id]`.
- `progreso.py seguir`: barrita layer-shell GTK4 (se relanza con LD_PRELOAD de libgtk4-layer-shell) de 420x26 abajo a la derecha de HDMI-A-1 (el monitor vertical); sin foco y los clics pasan. Una sola notificación al final. `PROGRESO_MODO=notificacion` / `PROGRESO_MONITOR`.
- `tarjetas.py`: `tarjetas.md` (plugin Spaced Repetition 1.15.4 instalado en la bóveda Vídeos; conserva los `<!--SR:` al regenerar) + `tarjetas-anki.txt`. No llama a Claude.
- `panel-cursos.py` → `~/Vídeos/Mis cursos.md` (conserva las casillas por ruta de clase y la sección "📝 Mis notas").
- Cuota: si Claude responde "hit your session limit", `cuadernillo.llamar_claude` espera 10 min y reintenta (hasta `APUNTES_ESPERA_MAX_H`=6). `rehacer-sin-ia.py` rehace las clases con apuntes.md sin `.apuntes-ia.json` (sin el video: usa los subtítulos de la carpeta + OCR); corre solo al final de las playlists y cursos. `.sin-ia` marca las hechas con SIN_IA=1 a propósito. Pasó el 28/09: 4 videos de JS quedaron sin IA por el límite.
- Cookies de YouTube (28/09, con permiso del usuario): `~/.config/yt-dlp/config` = `--cookies-from-browser brave+gnomekeyring` (sesión iniciada en Brave, perfil Default). Sin `+gnomekeyring` yt-dlp elige BASICTEXT en Hyprland, no descifra las cookies v11 y YouTube dice "cookies no longer valid". Necesita el paquete `python-secretstorage` (instalado).
- Centro de estudio (29/09, pedido del usuario: "el cuello de botella soy yo", quiere un flujo fácil de usar): `estudiar.py` es una ventana GTK4 (app_id `estudiar.centro`, regla flotante 760x760 en windowrules.lua; `SUPER+ALT+Z`) con pre-test de 3 preguntas (3/3 → marcar sabida `[s]`), idea+mapa, V/R/A/P/T y Ctrl+Enter para terminar. CLI: `--siguiente --terminar --tests --repasar --estado`; `SUPER+ALT+V` = `--tests`. El estado está en `Mis cursos.md` (`[x]` hecha, `[s]` sabida; `panel-cursos.py --marcar`, con flock) y en `~/.local/state/estudiar/estado.json`. `practica.py <clase>` genera `practica/` (3-5 ejercicios JS con node:test o Python con unittest, con los tests verificados contra la solución y el arranque; 1 llamada a Claude, solo al pedirla); `--correr [--notificar]` escribe `practica/.resultado.json`. Stream Deck: Mirabox, perfil "Cursos y Dev", teclas 6-9 (Estudiar/Tests/Terminé/Repasar, íconos `custom-icons/estudio-*.png`); para editar el JSON hay que cerrar OpenDeck antes.
- Medido: ~10,5 min por hora de video con IA; un video de 23 min tardó 2,5 min.

Pruebas (correrlas después de cualquier cambio): `auto-captura-tests.py` (10), `auto-captura-estres.py` (N=200 → 0 perdidos), `cuadernillo-tests.py` (8), `resumen-corto-tests.py` (4), `tarjetas-panel-tests.py` (11), `cola-capturas-tests.sh`, `playlist-a-apuntes-tests.sh`.

Guía para el usuario: `~/Documentos/Guia-Auto-captura-de-cursos.md` y el Google Doc "📸 Guía: Capturas y apuntes automáticos de cursos" (id 11XciglHYI0cjOH_APONc6GIedNLiq8igHoDipkynrcs). Para actualizarla SIN gastar tokens: mandar el doc viejo a la papelera y subir con `rclone copyto ~/Documentos/Guia-Auto-captura-de-cursos.md "gdrive:📸 Guía: Capturas y apuntes automáticos de cursos.md" --drive-import-formats md --drive-export-formats md` (crea un Google Doc de verdad; sin `--drive-export-formats md` falla). El paquete de migración se sube también con rclone. `read_file_content` muestra los emojis rotos; verificar con `download_file_content`.

Qué hace el cuadernillo:
- A Claude le pasa los subtítulos del idioma ORIGINAL (`subs_para_claude`: `-orig` o `.idioma`; si no se sabe, inglés, como en los videos doblados de Karpathy). La traducción automática confunde términos ("xp" en vez de exp). `video-a-capturas.sh` anota el idioma (`--print-to-file %(language)s .idioma`) y pide solo esos subtítulos (es → `es,es-orig`; en → `en,en-orig,es`; NA → `es-orig,en-orig,es`). Antes del 29/09 se bajaba la traducción al inglés de los cursos en español: 27 de las primeras 38 clases del curso de JS se armaron desde esa traducción (se pueden rehacer con `cuadernillo.py --forzar`).
- Para leer muestra los subtítulos en español y la transcripción queda plegada.
- Lee el código de la pantalla con OCR (tesseract, solo está instalado el idioma spa) cada ~4 min, así el código de los apuntes es el real.
- Llama a `claude -p --tools "" --strict-mcp-config --system-prompt --model sonnet` (variable `APUNTES_MODELO`, por defecto sonnet: el usuario lo eligió el 28/09/2026 para ahorrar cuota; `opus` o `""` para un curso difícil). UNA sola llamada por video: el JSON trae `corto` (el repaso), que cuadernillo guarda como `.resumen-ia.json` + `resumen.md`; `resumen-corto.py` queda solo para clases viejas. El costo depende de las horas de video, no de la cantidad de videos.
- Sin subtítulos, arma los apuntes solo con el OCR. Lo que agrega Claude por su cuenta queda marcado "(extra)".

Cómo elige las capturas: una captura queda "superada" solo si la siguiente la contiene y agrega bastante más (la comparación es asimétrica). Webcam = mancha compacta de 10 o más bloques que cambia aunque el resto de la pantalla esté quieto; si no se exige eso, las diapositivas se confunden con webcam.

El usuario estudia sobre todo cursos de programación: cada variable, parámetro o línea importa, y prefiere capturas de más antes que perder un estado del código. Quiere apuntes "completos pero con lo importante", para estudiar rápido.
Curso de Karpathy en `~/Vídeos/Descargas/Neural Networks： Zero to Hero/` (la carpeta se movió desde ~/Videos). Otra sesión del usuario dobla esos videos a `.es.mp4`.

**Why:** los apuntes del usuario se basan en capturas; quiere concentrarse en el video y practicar ([[quiere-aprender-no-solo-soluciones]]).
**How to apply:** si reporta problemas, reproducir con `video-a-capturas.sh`/`cuadernillo.py --forzar` y agregar el caso a las pruebas; si cambia el sistema, actualizar la guía (.md y Drive). No editar un `.sh` mientras un curso se está procesando: bash lee el script a medida que lo ejecuta.

Markdown por defecto (28/09/2026, lo pidió el usuario): `abrir-markdown.desktop` → `abrir-markdown.py` abre con `obsidian://open?path=` si el .md está en una bóveda de `~/.config/obsidian/obsidian.json`, y si no con VS Code. `~/Vídeos` está registrada como bóveda "Vídeos". Obsidian lee la lista de bóvedas solo al arrancar: para registrar una, cerrarlo antes (`pgrep -f obsidian/app.asar`; `pgrep -x obsidian` no lo encuentra). `xdg-open` adivina el tipo por el contenido (un .md con código → text/javascript → navegador); Dolphin usa la extensión.
