# Guía de mpv: reproductor de videos para estudiar

> Configurado el 25-09-2026 en CachyOS + Hyprland.
> Todo vive en `~/.config/mpv/`. Si algo se rompe, borra esa carpeta y mpv vuelve a la configuración de fábrica.

---

## 1. Idea general

**mpv** es un reproductor muy ligero que casi no trae botones: se maneja con el **teclado**. Encima le instalamos:

| Pieza | Qué aporta |
|---|---|
| **uosc** | Interfaz moderna: barra de tiempo, botones y menús para **explorar carpetas y subcarpetas** |
| `velocidad.lua` | Pasos de velocidad de ×0.1, **visor fijo** de la velocidad y memoria de la última velocidad usada |
| `marcadores.lua` | Marcar hasta **9 puntos por video** y saltar a ellos. Quedan guardados aunque cierres mpv |
| `curso.lua` | Cargar un **curso entero** (todas las subcarpetas o módulos) como una sola lista |
| `mpv.conf` | Lista automática con los videos de la carpeta y memoria del minuto donde te quedaste |

### ¿Chocan con los atajos de Hyprland?
**No.** Los atajos de mpv solo funcionan **con la ventana de mpv enfocada**, y **ninguno usa la tecla SUPER**. Todos tus atajos de sistema (SUPER+…, Alt+Tab, Ctrl+Shift+S, Ctrl+Shift+D, Impr…) siguen funcionando igual, también con un video abierto.

---

## 2. Tabla de atajos (la que más vas a usar)

### Reproducción
| Tecla | Acción |
|---|---|
| `Espacio` o `k` | Pausar / reanudar |
| `f` o doble clic | Pantalla completa |
| `Esc` | Salir de pantalla completa |
| `q` | Salir **recordando el minuto** |
| `Q` (Shift+q) | Salir sin recordar |

### Adelantar y retroceder
| Tecla | Acción |
|---|---|
| `→` / `←` | ±5 segundos |
| `Ctrl+→` / `Ctrl+←` | ±10 segundos |
| `Alt+→` / `Alt+←` | ±30 segundos |
| `l` / `j` | ±10 segundos (como en YouTube) |
| `.` / `,` | Un cuadro adelante o atrás (útil en pausa para leer código) |
| `Inicio` | Volver al principio |
| `Ctrl+z` | **Deshacer el último salto** (si adelantaste de más) |

### Velocidad
| Tecla | Acción |
|---|---|
| `]` | +0.1 (1.0 → 1.1 → 1.2 …) |
| `[` | −0.1 |
| `}` (Shift+]) | +0.5 |
| `{` (Shift+[) | −0.5 |
| `Retroceso` (←Borrar) | Volver a 1.0x |
| `Ctrl+v` | Mostrar u ocultar el visor fijo de velocidad |

- Rango: **0.25x a 4.0x**.
- El visor `⏩ 1.30x` aparece arriba a la derecha y desaparece cuando vuelves a 1.0x.
- El audio **conserva el tono**: a 2x la voz suena rápida, pero no aguda.
- mpv **recuerda la última velocidad** para el próximo video y para la próxima vez que lo abras.

> En teclado latinoamericano o español, `[` `]` `{` `}` pueden requerir **AltGr**. Si te resultan incómodas, dímelo y las cambiamos (por ejemplo a `x`/`c`, como la extensión *Video Speed Controller*).

### Marcadores (puntos del video)
| Tecla | Acción |
|---|---|
| `b` | Marca rápida: se guarda en el primer número libre (1 a 9) |
| `Ctrl+1` … `Ctrl+9` | Guardar la marca en ese número (reemplaza la anterior) |
| `1` … `9` | **Saltar** a esa marca |
| `Alt+1` … `Alt+9` | Borrar esa marca |
| `B` (Shift+b) | Menú con todas las marcas: eliges una y salta |
| `Ctrl+b` | Borrar **todas** las marcas del video |
| `RePág` / `AvPág` | Saltar a la marca o capítulo siguiente / anterior |
| `c` | Menú de capítulos con tus marcas incluidas |

- Las marcas se ven como **rayitas en la barra de tiempo**.
- Se guardan **por video** en `~/.local/state/mpv/marcadores.json`. Si mueves o renombras el archivo, esas marcas se pierden.

### Lista de videos, carpetas y cursos
| Tecla | Acción |
|---|---|
| `N` o `Enter` o `>` | Siguiente video |
| `P` o `<` | Video anterior |
| `Tab` | Ver la **lista** y elegir un video |
| `o` | **Explorador de carpetas**: navega carpetas y subcarpetas y abre cualquier video |
| `Alt+c` | **Cargar el curso completo** (carpeta padre + todas sus subcarpetas) |
| `Alt+C` (Alt+Shift+c) | Cargar la carpeta actual + sus subcarpetas |
| Clic derecho | Menú general de uosc |

### Volumen y otros
| Tecla | Acción |
|---|---|
| `↑` / `↓` o rueda del mouse | Volumen ±5 |
| `m` | Silenciar |
| `a` | Bucle A-B: 1ª vez = inicio, 2ª = fin (repite ese trozo), 3ª = quitar |
| `v` | Mostrar u ocultar subtítulos |
| `J` (Shift+j) | Cambiar pista de subtítulos |
| `s` | Captura de pantalla → `~/Imágenes/Capturas-mpv/` |
| `S` | Captura sin subtítulos |
| `t` | Muestra el tiempo transcurrido y el total |
| `i` | Estadísticas técnicas (resolución, códec…) |

---

## 3. Cómo trabajar con tutoriales

### Caso A: una carpeta con varios videos
```
Curso Python/
├── 1 Introducción.mp4
├── 2 Variables.mp4
└── 10 Funciones.mp4
```
Abre **cualquier video** con doble clic en el explorador de archivos. mpv carga automáticamente toda la carpeta **en orden natural** (1, 2, 10; no 1, 10, 2). Con `N` pasas al siguiente, y al terminar un video empieza el siguiente solo.

### Caso B: un curso con módulos en subcarpetas
```
Curso React/
├── Módulo 1/
│   ├── 1 Intro.mp4
│   └── 2 JSX.mp4
└── Módulo 2/
    └── 1 Hooks.mp4
```
Tienes tres formas de verlo:
1. **Abrir un video y pulsar `Alt+c`**: la lista pasa a ser el curso entero, módulo tras módulo, y el video actual no se corta. Al terminar el módulo 1, sigue solo con el módulo 2.
2. **Abrir la carpeta del curso directamente** desde la terminal: `mpv ~/Cursos/"Curso React"`. Carga todo, subcarpetas incluidas.
3. **Pulsar `o`**, entrar a la subcarpeta que quieras y elegir el video.

### Caso C: retomar mañana
Sal con `q`. La próxima vez que abras ese video, empezará en el minuto donde lo dejaste, y tus marcas seguirán ahí.

---

## 4. Rutina recomendada para estudiar

1. Abre el primer video del módulo (o pulsa `Alt+c` para cargar todo el curso).
2. Sube la velocidad con `]` hasta que el ritmo te resulte cómodo (1.3x a 1.7x suele ir bien).
3. En partes difíciles, baja con `[` o vuelve a 1x con `Retroceso`.
4. Cuando algo sea importante, pulsa **`b`** para marcarlo. Después vuelves con `1`…`9` o `B`.
5. ¿Una explicación que no entendiste? `j` retrocede 10 s, o usa `a` dos veces para repetir ese trozo en bucle.
6. ¿El profe escribe código rápido? `Espacio` para pausar y `.` / `,` para avanzar cuadro a cuadro.
7. Captura el código con `s` o con tu atajo del sistema `Ctrl+Shift+S`.

---

## 5. Archivos de la configuración

```
~/.config/mpv/
├── mpv.conf                 ← opciones generales (comentadas en español)
├── input.conf               ← atajos de teclado
├── GUIA-MPV.md              ← esta guía
├── script-opts/uosc.conf    ← opciones de la interfaz uosc (idioma = español)
├── fonts/                   ← íconos de uosc
└── scripts/
    ├── uosc/                ← interfaz (descargada de github.com/tomasklaen/uosc)
    ├── velocidad.lua        ← velocidad + visor
    ├── marcadores.lua       ← marcas por video
    └── curso.lua            ← cargar curso con subcarpetas

~/.local/state/mpv/
├── marcadores.json          ← tus marcas
├── ultima-velocidad         ← última velocidad usada
└── watch_later/             ← minuto donde quedó cada video
```

### Cambiar un atajo
Edita `~/.config/mpv/input.conf`. El formato es `TECLA comando`, por ejemplo:
```
x add speed -0.1
```
Los atajos de velocidad, marcadores y curso se definen en sus scripts `.lua`, pero los mismos scripts explican en su cabecera qué hace cada tecla. Los cambios se aplican la próxima vez que abras mpv.

### Ver qué tecla es cuál
Ejecuta en la terminal `mpv --input-test --force-window --idle`: cada tecla que pulses muestra su nombre y el comando asociado.

---

## 6. Extras

- **mpv es el reproductor predeterminado** de todos los formatos de video (`xdg-mime`). El doble clic en un video lo abre en mpv.
- **Teclas multimedia** (Play/Pausa, Siguiente del teclado o auriculares): necesitan el paquete `mpv-mpris`. Instálalo con:
  ```
  sudo pacman -S mpv-mpris
  ```
- **Actualizar uosc** (de vez en cuando):
  ```
  cd ~/.config/mpv && curl -fsSL -o /tmp/uosc.zip https://github.com/tomasklaen/uosc/releases/latest/download/uosc.zip && unzip -oq /tmp/uosc.zip -d .
  ```
- **Documentación oficial**: `man mpv`, o <https://mpv.io/manual/stable/>.
