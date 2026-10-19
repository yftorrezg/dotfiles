FORMATO de las chuletas (este archivo no se muestra: empieza con FORMATO)
=========================================================================
Cada hoja es un archivo NN-nombre.md en ~/.config/hypr/chuletas/ (NN = orden de las pestañas).
Validar una hoja:  python3 ~/.config/hypr/scripts/chuletas_md.py validar ~/.config/hypr/chuletas/03-css.md

Elementos (cada uno empieza al inicio de la línea):

# 🎨 CSS
    Título de la hoja (una sola vez, primera línea). Emoji + nombre corto (sale en la pestaña).

> Diseña páginas bonitas: colores, cajas, Flexbox, Grid y animaciones.
    Subtítulo de la hoja (una línea, justo después del título).

## 📦 Modelo de caja
    Sección. Aparece en el índice lateral. Siempre con un emoji al inicio.

### ✅ Ejemplo resuelto: tarjeta centrada
    Subtítulo dentro de una sección (subtemas y ejemplos resueltos).

Texto normal: uno o varios renglones seguidos forman un párrafo; una línea en blanco separa párrafos.
Se puede usar `código en línea` y **negrita**. No uses HTML ni enlaces.

- `display: flex;` :: Activa Flexbox en el contenedor
    Entrada rápida: guion, código entre comillas invertidas, " :: ", explicación corta.
    Al hacer clic se copia el código. Ideal para listas de comandos/propiedades.
    Varias entradas seguidas se dibujan como UNA tabla de dos columnas (código | explicación).

```css
.tarjeta {
  display: grid;
  place-items: center;
}
```
    Bloque de código de varias líneas (se puede copiar). Lenguajes que se colorean:
    python, js, jsx, ts, html, css, bash, sql, dockerfile, yaml, json, text.

💡 Consejo: ...      caja de consejo
⚠️ Cuidado: ...      caja de advertencia (errores típicos)
🇬🇧 ...              caja de inglés (vocabulario, frases, pronunciación)
📌 ...               caja de nota / resumen
    Una caja = una línea (puede ser larga; se ajusta sola).

| English | Suena | Español | Ejemplo |
|---|---|---|---|
| queue | kiú | cola | `queue.push(job)` |
    Tabla. Primera fila = encabezado. La fila de guiones es opcional. Mismo número de columnas en todas.
    En las celdas se puede usar `código` y **negrita**. Las columnas se ajustan solas al texto;
    mejor 2–5 columnas y celdas cortas (una idea por celda). Úsalas mucho: comparaciones
    (X vs Y), «cuándo usar qué», errores → causa → solución, vocabulario, resúmenes.
