# CLAUDE.md — repo `dotfiles` de yafer (PC + laptop)

Responde SIEMPRE en español. El usuario quiere entender el porqué (explica breve), prefiere que le
propongas los cambios grandes antes de hacerlos y usa atajos de mano izquierda.

## Qué es este repo
Fuente de **chezmoi** con la config de `$HOME` de dos equipos CachyOS + Hyprland 0.56 (config en **Lua**,
shell noctalia, fish). Se sincroniza por GitHub privado `yftorrezg/dotfiles` con `dotsync`.

| Equipo | hostname | `.equipo` | Hardware |
|---|---|---|---|
| PC de escritorio (casa) | `yf` | `pc` | i7-6700K, NVIDIA GTX 980 (driver 580xx), DP-3 + HDMI-A-1 vertical, mic USB Maono |
| Laptop ThinkPad E14 Gen4 (facultad) | `yafer` | `laptop` | i7-1255U, Iris Xe, eDP-1 1920x1080 escala 1 (+ Arzopa opcional), teclado UK `gb`+`extd`, batería tope 80% |
| Surface Pro 6 (casa) | `yf-s` | `surface` | Kaby Lake-R, UHD Graphics 620, eDP-1 2736x1824 escala 2, Type Cover teclado `es` |

`chezmoi execute-template '{{ .equipo }}'` dice en cuál estás.

## Cómo está organizado
- **Común** (igual en ambos): todo lo normal de chezmoi (`dot_config/...`, `dot_local/...`), incluida la
  memoria de Claude (`dot_claude/projects/-home-yafer/memory/`) → las memorias viajan entre equipos.
- **Por equipo**: los archivos listados en `.hosts-lista`. Su fuente real es `.hosts/<pc|laptop>/<ruta>`;
  en el árbol de chezmoi solo hay un `.tmpl` de una línea que hace `include` de la variante del equipo.
  Hoy: `hyprland.lua`, `config/{environment,variables,monitors,workspaces,inputs,misc,decorations,animations,autostart,binds_equipo}.lua`,
  scripts de voz (`leer-seleccion.sh`, `piper-daemon.py`, `elegir-voz.py`, `voz.conf`, `piper-voz-daemon.service`),
  `progreso.py`, `carpeta-capturas.conf`, `hyprwhspr/config.json`, `noctalia/config.toml`,
  `.local/state/noctalia/settings.toml`, `brave-flags.conf`, `btop.conf`, gtk `settings.ini`/`.gtkrc-2.0`,
  `mpv.conf`, `obsidian.json`, perfil OpenDeck `Escritorios.json`.
- **Atajos**: `config/binds.lua` es COMÚN (un atajo nuevo llega a los dos). Lo que depende de monitores
  (escritorios virtuales, mover entre pantallas, SUPER+Tab, teclas Fn) está en `config/binds_equipo.lua` (por equipo),
  que `binds.lua` carga con `require("config.binds_equipo")`.
- **Solo laptop** (`.chezmoiignore`): `config/escritorios.lua` (tabla global `VD`: monitores dinámicos, tapa) y `mpv/scripts/bateria.lua`.
- **Windows 11 de la laptop ThinkPad (SOLO ese Windows; no es la PC ni el CachyOS)** (`windows/`, ignorado por chezmoi, ver `windows/README.md`): AutoHotkey v2 (`ahk/yafer.ahk` = los mismos atajos de `binds.lua`),
  pwsh 7 + Windows Terminal, mpv (unión `%APPDATA%\mpv` → `windows/mpv`), SUPER+R con edge-tts (usa el `limpiar-texto.py` común),
  `winget/thinkpad.dsc.yaml`, `bootstrap.ps1`. Si cambias un atajo común en `binds.lua`, refléjalo en `yafer.ahk` y `ATAJOS-WINDOWS.md`.
  Lo pesado (doblar, auto-captura, cuadernillos, `estudiar.py`) queda solo en CachyOS.
- **Generados por noctalia** (temas de btop/gtk/kitty/qt/kdeglobals/color-schemes/mic-osd): NO se sincronizan (`.chezmoiignore`).
  Noctalia los calcula del fondo de pantalla, así que cada equipo genera los suyos; sincronizarlos hacía ping-pong entre PC y laptop.
  Si algún día se usa el mismo fondo en ambos, salen iguales solos.
- **Nunca se sincroniza**: `/etc`, secretos (rclone.conf, pass de restic, tokens gh), paquetes, datos, `.local/state/mpv`, plugins de OpenDeck, iconos.
- `docs/migracion/` = documentación completa de la PC (docs 01-08, GAPS, LIMPIEZA, paquetes). `laptop/` = scripts usados
  para migrar la laptop + `auditoria.sh`. `docs/base-pc-29-09/` = versión de la PC al 29-09 de los archivos comunes que la
  laptop mejoró (base para fusión a 3 vías). `pc/fusion-inicial.sh` = primer paso en la PC.

## Reglas al editar config
1. Edita en `$HOME` (lo vivo) y luego `dotsync subir`; o edita la fuente y `chezmoi apply`. Nunca dejes `$HOME` y la fuente divergentes.
2. Archivo nuevo que deba sincronizarse: `chezmoi add <ruta>`. Si depende del hardware → agrégalo a `.hosts-lista`,
   crea las dos variantes en `.hosts/pc/` y `.hosts/laptop/` y reemplaza la fuente por el `.tmpl` de `include` (copia uno existente).
3. Antes de aplicar Lua: `luac -p`. Tras aplicar: `hyprctl reload` y `hyprctl configerrors` vacío.
   `hyprctl dispatch` usa sintaxis Lua: `hyprctl dispatch 'hl.dsp.focus({ workspace = "name:estudio" })'`.
   `code:NN` en binds Lua: en la laptop falló; en la PC funciona (mouse Scimitar, `code:192–202`). Para atajos comunes usa keysyms.
4. Nunca subas secretos (`gitleaks`-style: chezmoi avisa; la clave de OpenSubtitles en uosc/main.lua es pública, OK).
5. Commits en español, cortos. `dotsync` hace commit/push solo.

## dotsync (`~/.local/bin/dotsync`)
`auto` (timer cada 30 min + al iniciar sesión) = captura cambios locales → commit → `git rebase origin/main` →
valida Lua/JSON/TOML → `chezmoi apply` → push. Si hay **conflicto** (misma línea editada en ambos equipos) aborta el
rebase sin tocar nada y notifica. Para resolver: `cd ~/.local/share/chezmoi && git fetch && git rebase origin/main`,
arreglar los archivos marcados, `git add`, `git rebase --continue`, `chezmoi apply`, `git push`.
Se niega a correr si falta `.hosts/<equipo>/.fusion-inicial-hecha` (protege a la PC hasta la fusión inicial).

**Captura = solo la 1ª columna de `chezmoi status`** (cambiado en `$HOME` desde el último apply). La 2ª columna es lo que
trae el repo. (Bug del 06-10, ya corregido: capturar con `chezmoi re-add` a secas, con el repo adelantado y sin aplicar,
"revirtió" 44 archivos de la PC; se arregló con `git revert`.) Nunca hagas `chezmoi re-add` global con el repo adelantado:
primero `chezmoi apply`, o re-add solo de rutas concretas con 1ª columna `M`.

## Estado (06-10-2026, tarde)
- Laptop: migrada, auditada (`laptop/auditoria.sh`), timer activo. **Pendiente: seguir `laptop/ACTUALIZAR-2026-10-06.md`** (paquetes nuevos, apuntes .md del paquete de Drive, timer de aviso de rclone).
- **PC: fusión inicial HECHA el 06-10** (PC = base + arreglos de la laptop). Decisiones del usuario: estudiar.py = **SUPER+I** en ambos
  (SUPER+ALT+B eliminado), pomodoro **sin atajo**. Mouse Corsair Scimitar (keyd, binds `code:192–202`) = solo PC, en
  `.hosts/pc/.config/hypr/config/binds_equipo.lua`; sus scripts y ckb-next se ignoran en la laptop (`.chezmoiignore`).
  En la PC `code:NN` SÍ funciona en binds Lua (probado con `hyprctl binds`).
- La PC es donde se hacen las mejoras continuas; la laptop se usa fuera de casa (facultad).
- `docs/migracion/` = paquete del 06-10 (incluye doc 09: sync, apuntes, client_id de rclone). Apuntes/planes no van en git: paquete de Drive.

## Fusión inicial en la PC (hacer UNA vez, con el usuario)
Precondición: el usuario corrió `pc/fusion-inicial.sh` (respaldo en `~/respaldo-antes-dotsync-*.tar`, repo clonado sin aplicar,
`~/dotsync-fusion-*/status.txt` y `diff.patch`). En `chezmoi diff`, `-` = lo que hay en la PC hoy, `+` = lo que pondría el repo.
La **PC es la verdad** para sus avances; la laptop aporta arreglos. Para cada archivo de `status.txt`:
1. **Por equipo** (está en `.hosts-lista`): copia el archivo actual de la PC a `.hosts/pc/<ruta>` (gana la PC).
   Excepciones:
   - `binds.lua` de la PC está ENTERO (sin separar). Sepáralo igual que en la laptop: lo que depende de monitores
     (bloque "WORKSPACES & MONITORS" hasta "-- Workspaces con nombre", SUPER+SHIFT+1/2, SUPER+Tab) va a
     `.hosts/pc/.config/hypr/config/binds_equipo.lua` (ya hay una versión del 29-09 de referencia); el resto se fusiona con
     el `binds.lua` común.
     Atajos nuevos de la PC posteriores al 29-09 → al común, salvo que dependan de monitores.
   - Si la PC agregó atajos/funciones que también sirven en la laptop dentro de un archivo por equipo, pórtalos a
     `.hosts/laptop/` y avisa al usuario.
2. **Común mejorado por la laptop** (`docs/base-pc-29-09/LISTA.txt`, "COMUN-MEJORADO"): fusión a 3 vías
   `git merge-file <copia-de-PC-actual> docs/base-pc-29-09/<ruta> <fuente-común-del-repo>` (base = 29-09). Resuelve
   conflictos conservando los avances de la PC + los arreglos de la laptop. Resultado → fuente común (`chezmoi add` desde $HOME tras escribirlo).
   Ojo `app-web.sh`: usa `hyprctl eval 'VD...'` con respaldo al método de la PC si `VD` no existe — debe seguir funcionando en la PC.
3. **Común sin cambios de la laptop**: gana la PC → `chezmoi re-add <ruta>` (o `chezmoi add`).
4. **Archivos nuevos en la PC** que no estén en el repo (scripts nuevos en `~/.config/hypr/scripts/`, configs nuevas): revisa
   que no tengan secretos y `chezmoi add`. Si dependen del hardware, trátalos como "por equipo".
5. Verifica: `chezmoi diff` en la PC debe quedar vacío (o solo con los arreglos de la laptop que el usuario aceptó).
   `chezmoi apply`, `hyprctl reload`, `hyprctl configerrors` vacío, prueba SUPER+1..5, SUPER+R, dictado (SUPER+ALT+Z), SUPER+I.
6. `touch .hosts/pc/.fusion-inicial-hecha`, `git add -A && git commit -m "pc: fusión inicial" && git push`, `dotsync activar`.
7. Actualiza la sección "Estado" de este archivo y la memoria `migracion-laptops.md`.

La laptop recibirá los avances comunes de la PC en su siguiente `dotsync` (≤30 min). Revisa allí con `laptop/auditoria.sh`.
