# ⌨️ Atajos · Mapa general y mnemotecnias

> Todos los atajos de tu PC en un solo lugar: cómo están pensados, los que más usas y dónde está cada grupo.

## 🧭 Resumen en 30 segundos

Las teclas tienen **lógica**. Si entiendes la regla, adivinas la mayoría sin memorizar:

| Combinación | Dónde se usa | Ejemplo |
|---|---|---|
| `SUPER` solo | Sistema: ventanas, buscador, bloquear | `SUPER + Q` cierra la ventana |
| `SUPER + letra` | Abrir apps (la letra suele ser la inicial) | `SUPER + N` = Notas (Obsidian) |
| `SUPER + ALT + letra` | Apps web y **estudio** | `SUPER + ALT + A` = Apuntes del curso |
| `SUPER + SHIFT + letra` | Acción sobre la ventana o la **selección** | `SUPER + SHIFT + S` = captura al portapapeles |
| `SUPER + CTRL + número` | Escritorios | `SUPER + CTRL + 3` = mandar ventana al 3 |
| `Ctrl + Shift + letra` | Dentro de cada programa (kitty, Dolphin…) | `Ctrl + Shift + C` copia en kitty |

🧠 Concepto: **SUPER** es la tecla del sistema; cada programa tiene su propio mundo de atajos (`Ctrl+...`) que solo funciona con esa ventana enfocada. Por eso `Ctrl+W` cierra una pestaña en el navegador y no cierra toda la ventana.

💡 Consejo: si no recuerdas un atajo, piensa en la **inicial** de lo que hace. Casi todos la usan: `N` Notas, `D` Descargas, `C` Curso, `S` Captura, `R` Leer, `T` Traducir, `G` Código, `A` Avisos.

## 🔟 Los 15 que más usas

| Atajo | Qué hace | Hoja |
|---|---|---|
| `SUPER + Return` | Terminal | 26 |
| `SUPER + Q` | Cerrar ventana | 26 |
| `SUPER + F` | Pantalla completa | 26 |
| `SUPER + flechas` | Enfocar ventana | 26 |
| `SUPER + 1…0` | Cambiar de escritorio | 26 |
| `SUPER + SHIFT + S` | Captura al portapapeles | 27 |
| `SUPER + I` | Centro de estudio (próxima clase) | 27 |
| `SUPER + ALT + A` | Apuntes de todo un curso | 27 |
| `SUPER + R` | Leer en voz alta la selección | 27 |
| `SUPER + SHIFT + T` | Traducir la selección | 27 |
| `SUPER + D` | Descargar lo que copiaste | 27 |
| `SUPER + N` | Obsidian (notas) | 26 |
| `SUPER + V` | Portapapeles (historial) | 26 |
| `SUPER + ALT + N` | Modo enfoque (todo negro) | 26 |
| `SUPER + SHIFT + C` | Estas chuletas | 26 |

## 🗺️ Dónde está cada grupo

| Hoja | Qué contiene | Fuente |
|---|---|---|
| 26 · Hyprland | Ventanas, escritorios, apps, sistema, mouse | `config/binds.lua` (automática) |
| 27 · Estudio | Cursos, capturas, voz, traducción, descargas | `binds.lua` (automática) |
| 28 · kitty | Terminal: paneles, pestañas, zoom | `kitty.conf` |
| 29 · Dolphin | Explorador de archivos | Atajos del programa |
| 30 · Obsidian | Notas y repaso | Atajos del programa + plugins |
| 31 · mpv | Videos: saltos, velocidad, notas | `input.conf` |
| 32 · Gwenview | Fotos | `gwenviewui.rc` |
| 33 · Mouse y Stream Deck | MX Master 4, Scimitar, teclas del deck | `binds_equipo.lua`, `keyd-scimitar.conf` |
| 22 · Claude Code | Atajos de la terminal con Claude | Hoja del agente |
| 24 · OpenCode | Atajos con tecla líder | Hoja del agente |
| 20 · MX Master 4 | Gestos del mouse en detalle | `mx-doc.py` |

## 🧩 Errores típicos

- ⚠️ **Cuidado:** `Ctrl + W` cierra pestaña en el navegador y en kitty, pero **no** es `SUPER + Q`. Son mundos distintos.
- ⚠️ **Cuidado:** `SUPER + S` muestra el escritorio especial; la captura es `SUPER + SHIFT + S`. Solo cambia el SHIFT.
- ⚠️ **Cuidado:** en mpv **no** se usa SUPER. Sus teclas solo funcionan con la ventana de mpv enfocada.
- ❌ Mal: cambiar un atajo en un programa y olvidarlo. ✅ Bien: cambia el bind y regenera la hoja (las hojas 26 y 27 se actualizan solas con `atajos-doc.py`).

## 🧠 Practica

::: desplegable 🧩 ¿Qué hace SUPER + ALT + O?
Abre el **anillo radial**: mantienes la combinación, eliges un sector con el mouse y al soltar ejecuta la acción. Es el mismo gesto del panel háptico del MX Master 4.
:::

::: desplegable 🧩 ¿Qué hace SUPER + CTRL + 3?
Manda la ventana enfocada al **escritorio 3** de su mismo monitor. Sin CTRL (`SUPER + 3`) cambias de escritorio en todos los monitores.
:::

::: desplegable 🧩 ¿Por qué SUPER + C abre el curso y SUPER + ALT + C lo configura?
La inicial de **C**urso. Con ALT, la acción es de **configuración** (cambiar links), no de uso diario.
:::
