# 🟨 JavaScript · El lenguaje de la web
> De la coerción rara al event loop: tipos, closures, this, prototipos, promesas, DOM, módulos y los errores que ya cometieron otros, con ejemplos comprobados en Node.

## 🟨 Qué es JavaScript y por qué existe

🧠 Concepto: **JavaScript** (JS) es un lenguaje de programación **interpretado y compilado al vuelo (JIT, just-in-time)**, de **tipado dinámico**, **multiparadigma** (imperativo, funcional y orientado a objetos con prototipos) y con **un solo hilo** que se apoya en un **event loop** (bucle de eventos) para no bloquearse.

Nació para un problema muy concreto: en 1995 las páginas web eran **documentos muertos**. Para validar un formulario había que mandarlo al servidor, esperar, y recibir otra página entera. Netscape quería un lenguaje pequeño, que cualquiera pudiera pegar dentro del HTML, para que la página **reaccionara** al usuario sin ir al servidor. Hoy es el único lenguaje que todos los navegadores ejecutan de forma nativa (WebAssembly es el otro formato que entienden, pero no se escribe a mano), y por eso se extendió a todo lo demás: servidores, apps de escritorio, móviles, CLIs y hasta funciones en el borde de la red (edge).

```capas
HTML : el contenido y la estructura — los sustantivos
CSS : la presentación — los adjetivos
JavaScript : el comportamiento — los verbos (qué pasa cuando...)
APIs del entorno : DOM, fetch, almacenamiento, timers — lo que el navegador o Node te prestan
Motor JS : V8, SpiderMonkey, JavaScriptCore — convierten tu código en código máquina
```

![JavaScript, TypeScript (JS con tipos) y Node.js (JS fuera del navegador): el trío que más vas a ver. Logos desde Wikimedia Commons](img/javascript/logos-js-ts-node.png)

### 🧭 Para qué se usa hoy (casos reales)

| Ámbito | Qué se hace con JS | Ejemplos reales conocidos |
|---|---|---|
| Frontend web | Interfaces interactivas (SPA) | Gmail, Google Docs, Facebook con React |
| Backend | APIs y servidores con Node.js | Netflix, PayPal y LinkedIn adoptaron Node |
| Escritorio | Apps con Electron (Chromium + Node) | VS Code, Discord, Slack |
| Móvil | React Native, apps híbridas | Partes de las apps de Meta (Facebook, Instagram) |
| Herramientas | CLIs, bundlers, linters | npm, ESLint, Prettier, Vite |
| Edge / serverless | Funciones cerca del usuario | Cloudflare Workers, Vercel, Deno Deploy |

💡 Consejo: VS Code, el editor que seguramente usas, está escrito en **TypeScript** y corre sobre **Electron**. Cuando abres su "Developer Tools" (Help → Toggle Developer Tools) ves la misma consola que en Chrome.

### 🧪 Tu primer programa (en el navegador y en Node)

```js
// Guarda como hola.js y ejecuta:  node hola.js
// O pégalo en la consola del navegador (F12 → Console)
const nombre = "Yamil";
const hora = new Date().getHours();
const saludo = hora < 12 ? "Buenos días" : hora < 19 ? "Buenas tardes" : "Buenas noches";
console.log(`${saludo}, ${nombre}. JavaScript funciona ✅`);
```

```flujo
Tu código .js -> Parser : texto → árbol (AST)
Parser -> Intérprete : bytecode, arranca rápido
Intérprete -> JIT : funciones "calientes"
JIT -> Código máquina : optimizado
Código máquina --> Intérprete : desoptimiza si cambian los tipos
```

🧠 Concepto: **JIT (Just-In-Time)**: el motor empieza interpretando (arranque rápido) y, cuando ve que una función se ejecuta muchas veces con los mismos tipos, la compila a código máquina optimizado. Si de pronto le pasas otro tipo, la **desoptimiza**. Por eso el código con tipos estables (siempre números, siempre los mismos campos) corre más rápido.

📌 Resumen: JS = el lenguaje del navegador que se escapó a todas partes. Un solo hilo + event loop, tipos dinámicos, funciones como valores y objetos con prototipos. Lo difícil no es la sintaxis: son la **coerción**, el **this**, la **asincronía** y la **mutación**. Esta hoja va justo por ahí.

## 📜 Historia: de 10 días a una versión por año

En mayo de 1995 **Brendan Eich**, en Netscape, escribió el primer prototipo en unos **10 días**. Se llamó Mocha, luego LiveScript y finalmente **JavaScript**, un nombre de marketing para aprovechar la fama de Java (no tienen nada que ver: "Java es a JavaScript lo que car es a carpet"). Para que Microsoft no impusiera su propia versión (JScript), Netscape llevó el lenguaje a **Ecma International**, que publica el estándar **ECMAScript** (ECMA-262). El comité que lo mantiene se llama **TC39**.

![Brendan Eich, creador de JavaScript (foto oficial de la Mozilla Foundation, Wikimedia Commons)](img/javascript/brendan-eich.jpg)

```tiempo
1995 : Brendan Eich crea JavaScript en Netscape (en ~10 días)
1996 : Microsoft lanza JScript en Internet Explorer 3; guerra de navegadores
1997 : ECMAScript 1, el primer estándar (ECMA-262)
1999 : ES3: expresiones regulares, try/catch
2005 : "AJAX": Gmail y Google Maps demuestran apps web de verdad
2008 : ES4 se abandona; Google lanza Chrome con el motor V8
2009 : ES5 (strict mode, JSON nativo) · Ryan Dahl presenta Node.js
2010 : nace npm, el gestor de paquetes
2012 : Microsoft publica TypeScript
2015 : ES2015 (ES6): let/const, clases, flechas, promesas, módulos
2017 : ES2017: async/await
2020 : ES2020: ?. ?? BigInt · Deno 1.0
2022 : ES2022: await en el nivel superior, campos #privados, .at()
2023 : ES2023: toSorted/toReversed/with · Bun 1.0
2024 : ES2024: Object.groupBy, Promise.withResolvers · Deno 2.0
2025 : ES2025: iterator helpers, métodos de Set, RegExp.escape, Promise.try
2026 : Temporal llega a los navegadores; Node ejecuta TypeScript quitando tipos
```

### 📚 Las versiones de ECMAScript que más importan

| Versión | Año | Lo que trajo (lo que usas a diario) |
|---|---|---|
| ES3 | 1999 | Regex, `try/catch`, la base de la web antigua |
| ES5 | 2009 | `"use strict"`, `JSON`, `forEach/map/filter` |
| ES2015 (ES6) | 2015 | `let/const`, `=>`, `class`, `Promise`, `import`, plantillas `${}` |
| ES2017 | 2017 | `async/await`, `Object.entries` |
| ES2020 | 2020 | `?.`, `??`, `BigInt`, `Promise.allSettled` |
| ES2022 | 2022 | `#privado`, `await` arriba del módulo, `.at(-1)` |
| ES2023 | 2023 | `toSorted`, `toReversed`, `with` (sin mutar) |
| ES2024 | 2024 | `Object.groupBy`, `Promise.withResolvers` |
| ES2025 | 2025 | Iterator helpers, `Set.union`, `RegExp.escape` |

🧠 Concepto: **TC39** trabaja con **etapas (stages)** del 0 al 4. Una propuesta en **Stage 4** entra en la siguiente edición anual. Si lees "Stage 3", ya está casi lista y los navegadores empiezan a implementarla; antes de eso, no la uses en producción sin un polyfill.

💡 Consejo: "ES6" y "ES2015" son lo mismo. Desde 2015 hay **una versión por año** con pocas novedades cada vez, en lugar de saltos gigantes como ES4, que fracasó por intentar cambiar demasiado.

🇬🇧 **ECMAScript** /ék-ma-skript/ = el nombre oficial del estándar · **proposal** /propóusal/ = propuesta · **stage** /stéich/ = etapa · **polyfill** /pólifil/ = código que imita una función nueva en entornos viejos

## 🌍 Dónde corre: navegador, Node, Deno y Bun

El lenguaje es el mismo; lo que cambia es el **entorno (runtime)**: el motor que ejecuta JS más las **APIs** que te presta. En el navegador tienes `document` y `window`; en Node tienes `fs` (archivos) y `process`, pero no hay DOM.

```capas
Tu código JS : el mismo lenguaje en todas partes
APIs del runtime : DOM y fetch (navegador) · fs, http, process (Node)
Event loop : navegador (HTML spec) · libuv (Node) · Tokio (Deno)
Motor : V8 · SpiderMonkey · JavaScriptCore
Sistema operativo : Linux, Windows, macOS, Android, iOS
```

| Runtime | Motor | Escrito en | Lo que lo distingue |
|---|---|---|---|
| Chrome / Edge | V8 | C++ | Los DevTools más usados |
| Firefox | SpiderMonkey | C++ y Rust | El primer motor de la historia (de Netscape) |
| Safari | JavaScriptCore | C++ | Único motor permitido en iOS durante años |
| Node.js | V8 | C++ y libuv | El estándar de servidor, ecosistema npm enorme |
| Deno | V8 | Rust | Seguro por defecto (permisos), TS directo |
| Bun | JavaScriptCore | Zig | Muy rápido al arrancar, todo en uno |

::: columnas
### 🟩 Node.js (2009)
- El más usado en servidores y herramientas.
- `npm` con millones de paquetes.
- CommonJS por historia, ESM hoy.
- Desde las versiones recientes ejecuta `.ts` quitando los tipos.
::: siguiente
### 🦕 Deno (2020)
- Del mismo creador de Node (Ryan Dahl).
- Permisos explícitos: `--allow-net`, `--allow-read`.
- TypeScript, formateador, linter y tests incluidos.
- Compatible con paquetes npm desde Deno 2.
::: siguiente
### 🥟 Bun (2023)
- Runtime + gestor de paquetes + bundler + tests.
- `bun install` muy rápido.
- Pretende ser reemplazo directo de Node.
- Menos maduro en casos raros de compatibilidad.
:::

### 🧪 Probarlo en tu PC

- `node` :: Abre la consola interactiva (REPL) de Node; sal con Ctrl+D
- `node archivo.js` :: Ejecuta un archivo
- `node --watch servidor.js` :: Reinicia solo al guardar cambios
- `node -p "1 + 1"` :: Evalúa e imprime una expresión
- `node --version` :: Versión instalada (en este PC: v26)
- `deno run archivo.ts` :: Deno ejecuta TypeScript sin configurar nada
- `bun run archivo.ts` :: Igual con Bun
- `F12 → Console` :: La consola del navegador, ideal para probar trozos

```js
// ¿Dónde estoy corriendo? Detectarlo sin romper en ningún entorno
const entorno =
  typeof window !== "undefined" ? "navegador" :
  typeof Deno !== "undefined"   ? "deno" :
  typeof Bun !== "undefined"    ? "bun" :
  typeof process !== "undefined" ? `node ${process.version}` : "desconocido";
console.log(entorno);              // en este PC → node v26.11.1
console.log(typeof globalThis);    // → object (globalThis existe en TODOS los entornos)
```

💡 Consejo: usa `globalThis` en vez de `window` (solo navegador) o `global` (solo Node) cuando escribas código que debe correr en cualquier sitio.

⚠️ Cuidado: que algo funcione en Chrome no significa que funcione en Safari. Antes de usar una API nueva, revisa su soporte (por ejemplo en MDN, sección "Browser compatibility").

## 🧬 Tipos y coerción: donde nacen las sorpresas

🧠 Concepto: **tipado dinámico** = la variable no tiene tipo; el **valor** sí. Una misma variable puede guardar un número y luego un texto. **Tipado débil** = JS convierte tipos **solo** cuando los mezclas (eso es la **coerción**).

JS tiene **7 primitivos** (valores simples e inmutables) y todo lo demás es **objeto** (arrays, funciones, fechas, Map...).

| Tipo | Ejemplo | `typeof` devuelve | Nota |
|---|---|---|---|
| `number` | `42`, `3.14`, `NaN` | `"number"` | Todos son decimales de 64 bits (IEEE 754) |
| `bigint` | `10n` | `"bigint"` | Enteros gigantes exactos |
| `string` | `"hola"` | `"string"` | Inmutable, UTF-16 |
| `boolean` | `true` | `"boolean"` | Solo true o false |
| `undefined` | `let x;` | `"undefined"` | "Todavía no tiene valor" |
| `null` | `null` | `"object"` ❗ | "Vacío a propósito"; bug histórico |
| `symbol` | `Symbol("id")` | `"symbol"` | Clave única, nunca choca |
| objeto | `{}`, `[]`, `fn` | `"object"` / `"function"` | Se pasan por referencia |

```js
console.log(typeof 42, typeof "hola", typeof true, typeof undefined, typeof null,
            typeof 10n, typeof Symbol("id"), typeof {}, typeof [], typeof function () {});
// → number string boolean undefined object bigint symbol object object function

console.log(0.1 + 0.2, 0.1 + 0.2 === 0.3);            // → 0.30000000000000004 false
console.log(Math.abs(0.1 + 0.2 - 0.3) < Number.EPSILON); // → true  (así se comparan decimales)
console.log(Number.MAX_SAFE_INTEGER);                  // → 9007199254740991
console.log(9007199254740992 + 1);                     // → 9007199254740992  (¡no suma!)
console.log(9007199254740992n + 1n);                   // → 9007199254740993n (BigInt sí)
```

::: desplegable 🤔 ¿Por qué 0.1 + 0.2 no da 0.3?
Los números se guardan en **binario** con 52 bits de mantisa (estándar IEEE 754, el mismo que usan Python, Java y C para `double`). En binario, 0.1 es periódico (como 1/3 = 0.333... en decimal), así que se guarda **redondeado**. Al sumar dos redondeos aparece el error en el último dígito.

- No es un bug de JS: en Python `0.1 + 0.2` también da `0.30000000000000004`.
- Para dinero: trabaja en **centavos enteros** (`1050` = Bs 10,50) o usa una librería decimal.
- Para mostrar: `(0.1 + 0.2).toFixed(2)` → `"0.30"` (devuelve **texto**).
:::

### 🔀 La tabla de sorpresas de `==` (todas comprobadas en Node)

`==` (igualdad **flexible**) convierte los tipos antes de comparar siguiendo un algoritmo largo. `===` (igualdad **estricta**) compara tipo y valor, sin convertir nada.

| Expresión | Resultado | Por qué |
|---|---|---|
| `1 == "1"` | `true` | El texto se convierte a número |
| `0 == ""` | `true` | `""` → 0 |
| `0 == "0"` | `true` | `"0"` → 0 |
| `"" == "0"` | `false` | Dos textos: se comparan como texto |
| `null == undefined` | `true` | Regla especial: solo son iguales entre sí |
| `null == 0` | `false` | null no se convierte en `==` |
| `null >= 0` | `true` | ¡Pero en `>=` sí se convierte a 0! |
| `[] == false` | `true` | `[]` → `""` → 0, y false → 0 |
| `[] == ![]` | `true` | `![]` es false (un array es truthy) |
| `NaN == NaN` | `false` | NaN no es igual a nada, ni a sí mismo |

```js
// Coerción con + (si hay un texto, concatena) y con - * / (siempre números)
console.log("5" + 3, "5" - 3, "5" * "2", true + 1);   // → 53 2 10 2
console.log([] + [], [] + {}, [1, 2] + [3]);           // → "" "[object Object]" "1,23"
console.log("b" + "a" + +"a" + "a");                   // → baNaNa  (+"a" es NaN)
console.log(3 > 2 > 1, 1 < 2 < 3);                     // → false true  (true > 1 → 1 > 1)
console.log("10" > "9", 10 > "9");                     // → false true  (texto vs número)
console.log(Math.max(), Math.min());                   // → -Infinity Infinity
```

### ✅ Truthy y falsy

🧠 Concepto: en un `if`, todo valor se convierte a booleano. Los **falsy** son solo 8: `false`, `0`, `-0`, `0n`, `""`, `null`, `undefined` y `NaN`. **Todo lo demás es truthy**, incluso `"0"`, `"false"`, `[]` y `{}`.

```js
console.log(Boolean(""), Boolean("0"), Boolean([]), Boolean({}));  // → false true true true
console.log(0 || "por defecto", 0 ?? "por defecto");                  // → por defecto 0
// || cae al valor por defecto con CUALQUIER falsy; ?? solo con null o undefined
const cantidad = 0;
console.log(cantidad || 10);   // → 10  ❌ perdiste el 0 que el usuario escribió
console.log(cantidad ?? 10);   // → 0   ✅
```

::: columnas
### ❌ Mal
```js
if (respuesta == null) {}      // ¿a propósito?
if (lista.length == "0") {}    // mezcla tipos
const total = precio || 10;    // pierde el 0
if (typeof x == "object") {}   // null también pasa
```
::: siguiente
### ✅ Bien
```js
if (respuesta === null) {}
if (lista.length === 0) {}
const total = precio ?? 10;
if (x !== null && typeof x === "object") {}
```
:::

### 🔧 Conversiones explícitas (las que deberías usar)

- `Number("42")` :: Texto → número (42); si no se puede, `NaN`
- `Number("")` :: ¡Ojo! da 0, no NaN
- `parseInt("8px", 10)` :: Lee dígitos del inicio → 8 (pasa siempre la base 10)
- `parseFloat("3.5kg")` :: Igual con decimales → 3.5
- `String(10)` :: Número → `"10"`
- `Boolean(valor)` :: A booleano (o `!!valor`)
- `Number.isNaN(x)` :: ¿Es NaN de verdad? (no uses el `isNaN` global)
- `Number.isInteger(5.0)` :: true; 5.0 y 5 son el mismo número
- `Object.is(NaN, NaN)` :: true; como `===` pero sin sus dos rarezas (NaN y -0)
- `Array.isArray(x)` :: La única forma fiable de saber si es array

```js
console.log(isNaN("hola"), Number.isNaN("hola"));     // → true false (el global convierte primero)
console.log([NaN].includes(NaN), [NaN].indexOf(NaN)); // → true -1 (indexOf usa ===)
console.log(Object.is(0, -0), 0 === -0);              // → false true
console.log(["1", "2", "3"].map(parseInt));           // → [ 1, NaN, NaN ] 😱 (ver errores famosos)
console.log(typeof typeof 1);                         // → string
```

💡 Consejo: regla de oro del equipo: **siempre `===` y `!==`**. La única excepción aceptada por muchas guías de estilo es `x == null`, que atrapa `null` y `undefined` a la vez. ESLint tiene la regla `eqeqeq` para obligarlo.

🇬🇧 **type coercion** /taip kouérshon/ = conversión implícita de tipos · **truthy / falsy** /trúzi, fólsi/ = "que cuenta como verdadero / falso" · **strict equality** /strikt ikuóliti/ = igualdad estricta · **floating point** /flóuting point/ = coma flotante

## 📦 var, let, const, scope y hoisting

🧠 Concepto: **scope** (ámbito) = la zona del código donde un nombre existe. JS tiene scope **global**, de **módulo**, de **función** y de **bloque** (`{ }`). El scope es **léxico**: se decide por **dónde está escrito** el código, no por desde dónde se llama.

| | `var` | `let` | `const` |
|---|---|---|---|
| Scope | Función | Bloque `{}` | Bloque `{}` |
| ¿Reasignar? | Sí | Sí | No |
| ¿Redeclarar? | Sí (peligroso) | No | No |
| Antes de declarar | `undefined` | ReferenceError (TDZ) | ReferenceError (TDZ) |
| Uso hoy | Evitar | Si el valor cambia | Por defecto |

```arbol
Scope global (o del módulo)
  const IVA = 0.13
  function calcularFactura()
    let total
    for (let i ...)  ← bloque
      const precio
    if (...)  ← bloque
      var descuento  ← ¡sube hasta la función!
```

Cuando usas una variable, el motor la busca en el scope actual; si no está, sube al de afuera, y así hasta el global. Esa escalera se llama **scope chain** (cadena de ámbitos). Nunca baja: el de afuera no ve lo de adentro.

### 🎈 Hoisting (elevación) y la TDZ

🧠 Concepto: **hoisting** = antes de ejecutar, el motor registra todas las declaraciones de cada scope. Las `function` quedan listas completas; las `var` quedan creadas con `undefined`; las `let/const/class` quedan creadas pero **sin inicializar**: tocarlas antes de su línea es la **TDZ (Temporal Dead Zone, zona muerta temporal)**.

```js
console.log(saludo);          // → undefined   (var se elevó, sin valor)
var saludo = "hola";

console.log(sumar(2, 3));     // → 5           (la declaración de función se eleva entera)
function sumar(a, b) { return a + b; }

try { console.log(edad); let edad = 20; }
catch (e) { console.log(e.name + ": " + e.message); }
// → ReferenceError: Cannot access 'edad' before initialization

try { restar(1, 1); var restar = (a, b) => a - b; }
catch (e) { console.log(e.name + ": " + e.message); }
// → TypeError: restar is not a function   (restar existe, pero vale undefined)
```

### 💥 El bug clásico: var dentro de un bucle con callbacks

```js
for (var i = 0; i < 3; i++) setTimeout(() => console.log("var i =", i), 0);
for (let j = 0; j < 3; j++) setTimeout(() => console.log("let j =", j), 0);
// → var i = 3   var i = 3   var i = 3     (UNA sola i compartida, ya vale 3)
// → let j = 0   let j = 1   let j = 2     (let crea una j NUEVA en cada vuelta)

if (true) { var a1 = "var se escapa"; let b1 = "let no"; }
console.log(a1, typeof b1);   // → var se escapa undefined
```

### 🔒 const no significa inmutable

```js
const usuario = { nombre: "Ana" };
usuario.nombre = "Luis";       // ✅ permitido: cambias el CONTENIDO del objeto
console.log(usuario);          // → { nombre: 'Luis' }
usuario = {};                  // ❌ TypeError: Assignment to constant variable.
```

📌 Resumen: `const` protege la **variable** (la flecha que apunta al valor), no el **valor**. Si quieres que el objeto no cambie, usa `Object.freeze` o, mejor, no lo mutes (sección de inmutabilidad).

✅ Bien: `const` por defecto; `let` solo cuando de verdad reasignas (contadores, acumuladores); `var` nunca en código nuevo.
⚠️ Cuidado: en un script clásico (no módulo), `var` en el nivel superior crea una propiedad de `window`. Un `var name` o `var status` puede pisar `window.name` o `window.status` sin que lo notes.
💡 Consejo: activa el **modo estricto** (`"use strict"`): los módulos ESM y las clases ya lo tienen siempre. En modo estricto, asignar a una variable no declarada lanza error en lugar de crear una global silenciosa.

## 🔐 Closures: funciones con memoria

🧠 Concepto: un **closure** (clausura) es una función **junto con las variables del scope donde fue creada**. Aunque la función de afuera ya terminó, la de adentro sigue pudiendo leer y modificar esas variables.

La intuición: cuando creas una función, JS le "pega una mochila" con referencias a las variables que ve a su alrededor. Donde vaya la función, va la mochila. No es una copia: es la **misma** variable viva.

```flujo
dir: abajo
crearContador() -> let cuenta = 0 : crea la variable
let cuenta = 0 -> return funciones : devuelve sumar y ver
return funciones -> crearContador terminó : su scope debería morir...
crearContador terminó -> cuenta sigue viva : ...pero sumar() la referencia
cuenta sigue viva -> c1.sumar() : lee y cambia la MISMA cuenta
```

```js
function crearContador() {
  let cuenta = 0;                         // privada: nadie de afuera puede tocarla
  return { sumar: () => ++cuenta, ver: () => cuenta };
}
const c1 = crearContador();
const c2 = crearContador();               // otra llamada = otra mochila independiente
c1.sumar(); c1.sumar(); c2.sumar();
console.log(c1.ver(), c2.ver(), c1.cuenta);   // → 2 1 undefined  (cuenta es privada)
```

### 🧰 Usos reales de los closures

| Patrón | Qué resuelve | Dónde lo ves |
|---|---|---|
| Fábricas de funciones | Configurar una vez, usar muchas | `crearMultiplicador(2)` |
| Datos privados | Encapsular estado | Módulos antes de `#privado` |
| Memoización | Cachear resultados caros | `useMemo`, librerías |
| Debounce / throttle | Limitar llamadas | Buscadores, scroll, resize |
| Callbacks y handlers | Recordar contexto | `addEventListener`, `setTimeout` |
| Hooks de React | Estado entre renders | `useState` usa closures |

```js
// 1) Fábrica de funciones
function crearMultiplicador(factor) { return n => n * factor; }
const doble = crearMultiplicador(2), triple = crearMultiplicador(3);
console.log(doble(5), triple(5));          // → 10 15

// 2) Memoización: la caché vive en el closure
function memo(fn) {
  const cache = new Map();
  return n => {
    if (cache.has(n)) return cache.get(n);
    const r = fn(n);
    cache.set(n, r);
    return r;
  };
}
let llamadas = 0;
const cuadradoLento = n => { llamadas++; return n * n; };
const cuadrado = memo(cuadradoLento);
cuadrado(9); cuadrado(9); cuadrado(9);
console.log("llamadas reales:", llamadas);  // → llamadas reales: 1

// 3) Debounce: solo ejecuta cuando el usuario DEJA de escribir
function debounce(fn, ms) {
  let temporizador;                          // vive en el closure entre llamadas
  return (...args) => {
    clearTimeout(temporizador);
    temporizador = setTimeout(() => fn(...args), ms);
  };
}
const buscar = debounce(q => console.log("buscando:", q), 50);
buscar("j"); buscar("ja"); buscar("jav"); buscar("java");
// → buscando: java   (una sola petición en lugar de cuatro)
```

⚠️ Cuidado: un closure mantiene viva **toda** variable que referencia. Si un handler que nunca se quita referencia un array enorme, ese array no se libera: es una de las fuentes clásicas de **memory leaks** (fugas de memoria).

💡 Consejo: si en una entrevista te piden "explica un closure", da el ejemplo del contador y menciona **debounce**: demuestra que lo entiendes y que sabes para qué sirve en la vida real.

## 🎯 this: depende de CÓMO llamas la función

🧠 Concepto: `this` es un parámetro **implícito** que recibe una función normal **en el momento de la llamada**. No importa dónde se escribió la función, sino **cómo se invoca**. Las funciones flecha son la excepción: **no tienen `this` propio**; usan el del scope donde fueron escritas.

| Cómo se llama | Qué vale `this` | Ejemplo |
|---|---|---|
| Como método `obj.f()` | El objeto antes del punto | `perro.ladrar()` → perro |
| Función suelta `f()` | `undefined` (estricto) o global | `const f = perro.ladrar; f()` |
| Con `new F()` | El objeto nuevo | `new Persona("Ana")` |
| `f.call(x)` / `f.apply(x)` | `x` | `ladrar.call(gato)` |
| `f.bind(x)` | `x` para siempre | `const g = f.bind(gato)` |
| Función flecha | El `this` de afuera (léxico) | dentro de un método |
| Handler del DOM (normal) | El elemento con el listener | `boton.addEventListener` |

```flujo
dir: abajo
¿Es flecha? -> this de afuera : sí
¿Es flecha? -> ¿Con new? : no
¿Con new? -> objeto nuevo : sí
¿Con new? -> ¿call/apply/bind? : no
¿call/apply/bind? -> el que pasaste : sí
¿call/apply/bind? -> ¿obj.metodo()? : no
¿obj.metodo()? -> obj : sí
¿obj.metodo()? -> undefined : no (estricto)
```

```js
"use strict";
const perro = {
  nombre: "Firulais",
  ladrar() { return `${this.nombre} dice guau`; },
  ladrarLuego() { return [1].map(() => this.nombre)[0]; },  // flecha: hereda this
};
console.log(perro.ladrar());                  // → Firulais dice guau

const suelta = perro.ladrar;                  // ¡perdiste el "perro." de adelante!
try { suelta(); } catch (e) { console.log(e.name + ": " + e.message); }
// → TypeError: Cannot read properties of undefined (reading 'nombre')

console.log(perro.ladrarLuego());             // → Firulais
const gato = { nombre: "Michi" };
console.log(perro.ladrar.call(gato));         // → Michi dice guau
const atada = perro.ladrar.bind(gato);
console.log(atada());                         // → Michi dice guau

class Boton {
  constructor(texto) {
    this.texto = texto;
    this.clicFlecha = () => this.texto;       // campo flecha: this fijado al crear
  }
  clic() { return this?.texto; }
}
const b = new Boton("Enviar");
const f1 = b.clic, f2 = b.clicFlecha;
console.log(f1(), f2());                      // → undefined Enviar
```

⚠️ Cuidado: el error más común con `this` es **pasar un método como callback**: `setTimeout(obj.metodo, 100)` o `boton.addEventListener("click", this.guardar)`. El método llega "suelto" y pierde su `this`. Soluciones: `() => obj.metodo()`, `.bind(obj)` o definirlo como campo flecha.

❌ Mal: usar una flecha como método de un objeto literal: `{ nombre: "x", saludar: () => this.nombre }`. Ahí `this` es el de afuera (el módulo), no el objeto.

## 🧩 Funciones: normales vs flecha

En JS las funciones son **valores de primera clase** (first-class): se guardan en variables, se pasan como argumento y se devuelven. Una función que recibe o devuelve otra función es una **función de orden superior** (higher-order function), como `map` o `debounce`.

::: columnas
### 🔧 Función normal
```js
function area(base, altura) {
  return base * altura;
}
const area2 = function (b, h) {
  return b * h;
};
```
- Tiene `this` dinámico y `arguments`.
- Se puede usar con `new`.
- La **declaración** se eleva (hoisting).
- Ideal para métodos y funciones con nombre.
::: siguiente
### ➡️ Función flecha (ES2015)
```js
const area = (base, altura) => base * altura;
const doble = n => n * 2;
const crear = () => ({ ok: true });
```
- `this` léxico (el de afuera), sin `arguments`.
- No se puede usar con `new`.
- No se eleva (es una variable).
- Ideal para callbacks cortos: `map`, `then`.
:::

```js
function normal() { return arguments.length; }
const flecha = (...args) => args.length;           // rest: la forma moderna
console.log(normal(1, 2, 3), flecha(1, 2, 3));      // → 3 3

const Flecha = () => {};
try { new Flecha(); } catch (e) { console.log(e.name + ": " + e.message); }
// → TypeError: Flecha is not a constructor

const objeto = () => ({ ok: true });                // paréntesis para devolver un objeto
const sinParentesis = () => { ok: true };           // ❌ eso es un BLOQUE con una etiqueta "ok:"
console.log(objeto(), sinParentesis());             // → { ok: true } undefined

const pot = (base, exp = 2) => base ** exp;         // parámetro por defecto
console.log(pot(3), pot(2, 10));                    // → 9 1024

const componer = (...fns) => x => fns.reduceRight((v, f) => f(v), x);
const limpiar = componer(s => s.toUpperCase(), s => s.trim());
console.log(limpiar("  hola  "));                   // → HOLA
```

### 🔁 Generadores e IIFE (los vas a ver en código ajeno)

```js
function* ids() { let i = 1; while (true) yield i++; }   // generador: pausa en cada yield
const gen = ids();
console.log(gen.next().value, gen.next().value);           // → 1 2
console.log([...ids().take(3)]);                           // → [ 1, 2, 3 ]  (iterator helpers, ES2025)

(function () { console.log("IIFE ejecutada al instante"); })();
// IIFE = función que se define y se llama a la vez; antes de los módulos se usaba para no ensuciar el global
```

- `function f(a, b = 1) {}` :: Parámetro por defecto
- `function f(...resto) {}` :: Rest: junta los argumentos sobrantes en un array
- `f(...lista)` :: Spread: reparte un array como argumentos
- `function f({ id, nombre }) {}` :: Desestructurar el objeto que te pasan
- `const f = async () => {}` :: Flecha asíncrona (devuelve promesa)
- `fn.length` :: Número de parámetros declarados (sin los que tienen valor por defecto)

💡 Consejo: una función = una tarea. Si su nombre necesita "y" (`validarYGuardarYEnviar`), divídela. Las funciones **puras** (misma entrada → misma salida, sin tocar nada externo) son las más fáciles de probar.

## 🏛️ Prototipos y clases

🧠 Concepto: en JS cada objeto tiene un enlace oculto a otro objeto, su **prototipo** (`[[Prototype]]`). Si buscas una propiedad que el objeto no tiene, JS la busca en su prototipo, luego en el prototipo del prototipo... hasta llegar a `null`. Eso es la **cadena de prototipos** (prototype chain). La herencia en JS es **delegación**, no copia.

```arbol
rex  (nombre: "Rex", #energia)
  Perro.prototype  (hablar)
    Animal.prototype  (comer, hablar, get energia)
      Object.prototype  (toString, hasOwnProperty...)
        null  ← fin de la cadena
```

`class` (ES2015) **no** añadió clases como las de Java: es una sintaxis más cómoda sobre los mismos prototipos. `typeof Animal` sigue siendo `"function"`.

```js
class Animal {
  #energia = 10;                 // campo privado (ES2022): ni se ve desde afuera
  static total = 0;              // propiedad de la clase, no de cada instancia
  constructor(nombre) { this.nombre = nombre; Animal.total++; }
  comer(n) { this.#energia += n; return this; }   // devolver this permite encadenar
  get energia() { return this.#energia; }          // getter: se lee como propiedad
  hablar() { return `${this.nombre} hace un ruido`; }
}
class Perro extends Animal {
  hablar() { return `${super.hablar()}... ¡guau!`; } // super = el método del padre
}

const rex = new Perro("Rex");
console.log(rex.hablar());                         // → Rex hace un ruido... ¡guau!
console.log(rex.comer(5).comer(2).energia);        // → 17
console.log(Animal.total);                         // → 1
console.log(Object.getPrototypeOf(rex) === Perro.prototype);              // → true
console.log(Object.getPrototypeOf(Perro.prototype) === Animal.prototype); // → true
console.log(rex instanceof Animal, typeof Animal);                        // → true function
console.log(Object.hasOwn(rex, "hablar"), "hablar" in rex);               // → false true
console.log(Object.getPrototypeOf(Object.prototype));                     // → null
```

```js
// Sin class: Object.create pone el prototipo a mano (así funciona por debajo)
const base = { saludar() { return "hola desde " + this.nombre; } };
const obj = Object.create(base);
obj.nombre = "obj";
console.log(obj.saludar(), Object.getPrototypeOf(obj) === base);  // → hola desde obj true
```

| Herramienta | Para qué |
|---|---|
| `class A extends B` | Herencia (un solo padre) |
| `#campo` | Privacidad real, verificada por el motor |
| `static` | Utilidades de la clase (`Date.now()`) |
| `get` / `set` | Propiedades calculadas o validadas |
| `Object.create(p)` | Objeto con prototipo `p` sin clase |
| `Object.hasOwn(o, k)` | ¿La propiedad es suya o heredada? |

⚠️ Cuidado: nunca modifiques los prototipos nativos (`Array.prototype.miMetodo = ...`). Se llama **monkey patching**: rompe código de otros y puede chocar con métodos futuros del estándar. Pasó de verdad: la librería MooTools añadió `Array.prototype.contains`, y por eso el método estándar tuvo que llamarse `includes` en vez de `contains`.
⚠️ Cuidado: la **prototype pollution** (contaminación de prototipos) es una vulnerabilidad real: si mezclas JSON del usuario en un objeto sin filtrar la clave `__proto__`, el atacante puede añadir propiedades a **todos** los objetos. Afectó a versiones antiguas de lodash (CVE-2019-10744). Usa `Object.create(null)` o `Map` para diccionarios con claves del usuario.
💡 Consejo: prefiere **composición** (objetos que contienen otros) sobre jerarquías profundas de herencia. En el frontend moderno (React) casi no verás `extends`.

## 📚 Arrays y sus métodos

🧠 Concepto: un **array** es una lista ordenada (índice desde 0) que puede crecer y mezclar tipos. Los métodos **funcionales** (`map`, `filter`, `reduce`...) reciben una función y la aplican a cada elemento: describes **qué** quieres, no **cómo** recorrer.

Todos los ejemplos de esta sección usan estos datos reales de un curso:

```js
const notas = [
  { alumno: "Ana",   materia: "Cálculo", nota: 85 },
  { alumno: "Luis",  materia: "Cálculo", nota: 42 },
  { alumno: "Ana",   materia: "Física",  nota: 91 },
  { alumno: "Sofía", materia: "Física",  nota: 67 },
  { alumno: "Luis",  materia: "Física",  nota: 55 },
];
```

### 🔀 map, filter y reduce en un esquema

```flujo
5 notas -> filter : nota >= 51
filter -> 4 aprobadas : descarta 1
4 aprobadas -> map : n => n.alumno
map -> 4 nombres : transforma cada una
5 notas -> reduce : (suma, n) => suma + n.nota
reduce -> 340 : un solo valor
```

| Método | Entra → sale | Pregunta que responde |
|---|---|---|
| `map(fn)` | n elementos → n elementos | "Transforma cada uno" |
| `filter(fn)` | n → entre 0 y n | "Quédate con los que cumplan" |
| `reduce(fn, inicial)` | n → 1 valor | "Acumula todo en uno" |
| `find(fn)` | n → 1 elemento o `undefined` | "Dame el primero que cumpla" |
| `some(fn)` / `every(fn)` | n → booleano | "¿Alguno? / ¿Todos?" |
| `flatMap(fn)` | n → m (aplana un nivel) | "Transforma y aplana" |

```js
console.log(notas.map(n => n.nota));                          // → [ 85, 42, 91, 67, 55 ]
console.log(notas.filter(n => n.nota >= 51).map(n => n.alumno)); // → [ 'Ana', 'Ana', 'Sofía', 'Luis' ]
console.log(notas.reduce((suma, n) => suma + n.nota, 0));     // → 340
console.log(notas.find(n => n.nota < 51));                    // → { alumno: 'Luis', materia: 'Cálculo', nota: 42 }
console.log(notas.findIndex(n => n.nota < 51));               // → 1
console.log(notas.some(n => n.nota > 90), notas.every(n => n.nota > 40)); // → true true

const promedio = notas.reduce((s, n) => s + n.nota, 0) / notas.length;
console.log(promedio);                                        // → 68

// reduce para AGRUPAR: el acumulador es un objeto
const porAlumno = notas.reduce((acc, n) => {
  (acc[n.alumno] ??= []).push(n.nota);   // ??= asigna solo si no existe
  return acc;                             // ⚠️ olvidar este return es el error nº 1 con reduce
}, {});
console.log(porAlumno);   // → { Ana: [ 85, 91 ], Luis: [ 42, 55 ], 'Sofía': [ 67 ] }

// Lo mismo, ya hecho (ES2024)
console.log(Object.groupBy(notas, n => n.materia).Física.length);   // → 3

// Ranking ordenado SIN mutar el original (ES2023)
console.log(notas.toSorted((a, b) => b.nota - a.nota).map(n => `${n.alumno}:${n.nota}`));
// → [ 'Ana:91', 'Ana:85', 'Sofía:67', 'Luis:55', 'Luis:42' ]
```

::: desplegable 🔬 Cómo trabaja reduce paso a paso
`notas.reduce((suma, n) => suma + n.nota, 0)`

| Vuelta | `suma` (acumulador) | `n.nota` | Devuelve |
|---|---|---|---|
| 1 | 0 (valor inicial) | 85 | 85 |
| 2 | 85 | 42 | 127 |
| 3 | 127 | 91 | 218 |
| 4 | 218 | 67 | 285 |
| 5 | 285 | 55 | 340 |

Lo que devuelves en una vuelta es el acumulador de la siguiente. Si no pasas el valor inicial, usa el primer elemento como inicial (y con un array vacío lanza `TypeError`): **pasa siempre el valor inicial**.
:::

### 🧨 Los que MUTAN vs los que devuelven uno nuevo

| Mutan el original ⚠️ | Versión que NO muta ✅ |
|---|---|
| `sort()` | `toSorted()` |
| `reverse()` | `toReversed()` |
| `splice(i, n)` | `toSpliced(i, n)` / `slice` + spread |
| `arr[i] = x` | `arr.with(i, x)` |
| `push`, `pop`, `shift`, `unshift` | `[...arr, x]`, `arr.slice(1)` |
| `fill`, `copyWithin` | `Array.from(...)` |

```js
const orig = [3, 1, 2];
console.log(orig.toSorted(), orig, orig.toReversed(), orig.with(0, 99), orig.at(-1));
// → [ 1, 2, 3 ] [ 3, 1, 2 ] [ 2, 1, 3 ] [ 99, 1, 2 ] 2     (orig sigue intacto)

console.log([10, 1, 2].sort());                 // → [ 1, 10, 2 ]  😱 ordena como TEXTO
console.log([10, 1, 2].sort((a, b) => a - b));  // → [ 1, 2, 10 ]  ✅ comparador numérico
console.log(["b", "a", "C", "á"].sort());       // → [ 'C', 'a', 'b', 'á' ]  (orden Unicode)
console.log(["b", "a", "C", "á"].sort((x, y) => x.localeCompare(y, "es"))); // → [ 'a', 'á', 'b', 'C' ]
```

### 📋 Chuleta de métodos (clic en la fila para copiar)

- `arr.at(-1)` :: Último elemento (índice negativo cuenta desde el final)
- `arr.includes(x)` :: ¿Está x? (sí detecta NaN)
- `arr.indexOf(x)` :: Posición o -1
- `arr.slice(1, 3)` :: Copia del índice 1 al 2 (no muta)
- `arr.join(", ")` :: Une en un texto
- `arr.flat(Infinity)` :: Aplana arrays anidados
- `arr.flatMap(s => s.split(" "))` :: map + flat de un nivel
- `Array.from({ length: 5 }, (_, i) => i * i)` :: Crea [0, 1, 4, 9, 16]
- `[..."hola"]` :: Texto → array de caracteres (respeta emojis)
- `new Array(3).fill(0)` :: [0, 0, 0]
- `Object.groupBy(arr, fn)` :: Agrupa en un objeto por clave
- `arr.entries()` :: Iterador de pares [índice, valor] para `for...of`

```js
console.log([[1, 2], [3, [4]]].flat(), [[1, 2], [3, [4]]].flat(Infinity)); // → [ 1, 2, 3, [ 4 ] ] [ 1, 2, 3, 4 ]
console.log(["hola mundo", "adiós"].flatMap(s => s.split(" ")));          // → [ 'hola', 'mundo', 'adiós' ]
console.log(Array.from({ length: 5 }, (_, i) => i * i));                  // → [ 0, 1, 4, 9, 16 ]
for (const [i, n] of notas.entries()) if (i < 2) console.log(i, n.alumno); // → 0 Ana / 1 Luis
```

💡 Consejo: encadenar `filter().map()` recorre el array dos veces; con 5 elementos no importa nada, con un millón quizá sí. Primero escribe claro; optimiza (un solo `reduce` o un `for`) solo si lo mediste.
⚠️ Cuidado: `forEach` no se puede cortar con `break` ni devuelve nada. Si necesitas parar, usa `for...of`, `some` o `find`.

## 🗂️ Objetos, desestructuración, spread e inmutabilidad

🧠 Concepto: un **objeto** es una colección de pares **clave → valor**. Las variables no guardan el objeto: guardan una **referencia** (una flecha) a él. Copiar la variable copia la flecha, no el objeto.

```js
const alumno = {
  nombre: "Ana", edad: 21,
  carrera: { nombre: "CC", semestre: 5 },
  materias: ["IA", "Redes"],
};

// Desestructuración: sacar propiedades a variables, con renombre y valor por defecto
const { nombre, edad: años, ciudad = "La Paz", carrera: { semestre } } = alumno;
console.log(nombre, años, ciudad, semestre);     // → Ana 21 La Paz 5

const [primera, ...resto] = alumno.materias;     // en arrays, por posición
console.log(primera, resto);                     // → IA [ 'Redes' ]

let x = 1, y = 2;
[x, y] = [y, x];                                 // intercambio sin variable temporal
console.log(x, y);                               // → 2 1

// En parámetros: "argumentos con nombre" y valores por defecto
function crearUsuario({ nombre, rol = "lector", activo = true } = {}) {
  return `${nombre} (${rol}, ${activo})`;
}
console.log(crearUsuario({ nombre: "Luis" }));   // → Luis (lector, true)
console.log(crearUsuario());                      // → undefined (lector, true)
```

### 🌊 Spread y rest: los tres puntos `...`

| Dónde | Nombre | Qué hace | Ejemplo |
|---|---|---|---|
| Al crear array | spread | Expande elementos | `[...a, ...b]` |
| Al crear objeto | spread | Copia propiedades | `{ ...obj, edad: 22 }` |
| Al llamar | spread | Array → argumentos | `Math.max(...nums)` |
| En parámetros | rest | Argumentos → array | `(...nums) => {}` |
| Al desestructurar | rest | Junta lo que sobra | `const { a, ...otros } = o` |

```js
console.log(Math.max(...[3, 9, 2]), [..."ab", ..."cd"]);   // → 9 [ 'a', 'b', 'c', 'd' ]
function sumarTodo(...n) { return n.reduce((a, b) => a + b, 0); }
console.log(sumarTodo(1, 2, 3, 4));                         // → 10

const clave = "color";
const prenda = { [clave]: "azul", ["talla" + 1]: "M" };     // claves calculadas
console.log(prenda);                                        // → { color: 'azul', talla1: 'M' }

console.log(alumno?.direccion?.calle);                      // → undefined (sin explotar)
console.log(alumno.direccion?.calle ?? "sin calle");        // → sin calle
```

- `Object.keys(o)` :: Array de claves
- `Object.values(o)` :: Array de valores
- `Object.entries(o)` :: Array de pares [clave, valor]
- `Object.fromEntries(pares)` :: Pares → objeto (inverso de entries)
- `"clave" in o` :: ¿Existe (propia o heredada)?
- `Object.hasOwn(o, "clave")` :: ¿Es propia?
- `delete o.clave` :: Borra una propiedad (muta)
- `structuredClone(o)` :: Copia profunda real (fechas, Map, Set incluidos)

### 🧊 Copia superficial vs profunda

```arbol
alumno
  nombre: "Ana"  ← primitivo: se copia el valor
  carrera → { semestre }  ← objeto: se copia SOLO la flecha
  materias → [IA, Redes]  ← array: se copia SOLO la flecha
copia = { ...alumno }
  nombre: "Ana"  (independiente)
  carrera → MISMO objeto que alumno.carrera
  materias → MISMO array que alumno.materias
```

```js
const copia = { ...alumno, edad: 22 };      // copia SUPERFICIAL (un nivel)
copia.carrera.semestre = 6;                 // ❌ cambia también alumno.carrera
copia.materias.push("BD");                  // ❌ cambia también alumno.materias
console.log(alumno.edad, alumno.carrera.semestre, alumno.materias);
// → 21 6 [ 'IA', 'Redes', 'BD' ]           (edad se salvó, lo anidado no)

const profunda = structuredClone(alumno);   // copia PROFUNDA
profunda.carrera.semestre = 9;
console.log(alumno.carrera.semestre);       // → 6  ✅ el original no se tocó

const congelado = Object.freeze({ nivel: 1, datos: { puntos: 0 } });
congelado.nivel = 99;                       // se ignora en silencio (TypeError en modo estricto)
congelado.datos.puntos = 50;                // ⚠️ freeze también es superficial
console.log(congelado);                     // → { nivel: 1, datos: { puntos: 50 } }

console.log([1, 2, 3] === [1, 2, 3], { a: 1 } == { a: 1 });  // → false false (referencias distintas)
```

🧠 Concepto: **inmutabilidad** = en lugar de cambiar un dato, creas uno nuevo con el cambio. Así nadie que tenga una referencia al viejo se lleva sorpresas, y comparar "¿cambió?" es tan barato como `viejo !== nuevo`. Es la base de cómo React, Redux y Angular detectan cambios.

::: columnas
### ❌ Mutando
```js
function marcarHecha(tareas, id) {
  const t = tareas.find(t => t.id === id);
  t.hecha = true;        // cambia el original
  return tareas;         // misma referencia:
}                        // React NO re-renderiza
```
::: siguiente
### ✅ Inmutable
```js
function marcarHecha(tareas, id) {
  return tareas.map(t =>
    t.id === id ? { ...t, hecha: true } : t
  );                     // array nuevo, objeto nuevo
}                        // solo lo cambiado es nuevo
```
:::

### 🧺 Map y Set: cuándo no usar un objeto

| Necesitas | Usa | Por qué |
|---|---|---|
| Diccionario con claves de usuario | `Map` | Sin `__proto__` ni claves heredadas |
| Claves que no son texto (objetos) | `Map` | Un objeto convierte la clave en string |
| Saber el tamaño | `Map` / `Set` | `.size` directo |
| Valores únicos | `Set` | Elimina duplicados |
| Buscar "¿está?" muchas veces | `Set` | `has` es O(1), `includes` es O(n) |
| Datos fijos tipo registro / JSON | Objeto `{}` | Sintaxis simple, serializable |

```js
const m = new Map([["ana", 1]]);
m.set({ id: 1 }, "un objeto como clave");
console.log(m.size, new Set([1, 1, 2, 3, 3]).size, [...new Set("banana")].join("")); // → 2 3 ban
const a = new Set(["js", "py"]), b = new Set(["py", "go"]);
console.log([...a.union(b)], [...a.intersection(b)]);   // → [ 'js', 'py', 'go' ] [ 'py' ]  (ES2025)
```

💡 Consejo: `WeakMap` y `WeakSet` guardan objetos **sin impedir que el recolector de basura los borre**. Úsalos para asociar datos extra a objetos que no controlas (por ejemplo, a elementos del DOM) sin crear fugas de memoria.

## 🔄 El event loop: cómo un solo hilo hace mil cosas

🧠 Concepto: JS ejecuta tu código en **un solo hilo** con una **call stack** (pila de llamadas). Las tareas lentas (red, timers, disco) las hace el **entorno** (navegador o libuv en Node) en paralelo. Cuando terminan, dejan su callback en una **cola**, y el **event loop** lo pasa a la pila **solo cuando la pila está vacía**.

```flujo
dir: abajo
Call stack -> APIs del entorno : setTimeout, fetch, eventos
APIs del entorno -> Cola de macrotareas : timer listo, clic, mensaje
Call stack -> Cola de microtareas : then, await, queueMicrotask
Cola de microtareas -> Event loop : 1º TODAS las microtareas
Cola de macrotareas -> Event loop : 2º UNA macrotarea
Event loop -> Call stack : solo si la pila está vacía
```

El algoritmo de cada vuelta, simplificado:

1. Ejecuta el código síncrono hasta que la **pila quede vacía**.
2. Vacía la **cola de microtareas completa** (promesas, `await`, `queueMicrotask`). Si una microtarea crea otra, también se ejecuta en esta misma ronda.
3. (Navegador) Si toca, **pinta** la pantalla (estilos, layout, `requestAnimationFrame`).
4. Toma **una sola macrotarea** (un `setTimeout`, un clic, un mensaje) y vuelve al paso 1.

| Cola | Qué entra | Prioridad |
|---|---|---|
| Microtareas | `.then/.catch/.finally`, continuación tras `await`, `queueMicrotask`, `MutationObserver` | Se vacía entera tras cada tarea |
| Macrotareas (tasks) | `setTimeout`, `setInterval`, eventos del DOM, I/O, `MessageChannel` | Una por vuelta |
| Render (navegador) | `requestAnimationFrame`, layout, pintado | Unas 60 veces por segundo si hay cambios |

### ✅ Ejemplo comprobado: ¿en qué orden sale?

```js
// loop.mjs  →  node loop.mjs   (salida REAL copiada de la terminal)
console.log("1. script: inicio");
setTimeout(() => console.log("8. macrotarea: setTimeout 0"), 0);
Promise.resolve()
  .then(() => console.log("4. micro: then #1"))
  .then(() => console.log("7. micro: then #2 (encadenado)"));
queueMicrotask(() => console.log("5. micro: queueMicrotask"));
(async () => {
  console.log("2. async: corre síncrono hasta el await");
  await null;
  console.log("6. async: continúa tras el await");
})();
console.log("3. script: fin");
```

```text
1. script: inicio
2. async: corre síncrono hasta el await
3. script: fin
4. micro: then #1
5. micro: queueMicrotask
6. async: continúa tras el await
7. micro: then #2 (encadenado)
8. macrotarea: setTimeout 0
```

```secuencia
actores: Pila, Microtareas, Macrotareas
Pila -> Macrotareas : setTimeout(8)
Pila -> Microtareas : then #1 (4), queueMicrotask (5)
Pila -> Microtareas : await null → continuación (6)
nota Pila : imprime 1, 2, 3 y queda vacía
Microtareas -> Pila : 4 · al terminar encola then #2 (7)
Microtareas -> Pila : 5, 6, 7 (se vacía TODA la cola)
Macrotareas -> Pila : 8 · por fin el timeout
```

::: desplegable 🤔 ¿Por qué "7" sale después de "5" y "6"?
El segundo `.then` no se encola al principio: se encola **cuando termina el primero**. En ese momento la cola ya tenía `queueMicrotask` (5) y la continuación del `await` (6), así que el 7 va detrás. Las microtareas se atienden en orden FIFO (first in, first out: la primera que entra es la primera que sale).
:::

### 🧱 Bloquear el hilo congela todo

```js
const t0 = Date.now();
setTimeout(() => console.log(`timeout de 0 ms llegó a los ${Date.now() - t0 >= 200 ? "≥200" : "<200"} ms`), 0);
while (Date.now() - t0 < 200) {}     // bucle síncrono de 200 ms: nadie más puede correr
console.log("bucle terminado");
// → bucle terminado
// → timeout de 0 ms llegó a los ≥200 ms
```

⚠️ Cuidado: `setTimeout(fn, 0)` no significa "ahora": significa "en cuanto la pila esté libre y no queden microtareas". Y el tiempo es un **mínimo**, no una promesa exacta.
⚠️ Cuidado: un cálculo pesado (procesar una imagen, un JSON de 100 MB, un bucle enorme) en el hilo principal **congela la página**: no hay clics, ni scroll, ni animaciones. En Node, congela **todas** las peticiones del servidor a la vez. Solución: **Web Workers** (navegador) o **worker_threads** (Node), o partir el trabajo en trozos.
💡 Consejo: en DevTools → **Performance**, las "Long tasks" (tareas de más de 50 ms) se marcan en rojo: son las que hacen que la página se sienta lenta.

🇬🇧 **call stack** /kol stak/ = pila de llamadas · **queue** /kiú/ = cola · **microtask** /máikrou-task/ = microtarea · **blocking** /blóking/ = que bloquea · **non-blocking I/O** /non-blóking ai-óu/ = entrada/salida que no bloquea

## ⏳ Callbacks → promesas → async/await

La asincronía en JS evolucionó en tres pasos, cada uno para arreglar el dolor del anterior:

```tiempo
Callbacks (1995→) : "llámame cuando termines"; anidar = callback hell
Promesas (ES2015) : un objeto que representa un valor futuro; se encadena con then
async/await (ES2017) : código asíncrono que se lee de arriba abajo, con try/catch
```

🧠 Concepto: una **promesa** (Promise) es un objeto que representa un resultado que **todavía no existe**. Está en uno de tres estados y, una vez decidida (settled), **nunca cambia**.

```flujo
pending -> fulfilled : resolve(valor) → corre .then
pending -> rejected : reject(error) → corre .catch
fulfilled -> finally : siempre
rejected -> finally : siempre
```

```js
const esperar = (ms, valor, falla = false) =>
  new Promise((res, rej) => setTimeout(() => (falla ? rej(new Error(valor)) : res(valor)), ms));

// 1) Callback al estilo Node: (error, resultado)
function leerUsuarioCb(id, cb) {
  setTimeout(() => (id > 0 ? cb(null, { id, nombre: "Ana" }) : cb(new Error("id inválido"))), 10);
}
leerUsuarioCb(1, (err, u) => {
  if (err) return console.log("cb error:", err.message);
  console.log("callback:", u.nombre);                     // → callback: Ana
});

// 2) "Promesificar" un callback y encadenar
const leerUsuario = id =>
  new Promise((res, rej) => leerUsuarioCb(id, (e, u) => (e ? rej(e) : res(u))));
leerUsuario(1)
  .then(u => u.nombre.toUpperCase())    // lo que devuelves pasa al siguiente then
  .then(n => console.log("then:", n))   // → then: ANA
  .catch(e => console.log(e.message));  // un catch atrapa errores de TODA la cadena

// 3) async/await
async function demo() {
  try { await leerUsuario(-1); }
  catch (e) { console.log("catch:", e.message); }         // → catch: id inválido
}
demo();
```

::: columnas
### 😵 Callback hell
```js
leerUsuario(id, (e, u) => {
  leerPedidos(u, (e, p) => {
    leerFactura(p[0], (e, f) => {
      enviar(f, (e) => {
        // ...y el manejo de
        // errores repetido 4 veces
      });
    });
  });
});
```
::: siguiente
### 😌 async/await
```js
async function procesar(id) {
  const u = await leerUsuario(id);
  const p = await leerPedidos(u);
  const f = await leerFactura(p[0]);
  await enviar(f);
}
// un solo try/catch para todo
```
:::

### ⚡ Secuencial vs paralelo (medido en este PC)

```js
let t = performance.now();
await esperar(100, "a");
await esperar(100, "b");                       // espera a que termine el anterior
console.log("secuencial ~", Math.round((performance.now() - t) / 100) * 100, "ms"); // → ~ 200 ms

t = performance.now();
await Promise.all([esperar(100, "a"), esperar(100, "b")]);  // ambas arrancan a la vez
console.log("paralelo   ~", Math.round((performance.now() - t) / 100) * 100, "ms"); // → ~ 100 ms
```

```grafica
tipo: barras
titulo: Dos esperas de 100 ms (medido en este PC con Node 26)
unidad: ms
await uno tras otro : 200
Promise.all : 100
```

| Combinador | Se resuelve cuando... | Falla cuando... | Úsalo para |
|---|---|---|---|
| `Promise.all` | Todas cumplen | UNA falla (la primera) | Datos que necesitas todos |
| `Promise.allSettled` | Todas terminan | Nunca | Lotes donde algunas pueden fallar |
| `Promise.race` | La primera termina | La primera falla | Timeouts |
| `Promise.any` | La primera cumple | Todas fallan | Servidores espejo, el más rápido |

```js
const r = await Promise.allSettled([esperar(10, "ok"), esperar(10, "caído", true)]);
console.log(r.map(x => x.status));                                  // → [ 'fulfilled', 'rejected' ]
console.log(await Promise.race([esperar(50, "lento"), esperar(5, "rápido")]));         // → rápido
console.log(await Promise.any([esperar(5, "falla", true), esperar(20, "primera buena")])); // → primera buena

const { promise, resolve } = Promise.withResolvers();   // ES2024
setTimeout(() => resolve("listo"), 5);
console.log("withResolvers:", await promise);           // → withResolvers: listo
```

### 🪤 Las trampas de async

```js
const ids = [1, 2, 3], vistos = [];
ids.forEach(async id => { await esperar(10); vistos.push(id); });
console.log("después de forEach:", vistos);   // → después de forEach: []   ❌ forEach NO espera

for (const id of ids) { await esperar(1); }   // ✅ for...of sí espera (en serie)
await Promise.all(ids.map(id => esperar(1, id)));  // ✅ o todas en paralelo
```

⚠️ Cuidado: olvidar `await` te deja una promesa en vez del valor: `if (await existeUsuario())` funciona, `if (existeUsuario())` es **siempre verdadero** porque una promesa es un objeto (truthy).
⚠️ Cuidado: una promesa rechazada sin `.catch` ni `try` produce un **unhandledRejection**. En Node moderno eso **termina el proceso** (por defecto desde Node 15). En el navegador solo sale un error rojo en la consola, y el bug pasa desapercibido.
⚠️ Cuidado: `await` en un `for` con peticiones **independientes** las hace una tras otra. 20 peticiones de 300 ms = 6 segundos; con `Promise.all` ≈ 300 ms. Pero si son miles, limita la concurrencia (lotes de 5–10) para no tumbar el servidor.
💡 Consejo: una función `async` **siempre** devuelve una promesa, aunque hagas `return 5`. Y `await` también se puede usar directamente en el nivel superior de un **módulo** (top-level await).

## 🚨 Manejo de errores

🧠 Concepto: un **error** es un objeto (instancia de `Error`) con `name`, `message` y `stack` (la pila de llamadas donde ocurrió). Con `throw` lo lanzas; sube por la pila hasta que un `try/catch` lo atrapa. Si nadie lo atrapa, el programa (o esa tarea del event loop) se detiene.

| Tipo | Cuándo aparece | Ejemplo real |
|---|---|---|
| `TypeError` | Operación sobre el tipo equivocado | `null.nombre`, llamar algo que no es función |
| `ReferenceError` | Variable que no existe o en TDZ | `noExiste()` |
| `SyntaxError` | Código o JSON mal escrito | `JSON.parse("{mal}")` |
| `RangeError` | Valor fuera de rango | `new Array(-1)`, recursión infinita |
| `AggregateError` | Varios errores juntos | `Promise.any` cuando todas fallan |
| Los tuyos | Reglas de negocio | `ErrorValidacion` |

```js
class ErrorValidacion extends Error {
  constructor(campo, mensaje) {
    super(mensaje);
    this.name = "ErrorValidacion";   // aparece en el stack y en los logs
    this.campo = campo;
  }
}
function registrar({ correo, edad }) {
  if (!correo?.includes("@")) throw new ErrorValidacion("correo", "Correo inválido");
  if (edad < 18) throw new ErrorValidacion("edad", "Debe ser mayor de edad");
  return "Registrado ✅";
}
for (const datos of [{ correo: "ana@umsa.bo", edad: 20 }, { correo: "ana", edad: 20 }, { correo: "a@b.c", edad: 15 }]) {
  try {
    console.log(registrar(datos));
  } catch (e) {
    if (e instanceof ErrorValidacion) console.log(`❌ ${e.campo}: ${e.message}`);
    else throw e;                     // ✅ lo que no sabes manejar, relánzalo
  }
}
// → Registrado ✅
// → ❌ correo: Correo inválido
// → ❌ edad: Debe ser mayor de edad

try { null.nombre } catch (e) { console.log(e.name, "|", e.message); }
// → TypeError | Cannot read properties of null (reading 'nombre')
try { new Array(-1) } catch (e) { console.log(e.name, "|", e.message); }
// → RangeError | Invalid array length

// cause (ES2022): envolver un error sin perder el original
try { throw new Error("Fallo al guardar", { cause: new Error("disco lleno") }); }
catch (e) { console.log(e.message, "← causa:", e.cause.message); }  // → Fallo al guardar ← causa: disco lleno

function siempre() { try { return "try"; } finally { console.log("finally corre igual"); } }
console.log(siempre());   // → finally corre igual / try
```

```flujo
dir: abajo
throw en guardar() -> ¿try en guardar? : sube
¿try en guardar? -> catch local : sí
¿try en guardar? -> ¿try en quien llamó? : no, sigue subiendo
¿try en quien llamó? -> catch de arriba : sí
¿try en quien llamó? -> Error no capturado : nadie lo atrapa
```

::: columnas
### ❌ Tragarse el error
```js
try {
  await guardarPago(pago);
} catch (e) {
  // nada... el usuario cree que pagó
}
```
::: siguiente
### ✅ Manejarlo o propagarlo
```js
try {
  await guardarPago(pago);
} catch (e) {
  registrarError(e);          // log/Sentry
  mostrarAviso("No se pudo pagar, reintenta");
  throw e;                    // o relanza
}
```
:::

✅ Bien: lanza siempre objetos `Error` (o subclases), nunca textos: `throw "falló"` no tiene `stack` y no sabrás de dónde vino.
💡 Consejo: en producción, usa un servicio de monitoreo (Sentry y similares) y escucha `window.addEventListener("error")` / `"unhandledrejection"` en el navegador, o `process.on("unhandledRejection")` en Node, para enterarte de los errores que nadie atrapó.

## 📤 Módulos: ESM vs CommonJS

🧠 Concepto: un **módulo** es un archivo con su propio scope: lo que declares adentro es privado salvo lo que **exportes**. Resolvió el problema de los años 2000, cuando todos los `<script>` compartían un único scope global y se pisaban las variables.

JS tuvo dos sistemas de módulos: **CommonJS** (CJS), que Node inventó en 2009 porque el lenguaje no tenía ninguno, y **ES Modules** (ESM), el estándar oficial desde ES2015, que funciona en navegadores y en Node.

::: columnas
### 📦 ESM (estándar)
```js
// matematica.js
export const PI = 3.1416;
export function areaCirculo(r) {
  return PI * r ** 2;
}
export default function saludar(n) {
  return `Hola, ${n}`;
}

// main.js
import saludar, { areaCirculo, PI as pi }
  from "./matematica.js";
```
::: siguiente
### 🟩 CommonJS (Node clásico)
```js
// matematica.js
const PI = 3.1416;
function areaCirculo(r) {
  return PI * r ** 2;
}
module.exports = { PI, areaCirculo };

// main.js
const { areaCirculo } =
  require("./matematica.js");
```
:::

```js
// main.js en una carpeta con package.json → { "type": "module" }
import saludar, { areaCirculo, PI as pi } from "./matematica.js";
console.log(saludar("Ana"), areaCirculo(2).toFixed(2), pi, typeof require);
// → Hola, Ana 12.57 3.1416 undefined      (en ESM no existe require)
const { default: s2 } = await import("./matematica.js");   // import dinámico: carga bajo demanda
console.log(s2 === saludar);                                // → true (el módulo se carga una sola vez)
```

| Aspecto | ESM | CommonJS |
|---|---|---|
| Sintaxis | `import` / `export` | `require` / `module.exports` |
| Cuándo se resuelve | Antes de ejecutar (estático) | Al ejecutar la línea (dinámico) |
| Tree shaking | Sí: el bundler borra lo no usado | Difícil |
| `await` arriba del todo | Sí | No |
| Navegador | Nativo (`<script type="module">`) | No (necesita bundler) |
| Variables especiales | `import.meta.url`, `import.meta.dirname` | `__dirname`, `__filename` |
| Cómo lo activa Node | `.mjs` o `"type": "module"` | `.cjs` o por defecto |

```flujo
main.js -> import "./api.js" : grafo estático
main.js -> import "./ui.js"
ui.js -> import "./api.js" : se carga UNA vez
api.js -> import "zod" : node_modules
```

✅ Bien: en proyectos nuevos, **ESM siempre** (`"type": "module"` en `package.json`). Todo el ecosistema moderno (Vite, Deno, Bun, los navegadores) va por ahí.
⚠️ Cuidado: en ESM las rutas relativas llevan **extensión** (`"./util.js"`, no `"./util"`). Y `__dirname` no existe: usa `import.meta.dirname` (Node 20.11+).
💡 Consejo: prefiere **exports con nombre** sobre `export default`: el editor autocompleta mejor, los renombres se detectan y todos importan con el mismo nombre.

## 🖱️ DOM y eventos

🧠 Concepto: el **DOM** (Document Object Model) es el árbol de objetos que el navegador construye a partir del HTML. JS no edita el archivo HTML: edita ese árbol, y el navegador repinta lo que cambió.

```arbol
document
  html
    head
      title
    body
      div#tabla
        ul#lista
          li
            button[data-id=7]
```

- `document.querySelector("#lista")` :: El primero que coincide con el selector CSS (o null)
- `document.querySelectorAll("li")` :: Todos (NodeList estática; no es un array)
- `el.textContent = "Hola"` :: Pone texto (seguro: no interpreta HTML)
- `el.innerHTML = "<b>Hola</b>"` :: Pone HTML (peligroso con datos del usuario)
- `el.classList.toggle("activo")` :: Añade/quita una clase CSS
- `el.dataset.id` :: Lee el atributo `data-id`
- `el.closest("li")` :: El ancestro más cercano que coincide (o él mismo)
- `document.createElement("li")` :: Crea un elemento nuevo
- `padre.append(hijo)` :: Lo inserta al final
- `el.remove()` :: Lo quita del DOM
- `el.addEventListener("click", fn)` :: Escucha un evento
- `e.preventDefault()` :: Cancela la acción por defecto (enviar formulario, seguir link)
- `e.stopPropagation()` :: Detiene la propagación (úsalo poco)

### 🫧 Capturing, target y bubbling

Cuando haces clic en un botón, el evento no ocurre solo en el botón: **baja** desde `document` hasta el botón (fase de **captura**), llega al **objetivo** (target) y luego **sube** de vuelta hasta `document` (fase de **burbuja**, bubbling). Por defecto, `addEventListener` escucha en la burbuja.

```flujo
dir: abajo
document -> div#tabla : 1 captura ↓
div#tabla -> ul#lista : 1 captura ↓
ul#lista -> button : 2 target
button --> ul#lista : 3 burbuja ↑
ul#lista --> div#tabla : 3 burbuja ↑
```

```js
// Comprobado con jsdom (el mismo DOM que usa Jest/Vitest para tests)
tabla.addEventListener("click", () => log.push("div captura"), { capture: true });
lista.addEventListener("click", () => log.push("ul captura"), true);
btn.addEventListener("click", () => log.push("button (target)"));
lista.addEventListener("click", () => log.push("ul burbuja"));
tabla.addEventListener("click", () => log.push("div burbuja"));
btn.click();
console.log(log.join(" → "));
// → div captura → ul captura → button (target) → ul burbuja → div burbuja
```

### 🎯 Delegación de eventos

🧠 Concepto: **delegación** = en vez de poner un listener en cada uno de los 500 botones, pones **uno solo** en el contenedor y, gracias al bubbling, preguntas `e.target` quién fue. Funciona incluso con elementos que se agregan **después**.

```js
lista.addEventListener("click", e => {
  const boton = e.target.closest("button[data-id]");   // closest: por si hizo clic en un <span> dentro
  if (!boton) return;                                   // clic en otra parte de la lista
  borrarTarea(boton.dataset.id);
});
// Un <li> creado DESPUÉS también funciona, sin añadirle nada:
const li = document.createElement("li");
li.innerHTML = '<button data-id="8">Borrar</button>';
lista.append(li);
li.querySelector("button").click();     // → borrarTarea("8")  (comprobado con jsdom)
```

::: columnas
### ❌ Un listener por elemento
```js
document.querySelectorAll(".borrar")
  .forEach(b =>
    b.addEventListener("click", borrar));
// 500 listeners, y los botones
// nuevos NO funcionan
```
::: siguiente
### ✅ Delegación
```js
lista.addEventListener("click", e => {
  if (e.target.matches(".borrar"))
    borrar(e);
});
// 1 listener, sirve para los
// botones de ahora y del futuro
```
:::

### 🛡️ XSS: el agujero más famoso del frontend

🧠 Concepto: **XSS (Cross-Site Scripting)** = un atacante logra que tu página ejecute **su** JS, normalmente metiendo HTML con código en un campo de texto (comentario, nombre) que luego tú pintas con `innerHTML`. Con eso puede robar sesiones o actuar como el usuario.

```js
const comentario = '<img src=x onerror="alert(1)">';   // lo escribió un usuario malicioso
p.innerHTML = comentario;     // ❌ el navegador crea la imagen, falla y EJECUTA onerror
p.textContent = comentario;   // ✅ se muestra como texto literal
console.log(p.innerHTML);     // → &lt;img src=x onerror="alert(1)"&gt;   (escapado)
```

⚠️ Cuidado: el caso real más famoso es el **gusano Samy** de MySpace (2005): un XSS almacenado en un perfil que se copiaba a cada visitante; se dice que en unas 20 horas superó el millón de perfiles. React, Vue y Angular escapan el texto por defecto; los peligros vuelven cuando usas `dangerouslySetInnerHTML` o `v-html`.
💡 Consejo: si de verdad necesitas HTML del usuario (un editor de texto enriquecido), sanéalo con una librería como **DOMPurify** y configura una **Content Security Policy (CSP)** en el servidor.

## 🌐 fetch y JSON

🧠 Concepto: **fetch** es la API estándar para hacer peticiones HTTP. Devuelve una promesa con un objeto `Response`. **JSON** (JavaScript Object Notation) es el formato de texto con el que viajan los datos entre frontend y backend.

```secuencia
actores: Tu código, Navegador, API
Tu código -> Navegador : fetch("/api/notas")
Navegador -> API : GET /api/notas
API --> Navegador : 200 OK + cuerpo JSON
Navegador --> Tu código : Response (cabeceras listas)
Tu código -> Navegador : await res.json()
Navegador --> Tu código : objeto JS ya parseado
```

```js
async function obtenerNotas(alumnoId, { signal } = {}) {
  const res = await fetch(`https://api.ejemplo.edu/alumnos/${alumnoId}/notas`, {
    headers: { Accept: "application/json" },
    signal,                                     // permite cancelar la petición
  });
  if (!res.ok) {                                // ⚠️ fetch NO lanza error con 404 o 500
    throw new Error(`HTTP ${res.status} al pedir notas`);
  }
  return res.json();                            // también es una promesa
}

async function crearTarea(tarea) {
  const res = await fetch("https://api.ejemplo.edu/tareas", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(tarea),                // objeto → texto
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

// Timeout: cancelar si tarda más de 5 s
try {
  const notas = await obtenerNotas(7, { signal: AbortSignal.timeout(5000) });
  console.log(notas);
} catch (e) {
  console.log(e.name === "TimeoutError" ? "El servidor tardó demasiado" : e.message);
}
```

| Situación | ¿fetch rechaza? | Qué hacer |
|---|---|---|
| Sin internet / DNS falla | Sí (`TypeError`) | `catch` y mensaje "sin conexión" |
| 404, 500, 401 | **No** | Revisar `res.ok` / `res.status` |
| Timeout con `AbortSignal` | Sí (`TimeoutError`) | Reintentar o avisar |
| Bloqueado por CORS | Sí (`TypeError`) | Configurar el **servidor** |
| JSON inválido | `res.json()` rechaza | `SyntaxError` en el catch |

🧠 Concepto: **CORS** (Cross-Origin Resource Sharing) = el navegador bloquea que una página de `misitio.com` lea respuestas de `otraapi.com` salvo que esa API diga explícitamente que lo permite (cabecera `Access-Control-Allow-Origin`). Se arregla **en el servidor**, nunca en el frontend.

### 🧾 JSON: lo que sí y lo que no

```js
console.log(JSON.stringify({ a: 1, f: () => 1, u: undefined, d: new Date(0), n: NaN }));
// → {"a":1,"d":"1970-01-01T00:00:00.000Z","n":null}
//   las funciones y undefined DESAPARECEN, Date se vuelve texto, NaN se vuelve null

console.log(JSON.stringify({ a: [1, 2] }, null, 2));   // tercer argumento = sangría bonita

try { JSON.parse("{nota: 85}"); } catch (e) { console.log(e.name); }  // → SyntaxError (claves sin comillas)

const ciclo = {}; ciclo.yo = ciclo;
try { JSON.stringify(ciclo); } catch (e) { console.log(e.message.split("\n")[0]); }
// → Converting circular structure to JSON

// reviver: reconstruir fechas al leer
const datos = JSON.parse('{"fecha":"2026-10-19T00:00:00.000Z"}',
  (k, v) => (k === "fecha" ? new Date(v) : v));
console.log(datos.fecha instanceof Date);              // → true
```

💡 Consejo: nunca confíes en la forma del JSON que llega de una API: valídalo (con **Zod** o similar) en el borde de tu app. Un campo que de pronto viene `null` es la causa de miles de `Cannot read properties of null`.

## 💾 Almacenamiento en el navegador

| Opción | Capacidad aprox. | ¿Viaja al servidor? | API | Úsalo para |
|---|---|---|---|---|
| `localStorage` | ~5 MB por origen | No | Síncrona, solo texto | Preferencias, tema, borradores |
| `sessionStorage` | ~5 MB | No | Síncrona, solo texto | Datos de esta pestaña |
| Cookies | ~4 KB c/u | **Sí, en cada petición** | `document.cookie` / servidor | Sesión (con `HttpOnly`) |
| IndexedDB | Cientos de MB o más | No | Asíncrona, objetos | Apps offline, caché grande |
| Cache API | Grande | No | Asíncrona | Respuestas HTTP (PWA, service worker) |

```js
// localStorage solo guarda texto: JSON para lo demás
const preferencias = { tema: "oscuro", idioma: "es" };
localStorage.setItem("prefs", JSON.stringify(preferencias));

function leerPrefs() {
  try {
    return JSON.parse(localStorage.getItem("prefs")) ?? { tema: "claro", idioma: "es" };
  } catch {
    return { tema: "claro", idioma: "es" };   // JSON corrupto o storage bloqueado
  }
}
localStorage.removeItem("prefs");

// Escuchar cambios hechos en OTRA pestaña del mismo sitio
window.addEventListener("storage", e => console.log("cambió", e.key, "a", e.newValue));
```

```flujo
dir: abajo
¿Qué guardas? -> Token de sesión : cookie HttpOnly + Secure + SameSite
¿Qué guardas? -> Preferencias pequeñas : localStorage
¿Qué guardas? -> Datos de una pestaña : sessionStorage
¿Qué guardas? -> Muchos datos u offline : IndexedDB
```

⚠️ Cuidado: **no guardes tokens de sesión en localStorage**: cualquier XSS los lee con una línea (`localStorage.getItem("token")`). Una cookie `HttpOnly` no es accesible desde JS.
⚠️ Cuidado: `localStorage` es **síncrono**: guardar un JSON de varios MB bloquea el hilo principal. Para datos grandes, IndexedDB (con una envoltura cómoda como `idb` o Dexie).
💡 Consejo: en modo incógnito o con el almacenamiento bloqueado, `localStorage` puede lanzar error o vaciarse al cerrar. Envuélvelo siempre en `try/catch` y ten un valor por defecto.

## 📅 Fechas, Intl, Temporal y regex

### 📆 Date: la API que todos odian (y por qué)

`Date` se copió en 1995 de `java.util.Date`, que Java ya ha reemplazado. Sus problemas: **meses desde 0**, es **mutable**, mezcla hora local y UTC, y parsear textos tiene reglas raras.

```js
// Ejecutado con TZ=America/La_Paz (UTC-4)
console.log(new Date(2026, 0, 31).getMonth());        // → 0   (enero es 0, diciembre es 11)
const d = new Date(2026, 0, 31);
d.setMonth(1);                                        // "pásalo a febrero"...
console.log(d.toDateString());                        // → Tue Mar 03 2026  😱 31 de febrero → 3 de marzo

const fechaUTC = new Date("2026-10-19");              // solo fecha → se interpreta en UTC
const fechaLocal = new Date("2026-10-19T00:00");      // fecha + hora → hora LOCAL
console.log(fechaLocal.getTime() === fechaUTC.getTime());  // → false (4 horas de diferencia)

// Intl: formatear bien para Bolivia
const fmt = new Intl.DateTimeFormat("es-BO", { dateStyle: "full", timeZone: "America/La_Paz" });
console.log(fmt.format(new Date(Date.UTC(2026, 9, 19, 15))));     // → lunes, 19 de octubre de 2026
console.log(new Intl.NumberFormat("es-BO", { style: "currency", currency: "BOB" }).format(1234.5)); // → Bs 1.234,50
console.log(new Intl.RelativeTimeFormat("es", { numeric: "auto" }).format(-1, "day"));            // → ayer
```

### 🕰️ Temporal: el reemplazo moderno

🧠 Concepto: **Temporal** es la nueva API de fechas del estándar: objetos **inmutables**, meses desde 1, tipos separados para "fecha sin hora" (`PlainDate`), "hora con zona" (`ZonedDateTime`) y "duración" (`Duration`). Ya está en Firefox (desde la 139, mayo de 2025) y en Chrome/Edge (desde la 144, enero de 2026); Safari aún no lo trae en versión estable. En el Node 26 de este PC todavía no está activado; en **Deno 2.9** sí funciona.

```js
// Comprobado con: deno run temporal.js   (Deno 2.9.7)
const hoy = Temporal.PlainDate.from("2026-01-31");
console.log(hoy.add({ months: 1 }).toString());       // → 2026-02-28  ✅ sin saltar a marzo
console.log(Temporal.PlainDate.from("2026-10-19").until("2026-12-25").days);  // → 67 días para Navidad
const reunion = Temporal.ZonedDateTime.from("2026-10-19T15:00[America/La_Paz]");
console.log(reunion.withTimeZone("Europe/Madrid").toPlainTime().toString());  // → 21:00:00
console.log(Temporal.Duration.from({ hours: 1, minutes: 90 })
  .round({ largestUnit: "hours" }).toString());       // → PT2H30M (2 h 30 min)
```

✅ Bien: guarda y envía fechas en **UTC con formato ISO 8601** (`2026-10-19T19:00:00.000Z`); convierte a la zona del usuario solo al mostrar.
💡 Consejo: mientras Temporal llega a todos lados, para proyectos usa `date-fns` o `dayjs` (pequeñas) o el polyfill de Temporal.

### 🔍 Expresiones regulares básicas

🧠 Concepto: una **regex** (expresión regular) es un patrón para buscar, validar o reemplazar texto. Se escribe entre barras `/patrón/banderas`.

- `\d` :: Un dígito (0-9); `\D` = lo que no es dígito
- `\w` :: Letra, dígito o _ (solo ASCII: no incluye ñ ni tildes)
- `\s` :: Espacio, tab o salto de línea
- `.` :: Cualquier carácter (menos salto de línea)
- `^` y `$` :: Inicio y fin del texto
- `+ * ? {2,4}` :: 1 o más · 0 o más · 0 o 1 · entre 2 y 4
- `[aeiou]` :: Uno de esos; `[^0-9]` = ninguno de esos
- `(?<anio>\d{4})` :: Grupo con nombre
- `/g /i /u /m` :: Todas las coincidencias · ignora mayúsculas · Unicode · multilínea

```js
const correo = /^[\w.+-]+@[\w-]+\.[\w.]+$/;
console.log(correo.test("ana.perez@umsa.bo"), correo.test("ana@@umsa"));   // → true false

const texto = "Pedido #A-102 el 2026-10-19, pedido #B-7 el 2026-11-02";
console.log(texto.match(/#[A-Z]-\d+/g));                                   // → [ '#A-102', '#B-7' ]
for (const m of texto.matchAll(/#(?<cod>[A-Z]-\d+) el (?<f>[\d-]+)/g))
  console.log(m.groups.cod, "→", m.groups.f);                              // → A-102 → 2026-10-19 / B-7 → 2026-11-02

console.log("2026-10-19".replace(/(\d+)-(\d+)-(\d+)/, "$3/$2/$1"));        // → 19/10/2026
console.log("  muchos    espacios  ".trim().replace(/\s+/g, " "));          // → muchos espacios
console.log("+591 7 123 4567".replace(/\D/g, ""));                          // → 59171234567

const g = /a/g;                                   // ⚠️ /g guarda estado en lastIndex
console.log(g.test("aa"), g.test("aa"), g.test("aa"));                      // → true true false
console.log(RegExp.escape("1+1=2?"));             // → \x31\+1\x3d2\?  (ES2025: escapa texto del usuario para usarlo en una regex)
```

⚠️ Cuidado: **ReDoS** (denegación de servicio por regex): patrones con cuantificadores anidados como `/(a+)+$/` pueden tardar un tiempo **exponencial** con ciertas entradas y congelar el hilo. En 2016 una regex mal hecha sobre un texto con miles de espacios tumbó Stack Overflow durante unos 34 minutos. Evita anidar `+` y `*`, y limita la longitud de la entrada.
💡 Consejo: no valides correos con una regex "perfecta": usa una simple para el formato y confirma enviando un correo real.

## ⚡ Rendimiento y memory leaks

🧠 Concepto: JS tiene **recolector de basura** (garbage collector, GC): libera automáticamente los objetos a los que ya **nadie puede llegar** desde las variables vivas. Un **memory leak** (fuga de memoria) en JS no es "olvidé hacer free", sino "**sigo teniendo una referencia** a algo que ya no necesito".

### 📏 Elegir la estructura correcta (medido)

```js
const N = 200_000;
const ids = Array.from({ length: N }, (_, i) => i);
const conjunto = new Set(ids);
const buscar = Array.from({ length: 2_000 }, (_, i) => N - i);

let t = performance.now();
for (const x of buscar) ids.includes(x);      // recorre el array cada vez: O(n)
const tArray = performance.now() - t;
t = performance.now();
for (const x of buscar) conjunto.has(x);      // tabla hash: O(1)
const tSet = performance.now() - t;
console.log(`array.includes: ${tArray.toFixed(1)} ms | set.has: ${tSet.toFixed(2)} ms`);
// → array.includes: 61.7 ms | set.has: 0.20 ms   (dos ejecuciones: ~62 ms vs ~0.2 ms)
```

```grafica
tipo: barras
titulo: 2000 búsquedas en 200 000 elementos (medido en este PC, Node 26)
unidad: ms
array.includes : 62
Set.has : 0.2
```

### 🕳️ Las fugas de memoria más comunes

| Fuga | Por qué no se libera | Solución |
|---|---|---|
| Caché `Map` sin límite | El Map referencia todo para siempre | Tope (LRU) o `WeakMap` |
| Listeners que nunca se quitan | El elemento/objeto sigue referenciado | `removeEventListener` o `{ signal }` |
| `setInterval` sin `clearInterval` | El callback y su closure viven siempre | Limpiar al desmontar |
| Nodos del DOM borrados guardados en variables | "Detached DOM" | Poner la variable a `null` |
| Closures que capturan datos enormes | La mochila mantiene vivo el array | Capturar solo lo necesario |
| Variables globales accidentales | El global nunca muere | Modo estricto, `const/let` |

```js
// Medido con node --expose-gc fuga.mjs
const cache = new Map();                          // ❌ crece para siempre
function procesar(id) { cache.set(id, new Array(10_000).fill(id)); }
for (let i = 0; i < 2_000; i++) procesar(i);
// → Map sin límite: +153 MB, entradas: 2000

const LIMITE = 100;                               // ✅ caché LRU (least recently used)
const lru = new Map();                            // un Map recuerda el orden de inserción
function procesarLRU(id) {
  if (lru.has(id)) { const v = lru.get(id); lru.delete(id); lru.set(id, v); return v; } // "lo usé": al final
  const v = new Array(10_000).fill(id);
  lru.set(id, v);
  if (lru.size > LIMITE) lru.delete(lru.keys().next().value);  // borra el más antiguo
  return v;
}
for (let i = 0; i < 2_000; i++) procesarLRU(i);
// → LRU con tope: entradas: 100
```

```js
// Quitar MUCHOS listeners de una vez con AbortController (navegador y Node)
const control = new AbortController();
window.addEventListener("resize", recalcular, { signal: control.signal });
window.addEventListener("scroll", recalcular, { signal: control.signal });
// al cerrar el componente/página:
control.abort();          // ✅ ambos listeners eliminados
```

### 🏎️ Reglas prácticas de rendimiento

1. **Mide antes de optimizar**: `console.time("x")` / `console.timeEnd("x")`, `performance.now()`, DevTools → Performance y Memory (Heap snapshot).
2. **Estructura correcta** > micro-trucos: `Set`/`Map` para búsquedas, no arrays.
3. **No toques el DOM en bucles**: arma todo y añádelo de una vez (`replaceChildren(...)` o un `DocumentFragment`). Leer `offsetHeight` después de escribir estilos fuerza un **reflow** (recalcular el layout).
4. **Debounce/throttle** para eventos que disparan muchas veces (input, scroll, resize).
5. **Carga menos JS**: el JS es el recurso más caro de la web (hay que descargarlo, parsearlo y ejecutarlo). Usa `import()` dinámico para lo que no se necesita al inicio.
6. **Trabajo pesado fuera del hilo principal**: Web Workers / worker_threads.
7. **Tipos estables**: un objeto que siempre tiene los mismos campos en el mismo orden deja que V8 lo optimice (hidden classes).

💡 Consejo: en Chrome DevTools → **Memory** → toma un *heap snapshot*, haz la acción sospechosa varias veces, toma otro y compara: lo que crece sin parar es tu fuga.

## 💥 Errores de otros programadores (para no repetirlos)

Cada uno con **causa → consecuencia → cómo evitarlo**. Todos los resultados están comprobados en Node.

| Error | Causa | Consecuencia | Cómo evitarlo |
|---|---|---|---|
| `0.1 + 0.2 !== 0.3` | Binario IEEE 754 | Totales de dinero con céntimos raros | Centavos enteros, `toFixed` al mostrar |
| `typeof null === "object"` | Bug de la primera versión, nunca se arregló | `if (typeof x === "object")` deja pasar null | `x !== null && typeof x === "object"` |
| `NaN !== NaN` | Así lo define IEEE 754 | `x === NaN` siempre es false | `Number.isNaN(x)` |
| `[10, 1, 2].sort()` → `[1, 10, 2]` | sort compara como texto | Rankings y precios mal ordenados | `sort((a, b) => a - b)` |
| `["1","2","3"].map(parseInt)` | map pasa (valor, **índice**); parseInt usa el índice como base | `[1, NaN, NaN]` | `map(Number)` o `map(s => parseInt(s, 10))` |
| `cantidad || 10` con 0 | `||` trata 0 y "" como falsos | Se pierde un 0 válido | `??` |
| Mutación accidental | Referencias compartidas | Datos que cambian "solos" | Copias, `toSorted`, `structuredClone` |
| Meses desde 0 en `Date` | Copiado de Java en 1995 | Fechas con un mes de diferencia | Temporal o librerías |
| `this` perdido en callbacks | `this` depende de la llamada | `Cannot read properties of undefined` | Flechas o `bind` |
| Promesa sin `await` | Una promesa es truthy | `if (promesa)` siempre true | ESLint `no-floating-promises` (TS) |

### 🧨 Mutación accidental: cinco formas de pisarte el pie

```js
const ranking = [{ n: "Ana", p: 90 }, { n: "Luis", p: 70 }];
function peor(lista) { return lista.sort((a, b) => a.p - b.p)[0]; }  // ❌ sort muta
peor(ranking);
console.log(ranking.map(x => x.n));          // → [ 'Luis', 'Ana' ]  el original quedó reordenado

const config = { tema: "oscuro", atajos: { guardar: "Ctrl+S" } };
const mia = config;  mia.tema = "claro";
console.log(config.tema);                    // → claro   (misma referencia, no es copia)

const superficial = { ...config };  superficial.atajos.guardar = "Ctrl+G";
console.log(config.atajos.guardar);          // → Ctrl+G  (el spread copia solo un nivel)

const fechas = [];
const d = new Date(2026, 0, 1);
for (let i = 0; i < 3; i++) { d.setDate(d.getDate() + 1); fechas.push(d); }  // ❌ el mismo objeto 3 veces
console.log(fechas.map(f => f.getDate()));   // → [ 4, 4, 4 ]

function agregar(item, lista = []) { lista.push(item); return lista; }
console.log(agregar(1), agregar(2));         // → [ 1 ] [ 2 ]  ✅ en JS el default se crea en CADA llamada
// (en Python, def f(x, lista=[]) SÍ comparte la lista entre llamadas: error clásico de allá)
```

### 🔢 Números y texto que sorprenden

```js
console.log((1.005).toFixed(2), Math.round(1.005 * 100) / 100);  // → 1.00 1   (1.005 es en realidad 1.00499...)
console.log(Math.round(-2.5), Math.round(2.5));                   // → -2 3     (redondea hacia +∞ en .5)
console.log(Math.trunc(-2.7), Math.floor(-2.7));                  // → -2 -3
console.log(parseInt(0.0000005));                                 // → 5  (porque String(0.0000005) es "5e-7")
console.log("ñandú".length, "👍".length, [..."👍"].length);        // → 5 2 1  (length cuenta unidades UTF-16)
console.log("ß".toUpperCase());                                   // → SS
```

### 📰 Incidentes reales del ecosistema JS

```tiempo
2016 : left-pad: un autor despublica de npm un paquete de 11 líneas y rompe builds de React y Babel en todo el mundo
2018 : event-stream: un nuevo mantenedor "voluntario" añade código para robar carteras de bitcoin (Copay)
2021 : ua-parser-js: secuestran la cuenta del autor y publican versiones con malware minero
2022 : colors y faker: su propio autor los sabotea con un bucle infinito como protesta
2025 : ataque a npm: phishing al mantenedor de chalk y debug, y el gusano Shai-Hulud que se propaga entre paquetes
```

| Lección | Qué hacer |
|---|---|
| Una dependencia diminuta puede romperlo todo | ¿De verdad necesitas un paquete para 5 líneas? |
| Las versiones nuevas pueden traer malware | Commitea `package-lock.json` y usa `npm ci` en CI |
| Los scripts de instalación ejecutan código | Revisa `postinstall`; considera `--ignore-scripts` |
| Las cuentas de mantenedores son el eslabón débil | 2FA en npm; desconfía de correos "urgentes" |
| Vulnerabilidades conocidas | `npm audit`, Dependabot o Renovate |

⚠️ Cuidado: `eval()` y `new Function(texto)` ejecutan texto como código: con datos del usuario es inyección de código directa. No hay casi ningún caso legítimo en una app normal.
⚠️ Cuidado: los secretos (API keys) puestos en el código del frontend **son públicos**: cualquiera los ve en DevTools → Sources. Las claves privadas van solo en el backend (variables de entorno).

## ⚖️ JavaScript vs TypeScript vs Python

🧠 Concepto: **TypeScript** (TS) es un **superconjunto** de JS: todo JS válido es TS válido, más **tipos estáticos** que se comprueban al compilar y luego **se borran**. El navegador nunca ve los tipos: ejecuta el JS resultante.

```ts
// usuario.ts — el error aparece en el EDITOR, antes de ejecutar nada
interface Alumno { nombre: string; nota: number; correo?: string }

function aprobados(lista: Alumno[], minimo = 51): string[] {
  return lista.filter(a => a.nota >= minimo).map(a => a.nombre);
}

aprobados([{ nombre: "Ana", nota: "85" }]);
// ❌ Type 'string' is not assignable to type 'number'.   (en JS esto pasaba y "85" >= 51 daba true)
```

| | JavaScript | TypeScript | Python |
|---|---|---|---|
| Tipos | Dinámicos, débiles | Estáticos (se borran al compilar) | Dinámicos, fuertes; hints opcionales |
| `"5" + 3` | `"53"` | Error si los tipos chocan | `TypeError` |
| Dónde corre | Navegador + Node/Deno/Bun | Igual (compila a JS) | CPython, servidores, notebooks |
| Concurrencia | Event loop, async/await | Igual | GIL, asyncio, multiprocessing |
| Fuerte en | Web, UI, APIs, tiempo real | Proyectos grandes, equipos | IA/ML, datos, scripts, ciencia |
| Ecosistema | npm | npm + tipos `@types` | PyPI (NumPy, PyTorch, pandas) |
| Curva | Fácil empezar, raro dominar | + aprender el sistema de tipos | La más amable |

```flujo
dir: abajo
¿Corre en el navegador? -> JS o TS : sí
¿Corre en el navegador? -> ¿Es IA / datos? : no
¿Es IA / datos? -> Python : sí
¿Es IA / datos? -> ¿Proyecto grande o en equipo? : no
¿Proyecto grande o en equipo? -> TypeScript : sí
¿Proyecto grande o en equipo? -> JS o Python : script pequeño
```

::: columnas
### 🟨 Elige JS puro cuando...
- Es un script corto o un prototipo.
- Estás aprendiendo los fundamentos.
- Un `<script>` pequeño en una página.
- No quieres paso de compilación.
::: siguiente
### 🟦 Elige TypeScript cuando...
- El proyecto vivirá meses o años.
- Trabajan varias personas.
- Hay modelos de datos y APIs.
- Quieres refactorizar sin miedo.
::: siguiente
### 🐍 Elige Python cuando...
- IA, ML, ciencia de datos.
- Automatización y scripts de sistema.
- Backends con Django/FastAPI.
- No necesitas el navegador.
:::

📌 Resumen: no compiten tanto como parece. Un proyecto típico de IA hoy: **Python** entrena y sirve el modelo, **TypeScript** hace la web que lo usa. Aprender JS bien es requisito para TS: los tipos no te salvan de no entender el event loop o el `this`.

## 🛠️ Herramientas, frameworks y casos de uso

```capas
Framework de UI : React, Vue, Svelte, Angular, Solid
Meta-framework : Next.js, Nuxt, SvelteKit, Astro, Remix
Bundler / dev server : Vite (esbuild + Rollup), webpack, Turbopack
Calidad : ESLint, Prettier, Biome, TypeScript
Tests : Vitest, Jest, Playwright, Cypress
Paquetes : npm, pnpm, yarn, bun
Runtime : Node.js, Deno, Bun, navegador
```

### 📦 npm en 10 comandos

- `npm init -y` :: Crea `package.json` con valores por defecto
- `npm create vite@latest mi-app` :: Proyecto nuevo con Vite (elige React, Vue, vanilla...)
- `npm install zod` :: Añade una dependencia (`npm i`)
- `npm install -D vitest` :: Dependencia solo de desarrollo
- `npm ci` :: Instala EXACTO lo del lockfile (para CI/servidores)
- `npm run dev` :: Ejecuta el script `dev` de `package.json`
- `npx eslint .` :: Ejecuta una herramienta sin instalarla globalmente
- `npm outdated` :: ¿Qué dependencias tienen versión nueva?
- `npm audit` :: Vulnerabilidades conocidas en tus dependencias
- `npm ls paquete` :: ¿Por qué tengo instalado este paquete?

```json
{
  "name": "notas-umsa",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "test": "vitest",
    "lint": "eslint .",
    "format": "prettier --write ."
  },
  "dependencies": { "zod": "^4.0.0" },
  "devDependencies": { "vite": "^8.0.0", "vitest": "^5.0.0", "eslint": "^10.0.0", "prettier": "^3.9.0" }
}
```

🧠 Concepto: **SemVer** (versionado semántico) = `MAYOR.MENOR.PARCHE`. `^4.0.0` acepta `4.x.x` (cambios compatibles); `~4.0.0` solo `4.0.x`. El **lockfile** (`package-lock.json`) fija la versión exacta de **todo** el árbol: commitéalo siempre.

| Herramienta | Qué hace | Por qué importa |
|---|---|---|
| **Vite** | Servidor de desarrollo instantáneo + build | Reemplazó a webpack en la mayoría de proyectos nuevos |
| **ESLint** | Encuentra bugs y malas prácticas | `eqeqeq`, `no-unused-vars`, promesas sin manejar |
| **Prettier** | Formatea el código siempre igual | Se acabaron las discusiones de estilo en los PR |
| **Biome** | Linter + formateador en Rust | Alternativa muy rápida a ESLint + Prettier |
| **TypeScript** | Comprobación de tipos (`tsc --noEmit`) | Atrapa errores antes de ejecutar |
| **Vitest / Jest** | Tests unitarios | Vitest comparte la config de Vite |
| **Playwright** | Tests end-to-end en navegadores reales | Chrome, Firefox y WebKit |

### 🧭 Frameworks de UI: cuál y por qué

| Framework | Idea central | Úsalo si... | Quién lo usa (conocidos) |
|---|---|---|---|
| React | Componentes + estado inmutable | Quieres el mayor mercado laboral | Meta, Netflix, Airbnb |
| Vue | Reactividad simple, plantillas | Quieres curva suave | GitLab, Alibaba |
| Angular | Framework completo con TS | Empresas grandes con estructura fija | Google (muchas apps internas) |
| Svelte | Compila; casi sin runtime | Quieres poco JS en el cliente | The New York Times (sus gráficos) |
| Astro | Páginas de contenido, JS solo donde hace falta | Blogs, documentación, landing pages | Muchos sitios de docs |

💡 Consejo: antes de elegir framework, domina el **JS de esta hoja**: closures, inmutabilidad, promesas y eventos. Los frameworks cambian cada pocos años; esto no.

## 🚀 Futuro de JavaScript

```tiempo
Hoy : ES2025 en todos los motores modernos; TypeScript es el estándar de facto en proyectos serios
2025-2026 : Node, Deno y Bun ejecutan .ts directamente quitando los tipos
2026 : Temporal disponible en Firefox y Chrome
2026 : TypeScript 7, el compilador reescrito en Go (entre 8 y 12 veces más rápido según Microsoft)
Propuesta : "type annotations": que el propio JS ignore la sintaxis de tipos
Propuesta : decoradores estándar, Signals para reactividad, manejo de recursos con using
```

🚀 Futuro: **TypeScript sin compilar**. Node incorporó *type stripping* (quitar los tipos y ejecutar) y Deno/Bun lo hacen desde su nacimiento. La propuesta TC39 de **type annotations** (Stage 1) busca que el lenguaje acepte la sintaxis de tipos y la ignore, como comentarios.
🚀 Futuro: **herramientas en lenguajes nativos**. esbuild (Go), SWC, Biome, Oxc y Rolldown (Rust) y el nuevo compilador de TypeScript en Go: la tendencia es que el tooling de JS ya no esté escrito en JS, por velocidad.
🚀 Futuro: **Signals**. Casi todos los frameworks (Solid, Vue, Angular, Svelte 5, Preact) convergieron en "señales" para la reactividad; hay una propuesta TC39 para estandarizarlas.
🚀 Futuro: **JS en el borde e IA**. Los runtimes edge (Cloudflare Workers, Vercel, Deno Deploy) ejecutan JS cerca del usuario, y los SDK de IA más usados (OpenAI, Anthropic, Vercel AI SDK) tienen versión TS de primera clase: mucha de la "capa de aplicación" de la IA se escribe en TypeScript.
🚀 Futuro: **WebAssembly** no reemplaza a JS: lo complementa para lo pesado (Figma, editores de video, juegos), mientras JS orquesta la interfaz.

```js
// Lo que ya funciona en el Node 26 de este PC (comprobado con typeof)
Iterator.from([1, 2, 3]).map(x => x * 2).toArray();   // iterator helpers (ES2025)
new Set([1, 2]).union(new Set([2, 3]));                // métodos de Set (ES2025)
RegExp.escape("1+1");                                  // ES2025
Promise.try(() => JSON.parse("{}"));                   // ES2025
Error.isError(new TypeError());                        // reciente
Uint8Array.fromBase64("aG9sYQ==");                     // base64 nativo, reciente
await Array.fromAsync(generadorAsincrono());           // reciente
```

💡 Consejo: para saber si algo ya se puede usar, mira la tabla de compatibilidad de MDN o "Can I use". Y sigue el repositorio `tc39/proposals` para ver qué viene.

🇬🇧 **type stripping** /taip strípin/ = quitar los tipos · **tooling** /túling/ = herramientas de desarrollo · **edge** /ech/ = borde de la red · **bundle** /bándol/ = paquete final de JS

## 🏋️ Ejercicios (de fácil a difícil)

Intenta cada uno **antes** de abrir la solución. Todas las soluciones se ejecutaron con Node 26 y la salida mostrada es la real.

### 1️⃣ Contar vocales (fácil)
Escribe `contarVocales(texto)` que cuente las vocales, **incluidas las tildadas** (`"Murciélago"` → 5).

::: desplegable 🧩 Ver la solución
```js
const contarVocales = s => (s.normalize("NFD").match(/[aeiou]/gi) ?? []).length;
console.log(contarVocales("Murciélago"), contarVocales("xyz"));   // → 5 0
```
- `normalize("NFD")` separa la "é" en "e" + tilde, así la regex la reconoce.
- `match` devuelve `null` si no hay coincidencias: `?? []` evita el error de `null.length`.
:::

### 2️⃣ Quitar duplicados manteniendo el orden (fácil)
`unicos([3, 1, 3, 2, 1])` → `[3, 1, 2]`.

::: desplegable 🧩 Ver la solución
```js
const unicos = lista => [...new Set(lista)];
console.log(unicos([3, 1, 3, 2, 1]));   // → [ 3, 1, 2 ]
```
Un `Set` guarda el orden de inserción y descarta repetidos. Es O(n); la versión con `filter` + `indexOf` es O(n²).
:::

### 3️⃣ agruparPor con reduce (medio)
Implementa `agruparPor(lista, fn)` sin usar `Object.groupBy`.

::: desplegable 🧩 Ver la solución
```js
const agruparPor = (lista, fn) =>
  lista.reduce((acc, x) => { (acc[fn(x)] ??= []).push(x); return acc; }, {});
console.log(agruparPor(["ana", "alba", "luis", "lea", "sofía"], s => s[0]));
// → { a: [ 'ana', 'alba' ], l: [ 'luis', 'lea' ], s: [ 'sofía' ] }
```
:::

### 4️⃣ Predice la salida (medio)
Sin ejecutarlo: ¿en qué orden se imprimen los números?

```js
console.log("1");
setTimeout(() => console.log("2"), 0);
Promise.resolve().then(() => { console.log("3"); setTimeout(() => console.log("4"), 0); });
(async () => { console.log("5"); await Promise.resolve(); console.log("6"); })();
queueMicrotask(() => console.log("7"));
console.log("8");
```

::: desplegable 🧩 Ver la solución
Salida real: **1 5 8 3 6 7 2 4**

1. Síncrono: `1`, luego la async imprime `5` hasta su `await`, luego `8`.
2. Microtareas en orden de llegada: `then` (3, y programa el timeout 4), la continuación del await (6), `queueMicrotask` (7).
3. Macrotareas en orden: el timeout `2` (programado primero) y después el `4`.
:::

### 5️⃣ conTimeout (medio)
Escribe `conTimeout(promesa, ms)` que rechace con `"Timeout de X ms"` si la promesa tarda más.

::: desplegable 🧩 Ver la solución
```js
function conTimeout(promesa, ms) {
  let id;
  const limite = new Promise((_, rej) => {
    id = setTimeout(() => rej(new Error(`Timeout de ${ms} ms`)), ms);
  });
  return Promise.race([promesa, limite]).finally(() => clearTimeout(id));  // limpia el timer
}
const lenta = new Promise(r => setTimeout(() => r("datos"), 300));
try { await conTimeout(lenta, 100); } catch (e) { console.log(e.message); }  // → Timeout de 100 ms
console.log(await conTimeout(Promise.resolve("rápido"), 100));              // → rápido
```
El `clearTimeout` en `finally` evita dejar timers vivos (en Node, un timer pendiente impide que el proceso termine).
:::

### 6️⃣ Tu propio Promise.all (medio-difícil)
Implementa `miPromiseAll(lista)` con el mismo comportamiento: resultados en el **orden original**, falla con el primer error y acepta valores que no son promesas.

::: desplegable 🧩 Ver la solución
```js
function miPromiseAll(promesas) {
  return new Promise((resolve, reject) => {
    const resultados = [];
    let pendientes = promesas.length;
    if (pendientes === 0) return resolve([]);
    promesas.forEach((p, i) => {
      Promise.resolve(p).then(v => {           // Promise.resolve envuelve valores normales
        resultados[i] = v;                      // por índice, no con push: respeta el orden
        if (--pendientes === 0) resolve(resultados);
      }, reject);                               // el primer rechazo gana
    });
  });
}
const esperar = (ms, v) => new Promise(r => setTimeout(() => r(v), ms));
console.log(await miPromiseAll([esperar(30, "a"), 42, esperar(10, "c")]));   // → [ 'a', 42, 'c' ]
try { await miPromiseAll([esperar(10, 1), Promise.reject(new Error("falló una"))]); }
catch (e) { console.log(e.message); }                                         // → falló una
```
:::

### 7️⃣ Igualdad profunda (difícil)
`iguales(a, b)` que compare objetos y arrays anidados por contenido.

::: desplegable 🧩 Ver la solución
```js
function iguales(a, b) {
  if (Object.is(a, b)) return true;
  if (typeof a !== "object" || typeof b !== "object" || a === null || b === null) return false;
  if (Array.isArray(a) !== Array.isArray(b)) return false;
  const ka = Object.keys(a), kb = Object.keys(b);
  return ka.length === kb.length && ka.every(k => iguales(a[k], b[k]));
}
console.log(iguales({ x: [1, { y: 2 }] }, { x: [1, { y: 2 }] }));  // → true
console.log(iguales({ x: 1 }, { x: "1" }));                         // → false
console.log(iguales([1, 2], { 0: 1, 1: 2 }));                       // → false
```
Limitaciones para comentar en una entrevista: no maneja ciclos, `Date`, `Map` ni `Set`. Para eso se usa una librería probada (por ejemplo `isEqual` de lodash) o `node:util`'s `isDeepStrictEqual`.
:::

### 8️⃣ curry y throttle (difícil)
a) `curry(fn)` que permita llamar `f(a)(b)(c)` o `f(a, b)(c)`. b) `throttle(fn, ms)` que ejecute como máximo una vez cada `ms`.

::: desplegable 🧩 Ver la solución
```js
const curry = fn => function c(...args) {
  return args.length >= fn.length ? fn(...args) : (...mas) => c(...args, ...mas);
};
const precioFinal = curry((iva, descuento, precio) => +(precio * (1 - descuento) * (1 + iva)).toFixed(2));
const conIvaBolivia = precioFinal(0.13);           // IVA del 13 %
console.log(conIvaBolivia(0.1)(100), conIvaBolivia(0, 50));   // → 101.7 56.5

function throttle(fn, ms) {
  let ultimo = 0;
  return (...a) => {
    const ahora = Date.now();
    if (ahora - ultimo >= ms) { ultimo = ahora; fn(...a); }
  };
}
let veces = 0;
const t = throttle(() => veces++, 50);
for (let i = 0; i < 1000; i++) t();
console.log("throttle ejecutó:", veces);           // → throttle ejecutó: 1
```

| | Debounce | Throttle |
|---|---|---|
| Ejecuta | Al terminar la ráfaga | Como máximo 1 vez por intervalo |
| Ejemplo | Buscador al escribir | Posición al hacer scroll |
:::

### 9️⃣ Mini proyecto: lista de tareas con delegación (integrador)
Con un `<form>` y un `<ul>`: añadir, marcar y borrar tareas, guardarlas en `localStorage`, con **un solo** listener para la lista y actualizaciones **inmutables**.

::: desplegable 🧩 Ver la solución
```js
// HTML: <form id="nueva"><input name="texto" required><button>Añadir</button></form>
//       <ul id="tareas"></ul> <p id="resumen"></p>
const form = document.querySelector("#nueva");
const ul = document.querySelector("#tareas");
const resumen = document.querySelector("#resumen");

let tareas;
try { tareas = JSON.parse(localStorage.getItem("tareas")) ?? []; } catch { tareas = []; }

function guardarYPintar() {
  try { localStorage.setItem("tareas", JSON.stringify(tareas)); } catch {}
  ul.replaceChildren(...tareas.map(t => {           // un solo cambio al DOM
    const li = document.createElement("li");
    li.dataset.id = t.id;
    li.className = t.hecha ? "hecha" : "";
    const check = Object.assign(document.createElement("input"), { type: "checkbox", checked: t.hecha });
    const texto = Object.assign(document.createElement("span"), { textContent: t.texto }); // sin XSS
    const borrar = Object.assign(document.createElement("button"), { className: "borrar", textContent: "🗑️" });
    li.append(check, " ", texto, " ", borrar);
    return li;
  }));
  resumen.textContent = `${tareas.filter(t => !t.hecha).length} pendiente(s) de ${tareas.length}`;
}

form.addEventListener("submit", e => {
  e.preventDefault();
  const texto = new FormData(form).get("texto").trim();
  if (!texto) return;
  tareas = [...tareas, { id: crypto.randomUUID(), texto, hecha: false }];
  form.reset();
  guardarYPintar();
});

ul.addEventListener("click", e => {                  // delegación
  const id = e.target.closest("li")?.dataset.id;
  if (!id) return;
  if (e.target.matches(".borrar")) tareas = tareas.filter(t => t.id !== id);
  if (e.target.matches("input[type=checkbox]"))
    tareas = tareas.map(t => (t.id === id ? { ...t, hecha: !t.hecha } : t));
  guardarYPintar();
});

guardarYPintar();
```
El array `tareas` es la **única fuente de verdad**: cada acción crea un array nuevo y llama a una única función que guarda y redibuja. Es exactamente la idea de React, hecha a mano.
:::

## 🎤 Preguntas típicas de entrevista

::: desplegable ❓ ¿Diferencia entre == y ===?
`===` compara tipo y valor sin convertir. `==` aplica coerción (`0 == ""` es `true`, `null == undefined` es `true`). En código profesional se usa `===` siempre, salvo el modismo `x == null` para atrapar null y undefined juntos.
:::

::: desplegable ❓ ¿Qué es un closure? Da un caso real.
Una función que recuerda las variables del scope donde se creó, aunque ese scope ya haya terminado. Casos reales: datos privados (contador), fábricas de funciones, memoización, **debounce** en un buscador y los hooks de React. Riesgo: pueden mantener vivos datos grandes (fugas).
:::

::: desplegable ❓ Explica el event loop.
JS corre en un hilo con una call stack. Lo lento (timers, red, I/O) lo hace el entorno; al terminar, encola callbacks. Cuando la pila se vacía, el event loop ejecuta **todas** las microtareas (promesas, await) y luego **una** macrotarea (setTimeout, eventos), y en el navegador pinta entre medio. Por eso un `then` sale antes que un `setTimeout(…, 0)` y un bucle largo congela la página.
:::

::: desplegable ❓ ¿Diferencias entre var, let y const?
`var` tiene scope de función, se eleva con `undefined` y se puede redeclarar. `let` y `const` tienen scope de bloque y TDZ (error si los usas antes de declararlos). `const` impide reasignar la variable, pero no mutar el objeto al que apunta.
:::

::: desplegable ❓ ¿Cómo se decide el valor de this?
Por cómo se llama la función: `obj.f()` → obj; `f()` → undefined en modo estricto; `new F()` → el objeto nuevo; `call/apply/bind` → el que pases. Las flechas no tienen this propio: usan el del scope donde se escribieron.
:::

::: desplegable ❓ ¿Qué es la herencia prototípica? ¿class cambia algo?
Cada objeto tiene un enlace a su prototipo; si una propiedad no está en el objeto, se busca en la cadena hasta `null`. `class` es azúcar sintáctico sobre ese mismo mecanismo (añade `#privados`, `static`, `super` y una sintaxis más clara, pero `typeof` de una clase sigue siendo `"function"`).
:::

::: desplegable ❓ null vs undefined
`undefined`: el valor por defecto de lo que no se asignó (variable sin valor, propiedad inexistente, función sin return). `null`: un "vacío" que pones **tú** a propósito. `typeof null` es `"object"` por un bug histórico. `null == undefined` es true, `null === undefined` es false.
:::

::: desplegable ❓ ¿Copia superficial vs profunda?
La superficial (`{...obj}`, `Object.assign`, `slice`) copia un nivel: los objetos anidados siguen compartidos. La profunda copia todo el árbol: `structuredClone(obj)` (soporta Date, Map, Set y ciclos; no funciones). `JSON.parse(JSON.stringify(obj))` es el truco viejo y pierde fechas, undefined y funciones.
:::

::: desplegable ❓ Promise.all vs allSettled vs race vs any
`all`: todas deben cumplir, falla con la primera que falle. `allSettled`: espera todas y te da el estado de cada una. `race`: la primera que termine (bien o mal), ideal para timeouts. `any`: la primera que cumpla; falla con `AggregateError` solo si todas fallan.
:::

::: desplegable ❓ ¿ESM o CommonJS? ¿Por qué?
ESM: estándar, análisis estático (permite tree shaking), funciona en navegadores, top-level await. CommonJS: `require` dinámico, el formato histórico de Node. En proyectos nuevos, ESM; CJS se mantiene por compatibilidad con paquetes viejos.
:::

::: desplegable ❓ ¿Qué es la delegación de eventos?
Poner un único listener en un contenedor y usar `e.target.closest(...)` para saber qué hijo se activó, aprovechando el bubbling. Menos listeners, menos memoria, y funciona con elementos añadidos después.
:::

::: desplegable ❓ ¿Cómo detectarías una fuga de memoria en una SPA?
DevTools → Memory: heap snapshot, repetir la acción (abrir/cerrar un modal varias veces), otro snapshot y comparar. Sospechosos habituales: listeners sin quitar, `setInterval` sin limpiar, cachés sin límite, nodos DOM separados retenidos por variables o closures.
:::

::: desplegable ❓ ¿Por qué 0.1 + 0.2 !== 0.3 y cómo manejas dinero?
Los números son binarios IEEE 754 de 64 bits y 0.1 no tiene representación exacta en binario. Para dinero: enteros en centavos (o `BigInt`), o una librería decimal; redondea solo al mostrar con `Intl.NumberFormat`.
:::

## 🇬🇧 Vocabulario en inglés

| English | Suena | Español |
|---|---|---|
| scope | /skoup/ | ámbito, alcance |
| hoisting | /hóisting/ | elevación de declaraciones |
| closure | /klóushur/ | clausura (función con memoria) |
| callback | /kólbak/ | función que se llama después |
| promise | /prómis/ | promesa |
| resolve / reject | /risólv/ /riyékt/ | cumplir / rechazar |
| pending | /pénding/ | pendiente |
| event loop | /ivént lup/ | bucle de eventos |
| call stack | /kol stak/ | pila de llamadas |
| bubbling | /bábling/ | propagación hacia arriba |
| event delegation | /ivént delegéishon/ | delegación de eventos |
| shallow / deep copy | /shálou/ /dip kópi/ | copia superficial / profunda |
| immutable | /imiútabol/ | inmutable |
| garbage collector | /gárbich kolékter/ | recolector de basura |
| memory leak | /mémori lik/ | fuga de memoria |
| truthy / falsy | /trúzi/ /fólsi/ | que cuenta como verdadero / falso |
| arrow function | /árou fánkshon/ | función flecha |
| spread / rest | /spred/ /rest/ | expandir / juntar el resto |
| destructuring | /distrákchering/ | desestructuración |
| bundler | /bándler/ | empaquetador |
| lockfile | /lókfail/ | archivo de versiones exactas |
| throw / catch | /zróu/ /kach/ | lanzar / atrapar (un error) |

🇬🇧 Frases que oirás en el equipo: **"It's a race condition"** = dos cosas asíncronas terminan en un orden inesperado · **"Don't mutate the state"** = no cambies el estado, crea uno nuevo · **"That promise is never awaited"** = esa promesa nunca se espera · **"It's blocking the main thread"** = está bloqueando el hilo principal.

## 📌 Resumen final (la chuleta de la chuleta)

| Tema | Recuerda esto |
|---|---|
| Igualdad | `===` siempre; `??` en vez de `||` para valores por defecto |
| Variables | `const` por defecto, `let` si cambia, nunca `var` |
| Scope | Léxico: lo decide dónde está escrito |
| Closures | Funciones con mochila de variables vivas |
| this | Depende de cómo se llama; las flechas usan el de afuera |
| Clases | Azúcar sobre prototipos; prefiere composición |
| Arrays | `map/filter/reduce`; ojo, `sort` y `splice` mutan |
| Objetos | Variables = referencias; spread copia 1 nivel; `structuredClone` copia todo |
| Event loop | Síncrono → todas las micro → una macro → repetir |
| Async | `async/await` + `try/catch`; `Promise.all` para paralelo |
| Errores | Lanza `Error`, nunca textos; no te tragues los errores |
| Módulos | ESM (`import/export`) en todo proyecto nuevo |
| DOM | `textContent` > `innerHTML`; delegación de eventos |
| fetch | Revisa `res.ok`; usa `AbortSignal.timeout` |
| Storage | Tokens en cookie HttpOnly, no en localStorage |
| Fechas | UTC + ISO al guardar; Temporal es el futuro |
| Rendimiento | Mide primero; `Set` para búsquedas; no bloquees el hilo |
| Seguridad | Nada de `eval`; lockfile + `npm audit`; secretos solo en el backend |

```flujo
dir: abajo
Fundamentos JS -> Asincronía y event loop
Asincronía y event loop -> DOM y fetch
DOM y fetch -> TypeScript
TypeScript -> Framework (React o Vue)
Framework (React o Vue) -> Node y backend
```

📌 Resumen: el orden de aprendizaje recomendado es este de arriba. Si dominas tipos y coerción, closures, `this`, inmutabilidad y el event loop, entenderás **por qué** se comportan así React, Node y cualquier framework que llegue después.
