# ⚛️ React
> Construye interfaces con componentes: JSX, props, estado, hooks, rutas, datos de APIs y despliegue (React 18/19).

## 🤔 Qué es React y por qué usarlo

React es una **librería de JavaScript para construir interfaces de usuario**. La idea central: en vez de escribir una página gigante, la armas con **componentes**, piezas pequeñas y reutilizables, como bloques de LEGO. Un botón, una tarjeta de producto o un menú son componentes.

Con JavaScript "puro" tú le dices al navegador **cómo** cambiar la página paso a paso (busca este div, cámbiale el texto, añade una clase...). Con React le dices **qué** quieres ver según los datos, y React se encarga del cómo. A esto se le llama programación **declarativa**.

### 🧠 El Virtual DOM explicado simple

Tocar el DOM real (la página) es lento, como repintar toda una casa cada vez que mueves un cuadro. React guarda una **copia ligera en memoria** (el Virtual DOM). Cuando cambian los datos, crea una copia nueva, **compara** ambas (a esto se le llama *reconciliation*) y solo cambia en la página real lo que de verdad cambió. Es como comparar dos fotos y retocar solo las diferencias.

- `UI = f(estado)` :: La fórmula mental de React: la interfaz es una función de los datos
- `componente` :: Función que devuelve lo que se ve (JSX)
- `props` :: Datos que un componente padre le pasa a un hijo (como parámetros)
- `estado (state)` :: Datos internos que cambian con el tiempo; al cambiar, React vuelve a dibujar
- `render` :: Cuando React ejecuta tu componente para saber qué mostrar
- `hook` :: Función especial que empieza con `use` (useState, useEffect...) y da "superpoderes" al componente

```jsx
// Un componente es solo una función que devuelve JSX
function Saludo() {
  return <h1>¡Hola desde Bolivia! 🇧🇴</h1>;
}

export default Saludo;
```

📌 React es la "vista" (lo que se ve). Para rutas, datos o estado global se combinan librerías: React Router, Zustand, TanStack Query...
💡 Antes de React domina bien JavaScript moderno: `map`, `filter`, desestructuración, spread `...`, arrow functions, `async/await` e import/export.
⚠️ React no es un framework completo como Angular; Next.js sí es un framework construido sobre React.
🇬🇧 **component** /kəm-PÓU-nent/ = componente · **library** /LÁI-bre-ri/ = librería · **render** /RÉN-der/ = dibujar/renderizar · **declarative** /di-KLÉ-ra-tiv/ = declarativo · **UI (user interface)** /iú-ái/ = interfaz de usuario

## 🚀 Crear un proyecto con Vite

**Vite** (se pronuncia /vit/, "rápido" en francés) es la herramienta recomendada para crear proyectos React: arranca en milisegundos y recarga al instante cuando guardas. `create-react-app` ya está obsoleto, no lo uses.

- `npm create vite@latest mi-app -- --template react` :: Crea un proyecto React con JavaScript
- `npm create vite@latest mi-app -- --template react-ts` :: Igual pero con TypeScript
- `cd mi-app && npm install` :: Entra a la carpeta e instala dependencias
- `npm run dev` :: Servidor de desarrollo (normalmente en http://localhost:5173)
- `npm run build` :: Genera la versión optimizada en `dist/`
- `npm run preview` :: Prueba localmente la versión de `dist/`
- `npm install react-router-dom zustand` :: Instalar librerías extra

```bash
npm create vite@latest tareas-app -- --template react
cd tareas-app
npm install
npm run dev
```

### 📁 Estructura de carpetas

```text
mi-app/
├── index.html          ← única página HTML; tiene <div id="root">
├── package.json        ← dependencias y scripts (dev, build...)
├── vite.config.js      ← configuración de Vite
├── public/             ← archivos estáticos (favicon, imágenes fijas)
└── src/
    ├── main.jsx        ← punto de entrada: monta <App /> en #root
    ├── App.jsx         ← componente principal
    ├── index.css       ← estilos globales
    ├── components/     ← componentes reutilizables (Boton, Tarjeta...)
    ├── pages/          ← páginas para las rutas (Inicio, Perfil...)
    ├── hooks/          ← hooks personalizados (useFetch...)
    └── context/        ← contextos (TemaContext...)
```

```jsx
// src/main.jsx — así arranca la app
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App.jsx";
import "./index.css";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <App />
  </StrictMode>
);
```

💡 Las carpetas `components/`, `pages/`, `hooks/` no vienen por defecto: créalas tú para mantener orden desde el día uno.
⚠️ `StrictMode` en desarrollo ejecuta algunos efectos **dos veces** a propósito para detectar errores. Si ves tu `console.log` duplicado, es normal.
🇬🇧 **scaffold** /SKÁ-fold/ = andamio, generar la base · **dependency** /di-PÉN-den-si/ = dependencia · **build** /bild/ = compilar/construir · **dev server** = servidor de desarrollo · **entry point** = punto de entrada

## 🧩 JSX: HTML dentro de JavaScript

**JSX** parece HTML pero es JavaScript. Vite lo transforma en llamadas a funciones que crean elementos. Tiene unas pocas reglas que debes memorizar.

### 📏 Las reglas de oro

- `return ( <div>...</div> )` :: Regla 1: devolver UN solo elemento padre
- `<>...</>` :: Fragmento: padre "invisible" que no agrega un div extra al HTML
- `className="caja"` :: Regla 2: `class` es palabra reservada en JS, se usa `className`
- `htmlFor="email"` :: En `<label>` se usa `htmlFor` en vez de `for`
- `<img src={url} />` :: Regla 3: toda etiqueta se cierra, también `<br />` e `<input />`
- `{nombre}` :: Regla 4: las llaves `{}` meten cualquier **expresión** JS
- `onClick`, `onChange`, `tabIndex` :: Regla 5: atributos en camelCase
- `style={{ color: "red", fontSize: 18 }}` :: Estilo en línea: un objeto (por eso doble llave)
- `{/* comentario */}` :: Comentario dentro de JSX

```jsx
function Perfil() {
  const nombre = "Yafer";
  const edad = 22;
  const avatar = "https://i.pravatar.cc/100";

  return (
    <>
      <h2 className="titulo">Hola, {nombre.toUpperCase()}</h2>
      <img src={avatar} alt="Foto de perfil" />
      <p>El próximo año tendrás {edad + 1} años.</p>
      <p style={{ color: edad >= 18 ? "green" : "orange" }}>
        {edad >= 18 ? "Mayor de edad" : "Menor de edad"}
      </p>
      {/* Esto es un comentario en JSX */}
    </>
  );
}
```

📌 Dentro de `{}` va una **expresión** (algo que da un valor: `2+2`, `x ? a : b`, `lista.map(...)`). No caben sentencias como `if`, `for` o `const`.
⚠️ Si devuelves dos elementos hermanos sin padre (`<h1/><p/>`) da error: envuélvelos en `<>...</>`.
⚠️ Los paréntesis después de `return (` son importantes: sin ellos, un salto de línea hace que JS devuelva `undefined`.
💡 Usa Fragment con nombre `<Fragment key={id}>` cuando necesites poner `key` en una lista (se importa de "react").
🇬🇧 **expression** /iks-PRÉ-shon/ = expresión · **curly braces** /KÉR-li BRÉI-ses/ = llaves `{}` · **fragment** /FRÁG-ment/ = fragmento · **tag** /tag/ = etiqueta · **self-closing** = que se cierra solo

## 🎁 Componentes y props

Un **componente** es una función cuyo nombre empieza con **Mayúscula** y que devuelve JSX. Las **props** son los datos que le pasa el padre, como los parámetros de una función. Analogía: el componente es un molde de salteña 🥟 y las props son el relleno; mismo molde, distintos sabores.

- `function Tarjeta(props) {}` :: Recibe todas las props en un objeto
- `function Tarjeta({ titulo, precio }) {}` :: Desestructurar: forma más usada y legible
- `function Boton({ texto = "OK" }) {}` :: Valor por defecto si no lo pasan
- `<Tarjeta titulo="Té" precio={5} />` :: Texto con comillas; números, booleanos u objetos con `{}`
- `<Modal abierto />` :: Prop booleana sin valor = `true`
- `function Caja({ children }) {}` :: `children` = lo que va entre las etiquetas de apertura y cierre
- `<Boton {...props} />` :: Pasar todas las props de un objeto de golpe
- `export default Tarjeta` / `import Tarjeta from "./Tarjeta"` :: Exportar e importar un componente

```jsx
// components/Tarjeta.jsx
function Tarjeta({ titulo, precio, enOferta = false, children }) {
  return (
    <article className="tarjeta">
      <h3>{titulo}</h3>
      <p>Bs {precio.toFixed(2)}</p>
      {enOferta && <span className="etiqueta">🔥 Oferta</span>}
      <div className="extra">{children}</div>
    </article>
  );
}

export default Tarjeta;

// App.jsx
import Tarjeta from "./components/Tarjeta";

function App() {
  return (
    <main>
      <Tarjeta titulo="Api morada" precio={8} enOferta>
        <p>Con pastel caliente 😋</p>
      </Tarjeta>
      <Tarjeta titulo="Salteña" precio={10} />
    </main>
  );
}
```

📌 Los datos fluyen **de arriba hacia abajo** (padre → hijo). Para que un hijo "hable" con el padre, el padre le pasa una **función** como prop.
⚠️ Las props son de **solo lectura**: nunca hagas `props.titulo = "x"`. Si algo cambia, va en el estado.
⚠️ `<tarjeta />` en minúscula React lo trata como etiqueta HTML y no funciona: los componentes siempre en PascalCase.
💡 Un componente = un archivo, con el mismo nombre (`Tarjeta.jsx`). Si un componente pasa de ~150 líneas, divídelo.
🇬🇧 **props (properties)** /PRÓ-per-tis/ = propiedades · **children** /CHÍL-dren/ = hijos · **default value** /di-FÓLT VÁ-liu/ = valor por defecto · **destructuring** /di-STRÁK-chu-ring/ = desestructurar · **read-only** /rid-ÓUN-li/ = solo lectura

## 🔀 Renderizado condicional y listas

Muchas veces quieres mostrar algo **solo si** se cumple una condición: un spinner mientras carga, un mensaje si la lista está vacía, el botón "Salir" si hay sesión. Como en JSX no cabe `if`, usamos operadores.

- `{cond && <p>Sí</p>}` :: Muestra solo si `cond` es verdadera
- `{cond ? <A /> : <B />}` :: Una cosa u otra (ternario)
- `if (cargando) return <Spinner />;` :: `if` normal ANTES del return principal (retorno temprano)
- `return null;` :: No mostrar nada
- `{lista.length > 0 && <Lista />}` :: Comparar explícitamente con números
- `{usuario?.nombre ?? "Invitado"}` :: Encadenamiento opcional + valor por defecto

```jsx
function Panel({ usuario, mensajes }) {
  // Retorno temprano: el caso especial primero
  if (!usuario) {
    return <p>Inicia sesión para continuar 🔐</p>;
  }

  return (
    <section>
      <h2>Bienvenido, {usuario.nombre}</h2>
      {usuario.esAdmin && <button>⚙️ Panel de admin</button>}
      {mensajes.length > 0
        ? <p>Tienes {mensajes.length} mensajes nuevos 📬</p>
        : <p>No hay mensajes</p>}
    </section>
  );
}
```

⚠️ Trampa clásica: `{mensajes.length && <Lista />}` muestra un **0** en pantalla si la lista está vacía, porque 0 es "falsy" pero React sí lo dibuja. Usa `mensajes.length > 0 &&`.
💡 Si el ternario se vuelve largo o anidado, sácalo a una variable o a un componente aparte; los ternarios dentro de ternarios son ilegibles.
🇬🇧 **conditional rendering** /kon-DÍ-sho-nal RÉN-de-ring/ = renderizado condicional · **early return** /ÉR-li ri-TÉRN/ = retorno temprano · **falsy** /FÓL-si/ = valor que cuenta como falso · **ternary** /TÉR-na-ri/ = ternario

### 📋 Listas y la prop key

Para mostrar una lista, transformas un array de datos en un array de JSX con `.map()`. Cada elemento necesita una **key** única: es como el carnet de identidad de cada elemento, para que React sepa cuál se añadió, borró o movió sin redibujar todo.

- `lista.map(item => <li key={item.id}>{item.nombre}</li>)` :: Patrón básico
- `key={item.id}` :: Usa un ID estable que venga de los datos
- `{ id: crypto.randomUUID(), ...datos }` :: Genera el ID al CREAR el objeto, nunca en el render
- `lista.filter(...).map(...)` :: Filtrar y luego mostrar
- `[...lista].sort((a, b) => a.precio - b.precio).map(...)` :: Ordenar una copia y mostrar

```jsx
const productos = [
  { id: 1, nombre: "Quinua", precio: 25 },
  { id: 2, nombre: "Café de los Yungas", precio: 40 },
  { id: 3, nombre: "Chocolate de Sucre", precio: 15 },
];

function ListaProductos() {
  return (
    <ul>
      {productos.map((p) => (
        <li key={p.id}>
          {p.nombre} — Bs {p.precio}
        </li>
      ))}
    </ul>
  );
}
```

⚠️ No uses el índice (`key={i}`) si la lista se puede reordenar, filtrar o borrar: React confunde los elementos y los inputs muestran datos cruzados.
⚠️ Nunca `key={Math.random()}` en el render: cambia en cada dibujo y React recrea todo (lento y pierde el estado).
📌 La `key` va en el elemento **más externo** que devuelve el `map`, no dentro. Y no llega como prop al hijo.
💡 Ojo con `map((p) => { <li/> })` con llaves: sin `return` devuelve `undefined`. Usa paréntesis `map((p) => ( <li/> ))`.
🇬🇧 **key** /ki/ = llave/clave · **unique** /iu-NÍK/ = único · **array** /a-RÉI/ = arreglo · **to map** /map/ = transformar cada elemento · **index** /ÍN-deks/ = índice

## 🖱️ Eventos

Los eventos (clic, escribir, enviar formulario) se manejan pasando una **función** al atributo `onAlgo`. Pasas la función, no la ejecutas: es como darle a alguien tu número de teléfono para que te llame después, no llamarle ahora.

- `onClick={manejarClic}` :: Correcto: pasas la función
- `onClick={() => borrar(id)}` :: Con argumentos: envuelve en arrow function
- `onChange={(e) => setTexto(e.target.value)}` :: Leer lo que se escribe en un input
- `onSubmit={(e) => { e.preventDefault(); ... }}` :: Enviar formulario sin recargar la página
- `e.stopPropagation()` :: Evita que el evento suba a los padres
- `onKeyDown={(e) => e.key === "Enter" && enviar()}` :: Detectar tecla
- `onMouseEnter`, `onFocus`, `onBlur` :: Otros eventos comunes

```jsx
function Botones() {
  function saludar() {
    alert("¡Hola! 👋");
  }

  function borrar(id) {
    console.log("Borrando", id);
  }

  return (
    <div>
      <button onClick={saludar}>Saludar</button>
      <button onClick={() => borrar(42)}>Borrar 42</button>
      <input onKeyDown={(e) => e.key === "Enter" && console.log(e.target.value)} />
    </div>
  );
}
```

⚠️ Error número uno: `onClick={borrar(42)}` **ejecuta** la función al dibujar (y si cambia estado, bucle infinito). Debe ser `onClick={() => borrar(42)}`.
💡 Convención de nombres: la función se llama `handleClick` / `manejarClic` y la prop que la recibe `onClick` / `onBorrar`.
🇬🇧 **event** /i-VÉNT/ = evento · **handler** /JÁND-ler/ = manejador · **click** /klik/ = clic · **to submit** /sab-MÍT/ = enviar · **prevent default** /pri-VÉNT di-FÓLT/ = evitar el comportamiento por defecto

## 🧠 useState a fondo

`useState` le da **memoria** a un componente. Las variables normales se "olvidan" en cada render; el estado se conserva y, cuando lo cambias con su función `set`, React **vuelve a dibujar** el componente con el valor nuevo.

- `const [valor, setValor] = useState(inicial);` :: Declarar estado (desestructuración de array)
- `setValor(5)` :: Reemplazar por un valor nuevo
- `setContador(c => c + 1)` :: Función actualizadora: usa el valor MÁS reciente
- `useState(() => calcularCaro())` :: Inicialización perezosa: solo se calcula la primera vez
- `setUsuario({ ...usuario, edad: 23 })` :: Objeto: copia y cambia (inmutable)
- `setLista([...lista, nuevo])` :: Array: añadir al final
- `setLista(lista.filter(x => x.id !== id))` :: Array: borrar
- `setLista(lista.map(x => x.id === id ? { ...x, hecho: true } : x))` :: Array: editar uno

### 🔒 Inmutabilidad: por qué no mutar

React decide si redibujar comparando **referencias**: ¿es el mismo objeto que antes? Si haces `lista.push(x)`, el array es el mismo (misma dirección de memoria), así que React cree que nada cambió y **no actualiza la pantalla**. Por eso siempre creas una **copia nueva**.

| ❌ Mutar (mal) | ✅ Inmutable (bien) |
|---|---|
| `lista.push(x)` | `[...lista, x]` |
| `lista.splice(i, 1)` | `lista.filter((_, j) => j !== i)` |
| `lista[i] = x` | `lista.map((v, j) => j === i ? x : v)` |
| `lista.sort()` | `[...lista].sort()` o `lista.toSorted()` |
| `obj.nombre = "Ana"` | `{ ...obj, nombre: "Ana" }` |
| `obj.dir.ciudad = "Cbba"` | `{ ...obj, dir: { ...obj.dir, ciudad: "Cbba" } }` |

### 🔁 La función actualizadora

`setX` no cambia la variable **inmediatamente**: programa un nuevo render. Dentro del mismo clic, `contador` sigue valiendo lo mismo. Si actualizas varias veces seguidas o dependes del valor anterior, usa la forma `c => c + 1`.

```jsx
// ❌ Suma solo 1: las tres líneas leen el mismo "contador" viejo
setContador(contador + 1);
setContador(contador + 1);
setContador(contador + 1);

// ✅ Suma 3: cada función recibe el valor actualizado por la anterior
setContador((c) => c + 1);
setContador((c) => c + 1);
setContador((c) => c + 1);
```

### ✅ Ejemplo resuelto: contador

```jsx
import { useState } from "react";

function Contador({ inicio = 0, paso = 1 }) {
  const [cuenta, setCuenta] = useState(inicio);

  const sumar = () => setCuenta((c) => c + paso);
  const restar = () => setCuenta((c) => Math.max(0, c - paso));
  const reiniciar = () => setCuenta(inicio);

  return (
    <div className="contador">
      <h2>Cuenta: {cuenta}</h2>
      <button onClick={restar} disabled={cuenta === 0}>➖</button>
      <button onClick={sumar}>➕</button>
      <button onClick={reiniciar}>🔄 Reiniciar</button>
      {cuenta >= 10 && <p>🎉 ¡Llegaste a 10!</p>}
    </div>
  );
}

export default Contador;
```

📌 Parte por parte: `useState(inicio)` crea el estado empezando en la prop `inicio`. `sumar` usa la función actualizadora para no depender de un valor viejo. `restar` usa `Math.max(0, ...)` para no bajar de cero. `disabled={cuenta === 0}` desactiva el botón cuando no tiene sentido. El mensaje 🎉 es renderizado condicional.

### ✅ Ejemplo resuelto: lista de tareas (CRUD)

```jsx
import { useState } from "react";

function ListaTareas() {
  const [tareas, setTareas] = useState([
    { id: 1, texto: "Estudiar React", hecha: false },
  ]);
  const [texto, setTexto] = useState("");
  const [editandoId, setEditandoId] = useState(null);

  // C — Crear
  function agregar(e) {
    e.preventDefault();
    const limpio = texto.trim();
    if (!limpio) return;
    if (editandoId) {
      // U — Actualizar texto
      setTareas((ts) => ts.map((t) => (t.id === editandoId ? { ...t, texto: limpio } : t)));
      setEditandoId(null);
    } else {
      setTareas((ts) => [...ts, { id: crypto.randomUUID(), texto: limpio, hecha: false }]);
    }
    setTexto("");
  }

  // U — Marcar como hecha
  function alternar(id) {
    setTareas((ts) => ts.map((t) => (t.id === id ? { ...t, hecha: !t.hecha } : t)));
  }

  // D — Borrar
  function borrar(id) {
    setTareas((ts) => ts.filter((t) => t.id !== id));
  }

  function editar(tarea) {
    setTexto(tarea.texto);
    setEditandoId(tarea.id);
  }

  const pendientes = tareas.filter((t) => !t.hecha).length; // dato derivado

  return (
    <div>
      <h2>📝 Tareas ({pendientes} pendientes)</h2>
      <form onSubmit={agregar}>
        <input value={texto} onChange={(e) => setTexto(e.target.value)} placeholder="Nueva tarea..." />
        <button type="submit">{editandoId ? "💾 Guardar" : "➕ Agregar"}</button>
      </form>

      {tareas.length === 0 && <p>¡Nada pendiente! 🏖️</p>}

      <ul>
        {tareas.map((t) => (
          <li key={t.id}>
            <input type="checkbox" checked={t.hecha} onChange={() => alternar(t.id)} />
            <span style={{ textDecoration: t.hecha ? "line-through" : "none" }}>{t.texto}</span>
            <button onClick={() => editar(t)}>✏️</button>
            <button onClick={() => borrar(t.id)}>🗑️</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ListaTareas;
```

📌 Claves del ejemplo: **C**rear con `[...ts, nueva]`, **R**ead (leer/mostrar) con `map`, **U**pdate con `map` + spread, **D**elete con `filter`. `pendientes` NO es estado: se **calcula** a partir de `tareas` en cada render (dato derivado). `editandoId` decide si el formulario crea o edita.
⚠️ No guardes en estado lo que puedes calcular (`pendientes`, `total`, `listaFiltrada`): tendrías dos fuentes de verdad que se desincronizan.
💡 Los hooks solo se llaman en el nivel superior del componente: nunca dentro de `if`, `for` o funciones internas.
🇬🇧 **state** /steit/ = estado · **setter** /SÉ-ter/ = función que asigna · **immutable** /i-MIÚ-ta-bol/ = inmutable · **updater function** /ap-DÉI-ter/ = función actualizadora · **derived state** /di-RÁIVD/ = estado derivado · **to mutate** /MIÚ-teit/ = modificar en el sitio

## 📝 Formularios controlados

Un input **controlado** es aquel cuyo valor vive en el estado de React: el input muestra `value={estado}` y cada tecla actualiza el estado con `onChange`. React es "la única fuente de verdad". Así puedes validar, limpiar o transformar lo que se escribe en tiempo real.

- `<input value={nombre} onChange={(e) => setNombre(e.target.value)} />` :: Input de texto controlado
- `<input type="checkbox" checked={acepto} onChange={(e) => setAcepto(e.target.checked)} />` :: Checkbox usa `checked`
- `<select value={pais} onChange={(e) => setPais(e.target.value)}>` :: Select controlado
- `<textarea value={msg} onChange={...} />` :: Textarea también usa `value`
- `const [form, setForm] = useState({ email: "", clave: "" })` :: Un solo estado para todo el formulario
- `setForm({ ...form, [e.target.name]: e.target.value })` :: Manejador genérico usando el atributo `name`
- `<input type="number" />` → `Number(e.target.value)` :: `value` siempre llega como texto

### ✅ Ejemplo resuelto: login con validación

```jsx
import { useState } from "react";

function validar({ email, clave }) {
  const errores = {};
  if (!email) errores.email = "El correo es obligatorio";
  else if (!/^\S+@\S+\.\S+$/.test(email)) errores.email = "Correo no válido";
  if (clave.length < 8) errores.clave = "Mínimo 8 caracteres";
  return errores;
}

function Login({ onLogin }) {
  const [form, setForm] = useState({ email: "", clave: "", recordar: false });
  const [errores, setErrores] = useState({});
  const [enviando, setEnviando] = useState(false);

  function cambiar(e) {
    const { name, value, type, checked } = e.target;
    setForm((f) => ({ ...f, [name]: type === "checkbox" ? checked : value }));
  }

  async function enviar(e) {
    e.preventDefault();
    const nuevos = validar(form);
    setErrores(nuevos);
    if (Object.keys(nuevos).length > 0) return; // hay errores: no enviar

    setEnviando(true);
    try {
      await onLogin(form); // por ejemplo, un fetch al backend
    } catch {
      setErrores({ general: "Credenciales incorrectas ❌" });
    } finally {
      setEnviando(false);
    }
  }

  return (
    <form onSubmit={enviar} noValidate>
      <label htmlFor="email">Correo</label>
      <input id="email" name="email" type="email" value={form.email} onChange={cambiar} />
      {errores.email && <small className="error">{errores.email}</small>}

      <label htmlFor="clave">Contraseña</label>
      <input id="clave" name="clave" type="password" value={form.clave} onChange={cambiar} />
      {errores.clave && <small className="error">{errores.clave}</small>}

      <label>
        <input name="recordar" type="checkbox" checked={form.recordar} onChange={cambiar} />
        Recordarme
      </label>

      {errores.general && <p className="error">{errores.general}</p>}
      <button type="submit" disabled={enviando}>
        {enviando ? "Entrando..." : "Iniciar sesión"}
      </button>
    </form>
  );
}

export default Login;
```

📌 Parte por parte: `validar` es una función pura fuera del componente (fácil de probar). `cambiar` es UN manejador para todos los inputs gracias a `name` y `[name]` (propiedad computada). `enviar` evita recargar con `preventDefault`, valida, y usa `enviando` para desactivar el botón y evitar doble envío. `finally` se ejecuta tanto si sale bien como si falla.
⚠️ Si pones `value={x}` sin `onChange`, el input queda "congelado" y React avisa en consola. Para solo valor inicial usa `defaultValue`.
⚠️ Pasar de `value={undefined}` a un texto da el aviso "uncontrolled to controlled": inicia siempre con `""`, no con `undefined`.
💡 Para formularios grandes usa **React Hook Form** + **Zod** (validación con esquemas). En React 19 también existen las *Actions* con `<form action={fn}>` y `useActionState`.
🇬🇧 **controlled input** /kon-TRÓULD ÍN-put/ = input controlado · **form** /form/ = formulario · **validation** /va-li-DÉI-shon/ = validación · **password** /PÁS-werd/ = contraseña · **required** /ri-KUÁI-erd/ = obligatorio · **to sign in / log in** = iniciar sesión

### 🔍 Ejemplo integrador: buscador con filtro

Este ejemplo junta estado, inputs controlados, listas, datos derivados y renderizado condicional. Es un patrón que usarás muchísimo.

### ✅ Ejemplo resuelto: buscador de lenguajes

```jsx
import { useState } from "react";

const LENGUAJES = [
  { id: 1, nombre: "Python", tipo: "backend", estrellas: 5 },
  { id: 2, nombre: "JavaScript", tipo: "frontend", estrellas: 5 },
  { id: 3, nombre: "TypeScript", tipo: "frontend", estrellas: 4 },
  { id: 4, nombre: "Go", tipo: "backend", estrellas: 4 },
  { id: 5, nombre: "Rust", tipo: "sistemas", estrellas: 4 },
  { id: 6, nombre: "C", tipo: "sistemas", estrellas: 3 },
];

function quitarTildes(s) {
  return s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();
}

function Buscador() {
  const [busqueda, setBusqueda] = useState("");
  const [tipo, setTipo] = useState("todos");
  const [orden, setOrden] = useState("nombre");

  // Datos derivados: se calculan en cada render, NO van en estado
  const q = quitarTildes(busqueda.trim());
  const resultados = LENGUAJES
    .filter((l) => quitarTildes(l.nombre).includes(q))
    .filter((l) => tipo === "todos" || l.tipo === tipo)
    .toSorted((a, b) =>
      orden === "nombre" ? a.nombre.localeCompare(b.nombre) : b.estrellas - a.estrellas
    );

  return (
    <div>
      <input
        type="search"
        placeholder="🔍 Buscar lenguaje..."
        value={busqueda}
        onChange={(e) => setBusqueda(e.target.value)}
      />
      <select value={tipo} onChange={(e) => setTipo(e.target.value)}>
        <option value="todos">Todos</option>
        <option value="frontend">Frontend</option>
        <option value="backend">Backend</option>
        <option value="sistemas">Sistemas</option>
      </select>
      <button onClick={() => setOrden((o) => (o === "nombre" ? "estrellas" : "nombre"))}>
        Ordenar por: {orden}
      </button>

      <p>{resultados.length} resultado(s)</p>

      {resultados.length === 0 ? (
        <p>😕 No hay coincidencias para "{busqueda}"</p>
      ) : (
        <ul>
          {resultados.map((l) => (
            <li key={l.id}>
              {l.nombre} <small>({l.tipo})</small> {"⭐".repeat(l.estrellas)}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default Buscador;
```

📌 Parte por parte: solo hay 3 estados (lo que el usuario elige). `resultados` se **deriva** encadenando `filter` → `filter` → `toSorted` (que no muta el original). `quitarTildes` permite buscar sin importar mayúsculas ni tildes (escribir "rust" o "RÚST" encuentra "Rust"). El ternario final cubre el caso "sin resultados".
💡 Si la lista viene de una API y cada tecla hace una petición, añade un **debounce** (esperar ~300 ms a que el usuario deje de escribir) o `useDeferredValue`.
🇬🇧 **search** /serch/ = buscar · **filter** /FÍL-ter/ = filtro · **to sort** /sort/ = ordenar · **match** /mach/ = coincidencia · **debounce** /di-BÁUNS/ = esperar a que paren los eventos

## ⚡ useEffect y fetch de datos

Un componente debería solo **calcular qué mostrar**. Todo lo que "sale" al mundo exterior es un **efecto**: pedir datos a una API, poner un temporizador, suscribirse a eventos de la ventana, cambiar el título de la pestaña. `useEffect` ejecuta ese código **después** de que React pinta la pantalla.

- `useEffect(() => { ... })` :: Sin array: se ejecuta después de CADA render (casi nunca lo quieres)
- `useEffect(() => { ... }, [])` :: Array vacío: solo al montar (aparecer) el componente
- `useEffect(() => { ... }, [id])` :: Al montar y cada vez que `id` cambia
- `return () => { ... }` :: Función de limpieza: se ejecuta antes del siguiente efecto y al desmontar
- `document.title = ...` :: Ejemplo típico de efecto sencillo

### 🔄 Ciclo de vida en una línea

**Montar** (aparece) → efecto corre. **Actualizar** (cambia una dependencia) → limpieza vieja, efecto nuevo. **Desmontar** (desaparece) → limpieza final. La limpieza es como apagar la luz al salir de un cuarto 💡.

```jsx
import { useEffect, useState } from "react";

function Reloj() {
  const [hora, setHora] = useState(new Date());

  useEffect(() => {
    const id = setInterval(() => setHora(new Date()), 1000);
    return () => clearInterval(id); // 🧹 limpieza: sin esto quedan intervalos fantasma
  }, []);

  return <p>🕐 {hora.toLocaleTimeString("es-BO")}</p>;
}

function AnchoVentana() {
  const [ancho, setAncho] = useState(window.innerWidth);

  useEffect(() => {
    const alCambiar = () => setAncho(window.innerWidth);
    window.addEventListener("resize", alCambiar);
    return () => window.removeEventListener("resize", alCambiar);
  }, []);

  return <p>Ancho: {ancho}px</p>;
}
```

### 🌀 Bucles infinitos y errores comunes

```jsx
// ❌ Bucle infinito: el efecto cambia estado → nuevo render → efecto otra vez...
useEffect(() => {
  setContador(contador + 1);
});

// ❌ Bucle infinito: un objeto/array creado en el render es "nuevo" cada vez
const filtros = { categoria: "libros" };
useEffect(() => { buscar(filtros); }, [filtros]);

// ✅ Depende de valores primitivos, o crea el objeto dentro del efecto
useEffect(() => { buscar({ categoria }); }, [categoria]);

// ❌ Efecto innecesario: calcular datos derivados
useEffect(() => { setTotal(precio * cantidad); }, [precio, cantidad]);
// ✅ Simplemente calcula en el render
const total = precio * cantidad;
```

⚠️ Pon en el array **todas** las variables de fuera que usas dentro del efecto. El plugin `eslint-plugin-react-hooks` te avisa; hazle caso.
⚠️ La función del efecto NO puede ser `async` directamente (`useEffect(async () => ...)` está mal). Define una función async dentro y llámala.
💡 Regla de oro: "¿esto sincroniza con algo externo (API, DOM, timer)?" Si no, probablemente **no necesitas** useEffect.
🇬🇧 **side effect** /sáid i-FÉKT/ = efecto secundario · **dependency array** /di-PÉN-den-si a-RÉI/ = arreglo de dependencias · **cleanup** /KLÍN-ap/ = limpieza · **to mount** /maunt/ = montar · **infinite loop** /ÍN-fi-nit lup/ = bucle infinito

### 🌐 Fetch de datos con loading y error

Pedir datos a una API tiene tres estados posibles: **cargando** ⏳, **error** ❌ y **éxito** ✅. Un buen componente muestra algo distinto en cada caso. Además, si el usuario cambia rápido de página, hay que **cancelar** la petición vieja para que no pise a la nueva (*race condition*).

- `const r = await fetch(url)` :: Hacer la petición
- `if (!r.ok) throw new Error(...)` :: fetch NO lanza error con 404/500: hay que revisarlo a mano
- `const datos = await r.json()` :: Convertir la respuesta a objeto JS
- `const ctrl = new AbortController()` :: Permite cancelar la petición
- `fetch(url, { signal: ctrl.signal })` :: Conectar la petición con el controlador
- `return () => ctrl.abort()` :: Cancelar al desmontar o al cambiar la URL

### ✅ Ejemplo resuelto: usuarios desde una API (loading/error)

```jsx
import { useEffect, useState } from "react";

function Usuarios() {
  const [usuarios, setUsuarios] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const ctrl = new AbortController();

    async function cargar() {
      try {
        setCargando(true);
        setError(null);
        const r = await fetch("https://jsonplaceholder.typicode.com/users", {
          signal: ctrl.signal,
        });
        if (!r.ok) throw new Error(`Error HTTP ${r.status}`);
        const datos = await r.json();
        setUsuarios(datos);
      } catch (err) {
        if (err.name !== "AbortError") setError(err.message);
      } finally {
        if (!ctrl.signal.aborted) setCargando(false);
      }
    }

    cargar();
    return () => ctrl.abort();
  }, []);

  if (cargando) return <p>⏳ Cargando usuarios...</p>;
  if (error) return <p>❌ Algo salió mal: {error}</p>;

  return (
    <ul>
      {usuarios.map((u) => (
        <li key={u.id}>
          <strong>{u.name}</strong> — {u.email}
        </li>
      ))}
    </ul>
  );
}

export default Usuarios;
```

📌 Parte por parte: tres estados (`usuarios`, `cargando`, `error`). La función `cargar` es async **dentro** del efecto. `r.ok` detecta 404/500. Ignoramos `AbortError` porque es una cancelación nuestra, no un fallo. Los `if` con retorno temprano muestran cada estado de forma limpia.
💡 En proyectos reales usa **TanStack Query** (`useQuery`): caché, reintentos, recarga en segundo plano y loading/error ya resueltos.
⚠️ Nunca pongas claves secretas de API en el frontend: todo lo que está en el navegador es visible. Variables `VITE_...` en `.env` también son públicas.
🇬🇧 **fetch** /fech/ = traer/ir a buscar · **loading** /LÓU-ding/ = cargando · **request** /ri-KUÉST/ = petición · **response** /ris-PÓNS/ = respuesta · **race condition** /reis kon-DÍ-shon/ = condición de carrera · **to abort** /a-BÓRT/ = cancelar

## 📌 useRef: referencias que no redibujan

`useRef` te da una "cajita" `{ current: valor }` que **persiste entre renders** pero que, al cambiarla, **no provoca** un nuevo render. Sirve para dos cosas: tocar elementos del DOM directamente (enfocar un input, medir un div, controlar un video) y guardar valores que no se ven en pantalla (ID de un intervalo, valor anterior).

- `const inputRef = useRef(null)` :: Crear la referencia
- `<input ref={inputRef} />` :: Conectarla a un elemento
- `inputRef.current.focus()` :: Usar el elemento DOM real
- `const idRef = useRef(null); idRef.current = setInterval(...)` :: Guardar un valor sin redibujar
- `videoRef.current.play()` :: Controlar un `<video>`
- `function Input({ ref }) {}` :: React 19: `ref` se pasa como prop normal (antes `forwardRef`)

```jsx
import { useEffect, useRef, useState } from "react";

function Buscador() {
  const inputRef = useRef(null);
  const clicsRef = useRef(0); // contador que no necesita mostrarse
  const [texto, setTexto] = useState("");

  useEffect(() => {
    inputRef.current.focus(); // enfocar al aparecer
  }, []);

  function limpiar() {
    clicsRef.current += 1;
    console.log("Limpiado", clicsRef.current, "veces");
    setTexto("");
    inputRef.current.focus();
  }

  return (
    <div>
      <input ref={inputRef} value={texto} onChange={(e) => setTexto(e.target.value)} />
      <button onClick={limpiar}>🧹 Limpiar</button>
    </div>
  );
}
```

| | useState | useRef |
|---|---|---|
| ¿Redibuja al cambiar? | ✅ Sí | ❌ No |
| ¿Persiste entre renders? | ✅ Sí | ✅ Sí |
| Se lee como | `valor` | `ref.current` |
| Úsalo para | Lo que se ve en pantalla | DOM, timers, valores internos |

⚠️ No leas ni escribas `ref.current` durante el render (en el cuerpo del componente): hazlo en eventos o efectos. En el primer render `current` aún es `null`.
💡 Si cambias algo y la pantalla debe reflejarlo, es estado; si no, puede ser ref.
🇬🇧 **reference** /RÉ-fe-rens/ = referencia · **current** /KÁ-rent/ = actual · **to focus** /FÓU-kas/ = enfocar · **to persist** /per-SÍST/ = persistir, conservarse

## 🏎️ useMemo y useCallback: cuándo SÍ y cuándo NO

Cada render vuelve a ejecutar todo el cuerpo del componente: recalcula variables y crea funciones nuevas. Casi siempre eso es rapidísimo y no importa. `useMemo` **memoriza un valor calculado** y `useCallback` **memoriza una función**, para reutilizarlos mientras sus dependencias no cambien. Analogía: apuntar el resultado de una cuenta larga en un papel para no rehacerla.

- `const v = useMemo(() => calcular(a, b), [a, b])` :: Recalcula solo si cambian `a` o `b`
- `const fn = useCallback((x) => hacer(x, id), [id])` :: Misma función mientras `id` no cambie
- `const Hijo = memo(function Hijo(props) {...})` :: El hijo no se redibuja si sus props no cambian
- `useCallback(fn, deps)` = `useMemo(() => fn, deps)` :: Son equivalentes

```jsx
import { memo, useCallback, useMemo, useState } from "react";

const FilaProducto = memo(function FilaProducto({ producto, onAgregar }) {
  console.log("Render fila", producto.id);
  return (
    <li>
      {producto.nombre} <button onClick={() => onAgregar(producto.id)}>🛒</button>
    </li>
  );
});

function Catalogo({ productos }) {
  const [busqueda, setBusqueda] = useState("");
  const [carrito, setCarrito] = useState([]);

  // ✅ SÍ: filtrar/ordenar miles de elementos es caro
  const visibles = useMemo(
    () => productos.filter((p) => p.nombre.toLowerCase().includes(busqueda.toLowerCase())),
    [productos, busqueda]
  );

  // ✅ SÍ: la función se pasa a un hijo envuelto en memo
  const agregar = useCallback((id) => setCarrito((c) => [...c, id]), []);

  return (
    <>
      <input value={busqueda} onChange={(e) => setBusqueda(e.target.value)} />
      <p>🛒 {carrito.length}</p>
      <ul>
        {visibles.map((p) => <FilaProducto key={p.id} producto={p} onAgregar={agregar} />)}
      </ul>
    </>
  );
}
```

| ✅ Úsalo cuando | ❌ No lo uses cuando |
|---|---|
| El cálculo es pesado (miles de elementos, ordenar, estadísticas) | Es una suma o un string simple |
| Pasas la función/objeto a un hijo con `memo` | El hijo no usa `memo` (no sirve de nada) |
| El valor es dependencia de un `useEffect` | "Por si acaso" en todo el código |
| Lo mediste con React DevTools Profiler y era lento | No has medido nada |

📌 **React Compiler** (estable con React 19) memoriza automáticamente: en proyectos con el compilador activado casi no necesitas escribir `useMemo`/`useCallback` a mano.
⚠️ Memorizar también cuesta (memoria + comparar dependencias). Optimizar sin medir solo complica el código.
💡 Antes de memorizar, prueba a **mover el estado más abajo** (al componente que lo usa) o pasar contenido como `children`: suele resolver el problema sin hooks extra.
🇬🇧 **memoization** /me-mo-ai-ZÉI-shon/ = memorización (guardar resultados) · **expensive** /iks-PÉN-siv/ = costoso · **callback** /KÓL-bak/ = función que se pasa para llamarla luego · **premature optimization** = optimización prematura · **to measure** /MÉ-yer/ = medir

## 🌍 Context API: datos para todo el árbol

Cuando muchos componentes en distintos niveles necesitan el mismo dato (usuario logueado, tema, idioma), pasarlo prop por prop por 5 niveles es tedioso: se llama **prop drilling** (taladrar props). **Context** es como un altavoz: el `Provider` "transmite" un valor y cualquier componente dentro puede "escucharlo" con `useContext`, sin intermediarios.

- `const TemaContext = createContext(null)` :: 1. Crear el contexto
- `<TemaContext value={valor}>...</TemaContext>` :: 2. Proveer el valor (React 19; antes `<TemaContext.Provider value>`)
- `const tema = useContext(TemaContext)` :: 3. Consumir en cualquier hijo
- `use(TemaContext)` :: React 19: alternativa a useContext que se puede usar dentro de `if`
- `export function useTema() {...}` :: Buena práctica: un hook propio para consumir el contexto

### ✅ Ejemplo resuelto: tema claro/oscuro

```jsx
// context/TemaContext.jsx
import { createContext, useContext, useEffect, useState } from "react";

const TemaContext = createContext(null);

export function TemaProvider({ children }) {
  const [tema, setTema] = useState(() => localStorage.getItem("tema") ?? "claro");

  useEffect(() => {
    document.documentElement.dataset.tema = tema; // <html data-tema="oscuro">
    localStorage.setItem("tema", tema);
  }, [tema]);

  const alternar = () => setTema((t) => (t === "claro" ? "oscuro" : "claro"));

  return <TemaContext value={{ tema, alternar }}>{children}</TemaContext>;
}

export function useTema() {
  const ctx = useContext(TemaContext);
  if (!ctx) throw new Error("useTema debe usarse dentro de <TemaProvider>");
  return ctx;
}

// components/BotonTema.jsx
import { useTema } from "../context/TemaContext";

function BotonTema() {
  const { tema, alternar } = useTema();
  return <button onClick={alternar}>{tema === "claro" ? "🌙 Oscuro" : "☀️ Claro"}</button>;
}

// App.jsx
import { TemaProvider } from "./context/TemaContext";
import BotonTema from "./components/BotonTema";

function App() {
  return (
    <TemaProvider>
      <header><BotonTema /></header>
      <main>Contenido...</main>
    </TemaProvider>
  );
}
```

```css
/* index.css: los colores cambian según data-tema */
:root { --fondo: #ffffff; --texto: #1a1a1a; }
:root[data-tema="oscuro"] { --fondo: #121212; --texto: #f0f0f0; }
body { background: var(--fondo); color: var(--texto); }
```

📌 Parte por parte: `TemaProvider` guarda el estado y lo comparte. La inicialización perezosa lee `localStorage` solo una vez. El efecto sincroniza con el exterior (atributo en `<html>` y almacenamiento). `useTema` esconde `useContext` y lanza un error claro si alguien lo usa fuera del Provider. El CSS cambia con variables.
⚠️ Cada vez que cambia el `value`, **todos** los consumidores se redibujan. No metas en un solo contexto cosas que cambian muy seguido (como la posición del mouse).
💡 Context es ideal para datos que cambian **poco** (tema, usuario, idioma). Para estado que cambia mucho y se comparte en muchos sitios, mira Zustand.
🇬🇧 **context** /KÓN-tekst/ = contexto · **provider** /pro-VÁI-der/ = proveedor · **consumer** /kon-SIÚ-mer/ = consumidor · **prop drilling** /prop DRÍ-ling/ = pasar props por muchos niveles · **dark mode** /dark moud/ = modo oscuro · **theme** /zim/ = tema

## 🪝 Hooks personalizados

Un **hook personalizado** es una función que empieza con `use` y usa otros hooks dentro. Sirve para **reutilizar lógica** (no interfaz) entre componentes. Si copias y pegas el mismo `useState + useEffect` en tres sitios, es hora de crear un hook.

- `function useAlgo() { ... return valor; }` :: Debe empezar con `use`
- `return [valor, setValor]` :: Devolver como array (estilo useState) para renombrar fácil
- `return { datos, cargando, error }` :: Devolver como objeto cuando son muchos valores
- `hooks/useFetch.js` :: Guárdalos en la carpeta `hooks/`

### ✅ Ejemplo resuelto: useFetch

```jsx
// hooks/useFetch.js
import { useEffect, useState } from "react";

export function useFetch(url) {
  const [estado, setEstado] = useState({ datos: null, cargando: true, error: null });

  useEffect(() => {
    if (!url) return;
    const ctrl = new AbortController();
    setEstado({ datos: null, cargando: true, error: null });

    fetch(url, { signal: ctrl.signal })
      .then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then((datos) => setEstado({ datos, cargando: false, error: null }))
      .catch((err) => {
        if (err.name !== "AbortError") setEstado({ datos: null, cargando: false, error: err.message });
      });

    return () => ctrl.abort();
  }, [url]);

  return estado;
}

// Uso en cualquier componente:
function Post({ id }) {
  const { datos, cargando, error } = useFetch(`https://jsonplaceholder.typicode.com/posts/${id}`);
  if (cargando) return <p>⏳</p>;
  if (error) return <p>❌ {error}</p>;
  return <h2>{datos.title}</h2>;
}
```

### ✅ Ejemplo resuelto: useLocalStorage

```jsx
// hooks/useLocalStorage.js
import { useEffect, useState } from "react";

export function useLocalStorage(clave, valorInicial) {
  const [valor, setValor] = useState(() => {
    try {
      const guardado = localStorage.getItem(clave);
      return guardado !== null ? JSON.parse(guardado) : valorInicial;
    } catch {
      return valorInicial; // JSON roto o storage bloqueado
    }
  });

  useEffect(() => {
    try {
      localStorage.setItem(clave, JSON.stringify(valor));
    } catch {
      /* modo incógnito o cuota llena: ignorar */
    }
  }, [clave, valor]);

  return [valor, setValor];
}

// Uso: igual que useState, ¡pero sobrevive al recargar la página!
function Notas() {
  const [nota, setNota] = useLocalStorage("nota", "");
  return <textarea value={nota} onChange={(e) => setNota(e.target.value)} />;
}
```

📌 Cada componente que usa un hook tiene **su propio estado**: dos componentes con `useFetch` no comparten datos. Los hooks comparten **lógica**, no estado.
⚠️ Si tu función no usa ningún hook dentro, no la llames `useAlgo`: es una función normal (`formatearFecha`).
💡 Ideas de hooks para practicar: `useDebounce`, `useToggle`, `useOnlineStatus`, `useWindowSize`, `useClickOutside`.
🇬🇧 **custom hook** /KÁS-tom juk/ = hook personalizado · **reusable** /ri-IÚ-sa-bol/ = reutilizable · **logic** /LÓ-yik/ = lógica · **storage** /STÓ-rich/ = almacenamiento · **to share** /sher/ = compartir

## 🧭 React Router: varias páginas

Una app React es una **SPA** (Single Page Application): hay un solo `index.html` y JavaScript cambia lo que se ve según la URL, sin recargar. **React Router** conecta URLs con componentes, como un índice de libro: `/perfil` → componente `Perfil`.

- `npm install react-router` :: Instalar (v7; en v6 era `react-router-dom`)
- `<BrowserRouter>` :: Envuelve la app y escucha la URL
- `<Routes><Route path="/" element={<Inicio />} /></Routes>` :: Definir rutas
- `<Route path="/producto/:id" element={<Producto />} />` :: Ruta con parámetro dinámico
- `<Route path="*" element={<NoEncontrado />} />` :: Página 404 para cualquier otra ruta
- `<Link to="/perfil">Perfil</Link>` :: Enlace SIN recargar la página (no uses `<a href>`)
- `<NavLink to="/" className={({ isActive }) => isActive ? "activo" : ""}>` :: Enlace que sabe si está activo
- `const { id } = useParams()` :: Leer el `:id` de la URL
- `const navigate = useNavigate(); navigate("/login")` :: Navegar desde código (tras guardar, login...)
- `navigate(-1)` :: Volver atrás
- `const [params, setParams] = useSearchParams()` :: Leer `?busqueda=algo` de la URL
- `<Outlet />` :: Lugar donde se pintan las rutas hijas dentro de un layout

```jsx
// main.jsx
import { BrowserRouter } from "react-router";
createRoot(document.getElementById("root")).render(
  <BrowserRouter><App /></BrowserRouter>
);

// App.jsx
import { Routes, Route, Link, Outlet, useParams, useNavigate } from "react-router";

function Layout() {
  return (
    <>
      <nav>
        <Link to="/">🏠 Inicio</Link> | <Link to="/productos/7">📦 Producto 7</Link>
      </nav>
      <Outlet /> {/* aquí aparece la página actual */}
    </>
  );
}

function Producto() {
  const { id } = useParams(); // "7" (siempre string)
  const navigate = useNavigate();
  return (
    <div>
      <h2>Producto #{id}</h2>
      <button onClick={() => navigate(-1)}>⬅️ Volver</button>
    </div>
  );
}

function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<h1>Bienvenido</h1>} />
        <Route path="productos/:id" element={<Producto />} />
        <Route path="*" element={<h1>404 😢</h1>} />
      </Route>
    </Routes>
  );
}
```

⚠️ Los parámetros de `useParams` siempre son **texto**: convierte con `Number(id)` antes de comparar con IDs numéricos.
⚠️ Al desplegar una SPA, recargar en `/perfil` puede dar 404 en el servidor: hay que redirigir todo a `index.html` (ver sección despliegue).
💡 Para rutas protegidas crea un componente `<RutaPrivada>` que haga `return usuario ? <Outlet /> : <Navigate to="/login" />`.
🇬🇧 **route** /rut/ o /raut/ = ruta · **router** /RÚ-ter/ = enrutador · **link** /link/ = enlace · **to navigate** /NÁ-vi-geit/ = navegar · **SPA (single page application)** = aplicación de una sola página · **not found** = no encontrado

## 🎨 Estilos: CSS, CSS Modules y Tailwind

Hay varias formas de dar estilo en React. Lo importante es evitar que los estilos de un componente "contaminen" a otros.

- `import "./App.css"` :: CSS global: afecta a toda la app (bueno para reset y variables)
- `Boton.module.css` + `import s from "./Boton.module.css"` :: CSS Modules: clases con alcance local
- `<button className={s.primario}>` :: Usar una clase del módulo
- `className={`${s.boton} ${activo ? s.activo : ""}`}` :: Combinar clases condicionalmente
- `npm install clsx` → `clsx(s.boton, activo && s.activo)` :: Combinar clases de forma limpia
- `style={{ width: `${pct}%` }}` :: Estilo en línea solo para valores dinámicos

```css
/* Boton.module.css */
.boton { padding: 0.6rem 1.2rem; border-radius: 8px; border: none; }
.primario { background: #2563eb; color: white; }
.peligro { background: #dc2626; color: white; }
```

```jsx
// Boton.jsx — CSS Modules renombra las clases (ej. "Boton_primario__x7a2"), no hay choques
import s from "./Boton.module.css";

function Boton({ variante = "primario", children, ...resto }) {
  return (
    <button className={`${s.boton} ${s[variante]}`} {...resto}>
      {children}
    </button>
  );
}
```

### 🌬️ Tailwind CSS (breve)

Tailwind usa **clases utilitarias** pequeñas directamente en el JSX: `p-4` (padding), `bg-blue-600`, `rounded-lg`. Escribes rápido sin inventar nombres de clases.

```bash
npm install tailwindcss @tailwindcss/vite
```

```js
// vite.config.js
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({ plugins: [react(), tailwindcss()] });
// y en index.css una sola línea: @import "tailwindcss";
```

```jsx
function Tarjeta({ titulo }) {
  return (
    <div className="p-4 rounded-xl shadow-md bg-white dark:bg-gray-800 hover:scale-105 transition">
      <h3 className="text-lg font-bold text-gray-900 dark:text-white">{titulo}</h3>
    </div>
  );
}
```

⚠️ En Tailwind no construyas clases con strings dinámicos (`bg-${color}-500`): Tailwind no las detecta. Usa clases completas en un objeto de mapeo.
💡 Elige una sola estrategia por proyecto. Para empezar: CSS Modules (aprendes CSS de verdad) o Tailwind (prototipas rápido).
🇬🇧 **stylesheet** /STÁIL-shit/ = hoja de estilos · **scope** /skoup/ = alcance · **utility class** /iu-TÍ-li-ti klas/ = clase utilitaria · **to override** /ou-ver-RÁID/ = sobrescribir · **layout** /LÉI-aut/ = disposición

## 🗄️ Estado global: Context vs Zustand

No todo estado debe ser global. Primero pregúntate: ¿quién necesita este dato? Sube el estado solo hasta el **ancestro común** más cercano (*lifting state up*). Si de verdad lo usa media app (carrito, sesión), entonces estado global.

| Tipo de estado | Herramienta recomendada |
|---|---|
| Local de un componente (input, modal abierto) | `useState` |
| Lógica de estado compleja con muchas acciones | `useReducer` |
| Compartido entre hermanos | Subir estado al padre |
| Global que cambia poco (tema, idioma, usuario) | Context |
| Global que cambia seguido (carrito, filtros) | **Zustand** (o Redux Toolkit) |
| Datos del servidor (APIs) | **TanStack Query** |
| Estado en la URL (búsqueda, página) | `useSearchParams` |

### 🐻 Zustand en 1 minuto

```bash
npm install zustand
```

```jsx
// store/carrito.js
import { create } from "zustand";

export const useCarrito = create((set) => ({
  items: [],
  agregar: (prod) => set((s) => ({ items: [...s.items, prod] })),
  quitar: (id) => set((s) => ({ items: s.items.filter((p) => p.id !== id) })),
  vaciar: () => set({ items: [] }),
}));

// Cualquier componente, sin Provider:
function IconoCarrito() {
  const cantidad = useCarrito((s) => s.items.length); // solo se redibuja si cambia esto
  return <span>🛒 {cantidad}</span>;
}

function BotonComprar({ producto }) {
  const agregar = useCarrito((s) => s.agregar);
  return <button onClick={() => agregar(producto)}>Agregar</button>;
}
```

### 🧮 useReducer (para lógica compleja)

```jsx
function reducer(estado, accion) {
  switch (accion.type) {
    case "sumar": return { ...estado, n: estado.n + 1 };
    case "reiniciar": return { ...estado, n: 0 };
    default: throw new Error("Acción desconocida: " + accion.type);
  }
}

const [estado, dispatch] = useReducer(reducer, { n: 0 });
dispatch({ type: "sumar" });
```

💡 Zustand con **selectores** (`useCarrito(s => s.items.length)`) evita renders innecesarios, algo que Context no hace por sí solo.
⚠️ No metas en el store global datos que vienen de una API "para cachearlos": eso lo hace mejor TanStack Query.
🇬🇧 **global state** /GLÓU-bal steit/ = estado global · **store** /stor/ = almacén · **reducer** /ri-DÚ-ser/ = reductor · **to dispatch** /dis-PÁCH/ = despachar, enviar una acción · **lifting state up** = subir el estado · **selector** /se-LÉK-tor/ = selector

## 🛡️ TypeScript con React (básico)

**TypeScript** añade tipos a JavaScript: el editor te avisa de errores **antes** de ejecutar ("esta prop es obligatoria", "esto puede ser null"). Es el estándar en la industria; vale la pena desde temprano. Archivos `.tsx` para componentes.

- `type Props = { titulo: string; precio?: number }` :: Tipar props (`?` = opcional)
- `function Tarjeta({ titulo, precio = 0 }: Props) {}` :: Usar el tipo en el componente
- `children: React.ReactNode` :: Tipo para `children`
- `useState<string>("")` :: Tipo explícito del estado (a veces se infiere solo)
- `useState<Usuario | null>(null)` :: Estado que puede estar vacío
- `useRef<HTMLInputElement>(null)` :: Ref a un input
- `(e: React.ChangeEvent<HTMLInputElement>) => {}` :: Tipo del evento onChange
- `onBorrar: (id: number) => void` :: Tipar una función que llega por props

```jsx
// Tarjeta.tsx
import { useState } from "react";

type Usuario = {
  id: number;
  nombre: string;
  rol: "admin" | "estudiante"; // solo esos dos valores
};

type Props = {
  usuario: Usuario;
  destacado?: boolean;
  onSeleccionar: (id: number) => void;
  children?: React.ReactNode;
};

export function TarjetaUsuario({ usuario, destacado = false, onSeleccionar, children }: Props) {
  const [likes, setLikes] = useState<number>(0);

  function manejarCambio(e: React.ChangeEvent<HTMLInputElement>) {
    console.log(e.target.value);
  }

  return (
    <div className={destacado ? "destacado" : ""} onClick={() => onSeleccionar(usuario.id)}>
      <h3>{usuario.nombre} {usuario.rol === "admin" && "👑"}</h3>
      <button onClick={() => setLikes((l) => l + 1)}>❤️ {likes}</button>
      <input onChange={manejarCambio} />
      {children}
    </div>
  );
}
```

💡 Pasa el cursor sobre cualquier prop o evento en VS Code y te dice su tipo exacto: copia de ahí en vez de memorizar.
⚠️ No abuses de `any`: apaga TypeScript justo donde más lo necesitas. Si no sabes el tipo, usa `unknown` y verifica.
🇬🇧 **type** /taip/ = tipo · **optional** /ÓP-sho-nal/ = opcional · **union type** /IÚ-nion taip/ = tipo unión (`a | b`) · **to infer** /in-FÉR/ = deducir · **type safety** /taip SÉIF-ti/ = seguridad de tipos

## ✨ Buenas prácticas y rendimiento

Escribir React que funciona es fácil; escribir React **mantenible** requiere hábitos. Estos son los que más diferencia hacen.

- `Componentes pequeños y con una sola responsabilidad` :: Si necesitas "y" para describirlo, divídelo
- `Estado lo más abajo posible` :: Solo sube cuando dos componentes lo necesiten
- `Una sola fuente de verdad` :: No dupliques datos entre estados; deriva lo que puedas
- `Componentes contenedor vs presentación` :: Uno trae datos, otro solo los muestra con props
- `Composición con children` :: Mejor `<Modal><Formulario /></Modal>` que props gigantes
- `Funciones puras` :: El componente no debe modificar variables de fuera durante el render
- `Early returns` :: Maneja loading/error/vacío arriba y deja el caso feliz al final
- `Nombres claros` :: `estaAbierto`, `onGuardar`, `handleSubmit`, `usuarios` (plural para arrays)
- `ESLint + Prettier` :: Detectar errores y formatear automáticamente
- `Error Boundaries` :: Capturar errores para que no se caiga toda la app (librería `react-error-boundary`)

```jsx
// Composición: el Modal no sabe qué tiene dentro, solo lo envuelve
function Modal({ abierto, onCerrar, titulo, children }) {
  if (!abierto) return null;
  return (
    <div className="fondo" onClick={onCerrar}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <header>
          <h2>{titulo}</h2>
          <button onClick={onCerrar} aria-label="Cerrar">✖️</button>
        </header>
        {children}
      </div>
    </div>
  );
}

// Uso
<Modal abierto={verLogin} onCerrar={() => setVerLogin(false)} titulo="Ingresar">
  <Login onLogin={iniciarSesion} />
</Modal>
```

⚠️ No declares un componente **dentro** de otro componente: se recrea en cada render y pierde su estado. Defínelos siempre en el nivel superior del archivo.
⚠️ Accesibilidad: usa `<button>` para acciones (no `<div onClick>`), pon `alt` en imágenes y `<label>` en inputs.
💡 Instala **React Developer Tools** en el navegador: ves el árbol de componentes, sus props, estado y qué se redibuja.
🇬🇧 **best practices** /best PRÁK-ti-ses/ = buenas prácticas · **maintainable** /mein-TÉI-na-bol/ = mantenible · **single responsibility** = responsabilidad única · **composition** /kom-po-SÍ-shon/ = composición · **accessibility (a11y)** /ak-se-si-BÍ-li-ti/ = accesibilidad · **pure function** /piur FÁNK-shon/ = función pura

### 🚄 Rendimiento

React ya es rápido por defecto. Los problemas reales suelen ser: renderizar listas enormes, recalcular cosas pesadas en cada tecla, o cargar todo el JavaScript de golpe. Mide primero, optimiza después.

- `React DevTools → Profiler` :: Graba una interacción y mira qué componentes tardan
- `lazy(() => import("./Admin"))` :: Carga perezosa: el código se descarga solo cuando se necesita
- `<Suspense fallback={<Spinner />}>` :: Muestra algo mientras carga un componente lazy
- `useDeferredValue(valor)` :: Versión "con retraso" de un valor para no bloquear al escribir
- `const [isPending, startTransition] = useTransition()` :: Marca una actualización como no urgente
- `react-window` / `@tanstack/react-virtual` :: Virtualizar listas de miles de filas (solo pinta las visibles)
- `memo`, `useMemo`, `useCallback` :: Evitar trabajo repetido (ver sección propia)
- `<img loading="lazy" />` :: Imágenes que cargan al acercarse con el scroll

```jsx
import { lazy, Suspense, useDeferredValue, useState } from "react";

const PanelAdmin = lazy(() => import("./pages/PanelAdmin")); // otro archivo .js separado

function App({ esAdmin, items }) {
  const [texto, setTexto] = useState("");
  const textoDiferido = useDeferredValue(texto); // el input responde al instante

  return (
    <>
      <input value={texto} onChange={(e) => setTexto(e.target.value)} />
      <ListaPesada filtro={textoDiferido} items={items} />

      {esAdmin && (
        <Suspense fallback={<p>⏳ Cargando panel...</p>}>
          <PanelAdmin />
        </Suspense>
      )}
    </>
  );
}
```

📌 Un componente se redibuja cuando: cambia su estado, cambia su padre (se redibuja), o cambia un contexto que usa. Redibujar no siempre significa tocar el DOM: React solo aplica las diferencias.
💡 Mide en modo producción (`npm run build && npm run preview`): el modo desarrollo es más lento a propósito.
🇬🇧 **performance** /per-FÓR-mans/ = rendimiento · **lazy loading** /LÉI-si LÓU-ding/ = carga perezosa · **bundle** /BÁN-dol/ = paquete de código · **to profile** /PRÓU-fail/ = perfilar, medir · **bottleneck** /BÓ-tol-nek/ = cuello de botella

## ☁️ Despliegue: build, Vercel y Netlify

Para publicar tu app, Vite la **compila** a archivos estáticos (HTML, CSS, JS minificados) en la carpeta `dist/`. Esos archivos se pueden subir a cualquier hosting estático. Vercel y Netlify tienen plan gratuito y despliegan solos cada vez que haces `git push`.

- `npm run build` :: Genera `dist/` optimizado
- `npm run preview` :: Probar `dist/` en local antes de subir
- `.env` con `VITE_API_URL=https://...` :: Variables de entorno (deben empezar con `VITE_`)
- `import.meta.env.VITE_API_URL` :: Leer la variable en el código
- `npm i -g vercel && vercel` :: Desplegar desde la terminal con Vercel
- `npx netlify deploy --prod --dir=dist` :: Desplegar `dist/` con Netlify CLI
- `base: "/mi-repo/"` :: En vite.config.js; necesario para GitHub Pages (sirve en subcarpeta)

```bash
# Flujo típico con GitHub + Vercel
git init && git add . && git commit -m "primera versión"
git remote add origin git@github.com:usuario/mi-app.git
git push -u origin main
# Luego en vercel.com → "Add New Project" → importar repo → Deploy
# Build command: npm run build  ·  Output directory: dist
```

### 🔁 Arreglar el 404 al recargar rutas (SPA)

```json
{
  "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }]
}
```

📌 Ese JSON va en `vercel.json` en la raíz. En Netlify, crea `public/_redirects` con la línea `/*  /index.html  200`.
⚠️ Todo lo que está en `VITE_...` termina dentro del JS público: nunca pongas ahí contraseñas ni claves privadas.
💡 Cada pull request en Vercel/Netlify genera una **URL de preview**: ideal para mostrar avances a tu equipo o docente.
🇬🇧 **deploy** /di-PLÓI/ = desplegar, publicar · **hosting** /JÓUS-ting/ = alojamiento · **environment variable** /en-VÁI-ron-ment/ = variable de entorno · **production** /pro-DÁK-shon/ = producción · **preview** /PRÍ-viu/ = vista previa · **rewrite** /ri-RÁIT/ = reescritura de URL

## 📊 Tabla resumen de hooks

| Hook | Para qué sirve | Ejemplo mínimo |
|---|---|---|
| `useState` | Guardar datos que cambian y redibujar | `const [n, setN] = useState(0)` |
| `useEffect` | Sincronizar con el exterior (API, timers, eventos) | `useEffect(() => {...}, [id])` |
| `useRef` | Acceder al DOM o guardar valores sin redibujar | `const r = useRef(null)` |
| `useContext` | Leer un contexto sin prop drilling | `const t = useContext(TemaCtx)` |
| `useReducer` | Estado con lógica compleja y acciones | `const [s, dispatch] = useReducer(fn, ini)` |
| `useMemo` | Memorizar un cálculo caro | `useMemo(() => calc(a), [a])` |
| `useCallback` | Memorizar una función para hijos con memo | `useCallback(() => f(id), [id])` |
| `useId` | Generar IDs únicos para label/input | `const id = useId()` |
| `useTransition` | Marcar actualizaciones como no urgentes | `const [pend, start] = useTransition()` |
| `useDeferredValue` | Retrasar un valor para no bloquear la UI | `const d = useDeferredValue(q)` |
| `useLayoutEffect` | Como useEffect pero antes de pintar (medir DOM) | `useLayoutEffect(() => {...}, [])` |
| `use` (19) | Leer una promesa o contexto (permite `if`) | `const t = use(TemaCtx)` |
| `useActionState` (19) | Estado de un formulario con Actions | `useActionState(accion, inicial)` |
| `useOptimistic` (19) | Mostrar el resultado antes de que responda el servidor | `useOptimistic(lista, fn)` |
| `useFormStatus` (19) | Saber si el formulario padre se está enviando | `const { pending } = useFormStatus()` |

### 📜 Reglas de los hooks

- `Solo en el nivel superior` :: Nunca dentro de `if`, bucles o funciones anidadas (excepto `use`)
- `Solo en componentes o hooks propios` :: No en funciones JS normales
- `Siempre en el mismo orden` :: React identifica cada hook por su posición

📌 Mapa mental final: **props** entran, **estado** recuerda, **efectos** hablan con el exterior, **refs** tocan el DOM, **contexto** comparte, **hooks propios** reutilizan.
💡 Ruta de estudio sugerida: contador → lista de tareas → buscador → app con API → login → router → contexto → Zustand → TypeScript → Next.js.
⚠️ Si un tutorial usa `class X extends React.Component`, `componentDidMount` o `this.setState`, es código antiguo: aprende la versión con funciones y hooks.
🇬🇧 **rules of hooks** /rúls ov juks/ = reglas de los hooks · **top level** /top LÉ-vel/ = nivel superior · **nested** /NÉS-ted/ = anidado · **cheat sheet** /chit shit/ = chuleta, hoja de referencia · **to keep learning** = seguir aprendiendo
