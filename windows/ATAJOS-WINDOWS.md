---
tags: [sistema, windows, atajos]
actualizado: 2026-10-06
---
# Atajos en Windows 11 (ThinkPad E14 Gen4)

Win = SUPER. Son **los mismos atajos que en Hyprland** (`binds.lua`). El dueño de las teclas es `ahk/yafer.ahk`: el Stream Deck, el MX Master 4 y el Mirabox mandan estos mismos atajos, sin lógica propia.
Recargar el script: **Win+Alt+F5**.

## Ventanas y escritorios
| Atajo | Acción |
|---|---|
| Win+Q | Cerrar ventana |
| Win+D | Maximizar / restaurar |
| Win+F | Pantalla completa (F11) |
| Win+Alt+Espacio | Siempre encima (PiP) |
| Win+1..5 | Escritorio 1 Redes · 2 Facultad · 3 Estudio · 4 Código · 5 Chats |
| Win+Ctrl+1..5 | Mover la ventana al escritorio N |
| Win+Ctrl+←/→ · Win+rueda | Escritorio anterior / siguiente |
| Win+Alt+E | Ir a Estudio (3) |
| Win+Tab | Vista de tareas (nativo) |
| Win+←/→/↑ | Acoplar (nativo). **Win+Z**: diseños de acoplamiento |
| Gestos | 4 dedos ←/→ = escritorio · 3 dedos ↑ = Vista de tareas |

## Apps
| Atajo | Abre o enfoca |
|---|---|
| Win+Enter | Windows Terminal (pwsh 7) |
| Win+S | Terminal desplegable (quake) |
| Win+Espacio | Lanzador: PowerToys Command Palette (sustituye a Win+R "Ejecutar") |
| Win+E / W / N / G | Explorador / Brave / Obsidian / VS Code (escr. 4) |
| Win+K | App del Stream Deck |
| Win+T | TikTok (1) |
| Win+Alt+Q / W / T / F / I / D | YouTube / WhatsApp (5) / Telegram (5) / Facebook (1) / Instagram (1) / Drive |
| Win+Ctrl+Alt+G / C / N / D | Gemini / Claude / NotebookLM / DeepSeek (pensados para el Stream Deck) |

## Estudio
| Atajo | Acción |
|---|---|
| Win+R | Leer la selección en voz alta (otra vez = cortar) |
| Win+Alt+R | Elegir voz y velocidad |
| Win+Alt+Z / X | Dictado (Handy): español / inglés · **Win+H** dictado de Windows |
| Ctrl+Shift+S | Captura de región → carpeta de estudio + portapapeles (*no actúa en Word, Excel, PowerPoint ni ER/Studio*) |
| Ctrl+Shift+D | Elegir la carpeta de capturas |
| Win+Shift+S | Recorte → solo portapapeles (nativo) |
| Impr | Herramienta Recortes (nativo) |
| Win+Shift+T | OCR: copiar el texto de la pantalla (PowerToys Text Extractor) |
| Win+C / Win+Alt+C | Abrir el curso (escritorio 3) / configurar sus 4 slots |
| Win+V · Win+. · Win+L | Portapapeles · emojis · bloquear (nativos) |

## Atajos de Windows que se reemplazaron (decidido el 06-10-2026: gana Hyprland)
| Atajo | En Windows era | Cómo llegar a lo de Windows |
|---|---|---|
| Win+R | Ejecutar | **Win+X → R**, o escribir el comando en Win+Espacio |
| Win+Q / Win+S | Búsqueda | Win+Espacio, o apretar Win y escribir |
| Win+Espacio | Cambiar idioma del teclado | **Alt+Shift** |
| Win+D | Mostrar escritorio | **Win+M** (minimizar todo) · **Win+,** (vistazo mientras se mantiene) |
| Win+N | Notificaciones y calendario | Clic en el reloj |
| Win+W | Widgets | — (desactivar Widgets) |
| Win+G | Game Bar | — (desactivada) |
| Win+C | Copilot | Ícono de Copilot |
| Win+K | Transmitir pantalla | Win+A → Transmitir |
| Win+T | Recorrer la barra de tareas | Tab desde la barra |
| Win+F | Centro de opiniones | — |
| Win+1..5 · Win+Ctrl+1..5 | Apps ancladas en la barra | Clic en la barra de tareas |
| Win+Alt+D | Panel de fecha y hora | Clic en el reloj |
| Win+Shift+T | Recorrer la barra hacia atrás | — (lo usa PowerToys OCR) |

Dentro de las apps: Ctrl+Shift+S / Ctrl+Shift+D están excluidos solo en Word, Excel, PowerPoint y ER/Studio. En **VS Code** se pierde *Guardar como* (Ctrl+Shift+S) y en **Brave** *Guardar pestañas en marcadores* (Ctrl+Shift+D). Para excluir otra app: agregar un `GroupAdd "Facultad", "ahk_exe <app>.exe"` en `yafer.ahk` y Win+Alt+F5.

## Lo que queda solo en CachyOS (el otro SSD)
`doblar`, auto-captura (Win+Alt+S), cuadernillos de cursos (Win+Alt+Y/A) y las capturas grandes. En Windows sí están `descargar` (en pwsh), SUPER+R, el dictado y las capturas.

## Después del bootstrap (pasos manuales)
1. **PowerToys**: activar Command Palette (Win+Alt+Espacio, que yafer.ahk lanza con Win+Espacio), Text Extractor, FancyZones (diseños 50/50 y 70/30), Workspaces "Facultad" y "Estudio", Advanced Paste.
2. **Handy**: modelo Parakeet V3 (CPU), micrófono Maono, atajos Win+Alt+Z (es) y Win+Alt+X (en) si la app lo permite.
3. **Apps predeterminadas** (Configuración → Aplicaciones): video → mpv, imágenes → ImageGlass, `.md` → Obsidian.
4. **Lenovo Vantage**: Modo de conservación de batería (80 %), actualizaciones del sistema.
5. **Logi Options+ (MX Master 4)**: pulgar = Ctrl+Shift+S, gestos = Win+Ctrl+←/→, Actions Ring = Win+R, Win+Alt+Z, Win+Shift+T y apps web.
6. **Stream Deck XL**: perfiles Facultad / Estudio / Sistema usando la acción "Tecla de acceso rápido" con los atajos de arriba.
7. **Configuración → Personalización → Barra de tareas**: desactivar Widgets. Copilot: desinstalar si no se usa.
8. **Win+Espacio** cambiaba el idioma del teclado: si usas dos distribuciones, queda **Alt+Shift**.
