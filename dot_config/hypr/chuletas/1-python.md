# 🐍 Python
Cada línea: código :: explicación. Edita este archivo para añadir las tuyas.

## Básico
nombre = "Ana"; edad = 20 :: Variables: no se declara el tipo
print(f"Hola {nombre}, tienes {edad}") :: f-string: mete variables dentro del texto
input("¿Tu nombre? ") :: Lee texto del teclado (siempre devuelve str)
int("42"), float("3.5"), str(10) :: Convertir entre tipos
type(x), isinstance(x, int) :: ¿De qué tipo es x?
a // b, a % b, a ** b :: División entera, resto, potencia

## Condiciones y bucles
if x > 0: ... elif x == 0: ... else: ... :: Condicional
for i in range(5): :: Repite con i = 0, 1, 2, 3, 4
for i, v in enumerate(lista): :: Recorre con índice y valor a la vez
for a, b in zip(xs, ys): :: Recorre dos listas en paralelo
while n > 0: n -= 1 :: Repite mientras se cumpla
break / continue :: Salir del bucle / saltar a la siguiente vuelta
x = "par" if n % 2 == 0 else "impar" :: If en una línea (ternario)

## Listas
xs = [3, 1, 2] :: Crear lista (se puede modificar)
xs.append(4); xs.pop() :: Añadir al final / sacar el último
xs[0], xs[-1], xs[1:3] :: Primero, último, rebanada [1, 3)
xs[::-1] :: Lista al revés
sorted(xs), xs.sort(reverse=True) :: Ordenar (nueva / en el sitio)
len(xs), sum(xs), max(xs), min(xs) :: Tamaño, suma, mayor, menor
[x * 2 for x in xs if x > 1] :: List comprehension: transformar y filtrar
x in xs :: ¿Está x en la lista?

## Diccionarios y conjuntos
d = {"nombre": "Ana", "edad": 20} :: Diccionario clave → valor
d["edad"], d.get("email", "—") :: Leer (get no falla si no existe)
for k, v in d.items(): :: Recorrer claves y valores
{k: v for k, v in d.items() if v} :: Dict comprehension
s = {1, 2, 3}; s & t; s | t :: Conjunto: intersección, unión
from collections import Counter; Counter("banana") :: Contar repeticiones

## Funciones
def sumar(a, b=0): return a + b :: Función con valor por defecto
def f(*args, **kwargs): :: Recibe cualquier cantidad de argumentos
cuadrado = lambda x: x ** 2 :: Función anónima de una línea
def saludar(nombre: str) -> str: :: Pistas de tipo (no obligan, ayudan al editor)

## Clases
class Perro: :: Definir una clase
def __init__(self, nombre): self.nombre = nombre :: Constructor: se ejecuta al crear el objeto
def __str__(self): return self.nombre :: Cómo se ve al imprimirlo
class Cachorro(Perro): :: Herencia
from dataclasses import dataclass :: @dataclass crea __init__ y __repr__ solo

## Archivos y errores
with open("datos.txt", encoding="utf-8") as f: texto = f.read() :: Leer un archivo (se cierra solo)
with open("salida.txt", "w") as f: f.write("hola\n") :: Escribir un archivo
from pathlib import Path; Path("a/b.txt").read_text() :: Rutas modernas
import json; json.loads(s); json.dumps(d, indent=2) :: Texto JSON ↔ diccionario
try: ... except ValueError as e: ... finally: ... :: Capturar errores
raise ValueError("edad negativa") :: Lanzar un error propio

## Útiles
import random; random.choice(xs); random.randint(1, 6) :: Aleatorios
from datetime import datetime; datetime.now() :: Fecha y hora actual
" ".join(palabras); texto.split(",") :: Unir / partir texto
texto.strip().lower().replace("a", "b") :: Limpiar y transformar texto
python -m venv .venv && source .venv/bin/activate :: Entorno virtual (en fish: activate.fish)
pip install requests :: Instalar un paquete
if __name__ == "__main__": main() :: Ejecutar solo si es el archivo principal
