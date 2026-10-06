---
tags: [sistema, instalacion]
actualizado: 2026-09-26
---
# 05 — Sistema base (lo que se elige en el instalador y en /etc)

Relevado el 2026-09-26 en la PC de escritorio "yf" (laboratorio). Copias en `../system/etc/`.

## Instalación de CachyOS (qué elegir en el instalador)

| Opción | En la PC | En las laptops |
|---|---|---|
| Escritorio | Hyprland (config propia en Lua, ver doc 01) | Igual |
| Bootloader | **Limine** + `limine-snapper-sync` (snapshots de btrfs como entradas de arranque) | Igual |
| Sistema de archivos | **btrfs** con subvolúmenes `@ @home @root @srv @cache @tmp @log`, `noatime,compress=zstd:1`; `/tmp` en tmpfs | Igual |
| Snapshots | `snapper` config `root` (solo `/`), `snapper-cleanup.timer` | Igual |
| Repos | `cachyos-v3` (CPU x86-64-v3) | Surface Pro 6 (i7-8ª) y ThinkPad E14 G4 (i7-12ª) soportan v3 → el instalador lo elige solo |
| Idioma / zona | `es_BO.UTF-8`, `America/La_Paz` | Igual |
| Teclado | Consola `KEYMAP=es`, XKB `es` / `pc105` (pero **Hyprland usa `us`**: no define `kb_layout`) | Lo pone el instalador. La distribución física del K380, Type Cover y ThinkPad **no está confirmada**: preguntar (doc 03 §2) |
| Login | **greetd** con `noctalia-greeter-session` (usuario `greeter`) | Igual (ver `system/etc/greetd/config.toml`) |
| Driver gráfico | **NVIDIA GTX 980** (`nvidia-*` + `nvidia-suspend/resume/hibernate.service`) | **NO**. Ambas son Intel → `mesa`, `vulkan-intel`, `intel-media-driver` (VA-API). No instalar nada `nvidia*` |

## Servicios del sistema habilitados (systemctl, nivel sistema)

`NetworkManager`, `bluetooth`, `logid` (botones del mouse M720, ver doc 03), `greetd`, `ufw` (firewall), `ananicy-cpp`, `avahi-daemon`, `systemd-resolved`, `systemd-timesyncd`, `limine-snapper-sync`, `fstrim.timer`, `snapper-cleanup.timer`, `cachyos-rate-mirrors.timer`, `cachyos-iw-set-regdomain.path` (+ los que trae el sistema por defecto: `NetworkManager-dispatcher`, `NetworkManager-wait-online`, `getty@`, `systemd-userdbd.socket`, `remote-fs.target`).
Los `nvidia-*.service` son solo de esta PC.

Servicios de usuario (`systemctl --user`): ver doc 02.

## Grupos del usuario

`wheel input video audio storage lp rfkill network sys uucp i2c users nopasswdlogin`.
- `input` hace falta para `ydotool`/`xremap` (inyectar teclas vía `/dev/uinput`).
- `i2c` era para control de brillo de monitores externos por DDC (en laptops el brillo de la pantalla interna va por backlight, no hace falta).
- `nopasswdlogin` lo crea el instalador para autologin; revisar si se quiere.
- Hay un grupo `companion` (gid 1001) creado a mano/por algún paquete; no es necesario replicarlo salvo que el doc 03/04 lo pida.

## Archivos de /etc tocados

| Archivo | Qué tiene | ¿Copiar a laptop? |
|---|---|---|
| `/etc/greetd/config.toml` | login con noctalia-greeter | Sí |
| `/etc/logid.cfg` | botones del M720 (doc 03) | Sí |
| `/etc/vconsole.conf`, `/etc/locale.conf` | idioma/teclado | Lo pone el instalador |
| `/etc/profile.d/Hyprland.sh` | exporta `GBM_BACKEND=nvidia-drm` **solo si** hay módulo nvidia sin i915/amdgpu | Inofensivo en Intel (no hace nada); lo trae el paquete, no copiar |
| `/etc/limine-snapper-sync.conf` | `LIMIT_USAGE_PERCENT=85`, `RESTORE_METHOD=replace` | Opcional. Hay un `.pacnew` pendiente que solo agrega `EXCLUDE_SNAPSHOT_ENTRIES="Windows*, windows*"` |
| `/etc/fstab` | incluye `/mnt/backups` (disco exFAT externo, `nofail`) | **No** copiar: los UUID cambian. Solo agregar la línea del disco de backups si se usa en esa laptop |

## Google Drive

`rclone` con remote `gdrive:` montado en `~/GoogleDrive` por `rclone-gdrive.service` (usuario). El `rclone.conf` tiene tokens: **no** está en este respaldo; en la laptop se recrea con `rclone config` (tipo `drive`, nombre `gdrive`). Detalle en doc 02.
