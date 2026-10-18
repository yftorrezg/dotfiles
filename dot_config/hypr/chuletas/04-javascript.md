# 🟨 JavaScript
> El lenguaje de la web: de variables y arrays a promesas, fetch y el DOM, con ejemplos resueltos y vocabulario en inglés.

## 📦 Variables y tipos

Una **variable** es una caja con nombre donde guardas un valor. En JavaScript moderno se usan `const` (no se puede reasignar) y `let` (sí se puede). `var` es la forma vieja: tiene reglas raras de alcance, así que evítala.

JavaScript es de **tipado dinámico**: la variable no tiene tipo, el valor sí. Hay 7 tipos primitivos (`string`, `number`, `bigint`, `boolean`, `undefined`, `null`, `symbol`) y todo lo demás es `object` (arrays, funciones, fechas…).

- `const PI = 3.1416;` :: Constante: no se puede reasignar (úsala por defecto)
- `let edad = 20; edad = 21;` :: Variable que sí cambia de valor
- `typeof "hola"` :: Devuelve el tipo como texto → "string"
- `Array.isArray([1, 2])` :: ¿Es un array? (typeof dice "object", no sirve)
- `Number("42")` :: Texto → número (42); si no se puede, da NaN
- `parseInt("8px", 10)` :: Lee el número del inicio del texto → 8
- `parseFloat("3.5kg")` :: Igual pero con decimales → 3.5
- `String(10)` :: Número → texto "10"
- `Boolean("")` :: A booleano: "", 0, null, undefined, NaN son false
- `Number.isNaN(x)` :: ¿Es NaN? (NaN no es igual ni a sí mismo)
- `let x;` :: Declarada sin valor → vale undefined
- `let y = null;` :: "Vacío a propósito": lo pones tú

```js
const nombre = "Ana";       // string
const edad = 20;            // number (enteros y decimales son lo mismo)
const activo = true;        // boolean
let apodo;                  // undefined: aún no tiene valor
const mascota = null;       // null: sin valor, a propósito
const grande = 9007199254740993n; // bigint: enteros enormes

console.log(typeof nombre, typeof edad, typeof activo); // → string number boolean
console.log(typeof apodo, typeof mascota);               // → undefined object (¡bug histórico!)
console.log(0.1 + 0.2);                                  // → 0.30000000000000004
console.log((0.1 + 0.2).toFixed(2));                     // → "0.30"
```

📌 Valores "falsy" (cuentan como falso en un if): `false`, `0`, `""`, `null`, `undefined`, `NaN`. Todo lo demás es "truthy", incluso `"0"`, `[]` y `{}`.
⚠️ Cuidado: `const` impide reasignar, no modificar. `const lista = []; lista.push(1);` funciona; `lista = [2]` da error.
⚠️ Cuidado: `typeof null` devuelve "object" por un error antiguo del lenguaje; para saber si algo es null compara `x === null`.
💡 Consejo: usa `const` siempre y cambia a `let` solo cuando de verdad necesites reasignar. Tu código será más fácil de razonar.
🇬🇧 **variable** /vérieibol/ = variable · **value** /váliu/ = valor · **type** /taip/ = tipo · **string** /string/ = texto · **boolean** /búlian/ = verdadero/falso · **undefined** /andifáind/ = no definido · **assign** /asáin/ = asignar

## ➕ Operadores

Los operadores combinan valores. Lo más importante: usa **siempre `===`** (igualdad estricta) y no `==`, porque `==` convierte tipos de forma sorprendente. Los operadores modernos `??` y `?.` te ahorran muchos `if`.

- `a === b` :: Igual en valor Y tipo (usa este)
- `a !== b` :: Distinto en valor o tipo
- `a == b` :: Igual convirtiendo tipos: "5" == 5 es true (evítalo)
- `&& || !` :: Y, O, NO lógicos
- `x ?? "def"` :: Usa "def" solo si x es null o undefined
- `x || "def"` :: Usa "def" si x es CUALQUIER falsy (0, "" incluidos)
- `user?.direccion?.ciudad` :: Encadenamiento opcional: undefined en vez de error
- `obj.metodo?.()` :: Llama al método solo si existe
- `x ??= 10` :: Asigna 10 solo si x es null/undefined
- `n += 1; n++` :: Sumar 1 (también -=, *=, /=)
- `2 ** 10` :: Potencia → 1024
- `7 % 3` :: Resto de la división → 1 (sirve para par/impar)
- `cond ? siEs : siNo` :: Ternario: if corto que devuelve valor

```js
console.log(5 == "5");    // → true  (convierte el texto a número)
console.log(5 === "5");   // → false (tipos distintos)
console.log(null == undefined, null === undefined); // → true false

const cantidad = 0;
console.log(cantidad || 10);  // → 10  (0 es falsy, ¡se pierde!)
console.log(cantidad ?? 10);  // → 0   (0 no es null/undefined, se respeta)

const usuario = { nombre: "Luis" };
console.log(usuario.direccion?.ciudad);        // → undefined (sin error)
console.log(usuario.direccion?.ciudad ?? "Sin ciudad"); // → Sin ciudad
```

⚠️ Cuidado: `usuario.direccion.ciudad` sin `?.` lanza "TypeError: Cannot read properties of undefined". Es el error más común de JS.
💡 Consejo: para valores por defecto de números o textos que pueden ser 0 o "" usa `??`, no `||`.
🇬🇧 **operator** /óperéitor/ = operador · **strict equality** /strikt ikuóliti/ = igualdad estricta · **nullish** /nálish/ = nulo o indefinido · **optional chaining** /ópshonal chéining/ = encadenamiento opcional

## 🔤 Strings y template literals

Los textos se escriben entre comillas `"..."`, `'...'` o comillas invertidas. Las invertidas crean **template literals**: permiten meter variables con `${...}` y escribir varias líneas. Los strings son **inmutables**: los métodos devuelven un texto nuevo, no cambian el original.

- ``Hola ${nombre}`` :: Template literal: inserta el valor de nombre
- `s.length` :: Cantidad de caracteres
- `s.toUpperCase() / s.toLowerCase()` :: Mayúsculas / minúsculas
- `s.trim()` :: Quita espacios al inicio y al final
- `s.includes("ana")` :: ¿Contiene el texto? → true/false
- `s.startsWith("http")` :: ¿Empieza con...? (también endsWith)
- `s.indexOf("a")` :: Posición de la primera aparición (-1 si no está)
- `s.slice(0, 3)` :: Recorta desde 0 hasta antes de 3
- `s.split(",")` :: Parte el texto en un array
- `arr.join(" - ")` :: Une un array en un texto
- `s.replace("a", "o")` :: Reemplaza la primera aparición
- `s.replaceAll("a", "o")` :: Reemplaza todas
- `s.padStart(3, "0")` :: Rellena a la izquierda: "7" → "007"
- `s.repeat(3)` :: Repite el texto
- `s.at(-1)` :: Último carácter

```js
const nombre = "  Ana Quispe  ";
const limpio = nombre.trim();                 // "Ana Quispe"
const [pila, apellido] = limpio.split(" ");   // ["Ana", "Quispe"]

console.log(`Hola ${pila}, tienes ${limpio.length} letras`); // → Hola Ana, tienes 10 letras
console.log(apellido.toUpperCase());          // → QUISPE
console.log("7".padStart(3, "0"));            // → 007
console.log("la-paz-bolivia".split("-").join(" ")); // → la paz bolivia

const mensaje = `Línea 1
Línea 2`;                                     // varias líneas sin \n
console.log(mensaje.split("\n").length);      // → 2
```

### ✅ Ejemplo resuelto: crear un "slug" para una URL

```js
function slug(texto) {
  return texto
    .trim()                              // 1. quita espacios de los bordes
    .toLowerCase()                       // 2. todo en minúsculas
    .normalize("NFD")                    // 3. separa letras de tildes (á → a + ´)
    .replace(/[̀-ͯ]/g, "")     // 4. borra las tildes sueltas
    .replace(/[^a-z0-9]+/g, "-")         // 5. lo que no sea letra/número → guion
    .replace(/^-|-$/g, "");              // 6. quita guiones del inicio/final
}
console.log(slug("  ¡Cómo aprender JavaScript en 2026!  "));
// → como-aprender-javascript-en-2026
```

💡 Consejo: encadenar métodos (`.trim().toLowerCase()...`) funciona porque cada uno devuelve un string nuevo.
⚠️ Cuidado: `"5" + 3` da `"53"` (concatena), pero `"5" - 3` da `2`. Convierte con `Number()` antes de sumar entradas de formularios.
🇬🇧 **template literal** /témpleit líteral/ = plantilla de texto · **backtick** /bákik/ = comilla invertida · **trim** /trim/ = recortar · **split** /split/ = partir · **join** /yoin/ = unir · **replace** /ripléis/ = reemplazar

## 🔀 Condicionales

Las condiciones deciden qué código se ejecuta. `if/else` es lo general; el **ternario** sirve para elegir un valor en una línea; `switch` para comparar una variable con muchos casos. Un truco muy usado es el **retorno temprano** (early return): salir de la función apenas algo no cumple, para no anidar `if` dentro de `if`.

- `if (x > 0) { } else if (x === 0) { } else { }` :: Condicional completo
- `const tipo = n % 2 === 0 ? "par" : "impar";` :: Ternario
- `switch (dia) { case 1: ...; break; default: ... }` :: Varios casos exactos
- `if (!usuario) return;` :: Retorno temprano: sale si no hay usuario
- `activo && mostrar()` :: Ejecuta mostrar() solo si activo es truthy

```js
function notaALetra(nota) {
  if (typeof nota !== "number") return "Nota inválida"; // retorno temprano
  if (nota >= 90) return "A";
  if (nota >= 70) return "B";
  if (nota >= 51) return "C (aprobado)";
  return "Reprobado";
}
console.log(notaALetra(95), notaALetra(60), notaALetra(30)); // → A C (aprobado) Reprobado

function nombreDia(n) {
  switch (n) {
    case 6:
    case 7:
      return "Fin de semana";  // dos casos comparten el mismo código
    case 1:
      return "Lunes";
    default:
      return "Entre semana";
  }
}
console.log(nombreDia(7)); // → Fin de semana
```

💡 Consejo: en vez de un switch enorme, muchas veces un objeto sirve de "tabla": `const precios = { cafe: 8, te: 5 }; precios[pedido] ?? 0`.
⚠️ Cuidado: en `switch` si olvidas `break` (o `return`) el código "cae" al siguiente caso.
🇬🇧 **condition** /kondíshon/ = condición · **statement** /stéitment/ = sentencia · **early return** /érli ritérn/ = retorno temprano · **fall through** /fol zru/ = caer al siguiente caso

## 🔁 Bucles

Un bucle repite código. Para arrays lo más claro es `for...of` (recorre **valores**). `for...in` recorre **claves** de un objeto. El `for` clásico con índice sirve cuando necesitas el número de vuelta. `while` repite mientras una condición sea verdadera. En código moderno muchos bucles se reemplazan por `map`, `filter` y `reduce` (ver Arrays).

- `for (let i = 0; i < 5; i++) { }` :: Bucle clásico con contador
- `for (const v of lista) { }` :: Recorre los valores de un array/string/Map/Set
- `for (const [i, v] of lista.entries()) { }` :: Valores con su índice
- `for (const k in objeto) { }` :: Recorre las claves de un objeto
- `while (cond) { }` :: Repite mientras cond sea true
- `do { } while (cond);` :: Igual pero se ejecuta al menos una vez
- `break; continue;` :: Salir del bucle / saltar a la siguiente vuelta
- `lista.forEach((v, i) => { })` :: Método de array para recorrer (no permite break)

```js
const frutas = ["mango", "papaya", "chirimoya"];

for (const f of frutas) console.log(f);          // → mango / papaya / chirimoya

for (const [i, f] of frutas.entries()) {
  console.log(`${i + 1}. ${f}`);                 // → 1. mango  2. papaya  3. chirimoya
}

const edades = { ana: 20, luis: 25 };
for (const nombre in edades) {
  console.log(nombre, edades[nombre]);           // → ana 20 / luis 25
}

let n = 1;
while (n < 100) n *= 2;
console.log(n);                                  // → 128
```

### ✅ Ejemplo resuelto: FizzBuzz (el clásico de entrevistas)

```js
const salida = [];
for (let i = 1; i <= 15; i++) {
  if (i % 15 === 0) salida.push("FizzBuzz");   // divisible por 3 y por 5
  else if (i % 3 === 0) salida.push("Fizz");
  else if (i % 5 === 0) salida.push("Buzz");
  else salida.push(i);
}
console.log(salida.join(" "));
// → 1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz 11 Fizz 13 14 FizzBuzz
```

⚠️ Cuidado: no uses `for...in` con arrays: recorre índices como texto ("0", "1"…) y también propiedades heredadas. Usa `for...of`.
⚠️ Cuidado: un `while` cuya condición nunca se vuelve falsa congela la pestaña (bucle infinito).
🇬🇧 **loop** /lup/ = bucle · **iterate** /íteréit/ = recorrer · **index** /índex/ = índice · **break** /bréik/ = romper/salir · **iteration** /iteréishon/ = vuelta del bucle

## 🧩 Funciones

Una función es un bloque de código reutilizable: recibe **parámetros**, hace algo y **devuelve** (return) un resultado. En JS las funciones son valores: se pueden guardar en variables, pasar a otras funciones (callbacks) y devolver desde funciones.

Un **closure** (clausura) es cuando una función "recuerda" las variables del lugar donde fue creada, aunque ese lugar ya haya terminado. Es la base de contadores privados, fábricas de funciones y muchos patrones de React.

- `function sumar(a, b) { return a + b; }` :: Declaración clásica (se puede usar antes de definirla: hoisting)
- `const sumar = (a, b) => a + b;` :: Función flecha con return implícito
- `const cuadrado = x => x * x;` :: Un solo parámetro: sin paréntesis
- `const crear = () => ({ id: 1 });` :: Flecha que devuelve un objeto: envuélvelo en ()
- `function saludo(nombre = "amigo") { }` :: Parámetro con valor por defecto
- `function total(...nums) { }` :: Parámetros rest: recibe todos en un array
- `max(...lista)` :: Spread: expande el array como argumentos
- `function f({ nombre, edad }) { }` :: Desestructurar el objeto recibido
- `lista.map(x => x * 2)` :: Pasar una función como argumento (callback)

```js
function saludar(nombre = "amigo", saludo = "Hola") {
  return `${saludo}, ${nombre}!`;
}
console.log(saludar());               // → Hola, amigo!
console.log(saludar("Ana", "Buenas")); // → Buenas, Ana!

const promedio = (...nums) => nums.reduce((a, b) => a + b, 0) / nums.length;
console.log(promedio(7, 8, 9));        // → 8

const notas = [51, 90, 77];
console.log(Math.max(...notas));       // → 90

function mostrarPerfil({ nombre, ciudad = "La Paz" }) {
  return `${nombre} vive en ${ciudad}`;
}
console.log(mostrarPerfil({ nombre: "Luis" })); // → Luis vive en La Paz
```

### ✅ Ejemplo resuelto: closure para un contador privado

```js
function crearContador(inicio = 0) {
  let cuenta = inicio;               // variable "privada": nadie de fuera la ve
  return {
    sumar: () => ++cuenta,           // estas funciones RECUERDAN a `cuenta`
    restar: () => --cuenta,
    valor: () => cuenta,
  };
}
const c = crearContador(10);
c.sumar(); c.sumar(); c.restar();
console.log(c.valor());              // → 11
console.log(c.cuenta);               // → undefined (no se puede tocar directo)
```

Qué pasa: `crearContador` termina, pero las tres flechas siguen teniendo acceso a `cuenta`. Cada llamada a `crearContador` crea un contador independiente.

### ✅ Ejemplo resuelto: funciones que crean funciones

```js
const multiplicarPor = factor => numero => numero * factor;
const doble = multiplicarPor(2);
const triple = multiplicarPor(3);
console.log(doble(5), triple(5));    // → 10 15
```

💡 Consejo: una función = una tarea. Si su nombre necesita "y" (validarYGuardar), probablemente son dos funciones.
⚠️ Cuidado: una flecha con llaves `{ }` necesita `return` explícito: `x => { x * 2 }` devuelve undefined.
⚠️ Cuidado: las flechas no tienen su propio `this`; no las uses como métodos de objeto que usan `this`.
🇬🇧 **function** /fánkshon/ = función · **parameter** /parámeter/ = parámetro · **argument** /árguiument/ = argumento (valor que pasas) · **return** /ritérn/ = devolver · **arrow function** /árou fánkshon/ = función flecha · **closure** /klóushur/ = clausura · **callback** /kólbak/ = función que se llama después · **scope** /skóup/ = alcance

## 📚 Arrays

Un array es una lista ordenada de valores (índices desde 0). Sus métodos son lo que más usarás en JS: transformar datos que llegan de una API, filtrar resultados de búsqueda, sumar totales… Distingue los métodos que **crean un array nuevo** (map, filter, slice, toSorted) de los que **modifican el original** (push, pop, splice, sort, reverse).

- `const xs = [3, 1, 2];` :: Crear un array
- `xs.length` :: Cantidad de elementos
- `xs[0]; xs.at(-1)` :: Primer elemento / último elemento
- `xs.push(4); xs.pop();` :: Añadir al final / sacar del final (modifica)
- `xs.unshift(0); xs.shift();` :: Añadir al inicio / sacar del inicio (modifica)
- `xs.splice(1, 1)` :: Borra 1 elemento en la posición 1 (modifica)
- `xs.slice(1, 3)` :: Copia del índice 1 al 2 (no modifica)
- `[...xs, 5]` :: Copia añadiendo al final (no modifica)
- `xs.indexOf(2)` :: Posición del valor (-1 si no está)
- `Array.from({ length: 3 }, (_, i) => i)` :: Crea [0, 1, 2]

### 📋 Tabla de métodos importantes

| Método | Qué hace | Devuelve | ¿Modifica? |
|---|---|---|---|
| `map(fn)` | transforma cada elemento | array nuevo, mismo largo | no |
| `filter(fn)` | se queda con los que cumplen | array nuevo, más corto | no |
| `reduce(fn, ini)` | acumula todo en un valor | un valor (número, objeto…) | no |
| `find(fn)` | primer elemento que cumple | elemento o undefined | no |
| `findIndex(fn)` | posición del primero que cumple | número o -1 | no |
| `some(fn)` | ¿al menos uno cumple? | true/false | no |
| `every(fn)` | ¿todos cumplen? | true/false | no |
| `includes(v)` | ¿contiene ese valor? | true/false | no |
| `sort(fn)` | ordena | el mismo array | **sí** |
| `toSorted(fn)` | ordena una copia | array nuevo | no |
| `reverse()` | invierte | el mismo array | **sí** |
| `flat(n)` | aplana arrays anidados | array nuevo | no |
| `flatMap(fn)` | map y luego flat(1) | array nuevo | no |
| `forEach(fn)` | recorre (sin devolver) | undefined | no |
| `join(sep)` | une en texto | string | no |
| `concat(b)` | une dos arrays | array nuevo | no |

```js
const productos = [
  { nombre: "salteña", precio: 8, categoria: "comida" },
  { nombre: "api morado", precio: 6, categoria: "bebida" },
  { nombre: "sándwich de chola", precio: 15, categoria: "comida" },
  { nombre: "mocochinchi", precio: 5, categoria: "bebida" },
];

const nombres = productos.map(p => p.nombre);
console.log(nombres);    // → [ 'salteña', 'api morado', 'sándwich de chola', 'mocochinchi' ]

const bebidas = productos.filter(p => p.categoria === "bebida");
console.log(bebidas.length);                      // → 2

const total = productos.reduce((suma, p) => suma + p.precio, 0);
console.log(total);                               // → 34

console.log(productos.find(p => p.precio > 10)?.nombre); // → sándwich de chola
console.log(productos.some(p => p.precio > 20));  // → false
console.log(productos.every(p => p.precio > 0));  // → true

const baratos = productos.toSorted((a, b) => a.precio - b.precio).map(p => p.nombre);
console.log(baratos[0]);                          // → mocochinchi

console.log([1, [2, [3, [4]]]].flat(Infinity));   // → [ 1, 2, 3, 4 ]
console.log(["hola mundo", "chau"].flatMap(f => f.split(" "))); // → [ 'hola', 'mundo', 'chau' ]
```

### ✅ Ejemplo resuelto: agrupar y contar con reduce

```js
const ventas = ["salteña", "api", "salteña", "tucumana", "api", "salteña"];

const conteo = ventas.reduce((acc, item) => {
  acc[item] = (acc[item] ?? 0) + 1;   // si no existe, empieza en 0 y suma 1
  return acc;                          // ¡siempre devuelve el acumulador!
}, {});                                // valor inicial: objeto vacío

console.log(conteo);                   // → { 'salteña': 3, api: 2, tucumana: 1 }

const masVendido = Object.entries(conteo).toSorted((a, b) => b[1] - a[1])[0];
console.log(masVendido);               // → [ 'salteña', 3 ]

// Moderno: Object.groupBy agrupa en listas
const porCategoria = Object.groupBy(
  [{ n: "api", c: "bebida" }, { n: "salteña", c: "comida" }, { n: "té", c: "bebida" }],
  x => x.c
);
console.log(Object.keys(porCategoria)); // → [ 'bebida', 'comida' ]
```

⚠️ Cuidado: `[10, 1, 5].sort()` da `[1, 10, 5]` porque ordena como TEXTO. Para números usa `sort((a, b) => a - b)`.
⚠️ Cuidado: `sort` y `reverse` modifican el array original. En React o con datos compartidos usa `toSorted` / `toReversed` o `[...xs].sort()`.
💡 Consejo: encadena `filter → map → reduce` para procesar datos en pasos legibles, como una tubería.
💡 Consejo: si tu `map` no usa el valor devuelto, en realidad querías `forEach` (o `for...of`).
🇬🇧 **array** /arréi/ = arreglo/lista · **element** /élement/ = elemento · **filter** /fílter/ = filtrar · **reduce** /ridiús/ = reducir · **find** /fáind/ = encontrar · **sort** /sort/ = ordenar · **flatten** /flátn/ = aplanar · **accumulator** /akiúmiuleitor/ = acumulador

## 🗂️ Objetos

Un objeto agrupa datos relacionados en pares **clave: valor**. Es la estructura más usada para representar "cosas": un usuario, un producto, la respuesta de una API. La **desestructuración** saca propiedades a variables y el **spread** `...` copia o combina objetos sin modificar el original (muy importante en React).

- `const p = { nombre: "Ana", edad: 20 };` :: Objeto literal
- `p.nombre; p["nombre"]` :: Leer (la forma con [] sirve con claves variables)
- `p.ciudad = "Sucre";` :: Añadir o cambiar una propiedad
- `delete p.edad;` :: Borrar una propiedad
- `"nombre" in p` :: ¿Existe la clave?
- `const { nombre, edad } = p;` :: Desestructurar
- `const { nombre: n } = p;` :: Desestructurar con otro nombre
- `const { ciudad = "La Paz" } = p;` :: Con valor por defecto
- `const { nombre, ...resto } = p;` :: Saca nombre; lo demás queda en resto
- `const copia = { ...p, edad: 21 };` :: Copia y cambia una propiedad
- `{ nombre, edad }` :: Atajo: igual a { nombre: nombre, edad: edad }
- `{ [clave]: valor }` :: Clave calculada desde una variable
- `Object.keys(p)` :: Array de claves
- `Object.values(p)` :: Array de valores
- `Object.entries(p)` :: Array de pares [clave, valor]
- `Object.fromEntries(pares)` :: Pares → objeto (lo inverso)
- `Object.assign(dest, a, b)` :: Copia propiedades de a y b a dest (modifica dest)
- `Object.freeze(p)` :: Congela: ya no se puede modificar

```js
const estudiante = {
  nombre: "Ana",
  carrera: "Ciencias de la Computación",
  notas: { calculo: 78, programacion: 95 },
  saludar() {                               // método (función dentro del objeto)
    return `Soy ${this.nombre}`;
  },
};

const { nombre, notas: { programacion } } = estudiante; // desestructuración anidada
console.log(nombre, programacion);          // → Ana 95
console.log(estudiante.saludar());          // → Soy Ana

const actualizado = { ...estudiante, semestre: 5 };   // copia + campo nuevo
console.log("semestre" in estudiante, actualizado.semestre); // → false 5

// Transformar un objeto: subir 5 puntos a cada nota
const subidas = Object.fromEntries(
  Object.entries(estudiante.notas).map(([materia, n]) => [materia, n + 5])
);
console.log(subidas);                       // → { calculo: 83, programacion: 100 }
```

⚠️ Cuidado: el spread `{ ...obj }` hace una copia **superficial**: los objetos de dentro (como `notas`) siguen compartidos. Para copia profunda usa `structuredClone(obj)`.
⚠️ Cuidado: comparar objetos con `===` compara si son el MISMO objeto en memoria, no si tienen el mismo contenido: `{a:1} === {a:1}` es false.
💡 Consejo: usa `Object.entries` + `map` + `Object.fromEntries` para transformar objetos igual que transformas arrays.
🇬🇧 **object** /óbyekt/ = objeto · **key** /ki/ = clave · **property** /próperti/ = propiedad · **destructuring** /distráktiuring/ = desestructuración · **spread** /spred/ = esparcir/expandir · **shallow copy** /shálou kópi/ = copia superficial · **deep copy** /dip kópi/ = copia profunda

## 🏛️ Clases y this

Una **clase** es un molde para crear objetos con los mismos datos y métodos. `constructor` se ejecuta al hacer `new`. `this` es "el objeto actual". Con `extends` una clase hereda de otra y con `super` llamas al padre. Los campos con `#` son **privados**: solo se usan dentro de la clase.

Regla simple de `this`: vale el objeto **antes del punto** al llamar (`perro.ladrar()` → this es perro). Si sacas el método y lo llamas suelto, `this` se pierde. Las funciones flecha no tienen this propio: usan el del lugar donde se escribieron.

- `class Perro { constructor(n) { this.nombre = n; } }` :: Definir una clase
- `const p = new Perro("Firulais");` :: Crear una instancia
- `ladrar() { return "guau"; }` :: Método dentro de la clase
- `class Cachorro extends Perro { }` :: Herencia
- `super(n)` :: Llamar al constructor del padre (antes de usar this)
- `#saldo = 0;` :: Campo privado
- `static crear() { }` :: Método de la clase, no de cada instancia
- `get total() { }` :: Getter: se lee como propiedad (obj.total)
- `p instanceof Perro` :: ¿Fue creado con esa clase?

```js
class CuentaBancaria {
  #saldo = 0;                         // privado: nadie de fuera lo cambia
  static banco = "Banco Unión";       // propiedad de la clase

  constructor(titular) {
    this.titular = titular;
  }
  depositar(monto) {
    if (monto <= 0) throw new Error("Monto inválido");
    this.#saldo += monto;
    return this;                      // devolver this permite encadenar
  }
  get saldo() {                       // getter: se usa sin ()
    return `Bs ${this.#saldo.toFixed(2)}`;
  }
}

class CuentaAhorro extends CuentaBancaria {
  constructor(titular, interes) {
    super(titular);                   // primero el padre
    this.interes = interes;
  }
  describir() {
    return `${this.titular} gana ${this.interes}% en ${CuentaBancaria.banco}`;
  }
}

const cuenta = new CuentaAhorro("Ana", 3);
cuenta.depositar(100).depositar(50.5);
console.log(cuenta.saldo);           // → Bs 150.50
console.log(cuenta.describir());     // → Ana gana 3% en Banco Unión
console.log(cuenta instanceof CuentaBancaria); // → true
```

### ✅ Ejemplo resuelto: perder this (y arreglarlo)

```js
const boton = {
  texto: "Enviar",
  normal() { return this?.texto; },
  flecha: () => typeof this,          // la flecha no tiene this propio
};
const suelta = boton.normal;
console.log(boton.normal());          // → Enviar   (this = boton)
console.log(suelta());                // → undefined (this se perdió)
const atada = boton.normal.bind(boton);
console.log(atada());                 // → Enviar   (bind fija el this)
```

⚠️ Cuidado: olvidar `new` (`const p = Perro("x")`) da error con clases: "Class constructor cannot be invoked without new".
💡 Consejo: en código de frontend moderno (React) se usan más funciones y objetos simples que clases, pero las verás en Node, librerías y entrevistas.
🇬🇧 **class** /klas/ = clase · **instance** /ínstans/ = instancia · **constructor** /konstráktor/ = constructor · **inheritance** /injéritans/ = herencia · **method** /mézod/ = método · **private field** /práivet fild/ = campo privado · **getter** /guéter/ = obtenedor

## 📤 Módulos import/export

Los **módulos** dividen el código en archivos. Cada archivo exporta lo que quiere compartir y los demás lo importan. Hay **export con nombre** (varios por archivo, se importan con llaves) y **export default** (uno por archivo, se importa con el nombre que quieras). En el navegador se activan con `<script type="module">`; en Node con `"type": "module"` en package.json o con archivos `.mjs`.

- `export const PI = 3.14;` :: Export con nombre
- `export function sumar(a, b) { }` :: Exportar una función con nombre
- `export default class Api { }` :: Export por defecto (uno por archivo)
- `import { PI, sumar } from "./mate.js";` :: Importar con nombre (llaves, mismo nombre)
- `import Api from "./api.js";` :: Importar el default (sin llaves, nombre libre)
- `import { sumar as add } from "./mate.js";` :: Renombrar al importar
- `import * as mate from "./mate.js";` :: Todo en un objeto: mate.PI
- `const mod = await import("./pesado.js");` :: Import dinámico (carga bajo demanda)
- `export { a, b } from "./otro.js";` :: Re-exportar (archivo índice)

```js
// archivo: utils/mate.js
export const IVA = 0.13;
export function conIva(precio) {
  return +(precio * (1 + IVA)).toFixed(2);
}
export default function redondear(n) {
  return Math.round(n);
}

// archivo: main.js
import redondear, { conIva, IVA } from "./utils/mate.js";
console.log(conIva(100), IVA, redondear(4.6)); // → 113 0.13 5
```

⚠️ Cuidado: en el navegador y en Node con ESM la ruta debe llevar la extensión: `"./mate.js"`, no `"./mate"`.
⚠️ Cuidado: abrir un HTML con módulos haciendo doble clic (file://) falla por CORS; sírvelo con un servidor local (`npx serve` o Live Server).
💡 Consejo: prefiere exports con nombre: el editor autocompleta mejor y es más fácil renombrar.
🇬🇧 **module** /módiul/ = módulo · **import** /ímport/ = importar · **export** /éksport/ = exportar · **default** /difólt/ = por defecto · **named export** /néimd éksport/ = exportación con nombre · **bundle** /bándol/ = paquete empaquetado

## 🚨 Manejo de errores

Cuando algo sale mal, JS **lanza** (throw) un error. Si nadie lo **atrapa** (catch), el programa se detiene. Con `try/catch` decides qué hacer: mostrar un mensaje, reintentar o usar un valor por defecto. `finally` se ejecuta siempre, haya error o no (ideal para ocultar un "cargando…").

- `try { } catch (err) { } finally { }` :: Intentar, atrapar el error, y limpiar siempre
- `throw new Error("mensaje")` :: Lanzar tu propio error
- `err.message; err.name; err.stack` :: Texto, tipo y traza del error
- `new Error("x", { cause: err })` :: Error nuevo que guarda la causa original
- `class ValidacionError extends Error { }` :: Tipo de error propio
- `err instanceof TypeError` :: Saber qué tipo de error es

| Error | Cuándo aparece |
|---|---|
| `ReferenceError` | usas una variable que no existe |
| `TypeError` | usas un valor de forma incorrecta (undefined.x, llamar algo que no es función) |
| `SyntaxError` | código o JSON mal escrito (JSON.parse de texto inválido) |
| `RangeError` | número fuera de rango (new Array(-1)) |

```js
class ValidacionError extends Error {
  constructor(campo, mensaje) {
    super(mensaje);
    this.name = "ValidacionError";
    this.campo = campo;
  }
}

function parsearEdad(texto) {
  const edad = Number(texto);
  if (Number.isNaN(edad)) throw new ValidacionError("edad", `"${texto}" no es un número`);
  if (edad < 0) throw new ValidacionError("edad", "La edad no puede ser negativa");
  return edad;
}

for (const entrada of ["21", "abc", "-3"]) {
  try {
    console.log("OK:", parsearEdad(entrada));
  } catch (err) {
    if (err instanceof ValidacionError) console.log(`Campo ${err.campo}: ${err.message}`);
    else throw err;                   // errores inesperados: no los escondas
  } finally {
    console.log("--- revisado:", entrada);
  }
}
// → OK: 21 / --- revisado: 21 / Campo edad: "abc" no es un número / ... / Campo edad: La edad no puede ser negativa

try {
  JSON.parse("{mal json}");
} catch (err) {
  console.log(err.name);              // → SyntaxError
}
```

⚠️ Cuidado: un `catch` vacío (`catch {}`) esconde errores y luego no sabes por qué algo no funciona. Al menos haz `console.error(err)`.
⚠️ Cuidado: `try/catch` NO atrapa errores de una promesa sin `await` ni de un `setTimeout`; dentro de funciones async usa `await` en el try.
💡 Consejo: lanza siempre `new Error(...)` (no strings sueltos) para tener la traza (stack) que dice en qué línea pasó.
🇬🇧 **error** /érror/ = error · **throw** /zróu/ = lanzar · **catch** /kach/ = atrapar · **stack trace** /stak tréis/ = traza de llamadas · **bug** /bag/ = fallo · **handle** /jándol/ = manejar

## ⏳ Asincronía y event loop

JavaScript tiene **un solo hilo**: hace una cosa a la vez. Para no congelarse mientras espera algo lento (una petición a internet, un temporizador, leer un archivo), delega esa espera al navegador o a Node y sigue con lo demás. Cuando la espera termina, la tarea pendiente se pone en una **cola**, y el **event loop** (bucle de eventos) la ejecuta apenas la pila de llamadas queda libre.

Piensa en un restaurante con un solo mesero: toma tu pedido (llamada), lo pasa a la cocina (Web API), atiende otras mesas, y cuando el plato está listo (cola) te lo trae. Hay dos colas: las **microtareas** (promesas, se atienden primero) y las **macrotareas** (setTimeout, eventos).

La evolución para escribir código asíncrono fue: **callbacks** (funciones que se llaman al terminar; se anidan feo: "callback hell") → **promesas** (un objeto que representa un valor futuro: pendiente, cumplida o rechazada) → **async/await** (escribir código asíncrono que se lee como normal).

- `setTimeout(fn, 1000)` :: Ejecuta fn una vez dentro de ~1 segundo
- `setInterval(fn, 1000)` :: Ejecuta fn cada segundo (para con clearInterval)
- `new Promise((resolve, reject) => { })` :: Crear una promesa
- `promesa.then(v => { }).catch(e => { })` :: Usar el valor o el error
- `.finally(() => { })` :: Se ejecuta al terminar, salga bien o mal
- `async function f() { }` :: Función que siempre devuelve una promesa
- `const v = await promesa;` :: Espera el valor (solo dentro de async o módulo)
- `Promise.all([p1, p2])` :: Espera todas; falla si UNA falla
- `Promise.allSettled([p1, p2])` :: Espera todas y te dice cuál salió bien o mal
- `Promise.race([p1, p2])` :: La primera que termine (bien o mal)
- `Promise.any([p1, p2])` :: La primera que salga BIEN
- `const esperar = ms => new Promise(r => setTimeout(r, ms));` :: Helper para pausar

```js
console.log("1. inicio");
setTimeout(() => console.log("4. timeout (macrotarea)"), 0);
Promise.resolve().then(() => console.log("3. promesa (microtarea)"));
console.log("2. fin del código normal");
// → 1. inicio / 2. fin del código normal / 3. promesa (microtarea) / 4. timeout (macrotarea)
```

### 🪜 De callbacks a promesas a async/await

```js
// 1) Callbacks: cada paso dentro del anterior (difícil de leer)
function pedirUsuarioCb(id, cb) {
  setTimeout(() => cb(null, { id, nombre: "Ana" }), 100);
}
pedirUsuarioCb(1, (err, usuario) => {
  if (err) return console.error(err);
  console.log("callback:", usuario.nombre);   // → callback: Ana
});

// 2) Promesas: se encadenan con .then
function pedirUsuario(id) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (id <= 0) reject(new Error("id inválido"));
      else resolve({ id, nombre: "Ana" });
    }, 100);
  });
}
pedirUsuario(1)
  .then(u => console.log("then:", u.nombre))  // → then: Ana
  .catch(e => console.error(e.message));

// 3) async/await: se lee de arriba a abajo
async function mostrar() {
  try {
    const u = await pedirUsuario(1);
    console.log("await:", u.nombre);          // → await: Ana
    await pedirUsuario(-1);
  } catch (e) {
    console.log("error atrapado:", e.message); // → error atrapado: id inválido
  }
}
mostrar();
```

### ✅ Ejemplo resuelto: Promise.all, allSettled y race

```js
const esperar = (ms, valor, falla = false) =>
  new Promise((res, rej) => setTimeout(() => (falla ? rej(new Error(valor)) : res(valor)), ms));

async function demo() {
  console.time("all");
  const [a, b] = await Promise.all([esperar(300, "notas"), esperar(200, "horario")]);
  console.timeEnd("all");                      // → all: ~300ms (en paralelo, no 500)
  console.log(a, b);                           // → notas horario

  const resultados = await Promise.allSettled([esperar(50, "ok"), esperar(50, "caído", true)]);
  console.log(resultados.map(r => r.status));  // → [ 'fulfilled', 'rejected' ]

  const ganador = await Promise.race([esperar(100, "lento"), esperar(10, "rápido")]);
  console.log(ganador);                        // → rápido

  try {
    await Promise.race([esperar(5000, "datos"), esperar(100, "timeout", true)]);
  } catch (e) {
    console.log("Se rindió por:", e.message);  // → Se rindió por: timeout
  }
}
demo();
```

⚠️ Cuidado: `await` dentro de un `for` hace las peticiones UNA TRAS OTRA. Si son independientes, usa `Promise.all(lista.map(async x => ...))`.
⚠️ Cuidado: olvidar `await` te deja una promesa en vez del valor: verás `Promise { <pending> }` en la consola.
⚠️ Cuidado: `forEach` no espera a funciones async; usa `for...of` con await o `Promise.all`.
💡 Consejo: `setTimeout(fn, 0)` no es "inmediato": espera a que termine todo el código actual y las microtareas.
🇬🇧 **asynchronous** /eisínkronos/ = asíncrono · **promise** /prómis/ = promesa · **resolve** /risólv/ = resolver · **reject** /riyékt/ = rechazar · **pending** /pénding/ = pendiente · **await** /euéit/ = esperar · **event loop** /ivént lup/ = bucle de eventos · **queue** /kiú/ = cola · **thread** /zred/ = hilo

## 🌐 fetch y JSON

**JSON** es texto con forma de objeto JS: así viajan los datos entre el frontend y el backend. `JSON.stringify` convierte objeto → texto y `JSON.parse` texto → objeto. **fetch** hace peticiones HTTP y devuelve una promesa con la respuesta. Ojo: fetch solo falla (rechaza) por errores de red; un 404 o 500 NO es error para fetch, tienes que revisar `res.ok`.

- `JSON.stringify(obj)` :: Objeto → texto JSON
- `JSON.stringify(obj, null, 2)` :: Igual pero con sangría de 2 espacios (legible)
- `JSON.parse(texto)` :: Texto JSON → objeto
- `const res = await fetch(url);` :: GET: pedir datos
- `res.ok; res.status` :: ¿Salió bien (200-299)? / código HTTP
- `await res.json()` :: Leer el cuerpo como JSON
- `await res.text()` :: Leer el cuerpo como texto
- `fetch(url, { method: "POST", headers, body })` :: Enviar datos
- `headers: { "Content-Type": "application/json" }` :: Avisar que envías JSON
- `new URLSearchParams({ q: "bolivia", page: 2 })` :: Armar query string seguro
- `AbortSignal.timeout(5000)` :: Cancelar la petición si tarda más de 5 s

| Código | Significa |
|---|---|
| 200 OK | todo bien |
| 201 Created | se creó el recurso (respuesta típica de POST) |
| 204 No Content | bien, pero sin cuerpo (típico de DELETE) |
| 400 Bad Request | enviaste datos mal formados |
| 401 / 403 | no autenticado / sin permiso |
| 404 Not Found | no existe |
| 500 | error del servidor |

```js
const persona = { nombre: "Ana", edad: 20, intereses: ["IA", "web"] };
const texto = JSON.stringify(persona);
console.log(texto);                    // → {"nombre":"Ana","edad":20,"intereses":["IA","web"]}
console.log(JSON.parse(texto).intereses[0]); // → IA
```

### ✅ Ejemplo resuelto: helper de fetch con GET y POST

```js
async function api(url, { method = "GET", datos } = {}) {
  const res = await fetch(url, {
    method,
    headers: datos ? { "Content-Type": "application/json" } : {},
    body: datos ? JSON.stringify(datos) : undefined,     // GET no lleva body
    signal: AbortSignal.timeout(8000),                   // máximo 8 segundos
  });
  if (!res.ok) throw new Error(`HTTP ${res.status} en ${url}`); // 404/500 → error
  return res.status === 204 ? null : res.json();
}

const BASE = "https://jsonplaceholder.typicode.com";

async function main() {
  try {
    // GET con parámetros de búsqueda
    const params = new URLSearchParams({ userId: 1 });
    const posts = await api(`${BASE}/posts?${params}`);
    console.log(posts.length, "posts del usuario 1");     // → 10 posts del usuario 1

    // POST: crear un recurso
    const nuevo = await api(`${BASE}/posts`, {
      method: "POST",
      datos: { title: "Hola", body: "Desde Bolivia", userId: 1 },
    });
    console.log("creado con id", nuevo.id);               // → creado con id 101

    await api(`${BASE}/no-existe`);                        // provoca un 404
  } catch (err) {
    console.log("Falló:", err.message);                    // → Falló: HTTP 404 en https://...
  }
}
main();
```

⚠️ Cuidado: `fetch` no lanza error con 404 o 500. Siempre revisa `if (!res.ok)`.
⚠️ Cuidado: el error "blocked by CORS policy" no se arregla en el frontend: el SERVIDOR debe permitir tu origen (ver la hoja de Node).
⚠️ Cuidado: `res.json()` también es una promesa: necesita `await`. Y solo se puede leer el cuerpo una vez.
💡 Consejo: en las DevTools pestaña **Network** ves cada petición, su estado, cabeceras y respuesta. Es lo primero que se revisa cuando algo no llega.
🇬🇧 **request** /rikuést/ = petición · **response** /rispóns/ = respuesta · **header** /jéder/ = cabecera · **body** /bódi/ = cuerpo · **endpoint** /éndpoint/ = dirección de la API · **payload** /péiloud/ = datos enviados · **status code** /stéitus kóud/ = código de estado

## 🖱️ DOM: seleccionar, crear, eventos

El **DOM** (Document Object Model) es el HTML convertido en objetos que JS puede leer y cambiar. Con él buscas elementos, cambias su texto o clases, creas nuevos y reaccionas a eventos (clics, teclas, envíos). La **delegación de eventos** consiste en poner un solo listener en el padre en vez de uno por hijo: funciona incluso con elementos que agregas después.

- `document.querySelector(".tarjeta")` :: Primer elemento que coincide con el selector CSS
- `document.querySelectorAll("li")` :: Todos (NodeList; se recorre con for...of)
- `document.getElementById("menu")` :: Por id (sin #)
- `el.textContent = "Hola"` :: Cambiar el texto (seguro)
- `el.innerHTML = "<b>Hola</b>"` :: Cambiar el HTML (¡cuidado con datos del usuario!)
- `el.classList.add("activo")` :: Añadir clase (también remove, toggle, contains)
- `el.style.color = "red"` :: Estilo en línea
- `el.setAttribute("href", url)` :: Poner atributo (getAttribute para leer)
- `el.dataset.id` :: Lee el atributo data-id="..."
- `document.createElement("li")` :: Crear un elemento nuevo
- `padre.append(hijo)` :: Agregar al final (prepend al inicio)
- `el.remove()` :: Quitar el elemento de la página
- `el.closest(".tarea")` :: Sube por los padres hasta encontrar el selector
- `el.addEventListener("click", e => { })` :: Escuchar un evento
- `e.target` :: El elemento exacto donde ocurrió el evento
- `e.preventDefault()` :: Evitar la acción por defecto (enviar form, seguir link)

| Evento | Cuándo |
|---|---|
| `click` | clic en el elemento |
| `input` | cada vez que cambia el texto de un campo |
| `change` | al confirmar un cambio (select, checkbox) |
| `submit` | al enviar un formulario |
| `keydown` | al presionar una tecla (e.key) |
| `DOMContentLoaded` | el HTML terminó de cargar |

```js
// HTML: <ul id="lista"><li data-id="1">Leer</li><li data-id="2">Programar</li></ul>
const lista = document.querySelector("#lista");

// Crear y agregar un elemento
const li = document.createElement("li");
li.textContent = "Dormir";
li.dataset.id = "3";
lista.append(li);

// Delegación: UN listener para todos los <li>, incluso los nuevos
lista.addEventListener("click", e => {
  const item = e.target.closest("li");
  if (!item) return;                       // clic fuera de un li
  item.classList.toggle("hecho");
  console.log("Tocaste la tarea", item.dataset.id);
});

// Teclado
document.addEventListener("keydown", e => {
  if (e.key === "Escape") console.log("Cerrar modal");
});
```

⚠️ Cuidado: si tu script está en el `<head>` sin `defer`, el DOM aún no existe y `querySelector` devuelve null. Usa `<script src="app.js" defer>` o `type="module"`.
⚠️ Cuidado: `innerHTML` con texto del usuario permite inyectar código (XSS). Para texto usa `textContent`.
💡 Consejo: `querySelectorAll` devuelve NodeList; si quieres `map` o `filter` conviértelo con `[...nodos]` o `Array.from(nodos)`.
🇬🇧 **element** /élement/ = elemento · **node** /nóud/ = nodo · **event listener** /ivént lísener/ = escuchador de eventos · **target** /tárguet/ = objetivo · **event delegation** /ivént deleguéishon/ = delegación de eventos · **render** /rénder/ = dibujar

## 📝 Formularios y validación

Un formulario se maneja escuchando su evento `submit` (no el clic del botón), cancelando el envío por defecto con `preventDefault()` y leyendo los datos con **FormData**. Valida primero con HTML (`required`, `type="email"`, `minlength`, `pattern`) y luego en JS para reglas propias. Y recuerda: la validación del frontend es por comodidad; la de verdad se repite en el servidor.

- `form.addEventListener("submit", e => { e.preventDefault(); })` :: Interceptar el envío
- `new FormData(form)` :: Lee todos los campos con atributo name
- `Object.fromEntries(new FormData(form))` :: Todos los campos como objeto
- `input.value` :: Valor actual de un campo (siempre string)
- `input.valueAsNumber` :: Valor de un input number como número
- `checkbox.checked` :: ¿Está marcado?
- `input.setCustomValidity("msg")` :: Marca el campo como inválido con tu mensaje ("" lo limpia)
- `form.reportValidity()` :: Muestra los mensajes de error del navegador
- `form.reset()` :: Vacía el formulario
- `<input name="email" type="email" required>` :: Validación nativa en HTML

### ✅ Ejemplo resuelto: registro con validación

```js
// HTML:
// <form id="registro" novalidate>
//   <input name="nombre" required minlength="2">
//   <input name="email" type="email" required>
//   <input name="edad" type="number">
//   <p id="errores"></p>
//   <button>Registrar</button>
// </form>
const form = document.querySelector("#registro");
const cajaErrores = document.querySelector("#errores");

function validar({ nombre, email, edad }) {
  const errores = [];
  if (nombre.trim().length < 2) errores.push("El nombre debe tener 2 letras o más");
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) errores.push("Email inválido");
  if (edad && (Number(edad) < 16 || Number(edad) > 99)) errores.push("Edad entre 16 y 99");
  return errores;
}

form.addEventListener("submit", e => {
  e.preventDefault();                                 // 1. no recargar la página
  const datos = Object.fromEntries(new FormData(form)); // 2. { nombre, email, edad }
  const errores = validar(datos);                     // 3. reglas propias
  if (errores.length) {
    cajaErrores.textContent = errores.join(" · ");    // 4. mostrar errores
    return;
  }
  cajaErrores.textContent = "";
  console.log("Enviar al servidor:", datos);          // 5. aquí iría un fetch POST
  form.reset();
});
```

⚠️ Cuidado: `input.value` siempre es texto: `"5" + "3"` da `"53"`. Convierte con `Number()` antes de calcular.
💡 Consejo: el atributo `novalidate` desactiva las burbujas del navegador para que muestres tus propios mensajes; quítalo si te bastan las nativas.
🇬🇧 **form** /form/ = formulario · **submit** /sabmít/ = enviar · **field** /fild/ = campo · **required** /rikuáierd/ = obligatorio · **validation** /validéishon/ = validación · **input** /ínput/ = entrada

## 💾 localStorage

**localStorage** guarda datos en el navegador que sobreviven al recargar o cerrar la pestaña (por dominio, unos 5 MB). Solo guarda **texto**, así que los objetos se pasan por `JSON.stringify` al guardar y `JSON.parse` al leer. **sessionStorage** es igual pero se borra al cerrar la pestaña.

- `localStorage.setItem("tema", "oscuro")` :: Guardar un texto
- `localStorage.getItem("tema")` :: Leer (null si no existe)
- `localStorage.removeItem("tema")` :: Borrar una clave
- `localStorage.clear()` :: Borrar todo lo de este sitio
- `localStorage.setItem("tareas", JSON.stringify(tareas))` :: Guardar un objeto/array
- `JSON.parse(localStorage.getItem("tareas")) ?? []` :: Leer con valor por defecto

```js
const almacen = {
  leer(clave, porDefecto) {
    try {
      return JSON.parse(localStorage.getItem(clave)) ?? porDefecto;
    } catch {
      return porDefecto;                 // texto corrupto → valor por defecto
    }
  },
  guardar(clave, valor) {
    localStorage.setItem(clave, JSON.stringify(valor));
  },
};

const prefs = almacen.leer("prefs", { tema: "claro", idioma: "es" });
prefs.tema = "oscuro";
almacen.guardar("prefs", prefs);
document.documentElement.dataset.tema = prefs.tema;  // <html data-tema="oscuro">
```

⚠️ Cuidado: nunca guardes contraseñas ni tokens sensibles en localStorage: cualquier script de la página puede leerlo.
⚠️ Cuidado: `localStorage.setItem("x", {a: 1})` guarda el texto "[object Object]". Usa JSON.stringify.
🇬🇧 **storage** /stóridch/ = almacenamiento · **key** /ki/ = clave · **persist** /persíst/ = persistir · **session** /séshon/ = sesión · **serialize** /sírialaiz/ = convertir a texto

## 📅 Fechas: Date e Intl

`Date` guarda un instante en el tiempo (milisegundos desde 1970). Tiene trampas: **los meses van de 0 a 11**. Para mostrar fechas, números y monedas bonitos en español usa **Intl** (internacionalización), que formatea según el país sin librerías.

- `new Date()` :: Ahora mismo
- `new Date(2026, 0, 15)` :: 15 de ENERO de 2026 (mes 0 = enero)
- `new Date("2026-08-06T10:00:00")` :: Desde texto ISO (hora local)
- `Date.now()` :: Milisegundos actuales (para medir tiempos)
- `d.getFullYear(); d.getMonth(); d.getDate()` :: Año / mes (0-11) / día del mes
- `d.getDay()` :: Día de la semana (0 = domingo)
- `d.toISOString()` :: Texto ISO en UTC: "2026-08-06T14:00:00.000Z"
- `d.toLocaleDateString("es-BO")` :: Fecha con formato boliviano
- `new Intl.NumberFormat("es-BO", { style: "currency", currency: "BOB" })` :: Formato de moneda
- `new Intl.RelativeTimeFormat("es", { numeric: "auto" })` :: "ayer", "en 3 días"

```js
const independencia = new Date(2026, 7, 6);          // 6 de agosto (mes 7)
console.log(independencia.getMonth() + 1);           // → 8

const fmt = new Intl.DateTimeFormat("es-BO", { dateStyle: "full" });
console.log(fmt.format(independencia));              // → jueves, 6 de agosto de 2026

const bs = new Intl.NumberFormat("es-BO", { style: "currency", currency: "BOB" });
console.log(bs.format(1234.5));                      // → Bs 1.234,50

const rel = new Intl.RelativeTimeFormat("es", { numeric: "auto" });
console.log(rel.format(-1, "day"), "|", rel.format(3, "week")); // → ayer | dentro de 3 semanas
```

### ✅ Ejemplo resuelto: ¿cuántos días faltan?

```js
function diasEntre(desde, hasta) {
  const MS_POR_DIA = 1000 * 60 * 60 * 24;
  const a = Date.UTC(desde.getFullYear(), desde.getMonth(), desde.getDate()); // sin horas
  const b = Date.UTC(hasta.getFullYear(), hasta.getMonth(), hasta.getDate());
  return Math.round((b - a) / MS_POR_DIA);          // restar fechas da milisegundos
}
console.log(diasEntre(new Date(2026, 9, 18), new Date(2026, 11, 25))); // → 68
```

⚠️ Cuidado: `new Date("2026-08-06")` (solo fecha) se interpreta en UTC y en Bolivia (UTC-4) puede mostrarse como el día 5. Añade la hora: `"2026-08-06T00:00"`.
💡 Consejo: guarda y envía fechas en ISO (`toISOString`) y conviértelas a formato local solo al mostrarlas.
🇬🇧 **date** /déit/ = fecha · **timestamp** /táimstamp/ = marca de tiempo · **time zone** /táim sóun/ = zona horaria · **locale** /loukál/ = configuración regional · **format** /fórmat/ = formatear

## 🔍 Expresiones regulares básicas

Una **regex** es un patrón para buscar o validar texto: emails, teléfonos, extraer números… Se escriben entre barras `/patrón/banderas`. Con `test` preguntas si coincide, con `match`/`matchAll` extraes, y con `replace` sustituyes.

| Patrón | Significa | Ejemplo que coincide |
|---|---|---|
| `\d` | un dígito 0-9 | `7` |
| `\w` | letra, dígito o _ | `a` |
| `\s` | espacio, tab, salto | ` ` |
| `.` | cualquier carácter | `x` |
| `[abc]` / `[^abc]` | uno de esos / ninguno de esos | `b` |
| `+ * ?` | 1 o más / 0 o más / 0 o 1 | `\d+` → `2026` |
| `{2,4}` | entre 2 y 4 veces | `\d{3}` → `591` |
| `^ $` | inicio / fin del texto | `^hola$` |
| `( )` | grupo que se captura | `(\d+)-(\d+)` |
| `(?<año>\d{4})` | grupo con nombre | `m.groups.año` |
| `a|b` | a o b | `gato|perro` |

- `/^\d{8}$/.test("71234567")` :: ¿Son exactamente 8 dígitos? → true
- `"a1b22".match(/\d+/g)` :: Todas las coincidencias → ["1", "22"]
- `texto.replace(/\s+/g, " ")` :: Varios espacios → uno
- `/hola/i` :: Bandera i: ignora mayúsculas
- `/x/g` :: Bandera g: global (todas las coincidencias)

```js
const celular = /^[67]\d{7}$/;                     // celulares bolivianos: 8 dígitos, empiezan en 6 o 7
console.log(celular.test("71234567"), celular.test("21234567")); // → true false

const texto = "Pedidos: 3 salteñas a Bs 8 y 2 apis a Bs 6";
console.log(texto.match(/\d+/g));                  // → [ '3', '8', '2', '6' ]

const fecha = "2026-10-18".match(/(?<año>\d{4})-(?<mes>\d{2})-(?<dia>\d{2})/);
console.log(fecha.groups.dia, fecha.groups.mes);   // → 18 10

console.log("2026-10-18".replace(/(\d+)-(\d+)-(\d+)/, "$3/$2/$1")); // → 18/10/2026

for (const m of "#js #node #ia".matchAll(/#(\w+)/g)) console.log(m[1]); // → js / node / ia
```

⚠️ Cuidado: los caracteres especiales `. * + ? ( ) [ ] { } ^ $ | \ /` se escapan con `\` para buscarlos literalmente: `/\./` busca un punto.
💡 Consejo: prueba tus regex en regex101.com (elige "ECMAScript") antes de usarlas; te explica cada parte.
🇬🇧 **regular expression** /réguiular expréshon/ = expresión regular · **pattern** /pátern/ = patrón · **match** /match/ = coincidir/coincidencia · **flag** /flag/ = bandera · **escape** /eskéip/ = escapar

## 🧺 Map y Set

**Set** es una colección de valores **sin repetidos**: perfecta para quitar duplicados o saber rápido si algo ya está. **Map** es como un objeto de clave → valor, pero las claves pueden ser de cualquier tipo (objetos, números), mantiene el orden de inserción y tiene `size`. Úsalo cuando agregas y quitas claves todo el tiempo.

- `new Set([1, 2, 2, 3])` :: Set {1, 2, 3}
- `[...new Set(lista)]` :: Quitar duplicados de un array
- `set.add(v); set.has(v); set.delete(v)` :: Añadir / ¿está? / quitar
- `set.size` :: Cantidad de elementos
- `a.union(b); a.intersection(b); a.difference(b)` :: Operaciones de conjuntos (moderno)
- `new Map()` :: Map vacío
- `map.set(k, v); map.get(k)` :: Guardar / leer
- `map.has(k); map.delete(k)` :: ¿Existe? / borrar
- `new Map(Object.entries(obj))` :: Objeto → Map
- `for (const [k, v] of map) { }` :: Recorrer un Map

```js
const inscritos = ["ana", "luis", "ana", "eva", "luis"];
const unicos = [...new Set(inscritos)];
console.log(unicos);                            // → [ 'ana', 'luis', 'eva' ]

const calculo = new Set(["ana", "luis", "eva"]);
const fisica = new Set(["luis", "eva", "rosa"]);
console.log([...calculo.intersection(fisica)]); // → [ 'luis', 'eva' ]
console.log([...calculo.difference(fisica)]);   // → [ 'ana' ]

// Map como caché: guarda resultados ya calculados
const cache = new Map();
function fibonacci(n) {
  if (n < 2) return n;
  if (cache.has(n)) return cache.get(n);
  const r = fibonacci(n - 1) + fibonacci(n - 2);
  cache.set(n, r);
  return r;
}
console.log(fibonacci(50), cache.size);         // → 12586269025 49
```

💡 Consejo: `set.has(x)` es casi instantáneo aunque el Set tenga un millón de elementos; `array.includes(x)` revisa uno por uno.
🇬🇧 **set** /set/ = conjunto · **map** /map/ = mapa/diccionario · **duplicate** /diúplikeit/ = duplicado · **unique** /iuník/ = único · **cache** /kash/ = memoria rápida

## 🛠️ Utilidades modernas

JavaScript se actualiza cada año (ES2015, ES2020…). Estas herramientas modernas ahorran código y evitan bugs; todas funcionan en navegadores actuales y en Node reciente.

- `structuredClone(obj)` :: Copia profunda real (incluye Date, Map, Set)
- `Array.from("hola")` :: Texto o iterable → array ['h','o','l','a']
- `Array.from({ length: 5 }, (_, i) => i * 2)` :: Generar [0, 2, 4, 6, 8]
- `xs.at(-1)` :: Último elemento sin xs[xs.length - 1]
- `obj?.a?.b ?? "def"` :: Leer seguro con valor por defecto
- `Object.groupBy(xs, fn)` :: Agrupar elementos en un objeto de listas
- `xs.toSorted(); xs.toReversed(); xs.with(0, "x")` :: Versiones que no modifican
- `xs.findLast(fn)` :: Último que cumple (también findLastIndex)
- `Object.hasOwn(obj, "k")` :: ¿Tiene esa propiedad propia?
- `1_000_000` :: Separador numérico para leer mejor
- `crypto.randomUUID()` :: Id único aleatorio
- `queueMicrotask(fn)` :: Ejecutar fn justo después del código actual
- `Math.trunc(-4.7); Math.round(4.5)` :: Quitar decimales / redondear
- `Math.floor(Math.random() * 6) + 1` :: Entero aleatorio del 1 al 6 (dado)

```js
const original = { nombre: "Ana", fechas: [new Date(2026, 0, 1)], tags: new Set(["ia"]) };
const copia = structuredClone(original);
copia.fechas[0].setFullYear(2030);
console.log(original.fechas[0].getFullYear());  // → 2026 (el original no cambió)
console.log(copia.tags.has("ia"));              // → true

const notas = [40, 85, 60, 92];
console.log(notas.at(-1), notas.findLast(n => n < 70)); // → 92 60
console.log(notas.with(0, 51), notas[0]);       // → [ 51, 85, 60, 92 ] 40

console.log(Array.from({ length: 5 }, (_, i) => i * 2)); // → [ 0, 2, 4, 6, 8 ]
console.log(crypto.randomUUID().length);        // → 36
```

⚠️ Cuidado: `structuredClone` no copia funciones ni instancias de clase con sus métodos (las vuelve objetos simples).
💡 Consejo: si dudas si algo es soportado, busca en caniuse.com o en MDN (sección "Browser compatibility").
🇬🇧 **clone** /klóun/ = clonar · **utility** /iutíliti/ = utilidad · **feature** /fícher/ = característica · **polyfill** /pólifil/ = parche para navegadores viejos · **random** /rándom/ = aleatorio

## 🐞 Depurar

Depurar (debug) es encontrar por qué el código no hace lo que esperas. La consola tiene mucho más que `console.log`, y las **DevTools** (F12) te dejan pausar el código línea por línea con **breakpoints** y ver el valor de cada variable.

- `console.log("x:", x)` :: Mostrar valores (pon etiqueta para saber cuál es)
- `console.log({ x, y })` :: Truco: muestra nombre y valor a la vez
- `console.table(lista)` :: Muestra un array de objetos como tabla
- `console.error(err); console.warn("ojo")` :: En rojo / en amarillo
- `console.dir(obj, { depth: null })` :: Objeto completo (útil en Node)
- `console.group("x"); console.groupEnd()` :: Agrupa mensajes con sangría
- `console.time("t"); console.timeEnd("t")` :: Mide cuánto tarda algo
- `console.count("clics")` :: Cuenta cuántas veces pasó por ahí
- `console.assert(x > 0, "x debe ser positivo")` :: Avisa solo si la condición falla
- `debugger;` :: Pausa aquí si las DevTools están abiertas
- `node --inspect-brk app.js` :: Depurar Node en Chrome (chrome://inspect)

```js
const alumnos = [
  { nombre: "Ana", nota: 95 },
  { nombre: "Luis", nota: 48 },
  { nombre: "Eva", nota: 71 },
];
console.table(alumnos);                 // tabla bonita con columnas nombre y nota

console.time("promedio");
const promedio = alumnos.reduce((s, a) => s + a.nota, 0) / alumnos.length;
console.timeEnd("promedio");            // → promedio: 0.05ms

const reprobados = alumnos.filter(a => a.nota < 51);
console.log({ promedio, reprobados: reprobados.length }); // → { promedio: 71.33333333333333, reprobados: 1 }
console.assert(promedio > 80, "El promedio es bajo");     // → Assertion failed: El promedio es bajo
```

### 🧭 Método para cazar un bug

1) Reproduce el error y lee el mensaje completo: tipo, texto y la línea (el stack). 2) Revisa la pestaña Console y Network. 3) Pon un `debugger` o breakpoint antes de la línea que falla y mira las variables. 4) Reduce: comenta código hasta aislar el trozo culpable. 5) Explica el problema en voz alta (técnica del patito de goma).

💡 Consejo: copia el mensaje de error exacto en inglés en el buscador; casi siempre alguien ya lo resolvió en Stack Overflow o en un issue de GitHub.
⚠️ Cuidado: borra los `console.log` y `debugger` antes de subir tu código; ensucian la consola de producción.
🇬🇧 **debug** /dibág/ = depurar · **breakpoint** /bréikpoint/ = punto de parada · **step over** /step óuver/ = pasar a la siguiente línea · **step into** /step íntu/ = entrar en la función · **rubber duck** /ráber dak/ = patito de goma

## 🏆 Ejemplos resueltos completos

Cuatro mini proyectos de navegador que juntan todo lo anterior. Copia el HTML en un archivo `index.html`, el JS en `app.js` y ábrelo con Live Server.

### ✅ Ejemplo resuelto: contador con botones

```js
// HTML: <h1 id="valor">0</h1>
//       <button data-accion="-1">−</button> <button data-accion="1">+</button>
//       <button data-accion="reset">Reiniciar</button>
const valor = document.querySelector("#valor");
let cuenta = Number(localStorage.getItem("cuenta")) || 0;  // recuerda el último valor

function pintar() {
  valor.textContent = cuenta;
  valor.style.color = cuenta < 0 ? "crimson" : "inherit";  // rojo si es negativo
  localStorage.setItem("cuenta", cuenta);
}

document.addEventListener("click", e => {
  const accion = e.target.dataset.accion;                  // delegación por data-accion
  if (!accion) return;
  cuenta = accion === "reset" ? 0 : cuenta + Number(accion);
  pintar();
});
pintar();
```

Qué hace: un solo listener en `document` atiende los tres botones leyendo su `data-accion`; `pintar()` es la única función que toca el DOM, así el estado (`cuenta`) y la vista nunca se desincronizan.

### ✅ Ejemplo resuelto: lista de tareas (crear, marcar, borrar, guardar)

```js
// HTML: <form id="nueva"><input name="texto" required placeholder="Nueva tarea"><button>Añadir</button></form>
//       <ul id="tareas"></ul> <p id="resumen"></p>
const form = document.querySelector("#nueva");
const ul = document.querySelector("#tareas");
const resumen = document.querySelector("#resumen");

let tareas = JSON.parse(localStorage.getItem("tareas")) ?? [];   // 1. estado inicial

function guardarYPintar() {
  localStorage.setItem("tareas", JSON.stringify(tareas));       // 2. persistir
  ul.replaceChildren(                                            // 3. redibujar la lista
    ...tareas.map(t => {
      const li = document.createElement("li");
      li.dataset.id = t.id;
      li.className = t.hecha ? "hecha" : "";
      li.innerHTML = `<input type="checkbox" ${t.hecha ? "checked" : ""}> <span></span> <button class="borrar">🗑️</button>`;
      li.querySelector("span").textContent = t.texto;            // texto seguro (sin XSS)
      return li;
    })
  );
  const pendientes = tareas.filter(t => !t.hecha).length;
  resumen.textContent = `${pendientes} pendiente(s) de ${tareas.length}`;
}

form.addEventListener("submit", e => {
  e.preventDefault();
  const texto = new FormData(form).get("texto").trim();
  if (!texto) return;
  tareas.push({ id: crypto.randomUUID(), texto, hecha: false }); // 4. crear
  form.reset();
  guardarYPintar();
});

ul.addEventListener("click", e => {                             // 5. delegación
  const id = e.target.closest("li")?.dataset.id;
  if (!id) return;
  if (e.target.matches(".borrar")) tareas = tareas.filter(t => t.id !== id);      // borrar
  if (e.target.matches("input[type=checkbox]"))
    tareas = tareas.map(t => (t.id === id ? { ...t, hecha: !t.hecha } : t));      // marcar
  guardarYPintar();
});

guardarYPintar();
```

Qué hace: el array `tareas` es la única fuente de verdad. Cada acción cambia el array (de forma inmutable con `filter`/`map`/spread) y luego llama a `guardarYPintar`, que guarda en localStorage y redibuja todo. Es exactamente la idea de React, pero a mano.

### ✅ Ejemplo resuelto: buscador que filtra mientras escribes

```js
// HTML: <input id="buscar" placeholder="Buscar ciudad..."> <ul id="resultados"></ul>
const ciudades = ["La Paz", "El Alto", "Cochabamba", "Santa Cruz", "Sucre", "Oruro", "Potosí", "Tarija", "Trinidad", "Cobija"];
const input = document.querySelector("#buscar");
const ul = document.querySelector("#resultados");

const normalizar = s => s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");

function debounce(fn, ms) {                 // espera a que el usuario deje de escribir
  let id;
  return (...args) => {
    clearTimeout(id);
    id = setTimeout(() => fn(...args), ms);
  };
}

function mostrar(termino) {
  const q = normalizar(termino.trim());
  const encontradas = ciudades.filter(c => normalizar(c).includes(q));
  ul.replaceChildren(
    ...encontradas.map(c => Object.assign(document.createElement("li"), { textContent: c }))
  );
  if (!encontradas.length) ul.textContent = "Sin resultados 😕";
}

input.addEventListener("input", debounce(e => mostrar(e.target.value), 200));
mostrar("");
// escribir "co" → Cochabamba, Cobija · escribir "potosi" (sin tilde) → Potosí
```

Qué hace: en cada tecla se reinicia un temporizador (`debounce`), así solo se filtra cuando paras 200 ms. `normalizar` quita tildes y mayúsculas para que "potosi" encuentre "Potosí".

### ✅ Ejemplo resuelto: consumir una API pública (usuarios)

```js
// HTML: <button id="cargar">Cargar usuarios</button> <p id="estado"></p> <ul id="usuarios"></ul>
const boton = document.querySelector("#cargar");
const estado = document.querySelector("#estado");
const ul = document.querySelector("#usuarios");

async function cargarUsuarios() {
  boton.disabled = true;
  estado.textContent = "Cargando… ⏳";
  try {
    const res = await fetch("https://jsonplaceholder.typicode.com/users");
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const usuarios = await res.json();
    ul.replaceChildren(
      ...usuarios
        .toSorted((a, b) => a.name.localeCompare(b.name))     // ordenar por nombre
        .map(({ name, email, address }) => {                  // desestructurar cada usuario
          const li = document.createElement("li");
          li.textContent = `${name} — ${email} (${address.city})`;
          return li;
        })
    );
    estado.textContent = `✅ ${usuarios.length} usuarios`;
  } catch (err) {
    estado.textContent = `❌ No se pudo cargar: ${err.message}`;
  } finally {
    boton.disabled = false;                                   // siempre reactivar el botón
  }
}
boton.addEventListener("click", cargarUsuarios);
// → ✅ 10 usuarios, lista ordenada: Chelsey Dietrich — Lucio_Hettinger@annie.ca (Roscoeview) ...
```

📌 Patrón para cualquier API: deshabilitar botón + "cargando" → fetch → revisar `res.ok` → `res.json()` → pintar → `catch` muestra el error → `finally` restaura la interfaz.
💡 Consejo: APIs públicas gratis para practicar: jsonplaceholder.typicode.com (datos falsos), pokeapi.co, restcountries.com, open-meteo.com (clima, sin clave).
🇬🇧 **to-do list** /tu du list/ = lista de tareas · **search bar** /serch bar/ = barra de búsqueda · **debounce** /dibáuns/ = esperar a que paren los eventos · **state** /stéit/ = estado · **loading** /lóuding/ = cargando · **source of truth** /sors ov truz/ = fuente de verdad
