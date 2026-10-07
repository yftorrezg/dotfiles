# windows/ — SOLO el Windows 11 de la laptop ThinkPad E14 Gen4

> ⚠️ Esta carpeta es **únicamente para el Windows 11 de la laptop ThinkPad E14 Gen4** (la de la facultad,
> i7-1255U, Iris Xe, 16 GB, disco 0; CachyOS está en el disco 1).
> **No es para la PC de escritorio ni para el CachyOS de la laptop**: chezmoi la ignora (`.chezmoiignore`),
> así que nunca se aplica en Linux.

## Qué hay
| Carpeta / archivo | Para qué |
|---|---|
| `ahk/yafer.ahk` | Los mismos atajos de `binds.lua` (SUPER = Win), con AutoHotkey v2 + escritorios nativos |
| `ATAJOS-WINDOWS.md` | Cheat sheet + qué atajos de Windows se reemplazaron y cómo llegar a ellos |
| `scripts/` | Win+R (leer en voz alta con edge-tts, usa el `limpiar-texto.py` común) y guardar capturas |
| `pwsh/`, `terminal/` | PowerShell 7 + Windows Terminal (como fish/kitty) |
| `mpv/` | Config de mpv de CachyOS adaptada a Windows (unión `%APPDATA%\mpv` → aquí) |
| `imageglass/` | Atajos de Gwenview para ImageGlass (se cargan a mano) |
| `winget/thinkpad.dsc.yaml` | Todos los programas |
| `bootstrap-admin.ps1` → `bootstrap.ps1` | Reinstalar todo (primero el de admin, después el normal) |

## Reinstalar desde cero
```powershell
gh repo clone yftorrezg/dotfiles $HOME\dotfiles
Start-Process pwsh -Verb RunAs -ArgumentList '-File', "$HOME\dotfiles\windows\bootstrap-admin.ps1"
pwsh -File $HOME\dotfiles\windows\bootstrap.ps1
```
Después, los pasos manuales de `ATAJOS-WINDOWS.md` (sección "Después del bootstrap").
