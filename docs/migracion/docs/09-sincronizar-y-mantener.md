---
tags: [sistema, sincronizacion, rclone, apuntes]
actualizado: 2026-10-06
---
# 09 · Sincronizar PC ↔ ThinkPad y mantener todo al día

Destino principal: **ThinkPad E14 Gen4** (i7 12ª gen, 16 GB RAM, Windows 11 500 GB + CachyOS 500 GB). Origen: PC "yf". Este documento dice **dónde está cada cosa** en el paquete, **cómo restaurarla en la ThinkPad** y **qué hacer para que no vuelva a haber desfase**.

## 1. Qué viaja y dónde se restaura

| En el paquete | Se restaura en | Notas |
|---|---|---|
| `dotfiles/` | `~/` (misma ruta relativa) | **Aplicar antes los ajustes de laptop** (README, «Orden de trabajo») |
| `solo-esta-pc/` | no se copia | Mouse Scimitar/keyd, ckb-next, teclas-fantasma, monitores |
| `system/etc/` | `/etc/` con `sudo` | Solo lo indicado en los docs |
| `paquetes/` | `pacman -S --needed - < pacman-repo.txt` (filtrar nvidia/solo-PC), `paru -S - < aur.txt`, `pipx install edge-tts gallery-dl`, extensiones VS Code | Quitar `nvidia*`, `lib32-nvidia*`, `keyd`, `ckb-next` |
| `apuntes/Videos/` | `~/Vídeos/` | 1.092 `.md` + `.tsv` de apuntes, resúmenes, tarjetas y paneles. **Sin las capturas** |
| `apuntes/Vault/` | `~/Documentos/Obsidian Vault/` | Apuntes de «Neural Networks: Zero to Hero» y React |
| `guias-usuario/` | `~/Documentos/` | Incluye `atajos-y-mouse.md` y `Guia-Auto-captura-de-cursos.md` |
| `claude-memoria/` | `~/.claude/projects/-home-<usuario>/memory/` | Las de `proyectos/` van a la carpeta de memoria de cada proyecto |
| `claude-planes/` | `~/.claude/plans/` | 9 planes (arquitectura de la tesis, etc.) |
| `proyectos-md/` | dentro de cada proyecto | `CLAUDE.md`, planes y docs de amazon, ortodoncia, mundo-animal… Son solo los `.md`; el código está en GitHub |

### Capturas de los cursos (31 GB): NO van en el paquete
Los `apuntes.md` enlazan imágenes WebP relativas (`0001.webp`). Sin ellas la nota se ve, pero con imágenes rotas. Opciones:
1. **Copiar por red local** (recomendado, 31 GB, ~10 min en Wi-Fi 5): en la ThinkPad `rsync -avP yafer@<ip-pc>:"~/Vídeos/Capturas\ de\ YouTube/" ~/Vídeos/"Capturas de YouTube"/` (y lo mismo con `~/Documentos/Obsidian Vault/capturas`).
2. Copiar solo los cursos que vayas a repasar.
3. **Regenerarlas**: `SUPER+ALT+Y` con el link del curso (~10,5 min por hora de video, gasta cuota de Claude para los apuntes).
Con 500 GB en CachyOS, el espacio no es problema.

## 2. rclone: crear tu propio client_id de Google (hacerlo antes de que se retire)

**Qué pasa:** rclone trae un `client_id` compartido de Google Drive y avisa que **deja de funcionar durante 2026**. Hoy el remoto `gdrive` tiene `client_id` vacío = usa el compartido. Si no se cambia, `rclone-gdrive.service` (el Drive montado) y las subidas del paquete **dejarán de funcionar de golpe**.

**Aviso automático:** `~/.config/systemd/user/rclone-aviso-clientid.timer` lanza cada semana una notificación crítica mientras algún remoto `drive` siga sin `client_id` propio. Se apaga solo cuando lo configures. En la ThinkPad viene en `dotfiles/` (habilitar con `systemctl --user enable --now rclone-aviso-clientid.timer`).

**Pasos (los hace el usuario, ~10 min; no hay forma de automatizarlo porque exige iniciar sesión en Google):**
1. Entrar a https://console.cloud.google.com con la cuenta de Google del Drive → crear un proyecto nuevo (p. ej. `rclone-yafer`).
2. **APIs y servicios → Biblioteca →** buscar «Google Drive API» → **Habilitar**.
3. **Pantalla de consentimiento OAuth:** tipo **Externo**, nombre de la app `rclone`, correo propio. En «Usuarios de prueba» **añadir tu propio correo**. Luego pulsar **Publicar la app** (pasarla a «En producción»); si se queda en «Prueba», el token caduca a los 7 días.
4. **Credenciales → Crear credenciales → ID de cliente de OAuth →** tipo **Aplicación de escritorio**. Copiar el *Client ID* y el *Client secret*.
5. En la PC: `rclone config` → editar `gdrive` → pegar `client_id` y `client_secret` → cuando pregunte, **reautenticar** (abre el navegador) y aceptar. Probar con `rclone lsd gdrive:`.
6. Repetir `rclone config` en la ThinkPad con **el mismo** client_id/secret (puede reutilizarse en varios equipos).
7. Comprobar: `rclone-aviso-clientid` ya no debe mostrar nada. Reiniciar `systemctl --user restart rclone-gdrive`.

**Qué NO hay que copiar al paquete:** `~/.config/rclone/rclone.conf` (contiene token y secret). Guardar el client_id/secret en el gestor de contraseñas (KeePassXC).

## 3. Cómo evitar el desfase en adelante

Hoy el paquete es una **foto** que se regenera a mano (por eso estaba atrasado 10 días). Propuesta, de menos a más trabajo:

1. **Ya (mínimo):** al terminar una tanda de cambios, pedirle a Claude «actualiza el paquete de migración» (copia dotfiles, regenera listas de paquetes, edita README/docs y sube a Drive). El tar del 06-10 está hecho así.
2. **Recomendado: repo git de dotfiles privado** (`~/dotfiles`) con **GNU stow**, en tres capas:
   - `common/` → igual en todas las máquinas (hypr, kitty, fish, noctalia, mpv, VS Code, gwenview, scripts…).
   - `machine/pc-escritorio/` y `machine/thinkpad/` → lo propio de cada equipo (monitores, mouse Scimitar/keyd, escala, touchpad).
   - `system/etc/` y `packages/` (listas) + `bootstrap.sh` que detecta el hostname.
   - Los archivos vivos pasan a ser **symlinks al repo**: se edita en un sitio, `git commit`, y en la otra máquina `git pull && stow`. Se acaba el desfase y los conflictos se resuelven con git.
   - Secretos (`rclone.conf`, contraseña de restic, `gh`) **fuera** del repo.
3. Los **apuntes `.md`** pueden vivir en el mismo repo (son pocos MB) o sincronizarse con la bóveda de Obsidian vía Drive/rclone.

Ya existe un repo local en `~/.config/hypr` (commit del 06-10) que sería la base.

## 4. Checklist para la ThinkPad (lo nuevo del 06-10)

- [ ] Restaurar `apuntes/`, `guias-usuario/`, `claude-planes/`, `claude-memoria/`, `proyectos-md/` según la tabla de arriba.
- [ ] Instalar `fuse2 kimageformats qt6-imageformats` (Gwenview con webp/avif) y `pipx install edge-tts gallery-dl`.
- [ ] **No** instalar `keyd`, `ckb-next`, nvidia, ni copiar los `mouse-*.sh` (el bloque de binds `code:192–202` es inofensivo sin keyd).
- [ ] Lectura SUPER+R a ×1.4 (`voz.conf`); VS Code sin escritorio fijo; `terminal.integrated.fontSize` 13 (probar en 14").
- [ ] Habilitar `rclone-aviso-clientid.timer` y crear el client_id propio (§2).
- [ ] Clonar el repo de la tesis: `gh auth login && gh repo clone yftorrezg/Ciego ~/Proyectos/Ciego` (solo código; datasets y modelos `.tflite` no están en git).
- [ ] Servicios que se pueden deshabilitar para arrancar más rápido: `NetworkManager-wait-online`, `avahi-daemon` si no se usa.
- [ ] Elegir qué hacer con el trackpad/TrackPoint de la ThinkPad (gestos de 3 dedos: ver README).

## 5. Estado de la PC al 06-10 (referencia)
- Auditoría: **98/98 atajos OK**, sin scripts rotos, servicios clave activos.
- Limpieza: ~28 GB liberados (cachés uv/pip/npm/paru, worktrees de agentes). Disco 117 GB usados de 928 GB.
- Pendientes en la PC: `sudo paccache -rk1`, retirar huérfanos (`pacman -Qdtq`), decidir qué hacer con gimp/geeqie/alacritty/docker/firefox/libreoffice y con 25 GB de `Capturas de YouTube`.
