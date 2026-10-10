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

Actualización 06/10/2026: mouse Corsair Scimitar vía keyd (`/etc/keyd/default.conf` → F14–F24 = `code:192`–`202` en binds.lua; modos M1 Estudio/M2 Programación/M3 Redes en `scripts/mouse-accion.sh`; solo PC, guía `~/Documentos/atajos-y-mouse.md`). VS Code ya NO se fija al escritorio 4 (quitado 01/10). SUPER+R a ×1.4. Auditoría: 98/98 binds OK.

Actualización 09/10/2026 (pedido del usuario): solo las REDES tienen escritorio fijo (FB/IG/TikTok → ws1, WhatsApp/Telegram → ws6 = escritorio 1). Drive (antes ws8) y VS Code (antes ws4 en app-web.sh) ahora son libres como YouTube: se abren en el escritorio donde estés; SUPER+C (`curso-abrir.sh`) ya no salta al workspace `estudio`. Además: el Stream Deck XL aparece como teclado (KEY_UNKNOWN) y disparaba a la vez todos los binds F14–F24 del mouse; arreglado con `hl.device({ name = "elgato-stream-deck-xl", keybinds = false })` en `config/inputs.lua`.
