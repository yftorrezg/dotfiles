---
tags: [sistema, paquetes]
actualizado: 2026-09-26
---
# 04 — Apps, paquetes, apps por defecto, shell y backups

Para la instancia de Claude que configure las laptops (Surface Pro 6 i7 8ª gen / ThinkPad E14 Gen4 i7 12ª gen, ambas GPU Intel integrada).
Origen: PC CachyOS + Hyprland (shell **noctalia**, paquete `cachyos-hypr-noctalia`), CPU Intel i7-6700K + NVIDIA GTX 980. Usuario `yafer`, responde siempre en español.
Estado a 2026-09-26.

Archivos relacionados en `~/migracion-cachyos/`:
- `paquetes/pacman-repo.txt`, `paquetes/aur.txt` — listas crudas (flatpak no se usa).
- `paquetes/CLASIFICACION.md` — clasificación completa (NVIDIA / base / apps USA / DUPLICADO / DUDOSO) con evidencia.
- `dotfiles/` — configs copiadas respetando la ruta relativa a `$HOME` (ver sección 8).

---

## 1. Apps que usa de verdad (y para qué)

| Función | App | Cómo se lanza |
|---|---|---|
| Navegador | **Brave** (`brave-bin`) | SUPER+W. Apps web con `~/.config/hypr/scripts/app-web.sh` (`brave --app=URL`): SUPER+ALT+Q YouTube, +W WhatsApp, +T Telegram, +F Facebook, +I Instagram, +D Drive, SUPER+T TikTok |
| Terminal | **kitty** | SUPER+Return; CTRL+SHIFT+Escape abre `kitty -e btop` |
| Archivos | **Dolphin** (+ Ark) | SUPER+E |
| Imágenes | **Gwenview** | por defecto para todo `image/*` (cambiado desde imv el 26-09) |
| Video/audio | **mpv** (config de estudio, sección 5) | por defecto para video/* y audio/* |
| PDF | **Brave** (ventana nueva) | `brave-new-window.desktop` |
| Capturas | noctalia (Impr / SUPER+Impr) → **satty** para editar; scripts `captura-guardar.sh` (CTRL+SHIFT+S) y `captura-portapapeles.sh` (SUPER+SHIFT+S) con grim+slurp; auto-captura de cursos `auto-captura-toggle.sh` (SUPER+ALT+S) y `video-a-capturas.sh` | auto-captura necesita `python-numpy`, `python-pillow`, `yt-dlp`, `ffmpeg` |
| Notas | **Obsidian** | SUPER+N |
| Código | **VS Code** (`visual-studio-code-bin`, AUR) | SUPER+G (enfoca/abre en escritorio 4). Los `.md` fuera de una bóveda de Obsidian se abren en VS Code (desde el 28-09 vía `abrir-markdown.desktop`, ver doc 06 §3.4) |
| Texto plano | gnome-text-editor | viene con noctalia |
| Calculadora | gnome-calculator | tecla XF86Calculator |
| Ofimática | LibreOffice (Writer, Impress) | CTRL+ALT+Escape mata LibreOffice colgado |
| IA | Claude Desktop (`claude-desktop`), Claude Code (`~/.local/bin/claude`, instalador oficial) | |
| Contraseñas | KeePassXC | |
| Compartir | LocalSend, RustDesk | |
| Grabar pantalla | OBS Studio | |
| Voz | SUPER+R lee la selección (edge-tts online vía pipx o Piper offline, `piper-voices-es-*`); SUPER+ALT+R elige voz; **hyprwhspr** = dictado | necesitan `wtype`, `ydotool`, `zenity` |
| Mouse M720 | **logiops** (`logid`, AUR; `/etc/logid.cfg`): pulgar = captura al portapapeles, click central = captura a archivo, inclinar rueda = cambiar pestaña (ver doc 03) | servicio de sistema `logid` |
| Teclado | xremap (`xremap-hypr-bin`): servicio activo pero **config vacía, no remapea nada** → opcional, no instalar en laptop | |
| Stream Deck | opendeck-bin (SUPER+K) | solo si se lleva el Stream Deck |

Tabla completa USA / DUPLICADO / DUDOSO con evidencia: `paquetes/CLASIFICACION.md`.

### Duplicados — NO instalar en la laptop
`firefox`, `geeqie`, `imv`, `okular`, `alacritty`, `vlc-plugins-all`. (Chromium/Chrome/Edge/Opera/Vivaldi y Code-OSS ni siquiera están instalados; sus carpetas en `~/.config` son residuos, no copiarlas.)

### Dudosos — preguntar al usuario antes de instalar
gimp, kdenlive (usados una vez en agosto), xournalpp (interesante para el lápiz de la Surface), meld, opencode, antigravity-cli, android-studio, docker(+compose, servicio deshabilitado), mosquitto, tesseract, solaar, opendeck-bin, swappy.

---

## 2. Apps por defecto

Se copian con `dotfiles/.config/mimeapps.list`. Resumen:

| MIME | App (.desktop) |
|---|---|
| image/* (png, jpeg, webp, gif, svg, avif, heif, psd, xcf...) | `org.kde.gwenview.desktop` |
| video/*, audio/* (mp4, mkv, webm, mov, avi, mp3, flac, ogg...) | `mpv.desktop` |
| application/pdf, application/x-gdoc-link | `brave-new-window.desktop` (personalizado, en `~/.local/share/applications/`) |
| text/html, x-scheme-handler/http(s), about, unknown | `brave-browser.desktop` |
| inode/directory | `org.kde.dolphin.desktop` |
| text/plain | `org.gnome.TextEditor.desktop` |
| text/markdown | `abrir-markdown.desktop` (personalizado, 28-09): Obsidian si el `.md` está en una bóveda (p. ej. `~/Vídeos`), si no VS Code. Antes: `vscode-markdown-preview.desktop` (sigue copiado) |
| x-scheme-handler/claude | `com.anthropic.Claude.desktop` (personalizado) |
| x-scheme-handler/claude-cli | `claude-code-url-handler.desktop` (personalizado) |
| opendeck/openaction/streamdeck | `opendeck-handler.desktop` |

Ojo: al final de `mimeapps.list` hay una lista de MIME de video sueltos sin `=app` (líneas basura de una edición anterior; solo la última, `video/vnd.avi=mpv.desktop`, es válida). Son inofensivas; se puede limpiar.

Verificar en la laptop:
```bash
for m in image/png image/jpeg video/mp4 application/pdf text/html inode/directory; do echo "$m: $(xdg-mime query default $m)"; done
```

`.desktop` personalizados (copiados en `dotfiles/.local/share/applications/`): `brave-new-window`, `vscode-markdown-preview`, `abrir-markdown` (Exec a `/home/yafer/.config/hypr/scripts/abrir-markdown.py`), `com.anthropic.Claude`, `claude-code-url-handler` (Exec a `/home/yafer/.local/bin/claude`), `opendeck-handler`, `nwg-displays` (apunta a `~/.config/hypr/config/nwg-monitors.conf`). Tras copiarlos: `update-desktop-database ~/.local/share/applications`.

---

## 3. Shell: fish

- Shell por defecto: `/bin/fish`. `~/.config/fish/config.fish` solo hace `source /usr/share/cachyos-fish-config/cachyos-config.fish` (paquete `cachyos-fish-config`, viene con CachyOS).
- **No hay abbr ni funciones propias.** Todas las funciones (`ll`, `la`, `lt`, `update`, `mirror`, `cleanup`, `fixpacman`, `jctl`, `tarnow`, `untar`, `psmem`, `rip`, `backup`, `copy`, `grubup`...) vienen de cachyos-fish-config.
- `fish_variables` (universales) contiene: `fish_user_paths = ~/.local/bin` (importante: ahí están `claude`, `backup-home.sh`, `edge-tts`), colores del prompt `pure`, y `__done_min_cmd_duration 10000` (notificación si un comando dura >10 s). Se copió `fish_variables`; no contiene secretos.
- Terminal kitty: `kitty.conf` mínimo (opacidad 1.0, `cursor_trail 1`, `window_padding_width 25`, `include themes/noctalia.conf` — el tema lo genera noctalia).

---

## 4. Backups (restic + backup-home.timer)

- Unidades de usuario: `~/.config/systemd/user/backup-home.service` (oneshot, `ExecStart=%h/.local/bin/backup-home.sh`) y `backup-home.timer` (`OnCalendar=daily`, `Persistent=true`, `RandomizedDelaySec=30m`). Copiados en `dotfiles/`.
- **Qué respalda:** todo `/home/yafer` con `restic backup`, excluyendo lo de `~/.config/restic/home-excludes.txt` (`.cache`, papelera, containers, Steam, node_modules, venvs, `__pycache__`, `*.tmp`, cachés de Firefox/Brave/Chrome) y `--exclude-caches`.
- **A dónde:** repositorio restic `/mnt/backups/restic-home` en un **disco externo exFAT** (fstab: `UUID=7FDC-A53B /mnt/backups exfat defaults,nofail,uid=1000,gid=1000,umask=000`). Si no está montado, el script aborta.
- Retención: `restic forget --keep-daily 7 --keep-weekly 4 --keep-monthly 6 --prune`.
- Contraseña: `~/.config/restic/home-backup.pass` (**NO se copió** a propósito; pedirla al usuario o copiarla a mano por un medio seguro, `chmod 600`).
- Log: `~/.local/state/backup-home.log`. Hay 21 snapshots (último 25-09, ~90 GiB).
- **ARREGLADO el 26-09:** se agregó `/home/yafer/GoogleDrive` a `home-excludes.txt` y se quitaron 4 bloqueos huérfanos con `restic unlock` (el `home-excludes.txt` copiado ya trae la exclusión). Historial de los problemas:
- **PROBLEMA 2 detectado en la PC (verificado 26-09):** `home-excludes.txt` NO excluye `GoogleDrive` y el script no usa `--one-file-system`, así que restic recorre el Drive montado por rclone (el backup del 26-09 llevaba ~50 min con archivos abiertos en `~/GoogleDrive`). En la laptop agregar la línea `GoogleDrive` a `home-excludes.txt` (o `--one-file-system`).
- **PROBLEMA detectado en la PC:** hay un lock viejo en el repo (PID 168805, del 01-09). El `restic backup` termina bien, pero el `forget --prune` falla con "repository is already locked" y, como el script usa `set -e`, nunca escribe "fin backup" ni se poda. Arreglo (con el disco montado y sin otro restic corriendo): `restic -r /mnt/backups/restic-home unlock`.
- En la laptop: decidir si el disco externo será el mismo (mismo repo, restic distingue por hostname) y habilitar con `systemctl --user enable --now backup-home.timer`. En una laptop el disco no siempre estará conectado: el script ya lo tolera (aborta limpio) y `Persistent=true` recupera el pendiente.
- Relacionado: `rclone-gdrive.service` (usuario) monta Google Drive en `~/GoogleDrive` con `rclone mount gdrive:`; necesita `~/.config/rclone/rclone.conf`, que **no se copió** (tokens) → rehacer con `rclone config`.

---

## 5. mpv (reproductor de estudio)

Guía completa del usuario: `~/.config/mpv/GUIA-MPV.md` (copiada). Estructura copiada en `dotfiles/.config/mpv/` (sin `*.bak*`):
- `mpv.conf`: `vo=gpu-next`, `hwdec=auto-safe`, OSC nativo apagado (lo dibuja **uosc**), `keep-open`, lista automática de la carpeta en orden natural (`autocreate-playlist=filter`, `directory-mode=recursive`), recuerda posición (`save-position-on-quit`), `audio-pitch-correction`, subtítulos/audio preferidos en español, capturas (tecla s) en `~/Imágenes/Capturas-mpv`.
- `scripts/`: `uosc/` (interfaz + explorador de carpetas), `velocidad.lua` (pasos de ×0.1 y recuerda última velocidad), `marcadores.lua` (hasta 9 marcadores por video), `curso.lua` (carga un curso entero con subcarpetas). `script-opts/uosc.conf`, `fonts/` (iconos de uosc).
- Datos de uso copiados en `dotfiles/.local/state/mpv/` (`marcadores.json`, `ultima-velocidad`, `watch_later/`): las rutas apuntan sobre todo a `/run/media/yafer/SuperYafer/...` (disco externo), así que siguen valiendo si se monta con la misma etiqueta.
- Atajos de salto (`input.conf`): **←/→ ±5 s, Ctrl+←/→ ±10 s, Alt+←/→ ±30 s**; Shift+←/→ desactivado; doble clic = pantalla completa; clic derecho = menú uosc.
- **Aceleración por hardware en Intel:** `hwdec=auto-safe` usa VA-API. En esta PC funcionaba con `libva-nvidia-driver`; en las laptops hay que instalar el driver VA-API de Intel:
  - ThinkPad E14 Gen4 (12ª gen, Alder Lake, Iris Xe): **`intel-media-driver`** (iHD). `libva-intel-driver` (i965) NO soporta Alder Lake.
  - Surface Pro 6 (8ª gen, Kaby Lake-R, UHD 620): **`intel-media-driver`** recomendado (soporta Broadwell+); `libva-intel-driver` también funciona como alternativa (`export LIBVA_DRIVER_NAME=i965`).
  - Verificar: `sudo pacman -S --needed libva-utils && vainfo` (debe decir `Driver version: Intel iHD driver` y listar perfiles H264/HEVC/VP9), y `mpv --hwdec=auto-safe -v video.mp4 2>&1 | grep -i hwdec` → debe decir `Using hardware decoding (vaapi)`. La tecla `Ctrl+h` en mpv alterna hwdec.
  - Brave: `~/.config/brave-flags.conf` tiene `VaapiOnNvidiaGPUs` y `VaapiIgnoreDriverChecks` (específicos de NVIDIA). **En la laptop quitar `VaapiOnNvidiaGPUs`**; dejar `--ozone-platform-hint=auto`, `AcceleratedVideoDecodeLinuxGL,AcceleratedVideoDecodeLinuxZeroCopyGL` y `--enable-gpu-rasterization`. Comprobar en `brave://gpu` → "Video Decode: Hardware accelerated".

---

## 6. Comando de instalación en la laptop

Suponiendo CachyOS instalado con la edición **Hyprland (noctalia)** — eso ya trae `cachyos-hypr-noctalia` (kitty, dolphin, gnome-text-editor, gnome-calculator, grim, slurp, wl-clipboard, noctalia...), fish y la base (ver CLASIFICACION.md sección b). Si no se eligió esa edición, añadir `hyprland cachyos-hypr-noctalia noctalia-greeter` al primer comando.

```bash
# 1) Driver gráfico Intel + VA-API (NO instalar nada nvidia*)
sudo pacman -S --needed intel-media-driver vulkan-intel libva-utils
# (Solo Surface, opcional alternativa: sudo pacman -S --needed libva-intel-driver)

# 2) Apps que usa (repos oficiales + cachyos)
sudo pacman -S --needed \
  brave-bin kitty dolphin ark gwenview mpv satty obsidian claude-desktop \
  libreoffice-fresh libreoffice-fresh-es keepassxc localsend obs-studio \
  wtype ydotool zenity inotify-tools jq restic rclone \
  python-numpy python-pillow yt-dlp \
  git github-cli ripgrep nodejs npm python-pipx \
  nwg-displays pavucontrol glances pv btop micro fastfetch \
  7zip unrar unzip ffmpegthumbnailer

# 3) AUR (con paru, ya viene en CachyOS)
paru -S --needed visual-studio-code-bin hyprwhspr piper-voices-es-ar piper-voices-es-mx rustdesk-bin logiops
sudo cp ~/migracion-cachyos/system/etc/logid.cfg /etc/ && sudo cp ~/migracion-cachyos/system/etc/udev/rules.d/99-logid-m720.rules /etc/udev/rules.d/ && sudo systemctl enable --now logid   # solo si usa el M720

# 4) Herramientas vía pipx / instalador oficial
pipx install edge-tts                       # voz online de SUPER+R
curl -fsSL https://claude.ai/install.sh | bash   # Claude Code en ~/.local/bin/claude
```

NO instalar: `nvidia-580xx-*`, `lib32-nvidia-580xx-utils`, `opencl-nvidia-580xx`, `lib32-opencl-nvidia-580xx`, `libva-nvidia-driver`, `idevicerestore-git` (+ sus `lib*-git`), `xremap-hypr-bin` (config vacía), ni los duplicados (`firefox geeqie imv okular alacritty vlc-plugins-all`).
Opcionales si el usuario confirma: `gimp kdenlive xournalpp meld opencode docker docker-compose mosquitto tesseract tesseract-data-spa solaar swappy` (repo) y `antigravity-cli android-studio opendeck-bin` (AUR).

Nota: `satty` hoy está instalado como dependencia huérfana (`pacman -Qdt` lo lista); en la laptop instalarlo explícito (ya incluido arriba) porque noctalia lo usa para editar capturas.

---

## 7. Servicios de usuario relacionados con apps

Habilitados en la PC (`~/.config/systemd/user/`): `backup-home.timer`, `hyprwhspr.service`, `piper-voz-daemon.service`, `rclone-gdrive.service`, `xremap.service`, `teclas-fantasma.service` (diagnóstico de apagados fantasma de la PC, 22-23 sep; **solo de esta PC**, movido a `solo-esta-pc/`, no va a la laptop). Sistema: `logid` **habilitado y activo** (botones del M720). Sistema: `docker` y `mosquitto` deshabilitados.

---

## 8. Dotfiles copiados (en `~/migracion-cachyos/dotfiles/`, ruta relativa a `$HOME`)

`.config/mpv/` (sin .bak), `.config/fish/`, `.config/kitty/`, `.config/alacritty/` (solo por si acaso; alacritty no se instala), `.config/satty/`, `.config/btop/`, `.config/micro/`, `.config/mimeapps.list`, `.config/brave-flags.conf` (editar, ver 5), `.config/dolphinrc`, `.config/user-dirs.dirs`, `.config/Code/User/settings.json` (no existe `keybindings.json`), `.config/restic/home-excludes.txt` (SIN `home-backup.pass`), `.config/systemd/user/backup-home.{service,timer}`, `.local/bin/backup-home.sh`, `.local/share/applications/*.desktop`, `.local/state/mpv/`, `.claude/settings.json` (no hay `~/.claude/CLAUDE.md`).

Revisado con `grep -iE 'token|password|secret|key'`: sin secretos (la única "api_key" es la clave pública por defecto de OpenSubtitles que trae uosc upstream).

NO copiados a propósito (contienen tokens/credenciales o son perfiles): perfiles de Brave/Firefox, kwallet/gnome-keyring, `~/.config/gh/hosts.yml`, `~/.config/rclone/rclone.conf`, `~/.config/restic/home-backup.pass`, resto de `~/.config/Code/`. Rehacer en la laptop: `gh auth login`, `rclone config`, login en Brave (sync), Claude.

Restaurar: `cp -a ~/migracion-cachyos/dotfiles/. ~/` (revisar antes `brave-flags.conf`), luego `systemctl --user daemon-reload`.
