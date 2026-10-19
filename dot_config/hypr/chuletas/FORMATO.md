FORMATO de las chuletas (este archivo no se muestra: empieza con FORMATO)
=========================================================================
Cada hoja es un archivo NN-nombre.md en ~/.config/hypr/chuletas/ (NN = orden de las pestañas).
Validar una hoja (OBLIGATORIO, debe salir con código 0):
  python3 ~/.config/hypr/scripts/chuletas_md.py validar ~/.config/hypr/chuletas/03-css.md
Las imágenes van en ~/.config/hypr/chuletas/img/<tema>/ y se enlazan con ruta relativa.

Elementos (cada uno empieza al inicio de la línea; nada de HTML, enlaces ni `####`):

# 🎨 CSS · Diseño de páginas
    Título de la hoja (una vez, primera línea). Lo que va antes de « · » sale en la pestaña.

> Diseña páginas bonitas: colores, cajas, Flexbox, Grid y animaciones.
    Subtítulo de la hoja (una línea, justo después del título).

## 📦 Modelo de caja
    Sección. Aparece en el índice lateral. Siempre con un emoji al inicio.

### ✅ Ejemplo resuelto: tarjeta centrada
    Subtítulo dentro de una sección.

Texto normal: renglones seguidos forman un párrafo; una línea en blanco los separa.
Se puede usar `código en línea` y **negrita**.

- Viñeta normal (lista). Puede llevar `código` y **negrita**.
- Otra viñeta. Si sigue en la línea siguiente con 2 espacios de sangría, continúa la misma viñeta.
1. Lista numerada (pasos)
2. Segundo paso

- `display: flex;` :: Activa Flexbox en el contenedor
    Entrada rápida: guion, código entre comillas invertidas, " :: ", explicación corta.
    Varias seguidas se dibujan como UNA tabla código | explicación; clic en la fila = copiar.

```css
.tarjeta { display: grid; place-items: center; }
```
    Bloque de código (botón Copiar). Lenguajes con color: python, js, jsx, ts, html, css, bash, sql,
    dockerfile, yaml, json, c, cpp, java, go, text.

Cajas de una línea (empiezan con el emoji):
💡 Consejo: ...      ⚠️ Cuidado: ... (error típico)      🇬🇧 inglés (vocabulario, frases)
📌 Resumen/nota      ✅ Bien: ... (lo correcto)           ❌ Mal: ... (lo que NO hacer)
🧠 Concepto: definición importante                       🚀 Futuro: tendencia / hacia dónde va

| Opción | Cuándo usarla | Ventaja | Desventaja |
|---|---|---|---|
| `grid` | 2 dimensiones | Potente | Más que aprender |
    Tabla. Primera fila = encabezado. Mismo número de columnas en todas (2–5). Celdas cortas.
    Úsalas para comparar (X vs Y), «cuándo usar qué», error → causa → solución, resúmenes.
    Un | dentro de una celda solo puede ir dentro de `código`.

![Pie de foto que explica la imagen](img/css/modelo-caja.png)
    Imagen (png/jpg/webp/svg), centrada sobre fondo claro, con el pie debajo.

::: desplegable 🧩 Ver la solución
...cualquier bloque (código, listas, tablas...)...
:::
    Desplegable: se abre con un clic. Ideal para soluciones de ejercicios, detalles avanzados,
    «¿por qué pasa esto?», código largo. Dentro NO puede haber `##`.

::: columnas
### ✅ SQL
- Relaciones, transacciones
::: siguiente
### 🍃 NoSQL
- Esquema flexible
:::
    Columnas lado a lado (2 o 3) en pantalla completa; en el panel lateral se apilan.
    Ideal para comparar dos opciones, antes/después, mal/bien.

ESQUEMAS Y GRÁFICAS (se dibujan solos con los colores del tema; bloques ``` con el tipo):

```flujo
dir: abajo
Código -> Commit -> Push -> CI
CI -> Tests : corre
Tests -> Deploy : ✅ pasan
Tests --> Código : ❌ fallan
```
    Diagrama de flujo / proceso / pipeline / arquitectura. «A -> B : etiqueta».
    -> flecha, --> flecha punteada, <-> doble. Varias en cadena: A -> B -> C.
    dir: derecha (por defecto) o abajo (mejor si hay más de 4 niveles). Nombres de nodo cortos.
    Para pedidos/respuestas entre sistemas usa secuencia (queda más claro).

```secuencia
Navegador -> Servidor : GET /api/users
Servidor -> BD : SELECT * FROM users
BD --> Servidor : filas
nota Servidor : arma el JSON
Servidor --> Navegador : 200 OK + JSON
```
    Diagrama de secuencia (quién habla con quién y en qué orden). --> = respuesta.
    «nota Actor : texto» añade una nota. «actores: A, B, C» fija el orden (opcional).

```arbol
html
  head
    title
  body
    main
```
    Árbol por sangría (2 espacios = un nivel): DOM, carpetas, herencia, árboles de datos (BST).

```capas
Presentación : React — lo que ve el usuario
Lógica : API en Node — reglas del negocio
Datos : PostgreSQL — guarda la información
```
    Capas apiladas: arquitecturas, modelo OSI/TCP-IP, stack, niveles de abstracción.

```tiempo
1995 : Nace JavaScript
2015 : ES6
2026 : hoy
```
    Línea de tiempo: historia y futuro de una tecnología.

```grafica
tipo: barras
titulo: Velocidad relativa
unidad: ms
Python : 120
Go : 15
```
```grafica
tipo: lineas
titulo: Crecimiento de cada complejidad
x: 1..20
ymax: 100
ejex: n (datos)
O(n): n
O(n log n): n*log2(n)
O(n²): n^2
Medido: 1, 3, 9, 20, 41
```
```grafica
tipo: pastel
titulo: ¿En qué se va el tiempo?
Leer código : 50
Escribir : 30
```
    barras / pastel: «Etiqueta : número». lineas: «Nombre : fórmula en n» (log, log2, sqrt,
    exp, factorial, ^) o lista de números. Si son datos de encuestas/benchmarks, di la fuente y
    el año; si son ilustrativos, dilo. No inventes cifras presentadas como reales.
