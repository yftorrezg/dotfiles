# 🪟 Portar todo a Windows 11 — ASUS Zenbook Pro Duo 15 OLED (UX582)

*Escrito el 28/09/2026 · Laptop: i7 12ª gen, 32 GB DDR5, RTX 3060 Laptop, SSD 1 TB, OLED 4K + ScreenPad Plus · En W11 ya andan: Stream Deck y Logitech MX Master 4.*

> **Pregunta:** ¿todo lo que hay en la PC con CachyOS (doblaje, capturas y apuntes de cursos, dictado, lectura en voz alta, atajos, visores, automatizaciones) se puede tener en Windows 11? ¿Cómo, y qué conviene?
>
> **Respuesta corta:** **sí, casi todo**, pero en Windows **no se copia: se rearma** con otras herramientas. La lógica "inteligente" (Python: detector de capturas, cuadernillo, doblaje, tarjetas) ya es portable. Lo que hay que rehacer es la "cáscara" que habla con Linux/Wayland (atajos, capturas de pantalla, notificaciones, barrita). **Recomendación: dual boot** (CachyOS para estudiar + W11 para lo que solo anda bien ahí), **probando antes CachyOS en vivo por USB**. Si Linux falla en algo crítico del hardware → **W11 + WSL2** (plan B, también viable).

---

## ⚡ Resumen: función por función

| Función de la PC | ¿En W11? | Cómo se haría en Windows | Nota |
|---|---|---|---|
| 🪟 Ventanas en mosaico + escritorios virtuales | 🟡 | **GlazeWM** (o FancyZones de PowerToys) + escritorios nativos de Windows (ya cambian todos los monitores a la vez) | No es tan fluido como Hyprland, pero cumple |
| ⌨️ Atajos globales (apps web, escritorios, capturas…) | ✅ | **AutoHotkey v2** + PowerToys Keyboard Manager (+ Stream Deck) | Muchos ya existen igual: Win+V, Win+Shift+S, Win+E, Win+. |
| 🚀 Lanzador / barra | ✅ | PowerToys **Command Palette** · barra: YASB o Zebar | |
| 📸 Capturas manuales + OCR | ✅ mejor | **ShareX** o Snipping Tool + **Text Extractor** (PowerToys) | |
| 🎙️ Dictado por voz | ✅ mejor | **Handy** u **OpenWhispr** con Whisper *large-v3-turbo* en la **RTX 3060** (o Win+H nativo) | Más rápido que hoy gracias a CUDA |
| 🔊 Lectura en voz alta (SUPER+R) | ✅ | Atajo AHK que copia la selección → tu `limpiar-texto.py` → edge-tts o Piper | En Windows no hace falta ydotool |
| 🎬 Doblaje inglés → español | ✅ mejor | **WSL2 + CUDA** (tus scripts casi sin cambios) → `device="cuda"` | Estimado 3–8 min de transcripción por hora de video (hoy ~30 min por CPU) |
| 📥 `descargar` (yt-dlp) | ✅ | yt-dlp igual (WSL2 o nativo) | Cookies de Brave/Chrome en Windows: más difícil (cifrado nuevo) |
| 🎓 Capturas + apuntes de cursos, playlists, cola, tarjetas, panel | ✅ | Motor en **WSL2 sin cambios** + barrita en la **ScreenPad Plus** + captura en vivo con `mss` | Etapa 1 ≈ 20–30 h de trabajo (Parte B) |
| 📊 Barrita de progreso discreta | ✅ | Ventana "siempre encima", semitransparente, sin foco, en la **ScreenPad Plus** | La ScreenPad reemplaza al monitor vertical |
| 🎞️ Visor de videos (mpv) | ✅ | **mpv / mpv.net** con tu misma config | |
| 🖼️ Visor de fotos | ✅ | **ImageGlass** o qView | |
| 📓 Obsidian (bóveda Vídeos, plugin de tarjetas) | ✅ | Igual | Guardar los cursos en NTFS (`C:\Cursos`), no dentro de WSL |
| 💾 Backups (restic) y snapshots (snapper/btrfs) | 🟡 / ❌ | restic existe para Windows; **snapshots del sistema como btrfs: no hay equivalente real** (Restaurar sistema es mucho peor) | Una de las ventajas grandes de Linux |
| ☁️ Drive (rclone) | ✅ | **Google Drive para escritorio** (mejor en Windows); rclone también existe | |
| 🎛️ Stream Deck · 🖱️ MX Master 4 | ✅ mejor | Apps oficiales (Elgato, Logi Options+) | En Linux: OpenDeck / Solaar, con limitaciones |
| 🎨 Estética Hyprland / Noctalia | ❌ | No vale la pena intentarlo | |

**Leyenda:** ✅ igual o mejor · 🟡 parcial · ❌ no.

## 🧭 Las 3 opciones, en una línea cada una

| Opción | Esfuerzo | Tu flujo de estudio | Hardware ASUS + Stream Deck + MX4 | Cuándo elegirla |
|---|---|---|---|---|
| **(a) W11 nativo + herramientas** | Alto (reescribir) | 🟡 portado | ✅ | Si no querés tocar Linux en la laptop |
| **(b) W11 + WSL2** | Medio | ✅ (motor en WSL2) | ✅ | **Plan B** si CachyOS falla en la Zenbook |
| **(c) Dual boot CachyOS + W11** | **Bajo** (ya está todo documentado en este paquete) | ✅ tal cual | 🟡 en Linux (probar) · ✅ en Windows | **Recomendado**, después de probar con USB |

## ✅ Plan recomendado (en orden, sin riesgos)

1. **W11 "domado" (1 tarde):** privacidad y actualizaciones (Parte A §7), PowerToys, AutoHotkey con tus atajos principales, Handy/OpenWhispr, ShareX, mpv, Google Drive. Así la laptop ya es útil pase lo que pase.
2. **Probar CachyOS en vivo por USB (15 min)** con el checklist de la Parte A §6.3: las dos pantallas, táctil de cada una, brillo de la ScreenPad, audio, `nvidia-smi`, suspensión y lápiz.
3. **Si pasa → dual boot:** antes **guardar la clave de recuperación de BitLocker**, resolver Secure Boot y **desactivar el Inicio rápido** de Windows. Aplicar este paquete con MONITOR1 = OLED y MONITOR2 = ScreenPad; doblaje con CUDA.
4. **Si algo crítico falla en Linux → plan B (W11 + WSL2)** siguiendo la Parte B (orden de migración y esfuerzo por script).

**El porqué:** tu ventaja no es Hyprland en sí, sino los ~45 scripts que hablan con Linux (`hyprctl`, `grim`, `wl-paste`, `ydotool`, systemd). Pasarlos a Windows es "portar a otra plataforma": la lógica se conserva, la capa de sistema se reescribe. En Linux esa capa ya existe; el riesgo del dual boot (el hardware) se mide en 15 minutos con un USB, mientras que el tiempo de reescribir no se recupera.

## ⚠️ Riesgos a tener en cuenta en W11
- **OneDrive** puede adueñarse de `Videos`/`Documentos` y ponerse a sincronizar miles de capturas → guardar los cursos en una carpeta propia (`C:\Cursos`) fuera de OneDrive.
- **Defender** escanea cada captura → excluir la carpeta de cursos (o usar un Dev Drive).
- **Suspensión** en medio de una playlist larga → el script debe pedirle a Windows que no suspenda (o configurarlo al procesar de noche).
- **Codificación** (cp1252 en vez de UTF-8) rompe los emojis y los prompts → forzar UTF-8 (`PYTHONUTF8=1`).
- **ScreenPad Plus:** tras algunas actualizaciones de W11 su táctil controla la pantalla principal → ASUS lo arregla con ScreenXpert ≥ 3.0.2.0 + ScreenPad Optimizer ≥ 1.2.3.0.
- **OLED:** evitar barras fijas todo el día (quemado) → barras que se ocultan solas.

## ❓ Lo que falta verificar en la laptop
MUX switch del UX582ZM, audio/suspensión/lápiz en Linux, qué GPU maneja cada pantalla en Linux, tiempos reales de doblaje en la 3060 Laptop, cookies de Brave con yt-dlp en Windows, "Virtual Stream Deck" en la ScreenPad. (Detalle en Parte A §9.)

---

# Parte A — Equivalentes en Windows 11 y comparación de opciones

## 0. Resumen en 30 segundos

1. **Casi todo tiene equivalente en Windows 11, pero muy poco se copia tal cual.** En Linux tu config son archivos que se copian: `binds.lua`, scripts bash/Python sobre `hyprctl`, `grim`, `wl-clipboard`, `ydotool` y *layer-shell*. En Windows hay que **rearmarla** con otras piezas: PowerToys + AutoHotkey v2 + un gestor de mosaico (GlazeWM o komorebi) + ShareX + una app de dictado. Resultado esperado: ~80 % de la *experiencia*, pero reescribiendo ~70 % de la *implementación*.
2. **Lo que Windows hace mejor en esta laptop:** la **ScreenPad Plus** (ScreenXpert, táctil bien asignado, brillo), el **lápiz**, **Stream Deck (app oficial de Elgato)**, **Logi Options+** (MX Master 4 completo: háptica, Actions Ring), **Optimus/NVIDIA sin pelear** y el soporte del fabricante (MyASUS). También los **escritorios virtuales nativos, que cambian todos los monitores a la vez**, igual que tu lógica de `switchVirtualDesktop()`.
3. **Lo que Linux hace mejor:** tu flujo de estudio (auto-captura → cuadernillo con Claude, SUPER+R, `descargar`, `doblar`, mpv de estudio) **ya está escrito para Linux**. Los snapshots btrfs/snapper, el control total del sistema, cero telemetría y cero actualizaciones forzadas.
4. **La RTX 3060 cambia el doblaje:** con CUDA (en CachyOS nativo o en WSL2), Whisper *large-v3-turbo* + NLLB en GPU deberían bajar la transcripción de ~30 min por hora de video (hoy, CPU) a **~3–8 min por hora** (estimación, §4.F). Lo que pasa a mandar el tiempo total es edge-tts (internet).
5. **Recomendación:** **dual boot**, con **CachyOS como sistema de estudio diario** y **Windows 11 "domado" para lo que solo anda bien ahí** (ScreenXpert, Stream Deck oficial, Options+, lápiz, juegos o apps de Windows). Antes de instalar, **probar CachyOS en vivo por USB** en la Zenbook con el checklist de §6.3. Si después de la prueba algo crítico falla en Linux (la ScreenPad o el audio), el plan B es W11 + herramientas + WSL2 (§6.1–6.2), que también es viable.

---

## 1. Premisas del hardware (por qué importan)

| Dato | Consecuencia |
|---|---|
| **UX582 de 12ª gen = UX582ZM** (i7-12700H / i9-12900H + RTX 3060), según las fichas de Amazon, Best Buy y el marketplace de NVIDIA [F1][F2] | Hay otras variantes UX582 (10ª/11ª gen: UX582LR/HS/HM). Los foros mezclan modelos: cuidado al seguir guías |
| RTX 3060 **Laptop**: 6 GB de VRAM (no verificado para tu unidad; la de escritorio tiene 12 GB) | Whisper turbo int8 (~1,5–3 GB) + NLLB 600M caben, **de a uno por vez** |
| Gráficos híbridos Intel Iris Xe + NVIDIA (Optimus). **No encontré fuente que confirme o niegue un MUX switch** en el UX582ZM **(no verificado)** | En Windows no importa. En Linux, Hyprland debe renderizar con la iGPU y la NVIDIA queda para CUDA (§6.3) |
| **ScreenPad Plus** 3840x1100, táctil, inclinable, gestionada por **ScreenXpert** [F3][F4] | En Windows es un **segundo monitor extendido normal** con táctil propio. Cumple el papel de tu **monitor vertical HP** (chats, Drive, barrita de progreso), pero es una **tira ancha y baja**, no vertical |
| OLED 4K 15,6" | Escala 250–300 %. **Riesgo de quemado (burn-in)** con barras estáticas: tu barra Noctalia ya se oculta sola; en Windows haz lo mismo (§4.C) |
| Periféricos del usuario: Stream Deck (XL + Mirabox HSV293S + Fifine D6), MX Master 4 (en la laptop; en la PC usa M720), K380, Maono DM40 | Stream Deck y Options+ **funcionan mejor en Windows** (§4.I) |

---

## 2. Inventario de la PC (lo que hay que replicar)

Salió de `docs/01–07`, `GAPS.md`, `binds.lua`, `systemctl --user` y tus guías:

| Área | Qué hay en la PC |
|---|---|
| Ventanas | Hyprland 0.56 (config Lua), mosaico dwindle, flotar, pantalla completa/maximizar, `togglesplit`, arrastrar/redimensionar con SUPER+ratón, zoom de pantalla SUPER +/−, scratchpad SUPER+S |
| Escritorios | 5 "escritorios virtuales" que cambian **los dos monitores a la vez** (ws i en DP-3 + ws i+5 en el vertical), SUPER+1..5, SUPER+CTRL+←/→, SUPER+rueda, SUPER+Tab (ventanas del escritorio actual), mover ventana a escritorio o monitor, workspace `estudio` |
| Reglas | Apps web con escritorio fijo (redes → 1, chats → 6, Drive → 8, VS Code → 4), PiP flotante y fijado, diálogos flotantes |
| Monitores | Principal 1080p horizontal + HP rotado 90° (vertical) |
| Shell | Noctalia: barra auto-oculta, lanzador (SUPER solo), emojis (SUPER+.), portapapeles (SUPER+V), centro de control, notificaciones, bloqueo (SUPER+L), OSD de volumen y brillo, fondos, tema generado desde el fondo |
| Atajos de apps | Terminal, Archivos, Brave, Obsidian, VS Code (enfocar o abrir), 7 apps web "enfocar o abrir" (YouTube, WhatsApp, Telegram, Facebook, Instagram, Drive, TikTok), btop, matar LibreOffice, OpenDeck |
| Capturas | Impr/SUPER+Impr (Noctalia → satty), SUPER+SHIFT+S (zona → portapapeles), CTRL+SHIFT+S (zona → carpeta + portapapeles), CTRL+SHIFT+D (elegir carpeta), botones del mouse |
| Estudio | **Auto-captura** SUPER+ALT+S (guarda solo si la pantalla cambió), **SUPER+ALT+Y** (link de YouTube → capturas + apuntes), **SUPER+ALT+A** (curso entero → cuadernillo con OCR tesseract + `claude -p`, `resumen.md`, `tarjetas.md` para Spaced Repetition/Anki), barrita de progreso *layer-shell* en el monitor vertical, `video-a-capturas.sh`, sesión de curso SUPER+C / SUPER+ALT+C, pomodoro |
| Voz | **Dictado** hyprwhspr (whisper.cpp `small` en CPU, SUPER+ALT+Z es / SUPER+ALT+X en, micrófono Maono). **Lectura** SUPER+R (selección → limpieza → edge-tts / Piper con daemon / Chatterbox; Ctrl+C simulado con ydotool), SUPER+ALT+R para elegir la voz |
| Video | `descargar` (yt-dlp con cookies de Brave), `doblar` (Whisper → NLLB → edge-tts → ffmpeg; GTX 980 por Vulkan o CPU), **mpv** de estudio (uosc, marcadores, velocidad, curso.lua, saltos ±5/10/30 s) |
| Apps | Brave (+PWA `--app`), kitty, Dolphin, Gwenview, mpv, Obsidian, VS Code, LibreOffice, Claude Desktop/Code, KeePassXC, LocalSend, RustDesk, OBS, arduino-cli, Android Studio |
| Sistema | fish (cachyos-fish-config), restic diario a un disco externo, snapper/btrfs + Limine, rclone mount de Drive, servicios de usuario (hyprwhspr, piper-daemon, ydotool, rclone, backup timer), restaurar ventanas de Brave al iniciar (`sesion-ventanas.py`), tema oscuro, cursor Bibata |
| Periféricos | 3 Stream Decks con OpenDeck (docenas de botones → comandos Hyprland), mouse con logiops, K380 |

---

## 3. Cómo leer las tablas: "atajos que Windows ya ocupa"

Antes de mapear atajos, conviene saber cuáles de tus SUPER+X **ya existen en Windows** (Win = SUPER):

| Tu atajo | En Windows ya es… | ¿Choca? |
|---|---|---|
| SUPER+V portapapeles | **Win+V historial del portapapeles** | ✅ **Mismo propósito** |
| SUPER+SHIFT+S captura → portapapeles | **Win+Shift+S Recortes** | ✅ **Mismo propósito** |
| SUPER+Impr pantalla completa | **Win+Impr** guarda en Imágenes\Capturas | ✅ Igual |
| SUPER+E archivos | Win+E Explorador | ✅ Igual |
| SUPER+L bloquear | Win+L bloquear (reservado, no se puede reasignar) | ✅ Igual |
| SUPER+. emojis | Win+. emojis | ✅ Igual |
| SUPER +/− zoom | Win +/− **Lupa** | ✅ Igual |
| SUPER+CTRL+←/→ escritorio anterior/siguiente | **Win+Ctrl+←/→ escritorios virtuales** | ✅ Igual |
| CTRL+SHIFT+Esc btop | Ctrl+Shift+Esc Administrador de tareas | ✅ Equivalente |
| SUPER solo = lanzador | Win solo = Inicio | 🟡 Reasignable a PowerToys Run / Command Palette |
| SUPER+R leer | Win+R "Ejecutar" | 🟡 AutoHotkey puede quitárselo |
| SUPER+D maximizar | Win+D mostrar escritorio | 🟡 Choca: decidir |
| SUPER+Tab ventanas del escritorio | Win+Tab Vista de tareas | 🟡 Choca: decidir |
| SUPER+A notificaciones | Win+A configuración rápida · Win+N notificaciones | 🟡 Parecido |
| SUPER+N Obsidian | Win+N notificaciones | 🟡 Choca |
| SUPER+W Brave | Win+W widgets | 🟡 Choca (se puede desactivar Widgets) |
| SUPER+G VS Code | Win+G Game Bar | 🟡 Se desactiva la Game Bar |
| SUPER+K OpenDeck | Win+K transmitir | 🟡 Choca |
| SUPER+H — | **Win+H dictado de Windows** | Libre en tu config |
| SUPER+1..5 escritorio | Win+1..5 abrir la app N de la barra de tareas | 🟡 AutoHotkey/GlazeWM los toman |

**Por qué pasa esto (lo conceptual):** en Hyprland el compositor **es** el dueño de todas las teclas, y tu `binds.lua` define el sistema entero. En Windows, el dueño es **Explorer/shell**: registra sus Win+X primero, y las herramientas de terceros (AutoHotkey, GlazeWM) "secuestran" esas teclas con un *hook* de teclado de bajo nivel (`SetWindowsHookEx`). Por eso casi todo se puede reasignar, **salvo Win+L** (y Ctrl+Alt+Supr), que Windows protege a propósito por seguridad.

---

## 4. Tablas por área

### 4.A Ventanas en mosaico y escritorios virtuales

| Función | W11 | Herramienta concreta | Cómo, en líneas generales | Pierdes / ganas |
|---|---|---|---|---|
| Mosaico automático tipo i3/Hyprland | ✅ | **GlazeWM v3.10.1** (21-03-2026, gratis, open source) [F5] **o komorebi v0.1.41** (03-05-2026) + **whkd v0.2.10** [F6] | GlazeWM: un solo `config.yaml` con *keybindings*, *window_rules* y *workspaces* (muy parecido a tu `binds.lua`). komorebi: más potente (layouts, pilas, reglas por monitor), pero atajos aparte (whkd o AHK) | **Licencia:** komorebi es gratis **solo para uso personal**; está prohibido usarlo en un trabajo pago (Komorebi License 2.0.0) [F6]. GlazeWM no tiene esa restricción. Pierdes: animaciones, blur, bordes con gradiente, *swallow* de terminal. Algunas ventanas de Windows (UWP, diálogos de sistema) se resisten al mosaico |
| Zonas manuales (sin mosaico automático) | ✅ | **PowerToys FancyZones** (PowerToys v0.101, 25-08-2026) [F7] | Defines zonas por monitor, incluida la ScreenPad; Shift+arrastrar o Win+flechas | Más "Windows-like" y estable; menos automático |
| Snap nativo | ✅ | Win+Z / Win+flechas | — | Viene de fábrica |
| Mover/redimensionar con modificador + arrastrar | ✅ | PowerToys **Grab And Move** (nuevo) [F7] | Modificador + arrastrar dentro de la ventana | = SUPER+clic izq./der. |
| Flotar (SUPER+ALT+Espacio), pantalla completa, `togglesplit` | ✅ | GlazeWM `toggle-floating`, `toggle-fullscreen`, `toggle-tiling-direction` | Atajos en `config.yaml` | Igual |
| **5 escritorios que cambian ambas pantallas a la vez** | ✅ (**mejor que nativo en Linux**) | **Escritorios virtuales nativos** de W11 + **AutoHotkey v2.0.28** (12-09-2026) [F8] + **VD.ah2** / **VirtualDesktopAccessor** [F9] | En Windows **un escritorio virtual ya abarca todos los monitores**: lo que en Hyprland hiciste a mano (`switchVirtualDesktop`), acá es el comportamiento de fábrica. AHK agrega Win+1..5 (ir), Win+Ctrl+1..5 (mover ventana), Win+rueda y "fijar app a escritorio" | Win+Ctrl+←/→ ya viene. Nota: **GlazeWM/komorebi usan sus propios workspaces por monitor** (como Hyprland). Con GlazeWM puedes imitar tu lógica con un atajo que ejecute dos comandos (`focus --workspace 6` y luego `--workspace 1`) **(sintaxis de lista de comandos no verificada)**. Elige **uno** de los dos modelos: no mezclar escritorios nativos con workspaces de GlazeWM |
| SUPER+Tab = ciclar ventanas del escritorio actual | ✅ | AHK (`WinGetList` filtrado por escritorio) o PowerToys **Window Hopper** (cicla ventanas de la misma app) [F7] | Script AHK de ~20 líneas | — |
| Scratchpad SUPER+S | 🟡 | AHK: `WinHide`/`WinShow` de una ventana "cajón" | Un toggle que muestra u oculta p. ej. una terminal | No hay scratchpad nativo; GlazeWM no lo trae **(no verificado en v3.10)** |
| Reglas de ventana (app → escritorio fijo, PiP flotante) | 🟡 | GlazeWM `window_rules` (mueve por proceso o título); con escritorios nativos, AHK + VD.ah2 "mover ventana al escritorio N" al detectarla; PowerToys **Always On Top** para PiP | Las PWA de Brave se identifican por el **título** o por el AppUserModelID; es menos limpio que la clase `brave-web.whatsapp.com__-Default` | Más frágil que `windowrules.lua` |
| Restaurar ventanas al iniciar (`sesion-ventanas.py`) | 🟡 | Brave "Continuar donde lo dejaste" + W11 "Reiniciar apps al iniciar sesión" + PowerToys **Workspaces** (abre un set de apps en posiciones guardadas, con un clic) [F10] | Un Workspace de PowerToys "Estudio" y otro "Redes" | No hay un daemon que devuelva cada ventana de Brave a su escritorio; se podría portar el script a Python + pywin32 (trabajo medio) |
| Monitor vertical rotado | ✅ | Configuración → Pantalla → Orientación | — | En la laptop no hay monitor vertical: lo reemplaza la ScreenPad (§4.J) |

**Mi elección para ti en Windows:** **escritorios nativos + AutoHotkey v2 + FancyZones**, y agregar **GlazeWM** solo si extrañas el mosaico automático. Es la combinación que menos se rompe con las actualizaciones de Windows y la que mejor respeta la ScreenPad (ScreenXpert también mueve ventanas y puede pelearse con un gestor de mosaico **(no verificado; probarlo)**).

### 4.B Atajos globales (todo `binds.lua`, agrupado)

La herramienta es **AutoHotkey v2** (gratis, madura, 20 años). Un solo `yafer.ahk` en `shell:startup` reemplaza a `binds.lua`, los scripts `app-web.sh`/`curso-*.sh` y buena parte de los botones de OpenDeck. **PowerToys Keyboard Manager** sirve para remapeos simples, sin lógica [F11].

| Grupo (binds.lua) | W11 | Equivalente |
|---|---|---|
| Ventanas: Q cerrar, D/F, J, flechas, SHIFT+flechas, SHIFT+1/2 monitor, ALT+Tab | ✅ | GlazeWM o AHK (`WinClose`, `WinMaximize`). Win+Shift+←/→ ya mueve la ventana de monitor (nativo). Alt+Tab nativo |
| Apps: Enter terminal, E archivos, W Brave, N Obsidian, G VS Code, XF86Calculator | ✅ | AHK `Run` + "enfocar si existe" (`WinExist`/`WinActivate`) |
| **Apps web "enfocar o abrir"** SUPER+ALT+Q/W/T/F/I/D, SUPER+T | ✅ | AHK: `if WinExist("WhatsApp ahk_exe brave.exe") WinActivate else Run 'brave.exe --app=https://web.whatsapp.com'`. Es la lógica exacta de `app-web.sh`, más simple porque no hace falta `hyprctl -j` + `jq` |
| CTRL+SHIFT+Esc btop, CTRL+ALT+Esc matar LibreOffice | ✅ | Nativo (Administrador de tareas) / AHK `ProcessClose("soffice.bin")` |
| Noctalia: Z ajustes, X centro de control, SUPER lanzador, . emojis, L bloquear, V portapapeles, A notificaciones | ✅ | Win+I, Win+A, PowerToys Run/Command Palette, Win+., Win+L, Win+V, Win+N (ver §4.C) |
| Multimedia/brillo (XF86…) | ✅ | Nativo |
| Capturas: Impr, SUPER+Impr, CTRL+SHIFT+S/D, SUPER+SHIFT+S | ✅ | ShareX / Recortes + AHK (§4.D) |
| Estudio: SUPER+ALT+S/Y/A, SUPER+C, SUPER+ALT+C/E | 🟡 | AHK que llama a los scripts Python portados (§4.D) |
| Voz: SUPER+R, SUPER+ALT+R, SUPER+ALT+Z/X | ✅/🟡 | §4.E |
| Escritorios: 1..5, CTRL+1..5, CTRL+←/→, rueda, Tab, ALT+1/2, S | ✅ | §4.A |
| SUPER+K OpenDeck | ✅ | Abrir la app Stream Deck |
| Gestos del touchpad (4 dedos = escritorio; 3 dedos = cerrar/fullscreen/flotar) | ✅/🟡 | W11 trae **3 y 4 dedos** configurables (escritorios, Vista de tareas, multimedia) en Configuración → Panel táctil. "3 dedos = cerrar ventana" no existe (y es mejor así: en tu doc 01 ya figura como gesto peligroso) |

Ejemplo mínimo para que veas el "idioma" (AHK v2; `#` = Win, `!` = Alt, `^` = Ctrl, `+` = Shift):

```ahk
#Requires AutoHotkey v2.0
AppWeb(titulo, url) {                      ; = app-web.sh
    if WinExist(titulo " ahk_exe brave.exe")
        WinActivate
    else
        Run 'brave.exe --app=' url
}
#!w::AppWeb("WhatsApp", "https://web.whatsapp.com")
#!t::AppWeb("Telegram", "https://web.telegram.org")
#g::(WinExist("ahk_exe Code.exe") ? WinActivate() : Run("code"))
^!Esc::ProcessClose("soffice.bin")
#r::Run 'pythonw "' A_ScriptDir '\leer-seleccion.pyw"'   ; SUPER+R (ver §4.E)
```

### 4.C Shell, barra, lanzador, portapapeles, notificaciones, tema

| Función (Noctalia) | W11 | Herramienta | Notas |
|---|---|---|---|
| Barra (workspaces, reloj, CPU/RAM/temp, media, tray, red, volumen) | ✅ | **YASB v2.0.7** (11-09-2026, config YAML+CSS, widgets de GlazeWM/komorebi) [F12] o **Zebar v3.3.1** (de los autores de GlazeWM, widgets en HTML/JS) [F13]; o la barra de tareas nativa oculta automáticamente | **OLED:** usa auto-ocultar o una barra fina y oscura; las barras fijas son el caso típico de quemado |
| Lanzador (SUPER solo), calculadora, emojis | ✅ | **PowerToys Command Palette** (sucesor de PowerToys Run) [F14] o **Flow Launcher v2.1.4** (20-09-2026, muchos plugins) [F15]; emojis con Win+. | "SUPER solo" → AHK: `LWin up` abre el lanzador (hay que tener cuidado para no romper los combos Win+X) |
| Historial del portapapeles | ✅ | **Win+V** nativo (fija elementos, sincroniza opcional) + PowerToys **Advanced Paste** (pegar como texto plano/Markdown/JSON) [F7] | Mejor que el de Noctalia |
| Notificaciones / centro de control / OSD | ✅ | Nativo (Win+N, Win+A) | — |
| Bloqueo | ✅ | Win+L | — |
| Selector de color (hyprpicker, botón del Fifine) | ✅ | PowerToys **Color Picker** (Win+Shift+C) | — |
| Brillo de monitor externo (ddcutil) | ✅ | PowerToys **Power Display** (nuevo) [F7] o Twinkle Tray | — |
| Tema desde el fondo (Material You), modo oscuro | ✅/🟡 | W11: "elegir color de énfasis desde el fondo" + modo oscuro + PowerToys **Light Switch** (claro/oscuro por horario) [F7] | No re-tematiza terminal/btop/Qt como Noctalia |
| Fondos por monitor | ✅ | Nativo (clic derecho sobre el monitor en Personalización) | — |
| Cursor Bibata | ✅ | Bibata tiene versión para Windows (.inf) **(no verificado)** | — |

### 4.D Capturas: manuales, "inteligentes", auto-captura y cuadernillo

| Función | W11 | Herramienta | Cómo / qué cambia |
|---|---|---|---|
| Zona → **solo portapapeles**, 2 pasos (SUPER+SHIFT+S) | ✅ | **Win+Shift+S** (Recortes) nativo, o **ShareX v21.0.0** (03-07-2026) [F16] | Recortes: atajo → arrastrar → queda en el portapapeles (y, si lo activas, también se guarda en Imágenes\Capturas). **Tus 2 pasos se cumplen** |
| Zona → **carpeta elegida + portapapeles** (CTRL+SHIFT+S) y **elegir carpeta** (CTRL+SHIFT+D) | ✅ | **ShareX**: una tarea por atajo ("después de capturar: copiar imagen + guardar en…") con ruta configurable; o AHK: `DirSelect` guarda la carpeta en un .ini y otro atajo lanza Recortes, espera la imagen y la guarda con Python/Pillow `ImageGrab.grabclipboard()` | ShareX también hace **selección "inteligente"** (detecta ventanas y controles al pasar el cursor), **OCR** y anotaciones. Ojo: CTRL+SHIFT+S le quita "Guardar como" a las apps (lo mismo pasa hoy en Linux, GAPS §5) |
| Impr → editor (satty) | ✅ | ShareX (editor de anotaciones) o Recortes (editor + **acciones de texto/OCR**) | — |
| OCR de pantalla | ✅ (mejor) | PowerToys **Text Extractor** (Win+Shift+T) [F17] | En Linux tienes tesseract instalado pero sin atajo |
| **Auto-captura SUPER+ALT+S** (guarda solo si cambió la pantalla) | 🟡 portable | Tu `auto-captura.py` es Python puro (numpy + Pillow): **solo hay que cambiar la "capa de sistema"**: `grim -o monitor` → librería `mss`; `hyprctl activewindow` → `pywin32`/`GetForegroundWindow`; `notify-send` → toast de Windows; el PID en `/tmp` → `%TEMP%` | Algoritmo, `auto-captura.conf` y `auto-captura-tests.py` **se reutilizan tal cual**. ShareX tiene "Auto capture" por intervalo, pero **sin detección de cambios**: el tuyo es mejor |
| `video-a-capturas.sh`, SUPER+ALT+Y (YouTube), SUPER+ALT+A (curso entero → cuadernillo) | ✅ (con trabajo) | Mismos scripts Python + `yt-dlp.exe` + `ffmpeg.exe` + **Tesseract** (instalador UB Mannheim) [F18] + **Claude Code nativo de Windows** (`claude -p`) | Los `.sh` (cola, playlist) conviene reescribirlos en Python o PowerShell, **o correr todo el pipeline en WSL2** (§4.F), donde bash funciona tal cual |
| Barrita de progreso *layer-shell* en el monitor vertical | 🟡 | Ventana Tkinter/PyQt **siempre encima, sin foco y "click-through"** (`WS_EX_TRANSPARENT \| WS_EX_NOACTIVATE` vía ctypes) ubicada en la **ScreenPad** | En Windows no existe layer-shell; es el truco equivalente. La ScreenPad es **el lugar perfecto** para esa barra |
| Obsidian con bóveda "Vídeos" + Spaced Repetition | ✅ | Obsidian para Windows | Igual |

### 4.E Voz: dictado y lectura en voz alta

| Función | W11 | Herramienta | Cómo / valoración |
|---|---|---|---|
| **Dictado** (hyprwhspr, Whisper local, toggle es/en) | ✅ **mejor que hoy** | **Handy v0.9.7** (18-09-2026, MIT, `winget install cjpais.Handy`; Whisper Small/Medium/Turbo/Large con GPU o Parakeet V3) [F19] · **OpenWhispr** (MIT, Whisper/Parakeet local con **CUDA**, atajo global, atajo de "dictar y traducir") [F20] · **Win+H** nativo (dictado de Windows; necesita internet; español OK) [F21] | Con la RTX 3060 puedes usar **large-v3-turbo** en lugar de `small`: más preciso en español y más rápido que tu CPU actual. El Maono (receptor USB) funciona igual. **WhisperWriter está abandonado** (último release en enero de 2024) [F22]: descartado. Buzz v1.4.5 [F23] sirve para transcribir **archivos**, no para dictar. **Pendiente:** confirmar si Handy permite **dos atajos con idiomas distintos** (es/en) como tu Z/X **(no verificado)**; OpenWhispr sí tiene un atajo de traducción aparte |
| **Lectura SUPER+R** (selección → limpieza → voz natural, toggle) | ✅ con script propio | AHK + tus scripts: 1) AHK guarda `ClipboardAll`, manda Ctrl+C, `ClipWait(0.3)` (tus **300 ms**), 2) pasa el texto a **tu `limpiar-texto.py` y los mismos `sed`** (portados a Python), 3) voz con **edge-tts 7.2.8** (`pip install edge-tts`, mismas voces es-AR-Elena / es-MX-Jorge) [F24] o **Piper** (`piper1-gpl` v1.8.0, `pip install piper-tts`, voces es_AR-daniela-high de HF) [F25][F26], 4) reproducir con `ffplay`/`winsound`; apretar otra vez = `ProcessClose` | **Ventaja en Windows:** no hace falta ydotool: `SendInput` llega también a los *webviews* de VS Code (en Linux era el problema de wtype). Mantén la **exclusión de terminales** (Ctrl+C = cortar el proceso también en Windows Terminal). **Riesgo:** AHK sin permisos de administrador no puede mandar teclas a ventanas elevadas (UIPI) |
| Daemon de Piper (modelo en RAM) | ✅ | El mismo `piper-daemon.py`, cambiando el socket Unix por `localhost:puerto` o un *named pipe*, arrancado con el Programador de tareas | — |
| Selector de voz SUPER+ALT+R (GTK4) | 🟡 | AHK `Gui` (2 listas + barra de velocidad) que escribe `voz.conf` | Reescribir ~60 líneas |
| Alternativas listas sin programar | 🟡 | **Balabolka** (gratis, voces SAPI y lectura del portapapeles con atajo) **(sitio no verificado hoy)**; **Narrador** con voces naturales; "Leer en voz alta" de Edge; NaturalReader (pago) | Ninguna limpia el Markdown/código como tu `limpiar-texto.py`. Tu script es mejor para estudiar código |
| Chatterbox (máxima calidad, lento) | ✅ | Mismo venv con **PyTorch CUDA** en la 3060 | Pasaría de ~50 s por lectura en CPU a pocos segundos (estimación, **no medido**) |

### 4.F Video: descargar, doblar, mpv, sesión de curso

| Función | W11 | Herramienta | Cómo / valoración |
|---|---|---|---|
| `descargar` (yt-dlp, numerado, reanuda) | ✅/🟡 | **yt-dlp 2026.08.19** (`winget install yt-dlp`) [F27] + ffmpeg + aria2 | **Posible problema:** en Windows los navegadores Chromium cifran las cookies con "App-Bound Encryption", y `--cookies-from-browser` puede fallar con Brave abierto **(no verificado para Brave en 2026)**. Soluciones: cerrar Brave antes, exportar `cookies.txt` o descargar desde WSL2 con un archivo de cookies |
| **`doblar`** (Whisper → NLLB → edge-tts → ffmpeg) | ✅ **mucho más rápido** | Opción recomendada: **WSL2 (Ubuntu o Arch) + CUDA**. El driver NVIDIA de Windows expone CUDA dentro de WSL2 y no hay que instalar driver en Linux [F28][F29]. En el venv: `faster-whisper` + `ctranslate2` + `pip install nvidia-cublas-cu12 nvidia-cudnn-cu12==9.*` y exportar `LD_LIBRARY_PATH` (así lo documenta faster-whisper) [F30] | **Cambio en `doblar.py`:** la vía B hoy es `device="cpu"`; pasarla a `device="cuda", compute_type="int8_float16"` con modelo **large-v3-turbo**, y NLLB con `device="cuda"`. La vía A (whisper-cli por Vulkan) **no conviene en WSL2** (ahí Vulkan va por una capa de traducción). **Velocidad esperada:** el benchmark oficial transcribe 13 min de audio con large-v2 en ~1 min (RTX 3070 Ti de escritorio, fp16) y en ~16 s con `batch_size=8` [F30]; turbo es más liviano que large-v2. Para una **3060 Laptop**, estimo **3–8 min de transcripción por hora de video** (**estimación, no medida**), contra ~30 min por hora hoy en CPU. edge-tts sigue dependiendo de internet |
| `doblar` en Windows nativo | 🟡 | Python de Windows + las DLL de cuBLAS/cuDNN (p. ej. el paquete de *Purfview whisper-standalone-win*, que recomienda el README de faster-whisper) [F30][F31] | Funciona, pero el script bash `doblar` y `--seguir` habría que reescribirlos; en WSL2 corren tal cual |
| Dónde viven los videos | — | Guárdalos **dentro de WSL2** (ext4) mientras se procesan; `/mnt/c` es lento para E/S intensiva. Luego se ven desde Windows en `\\wsl$\...` | Es el detalle que más frustra en WSL2 |
| mpv de estudio (uosc, marcadores, velocidad, curso.lua, input.conf) | ✅ **casi copiar y pegar** | **mpv** (builds oficiales o **mpv.net v7.1.2**) [F32] | Copia `~/.config/mpv/` a `%APPDATA%\mpv\`: los scripts Lua y uosc funcionan en Windows. Cambian las rutas (`~/Imágenes/Capturas-mpv`) y `hwdec=auto-safe` usará D3D11/NVDEC. **Es de lo mejor que se porta** |
| Sesión de curso SUPER+C / SUPER+ALT+C | ✅ | AHK: `curso.ini` + `InputBox`/`Gui` de 4 campos; abrir en un escritorio "Estudio" + FancyZones (izquierda curso, derecha apuntes) o un **PowerToys Workspace** | De paso se arregla el bug actual (sintaxis vieja `hyprctl dispatch workspace`) |
| Pomodoro | ✅ | Reloj de Windows → **Sesiones de concentración**, o el botón de Stream Deck (plugin Pomodoro) | — |

### 4.G Apps y apps por defecto

| En la PC | W11 | Nota |
|---|---|---|
| Brave + PWA | ✅ | Idéntico (instalar como app; `--app=URL`) |
| kitty | 🟡 | kitty no existe para Windows → **Windows Terminal** o **WezTerm** [F33] |
| fish (cachyos-fish-config) | 🟡 | En WSL2 fish funciona igual. En Windows: **PowerShell 7 + Starship** (prompt) [F34]. Tus funciones fish no tienen equivalente directo, pero **casi no usas la terminal directamente** (doc 07: todo pasa por Claude Code) |
| Dolphin | 🟡 | Explorador de W11 (pestañas) o **Files** [F35] |
| Gwenview | ✅ | **ImageGlass 10.0.6** (05-09-2026) [F36] o **qView 7.1** [F37]; Fotos nativa |
| mpv | ✅ | §4.F |
| Obsidian, VS Code (Settings Sync), LibreOffice, KeePassXC, LocalSend, RustDesk, OBS, Claude Desktop | ✅ | Todas tienen versión Windows; VS Code se sincroniza solo con GitHub |
| Claude Code | ✅ | Instalador nativo de Windows (o dentro de WSL2) |
| btop | ✅ | Administrador de tareas (Ctrl+Shift+Esc), o btop dentro de WSL |
| arduino-cli + ESP32, Android Studio + adb | ✅ | En Windows los drivers USB-serie y adb andan mejor (los del fabricante) |
| gnome-text-editor | ✅ | Bloc de notas (con pestañas y Markdown) |
| Apps por defecto (`mimeapps.list`) | ✅ | Configuración → Aplicaciones → Aplicaciones predeterminadas (por extensión). `.md` → Obsidian o VS Code |

### 4.H Sistema: backups, snapshots, Drive, servicios

| Función | W11 | Herramienta | Nota |
|---|---|---|---|
| Backup restic diario a disco externo | ✅ | **restic 0.19.1** tiene binario para Windows y soporta **VSS** (`--use-fs-snapshot`, copia archivos abiertos) [F38]; programado con el Programador de tareas, o **Backrest** (interfaz web para restic) [F39] | **Mismo repositorio** que la PC (restic distingue por hostname). Excluir la unidad de Google Drive |
| **Snapshots btrfs + snapper + Limine** (volver atrás tras una actualización) | 🟡/❌ | Puntos de restauración del sistema + Copias de seguridad de Windows + historial de archivos | **No hay equivalente real.** Un punto de restauración no es un snapshot atómico del sistema. Lo más parecido: una imagen completa del disco con otra herramienta antes de cada actualización grande |
| Google Drive montado (rclone) | ✅ | **Google Drive para escritorio** (oficial, unidad G:, archivos en *streaming*) — en Windows es **mejor** que rclone; o **rclone v1.75.1** + **WinFsp** [F40][F41] | Recuerda el problema del *client_id* compartido de rclone (README) si sigues con rclone |
| Servicios de usuario (systemd --user) | ✅ | Programador de tareas ("al iniciar sesión") o accesos directos en `shell:startup` | El equivalente mental a `systemctl --user enable` |
| Restaurar ventanas de Brave | 🟡 | §4.A | — |
| Tema/estética (blur, bordes, animaciones) | 🟡 | Mica/Acrylic nativos, bordes redondeados, modo oscuro | Nunca vas a tener el nivel de control de Hyprland; es la mayor pérdida "estética" |

### 4.I Periféricos

| Aparato | W11 | Linux (CachyOS en la Zenbook) |
|---|---|---|
| **Stream Deck XL** | ✅ **mejor**: app oficial de Elgato (plugins de la tienda, multiacciones, perfiles por app) [F42]. Los botones se reescriben para lanzar tus `.ahk` / URLs | ✅ **OpenDeck 2.14** (lo que ya usas; soporte nativo del XL). Elgato **nunca** sacó cliente oficial para Linux [F43] |
| Mirabox HSV293S / Fifine D6 | 🟡 Apps propias de cada marca **(no verificado)**; también **OpenDeck para Windows** (hay `.exe`/`.msi` de la 2.14) [F44], pero el plugin `akp153` declara Windows como "*zero effort, no tests*" [F45] | ✅ OpenDeck + plugins (tu guía `portabilidad-laptops.md`) |
| **MX Master 4** | ✅ **mejor**: Logi Options+ (háptica, Actions Ring, botones por app, Smart Actions) [F46]. Pulgar → Win+Shift+S / atajo de ShareX, igual que tu M720 | 🟡 **Solaar 1.1.20** y **logiops 0.3.5** lo reconocen (botones, DPI, SmartShift), pero hay issues abiertos en 2026: con receptor **Bolt** falla al iniciar y el scroll hi-res va demasiado rápido; la **háptica** está en un PR sin fusionar [F47][F48]. Sin Actions Ring |
| K380 | ✅ | ✅ |
| Maono DM40 | ✅ (micrófono USB estándar) | ✅ (ya lo usas) |
| **Lápiz ASUS** (MPP) | ✅ Windows Ink, presión, rechazo de palma, escritura a mano de ScreenXpert | 🟡 Normalmente funciona como digitalizador HID (Xournal++) **(no verificado en el UX582)** |

### 4.J Específico de la Zenbook Pro Duo 15 (UX582)

| Tema | Windows 11 | CachyOS (dual boot) |
|---|---|---|
| **ScreenPad Plus como monitor** | ✅ Segundo monitor extendido (3840x1100) con táctil propio; ScreenXpert agrega lanzador, "Task Group", pasar ventanas de una pantalla a otra, panel de control para apps creativas y escritura a mano [F3] | 🟡 Aparece como **segundo panel interno**; Hyprland lo maneja como otro monitor (`monitor = eDP-2,...` o como se llame). **Brillo:** el kernel mainline ya trae el backlight `asus_screenpad` en `asus-wmi` (lo verifiqué en el código fuente actual) [F49], y un usuario lo confirma de forma nativa con el kernel 6.18.26 en un UX482 [F50]. Antes hacía falta el módulo DKMS de Plippo [F51]. Hay reportes (en otro modelo Duo con NVIDIA) de la ScreenPad **en negro tras instalar el driver propietario**, que se arreglaron con la configuración NVIDIA/KMS correcta [F52] |
| Táctil de cada pantalla | 🟡 **El problema conocido:** después de actualizaciones de W11, el táctil de la ScreenPad **controla la pantalla principal**. ASUS tiene una FAQ: actualizar el driver *ScreenXpert Interface* ≥ 3.0.2.0 y correr *ScreenPad Optimizer* ≥ 1.2.3.0; además, "Configuración de Tablet PC → Configurar" para reasignar el táctil [F3][F4][F53] | 🟡 Hay que mapear cada digitalizador a su salida (en Hyprland: `device { name = ...; output = ... }`) |
| Uso ideal de la ScreenPad | Barrita de progreso de la auto-captura, WhatsApp/Telegram/Drive (lo que hoy va en el HP vertical), la barra YASB, un "Stream Deck táctil" (ScreenXpert App Navigator o **Virtual Stream Deck** de Elgato **(no verificado)**), mpv en PiP | Lo mismo con Hyprland: ws 6-10 = ScreenPad → **tu modelo de "escritorio virtual de 2 monitores" funciona casi sin cambios** (solo cambian los nombres de MONITOR1/2 y la resolución/escala) |
| Brillo de la ScreenPad / teclas especiales | ✅ MyASUS / ScreenXpert; **G-Helper** (alternativa liviana a Armoury Crate, dice soportar Zenbook) trae atajos de brillo de la ScreenPad [F54] | ✅ `brightnessctl -d asus_screenpad`; algunas teclas Fn especiales necesitaban el parche de `asus-nb-wmi` [F50] |
| GPU híbrida | ✅ Optimus automático; Panel de control de NVIDIA por app | 🟡 **nvidia-open** (Ampere lo soporta) + Hyprland en la iGPU (`AQ_DRM_DEVICES` con la Intel primero) + la NVIDIA para CUDA/juegos (`prime-run`). **supergfxctl 5.2.7** existe para cambiar de modo [F55], pero asus-linux se centra en ROG/TUF [F56] |
| Batería (límite de carga 60/80 %), ventiladores | ✅ MyASUS (Battery Care, modos de ventilador) o G-Helper | 🟡 El límite de carga va por `asus-wmi` (`charge_control_end_threshold`) **(no verificado en este modelo)**; perfiles con power-profiles-daemon |
| Audio | ✅ | ❓ **No verificado** en el UX582ZM (12ª gen suele usar firmware SOF; los hackintosh del UX582 mencionan el códec ALC294) |
| Suspensión | ✅ (Modern Standby, a veces gasta batería en la mochila) | ❓ **No verificado** |
| OLED | ASUS OLED Care (desplazamiento de píxeles, barra de tareas oculta) | Barra auto-oculta (ya la tienes), fondos oscuros |

---

## 5. Qué NO conviene intentar replicar en Windows (y por qué)

1. **Hyprland pixel por pixel** (blur, animaciones, bordes con gradiente, *swallow*, config programable en Lua). El compositor de Windows (DWM) no se reemplaza; los gestores de mosaico **mueven ventanas desde afuera**, así que siempre habrá parpadeos y ventanas rebeldes. Mejor aceptar la estética de W11.
2. **ydotool, wtype, wl-clipboard, layer-shell, `hyprctl -j`.** Son "pegamento Wayland" que en Windows no hace falta: `SendInput`, el portapapeles de Win32 y las ventanas *topmost* ya existen. **Porta la lógica, no las herramientas.**
3. **snapper/btrfs como "red de seguridad".** No existe; simularlo con terceros cuesta mucho y protege poco. Si la necesitas, es un argumento a favor del dual boot.
4. **rclone mount de Drive**: en Windows, Google Drive para escritorio es más estable (y no depende de WinFsp ni del *client_id*).
5. **La lógica "ws i + ws i+5" con GlazeWM *y además* escritorios nativos.** Son dos modelos de escritorio que se pisan. Elige uno (recomendado: nativos + AHK).
6. **Debloaters/"optimizadores" de Windows de origen dudoso.** Rompen las actualizaciones, ScreenXpert o MyASUS justo en este modelo, que depende de servicios de ASUS. Ajusta a mano (§7).
7. **OpenDeck en Windows con los 3 aparatos.** Posible, pero los plugins Mirabox/Fifine no están probados en Windows. En Windows usa la app de Elgato para el XL; los otros dos, solo si hace falta.

---

## 6. Las tres alternativas globales

### 6.1 (a) Windows 11 nativo + herramientas

**Stack:** PowerToys (Command Palette, FancyZones, Workspaces, Text Extractor, Advanced Paste, Keyboard Manager) · AutoHotkey v2 (atajos + apps web + SUPER+R + sesión de curso) · escritorios nativos (+ GlazeWM opcional) · YASB o barra nativa · Handy u OpenWhispr (dictado con CUDA) · ShareX · mpv con tu config · Obsidian · Google Drive para escritorio · restic/Backrest · Elgato Stream Deck · Logi Options+ · MyASUS/ScreenXpert.

- ✅ Hardware al 100 % (ScreenPad, lápiz, Options+, Stream Deck, Optimus). Todo con soporte del fabricante.
- 🟡 Hay que reescribir: `binds.lua` → AHK (1 tarde), SUPER+R (1 tarde), auto-captura/cuadernillo (portar la capa de sistema: 1–2 días), `doblar` (mejor en WSL2).
- ❌ Sin snapshots reales; actualizaciones que a veces rompen ScreenXpert o el táctil; menos control.

### 6.2 (b) W11 + WSL2 para lo "Linux"

Igual que (a), pero **`descargar`, `doblar`, `video-a-capturas`, `playlist-a-apuntes` y el cuadernillo corren en WSL2** (Arch o Ubuntu) con **CUDA de la RTX 3060** y fish. Lo gráfico (atajos, capturas en vivo, lectura, barrita) queda en Windows.
- ✅ Reutilizas tus scripts bash/Python casi tal cual; el doblaje usa CUDA sin instalar drivers en Linux [F28][F29].
- 🟡 WSL2 **no ve tu escritorio**: nada de `grim`/`hyprctl`. La auto-captura en vivo y SUPER+R tienen que ser de Windows. Hay que cuidar dónde viven los archivos (`/mnt/c` es lento). Límite de RAM/CPU de WSL en `.wslconfig` [F57].
- Es la mejor opción **si decides quedarte solo con Windows**.

### 6.3 (c) Dual boot: CachyOS en la Zenbook

- ✅ **Tu config viaja casi entera**: el paquete `~/migracion-cachyos` ya prevé el ajuste a laptop. Con la ScreenPad como MONITOR2, tu modelo de 2 monitores y 5 escritorios vuelve a tener sentido (en la ThinkPad/Surface había que inventar el "voltear").
- ✅ **La RTX 3060 le da CUDA nativo a `doblar`, al dictado (hyprwhspr con backend CUDA o `large-v3-turbo`) y a Chatterbox**, sin la capa de WSL.
- ✅ snapper + Limine, sin telemetría, control total.
- 🟡 **Pierdes en Linux:** app oficial de Stream Deck (te quedas con OpenDeck, que ya dominas), Logi Options+ (Solaar/logiops cubren lo básico del MX Master 4, sin háptica ni Actions Ring), ScreenXpert (la ScreenPad queda como "un monitor más"), MyASUS, y quizás detalles del lápiz, el audio y la suspensión **(no verificados)**.
- 🟡 **Riesgos de instalación en este equipo:**
  1. **BitLocker/cifrado de dispositivo**: W11 lo activa solo en muchos equipos nuevos. **Guarda la clave de recuperación** (cuenta Microsoft) antes de achicar la partición o tocar el arranque.
  2. **Secure Boot**: CachyOS + Limine necesita firmar con `sbctl` o desactivar Secure Boot; desactivarlo puede hacer que BitLocker pida la clave **(detalles no verificados, ver wiki de CachyOS)** [F58].
  3. Desactivar **Inicio rápido** de Windows (deja el NTFS "sucio" para Linux).
  4. Reparto sugerido del SSD de 1 TB: ~350 GB Windows · ~550 GB CachyOS (btrfs) · resto libre. Los videos de cursos, en el disco externo como hoy.
- **Checklist obligatorio con un USB en vivo de CachyOS antes de instalar** (15 minutos): ¿se ven **las dos** pantallas? ¿el táctil de cada una va a su pantalla? ¿sube y baja el brillo de la ScreenPad (`ls /sys/class/backlight`)? ¿suena el audio y anda el micrófono interno? ¿Wi-Fi y Bluetooth (K380/MX Master 4)? ¿`nvidia-smi` ve la 3060? ¿suspende y despierta? ¿el lápiz dibuja en Xournal++?

### 6.4 Comparación rápida

| Criterio | (a) W11 | (b) W11+WSL2 | (c) Dual boot |
|---|---|---|---|
| Esfuerzo de migrar tu config | Alto (reescribir) | Medio-alto | **Bajo** (ya documentado) |
| Flujo de estudio (auto-captura, SUPER+R, doblar, mpv) | 🟡 portado | 🟡/✅ | ✅ tal cual |
| Doblaje con la RTX 3060 | ✅ (nativo, más difícil) | ✅ | ✅ |
| ScreenPad / lápiz / ASUS | ✅ | ✅ | 🟡 (probar) |
| Stream Deck / MX Master 4 | ✅ mejor | ✅ mejor | 🟡 (OpenDeck / Solaar) |
| Snapshots / control / privacidad | ❌/🟡 | ❌/🟡 | ✅ |
| Mantenimiento | Actualizaciones de W11 | + WSL | Dos sistemas |

### 6.5 Recomendación

**Dual boot con CachyOS como sistema principal de estudio, y W11 bien configurado como respaldo**, en este orden:

1. **Primero W11 "domado" (1 tarde, sin riesgo):** privacidad y actualizaciones (§7), PowerToys, AHK con tus atajos principales (escritorios, apps web, SUPER+R), Handy u OpenWhispr con turbo en CUDA, ShareX, mpv con tu config, Google Drive para escritorio. Así, si Linux falla en algo, la laptop ya es útil.
2. **Probar CachyOS en vivo** con el checklist de §6.3. Si la ScreenPad (imagen + táctil) y el audio funcionan → **instalar en dual boot** y aplicar `~/migracion-cachyos` con MONITOR1 = OLED y MONITOR2 = ScreenPad; en `doblar.py`, usar CUDA. Si algo crítico falla → quedarse con **(b) W11 + WSL2** para el doblaje y el cuadernillo.
3. **Reparto:** estudiar, programar y doblar en CachyOS; Windows para lo que exija su hardware o sus apps (por ejemplo, editar perfiles del Stream Deck con la app oficial, usar el lápiz a fondo o ScreenXpert).

**El porqué (lo que quieres aprender):** tu ventaja no está en Hyprland como programa, sino en ~45 scripts que dependen de **interfaces de Linux/Wayland** (`hyprctl`, `grim`, `wl-paste`, `/dev/uinput`, systemd). Migrar a Windows es "portar a otra ABI": la lógica (numpy, Whisper, NLLB, `limpiar-texto.py`, el prompt del cuadernillo) se conserva, pero hay que reescribir la capa que habla con el sistema. En Linux esa capa ya existe y funciona. Por eso el costo real de (a) es tu tiempo, y el de (c) es el riesgo de hardware. Ese riesgo se **mide en 15 minutos con un USB en vivo**; el tiempo de reescribir no se recupera.

---

## 7. Riesgos típicos de W11 y cómo mitigarlos (sin software dudoso)

| Problema | Mitigación (solo opciones oficiales) |
|---|---|
| Actualizaciones que reinician o rompen cosas (ScreenXpert/táctil) | Configuración → Windows Update: **Horas activas**, **Pausar** (hasta 5 semanas), desactivar "Obtener las actualizaciones más recientes en cuanto estén disponibles" y "Reiniciar lo antes posible" [F59]. Antes de una actualización grande: punto de restauración + backup. **Drivers de ASUS solo desde MyASUS** o la página de soporte del modelo. Después de actualizar: si el táctil se cruzó, FAQ de ASUS [F53] |
| Telemetría y "sugerencias" | Privacidad y seguridad → Diagnóstico: **solo datos obligatorios**, sin experiencias personalizadas, sin ID de publicidad, sin historial de actividad; Inicio: sin recomendaciones ni anuncios; Búsqueda: sin contenido web [F60]. (En W11 Home no existe `gpedit`; con lo anterior alcanza) |
| Rendimiento y batería | Modo de energía por perfil (MyASUS/G-Helper), revisar **Aplicaciones de inicio** (Administrador de tareas), Optimus elige la GPU sola (forzar la NVIDIA solo en apps pesadas), no desactivar Defender ni la Integridad de memoria |
| Programas que se pelean (Options+, Stream Deck, AHK, GlazeWM, ScreenXpert) | Instalar de a uno y probar; AHK **sin administrador** salvo que haga falta; si GlazeWM se pelea con la ScreenPad, dejarla como monitor sin mosaico o usar solo FancyZones |
| OneDrive / cuenta Microsoft | Desactivar la copia de seguridad de carpetas de OneDrive si usas Google Drive (evita duplicar Documentos/Imágenes) |
| OLED | Barra auto-oculta, modo oscuro, ASUS OLED Care |

---

## 8. Mapa rápido "atajo de la PC → Windows" (para tener a mano)

| PC | Windows propuesto |
|---|---|
| SUPER+1..5 / CTRL+1..5 / CTRL+←/→ | AHK + VD.ah2 (Win+1..5, Win+Ctrl+1..5) / nativo Win+Ctrl+←/→ |
| SUPER+Tab | AHK "ciclar ventanas del escritorio" |
| SUPER+Q / F / D / ALT+Espacio | AHK o GlazeWM |
| SUPER+Enter / E / W / N / G | AHK (Windows Terminal / Explorador / Brave / Obsidian / VS Code) |
| SUPER+ALT+Q/W/T/F/I/D, SUPER+T | AHK `AppWeb()` |
| SUPER (solo) / SUPER+. / SUPER+V / SUPER+L | Command Palette / Win+. / Win+V / Win+L |
| Impr / SUPER+Impr / SUPER+SHIFT+S / CTRL+SHIFT+S / CTRL+SHIFT+D | ShareX o Recortes / Win+Impr / Win+Shift+S / ShareX tarea "guardar+copiar" / AHK `DirSelect` |
| SUPER+ALT+S / Y / A | AHK → `auto-captura.py` portado / pipeline en WSL2 |
| SUPER+R / SUPER+ALT+R | AHK + Python (edge-tts / Piper) / AHK Gui |
| SUPER+ALT+Z / X | Handy u OpenWhispr (atajos configurables) · Win+H nativo |
| SUPER+C / SUPER+ALT+C | AHK + `curso.ini` (+ PowerToys Workspace) |
| CTRL+SHIFT+Esc / CTRL+ALT+Esc | Nativo / AHK `ProcessClose` |
| Pulgar del mouse / clic de la rueda | Logi Options+ → Win+Shift+S / atajo de ShareX |

---

## 9. Lo que NO pude verificar

- Si el **UX582ZM tiene MUX switch** (no encontré fuente; supongo Optimus sin MUX).
- **Audio, suspensión, lápiz y teclas Fn** del UX582ZM en Linux (no hay reportes específicos de este modelo; los repos encontrados son de UX482/UX8406 y de hackintosh del UX582).
- **Qué GPU maneja cada pantalla** del UX582ZM en Linux (importa para Hyprland/nvidia).
- Qué número de kernel incorporó exactamente el backlight `asus_screenpad` (el código está en mainline; hay un reporte de que funciona en 6.18.26).
- Si **Handy** admite dos atajos con idiomas distintos (es/en).
- Si `--cookies-from-browser brave` de yt-dlp falla hoy en Windows por App-Bound Encryption.
- La sintaxis de **lista de comandos por atajo** en GlazeWM v3.10 y si trae scratchpad.
- Si Elgato ofrece hoy un **"Virtual Stream Deck"** usable en la ScreenPad, y cuáles son las apps oficiales de Mirabox/Fifine para Windows.
- La compatibilidad real de ScreenXpert con GlazeWM/komorebi.
- **Tiempos de doblaje en la 3060 Laptop** (§4.F es una estimación a partir del benchmark de una 3070 Ti de escritorio). Una búsqueda devolvió "~2× tiempo real en una RTX 3060", pero no coincide con el benchmark oficial de faster-whisper; la descarto hasta medirlo.
- Sitios que no respondieron hoy (getsharex.com, mpv.io, obsidian.md, balabolka): son proyectos conocidos, pero no confirmé la página.

---

## 10. Fuentes

- [F1] ASUS ZenBook Pro Duo 15 UX582ZM (i7-12700H, RTX 3060) — https://www.amazon.com/ASUS-i7-12700H-ScreenPad-Celestial-UX582ZM-AS76T/dp/B09TDKV65Z · Best Buy UX582ZM-XS96T — https://www.bestbuy.com/site/asus-zenbook-pro-duo-15-oled-ux582-15-6-touch-screen-laptop-intel-core-i9-32gb-memory-nvidia-geforce-rtx-3060-1tb-ssd/6513492.p?skuId=6513492
- [F2] ASUS, ficha del UX582 (12ª gen) — https://www.asus.com/us/laptops/for-home/zenbook/zenbook-pro-duo-15-oled-ux582-12th-gen-intel/ · especificaciones — https://www.asus.com/us/laptops/for-creators/zenbook/zenbook-pro-duo-15-oled-ux582/techspec/
- [F3] ASUS FAQ ScreenXpert — https://www.asus.com/us/support/faq/1050477/
- [F4] ASUS FAQ "ScreenPad Plus no funciona bien" — https://www.asus.com/us/support/faq/1041420/
- [F5] GlazeWM — https://github.com/glzr-io/glazewm · https://glazewm.com
- [F6] komorebi (licencia en el README) — https://github.com/LGUG2Z/komorebi · docs https://lgug2z.github.io/komorebi/ · whkd https://github.com/LGUG2Z/whkd
- [F7] PowerToys, lista de utilidades (Grab And Move, Power Display, Light Switch, Window Hopper, etc.) — https://learn.microsoft.com/en-us/windows/powertoys/ · FancyZones https://learn.microsoft.com/en-us/windows/powertoys/fancyzones
- [F8] AutoHotkey v2 — https://www.autohotkey.com/docs/v2/ · https://github.com/AutoHotkey/AutoHotkey
- [F9] VD.ah2 (escritorios virtuales en W11 con AHK v2) — https://github.com/Viqsi/VD.ah2 · VirtualDesktopAccessor — https://github.com/Ciantic/VirtualDesktopAccessor · kit AHK — https://github.com/GigaFable/autohotkey-virtual-desktop-kit
- [F10] PowerToys Workspaces — https://learn.microsoft.com/en-us/windows/powertoys/workspaces
- [F11] PowerToys Keyboard Manager — https://learn.microsoft.com/en-us/windows/powertoys/keyboard-manager
- [F12] YASB — https://github.com/amnweb/yasb
- [F13] Zebar — https://github.com/glzr-io/zebar
- [F14] Command Palette — https://learn.microsoft.com/en-us/windows/powertoys/command-palette/overview
- [F15] Flow Launcher — https://github.com/Flow-Launcher/Flow.Launcher
- [F16] ShareX — https://github.com/ShareX/ShareX
- [F17] Text Extractor — https://learn.microsoft.com/en-us/windows/powertoys/text-extractor · Advanced Paste — https://learn.microsoft.com/en-us/windows/powertoys/advanced-paste
- [F18] Tesseract para Windows (UB Mannheim) — https://github.com/UB-Mannheim/tesseract/wiki
- [F19] Handy — https://github.com/cjpais/Handy
- [F20] OpenWhispr — https://github.com/OpenWhispr/openwhispr
- [F21] Dictado de Windows (Win+H) — https://support.microsoft.com/en-us/windows/use-voice-typing-to-talk-instead-of-type-on-your-pc-fec94565-c4bd-329d-e59a-af033fa5689f
- [F22] WhisperWriter (último release 01-2024) — https://github.com/savbell/whisper-writer
- [F23] Buzz — https://github.com/chidiwilliams/buzz
- [F24] edge-tts — https://github.com/rany2/edge-tts
- [F25] Piper (continuación oficial, piper1-gpl) — https://github.com/OHF-Voice/piper1-gpl
- [F26] Voces Piper — https://huggingface.co/rhasspy/piper-voices
- [F27] yt-dlp — https://github.com/yt-dlp/yt-dlp
- [F28] CUDA en WSL (Microsoft) — https://learn.microsoft.com/en-us/windows/ai/directml/gpu-cuda-in-wsl · https://learn.microsoft.com/en-us/windows/wsl/tutorials/gpu-compute
- [F29] Guía de CUDA en WSL (NVIDIA) — https://docs.nvidia.com/cuda/wsl-user-guide/index.html
- [F30] faster-whisper (requisitos de GPU y benchmark) — https://github.com/SYSTRAN/faster-whisper
- [F31] Purfview whisper-standalone-win (librerías CUDA para Windows) — https://github.com/Purfview/whisper-standalone-win
- [F32] mpv.net — https://github.com/mpvnet-player/mpv.net · mpv — https://mpv.io/installation/
- [F33] WezTerm — https://wezterm.org
- [F34] Starship — https://starship.rs
- [F35] Files — https://github.com/files-community/Files
- [F36] ImageGlass — https://github.com/d2phap/ImageGlass
- [F37] qView — https://github.com/jurplel/qView
- [F38] restic (backup; `--use-fs-snapshot` en Windows) — https://restic.readthedocs.io/en/stable/040_backup.html
- [F39] Backrest — https://github.com/garethgeorge/backrest
- [F40] rclone mount — https://rclone.org/commands/rclone_mount/
- [F41] WinFsp — https://winfsp.dev
- [F42] Descargas de Elgato — https://www.elgato.com/us/en/s/downloads
- [F43] Stream Deck en Linux (sin cliente oficial) — https://cyberpanel.net/blog/stream-deck-linux · https://github.com/streamdeck-linux-gui/streamdeck-linux-gui
- [F44] OpenDeck (releases con .exe/.msi) — https://github.com/nekename/OpenDeck/releases
- [F45] opendeck-akp153 (soporte de plataformas en el README) — https://github.com/4ndv/opendeck-akp153
- [F46] Logi Options+ — https://www.logitech.com/en-us/software/logi-options-plus.html
- [F47] Issues del MX Master 4 en Solaar — https://github.com/pwr-Solaar/Solaar/issues/3290 · https://github.com/pwr-Solaar/Solaar/issues/3264
- [F48] Issues del MX Master 4 en logiops — https://github.com/PixlOne/logiops/issues/564 · https://github.com/PixlOne/logiops/issues/565 · PR de háptica https://github.com/PixlOne/logiops/pull/524
- [F49] Kernel Linux, `asus-wmi.c` (backlight de la ScreenPad) — https://github.com/torvalds/linux/blob/master/drivers/platform/x86/asus-wmi.c
- [F50] "ScreenPad soportado upstream en 6.18.26" (UX482) — https://github.com/Plippo/asus-wmi-screenpad/issues/72
- [F51] asus-wmi-screenpad (DKMS) — https://github.com/Plippo/asus-wmi-screenpad
- [F52] ScreenPad en negro tras instalar NVIDIA en Hyprland (Zephyrus Duo) — https://forum.garudalinux.org/t/asus-screenpad-worked-upon-first-boot-of-live-garuda-usb-stick-but-not-after-installation/42372 · Hyprland y portátiles Duo — https://github.com/hyprwm/Hyprland/issues/1587 · https://github.com/laithm/zenbook-duo-hyprland
- [F53] Hilo de problemas de la ScreenPad Plus (LTT) — https://linustechtips.com/topic/1303328-asus-zenbook-duo-screenpad-plus-problems/
- [F54] G-Helper — https://github.com/seerge/g-helper
- [F55] supergfxctl / asusctl — https://gitlab.com/asus-linux/supergfxctl · https://gitlab.com/asus-linux/asusctl
- [F56] asus-linux.org — https://asus-linux.org/ · Arch Wiki, NVIDIA Optimus — https://wiki.archlinux.org/title/NVIDIA_Optimus
- [F57] Configuración de WSL (`.wslconfig`) — https://learn.microsoft.com/en-us/windows/wsl/wsl-config · instalación https://learn.microsoft.com/en-us/windows/wsl/install
- [F58] Wiki de CachyOS — https://wiki.cachyos.org/
- [F59] Administrar actualizaciones en Windows — https://support.microsoft.com/en-us/windows/manage-updates-in-windows-643e9ea7-3cf6-7da6-a25c-95d4f7f099fe
- [F60] Diagnóstico y privacidad en Windows — https://support.microsoft.com/en-us/windows/diagnostics-feedback-and-privacy-in-windows-28808a2b-a31b-dd73-dcd3-4559a5199319
- Documentación local usada: `~/migracion-cachyos/{README,00-RESUMEN}.md`, `docs/01–07`, `docs/GAPS.md`, `~/Documentos/StreamDeck/docs/portabilidad-laptops.md`, `~/Documentos/Guia-Auto-captura-de-cursos.md`, `~/Documentos/aprender/funciones.md`, `~/.config/hypr/config/binds.lua`, `systemctl --user`.

---

# Parte B — Portabilidad de los scripts propios

## 0. Resumen en 30 segundos

- **El “cerebro” ya es portable.** La parte difícil (detector de cambios de `auto-captura.py`, `cuadernillo.py`, `resumen-corto.py`, `tarjetas.py`, `panel-cursos.py`, `capturas-*.py`, `doblar.py`) es **Python + numpy + PIL + ffmpeg/ffprobe + tesseract + `claude -p`**. Todo eso existe en Windows. Hacen falta **unos 6 arreglos chicos** (codificación, una ruta con `\`, `~/Vídeos`, `os.nice`, `pgrep`, `fcntl`).
- **Lo que atás al Linux es la “cáscara”:** bash + `flock`/`setsid`/`nice`/`ionice` (orquestación y cola), `grim` (captura en vivo), `hyprctl` (monitor y ventana activa), `notify-send`, `zenity`, `wl-paste`/`wl-copy`/`ydotool`/`wtype`, la barrita GTK4 + layer-shell y el socket Unix del daemon de Piper.
- **Recomendación: una migración híbrida por etapas.**
  1. **Etapa 1 (un fin de semana):** el motor por lotes corre en **WSL2 sin cambios** (bash tal cual, CUDA en la RTX 3060) y guarda los datos **en NTFS** (`C:\Cursos`), para que Obsidian y la captura en vivo trabajen sobre los mismos archivos. La UI se hace **nativa**: barrita en la ScreenPad Plus (tkinter), captura en vivo (`mss`/`windows-capture`), atajos con AutoHotkey v2 o el Stream Deck, y notificaciones toast. El único “cable” entre los dos mundos es el **archivo de progreso**, y ese diseño ya existe.
  2. **Etapa 2 (cuando moleste o sobre tiempo):** pasar los ~550 renglones de bash a Python con una capa `plataforma.py`. Así queda **un solo código** que corre nativo en Windows **y** en CachyOS, y WSL deja de hacer falta.
- **Esfuerzo:** la Etapa 1 son unas **20–30 h**. Llegar a todo multiplataforma son **45–70 h** en total (la Etapa 2 suma unas 25–40 h).
- **Riesgos principales:**
  - **OneDrive** puede “adueñarse” de `Videos`/`Documentos`: 16 000 capturas sincronizándose.
  - **Defender** escanea cada `.webp`.
  - El PC **suspende** en medio de una playlist.
  - **Cookies de Brave/Chrome en Windows** con yt-dlp (cifrado “app-bound”).
  - El texto se escribe en **cp1252** en vez de UTF-8, lo que rompe los prompts a Claude y los logs con emojis.
  - Los procesos de **WSL** se mueren cuando se cierra la sesión.

---

## 1. Inventario y dependencias exactas por script

Leyenda: **WSL2** = ¿corre en WSL2 sin tocarlo? · **Nativo** = qué hay que cambiar para Windows sin WSL · **h** = horas estimadas para dejarlo nativo (entre paréntesis, horas para dejarlo andando en WSL2).

### 1.1 Sistema de cursos: núcleo en Python (el valor está acá)

| Script | Depende de (Linux/Wayland en **negrita**) | WSL2 | Nativo Windows: qué cambiar | h nativo (WSL) |
|---|---|---|---|---|
| `auto-captura.py` **modo video** (`--video`) | numpy, PIL (WebP lossless), `ffprobe`, `ffmpeg` (pipe `rawvideo` por stdout), `progreso.reportar` (escribe un archivo), `open(CONF)` **sin `encoding`** | ✅ tal cual | Nada estructural. El pipe binario de ffmpeg anda igual en Windows. Hay que fijar la codificación (ver §4.4). | 0,5 (0) |
| `auto-captura.py` **modo vivo** (`--monitor`) | **`grim -t ppm -o DP-3`** (captura Wayland por conector), **`signal.SIGTERM`** para cortar y guardar el último frame | ❌ (en WSL no se ve la pantalla de Windows) | Cambiar `grim` por **`mss`** (GDI, trivial) o **`windows-capture`/`dxcam`** (API moderna, más rápida; `windows-capture` además puede capturar **una ventana** aunque esté tapada). **Ojo con SIGTERM:** en Windows, `kill`/`TerminateProcess` **no ejecuta el handler**, así que se perdería el `det.cerrar()` (el último frame) y el `.cantidad`. Hay que cortar con un **archivo “stop”**, un evento con nombre o `CTRL_BREAK_EVENT` (`CREATE_NEW_PROCESS_GROUP`). También hay que llamar a `SetProcessDpiAwareness(2)`, porque el 4K usa escala de ~250 % y sin eso las coordenadas mienten. | 4–6 |
| `auto-captura-toggle.sh` (SUPER+ALT+S) | bash, **`hyprctl monitors -j`** (monitor con foco), **`hyprctl activewindow -j`** (título), `kill`, pidfile en `/tmp`, **`notify-send`** | ❌ | Reescribir en Python y llamarlo desde AHK v2 o el Stream Deck. `GetForegroundWindow` + `MonitorFromWindow` + `GetWindowTextW` (ctypes o `pywin32`) dan el monitor y el título. PID en `%LOCALAPPDATA%\auto-captura\`. Toast con `win11toast`. | 2–3 |
| `cuadernillo.py` | numpy, PIL, `ffmpeg` (saca subtítulos embebidos), **`tesseract`** (OCR, en hilos), **`claude -p --output-format json --tools ""`**, `ruta_claude()` busca `~/.local/bin/claude`, **`subprocess(..., text=True)` sin `encoding`** (4 lugares) | ✅ tal cual | Tesseract (instalador UB-Mannheim, **agregarlo al PATH** y marcar los paquetes `spa`+`eng`). `shutil.which("claude")` encuentra `claude.exe`. **Obligatorio:** UTF-8 (§4.4). Si no, `input=prompt` se codifica en cp1252 y **revienta con emojis o caracteres raros** en los subtítulos. | 1–2 (0) |
| `resumen-corto.py` | `claude -p` (vía `cuadernillo.ruta_claude`), `text=True` sin encoding | ✅ | Igual que el anterior (UTF-8). | 0,5 (0) |
| `tarjetas.py` | Python puro (parser copiado de obsidian-spaced-repetition, `unicodedata`, `hashlib`) | ✅ | Nada. Si se escribe en Windows, conviene `newline="\n"` para que el `.md` no cambie de CRLF a LF según la máquina (Obsidian acepta los dos). | 0,5 (0) |
| `panel-cursos.py` | Python puro. Por defecto **`--base ~/Vídeos`**. **`os.path.relpath`** para armar links Markdown | ✅ | **Bug real en Windows:** `relpath` devuelve `Curso\capturas\...` con **barras invertidas**, lo que rompe los links de Obsidian y el “recordar marcas” (usa esa ruta como clave). Arreglo: `.replace(os.sep, "/")`. Además, `~/Vídeos` no existe en Windows (la carpeta real es `C:\Users\<u>\Videos`, **sin tilde**; “Vídeos” es solo el nombre que muestra el Explorador). Hay que pasar la base a config. | 1 (0) |
| `capturas-a-webp.py`, `capturas-nombre-corto.py` | Python, PIL, numpy, **`os.nice(19)`** | ✅ | `os.nice` **no existe en Windows** (AttributeError). Usar `psutil.Process().nice(psutil.IDLE_PRIORITY_CLASS)`. Son migraciones de una sola vez: casi no hace falta portarlos. | 0,5 (0) |
| `abrir-markdown.py` | Lee **`~/.config/obsidian/obsidian.json`**, lanza **`obsidian obsidian://…`** o **`code --open-url`** con `start_new_session` | ⚠️ (en WSL no tiene sentido) | En Windows: `%APPDATA%\obsidian\obsidian.json` y `os.startfile("obsidian://open?path=…")`. Asociar `.md` con `pythonw.exe abrir-markdown.py "%1"`, o simplemente poner Obsidian/VS Code como app por defecto. | 1 |
| `progreso.py` (barrita + `reportar`) | `reportar()`: Python puro (escritura atómica con `os.replace`). La barrita: **GTK4 + `libgtk4-layer-shell.so`** (capa OVERLAY, anclada abajo a la derecha del monitor `HDMI-A-1`, sin foco y con clics que la atraviesan), **`fcntl.flock`** en **`$XDG_RUNTIME_DIR`** para apilar varias barritas, fallback **`notify-send -p`** (reemplazar la notificación por id) | `reportar` ✅. La barrita **no** (WSLg dibuja ventanas, pero no tiene layer-shell ni sabe de la ScreenPad) | **Reescribir solo `seguir_barrita`:** tkinter con `overrideredirect(True)`, `-topmost`, `-alpha 0.85` y, por ctypes, `WS_EX_LAYERED \| WS_EX_TRANSPARENT \| WS_EX_NOACTIVATE \| WS_EX_TOOLWINDOW`, para que los clics pasen, no robe el foco y no aparezca en la barra de tareas. Ubicarla en la **ScreenPad Plus** buscando el monitor de 3840×1100 (`EnumDisplayMonitors`, `screeninfo` o `mss().monitors`), con DPI-aware. Lock: `msvcrt.locking` o `portalocker`/`filelock`. Fallback: `win11toast` (permite actualizar una toast con barra de progreso nativa) o BurntToast. | 6–8 (el `reportar` queda igual) |
| `auto-captura.conf`, `curso.conf`, `carpeta-capturas.conf`, `voz.conf` | `carpeta-capturas.conf` apunta a **`/run/media/yafer/SuperYafer/…`**. `voz.conf` usa rutas a **`/usr/share/piper-voices/…`** | — | Pasar rutas a config por máquina (p. ej. `%APPDATA%\cursos\config.toml`). | 0,5 |
| Tests (`*-tests.py`, `*-tests.sh`) | Los `.py` son portables. Los `.sh` dependen de `flock`/`pgrep`/stubs de bash | `.py` ✅ `.sh` ✅ | Los `.sh` se reescriben junto con la orquestación (conviene pasarlos a pytest). | incluido abajo |

### 1.2 Sistema de cursos: orquestación en bash (la “cáscara”)

| Script | Depende de | WSL2 | Nativo: con qué reescribir | h nativo (WSL) |
|---|---|---|---|---|
| `video-a-capturas.sh` | bash (`[[ =~ ]]`, `BASH_REMATCH`, `trap EXIT`), **`xdg-user-dir VIDEOS`**, **`$XDG_RUNTIME_DIR`**, **`setsid`** (lanza la barrita), `sed`, `realpath`, **yt-dlp** (`-S proto,vcodec:h264`, `--progress-template`, subtítulos con `--sleep-subtitles`), `python3` | ✅ casi tal cual (`xdg-user-dir` no existe en Ubuntu mínimo pero ya tiene el fallback `\|\| echo "$HOME/Vídeos"`; conviene fijar `BASE` a `/mnt/c/Cursos`) | Python: `subprocess` + parseo de la línea `PROGRESO`, `pathlib`, `tempfile.gettempdir()` en vez de `XDG_RUNTIME_DIR`, `subprocess.Popen(..., creationflags=DETACHED_PROCESS\|CREATE_NEW_PROCESS_GROUP)` en vez de `setsid`. | 4–6 (0,5) |
| `playlist-a-apuntes.sh` | lo anterior + **`flock -n 9`** (una sola playlist a la vez), `mapfile`, `declare -A`, **`nice -n 19 ionice -c 3`**, `tee`, `PIPESTATUS`, `grep` para detectar anti-bot/429, reintentos con `sleep 600/1200/1800` | ✅ | Python: `filelock`/`portalocker`, `psutil` (`IDLE_PRIORITY_CLASS` + `ioprio VERYLOW`), `re` para la detección de bloqueo. La lógica (reintentos, saltear privados, `.youtube-id` como identidad) se traduce 1:1. | 4–6 (0,5) |
| `curso-a-apuntes.sh` | `flock`, `find -printf`, `awk` (elige `clase.es.mp4` antes que `clase.mp4`), `nice`/`ionice`, `setsid`, `notify-send` | ✅ | Python: `pathlib.glob` + un dict. Es sencillo. | 2–3 (0,5) |
| `cola-capturas.sh` | **Dos `flock`** (cola.lock para secciones cortas y trabajador.lock mientras vive el trabajador), `exec 7>`, **`setsid bash "$0" trabajar &`**, `kill -TERM -- -PGID` (mata el grupo entero), `env -u`, `sed -i '1d'`, `mktemp`, `notify-send`; estado en `~/.cache/auto-captura/` | ✅ (flock y setsid andan en WSL). Ver el riesgo “WSL apaga la distro” en §5 | Python: `filelock` (dos locks, igual diseño), trabajador lanzado con `pythonw.exe` desacoplado, y para “cancelar” un **Job Object** o `psutil` recorriendo los hijos (`kill -PGID` no existe). Es la pieza con más concurrencia sutil: portar primero los tests. | 5–8 (1) |
| `youtube-capturas.sh` (SUPER+ALT+Y) | **`wl-paste`** (portapapeles), **`zenity --question --extra-button`** (¿solo el video o la playlist entera?), `notify-send`, yt-dlp `--flat-playlist` | ⚠️ `wl-paste` en WSLg no es confiable para el portapapeles de Windows; `zenity` sí abre por WSLg (feo, pero anda) | Del lado Windows: **AHK v2** lee `A_Clipboard` y muestra `MsgBox` con 3 botones, o Python con `pyperclip` + tkinter. Después **encola** (en WSL: `wsl.exe -e bash …/cola-capturas.sh encolar …`). | 2–3 (1) |
| `curso-apuntes-elegir.sh` (SUPER+ALT+A) | **`zenity --file-selection --directory`**, `xdg-user-dir` | ⚠️ (el selector de WSLg ve `/mnt/c/...`, incómodo) | AHK `DirSelect()` o `tkinter.filedialog.askdirectory()`. Convertir la ruta con `wslpath -u` si el motor está en WSL. | 0,5–1 (0,5) |
| `elegir-carpeta-capturas.sh`, `curso-configurar.sh`, `curso-abrir.sh` (SUPER+C) | `zenity`, `xdg-open`, **`hyprctl dispatch`** (workspace “estudio”), `brave`, `code` | ❌ (son de escritorio) | `curso-abrir`: AHK `Run` de URLs y apps. El “workspace” lo resuelve el tiling de Windows que evalúa el otro agente. Los diálogos de config: tkinter o editar el `.toml` a mano. | 2–3 |

### 1.3 Descargar y doblar

| Script | Depende de | WSL2 | Nativo | h nativo (WSL) |
|---|---|---|---|---|
| `descargar` (`~/.local/bin`) | bash, yt-dlp, **`--cookies-from-browser brave`**, `aria2c` (opcional), **`xdg-user-dir VIDEOS/MUSIC`** | ✅ el script sí, **pero las cookies no**: en WSL no hay Brave de Linux, y el Brave de Windows guarda las cookies cifradas con DPAPI de Windows, que Linux no descifra. Usar `--cookies cookies.txt` o Firefox (cookies sin cifrar: `--cookies-from-browser firefox:/mnt/c/Users/<u>/AppData/Roaming/Mozilla/Firefox/Profiles/<perfil>`) | Es un wrapper de 30 renglones: `descargar.ps1` o Python. yt-dlp.exe y aria2c existen para Windows (`winget`). **Cookies de Chromium en Windows:** ver riesgo en §5. | 1–2 (0,5) |
| `doblar` → `doblar.py` (+ `estado.py`) | venv con `faster-whisper` 1.2.1 / `ctranslate2` 4.8.2 / `sentencepiece` / `edge-tts` / `soundfile` / numpy; **`whisper-cli` (whisper.cpp por Vulkan, pensado para la GTX 980)**; NLLB-200 en CTranslate2 (**2,4 GB**, `device="cpu"` fijo); **`pgrep -f bin/yt-dlp`** (modo `--seguir`); `~/.cache/doblar`; `estado.py` usa **`journalctl`** | ✅ con **CUDA**. En WSL2 la RTX 3060 se ve como CUDA real (§3.2) | Mismo código. `pgrep` → `psutil.process_iter()` buscando `yt-dlp`. `journalctl` → leer un log propio. whisper.cpp tiene binarios oficiales para Windows (CUDA y Vulkan) y el `GPU_OK` anda si `whisper-cli.exe` está en el PATH. | 3–5 (3–5, casi todo es instalar CUDA/cuDNN y modelos) |

**Mejora casi gratis en la laptop:** con la RTX 3060 (arquitectura Ampere, sirve con CTranslate2/CUDA 12, a diferencia de la GTX 980), `faster-whisper` puede correr `large-v3-turbo` en `device="cuda", compute_type="float16"` y **NLLB también en CUDA** (`device="cuda"`, hoy está en `"cpu"` fijo, línea 169). Es cambiar 2 renglones, idealmente con una variable `DISPOSITIVO=auto`. La traducción, que hoy es CPU int8, debería acelerarse mucho. NLLB-1.3B en float16 ocupa ~2,6 GB de VRAM y whisper turbo ~1,5–2 GB, así que entran los dos en los 6 GB de la 3060 laptop si se cargan uno después del otro (el script ya los usa en etapas separadas).

### 1.4 Lectura en voz alta (SUPER+R) y voz

| Script | Depende de | WSL2 | Nativo | h |
|---|---|---|---|---|
| `leer-seleccion.sh` | **`wl-paste --primary`** (selección primaria: **no existe en Windows**), **`hyprctl activewindow`** (¿es una terminal?), **`ydotool key 29:1 46:1…`** / **`wtype`** (Ctrl+C sintético), `wl-copy` (restaura el portapapeles), `pgrep`/`pkill` (toggle), **`edge-tts`**, **`piper-tts`**, **`pw-play`/`paplay`**, `systemctl --user start piper-voz-daemon` | ❌ | **AHK v2**: `ClipSaved := ClipboardAll()`, `A_Clipboard := ""`, `Send "^c"`, `ClipWait 0.3`, llamar a `pythonw leer.py` con el texto y restaurar `A_Clipboard := ClipSaved`. Es lo mismo que hace hoy, pero sin selección primaria: **siempre** hace falta el Ctrl+C. El toggle: si hay un proceso de lectura vivo, matarlo (`psutil` o PID file). Audio: `sounddevice` o `ffplay -nodisp -autoexit`. `edge-tts` y `piper-tts` (pip, onnxruntime) andan en Windows; las voces `.onnx` se copian. | 6–10 |
| `piper-daemon.py` / `piper-client.py` | **`socketserver` sobre socket Unix (`AF_UNIX`)** en `~/.cache/piper-voz.sock`, servicio systemd | ❌ | CPython en Windows **no expone `AF_UNIX`**. Usar TCP en `127.0.0.1` o `multiprocessing.connection.Listener(r'\\.\pipe\piper-voz')`. Arranque: carpeta *Startup* o Programador de tareas. | 2–3 |
| `limpiar-texto.py` | Python puro | ✅ | Nada. | 0 |
| `elegir-voz.py` (SUPER+ALT+R), `actualizar-voz.sh` | **GTK (gi)**, `zenity`, `notify-send` | ❌ | Reescribir la ventanita en tkinter o dejar la voz en un `.toml`. Hay alternativa: la voz neural “Leer en voz alta” de Edge o las voces naturales del Narrador (lo evalúa el otro agente). | 3–4 (u omitir) |
| `chatterbox-hablar.py` | venv de chatterbox (torch) | ⚠️ | Opcional; con CUDA en la 3060 incluso andaría mejor. No es prioritario. | — |

### 1.5 Dictado (hyprwhspr)

- No es código propio: es el paquete AUR `hyprwhspr` (evdev para el atajo, pywhispercpp, **ydotool/uinput** para pegar, overlay GTK4 layer-shell) con `~/.config/hyprwhspr/config.json` (`small`, `es`, toggle, `SUPER+ALT+Z`/`X`, mic “Maono”).
- **No se porta: se reemplaza.** Opciones en Windows (que las compare el otro agente): **Win+H** (dictado de Windows, gratis, en español), o apps con whisper local que aprovechen la 3060 (p. ej. Handy u OpenWhispr, que ya aparecían como plan B en `~/Documentos/maono/CLAUDE.md`). Lo único a reproducir de la config: idioma `es`/`en` con dos atajos, modo toggle, filtro de muletillas y el micrófono Maono (el receptor USB anda igual en Windows).
- Esfuerzo propio: 0–2 h de configuración.

### 1.6 Escritorio / sesión (no se portan: los reemplaza Windows o apps)

| Script | Qué hace | En Windows |
|---|---|---|
| `sesion-ventanas.py` | Recuerda en qué workspace estaba cada ventana de Brave (`hyprctl clients -j`, `difflib`) | Lo cubre el tiling/“Workspaces” que investiga el otro agente (p. ej. PowerToys Workspaces). Reescribirlo con `pywin32` + escritorios virtuales es posible pero frágil: **no vale la pena**. |
| `app-web.sh`, `vscode-open-md.sh`, `watch-monitors.sh` (`inotifywait` + `hyprctl`), `pomodoro-toggle.sh`, `matar-libreoffice.sh` | Lanzadores y utilidades de Hyprland | AHK `Run`/`WinActivate`; Brave “instalar como app”. Pomodoro: cualquier app. |
| `captura-guardar.sh`, `captura-portapapeles.sh` | `slurp` + `grim` + `wl-copy` | **Win+Shift+S** (Recortes) o ShareX, que guarda en una carpeta y copia en un paso. |
| `teclas-fantasma.py` (evdev) | Diagnóstico de suspensiones fantasma en esta PC | No aplica. |
| `backup-home.sh` (restic) | Backup diario | restic tiene binario para Windows + Programador de tareas (1–2 h), o el backup nativo/OneDrive (**nunca** sobre la carpeta de cursos, ver §5). |

---

## 2. Qué es portable tal cual, qué va en WSL2 y qué hay que reescribir

```
PORTABLE TAL CUAL (Python + numpy/PIL + ffmpeg + tesseract + claude)       ≈ 2 000 renglones
  auto-captura.py (Detector + modo video) · cuadernillo.py · resumen-corto.py · tarjetas.py
  panel-cursos.py* · capturas-*.py* · limpiar-texto.py · doblar.py* · progreso.reportar()
  (*) con los arreglos chicos de §4.4

CORRE EN WSL2 SIN CAMBIOS (bash + coreutils + flock + setsid + nice/ionice + yt-dlp)  ≈ 550 renglones
  video-a-capturas.sh · playlist-a-apuntes.sh · curso-a-apuntes.sh · cola-capturas.sh · descargar
  (con “shims” de 3 renglones para notify-send / xdg-user-dir / progreso “seguir”, ver §3.3)

HAY QUE REESCRIBIR PARA WINDOWS (UI, entrada, pantalla, audio)
  captura en vivo (grim)            → mss / windows-capture / dxcam
  monitor y ventana activa (hyprctl) → ctypes/pywin32: GetForegroundWindow, MonitorFromWindow
  barrita GTK4 layer-shell          → tkinter topmost + alpha + WS_EX_TRANSPARENT|NOACTIVATE
  notify-send                       → win11toast / BurntToast (powershell)
  zenity                            → AHK MsgBox/DirSelect o tkinter
  wl-paste/wl-copy                  → pyperclip / AHK A_Clipboard / powershell Get-Clipboard
  ydotool/wtype (Ctrl+C sintético)  → AHK Send "^c" (o SendInput por ctypes)
  fcntl.flock / flock(1)            → msvcrt.locking / portalocker / filelock
  setsid / kill -PGID               → DETACHED_PROCESS + Job Object / psutil
  nice / ionice                     → psutil IDLE_PRIORITY_CLASS + IOPRIO_VERYLOW
  socket AF_UNIX                    → TCP localhost o named pipe
  systemd --user                    → Programador de tareas / carpeta Startup
  atajos Hyprland (binds.lua)       → AutoHotkey v2 o botones del Stream Deck
```

---

## 3. Estrategia recomendada

### 3.1 Comparación de las tres opciones

| | **A. WSL2 para el motor + UI nativa** | **B. Todo Python nativo (solo Windows)** | **C. Python multiplataforma (Linux + Windows, un solo código)** |
|---|---|---|---|
| Tiempo hasta que ande | **El más corto** (~20–30 h, la mayoría en la UI nativa, que igual hay que hacer) | ~35–50 h | ~45–70 h (es B más una capa `plataforma.py` con dos backends) |
| Scripts bash | Quedan igual | Se reescriben | Se reescriben una vez y sirven para CachyOS, las laptops Linux y el Zenbook |
| CUDA | Anda (driver de Windows + wheels CUDA dentro de WSL) | Anda (DLLs de cuBLAS/cuDNN en Windows: un poco más “mañoso”) | Igual que B en Windows, igual que hoy en Linux |
| Archivos | Fricción: si los datos están en ext4 (rápido para WSL), Obsidian y la captura en vivo pasan por `\\wsl$`, que es lento. Si están en NTFS (`/mnt/c`), WSL pasa por 9P, más lento para muchos archivos chicos. | Sin fricción: todo en NTFS | Sin fricción |
| Suspensión, energía, prioridad | WSL no sabe de la batería ni puede impedir que Windows suspenda (hace falta un helper del lado Windows) | `SetThreadExecutionState`, `psutil.sensors_battery()`, prioridad idle nativa | Igual que B |
| Mantenimiento | Dos mundos (dos Pythons, dos `claude` logueados, dos yt-dlp que actualizar) | Un mundo, pero solo Windows | **Un mundo y un código**: un arreglo en el detector llega a todas las máquinas |
| Riesgo | Que WSL mate procesos largos (§5) | Poco | Poco; es más trabajo inicial |

**Veredicto:**
- **A como punto de partida** (valor inmediato con poco código nuevo).
- **C como destino**, porque el usuario sigue con CachyOS en la PC de escritorio y quizás en otras laptops. Hoy el ~80 % del código ya es multiplataforma. Lo que falta es justamente la “cáscara”, y pasarla a Python con una capa de plataforma es un buen ejercicio de ingeniería (inyección de dependencias, adaptadores por SO).
- **B solo no conviene:** cuesta casi lo mismo que C y deja dos versiones que divergen.

**¿Vale la pena C?** Sí, pero **sin apuro**. La Etapa 1 ya hace que la UI nativa sea Python (barrita, captura en vivo, toggle). Esos módulos nacen multiplataforma si se escriben detrás de una interfaz: `capturar_pantalla(monitor)`, `notificar(...)`, `barrita(...)`, `portapapeles()`, `elegir_carpeta()`, `lock(nombre)`, `lanzar_desacoplado(cmd)`, `prioridad_baja()`. Después, portar la orquestación bash a Python es el último paso, y ahí WSL deja de ser necesario.

### 3.2 CUDA en WSL2: qué instalar (RTX 3060 laptop)

1. **En Windows:** solo el **driver NVIDIA normal** (Game Ready/Studio). Ese driver ya incluye el soporte para WSL: dentro de WSL aparece `libcuda.so` en `/usr/lib/wsl/lib/` y `nvidia-smi` funciona. Actualizar WSL con `wsl --update` (el kernel tiene que ser ≥ 5.10.43.3 según la doc de Microsoft).
2. **En WSL (Ubuntu): NO instalar ningún driver NVIDIA de Linux**, porque pisaría el `libcuda` que viene de Windows. Si hiciera falta el toolkit completo (nvcc), usar el paquete `cuda-toolkit-12-x` del repositorio **“WSL-Ubuntu”** de NVIDIA, **no** el metapaquete `cuda` (ese arrastra el driver).
3. Para `faster-whisper`/CTranslate2 no hace falta el toolkit: alcanza con `pip install nvidia-cublas-cu12 nvidia-cudnn-cu12` dentro del venv y exportar `LD_LIBRARY_PATH` a esas carpetas. CTranslate2 4.5 o más nuevo pide **CUDA 12 + cuDNN 9**. Para whisper.cpp: compilar con `-DGGML_CUDA=1` o seguir con Vulkan (en WSL el Vulkan de la GPU va por la capa D3D12 de Mesa: **CUDA es el camino seguro**).
4. Probar: `nvidia-smi` dentro de WSL; `python -c "import ctranslate2; print(ctranslate2.get_cuda_device_count())"` tiene que dar 1.

En **Windows nativo** (opción B/C) es lo mismo sin WSL: driver + `pip install nvidia-cublas-cu12 nvidia-cudnn-cu12`, y hacer `os.add_dll_directory()` a las carpetas `bin` de esos paquetes antes de importar ctranslate2 (o usar las DLLs que empaqueta *whisper-standalone-win* de Purfview). whisper.cpp publica binarios Windows con CUDA listos.

### 3.3 Diagrama de la Etapa 1 (híbrida)

```
                         WINDOWS 11 (nativo)                                      │  WSL2 (Ubuntu, motor por lotes)
                                                                                  │
 Stream Deck / AHK v2 ─┬─ Win+Alt+S ─► pythonw auto_captura_vivo.py ──(mss)──┐    │
                       │                    │ Detector (mismo auto-captura.py)│   │
                       │                    └──► C:\Cursos\Capturas\auto_…    │   │
                       │                                                      │   │
                       ├─ Win+Alt+Y ─► lee portapapeles, pregunta (MsgBox) ───┼───┼─► wsl.exe -e bash cola-capturas.sh encolar video|playlist URL
                       ├─ Win+Alt+A ─► DirSelect → wslpath ───────────────────┼───┼─► wsl.exe -e bash cola-capturas.sh encolar curso /mnt/c/Cursos/…
                       │                                                      │   │        │ trabajador (flock) → playlist/video-a-capturas.sh
                       │                                                      │   │        │   yt-dlp → ffmpeg → auto-captura.py --video → cuadernillo.py
                       │                                                      │   │        │   → claude -p → resumen/tarjetas/panel
                       │                                                      │   │        ▼
                       │          C:\Cursos\  (NTFS, fuera de OneDrive) ◄─────┴───┼──── escribe en /mnt/c/Cursos/…  (misma carpeta)
                       │             ▲   ▲                                        │        │
                       │   Obsidian ─┘   └─ progreso_win.py (barrita tkinter      │        └─ progreso.py poner → C:\Cursos\.estado\progreso.txt
                       │   (bóveda)          en la ScreenPad Plus) lee ─────────────────────────────────────────────┘
                       │                                                          │
                       ├─ Win+R (o otra tecla) ─► AHK Ctrl+C → pythonw leer.py → edge-tts / piper (named pipe) → audio
                       └─ Dictado: Win+H o app whisper (no se porta)              │  doblar (faster-whisper + NLLB en CUDA)
                                                                                  │  descargar (yt-dlp + cookies.txt)
```

**El contrato entre los dos mundos ya existe:** `progreso.py` separa *quién trabaja* (`reportar()` escribe `pct|etapa|detalle|clase` en un archivo, con escritura atómica) de *quién muestra* (`seguir`). En WSL solo hace falta:
- `PROGRESO_ARCHIVO` apuntando a `/mnt/c/...`.
- Que `progreso.py seguir` detecte WSL (existe `/proc/sys/fs/binfmt_misc/WSLInterop`) y **delegue** en `pythonw.exe C:\...\progreso_win.py seguir "$(wslpath -w "$archivo")" "$titulo"` en vez de abrir GTK.
- Un `notify-send` falso en `~/.local/bin` de WSL que llame a `powershell.exe -NoProfile -Command New-BurntToastNotification …` (o `wsl-notify-send.exe`). Así los `.sh` quedan **sin tocar**.

### 3.4 Dónde guardar los cursos

- **Recomendado: `C:\Cursos\` (o `D:` si hay otra partición), fuera de OneDrive.** Obsidian (nativo), la captura en vivo (nativa) y el motor (WSL por `/mnt/c`, después nativo) ven la misma carpeta. La bóveda de Obsidian = `C:\Cursos`.
- **Por qué no en ext4 de WSL:** Microsoft recomienda guardar los archivos en el sistema de archivos del lado donde se trabaja (§ fuentes). Obsidian leyendo 16 000 archivos por `\\wsl$` (protocolo 9P) indexa lento y **el aviso de cambios no cruza bien**: las notas nuevas pueden no aparecer hasta reabrir.
- **Costo de `/mnt/c` para el motor:** este trabajo es sobre todo CPU/GPU (decodificar video, numpy, OCR, Claude). La E/S es secuencial (el video) y de pocos cientos de `.webp` por clase, así que la penalidad de 9P debería ser **chica**. Pesan más las operaciones de metadatos (`ls`, `find`, `glob` sobre miles de archivos); por ejemplo `cuadernillo.elegir_capturas` relee todas las capturas de una clase. **Medirlo** con una clase: `time` en WSL con los datos en `~/` y en `/mnt/c/`.
- **Dev Drive (ReFS + Defender en “modo rendimiento”):** mejora la E/S nativa de Windows con muchos archivos (ideal para la Etapa 2). Condiciones: **no puede ser C:**, mínimo 50 GB, se crea como partición nueva o como **VHDX dinámico**. **No mejora WSL** (lo dice la doc). Es buena opción para `C:\Cursos` → `D:\Cursos` (VHDX) cuando el motor sea nativo.

---

## 4. Detalles finos que rompen cosas (y cómo evitarlos)

### 4.1 Nombres de archivo y caracteres
- **`：` (U+FF1A) y `｜` (U+FF5C) son caracteres Unicode “de ancho completo”, no los ASCII prohibidos.** NTFS los acepta sin problema: el curso `Neural Networks： Zero to Hero` se puede copiar tal cual. yt-dlp en Windows ya reemplaza así los caracteres prohibidos por defecto.
- Los scripts ya limpian `/ \ : * ? " < > |`, puntos y espacios al final (`limpiar()` en bash; la misma regla hay que llevarla a Python). **Falta en esa regla:** los nombres reservados de Windows (`CON`, `PRN`, `AUX`, `NUL`, `COM1`…`LPT9`, también con extensión: `con.md`). Es raro en títulos, pero agregar un chequeo cuesta un renglón.
- Windows **no distingue mayúsculas**: dos clases “Intro” e “intro” chocarían (improbable, porque llevan el prefijo `NNN - `).
- Si el motor corre en WSL y escribe en `/mnt/c` un nombre con `:` ASCII, DrvFs lo guarda como un carácter de uso privado que en el Explorador se ve como un cuadrito. La limpieza actual lo evita: **no sacarla**.

### 4.2 Rutas largas (>260)
- Medido hoy: la ruta relativa más larga dentro de `~/Vídeos` tiene **155** caracteres (16 193 archivos, 17 GB). Con `C:\Users\yafer\Videos\` delante da ~177: **pasa**. Pero los títulos se cortan a 80 bytes (`%(title).80B`) **dos veces** (playlist + clase), más `capturas\NNN - ` y `subtitulos.es-orig.srt`, así que el peor caso ronda ~250.
- **Habilitar igual:** `HKLM\SYSTEM\CurrentControlSet\Control\FileSystem\LongPathsEnabled = 1` (o la directiva “Habilitar rutas largas de Win32”). Ojo: **solo sirve para programas que lo declaran en su manifiesto** (`longPathAware`). El `python.exe` de python.org lo declara. yt-dlp.exe, tesseract o el Explorador pueden no hacerlo.
- La defensa real: **base corta** (`C:\Cursos` en vez de `C:\Users\yafer\Videos\Capturas de YouTube`) y mantener los recortes a 80 bytes.

### 4.3 Fin de línea (CRLF)
- Si los scripts viajan por git con `core.autocrlf=true`, los `.sh` llegan con CRLF y bash en WSL falla con `$'\r': command not found`. Solución: `.gitattributes` con `*.sh text eol=lf` y `*.py text eol=lf`.
- Archivos que se leen desde bash (`cola.txt`, `.youtube-id`, `.cantidad`, `.playlist.tsv`, el archivo de progreso) no pueden tener `\r` si los escribe Python de Windows. Al escribirlos desde Windows, usar `open(..., "w", newline="\n")`. Python leyendo en modo texto tolera las dos cosas.

### 4.4 Codificación (el bug más probable)
- En Windows, `open()` sin `encoding`, `subprocess(..., text=True)` sin `encoding` y `print()` redirigido a un archivo de log usan la **página de códigos ANSI (cp1252)**, no UTF-8. Consecuencias concretas en este código:
  - `cuadernillo.py:362` y `resumen-corto.py:67`: `subprocess.run(cmd, input=prompt, text=True)`. El prompt lleva subtítulos y OCR, y **cualquier carácter fuera de cp1252 (emoji, chino, `｜`) tira `UnicodeEncodeError`**.
  - Los `print("📓 …")` de los scripts, cuando la cola los redirige a `~/.cache/auto-captura/*.log`, también fallan.
  - `auto-captura.py:47` lee el `.conf` (comentarios con tildes) sin `encoding`. No rompe, pero lee basura en los comentarios.
- **Arreglo global:** variable de entorno de usuario **`PYTHONUTF8=1`** (`setx PYTHONUTF8 1`). Con eso, todo lo anterior pasa a UTF-8. PEP 686 hace de UTF-8 el modo por defecto a partir de **Python 3.15** (la versión que sale en octubre de 2026). Para 3.13/3.14 hay que poner la variable. Igual conviene agregar `encoding="utf-8"` en esos 7 `subprocess` y 2 `open`.
- Consola: Windows Terminal + Python ≥3.6 muestran emojis bien en pantalla. El problema aparece solo al redirigir la salida.

### 4.5 Otras trampas de Windows en este código
- `panel-cursos.py:119`: `os.path.relpath` devuelve `\`, lo que rompe los links Markdown (§1.1).
- `os.nice` (capturas-a-webp), `fcntl` (progreso), `signal.SIGTERM` como mecanismo de corte (auto-captura vivo), `pgrep`/`journalctl` (doblar/estado).
- `python3` en Windows puede ser el **alias de la Microsoft Store** (abre la tienda). Usar `py -3.13` o el `python.exe` de un venv creado con `uv`. Desactivar los “alias de ejecución de aplicaciones”.
- `claude` en Windows: instalación nativa por PowerShell. `ruta_claude()` lo encuentra con `shutil.which`. **Login aparte en Windows y en WSL** (son dos instalaciones). Las dos comparten los límites de uso del plan: no correr una playlist en la PC y otra en la laptop a la vez.
- DPI: pantalla 4K de 15,6" con escala ~250 %. Todo lo que mida o ubique ventanas (captura en vivo, barrita) tiene que ser *per-monitor DPI aware*; si no, la barrita de 420×28 px sale diminuta o fuera de lugar en la ScreenPad (que puede tener otra escala).

---

## 5. Riesgos concretos y mitigación

| Riesgo | Por qué pasa | Mitigación |
|---|---|---|
| **OneDrive se “come” la carpeta de cursos** | Windows 11 suele activar “Copia de seguridad de carpetas” (Known Folder Move) para Escritorio/Documentos/Imágenes; en algunas cuentas también Videos. 16 000 `.webp` + mp4 temporales sincronizándose = CPU, red y conflictos | Base **fuera** de las carpetas conocidas (`C:\Cursos`). Revisar OneDrive → Configuración → Copia de seguridad. |
| **Defender escanea cada captura** | La protección en tiempo real inspecciona cada archivo creado. Miles de `.webp` + ffmpeg/yt-dlp escribiendo lo vuelven lento, y cada `.exe` de un venv también se escanea | **Dev Drive** (Defender en modo rendimiento, asíncrono) para `D:\Cursos` y los venv, o una exclusión de carpeta para `C:\Cursos` (menos seguro; nunca excluir Descargas). |
| **La laptop suspende o hiberna en medio de una playlist de 166 videos** | Modern Standby / plan de energía; cerrar la tapa | En nativo: el trabajador llama a `SetThreadExecutionState(ES_CONTINUOUS \| ES_SYSTEM_REQUIRED)` mientras trabaja. Con WSL: Windows no ve esa actividad, así que hace falta un helper del lado Windows (PowerToys **Awake**, o que el `wsl.exe` que lanza AHK sea hijo de un script que haga esa llamada). “Al cerrar la tapa, enchufado: no hacer nada”. Todo ya es **reanudable** (`.cantidad`, `apuntes.md`, `.youtube-id`), así que un corte no pierde trabajo, solo tiempo. |
| **Batería y térmica** | RTX 3060 + i7 al 100 % durante horas; a batería la GPU se limita | Correr el motor **solo enchufado**: chequear con `psutil.sensors_battery().power_plugged` y pausar si no. Prioridad idle. Perfil de ventiladores de MyASUS en “Estándar” o “Rendimiento”. |
| **WSL apaga la distro y mata al trabajador** | WSL cierra la VM o la distro cuando no quedan procesos “de sesión” (`vmIdleTimeout`, y el cierre de la distro unos segundos después de la última terminal). Un `setsid … &` lanzado desde un `wsl.exe` que ya terminó puede morir con ella. **No lo pude verificar hoy: probarlo** | Que el trabajador **sea** el proceso de un `wsl.exe` que no termina hasta vaciar la cola (AHK: `Run 'wsl.exe -e bash …/cola-capturas.sh trabajar',, "Hide"`), no un `setsid` suelto. O `systemd=true` en `/etc/wsl.conf` con el trabajador como servicio. Probar con `wsl --list --running` después de cerrar todas las terminales. |
| **Cookies de Brave/Chrome para yt-dlp en Windows** | Desde Chrome 127 (2024), Chromium en Windows cifra las cookies con “App-Bound Encryption”, y `--cookies-from-browser chrome` falla (dato de memoria sobre el issue #10927 de yt-dlp: **verificar el estado actual y si alcanza también a Brave/Edge**). Además, con el navegador abierto la base de cookies está bloqueada | Usar **Firefox** para la sesión (`--cookies-from-browser firefox`, sin ese cifrado) o exportar un `cookies.txt` con una extensión y pasar `--cookies`. En WSL es obligatorio igual (§1.3). |
| **Anti-bot / 429 de YouTube** | Es igual en todos lados (depende de la IP y la cuenta, no del SO) | Ya está resuelto en `playlist-a-apuntes.sh` (espera 10/20/30 min y corta). Mantener yt-dlp al día (`yt-dlp -U` / `winget upgrade`). Las versiones recientes de yt-dlp piden un **runtime de JavaScript (Deno)** para YouTube: instalarlo en el lado donde corra (dato de memoria, verificar). No correr la misma playlist desde dos máquinas. |
| **Contenido con DRM → capturas negras** | La captura en vivo de Windows (GDI/DXGI/WGC) devuelve negro para video protegido con DRM por hardware (Udemy/plataformas pagas en Edge o Chrome con PlayReady/Widevine) | Para esos cursos, bajar la aceleración de hardware del navegador o usar el modo “video descargado” si la plataforma lo permite. YouTube normal no tiene DRM. |
| **Atajos que choca Windows** | Win+R (Ejecutar), Win+H (dictado), Win+C (Copilot), Win+Alt+R/G/K… (Xbox Game Bar), Win+Alt+D (fecha) | AHK v2 puede pisar la mayoría. Desactivar los atajos de Game Bar. O usar el Stream Deck, que evita conflictos. Lo coordina el otro agente. |
| **Dos entornos que se desincronizan** | Dos Python, dos `claude`, dos yt-dlp y dos copias de los scripts en la Etapa 1 | Un repo git con los scripts (`eol=lf`), un `pyproject.toml` con `uv` y una lista de dependencias por SO. Es otro motivo para ir a la Etapa 2. |
| **Espacio en disco** | venv de doblar (455 MB) + NLLB (2,4 GB) + whisper (835 MB) + caché HF + videos temporales; además, el disco virtual de WSL (`ext4.vhdx`) **crece y no se achica solo** | Modelos en una carpeta compartida. `wsl --manage <distro> --set-sparse true` o compactar el VHDX de vez en cuando. |
| **Carpetas en español** | El código tiene `~/Vídeos` y `~/Imágenes` fijos. En Windows son `Videos`/`Pictures` (el nombre en español es solo visual) | Base configurable (una sola variable `CURSOS_BASE`). |

---

## 6. Orden de migración sugerido (valor ÷ esfuerzo)

| # | Qué | Por qué primero | h aprox. |
|---|---|---|---|
| 0 | **Preparación:** WSL2 Ubuntu + driver NVIDIA + `PYTHONUTF8=1` + `LongPathsEnabled` + carpeta `C:\Cursos` fuera de OneDrive (idealmente un Dev Drive VHDX) + Python (uv) + ffmpeg, tesseract, yt-dlp, deno y `claude` en los dos lados + repo git con `eol=lf` | Base de todo lo demás | 3–4 |
| 1 | **Motor por lotes en WSL2:** copiar los scripts, `BASE_CAPTURAS=/mnt/c/Cursos/…`, shims `notify-send`/`xdg-user-dir`, cookies.txt. Probar `video-a-capturas.sh` con un link, después `playlist-a-apuntes.sh` con `MAX_VIDEOS=2`. Correr los tests `.sh` y `.py` | Es el 80 % del valor (apuntes, resumen y tarjetas de playlists enteras) con ~0 código nuevo | 3–4 |
| 2 | **Obsidian** en Windows con la bóveda en `C:\Cursos` + arreglo de `relpath` en `panel-cursos.py` + plugin de repetición espaciada | Para *usar* lo que produce el motor | 1–2 |
| 3 | **Atajos de encolar** (Win+Alt+Y con portapapeles + pregunta de playlist; Win+Alt+A con selector de carpeta) en AHK v2 o Stream Deck → `wsl.exe … cola-capturas.sh encolar` | Recupera el flujo “copio el link y me olvido” | 3–4 |
| 4 | **Barrita en la ScreenPad Plus** (`progreso_win.py` en tkinter, sin foco y sin clics, DPI-aware) + delegación desde el `progreso.py` de WSL + toast final | Es lo que da “tranquilidad” en procesos de horas; la ScreenPad es el lugar ideal | 6–8 |
| 5 | **doblar con CUDA** (en WSL: wheels cuBLAS/cuDNN; `device="cuda"` para whisper **y** NLLB) + `descargar` con cookies de Firefox o cookies.txt | Gran mejora de velocidad gracias a la 3060 | 3–5 |
| 6 | **Auto-captura en vivo** nativa (mss o windows-capture + monitor de la ventana activa + corte por archivo “stop” + toggle desde AHK) | Útil, pero se usa menos que el modo link | 6–9 |
| 7 | **Lectura en voz alta** (AHK Ctrl+C → Python → edge-tts, con Piper offline por named pipe) — **o** adoptar la opción nativa que recomiende el otro agente | Hay alternativas nativas “buenas enough”; es mucho código propio por poca ganancia | 0–10 |
| 8 | **Dictado:** configurar Win+H o una app whisper local | Reemplazo, no port | 0–2 |
| 9 | **Etapa 2: orquestación a Python multiplataforma** (`cola`, `playlist`, `curso`, `video-a-capturas`, `youtube-capturas`) + `plataforma.py` + tests a pytest. Después, apagar WSL para esto | Un solo código para CachyOS y Windows, con control nativo de suspensión y energía | 20–30 |
| — | Descartar o reemplazar: `sesion-ventanas.py`, `app-web.sh`, `watch-monitors.sh`, `vscode-open-md.sh`, `pomodoro`, `matar-libreoffice`, `teclas-fantasma`, `captura-*.sh` (→ Win+Shift+S/ShareX), `elegir-voz.py` | Los resuelve Windows o las apps del otro agente | 0–3 |

**Total aproximado:** pasos 0–6 ≈ **25–36 h** (sistema de cursos completo en la laptop). Con lectura/dictado ≈ 30–48 h. Con la Etapa 2 ≈ **45–70 h**.

---

## 7. Fuentes

Verificadas hoy (leídas el 28-09-2026):
- Microsoft Learn, *Working across file systems (WSL)*: recomienda guardar los archivos en el sistema de archivos del SO donde se trabaja; `\\wsl$`; interoperabilidad `wsl.exe`/`.exe`; `WSLENV`. https://learn.microsoft.com/en-us/windows/wsl/filesystems
- Microsoft Learn, *Maximum Path Length Limitation*: `LongPathsEnabled`, directiva de grupo y el requisito del manifiesto `longPathAware`. https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation
- Microsoft Learn, *Set up a Dev Drive on Windows 11*: ReFS, Defender en modo rendimiento, mínimo 50 GB, no puede ser C:, VHDX, “no mejora WSL”. https://learn.microsoft.com/en-us/windows/dev-drive/
- Microsoft Learn, *Enable NVIDIA CUDA on WSL 2*: driver en Windows, kernel ≥ 5.10.43.3, distro glibc. https://learn.microsoft.com/en-us/windows/ai/directml/gpu-cuda-in-wsl

No se pudieron abrir hoy (límite de la herramienta web). Son datos de memoria, **a verificar** antes de instalar:
- NVIDIA, *CUDA on WSL User Guide*: no instalar el driver de Linux dentro de WSL; `/usr/lib/wsl/lib/libcuda.so`; toolkit del repo “WSL-Ubuntu”. https://docs.nvidia.com/cuda/wsl-user-guide/index.html
- SYSTRAN/faster-whisper README: CTranslate2 reciente = CUDA 12 + cuDNN 9; wheels `nvidia-cublas-cu12`/`nvidia-cudnn-cu12`; en Windows, las DLLs de Purfview. https://github.com/SYSTRAN/faster-whisper
- yt-dlp issue #10927 (cookies de Chromium en Windows, App-Bound Encryption). https://github.com/yt-dlp/yt-dlp/issues/10927 · Wiki EJS/Deno de yt-dlp: https://github.com/yt-dlp/yt-dlp/wiki/EJS
- PEP 686 (UTF-8 mode por defecto desde Python 3.15). https://peps.python.org/pep-0686/
- WSL `.wslconfig` (`vmIdleTimeout`, `autoMemoryReclaim`, `sparseVhd`) y `wsl.conf` (`systemd=true`). https://learn.microsoft.com/en-us/windows/wsl/wsl-config
- `SetThreadExecutionState`: https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-setthreadexecutionstate
- Estilos de ventana extendidos (`WS_EX_TRANSPARENT`, `WS_EX_NOACTIVATE`, `WS_EX_LAYERED`): https://learn.microsoft.com/en-us/windows/win32/winmsg/extended-window-styles
- Librerías: `mss` https://github.com/BoboTiG/python-mss · `windows-capture` https://github.com/NiiightmareXD/windows-capture · `dxcam` https://github.com/ra1nty/DXcam · `win11toast` https://github.com/GitHub30/win11toast · BurntToast https://github.com/Windos/BurntToast · `filelock` https://github.com/tox-dev/filelock · `portalocker` https://github.com/wolph/portalocker · whisper.cpp releases (binarios Windows CUDA/Vulkan) https://github.com/ggml-org/whisper.cpp/releases

Evidencia local (comandos de solo lectura hechos hoy): `grep` de dependencias por script; `~/Vídeos` = 17 GB, 16 193 archivos (15 960 `.webp`), ruta relativa más larga de 155 caracteres, ningún carácter ASCII prohibido por NTFS en los nombres (sí `：` de ancho completo); `open()`/`text=True` sin `encoding` en `auto-captura.py:47`, `cuadernillo.py:251,272,337,362`, `resumen-corto.py:67`; `os.path.relpath` en `panel-cursos.py:119`; `device="cpu"` fijo en `doblar.py:169` y `WhisperModel(..., device="cpu")` en `doblar.py:101`.
