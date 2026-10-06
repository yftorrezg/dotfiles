---
name: windows-thinkpad-setup
description: W11 de la ThinkPad E14 G4 armado con AHK + PowerToys + WT/pwsh; carpeta windows/ del repo dotfiles (06-10-2026)
metadata:
  type: project
---

El 06/10/2026 se armó el Windows 11 de la ThinkPad (disco 0; CachyOS está en el disco 1) para la facultad. Decisiones del usuario: Windows **ligero**, y lo pesado (doblar, cuadernillos y auto-captura de cursos) sigue en CachyOS. Terminal: Windows Terminal + pwsh 7. Ventanas: escritorios nativos + AutoHotkey v2 (VD.ah2), sin gestor de mosaico. Periféricos: Stream Deck XL, Mirabox/Fifine, MX Master 4, K380, Maono.

Todo está en `windows/` del repo chezmoi `yftorrezg/dotfiles` (clonado en `C:\Users\Ferto\dotfiles`; `windows/` está en `.chezmoiignore`): `ahk/yafer.ahk` (los mismos atajos de binds.lua), `scripts/` (leer en voz alta con edge-tts usando el limpiar-texto.py de CachyOS; guardar capturas), `pwsh/profile.ps1`, `terminal/wt-ajustes.json`, `mpv/` (config de CachyOS adaptada a Windows), `winget/thinkpad.dsc.yaml`, `bootstrap.ps1` / `bootstrap-admin.ps1` y `ATAJOS-WINDOWS.md`.

**Why:** que tenga la misma memoria muscular en los dos sistemas, sin choques con los atajos de Office.
**How to apply:** las teclas las maneja un solo dueño, `yafer.ahk`; el Stream Deck, Options+ y el Mirabox mandan esos atajos y no llevan lógica propia. Para un cambio de atajos se edita yafer.ahk y el cheat sheet. Ctrl+Shift+S y Ctrl+Shift+D están excluidos en Office y ER/Studio. Ver [[hyprland-escritorios-atajos]] y [[migracion-laptops]].
