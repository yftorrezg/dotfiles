# 🟨 JavaScript
Cada línea: código :: explicación. Edita este archivo para añadir las tuyas.

## Básico
const nombre = "Ana"; let edad = 20; :: const no se reasigna; let sí (evita var)
console.log(`Hola ${nombre}`) :: Template string con variables
typeof x; Array.isArray(xs) :: ¿Qué tipo es?
Number("42"); String(10); parseInt("8px") :: Convertir tipos
a === b; a !== b :: Comparar SIN conversión rara (usa siempre ===)
x ?? "por defecto" :: Valor si x es null o undefined
obj?.direccion?.ciudad :: Encadenamiento opcional: no falla si algo falta

## Condiciones y bucles
if (x > 0) {} else if (x === 0) {} else {} :: Condicional
const tipo = n % 2 === 0 ? "par" : "impar"; :: Ternario
for (let i = 0; i < 5; i++) {} :: Bucle clásico
for (const v of lista) {} :: Recorre valores de un array
for (const k in objeto) {} :: Recorre claves de un objeto
switch (dia) { case 1: ...; break; default: ... } :: Varios casos

## Arrays
const xs = [3, 1, 2]; :: Crear array
xs.push(4); xs.pop(); xs.unshift(0); :: Añadir/sacar al final y al inicio
xs.map(x => x * 2) :: Transformar cada elemento (devuelve array nuevo)
xs.filter(x => x > 1) :: Quedarse con los que cumplen
xs.reduce((acc, x) => acc + x, 0) :: Reducir a un solo valor (ej. suma)
xs.find(x => x > 1); xs.includes(2) :: Buscar el primero / ¿está?
[...xs].sort((a, b) => a - b) :: Ordenar números (copia, sin tocar el original)
xs.slice(1, 3); xs.at(-1) :: Rebanada / último elemento

## Objetos
const p = { nombre: "Ana", edad: 20 }; :: Objeto literal
const { nombre, edad } = p; :: Desestructurar: sacar propiedades a variables
const copia = { ...p, edad: 21 }; :: Copiar y cambiar una propiedad
Object.keys(p); Object.entries(p) :: Claves / pares [clave, valor]
JSON.stringify(p); JSON.parse(texto) :: Objeto ↔ texto JSON

## Funciones
function sumar(a, b = 0) { return a + b; } :: Función clásica con valor por defecto
const sumar = (a, b) => a + b; :: Función flecha (return implícito)
const f = (...nums) => nums.length; :: Parámetros rest: cualquier cantidad
class Perro { constructor(n) { this.nombre = n; } } :: Clase
class Cachorro extends Perro {} :: Herencia

## Asíncrono
const r = await fetch("/api/datos"); :: Pedir datos (dentro de una función async)
const datos = await r.json(); :: Leer la respuesta como JSON
async function cargar() { try { ... } catch (e) { ... } } :: async/await con errores
Promise.all([p1, p2]) :: Esperar varias promesas a la vez
setTimeout(() => {}, 1000); setInterval(f, 1000); :: Ejecutar después / cada X ms

## DOM (navegador)
document.querySelector(".boton") :: Primer elemento que coincide con el selector CSS
document.querySelectorAll("li") :: Todos los que coinciden
el.addEventListener("click", e => {}) :: Reaccionar a un clic
el.textContent = "Hola"; el.classList.toggle("activo"); :: Cambiar texto / alternar clase
el.style.color = "red"; el.setAttribute("href", url); :: Estilos y atributos
localStorage.setItem("clave", "valor") :: Guardar en el navegador

## Módulos y Node
export function f() {}; import { f } from "./util.js"; :: Exportar / importar
npm init -y; npm install express :: Crear proyecto / instalar paquete
npm run dev :: Ejecutar el script "dev" de package.json
node archivo.js :: Ejecutar con Node
