# 🟩 Node.js · JavaScript en el servidor
> V8 + libuv, event loop, npm, Express, APIs REST, bases de datos, auth, streams, workers, tests, seguridad y despliegue: con ejemplos ejecutados en Node 26.

## 🟩 Qué es Node.js y por qué existe

![Logo oficial de Node.js (Wikimedia Commons, OpenJS Foundation)](img/node/node-logo.png)

🧠 Concepto: **Node.js** es un **runtime** (entorno de ejecución) que corre JavaScript fuera del navegador.
🧠 Concepto: junta el motor **V8** de Google (compila JS a código máquina), la librería **libuv** (en C, hace la E/S asíncrona) y una **librería estándar** (fs, http, crypto).

En 2009 los servidores típicos (Apache con PHP, Java) usaban **un hilo por conexión**: si 10 000 usuarios esperaban a la base de datos, había 10 000 hilos dormidos comiendo memoria. Ryan Dahl tuvo la idea de usar **un solo hilo** que nunca espera: pide la operación al sistema operativo, sigue atendiendo a otros, y cuando la respuesta está lista ejecuta un **callback** (función de retorno). JavaScript encajaba perfecto porque ya estaba hecho para eventos (clics del navegador) y no tenía una librería de E/S bloqueante heredada.

```capas
Tu código : app.js, Express, tus rutas — JavaScript
Librería de Node : fs, http, net, crypto, stream — JS + C++
Bindings C++ : puente entre JS y el mundo nativo
V8 : compila y ejecuta JS — heap, GC, JIT
libuv : event loop + thread pool + epoll/kqueue/IOCP
Sistema operativo : sockets, archivos, procesos — Linux, macOS, Windows
```

![Ryan Dahl, creador de Node.js (2009) y luego de Deno (2018) — foto de Wikimedia Commons](img/node/ryan-dahl.jpg)

::: columnas
### 🟨 JS en el navegador
- Tiene `document`, `window`, `localStorage`
- Sandbox: no toca tus archivos
- Lo controla el usuario (lo puede ver y cambiar)
- Motor: V8, SpiderMonkey o JavaScriptCore
::: siguiente
### 🟩 JS en Node
- Tiene `process`, `fs`, `http`, `child_process`
- Acceso completo al disco, red y procesos
- Lo controlas tú (código y secretos seguros)
- Motor: siempre V8
:::

📌 Ambos comparten: `fetch`, `URL`, `setTimeout`, `console`, `crypto.randomUUID()`, `structuredClone`, `AbortController`, `TextEncoder`. Node adoptó muchas **Web APIs** para que el mismo código sirva en los dos lados.

### 📜 Historia en una línea de tiempo

```tiempo
2009 : Ryan Dahl presenta Node en JSConf EU
2010 : nacen npm (Isaac Schlueter) y Express (TJ Holowaychuk)
2014 : fork io.js por desacuerdos de gobierno
2015 : io.js y Node se reúnen en Node 4 (Node.js Foundation)
2016 : incidente left-pad rompe miles de builds
2018 : Dahl anuncia Deno ("10 cosas que lamento de Node")
2019 : OpenJS Foundation · ESM sin flag (Node 13.2)
2023 : Bun 1.0 compite como runtime
2024 : Express 5 estable · type stripping experimental (22.6)
2025 : TypeScript sin flag (23.6) · gusano Shai-Hulud en npm
2026 : Node 26 (el de este PC: v26.11.1)
```

### 🏢 Dónde se usa de verdad

| Empresa / proyecto | Para qué usa Node |
|---|---|
| PayPal | migró páginas de Java a Node (2013); contaron menos código y respuestas más rápidas |
| Netflix | capa de interfaz y servidores "edge" que arman las páginas |
| LinkedIn | backend de su app móvil (2011, venía de Ruby on Rails) |
| Walmart | backend móvil; lo usaron en Black Friday de 2013 |
| VS Code, Slack, Discord | apps de escritorio con **Electron** (= Chromium + Node) |
| Vite, ESLint, Prettier, Next.js | casi todo el tooling de frontend corre sobre Node |

| ✅ Node brilla en | ❌ Mejor otra cosa |
|---|---|
| APIs REST/GraphQL con mucha E/S | cálculo numérico pesado, IA (Python, C++) |
| tiempo real: chats, websockets, juegos | procesar video/imágenes en el hilo del servidor |
| BFF (backend for frontend) y proxies | sistemas con latencia dura de microsegundos (Rust, C) |
| CLIs y herramientas de desarrollo | scripts de ciencia de datos (pandas, NumPy) |
| full stack con un solo lenguaje (JS/TS) | microcontroladores pequeños |

- `node -v` :: Versión de Node (aquí v26.11.1)
- `node` :: REPL: escribe JS y ve el resultado (.exit para salir)
- `node app.js` :: Ejecuta un archivo
- `node -e "console.log(2 + 2)"` :: Ejecuta una línea suelta
- `node -p "process.versions"` :: Versiones de V8, libuv, OpenSSL...
- `fnm install --lts` :: Instala la última LTS con el gestor de versiones fnm
- `fnm use 24` :: Cambia de versión en esta terminal
- `echo 24 > .nvmrc` :: Fija la versión del proyecto (fnm y nvm la leen)

```bash
node -p "process.versions.v8 + ' · libuv ' + process.versions.uv"
# → 14.6.202.34-node.37 · libuv 1.52.1   (salida real en este PC)
```

💡 Consejo: en producción usa versiones **pares** cuando son **LTS** (Long Term Support: soporte largo, unos 30 meses). Hasta Node 26, las impares viven poco (solo sirven para probar lo nuevo); según el calendario oficial, desde **Node 27** habrá un lanzamiento mayor al año y todos pasarán a LTS.
⚠️ Cuidado: no instales paquetes globales con `sudo npm install -g`; con fnm/nvm todo vive en tu carpeta personal y no necesitas sudo.
🇬🇧 **runtime** /rántaim/ = entorno de ejecución · **non-blocking I/O** /non blóking ái óu/ = entrada/salida no bloqueante · **callback** /kólbak/ = función de retorno · **single-threaded** /síngol zréded/ = de un solo hilo

## 🔁 El event loop: cómo un hilo atiende a miles

![libuv, la librería en C que implementa el event loop de Node (logo oficial, Wikimedia Commons)](img/node/libuv-logo.png)

🧠 Concepto: el **event loop** (bucle de eventos) es un bucle infinito de libuv que pregunta "¿qué terminó?" y ejecuta el callback correspondiente, **uno a la vez**, en el hilo principal. Tu JavaScript nunca corre en paralelo consigo mismo (salvo que uses workers).

🧠 Concepto: el **thread pool** de libuv (4 hilos por defecto, `UV_THREADPOOL_SIZE`) hace en segundo plano lo que el sistema operativo no ofrece de forma asíncrona: archivos (`fs`), `dns.lookup`, `crypto.pbkdf2/scrypt` y `zlib`. Los **sockets de red NO usan el pool**: el kernel avisa con epoll (Linux), kqueue (macOS) o IOCP (Windows).

```secuencia
actores: Tu código, Node/libuv, Thread pool, Disco
Tu código -> Node/libuv : readFile("notas.txt", cb)
Node/libuv -> Thread pool : leer en segundo plano
nota Tu código : sigue ejecutando otras cosas
Thread pool -> Disco : read()
Disco --> Thread pool : bytes
Thread pool --> Node/libuv : listo: encola cb
Node/libuv --> Tu código : (fase poll) ejecuta cb(null, datos)
```

### 🔄 Las fases de cada vuelta

Cada vuelta del loop (un **tick**) pasa por fases en orden. Cada fase tiene su propia cola de callbacks:

```flujo
dir: abajo
timers -> pending -> poll -> check -> close
close --> timers : siguiente vuelta
```

| Fase | Qué ejecuta | Ejemplo |
|---|---|---|
| **timers** | callbacks de timers vencidos | `setTimeout`, `setInterval` |
| **pending** | algunos errores de sistema diferidos | error TCP `ECONNREFUSED` |
| **poll** | E/S lista; aquí el loop **espera** si no hay nada | `fs.readFile`, sockets, `http` |
| **check** | lo programado para "justo después de poll" | `setImmediate` |
| **close** | eventos de cierre | `socket.on("close")` |

📌 Entre **cada callback** (no solo entre fases) Node vacía dos colas de máxima prioridad: primero `process.nextTick` y después las **microtareas** (promesas: `.then`, `await`). Por eso una cadena infinita de promesas también congela el loop.

### ✅ Ejemplo resuelto: ¿en qué orden se imprime?

```js
// orden.cjs — ejecutado con: node orden.cjs
const { readFile } = require("node:fs");

console.log("A. código síncrono");
setTimeout(() => console.log("B. setTimeout 0 (timers)"), 0);
setImmediate(() => console.log("C. setImmediate (check)"));
Promise.resolve().then(() => console.log("D. promesa (microtarea)"));
process.nextTick(() => console.log("E. nextTick"));

readFile(__filename, () => {                       // callback en la fase poll
  setTimeout(() => console.log("F. setTimeout dentro de E/S"), 0);
  setImmediate(() => console.log("G. setImmediate dentro de E/S"));
});
console.log("H. fin del código síncrono");
```

```text
A. código síncrono
H. fin del código síncrono
E. nextTick
D. promesa (microtarea)
B. setTimeout 0 (timers)      ← en 1 de 3 ejecuciones salió C antes que B
C. setImmediate (check)
G. setImmediate dentro de E/S ← SIEMPRE antes que F
F. setTimeout dentro de E/S
```

::: desplegable 🤔 ¿Por qué B y C cambian de orden, pero G siempre va antes que F?
- En el nivel superior, `setTimeout(fn, 0)` en realidad es 1 ms. Si al entrar al loop ya pasó 1 ms, la fase **timers** lo ejecuta (B primero); si no, el loop sigue hasta **check** (C primero). Depende de la velocidad del PC en ese instante.
- Dentro de un callback de E/S estás en la fase **poll**; la siguiente fase es **check**, así que `setImmediate` (G) gana siempre y el timer (F) espera a la próxima vuelta.
- Moraleja: si necesitas "después de la E/S actual", usa `setImmediate`, no `setTimeout(…, 0)`.
:::

⚠️ Cuidado: el mismo archivo como **ESM** (`orden.js` con `import`) imprimió `D` (promesa) **antes** que `E` (nextTick). Un módulo ES se evalúa dentro de una promesa, así que las microtareas se vacían antes de llegar a la cola de nextTick. No escribas código que dependa de ese orden.
💡 Consejo: en código nuevo casi nunca necesitas `process.nextTick`; usa `queueMicrotask()` (estándar, también existe en el navegador) o simplemente `await`.

### 🧱 No bloquees el hilo

Como hay **un solo hilo** para tu JS, cualquier cálculo largo **congela a todos los usuarios**: mientras recorres un array de 10 millones, nadie más recibe respuesta, ni siquiera los timers.

```js
// bloqueo.js — un "latido" cada 100 ms... hasta que alguien bloquea el hilo
const inicio = Date.now();
const t = () => `${String(Date.now() - inicio).padStart(4)} ms`;

const latido = setInterval(() => console.log(`💓 latido a los ${t()}`), 100);

setTimeout(() => {
  console.log(`🧱 empiezo un cálculo síncrono a los ${t()}`);
  let suma = 0;
  for (let i = 0; i < 1e9; i++) suma += i;      // CPU pura: nadie más puede ejecutarse
  console.log(`🧱 termino el cálculo a los ${t()}`);
}, 250);

setTimeout(() => clearInterval(latido), 1800);
```

```text
💓 latido a los  100 ms
💓 latido a los  201 ms
🧱 empiezo un cálculo síncrono a los  251 ms
🧱 termino el cálculo a los 1639 ms
💓 latido a los 1640 ms        ← ¡faltaron 13 latidos!
💓 latido a los 1741 ms
```

| ❌ Bloquea el loop | ✅ Alternativa |
|---|---|
| `fs.readFileSync` en una ruta | `await readFile()` de `node:fs/promises` |
| `crypto.pbkdf2Sync`, `bcrypt.hashSync` | versiones async (van al thread pool) |
| `JSON.parse` de un JSON de 200 MB | streams (procesar por pedazos) |
| bucles de millones de iteraciones | `worker_threads` o un servicio aparte |
| regex con backtracking catastrófico (ReDoS) | regex simples, límites de largo, `re2` |
| `while (Date.now() < fin) {}` para "esperar" | `await setTimeout(ms)` de `node:timers/promises` |

💡 Consejo: los `...Sync` están bien al **arrancar** (leer la config una vez) y en scripts de terminal. En el código que atiende peticiones, nunca.
🇬🇧 **event loop** /ivént lup/ = bucle de eventos · **thread pool** /zred pul/ = grupo de hilos · **microtask** /máikrotask/ = microtarea · **tick** /tik/ = vuelta del bucle · **starvation** /starvéishon/ = inanición (una cola que nunca deja pasar a otra)

## 🔗 Módulos: ESM vs CommonJS

Node tiene **dos** sistemas de módulos porque nació antes de que JavaScript tuviera uno oficial. **CommonJS** (CJS, 2009) usa `require` y `module.exports`, y carga **síncronamente**. **ES Modules** (ESM, estándar ES2015) usa `import`/`export`, es el mismo del navegador y se analiza **antes** de ejecutar (por eso permite tree-shaking y `await` en el nivel superior).

| | ESM (moderno) | CommonJS (heredado) |
|---|---|---|
| Importar | `import fs from "node:fs"` | `const fs = require("node:fs")` |
| Exportar | `export function f() {}` | `module.exports = { f }` |
| Se activa con | `"type": "module"` o `.mjs` | por defecto o `.cjs` |
| `await` arriba del todo | sí | no |
| Carpeta actual | `import.meta.dirname` | `__dirname` |
| Extensión en rutas | obligatoria `./db.js` | opcional `./db` |
| Carga | asíncrona, analizable | síncrona, dinámica |

::: columnas
### 🟦 ESM
```js
// precio.js
export const IVA = 0.13;
export default function conIva(p) {
  return +(p * (1 + IVA)).toFixed(2);
}

// app.js
import conIva, { IVA } from "./precio.js";
console.log(conIva(50), IVA); // 56.5 0.13
```
::: siguiente
### 🟧 CommonJS
```js
// precio.cjs
const IVA = 0.13;
function conIva(p) {
  return +(p * (1 + IVA)).toFixed(2);
}
module.exports = { IVA, conIva };

// app.cjs
const { conIva, IVA } = require("./precio.cjs");
console.log(conIva(50), IVA); // 56.5 0.13
```
:::

- `import { readFile } from "node:fs/promises";` :: Módulo interno (usa siempre el prefijo `node:`)
- `import express from "express";` :: Paquete de npm (lo busca en node_modules)
- `import datos from "./datos.json" with { type: "json" };` :: Importar JSON en ESM
- `const { f } = await import("./plugin.js");` :: Import dinámico (también funciona en CJS)
- `require("./precio.mjs")` :: Node 22.12+ permite `require` de ESM (si no usa top-level await)
- `import { createRequire } from "node:module";` :: Crear un require dentro de ESM (casos raros)

```bash
# Probado en Node 26: un .cjs puede hacer require() de un .mjs
echo 'export const iva = 0.13; export default (p) => +(p*1.13).toFixed(2)' > precio.mjs
echo 'const m = require("./precio.mjs"); console.log(m.iva, m.default(50))' > usa.cjs
node usa.cjs   # → 0.13 56.5
```

⚠️ Cuidado: "Cannot use import statement outside a module" → falta `"type": "module"` en package.json (o renombra a `.mjs`).
⚠️ Cuidado: "require is not defined in ES module scope" → estás en ESM: cambia `require` por `import`, y `__dirname` por `import.meta.dirname`.
💡 Consejo: proyecto nuevo = ESM. Solo verás CJS en código heredado y en configs viejas (`.eslintrc.cjs`, `jest.config.cjs`).
🇬🇧 **module** /módiul/ = módulo · **named export** /neimd ékspórt/ = exportación con nombre · **default export** /difólt ékspórt/ = exportación por defecto · **top-level await** /top lével euéit/ = await en el nivel superior · **tree-shaking** /tri shéiking/ = quitar el código no usado

## 📦 npm, pnpm, yarn y package.json

🧠 Concepto: un **gestor de paquetes** descarga librerías del **registro** (registry) npmjs.com a `node_modules`, resuelve sus dependencias (y las de sus dependencias...) y anota las versiones exactas en un **lockfile**.

```arbol
mi-api/
  package.json — nombre, scripts, rangos de dependencias
  package-lock.json — versiones EXACTAS (sí va a git)
  node_modules/ — lo descargado (NUNCA a git)
    express/
    body-parser/ — dependencia de express (transitiva)
    ...65 paquetes solo por instalar express
  src/
    server.js
  .env — secretos locales (NUNCA a git)
  .env.example — plantilla sin valores (sí a git)
```

📌 Dato real medido aquí: `npm i express` (Express 5.3) dejó **65 paquetes** y 3,8 MB en `node_modules`. Cada uno es código de un desconocido que se ejecuta con tus permisos: por eso importa la seguridad de la cadena de suministro (sección 🛡️).

### 🧰 npm vs pnpm vs yarn

| | npm | pnpm | yarn |
|---|---|---|---|
| Viene con Node | sí | vía `corepack` o instalar | vía `corepack` o instalar |
| Cómo guarda | copia en cada proyecto | **almacén global + enlaces** | copia o Plug'n'Play (Berry) |
| Disco | más | mucho menos | depende del modo |
| Dependencias fantasma | permite | **las prohíbe** (estricto) | PnP las prohíbe |
| Monorepos | workspaces | workspaces (muy usado) | workspaces |
| Lockfile | `package-lock.json` | `pnpm-lock.yaml` | `yarn.lock` |

💡 Consejo: para aprender y en proyectos pequeños, **npm** basta. En monorepos o si tienes muchos proyectos en el disco, **pnpm** ahorra GB y evita importar paquetes que no declaraste. Lo importante: **un solo gestor por proyecto** (no mezcles lockfiles).

- `npm init -y` :: Crea package.json
- `npm i express` :: Instala y guarda en dependencies
- `npm i -D vitest` :: Instala como devDependency (solo desarrollo)
- `npm ci` :: Instalación limpia y EXACTA desde el lock (CI, Docker, servidores)
- `npm ci --omit=dev` :: Solo dependencias de producción
- `npm outdated` :: Qué paquetes tienen versión nueva
- `npm update` :: Actualiza dentro del rango permitido por ^ o ~
- `npm ls express` :: Quién depende de express (árbol)
- `npm explain uuid` :: Por qué está instalado un paquete
- `npx vitest` :: Ejecuta un binario del proyecto (o lo descarga si no está)
- `npm pkg set type=module` :: Cambia un campo de package.json desde la terminal
- `pnpm add express` :: Equivalente en pnpm
- `yarn add express` :: Equivalente en yarn

### 📄 Un package.json bien hecho

```json
{
  "name": "api-libros",
  "version": "1.0.0",
  "type": "module",
  "private": true,
  "engines": { "node": ">=22" },
  "scripts": {
    "dev": "node --watch --env-file-if-exists=.env src/server.js",
    "start": "node src/server.js",
    "test": "node --test",
    "lint": "eslint .",
    "check": "npm run lint && npm test"
  },
  "dependencies": {
    "express": "^5.3.0",
    "zod": "^4.6.7"
  },
  "devDependencies": {
    "vitest": "^5.0.5"
  }
}
```

| Campo | Para qué |
|---|---|
| `type` | `"module"` = los `.js` son ESM |
| `private` | impide publicarlo en npm por accidente |
| `engines` | versión de Node que necesita |
| `scripts` | comandos del proyecto (`npm run dev`) |
| `dependencies` | lo que necesita en producción |
| `devDependencies` | solo para desarrollar: tests, linters, tipos |
| `bin` | convierte tu paquete en un comando de terminal |
| `exports` | qué archivos puede importar quien use tu librería |

### 🔢 Semver: ^ y ~ (probado con el paquete `semver`)

**Semver** = `MAYOR.MENOR.PARCHE`. PARCHE corrige bugs, MENOR añade cosas sin romper, MAYOR puede romper tu código.

| Rango | Acepta | Ejemplo real |
|---|---|---|
| `4.18.2` | exactamente esa | solo 4.18.2 |
| `~4.18.2` | parches | 4.18.9 sí · 4.19.0 no |
| `^4.18.2` | menores y parches (por defecto) | 4.99.0 sí · 5.0.0 no |
| `^0.2.3` | en 0.x, ^ se comporta como ~ | 0.2.9 sí · 0.3.0 no |
| `^0.0.3` | en 0.0.x, solo esa | 0.0.4 no |
| `*` o `latest` | cualquiera | evítalo |

```bash
npx semver -r "^4.18.2" 4.18.9 4.19.0 4.99.0 5.0.0
# → 4.18.9 4.19.0 4.99.0        (5.0.0 queda fuera)
npx semver -r "^0.2.3" 0.2.9 0.3.0
# → 0.2.9                        (en 0.x un menor PUEDE romper)
```

### ▶️ Scripts

- `npm run dev` :: Ejecuta el script "dev"
- `npm start / npm test` :: Atajos sin "run"
- `node --run dev` :: Ejecuta el script sin cargar npm (más rápido, Node 22+)
- `"pretest": "npm run lint"` :: Script `pre...` que corre antes de test
- `npm run test -- --watch` :: Lo que va tras `--` se pasa al comando

💡 Consejo: dentro de los scripts, los binarios de `node_modules/.bin` están en el PATH: escribe `"test": "vitest"`, no `"npx vitest"`.
⚠️ Cuidado: si tu servidor importa un paquete que pusiste en devDependencies, el despliegue con `npm ci --omit=dev` fallará con "Cannot find package".
🇬🇧 **package manager** /pákech mánayer/ = gestor de paquetes · **lockfile** /lókfail/ = archivo de versiones fijadas · **transitive dependency** /tránsitiv dipéndensi/ = dependencia de una dependencia · **breaking change** /bréiking chéinch/ = cambio que rompe · **registry** /réyistri/ = registro de paquetes

## 📁 Archivos, rutas y sistema: fs, path, os

🧠 Concepto: **fs** (file system) lee y escribe archivos; **path** arma rutas que funcionan en Linux (`/`) y Windows (`\`); **os** da datos de la máquina. Usa `node:fs/promises` con `await`: el trabajo va al thread pool y el loop sigue libre.

```js
// archivos.js — fs/promises + path + os (ejecutado en este PC)
import { mkdir, writeFile, readFile, readdir, stat, rm } from "node:fs/promises";
import path from "node:path";
import os from "node:os";

const base = path.join(import.meta.dirname, "datos");       // carpeta junto a ESTE archivo
await mkdir(base, { recursive: true });                      // no falla si ya existe

const notas = [{ materia: "Cálculo", nota: 78 }, { materia: "Redes", nota: 91 }];
await writeFile(path.join(base, "notas.json"), JSON.stringify(notas, null, 2));

const leidas = JSON.parse(await readFile(path.join(base, "notas.json"), "utf8"));
console.log("Promedio:", leidas.reduce((s, n) => s + n.nota, 0) / leidas.length);

for (const nombre of await readdir(base)) {
  const info = await stat(path.join(base, nombre));
  console.log(`${nombre} → ${info.size} bytes, ext ${path.extname(nombre)}`);
}

try {
  await readFile(path.join(base, "no-existe.txt"), "utf8");
} catch (err) {
  console.log("Error esperado:", err.code);                  // ENOENT
}

console.log("Sistema:", os.platform(), os.arch(), `${os.cpus().length} núcleos`,
  `${(os.totalmem() / 1024 ** 3).toFixed(1)} GB RAM`);
await rm(base, { recursive: true, force: true });            // limpiar
```

```text
Promedio: 84.5
notas.json → 101 bytes, ext .json
Error esperado: ENOENT
Sistema: linux x64 8 núcleos 23.4 GB RAM
```

- `await readFile(ruta, "utf8")` :: Leer texto (sin "utf8" devuelve un Buffer)
- `await writeFile(ruta, texto)` :: Escribir (reemplaza)
- `await appendFile(ruta, "línea\n")` :: Añadir al final
- `await readdir(dir, { withFileTypes: true })` :: Listar con `e.isFile()` / `e.isDirectory()`
- `await mkdir(dir, { recursive: true })` :: Crear carpetas anidadas
- `await rm(dir, { recursive: true, force: true })` :: Borrar carpeta completa
- `await cp("a", "b", { recursive: true })` :: Copiar carpetas
- `fs.watch(dir, cb)` :: Avisar cuando algo cambia
- `path.join(a, b, c)` :: Unir partes de ruta
- `path.resolve("datos")` :: Ruta absoluta desde la carpeta actual
- `path.basename(r) / path.extname(r) / path.dirname(r)` :: Nombre / extensión / carpeta
- `import.meta.dirname` :: Carpeta del archivo actual (ESM)
- `process.cwd()` :: Carpeta DESDE donde ejecutaste node
- `os.homedir() / os.tmpdir()` :: Carpeta personal / temporal
- `os.availableParallelism()` :: Núcleos útiles (para workers/cluster)

| Código | Significa |
|---|---|
| `ENOENT` | no existe el archivo o carpeta |
| `EACCES` / `EPERM` | sin permisos |
| `EEXIST` | ya existe |
| `EISDIR` | es carpeta, esperabas archivo |
| `EMFILE` | demasiados archivos abiertos a la vez |
| `EADDRINUSE` | puerto ocupado (servidores) |

⚠️ Cuidado: una ruta relativa como `"datos/x.json"` se resuelve desde `process.cwd()`, NO desde tu archivo. Si ejecutas `node src/app.js` desde otra carpeta, falla. Usa `path.join(import.meta.dirname, ...)`.
⚠️ Cuidado: **path traversal**: si un usuario manda `../../etc/passwd` y haces `path.join(carpeta, nombre)`, se escapa de la carpeta. Comprueba que `path.resolve(carpeta, nombre)` empiece con `path.resolve(carpeta) + path.sep`.
🇬🇧 **file system** /fáil sístem/ = sistema de archivos · **path** /paz/ = ruta · **working directory** /uérking dairéktori/ = carpeta de trabajo · **path traversal** /paz travérsal/ = escaparse de una carpeta con ../

## ⚙️ process y variables de entorno (.env)

🧠 Concepto: `process` es el objeto global del programa en ejecución: argumentos (`argv`), **variables de entorno** (`env`), señales del sistema y código de salida (0 = bien, otro = error).

🧠 Concepto: una **variable de entorno** es un par NOMBRE=valor que el sistema le pasa al proceso. Es la forma estándar (metodología "12-factor app") de dar configuración y **secretos** sin escribirlos en el código.

- `process.argv.slice(2)` :: Tus argumentos (`node app.js hola 3` → `["hola", "3"]`)
- `parseArgs({ options })` :: Opciones tipo `--puerto 3000 -v` (de `node:util`)
- `process.env.PORT` :: Leer una variable (SIEMPRE string o undefined)
- `process.exitCode = 1` :: Marcar error y dejar que termine solo
- `process.exit(1)` :: Salir YA (corta lo pendiente: úsalo poco)
- `process.on("SIGTERM", fn)` :: Te piden apagarte (Docker, PM2, systemd)
- `process.memoryUsage()` :: RSS, heap usado...
- `process.uptime()` :: Segundos desde que arrancó
- `node --env-file=.env app.js` :: Carga un .env sin instalar dotenv
- `node --env-file-if-exists=.env app.js` :: Igual, pero no falla si no existe
- `process.loadEnvFile(".env")` :: Cargar el .env desde el código
- `NODE_ENV=production node app.js` :: Variable solo para este comando (bash)

```bash
# .env — añádelo a .gitignore (valores de ejemplo, no reales)
PORT=38080
NODE_ENV=development
JWT_SECRET=cambia_esto_por_algo_largo
DEBUG=false
```

### ✅ Ejemplo resuelto: configuración validada al arrancar

```js
// config.js — lee y valida el entorno UNA vez; si falta algo, falla rápido y claro
function requerida(nombre) {
  const valor = process.env[nombre];
  if (!valor) throw new Error(`Falta la variable de entorno ${nombre} (revisa tu .env)`);
  return valor;
}

export const config = Object.freeze({
  port: Number(process.env.PORT ?? 3000),
  produccion: process.env.NODE_ENV === "production",
  debug: process.env.DEBUG === "true",           // "false" es un string truthy: compara
  jwtSecret: requerida("JWT_SECRET"),
});

console.log(config.port, typeof config.port, config.debug, Boolean(process.env.DEBUG));
```

```bash
node --env-file=.env config.js
# → 38080 number false true      ← Boolean("false") es true: por eso se compara con "true"
node config.js
# → Error: Falta la variable de entorno JWT_SECRET (revisa tu .env)
```

```flujo
.env.example -> .env : copias y rellenas
.env -> process.env : --env-file
Panel del hosting -> process.env : en producción
process.env -> config.js : valida una vez
config.js -> Tu app : importa config
```

⚠️ Cuidado: subir un `.env` a GitHub y luego borrarlo **no basta**: queda en el historial y hay bots que escanean GitHub buscando claves en minutos. **Rota** (cambia) la clave de inmediato.
💡 Consejo: lee `process.env` en un solo archivo (`config.js`) y valida ahí (a mano o con zod). El resto del código importa `config`, nunca `process.env` suelto.
🇬🇧 **environment variable** /enváironment vérieibol/ = variable de entorno · **secret** /síkret/ = secreto · **to rotate a key** /tu routéit a ki/ = cambiar una clave comprometida · **exit code** /éksit kóud/ = código de salida · **signal** /sígnal/ = señal

## 🌍 Servidor HTTP nativo (sin dependencias)

🧠 Concepto: el módulo `node:http` crea servidores sin instalar nada. Por cada petición recibes `req` (método, URL, cabeceras y un **stream** con el cuerpo) y `res` (donde escribes código, cabeceras y cuerpo). Express, Fastify y casi todos los frameworks están construidos encima.

```secuencia
Cliente -> Servidor : POST /frases + JSON
nota Servidor : req = stream con el body
Servidor -> Servidor : junta chunks y JSON.parse
Servidor --> Cliente : 201 + {"ok":true}
```

```js
// nativo.js — servidor HTTP sin ninguna dependencia
import http from "node:http";

const frases = ["Poco a poco se anda lejos", "El que madruga, Dios lo ayuda"];

const enviar = (res, codigo, datos) => {
  res.writeHead(codigo, { "Content-Type": "application/json; charset=utf-8" });
  res.end(JSON.stringify(datos));
};

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);   // ruta + query

  if (req.method === "GET" && url.pathname === "/frases") {
    const limite = Number(url.searchParams.get("limite") ?? frases.length);
    return enviar(res, 200, frases.slice(0, limite));
  }
  if (req.method === "POST" && url.pathname === "/frases") {
    let cuerpo = "";
    for await (const chunk of req) cuerpo += chunk;             // el body llega por pedazos
    try {
      const { texto } = JSON.parse(cuerpo || "{}");
      if (typeof texto !== "string" || !texto.trim()) return enviar(res, 400, { error: "Falta texto" });
      frases.push(texto.trim());
      return enviar(res, 201, { ok: true, total: frases.length });
    } catch {
      return enviar(res, 400, { error: "JSON inválido" });
    }
  }
  enviar(res, 404, { error: `No existe ${req.method} ${url.pathname}` });
});

const PORT = Number(process.env.PORT ?? 3000);
server.listen(PORT, () => console.log(`🚀 http://localhost:${PORT}`));
```

```bash
PORT=38081 node nativo.js &
curl -s "localhost:38081/frases?limite=1"
# → ["Poco a poco se anda lejos"]
curl -s -X POST localhost:38081/frases -H "Content-Type: application/json" -d '{"texto":"Más vale tarde que nunca"}'
# → {"ok":true,"total":3}
curl -s -X POST localhost:38081/frases -d '{roto'
# → {"error":"JSON inválido"}
curl -s localhost:38081/otra
# → {"error":"No existe GET /otra"}
kill %1     # cerrar el servidor
```

::: columnas
### ✅ Bueno para
- Entender HTTP de verdad
- Microservicios diminutos, health checks
- Cero dependencias (cero riesgo de supply chain)
::: siguiente
### ❌ Te faltará
- Rutas con parámetros (`/libros/:id`)
- Middlewares, validación, cookies
- Límite de tamaño del body (¡alguien te manda 2 GB!)
:::

- `http.createServer((req, res) => {})` :: Crear el servidor
- `server.listen(puerto, cb)` :: Empezar a escuchar
- `req.method / req.url / req.headers` :: Método, ruta con query, cabeceras (en minúsculas)
- `new URL(req.url, "http://x")` :: Separar `pathname` y `searchParams`
- `res.writeHead(201, { ... })` :: Código y cabeceras
- `res.end(texto)` :: Enviar y cerrar la respuesta
- `server.close(cb)` :: Dejar de aceptar conexiones (apagado elegante)

⚠️ Cuidado: "EADDRINUSE: address already in use" = el puerto está ocupado (seguramente tu servidor anterior sigue vivo). `ss -ltnp | grep 3000` te dice qué proceso lo usa.
🇬🇧 **request** /rikuést/ = petición · **response** /rispóns/ = respuesta · **header** /jéder/ = cabecera · **status code** /stéitus kóud/ = código de estado · **to listen** /tu lísen/ = escuchar (un puerto)

## 🚂 Express a fondo: rutas, middlewares y errores

![Logo de Express (Wikimedia Commons)](img/node/express-logo.png)

🧠 Concepto: **Express** es el framework web más usado de Node (desde 2010). Es **minimalista**: te da rutas, un sistema de **middlewares** y helpers (`res.json`, `req.params`), y el resto lo eliges tú. **Express 5** (estable desde 2024) pasa automáticamente los errores de funciones `async` al manejador de errores.

🧠 Concepto: un **middleware** es una función `(req, res, next)` que se ejecuta en cadena. Puede **leer/modificar** `req` y `res`, **responder** (y cortar la cadena) o llamar a `next()` para pasar al siguiente. Llamar `next(err)` salta directo al manejador de errores.

```flujo
dir: abajo
Petición -> express.json -> log -> auth
auth -> Ruta : next()
auth --> Respuesta : 401 corta la cadena
Ruta -> Respuesta : res.json()
Ruta --> Errores : throw o next(err)
Errores -> Respuesta : 500 genérico
```

📌 Analogía: la petición entra a un edificio. Recepción la registra (log), seguridad revisa el carnet (auth) y recién llega a la oficina (la ruta). Cualquiera puede detenerla en el camino. El **orden** en que haces `app.use` es el orden de los controles.

### ✅ Ejemplo resuelto: rutas, parámetros y middlewares

```js
// basico.js — rutas, parámetros y middlewares en Express 5
import express from "express";

const app = express();
app.use(express.json());                                   // 1. body JSON → req.body

app.use((req, res, next) => {                              // 2. middleware global: log
  const t0 = performance.now();
  res.on("finish", () =>
    console.log(`${req.method} ${req.originalUrl} → ${res.statusCode} (${(performance.now() - t0).toFixed(1)} ms)`));
  next();                                                  // ¡sin next() la petición se cuelga!
});

function soloConClave(req, res, next) {                    // 3. middleware de ruta: "seguridad"
  if (req.get("x-api-key") !== "clave_de_prueba") return res.status(401).json({ error: "Sin clave" });
  req.usuario = { nombre: "admin" };                       // los middlewares pueden "decorar" req
  next();
}

app.get("/saludo/:nombre", (req, res) => {
  const { nombre } = req.params;                           // /saludo/Ana
  const { idioma = "es" } = req.query;                     // ?idioma=en
  res.json({ mensaje: idioma === "en" ? `Hello, ${nombre}` : `Hola, ${nombre}` });
});
app.post("/eco", (req, res) => res.status(201).json({ recibido: req.body }));
app.get("/admin", soloConClave, (req, res) => res.json({ hola: req.usuario.nombre }));
app.get("/falla", async () => {
  await new Promise((r) => setTimeout(r, 10));
  throw new Error("La BD explotó");                        // Express 5 atrapa errores async
});

app.use((req, res) => res.status(404).json({ error: `No existe ${req.method} ${req.path}` }));
app.use((err, req, res, next) => {                         // 4 parámetros = manejador de errores
  console.error("💥", err.message);
  res.status(500).json({ error: "Error interno" });
});

app.listen(Number(process.env.PORT ?? 3000), () => console.log("🚂 Express listo"));
```

```bash
curl -s "localhost:38084/saludo/Ana?idioma=en"        # → {"mensaje":"Hello, Ana"}
curl -s -X POST localhost:38084/eco -H "Content-Type: application/json" -d '{"curso":"Node"}'
                                                       # → {"recibido":{"curso":"Node"}}
curl -s localhost:38084/admin                          # → {"error":"Sin clave"}
curl -s -H "x-api-key: clave_de_prueba" localhost:38084/admin   # → {"hola":"admin"}
curl -s localhost:38084/falla                          # → {"error":"Error interno"}
curl -s localhost:38084/nada                           # → {"error":"No existe GET /nada"}
# Y en la terminal del servidor (log del middleware):
# GET /saludo/Ana?idioma=en → 200 (11.4 ms)
# GET /admin → 401 (0.6 ms)
# 💥 La BD explotó
# GET /falla → 500 (11.0 ms)
```

### 🧾 Referencia rápida

- `app.use(express.json({ limit: "100kb" }))` :: Leer body JSON con límite de tamaño
- `app.use(express.static("public"))` :: Servir HTML/CSS/JS/imágenes
- `app.get/post/put/patch/delete(ruta, ...fns)` :: Definir rutas (varias fns = middlewares de ruta)
- `req.params.id` :: `/libros/:id` → `/libros/7`
- `req.query.q` :: `/buscar?q=hola` (siempre strings)
- `req.body` :: Cuerpo (necesita `express.json()`)
- `req.get("Authorization")` :: Leer una cabecera
- `res.status(201).json(obj)` :: Código + JSON
- `res.sendStatus(204)` :: Solo el código
- `res.location(url)` :: Cabecera Location (tras crear algo)
- `res.cookie("sid", valor, { httpOnly: true })` :: Poner una cookie
- `const r = express.Router()` :: Agrupar rutas de un recurso
- `app.use("/api/libros", r)` :: Montar un router con prefijo
- `app.use((err, req, res, next) => {})` :: Manejador de errores (4 parámetros, al final)
- `app.disable("x-powered-by")` :: No anunciar que usas Express
- `app.get("/*splat", fn)` :: Comodín en Express 5 (en Express 4 era `*`)

### ✅ Validación: nunca confíes en `req.body`

🧠 Concepto: **validar** = comprobar tipo, forma y rango de los datos que llegan **antes** de usarlos. **zod** describe el esquema una vez y te devuelve datos limpios o una lista de errores (y con TypeScript, también el tipo).

```js
import { z } from "zod";

const LibroSchema = z.object({
  titulo: z.string().trim().min(1, "titulo es obligatorio").max(200),
  autor: z.string().trim().min(1, "autor es obligatorio"),
  anio: z.number().int().min(0).max(new Date().getFullYear()),
  leido: z.boolean().default(false),
});

// Middleware reutilizable: valida y reemplaza req.body por los datos limpios
const validar = (schema) => (req, res, next) => {
  const r = schema.safeParse(req.body ?? {});
  if (!r.success) {
    const detalles = r.error.issues.map((i) => `${i.path.join(".") || "body"}: ${i.message}`);
    return next(new HttpError(400, "Datos inválidos", detalles));
  }
  req.body = r.data;
  next();
};
// Uso: app.post("/api/libros", validar(LibroSchema), crearLibro)
```

| Alternativa | Idea |
|---|---|
| **zod** | esquemas en JS/TS, infiere tipos; el más popular hoy |
| **valibot** | como zod pero modular y más pequeño |
| **joi** | clásico del mundo hapi/Express |
| **JSON Schema** (ajv) | estándar; Fastify lo usa de serie |

⚠️ Cuidado: si `req.body` sale `undefined`, falta `app.use(express.json())` o el cliente no mandó `Content-Type: application/json`.
⚠️ Cuidado: "Cannot set headers after they are sent to the client" = respondiste dos veces. Escribe `return res.status(...).json(...)` para cortar la función.
⚠️ Cuidado: el manejador de errores debe tener **exactamente 4 parámetros** aunque no uses `next`; con 3, Express lo trata como middleware normal.
🇬🇧 **middleware** /mídoluer/ = función intermedia · **route handler** /rut jándler/ = manejador de ruta · **to validate** /tu válideit/ = validar · **schema** /skíma/ = esquema · **error handler** /érror jándler/ = manejador de errores

## 📚 API REST completa: CRUD de libros probado con curl

🧠 Concepto: **REST** (Representational State Transfer) organiza una API por **recursos** (libros, usuarios) con URLs en plural, y el **método HTTP** dice la acción. **CRUD** = Create, Read, Update, Delete.

| Método | Ruta | Acción | Respuesta |
|---|---|---|---|
| GET | `/api/libros?leido=true&q=raza` | listar con filtros | 200 + array |
| GET | `/api/libros/:id` | ver uno | 200 o 404 |
| POST | `/api/libros` | crear | 201 + Location + libro |
| PUT | `/api/libros/:id` | reemplazar completo | 200 o 400/404 |
| PATCH | `/api/libros/:id` | cambiar algunos campos | 200 o 400/404 |
| DELETE | `/api/libros/:id` | borrar | 204 sin cuerpo |

```arbol
api-libros/
  package.json — "type": "module"
  src/
    app.js — crea la app, middlewares y rutas (exporta app)
    server.js — solo hace app.listen y el apagado elegante
  test/
    libros.test.js — node --test test/libros.test.js
    libros.spec.js — vitest run test/libros.spec.js
```

💡 Consejo: separar `app.js` (la app) de `server.js` (el `listen`) permite **testear** la app sin abrir un puerto fijo.

### 🧩 src/app.js

```js
// src/app.js — crea la app (sin listen) para poder testearla
// npm i express helmet express-rate-limit zod
import express from "express";
import helmet from "helmet";
import { rateLimit } from "express-rate-limit";
import { z } from "zod";

// ---------- "Base de datos" en memoria (luego: Postgres) ----------
const libros = new Map([
  [1, { id: 1, titulo: "Cien años de soledad", autor: "García Márquez", anio: 1967, leido: true }],
  [2, { id: 2, titulo: "Raza de bronce", autor: "Alcides Arguedas", anio: 1919, leido: false }],
]);
let siguienteId = 3;

// ---------- Errores con código HTTP ----------
export class HttpError extends Error {
  constructor(status, message, detalles) {
    super(message);
    this.status = status;
    this.detalles = detalles;
  }
}

// ---------- Validación con zod ----------
const LibroSchema = z.object({
  titulo: z.string().trim().min(1, "titulo es obligatorio").max(200),
  autor: z.string().trim().min(1, "autor es obligatorio"),
  anio: z.number().int().min(0).max(new Date().getFullYear()),
  leido: z.boolean().default(false),
});
const validar = (schema) => (req, res, next) => {
  const r = schema.safeParse(req.body ?? {});
  if (!r.success) {
    const detalles = r.error.issues.map((i) => `${i.path.join(".") || "body"}: ${i.message}`);
    return next(new HttpError(400, "Datos inválidos", detalles));
  }
  req.body = r.data;                       // datos ya limpios (trim, default...)
  next();
};
const buscar = (id) => {
  const libro = libros.get(Number(id));
  if (!libro) throw new HttpError(404, `No existe el libro ${id}`);
  return libro;
};

// ---------- App y middlewares globales (el orden importa) ----------
export const app = express();
app.disable("x-powered-by");
app.use((req, res, next) => {                         // log: método, ruta, código, duración
  const t0 = performance.now();
  res.on("finish", () => {
    if (process.env.NODE_ENV !== "test")
      console.log(`${req.method} ${req.originalUrl} → ${res.statusCode} (${(performance.now() - t0).toFixed(1)} ms)`);
  });
  next();
});
app.use(helmet());                                    // cabeceras de seguridad
app.use(rateLimit({ windowMs: 60_000, limit: 100 }));  // 100 peticiones/minuto por IP
app.use(express.json({ limit: "100kb" }));            // body JSON → req.body

// ---------- Rutas CRUD ----------
const r = express.Router();

r.get("/", (req, res) => {                            // LISTAR con filtros ?leido=true&q=raza
  let lista = [...libros.values()];
  if (req.query.leido) lista = lista.filter((l) => String(l.leido) === req.query.leido);
  if (req.query.q) {
    const q = String(req.query.q).toLowerCase();
    lista = lista.filter((l) => l.titulo.toLowerCase().includes(q));
  }
  res.json(lista);
});
r.get("/:id", (req, res) => res.json(buscar(req.params.id)));               // VER UNO
r.post("/", validar(LibroSchema), (req, res) => {                            // CREAR
  const libro = { id: siguienteId++, ...req.body };
  libros.set(libro.id, libro);
  res.status(201).location(`/api/libros/${libro.id}`).json(libro);
});
r.put("/:id", validar(LibroSchema), (req, res) => {                         // REEMPLAZAR
  const { id } = buscar(req.params.id);
  const libro = { id, ...req.body };
  libros.set(id, libro);
  res.json(libro);
});
r.patch("/:id", validar(LibroSchema.partial()), (req, res) => {             // CAMBIAR ALGO
  const libro = buscar(req.params.id);
  Object.assign(libro, req.body);                     // solo campos que pasaron zod
  res.json(libro);
});
r.delete("/:id", (req, res) => {                                             // BORRAR
  buscar(req.params.id);
  libros.delete(Number(req.params.id));
  res.sendStatus(204);
});

app.use("/api/libros", r);
app.get("/health", (req, res) => res.json({ ok: true, uptime: Math.round(process.uptime()) }));

// ---------- 404 y manejador de errores (SIEMPRE al final) ----------
app.use((req, res) => res.status(404).json({ error: `No existe ${req.method} ${req.path}` }));
app.use((err, req, res, next) => {
  if (err.type === "entity.parse.failed") err = new HttpError(400, "JSON mal formado");
  const status = err.status ?? 500;
  if (status >= 500) console.error("💥", err);        // el detalle va al log, no al cliente
  res.status(status).json({
    error: status >= 500 ? "Error interno" : err.message,
    ...(err.detalles && { detalles: err.detalles }),
  });
});
```

### 🧩 src/server.js

```js
// src/server.js — arranca el servidor y lo apaga con elegancia
import { app } from "./app.js";

const PORT = Number(process.env.PORT ?? 3000);
const server = app.listen(PORT, () => console.log(`📚 API en http://localhost:${PORT}/api/libros`));

for (const senal of ["SIGINT", "SIGTERM"]) {
  process.on(senal, () => {
    console.log(`\n${senal} recibido: cierro conexiones...`);
    server.close(() => process.exit(0));            // deja terminar las peticiones en curso
  });
}
```

### 🧪 Probada con curl (salidas reales)

```bash
PORT=38082 node src/server.js &
H='Content-Type: application/json'

curl -s localhost:38082/api/libros
# → [{"id":1,"titulo":"Cien años de soledad",...,"leido":true},{"id":2,"titulo":"Raza de bronce",...}]
curl -s "localhost:38082/api/libros?leido=false"
# → [{"id":2,"titulo":"Raza de bronce","autor":"Alcides Arguedas","anio":1919,"leido":false}]

curl -s -i -X POST localhost:38082/api/libros -H "$H" \
  -d '{"titulo":"  Juan de la Rosa ","autor":"Nataniel Aguirre","anio":1885}'
# → HTTP/1.1 201 Created
# → Location: /api/libros/3
# → {"id":3,"titulo":"Juan de la Rosa","autor":"Nataniel Aguirre","anio":1885,"leido":false}

curl -s -X POST localhost:38082/api/libros -H "$H" -d '{"titulo":"","anio":"mil"}'
# → {"error":"Datos inválidos","detalles":["titulo: titulo es obligatorio",
#    "autor: Invalid input: expected string, received undefined",
#    "anio: Invalid input: expected number, received string"]}

curl -s -X POST localhost:38082/api/libros -H "$H" -d '{titulo:'
# → {"error":"JSON mal formado"}

curl -s -X PATCH localhost:38082/api/libros/3 -H "$H" -d '{"leido":true}'
# → {"id":3,"titulo":"Juan de la Rosa","autor":"Nataniel Aguirre","anio":1885,"leido":true}

curl -s -i -X DELETE localhost:38082/api/libros/1 | head -1
# → HTTP/1.1 204 No Content
curl -s localhost:38082/api/libros/1
# → {"error":"No existe el libro 1"}

curl -s -I localhost:38082/health | grep -iE "content-security|nosniff|ratelimit-limit"
# → Content-Security-Policy: default-src 'self';base-uri 'self';...   (helmet)
# → X-Content-Type-Options: nosniff                                     (helmet)
# → X-RateLimit-Limit: 100                                              (rate limit)

kill %1
```

```text
📚 API en http://localhost:38082/api/libros
GET /api/libros → 200 (5.0 ms)
GET /api/libros?leido=false → 200 (0.6 ms)
POST /api/libros → 201 (2.2 ms)
POST /api/libros → 400 (1.2 ms)
PATCH /api/libros/3 → 200 (0.9 ms)
DELETE /api/libros/1 → 204 (0.5 ms)
GET /api/libros/1 → 404 (0.4 ms)
```

::: desplegable 🤔 ¿Por qué el PATCH no deja cambiar el id?
Porque `LibroSchema.partial()` solo conoce `titulo`, `autor`, `anio` y `leido`; zod **descarta** las claves que no están en el esquema (`{ "id": 999 }` desaparece). Si hicieras `Object.assign(libro, req.body)` con el body crudo, un cliente podría cambiar `id`, `rol` o `esAdmin`: es la vulnerabilidad **mass assignment** (asignación masiva).
:::

⚠️ Cuidado: si pruebas el apagado elegante con `kill -INT %1` en un script, no funciona: los procesos en segundo plano de un shell no interactivo **ignoran SIGINT**. Usa `kill %1` (SIGTERM), que es lo que envían Docker y PM2.
💡 Consejo: sustantivos en plural para las rutas (`/api/libros`), nunca verbos (`/api/crearLibro`): el verbo ya lo pone el método HTTP. Versiona si la API es pública: `/api/v1/libros`.
🇬🇧 **resource** /rísors/ = recurso · **endpoint** /éndpoint/ = punto de la API · **payload** /péilóud/ = datos enviados · **mass assignment** /mas asáinment/ = asignación masiva · **graceful shutdown** /gréisful shátdaun/ = apagado elegante

## ⚖️ Express vs Fastify vs NestJS vs Hono vs Koa

Todos hacen lo mismo (rutas → respuesta). Cambian en **filosofía**, **rendimiento**, **estructura** y **dónde corren**.

| Framework | Estilo | Fuerte en | Débil en |
|---|---|---|---|
| **Express** | minimalista, middlewares | ecosistema enorme, tutoriales | más lento, poca estructura |
| **Fastify** | plugins + JSON Schema | rendimiento, validación y logs de serie | ecosistema menor que Express |
| **NestJS** | arquitectura tipo Angular (TS) | equipos grandes, módulos, DI | curva y "ceremonia" para apps chicas |
| **Hono** | Web Standards (`Request`/`Response`) | corre en Node, Bun, Deno, Cloudflare Workers | más joven |
| **Koa** | middlewares `async` en "cebolla" | elegante y mínimo (del equipo original de Express) | poca actividad hoy |

::: columnas
### ⚡ Fastify
```js
import Fastify from "fastify";
const app = Fastify({ logger: true });

app.get("/libros/:id", {
  schema: { params: { type: "object",
    properties: { id: { type: "integer" } } } },
}, async (req) => ({ id: req.params.id }));

await app.listen({ port: 3000 });
```
::: siguiente
### 🔥 Hono
```js
import { Hono } from "hono";
import { serve } from "@hono/node-server";
const app = new Hono();

app.get("/libros/:id", (c) =>
  c.json({ id: Number(c.req.param("id")) }));

serve({ fetch: app.fetch, port: 3000 });
// el MISMO app.fetch sirve en Workers o Bun
```
:::

```js
// NestJS (TypeScript): controladores con decoradores e inyección de dependencias
@Controller("libros")
export class LibrosController {
  constructor(private readonly libros: LibrosService) {}   // DI: Nest crea el servicio

  @Get(":id")
  uno(@Param("id", ParseIntPipe) id: number) {
    return this.libros.buscar(id);
  }
}
```

### 📊 Benchmark medido en este PC

Mismo endpoint `GET /` que responde `{"hola":"mundo"}`, un solo proceso, `autocannon -c 50 -d 6`, Node 26.11, Express 5.3, Fastify 5.12, Hono 4.13:

```grafica
tipo: barras
titulo: Peticiones por segundo (más es mejor) — medido en este PC, oct 2026
unidad: req/s
node:http : 46309
Fastify : 47563
Hono : 40252
Express : 23325
```

📌 Interpretación honesta: en un "hola mundo" Express atiende la mitad que Fastify; pero en una API real el cuello de botella suele ser la **base de datos** (milisegundos), no el framework (microsegundos). Elige por equipo y ecosistema primero, rendimiento después.

| Situación | Elige | Por qué no otro |
|---|---|---|
| Aprender / proyecto de clase | Express | todo tutorial lo usa; Nest sería demasiada estructura |
| API con mucho tráfico y JSON | Fastify | validación + serialización rápidas de serie |
| Empresa, equipo de 10+, TypeScript | NestJS | módulos y convenciones evitan el caos |
| Edge / serverless / multi-runtime | Hono | Express depende de `node:http` |
| Mantener código heredado | Express o Koa | reescribir rara vez compensa |

💡 Consejo: frameworks "full stack" como **Next.js**, **Nuxt**, **Remix/React Router** o **SvelteKit** también corren sobre Node y ya traen su backend (route handlers, server actions). Si tu backend solo sirve a tu frontend, quizá no necesites un Express aparte.
🇬🇧 **benchmark** /bénchmark/ = prueba de rendimiento · **throughput** /zrúput/ = peticiones atendidas por segundo · **dependency injection** /dipéndensi inyékshon/ = inyección de dependencias · **boilerplate** /bóilerpleit/ = código repetitivo de plantilla

## 🗄️ Bases de datos: pg, Prisma, Drizzle

Un array en memoria se pierde al reiniciar y no se comparte entre procesos. Para datos de verdad usa una base de datos; en Node las opciones van de **SQL a mano** a **ORM** completos.

```capas
ORM (Prisma) : modelos y métodos — prisma.libro.findMany()
Query builder (Drizzle, Kysely) : SQL con tipos — db.select().from(libros)
Driver (pg, mysql2) : SQL a mano — pool.query("SELECT...", [id])
Base de datos : PostgreSQL, MySQL, SQLite
```

| | pg (driver) | Drizzle | Prisma |
|---|---|---|---|
| Escribes | SQL puro | TS que se parece a SQL | API propia + schema.prisma |
| Tipos TS | a mano | inferidos del esquema | generados (`prisma generate`) |
| Migraciones | aparte | `drizzle-kit` | `prisma migrate` |
| Control del SQL | total | alto | menor |
| Ideal para | aprender, consultas finas | apps TS modernas, serverless | productividad, equipos |

### 🐘 pg: SQL a mano con pool y parámetros

```js
// npm i pg   ·   .env → DATABASE_URL=postgres://app:cambia_esto@localhost:5432/biblioteca
import pg from "pg";

export const pool = new pg.Pool({ connectionString: process.env.DATABASE_URL, max: 10 });

export async function buscarLibros(texto) {
  // $1 = parámetro: el driver lo envía APARTE del SQL → sin inyección SQL
  const { rows } = await pool.query(
    "SELECT id, titulo, anio FROM libros WHERE titulo ILIKE $1 ORDER BY anio",
    [`%${texto}%`]
  );
  return rows;
}

// Transacción: o se hacen las dos cosas, o ninguna
export async function prestar(libroId, usuarioId) {
  const cliente = await pool.connect();
  try {
    await cliente.query("BEGIN");
    await cliente.query("UPDATE libros SET disponible = false WHERE id = $1", [libroId]);
    await cliente.query("INSERT INTO prestamos (libro_id, usuario_id) VALUES ($1, $2)", [libroId, usuarioId]);
    await cliente.query("COMMIT");
  } catch (err) {
    await cliente.query("ROLLBACK");
    throw err;
  } finally {
    cliente.release();                    // ¡devolver la conexión al pool SIEMPRE!
  }
}
```

### 🔺 Prisma

```text
// prisma/schema.prisma
model Libro {
  id     Int     @id @default(autoincrement())
  titulo String
  anio   Int
  leido  Boolean @default(false)
}
```

```js
// Prisma 6 o anterior. En Prisma 7 el cliente se genera dentro de tu proyecto
// (generator "prisma-client" con output) y se crea con un adaptador de driver:
// new PrismaClient({ adapter: new PrismaPg({ connectionString }) }). Mira su guía de migración.
import { PrismaClient } from "@prisma/client";
const prisma = new PrismaClient();

const recientes = await prisma.libro.findMany({
  where: { anio: { gte: 1900 }, leido: false },
  orderBy: { anio: "desc" },
  take: 10,
});
```

### 💧 Drizzle

```js
import { pgTable, serial, text, integer, boolean } from "drizzle-orm/pg-core";
import { drizzle } from "drizzle-orm/node-postgres";
import { and, gte, eq, desc } from "drizzle-orm";

export const libros = pgTable("libros", {
  id: serial("id").primaryKey(),
  titulo: text("titulo").notNull(),
  anio: integer("anio").notNull(),
  leido: boolean("leido").notNull().default(false),
});

const db = drizzle(process.env.DATABASE_URL);
const recientes = await db.select().from(libros)
  .where(and(gte(libros.anio, 1900), eq(libros.leido, false)))
  .orderBy(desc(libros.anio)).limit(10);
```

### 🪶 Sin instalar nada: node:sqlite (ejecutado)

```js
// sqlite.js — base de datos real incorporada en Node 22.5+ (npm i no hace falta)
import { DatabaseSync } from "node:sqlite";

const db = new DatabaseSync(":memory:");        // o "libros.db" para un archivo
db.exec(`CREATE TABLE libros (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  titulo TEXT NOT NULL,
  anio INTEGER NOT NULL
)`);

const insertar = db.prepare("INSERT INTO libros (titulo, anio) VALUES (?, ?)");
for (const [t, a] of [["Raza de bronce", 1919], ["Juan de la Rosa", 1885]]) insertar.run(t, a);

const buscar = db.prepare("SELECT * FROM libros WHERE titulo LIKE ?");
console.log(buscar.all("%bronce%"));   // → [ [Object: null prototype] { id: 1, titulo: 'Raza de bronce', anio: 1919 } ]
console.log(buscar.all("' OR 1=1 --")); // → []  (el intento de inyección es solo texto)
```

::: columnas
### ❌ Inyección SQL
```js
// el usuario manda q = "' OR 1=1 --"
pool.query(
  `SELECT * FROM usuarios
   WHERE nombre = '${req.query.q}'`
); // devuelve TODOS los usuarios
```
::: siguiente
### ✅ Consulta parametrizada
```js
pool.query(
  "SELECT * FROM usuarios WHERE nombre = $1",
  [req.query.q]
); // q es un valor, nunca SQL
```
:::

⚠️ Cuidado: el problema **N+1**: listar 50 libros y luego hacer 1 consulta por cada autor = 51 viajes a la BD. Usa `JOIN`, `include` (Prisma) o `IN (...)`.
⚠️ Cuidado: crear un `new Pool()` o `new PrismaClient()` **por petición** agota las conexiones de Postgres. Créalo una vez y reutilízalo. En serverless usa un pooler (PgBouncer, el de Neon o Supabase).
💡 Consejo: aprende primero SQL con `pg` (ver la hoja de SQL); después un ORM te ahorra trabajo sin esconderte lo que pasa. Para probar Postgres sin instalarlo: `docker run -d -e POSTGRES_PASSWORD=cambia_esto -p 5432:5432 postgres:17`.
🇬🇧 **driver** /dráiver/ = controlador · **ORM (object-relational mapper)** /o ar em/ = mapeador objeto-relacional · **connection pool** /konékshon pul/ = grupo de conexiones · **migration** /maigréishon/ = migración del esquema · **SQL injection** /es kiu el inyékshon/ = inyección SQL

## 🔐 Autenticación: sesiones vs JWT, bcrypt

🧠 Concepto: **autenticación** = comprobar QUIÉN eres (login). **Autorización** = comprobar QUÉ puedes hacer (roles, permisos). Son cosas distintas y se mezclan mucho.

🧠 Concepto: una contraseña NUNCA se guarda: se guarda su **hash** con un algoritmo **lento a propósito** (bcrypt, scrypt, argon2) y una **sal** (salt) aleatoria. Si roban la base de datos, cada contraseña cuesta mucho adivinarla. SHA-256 o MD5 son rápidos: no sirven para esto.

::: columnas
### 🍪 Sesión (cookie)
- El servidor guarda la sesión (memoria, Redis, BD)
- El navegador guarda solo un ID en una cookie `httpOnly`
- Fácil de **revocar**: borras la sesión
- Necesita almacenamiento compartido si hay varios servidores
::: siguiente
### 🎫 JWT (token firmado)
- El token lleva los datos y una firma; el servidor no guarda nada
- Escala sin estado, útil entre servicios y apps móviles
- **Difícil de revocar** hasta que expira
- El payload se puede LEER (solo está firmado, no cifrado)
:::

| Criterio | Sesión + cookie | JWT |
|---|---|---|
| Web clásica / mismo dominio | ✅ lo más simple y seguro | posible |
| App móvil + API pública | incómodo | ✅ natural |
| Cerrar sesión de verdad | inmediato | necesitas lista negra o tokens cortos |
| Dónde guardarlo | cookie `httpOnly; Secure; SameSite` | cookie `httpOnly` (no localStorage) |

```flujo
Login -> Verificar hash : bcrypt.compare
Verificar hash -> Emitir token : ✅ coincide
Verificar hash --> Login : ❌ 401
Emitir token -> Cliente : cookie httpOnly
Cliente -> Middleware auth : cada petición
Middleware auth -> Ruta : ✅ firma válida
Middleware auth --> Cliente : ❌ 401 expirado/falso
```

### ✅ Ejemplo resuelto: bcrypt + JWT (ejecutado)

```js
// auth.js — contraseñas con bcrypt + tokens JWT
// npm i bcrypt jsonwebtoken
import bcrypt from "bcrypt";
import jwt from "jsonwebtoken";

const SECRETO = process.env.JWT_SECRET ?? "cambia_esto_por_algo_largo";

// 1) REGISTRO: nunca guardes la contraseña, guarda su hash
const hash = await bcrypt.hash("MiClave#2026", 12);   // 12 = costo (2^12 rondas)
console.log("Hash guardado en la BD:", hash);

// 2) LOGIN: comparar lo que escribió el usuario con el hash
console.log("¿Clave correcta?", await bcrypt.compare("MiClave#2026", hash));
console.log("¿Clave falsa?   ", await bcrypt.compare("miclave#2026", hash));

// 3) Emitir un JWT corto con lo mínimo (nada secreto: el payload se puede leer)
const token = jwt.sign({ sub: "42", rol: "admin" }, SECRETO, { expiresIn: "15m" });
console.log("JWT:", token.slice(0, 40) + "...");
const [, payload] = token.split(".");
console.log("Payload decodificado SIN clave:", Buffer.from(payload, "base64url").toString());

// 4) Verificar en cada petición
console.log("Verificado:", jwt.verify(token, SECRETO, { algorithms: ["HS256"] }));
try {
  jwt.verify(token, "otro_secreto");
} catch (e) {
  console.log("Firma falsa →", e.name, e.message);
}
```

```text
Hash guardado en la BD: $2b$12$uICTgIDz3F/fqGIYvaogPejWXI7Py8miWzouXi8abs11/LC6/XZEm
¿Clave correcta? true
¿Clave falsa?    false
JWT: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ...
Payload decodificado SIN clave: {"sub":"42","rol":"admin","iat":1792442818,"exp":1792443718}
Verificado: { sub: '42', rol: 'admin', iat: 1792442818, exp: 1792443718 }
Firma falsa → JsonWebTokenError invalid signature
```

Medido en este PC: `bcrypt.hashSync` con costo 10 tarda 49 ms, con 12 tarda 196 ms y con 14 tarda 771 ms. Cada +1 de costo **duplica** el tiempo. Eso frena al atacante... y también bloquea tu loop si usas la versión `Sync`.

### 🛡️ Middleware de autenticación y roles

```js
import jwt from "jsonwebtoken";

export function exigirLogin(req, res, next) {
  const cabecera = req.get("Authorization") ?? "";          // "Bearer eyJ..."
  const token = cabecera.startsWith("Bearer ") ? cabecera.slice(7) : null;
  if (!token) return res.status(401).json({ error: "Falta el token" });
  try {
    req.usuario = jwt.verify(token, process.env.JWT_SECRET, { algorithms: ["HS256"] });
    next();
  } catch {
    res.status(401).json({ error: "Token inválido o expirado" });   // mismo mensaje para todo
  }
}

export const exigirRol = (rol) => (req, res, next) =>
  req.usuario?.rol === rol ? next() : res.status(403).json({ error: "No tienes permiso" });

// app.delete("/api/libros/:id", exigirLogin, exigirRol("admin"), borrarLibro);
```

| Código | Significa | Cuándo |
|---|---|---|
| **401** Unauthorized | no sabemos quién eres | sin token, token malo |
| **403** Forbidden | sabemos quién eres y NO puedes | rol insuficiente |

- `await bcrypt.hash(clave, 12)` :: Hash con sal incluida (costo 12 es un buen punto de partida)
- `await bcrypt.compare(clave, hash)` :: Comparar sin descifrar (no se puede descifrar)
- `jwt.sign(payload, secreto, { expiresIn: "15m" })` :: Crear token con caducidad
- `jwt.verify(token, secreto, { algorithms: ["HS256"] })` :: Verificar y fijar el algoritmo
- `crypto.randomUUID()` :: ID aleatorio para sesiones
- `crypto.randomBytes(32).toString("hex")` :: Secreto aleatorio fuerte
- `crypto.timingSafeEqual(a, b)` :: Comparar secretos sin filtrar tiempo
- `res.cookie("sid", id, { httpOnly: true, secure: true, sameSite: "lax" })` :: Cookie segura

⚠️ Cuidado: guardar el JWT en `localStorage` lo deja al alcance de cualquier script inyectado (XSS). Una cookie `httpOnly` no la puede leer JavaScript.
⚠️ Cuidado: pon siempre `algorithms` en `jwt.verify`. Ataques históricos en librerías JWT aceptaban tokens con `alg: none` (sin firma) o cambiaban el algoritmo.
⚠️ Cuidado: no pongas contraseñas ni datos sensibles en el payload: cualquiera lo decodifica con base64.
💡 Consejo: no inventes tu login si puedes evitarlo: **Better Auth**, **Auth.js**, **Passport** o servicios como Auth0, Clerk o Supabase Auth resuelven recuperación de clave, OAuth y 2FA.
🇬🇧 **hash** /jash/ = resumen irreversible · **salt** /solt/ = sal (dato aleatorio) · **token** /tóuken/ = ficha · **session** /séshon/ = sesión · **authentication** /ozentikéishon/ = autenticación · **authorization** /ozoraizéishon/ = autorización

## 🌊 Streams y buffers

🧠 Concepto: un **Buffer** es un bloque de **bytes** crudos (los archivos, la red y los sockets hablan bytes, no texto). Un **stream** es un flujo de esos bytes (o de objetos) que se procesa **por pedazos** (chunks), así un archivo de 10 GB no necesita 10 GB de RAM.

```js
// buffers.js — "Ñandú" son 5 caracteres pero 7 bytes en UTF-8
const b = Buffer.from("Ñandú", "utf8");
console.log(b);                       // <Buffer c3 91 61 6e 64 c3 ba>
console.log(b.length, "bytes vs", "Ñandú".length, "caracteres");   // 7 bytes vs 5 caracteres
console.log(b.toString("base64"), "|", b.toString("hex"));          // w5FhbmTDug== | c391616e64c3ba
console.log(Buffer.from("w5FhbmTDug==", "base64").toString());      // Ñandú
```

```flujo
Archivo -> createReadStream : chunks de 64 KB
createReadStream -> Transform : filtra líneas ERROR
Transform -> createGzip : comprime
createGzip -> createWriteStream : escribe .gz
createWriteStream --> Archivo : backpressure (frena al lector)
```

🧠 Concepto: **backpressure** (contrapresión): si el destino es más lento que el origen, el stream **frena** al origen para no llenar la memoria. `pipeline()` lo maneja por ti y además cierra todo si algo falla.

### ✅ Ejemplo resuelto: filtrar errores de un log de 1 000 000 de líneas

```js
// streams.js — procesar un archivo grande sin cargarlo entero
import { createReadStream, createWriteStream } from "node:fs";
import { writeFile, stat } from "node:fs/promises";
import { pipeline } from "node:stream/promises";
import { Transform } from "node:stream";
import { createGzip } from "node:zlib";

const lineas = Array.from({ length: 1_000_000 }, (_, i) => `${i % 20 ? "INFO" : "ERROR"} pedido ${i}`);
await writeFile("app.log", lineas.join("\n"));

// Transform: deja pasar solo las líneas ERROR (un chunk puede cortar una línea a la mitad)
let resto = "";
const soloErrores = new Transform({
  transform(chunk, _enc, listo) {
    const partes = (resto + chunk).split("\n");
    resto = partes.pop();                               // la última puede venir incompleta
    listo(null, partes.filter((l) => l.startsWith("ERROR")).join("\n") + "\n");
  },
  flush(listo) { listo(null, resto.startsWith("ERROR") ? resto + "\n" : ""); },
});

await pipeline(createReadStream("app.log"), soloErrores, createGzip(), createWriteStream("errores.log.gz"));

console.log(`app.log: ${((await stat("app.log")).size / 1e6).toFixed(1)} MB`);
console.log(`errores.log.gz: ${((await stat("errores.log.gz")).size / 1e3).toFixed(0)} KB`);
```

```text
app.log: 18.9 MB
errores.log.gz: 123 KB        ← 50 000 líneas ERROR comprobadas con zcat | wc -l
```

- `createReadStream(ruta) / createWriteStream(ruta)` :: Leer / escribir por pedazos
- `await pipeline(a, b, c)` :: Conectar streams con errores y cierre correctos (`node:stream/promises`)
- `for await (const chunk of stream)` :: Recorrer un stream con async iterator
- `Readable.from(array)` :: Crear un stream desde un array
- `Buffer.from(texto, "utf8")` :: Texto → bytes
- `buf.toString("hex" | "base64")` :: Bytes → texto
- `Buffer.concat([a, b])` :: Unir buffers
- `Readable.toWeb(stream)` :: Convertir a Web Streams (los de `fetch`)
- `readline.createInterface({ input })` :: Leer línea por línea

⚠️ Cuidado: un stream sin `.on("error")` que falla **tumba el proceso**. Con `pipeline` el error llega a tu `try/catch`.
⚠️ Cuidado: `res.send(await readFile("video.mp4"))` carga el video entero en RAM por cada usuario. Usa `createReadStream(...).pipe(res)` (o `pipeline`).
🇬🇧 **stream** /strim/ = flujo · **chunk** /chank/ = pedazo · **buffer** /báfer/ = bloque de bytes · **backpressure** /bákpresher/ = contrapresión · **pipe** /páip/ = tubería

## 🧵 Workers, child_process y cluster

Un solo hilo no usa todos los núcleos y se bloquea con CPU pesada. Node ofrece tres formas de salir de ahí:

```flujo
Problema -> worker_threads : cálculo pesado en el MISMO proceso
Problema -> child_process : ejecutar OTRO programa (git, ffmpeg)
Problema -> cluster : escalar el servidor a todos los núcleos
```

| Herramienta | Qué crea | Memoria | Úsala para |
|---|---|---|---|
| `worker_threads` | hilos con su propio V8 | pueden compartir buffers | cálculo pesado, procesar imágenes |
| `child_process` | un proceso del sistema | separada | ejecutar `git`, `ffmpeg`, scripts |
| `cluster` | N copias de tu servidor | separada | usar todos los núcleos con HTTP |

### ✅ worker_threads: 4 × fib(40) (ejecutado)

```js
// worker.js — mover un cálculo pesado a otro hilo
import { Worker, isMainThread, parentPort, workerData } from "node:worker_threads";

const fib = (n) => (n < 2 ? n : fib(n - 1) + fib(n - 2));   // a propósito lento: O(2^n)

if (isMainThread) {
  const t0 = performance.now();
  const latido = setInterval(() => console.log(`💓 el hilo principal sigue libre (${(performance.now() - t0).toFixed(0)} ms)`), 250);

  const calcular = (n) =>
    new Promise((ok, fallo) => {
      const w = new Worker(import.meta.filename, { workerData: n });   // mismo archivo, otro hilo
      w.once("message", ok);
      w.once("error", fallo);
    });

  const resultados = await Promise.all([calcular(40), calcular(40), calcular(40), calcular(40)]);
  clearInterval(latido);
  console.log(`4 × fib(40) = ${resultados[0]} en ${(performance.now() - t0).toFixed(0)} ms (en paralelo)`);
} else {
  parentPort.postMessage(fib(workerData));     // esto corre en el worker
}
```

```text
💓 el hilo principal sigue libre (250 ms)
💓 el hilo principal sigue libre (500 ms)
...
4 × fib(40) = 102334155 en 1557 ms (en paralelo)
secuencial en el hilo principal: 5055 ms     ← lo mismo sin workers (8 núcleos)
```

### child_process: execFile y spawn (ejecutado)

```js
import { execFile, spawn } from "node:child_process";
import { promisify } from "node:util";
const execFileP = promisify(execFile);

// execFile: argumentos separados → sin inyección de comandos
const { stdout } = await execFileP("git", ["--version"]);
console.log("execFile →", stdout.trim());              // → git version 2.56.0

// spawn: salida en streaming, ideal para procesos largos
const ls = spawn("ls", ["-1", "/etc"]);
let n = 0;
ls.stdout.on("data", (c) => (n += c.toString().split("\n").filter(Boolean).length));
ls.on("close", (codigo) => console.log(`ls terminó con código ${codigo}, ${n} entradas`));
```

### cluster: un proceso por núcleo (ejecutado)

```js
// cluster.js
import cluster from "node:cluster";
import http from "node:http";
import { availableParallelism } from "node:os";

if (cluster.isPrimary) {
  const n = Math.min(availableParallelism(), 4);
  for (let i = 0; i < n; i++) cluster.fork();
  cluster.on("exit", () => cluster.fork());            // auto-reparación si uno muere
} else {
  http.createServer((req, res) => res.end(`atendido por el pid ${process.pid}\n`)).listen(3000);
}
```

```text
# 6 peticiones con curl, repartidas entre 4 workers:
2 atendido por el pid 979139 · 1 por el 979140 · 2 por el 979141 · 1 por el 979142
```

💡 Consejo: hoy es más común escalar con **varios contenedores** o con PM2 en modo cluster (`pm2 start app.js -i max`) que escribir `cluster` a mano.
⚠️ Cuidado: con varios procesos, la memoria NO se comparte: un contador en una variable o una sesión en memoria será distinta en cada worker. Usa Redis o la base de datos.
⚠️ Cuidado: `exec("convert " + nombre)` con un nombre como `x; rm -rf ~` ejecuta comandos del atacante (**command injection**). Usa `execFile` con arreglo de argumentos.
🇬🇧 **thread** /zred/ = hilo · **process** /próses/ = proceso · **worker** /uérker/ = trabajador · **fork** /fork/ = bifurcar · **command injection** /komand inyékshon/ = inyección de comandos

## 📋 Logging: registrar bien lo que pasa

🧠 Concepto: un **log** es el diario de tu aplicación. En producción no se lee en una terminal sino que lo recoge una herramienta (Loki, Datadog, CloudWatch), así que debe ser **estructurado**: una línea JSON con campos, no una frase suelta.

```js
// log.js — logs estructurados con pino (npm i pino)
import pino from "pino";

const log = pino({ level: process.env.LOG_LEVEL ?? "info" });

log.info("servidor arrancado");
log.info({ usuarioId: 42, ruta: "/api/libros", ms: 3.1 }, "petición atendida");
log.debug("esto NO sale con level=info");
log.error({ err: new Error("conexión rechazada") }, "falló la BD");
```

```json
{"level":30,"time":1792442873968,"pid":979493,"hostname":"yf","msg":"servidor arrancado"}
{"level":30,"time":1792442873968,"pid":979493,"hostname":"yf","usuarioId":42,"ruta":"/api/libros","ms":3.1,"msg":"petición atendida"}
{"level":50,"time":1792442873968,"pid":979493,"hostname":"yf","err":{"type":"Error","message":"conexión rechazada","stack":"..."},"msg":"falló la BD"}
```

| Nivel | Cuándo | pino |
|---|---|---|
| fatal | el proceso no puede seguir | 60 |
| error | falló una operación | 50 |
| warn | raro pero tolerable | 40 |
| info | eventos normales (arranque, petición) | 30 |
| debug / trace | detalle para depurar | 20 / 10 |

- `LOG_LEVEL=debug node app.js` :: Cambiar el detalle sin tocar código
- `node app.js | npx pino-pretty` :: Verlo bonito en desarrollo
- `log.child({ reqId })` :: Logger que añade el id de petición a cada línea
- `console.table(datos)` :: Tabla rápida para depurar
- `node --inspect app.js` :: Depurar con Chrome DevTools (`chrome://inspect`)

⚠️ Cuidado: no registres contraseñas, tokens, tarjetas ni cabeceras `Authorization`. Los logs se copian a muchos lugares y viven años (pino tiene la opción `redact` para tachar campos).
💡 Consejo: `console.log` sirve para aprender; en producción `pino` es unas veces más rápido y escribe JSON que las plataformas entienden.
🇬🇧 **log level** /log lével/ = nivel de registro · **structured logging** /strákchurd lóguing/ = registro estructurado · **to redact** /tu ridákt/ = tachar datos sensibles · **trace** /treis/ = rastro

## 🧪 Testing: node:test y Vitest

🧠 Concepto: un **test automático** ejecuta tu código con entradas conocidas y comprueba la salida. Te avisa al instante si un cambio rompe algo (**regresión**). Una API sin tests da miedo tocar.

| | `node:test` | Vitest |
|---|---|---|
| Instalación | ninguna (viene con Node) | `npm i -D vitest` |
| Estilo | `test()`, `assert` | `describe/it/expect` (como Jest) |
| Mocks, snapshots, cobertura | básicos (`--experimental-test-coverage`) | completos |
| Velocidad / modo watch | bueno | excelente |
| Ideal para | librerías, proyectos pequeños | proyectos con frontend o TS |

### ✅ node:test con la API de libros (4 tests pasan)

```js
// test/libros.test.js — node --test
import { test, before, after } from "node:test";
import assert from "node:assert/strict";
import { app } from "../src/app.js";

let server, base;
before(() => {
  server = app.listen(0);                        // puerto 0 = el sistema elige uno libre
  base = `http://localhost:${server.address().port}/api/libros`;
});
after(() => server.close());

test("lista los libros iniciales", async () => {
  const res = await fetch(base);
  assert.equal(res.status, 200);
  assert.equal((await res.json()).length, 2);
});

test("crea un libro válido y limpia espacios", async () => {
  const res = await fetch(base, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ titulo: "  Ficciones ", autor: "Borges", anio: 1944 }),
  });
  assert.equal(res.status, 201);
  const libro = await res.json();
  assert.equal(libro.titulo, "Ficciones");
  assert.equal(libro.leido, false);              // valor por defecto de zod
});

test("rechaza datos inválidos con 400", async () => {
  const res = await fetch(base, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ titulo: "" }),
  });
  assert.equal(res.status, 400);
  assert.match((await res.json()).detalles[0], /titulo/);
});

test("404 para un id que no existe", async () => {
  assert.equal((await fetch(`${base}/999`)).status, 404);
});
```

```text
$ NODE_ENV=test node --test test/libros.test.js
✔ lista los libros iniciales (47.68ms)
✔ crea un libro válido y limpia espacios (12.87ms)
✔ rechaza datos inválidos con 400 (4.16ms)
✔ 404 para un id que no existe (2.26ms)
ℹ tests 4 · pass 4 · fail 0
```

### Vitest + supertest (sin abrir puerto)

```js
// test/libros.spec.js — npm i -D vitest supertest   ·   npx vitest run
import { describe, it, expect } from "vitest";
import request from "supertest";
import { app } from "../src/app.js";

describe("API de libros", () => {
  it("borra y luego da 404", async () => {
    await request(app).delete("/api/libros/1").expect(204);
    const res = await request(app).get("/api/libros/1").expect(404);
    expect(res.body.error).toContain("No existe");
  });

  it("PATCH cambia solo lo enviado", async () => {
    const res = await request(app).patch("/api/libros/2").send({ leido: true }).expect(200);
    expect(res.body).toMatchObject({ id: 2, titulo: "Raza de bronce", leido: true });
  });
});
// → Test Files 1 passed (1) · Tests 2 passed (2)
```

- `node --test` :: Busca y corre `*.test.js` y TODO lo que haya en `test/` (¡también el `.spec.js` de Vitest!)
- `node --test --watch` :: Repite al guardar
- `node --test --experimental-test-coverage` :: Muestra cobertura
- `npx vitest` :: Modo watch interactivo
- `npx vitest run` :: Una pasada (para CI); aquí con `test/libros.spec.js` para no recoger el `.test.js` de node:test

⚠️ Cuidado: si mezclas ambos en la misma carpeta, `node --test` falla con el `.spec.js` y `vitest run` con el `.test.js` (probado): pasa la ruta del archivo o usa un solo ejecutor. Vitest solo encuentra archivos `*.test.js` o `*.spec.js`; si lo llamas `libros.vitest.js` dirá "No test files found" (nos pasó al probar).
💡 Consejo: testea la **app**, no el `listen`: por eso separamos `app.js` de `server.js`. Y en los tests de BD usa una base aparte o `:memory:`.
🇬🇧 **test** /test/ = prueba · **assertion** /asérshon/ = afirmación · **mock** /mok/ = simulacro · **coverage** /káverich/ = cobertura · **regression** /rigréshon/ = fallo que reaparece

## 🚀 Rendimiento y profiling

🧠 Concepto: **profiling** = medir dónde se va el tiempo o la memoria. Regla de oro: **mide antes de optimizar**; casi siempre el cuello de botella no está donde crees (suele ser la BD o una consulta N+1).

### 📏 Medir el retraso del event loop (ejecutado)

```js
// retraso.js — ¿cuánto se atrasa el loop?
import { monitorEventLoopDelay } from "node:perf_hooks";
import { pbkdf2Sync, pbkdf2 } from "node:crypto";

const h = monitorEventLoopDelay({ resolution: 10 });
const medir = async (nombre, fn) => {
  h.reset(); h.enable();
  await fn();
  h.disable();
  console.log(`${nombre.padEnd(22)} retraso p99: ${(h.percentile(99) / 1e6).toFixed(0)} ms`);
};

const sync = async () => { for (let i = 0; i < 10; i++) { pbkdf2Sync("clave", "sal", 200_000, 64, "sha512"); await new Promise(r => setImmediate(r)); } };
const asyncPool = () => Promise.all(Array.from({ length: 10 }, () =>
  new Promise((ok) => pbkdf2("clave", "sal", 200_000, 64, "sha512", ok))));   // thread pool

await medir("pbkdf2Sync (bloquea)", sync);
await medir("pbkdf2 (thread pool)", asyncPool);
```

```text
pbkdf2Sync (bloquea)   retraso p99: 124 ms
pbkdf2 (thread pool)   retraso p99: 10 ms      ← el loop casi no se entera
```

- `node --cpu-prof app.js` :: Genera `.cpuprofile` (ábrelo en Chrome DevTools > Performance)
- `node --inspect app.js` :: Perfiles y memoria en vivo con DevTools
- `node --heap-prof app.js` :: Perfil de memoria
- `npx autocannon -c 50 -d 10 localhost:3000` :: Prueba de carga (50 conexiones, 10 s)
- `npx clinic doctor -- node app.js` :: Diagnóstico automático (Clinic.js)
- `process.memoryUsage().heapUsed` :: Memoria JS en uso
- `UV_THREADPOOL_SIZE=8 node app.js` :: Más hilos para fs/crypto/zlib

```grafica
tipo: barras
titulo: Pbkdf2 de 10 claves — retraso p99 del loop (medido aquí)
unidad: ms
Sync bloquea : 124
Thread pool : 10
```

| Problema típico | Síntoma | Solución |
|---|---|---|
| bucle/regex pesado | latencia alta para todos | worker o algoritmo mejor |
| fuga de memoria (listeners, cachés sin límite) | RAM sube sin parar y se cae (OOM) | heap snapshot; `Map` con límite (LRU) |
| N+1 consultas | lento con muchos datos | `JOIN` / `include` |
| sin compresión | respuestas grandes | `compression` o nginx delante |
| sin caché | misma consulta mil veces | Redis o caché en memoria con TTL |

💡 Consejo: lo más rentable casi siempre: índices en la BD, caché, y paginar (`LIMIT/OFFSET` o cursor) en vez de devolver 100 000 filas.
⚠️ Cuidado: el límite por defecto del heap de V8 depende de la memoria del equipo; si tu servidor se cae con "JavaScript heap out of memory", sube `--max-old-space-size=MB` solo después de buscar la fuga.
🇬🇧 **profiling** /próufailing/ = medir rendimiento · **bottleneck** /bótolnek/ = cuello de botella · **memory leak** /mémori lik/ = fuga de memoria · **latency** /léitensi/ = latencia · **load test** /loud test/ = prueba de carga

## 🛡️ Seguridad: la cadena de suministro y tu API

🧠 Concepto: **supply chain attack** (ataque a la cadena de suministro) = el atacante compromete una librería que tú instalas, en vez de atacarte a ti.
📌 Con `npm i express` bajaron **65 paquetes** (medido aquí); un proyecto mediano tiene cientos o miles, y cada uno corre con tus permisos.

```tiempo
2016 : left-pad — un autor retira 11 líneas y se rompen builds en todo el mundo
2018 : event-stream — un mantenedor cede el paquete a un extraño que mete código malicioso
2021 : ua-parser-js y coa/rc — cuentas de mantenedores secuestradas
2022 : colors y faker — el propio autor sabotea sus paquetes (protesta)
2025 : cuentas de npm phisheadas (chalk, debug) y el gusano Shai-Hulud
```

### 📰 Incidentes reales (aprende de ellos)

| Incidente | Qué pasó | Lección |
|---|---|---|
| **left-pad** (marzo 2016) | Azer Koçulu retiró sus paquetes de npm tras una disputa por el nombre `kik`; `left-pad` (rellena un texto con espacios, ~11 líneas) era dependencia de Babel y React: miles de builds fallaron. npm restauró el paquete | una dependencia trivial puede parar el mundo; **fija versiones** y usa un lockfile |
| **event-stream** (nov 2018) | el autor original cedió el mantenimiento a alguien que ofrecía ayuda; este añadió la dependencia `flatmap-stream` con código que robaba monederos de bitcoin (apuntaba a la app Copay) | confiar en "quien se ofrece a ayudar" es un riesgo; revisa los cambios de dependencias |
| **Gusano Shai-Hulud** (desde el 15 sept 2025; hubo una segunda oleada en nov 2025) | malware que se propagaba solo: robaba tokens de npm de los mantenedores infectados y republicaba sus otros paquetes con el código malicioso | nunca dejes tokens de publicación en tu PC sin 2FA; los scripts de instalación son la puerta de entrada |
| **chalk y debug** (8 sept 2025) | un mantenedor cayó en un phishing y se publicaron versiones maliciosas de 18 paquetes muy descargados (chalk, debug, ansi-styles, supports-color…) que cambiaban direcciones de criptomonedas en el navegador | un solo mantenedor engañado afecta a medio ecosistema; 2FA resistente a phishing y esperar unos días antes de actualizar |
| **Typosquatting** (siempre) | paquetes con nombre casi igual (`expres`, `reqeusts`) que contienen malware | escribe y revisa bien el nombre antes de `npm i` |

📌 Por eso las versiones nuevas de npm (la 12 de este PC) **bloquean por defecto los scripts de instalación** de las dependencias: al instalar `bcrypt` me avisó "1 package has install scripts blocked" y hubo que aprobarlo con `npm install-scripts approve bcrypt`. Ese bloqueo corta justo la vía que usan los gusanos.

```flujo
dir: abajo
npm install paquete -> preinstall / postinstall : se ejecuta código del autor
preinstall / postinstall -> Roba .env y tokens : si es malicioso
Roba .env y tokens -> Publica versiones infectadas : se propaga
Publica versiones infectadas -> npm install paquete : otros lo instalan
```

### 🧰 Defensas

- `npm audit` :: Busca vulnerabilidades conocidas (en el proyecto de pruebas halló 3 moderadas, todas en `uuid` vía `autocannon`)
- `npm audit signatures` :: Verifica firmas y procedencia del registro (en la prueba: 231 paquetes verificados)
- `npm ci` :: Instala EXACTO desde el lockfile (no sube versiones por sorpresa)
- `npm ci --ignore-scripts` :: Instala sin ejecutar scripts de dependencias
- `npm install-scripts ls` :: Qué paquetes quieren ejecutar scripts (npm 12+)
- `npm ls --all | wc -l` :: Cuánto árbol de dependencias tienes (en el proyecto de pruebas: 384 líneas)
- `npm outdated` :: Qué está desactualizado (actualiza con tests, no a ciegas)
- `npm publish --provenance` :: Al publicar, adjunta prueba de dónde se construyó
- `npx depcheck` :: Detecta dependencias que no usas (menos superficie)

```bash
npm audit
# → 3 moderate severity vulnerabilities
#   uuid  <11.1.1 ... Missing buffer bounds check ... (viene de autocannon, una devDependency)
npm audit signatures
# → 231 packages have verified registry signatures
```

✅ Bien: lockfile en git · `npm ci` en CI y producción · 2FA en tu cuenta de npm y GitHub · mirar descargas, mantenimiento y repo antes de instalar · pocas dependencias · Dependabot/Renovate para actualizar con PRs revisables.
❌ Mal: `"latest"` o `*` como versión · copiar `npm i` de un blog sin mirar el nombre · ejecutar `curl ... | sudo bash` de un README · publicar con un token sin 2FA guardado en el PC.

### 🔒 Proteger tu API Express

```js
import express from "express";
import helmet from "helmet";                       // cabeceras de seguridad HTTP
import { rateLimit } from "express-rate-limit";     // frenar abusos y fuerza bruta

const app = express();
app.disable("x-powered-by");                        // no anunciar la tecnología
app.use(helmet());
app.use(rateLimit({ windowMs: 60_000, limit: 100 })); // 100 peticiones/min por IP
app.use(express.json({ limit: "100kb" }));          // limitar el tamaño del body

// Login: límite MUY estricto contra adivinar contraseñas
app.use("/api/login", rateLimit({ windowMs: 15 * 60_000, limit: 5 }));
```

| Amenaza | Qué es | Defensa |
|---|---|---|
| Inyección SQL | datos del usuario dentro del SQL | consultas parametrizadas |
| XSS | script inyectado en la página | escapar salida, CSP (helmet), cookies `httpOnly` |
| CSRF | otro sitio hace peticiones con tu cookie | `SameSite`, tokens CSRF |
| Fuerza bruta | probar miles de claves | rate limit, bcrypt, bloqueo temporal |
| Mass assignment | el cliente cambia campos que no debe | whitelist con zod |
| Path traversal | `../../etc/passwd` | `path.resolve` + comprobar prefijo |
| ReDoS | regex que tarda minutos | regex simples, límites de largo |
| SSRF | tu servidor pide una URL interna que manda el atacante | lista permitida de hosts |
| Secretos en el repo | `.env` en GitHub | `.gitignore`, rotar claves, gitleaks |

::: desplegable 🔬 Probando el rate limit y helmet
La API del CRUD envía `X-RateLimit-Limit: 100` y `X-RateLimit-Remaining: 89` (bajaba con cada petición), `X-Content-Type-Options: nosniff` y un `Content-Security-Policy` por defecto. Con más de 100 peticiones por minuto desde la misma IP, express-rate-limit responde **429 Too Many Requests**.

Detrás de un proxy (nginx, Render, Railway) todos los usuarios parecen venir de la misma IP; hay que configurar `app.set("trust proxy", 1)` para que el límite funcione por usuario real.
:::

⚠️ Cuidado: CORS **no** es seguridad de la API (solo lo aplica el navegador). Cualquiera puede llamar tu API con curl; la protección real es autenticación + validación.
⚠️ Cuidado: en producción nunca devuelvas `err.stack` ni el mensaje del driver de BD al cliente: filtra tablas y rutas. Registra el detalle en el log y responde "Error interno".
💡 Consejo: ejecuta `npm audit` y un escáner de secretos (`gitleaks`) en tu CI. Y recuerda que la mejor dependencia es la que no instalas: `fetch`, `node:test`, `--env-file`, `node:sqlite` y `parseArgs` ya vienen con Node.
🇬🇧 **supply chain** /suplái chein/ = cadena de suministro · **vulnerability** /valnerabíliti/ = vulnerabilidad · **typosquatting** /taiposkuóting/ = nombre falso parecido · **rate limit** /réit límit/ = límite de peticiones · **to rotate** /tu routéit/ = rotar (cambiar una clave)

## 🌐 Despliegue: PM2, Docker y la nube

```flujo
Tu PC -> GitHub : git push
GitHub -> CI : tests y npm audit
CI -> Plataforma : deploy
Plataforma -> Usuarios : https://miapi.com
```

| Opción | Ideal para | Cómo |
|---|---|---|
| **Railway / Render** | primera API, proyectos de clase | conectas el repo; build `npm ci`; start `npm start`; variables en el panel |
| **Fly.io** | contenedores cerca del usuario, regiones | `fly launch` genera el Dockerfile y despliega |
| **Vercel / Netlify** | frontend + funciones serverless | `npx vercel`; cada ruta es una función |
| **VPS** (Hetzner, DigitalOcean) | control total, barato | `git pull` + PM2/systemd + nginx |
| **Docker en cualquier lado** | mismo entorno en todas partes | Dockerfile (abajo) |

⚠️ Cuidado: los planes gratuitos cambian a menudo (límites, pausas por inactividad, tarjeta obligatoria). Mira las condiciones actuales antes de elegir.

### 🐳 Dockerfile para una API de Node

```dockerfile
FROM node:24-slim
WORKDIR /app
ENV NODE_ENV=production
COPY package*.json ./
RUN npm ci --omit=dev          # capa cacheada: solo cambia si cambian las dependencias
COPY src ./src
USER node                      # no ejecutes como root
EXPOSE 3000
CMD ["node", "src/server.js"]
```

```bash
docker build -t api-libros .
docker run -d -p 3000:3000 --env-file .env --name api api-libros
docker logs -f api
```

### 🔁 PM2 en un VPS

```bash
git clone https://github.com/usuario/api-libros.git && cd api-libros
npm ci --omit=dev
cp .env.example .env && nano .env              # poner los valores reales
npx pm2 start src/server.js --name api -i max  # un proceso por núcleo (modo cluster)
npx pm2 save && npx pm2 startup                # que arranque al reiniciar el servidor
npx pm2 logs api                               # logs en vivo
```

- `GET /health` :: Ruta que responde `{ ok: true }`; las plataformas la usan para saber si vives
- `process.env.PORT` :: Las plataformas te dan el puerto por variable: úsalo siempre
- `process.on("SIGTERM", cerrar)` :: Docker/PM2 piden apagarte con esta señal; cierra el servidor con elegancia
- `NODE_ENV=production` :: Express y otras librerías se optimizan

📌 Checklist: puerto desde `PORT` · secretos en variables del panel (no en el repo) · `NODE_ENV=production` · CORS solo con tu dominio · errores sin stack al cliente · `npm audit` limpio · base de datos gestionada (SQLite en disco efímero se borra en cada despliegue) · logs a stdout en JSON.
💡 Consejo: nginx o Caddy delante de Node para HTTPS, compresión y archivos estáticos; Node se ocupa solo de la lógica.
🇬🇧 **deploy** /diplói/ = desplegar · **container** /kontéiner/ = contenedor · **health check** /jelz chek/ = chequeo de salud · **reverse proxy** /rivérs próksi/ = proxy inverso · **ephemeral** /ifémeral/ = efímero, temporal

## 🦕 Node vs Deno vs Bun

![Node.js y Deno, dos runtimes de JavaScript creados por la misma persona (logos de Wikimedia Commons)](img/node/node-deno.png)

🧠 Concepto: los tres son **runtimes** de JavaScript/TypeScript fuera del navegador. **Deno** (2018, Ryan Dahl) corrige lo que él "lamentaba" de Node: seguridad por permisos, TypeScript nativo y módulos por URL/JSR. **Bun** (2022, escrito en Zig, motor JavaScriptCore de Safari) apuesta por la velocidad y por ser "todo en uno": runtime + gestor de paquetes + bundler + test runner.

| | Node.js | Deno | Bun |
|---|---|---|---|
| Año | 2009 | 2018 | 2022 |
| Motor | V8 | V8 | JavaScriptCore |
| TypeScript | sin compilar solo "strip types" (probado: `node hola.ts` funciona) | nativo | nativo |
| Permisos | opcionales (`--permission`) | **por defecto denegado** (`--allow-read`...) | no |
| Paquetes | npm | npm + JSR | npm (instalador muy rápido) |
| Compatibilidad con npm | 100% | alta | alta |
| Madurez y empleo | la mayor, con diferencia | media | creciendo |
| Ideal para | producción, empleo, ecosistema | scripts seguros, edge | velocidad, tooling, proyectos nuevos |

```bash
# Medido en este PC (Node 26.11 y Deno 2.9.7, promedio de 20 arranques de "0"):
#   node -e 0  → ~38 ms        deno eval 0 → ~25 ms
node hola.ts      # → Hola Ana, tienes 21       (Node ejecuta TS sin compilar)
deno run hola.ts  # → Hola Ana, tienes 21
```

⚠️ Cuidado: no medí Bun porque no está instalado en este PC; no te fíes de benchmarks de blog sin ver qué miden (un "hola mundo" no dice nada de tu app real con base de datos).

| Si quieres... | Usa | Por qué |
|---|---|---|
| trabajo y máximo soporte | **Node** | casi todas las ofertas y todos los hostings lo soportan |
| script que no debe tocar tu disco | **Deno** | permisos explícitos: `deno run --allow-net=api.com script.ts` |
| arrancar rápido, instalar paquetes rápido | **Bun** | un solo binario con todo |
| compatibilidad y estabilidad en la empresa | **Node LTS** | años de historia |

💡 Consejo: aprende **Node primero**: casi todo lo que sabes (APIs, módulos, `fetch`, streams) se traslada a los otros dos.
🇬🇧 **runtime** /rántaim/ = entorno de ejecución · **permission** /permíshon/ = permiso · **bundler** /bándler/ = empaquetador · **all-in-one** /ol in uán/ = todo en uno

## 🥊 Node vs Python vs Go para el backend

| | Node.js | Python (FastAPI/Django) | Go |
|---|---|---|---|
| Modelo | un hilo + event loop | hilos/procesos o `asyncio` | goroutines (miles de hilos ligeros) |
| Tipado | dinámico (o TS) | dinámico (o type hints) | estático, compilado |
| Velocidad CPU | media (JIT) | baja | alta |
| E/S concurrente | excelente | buena con async | excelente |
| IA / datos | limitada | **líder** (PyTorch, pandas) | poca |
| Despliegue | runtime + `node_modules` | runtime + venv | **un binario** |
| Curva | baja | muy baja | media |
| Ideal para | APIs, tiempo real, full stack JS | IA, ciencia de datos, scripts, Django | microservicios, infraestructura, CLIs |

```arbol
¿Qué backend elijo?
  ¿El proyecto usa IA o datos pesados?
    sí → Python (FastAPI) y, si quieres, Node como capa de API
    no → ¿Ya sabes JavaScript/TypeScript y haces el frontend?
      sí → Node (un solo lenguaje en todo el stack)
      no → ¿Necesitas rendimiento máximo y binarios simples?
        sí → Go
        no → lo que domine tu equipo
```

📌 Casos reales: Docker, Kubernetes y Terraform están escritos en **Go**; Instagram y Dropbox usan Python a gran escala; Netflix, PayPal y LinkedIn usan Node en capas de API. Ningún lenguaje "gana": cada uno resuelve mejor un tipo de problema.
💡 Consejo: para tu carrera (CS/IA) lo común es **Python para modelos y Node/TypeScript para el producto web** que los consume (la API de Node llama al servicio de Python).
🇬🇧 **goroutine** /gorutín/ = hilo ligero de Go · **compiled** /kompáild/ = compilado · **dynamic typing** /dainámik taiping/ = tipado dinámico · **binary** /báinari/ = ejecutable

## 💥 Errores de otros programadores (y cómo no repetirlos)

| Error | Causa → consecuencia | Cómo evitarlo |
|---|---|---|
| **Callback hell** | callbacks anidados 5 niveles → código ilegible y errores perdidos | `async/await` y `fs/promises` |
| **Promesa sin catch** | `guardar()` sin `await` → error silencioso o proceso caído | siempre `await` + `try/catch`; manejador global |
| **Bloquear el loop** | `readFileSync`/bucle grande → todos los usuarios se congelan | async, workers, streams |
| **Secretos en el repo** | `.env` o claves en GitHub → bots las roban en minutos | `.gitignore`, rotar, gitleaks |
| `req.body` sin validar | datos raros → crash o inyección | zod en cada ruta |
| Olvidar `await` | usas una Promise como si fuera el valor → `[object Promise]` | lint `no-floating-promises` |
| `forEach` con `await` | no espera nada: el código sigue antes de acabar | `for...of` o `Promise.all(map)` |
| **Nuevo Pool por petición** | se agotan las conexiones de la BD | un pool global |
| **Sin límite en el body** | alguien sube 2 GB → RAM llena | `express.json({ limit })` |
| `npm i` sin mirar | typosquatting, paquete abandonado | revisar nombre, mantenimiento, descargas |
| **Estado en memoria** | contador/sesión distinto en cada proceso | Redis o BD |
| `process.exit()` en medio | corta respuestas pendientes | cerrar con `server.close()` |

### ❌ Promesa sin catch: lo que pasa (ejecutado)

```js
// sincatch.js
async function guardarPedido() {
  throw new Error("la BD no responde");
}
setInterval(() => console.log("servidor atendiendo..."), 300);
guardarPedido();                 // ❌ sin await ni .catch
```

```text
file:///.../sincatch.js:3
  throw new Error("la BD no responde");
        ^
Error: la BD no responde
...
Node.js v26.11.1            ← el proceso murió con código de salida 1, sin imprimir ni un "atendiendo"
```

::: columnas
### ❌ forEach con await
```js
const ids = [1, 2, 3];
ids.forEach(async (id) => {
  await guardar(id);        // nadie espera esto
});
console.log("listo");       // sale ANTES de guardar
```
::: siguiente
### ✅ for...of o Promise.all
```js
for (const id of ids) await guardar(id);     // en orden
// o en paralelo:
await Promise.all(ids.map((id) => guardar(id)));
console.log("listo");       // ahora sí
```
:::

```js
// Red de seguridad global: registra y muere (que PM2/Docker lo reinicien)
process.on("unhandledRejection", (motivo) => { console.error("Promesa rechazada:", motivo); process.exit(1); });
process.on("uncaughtException", (err) => { console.error("Excepción:", err); process.exit(1); });
```

⚠️ Cuidado: un `uncaughtException` deja el programa en un estado dudoso. Regístralo, y reinicia el proceso; no sigas como si nada.
💡 Consejo: activa ESLint con `@typescript-eslint/no-floating-promises` (o la regla `no-floating-promises`): detecta promesas olvidadas antes de ejecutar.
🇬🇧 **callback hell** /kólbak jel/ = pirámide de callbacks · **floating promise** /flóuting prómis/ = promesa sin esperar · **memory leak** /mémori lik/ = fuga de memoria · **crash** /krash/ = caída del programa

## 🚀 El futuro de Node

🚀 Futuro: **TypeScript sin compilar**. Node ya puede ejecutar `.ts` quitando los tipos ("type stripping"): en este PC `node hola.ts` funciona. Solo admite TS "borrable": un `enum` da `ERR_UNSUPPORTED_TYPESCRIPT_SYNTAX` ("TypeScript enum is not supported in strip-only mode"). Para tipar y comprobar errores sigues usando `tsc` (o tu editor).

```bash
cat hola.ts
# interface Usuario { nombre: string; edad: number }
# const u: Usuario = { nombre: "Ana", edad: 21 };
# console.log(`Hola ${u.nombre}, tienes ${u.edad}`);
node hola.ts          # → Hola Ana, tienes 21        (sin ts-node, sin build)
echo 'enum Color { Rojo } console.log(Color.Rojo)' > enum.ts
node enum.ts          # → SyntaxError [ERR_UNSUPPORTED_TYPESCRIPT_SYNTAX]: ... enum is not supported in strip-only mode
```

🚀 Futuro: **modelo de permisos**. Con `--permission` Node deniega por defecto y tú concedes (idea tomada de Deno):

```bash
node --permission perm.mjs
# → Error: Access to this API has been restricted. Use --allow-fs-read to manage permissions.
#   code: 'ERR_ACCESS_DENIED', permission: 'FileSystemRead', resource: '/etc/hostname'
node --permission --allow-fs-read=/etc/hostname --allow-fs-read=. perm.mjs   # ahora lee el archivo
node --help | grep -E "allow-"   # → allow-fs-read, allow-fs-write, allow-net, allow-child-process, allow-worker, allow-addons, allow-wasi
```

Es una defensa contra la cadena de suministro: aunque una dependencia sea maliciosa, no podría leer `~/.ssh` ni abrir la red si no se lo permitiste.

```tiempo
Ahora : fetch, --watch, --env-file, node:test, node:sqlite integrados
Ahora : require(esm), type stripping, --permission
Tendencia : menos dependencias, más librería estándar y Web APIs
Tendencia : TypeScript como lenguaje por defecto
Tendencia : npm bloquea scripts de instalación por defecto
```

- `node --watch app.js` :: Ya no necesitas nodemon
- `node --env-file=.env app.js` :: Ya no necesitas dotenv
- `node --test` :: Ya no necesitas Jest para lo simple
- `node --run dev` :: Ejecuta scripts sin pasar por npm
- `import { DatabaseSync } from "node:sqlite"` :: SQLite incorporada
- `fetch, WebSocket, URLPattern, AbortSignal.timeout()` :: Web APIs estándar (algunas pueden requerir versiones recientes: prueba en tu `node -v`)

🚀 Futuro: se acercan los runtimes: Node adopta ideas de Deno (permisos, TS, Web APIs) y Bun (velocidad), y Hono/Fastify empujan código que corre igual en todos. Aprender los **estándares web** (`fetch`, `Request/Response`, streams web) te sirve en Node, Deno, Bun y el edge.
🇬🇧 **type stripping** /taip stríping/ = quitar los tipos al ejecutar · **standard library** /stándard láibrari/ = librería estándar · **edge** /edch/ = servidores cerca del usuario

## 🏋️ Ejercicios (de fácil a difícil)

### 1️⃣ Contador de palabras (fácil)
Haz `node e1.js archivo.txt` que diga cuántas palabras hay, cuántas son distintas y las 3 más repetidas.

::: desplegable 🧩 Ver la solución
```js
// e1.js — uso: node e1.js archivo.txt
import { readFile } from "node:fs/promises";

const [ruta] = process.argv.slice(2);
if (!ruta) { console.error("Uso: node e1.js <archivo>"); process.exit(1); }

const texto = await readFile(ruta, "utf8");
const palabras = texto.toLowerCase().match(/\p{L}+/gu) ?? [];   // \p{L} = cualquier letra (con tildes)
const conteo = new Map();
for (const p of palabras) conteo.set(p, (conteo.get(p) ?? 0) + 1);
const top = [...conteo].sort((a, b) => b[1] - a[1]).slice(0, 3);
console.log(`${palabras.length} palabras, ${conteo.size} distintas`);
console.table(Object.fromEntries(top));
```
Con un archivo que dice "el perro y el gato y el loro / el sol" salió: `10 palabras, 6 distintas` y la tabla `el 4 · y 2 · perro 1`.
:::

### 2️⃣ Del callback hell a async/await (fácil)
Reescribe: lee `origen`, pasa el texto a mayúsculas y guárdalo en `destino`, manejando errores.

```js
import fs from "node:fs";
fs.readFile(origen, "utf8", (err, texto) => {
  if (err) return console.error(err);
  fs.writeFile(destino, texto.toUpperCase(), (err2) => {
    if (err2) return console.error(err2);
    console.log("Listo");
  });
});
```

::: desplegable 🧩 Ver la solución
```js
import { readFile, writeFile } from "node:fs/promises";

async function copiarMayusculas(origen, destino) {
  try {
    const texto = await readFile(origen, "utf8");
    await writeFile(destino, texto.toUpperCase());
    console.log("Listo");
  } catch (err) {
    console.error("Falló:", err.code ?? err.message);   // un solo catch para ambos pasos
  }
}
await copiarMayusculas("t.txt", "T.txt");   // → Listo
await copiarMayusculas("nada.txt", "x.txt"); // → Falló: ENOENT
```
:::

### 3️⃣ Servidor nativo con `/hora` (fácil)
Con `node:http` responde JSON con la hora en `GET /hora` y 404 en cualquier otra ruta.

::: desplegable 🧩 Ver la solución
```js
import http from "node:http";
http.createServer((req, res) => {
  if (req.method === "GET" && req.url === "/hora") {
    res.writeHead(200, { "Content-Type": "application/json" });
    return res.end(JSON.stringify({ hora: new Date().toISOString() }));
  }
  res.writeHead(404).end();
}).listen(3000);
// curl localhost:3000/hora → {"hora":"2026-10-20T06:34:28.994Z"}   curl .../x → 404
```
:::

### 4️⃣ Paginación (medio)
Haz `GET /api/items?pagina=3&limite=10` que devuelva `{ pagina, limite, total, paginas, items }` con límite máximo de 50 y valores seguros si mandan basura.

::: desplegable 🧩 Ver la solución
```js
import express from "express";
const datos = Array.from({ length: 25 }, (_, i) => ({ id: i + 1 }));
const app = express();
app.get("/api/items", (req, res) => {
  const pagina = Math.max(1, Number(req.query.pagina) || 1);       // NaN → 1
  const limite = Math.min(50, Math.max(1, Number(req.query.limite) || 10));
  const inicio = (pagina - 1) * limite;
  res.json({ pagina, limite, total: datos.length,
    paginas: Math.ceil(datos.length / limite),
    items: datos.slice(inicio, inicio + limite) });
});
app.listen(3000);
```
Probado: `?pagina=3&limite=10` → `{"pagina":3,"limite":10,"total":25,"paginas":3,"items":[{"id":21},...,{"id":25}]}`; con `limite=999&pagina=-4` → página 1 y límite 50.
:::

### 5️⃣ Tu propio rate limiter (medio)
Middleware `limitar(max, ventanaMs)`: máximo `max` peticiones por IP por ventana; si se pasa, responde **429** con la cabecera `Retry-After`.

::: desplegable 🧩 Ver la solución
```js
import express from "express";
const hits = new Map();                                  // ip → { n, reinicia }
const limitar = (max, ventanaMs) => (req, res, next) => {
  const ahora = Date.now();
  const r = hits.get(req.ip);
  if (!r || ahora > r.reinicia) { hits.set(req.ip, { n: 1, reinicia: ahora + ventanaMs }); return next(); }
  if (++r.n > max) {
    res.set("Retry-After", Math.ceil((r.reinicia - ahora) / 1000));
    return res.status(429).json({ error: "Demasiadas peticiones" });
  }
  next();
};
const app = express();
app.use(limitar(3, 10_000));
app.get("/", (req, res) => res.json({ ok: true }));
app.listen(3000);
// 4 curls seguidos → 200 200 200 429
```
Limitación: el `Map` vive en un solo proceso y crece sin límite. En producción usa `express-rate-limit` (con Redis si hay varios procesos).
:::

### 6️⃣ Contar errores sin cargar el archivo (medio)
Cuenta cuántas líneas tiene un log y cuántas contienen `ERROR`, aunque pese 5 GB.

::: desplegable 🧩 Ver la solución
```js
import { createReadStream } from "node:fs";
import { createInterface } from "node:readline";

let n = 0, errores = 0;
for await (const linea of createInterface({ input: createReadStream(process.argv[2]) })) {
  n++;
  if (linea.includes("ERROR")) errores++;
}
console.log(`${n} líneas, ${errores} con ERROR`);   // → 3 líneas, 1 con ERROR
```
La memoria usada es la de un pedazo (64 KB), no la del archivo.
:::

### 7️⃣ Reto: login con roles (difícil)
Añade `POST /api/login` (usuario `ana`, clave hasheada con bcrypt, devuelve un JWT de 15 min) y haz que `DELETE /api/libros/:id` exija rol `admin` (401 sin token, 403 con otro rol).

::: desplegable 🧩 Ver la pista y esquema
- Guarda el hash al arrancar: `const usuarios = { ana: { hash: await bcrypt.hash("cambia_esto", 12), rol: "admin" } }`.
- En el login compara con `bcrypt.compare`; si falla responde **401** con el mismo mensaje para "usuario no existe" y "clave mala" (no reveles cuál).
- Firma `jwt.sign({ sub: "ana", rol }, process.env.JWT_SECRET, { expiresIn: "15m" })`.
- Usa los middlewares `exigirLogin` y `exigirRol("admin")` de la sección de autenticación: `app.delete("/api/libros/:id", exigirLogin, exigirRol("admin"), ...)`.
- Prueba con curl: sin token → 401; token de otro rol → 403; admin → 204.
- Añade `rateLimit` de 5 intentos / 15 min al login.
:::

### 8️⃣ Reto: no bloquear el loop (difícil)
Un endpoint `GET /primos?hasta=5000000` cuenta primos con un bucle y congela el servidor. Muévelo a un `Worker` y comprueba con `monitorEventLoopDelay` que el loop sigue libre.

::: desplegable 🧩 Ver la pista y esquema
- Crea `primos.worker.js` con `parentPort.postMessage(contar(workerData))`, igual que el ejemplo de `fib`.
- En la ruta: `new Promise((ok, fallo) => { const w = new Worker(url, { workerData: hasta }); w.once("message", ok); w.once("error", fallo); })`.
- Limita `hasta` (zod o `Math.min`) para que nadie pida 10^12.
- Para muchos pedidos, usa un **pool** de workers (`piscina`) en vez de crear uno por petición.
:::

## 🎤 Preguntas de entrevista

::: desplegable ❓ ¿Qué es Node.js? ¿Es un lenguaje o un framework?
Ni lo uno ni lo otro: es un **runtime** de JavaScript construido sobre el motor **V8** y la librería **libuv**. Añade APIs que el navegador no tiene (`fs`, `http`, `process`) y un modelo de E/S **no bloqueante** dirigido por eventos.
:::

::: desplegable ❓ ¿Node es de un solo hilo? ¿Cómo atiende miles de conexiones?
Tu JavaScript corre en **un hilo**, pero la E/S de red la delega al sistema operativo (epoll/kqueue/IOCP) y la de archivos, DNS, crypto y zlib al **thread pool** de libuv (4 hilos). Cuando algo termina, el **event loop** ejecuta su callback. Funciona bien con mucha E/S y poca CPU; con CPU pesada hay que usar workers o servicios aparte.
:::

::: desplegable ❓ Explica las fases del event loop y la diferencia entre nextTick, promesas y setImmediate.
Fases: timers → pending → poll → check → close. Entre cada callback se vacía primero `process.nextTick`, luego las microtareas (promesas). `setTimeout(fn, 0)` va a la fase timers; `setImmediate` a check. Dentro de un callback de E/S, `setImmediate` siempre corre antes que `setTimeout(…, 0)`; en el nivel superior el orden no está garantizado.
:::

::: desplegable ❓ ¿Qué significa bloquear el event loop? Da un ejemplo y la solución.
Ejecutar algo síncrono y largo (un bucle de 1e9 iteraciones, `readFileSync` de un archivo grande, `bcrypt.hashSync`, una regex catastrófica) impide que se atienda a cualquier otro usuario. En la prueba, un cálculo de ~1,4 s hizo que desaparecieran 13 "latidos" de 100 ms. Soluciones: versiones async, streams, `worker_threads`, mover el trabajo a una cola o servicio.
:::

::: desplegable ❓ ESM vs CommonJS: diferencias prácticas.
CJS: `require`/`module.exports`, carga síncrona, `__dirname`. ESM: `import`/`export`, estándar del navegador, análisis estático (tree-shaking), `await` de nivel superior, `import.meta.dirname`, extensión obligatoria. Se activa con `"type": "module"` o `.mjs`. Desde Node 22.12 también se puede hacer `require()` de un ESM sin top-level await.
:::

::: desplegable ❓ ¿Qué es un middleware en Express y qué pasa si olvidas llamar a next()?
Una función `(req, res, next)` que forma una cadena. Si no responde ni llama a `next()`, la petición queda **colgada** hasta que el cliente cierra por timeout. Con `next(err)` se salta al manejador de errores (el de 4 parámetros).
:::

::: desplegable ❓ ¿Cómo manejas errores en una API de Node?
Lanzas errores propios con código (`HttpError(404, ...)`), validas la entrada (zod), usas `async/await` con `try/catch` (en Express 5 los errores async llegan solos al manejador), un **manejador central** al final que responde 4xx con mensaje claro y 5xx con "Error interno" (el detalle va al log), y una red de seguridad con `unhandledRejection`/`uncaughtException` que registra y reinicia.
:::

::: desplegable ❓ ¿Sesiones o JWT? ¿Dónde guardas el token?
Sesiones (cookie con ID, estado en el servidor): más simples y fáciles de revocar; ideales para webs clásicas. JWT (firmado, sin estado): cómodos entre servicios y apps móviles, difíciles de revocar, el payload es legible. El token debe ir en una cookie `httpOnly; Secure; SameSite`, no en `localStorage` (por XSS). Contraseñas siempre con bcrypt/argon2.
:::

::: desplegable ❓ ¿Qué es un stream y qué es el backpressure?
Un flujo que se procesa por pedazos, sin cargar todo en memoria. El backpressure es el mecanismo por el que un destino lento frena al origen para no llenar la RAM. `pipeline()` conecta streams, maneja el backpressure y cierra todo ante un error.
:::

::: desplegable ❓ ¿worker_threads, child_process o cluster?
`worker_threads`: CPU pesada dentro del mismo proceso (hilos con su propio V8). `child_process`: ejecutar otro programa (git, ffmpeg) con `execFile`/`spawn`. `cluster`: varias copias de tu servidor que comparten un puerto para usar todos los núcleos (hoy suele hacerse con PM2 o contenedores).
:::

::: desplegable ❓ ¿Cómo proteges una app Node de ataques a la cadena de suministro?
Lockfile en git y `npm ci`; pocas dependencias; revisar mantenimiento y nombre antes de instalar; `npm audit` y `npm audit signatures` en CI; 2FA en npm/GitHub; no ejecutar scripts de instalación que no necesitas (`--ignore-scripts`, npm 12 los bloquea por defecto); Dependabot/Renovate; y el modelo `--permission` de Node para limitar lo que puede hacer el proceso. Casos conocidos: left-pad (2016), event-stream (2018).
:::

::: desplegable ❓ ¿Cuándo NO usarías Node?
Cálculo numérico intensivo o IA (Python/C++), procesamiento de video en el mismo proceso, sistemas de latencia muy estricta o con mucha CPU por petición (Go, Rust, Java). Para esos casos Node puede ser la capa de API y delegar el trabajo pesado a un servicio especializado.
:::

::: desplegable ❓ ¿Qué es la diferencia entre 401 y 403?
401: no estás autenticado (no sabemos quién eres o el token es malo). 403: estás autenticado pero **no tienes permiso** para esa acción.
:::

## 🇬🇧 Vocabulario esencial de Node

| English | Suena | Español |
|---|---|---|
| runtime | /rántaim/ | entorno de ejecución |
| event loop | /ivént lup/ | bucle de eventos |
| callback | /kólbak/ | función de retorno |
| promise | /prómis/ | promesa |
| middleware | /mídoluer/ | función intermedia |
| endpoint | /éndpoint/ | punto de entrada de la API |
| payload | /péilóud/ | cuerpo/datos enviados |
| stream | /strim/ | flujo de datos |
| buffer | /báfer/ | bloque de bytes |
| thread pool | /zred pul/ | grupo de hilos |
| dependency | /dipéndensi/ | dependencia |
| lockfile | /lókfail/ | archivo de versiones fijas |
| supply chain attack | /suplái chein atak/ | ataque a la cadena de suministro |
| rate limit | /réit límit/ | límite de peticiones |
| deploy | /diplói/ | desplegar |
| graceful shutdown | /gréisful shátdaun/ | apagado ordenado |
| memory leak | /mémori lik/ | fuga de memoria |
| bottleneck | /bótolnek/ | cuello de botella |

## 📌 Resumen final (la chuleta de bolsillo)

📌 Node = V8 + libuv: **un hilo** que delega la E/S y ejecuta callbacks desde el **event loop**. Brilla con mucha E/S; nunca lo bloquees.
📌 Orden de colas: código síncrono → `nextTick` → promesas → timers → poll (E/S) → `setImmediate` → close.
📌 Proyecto nuevo: `"type": "module"`, `node:` en los imports, `import.meta.dirname`, `--watch`, `--env-file`, `node --test`.
📌 Dependencias: `npm ci` en producción, lockfile en git, `npm audit`, pocas librerías; los secretos en `.env` fuera de git.
📌 Express: `express.json()` → logs → rutas → 404 → manejador de errores de 4 parámetros, **en ese orden**; valida con zod.
📌 REST: sustantivos en plural, método = acción, 201 al crear, 204 al borrar, 400/401/403/404 con mensajes claros.
📌 BD: consultas parametrizadas, un `Pool` global, cuidado con N+1; bcrypt para claves; JWT en cookie `httpOnly`.
📌 CPU pesada → `worker_threads`; otro programa → `execFile`; todos los núcleos → PM2/contenedores.
📌 Seguridad: helmet + rate limit + límite de body + validación; CORS no protege tu API; revisa cada dependencia.
📌 Futuro: TypeScript sin compilar, `--permission`, más librería estándar y Web APIs, menos dependencias.

| Quiero... | Comando / API |
|---|---|
| ejecutar y recargar | `node --watch --env-file=.env app.js` |
| instalar exacto | `npm ci --omit=dev` |
| leer archivo grande | `createReadStream` + `pipeline` |
| consulta segura | `pool.query("... $1", [valor])` |
| hash de clave | `await bcrypt.hash(clave, 12)` |
| tests | `node --test` o `npx vitest run` |
| medir el loop | `monitorEventLoopDelay()` |
| auditar | `npm audit` + `npm audit signatures` |
