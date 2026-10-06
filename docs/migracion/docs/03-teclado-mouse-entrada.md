---
tags: [sistema, entrada]
actualizado: 2026-09-26
---
# 03 — Teclado, mouse y dispositivos de entrada

> Documento para otra instancia de Claude que va a montar esto en una laptop (Surface Pro 6 o ThinkPad E14 Gen4, ambas Intel) sin tener contexto. Origen: PC de escritorio CachyOS + Hyprland 0.56 (config en **Lua**), usuario `yafer`. Datos tomados el 2026-09-26.
>
> Los archivos copiados están en `~/migracion-cachyos/dotfiles/` (rutas relativas a `$HOME`) y en `~/migracion-cachyos/system/etc/` (rutas de `/etc`).

---

## 1. Resumen rápido

| Pieza | Qué hace | ¿Llevarla a la laptop? |
|---|---|---|
| `logiops` (`logid`, en /etc/logid.cfg) | Remapea botones del mouse **Logitech M720** | **Sí**, si va a usar el M720 |
| `99-logid-m720.rules` (udev) | Reinicia `logid` cuando el M720 se (re)conecta por BT | Sí, junto con logiops |
| `xremap` (servicio de usuario) | Capa de remapeo por aplicación. **Ahora mismo está vacía** (sin reglas) | Opcional (ver §4) |
| `solaar` | Instalado, **no se ejecuta**. Solo quedó su config en caché | No hace falta; no correrlo a la vez que logid |
| `teclas-fantasma` (servicio de usuario + script Python) | Diagnóstico: registra qué dispositivo envía teclas de suspender/apagar | **No** en laptop (ver §5) |
| `logind.conf.d/no-teclas-fantasma.conf` | Ignora botón de encendido y tecla de suspender | **NO copiar tal cual en laptop** (ver §5) |
| `ydotool` (servicio de usuario) | Teclado/ratón virtual; lo usa el atajo SUPER+R (lectura) | Sí |
| OpenDeck + reglas udev Stream Deck | Software para Elgato Stream Deck XL y clones (AKP153, Fifine D6) | Solo si conecta el Stream Deck a la laptop |
| Autosuspend BT desactivado (modprobe) | Evita que el K380/M720 se desconecten | Útil, pero en laptop cuesta algo de batería |

Grupos del usuario en la PC: `yafer sys network i2c nopasswdlogin rfkill users video uucp storage lp input audio wheel companion`.
El importante para esta área es **`input`** (xremap, teclas-fantasma y ydotool leen/escriben `/dev/input/*` y `/dev/uinput`). `companion` es un resto de Bitfocus Companion (ya no está instalado; no hace falta).

---

## 2. Distribución de teclado (¡ojo, hay una discrepancia!)

- Consola/TTY y X11 (`/etc/vconsole.conf`, `/etc/X11/xorg.conf.d/00-keyboard.conf`, `localectl`): **`es`** (España), modelo `pc105`.
- **Hyprland NO define `kb_layout`** en `inputs.lua`, así que usa el valor por defecto **`us`**. `hyprctl devices` confirma `l "us"` / "English (US)" en todos los teclados. O sea: en la sesión gráfica el usuario escribe con distribución **US**, aunque el sistema diga `es`.
- Repetición: por defecto de Hyprland (`repeat_rate 25`, `repeat_delay 600`); no está personalizada.
- Teclados vistos en la PC: SiGma Micro "TRACER Gamma Ivory" (USB, es el teclado principal ahora), Logitech K380 (Bluetooth), receptor "CX 2.4G".

**No sé** qué distribución física tienen el K380, el Type Cover de la Surface ni el teclado de la ThinkPad (ES, LATAM o US). **Pregúntale al usuario** antes de tocar nada. Si el teclado interno es ES/LATAM y quiere seguir con US en el K380, lo más limpio es poner ambas distribuciones con tecla de cambio, p. ej. en `inputs.lua`:

```lua
hl.config({
    input = {
        kb_layout  = "us,es",            -- o "us,latam" según el teclado físico
        kb_options = "grp:alt_shift_toggle",
        accel_profile = "flat",
    },
})
```

(También se puede asignar distribución por dispositivo; revisa la sintaxis de "per-device input config" en la wiki de Hyprland para la API Lua de la versión instalada, no la inventes.)

---

## 3. Mouse Logitech M720 Triathlon — logiops

Archivo: `/etc/logid.cfg` → copia en `system/etc/logid.cfg`.

| Botón M720 (CID) | Acción configurada | Qué dispara en Hyprland (`binds.lua`) |
|---|---|---|
| Botón de gestos del pulgar (`0xd0`) | `Super+Shift+S` | `~/.config/hypr/scripts/captura-portapapeles.sh` (captura a portapapeles) |
| Click de la rueda / central (`0x52`) | `Ctrl+Shift+S` | `~/.config/hypr/scripts/captura-guardar.sh` (captura a archivo). **Reemplaza el click medio nativo** (pegar selección, abrir enlace en pestaña nueva, etc.) |
| Inclinar rueda a la izquierda (`0x5b`) | `Ctrl+Shift+Tab` | Pestaña anterior |
| Inclinar rueda a la derecha (`0x5d`) | `Ctrl+Tab` | Pestaña siguiente |
| Atrás / Adelante (`0x53` / `0x56`) | Sin tocar (nativo) | — |
| SmartShift | Activado, umbral 15 | Rueda libre al girar rápido |

Notas del propio archivo: los gestos direccionales del botón del pulgar **no funcionan** con el M720 en logiops (bug https://github.com/PixlOne/logiops/issues/450), por eso cada botón es una tecla fija.

Hyprland: `accel_profile = "flat"` (sin aceleración) para todos los punteros. En la laptop eso afecta también al touchpad; si el touchpad se siente lento, sube `sensitivity` o usa config por dispositivo.

### Reconexión
`logid` no reintenta si el mouse estaba dormido al arrancar. Solución aplicada: regla udev `/etc/udev/rules.d/99-logid-m720.rules`:

```
ACTION=="add", SUBSYSTEM=="hidraw", KERNELS=="0005:046D:B015.*", RUN+="/usr/bin/systemctl --no-block restart logid.service"
```
(`0005` = bus Bluetooth; `046D:B015` = M720). Si el usuario conecta el M720 por **receptor Unifying** en vez de BT, el `KERNELS` será distinto (bus `0003`, y el dispositivo cuelga del receptor) y habría que ajustar la regla.

Existe además `/etc/systemd/system/logid-restart-m720.service` (copia en `solo-esta-pc/`) (oneshot, espera 3 s y reinicia logid) pero **no lo usa nada** (la regla udev reinicia logid directamente). Es un resto; no hace falta copiarlo.

En el log de logid aparece también el K380 (`Device found: ... K380`) con un `Device timed out` al añadirlo: es inofensivo (no hay config para el K380 en logid.cfg).

### Reinstalar
```bash
paru -S logiops            # AUR (no está en repos de CachyOS/Arch). Versión en la PC: 0.3.5-1
sudo cp ~/migracion-cachyos/system/etc/logid.cfg /etc/logid.cfg
sudo cp ~/migracion-cachyos/system/etc/udev/rules.d/99-logid-m720.rules /etc/udev/rules.d/
sudo udevadm control --reload
sudo systemctl enable --now logid.service
journalctl -u logid -f      # debe decir "Device found: M720 Triathlon ..."
```

### Solaar
`solaar` 1.1.20 (repo `extra`) está instalado pero **no corre** (ni autostart ni servicio). `~/.config/solaar/config.yaml` solo es la caché de ajustes del M720 (`divert-keys` todo a 0). Su paquete aporta la regla udev `/usr/lib/udev/rules.d/42-logitech-unify-permissions.rules` (permisos del receptor Unifying), útil si se usa receptor. Instalarlo es opcional (`sudo pacman -S solaar`), sirve para ver batería/emparejar con el receptor. **No dejarlo corriendo a la vez que logid**: ambos pelean por el desvío (divert) de botones.

---

## 4. xremap

- Paquete: `xremap-hypr-bin` 0.15.9 (AUR), variante con soporte Hyprland para reglas por aplicación.
- Servicio de usuario: `~/.config/systemd/user/xremap.service` → `ExecStart=/usr/bin/xremap --allow-launch true %h/.config/xremap/config.yml`, `WantedBy=graphical-session.target`.
- Config: `~/.config/xremap/config.yml` → **`modmap: []` y `keymap: []`**. No remapea nada; se dejó corriendo "por si acaso" para futuras reglas por app (el archivo trae un ejemplo comentado).
- Efecto secundario: xremap hace *grab* de todos los teclados y los re-emite por un dispositivo virtual `xremap`. Esto confunde el diagnóstico (todo parece venir de "xremap").

Recomendación para la laptop: **no es necesario**. Si el usuario lo quiere igual:
```bash
paru -S xremap-hypr-bin
# requiere estar en el grupo input y acceso a /dev/uinput (lo da la regla 80-uinput.rules de ydotool)
systemctl --user enable --now xremap.service
```
Con la pantalla táctil/pluma de la Surface, conviene vigilar que xremap no capture dispositivos que no debe (si hay problemas, limitar con `--device`).

---

## 5. `teclas-fantasma` — qué es y por qué existe

**Motivo:** el 22 y 23 de septiembre de 2026 logind recibió "Suspend key pressed" / "Power key pressed" sin que nadie tocara nada, y la PC se suspendió/apagó.

**Qué se hizo:**
1. `~/.local/bin/teclas-fantasma.py` (usa `python-evdev`) + servicio de usuario `teclas-fantasma.service` (`Restart=always`, `WantedBy=default.target`). Escucha todos los `/dev/input/event*` que tengan KEY_SLEEP/KEY_POWER/KEY_SUSPEND/KEY_WAKEUP (reescanea cada 2 s para dispositivos BT que se conectan después) y anota en `~/.local/state/teclas-fantasma.log` quién la envió.
2. `/etc/systemd/logind.conf.d/no-teclas-fantasma.conf`:
   ```ini
   [Login]
   HandleSuspendKey=ignore
   HandlePowerKey=ignore
   ```

**Hallazgos del log (hasta el 26-sep):**
- `KEY_POWER` desde **`Power Button` (LNXPWRBN, el botón ACPI del chasis)** el 23-sep 17:23 y el 25-sep 15:26 → el "fantasma" parece ser el **botón de encendido físico de la PC de escritorio** (cable/pulsador del frontal), no un teclado.
- `KEY_WAKEUP` desde un "Bluetooth Keyboard" (Samsung, `04E8:7021`) → inofensivo.
- Ningún evento del K380 ni del M720.

**En laptop:** el problema es del hardware de la PC. **No copies `no-teclas-fantasma.conf`**: en una laptop el usuario casi seguro quiere que el botón de encendido y la tapa funcionen (suspender al cerrar la tapa es el comportamiento por defecto de logind, y este archivo no lo toca, pero `HandlePowerKey=ignore` dejaría el botón de encendido muerto). Tampoco hace falta el servicio `teclas-fantasma`. Los archivos están en `solo-esta-pc/`, solo como referencia.

---

## 6. Bluetooth

- `bluez` 5.87 + `bluez-utils`; `bluetooth.service` habilitado. Sin blueman (la UI la da noctalia-shell, probablemente).
- `/etc/bluetooth/main.conf` e `input.conf`: **por defecto**, sin cambios.
- `/etc/modprobe.d/disable_btusb-autosuspend.conf`: `options btusb enable_autosuspend=0` → evita que el adaptador BT USB se duerma y desconecte K380/M720. En laptop cuesta un poco de batería; si hay desconexiones del K380/M720, ponerlo. (`/etc/udev/rules.d/50-bluetooth-no-autosuspend.rules` existe pero está **vacío**.)
- Dispositivos emparejados (solo nombres): **Keyboard K380**, **M720 Triathlon**, JBL Clip 4, y dos "Bluetooth Keyboard" (Samsung).
- Los emparejamientos **no se migran** (las claves en `/var/lib/bluetooth` dependen del adaptador). Hay que re-emparejar en la laptop:
  ```bash
  bluetoothctl
  power on; agent on; default-agent; scan on
  pair <MAC>; trust <MAC>; connect <MAC>
  ```
  **K380 y M720 son multi-dispositivo** (botones Easy-Switch 1/2/3 en ambos): conviene emparejar la laptop en **otro canal** distinto al de la PC y así cambiar con un botón sin re-emparejar. El M720 también puede usar su receptor Unifying.

---

## 7. ydotool

`ydotool` 1.0.4 (repo) con servicio de **usuario** `ydotool.service` habilitado (`systemctl --user enable --now ydotool`). Se usa en el atajo SUPER+R (lectura en voz alta en webviews de VS Code, donde wtype no funciona). Su paquete trae `/usr/lib/udev/rules.d/80-uinput.rules` (`/dev/uinput` → grupo `input`, 0660). `wtype` también está instalado.

---

## 8. Stream Deck / OpenDeck (periféricos extra)

- `opendeck-bin` 2.14.0 (AUR). Autostart con `~/.config/autostart/opendeck.desktop` (`opendeck --hide`). SUPER+K abre la ventana.
- Dispositivos con perfil: Elgato Stream Deck XL (`sd-A00NA538346JSS`), un clon AKP153 (`99-...-293S`), FIFINE AmpliGame D6 (`d6-...`).
- Copiado entero `~/.config/opendeck` (79 MB, 77 MB son plugins).
- Reglas udev: `40-streamdeck.rules` (la instala el paquete), `40-opendeck-akp153.rules` y `40-opendeck-ampgd6.rules` (manuales, de los plugins). `50-companion-headless.rules` y `70-apple-restore.rules` son restos de Bitfocus Companion y de restaurar iPhone/iPad; no hacen falta para lo básico.
- Solo instalar en la laptop si el usuario va a conectar el Stream Deck ahí.

---

## 9. Hyprland: gestos y config de entrada actual

`~/.config/hypr/config/inputs.lua` (copiado):

```lua
hl.config({ input = { accel_profile = "flat" } })

hl.gesture({ fingers = 4, direction = "horizontal", action = "workspace" })
hl.gesture({ fingers = 3, direction = "down",       action = "close" })
hl.gesture({ fingers = 3, direction = "up",         action = "fullscreen" })
hl.gesture({ fingers = 3, direction = "left",       action = "float" })
```

En la PC no hay touchpad, así que estos gestos **nunca se han usado de verdad**. Atención: **3 dedos hacia abajo = cerrar ventana**, fácil de disparar sin querer en un touchpad.

---

## 10. En laptop

### 10.1 Touchpad (ThinkPad E14 Gen4 y Type Cover de la Surface)
Hyprland por defecto ya tiene `tap-to-click = true` y `natural_scroll = false`. Propuesta para `inputs.lua` (confirmar preferencias con el usuario):

```lua
hl.config({
    input = {
        accel_profile = "flat",          -- para el mouse; ver nota abajo
        touchpad = {
            natural_scroll = true,
            ["tap-to-click"] = true,
            disable_while_typing = true,
            clickfinger_behavior = true,   -- 2 dedos = click derecho, 3 = medio
        },
    },
})

-- Cambiar de workspace con 3 y/o 4 dedos en horizontal
hl.gesture({ fingers = 3, direction = "horizontal", action = "workspace" })
hl.gesture({ fingers = 4, direction = "horizontal", action = "workspace" })
```

- Si se añade el gesto de 3 dedos horizontal, **quitar** el de `fingers = 3, direction = "left", action = "float"` (choca) y considerar quitar el de "cerrar ventana".
- `accel_profile = "flat"` global hace que el touchpad se sienta lento; mejor dejarlo "flat" solo para el mouse con config por dispositivo, o usar `adaptive` para el touchpad.
- Verifica los nombres de opciones con `hyprctl getoption input:touchpad:natural_scroll` etc. y los nombres de dispositivos con `hyprctl devices` en la laptop.
- ThinkPad E14 Gen4: **no tiene TrackPoint**, solo touchpad (funciona con libinput sin nada extra). Lector de huellas: `fprintd` ya está instalado en la PC (pregunta si lo quiere usar en la ThinkPad).

### 10.2 Surface Pro 6: pantalla táctil, pluma y Type Cover
Lo que se sabe (verificar en la máquina, no se pudo probar desde la PC):
- El **Type Cover** (teclado + touchpad) funciona con el kernel normal en general.
- La **pantalla táctil y la pluma** de la Surface Pro 6 usan IPTS (Intel Precise Touch & Stylus). Para que funcionen bien hace falta el proyecto **linux-surface**: su kernel (`linux-surface`) + el daemon **`iptsd`** (+ `libwacom-surface` para la pluma). Nada de esto está en los repos de CachyOS/Arch (comprobado: `pacman -Ss linux-surface` / `iptsd` no devuelve nada en la PC).
- Hay que añadir el **repo de linux-surface** a `/etc/pacman.conf` según https://github.com/linux-surface/linux-surface/wiki/Installation-and-Setup (sección Arch): importar su clave GPG, añadir `[linux-surface]` con `Server = https://pkg.surfacelinux.com/arch/`, e instalar `linux-surface linux-surface-headers iptsd` (y `libwacom-surface`, opcional `linux-firmware-marvell` para el WiFi). Después añadir la entrada de arranque del kernel nuevo (el sistema usa **Limine** + limine-snapper-sync; revisar el documento de arranque).
- Consecuencia: en la Surface se usaría el kernel `linux-surface` en vez del `linux-cachyos` (se pierden los parches de CachyOS). Comprueba en la wiki de linux-surface si hay alguna forma soportada de mantener el kernel CachyOS; no lo asumas.
- En Hyprland: la táctil aparece en `hyprctl devices` bajo `Touch:` y la pluma bajo `Tablets:`. Para que coincidan con la pantalla rotada/escalada, usa `input:touchdevice:output` / `input:tablet:output` (nombre del monitor, p. ej. `eDP-1`). Para gestos táctiles en pantalla existe el plugin **hyprgrass** (no instalado en la PC; AUR `hyprgrass-git` o `hyprpm`). Para teclado en pantalla: `squeekboard` (repo) o `wvkbd` (AUR) (tampoco instalados).
- Rotación automática: requiere `iio-sensor-proxy` (repo) + algún script/daemon, p. ej. `iio-hyprland-git` (AUR) (no hay nada configurado en la PC).

### 10.3 Teclado interno vs K380
- Los dos pueden coexistir; Hyprland aplica el mismo `kb_layout` a todos salvo config por dispositivo. Decidir con el usuario la distribución (ver §2).
- La fila F del K380 funciona por defecto como teclas multimedia; logiops **no** tiene config para el K380 (solo lo detecta). Si quiere F1–F12 directas, el K380 permite Fn+Esc (según modelo) o se puede configurar desde Solaar (`fn-swap`).
- Los atajos de Hyprland de volumen/brillo (`XF86Audio*`, `XF86MonBrightness*`) ya están en `binds.lua` y llaman a noctalia; en laptop el brillo de la pantalla interna funcionará con las teclas Fn del teclado interno.

### 10.4 Checklist de servicios en la laptop
```bash
sudo usermod -aG input yafer           # cerrar sesión después
sudo systemctl enable --now bluetooth
sudo systemctl enable --now logid       # si usa el M720 (tras instalar logiops y copiar logid.cfg + regla udev)
systemctl --user enable --now ydotool
# opcionales:
systemctl --user enable --now xremap    # config vacía; solo si lo pide
# NO: teclas-fantasma.service ni no-teclas-fantasma.conf
# Surface: sudo systemctl enable --now iptsd@...  (ver wiki linux-surface; en versiones recientes iptsd se lanza por udev)
```

---

## 11. Paquetes (versiones en la PC)

| Paquete | Versión | Origen |
|---|---|---|
| logiops | 0.3.5-1 | AUR |
| xremap-hypr-bin | 0.15.9-1 | AUR |
| opendeck-bin | 2.14.0-1 | AUR |
| solaar | 1.1.20-2 | extra |
| python-evdev | 2.0.0 | repo (solo para teclas-fantasma) |
| bluez / bluez-utils | 5.87 | repo |
| libinput | 1.32.0 | repo |
| ydotool / wtype | 1.0.4 / 0.4 | repo |
| hyprland | 0.56.2 | repo CachyOS |

No instalados: keyd, interception-tools, iptsd, linux-surface, libwacom-surface, hyprgrass, touchegg/fusuma/libinput-gestures. No existe `~/.claude/keybindings.json`.
