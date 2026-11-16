# 🎬 mpv · Video para estudiar

> El reproductor de tus clases: saltos, velocidad, bucles, marcas y notas con tiempo. Las teclas salen de `input.conf` y de `GUIA-MPV.md`.

## 🧭 Resumen en 30 segundos

mpv **no usa SUPER**: sus teclas solo funcionan con la ventana de mpv enfocada. Lo que más usas:

| Quiero… | Tecla |
|---|---|
| Pausar / seguir | `Espacio`, `k` o clic en el video |
| Pantalla completa | `f` o doble clic (`Esc` sale) |
| Adelantar / atrasar 5 s | `→` / `←` |
| Velocidad más rápida / más lenta | `d` / `a` (±0.1) |
| Velocidad normal | `s` |
| Nota con tiempo | `Ctrl+n` |
| Ver el panel de notas | `h` |
| Repetir un fragmento | `c` (dos veces: inicio y fin) |
| Captura de pantalla | `S` |
| Salir recordando el minuto | `Ctrl+q` |

🧠 Concepto: mpv tiene **teclas de una letra** (`z x y u o p l j`) que saltan distinto. Las de Brave (`z`/`x` = ±5 s) son las que ya conoces del Video Speed Controller; por eso están puestas así.

## ⏩ Adelantar y retroceder

| Tecla | Salto |
|---|---|
| `←` / `→` | −5 / +5 s |
| `Ctrl+←` / `Ctrl+→` | −10 / +10 s |
| `Alt+←` / `Alt+→` | −30 / +30 s |
| `z` / `x` | −5 / +5 s (como Brave) |
| `y` / `u` | −10 / −5 s |
| `o` / `p` | +5 / +10 s |
| `[` / `]` | −30 / +30 s |
| `j` / `l` | −10 / +10 s (como YouTube) |
| `0` … `9` | Salto a 0 %, 10 %, … 90 % del video |
| `.` / `,` | Un cuadro adelante / atrás (con pausa) |
| `Inicio` | Ir al principio |
| `Ctrl+z` | **Deshacer** el último salto |

💡 Consejo: `Ctrl+z` es el «deshacer» que más salva: si saltaste sin querer, vuelves al minuto anterior.

## 🐢 Velocidad

| Tecla | Qué hace |
|---|---|
| `d` / `a` | +0.1 / −0.1 |
| `s` o `Retroceso` | Volver a 1.0x |
| `q` / `w` / `g` / `e` | Velocidad fija 1.3 / 1.5 / 1.8 / 2.0 |
| `v` | Mostrar u ocultar el visor `⏩` |

Rango de 0.25x a 4.0x. El audio conserva el tono y mpv recuerda la última velocidad.

## 🔁 Bucle (repetir un fragmento)

| Tecla | Qué hace |
|---|---|
| `c` | 1ª vez: marca el **inicio** · 2ª: marca el **fin** y repite · 3ª: quita el bucle |
| `Ctrl+c` | Repite los **últimos 15 s** (sin marcar nada) |
| `L` | Lista de **bucles guardados** de este video |

🧠 Concepto: el bucle y la velocidad se combinan: pones el bucle y bajas con `a` para entender una parte difícil.

## 🔖 Marcas (puntos del video)

| Tecla | Qué hace |
|---|---|
| `b` | Marca rápida en el primer número libre (1 a 9) |
| `n` | Saltar a la marca más cercana |
| `B` | Menú con todas las marcas |
| `Ctrl+1` … `Ctrl+9` | Guardar la marca en ese número |
| `Alt+1` … `Alt+9` | Borrar esa marca |
| `Ctrl+b` | Borrar **todas** las marcas del video |
| `RePág` / `AvPág` | Marca o capítulo siguiente / anterior |

## 📝 Notas con tiempo (panel al lado)

| Tecla | Qué hace |
|---|---|
| `Ctrl+n` | **Nota nueva** en este instante: pausa, escribes título y anotación. Toma una captura sola |
| `h` | Ver u ocultar el **panel de notas**: mpv a la izquierda (80 %), panel a la derecha (20 %) |
| `H` | Panel con la lista de reproducción (miniatura de cada clase) |
| `i` | Ventana con los apuntes, tarjetas y resumen del video |
| `r` | Ventana para **recortar** (intro y final) |

⚠️ Cuidado: `Delete` (en la ventana de notas/lista) **borra el video y sus apuntes sin preguntar**. Va a la papelera, pero no tiene confirmación.

## 📂 Lista de videos y cursos

| Tecla | Qué hace |
|---|---|
| `N` · `Enter` · `>` | Video siguiente |
| `P` · `<` | Video anterior |
| `Tab` | Ver la lista y elegir un video |
| `Ctrl+o` | Explorador de carpetas |
| `Alt+c` | Cargar a mano el curso (carpeta padre + subcarpetas) |
| `Alt+C` | Cargar la carpeta actual + sus subcarpetas |
| `C` | Capítulos (con tus marcas incluidas) |

## 🔊 Volumen, subtítulos y otros

| Tecla | Qué hace |
|---|---|
| `↑` / `↓` o rueda | Volumen ±5 |
| `m` | Silenciar |
| `V` | Mostrar u ocultar subtítulos |
| `J` | Cambiar pista de subtítulos |
| `S` | Captura sin subtítulos → `~/Imágenes/Capturas-mpv/` |
| `t` | Tiempo transcurrido y total |
| `Ctrl+i` | Estadísticas técnicas |
| `f` | Pantalla completa (`Esc` sale) |
| `Ctrl+q` | Salir **recordando el minuto** |
| `Ctrl+Shift+q` | Salir sin recordar |

## ⚠️ Errores típicos

- ⚠️ **Cuidado:** `Delete` borra video y apuntes sin preguntar.
- ⚠️ **Cuidado:** `Shift+←/→` **no** hace nada (lo desactivé; mpv trae ±1 s por defecto).
- ⚠️ **Cuidado:** `Ctrl+q` recuerda el minuto; `Ctrl+Shift+q` no. Si quieres volver a donde estabas, usa `Ctrl+q`.
- ✅ Bien: si `Ctrl+n` no responde, asegúrate de que la ventana de mpv esté enfocada (no el navegador).

## 🧠 Practica

::: desplegable 🧩 Quiero repetir un minuto difícil sin marcar nada. ¿Qué pulso?
`Ctrl+c` repite los últimos 15 segundos. Otra vez para quitar el bucle.
:::

::: desplegable 🧩 Salté sin querer al final del video. ¿Cómo vuelvo?
`Ctrl+z` deshace el último salto.
:::

::: desplegable 🧩 ¿Cuál es la diferencia entre `b` y `Ctrl+1`?
`b` guarda la marca en el primer número libre. `Ctrl+1` la guarda en el número 1 y **reemplaza** la que ya estaba ahí.
:::

> 📌 Nota: el panel de notas y el repaso están explicados completos en `~/.config/mpv/GUIA-MPV.md`. Las teclas `b`, `n`, `c`, `Ctrl+n` y `r` vienen de sus scripts, no de `input.conf`.
