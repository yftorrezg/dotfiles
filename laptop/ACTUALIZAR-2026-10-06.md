# Laptop: ponerse al día con la PC (06-10-2026)

> **Claude en la laptop:** el usuario te dirá «lee `~/.local/share/chezmoi/laptop/ACTUALIZAR-2026-10-06.md` y hazlo».
> Hazlo entero, explicando breve el porqué. Propón antes cualquier paso que borre o sobrescriba datos del usuario.

La PC hizo la **fusión inicial** el 06-10 (PC = base, + los arreglos de la laptop). La **config** llega sola con `dotsync`;
lo que NO va en git (apuntes, planes, paquetes) se trae del paquete de Drive.

## 1. Config (automático)
1. `dotsync` (o esperar ≤30 min). Debe terminar sin "CONFLICTO".
2. `hyprctl reload && hyprctl configerrors` → vacío.
3. Qué cambió para la laptop:
   - **SUPER+I = centro de estudio** (`estudiar.py`) en los dos equipos. **SUPER+ALT+B ya no existe** (la PC lo tenía en SUPER+I desde el 29-09).
   - **Pomodoro sin atajo** (el usuario no lo usa; sigue en el Stream Deck).
   - VS Code ya no se fija al escritorio 4 (`windowrules.lua`).
   - `curso-abrir.sh`, backup, rclone y doblar: quedan las versiones mejoradas de la laptop (ya eran tuyas).
   - Nuevos comunes: `xremap` (config vacía, no hace falta activarlo), `qt5ct/colors`, `opencode.desktop`, `doblar-estado`,
     **`rclone-aviso-clientid` (script + service + timer)**.
   - Solo PC (la laptop los ignora por `.chezmoiignore`): mouse Scimitar (`mouse-*.sh`, `keyd-scimitar.conf`, binds `code:192–202`
     en `.hosts/pc/.../binds_equipo.lua`), ckb-next.
   - Memorias de Claude fusionadas (incluye `ahorro-cuota.md`).
4. **rclone con client_id propio (hecho en la PC el 06-10):** proyecto Google Cloud `rclone-yafer`, app OAuth «En producción» (página en
   `https://yftorrezg.github.io`). En la laptop: copiar `~/.config/rclone/LEEME-llave-google-drive.txt` de la PC (USB o `rsync` por LAN; NUNCA por git/Drive) y leer de ahí el client_id/secret (memoria `rclone-llave-google`). El usuario no gestiona la llave: hazlo tú. Luego
   `rclone config update gdrive client_id <ID> client_secret <SECRETO> --non-interactive && rclone config reconnect gdrive: --auto-confirm`
   (el usuario acepta en el navegador: «Configuración avanzada» → «Ir a rclone»), luego `systemctl --user restart rclone-gdrive`.
5. Activar el aviso de rclone: `systemctl --user daemon-reload && systemctl --user enable --now rclone-aviso-clientid.timer`.

## 2. Paquetes nuevos
```
sudo pacman -S --needed fuse2 kimageformats qt6-imageformats
pipx install edge-tts gallery-dl      # si no están (pipx list)
```
No instalar: `keyd`, `ckb-next`, `firefox`, `alacritty` (la PC los quitó/son solo PC), nada `nvidia*`.

## 3. Apuntes, capturas, planes y llave de rclone: copiar DIRECTO desde la PC por la red de casa
**Cambio 06-10 noche:** la PC unificó las bóvedas de Obsidian. Ya **no existe** `~/Documentos/Obsidian Vault`: todo está en la bóveda
`~/Vídeos` (Karpathy pasó a `~/Vídeos/Capturas de YouTube/Neural Networks： Zero to Hero/`, en WebP como los demás cursos; el React
viejo en PNG quedó archivado en la PC). Por eso NO uses `apuntes/` del tar de Drive (es la versión vieja): copia desde la PC.

**En la PC (lo corre el usuario, abre SSH solo para la red de casa y solo mientras dure la copia):**
```
sudo ufw allow from 192.168.100.0/24 to any port 22 proto tcp && sudo systemctl start sshd
```
IP de la PC al 06-10: `192.168.100.63` (Wi-Fi; si cambió: `ip -4 addr` en la PC).

**En la laptop** (primero una prueba en seco con `-n`, enseñar el resumen al usuario y luego sin `-n`). `-u` = no pisa lo que la laptop
tenga más nuevo; sin `--delete`, nunca borra nada de la laptop:
```
PC=yafer@192.168.100.63
rsync -avhu --info=stats1 -n "$PC:Vídeos/Capturas de YouTube/" ~/"Vídeos/Capturas de YouTube"/   # ~30 GB, capturas + apuntes
rsync -avhu "$PC:Vídeos/Mis cursos.md" ~/Vídeos/
rsync -avhu "$PC:Documentos/" ~/Documentos/ --include='*/' --include='*.md' --exclude='*' --prune-empty-dirs   # guías
rsync -avhu "$PC:.claude/plans/" ~/.claude/plans/
umask 077; mkdir -p ~/.config/rclone && rsync -avh "$PC:.config/rclone/LEEME-llave-google-drive.txt" ~/.config/rclone/
```
Si la laptop tiene un `~/Documentos/Obsidian Vault` viejo de la migración: comparar con lo copiado y, si no tiene nada propio,
quitarlo de `~/.config/obsidian/obsidian.json` (con Obsidian cerrado) para que quede una sola bóveda, igual que en la PC.

**Al terminar, en la PC (cerrar SSH otra vez):**
```
sudo systemctl stop sshd && sudo ufw delete allow from 192.168.100.0/24 to any port 22 proto tcp
```
`$P/proyectos-md/` del tar de Drive: `CLAUDE.md`/docs de proyectos; copiar solo dentro de los proyectos clonados en la laptop.

## 4. Verificar
- `bash ~/.local/share/chezmoi/laptop/auditoria.sh` → todo ✔.
- Probar: SUPER+I (estudio), SUPER+ALT+V (tests), SUPER+R (lectura), SUPER+ALT+Z (dictado), SUPER+1..5, Gwenview (A/D, fondo oscuro).
- Leer `docs/migracion/docs/09-sincronizar-y-mantener.md` (§2: el usuario debe crear su **client_id propio de rclone**; el compartido se retira en 2026).
- Al terminar: actualizar la memoria `migracion-laptops.md` con «laptop al día con la PC al 06-10» y `dotsync`.
