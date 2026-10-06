# dotfiles de yafer — PC 🖥️ + laptop 💻 a la par

Mi config de CachyOS + Hyprland (atajos, scripts de estudio, mpv, Obsidian, voz, noctalia...) en un solo lugar.
Lo que cambio en un equipo llega solo al otro, **sin pisar lo que es distinto** en cada uno.

> **¿Eres Claude?** Lee `CLAUDE.md` primero: tiene las reglas y el procedimiento completo.

## Cómo funciona (en simple)

- **Común** → atajos, scripts de cursos, mpv, Gwenview, Obsidian, memorias de Claude. Igual en los dos.
- **Por equipo** → monitores, NVIDIA, touchpad, escala, micrófono, batería. Cada equipo tiene su versión
  (carpeta `.hosts/pc/` y `.hosts/laptop/`); se elige sola por el nombre del equipo.
- **Nunca se sincroniza** → contraseñas, `/etc`, programas instalados, tus videos/datos.

El comando **`dotsync`** hace todo. Corre solo cada 30 min y al iniciar sesión:
1. guarda lo que cambiaste aquí,
2. baja lo que cambiaste en el otro equipo,
3. revisa que no tenga errores **antes** de aplicarlo (si tiene, no aplica nada y te avisa),
4. lo aplica y sube lo tuyo.

Si editaste **la misma línea** en los dos equipos, **no sobrescribe nada**: te sale una notificación
"CONFLICTO" → abre Claude y dile *"resuelve el conflicto de dotsync"*.

## Comandos

| Comando | Qué hace |
|---|---|
| `dotsync` | sincroniza ahora (subir + bajar) |
| `dotsync estado` | qué falta subir / bajar |
| `dotsync subir` / `dotsync bajar` | solo una dirección |
| `dotsync activar` / `desactivar` | automático on/off |
| `bash ~/.local/share/chezmoi/laptop/auditoria.sh` | chequeo completo de la laptop (✔/✘) |

**Regla de oro:** antes de cambiar mucho en un equipo, corre `dotsync` (para partir de lo último).
Y mantén los dos actualizados (`update` en fish) para que tengan la misma versión de Hyprland.

## ✅ Laptop (ThinkPad) — LISTA
Migrada el 05-10-2026. Sincronización automática activada.
Si reinstalas la laptop algún día:
```
sudo pacman -S chezmoi github-cli && gh auth login && gh auth setup-git
chezmoi init --apply https://github.com/yftorrezg/dotfiles.git
# luego los scripts de laptop/ (01 → 05) para paquetes y /etc, y laptop/auditoria.sh
```

## ⏳ PC — PENDIENTE (hacer una vez, en casa)
La PC tiene avances más nuevos que este repo, así que primero hay que **fusionar** (no copiar encima).

1. En la PC, en una terminal:
   ```
   sudo pacman -S --needed chezmoi github-cli lua
   gh auth login        # GitHub.com → HTTPS → Yes → Login with a web browser
   bash <(gh api repos/yftorrezg/dotfiles/contents/pc/fusion-inicial.sh -H 'Accept: application/vnd.github.raw')
   ```
   Esto **solo** respalda tu config, baja el repo y muestra diferencias. **No cambia nada.**
2. Abre Claude Code en la PC y dile lo que el script te muestra al final:
   > *«Lee ~/.local/share/chezmoi/CLAUDE.md y haz la fusión inicial de la PC»*
3. Claude junta tus avances de la PC con los arreglos de la laptop, prueba, y activa `dotsync`.
   En ≤30 min la laptop recibe tus avances.

## Atajos que cambiaron (para los dos equipos)
- **SUPER+ALT+B** → centro de estudio (`estudiar.py`). Antes era SUPER+ALT+Z, que **chocaba con el dictado**.
- **SUPER+ALT+Z / X** → dictado español / inglés.
- **SUPER+ALT+P** → pomodoro.

Solo laptop: **SUPER+`** (tecla bajo Esc) o 3 dedos ↑↓ = voltear a los escritorios 6-10 · tildes con **AltGr+vocal**,
ñ = AltGr+# luego n · F7 = pantallas (Arzopa).

## Pendientes
- [ ] Fusión inicial en la PC (arriba).
- [ ] Fondos de pantalla de Luffy → copiarlos a `~/Imágenes/Wallpapers` en la laptop.
- [ ] Laptop: `rclone config` (Drive) y contraseña de restic (backup) → ver `laptop/04-voz-servicios.sh drive|backup`.
- [ ] Laptop: `fprintd-enroll` (huella).
- [ ] ⚠️ PC: subir `~/Proyectos/Ciego` (tesis) a GitHub privado — hoy no tiene copia remota.
