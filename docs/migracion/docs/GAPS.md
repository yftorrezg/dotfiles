---
title: GAPS — lo que existe en la PC y no cubren los docs 01-05
fecha: 2026-09-26
actualizado: 2026-09-28
tags: [sistema, auditoria]
---

# GAPS: lo que existe en la PC y no está en los docs 01-05

Relevado el 26-09-2026 (auditoría de solo lectura). Detalle y contexto en [[07-uso-y-novedades]].
Prioridad para migrar: **alta** = sin esto la laptop pierde algo que usa o hay riesgo de perder datos; **media** = lo usa a veces o pronto; **baja** = opcional o resto.

"Copiado" = ya está en `~/migracion-cachyos/` (lo copió esta auditoría).

## 1. Datos y riesgos (no son config, pero importan)

| Qué | Dónde vive | Prioridad | Nota |
|---|---|---|---|
| **Tesis Lazarillo sin remoto git** | `~/Proyectos/Ciego` (git local, último commit 11-09) | **alta** | Solo existe aquí y en restic, que está roto (doc 04). Crear un repo privado y hacer `git push` **antes** de migrar. La rama `worktree-agent-aaff555bbd087c837` tiene trabajo sin verificar |
| Guías markdown del usuario (varias pensadas "para la laptop") | `~/Documentos/{aprender,StreamDeck,maono,mouse_M720TriathlonLogitech,movil,lectura,claude_curso}` | **alta** | No están en Drive ni en git. Copiarlas como datos (o subirlas a Drive). Incluyen `atajosTeclado.md`, `StreamDeck/docs/portabilidad-laptops.md`, `maono/CLAUDE.md` |
| Proyectos sin git | `~/Proyectos/anghy21` (+ `mundoanimal`, vacío) | media | Copiar como datos |
| Datos del parcial de Robótica | `~/.local/share/parcial1/` (SQLite + mosquitto_data, 460 KB) | baja | Solo si se retoma |
| Vault de Obsidian | `~/Documentos/Obsidian Vault` (3 notas, 80 KB) | baja | Casi no lo usa |
| Apuntes de cursos (capturas, `apuntes.md`, `resumen.md`, `tarjetas.md`, `Mis cursos.md`, progreso de repaso en los `<!--SR:`) | `~/Vídeos/**`, `<curso>/capturas/` | media | **Datos**, no van en el paquete. Si se quieren en la laptop, copiarlos aparte (disco o Drive); se pueden regenerar desde los videos, pero se pierden las casillas tildadas y el progreso de las tarjetas |

## 2. Configuración no documentada

| Qué | Dónde vive | Prioridad | Estado |
|---|---|---|---|
| **gnome-keyring se desbloquea al iniciar sesión** (`pam_gnome_keyring.so` en auth + session, agregado el 26-09 porque al arrancar le pedía la contraseña del llavero) | `/etc/pam.d/greetd` (backup `greetd.bak`) | **alta** | Copiado → `system/etc/pam.d/greetd`. En la laptop: `sudo cp` después de instalar greetd. Si la contraseña de sesión y la del llavero no coinciden, igual la pide una vez |
| Scripts y atajo de la auto-captura, `descargar`, `doblar`, `whisper-cpp`/`ggml-vulkan`, `yt-dlp`, `aria2`, `python-curl_cffi` (paquetes instalados el 26-09 que no están en `paquetes/*.txt`) | `hypr/scripts/auto-captura*`, `video-a-capturas.sh`, `~/.local/bin/{descargar,doblar}`, `~/.local/share/doblar/` | **alta** | **Cubierto** en doc 06 (copiados a `dotfiles/`; actualizado el 28-09 con todo el sistema de apuntes) |
| `carpeta-capturas.conf` apunta al disco externo SuperYafer; `captura-guardar.sh` falla si no está montado (no cae a `~/Imágenes/Capturas`) | `~/.config/hypr/scripts/carpeta-capturas.conf` | **alta** | En la laptop: poner una ruta local (o agregar el fallback al script) |
| Git: nombre, email, `gh` como credential helper, rama `main` | `~/.gitconfig` | **alta** | Copiado → `dotfiles/.gitconfig` (necesita `gh auth login`) |
| npm con prefijo en `~/.local` (instalar global sin sudo) | `~/.npmrc` | media | Copiado → `dotfiles/.npmrc` |
| Extensiones de VS Code (95) | `~/.vscode/extensions` | **alta** | Lista copiada → `paquetes/vscode-extensions.txt`. Doc 04 solo copia `settings.json`. Preguntarle si quiere todas (hay muchas de PHP/Java/C#) o usar la sincronización de VS Code (`Code/User/sync` existe) |
| Snippets de VS Code | `~/.config/Code/User/snippets/{html,markdown}.json` | media | Copiado |
| Claude Code: MCP **vercel** (alcance usuario) | `~/.claude.json` → `mcpServers.vercel` | media | `claude mcp add --transport http vercel https://mcp.vercel.com` + `/mcp` login |
| Claude Code: marketplace `claude-plugins-official`, `settings.local.json` (4 permisos de lectura) | `~/.claude/plugins/`, `~/.claude/settings.local.json` | baja | Rehacer con `/plugin` si hace falta |
| Memorias de Claude de otros proyectos (StreamDeck, Ciego) | `~/.claude/projects/-home-yafer-Documentos-StreamDeck/memory/`, `…-Proyectos-Ciego/memory/` | media | Copiadas → `claude-memoria/proyectos/`. En la laptop van en `~/.claude/projects/<ruta-con-guiones>/memory/` (la carpeta depende de la ruta del proyecto) |
| Planes de Claude (arquitectura de la tesis: `que-opinas-sobre-este-wobbly-elephant.md`, etc.) | `~/.claude/plans/*.md` (10) | media | El `CLAUDE.md` de Ciego apunta a uno. Copiar junto con el proyecto |
| Repo git de Noctalia (`noctalia-config`, 2 cambios sin commit) | `~/.config/noctalia/.git` | baja | Doc 01 solo menciona el de hypr |
| Esquema de colores KDE generado por Noctalia (Dolphin/Qt) | `~/.local/share/color-schemes/noctalia.colors` | baja | Copiado (Noctalia lo regenera) |
| Tema oscuro de GTK por gsettings (`color-scheme prefer-dark`, 29-08) | dconf (binario) | baja | En la laptop: `gsettings set org.gnome.desktop.interface color-scheme 'prefer-dark'` (Noctalia suele ponerlo) |
| Backup de la transparencia anterior de Noctalia | `~/.config/backup-transparencia-2026-09-25/` | baja | Resto, no migrar |

## 3. Herramientas y desarrollo

| Qué | Dónde vive | Prioridad | Estado |
|---|---|---|---|
| **Android Studio + SDK** (tesis Android, adb con Samsung SM-S928B) | `android-studio` (AUR), `~/Android/Sdk` (1,7 GB), `~/.android`, `~/.gradle` | **alta** si la tesis sigue en la laptop | Doc 04 lo marca "dudoso"; en realidad lo necesita la tesis. Reinstalar con `paru -S android-studio` y dejar que baje el SDK |
| **arduino-cli** + núcleo ESP32 3.3.11 + librerías | `~/.local/bin/arduino-cli`, `~/.arduino15/`, `~/Arduino/libraries/` | **alta** (Robótica 2, va a defender con la laptop) | Config copiada → `dotfiles/.arduino15/arduino-cli.yaml`, libs → `paquetes/arduino-libraries.txt`. Comandos en doc 07 §d. Grupo `uucp` (ya en doc 05) |
| mosquitto + reglas ufw 1883/tcp y 8080/tcp | paquete `mosquitto`, ufw | media | Solo para Robótica. `sudo ufw allow 1883/tcp && sudo ufw allow 8080/tcp` |
| venv del parcial (Flask, paho-mqtt, OpenCV) | `~/.venvs/parcial1` | baja | Recrear si hace falta (doc 07 §d) |
| opencode: plugin `opencode-slim-mcp` + MCP playwright/context7 | `~/.config/opencode/opencode.jsonc` | baja | Copiado. Solo si lo instala |
| antigravity-cli (`agy`) | `~/.gemini/antigravity-cli` | baja | Dudoso |
| Ultralytics (YOLO) settings | `~/.config/Ultralytics/` | baja | Caché; no migrar |
| GitKraken CLI | `~/.local/share/GitKrakenCLI/` | baja | La instala GitLens sola |

## 4. Periféricos

| Qué | Dónde vive | Prioridad | Nota |
|---|---|---|---|
| Tabla de botones de los 3 Stream Deck | `~/.config/opendeck/profiles/` | media | Perfiles copiados; ahora documentados en doc 07 §c. En la laptop los botones "monitor 2" no hacen nada con una pantalla |
| Restaurar iPhone (`idevicerestore-git`, `usbmuxd`, `70-apple-restore.rules`) y guía IMEI | `~/Documentos/movil/` | baja | Doc 03 lo llama "resto", pero es su **trabajo de reparación de celulares**: preguntarle si lo quiere en la laptop |
| Maono DM40: el nombre del dispositivo sirve igual en la laptop si lleva el receptor USB | `hyprwhspr/config.json` | media | Los docs dicen "cambiar al mic interno"; mejor: dejar `"Maono"` (hyprwhspr cae al mic por defecto si no está) |
| Handy / hyprvoice como plan B del dictado | `~/Documentos/maono/CLAUDE.md` | baja | Solo referencia |

## 5. Hallazgos raros / deuda (en la PC)

| Qué | Dónde | Prioridad | Nota |
|---|---|---|---|
| **Claude Code duplicado**: `/usr/bin/claude` → `/usr/lib/node_modules/@anthropic-ai/claude-code` (2.1.251, instalado con `sudo npm` el 29-08, sin paquete dueño), tapado por `~/.local/bin/claude` (2.1.283) | `/usr/lib/node_modules/` | baja (limpieza en la PC) | `sudo npm uninstall -g @anthropic-ai/claude-code`. En la laptop usar solo el instalador oficial |
| **CTRL+SHIFT+D sigue siendo "elegir carpeta de capturas"**, aunque el 25-09 se le dijo que se había movido a SUPER+ALT+S por chocar con VS Code (panel Debug) y Brave. Hoy SUPER+ALT+S es la auto-captura. CTRL+SHIFT+S (guardar captura) también le quita "Guardar como" a las apps | `binds.lua:134-138` | media | Preguntar al usuario. Se suma al choque de SUPER+ALT+D/I (README) |
| Etiqueta equivocada en el Stream Deck XL: "MDN" abre un video de React en YouTube | perfil `sd-…/Default.json` tecla 20 | baja | — |
| 26-09 01:01 "OpenDeck no reconoce mi Stream Deck XL": no consta que se resolviera | — | baja | Probar en la laptop |
| Enlace roto `~/.local/bin/python3.11` → `/tmp/uv-python/…` | `~/.local/bin` | baja | No copiar |
| Carpetas duplicadas `~/Videos` (con `Descargas/` y una prueba de doblaje) y `~/Vídeos` (vacía, la de XDG) | `~` | baja | Lo trata el documento de descargar/doblar |
| Sesión con zsh/bash sin uso (`.zshrc` de CachyOS, `.zsh_history` vacío) | `~` | baja | La shell es fish |
| Restos de apps que ya no están: `.config/{chromium,google-chrome*,microsoft-edge,opera,vivaldi,Code - OSS,geeqie}`, `.vscode-oss*` | `~/.config`, `~` | baja | No migrar (doc 04 ya lo dice para navegadores) |
| Muchos `.bak` de `binds.lua` y perfiles de OpenDeck | `hypr/config/backups/`, `opendeck/profiles/*/*.bak-*` | baja | No migrar |

## Archivos que agregó esta auditoría al paquete

- `dotfiles/.gitconfig`, `dotfiles/.npmrc`
- `dotfiles/.config/Code/User/snippets/{html,markdown}.json`
- `dotfiles/.config/opencode/{opencode.jsonc,package.json}`
- `dotfiles/.arduino15/arduino-cli.yaml`
- `dotfiles/.local/share/color-schemes/noctalia.colors`
- `system/etc/pam.d/greetd`
- `paquetes/vscode-extensions.txt`, `paquetes/arduino-libraries.txt`
- `claude-memoria/{auto-captura-cursos,migracion-laptops,quiere-aprender-no-solo-soluciones}.md`, `claude-memoria/proyectos/{Documentos-StreamDeck,Proyectos-Ciego}/`

## Actualización 28-09 (sistema de capturas + apuntes)

Cubierto ahora: scripts nuevos y modificados de `hypr/scripts/`, `binds.lua` (SUPER+ALT+Y/A), `abrir-markdown.desktop`, `mimeapps.list`, `obsidian.json`, `~/Vídeos/.obsidian/` (con plugin Spaced Repetition), `doblar.py`, `voz.conf`, `noctalia/config.toml` + `templates/qtct-oscuro.conf`, `qt6ct/colors/noctalia.conf`, `dolphinrc`, guía `guias-usuario/Guia-Auto-captura-de-cursos.md`, memorias de Claude. Doc 06 §3 reescrito.

Gaps nuevos:

| Qué | Dónde | Prioridad | Nota |
|---|---|---|---|
| Barrita de progreso fija en `HDMI-A-1` (monitor vertical de la PC) | `progreso.py` (`PROGRESO_MONITOR`) | media | En la laptop cae al monitor enfocado; con la Arzopa por HDMI iría a la Arzopa. Decidir con el usuario (doc 06 §3.9) |
| `python-numpy`, `python-pillow`, **`python-gobject`** solo como dependencias en la PC | pacman | **alta** | Instalarlas explícitamente en la laptop (doc 06 §3.10); si no, capturas/barrita no arrancan |
| OCR solo con `tesseract-data-spa` (sin inglés) | pacman | baja | El código está en inglés: agregar `tesseract-data-eng` en la laptop (no probado en la PC) |
| Apuntes dependen de **Claude Code logueado** y de la cuota del plan | `cuadernillo.py` | **alta** | Sin sesión, los apuntes salen "sin resumen de IA". Playlists largas pueden agotar la cuota |
| Rutas `/home/yafer` fijas | `abrir-markdown.desktop`, `obsidian.json` | baja | Solo importa si el usuario de la laptop no se llama `yafer` |
| Tema Qt oscuro propio de Noctalia y vista previa compacta de Dolphin | `noctalia/templates/qtct-oscuro.conf`, `dolphinrc` | baja | Copiados, pero no explicados en doc 01/04 |
| Estado de OpenDeck (`settings.json` brillo, `current_state` de una tecla del XL) cambiado el 28-09 | `~/.config/opendeck/` | baja | Es estado de ejecución: **no** se recopió |

### Actualización 28-09 (noche): cookies de YouTube
- `dotfiles/.config/yt-dlp/config` = `--cookies-from-browser brave+gnomekeyring`: yt-dlp usa la sesión de YouTube de Brave (menos bloqueos "no sos un robot" en playlists). **En la laptop:** instalar `python-secretstorage`, iniciar sesión en YouTube en Brave y verificar con `yt-dlp -v --simulate <link>` que diga "Extracted N cookies" sin "could not be decrypted" ni "no longer valid". Con otro navegador, cambiar `brave` por `firefox`/`chromium`. En Windows (doc 08): las cookies de navegadores Chromium usan cifrado "app-bound" → usar Firefox o exportar `cookies.txt`.
