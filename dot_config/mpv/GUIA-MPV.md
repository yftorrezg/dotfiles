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

> Desde el 07-10-2026 las teclas se parecen a tu *Video Speed Controller* de Brave.
> Copia de los atajos anteriores: `input.conf.bak-2026-10-07-brave`, `GUIA-MPV.md.bak-2026-10-07` y `scripts/*.lua.bak-2026-10-07`.

### Reproducción
| Tecla | Acción |
|---|---|
| `Espacio`, `k`, `i` o un clic en el video | Pausar / reanudar |
| `f` o doble clic | Pantalla completa |
| `Esc` | Salir de pantalla completa |
| `Ctrl+q` | Salir **recordando el minuto** |
| `Ctrl+Shift+q` | Salir sin recordar |

### Adelantar y retroceder
| Tecla | Acción |
|---|---|
| `z` / `x` | −5 / +5 s |
| `y` / `u` | −10 / −5 s |
| `o` / `p` | +5 / +10 s |
| `[` / `]` | −30 / +30 s |
| `←` `→` · `Ctrl+←→` · `Alt+←→` | ±5 · ±10 · ±30 s |
| `j` / `l` | ∓10 / +10 s (como YouTube) |
| `.` / `,` | Un cuadro adelante o atrás |
| `Inicio` | Volver al principio |
| `Ctrl+z` | **Deshacer el último salto** |

### Velocidad
| Tecla | Acción |
|---|---|
| `d` / `a` | +0.1 / −0.1 |
| `r` o `Retroceso` | Volver a 1.0x |
| `q` / `w` / `g` / `e` | Velocidad fija 1.3 / 1.5 / 1.8 / 2.0 |
| `v` | Mostrar u ocultar el visor fijo `⏩` |

Rango 0.25x a 4.0x. El audio conserva el tono. mpv recuerda la última velocidad.

### Bucle (repetir un fragmento)
| Tecla | Acción |
|---|---|
| `c` | 1ª vez: marca el **inicio** · 2ª vez: marca el **fin** y empieza a repetir · 3ª vez: quita el bucle |
| `Ctrl+c` | Repite los **últimos 15 s** al instante (no marcas nada). Otra vez: quita el bucle |
| `L` (Shift+l) | Lista de **bucles guardados** de este video: eliges uno y se activa |

- Arriba a la izquierda se ve `🔁 A 12:30 → B 13:10` mientras repite, y el trozo se pinta en la barra de tiempo.
- Cada bucle que cierras se guarda solo, por video, en `~/.local/state/mpv/bucles.json` (máx. 20). Al reabrir el video lo encuentras con `L`.
- Se puede combinar con la velocidad: pon el bucle y baja con `a` para entender una parte difícil.

### Marcadores (puntos del video)
| Tecla | Acción |
|---|---|
| `b` | Marca rápida: se guarda en el primer número libre (1 a 9) |
| `n` | **Saltar a la marca más cercana** (la que no tienes encima) |
| `1` … `9` | Saltar a esa marca |
| `Ctrl+1` … `Ctrl+9` | Guardar la marca en ese número (reemplaza la anterior) |
| `Alt+1` … `Alt+9` | Borrar esa marca |
| `B` (Shift+b) | Menú con todas las marcas |
| `Ctrl+b` | Borrar **todas** las marcas del video |
| `RePág` / `AvPág` | Marca o capítulo siguiente / anterior |
| `C` (Shift+c) | Menú de capítulos con tus marcas incluidas |

Las marcas se ven como rayitas en la barra y se guardan en `~/.local/state/mpv/marcadores.json`.

### Notas con tiempo (panel al lado)
| Tecla | Acción |
|---|---|
| `Ctrl+n` | **Nueva nota** en este instante: pausa, escribes el **título** (con `?`, `!` o `p` al inicio si quieres un tipo; `Enter`) y la **anotación** (`Enter`), y el video sigue. Toma una captura sola. `Esc` en el título cancela; `Esc` en la anotación guarda solo con título |
| `H` (Shift+h) | **Panel con la lista de reproducción** (miniatura + título de cada clase, la actual resaltada y centrada; clic = reproducir). Mismo panel al 20 % a la derecha; también está el botón **Lista** dentro del panel |
| `h` | **Ver / ocultar el panel de notas**: mpv queda al 80 % a la izquierda y el panel al 20 % a la derecha (si estabas en pantalla completa, sale de ella) |

En el panel (ventana de Brave): clic en `⏱ 12:34` o en la captura = mpv **salta a ese minuto**; la nota del momento actual se resalta y el panel la sigue solo (casilla *seguir*); `Editar` / `Borrar` en cada nota; buscador; `＋ Nota` crea una nota desde el panel; `Videos` lista **todos los videos con notas** y al pulsar uno lo abre en mpv.

**Tipos de nota**: empieza el título con `?` (duda), `!` (clave) o `p` (practicar), por ejemplo `? por qué className`. Un título que empieza con `¿` cuenta como duda. En el panel cada tipo tiene color e insignia, y los botones ❓ 🔑 🛠️ filtran.

- **Repaso** (botón del panel, con contador): las notas `?` `!` `p` de TODOS tus videos que toca ver hoy. La anotación sale borrosa: intenta recordarla y pulsa para verla; luego **Ya lo sé** (vuelve en 2, 4, 8… hasta 60 días) o **Repetir** (mañana). Clic en el minuto abre el video ahí.
- **Tarjetas**: tus notas `?` se vuelven `tarjetas.md` (plugin Spaced Repetition de Obsidian, conserva tu progreso).
- **Cuadernillo**: si el video tiene su carpeta en `Capturas de YouTube/`, se escribe ahí `mis-notas.md` junto a `apuntes.md` (que no se toca).

- Cada nota queda ligada a su video: `~/Vídeos/Notas de videos/<nombre del video>/` con `notas.md` (legible), `notas.json`, `tarjetas.md` y `capturas/`. Está **dentro de tu bóveda de Obsidian** (`~/Vídeos`), así que lo ves y lo repasas allí (`~/Documentos/Notas-cursos` es un acceso directo a la misma carpeta). El archivo `indice.json` enlaza la ruta de cada video con su carpeta, así que si abres el mismo video otro día, sus notas aparecen.
- Si renombras o mueves el video, sus notas antiguas siguen en su carpeta (se ven en `Videos`), pero el video nuevo empieza sin notas.
- El panel habla con mpv por un socket (`$XDG_RUNTIME_DIR/mpv-notas.sock`). Con **dos ventanas de mpv**, controla la última que abriste; pulsa `h` en otra ventana para que el panel pase a controlar esa.
- El servidor del panel (`panel-notas/servidor.py`, puerto 47831) se arranca solo con `h` y se apaga tras 20 min sin uso.

### Lista de videos, carpetas y cursos
| Tecla | Acción |
|---|---|
| `N` (Shift+n) o `Enter` o `>` | Siguiente video |
| `P` (Shift+p) o `<` | Video anterior |
| `Tab` | Ver la **lista** y elegir un video |
| `Ctrl+o` | **Explorador de carpetas** |
| `Alt+c` | **Cargar el curso completo** (carpeta padre + subcarpetas) |
| `Alt+C` (Alt+Shift+c) | Cargar la carpeta actual + sus subcarpetas |
| Clic derecho | Menú general de uosc |

### Volumen y otros
| Tecla | Acción |
|---|---|
| `↑` / `↓` o rueda del mouse | Volumen ±5 |
| `m` | Silenciar |
| `V` (Shift+v) | Mostrar u ocultar subtítulos |
| `J` (Shift+j) | Cambiar pista de subtítulos |
| `s` / `S` | Captura de pantalla / sin subtítulos → `~/Imágenes/Capturas-mpv/`. Si el video dura **más de 1 hora**, va a una subcarpeta con el nombre del video (`capturas.lua`) |
| `t` | Tiempo transcurrido y total |
| `Ctrl+i` | Estadísticas técnicas |

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
Sal con `Ctrl+q`. La próxima vez que abras ese video, empezará en el minuto donde lo dejaste, y tus marcas seguirán ahí.

---

## 4. Rutina recomendada para estudiar

1. Abre el primer video del módulo (o pulsa `Alt+c` para cargar todo el curso).
2. Sube la velocidad con `d` (o salta con `w`/`g`/`e`) hasta que el ritmo te resulte cómodo (1.3x a 1.7x suele ir bien).
3. En partes difíciles, baja con `a` o vuelve a 1x con `r`.
4. Cuando algo sea importante, pulsa **`b`** para marcarlo. Después vuelves con `n`, `1`…`9` o `B`.
5. ¿Una explicación que no entendiste? `y` retrocede 10 s, o `Ctrl+c` para repetir los últimos 15 s (o `c` dos veces para elegir tú el trozo).
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
├── panel-notas/             ← servidor.py + panel.html + panel-toggle.sh (panel de notas)
├── fonts/                   ← íconos de uosc
└── scripts/
    ├── uosc/                ← interfaz (descargada de github.com/tomasklaen/uosc)
    ├── velocidad.lua        ← velocidad + visor
    ├── marcadores.lua       ← marcas por video
    ├── capturas.lua         ← carpeta de capturas por video (si dura más de 1 h)
    ├── notas.lua            ← Ctrl+n nota nueva, h panel de notas
    ├── bucle.lua            ← repetir fragmentos y guardarlos
    ├── curso.lua            ← cargar curso con subcarpetas
    └── bateria.lua          ← laptop: render liviano cuando está desenchufada

~/.local/state/mpv/
├── marcadores.json          ← tus marcas
├── bucles.json              ← tus bucles guardados
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
- **Laptop (Intel Iris Xe)**: los videos se decodifican con la gráfica (`hwdec=vaapi`, menos CPU y batería). Para comprobarlo, con un video abierto pulsa `i`: debe decir `vaapi` junto al códec. Sin cargador, `bateria.lua` activa el perfil `[bateria]` de `mpv.conf` (escalado simple); al enchufar vuelve solo.
- **Documentación oficial**: `man mpv`, o <https://mpv.io/manual/stable/>.
