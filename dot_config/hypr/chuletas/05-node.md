# 🟩 Node.js
> JavaScript fuera del navegador: npm, archivos, servidores, Express, APIs REST, bases de datos y scripts, con ejemplos que funcionan.

## 🟩 Qué es Node y cuándo usarlo

**Node.js** es un programa que ejecuta JavaScript fuera del navegador, usando el mismo motor V8 de Chrome. Con él JS puede hacer lo que un navegador no deja: leer y escribir archivos, abrir puertos de red, hablar con bases de datos y ejecutar comandos del sistema.

Su superpoder es la **E/S no bloqueante** (non-blocking I/O): mientras espera la base de datos o la red, atiende otras peticiones con un solo hilo y el event loop (el mismo de la hoja de JavaScript). Por eso es excelente para servidores con muchas conexiones que esperan mucho y calculan poco.

| Úsalo para | Mejor otra cosa para |
|---|---|
| APIs REST y backends web | cálculo numérico pesado o IA (Python, C++) |
| tiempo real: chats, websockets | procesar video en el mismo hilo del servidor |
| herramientas de línea de comandos (CLI) | scripts de ciencia de datos (Python + pandas) |
| herramientas de frontend (Vite, ESLint, Prettier) | sistemas embebidos muy pequeños |
| bots (Discord, Telegram) y automatizaciones | |

- `node` :: Abre el REPL: escribe JS y ve el resultado al instante (.exit para salir)
- `node app.js` :: Ejecuta un archivo
- `node -e "console.log(2 + 2)"` :: Ejecuta una línea suelta
- `node -p "process.version"` :: Ejecuta e imprime el resultado

📌 Diferencias con el navegador: en Node NO hay `document`, `window` ni `localStorage`; en cambio hay `process`, `fs`, `http` y módulos `node:*`. `fetch`, `console`, `setTimeout`, `URL` y `crypto` existen en ambos.
💡 Consejo: el frontend (React, Vue) también usa Node aunque la app corra en el navegador: Vite, npm y los compiladores son programas de Node.
🇬🇧 **runtime** /rántaim/ = entorno de ejecución · **backend** /bákend/ = parte del servidor · **non-blocking** /non blóking/ = no bloqueante · **I/O** /ái óu/ = entrada/salida · **server** /sérver/ = servidor · **REPL** /répol/ = consola interactiva

### ⬇️ Instalar y versiones

Node publica una versión nueva cada 6 meses. Las versiones **pares** se vuelven **LTS** (Long Term Support: soporte largo) y son las que se usan en producción. Lo más cómodo es instalarlo con un gestor de versiones (fnm o nvm), así cambias de versión por proyecto sin pelearte con permisos.

- `node -v` :: Versión de Node (ej. v24.x)
- `npm -v` :: Versión de npm (viene con Node)
- `sudo pacman -S nodejs npm` :: Instalar en Arch / CachyOS
- `curl -fsSL https://fnm.vercel.app/install | bash` :: Instalar fnm (gestor de versiones)
- `fnm install --lts` :: Instalar la última LTS
- `fnm use 22` :: Usar la versión 22 en esta terminal
- `echo "22" > .nvmrc` :: Fijar la versión del proyecto (fnm y nvm la leen)
- `which node` :: Ver qué node se está usando

```bash
node -v                     # → v24.11.0 (o la que tengas)
node -p "process.versions.v8"   # versión del motor V8
node                        # REPL interactivo
> [1, 2, 3].map(x => x * 2)
[ 2, 4, 6 ]
> .exit
```

⚠️ Cuidado: no instales paquetes globales con `sudo npm install -g`; da problemas de permisos. Con fnm/nvm no necesitas sudo.
💡 Consejo: para aprender usa la LTS más reciente; las funciones de esta hoja (fetch, --watch, --env-file, node:sqlite) necesitan Node 22 o más.
🇬🇧 **LTS (long-term support)** /long term sapórt/ = soporte a largo plazo · **release** /rilís/ = publicación · **version manager** /vérshon mánayer/ = gestor de versiones · **install** /instól/ = instalar · **upgrade** /ápgreid/ = actualizar

## 📦 npm y package.json

**npm** es el gestor de paquetes de Node: descarga librerías de npmjs.com a la carpeta `node_modules`. El archivo **package.json** es el "DNI" del proyecto: nombre, versión, scripts y la lista de dependencias. **package-lock.json** guarda las versiones exactas instaladas para que todos tengan lo mismo; se sube a git, `node_modules` no.

**dependencies** son paquetes que la app necesita para funcionar (express, pg). **devDependencies** solo se usan al desarrollar (nodemon, eslint, vitest) y no se instalan en producción con `npm ci --omit=dev`.

- `npm init -y` :: Crea package.json con valores por defecto
- `npm install express` :: Instala y guarda en dependencies (corto: npm i)
- `npm install -D nodemon` :: Instala como devDependency
- `npm install` :: Instala todo lo que dice package.json
- `npm ci` :: Instalación limpia y exacta desde el lock (para CI y servidores)
- `npm uninstall express` :: Desinstala
- `npm run dev` :: Ejecuta el script "dev"
- `npm start; npm test` :: Atajos de los scripts start y test (sin "run")
- `npm outdated` :: Paquetes con versiones más nuevas
- `npm update` :: Actualiza dentro del rango permitido
- `npm ls --depth=0` :: Lista lo instalado
- `npm audit` :: Busca vulnerabilidades conocidas
- `npx cowsay hola` :: Ejecuta un paquete sin instalarlo de forma permanente
- `npx serve .` :: Servidor estático rápido para probar un HTML
- `node --run dev` :: Ejecuta un script sin pasar por npm (Node 22+, más rápido)

```json
{
  "name": "mi-api",
  "version": "1.0.0",
  "type": "module",
  "main": "src/server.js",
  "scripts": {
    "dev": "node --watch --env-file=.env src/server.js",
    "start": "node src/server.js",
    "test": "node --test"
  },
  "dependencies": {
    "cors": "^2.8.5",
    "express": "^5.1.0"
  },
  "devDependencies": {
    "nodemon": "^3.1.10"
  },
  "engines": {
    "node": ">=22"
  }
}
```

### 🔢 Semver: qué significan ^ y ~

Las versiones siguen **semver** `MAYOR.MENOR.PARCHE`: el parche corrige bugs, el menor añade funciones sin romper nada, el mayor puede romper tu código.

| Escrito | Acepta | Ejemplo con 4.18.2 |
|---|---|---|
| `4.18.2` | exactamente esa | solo 4.18.2 |
| `~4.18.2` | parches nuevos | 4.18.3, 4.18.9 (no 4.19) |
| `^4.18.2` | menores y parches (por defecto) | 4.19.0, 4.99.0 (no 5.0) |
| `>=4.0.0` | cualquiera desde ahí | 5.0, 6.0… (arriesgado) |
| `*` o `latest` | la que sea | evítalo |

⚠️ Cuidado: nunca subas `node_modules` a git; añade `node_modules/` y `.env` al `.gitignore`.
⚠️ Cuidado: un paquete en devDependencies que tu servidor usa al arrancar hará fallar el despliegue ("Cannot find package").
💡 Consejo: antes de instalar una librería mira en npmjs.com sus descargas semanales, la fecha del último cambio y si tiene tipos; menos dependencias = menos problemas.
🇬🇧 **package** /pákech/ = paquete · **dependency** /dipéndensi/ = dependencia · **lockfile** /lókfail/ = archivo de versiones fijas · **script** /skript/ = guion/comando · **semantic versioning** /semántik vérshoning/ = versionado semántico · **breaking change** /bréiking chéinch/ = cambio que rompe

## 🔗 Módulos: ESM vs CommonJS

Node tiene dos sistemas de módulos. **CommonJS** (CJS) es el viejo: `require` y `module.exports`. **ES Modules** (ESM) es el estándar moderno, el mismo del navegador: `import` y `export`. Para proyectos nuevos usa ESM poniendo `"type": "module"` en package.json. Los módulos que vienen con Node se importan con el prefijo `node:`.

| | ESM (moderno) | CommonJS (viejo) |
|---|---|---|
| importar | `import fs from "node:fs";` | `const fs = require("fs");` |
| exportar | `export function f() {}` | `module.exports = { f };` |
| se activa con | `"type": "module"` o `.mjs` | por defecto o `.cjs` |
| await arriba del todo | sí (top-level await) | no |
| carpeta actual | `import.meta.dirname` | `__dirname` |
| extensión en rutas | obligatoria `./db.js` | opcional `./db` |

- `import { readFile } from "node:fs/promises";` :: Importar una función de un módulo de Node
- `import express from "express";` :: Importar un paquete de npm
- `import { db } from "./db.js";` :: Importar tu propio archivo (con .js)
- `import datos from "./datos.json" with { type: "json" };` :: Importar un JSON en ESM
- `import { createRequire } from "node:module";` :: Usar require dentro de ESM (casos raros)
- `const { f } = require("./util");` :: CommonJS: importar
- `module.exports = { f };` :: CommonJS: exportar

```js
// src/utils/precio.js
export const IVA = 0.13;
export const conIva = p => Math.round(p * (1 + IVA) * 100) / 100;

// src/app.js
import { conIva } from "./utils/precio.js";
import os from "node:os";
console.log(conIva(50), os.platform());   // → 56.5 linux
```

⚠️ Cuidado: el error "Cannot use import statement outside a module" significa que falta `"type": "module"` en package.json.
⚠️ Cuidado: el error "require is not defined in ES module scope" es el caso contrario: estás en ESM, cambia `require` por `import`.
💡 Consejo: siempre escribe `node:fs`, `node:path`… con el prefijo: queda claro que es de Node y no un paquete de npm.
🇬🇧 **module** /módiul/ = módulo · **require** /rikuáier/ = requerir · **built-in** /bilt in/ = incorporado · **top-level await** /top lével euéit/ = await en el nivel superior · **resolve** /risólv/ = resolver (encontrar el archivo)

## 📁 Archivos con fs/promises

El módulo **fs** (file system) lee y escribe archivos. Usa la versión de promesas `node:fs/promises` con `await`: no bloquea el servidor mientras el disco trabaja. Las versiones `...Sync` bloquean todo; solo úsalas en scripts pequeños o al arrancar.

- `await readFile("notas.txt", "utf8")` :: Leer un archivo de texto
- `await writeFile("salida.txt", texto)` :: Escribir (reemplaza el contenido)
- `await appendFile("log.txt", "línea\n")` :: Añadir al final
- `await readdir("carpeta")` :: Lista de nombres de archivos
- `await readdir(".", { withFileTypes: true })` :: Con info: e.isDirectory(), e.isFile()
- `await readdir(".", { recursive: true })` :: Incluye subcarpetas
- `await mkdir("a/b/c", { recursive: true })` :: Crear carpetas (no falla si existen)
- `await rm("tmp", { recursive: true, force: true })` :: Borrar carpeta y contenido
- `await rename("viejo.txt", "nuevo.txt")` :: Renombrar o mover
- `await copyFile("a.txt", "b.txt")` :: Copiar
- `await stat("a.txt")` :: Tamaño, fechas: s.size, s.mtime
- `await access("a.txt")` :: Lanza error si no existe
- `existsSync("a.txt")` :: ¿Existe? (de node:fs, síncrono pero muy usado)

```js
import { readFile, writeFile, readdir, mkdir, stat } from "node:fs/promises";

await mkdir("datos", { recursive: true });

// Guardar y leer JSON
const tareas = [{ id: 1, texto: "Estudiar Node", hecha: false }];
await writeFile("datos/tareas.json", JSON.stringify(tareas, null, 2));
const leidas = JSON.parse(await readFile("datos/tareas.json", "utf8"));
console.log(leidas[0].texto);                 // → Estudiar Node

// Listar con tamaños
for (const entrada of await readdir("datos", { withFileTypes: true })) {
  if (entrada.isFile()) {
    const info = await stat(`datos/${entrada.name}`);
    console.log(entrada.name, info.size, "bytes"); // → tareas.json 73 bytes
  }
}
```

### ✅ Ejemplo resuelto: leer un archivo que quizá no existe

```js
import { readFile, writeFile } from "node:fs/promises";

async function leerJSON(ruta, porDefecto) {
  try {
    return JSON.parse(await readFile(ruta, "utf8"));
  } catch (err) {
    if (err.code === "ENOENT") return porDefecto;   // ENOENT = "no existe ese archivo"
    throw err;                                      // otro error (permisos, JSON roto): avisar
  }
}

const config = await leerJSON("config.json", { tema: "oscuro", visitas: 0 });
config.visitas++;
await writeFile("config.json", JSON.stringify(config));
console.log("Visitas:", config.visitas);           // → Visitas: 1 (2, 3… en cada ejecución)
```

| Código de error | Significa |
|---|---|
| `ENOENT` | no existe el archivo o carpeta |
| `EACCES` | sin permisos |
| `EEXIST` | ya existe |
| `EISDIR` | es una carpeta y esperabas un archivo |
| `EADDRINUSE` | el puerto ya está ocupado (servidores) |

⚠️ Cuidado: las rutas relativas (`"datos/x.json"`) son relativas a la carpeta DESDE donde ejecutas node, no a la del archivo. Usa `import.meta.dirname` (siguiente sección).
⚠️ Cuidado: sin `"utf8"` readFile devuelve un Buffer (bytes), no texto.
🇬🇧 **file system** /fáil sístem/ = sistema de archivos · **read** /rid/ = leer · **write** /ráit/ = escribir · **directory** /dairéktori/ = carpeta · **path** /paz/ = ruta · **encoding** /enkóuding/ = codificación · **buffer** /báfer/ = bloque de bytes

## 🧭 path y __dirname en ESM

Las rutas cambian entre sistemas (Linux usa `/`, Windows `\`). El módulo **path** las arma bien en cualquiera. En ESM no existen `__dirname` ni `__filename`; en Node moderno se usan `import.meta.dirname` (carpeta del archivo actual) e `import.meta.filename`.

- `import path from "node:path";` :: Importar path
- `path.join("datos", "fotos", "a.jpg")` :: Une partes → datos/fotos/a.jpg
- `path.resolve("datos")` :: Ruta absoluta desde la carpeta actual
- `path.basename("/a/b/foto.jpg")` :: → foto.jpg
- `path.basename("foto.jpg", ".jpg")` :: → foto (sin extensión)
- `path.extname("foto.jpg")` :: → .jpg
- `path.dirname("/a/b/foto.jpg")` :: → /a/b
- `path.parse("/a/b/foto.jpg")` :: Objeto con root, dir, base, ext, name
- `import.meta.dirname` :: Carpeta del archivo actual (ESM, Node 20.11+)
- `import.meta.filename` :: Ruta completa del archivo actual
- `fileURLToPath(import.meta.url)` :: Forma antigua de obtener __filename (de node:url)
- `process.cwd()` :: Carpeta desde donde se ejecutó node
- `os.homedir()` :: Carpeta del usuario (/home/yafer)

```js
import path from "node:path";
import { readFile } from "node:fs/promises";

const RAIZ = import.meta.dirname;                    // carpeta de ESTE archivo
const rutaDatos = path.join(RAIZ, "datos", "tareas.json");

console.log(path.basename(rutaDatos));               // → tareas.json
console.log(path.extname(rutaDatos));                // → .json
console.log(path.parse("/home/ana/foto.png").name);  // → foto

// Funciona igual aunque ejecutes `node src/app.js` desde otra carpeta
const texto = await readFile(rutaDatos, "utf8").catch(() => "[]");
console.log(Array.isArray(JSON.parse(texto)));       // → true
```

⚠️ Cuidado: no concatenes rutas a mano con `+ "/" +`: se rompe en Windows y con barras repetidas. Usa `path.join`.
💡 Consejo: si un ejemplo viejo usa `__dirname` y tú estás en ESM, cámbialo por `import.meta.dirname`.
🇬🇧 **absolute path** /ábsolut paz/ = ruta absoluta · **relative path** /rélativ paz/ = ruta relativa · **working directory** /uérking dairéktori/ = carpeta de trabajo · **extension** /iksténshon/ = extensión · **separator** /séparéitor/ = separador

## ⚙️ process: argv, env, exit

`process` es un objeto global con información del programa que se está ejecutando: los argumentos que le pasaste (**argv**), las variables de entorno (**env**), la carpeta actual, y métodos para terminar con un código de salida. Por convención, código 0 = todo bien y cualquier otro = error (la terminal y los scripts lo usan para saber si falló).

- `process.argv` :: Array: [ruta de node, ruta del script, ...tus argumentos]
- `process.argv.slice(2)` :: Solo tus argumentos
- `process.env.PORT` :: Leer una variable de entorno (siempre string o undefined)
- `process.exit(1)` :: Terminar con código de error
- `process.exitCode = 1` :: Marcar error y dejar que termine solo (más limpio)
- `process.cwd()` :: Carpeta actual
- `process.platform` :: "linux", "win32", "darwin"
- `process.memoryUsage()` :: Memoria usada
- `process.on("SIGINT", fn)` :: Al presionar Ctrl+C
- `process.on("uncaughtException", fn)` :: Error no atrapado (último recurso)
- `process.stdout.write("sin salto")` :: Escribir sin salto de línea
- `process.stdin` :: Entrada estándar (lo que escribe el usuario o un pipe)

```js
// saludo.js  →  node saludo.js Ana 3
const [nombre = "mundo", veces = "1"] = process.argv.slice(2);
const n = Number(veces);

if (Number.isNaN(n) || n < 1) {
  console.error("Uso: node saludo.js <nombre> <veces>");
  process.exit(1);                         // sale con error
}
for (let i = 0; i < n; i++) console.log(`Hola, ${nombre}!`);
console.log("Modo:", process.env.NODE_ENV ?? "development");
// → Hola, Ana! (3 veces) / Modo: development
```

```bash
node saludo.js Ana 3
NODE_ENV=production node saludo.js Ana   # pasar una variable solo a este comando
node saludo.js Ana cero; echo $?        # → Uso: ... y luego 1 (código de salida)
```

💡 Consejo: para opciones tipo `--puerto 3000 -v` no partas argv a mano: usa `parseArgs` de `node:util` (ver la sección de scripts CLI).
🇬🇧 **argument** /árguiument/ = argumento · **environment** /enváironment/ = entorno · **exit code** /éksit kóud/ = código de salida · **signal** /sígnal/ = señal · **standard output** /stándard áutput/ = salida estándar

## 🔐 Variables de entorno y .env

Las contraseñas, claves de API y datos que cambian según el lugar (tu PC, el servidor) NO se escriben en el código: van en **variables de entorno**. En desarrollo se guardan en un archivo `.env` que **nunca** se sube a git. Node moderno lo lee solo con `--env-file`, sin instalar `dotenv`.

- `node --env-file=.env app.js` :: Carga .env antes de arrancar (Node 20.6+)
- `node --env-file-if-exists=.env app.js` :: Igual pero no falla si no existe
- `process.loadEnvFile()` :: Cargar .env desde el código (Node 21.7+)
- `process.env.DATABASE_URL` :: Leer la variable
- `import "dotenv/config";` :: Alternativa clásica con el paquete dotenv (npm i dotenv)
- `.env.example` :: Plantilla SIN valores reales que sí se sube a git

```bash
# .env  (añádelo a .gitignore)
PORT=3000
NODE_ENV=development
DATABASE_URL=postgres://yafer:secreto@localhost:5432/tienda
API_KEY=sk-123456
```

### ✅ Ejemplo resuelto: config validada al arrancar

```js
// src/config.js — lee y valida TODO al inicio: si falta algo, falla rápido y claro
function requerida(nombre) {
  const valor = process.env[nombre];
  if (!valor) throw new Error(`Falta la variable de entorno ${nombre} (revisa tu .env)`);
  return valor;
}

export const config = {
  port: Number(process.env.PORT ?? 3000),         // número con valor por defecto
  esProduccion: process.env.NODE_ENV === "production",
  apiKey: requerida("API_KEY"),                    // obligatoria
};
console.log(`Puerto ${config.port}, producción: ${config.esProduccion}`);
// con .env → Puerto 3000, producción: false
// sin API_KEY → Error: Falta la variable de entorno API_KEY (revisa tu .env)
```

⚠️ Cuidado: si subiste un `.env` con claves a GitHub, bórralo no basta: las claves quedaron en el historial. **Cámbialas** (rota las claves) de inmediato.
⚠️ Cuidado: todo en `process.env` es texto: `process.env.DEBUG === "false"` es un string truthy. Compara explícitamente.
💡 Consejo: en el servidor (Render, Railway, VPS) las variables se configuran en el panel o en el servicio, no con un .env subido.
🇬🇧 **environment variable** /enváironment vérieibol/ = variable de entorno · **secret** /síkret/ = secreto · **API key** /ei pi ái ki/ = clave de API · **credentials** /kredénshals/ = credenciales · **leak** /lik/ = filtración

## 📡 Eventos y streams

Mucho de Node funciona con **eventos**: un objeto avisa "pasó algo" (`emit`) y los que lo escuchan (`on`) reaccionan. Servidores, streams y procesos son EventEmitters.

Un **stream** procesa datos **por pedazos** (chunks) en vez de cargar todo en memoria. Es la diferencia entre ver una película en streaming y esperar a descargar los 4 GB. Con streams puedes leer un archivo de 10 GB usando pocos MB de RAM. `pipeline` conecta streams: leer → transformar → escribir.

- `import { EventEmitter } from "node:events";` :: Importar la clase base
- `emisor.on("evento", fn)` :: Escuchar (cada vez)
- `emisor.once("evento", fn)` :: Escuchar solo la primera vez
- `emisor.emit("evento", datos)` :: Disparar el evento
- `emisor.off("evento", fn)` :: Dejar de escuchar
- `createReadStream("big.log")` :: Leer un archivo por pedazos (de node:fs)
- `createWriteStream("out.txt")` :: Escribir por pedazos
- `await pipeline(origen, transformar, destino)` :: Conectar streams con manejo de errores (node:stream/promises)
- `readline.createInterface({ input })` :: Leer línea por línea
- `for await (const linea of rl) { }` :: Recorrer las líneas de un stream

```js
import { EventEmitter } from "node:events";

class Pedidos extends EventEmitter {
  crear(plato) {
    const pedido = { id: Date.now(), plato };
    this.emit("nuevo", pedido);               // avisa a todos los que escuchan
    return pedido;
  }
}
const pedidos = new Pedidos();
pedidos.on("nuevo", p => console.log("🍳 Cocina prepara:", p.plato));
pedidos.on("nuevo", p => console.log("🧾 Caja registra:", p.plato));
pedidos.crear("silpancho");
// → 🍳 Cocina prepara: silpancho / 🧾 Caja registra: silpancho
```

### ✅ Ejemplo resuelto: comprimir y contar líneas de un archivo grande

```js
import { createReadStream, createWriteStream } from "node:fs";
import { writeFile } from "node:fs/promises";
import { pipeline } from "node:stream/promises";
import { createGzip } from "node:zlib";
import readline from "node:readline";

// Preparar un "log" de ejemplo con 100 000 líneas
const lineas = Array.from({ length: 100_000 }, (_, i) => `${i % 10 === 0 ? "ERROR" : "INFO"} evento ${i}`);
await writeFile("app.log", lineas.join("\n"));

// 1) Comprimir sin cargar todo en memoria: leer → gzip → escribir
await pipeline(createReadStream("app.log"), createGzip(), createWriteStream("app.log.gz"));
console.log("Comprimido ✅");

// 2) Contar errores línea por línea
const rl = readline.createInterface({ input: createReadStream("app.log") });
let errores = 0;
for await (const linea of rl) {
  if (linea.startsWith("ERROR")) errores++;
}
console.log("Errores:", errores);   // → Errores: 10000
```

💡 Consejo: si un archivo cabe de sobra en memoria (unos MB), `readFile` es más simple. Usa streams para archivos grandes, descargas y respuestas HTTP largas.
⚠️ Cuidado: si emites un evento `"error"` y nadie lo escucha, Node lanza el error y el programa se cae. Escucha siempre `"error"` en streams y emisores.
🇬🇧 **event emitter** /ivént imíter/ = emisor de eventos · **listener** /lísener/ = oyente · **stream** /strim/ = flujo · **chunk** /chank/ = pedazo · **pipe** /páip/ = tubería · **compress** /komprés/ = comprimir

## 🌍 Servidor http nativo

Node trae el módulo **http** para crear servidores sin instalar nada. Cada petición llega con `req` (lo que pide el cliente: método, URL, cabeceras, cuerpo) y respondes con `res` (código, cabeceras y cuerpo). Es útil para entender cómo funciona por dentro; para apps reales se usa Express, que construye sobre esto.

- `http.createServer((req, res) => { })` :: Crear el servidor
- `server.listen(3000, () => { })` :: Escuchar en el puerto 3000
- `req.method; req.url; req.headers` :: Método (GET, POST…), ruta y cabeceras
- `new URL(req.url, "http://localhost")` :: Parsear ruta y query
- `res.writeHead(200, { "Content-Type": "application/json" })` :: Código y cabeceras
- `res.end(JSON.stringify(datos))` :: Enviar el cuerpo y terminar
- `for await (const chunk of req) { }` :: Leer el cuerpo de la petición por pedazos

### ✅ Ejemplo resuelto: mini API sin librerías

```js
import http from "node:http";

const frases = ["El que madruga, Dios lo ayuda", "Poco a poco se anda lejos"];

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);
  const enviar = (codigo, datos) => {
    res.writeHead(codigo, { "Content-Type": "application/json; charset=utf-8" });
    res.end(JSON.stringify(datos));
  };

  if (req.method === "GET" && url.pathname === "/frases") {
    const limite = Number(url.searchParams.get("limite") ?? frases.length); // ?limite=1
    return enviar(200, frases.slice(0, limite));
  }
  if (req.method === "POST" && url.pathname === "/frases") {
    let cuerpo = "";
    for await (const chunk of req) cuerpo += chunk;   // juntar el cuerpo
    const { texto } = JSON.parse(cuerpo || "{}");
    if (!texto) return enviar(400, { error: "Falta texto" });
    frases.push(texto);
    return enviar(201, { ok: true, total: frases.length });
  }
  enviar(404, { error: "Ruta no encontrada" });
});

server.listen(3000, () => console.log("🚀 http://localhost:3000"));
```

```bash
curl localhost:3000/frases?limite=1
# → ["El que madruga, Dios lo ayuda"]
curl -X POST localhost:3000/frases -H "Content-Type: application/json" -d '{"texto":"Más vale tarde que nunca"}'
# → {"ok":true,"total":3}
curl localhost:3000/otra
# → {"error":"Ruta no encontrada"}
```

⚠️ Cuidado: "EADDRINUSE: address already in use :::3000" = ya hay otro servidor en ese puerto. Ciérralo (Ctrl+C en su terminal) o usa otro puerto. `ss -ltnp | grep 3000` te dice quién lo usa.
💡 Consejo: `curl` es tu mejor amigo para probar APIs desde la terminal; en VS Code la extensión REST Client o Thunder Client hace lo mismo con botones.
🇬🇧 **request** /rikuést/ = petición · **response** /rispóns/ = respuesta · **port** /port/ = puerto · **listen** /lísen/ = escuchar · **route** /rut/ o /ráut/ = ruta · **query string** /kuíri string/ = parámetros de la URL

## 🚂 Express

**Express** es el framework web más usado de Node. Te da **rutas** limpias (`app.get("/usuarios/:id")`), lee el cuerpo JSON, sirve archivos estáticos y organiza el código con **middleware**: funciones que se ejecutan en cadena antes de llegar a la ruta. Cada middleware recibe `(req, res, next)` y o responde, o llama a `next()` para pasar al siguiente.

Piensa en la petición como alguien que entra a un edificio: pasa por recepción (log), seguridad (autenticación), y recién llega a la oficina (la ruta). Cualquiera en el camino puede detenerlo.

- `npm install express` :: Instalar (Express 5)
- `const app = express();` :: Crear la app
- `app.use(express.json())` :: Leer cuerpos JSON en req.body
- `app.use(express.static("public"))` :: Servir HTML/CSS/JS/imágenes de la carpeta public
- `app.get("/ruta", (req, res) => { })` :: Ruta GET (también post, put, patch, delete)
- `req.params.id` :: Parámetro de ruta: /usuarios/:id → /usuarios/7
- `req.query.q` :: Query string: /buscar?q=hola
- `req.body` :: Cuerpo de la petición (con express.json)
- `req.get("Authorization")` :: Leer una cabecera
- `res.json(datos)` :: Responder JSON
- `res.status(201).json(datos)` :: Con código de estado
- `res.sendStatus(204)` :: Solo el código, sin cuerpo
- `res.send("<h1>Hola</h1>")` :: Responder texto/HTML
- `res.redirect("/login")` :: Redirigir
- `app.use((req, res, next) => { next(); })` :: Middleware global
- `const router = express.Router();` :: Agrupar rutas en otro archivo
- `app.use("/api/tareas", router)` :: Montar el router con un prefijo
- `app.use((err, req, res, next) => { })` :: Manejador de errores (4 parámetros)

```js
import express from "express";

const app = express();
app.use(express.json());                        // 1. body JSON → req.body
app.use(express.static("public"));              // 2. archivos estáticos

// 3. middleware propio: log de cada petición con su duración
app.use((req, res, next) => {
  const inicio = Date.now();
  res.on("finish", () => console.log(`${req.method} ${req.url} → ${res.statusCode} (${Date.now() - inicio} ms)`));
  next();                                       // ¡sin next() la petición se queda colgada!
});

// 4. middleware de una ruta: "seguridad"
function soloConClave(req, res, next) {
  if (req.get("x-api-key") !== "secreto") return res.status(401).json({ error: "Sin clave" });
  next();
}

app.get("/", (req, res) => res.send("Hola desde Express 👋"));
app.get("/saludo/:nombre", (req, res) => {
  const { nombre } = req.params;                // /saludo/Ana
  const { idioma = "es" } = req.query;          // ?idioma=en
  res.json({ mensaje: idioma === "en" ? `Hello, ${nombre}` : `Hola, ${nombre}` });
});
app.post("/eco", (req, res) => res.status(201).json({ recibido: req.body }));
app.get("/admin", soloConClave, (req, res) => res.json({ secreto: 42 }));
app.get("/falla", async () => {
  throw new Error("Algo explotó");              // Express 5 pasa errores async al manejador
});

// 5. 404: ninguna ruta coincidió
app.use((req, res) => res.status(404).json({ error: `No existe ${req.method} ${req.path}` }));

// 6. manejador de errores: SIEMPRE al final y con 4 parámetros
app.use((err, req, res, next) => {
  console.error("💥", err.message);
  res.status(err.status ?? 500).json({ error: err.status ? err.message : "Error interno" });
});

app.listen(3000, () => console.log("🚀 http://localhost:3000"));
```

```bash
curl "localhost:3000/saludo/Ana?idioma=en"        # → {"mensaje":"Hello, Ana"}
curl -X POST localhost:3000/eco -H "Content-Type: application/json" -d '{"a":1}'   # → {"recibido":{"a":1}}
curl localhost:3000/admin                          # → {"error":"Sin clave"}
curl -H "x-api-key: secreto" localhost:3000/admin  # → {"secreto":42}
curl localhost:3000/falla                          # → {"error":"Error interno"}
curl localhost:3000/nada                           # → {"error":"No existe GET /nada"}
```

📌 El orden importa: Express prueba los middleware y rutas de arriba a abajo. JSON y estáticos primero, rutas en medio, 404 y errores al final.
⚠️ Cuidado: si `req.body` sale `undefined`, falta `app.use(express.json())` o el cliente no envió `Content-Type: application/json`.
⚠️ Cuidado: responder dos veces (`res.json` y luego otro `res.json`) da "Cannot set headers after they are sent". Usa `return res...` para cortar.
🇬🇧 **framework** /fréimuerk/ = marco de trabajo · **middleware** /mídoluer/ = función intermedia · **route handler** /rut jándler/ = manejador de ruta · **router** /ráuter/ = enrutador · **static files** /státik fáils/ = archivos estáticos · **next** /nekst/ = siguiente

## 🧪 API REST CRUD completa con Express

**REST** es una forma de diseñar APIs: cada **recurso** (tareas, usuarios) tiene una URL y el **método HTTP** dice qué hacer con él. **CRUD** = Create, Read, Update, Delete: las cuatro operaciones básicas de cualquier app.

| Método | Ruta | Acción | Respuesta |
|---|---|---|---|
| GET | `/api/tareas` | listar (con filtros ?hecha=true) | 200 + array |
| GET | `/api/tareas/:id` | ver una | 200 o 404 |
| POST | `/api/tareas` | crear | 201 + la tarea creada |
| PUT | `/api/tareas/:id` | reemplazar completa | 200 o 404 |
| PATCH | `/api/tareas/:id` | cambiar solo algunos campos | 200 o 404 |
| DELETE | `/api/tareas/:id` | borrar | 204 sin cuerpo |

### ✅ Ejemplo resuelto: API de tareas (en memoria)

```js
// src/server.js — npm init -y && npm i express  (y "type": "module")
import express from "express";

const app = express();
app.use(express.json());

let tareas = [
  { id: 1, titulo: "Aprender Express", hecha: false },
  { id: 2, titulo: "Practicar inglés", hecha: true },
];
let siguienteId = 3;

// Error con código HTTP para lanzarlo desde cualquier ruta
class HttpError extends Error {
  constructor(status, message) { super(message); this.status = status; }
}
const buscar = id => {
  const tarea = tareas.find(t => t.id === Number(id));
  if (!tarea) throw new HttpError(404, `No existe la tarea ${id}`);
  return tarea;
};
const validar = ({ titulo, hecha } = {}, parcial = false) => {   // = {} por si no llega body
  if (!parcial || titulo !== undefined)
    if (typeof titulo !== "string" || !titulo.trim()) throw new HttpError(400, "titulo es obligatorio");
  if (hecha !== undefined && typeof hecha !== "boolean") throw new HttpError(400, "hecha debe ser true/false");
};

// READ: listar con filtro y búsqueda opcionales
app.get("/api/tareas", (req, res) => {
  let resultado = tareas;
  if (req.query.hecha) resultado = resultado.filter(t => String(t.hecha) === req.query.hecha);
  if (req.query.q) resultado = resultado.filter(t => t.titulo.toLowerCase().includes(req.query.q.toLowerCase()));
  res.json(resultado);
});

// READ: una
app.get("/api/tareas/:id", (req, res) => res.json(buscar(req.params.id)));

// CREATE
app.post("/api/tareas", (req, res) => {
  validar(req.body);
  const nueva = { id: siguienteId++, titulo: req.body.titulo.trim(), hecha: req.body.hecha ?? false };
  tareas.push(nueva);
  res.status(201).location(`/api/tareas/${nueva.id}`).json(nueva);
});

// UPDATE completo
app.put("/api/tareas/:id", (req, res) => {
  const tarea = buscar(req.params.id);
  validar(req.body);
  Object.assign(tarea, { titulo: req.body.titulo.trim(), hecha: req.body.hecha ?? false });
  res.json(tarea);
});

// UPDATE parcial
app.patch("/api/tareas/:id", (req, res) => {
  const tarea = buscar(req.params.id);
  validar(req.body, true);
  const { titulo, hecha } = req.body;             // solo copiamos campos permitidos
  if (titulo !== undefined) tarea.titulo = titulo.trim();
  if (hecha !== undefined) tarea.hecha = hecha;
  res.json(tarea);
});

// DELETE
app.delete("/api/tareas/:id", (req, res) => {
  buscar(req.params.id);
  tareas = tareas.filter(t => t.id !== Number(req.params.id));
  res.sendStatus(204);
});

app.use((req, res) => res.status(404).json({ error: "Ruta no encontrada" }));
app.use((err, req, res, next) => {
  if (err.type === "entity.parse.failed") return res.status(400).json({ error: "JSON inválido" });
  res.status(err.status ?? 500).json({ error: err.status ? err.message : "Error interno" });
});

const PORT = Number(process.env.PORT ?? 3000);
app.listen(PORT, () => console.log(`✅ API en http://localhost:${PORT}/api/tareas`));
```

```bash
curl localhost:3000/api/tareas
# → [{"id":1,"titulo":"Aprender Express","hecha":false},{"id":2,"titulo":"Practicar inglés","hecha":true}]
curl "localhost:3000/api/tareas?hecha=true"
# → [{"id":2,"titulo":"Practicar inglés","hecha":true}]
curl -X POST localhost:3000/api/tareas -H "Content-Type: application/json" -d '{"titulo":"Desplegar API"}'
# → {"id":3,"titulo":"Desplegar API","hecha":false}
curl -X PATCH localhost:3000/api/tareas/3 -H "Content-Type: application/json" -d '{"hecha":true}'
# → {"id":3,"titulo":"Desplegar API","hecha":true}
curl -X POST localhost:3000/api/tareas -H "Content-Type: application/json" -d '{"titulo":""}'
# → {"error":"titulo es obligatorio"}
curl -i -X DELETE localhost:3000/api/tareas/1
# → HTTP/1.1 204 No Content
curl localhost:3000/api/tareas/99
# → {"error":"No existe la tarea 99"}
```

Qué hace cada parte: `buscar` y `validar` lanzan `HttpError` con el código correcto, así las rutas quedan cortas y todo error termina en UN solo manejador al final. `Object.assign` y el PATCH copian solo campos permitidos (nunca `req.body` entero, para que nadie se cambie el `id`). Para que los datos sobrevivan a un reinicio, cambia el array por una base de datos (sección siguiente a CORS).

💡 Consejo: usa sustantivos en plural para las rutas (`/api/tareas`), nunca verbos (`/api/crearTarea`): el verbo ya lo pone el método HTTP.
⚠️ Cuidado: nunca confíes en lo que llega en `req.body`; valida tipos y largos. Para validaciones grandes se usa la librería **zod**.
🇬🇧 **CRUD (create, read, update, delete)** /krad/ = crear, leer, actualizar, borrar · **resource** /rísors/ = recurso · **endpoint** /éndpoint/ = punto de la API · **status code** /stéitus kóud/ = código de estado · **payload** /péiloud/ = datos enviados

## 🤝 CORS

El navegador, por seguridad, bloquea que una página de un **origen** (protocolo + dominio + puerto, ej. `http://localhost:5173`) lea respuestas de OTRO origen (ej. tu API en `http://localhost:3000`). Esto es la **política del mismo origen**. **CORS** (Cross-Origin Resource Sharing) es el mecanismo para que el SERVIDOR diga "este origen sí puede": lo hace con cabeceras como `Access-Control-Allow-Origin`.

Para peticiones "no simples" (JSON con POST/PUT/DELETE, cabeceras propias) el navegador primero envía una petición **preflight** con método OPTIONS para preguntar permiso. El paquete `cors` responde todo eso por ti.

- `npm install cors` :: Instalar el middleware
- `app.use(cors())` :: Permitir CUALQUIER origen (solo para pruebas)
- `app.use(cors({ origin: "http://localhost:5173" }))` :: Permitir solo tu frontend
- `cors({ origin: ["https://miapp.com", "http://localhost:5173"] })` :: Varios orígenes
- `cors({ credentials: true, origin })` :: Permitir cookies (origen no puede ser *)
- `res.set("Access-Control-Allow-Origin", "*")` :: La cabecera a mano, sin paquete

```js
import express from "express";
import cors from "cors";

const app = express();
const PERMITIDOS = (process.env.CORS_ORIGINS ?? "http://localhost:5173").split(",");

app.use(cors({
  origin: PERMITIDOS,                       // solo estos orígenes leen la API
  methods: ["GET", "POST", "PUT", "PATCH", "DELETE"],
}));
app.use(express.json());
app.get("/api/ping", (req, res) => res.json({ pong: true }));
app.listen(3000);
```

```bash
curl -i -H "Origin: http://localhost:5173" localhost:3000/api/ping | grep -i access-control
# → Access-Control-Allow-Origin: http://localhost:5173
```

⚠️ Cuidado: CORS lo aplica el **navegador**. curl, Postman y otro servidor no tienen CORS: si allí funciona y en el navegador no, es CORS.
⚠️ Cuidado: CORS no es seguridad para tu API: cualquiera puede llamarla con curl. Para proteger datos necesitas autenticación.
💡 Consejo: en desarrollo con Vite puedes evitar CORS con el proxy de `vite.config.js` (`server.proxy`), así el frontend llama a `/api` en su mismo origen.
🇬🇧 **origin** /óriyin/ = origen · **cross-origin** /kros óriyin/ = entre orígenes distintos · **preflight** /prífláit/ = petición previa de permiso · **allow** /aláu/ = permitir · **policy** /pólisi/ = política · **blocked** /blokt/ = bloqueado

## 🗄️ Base de datos: SQLite y Postgres

Guardar en un array se pierde al reiniciar; un archivo JSON se corrompe si dos peticiones escriben a la vez. Una **base de datos** resuelve eso. **SQLite** es una base de datos en un solo archivo, perfecta para aprender y para apps pequeñas; Node 22+ la trae incorporada en `node:sqlite` (sin instalar nada). **PostgreSQL** es la base de datos de servidor más recomendada para producción; desde Node se usa con el paquete `pg`.

Regla de oro: usa **consultas parametrizadas** (`?` en SQLite, `$1` en Postgres) y NUNCA metas datos del usuario dentro del SQL con template literals, o te harán **inyección SQL**.

- `import { DatabaseSync } from "node:sqlite";` :: SQLite incorporado en Node 22+
- `const db = new DatabaseSync("app.db");` :: Abre o crea el archivo
- `db.exec("CREATE TABLE ...")` :: Ejecutar SQL sin resultados
- `db.prepare("SELECT * FROM t WHERE id = ?")` :: Preparar consulta con parámetros
- `stmt.all(...params)` :: Todas las filas (array de objetos)
- `stmt.get(...params)` :: Una fila (o undefined)
- `stmt.run(...params)` :: INSERT/UPDATE/DELETE → { changes, lastInsertRowid }
- `npm install pg` :: Cliente de PostgreSQL
- `new pg.Pool({ connectionString })` :: Grupo de conexiones a Postgres
- `await pool.query("SELECT * FROM t WHERE id = $1", [id])` :: Consulta Postgres → result.rows

### ✅ Ejemplo resuelto: tareas persistentes con SQLite

```js
// src/db.js
import { DatabaseSync } from "node:sqlite";

export const db = new DatabaseSync(process.env.DB_FILE ?? "tareas.db");
db.exec(`
  CREATE TABLE IF NOT EXISTS tareas (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT    NOT NULL,
    hecha  INTEGER NOT NULL DEFAULT 0          -- SQLite no tiene boolean: 0/1
  )
`);

const q = {
  listar: db.prepare("SELECT id, titulo, hecha = 1 AS hecha FROM tareas ORDER BY id"),
  una:    db.prepare("SELECT id, titulo, hecha = 1 AS hecha FROM tareas WHERE id = ?"),
  crear:  db.prepare("INSERT INTO tareas (titulo, hecha) VALUES (?, ?)"),
  marcar: db.prepare("UPDATE tareas SET hecha = ? WHERE id = ?"),
  borrar: db.prepare("DELETE FROM tareas WHERE id = ?"),
};
const aBool = t => t && { ...t, hecha: Boolean(t.hecha) };

export const Tareas = {
  listar: () => q.listar.all().map(aBool),
  una: id => aBool(q.una.get(id)),
  crear: (titulo, hecha = false) => {
    const { lastInsertRowid } = q.crear.run(titulo, hecha ? 1 : 0);   // ? evita inyección SQL
    return Tareas.una(lastInsertRowid);
  },
  marcar: (id, hecha) => q.marcar.run(hecha ? 1 : 0, id).changes > 0,
  borrar: id => q.borrar.run(id).changes > 0,                           // true si borró algo
};

// prueba rápida: node src/db.js
if (import.meta.filename === process.argv[1]) {
  const t = Tareas.crear("Aprender SQLite");
  Tareas.marcar(t.id, true);
  console.log(Tareas.una(t.id));         // → { id: 1, titulo: 'Aprender SQLite', hecha: true }
  console.log(Tareas.borrar(999));       // → false
}
```

Y en Express las rutas solo llaman al modelo:

```js
import express from "express";
import { Tareas } from "./db.js";

const app = express();
app.use(express.json());
app.get("/api/tareas", (req, res) => res.json(Tareas.listar()));
app.post("/api/tareas", (req, res) => {
  if (!req.body?.titulo?.trim()) return res.status(400).json({ error: "titulo es obligatorio" });
  res.status(201).json(Tareas.crear(req.body.titulo.trim()));
});
app.delete("/api/tareas/:id", (req, res) =>
  Tareas.borrar(Number(req.params.id)) ? res.sendStatus(204) : res.status(404).json({ error: "No existe" })
);
app.listen(3000, () => console.log("💾 API con SQLite en :3000"));
```

### 🐘 Lo mismo con PostgreSQL

```js
// npm install pg   ·   .env → DATABASE_URL=postgres://usuario:clave@localhost:5432/tienda
import pg from "pg";

const pool = new pg.Pool({ connectionString: process.env.DATABASE_URL });

await pool.query(`CREATE TABLE IF NOT EXISTS tareas (
  id SERIAL PRIMARY KEY, titulo TEXT NOT NULL, hecha BOOLEAN NOT NULL DEFAULT false)`);

const { rows } = await pool.query(
  "INSERT INTO tareas (titulo) VALUES ($1) RETURNING *",   // $1, $2… = parámetros
  ["Aprender Postgres"]
);
console.log(rows[0]);           // → { id: 1, titulo: 'Aprender Postgres', hecha: false }
await pool.end();               // cerrar al terminar un script (en un servidor, no)
```

⚠️ Cuidado: meter datos del usuario en el SQL con un template literal (`... WHERE titulo = '${req.query.t}'`) es inyección SQL. Siempre `?` o `$1` con los valores aparte.
💡 Consejo: cuando el proyecto crezca, un ORM/query builder como **Drizzle** o **Prisma** te da tipos y migraciones; aprende primero SQL a mano (ver la hoja de SQL).
💡 Consejo: para probar Postgres sin instalarlo: `docker run -d -e POSTGRES_PASSWORD=clave -p 5432:5432 postgres:17` (ver la hoja de Docker).
🇬🇧 **database** /déitabeis/ = base de datos · **query** /kuíri/ = consulta · **table** /téibol/ = tabla · **row** /róu/ = fila · **prepared statement** /pripérd stéitment/ = consulta preparada · **SQL injection** /es kiu el inyékshon/ = inyección SQL · **connection pool** /konékshon pul/ = grupo de conexiones

## ☁️ Llamar APIs externas con fetch

Node 18+ trae `fetch` igual que el navegador, así que tu backend puede consumir otras APIs (clima, pagos, IA) sin instalar axios. Una razón importante para hacerlo desde el backend: **esconder la clave de API**. El frontend llama a tu servidor, y tu servidor (que tiene la clave en `.env`) llama al servicio externo.

- `const res = await fetch(url)` :: GET
- `if (!res.ok) throw new Error(...)` :: fetch no falla con 404/500: revísalo tú
- `await res.json()` :: Cuerpo como objeto
- `fetch(url, { headers: { Authorization: "Bearer " + key } })` :: Enviar la clave
- `signal: AbortSignal.timeout(5000)` :: Rendirse a los 5 segundos
- `new URLSearchParams({ lat, lon })` :: Armar la query sin errores de escape

### ✅ Ejemplo resuelto: clima de La Paz con Open-Meteo (sin clave)

```js
async function clima(lat, lon) {
  const params = new URLSearchParams({
    latitude: lat, longitude: lon,
    current: "temperature_2m,wind_speed_10m",
    timezone: "America/La_Paz",
  });
  const res = await fetch(`https://api.open-meteo.com/v1/forecast?${params}`, {
    signal: AbortSignal.timeout(8000),
  });
  if (!res.ok) throw new Error(`Open-Meteo respondió ${res.status}`);
  const { current } = await res.json();                 // desestructurar lo que interesa
  return { temperatura: current.temperature_2m, viento: current.wind_speed_10m };
}

const ciudades = { "La Paz": [-16.5, -68.15], "Santa Cruz": [-17.78, -63.18] };
const resultados = await Promise.all(                    // en paralelo
  Object.entries(ciudades).map(async ([nombre, [lat, lon]]) => ({ nombre, ...(await clima(lat, lon)) }))
);
console.table(resultados);
// → tabla: La Paz 10.9 °C · Santa Cruz 22.5 °C (cambia según el día y la hora)
```

### 🔁 Reintentos con espera creciente

```js
async function fetchConReintentos(url, intentos = 3) {
  for (let i = 1; i <= intentos; i++) {
    try {
      const res = await fetch(url, { signal: AbortSignal.timeout(5000) });
      if (res.status >= 500) throw new Error(`HTTP ${res.status}`);  // reintentar solo fallos del servidor
      return res;
    } catch (err) {
      if (i === intentos) throw err;
      await new Promise(r => setTimeout(r, 500 * 2 ** i));          // 1 s, 2 s, 4 s…
    }
  }
}
```

⚠️ Cuidado: nunca pongas la clave de una API de pago en el frontend: cualquiera la ve en DevTools. Pásala por tu backend.
💡 Consejo: respeta los límites (rate limit) de las APIs: si responden 429 Too Many Requests, espera antes de reintentar.
🇬🇧 **third-party** /zerd párti/ = de terceros · **rate limit** /réit límit/ = límite de peticiones · **retry** /ritrái/ = reintentar · **timeout** /táimaut/ = tiempo de espera agotado · **bearer token** /bérer tóuken/ = token portador

## 🖥️ Scripts de línea de comandos

Node es genial para automatizar: renombrar fotos, convertir CSV a JSON, generar reportes. Un script CLI lee argumentos con `parseArgs`, puede preguntar al usuario con `readline` y ejecutar otros programas con `child_process`. Con un **shebang** (`#!/usr/bin/env node`) y permiso de ejecución se usa como cualquier comando.

- `#!/usr/bin/env node` :: Primera línea: ejecutar el archivo con node
- `chmod +x renombrar.js` :: Darle permiso de ejecución
- `import { parseArgs } from "node:util";` :: Leer opciones como --salida x -v
- `import { createInterface } from "node:readline/promises";` :: Preguntar en la terminal
- `await rl.question("¿Nombre? ")` :: Esperar respuesta del usuario
- `import { execFile } from "node:child_process";` :: Ejecutar otro programa
- `"bin": { "micli": "./cli.js" }` :: En package.json: nombre del comando
- `npm link` :: Instalar tu CLI localmente para probarla en cualquier carpeta
- `import { styleText } from "node:util";` :: Colores en la terminal sin librerías

### ✅ Ejemplo resuelto: CSV → JSON con opciones

```js
#!/usr/bin/env node
// csv2json.js — uso: node csv2json.js notas.csv --salida notas.json --separador ";"
import { parseArgs, styleText } from "node:util";
import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";

const { values, positionals } = parseArgs({
  allowPositionals: true,
  options: {
    salida:    { type: "string", short: "o" },
    separador: { type: "string", short: "s", default: "," },
    ayuda:     { type: "boolean", short: "h" },
  },
});

if (values.ayuda || positionals.length === 0) {
  console.log("Uso: csv2json <archivo.csv> [-o salida.json] [-s ;]");
  process.exit(values.ayuda ? 0 : 1);
}

const entrada = positionals[0];
const [cabecera, ...filas] = (await readFile(entrada, "utf8")).trim().split(/\r?\n/);
const columnas = cabecera.split(values.separador);

const datos = filas.map(fila => {
  const celdas = fila.split(values.separador);
  return Object.fromEntries(columnas.map((col, i) => {
    const v = celdas[i]?.trim() ?? "";
    return [col.trim(), v !== "" && !Number.isNaN(Number(v)) ? Number(v) : v]; // números como número
  }));
});

const salida = values.salida ?? path.basename(entrada, path.extname(entrada)) + ".json";
await writeFile(salida, JSON.stringify(datos, null, 2));
console.log(styleText("green", `✔ ${datos.length} filas → ${salida}`));
```

```bash
printf "nombre;nota\nAna;95\nLuis;48\n" > notas.csv
node csv2json.js notas.csv -s ";"
# → ✔ 2 filas → notas.json
cat notas.json
# → [ { "nombre": "Ana", "nota": 95 }, { "nombre": "Luis", "nota": 48 } ]
```

### 💬 Preguntar al usuario

```js
import { createInterface } from "node:readline/promises";

const rl = createInterface({ input: process.stdin, output: process.stdout });
const nombre = await rl.question("¿Cómo te llamas? ");
const edad = Number(await rl.question("¿Edad? "));
console.log(`Hola ${nombre}, en 10 años tendrás ${edad + 10}`); // → Hola Ana, en 10 años tendrás 30
rl.close();                                  // sin close() el programa no termina
```

⚠️ Cuidado: con `exec("rm " + archivo)` un nombre como `"x; rm -rf ~"` ejecuta comandos ajenos. Usa `execFile("rm", [archivo])`, que pasa los argumentos separados.
💡 Consejo: para CLIs grandes existen `commander` (opciones) y `@clack/prompts` (menús bonitos), pero `parseArgs` y `readline` cubren lo básico sin dependencias.
🇬🇧 **command line** /kománd láin/ = línea de comandos · **shebang** /shibáng/ = línea #! inicial · **flag / option** /flag, ópshon/ = opción · **prompt** /prompt/ = pregunta/indicador · **child process** /cháild próses/ = proceso hijo

## 🔄 Recargar solo: --watch y nodemon

Mientras programas un servidor, reiniciarlo a mano tras cada cambio es tedioso. `node --watch` (incorporado) o **nodemon** (paquete) vigilan tus archivos y reinician el proceso solos al guardar. Para el frontend, Vite ya hace esto (con recarga en caliente).

- `node --watch src/server.js` :: Reinicia al cambiar cualquier archivo importado
- `node --watch-path=src src/server.js` :: Vigilar solo una carpeta
- `node --watch --env-file=.env src/server.js` :: Con variables de entorno
- `npm install -D nodemon` :: Instalar nodemon como devDependency
- `npx nodemon src/server.js` :: Reinicia al cambiar archivos .js, .json…
- `nodemon --ext js,json,sql` :: Elegir qué extensiones vigila
- `rs` :: En nodemon: escribe rs + Enter para reiniciar a mano
- `node --test --watch` :: Repetir los tests al guardar

```json
{
  "scripts": {
    "dev": "node --watch --env-file-if-exists=.env src/server.js",
    "dev:nodemon": "nodemon --ext js,json src/server.js",
    "start": "node src/server.js"
  }
}
```

💡 Consejo: `--watch` es suficiente para casi todo y no necesita instalar nada; usa nodemon si necesitas vigilar archivos que no se importan (plantillas, .sql).
⚠️ Cuidado: no uses --watch ni nodemon en producción; ahí el servidor lo mantiene vivo systemd, pm2 o la plataforma.
🇬🇧 **watch** /uách/ = vigilar · **reload** /rilóud/ = recargar · **hot reload** /jot rilóud/ = recarga en caliente · **restart** /ristárt/ = reiniciar · **development** /divélopment/ = desarrollo

## 🏗️ Estructura de proyecto y despliegue

Un proyecto ordenado separa responsabilidades: **rutas** (qué URL), **controladores** (qué hacer con la petición), **servicios/modelos** (lógica y base de datos). Al principio basta con pocos archivos; separa cuando un archivo pase de ~200 líneas.

```text
mi-api/
├── package.json
├── package-lock.json
├── .env              ← secretos locales (NO a git)
├── .env.example      ← plantilla sin valores (sí a git)
├── .gitignore        ← node_modules/  .env  *.db
├── public/           ← frontend estático (index.html, app.js, estilos.css)
├── src/
│   ├── server.js     ← arranca: app.listen(PORT)
│   ├── app.js        ← crea la app, middleware, monta routers
│   ├── config.js     ← lee y valida process.env
│   ├── db.js         ← conexión a la base de datos
│   ├── routes/
│   │   └── tareas.routes.js
│   ├── controllers/
│   │   └── tareas.controller.js
│   └── middleware/
│       └── errores.js
└── test/
    └── tareas.test.js
```

```js
// src/routes/tareas.routes.js — un Router por recurso
import { Router } from "express";
import { Tareas } from "../db.js";

export const tareasRouter = Router();
tareasRouter.get("/", (req, res) => res.json(Tareas.listar()));
tareasRouter.get("/:id", (req, res) => {
  const t = Tareas.una(Number(req.params.id));
  t ? res.json(t) : res.status(404).json({ error: "No existe" });
});

// src/app.js
// import { tareasRouter } from "./routes/tareas.routes.js";
// app.use("/api/tareas", tareasRouter);
```

### 🧪 Tests con el runner incorporado

```js
// test/precio.test.js  →  node --test
import { test } from "node:test";
import assert from "node:assert/strict";

const conIva = p => Math.round(p * 1.13 * 100) / 100;

test("suma el 13% de IVA", () => {
  assert.equal(conIva(100), 113);
  assert.equal(conIva(0), 0);
});
// → ✔ suma el 13% de IVA · tests 1 · pass 1
```

### 🚀 Despliegue básico

| Opción | Ideal para | Cómo |
|---|---|---|
| Render / Railway | primera API, gratis o barato | conectas el repo de GitHub, build `npm ci`, start `npm start`, variables en el panel |
| Vercel / Netlify | frontend + funciones serverless | `npx vercel` o conectar el repo |
| VPS (Ubuntu) | control total, varias apps | git pull + `npm ci --omit=dev` + systemd o pm2 + nginx delante |
| Docker | mismo entorno en todos lados | Dockerfile con `node:22-slim` (ver la hoja de Docker) |

```bash
# En un VPS: preparar y dejar corriendo con pm2
git clone https://github.com/usuario/mi-api.git && cd mi-api
npm ci --omit=dev                     # solo dependencias de producción
cp .env.example .env && nano .env     # poner los valores reales
npx pm2 start src/server.js --name mi-api
npx pm2 save && npx pm2 startup       # que arranque solo al reiniciar el servidor
npx pm2 logs mi-api                   # ver logs en vivo
```

📌 Checklist antes de desplegar: el puerto sale de `process.env.PORT` · secretos en variables de entorno · `NODE_ENV=production` · CORS solo con tu dominio · manejador de errores que no muestra el stack al usuario · `npm audit` sin vulnerabilidades graves.
⚠️ Cuidado: SQLite en Render/Vercel se borra en cada despliegue (disco efímero). En esas plataformas usa una base de datos gestionada (Postgres de Render, Neon, Supabase).
💡 Consejo: añade una ruta `GET /health` que responda `{ ok: true }`; las plataformas la usan para saber si tu app está viva.
🇬🇧 **deploy** /diplói/ = desplegar · **production** /prodákshon/ = producción · **build** /bild/ = construir · **health check** /jelz chek/ = chequeo de salud · **logs** /logs/ = registros · **serverless** /sérverles/ = sin servidor propio

## 🏆 Ejemplos resueltos completos

### ✅ Ejemplo resuelto: frontend + API en el mismo servidor

```js
// server.js — sirve public/index.html y una API en /api; sin CORS porque es el mismo origen
import express from "express";
import path from "node:path";

const app = express();
const visitas = new Map();                                   // contador por página

app.use(express.json());
app.use(express.static(path.join(import.meta.dirname, "public")));

app.post("/api/visitas", (req, res) => {
  const pagina = String(req.body?.pagina ?? "inicio");
  visitas.set(pagina, (visitas.get(pagina) ?? 0) + 1);
  res.status(201).json({ pagina, visitas: visitas.get(pagina) });
});
app.get("/api/visitas", (req, res) => res.json(Object.fromEntries(visitas)));
app.get("/health", (req, res) => res.json({ ok: true, uptime: Math.round(process.uptime()) }));

app.listen(process.env.PORT ?? 3000, () => console.log("🌐 http://localhost:3000"));

// public/app.js (navegador):
// const r = await fetch("/api/visitas", { method: "POST", headers: { "Content-Type": "application/json" },
//                                          body: JSON.stringify({ pagina: "inicio" }) });
// console.log(await r.json());   // → { pagina: 'inicio', visitas: 1 }
```

### ✅ Ejemplo resuelto: organizar descargas por tipo (script)

```js
// ordenar.js — uso: node ordenar.js ~/Descargas --probar
import { readdir, mkdir, rename } from "node:fs/promises";
import path from "node:path";

const TIPOS = {
  Imagenes: [".jpg", ".jpeg", ".png", ".webp", ".gif"],
  Documentos: [".pdf", ".docx", ".txt", ".md"],
  Videos: [".mp4", ".mkv", ".webm"],
  Comprimidos: [".zip", ".rar", ".7z", ".tar", ".gz"],
};
const carpetaDe = ext =>
  Object.entries(TIPOS).find(([, exts]) => exts.includes(ext.toLowerCase()))?.[0] ?? "Otros";

const [dir = ".", bandera] = process.argv.slice(2);
const probar = bandera === "--probar";                       // solo muestra, no mueve

const resumen = {};
for (const e of await readdir(dir, { withFileTypes: true })) {
  if (!e.isFile()) continue;                                 // saltar carpetas
  const destino = carpetaDe(path.extname(e.name));
  resumen[destino] = (resumen[destino] ?? 0) + 1;
  if (!probar) {
    await mkdir(path.join(dir, destino), { recursive: true });
    await rename(path.join(dir, e.name), path.join(dir, destino, e.name));
  }
}
console.log(probar ? "🔎 Simulación:" : "✅ Movidos:", resumen);
// → 🔎 Simulación: { Imagenes: 12, Documentos: 5, Otros: 2 }
```

Qué hace: `readdir` con `withFileTypes` separa archivos de carpetas, `carpetaDe` busca la extensión en la tabla `TIPOS` (con `find` + `?.[0]` + `??` para el caso "Otros"), y la bandera `--probar` permite ver qué pasaría antes de mover nada. Siempre añade un modo de prueba a los scripts que mueven o borran archivos.

### ✅ Ejemplo resuelto: proxy seguro a una API con clave

```js
// El frontend llama a /api/traducir; la clave vive solo en el servidor (.env → TRAD_KEY)
import express from "express";

const app = express();
app.use(express.json({ limit: "10kb" }));                   // limitar tamaño del body

app.post("/api/traducir", async (req, res, next) => {
  const { texto } = req.body ?? {};
  if (typeof texto !== "string" || texto.length > 500)
    return res.status(400).json({ error: "texto (máx. 500 caracteres) es obligatorio" });
  try {
    const r = await fetch("https://api.ejemplo-traductor.com/v1/translate", {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${process.env.TRAD_KEY}` },
      body: JSON.stringify({ text: texto, from: "es", to: "en" }),
      signal: AbortSignal.timeout(10_000),
    });
    if (!r.ok) return res.status(502).json({ error: "El servicio de traducción falló" });
    const { translation } = await r.json();
    res.json({ original: texto, ingles: translation });
  } catch (err) {
    next(err);                                               // al manejador de errores
  }
});

app.use((err, req, res, next) => res.status(500).json({ error: "Error interno" }));
app.listen(3000);
```

📌 Resumen del camino Node: `npm init` → `"type": "module"` → Express + `express.json()` → rutas REST → validación → base de datos con consultas parametrizadas → `.env` para secretos → CORS solo para tu frontend → `--watch` en desarrollo → desplegar con `npm ci --omit=dev`.
🇬🇧 **proxy** /próksi/ = intermediario · **full stack** /ful stak/ = frontend y backend · **side project** /sáid próyekt/ = proyecto personal · **bad gateway (502)** /bad guéituei/ = el servicio de atrás falló · **wrap up** /rap ap/ = resumir/cerrar
