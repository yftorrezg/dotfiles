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
4. Activar el aviso de rclone: `systemctl --user daemon-reload && systemctl --user enable --now rclone-aviso-clientid.timer`.

## 2. Paquetes nuevos
```
sudo pacman -S --needed fuse2 kimageformats qt6-imageformats
pipx install edge-tts gallery-dl      # si no están (pipx list)
```
No instalar: `keyd`, `ckb-next`, `firefox`, `alacritty` (la PC los quitó/son solo PC), nada `nvidia*`.

## 3. Lo que no va en git: apuntes, planes, guías (del paquete de Drive)
Paquete: Drive `LaptopPcOptimizaciones/migracion-cachyos-hyprland/migracion-cachyos-2026-10-06.tar.zst` (53 MB).
```
mkdir -p ~/migracion-2026-10-06 && cd ~/migracion-2026-10-06
rclone copy "gdrive:LaptopPcOptimizaciones/migracion-cachyos-hyprland/migracion-cachyos-2026-10-06.tar.zst" .   # o bajarlo desde Drive web
tar --zstd -xf migracion-cachyos-2026-10-06.tar.zst
P=~/migracion-2026-10-06/migracion-cachyos
```
Restaurar **sin pisar lo que la laptop tenga más nuevo** (`-u` = solo si el del paquete es más reciente):
```
rsync -au "$P/apuntes/Videos/" ~/Vídeos/                        # 1.092 apuntes/resúmenes/tarjetas .md + .tsv
rsync -au "$P/apuntes/Vault/" ~/"Documentos/Obsidian Vault"/
rsync -au "$P/guias-usuario/" ~/Documentos/                     # incluye atajos-y-mouse.md y la guía de auto-captura
mkdir -p ~/.claude/plans && rsync -au "$P/claude-planes/" ~/.claude/plans/
```
`$P/proyectos-md/<proyecto>/` = `CLAUDE.md` y docs de cada proyecto: copiarlos solo dentro de los proyectos que el usuario
tenga clonados en la laptop (preguntar cuáles; la tesis se clona con `gh repo clone yftorrezg/Ciego ~/Proyectos/Ciego`).
**No** copiar `dotfiles/` ni `system/` del paquete: la config ya la gestiona chezmoi (sería pisar la variante de laptop).

**Capturas WebP de los cursos (31 GB)** no vienen: los apuntes se ven con imágenes rotas. Cuando la laptop y la PC estén en la
misma red: `rsync -avP yafer@<ip-PC>:"Vídeos/Capturas de YouTube/" ~/"Vídeos/Capturas de YouTube"/` (preguntar antes; necesita sshd en la PC).

## 4. Verificar
- `bash ~/.local/share/chezmoi/laptop/auditoria.sh` → todo ✔.
- Probar: SUPER+I (estudio), SUPER+ALT+V (tests), SUPER+R (lectura), SUPER+ALT+Z (dictado), SUPER+1..5, Gwenview (A/D, fondo oscuro).
- Leer `docs/migracion/docs/09-sincronizar-y-mantener.md` (§2: el usuario debe crear su **client_id propio de rclone**; el compartido se retira en 2026).
- Al terminar: actualizar la memoria `migracion-laptops.md` con «laptop al día con la PC al 06-10» y `dotsync`.
