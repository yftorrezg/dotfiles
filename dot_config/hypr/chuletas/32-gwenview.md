# 🖼️ Gwenview · Fotos y visor

> El visor de imágenes de KDE con tus atajos propios. Las teclas de la tabla salen de `gwenviewui.rc` (tu configuración).

## 🧭 Resumen en 30 segundos

En Gwenview **las letras son el control**: `A` y `D` pasan de foto, `Q` y `E` giran, `X` manda a la papelera, `F` pone pantalla completa.

| Quiero… | Tecla |
|---|---|
| Foto siguiente / anterior | `D` / `A` (también `Space` / `Backspace`) |
| Girar izquierda / derecha | `Q` / `E` |
| Recortar | `C` |
| Redimensionar | `R` |
| Mandar a la papelera | `X` (también `Supr`) |
| Pantalla completa | `F` (también `F11`) |
| Ajustar la foto a la ventana | `W` |
| Llenar la ventana | `Shift+W` |
| Miniaturas | `T` (también `Ctrl+B`) |
| Barra lateral | `I` (también `F4`) |
| Modo foco (sin barras) | `S` |

🧠 Concepto: las teclas de **una mano** (`A S D W Q E`) te dejan usar el visor sin soltar el teclado. Es el mismo criterio que usas con `SUPER + ...`.

## 📋 Más atajos de Gwenview

| Atajo | Qué hace |
|---|---|
| `Ctrl+S` | Guardar |
| `M` | Reflejar (espejo) |
| `Ctrl+Alt+N` | Abrir en ventana nueva |
| `Ctrl+Alt+O` | Abrir la carpeta que contiene la foto |
| `F7` | Copiar a… |
| `Ctrl+Alt+M` | Mover a… |
| `Shift+Supr` | Borrar sin papelera (no hay vuelta atrás) |

## ⚠️ Errores típicos

- ⚠️ **Cuidado:** `X` y `Supr` mandan a la **papelera**; `Shift+Supr` la **salta**. Confirma antes de usar `Shift+Supr`.
- ⚠️ **Cuidado:** `Ctrl+L` y `Ctrl+R` son para **girar**, no para recargar la carpeta.
- ✅ Bien: si cambias la versión de Gwenview y se rompe la tabla, revisa `~/.local/share/kxmlgui5/gwenview/gwenviewui.rc` (la versión del archivo es 71).

## 🧠 Practica

::: desplegable 🧩 ¿Qué tecla quito de la papelera si borré una foto por error?
Gwenview manda a la papelera con `X`: la foto sigue ahí. Ábrela desde la papelera del sistema (Dolphin → Papelera). Con `Shift+Supr` no se puede.
:::

::: desplegable 🧩 Quiero solo ver la foto, sin ruido. ¿Qué pulso?
`S` (modo foco): oculta las barras y deja la imagen. Otra vez para volver.
:::
