---
tags: [sistema, dictado]
actualizado: 2026-09-26
---
# 02 — Dictado por voz, lectura en voz alta (TTS) y servicios de usuario

Documento para reinstalar en las laptops (Surface Pro 6: i7-8650U/8ª gen, Intel UHD 620; ThinkPad E14 Gen4: i7 12ª gen, Iris Xe; ambas 16 GB, **sin NVIDIA**). Origen: PC CachyOS + Hyprland (config en Lua, sesión vía UWSM) con GTX 980. Relevado el 2026-09-26.

Los archivos están copiados en `~/migracion-cachyos/dotfiles/` con la misma ruta relativa a `$HOME`. Restaurar con:

```bash
cp -a ~/migracion-cachyos/dotfiles/.config/hyprwhspr      ~/.config/
cp -a ~/migracion-cachyos/dotfiles/.config/systemd/user/* ~/.config/systemd/user/
cp -a ~/migracion-cachyos/dotfiles/.config/hypr/scripts/* ~/.config/hypr/scripts/
cp -a ~/migracion-cachyos/dotfiles/.local/bin/backup-home.sh ~/.local/bin/   # teclas-fantasma.py está en solo-esta-pc/, no va a la laptop
cp -a ~/migracion-cachyos/dotfiles/.config/restic/home-excludes.txt ~/.config/restic/
```

NO se copió (hay que regenerarlo): modelos whisper, voces Piper, venvs, caché de HuggingFace, `~/.config/rclone/rclone.conf` (tiene tokens), `~/.config/restic/home-backup.pass` (contraseña del repo restic), ni los symlinks runtime de `~/.config/hyprwhspr/` (`audio_level`, `recording_control`, `recording_status` → apuntan a `/run/user/1000/hyprwhspr/`, hyprwhspr los recrea solo).

---

## 1. Atajos

| Atajo | Qué hace | Dónde está definido |
|---|---|---|
| `SUPER+ALT+Z` | Dictado (toggle) en **español** | `~/.config/hyprwhspr/config.json` (`primary_shortcut`). hyprwhspr lo escucha solo vía evdev, **no** está en binds.lua |
| `SUPER+ALT+X` | Dictado (toggle) en **inglés** | `config.json` (`secondary_shortcut` + `secondary_language: en`) |
| `SUPER+R` | Lee en voz alta el texto seleccionado; apretar de nuevo corta | `~/.config/hypr/config/binds.lua:264` → `uwsm app -- bash ~/.config/hypr/scripts/leer-seleccion.sh` |
| `SUPER+ALT+R` | Ventanita GTK4 para elegir voz y velocidad | `binds.lua:265` → `actualizar-voz.sh` → `elegir-voz.py` |

**Conflicto RESUELTO el 26-09** (dictado movido a SUPER+ALT+Z/X; antes era D/I). Texto original del hallazgo: en `binds.lua:81-82` también están `SUPER+ALT+I` → app web Instagram y `SUPER+ALT+D` → app web Drive (`app-web.sh`). Como hyprwhspr tiene `grab_keys: false` (default), ambos se disparan a la vez. Preguntarle al usuario si quiere mover uno de los dos antes de replicarlo tal cual.

---

## 2. Dictado: hyprwhspr

- Paquete: **`hyprwhspr` 1.43.0-1** (AUR, que al 26-09 ya ofrece 1.45.2; `pacman -Qm` lo lista como foráneo). Instala en `/usr/lib/hyprwhspr/` y el binario `/usr/bin/hyprwhspr`. Upstream: https://github.com/goodroot/hyprwhspr
- Dependencias que arrastra: python, python-sounddevice, python-numpy, python-soxr, python-evdev, python-pyperclip, python-pyudev, python-rich, python-pulsectl, wtype, ydotool, wl-clipboard, xclip, xdotool, xorg-xprop, pipewire, pipewire-alsa, pipewire-pulse. Opcionales instalados: python-dbus, python-gobject, gtk4-layer-shell (Mic-OSD), cmake, git, base-devel.
- Backend de transcripción: **pywhispercpp 1.5.1 (whisper.cpp) en CPU**. Venv en `~/.local/share/hyprwhspr/venv` (Python 3.14, `--system-site-packages`, ~30 MB; solo contiene `libggml-cpu`, no hay libs CUDA). `~/.local/state/hyprwhspr/install-state.json` dice `"installed_backend": "cpu"`.
  - **Ojo: el journal dice `[BACKEND] pywhispercpp (CUDA (NVIDIA) - package unknown)`, pero es falso.** Ese texto sale de una detección de respaldo que solo mira si existe `nvidia-smi` (`/usr/lib/hyprwhspr/lib/src/backends/pywhispercpp_backend.py:266`). En realidad ya corre en CPU en esta PC. O sea, en las laptops no cambia nada de fondo.
- Modelos (en `~/.local/share/pywhispercpp/models/`, **no copiados**):
  - `ggml-small.bin` 466 MB ← **el que usa** (`"model": "small"`)
  - `ggml-base.bin` 142 MB (instalado, sin uso)
  - `ggml-silero-v5.1.2.bin` 0,9 MB (VAD, porque `pywhispercpp_use_vad: true`)
- Config (`~/.config/hyprwhspr/config.json`, copiada): modelo `small`, idioma `es`, secundario `en`, `recording_mode: toggle`, filtro de muletillas, `symbol_replacements: true`, `audio_device_name: "Maono"`.
- Tema del overlay del micrófono: `~/.config/hyprwhspr/theme/mic-osd.css` (copiado).
- Hay un plugin de barra Noctalia `~/.local/share/noctalia/plugins/noctwhspr/` (lo copió el agente de Noctalia; se genera con `hyprwhspr noctalia install`).
- Servicio: `~/.config/systemd/user/hyprwhspr.service` (enabled + active, `WantedBy=graphical-session.target`). Espera el socket Wayland, luego corre `/usr/lib/hyprwhspr/bin/hyprwhspr`, y al parar mata sus teclados virtuales y el socket de ydotool propio.
- Cómo escribe el texto: portapapeles + atajo de pegar sintético (ydotool/uinput). Necesita al usuario en los grupos `input` y `audio` y acceso a `/dev/uinput`.

### Ajustes para las laptops

1. **Micrófono:** `"audio_device_name": "Maono"` es el mic USB de la PC. En las laptops no está: hyprwhspr cae al primer dispositivo PulseAudio (funciona igual, pero conviene sacar la clave o poner el mic interno). Ver fuentes con `pactl list short sources` y poner un trozo del nombre. En el journal de esta PC aparecen errores `PaErrorCode -9999 ... Microphone unavailable` cuando el Maono se desconecta.
2. **Modelo (CPU):**
   - ThinkPad E14 Gen4 (i7 12ª gen, 10–12 núcleos): **`small` va bien** en CPU (1–3 s por frase corta). Dejarlo.
   - Surface Pro 6 (i7-8650U, 4c/8t, 15 W, se calienta y baja frecuencia): `small` funciona pero tarda más (~3–6 s). Si molesta, cambiar a **`base`** (bastante más rápido, algo menos preciso en español). Descargar con `hyprwhspr model download base`.
   - Opcional: `"threads"` (default = min(8, núcleos)). En la Surface puede convenir `"threads": 4`.
   - Opcional (experimental): backend Vulkan en la iGPU Intel (`hyprwhspr setup auto --backend vulkan`, requiere `vulkan-intel` y compila pywhispercpp). En UHD 620 casi no gana; en Iris Xe puede ayudar. Primero dejar CPU y probar.
3. No hace falta nada de CUDA ni `nvidia-utils`. En las laptops el log dirá `CPU` (sin `nvidia-smi` la detección falsa desaparece).

### Reinstalación paso a paso

```bash
paru -S hyprwhspr gtk4-layer-shell python-dbus python-gobject   # o yay
sudo usermod -aG input,audio $USER        # cerrar sesión y volver a entrar después
cp -a ~/migracion-cachyos/dotfiles/.config/hyprwhspr ~/.config/
# editar ~/.config/hyprwhspr/config.json: audio_device_name (y model si es la Surface)
hyprwhspr setup auto --backend cpu        # crea venv, pywhispercpp y descarga el modelo
hyprwhspr model download small            # (o base) si el setup no lo bajó
cp -a ~/migracion-cachyos/dotfiles/.config/systemd/user/hyprwhspr.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now hyprwhspr.service
```

(`hyprwhspr systemd install` hace lo mismo que las últimas 3 líneas con su unit por defecto; la copiada es idéntica a la que genera la versión 1.43.)

### Cómo probar

```bash
hyprwhspr status              # instalación, servicio, modelos, permisos (input/audio/uinput)
hyprwhspr test                # micrófono + backend
journalctl --user -u hyprwhspr -f   # debe decir "[READY] hyprwhspr ready" y "[BACKEND] ... CPU"
```

Después abrir un editor, apretar `SUPER+ALT+Z`, hablar, apretar de nuevo: el texto aparece pegado. (El aviso "User NOT in 'tty' group" de `status` es normal y no se usa.)

---

## 3. Lectura en voz alta (SUPER+R)

### Piezas

| Archivo (`~/.config/hypr/scripts/`) | Rol |
|---|---|
| `leer-seleccion.sh` | Script principal. Toggle (si ya suena algo, mata piper-tts/edge-tts/ffplay/pw-play/chatterbox y sale). Toma la selección primaria (`wl-paste --primary`); si está vacía y la ventana no es una terminal, guarda el portapapeles, simula **Ctrl+C con ydotool** (`ydotool key 29:1 46:1 46:0 29:0`, cae a `wtype` si falla), hace polling del portapapeles hasta **300 ms** (15 × 20 ms) y restaura el portapapeles viejo en segundo plano. Luego limpia el texto y lo manda al motor elegido. |
| `limpiar-texto.py` | Primer paso de limpieza: saca emojis, cambia URLs por "este enlace" y rutas por "esta ruta". Después `leer-seleccion.sh` aplica varios `sed` (operadores a palabras, símbolos a pausas, saltos de línea a comas). |
| `piper-daemon.py` | Daemon que mantiene los modelos Piper cargados (ahorra ~2 s por lectura). Socket unix `~/.cache/piper-voz.sock`. Precarga `es_AR-daniela-high` y `es_MX-claude-high`. Usa el módulo Python `piper` del paquete del sistema (`/usr/bin/python3`). |
| `piper-client.py` | Cliente del daemon: manda `{"text","model","length_scale"}` y recibe PCM s16le mono 22050 Hz, que se reproduce con `pw-play`. Si el daemon no responde, `leer-seleccion.sh` usa `piper-tts` directo y arranca el servicio. |
| `chatterbox-hablar.py` | Motor opcional "Chatterbox" (máxima calidad, offline, lento). Corre con `~/.local/share/piper-voz/chatterbox-venv/bin/python` en CPU. |
| `elegir-voz.py` + `actualizar-voz.sh` | Ventanita GTK4/libadwaita (SUPER+ALT+R). Escribe `ENGINE`, `VOICE`, `SPEED_MULT` en `voz.conf`. |
| `voz.conf` | Estado actual: `ENGINE=piper`, `VOICE=/usr/share/piper-voices/es/es_AR/daniela/high/es_AR-daniela-high.onnx`, `SPEED_MULT=1.3`. |

**Decisiones del usuario que NO hay que cambiar:**
- El Ctrl+C simulado usa **ydotool, no wtype**, porque wtype (protocolo virtual-keyboard) no llega a los webviews de VSCode (por ejemplo Markdown Preview). ydotool inyecta a nivel kernel (`/dev/uinput`).
- El tope de espera de copia de **300 ms** es decisión del usuario.
- Si "no lee" en VSCode, casi siempre es que el mouse quedó fuera de la selección (falsa alarma conocida).
- Las terminales (kitty, alacritty, foot, konsole, etc.) se excluyen del Ctrl+C simulado porque mandaría SIGINT.

### Motores y voces

Voces del selector (`elegir-voz.py`):
- edge-tts (online, Microsoft): `es-AR-ElenaNeural`, `es-MX-JorgeNeural`. Si falla (sin internet, timeout de 12 s) cae a Piper Daniela.
- Piper (offline): `es_AR-daniela-high`, `es_MX-claude-high`.
- Chatterbox (offline, `es`).

Voces Piper instaladas (paquetes AUR, en `/usr/share/piper-voices/`):

| Archivo | Tamaño | Paquete |
|---|---|---|
| `es/es_AR/daniela/high/es_AR-daniela-high.onnx` (+ `.onnx.json`) | 109 MB | `piper-voices-es-ar` 1.0.1-1 |
| `es/es_MX/claude/high/es_MX-claude-high.onnx` | 61 MB | `piper-voices-es-mx` 1.0.1-1 |
| `es/es_MX/ald/medium/es_MX-ald-medium.onnx` | 61 MB | `piper-voices-es-mx` (sin uso) |
| `es/es_MX/ald/x_low/es_MX-ald-x_low.onnx` | 21 MB | `piper-voices-es-mx` (sin uso) |

Las rutas están fijas en los scripts, así que **instalar los mismos paquetes AUR** mantiene todo igual.

### Paquetes y entornos Python

| Componente | Cómo está instalado | Versión en la PC |
|---|---|---|
| `piper-tts` (binario `/usr/bin/piper-tts` + módulo `piper`) | AUR | 1.5.0-1 (el AUR ya tiene 1.8.0; la API `PiperVoice`/`SynthesisConfig` existe desde 1.3, debería andar, probar) |
| `piper-voices-common`, `piper-voices-es-ar`, `piper-voices-es-mx` | AUR | 1.0.1 |
| `python-onnxruntime-cpu` | repo (dependencia de piper-tts) | 1.29.0 |
| `edge-tts` | **pipx** (`~/.local/share/pipx/venvs/edge-tts`, symlinks en `~/.local/bin/edge-tts` y `edge-playback`) | 7.2.8 |
| Chatterbox | venv `~/.local/share/piper-voz/chatterbox-venv` (1,6 GB, Python 3.14): `chatterbox-tts` 0.1.7, `torch` 2.13.0+cpu, `torchaudio` 2.11.0+cpu, `soundfile` 0.14.0, `numpy` | — |
| Modelo Chatterbox | caché HF `~/.cache/huggingface/hub/models--ResembleAI--chatterbox` (**3,0 GB**), se baja solo en el primer uso | — |
| Reproductores | `ffplay` (paquete `ffmpeg`), `pw-play` (`pipewire`), `paplay` (`libpulse`/`pipewire-pulse`) | ffmpeg 9.0.2 |
| Otros | `wl-clipboard` 2.3.0, `wtype` 0.4, `ydotool` 1.0.4, `jq` 1.8.2, `libnotify` (notify-send), `python-gobject` 3.56.3, `gtk4`, `libadwaita` 1.9.4 | — |

### Reinstalación paso a paso

```bash
sudo pacman -S --needed wl-clipboard wtype ydotool jq libnotify ffmpeg pipewire pipewire-pulse \
                        python-gobject gtk4 libadwaita python-pipx python-onnxruntime-cpu
paru -S piper-tts piper-voices-common piper-voices-es-ar piper-voices-es-mx
pipx install edge-tts          # queda en ~/.local/bin/edge-tts (el script agrega ~/.local/bin al PATH)

cp -a ~/migracion-cachyos/dotfiles/.config/hypr/scripts/{leer-seleccion.sh,limpiar-texto.py,piper-daemon.py,piper-client.py,chatterbox-hablar.py,elegir-voz.py,actualizar-voz.sh,voz.conf} ~/.config/hypr/scripts/
cp -a ~/migracion-cachyos/dotfiles/.config/systemd/user/piper-voz-daemon.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now piper-voz-daemon.service
```

Chatterbox (opcional, **no recomendado en la Surface**; ver abajo):

```bash
python3 -m venv ~/.local/share/piper-voz/chatterbox-venv
~/.local/share/piper-voz/chatterbox-venv/bin/pip install --index-url https://download.pytorch.org/whl/cpu torch torchaudio
~/.local/share/piper-voz/chatterbox-venv/bin/pip install chatterbox-tts soundfile
# el primer uso descarga ~3 GB a ~/.cache/huggingface
```

(Si `chatterbox-tts` no instala con Python 3.14, crear el venv con `uv venv --python 3.11 ...`.)

### Ajustes para las laptops

- Piper y edge-tts **no usan GPU**, andan igual. Piper "high" en CPU es rápido en las dos laptops.
- En la Surface (16 GB, 4 núcleos) el daemon precarga 2 voces (~350–450 MB de RAM). Aceptable; si hace falta, dejar solo Daniela en `PRELOAD_VOICES`.
- **Chatterbox** ya corre en CPU (`device="cpu"`), pero recarga el modelo en cada lectura y es muy lento (decenas de segundos en la Surface). Sugerencia: no instalarlo en la Surface; el script cae solo a Piper si falta el venv ("Chatterbox no instalado").
- Si la laptop no tiene sesión UWSM, `binds.lua` define `launchPrefix = "uwsm app -- "`; dejarlo vacío si no se usa UWSM (lo maneja el agente de Hyprland).

### Cómo probar

```bash
systemctl --user is-active piper-voz-daemon      # active
ls -l ~/.cache/piper-voz.sock                    # socket existe
echo "Hola, esto es una prueba" | python3 ~/.config/hypr/scripts/piper-client.py \
  /usr/share/piper-voices/es/es_AR/daniela/high/es_AR-daniela-high.onnx 0.77 \
  | pw-play --rate=22050 --format=s16 --channels=1 --raw -
edge-tts --voice es-AR-ElenaNeural --text "Prueba online" --write-media /tmp/t.mp3 && ffplay -nodisp -autoexit /tmp/t.mp3
```

Luego seleccionar texto en Brave, en VSCode (incluido Markdown Preview) y en kitty, apretar `SUPER+R` (y otra vez para cortar). `SUPER+ALT+R` debe abrir el selector.

---

## 4. ydotool, wtype, wl-clipboard

- `ydotool` 1.0.4 (repo). Servicio **de usuario** del paquete: `/usr/lib/systemd/user/ydotool.service` (`ExecStart=/usr/bin/ydotoold`, `Restart=always`). Habilitado vía symlink en `~/.config/systemd/user/default.target.wants/ydotool.service` (enabled + active).
- Socket: `/run/user/1000/.ydotool_socket` (lo usa `leer-seleccion.sh` con `YDOTOOL_SOCKET`).
- Permisos de `/dev/uinput`: `crw-rw----+ root:input`. Lo da la regla del sistema `/usr/lib/udev/rules.d/80-uinput.rules` (`KERNEL=="uinput", GROUP="input", MODE="0660"`), no hay reglas propias en `/etc/udev/rules.d` para esto. Además `42-logitech-unify-permissions.rules` agrega `uaccess` (el `+` del ACL).
- El usuario está en los grupos: `sys network i2c nopasswdlogin rfkill users video uucp storage lp input audio wheel companion`. Para esta área importan **`input`** (uinput/evdev para ydotool, hyprwhspr, xremap, teclas-fantasma) y **`audio`**.
- No hay `/etc/modules-load.d/uinput.conf` (el módulo carga solo). Si en la laptop `/dev/uinput` no existe: `echo uinput | sudo tee /etc/modules-load.d/uinput.conf`.

```bash
sudo pacman -S --needed ydotool wtype wl-clipboard
sudo usermod -aG input $USER     # re-login
systemctl --user enable --now ydotool.service
# prueba (escribe "hola" en la ventana enfocada tras 2 s):
sleep 2; YDOTOOL_SOCKET=/run/user/$(id -u)/.ydotool_socket ydotool type hola
```

Nota: hyprwhspr levanta además su propio socket de ydotool (`hyprwhspr-ydotool.sock`), independiente del servicio global.

---

## 5. Todos los servicios de `~/.config/systemd/user/`

| Unit | Estado | ExecStart / qué hace | Dependencias / notas |
|---|---|---|---|
| `hyprwhspr.service` | enabled, active | `/usr/lib/hyprwhspr/bin/hyprwhspr` — dictado | `PartOf/After=graphical-session.target`, `After/Wants=pipewire, wireplumber`. Ver sección 2 |
| `piper-voz-daemon.service` | enabled, active | `/usr/bin/python3 %h/.config/hypr/scripts/piper-daemon.py` — Piper en memoria | `After=graphical-session.target`, `WantedBy=graphical-session.target`. Necesita `piper-tts` + voces |
| `ydotool.service` (del paquete, en `/usr/lib/systemd/user/`) | enabled, active | `/usr/bin/ydotoold` | `WantedBy=default.target`; grupo `input` |
| `xremap.service` | enabled, active | `/usr/bin/xremap --allow-launch true %h/.config/xremap/config.yml` — remapeo por app | Paquete AUR **`xremap-hypr-bin` 0.15.9-1**. La config (`~/.config/xremap/config.yml`, copiada) está **vacía** (`modmap: []`, `keymap: []`): los botones del mouse M720 se manejan en `/etc/logid.cfg` (logiops, otro agente). Hace grab de todos los teclados. En laptops se puede no habilitar |
| `teclas-fantasma.service` (copia en `solo-esta-pc/`) | enabled, active | `/usr/bin/python3 %h/.local/bin/teclas-fantasma.py` — registra qué dispositivo manda KEY_SLEEP/POWER/SUSPEND/WAKEUP (diagnóstico de suspensiones/apagados fantasma del 22–23 sep). Log `~/.local/state/teclas-fantasma.log` | `WantedBy=default.target`, `Restart=always`. Usa `python-evdev` + grupo `input`. **Es diagnóstico de esta PC: en las laptops no hace falta** (instalarlo solo si ahí también hay suspensiones raras) |
| `rclone-gdrive.service` | enabled, active | `rclone mount gdrive: %h/GoogleDrive --vfs-cache-mode full --vfs-cache-max-size 50G --vfs-cache-max-age 72h ...`; `ExecStop=fusermount3 -u` | `Type=notify`, `AssertPathIsDirectory=%h/GoogleDrive`, `After=network-online.target`, `WantedBy=default.target`. Paquetes: `rclone` 1.75.1, `fuse3` |
| `backup-home.service` | static (lo dispara el timer); **estaba "activating" hace 46 min** al relevar (26-09); más tarde el 26-09 figura **failed** | `%h/.local/bin/backup-home.sh` — `restic backup $HOME` a `/mnt/backups/restic-home` (disco externo exFAT, UUID `7FDC-A53B` en `/etc/fstab`), luego `forget --keep-daily 7 --keep-weekly 4 --keep-monthly 6 --prune`. Log `~/.local/state/backup-home.log` | `Type=oneshot`. Paquete `restic` 0.19.1. Contraseña en `~/.config/restic/home-backup.pass` (NO copiada). Excludes en `~/.config/restic/home-excludes.txt` (copiado) |
| `backup-home.timer` | enabled, active | `OnCalendar=daily`, `Persistent=true`, `RandomizedDelaySec=30m` | `WantedBy=timers.target` |

### rclone / Google Drive (remote `gdrive:`)

`~/.config/rclone/rclone.conf` **no se copió** (tiene token OAuth, client_id y client_secret). Contenido relevante sin secretos:

```ini
[gdrive]
type = drive
scope = drive
team_drive =
export_formats = link.html
client_id = <propio del usuario, un client ID OAuth de Google Cloud>
client_secret = <idem>
token = <OAuth>
```

Recrear en la laptop:

```bash
sudo pacman -S --needed rclone fuse3
rclone config          # n → nombre: gdrive → storage: drive → client_id/secret: pedírselos al usuario
                       # (usa uno propio; o dejar vacío para el de rclone, más lento) → scope: 1 (drive, acceso total)
                       # → sin service account → auto config: y (abre el navegador) → shared drive: n
# luego editar ~/.config/rclone/rclone.conf y agregar: export_formats = link.html
mkdir -p ~/GoogleDrive
cp -a ~/migracion-cachyos/dotfiles/.config/systemd/user/rclone-gdrive.service ~/.config/systemd/user/
systemctl --user daemon-reload && systemctl --user enable --now rclone-gdrive.service
ls ~/GoogleDrive       # debe listar el Drive
```

**Laptop:** `--vfs-cache-max-size 50G` es mucho para un SSD de laptop; bajarlo a 5–10G (sobre todo en la Surface).

### Backup restic: está roto en la PC, NO replicar tal cual

- El log muestra **27 inicios y 0 "fin backup"**. Casi todos los días falla con `repository is already locked by PID 168805` (lock viejo del 2026-09-01) y a veces por el PID 30296 (11-sep). Nunca se hizo `restic unlock`.
- **Además `home-excludes.txt` no excluye `~/GoogleDrive`** y el script no usa `--one-file-system`: restic intenta recorrer el mount FUSE de rclone (bajaría el Drive entero). Probable causa de que las corridas queden colgadas ("activating" por mucho tiempo) y dejen locks.
- En las laptops no existe el disco `/mnt/backups`: el script aborta solo ("no está montado"). Decidir con el usuario si quiere backup en la laptop y a dónde. Si se replica: agregar `GoogleDrive` al excludes (o `--one-file-system`) y correr `restic unlock` antes de `backup`.

---

## 6. Checklist rápido para la laptop

1. `sudo usermod -aG input,audio $USER` → cerrar sesión.
2. Paquetes: `sudo pacman -S --needed wl-clipboard wtype ydotool jq libnotify ffmpeg python-gobject gtk4 libadwaita python-pipx rclone fuse3 restic` y `paru -S hyprwhspr gtk4-layer-shell piper-tts piper-voices-common piper-voices-es-ar piper-voices-es-mx` (+ `xremap-hypr-bin` solo si se quiere).
3. `pipx install edge-tts`.
4. Copiar dotfiles (bloque del inicio).
5. Editar `config.json` de hyprwhspr: micrófono (y `base` en la Surface si `small` es lento).
6. `hyprwhspr setup auto --backend cpu`.
7. `systemctl --user daemon-reload && systemctl --user enable --now ydotool hyprwhspr piper-voz-daemon` (+ `rclone-gdrive` después de `rclone config`; `teclas-fantasma`, `xremap` y `backup-home.timer` solo si el usuario los quiere).
8. Probar: `hyprwhspr status`, dictado con `SUPER+ALT+Z`, lectura con `SUPER+R` en Brave, VSCode y kitty.
9. (Conflicto de atajos ya resuelto el 26-09: dictado en SUPER+ALT+Z/X.)
