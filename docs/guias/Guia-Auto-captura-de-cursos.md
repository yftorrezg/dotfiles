# 📸 Guía: Capturas y apuntes automáticos de cursos

> **En una frase:** la computadora saca capturas **solo cuando aparece algo nuevo** en el curso y arma un **cuadernillo de apuntes** por clase (resumen, conceptos, temas con el código real y ejercicios). Tú te concentras en entender y practicar.

*Actualizado el 29/09/2026 · CachyOS + Hyprland*

---

## 🗺️ Índice

1. [¿Para qué sirve?](#-para-qué-sirve)
2. [Los atajos que tienes que recordar](#️-los-atajos-que-tienes-que-recordar)
3. [📊 ¿Cómo va? La barrita de progreso](#-cómo-va-la-barrita-de-progreso)
4. [🎓 Centro de estudio: cómo estudiar](#-centro-de-estudio-cómo-estudiar-el-flujo-de-todos-los-días)
5. [📓 Los apuntes (cuadernillo)](#-los-apuntes-cuadernillo)
6. [🎓 Curso entero de una vez (SUPER+ALT+A)](#-curso-entero-de-una-vez)
7. [Forma 1: En vivo (YouTube, Udemy, Platzi…)](#-forma-1-en-vivo-mientras-miras-el-curso)
8. [Forma 2: Link de YouTube (sin mirarlo)](#-forma-2-link-de-youtube-sin-mirar-el-video)
9. [Forma 3: Un video descargado](#-forma-3-un-video-que-ya-tienes-descargado)
10. [¿Dónde queda todo?](#-dónde-queda-todo)
11. [¿Cuánto tarda?](#️-cuánto-tarda)
12. [¿Con qué videos funciona bien?](#-con-qué-videos-funciona-bien)
13. [Rutina de estudio recomendada](#-rutina-de-estudio-recomendada)
14. [¿Cómo funciona por dentro?](#-cómo-funciona-por-dentro-para-entenderlo)
15. [Ajustes](#️-ajustes)
16. [Problemas comunes](#-problemas-comunes)
17. [Archivos del sistema y pruebas](#-archivos-del-sistema-y-pruebas)

---

## 🎯 ¿Para qué sirve?

| ❌ Antes | ✅ Ahora |
|---|---|
| Pausar el video para sacar captura | Las capturas se sacan solas |
| Perder el hilo del profe | Te concentras 100 % en entender |
| Volver a ver 5 h de video para repasar | Lees el **cuadernillo** en ~30 min |
| Escribir apuntes a mano | Resumen, conceptos, temas, **código real** y ejercicios listos |
| Capturas repetidas por todos lados | Solo guarda cuando **algo cambia** |

💡 **La idea clave:** no saca una foto cada X segundos a lo loco. **Compara la pantalla** y guarda solo si cambió algo: una línea de código nueva, una variable, un parámetro, una diapositiva.

---

## ⌨️ Los atajos que tienes que recordar

| Atajo | Qué hace | Cuándo usarlo |
|---|---|---|
| **`SUPER + ALT + A`** | 🎓 **Curso entero:** eliges la carpeta → capturas + apuntes de **todas** las clases | Cursos descargados (lo más completo) |
| **`SUPER + ALT + Y`** | 🔗 Capturas + apuntes del **link de YouTube copiado** (video o **playlist entera**) | Videos y cursos de YouTube |
| **`SUPER + ALT + S`** | ▶️ Empieza / ⏹️ termina la captura **en vivo** | Udemy, Platzi o lo que estés mirando |
| `CTRL + SHIFT + S` | ✂️ Captura **manual** de una zona | Un momento puntual que quieres sí o sí |
| **`SUPER + I`** | 🎓 **Centro de estudio:** la próxima clase, con pre-test, apuntes, práctica y tests | Cada vez que te sentás a estudiar |
| `SUPER + ALT + V` | 🧪 **Verificar** los tests de tu práctica → aviso ✅/❌ | Después de resolver ejercicios |

> 🧠 **Truco para acordarte:** **A** = *Apuntes* · **Y** = *YouTube* · **S** = *Screen* (pantalla) · **Z** = *Zona de estudio* · **V** = *Verificar*
>
> 🎛️ **Stream Deck (Mirabox, perfil "Cursos y Dev"):** 🎓 Estudiar · 🧪 Tests · ✅ Terminé · 🃏 Repasar

---

## 📊 ¿Cómo va? La barrita de progreso

Mientras procesa un video, una playlist o un curso, aparece una **barrita fina y semitransparente abajo a la derecha del monitor vertical** (el HP). No toma el foco, los clics pasan de largo y en el monitor principal no aparece nada, así estudias tranquilo:

```
📚 Curso React        3/41 · 📸 120 guardadas · 48% · ~12 min
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬───────────────────────────
```

| Etapa | Qué está haciendo | Parte de la barrita |
|---|---|---|
| 📥 Descargando | Baja el video y los subtítulos (solo YouTube) | 0 → 25 % |
| 📸 Capturas | Recorre el video sacando capturas | 25 → 85 % |
| 🤖 Apuntes | Elige capturas → lee el código (OCR) → Claude arma el resumen | 85 → 100 % |
| ✅ Listo / ❌ Falló | Terminó: dice dónde quedaron los apuntes (o dónde ver el error) | — |

- ⏱️ **"faltan ~N min"** es un cálculo aproximado; en la etapa de Claude puede tardar un poco más.
- 🎓 En un **curso o playlist** dice **"3/41"** (clase actual / total).
- 🎨 La línea es **azul** mientras trabaja, **verde** al terminar y **roja** si falló. Al final se cierra sola y recién ahí llega **una** notificación normal con el resultado.
- 🧱 Si hay dos procesos a la vez, las barritas se apilan sin taparse.
- 🔧 ¿Preferís la notificación de antes? `PROGRESO_MODO=notificacion` · ¿otro monitor? `PROGRESO_MONITOR=DP-3`.

---

## 🎓 Centro de estudio: cómo estudiar (el flujo de todos los días)

No hace falta entrar a las carpetas: **`SUPER+I`** (o 🎓 en el Stream Deck) abre una ventana con **la próxima clase que te toca**, y todo se hace desde ahí con el teclado:

```
1️⃣  ¿YA LO SABÉS?  3 preguntas de la clase. Pensá → Espacio (ver respuesta) → 1 la sabía / 2 no.
                   3/3 → Enter: "ya la sé", se marca ⏭️ y pasás a la siguiente (¡sin ver el video!)
                   Si no → Enter: a estudiarla.  (S = saltear el pre-test)
2️⃣  ESTUDIAR       💡 idea + 🗺️ mapa de la clase a la vista.
                   V ver la clase (YouTube) · R resumen · A apuntes (Obsidian)
3️⃣  PRACTICAR      P práctica: 3-5 ejercicios con tests (se generan la 1ª vez, ~30 s) y se abren
                   en VS Code. Resolvés el TODO de cada archivo...
4️⃣  VERIFICAR      T (o SUPER+ALT+V / 🧪): ✅ ej01 · ❌ ej02 (esperado 3, obtenido undefined) · 1/4
5️⃣  TERMINÉ        Ctrl+Enter (o ✅ del Stream Deck): la clase queda ✅ y aparece la siguiente.
```

- ← → mirar otra clase · **K** tarjetas · **Ctrl+Z** deshacer la última marca · **Esc** cerrar (se reabre al instante).
- El progreso queda en **`~/Vídeos/Mis cursos.md`**: `[x]` estudiada, `[s]` ⏭️ ya la sabía (también podés tildar a mano en Obsidian).
- Arriba a la derecha: **🃏 N para repasar** (tarjetas vencidas + nuevas de las clases que ya hiciste). Botón 🃏 del Stream Deck: abre las tarjetas en Obsidian → `Ctrl+P` → «Revisar tarjetas».

### 🏋️ La práctica con tests (carpeta `practica/` de cada clase)

- `README.md`: los enunciados (🟢 fácil → 🔴 difícil), con **💡 pista plegada** y una casilla "Resuelto".
- `ej01-nombre.js` (lo resolvés vos, donde dice `TODO`) + `ej01-nombre.test.js` (no lo toques). En Python: `ej01_nombre.py` + `test_ej01_nombre.py`.
- `.soluciones/`: la solución de referencia, **solo si te trabás de verdad** (intentalo antes: equivocarse es lo que enseña).
- Los tests están **verificados** antes de dártelos: la solución los pasa y el archivo vacío los falla. Si un test te marca ❌, el problema está en tu código.
- Desde la terminal: `python3 ~/.config/hypr/scripts/practica.py --correr "<carpeta de la clase>"`.
- Costo: **1 llamada a Claude por clase, solo cuando abrís su práctica** (no para todo el curso).

---

## 📓 Los apuntes (cuadernillo)

Cada clase tiene un archivo **`apuntes.md`** al lado de sus capturas.

📖 **Doble clic en un `.md` → se abre en Obsidian**, porque `~/Vídeos` está registrada como bóveda ("Vídeos"). Obsidian es el mejor visor para estos apuntes: dibuja los bloques plegables (📸 más capturas, 🗣️ lo que dice el profe, 🔁 preguntas), que VS Code muestra como texto plano. Un `.md` fuera de una bóveda (por ejemplo, el README de un proyecto) se sigue abriendo en VS Code.

> 💡 Si un curso queda **fuera de `~/Vídeos`**, en Obsidian: *Abrir otra bóveda → Abrir carpeta como bóveda* con esa carpeta, y listo.

### ¿Qué trae?

| Parte | Qué es |
|---|---|
| 🎯 **Resumen de la clase** | 5 a 8 ideas clave. Si solo lees esto, ya te acuerdas de qué trataba |
| 🧠 **Conceptos clave** | Tabla con cada término técnico y qué es, en 1-2 frases |
| 🗂️ **Índice** | Los temas de la clase con su minuto (clic → salta a la sección) |
| 📚 **Secciones por tema** | Puntos esenciales + **el código real** que se escribió + las **3-4 capturas más importantes** |
| 📸 *Más capturas* (plegado) | El resto de las capturas de ese tema, por si necesitas ver un paso intermedio |
| 🗣️ *Lo que dice el profe* (plegado) | La transcripción completa de ese tema, con minutos |
| ⚠️ **Errores comunes** | Trampas típicas que se mencionan |
| 🏋️ **Para practicar** | Ejercicios concretos de fácil a difícil, con casillas ☐ para tachar |

> 🎯 **Lo importante, a la vista. Lo completo, plegado.** Así lees rápido, pero si te falta algo está ahí mismo.

### ¿De dónde saca cada cosa?

```
🗣️ Subtítulos del video  ──┐
🔎 Texto de la pantalla     ├──► 🤖 Claude arma resumen, temas, código y ejercicios
   (OCR del código)        ──┘
📸 Capturas ──► elige las importantes de cada tema
```

- **Subtítulos:** los que vienen **dentro del video** (tus videos doblados `.es.mp4` los traen), los `.srt` al lado del video o los que baja YouTube.
- **Código real:** lee con OCR la pantalla cada ~4 minutos. Así el código de los apuntes es **el que escribió el profe**, no uno inventado.
- **(extra):** si Claude agrega algo que **no está en la clase** (un complemento útil), lo marca con **(extra)** para que sepas distinguirlo.
- **Sin subtítulos** (por ejemplo, un curso de diapositivas sin audio transcrito): arma los apuntes con lo que **se ve en pantalla**.

### ¿Cómo elige las capturas "importantes"?

- Si una captura queda **contenida en la siguiente** (el profe siguió escribiendo sobre el mismo código), solo va la **versión final**.
- Dos diapositivas distintas, aunque tengan el mismo diseño, son las dos importantes.
- En cada tema se ven: **la última** (el estado final del código) + **las que más cosas nuevas muestran**.

### ⚡ Versión corta: `resumen.md`

Al lado de `apuntes.md` se arma también **`resumen.md`**: una hoja de repaso de 3-5 minutos (no reemplaza a los apuntes, es otra forma de estudiar):

- 💡 **En una frase**: la idea central.
- ✅ **Lo esencial**: 4 a 8 cosas para llevarse.
- 🧩 **Chuleta**: tabla "Quiero… → Cómo" (comandos, funciones, sintaxis).
- 💻 **Código mínimo**: 1 a 3 fragmentos cortos que resumen la clase.
- 🗺️ **Mapa de la clase**: los bloques grandes con su minuto.
- 🔁 **Autoevaluación**: preguntas con la respuesta plegada (respondé de memoria y después abrila).

Sale en la **misma llamada** a Claude que los apuntes (no gasta una llamada extra). Para clases viejas que no lo tienen:

```bash
python3 ~/.config/hypr/scripts/resumen-corto.py "<carpeta de la clase>"
python3 ~/.config/hypr/scripts/resumen-corto.py --todos "<carpeta capturas/ del curso>"   # todas
```

### 🃏 Tarjetas de repaso: `tarjetas.md`

Cada clase trae también **`tarjetas.md`** (~20-30 tarjetas): las preguntas del resumen, los conceptos ("¿Qué es…?") y la chuleta ("¿Cómo…?"). Salen de lo que ya armó Claude: **no gastan nada extra**.

Se repasan con el plugin **Spaced Repetition** de Obsidian (ya instalado en la bóveda "Vídeos"): te muestra cada tarjeta **justo cuando estás por olvidarla**. Así te acordás del curso a largo plazo con ~5 min por día.

1. La primera vez: al abrir Obsidian, elegí **"Confiar en el autor y habilitar plugins"**.
2. Para repasar: ícono 🃏 de la barra izquierda, o `Ctrl+P` → **"Revisar tarjetas"**.
3. Respondé de memoria, mostrá la respuesta y marcá **Difícil / Bien / Fácil**.

- 💾 **Tu progreso de repaso no se pierde** aunque se regeneren las tarjetas. Tarjetas propias: escribilas en la sección **✍️ Mis tarjetas** (nunca se pisa).
- 🗃️ **Anki:** cada clase tiene también `tarjetas-anki.txt` (Anki → Archivo → Importar). Reimportarlo actualiza, no duplica.

### 📋 Panel de todos tus cursos: `~/Vídeos/Mis cursos.md`

Una página con **todos tus cursos**: cantidad de clases, horas de video y, por clase, una casilla ☐ y links a 📓 apuntes, ⚡ resumen y 🃏 tarjetas. **Tildá la casilla cuando estudiaste y practicaste una clase**: el progreso ("3/41 clases estudiadas") se actualiza cada vez que termina un video nuevo. Tus casillas y la sección **📝 Mis notas** del final nunca se pierden.

### 🖼️ Formato de las capturas: WebP sin pérdida

Las capturas se guardan en **`.webp` sin pérdida**: los píxeles son **exactamente los mismos** que en un PNG (verificado píxel por píxel), pero ocupan **~43 % menos**. Se ven en Obsidian, VS Code, el navegador y cualquier visor de imágenes.

> ❌ No se usa WebP *con* pérdida: pesa mucho menos, pero difumina las letras chicas del código (peor para leer y para el OCR).

Las capturas viejas en PNG siguen funcionando. Para pasarlas a WebP (compara cada imagen antes de borrar el PNG y corrige los links de los apuntes):

```bash
python3 ~/.config/hypr/scripts/capturas-a-webp.py "<carpeta del curso o de la clase>"
```

### 🗂️ Índice del curso

En la carpeta `capturas/` del curso se arma **`INDICE.md`**: una tabla con todas las clases, la idea principal de cada una y el link a sus apuntes. **Empieza por ahí.**

---

## 🎓 Curso entero de una vez

**Sirve para:** un curso descargado completo (una carpeta con todos los videos).

### Paso a paso

1. ⌨️ Aprieta **`SUPER + ALT + A`**.
2. 📁 Elige la carpeta del curso y aprieta **Aceptar**.
3. 📊 Aparece la **barrita de progreso** del curso ("clase 1/10", "clase 2/10"…).
4. ☕ Sigue con tu vida. Va clase por clase, **en segundo plano y con prioridad baja** (no te frena la compu).
5. ✅ Al final: **"Listo · N de N clases con apuntes"** → abre `capturas/INDICE.md`.

### Detalles útiles

- 🔁 **Si se corta** (apagaste la compu, etc.), aprieta `SUPER+ALT+A` otra vez con la misma carpeta: **sigue donde quedó** y saltea las clases ya hechas.
- 🎙️ Si hay `clase.mp4` **y** `clase.es.mp4` (doblado), usa **el doblado**, que trae los subtítulos adentro.
- ⏳ Ignora descargas a medias (`.part`).
- 🚦 Solo corre **un curso a la vez**. Si ya hay uno, te avisa.
- 📝 El detalle de lo que va haciendo queda en `~/.cache/auto-captura/curso_*.log`.

💻 **Desde la terminal:**

```bash
~/.config/hypr/scripts/curso-a-apuntes.sh "/ruta/a/la/carpeta del curso"
```

---

## 🔴 Forma 1: En vivo (mientras miras el curso)

**Sirve para:** Udemy, Platzi, YouTube, Coursera, cualquier cosa que se vea en pantalla.

1. 🖥️ Pon el curso en **pantalla completa** en tu monitor principal (x1.5 o x2 también funciona).
2. 🖱️ Haz clic en el video para que ese monitor tenga el **foco**.
3. ⌨️ Aprieta **`SUPER + ALT + S`** → aviso **"Auto-captura ON"**.
4. 🍿 Mira el curso tranquilo.
5. ⌨️ Al terminar, **`SUPER + ALT + S`** otra vez → **"Auto-captura OFF — N capturas"**.

### ⚠️ Ojo con esto

- 📢 Captura **todo lo que se ve en ese monitor** (notificaciones, otra ventana…).
- 🕐 Los archivos se llaman `0001.webp`, `0002.webp`… y la **hora del día** de cada una queda en `.minutos.tsv`.
- 📓 En vivo **no arma cuadernillo** (no tiene los subtítulos del video). Si el curso se puede descargar, conviene la forma 2 o `SUPER+ALT+A`.
- 🔒 **Udemy / Platzi:** la primera vez prueba 1 minuto. Si sale en **negro** (protección anticopia), avísale a Claude.

---

## 🔗 Forma 2: Link de YouTube (sin mirar el video)

1. 📋 Copia el link del video (**`Ctrl + C`**).
2. ⌨️ Aprieta **`SUPER + ALT + Y`** → aviso **"Leyendo el link…"**.
3. 📊 Aparece la **barrita de progreso** (📥 → 📸 → 🤖). Trabaja en segundo plano.
4. ✅ La barrita termina en **"Listo"** con la carpeta de los apuntes.

```
📥 Baja el video (sin audio, 1080p) + 📝 subtítulos
📸 Saca las capturas → 📓 arma el cuadernillo
🗑️ Borra el video (ya está en YouTube)
```

### 📋 Playlists enteras (cursos de YouTube)

Si el link copiado es de una **playlist** (tiene `list=`), `SUPER+ALT+Y` pregunta: **"Solo este video"** o **"Playlist entera (41 videos · 15,7 h)"**.

- 📁 Queda como un curso: `~/Vídeos/Capturas de YouTube/<playlist>/capturas/001 - …/`, `002 - …/` + `INDICE.md`.
- 🔁 **Se puede cortar cuando quieras** (apagar la compu, etc.): volvé a apretar `SUPER+ALT+Y` con el mismo link y **sigue donde quedó**.
- 🚫 Videos privados o eliminados se saltean. Si YouTube frena ("no sos un robot"), espera y reintenta; si sigue frenado, corta y te avisa que lo retomes más tarde.
- ⏱️ Tarda **~10 min por hora de video**: una playlist de 15 h ≈ 3 h (una noche); una de 70 h ≈ 15 h (varias noches).

### 📥 Cola: podés encolar varios links

Si apretás `SUPER+ALT+Y` (o `SUPER+ALT+A`) mientras ya se está procesando algo, **no se mezclan**: queda **en cola** ("⏳ En cola, posición 2") y se procesa después, de a uno. Un link repetido no se duplica. Ideal para encolar varios videos antes de dormir.

```bash
~/.config/hypr/scripts/cola-capturas.sh estado     # qué se procesa y qué espera
~/.config/hypr/scripts/cola-capturas.sh vaciar     # borrar lo que espera
~/.config/hypr/scripts/cola-capturas.sh cancelar   # cortar lo actual (se retoma después)
```

✨ Las capturas se llaman **`0001.webp`, `0002.webp`…** en orden. El minuto del video de cada una queda anotado en el archivo oculto `.minutos.tsv`, y en los apuntes cada captura muestra su minuto debajo (⏱️ 1:23:45).

---

## 💾 Forma 3: Un video que ya tienes descargado

```bash
~/.config/hypr/scripts/video-a-capturas.sh "/ruta/al/video.mp4"
```

Capturas + cuadernillo quedan **al lado del video**, en `capturas/<nombre de la clase>/`.

---

## 📂 ¿Dónde queda todo?

| Cómo lo usaste | Carpeta |
|---|---|
| 🎓 Curso entero (`SUPER+ALT+A`) | `<carpeta del curso>/capturas/<clase>/` + `capturas/INDICE.md` |
| 🔗 Link de YouTube (`SUPER+ALT+Y`) | `~/Vídeos/Capturas de YouTube/<título del video>/` |
| 💾 Video descargado | `<carpeta del video>/capturas/<clase>/` |
| 🔴 En vivo (`SUPER+ALT+S`) | La carpeta que elegiste con `CTRL+SHIFT+D` → `auto_FECHA_HORA_nombre/` |

### Ejemplo

```
📁 Neural Networks： Zero to Hero/
├── 🎬 001 - The spelled-out intro….es.mp4
├── 🎬 002 - …es.mp4
└── 📁 capturas/
    ├── 🗂️ INDICE.md                ← empieza por acá
    ├── 📁 001 - The spelled-out intro…/
    │   ├── 📓 apuntes.md           ← el cuadernillo
    │   ├── ⚡ resumen.md           ← la versión corta (repaso)
    │   ├── 🖼️ 0001.webp
    │   ├── 🖼️ 0002.webp
    │   ├── 🕐 .minutos.tsv         ← (oculto) minuto de cada captura
    │   └── …
    └── 📁 002 - …/
```

---

## ⏱️ ¿Cuánto tarda?

| Qué | Tiempo aproximado |
|---|---|
| 🔴 En vivo | **Nada extra** |
| 📸 Capturas de un video 4K de 2,5 h | ~**30 min** (1080p: bastante menos) |
| 📓 Cuadernillo de una clase de 2 h | ~**5 min** (elegir capturas + OCR + Claude) |
| 🔗 Video de YouTube de 20-30 min | ~**3 min** en total |
| 📋 Playlist | ~**10 min por hora de video** |
| 🎓 Curso de 10 clases largas | **Varias horas** → ideal dejarlo **de noche** |

📊 **Capturas:** diapositivas ~3 por minuto · código intenso (tipo Karpathy) ~7-8 por minuto. En el cuadernillo solo se ven **3-4 por tema**.

---

## 🎬 ¿Con qué videos funciona bien?

| Tipo de video | Resultado |
|---|---|
| 💻 **Código** (VS Code, Jupyter, terminal) | ⭐⭐⭐ Excelente: cada línea nueva + el código real en los apuntes |
| 🎞️ **Diapositivas** | ⭐⭐⭐ Excelente: una por diapositiva o punto nuevo |
| 🧑‍🏫 **Diapositivas + cara del profe** | ⭐⭐⭐ La cara se ignora sola |
| ✏️ **Pizarra / dibujo** | ⭐⭐ Guarda cuando termina el trazo |
| 🎥 **Video filmado** (persona hablando, TikTok) | ⭐ Pocas capturas útiles, pero **el cuadernillo sí sirve** (sale de los subtítulos) |

---

## 📚 Rutina de estudio recomendada

```
0️⃣  ABRIR     → SUPER+I: el Centro de estudio te lleva a la próxima clase (con pre-test).
1️⃣  PROCESAR  → SUPER+ALT+A con el curso (de noche) o SUPER+ALT+Y con un video.
2️⃣  VER       → Mira la clase a x1.5–x2. Solo entender, sin pausar ni anotar.
3️⃣  LEER      → Abre apuntes.md: Resumen + Conceptos + los temas (10-15 min).
4️⃣  PRACTICAR → P en el Centro de estudio: ejercicios con tests (T para verificar), SIN mirar.
                Si te trabas: la sección del tema → las capturas → "lo que dice el profe".
5️⃣  REPASAR   → Todos los días ~5 min: 🃏 tarjetas (Ctrl+P → Revisar tarjetas).
                Antes de la clase siguiente: resumen.md (la Autoevaluación de memoria).
6️⃣  MARCAR    → Ctrl+Enter en el Centro de estudio (o ✅ del Stream Deck).
```

> 💪 **Lo que más enseña es el paso 4.** Los apuntes son para **recordar rápido** y **destrabarte**, no para reemplazar la práctica.

---

## 🧠 ¿Cómo funciona por dentro? (para entenderlo)

### Las capturas

Cada **1 segundo** mira la pantalla y se pregunta:

1. 🔲 **¿Cambió algo?** Divide la pantalla en **cuadritos de 32 px**. Con que cambie **uno solo** (una letra, un `;`), cuenta. *(Un promedio de toda la pantalla no sirve: una línea nueva es menos del 1 %).*
2. ⏳ **¿Ya terminó de escribir?** Espera **2 s de pantalla quieta**. Si el profe escribe sin parar, guarda igual cada 6 s.
3. 📜 **¿Va a hacer scroll o cambiar de diapositiva?** Antes, guarda cómo estaba (la versión más completa).
4. 🙈 **¿Qué ignora?**

| Qué | Cómo lo reconoce |
|---|---|
| ⌨️ Cursor de texto | Rayita vertical finita y alta (un trazo de letra es más bajito) |
| 🖱️ Mouse del profe | Mancha chiquita que desaparece de un lugar y aparece en otro |
| 🔁 Íconos que parpadean | Van y vuelven entre dos estados (A → B → A) |
| 🧑 Webcam del profe | Zona compacta que se mueve **aunque el resto de la pantalla esté quieto** |

5. ♻️ **¿Ya lo tengo guardado?** Compara con las **últimas 30 capturas**, aunque el profe haya vuelto al mismo código más arriba o más abajo (scroll). 🛡️ Cada línea tiene que estar **entera e idéntica** en una captura anterior: **un solo carácter distinto → se guarda**.

### El cuadernillo

1. 📸 **Elige las capturas importantes** (las que no quedan contenidas en la siguiente).
2. 🗣️ **Junta los subtítulos.** Para Claude usa los **originales en inglés** si existen (la traducción automática confunde términos: "xp" en vez de `exp`, "10h" en vez de `tanh`). Para que tú leas, muestra los de **español**.
3. 🔎 **OCR:** lee el código de la pantalla cada ~4 min.
4. 🤖 **Claude Sonnet** (tu cuenta, desde la terminal) arma en **una sola llamada** los temas, el resumen, los conceptos, el código, los ejercicios **y** el repaso corto (`resumen.md`). Sonnet gasta bastante menos cuota que el modelo más potente y resume muy bien. Lo que gasta depende de las **horas de video**, no de cuántos videos sean.
5. 📓 **Arma `apuntes.md`**: a la vista lo importante; plegado, todo lo demás.

### ✅ Probado

- 🧪 **10 pruebas** del sistema de capturas + **8** del cuadernillo + **4** del resumen corto + **11** de tarjetas y panel + **14** de la cola + **19** de playlists
- 🎲 **Prueba de estrés:** 200 cambios de 1 carácter al azar → **0 perdidos**
- 🎬 Cursos reales: Karpathy (4K, código), React (diapositivas, sin subtítulos), YouTube

---

## ⚙️ Ajustes

**Capturas:** `~/.config/hypr/scripts/auto-captura.conf`

| Ajuste | Valor | Para qué |
|---|---|---|
| `RUIDO` | 28 | ⬆️ Subir si salen capturas "iguales" · ⬇️ bajar si se pierde algo |
| `MIN_PIXELES` | 6 | Igual que RUIDO: más alto = menos sensible |
| `ESTABLE` | 2 | Segundos de pantalla quieta para guardar |
| `TOPE` | 6 | Si cambia sin parar, guarda igual cada N segundos |
| `HISTORIAL` | 30 | Con cuántas capturas anteriores compara (0 = apagado) |
| `INTERVALO` | 1 | Cada cuántos segundos mira la pantalla |
| `MASCARA_ABAJO` | 0 | Ej. `0.08` ignora la barra del reproductor |

**Cuadernillo** (sin editar nada, desde la terminal):

```bash
SIN_IA=1       ~/.config/hypr/scripts/video-a-capturas.sh video.mp4   # apuntes sin Claude
SIN_APUNTES=1  ~/.config/hypr/scripts/video-a-capturas.sh video.mp4   # solo capturas
APUNTES_MODELO=opus ~/.config/hypr/scripts/video-a-capturas.sh video.mp4   # curso difícil: el modelo más potente (gasta más)
MAX_VIDEOS=2   ~/.config/hypr/scripts/playlist-a-apuntes.sh "<link de playlist>"   # probar con los 2 primeros
python3 ~/.config/hypr/scripts/cuadernillo.py "<carpeta de capturas>" --video video.mp4 --forzar   # rehacer apuntes
```

---

## 🆘 Problemas comunes

| 😕 Problema | 🔧 Solución |
|---|---|
| `SUPER+ALT+Y` dice "no es un link de YouTube" | Primero copia el link con `Ctrl+C` |
| "falló" en un aviso | Mira el `.log` en `~/.cache/auto-captura/` |
| El cuadernillo dice "sin resumen de IA" | No había subtítulos ni texto en pantalla, o Claude no respondió. Se arregla con `rehacer-sin-ia.py "<carpeta del curso>"` (no hace falta el video) |
| Se agotó la cuota de Claude en medio de una playlist | Ya no pasa nada: el sistema **espera** a que se renueve (reintenta cada 10 min, hasta 6 h) y sigue con IA. Al final de cada playlist o curso rehace solo las clases que hayan quedado sin IA |
| No bajó subtítulos de YouTube | YouTube a veces los bloquea (error 429). Igual se arman capturas y apuntes (con OCR) |
| Algo en los apuntes no coincide con el video | Revisa la captura y "lo que dice el profe" de esa sección. Lo marcado **(extra)** no está en la clase |
| `SUPER+ALT+A` dice que ya hay un curso procesándose | Espera a que termine (o mira el log) |
| Salen muchas capturas casi iguales | Sube `RUIDO` (ej. 35) |
| Siento que falta algo | Baja `RUIDO` (ej. 22) · para algo puntual: `CTRL+SHIFT+S` |
| Udemy sale en negro | Protección anticopia: avísale a Claude |
| Capturó el monitor equivocado | Clic en el monitor del curso **antes** de `SUPER+ALT+S` |

---

## 📁 Archivos del sistema y pruebas

Todo está en `~/.config/hypr/scripts/`:

| Archivo | Qué es |
|---|---|
| `auto-captura.py` | 🧠 El "cerebro" de las capturas |
| `cuadernillo.py` | 📓 Arma los apuntes (y el `INDICE.md` del curso) |
| `resumen-corto.py` | ⚡ Arma la versión corta (`resumen.md`) |
| `capturas-a-webp.py` | 🖼️ Pasa capturas viejas PNG a WebP sin pérdida |
| `capturas-nombre-corto.py` | 🔢 Renombra capturas viejas `0012_01-23-45` → `0012` (guarda el minuto en `.minutos.tsv`) |
| `playlist-a-apuntes.sh` | 📋 Una playlist de YouTube → curso con apuntes |
| `cola-capturas.sh` | 📥 La cola: un pedido por vez (`estado`, `vaciar`, `cancelar`) |
| `tarjetas.py` | 🃏 Arma `tarjetas.md` (Obsidian) y `tarjetas-anki.txt` |
| `panel-cursos.py` | 📋 Arma `~/Vídeos/Mis cursos.md` |
| `rehacer-sin-ia.py` | 🔁 Rehace con IA las clases que quedaron sin resumen (sin bajar el video) |
| `estudiar.py` | 🎓 Centro de estudio (`SUPER+I`; `--tests`, `--terminar`, `--repasar`, `--estado`) |
| `practica.py` | 🏋️ Práctica con tests verificados (`--correr` para verificar) |
| `abrir-markdown.py` | 📖 Doble clic en un `.md` → Obsidian (si está en una bóveda) o VS Code |
| `curso-a-apuntes.sh` | 🎓 Procesa un curso entero |
| `curso-apuntes-elegir.sh` | 📁 Lo que ejecuta `SUPER+ALT+A` (elegir carpeta) |
| `youtube-capturas.sh` | 🔗 Lo que ejecuta `SUPER+ALT+Y` |
| `video-a-capturas.sh` | 💾 Un video o link → capturas + apuntes |
| `auto-captura-toggle.sh` | ▶️⏹️ Lo que ejecuta `SUPER+ALT+S` |
| `progreso.py` | 📊 La barrita de progreso (monitor vertical) |
| `auto-captura.conf` | ⚙️ Ajustes de las capturas |
| `auto-captura-tests.py` · `auto-captura-estres.py` · `cuadernillo-tests.py` · `resumen-corto-tests.py` · `tarjetas-panel-tests.py` · `cola-capturas-tests.sh` · `playlist-a-apuntes-tests.sh` | 🧪 Pruebas |

Los atajos están en `~/.config/hypr/config/binds.lua`.

🧪 **Si se cambia el código, correr las pruebas** (todas tienen que dar OK):

```bash
python3 ~/.config/hypr/scripts/auto-captura-tests.py     # TODO OK
python3 ~/.config/hypr/scripts/auto-captura-estres.py    # cambios perdidos: 0/40
python3 ~/.config/hypr/scripts/cuadernillo-tests.py      # TODO OK
python3 ~/.config/hypr/scripts/resumen-corto-tests.py    # 4/4 pruebas OK
python3 ~/.config/hypr/scripts/tarjetas-panel-tests.py   # 11/11 pruebas OK
bash ~/.config/hypr/scripts/cola-capturas-tests.sh       # OK
bash ~/.config/hypr/scripts/playlist-a-apuntes-tests.sh  # OK
python3 ~/.config/hypr/scripts/practica-tests.py         # 10/10
python3 ~/.config/hypr/scripts/estudiar-tests.py         # 10/10
```

---

## ⚡ Resumen ultra corto

```
🎓 Curso descargado  →  SUPER+ALT+A  →  elegir carpeta  →  (de noche)  →  capturas/INDICE.md
🔗 Link de YouTube   →  Ctrl+C al link  →  SUPER+ALT+Y  →  apuntes.md + resumen.md + tarjetas.md
📋 Playlist          →  Ctrl+C al link  →  SUPER+ALT+Y  →  "Playlist entera"  →  capturas/INDICE.md
📥 Varios links      →  SUPER+ALT+Y uno tras otro  →  se encolan solos
🔴 Curso que miro    →  SUPER+ALT+S (empezar) … SUPER+ALT+S (terminar)
✂️ Captura puntual   →  CTRL+SHIFT+S
🎓 Estudiar          →  SUPER+I → ¿ya lo sabés? → estudiar → P práctica → T tests → Ctrl+Enter
⚡ Repasar           →  resumen.md (Autoevaluación) + 🃏 tarjetas (Ctrl+P → Revisar tarjetas)
📋 Mi progreso       →  ~/Vídeos/Mis cursos.md (tildar cada clase estudiada)
```

🎓 **¡A estudiar y a practicar!**
