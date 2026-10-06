# Atajos y mouse Corsair Scimitar RGB Elite

Actualizado: 05/10/2026. Teclado: `~/.config/hypr/config/binds.lua`.
Mouse: `/etc/keyd/default.conf` (copia en `~/.config/hypr/keyd-scimitar.conf`) + `scripts/mouse-accion.sh`.

## 1. Mouse: cómo funciona

La memoria del mouse (de Windows) manda atajos; **keyd** los convierte en F14..F24 solo para este mouse y
Hyprland les da la acción. Botones físicos en cuadrícula: 1 2 3 / 4 5 6 / 7 8 9 / 10 11 12.

### Siempre iguales (los 3 modos)
| Botón | Acción |
|---|---|
| 1 / 4 | Adelante / Atrás |
| 2 | Escritorio 2 |
| 3 | Escritorio 3 |
| 5 | Escritorio 4 |
| 6 | Escritorio 5 |
| 10 / 11 / 12 | Cambiar a modo M1 / M2 / M3 |
| Rueda (clic) | Captura (Impr Pant) |
| Botón de velocidad | DPI (nativo del mouse) |
| Botón del medio (arriba) | Memoria física 1/2 del mouse |

### Cambian según el modo (solo 7, 8, 9)
| Botón | M1 Estudio | M2 Programación | M3 Redes |
|---|---|---|---|
| 7 | Leer (SUPER+R) | CTRL+S guardar | YouTube |
| 8 | Captura guardada (CTRL+SHIFT+S) | CTRL+P abrir archivo | Telegram |
| 9 | Modo estudiar (SUPER+I) | CTRL+` terminal | Instagram |

Cambiar acciones: editar `scripts/mouse-accion.sh` (líneas `M:botón`).

## 2. Teclado: lo esencial, por prioridad

**A. Imprescindibles (diario)**
| Atajo | Acción |
|---|---|
| SUPER+1..5 | Escritorio 1..5 |
| SUPER+Q | Cerrar ventana |
| CTRL+W | Cerrar pestaña |
| SUPER+R | Leer selección en voz alta |
| SUPER+SHIFT+S | Captura al portapapeles |
| CTRL+SHIFT+S | Captura guardada |
| CTRL+SHIFT+D | Carpeta de capturas |
| SUPER+V | Historial del portapapeles |

**B. Estudio**
| Atajo | Acción |
|---|---|
| SUPER+C / SUPER+ALT+C | Abrir / configurar curso |
| SUPER+I / SUPER+ALT+V | Modo estudiar / tests |
| SUPER+ALT+S | Auto-captura on/off |
| SUPER+ALT+Y / A | Capturas de YouTube / elegir apuntes |
| SUPER+ALT+Z / X | Dictado español / inglés |

**C. Ventanas**
| Atajo | Acción |
|---|---|
| SUPER+F / SUPER+D | Pantalla completa / maximizar |
| SUPER+Tab, ALT+Tab | Ciclar ventanas |
| SUPER+flechas | Mover foco |
| SUPER+CTRL+1..5 | Mover ventana a escritorio |
| SUPER+S | Escritorio especial (scratchpad) |

**D. Apps**
| Atajo | App |
|---|---|
| SUPER+Return / E / W / N / G | Terminal / Archivos / Navegador / Obsidian / VS Code |
| SUPER+ALT+Q/W/T/F/I/D | YouTube / WhatsApp / Telegram / Facebook / Instagram / Drive |
| SUPER+T | TikTok |

## 3. Atajos de apps para estudiar

**Navegador:** CTRL+F buscar · CTRL+L URL · CTRL+SHIFT+T reabrir pestaña · CTRL+Tab cambiar pestaña ·
CTRL+1..8 ir a pestaña · CTRL+D marcador · CTRL+rueda zoom · F11 pantalla completa.

**VS Code:** CTRL+P abrir archivo · CTRL+SHIFT+P comandos · CTRL+B panel · CTRL+` terminal · CTRL+/ comentar ·
ALT+↑/↓ mover línea · CTRL+D siguiente coincidencia · CTRL+SHIFT+F buscar en proyecto · F2 renombrar.

**Edición:** CTRL+Z/Y · CTRL+←/→ saltar palabra · CTRL+Backspace borrar palabra · CTRL+Home/End.

## 4. Notas técnicas
- Hyprland no resuelve los nombres F13–F24 con layout `us`: se bindea por keycode (F14=192 … F24=202).
- keyd no admite comentarios en la misma línea que una regla.
- ckb-next no entiende los botones laterales de este modelo: está desactivado (`ckb-next-daemon`).
