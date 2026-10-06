---
title: 07 — Uso real y novedades no documentadas
fecha: 2026-09-26
actualizado: 2026-09-28
equipo: PC "yf" (CachyOS + Hyprland, laboratorio)
tags: [sistema, auditoria]
---

# 07 — Qué usa más el usuario y qué hay nuevo

Auditoría de solo lectura hecha el 26-09-2026. Fuentes: historial de fish (177 comandos), `~/.claude/history.jsonl` (583 prompts entre el 29-08 y el 26-09), memorias de Claude, `~/.local/state/noctalia/usage_counts.json` (contador del lanzador), archivos modificados en los últimos 45 días, perfiles de OpenDeck y `~/Documentos/*`.

> **Ojo:** otro documento de esta auditoría cubre **`descargar`, `doblar` y las capturas de estudio** (`auto-captura.py`, `video-a-capturas.sh`, SUPER+ALT+S). Aquí solo se mencionan.

Lo que falta en los docs 01-05 está en **[[GAPS]]** (`docs/GAPS.md`).

---

## (a) Ranking de uso (con evidencia)

### Cómo trabaja el usuario

- **Casi todo lo hace a través de Claude Code**, no desde la terminal: fish tiene solo 177 comandos en un mes (73 son `sudo …` que Claude le pasó para pegar, 15 `paru`, 15 `claude`), mientras que Claude tiene **583 prompts**. En la laptop lo primero que tiene que funcionar es **Claude Code + el dictado** (le dicta a Claude con el Maono).
- Días con más actividad: 30-08 (99 prompts), 02-09 (77), 31-08 (50), 03-09 (42), 10-09 (41), 26-09 (39).
- Prompts por carpeta: `~` 333, `Documentos/StreamDeck` 63, `Proyectos/Ciego` 43, `Documentos/claude_curso` 40, `Documentos/lectura` 32, `Documentos/aprender` 26, `Proyectos/anghy21` 12, `GoogleDrive/*` 23, `Documentos/maono` 11.

### Temas más pedidos a Claude (prompts que los mencionan)

| # | Tema | Prompts | Comentario |
|---|---|---|---|
| 1 | Escritorios / monitores / workspaces | 53 | 2 monitores (uno vertical), 5 escritorios que cambian los dos a la vez, que las apps se abran en el escritorio actual, restaurar ventanas |
| 2 | Mouse M720 / teclado K380 | 47 | logiops (pulgar = captura, rueda inclinada = pestañas); se "pierde" tras reiniciar → regla udev el 26-09 |
| 3 | Stream Deck / OpenDeck (3 aparatos) | 41 | Stream Deck XL + Mirabox HSV293S + Fifine D6 |
| 4 | Video: mpv, descargar, doblar | 39 | Casi todo el 25 y el 26-09 (mpv de estudio, yt-dlp, doblaje) |
| 5 | Cursos / estudio | 37 | Udemy, YouTube, universidad (Robótica 2, Base de Datos 3, Taller) |
| 6 | Tema, fondos, colores Noctalia | 33 | Probó paletas y **siempre volvió al tema por defecto de Noctalia**; solo cambió el fondo |
| 7 | VS Code / markdown | 27 | Lee y estudia `.md` en la vista previa de VS Code |
| 8 | Google Drive (rclone) | 27 | Montaje `~/GoogleDrive`, abrir Docs de Google en Brave |
| 9 | SUPER+R (lectura en voz alta) | 27 | La función que más pulió (voces, velocidad, pausas, VS Code) |
| 10 | Brave | 25 | Navegador único, apps web |
| 11 | Capturas | 17 | Base de sus apuntes |
| 12 | Celulares (iPhone/Huawei) | 15 | Repara celulares de clientes (ver periféricos) |
| 13 | Dictado / Maono | 13 | hyprwhspr |
| 14 | Robótica / ESP32 / Arduino | 12 | Parcial y práctica de Robótica 2 |

### Apps (contador del lanzador de Noctalia + ventanas abiertas + prompts)

| App | Evidencia | Uso |
|---|---|---|
| **Brave** + apps web | 7 ventanas abiertas ahora (WhatsApp, Telegram, Drive, Facebook en ws 1/6/8); 25 prompts | Todo lo web, PDF, Google Docs |
| **kitty** | 4 ventanas abiertas (ws 5, 9, 10) | Claude Code corre aquí |
| **Claude Code** | 583 prompts | Herramienta principal |
| **OpenDeck** | **20** aperturas desde el lanzador (la app más abierta) | Editar botones del Stream Deck |
| **VS Code** | 13 aperturas desde el lanzador + SUPER+G | Markdown, proyectos |
| **nwg-look / nwg-displays** | 10 / 4 aperturas | Tema GTK y monitores (solo al configurar) |
| Dolphin, Gwenview | ventanas abiertas | Archivos; Gwenview es el visor por defecto desde el 25-09 |
| mpv | 39 prompts de video | Reproductor de cursos |
| Obsidian | 1 apertura, vault de 80 KB (3 notas) | **Casi sin uso** a pesar de tener SUPER+N (al 26-09). **Desde el 28-09** es el visor por defecto de los apuntes de cursos (bóveda `~/Vídeos` + tarjetas de repaso) |
| Android Studio | 2 aperturas | Tesis "Lazarillo" (`~/Proyectos/Ciego`) |
| Firefox, Alacritty, code-oss | 1-2 aperturas | Duplicados (ya marcados para no instalar) |

### Atajos más usados (inferido)

| Atajo | Evidencia |
|---|---|
| **SUPER+R** leer selección | 27 prompts, memoria dedicada, también en el Fifine D6 |
| **SUPER+1..5** escritorios | 53 prompts de escritorios; perfil "Escritorios" del Fifine |
| **Pulgar del M720 / SUPER+SHIFT+S** captura al portapapeles | Lo reclamó 3 veces cuando dejó de funcionar (02-09, 20-09, 26-09) |
| **SUPER+ALT+D** dictado (movido a **SUPER+ALT+Z/X** el 26-09) | Le dicta a Claude (hay prompts claramente dictados, p. ej. 02-09: "Cloud" por "Claude"); también en el Fifine D6 |
| **SUPER** solo = buscador | Lo pidió el 18-09 |
| **SUPER+Tab** ventanas del escritorio actual | Lo pidió el 11-09 |
| **SUPER+W / SUPER+ALT+W/T/F** | Brave y apps web siempre abiertas |
| **CTRL+SHIFT+Escape** btop, **CTRL+ALT+Escape** matar LibreOffice | Pedidos el 14-09 |
| Teclas de mpv (Ctrl/Alt+←/→, `[` `]`, marcadores) | Configuradas el 25-26-09 para estudiar |

---

## (b) Línea de tiempo de lo que se fue creando

(29-08 → 28-09. Las filas del 26-09 noche al 28-09 se agregaron el 28-09.)

| Fecha | Qué | Dónde vive | ¿En docs 01-05? |
|---|---|---|---|
| 29-08 | Instalación de CachyOS + Hyprland/Noctalia; auditoría inicial, tema oscuro (`gsettings … color-scheme prefer-dark`), paru compilado en `~/aur-builds/paru`, VS Code oficial (`visual-studio-code-bin`, quitó `code`), primera guía `~/Documentos/aprender/CachyOS-Guia.md` | sistema, `~/Documentos/aprender/` | Parcial |
| 29-08 | Audio del parlante JBL por Bluetooth arreglado | PipeWire/BT | No (no dejó config propia) |
| 29-08 | `gemini-cli` por npm (ya no está instalado) | — | No |
| 30-08 | 95 paquetes actualizados + driver NVIDIA; snapshots de snapper antes y después | snapper | Sí (05) |
| 30-08 | Scripts de captura (`captura-guardar.sh`, `captura-portapapeles.sh`, `elegir-carpeta-capturas.sh`) | `~/.config/hypr/scripts/` | Sí (01) |
| 30-08 | Modo curso: `curso-abrir.sh`, `curso-configurar.sh` (SUPER+C / SUPER+ALT+C) | idem | Sí (01) |
| 30-08 | **SUPER+R** lectura con Piper + edge-tts, selector GTK4 de voz y velocidad (SUPER+ALT+R), daemon Piper | `scripts/leer-seleccion.sh`, `elegir-voz.py`, `piper-daemon.py`, `piper-voz-daemon.service` | Sí (02) |
| 30-08 | Brillo de monitores por DDC (`ddcutil`, grupo `i2c`, `i2c-dev`) | `/etc/modules-load.d/i2c-dev.conf` | Sí (05) |
| 30-08 | Disco externo de 2 TB montado en `/mnt/backups` | `/etc/fstab` | Sí (04/05) |
| 30-08 | K380 por Bluetooth; autosuspend de BT desactivado | `/etc/modprobe.d/`, `/etc/bluetooth/` | Sí (03) |
| 31-08 | **Google Drive** con rclone (client_id propio, `export_formats = link.html` para abrir Google Docs en Brave) | `rclone-gdrive.service` | Sí (02) |
| 31-08 | Apps por defecto (PDF y Docs → Brave, `.md` → vista previa de VS Code) | `mimeapps.list`, `.local/share/applications/` | Sí (04) |
| 31-08 | 2 monitores (horizontal + vertical), 5 escritorios que cambian los dos a la vez; guía `Multi-Monitor-Hyprland.md` | `hypr/config/*.lua`, `~/Documentos/aprender/` | Sí (01) |
| 31-08 | Dotfiles en GitHub: repos `hypr-config` **y `noctalia-config`** | `~/.config/hypr/.git`, `~/.config/noctalia/.git` | Solo el de hypr |
| 31-08 | Backup restic diario | `backup-home.timer` | Sí (04, roto) |
| 31-08 | Primera instalación de OpenDeck (Stream Deck XL) | `~/.config/opendeck` | Sí (03) |
| 01-09 | Curso de Claude (`CURSO_CLAUDE.md`) | `~/Documentos/claude_curso/` | No (es contenido) |
| 01-09 | SUPER+R en VS Code: Ctrl+C con **ydotool**, espera de 300 ms | `leer-seleccion.sh`, `ydotool.service` | Sí (02) |
| 02-09 | **Maono DM40 + hyprwhspr** (dictado). Guía propia de la decisión | `~/.config/hyprwhspr/`, `~/Documentos/maono/CLAUDE.md` | Sí (02), la guía no |
| 02-09 | Limpieza del texto leído (pausas, sin emojis, URLs) | `limpiar-texto.py` | Sí (02) |
| 02-09 | Pomodoro (botón del Stream Deck) | `scripts/pomodoro-toggle.sh` | Sí (01) |
| 02-09 | **M720 con logiops + xremap + solaar**; guía propia | `/etc/logid.cfg`, `~/Documentos/mouse_M720TriathlonLogitech/` | Sí (03), la guía no |
| 02-09 | Mirabox en Bitfocus Companion (desinstalado el 04-09) | restos: grupo `companion`, `50-companion-headless.rules` | Sí (03/05, como resto) |
| 02-09 | Proyecto de Robótica (ESP32 + Arduino Cloud) | Drive `Uni/Robotica2` | No |
| 03-09 | Claude Desktop (`claude-desktop`, AUR); **MCP de Vercel** en Claude Code | `~/.claude.json` (`mcpServers.vercel`) | App sí, MCP no |
| 03-09 | Portafolio Next.js con rama `developer` | `~/Documentos/claude_curso/portafolio` → `github.com/yftorrezg/portfolio` | No |
| 03-09 | **Restaurar un iPhone desde Linux** (`idevicerestore-git`, `usbmuxd`, regla udev) y guía de verificación de IMEI | `~/Documentos/movil/`, `70-apple-restore.rules` | Solo la regla (como resto) |
| 04-09 | Mirabox pasa a OpenDeck (plugin `akp153`); `atajosTeclado.md` | `~/Documentos/StreamDeck/` | Sí (03), las guías no |
| 04-09 | Huawei en recuperación (consulta, sin config) | — | — |
| 05-09 | **Fifine AmpliGame D6** con plugin `ampgd6`; perfiles "IA y Redes", "Cursos y Dev", materias de la universidad | `~/.config/opendeck/profiles/` | Perfiles copiados, botones no documentados → sección (c) |
| 06-09 | Monitores cambiados a 2 Yodoit de 15,6" | `hypr/config/monitors.lua` | Sí (01) |
| 10/11-09 | Tesis **Lazarillo** (app Android, modelos entrenados en Kaggle) | `~/Proyectos/Ciego`, `~/Android/Sdk` | No |
| 11-09 | SUPER+Tab solo en el escritorio actual | `binds.lua` | Sí (01) |
| 13-09 | nwg-displays en vivo + `watch-monitors.sh` | `hypr/scripts/` | Sí (01) |
| 14-09 | Dock de Noctalia con apps; CTRL+SHIFT+Esc btop; CTRL+ALT+Esc `matar-libreoffice.sh` | `noctalia`, `binds.lua` | Sí (01/04) |
| 16-09 | **opencode** con plugin `opencode-slim-mcp` y MCP playwright + context7 | `~/.config/opencode/opencode.jsonc` | App sí (dudosa), config no |
| 16-09 | **arduino-cli** (binario suelto) + núcleo ESP32 3.3.11 + 5 librerías | `~/.local/bin/arduino-cli`, `~/.arduino15/`, `~/Arduino/libraries/` | No |
| 18-09 | SUPER solo = lanzador | `binds.lua` | Sí (01) |
| 20-09 | M720 pierde los botones → se reinstala logid | `/etc/logid.cfg` | Sí (03) |
| 21-09 | Página "anghy21" (Netlify) | `~/Proyectos/anghy21` | No |
| 22/23-09 | "Teclas fantasma" (apagados solos): logger + logind ignora las teclas de encendido/suspensión | `solo-esta-pc/` | Sí (solo PC) |
| 23/24-09 | **Parcial de Robótica**: cinta transportadora con 2 ESP32 + ESP32-CAM, MQTT (mosquitto, `ufw allow 1883/tcp 8080/tcp`), Flask + SQLite, OpenCV | `~/.venvs/parcial1`, `~/.local/share/parcial1/` (mosquitto_data + `.db`) | No |
| 24-09 | Auditoría y limpieza de atajos (se quitaron SUPER+P, SUPER+SHIFT+W…) | `binds.lua` (+ backups en `hypr/config/backups/`) | Sí (01) |
| 25-09 | Fondo de Noctalia en los 2 monitores (volvió a la transparencia anterior) | `noctalia`, `~/.config/backup-transparencia-2026-09-25/` | Parcial |
| 25-09 | Gwenview por defecto (navegar con ←/→ por la carpeta) | `mimeapps.list` | Sí (04) |
| 25-09 | **mpv de estudio** (uosc, velocidad ×0.1, marcadores, curso.lua) | `~/.config/mpv/` | Sí (04) |
| 25-09 | `sesion-ventanas.py` (restaurar ventanas al iniciar), `app-web.sh` abre en el escritorio actual | `hypr/scripts/` | Sí (01) |
| 25-09 | Flags VA-API de Brave | `brave-flags.conf` | Sí (04) |
| 26-09 00:26 | Regla udev que reinicia logid al reconectar el M720 | `/etc/udev/rules.d/99-logid-m720.rules` | Sí (03) |
| 26-09 00:27 | **gnome-keyring se desbloquea al iniciar sesión** (PAM de greetd), porque al arrancar le pedía la contraseña del llavero | `/etc/pam.d/greetd` | **No** → copiado a `system/etc/pam.d/greetd` |
| 26-09 01:00 | mpv: Ctrl+←/→ ±10 s, Alt+←/→ ±30 s | `mpv/input.conf` | Sí (README) |
| 26-09 | `descargar` (yt-dlp + aria2, cookies de Brave), `doblar` (inglés→español con whisper + NLLB, venv de 3,6 GB), `whisper-cpp` + `ggml-vulkan`, auto-captura SUPER+ALT+S, `video-a-capturas.sh` | `~/.local/bin/`, `~/.local/share/doblar/`, `hypr/scripts/` | **Otro documento** |
| 26-09 | Paquete de migración | `~/migracion-cachyos/` | — |
| 26-09 23:00 | `doblar.py`: caché por nombre+tamaño (mover la carpeta no pierde el trabajo), acelera hasta ×1,45 si la voz se atrasa, aviso de desfase, un error no corta la carpeta | `~/.local/share/doblar/doblar.py` | Sí (06 §2) |
| 26/27-09 | **Cuadernillo de apuntes** (`cuadernillo.py`: capturas importantes + subtítulos + OCR tesseract + Claude → `apuntes.md` + `INDICE.md`), **SUPER+ALT+Y** (link de YouTube copiado) y **SUPER+ALT+A** (curso entero, `curso-a-apuntes.sh`, reanudable, nice), barrita de progreso (primero como notificación ▰▱). Curso de Karpathy procesado entero | `hypr/scripts/`, `binds.lua` | Sí (06 §3) |
| 27-09 | Lectura SUPER+R un poco más lenta (`SPEED_MULT` 1.3 → 1.2) | `hypr/scripts/voz.conf` | Sí (02) |
| 27/28-09 | `resumen.md` (repaso corto, `resumen-corto.py`); algoritmo de captura con detección de webcam e historial exigente; prueba de estrés (200 cambios → 0 perdidos) | `hypr/scripts/` | Sí (06 §3) |
| 28-09 | yt-dlp con `-S "proto,vcodec:h264"` (el HLS pesaba 6 GB en vez de 335 MB); capturas en **WebP sin pérdida** (`capturas-a-webp.py`) con nombre corto `0001.webp` + `.minutos.tsv` (`capturas-nombre-corto.py`) | `hypr/scripts/` | Sí (06 §3.4) |
| 28-09 | Apuntes con **Claude Sonnet** por defecto (`APUNTES_MODELO`) y `resumen.md` en la **misma llamada** (ahorro de cuota) | `cuadernillo.py` | Sí (06 §3.4) |
| 28-09 (con 3 agentes en paralelo) | **Playlists** (`playlist-a-apuntes.sh`, reanudable, espera ante el anti-bot), **cola** (`cola-capturas.sh`: un pedido por vez), **barrita GTK4 layer-shell** en el monitor vertical (`progreso.py`), **tarjetas** (`tarjetas.py` + plugin Obsidian Spaced Repetition 1.15.4 en la bóveda `~/Vídeos`, + Anki), **panel** `~/Vídeos/Mis cursos.md` (`panel-cursos.py`), pruebas nuevas (`*-tests.py`, `*-tests.sh`). Medido: **~10,5 min por hora de video** con IA | `hypr/scripts/`, `~/Vídeos/.obsidian/` | Sí (06 §3) |
| 28-09 | `.md` se abren en **Obsidian** si están en una bóveda, si no en VS Code (`abrir-markdown.py` + `abrir-markdown.desktop` + `xdg-mime`); `~/Vídeos` registrada como bóveda "Vídeos" | `mimeapps.list`, `.local/share/applications/`, `~/.config/obsidian/obsidian.json` | Sí (06 §3.4); doc 04 dice aún "`.md` → VS Code" |
| 28-09 | Qt oscuro: plantilla propia de Noctalia `templates/qtct-oscuro.conf` (bordes oscuros en Fusion) en vez de la `qt` integrada; Dolphin con vista previa compacta | `noctalia/config.toml`, `qt6ct/colors/`, `dolphinrc` | Copiado al paquete; no documentado en 01/04 |
| 28-09 noche | En marcha: playlist "Curso JavaScript" de **166 videos** con `playlist-a-apuntes.sh` (YouTube ya respondió 429 una vez) | `~/Vídeos/Capturas de YouTube/` | Datos, no config |
| 28-09 | Paquete de migración actualizado (scripts, bóveda Obsidian, docs 06/07, guía de auto-captura) | `~/migracion-cachyos/` | — |
| 01-10 | VS Code deja de fijarse al escritorio 4 | `hypr/config/windowrules.lua` | Sí (01) |
| 03-10 | Productividad de shell y Dolphin (zoxide, fzf, plantilla Markdown, «Abrir con VS Code/Obsidian») | `fish/config.fish`, `dolphinrc` | Sí (04) |
| 05-10 | **Mouse Scimitar con keyd** (modos Estudio/Programación/Redes), `mouse-*.sh`, guía `atajos-y-mouse.md`; lectura SUPER+R a ×1.4; ckb-next desactivado para botones laterales | `/etc/keyd/default.conf`, `hypr/scripts/mouse-*.sh`, `voz.conf` | Solo PC (03 §9) salvo `voz.conf` |
| 05-10 | Gwenview oscuro + atajos propios incluidos en el paquete; plantilla Qt de Noctalia regenera `kdeglobals` | `gwenviewrc`, `gwenviewui.rc` | Sí (03 §9.1) |
| 06-10 | **Auditoría completa** (atajos 98/98 OK, paquetes, espacio) y limpieza: ~28 GB (cachés, worktrees); `~/Proyectos/Ciego` a GitHub privado; paquete de migración sincronizado; doc 09 | todo | Sí (09) |

---

## (c) Stream Deck: botones por perfil

Todo vive en `~/.config/opendeck/profiles/<dispositivo>/<perfil>.json` (ya copiado en `dotfiles/`). Casi todos los botones usan **Run Command** (plugin `starterpack`) con `uwsm app -- …`. La posición es el índice de la tecla (`Keypad.N`), contada de izquierda a derecha y de arriba abajo. Plugins instalados: `starterpack`, `oadesktopentry` (Launch App), `oampris` (multimedia), `tasktimer`, `obsideck`, `uinput` (Simulate Input), `opendeck-akp153` (Mirabox) y `opendeck-ampgd6` (Fifine).

### Elgato Stream Deck XL (`sd-A00NA538346JSS`, 32 teclas)

**Perfil "Default"**

| # | Botón | Acción |
|---|---|---|
| 0 | Archivos | `dolphin` |
| 1 | NotebookLM | Brave → notebooklm.google.com |
| 2 | Brave | `brave` |
| 3 | VS Code | `code` |
| 4 | Editor | `gnome-text-editor` |
| 5 | Obsidian | Launch App |
| 6 | OBS | Launch App |
| 7 | btop | `kitty -e btop` |
| 8 | aprender | `dolphin ~/Documentos/aprender` |
| 9 | Descargas | `dolphin ~/Descargas` |
| 10 | Documentos | `dolphin ~/Documentos` |
| 12 | Bloquear | `noctalia msg session lock` |
| 13 | Guía | `vscode-open-md.sh …/aprender/CachyOS-Guia.md` |
| 14 | Mute | `wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle` |
| 15 | Emoji | lanzador de Noctalia `/emo` |
| 16-18 | GitHub · Gmail · Drive | Brave (ventana nueva) |
| 19 | fCC | freecodecamp.org |
| 20 | "MDN" | **abre un video de React en YouTube** (etiqueta equivocada) |
| 21-22 | Claude · YouTube | Brave |
| 23 | → perfil "web" | Switch Profile |
| 24 | Modo Código | Multi: VS Code + kitty en `~/Documentos/aprender` |
| 25 | Modo Estudio | Multi: freeCodeCamp + `Plan-Aprendizaje.md` en VS Code |
| 26 | Fecha | `wtype "$(date +%Y-%m-%d)"` (escribe la fecha) |
| 27 | OpenDeck | Launch App |
| 28 | react | Open URL (el mismo video de React) |
| 29 | Mic | `wpctl set-mute @DEFAULT_SOURCE@ toggle` |
| 30 | Buenos días | Multi: Gmail + Drive |
| 31 | Brillo | Toggle 0 % / 100 % del Stream Deck |

**Perfil "web"** (lanzadores y multimedia): 0 LibreOffice Writer · 1 Editor de texto · 3 pista anterior · 4 mpv · 5 pista siguiente · 6 Open URL (vacío) · 7 Dolphin · 10 kitty · 11 −10 s · 12 Play/Pausa · 13 +10 s · 16 OpenDeck · 18 Obsidian · 24 Solaar · 26 VS Code · 29 Brave · 31 volver a Default.

### Mirabox Stream Dock HSV293S (`99-355499441494-293S`, 15 teclas + 3 del panel)

| # | "Default" (materias) | "IA y Redes" | "Cursos y Dev" |
|---|---|---|---|
| 0 | → IA y Redes | → Cursos y Dev | → Default |
| 1 | Base3 (Drive) | Gemini | Udemy |
| 2 | Captura al portapapeles | DeepSeek | Duolingo |
| 3 | Elegir carpeta de capturas | NotebookLM | Sololearn |
| 4 | Cambiar voz (SUPER+ALT+R) | YouTube | Vercel |
| 5 | — | Telegram | Netlify |
| 6 | Robotica2 (Drive) | WhatsApp Web | |
| 7 | Taller1 (Drive) | TikTok | |
| 8 | Telegram | Instagram | |
| 9 | — | Pomodoro | |
| 10 | `dolphin ~/Imágenes` | Claude | |
| 11 | — | ChatGPT | |
| 12 | Taller2 (Drive) | Qwen | |
| 13 | Etica (Drive) | Facebook | |
| 14 | Captura guardada | AI Studio | |
| 15-17 | Brillo 0 % / 100 % | Canva · Ideogram · Bing Image | |

Los enlaces de Drive de las materias están en la memoria `claude-memoria/proyectos/Documentos-StreamDeck/drive_carpeta_universidad.md`.

### Fifine AmpliGame D6 (`d6-355499441494-AMPGD6`, 15 teclas; la 2 cambia de perfil en ciclo)

| # | "Default" (Estudio) | "Ventanas" | "Escritorios" | "Lanzadores" |
|---|---|---|---|---|
| 0 | Captura (`noctalia msg screenshot-region`) | Cerrar ventana | Escritorio anterior | kitty |
| 1 | Elegir carpeta de capturas | Foco ↑ | Escritorio 1 | Dolphin |
| 2 | → Ventanas | → Escritorios | → Lanzadores | → Estudio |
| 3 | kitty | Maximizar | Escritorio 2 | Editor de texto |
| 4 | Bloquear | Pantalla completa | Escritorio siguiente | Brave |
| 5 | Buscador | Foco ← | Escritorio 3 | Calculadora |
| 6 | Emoji | Ciclar ventana | Escritorio 4 | btop |
| 7 | **Dictado** (`hyprwhspr record toggle --lang es`) | Foco → | Escritorio 5 | Lanzador |
| 8 | Archivos (SUPER+E simulado) | — | Próximo vacío | Ajustes rápidos |
| 9 | Cerrar ventana | Dividir layout | Special workspace | Centro de control |
| 10 | Configurar curso | — | Enfocar monitor 1 | Notificaciones |
| 11 | Ir al curso | Foco ↓ | Enfocar monitor 2 | Historial del portapapeles |
| 12 | Maximizar | Selector de ventanas | Mover a monitor 1 | Fondos de pantalla |
| 13 | Pantalla completa | Flotar/mosaico | Mover a monitor 2 | Selector de color (`hyprpicker`) |
| 14 | **Leer selección** (SUPER+R) | — | — | Emoji |

**Para la laptop:** los botones usan `hyprctl dispatch 'hl.dsp…'` (sintaxis Lua, válida) y las variables `MONITOR1`/`MONITOR2`. Con una sola pantalla, "Enfocar/Mover a monitor 2" no hacen nada. Los botones que simulan teclas (Simulate Input, plugin `uinput`) necesitan `/dev/uinput` y el grupo `input`. Guías completas del usuario: `~/Documentos/StreamDeck/docs/` (`opendeck-guia.md`, `portabilidad-laptops.md`, `dispositivos.md`).

---

## (d) Herramientas instaladas fuera de pacman

| Herramienta | Dónde | Reinstalar en la laptop |
|---|---|---|
| **Claude Code** 2.1.283 | `~/.local/bin/claude` → `~/.local/share/claude/versions/` | `curl -fsSL https://claude.ai/install.sh \| bash`. **No usar `sudo npm`**: en la PC quedó una copia vieja (2.1.251) en `/usr/lib/node_modules/@anthropic-ai/claude-code` + `/usr/bin/claude`, de un intento del 29-08 (hoy tapada por `~/.local/bin`) |
| MCP **vercel** (Claude Code, alcance usuario) | `~/.claude.json` | `claude mcp add --transport http vercel https://mcp.vercel.com` y luego `/mcp` → login. Los conectores de claude.ai (Drive, Calendar, Context7, Hugging Face, Netlify, Docs) vienen con la cuenta |
| Marketplace de plugins de Claude | `~/.claude/plugins/known_marketplaces.json` (`anthropics/claude-plugins-official`) | `/plugin marketplace add anthropics/claude-plugins-official` |
| **edge-tts** 7.2.8 | pipx | `pipx install edge-tts` (ya en doc 04) |
| **arduino-cli** | binario suelto `~/.local/bin/arduino-cli` (36 MB) | `sudo pacman -S arduino-cli` (o el script oficial con `BINDIR=~/.local/bin`). Luego copiar `dotfiles/.arduino15/arduino-cli.yaml` (URL del gestor de placas ESP32), `arduino-cli core update-index && arduino-cli core install esp32:esp32@3.3.11`, y `arduino-cli lib install ArduinoJson ESP32Servo Keypad LiquidCrystal_I2C MQTT` (lista en `paquetes/arduino-libraries.txt`). Grupo `uucp` para el puerto serie |
| `descargar`, `doblar` | `~/.local/bin/`, `~/.local/share/doblar/` (venv + modelos, 3,6 GB) | **Otro documento** |
| opencode (pacman) + config | `~/.config/opencode/opencode.jsonc` (plugin `opencode-slim-mcp`, MCP playwright y context7 vía `npx`) | Copiado en `dotfiles/.config/opencode/`. Solo si el usuario lo quiere (dudoso) |
| antigravity-cli (`agy`, AUR) | `~/.gemini/antigravity-cli` | `paru -S antigravity-cli` + login (dudoso) |
| Extensiones de VS Code (95) | `~/.vscode/extensions` | Lista en `paquetes/vscode-extensions.txt` → `xargs -n1 code --install-extension < paquetes/vscode-extensions.txt`. Hay una carpeta `Code/User/sync`, así que la **sincronización de ajustes** de VS Code puede estar activa: iniciar sesión en VS Code también las trae. Muchas son de PHP/Java/C#/Django viejas: conviene preguntarle cuáles quiere |
| Snippets de VS Code (`html.json`, `markdown.json`) | `~/.config/Code/User/snippets/` | Copiados en `dotfiles/` |
| Plugins de OpenDeck (8) | `~/.config/opendeck/plugins/` | Ya copiados con `~/.config/opendeck` |
| GitKraken CLI (`gk`) | `~/.local/share/GitKrakenCLI/` | Lo instala la extensión GitLens sola; no hace falta |
| Android SDK (1,7 GB) | `~/Android/Sdk` | Lo baja Android Studio (`paru -S android-studio`) — **hace falta para la tesis** |
| venv del parcial de Robótica (306 MB) | `~/.venvs/parcial1` (Flask, paho-mqtt, OpenCV) | `python -m venv ~/.venvs/parcial1 && pip install flask paho-mqtt opencv-python` si se retoma |
| paru | `~/aur-builds/paru` | Ya viene en CachyOS |
| npm global | prefijo `~/.local` (`~/.npmrc`), **vacío** | Nada (el `gemini-cli` del 29-08 ya no está) |
| `~/.local/bin/python3.11` | enlace **roto** a `/tmp/uv-python/…` | No copiar |

Cargo, go, bun y deno no se usan. Flatpak tampoco.

---

## (e) Periféricos y dispositivos

| Aparato | Qué hay configurado | Dónde está la doc/config |
|---|---|---|
| **Maono DM40** (micrófono corbatero inalámbrico, receptor USB `SmartlinkTechnology_Maono_DM40_RX`, mono 48 kHz) | Lo usa hyprwhspr (`audio_device_name: "Maono"`). Es un micrófono USB estándar: en la laptop debería funcionar igual, **si lleva el receptor puede dejar `"Maono"`** (hyprwhspr usa el mic por defecto cuando no lo encuentra) | doc 02 + `~/Documentos/maono/CLAUDE.md` (opciones evaluadas: Handy, OpenWhispr, nerd-dictation, hyprvoice = plan B) |
| **Logitech M720 + K380** (Bluetooth) | logiops, regla udev de reconexión, BT sin autosuspend. xremap corre sin reglas; solaar solo para ver la batería | doc 03 + `~/Documentos/mouse_M720TriathlonLogitech/README.md` |
| **Stream Deck XL, Mirabox HSV293S, Fifine D6** | OpenDeck 2.14 + 2 plugins no oficiales + 3 reglas udev. El 26-09 a la 01:01 dijo que "OpenDeck no reconoce el Stream Deck XL" (no consta que se resolviera; la guía dice: desenchufar/enchufar y reiniciar OpenDeck) | doc 03 + sección (c) + `~/Documentos/StreamDeck/` |
| **Celulares (trabajo de reparación)** | No hay KDE Connect ni scrcpy. Solo: restaurar iPhone con `idevicerestore-git` + `usbmuxd` + regla `70-apple-restore.rules` (03-09), guía de verificación de IMEI/FRP/iCloud, e intento con un Huawei. El 11-09 usaba **adb** con un Samsung SM-S928B para la tesis (de Android Studio) | `~/Documentos/movil/restauracion-iphone-linux.md`, `verificacion-imei-antes-de-reparar.md` |
| **ESP32 / ESP32-CAM / Arduino** | arduino-cli, núcleo esp32 3.3.11, librerías, mosquitto (MQTT) con puertos 1883 y 8080 abiertos en ufw, grupo `uucp` | sección (d); proyectos en Drive `Uni/Robotica2` |
| Parlante **JBL** (BT) | Arreglado el 29-08, sin config propia | — |
| Monitores (2 Yodoit 15,6"; antes Xiaomi + HP) | Solo de la PC | doc 01 |
| Disco externo "SuperYafer" (`/run/media/yafer/SuperYafer`) | Ahí están los cursos, los marcadores de mpv y **la carpeta de capturas actual** (`carpeta-capturas.conf` apunta a una carpeta de ese disco; `video-a-capturas.sh` cae a `~/Imágenes/Capturas` si no está montado, pero **`captura-guardar.sh` no**: falla. En la laptop hay que poner una ruta local en `carpeta-capturas.conf`) | doc 04 (mpv) |

---

## (f) Proyectos del usuario

| Proyecto | Qué es | Git / remoto |
|---|---|---|
| `~/Proyectos/Ciego` | **Tesis "Lazarillo"**: app Android (Kotlin) de ayuda para ciegos, con modelos de visión entrenados en Kaggle. Pendiente: probar el servicio en primer plano en el teléfono | git local, **sin remoto** (⚠️ solo existe en esta PC y en el backup restic, que está roto) |
| `~/Documentos/claude_curso/portafolio` | Portafolio Next.js (ramas main/developer, Vercel) | `github.com/yftorrezg/portfolio` |
| `~/Proyectos/closet-outlet` | Tienda React + Vite | `github.com/yftorrezg/closet-outlet` |
| `~/Proyectos/anghy21` | Página personalizada (Netlify, 21-09) | sin git |
| `~/Proyectos/mundoanimal` | Carpeta vacía | — |
| `~/.config/hypr`, `~/.config/noctalia` | Dotfiles | `github.com/yamilfernandotorrezgarciacc-bit/hypr-config` (36 cambios sin commit) y `…/noctalia-config` (2 cambios sin commit) |
| `~/Documentos/aprender`, `claude_curso`, `StreamDeck`, `maono`, `lectura`, `movil`, `mouse_M720…` | Guías y notas en markdown que Claude escribió para él (varias pensadas "para la laptop") | sin git, **no están en Drive** |
| Drive `Uni/Robotica2`, `Udemy`, `trabajos/` | Tareas de la universidad y cursos | Google Drive |

Perfil (de las memorias): estudiante de Ing. en Ciencias de la Computación (Sucre, Bolivia), enfocado en IA aplicada + fullstack; quiere **entender** lo que se hace ("modo profesor"); estudia con capturas y videos; usa mucho Gemini para estudiar.
