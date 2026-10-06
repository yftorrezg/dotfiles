# Migración CachyOS + Hyprland a las laptops — Resumen

26/09/2026 (actualizado tras la auditoría) · **actualizado 28/09/2026**: capturas y apuntes automáticos de cursos, Obsidian, Windows 11 · Lectura simple. El detalle técnico está en `README.md` y en `docs/`.

**Orden recomendado para leer:** 1) este resumen → 2) `README.md` → 3) el `docs/` del tema que quieras estudiar.

**En Obsidian:** abre la carpeta `~/migracion-cachyos` como bóveda y empieza por `INICIO.md` (ver sección 7).

---

## 1. Qué hay en la carpeta de Drive

La carpeta tiene todo lo necesario para que Claude repita en la laptop la configuración de esta PC.

| Archivo | Qué es | ¿Se puede leer en Drive? |
| --- | --- | --- |
| `00-RESUMEN.md` | Este resumen | Sí |
| `INICIO.md` | Índice con enlaces (pensado para Obsidian) | Sí |
| `README.md` | Instrucciones para Claude en la laptop | Sí |
| `docs/01` a `docs/08` | Explicación detallada por tema (ver tabla abajo) | Sí |
| `docs/GAPS.md` / `docs/LIMPIEZA.md` | Qué faltaba documentar / qué se limpió del paquete | Sí |
| `guias-usuario/` | Tus propias guías de `~/Documentos` (Stream Deck, Maono, M720, móvil, aprender, **capturas y apuntes de cursos**...) | Sí |
| `paquetes/` | Programas instalados, cuáles se usan y las 95 extensiones de VS Code | Sí |
| `claude-memoria/` | Lo que Claude recuerda de tus preferencias y proyectos | Sí |
| `migracion-cachyos-AAAA-MM-DD.tar.zst` | **Todas las configuraciones** comprimidas | **No**, es un comprimido de Linux |

| Doc | Tema |
| --- | --- |
| `01-hyprland-escritorios-monitores.md` | Escritorios, ventanas, todos los atajos, monitores, tema visual |
| `02-dictado-lectura-servicios.md` | Dictado por voz, lectura en voz alta, servicios automáticos, Drive |
| `03-teclado-mouse-entrada.md` | Teclado K380, mouse M720, Bluetooth, touchpad, táctil de la Surface |
| `04-apps-paquetes.md` | Apps que usas, apps por defecto, backups, mpv, comando de instalación |
| `05-sistema-base.md` | Qué elegir al instalar CachyOS |
| `06-estudio-descargar-doblar-capturas.md` | Descargar videos y cursos, doblar inglés→español, **capturas + apuntes automáticos de cursos**, sesión de curso |
| `07-uso-y-novedades.md` | Qué usas más, línea de tiempo de lo que se fue creando, botones de los Stream Deck |
| `08-windows11-zenbook.md` | Portar todo a Windows 11 en la Zenbook Pro Duo 15 OLED UX582: qué se puede, cómo y qué conviene |

**¿Por qué el `.tar.zst` no se abre?** Es como un `.zip`, pero de Linux. Va comprimido porque Drive estropea algunos archivos de configuración si se suben sueltos. En la laptop, Claude lo descarga y lo descomprime.

**Para revisarlo por dentro:** en esta PC ya está descomprimido en `~/migracion-cachyos/` (ábrelo con Dolphin). Para ver la lista de archivos del comprimido sin extraerlo:

```
tar --zstd -tf migracion-cachyos-*.tar.zst | less
```

---

## 2. Tus atajos principales

SUPER = tecla de Windows. La lista completa está en `docs/01`.

### Escritorios (hay 5)

| Atajo | Qué hace |
| --- | --- |
| SUPER+1 a 5 | Ir al escritorio 1 a 5 (en esta PC cambia los dos monitores a la vez) |
| SUPER+CTRL+←/→ o SUPER+rueda | Escritorio anterior / siguiente |
| SUPER+Tab | Pasar entre las ventanas del escritorio actual |
| SUPER+S | Mostrar u ocultar el espacio oculto (scratchpad) |

Uso de los escritorios: **1** redes · **2** entretenimiento · **3** estudio · **4** práctica (VS Code) · **5** Claude y terminal.

### Ventanas

| Atajo | Qué hace |
| --- | --- |
| SUPER+Q | Cerrar ventana |
| SUPER+F / SUPER+D | Pantalla completa / maximizar |
| SUPER+ALT+Espacio | Ventana flotante |
| SUPER+flechas | Cambiar de ventana |
| SUPER+SHIFT+flechas | Mover la ventana |
| ALT+Tab | Siguiente ventana |

### Abrir apps

| Atajo | App |
| --- | --- |
| SUPER+Enter / E / W | Terminal (kitty) / Archivos (Dolphin) / Brave |
| SUPER+N / G | Obsidian / VS Code |
| SUPER+T | TikTok |
| SUPER+ALT+Q / W / T / F / I / D | YouTube / WhatsApp / Telegram / Facebook / Instagram / Drive |
| SUPER+C / SUPER+ALT+C | Abrir el curso / configurar el curso |
| SUPER (tocar y soltar) | Buscador de apps |
| SUPER+V / SUPER+L | Historial del portapapeles / bloquear pantalla |

### Capturas, voz y dictado

| Atajo | Qué hace |
| --- | --- |
| Impr / SUPER+Impr | Captura de una zona / de toda la pantalla, con editor |
| SUPER+SHIFT+S | Captura de una zona, solo al portapapeles |
| CTRL+SHIFT+S | Captura de una zona, guardada en archivo |
| SUPER+ALT+S | Auto-captura **en vivo** del monitor activo (guarda solo cuando cambia la pantalla; otra vez = parar) |
| SUPER+ALT+Y | Capturas + apuntes del **link de YouTube copiado** (video o playlist entera) |
| SUPER+ALT+A | Capturas + apuntes de un **curso descargado entero** (eliges la carpeta) |
| SUPER+R | Leer en voz alta el texto seleccionado (se corta apretando otra vez) |
| SUPER+ALT+R | Elegir la voz de lectura |
| SUPER+ALT+Z / SUPER+ALT+X | Dictado en español / en inglés (apretar otra vez = terminar) |

### Mouse Logitech M720

| Botón | Qué hace |
| --- | --- |
| Botón del pulgar | Captura al portapapeles (= SUPER+SHIFT+S) |
| Clic de la rueda | Captura guardada en archivo (= CTRL+SHIFT+S) |
| Inclinar la rueda a los lados | Cambiar de pestaña |

### Reproductor de video (mpv)

| Atajo | Qué hace |
| --- | --- |
| ← / → | Retroceder / adelantar 5 s |
| Ctrl+← / → | Retroceder / adelantar **10 s** |
| Alt+← / → | Retroceder / adelantar **30 s** |
| Espacio | Pausa |
| ] / [ | Más / menos velocidad |
| b / 1 a 9 | Marcar un punto / saltar a una marca |
| q | Salir recordando el minuto |

Guía completa de mpv: `~/.config/mpv/GUIA-MPV.md`.

---

## 2b. Funcionalidades de estudio

Detalle completo en `docs/06`.

| Funcionalidad | Cómo se usa | Qué hace |
| --- | --- | --- |
| **Descargar** | `descargar <link>` en la terminal (`--mp3` = solo audio) | Baja videos, playlists o cursos completos con yt-dlp usando tu sesión de Brave. Guarda en `~/Vídeos/Descargas`, numerado, y sigue donde quedó si se corta |
| **Doblar** | `doblar <video o carpeta>` (`--seguir` dobla a medida que se descarga) | Inglés → español en 4 pasos: transcribe (Whisper), traduce (NLLB, local), pone voz (edge-tts, necesita internet) y mezcla. Queda un video con audio español + inglés y 2 subtítulos. **Ojo: borra el original por defecto** |
| **Apuntes automáticos de cursos** | SUPER+ALT+Y (link de YouTube o playlist) · SUPER+ALT+A (curso descargado) | Saca las capturas sin reproducir el video y arma por clase `apuntes.md` (cuadernillo), `resumen.md` (repaso de 5 min) y `tarjetas.md` (repaso espaciado en Obsidian), con Claude Sonnet. Varios pedidos se ponen **en cola**; una barrita abajo a la derecha muestra el avance. ~10 min por hora de video |
| **Auto-captura en vivo** | SUPER+ALT+S (otra vez = parar) | Captura el monitor activo solo cuando la pantalla cambia (Udemy, Platzi…) |
| **Mis cursos** | `~/Vídeos/Mis cursos.md` (en Obsidian) | Todos tus cursos con casillas para tildar lo estudiado |
| **Video a capturas** | `video-a-capturas.sh <link o archivo>` | Lo mismo desde la terminal; capturas `0001.webp`, `0002.webp`… |
| **Capturas manuales** | Impr, SUPER+SHIFT+S, CTRL+SHIFT+S, botón del pulgar del M720 | Ver sección 2 |
| **Sesión de curso** | SUPER+C / SUPER+ALT+C | Abre el curso y los apuntes |
| **Pomodoro** | Tecla 9 del Stream Dock | Temporizador de estudio |

Guía completa en lenguaje simple: `guias-usuario/Guia-Auto-captura-de-cursos.md`.

**En la laptop:** los apuntes funcionan igual (no usan la tarjeta de video); la barrita, que en esta PC va en el monitor vertical, aparecerá en la pantalla de la laptop (o en la Arzopa si está conectada por HDMI). Hay que iniciar sesión en Claude Code. `doblar` va por el procesador. Tiempo estimado por hora de video (no medido aún): ThinkPad 25–35 min, Surface 45–70 min (25–40 con el modelo `base`). Mejor doblar un video a la vez.

## 3. Qué cambia en las laptops

Casi todo se copia igual; lo único que cambia es lo que depende del hardware de esta PC. Esta PC tiene 2 monitores y una tarjeta NVIDIA; las laptops tienen 1 pantalla y gráficos Intel.

| Tema | En esta PC | En la laptop |
| --- | --- | --- |
| Gráficos | NVIDIA GTX 980 | Intel. Se quitan los ajustes de NVIDIA y se instala el driver de Intel |
| Pantallas | 2 monitores (horizontal y vertical) | Normalmente solo la pantalla de la laptop |
| Escritorios | Cada escritorio usa los 2 monitores | Solo la laptop: todo en su pantalla, con un atajo para ver la "mitad secundaria" (chats, Drive). Con la Arzopa: igual que esta PC |
| Tamaño de la imagen | Normal | Surface: escala 2 (1.75 no funciona en su pantalla). ThinkPad: 1 o 1.25 |
| Touchpad | No hay | Activar tocar para hacer clic y el desplazamiento natural |
| Barra (Noctalia) | Sin batería, con temperatura de la GPU | Se agrega el indicador de batería |
| Micrófono del dictado | Maono USB | El micrófono interno de la laptop |

- **Monitor Arzopa:** tu monitor vertical se llama `HDMI-A-1`, y la Arzopa por HDMI tendrá ese mismo nombre. Si la config se copia sin ajustar, la Arzopa saldría **girada 90°**. Las instrucciones para Claude le piden borrar ese archivo primero.
- **Gesto peligroso en el touchpad:** tres dedos hacia abajo **cierra la ventana**. En esta PC nunca se usó porque no hay touchpad; en la laptop conviene cambiarlo.
- **Surface Pro 6:** para que el táctil y el lápiz funcionen al 100% hace falta el kernel **linux-surface**, que no viene en CachyOS y se agrega aparte.

---

## 4. Apps: cuáles se instalan y cuáles sobran

En la laptop solo se instalan las apps que usas. No desinstalé nada en esta PC.

| Uso | La que usas (se instala) | Sobran (puedes desinstalarlas) |
| --- | --- | --- |
| Navegador y PDF | Brave | Firefox |
| Fotos | Gwenview | imv, geeqie |
| Video | mpv | vlc-plugins-all |
| Visor de PDF | Brave | Okular |
| Terminal | kitty | Alacritty |
| Archivos | Dolphin | — |
| Notas / código / oficina | Obsidian, VS Code, LibreOffice | — |
| Otras | Claude, KeePassXC, LocalSend, OBS, RustDesk | — |

**Dudosas (dime si las quieres en la laptop):** GIMP y Kdenlive (usados una sola vez en agosto), Xournal++ (sirve para escribir con el lápiz de la Surface), OpenDeck (Stream Deck), Docker, Android Studio, meld, opencode.

Para desinstalar las que sobran en esta PC (probado en simulación: solo se lleva dependencias que ninguna otra app usa):

```
sudo pacman -Rns firefox imv geeqie okular alacritty vlc-plugins-all
```

---

## 5. Pasos en la laptop

Tú solo instalas CachyOS y abres Claude Code; del resto se encarga Claude leyendo el README.

1. **Instala CachyOS** con: escritorio **Hyprland (Noctalia)**, arranque **Limine**, disco **btrfs**, idioma español (Bolivia).
2. **Instala Claude Code** e inicia sesión.
3. **Dile a Claude:** "Baja la carpeta migracion-cachyos-hyprland de mi Drive (LaptopPcOptimizaciones), lee el README y pasa mi configuración a esta laptop".
4. **Claude hará esto:**
    - Instalará el driver de Intel y solo las apps que usas.
    - Ajustará la config para la laptop antes de copiarla (quitar NVIDIA, una sola pantalla, escala, touchpad, batería).
    - Te propondrá cómo manejar los escritorios con y sin la Arzopa, y lo aplicará cuando estés de acuerdo.
    - Te hará las preguntas pendientes de la sección 6.
5. **Datos que tendrás que darle:** la contraseña del backup (restic) y los inicios de sesión de Google Drive (rclone), GitHub y Brave. Por seguridad **no** están en el paquete.
6. **Pruebas finales:** cambiar de escritorio con y sin la Arzopa, leer en voz alta con SUPER+R, dictar, los botones del mouse y un video en mpv.

---

## 6. Lo que falta decidir y problemas en esta PC

### Decisiones pendientes

- [ ] **Teclado:** Hyprland está en distribución `us` (inglés). ¿Los teclados de la ThinkPad y de la Surface tienen ñ (español)?
- [ ] **Apps dudosas:** cuáles quieres en la laptop (sección 4).
- [ ] **Surface:** ¿instalar linux-surface para el táctil y el lápiz completos?

### Ya resuelto (26-09)

- **Dictado:** pasó a SUPER+ALT+Z (español) y SUPER+ALT+X (inglés). Drive e Instagram se quedan en SUPER+ALT+D / SUPER+ALT+I.
- **Backup (restic):** ya no respalda `~/GoogleDrive` y se quitaron los bloqueos viejos.
- **Extensiones de VS Code:** se restauran solas al iniciar sesión con GitHub (Settings Sync activo).
- **CTRL+SHIFT+D:** se queda así; no usas ese atajo en VS Code ni en Brave.

### Problemas por arreglar

| Problema | Qué pasa | Arreglo |
| --- | --- | --- |
| SUPER+C (curso) | El script usa un comando viejo; probablemente no te lleva al escritorio de estudio | Actualizar una línea del script |
| Conexión a Drive (rclone) | Usa una clave compartida que rclone retira durante 2026 | Crear tu propia clave de Google |
| **Tesis `~/Proyectos/Ciego`** | Git **sin copia remota**: solo existe en esta PC (y el backup está roto) | **Urgente:** subirla a un repo privado de GitHub antes de migrar |
| Carpeta de capturas | Apunta al disco externo SuperYafer; sin el disco, CTRL+SHIFT+S falla sin avisar | Ruta local o respaldo automático a `~/Imágenes/Capturas` |
| Claude Code duplicado | Hay uno viejo en `/usr/bin/claude` (npm) tapado por el nuevo en `~/.local/bin` | `sudo npm rm -g @anthropic-ai/claude-code` |

## 7. Segundo cerebro en Obsidian

Todo el paquete sirve también como bóveda de Obsidian: son notas markdown con etiquetas y enlaces entre sí.

1. Obsidian → **Abrir carpeta como bóveda** → `~/migracion-cachyos`.
2. Empieza por **`INICIO.md`**: ahí están enlazadas todas las funcionalidades, atajos y docs.
3. Las carpetas técnicas (`dotfiles/`, `system/`, `solo-esta-pc/`) están ocultas en la búsqueda para no ensuciar.
4. Cuando cambies algo en esta PC, pídele a Claude que actualice la nota y vuelva a subir a Drive.
