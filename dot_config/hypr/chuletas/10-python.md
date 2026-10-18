# 🐍 Python
> El lenguaje de la IA y la ciencia de datos: de print("hola") a clases, generadores, APIs, pandas y tests.

## 🌱 Básicos: variables, tipos y números

Python es **interpretado** (no compilas: ejecutas `python archivo.py`) y de **tipado dinámico** (no declaras el tipo; la variable es una etiqueta pegada a un valor). La **indentación** (4 espacios) no es estética: marca los bloques, como las llaves `{}` en otros lenguajes.

Analogía: una variable es un **post-it** con un nombre pegado sobre una caja. `x = 5` pega el post-it "x" en la caja que contiene 5; `x = "hola"` despega el post-it y lo pega en otra caja.

- `nombre = "Ana"; edad = 20` :: Variables: no se declara el tipo
- `print("Hola", nombre, sep=" - ", end="!\n")` :: Imprimir con separador y final propios
- `input("¿Tu nombre? ")` :: Lee texto del teclado (SIEMPRE devuelve str)
- `int("42"), float("3.5"), str(10), bool(0)` :: Convertir entre tipos
- `type(x), isinstance(x, (int, float))` :: ¿De qué tipo es x?
- `a, b = b, a` :: Intercambiar dos variables sin auxiliar
- `x = y = 0` :: Asignar el mismo valor a varias
- `None` :: "Nada": valor vacío (como null)
- `# comentario` :: Comentario de una línea
- `help(str.split)` :: Ayuda de cualquier cosa en la consola

| Tipo | Ejemplo | Mutable | Para qué |
|---|---|---|---|
| `int` | `42`, `-7`, `1_000_000` | No | Enteros (sin límite de tamaño) |
| `float` | `3.14`, `1e-3` | No | Decimales (aproximados) |
| `bool` | `True`, `False` | No | Verdadero / falso |
| `str` | `"hola"`, `'hola'` | No | Texto |
| `list` | `[1, 2, 3]` | Sí | Secuencia modificable |
| `tuple` | `(1, 2)` | No | Secuencia fija |
| `dict` | `{"a": 1}` | Sí | Clave → valor |
| `set` | `{1, 2}` | Sí | Elementos únicos |
| `NoneType` | `None` | No | Ausencia de valor |

### 🔢 Operadores y números

- `7 / 2` :: División normal → 3.5 (siempre float)
- `7 // 2` :: División entera → 3
- `7 % 2` :: Resto (módulo) → 1; `n % 2 == 0` = es par
- `2 ** 10` :: Potencia → 1024
- `divmod(17, 5)` :: Cociente y resto juntos → (3, 2)
- `round(3.14159, 2)` :: Redondear → 3.14
- `abs(-5), max(3, 9), min(3, 9)` :: Valor absoluto, mayor, menor
- `x += 1` :: Atajo de `x = x + 1` (también -=, *=, /=)
- `import math; math.sqrt(16), math.pi, math.floor(2.7)` :: Raíz, π, piso
- `0.1 + 0.2 == 0.3` :: ¡False! (los float son aproximados)
- `math.isclose(0.1 + 0.2, 0.3)` :: Así se comparan floats → True
- `from decimal import Decimal; Decimal("0.1") + Decimal("0.2")` :: Decimales exactos (dinero)
- `0b1010, 0xFF, bin(10), hex(255)` :: Binario y hexadecimal

⚠️ Cuidado: `input()` devuelve texto. `input("Edad: ") + 1` da error; usa `int(input("Edad: "))`.

💡 Consejo: en la terminal escribe `python` y tendrás la consola interactiva (REPL) para probar cualquier línea al instante. `ipython` es aún más cómoda.

🇬🇧 **variable** /vériabol/ = variable · **string** /string/ = cadena de texto · **integer** /ínteyer/ = entero · **float** /flóut/ = decimal · **boolean** /búlian/ = booleano · **indentation** /indentéishon/ = sangría

## 🔤 Strings y f-strings

Un **string** es una secuencia **inmutable** de caracteres: los métodos no lo cambian, devuelven uno nuevo. Por eso se escribe `s = s.upper()` y no solo `s.upper()`.

- `s[0], s[-1], s[1:4], s[::-1]` :: Primer carácter, último, rebanada, al revés
- `len(s)` :: Longitud
- `"ab" * 3` :: Repetir → "ababab"
- `"py" in "python"` :: ¿Contiene? → True
- `"""texto de varias líneas"""` :: String multilínea (también para docstrings)
- `r"C:\nueva\ruta"` :: String "crudo": las barras no son escapes (útil en regex)

| Método | Qué hace | Ejemplo → resultado |
|---|---|---|
| `upper()` / `lower()` | Mayúsculas / minúsculas | `"Hola".upper()` → `"HOLA"` |
| `title()` / `capitalize()` | Cada palabra / solo la primera | `"la paz".title()` → `"La Paz"` |
| `strip()` | Quita espacios a los lados | `"  hola ".strip()` → `"hola"` |
| `split(sep)` | Parte en lista | `"a,b,c".split(",")` → `['a', 'b', 'c']` |
| `sep.join(lista)` | Une una lista | `"-".join(["a", "b"])` → `"a-b"` |
| `replace(a, b)` | Reemplaza | `"hola".replace("o", "0")` → `"h0la"` |
| `find(x)` | Posición (o -1) | `"hola".find("l")` → `2` |
| `count(x)` | Cuántas veces | `"banana".count("a")` → `3` |
| `startswith` / `endswith` | Empieza / termina con | `"foto.png".endswith(".png")` → `True` |
| `isdigit()` / `isalpha()` | ¿Solo dígitos / letras? | `"123".isdigit()` → `True` |
| `zfill(n)` | Rellena con ceros | `"7".zfill(3)` → `"007"` |
| `center(n, c)` | Centra | `"hi".center(6, "*")` → `"**hi**"` |

### ✨ f-strings con formato

Las **f-strings** (`f"..."`) meten expresiones dentro del texto entre `{}`. Después de `:` va el **formato**.

| Formato | Ejemplo | Resultado |
|---|---|---|
| Decimales | `f"{3.14159:.2f}"` | `3.14` |
| Miles | `f"{1234567:,}"` | `1,234,567` |
| Porcentaje | `f"{0.875:.1%}"` | `87.5%` |
| Ancho a la derecha | `f"{42:>6}"` | `    42` |
| Ancho a la izquierda | `f"{'ab':<5}"` + `"|"` | `ab   |` |
| Centrado con relleno | `f"{'hi':*^8}"` | `***hi***` |
| Ceros a la izquierda | `f"{7:03d}"` | `007` |
| Binario / hexadecimal | `f"{10:b} {255:x}"` | `1010 ff` |
| Depuración | `f"{x=}"` | `x=5` |
| Notación científica | `f"{12345.678:.2e}"` | `1.23e+04` |

### ✅ Ejemplo resuelto: boleta de compra alineada

```python
productos = [("Salteña", 4, 6.5), ("Api morado", 2, 5.0), ("Pastel", 3, 3.5)]

total = 0
print(f"{'Producto':<12}{'Cant':>5}{'Precio':>9}{'Subtotal':>10}")
print("-" * 36)
for nombre, cant, precio in productos:
    subtotal = cant * precio
    total += subtotal
    print(f"{nombre:<12}{cant:>5}{precio:>9.2f}{subtotal:>10.2f}")
print("-" * 36)
print(f"{'TOTAL Bs.':<26}{total:>10.2f}")
```

Qué hace cada parte: la lista tiene tuplas (nombre, cantidad, precio); el `for` las **desempaqueta** en tres variables; `:<12` alinea a la izquierda en 12 caracteres y `:>9.2f` a la derecha con 2 decimales; `"-" * 36` dibuja la línea.

```text
Producto     Cant   Precio  Subtotal
------------------------------------
Salteña         4     6.50     26.00
Api morado      2     5.00     10.00
Pastel          3     3.50     10.50
------------------------------------
TOTAL Bs.                      46.50
```

⚠️ Cuidado: los strings son inmutables: `s[0] = "H"` da `TypeError`. Crea uno nuevo: `s = "H" + s[1:]`.

💡 Consejo: para concatenar muchos trozos en un bucle, guárdalos en una lista y al final haz `"".join(lista)`: es mucho más rápido que `+=`.

🇬🇧 **slice** /sláis/ = rebanada · **immutable** /imiútabol/ = inmutable · **split** /split/ = partir · **join** /yóin/ = unir · **whitespace** /uáit-spéis/ = espacios en blanco · **padding** /páding/ = relleno

## 📋 Listas y tuplas

Una **lista** es una fila ordenada y modificable de elementos (pueden ser de tipos distintos). Una **tupla** es igual pero **fija**: no se puede cambiar. Usa tuplas para datos que van juntos y no cambian (coordenadas, un registro), y listas para colecciones que crecen.

Analogía: la lista es una **mochila** (metes y sacas cosas); la tupla es una **foto** (lo que salió, salió).

| Método de lista | Qué hace | Ejemplo con `xs = [3, 1, 2]` |
|---|---|---|
| `append(x)` | Añade al final | `xs.append(4)` → `[3, 1, 2, 4]` |
| `extend(otra)` | Añade varios | `xs.extend([5, 6])` |
| `insert(i, x)` | Inserta en una posición | `xs.insert(0, 9)` → `[9, 3, 1, 2]` |
| `pop()` / `pop(i)` | Saca y devuelve el último / el i | `xs.pop()` → `2` |
| `remove(x)` | Quita la primera aparición de x | `xs.remove(1)` → `[3, 2]` |
| `index(x)` | Posición de x | `xs.index(2)` → `2` |
| `count(x)` | Cuántas veces está | `xs.count(3)` → `1` |
| `sort()` | Ordena en el sitio (devuelve None) | `xs.sort()` → `[1, 2, 3]` |
| `reverse()` | Invierte en el sitio | `xs.reverse()` → `[2, 1, 3]` |
| `copy()` | Copia superficial | `ys = xs.copy()` |
| `clear()` | Vacía | `xs.clear()` → `[]` |

- `xs[0], xs[-1], xs[1:3], xs[::2]` :: Primero, último, rebanada [1, 3), de dos en dos
- `xs[::-1]` :: Lista al revés (copia)
- `sorted(xs, reverse=True)` :: Nueva lista ordenada (no toca la original)
- `len(xs), sum(xs), max(xs), min(xs)` :: Tamaño, suma, mayor, menor
- `x in xs` :: ¿Está x en la lista?
- `del xs[0]` :: Borra por posición
- `[0] * 5` :: Lista de cinco ceros
- `primero, *resto = [1, 2, 3, 4]` :: Desempaquetado: primero=1, resto=[2, 3, 4]
- `t = (1, 2); t = 1, 2` :: Tupla (los paréntesis son opcionales)
- `t = (5,)` :: Tupla de UN elemento: lleva coma
- `x, y = (10, 20)` :: Desempaquetar una tupla
- `from collections import namedtuple` :: Tuplas con nombres de campo

⚠️ Cuidado: `ys = xs` NO copia: las dos variables apuntan a la MISMA lista. Si cambias `ys`, cambia `xs`. Usa `ys = xs.copy()` o `ys = xs[:]`.

⚠️ Cuidado: `xs = xs.sort()` deja `xs` en `None`, porque `sort()` ordena en el sitio y no devuelve nada. Usa `xs.sort()` solo, o `xs = sorted(xs)`.

⚠️ Cuidado: `[[0] * 3] * 3` crea tres referencias a LA MISMA fila. Para una matriz usa `[[0] * 3 for _ in range(3)]`.

🇬🇧 **list** /list/ = lista · **tuple** /túpol/ = tupla · **append** /apénd/ = añadir al final · **index** /índeks/ = índice · **mutable** /miútabol/ = modificable · **unpacking** /anpáking/ = desempaquetado

## 📖 Diccionarios y conjuntos

Un **diccionario** (`dict`) guarda pares **clave → valor**, como una agenda: buscas por el nombre (clave) y obtienes el teléfono (valor). Buscar es instantáneo aunque tenga millones de elementos (usa una tabla hash). Desde Python 3.7 mantienen el orden de inserción.

Un **conjunto** (`set`) es una bolsa de elementos **sin repetidos y sin orden**. Ideal para quitar duplicados y para preguntar "¿está?" muy rápido.

| Método de dict | Qué hace | Ejemplo |
|---|---|---|
| `d[k]` | Lee (KeyError si no existe) | `d["nombre"]` |
| `d.get(k, defecto)` | Lee sin fallar | `d.get("email", "—")` |
| `d[k] = v` | Crea o cambia | `d["edad"] = 21` |
| `d.keys()` / `values()` / `items()` | Claves / valores / pares | `for k, v in d.items():` |
| `d.pop(k)` | Saca y devuelve | `d.pop("edad")` |
| `d.update(otro)` | Mezcla otro dict | `d.update({"ciudad": "Sucre"})` |
| `d.setdefault(k, v)` | Lee, o crea con v si no existe | `d.setdefault("tags", []).append("x")` |
| `k in d` | ¿Existe la clave? | `"nombre" in d` |
| `d \| otro` | Unión de dicts (3.9+) | `base \| extra` |
| `dict(zip(ks, vs))` | Crear desde dos listas | `dict(zip(["a", "b"], [1, 2]))` |

| Operación de set | Símbolo | Ejemplo con `a={1,2,3}`, `b={2,3,4}` |
|---|---|---|
| Unión | `a \| b` | `{1, 2, 3, 4}` |
| Intersección | `a & b` | `{2, 3}` |
| Diferencia | `a - b` | `{1}` |
| Diferencia simétrica | `a ^ b` | `{1, 4}` |
| Añadir / quitar | `add(x)` / `discard(x)` | `a.add(5)` |
| ¿Subconjunto? | `a <= b` | `False` |

- `set()` :: Conjunto vacío (`{}` es un dict vacío, ¡no un set!)
- `list(set(xs))` :: Quitar duplicados (pierde el orden)
- `list(dict.fromkeys(xs))` :: Quitar duplicados conservando el orden

### ✅ Ejemplo resuelto: agenda de notas por alumno

```python
notas = {"Ana": [85, 92], "Luis": [70], "Sofía": []}

notas["Luis"].append(78)
notas.setdefault("Pedro", []).append(60)

for alumno, lista in notas.items():
    promedio = sum(lista) / len(lista) if lista else 0
    print(f"{alumno:<6} {lista} -> {promedio:.1f}")

materias_ana = {"Cálculo", "Física", "Programación"}
materias_luis = {"Física", "Programación", "Química"}
print("En común:", sorted(materias_ana & materias_luis))
```

Qué hace cada parte: `notas["Luis"].append(78)` modifica la lista guardada en el dict; `setdefault` crea la clave "Pedro" con lista vacía porque no existía y le añade 60; el ternario evita dividir entre cero con Sofía; `&` saca la intersección y `sorted` la ordena para que la salida sea siempre igual.

```text
Ana    [85, 92] -> 88.5
Luis   [70, 78] -> 74.0
Sofía  [] -> 0.0
Pedro  [60] -> 60.0
En común: ['Física', 'Programación']
```

⚠️ Cuidado: las claves de un dict deben ser **inmutables** (str, int, tuple). Una lista no puede ser clave: `TypeError: unhashable type: 'list'`.

💡 Consejo: `x in mi_set` es casi instantáneo, `x in mi_lista` recorre toda la lista. Si vas a preguntar muchas veces, convierte a set.

🇬🇧 **dictionary** /díkshoneri/ = diccionario · **key** /kí/ = clave · **value** /váliu/ = valor · **set** /set/ = conjunto · **hashable** /jáshabol/ = que se puede usar como clave · **lookup** /lúk-ap/ = búsqueda

## 🧩 Comprehensions

Una **comprehension** construye una lista, dict o set en una sola línea: "dame `expresión` para cada `x` de `algo` que cumpla `condición`". Es más corta y más rápida que un `for` con `append`. Se lee casi como en matemáticas: { x² | x ∈ N, x par }.

```python
# Estructura:  [EXPRESIÓN  for VARIABLE in ITERABLE  if CONDICIÓN]
cuadrados = [x ** 2 for x in range(10)]
pares     = [x for x in range(20) if x % 2 == 0]
etiquetas = ["par" if x % 2 == 0 else "impar" for x in range(4)]   # if-else va ANTES del for
```

- `[x * 2 for x in xs if x > 1]` :: Lista: transformar y filtrar
- `{k: v for k, v in d.items() if v > 0}` :: Dict comprehension
- `{p.lower() for p in palabras}` :: Set comprehension (únicos)
- `(x ** 2 for x in range(10**9))` :: Generador: con paréntesis, no gasta memoria
- `sum(x ** 2 for x in range(10))` :: Generador directo dentro de una función
- `[(i, j) for i in range(3) for j in range(2)]` :: Doble bucle (el primer for es el de fuera)
- `[c for fila in matriz for c in fila]` :: Aplanar una matriz
- `{v: k for k, v in d.items()}` :: Invertir un diccionario

### ✅ Ejemplo resuelto: limpiar y analizar una lista de correos

```python
correos = [" Ana@Gmail.com", "luis@umsa.bo ", "ANA@gmail.com", "", "sofia@ucb.edu.bo"]

limpios = sorted({c.strip().lower() for c in correos if c.strip()})
dominios = {c: c.split("@")[1] for c in limpios}
bolivianos = [c for c in limpios if c.endswith(".bo")]

print(limpios)
print(dominios)
print(bolivianos)
```

Qué hace cada parte: el set comprehension limpia espacios, pasa a minúsculas, descarta vacíos (`if c.strip()`) y elimina el duplicado de Ana; `sorted` lo convierte en lista ordenada; el dict comprehension asocia cada correo con su dominio; el último filtra los terminados en `.bo`.

```text
['ana@gmail.com', 'luis@umsa.bo', 'sofia@ucb.edu.bo']
{'ana@gmail.com': 'gmail.com', 'luis@umsa.bo': 'umsa.bo', 'sofia@ucb.edu.bo': 'ucb.edu.bo'}
['luis@umsa.bo', 'sofia@ucb.edu.bo']
```

⚠️ Cuidado: si la comprehension no cabe en una línea o tiene más de dos `for`, vuelve al `for` normal. Legible > ingenioso.

🇬🇧 **comprehension** /komprijénshon/ = comprensión (construcción compacta) · **iterable** /íterabol/ = recorrible · **filter** /fílter/ = filtrar · **nested** /nésted/ = anidado · **flatten** /fláten/ = aplanar

## 🔀 Condicionales y bucles

`if` decide, `for` recorre algo, `while` repite mientras se cumpla una condición. En Python el `for` no cuenta números como en C: **recorre** cualquier iterable (lista, string, archivo, dict...).

- `if x > 0: ... elif x == 0: ... else: ...` :: Condicional
- `x = "par" if n % 2 == 0 else "impar"` :: If en una línea (ternario)
- `if 18 <= edad < 65:` :: Comparaciones encadenadas
- `if not lista:` :: ¿Está vacía? (vacíos, 0 y None cuentan como False)
- `and, or, not` :: Operadores lógicos (en palabras, no && ||)
- `x is None` :: Comparar con None usando is, no ==
- `for i in range(5):` :: i = 0, 1, 2, 3, 4
- `range(inicio, fin, paso)` :: `range(10, 0, -2)` → 10, 8, 6, 4, 2
- `for i, v in enumerate(lista, start=1):` :: Índice y valor a la vez
- `for a, b in zip(xs, ys):` :: Dos listas en paralelo
- `for k, v in d.items():` :: Recorrer un dict
- `while n > 0: n -= 1` :: Repite mientras se cumpla
- `break / continue` :: Salir del bucle / saltar a la siguiente vuelta
- `for ... else:` :: El else corre si el bucle NO terminó con break
- `pass` :: "No hacer nada" (bloque vacío)

### 🎯 match (Python 3.10+)

```python
def describir(comando):
    match comando.split():
        case ["salir"]:
            return "Adiós"
        case ["ir", direccion]:
            return f"Vas hacia {direccion}"
        case ["comprar", *cosas] if cosas:
            return f"Compras {len(cosas)} cosas"
        case _:
            return "No entiendo"

print(describir("ir norte"))         # Vas hacia norte
print(describir("comprar pan leche"))  # Compras 2 cosas
```

### ✅ Ejemplo resuelto: FizzBuzz y búsqueda de primos

```python
for n in range(1, 16):
    if n % 15 == 0:
        print("FizzBuzz", end=" ")
    elif n % 3 == 0:
        print("Fizz", end=" ")
    elif n % 5 == 0:
        print("Buzz", end=" ")
    else:
        print(n, end=" ")
print()

primos = []
for n in range(2, 30):
    for d in range(2, int(n ** 0.5) + 1):
        if n % d == 0:
            break
    else:
        primos.append(n)
print(primos)
```

Qué hace cada parte: FizzBuzz comprueba primero el caso 15 (si no, nunca llegaría); `end=" "` imprime en la misma línea. En los primos, el `for` interno busca un divisor hasta la raíz cuadrada; si lo encuentra hace `break`; el `else` del `for` solo corre cuando NO hubo `break`, es decir, cuando n es primo.

```text
1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz 11 Fizz 13 14 FizzBuzz 
[2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
```

⚠️ Cuidado: no modifiques una lista mientras la recorres con `for` (te saltarás elementos). Recorre una copia (`for x in xs[:]`) o crea una nueva con comprehension.

🇬🇧 **loop** /lup/ = bucle · **condition** /kondíshon/ = condición · **break** /bréik/ = romper (salir) · **statement** /stéitment/ = sentencia · **pattern matching** /pátern máching/ = coincidencia de patrones

## 🧰 Funciones

Una **función** es una receta con nombre: recibe ingredientes (parámetros), hace algo y devuelve un resultado con `return`. Si no hay `return`, devuelve `None`. Las funciones son **objetos**: se pueden guardar en variables y pasar a otras funciones.

```python
def saludar(nombre: str, saludo: str = "Hola") -> str:
    """Devuelve un saludo. (Esto es un docstring: documentación.)"""
    return f"{saludo}, {nombre}!"

saludar("Ana")                    # 'Hola, Ana!'
saludar("Ana", saludo="Buenas")   # argumento por nombre (keyword)
```

| Tipo de parámetro | Sintaxis | Qué recibe |
|---|---|---|
| Posicional | `def f(a, b)` | Por orden: `f(1, 2)` |
| Por defecto | `def f(a, b=10)` | Opcional: `f(1)` |
| `*args` | `def f(*args)` | Tupla con los posicionales extra |
| `**kwargs` | `def f(**kwargs)` | Dict con los nombrados extra |
| Solo por nombre | `def f(a, *, b)` | `b` debe ir como `b=...` |
| Solo posicional | `def f(a, /, b)` | `a` no se puede pasar por nombre |

- `cuadrado = lambda x: x ** 2` :: Función anónima de una línea
- `def f(*args, **kwargs):` :: Recibe cualquier cantidad de argumentos
- `f(*lista, **diccionario)` :: Desempaquetar al LLAMAR
- `return a, b` :: Devolver varios valores (en realidad, una tupla)
- `def f(xs: list[int]) -> dict[str, float]:` :: Type hints con genéricos
- `def f(x: int | None = None):` :: Valor que puede ser None (3.10+)
- `from typing import Callable, Iterable, Optional` :: Más tipos para hints
- `global contador` :: Modificar una variable global (evítalo)
- `nonlocal total` :: Modificar una variable de la función exterior

### ✅ Ejemplo resuelto: args, kwargs y lambda juntos

```python
def resumen(titulo, *numeros, decimales=2, **extra):
    total = sum(numeros)
    promedio = total / len(numeros) if numeros else 0
    print(f"{titulo}: total={total}, promedio={promedio:.{decimales}f}")
    for clave, valor in extra.items():
        print(f"  {clave} = {valor}")

resumen("Ventas", 10, 20, 35)
resumen("Notas", 51, 87, decimales=1, curso="INF-111", docente="Quispe")

alumnos = [("Ana", 88), ("Luis", 95), ("Sofía", 72)]
print(sorted(alumnos, key=lambda a: a[1], reverse=True))
```

Qué hace cada parte: `*numeros` junta todos los números sueltos en una tupla; `decimales` va después de `*numeros`, así que solo se puede pasar por nombre; `**extra` recoge los argumentos nombrados que sobran en un dict; `{promedio:.{decimales}f}` usa una variable dentro del formato; la lambda le dice a `sorted` que ordene por la nota (posición 1).

```text
Ventas: total=65, promedio=21.67
Notas: total=138, promedio=69.0
  curso = INF-111
  docente = Quispe
[('Luis', 95), ('Ana', 88), ('Sofía', 72)]
```

⚠️ Cuidado: NUNCA uses una lista o dict como valor por defecto: `def f(x, lista=[])`. Se crea UNA vez y se comparte entre llamadas. Usa `lista=None` y dentro `if lista is None: lista = []`.

💡 Consejo: los type hints no los comprueba Python al ejecutar, pero tu editor y `mypy` sí: detectan errores antes de correr el programa. Acostúmbrate a ponerlos.

🇬🇧 **function** /fánkshon/ = función · **argument** /árguiument/ = argumento · **parameter** /parámeter/ = parámetro · **return** /ritérn/ = devolver · **default** /difólt/ = por defecto · **type hint** /táip jint/ = pista de tipo

## 📦 Módulos y paquetes

Un **módulo** es un archivo `.py`; un **paquete** es una carpeta con módulos (y normalmente un `__init__.py`). `import` carga código de otro archivo para reutilizarlo. La **biblioteca estándar** ("baterías incluidas") trae cientos de módulos listos: `math`, `random`, `json`, `os`, `pathlib`, `datetime`...

```text
mi_proyecto/
├── main.py
└── utilidades/
    ├── __init__.py
    ├── texto.py        # def limpiar(s): ...
    └── numeros.py      # def promedio(xs): ...
```

```python
# main.py
from utilidades.texto import limpiar
from utilidades import numeros

print(limpiar("  Hola  "))
print(numeros.promedio([1, 2, 3]))
```

- `import math` :: Importar el módulo entero: `math.sqrt(2)`
- `from math import sqrt, pi` :: Importar nombres concretos
- `import numpy as np` :: Importar con alias (convención)
- `from . import modelo` :: Import relativo dentro de un paquete
- `if __name__ == "__main__": main()` :: Código que solo corre si ejecutas ESTE archivo (no al importarlo)
- `python -m paquete.modulo` :: Ejecutar un módulo como programa
- `import sys; sys.path` :: Dónde busca Python los módulos
- `dir(math)` :: Qué hay dentro de un módulo

| Módulo estándar | Para qué |
|---|---|
| `os`, `sys`, `shutil` | Sistema, argumentos, copiar/mover archivos |
| `pathlib` | Rutas y archivos (moderno) |
| `json`, `csv` | Formatos de datos |
| `datetime`, `time` | Fechas y tiempo |
| `random`, `math`, `statistics` | Azar y matemáticas |
| `re` | Expresiones regulares |
| `collections`, `itertools`, `functools` | Estructuras y herramientas funcionales |
| `argparse` | Argumentos de línea de comandos |
| `logging` | Registro de eventos (mejor que print) |
| `subprocess` | Ejecutar otros programas |
| `sqlite3` | Base de datos SQL incluida |

⚠️ Cuidado: no llames a tus archivos como módulos existentes (`random.py`, `json.py`, `pandas.py`): Python importará el tuyo y todo fallará de forma rara.

⚠️ Cuidado: evita `from modulo import *`: no sabes qué nombres trae y puede pisar los tuyos.

🇬🇧 **module** /módiul/ = módulo · **package** /pákech/ = paquete · **import** /ímport/ = importar · **standard library** /stándard láibreri/ = biblioteca estándar · **alias** /éilias/ = alias

## 🧪 Entornos virtuales: venv, pip y uv

Cada proyecto necesita sus propias versiones de librerías (uno usa Django 4 y otro Django 5). Un **entorno virtual** es una carpeta (`.venv`) con un Python y sus paquetes **aislados** del sistema. Analogía: una caja de herramientas por proyecto, en vez de una sola caja revuelta para todo.

En Arch, `pip install` fuera de un venv da el error **externally-managed-environment**: el sistema te protege para que no rompas los paquetes de pacman. Solución: siempre venv (o uv).

```bash
# Con venv + pip (clásico)
python -m venv .venv
source .venv/bin/activate          # en fish: source .venv/bin/activate.fish
pip install requests pandas
pip freeze > requirements.txt      # guardar versiones exactas
pip install -r requirements.txt    # reinstalar en otra máquina
deactivate
```

```bash
# Con uv (moderno y 10-100x más rápido)
uv init mi-proyecto && cd mi-proyecto   # crea pyproject.toml
uv add requests pandas                  # instala y anota en pyproject.toml
uv add --dev pytest                     # dependencia solo de desarrollo
uv run main.py                          # ejecuta dentro del entorno (lo crea solo)
uv sync                                 # instala todo lo del pyproject/uv.lock
uv python install 3.12                  # instala otra versión de Python
uvx ruff check .                        # ejecuta una herramienta sin instalarla
```

- `pip list` :: Paquetes instalados en el entorno activo
- `pip show requests` :: Versión y dependencias de un paquete
- `pip install -U paquete` :: Actualizar
- `pip uninstall paquete` :: Desinstalar
- `which python` :: ¿Qué Python estoy usando? (debe ser el de .venv)
- `uv pip install -r requirements.txt` :: Usar uv como reemplazo directo de pip

💡 Consejo: añade `.venv/` a tu `.gitignore`. Lo que se sube a git es `requirements.txt` o `pyproject.toml` + `uv.lock`, nunca la carpeta.

⚠️ Cuidado: si VS Code no encuentra tus librerías, elige el intérprete del venv: Ctrl+Shift+P → "Python: Select Interpreter" → `.venv`.

🇬🇧 **virtual environment** /vérchual enváironment/ = entorno virtual · **dependency** /dipéndensi/ = dependencia · **install** /instól/ = instalar · **lock file** /lok fáil/ = archivo de versiones fijadas · **activate** /áktiveit/ = activar

## 📁 Archivos y pathlib

Para leer y escribir archivos se usa `open` dentro de un bloque `with`: cuando el bloque termina, el archivo se **cierra solo**, aunque haya un error. `pathlib` representa rutas como objetos y funciona igual en Linux y Windows.

| Modo | Significado |
|---|---|
| `"r"` | Leer (por defecto); error si no existe |
| `"w"` | Escribir; **borra** el contenido anterior |
| `"a"` | Añadir al final |
| `"x"` | Crear; error si ya existe |
| `"rb"` / `"wb"` | Binario (imágenes, PDFs) |

- `with open("datos.txt", encoding="utf-8") as f: texto = f.read()` :: Leer todo
- `for linea in f:` :: Leer línea a línea (ideal para archivos grandes)
- `f.readlines()` :: Lista de líneas (con el \n)
- `with open("salida.txt", "w", encoding="utf-8") as f: f.write("hola\n")` :: Escribir
- `print("texto", file=f)` :: Escribir con print a un archivo
- `from pathlib import Path` :: Importar pathlib
- `Path.home() / "Documentos" / "notas.txt"` :: Construir rutas con /
- `p.read_text(encoding="utf-8")` / `p.write_text(...)` :: Leer / escribir en una línea
- `p.exists(), p.is_file(), p.is_dir()` :: Comprobaciones
- `p.name, p.stem, p.suffix, p.parent` :: "notas.txt", "notas", ".txt", carpeta
- `p.mkdir(parents=True, exist_ok=True)` :: Crear carpeta (y padres)
- `list(Path(".").glob("*.py"))` :: Buscar archivos por patrón
- `Path(".").rglob("*.csv")` :: Buscar recursivamente en subcarpetas
- `p.rename(nuevo)`, `p.unlink()` :: Renombrar, borrar archivo
- `p.stat().st_size` :: Tamaño en bytes

### ✅ Ejemplo resuelto: organizar archivos por extensión

```python
from pathlib import Path
import tempfile

base = Path(tempfile.mkdtemp())
for nombre in ["foto1.jpg", "foto2.jpg", "tarea.pdf", "notas.txt", "LEEME"]:
    (base / nombre).write_text("contenido", encoding="utf-8")

for archivo in base.iterdir():
    if archivo.is_file():
        extension = archivo.suffix.lstrip(".").lower() or "sin_extension"
        destino = base / extension
        destino.mkdir(exist_ok=True)
        archivo.rename(destino / archivo.name)

for carpeta in sorted(p for p in base.iterdir() if p.is_dir()):
    print(carpeta.name, sorted(a.name for a in carpeta.iterdir()))
```

Qué hace cada parte: `tempfile.mkdtemp()` crea una carpeta temporal para probar sin riesgo; `write_text` crea archivos de ejemplo; `iterdir()` recorre la carpeta; `suffix` da la extensión (".jpg"), `lstrip(".")` le quita el punto y `or "sin_extension"` cubre archivos sin extensión; `rename` mueve el archivo a su carpeta.

```text
jpg ['foto1.jpg', 'foto2.jpg']
pdf ['tarea.pdf']
sin_extension ['LEEME']
txt ['notas.txt']
```

⚠️ Cuidado: pon siempre `encoding="utf-8"`. Sin él, en Windows las tildes y la ñ salen como "Ã±".

🇬🇧 **file** /fáil/ = archivo · **path** /paz/ = ruta · **folder / directory** /fóulder / dairéktori/ = carpeta · **read / write** /ríd / ráit/ = leer / escribir · **encoding** /enkóuding/ = codificación

## 🗂️ JSON y CSV

**JSON** es el formato estándar de las APIs web y de los archivos de configuración: se parece mucho a un dict de Python. **CSV** es una tabla en texto plano (como un Excel simple): cada línea es una fila y las columnas van separadas por comas.

| Python | JSON |
|---|---|
| `dict` | objeto `{}` |
| `list`, `tuple` | array `[]` |
| `str` | string `""` |
| `int`, `float` | number |
| `True` / `False` | `true` / `false` |
| `None` | `null` |

- `json.dumps(d, indent=2, ensure_ascii=False)` :: dict → texto JSON bonito (con tildes reales)
- `json.loads(texto)` :: texto JSON → dict
- `json.dump(d, f)` / `json.load(f)` :: Lo mismo pero con un archivo abierto
- `csv.reader(f)` / `csv.writer(f)` :: Filas como listas
- `csv.DictReader(f)` / `csv.DictWriter(f, fieldnames=[...])` :: Filas como dicts (usa los encabezados)
- `open("x.csv", newline="", encoding="utf-8")` :: Siempre newline="" con csv

### ✅ Ejemplo resuelto: CSV de notas → resumen en JSON

```python
import csv
import io
import json

texto_csv = """nombre,materia,nota
Ana,Cálculo,85
Luis,Cálculo,62
Ana,Física,91
Luis,Física,48
"""

resumen = {}
for fila in csv.DictReader(io.StringIO(texto_csv)):
    alumno = resumen.setdefault(fila["nombre"], {"notas": {}, "aprobadas": 0})
    nota = int(fila["nota"])
    alumno["notas"][fila["materia"]] = nota
    if nota >= 51:
        alumno["aprobadas"] += 1

print(json.dumps(resumen, indent=2, ensure_ascii=False))
```

Qué hace cada parte: `io.StringIO` hace que un string se comporte como archivo (en la vida real sería `open("notas.csv", newline="", encoding="utf-8")`); `DictReader` usa la primera línea como claves; los valores del CSV siempre llegan como **texto**, por eso `int(...)`; la nota mínima de aprobación en Bolivia suele ser 51; `ensure_ascii=False` deja "Cálculo" legible.

```text
{
  "Ana": {
    "notas": {
      "Cálculo": 85,
      "Física": 91
    },
    "aprobadas": 2
  },
  "Luis": {
    "notas": {
      "Cálculo": 62,
      "Física": 48
    },
    "aprobadas": 1
  }
}
```

⚠️ Cuidado: JSON usa comillas **dobles**. `{'a': 1}` no es JSON válido (es un dict de Python impreso).

🇬🇧 **parse** /pars/ = analizar (convertir texto en datos) · **serialize** /sírialais/ = serializar · **header** /jéder/ = encabezado · **comma-separated** /kóma séparéited/ = separado por comas · **field** /fíld/ = campo

## 🚑 Errores y excepciones

Cuando algo sale mal, Python **lanza una excepción**. Si nadie la captura, el programa se detiene y muestra un **traceback** (léelo de abajo hacia arriba: la última línea dice el error y la penúltima dónde ocurrió). Con `try/except` la atrapas y decides qué hacer.

```python
try:
    edad = int(input("Edad: "))
    print(100 / edad)
except ValueError:
    print("Eso no es un número")
except ZeroDivisionError:
    print("La edad no puede ser 0")
else:
    print("Todo salió bien")          # solo si NO hubo error
finally:
    print("Esto se ejecuta SIEMPRE")  # haya error o no
```

| Excepción | Cuándo ocurre |
|---|---|
| `ValueError` | Valor con el tipo correcto pero inválido: `int("hola")` |
| `TypeError` | Tipo equivocado: `"a" + 1` |
| `KeyError` | Clave que no existe en un dict |
| `IndexError` | Índice fuera de la lista |
| `AttributeError` | El objeto no tiene ese atributo/método: `None.upper()` |
| `NameError` | Variable no definida (o mal escrita) |
| `ZeroDivisionError` | División entre cero |
| `FileNotFoundError` | El archivo no existe |
| `ImportError` / `ModuleNotFoundError` | No se encuentra el módulo |
| `IndentationError` | Indentación mal hecha |

- `except (ValueError, TypeError) as e:` :: Capturar varias y guardar el error en e
- `raise ValueError("edad negativa")` :: Lanzar un error propio
- `raise` :: Dentro de except: relanza el mismo error
- `raise NuevoError("...") from e` :: Encadenar errores (conserva la causa)
- `class SaldoInsuficiente(Exception): pass` :: Excepción personalizada
- `assert x > 0, "x debe ser positivo"` :: Comprobación rápida (para depurar y tests)
- `import traceback; traceback.print_exc()` :: Imprimir el traceback sin detener el programa

### ✅ Ejemplo resuelto: cuenta bancaria con excepción propia

```python
class SaldoInsuficiente(Exception):
    def __init__(self, saldo, monto):
        super().__init__(f"Saldo {saldo} Bs. insuficiente para retirar {monto} Bs.")
        self.faltante = monto - saldo

def retirar(saldo, monto):
    if monto <= 0:
        raise ValueError("El monto debe ser positivo")
    if monto > saldo:
        raise SaldoInsuficiente(saldo, monto)
    return saldo - monto

for monto in [30, -5, 500]:
    try:
        print("Nuevo saldo:", retirar(100, monto))
    except SaldoInsuficiente as e:
        print("Error:", e, "| faltan", e.faltante)
    except ValueError as e:
        print("Error:", e)
```

Qué hace cada parte: `SaldoInsuficiente` hereda de `Exception` y guarda un dato extra (`faltante`); `super().__init__(mensaje)` define el texto del error; la función lanza errores distintos según el caso; el bucle captura cada tipo por separado.

```text
Nuevo saldo: 70
Error: El monto debe ser positivo
Error: Saldo 100 Bs. insuficiente para retirar 500 Bs. | faltan 400
```

⚠️ Cuidado: no uses `except:` a secas ni `except Exception: pass`: escondes TODOS los errores, incluso los bugs, y luego no sabrás qué pasa. Captura solo lo que sepas manejar.

💡 Consejo: en Python se prefiere "pedir perdón antes que permiso" (EAFP): intenta la operación con `try` en vez de comprobar todo antes con `if`.

🇬🇧 **exception** /eksépshon/ = excepción · **raise** /réis/ = lanzar · **catch** /kach/ = atrapar · **traceback** /tréis-bak/ = rastro del error · **bug** /bag/ = error de programación · **handle** /jándol/ = manejar

## 🏛️ POO: clases, herencia y dataclasses

La **Programación Orientada a Objetos** agrupa datos (**atributos**) y comportamiento (**métodos**) en una **clase**. La clase es el plano de una casa; cada **objeto** es una casa construida con ese plano. `self` es "este objeto en concreto".

```python
class Mascota:
    especie = "desconocida"            # atributo de CLASE (compartido)

    def __init__(self, nombre, edad):  # constructor
        self.nombre = nombre           # atributo de INSTANCIA
        self.edad = edad

    def hablar(self):
        return "..."

    def __str__(self):                 # cómo se ve con print()
        return f"{self.nombre} ({self.edad} años)"

class Perro(Mascota):                  # herencia
    especie = "perro"

    def __init__(self, nombre, edad, raza):
        super().__init__(nombre, edad) # reutiliza el constructor del padre
        self.raza = raza

    def hablar(self):                  # sobrescribe (polimorfismo)
        return "¡Guau!"
```

| Método especial | Se usa cuando... | Ejemplo |
|---|---|---|
| `__init__` | Creas el objeto | `Perro("Firulais", 3, "mestizo")` |
| `__str__` | `print(obj)` o `str(obj)` | Texto para usuarios |
| `__repr__` | Lo ves en la consola | Texto para programadores |
| `__len__` | `len(obj)` | Tamaño |
| `__eq__` / `__lt__` | `==` / `<` | Comparar objetos |
| `__add__` | `a + b` | Sumar objetos |
| `__getitem__` | `obj[i]` | Indexar |
| `__iter__` | `for x in obj` | Hacerlo recorrible |
| `__contains__` | `x in obj` | Pertenencia |
| `__call__` | `obj()` | Llamarlo como función |
| `__enter__` / `__exit__` | `with obj:` | Gestor de contexto |

- `@property` :: Método que se usa como atributo (`c.area` sin paréntesis)
- `@classmethod` :: Recibe la clase (cls): constructores alternativos
- `@staticmethod` :: Función normal guardada dentro de la clase
- `self._privado` :: Convención: "no lo toques desde afuera" (Python no lo impide)
- `isinstance(p, Mascota), issubclass(Perro, Mascota)` :: Comprobar tipo / herencia
- `from abc import ABC, abstractmethod` :: Clases abstractas (obligan a implementar métodos)

### 📐 dataclasses

Para clases que sobre todo **guardan datos**, `@dataclass` escribe por ti `__init__`, `__repr__` y `__eq__`.

### ✅ Ejemplo resuelto: vectores y productos con dataclass

```python
from dataclasses import dataclass, field

@dataclass
class Vector:
    x: float
    y: float

    def __add__(self, otro):
        return Vector(self.x + otro.x, self.y + otro.y)

    def __mul__(self, k):
        return Vector(self.x * k, self.y * k)

    @property
    def norma(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

@dataclass(order=True)
class Producto:
    precio: float
    nombre: str = field(compare=False)
    etiquetas: list[str] = field(default_factory=list, compare=False)

v = Vector(3, 4) + Vector(1, 2)
print(v, v * 2, Vector(3, 4).norma)

carrito = [Producto(12.5, "Queso"), Producto(3.0, "Pan", ["desayuno"]), Producto(8.0, "Leche")]
print(min(carrito).nombre, [p.nombre for p in sorted(carrito)])
print(Producto(3.0, "Pan") == Producto(3.0, "Marraqueta"))
```

Qué hace cada parte: `@dataclass` genera el constructor a partir de las anotaciones `x: float`; `__add__` y `__mul__` hacen que `+` y `*` funcionen con vectores; `@property` permite escribir `.norma` sin paréntesis; `order=True` genera `<`, `>` para ordenar; `field(compare=False)` excluye un campo de las comparaciones (solo cuenta el precio); `default_factory=list` da una lista nueva a cada objeto (nunca `= []`).

```text
Vector(x=4, y=6) Vector(x=8, y=12) 5.0
Pan ['Pan', 'Leche', 'Queso']
True
```

💡 Consejo: prefiere **composición** (un objeto tiene otro) a herencias profundas. Si dudas entre "es un" y "tiene un", casi siempre es "tiene un".

🇬🇧 **class** /klas/ = clase · **object / instance** /óbyekt / ínstans/ = objeto / instancia · **inheritance** /injéritans/ = herencia · **method** /mézod/ = método · **attribute** /átribiut/ = atributo · **constructor** /konstráktor/ = constructor

## 🔄 Iteradores y generadores

Un **iterable** es cualquier cosa que puedes recorrer con `for` (lista, string, archivo). Un **iterador** es el objeto que va entregando los elementos uno a uno con `next()` y "recuerda" por dónde va. Un **generador** es la forma fácil de crear iteradores: una función con `yield` en vez de `return`.

Analogía: una lista es una **bandeja** con todas las salteñas ya hechas (ocupa espacio); un generador es el **horno** que te da una salteña cada vez que pides (casi no ocupa memoria). Para millones de datos, el generador gana.

```python
xs = [10, 20, 30]
it = iter(xs)
print(next(it), next(it), next(it))   # 10 20 30
# next(it) otra vez -> StopIteration (el for la maneja solo)
```

- `yield valor` :: Entrega un valor y pausa la función hasta el próximo next()
- `yield from otro_iterable` :: Delegar en otro generador
- `(x * 2 for x in datos)` :: Expresión generadora (perezosa)
- `next(gen, None)` :: Siguiente valor, o None si se acabó
- `list(gen)` :: Consumir todo el generador en una lista
- `range(10**12)` :: range también es perezoso: no crea un billón de números

### ✅ Ejemplo resuelto: Fibonacci infinito y lectura por lotes

```python
from itertools import islice

def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

def por_lotes(iterable, tam):
    lote = []
    for x in iterable:
        lote.append(x)
        if len(lote) == tam:
            yield lote
            lote = []
    if lote:
        yield lote

print(list(islice(fibonacci(), 10)))
for lote in por_lotes(range(1, 8), 3):
    print("Procesando lote:", lote)
```

Qué hace cada parte: `fibonacci` tiene un `while True` pero NO se cuelga, porque `yield` pausa la función tras cada número; `islice(..., 10)` toma solo los 10 primeros; `por_lotes` agrupa elementos de a 3 (útil para enviar datos a una API o a una red neuronal por batches) y el `if lote` final entrega el resto incompleto.

```text
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
Procesando lote: [1, 2, 3]
Procesando lote: [4, 5, 6]
Procesando lote: [7]
```

⚠️ Cuidado: un generador se **agota**: después de recorrerlo una vez, un segundo `for` no da nada. Si lo necesitas dos veces, conviértelo a lista o créalo de nuevo.

🇬🇧 **iterator** /íteréitor/ = iterador · **generator** /yeneréitor/ = generador · **yield** /yíld/ = ceder (entregar) · **lazy** /léisi/ = perezoso (calcula solo cuando se pide) · **batch** /bach/ = lote

## 🎀 Decoradores

Un **decorador** es una función que **envuelve** a otra para añadirle comportamiento sin tocar su código: medir tiempo, registrar llamadas, reintentar, comprobar permisos, cachear. La sintaxis `@decorador` encima de una función es solo un atajo de `funcion = decorador(funcion)`.

Analogía: es como ponerle **funda** a tu celular: el celular sigue igual, pero ahora tiene protección extra.

```python
import functools

def mi_decorador(func):
    @functools.wraps(func)           # conserva nombre y docstring de func
    def envoltura(*args, **kwargs):
        # ... antes ...
        resultado = func(*args, **kwargs)
        # ... después ...
        return resultado
    return envoltura
```

- `@functools.cache` :: Memoriza resultados (memoización) sin escribir nada
- `@functools.lru_cache(maxsize=128)` :: Cache con tamaño máximo
- `@property, @staticmethod, @classmethod` :: Decoradores de clases que ya conoces
- `@app.get("/")` :: En FastAPI/Flask, los decoradores registran rutas

### ✅ Ejemplo resuelto: medir tiempo y reintentar

```python
import functools
import time

def cronometro(func):
    @functools.wraps(func)
    def envoltura(*args, **kwargs):
        inicio = time.perf_counter()
        resultado = func(*args, **kwargs)
        ms = (time.perf_counter() - inicio) * 1000
        print(f"{func.__name__} tardó {ms:.0f} ms")
        return resultado
    return envoltura

def reintentar(veces):
    def decorador(func):
        @functools.wraps(func)
        def envoltura(*args, **kwargs):
            for intento in range(1, veces + 1):
                try:
                    return func(*args, **kwargs)
                except ConnectionError as e:
                    print(f"Intento {intento} falló: {e}")
            raise RuntimeError("Se agotaron los intentos")
        return envoltura
    return decorador

@cronometro
def lento():
    time.sleep(0.2)
    return "listo"

llamadas = {"n": 0}

@reintentar(veces=3)
def conectar():
    llamadas["n"] += 1
    if llamadas["n"] < 3:
        raise ConnectionError("servidor ocupado")
    return "conectado"

print(lento())
print(conectar())

@functools.cache
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

print(fib(100))
```

Qué hace cada parte: `cronometro` mide el tiempo antes y después de llamar a la función original; `reintentar(veces=3)` es un decorador **con parámetros**, por eso tiene tres niveles (fábrica → decorador → envoltura); `conectar` falla dos veces a propósito y al tercer intento funciona; `@functools.cache` hace que `fib(100)` sea instantáneo en vez de tardar siglos.

```text
lento tardó 200 ms
listo
Intento 1 falló: servidor ocupado
Intento 2 falló: servidor ocupado
conectado
354224848179261915075
```

⚠️ Cuidado: sin `@functools.wraps`, la función decorada pierde su nombre (`envoltura` en vez de `lento`) y su docstring, y las herramientas de depuración se confunden.

🇬🇧 **decorator** /dékoreitor/ = decorador · **wrapper** /ráper/ = envoltura · **cache** /kash/ = memoria rápida · **retry** /ritrái/ = reintentar · **closure** /klóusher/ = cierre (función que recuerda variables de afuera)

## 📅 Fechas y horas

El módulo `datetime` maneja fechas (`date`), horas (`time`), ambas (`datetime`) y diferencias (`timedelta`). Para zonas horarias se usa `zoneinfo` (Bolivia es `America/La_Paz`, UTC-4, sin horario de verano).

- `from datetime import date, datetime, timedelta` :: Importar lo principal
- `datetime.now()`, `date.today()` :: Ahora / hoy
- `datetime(2026, 8, 6, 10, 30)` :: Fecha concreta (6 de agosto, 10:30)
- `d + timedelta(days=30, hours=2)` :: Sumar tiempo
- `(fecha2 - fecha1).days` :: Diferencia en días
- `d.year, d.month, d.day, d.weekday()` :: Partes (weekday: 0 = lunes)
- `d.strftime("%d/%m/%Y %H:%M")` :: Fecha → texto con formato
- `datetime.strptime("18/10/2026", "%d/%m/%Y")` :: Texto → fecha
- `d.isoformat()`, `datetime.fromisoformat(s)` :: Formato estándar ISO 8601 (para JSON y APIs)
- `from zoneinfo import ZoneInfo; datetime.now(ZoneInfo("America/La_Paz"))` :: Hora con zona horaria
- `datetime.now().timestamp()` :: Segundos desde 1970 (Unix time)

| Código | Significado | Ejemplo |
|---|---|---|
| `%Y` / `%y` | Año 4 / 2 dígitos | `2026` / `26` |
| `%m` | Mes 01-12 | `10` |
| `%d` | Día 01-31 | `18` |
| `%H` / `%I` | Hora 00-23 / 01-12 | `15` / `03` |
| `%M` / `%S` | Minutos / segundos | `07` / `59` |
| `%A` / `%a` | Día de la semana completo / corto | `Sunday` / `Sun` |
| `%B` / `%b` | Mes completo / corto | `October` / `Oct` |
| `%p` | AM / PM | `PM` |
| `%j` | Día del año | `291` |

### ✅ Ejemplo resuelto: ¿cuántos días faltan?

```python
from datetime import date, datetime, timedelta

hoy = date(2026, 10, 18)
examen = datetime.strptime("05/12/2026", "%d/%m/%Y").date()
faltan = (examen - hoy).days
dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]

print(f"Faltan {faltan} días para el examen ({dias[examen.weekday()]})")
print("Semanas completas:", faltan // 7)
print("Repaso empieza el:", (examen - timedelta(days=14)).strftime("%d/%m/%Y"))
```

Qué hace cada parte: fijamos "hoy" para que la salida sea reproducible (en la vida real `date.today()`); `strptime` convierte el texto en fecha y `.date()` descarta la hora; restar dos fechas da un `timedelta` con `.days`; `weekday()` da 0-6 y lo traducimos con una lista; restar 14 días da la fecha de inicio del repaso.

```text
Faltan 48 días para el examen (sábado)
Semanas completas: 6
Repaso empieza el: 21/11/2026
```

⚠️ Cuidado: no mezcles fechas con zona horaria ("aware") y sin zona ("naive"): restarlas da `TypeError`. En servidores guarda todo en UTC y convierte solo al mostrar.

🇬🇧 **date** /déit/ = fecha · **time zone** /táim sóun/ = zona horaria · **timestamp** /táim-stamp/ = marca de tiempo · **deadline** /déd-láin/ = fecha límite · **weekday** /uík-déi/ = día de la semana

## 🔎 Expresiones regulares (re)

Una **expresión regular** (regex) es un patrón para buscar texto: "un correo", "un número de 8 dígitos", "una fecha". Es como un buscador con superpoderes. Escribe los patrones con `r"..."` (string crudo) para que las barras `\` no se interpreten.

| Patrón | Significa | Ejemplo que coincide |
|---|---|---|
| `\d` / `\D` | Dígito / no dígito | `7` |
| `\w` / `\W` | Letra, dígito o _ / lo contrario | `a`, `Z`, `_` |
| `\s` / `\S` | Espacio en blanco / no espacio | ` ` |
| `.` | Cualquier carácter (menos \n) | `x` |
| `^` / `$` | Inicio / fin del texto | |
| `*` / `+` / `?` | 0 o más / 1 o más / 0 o 1 | `a+` → `aaa` |
| `{3}` / `{2,4}` | Exactamente 3 / entre 2 y 4 | `\d{3}` → `591` |
| `[abc]` / `[^abc]` | Uno de esos / ninguno de esos | `[aeiou]` |
| `[a-z0-9]` | Rango | `k`, `5` |
| `(...)` | Grupo (captura) | `(\d+)-(\d+)` |
| `(?P<nombre>...)` | Grupo con nombre | `(?P<anio>\d{4})` |
| `a\|b` | a o b | `gato\|perro` |
| `\b` | Borde de palabra | `\bsol\b` |

- `re.search(patron, texto)` :: Primera coincidencia en cualquier parte (o None)
- `re.match(patron, texto)` :: Solo si coincide AL INICIO
- `re.fullmatch(patron, texto)` :: Todo el texto debe coincidir (validar)
- `re.findall(patron, texto)` :: Lista con todas las coincidencias
- `re.finditer(patron, texto)` :: Iterador de objetos Match (con posiciones)
- `re.sub(patron, reemplazo, texto)` :: Buscar y reemplazar
- `re.split(r"[,;]\s*", texto)` :: Partir por varios separadores
- `m.group(0), m.group(1), m.groupdict()` :: Texto completo, grupo 1, grupos con nombre
- `re.compile(patron, re.IGNORECASE)` :: Compilar para reusar (y con banderas)

### ✅ Ejemplo resuelto: extraer datos de un mensaje

```python
import re

texto = """Contacto: ana.quispe@umsa.bo, cel 71234567.
Pedido #A-1024 del 15/10/2026 por Bs. 350.50; otro: luis_m@gmail.com, 69876543."""

correos = re.findall(r"[\w.]+@[\w.]+\.\w+", texto)
celulares = re.findall(r"\b[67]\d{7}\b", texto)
fecha = re.search(r"(?P<dia>\d{2})/(?P<mes>\d{2})/(?P<anio>\d{4})", texto)
monto = float(re.search(r"Bs\. (\d+\.\d{2})", texto).group(1))
censurado = re.sub(r"\b([67]\d)\d{4}(\d{2})\b", r"\1****\2", texto.splitlines()[0])

print(correos)
print(celulares)
print(fecha.groupdict(), monto)
print(censurado)
print(bool(re.fullmatch(r"[A-Z]-\d{4}", "A-1024")))
```

Qué hace cada parte: `[\w.]+@[\w.]+\.\w+` busca "letras/puntos @ dominio . terminación"; `\b[67]\d{7}\b` son 8 dígitos empezando por 6 o 7 (celulares de Bolivia) con bordes de palabra para no cortar números más largos; los grupos con nombre permiten `groupdict()`; `\.` es un punto literal; en `re.sub`, `\1` y `\2` reinsertan los grupos capturados para ocultar el centro del número.

```text
['ana.quispe@umsa.bo', 'luis_m@gmail.com']
['71234567', '69876543']
{'dia': '15', 'mes': '10', 'anio': '2026'} 350.5
Contacto: ana.quispe@umsa.bo, cel 71****67.
True
```

⚠️ Cuidado: `.` significa "cualquier carácter". Para un punto de verdad escribe `\.`. Y `*` es codicioso: `<.*>` en `<a><b>` toma todo; usa `<.*?>` para lo mínimo.

💡 Consejo: prueba tus patrones en regex101.com (elige "Python"); explica cada parte del patrón en inglés.

🇬🇧 **regular expression** /réguiular ekspréshon/ = expresión regular · **pattern** /pátern/ = patrón · **match** /mach/ = coincidencia · **greedy** /grídi/ = codicioso · **escape** /eskéip/ = escapar (quitar el significado especial)

## 🌍 requests y APIs

Una **API web** es un servicio al que tu programa le hace preguntas por HTTP y que responde (casi siempre) en JSON. La librería `requests` (`pip install requests`) es la forma más cómoda de hablar con ellas.

| Método HTTP | Para qué | Ejemplo |
|---|---|---|
| `GET` | Leer datos | `requests.get(url)` |
| `POST` | Crear | `requests.post(url, json=datos)` |
| `PUT` / `PATCH` | Reemplazar / modificar | `requests.patch(url, json={...})` |
| `DELETE` | Borrar | `requests.delete(url)` |

| Código | Significado |
|---|---|
| `200` OK / `201` Created | Todo bien / creado |
| `400` Bad Request | Pediste algo mal formado |
| `401` / `403` | Sin autenticar / sin permiso |
| `404` Not Found | No existe |
| `429` Too Many Requests | Demasiadas peticiones: espera |
| `500` | Error del servidor (no es tu culpa) |

- `r = requests.get(url, params={"q": "python"}, timeout=10)` :: GET con parámetros (?q=python) y tiempo límite
- `r.status_code, r.ok` :: Código numérico / True si es 2xx
- `r.json()` :: Respuesta JSON → dict o lista
- `r.text, r.content` :: Respuesta como texto / bytes (imágenes)
- `r.raise_for_status()` :: Lanza excepción si fue un error 4xx/5xx
- `headers={"Authorization": f"Bearer {token}"}` :: Enviar un token
- `requests.Session()` :: Reutiliza la conexión (más rápido en muchas peticiones)
- `import httpx` :: Alternativa moderna con soporte async

### ✅ Ejemplo resuelto: consumir una API pública

```python
import requests

URL = "https://jsonplaceholder.typicode.com"

def tareas_de_usuario(user_id):
    r = requests.get(f"{URL}/todos", params={"userId": user_id}, timeout=10)
    r.raise_for_status()
    return r.json()

try:
    tareas = tareas_de_usuario(1)
    hechas = [t for t in tareas if t["completed"]]
    print(f"Usuario 1: {len(tareas)} tareas, {len(hechas)} completadas")
    print("Primera:", tareas[0]["title"])

    nueva = requests.post(f"{URL}/posts", json={"title": "Hola", "body": "Desde Bolivia", "userId": 1}, timeout=10)
    print(nueva.status_code, nueva.json())
except requests.RequestException as e:
    print("Problema de red:", e)
```

Qué hace cada parte: JSONPlaceholder es una API falsa gratuita para practicar; `params` arma la URL `.../todos?userId=1`; `timeout=10` evita que el programa se quede colgado para siempre; `raise_for_status()` convierte un 404 o 500 en excepción; el `json=` del POST convierte el dict a JSON y pone la cabecera adecuada; `RequestException` agrupa todos los errores de red.

```text
Usuario 1: 20 tareas, 11 completadas
Primera: delectus aut autem
201 {'title': 'Hola', 'body': 'Desde Bolivia', 'userId': 1, 'id': 101}
```

⚠️ Cuidado: pon SIEMPRE `timeout`. Sin él, si el servidor no responde, tu programa espera para siempre.

⚠️ Cuidado: nunca escribas tu API key en el código que subes a GitHub. Guárdala en una variable de entorno y léela con `os.environ["API_KEY"]`.

🇬🇧 **request / response** /rikuést / rispóns/ = petición / respuesta · **endpoint** /énd-póint/ = punto de acceso (URL de la API) · **header** /jéder/ = cabecera · **payload** /péi-loud/ = carga (datos enviados) · **rate limit** /réit límit/ = límite de peticiones

## 🪄 Programación funcional, collections e itertools

La programación funcional trata las funciones como datos: las pasas a otras funciones (`map`, `filter`, `sorted`) en vez de escribir bucles. La clave más útil en la práctica es el parámetro **`key=`**: le dices a `sorted`, `max` o `min` **por qué** comparar.

- `sorted(xs, key=len)` :: Ordenar por longitud
- `sorted(gente, key=lambda p: (-p["edad"], p["nombre"]))` :: Por edad descendente y luego nombre
- `max(productos, key=lambda p: p.precio)` :: El más caro (devuelve el objeto, no el precio)
- `list(map(str.upper, palabras))` :: Aplicar una función a cada elemento
- `list(filter(lambda x: x > 0, xs))` :: Quedarse con los que cumplen
- `functools.reduce(lambda a, b: a * b, xs)` :: Reducir a un valor (producto total)
- `from operator import itemgetter, attrgetter` :: `key=itemgetter("edad")` en vez de lambda
- `any(x < 0 for x in xs), all(...)` :: ¿Alguno cumple? / ¿Todos cumplen?
- `functools.partial(pow, exp=2)` :: Fijar argumentos de una función

### 🧺 collections

| Clase | Qué es | Ejemplo |
|---|---|---|
| `Counter` | Contador de elementos | `Counter("banana").most_common(1)` → `[('a', 3)]` |
| `defaultdict` | Dict que crea valores solos | `defaultdict(list)` |
| `deque` | Cola rápida por ambos lados | `deque(maxlen=3)` |
| `namedtuple` | Tupla con nombres | `Punto = namedtuple("Punto", "x y")` |
| `OrderedDict` | Dict con operaciones de orden (move_to_end) | Caché LRU manual |
| `ChainMap` | Busca en varios dicts en cadena | Configuración por capas |

### ♾️ itertools

| Función | Qué hace | Ejemplo → resultado |
|---|---|---|
| `count(10)` | 10, 11, 12... infinito | IDs consecutivos |
| `cycle("AB")` | A, B, A, B... | Turnos |
| `chain(a, b)` | Une iterables | `chain([1], [2, 3])` → 1, 2, 3 |
| `islice(it, 5)` | Toma 5 elementos | De un generador infinito |
| `product("ab", repeat=2)` | Producto cartesiano | aa, ab, ba, bb |
| `permutations("abc", 2)` | Permutaciones | ab, ac, ba, ... |
| `combinations("abcd", 2)` | Combinaciones sin orden | ab, ac, ad, bc, ... |
| `groupby(datos, key)` | Agrupa consecutivos iguales | Ordena antes por la misma key |
| `accumulate([1, 2, 3])` | Sumas acumuladas | 1, 3, 6 |
| `pairwise([1, 2, 3])` | Pares consecutivos | (1, 2), (2, 3) |
| `zip_longest(a, b)` | zip sin cortar en el más corto | Rellena con None |

### ✅ Ejemplo resuelto: ranking, agrupación y combinaciones

```python
from collections import Counter, defaultdict, deque
from itertools import combinations, accumulate, groupby
from operator import itemgetter

ventas = [
    {"vendedor": "Ana", "ciudad": "La Paz", "monto": 300},
    {"vendedor": "Luis", "ciudad": "Santa Cruz", "monto": 450},
    {"vendedor": "Ana", "ciudad": "La Paz", "monto": 200},
    {"vendedor": "Sofía", "ciudad": "Santa Cruz", "monto": 150},
]

por_vendedor = defaultdict(int)
for v in ventas:
    por_vendedor[v["vendedor"]] += v["monto"]
ranking = sorted(por_vendedor.items(), key=itemgetter(1), reverse=True)
print("Ranking:", ranking)

print("Ventas por ciudad:", Counter(v["ciudad"] for v in ventas))

ordenadas = sorted(ventas, key=itemgetter("ciudad"))
for ciudad, grupo in groupby(ordenadas, key=itemgetter("ciudad")):
    print(ciudad, "->", sum(v["monto"] for v in grupo))

print("Parejas posibles:", list(combinations(sorted(por_vendedor), 2)))
print("Acumulado:", list(accumulate(v["monto"] for v in ventas)))

ultimas = deque(maxlen=2)
for v in ventas:
    ultimas.append(v["monto"])
print("Últimas 2:", list(ultimas))
```

Qué hace cada parte: `defaultdict(int)` empieza cada vendedor en 0 sin `if`; `itemgetter(1)` ordena los pares por el total; `Counter` cuenta cuántas ventas hubo por ciudad; `groupby` agrupa elementos **consecutivos**, por eso primero se ordena por ciudad; `combinations` arma todas las parejas posibles de vendedores; `accumulate` da el total corriendo; `deque(maxlen=2)` descarta solo los más viejos.

```text
Ranking: [('Ana', 500), ('Luis', 450), ('Sofía', 150)]
Ventas por ciudad: Counter({'La Paz': 2, 'Santa Cruz': 2})
La Paz -> 500
Santa Cruz -> 600
Parejas posibles: [('Ana', 'Luis'), ('Ana', 'Sofía'), ('Luis', 'Sofía')]
Acumulado: [300, 750, 950, 1100]
Últimas 2: [200, 150]
```

⚠️ Cuidado: `map` y `filter` devuelven iteradores, no listas: `print(map(...))` muestra `<map object>`. Envuélvelos con `list(...)` o usa comprehensions.

🇬🇧 **higher-order function** /jáier órder fánkshon/ = función de orden superior · **key** /kí/ = clave (criterio) · **counter** /káunter/ = contador · **queue** /kiú/ = cola · **accumulate** /akiúmiuleit/ = acumular

## ✅ Testing con pytest

Un **test** es código que comprueba que tu código hace lo que dices. Con tests puedes cambiar cosas sin miedo: si rompes algo, el test te avisa. `pytest` (`uv add --dev pytest`) busca archivos `test_*.py`, ejecuta las funciones `test_*` y revisa los `assert`.

Analogía: los tests son la **red de seguridad del trapecista**: no te impiden caer, pero evitan que la caída sea fatal.

```python
# calculadora.py
def dividir(a, b):
    if b == 0:
        raise ValueError("No se puede dividir entre cero")
    return a / b

def es_aprobado(nota):
    return nota >= 51
```

```python
# test_calculadora.py
import pytest
from calculadora import dividir, es_aprobado

def test_dividir_normal():
    assert dividir(10, 4) == 2.5

def test_dividir_entre_cero():
    with pytest.raises(ValueError, match="cero"):
        dividir(1, 0)

@pytest.mark.parametrize("nota, esperado", [(51, True), (50, False), (100, True), (0, False)])
def test_es_aprobado(nota, esperado):
    assert es_aprobado(nota) == esperado

@pytest.fixture
def alumnos():
    return [{"nombre": "Ana", "nota": 80}, {"nombre": "Luis", "nota": 40}]

def test_cuantos_aprueban(alumnos):
    assert sum(es_aprobado(a["nota"]) for a in alumnos) == 1
```

```text
$ pytest -v
test_calculadora.py::test_dividir_normal PASSED
test_calculadora.py::test_dividir_entre_cero PASSED
test_calculadora.py::test_es_aprobado[51-True] PASSED
test_calculadora.py::test_es_aprobado[50-False] PASSED
test_calculadora.py::test_es_aprobado[100-True] PASSED
test_calculadora.py::test_es_aprobado[0-False] PASSED
test_calculadora.py::test_cuantos_aprueban PASSED
========== 7 passed in 0.02s ==========
```

- `pytest` :: Ejecutar todos los tests
- `pytest -v` :: Modo detallado (un renglón por test)
- `pytest -k aprobado` :: Solo los tests cuyo nombre contiene "aprobado"
- `pytest -x` :: Parar en el primer fallo
- `pytest --lf` :: Repetir solo los que fallaron la última vez
- `pytest -s` :: Mostrar los print
- `pytest.approx(0.3)` :: Comparar floats: `assert 0.1 + 0.2 == pytest.approx(0.3)`
- `tmp_path` :: Fixture integrada: carpeta temporal para tests con archivos
- `monkeypatch` :: Fixture para reemplazar funciones o variables de entorno en un test
- `pytest --cov=mi_paquete` :: Cobertura (con pytest-cov): qué líneas probaste

💡 Consejo: sigue el patrón **AAA**: Arrange (preparar datos), Act (ejecutar), Assert (comprobar). Un test = una idea.

⚠️ Cuidado: nombra los archivos `test_algo.py` y las funciones `test_algo()`; si no, pytest no los encuentra y dice "no tests ran".

🇬🇧 **test** /test/ = prueba · **assert** /asért/ = afirmar · **fixture** /fíkscher/ = preparación reutilizable · **pass / fail** /pas / féil/ = pasar / fallar · **coverage** /kóverech/ = cobertura · **edge case** /ech kéis/ = caso límite

## 🤖 Python para IA y ciencia de datos

Tres librerías forman la base de todo: **NumPy** (arrays numéricos rapidísimos, escritos en C), **pandas** (tablas tipo Excel: DataFrames) y **matplotlib** (gráficos). Encima de ellas se construyen scikit-learn, PyTorch y compañía. Instalar: `uv add numpy pandas matplotlib`.

### 🔢 NumPy

La idea clave es la **vectorización**: operas sobre el array entero de golpe, sin bucles. `a * 2` multiplica millones de números en milisegundos.

- `import numpy as np` :: Convención universal
- `np.array([1, 2, 3])` :: Crear un array
- `np.zeros((2, 3)), np.ones(5), np.eye(3)` :: Ceros, unos, identidad
- `np.arange(0, 10, 2), np.linspace(0, 1, 5)` :: Rango con paso / n puntos equiespaciados
- `a.shape, a.ndim, a.dtype` :: Forma, dimensiones, tipo
- `a.reshape(3, 2)` :: Cambiar la forma
- `a[a > 2]` :: Filtrado booleano (máscara)
- `a.mean(), a.std(), a.sum(axis=0)` :: Estadísticas (axis=0 por columnas)
- `A @ B` :: Producto de matrices
- `np.random.default_rng(42).normal(0, 1, 100)` :: 100 números normales con semilla fija

```python
import numpy as np

notas = np.array([[85, 70, 92], [60, 45, 75], [95, 88, 90]])   # 3 alumnos x 3 materias
print(notas.mean(axis=1))          # promedio de cada alumno: ≈ [82.33, 60, 91]
print(notas.max(axis=0))           # mejor nota por materia:  [95 88 92]
print((notas >= 51).all(axis=1))   # ¿aprobó todo?:           [ True False  True]
print(notas * 1.1)                 # broadcasting: subir 10% a todos
```

### 🐼 pandas

Un **DataFrame** es una tabla con columnas con nombre; cada columna es una **Series**. Piensa en una hoja de Excel que puedes manipular con código.

| Operación | Código |
|---|---|
| Leer CSV / Excel | `pd.read_csv("datos.csv")`, `pd.read_excel("x.xlsx")` |
| Primeras filas / info | `df.head()`, `df.info()`, `df.describe()` |
| Elegir columnas | `df["nota"]`, `df[["nombre", "nota"]]` |
| Filtrar filas | `df[df["nota"] >= 51]` |
| Varias condiciones | `df[(df["nota"] > 80) & (df["ciudad"] == "La Paz")]` |
| Por posición / etiqueta | `df.iloc[0]`, `df.loc[3, "nota"]` |
| Nueva columna | `df["aprobado"] = df["nota"] >= 51` |
| Agrupar | `df.groupby("ciudad")["nota"].mean()` |
| Ordenar | `df.sort_values("nota", ascending=False)` |
| Valores nulos | `df.isna().sum()`, `df.dropna()`, `df.fillna(0)` |
| Contar valores | `df["ciudad"].value_counts()` |
| Unir tablas | `pd.merge(a, b, on="id", how="left")` |
| Guardar | `df.to_csv("salida.csv", index=False)` |

### 📈 matplotlib

```python
import matplotlib.pyplot as plt

meses = ["Ene", "Feb", "Mar", "Abr"]
ventas = [120, 150, 90, 200]

fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(meses, ventas, marker="o", label="2026")
ax.set_title("Ventas mensuales")
ax.set_xlabel("Mes")
ax.set_ylabel("Bs.")
ax.legend()
ax.grid(alpha=0.3)
fig.savefig("ventas.png", dpi=150, bbox_inches="tight")   # o plt.show()
```

- `ax.bar(x, y)`, `ax.hist(datos, bins=20)`, `ax.scatter(x, y)` :: Barras, histograma, dispersión
- `df.plot(kind="bar", x="ciudad", y="nota")` :: pandas grafica directamente con matplotlib
- `fig, axs = plt.subplots(1, 2)` :: Dos gráficos lado a lado

### ✅ Ejemplo resuelto: análisis de un CSV con pandas

```python
import io
import pandas as pd

csv = """alumno,ciudad,materia,nota
Ana,La Paz,Cálculo,85
Luis,Cochabamba,Cálculo,45
Sofía,Santa Cruz,Cálculo,92
Ana,La Paz,Física,78
Luis,Cochabamba,Física,58
Sofía,Santa Cruz,Física,
Pedro,La Paz,Cálculo,50
"""

df = pd.read_csv(io.StringIO(csv))
print("Filas:", len(df), "| nulos en nota:", df["nota"].isna().sum())

df = df.dropna(subset=["nota"])
df["aprobado"] = df["nota"] >= 51

print(df.groupby("materia")["nota"].agg(["mean", "max", "count"]).round(1))
print(df.groupby("ciudad")["aprobado"].mean().mul(100).round(0).sort_values(ascending=False))
mejor = df.loc[df["nota"].idxmax()]
print("Mejor nota:", mejor["alumno"], mejor["materia"], mejor["nota"])
```

Qué hace cada parte: `read_csv` lee la tabla (aquí desde texto; normalmente un archivo); la nota vacía de Sofía en Física se lee como `NaN` (nulo); `dropna(subset=...)` quita esa fila; la nueva columna `aprobado` es True/False; `groupby(...).agg([...])` calcula varias estadísticas por materia; el promedio de una columna booleana es el **porcentaje** de True; `idxmax()` da el índice de la mejor nota y `loc` trae esa fila.

```text
Filas: 7 | nulos en nota: 1
         mean   max  count
materia                   
Cálculo  68.0  92.0      4
Física   68.0  78.0      2
ciudad
Santa Cruz    100.0
La Paz         67.0
Cochabamba     50.0
Name: aprobado, dtype: float64
Mejor nota: Sofía Cálculo 92.0
```

⚠️ Cuidado: en pandas las condiciones se combinan con `&`, `|`, `~` y **paréntesis**, nunca con `and`/`or`: `df[(df.a > 1) & (df.b < 5)]`.

⚠️ Cuidado: el aviso `SettingWithCopyWarning` aparece al modificar un filtro. Usa `df.loc[filtro, "col"] = valor` o haz `.copy()` del filtro.

💡 Consejo: para explorar datos usa Jupyter (`uv add --dev jupyterlab` y `uv run jupyter lab`): ves tablas y gráficos celda a celda.

🇬🇧 **array** /aréi/ = arreglo · **DataFrame** /déita-fréim/ = tabla de datos · **missing values** /mísing váliuz/ = valores faltantes · **plot** /plot/ = gráfico · **mean / median** /mín / mídian/ = media / mediana · **dataset** /déita-set/ = conjunto de datos

## 🧼 Buenas prácticas (PEP 8 y estilo pythónico)

**PEP 8** es la guía de estilo oficial de Python. El código se lee muchas más veces de las que se escribe, así que la legibilidad es lo primero. Escribe `import this` en Python para leer "El Zen de Python".

| Cosa | Estilo | Ejemplo |
|---|---|---|
| Variables y funciones | `snake_case` | `total_ventas`, `calcular_promedio()` |
| Clases | `PascalCase` | `GestorTareas` |
| Constantes | `MAYUSCULAS` | `NOTA_MINIMA = 51` |
| "Privado" | `_guion_bajo` | `_cache` |
| Indentación | 4 espacios | nunca tabs |
| Largo de línea | 79-99 caracteres | parte con paréntesis |
| Imports | arriba: estándar, terceros, propios | un grupo por bloque |
| Espacios | `x = 1`, `f(a, b)` | sin espacios en `f(a=1)` |

| ❌ Menos pythónico | ✅ Pythónico |
|---|---|
| `for i in range(len(xs)): print(xs[i])` | `for x in xs: print(x)` |
| `if len(xs) == 0:` | `if not xs:` |
| `if x == True:` | `if x:` |
| `if x == None:` | `if x is None:` |
| `f = open(...); ...; f.close()` | `with open(...) as f:` |
| `s = s + palabra` en bucle | `"".join(palabras)` |
| `d.has_key(k)` o try/except KeyError | `d.get(k, defecto)` |
| `tmp = a; a = b; b = tmp` | `a, b = b, a` |

- `uvx ruff check . --fix` :: Linter rapidísimo: detecta y arregla problemas de estilo
- `uvx ruff format .` :: Formatea el código automáticamente (como black)
- `uvx mypy .` :: Comprueba los type hints
- `import logging; logging.basicConfig(level=logging.INFO)` :: Usa logging en vez de print en programas serios
- `breakpoint()` :: Pausa el programa y abre el depurador (pdb) en esa línea

💡 Consejo: nombres que expliquen: `dias_hasta_examen` es mejor que `d` o `x2`. Si necesitas un comentario para explicar qué es una variable, cámbiale el nombre.

💡 Consejo: funciones pequeñas que hagan UNA cosa. Si una función pasa de unas 30 líneas o tiene "y" en su descripción, pártela.

🇬🇧 **readability** /ridabíliti/ = legibilidad · **style guide** /stáil gáid/ = guía de estilo · **linter** /línter/ = revisor de estilo · **refactor** /rifáktor/ = reorganizar el código · **pythonic** /paizónik/ = al estilo Python

## 🏆 Ejemplos resueltos completos

### ✅ Ejemplo resuelto: contador de palabras

```python
import re
from collections import Counter

texto = """La programación en Python es divertida. Python es claro,
y con Python la ciencia de datos es accesible. ¡Programar es crear!"""

VACIAS = {"la", "el", "en", "es", "y", "con", "de", "los", "las"}

palabras = re.findall(r"[a-záéíóúñü]+", texto.lower())
utiles = [p for p in palabras if p not in VACIAS]
conteo = Counter(utiles)

print("Total de palabras:", len(palabras))
print("Palabras distintas:", len(set(palabras)))
print("Top 3:", conteo.most_common(3))
for palabra, n in conteo.most_common(3):
    print(f"{palabra:<12} {'█' * n} {n}")
```

Qué hace cada parte: `lower()` unifica mayúsculas; la regex toma solo secuencias de letras (incluidas tildes y ñ), así los signos de puntuación desaparecen; las "palabras vacías" (stopwords) se filtran porque no aportan significado; `Counter.most_common(3)` da las 3 más frecuentes; `'█' * n` dibuja una barra de texto.

```text
Total de palabras: 21
Palabras distintas: 15
Top 3: [('python', 3), ('programación', 1), ('divertida', 1)]
python       ███ 3
programación █ 1
divertida    █ 1
```

### ✅ Ejemplo resuelto: gestor de tareas con JSON

```python
import json
import tempfile
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class Tarea:
    id: int
    titulo: str
    hecha: bool = False

class GestorTareas:
    def __init__(self, archivo: Path):
        self.archivo = archivo
        self.tareas: list[Tarea] = []
        if archivo.exists():
            datos = json.loads(archivo.read_text(encoding="utf-8"))
            self.tareas = [Tarea(**d) for d in datos]

    def guardar(self):
        datos = [asdict(t) for t in self.tareas]
        self.archivo.write_text(json.dumps(datos, indent=2, ensure_ascii=False), encoding="utf-8")

    def agregar(self, titulo: str) -> Tarea:
        nuevo_id = max((t.id for t in self.tareas), default=0) + 1
        tarea = Tarea(nuevo_id, titulo)
        self.tareas.append(tarea)
        self.guardar()
        return tarea

    def completar(self, id_: int):
        for t in self.tareas:
            if t.id == id_:
                t.hecha = True
                self.guardar()
                return
        raise KeyError(f"No existe la tarea {id_}")

    def listar(self):
        for t in self.tareas:
            print(f"[{'x' if t.hecha else ' '}] {t.id}. {t.titulo}")

ruta = Path(tempfile.mkdtemp()) / "tareas.json"
g = GestorTareas(ruta)
g.agregar("Estudiar SQL")
g.agregar("Practicar Docker")
g.agregar("Leer sobre redes neuronales")
g.completar(2)
g.listar()

g2 = GestorTareas(ruta)
print("Recargadas desde el archivo:", len(g2.tareas), "| pendientes:", sum(not t.hecha for t in g2.tareas))
```

Qué hace cada parte: `Tarea` es una dataclass (datos puros); `asdict` la convierte a dict para guardarla en JSON y `Tarea(**d)` hace lo contrario; `max(..., default=0) + 1` genera el siguiente id aunque la lista esté vacía; cada cambio llama a `guardar()` para no perder datos; `g2` se crea desde el mismo archivo para demostrar que las tareas persisten.

```text
[ ] 1. Estudiar SQL
[x] 2. Practicar Docker
[ ] 3. Leer sobre redes neuronales
Recargadas desde el archivo: 3 | pendientes: 2
```

💡 Consejo: para convertirlo en programa de terminal, añade `argparse` con subcomandos (`agregar`, `completar`, `listar`) y una ruta fija como `Path.home() / ".tareas.json"`.

📌 Los otros dos ejemplos completos pedidos están en sus secciones: "consumir una API pública" en 🌍 requests y APIs, y "análisis de un CSV con pandas" en 🤖 Python para IA.

🇬🇧 **word count** /uórd káunt/ = conteo de palabras · **stopwords** /stóp-uords/ = palabras vacías · **to-do list** /tu-dú list/ = lista de tareas · **persist** /persíst/ = persistir (guardar) · **load / save** /lóud / séiv/ = cargar / guardar
