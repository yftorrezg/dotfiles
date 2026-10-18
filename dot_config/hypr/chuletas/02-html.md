# 🧱 HTML
> El esqueleto de toda página web: etiquetas, formularios, semántica, accesibilidad y SEO, con ejemplos resueltos.

## 🌱 Qué es HTML y cómo se escribe
HTML (HyperText Markup Language) no es un lenguaje de programación: es un lenguaje de **marcado**. No calcula nada; le dice al navegador **qué es** cada cosa: esto es un título, esto un párrafo, esto un botón. El aspecto lo pone CSS y el comportamiento lo pone JavaScript.

Todo se escribe con **etiquetas**: una de apertura `<p>`, el contenido y una de cierre `</p>`. El conjunto completo se llama **elemento**. Las etiquetas pueden llevar **atributos** (`nombre="valor"`) que dan información extra.

- `<p>Hola</p>` :: Elemento completo: apertura + contenido + cierre
- `<a href="/contacto">Contacto</a>` :: `href` es un atributo: datos extra del elemento
- `<img src="foto.jpg" alt="Mi gato">` :: Elemento vacío: no tiene cierre ni contenido
- `<!-- comentario -->` :: Comentario: el navegador lo ignora (sí se ve en el código fuente)
- `<strong><em>hola</em></strong>` :: Anidar: se cierra en orden inverso al que se abrió

```html
<!-- Anatomía de un elemento -->
<a href="https://example.com" target="_blank" class="boton">
  Visitar sitio
</a>
<!-- etiqueta: a · atributos: href, target, class · contenido: "Visitar sitio" -->
```

📌 HTML = estructura (los huesos) · CSS = presentación (la ropa) · JS = comportamiento (los músculos).
💡 Consejo: escribe siempre las etiquetas y atributos en minúsculas y los valores entre comillas dobles; es el estilo estándar.
⚠️ Cuidado: cerrar mal el anidado `<b><i>texto</b></i>` es un error clásico; cierra primero lo último que abriste: `<b><i>texto</i></b>`.
🇬🇧 **markup** /márkap/ = marcado · **tag** = etiqueta · **element** = elemento · **attribute** /átribiut/ = atributo · **nested** = anidado · **opening / closing tag** = etiqueta de apertura / cierre

## 📄 Estructura del documento
Cada página HTML sigue el mismo esqueleto. `<!DOCTYPE html>` le dice al navegador que use el modo moderno (HTML5). Dentro de `<html>` hay dos partes: `<head>` con información **para el navegador y los buscadores** (no se ve), y `<body>` con lo que **ve el usuario**.

- `<!DOCTYPE html>` :: Primera línea siempre: activa el modo estándar HTML5
- `<html lang="es">` :: Raíz del documento; `lang` ayuda a lectores de pantalla y traductores
- `<head>` :: Metadatos: título, codificación, CSS, SEO (no se muestra)
- `<meta charset="UTF-8">` :: Codificación: sin esto las tildes y la ñ salen rotas
- `<meta name="viewport" content="width=device-width, initial-scale=1.0">` :: Imprescindible para que se vea bien en el celular
- `<title>Mi página</title>` :: Texto de la pestaña y del resultado en Google
- `<body>` :: Todo el contenido visible

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Mi primera página</title>
</head>
<body>
  <h1>¡Hola, mundo!</h1>
  <p>Esta es mi primera página web.</p>
</body>
</html>
```

💡 Consejo: en VS Code escribe `!` y pulsa Tab: Emmet te genera este esqueleto entero.
⚠️ Cuidado: olvidar el `meta viewport` hace que en el celular la página salga diminuta, como una versión de escritorio encogida.
🇬🇧 **head** /jed/ = cabeza · **body** = cuerpo · **charset** /chár-set/ = juego de caracteres · **viewport** /viúport/ = área visible de la pantalla · **encoding** = codificación

## 🔤 Encabezados y texto
Los encabezados `<h1>` a `<h6>` forman el **índice** de la página: Google y los lectores de pantalla los usan para entender la jerarquía. Elígelos por su **importancia**, no por su tamaño (el tamaño lo cambias con CSS).

- `<h1>Título principal</h1>` :: Uno por página: el tema central
- `<h2> … <h6>` :: Subniveles; no te saltes niveles (de h2 a h4 no)
- `<p>Párrafo</p>` :: Bloque de texto
- `<br>` :: Salto de línea dentro de un párrafo (poemas, direcciones)
- `<hr>` :: Separador temático (línea horizontal)
- `<strong>importante</strong>` :: Importancia fuerte (negrita, y los lectores lo enfatizan)
- `<em>énfasis</em>` :: Énfasis al leer (cursiva)
- `<mark>resaltado</mark>` :: Texto marcado, como con resaltador
- `<small>letra chica</small>` :: Notas legales, aclaraciones
- `<code>let x = 5</code>` :: Código en línea (fuente monoespaciada)
- `<pre>` :: Texto preformateado: respeta espacios y saltos
- `<blockquote cite="url">` :: Cita larga en bloque
- `<q>cita corta</q>` :: Cita en línea (añade comillas)
- `<abbr title="Inteligencia Artificial">IA</abbr>` :: Abreviatura con su significado al pasar el ratón
- `<sub> / <sup>` :: Subíndice (H₂O) / superíndice (x²)
- `<span>` :: Contenedor en línea sin significado, para dar estilo a un trozo

```html
<h1>Aprendiendo IA</h1>
<h2>1. Redes neuronales</h2>
<p>Una red neuronal aprende <strong>ajustando pesos</strong>. La fórmula
básica es y = w<sub>1</sub>x<sub>1</sub> + b.</p>
<blockquote>
  <p>"La IA es la nueva electricidad."</p>
</blockquote>
<p>Ejemplo en Python: <code>model.fit(X, y)</code></p>
```

📌 `<b>` e `<i>` existen, pero solo cambian el aspecto; `<strong>` y `<em>` además dan **significado**. Prefiere estos últimos.
⚠️ Cuidado: varios `<br><br><br>` para separar bloques es mala práctica; usa márgenes en CSS.
⚠️ Cuidado: HTML junta los espacios: 10 espacios seguidos se ven como 1. Para respetarlos usa `<pre>`.
🇬🇧 **heading** /jéding/ = encabezado · **paragraph** = párrafo · **bold** = negrita · **italic** = cursiva · **quote** /kuóut/ = cita · **line break** /bréik/ = salto de línea

## 🔗 Enlaces e imágenes
Los enlaces `<a>` (de "anchor", ancla) son lo que hace a la web una **web**: conectan páginas. Las imágenes `<img>` se insertan, no se "pegan": el navegador las descarga desde la ruta que indicas.

### Enlaces
- `<a href="https://google.com">Google</a>` :: Enlace absoluto a otro sitio
- `<a href="contacto.html">` :: Ruta relativa (misma carpeta)
- `<a href="../index.html">` :: Subir una carpeta
- `<a href="/blog">` :: Desde la raíz del sitio
- `<a href="#precios">` :: Salta a un elemento con `id="precios"` en la misma página
- `<a href="mailto:hola@ejemplo.com">` :: Abre el correo
- `<a href="tel:+59170000000">` :: Llama por teléfono (en el celular)
- `<a href="cv.pdf" download>` :: Descarga el archivo en vez de abrirlo
- `target="_blank" rel="noopener"` :: Abrir en pestaña nueva de forma segura

### Imágenes
- `<img src="gato.jpg" alt="Gato naranja durmiendo">` :: `alt` describe la imagen si no carga o para ciegos
- `width="400" height="300"` :: Reserva el espacio y evita que la página "salte" al cargar
- `loading="lazy"` :: Carga la imagen solo cuando se acerca al scroll
- `<figure> + <figcaption>` :: Imagen con pie de foto
- `<picture> + <source>` :: Ofrecer formatos o tamaños distintos (webp, avif)
- `srcset="foto-480.jpg 480w, foto-960.jpg 960w"` :: El navegador elige la resolución adecuada

```html
<figure>
  <img src="img/salar-uyuni.webp"
       alt="El Salar de Uyuni reflejando el cielo"
       width="800" height="450" loading="lazy">
  <figcaption>Salar de Uyuni, Potosí 🇧🇴</figcaption>
</figure>

<picture>
  <source srcset="logo.avif" type="image/avif">
  <source srcset="logo.webp" type="image/webp">
  <img src="logo.png" alt="Logo de la empresa">
</picture>

<p>Lee la <a href="#instalacion">guía de instalación</a> o
<a href="https://github.com" target="_blank" rel="noopener">mira el repo</a>.</p>
```

💡 Consejo: el texto del enlace debe tener sentido solo: "Descargar el temario" es mejor que "haz clic aquí".
💡 Consejo: si una imagen es pura decoración, pon `alt=""` (vacío): así el lector de pantalla la salta.
⚠️ Cuidado: las rutas distinguen mayúsculas en un servidor Linux: `Foto.JPG` no es `foto.jpg`. Usa nombres en minúsculas y sin espacios.
⚠️ Cuidado: no metas un `<a>` dentro de otro `<a>`; está prohibido y se rompe.
🇬🇧 **link** = enlace · **anchor** /ánker/ = ancla · **path** /paz/ = ruta · **relative / absolute** = relativa / absoluta · **caption** /cápshon/ = pie de foto · **lazy loading** /léisi/ = carga diferida

## 📋 Listas
Las listas agrupan elementos relacionados. Se usan muchísimo, no solo para viñetas: los menús de navegación son listas de enlaces.

- `<ul>` :: Lista desordenada (viñetas): el orden no importa
- `<ol>` :: Lista ordenada (números): pasos, rankings
- `<li>` :: Cada elemento de la lista (solo dentro de `ul` u `ol`)
- `<ol start="5">` :: Empezar a contar desde 5
- `<ol reversed>` :: Cuenta hacia atrás
- `<ol type="a">` :: Usar letras (a, b, c) o romanos (`type="I"`)
- `<dl> <dt> <dd>` :: Lista de definiciones: término y descripción

```html
<h2>Receta de salteñas</h2>
<ol>
  <li>Preparar el jigote el día anterior.</li>
  <li>Hacer la masa.
    <ul>
      <li>Harina</li>
      <li>Manteca</li>
      <li>Azúcar</li>
    </ul>
  </li>
  <li>Hornear a 220 °C.</li>
</ol>

<dl>
  <dt>API</dt>
  <dd>Interfaz para que dos programas se comuniquen.</dd>
  <dt>DOM</dt>
  <dd>Árbol de objetos que representa la página.</dd>
</dl>
```

⚠️ Cuidado: dentro de `<ul>` solo puede haber `<li>`. Una sublista va **dentro** de un `<li>`, no suelta.
💡 Consejo: para quitar las viñetas de un menú usa CSS `list-style: none;`, no cambies de etiqueta.
🇬🇧 **list** = lista · **unordered / ordered** = desordenada / ordenada · **list item** /áitem/ = elemento de lista · **bullet** /búlet/ = viñeta · **step** = paso

## 📊 Tablas
Las tablas son para **datos tabulares** (filas y columnas que se comparan: horarios, notas, precios). Hace años se usaban para maquetar páginas; hoy eso se hace con Flexbox y Grid.

- `<table>` :: La tabla completa
- `<caption>` :: Título de la tabla (accesible)
- `<thead> <tbody> <tfoot>` :: Cabecera, cuerpo y pie
- `<tr>` :: Una fila (table row)
- `<th scope="col">` :: Celda de encabezado de columna (negrita y centrada)
- `<th scope="row">` :: Encabezado de fila
- `<td>` :: Celda de datos
- `colspan="2"` :: La celda ocupa 2 columnas
- `rowspan="3"` :: La celda ocupa 3 filas

```html
<table>
  <caption>Notas del semestre</caption>
  <thead>
    <tr>
      <th scope="col">Materia</th>
      <th scope="col">Parcial</th>
      <th scope="col">Final</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">Cálculo I</th>
      <td>78</td>
      <td>85</td>
    </tr>
    <tr>
      <th scope="row">Programación</th>
      <td>92</td>
      <td>95</td>
    </tr>
  </tbody>
  <tfoot>
    <tr>
      <td colspan="2">Promedio final</td>
      <td>90</td>
    </tr>
  </tfoot>
</table>
```

💡 Consejo: en el celular las tablas anchas se desbordan; envuélvelas en un `<div>` con `overflow-x: auto;` en CSS.
⚠️ Cuidado: no uses tablas para poner cosas lado a lado (menús, columnas de la página): es inaccesible y difícil de adaptar.
🇬🇧 **table** /téibol/ = tabla · **row** /róu/ = fila · **column** /cólum/ = columna · **cell** = celda · **header** /jéder/ = encabezado · **span** = abarcar

## 📝 Formularios
Los formularios son cómo el usuario **envía datos**: login, registro, búsqueda, pagos. El `<form>` agrupa los campos; `action` dice a dónde se envían y `method` cómo (`GET` los pone en la URL, `POST` los manda ocultos en el cuerpo de la petición).

### Lo básico
- `<form action="/registro" method="post">` :: Formulario que envía por POST a `/registro`
- `<label for="email">Correo</label>` :: Etiqueta del campo; `for` = `id` del input
- `<input id="email" name="email" type="email">` :: `name` es la clave con la que llega al servidor
- `<textarea name="msg" rows="4"></textarea>` :: Texto largo de varias líneas
- `<select name="pais"> + <option value="bo">` :: Lista desplegable
- `<optgroup label="Sudamérica">` :: Agrupar opciones del select
- `<button type="submit">Enviar</button>` :: Envía el formulario
- `<button type="button">` :: Botón que NO envía (para JS)
- `<button type="reset">` :: Vacía el formulario
- `<fieldset> + <legend>` :: Agrupar campos relacionados con un título
- `<datalist id="lenguajes">` :: Sugerencias de autocompletado para un input (`list="lenguajes"`)

### Todos los tipos de input
| type | Qué muestra | Uso típico |
|---|---|---|
| `text` | Caja de texto | Nombre, usuario |
| `email` | Texto que valida formato de correo | Correo electrónico |
| `password` | Texto oculto con puntos | Contraseña |
| `number` | Número con flechitas (`min`, `max`, `step`) | Edad, cantidad |
| `tel` | Teclado numérico en celular | Teléfono |
| `url` | Valida que empiece con http(s) | Sitio web |
| `search` | Caja de búsqueda con botón de borrar | Buscador |
| `date` | Selector de fecha | Fecha de nacimiento |
| `time` | Selector de hora | Hora de cita |
| `datetime-local` | Fecha y hora | Reservas |
| `month` / `week` | Mes / semana | Reportes |
| `color` | Selector de color | Personalizar tema |
| `range` | Barra deslizante | Volumen, precio máximo |
| `checkbox` | Casilla que se marca (varias a la vez) | Aceptar términos, intereses |
| `radio` | Opción única dentro de un grupo con el mismo `name` | Género, plan |
| `file` | Subir archivo (`accept`, `multiple`) | Foto de perfil, CV |
| `hidden` | Nada: valor oculto que se envía igual | IDs, tokens |
| `submit` / `reset` / `button` | Botones (mejor usa `<button>`) | Enviar |

### Validación nativa (sin JavaScript)
- `required` :: Campo obligatorio
- `minlength="8" / maxlength="20"` :: Largo mínimo / máximo del texto
- `min="18" / max="99" / step="0.5"` :: Límites para números y fechas
- `pattern="[0-9]{8}"` :: Expresión regular que debe cumplir (aquí: 8 dígitos)
- `placeholder="ej. juan@mail.com"` :: Texto de ejemplo gris (no reemplaza al label)
- `autocomplete="email"` :: Ayuda al navegador a autocompletar
- `autofocus` :: El cursor empieza en este campo
- `disabled / readonly` :: Desactivado (no se envía) / solo lectura (sí se envía)
- `checked / selected` :: Marcado por defecto (checkbox/radio) / opción elegida por defecto
- `novalidate` :: En el `<form>`: desactiva la validación nativa (para validar con JS)

```html
<form action="/buscar" method="get">
  <label for="q">Buscar curso</label>
  <input type="search" id="q" name="q" list="cursos" required>
  <datalist id="cursos">
    <option value="HTML">
    <option value="CSS">
    <option value="JavaScript">
  </datalist>
  <button type="submit">🔍 Buscar</button>
</form>
<!-- Al enviar va a: /buscar?q=HTML -->
```

📌 Sin `name`, un campo **no se envía**. Sin `label`, un campo **no es accesible**. Pon siempre los dos.
💡 Consejo: hacer clic en un `<label>` enfoca su input (o marca su checkbox): más área para tocar en el celular.
⚠️ Cuidado: un `<button>` dentro de un form es `type="submit"` por defecto; si es para otra cosa, pon `type="button"` o recargará la página.
⚠️ Cuidado: la validación del navegador es comodidad para el usuario, no seguridad; el servidor SIEMPRE debe validar otra vez.
🇬🇧 **form** = formulario · **input** = campo de entrada · **submit** /sabmít/ = enviar · **required** /rikuáierd/ = obligatorio · **placeholder** = texto de ejemplo · **dropdown** = desplegable · **checkbox** = casilla

## 🏛️ HTML semántico
**Semántico** significa que la etiqueta describe **qué es** el contenido, no cómo se ve. Un `<div>` no dice nada; un `<nav>` dice "esto es la navegación". Ganas tres cosas: mejor SEO (Google entiende la página), accesibilidad (los lectores de pantalla permiten saltar al `main`) y código más legible.

- `<header>` :: Cabecera: logo, título, a veces el menú (de la página o de un artículo)
- `<nav>` :: Bloque de navegación principal
- `<main>` :: Contenido principal; **uno solo** por página
- `<article>` :: Contenido independiente que tendría sentido solo (post, noticia, tarjeta de producto)
- `<section>` :: Sección temática con su propio encabezado
- `<aside>` :: Contenido relacionado pero secundario (barra lateral, publicidad)
- `<footer>` :: Pie: copyright, contacto, enlaces
- `<address>` :: Datos de contacto
- `<time datetime="2026-10-18">18 de octubre</time>` :: Fecha legible por máquinas
- `<details> + <summary>` :: Acordeón desplegable sin JavaScript
- `<dialog>` :: Ventana modal nativa (se abre con JS: `dialog.showModal()`)
- `<div>` :: Caja genérica sin significado: úsala solo para agrupar y dar estilo

```html
<body>
  <header>
    <h1>Blog de Yafer</h1>
    <nav>
      <ul>
        <li><a href="/">Inicio</a></li>
        <li><a href="/blog">Blog</a></li>
      </ul>
    </nav>
  </header>

  <main>
    <article>
      <h2>Cómo entrené mi primer modelo</h2>
      <p>Publicado el <time datetime="2026-10-18">18/10/2026</time></p>
      <section>
        <h3>Los datos</h3>
        <p>...</p>
      </section>
    </article>
    <aside>
      <h2>Posts populares</h2>
    </aside>
  </main>

  <footer>
    <p>© 2026 Yafer · Cochabamba</p>
  </footer>
</body>
```

```html
<details>
  <summary>¿Qué es un transformer?</summary>
  <p>Una arquitectura de red basada en atención.</p>
</details>
```

💡 Consejo: pregunta "¿esto tiene sentido si lo saco de la página?". Si sí → `article`. Si es una parte de algo mayor con título → `section`. Si solo es para estilo → `div`.
⚠️ Cuidado: la "divitis" (todo con `div`) funciona, pero la página queda ciega para Google y para los lectores de pantalla.
🇬🇧 **semantic** /simántik/ = semántico · **layout** /léiaut/ = maquetación · **sidebar** = barra lateral · **footer** /fúter/ = pie de página · **landmark** = región de referencia

## 🎬 Multimedia: video, audio e iframe
HTML5 reproduce video y audio sin plugins. `<iframe>` incrusta otra página dentro de la tuya (YouTube, Google Maps).

- `<video src="clase.mp4" controls>` :: Video con botones de play, volumen, etc.
- `poster="portada.jpg"` :: Imagen antes de darle play
- `autoplay muted loop playsinline` :: Video de fondo (autoplay solo funciona si está `muted`)
- `preload="metadata"` :: Carga solo la duración, no el video entero
- `<audio src="podcast.mp3" controls>` :: Reproductor de audio
- `<source src="v.webm" type="video/webm">` :: Varias fuentes: el navegador usa la primera que soporte
- `<track kind="subtitles" src="es.vtt" srclang="es">` :: Subtítulos
- `<iframe src="..." title="..." loading="lazy">` :: Incrustar otra página
- `allowfullscreen` :: Permite pantalla completa en el iframe

```html
<video controls width="640" poster="img/portada.jpg" preload="metadata">
  <source src="video/clase1.webm" type="video/webm">
  <source src="video/clase1.mp4" type="video/mp4">
  <track kind="subtitles" src="subs/es.vtt" srclang="es" label="Español" default>
  Tu navegador no soporta video. <a href="video/clase1.mp4">Descárgalo aquí</a>.
</video>

<audio controls src="audio/podcast-ep1.mp3"></audio>

<iframe width="560" height="315"
  src="https://www.youtube.com/embed/ID_DEL_VIDEO"
  title="Tutorial de HTML"
  loading="lazy" allowfullscreen></iframe>
```

⚠️ Cuidado: los navegadores bloquean `autoplay` con sonido; si quieres que arranque solo, añade `muted`.
💡 Consejo: dale siempre un `title` al `iframe`: el lector de pantalla lo anuncia para saber qué contiene.
🇬🇧 **embed** /embéd/ = incrustar · **controls** = controles · **muted** /miúted/ = silenciado · **loop** = bucle · **subtitles** /sábtaitels/ = subtítulos · **poster** = imagen de portada

## 🔎 Meta etiquetas y SEO básico
**SEO** (Search Engine Optimization) es lograr que Google entienda y muestre tu página. Lo esencial está en el `<head>`: un buen `title`, una buena `description` y HTML semántico. Las etiquetas **Open Graph** (`og:`) controlan cómo se ve tu enlace al compartirlo en WhatsApp, Facebook o LinkedIn.

- `<title>Curso de HTML gratis · Yafer</title>` :: Lo más importante del SEO: único por página, ~60 caracteres
- `<meta name="description" content="...">` :: Resumen que sale debajo del título en Google (~155 caracteres)
- `<meta name="robots" content="noindex">` :: Pide a Google que NO indexe la página
- `<link rel="canonical" href="https://...">` :: URL oficial si hay copias de la página
- `<link rel="icon" href="/favicon.svg">` :: Icono de la pestaña
- `<meta property="og:title" content="...">` :: Título al compartir en redes
- `<meta property="og:image" content="https://.../preview.jpg">` :: Imagen de la vista previa (1200×630 ideal)
- `<meta name="theme-color" content="#7c3aed">` :: Color de la barra del navegador en el celular

```html
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Aprende HTML desde cero · Academia Yafer</title>
  <meta name="description" content="Curso gratuito de HTML con ejemplos resueltos, formularios, semántica y accesibilidad.">
  <link rel="canonical" href="https://academia.example/html">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">

  <!-- Vista previa al compartir -->
  <meta property="og:title" content="Aprende HTML desde cero">
  <meta property="og:description" content="Curso gratuito con ejemplos resueltos.">
  <meta property="og:image" content="https://academia.example/og-html.jpg">
  <meta property="og:type" content="website">
</head>
```

📌 SEO básico: un `h1` claro, encabezados en orden, `alt` en imágenes, URLs legibles (`/curso-html`), página rápida y adaptada al celular.
⚠️ Cuidado: la etiqueta `<meta name="keywords">` ya no sirve: Google la ignora desde hace años.
🇬🇧 **search engine** /sérch énjin/ = buscador · **ranking** = posicionamiento · **crawler** /cróler/ = rastreador · **preview** /príviu/ = vista previa · **metadata** = metadatos

## ♿ Accesibilidad (a11y)
La **accesibilidad** es que todos puedan usar tu web: personas ciegas (con lectores de pantalla como NVDA o VoiceOver), con baja visión, que solo usan teclado, o con un celular viejo bajo el sol. La regla de oro: **usa la etiqueta HTML correcta** y gran parte del trabajo ya está hecho.

### Lo esencial
- `alt="descripción"` :: Toda imagen con contenido necesita texto alternativo
- `<label for="id">` :: Todo campo de formulario necesita su etiqueta
- `<button> vs <a>` :: `button` para acciones, `a` para navegar. No hagas botones con `div`: no reciben foco ni Enter
- `lang="es"` :: El lector pronuncia con el acento correcto
- `contraste 4.5:1` :: Mínimo entre texto y fondo: gris claro sobre blanco es ilegible

### ARIA y roles
ARIA son atributos que **añaden información** cuando el HTML no alcanza. Regla número uno de ARIA: si existe una etiqueta nativa que lo hace, úsala en vez de ARIA.

- `aria-label="Cerrar menú"` :: Nombre accesible para un botón que solo tiene un icono
- `aria-labelledby="id"` :: Usa el texto de otro elemento como nombre
- `aria-describedby="ayuda-pass"` :: Asocia una descripción extra (ej. requisitos de contraseña)
- `aria-hidden="true"` :: Oculta algo decorativo al lector de pantalla (emojis, iconos)
- `aria-expanded="false"` :: Indica si un menú desplegable está abierto
- `aria-current="page"` :: Marca el enlace de la página actual en el menú
- `aria-live="polite"` :: Anuncia cambios dinámicos (ej. "Guardado ✅")
- `role="alert"` :: Mensaje urgente que se lee de inmediato
- `role="button"` :: Dice que algo es un botón (mejor usa `<button>`)

### Orden de foco y teclado
- `Tab / Shift+Tab` :: Así navega quien usa teclado: prueba tu página así
- `tabindex="0"` :: Hace enfocable un elemento que no lo es, en el orden natural
- `tabindex="-1"` :: Enfocable solo por JS (`el.focus()`), no con Tab
- `tabindex="5"` :: Positivo: cambia el orden. Evítalo, rompe la navegación
- `<a href="#main">Saltar al contenido</a>` :: Primer enlace de la página: salta el menú y va directo al contenido

```html
<a href="#contenido" class="saltar">Saltar al contenido</a>

<button type="button" aria-label="Abrir menú" aria-expanded="false">
  <span aria-hidden="true">☰</span>
</button>

<nav aria-label="Principal">
  <a href="/" aria-current="page">Inicio</a>
  <a href="/cursos">Cursos</a>
</nav>

<main id="contenido">
  <label for="pass">Contraseña</label>
  <input type="password" id="pass" aria-describedby="ayuda-pass" minlength="8" required>
  <p id="ayuda-pass">Mínimo 8 caracteres.</p>

  <p aria-live="polite" id="estado"></p>
</main>
```

💡 Consejo: el orden de foco sigue el orden del HTML. Si con CSS cambias visualmente el orden (flex `order`), el teclado seguirá el del código.
⚠️ Cuidado: nunca quites el contorno de foco con `outline: none` sin poner otro estilo visible; los usuarios de teclado se pierden.
🇬🇧 **accessibility** /aksesibíliti/ (a11y) = accesibilidad · **screen reader** /scrín ríder/ = lector de pantalla · **focus** /fóukus/ = foco · **keyboard** = teclado · **contrast** = contraste · **skip link** = enlace para saltar

## 🏷️ Atributos globales
Son atributos que sirven en **cualquier** etiqueta. Los tres que usarás todos los días son `id`, `class` y `data-*`.

- `id="menu"` :: Identificador **único** en la página (anclas `#menu`, `getElementById`, `label for`)
- `class="btn btn-primario"` :: Una o varias clases separadas por espacio; para CSS y JS, se repiten libremente
- `data-precio="25"` :: Datos propios para JS: `el.dataset.precio`
- `title="Más info"` :: Tooltip al pasar el ratón
- `style="color: red"` :: Estilo en línea (evítalo, usa CSS aparte)
- `hidden` :: Oculta el elemento
- `lang="en"` :: Idioma de ese trozo concreto
- `dir="rtl"` :: Dirección del texto (árabe, hebreo)
- `tabindex` :: Control del foco con teclado
- `contenteditable` :: El usuario puede editar el texto
- `draggable="true"` :: Se puede arrastrar
- `spellcheck="false"` :: Desactiva el corrector ortográfico
- `inert` :: Desactiva todo un bloque (no clicable ni enfocable)

```html
<article class="producto destacado" id="prod-42"
         data-id="42" data-precio="35.50" data-categoria="libros">
  <h3>Python para IA</h3>
  <button type="button" class="btn-comprar">Agregar al carrito</button>
</article>

<script>
  const prod = document.querySelector("#prod-42");
  console.log(prod.dataset.precio);     // "35.50" (siempre texto)
  console.log(prod.dataset.categoria);  // "libros"
</script>
```

📌 `data-mi-dato` en HTML se lee como `dataset.miDato` en JS (los guiones pasan a camelCase).
⚠️ Cuidado: repetir el mismo `id` en dos elementos es inválido; `querySelector` solo encontrará el primero. Para varios, usa `class`.
🇬🇧 **global attribute** = atributo global · **class** = clase · **identifier** /aidéntifaier/ = identificador · **tooltip** /túltip/ = globo de ayuda · **custom data** = datos personalizados

## 🔣 Entidades y caracteres especiales
Algunos caracteres tienen significado en HTML (`<` abre una etiqueta). Para mostrarlos como texto se usan **entidades**: empiezan con `&` y terminan con `;`. Con `UTF-8` puedes escribir tildes, ñ y emojis directamente.

| Entidad | Resultado | Para qué |
|---|---|---|
| `&lt;` | < | Mostrar código HTML como texto |
| `&gt;` | > | Igual que arriba |
| `&amp;` | & | El propio ampersand |
| `&quot;` | " | Comillas dentro de un atributo |
| `&nbsp;` | espacio | Espacio que no se rompe (ej. `10&nbsp;km`) |
| `&copy;` | © | Copyright |
| `&reg;` / `&trade;` | ® / ™ | Marcas |
| `&euro;` | € | Euro |
| `&hellip;` | … | Puntos suspensivos |
| `&mdash;` | — | Raya larga |
| `&times;` | × | Multiplicación o botón cerrar |
| `&rarr;` | → | Flecha |

```html
<p>Para un párrafo escribe: <code>&lt;p&gt;texto&lt;/p&gt;</code></p>
<p>Precio: Bs&nbsp;150 &mdash; envío gratis &rarr;</p>
<footer>&copy; 2026 Tom &amp; Jerry S.R.L.</footer>
```

💡 Consejo: con `<meta charset="UTF-8">` no necesitas `&aacute;`; escribe "á" directamente. Solo `&lt;`, `&gt;` y `&amp;` son realmente obligatorias.
🇬🇧 **entity** /éntiti/ = entidad · **ampersand** /ámpersand/ = & · **non-breaking space** = espacio irrompible · **escape** = escapar (convertir en texto)

## 🔌 HTML + CSS + JS: cómo se conectan
HTML carga los otros dos desde el `<head>` o el final del `<body>`. El CSS va con `<link>`; el JavaScript con `<script>`. Lo importante es **cuándo** se ejecuta el script: si corre antes de que exista el HTML, no encuentra los elementos.

- `<link rel="stylesheet" href="css/estilos.css">` :: Cargar una hoja de estilos externa (lo normal)
- `<style> ... </style>` :: CSS dentro del HTML (para pruebas rápidas)
- `<script src="app.js"></script>` :: Bloquea el HTML mientras descarga y ejecuta (evítalo en el head)
- `<script src="app.js" defer></script>` :: Descarga en paralelo y ejecuta **al terminar** el HTML, en orden
- `<script src="stats.js" async></script>` :: Ejecuta en cuanto llega, sin orden (analytics, anuncios)
- `<script type="module" src="main.js"></script>` :: Módulo ES: permite `import`/`export` y ya es `defer` por defecto
- `<noscript>` :: Contenido si el usuario tiene JS desactivado
- `<link rel="preconnect" href="https://fonts.googleapis.com">` :: Conectar antes a un dominio (fuentes)

| Forma | ¿Bloquea el HTML? | ¿Cuándo se ejecuta? | ¿Respeta el orden? |
|---|---|---|---|
| `<script>` normal | Sí | Al llegar a él | Sí |
| `defer` | No | Al terminar de leer el HTML | Sí |
| `async` | No | Apenas descarga | No |
| `type="module"` | No | Como `defer` | Sí |

```html
<head>
  <link rel="stylesheet" href="css/estilos.css">
  <script type="module" src="js/main.js"></script>
</head>
```

```js
// js/main.js (es módulo: puede importar)
import { saludar } from "./utils.js";

const boton = document.querySelector("#saludar");
boton.addEventListener("click", () => saludar("Yafer"));
```

💡 Consejo: el patrón moderno es poner los `<script>` en el `<head>` con `defer` o `type="module"`; ya no hace falta ponerlos al final del body.
⚠️ Cuidado: `type="module"` no funciona abriendo el archivo con doble clic (`file://`); necesitas un servidor local, como Live Server en VS Code o `python3 -m http.server`.
🇬🇧 **stylesheet** /stáilshit/ = hoja de estilos · **script** = guion/programa · **defer** /difér/ = aplazar · **async** /éisink/ = asíncrono · **module** /mádiul/ = módulo · **render-blocking** = que bloquea el dibujado

## ✨ Buenas prácticas
Escribir HTML que funciona es fácil; escribir HTML **limpio, accesible y mantenible** es lo que te diferencia en una entrevista o en un equipo.

- `Indenta con 2 espacios` :: Cada nivel de anidado, un nivel más de sangría
- `Un solo h1` :: Y encabezados en orden lógico
- `Semántica primero` :: `header`, `nav`, `main`, `footer` antes que `div`
- `Clases con sentido` :: `.tarjeta-producto` mejor que `.caja-roja` (el color puede cambiar)
- `Nada de estilos en línea` :: Todo el CSS en su archivo
- `Imágenes optimizadas` :: Formatos webp/avif, con `width`, `height` y `loading="lazy"`
- `Valida tu HTML` :: validator.w3.org detecta etiquetas mal cerradas
- `Prueba con teclado y en celular` :: Tab por toda la página y F12 → modo dispositivo
- `Nombres de archivo` :: minúsculas-con-guiones, sin espacios ni tildes: `sobre-mi.html`

```text
mi-proyecto/
├── index.html
├── sobre-mi.html
├── css/
│   └── estilos.css
├── js/
│   └── main.js
└── img/
    ├── logo.svg
    └── foto-perfil.webp
```

💡 Consejo: aprende atajos de Emmet: `ul>li*5` + Tab crea una lista de 5 elementos; `.tarjeta>h2+p` crea un div con título y párrafo.
⚠️ Cuidado: no uses `<br>` ni `&nbsp;` para maquetar; todo espaciado se hace con CSS.
🇬🇧 **best practices** = buenas prácticas · **indentation** = sangría · **maintainable** /meintéinabol/ = mantenible · **naming** = nombrar · **validator** = validador

## 🧩 Plantilla base completa
Copia esto al empezar cualquier proyecto: ya trae todo lo necesario para que funcione bien, sea accesible y se vea correcto al compartirlo.

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Nombre de la página · Mi sitio</title>
  <meta name="description" content="Descripción breve de la página en unas 150 letras.">
  <meta name="theme-color" content="#7c3aed">
  <link rel="icon" href="img/favicon.svg" type="image/svg+xml">

  <meta property="og:title" content="Nombre de la página">
  <meta property="og:description" content="Descripción para redes sociales.">
  <meta property="og:image" content="https://misitio.example/img/og.jpg">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/estilos.css">
  <script type="module" src="js/main.js"></script>
</head>
<body>
  <a href="#contenido" class="saltar">Saltar al contenido</a>

  <header class="cabecera">
    <a href="/" class="logo">Mi sitio</a>
    <nav aria-label="Principal">
      <ul>
        <li><a href="/" aria-current="page">Inicio</a></li>
        <li><a href="/proyectos">Proyectos</a></li>
        <li><a href="/contacto">Contacto</a></li>
      </ul>
    </nav>
  </header>

  <main id="contenido">
    <h1>Título principal</h1>
    <p>Contenido...</p>
  </main>

  <footer>
    <p>&copy; 2026 Mi sitio</p>
  </footer>
</body>
</html>
```

📌 Orden recomendado en el `head`: charset → viewport → title → description → iconos → og → fuentes → CSS → JS.
🇬🇧 **template** /témpleit/ = plantilla · **boilerplate** /bóilerpleit/ = código base repetido · **favicon** /fávicon/ = icono de la pestaña · **scaffold** = estructura inicial

## 🏆 Ejemplos resueltos
Tres piezas que aparecen en casi todos los proyectos reales. Lee el código y luego la explicación de cada parte.

### ✅ Ejemplo resuelto: landing page
Una **landing page** es la página de aterrizaje de un producto: presenta, convence y pide una acción (registrarse, comprar).

```html
<body>
  <header class="cabecera">
    <a href="/" class="logo">🤖 IAprende</a>
    <nav aria-label="Principal">
      <ul>
        <li><a href="#funciones">Funciones</a></li>
        <li><a href="#precios">Precios</a></li>
        <li><a href="#registro" class="btn">Empieza gratis</a></li>
      </ul>
    </nav>
  </header>

  <main>
    <section class="hero">
      <h1>Aprende Inteligencia Artificial desde Bolivia</h1>
      <p>Cursos prácticos en español, con proyectos reales y mentoría.</p>
      <a href="#registro" class="btn btn-grande">Crear mi cuenta</a>
      <img src="img/hero.webp" alt="Estudiante programando una red neuronal"
           width="900" height="500">
    </section>

    <section id="funciones" aria-labelledby="titulo-funciones">
      <h2 id="titulo-funciones">¿Por qué IAprende?</h2>
      <ul class="funciones">
        <li><h3>📚 Teoría clara</h3><p>Matemáticas explicadas sin miedo.</p></li>
        <li><h3>💻 Práctica</h3><p>Notebooks listos para Colab.</p></li>
        <li><h3>🎓 Certificado</h3><p>Valídalo en LinkedIn.</p></li>
      </ul>
    </section>

    <section id="precios">
      <h2>Precios</h2>
      <article class="plan">
        <h3>Plan Estudiante</h3>
        <p><strong>Bs 49</strong> / mes</p>
        <a href="#registro" class="btn">Elegir plan</a>
      </article>
    </section>
  </main>

  <footer>
    <p>&copy; 2026 IAprende · Hecho en Cochabamba</p>
  </footer>
</body>
```

📌 Qué hace cada parte: el `header` con `nav` da navegación por anclas (`#funciones` salta a la sección con ese `id`). La `section.hero` es el bloque grande inicial con el único `h1` y el botón principal (CTA). `aria-labelledby` nombra la sección con su propio `h2`. Cada plan es un `article` porque tiene sentido solo. El `footer` cierra con el copyright.

### ✅ Ejemplo resuelto: formulario de registro
```html
<form action="/api/registro" method="post" class="form-registro">
  <h2>Crear cuenta</h2>

  <fieldset>
    <legend>Datos personales</legend>

    <label for="nombre">Nombre completo</label>
    <input type="text" id="nombre" name="nombre" autocomplete="name"
           minlength="3" required>

    <label for="email">Correo electrónico</label>
    <input type="email" id="email" name="email" autocomplete="email"
           placeholder="tu@correo.com" required>

    <label for="celular">Celular</label>
    <input type="tel" id="celular" name="celular" pattern="[67][0-9]{7}"
           placeholder="70012345" aria-describedby="ayuda-cel">
    <small id="ayuda-cel">8 dígitos, empieza con 6 o 7.</small>

    <label for="nacimiento">Fecha de nacimiento</label>
    <input type="date" id="nacimiento" name="nacimiento" max="2010-12-31">
  </fieldset>

  <fieldset>
    <legend>Cuenta</legend>

    <label for="pass">Contraseña</label>
    <input type="password" id="pass" name="password" minlength="8"
           autocomplete="new-password" required aria-describedby="ayuda-pass">
    <small id="ayuda-pass">Mínimo 8 caracteres.</small>

    <label for="ciudad">Ciudad</label>
    <select id="ciudad" name="ciudad" required>
      <option value="">-- Elige --</option>
      <option value="cbba">Cochabamba</option>
      <option value="lpz">La Paz</option>
      <option value="scz">Santa Cruz</option>
    </select>
  </fieldset>

  <fieldset>
    <legend>Nivel de programación</legend>
    <input type="radio" id="nivel-0" name="nivel" value="principiante" checked>
    <label for="nivel-0">Principiante</label>
    <input type="radio" id="nivel-1" name="nivel" value="intermedio">
    <label for="nivel-1">Intermedio</label>
  </fieldset>

  <input type="checkbox" id="terminos" name="terminos" required>
  <label for="terminos">Acepto los términos y condiciones</label>

  <button type="submit">Registrarme 🚀</button>
</form>
```

📌 Qué hace cada parte: cada `input` tiene `id` (para su `label`) y `name` (para el servidor). `type="email"`, `minlength`, `pattern` y `required` validan sin JS: el navegador no deja enviar si algo falla. `autocomplete` permite que el celular rellene solo. Los radios comparten `name="nivel"`, por eso solo se elige uno. `fieldset`/`legend` agrupan y dan contexto al lector de pantalla. El `option` con `value=""` + `required` obliga a elegir ciudad.

### ✅ Ejemplo resuelto: tarjeta de perfil
```html
<article class="perfil" aria-labelledby="perfil-nombre">
  <img class="perfil__foto" src="img/yafer.webp"
       alt="Foto de Yafer sonriendo" width="120" height="120">
  <h2 id="perfil-nombre" class="perfil__nombre">Yafer Torrez</h2>
  <p class="perfil__rol">Estudiante de Ciencias de la Computación · IA</p>
  <ul class="perfil__tags">
    <li>Python</li>
    <li>PyTorch</li>
    <li>HTML/CSS</li>
  </ul>
  <p class="perfil__ubicacion">
    <span aria-hidden="true">📍</span> Cochabamba, Bolivia
  </p>
  <nav aria-label="Redes de Yafer" class="perfil__redes">
    <a href="https://github.com/yftorrezg" target="_blank" rel="noopener">GitHub</a>
    <a href="mailto:hola@ejemplo.com">Correo</a>
  </nav>
</article>
```

📌 Qué hace cada parte: es un `article` porque la tarjeta es independiente (podría ir en otra página). La foto tiene `alt`, ancho y alto. Las clases siguen BEM (`perfil__foto`), así el CSS es ordenado. Las habilidades son una lista `ul`. El emoji va con `aria-hidden` para que el lector no diga "chincheta redonda". Los enlaces van en un `nav` con su propio nombre accesible.

💡 Consejo: arma estos tres ejemplos tú mismo sin mirar y luego dales estilo con la chuleta de CSS: es el mejor ejercicio para fijar lo aprendido.
🇬🇧 **landing page** = página de aterrizaje · **hero section** = bloque principal de portada · **call to action (CTA)** = llamada a la acción · **sign up** = registrarse · **profile card** = tarjeta de perfil · **pricing** /práising/ = precios
