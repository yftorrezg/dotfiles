# 🎨 CSS
> Diseña páginas bonitas: cascada, selectores, cajas, Flexbox, Grid, animaciones, responsive y modo oscuro.

## 🌱 Qué es CSS y cómo se escribe
CSS (Cascading Style Sheets, hojas de estilo en cascada) dice **cómo se ve** el HTML: colores, tamaños, posiciones, animaciones. Se escribe en **reglas**: un **selector** (a quién) y un bloque de **declaraciones** `propiedad: valor;` (qué cambiar).

- `selector { propiedad: valor; }` :: Forma de toda regla CSS
- `<link rel="stylesheet" href="estilos.css">` :: CSS externo: la forma correcta (va en el head)
- `<style> p { color: red; } </style>` :: CSS interno en el HTML (pruebas)
- `<p style="color: red">` :: En línea: gana casi siempre, pero ensucia el HTML
- `/* comentario */` :: Comentario en CSS (no existe el //)
- `F12 → Elements → Styles` :: DevTools: ver y probar estilos en vivo

```css
/* selector    { propiedad: valor; } */
h1 {
  color: #7c3aed;          /* color del texto */
  font-size: 2.5rem;       /* tamaño de letra */
  text-align: center;      /* centrado */
}

.tarjeta, .aviso {          /* varias reglas a la vez con coma */
  padding: 1rem;
  border-radius: 12px;
}
```

💡 Consejo: en DevTools puedes editar cualquier valor y verlo al instante; experimenta ahí y luego copia a tu archivo.
⚠️ Cuidado: olvidar el `;` hace que la siguiente declaración se rompa en silencio. CSS no da errores: simplemente ignora lo que no entiende.
🇬🇧 **stylesheet** /stáilshit/ = hoja de estilos · **rule** = regla · **selector** = selector · **property** /próperti/ = propiedad · **value** /váliu/ = valor · **declaration** = declaración

## ⚖️ Cascada, especificidad y herencia
Cuando dos reglas chocan sobre el mismo elemento, ¿cuál gana? CSS decide en este orden: **1) importancia** (`!important`), **2) especificidad** (qué tan preciso es el selector), **3) orden** (la última escrita gana). Además, algunas propiedades se **heredan** de padres a hijos.

### Tabla de especificidad
Se cuenta como un número de tres cifras (A, B, C). Gana el que tenga la cifra más alta empezando por la izquierda.

| Selector | Ejemplo | Peso (A,B,C) |
|---|---|---|
| Estilo en línea | `style="..."` | gana a todos (1,0,0,0) |
| ID | `#menu` | 1,0,0 |
| Clase, atributo, pseudo-clase | `.btn`, `[type="text"]`, `:hover` | 0,1,0 |
| Etiqueta, pseudo-elemento | `p`, `::before` | 0,0,1 |
| Universal y combinadores | `*`, `>`, `+`, `~` | 0,0,0 |
| Combinado | `nav .menu a:hover` | 0,2,2 |
| Combinado con ID | `#header .logo img` | 1,1,1 |
| Sin peso | `:where(.btn)` | 0,0,0 |
| Peso del argumento más fuerte | `:is(#id, .clase)` | 1,0,0 |

```css
p { color: black; }               /* 0,0,1 */
.intro { color: blue; }           /* 0,1,0 → gana a p */
#bienvenida { color: green; }     /* 1,0,0 → gana a .intro */
p.intro { color: red; }           /* 0,1,1 → gana a .intro, pierde con #bienvenida */

.btn { background: gray; }
.btn { background: purple; }      /* mismo peso → gana la última: purple */
```

### Herencia
- `color, font-*, line-height, text-align` :: Se heredan: ponlas en `body` y todo las usa
- `margin, padding, border, width, background` :: NO se heredan
- `inherit` :: Forzar que herede del padre: `border-color: inherit;`
- `initial` :: Volver al valor por defecto de CSS
- `unset` :: Hereda si es heredable; si no, valor inicial
- `revert` :: Volver al estilo por defecto del navegador
- `!important` :: Gana a todo; úsalo solo como último recurso
- `@layer base, componentes, utilidades;` :: Capas: controlas el orden de la cascada a mano

💡 Consejo: si tu estilo "no se aplica", abre DevTools: la regla tachada te dice quién la está ganando.
⚠️ Cuidado: usar `!important` para arreglar un conflicto crea una guerra de `!important`. Mejor baja la especificidad (usa clases, evita IDs para estilo).
🇬🇧 **cascade** /kaskéid/ = cascada · **specificity** /spesifísiti/ = especificidad · **inheritance** /injéritans/ = herencia · **override** /ouverráid/ = sobrescribir · **weight** /uéit/ = peso

## 🎯 Selectores, pseudo-clases y pseudo-elementos
Los selectores eligen **a qué elementos** aplicar el estilo. Dominarlos te ahorra llenar el HTML de clases.

### Básicos y combinadores
- `* { }` :: Universal: todos los elementos
- `p { }` :: Por etiqueta
- `.tarjeta { }` :: Por clase (lo más usado)
- `#menu { }` :: Por id (evítalo para estilos: pesa demasiado)
- `h1, h2, h3 { }` :: Grupo: varios selectores con la misma regla
- `.menu a { }` :: Descendiente: cualquier `a` dentro de `.menu`, a cualquier nivel
- `.menu > a { }` :: Hijo directo solamente
- `h2 + p { }` :: Hermano adyacente: el `p` justo después de un `h2`
- `h2 ~ p { }` :: Todos los hermanos `p` que vienen después del `h2`
- `.btn.activo { }` :: Ambas clases en el mismo elemento (sin espacio)

### Atributos
- `[disabled] { }` :: Tiene el atributo
- `[type="email"] { }` :: Valor exacto
- `a[href^="https"] { }` :: Empieza con
- `a[href$=".pdf"] { }` :: Termina con
- `[class*="col-"] { }` :: Contiene

### Pseudo-clases (estado o posición)
- `a:hover { }` :: Ratón encima
- `button:active { }` :: Mientras se presiona
- `input:focus { }` :: Tiene el foco
- `:focus-visible { }` :: Foco solo cuando se navega con teclado (ideal para anillos de foco)
- `a:visited { }` :: Enlace ya visitado
- `li:first-child { }` :: El primer hijo
- `li:last-child { }` :: El último hijo
- `li:nth-child(2n) { }` :: Pares (`odd` = impares, `3n+1` = 1, 4, 7...)
- `p:nth-of-type(2) { }` :: El segundo `p` entre sus hermanos
- `:not(.activo) { }` :: Todo lo que NO tenga la clase
- `:is(h1, h2, h3) a { }` :: Agrupa selectores de forma compacta
- `.tarjeta:has(img) { }` :: El padre que CONTIENE una imagen (el "selector padre")
- `:root { }` :: El elemento raíz (`html`): lugar para variables
- `:empty { }` :: Elemento sin contenido

### Pseudo-elementos (partes de un elemento)
- `.btn::before { content: "★ "; }` :: Contenido extra antes (necesita `content`)
- `.btn::after { content: ""; }` :: Contenido extra después (ideal para decoraciones)
- `p::first-letter { }` :: Primera letra (letra capital)
- `p::first-line { }` :: Primera línea
- `::selection { }` :: Texto seleccionado con el ratón
- `input::placeholder { }` :: El texto de ejemplo del input
- `li::marker { }` :: La viñeta o número de la lista

```css
/* Filas de tabla tipo cebra */
tbody tr:nth-child(even) { background: #f3f4f6; }

/* Enlaces a PDF con icono */
a[href$=".pdf"]::after { content: " 📄"; }

/* Tarjeta que cambia si tiene imagen */
.tarjeta:has(img) { padding-top: 0; }

/* Todos los items menos el último llevan separador */
.menu li:not(:last-child) { border-right: 1px solid #ddd; }
```

⚠️ Cuidado: `.a .b` (con espacio) es "b dentro de a"; `.a.b` (sin espacio) es "elemento con ambas clases". Un espacio cambia todo.
⚠️ Cuidado: `::before` y `::after` no aparecen si falta `content`, aunque sea `content: "";`.
🇬🇧 **descendant** /diséndant/ = descendiente · **child** /cháild/ = hijo · **sibling** = hermano · **hover** /jóver/ = pasar por encima · **pseudo** /súdou/ = pseudo · **odd / even** = impar / par

## 📏 Unidades
Las unidades **absolutas** (`px`) siempre miden lo mismo; las **relativas** dependen de algo (tamaño de letra, del padre o de la pantalla). Lo moderno es usar relativas para que la página se adapte y respete el tamaño de letra que eligió el usuario.

| Unidad | Relativa a | Uso típico |
|---|---|---|
| `px` | Pixel de pantalla (fijo) | Bordes, sombras, detalles finos |
| `rem` | Tamaño de letra del `html` (16px por defecto) | Tamaños de texto, márgenes, padding |
| `em` | Tamaño de letra del propio elemento | Padding de botones que crece con su texto |
| `%` | El tamaño del padre | Anchos fluidos |
| `vw` | 1% del ancho de la ventana | Títulos gigantes, secciones a pantalla completa |
| `vh` | 1% del alto de la ventana | Portadas de altura completa |
| `dvh` | 1% del alto visible real (celular con barra) | `min-height: 100dvh` en móviles |
| `fr` | Fracción del espacio libre (solo Grid) | Columnas `1fr 2fr` |
| `ch` | Ancho del carácter "0" | Ancho de lectura `max-width: 65ch` |
| `lh` | Alto de línea actual | Espaciados ligados al texto |

```css
html { font-size: 100%; }              /* 16px: respeta la elección del usuario */
h1 { font-size: 2.5rem; }              /* 40px */
.btn { font-size: 1rem; padding: 0.75em 1.5em; }  /* el padding crece con la letra */
.articulo { max-width: 65ch; }         /* líneas de lectura cómoda */
.portada { min-height: 100dvh; }       /* alto completo, también en el celular */
.contenedor { width: min(90%, 1100px); margin-inline: auto; }
```

💡 Consejo: regla práctica: `rem` para casi todo, `px` para bordes, `%`/`fr` para anchos, `ch` para textos largos.
⚠️ Cuidado: `em` se multiplica al anidar: una lista con `font-size: 1.2em` dentro de otra igual termina en 1.44×. Con `rem` no pasa.
🇬🇧 **unit** /iúnit/ = unidad · **relative** = relativa · **viewport width / height** = ancho / alto de la ventana · **fraction** = fracción · **root em (rem)** = em de la raíz

## 🌈 Colores
CSS acepta varios formatos de color. Todos sirven; la diferencia es qué tan fácil es **razonar** con ellos. `hsl` y `oklch` son los más cómodos para crear paletas porque separas el tono, la saturación y la luz.

- `color: tomato;` :: Por nombre (hay ~140)
- `color: #7c3aed;` :: Hexadecimal: rojo, verde, azul en base 16
- `color: #7c3aed80;` :: Hex con transparencia (80 ≈ 50%)
- `color: rgb(124 58 237);` :: Rojo, verde, azul de 0 a 255
- `color: rgb(0 0 0 / 50%);` :: Con transparencia (alfa)
- `color: hsl(262 83% 58%);` :: Tono (0-360°), saturación, luminosidad
- `color: oklch(60% 0.2 290);` :: Luminosidad, croma, tono: perceptualmente uniforme (moderno)
- `color-mix(in oklch, var(--acento), white 30%)` :: Mezclar colores: aclarar u oscurecer
- `currentColor` :: Usa el valor de `color` actual (perfecto para iconos y bordes)
- `transparent` :: Totalmente transparente
- `opacity: 0.5;` :: Transparencia de todo el elemento (incluidos sus hijos)
- `accent-color: #7c3aed;` :: Color de checkbox, radio y range nativos

```css
:root {
  --acento: oklch(58% 0.22 290);                          /* violeta */
  --acento-claro: color-mix(in oklch, var(--acento), white 40%);
  --acento-oscuro: color-mix(in oklch, var(--acento), black 25%);
}

/* Paleta con HSL: solo cambia la luminosidad */
.alerta     { background: hsl(0 85% 95%); color: hsl(0 70% 35%); border-color: hsl(0 70% 60%); }
.exito      { background: hsl(140 60% 94%); color: hsl(140 60% 25%); }
.sombreado  { background: rgb(0 0 0 / 6%); }
```

💡 Consejo: con `hsl` u `oklch`, para hacer un color más claro solo sube la luminosidad; con hex tendrías que recalcularlo todo.
⚠️ Cuidado: `opacity` vuelve transparente también el texto de dentro. Si solo quieres el fondo transparente, usa `background: rgb(0 0 0 / 50%)`.
🇬🇧 **hue** /jiú/ = tono · **saturation** = saturación · **lightness** = luminosidad · **alpha** /álfa/ = transparencia · **shade / tint** = más oscuro / más claro · **palette** = paleta

## 📦 Modelo de caja
En CSS **todo es una caja**. Cada caja tiene, de dentro hacia fuera: **contenido** → **padding** (relleno interior) → **border** (borde) → **margin** (espacio exterior que la separa de otras cajas).

```text
┌─────────────── margin ───────────────┐
│ ┌──────────── border ──────────────┐ │
│ │ ┌────────── padding ───────────┐ │ │
│ │ │          CONTENIDO           │ │ │
│ │ └──────────────────────────────┘ │ │
│ └──────────────────────────────────┘ │
└──────────────────────────────────────┘
```

- `*, *::before, *::after { box-sizing: border-box; }` :: El `width` incluye padding y borde (ponlo SIEMPRE)
- `padding: 1rem;` :: Relleno interior en los 4 lados
- `padding: 1rem 2rem;` :: Arriba/abajo 1rem, izquierda/derecha 2rem
- `margin: 10px 20px 30px 40px;` :: Arriba, derecha, abajo, izquierda (sentido del reloj)
- `margin-inline: auto;` :: Centrar un bloque horizontalmente (necesita ancho)
- `padding-block: 2rem;` :: Arriba y abajo (propiedades lógicas)
- `width: min(90%, 800px);` :: Ancho fluido con tope máximo
- `max-width: 100%;` :: Nunca más ancho que el padre
- `min-height: 300px;` :: Alto mínimo (crece si el contenido es mayor)
- `aspect-ratio: 16 / 9;` :: Mantener proporción (videos, tarjetas)
- `overflow: hidden;` :: Recorta lo que se sale (`auto` pone scroll solo si hace falta)
- `outline: 2px solid;` :: Contorno que NO ocupa espacio (usado en foco)

```css
*, *::before, *::after { box-sizing: border-box; }

.caja {
  width: 300px;
  padding: 20px;
  border: 5px solid #333;
  margin: 2rem auto;
}
/* Con border-box ocupa 300px exactos.
   Sin border-box ocuparía 300 + 40 + 10 = 350px. */
```

⚠️ Cuidado: **colapso de márgenes**: dos márgenes verticales que se tocan no se suman, gana el mayor (20px + 30px = 30px). En Flexbox y Grid no pasa.
💡 Consejo: para separar hijos de un contenedor flex o grid usa `gap` en vez de márgenes: más simple y sin colapsos.
🇬🇧 **box model** = modelo de caja · **padding** = relleno · **border** = borde · **margin** = margen · **overflow** = desbordamiento · **aspect ratio** /áspect réishio/ = proporción

## 🧊 Display
`display` decide **cómo se comporta** una caja respecto a las demás: si ocupa toda la fila, si se pone al lado de otras, o si organiza a sus hijos con Flexbox o Grid.

| Valor | Comportamiento | Ejemplos por defecto |
|---|---|---|
| `block` | Ocupa todo el ancho, empieza en línea nueva, acepta width/height | `div`, `p`, `h1`, `section` |
| `inline` | Va dentro del texto; ignora width/height y margen vertical | `span`, `a`, `strong` |
| `inline-block` | En línea, pero acepta width/height/padding completos | Botones, badges |
| `flex` | El elemento es bloque y sus hijos se ordenan en una dimensión | Menús, barras |
| `grid` | El elemento es bloque y sus hijos van en filas y columnas | Galerías, layouts |
| `inline-flex` | Como flex, pero el contenedor va en línea | Botón con icono |
| `none` | Desaparece por completo (no ocupa espacio) | Menú cerrado |
| `contents` | La caja desaparece, sus hijos suben al padre | Casos especiales |

- `display: none;` :: Quita el elemento (no ocupa espacio, lector de pantalla tampoco lo lee)
- `visibility: hidden;` :: Invisible pero sigue ocupando su espacio
- `opacity: 0;` :: Invisible, ocupa espacio y aún recibe clics

```css
.badge {
  display: inline-block;
  padding: 0.2em 0.6em;
  border-radius: 999px;
  background: #ede9fe;
}
.oculto { display: none; }
```

🇬🇧 **block** = bloque · **inline** /inláin/ = en línea · **hidden** /jíden/ = oculto · **visibility** = visibilidad · **flow** /flóu/ = flujo (normal de la página)

## ↔️ Flexbox a fondo
Flexbox organiza elementos en **una dimensión**: una fila o una columna. Tiene un **eje principal** (la dirección de `flex-direction`) y un **eje cruzado** (perpendicular). `justify-content` alinea en el principal; `align-items` en el cruzado. Es ideal para menús, barras, centrar cosas y componentes pequeños.

### Propiedades del contenedor
| Propiedad | Valores | Qué hace |
|---|---|---|
| `display` | `flex` | Activa Flexbox en los hijos directos |
| `flex-direction` | `row`, `column`, `row-reverse` | Dirección del eje principal |
| `justify-content` | `flex-start`, `center`, `space-between`, `space-around`, `space-evenly` | Reparte en el eje principal |
| `align-items` | `stretch`, `center`, `flex-start`, `flex-end`, `baseline` | Alinea en el eje cruzado |
| `flex-wrap` | `nowrap`, `wrap` | Permite saltar a otra línea |
| `gap` | `1rem` o `1rem 2rem` | Espacio entre hijos |
| `align-content` | `center`, `space-between` | Reparte las líneas (si hay `wrap`) |
| `flex-flow` | `row wrap` | Atajo de dirección + wrap |

### Propiedades de los hijos
| Propiedad | Ejemplo | Qué hace |
|---|---|---|
| `flex-grow` | `1` | Cuánto crece para llenar el espacio libre |
| `flex-shrink` | `0` | Cuánto se encoge (0 = nunca) |
| `flex-basis` | `200px` | Tamaño inicial antes de crecer o encoger |
| `flex` | `1` o `1 1 200px` | Atajo de grow, shrink, basis |
| `align-self` | `flex-end` | Alinea solo a este hijo |
| `order` | `-1` | Cambia el orden visual (no el del teclado) |
| `margin-left` | `auto` | Empuja el hijo (y los siguientes) al extremo |

### ✅ Ejemplo resuelto: centrar cualquier cosa
```css
.centrar {
  display: flex;
  justify-content: center;   /* horizontal (eje principal = fila) */
  align-items: center;       /* vertical (eje cruzado) */
  min-height: 100dvh;        /* hace falta altura para centrar verticalmente */
}
```

📌 Explicación: `display: flex` convierte a los hijos en elementos flex. Como la dirección por defecto es `row`, `justify-content` mueve en horizontal y `align-items` en vertical. Sin `min-height`, el contenedor mide lo mismo que su hijo y no hay espacio para centrar.

### ✅ Ejemplo resuelto: navbar
```html
<nav class="navbar">
  <a href="/" class="logo">🤖 IAprende</a>
  <ul class="menu">
    <li><a href="/cursos">Cursos</a></li>
    <li><a href="/blog">Blog</a></li>
  </ul>
  <a href="/login" class="btn">Entrar</a>
</nav>
```

```css
.navbar {
  display: flex;
  align-items: center;      /* todos alineados al centro vertical */
  gap: 2rem;
  padding: 1rem 2rem;
}
.menu {
  display: flex;
  gap: 1.5rem;
  list-style: none;
  margin: 0;
  padding: 0;
}
.btn { margin-left: auto; } /* empuja el botón a la derecha */
```

📌 Explicación: el `nav` y la `ul` son ambos contenedores flex (flex anidado). `margin-left: auto` en el botón se come todo el espacio sobrante a su izquierda, así queda pegado a la derecha mientras logo y menú quedan a la izquierda.

### ✅ Ejemplo resuelto: fila de cards que se adapta
```css
.cards {
  display: flex;
  flex-wrap: wrap;          /* si no caben, bajan a otra fila */
  gap: 1.5rem;
}
.card {
  flex: 1 1 250px;          /* crece, se encoge, ideal 250px */
  padding: 1.5rem;
  border-radius: 1rem;
  background: #f5f3ff;
  display: flex;
  flex-direction: column;   /* contenido de la card en columna */
}
.card .btn { margin-top: auto; }  /* botón siempre pegado abajo */
```

📌 Explicación: cada card parte de 250px y crece para llenar la fila; con `wrap` bajan a otra fila cuando no caben, sin media queries. Dentro, la columna flex + `margin-top: auto` alinea los botones abajo aunque los textos tengan largos distintos.

💡 Consejo: juega Flexbox Froggy (flexboxfroggy.com): en 20 minutos dominas `justify-content` y `align-items`.
⚠️ Cuidado: `display: flex` solo afecta a los hijos **directos**, no a los nietos. Si quieres ordenar los nietos, ese hijo también necesita `display: flex`.
⚠️ Cuidado: si cambias a `flex-direction: column`, los ejes se intercambian: ahora `justify-content` es vertical y `align-items` horizontal.
🇬🇧 **main axis** /méin áksis/ = eje principal · **cross axis** = eje cruzado · **wrap** /rap/ = envolver, saltar de línea · **grow / shrink** = crecer / encoger · **justify** = justificar, repartir · **align** /aláin/ = alinear

## 🔲 Grid a fondo
Grid organiza en **dos dimensiones**: filas y columnas a la vez. Defines la cuadrícula en el contenedor y luego colocas a los hijos. Es lo mejor para layouts de página completos y galerías.

### Propiedades principales
- `display: grid;` :: Activa Grid
- `grid-template-columns: 200px 1fr 1fr;` :: 3 columnas: una fija y dos que reparten el resto
- `grid-template-columns: repeat(4, 1fr);` :: 4 columnas iguales
- `grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));` :: Tantas columnas como quepan (mín. 220px): responsive sin media queries
- `grid-template-rows: auto 1fr auto;` :: Filas: cabecera, contenido que se estira, pie
- `gap: 1rem 2rem;` :: Espacio entre filas y entre columnas
- `grid-column: 1 / 3;` :: El hijo va de la línea 1 a la 3 (ocupa 2 columnas)
- `grid-column: span 2;` :: Ocupa 2 columnas desde donde caiga
- `grid-column: 1 / -1;` :: De la primera a la última línea: ancho completo
- `grid-row: span 2;` :: Ocupa 2 filas
- `place-items: center;` :: Centra el contenido de cada celda (align + justify)
- `grid-auto-rows: 200px;` :: Alto de las filas creadas automáticamente
- `grid-auto-flow: dense;` :: Rellena huecos con elementos posteriores
- `grid-template-columns: subgrid;` :: El hijo usa las mismas columnas que el padre

### Template areas: dibujar el layout con nombres
Puedes "dibujar" la página con texto: cada palabra es un área y luego asignas cada hijo a su área.

```css
.pagina {
  display: grid;
  grid-template-columns: 250px 1fr;
  grid-template-rows: auto 1fr auto;
  grid-template-areas:
    "cabecera cabecera"
    "lateral  contenido"
    "pie      pie";
  min-height: 100dvh;
  gap: 1rem;
}
.pagina > header { grid-area: cabecera; }
.pagina > aside  { grid-area: lateral; }
.pagina > main   { grid-area: contenido; }
.pagina > footer { grid-area: pie; }
```

| auto-fit vs auto-fill | Qué hace |
|---|---|
| `auto-fit` | Si sobran columnas vacías, las colapsa y estira los elementos existentes |
| `auto-fill` | Mantiene columnas vacías: los elementos no se estiran más allá |

### ✅ Ejemplo resuelto: galería de fotos
```css
.galeria {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  grid-auto-rows: 200px;
  gap: 0.75rem;
}
.galeria img {
  width: 100%;
  height: 100%;
  object-fit: cover;          /* recorta sin deformar */
  border-radius: 0.5rem;
}
.galeria .destacada {
  grid-column: span 2;
  grid-row: span 2;           /* foto grande de 2×2 */
}
```

📌 Explicación: `repeat(auto-fit, minmax(200px, 1fr))` crea tantas columnas de al menos 200px como quepan y las estira para llenar: 1 columna en el celular, 5 en un monitor. `grid-auto-rows` fija el alto. `object-fit: cover` evita fotos estiradas. La clase `destacada` ocupa un bloque de 2×2.

### ✅ Ejemplo resuelto: layout de página responsive
```css
.pagina {
  display: grid;
  grid-template-areas:
    "cabecera"
    "contenido"
    "lateral"
    "pie";
  gap: 1rem;
}
@media (min-width: 768px) {
  .pagina {
    grid-template-columns: 1fr 300px;
    grid-template-areas:
      "cabecera  cabecera"
      "contenido lateral"
      "pie       pie";
  }
}
```

📌 Explicación: en el celular todo va en una columna (mobile first). Desde 768px solo se redibujan las áreas y aparece la barra lateral a la derecha; los hijos no cambian porque ya tienen su `grid-area` asignada.

💡 Consejo: ¿Flex o Grid? Flex cuando piensas en **contenido** que fluye en una línea (menú, botones). Grid cuando piensas en la **estructura** con filas y columnas (página, galería). Se combinan sin problema.
⚠️ Cuidado: en `grid-template-areas` cada fila debe tener el mismo número de palabras y las áreas deben ser rectángulos; si no, la regla entera se ignora.
🇬🇧 **grid** = cuadrícula · **track** = pista (fila o columna) · **area** /éria/ = área · **span** = abarcar · **fit / fill** = ajustar / rellenar · **template** = plantilla

## 📍 Posicionamiento
`position` saca o ajusta un elemento respecto al flujo normal. Se combina con `top`, `right`, `bottom`, `left` (o `inset`) y `z-index`.

| Valor | Se mueve respecto a | ¿Ocupa su hueco? | Uso típico |
|---|---|---|---|
| `static` | Nada (por defecto) | Sí | Normal |
| `relative` | Su posición original | Sí | Referencia para hijos absolute |
| `absolute` | El ancestro posicionado más cercano | No | Badges, iconos en esquinas |
| `fixed` | La ventana | No | Botón de WhatsApp, cabecera fija |
| `sticky` | Se pega al hacer scroll dentro de su padre | Sí | Cabeceras, encabezados de tabla |

- `position: relative;` :: Convierte al padre en la referencia de sus hijos absolute
- `position: absolute; top: 0; right: 0;` :: Pegado a la esquina superior derecha del padre
- `inset: 0;` :: Atajo de top/right/bottom/left = 0 (cubre todo el padre)
- `position: sticky; top: 0;` :: Se queda pegado arriba al hacer scroll
- `position: fixed; bottom: 1rem; right: 1rem;` :: Fijo en la esquina de la pantalla
- `z-index: 10;` :: Quién queda encima (solo funciona en elementos posicionados, flex o grid)
- `isolation: isolate;` :: Crea un contexto de apilado nuevo (z-index aislado)

```css
.tarjeta { position: relative; }
.tarjeta .etiqueta {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  background: crimson;
  color: white;
  padding: 0.2rem 0.6rem;
  border-radius: 999px;
}

.cabecera {
  position: sticky;
  top: 0;
  z-index: 100;
  background: white;
}

.overlay {             /* capa oscura sobre una imagen */
  position: absolute;
  inset: 0;
  background: rgb(0 0 0 / 40%);
}
```

⚠️ Cuidado: si tu `absolute` se va a la esquina de la página, es porque el padre no tiene `position: relative`.
⚠️ Cuidado: `sticky` no funciona si algún ancestro tiene `overflow: hidden` o si no le das `top`.
🇬🇧 **position** = posición · **sticky** = pegajoso · **fixed** = fijo · **overlay** /óverlei/ = capa superpuesta · **stacking context** = contexto de apilado · **offset** = desplazamiento

## 🔠 Tipografía
El texto es el 90% de una web. Una buena tipografía se nota en tres cosas: **fuente legible**, **tamaño suficiente** y **alto de línea** cómodo.

- `font-family: "Inter", system-ui, sans-serif;` :: Fuente con respaldos si no carga
- `font-size: 1.125rem;` :: Tamaño (18px)
- `font-weight: 700;` :: Grosor: 400 normal, 600 seminegrita, 700 negrita
- `font-style: italic;` :: Cursiva
- `line-height: 1.6;` :: Alto de línea SIN unidad: se multiplica por el tamaño de cada elemento
- `letter-spacing: 0.05em;` :: Espacio entre letras (útil en mayúsculas)
- `text-align: center;` :: Alineación
- `text-transform: uppercase;` :: Mayúsculas
- `text-decoration: none;` :: Quitar subrayado a enlaces
- `text-underline-offset: 4px;` :: Separar el subrayado del texto
- `text-wrap: balance;` :: Reparte las líneas de los títulos de forma equilibrada
- `text-overflow: ellipsis;` :: Cortar con "…" (junto a `white-space: nowrap; overflow: hidden;`)
- `-webkit-line-clamp: 3;` :: Limitar a 3 líneas (con `display: -webkit-box; -webkit-box-orient: vertical; overflow: hidden;`)
- `font: 600 1.1rem/1.5 "Inter", sans-serif;` :: Atajo: peso, tamaño/alto de línea, fuente

### Google Fonts
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=JetBrains+Mono&display=swap" rel="stylesheet">
```

```css
body {
  font-family: "Inter", system-ui, sans-serif;
  font-size: 1rem;
  line-height: 1.6;
  color: #1f2937;
}
h1, h2, h3 {
  line-height: 1.15;            /* los títulos van más apretados */
  text-wrap: balance;
}
code { font-family: "JetBrains Mono", monospace; }
p { max-width: 65ch; }          /* 50-75 caracteres por línea */
```

💡 Consejo: `display=swap` en Google Fonts muestra el texto con la fuente del sistema mientras descarga la tuya; nada de texto invisible.
⚠️ Cuidado: no uses más de 2 familias de fuente ni texto menor a 16px para párrafos; en el celular se vuelve ilegible.
🇬🇧 **font** = fuente · **typeface** /táipfeis/ = tipo de letra · **weight** = grosor · **line height** = alto de línea · **fallback** /fólbak/ = respaldo · **serif / sans-serif** = con remates / sin remates

## 🖼️ Fondos y degradados
- `background-color: #f5f3ff;` :: Color de fondo
- `background-image: url("img/fondo.webp");` :: Imagen de fondo
- `background-size: cover;` :: La imagen cubre todo (recorta si hace falta); `contain` la muestra entera
- `background-position: center;` :: Dónde se centra la imagen
- `background-repeat: no-repeat;` :: No repetir en mosaico
- `background-attachment: fixed;` :: Efecto parallax simple
- `linear-gradient(135deg, #7c3aed, #ec4899)` :: Degradado lineal en diagonal
- `radial-gradient(circle at top, #a78bfa, transparent 60%)` :: Degradado circular
- `conic-gradient(red, yellow, green, red)` :: Degradado cónico (gráficos de torta)
- `background-clip: text;` :: Recorta el fondo con la forma del texto (texto degradado)
- `object-fit: cover;` :: Como `background-size: cover` pero para `img` y `video`
- `backdrop-filter: blur(10px);` :: Desenfoca lo que hay DETRÁS (efecto vidrio)

```css
.hero {
  /* capas: la primera queda encima */
  background:
    linear-gradient(rgb(0 0 0 / 55%), rgb(0 0 0 / 55%)),
    url("img/illimani.webp") center / cover no-repeat;
  color: white;
  min-height: 70vh;
}

.texto-degradado {
  background: linear-gradient(90deg, #7c3aed, #ec4899);
  background-clip: text;
  color: transparent;
}

.vidrio {
  background: rgb(255 255 255 / 15%);
  backdrop-filter: blur(12px);
  border: 1px solid rgb(255 255 255 / 25%);
}
```

💡 Consejo: pon un degradado oscuro semitransparente sobre las fotos de fondo; así el texto blanco siempre se lee.
🇬🇧 **background** = fondo · **gradient** /gréidient/ = degradado · **cover** = cubrir · **repeat** = repetir · **blur** /blér/ = desenfoque · **glassmorphism** = efecto vidrio

## 🔳 Bordes y sombras
- `border: 2px solid #e5e7eb;` :: Grosor, estilo (`solid`, `dashed`, `dotted`) y color
- `border-bottom: 3px solid var(--acento);` :: Solo un lado
- `border-radius: 12px;` :: Esquinas redondeadas
- `border-radius: 50%;` :: Círculo (si es cuadrado)
- `border-radius: 999px;` :: Forma de píldora
- `box-shadow: 0 4px 12px rgb(0 0 0 / 10%);` :: Sombra: x, y, desenfoque, color
- `box-shadow: 0 0 0 3px #a78bfa;` :: Sin desenfoque: un "anillo" que no ocupa espacio
- `box-shadow: inset 0 2px 4px rgb(0 0 0 / 10%);` :: Sombra interior
- `text-shadow: 0 2px 4px rgb(0 0 0 / 50%);` :: Sombra del texto
- `filter: drop-shadow(0 4px 6px rgb(0 0 0 / 30%));` :: Sombra que sigue la forma (PNG con transparencia)
- `outline-offset: 3px;` :: Separa el contorno del elemento

```css
.card {
  border: 1px solid #e5e7eb;
  border-radius: 1rem;
  box-shadow:
    0 1px 2px rgb(0 0 0 / 6%),
    0 8px 24px rgb(0 0 0 / 8%);   /* dos sombras = más realista */
}
.avatar {
  width: 96px;
  aspect-ratio: 1;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid white;
}
```

💡 Consejo: las sombras suaves y grandes con poca opacidad (5-15%) se ven profesionales; las negras y duras se ven de 2005.
🇬🇧 **shadow** /shádou/ = sombra · **rounded corners** = esquinas redondeadas · **dashed / dotted** = discontinuo / punteado · **inset** = hacia dentro · **ring** = anillo

## 🔄 Transformaciones
`transform` mueve, gira o escala un elemento **sin afectar** a los demás (no empuja nada). Es muy eficiente para animar porque lo hace la tarjeta gráfica.

- `transform: translateY(-4px);` :: Mover hacia arriba 4px
- `transform: translate(-50%, -50%);` :: Mover la mitad de su propio tamaño (centrado clásico con absolute)
- `transform: scale(1.05);` :: Agrandar 5%
- `transform: rotate(45deg);` :: Girar 45°
- `transform: skewX(-10deg);` :: Inclinar
- `transform: translateY(-4px) scale(1.02);` :: Combinar (se aplican de derecha a izquierda)
- `transform-origin: top left;` :: Punto desde el que gira o escala
- `rotate: 10deg; scale: 1.1; translate: 0 -4px;` :: Propiedades individuales modernas (se animan por separado)
- `perspective: 800px;` :: Profundidad 3D en el padre
- `transform: rotateY(180deg);` :: Giro 3D (tarjeta que se voltea)

```css
.icono:hover { rotate: 15deg; scale: 1.1; }

.centrado-absoluto {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
```

⚠️ Cuidado: escribir dos `transform` en reglas distintas no los suma: el segundo reemplaza al primero. Combínalos en una línea o usa `rotate`, `scale` y `translate` por separado.
🇬🇧 **transform** = transformar · **translate** = desplazar · **scale** /skéil/ = escalar · **rotate** /routéit/ = rotar · **skew** /skiú/ = inclinar · **origin** = origen

## 🎞️ Transiciones y animaciones
Una **transición** anima el cambio entre dos estados (normal → hover). Una **animación** con `@keyframes` define una secuencia completa que puede repetirse sola.

### Transiciones
- `transition: background-color 200ms ease;` :: Propiedad, duración, curva
- `transition: transform 300ms ease, opacity 300ms;` :: Varias propiedades
- `transition: all 0.2s;` :: Todas (cómodo, pero menos eficiente)
- `transition-delay: 100ms;` :: Esperar antes de empezar
- `ease, linear, ease-in, ease-out, ease-in-out` :: Curvas de velocidad
- `cubic-bezier(0.34, 1.56, 0.64, 1)` :: Curva propia (esta "rebota")

### Animaciones
- `@keyframes nombre { from { } to { } }` :: Define los pasos de la animación
- `animation: latir 1s ease-in-out infinite alternate;` :: Nombre, duración, curva, repeticiones, dirección
- `animation-iteration-count: 3;` :: Repetir 3 veces (`infinite` = siempre)
- `animation-fill-mode: forwards;` :: Quedarse en el último fotograma
- `animation-delay: 0.5s;` :: Retraso inicial
- `animation-play-state: paused;` :: Pausar
- `@media (prefers-reduced-motion: reduce) { }` :: Respetar a usuarios que piden menos movimiento

```css
@keyframes aparecer {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes girar {
  to { rotate: 360deg; }
}
@keyframes latir {
  0%, 100% { scale: 1; }
  50%      { scale: 1.08; }
}

.seccion  { animation: aparecer 600ms ease-out both; }
.spinner  {
  width: 2rem; aspect-ratio: 1;
  border: 3px solid #ddd; border-top-color: #7c3aed;
  border-radius: 50%;
  animation: girar 0.8s linear infinite;
}
.corazon  { animation: latir 1.2s ease-in-out infinite; }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

### ✅ Ejemplo resuelto: botón animado
```css
.btn {
  position: relative;
  overflow: hidden;
  padding: 0.8em 1.8em;
  border: none;
  border-radius: 999px;
  background: linear-gradient(135deg, #7c3aed, #ec4899);
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: translate 200ms ease, box-shadow 200ms ease;
}
.btn::after {                       /* brillo que cruza el botón */
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(120deg, transparent 30%, rgb(255 255 255 / 40%), transparent 70%);
  translate: -100% 0;
  transition: translate 600ms ease;
}
.btn:hover {
  translate: 0 -3px;
  box-shadow: 0 10px 24px rgb(124 58 237 / 40%);
}
.btn:hover::after { translate: 100% 0; }
.btn:active { translate: 0 0; }
.btn:focus-visible { outline: 3px solid #a78bfa; outline-offset: 3px; }
```

📌 Explicación: el botón tiene `position: relative` y `overflow: hidden` para contener el brillo. El `::after` es una franja clara que empieza fuera a la izquierda (`-100%`); al hacer hover se desliza al otro lado. El botón sube 3px y gana sombra con una transición suave; al presionar (`:active`) baja, dando sensación de clic. `:focus-visible` muestra un anillo solo con teclado.

💡 Consejo: anima solo `transform`/`translate`/`scale`/`rotate` y `opacity`: son baratos. Animar `width`, `top` o `margin` hace que el navegador recalcule toda la página.
⚠️ Cuidado: `transition` va en el estado normal, no en el `:hover`; si no, la animación solo ocurre al entrar y no al salir.
🇬🇧 **transition** = transición · **keyframe** /kíifreim/ = fotograma clave · **duration** = duración · **easing** /ísing/ = curva de velocidad · **delay** /diléi/ = retraso · **loop** = bucle

## 📱 Responsive design
Una web **responsive** se adapta a cualquier pantalla. La estrategia moderna es **mobile first**: escribes los estilos para el celular (lo más simple) y vas añadiendo con `min-width` para pantallas más grandes.

- `<meta name="viewport" content="width=device-width, initial-scale=1.0">` :: Sin esto nada de lo demás funciona en el celular
- `img, video { max-width: 100%; height: auto; }` :: Medios que nunca se desbordan
- `@media (min-width: 768px) { }` :: Desde tablet hacia arriba (mobile first)
- `@media (max-width: 600px) { }` :: Solo pantallas pequeñas (desktop first)
- `@media (768px <= width < 1024px) { }` :: Sintaxis de rango moderna
- `@media (orientation: landscape) { }` :: Celular en horizontal
- `@media (hover: hover) { }` :: Solo dispositivos con ratón (evita hovers pegados en táctil)
- `@media print { }` :: Estilos para imprimir
- `font-size: clamp(1.75rem, 4vw + 1rem, 3.5rem);` :: Tamaño fluido: mínimo, ideal, máximo
- `width: min(100% - 2rem, 1100px);` :: Contenedor con margen lateral y ancho máximo
- `container-type: inline-size;` :: Convierte el elemento en contenedor consultable
- `@container (min-width: 400px) { }` :: El componente cambia según SU ancho, no el de la pantalla

| Breakpoint típico | Dispositivo |
|---|---|
| `< 640px` | Celular (estilos base) |
| `min-width: 640px` | Celular grande / tablet pequeña |
| `min-width: 768px` | Tablet |
| `min-width: 1024px` | Laptop |
| `min-width: 1280px` | Escritorio |

```css
/* Base: celular */
.productos { display: grid; gap: 1rem; }
.titulo { font-size: clamp(1.75rem, 5vw, 3rem); }

/* Tablet */
@media (min-width: 768px) {
  .productos { grid-template-columns: repeat(2, 1fr); }
}
/* Laptop */
@media (min-width: 1024px) {
  .productos { grid-template-columns: repeat(4, 1fr); }
}

/* Container query: la card se pone horizontal si SU contenedor es ancho */
.zona-cards { container-type: inline-size; }
@container (min-width: 450px) {
  .card { display: flex; gap: 1rem; }
  .card img { width: 40%; }
}
```

💡 Consejo: con `clamp()` para tipografía y `auto-fit/minmax` para grids, muchas veces ya no necesitas media queries.
⚠️ Cuidado: prueba en DevTools (Ctrl+Shift+M) con 360px de ancho: es el celular Android más común en Bolivia. Si aparece scroll horizontal, algo se desborda.
🇬🇧 **responsive** = adaptable · **breakpoint** /bréikpoint/ = punto de quiebre · **media query** /míidia kuíri/ = consulta de medios · **mobile first** = primero el celular · **fluid** /flúid/ = fluido · **container** = contenedor

## 🎛️ Variables CSS y tema claro/oscuro
Las **custom properties** (variables) guardan valores para reutilizarlos. Se definen con `--nombre` y se usan con `var(--nombre)`. A diferencia de las de Sass, viven en el navegador: se heredan, se pueden cambiar con media queries y con JavaScript. Son la base de cualquier sistema de temas.

- `:root { --acento: #7c3aed; }` :: Definir variable global
- `color: var(--acento);` :: Usarla
- `var(--sombra, none)` :: Valor de respaldo si la variable no existe
- `.card { --pad: 1rem; padding: var(--pad); }` :: Variable local a un componente
- `.card.grande { --pad: 2rem; }` :: Cambias la variable y todo lo que la usa se actualiza
- `calc(var(--espacio) * 2)` :: Operar con variables
- `color-scheme: light dark;` :: Avisa al navegador: adapta scrollbars e inputs nativos
- `@media (prefers-color-scheme: dark) { }` :: Detecta el modo oscuro del sistema
- `light-dark(#111, #eee)` :: Elige color según el esquema activo (moderno)
- `el.style.setProperty("--acento", "red")` :: Cambiar una variable desde JS

### ✅ Ejemplo resuelto: modo oscuro
```css
:root {
  color-scheme: light dark;
  --fondo: #ffffff;
  --superficie: #f4f4f5;
  --texto: #18181b;
  --texto-suave: #52525b;
  --acento: #7c3aed;
  --borde: #e4e4e7;
}

/* 1) Sigue al sistema, salvo que el usuario haya forzado claro */
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --fondo: #0f0f14;
    --superficie: #1c1c24;
    --texto: #f4f4f5;
    --texto-suave: #a1a1aa;
    --acento: #a78bfa;
    --borde: #2e2e38;
  }
}
/* 2) Oscuro forzado con un botón */
:root[data-theme="dark"] {
  --fondo: #0f0f14;
  --superficie: #1c1c24;
  --texto: #f4f4f5;
  --texto-suave: #a1a1aa;
  --acento: #a78bfa;
  --borde: #2e2e38;
}

body {
  background: var(--fondo);
  color: var(--texto);
  transition: background-color 300ms, color 300ms;
}
.card {
  background: var(--superficie);
  border: 1px solid var(--borde);
}
a { color: var(--acento); }
```

```js
// Botón que alterna el tema y lo recuerda
const boton = document.querySelector("#tema");
const raiz = document.documentElement;
const guardado = localStorage.getItem("tema");
if (guardado) raiz.dataset.theme = guardado;

boton.addEventListener("click", () => {
  const oscuroAhora = raiz.dataset.theme === "dark" ||
    (!raiz.dataset.theme && matchMedia("(prefers-color-scheme: dark)").matches);
  raiz.dataset.theme = oscuroAhora ? "light" : "dark";
  localStorage.setItem("tema", raiz.dataset.theme);
});
```

📌 Explicación: los componentes nunca usan colores directos, solo variables (`var(--fondo)`). Para cambiar de tema basta redefinir las variables. El bloque 1 respeta la preferencia del sistema; el bloque 2 aplica cuando el usuario pulsa el botón, que pone `data-theme="dark"` en `html`. El JS guarda la elección en `localStorage` para la próxima visita.

💡 Consejo: en modo oscuro no uses negro puro `#000` ni blanco puro de texto: un gris muy oscuro y un blanco roto cansan menos la vista.
⚠️ Cuidado: las variables CSS distinguen mayúsculas (`--Acento` no es `--acento`) y no se pueden usar dentro de media queries como `@media (min-width: var(--x))`.
🇬🇧 **custom property** = propiedad personalizada (variable) · **theme** /zíim/ = tema · **dark mode** = modo oscuro · **fallback** = respaldo · **toggle** /tógol/ = alternar · **color scheme** = esquema de color

## 📝 Estilos de formularios
Los formularios tienen pseudo-clases propias que reflejan su **estado**: válido, inválido, obligatorio, marcado... Así das feedback visual sin escribir JavaScript.

- `input:focus-visible { }` :: Campo enfocado con teclado
- `input:required { }` :: Campos obligatorios
- `input:optional { }` :: Campos opcionales
- `input:valid { } / input:invalid { }` :: Cumple o no la validación (`required`, `pattern`, `type`...)
- `input:user-invalid { }` :: Inválido solo DESPUÉS de que el usuario lo tocó (no grita al cargar)
- `input:placeholder-shown { }` :: Cuando se ve el placeholder (campo vacío)
- `input:checked { }` :: Checkbox o radio marcado
- `input:disabled { }` :: Desactivado
- `input:read-only { }` :: Solo lectura
- `input:in-range { } / input:out-of-range { }` :: Número dentro o fuera de `min`/`max`
- `form:has(:user-invalid) button { }` :: Cambiar el botón si algún campo está mal
- `accent-color: var(--acento);` :: Pinta checkbox, radio y range con tu color
- `appearance: none;` :: Quita el estilo nativo para diseñar el control desde cero

```css
input, select, textarea {
  font: inherit;                    /* los inputs NO heredan la fuente por defecto */
  width: 100%;
  padding: 0.7rem 0.9rem;
  border: 1.5px solid var(--borde, #d4d4d8);
  border-radius: 0.6rem;
  background: var(--superficie, white);
  transition: border-color 150ms, box-shadow 150ms;
}
input:focus-visible {
  outline: none;
  border-color: #7c3aed;
  box-shadow: 0 0 0 4px rgb(124 58 237 / 20%);
}
input:user-invalid {
  border-color: #dc2626;
}
input:user-invalid + .error { display: block; }  /* mensaje de error al lado */
.error { display: none; color: #dc2626; font-size: 0.875rem; }

label:has(input:checked) { font-weight: 600; }   /* la opción elegida resalta */
input[type="checkbox"], input[type="radio"] { accent-color: #7c3aed; width: auto; }
```

⚠️ Cuidado: `:invalid` se activa apenas carga la página (un campo `required` vacío ya es inválido) y todo sale en rojo. Usa `:user-invalid`.
💡 Consejo: pon `font: inherit;` a inputs y botones; si no, usan una fuente pequeña del sistema distinta al resto.
🇬🇧 **valid / invalid** = válido / inválido · **checked** = marcado · **disabled** = desactivado · **feedback** /fíidbak/ = retroalimentación · **field** /fíild/ = campo

## ✨ Buenas prácticas: reset, BEM y orden
### Reset moderno
Cada navegador trae estilos por defecto distintos. Un pequeño **reset** los iguala y corrige comportamientos molestos.

```css
*, *::before, *::after { box-sizing: border-box; }
* { margin: 0; }
html { -webkit-text-size-adjust: none; text-size-adjust: none; }
body { min-height: 100dvh; line-height: 1.6; -webkit-font-smoothing: antialiased; }
img, picture, video, canvas, svg { display: block; max-width: 100%; }
input, button, textarea, select { font: inherit; }
p, h1, h2, h3, h4, h5, h6 { overflow-wrap: break-word; }
h1, h2, h3 { text-wrap: balance; line-height: 1.15; }
```

### BEM: nombres de clases ordenados
**BEM** = Bloque, Elemento, Modificador. El bloque es el componente (`.card`), el elemento es una parte (`.card__titulo`, con dos guiones bajos) y el modificador una variante (`.card--destacada`, con dos guiones).

```css
.card { }                  /* Bloque */
.card__imagen { }          /* Elemento: parte de la card */
.card__titulo { }
.card__boton { }
.card--destacada { }       /* Modificador: variante */
.card__boton--deshabilitado { }
```

### Reglas de oro
- `Clases, no IDs` :: Para estilos usa clases: especificidad baja y reutilizable
- `Selectores cortos` :: `.menu__link` mejor que `header nav ul li a`
- `Variables para todo lo repetido` :: Colores, espaciados, radios, sombras
- `Mobile first` :: Base para celular, `min-width` para crecer
- `gap antes que margin` :: Para espaciar hijos de flex y grid
- `Unidades relativas` :: rem para texto y espacios
- `Orden en el archivo` :: reset → variables → base → layout → componentes → utilidades
- `Anidado nativo con &` :: CSS moderno ya permite anidar sin Sass (ver abajo)

```css
/* Anidado nativo (soportado en navegadores actuales) */
.card {
  padding: 1rem;
  & h3 { margin-bottom: 0.5rem; }
  &:hover { translate: 0 -4px; }
  @media (min-width: 768px) { padding: 2rem; }
}
```

⚠️ Cuidado: no copies frameworks enteros para un proyecto pequeño; aprender CSS puro primero hace que luego Tailwind o Bootstrap tengan sentido.
🇬🇧 **reset** = reinicio de estilos · **naming convention** = convención de nombres · **block / element / modifier** = bloque / elemento / modificador · **nesting** = anidado · **utility class** = clase utilitaria

## 🏆 Ejemplos resueltos
### ✅ Ejemplo resuelto: card con hover
```html
<article class="card">
  <img class="card__imagen" src="img/curso-ia.webp" alt="Red neuronal ilustrada">
  <div class="card__cuerpo">
    <span class="card__tag">Nuevo</span>
    <h3 class="card__titulo">Deep Learning desde cero</h3>
    <p class="card__texto">Construye tu primera red con PyTorch.</p>
    <a href="/cursos/dl" class="card__boton">Ver curso →</a>
  </div>
</article>
```

```css
.card {
  max-width: 340px;
  border-radius: 1rem;
  overflow: hidden;                       /* la imagen respeta las esquinas */
  background: var(--superficie, white);
  box-shadow: 0 4px 16px rgb(0 0 0 / 8%);
  transition: translate 250ms ease, box-shadow 250ms ease;
}
.card__imagen {
  width: 100%;
  aspect-ratio: 16 / 9;
  object-fit: cover;
  transition: scale 400ms ease;
}
.card__cuerpo { padding: 1.25rem; display: grid; gap: 0.5rem; }
.card__tag {
  justify-self: start;
  padding: 0.15rem 0.6rem;
  border-radius: 999px;
  background: #ede9fe;
  color: #6d28d9;
  font-size: 0.75rem;
  font-weight: 600;
}
.card__boton { color: #7c3aed; font-weight: 600; text-decoration: none; }

.card:hover {
  translate: 0 -6px;
  box-shadow: 0 16px 32px rgb(0 0 0 / 14%);
}
.card:hover .card__imagen { scale: 1.06; }   /* zoom de la imagen dentro */
```

📌 Explicación: `overflow: hidden` en la card recorta la imagen con las esquinas redondeadas y oculta el zoom que se sale. Al hacer hover la card sube 6px y la sombra crece (sensación de elevarse) mientras la imagen hace zoom. `aspect-ratio` + `object-fit` dan imágenes uniformes aunque las fotos originales tengan tamaños distintos. `justify-self: start` hace que la etiqueta no se estire a todo el ancho.

### ✅ Ejemplo resuelto: navbar responsive con menú hamburguesa
```html
<header class="nav">
  <a href="/" class="nav__logo">🤖 IAprende</a>
  <button class="nav__toggle" aria-label="Abrir menú" aria-expanded="false">☰</button>
  <nav class="nav__menu" aria-label="Principal">
    <a href="/cursos">Cursos</a>
    <a href="/blog">Blog</a>
    <a href="/contacto">Contacto</a>
  </nav>
</header>
```

```css
.nav {
  position: sticky;
  top: 0;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.5rem;
  background: var(--fondo, white);
  border-bottom: 1px solid var(--borde, #e4e4e7);
}
.nav__toggle {
  font-size: 1.5rem;
  background: none;
  border: none;
  cursor: pointer;
}
.nav__menu {
  display: none;               /* celular: oculto */
  flex-basis: 100%;            /* ocupa toda una fila bajo el logo */
  flex-direction: column;
  gap: 0.75rem;
  padding-top: 1rem;
}
.nav--abierto .nav__menu { display: flex; }
.nav__menu a { color: inherit; text-decoration: none; font-weight: 500; }
.nav__menu a:hover { color: #7c3aed; }

@media (min-width: 768px) {
  .nav__toggle { display: none; }
  .nav__menu {
    display: flex;
    flex-direction: row;
    flex-basis: auto;
    padding-top: 0;
    gap: 2rem;
  }
}
```

```js
const nav = document.querySelector(".nav");
const toggle = document.querySelector(".nav__toggle");
toggle.addEventListener("click", () => {
  const abierto = nav.classList.toggle("nav--abierto");
  toggle.setAttribute("aria-expanded", abierto);
});
```

📌 Explicación: en el celular el menú está oculto y el botón ☰ visible; al pulsarlo, JS agrega `nav--abierto` y el menú aparece en columna ocupando una fila completa (`flex-basis: 100%` + `flex-wrap`). Desde 768px el botón desaparece y el menú se muestra en fila junto al logo. `aria-expanded` avisa al lector de pantalla si está abierto. `sticky` mantiene la barra arriba al hacer scroll.

### ✅ Ejemplo resuelto: botón animado y modo oscuro
Están resueltos en las secciones 🎞️ Transiciones y animaciones (botón con brillo) y 🎛️ Variables CSS (tema claro/oscuro con botón y `localStorage`). Junta los dos con la card y la navbar: ya tienes una mini página profesional.

💡 Consejo: reconstruye cada ejemplo sin mirar y cambia una cosa a la vez en DevTools para entender qué hace cada línea; así se aprende de verdad.
🇬🇧 **hamburger menu** = menú hamburguesa · **toggle** = alternar · **hover effect** = efecto al pasar el ratón · **component** = componente · **sticky header** = cabecera fija · **zoom** = acercar

