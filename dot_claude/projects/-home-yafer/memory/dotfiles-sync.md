---
name: dotfiles-sync
description: PC y laptop se sincronizan con chezmoi + repo privado yftorrezg/dotfiles + comando dotsync; leer CLAUDE.md del repo antes de tocar config
metadata:
  type: project
---
Desde el 06-10-2026 la config de `$HOME` de la PC (`yf`, equipo `pc`) y la laptop ThinkPad (`yafer`, equipo `laptop`) vive en `~/.local/share/chezmoi` (GitHub privado `yftorrezg/dotfiles`). Archivos que dependen del hardware: `.hosts/<equipo>/` + `.hosts-lista`; atajos comunes en `binds.lua`, los de monitores en `binds_equipo.lua`. `dotsync` (timer 30 min) captura, valida y aplica; ante conflicto no pisa nada y notifica.

**Why:** el usuario usa la PC en casa y la laptop en la facultad y quiere ambas a la par sin romper lo propio de cada una.
**How to apply:** antes de editar config, lee `~/.local/share/chezmoi/CLAUDE.md`; tras editar en `$HOME`, `dotsync subir` (o `chezmoi add` si es archivo nuevo). En la PC, NO aplicar hasta hacer la "fusión inicial" descrita ahí. Ver [[migracion-laptops]].
