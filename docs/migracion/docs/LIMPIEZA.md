---
tags: [sistema, limpieza]
actualizado: 2026-09-26
---
# Archivos copiados que no sirven (candidatos a borrar del paquete)

Auditoría del 26-09-2026.

> **Aplicado el 26-09 (verificado antes):** se borraron del paquete las secciones 1, 2, 4 y 5, **excepto** `vconsole.conf`/`locale.conf`/`00-keyboard.conf` (referencia, pesan nada), `i2c-dev.conf` (por si la Arzopa tiene DDC) y `auto-captura-tests.py` (pruebas útiles). De la sección 3 se borraron `install-state.json`, `ultima-velocidad`, `watch_later/` y las carpetas vacías de opendeck; `settings.toml` de Noctalia y lo de gtk-4.0 se quedan. `nwg-monitors.conf` se **movió** a `solo-esta-pc/`. Nada del sistema real se tocó.
Rutas relativas a `~/migracion-cachyos/`.

## 1. Huérfanos (nadie los lee)

| Archivo | Razón |
|---|---|
| `dotfiles/.config/hypr/monitors.conf` | 0 bytes. Resto del formato hyprlang; `hyprland.lua` no lo lee |
| `dotfiles/.config/hypr/workspaces.conf` | 0 bytes. Ídem |
| `dotfiles/.config/hypr/config/nwg-monitors.lua` | Ningún `require` lo carga. Además trae DP-3/HDMI-A-1 de la PC (doc 01 §4.1 #4 ya dice que hay que borrarlo en la laptop) |
| `dotfiles/.config/hypr/config/nwg-monitors.conf` | Sí se usa en la PC, pero en la laptop **hay que borrarlo** (rota la Arzopa 90°). Conviene sacarlo del paquete o renombrarlo a `.pc` |
| `dotfiles/.config/xsettingsd/xsettingsd.conf` | `xsettingsd` no está instalado; nwg-look lo escribe igual |
| `dotfiles/.config/qt5ct/colors/noctalia.conf` | `qt5ct` no está instalado y no hay `qt5ct.conf` |
| `dotfiles/.config/nwg-displays/profiles/` | Carpeta vacía |
| `dotfiles/.config/qt6ct/qss/` | Carpeta vacía |

## 2. Apps que no se instalan en la laptop

| Archivo | Razón |
|---|---|
| `dotfiles/.config/alacritty/` | Alacritty está en DUPLICADO (no se instala); el tema lo regenera Noctalia |
| `dotfiles/.config/solaar/config.yaml` | Solo caché de ajustes del M720 que escribe Solaar; Solaar no corre y es DUDOSO |
| `dotfiles/.config/xremap/config.yml` + `dotfiles/.config/systemd/user/xremap.service` | Config vacía (`modmap: []`, `keymap: []`); doc 03/04 recomiendan no instalar xremap |
| `dotfiles/.config/autostart/cachyos-hello.desktop` | Lanza la bienvenida de CachyOS en cada inicio de sesión; el instalador ya lo crea si hace falta. Copiarlo no aporta |

## 3. Estado runtime / datos generados (no son configuración)

| Archivo | Razón |
|---|---|
| `dotfiles/.local/state/hyprwhspr/install-state.json` | Estado de instalación con hashes de modelos de esta PC; `hyprwhspr setup` lo regenera. Si se copia, hyprwhspr podría creer que el setup ya está hecho sin venv ni modelos |
| `dotfiles/.local/state/mpv/ultima-velocidad` | Estado (1.70); ya desactualizado respecto al original. Se regenera solo |
| `dotfiles/.local/state/mpv/watch_later/` | 1 archivo de posición de reproducción; el original ya tiene 17. Solo sirve si los videos están en la misma ruta |
| `dotfiles/.local/state/noctalia/settings.toml` | Mezcla ajustes con estado de la PC (wallpapers por DP-3/HDMI-A-1, widgets de lockscreen por salida). Útil como referencia, pero no para copiar a ciegas |
| `dotfiles/.config/opendeck/images/**/Keypad.*.0` (32 carpetas vacías de 46) | Carpetas de caché de imágenes que OpenDeck crea en runtime; las vacías no aportan nada |
| `dotfiles/.config/gtk-4.0/thumbnail.png` | Miniatura del tema que copia nwg-look; se regenera |
| `dotfiles/.config/gtk-4.0/assets`, `gtk-dark.css` | Symlinks a `/usr/share/themes/adw-gtk3-dark/...`; nwg-look los recrea (se rompen si falta `adw-gtk-theme`) |

## 4. Duplicados de lo que ya trae un paquete

| Archivo | Razón |
|---|---|
| `dotfiles/.config/micro/syntax/` (146 archivos, 664 KB, incluye `LICENSE`, `README.md`, `make_headers.go`, `syntax_converter.go`) | Copia completa de la carpeta de sintaxis del repo de micro; micro ya las trae integradas. Solo `settings.json` y `colorschemes/` (catppuccin) son del usuario |
| `system/etc/bluetooth/main.conf`, `system/etc/bluetooth/input.conf` | Del paquete `bluez`, **sin modificar** (`pacman -Qkk` no los marca). El doc 03 también dice "por defecto" |
| `system/etc/profile.d/Hyprland.sh` | Del paquete `cachyos-hypr-noctalia`; doc 05 ya dice "no copiar" |
| `system/etc/udev/rules.d/40-streamdeck.rules` | La instala el paquete `opendeck-bin` |
| `system/etc/vconsole.conf`, `system/etc/locale.conf`, `system/etc/X11/xorg.conf.d/00-keyboard.conf` | Los escribe el instalador / `localectl`; doc 05 dice "lo pone el instalador" |
| `system/etc/udev/rules.d/50-bluetooth-no-autosuspend.rules` | Prácticamente vacío (3 bytes); el efecto real lo da `modprobe.d/disable_btusb-autosuspend.conf` |

## 5. Restos de otros usos

| Archivo | Razón |
|---|---|
| `system/etc/udev/rules.d/50-companion-headless.rules` | Resto de Bitfocus Companion (desinstalado) |
| `system/etc/udev/rules.d/70-apple-restore.rules` | Resto de restaurar iPhone/iPad (`idevicerestore-git`, en "NO instalar") |
| `system/etc/modules-load.d/i2c-dev.conf` | Para ddcutil (brillo de monitores externos por DDC); en laptop no hace falta salvo que la Arzopa tenga DDC/CI |
| `dotfiles/.config/hypr/scripts/auto-captura-tests.py` | Pruebas del script de auto-captura; no hace falta para usarlo (se copió para que el paquete esté completo) |

## 6. Ya excluidos correctamente (no están en el paquete, bien)

`hypr/config/backups/`, `hypr/scripts/__pycache__/`, `mpv/input.conf.bak-2026-09-26`, `opendeck/profiles/*/*.bak-*`, symlinks runtime de `hyprwhspr/` (`audio_level`, `recording_*`), `restic/home-backup.pass`, `rclone.conf`, `.git` de hypr y noctalia.

**28-09:** también se dejan en el paquete las demás pruebas del sistema de apuntes (`auto-captura-estres.py`, `cuadernillo-tests.py`, `resumen-corto-tests.py`, `tarjetas-panel-tests.py`, `cola-capturas-tests.sh`, `playlist-a-apuntes-tests.sh`): son la forma de verificar que todo funciona en la laptop. Excluidos a propósito: `Vídeos/.obsidian/workspace.json`, `~/.cache/auto-captura/`, `noctalia/config.toml.bak-*`, `hyprwhspr/config.json.bak-*`, `qt6ct/colors/*.bak`, `qt5ct/` (no instalado) y todo dato de estudio (capturas, apuntes, `Mis cursos.md`).
