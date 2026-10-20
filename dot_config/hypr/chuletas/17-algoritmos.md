# 🧮 Algoritmos · Estructuras de datos
> Big O, estructuras (arrays, hash, árboles, heaps, grafos), técnicas (DP, greedy, backtracking) y el método para entrevistas, en Python.

## 🧮 Qué es un algoritmo y por qué importa la eficiencia

🧠 Concepto: un **algoritmo** es una secuencia finita de pasos precisos que transforma una entrada en una salida y siempre termina. Una **estructura de datos** es una forma de organizar datos en memoria para que ciertas operaciones (buscar, insertar, borrar) sean rápidas.

La idea clave: **el mismo problema se puede resolver con algoritmos muy distintos**, y la diferencia no es de 2× sino de "1 segundo" contra "3 horas" o "más que la edad del universo". Con 10 datos todo es rápido; con 10 millones (usuarios, filas, píxeles, tokens) la elección del algoritmo decide si tu programa funciona o no. Un PC más rápido no te salva: un algoritmo cuadrático en un PC 10× más rápido solo procesa ~3× más datos en el mismo tiempo.

```flujo
Problema -> Entrada : define
Entrada -> Algoritmo : pasos
Estructura -> Algoritmo : organiza datos
Algoritmo -> Salida : resultado
Algoritmo -> Coste : tiempo + memoria
```

Analogía: buscar una palabra en el diccionario. **Algoritmo 1**: leer página por página desde la A (búsqueda lineal). **Algoritmo 2**: abrir por la mitad, ver si la palabra está antes o después, y repetir con esa mitad (búsqueda binaria). Para un diccionario de 1 000 000 de palabras, el primero hace hasta 1 000 000 de comparaciones; el segundo, unas **20**. Esa es la diferencia entre O(n) y O(log n), y funciona porque el diccionario está **ordenado** (la estructura de datos importa).

```python
import time

datos = list(range(10_000_000))          # 10 millones de números ordenados
objetivo = 9_999_999

# 1) Búsqueda lineal: recorre uno por uno
t0 = time.perf_counter()
pos = -1
for i, x in enumerate(datos):
    if x == objetivo:
        pos = i
        break
t_lineal = time.perf_counter() - t0

# 2) Búsqueda binaria (bisect): parte a la mitad cada vez
import bisect
t0 = time.perf_counter()
pos2 = bisect.bisect_left(datos, objetivo)
t_binaria = time.perf_counter() - t0

print(pos, pos2)
print(f"lineal:  {t_lineal:.4f} s")
print(f"binaria: {t_binaria:.6f} s")
# Salida en mi PC (varía según la máquina):
# 9999999 9999999
# lineal:  0.8 s aprox.
# binaria: 0.00001 s aprox.  → decenas de miles de veces más rápida
```

| Propiedad | Qué significa |
|---|---|
| Correcto | Da la salida correcta para TODA entrada válida |
| Finito | Termina en un número finito de pasos |
| Definido | Cada paso es preciso, sin ambigüedad |
| Eficiente | Usa poco tiempo y poca memoria |

💡 Consejo: piensa siempre en **dos preguntas**: ¿es correcto? (casos borde: vacío, un elemento, repetidos, negativos) y ¿cómo escala? (qué pasa si n se multiplica por 1000).

### 🌍 Dónde vive esto en el mundo real

| Sistema real | Estructura / algoritmo |
|---|---|
| `dict` y `set` de Python, `Map` de JS | Tablas hash |
| Índices de PostgreSQL / MySQL (InnoDB) | Árbol B / B+ |
| `list.sort()` de Python, `Array.prototype.sort` en V8 | Timsort (y variantes) |
| Protocolo de enrutamiento OSPF | Dijkstra (camino más corto) |
| Git: historial de commits | Grafo dirigido acíclico (DAG) |
| Redis: sorted sets (`ZADD`) | Skip list + hash |
| Planificadores de tareas, `heapq` | Heap (montículo) |
| Autocompletado, enrutadores IP | Tries / árboles de prefijos |
| Compresión ZIP/gzip (DEFLATE) | Códigos de Huffman (greedy) |
| `diff` de Git, correctores ortográficos | Programación dinámica (LCS, edición) |

🇬🇧 **algorithm** /álgorizm/ = algoritmo · **data structure** /déita strákcher/ = estructura de datos · **input / output** = entrada / salida · **edge case** /edch kéis/ = caso borde · **scalable** /skéilabol/ = escalable

## 📈 Notación Big O

🧠 Concepto: **Big O** (O grande) describe cómo **crece** el número de operaciones (o la memoria) de un algoritmo cuando crece el tamaño de la entrada `n`, en el **peor caso**, ignorando constantes y términos pequeños. No mide segundos: mide la **forma de la curva**.

¿Por qué ignorar constantes? Porque 3n y 100n crecen igual (en línea recta) y la diferencia la decide la máquina, el lenguaje, la caché... En cambio n² contra n es una diferencia que **ningún hardware compensa** cuando n es grande.

Reglas para simplificar:
1. Quita constantes multiplicativas: `O(3n + 5)` → `O(n)`.
2. Quédate con el término dominante: `O(n² + n + 1000)` → `O(n²)`.
3. Variables distintas se mantienen: dos listas de tamaños `a` y `b` recorridas una dentro de otra → `O(a·b)`, no `O(n²)`.
4. La base del logaritmo no importa: `log₂ n` y `log₁₀ n` solo difieren en una constante.

```grafica
tipo: lineas
titulo: Cómo crece cada complejidad (ilustrativo)
x: 1..20
ymax: 120
ejex: n (tamaño de la entrada)
O(1): 1
O(log n): log2(n)
O(n): n
O(n log n): n*log2(n)
O(n²): n^2
O(2^n): 2^n
```

![Curvas de complejidad: 1, log n, √n, n, n log n, n², 2ⁿ y n! (Wikimedia Commons, Cmglee, CC BY-SA 4.0)](img/algoritmos/complejidades.png)

### 🔢 ¿Cuántas operaciones son?

| Complejidad | n = 10 | n = 1 000 | n = 10⁶ |
|---|---|---|---|
| O(1) constante | 1 | 1 | 1 |
| O(log n) logarítmica | ~3 | ~10 | ~20 |
| O(n) lineal | 10 | 1 000 | 1 000 000 |
| O(n log n) | ~33 | ~10 000 | ~20 000 000 |
| O(n²) cuadrática | 100 | 1 000 000 | 10¹² |
| O(2ⁿ) exponencial | 1 024 | ~10³⁰¹ | imposible |

Traducido a tiempo, suponiendo **~10⁸ operaciones simples por segundo** (orden de magnitud típico, ilustrativo): con n = 10⁶, O(n log n) tarda ~0,2 s; O(n²) tarda 10⁴ s ≈ **casi 3 horas**; O(2ⁿ) ya con n = 60 tarda siglos.

📌 Resumen: regla de oro para entrevistas y concursos: si n ≤ 10⁶ necesitas O(n) u O(n log n); si n ≤ 10⁴, O(n²) suele pasar; si n ≤ 20, O(2ⁿ) es aceptable; si n ≤ 10, incluso O(n!).

| Nombre | Big O | Ejemplo típico |
|---|---|---|
| Constante | O(1) | `lista[i]`, `dict[clave]`, push/pop en pila |
| Logarítmica | O(log n) | Búsqueda binaria, operación en heap o BST balanceado |
| Lineal | O(n) | Recorrer una lista, `x in lista`, `max()` |
| Lineal-logarítmica | O(n log n) | Merge sort, `sorted()`, heap sort |
| Cuadrática | O(n²) | Dos bucles anidados, bubble sort |
| Cúbica | O(n³) | Multiplicar matrices ingenuo, Floyd-Warshall |
| Exponencial | O(2ⁿ) | Todos los subconjuntos, Fibonacci recursivo ingenuo |
| Factorial | O(n!) | Todas las permutaciones (viajante por fuerza bruta) |

### 🎭 Big O, Big Ω y Big Θ

::: columnas
### O grande
- Cota **superior**: "como mucho crece así".
- Es la que se usa en la práctica (peor caso).
::: siguiente
### Ω (Omega)
- Cota **inferior**: "como mínimo crece así".
- Ej.: ordenar por comparaciones es Ω(n log n).
::: siguiente
### Θ (Theta)
- Cota **exacta**: O y Ω a la vez.
- Merge sort es Θ(n log n) siempre.
:::

⚠️ Cuidado: "peor / mejor / caso promedio" NO es lo mismo que O / Ω / Θ. Quicksort tiene caso promedio O(n log n) y peor caso O(n²). En entrevistas, cuando dicen "la complejidad", casi siempre quieren el **peor caso** (o el promedio para hash tables, aclarándolo).

🧠 Concepto: **complejidad amortizada** = coste promedio por operación en una secuencia larga. `list.append` a veces copia toda la lista (O(n)), pero tan pocas veces que en promedio cuesta **O(1) amortizado**.

🇬🇧 **worst case** /uérst kéis/ = peor caso · **average case** /ávrich/ = caso promedio · **upper bound** /ápper báund/ = cota superior · **amortized** /ámortaizd/ = amortizado · **time complexity** = complejidad temporal · **space complexity** = complejidad espacial

## 🔍 Calcular la complejidad paso a paso (tiempo y espacio)

El método: **cuenta cuántas veces se ejecuta la línea más repetida** en función de n, y simplifica.

```flujo
dir: abajo
Código -> Bucles
Bucles -> Anidados
Bucles -> Seguidos
Bucles -> Mitad
Anidados -> Multiplica
Seguidos -> Suma
Mitad -> Log
Multiplica -> Simplifica
Suma -> Simplifica
Log -> Simplifica
Simplifica -> Resultado : término dominante
```

| Patrón de código | Complejidad | Por qué |
|---|---|---|
| Una instrucción, acceso por índice | O(1) | No depende de n |
| `for x in lista` | O(n) | n vueltas |
| Dos `for` seguidos (no anidados) | O(n + n) = O(n) | Se suman |
| `for` dentro de `for` | O(n · n) = O(n²) | Se multiplican |
| `while n > 1: n //= 2` | O(log n) | Cada vuelta divide a la mitad |
| `for` + dentro algo que divide a la mitad | O(n log n) | n veces log n |
| Recursión con 2 llamadas que bajan n en 1 | O(2ⁿ) | El árbol de llamadas se duplica |

### ✅ Ejemplo resuelto: ¿hay dos números que sumen `objetivo`?

```python
def par_suma_lento(nums, objetivo):
    n = len(nums)                          # O(1)
    for i in range(n):                     # n vueltas
        for j in range(i + 1, n):          # n-1, n-2, ..., 1 vueltas
            if nums[i] + nums[j] == objetivo:   # O(1)
                return (i, j)
    return None
# Comparaciones: (n-1) + (n-2) + ... + 1 = n(n-1)/2 → O(n²) tiempo, O(1) espacio

def par_suma_rapido(nums, objetivo):
    vistos = {}                            # valor → índice
    for i, x in enumerate(nums):           # n vueltas
        falta = objetivo - x
        if falta in vistos:                # O(1) promedio en un dict
            return (vistos[falta], i)
        vistos[x] = i                      # O(1) promedio
    return None
# → O(n) tiempo, O(n) espacio (el dict)

print(par_suma_lento([2, 7, 11, 15], 9))    # (0, 1)
print(par_suma_rapido([3, 2, 4], 6))        # (1, 2)
```

Paso a paso del lento: el `for` de fuera da n vueltas; el de dentro, en promedio n/2. Total ≈ n²/2 → quitamos la constante 1/2 → **O(n²)**. El rápido cambia memoria por tiempo: guarda lo visto en un diccionario para no volver a buscar.

### 🧪 Más ejemplos resueltos

```python
def a(n):
    i = 1
    while i < n:        # i vale 1, 2, 4, 8, ... hasta n
        i *= 2          # → log2(n) vueltas → O(log n)
    return i

def b(n):
    total = 0
    for i in range(n):          # n
        j = n
        while j > 0:            # log n
            j //= 2
            total += 1
    return total                # → O(n log n)

def c(lista_a, lista_b):
    return [x for x in lista_a if x in lista_b]   # `in` en lista = O(len b) → O(a·b)

def c_mejor(lista_a, lista_b):
    conjunto_b = set(lista_b)                     # O(b)
    return [x for x in lista_a if x in conjunto_b]  # O(a) → total O(a + b)

print(a(1000), b(8), c([1, 2, 3], [2, 3, 4]), c_mejor([1, 2, 3], [2, 3, 4]))
# 1024 32 [2, 3] [2, 3]
```

⚠️ Cuidado: **operaciones "ocultas"** que parecen O(1) y no lo son: `x in lista` (O(n)), `lista.insert(0, x)` y `lista.pop(0)` (O(n)), `lista[a:b]` (copia O(b-a)), `s1 + s2` con strings (O(len)), `sorted()` (O(n log n)), `lista.index(x)` (O(n)), `max()` / `sum()` (O(n)).

### 💾 Espacio vs tiempo

🧠 Concepto: la **complejidad espacial** es cuánta memoria **extra** usa el algoritmo (sin contar la entrada). Incluye estructuras auxiliares y la **pila de llamadas** de la recursión.

::: columnas
### 🐢 Menos memoria, más tiempo
- Comparar todos los pares: O(n²) tiempo, O(1) espacio.
- Recalcular en vez de guardar.
- Útil en microcontroladores o datos que no caben en RAM.
::: siguiente
### 🐇 Más memoria, menos tiempo
- Dict de vistos: O(n) tiempo, O(n) espacio.
- Memoización y cachés (Redis, CDN).
- Lo normal hoy: la RAM es barata, el tiempo del usuario no.
:::

| Algoritmo | Tiempo | Espacio extra |
|---|---|---|
| Recorrer y sumar | O(n) | O(1) |
| Merge sort | O(n log n) | O(n) |
| Heap sort | O(n log n) | O(1) |
| Factorial recursivo | O(n) | O(n) por la pila |
| Fibonacci con memo | O(n) | O(n) |
| Fibonacci con 2 variables | O(n) | O(1) |

💡 Consejo: en una entrevista di SIEMPRE las dos: "Esto es O(n) en tiempo y O(n) en espacio por el diccionario. Si la memoria importara, puedo ordenar y usar dos punteros: O(n log n) tiempo y O(1) espacio extra."

## 📦 Arrays y arrays dinámicos (list de Python)

🧠 Concepto: un **array** es un bloque **contiguo** de memoria con elementos del mismo tamaño. Como están seguidos, la dirección del elemento i es inicio + i × tamaño: por eso acceder por índice es **O(1)**.

Un **array dinámico** (la `list` de Python, el `Array` de JS, el `vector` de C++, el `ArrayList` de Java) reserva **más espacio del que usa** (capacidad > tamaño). Cuando se llena, pide un bloque más grande (en CPython ~1,125× + un poco; en otros lenguajes 1,5× o 2×), copia todo y libera el viejo. Esa copia es O(n), pero ocurre tan pocas veces que `append` es **O(1) amortizado**.

```capas
Índice : 0 · 1 · 2 · 3 · 4 · 5 · 6 · 7
Valores : 12 · 5 · 8 · 3 · 9 · (libre) · (libre) · (libre)
Memoria : un solo bloque contiguo → dirección = inicio + i × 8 bytes
```

```python
import sys

lista = []
capacidad_anterior = sys.getsizeof(lista)
for i in range(20):
    lista.append(i)
    tam = sys.getsizeof(lista)
    if tam != capacidad_anterior:          # el bloque creció: hubo copia
        print(f"len={len(lista):2d} → {tam} bytes")
        capacidad_anterior = tam
# Salida (CPython 3.14, 64 bits):
# len= 1 → 88 bytes
# len= 5 → 120 bytes
# len= 9 → 184 bytes
# len=17 → 248 bytes
```

Fíjate: no crece en cada `append`, sino a saltos. Entre salto y salto, cada `append` es una simple escritura.

| Operación en `list` | Complejidad | Nota |
|---|---|---|
| `a[i]`, `a[i] = x` | O(1) | Acceso directo |
| `a.append(x)` | O(1) amortizado | A veces redimensiona |
| `a.pop()` (del final) | O(1) | |
| `a.insert(0, x)`, `a.pop(0)` | O(n) | Desplaza todo |
| `x in a`, `a.index(x)` | O(n) | Búsqueda lineal |
| `a[i:j]` | O(j − i) | Crea una copia |
| `a.sort()` | O(n log n) | Timsort, estable |
| `len(a)` | O(1) | Guarda el tamaño |

::: columnas
### 🐍 Python
```python
a = [3, 1, 2]
a.append(4)      # [3, 1, 2, 4]
a.pop()          # 4
a.sort()         # [1, 2, 3]
print(a[-1])     # 3
```
::: siguiente
### 🟨 JavaScript
```js
const a = [3, 1, 2];
a.push(4);       // [3, 1, 2, 4]
a.pop();         // 4
a.sort((x, y) => x - y); // ¡con comparador!
console.log(a.at(-1));   // 3
```
:::

⚠️ Cuidado: en JS `[10, 9, 1].sort()` da `[1, 10, 9]` porque por defecto compara como **texto**. Siempre pasa `(a, b) => a - b` para números.

🇬🇧 **contiguous** /kontíguius/ = contiguo · **resize** /risáis/ = redimensionar · **capacity** = capacidad · **index** = índice · **out of bounds** = fuera de rango

## 🔗 Listas enlazadas

🧠 Concepto: una **lista enlazada** (linked list) es una cadena de **nodos** dispersos en memoria; cada nodo guarda un valor y un **puntero** al siguiente (y en la doblemente enlazada, también al anterior). No hay acceso por índice: para llegar al k-ésimo hay que caminar k pasos.

```flujo
cabeza -> N1
N1 -> N2 : next
N2 -> N3 : next
N3 -> None : next
```

¿Para qué, si el array es más rápido de acceder? Porque **insertar o borrar un nodo conocido es O(1)**: solo cambias dos punteros, sin desplazar nada. Por eso se usa dentro de otras estructuras: la caché **LRU** (dict + lista doblemente enlazada), `collections.deque` en CPython (lista doblemente enlazada de bloques), las listas del kernel de Linux, o el encadenamiento de colisiones en tablas hash.

```python
class Nodo:
    def __init__(self, valor, siguiente=None):
        self.valor = valor
        self.siguiente = siguiente

def imprimir(cabeza):
    partes = []
    while cabeza:
        partes.append(str(cabeza.valor))
        cabeza = cabeza.siguiente
    print(" -> ".join(partes) + " -> None")

def invertir(cabeza):
    """Clásico de entrevista: O(n) tiempo, O(1) espacio."""
    anterior = None
    actual = cabeza
    while actual:
        siguiente = actual.siguiente   # 1. guarda el resto
        actual.siguiente = anterior    # 2. da la vuelta a la flecha
        anterior = actual              # 3. avanza los dos punteros
        actual = siguiente
    return anterior                    # nueva cabeza

def tiene_ciclo(cabeza):
    """Floyd: tortuga (1 paso) y liebre (2 pasos). Si hay ciclo, se encuentran."""
    lento = rapido = cabeza
    while rapido and rapido.siguiente:
        lento = lento.siguiente
        rapido = rapido.siguiente.siguiente
        if lento is rapido:
            return True
    return False

lista = Nodo(1, Nodo(2, Nodo(3, Nodo(4))))
imprimir(lista)                 # 1 -> 2 -> 3 -> 4 -> None
lista = invertir(lista)
imprimir(lista)                 # 4 -> 3 -> 2 -> 1 -> None
print(tiene_ciclo(lista))       # False
lista.siguiente.siguiente.siguiente.siguiente = lista.siguiente   # 1 apunta a 3: ciclo
print(tiene_ciclo(lista))       # True
```

| Operación | Array dinámico | Lista enlazada |
|---|---|---|
| Acceso `k`-ésimo | O(1) | O(k) |
| Insertar al inicio | O(n) | O(1) |
| Insertar al final | O(1) amortizado | O(1) con puntero a la cola |
| Insertar en medio (nodo conocido) | O(n) | O(1) |
| Buscar valor | O(n) | O(n) |
| Uso de caché de CPU | Excelente (contiguo) | Malo (saltos en memoria) |

⚠️ Cuidado: en la práctica los arrays ganan casi siempre por la **localidad de caché**: la CPU trae bloques contiguos de memoria y recorrer un array es muchísimo más rápido que perseguir punteros. Bjarne Stroustrup (creador de C++) lo mostró en charlas comparando `vector` vs `list`: incluso insertando en medio, `vector` suele ganar. Usa listas enlazadas cuando de verdad necesites O(1) al borrar nodos que ya tienes localizados (LRU).

💡 Consejo: en entrevistas de listas enlazadas usa un **nodo centinela** (`dummy = Nodo(0, cabeza)`): evita el caso especial "¿y si borro la cabeza?". Y dibuja las flechas en papel antes de reasignar punteros.

## 🥞 Pilas y colas

::: columnas
### 🥞 Pila (stack) — LIFO
- **Last In, First Out**: el último en entrar es el primero en salir.
- Como una pila de platos.
- `push` (apilar), `pop` (desapilar), `peek` (mirar arriba): todo O(1).
- En Python: una `list` con `append` / `pop`.
::: siguiente
### 🚶 Cola (queue) — FIFO
- **First In, First Out**: el primero en llegar es el primero en salir.
- Como la fila del banco.
- `enqueue` (encolar), `dequeue` (desencolar): O(1).
- En Python: `collections.deque` con `append` / `popleft`.
:::

```secuencia
actores: Programa, Pila
Programa -> Pila : push("escribir hola")
Programa -> Pila : push("poner negrita")
Programa -> Pila : push("borrar línea")
nota Pila : Ctrl+Z saca lo último
Pila --> Programa : pop() → "borrar línea"
Pila --> Programa : pop() → "poner negrita"
```

| Estructura | Uso real |
|---|---|
| Pila | Deshacer/rehacer (Ctrl+Z), botón "atrás" del navegador |
| Pila | **Call stack**: cada llamada a función se apila; al hacer `return` se desapila |
| Pila | Verificar paréntesis, evaluar expresiones, DFS iterativo |
| Cola | **BFS** (recorrido por niveles), colas de impresión |
| Cola | Colas de mensajes (RabbitMQ, SQS, Kafka) y tareas (Celery) |
| Cola | Event loop de JS / asyncio: la cola de callbacks |
| Deque | Ventana deslizante con máximo, historial con tamaño fijo |

```python
from collections import deque

# ── Pila: ¿están balanceados los paréntesis? (LeetCode 20) ──
def balanceado(texto):
    pares = {")": "(", "]": "[", "}": "{"}
    pila = []
    for c in texto:
        if c in "([{":
            pila.append(c)                     # push
        elif c in pares:
            if not pila or pila.pop() != pares[c]:   # pop y compara
                return False
    return not pila                            # al final la pila debe quedar vacía

print(balanceado("def f(a[0]): {return}"))     # True
print(balanceado("(]"))                        # False
print(balanceado("(("))                        # False

# ── Cola: atender clientes en orden de llegada ──
cola = deque()
for cliente in ["Ana", "Luis", "Rosa"]:
    cola.append(cliente)          # encolar (por la derecha)
while cola:
    print("Atiendo a", cola.popleft())   # desencolar (por la izquierda), O(1)

# ── Historial con tamaño fijo: solo las 3 últimas páginas ──
historial = deque(maxlen=3)
for url in ["/inicio", "/cursos", "/algoritmos", "/grafos"]:
    historial.append(url)
print(list(historial))            # ['/cursos', '/algoritmos', '/grafos']
```

❌ Mal: usar `lista.pop(0)` como cola: cada `pop(0)` desplaza todos los elementos → O(n) por operación y O(n²) en total.
✅ Bien: `deque.popleft()` es O(1). En JS, `array.shift()` también es O(n) en general; para colas grandes usa un índice de "cabeza" o una cola enlazada.

```js
// Cola eficiente en JS: un array + índice de cabeza (sin shift)
const cola = [];
let cabeza = 0;
cola.push("Ana"); cola.push("Luis");
console.log(cola[cabeza++]); // Ana
console.log(cola[cabeza++]); // Luis
```

🇬🇧 **stack** /stak/ = pila · **queue** /kiú/ = cola · **push / pop** = apilar / desapilar · **enqueue / dequeue** /enkiú/ = encolar / desencolar · **deque** /dek/ = cola doble · **LIFO / FIFO** = último/primero en entrar, primero en salir

## 🗝️ Tablas hash y conjuntos

🧠 Concepto: una **tabla hash** guarda pares clave → valor en un array de "cubetas" (buckets). Una **función hash** convierte la clave en un número, y `hash(clave) % tamaño` dice en qué cubeta va. Así buscar, insertar y borrar cuestan **O(1) en promedio**: no se busca, se **calcula** dónde está.

```flujo
"Ana" -> hash : hash("Ana")
hash -> Número : 8274651...
Número -> Módulo : % 8
Módulo -> Cubeta3 : índice 3
Cubeta3 -> Valor : ("Ana", 20)
```

![Tabla hash: la función hash lleva cada clave (nombre) a una cubeta con su teléfono (Wikimedia Commons, Jorge Stolfi, CC BY-SA 3.0)](img/algoritmos/hash-table.png)

### 💥 Colisiones

Dos claves distintas pueden caer en la misma cubeta (hay infinitas claves y pocas cubetas: es inevitable, principio del palomar). Dos soluciones clásicas:

::: columnas
### ⛓️ Encadenamiento (chaining)
- Cada cubeta guarda una **lista** de pares.
- Colisión → se añade a la lista.
- Lo usa `HashMap` de Java (y desde Java 8 convierte listas largas en árboles).
::: siguiente
### 🚪 Direccionamiento abierto
- Si la cubeta está ocupada, se **prueba otra** (sondeo).
- Todo vive en un solo array: mejor caché.
- Lo usa el `dict` de CPython (sondeo pseudoaleatorio).
:::

Cuando la tabla se llena demasiado (**factor de carga** = elementos / cubetas pasa de ~2/3 en CPython), se crea una tabla más grande y se **rehashea** todo: O(n) puntual, O(1) amortizado.

```python
class TablaHash:
    """Tabla hash didáctica con encadenamiento."""
    def __init__(self, capacidad=4):
        self.cubetas = [[] for _ in range(capacidad)]
        self.n = 0

    def _indice(self, clave):
        return hash(clave) % len(self.cubetas)

    def poner(self, clave, valor):
        cubeta = self.cubetas[self._indice(clave)]
        for i, (k, _) in enumerate(cubeta):
            if k == clave:                 # ya existe: actualizar
                cubeta[i] = (clave, valor)
                return
        cubeta.append((clave, valor))      # nueva (o colisión: se encadena)
        self.n += 1
        if self.n / len(self.cubetas) > 0.75:   # factor de carga alto
            self._crecer()

    def obtener(self, clave):
        for k, v in self.cubetas[self._indice(clave)]:
            if k == clave:
                return v
        raise KeyError(clave)

    def _crecer(self):
        viejos = [par for cubeta in self.cubetas for par in cubeta]
        self.cubetas = [[] for _ in range(len(self.cubetas) * 2)]
        self.n = 0
        for k, v in viejos:
            self.poner(k, v)               # rehash: cada clave cae en otro sitio

t = TablaHash()
for nombre, edad in [("Ana", 20), ("Luis", 31), ("Rosa", 25), ("Juan", 40), ("Eva", 22)]:
    t.poner(nombre, edad)
print(t.obtener("Rosa"), len(t.cubetas), t.n)   # 25 8 5
```

### 🔑 Qué puede ser clave

La clave debe ser **hashable**: su hash no puede cambiar mientras está dentro. Por eso en Python `str`, `int`, `tuple` (de inmutables) y `frozenset` sirven; `list`, `dict` y `set` no.

```python
precios = {("La Paz", "pan"): 0.5}     # tupla como clave: OK
print(precios[("La Paz", "pan")])      # 0.5
try:
    malo = {["La Paz", "pan"]: 0.5}    # lista como clave
except TypeError as e:
    print("Error:", e)
# Error: cannot use 'list' as a dict key (unhashable type: 'list')
```

### 🧺 Conjuntos (`set`)

Un **set** es una tabla hash solo con claves: elementos **únicos**, `in` en O(1) promedio, sin orden por posición.

- `set(lista)` :: Quitar duplicados en O(n)
- `x in s` :: Pertenencia O(1) promedio (vs O(n) en lista)
- `a | b`, `a & b`, `a - b`, `a ^ b` :: Unión, intersección, diferencia, diferencia simétrica
- `Counter(texto).most_common(3)` :: Contar frecuencias (dict especializado)
- `defaultdict(list)` :: Dict que crea el valor por defecto (agrupar)

```python
from collections import Counter, defaultdict

alumnos_algoritmos = {"Ana", "Luis", "Rosa", "Juan"}
alumnos_ia = {"Rosa", "Juan", "Eva"}
print(sorted(alumnos_algoritmos & alumnos_ia))   # ['Juan', 'Rosa'] — en los dos
print(sorted(alumnos_ia - alumnos_algoritmos))   # ['Eva'] — solo en IA

# Anagramas agrupados (LeetCode 49): la clave es la palabra ordenada
palabras = ["amor", "roma", "mora", "perro", "ramo", "porre"]
grupos = defaultdict(list)
for p in palabras:
    grupos["".join(sorted(p))].append(p)
print(list(grupos.values()))   # [['amor', 'roma', 'mora', 'ramo'], ['perro', 'porre']]

print(Counter("abracadabra").most_common(2))     # [('a', 5), ('b', 2)]
```

| Operación | Promedio | Peor caso | Nota |
|---|---|---|---|
| Buscar / insertar / borrar | O(1) | O(n) | Peor caso: todas las claves colisionan |
| Recorrer | O(n) | O(n) | En Python el `dict` conserva orden de inserción (desde 3.7) |
| Espacio | O(n) | O(n) | Siempre hay cubetas vacías de sobra |

⚠️ Cuidado: el peor caso O(n) no es teórico. En 2011 (congreso 28C3) se mostró el ataque **HashDoS**: enviar a un servidor web miles de parámetros cuyas claves colisionan a propósito convertía cada petición en O(n²) y tumbaba servidores de PHP, Java, Python, Ruby... La solución fue **aleatorizar el hash** con una semilla secreta por proceso (en Python, activado por defecto desde 3.3; ver `PYTHONHASHSEED`). Consecuencia práctica: `hash("hola")` da otro número cada vez que arrancas Python.

::: columnas
### 🐍 Python
```python
edades = {"Ana": 20}
edades["Luis"] = 31
print(edades.get("Eva", 0))  # 0
vistos = set()
vistos.add(5)
```
::: siguiente
### 🟨 JavaScript
```js
const edades = new Map([["Ana", 20]]);
edades.set("Luis", 31);
console.log(edades.get("Eva") ?? 0); // 0
const vistos = new Set();
vistos.add(5);
```
:::

💡 Consejo: en JS usa `Map`/`Set` en vez de objetos `{}` como diccionario: aceptan cualquier tipo de clave, mantienen orden, tienen `.size` y no chocan con claves heredadas como `"constructor"` o `"__proto__"`.

🇬🇧 **hash function** = función hash · **bucket** /báket/ = cubeta · **collision** /kolíshon/ = colisión · **load factor** = factor de carga · **chaining** /chéining/ = encadenamiento · **open addressing** = direccionamiento abierto · **hashable** = que se puede hashear

## 🌳 Árboles, BST, recorridos y tries

🧠 Concepto: un **árbol** es una estructura jerárquica de nodos sin ciclos: hay una **raíz**, cada nodo tiene **hijos**, y los nodos sin hijos son **hojas**. La **altura** es el camino más largo de la raíz a una hoja. Un **árbol binario** tiene como mucho 2 hijos por nodo.

```arbol
/ (raíz)
  home
    yafer
      .config
        hypr
      Vídeos
  etc
    pacman.conf
  usr
    bin
```

Árboles en todas partes: el sistema de archivos, el DOM del navegador, el AST que crea un compilador (y Python con `ast.parse`), los índices B-tree de las bases de datos, los árboles de decisión y Random Forest en ML, el árbol de componentes de React.

### 🔎 Árbol binario de búsqueda (BST)

🧠 Concepto: en un **BST** (Binary Search Tree), para cada nodo, **todo** lo de su subárbol izquierdo es menor y **todo** lo del derecho es mayor. Buscar es como la búsqueda binaria: en cada nodo descartas una mitad. Coste O(h), donde h es la altura.

```arbol
8
  3
    1
    6
      4
      7
  10
    (vacío)
    14
      13
```

![El mismo BST dibujado: menores a la izquierda, mayores a la derecha (Wikimedia Commons, dominio público)](img/algoritmos/bst.png)

```python
class NodoBST:
    def __init__(self, valor):
        self.valor = valor
        self.izq = None
        self.der = None

def insertar(raiz, valor):
    if raiz is None:
        return NodoBST(valor)
    if valor < raiz.valor:
        raiz.izq = insertar(raiz.izq, valor)
    else:
        raiz.der = insertar(raiz.der, valor)
    return raiz

def buscar(raiz, valor):
    while raiz and raiz.valor != valor:
        raiz = raiz.izq if valor < raiz.valor else raiz.der   # descarta una mitad
    return raiz is not None

def altura(raiz):
    if raiz is None:
        return 0
    return 1 + max(altura(raiz.izq), altura(raiz.der))

raiz = None
for v in [8, 3, 10, 1, 6, 14, 4, 7, 13]:
    raiz = insertar(raiz, v)
print(buscar(raiz, 6), buscar(raiz, 5), altura(raiz))   # True False 4

# El peligro: insertar datos YA ORDENADOS crea una "lista" torcida
torcido = None
for v in range(1, 8):
    torcido = insertar(torcido, v)
print(altura(torcido))   # 7 → buscar es O(n), no O(log n)
```

⚠️ Cuidado: un BST **sin balancear** degenera en lista enlazada si los datos llegan ordenados (y en la vida real, los IDs y fechas suelen llegar ordenados). Por eso en producción se usan árboles **autobalanceados**: **AVL**, **rojo-negro** (`TreeMap` de Java, `std::map` de C++, el planificador de procesos del kernel de Linux (CFS y su sucesor EEVDF)) y **B-trees** (índices de bases de datos y sistemas de archivos). Garantizan altura O(log n).

### 🚶 Recorridos de un árbol

| Recorrido | Orden | Resultado en el BST de arriba | Uso típico |
|---|---|---|---|
| **Inorden** | izq → raíz → der | 1 3 4 6 7 8 10 13 14 | En un BST da los valores **ordenados** |
| **Preorden** | raíz → izq → der | 8 3 1 6 4 7 10 14 13 | Copiar/serializar el árbol |
| **Postorden** | izq → der → raíz | 1 4 7 6 3 13 14 10 8 | Borrar, calcular tamaños de carpetas |
| **Por niveles (BFS)** | nivel a nivel | 8 3 10 1 6 14 4 7 13 | Distancia mínima, imprimir por pisos |

```python
from collections import deque

class N:
    def __init__(self, v, izq=None, der=None):
        self.valor, self.izq, self.der = v, izq, der

#        8
#      /   \
#     3     10
#    / \      \
#   1   6      14
#      / \     /
#     4   7   13
raiz = N(8, N(3, N(1), N(6, N(4), N(7))), N(10, None, N(14, N(13))))

def inorden(n):
    return inorden(n.izq) + [n.valor] + inorden(n.der) if n else []

def preorden(n):
    return [n.valor] + preorden(n.izq) + preorden(n.der) if n else []

def postorden(n):
    return postorden(n.izq) + postorden(n.der) + [n.valor] if n else []

def por_niveles(raiz):
    niveles, cola = [], deque([raiz])
    while cola:
        nivel = []
        for _ in range(len(cola)):         # procesa exactamente un piso
            n = cola.popleft()
            nivel.append(n.valor)
            if n.izq: cola.append(n.izq)
            if n.der: cola.append(n.der)
        niveles.append(nivel)
    return niveles

def inorden_iterativo(raiz):
    """Sin recursión, con pila explícita (evita RecursionError en árboles muy altos)."""
    res, pila, n = [], [], raiz
    while pila or n:
        while n:                 # baja todo a la izquierda
            pila.append(n)
            n = n.izq
        n = pila.pop()
        res.append(n.valor)
        n = n.der
    return res

print(inorden(raiz))            # [1, 3, 4, 6, 7, 8, 10, 13, 14]
print(preorden(raiz))           # [8, 3, 1, 6, 4, 7, 10, 14, 13]
print(postorden(raiz))          # [1, 4, 7, 6, 3, 13, 14, 10, 8]
print(por_niveles(raiz))        # [[8], [3, 10], [1, 6, 14], [4, 7, 13]]
print(inorden_iterativo(raiz) == inorden(raiz))   # True
```

💡 Consejo: truco para recordar: el nombre dice **cuándo visitas la raíz**: **pre** = antes de los hijos, **in** = entre ellos, **post** = después.

### 🔤 Tries (árbol de prefijos)

🧠 Concepto: un **trie** guarda palabras letra por letra: cada camino desde la raíz deletrea un prefijo. Buscar una palabra o saber si existe algún prefijo cuesta **O(L)** (L = largo de la palabra), sin importar cuántas palabras haya.

![Trie con las claves "A", "to", "tea", "ted", "ten", "i", "in", "inn" (Wikimedia Commons, dominio público)](img/algoritmos/trie.png)

```python
class Trie:
    def __init__(self):
        self.raiz = {}

    def insertar(self, palabra):
        nodo = self.raiz
        for letra in palabra:
            nodo = nodo.setdefault(letra, {})   # crea el hijo si no existe
        nodo["$"] = True                        # marca de fin de palabra

    def contiene(self, palabra):
        nodo = self._bajar(palabra)
        return nodo is not None and "$" in nodo

    def autocompletar(self, prefijo):
        nodo = self._bajar(prefijo)
        if nodo is None:
            return []
        resultado = []
        def dfs(n, camino):
            if "$" in n:
                resultado.append(prefijo + camino)
            for letra in sorted(k for k in n if k != "$"):
                dfs(n[letra], camino + letra)
        dfs(nodo, "")
        return resultado

    def _bajar(self, texto):
        nodo = self.raiz
        for letra in texto:
            if letra not in nodo:
                return None
            nodo = nodo[letra]
        return nodo

t = Trie()
for p in ["python", "pytorch", "pandas", "pila", "pilas", "grafo"]:
    t.insertar(p)
print(t.contiene("pila"), t.contiene("pil"))   # True False
print(t.autocompletar("py"))                   # ['python', 'pytorch']
print(t.autocompletar("pi"))                   # ['pila', 'pilas']
```

Usos reales: autocompletado de buscadores y teclados, corrector ortográfico, tablas de enrutamiento IP (búsqueda del prefijo más largo), y los tokenizadores de modelos de lenguaje que buscan el prefijo más largo en su vocabulario.

🇬🇧 **root** /rut/ = raíz · **leaf** /lif/ = hoja · **height** /jáit/ = altura · **binary search tree** = árbol binario de búsqueda · **in-order / pre-order / post-order** = inorden / preorden / postorden · **level-order** = por niveles · **balanced** = balanceado · **trie** /trai/ = árbol de prefijos

## ⛰️ Heaps y colas de prioridad

🧠 Concepto: un **heap** (montículo) es un árbol binario **completo** donde cada padre es ≤ que sus hijos (**min-heap**) o ≥ (**max-heap**). No está totalmente ordenado: solo garantiza que **la raíz es el mínimo** (o el máximo). Ver el mínimo: O(1). Sacarlo o insertar: **O(log n)**.

El truco: como el árbol es completo, se guarda en un **array** sin punteros. Para el nodo en la posición `i`: hijos en `2i + 1` y `2i + 2`, padre en `(i − 1) // 2`.

![Max-heap: el mismo heap como árbol y como array (Wikimedia Commons, Ermishin, CC BY-SA 3.0)](img/algoritmos/max-heap.png)

```flujo
dir: abajo
Insertar -> AlFinal : pon el nuevo al final del array
AlFinal -> Sube : ¿menor que su padre?
Sube -> Intercambia : sí
Intercambia -> Sube : repite
Sube -> Listo : no / es la raíz
```

```python
import heapq

# heapq de Python es un MIN-heap sobre una lista normal
tareas = []
heapq.heappush(tareas, (3, "responder correos"))
heapq.heappush(tareas, (1, "arreglar bug en producción"))
heapq.heappush(tareas, (2, "revisar PR"))
while tareas:
    prioridad, tarea = heapq.heappop(tareas)   # siempre sale la de menor número
    print(prioridad, tarea)
# 1 arreglar bug en producción
# 2 revisar PR
# 3 responder correos

# Max-heap: guarda los números negados
precios = [30, 10, 50, 20]
max_heap = [-p for p in precios]
heapq.heapify(max_heap)            # O(n), no O(n log n)
print(-max_heap[0])                # 50

# Top-k: los 3 mayores de un millón de datos sin ordenar todo → O(n log k)
import random
random.seed(42)
datos = [random.randint(1, 10**9) for _ in range(1_000_000)]
print(heapq.nlargest(3, datos) == sorted(datos)[-3:][::-1])   # True
```

### ✅ Ejemplo resuelto: mediana en streaming (dos heaps)

```python
import heapq

class Mediana:
    """Mitad menor en un max-heap, mitad mayor en un min-heap."""
    def __init__(self):
        self.menores = []   # max-heap (negados)
        self.mayores = []   # min-heap

    def agregar(self, x):
        heapq.heappush(self.menores, -x)
        heapq.heappush(self.mayores, -heapq.heappop(self.menores))  # equilibra valores
        if len(self.mayores) > len(self.menores):                   # equilibra tamaños
            heapq.heappush(self.menores, -heapq.heappop(self.mayores))

    def mediana(self):
        if len(self.menores) > len(self.mayores):
            return -self.menores[0]
        return (-self.menores[0] + self.mayores[0]) / 2

m = Mediana()
for x in [5, 15, 1, 3]:
    m.agregar(x)
    print(m.mediana(), end=" ")    # 5 10.0 5 4.0
print()
```

| Uso real | Por qué un heap |
|---|---|
| Dijkstra / A* (mapas, juegos) | Sacar siempre el nodo más cercano |
| Planificadores de procesos y timers | Siguiente evento por tiempo |
| Top-k (trending, ranking) | Mantener solo k elementos |
| Mezclar k archivos ordenados (`heapq.merge`) | El menor de k cabezas |
| Huffman (compresión) | Unir los dos símbolos menos frecuentes |

⚠️ Cuidado: si metes tuplas `(prioridad, objeto)` y hay empate en prioridad, Python compara los objetos y puede lanzar `TypeError` si no son comparables. Solución: `(prioridad, contador, objeto)` con un contador creciente (`itertools.count()`).

🇬🇧 **heap** /jiip/ = montículo · **priority queue** /praióriti kiú/ = cola de prioridad · **heapify** = convertir en heap · **sift up / sift down** = subir / hundir · **top-k** = los k mejores

## 🕸️ Grafos: representación, BFS y DFS

🧠 Concepto: un **grafo** es un conjunto de **vértices** (nodos) unidos por **aristas** (edges). Puede ser **dirigido** (A → B no implica B → A, como "seguir" en Instagram) o **no dirigido** (amistad en Facebook), y **ponderado** (las aristas tienen peso: km, ms, costo) o no. Un árbol es un grafo conexo sin ciclos.

Casi todo es un grafo: mapas y rutas, redes sociales, dependencias de paquetes (`npm`, `pip`), enlaces entre páginas web (PageRank de Google), el historial de Git, las redes neuronales (grafo de cómputo de PyTorch), los microservicios que se llaman entre sí.

```flujo
La Paz <-> El Alto : 15 km
El Alto <-> Oruro : 215 km
Oruro <-> Potosí : 310 km
Oruro <-> Cochabamba : 210 km
Cochabamba <-> Santa Cruz : 470 km
```

📌 Resumen: distancias **aproximadas e ilustrativas**, solo para practicar. Las carreteras son de doble sentido (flechas en ambas puntas). Para no cruzar líneas no se dibuja la ruta directa La Paz–Oruro (230 km), pero sí está en el código de Dijkstra más abajo.

### 🗂️ Cómo guardar un grafo

| Representación | Espacio | ¿Existe arista u→v? | Vecinos de u | Cuándo |
|---|---|---|---|---|
| **Lista de adyacencia** (`dict` de listas) | O(V + E) | O(grado) | O(grado) | Casi siempre (grafos dispersos) |
| **Matriz de adyacencia** | O(V²) | O(1) | O(V) | Grafos densos, pocos nodos |
| **Lista de aristas** | O(E) | O(E) | O(E) | Kruskal, entrada de problemas |

```python
# Lista de adyacencia: lo más usado en entrevistas y en la vida real
grafo = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "F"],
    "D": ["B"],
    "E": ["B", "F"],
    "F": ["C", "E"],
}

# Construirla desde una lista de aristas (formato típico de LeetCode)
from collections import defaultdict
aristas = [(0, 1), (0, 2), (1, 3)]
adj = defaultdict(list)
for u, v in aristas:
    adj[u].append(v)
    adj[v].append(u)       # quita esta línea si el grafo es dirigido
print(dict(adj))           # {0: [1, 2], 1: [0, 3], 2: [0], 3: [1]}

# Matriz de adyacencia del mismo grafo
n = 4
matriz = [[0] * n for _ in range(n)]
for u, v in aristas:
    matriz[u][v] = matriz[v][u] = 1
for fila in matriz:
    print(fila)
# [0, 1, 1, 0]
# [1, 0, 0, 1]
# [1, 0, 0, 0]
# [0, 1, 0, 0]
```

### 🌊 BFS vs 🕳️ DFS

::: columnas
### 🌊 BFS (en anchura)
- Explora **por niveles**: primero los vecinos, luego los vecinos de los vecinos.
- Usa una **cola** (FIFO).
- Encuentra el **camino más corto en número de aristas** (grafos sin pesos).
- Usos: "grados de separación", laberintos, propagación.
::: siguiente
### 🕳️ DFS (en profundidad)
- Baja por un camino **hasta el fondo** y luego retrocede.
- Usa una **pila** (o la recursión, que es la pila de llamadas).
- Útil para detectar ciclos, componentes, orden topológico, backtracking.
- Usos: resolver laberintos, explorar todas las opciones.
:::

```arbol
A (nivel 0)
  B (nivel 1)
    D (nivel 2)
    E (nivel 2)
  C (nivel 1)
    F (nivel 2)
```

Con el grafo de arriba empezando en A: **BFS** visita `A B C D E F` (nivel por nivel); **DFS** visita `A B D E F C` (baja por B hasta D, retrocede, sigue por E → F, y C ya solo queda al final).

```python
from collections import deque

grafo = {
    "A": ["B", "C"], "B": ["A", "D", "E"], "C": ["A", "F"],
    "D": ["B"], "E": ["B", "F"], "F": ["C", "E"],
}

def bfs(grafo, inicio):
    visitados = {inicio}            # marcar AL ENCOLAR, no al sacar
    cola = deque([inicio])
    orden = []
    while cola:
        nodo = cola.popleft()
        orden.append(nodo)
        for vecino in grafo[nodo]:
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append(vecino)
    return orden

def dfs(grafo, nodo, visitados=None):
    if visitados is None:           # ¡nunca uses set() como valor por defecto!
        visitados = []
    visitados.append(nodo)
    for vecino in grafo[nodo]:
        if vecino not in visitados:
            dfs(grafo, vecino, visitados)
    return visitados

def camino_mas_corto(grafo, origen, destino):
    """BFS guardando de dónde vino cada nodo para reconstruir el camino."""
    padre = {origen: None}
    cola = deque([origen])
    while cola:
        nodo = cola.popleft()
        if nodo == destino:
            camino = []
            while nodo is not None:
                camino.append(nodo)
                nodo = padre[nodo]
            return camino[::-1]
        for v in grafo[nodo]:
            if v not in padre:
                padre[v] = nodo
                cola.append(v)
    return None

print(bfs(grafo, "A"))                     # ['A', 'B', 'C', 'D', 'E', 'F']
print(dfs(grafo, "A"))                     # ['A', 'B', 'D', 'E', 'F', 'C']
print(camino_mas_corto(grafo, "D", "F"))   # ['D', 'B', 'E', 'F']
```

Ambos son **O(V + E)**: cada vértice se visita una vez y cada arista se mira una (o dos) veces.

### ✅ Ejemplo resuelto: contar islas en una cuadrícula (LeetCode 200)

Una matriz es un grafo implícito: cada celda es un nodo y sus 4 vecinos son las aristas.

```python
def contar_islas(mapa):
    filas, cols = len(mapa), len(mapa[0])
    vistos = set()

    def hundir(f, c):                       # DFS iterativo con pila
        pila = [(f, c)]
        while pila:
            f, c = pila.pop()
            if (0 <= f < filas and 0 <= c < cols
                    and mapa[f][c] == "1" and (f, c) not in vistos):
                vistos.add((f, c))
                pila.extend([(f + 1, c), (f - 1, c), (f, c + 1), (f, c - 1)])

    islas = 0
    for f in range(filas):
        for c in range(cols):
            if mapa[f][c] == "1" and (f, c) not in vistos:
                islas += 1                  # encontramos tierra nueva
                hundir(f, c)                # marcamos toda la isla
    return islas

mapa = ["11000",
        "11000",
        "00100",
        "00011"]
print(contar_islas(mapa))    # 3
```

🇬🇧 **graph** /graf/ = grafo · **vertex / vertices** /vértex, vértisis/ = vértice(s) · **edge** /edch/ = arista · **directed / undirected** = dirigido / no dirigido · **weighted** /uéitid/ = ponderado · **adjacency list** /adyéisensi/ = lista de adyacencia · **breadth-first** /bredz/ = en anchura · **depth-first** /depz/ = en profundidad

## 🗺️ Dijkstra, orden topológico y union-find

### 🚗 Dijkstra: camino más corto con pesos

🧠 Concepto: **Dijkstra** (ideado en 1956 por Edsger Dijkstra, publicado en 1959) encuentra la distancia mínima desde un origen a todos los nodos en un grafo con pesos **no negativos**. Idea greedy: saca siempre el nodo no procesado **más cercano** (con un heap) y "relaja" sus aristas: si pasar por él mejora la distancia a un vecino, la actualiza.

```flujo
dir: abajo
Inicio -> Heap : origen con distancia 0
Heap -> Sacar : el más cercano
Sacar -> Relajar : cada vecino
Relajar -> Mejora : ¿d + peso es menor?
Mejora --> Heap : sí: actualiza y push
```

```python
import heapq

rutas = {   # km aproximados, ilustrativos
    "La Paz": [("El Alto", 15), ("Oruro", 230)],
    "El Alto": [("La Paz", 15), ("Oruro", 215)],
    "Oruro": [("La Paz", 230), ("El Alto", 215), ("Cochabamba", 210), ("Potosí", 310)],
    "Cochabamba": [("Oruro", 210), ("Santa Cruz", 470)],
    "Potosí": [("Oruro", 310)],
    "Santa Cruz": [("Cochabamba", 470)],
}

def dijkstra(grafo, origen):
    dist = {origen: 0}
    previo = {origen: None}
    heap = [(0, origen)]
    while heap:
        d, nodo = heapq.heappop(heap)
        if d > dist[nodo]:
            continue                      # entrada vieja del heap: ignorar
        for vecino, peso in grafo[nodo]:
            nueva = d + peso
            if nueva < dist.get(vecino, float("inf")):
                dist[vecino] = nueva      # relajar
                previo[vecino] = nodo
                heapq.heappush(heap, (nueva, vecino))
    return dist, previo

def reconstruir(previo, destino):
    camino = []
    while destino is not None:
        camino.append(destino)
        destino = previo[destino]
    return camino[::-1]

dist, previo = dijkstra(rutas, "El Alto")
print(dist["Santa Cruz"])                  # 895
print(" → ".join(reconstruir(previo, "Santa Cruz")))
# El Alto → Oruro → Cochabamba → Santa Cruz
```

Complejidad con heap binario: **O((V + E) log V)**.

| Algoritmo | Problema | Pesos negativos | Complejidad |
|---|---|---|---|
| BFS | Camino más corto sin pesos | — | O(V + E) |
| Dijkstra | Desde un origen, pesos ≥ 0 | ❌ No | O((V + E) log V) |
| Bellman-Ford | Desde un origen, detecta ciclos negativos | ✅ Sí | O(V · E) |
| Floyd-Warshall | Entre todos los pares | ✅ Sí (sin ciclos negativos) | O(V³) |
| A* | Origen → destino con heurística | ❌ No | Depende de la heurística |

💡 Consejo: los navegadores tipo Google Maps no corren Dijkstra "puro" sobre el mapa del mundo: usan variantes y preprocesamiento (A*, contraction hierarchies y similares) porque el grafo tiene cientos de millones de nodos. Pero la base conceptual es Dijkstra. Los protocolos de enrutamiento de Internet como **OSPF** sí usan Dijkstra (SPF = Shortest Path First).

### 📋 Orden topológico

🧠 Concepto: en un **grafo dirigido acíclico** (DAG), un **orden topológico** pone cada nodo antes de todos los que dependen de él. Es exactamente lo que hace `pip`/`npm` al instalar dependencias, `make` al compilar, Airflow al ejecutar tareas, o una malla curricular con prerrequisitos.

```flujo
Programación -> Estructuras
Matemática discreta -> Estructuras
Estructuras -> Algoritmos
Algoritmos -> IA
Estadística -> IA
```

```python
from collections import deque

def orden_topologico(dependencias):
    """Algoritmo de Kahn: saca primero los que no tienen prerrequisitos."""
    grafo = {n: [] for n in dependencias}
    grado_entrada = {n: 0 for n in dependencias}
    for curso, previos in dependencias.items():
        for p in previos:
            grafo[p].append(curso)
            grado_entrada[curso] += 1
    cola = deque(n for n in dependencias if grado_entrada[n] == 0)
    orden = []
    while cola:
        n = cola.popleft()
        orden.append(n)
        for siguiente in grafo[n]:
            grado_entrada[siguiente] -= 1
            if grado_entrada[siguiente] == 0:
                cola.append(siguiente)
    if len(orden) != len(dependencias):
        raise ValueError("Hay un ciclo: no existe orden posible")
    return orden

malla = {
    "Programación": [],
    "Matemática discreta": [],
    "Estadística": [],
    "Estructuras": ["Programación", "Matemática discreta"],
    "Algoritmos": ["Estructuras"],
    "IA": ["Algoritmos", "Estadística"],
}
print(orden_topologico(malla))
# ['Programación', 'Matemática discreta', 'Estadística', 'Estructuras', 'Algoritmos', 'IA']

# En la librería estándar (Python 3.9+): graphlib
from graphlib import TopologicalSorter
print(list(TopologicalSorter(malla).static_order())[-1])   # IA
```

### 🤝 Union-Find (Disjoint Set Union)

🧠 Concepto: **Union-Find** mantiene grupos disjuntos y responde muy rápido "¿están a y b en el mismo grupo?" (`find`) y "junta sus grupos" (`union`). Con **compresión de caminos** y **unión por rango**, cada operación cuesta casi O(1) (técnicamente O(α(n)), la inversa de Ackermann, ≤ 4 para cualquier n práctico).

Usos: Kruskal (árbol de expansión mínima: cablear una red con el mínimo cable), detectar ciclos en grafos no dirigidos, componentes conexas, agrupar cuentas de un mismo usuario, segmentación de imágenes.

```python
class UnionFind:
    def __init__(self, n):
        self.padre = list(range(n))   # cada uno es su propio jefe
        self.rango = [0] * n
        self.grupos = n

    def find(self, x):
        if self.padre[x] != x:
            self.padre[x] = self.find(self.padre[x])   # compresión de caminos
        return self.padre[x]

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False                  # ya estaban juntos → esta arista haría un ciclo
        if self.rango[ra] < self.rango[rb]:
            ra, rb = rb, ra
        self.padre[rb] = ra               # el árbol bajo cuelga del alto
        if self.rango[ra] == self.rango[rb]:
            self.rango[ra] += 1
        self.grupos -= 1
        return True

# Kruskal: conectar 5 oficinas con el menor costo de cable
aristas = [(1, 0, 1), (4, 0, 2), (3, 1, 2), (2, 1, 3), (5, 2, 4), (7, 3, 4)]   # (costo, u, v)
uf = UnionFind(5)
total, usadas = 0, []
for costo, u, v in sorted(aristas):      # greedy: las más baratas primero
    if uf.union(u, v):
        total += costo
        usadas.append((u, v))
print(usadas, total, uf.grupos)          # [(0, 1), (1, 3), (1, 2), (2, 4)] 11 1
```

🇬🇧 **shortest path** = camino más corto · **relaxation** = relajación · **topological sort** = orden topológico · **DAG** (directed acyclic graph) = grafo dirigido acíclico · **in-degree** = grado de entrada · **disjoint set** = conjuntos disjuntos · **minimum spanning tree** = árbol de expansión mínima

## 🔁 Recursión

🧠 Concepto: una función **recursiva** se llama a sí misma con un problema más pequeño. Necesita dos partes: un **caso base** (cuándo parar, sin llamarse) y un **caso recursivo** (que se acerque al caso base). Sin caso base → recursión infinita → `RecursionError` (en otros lenguajes, stack overflow).

Cada llamada ocupa un **marco** (frame) en la **pila de llamadas** (call stack) con sus variables locales. Las llamadas se apilan hasta llegar al caso base, y luego se desapilan devolviendo resultados.

```python
def factorial(n):
    if n <= 1:                  # caso base
        return 1
    return n * factorial(n - 1) # caso recursivo: problema más pequeño

print(factorial(5))   # 120
```

```secuencia
actores: main, f(4), f(3), f(2), f(1)
main -> f(4) : factorial(4)
f(4) -> f(3) : 4 * factorial(3)
f(3) -> f(2) : 3 * factorial(2)
f(2) -> f(1) : 2 * factorial(1)
nota f(1) : caso base
f(1) --> f(2) : 1
f(2) --> f(3) : 2
f(3) --> f(4) : 6
f(4) --> main : 24
```

```capas
f(1) : cima de la pila — n=1, devuelve 1
f(2) : n=2, espera el resultado de f(1)
f(3) : n=3, espera f(2)
f(4) : n=4, espera f(3)
main : fondo de la pila
```

```python
import sys

print(sys.getrecursionlimit())    # 1000 (por defecto en CPython)

def suma_recursiva(n):
    return 0 if n == 0 else n + suma_recursiva(n - 1)

try:
    suma_recursiva(100_000)
except RecursionError as e:
    print("RecursionError:", e)   # RecursionError: maximum recursion depth exceeded

# Solución: hacerlo iterativo (o con pila explícita)
def suma_iterativa(n):
    total = 0
    for i in range(n + 1):
        total += i
    return total
print(suma_iterativa(100_000))     # 5000050000
```

⚠️ Cuidado: Python **no optimiza la recursión de cola** (tail call): una recursión de 100 000 niveles revienta aunque sea "de cola". Para recorridos profundos (listas enlazadas largas, DFS en grafos grandes, árboles degenerados) usa una pila explícita. Subir el límite con `sys.setrecursionlimit` puede hacer que el proceso muera por falta de pila del sistema.

| Recursión | Iteración |
|---|---|
| Natural para árboles, grafos, divide y vencerás | Natural para recorrer secuencias |
| Código corto y elegante | Código a veces más largo |
| Usa O(profundidad) de memoria en la pila | O(1) extra normalmente |
| Riesgo de `RecursionError` | Sin ese riesgo |

💡 Consejo: para escribir una recursión, **confía en la llamada recursiva** ("salto de fe"): asume que `f(n-1)` ya funciona y solo piensa cómo usar su resultado para construir `f(n)`. Luego verifica el caso base.

🇬🇧 **recursion** /rikérshon/ = recursión · **base case** /béis kéis/ = caso base · **call stack** = pila de llamadas · **stack frame** = marco de pila · **stack overflow** = desbordamiento de pila · **tail call** = llamada de cola

## 🎯 Búsqueda binaria

🧠 Concepto: la **búsqueda binaria** encuentra un valor en un array **ordenado** comparando con el elemento del medio y descartando la mitad que no puede contenerlo. Cada paso divide el espacio entre 2 → **O(log n)**: 1 000 000 de elementos en ≤ 20 pasos; 1 000 millones en ≤ 30.

```flujo
dir: abajo
Rango -> Medio : mira el centro
Medio -> Encontrado : igual
Medio -> Descartar : distinto
Descartar --> Rango : otra mitad
```

Si el rango queda vacío (`izq > der`), el valor no está y se devuelve -1.

```python
def busqueda_binaria(a, objetivo):
    izq, der = 0, len(a) - 1          # rango CERRADO [izq, der]
    while izq <= der:                 # <= porque el rango de 1 elemento es válido
        medio = (izq + der) // 2
        if a[medio] == objetivo:
            return medio
        if a[medio] < objetivo:
            izq = medio + 1           # +1: medio ya se descartó
        else:
            der = medio - 1
    return -1

notas = [35, 42, 51, 51, 51, 67, 78, 85, 91]
print(busqueda_binaria(notas, 78))    # 6
print(busqueda_binaria(notas, 50))    # -1

# bisect: la versión de la librería estándar (en C, probada)
import bisect
print(bisect.bisect_left(notas, 51))  # 2 → primera posición donde cabe 51
print(bisect.bisect_right(notas, 51)) # 5 → justo después del último 51
print(bisect.bisect_right(notas, 51) - bisect.bisect_left(notas, 51))  # 3 veces aparece
```

### 🐛 Los errores off-by-one (de uno en uno)

| Error | Consecuencia | Cómo evitarlo |
|---|---|---|
| `while izq < der` con rango cerrado | No revisa el último elemento | Rango cerrado → `<=` |
| `izq = medio` (sin +1) | **Bucle infinito** cuando izq + 1 == der | Siempre avanza: `medio + 1` |
| `der = len(a)` con `a[der]` | `IndexError` | Decide: cerrado `[0, n-1]` o semiabierto `[0, n)` y sé coherente |
| `medio = (izq + der) / 2` | En Python da float → `TypeError` al indexar | Usa `//` |
| `(izq + der) / 2` en Java/C con int | **Desbordamiento** de enteros con arrays enormes | `izq + (der - izq) / 2` |

⚠️ Cuidado: el último error es famoso: en 2006 Joshua Bloch (Google) publicó que la búsqueda binaria de la librería de Java (`Arrays.binarySearch`, que él mismo escribió) tenía este bug desde hacía ~9 años: con arrays de más de ~2³⁰ elementos, `low + high` desbordaba a negativo. Lo mismo afectaba a muchos merge sort. En Python no pasa (enteros sin límite), pero en Java, C, C++, Go o Rust sí.

### 🔭 Búsqueda binaria "sobre la respuesta"

El patrón más potente: no buscas en un array, sino el **menor valor que cumple una condición monótona** (falso, falso, ..., verdadero, verdadero).

```python
# ¿Velocidad mínima para comer todas las pilas de bananas en h horas? (LeetCode 875)
import math

def puede(pilas, h, velocidad):
    return sum(math.ceil(p / velocidad) for p in pilas) <= h

def velocidad_minima(pilas, h):
    izq, der = 1, max(pilas)          # rango de respuestas posibles
    while izq < der:                  # rango semiabierto: busca el primer True
        medio = (izq + der) // 2
        if puede(pilas, h, medio):
            der = medio               # medio sirve: quizás hay uno menor
        else:
            izq = medio + 1           # medio no sirve: hay que ir más rápido
    return izq

print(velocidad_minima([3, 6, 7, 11], 8))   # 4
```

💡 Consejo: plantilla mental: "si puedo con X, también puedo con cualquier cosa mayor que X" → búsqueda binaria sobre X. Aparece en: capacidad mínima de un barco, mínimo máximo de una partición, raíz cuadrada entera, `git bisect` (encontrar el primer commit que rompió algo).

🇬🇧 **binary search** = búsqueda binaria · **off-by-one error** = error de uno en uno · **midpoint** = punto medio · **overflow** /óverflou/ = desbordamiento · **lower bound / upper bound** = primera posición ≥ / > · **monotonic** /monotónik/ = monótono

## 🔀 Algoritmos de ordenamiento

Ordenar es el paso previo de muchísimos algoritmos (búsqueda binaria, two pointers, quitar duplicados, intervalos, greedy). En el día a día **usas** `sorted()`, pero entender cómo funcionan por dentro te enseña las técnicas base: incremental, divide y vencerás, heaps y conteo.

🧠 Concepto: un ordenamiento es **estable** si elementos iguales conservan su orden original. Importa al ordenar por varios criterios: ordenar alumnos por nota sin desordenar los que ya estaban por nombre.

| Algoritmo | Mejor | Promedio | Peor | Espacio | Estable |
|---|---|---|---|---|---|
| Bubble sort | O(n) | O(n²) | O(n²) | O(1) | ✅ |
| Insertion sort | O(n) | O(n²) | O(n²) | O(1) | ✅ |
| Selection sort | O(n²) | O(n²) | O(n²) | O(1) | ❌ |
| Merge sort | O(n log n) | O(n log n) | O(n log n) | O(n) | ✅ |
| Quicksort | O(n log n) | O(n log n) | O(n²) | O(log n) | ❌ |
| Heap sort | O(n log n) | O(n log n) | O(n log n) | O(1) | ❌ |
| Counting sort | O(n + k) | O(n + k) | O(n + k) | O(k) | ✅ |
| Timsort (Python) | O(n) | O(n log n) | O(n log n) | O(n) | ✅ |

📌 Resumen: ningún ordenamiento **por comparaciones** puede ser mejor que **O(n log n)** en el peor caso (hay n! órdenes posibles y cada comparación da 1 bit: log₂(n!) ≈ n log n). Counting/radix sort lo "rompen" porque **no comparan**: aprovechan que las claves son enteros pequeños.

### 🫧 Bubble e insertion sort (O(n²), pero útiles para entender)

```python
def bubble_sort(a):
    a = a[:]                                # no modificar la original
    n = len(a)
    for i in range(n):
        hubo_cambio = False
        for j in range(n - 1 - i):          # el mayor "burbujea" al final
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                hubo_cambio = True
        if not hubo_cambio:                 # ya ordenado → O(n) en el mejor caso
            break
    return a

def insertion_sort(a):
    a = a[:]
    for i in range(1, len(a)):
        actual = a[i]
        j = i - 1
        while j >= 0 and a[j] > actual:     # desplaza los mayores a la derecha
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = actual                   # inserta en su hueco (como cartas en la mano)
    return a

datos = [29, 10, 14, 37, 13]
print(bubble_sort(datos))      # [10, 13, 14, 29, 37]
print(insertion_sort(datos))   # [10, 13, 14, 29, 37]
```

💡 Consejo: **insertion sort** es excelente para arrays **pequeños** o **casi ordenados** (cada elemento se mueve poco). Por eso Timsort lo usa para tramos cortos.

### ✂️ Merge sort (divide y vencerás, estable)

```arbol
[38, 27, 43, 3, 9, 82, 10]
  [38, 27, 43]
    [38]
    [27, 43]
      [27]
      [43]
  [3, 9, 82, 10]
    [3, 9]
      [3]
      [9]
    [82, 10]
      [82]
      [10]
```

Se divide hasta tener listas de 1 elemento (ya ordenadas) y luego se **mezclan** de dos en dos comparando las cabezas. Hay log n niveles y cada nivel mezcla n elementos → **O(n log n) siempre**.

```python
def merge_sort(a):
    if len(a) <= 1:                       # caso base
        return a
    medio = len(a) // 2
    izq = merge_sort(a[:medio])           # divide
    der = merge_sort(a[medio:])
    return mezclar(izq, der)              # combina

def mezclar(izq, der):
    res, i, j = [], 0, 0
    while i < len(izq) and j < len(der):
        if izq[i] <= der[j]:              # <= mantiene la estabilidad
            res.append(izq[i]); i += 1
        else:
            res.append(der[j]); j += 1
    res.extend(izq[i:])                   # lo que sobre de cada lado
    res.extend(der[j:])
    return res

print(merge_sort([38, 27, 43, 3, 9, 82, 10]))   # [3, 9, 10, 27, 38, 43, 82]
```

### ⚡ Quicksort

Elige un **pivote**, pon a la izquierda los menores y a la derecha los mayores (**partición**), y ordena cada lado recursivamente. En promedio O(n log n) y muy rápido en la práctica (trabaja in-place, buena caché); en el peor caso (pivote siempre el mínimo o el máximo, por ejemplo el primero en un array ya ordenado) es **O(n²)**. Por eso se elige el pivote **al azar** o con "mediana de tres".

```python
import random

def quicksort(a):
    """Versión clara (no in-place) para entender la idea."""
    if len(a) <= 1:
        return a
    pivote = random.choice(a)                       # pivote aleatorio: evita el peor caso
    menores = [x for x in a if x < pivote]
    iguales = [x for x in a if x == pivote]         # maneja muchos repetidos
    mayores = [x for x in a if x > pivote]
    return quicksort(menores) + iguales + quicksort(mayores)

def quicksort_inplace(a, lo=0, hi=None):
    """Partición de Lomuto: O(log n) de espacio extra en promedio."""
    if hi is None:
        hi = len(a) - 1
    if lo < hi:
        r = random.randint(lo, hi)
        a[r], a[hi] = a[hi], a[r]                   # pivote aleatorio al final
        pivote, i = a[hi], lo
        for j in range(lo, hi):
            if a[j] < pivote:
                a[i], a[j] = a[j], a[i]
                i += 1
        a[i], a[hi] = a[hi], a[i]                   # pivote a su sitio definitivo
        quicksort_inplace(a, lo, i - 1)
        quicksort_inplace(a, i + 1, hi)
    return a

print(quicksort([3, 6, 8, 10, 1, 2, 1]))            # [1, 1, 2, 3, 6, 8, 10]
print(quicksort_inplace([3, 6, 8, 10, 1, 2, 1]))    # [1, 1, 2, 3, 6, 8, 10]
```

### ⛰️ Heap sort y 🔢 counting sort

```python
import heapq

def heap_sort(a):
    h = a[:]
    heapq.heapify(h)                                # O(n)
    return [heapq.heappop(h) for _ in range(len(h))]   # n × O(log n)

def counting_sort(edades, maximo=120):
    """Para enteros en un rango pequeño [0, k]: O(n + k), sin comparar."""
    conteo = [0] * (maximo + 1)
    for e in edades:
        conteo[e] += 1
    res = []
    for valor, veces in enumerate(conteo):
        res.extend([valor] * veces)
    return res

print(heap_sort([5, 2, 9, 1, 5, 6]))                # [1, 2, 5, 5, 6, 9]
print(counting_sort([25, 19, 31, 19, 22, 25]))      # [19, 19, 22, 25, 25, 31]
```

### 🐍 Lo que usa Python: Timsort

🧠 Concepto: **Timsort** (Tim Peters, 2002, creado para CPython) es un híbrido de **merge sort + insertion sort**. Detecta tramos ya ordenados en los datos (**runs**, ascendentes o descendentes), alarga los cortos con insertion sort y los mezcla con merge inteligente ("galloping"). Con datos reales —que suelen venir parcialmente ordenados— es rapidísimo: O(n) si ya están ordenados.

```tiempo
2002 : Tim Peters crea Timsort para CPython
2011 : Java 7 lo usa para ordenar objetos (Arrays.sort)
2018 : V8 (Chrome, Node) cambia Array.prototype.sort a Timsort
2022 : Python 3.11 adopta la política de mezcla Powersort
```

```python
alumnos = [("Rosa", 85), ("Ana", 92), ("Luis", 85), ("Eva", 92), ("Juan", 70)]

# Estable: los que empatan conservan el orden de entrada
por_nota = sorted(alumnos, key=lambda a: a[1], reverse=True)
print(por_nota)
# [('Ana', 92), ('Eva', 92), ('Rosa', 85), ('Luis', 85), ('Juan', 70)]

# Varios criterios: nota descendente y, si empatan, nombre ascendente
print(sorted(alumnos, key=lambda a: (-a[1], a[0])))
# [('Ana', 92), ('Eva', 92), ('Luis', 85), ('Rosa', 85), ('Juan', 70)]
```

| Lenguaje | Ordenamiento por defecto |
|---|---|
| Python `sorted` / `list.sort` | Timsort (estable) |
| Java `Arrays.sort` objetos / primitivos | Timsort (estable) / Dual-Pivot Quicksort |
| JavaScript (V8) `Array.prototype.sort` | Timsort (estable; la especificación exige estable desde ES2019) |
| C++ `std::sort` / `std::stable_sort` | Introsort (no estable) / merge sort |
| Rust `sort` / `sort_unstable` | Estable (híbrido tipo merge) / no estable (quicksort híbrido) |

⚠️ Cuidado: no implementes tu propio sort en producción: el de la librería está optimizado en C y probado durante décadas. Implementarlo es para aprender y para entrevistas.

🇬🇧 **sorting** = ordenamiento · **stable** /stéibol/ = estable · **in-place** = en el sitio (sin copia) · **pivot** /pívot/ = pivote · **merge** /merch/ = mezclar · **run** = tramo ordenado · **key function** = función clave

## 🧰 Técnicas: two pointers, sliding window y prefix sums

Estas tres técnicas convierten muchos O(n²) "de fuerza bruta" en **O(n)**. La idea común: no recalcular desde cero, sino **reutilizar** el trabajo del paso anterior.

### 👉👈 Two pointers (dos punteros)

Dos índices que se mueven por el array según una regla. Variantes: **extremos que se acercan** (array ordenado, palíndromos) y **lento/rápido** (compactar en el sitio, ciclos).

```python
def par_suma_ordenado(nums, objetivo):
    """nums ORDENADO. O(n) tiempo, O(1) espacio (LeetCode 167)."""
    izq, der = 0, len(nums) - 1
    while izq < der:
        s = nums[izq] + nums[der]
        if s == objetivo:
            return izq, der
        if s < objetivo:
            izq += 1          # necesito más: muevo el pequeño
        else:
            der -= 1          # me pasé: muevo el grande
    return None

def es_palindromo(s):
    limpio = [c.lower() for c in s if c.isalnum()]
    i, j = 0, len(limpio) - 1
    while i < j:
        if limpio[i] != limpio[j]:
            return False
        i, j = i + 1, j - 1
    return True

def quitar_duplicados(nums):
    """nums ORDENADO; compacta en el sitio. Devuelve la nueva longitud (LeetCode 26)."""
    if not nums:
        return 0
    lento = 0
    for rapido in range(1, len(nums)):
        if nums[rapido] != nums[lento]:
            lento += 1
            nums[lento] = nums[rapido]
    return lento + 1

print(par_suma_ordenado([1, 3, 4, 6, 9], 10))          # (0, 4)
print(es_palindromo("Anita lava la tina"))             # True
a = [1, 1, 2, 3, 3, 3, 7]
k = quitar_duplicados(a)
print(k, a[:k])                                        # 4 [1, 2, 3, 7]
```

### 🪟 Sliding window (ventana deslizante)

Para problemas de **subarrays/substrings contiguos**. En vez de recalcular cada ventana (O(n·k)), al deslizar **sumas el que entra y restas el que sale**.

```flujo
V1 -> V2 : + entra a[3], − sale a[0]
V2 -> V3 : + entra a[4], − sale a[1]
V3 -> V4 : ...
```

```python
def max_suma_ventana(nums, k):
    """Ventana FIJA de tamaño k: O(n)."""
    actual = sum(nums[:k])
    mejor = actual
    for i in range(k, len(nums)):
        actual += nums[i] - nums[i - k]     # entra uno, sale otro
        mejor = max(mejor, actual)
    return mejor

def subcadena_sin_repetir(s):
    """Ventana VARIABLE: la más larga sin caracteres repetidos (LeetCode 3)."""
    ultima_vez = {}
    inicio = mejor = 0
    for fin, c in enumerate(s):
        if c in ultima_vez and ultima_vez[c] >= inicio:
            inicio = ultima_vez[c] + 1      # encoge la ventana por la izquierda
        ultima_vez[c] = fin
        mejor = max(mejor, fin - inicio + 1)
    return mejor

ventas = [2, 1, 5, 1, 3, 2]
print(max_suma_ventana(ventas, 3))            # 9   (5 + 1 + 3)
print(subcadena_sin_repetir("abcabcbb"))      # 3   ("abc")
print(subcadena_sin_repetir("pwwkew"))        # 3   ("wke")
```

💡 Consejo: plantilla de ventana variable: **expande `fin` siempre**; mientras la ventana sea inválida, **encoge `inicio`**; actualiza la mejor respuesta. Cada índice entra y sale una sola vez → O(n).

### ➕ Prefix sums (sumas prefijas)

Precalcula `pref[i] = a[0] + ... + a[i-1]`. Luego la suma de cualquier rango `[i, j)` es `pref[j] − pref[i]` en **O(1)**.

```python
from itertools import accumulate

ventas = [3, 1, 4, 1, 5, 9, 2, 6]
pref = [0] + list(accumulate(ventas))
print(pref)                   # [0, 3, 4, 8, 9, 14, 23, 25, 31]
print(pref[6] - pref[2])      # 19 → ventas[2:6] = 4 + 1 + 5 + 9

def subarrays_que_suman_k(nums, k):
    """Cuántos subarrays suman k (LeetCode 560). O(n) con prefijos + dict."""
    cuenta, suma, vistos = 0, 0, {0: 1}
    for x in nums:
        suma += x
        cuenta += vistos.get(suma - k, 0)   # ¿algún prefijo anterior deja exactamente k?
        vistos[suma] = vistos.get(suma, 0) + 1
    return cuenta

print(subarrays_que_suman_k([1, 2, 3, -2, 2], 3))   # 4
```

| Técnica | Señal en el enunciado | De → a |
|---|---|---|
| Two pointers | Array **ordenado**, pares, palíndromo, "en el sitio" | O(n²) → O(n) |
| Sliding window | Subarray/substring **contiguo**, "el más largo/corto que…" | O(n·k) → O(n) |
| Prefix sums | Muchas consultas de **suma de rangos** | O(n) por consulta → O(1) |

🇬🇧 **two pointers** = dos punteros · **sliding window** /sláiding uíndou/ = ventana deslizante · **prefix sum** = suma prefija · **subarray** = subarreglo contiguo · **in-place** = sin memoria extra

## ⚔️ Divide y vencerás, backtracking y greedy

### ✂️ Divide y vencerás

🧠 Concepto: **divide y vencerás** parte el problema en subproblemas **independientes** del mismo tipo, los resuelve recursivamente y **combina** sus respuestas. Ejemplos: merge sort, quicksort, búsqueda binaria, multiplicación de Karatsuba, la FFT (procesamiento de audio, señales).

```flujo
Problema -> Dividir
Dividir -> Sub1 : mitad izq
Dividir -> Sub2 : mitad der
Sub1 -> Combinar : resuelto
Sub2 -> Combinar : resuelto
Combinar -> Solución
```

```python
def potencia_rapida(base, exp):
    """base^exp en O(log exp): x^10 = (x^5)^2, x^5 = x · (x^2)^2."""
    if exp == 0:
        return 1
    mitad = potencia_rapida(base, exp // 2)   # un solo subproblema de la mitad
    if exp % 2 == 0:
        return mitad * mitad
    return mitad * mitad * base

print(potencia_rapida(2, 10))              # 1024
print(potencia_rapida(3, 13))              # 1594323
print(pow(7, 128, 1000))                   # 801 — Python ya lo hace (con módulo, base de RSA)
```

💡 Consejo: para saber la complejidad de un divide y vencerás piensa en el **árbol de recursión**: merge sort tiene log n niveles y en cada nivel se trabaja O(n) → O(n log n). Formalmente se usa el **teorema maestro**: T(n) = a·T(n/b) + f(n).

### 🔙 Backtracking (vuelta atrás)

🧠 Concepto: **backtracking** construye una solución paso a paso, probando una opción; si lleva a un callejón sin salida, **deshace** la última elección y prueba otra. Es un DFS sobre el árbol de decisiones, con **poda** (cortar ramas que ya no pueden dar solución).

```arbol
[ ]
  [1]
    [1, 2]
      [1, 2, 3] ✅
    [1, 3]
      [1, 3, 2] ✅
  [2]
    [2, 1]
      [2, 1, 3] ✅
    [2, 3]
      [2, 3, 1] ✅
  [3]
    ... (2 permutaciones más)
```

```python
def permutaciones(nums):
    res, camino, usados = [], [], set()
    def bt():
        if len(camino) == len(nums):          # solución completa
            res.append(camino[:])             # ¡copia! camino se seguirá modificando
            return
        for x in nums:
            if x in usados:
                continue
            camino.append(x); usados.add(x)   # 1. elegir
            bt()                              # 2. explorar
            camino.pop(); usados.remove(x)    # 3. deshacer (backtrack)
    bt()
    return res

def subconjuntos_que_suman(nums, objetivo):
    """Combinaciones que suman objetivo, con poda (nums positivos)."""
    nums = sorted(nums)
    res = []
    def bt(inicio, camino, resto):
        if resto == 0:
            res.append(camino[:])
            return
        for i in range(inicio, len(nums)):
            if nums[i] > resto:
                break                         # PODA: los siguientes son aún mayores
            camino.append(nums[i])
            bt(i + 1, camino, resto - nums[i])
            camino.pop()
    bt(0, [], objetivo)
    return res

def n_reinas(n):
    """Cuántas formas de poner n reinas sin que se ataquen."""
    cols, diag1, diag2 = set(), set(), set()
    def bt(fila):
        if fila == n:
            return 1
        total = 0
        for c in range(n):
            if c in cols or fila - c in diag1 or fila + c in diag2:
                continue                      # poda: esa casilla está atacada
            cols.add(c); diag1.add(fila - c); diag2.add(fila + c)
            total += bt(fila + 1)
            cols.remove(c); diag1.remove(fila - c); diag2.remove(fila + c)
        return total
    return bt(0)

print(permutaciones([1, 2, 3]))
# [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
print(subconjuntos_que_suman([10, 1, 2, 7, 6, 5], 8))
# [[1, 2, 5], [1, 7], [2, 6]]
print(n_reinas(8))     # 92
```

⚠️ Cuidado: backtracking es **exponencial** (O(n!) en permutaciones, O(2ⁿ) en subconjuntos). Solo sirve con n pequeño (~≤ 20) o con mucha poda. Ejemplos reales: resolver sudokus, solucionadores SAT, generar horarios.

### 🤑 Greedy (voraz)

🧠 Concepto: un algoritmo **greedy** toma en cada paso la decisión **localmente mejor** sin volver atrás. Es rápido y simple, pero **solo es correcto** cuando el problema tiene la propiedad de que la mejor elección local lleva a la óptima global (hay que demostrarlo o conocer el resultado).

```python
def max_actividades(actividades):
    """Selección de actividades: elegir la que TERMINA antes (greedy correcto)."""
    elegidas, fin_actual = [], float("-inf")
    for inicio, fin, nombre in sorted(actividades, key=lambda a: a[1]):
        if inicio >= fin_actual:
            elegidas.append(nombre)
            fin_actual = fin
    return elegidas

clases = [(8, 10, "Cálculo"), (9, 11, "Física"), (10, 12, "Algoritmos"),
          (11, 13, "Inglés"), (12, 14, "IA")]
print(max_actividades(clases))   # ['Cálculo', 'Algoritmos', 'IA']

def cambio_greedy(monto, monedas):
    usadas = []
    for m in sorted(monedas, reverse=True):
        while monto >= m:
            monto -= m
            usadas.append(m)
    return usadas

print(cambio_greedy(8, [5, 2, 1]))     # [5, 2, 1] → 3 monedas ✅ óptimo
print(cambio_greedy(6, [4, 3, 1]))     # [4, 1, 1] → 3 monedas ❌ lo óptimo es [3, 3]
```

::: columnas
### ✅ Greedy SÍ funciona
- Selección de actividades (la que termina antes)
- Dijkstra (pesos ≥ 0)
- Kruskal y Prim (árbol de expansión mínima)
- Códigos de Huffman (compresión)
- Monedas en sistemas "canónicos" (como 1, 2, 5, 10...)
::: siguiente
### ❌ Greedy NO funciona
- Monedas arbitrarias (`[4, 3, 1]` para 6)
- Mochila 0/1 (no puedes partir objetos)
- Camino más corto con pesos negativos
- Viajante (TSP): el vecino más cercano no es óptimo
- → Usa **programación dinámica** o búsqueda
:::

🇬🇧 **divide and conquer** = divide y vencerás · **backtracking** = vuelta atrás · **pruning** /prúning/ = poda · **greedy** /grídi/ = voraz · **locally optimal** = óptimo local · **counterexample** = contraejemplo

## 🧩 Programación dinámica

🧠 Concepto: la **programación dinámica** (DP) resuelve problemas cuyos subproblemas **se repiten** (subproblemas solapados) y cuya solución óptima se construye con soluciones óptimas de subproblemas (**subestructura óptima**). La idea: **resolver cada subproblema una sola vez y guardar la respuesta**.

Diferencia con divide y vencerás: allí los subproblemas son **independientes** (merge sort no repite trabajo); en DP se **repiten** muchísimo, y guardarlos convierte algo exponencial en polinómico.

### 🐇 Fibonacci: del desastre a O(n)

```arbol
fib(5)
  fib(4)
    fib(3)
      fib(2)
      fib(1)
    fib(2)
  fib(3)  ← se repite
    fib(2)  ← se repite
    fib(1)
```

```python
from functools import cache
import time

def fib_ingenuo(n):                 # O(2^n): recalcula lo mismo millones de veces
    return n if n < 2 else fib_ingenuo(n - 1) + fib_ingenuo(n - 2)

@cache                              # MEMOIZACIÓN (top-down): recursión + caché
def fib_memo(n):
    return n if n < 2 else fib_memo(n - 1) + fib_memo(n - 2)

def fib_tabla(n):                   # TABULACIÓN (bottom-up): llena una tabla de abajo a arriba
    if n < 2:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]

def fib_optimo(n):                  # solo necesito los 2 anteriores → O(1) espacio
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

t0 = time.perf_counter(); r = fib_ingenuo(30); t1 = time.perf_counter()
print(r, f"ingenuo: {t1 - t0:.2f} s")      # 832040 ingenuo: ~0.1 s (unas 2,7 millones de llamadas)
print(fib_memo(30), fib_tabla(30), fib_optimo(30))   # 832040 832040 832040
print(fib_optimo(100))                     # 354224848179261915075
```

::: columnas
### ⬇️ Memoización (top-down)
- Escribes la recursión natural y añades caché (`@cache`).
- Solo calcula los subproblemas que se necesitan.
- Fácil de pensar.
- Riesgo: `RecursionError` con n grande.
::: siguiente
### ⬆️ Tabulación (bottom-up)
- Llenas una tabla en orden, de los casos pequeños a los grandes.
- Sin recursión: sin límite de pila.
- Permite **optimizar espacio** (guardar solo la última fila).
- Hay que pensar bien el orden.
:::

### 🪜 Los 5 pasos para cualquier DP

1. **Estado**: ¿qué significa `dp[i]` (o `dp[i][j]`)? Escríbelo en una frase.
2. **Transición**: ¿cómo se calcula `dp[i]` a partir de estados más pequeños?
3. **Casos base**: los valores que se saben sin calcular.
4. **Orden**: en qué orden llenar para que lo necesario ya esté calculado.
5. **Respuesta**: qué celda (o el máximo de cuáles) es la solución.

### 🎒 Mochila 0/1

Tienes una mochila de capacidad W y objetos con peso y valor. Cada objeto se lleva **entero o no se lleva**. Maximiza el valor.

- **Estado**: `dp[i][w]` = mejor valor usando los primeros `i` objetos con capacidad `w`.
- **Transición**: no llevar el objeto i → `dp[i-1][w]`; llevarlo (si cabe) → `valor_i + dp[i-1][w - peso_i]`. Me quedo con el máximo.

```python
def mochila(pesos, valores, W):
    n = len(pesos)
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        p, v = pesos[i - 1], valores[i - 1]
        for w in range(W + 1):
            dp[i][w] = dp[i - 1][w]                       # no lo llevo
            if p <= w:
                dp[i][w] = max(dp[i][w], v + dp[i - 1][w - p])   # lo llevo
    # reconstruir qué objetos se eligieron
    elegidos, w = [], W
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            elegidos.append(i - 1)
            w -= pesos[i - 1]
    return dp[n][W], sorted(elegidos), dp

objetos = ["laptop", "cámara", "libro", "audífonos"]
pesos   = [3, 2, 1, 1]          # kg
valores = [2000, 800, 150, 300] # Bs (ilustrativo)
mejor, idx, dp = mochila(pesos, valores, 4)
print(mejor, [objetos[i] for i in idx])     # 2300 ['laptop', 'audífonos']
for fila in dp:
    print(fila)
# [0, 0, 0, 0, 0]
# [0, 0, 0, 2000, 2000]
# [0, 0, 800, 2000, 2000]
# [0, 150, 800, 2000, 2150]
# [0, 300, 800, 2000, 2300]
```

| i \ capacidad | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| sin objetos | 0 | 0 | 0 | 0 | 0 |
| + laptop (3 kg, 2000) | 0 | 0 | 0 | 2000 | 2000 |
| + cámara (2 kg, 800) | 0 | 0 | 800 | 2000 | 2000 |
| + libro (1 kg, 150) | 0 | 150 | 800 | 2000 | 2150 |
| + audífonos (1 kg, 300) | 0 | 300 | 800 | 2000 | **2300** |

Complejidad: **O(n · W)** tiempo y espacio (reducible a O(W) con una sola fila recorrida de derecha a izquierda). Ojo: es "pseudo-polinómico": si W es enorme (10⁹), la tabla no cabe.

### 🧬 LCS: subsecuencia común más larga

La **LCS** (Longest Common Subsequence) es la base de `diff` y de `git diff` (qué líneas se mantienen entre dos versiones), y de la comparación de secuencias de ADN en bioinformática.

- **Estado**: `dp[i][j]` = LCS de los primeros `i` caracteres de A y los primeros `j` de B.
- **Transición**: si `A[i-1] == B[j-1]` → `dp[i-1][j-1] + 1` (diagonal + 1); si no → `max(dp[i-1][j], dp[i][j-1])` (arriba o izquierda).

```python
def lcs(a, b):
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    # reconstruir la subsecuencia caminando hacia atrás
    res, i, j = [], m, n
    while i and j:
        if a[i - 1] == b[j - 1]:
            res.append(a[i - 1]); i -= 1; j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return dp[m][n], "".join(reversed(res)), dp

largo, sub, dp = lcs("ABCBDAB", "BDCABA")
print(largo, sub)     # 4 BCBA
```

Tabla de `lcs("ABCB", "BDCAB")` (filas = A, columnas = B):

| · | B | D | C | A | B |
|---|---|---|---|---|---|
| A | 0 | 0 | 0 | 1 | 1 |
| B | 1 | 1 | 1 | 1 | 2 |
| C | 1 | 1 | 2 | 2 | 2 |
| B | 1 | 1 | 2 | 2 | **3** |

LCS = 3 ("BCB"). Cada celda mira **diagonal** (si las letras coinciden), **arriba** e **izquierda**.

### 🗺️ Problemas DP clásicos

| Problema | Estado | Complejidad |
|---|---|---|
| Subir escaleras (1 o 2 pasos) | `dp[i]` = formas de llegar al escalón i | O(n) |
| Robar casas sin adyacentes | `dp[i]` = máximo hasta la casa i | O(n) |
| Cambio de monedas (mínimo) | `dp[x]` = mínimas monedas para x | O(x · monedas) |
| Subsecuencia creciente más larga | `dp[i]` = LIS que termina en i | O(n²) o O(n log n) |
| Distancia de edición (Levenshtein) | `dp[i][j]` = ediciones para A[:i] → B[:j] | O(m · n) |
| Caminos en una cuadrícula | `dp[f][c]` = caminos hasta (f, c) | O(filas · cols) |

💡 Consejo: Señales de DP en un enunciado: "**número de formas**", "**mínimo/máximo** de...", "¿es **posible**...?", con elecciones que se repiten. Si el greedy tiene un contraejemplo, prueba DP.

🇬🇧 **dynamic programming** = programación dinámica · **memoization** /memoaiséishon/ = memoización · **tabulation** = tabulación · **overlapping subproblems** = subproblemas solapados · **optimal substructure** = subestructura óptima · **knapsack** /nápsak/ = mochila · **longest common subsequence** = subsecuencia común más larga

## 💡 Manipulación de bits

Los enteros son bits; operar directamente sobre ellos es O(1) y muy rápido. Aparece en permisos (`chmod 755`), flags, máscaras de red, compresión, hashing, gráficos y en preguntas de entrevista.

- `a & b` :: AND: 1 si ambos son 1 (apagar bits, máscaras)
- `a | b` :: OR: 1 si alguno es 1 (encender bits)
- `a ^ b` :: XOR: 1 si son distintos (`x ^ x = 0`, `x ^ 0 = x`)
- `~a` :: NOT: invierte todos los bits (en Python `~a == -a - 1`)
- `a << k` :: Desplaza a la izquierda = multiplicar por 2ᵏ
- `a >> k` :: Desplaza a la derecha = división entera por 2ᵏ
- `n & 1` :: ¿Es impar? (último bit)
- `n & (n - 1)` :: Apaga el bit 1 más bajo; `== 0` → es potencia de 2
- `(n >> k) & 1` :: ¿Está encendido el bit k?
- `n.bit_count()` :: Cuántos bits a 1 (Python 3.10+)

```python
print(bin(13), bin(13 & 6), bin(13 | 6), bin(13 ^ 6))
# 0b1101 0b100 0b1111 0b1011

def es_potencia_de_2(n):
    return n > 0 and n & (n - 1) == 0      # 8 = 1000, 7 = 0111 → AND = 0

def numero_solitario(nums):
    """Todos aparecen 2 veces menos uno (LeetCode 136). XOR cancela los pares."""
    res = 0
    for x in nums:
        res ^= x
    return res

def subconjuntos_con_bits(items):
    """Cada número de 0 a 2^n - 1 es una máscara: bit i = ¿incluyo items[i]?"""
    n = len(items)
    return [[items[i] for i in range(n) if mask >> i & 1] for mask in range(1 << n)]

# Permisos estilo Unix con flags
LEER, ESCRIBIR, EJECUTAR = 4, 2, 1
permiso = LEER | EJECUTAR                 # 5 = r-x
print(es_potencia_de_2(64), es_potencia_de_2(48))   # True False
print(numero_solitario([4, 1, 2, 1, 2]))            # 4
print(subconjuntos_con_bits(["a", "b", "c"]))
# [[], ['a'], ['b'], ['a', 'b'], ['c'], ['a', 'c'], ['b', 'c'], ['a', 'b', 'c']]
print(bool(permiso & ESCRIBIR), (37).bit_count())   # False 3
```

⚠️ Cuidado: en JavaScript los operadores de bits convierten los números a **enteros de 32 bits con signo**: `2**31 | 0` da `-2147483648`. Para enteros grandes usa `BigInt` (`1n << 40n`). En Python los enteros no tienen límite, pero `~` y los negativos usan complemento a dos "infinito", lo que confunde al principio.

🇬🇧 **bitwise** /bítuais/ = a nivel de bits · **mask** = máscara · **shift** = desplazamiento · **flag** = indicador · **two's complement** = complemento a dos · **set / clear a bit** = encender / apagar un bit

## 🎤 Cómo resolver un problema de entrevista y patrones de LeetCode

En una entrevista técnica no solo evalúan si llegas a la respuesta: evalúan **cómo piensas, cómo comunicas y cómo pruebas**. Callarte 20 minutos y escribir la solución perfecta puntúa peor que razonar en voz alta.

```flujo
dir: abajo
Entender -> Ejemplos : repite el enunciado, pregunta
Ejemplos -> Bruta : casos borde
Bruta -> Optimizar : di su Big O
Optimizar -> Codificar : ¿qué estructura ayuda?
Codificar -> Probar : nombres claros
Probar -> Complejidad : recorre un ejemplo a mano
Complejidad -> Mejoras : tiempo y espacio
```

1. **Entender** (2–3 min): repite el problema con tus palabras. Pregunta: ¿puede estar vacío? ¿hay negativos o repetidos? ¿tamaño de n? ¿está ordenado? ¿qué devuelvo si no hay respuesta?
2. **Ejemplos**: escribe uno normal y uno borde (vacío, un elemento, todos iguales).
3. **Fuerza bruta**: dila en voz alta con su complejidad, aunque no la programes. Demuestra que entiendes el problema.
4. **Optimizar**: ¿qué trabajo se repite? Busca el patrón: ¿un hash evita la búsqueda? ¿ordenar ayuda? ¿ventana? ¿DP?
5. **Codificar**: limpio, funciones pequeñas, nombres claros. Narra lo que haces.
6. **Probar**: recorre tu ejemplo línea a línea (la "traza"), luego los casos borde.
7. **Complejidad**: tiempo y espacio, y qué cambiarías si n fuera 1000× mayor.

💡 Consejo: el tamaño de n te chiva la complejidad esperada: n ≤ 20 → backtracking/bitmask; n ≤ 10³ → O(n²); n ≤ 10⁵–10⁶ → O(n log n) u O(n); n ≤ 10⁹ o "muy grande" → O(log n) u O(1) (búsqueda binaria, matemáticas).

### 🧩 Patrones más frecuentes

| Patrón | Señal | Problema tipo (LeetCode) |
|---|---|---|
| Hash map | "¿existe…?", contar, agrupar | Two Sum (1), Group Anagrams (49) |
| Two pointers | Array ordenado, pares, palíndromo | Container With Most Water (11), 3Sum (15) |
| Sliding window | Subarray/substring contiguo | Longest Substring Without Repeating (3), Minimum Window Substring (76) |
| Prefix sum | Sumas de rangos, subarrays que suman k | Subarray Sum Equals K (560) |
| Pila monótona | "Siguiente mayor/menor" | Daily Temperatures (739), Largest Rectangle (84) |
| Búsqueda binaria | Ordenado o respuesta monótona | Search in Rotated Array (33), Koko Eating Bananas (875) |
| Lista enlazada (rápido/lento) | Ciclos, mitad, invertir | Linked List Cycle (141), Reverse Linked List (206) |
| Árbol DFS/BFS | Altura, caminos, niveles | Max Depth (104), Level Order (102), LCA (236) |
| Grafo BFS/DFS | Islas, conexiones, camino mínimo | Number of Islands (200), Rotting Oranges (994) |
| Orden topológico | Dependencias, prerrequisitos | Course Schedule (207) |
| Heap / top-k | "Los k mayores", mezclar k listas | Kth Largest (215), Merge k Sorted Lists (23) |
| Intervalos | Solapamientos, agendas | Merge Intervals (56), Meeting Rooms II (253) |
| Backtracking | Todas las combinaciones | Subsets (78), Permutations (46), N-Queens (51) |
| DP 1D / 2D | Contar formas, mín/máx | Climbing Stairs (70), Coin Change (322), LCS (1143) |
| Union-Find | Grupos, conectividad dinámica | Number of Provinces (547), Redundant Connection (684) |
| Trie | Prefijos, diccionario de palabras | Implement Trie (208), Word Search II (212) |

### ✅ Ejemplo resuelto con el método: pila monótona

**Problema** (LeetCode 739): para cada día, ¿cuántos días hay que esperar a una temperatura más alta? (0 si nunca).

- **Fuerza bruta**: para cada día, mirar hacia adelante → O(n²).
- **Observación**: los días "pendientes" de respuesta forman una pila con temperaturas **decrecientes**. Cuando llega un día más caliente, resuelve a todos los más fríos de la cima.

```python
def dias_hasta_mas_calor(temps):
    res = [0] * len(temps)
    pila = []                                  # índices con temperaturas decrecientes
    for i, t in enumerate(temps):
        while pila and temps[pila[-1]] < t:    # hoy es más caliente que esos días
            j = pila.pop()
            res[j] = i - j
        pila.append(i)
    return res

print(dias_hasta_mas_calor([73, 74, 75, 71, 69, 72, 76, 73]))
# [1, 1, 4, 2, 1, 1, 0, 0]
```

Complejidad: **O(n)** aunque haya un `while` dentro del `for`: cada índice entra y sale de la pila **una sola vez** (análisis amortizado). Espacio O(n).

🇬🇧 **brute force** = fuerza bruta · **trade-off** /tréid of/ = compromiso, intercambio · **dry run / trace** = traza a mano · **follow-up question** = pregunta de seguimiento · **constraints** /konstréints/ = restricciones · **"Can I assume...?"** = ¿puedo asumir...?

## 🌍 Herramientas, comparativa y futuro

### 🧰 Qué usar en cada lenguaje (no reinventes la rueda)

| Necesito | Python | JavaScript | Java | C++ |
|---|---|---|---|---|
| Array dinámico | `list` | `Array` | `ArrayList` | `vector` |
| Hash map / set | `dict` / `set` | `Map` / `Set` | `HashMap` / `HashSet` | `unordered_map` / `unordered_set` |
| Mapa ordenado | `sortedcontainers` (externo) | — (no nativo) | `TreeMap` | `map` |
| Pila | `list` | `Array` (`push`/`pop`) | `ArrayDeque` | `stack` |
| Cola / deque | `collections.deque` | — (array + índice) | `ArrayDeque` | `deque` |
| Heap | `heapq` | — (no nativo) | `PriorityQueue` | `priority_queue` |
| Búsqueda binaria | `bisect` | — (manual) | `Collections.binarySearch` | `lower_bound` |
| Memoización | `functools.cache` | — (manual con `Map`) | — (manual) | — (manual) |

📌 Resumen: Python y C++ son los favoritos en entrevistas y programación competitiva: Python por ser corto (`heapq`, `Counter`, `deque`, `bisect` y `cache` ya vienen); C++ por velocidad (en concursos con límites de tiempo ajustados) y su STL completa. JavaScript se queda corto: no trae heap ni deque y te toca implementarlos.

| Librería | Para qué |
|---|---|
| `collections`, `heapq`, `bisect`, `itertools`, `functools`, `graphlib` | Librería estándar de Python: lo básico de esta hoja |
| `networkx` | Grafos en Python: Dijkstra, PageRank, componentes, flujo |
| `numpy` | Arrays contiguos y vectorizados (operaciones en C, mucho más rápidas que bucles) |
| `sortedcontainers` | Lista/dict/set ordenados en Python puro, muy usado |
| `scipy.sparse.csgraph` | Algoritmos de grafos sobre matrices dispersas grandes |

### 🚀 Ecosistema y futuro

```tiempo
1945 : von Neumann describe merge sort
1956 : Dijkstra inventa su algoritmo de caminos mínimos
1959 : Tony Hoare inventa quicksort
1968 : Knuth publica el primer tomo de The Art of Computer Programming
2002 : Timsort en CPython
2023 : AlphaDev (DeepMind) mejora rutinas de ordenar pocos elementos (en libc++)
2025 : AlphaEvolve (DeepMind) usa LLMs para descubrir y mejorar algoritmos
```

🚀 Futuro: la IA ya **genera** código algorítmico (Copilot, Claude, ChatGPT) y hasta **descubre** algoritmos nuevos (AlphaDev, AlphaEvolve). Eso no hace inútil esta hoja: hace **más** valioso saber si el código que te da la IA es O(n²) escondido, si tiene un off-by-one o si usa la estructura equivocada. Quien entiende complejidad revisa y decide; quien no, copia y pega bugs a escala.

🚀 Futuro: tendencias a seguir: estructuras **conscientes de la caché** y del hardware (SIMD, GPU), **índices aprendidos** (modelos de ML que reemplazan partes de un B-tree, investigación desde 2018), **búsqueda vectorial aproximada** (HNSW, un grafo navegable usado en bases de datos vectoriales para RAG y embeddings), y algoritmos **probabilísticos** (Bloom filters, HyperLogLog en Redis) que cambian exactitud por memoria.

## 🐛 Errores de otros programadores y buenas prácticas

| Error | Causa | Consecuencia | Cómo evitarlo |
|---|---|---|---|
| `x in lista` dentro de un bucle | No saber que es O(n) | O(n²) oculto, endpoints lentos | Convierte a `set` antes del bucle |
| `lista.pop(0)` como cola | Desplaza todo | O(n) por operación | `collections.deque` |
| Concatenar strings en bucle (`s += x`) | Cada `+=` puede copiar | O(n²) en el peor caso | `"".join(partes)` |
| Lista mutable como valor por defecto | `def f(x, vistos=[])` se crea UNA vez | Estado compartido entre llamadas | `vistos=None` y créala dentro |
| `[[0] * m] * n` para una matriz | Copia la MISMA fila n veces | Cambiar una celda cambia toda la columna | `[[0] * m for _ in range(n)]` |
| Guardar `camino` sin copiar en backtracking | Se guarda la referencia | Resultados vacíos al final | `res.append(camino[:])` |
| Marcar visitado al SACAR en BFS | Un nodo se encola varias veces | Trabajo repetido, O(V²) | Marca al ENCOLAR |
| BST sin balancear con datos ordenados | El árbol degenera | O(n) en vez de O(log n) | Árbol balanceado / `sortedcontainers` |
| Recursión profunda en Python | Límite de ~1000 marcos | `RecursionError` | Pila explícita o iterativo |
| Dijkstra con pesos negativos | Greedy asume que no mejora después | Distancias erróneas | Bellman-Ford |
| Modificar un dict/lista mientras se recorre | Iterador inválido | `RuntimeError` o elementos saltados | Recorre una copia o construye otra |
| Optimizar sin medir | Intuición equivocada | Tiempo perdido, código feo | Perfila primero (`cProfile`, `timeit`) |

```python
# El error de la matriz compartida, en vivo
mal = [[0] * 3] * 3
mal[0][0] = 9
print(mal)      # [[9, 0, 0], [9, 0, 0], [9, 0, 0]]  ← ¡las 3 filas son la misma!

bien = [[0] * 3 for _ in range(3)]
bien[0][0] = 9
print(bien)     # [[9, 0, 0], [0, 0, 0], [0, 0, 0]]

# El error del valor por defecto mutable
def agregar(x, lista=[]):
    lista.append(x)
    return lista
print(agregar(1), agregar(2))   # [1, 2] [1, 2]  ← la lista sobrevive entre llamadas
```

### 🔥 Incidentes reales

- **Cloudflare, 2 de julio de 2019**: una regla nueva del WAF tenía una expresión regular con **backtracking catastrófico** (patrones como `.*.*=.*`). El motor de regex probaba un número enorme de combinaciones, la CPU de los servidores se fue al 100 % y gran parte del tráfico que pasaba por Cloudflare falló durante unos 27 minutos. Lección: las regex con backtracking pueden ser exponenciales; usa motores con tiempo lineal (RE2, el de Rust) para entradas no confiables y limita el tiempo de ejecución.
- **Stack Overflow, julio de 2016**: una regex para recortar espacios en blanco era cuadrática; un post con ~20 000 espacios seguidos tumbó la página principal unos 34 minutos. Mismo tipo de causa: un algoritmo que parecía inocente con entradas normales.
- **HashDoS (2011)**: colisiones forzadas en tablas hash convertían peticiones HTTP en O(n²) (ver la sección de tablas hash).
- **Bug de búsqueda binaria de Java (2006)**: desbordamiento en `(low + high) / 2` (ver la sección de búsqueda binaria).

📌 Resumen: los incidentes se repiten con el mismo patrón: un algoritmo con **peor caso** malo (cuadrático o exponencial) que nadie probó con la **entrada adversa** o grande. Pregúntate siempre: "¿qué entrada haría explotar esto?".

### ✅ Buenas prácticas

- **Primero correcto, luego rápido**: escribe la versión simple, con tests; optimiza solo lo que el perfilador señale.
- **Mide** con `timeit` y `cProfile`; la Big O dice cómo escala, no cuál es más rápido para n pequeño.
- **Usa la librería estándar** (`sorted`, `heapq`, `bisect`, `deque`, `Counter`): está escrita en C y probada.
- **Elige la estructura según la operación más frecuente**: ¿buscas mucho? hash. ¿necesitas orden? árbol/ordenado. ¿el mínimo? heap.
- **Prueba los casos borde**: vacío, un elemento, todos iguales, ya ordenado, al revés, muy grande, negativos.
- **Seguridad**: con datos del usuario, piensa en el peor caso (regex, hash, recursión profunda) para evitar ataques de denegación de servicio.
- **Mantenimiento**: un O(n log n) claro suele ser mejor que un O(n) ilegible si n es pequeño; documenta la complejidad en el docstring.

## 🏋️ Ejercicios (de fácil a difícil)

### 1️⃣ Fácil: ¿hay duplicados?

Devuelve `True` si algún número aparece más de una vez. Hazlo en O(n).

::: desplegable 🧩 Ver la solución
```python
def tiene_duplicados(nums):
    return len(set(nums)) != len(nums)      # O(n) tiempo, O(n) espacio

def tiene_duplicados_temprano(nums):
    vistos = set()
    for x in nums:
        if x in vistos:                     # sale en cuanto encuentra uno
            return True
        vistos.add(x)
    return False

print(tiene_duplicados([1, 2, 3, 1]), tiene_duplicados_temprano([1, 2, 3]))   # True False
```
Alternativa O(1) espacio: ordenar y comparar vecinos → O(n log n) tiempo.
:::

### 2️⃣ Fácil: ¿son anagramas?

¿Las palabras `"listen"` y `"silent"` tienen las mismas letras con las mismas cantidades?

::: desplegable 🧩 Ver la solución
```python
from collections import Counter

def son_anagramas(a, b):
    return Counter(a) == Counter(b)          # O(n)

print(son_anagramas("listen", "silent"), son_anagramas("rata", "tara"))
print(son_anagramas("hola", "halo"), son_anagramas("abc", "abd"))
# True True
# True False
```
`sorted(a) == sorted(b)` también funciona, pero es O(n log n).
:::

### 3️⃣ Fácil: máximo beneficio comprando y vendiendo una vez

Dados precios diarios, compra un día y vende otro posterior. Máximo beneficio (LeetCode 121).

::: desplegable 🧩 Ver la solución
```python
def max_beneficio(precios):
    minimo = float("inf")
    mejor = 0
    for p in precios:
        minimo = min(minimo, p)             # el día más barato hasta hoy
        mejor = max(mejor, p - minimo)      # ¿y si vendo hoy?
    return mejor

print(max_beneficio([7, 1, 5, 3, 6, 4]), max_beneficio([7, 6, 4, 3, 1]))   # 5 0
```
Una pasada, O(n) tiempo, O(1) espacio. Es un "greedy" sobre el mínimo visto.
:::

### 4️⃣ Medio: profundidad máxima de un árbol

Calcula la altura de un árbol binario, de forma recursiva y por niveles (BFS).

::: desplegable 🧩 Ver la solución
```python
from collections import deque

class N:
    def __init__(self, v, izq=None, der=None):
        self.v, self.izq, self.der = v, izq, der

def profundidad(n):
    return 0 if n is None else 1 + max(profundidad(n.izq), profundidad(n.der))

def profundidad_bfs(raiz):
    if not raiz:
        return 0
    cola, niveles = deque([raiz]), 0
    while cola:
        niveles += 1
        for _ in range(len(cola)):
            n = cola.popleft()
            cola.extend(h for h in (n.izq, n.der) if h)
    return niveles

arbol = N(3, N(9), N(20, N(15), N(7)))
print(profundidad(arbol), profundidad_bfs(arbol))   # 3 3
```
:::

### 5️⃣ Medio: mezclar intervalos

`[[1,3],[2,6],[8,10],[15,18]]` → `[[1,6],[8,10],[15,18]]` (LeetCode 56).

::: desplegable 🧩 Ver la solución
```python
def mezclar_intervalos(intervalos):
    res = []
    for ini, fin in sorted(intervalos):      # ordenar por inicio: O(n log n)
        if res and ini <= res[-1][1]:        # se solapa con el último
            res[-1][1] = max(res[-1][1], fin)
        else:
            res.append([ini, fin])
    return res

print(mezclar_intervalos([[1, 3], [2, 6], [8, 10], [15, 18]]))   # [[1, 6], [8, 10], [15, 18]]
print(mezclar_intervalos([[1, 4], [4, 5]]))                      # [[1, 5]]
```
Patrón clave: **ordenar primero** transforma un problema O(n²) de comparar todos contra todos en una sola pasada.
:::

### 6️⃣ Medio: k elementos más frecuentes

Devuelve los `k` valores más frecuentes (LeetCode 347). Mejor que O(n log n).

::: desplegable 🧩 Ver la solución
```python
from collections import Counter
import heapq

def top_k_frecuentes(nums, k):
    cuenta = Counter(nums)                                   # O(n)
    return heapq.nlargest(k, cuenta, key=cuenta.get)         # O(n log k)

def top_k_cubetas(nums, k):
    """Bucket sort por frecuencia: O(n)."""
    cuenta = Counter(nums)
    cubetas = [[] for _ in range(len(nums) + 1)]
    for valor, f in cuenta.items():
        cubetas[f].append(valor)
    res = []
    for f in range(len(cubetas) - 1, 0, -1):
        res.extend(cubetas[f])
        if len(res) >= k:
            return res[:k]
    return res

datos = [1, 1, 1, 2, 2, 3]
print(top_k_frecuentes(datos, 2), top_k_cubetas(datos, 2))   # [1, 2] [1, 2]
```
:::

### 7️⃣ Medio: cambio de monedas (mínimo número)

Monedas `[1, 3, 4]`, monto 6 → 2 (3 + 3). Si no se puede, -1 (LeetCode 322). Aquí el greedy falla.

::: desplegable 🧩 Ver la solución
```python
def cambio_minimo(monedas, monto):
    INF = float("inf")
    dp = [0] + [INF] * monto                 # dp[x] = mínimas monedas para formar x
    for x in range(1, monto + 1):
        for m in monedas:
            if m <= x and dp[x - m] + 1 < dp[x]:
                dp[x] = dp[x - m] + 1
    return dp[monto] if dp[monto] != INF else -1

print(cambio_minimo([1, 3, 4], 6), cambio_minimo([2], 3))   # 2 -1
print(cambio_minimo([1, 2, 5], 11))                         # 3
```
O(monto · monedas) tiempo, O(monto) espacio.
:::

### 8️⃣ Medio-difícil: ¿se pueden terminar todos los cursos?

`n` cursos y pares `[curso, prerrequisito]`. ¿Hay un ciclo? (LeetCode 207).

::: desplegable 🧩 Ver la solución
```python
from collections import deque

def puede_terminar(n, prerrequisitos):
    grafo = [[] for _ in range(n)]
    entrada = [0] * n
    for curso, previo in prerrequisitos:
        grafo[previo].append(curso)
        entrada[curso] += 1
    cola = deque(i for i in range(n) if entrada[i] == 0)
    terminados = 0
    while cola:
        c = cola.popleft()
        terminados += 1
        for sig in grafo[c]:
            entrada[sig] -= 1
            if entrada[sig] == 0:
                cola.append(sig)
    return terminados == n                   # si quedó alguno, hay ciclo

print(puede_terminar(2, [[1, 0]]), puede_terminar(2, [[1, 0], [0, 1]]))   # True False
```
Orden topológico (Kahn): O(V + E).
:::

### 9️⃣ Difícil: distancia de edición (Levenshtein)

Mínimo de inserciones, borrados o reemplazos para convertir `"gato"` en `"pato"`, o `"intention"` en `"execution"` (LeetCode 72). Base de correctores ortográficos.

::: desplegable 🧩 Ver la solución
```python
def distancia_edicion(a, b):
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i                          # borrar todo
    for j in range(n + 1):
        dp[0][j] = j                          # insertar todo
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]   # gratis
            else:
                dp[i][j] = 1 + min(dp[i - 1][j],      # borrar
                                   dp[i][j - 1],      # insertar
                                   dp[i - 1][j - 1])  # reemplazar
    return dp[m][n]

print(distancia_edicion("gato", "pato"), distancia_edicion("", "abc"))   # 1 3
print(distancia_edicion("intention", "execution"))                       # 5
```
O(m · n). Misma familia que LCS: cada celda mira arriba, izquierda y diagonal.
:::

### 🔟 Difícil: caché LRU con O(1)

Implementa `get(clave)` y `put(clave, valor)` en O(1); al superar la capacidad, expulsa la clave usada hace más tiempo (LeetCode 146).

::: desplegable 🧩 Ver la solución
```python
from collections import OrderedDict

class LRU:
    """OrderedDict = dict + lista doblemente enlazada por dentro."""
    def __init__(self, capacidad):
        self.cap = capacidad
        self.datos = OrderedDict()

    def get(self, clave):
        if clave not in self.datos:
            return -1
        self.datos.move_to_end(clave)        # recién usada → al final
        return self.datos[clave]

    def put(self, clave, valor):
        self.datos[clave] = valor
        self.datos.move_to_end(clave)
        if len(self.datos) > self.cap:
            self.datos.popitem(last=False)   # expulsa la más antigua (el inicio)

c = LRU(2)
c.put("a", 1); c.put("b", 2)
print(c.get("a"))      # 1   (ahora "b" es la menos reciente)
c.put("c", 3)          # expulsa "b"
print(c.get("b"), c.get("c"))   # -1 3
```
En una entrevista pueden pedirte hacerlo **sin** `OrderedDict`: un `dict` clave → nodo y una lista doblemente enlazada con centinelas al inicio y al final. `functools.lru_cache` de Python hace exactamente esto para memoizar funciones.
:::

### 1️⃣1️⃣ Difícil: la ventana mínima que contiene todas las letras

Dados `s = "ADOBECODEBANC"` y `t = "ABC"`, el substring más corto de `s` que contiene todas las letras de `t` es `"BANC"` (LeetCode 76).

::: desplegable 🧩 Ver la solución
```python
from collections import Counter

def ventana_minima(s, t):
    falta = Counter(t)
    pendientes = len(t)                       # letras que aún faltan cubrir
    inicio = 0
    mejor = (float("inf"), 0, 0)
    for fin, c in enumerate(s):
        if falta[c] > 0:
            pendientes -= 1
        falta[c] -= 1                         # puede quedar negativo: sobra
        while pendientes == 0:                # ventana válida → intenta encoger
            if fin - inicio + 1 < mejor[0]:
                mejor = (fin - inicio + 1, inicio, fin + 1)
            falta[s[inicio]] += 1
            if falta[s[inicio]] > 0:
                pendientes += 1               # quitamos una letra necesaria
            inicio += 1
    return s[mejor[1]:mejor[2]] if mejor[0] != float("inf") else ""

print(ventana_minima("ADOBECODEBANC", "ABC"), repr(ventana_minima("a", "aa")))   # BANC ''
```
Ventana variable: O(|s| + |t|).
:::

## 💼 Preguntas de entrevista

::: desplegable ❓ ¿Qué es Big O y por qué se ignoran las constantes?
Describe cómo crece el coste (tiempo o memoria) cuando n crece, en el peor caso. Se ignoran constantes porque dependen del hardware y del lenguaje, mientras que la forma de la curva (lineal vs cuadrática) domina para n grande. En la práctica las constantes sí importan para n pequeño, por eso se mide.
:::

::: desplegable ❓ ¿Por qué el acceso a un dict es O(1) y cuándo no lo es?
La función hash calcula directamente la cubeta, sin recorrer. Es O(1) **en promedio**; en el peor caso (muchas colisiones, o ataques HashDoS) degenera a O(n). El redimensionado es O(n) puntual pero O(1) amortizado.
:::

::: desplegable ❓ Array vs lista enlazada: ¿cuándo usar cada uno?
Array: acceso por índice O(1), excelente caché, append amortizado O(1); lo normal. Lista enlazada: insertar/borrar O(1) **cuando ya tienes el nodo** (LRU, colas en el kernel); acceso O(n) y mala caché.
:::

::: desplegable ❓ ¿Diferencia entre BFS y DFS? ¿Cuál da el camino más corto?
BFS usa cola y avanza por niveles; DFS usa pila (o recursión) y baja hasta el fondo. BFS da el camino más corto en **número de aristas** en grafos sin pesos. Con pesos, Dijkstra (≥ 0) o Bellman-Ford (negativos). Ambos son O(V + E).
:::

::: desplegable ❓ ¿Por qué quicksort es O(n²) en el peor caso y aun así se usa tanto?
Si el pivote cae siempre en un extremo, las particiones son de tamaño n−1 y 0. Con pivote aleatorio la probabilidad es despreciable, y en promedio es O(n log n) con constantes pequeñas, in-place y buena caché. Las librerías usan híbridos (introsort cambia a heap sort si la recursión se hace demasiado profunda).
:::

::: desplegable ❓ ¿Qué significa que un sort sea estable y por qué importa?
Que los elementos con la misma clave mantienen su orden relativo. Permite ordenar por varios criterios en pasadas sucesivas (primero por nombre, luego por nota) y es lo que se espera en interfaces (tablas ordenables). Python, Java (objetos) y JS (desde ES2019) garantizan estabilidad.
:::

::: desplegable ❓ ¿Memoización o tabulación?
Las dos son DP con la misma complejidad. Memoización (top-down) es recursión + caché: fácil de escribir y solo calcula lo necesario, pero arriesga `RecursionError`. Tabulación (bottom-up) llena una tabla iterativamente: sin límite de pila y permite reducir memoria guardando solo las filas necesarias.
:::

::: desplegable ❓ ¿Cuándo funciona un algoritmo greedy?
Cuando la elección localmente óptima nunca impide llegar al óptimo global (propiedad de elección greedy + subestructura óptima). Se demuestra con un argumento de intercambio. Si encuentras un contraejemplo (monedas `[4, 3, 1]` para 6), cambia a DP.
:::

::: desplegable ❓ ¿Cómo detectas un ciclo en una lista enlazada y en un grafo dirigido?
Lista: Floyd (tortuga y liebre), O(n) tiempo y O(1) espacio. Grafo dirigido: DFS con tres colores (blanco / en la pila / terminado): si llegas a un nodo "en la pila" hay ciclo; o Kahn: si el orden topológico no incluye todos los nodos, hay ciclo. Grafo no dirigido: union-find.
:::

::: desplegable ❓ Tienes 10 GB de números y 1 GB de RAM. ¿Cómo los ordenas?
**Ordenamiento externo**: lee bloques que quepan en RAM, ordena cada uno y escríbelo a disco (runs); luego haz una mezcla k-vías con un heap leyendo de a poco de cada archivo (`heapq.merge`). Es como funcionan los `sort` de bases de datos y el comando `sort` de Unix con archivos grandes.
:::

::: desplegable ❓ ¿Cómo encontrarías los 10 productos más vendidos en un flujo infinito de ventas?
Contador (dict) por producto + min-heap de tamaño 10, o `Counter.most_common(10)` periódicamente. Si los productos son demasiados para la memoria, estructuras aproximadas como Count-Min Sketch. Discute exactitud vs memoria.
:::

## 📋 Resumen: estructuras, complejidades y vocabulario

| Estructura | Acceso / buscar | Insertar | Borrar | Ideal para |
|---|---|---|---|---|
| Array dinámico (`list`) | O(1) índice / O(n) valor | O(1)* final, O(n) medio | O(1) final, O(n) medio | Casi todo, recorrer |
| Lista enlazada | O(n) | O(1) con el nodo | O(1) con el nodo | LRU, inserciones locales |
| Pila | O(1) cima | O(1) | O(1) | Deshacer, DFS, paréntesis |
| Cola (`deque`) | O(1) extremos | O(1) | O(1) | BFS, tareas en orden |
| Hash map / set | O(1)† | O(1)† | O(1)† | Buscar, contar, agrupar |
| BST balanceado | O(log n) | O(log n) | O(log n) | Datos ordenados + rangos |
| Heap | O(1) mín | O(log n) | O(log n) mín | Prioridades, top-k |
| Trie | O(L) | O(L) | O(L) | Prefijos, autocompletar |
| Union-Find | ~O(1) | ~O(1) | — | Grupos, conectividad |
| Grafo (lista adyacencia) | O(grado) | O(1) | O(grado) | Redes, rutas, dependencias |

📌 Resumen: `*` amortizado · `†` promedio (peor caso O(n)) · L = longitud de la palabra.

```capas
Problema : ¿qué operación se repite más?
Estructura : la que la hace O(1) u O(log n)
Técnica : two pointers, ventana, binaria, DP, greedy, BFS/DFS
Código : librería estándar + casos borde
Verificación : traza a mano, tests, Big O de tiempo y espacio
```

📌 Resumen: chuleta mental de 6 líneas:
- ¿Buscar rápido? → **hash**. ¿Mínimo/máximo repetido? → **heap**. ¿Ordenado + rangos? → **árbol / bisect**.
- ¿Contiguo? → **ventana**. ¿Ordenado? → **dos punteros / binaria**. ¿Sumas de rangos? → **prefijos**.
- ¿Niveles / camino mínimo sin pesos? → **BFS**. ¿Con pesos? → **Dijkstra**. ¿Dependencias? → **topológico**.
- ¿Todas las combinaciones? → **backtracking**. ¿Contar formas / óptimo con repeticiones? → **DP**.
- ¿Grupos que se unen? → **union-find**. ¿Prefijos de palabras? → **trie**.
- Siempre: fuerza bruta primero, luego optimiza, y di **tiempo y espacio**.

| English | Suena | Español |
|---|---|---|
| algorithm | álgorizm | algoritmo |
| data structure | déita strákcher | estructura de datos |
| time / space complexity | táim / spéis komplékxiti | complejidad temporal / espacial |
| worst case | uérst kéis | peor caso |
| amortized | ámortaizd | amortizado |
| array | aréi | arreglo |
| linked list | linkt list | lista enlazada |
| stack / queue | stak / kiú | pila / cola |
| hash table | jash téibol | tabla hash |
| tree / leaf / root | trí / lif / rut | árbol / hoja / raíz |
| heap | jiip | montículo |
| graph / edge / vertex | graf / edch / vértex | grafo / arista / vértice |
| breadth-first search | bredz ferst sérch | búsqueda en anchura |
| depth-first search | depz ferst sérch | búsqueda en profundidad |
| shortest path | shórtest paz | camino más corto |
| recursion | rikérshon | recursión |
| binary search | báinari sérch | búsqueda binaria |
| sorting / stable | sórting / stéibol | ordenamiento / estable |
| sliding window | sláiding uíndou | ventana deslizante |
| greedy | grídi | voraz |
| dynamic programming | dainámik prógraming | programación dinámica |
| memoization | memoaiséishon | memoización |
| backtracking | báktraking | vuelta atrás |
| bitwise | bítuais | a nivel de bits |
| brute force | brut fors | fuerza bruta |
| edge case | edch kéis | caso borde |
