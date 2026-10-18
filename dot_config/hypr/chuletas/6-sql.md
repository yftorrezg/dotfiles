# 🗃️ SQL
Cada línea: código :: explicación. Edita este archivo para añadir las tuyas.

## Consultar
SELECT * FROM alumnos; :: Todas las columnas y filas
SELECT nombre, edad FROM alumnos WHERE edad >= 18; :: Columnas concretas con filtro
WHERE nombre LIKE 'A%' :: Empieza por A (% = cualquier cosa)
WHERE edad BETWEEN 18 AND 25 AND activo = 1 :: Rango y varias condiciones
WHERE ciudad IN ('La Paz', 'Cochabamba') :: Uno de varios valores
ORDER BY edad DESC LIMIT 10; :: Ordenar de mayor a menor, solo 10
SELECT DISTINCT ciudad FROM alumnos; :: Sin repetidos

## Agrupar
SELECT COUNT(*), AVG(nota), MAX(nota) FROM notas; :: Contar, promedio, máximo
SELECT ciudad, COUNT(*) FROM alumnos GROUP BY ciudad; :: Contar por grupo
... GROUP BY ciudad HAVING COUNT(*) > 5; :: Filtrar grupos (WHERE es para filas)

## Unir tablas
SELECT a.nombre, c.titulo FROM alumnos a JOIN cursos c ON c.id = a.curso_id; :: Solo los que coinciden
LEFT JOIN cursos c ON c.id = a.curso_id :: Todos los alumnos, aunque no tengan curso

## Modificar
INSERT INTO alumnos (nombre, edad) VALUES ('Ana', 20); :: Insertar fila
UPDATE alumnos SET edad = 21 WHERE id = 3; :: Cambiar (¡siempre con WHERE!)
DELETE FROM alumnos WHERE id = 3; :: Borrar (¡siempre con WHERE!)

## Tablas
CREATE TABLE alumnos (id INTEGER PRIMARY KEY, nombre TEXT NOT NULL, edad INT); :: Crear tabla
ALTER TABLE alumnos ADD COLUMN email TEXT; :: Añadir columna
CREATE INDEX idx_nombre ON alumnos(nombre); :: Índice: búsquedas más rápidas
DROP TABLE alumnos; :: Borrar la tabla entera
