# Migración de la config CachyOS + Hyprland → laptops

**Origen:** PC de escritorio "yf" (laboratorio de pruebas del usuario `yafer`): CachyOS, Hyprland 0.56 con **config en Lua**, shell **Noctalia**, Intel i7-6700K + **NVIDIA GTX 980**, 2 monitores (DP-3 principal, HDMI-A-1 vertical).
**Fecha del relevamiento:** 2026-09-26 (auditoría completa el mismo día: docs 06, 07, GAPS, LIMPIEZA). **Actualizado 2026-09-28:** sistema de capturas + apuntes automáticos de cursos (doc 06 §3), bóveda Obsidian `~/Vídeos`, doc 08 (Windows 11).
**Destinos:**

| Equipo | CPU / GPU | Pantalla | Notas |
|---|---|---|---|
| Surface Pro 6 (hoy tiene Fedora) | i7 8ª gen / Intel UHD 620 | 2736x1824 táctil + lápiz | Táctil completo necesita kernel **linux-surface** (no está en repos de CachyOS, ver doc 03). Escala **2** (1.75 NO es válida) |
| ThinkPad E14 Gen4 | i7 12ª gen / Intel Iris Xe | 1920x1080 | Escala 1 o 1.25 |

Ambas: 16 GB RAM, SSD 512 GB, **sin NVIDIA**. Uso normal: **solo la pantalla interna (eDP-1)**; a veces un **monitor portátil Arzopa** (USB-C o HDMI).

---

## Para Claude en la laptop: léeme primero

1. El usuario habla **español**: responde siempre en español.
2. Esta carpeta es una **foto** de la PC, no un instalador ciego. **No hagas `cp -a dotfiles/. ~/` sin antes aplicar los ajustes de laptop** (sección "Orden de trabajo"): copiar tal cual deja variables NVIDIA activas y la Arzopa saldría **rotada 90°** (la PC tiene un monitor vertical llamado `HDMI-A-1`, que es justo el nombre que tendrá la Arzopa por HDMI).
3. El usuario prefiere que le **propongas los cambios grandes antes de implementarlos**, y atajos de **mano izquierda** (usa teclado Logitech K380 y mouse Logitech M720).
4. Instala **solo** las apps de la lista "USA" (doc 04 / `paquetes/CLASIFICACION.md`). Los duplicados (firefox, geeqie, imv, okular, alacritty, vlc) **no se instalan**; los "dudosos" se preguntan.
5. `hyprctl dispatch` usa **sintaxis Lua** en esta versión (ej. `hl.dsp.window.move({ workspace = "3" })`). No uses la sintaxis vieja.
6. En `claude-memoria/` están las memorias que Claude acumuló en la PC (decisiones del usuario). Cópialas a tu memoria (`~/.claude/projects/-home-yafer/memory/`) — la de escritorios describe los 2 monitores de la PC; actualízala al estado de la laptop cuando la adaptes.
7. La config de Hyprland también está en GitHub: `github.com/yamilfernandotorrezgarciacc-bit/hypr-config` (pero con muchos cambios sin commitear al 26-09; la versión buena es la de este paquete).

## Contenido

| Ruta | Qué es |
|---|---|
| `00-RESUMEN.md` | Resumen simple para el usuario (atajos, qué cambia, apps, pasos, pendientes) |
| `docs/01-hyprland-escritorios-monitores.md` | Hyprland: archivos, **todos los atajos**, escritorios virtuales, reglas, scripts, tema. **§4 = qué cambia en laptop** (monitores, Arzopa, escalado, touchpad, gestos) |
| `docs/02-dictado-lectura-servicios.md` | Dictado (hyprwhspr), lectura en voz alta SUPER+R (Piper / edge-tts), ydotool, servicios de usuario, rclone/Drive |
| `docs/03-teclado-mouse-entrada.md` | K380, M720 (logiops/logid), udev, Bluetooth, layout, touchpad, táctil/lápiz Surface |
| `docs/04-apps-paquetes.md` | Apps que usa, apps por defecto, fish, backups restic, mpv, **comando exacto de instalación** |
| `docs/05-sistema-base.md` | Qué elegir en el instalador (Limine, btrfs, snapper, greetd), servicios y /etc |
| `docs/06-estudio-descargar-doblar-capturas.md` | `descargar` (yt-dlp), `doblar` (Whisper → NLLB → edge-tts → ffmpeg; en laptop va por CPU), **capturas + apuntes automáticos de cursos** (SUPER+ALT+S/Y/A, cola, playlists, barrita, cuadernillo con Claude Sonnet, tarjetas, panel `Mis cursos.md`; §3.9 = adaptaciones para laptop), sesión de curso |
| `docs/07-uso-y-novedades.md` | Qué usa más el usuario, línea de tiempo 29-08→28-09, botones de los 3 Stream Deck, herramientas fuera de pacman |
| `docs/08-windows11-zenbook.md` | Portar todo a Windows 11 en la Zenbook Pro Duo 15 OLED UX582: qué se puede, cómo y qué conviene |
| `docs/GAPS.md` | Lo que existía y no cubrían los docs 01-05, con prioridad (incluye riesgos de datos) |
| `docs/LIMPIEZA.md` | Qué se sacó del paquete y por qué (verificado) |
| `guias-usuario/` | Guías markdown del propio usuario (de `~/Documentos`): Stream Deck + `portabilidad-laptops.md`, Maono, M720, móvil, aprender, **`Guia-Auto-captura-de-cursos.md`** (capturas y apuntes, 28-09). **Leer `guias-usuario/StreamDeck/docs/portabilidad-laptops.md`** |
| `INICIO.md` + `.obsidian/` | Índice para abrir la carpeta como bóveda de Obsidian |
| `paquetes/` | Listas crudas `pacman -Qqen`/`-Qqem` y `CLASIFICACION.md` (NVIDIA / base / USA / DUPLICADO / DUDOSO) |
| `dotfiles/` | Configs de `$HOME`, misma ruta relativa (`dotfiles/.config/hypr/...` → `~/.config/hypr/...`; `dotfiles/Vídeos/.obsidian/` → `~/Vídeos/.obsidian/`, config de la bóveda de apuntes) |
| `system/etc/` | Configs de `/etc` (logid.cfg, greetd, udev, bluetooth, modprobe...) |
| `solo-esta-pc/` | Cosas **exclusivas de la PC** que NO van a la laptop (diagnóstico de "teclas fantasma" que ignora el botón de encendido, servicio sin uso). Solo referencia |
| `claude-memoria/` | Memorias de Claude de la PC |

**Secretos NO incluidos** (a propósito): `rclone.conf` (token de Drive → `rclone config`, el usuario usa su propio client_id/secret), contraseña de restic (`~/.config/restic/home-backup.pass`), `gh` (`gh auth login`), perfiles de navegador, llaveros. Pedírselos al usuario.

## Orden de trabajo sugerido en la laptop

1. **Instalar CachyOS** con edición Hyprland (Noctalia), Limine, btrfs — doc 05. En la Surface, decidir antes si se instala linux-surface (doc 03).
2. **Paquetes**: driver Intel (`intel-media-driver vulkan-intel`) + apps "USA" — comando en doc 04 §6. Nada `nvidia*`.
3. **Copiar dotfiles a una carpeta temporal y ajustar ANTES de copiar a `~`** (doc 01 §4.6):
   - `hypr/config/environment.lua`: comentar las 4 variables NVIDIA (líneas 8-11).
   - `hypr/config/nwg-monitors.conf` (el que rotaría la Arzopa) **ya no viene en `dotfiles/`**: está en `solo-esta-pc/` como referencia. Si aparece en la laptop, bórralo.
   - `hypr/config/variables.lua`: `MONITOR1 = "eDP-1"`.
   - `hypr/config/monitors.lua`: escala (Surface 2, ThinkPad 1–1.25).
   - `hypr/config/autostart.lua`: quitar `powerprofilesctl set balanced`.
   - `hypr/config/inputs.lua`: bloque touchpad (tap, natural scroll) — y **revisar el gesto 3 dedos abajo = cerrar ventana**, se dispara fácil en touchpad.
   - `noctalia/config.toml`: quitar brillo ddcutil de HDMI-A-1, `gpu_temp` → CPU, agregar widget **battery**.
   - `brave-flags.conf`: quitar `VaapiOnNvidiaGPUs`.
   - `hyprwhspr/config.json`: `audio_device_name: "Maono"` es el micrófono USB de la PC → usar el mic interno.
   - `restic/home-excludes.txt`: agregar `GoogleDrive` (ver "Problemas conocidos").
   - `hypr/scripts/carpeta-capturas.conf` → `~/Imágenes/Capturas`; barrita de progreso de los apuntes: sin monitor vertical usa el enfocado, o fijarla con `PROGRESO_MONITOR=eDP-1` en `uwsm/env` (doc 06 §3.9). Si el usuario no es `yafer`, corregir `/home/yafer` en `abrir-markdown.desktop` y `obsidian/obsidian.json`.
4. Copiar a `~`, `/etc` (con sudo, solo lo indicado en los docs), `systemctl --user daemon-reload`, habilitar servicios (docs 02/03).
5. Implementar la **lógica de monitores dinámica** (doc 01 §4.2): con solo eDP-1, los ws 6-10 viven en la interna y se accede con un atajo de "voltear"; con Arzopa, se comporta como la PC. **Proponérsela al usuario antes.**
6. Probar: SUPER+1..5 con y sin Arzopa, SUPER+R (lectura), dictado, botones del M720, mpv con `vainfo` / hwdec.

## Decisiones pendientes del usuario (preguntar)

- ~~Choque de atajos del dictado~~ **resuelto 26-09:** dictado = SUPER+ALT+Z (es) / SUPER+ALT+X (en) en `hyprwhspr/config.json`; Drive/Instagram siguen en SUPER+ALT+D/I.
- **Layout de teclado:** Hyprland no define `kb_layout` (usa `us`), aunque la consola está en `es`. Preguntar la distribución física del teclado de la ThinkPad y del Type Cover.
- Apps "dudosas" (gimp, kdenlive, xournalpp —útil para el lápiz de la Surface—, opendeck/Stream Deck, docker, android-studio...).
- En la Surface: ¿kernel linux-surface para táctil/lápiz completos?
- Modelo de dictado: `small` en la ThinkPad; en la Surface quizá `base` si va lento.

- Extensiones de VS Code: **resuelto**, se restauran con Settings Sync al iniciar sesión con GitHub (la lista queda en `paquetes/vscode-extensions.txt` solo como referencia).
- CTRL+SHIFT+D se queda como está (el usuario no usa ese atajo en VS Code ni en Brave).

## Problemas conocidos en la PC (no replicar)

- **DATOS EN RIESGO:** `~/Proyectos/Ciego` (tesis) es un git **sin remoto**. Antes de reinstalar nada, confirmar que el usuario la subió a GitHub (repo privado). Detalle en `docs/GAPS.md`.
- `carpeta-capturas.conf` apunta a un disco externo; en la laptop poner ruta local.
- `doblar` borra el video original por defecto (`BORRAR_ORIGINAL=1`).

- **Backup restic**: arreglado el 26-09 (exclusión de `/home/yafer/GoogleDrive` en `home-excludes.txt` + `restic unlock`). En la laptop copiar el `home-excludes.txt` nuevo.
- `scripts/curso-abrir.sh:28` usa `hyprctl dispatch workspace name:estudio` (sintaxis vieja, pre-Lua): probablemente SUPER+C no cambia de workspace.
- Restos: `xremap` corre con config vacía; reglas de Steam sin Steam; carpetas de navegadores desinstalados.

## Cambios recientes (26-09-2026)

- mpv: **Ctrl+←/→ = ±10 s**, **Alt+←/→ = ±30 s**, Shift+←/→ desactivado (←/→ siguen en ±5 s). Guía del usuario en `~/.config/mpv/GUIA-MPV.md`.
- mpv.conf: se entrecomilló `screenshot-template` (mpv daba un aviso de sintaxis).
- Hyprland (tarde del 26-09): **SUPER+ALT+S = auto-captura de cursos** (`scripts/auto-captura-toggle.sh` + `auto-captura.py`, ajustes en `auto-captura.conf`) y `scripts/video-a-capturas.sh`. Requiere `python-numpy python-pillow yt-dlp ffmpeg` (doc 01 §3.3).

## Cambios recientes (27/28-09-2026)

- **Capturas + apuntes automáticos de cursos** rehecho (doc 06 §3, guía `guias-usuario/Guia-Auto-captura-de-cursos.md`): **SUPER+ALT+Y** (link de YouTube copiado, video o playlist entera), **SUPER+ALT+A** (curso descargado entero), SUPER+ALT+S (en vivo). Cola de un pedido por vez, barrita de progreso GTK4 layer-shell (busca el monitor `HDMI-A-1`; en laptop ver doc 06 §3.9), capturas WebP sin pérdida `0001.webp` + `.minutos.tsv`, `apuntes.md` + `resumen.md` en una sola llamada a **Claude Sonnet** (`APUNTES_MODELO`), `tarjetas.md` (plugin Spaced Repetition), panel `~/Vídeos/Mis cursos.md`. ~10,5 min por hora de video. Nuevas dependencias: `python-gobject gtk4-layer-shell tesseract tesseract-data-spa obsidian` y **Claude Code con sesión iniciada**.
- `.md` por defecto → `abrir-markdown.desktop` (Obsidian si está en una bóveda, si no VS Code). `~/Vídeos` es bóveda de Obsidian: copiar `dotfiles/Vídeos/.obsidian/` y `dotfiles/.config/obsidian/obsidian.json` con Obsidian cerrado.
- `doblar.py` actualizado (caché por nombre+tamaño, alcance ×1,45, no corta la carpeta ante un error). `voz.conf`: lectura SUPER+R a ×1.2.
- Noctalia: plantilla Qt oscura propia (`noctalia/templates/qtct-oscuro.conf`, reemplaza a la `qt` integrada en `config.toml`); `dolphinrc` con vista previa compacta.
