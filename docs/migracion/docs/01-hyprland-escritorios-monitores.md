---
tags: [sistema, hyprland]
actualizado: 2026-09-26
---
# 01 · Hyprland: escritorios, monitores, atajos, scripts y tema

> Documento para migrar la config de Hyprland de la PC de escritorio de `yafer`
> (CachyOS, Hyprland **0.56.2** con config en **Lua**, shell/barra **Noctalia**, sesión vía **UWSM**)
> a dos laptops Intel: **Surface Pro 6** (i7-8650U, UHD 620, táctil 2736x1824, 16 GB) y
> **ThinkPad E14 Gen4** (i7 12ª gen, Iris Xe, 16 GB).
> Escrito para que otra instancia de Claude lo entienda **sin contexto previo**.
> Fecha de relevamiento: 2026-09-26.

Los archivos están copiados en `~/migracion-cachyos/dotfiles/` con la misma ruta relativa a `$HOME`.

---

## 0. Hardware de origen (lo que NO existe en las laptops)

| Cosa | PC de escritorio |
|---|---|
| GPU | NVIDIA GTX 980, driver `nvidia-580xx-dkms` + `libva-nvidia-driver` |
| Monitor principal | `DP-3` — ASUS VY279HGR, 1920x1080@60, horizontal, posición `1080x148`, ws 1-5 |
| Monitor secundario | `HDMI-A-1` — HP E24t G4, 1920x1080@60, **rotado 90° (transform 1)**, posición `0x0`, ws 6-10 |
| Teclado | layout `us` (no hay `kb_layout` en la config: es el default de Hyprland) |
| Punteros | Mouse Corsair Scimitar, Logitech M720, receptor 2.4G. Sin touchpad ni táctil |

> Nota: los comentarios de `variables.lua` dicen "yodoit 15.6"", pero `hyprctl monitors` muestra que
> hoy los monitores reales son ASUS (DP-3) y HP (HDMI-A-1). Comentarios desactualizados.

---

## 1. Estructura de archivos y qué hace cada uno

### 1.1 `~/.config/hypr/` (es un repo git: `github.com/yamilfernandotorrezgarciacc-bit/hypr-config`, con muchos cambios sin commitear)

Base: paquete `cachyos-hypr-noctalia` (instala la plantilla en `/etc/skel/.config/hypr/`). El usuario la modificó.

| Archivo | Función |
|---|---|
| `hyprland.lua` | Punto de entrada. Solo hace `require("config.X")` de: animations, autostart, colors, decorations, variables, environment, inputs, binds, misc, monitors, windowrules, workspaces (en ese orden; `variables` va antes de `binds`/`monitors`/`workspaces` porque define globales). |
| `config/variables.lua` | Globales Lua: `TERMINAL=kitty`, `FILE_MANAGER=dolphin`, `BROWSER=brave`, `EDITOR=gnome-text-editor --new-window`, `CALCULATOR=gnome-calculator`, **`MONITOR1="DP-3"`**, **`MONITOR2="HDMI-A-1"`**, `MONITOR3=""`, `PRIMARY_MONITOR=MONITOR1`, **`NUM_WPM=5`** (workspaces por monitor). |
| `config/environment.lua` | `hl.env(...)`: **4 variables NVIDIA activas** (ver §4). |
| `config/monitors.lua` | Lee `config/nwg-monitors.conf` (formato hyprlang `monitor=...` que escribe nwg-displays) con un parser Lua propio y llama `hl.monitor()` por cada salida. Si el archivo no existe, usa un **fallback fijo** (HDMI-A-1 rotado a la izquierda + DP-3 a la derecha). Al final, regla comodín `output=""` → `preferred / auto / scale auto` para cualquier otro monitor. |
| `config/nwg-monitors.conf` | Generado por nwg-displays (15/09/2026): `DP-3 1920x1080@60 1080x148 scale 1`, `HDMI-A-1 1920x1080@60 0x0 scale 1` + `HDMI-A-1,transform,1`. **Es el que realmente se aplica.** |
| `config/nwg-monitors.lua` | Versión Lua de lo mismo generada por nwg-displays. **HUÉRFANO: nadie lo `require`-a.** |
| `config/workspaces.lua` | Reglas de workspace: `name:gaming` y `name:estudio` → `PRIMARY_MONITOR`; ws `1..NUM_WPM` → `MONITOR1` y ws `NUM_WPM+1..2*NUM_WPM` → `MONITOR2`, todos `default=true, persistent=true`. |
| `config/binds.lua` | Todos los atajos + la lógica de "escritorio virtual" (ver §2 y §3.1). |
| `config/windowrules.lua` | Reglas de ventanas (ver §3.2). |
| `config/inputs.lua` | `accel_profile="flat"` global (sin sensibilidad, sin layout, **sin sección touchpad**). Gestos: 4 dedos horizontal = workspace; 3 dedos abajo = cerrar, arriba = fullscreen, izquierda = float. |
| `config/misc.lua` | `dwindle.preserve_split`, sin news/donation nag, `misc.vrr=3`, `enable_swallow` para terminales, `middle_click_paste=false`, `render.direct_scanout=2`, **`xwayland.force_zero_scaling=true`**. |
| `config/decorations.lua` | gaps 2/3, borde 2px con gradiente verde Cachy, rounding 10, **blur size 5 / passes 4** (caro en GPU integrada), `dim_special=0.3`. |
| `config/animations.lua` | Curvas y animaciones por defecto de CachyOS (slide). |
| `config/colors.lua` | Constantes de color `CACHY*`. |
| `config/autostart.lua` | En `hyprland.start`: `dbus-update-activation-environment --systemd --all`, `noctalia`, `xhost +SI:localuser:root`, **`powerprofilesctl set balanced`** (fuerza perfil balanceado — pensado para desktop), `python3 scripts/sesion-ventanas.py`. |
| `monitors.conf`, `workspaces.conf` | **Vacíos (0 bytes). Huérfanos** (restos del formato hyprlang; nadie los lee). |
| `xdph.conf` | xdg-desktop-portal-hyprland: `screencopy.allow_token_by_default = true`. |
| `config/backups/` | Backups `.bak*` (NO copiados). |
| `scripts/` | Ver §3.3. |

### 1.2 Otros archivos del área

| Archivo | Función |
|---|---|
| `~/.config/uwsm/env` | Variables de sesión exportadas por UWSM: `BROWSER=brave`, `TERM=xterm-kitty`, `QT_QPA_PLATFORM="wayland;xcb"`, `QT_QPA_PLATFORMTHEME=qt6ct`, `ELECTRON_OZONE_PLATFORM_HINT=auto`, `HYPRCURSOR_THEME/XCURSOR_THEME=Bibata-Modern-Ice`, `HYPRCURSOR_SIZE/XCURSOR_SIZE=24`. Las líneas NVIDIA están **comentadas** acá (bien). |
| `~/.local/share/applications/nwg-displays.desktop` | Override del lanzador: `nwg-displays -m ~/.config/hypr/config/nwg-monitors.conf -w ~/.config/hypr/config/nwg-workspaces.conf` (el `nwg-workspaces.conf` **no existe** y nadie lo lee). Tiene la ruta `/home/yafer` hardcodeada. |
| `~/.config/nwg-displays/config` | Preferencias de la GUI de nwg-displays. `profiles/` vacío. |
| `~/.config/noctalia/config.toml` | Config de Noctalia (barra/shell): `ui_scale=1.20`, barra auto-hide arriba (launcher, gdrive, reloj, temp, **gpu_temp**, ram · workspaces, ventana activa · media, tray, notificaciones, red, volumen, sesión). **`[brightness] enable_ddcutil=true` + `[brightness.monitor.HDMI-A-1] backend="ddcutil"`**. Capturas → `satty`. Tema desde wallpaper (m3-tonal-spot, dark) y plantillas para btop/gtk3/gtk4/kcolorscheme/kitty/qt/alacritty. **No hay widget de batería.** |
| `~/.config/noctalia/palettes/luffy-oscuro-sft.json` | Paleta propia. |
| `~/.config/noctalia/templates/noctwhspr-mic-osd.css` | Plantilla que Noctalia renderiza a `~/.config/hyprwhspr/theme/mic-osd.css` (dictado). |
| `~/.local/state/noctalia/settings.toml` | Estado/ajustes hechos desde la GUI de Noctalia: dock (auto_hide, pinned), lockscreen widgets **por salida** (DP-2, DP-3, HDMI-A-1, FALLBACK), plugin `goodroot/noctwhspr`, tema, **wallpapers por monitor (`DP-3`, `HDMI-A-1`)** con rutas en `~/Imágenes/Wallpapers/...`. |
| `~/.local/share/noctalia/plugins/noctwhspr/` | Plugin de barra para hyprwhspr (dictado). |
| `~/.config/autostart/` | XDG autostart (UWSM los lanza): `opendeck.desktop` (`/usr/bin/opendeck --hide`, Stream Deck) y `cachyos-hello.desktop`. |
| `~/.config/systemd/user/piper-voz-daemon.service` | Daemon de Piper (TTS) usado por SUPER+R. `WantedBy=graphical-session.target`. |
| Tema GTK | `gtk-3.0/settings.ini`, `gtk-4.0/settings.ini`, `~/.gtkrc-2.0`, `xsettingsd/xsettingsd.conf` (escritos por **nwg-look**): tema `adw-gtk3-dark`, iconos `Adwaita`, fuente `Adwaita Sans 11`, cursor `Bibata-Modern-Ice` **tamaño 30** (≠ 24 de uwsm/env). `gtk.css` importa `noctalia.css` (generado por Noctalia). `gtk-4.0/assets` y `gtk-dark.css` son **symlinks** a `/usr/share/themes/adw-gtk3-dark/...` (requieren `adw-gtk-theme`). `gtk-4.0/gtk.css` también importa `libadwaita.css`/`libadwaita-tweaks.css` que **no existen** (inofensivo). |
| `~/.config/nwg-look/config` | Opciones de export de nwg-look. |
| Qt | `qt6ct/qt6ct.conf` (estilo Fusion, paleta `colors/noctalia.conf`, iconos `breeze`, diálogos gtk3). `qt5ct/colors/noctalia.conf` existe pero **qt5ct no está instalado** ni hay `qt5ct.conf`. |
| `~/.config/kdeglobals` | Esquema de color "Noctalia" (generado por Noctalia) para apps KDE (Dolphin). `TerminalApplication=kitty`. |
| Cursor | `~/.local/share/icons/Bibata-Modern-Ice/` (28 MB, **instalado a mano, no por paquete**; solo formato xcursor) + `~/.icons/default/index.theme` (`Inherits=Bibata-Modern-Ice`). Copiados. |
| Fuentes | No hay fuentes de usuario (`~/.local/share/fonts` no existe). Todo por paquetes (§5). |

`xsettingsd` **no está instalado**, así que `xsettingsd.conf` no se usa (lo escribe nwg-look igual).

---

## 2. Tabla completa de atajos (`config/binds.lua`)

`mainMod = SUPER`. `launchPrefix = "uwsm app -- "`. `noctCall = "noctalia msg "`. `N` = 1..5.

### 2.1 Ventanas
| Tecla | Acción |
|---|---|
| SUPER+Q | Cerrar ventana |
| SUPER+ALT+Space | Alternar flotante |
| SUPER+D | Fullscreen modo 1 (maximizar, mantiene barra/gaps) |
| SUPER+F | Fullscreen real |
| SUPER+J | `togglesplit` (dwindle) |
| SUPER+←/→/↑/↓ | Mover foco en esa dirección |
| ALT+Tab | Siguiente ventana (`cycle_next`) |
| SUPER+Tab | Cicla entre ventanas del **escritorio virtual actual** en todos los monitores (función Lua `cycleVirtualDesktopWindows`) |
| SUPER+SHIFT+←/→/↑/↓ | Mover ventana en esa dirección |
| SUPER+SHIFT+1 | Mover ventana a `MONITOR1` |
| SUPER+SHIFT+2 | Mover ventana a `MONITOR2` |
| SUPER+CTRL+SHIFT+→ / ← | Mover ventana al workspace siguiente/anterior del monitor (`m+1` / `m-1`) |
| SUPER+CTRL+N | Mover ventana al workspace N **relativo al monitor** (`m~N`). Sirve para sacar ventanas del special |
| SUPER+clic izq (arrastrar) | Mover ventana |
| SUPER+clic der (arrastrar) | Redimensionar |
| SUPER+Minus / SUPER+Plus | Zoom de cursor −0.3 / +0.3 (1.0–3.0), repetible |

### 2.2 Lanzadores y apps
| Tecla | Acción |
|---|---|
| SUPER+Return | kitty |
| SUPER+E | dolphin |
| SUPER+W | brave |
| SUPER+N ("N" letra) | obsidian |
| XF86Calculator | gnome-calculator |
| SUPER+G | VS Code (enfocar-o-abrir, ws 4) — `app-web.sh code` |
| SUPER+T | TikTok (ws 1) — `app-web.sh tiktok` |
| SUPER+ALT+Q | YouTube (escritorio actual) — `app-web.sh youtube` |
| SUPER+ALT+W | WhatsApp Web (ws 6) |
| SUPER+ALT+T | Telegram Web (ws 6) |
| SUPER+ALT+F | Facebook (ws 1) |
| SUPER+ALT+I | Instagram (ws 1) |
| SUPER+ALT+D | Google Drive (ws 8) |
| SUPER+K | opendeck (config del Stream Deck) |
| CTRL+SHIFT+Escape | kitty -e btop |
| CTRL+ALT+Escape | `matar-libreoffice.sh` (SIGKILL a soffice.bin) |
| SUPER+C | `curso-abrir.sh` (sesión de estudio en ws `name:estudio`) |
| SUPER+ALT+C | `curso-configurar.sh` (zenity: configurar los 4 slots) |

### 2.3 Noctalia (shell)
| Tecla | Acción |
|---|---|
| SUPER (tap y soltar, bind `release` sobre `Super_L`) | Launcher (`panel-toggle launcher`) |
| SUPER+period | Selector de emojis (`launcher /emo`) |
| SUPER+Z | Ajustes de Noctalia |
| SUPER+X | Centro de control |
| SUPER+A | Centro de control → notificaciones |
| SUPER+V | Historial del portapapeles |
| SUPER+L | Bloquear sesión |

### 2.4 Hardware (todas `locked`, funcionan con pantalla bloqueada)
| Tecla | Acción |
|---|---|
| XF86AudioRaiseVolume / LowerVolume | `noctalia msg volume-up/down` (repetible) |
| XF86AudioMute / XF86AudioMicMute | mute salida / micrófono |
| XF86AudioPlay / Pause | `media toggle` |
| XF86AudioNext / Prev | `media next/previous` |
| XF86MonBrightnessUp / Down | `noctalia msg brightness-up/down` (repetible) — **en laptop controla la pantalla interna vía backlight** |

### 2.5 Capturas, portapapeles, voz
| Tecla | Acción |
|---|---|
| Print | Captura de región (Noctalia → satty) |
| SUPER+Print | Captura pantalla completa (Noctalia → satty) |
| SUPER+SHIFT+S | `captura-portapapeles.sh` (región → solo portapapeles) |
| CTRL+SHIFT+S | `captura-guardar.sh` (región → archivo en carpeta configurada + portapapeles) |
| CTRL+SHIFT+D | `elegir-carpeta-capturas.sh` (zenity) |
| SUPER+ALT+S | `auto-captura-toggle.sh` (activa/desactiva la auto-captura del monitor con foco; agregado 26-09-2026 por la tarde) |
| SUPER+R | `leer-seleccion.sh` (lee en voz alta la selección; repetir = cortar) |
| SUPER+ALT+R | `actualizar-voz.sh` → `elegir-voz.py` (GTK4: motor/voz/velocidad) |

### 2.6 Workspaces y monitores
| Tecla | Acción |
|---|---|
| SUPER+1..5 | **Escritorio virtual N**: pone ws N en MONITOR1 y ws N+5 en MONITOR2 a la vez (`switchVirtualDesktop`) |
| SUPER+CTRL+→ / ← | Escritorio virtual siguiente/anterior (cíclico 1..5). **El Stream Deck simula estas teclas, no cambiarlas** |
| SUPER+rueda abajo / arriba | Escritorio virtual anterior / siguiente |
| SUPER+ALT+1 / SUPER+ALT+2 | Enfocar MONITOR1 / MONITOR2 |
| SUPER+ALT+E | Ir a `name:estudio` |
| SUPER+S | Mostrar/ocultar special workspace (scratchpad). No hay atajo para *enviar* ventanas al special |

Teclas libres notables (quitadas a propósito): SUPER+Escape, SUPER+P, SUPER+SHIFT+W, SUPER+SHIFT+3, SUPER+Space.

---

## 3. Escritorios, reglas y scripts

### 3.1 Modelo de "escritorio virtual"
- `NUM_WPM=5`. `monitorSlots = { MONITOR1, MONITOR2, MONITOR3 }`.
- Slot `s` (1-based) usa los workspaces `(s-1)*5 + 1 .. (s-1)*5 + 5`. O sea DP-3 = 1..5, HDMI-A-1 = 6..10.
- Escritorio virtual `i` = ws `i` en MONITOR1 + ws `i+5` en MONITOR2. `switchVirtualDesktop(i)` recorre los slots, y para cada salida que `hl.get_monitor(output)` encuentre, llama `mon:set_workspace({workspace = (slot-1)*5 + i})`. **Si el monitor no existe, simplemente lo salta** (no rompe con 1 monitor, pero los ws 6-10 quedan inalcanzables por SUPER+N).
- `currentVirtualDesktopIndex()` deduce `i` del ws activo del monitor enfocado **comparando su nombre con MONITOR1/MONITOR2** → si el monitor enfocado se llama distinto (p. ej. `eDP-1` sin cambiar variables) devuelve siempre 1.
- La misma aritmética (`NUM_WPM=5`, `ws+5`) está **duplicada a mano** en `scripts/app-web.sh` y en los comentarios de `windowrules.lua`.
- Workspaces con nombre: `name:gaming` (reglas de Steam, pero Steam no está instalado) y `name:estudio` (SUPER+C / SUPER+ALT+E).
- Asignaciones fijas (windowrules): ws1 = redes (Facebook/Instagram/TikTok), ws6 = chats (WhatsApp/Telegram), ws8 = Drive, ws4 = VS Code. YouTube libre.

### 3.2 Reglas de ventana (`config/windowrules.lua`)
- Flotantes: centradas y `persistent_size`.
- Picture-in-Picture: flotante, pin, 25% del monitor, mantiene aspecto.
- Gaming (`steam_app*`, `gamescope`, tag/content game) → `name:gaming`, fullscreen.
- `*.exe` flotantes y `*launcher*` → `PRIMARY_MONITOR`; `vesktop|discord` → `PRIMARY_MONITOR`.
- Calculadoras flotantes (tamaño relativo), `keditfiletype` flotante, `ark` 40%, `satty` flotante (min 35%), ajustes de Noctalia flotante 70%.
- **Escritorios fijos** (tabla `escritoriosFijos`): clases `brave-www.(facebook|instagram|tiktok).com__*` → "1"; `brave-web.(whatsapp.com|telegram.org)__*` → "6"; `brave-drive.google.com__*` → "8"; `code|Code|code-oss` → "4".
- Opacidad 1.0 override: firefox/zen, terminales, mpv/haruna/plex/gwenview/vlc.
- Flotantes utilitarios: kvantum/qt5ct/qt6ct/nwg-look, pavucontrol/blueman/nm-applet/nm-connection-editor, winetricks/protontricks.
- Modales comunes flotantes (Open, Save As, portal-gtk, *dialog*, hyprland-share-picker…).
- `suppress_event = "maximize"` para todas; fix de drags XWayland (`no_focus`).

### 3.3 Scripts (`~/.config/hypr/scripts/`)

| Script | Quién lo llama | Qué hace | Dependencias |
|---|---|---|---|
| `app-web.sh <app>` | binds SUPER+T/G, SUPER+ALT+Q/W/T/F/I/D | Enfocar-o-abrir apps web como ventanas `brave --app=URL` (clase `brave-<dominio>__-Default`) o VS Code. Si la app tiene ws fijo, muestra el escritorio virtual correspondiente (enfoca ws i+5 y luego ws i) y enfoca/abre. YouTube: busca en el escritorio actual o abre ahí. **`NUM_WPM=5` hardcodeado**. Usa `hyprctl dispatch 'hl.dsp....'` (sintaxis Lua). | brave-bin, visual-studio-code-bin, jq, hyprland, util-linux (setsid) |
| `sesion-ventanas.py` | autostart.lua | Daemon: cada 2 s lee `hyprctl clients -j`, guarda cada 20 s la distribución en `~/.local/state/hypr-sesion/actual.json`, y cuando reaparece una ventana normal de Brave (`brave-browser`) la devuelve a su workspace anterior (match por título exacto o similar ≥0.6). Log en `movimientos.log`. Mueve con `hl.dsp.window.move({workspace=..., window="address:...", follow=false})`. | python, hyprland, brave |
| `leer-seleccion.sh` | SUPER+R | TTS de la selección primaria; en apps Chromium/Electron simula Ctrl+C con **ydotool** (fallback wtype) y restaura el portapapeles. Limpia el texto (`limpiar-texto.py` + sed/awk). Motores: `edge` (online, cae a Piper), `chatterbox` (venv en `~/.local/share/piper-voz/chatterbox-venv`), `piper` (vía daemon por socket `~/.cache/piper-voz.sock` o `piper-tts` directo). | wl-clipboard, jq, ydotool (+ servicio `ydotoold` y acceso a `/dev/uinput`), wtype, libnotify, piper-tts, piper-voices-es-ar, pipewire-audio (pw-play), ffmpeg (ffplay), libpulse (paplay), `edge-tts` (**pipx**, symlink en `~/.local/bin`, no paquete), python |
| `limpiar-texto.py` | leer-seleccion.sh | Quita emojis, cambia URLs/rutas por "este enlace"/"esta ruta". | python |
| `piper-daemon.py` / `piper-client.py` | `piper-voz-daemon.service` / leer-seleccion.sh | Daemon que mantiene los modelos Piper en RAM; cliente por socket Unix. | python, piper-tts |
| `chatterbox-hablar.py` | leer-seleccion.sh (motor chatterbox) | TTS Chatterbox multilingüe. | venv propio con `chatterbox`, `soundfile` (pesado; en laptop sin GPU NVIDIA será muy lento → mejor no migrarlo) |
| `actualizar-voz.sh` → `elegir-voz.py` | SUPER+ALT+R | Ventana GTK4/libadwaita para elegir motor/voz/velocidad → escribe `voz.conf`. | python-gobject, gtk4, libadwaita |
| `voz.conf` | datos | `ENGINE=piper`, voz `es_AR-daniela-high`, `SPEED_MULT=1.3`. | — |
| `captura-portapapeles.sh` | SUPER+SHIFT+S | slurp → grim → wl-copy. | grim, slurp, wl-clipboard, libnotify |
| `captura-guardar.sh` | CTRL+SHIFT+S | slurp → grim a `$(cat carpeta-capturas.conf)` o `~/Imágenes/Capturas` + wl-copy. | ídem |
| `elegir-carpeta-capturas.sh` | CTRL+SHIFT+D | zenity para elegir carpeta → `carpeta-capturas.conf`. | zenity |
| `carpeta-capturas.conf` | datos | Hoy apunta a `/run/media/yafer/SuperYafer/paola_v` (**disco externo**; en la laptop puede no existir → `mkdir -p` lo crearía en /run/media, conviene resetearlo a `~/Imágenes/Capturas`). | — |
| `curso-abrir.sh` | SUPER+C | Abre los 4 slots de `curso.conf` (URL → `brave --new-window`, ruta → xdg-open, o comando con `eval`) tras ir a `name:estudio`. **Usa `hyprctl dispatch workspace name:estudio` (sintaxis vieja, no Lua) → probablemente no cambia de workspace** con Hyprland 0.56 Lua. Debería ser `hyprctl dispatch 'hl.dsp.focus({ workspace = "name:estudio" })'`. | brave, xdg-utils, libnotify |
| `curso-configurar.sh` | SUPER+ALT+C | Formulario zenity → `curso.conf`. | zenity |
| `curso.conf` | datos | URLs de YouTube y Google Docs del curso actual. | — |
| `matar-libreoffice.sh` | CTRL+ALT+Escape | `pkill -9 -f soffice.bin`. | procps-ng, libnotify |
| `vscode-open-md.sh <archivo>` | **Stream Deck** (opendeck) | Abre un .md en VS Code y mueve la ventana al ws actual. Usa `hl.dsp.window.move({ workspace = N, address = "..." })` — **inconsistente** con los otros scripts, que usan `window = "address:..."`; posiblemente mueve la ventana activa en vez de la de Code. Verificar. | visual-studio-code-bin, python |
| `pomodoro-toggle.sh` | **Stream Deck** | Timer de 25 min con notificaciones. | libnotify |
| `auto-captura-toggle.sh` → `auto-captura.py` | SUPER+ALT+S | Toggle (PID en `/tmp/auto-captura.pid`): captura con `grim -o <monitor con foco>` cada `INTERVALO` s y guarda PNG solo cuando la pantalla cambió (bloques de 32 px, espera pantalla quieta, tope). Carpeta: `carpeta-capturas.conf` o `~/Imágenes/Capturas`, subcarpeta `auto_<fecha>_<título>`. Ajustes en `auto-captura.conf`. `auto-captura-tests.py` = pruebas. | grim, python-numpy, python-pillow, libnotify, hyprland |
| `video-a-capturas.sh <url\|archivo>` | manual | Mismo algoritmo sobre un video (YouTube vía yt-dlp, o archivo local) sin reproducirlo; `auto-captura.py --video`. | yt-dlp, ffmpeg, python-numpy, python-pillow |
| `watch-monitors.sh` | **nadie** (manual) | `inotifywait` sobre `config/` y `hyprctl reload` cuando nwg-displays reescribe `nwg-monitors.conf`. No está en autostart. | inotify-tools |

Servicios relacionados (fuera de `hypr/`, otros documentos): `ydotool` (necesario para SUPER+R), `hyprwhspr.service` (dictado), `xremap.service`, `teclas-fantasma.service`.

---

## 4. ⚠️ SECCIÓN CRÍTICA: qué cambia en una laptop

### 4.1 Inventario de todo lo que depende de esta PC

| # | Dónde | Qué | Impacto en laptop |
|---|---|---|---|
| 1 | `config/environment.lua` líneas 8-11 | `GBM_BACKEND=nvidia-drm`, `__GLX_VENDOR_LIBRARY_NAME=nvidia`, `LIBVA_DRIVER_NAME=nvidia`, `NVD_BACKEND=direct` | **Rompe** GL/VA-API en Intel (Hyprland puede no arrancar o no haber aceleración de video). **QUITAR/comentar las 4.** Opcional: `hl.env("LIBVA_DRIVER_NAME", "iHD")` (no hace falta, se autodetecta). `/etc/profile.d/Hyprland.sh` ya solo exporta GBM_BACKEND si hay nvidia sin i915, así que no molesta. |
| 2 | `config/variables.lua` líneas 10-11 | `MONITOR1="DP-3"`, `MONITOR2="HDMI-A-1"` | Con nombres inexistentes: SUPER+1..5 no hace nada, SUPER+Tab y SUPER+CTRL+←/→ fallan (índice siempre 1), SUPER+ALT+1/2 y SUPER+SHIFT+1/2 no hacen nada, las reglas de workspace no aplican. |
| 3 | `config/nwg-monitors.conf` (y fallback en `config/monitors.lua` líneas 67-82) | `HDMI-A-1` con **transform 1 (rotado)** en `0x0`, DP-3 en `1080x148` | **Peligro real**: en la ThinkPad la Arzopa por HDMI se llamará casi seguro `HDMI-A-1` → aparecería **rotada 90°**. **Borrar `nwg-monitors.conf` en la laptop** (y reescribir el fallback de `monitors.lua`). |
| 4 | `config/nwg-monitors.lua` | Huérfano con DP-3/HDMI-A-1 | Borrar (no se usa). |
| 5 | `config/workspaces.lua` líneas 7-15 | ws 1-5 → MONITOR1, ws 6-10 → MONITOR2 | Necesita lógica para MONITOR2 ausente (ver §4.2). |
| 6 | `config/binds.lua` líneas 157-244 | `monitorSlots`, `switchVirtualDesktop`, `currentVirtualDesktopIndex`, `cycleVirtualDesktopWindows`, SUPER+ALT+1/2, SUPER+SHIFT+1/2 | Dependen de nombres fijos. Ver §4.2. |
| 7 | `scripts/app-web.sh` línea 11 y 28-32 | `NUM_WPM=5` y `ir_a_escritorio` (enfoca ws i+5 y luego ws i) | Con 1 monitor: abrir WhatsApp deja al usuario en ws 1 mientras la ventana nace en ws 6 (invisible). Ver §4.2. |
| 8 | `config/windowrules.lua` líneas 61-66 | ws "6" chats, "8" Drive | Con 1 monitor esos ws existen en eDP-1 pero no se ven junto al ws 1/3. |
| 9 | `scripts/watch-monitors.sh` | Recarga al cambiar nwg-monitors.conf | No se usa; en laptop puede servir si se usa nwg-displays, pero con la propuesta §4.2 (eventos `monitor.added/removed`) sobra. |
| 10 | `config/autostart.lua` línea 9 | `powerprofilesctl set balanced` al iniciar | En laptop **quitar**: deja que power-profiles-daemon/Noctalia elijan (power-saver en batería). |
| 11 | `config/inputs.lua` | `accel_profile="flat"` global, sin `touchpad {}`, sin `kb_layout` | Touchpad sin tap-to-click ni natural scroll y con aceleración plana (se siente mal). Ver §4.4. |
| 12 | `config/misc.lua` línea 22 | `xwayland.force_zero_scaling = true` | Con escala 2 en la Surface, apps XWayland se verán diminutas salvo que se escalen solas. Ver §4.3. |
| 13 | `config/decorations.lua` líneas 38-42 | blur size 5 / passes 4 | Caro en UHD 620 → batería/lag. Sugerido `passes = 2`. |
| 14 | `~/.config/noctalia/config.toml` | `[brightness.monitor.HDMI-A-1] backend = "ddcutil"`; widget `sysmon_2` con `stat = "gpu_temp"`; sin widget `battery` | Quitar el bloque `brightness.monitor.HDMI-A-1` (la Arzopa por HDMI heredaría ddcutil; el brillo interno va por backlight/brightnessctl). Cambiar `gpu_temp` por temperatura de CPU. **Agregar `"battery"`** a `end` de la barra. |
| 15 | `~/.local/state/noctalia/settings.toml` | `wallpaper.monitors.DP-3` / `HDMI-A-1`, lockscreen widgets por DP-2/DP-3/HDMI-A-1 | eDP-1 no tiene wallpaper asignado (cae al default/last). Elegir wallpaper desde Noctalia en la laptop; las entradas viejas son inofensivas. |
| 16 | `~/.config/brave-flags.conf` (otra área) | `VaapiOnNvidiaGPUs`, `VaapiIgnoreDriverChecks` | Quitar `VaapiOnNvidiaGPUs`; en Intel basta `AcceleratedVideoDecodeLinuxGL`. |
| 17 | `~/.config/mpv/mpv.conf` líneas 12-13 (otra área) | `vo=gpu-next`, `hwdec=auto-safe` | **Sirve tal cual en Intel** (usará VA-API con `intel-media-driver`). No cambiar; solo instalar el driver VA-API de Intel. |
| 18 | `scripts/carpeta-capturas.conf` | `/run/media/yafer/SuperYafer/paola_v` | Resetear a `~/Imágenes/Capturas` si el disco no está. |
| 19 | Paquetes | `nvidia-580xx-*`, `lib32-nvidia-580xx-utils`, `opencl-nvidia-580xx`, `libva-nvidia-driver`, `linux-firmware-nvidia` | No instalar en laptops. Instalar `intel-media-driver`, `vulkan-intel`, `lib32-vulkan-intel` (si hay Steam/juegos). |
| 20 | Cursor | GTK usa tamaño 30, uwsm/env 24 | Unificar (p. ej. 24) — en la Surface la escala de Hyprland ya lo agranda. |

### 4.2 Propuesta de comportamiento de monitores y escritorios (NO implementado)

**Objetivo**
- **Solo eDP-1**: SUPER+1..5 cambia el ws 1..5 en eDP-1. Los ws 6..10 (la "cara secundaria" de cada escritorio: chats en 6, Drive en 8) viven también en eDP-1 y se llega a ellos con un atajo de "voltear" el escritorio virtual.
- **eDP-1 + Arzopa**: se comporta como la PC: eDP-1 = ws 1..5 (principal), Arzopa = ws 6..10; SUPER+N cambia ambos.
- Conectar/desconectar la Arzopa en caliente reubica los ws 6-10 sin recargar a mano.

**Cambios concretos propuestos**

1. `config/variables.lua` líneas 10-12:
   ```lua
   MONITOR1 = "eDP-1"   -- pantalla interna (siempre)
   MONITOR2 = ""        -- se resuelve en runtime: el primer monitor que NO sea eDP-1 (Arzopa)
   MONITOR3 = ""
   PRIMARY_MONITOR = MONITOR1
   -- Función global: devuelve el nombre del monitor secundario actual o nil
   function secondaryMonitor()
       for _, m in ipairs(hl.get_monitors()) do
           if m.name ~= MONITOR1 then return m.name end
       end
       return nil
   end
   ```
   (Alternativa más robusta si hay varios externos: matchear por descripción EDID de la Arzopa. Obtenerla conectándola y corriendo `hyprctl monitors` → campo `description:`; los nombres de salida cambian según puerto: USB-C suele ser `DP-1`/`DP-2`, HDMI en la ThinkPad `HDMI-A-1`.)
   Verificar los nombres de campos de `hl.get_monitors()` (se confirmó que la función existe en 0.56.2 vía `strings`; `binds.lua` ya usa `mon.name` y `mon.active_workspace.id` en objetos de monitor).

2. `config/binds.lua`:
   - Línea 157: reemplazar la tabla fija por una función `local function slots() return { MONITOR1, secondaryMonitor() or "" } end` y usar `slots()` dentro de `switchVirtualDesktop`, `currentVirtualDesktopIndex` y `cycleVirtualDesktopWindows` (líneas 157, 170, 192).
   - `currentVirtualDesktopIndex` (170-180): si el ws activo es 6..10 en eDP-1 (modo 1 monitor), devolver `id - NUM_WPM` (hoy devolvería 1 porque solo compara con el rango del slot 1).
   - Nuevo atajo "voltear escritorio" solo útil con 1 monitor, p. ej. `SUPER+grave` (tecla `` ` ``, libre) o `SUPER+ALT+Tab`: si el ws activo de eDP-1 es `i` → ir a `i+5`; si es `i+5` → ir a `i`. Con Arzopa conectada, podría simplemente enfocar el otro monitor.
   - SUPER+ALT+2 / SUPER+SHIFT+2 (líneas 218 y 34): que usen `secondaryMonitor()` en una función en vez de la constante `MONITOR2` (si es nil, no hacer nada).
   - `cycleVirtualDesktopWindows` con 1 monitor: incluir ws `i` e `i+5` (ya lo hace si se pasan los dos slots; al enfocar una ventana del ws `i+5` Hyprland salta a ese ws, aceptable).

3. `config/workspaces.lua` líneas 12-14: las reglas `monitor = MONITOR2` no sirven con MONITOR2 dinámico. Opciones:
   - (a) Quitar `monitor=` de los ws 6-10 (quedan `persistent=true` sin monitor → se crean en el monitor activo = eDP-1), y mover los ws en runtime con eventos (punto 4).
   - (b) Si se usa descripción fija de la Arzopa: `monitor = "desc:<descripción Arzopa>"` (Hyprland acepta `desc:` en reglas de workspace); si la Arzopa no está, Hyprland los pone en eDP-1.

4. Nuevo bloque en `config/monitors.lua` (o un archivo nuevo `config/hotplug.lua` requerido desde `hyprland.lua`): eventos Lua (confirmados en el binario: `monitor.added`, `monitor.removed`, `workspace.move_to_monitor`):
   ```lua
   local function redistribuir()
       local sec = secondaryMonitor()
       for i = NUM_WPM + 1, 2 * NUM_WPM do
           -- mover ws i a sec si existe, si no a MONITOR1
           hl.dispatch(hl.dsp.workspace.move_to_monitor({ workspace = tostring(i), monitor = sec or MONITOR1 }))  -- VERIFICAR nombre exacto del dispatcher en la wiki Lua
       end
   end
   hl.on("monitor.added", redistribuir)
   hl.on("monitor.removed", redistribuir)
   hl.on("hyprland.start", redistribuir)
   ```
   El nombre exacto del dispatcher (`moveworkspacetomonitor` en la sintaxis vieja) hay que verificarlo en https://wiki.hypr.land (Configuring → Dispatchers, versión Lua). **No usar `hyprctl dispatch` para probar sin saber la sintaxis Lua.**

5. `config/monitors.lua`:
   - `config/nwg-monitors.conf` y `nwg-monitors.lua` **ya se sacaron del paquete** (26-09; el .conf quedó en `solo-esta-pc/`). Sin ese archivo, `monitors.lua` usa el fallback.
   - Reescribir el fallback (líneas 64-83) por:
     ```lua
     -- Surface Pro 6: 2736x1824, escala 2 (o 1.6 / 1.9, ver §4.3)
     hl.monitor({ output = "eDP-1", mode = "preferred", position = "0x0", scale = 2 })
     -- ThinkPad E14 Gen4 (1920x1080 14"): scale 1 o 1.25
     -- Arzopa / cualquier externo: arriba de la interna o a la derecha
     hl.monitor({ output = "", mode = "preferred", position = "auto-right", scale = 1 })
     ```
     (La regla comodín `output = ""` de las líneas 85-90 ya existe; cambiar `position="auto"` por `"auto-right"` o `"auto-up"` según dónde se apoye la Arzopa, y `scale="auto"` por `1`, porque `auto` puede elegir 1.5/2 en la Arzopa FHD.)
   - Mantener el parser de nwg-displays: si en la laptop se usa nwg-displays, volverá a crear `nwg-monitors.conf` con los nombres correctos. Ojo: nwg-displays guarda posiciones por nombre de salida, así que la Arzopa por USB-C (`DP-x`) y por HDMI (`HDMI-A-1`) son entradas distintas.
   - Opcional (cerrar la tapa con Arzopa conectada): bindings de switch en `binds.lua`:
     `hl.bind("switch:on:Lid Switch", <deshabilitar eDP-1>, { locked = true })` / `switch:off` para rehabilitar — verificar sintaxis Lua de `bindl` + `hl.monitor({output="eDP-1", disabled=true})`. Si se deshabilita eDP-1, `secondaryMonitor()` pasa a ser el único y los ws 1-5 migran solos.

6. `scripts/app-web.sh`:
   - Línea 11: en vez de `NUM_WPM=5` fijo está bien dejarlo, pero `ir_a_escritorio` (28-32) debe detectar cuántos monitores hay: `n=$(hyprctl monitors -j | jq length)`. Si `n == 1`: enfocar directamente el ws destino (`$ws`, p. ej. 6 para WhatsApp) en vez de "ws i+5 y luego ws i". Si `n >= 2`: comportamiento actual.
   - YouTube (rama `else`, 57-66) funciona igual en ambos modos.

7. `config/windowrules.lua` líneas 61-66: no hace falta cambiar nada (ws 6 y 8 siguen siendo "cara secundaria"). Solo actualizar el comentario de la línea 58.

### 4.3 Escalado (Surface Pro 6: 2736x1824, 12.3", ~267 ppi)

- Hyprland exige que `ancho/escala` y `alto/escala` den enteros (si no, avisa "invalid scale" y elige otra). Para 2736x1824:
  - `2` → 1368x912 lógicos ✅ (lo más nítido y seguro)
  - `1.9` → 1440x960 ✅
  - `1.6` → 1710x1140 ✅
  - `1.5` → 1824x1216 ✅
  - `1.75` → 1563.4x1042.3 ❌ **no válido**, evitarlo.
  - Recomendación: empezar con **2**; si se ve grande, **1.6**.
- ThinkPad E14 Gen4 (1920x1080 14"): `1` o `1.25` (1536x864 ✅).
- Arzopa (normalmente 1920x1080 15.6"): `1`.
- `misc.lua` línea 22 `force_zero_scaling = true`: con escala fraccional/2, las apps XWayland se dibujan a escala 1 (nítidas pero chicas). Si molesta en la Surface, agregar en `~/.config/uwsm/env`: `export GDK_SCALE=2` (solo afecta GTK en XWayland) o quitar `force_zero_scaling` (se ven borrosas pero de tamaño correcto). La mayoría de las apps del usuario (Brave, VS Code, kitty, Dolphin, Obsidian) corren nativas en Wayland (`ELECTRON_OZONE_PLATFORM_HINT=auto`, `--ozone-platform-hint=auto`), así que el impacto es menor.
- Noctalia: `config.toml` `ui_scale = 1.20` y `bar.default.scale = 1.10`. Noctalia ya escala con el monitor; en la Surface probar `ui_scale = 1.0`.
- Cursor: dejar `HYPRCURSOR_SIZE/XCURSOR_SIZE=24` y poner `gtk-cursor-theme-size=24` en gtk-3.0/gtk-4.0 (hoy 30); Hyprland lo multiplica por la escala.

### 4.4 Touchpad, táctil y gestos (NO implementado)

`config/inputs.lua` — propuesta de bloque (reemplaza líneas 3-12):
```lua
hl.config({
    input = {
        kb_layout = "us",            -- VERIFICAR teclado físico: ThinkPad latam = "latam", Type Cover US = "us"
        accel_profile = "flat",      -- solo mouse; el touchpad usa su propio perfil abajo
        touchpad = {
            natural_scroll = true,
            tap_to_click = true,     -- VERIFICAR nombre exacto de la clave en 0.56 (en hyprlang era "tap-to-click")
            disable_while_typing = true,
            clickfinger_behavior = true,   -- 2 dedos = clic derecho, 3 = medio
            scroll_factor = 0.5,
        },
    },
    gestures = {
        workspace_swipe_touch = true,      -- swipe de workspace también en la pantalla táctil (Surface)
        workspace_swipe_create_new = false,
    },
})
-- Per-device: aceleración adaptativa solo para el touchpad
-- hl.device({ name = "<nombre de hyprctl devices>", accel_profile = "adaptive" })  -- VERIFICAR API
```
- Claves confirmadas en el binario 0.56.2: `input:touchpad:disable_while_typing`, `input:touchpad:clickfinger_behavior`, `input:natural_scroll`, `gestures:workspace_swipe_touch`, `gestures:workspace_swipe_invert`, `gestures:workspace_swipe_create_new`, `gestures:workspace_swipe_forever`.
- **Problema del gesto actual**: `hl.gesture({fingers=4, direction="horizontal", action="workspace"})` (línea 14) recorre ws consecutivos del monitor. Con 1 monitor recorrería 1→2→…→10, mezclando la "cara secundaria". Propuesta: si `hl.gesture` acepta una función/dispatcher como acción, usar `switchVirtualDesktopRelative(±1)` (habría que exportarla como global desde binds.lua); si no, dejar el gesto y aceptar el comportamiento, o limitarlo con reglas. Los gestos de 3 dedos (cerrar/fullscreen/float) son peligrosos en un touchpad chico: **3 dedos abajo = cerrar ventana** se dispara fácil; considerar pasar "close" a 4 dedos abajo.
- Surface Pro 6: el táctil y el lápiz normalmente requieren el kernel **linux-surface** + `iptsd` (fuera de esta área; ver doc de sistema). Opcionales para uso tablet: `hyprgrass` (plugin de gestos táctiles; no hay paquete estable: AUR `hyprgrass-git` o `hyprpm add`), teclado en pantalla (`squeekboard` repo o `wvkbd` AUR), rotación automática (`iio-sensor-proxy` repo + `iio-hyprland-git` AUR).
- ThinkPad: teclas Fn de brillo/volumen ya están mapeadas (XF86*). Micrófono mute (XF86AudioMicMute) también.

### 4.5 Energía / idle (faltante)
- No hay `hypridle` ni `hyprlock` instalados; el bloqueo lo hace Noctalia (`SUPER+L`, `noctalia msg session lock`) y la acción "lock_and_suspend" del menú. **Verificar en la laptop que Noctalia tenga configurado idle → apagar pantalla → suspender** (en ajustes de Noctalia); si no, instalar `hypridle`. En desktop no importaba.
- `brightnessctl` ya está instalado (dependencia de `cachyos-hypr-noctalia`); Noctalia lo usa para backlight.

### 4.6 Checklist rápida de adaptación (orden sugerido)
1. Copiar dotfiles. 2. Comentar `environment.lua` líneas 8-11. 3. Confirmar que NO existe `config/nwg-monitors.conf` (ya no viene en el paquete). 4. `variables.lua`: `MONITOR1="eDP-1"`. 5. Escala en `monitors.lua` (fallback). 6. `autostart.lua`: quitar `powerprofilesctl set balanced`. 7. `inputs.lua`: touchpad + kb_layout. 8. Noctalia: quitar brillo ddcutil HDMI-A-1, `gpu_temp`→CPU, añadir `battery`. 9. `brave-flags.conf`: quitar `VaapiOnNvidiaGPUs`. 10. Luego implementar la lógica dinámica §4.2 (binds/workspaces/app-web/hotplug). 11. `hyprctl reload` y probar SUPER+1..5 con y sin Arzopa.

---

## 5. Paquetes necesarios para esta área

Verificados en la PC con `pacman -Qo` / `pacman -Qq` (repos CachyOS/Arch salvo donde dice AUR).

**Núcleo de sesión**
- `hyprland` (0.56.2; incluye hyprctl), `hyprutils`, `hyprlang`, `hyprcursor`, `hyprgraphics`, `hyprwayland-scanner`, `hyprtoolkit`, `hyprwire`, `hyprland-guiutils` (arrastrados como deps)
- `uwsm`
- `xdg-desktop-portal-hyprland`, `xdg-desktop-portal-gtk`, `xdg-desktop-portal`
- `noctalia` (shell/barra/launcher/lock/notificaciones/portapapeles)
- `cachyos-hypr-noctalia` (meta-config de CachyOS; trae como deps: adw-gtk-theme, awesome-terminal-fonts, brightnessctl, cachyos-alacritty-config, ddcutil, curl, dolphin, gnome-calculator, gnome-keyring, gnome-text-editor, grim, hyprpicker, kde-cli-tools, kitty, noto-fonts, noto-fonts-emoji, nwg-look, qt6ct, qview, slurp, swash, uwsm, wl-clipboard, xorg-xhost)
- `polkit`, `dbus`, `power-profiles-daemon`, `xorg-xhost`

**Monitores / tema**
- `nwg-displays`, `nwg-look`, `qt6ct` (qt5ct NO está instalado)
- `adw-gtk-theme` (adw-gtk3-dark), `adwaita-icon-theme`, `adwaita-icon-theme-legacy`, `adwaita-cursors`, `breeze-icons`
- Fuentes: `adwaita-fonts` (Adwaita Sans), `noto-fonts`, `noto-fonts-cjk`, `noto-fonts-emoji`, `cantarell-fonts`, `ttf-meslo-nerd`, `ttf-fantasque-nerd`, `awesome-terminal-fonts`, `powerline-fonts`
- Cursor **Bibata-Modern-Ice**: NO es paquete (está en `~/.local/share/icons/`, ya copiado). Alternativa: AUR `bibata-cursor-theme-bin`.
- `gtk-layer-shell`, `gtk4-layer-shell`, `libadwaita`, `gtk4`

**Apps que lanzan los atajos**
- `kitty`, `dolphin`, `brave-bin` (AUR/chaotic), `gnome-text-editor`, `gnome-calculator`, `obsidian`, `opendeck-bin` (AUR), `visual-studio-code-bin` (AUR), `btop`, `satty`

**Scripts**
- `grim`, `slurp`, `wl-clipboard`, `libnotify`, `zenity`, `jq`, `inotify-tools`, `ydotool`, `wtype`, `xdg-utils`, `python`, `python-gobject`
- Auto-captura (SUPER+ALT+S / `video-a-capturas.sh`): `python-numpy`, `python-pillow` (hoy instalados solo como dependencias → instalarlos **explícitos**), `yt-dlp`, `ffmpeg`
- TTS: `piper-tts`, `piper-voices-es-ar` (+ `piper-voices-common`, `piper-voices-es-mx`), `pipewire-audio`, `ffmpeg`, `libpulse`; `edge-tts` vía `pipx install edge-tts` (no es paquete; venv en `~/.local/share/pipx/venvs/edge-tts`, symlink en `~/.local/bin`). Chatterbox: venv propio, no migrar a laptops sin GPU dedicada.
- `ddcutil` (brillo de monitores externos; en laptop solo si la Arzopa soporta DDC/CI, raro)

**Otros relacionados (otros docs)**: `hyprwhspr` (dictado, AUR), `xremap-hypr-bin` (AUR), `hyprpicker`.

**GPU — cambiar en laptops**
- NO instalar: `nvidia-580xx-dkms`, `nvidia-580xx-utils`, `nvidia-580xx-settings`, `lib32-nvidia-580xx-utils`, `opencl-nvidia-580xx`, `lib32-opencl-nvidia-580xx`, `libva-nvidia-driver`, `linux-firmware-nvidia`.
- SÍ instalar: `mesa`, `lib32-mesa`, `vulkan-intel`, `intel-media-driver` (VA-API iHD, sirve para UHD 620 y Iris Xe), `libva-utils` (para verificar con `vainfo`), opcional `intel-gpu-tools`.
- Laptop: `brightnessctl` (ya viene), opcional `hypridle`, `iio-sensor-proxy` (repo) + `iio-hyprland-git` (AUR) (Surface), `squeekboard` (repo) o `wvkbd` (AUR) (teclado en pantalla).

---

## 6. Cosas raras / deuda detectada
- `config/nwg-monitors.lua`, `monitors.conf`, `workspaces.conf`: huérfanos. El lanzador de nwg-displays pasa `-w nwg-workspaces.conf`, archivo inexistente y no leído.
- `scripts/curso-abrir.sh` línea 28 usa `hyprctl dispatch workspace name:estudio` (sintaxis pre-Lua) → probablemente no funciona.
- `scripts/vscode-open-md.sh` línea 19 usa `address = "..."` en `hl.dsp.window.move` mientras el resto usa `window = "address:..."` → sospechoso.
- `scripts/watch-monitors.sh` y `pomodoro-toggle.sh` no se llaman desde Hyprland (watch: nadie; pomodoro/vscode-open-md: solo desde Stream Deck/opendeck).
- Reglas de gaming/Steam siguen activas aunque Steam no está instalado (inofensivo).
- `gtk-4.0/gtk.css` importa `libadwaita.css`/`libadwaita-tweaks.css` inexistentes (inofensivo).
- Tamaño de cursor inconsistente: GTK 30 vs Hyprland/XCursor 24.
- `qt5ct/colors/noctalia.conf` y `xsettingsd.conf` existen pero qt5ct y xsettingsd no están instalados.
- Comentarios de `variables.lua` ("yodoit") no coinciden con los monitores reales (ASUS/HP).
- El repo git `~/.config/hypr` tiene muchos cambios sin commitear (commit único "Estado inicial").
