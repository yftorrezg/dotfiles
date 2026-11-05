# 🖱️ MX Master 4 · Botones, gestos y anillo

> Todo lo que hace el mouse: cada botón, cada gesto por programa y el anillo radial. Este documento se genera solo con `mx-doc.py`.

## 🧭 Resumen en 30 segundos

| Control | Dónde está | Qué hace | Alcance |
|---|---|---|---|
| Rueda | Clic central | Pantalla y escritorios | Global |
| Superior | Botón plano detrás de la rueda | Abrir IAs | Global |
| Gestos | Apoyo del pulgar | Acciones del programa con foco | Por programa |
| Atrás | Lateral | Navegar | Por programa |
| Adelante | Lateral | Pestañas y vistas | Por programa |
| Panel háptico | Panel con puntitos | **Anillo radial** de 12 acciones | Por programa |
| Rueda del pulgar | Rueda horizontal | Según el programa | Por programa |

🧠 Concepto: **global** = hace lo mismo en cualquier ventana. **Por programa** = el mouse mira qué ventana tiene el foco y cambia lo que hace.

## 🤏 Cómo se usa un botón de gestos
Sirve para Rueda, Superior, Gestos, Atrás y Adelante. Cada uno tiene **5 acciones**: clic y 4 direcciones.

1. **Clic**: pulsa y suelta sin mover el mouse.
2. **Gesto**: mantén el botón, mueve el mouse unos 2 cm hacia arriba, abajo, izquierda o derecha y suelta.
3. Las diagonales no hacen nada.

💡 Consejo: no hace falta un gesto largo; con 2 cm basta. Si mueves poco, cuenta como clic.

## 🌐 Botones globales (iguales en todo)

| Botón | Clic | ↑ Arriba | ↓ Abajo | ← Izquierda | → Derecha |
|---|---|---|---|---|---|
| Rueda | Captura al portapapeles `Super+Shift+S` | Pantalla completa `Super+F` | Cerrar ventana `Super+Q` | Escritorio anterior `Super+Ctrl+←` | Escritorio siguiente `Super+Ctrl+→` |
| Superior | Esc | Gemini + ChatGPT (las 2) | Dictado (SUPER+ALT+Z) | Claude | DeepSeek |

📌 Nota: las IAs se abren como ventana de app de Brave; si ya está abierta, la enfoca en vez de abrir otra.

## 📱 Gestos, Atrás y Adelante por programa
El botón **Gestos** es el que cambia más: cada programa tiene sus 5 acciones más útiles. Atrás y Adelante también cambian.

### 🦁 Brave

| Botón | Clic | ↑ Arriba | ↓ Abajo | ← Izquierda | → Derecha |
|---|---|---|---|---|---|
| Gestos | Reabrir pestaña `Ctrl+Shift+T` | Nueva pestaña `Ctrl+T` | Cerrar pestaña `Ctrl+W` | Buscar pestaña `Ctrl+Shift+A` | Curso de estudio (Udemy) |
| Atrás | Atrás `Alt+←` | Seleccionar todo `Ctrl+A` | Enter | Copiar `Ctrl+C` | Pegar `Ctrl+V` |
| Adelante | Adelante `Alt+→` | Barra de direcciones `Ctrl+L` | Añadir a marcadores `Ctrl+D` | Recargar `F5` | Buscar en la página `Ctrl+F` |

- `Rueda del pulgar` :: Pestaña anterior (`Ctrl+Re Pág`) / Pestaña siguiente (`Ctrl+Av Pág`)

### 💬 WhatsApp

| Botón | Clic | ↑ Arriba | ↓ Abajo | ← Izquierda | → Derecha |
|---|---|---|---|---|---|
| Gestos | Buscar chat `Ctrl+Alt+/` | Perfil `Ctrl+Alt+P` | Volumen − | Pista anterior | Pista siguiente |
| Atrás | Esc | Chat anterior `Ctrl+Alt+Shift+[` | Chat siguiente `Ctrl+Alt+Shift+]` | Esc | Buscar `Ctrl+Alt+/` |
| Adelante | Chat nuevo `Ctrl+Alt+N` | Fijar chat `Ctrl+Alt+Shift+P` | Archivar chat `Ctrl+Alt+Shift+E` | Silenciar chat `Ctrl+Alt+Shift+M` | Marcar no leído `Ctrl+Alt+Shift+U` |

- `Rueda del pulgar` :: Chat anterior (`Ctrl+Alt+Shift+[`) / Chat siguiente (`Ctrl+Alt+Shift+]`)

### 🎬 mpv

| Botón | Clic | ↑ Arriba | ↓ Abajo | ← Izquierda | → Derecha |
|---|---|---|---|---|---|
| Gestos | Pausa / play `Espacio` | Poner marca `B` | Ir a la marca `N` | Lista de videos `Tab` | Panel de notas `H` |
| Atrás | Video anterior | +30 s `Alt+→` | −30 s `Alt+←` | −10 s `Ctrl+←` | +10 s `Ctrl+→` |
| Adelante | Video siguiente | Velocidad x2 | Velocidad x1.5 `W` | Velocidad +0.1 | Velocidad −0.1 |

- `Rueda del pulgar` :: −5 s (`←`) / +5 s (`→`)

### 🖼️ Fotos (Gwenview)

| Botón | Clic | ↑ Arriba | ↓ Abajo | ← Izquierda | → Derecha |
|---|---|---|---|---|---|
| Gestos | Papelera `X` | Redimensionar | Recortar | Rotar izquierda | Rotar derecha |
| Atrás | Deshacer `Ctrl+Z` | Miniaturas | Abrir en ventana nueva `Ctrl+Alt+N` | Copiar `Ctrl+C` | Abrir carpeta contenedora `Ctrl+Alt+O` |
| Adelante | Guardar `Ctrl+S` | Modo foco `S` | Reflejar `M` | Copiar a… `F7` | Mover a… `Ctrl+Alt+M` |

- `Rueda del pulgar` :: Foto anterior (`A`) / Foto siguiente (`D`)

### 📁 Dolphin

| Botón | Clic | ↑ Arriba | ↓ Abajo | ← Izquierda | → Derecha |
|---|---|---|---|---|---|
| Gestos | Carpeta nueva `Ctrl+Shift+N` | Dividir vista `F3` | Mostrar ocultos `Alt+.` | Ordenar por nombre `Ctrl+Alt+N` | Ordenar por tipo `Ctrl+Alt+T` |
| Atrás | Atrás `Alt+←` | Barra de direcciones `F6` | Carpeta superior `Alt+↑` | Renombrar `F2` | Duplicar `Ctrl+D` |
| Adelante | Adelante `Alt+→` | Nueva pestaña `Ctrl+T` | Cerrar pestaña `Ctrl+W` | Pestaña anterior `Ctrl+Re Pág` | Pestaña siguiente `Ctrl+Av Pág` |

- `Rueda del pulgar` :: Iconos más chicos (`Ctrl+-`) / Iconos más grandes (`Ctrl+=`)

### 🧑‍💻 VS Code

| Botón | Clic | ↑ Arriba | ↓ Abajo | ← Izquierda | → Derecha |
|---|---|---|---|---|---|
| Gestos | Terminal `Ctrl+acento grave` | Paleta de comandos `Ctrl+Shift+P` | Abrir archivo `Ctrl+P` | Barra lateral `Ctrl+B` | Dividir editor `Ctrl+\` |
| Atrás | Atrás (navegación) `Ctrl+Alt+-` | Ir a definición `F12` | Ver definición (peek) `Alt+F12` | Referencias `Shift+F12` | Adelante (navegación) `Ctrl+Shift+-` |
| Adelante | Depurar: continuar `F5` | Punto de interrupción `F9` | Paso sobre `F10` | Paso dentro `F11` | Paso fuera `Shift+F11` |

- `Rueda del pulgar` :: Pestaña anterior (`Ctrl+Re Pág`) / Pestaña siguiente (`Ctrl+Av Pág`)

### 📓 Obsidian

| Botón | Clic | ↑ Arriba | ↓ Abajo | ← Izquierda | → Derecha |
|---|---|---|---|---|---|
| Gestos | Deshacer `Ctrl+Z` | Fila encima `Ctrl+Alt+Shift+↑` | Fila debajo `Ctrl+Alt+Shift+↓` | Columna a la izquierda `Ctrl+Alt+Shift+←` | Columna a la derecha `Ctrl+Alt+Shift+→` |
| Atrás | Atrás (historial) | Mover fila arriba `Ctrl+Alt+Shift+Re Pág` | Mover fila abajo `Ctrl+Alt+Shift+Av Pág` | Mover columna izquierda `Ctrl+Alt+Shift+Inicio` | Mover columna derecha `Ctrl+Alt+Shift+Fin` |
| Adelante | Adelante (historial) | Borrar fila `Ctrl+Alt+Shift+Retroceso` | Borrar columna `Ctrl+Alt+Shift+Supr` | Duplicar fila `Ctrl+Alt+Shift+D` | Duplicar columna `Ctrl+Alt+Shift+C` |

- `Rueda del pulgar` :: Pestaña anterior (`Ctrl+Shift+Tab`) / Pestaña siguiente (`Ctrl+Tab`)

### ⌨️ Terminal (shell)

| Botón | Clic | ↑ Arriba | ↓ Abajo | ← Izquierda | → Derecha |
|---|---|---|---|---|---|
| Gestos | Interrumpir `Ctrl+C` | Historial (fzf) `Ctrl+R` | Limpiar `Ctrl+L` | Borrar línea `Ctrl+U` | Último argumento `Alt+.` |
| Atrás | Directorio anterior `Alt+←` | Copiar `Ctrl+Shift+C` | Pegar `Ctrl+Shift+V` | Borrar palabra `Ctrl+W` | Anteponer sudo `Alt+S` |
| Adelante | Directorio siguiente `Alt+→` | Pestaña nueva `Ctrl+Shift+T` | Cerrar pestaña `Ctrl+Shift+Q` | Pestaña anterior `Ctrl+Shift+←` | Pestaña siguiente `Ctrl+Shift+→` |

- `Rueda del pulgar` :: Prompt anterior (`Ctrl+Shift+Z`) / Prompt siguiente (`Ctrl+Shift+X`)

### ✳️ Claude Code

| Botón | Clic | ↑ Arriba | ↓ Abajo | ← Izquierda | → Derecha |
|---|---|---|---|---|---|
| Gestos | Cambiar modo (editar / plan) `Shift+Tab` | Transcript `Ctrl+O` | Pasar a segundo plano `Ctrl+B` | Cambiar modelo `Alt+P` | Checklist de tareas `Ctrl+T` |
| Atrás | Pegar imagen `Ctrl+V` | Editar prompt en editor `Ctrl+G` | Pegar texto `Ctrl+Shift+V` | Borrar línea `Ctrl+U` | Guardar borrador `Ctrl+S` |
| Adelante | Último mensaje `Ctrl+Fin` | Inicio de la conversación `Ctrl+Inicio` | Redibujar `Ctrl+L` | Rewind (Esc Esc) | Enviar cola ya `Ctrl+Enter` |

- `Rueda del pulgar` :: Subir (media pantalla) (`Re Pág`) / Bajar (media pantalla) (`Av Pág`)

### 🤖 opencode

| Botón | Clic | ↑ Arriba | ↓ Abajo | ← Izquierda | → Derecha |
|---|---|---|---|---|---|
| Gestos | Agente build / plan `Tab` | Variante de esfuerzo `Ctrl+T` | Paleta de comandos `Ctrl+P` | Modelo reciente `F2` | Agente anterior `Shift+Tab` |
| Atrás | Deshacer mensaje `Ctrl+X → U` | Pegar imagen `Ctrl+V` | Pegar texto `Ctrl+Shift+V` | Borrar línea `Ctrl+U` | Editor externo `Ctrl+X → E` |
| Adelante | Rehacer `Ctrl+X → R` | Primer mensaje `Ctrl+G` | Último mensaje `Ctrl+Alt+G` | Barra lateral `Ctrl+X → B` | Línea de tiempo `Ctrl+X → G` |

- `Rueda del pulgar` :: Subir (media pantalla) (`Re Pág`) / Bajar (media pantalla) (`Av Pág`)

### 🧰 Resto de programas

Lo que no tiene perfil propio usa esto (también Telegram, terminal, VS Code y YouTube para estos botones; su anillo sí es propio).

| Botón | Clic | ↑ Arriba | ↓ Abajo | ← Izquierda | → Derecha |
|---|---|---|---|---|---|
| Gestos | Play / pausa | Volumen + | Volumen − | Pista anterior | Pista siguiente |
| Atrás | Atrás (nativo) | Inicio | Fin | Atrás `Alt+←` | Adelante `Alt+→` |
| Adelante | Adelante (nativo) | Nueva pestaña `Ctrl+T` | Cerrar pestaña `Ctrl+W` | Pestaña anterior `Ctrl+Shift+Tab` | Pestaña siguiente `Ctrl+Tab` |

- `Rueda del pulgar` :: Volumen − (`Vol −`) / Volumen + (`Vol +`)

⚠️ Cuidado: los atajos de WhatsApp (fijar, archivar, silenciar, no leído) son los oficiales de WhatsApp Web; si alguno no responde, se corrige en `mx-accion.py`.

## 🎯 El anillo radial (panel háptico)

### ¿Qué es?
Un anillo de **12 burbujas** que aparece alrededor del cursor al tocar el panel háptico. Las 12 acciones **cambian según el programa**: en WhatsApp salen acciones de chats, en mpv acciones de video, en Dolphin acciones de archivos. Es la forma más rápida de tener a mano decenas de atajos sin memorizarlos.

### Cómo se usa
1. **Toca** el panel háptico (un toque, sin mantener). El anillo aparece y se queda abierto.
2. **Mueve el mouse** hacia una burbuja. No hace falta llegar a ella: cuenta la **dirección**. La elegida crece, se enciende y el mouse vibra suave.
3. **Confirma** con un clic izquierdo o tocando otra vez el panel. Se ejecuta y el anillo se cierra.

Para cerrar sin hacer nada: clic en el centro, clic derecho o 10 segundos sin moverte.

⚡ Modo rápido: **mantén** el panel, apunta hacia la burbuja y suelta. Funciona si lo mantuviste más de 0,35 s; si soltaste antes, cuenta como un toque y el anillo se queda abierto.

### Las 12 posiciones (como un reloj)
Las burbujas se numeran como las horas: **12** arriba, **3** a la derecha, **6** abajo y **9** a la izquierda. En las tablas de abajo, la columna **Hora** dice dónde está cada una. Con el tiempo tu mano aprende «la hora de» las que más usas.

### Sub-opciones (burbujas con un puntito)
Una burbuja con un **puntito** guarda más acciones. Apunta a ella y **aleja más el mouse** en esa misma dirección: salen en un arco por fuera. Elige una y confirma igual que antes. Ejemplo: en Telegram, **Formato** tiene negrita, cursiva, tachado, código, spoiler y enlace.

### Rueda del mouse
- Sobre una burbuja con rueda (columna **Rueda del mouse**) la rueda hace su ajuste: pestañas, zoom, velocidad, chat siguiente…
- En el **centro** (sin elegir nada) la rueda siempre sube o baja el volumen, en cualquier programa.

### Colores y centro
Cada color es un **tipo** de acción, igual en todos los programas:

| Color | Tipo de acción |
|---|---|
| 🔴 Rojo | Cerrar, borrar, bloquear |
| 🟢 Verde | Nuevo, crear, reabrir |
| 🟡 Amarillo | Buscar |
| 🔵 Azul | Moverse, navegar, ir a |
| 🟣 Morado | Multimedia: play, volumen, velocidad |
| 🟠 Naranja | Capturas y fotos |
| 🩷 Rosa | Editar, formato, rotar |
| 🩵 Cian | Vistas, ventanas, pestañas |

El **centro** muestra el logo del programa activo. Al elegir una burbuja muestra su icono y su nombre.

### Si vibra raro o no abre
El sensor del panel es de **fuerza** y puede rebotar (mandar varios toques seguidos); el anillo los filtra (0,14 s). Si en alguna zona del panel no abre, mira la tabla de problemas más abajo.

## 🧩 Qué hay en cada programa (el anillo)
Cada tabla es el anillo de ese programa. «Atajo» es lo que se ejecuta; si pone `noctalia msg …` es un comando del escritorio.

### Sistema (el de cualquier programa sin perfil propio)

| Hora | Acción | Atajo | Sub-opciones (aleja más el mouse) | Rueda del mouse |
|---|---|---|---|---|
| 12 | **Volumen** | `noctalia msg volume-mute` | Silenciar micrófono `noctalia msg mic-mute` · Silenciar `noctalia msg volume-mute` | `↑ noctalia msg volume-up / ↓ noctalia msg volume-down` |
| 1 | **Luz nocturna** | `noctalia msg nightlight-toggle` | — | `↑ noctalia msg brightness-up / ↓ noctalia msg brightness-down` |
| 2 | **Play / pausa** | `noctalia msg media toggle` | Anterior `noctalia msg media previous` · Siguiente `noctalia msg media next` | `↑ noctalia msg media next / ↓ noctalia msg media previous` |
| 3 | **Notificaciones** | `noctalia msg panel-toggle control-center notifications` | No molestar `noctalia msg notification-dnd-toggle` · Abrir la última `noctalia msg notification-invoke-latest` · Limpiar todas `noctalia msg notification-clear-history` | — |
| 4 | **Captura al portapapeles** | `captura-portapapeles.sh` | Captura a carpeta `captura-guardar.sh` · Pantalla completa `noctalia msg screenshot-fullscreen` · Captura y anotar `noctalia msg screenshot-annotate` · Dibujar en pantalla `noctalia msg annotate` | — |
| 5 | **Portapapeles** | `noctalia msg panel-toggle clipboard` | — | — |
| 6 | **Cambiar ventana** | `noctalia msg window-switcher` | Pantalla completa `Super+F` · Flotante `Super+Alt+Espacio` · Girar división `Super+J` · Cerrar ventana `Super+Q` | — |
| 7 | **Archivos** | `Super+E` | — | — |
| 8 | **Terminal** | `Super+Enter` | — | — |
| 9 | **Lanzador** | `noctalia msg panel-toggle launcher` | — | — |
| 10 | **Modo enfoque** | `modo-enfoque.py` | — | — |
| 11 | **Centro de control** | `noctalia msg panel-toggle control-center` | Bloquear `noctalia msg session lock` · Claro / oscuro `noctalia msg theme-mode-toggle` · Fondo siguiente `noctalia msg wallpaper-next` · Cafeína (no suspender) `noctalia msg caffeine-toggle` · Ajustes del mouse `solaar` | — |

### YouTube (también en las pestañas de Brave con YouTube)

| Hora | Acción | Atajo | Sub-opciones (aleja más el mouse) | Rueda del mouse |
|---|---|---|---|---|
| 12 | **Play / pausa** | `K` | — | — |
| 1 | **+10 s** | `L` | — | `↑ L / ↓ J` |
| 2 | **Más rápido** | `D` | Más lento `S` · Velocidad normal `R` · Velocidad preferida `G` · Mostrar control `V` | `↑ D / ↓ S` |
| 3 | **Pantalla completa** | `F` | Modo cine `T` · Miniplayer `I` | — |
| 4 | **Subtítulos** | `C` | — | — |
| 5 | **Siguiente video** | `Shift+N` | Video anterior `Shift+P` | — |
| 6 | **-10 s** | `J` | — | — |
| 7 | **Silenciar** | `M` | — | — |
| 8 | **Ir a…** | `0` | Inicio `0` · Mitad `5` · 90 % `9` | — |
| 9 | **Buscar** | `/` | — | — |
| 10 | **Capturas del video** | `youtube-capturas.sh` | — | — |
| 11 | **Atrás** | `Alt+←` | — | — |

### WhatsApp

| Hora | Acción | Atajo | Sub-opciones (aleja más el mouse) | Rueda del mouse |
|---|---|---|---|---|
| 12 | **Nuevo chat** | `Ctrl+Alt+N` | Nuevo grupo `Ctrl+Alt+Shift+N` | — |
| 1 | **Chat siguiente** | `Ctrl+Alt+Shift+]` | — | `↑ Ctrl+Alt+Shift+[ / ↓ Ctrl+Alt+Shift+]` |
| 2 | **Fijar chat** | `Ctrl+Alt+Shift+P` | — | — |
| 3 | **Silenciar chat** | `Ctrl+Alt+Shift+M` | — | — |
| 4 | **Archivar chat** | `Ctrl+Alt+Shift+E` | — | — |
| 5 | **Marcar no leído** | `Ctrl+Alt+Shift+U` | — | — |
| 6 | **Pegar captura** | `captura de región y pegar → Ctrl+V` | — | — |
| 7 | **Audio más rápido** | `Shift+.` | Audio más lento `Shift+,` | — |
| 8 | **Chat anterior** | `Ctrl+Alt+Shift+[` | — | — |
| 9 | **Buscar chats** | `Ctrl+Alt+/` | Buscar en este chat `Ctrl+Alt+Shift+F` | — |
| 10 | **Cerrar chat** | `Esc` | Eliminar chat `Ctrl+Alt+Retroceso` | — |
| 11 | **Perfil** | `Ctrl+Alt+P` | Ajustes `Ctrl+Alt+,` | — |

### Telegram

| Hora | Acción | Atajo | Sub-opciones (aleja más el mouse) | Rueda del mouse |
|---|---|---|---|---|
| 12 | **Buscar** | `Ctrl+F` | — | — |
| 1 | **Chat siguiente** | `Alt+↓` | — | `↑ Alt+↑ / ↓ Alt+↓` |
| 2 | **Mensajes guardados** | `Ctrl+0` | — | — |
| 3 | **Carpeta siguiente** | `Ctrl+Shift+↓` | Carpeta 1 `Ctrl+1` · Carpeta 2 `Ctrl+2` · Carpeta 3 `Ctrl+3` · Carpeta 4 `Ctrl+4` | `↑ Ctrl+Shift+↑ / ↓ Ctrl+Shift+↓` |
| 4 | **Archivados** | `Ctrl+9` | — | — |
| 5 | **Marcar leído** | `Ctrl+R` | — | — |
| 6 | **Pegar captura** | `captura de región y pegar → Ctrl+V` | — | — |
| 7 | **Formato** | `Ctrl+B` | Negrita `Ctrl+B` · Cursiva `Ctrl+I` · Tachado `Ctrl+Shift+X` · Código `Ctrl+Shift+M` · Spoiler `Ctrl+Shift+P` · Enlace `Ctrl+K` | — |
| 8 | **Chat anterior** | `Alt+↑` | — | — |
| 9 | **Responder último** | `Ctrl+↑` | Editar mi último `↑` | — |
| 10 | **Contactos** | `Ctrl+J` | — | — |
| 11 | **Bloquear** | `Ctrl+L` | Minimizar `Ctrl+M` · Cerrar ventana `Ctrl+W` | — |

### Brave

| Hora | Acción | Atajo | Sub-opciones (aleja más el mouse) | Rueda del mouse |
|---|---|---|---|---|
| 12 | **Nueva pestaña** | `Ctrl+T` | — | — |
| 1 | **Pestaña siguiente** | `Ctrl+Tab` | Pestaña anterior `Ctrl+Shift+Tab` · Duplicar pestaña `Ctrl+L → Alt+Enter` · Última pestaña `Ctrl+9` | `↑ Ctrl+Shift+Tab / ↓ Ctrl+Tab` |
| 2 | **Recargar** | `F5` | Recargar sin caché `Ctrl+Shift+R` · Detener carga `Esc` | — |
| 3 | **Buscar en la página** | `Ctrl+F` | — | — |
| 4 | **Zoom normal** | `Ctrl+0` | — | `↑ Ctrl+= / ↓ Ctrl+-` |
| 5 | **Guardar en marcadores** | `Ctrl+D` | Marcadores `Ctrl+Shift+O` · Historial `Ctrl+H` · Descargas `Ctrl+J` · Imprimir / PDF `Ctrl+P` | — |
| 6 | **Cerrar pestaña** | `Ctrl+W` | — | — |
| 7 | **Reabrir pestaña** | `Ctrl+Shift+T` | — | — |
| 8 | **Atrás** | `Alt+←` | Adelante `Alt+→` · Inicio `Alt+Inicio` | — |
| 9 | **Buscar pestaña** | `Ctrl+Shift+A` | — | — |
| 10 | **Barra de direcciones** | `Ctrl+L` | — | — |
| 11 | **Herramientas** | `Ctrl+Shift+I` | Ventana privada `Ctrl+Shift+N` · Ver código fuente `Ctrl+U` · Borrar datos `Ctrl+Shift+Supr` · Barra de marcadores `Ctrl+Shift+B` | — |

### mpv

| Hora | Acción | Atajo | Sub-opciones (aleja más el mouse) | Rueda del mouse |
|---|---|---|---|---|
| 12 | **Play / pausa** | `Espacio` | — | — |
| 1 | **+10 s** | `Ctrl+→` | — | `↑ → / ↓ ←` |
| 2 | **Velocidad 2x** | `E` | Velocidad 1.5x `W` · +0.1 `D` · -0.1 `A` · Velocidad normal `Retroceso` | `↑ D / ↓ A` |
| 3 | **Pantalla completa** | `F` | — | — |
| 4 | **Poner marca** | `B` | Ir a la marca `N` · Capítulos y marcas `Shift+C` · Marca siguiente `Re Pág` · Marca anterior `Av Pág` | — |
| 5 | **Lista de videos** | `Tab` | — | — |
| 6 | **-10 s** | `Ctrl+←` | — | — |
| 7 | **Notas** | `H` | — | — |
| 8 | **Siguiente video** | `Shift+N` | Video anterior `Shift+P` | — |
| 9 | **Saltos** | `Alt+→` | +30 s `Alt+→` · -30 s `Alt+←` · Deshacer salto `Ctrl+Z` · Al inicio `Inicio` | — |
| 10 | **Captura** | `S` | — | `↑ ↑ / ↓ ↓` |
| 11 | **Abrir archivo** | `Ctrl+O` | — | — |

### Dolphin

| Hora | Acción | Atajo | Sub-opciones (aleja más el mouse) | Rueda del mouse |
|---|---|---|---|---|
| 12 | **Carpeta nueva** | `Ctrl+Shift+N` | — | — |
| 1 | **Renombrar** | `F2` | — | — |
| 2 | **Dividir vista** | `F3` | — | — |
| 3 | **Buscar** | `Ctrl+F` | Filtrar `Ctrl+I` | — |
| 4 | **Nueva pestaña** | `Ctrl+T` | Pestaña anterior `Ctrl+Re Pág` · Pestaña siguiente `Ctrl+Av Pág` · Cerrar pestaña `Ctrl+W` | `↑ Ctrl+Re Pág / ↓ Ctrl+Av Pág` |
| 5 | **Vista** | `Ctrl+1` | Iconos `Ctrl+1` · Compacta `Ctrl+2` · Detalles `Ctrl+3` · Mostrar ocultos `Alt+.` | `↑ Ctrl+= / ↓ Ctrl+-` |
| 6 | **Carpeta superior** | `Alt+↑` | — | — |
| 7 | **Atrás** | `Alt+←` | Adelante `Alt+→` | — |
| 8 | **Ordenar por nombre** | `Ctrl+Alt+N` | Ordenar por tipo `Ctrl+Alt+T` | — |
| 9 | **Terminal aquí** | `Alt+Shift+F4` | — | — |
| 10 | **Barra de direcciones** | `Ctrl+L` | — | — |
| 11 | **A la papelera** | `Supr` | Deshacer `Ctrl+Z` · Duplicar `Ctrl+D` · Propiedades `Alt+Enter` | — |

### Fotos

| Hora | Acción | Atajo | Sub-opciones (aleja más el mouse) | Rueda del mouse |
|---|---|---|---|---|
| 12 | **Siguiente foto** | `D` | — | `↑ A / ↓ D` |
| 1 | **Rotar derecha** | `E` | — | — |
| 2 | **Recortar** | `C` | — | — |
| 3 | **Ajustar** | `W` | Rellenar `Shift+W` · Tamaño real `Ctrl+0` | — |
| 4 | **Pantalla completa** | `F` | — | — |
| 5 | **A la papelera** | `X` | — | — |
| 6 | **Foto anterior** | `A` | — | — |
| 7 | **Rotar izquierda** | `Q` | — | — |
| 8 | **Editar** | `M` | Reflejar `M` · Redimensionar `R` · Deshacer `Ctrl+Z` · Guardar `Ctrl+S` | — |
| 9 | **Miniaturas** | `T` | Barra lateral `I` · Modo foco `S` | — |
| 10 | **Copiar imagen** | `Ctrl+C` | — | — |
| 11 | **Archivo** | `Ctrl+Alt+O` | Copiar a… `F7` · Mover a… `Ctrl+Alt+M` · Abrir en otra ventana `Ctrl+Alt+N` | — |

### Claude Code

| Hora | Acción | Atajo | Sub-opciones (aleja más el mouse) | Rueda del mouse |
|---|---|---|---|---|
| 12 | **Nueva conversación** | `/clear` | Retomar `/resume` · Ramificar `/branch` · Nombrar sesión `/rename` · Salir `/exit` | — |
| 1 | **Insertar ruta** | `Ctrl+Shift+P → F` | Hash de git `Ctrl+Shift+P → H` · Línea de pantalla `Ctrl+Shift+P → L` · Abrir URL `Ctrl+Shift+E` | — |
| 2 | **Ver cambios** | `/diff` | Revisar `/review` · Seguridad `/security-review` · Simplificar `/simplify` | — |
| 3 | **Captura y pegar** | `captura de región y pegar → Ctrl+V` | — | — |
| 4 | **Copiar respuesta** | `/copy` | Exportar `/export` · Copiar selección `Ctrl+Shift+C` | — |
| 5 | **Permisos** | `/permissions` | Memoria `/memory` · Agentes `/agents` · MCP `/mcp` · Ajustes `/config` | — |
| 6 | **@ Archivo** | `Shift+Apostrophe` | ! Comando `Shift+1` · Buscar prompt `Ctrl+R` · Buscar en conversación `Ctrl+O → /` | — |
| 7 | **Tareas** | `/tasks` | Plan `/plan` · Crear CLAUDE.md `/init` | — |
| 8 | **Esfuerzo** | `/effort` | Modo rápido `Alt+O` · Uso y cuota `/usage` | — |
| 9 | **Compactar** | `/compact` | Contexto `/context` · Pregunta lateral `/btw` | — |
| 10 | **Skills** | `/skills` | Bucle `/loop` | — |
| 11 | **Diagnóstico** | `/doctor` | Estado `/status` · Ayuda `/help` | — |

### opencode

| Hora | Acción | Atajo | Sub-opciones (aleja más el mouse) | Rueda del mouse |
|---|---|---|---|---|
| 12 | **Nueva sesión** | `Ctrl+X → N` | Sesiones `Ctrl+X → L` · Exportar `Ctrl+X → X` | — |
| 1 | **Insertar ruta** | `Ctrl+Shift+P → F` | Hash de git `Ctrl+Shift+P → H` · Línea de pantalla `Ctrl+Shift+P → L` · Abrir URL `Ctrl+Shift+E` | — |
| 2 | **Modelos** | `Ctrl+X → M` | Conectar proveedor `/connect` · Temas `Ctrl+X → T` | — |
| 3 | **Captura y pegar** | `captura de región y pegar → Ctrl+V` | — | — |
| 4 | **Copiar mensaje** | `Ctrl+X → Y` | Copiar selección `Ctrl+Shift+C` | — |
| 5 | **Estado** | `Ctrl+X → S` | Crear AGENTS.md `/init` · Actualizar `/update` | — |
| 6 | **@ Archivo** | `Shift+Apostrophe` | ! Comando `Shift+1` | — |
| 7 | **Detalles de herramientas** | `/details` | Razonamiento `/thinking` | — |
| 8 | **Agentes** | `Ctrl+X → A` | Subagente (hijo) `Ctrl+X → ↓` | — |
| 9 | **Compactar** | `Ctrl+X → C` | Exportar `Ctrl+X → X` | — |
| 10 | **Salir** | `Ctrl+X → Q` | Suspender `Ctrl+Z` | — |
| 11 | **Chuleta de atajos** | `Ctrl+Alt+K` | Ayuda `/help` | — |

### Terminal

| Hora | Acción | Atajo | Sub-opciones (aleja más el mouse) | Rueda del mouse |
|---|---|---|---|---|
| 12 | **Archivo (fzf)** | `Ctrl+T` | Carpeta (fzf) `Alt+C` · Carpeta frecuente `zi` | — |
| 1 | **Insertar ruta** | `Ctrl+Shift+P → F` | Hash de git `Ctrl+Shift+P → H` · Línea de pantalla `Ctrl+Shift+P → L` · Abrir URL `Ctrl+Shift+E` | — |
| 2 | **Git estado** | `git status -sb` | Diff `git diff` · Log `git log --oneline -15` · Pull `git pull` · Push `git push` | — |
| 3 | **Claude Code** | `claude` | Continuar `claude --continue` · opencode `opencode` · opencode continuar `opencode -c` | — |
| 4 | **Salida del último comando** | `Ctrl+Shift+G` | Scrollback completo `Ctrl+Shift+H` | — |
| 5 | **Nueva ventana kitty** | `Ctrl+Shift+Enter` | Siguiente layout `Ctrl+Shift+L` · Redimensionar `Ctrl+Shift+R` · Cerrar ventana `Ctrl+Shift+W` | — |
| 6 | **Editar comando** | `Alt+E` | Inicio de línea `Ctrl+A` · Fin de línea `Ctrl+E` | — |
| 7 | **Suspender** | `Ctrl+Z` | Reanudar (fg) `fg` · Salir (EOF) `Ctrl+D` | — |
| 8 | **Monitor** | `btop` | Contenedores `docker ps` | — |
| 9 | **Reiniciar terminal** | `reset` | Limpiar todo `Ctrl+Shift+Supr` | — |
| 10 | **Letra normal** | `Ctrl+Shift+Retroceso` | Más grande `Ctrl+Shift+=` · Más chica `Ctrl+Shift+-` | `↑ Ctrl+Shift+= / ↓ Ctrl+Shift+-` |
| 11 | **Abrir en Dolphin** | `xdg-open .` | VS Code aquí `code .` | — |

### VS Code

| Hora | Acción | Atajo | Sub-opciones (aleja más el mouse) | Rueda del mouse |
|---|---|---|---|---|
| 12 | **Chat IA** | `Ctrl+Alt+I` | Chat en línea `Ctrl+I` · Ajustes `Ctrl+,` · Atajos `Ctrl+K → Ctrl+S` · Extensiones `Ctrl+Shift+X` · Tareas / Build `Ctrl+Shift+B` | — |
| 1 | **Nueva terminal** | `Ctrl+Shift+acento grave` | Dividir `Ctrl+Shift+5` · Maximizar panel `Ctrl+Alt+M` · Foco terminal `Ctrl+Alt+J` · Terminal siguiente `Ctrl+Alt+Av Pág` · Terminal anterior `Ctrl+Alt+Re Pág` | — |
| 2 | **Explorador** | `Ctrl+Shift+E` | Git `Ctrl+Shift+G` · Depurar `Ctrl+Shift+D` · Problemas `Ctrl+Shift+M` · Revelar archivo `Ctrl+Alt+E` · Salida `Ctrl+Shift+U` | — |
| 3 | **Buscar en proyecto** | `Ctrl+Shift+F` | Reemplazar en proyecto `Ctrl+Shift+H` · Buscar en archivo `Ctrl+F` · Reemplazar en archivo `Ctrl+H` · Siguiente coincidencia `F3` · Anterior coincidencia `Shift+F3` · Regex `Alt+R` | — |
| 4 | **Ir a símbolo** | `Ctrl+Shift+O` | Símbolo en proyecto `Ctrl+T` · Ir a línea `Ctrl+G` · Implementación `Ctrl+F12` · Archivos recientes `Ctrl+R` · Última edición `Ctrl+K → Ctrl+Q` · Corchete par `Ctrl+Shift+\` | `↑ Ctrl+Alt+- / ↓ Ctrl+Shift+-` |
| 5 | **Siguiente problema** | `F8` | Problema anterior `Shift+F8` · Arreglo rápido `Ctrl+.` · Mostrar hover `Ctrl+K → Ctrl+I` · Desplegar todo `Ctrl+K → Ctrl+J` · Plegar todo `Ctrl+K → Ctrl+0` | `↑ Shift+F8 / ↓ F8` |
| 6 | **Parar depuración** | `Shift+F5` | Reiniciar `Ctrl+Shift+F5` · Ejecutar sin depurar `Ctrl+F5` · Consola de depuración `Ctrl+Shift+Y` · Build `Ctrl+Shift+B` | — |
| 7 | **Ejecutar .py** | `Ctrl+Alt+R` | Ejecutar selección en REPL `Shift+Enter` · Organizar imports `Shift+Alt+O` · Elegir intérprete `Ctrl+Alt+Shift+I` · Abrir REPL `Ctrl+Alt+Shift+R` | — |
| 8 | **Multicursor** | `Ctrl+D` | Todas las ocurrencias `Ctrl+Shift+L` · Cursor arriba `Ctrl+Alt+↑` · Cursor abajo `Ctrl+Alt+↓` · Deshacer cursor `Ctrl+U` · Cursores al fin de línea `Shift+Alt+I` · Expandir selección `Shift+Alt+→` | `↑ Ctrl+Alt+↑ / ↓ Ctrl+Alt+↓` |
| 9 | **Formatear** | `Ctrl+Shift+I` | Renombrar símbolo `F2` · Comentar línea `Ctrl+/` · Comentario de bloque `Shift+Alt+A` · Formatear selección `Ctrl+K → Ctrl+F` · Ajuste de línea `Alt+Z` · Quitar espacios finales `Ctrl+K → Ctrl+X` | — |
| 10 | **Mover línea** | `Alt+↓` | Mover arriba `Alt+↑` · Duplicar abajo `Shift+Alt+↓` · Borrar línea `Ctrl+Shift+K` · Línea debajo `Ctrl+Enter` · Línea encima `Ctrl+Shift+Enter` · Seleccionar línea `Ctrl+L` | `↑ Alt+↑ / ↓ Alt+↓` |
| 11 | **Cerrar editor** | `Ctrl+W` | Reabrir `Ctrl+Shift+T` · Cerrar otros `Ctrl+Alt+T` · Anclar pestaña `Ctrl+K → Shift+Enter` · Mover a grupo derecho `Ctrl+K → Ctrl+→` · Foco al editor `Ctrl+1` | — |

### Obsidian

| Hora | Acción | Atajo | Sub-opciones (aleja más el mouse) | Rueda del mouse |
|---|---|---|---|---|
| 12 | **Ir a nota** | `Ctrl+O` | Paleta `Ctrl+P` · Nota nueva `Ctrl+N` · Nota diaria `Ctrl+Alt+7` · Marcadores `Ctrl+Alt+6` · Reabrir pestaña `Ctrl+Alt+R` · Plantilla `Ctrl+Alt+8` | — |
| 1 | **Buscar en el vault** | `Ctrl+Shift+F` | En esta nota `Ctrl+F` · Reemplazar `Ctrl+H` · Etiquetas `Ctrl+Alt+5` | — |
| 2 | **Seleccionar línea** | `Inicio → Shift+Fin` | Copiar línea `Inicio → Shift+Fin → Ctrl+C` · Cortar línea `Inicio → Shift+Fin → Ctrl+X` · Borrar línea `Ctrl+D` · Duplicar línea `Inicio → Shift+Fin → Ctrl+C → Fin → Enter → Ctrl+V` · Pegar sin formato `Ctrl+Shift+V` · Seleccionar todo `Ctrl+A` | `↑ Ctrl+Alt+↑ / ↓ Ctrl+Alt+↓` |
| 3 | **Insertar tabla** | `Ctrl+Alt+T` | Callout `Ctrl+Alt+L` · Bloque de código `Ctrl+Alt+B` · Fórmula `Ctrl+Alt+M` · Enlace [[ ]] `Ctrl+Alt+I` · Cita `Ctrl+Shift+9` · Línea horizontal `- → - → -` | — |
| 4 | **Negrita** | `Ctrl+B` | Cursiva `Ctrl+I` · Resaltar `Ctrl+Alt+H` · Código `Ctrl+Alt+K` · Tachado `Ctrl+Alt+X` · Enlace `Ctrl+K` · Limpiar formato `Ctrl+Alt+C` | — |
| 5 | **Encabezado H2** | `Ctrl+Alt+2` | H1 `Ctrl+Alt+1` · H3 `Ctrl+Alt+3` · H4 `Ctrl+Alt+4` · Texto normal `Ctrl+Alt+0` | — |
| 6 | **Tarea** | `Ctrl+Enter` | Viñetas `Ctrl+Alt+U` · Numerada `Ctrl+Alt+N` · Lista a tarea `Ctrl+Alt+J` · Sangrar `Tab` · Quitar sangría `Shift+Tab` | — |
| 7 | **Lectura / edición** | `Ctrl+E` | Modo fuente `Ctrl+Alt+E` · Ancho legible `Ctrl+Alt+Y` · Panel izquierdo `Ctrl+Alt+V` · Panel derecho `Ctrl+Alt+G` · Plegar todo `Ctrl+Alt+,` · Desplegar todo `Ctrl+Alt+.` | `↑ Ctrl+Alt+[ / ↓ Ctrl+Alt+]` |
| 8 | **Pestaña nueva** | `Ctrl+T` | Cerrar `Ctrl+W` · Reabrir `Ctrl+Alt+R` · Última `Ctrl+9` · Fijar `Ctrl+Alt+P` · Cerrar otras `Ctrl+Alt+O` | `↑ Ctrl+Shift+Tab / ↓ Ctrl+Tab` |
| 9 | **Dividir a la derecha** | `Ctrl+Alt+D` | Dividir abajo `Ctrl+Alt+S` · Cerrar panel `Ctrl+Alt+W` | — |
| 10 | **Backlinks** | `Ctrl+Alt+Q` | Grafo `Ctrl+G` · Grafo local `Ctrl+Alt+Z` · Enlaces salientes `Ctrl+Alt+9` · Esquema `Ctrl+Alt+A` | — |
| 11 | **Repasar esta nota (SR)** | `Ctrl+Alt+4` | Repasar todas `Ctrl+Alt+3` · Cola de repaso `Ctrl+Alt+2` · Siguiente nota a repasar `Ctrl+Alt+1` | — |

## ⚙️ Cómo cambiar cosas

### Qué archivo toca qué

| Archivo | Qué contiene |
|---|---|
| `~/.config/hypr/scripts/mx-accion.py` | Gestos, Atrás, Adelante, Rueda, Superior y rueda del pulgar (tabla `PERFILES`) |
| `~/.config/hypr/scripts/anillo_apps.py` | Las 12 burbujas de cada programa, sub-opciones, colores e iconos |
| `~/.config/hypr/scripts/anillo.py` | El anillo en sí: tamaño, animación, vibración, tiempos |
| `~/.config/hypr/scripts/mx-reglas.py` | Reglas de Solaar (solo si cambian los botones, casi nunca) |
| `~/.config/hypr/scripts/mx-doc.py` | Genera este documento |
| `~/.local/state/mx-accion.log` | Registro de lo que se abre y ejecuta (para depurar) |

### Cómo se escribe una acción

| Escribes | Qué hace | Ejemplo |
|---|---|---|
| `"ctrl+t"` | Pulsa esa combinación | `"ctrl+shift+t"` |
| `["ctrl+l", "alt+return"]` | Varias combinaciones seguidas | duplicar pestaña |
| `("cmd", ["prog", "arg"])` | Ejecuta un programa | `("cmd", ["solaar"])` |
| `NOC("volume-up")` | Comando de Noctalia (volumen, brillo, notificaciones…) | `NOC("brightness-up")` |
| `SH("captura-guardar.sh")` | Script de `~/.config/hypr/scripts` | captura a carpeta |
| `web("claude")` | Abre o enfoca una app web (solo en `mx-accion.py`) | `web("gemini")` |

Las teclas se escriben en minúscula: `ctrl`, `shift`, `alt`, `super`, `return`, `esc`, `tab`, `space`, `left`, `pageup`, `delete`, `slash`, `comma`, `period`, `f1`…`f12`, `0`…`9`. Si usas una tecla nueva y no existe, el test te avisa.

### Receta 1 · Cambiar una burbuja del anillo
Abre `anillo_apps.py`, busca el programa y edita la línea. Cada burbuja es `S(icono, "Nombre", acción, sub=[…], rueda=(subir, bajar))`.

```python
S("browser-plus", "Nueva pestaña", "ctrl+t", color=VERDE),
```

### Receta 2 · Añadir sub-opciones a una burbuja
```python
S("search", "Buscar", "ctrl+f",
  sub=[S("filter", "Filtrar", "ctrl+i"),
       S("replace", "Reemplazar", "ctrl+h")]),
```
Pon entre 1 y 6 sub-opciones; salen abiertas en abanico.

### Receta 3 · Añadir un programa nuevo
1. Enfoca el programa y averigua su **clase**:

```bash
hyprctl activewindow | grep class
```

2. En `anillo_apps.py` copia un perfil (por ejemplo `KITTY`), cámbiale nombre, `logo` y las 12 burbujas.
3. Añádelo a la lista `PERFILES` del final con su clase. El primero que coincide gana, y se puede afinar por título con `"titulo"`.

```python
{"clase": r"^obsidian$", **OBSIDIAN},
```

### Receta 4 · Cambiar un gesto (Gestos, Atrás, Adelante…)
Abre `mx-accion.py`, busca el programa en `PERFILES` y edita la lista `[clic, arriba, abajo, izquierda, derecha]`. `None` = usa la del perfil global. Después actualiza el nombre en `NOMBRES` de `mx-doc.py` para que el documento lo diga bien.

### Receta 5 · Elegir otro icono
Los iconos son de la colección **Tabler** (casi 6000). Busca por palabra:

```bash
grep -i "camera" /usr/share/noctalia/assets/fonts/tabler.json | head
```

Usa el nombre sin más, por ejemplo `"camera"`. El color sale solo del icono; para forzarlo añade `color=ROJO` (colores: `ROJO NARANJA AMARILLO VERDE TURQUESA CIAN AZUL MORADO ROSA BLANCO`).

### Receta 6 · Probar y aplicar
```bash
# comprobar que los iconos y las teclas existen
python3 ~/.config/hypr/scripts/anillo-tests.py

# ver un programa sin tocar el mouse (6 s)
ANILLO_PRUEBA=1 ANILLO_APP=Brave python3 ~/.config/hypr/scripts/anillo.py --demonio

# aplicar los cambios del anillo
pkill -f "[a]nillo.py --demonio"; setsid python3 ~/.config/hypr/scripts/anillo.py --demonio &

# regenerar este documento
python3 ~/.config/hypr/scripts/mx-doc.py
```

Los gestos (`mx-accion.py`) se aplican solos: el archivo se lee en cada gesto.

## 🔧 Problemas típicos

| Síntoma | Causa | Solución |
|---|---|---|
| El anillo no abre | El servicio no corre | Mira el registro; reinícialo con el comando de la receta 6 |
| Abre a veces y a veces no | Rebote del sensor de fuerza del panel | Ya se filtra; si sigue, baja el umbral con `solaar config "MX Master 4" force-sensing N` |
| Una acción no hace nada | Atajo equivocado para ese programa | Abre `~/.local/state/mx-accion.log`, mira qué ejecutó y corrige la tecla |
| Salen mal los iconos | Fuente Tabler no encontrada | Comprueba que existe `/usr/share/noctalia/assets/fonts/noctalia-tabler.ttf` |
| Un gesto no responde | Solaar no corre | Debe estar corriendo (arranca con Hyprland): `solaar -w hide` |

📌 Nota: Solaar no puede guardar perfiles por programa en Wayland, por eso el script pregunta a Hyprland cuál es la ventana activa.

## 🔍 Para optimizar

### Acciones repetidas
Estas acciones están a la vez en el anillo y en un botón. Es duplicar esfuerzo: cambia una de las dos por algo que todavía no tengas a mano.

| Programa | Acción repetida | En el anillo | En el botón |
|---|---|---|---|
| YouTube | `Alt+←` | Atrás (hora 11) | Atrás ← |
| WhatsApp | `Ctrl+Alt+N` | Nuevo chat (hora 12) | Adelante clic |
| WhatsApp | `Ctrl+Alt+Shift+]` | Chat siguiente (hora 1) | Atrás ↓ |
| WhatsApp | `Ctrl+Alt+Shift+P` | Fijar chat (hora 2) | Adelante ↑ |
| WhatsApp | `Ctrl+Alt+Shift+M` | Silenciar chat (hora 3) | Adelante ← |
| WhatsApp | `Ctrl+Alt+Shift+E` | Archivar chat (hora 4) | Adelante ↓ |
| WhatsApp | `Ctrl+Alt+Shift+U` | Marcar no leído (hora 5) | Adelante → |
| WhatsApp | `Ctrl+Alt+Shift+[` | Chat anterior (hora 8) | Atrás ↑ |
| WhatsApp | `Ctrl+Alt+/` | Buscar chats (hora 9) | Gestos clic |
| WhatsApp | `Esc` | Cerrar chat (hora 10) | Atrás clic |
| WhatsApp | `Ctrl+Alt+P` | Perfil (hora 11) | Gestos ↑ |
| Telegram | `Ctrl+W` | Cerrar ventana (hora 11) | Adelante ↓ |
| Brave | `Ctrl+T` | Nueva pestaña (hora 12) | Gestos ↑ |
| Brave | `F5` | Recargar (hora 2) | Adelante ← |
| Brave | `Ctrl+F` | Buscar en la página (hora 3) | Adelante → |
| Brave | `Ctrl+D` | Guardar en marcadores (hora 5) | Adelante ↓ |
| Brave | `Ctrl+W` | Cerrar pestaña (hora 6) | Gestos ↓ |
| Brave | `Ctrl+Shift+T` | Reabrir pestaña (hora 7) | Gestos clic |
| Brave | `Alt+←` | Atrás (hora 8) | Atrás clic |
| Brave | `Alt+→` | Adelante (hora 8) | Adelante clic |
| Brave | `Ctrl+Shift+A` | Buscar pestaña (hora 9) | Gestos ← |
| Brave | `Ctrl+L` | Barra de direcciones (hora 10) | Adelante ↑ |
| mpv | `Espacio` | Play / pausa (hora 12) | Gestos clic |
| mpv | `Ctrl+→` | +10 s (hora 1) | Atrás → |
| mpv | `E` | Velocidad 2x (hora 2) | Adelante ↑ |
| mpv | `W` | Velocidad 1.5x (hora 2) | Adelante ↓ |
| mpv | `D` | +0.1 (hora 2) | Adelante ← |
| mpv | `A` | -0.1 (hora 2) | Adelante → |
| mpv | `B` | Poner marca (hora 4) | Gestos ↑ |
| mpv | `N` | Ir a la marca (hora 4) | Gestos ↓ |
| mpv | `Tab` | Lista de videos (hora 5) | Gestos ← |
| mpv | `Ctrl+←` | -10 s (hora 6) | Atrás ← |
| mpv | `H` | Notas (hora 7) | Gestos → |
| mpv | `Alt+→` | Saltos (hora 9) | Atrás ↑ |
| mpv | `Alt+←` | -30 s (hora 9) | Atrás ↓ |
| Dolphin | `Ctrl+Shift+N` | Carpeta nueva (hora 12) | Gestos clic |
| Dolphin | `F2` | Renombrar (hora 1) | Atrás ← |
| Dolphin | `F3` | Dividir vista (hora 2) | Gestos ↑ |
| Dolphin | `Ctrl+T` | Nueva pestaña (hora 4) | Adelante ↑ |
| Dolphin | `Ctrl+Re Pág` | Pestaña anterior (hora 4) | Adelante ← |
| Dolphin | `Ctrl+Av Pág` | Pestaña siguiente (hora 4) | Adelante → |
| Dolphin | `Ctrl+W` | Cerrar pestaña (hora 4) | Adelante ↓ |
| Dolphin | `Alt+.` | Mostrar ocultos (hora 5) | Gestos ↓ |
| Dolphin | `Alt+↑` | Carpeta superior (hora 6) | Atrás ↓ |
| Dolphin | `Alt+←` | Atrás (hora 7) | Atrás clic |
| Dolphin | `Alt+→` | Adelante (hora 7) | Adelante clic |
| Dolphin | `Ctrl+Alt+N` | Ordenar por nombre (hora 8) | Gestos ← |
| Dolphin | `Ctrl+Alt+T` | Ordenar por tipo (hora 8) | Gestos → |
| Dolphin | `Ctrl+D` | Duplicar (hora 11) | Atrás → |
| Fotos | `E` | Rotar derecha (hora 1) | Gestos → |
| Fotos | `C` | Recortar (hora 2) | Gestos ↓ |
| Fotos | `X` | A la papelera (hora 5) | Gestos clic |
| Fotos | `Q` | Rotar izquierda (hora 7) | Gestos ← |
| Fotos | `M` | Editar (hora 8) | Adelante ↓ |
| Fotos | `R` | Redimensionar (hora 8) | Gestos ↑ |
| Fotos | `Ctrl+Z` | Deshacer (hora 8) | Atrás clic |
| Fotos | `Ctrl+S` | Guardar (hora 8) | Adelante clic |
| Fotos | `T` | Miniaturas (hora 9) | Atrás ↑ |
| Fotos | `S` | Modo foco (hora 9) | Adelante ↑ |
| Fotos | `Ctrl+C` | Copiar imagen (hora 10) | Atrás ← |
| Fotos | `Ctrl+Alt+O` | Archivo (hora 11) | Atrás → |
| Fotos | `F7` | Copiar a… (hora 11) | Adelante ← |
| Fotos | `Ctrl+Alt+M` | Mover a… (hora 11) | Adelante → |
| Fotos | `Ctrl+Alt+N` | Abrir en otra ventana (hora 11) | Atrás ↓ |

### Por revisar
- **WhatsApp · Archivar chat**: dos fuentes dicen `Ctrl+Alt+E` y otras `Ctrl+Alt+Shift+E`; comprueba cuál funciona.
- **Telegram · Carpetas 1 a 4** (`Ctrl+1…4`): en Telegram también fijan chats; si chocan, usa Carpeta siguiente.
- **Brave · Duplicar pestaña**: es la combinación `Ctrl+L` y `Alt+Enter`; si no te gusta, quítala.
- **Gestos globales antiguos** (portapapeles, YouTube, terminal, archivos, WhatsApp): se quitaron de Gestos. Siguen en teclado: `Super+V`, `Super+Alt+Q`, `Super+Enter`, `Super+E`, `Super+Alt+W`.

### Ideas
- Poner en el anillo lo que más usas y quitar lo que no: el anillo cambia con `anillo_apps.py`, sin tocar nada más.
- Pasar al anillo los gestos que casi no usas, y dejar en los gestos solo lo imprescindible.
- Añadir perfiles para Obsidian, el editor de código o cualquier programa que uses a diario.

