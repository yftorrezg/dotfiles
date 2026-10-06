---
name: migracion-laptops
description: Migración de la config de la PC (CachyOS+Hyprland) a laptops; ThinkPad E14 G4 ya migrada el 05-10-2026, estado y pendientes
metadata:
  type: project
---
El 26/09/2026 se armó `~/migracion-cachyos/` (README + docs 01-05 + dotfiles + system/etc + paquetes + claude-memoria) y se subió a Drive `LaptopPcOptimizaciones/migracion-cachyos-hyprland/` (docs sueltos + `migracion-cachyos-2026-09-26.tar.zst`, el tar conserva symlinks). Destinos: Surface Pro 6 (i7-8ª, táctil, escala 2) y ThinkPad E14 G4 (i7-12ª); ambas Intel, sin NVIDIA; normalmente solo eDP-1 y a veces monitor portátil Arzopa.

**Why:** esta PC es el laboratorio del usuario; lo que se cambie aquí se replica luego en las laptops.
**How to apply:** si cambias config de esta PC, actualiza también el paquete/docs y vuelve a subirlo. Pendiente de decidir por el usuario: choque SUPER+ALT+D / SUPER+ALT+I (dictado hyprwhspr vs Drive/Instagram), kb_layout, apps dudosas, linux-surface. Ver [[hyprland-escritorios-atajos]].

Actualización 26/09 tarde: auditoría completa → docs 06 (descargar/doblar/auto-captura), 07 (uso y cronología), GAPS, LIMPIEZA, `guias-usuario/`, `INICIO.md` + `.obsidian/` (la carpeta es también bóveda de Obsidian). Paquete actual en Drive: `migracion-cachyos-2026-09-26-v3.tar.zst` (se reemplaza con cada actualización). Al actualizar: editar nota del tema, regenerar tar (probar extracción con diff) y subir con rclone usando filtros `--include "/docs/**"` con barra inicial (sin barra agarra carpetas anidadas). El usuario NO quiso borrar el doc de claude.ai del resumen. Riesgo urgente: `~/Proyectos/Ciego` (tesis) sin remoto git.

**ThinkPad E14 G4 migrada el 05/10/2026** (hostname `yafer`, la PC es `yf`). Trabajo en `~/migracion-laptop/`: `staging/` (git con un commit por área = diff exacto PC→laptop), scripts 01-05 ya ejecutados, `auditoria.sh` (re-ejecutable, sin sudo), respaldo de la config previa en `respaldo-laptop-*/`. Decisiones del usuario: escala interna **1** (probó 1.25 y no le gustó), teclado físico UK → `gb` + variante `extd` (AltGr+vocal = tilde), batería tope 80%, extras gimp/kdenlive/meld/opencode/docker/opendeck, sin firefox/alacritty. Cambios clave: piper vía pipx + voces en `~/.local/share/piper-voices` (AUR piper-tts no compila), thermald quitado (ThinkPad usa DYTC), `/etc/pam.d/noctalia` creado (sin él el lockscreen deniega), estudiar.py movido a SUPER+ALT+B (chocaba con dictado SUPER+ALT+Z), pomodoro SUPER+ALT+P, monitores dinámicos en `hypr/config/escritorios.lua` (SUPER+` voltea a ws N+5 sin Arzopa). Pendiente: sync PC↔laptop con chezmoi (plantillas por hostname), fondos de pantalla, rclone config, pass de restic.
