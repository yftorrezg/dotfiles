# Clasificación de paquetes (PC de escritorio -> laptops)

Origen: PC CachyOS + Hyprland (noctalia), CPU Intel i7-6700K, GPU NVIDIA GTX 980.
Destino: Surface Pro 6 (i7 8ª gen, Intel UHD 620) y ThinkPad E14 Gen4 (i7 12ª gen, Intel Iris Xe).
Listas crudas: `pacman-repo.txt` (220 al 26-09, `pacman -Qqen`), `aur.txt` (11, `pacman -Qqem`), `flatpak.txt` (flatpak NO instalado).
Fecha: 2026-09-26.

> Método robusto en la laptop: tras instalar CachyOS (edición Hyprland/noctalia), ejecutar
> `comm -13 <(pacman -Qqen | sort) <(sort pacman-repo.txt)` para ver qué falta, y cruzarlo con la sección (c).
> La sección (b) es una estimación de lo que trae el instalador; no hace falta instalarla a mano.

---

## (a) Específicos de esta PC — NO instalar en la laptop

| Paquete | Motivo |
|---|---|
| nvidia-580xx-dkms, nvidia-580xx-utils, nvidia-580xx-settings | Driver NVIDIA (rama legacy 580xx para Maxwell/GTX 980) |
| lib32-nvidia-580xx-utils, opencl-nvidia-580xx, lib32-opencl-nvidia-580xx | Partes 32-bit / OpenCL de NVIDIA |
| libva-nvidia-driver | VA-API sobre NVIDIA. En Intel se usa `intel-media-driver` (ver abajo) |
| linux-cachyos-lts, linux-cachyos-lts-headers | Kernel LTS de respaldo, útil sobre todo por el driver NVIDIA DKMS. Opcional en la laptop |
| logiops | Demonio para ratón Logitech; el servicio `logid` está **deshabilitado** y no hay `/etc/logid.cfg` en uso. No instalar |
| idevicerestore-git (AUR) | Restaurar firmware de iPhone. Uso puntual, no hace falta |

Nota: `intel-ucode` SÍ va a la laptop (esta PC también es Intel). `chwd` lo pone solo.

**Añadir en la laptop (no está en esta PC):** `intel-media-driver` (VA-API iHD, 8ª y 12ª gen), `vulkan-intel`, opcional `libva-intel-driver` (i965, solo como alternativa en la Surface 8ª gen), `libva-utils` (para `vainfo`), `intel-gpu-tools` (opcional). En Surface: kernel/paquetes `linux-surface` son opcionales (cámara, pen, touch mejorado).

---

## (b) Base de CachyOS (el instalador / la edición Hyprland-noctalia ya lo pone)

base base-devel linux-cachyos linux-cachyos-headers linux-firmware intel-ucode mkinitcpio
limine limine-mkinitcpio-hook limine-snapper-sync snapper cachyos-snapper-support btrfs-progs btrfs-assistant
plymouth cachyos-plymouth-bootanimation cachyos-plymouth-theme efibootmgr efitools os-prober
cachyos-hello cachyos-hooks cachyos-kernel-manager cachyos-keyring cachyos-mirrorlist cachyos-v3-mirrorlist cachyos-v4-mirrorlist
cachyos-packageinstaller cachyos-rate-mirrors cachyos-settings cachyos-wallpapers cachyos-fish-config cachyos-zsh-config cachyos-micro-settings
cachyos-hypr-noctalia (meta: trae kitty, dolphin, gnome-text-editor, gnome-calculator, qview, grim, slurp, wl-clipboard, hyprpicker, ddcutil, noctalia, uwsm, xdg-desktop-portal-hyprland, cachyos-alacritty-config...)
hyprland noctalia-greeter chwd hwdetect hwinfo shelly paru
networkmanager networkmanager-openvpn iwd wpa_supplicant netctl modemmanager usb_modeswitch xl2tpd dnsmasq bind inetutils nss-mdns openssh ethtool
bluez bluez-hid2hci bluez-libs bluez-obex bluez-utils
pipewire-alsa pipewire-pulse wireplumber alsa-firmware alsa-plugins alsa-utils sof-firmware
gst-libav gst-plugin-pipewire gst-plugins-bad gst-plugins-ugly
cantarell-fonts noto-fonts noto-fonts-cjk noto-fonts-emoji ttf-bitstream-vera ttf-dejavu ttf-liberation ttf-meslo-nerd ttf-opensans awesome-terminal-fonts papirus-icon-theme
cryptsetup device-mapper dmraid lvm2 mdadm dosfstools e2fsprogs exfatprogs f2fs-tools jfsutils nilfs-utils xfsprogs mtools fsarchiver nfs-utils wimlib
dmidecode hdparm lsscsi sg3_utils sysfsutils smartmontools usbutils upower power-profiles-daemon cpupower accountsservice fprintd realtime-privileges
man-db man-pages texinfo less which diffutils perl python nano nano-syntax-highlighting vim micro bash-completion sudo
pacman-contrib pkgfile plocate reflector rebuild-detector logrotate lsb-release s-nail xdg-user-dirs ufw ufw-extras
mesa-utils vulkan-icd-loader lib32-vulkan-icd-loader wget rsync unzip unrar 7zip duf fastfetch btop
poppler-glib libgsf libopenraw ffmpegthumbnailer libdvdcss gtk4-layer-shell python-defusedxml python-packaging

(Si alguno falta tras instalar, reinstalar con `pacman -S --needed`; es inocuo. `fprintd` es útil en la ThinkPad E14 si tiene lector de huellas.)

---

## (c) Apps del usuario

### (c1) USA — instalar en la laptop
| Paquete | Origen | Para qué / evidencia |
|---|---|---|
| brave-bin | repo cachyos | Navegador por defecto (http/https/html/**PDF** vía `brave-new-window.desktop`), SUPER+W, apps web (`app-web.sh`: YouTube, WhatsApp, Telegram, FB, IG, TikTok, Drive) |
| kitty | (dep noctalia) | Terminal: `TERMINAL="kitty"` en `hypr/config/variables.lua` (SUPER+Return) |
| dolphin, ark | dolphin es dep noctalia; ark repo | Gestor de archivos por defecto (SUPER+E, inode/directory) |
| gwenview | repo | Visor de imágenes por defecto (todo image/*) desde 26-09-2026 |
| mpv | repo | Video/audio por defecto; config de estudio con uosc + scripts propios |
| satty | repo | Editor de capturas usado por noctalia (`noctalia/config.toml: satty -f -`). **Hoy está como huérfano (dep), instalarlo EXPLÍCITO** |
| obsidian | repo extra | Notas, SUPER+N |
| visual-studio-code-bin | AUR | Editor, SUPER+G; `.md` abren en VS Code preview |
| claude-desktop | repo cachyos | App Claude (x-scheme-handler/claude). Claude Code va en `~/.local/bin/claude` (instalador oficial, no pacman) |
| libreoffice-fresh, libreoffice-fresh-es | repo | Writer/Impress usados hasta 09-09; bind CTRL+ALT+Escape para matar LibreOffice |
| keepassxc | repo | Gestor de contraseñas |
| localsend | repo cachyos | Pasar archivos entre dispositivos |
| rustdesk-bin | AUR | Escritorio remoto |
| obs-studio | repo | Grabación de pantalla |
| wtype, ydotool | repo | Necesarios para SUPER+R (leer selección) y hyprwhspr |
| zenity | repo | Diálogos de scripts (curso, voz, carpeta de capturas) |
| inotify-tools | repo | `watch-monitors.sh` |
| hyprwhspr | AUR | Dictado por voz (servicio de usuario habilitado) |
| piper-voices-es-ar, piper-voices-es-mx | AUR | Voces TTS offline para SUPER+R (traen `piper-tts`) |
| xremap-hypr-bin | AUR | Remapeo de teclas (servicio de usuario `xremap` habilitado). **Config vacía: doc 03/04 recomiendan NO instalarlo en la laptop salvo que el usuario lo pida** |
| swappy | repo | Explícito, usado 08-31; mantener si se quiere, pero satty lo sustituye (ver DUDOSO) |
| restic, rclone | repo | Backup diario (backup-home.timer) y montaje Google Drive (rclone-gdrive.service) |
| git, github-cli, ripgrep, nodejs, npm, python-pipx | repo | Desarrollo; pipx tiene `edge-tts` (voz online para SUPER+R) |
| nwg-displays, pavucontrol | repo | Monitores y audio |
| glances, pv | repo | Utilidades CLI |
| yt-dlp, python-numpy, python-pillow | repo | Auto-captura de cursos (SUPER+ALT+S, `video-a-capturas.sh`). numpy/pillow hoy son dependencias: instalarlos explícitos |

### (c2) DUPLICADO — NO instalar en la laptop (candidatos a desinstalar aquí)
| Paquete | Por qué |
|---|---|
| firefox | Brave es el navegador por defecto en todo; Firefox solo usado hasta 12-09 para abrir .ipynb |
| geeqie | Visor de imágenes; último uso 30/31-08; el por defecto es gwenview |
| imv | Visor de imágenes; fue el más usado hasta el 25-09 (99 aperturas) pero el 26-09 se cambió el por defecto a gwenview |
| okular | Visor PDF; PDF abre en Brave; 1 solo uso (31-08) |
| alacritty | Terminal; el configurado es kitty (alacritty.toml solo lo retoca el tema noctalia) |
| vlc-plugins-all | Plugins de VLC sin VLC instalado; el reproductor es mpv |

(Chromium, Google Chrome, Edge, Opera, Vivaldi **no están instalados**: sus carpetas en ~/.config solo contienen `NativeMessagingHosts/` (4 KB) que crea la extensión Claude in Chrome. Code - OSS tampoco está instalado: carpeta residual del 29-08.)

### (c3) DUDOSO — preguntar al usuario
| Paquete | Nota |
|---|---|
| gimp | Único editor de imágenes; usado solo el 30-08 |
| kdenlive | Único editor de video; usado solo el 31-08 |
| xournalpp | Anotar PDFs / notas a mano (útil con el lápiz de la Surface) — sin uso registrado |
| meld | Comparar archivos; sin uso registrado |
| opencode | Agente IA en terminal; config 16-09, 1 uso en historial |
| antigravity-cli | AUR, CLI de Google Antigravity |
| android-studio | AUR, pesado (~3 GB); sin evidencia de uso reciente |
| docker, docker-compose | Servicio docker **deshabilitado**, 0 imágenes |
| mosquitto | Broker MQTT; ningún config lo usa |
| tesseract, tesseract-data-spa | OCR; ningún script lo usa |
| opendeck-bin | AUR, software del Stream Deck (periférico de escritorio). Solo si el Stream Deck se usará con la laptop |
| solaar | Receptor Logitech (teclado K380 va por Bluetooth). Solo si se usa receptor Unifying/Bolt |
| swappy | Duplica a satty (ambos editan capturas); noctalia usa satty |
| whisper-cpp, ggml-vulkan | Instalados explícitos el 26-09 15:03 (después del relevamiento); hyprwhspr usa su propio venv pywhispercpp en CPU, no estos. Preguntar para qué |
| aria2, python-curl_cffi | Instalados explícitos el 26-09 (después del relevamiento); probablemente acompañan a yt-dlp. Preguntar |
