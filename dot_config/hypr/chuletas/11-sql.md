# 🗃️ SQL
> Habla con las bases de datos: crear tablas, consultar, unir, agrupar, ventanas, índices y SQL seguro desde Python.

## 🧠 Conceptos básicos

Una **base de datos relacional** guarda la información en **tablas**, como hojas de Excel muy disciplinadas: cada **columna** tiene un nombre y un tipo fijo, y cada **fila** es un registro. Las tablas se **relacionan** entre sí mediante claves. **SQL** (Structured Query Language) es el idioma para pedirle cosas a la base: es **declarativo**, dices QUÉ quieres y el motor decide CÓMO buscarlo.

Analogía: la base de datos es la **secretaría de la universidad**. Cada tabla es un archivador (alumnos, cursos, notas); cada fila es una ficha; la clave primaria es el número de matrícula, que nunca se repite; y una clave foránea es cuando en la ficha de notas escribes el número de matrícula para saber de quién es la nota.

| Concepto | Qué es | Ejemplo |
|---|---|---|
| Tabla | Conjunto de filas con las mismas columnas | `alumnos` |
| Fila (registro, tupla) | Un elemento concreto | Ana, La Paz, 20 años |
| Columna (campo, atributo) | Una propiedad con tipo | `nombre TEXT` |
| Clave primaria (PK) | Identifica cada fila, única y no nula | `alumnos.id` |
| Clave foránea (FK) | Apunta a la PK de otra tabla | `notas.alumno_id` |
| NULL | "Valor desconocido / ausente" (no es 0 ni "") | nota aún no puesta |
| Esquema | La estructura: tablas, columnas, relaciones | el diseño de la base |
| Consulta (query) | Una pregunta en SQL | `SELECT ...` |

| Sublenguaje | Comandos | Para qué |
|---|---|---|
| DDL (definición) | `CREATE`, `ALTER`, `DROP` | Crear y cambiar la estructura |
| DML (manipulación) | `INSERT`, `UPDATE`, `DELETE` | Cambiar los datos |
| DQL (consulta) | `SELECT` | Leer datos |
| DCL (control) | `GRANT`, `REVOKE` | Permisos de usuarios |
| TCL (transacciones) | `BEGIN`, `COMMIT`, `ROLLBACK` | Agrupar cambios |

📌 En esta hoja usamos siempre la misma base de ejemplo: **alumnos**, **cursos** y **notas** (la sección siguiente tiene el script para crearla). Todo funciona en SQLite; las diferencias con PostgreSQL y MySQL están al final.

💡 Consejo: para practicar sin instalar nada escribe `sqlite3 escuela.db` en la terminal (o `python3` + `import sqlite3`). Dentro de sqlite3 usa `.tables`, `.schema alumnos`, `.mode box` y `.headers on` para ver bonito.

⚠️ Cuidado: las palabras clave de SQL no distinguen mayúsculas (`select` = `SELECT`), pero por costumbre se escriben en MAYÚSCULAS y los nombres de tablas en minúsculas. Los textos entre comillas sí distinguen: `'Ana'` no es `'ana'` en PostgreSQL.

🇬🇧 **database** /déita-béis/ = base de datos · **table** /téibol/ = tabla · **row** /róu/ = fila · **column** /kólum/ = columna · **query** /kuíri/ = consulta · **primary key** /práimari kí/ = clave primaria · **foreign key** /fórin kí/ = clave foránea

## 🏗️ Crear tablas y tipos de datos

`CREATE TABLE` define el nombre de la tabla, sus columnas, el tipo de cada una y sus reglas (restricciones). Elegir bien los tipos evita errores y ahorra espacio.

| Tipo (estándar / PostgreSQL) | En SQLite | Para qué | Ejemplo |
|---|---|---|---|
| `INTEGER`, `BIGINT` | `INTEGER` | Enteros | `edad INTEGER` |
| `SERIAL` / `GENERATED ALWAYS AS IDENTITY` | `INTEGER PRIMARY KEY` | Id autoincremental | `id INTEGER PRIMARY KEY` |
| `NUMERIC(10,2)`, `DECIMAL` | `NUMERIC` | Dinero y decimales exactos | `precio NUMERIC(10,2)` |
| `REAL`, `DOUBLE PRECISION` | `REAL` | Decimales aproximados (ciencia) | `temperatura REAL` |
| `VARCHAR(n)` | `TEXT` | Texto con límite | `email VARCHAR(120)` |
| `TEXT` | `TEXT` | Texto sin límite | `descripcion TEXT` |
| `BOOLEAN` | `INTEGER` (0/1) | Verdadero / falso | `activo BOOLEAN` |
| `DATE`, `TIME`, `TIMESTAMP` | `TEXT` ('2026-10-18') | Fechas y horas | `fecha_nac DATE` |
| `JSON`, `JSONB` | `TEXT` + funciones json | Datos semiestructurados | `extra JSONB` |
| `UUID` | `TEXT` | Identificadores globales | `id UUID` |
| `BYTEA` / `BLOB` | `BLOB` | Datos binarios | `foto BLOB` |

- `CREATE TABLE IF NOT EXISTS t (...);` :: Crear solo si no existe (no da error)
- `DROP TABLE IF EXISTS t;` :: Borrar la tabla entera (estructura y datos)
- `ALTER TABLE alumnos ADD COLUMN telefono TEXT;` :: Añadir columna
- `ALTER TABLE alumnos RENAME COLUMN telefono TO celular;` :: Renombrar columna
- `ALTER TABLE alumnos RENAME TO estudiantes;` :: Renombrar tabla
- `ALTER TABLE alumnos DROP COLUMN celular;` :: Quitar columna
- `CREATE TABLE copia AS SELECT * FROM alumnos;` :: Crear una tabla a partir de una consulta
- `DEFAULT CURRENT_TIMESTAMP` :: Valor por defecto: la fecha y hora actual

### ✅ Ejemplo resuelto: crear la base de ejemplo (escuela)

```sql
CREATE TABLE alumnos (
    id        INTEGER PRIMARY KEY,
    nombre    TEXT    NOT NULL,
    ciudad    TEXT    NOT NULL,
    edad      INTEGER CHECK (edad > 0),
    email     TEXT    UNIQUE
);

CREATE TABLE cursos (
    id        INTEGER PRIMARY KEY,
    nombre    TEXT    NOT NULL UNIQUE,
    creditos  INTEGER NOT NULL DEFAULT 4,
    docente   TEXT
);

CREATE TABLE notas (
    alumno_id INTEGER NOT NULL REFERENCES alumnos(id),
    curso_id  INTEGER NOT NULL REFERENCES cursos(id),
    nota      INTEGER CHECK (nota BETWEEN 0 AND 100),
    PRIMARY KEY (alumno_id, curso_id)
);

INSERT INTO alumnos (id, nombre, ciudad, edad, email) VALUES
    (1, 'Ana Quispe',   'La Paz',     20, 'ana@umsa.bo'),
    (2, 'Luis Mamani',  'Cochabamba', 22, 'luis@umss.bo'),
    (3, 'Sofía Rojas',  'Santa Cruz', 19, 'sofia@uagrm.bo'),
    (4, 'Pedro Choque', 'La Paz',     21, NULL),
    (5, 'María Flores', 'Sucre',      23, 'maria@usfx.bo');

INSERT INTO cursos (id, nombre, creditos, docente) VALUES
    (1, 'Bases de Datos',          5, 'Ing. Vargas'),
    (2, 'Programación I',          6, 'Lic. Torrez'),
    (3, 'Cálculo I',               5, 'Lic. Gutiérrez'),
    (4, 'Inteligencia Artificial', 4, NULL);

INSERT INTO notas (alumno_id, curso_id, nota) VALUES
    (1, 1, 85), (1, 2, 92), (1, 3, 70),
    (2, 1, 45), (2, 2, 60),
    (3, 1, 95), (3, 2, NULL), (3, 3, 88),
    (4, 2, 51), (4, 3, 38);

SELECT
    (SELECT COUNT(*) FROM alumnos) AS alumnos,
    (SELECT COUNT(*) FROM cursos)  AS cursos,
    (SELECT COUNT(*) FROM notas)   AS notas;
```

Qué hace cada parte: `alumnos` y `cursos` tienen un `id` como clave primaria; `NOT NULL` obliga a rellenar el campo; `UNIQUE` impide emails o nombres de curso repetidos; `CHECK` valida edades y notas; `notas` es una **tabla intermedia** (relación muchos a muchos: un alumno lleva muchos cursos y un curso tiene muchos alumnos) con una **clave primaria compuesta** `(alumno_id, curso_id)` para que nadie tenga dos notas en el mismo curso; `REFERENCES` crea las claves foráneas. Fíjate en los casos especiales que usaremos: María (5) no está inscrita en nada, el curso de IA (4) no tiene alumnos, Sofía aún no tiene nota en Programación (`NULL`) y Pedro no tiene email.

```text
alumnos | cursos | notas
--------+--------+------
5       | 4      | 10
```

```text
 alumnos              notas                    cursos
+----+---------+    +-----------+----------+   +----+-----------+
| id | nombre  |<---| alumno_id | curso_id |-->| id | nombre    |
+----+---------+    |   nota    |          |   +----+-----------+
                    +-----------+----------+
   1 alumno ---< N notas >--- 1 curso      (relación muchos a muchos)
```

⚠️ Cuidado: en SQLite las claves foráneas vienen **desactivadas**. Ejecuta `PRAGMA foreign_keys = ON;` al conectar o no se comprobarán.

💡 Consejo: guarda tu script de creación en un archivo `esquema.sql` y cárgalo con `sqlite3 escuela.db < esquema.sql`. Así puedes recrear la base cuando quieras.

🇬🇧 **create** /kriéit/ = crear · **data type** /déita táip/ = tipo de dato · **not null** /not nal/ = no nulo · **default** /difólt/ = por defecto · **schema** /skíma/ = esquema · **junction table** /yánkshon téibol/ = tabla intermedia

## ✍️ CRUD: INSERT, SELECT, UPDATE, DELETE

**CRUD** son las cuatro operaciones básicas sobre datos: **C**reate (INSERT), **R**ead (SELECT), **U**pdate (UPDATE) y **D**elete (DELETE). Todo sistema (una app de notas, un banco, TikTok) se reduce en el fondo a estas cuatro.

### ➕ INSERT

- `INSERT INTO alumnos (nombre, ciudad, edad) VALUES ('Rosa', 'Oruro', 20);` :: Insertar una fila (el id se genera solo)
- `INSERT INTO t (a, b) VALUES (1, 'x'), (2, 'y');` :: Varias filas de una vez
- `INSERT INTO t (a) SELECT x FROM otra;` :: Insertar el resultado de una consulta
- `INSERT ... ON CONFLICT (email) DO NOTHING;` :: Si ya existe, ignorar (SQLite y PostgreSQL)
- `INSERT ... ON CONFLICT (id) DO UPDATE SET nota = excluded.nota;` :: "Upsert": insertar o actualizar
- `INSERT ... RETURNING id;` :: Devuelve el id creado (PostgreSQL y SQLite 3.35+)

### 🔍 SELECT

- `SELECT * FROM alumnos;` :: Todas las columnas y filas
- `SELECT nombre, edad FROM alumnos;` :: Columnas concretas
- `SELECT nombre AS alumno FROM alumnos;` :: Alias: renombra la columna en el resultado
- `SELECT nombre, edad + 1 AS edad_proxima FROM alumnos;` :: Columnas calculadas
- `SELECT DISTINCT ciudad FROM alumnos;` :: Sin repetidos
- `SELECT COUNT(*) FROM alumnos;` :: Cuántas filas hay

### ✏️ UPDATE y 🗑️ DELETE

- `UPDATE alumnos SET edad = 21 WHERE id = 3;` :: Cambiar un valor (¡siempre con WHERE!)
- `UPDATE alumnos SET edad = edad + 1, ciudad = 'El Alto' WHERE id = 4;` :: Varias columnas, usando el valor actual
- `DELETE FROM notas WHERE nota IS NULL;` :: Borrar filas que cumplan (¡siempre con WHERE!)
- `DELETE FROM notas;` :: Borra TODAS las filas (la tabla queda vacía)
- `TRUNCATE TABLE notas;` :: Vaciar rápido (PostgreSQL/MySQL; no existe en SQLite)

### ✅ Ejemplo resuelto: ciclo CRUD completo

```sql
INSERT INTO alumnos (nombre, ciudad, edad, email)
VALUES ('Rosa Condori', 'Oruro', 20, 'rosa@uto.bo');

UPDATE alumnos SET edad = edad + 1 WHERE nombre = 'Rosa Condori';

SELECT id, nombre, ciudad, edad FROM alumnos WHERE ciudad = 'Oruro';

DELETE FROM alumnos WHERE email = 'rosa@uto.bo';

SELECT COUNT(*) AS total_alumnos FROM alumnos;
```

Qué hace cada parte: el `INSERT` no da `id` y SQLite le asigna el siguiente (6) porque es `INTEGER PRIMARY KEY`; el `UPDATE` usa el valor actual (`edad + 1`) y el `WHERE` limita el cambio a Rosa; el primer `SELECT` comprueba el resultado; el `DELETE` la quita usando su email (que es `UNIQUE`); el último `SELECT` confirma que volvemos a tener 5 alumnos.

```text
id | nombre       | ciudad | edad
---+--------------+--------+-----
6  | Rosa Condori | Oruro  | 21

total_alumnos
-------------
5
```

⚠️ Cuidado: un `UPDATE` o `DELETE` sin `WHERE` afecta a **toda la tabla**. Truco de seguridad: escribe primero el `SELECT ... WHERE ...`, comprueba que salen las filas correctas, y luego cambia `SELECT *` por `DELETE`.

💡 Consejo: en la vida real evita `SELECT *` en programas: pide solo las columnas que usas. Es más rápido y no se rompe si alguien añade columnas.

🇬🇧 **insert** /insért/ = insertar · **update** /apdéit/ = actualizar · **delete** /dilít/ = borrar · **select** /seléct/ = seleccionar · **upsert** /apsért/ = insertar o actualizar · **alias** /éilias/ = alias

## 🎯 WHERE: filtrar filas

`WHERE` se queda solo con las filas que cumplen una condición. Es el colador de SQL.

| Operador | Significado | Ejemplo |
|---|---|---|
| `=`, `<>` (o `!=`) | Igual, distinto | `ciudad = 'La Paz'` |
| `<`, `>`, `<=`, `>=` | Comparaciones | `edad >= 21` |
| `AND`, `OR`, `NOT` | Combinar condiciones | `edad > 20 AND ciudad = 'La Paz'` |
| `BETWEEN a AND b` | Entre a y b (incluidos) | `nota BETWEEN 51 AND 70` |
| `IN (...)` | Uno de la lista | `ciudad IN ('Sucre', 'Oruro')` |
| `NOT IN (...)` | Ninguno de la lista | `id NOT IN (1, 2)` |
| `LIKE 'A%'` | Patrón: `%` = cualquier cosa | `nombre LIKE '%Quispe'` |
| `LIKE '_na'` | `_` = exactamente un carácter | `'Ana'`, `'Ina'` |
| `ILIKE` | LIKE sin distinguir mayúsculas (PostgreSQL) | `nombre ILIKE 'ana%'` |
| `IS NULL`, `IS NOT NULL` | Es nulo / no es nulo | `email IS NULL` |
| `EXISTS (subconsulta)` | ¿La subconsulta devuelve algo? | ver subconsultas |
| `GLOB 'A*'` | Patrón estilo shell (SQLite, distingue mayúsculas) | `nombre GLOB 'S*'` |

### 🕳️ El caso especial de NULL

`NULL` significa "no sé". Cualquier comparación con NULL da **desconocido** (ni verdadero ni falso), por eso `nota = NULL` nunca encuentra nada: hay que escribir `nota IS NULL`.

- `COALESCE(email, 'sin email')` :: Primer valor no nulo: reemplaza NULL por algo
- `NULLIF(a, b)` :: Devuelve NULL si a = b (útil para evitar dividir entre 0)
- `WHERE nota IS DISTINCT FROM 50` :: Comparación que trata NULL como un valor (PostgreSQL, SQLite 3.39+)

### ✅ Ejemplo resuelto: filtros combinados

```sql
SELECT nombre, ciudad, edad, COALESCE(email, '(sin email)') AS email
FROM alumnos
WHERE (ciudad = 'La Paz' OR edad >= 22)
  AND nombre NOT LIKE 'L%';

SELECT alumno_id, curso_id, nota
FROM notas
WHERE nota BETWEEN 40 AND 60 OR nota IS NULL;
```

Qué hace cada parte: los **paréntesis** agrupan el `OR` (sin ellos, `AND` se evalúa primero y el resultado cambia); `NOT LIKE 'L%'` excluye nombres que empiezan por L (Luis); `COALESCE` muestra un texto cuando el email es NULL. La segunda consulta busca notas "en el límite" o sin poner; sin `OR nota IS NULL` la fila de Sofía no aparecería.

```text
nombre       | ciudad | edad | email
-------------+--------+------+--------------
Ana Quispe   | La Paz | 20   | ana@umsa.bo
Pedro Choque | La Paz | 21   | (sin email)
María Flores | Sucre  | 23   | maria@usfx.bo

alumno_id | curso_id | nota
----------+----------+-----
2         | 1        | 45
2         | 2        | 60
3         | 2        | NULL
4         | 2        | 51
```

⚠️ Cuidado: los textos van entre comillas **simples** (`'La Paz'`). Las comillas dobles son para nombres de columnas o tablas (`"Mi Columna"`) en PostgreSQL y SQLite.

⚠️ Cuidado: `NOT IN (subconsulta)` falla en silencio si la subconsulta devuelve algún NULL: no devuelve ninguna fila. Usa `NOT EXISTS` en su lugar.

🇬🇧 **filter** /fílter/ = filtrar · **condition** /kondíshon/ = condición · **between** /bituín/ = entre · **like** /láik/ = como (parecido a) · **null** /nal/ = nulo · **wildcard** /uáild-kard/ = comodín

## ↕️ ORDER BY, LIMIT y funciones útiles

`ORDER BY` ordena el resultado (`ASC` de menor a mayor, por defecto; `DESC` al revés). `LIMIT` corta a N filas y `OFFSET` se salta las primeras: juntos sirven para **paginar** (página 3 de 10 resultados = `LIMIT 10 OFFSET 20`).

- `ORDER BY edad DESC` :: De mayor a menor
- `ORDER BY ciudad ASC, edad DESC` :: Por ciudad y, si empatan, por edad descendente
- `ORDER BY nota DESC NULLS LAST` :: Los NULL al final (PostgreSQL, SQLite 3.30+)
- `LIMIT 3` :: Solo las 3 primeras filas
- `LIMIT 10 OFFSET 20` :: Filas 21 a 30 (paginación)
- `FETCH FIRST 3 ROWS ONLY` :: Estándar SQL de LIMIT (PostgreSQL, Oracle)
- `SELECT TOP 3 ...` :: LIMIT en SQL Server

### 🧰 Funciones de texto, número y fecha

| Función | Qué hace | Ejemplo → resultado |
|---|---|---|
| `UPPER(s)` / `LOWER(s)` | Mayúsculas / minúsculas | `UPPER('ana')` → `ANA` |
| `LENGTH(s)` | Longitud | `LENGTH('Sucre')` → `5` |
| `SUBSTR(s, inicio, n)` | Recorte (empieza en 1) | `SUBSTR('Bolivia', 1, 3)` → `Bol` |
| `TRIM(s)` | Quita espacios | `TRIM('  x ')` → `x` |
| `REPLACE(s, a, b)` | Reemplaza | `REPLACE('a-b', '-', '/')` → `a/b` |
| `s1 \|\| s2` | Concatenar (estándar) | `'Hola' \|\| ' ' \|\| 'Ana'` |
| `INSTR(s, x)` | Posición de x (SQLite/MySQL) | `INSTR('ana@umsa.bo', '@')` → `4` |
| `ROUND(x, n)` | Redondear | `ROUND(72.456, 1)` → `72.5` |
| `ABS(x)` | Valor absoluto | `ABS(-3)` → `3` |
| `CAST(x AS tipo)` | Convertir tipo | `CAST('42' AS INTEGER)` |
| `DATE('now')` | Fecha actual (SQLite) | `2026-10-18` |
| `CURRENT_DATE` | Fecha actual (estándar) | |
| `STRFTIME('%Y', fecha)` | Parte de una fecha (SQLite) | `2026` |
| `EXTRACT(YEAR FROM fecha)` | Parte de una fecha (PostgreSQL/MySQL) | `2026` |

### 🔀 CASE: el if de SQL

```sql
SELECT nombre,
       CASE
           WHEN edad < 20 THEN 'adolescente'
           WHEN edad BETWEEN 20 AND 22 THEN 'joven'
           ELSE 'mayor'
       END AS grupo
FROM alumnos;
```

### ✅ Ejemplo resuelto: top 3 notas con calificación

```sql
SELECT alumno_id,
       curso_id,
       nota,
       CASE
           WHEN nota >= 90 THEN 'Excelente'
           WHEN nota >= 71 THEN 'Bueno'
           WHEN nota >= 51 THEN 'Aprobado'
           ELSE 'Reprobado'
       END AS calificacion
FROM notas
WHERE nota IS NOT NULL
ORDER BY nota DESC
LIMIT 3;

SELECT UPPER(SUBSTR(nombre, 1, INSTR(nombre, ' ') - 1)) AS nombre_pila,
       SUBSTR(email, INSTR(email, '@') + 1) AS dominio
FROM alumnos
WHERE email IS NOT NULL
ORDER BY dominio;
```

Qué hace cada parte: `CASE` evalúa las condiciones **en orden** y se queda con la primera verdadera (por eso 95 es "Excelente" y no "Bueno"); `WHERE nota IS NOT NULL` quita la nota pendiente; `ORDER BY nota DESC LIMIT 3` deja las tres mejores. En la segunda consulta, `INSTR(nombre, ' ')` encuentra el espacio y `SUBSTR` corta hasta ahí (el nombre de pila); con el `@` se saca el dominio del email. Mira la salida: `SOFíA` y `MARíA` conservan la í minúscula.

⚠️ Cuidado: en SQLite `UPPER`, `LOWER` y `LIKE` sin mayúsculas solo funcionan con letras ASCII: las tildes y la ñ no cambian. PostgreSQL y MySQL sí las convierten bien.

```text
alumno_id | curso_id | nota | calificacion
----------+----------+------+-------------
3         | 1        | 95   | Excelente
1         | 2        | 92   | Excelente
3         | 3        | 88   | Bueno

nombre_pila | dominio
------------+---------
SOFíA       | uagrm.bo
ANA         | umsa.bo
LUIS        | umss.bo
MARíA       | usfx.bo
```

⚠️ Cuidado: sin `ORDER BY` la base de datos **no garantiza ningún orden**, aunque parezca que siempre sale igual. Si el orden importa, ponlo.

🇬🇧 **order by** /órder bái/ = ordenar por · **ascending / descending** /asénding / disénding/ = ascendente / descendente · **limit** /límit/ = límite · **offset** /óf-set/ = desplazamiento · **pagination** /payinéishon/ = paginación

## 📊 Agregación: GROUP BY y HAVING

Las **funciones de agregación** convierten muchas filas en un solo valor (contar, sumar, promediar). `GROUP BY` las aplica **por grupo**: "promedio de notas **por curso**". `HAVING` filtra **grupos** (después de agrupar), mientras que `WHERE` filtra **filas** (antes de agrupar).

Analogía: tienes un montón de exámenes. `GROUP BY curso` los separa en pilas, una por curso; `AVG(nota)` calcula el promedio de cada pila; `HAVING AVG(nota) > 70` te quedas solo con las pilas que superan 70.

| Función | Qué hace | Ojo con NULL |
|---|---|---|
| `COUNT(*)` | Cuenta filas | Cuenta todas |
| `COUNT(col)` | Cuenta valores no nulos | Ignora NULL |
| `COUNT(DISTINCT col)` | Cuenta valores distintos | Ignora NULL |
| `SUM(col)` | Suma | Ignora NULL |
| `AVG(col)` | Promedio | Ignora NULL (no cuenta como 0) |
| `MIN(col)` / `MAX(col)` | Menor / mayor | Ignora NULL |
| `GROUP_CONCAT(col, ', ')` | Une textos (SQLite/MySQL) | En PostgreSQL: `STRING_AGG(col, ', ')` |

```text
Orden en que SQL EJECUTA una consulta (no el orden en que se escribe):
  1. FROM / JOIN     ¿de qué tablas?
  2. WHERE           filtra filas
  3. GROUP BY        forma grupos
  4. HAVING          filtra grupos
  5. SELECT          calcula columnas y alias
  6. DISTINCT        quita repetidos
  7. ORDER BY        ordena
  8. LIMIT / OFFSET  corta
```

- `SELECT ciudad, COUNT(*) FROM alumnos GROUP BY ciudad;` :: Contar por grupo
- `... GROUP BY ciudad HAVING COUNT(*) > 1;` :: Filtrar grupos
- `SELECT COUNT(*), COUNT(nota), AVG(nota) FROM notas;` :: Totales de toda la tabla (un solo grupo)
- `GROUP BY 1` :: Agrupar por la primera columna del SELECT (atajo)

### ✅ Ejemplo resuelto: estadísticas por curso

```sql
SELECT curso_id,
       COUNT(*)                 AS inscritos,
       COUNT(nota)              AS con_nota,
       ROUND(AVG(nota), 1)      AS promedio,
       MAX(nota)                AS maxima,
       SUM(CASE WHEN nota >= 51 THEN 1 ELSE 0 END) AS aprobados
FROM notas
GROUP BY curso_id
ORDER BY promedio DESC;

SELECT ciudad, COUNT(*) AS alumnos, GROUP_CONCAT(nombre, ', ') AS nombres
FROM alumnos
GROUP BY ciudad
HAVING COUNT(*) >= 2;
```

Qué hace cada parte: `COUNT(*)` cuenta inscripciones y `COUNT(nota)` solo las que tienen nota (en el curso 2 la diferencia es Sofía); `AVG` ignora el NULL, así que el promedio del curso 2 es de 3 notas, no de 4; `SUM(CASE ...)` es el truco clásico para contar los que cumplen una condición. La segunda consulta agrupa alumnos por ciudad y `HAVING` deja solo las ciudades con al menos 2 alumnos.

```text
curso_id | inscritos | con_nota | promedio | maxima | aprobados
---------+-----------+----------+----------+--------+----------
1        | 3         | 3        | 75.0     | 95     | 2
2        | 4         | 3        | 67.7     | 92     | 3
3        | 3         | 3        | 65.3     | 88     | 2

ciudad | alumnos | nombres
-------+---------+-------------------------
La Paz | 2       | Ana Quispe, Pedro Choque
```

⚠️ Cuidado: toda columna del `SELECT` que no esté dentro de una función de agregación debe estar en el `GROUP BY`. PostgreSQL da error ("must appear in the GROUP BY clause"); SQLite y MySQL antiguos lo permiten pero devuelven un valor cualquiera.

⚠️ Cuidado: no puedes usar una agregación en `WHERE` (`WHERE AVG(nota) > 70` da error). Para eso existe `HAVING`.

🇬🇧 **aggregate** /ágregueit/ = agregar (resumir) · **group by** /grup bái/ = agrupar por · **having** /jáving/ = que tenga · **average** /áverech/ = promedio · **count** /káunt/ = contar · **sum** /sam/ = suma

## 🔗 JOINs: unir tablas

Los datos están repartidos en varias tablas para no repetirlos; `JOIN` los vuelve a juntar usando las claves. `ON` dice qué columnas deben coincidir. Es la parte más importante (y más preguntada en entrevistas) de SQL.

```text
   A = alumnos      B = notas

   INNER JOIN         LEFT JOIN          RIGHT JOIN         FULL JOIN
    .--. .--.          .--. .--.          .--. .--.          .--. .--.
   /    X    \        /####X    \        /    X####\        /####X####\
  |  A |##| B |      |##A#|##| B |      |  A |##|#B##|     |##A#|##|#B##|
   \    X    /        \####X    /        \    X####/        \####X####/
    '--' '--'          '--' '--'          '--' '--'          '--' '--'
  solo lo común     todo A + lo común   todo B + lo común   todo de ambos
```

| Tipo | Devuelve | Si no hay pareja | Uso típico |
|---|---|---|---|
| `INNER JOIN` (o `JOIN`) | Solo filas con coincidencia en ambas | Se descarta | "Alumnos con sus notas" |
| `LEFT JOIN` | Todas las de la izquierda + coincidencias | Columnas de la derecha en NULL | "Todos los alumnos, tengan o no notas" |
| `RIGHT JOIN` | Todas las de la derecha + coincidencias | Columnas de la izquierda en NULL | Igual que LEFT con las tablas al revés |
| `FULL OUTER JOIN` | Todas las de ambas | NULL en el lado que falte | Comparar dos listas |
| `CROSS JOIN` | Todas las combinaciones (producto cartesiano) | — | Generar combinaciones |
| Self join | Una tabla consigo misma (con alias) | — | Jerarquías, comparar filas |

- `FROM alumnos a JOIN notas n ON n.alumno_id = a.id` :: Alias cortos (`a`, `n`) para no repetir nombres largos
- `JOIN cursos c USING (id)` :: Atajo cuando la columna se llama igual en ambas
- `LEFT JOIN ... WHERE n.alumno_id IS NULL` :: Patrón "anti-join": los que NO tienen pareja
- `FROM a JOIN b ON ... JOIN c ON ...` :: Encadenar varios JOIN

### ✅ Ejemplo resuelto: los cuatro JOIN sobre las mismas tablas

```sql
-- 1) INNER JOIN: alumnos con sus notas y el nombre del curso
SELECT a.nombre, c.nombre AS curso, n.nota
FROM alumnos a
JOIN notas  n ON n.alumno_id = a.id
JOIN cursos c ON c.id = n.curso_id
WHERE a.ciudad = 'La Paz'
ORDER BY a.nombre, curso;

-- 2) LEFT JOIN: TODOS los alumnos y cuántos cursos llevan (María aparece con 0)
SELECT a.nombre, COUNT(n.curso_id) AS cursos
FROM alumnos a
LEFT JOIN notas n ON n.alumno_id = a.id
GROUP BY a.id
ORDER BY cursos DESC, a.nombre;

-- 3) RIGHT JOIN: todos los cursos aunque nadie esté inscrito (IA aparece con NULL)
SELECT c.nombre AS curso, n.alumno_id
FROM notas n
RIGHT JOIN cursos c ON c.id = n.curso_id
WHERE n.alumno_id IS NULL OR n.alumno_id = 1;

-- 4) FULL JOIN: alumnos y cursos "huérfanos" de ambos lados
SELECT a.nombre AS alumno, c.nombre AS curso
FROM (SELECT a.id AS aid, n.curso_id AS cid FROM alumnos a LEFT JOIN notas n ON n.alumno_id = a.id) x
FULL JOIN cursos c ON c.id = x.cid
LEFT JOIN alumnos a ON a.id = x.aid
WHERE x.cid IS NULL OR x.aid IS NULL;
```

Qué hace cada parte: (1) el `INNER JOIN` encadena alumnos → notas → cursos y solo muestra combinaciones que existen; (2) con `LEFT JOIN` María no se pierde: sus columnas de `notas` quedan en NULL y `COUNT(n.curso_id)` las cuenta como 0 (con `COUNT(*)` saldría 1, ¡error típico!); (3) el `RIGHT JOIN` conserva todos los cursos; filtramos para ver los de Ana y el curso sin nadie; (4) el `FULL JOIN` conserva lo que no tiene pareja en ningún lado: María (alumna sin curso) e Inteligencia Artificial (curso sin alumnos).

```text
nombre       | curso          | nota
-------------+----------------+-----
Ana Quispe   | Bases de Datos | 85
Ana Quispe   | Cálculo I      | 70
Ana Quispe   | Programación I | 92
Pedro Choque | Cálculo I      | 38
Pedro Choque | Programación I | 51

nombre       | cursos
-------------+-------
Ana Quispe   | 3
Sofía Rojas  | 3
Luis Mamani  | 2
Pedro Choque | 2
María Flores | 0

curso                   | alumno_id
------------------------+----------
Bases de Datos          | 1
Programación I          | 1
Cálculo I               | 1
Inteligencia Artificial | NULL

alumno       | curso
-------------+------------------------
María Flores | NULL
NULL         | Inteligencia Artificial
```

⚠️ Cuidado: si olvidas el `ON` (o pones uno incorrecto) obtienes un producto cartesiano: 5 alumnos × 10 notas = 50 filas sin sentido. Si te salen "demasiadas filas", revisa los `ON`.

⚠️ Cuidado: poner en el `WHERE` una condición sobre la tabla derecha de un `LEFT JOIN` (`WHERE n.nota > 50`) lo convierte en `INNER JOIN` (las filas con NULL se descartan). Si quieres conservarlas, pon la condición en el `ON`: `LEFT JOIN notas n ON n.alumno_id = a.id AND n.nota > 50`.

💡 Consejo: casi siempre basta con `INNER` y `LEFT`. Un `RIGHT JOIN` se puede reescribir como `LEFT JOIN` cambiando el orden de las tablas, y es más fácil de leer.

🇬🇧 **join** /yóin/ = unir · **inner** /íner/ = interior · **outer** /áuter/ = exterior · **left / right** /left / ráit/ = izquierda / derecha · **match** /mach/ = coincidencia · **cartesian product** /kartíshan pródakt/ = producto cartesiano

## 🪆 Subconsultas

Una **subconsulta** es un `SELECT` dentro de otro, entre paréntesis. Sirve para preguntas en dos pasos: "alumnos cuya nota supera **el promedio**" (primero calculas el promedio, luego filtras).

| Dónde va | Devuelve | Ejemplo |
|---|---|---|
| En `WHERE` con `=`, `>`... | Un solo valor (escalar) | `WHERE nota > (SELECT AVG(nota) FROM notas)` |
| En `WHERE` con `IN` | Una lista | `WHERE id IN (SELECT alumno_id FROM notas)` |
| En `WHERE` con `EXISTS` | ¿Hay alguna fila? | `WHERE EXISTS (SELECT 1 FROM notas n WHERE n.alumno_id = a.id)` |
| En `FROM` | Una tabla temporal (necesita alias) | `FROM (SELECT ...) AS t` |
| En `SELECT` | Un valor por fila | `(SELECT COUNT(*) FROM notas n WHERE n.alumno_id = a.id)` |

Una subconsulta **correlacionada** usa columnas de la consulta de afuera (como `a.id` arriba): se evalúa una vez por cada fila exterior. Es potente pero puede ser lenta en tablas grandes; a menudo un JOIN o una CTE es mejor.

### ✅ Ejemplo resuelto: preguntas en dos pasos

```sql
-- Notas por encima del promedio general
SELECT alumno_id, curso_id, nota
FROM notas
WHERE nota > (SELECT AVG(nota) FROM notas)
ORDER BY nota DESC;

-- Alumnos que NO están inscritos en ningún curso
SELECT nombre
FROM alumnos a
WHERE NOT EXISTS (SELECT 1 FROM notas n WHERE n.alumno_id = a.id);

-- La mejor nota de cada curso y quién la sacó (correlacionada)
SELECT c.nombre AS curso, a.nombre AS alumno, n.nota
FROM notas n
JOIN alumnos a ON a.id = n.alumno_id
JOIN cursos  c ON c.id = n.curso_id
WHERE n.nota = (SELECT MAX(n2.nota) FROM notas n2 WHERE n2.curso_id = n.curso_id)
ORDER BY curso;
```

Qué hace cada parte: la primera subconsulta calcula el promedio general (624 / 9 ≈ 69.3, ignorando el NULL) y la exterior compara cada nota con él; `NOT EXISTS` devuelve verdadero cuando la subconsulta no encuentra ninguna nota de ese alumno (María); en la tercera, para cada fila `n` se calcula el máximo **de su propio curso** (`n2.curso_id = n.curso_id`) y nos quedamos con las filas que lo igualan.

```text
alumno_id | curso_id | nota
----------+----------+-----
3         | 1        | 95
1         | 2        | 92
3         | 3        | 88
1         | 1        | 85
1         | 3        | 70

nombre
------------
María Flores

curso          | alumno      | nota
---------------+-------------+-----
Bases de Datos | Sofía Rojas | 95
Cálculo I      | Sofía Rojas | 88
Programación I | Ana Quispe  | 92
```

💡 Consejo: `SELECT 1` dentro de `EXISTS` es una convención: no importa qué devuelva, solo si devuelve algo.

🇬🇧 **subquery** /sab-kuíri/ = subconsulta · **nested** /nésted/ = anidado · **correlated** /kórreleited/ = correlacionado · **exists** /eksísts/ = existe · **scalar** /skéilar/ = escalar (un solo valor)

## 🧱 CTE: consultas con WITH

Una **CTE** (Common Table Expression) es una subconsulta con **nombre**, definida al principio con `WITH`. Hace que las consultas largas se lean de arriba abajo, paso a paso, como variables en un programa: "primero calculo los promedios, luego los uno con los nombres, luego filtro".

```sql
WITH paso1 AS (
    SELECT ...
),
paso2 AS (
    SELECT ... FROM paso1 ...
)
SELECT * FROM paso2;
```

- `WITH t AS (SELECT ...) SELECT * FROM t;` :: CTE simple
- `WITH a AS (...), b AS (...)` :: Varias CTE separadas por coma (b puede usar a)
- `WITH RECURSIVE ...` :: CTE recursiva: jerarquías, series, grafos

### ✅ Ejemplo resuelto: promedio por alumno paso a paso

```sql
WITH promedios AS (
    SELECT alumno_id, ROUND(AVG(nota), 1) AS promedio, COUNT(nota) AS materias
    FROM notas
    GROUP BY alumno_id
),
general AS (
    SELECT AVG(promedio) AS media FROM promedios
)
SELECT a.nombre, p.promedio, p.materias,
       CASE WHEN p.promedio >= g.media THEN 'sobre la media' ELSE 'bajo la media' END AS situacion
FROM promedios p
JOIN alumnos a ON a.id = p.alumno_id
CROSS JOIN general g
ORDER BY p.promedio DESC;

-- CTE recursiva: los números del 1 al 5 y su factorial
WITH RECURSIVE fact(n, f) AS (
    SELECT 1, 1
    UNION ALL
    SELECT n + 1, f * (n + 1) FROM fact WHERE n < 5
)
SELECT n, f AS factorial FROM fact;
```

Qué hace cada parte: `promedios` calcula el promedio de cada alumno; `general` usa esa CTE para calcular la media de los promedios; la consulta final une los promedios con los nombres y, con `CROSS JOIN` (una sola fila), compara cada uno con la media. En la recursiva, la primera parte (`SELECT 1, 1`) es el **caso base** y la segunda se repite usando la fila anterior hasta que `n < 5` deja de cumplirse.

```text
nombre       | promedio | materias | situacion
-------------+----------+----------+---------------
Sofía Rojas  | 91.5     | 2        | sobre la media
Ana Quispe   | 82.3     | 3        | sobre la media
Luis Mamani  | 52.5     | 2        | bajo la media
Pedro Choque | 44.5     | 2        | bajo la media

n | factorial
--+----------
1 | 1
2 | 2
3 | 6
4 | 24
5 | 120
```

💡 Consejo: cuando una consulta se vuelve ilegible con subconsultas dentro de subconsultas, reescríbela con `WITH`. Mismo resultado, mucho más claro.

🇬🇧 **common table expression** /kómon téibol eksprésshon/ = expresión de tabla común · **recursive** /rikérsiv/ = recursivo · **base case** /béis kéis/ = caso base · **step** /step/ = paso · **readable** /rídabol/ = legible

## 🪟 Funciones de ventana

Las **funciones de ventana** (window functions) calculan algo sobre un grupo de filas **sin colapsarlas**: a diferencia de `GROUP BY`, cada fila sigue apareciendo y gana una columna nueva (su puesto, el total de su grupo, la fila anterior...). La "ventana" se define con `OVER (PARTITION BY ... ORDER BY ...)`.

Analogía: `GROUP BY` es el **acta final** con el promedio de cada curso; una función de ventana es la **lista completa de alumnos** donde al lado de cada uno escribes su puesto en el curso y el promedio del curso.

| Función | Qué devuelve | Ejemplo |
|---|---|---|
| `ROW_NUMBER()` | 1, 2, 3, 4 (sin empates) | Numerar filas |
| `RANK()` | 1, 2, 2, 4 (empate salta) | Ranking olímpico |
| `DENSE_RANK()` | 1, 2, 2, 3 (empate no salta) | Ranking sin huecos |
| `NTILE(4)` | Cuartil 1-4 | Dividir en grupos iguales |
| `SUM(x) OVER (...)` | Suma del grupo o acumulada | Totales corrientes |
| `AVG(x) OVER (...)` | Promedio del grupo | Comparar con la media |
| `LAG(x)` / `LEAD(x)` | Valor de la fila anterior / siguiente | Diferencia con el mes pasado |
| `FIRST_VALUE(x)` / `LAST_VALUE(x)` | Primer / último del grupo | El mejor del curso |

- `OVER ()` :: Ventana = toda la tabla
- `OVER (PARTITION BY curso_id)` :: Una ventana por curso (como GROUP BY, pero sin colapsar)
- `OVER (ORDER BY nota DESC)` :: Ventana ordenada (para rankings y acumulados)
- `OVER (PARTITION BY a ORDER BY b ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)` :: Ventana móvil (media de 3 filas)
- `WINDOW w AS (PARTITION BY curso_id ORDER BY nota DESC)` :: Nombrar una ventana para reutilizarla

### ✅ Ejemplo resuelto: ranking por curso y acumulados

```sql
SELECT c.nombre AS curso,
       a.nombre AS alumno,
       n.nota,
       ROW_NUMBER() OVER w                              AS fila,
       RANK()       OVER w                              AS puesto,
       ROUND(AVG(n.nota) OVER (PARTITION BY n.curso_id), 1) AS prom_curso,
       n.nota - LAG(n.nota) OVER w                      AS dif_con_anterior
FROM notas n
JOIN alumnos a ON a.id = n.alumno_id
JOIN cursos  c ON c.id = n.curso_id
WHERE n.nota IS NOT NULL
WINDOW w AS (PARTITION BY n.curso_id ORDER BY n.nota DESC)
ORDER BY curso, puesto;

-- Top 1 de cada curso usando ROW_NUMBER en una CTE
WITH ranking AS (
    SELECT curso_id, alumno_id, nota,
           ROW_NUMBER() OVER (PARTITION BY curso_id ORDER BY nota DESC) AS rn
    FROM notas
    WHERE nota IS NOT NULL
)
SELECT curso_id, alumno_id, nota,
       SUM(nota) OVER (ORDER BY curso_id) AS suma_acumulada
FROM ranking
WHERE rn = 1;
```

Qué hace cada parte: `PARTITION BY n.curso_id` crea una ventana por curso y `ORDER BY n.nota DESC` ordena dentro de ella; `ROW_NUMBER` numera, `RANK` da el puesto; `AVG(...) OVER (PARTITION BY ...)` pone el promedio del curso en cada fila sin agrupar; `LAG` trae la nota del alumno anterior en la ventana (NULL para el primero) y la restamos. En la segunda consulta, el patrón **"top N por grupo"**: numeras dentro de cada grupo en una CTE y luego filtras `rn = 1` (no se puede filtrar una función de ventana directamente en `WHERE`); `SUM ... OVER (ORDER BY ...)` da una suma acumulada.

```text
curso          | alumno       | nota | fila | puesto | prom_curso | dif_con_anterior
---------------+--------------+------+------+--------+------------+-----------------
Bases de Datos | Sofía Rojas  | 95   | 1    | 1      | 75.0       | NULL
Bases de Datos | Ana Quispe   | 85   | 2    | 2      | 75.0       | -10
Bases de Datos | Luis Mamani  | 45   | 3    | 3      | 75.0       | -40
Cálculo I      | Sofía Rojas  | 88   | 1    | 1      | 65.3       | NULL
Cálculo I      | Ana Quispe   | 70   | 2    | 2      | 65.3       | -18
Cálculo I      | Pedro Choque | 38   | 3    | 3      | 65.3       | -32
Programación I | Ana Quispe   | 92   | 1    | 1      | 67.7       | NULL
Programación I | Luis Mamani  | 60   | 2    | 2      | 67.7       | -32
Programación I | Pedro Choque | 51   | 3    | 3      | 67.7       | -9

curso_id | alumno_id | nota | suma_acumulada
---------+-----------+------+---------------
1        | 3         | 95   | 95
2        | 1         | 92   | 187
3        | 3         | 88   | 275
```

⚠️ Cuidado: las funciones de ventana se calculan **después** de `WHERE` y `GROUP BY`, por eso no se pueden usar en `WHERE`. Envuelve la consulta en una CTE o subconsulta y filtra afuera.

🇬🇧 **window function** /uíndou fánkshon/ = función de ventana · **partition** /partíshon/ = partición · **rank** /rank/ = puesto · **running total** /rániŋ tóutal/ = total acumulado · **preceding / following** /prisíding / fólouing/ = anterior / siguiente

## 🛡️ Restricciones (constraints)

Las **restricciones** son reglas que la base de datos hace cumplir **siempre**, venga el dato de donde venga (tu app, un script, alguien en la consola). Son la última línea de defensa de la calidad de los datos: mejor que la base rechace un dato malo a que lo guarde.

| Restricción | Qué garantiza | Ejemplo |
|---|---|---|
| `PRIMARY KEY` | Único y no nulo; identifica la fila | `id INTEGER PRIMARY KEY` |
| `FOREIGN KEY` / `REFERENCES` | El valor existe en otra tabla | `curso_id REFERENCES cursos(id)` |
| `UNIQUE` | No se repite (NULL sí puede repetirse) | `email TEXT UNIQUE` |
| `NOT NULL` | Obligatorio | `nombre TEXT NOT NULL` |
| `CHECK (cond)` | Cumple una condición | `CHECK (nota BETWEEN 0 AND 100)` |
| `DEFAULT valor` | Valor si no se indica (no restringe, ayuda) | `creditos INTEGER DEFAULT 4` |

| Acción de FK | Qué pasa con las notas si borras un alumno |
|---|---|
| `ON DELETE RESTRICT` / `NO ACTION` (por defecto) | No te deja borrarlo mientras tenga notas |
| `ON DELETE CASCADE` | Borra también sus notas |
| `ON DELETE SET NULL` | Deja `alumno_id` en NULL |
| `ON UPDATE CASCADE` | Si cambia el id, se actualiza en notas |

```sql
CREATE TABLE pagos (
    id          INTEGER PRIMARY KEY,
    alumno_id   INTEGER NOT NULL REFERENCES alumnos(id) ON DELETE CASCADE,
    monto       NUMERIC NOT NULL CHECK (monto > 0),
    metodo      TEXT    NOT NULL CHECK (metodo IN ('efectivo', 'QR', 'tarjeta')),
    fecha       TEXT    NOT NULL DEFAULT CURRENT_DATE,
    CONSTRAINT pago_unico UNIQUE (alumno_id, fecha)
);
```

### ✅ Ejemplo resuelto: la base rechaza datos malos

```sql
PRAGMA foreign_keys = ON;

INSERT OR IGNORE INTO notas (alumno_id, curso_id, nota) VALUES (1, 4, 150);
INSERT OR IGNORE INTO notas (alumno_id, curso_id, nota) VALUES (1, 1, 50);
INSERT OR IGNORE INTO alumnos (nombre, ciudad, email) VALUES ('Clon', 'Potosí', 'ana@umsa.bo');
INSERT OR IGNORE INTO notas (alumno_id, curso_id, nota) VALUES (5, 4, 77);

SELECT COUNT(*) AS notas_totales,
       (SELECT COUNT(*) FROM alumnos) AS alumnos_totales
FROM notas;
```

Qué hace cada parte: `PRAGMA foreign_keys = ON` activa las FK en SQLite; `INSERT OR IGNORE` (propio de SQLite) descarta en silencio las filas que violan una regla, así vemos cuáles entran. 150 viola el `CHECK`; Ana ya tiene nota en el curso 1 (falla la PK compuesta); el email de Ana ya existe (falla `UNIQUE`); solo la última es válida (María en IA), por eso pasamos de 10 a 11 notas y seguimos con 5 alumnos. Sin `OR IGNORE` cada intento fallido daría un error: `CHECK constraint failed`, `UNIQUE constraint failed: notas.alumno_id, notas.curso_id`...

📌 `OR IGNORE` NO salta las claves foráneas: `INSERT INTO notas VALUES (99, 1, 80);` (el alumno 99 no existe) siempre termina con el error `FOREIGN KEY constraint failed` y no inserta nada. Lo verás en acción en el ejemplo de Python.

```text
notas_totales | alumnos_totales
--------------+----------------
11            | 5
```

💡 Consejo: pon nombre a tus restricciones (`CONSTRAINT nota_valida CHECK (...)`): el mensaje de error dirá exactamente qué regla falló.

🇬🇧 **constraint** /konstréint/ = restricción · **unique** /iuník/ = único · **cascade** /kaskéid/ = cascada · **violate** /váioleit/ = violar (incumplir) · **integrity** /intégriti/ = integridad · **reference** /réferens/ = referencia

## ⚡ Índices y rendimiento (EXPLAIN)

Un **índice** es una estructura extra (normalmente un **árbol B**) que permite encontrar filas sin leer toda la tabla. Analogía: el **índice alfabético** al final de un libro: en vez de hojear las 800 páginas buscando "recursión", vas al índice y saltas a la página 312. Sin índice, la base hace un **full table scan** (lee todo).

El precio: los índices ocupan espacio y hacen más lentos los `INSERT`/`UPDATE` (hay que actualizar también el índice). Se crean en las columnas que más usas en `WHERE`, `JOIN` y `ORDER BY`.

- `CREATE INDEX idx_alumnos_ciudad ON alumnos(ciudad);` :: Índice simple
- `CREATE UNIQUE INDEX idx_email ON alumnos(email);` :: Índice que además impide repetidos
- `CREATE INDEX idx_notas_curso_nota ON notas(curso_id, nota);` :: Índice compuesto (el orden de columnas importa)
- `CREATE INDEX idx_activos ON alumnos(ciudad) WHERE email IS NOT NULL;` :: Índice parcial
- `DROP INDEX idx_alumnos_ciudad;` :: Borrar índice
- `EXPLAIN QUERY PLAN SELECT ...;` :: SQLite: cómo va a ejecutar la consulta
- `EXPLAIN ANALYZE SELECT ...;` :: PostgreSQL: plan + tiempos reales
- `ANALYZE;` :: Actualiza estadísticas para que el optimizador elija mejor

### ✅ Ejemplo resuelto: ver el efecto de un índice

```sql
EXPLAIN QUERY PLAN
SELECT nombre FROM alumnos WHERE ciudad = 'La Paz';

CREATE INDEX idx_alumnos_ciudad ON alumnos(ciudad);

EXPLAIN QUERY PLAN
SELECT nombre FROM alumnos WHERE ciudad = 'La Paz';
```

Qué hace cada parte: el primer plan muestra `SCAN alumnos` (leer la tabla entera, fila por fila); después de crear el índice, el plan cambia a `SEARCH alumnos USING INDEX idx_alumnos_ciudad (ciudad=?)`: salta directo a las filas de La Paz. Con 5 filas no se nota, con 5 millones es la diferencia entre 2 segundos y 2 milisegundos. La columna `detail` es la que hay que leer.

```text
id | parent | notused | detail
---+--------+---------+-------------
2  | 0      | 216     | SCAN alumnos

id | parent | notused | detail
---+--------+---------+---------------------------------------------------------
3  | 0      | 62      | SEARCH alumnos USING INDEX idx_alumnos_ciudad (ciudad=?)
```

| Hace que el índice NO se use | Mejor así |
|---|---|
| `WHERE UPPER(nombre) = 'ANA'` (función sobre la columna) | Índice sobre la expresión o guardar normalizado |
| `WHERE nombre LIKE '%quispe'` (comodín al inicio) | `LIKE 'quispe%'` o búsqueda de texto completo |
| `WHERE edad + 1 = 21` | `WHERE edad = 20` |
| Índice `(curso_id, nota)` pero filtras solo por `nota` | El índice compuesto sirve de izquierda a derecha |

⚠️ Cuidado: no indexes todas las columnas "por si acaso". Cada índice frena las escrituras. Mide con `EXPLAIN` antes y después.

💡 Consejo: las claves primarias y `UNIQUE` ya crean índice solos. Lo que casi siempre falta es el índice en las **claves foráneas** (`notas.curso_id`), muy usadas en JOIN.

🇬🇧 **index** /índeks/ = índice · **full table scan** /ful téibol skan/ = recorrido completo de la tabla · **query plan** /kuíri plan/ = plan de ejecución · **optimizer** /óptimaiser/ = optimizador · **bottleneck** /bótol-nek/ = cuello de botella

## 🔒 Transacciones

Una **transacción** agrupa varias operaciones para que se hagan **todas o ninguna**. El ejemplo clásico: transferir 100 Bs. de una cuenta a otra son dos `UPDATE`; si el sistema se cae entre los dos, el dinero desaparecería. Con una transacción, o se aplican ambos o ninguno.

Las propiedades **ACID**:

| Letra | Propiedad | Significa |
|---|---|---|
| A | Atomicidad | Todo o nada |
| C | Consistencia | Las reglas (restricciones) se cumplen antes y después |
| I | Aislamiento (Isolation) | Las transacciones simultáneas no se pisan |
| D | Durabilidad | Lo confirmado sobrevive a un apagón |

- `BEGIN;` :: Empieza una transacción (también `BEGIN TRANSACTION;` o `START TRANSACTION;` en MySQL)
- `COMMIT;` :: Confirma: los cambios quedan guardados
- `ROLLBACK;` :: Deshace todo desde el BEGIN
- `SAVEPOINT punto1;` :: Punto intermedio
- `ROLLBACK TO punto1;` :: Deshace solo hasta el punto intermedio
- `SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;` :: Máximo aislamiento (PostgreSQL)

### ✅ Ejemplo resuelto: transferencia que se deshace

```sql
CREATE TABLE cuentas (id INTEGER PRIMARY KEY, titular TEXT, saldo NUMERIC CHECK (saldo >= 0));
INSERT INTO cuentas VALUES (1, 'Ana', 500), (2, 'Luis', 100);

BEGIN;
UPDATE cuentas SET saldo = saldo - 200 WHERE id = 1;
UPDATE cuentas SET saldo = saldo + 200 WHERE id = 2;
COMMIT;

BEGIN;
UPDATE cuentas SET saldo = saldo + 1000 WHERE id = 2;
SAVEPOINT antes_de_retirar;
UPDATE cuentas SET saldo = saldo - 50 WHERE id = 1;
ROLLBACK TO antes_de_retirar;
ROLLBACK;

SELECT titular, saldo FROM cuentas;
```

Qué hace cada parte: la primera transacción mueve 200 Bs. de Ana a Luis y `COMMIT` la confirma; la segunda suma 1000 a Luis, marca un `SAVEPOINT`, resta 50 a Ana, vuelve al savepoint (deshace solo los 50) y al final `ROLLBACK` deshace también los 1000. Resultado: solo cuenta la primera transferencia. En una app real, si un `UPDATE` falla (por ejemplo el `CHECK (saldo >= 0)`), tu código hace `ROLLBACK` y nada queda a medias.

```text
titular | saldo
--------+------
Ana     | 300
Luis    | 300
```

⚠️ Cuidado: una transacción abierta y olvidada bloquea filas o tablas para los demás. Haz `COMMIT` o `ROLLBACK` cuanto antes.

💡 Consejo: insertar 100 000 filas dentro de un solo `BEGIN ... COMMIT` es muchísimo más rápido que 100 000 inserciones sueltas (cada una sería su propia transacción).

🇬🇧 **transaction** /transákshon/ = transacción · **commit** /komít/ = confirmar · **rollback** /róul-bak/ = deshacer · **atomic** /atómik/ = atómico · **isolation** /aisoléishon/ = aislamiento · **lock** /lok/ = bloqueo

## 🧹 Normalización y vistas

La **normalización** es organizar las tablas para **no repetir datos**. Si el nombre del docente está escrito en cada fila de notas, cuando cambie tendrás que corregirlo en 300 sitios (y se te olvidará alguno). Regla práctica: **cada dato se guarda en un solo lugar** y las demás tablas lo referencian por su clave.

| Forma normal | Regla | Ejemplo de violación |
|---|---|---|
| 1FN | Valores atómicos: una celda = un valor; sin grupos repetidos | `cursos = 'BD, Cálculo, IA'` en una sola celda |
| 2FN | 1FN + cada columna depende de TODA la clave (no de parte) | En `notas(alumno_id, curso_id, nota, nombre_curso)`, `nombre_curso` depende solo de `curso_id` |
| 3FN | 2FN + ninguna columna depende de otra que no sea clave | `alumnos(id, ciudad, departamento)`: departamento depende de ciudad |

```text
❌ ANTES (una tabla, todo repetido)
| alumno | ciudad | curso          | docente      | nota |
| Ana    | La Paz | Bases de Datos | Ing. Vargas  | 85   |
| Ana    | La Paz | Cálculo I      | Lic. Gutiérrez | 70 |
| Luis   | Cbba   | Bases de Datos | Ing. Vargas  | 45   |

✅ DESPUÉS (3 tablas: cada dato una sola vez)
alumnos(id, nombre, ciudad)
cursos(id, nombre, docente)
notas(alumno_id -> alumnos.id, curso_id -> cursos.id, nota)
```

💡 Consejo: normaliza hasta 3FN por defecto. Desnormalizar (repetir datos a propósito) se hace solo por rendimiento, medido, en sistemas de análisis o caché.

### 👁️ Vistas

Una **vista** es una consulta guardada con nombre que se usa como si fuera una tabla. No guarda datos (se recalcula cada vez): es un "atajo" para consultas largas que usas mucho y una forma de mostrar solo ciertas columnas a ciertos usuarios.

- `CREATE VIEW v AS SELECT ...;` :: Crear una vista
- `SELECT * FROM v WHERE ...;` :: Usarla como una tabla
- `DROP VIEW IF EXISTS v;` :: Borrarla
- `CREATE OR REPLACE VIEW v AS ...;` :: Reemplazarla (PostgreSQL/MySQL; en SQLite: DROP + CREATE)
- `CREATE MATERIALIZED VIEW mv AS ...;` :: Vista que SÍ guarda el resultado (PostgreSQL); se actualiza con `REFRESH MATERIALIZED VIEW mv;`

### ✅ Ejemplo resuelto: vista de boletín

```sql
CREATE VIEW boletin AS
SELECT a.nombre AS alumno,
       c.nombre AS curso,
       c.creditos,
       n.nota,
       CASE WHEN n.nota >= 51 THEN 'Aprobado'
            WHEN n.nota IS NULL THEN 'Pendiente'
            ELSE 'Reprobado' END AS estado
FROM notas n
JOIN alumnos a ON a.id = n.alumno_id
JOIN cursos  c ON c.id = n.curso_id;

SELECT alumno, SUM(creditos) AS creditos_aprobados
FROM boletin
WHERE estado = 'Aprobado'
GROUP BY alumno
ORDER BY creditos_aprobados DESC;

SELECT * FROM boletin WHERE estado <> 'Aprobado' ORDER BY alumno;
```

Qué hace cada parte: la vista `boletin` esconde los dos JOIN y el CASE; después, las consultas sobre ella son cortas y legibles, como si existiera una tabla `boletin`. La primera suma los créditos aprobados por alumno; la segunda lista lo pendiente o reprobado. Si mañana cambia una nota, la vista lo refleja sola.

```text
alumno       | creditos_aprobados
-------------+-------------------
Ana Quispe   | 16
Sofía Rojas  | 10
Pedro Choque | 6
Luis Mamani  | 6

alumno       | curso          | creditos | nota | estado
-------------+----------------+----------+------+----------
Luis Mamani  | Bases de Datos | 5        | 45   | Reprobado
Pedro Choque | Cálculo I      | 5        | 38   | Reprobado
Sofía Rojas  | Programación I | 6        | NULL | Pendiente
```

🇬🇧 **normalization** /normalizéishon/ = normalización · **redundancy** /ridándansi/ = redundancia · **normal form** /nórmal form/ = forma normal · **view** /viú/ = vista · **materialized** /matírializd/ = materializada

## ⚖️ SQLite vs PostgreSQL vs MySQL

Los tres hablan SQL, pero cada uno tiene su "acento". **SQLite** es un archivo (sin servidor): perfecto para apps móviles, prototipos, tests y aprender. **PostgreSQL** es el más completo y estricto: el favorito para backends serios y para IA (extensión `pgvector`). **MySQL/MariaDB** es muy popular en hosting web y WordPress.

| Tema | SQLite | PostgreSQL | MySQL / MariaDB |
|---|---|---|---|
| Arquitectura | Un archivo, sin servidor | Servidor cliente/servidor | Servidor cliente/servidor |
| Id autoincremental | `INTEGER PRIMARY KEY` | `GENERATED ALWAYS AS IDENTITY` o `SERIAL` | `INT AUTO_INCREMENT` |
| Tipos | Flexibles (puedes meter texto en INTEGER) | Estrictos y muy ricos (JSONB, arrays, UUID) | Estrictos (en modo estricto) |
| Booleanos | 0 / 1 | `BOOLEAN` real (`true`/`false`) | `TINYINT(1)` |
| Concatenar texto | `\|\|` | `\|\|` | `CONCAT(a, b)` |
| Unir textos agrupados | `GROUP_CONCAT` | `STRING_AGG` | `GROUP_CONCAT` |
| Fecha actual | `DATE('now')` | `CURRENT_DATE`, `NOW()` | `CURDATE()`, `NOW()` |
| LIKE sin mayúsculas | `LIKE` ya ignora mayúsculas (ASCII) | `ILIKE` | Depende de la collation (normalmente sí) |
| Comillas de nombres | `"col"` | `"col"` | `` `col` `` |
| Upsert | `ON CONFLICT DO UPDATE` | `ON CONFLICT DO UPDATE` | `ON DUPLICATE KEY UPDATE` |
| `RETURNING` | Sí (3.35+) | Sí | No (MariaDB sí) |
| `FULL JOIN` | Sí (3.39+) | Sí | No (se simula con UNION) |
| Ver tablas | `.tables` | `\dt` | `SHOW TABLES;` |
| Ver estructura | `.schema t` | `\d t` | `DESCRIBE t;` |
| Cliente de terminal | `sqlite3 base.db` | `psql -U usuario -d base` | `mysql -u usuario -p base` |
| Placeholder en Python | `?` | `%s` (psycopg) | `%s` |

- `docker run -d --name pg -e POSTGRES_PASSWORD=clave -p 5432:5432 postgres:16` :: Levantar PostgreSQL para practicar (ver la hoja de Docker)
- `psql -h localhost -U postgres` :: Conectarse a PostgreSQL
- `\l`, `\c base`, `\dt`, `\d tabla`, `\q` :: psql: listar bases, cambiar de base, tablas, estructura, salir

💡 Consejo: aprende con SQLite y pasa a PostgreSQL para proyectos reales. El 95 % del SQL de esta hoja funciona igual en ambos.

🇬🇧 **server** /sérver/ = servidor · **client** /kláient/ = cliente · **engine** /énchin/ = motor · **dialect** /dáialekt/ = dialecto · **lightweight** /láit-uéit/ = ligero · **embedded** /imbéded/ = embebido

## 🐍 SQL desde Python (sqlite3) e inyección SQL

Python trae `sqlite3` de serie. El flujo siempre es: **conectar → cursor/ejecutar → leer resultados → commit → cerrar**. Para PostgreSQL es casi igual con `psycopg` (`pip install "psycopg[binary]"`).

La regla más importante: **nunca construyas SQL pegando texto del usuario** (con f-strings o `+`). Usa **parámetros** (`?` en SQLite, `%s` en psycopg) y deja que la librería los inserte de forma segura. Si no, sufres **inyección SQL**: un usuario escribe `' OR '1'='1` en el formulario y ve (o borra) toda tu base.

Analogía: los parámetros son como un **formulario con casillas**: lo que el usuario escribe va dentro de la casilla y nunca puede cambiar las instrucciones del formulario. Pegar texto es como dejar que el usuario reescriba las instrucciones.

- `con = sqlite3.connect("escuela.db")` :: Abrir (o crear) una base; `":memory:"` para una en RAM
- `con.execute("SELECT ... WHERE id = ?", (5,))` :: Parámetro posicional (ojo: tupla con coma)
- `con.execute("... WHERE nombre = :n", {"n": "Ana"})` :: Parámetro con nombre
- `con.executemany("INSERT ... VALUES (?, ?)", lista_de_tuplas)` :: Insertar muchas filas
- `cur.fetchone(), cur.fetchall(), cur.fetchmany(10)` :: Leer una, todas, de a 10
- `con.row_factory = sqlite3.Row` :: Filas accesibles por nombre: `fila["nombre"]`
- `with con:` :: Transacción: commit automático al salir, rollback si hay excepción
- `cur.lastrowid` :: Id de la última fila insertada
- `pd.read_sql("SELECT ...", con)` :: Consulta directo a un DataFrame de pandas

### ✅ Ejemplo resuelto: CRUD seguro e intento de inyección

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.row_factory = sqlite3.Row
con.execute("PRAGMA foreign_keys = ON")
con.executescript("""
    CREATE TABLE usuarios (id INTEGER PRIMARY KEY, usuario TEXT UNIQUE, clave TEXT);
    CREATE TABLE compras (id INTEGER PRIMARY KEY,
                          usuario_id INTEGER REFERENCES usuarios(id),
                          monto REAL);
""")

with con:
    con.executemany("INSERT INTO usuarios (usuario, clave) VALUES (?, ?)",
                    [("ana", "x1"), ("luis", "x2"), ("sofia", "x3")])
    con.executemany("INSERT INTO compras (usuario_id, monto) VALUES (?, ?)",
                    [(1, 50.0), (1, 25.5), (2, 100.0)])

def login_inseguro(usuario, clave):
    sql = f"SELECT usuario FROM usuarios WHERE usuario = '{usuario}' AND clave = '{clave}'"
    return [f["usuario"] for f in con.execute(sql)]

def login_seguro(usuario, clave):
    sql = "SELECT usuario FROM usuarios WHERE usuario = ? AND clave = ?"
    return [f["usuario"] for f in con.execute(sql, (usuario, clave))]

ataque = "' OR '1'='1"
print("Inseguro:", login_inseguro("nadie", ataque))
print("Seguro:  ", login_seguro("nadie", ataque))

consulta = """
    SELECT u.usuario, COUNT(c.id) AS compras, COALESCE(SUM(c.monto), 0) AS total
    FROM usuarios u LEFT JOIN compras c ON c.usuario_id = u.id
    GROUP BY u.id HAVING total >= ? ORDER BY total DESC
"""
for fila in con.execute(consulta, (0,)):
    print(f"{fila['usuario']:<6} {fila['compras']} compras  {fila['total']:>7.2f} Bs.")

try:
    with con:
        con.execute("INSERT INTO compras (usuario_id, monto) VALUES (?, ?)", (3, 10.0))
        con.execute("INSERT INTO compras (usuario_id, monto) VALUES (?, ?)", (99, 10.0))
except sqlite3.IntegrityError as e:
    print("Rollback por:", e)
print("Compras guardadas:", con.execute("SELECT COUNT(*) FROM compras").fetchone()[0])
con.close()
```

Qué hace cada parte: `":memory:"` crea una base temporal en RAM; `row_factory = sqlite3.Row` deja leer columnas por nombre; `executescript` ejecuta varias sentencias de golpe; `with con:` hace commit al terminar el bloque. En `login_inseguro`, la f-string mete el texto del atacante dentro del SQL y la condición se convierte en `... clave = '' OR '1'='1'`, que siempre es verdadera: ¡devuelve todos los usuarios! En `login_seguro` el `?` trata el texto como un **dato**, nunca como código, y no encuentra a nadie. La consulta agregada usa un parámetro también para el número. Al final, el `with con:` ve el `IntegrityError` de la FK (usuario 99 no existe) y deshace **también** la compra válida de Sofía: todo o nada.

```text
Inseguro: ['ana', 'luis', 'sofia']
Seguro:   []
luis   1 compras   100.00 Bs.
ana    2 compras    75.50 Bs.
sofia  0 compras     0.00 Bs.
Rollback por: FOREIGN KEY constraint failed
Compras guardadas: 3
```

⚠️ Cuidado: los parámetros sirven para **valores**, no para nombres de tablas o columnas (`SELECT * FROM ?` no funciona). Si necesitas un nombre dinámico, compruébalo contra una lista blanca de nombres permitidos.

⚠️ Cuidado: un solo parámetro necesita una tupla con coma: `(5,)`. Escribir `(5)` es solo el número 5 entre paréntesis y da error.

⚠️ Cuidado: nunca guardes contraseñas en texto plano como en este ejemplo didáctico. Usa un hash lento como `bcrypt` o `argon2`.

🇬🇧 **SQL injection** /es-kiu-él inyékshon/ = inyección SQL · **placeholder** /pléis-jóulder/ = marcador de parámetro · **cursor** /kérsor/ = cursor · **fetch** /fech/ = traer · **sanitize** /sánitais/ = desinfectar (limpiar entradas) · **allowlist** /aláu-list/ = lista blanca

## 🏋️ Ejercicios resueltos (alumnos, cursos, notas)

Intenta cada uno antes de mirar la solución. Todos usan la base de ejemplo de la sección "🏗️ Crear tablas".

### ✅ Ejemplo resuelto: ejercicio 1, promedio ponderado por créditos

Enunciado: calcula el promedio de cada alumno **ponderado por créditos** (un curso de 6 créditos pesa más que uno de 4). Solo notas no nulas. Ordena de mayor a menor.

```sql
SELECT a.nombre,
       ROUND(SUM(n.nota * c.creditos) * 1.0 / SUM(c.creditos), 2) AS ponderado,
       SUM(c.creditos) AS creditos_cursados
FROM notas n
JOIN alumnos a ON a.id = n.alumno_id
JOIN cursos  c ON c.id = n.curso_id
WHERE n.nota IS NOT NULL
GROUP BY a.id
ORDER BY ponderado DESC;
```

Qué hace cada parte: multiplica cada nota por los créditos del curso, suma, y divide entre el total de créditos; el `* 1.0` fuerza división decimal (en SQLite y PostgreSQL, entero / entero da entero).

```text
nombre       | ponderado | creditos_cursados
-------------+-----------+------------------
Sofía Rojas  | 91.5      | 10
Ana Quispe   | 82.94     | 16
Luis Mamani  | 53.18     | 11
Pedro Choque | 45.09     | 11
```

### ✅ Ejemplo resuelto: ejercicio 2, cursos sin alumnos y alumnos sin cursos

Enunciado: en una sola consulta, lista los cursos sin inscritos y los alumnos sin cursos, indicando el tipo.

```sql
SELECT 'curso sin alumnos' AS tipo, c.nombre AS nombre
FROM cursos c
LEFT JOIN notas n ON n.curso_id = c.id
WHERE n.curso_id IS NULL
UNION ALL
SELECT 'alumno sin cursos', a.nombre
FROM alumnos a
WHERE a.id NOT IN (SELECT alumno_id FROM notas);
```

Qué hace cada parte: la primera mitad es un **anti-join** (`LEFT JOIN` + `IS NULL`); la segunda usa `NOT IN` (seguro aquí porque `alumno_id` es `NOT NULL`); `UNION ALL` pega los dos resultados uno debajo del otro (deben tener el mismo número de columnas). `UNION` a secas además quitaría duplicados.

```text
tipo              | nombre
------------------+------------------------
curso sin alumnos | Inteligencia Artificial
alumno sin cursos | María Flores
```

### ✅ Ejemplo resuelto: ejercicio 3, reprobados por curso y el docente

Enunciado: por cada curso, cuántos reprobaron (nota menor a 51) y el porcentaje respecto a los que tienen nota. Muestra también el docente o "Sin asignar".

```sql
SELECT c.nombre AS curso,
       COALESCE(c.docente, 'Sin asignar') AS docente,
       COUNT(n.nota) AS evaluados,
       SUM(CASE WHEN n.nota < 51 THEN 1 ELSE 0 END) AS reprobados,
       ROUND(100.0 * SUM(CASE WHEN n.nota < 51 THEN 1 ELSE 0 END) / NULLIF(COUNT(n.nota), 0), 1) AS pct_reprobados
FROM cursos c
LEFT JOIN notas n ON n.curso_id = c.id
GROUP BY c.id
ORDER BY pct_reprobados DESC;
```

Qué hace cada parte: el `LEFT JOIN` conserva el curso de IA aunque no tenga notas; `NULLIF(COUNT(n.nota), 0)` convierte 0 en NULL para no dividir entre cero (el resultado queda NULL en vez de error); `100.0 *` evita la división entera. En SQLite los NULL van primero al ordenar ascendente y últimos en descendente.

```text
curso                   | docente        | evaluados | reprobados | pct_reprobados
------------------------+----------------+-----------+------------+---------------
Bases de Datos          | Ing. Vargas    | 3         | 1          | 33.3
Cálculo I               | Lic. Gutiérrez | 3         | 1          | 33.3
Programación I          | Lic. Torrez    | 3         | 0          | 0.0
Inteligencia Artificial | Sin asignar    | 0         | 0          | NULL
```

### ✅ Ejemplo resuelto: ejercicio 4, el mejor alumno de cada ciudad

Enunciado: para cada ciudad, el alumno con mejor promedio (con funciones de ventana).

```sql
WITH prom AS (
    SELECT a.ciudad, a.nombre, ROUND(AVG(n.nota), 1) AS promedio
    FROM alumnos a
    JOIN notas n ON n.alumno_id = a.id
    GROUP BY a.id
),
ranking AS (
    SELECT *, RANK() OVER (PARTITION BY ciudad ORDER BY promedio DESC) AS puesto
    FROM prom
)
SELECT ciudad, nombre, promedio
FROM ranking
WHERE puesto = 1
ORDER BY promedio DESC;
```

Qué hace cada parte: la primera CTE calcula el promedio de cada alumno; la segunda los numera dentro de cada ciudad con `RANK` (si dos empatan, ambos salen con puesto 1); la consulta final se queda con los primeros. María no aparece porque el `JOIN` (inner) la descarta al no tener notas.

```text
ciudad     | nombre      | promedio
-----------+-------------+---------
Santa Cruz | Sofía Rojas | 91.5
La Paz     | Ana Quispe  | 82.3
Cochabamba | Luis Mamani | 52.5
```

### ✅ Ejemplo resuelto: ejercicio 5, subir 5 puntos a los reprobados de Cálculo

Enunciado: el docente de Cálculo I decide subir 5 puntos (máximo 100) a quienes reprobaron. Hazlo de forma segura y comprueba.

```sql
BEGIN;

SELECT alumno_id, nota FROM notas
WHERE curso_id = (SELECT id FROM cursos WHERE nombre = 'Cálculo I') AND nota < 51;

UPDATE notas
SET nota = MIN(nota + 5, 100)
WHERE curso_id = (SELECT id FROM cursos WHERE nombre = 'Cálculo I')
  AND nota < 51;

SELECT a.nombre, n.nota
FROM notas n JOIN alumnos a ON a.id = n.alumno_id
WHERE n.curso_id = 3
ORDER BY n.nota DESC;

COMMIT;
```

Qué hace cada parte: primero un `SELECT` con el mismo `WHERE` para ver a quién afectará (Pedro, con 38); luego el `UPDATE` usa una subconsulta para encontrar el id del curso por su nombre y `MIN(nota + 5, 100)` (en PostgreSQL sería `LEAST`) para no pasar de 100; se comprueba el resultado y se confirma con `COMMIT` (si algo saliera mal, `ROLLBACK`).

```text
alumno_id | nota
----------+-----
4         | 38

nombre       | nota
-------------+-----
Sofía Rojas  | 88
Ana Quispe   | 70
Pedro Choque | 43
```

💡 Consejo: para seguir practicando, inventa preguntas sobre esta base ("¿qué docente tiene el mejor promedio?", "¿qué alumno lleva más créditos?") y resuélvelas primero en español, luego en SQL, paso a paso con `WITH`.

📌 Resumen mental de una consulta: `SELECT` columnas `FROM` tabla `JOIN` otras `ON` claves `WHERE` filtro de filas `GROUP BY` grupos `HAVING` filtro de grupos `ORDER BY` orden `LIMIT` cuántas.

🇬🇧 **exercise** /éksersais/ = ejercicio · **weighted average** /uéited áverech/ = promedio ponderado · **union** /iúnion/ = unión · **failed / passed** /féild / pást/ = reprobado / aprobado · **"Let's break it down"** /lets bréik it dáun/ = "Vamos a desglosarlo"
