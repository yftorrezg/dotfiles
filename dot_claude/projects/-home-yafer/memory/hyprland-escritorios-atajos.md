---
name: hyprland-escritorios-atajos
description: "Organización de escritorios virtuales, atajos de apps web y script de restauración de ventanas en Hyprland (Lua config)"
metadata:
  node_type: memory
  type: project
  originSessionId: 9c5f82ef-8af9-4b4a-b593-a81dd9949055
  modified: 2026-09-26T02:18:52.126Z
---

Hyprland con config en Lua (`~/.config/hypr/config/*.lua`); `hyprctl dispatch` exige sintaxis Lua, ej. `hl.dsp.window.move({ workspace = "3", window = "address:0x..", follow = false })`.
2 monitores: DP-3 principal (ws 1-5) y HDMI-A-1 vertical (ws 6-10); SUPER+N = escritorio virtual N (ws N + ws N+5).

Organización acordada (25/09/2026): 1 redes (FB/IG/TikTok principal, WhatsApp/Telegram vertical, fijo), 2 entretenimiento, 3 estudio (curso + Drive apuntes en vertical ws8), 4 práctica (VS Code ws4), 5 Claude/terminal.
Atajos: SUPER+ALT+Q YouTube (libre, escritorio actual), +W WhatsApp, +T Telegram, +F Facebook, +I Instagram, +D Drive; SUPER+T TikTok; SUPER+G VS Code. Script `scripts/app-web.sh` (ventanas `brave --app`, clase `brave-<dominio>__-Default`), reglas en `windowrules.lua`.
`scripts/sesion-ventanas.py` (autostart) guarda/restaura el workspace de ventanas de Brave al iniciar y al reabrir a mitad de sesión.

**Why:** el usuario prefiere atajos de mano izquierda (teclado K380) y revisar propuestas antes de implementar cambios grandes.
**How to apply:** al agregar atajos, verificar conflictos en `binds.lua` y proponer primero; reusar app-web.sh para nuevas apps web.

Dictado (hyprwhspr, `~/.config/hyprwhspr/config.json`): desde el 26/09 SUPER+ALT+Z español y SUPER+ALT+X inglés (antes D/I, que chocaban con Drive/Instagram de binds.lua; hyprwhspr no roba la tecla, así que se disparaban ambos). CTRL+SHIFT+D se queda: el usuario no usa ese atajo en VS Code/Brave.
