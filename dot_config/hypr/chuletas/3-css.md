# 🎨 CSS
Cada línea: código :: explicación. Edita este archivo para añadir las tuyas.

## Selectores
.tarjeta { } #menu { } p { } :: Por clase, por id, por etiqueta
.menu a { } .menu > a { } :: Descendiente (cualquier nivel) / hijo directo
a:hover { } input:focus { } :: Al pasar el ratón / al tener foco
li:nth-child(2n) { } li:first-child { } :: Pares / el primero
.btn::before { content: "★"; } :: Pseudo-elemento: contenido extra
[type="email"] { } :: Por atributo

## Modelo de caja
* { box-sizing: border-box; } :: El ancho incluye padding y borde (ponlo siempre)
margin: 10px 20px; :: Espacio fuera (arriba/abajo 10, lados 20)
padding: 1rem; :: Espacio dentro
border: 2px solid #333; border-radius: 12px; :: Borde y esquinas redondeadas
width: min(90%, 800px); :: Ancho adaptable con tope
margin-inline: auto; :: Centrar un bloque horizontalmente

## Flexbox (una dimensión)
display: flex; :: Activa flexbox en el contenedor
justify-content: center; :: Alinear en el eje principal (space-between, space-around…)
align-items: center; :: Alinear en el eje cruzado
flex-direction: column; :: En columna en vez de fila
gap: 1rem; :: Espacio entre elementos
flex: 1; :: Este hijo ocupa el espacio que sobre
flex-wrap: wrap; :: Pasar a otra línea si no cabe

## Grid (dos dimensiones)
display: grid; :: Activa grid
grid-template-columns: repeat(3, 1fr); :: 3 columnas iguales
grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); :: Columnas que se adaptan solas
grid-column: span 2; :: Ocupar 2 columnas
place-items: center; :: Centrar todo en ambos ejes

## Texto y color
font: 600 1.1rem/1.6 "Inter", sans-serif; :: Peso, tamaño/alto de línea y fuente
color: #222; background: #fafafa; :: Color de texto y fondo
text-align: center; text-transform: uppercase; :: Alinear / mayúsculas
color: rgb(0 0 0 / 60%); :: Color con transparencia
background: linear-gradient(135deg, #ff6fa8, #7ec8ff); :: Degradado

## Posición
position: relative; :: Referencia para hijos absolute
position: absolute; top: 0; right: 0; :: Pegado a una esquina del padre
position: sticky; top: 0; :: Se queda pegado al hacer scroll
position: fixed; bottom: 1rem; :: Fijo en la pantalla
z-index: 10; :: Qué queda encima

## Responsive y variables
@media (max-width: 600px) { } :: Estilos solo en pantallas pequeñas
:root { --acento: #8b5cf6; } :: Definir una variable
color: var(--acento); :: Usar la variable
img { max-width: 100%; height: auto; } :: Imágenes que no se desbordan
clamp(1rem, 2.5vw, 2rem) :: Tamaño fluido entre un mínimo y un máximo

## Animaciones
transition: all 200ms ease; :: Transición suave al cambiar propiedades
transform: translateY(-4px) scale(1.05); :: Mover / escalar
@keyframes latir { to { transform: scale(1.1); } } :: Definir animación
animation: latir 1s infinite alternate; :: Usarla
box-shadow: 0 10px 30px rgb(0 0 0 / 20%); :: Sombra
