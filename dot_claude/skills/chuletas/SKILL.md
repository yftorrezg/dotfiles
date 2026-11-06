---
name: chuletas
description: Crear, auditar o mejorar las hojas de apuntes/chuletas de cualquier curso o tema del usuario (visor SUPER+SHIFT+C, archivos ~/.config/hypr/chuletas/NN-tema.md). Úsalo cuando pida apuntes, chuleta, cheatsheet, resumen o guía de un curso, materia de la facultad, herramienta o tecnología, o cuando pida revisar, auditar, corregir o actualizar una hoja existente.
---

# Chuletas: crear y auditar hojas de estudio

El usuario estudia Ciencias de la Computación / IA en Bolivia, aprende leyendo y quiere entender el **porqué**.
Exige que todo sea **verídico, nada inventado**. Responde y escribe siempre en español.
Una hoja se juzga por dos cosas: **¿es verdad todo lo que dice?** y **¿le enseña bien?**

## Archivos

- Hojas: `~/.config/hypr/chuletas/NN-tema.md` (NN = orden de la pestaña). Imágenes: `chuletas/img/<tema>/`.
- Formato obligatorio: leer `~/.config/hypr/chuletas/FORMATO.md` antes de escribir.
- Validador (debe salir con código 0): `python3 ~/.config/hypr/scripts/chuletas_md.py validar <hoja.md>`
- Herramientas de esta skill (`~/.claude/skills/chuletas/scripts/`):
  - `bloques.py hoja.md [--lenguaje sql] [--ver LÍNEA]`: lista los bloques de código y su "salida esperada".
  - `probar_sql.py hoja.md --base LÍNEA [--motor postgres]`: ejecuta cada ```sql en una base nueva y compara con su salida.
  - `esquemas.py <salida> <ancho> hojas...`: dibuja los esquemas a PNG (900 = pantalla completa, 420 = panel lateral).

## Regla de oro: la verdad se comprueba, no se recuerda

Orden de fuentes (usa la más alta que exista):
1. **Ejecutarlo**: el código de la hoja se corre en el motor o programa real, y se pega la salida real.
   - Motores en este PC: `sqlite3`, Python, Docker (`postgres:18-alpine`; la imagen `gvenzl/oracle-xe:21-slim` ya está bajada
     para Oracle/PL/SQL). Contenedores temporales con `--rm` y nombre `*-auditoria`; al terminar, `docker stop`.
   - Sin hardware (Arduino, ESP32, Raspberry Pi): compila al menos (`arduino-cli compile`, `platformio`) si está instalado,
     y verifica pines y límites eléctricos en la hoja de datos oficial. Di qué se compiló y qué no se probó en la placa.
2. **La versión instalada**: `programa --version`, `--help`, y el código fuente del **tag exacto** de esa versión.
   Los snapshots de pruebas (`*.snap`) son el texto real de la interfaz.
3. **Documentación oficial** de esa versión (docs del fabricante, RFC, hojas de datos, estándares).
4. Fuentes secundarias serias (OWASP, artículos con autor y fecha). Cita la fuente en la hoja.

Nunca presentes como hecho algo que no verificaste: o lo compruebas, o lo quitas, o lo marcas como
"aproximado / ilustrativo". Las cifras de rendimiento van con "medido en este PC" y cómo se midió, o con fuente y año.
Las fechas de historia solo si las confirmaste. Si una herramienta cambia rápido, anota la versión de la hoja.

## Crear una hoja nueva

1. **Alcance**: si es una materia de la facultad, pide el sílabo o los temas al usuario (o búscalo en el material que tenga).
   Pregunta qué hardware o software tiene de verdad (modelo exacto: "Raspberry Pi 4 Model B 2 GB").
2. **Investiga** con el orden de fuentes de arriba. Anota la versión de cada cosa.
3. **Esqueleto** (adáptalo al tema; no todas las secciones aplican):
   - `🧭 Resumen en 30 segundos`: tabla de lo más usado (atajos, comandos, fórmulas).
   - `🧠 Qué es y por qué existe`: el problema que resuelve, con una analogía.
   - Historia solo verificada (```tiempo).
   - El núcleo: secciones por tema con **ejemplo resuelto** + salida real en cada una.
   - Comparativas en tabla (X vs Y, cuándo usar qué) y ::: columnas para mal/bien.
   - `❌ Errores típicos`: error → causa → solución (casos reales cuando los hay).
   - `🏋️ Ejercicios` con la solución en ::: desplegable (de 🟢 fácil a 🔴 difícil).
   - `🎤 Preguntas de examen o entrevista` en desplegables.
   - `🇬🇧 Vocabulario`: tabla `English | Suena | Español`, con la pronunciación escrita a la española
     (`database | déita-beis | base de datos`), nunca en IPA. Incluye 1–2 frases útiles.
   - `📌 Resumen final tipo chuleta`.
4. **Un ejemplo que atraviesa toda la hoja** (como la base `universidad` de 10-sql.md): datos de Bolivia
   (La Paz, Cochabamba, Bs.), casos especiales a propósito (un NULL, alguien sin datos), siempre los mismos.
5. Escribe, valida, dibuja los esquemas, mira los PNG, corrige, sincroniza (ver abajo).

## Auditar una hoja existente

Lee la hoja **entera** (por partes con offset/limit) antes de juzgar. Luego:

1. **Ejecuta** todo el código posible (`probar_sql.py`, o extrae con `bloques.py` y corre en Python/compilador).
   Cada "DIFIERE" se revisa a mano: puede ser un recorte a propósito, un bloque que depende de otro,
   o un error de verdad. Si no se puede reproducir porque falta crear algo, agrega un desplegable 🧪 con el setup.
2. **Hechos**: versiones vigentes (¿la imagen o versión recomendada sigue siendo la actual?), afirmaciones del tipo
   "X hace Y" (pruébalas en el motor), parámetros de seguridad (contra OWASP vigente), fechas e historia, licencias.
3. **Enseñanza**: ¿explica el porqué? ¿tiene ejemplo resuelto por sección? ¿errores comunes? ¿ejercicios con solución?
   ¿le sirve para su examen de la facultad (sílabo)? ¿lo que falta es importante o es relleno?
4. **Formato**: validador, esquemas legibles a 900 y 420 px, tablas de 2–5 columnas, vocabulario con pronunciación.
5. **Informe al usuario** antes o junto con los cambios: tabla `Hallazgo | Gravedad | Prueba | Arreglo`, separando
   lo comprobado de lo que es opinión. Di también lo que está bien (con evidencia: "31 de 52 bloques idénticos").
6. Aplica los arreglos con reemplazos exactos (un script Python con `assert t.count(viejo) == 1`), guarda una copia
   de la hoja original en el scratchpad, valida y vuelve a ejecutar para confirmar.

Gravedad: 🔴 enseña algo falso o el ejemplo da otro resultado · 🟠 desactualizado o incompleto en algo que importa ·
🟡 mejora de claridad o reproducibilidad.

## Errores del validador que ya salieron

- Una entrada rápida debe ser exactamente `` - `código` :: explicación ``: el código va entre comillas invertidas
  **al inicio**; texto antes del `::` fuera de las comillas da error.
- Tablas de 2 a 5 columnas (no dejes celdas de encabezado vacías para simular grupos: usa una columna "Grupo").
- Evita la doble comilla invertida (`` `` ` `` ``) en entradas: escribe "comilla invertida".
- Nada de `####`, HTML ni enlaces.

## Sincronizar (PC ↔ laptop)

Lee `~/.local/share/chezmoi/CLAUDE.md` si no lo hiciste en la sesión. Archivo nuevo: `chezmoi add <ruta>`;
luego `dotsync subir`. Archivos ya gestionados: basta `dotsync subir`. No abras el visor SUPER+SHIFT+C por tu cuenta
mientras el usuario trabaja (el panel toma el teclado); verifica con el validador y `esquemas.py`.

## Tono con el usuario

Directo y honesto: si algo de una hoja está mal, dilo con la prueba; si está bien, también. Explica brevemente el
porqué de cada corrección: el usuario aprende de las correcciones tanto como de las hojas.
