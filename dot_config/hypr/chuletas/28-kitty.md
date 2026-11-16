# 🐱 kitty · Terminal: paneles, pestañas y zoom

> La terminal donde viven Claude Code y OpenCode. Tus atajos propios (`kitty.conf`) y los de fábrica verificados contra la documentación de kitty 0.50.

## 🧭 Resumen en 30 segundos

kitty usa **Ctrl+Shift** como tecla base (`kitty_mod`). Por eso `Ctrl+Shift+C` copia y `Ctrl+Shift+V` pega (no `Ctrl+C`, que en la terminal es «interrumpir»).

| Quiero… | Atajo |
|---|---|
| Copiar / pegar | `Ctrl+Shift+C` / `Ctrl+Shift+V` |
| Panel dividido a la derecha | `Ctrl+Shift+\` |
| Panel dividido abajo | `Ctrl+Shift+-` |
| Moverme entre paneles | `Ctrl+Alt+` flechas |
| Hacer grande el panel actual (pila) | `Ctrl+Shift+Z` |
| Pestaña nueva / cerrar pestaña | `Ctrl+Shift+T` / `Ctrl+Shift+Q` |
| Cambiar de pestaña | `Ctrl+Shift+→` / `Ctrl+Shift+←` |
| Buscar en lo que ya salió | `Ctrl+Shift+H` (historial) |
| Abrir un enlace de la pantalla | `Ctrl+Shift+E` |

🧠 Concepto: un **panel** (split) es una división dentro de una misma pestaña. Una **pestaña** es otra terminal entera. Un **layout** es la forma en que se acomodan los paneles; `Ctrl+Shift+L` cambia el layout.

## 🪟 Paneles (los tuyos)

Tu `kitty.conf` activa dos layouts: `splits` (paneles) y `stack` (uno grande a la vez).

| Atajo | Qué hace | Notas |
|---|---|---|
| `Ctrl+Shift+\` | Abrir panel a la derecha (vertical) | Mismo directorio de la terminal actual |
| `Ctrl+Shift+-` | Abrir panel abajo (horizontal) | Igual, en el mismo directorio |
| `Ctrl+Alt+←↑→↓` | Ir al panel vecino | Tu configuración |
| `Ctrl+Shift+Z` | Mostrar solo el panel actual (stack) | Otra vez = volver a los paneles |

⚠️ Cuidado: `Ctrl+Shift+-` es el **guion**, no el signo menos del teclado numérico. Si no responde, prueba la tecla de guion normal.

## 🔤 Tamaño de letra (los tuyos)

| Atajo | Qué hace |
|---|---|
| `Ctrl+Alt+=` | Letra más grande (+0.5) |
| `Ctrl+Alt+-` | Letra más chica (−0.5) |
| `Ctrl+Alt+Backspace` | Volver al tamaño normal |

💡 Consejo: el tamaño se aplica a **todas** las ventanas de kitty a la vez (`change_font_size all`).

## 📑 Pestañas y ventanas (de fábrica)

| Atajo | Qué hace |
|---|---|
| `Ctrl+Shift+T` | Pestaña nueva |
| `Ctrl+Shift+Q` | Cerrar pestaña |
| `Ctrl+Shift+W` | Cerrar ventana (panel) |
| `Ctrl+Shift+→` / `←` | Pestaña siguiente / anterior |
| `Ctrl+Shift+.` / `,` | Mover pestaña adelante / atrás |
| `Ctrl+Shift+L` | Cambiar layout |
| `Ctrl+Shift+F` | Mover ventana adelante |
| `Ctrl+Shift+R` | Redimensionar ventana (modo resize, tecla de flechas) |

## 📜 Historial y búsqueda (de fábrica)

| Atajo | Qué hace |
|---|---|
| `Ctrl+Shift+↑` / `↓` | Subir / bajar una línea |
| `Ctrl+Shift+PgUp` / `PgDn` | Subir / bajar una página |
| `Ctrl+Shift+Inicio` / `Fin` | Ir al inicio / al final |
| `Ctrl+Shift+/` | Buscar en el historial |
| `Ctrl+Shift+H` | Mostrar el historial completo en otra ventana |
| `Ctrl+Shift+Supr` | Limpiar la terminal |

## 🛠️ Utilidades (de fábrica)

| Atajo | Qué hace |
|---|---|
| `Ctrl+Shift+E` | Abrir enlaces de la pantalla (hints) |
| `Ctrl+Shift+U` | Escribir un carácter por su código Unicode |
| `Ctrl+Shift+F5` | Recargar `kitty.conf` (después de editarlo) |
| `Ctrl+Shift+F2` | Abrir `kitty.conf` para editarlo |
| `Ctrl+Shift+F3` | Paleta de comandos de kitty |
| `Ctrl+Shift+F6` | Ver la configuración que se está usando |
| `F11` | Pantalla completa |
| `Ctrl+Shift+Esc` | Consola de kitty (`kitty_shell`) |

🧠 Concepto: `Ctrl+Shift+F5` es la forma rápida de probar cambios: editas `kitty.conf`, recargas y ves el efecto sin cerrar la terminal.

## ⚠️ Errores típicos

- ⚠️ **Cuidado:** `Ctrl+C` **interrumpe** el programa que corre; para copiar usa `Ctrl+Shift+C`.
- ⚠️ **Cuidado:** `Ctrl+Shift+Q` cierra la pestaña **sin preguntar** si hay procesos corriendo.
- ❌ Mal: usar `Ctrl+W` pensando que cierra el panel. En kitty es `Ctrl+Shift+W`.
- ✅ Bien: si tu atajo no hace nada, mira si otra app se lo quedó (Noctalia o Hyprland) con `SUPER + SHIFT + C`, hoja 26.

## 🧠 Practica

::: desplegable 🧩 Quiero ver el servidor en un panel y Claude Code en otro. ¿Qué pulso?
`Ctrl+Shift+\` abre el panel a la derecha con el mismo directorio. Luego `Ctrl+Alt+←` o `→` para moverte entre los dos.
:::

::: desplegable 🧩 ¿Cómo hago el panel actual pantalla completa dentro de kitty?
`Ctrl+Shift+Z` (layout stack). Otra vez para volver a los paneles. `F11` pone toda la ventana de kitty en pantalla completa, que es otra cosa.
:::

::: desplegable 🧩 Cambié kitty.conf y no se nota el cambio. ¿Qué hago?
`Ctrl+Shift+F5` recarga la configuración. Si sigue igual, revisa el error con `Ctrl+Shift+F6`.
:::

> 📌 Nota: los atajos de fábrica salen de la documentación instalada de kitty (`/usr/share/doc/kitty/kitty.conf`). Ahí algunos aparecen como líneas comentadas (`# map ...`), que describen el valor por defecto; si alguno no responde en tu equipo, mira la lista real con `Ctrl+Shift+F3` (paleta de comandos). Los tuyos están en `~/.config/kitty/kitty.conf`; si cambias alguno, actualiza esta hoja.
