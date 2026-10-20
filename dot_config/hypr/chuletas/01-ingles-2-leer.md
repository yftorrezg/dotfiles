# 🇬🇧 Inglés 2 · Gramática, errores y docs
> Gramática para leer y escribir docs, verbos y nombres de código, mensajes de error reales, documentación, licencias y falsos amigos.

## 🧭 Cómo usar esta hoja

Esta hoja es para **leer** inglés técnico sin traductor y **escribirlo** sin los errores típicos del hispanohablante. La documentación y los errores usan una gramática muy pequeña y muy repetitiva: si dominas unas 15 estructuras, entiendes casi todo.

| Parte de la hoja | Qué aprendes | Para qué te sirve |
|---|---|---|
| Gramática (tiempos, pasiva, modales...) | Cómo están construidas las frases de las docs | Leer rápido y escribir bien |
| Errores de hispanohablantes | Lo que todos hacemos mal | No pasar vergüenza en un PR |
| Verbos y nombres | Qué significa cada verbo de función | Entender código ajeno por los nombres |
| Mensajes de error | Más de 150 mensajes reales traducidos | Arreglar bugs sin pánico |
| Documentación y licencias | Partes de una doc, firmas, `--help`, MIT/GPL | Usar librerías bien y legalmente |
| Falsos amigos | Palabras que engañan | No entender lo contrario |

| Nivel | Señal de que lo dominas | Siguiente paso |
|---|---|---|
| 🌱 Principiante | Traduces cada error con el traductor | Lee solo la última línea y busca las palabras clave de la tabla de errores |
| 🌿 Intermedio | Entiendes los errores pero no las docs largas | Lee cada día la sección "Parameters" y "Returns" de una función |
| 🌳 Avanzado | Lees docs sin traductor | Escribe issues y respuestas en Stack Overflow |

💡 Consejo: cada vez que veas un error o una frase de doc que no entiendes, búscala en esta hoja (el visor tiene búsqueda) y **cópiala en tu libreta con su traducción**. Así aprendes de tus propios bugs.

📌 Regla de oro de toda la hoja: **en inglés técnico el sujeto siempre aparece, los verbos de tercera persona llevan -s, y los sustantivos contables en singular llevan artículo**.

## ⏳ Tiempos verbales en docs, logs y changelogs

Cada tipo de texto técnico usa **su** tiempo verbal: las docs usan presente simple, los logs presente continuo, los changelogs pasado o imperativo, los avisos de deprecación presente perfecto. Si reconoces el tiempo, sabes **qué tipo de información** estás leyendo.

### 🗺️ Mapa rápido: qué tiempo usa cada texto

| Texto técnico | Tiempo verbal | Ejemplo real | Por qué |
|---|---|---|---|
| Documentación de API | Presente simple | "Returns a new list." | Describe lo que pasa **siempre** |
| Logs y barras de progreso | Presente continuo | "Downloading packages..." | Está pasando **ahora** |
| Changelog, release notes | Pasado simple o imperativo | "Fixed a memory leak." | Ya ocurrió en esa versión |
| Avisos de deprecación | Presente perfecto | "has been deprecated" | Pasó antes y **sigue** vigente |
| Avisos de futuro | Futuro con will | "will be removed in 3.0" | Ocurrirá |
| Tutoriales, commits | Imperativo | "Install the package." | Es una orden o un paso |
| Mensajes de error | Pasado o presente | "Build failed." / "File not found." | Resultado de una acción |
| Planes en issues | going to / will | "I'm going to refactor this." | Intención |

### 1️⃣ Presente simple: la voz de la documentación

Describe hechos permanentes: qué hace una función, qué acepta, qué devuelve. Con **he/she/it** (y cualquier sujeto en singular: "the function", "this method") el verbo lleva **-s**.

| Estructura | Cuándo se usa | Ejemplo en docs/código | Traducción |
|---|---|---|---|
| Sujeto + verbo(**-s**) | Qué hace siempre | "The function **returns** a list." | La función devuelve una lista. |
| Sujeto + verbo(**-s**) + objeto | Qué recibe | "This method **takes** two arguments." | Este método recibe dos argumentos. |
| Sujeto + **does not** + verbo | Lo que no hace | "It **does not modify** the original." | No modifica el original. |
| **Does** + sujeto + verbo? | Preguntas en foros | "**Does** it **support** async?" | ¿Soporta async? |
| Verbo(**-s**) al inicio (sin sujeto) | Docstrings resumidos | "**Raises** `ValueError` if empty." | Lanza ValueError si está vacío. |
| There **is** / There **are** | Existencia | "There **is** no default value." | No hay valor por defecto. |

| Verbo base | Con -s / -es / -ies | Regla |
|---|---|---|
| return | returns | Normal: + s |
| pass | passes | Termina en s, sh, ch, x, z: + es |
| fetch | fetches | + es |
| match | matches | + es |
| apply | applies | Consonante + y → ies |
| copy | copies | Consonante + y → ies |
| destroy | destroys | Vocal + y → solo s |
| do / go | does / goes | Irregulares |
| have | has | Irregular: "it **has** a method" |

⚠️ Cuidado: "it return a list", "the function take two parameters" son los errores **más** comunes. En singular: **returns**, **takes**, **has**, **does**.

🇬🇧 Frases modelo: "This function **checks** whether the user **exists** and **returns** `True` if it **does**."

### 2️⃣ Presente continuo: lo que pasa ahora (logs y progreso)

**am/is/are + verbo-ing**. Lo verás en terminales, barras de progreso y en tus mensajes de estado ("I'm working on it"). Los logs suelen **omitir** el sujeto y el verbo auxiliar: "Downloading..." = "(I am) downloading".

| Estructura | Cuándo se usa | Ejemplo en logs/código | Traducción |
|---|---|---|---|
| Verbo-ing + ... | Paso en curso de una herramienta | "Downloading `torch-2.5.1`..." | Descargando torch... |
| Verbo-ing + ... | Instalación | "Installing collected packages: numpy" | Instalando los paquetes recogidos |
| Verbo-ing + ... | Compilación | "Compiling `main.rs`..." | Compilando main.rs |
| Verbo-ing + ... | Servidor | "Listening on port 3000" | Escuchando en el puerto 3000 |
| Verbo-ing + ... | Reintento | "Retrying in 5 seconds..." | Reintentando en 5 segundos |
| is + verbo-ing | Estado | "The server **is running**." | El servidor está corriendo. |
| is + being + participio | Pasiva en curso | "Your request **is being processed**." | Tu petición se está procesando. |
| am + verbo-ing | Tú, en un issue | "I'**m getting** this error..." | Me sale este error... |

| Log real | Traducción |
|---|---|
| Resolving dependencies... | Resolviendo dependencias... |
| Collecting requests | Recogiendo (buscando) requests |
| Building wheel for numpy (pyproject.toml) | Construyendo el paquete wheel de numpy |
| Waiting for connection... | Esperando conexión... |
| Starting development server at http://127.0.0.1:8000/ | Iniciando el servidor de desarrollo en... |
| Watching for file changes with StatReloader | Vigilando cambios en archivos con StatReloader |
| Cloning into 'repo'... | Clonando en 'repo'... |
| Receiving objects: 100% (120/120), done. | Recibiendo objetos: 100%, hecho. |
| Pulling fs layer | Descargando una capa del sistema de archivos (Docker) |
| Running migrations: | Ejecutando migraciones: |
| Epoch 3/10 - training... | Época 3 de 10, entrenando... |

💡 Consejo: en un issue, "I'**m getting** an error" (me está saliendo) suena más natural que "I get an error". "I **got** an error" = me salió una vez.

⚠️ Cuidado: no uses presente continuo para hechos permanentes en una doc: ❌ "This function is returning a list" → ✅ "This function **returns** a list".

### 3️⃣ Pasado simple: changelogs, logs terminados y bugs

**verbo-ed** (regular) o forma irregular. Para contar lo que **ya pasó**: un build que falló, un fix de una versión, lo que hiciste ayer.

| Estructura | Cuándo se usa | Ejemplo en docs/código | Traducción |
|---|---|---|---|
| Verbo-ed | Changelog | "**Fixed** a crash when the list is empty." | Se corrigió un fallo cuando la lista está vacía. |
| Verbo-ed | Changelog | "**Added** support for Python 3.13." | Se añadió soporte para Python 3.13. |
| Verbo-ed | Changelog | "**Removed** the deprecated `--old` flag." | Se eliminó la opción obsoleta --old. |
| Sujeto + verbo-ed | Resultado de comando | "Build **failed**." / "Tests **passed**." | El build falló. / Los tests pasaron. |
| Sujeto + verbo-ed | Resultado | "Process **exited** with code 1." | El proceso terminó con código 1. |
| **did not** + verbo | Negación | "The server **did not respond**." | El servidor no respondió. |
| **Did** + sujeto + verbo? | Pregunta en review | "**Did** you **run** the tests?" | ¿Corriste los tests? |
| **was / were** | Estados pasados | "The file **was** empty." | El archivo estaba vacío. |

| Verbo irregular | Pasado | Participio | Ejemplo técnico |
|---|---|---|---|
| build | built | built | "Successfully **built** the image." |
| write | wrote | written | "**Wrote** 3 files to `dist/`." |
| run | ran | run | "**Ran** 42 tests in 1.3s" (pytest/unittest) |
| find | found | found | "**Found** 2 vulnerabilities." |
| take | took | taken | "The request **took** 3 seconds." |
| throw | threw | thrown | "The function **threw** an exception." |
| break | broke | broken | "This update **broke** my build." |
| get | got | got / gotten | "I **got** a 404." |
| send | sent | sent | "**Sent** 3 requests." |
| begin | began | begun | "Download **began**." |
| choose | chose | chosen | "You **chose** the wrong branch." |
| hide | hid | hidden | "**hidden** files" |
| set / reset | set / reset | set / reset | "The variable was **set** to null." |
| read | read (suena "red") | read | "**Read** 100 lines." |
| bind | bound | bound | "Server **bound** to port 80." |
| seek | sought | sought | "the **sought** value" (raro en código) |

🇬🇧 Pronuncia el **-ed**: tras t/d suena "id" (**added** = ádid, **updated** = ápdeitid); si no, "t" o "d" (**fixed** = fikst, **removed** = rimúvd).

### 4️⃣ Presente perfecto: deprecaciones y cambios que siguen vigentes

**has/have + participio**. Une el pasado con el presente: algo pasó y **todavía** importa. Es el tiempo favorito de los avisos de deprecación y de los mensajes de estado.

| Estructura | Cuándo se usa | Ejemplo en docs/código | Traducción |
|---|---|---|---|
| has been + participio | Deprecación | "This function **has been deprecated**." | Esta función ha sido marcada como obsoleta. |
| has been + participio | Eliminación | "`np.float` **has been removed**." | np.float ha sido eliminado. |
| has been + participio | Renombrado | "`find_element_by_id` **has been replaced** by `find_element`." | Ha sido reemplazado por... |
| have + participio | Experiencia | "**Have** you **tried** restarting it?" | ¿Has probado a reiniciarlo? |
| has + participio | Estado actual | "The connection **has timed out**." | La conexión ha agotado el tiempo. |
| has already + participio | Repetición | "The module **has already been** imported." | El módulo ya ha sido importado. |
| has not + participio + yet | Pendiente | "The migration **has not been applied yet**." | La migración aún no se ha aplicado. |
| have been + verbo-ing | Duración | "I'**ve been trying** to fix this for hours." | Llevo horas intentando arreglarlo. |
| since / for | Desde cuándo | "deprecated **since** 3.10" / "**for** two days" | desde la 3.10 / desde hace dos días |

⚠️ Cuidado: "I have 3 hours with this bug" ❌ → ✅ "I've **been stuck on** this bug **for** 3 hours". El español "llevo X tiempo" = **have been + -ing + for**.

💡 Consejo: **since** + momento (since 2024, since version 2.0) y **for** + duración (for 3 days, for a week).

### 5️⃣ Futuro: will, going to y presente con valor de futuro

**will** = futuro neutro (docs, avisos, promesas). **going to** = plan o intención ("I'm going to open a PR"). En docs casi siempre verás **will**.

| Estructura | Cuándo se usa | Ejemplo en docs/código | Traducción |
|---|---|---|---|
| will + verbo | Consecuencia segura | "This **will delete** all your data." | Esto borrará todos tus datos. |
| will be + participio | Futuro pasivo | "It **will be removed** in version 3.0." | Se eliminará en la versión 3.0. |
| will not (won't) + verbo | Negación | "Changes **won't** take effect until restart." | Los cambios no surtirán efecto hasta reiniciar. |
| am/is/are going to + verbo | Plan, intención | "I'**m going to** refactor the parser." | Voy a refactorizar el parser. |
| is about to + verbo | Inminente | "You **are about to** delete this repository." | Estás a punto de borrar este repositorio. |
| Presente continuo + fecha | Plan fijo | "We'**re releasing** v2 next week." | Lanzamos la v2 la semana que viene. |
| will have + participio | Futuro perfecto | "By then, the job **will have finished**." | Para entonces, el job habrá terminado. |
| In a future version, ... + will | Avisos | "In a future version, this **will raise** an error." | En una versión futura, esto lanzará un error. |

🇬🇧 Aviso real de pandas: "In a future version, this will raise an error" = hoy es un **warning**, mañana será un **error**. Arréglalo ya.

### 6️⃣ Imperativo: tutoriales, commits y mensajes de ayuda

**Verbo en forma base, sin sujeto**. Es una orden, un paso o una sugerencia. Lo usan los tutoriales, los commits, los botones y las pistas de los errores ("hint:").

| Estructura | Cuándo se usa | Ejemplo en docs/código | Traducción |
|---|---|---|---|
| Verbo + objeto | Paso de tutorial | "**Install** the package with pip." | Instala el paquete con pip. |
| Verbo + objeto | Pista de error | "**Use** `--force` to override." | Usa --force para forzar. |
| Don't + verbo | Prohibición | "**Don't commit** your `.env` file." | No subas tu archivo .env. |
| Make sure + frase | Comprobación | "**Make sure** Docker is running." | Asegúrate de que Docker está corriendo. |
| Let's + verbo | Tutorial amable | "**Let's create** a new component." | Creemos un componente nuevo. |
| Please + verbo | Petición | "**Please** commit your changes or stash them." | Por favor, haz commit o stash de tus cambios. |
| Try + verbo-ing | Sugerencia | "**Try running** `npm install` again." | Prueba a ejecutar npm install otra vez. |
| Consider + verbo-ing | Recomendación | "**Consider using** a virtual environment." | Considera usar un entorno virtual. |
| Verbo (botón/menú) | Interfaz | "**Save**", "**Cancel**", "**Retry**" | Guardar, Cancelar, Reintentar |

💡 Consejo: después de **try**, **consider**, **avoid**, **keep**, **stop** va **-ing**: "try restarting", "avoid using", "keep running". Ver la sección de gerundio vs infinitivo.

📌 Resumen: docs = **presente** ("returns"); logs = **-ing** ("Downloading"); changelog = **pasado** ("Fixed"); deprecación = **has been**; aviso = **will**; tutorial y commit = **imperativo** ("Add").

## 🔄 Voz pasiva: el "se" de la documentación

En las docs lo importante es **qué pasa**, no **quién** lo hace. Por eso usan muchísimo la pasiva: **be + participio**. Truco: cuando en español dirías "**se** devuelve", "**se** llama", "**se** ignora", en inglés casi siempre es pasiva.

### 🧱 La pasiva en todos los tiempos

| Tiempo | Estructura | Ejemplo en docs | Traducción |
|---|---|---|---|
| Presente | is/are + participio | "The callback **is called** on every change." | El callback se llama en cada cambio. |
| Pasado | was/were + participio | "This method **was added** in 3.8." | Este método se añadió en la 3.8. |
| Presente perfecto | has/have been + participio | "It **has been deprecated**." | Ha sido marcado como obsoleto. |
| Futuro | will be + participio | "It **will be removed** in 4.0." | Se eliminará en la 4.0. |
| Continuo | is being + participio | "The file **is being used** by another process." | Otro proceso está usando el archivo. |
| Con modal | must/can/should be + participio | "The token **must be passed** in the header." | El token debe pasarse en la cabecera. |
| Infinitivo | to be + participio | "Values **to be inserted**." | Valores que se van a insertar. |
| Participio solo (reducida) | participio | "Files **changed**: 3" | Archivos cambiados: 3 |

### 🔁 Activa vs pasiva

| Activa (quién lo hace) | Pasiva (qué pasa) | Traducción natural |
|---|---|---|
| The interpreter ignores this value. | This value **is ignored**. | Este valor se ignora. |
| The library creates the file automatically. | The file **is created** automatically. | El archivo se crea automáticamente. |
| The system logs errors to stderr. | Errors **are logged** to stderr. | Los errores se registran en stderr. |
| The core team deprecated the API. | The API **was deprecated**. | La API se marcó como obsoleta. |
| React calls the effect after render. | The effect **is called** after render. | El efecto se ejecuta tras el render. |
| You must specify the name. | The name **must be specified**. | Hay que especificar el nombre. |
| The server rejected your request. | Your request **was rejected**. | Tu petición fue rechazada. |
| Somebody already took this name. | This name **is already taken**. | Este nombre ya está en uso. |

### 🧩 Pasivas reducidas que verás en errores

Los mensajes de error recortan la pasiva: quitan el sujeto y el verbo **be**, dejando solo el participio. Reconócelas:

| Mensaje recortado | Frase completa | Traducción |
|---|---|---|
| File not found | The file was not found | No se encontró el archivo |
| Permission denied | Permission is denied | Permiso denegado |
| Connection refused | The connection was refused | Conexión rechazada |
| Module not installed | The module is not installed | El módulo no está instalado |
| Access denied for user 'root' | Access is denied for user 'root' | Acceso denegado para el usuario root |
| Request blocked by CORS policy | The request was blocked by the CORS policy | Petición bloqueada por la política CORS |
| Command not found | The command was not found | Comando no encontrado |
| Port already allocated | The port is already allocated | Puerto ya asignado |
| Not supported | It is not supported | No soportado |
| Expected 2 arguments | 2 arguments were expected | Se esperaban 2 argumentos |

⚠️ Cuidado: no confundas "**is used to**" (se usa para) con "**is used to** + -ing" (está acostumbrado a). En docs casi siempre es lo primero: "This flag **is used to** enable debug mode."

🇬🇧 Frase modelo: "If no value **is provided**, the default **is used**." = Si no se proporciona valor, se usa el de por defecto.

## ⚖️ Modales: cuánto te obliga cada palabra

Los modales dicen **qué tan obligatorio** es algo. En una doc, la diferencia entre **must** y **may** es la diferencia entre "si no lo haces, falla" y "si quieres". Después de un modal el verbo va **sin to y sin -s**: "it **must be**", nunca "it must to be" ni "it musts".

### 📊 Escala de obligación

| Modal | Nivel | Ejemplo en docs | Traducción | Si lo ignoras |
|---|---|---|---|---|
| must | 🔴 Obligatorio | "The name **must be** unique." | El nombre debe ser único. | Falla o rompe |
| must not | ⛔ Prohibido | "You **must not** call this twice." | No debes llamarlo dos veces. | Comportamiento indefinido |
| have to / has to | 🔴 Obligatorio (externo) | "You **have to** restart the server." | Tienes que reiniciar el servidor. | No funciona |
| need to | 🟠 Necesario | "You **need to** install Node first." | Necesitas instalar Node primero. | No funciona |
| should | 🟡 Recomendado | "You **should** use HTTPS." | Deberías usar HTTPS. | Funciona pero es mala idea |
| should not | 🟡 Desaconsejado | "You **should not** store passwords in plain text." | No deberías guardar contraseñas en texto plano. | Riesgo |
| can | 🟢 Posible, permitido | "You **can** pass a list or a tuple." | Puedes pasar una lista o una tupla. | Nada |
| may | 🟢 Permitido o posible | "This **may** take a while." | Esto puede tardar. | Nada |
| might | ⚪ Posibilidad baja | "It **might** not work on Windows." | Puede que no funcione en Windows. | Quizás nada |
| could | ⚪ Posibilidad, sugerencia | "You **could** also use a set." | También podrías usar un set. | Nada |
| don't have to / don't need to | ⚪ No hace falta | "You **don't need to** close the file." | No hace falta cerrar el archivo. | Nada |
| will | 🔵 Certeza futura | "This **will** overwrite the file." | Esto sobrescribirá el archivo. | Pasa seguro |
| would | 🔵 Hipotético, cortés | "**Would** you review my PR?" | ¿Podrías revisar mi PR? | — |

### ⚠️ Las tres confusiones clásicas

| Confusión | Significado A | Significado B | Ejemplo |
|---|---|---|---|
| must not vs don't have to | **must not** = prohibido | **don't have to** = opcional | "You must not delete it" ≠ "You don't have to delete it" |
| may (permiso) vs may (posibilidad) | "You **may** use it" = te está permitido | "It **may** fail" = puede que falle | Decide por el contexto |
| can vs may en docs | **can** = es capaz, se puede | **may** = puede ocurrir, o está permitido | "The value can be null" (se permite) / "may be null" (puede venir null) |

### 🧪 Modales en pasado y deducción (para debugging)

| Estructura | Significa | Ejemplo | Traducción |
|---|---|---|---|
| must have + participio | Deducción segura del pasado | "The cache **must have expired**." | La caché debe de haber caducado. |
| might / may have + participio | Posibilidad pasada | "The deploy **might have failed**." | Puede que el deploy haya fallado. |
| should have + participio | Lo correcto que no se hizo | "I **should have tested** it." | Debería haberlo probado. |
| could have + participio | Posibilidad no realizada | "It **could have been** a race condition." | Podría haber sido una condición de carrera. |
| can't have + participio | Imposible | "It **can't have been** the network." | No puede haber sido la red. |
| was supposed to + verbo | Expectativa no cumplida | "It **was supposed to** return a list." | Se suponía que devolvía una lista. |

⚠️ Cuidado: ❌ "You must to install" / ❌ "It cans be null" / ❌ "It should works". ✅ "You **must install**", "It **can be** null", "It **should work**".

🇬🇧 Frase modelo de issue: "It **should** return `200`, but it returns `500`. I think the token **might have expired**."

📌 Resumen: **must** = sí o sí · **should** = muy recomendable · **may/can** = opcional o posible · **might** = quizás · **don't need to** = no hace falta.

## 🔀 Condicionales, gerundio e infinitivo

Las docs están llenas de "**if** this, **then** that". Hay cuatro tipos de condicional, pero en documentación usarás sobre todo el **0** (siempre pasa) y el **1** (pasará). Además, muchos errores de escritura vienen de poner **to** donde va **-ing** o al revés.

### 🔁 Los condicionales

| Tipo | Estructura | Cuándo se usa | Ejemplo en docs/código | Traducción |
|---|---|---|---|---|
| 0 (verdad general) | If + presente, presente | Comportamiento fijo | "If the list **is** empty, it **returns** `None`." | Si la lista está vacía, devuelve None. |
| 1 (futuro real) | If + presente, will + verbo | Consecuencia probable | "If you **delete** this, you **will lose** your data." | Si borras esto, perderás tus datos. |
| 1 con imperativo | If + presente, imperativo | Instrucción | "If it **fails**, **run** it again." | Si falla, ejecútalo otra vez. |
| 1 con modal | If + presente, may/can/should | Recomendación | "If you **use** Windows, you **should** use WSL." | Si usas Windows, deberías usar WSL. |
| 2 (hipotético) | If + pasado, would + verbo | Situación imaginaria | "If we **used** a cache, it **would be** faster." | Si usáramos caché, sería más rápido. |
| 3 (pasado imposible) | If + had + participio, would have + participio | Lamentar | "If I **had tested** it, I **would have caught** the bug." | Si lo hubiera probado, habría detectado el bug. |

### 🧷 Otras formas de poner condiciones

| Palabra | Significa | Ejemplo en docs | Traducción |
|---|---|---|---|
| unless | a menos que, salvo que | "**Unless** specified, UTF-8 is used." | Salvo que se indique, se usa UTF-8. |
| provided (that) | siempre que | "**Provided that** the key exists, ..." | Siempre que la clave exista, ... |
| as long as | mientras, siempre que | "It works **as long as** the port is free." | Funciona mientras el puerto esté libre. |
| in case | por si acaso | "Keep a backup **in case** something fails." | Guarda una copia por si algo falla. |
| in case of | en caso de | "**In case of** error, returns -1." | En caso de error, devuelve -1. |
| whether | si (sí o no) | "**whether** to include headers" | si incluir o no las cabeceras |
| whether or not | tanto si... como si no | "It runs **whether or not** the test passes." | Se ejecuta pase o no el test. |
| if not / if omitted | si no / si se omite | "**If omitted**, defaults to 10." | Si se omite, vale 10 por defecto. |
| if any | si lo hay | "Returns the error, **if any**." | Devuelve el error, si lo hay. |
| if so / if not | en ese caso / si no | "Is it cached? **If so**, return it." | ¿Está en caché? En ese caso, devuélvelo. |
| only if | solo si | "Runs **only if** `debug=True`." | Se ejecuta solo si debug=True. |
| even if | aunque (incluso si) | "It retries **even if** the server is down." | Reintenta aunque el servidor esté caído. |
| otherwise | si no, de lo contrario | "Returns the value; **otherwise**, `None`." | Devuelve el valor; si no, None. |

⚠️ Cuidado: no pongas **will** después de **if** en el condicional 1: ❌ "If it will fail, ..." → ✅ "If it **fails**, ...". Lo mismo con **when**: ✅ "**When** the user **clicks**, ..."

💡 Consejo: **if** vs **whether**: en "I don't know **whether** it's a bug" se puede usar "if", pero después de preposición o antes de *to* solo vale **whether**: "decide **whether to** retry".

### 🧬 Gerundio (-ing) vs infinitivo (to + verbo)

Algunos verbos exigen **-ing** detrás, otros **to + verbo**. En español siempre usamos infinitivo ("evitar usar", "intentar reiniciar"), por eso nos equivocamos.

| Va con -ing | Ejemplo | Va con to + verbo | Ejemplo |
|---|---|---|---|
| avoid | "Avoid **using** global variables." | want | "I want **to learn** Rust." |
| consider | "Consider **adding** a test." | need | "You need **to install** it." |
| keep | "It keeps **crashing**." | decide | "We decided **to migrate**." |
| finish | "It finished **downloading**." | plan | "We plan **to support** ARM." |
| suggest | "I suggest **renaming** it." | expect | "I expected it **to return** a list." |
| recommend | "We recommend **using** HTTPS." | fail | "It failed **to connect**." |
| enjoy | "I enjoy **coding**." | manage | "I managed **to fix** it." |
| mind | "Would you mind **reviewing** it?" | refuse | "Git refuses **to merge**." |
| stop (dejar de) | "It stopped **working**." | attempt | "Attempted **to import** X." |
| start / begin (ambos) | "It started **failing**." | allow + objeto | "It allows you **to export**." |
| be worth | "It's worth **trying**." | tend | "It tends **to be** slow." |
| after / before / without | "**Before running**, install deps." | seem | "It seems **to work**." |
| look forward to | "I look forward **to hearing** from you." | be able | "I wasn't able **to reproduce** it." |

| Verbo con doble uso | Con -ing | Con to | Diferencia |
|---|---|---|---|
| try | "Try **restarting** it." (prueba a ver) | "I tried **to restart** it." (intenté, con esfuerzo) | experimento vs esfuerzo |
| stop | "Stop **using** it." (deja de) | "He stopped **to check**." (se paró para) | dejar vs parar para |
| remember | "I remember **setting** it." (recuerdo haberlo hecho) | "Remember **to set** it." (no olvides hacerlo) | pasado vs futuro |
| forget | "I forgot **adding** it" (raro) | "I forgot **to add** the import." (olvidé hacerlo) | usa casi siempre to |

| Preposición + -ing | Ejemplo | Traducción |
|---|---|---|
| for + -ing | "a tool **for parsing** JSON" | una herramienta para parsear JSON |
| by + -ing | "Fix it **by adding** a key." | Arréglalo añadiendo una clave. |
| without + -ing | "**without breaking** compatibility" | sin romper la compatibilidad |
| instead of + -ing | "**instead of using** `var`" | en vez de usar var |
| before / after + -ing | "**after installing** Python" | después de instalar Python |
| when + -ing | "**when using** async code" | al usar código asíncrono |
| responsible for + -ing | "**responsible for handling** errors" | encargado de manejar errores |

⚠️ Cuidado: después de **preposición** el verbo SIEMPRE va en **-ing**: ❌ "a function for parse JSON", ❌ "before to run" → ✅ "for **parsing**", "before **running**".

⚠️ Cuidado: "**used to**" para propósito en docs lleva infinitivo: "a tool used **to parse** JSON". Pero "**for**" lleva -ing: "a tool **for parsing** JSON". Ambas correctas.

🇬🇧 Frase modelo: "I **tried reinstalling** the package, but it **keeps failing to compile**. I'd **suggest adding** a note to the docs."

## 📰 Artículos, plurales y contables

Los artículos son **el gran error del hispanohablante**: los ponemos donde no van ("the people is") y los quitamos donde sí van ("it returns list"). Además, el inglés técnico tiene plurales latinos y griegos (index → indices) y palabras incontables (information, software) que nunca llevan -s.

### 🅰️ a / an / the / nada

| Artículo | Cuándo | Ejemplo en docs | Traducción |
|---|---|---|---|
| a | Uno cualquiera, singular, suena consonante | "Returns **a** list." | Devuelve una lista. |
| an | Uno cualquiera, suena vocal | "Raises **an** error." / "**an** HTTP request" | Lanza un error. / una petición HTTP |
| the | Uno concreto, ya conocido o único | "**The** list is sorted in place." | La lista se ordena en el sitio. |
| (nada) | Plural en general | "Lists are mutable." | Las listas son mutables. |
| (nada) | Incontable en general | "Data is stored in JSON." | Los datos se guardan en JSON. |
| (nada) | Nombres propios, lenguajes | "Python supports..." / "Linux is..." | Python soporta... |
| the + plural | Plural concreto | "**The** files in `src/`" | Los archivos de src/ |

| a o an se decide por el SONIDO | Correcto | Por qué |
|---|---|---|
| hour, honest | **an** hour, **an** honest mistake | La h no suena |
| HTTP, HTML, SQL (és-kiu-el) | **an** HTTP request, **an** HTML file, **an** SQL query | Se deletrean: "eich", "es" empiezan en vocal |
| URL, user, unique | **a** URL, **a** user, **a** unique id | Suenan "iu" (consonante y) |
| API, ID, IDE | **an** API, **an** ID, **an** IDE | "ei", "ai" |
| one-time | **a** one-time token | Suena "uan" |
| array, object, integer | **an** array, **an** object, **an** integer | Vocal |
| UI, USB | **a** UI, **a** USB drive | "iu" |

```flujo
dir: abajo
Sustantivo -> ¿Contable singular? : primera pregunta
¿Contable singular? -> a / an / the : sí, siempre artículo
¿Contable singular? -> Sin artículo : plural o incontable en general
```

### 🚫 Cuándo NO poner "the" (aunque en español sí)

| ❌ Calco del español | ✅ Inglés correcto | Por qué |
|---|---|---|
| The Python is easy. | Python is easy. | Nombre propio |
| The programming is fun. | Programming is fun. | Concepto general |
| The people is waiting. | People **are** waiting. | General + people es plural |
| I study the Computer Science. | I study Computer Science. | Asignaturas y carreras |
| The machine learning needs data. | Machine learning needs data. | Disciplina general |
| I use the Linux. | I use Linux. | Nombre propio |
| On the Monday | On Monday | Días de la semana |
| The users want dark mode. (en general) | Users want dark mode. | Plural en general |

### ✅ Cuándo SÍ poner artículo (aunque en español no)

| ❌ Sin artículo | ✅ Con artículo | Por qué |
|---|---|---|
| It returns list. | It returns **a** list. | Contable singular siempre lleva artículo |
| I'm developer. | I'm **a** developer. | Profesiones llevan a/an |
| I have question. | I have **a** question. | Contable singular |
| This is bug. | This is **a** bug. | Contable singular |
| Open terminal. | Open **a** terminal. / Open **the** terminal. | Contable singular |
| Function takes argument. | **The** function takes **an** argument. | Ambos contables singulares |
| What's best way? | What's **the** best way? | Superlativo lleva the |
| It's in same file. | It's in **the** same file. | same lleva the |

### 🔢 Plurales irregulares técnicos

| Singular | Plural | Uso real | Nota |
|---|---|---|---|
| index | indices / indexes | "array **indices**", "database **indexes**" | Matemáticas y arrays: indices; bases de datos: indexes |
| matrix | matrices | "multiply two **matrices**" | Se dice "MÉI-tri-siz" |
| vertex | vertices | "the graph has 5 **vertices**" | Geometría y grafos |
| vortex / apex | vortices / apices | raro en código | — |
| datum | data | "the **data is** clean" | En código, data se usa como incontable: "data is" |
| schema | schemas / schemata | "two database **schemas**" | Schemata es formal y raro |
| criterion | criteria | "search **criteria**" | ❌ "a criteria" → ✅ "a criterion" |
| phenomenon | phenomena | "a rare **phenomenon**" | — |
| analysis | analyses | "run two **analyses**" | -is → -es |
| hypothesis | hypotheses | "test the **hypotheses**" | -is → -es |
| axis | axes | "the x and y **axes**" | matplotlib: `ax`, `axes` |
| basis | bases | "a vector **basis**" | Álgebra lineal |
| parenthesis | parentheses | "missing **parentheses**" | Errores de sintaxis |
| thesis | theses | — | — |
| appendix | appendices / appendixes | "see the **appendices**" | — |
| medium | media | "social **media**" | En CSS: `@media` |
| stimulus | stimuli | — | Redes neuronales biológicas |
| radius | radii / radiuses | `border-radius` | — |
| focus | foci / focuses | "focuses" es lo normal | — |
| alumnus | alumni | "university **alumni**" | — |
| child | children | "the node's **children**" | Árboles y DOM |
| leaf | leaves | "the tree **leaves**" | Árboles |
| person | people | "**people** are" | ❌ "peoples" para personas |
| mouse | mice / mouses | "two **mice**" (dispositivo: ambas) | — |
| goose / foot / tooth | geese / feet / teeth | — | Cultura general |
| status | statuses | "HTTP **statuses**" | ❌ "stati" |
| virus | viruses | "computer **viruses**" | ❌ "viri" |
| bus | buses / busses | "data **buses**" | — |
| process | processes | "kill all **processes**" | -s → -es |
| box / patch | boxes / patches | "apply two **patches**" | -x, -ch → -es |
| query / dependency | queries / dependencies | "install **dependencies**" | consonante + y → ies |
| key / array | keys / arrays | "dictionary **keys**" | vocal + y → solo s |

### 🫙 Incontables: nunca llevan -s ni "a"

| ❌ Mal | ✅ Bien | Si necesitas contar |
|---|---|---|
| informations | information | a piece of information |
| softwares | software | a software package, two programs |
| hardwares | hardware | a piece of hardware |
| feedbacks | feedback | a comment, some feedback |
| advices | advice | a piece of advice, a tip |
| researches | research | a study, a paper |
| equipments | equipment | a piece of equipment |
| knowledges | knowledge | some knowledge |
| homeworks | homework | an assignment |
| evidences | evidence | a piece of evidence |
| documentations | documentation | a doc, a page of the docs |
| codes (programa) | code | a code snippet, some code |
| furnitures / luggages | furniture / luggage | a piece of furniture |
| a progress | progress | some progress |
| a good news | good news (singular) | a piece of news |

| Contable o incontable | Cuántos (contable) | Cuánto (incontable) |
|---|---|---|
| Pregunta | **how many** files? | **how much** memory? |
| Pocos | **few / a few** errors | **little / a little** time |
| Menos | **fewer** bugs | **less** code |
| Mucho | **many** requests | **much** data |
| Algo de | **some** tests | **some** feedback |
| Número de | **the number of** users | **the amount of** RAM |

⚠️ Cuidado: "**code**" como programa es incontable: ❌ "I wrote a code" → ✅ "I wrote **some code**" / "a **piece of code**" / "a **snippet**". "A code" solo es un código concreto: "an error code", "a verification code".

💡 Consejo: **data** en inglés técnico moderno se trata como incontable singular: "the data **is** ready". En papers formales verás "the data **are**". Ambas se aceptan; elige una y sé consistente.

📌 Resumen: contable singular → **siempre** a/an/the · general en plural o incontable → **sin** artículo · **information, software, feedback, code, advice** → nunca -s.

## 📍 Preposiciones, comparativos y superlativos

Las preposiciones no se traducen 1 a 1 desde el español: "en" puede ser "in", "on" o "at"; "por" puede ser "by", "per", "for" o "via". En docs aparecen siempre en las mismas combinaciones, así que apréndelas **en bloque**.

### 📌 in / on / at en contexto técnico

| Preposición | Uso técnico | Ejemplo | Traducción |
|---|---|---|---|
| in | Dentro de archivo, carpeta, lenguaje | "the bug **in** `main.py`" | el bug en main.py |
| in | Dentro de lenguaje o herramienta | "written **in** Python" | escrito en Python |
| in | Meses, años, versiones | "**in** v3.0", "**in** 2024" | en la v3.0, en 2024 |
| in | Modo o formato | "**in** JSON format", "**in** dark mode" | en formato JSON |
| on | Plataforma, sistema, superficie | "runs **on** Linux", "**on** GitHub" | corre en Linux, en GitHub |
| on | Línea de código | "**on** line 42" | en la línea 42 |
| on | Eventos y disparadores | "**on** click", "**on** error", "**on** save" | al hacer clic |
| on | Rama | "**on** the `main` branch" | en la rama main |
| on | Página web, pantalla | "**on** the login page" | en la página de login |
| at | Punto exacto, dirección, hora | "**at** `localhost:3000`", "**at** 3 pm" | en localhost:3000 |
| at | Posición en una estructura | "the item **at** index 0" | el elemento en el índice 0 |
| at | Tiempo de ejecución | "**at** runtime", "**at** compile time" | en tiempo de ejecución |

### 🧭 Preposiciones técnicas que dan problemas

| Preposición | Significa | Ejemplo real | Traducción |
|---|---|---|---|
| by | por (agente), mediante | "sorted **by** date", "created **by** the server" | ordenado por fecha |
| by | por (operación) | "divide **by** zero", "increment **by** 1" | dividir entre cero |
| via | a través de, mediante | "install **via** pip", "**via** SSH" | instalar mediante pip |
| per | por cada | "100 requests **per** minute" | 100 peticiones por minuto |
| per | según | "**per** the docs", "**as per** RFC 7231" | según la doc |
| against | contra (comparar, ejecutar sobre) | "run tests **against** Python 3.12", "validate **against** a schema" | ejecutar los tests con Python 3.12 |
| across | a lo largo de, en todos | "consistent **across** platforms", "**across** files" | coherente en todas las plataformas |
| over | sobre, recorrer | "iterate **over** a list", "**over** HTTPS" | recorrer una lista |
| through | a través de | "loop **through** items", "go **through** the docs" | recorrer los elementos |
| within | dentro de (límite) | "**within** 5 seconds", "**within** the function" | en menos de 5 segundos |
| from ... to ... | de ... a ... | "convert **from** CSV **to** JSON" | convertir de CSV a JSON |
| into | dentro de (movimiento) | "insert **into** a table", "split **into** chunks" | insertar en una tabla |
| onto | encima de (movimiento) | "rebase **onto** `main`", "push **onto** the stack" | rebasar sobre main |
| out of | fuera de | "**out of** memory", "**out of** range" | sin memoria, fuera de rango |
| under | bajo, en (ruta) | "**under** `/usr/lib`", "**under** the MIT license" | bajo licencia MIT |
| behind / ahead of | detrás / delante | "2 commits **behind**", "**ahead of** origin" | 2 commits por detrás |
| up to | hasta | "**up to** 10 files" | hasta 10 archivos |
| except / except for | excepto | "all files **except** `.env`" | todos menos .env |
| instead of | en lugar de | "use `let` **instead of** `var`" | usa let en lugar de var |
| on top of | encima de, además de | "built **on top of** React" | construido sobre React |

### 🔗 Verbo + preposición fija (memorízalas juntas)

| ✅ Correcto | ❌ Error típico | Traducción |
|---|---|---|
| depend **on** | depend of | depender de |
| consist **of** | consist in | consistir en |
| be based **on** | based in | basado en |
| be compatible **with** | compatible to | compatible con |
| be responsible **for** | responsible of | responsable de |
| be different **from** | different of | diferente de |
| be similar **to** | similar of / with | similar a |
| look **for** | search for (también vale) | buscar |
| wait **for** | wait (sin for) | esperar a |
| listen **to** / listen **on** port | listen | escuchar / escuchar en un puerto |
| point **to** | point at (otro matiz) | apuntar a |
| convert **to** / **into** | convert in | convertir a |
| interested **in** | interested on | interesado en |
| good **at** | good in | bueno en |
| familiar **with** | familiar to | familiarizado con |
| apply **to** | apply on | aplicar a / postular a |
| subscribe **to** | subscribe on | suscribirse a |
| fall back **to** | fallback (verbo) | recurrir a (alternativa) |
| opt **in** / opt **out** | — | activar / desactivar voluntariamente |
| log **in** / log **out** (verbo) | login (verbo) | iniciar / cerrar sesión ("the login page") |
| set **up** (verbo) / setup (sustantivo) | setup the project | configurar / la configuración |

⚠️ Cuidado: **login, setup, backup, checkout, shutdown** son sustantivos o adjetivos; el verbo se escribe separado: "**log in** to your account", "**set up** the project", "**back up** your files", "**shut down** the server".

### 📈 Comparativos y superlativos

| Tipo de adjetivo | Comparativo | Superlativo | Ejemplo técnico |
|---|---|---|---|
| Corto (1 sílaba) | fast → fast**er** | the fast**est** | "Rust is **faster than** Python." |
| Corto | small → small**er** | the small**est** | "the **smallest** element" |
| Corto | new → new**er** | the new**est** | "Use a **newer** version." |
| Termina en -y | easy → eas**ier** | the eas**iest** | "the **easiest** way" |
| Consonante-vocal-consonante | big → big**ger** | the big**gest** | "a **bigger** batch size" |
| Largo (2+ sílabas) | efficient → **more** efficient | the **most** efficient | "**more efficient than** a loop" |
| Largo | readable → **more** readable | the **most** readable | "**more readable** code" |
| Irregular | good → **better** | the **best** | "**best** practices" |
| Irregular | bad → **worse** | the **worst** | "**worst-case** complexity" |
| Irregular | far → **further** | the **furthest** | "for **further** details" |
| Irregular | little → **less** | the **least** | "**least** recently used (LRU)" |
| Irregular | many/much → **more** | the **most** | "**most** recent call last" |
| Igualdad | as + adj + as | — | "**as fast as** C" |
| Inferioridad | less + adj + than | — | "**less** memory **than** before" |
| Progresivo | the + comp, the + comp | — | "**The more** data, **the better**." |

| Frase de doc | Traducción |
|---|---|
| most recent call last | la llamada más reciente al final |
| at least one argument | al menos un argumento |
| at most 255 characters | como máximo 255 caracteres |
| no more than 10 MB | no más de 10 MB |
| greater than or equal to 0 | mayor o igual que 0 |
| less than zero | menor que cero |
| later / earlier versions | versiones posteriores / anteriores |
| Python 3.10 or later / or higher / or newer | Python 3.10 o superior |
| the latest version | la versión más reciente |
| the last element | el último elemento |
| worst case / best case | peor caso / mejor caso |

⚠️ Cuidado: ❌ "more faster", ❌ "more better", ❌ "the most fastest". Elige uno: **faster** o **more efficient**, nunca los dos. Y la comparación usa **than**, no "that": "faster **than** Python".

⚠️ Cuidado: **latest** = la más nueva (latest version); **last** = la última de una serie (last element, last week). "The **latest** release" ≠ "the **last** release" (esta suena a que no habrá más).

🇬🇧 Frase modelo: "Using a set is **much faster than** using a list **for** membership tests, **especially** with large inputs."

## 🔗 Conectores para leer y escribir explicaciones

Los conectores son las "bisagras" de un texto: te dicen si lo que viene es un **contraste** (however), una **consecuencia** (therefore), una **condición** (unless) o una **alternativa** (instead). Si entiendes el conector, entiendes la lógica del párrafo aunque no sepas todas las palabras.

### ↔️ Contraste y alternativa

| Conector | Significa | Ejemplo en docs | Traducción |
|---|---|---|---|
| however | sin embargo | "It's fast. **However**, it uses more memory." | Es rápido. Sin embargo, usa más memoria. |
| but | pero | "It works, **but** it's slow." | Funciona, pero es lento. |
| although / though | aunque | "**Although** it's optional, we recommend it." | Aunque es opcional, lo recomendamos. |
| even though | aunque (sabiendo que) | "It fails **even though** the file exists." | Falla aunque el archivo existe. |
| whereas | mientras que | "`list` is mutable, **whereas** `tuple` is not." | list es mutable, mientras que tuple no. |
| while | mientras que (contraste o tiempo) | "**While** `==` compares values, `is` compares identity." | Mientras == compara valores, is compara identidad. |
| instead | en su lugar | "Don't use `var`. Use `let` **instead**." | No uses var. Usa let en su lugar. |
| instead of | en vez de | "**instead of** a for loop" | en vez de un bucle for |
| rather than | en lugar de | "returns an iterator **rather than** a list" | devuelve un iterador en lugar de una lista |
| on the other hand | por otro lado | "**On the other hand**, SQLite needs no server." | Por otro lado, SQLite no necesita servidor. |
| despite / in spite of | a pesar de | "**Despite** the warning, it compiles." | A pesar del aviso, compila. |
| nevertheless | no obstante | "**Nevertheless**, use it with care." | No obstante, úsalo con cuidado. |
| unlike | a diferencia de | "**Unlike** Python, JS has `undefined`." | A diferencia de Python, JS tiene undefined. |
| otherwise | si no, de lo contrario | "Set a timeout; **otherwise**, it may hang." | Pon un timeout; si no, puede colgarse. |

### ➡️ Causa, consecuencia y finalidad

| Conector | Significa | Ejemplo en docs | Traducción |
|---|---|---|---|
| therefore | por lo tanto | "It's immutable; **therefore**, it's hashable." | Es inmutable; por lo tanto, es hasheable. |
| thus | así, por ende | "**Thus**, the result is cached." | Así, el resultado se guarda en caché. |
| hence | de ahí, por eso | "It's lazy, **hence** the name." | Es perezoso, de ahí el nombre. |
| so | así que | "It's slow, **so** we cache it." | Es lento, así que lo cacheamos. |
| because | porque (+ frase) | "It fails **because** the key is missing." | Falla porque falta la clave. |
| because of / due to | debido a (+ sustantivo) | "**due to** a race condition" | debido a una condición de carrera |
| since | ya que | "**Since** v2.0 is stable, upgrade now." | Ya que la v2.0 es estable, actualiza. |
| as a result | como resultado | "**As a result**, the tests pass." | Como resultado, los tests pasan. |
| in order to | para (finalidad) | "**In order to** use it, import it first." | Para usarlo, impórtalo primero. |
| so that | para que | "Add a key **so that** React can track items." | Añade una key para que React pueda seguir los elementos. |
| that's why | por eso | "**That's why** it returns `None`." | Por eso devuelve None. |
| which means | lo que significa | "It's async, **which means** you must await it." | Es async, lo que significa que debes esperarlo. |

### ➕ Añadir, ordenar y ejemplificar

| Conector | Significa | Ejemplo en docs | Traducción |
|---|---|---|---|
| also | también | "It **also** supports YAML." | También soporta YAML. |
| in addition / additionally | además | "**Additionally**, you can pass a callback." | Además, puedes pasar un callback. |
| moreover / furthermore | es más, además | "**Furthermore**, it's thread-safe." | Además, es seguro con hilos. |
| as well as | así como | "Linux **as well as** macOS" | Linux así como macOS |
| such as | como (ejemplos) | "formats **such as** JSON or CSV" | formatos como JSON o CSV |
| for example / e.g. | por ejemplo | "a sequence, **e.g.** a list" | una secuencia, p. ej. una lista |
| that is / i.e. | es decir | "falsy values, **i.e.** `0`, `''`, `None`" | valores falsy, es decir... |
| namely | a saber, concretamente | "two options, **namely** A and B" | dos opciones, concretamente A y B |
| first / then / finally | primero / luego / por último | "**First**, install it. **Then**, run it." | Primero instálalo. Luego, ejecútalo. |
| once | una vez que | "**Once** installed, restart the shell." | Una vez instalado, reinicia la shell. |
| respectively | respectivamente | "`x` and `y` are 1 and 2, **respectively**." | x e y valen 1 y 2, respectivamente. |
| in other words | en otras palabras | "**In other words**, it's a pure function." | En otras palabras, es una función pura. |
| note that | ten en cuenta que | "**Note that** this is case-sensitive." | Ten en cuenta que distingue mayúsculas. |
| in particular / especially | en particular / sobre todo | "**especially** on large inputs" | sobre todo con entradas grandes |

### ⏱️ Condición, tiempo y referencia

| Conector | Significa | Ejemplo en docs | Traducción |
|---|---|---|---|
| unless | a menos que | "**Unless** `strict=True`, it ignores errors." | A menos que strict=True, ignora errores. |
| as long as | siempre que, mientras | "**as long as** the types match" | siempre que coincidan los tipos |
| as of | a partir de, desde | "**As of** version 3.0, this is the default." | A partir de la versión 3.0, esto es el comportamiento por defecto. |
| until | hasta que | "It blocks **until** the job finishes." | Se bloquea hasta que el job termina. |
| as soon as | en cuanto | "**as soon as** the data arrives" | en cuanto llegan los datos |
| whenever | cada vez que | "**whenever** the state changes" | cada vez que cambia el estado |
| meanwhile | mientras tanto | "**Meanwhile**, use the old API." | Mientras tanto, usa la API vieja. |
| regarding / as for | respecto a | "**Regarding** performance, ..." | Respecto al rendimiento, ... |
| in terms of | en cuanto a | "**in terms of** memory" | en cuanto a memoria |
| according to | según | "**according to** the docs" | según la documentación |
| by default | por defecto | "**By default**, it's disabled." | Por defecto, está desactivado. |
| at the moment | de momento | "Not supported **at the moment**." | No está soportado de momento. |
| so far | hasta ahora | "No issues **so far**." | Sin problemas hasta ahora. |
| eventually | al final, con el tiempo | "It will **eventually** time out." | Al final agotará el tiempo. |

⚠️ Cuidado: **however** al inicio de frase va seguido de **coma**: "However, ...". Entre dos frases completas usa punto y coma: "It's fast; **however**, it's unsafe." No lo uses como "pero" en medio sin puntuación.

⚠️ Cuidado: **as of** no es "como de". "As of today" = a partir de hoy, a fecha de hoy. "As of v18" = desde la v18.

💡 Consejo: **because** + frase completa ("because **the key is missing**"); **because of / due to** + sustantivo ("because of **a missing key**").

🇬🇧 Frase modelo: "This function is pure; **therefore**, it can be memoized. **However**, **unless** the input is hashable, the cache won't work."

## 🚫 Errores típicos de hispanohablantes

Todos los cometemos porque traducimos desde el español. Aprenderlos de memoria te ahorra correcciones en PRs, issues y entrevistas. Lee la columna **por qué**: entender el patrón evita el error en otras frases.

### 🧱 Gramática y estructura

| ❌ Mal | ✅ Bien | Por qué |
|---|---|---|
| Is working. | **It** is working. | El sujeto es obligatorio en inglés |
| Is a bug in the parser. | **There is** a bug in the parser. | "Hay" = there is / there are |
| Is possible to... | **It is** possible to... | Sujeto vacío "it" |
| The people is waiting. | The people **are** waiting. | people es plural |
| The function return a list. | The function **returns** a list. | -s en tercera persona |
| It don't work. | It **doesn't** work. | he/she/it → doesn't |
| I have 20 years. | I **am** 20 (years old). | La edad va con **be** |
| I have hunger / I have cold. | I'**m** hungry / I'**m** cold. | Sensaciones con **be** |
| I have a doubt. | I have **a question**. | doubt = desconfianza |
| Explain me this. | Explain this **to me**. | explain **to** someone |
| Say me the error. | **Tell** me the error. | tell + persona; say + algo |
| It depends of the OS. | It depends **on** the OS. | depend **on** |
| I'm agree. | I agree. | agree es verbo, no adjetivo |
| I am boring with this bug. | I am **bored** with this bug. | bored = aburrido (sentir); boring = aburrido (que aburre) |
| Make a question. | **Ask** a question. | ask a question |
| Do a mistake. | **Make** a mistake. | make a mistake |
| I didn't went. | I didn't **go**. | Tras did, verbo base |
| Did you tried it? | Did you **try** it? | Tras did, verbo base |
| Can you to help me? | Can you help me? | Tras modal, sin to |
| I want that you review it. | I want **you to review** it. | want + persona + to |
| It's more easy. | It's **easier**. | Comparativo corto con -er |
| More better / more faster | **better** / **faster** | No dobles el comparativo |
| Since three days. | **For** three days. | for + duración |
| I'm here since Monday. | I'**ve been** here since Monday. | Duración hasta hoy = present perfect |
| Yesterday I have fixed it. | Yesterday I **fixed** it. | Con tiempo pasado concreto, pasado simple |
| If it will fail... | If it **fails**... | Tras if, presente |
| It's the same that before. | It's the same **as** before. | same **as** |
| Different of | Different **from** | different from |
| Very much bugs | **A lot of** bugs / **many** bugs | very much no va con sustantivos |
| How is called this? | **What** is this called? | Orden y what para nombres |
| What means "deprecated"? | What **does** "deprecated" **mean**? | Preguntas con do/does |
| Where is the file? It's in the line 5. | It's **on** line 5. | on line N, sin the |
| I didn't nothing. | I didn't **do anything**. / I did nothing. | Una sola negación |
| Nobody don't know. | Nobody knows. | Una sola negación |

### 🗂️ Vocabulario y plurales

| ❌ Mal | ✅ Bien | Por qué |
|---|---|---|
| informations | information | Incontable |
| softwares | software / programs | Incontable |
| hardwares | hardware | Incontable |
| feedbacks | feedback / comments | Incontable |
| advices | advice / tips | Incontable |
| a code | some code / a snippet | Incontable como programa |
| datas | data | Ya es plural (o incontable) |
| a criteria | a criterion | criteria es plural |
| actually (= actualmente) | currently | actually = en realidad |
| eventually (= quizás) | possibly / occasionally | eventually = al final |
| assist to the meeting | **attend** the meeting | assist = ayudar |
| realize a task | **carry out** / **do** / **perform** a task | realize = darse cuenta |
| a sensible data | **sensitive** data | sensible = sensato |
| I'm exited | I'm **excited** | exited = salió (de un proceso) |
| I can't login | I can't **log in** | verbo separado |
| open the computer | **turn on** the computer | open = abrir físicamente |
| close the light | **turn off** the light | luces y aparatos: turn on/off |
| the career of Computer Science | the Computer Science **degree / program** | career = trayectoria profesional |
| make a test | **run** a test / **write** a test | run tests |
| put a password | **set** / **enter** a password | set / enter |
| win money | **earn** money | earn = ganar trabajando |
| I'm learning about the course | I'm **taking** the course | take a course |
| the last version (la más nueva) | the **latest** version | latest = más reciente |
| many money | a lot of money / much money | money es incontable: no lleva many |
| programmation | programming | programmation no existe |
| a computation engineer | a computer engineer / software engineer | — |
| carpet | folder / directory | carpet = alfombra |
| file (fila) | row | file = archivo |

### ✍️ Ortografía y puntuación

| ❌ Mal | ✅ Bien | Por qué |
|---|---|---|
| ¿How are you? | How are you? | Sin signo de apertura |
| ¡Thanks! | Thanks! | Sin signo de apertura |
| monday, january, english, python | Monday, January, English, Python | Días, meses, idiomas y nombres propios con mayúscula |
| i think | **I** think | "I" siempre mayúscula |
| Its working. | **It's** working. | it's = it is; its = su |
| Your welcome. | **You're** welcome. | you're = you are |
| Their is a bug. | **There** is a bug. | there / their / they're |
| Then (comparación) | **Than** | faster **than**; then = luego |
| Loose (perder) | **Lose** | lose data; loose = suelto |
| Affect vs effect | affect (verbo) / effect (sustantivo) | "it **affects** performance" / "side **effect**" |
| Lenght, widht | length, width | Orden de letras |
| Seperate, recieve, occured | separate, receive, occurred | Ortografía frecuente en código |
| Adress | address | doble d, doble s |
| Comit, comited | commit, committed | doble t al añadir -ed |
| 1.000 users / 3,5 MB | 1,000 users / 3.5 MB | En inglés la coma separa miles y el punto decimales |

::: columnas
### ❌ Mal
- "It don't work."
- "The function return a list."
- "Is possible to do it."
::: siguiente
### ✅ Bien
- "It **doesn't** work."
- "The function **returns** a list."
- "**It is** possible to do it."
:::

⚠️ Cuidado: el formato numérico al revés del español causa bugs reales: `float("3,5")` lanza `ValueError` en Python. En código siempre punto decimal.

💡 Consejo: después de escribir un issue o PR, revisa solo tres cosas: **¿cada frase tiene sujeto?**, **¿puse -s en tercera persona?**, **¿los contables singulares tienen artículo?** Eso elimina el 80% de errores.

🇬🇧 Frase modelo corregida: ❌ "Is not working, I have a doubt, explain me please" → ✅ "**It**'s not working and I have **a question**. Could you **explain it to me**, please?"

## ⚙️ Verbos de código y documentación

Los nombres de funciones casi siempre empiezan con un **verbo en imperativo**. Conocer el verbo exacto (y en qué se diferencia de sus sinónimos) te deja adivinar qué hace una función sin leer su código, y elegir buenos nombres para las tuyas.

### 📥 Leer y obtener datos

| Verbo | Español | Matiz | Nombres reales |
|---|---|---|---|
| get | obtener | Genérico, normalmente rápido y local, sin efectos | `getItem`, `dict.get`, `getattr` |
| fetch | traer, ir a buscar | Desde fuera, por red, suele ser asíncrono | `fetch(url)`, `fetchPosts`, `git fetch` |
| retrieve | recuperar | Buscar algo guardado (BD, caché, almacén) | `retrieve_document`, RAG = Retrieval |
| load | cargar | Leer de disco o recurso a memoria | `json.load`, `loadModel`, `torch.load` |
| read | leer | Leer bytes o texto de un flujo | `file.read`, `readFileSync`, `pd.read_csv` |
| query | consultar | Pedir con criterios (SQL, API) | `queryUsers`, `useQuery` |
| find | encontrar | Buscar y devolver el primero (o null) | `Array.find`, `findOne` |
| search | buscar | Buscar varios por texto o criterio | `searchProducts`, `re.search` |
| lookup / look up | consultar (por clave) | Buscar por clave en tabla o diccionario | `dns.lookup`, `lookupUser` |
| select | seleccionar | Elegir subconjunto (SQL, DOM) | `SELECT`, `querySelector` |
| peek | echar un vistazo | Ver sin sacar (pilas, colas) | `stack.peek()` |
| pull | traer (y aplicar) | Traer cambios remotos | `git pull`, `docker pull` |
| download | descargar | Bajar archivo a disco | `download_file` |
| scan | escanear, recorrer | Recorrer todo buscando algo | `os.scandir`, `SCAN` en Redis |
| inspect | inspeccionar | Mirar el detalle interno | `docker inspect`, `inspect` (Python) |
| list | listar | Devolver todos los elementos | `listdir`, `listUsers` |
| count | contar | Devolver cuántos hay | `count()`, `COUNT(*)` |

### 📤 Escribir, cambiar y guardar

| Verbo | Español | Matiz | Nombres reales |
|---|---|---|---|
| set | asignar | Cambiar un valor concreto | `setState`, `setTimeout`, `setattr` |
| put | poner | Guardar en una clave o lugar (a veces reemplaza) | `map.put`, HTTP `PUT`, `queue.put` |
| save | guardar | Persistir en disco o BD | `model.save`, `save_checkpoint` |
| store | almacenar | Guardar para después | `storeToken`, `localStorage` |
| write | escribir | Escribir bytes o texto en un flujo | `file.write`, `writeFile` |
| update | actualizar | Modificar algo que ya existe | `updateProfile`, `dict.update` |
| patch | parchear | Cambio parcial | HTTP `PATCH`, `mock.patch` |
| upsert | insertar o actualizar | Insert si no existe, update si sí | `upsert`, `ON CONFLICT DO UPDATE` |
| insert | insertar | Meter en una posición o tabla | `list.insert`, `INSERT INTO` |
| append | añadir al final | Siempre al final | `list.append`, `appendChild` |
| prepend | añadir al principio | Siempre al inicio | `prepend()` |
| push | empujar, subir | Añadir al final de pila o subir a remoto | `arr.push`, `git push` |
| pop | sacar | Quitar el último (o el indicado) y devolverlo | `arr.pop`, `dict.pop` |
| shift / unshift | sacar / meter por delante | Al inicio del array (JS) | `arr.shift()` |
| mutate | mutar | Cambiar el objeto original (vs crear uno nuevo) | `useMutation`, "don't mutate state" |
| assign | asignar | Dar valor o copiar propiedades | `Object.assign` |
| commit | confirmar | Hacer permanente un cambio | `db.commit()`, `git commit` |
| flush | vaciar (al destino) | Forzar que lo pendiente se escriba | `stdout.flush()`, `flush=True` |
| sync | sincronizar | Igualar dos lados | `fsync`, `rsync` |
| persist | persistir | Que sobreviva a reinicios | `persist()`, "persisted state" |

### 🆕 Crear: create vs make vs build vs generate

| Verbo | Matiz | Ejemplo | Cuándo elegirlo |
|---|---|---|---|
| create | Crear una entidad nueva (registro, objeto, archivo) | `createUser`, `os.makedirs` crea carpetas | Algo nuevo que antes no existía |
| make | Fabricar (más informal, también herramienta) | `make`, `makedirs`, `mkdir` | Utilidades, casi sinónimo de create |
| build | Construir algo complejo a partir de partes | `npm run build`, `docker build`, `buildQuery` | Hay un proceso de ensamblado o compilación |
| generate | Producir automáticamente (por reglas o al azar) | `generateToken`, `uuid4`, `model.generate` | La máquina lo produce (IDs, código, texto) |
| new | Instanciar (palabra clave) | `new Date()`, `NewClient` (Go) | Constructores |
| init / initialize | Preparar el estado inicial | `__init__`, `git init`, `initApp` | Poner a punto antes de usar |
| instantiate | Crear una instancia de una clase | "instantiate the model" | Hablando de POO |
| spawn | Lanzar un proceso o hilo hijo | `child_process.spawn`, `spawnWorker` | Procesos, hilos, enemigos en juegos |
| fork | Duplicar un proceso o repo | `os.fork`, botón Fork | Copia que luego diverge |
| clone | Copiar exactamente | `git clone`, `structuredClone` | Copia idéntica |
| copy | Copiar | `shutil.copy`, `copy.deepcopy` | Copia (superficial o profunda) |
| compile | Compilar | `re.compile`, `tsc` | De código fuente a otra forma |
| scaffold | Generar estructura base | `npm create vite`, "scaffold a project" | Plantillas de proyecto |

### 🗑️ Borrar: remove vs delete vs drop vs clear vs destroy

| Verbo | Matiz | Ejemplo | Peligro |
|---|---|---|---|
| remove | Quitar de un contenedor (puede seguir existiendo fuera) | `list.remove(x)`, `removeEventListener`, `git rm` | 🟡 Medio |
| delete | Borrar el dato o recurso en sí | `DELETE FROM`, `deleteUser`, `del d[k]` | 🟠 Alto |
| drop | Eliminar una estructura entera (tabla, columna, BD) o descartar | `DROP TABLE`, `df.drop`, "drop support for 3.8" | 🔴 Muy alto |
| clear | Vaciar el contenido, el contenedor sigue | `list.clear()`, `clearCache`, `clearTimeout` | 🟡 Medio |
| truncate | Vaciar rápido o cortar a un tamaño | `TRUNCATE TABLE`, `truncate(text, 50)` | 🔴 Alto en SQL |
| destroy | Destruir y liberar recursos (no se puede usar más) | `destroy()`, `terraform destroy` | 🔴 Muy alto |
| dispose | Liberar recursos (memoria, conexiones) | `dispose()`, `IDisposable` | 🟢 Limpieza |
| purge | Borrar todo a fondo, sin vuelta atrás | `purge`, `pacman -Rns`, `docker system prune` | 🔴 Muy alto |
| prune | Podar lo que sobra o no se usa | `git remote prune`, `docker image prune` | 🟡 Medio |
| erase | Borrar (posiciones de un contenedor) | `vector.erase` (C++) | 🟡 Medio |
| discard | Descartar cambios | `git restore` "discard changes", `set.discard` | 🟠 Pierdes cambios |
| unset | Quitar el valor de una variable | `unset VAR`, `git config --unset` | 🟢 Bajo |
| revoke | Anular un permiso o token | `revokeToken` | 🟢 Seguridad |
| uninstall | Desinstalar | `pip uninstall` | 🟢 Bajo |
| kill / terminate | Matar un proceso | `kill -9`, `process.terminate()` | 🟠 Se pierde el estado |

### 🧠 Procesar y transformar

| Verbo | Español | Matiz | Nombres reales |
|---|---|---|---|
| parse | analizar, interpretar | Texto → estructura | `JSON.parse`, `argparse`, `parseInt` |
| serialize | serializar | Estructura → texto o bytes | `json.dumps`, `JSON.stringify`, `pickle.dump` |
| deserialize | deserializar | Texto o bytes → estructura | `json.loads`, `pickle.load` |
| encode / decode | codificar / decodificar | Cambiar representación (UTF-8, base64) | `str.encode`, `atob` |
| encrypt / decrypt | cifrar / descifrar | Con clave secreta | `encrypt(data, key)` |
| hash | hashear | Resumen irreversible | `hashlib.sha256`, `bcrypt.hash` |
| format | formatear | Presentar bonito | `str.format`, `formatDate` |
| convert | convertir | Cambiar tipo o formato | `convert_to_rgb` |
| transform | transformar | Aplicar una operación a datos | `transform()`, `transforms.Compose` |
| normalize | normalizar | Llevar a una forma o escala estándar | `normalize()`, `unicodedata.normalize` |
| sanitize | sanear | Quitar lo peligroso (inyección, XSS) | `sanitizeHtml` |
| validate | validar | Comprobar reglas y avisar | `validateEmail`, `model_validate` |
| escape | escapar | Proteger caracteres especiales | `html.escape`, `re.escape` |
| strip / trim | recortar | Quitar espacios en los extremos | `str.strip`, `String.trim` |
| split / join | dividir / unir | Cadena ↔ lista | `str.split`, `", ".join(x)` |
| map | mapear | Aplicar función a cada elemento | `arr.map(fn)` |
| filter | filtrar | Quedarse con los que cumplen | `arr.filter(fn)` |
| reduce / fold | reducir | Combinar en un solo valor | `functools.reduce` |
| flatten | aplanar | Lista de listas → lista | `arr.flat()`, `torch.flatten` |
| merge | fusionar | Unir dos en uno | `merge()`, `pd.merge`, `git merge` |
| aggregate | agregar | Resumir (suma, media...) | `df.agg`, `GROUP BY` |
| sort | ordenar | Orden | `sort`, `sorted` |
| shuffle | barajar | Orden aleatorio | `random.shuffle` |
| slice | rebanar | Tomar una parte | `arr.slice(0, 3)`, `s[1:4]` |
| wrap / unwrap | envolver / desenvolver | Rodear o sacar de un contenedor | `Option.unwrap` (Rust), `functools.wraps` |
| bind | enlazar | Atar a un contexto, puerto o valor | `fn.bind(this)`, `socket.bind` |
| resolve | resolver | Encontrar el valor final o cumplir una promesa | `Promise.resolve`, `path.resolve`, DNS resolve |
| compute / calculate | calcular | Operaciones | `computeLoss` |
| evaluate | evaluar | Calcular el valor de una expresión o medir un modelo | `eval`, `model.evaluate` |
| infer | inferir | Deducir (tipos o predicción de un modelo) | type inference, `infer()` |

### 🎛️ Control de ejecución, eventos y errores

| Verbo | Español | Matiz | Nombres reales |
|---|---|---|---|
| call / invoke | llamar, invocar | Ejecutar una función (invoke es más formal) | `fn.call`, `lambda invoke` |
| execute / run | ejecutar | Correr código, consulta o comando | `cursor.execute`, `npm run` |
| apply | aplicar | Ejecutar con argumentos o aplicar cambios | `fn.apply`, `df.apply`, `kubectl apply` |
| handle | manejar | Responder a un evento o error | `handleClick`, `handle_exception` |
| trigger | disparar | Provocar que algo ocurra | `triggerBuild`, "triggers a re-render" |
| fire | disparar (evento) | Lanzar un evento | "the event fires twice" |
| emit | emitir | Enviar un evento a quien escuche | `socket.emit`, `emitter.emit` |
| dispatch | despachar | Enviar una acción o evento a quien lo procese | `dispatch(action)` (Redux), `dispatchEvent` |
| listen | escuchar | Esperar eventos o conexiones | `app.listen(3000)`, `addEventListener` |
| subscribe / unsubscribe | suscribirse / anular | Registrarse para recibir eventos | `store.subscribe` |
| notify | notificar | Avisar a los observadores | `notifyAll` |
| throw / raise | lanzar | Provocar una excepción | `throw new Error`, `raise ValueError` |
| catch / except | atrapar | Capturar una excepción | `try/catch`, `try/except` |
| rethrow | relanzar | Volver a lanzar tras atrapar | `raise` sin argumentos |
| reject | rechazar | Fallar una promesa | `Promise.reject`, `reject(err)` |
| await | esperar | Esperar a una promesa o corrutina | `await fetch()` |
| yield | ceder, producir | Devolver un valor y pausar (generador) | `yield item`, "yields control" |
| block | bloquear | Esperar sin dejar hacer otra cosa | "a blocking call" |
| schedule | programar | Ejecutar más tarde | `setTimeout`, `cron`, `scheduler` |
| defer | aplazar | Ejecutar al final | `defer` (Go), `<script defer>` |
| debounce / throttle | rebotar / limitar | Limitar la frecuencia de llamadas | `debounce(fn, 300)` |
| retry | reintentar | Volver a intentar tras fallar | `retry(times=3)` |
| abort / cancel | abortar / cancelar | Detener algo en curso | `AbortController`, `task.cancel()` |
| skip | saltar | No ejecutar | `pytest.skip`, `--skip-tests` |
| exit / quit | salir | Terminar el programa | `sys.exit(1)`, `process.exit` |
| return | devolver | Salir de la función con valor | `return result` |
| break / continue | romper / continuar | Salir del bucle / pasar a la siguiente vuelta | `break` |
| fallback / fall back | recurrir a | Usar una alternativa si falla | "falls back to UTF-8" |
| hook | enganchar | Insertar código en un punto | `useEffect` (hook), git hooks |
| mount / unmount | montar / desmontar | Conectar al DOM o al sistema de archivos | `onMounted`, `mount /dev/sdb1` |
| render | renderizar | Producir la vista | `render()`, `ReactDOM.render` |
| hydrate | hidratar | Dar interactividad a HTML del servidor | `hydrateRoot` |
| cache / memoize | cachear / memorizar | Guardar resultados para reusarlos | `@lru_cache`, `useMemo` |
| lock / unlock | bloquear | Exclusión mutua | `threading.Lock`, `package-lock.json` |
| toggle | alternar | on ↔ off | `toggleMenu`, `classList.toggle` |
| enable / disable | activar / desactivar | Encender una opción | `--enable-gpu` |
| register | registrar | Dar de alta en un sistema | `registerServiceWorker`, `app.register_blueprint` |
| inject | inyectar | Pasar una dependencia desde fuera | dependency injection, `@Inject` |
| expose | exponer | Hacer visible al exterior | `EXPOSE 8080` (Docker), "exposes an API" |
| deploy / ship / release | desplegar / sacar / publicar | Llevar a producción | `deploy.sh`, "ship it" |
| rollback / revert | deshacer | Volver atrás | `ROLLBACK`, `git revert` |
| migrate | migrar | Cambiar esquema o versión | `manage.py migrate` |
| bump | subir (versión) | Incrementar número de versión | "bump version to 1.2.0" |

### ✅ Ejemplo resuelto: leer código solo por los verbos

```js
async function syncUserProfile(userId) {
  const cached = cache.get(userId);              // mira en caché local (rápido)
  if (cached && !isExpired(cached)) return cached;
  const raw = await fetchProfile(userId);         // va a la red a por el perfil
  const profile = normalizeProfile(parseJson(raw)); // texto → objeto → formato estándar
  validateProfile(profile);                       // lanza error si no cumple las reglas
  await db.upsert("profiles", profile);           // inserta o actualiza en la BD
  cache.set(userId, profile);                     // guarda en caché
  emitter.emit("profile:updated", profile);       // avisa a quien escuche
  return profile;
}
```

| Verbo | Qué te dice sin leer el cuerpo |
|---|---|
| sync | Va a igualar dos fuentes (red, BD, caché) |
| get | Barato, local, puede devolver vacío |
| fetch | Lento, red, por eso lleva `await` |
| parse → normalize | Primero interpretar, luego dejar en forma estándar |
| validate | Puede lanzar excepción |
| upsert | No falla si ya existe |
| emit | Otras partes del programa reaccionarán |

💡 Consejo: **get** = barato y local; **fetch** = red o espera (normalmente `async`); **load** = de disco; **retrieve** = de un almacén; **compute** = lo calcula. Si tu función tarda, no la llames `getX`.

⚠️ Cuidado: **remove** no siempre borra: `list.remove(x)` quita el elemento de la lista, pero el objeto puede seguir vivo en otra variable. **delete** y **drop** sí eliminan el dato. Lee el verbo antes de ejecutar un comando destructivo.

🇬🇧 Frase de doc: "This method **mutates** the array **in place** and **returns** `undefined`" = modifica el array original y no devuelve nada (por ejemplo `arr.forEach`); compara con "**returns a new** array" (`arr.map`).

## 🏷️ Nombrar variables, funciones, clases, ramas y archivos

Un buen nombre explica el código sin comentarios. El 80% del tiempo programando lo pasas **leyendo** código, así que un nombre claro vale más que un comentario. Reglas de oro: **funciones = verbo**, **variables y clases = sustantivo**, **booleanos = pregunta**, **colecciones = plural**.

### 🐫 Estilos de escritura

| Estilo | Ejemplo | Dónde se usa |
|---|---|---|
| camelCase | `userName`, `getUserById` | Variables y funciones en JS, TS, Java, Kotlin, Swift |
| PascalCase | `UserProfile`, `HttpClient` | Clases, tipos, interfaces, componentes React, C# métodos |
| snake_case | `user_name`, `get_user_by_id` | Python, Rust, Ruby, SQL, PHP (funciones) |
| SCREAMING_SNAKE_CASE | `MAX_RETRIES`, `API_KEY` | Constantes y variables de entorno |
| kebab-case | `user-profile.css`, `fix-login-bug` | Archivos web, URLs, clases CSS, ramas Git, paquetes npm |
| lowercase | `numpy`, `os`, `mypackage` | Paquetes Python y Go |
| dot.case | `app.config.js`, `eslint.config.mjs` | Archivos de configuración |
| Train-Case | `Content-Type`, `X-Request-Id` | Cabeceras HTTP |

### 🌍 Convenciones por lenguaje

| Lenguaje | Variables / funciones | Clases / tipos | Constantes | Archivos |
|---|---|---|---|---|
| Python (PEP 8) | `snake_case` | `PascalCase` | `UPPER_SNAKE` | `snake_case.py` |
| JavaScript | `camelCase` | `PascalCase` | `UPPER_SNAKE` o `camelCase` | `kebab-case.js` o `camelCase.js` |
| TypeScript | `camelCase` | `PascalCase` (sin prefijo I) | `UPPER_SNAKE` | `kebab-case.ts` |
| React | `camelCase` (hooks: `useX`) | `PascalCase` componentes | `UPPER_SNAKE` | `UserCard.tsx` |
| Java | `camelCase` | `PascalCase` | `UPPER_SNAKE` | `UserService.java` (igual que la clase) |
| Kotlin | `camelCase` | `PascalCase` | `UPPER_SNAKE` | `UserService.kt` |
| C# | `camelCase` (locales) / `PascalCase` (métodos) | `PascalCase` (interfaces `IUser`) | `PascalCase` | `UserService.cs` |
| C | `snake_case` | `snake_case` o `PascalCase` (structs) | `UPPER_SNAKE` (macros) | `snake_case.c` / `.h` |
| C++ | `snake_case` o `camelCase` | `PascalCase` | `kConstant` o `UPPER_SNAKE` | `snake_case.cpp` |
| Go | `camelCase` (privado) / `PascalCase` (exportado) | `PascalCase` | `PascalCase` o `camelCase` | `snake_case.go` |
| Rust | `snake_case` | `PascalCase` | `UPPER_SNAKE` | `snake_case.rs` |
| PHP | `camelCase` | `PascalCase` | `UPPER_SNAKE` | `PascalCase.php` |
| SQL | `snake_case` columnas | `snake_case` tablas (plural o singular, consistente) | — | `001_create_users.sql` |
| CSS | `kebab-case` clases | BEM: `card__title--active` | `--kebab-case` variables | `kebab-case.css` |
| Bash | `snake_case` locales | — | `UPPER_SNAKE` entorno | `kebab-case.sh` |

### ❓ Booleanos: que suenen a pregunta de sí o no

| Prefijo | Pregunta | Ejemplos | Evita |
|---|---|---|---|
| is | ¿Está / es...? (estado) | `isLoading`, `isValid`, `is_admin` | `loading` (¿es bool o función?) |
| has | ¿Tiene...? (posesión) | `hasPermission`, `hasChildren`, `has_errors` | `permission` |
| can | ¿Puede...? (capacidad) | `canEdit`, `canSubmit` | `editable` (vale, pero menos claro) |
| should | ¿Debería...? (decisión) | `shouldRetry`, `shouldRender` | `retry` |
| was / did | ¿Ocurrió...? (pasado) | `wasDeleted`, `didMount` | `deleted` (¿fecha o bool?) |
| will | ¿Va a...? (futuro) | `willExpire` | — |
| needs | ¿Necesita...? | `needsUpdate`, `needs_migration` | — |
| allow / enable | ¿Se permite / activa...? | `allowDuplicates`, `enableCache` | `noCache` (negación) |

⚠️ Cuidado: evita booleanos en negativo: `isNotEnabled`, `disableNoCache`. `if (!isNotEnabled)` obliga a pensar dos veces. Usa `isEnabled` y niega con `!`.

### 🧩 Qué palabra usar para cada cosa

| Qué nombras | Forma | ✅ Ejemplos | ❌ Evitar |
|---|---|---|---|
| Función que hace algo | verbo + objeto | `sendEmail`, `calculate_tax`, `parseConfig` | `email`, `tax`, `config` |
| Función que devuelve bool | is/has + adjetivo | `isEmpty()`, `has_access()` | `checkEmpty()` (¿qué devuelve?) |
| Función que convierte | to + destino / from + origen | `toString`, `toJSON`, `fromDict` | `stringConvert` |
| Clase | sustantivo singular | `User`, `Invoice`, `PaymentGateway` | `Users`, `DoPayment`, `Manager` vago |
| Clase que hace algo | sustantivo de agente (-er/-or) | `Parser`, `Validator`, `HttpClient` | `ParseData` |
| Interfaz o trait | adjetivo -able o sustantivo | `Serializable`, `Comparable`, `Repository` | `IInterface` |
| Colección | plural | `users`, `orderItems`, `selected_ids` | `userList`, `arr`, `data` |
| Diccionario o mapa | `xByY` / `x_to_y` | `usersById`, `price_by_product`, `id_to_name` | `dict1`, `map` |
| Contador | `count` / `numX` / `xCount` | `retryCount`, `num_users` | `cont`, `n2` |
| Índice | `index` / `i` en bucles cortos | `currentIndex`, `for i in range(n)` | `indice`, `idx2` |
| Unidades | sufijo de unidad | `timeoutMs`, `delay_seconds`, `sizeInBytes` | `timeout` (¿ms o s?) |
| Fechas | `xAt` (momento) / `xOn` (día) | `createdAt`, `expires_at`, `birthDate` | `fecha`, `date1` |
| Evento (prop) | `on` + evento | `onClick`, `onSubmit` | `click` |
| Manejador | `handle` + evento | `handleClick`, `handle_submit` | `clickFunction` |
| Hook de React | `use` + cosa | `useAuth`, `useFetchUsers` | `authHook` |
| Constante | sustantivo en mayúsculas | `MAX_UPLOAD_SIZE`, `DEFAULT_TIMEOUT_MS` | `max`, `TEN` |
| Callback | verbo o `onX` | `onSuccess`, `transform`, `compareFn` | `cb2` |
| Promesa o tarea | sustantivo + `Promise` / `task` | `userPromise`, `download_task` | `p` |

### 🌿 Ramas, archivos y carpetas

| Qué | Convención | ✅ Ejemplos | ❌ Evitar |
|---|---|---|---|
| Rama de funcionalidad | `feature/` o `feat/` + kebab-case | `feature/dark-mode`, `feat/google-login` | `rama-nueva`, `yafer2` |
| Rama de bug | `fix/` o `bugfix/` + descripción | `fix/null-avatar-crash` | `arreglo` |
| Rama urgente | `hotfix/` | `hotfix/payment-timeout` | `urgente!!` |
| Rama de tarea | `chore/`, `docs/`, `refactor/` | `docs/update-readme`, `refactor/auth-service` | `cambios` |
| Rama con issue | prefijo + número | `fix/123-login-redirect` | `issue` |
| Ramas principales | `main`, `develop`, `release/1.2` | `release/2.0.0` | `master2` |
| Archivo de componente | PascalCase | `UserCard.tsx`, `NavBar.vue` | `usercard-final.tsx` |
| Módulo Python | snake_case corto | `data_loader.py`, `utils/text.py` | `Data Loader.py`, `módulo.py` |
| Script de shell | kebab-case + `.sh` | `backup-db.sh` | `script final(2).sh` |
| Test | `test_` o `.test` / `.spec` | `test_parser.py`, `parser.test.ts` | `prueba.py` |
| Config | nombre estándar | `.env`, `pyproject.toml`, `tsconfig.json` | `config_mia.json` |
| Carpetas | minúsculas, plural o rol | `src/`, `tests/`, `components/`, `utils/` | `Nueva carpeta/` |
| Migraciones | número o fecha + acción | `0003_add_email_to_users.py` | `migracion.py` |
| Imágenes y assets | kebab-case descriptivo | `logo-dark.svg`, `hero-banner@2x.png` | `IMG_2024.png` |

### ❌ Nombres malos vs ✅ nombres buenos

| ❌ Mal | ✅ Bien | Qué estaba mal |
|---|---|---|
| `data2` | `cleanedOrders` | Número sin significado |
| `temp` | `swapValue`, `unsavedDraft` | No dice qué guarda |
| `foo`, `bar`, `baz` | `retryDelay` | Solo valen en ejemplos |
| `x`, `y` (fuera de matemáticas) | `width`, `height` | Una letra no explica |
| `getUsuarios()` | `getUsers()` | Spanglish |
| `lista_users` | `users` | Spanglish y tipo en el nombre |
| `calcularTotal` | `calculateTotal` | Mezcla de idiomas en el proyecto |
| `año` | `year` | ñ y tildes en identificadores |
| `flag` | `isDirty`, `hasUnsavedChanges` | ¿Bandera de qué? |
| `doStuff()` | `syncInventory()` | Verbo vago |
| `process(x)` | `resizeImage(image)` | Verbo vago y argumento opaco |
| `handleData()` | `saveSurveyAnswers()` | "data" no dice nada |
| `Manager`, `Helper`, `Util` | `InvoiceRepository`, `DateFormatter` | Clases cajón de sastre |
| `userList` | `users` | Ya es plural |
| `strName` | `name` | Notación húngara innecesaria |
| `btn`, `msg`, `usr` | `button`, `message`, `user` | Abreviaturas raras |
| `numberOfTheUsersThatAreActive` | `activeUserCount` | Demasiado largo |
| `isNotValid` | `isInvalid` o `!isValid` | Negación en el nombre |
| `getUser()` que también lo borra | `popUser()` o separar funciones | El nombre miente |
| `check()` que devuelve objeto | `findUser()` | check suena a bool |
| `timeout = 30` | `timeoutSeconds = 30` | Falta la unidad |
| `date` | `createdAt` | ¿Qué fecha? |
| `arr` | `scores` | Nombre del tipo, no del contenido |
| `obj` | `config` | Nombre del tipo, no del contenido |
| `res2` | `paymentResponse` | Número sin significado |
| `final_final_v2.py` | `train_model.py` (y usa Git) | Versiones en el nombre |
| `MyClass` | `ShoppingCart` | Nombre de tutorial |
| `def f(l):` | `def mean(values):` | `l` se confunde con `1` |
| `const DATA = fetch()` | `const response = await fetch(url)` | No es constante; mayúsculas engañan |
| `value_of_the_price` | `price` | Palabras de relleno |

### ✅ Ejemplo resuelto: renombrar código de estudiante

```python
# ❌ Antes: spanglish, abreviaturas, nombres que no explican
def proc(l, f=False):
    res = []
    for x in l:
        if x["edad"] >= 18 or f:
            res.append(x["nombre"].strip().title())
    return res

lista_users = cargarUsuarios("users.json")
data2 = proc(lista_users, True)

# ✅ Después: inglés consistente, verbo + objeto, plural, booleano con "include"
def get_adult_names(users, include_minors=False):
    names = []
    for user in users:
        if user["age"] >= 18 or include_minors:
            names.append(user["name"].strip().title())
    return names

users = load_users("users.json")
all_names = get_adult_names(users, include_minors=True)
```

| Cambio | Regla aplicada |
|---|---|
| `proc` → `get_adult_names` | Verbo + objeto, explica qué devuelve |
| `l` → `users`, `x` → `user` | Plural para la colección, singular para el elemento |
| `f` → `include_minors` | Booleano que se lee como frase |
| `res` → `names` | Nombre del contenido, no del rol |
| `edad`, `nombre` → `age`, `name` | Un solo idioma en el código |
| `cargarUsuarios` → `load_users` | snake_case en Python y verbo de disco |

### 🧰 Vocabulario para nombres

| Palabra | Significa | Ejemplo |
|---|---|---|
| current / previous / next | actual / anterior / siguiente | `currentPage`, `prevState` |
| initial / default | inicial / por defecto | `initialValue`, `DEFAULT_PORT` |
| raw / parsed / cleaned | crudo / interpretado / limpio | `rawHtml`, `parsedArgs` |
| pending / active / archived | pendiente / activo / archivado | `pendingOrders` |
| selected / checked / focused | seleccionado / marcado / con foco | `selectedIds` |
| min / max / total / average | mínimo / máximo / total / media | `maxRetries`, `averageLoss` |
| source / target / destination | origen / objetivo / destino | `sourcePath`, `targetDir` |
| input / output | entrada / salida | `inputTensor`, `output_file` |
| config / options / settings | configuración / opciones / ajustes | `options = {...}` |
| handler / listener / callback | manejador / escuchador / función de vuelta | `errorHandler` |
| payload / body / params | carga / cuerpo / parámetros | `requestBody` |
| entry / item / record | entrada / elemento / registro | `logEntry` |
| buffer / chunk / batch | búfer / trozo / lote | `chunkSize`, `batch` |
| threshold / limit / cap | umbral / límite / tope | `confidenceThreshold` |
| legacy / deprecated / experimental | heredado / obsoleto / experimental | `legacyApi` |

💡 Consejo: si no encuentras un buen nombre, la función probablemente hace **demasiadas cosas**. Divídela hasta que cada parte tenga un verbo claro.

⚠️ Cuidado: no mezcles idiomas en el mismo proyecto. Todo el **código** en inglés; los **textos que ve el usuario** (botones, mensajes) sí pueden estar en español, mejor en archivos de traducción (i18n).

🇬🇧 Frase de code review: "Could we **rename** `data` **to** something more descriptive, **like** `pendingInvoices`?"

📌 Resumen: **verbo** para funciones · **sustantivo** para clases · **plural** para colecciones · **is/has/can** para booleanos · **unidad** en el nombre · **un solo idioma**.

## 🧯 Anatomía de un mensaje de error

Casi todos los errores siguen la forma **Tipo: qué pasó + dónde**. El texto largo asusta, pero solo necesitas tres cosas: **qué tipo** de error es, **qué palabra clave** describe el problema y **qué línea de tu código** lo provocó. Los demás programadores pierden horas leyendo el traceback de arriba abajo; tú léelo de abajo arriba.

### 🔑 Palabras clave de los errores

| Palabra | Suena | Significa | Ejemplo real |
|---|---|---|---|
| expected | iks-PÉK-tid | se esperaba | `SyntaxError: expected ':'` |
| unexpected | an-iks-PÉK-tid | inesperado | `Unexpected token '}'` |
| undefined | an-di-FÁIND | no definido | `x is not defined` / `undefined` |
| undeclared | an-di-KLÉRD | no declarado | `'b' undeclared` |
| unresolved | an-ri-SÓLVD | no resuelto (no se encontró) | `unresolved import`, `Unresolved reference` |
| missing | MÍ-sing | falta | `missing 1 required positional argument` |
| required | ri-KUÁI-erd | obligatorio | `field required` |
| invalid | in-VÁ-lid | inválido | `invalid syntax`, `invalid literal` |
| illegal | i-LÍ-gal | no permitido por las reglas | `IllegalArgumentException` |
| unsupported | an-su-PÓR-tid | no soportado | `unsupported operand type(s)` |
| deprecated | DÉ-pre-kei-tid | obsoleto, se eliminará | `DeprecationWarning` |
| mismatch | MÍS-match | no coincide | `type mismatch`, `shape mismatch` |
| incompatible | in-kom-PÁ-ti-bol | incompatible | `incompatible types` |
| not assignable | not a-SÁI-na-bol | no se puede asignar | `Type 'string' is not assignable to type 'number'` |
| out of range / bounds | aut ov reinch / baunds | fuera de rango / límites | `list index out of range` |
| overflow | ÓU-ver-flou | desbordamiento | `stack overflow`, `integer overflow` |
| underflow | ÁN-der-flou | desbordamiento por abajo | `float underflow` |
| exceeded | ik-SÍ-did | superado | `maximum recursion depth exceeded` |
| timeout / timed out | TÁIM-aut | tiempo agotado | `Connection timed out` |
| refused | ri-FIÚSD | rechazado | `Connection refused` |
| denied | di-NÁID | denegado | `Permission denied` |
| forbidden | for-BÍ-den | prohibido | `403 Forbidden` |
| unauthorized | an-Ó-zo-raizd | no autenticado | `401 Unauthorized` |
| conflict | KÁN-flikt | conflicto | `Merge conflict`, `409 Conflict` |
| ambiguous | am-BÍ-giu-os | ambiguo | `column reference "id" is ambiguous` |
| unreachable | an-RÍ-cha-bol | inalcanzable | `Network is unreachable`, `unreachable code` |
| unhandled / uncaught | an-JÁN-dold / an-KÓT | no manejado / no atrapado | `Uncaught TypeError`, `UnhandledPromiseRejection` |
| failed | feild | falló | `Build failed`, `failed to push` |
| fatal | FÉI-tal | fatal, no se puede seguir | `fatal: not a git repository` |
| abort / aborted | a-BÓRT | abortado | `Aborted (core dumped)` |
| corrupt / corrupted | ko-RÁP-tid | dañado | `corrupted size vs. prev_size` |
| duplicate | DÚ-pli-kit | duplicado | `duplicate key value` |
| already exists / in use | ol-RÉ-di ig-SISTS | ya existe / ya en uso | `address already in use` |
| not found | not faund | no encontrado | `404 Not Found`, `command not found` |
| no such | nou sach | no existe tal | `No such file or directory` |
| cannot / can't | KÁ-not | no se puede | `cannot import name` |
| unable to | an-ÉI-bol tu | incapaz de | `unable to resolve dependency tree` |
| violates | VÁI-o-leits | viola (una regla) | `violates foreign key constraint` |
| constraint | kons-TRÉINT | restricción | `NOT NULL constraint failed` |
| implicit / implicitly | im-PLÍ-sit | implícito, sin declarar | `implicitly has an 'any' type` |
| possibly | PÓ-si-bli | posiblemente | `Object is possibly 'undefined'` |
| leak | lik | fuga | `memory leak` |
| hang / hung | jang | colgado | `the process hangs` |
| panic | PÁ-nik | pánico (error irrecuperable) | `thread 'main' panicked at` (Rust) |
| segfault | ség-folt | fallo de segmentación | `Segmentation fault` |
| dumped | dampt | volcado | `core dumped` |
| stale | steil | desactualizado, caducado | `stale file handle`, `stale cache` |
| dangling | DÁNG-ling | colgante, que apunta a nada | `dangling pointer` |
| detached | di-TÁCHT | separado | `detached HEAD` |
| diverged | dai-VÉRDYD | divergido | `have diverged` |
| hint | jint | pista | `hint: Updates were rejected...` |
| traceback / stack trace | TRÉIS-bak | rastro de llamadas | `Traceback (most recent call last)` |

### 🧱 Anatomía de un stack trace

```text
Traceback (most recent call last):
  File "/home/yafer/shop/main.py", line 18, in <module>
    report = build_report(orders)
  File "/home/yafer/shop/report.py", line 9, in build_report
    total = sum_prices(orders)
  File "/home/yafer/shop/report.py", line 4, in sum_prices
    return sum(o["price"] for o in orders)
KeyError: 'price'
```

| Parte | En el ejemplo | Qué te dice |
|---|---|---|
| Cabecera | `Traceback (most recent call last):` | Rastro de llamadas; la más reciente está **al final** |
| Frame externo | `main.py, line 18, in <module>` | Dónde empezó todo (el script principal) |
| Frames intermedios | `report.py, line 9, in build_report` | El camino de funciones que se fueron llamando |
| Frame final | `report.py, line 4, in sum_prices` | La línea exacta donde explotó |
| Código de la línea | `return sum(o["price"] ...)` | El código culpable, copiado |
| `File "..."` | ruta del archivo | Si es **tuyo** o de una librería (`site-packages`) |
| `line N` | número de línea | Abre el editor justo ahí |
| `in nombre` | función que se ejecutaba | `<module>` = nivel superior del archivo |
| Tipo de error | `KeyError` | La categoría del problema |
| Mensaje | `'price'` | El detalle: aquí, la clave que no existe |

| Lenguaje | Dónde está lo importante | Forma típica |
|---|---|---|
| Python | Abajo (última línea) | `Traceback (most recent call last):` ... `Error: mensaje` |
| JavaScript / Node | Arriba (primera línea) | `TypeError: mensaje` + líneas `at función (archivo:línea:columna)` |
| Java | Arriba + `Caused by:` | `Exception in thread "main" ...` + `at paquete.Clase.metodo(Archivo.java:12)` |
| C / C++ | Compilador: `archivo:línea:columna: error:` | `main.c:5:12: error: ...` |
| Rust | Arriba con flecha `-->` | `error[E0382]: borrow of moved value` + `--> src/main.rs:4:20` |
| Go | `panic:` + goroutine | `panic: runtime error: index out of range [5] with length 3` |

```js
TypeError: Cannot read properties of undefined (reading 'name')
    at renderUser (/home/yafer/app/src/user.js:12:23)
    at main (/home/yafer/app/src/index.js:5:3)
    at Object.<anonymous> (/home/yafer/app/src/index.js:8:1)
    at Module._compile (node:internal/modules/cjs/loader:1554:14)
```

| Pieza JS | Significa |
|---|---|
| `TypeError: ...` | Tipo y mensaje (lo primero que lees) |
| `at renderUser` | Función donde ocurrió |
| `user.js:12:23` | Archivo, línea 12, columna 23 |
| `Object.<anonymous>` | Código suelto del módulo (sin función) |
| `node:internal/...` | Código interno de Node: ignóralo |

### 🪜 Método en 5 pasos para cualquier error

| Paso | Qué haces | Pregunta clave |
|---|---|---|
| 1 | Lee el **tipo** de error | ¿Es de sintaxis, de tipo, de red, de permisos? |
| 2 | Lee el **mensaje** y busca la **palabra clave** | ¿missing, unexpected, denied, not found? |
| 3 | Busca la primera línea que sea de **tu** código | Salta las de `site-packages`, `node_modules`, `node:internal` |
| 4 | Lee esa línea y la anterior | ¿Qué valor tenía cada variable? |
| 5 | Si no lo entiendes, busca el mensaje **sin tus nombres** | `TypeError: Cannot read properties of undefined (reading` + lenguaje |

```flujo
dir: abajo
Error -> Tipo : TypeError, KeyError...
Tipo -> Mensaje : palabra clave
Mensaje -> Tu línea : salta site-packages
Tu línea -> Valores : qué valía cada variable
Valores -> Buscar : mensaje sin tus nombres
```

⚠️ Cuidado: el error de los principiantes es leer **solo** la primera línea del traceback de Python (que es la más lejana) o copiar en Google el mensaje con tus rutas (`/home/yafer/...`). Quita rutas, nombres de variables y números propios.

⚠️ Cuidado: un **warning** no detiene el programa, un **error** sí. Pero los warnings de deprecación de hoy son los errores de mañana: léelos.

💡 Consejo: en Python, `python -X dev` y `PYTHONWARNINGS=default` muestran más avisos; en Node, `--trace-warnings` te dice de dónde viene un warning.

## 🐍 Errores de Python

Python tiene los mensajes de error más legibles: casi son frases completas. Desde Python 3.10 incluso sugieren la solución ("**Did you mean**...?") y desde 3.11 marcan con `^^^^` la parte exacta que falló. Estos son los que te vas a encontrar el 95% de las veces.

### 🔤 Sintaxis e indentación (antes de ejecutar)

| Mensaje literal | Qué significa | Causa típica | Qué hacer |
|---|---|---|---|
| `SyntaxError: invalid syntax` | Sintaxis inválida | Falta `:`, paréntesis, comillas; `=` en vez de `==` | Mira la línea marcada **y la anterior** |
| `SyntaxError: expected ':'` | Se esperaba `:` | `if x > 0` sin dos puntos | Añade `:` al final de `if/for/def/class` |
| `SyntaxError: '(' was never closed` | El paréntesis nunca se cerró | Falta `)` (a veces el error sale líneas después) | Cuenta paréntesis; el editor los empareja |
| `SyntaxError: unterminated string literal (detected at line 3)` | String sin cerrar | Falta comilla de cierre | Cierra la comilla |
| `SyntaxError: invalid syntax. Perhaps you forgot a comma?` | Quizás olvidaste una coma | Lista o argumentos sin coma | Pon la coma |
| `SyntaxError: cannot assign to function call here. Maybe you meant '==' instead of '='?` | No puedes asignar a una llamada | `if f() = 3` | Usa `==` |
| `SyntaxError: 'return' outside function` | `return` fuera de función | Mala indentación | Indenta dentro del `def` |
| `IndentationError: expected an indented block after 'if' statement on line 2` | Se esperaba un bloque indentado | `if` sin cuerpo | Añade cuerpo o `pass` |
| `IndentationError: unexpected indent` | Sangría inesperada | Espacios de más al inicio | Alinea con el bloque |
| `IndentationError: unindent does not match any outer indentation level` | La sangría no coincide con ningún nivel | Mezcla de 2 y 4 espacios | Usa siempre 4 espacios |
| `TabError: inconsistent use of tabs and spaces in indentation` | Mezcla de tabs y espacios | Copiar y pegar código | Convierte tabs a espacios en el editor |

### 🧮 Nombres, tipos y valores

| Mensaje literal | Qué significa | Causa típica | Qué hacer |
|---|---|---|---|
| `NameError: name 'pirnt' is not defined. Did you mean: 'print'?` | El nombre no existe | Error de tipeo, falta `import`, variable aún no creada | Corrige el nombre o importa |
| `UnboundLocalError: cannot access local variable 'x' where it is not associated with a value` | Variable local usada antes de tener valor | Asignas `x` dentro de la función y la usas antes | Usa `global`/`nonlocal` o pásala como argumento |
| `TypeError: unsupported operand type(s) for +: 'int' and 'str'` | Operación no soportada entre esos tipos | `5 + "3"` | Convierte: `5 + int("3")` |
| `TypeError: can only concatenate str (not "int") to str` | Solo se concatena str con str | `"Edad: " + 20` | f-string: `f"Edad: {age}"` |
| `TypeError: greet() missing 1 required positional argument: 'name'` | Falta un argumento obligatorio | Llamada con menos argumentos | Pasa el argumento; en métodos, ¿olvidaste `self`? |
| `TypeError: g() takes 1 positional argument but 2 were given` | Recibe 1 y le diste 2 | Falta `self` en el método o argumento de más | Añade `self` o quita el argumento |
| `TypeError: f() got an unexpected keyword argument 'colour'` | Argumento con nombre inesperado | Nombre mal escrito o versión distinta | Revisa la firma en la doc |
| `TypeError: 'NoneType' object is not subscriptable` | `None` no admite `[ ]` | Una función devolvió `None` | Revisa el `return`; `list.sort()` devuelve `None` |
| `TypeError: 'int' object is not iterable` | No se puede recorrer un entero | `for i in 10` | `for i in range(10)` |
| `TypeError: 'str' object is not callable` | Un string no se puede llamar | Tapaste una función: `str = "hola"` y luego `str(5)` | No uses nombres de built-ins como variables |
| `TypeError: unhashable type: 'list'` | Una lista no puede ser clave | `{[1, 2]: "a"}` o `set([[1]])` | Usa una tupla. En 3.14: `cannot use 'list' as a dict key` |
| `TypeError: string indices must be integers, not 'str'` | Índices de string deben ser enteros | Tratas un string como dict (JSON sin parsear) | `json.loads(...)` primero |
| `TypeError: object of type 'int' has no len()` | Un entero no tiene longitud | `len(5)` | Revisa el tipo con `type(x)` |
| `TypeError: Object of type datetime is not JSON serializable` | No se puede convertir a JSON | Fechas, sets u objetos en `json.dumps` | `default=str` o conviértelo antes |
| `AttributeError: 'NoneType' object has no attribute 'split'` | `None` no tiene ese atributo | Algo devolvió `None` (función sin return, regex sin match) | Comprueba `if x is not None` |
| `AttributeError: 'list' object has no attribute 'split'` | Las listas no tienen `.split` | Lo usas sobre una lista y no un string | Recorre la lista o únela |
| `AttributeError: module 'numpy' has no attribute 'float'` | El módulo ya no tiene eso | Alias eliminado en NumPy 1.24 | Usa `float` o `np.float64` |
| `AttributeError: partially initialized module 'random' has no attribute 'randint' (most likely due to a circular import)` | Módulo a medio cargar | Llamaste a tu archivo `random.py` | Renombra tu archivo (no uses nombres de librerías) |
| `IndexError: list index out of range` | Índice fuera de rango | `lista[5]` con 5 elementos (empieza en 0) | Revisa `len()` y los bucles |
| `KeyError: 'email'` | La clave no existe | JSON distinto al esperado | `d.get("email")` o `"email" in d` |
| `ValueError: invalid literal for int() with base 10: 'abc'` | Texto que no es número | `int("abc")`, `int("3.5")` | Valida la entrada; `float()` para decimales |
| `ValueError: too many values to unpack (expected 2, got 3)` | Sobran valores al desempaquetar | `a, b = [1, 2, 3]` | Ajusta variables o usa `*rest` |
| `ValueError: not enough values to unpack (expected 3, got 2)` | Faltan valores | `a, b, c = (1, 2)` | Revisa la forma de los datos |
| `ValueError: list.remove(x): x not in list` | El elemento no está | `remove` de algo que no existe | Comprueba con `in` antes |
| `ZeroDivisionError: division by zero` | División entre cero | Lista vacía al sacar una media | Comprueba el divisor |
| `RecursionError: maximum recursion depth exceeded` | Recursión demasiado profunda | Falta caso base | Añade caso base o hazlo iterativo |
| `StopIteration` | El iterador se agotó | `next()` sin más elementos | `next(it, None)` |
| `AssertionError` | Falló un `assert` | Una condición que creías cierta no lo es | Mira qué valor tenía |
| `KeyboardInterrupt` | Interrumpido por teclado | Pulsaste Ctrl+C | Nada (o captúralo para limpiar) |
| `MemoryError` | Sin memoria | Cargaste demasiados datos | Procesa por trozos (chunks) |

```arbol
Exception
  SyntaxError
    IndentationError
      TabError
  LookupError
    IndexError
    KeyError
  ArithmeticError
    ZeroDivisionError
  ImportError
    ModuleNotFoundError
  OSError
    FileNotFoundError
    PermissionError
  ValueError
    UnicodeError
```

### 📦 Archivos, imports, codificación y entornos

| Mensaje literal | Qué significa | Causa típica | Qué hacer |
|---|---|---|---|
| `ModuleNotFoundError: No module named 'numpy'` | No se encuentra el módulo | No instalado **en este** entorno | Activa el venv y `pip install numpy` |
| `ImportError: cannot import name 'foo' from 'bar'` | Ese nombre no existe en el módulo | Versión distinta o import circular | Revisa la doc de la versión instalada |
| `ImportError: attempted relative import with no known parent package` | Import relativo sin paquete | Ejecutas `python archivo.py` con `from .x import y` | Ejecuta `python -m paquete.modulo` |
| `FileNotFoundError: [Errno 2] No such file or directory: 'data.csv'` | No existe ese archivo | Directorio actual distinto | `pwd`; usa rutas con `pathlib` |
| `PermissionError: [Errno 13] Permission denied: '/etc/hosts'` | Permiso denegado | Escribir en carpeta del sistema | Usa otra ruta o revisa permisos |
| `IsADirectoryError: [Errno 21] Is a directory: 'data'` | Es una carpeta, no archivo | `open("data")` | Indica el archivo dentro |
| `FileExistsError: [Errno 17] File exists: 'out'` | Ya existe | `os.mkdir` de algo existente | `exist_ok=True` |
| `json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)` | No es JSON válido | Respuesta vacía o HTML de error | Imprime la respuesta antes de parsear |
| `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xf1 in position 0: invalid continuation byte` | No es UTF-8 válido | Archivo en Latin-1 (la ñ = 0xf1) | `open(f, encoding="latin-1")` |
| `UnicodeEncodeError: 'ascii' codec can't encode character '\xf1'` | No se puede codificar en ASCII | Terminal o archivo en ASCII | Usa `encoding="utf-8"` |
| `error: externally-managed-environment` | El Python del sistema está protegido (PEP 668) | `pip install` global en Arch, Debian, Fedora | Crea un venv o usa `pipx` |
| `WARNING: The script flask is installed in '/home/u/.local/bin' which is not on PATH.` | El ejecutable no está en el PATH | Instalación de usuario | Añade `~/.local/bin` al PATH |
| `ERROR: Could not find a version that satisfies the requirement tensorflow==2.20` | No hay esa versión para ti | Tu Python es demasiado nuevo o la versión no existe | Revisa versiones soportadas |
| `ERROR: No matching distribution found for torch` | No hay paquete compatible | Python o plataforma no soportados | Usa una versión de Python compatible |
| `ERROR: Failed building wheel for xyz` | No se pudo compilar el paquete | Faltan compiladores o cabeceras | Instala `base-devel` / `python-dev` o usa versión con wheel |

### 🤖 Errores de IA y datos (PyTorch, NumPy, pandas)

| Mensaje literal | Qué significa | Causa típica | Qué hacer |
|---|---|---|---|
| `torch.OutOfMemoryError: CUDA out of memory. Tried to allocate 2.00 GiB` | La GPU se quedó sin memoria | Batch o modelo grande | Baja `batch_size`, usa `torch.no_grad()` en inferencia |
| `RuntimeError: Expected all tensors to be on the same device, but found at least two devices, cuda:0 and cpu!` | Tensores en dispositivos distintos | Modelo en GPU, datos en CPU | `.to(device)` en ambos |
| `RuntimeError: mat1 and mat2 shapes cannot be multiplied (32x784 and 128x10)` | Las formas no encajan para multiplicar | Capa con tamaño de entrada mal | Ajusta `in_features` |
| `ValueError: operands could not be broadcast together with shapes (3,) (4,)` | NumPy no puede combinar esas formas | Arrays de tamaños distintos | Revisa `.shape` |
| `SettingWithCopyWarning: A value is trying to be set on a copy of a slice from a DataFrame` | Modificas una copia, no el original | Asignar sobre un filtro | Usa `.loc[...]` o `.copy()` |
| `KeyError: "None of [Index(['edad'], dtype='object')] are in the [columns]"` | Esas columnas no existen | Nombre de columna distinto | `df.columns` para ver los nombres |

⚠️ Cuidado: el error **número uno** de estudiantes en Python es llamar a su archivo como una librería (`random.py`, `numpy.py`, `email.py`, `token.py`). Python importa **tu** archivo y todo falla con mensajes raros.

💡 Consejo: lee los `^^^^^` debajo del código en el traceback: desde Python 3.11 marcan **exactamente** la parte de la expresión que falló.

🇬🇧 Frase para preguntar: "I'm getting `KeyError: 'price'` when I iterate over the orders. It looks like some orders don't have a `price` field."

## 🟨 Errores de JavaScript, Node y TypeScript

En JavaScript el error importante va **arriba** del stack. En el navegador aparece en la consola con **Uncaught** (nadie lo atrapó) o **Uncaught (in promise)** (una promesa rechazada sin `.catch`). TypeScript, en cambio, te avisa **antes** de ejecutar, con un código `TSxxxx` que puedes buscar.

### 🟨 JavaScript (navegador y Node)

| Mensaje literal | Qué significa | Causa típica | Qué hacer |
|---|---|---|---|
| `TypeError: Cannot read properties of undefined (reading 'map')` | No se puede leer una propiedad de `undefined` | `data.map` antes de que llegue el fetch | Valor inicial `[]` o `data?.map` |
| `TypeError: Cannot read properties of null (reading 'addEventListener')` | El elemento es `null` | `querySelector` no encontró nada; script antes del HTML | `defer` en el script o revisa el selector |
| `TypeError: Cannot set properties of undefined (setting 'name')` | No se puede asignar a `undefined` | `obj.user.name = x` sin `obj.user` | Crea el objeto antes |
| `TypeError: user.getName is not a function` | Eso no es una función | Nombre mal escrito, import incorrecto | `console.log(typeof user.getName)` |
| `TypeError: Assignment to constant variable.` | Reasignas una `const` | `const x = 1; x = 2` | Usa `let` |
| `TypeError: Converting circular structure to JSON` | Objeto con referencia a sí mismo | `JSON.stringify` de un objeto con ciclos | Quita el ciclo o usa un replacer |
| `TypeError: Failed to fetch` (navegador; en Node: `fetch failed`) | La petición no llegó | Servidor caído, CORS, URL mal, sin red | Revisa la pestaña Network |
| `ReferenceError: x is not defined` | La variable no existe | Error de tipeo o fuera de scope | Declárala o impórtala |
| `ReferenceError: Cannot access 'x' before initialization` | Usada antes de `let/const` | Temporal Dead Zone | Mueve la declaración arriba |
| `ReferenceError: require is not defined in ES module scope, you can use import instead` | `require` en un módulo ES | `"type": "module"` en package.json | Usa `import` |
| `SyntaxError: Unexpected token '}'` | Token inesperado | Llave, paréntesis o coma de más o de menos | Formatea con Prettier para verlo |
| `SyntaxError: Unexpected token '<', "<!DOCTYPE "... is not valid JSON` | Recibiste HTML en vez de JSON | URL de API mal, servidor devolvió página de error | Imprime `await res.text()` |
| `SyntaxError: Unexpected end of JSON input` | JSON vacío o cortado | Respuesta sin cuerpo (204) | Comprueba `res.ok` y el cuerpo |
| `SyntaxError: Cannot use import statement outside a module` | `import` en un script no-módulo | Falta `"type": "module"` o `<script type="module">` | Añade el tipo módulo |
| `SyntaxError: Identifier 'x' has already been declared` | Ya declarada | Dos `let x` en el mismo scope | Renombra o reasigna |
| `SyntaxError: await is only valid in async functions and the top level bodies of modules` | `await` fuera de función async | Falta `async` | Marca la función como `async` |
| `RangeError: Maximum call stack size exceeded` | Pila de llamadas desbordada | Recursión infinita o `setState` en bucle | Busca la función que se llama a sí misma |
| `RangeError: Invalid array length` | Longitud de array inválida | `new Array(-1)` | Valida el número |
| `Uncaught (in promise) TypeError: ...` | Promesa rechazada sin manejar | Falta `try/catch` o `.catch` | Envuelve el `await` en `try/catch` |

```secuencia
Navegador -> API : OPTIONS /data (preflight)
API --> Navegador : sin Access-Control-Allow-Origin
nota Navegador : bloqueado por CORS
Navegador -> API : GET /data (nunca se envía)
```

### 🟩 Node.js y servidores

| Mensaje literal | Qué significa | Causa típica | Qué hacer |
|---|---|---|---|
| `Error: Cannot find module 'express'` | No encuentra el módulo | No instalado o ruta relativa mal | `npm install express`; revisa `./` |
| `Error: listen EADDRINUSE: address already in use :::3000` | Puerto ocupado | Otro servidor (o el mismo) sigue abierto | `lsof -i :3000` y ciérralo, o cambia de puerto |
| `Error: connect ECONNREFUSED 127.0.0.1:5432` | Conexión rechazada | PostgreSQL apagado o puerto distinto | Arranca el servicio |
| `Error: ENOENT: no such file or directory, open 'config.json'` | No existe el archivo | Ruta relativa al directorio actual | Usa `path.join(__dirname, ...)` |
| `Error: EACCES: permission denied, mkdir '/usr/lib/node_modules'` | Permiso denegado | `npm install -g` sin permisos | Usa un gestor de versiones (nvm, fnm) |
| `Error: getaddrinfo ENOTFOUND api.example.com` | No se resolvió el dominio | Dominio mal escrito o sin internet | Revisa la URL y el DNS |
| `Error: socket hang up` | El otro lado cortó la conexión | Timeout del servidor o proxy | Revisa logs del servidor |
| `FATAL ERROR: Reached heap limit Allocation failed - JavaScript heap out of memory` | Node se quedó sin memoria | Build grande o fuga | `NODE_OPTIONS=--max-old-space-size=4096` |
| `Access to fetch at '...' from origin 'http://localhost:3000' has been blocked by CORS policy` | Bloqueado por CORS | El **servidor** no permite tu origen | Configura CORS en el backend |
| `No 'Access-Control-Allow-Origin' header is present on the requested resource.` | Falta la cabecera CORS | Backend sin middleware CORS | Añade `cors()` o la cabecera |

### ⚛️ React

| Mensaje literal | Qué significa | Causa típica | Qué hacer |
|---|---|---|---|
| `Warning: Each child in a list should have a unique "key" prop.` | Cada hijo de una lista necesita `key` única | `map` sin `key` | `key={item.id}` (no el índice si reordenas) |
| `Error: Too many re-renders. React limits the number of renders to prevent an infinite loop.` | Demasiados renders | `onClick={setX(1)}` en vez de `onClick={() => setX(1)}` | Pasa una función, no la llamada |
| `Objects are not valid as a React child (found: object with keys {id, name}).` | No puedes pintar un objeto | `{user}` en JSX | `{user.name}` |
| `Invalid hook call. Hooks can only be called inside of the body of a function component.` | Hook en sitio prohibido | Hook dentro de `if`, bucle o función normal | Llama hooks arriba del componente |
| `Hydration failed because the initial UI does not match what was rendered on the server.` | El HTML del servidor no coincide | `Date.now()`, `Math.random()`, `window` en render | Mueve eso a `useEffect` |
| `React Hook useEffect has a missing dependency: 'userId'.` | Falta una dependencia (ESLint) | Array de dependencias incompleto | Añádela o justifica |

### 🔷 TypeScript

| Mensaje literal | Qué significa | Causa típica | Qué hacer |
|---|---|---|---|
| `TS2322: Type 'string' is not assignable to type 'number'.` | Ese tipo no se puede asignar | Valor del tipo equivocado | Convierte o corrige el tipo |
| `TS2345: Argument of type 'string' is not assignable to parameter of type 'number'.` | Argumento de tipo incorrecto | Pasas un string donde va número | `Number(x)` o cambia la firma |
| `TS2339: Property 'foo' does not exist on type 'User'.` | Esa propiedad no existe en el tipo | Tipo incompleto o error de tipeo | Añádela a la interfaz |
| `TS2551: Property 'lenght' does not exist on type 'string'. Did you mean 'length'?` | No existe, ¿quisiste decir...? | Tipeo | Acepta la sugerencia |
| `TS18048: 'user' is possibly 'undefined'.` | Puede ser `undefined` | Resultado de `find`, prop opcional | `if (user)`, `user?.name` |
| `TS2531: Object is possibly 'null'.` | Puede ser `null` | `getElementById` | Comprueba antes o `!` si estás seguro |
| `TS7006: Parameter 'x' implicitly has an 'any' type.` | Parámetro sin tipo | `strict` activado | Anota: `(x: number)` |
| `TS2304: Cannot find name 'foo'.` | No encuentra el nombre | Falta import o tipos (`@types/node`) | Importa o instala los tipos |
| `TS2307: Cannot find module 'lodash' or its corresponding type declarations.` | No encuentra módulo o sus tipos | Falta paquete o `@types/lodash` | `npm i -D @types/lodash` |
| `TS2554: Expected 2 arguments, but got 1.` | Esperaba 2 argumentos | Falta uno | Pásalo o hazlo opcional con `?` |
| `TS2741: Property 'age' is missing in type '{ name: string; }' but required in type 'User'.` | Falta una propiedad obligatoria | Objeto incompleto | Añádela o márcala `age?:` |
| `TS2366: Function lacks ending return statement and return type does not include 'undefined'.` | No todos los caminos devuelven | Falta `return` en un `else` | Añade `return` final |
| `TS2564: Property 'name' has no initializer and is not definitely assigned in the constructor.` | Propiedad sin inicializar | Clase con `strict` | Inicialízala o usa `!` |
| `TS7053: Element implicitly has an 'any' type because expression of type 'string' can't be used to index type` | No se puede indexar con string | `obj[key]` con key genérico | `Record<string, T>` o `keyof typeof obj` |
| `TS1005: ';' expected.` | Se esperaba `;` | Sintaxis rota | Mira la línea anterior |

⚠️ Cuidado: el error de CORS **no se arregla en el frontend**. Muchos estudiantes instalan extensiones "Allow CORS" en el navegador: funciona en tu PC y falla en producción. Se configura en el servidor.

⚠️ Cuidado: no silencies TypeScript con `any` o `// @ts-ignore` a la primera. El error suele avisarte de un bug real (por ejemplo, un `undefined` que romperá en producción).

💡 Consejo: busca los errores de TypeScript **por su código**: "TS2345" da resultados exactos aunque el mensaje tenga tus tipos.

## ☕ Errores de Java, C/C++ y SQL

En lenguajes compilados hay dos momentos de error: **compile time** (el compilador no te deja compilar) y **runtime** (compila pero explota al ejecutar). En C y C++ algunos errores ni siquiera dan mensaje: el programa simplemente muere con un **segfault**.

### ☕ Java

| Mensaje literal | Qué significa | Causa típica | Qué hacer |
|---|---|---|---|
| `error: cannot find symbol` | No encuentra el símbolo | Variable, método o clase mal escrita o sin importar | Revisa la línea `symbol:` que viene debajo |
| `error: incompatible types: String cannot be converted to int` | Tipos incompatibles | Asignar String a int | `Integer.parseInt(s)` |
| `error: ';' expected` | Falta punto y coma | Línea sin `;` | Añádelo (mira la línea anterior) |
| `error: missing return statement` | Falta `return` | Un camino del método no devuelve | Añade `return` al final |
| `error: variable x might not have been initialized` | Puede no estar inicializada | Variable local sin valor | Dale valor inicial |
| `error: class Main is public, should be declared in a file named Main.java` | Nombre de archivo ≠ clase | Archivo `main.java` o `Programa.java` | Renombra el archivo |
| `error: unreported exception IOException; must be caught or declared to be thrown` | Excepción comprobada sin manejar | Leer archivo sin `try` | `try/catch` o `throws IOException` |
| `error: non-static method foo() cannot be referenced from a static context` | Método de instancia desde `static` | Llamar desde `main` sin objeto | Crea un objeto o hazlo `static` |
| `Exception in thread "main" java.lang.NullPointerException: Cannot invoke "String.length()" because "name" is null` | Puntero nulo | Usar un objeto `null` | Inicializa o comprueba `!= null` |
| `java.lang.ArrayIndexOutOfBoundsException: Index 5 out of bounds for length 5` | Índice fuera de límites | `arr[arr.length]` | Bucle hasta `< length` |
| `java.lang.StringIndexOutOfBoundsException` | Índice de string fuera | `substring` con índices mal | Revisa `length()` |
| `java.lang.NumberFormatException: For input string: "abc"` | Formato de número inválido | `parseInt("abc")` | Valida la entrada |
| `java.lang.ClassCastException: class java.lang.Integer cannot be cast to class java.lang.String` | Conversión de clase imposible | Cast incorrecto | Usa genéricos o `String.valueOf` |
| `java.lang.ArithmeticException: / by zero` | División entre cero (enteros) | Divisor 0 | Comprueba el divisor |
| `java.util.ConcurrentModificationException` | Modificación durante iteración | `list.remove` dentro de un for-each | Usa `Iterator.remove` o `removeIf` |
| `java.lang.StackOverflowError` | Pila desbordada | Recursión infinita | Caso base |
| `java.lang.OutOfMemoryError: Java heap space` | Sin memoria en el heap | Colecciones enormes o fuga | Más `-Xmx` o arreglar la fuga |
| `java.lang.ClassNotFoundException: com.mysql.cj.jdbc.Driver` | No encuentra la clase | Falta la dependencia en el classpath | Añádela en Maven o Gradle |
| `Caused by: ...` | Causado por (excepción original) | Excepción envuelta en otra | Lee el **último** `Caused by` |

### ⚙️ C y C++

```text
main.c:1:21: error: 'b' undeclared (first use in this function)
main.c:1:32: error: expected ';' before '}' token
main.c:1:13: error: implicit declaration of function 'printf' [-Wimplicit-function-declaration]
main.cpp:2:13: error: 'cout' was not declared in this scope; did you mean 'std::cout'?
/usr/bin/ld: /tmp/ccCXXTsV.o: in function `f':
main.c:(.text+0x17): undefined reference to `sqrt'
collect2: error: ld returned 1 exit status
```

| Mensaje literal | Qué significa | Causa típica | Qué hacer |
|---|---|---|---|
| `error: 'b' undeclared (first use in this function)` | Variable no declarada | Tipeo o declaración olvidada | Declárala |
| `error: expected ';' before '}' token` | Falta `;` antes de `}` | Última sentencia sin `;` | Añádelo |
| `error: implicit declaration of function 'printf'` | Función usada sin declarar | Falta `#include <stdio.h>` | Incluye la cabecera (en GCC 14+ es error) |
| `error: 'cout' was not declared in this scope; did you mean 'std::cout'?` | No declarado en este ámbito | Falta `std::` | Usa `std::cout` |
| `undefined reference to 'sqrt'` | Referencia indefinida (enlazador) | Falta enlazar la librería o el `.c` | `gcc main.c -lm` / compila todos los `.c` |
| `undefined reference to 'main'` | No hay función `main` | Compilas un archivo sin `main` | Compila junto al que tiene `main` |
| `collect2: error: ld returned 1 exit status` | El enlazador falló | Es consecuencia del error de arriba | Lee la línea anterior |
| `warning: comparison of integer expressions of different signedness: 'int' and 'long unsigned int'` | Comparas con y sin signo | `int i < v.size()` | Usa `size_t i` |
| `warning: unused variable 'x' [-Wunused-variable]` | Variable sin usar | Código muerto | Bórrala |
| `Segmentation fault (core dumped)` | Acceso a memoria no permitida | Puntero nulo, array fuera de rango, puntero colgante | `gdb`, `valgrind` o `-fsanitize=address` |
| `free(): double free detected in tcache 2` | Liberaste dos veces la misma memoria | `free(p)` repetido | `p = NULL` tras `free` |
| `munmap_chunk(): invalid pointer` | Puntero inválido al liberar | `free` de algo no reservado con malloc | Libera solo lo que reservaste |
| `*** stack smashing detected ***: terminated` | Desbordaste un array en la pila | Escribir fuera de un buffer local | Revisa tamaños y `strcpy` |
| `terminate called after throwing an instance of 'std::out_of_range'` | Excepción C++ no atrapada | `v.at(5)` con 5 elementos | `try/catch` o revisa índices |
| `Floating point exception (core dumped)` | Excepción aritmética | División **entera** entre 0 | Comprueba el divisor |
| `Aborted (core dumped)` | El programa abortó | `assert` falló o `abort()` | Mira el mensaje anterior |

### 🗄️ SQL (PostgreSQL, MySQL, SQLite)

| Mensaje literal | Qué significa | Causa típica | Qué hacer |
|---|---|---|---|
| `ERROR:  relation "users" does not exist` | La tabla no existe (Postgres) | Migración sin aplicar, esquema o mayúsculas | `\dt`; revisa comillas y esquema |
| `ERROR:  column "nmae" does not exist` | Columna inexistente | Tipeo o comillas dobles vs simples | Strings con comillas **simples** |
| `ERROR:  syntax error at or near "FROM"` | Error de sintaxis cerca de FROM | Coma de más antes de FROM | Revisa justo antes de esa palabra |
| `ERROR:  duplicate key value violates unique constraint "users_email_key"` | Valor duplicado en campo único | Insertar un email repetido | Valida antes o `ON CONFLICT` |
| `ERROR:  null value in column "email" of relation "users" violates not-null constraint` | Null en columna obligatoria | Falta el campo en el INSERT | Envía el valor |
| `ERROR:  insert or update on table "orders" violates foreign key constraint "orders_user_id_fkey"` | Clave foránea inexistente | `user_id` que no existe | Crea primero el usuario |
| `ERROR:  column "users.name" must appear in the GROUP BY clause or be used in an aggregate function` | Columna fuera del GROUP BY | SELECT con columnas no agrupadas | Añádela al GROUP BY o agrégala |
| `ERROR:  column reference "id" is ambiguous` | Columna ambigua | `id` existe en dos tablas del JOIN | Usa `users.id` |
| `ERROR:  operator does not exist: integer = text` | No existe ese operador | Comparar número con texto | Convierte con `::int` |
| `ERROR:  permission denied for table users` | Sin permiso | Rol sin `GRANT` | `GRANT SELECT ON users TO rol` |
| `FATAL:  password authentication failed for user "postgres"` | Falló la contraseña | Credenciales mal en `.env` | Revisa usuario y contraseña |
| `ERROR:  deadlock detected` | Interbloqueo | Dos transacciones esperándose | Ordena los bloqueos; reintenta |
| `ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: YES)` | Acceso denegado (MySQL) | Contraseña o host mal | Revisa credenciales |
| `ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version` | Error de sintaxis (MySQL) | Palabra reservada, coma | Mira el texto tras `near` |
| `ERROR 1146 (42S02): Table 'shop.users' doesn't exist` | La tabla no existe (MySQL) | BD equivocada | `USE shop;` / `SHOW TABLES;` |
| `ERROR 1062 (23000): Duplicate entry 'a@b.com' for key 'users.email'` | Entrada duplicada (MySQL) | Campo UNIQUE | Valida antes |
| `sqlite3.OperationalError: no such table: users` | No existe la tabla (SQLite) | Otra ruta de BD (se crea un archivo nuevo vacío) | Revisa la ruta del `.db` |
| `sqlite3.OperationalError: database is locked` | BD bloqueada | Otra conexión escribiendo | Cierra conexiones, usa timeout |
| `sqlite3.IntegrityError: UNIQUE constraint failed: users.email` | Viola UNIQUE (SQLite) | Email repetido | `INSERT OR IGNORE` o valida |

⚠️ Cuidado: en SQL, **"comillas dobles"** son nombres de columnas/tablas y **'comillas simples'** son textos. `WHERE name = "Ana"` en Postgres busca una **columna** llamada Ana.

💡 Consejo: en C/C++ compila siempre con `-Wall -Wextra -g -fsanitize=address`: los warnings te avisan del bug y el sanitizer convierte un segfault mudo en un mensaje con la línea exacta.

## 🐧 Errores de Linux, Git, Docker, npm y pip

Las herramientas de terminal tienen errores cortos y crípticos, pero muy repetidos. Fíjate en el **prefijo**: `bash:`, `fatal:`, `error:`, `npm ERR!`, `Error response from daemon:` te dicen **qué programa** se queja.

### 🐧 Terminal y sistema

| Mensaje literal | Qué significa | Causa típica | Qué hacer |
|---|---|---|---|
| `bash: nmp: command not found` | Comando no encontrado | Tipeo, no instalado o fuera del PATH | Corrige o instala; `which nombre` |
| `fish: Unknown command: nmp` | Igual, en fish | Lo mismo | Lo mismo |
| `zsh: command not found: tsc` | Igual, en zsh | Herramienta no instalada globalmente | `npx tsc` o instálala |
| `bash: ./script.sh: Permission denied` | Permiso denegado | Sin permiso de ejecución | `chmod +x script.sh` |
| `/bin/bash^M: bad interpreter: No such file or directory` | Intérprete inválido | Archivo con finales de línea de Windows (CRLF) | `dos2unix script.sh` |
| `ls: cannot access 'foo': No such file or directory` | No existe | Ruta mal escrita | `ls` del directorio padre |
| `rm: cannot remove 'dir': Is a directory` | Es una carpeta | `rm` sin `-r` | `rm -r dir` (con cuidado) |
| `mkdir: cannot create directory 'out': File exists` | Ya existe | Carpeta creada antes | `mkdir -p` |
| `cp: -r not specified; omitting directory 'src'` | Omitió una carpeta | `cp` sin `-r` | `cp -r` |
| `sudo: a terminal is required to read the password` | sudo necesita terminal | Script sin TTY | Ejecútalo en terminal interactiva |
| `Killed` | El sistema mató el proceso | Sin memoria (OOM killer) | Menos datos, más swap, revisa `dmesg` |
| `No space left on device` | Disco lleno | Logs, caché, imágenes Docker | `df -h`, `du -sh *`, limpia |
| `Argument list too long` | Demasiados argumentos | `rm *` con miles de archivos | `find . -name '*.log' -delete` |
| `Text file busy` | Archivo en uso | Sobrescribir un binario que corre | Para el proceso primero |
| `Too many open files` | Demasiados archivos abiertos | No cierras archivos o sockets | Cierra recursos; `ulimit -n` |
| `ssh: connect to host 192.168.1.10 port 22: Connection refused` | SSH rechazado | sshd apagado o puerto distinto | Arranca `sshd` o usa `-p` |
| `Permission denied (publickey).` | Clave rechazada | Tu clave SSH no está autorizada | Añade la clave pública al servidor o a GitHub |
| `WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!` | La huella del servidor cambió | Servidor reinstalado (o ataque) | Verifica y `ssh-keygen -R host` |
| `error: target not found: foo` | Paquete inexistente (pacman) | Nombre mal o está en AUR | `pacman -Ss` / usa `paru` |
| `error: failed to init transaction (unable to lock database)` | Base de pacman bloqueada | Otro pacman corriendo o se colgó | Si no hay otro: borra `/var/lib/pacman/db.lck` |

### 🌿 Git

| Mensaje literal | Qué significa | Causa típica | Qué hacer |
|---|---|---|---|
| `fatal: not a git repository (or any of the parent directories): .git` | No es un repositorio | Carpeta equivocada | `cd` al proyecto o `git init` |
| `CONFLICT (content): Merge conflict in app.py` | Conflicto de fusión | Dos ramas cambiaron las mismas líneas | Edita, `git add`, `git commit` |
| `Automatic merge failed; fix conflicts and then commit the result.` | Fusión automática falló | Lo mismo | Resuelve y haz commit |
| `! [rejected] main -> main (fetch first)` | Push rechazado | El remoto tiene commits que tú no | `git pull --rebase` y luego `git push` |
| `! [rejected] main -> main (non-fast-forward)` | No es avance directo | Historia divergente | `git pull --rebase` (no `--force` en ramas compartidas) |
| `error: failed to push some refs to 'github.com:user/repo.git'` | Falló el push | Consecuencia del rechazo | Lee el `hint:` |
| `fatal: The current branch feature has no upstream branch.` | La rama no tiene remoto asociado | Primer push de una rama nueva | `git push -u origin feature` |
| `fatal: refusing to merge unrelated histories` | Historias sin relación | Repo local y remoto creados por separado | `--allow-unrelated-histories` (si estás seguro) |
| `error: Your local changes to the following files would be overwritten by merge:` | Tus cambios se perderían | Cambios sin commit | `git stash`, pull, `git stash pop` |
| `fatal: Need to specify how to reconcile divergent branches.` | Hay que elegir cómo reconciliar | Ramas divergentes sin config | `git config pull.rebase true` |
| `You are in 'detached HEAD' state.` | HEAD separado de una rama | `checkout` de un commit o tag | `git switch -c nueva-rama` |
| `error: pathspec 'mian' did not match any file(s) known to git` | No coincide con nada | Rama o archivo mal escrito | `git branch -a` |
| `error: remote origin already exists.` | Ya hay un remoto origin | `git remote add` repetido | `git remote set-url origin URL` |
| `fatal: destination path 'repo' already exists and is not an empty directory.` | La carpeta ya existe | Clonaste dos veces | Clona en otra carpeta |
| `remote: Support for password authentication was removed on August 13, 2021.` | GitHub ya no acepta contraseña | Usaste tu contraseña en HTTPS | Token personal o SSH |
| `nothing to commit, working tree clean` | Nada que confirmar | No hay cambios (o no guardaste) | Guarda el archivo |
| `Your branch is ahead of 'origin/main' by 2 commits.` | Vas 2 commits por delante | Commits sin subir | `git push` |
| `Your branch is behind 'origin/main' by 3 commits, and can be fast-forwarded.` | Vas 3 por detrás | Otros subieron cambios | `git pull` |
| `warning: in the working copy of 'a.txt', LF will be replaced by CRLF the next time Git touches it` | Cambiará finales de línea | Windows y `core.autocrlf` | Configura `.gitattributes` |

### 🐳 Docker

| Mensaje literal | Qué significa | Causa típica | Qué hacer |
|---|---|---|---|
| `Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?` | No hay conexión con el demonio | Docker no arrancado | `sudo systemctl start docker` |
| `permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock` | Sin permiso al socket | Tu usuario no está en el grupo docker | `sudo usermod -aG docker $USER` y reinicia sesión |
| `Bind for 0.0.0.0:8080 failed: port is already allocated` | Puerto ya asignado | Otro contenedor o proceso lo usa | `docker ps`; cambia `-p 8081:80` |
| `Conflict. The container name "/web" is already in use by container` | Nombre de contenedor en uso | Contenedor viejo parado | `docker rm web` |
| `pull access denied for myimage, repository does not exist or may require 'docker login'` | No se puede descargar la imagen | Nombre mal o repo privado | Revisa nombre o haz `docker login` |
| `manifest unknown` | Esa etiqueta no existe | Tag mal escrito | Revisa tags en Docker Hub |
| `exec format error` | Formato de ejecutable incorrecto | Imagen de otra arquitectura (ARM vs x86) | `--platform linux/amd64` |
| `failed to solve: failed to compute cache key: ... not found` | No encuentra el archivo a copiar | `COPY` de algo fuera del contexto o en `.dockerignore` | Revisa rutas y `.dockerignore` |
| `Exited (137)` | Terminado con SIGKILL | Sin memoria (OOM) o `docker kill` | Más memoria o menos carga |
| `Exited (1)` | El proceso falló | Error de tu aplicación | `docker logs contenedor` |
| `no space left on device` | Disco lleno | Imágenes y capas viejas | `docker system prune` |

### 📦 npm y pip

| Mensaje literal | Qué significa | Causa típica | Qué hacer |
|---|---|---|---|
| `npm ERR! code ERESOLVE` | No resuelve dependencias | Versiones incompatibles (peer deps) | Actualiza paquetes; `--legacy-peer-deps` como último recurso |
| `npm ERR! ERESOLVE unable to resolve dependency tree` | No puede resolver el árbol | Lo mismo | Lee qué paquete pide qué versión |
| `npm error code ERESOLVE` | Igual (npm 10+) | Lo mismo | Lo mismo |
| `npm ERR! enoent Could not read package.json` | No encuentra package.json | Estás en otra carpeta | `cd` al proyecto |
| `npm ERR! Missing script: "dev"` | No existe ese script | No está en `"scripts"` | `npm run` para ver la lista |
| `npm WARN deprecated request@2.88.2: request has been deprecated` | Paquete obsoleto | Dependencia vieja | Busca alternativa si es tuya |
| `found 3 vulnerabilities (1 moderate, 2 high)` | Vulnerabilidades encontradas | Dependencias con CVE | `npm audit` y actualiza con cuidado |
| `sh: vite: command not found` | No encuentra el binario | No hiciste `npm install` | `npm install` |
| `npm ERR! code EINTEGRITY` | Checksum no coincide | Caché o lockfile corrupto | `npm cache verify`, borra `node_modules` |
| `error: externally-managed-environment` | Python del sistema protegido | `pip install` fuera de venv | `python -m venv .venv` |
| `ERROR: pip's dependency resolver does not currently take into account all the packages that are installed.` | Conflicto de dependencias | Dos paquetes piden versiones distintas | Entorno limpio y versiones fijadas |
| `ERROR: Could not install packages due to an OSError: [Errno 13] Permission denied` | Sin permiso | Instalar en el sistema | Usa venv |
| `Requirement already satisfied: numpy` | Ya instalado | Nada | Nada (no es error) |

⚠️ Cuidado: **nunca** copies `git push --force` o `sudo chmod -R 777 /` de un foro sin entenderlo. Muchos "arreglos" de Stack Overflow borran trabajo ajeno o rompen la seguridad. Lee qué hace cada flag.

⚠️ Cuidado: `npm install --force` y `--legacy-peer-deps` esconden el problema, no lo resuelven. Úsalos solo si entiendes qué dependencia choca.

💡 Consejo: en Git, lee siempre las líneas **hint:**. Git te escribe la solución literal: "hint: Updates were rejected because the remote contains work that you do not have locally... You may want to first integrate the remote changes (e.g., 'git pull ...') before pushing again."

## 🌐 Códigos de estado HTTP

El primer dígito te dice **de quién es la culpa**: 2xx todo bien, 3xx ve a otro sitio, **4xx la culpa es del cliente (tú)**, **5xx la culpa es del servidor**. Aprende los nombres en inglés: aparecen tal cual en logs, consolas y respuestas de APIs.

| Familia | Significa | Culpable | Ejemplo |
|---|---|---|---|
| 1xx | Informativo | Nadie | 101 Switching Protocols (WebSocket) |
| 2xx | Éxito | Nadie | 200 OK |
| 3xx | Redirección | Nadie (sigue la URL) | 301 Moved Permanently |
| 4xx | Error del cliente | Tu petición | 404 Not Found |
| 5xx | Error del servidor | El backend | 500 Internal Server Error |

| Código | Nombre en inglés | Significa | Causa típica | Qué hacer |
|---|---|---|---|---|
| 100 | Continue | Sigue enviando el cuerpo | Subidas grandes | Nada |
| 101 | Switching Protocols | Cambio de protocolo | Conexión WebSocket | Nada |
| 200 | OK | Todo bien | — | Nada |
| 201 | Created | Recurso creado | POST correcto | Lee el `Location` o el cuerpo |
| 202 | Accepted | Aceptado, se procesará luego | Tareas en cola | Consulta el estado después |
| 204 | No Content | Éxito sin cuerpo | DELETE o PUT | No hagas `res.json()` |
| 206 | Partial Content | Contenido parcial | Descargas por rangos, vídeo | Nada |
| 301 | Moved Permanently | Movido para siempre | URL cambiada, http → https | Actualiza la URL |
| 302 | Found | Redirección temporal | Login redirige | Sigue la redirección |
| 304 | Not Modified | No ha cambiado | Caché del navegador válida | Nada |
| 307 / 308 | Temporary / Permanent Redirect | Redirige sin cambiar el método | POST que se redirige | Sigue la URL |
| 400 | Bad Request | Petición mal formada | JSON roto, parámetro mal | Revisa el cuerpo y `Content-Type` |
| 401 | Unauthorized | No autenticado | Falta o caducó el token | Inicia sesión o renueva el token |
| 403 | Forbidden | Prohibido | Autenticado pero sin permiso | Revisa roles y permisos |
| 404 | Not Found | No existe | URL o id incorrecto | Revisa ruta, barra final, id |
| 405 | Method Not Allowed | Método no permitido | GET donde va POST | Usa el método correcto |
| 406 | Not Acceptable | No hay formato aceptable | Cabecera `Accept` rara | Revisa `Accept` |
| 408 | Request Timeout | El cliente tardó demasiado | Red lenta | Reintenta |
| 409 | Conflict | Conflicto con el estado actual | Ya existe, versión desactualizada | Revisa duplicados |
| 410 | Gone | Eliminado para siempre | API retirada | Usa la nueva |
| 413 | Content Too Large | Cuerpo demasiado grande | Archivo enorme (antes "Payload Too Large") | Sube límite o comprime |
| 415 | Unsupported Media Type | Tipo de contenido no soportado | Falta `Content-Type: application/json` | Pon la cabecera correcta |
| 418 | I'm a teapot | Soy una tetera (broma, RFC 2324) | — | Sonríe |
| 422 | Unprocessable Content | Formato bien, datos inválidos | Validación fallida (FastAPI, Rails) | Lee el detalle del error |
| 429 | Too Many Requests | Demasiadas peticiones | Rate limit | Espera (`Retry-After`), backoff |
| 500 | Internal Server Error | Error interno | Excepción en el backend | Mira los logs del servidor |
| 501 | Not Implemented | No implementado | Método no soportado | Usa otro endpoint |
| 502 | Bad Gateway | El proxy recibió mala respuesta | Backend caído tras nginx | Arranca o revisa el backend |
| 503 | Service Unavailable | No disponible | Sobrecarga o mantenimiento | Reintenta más tarde |
| 504 | Gateway Timeout | El proxy se cansó de esperar | Backend lento | Optimiza o sube el timeout |

⚠️ Cuidado: **401 Unauthorized** en realidad significa "no **autenticado**" (no sé quién eres), y **403 Forbidden** significa "no **autorizado**" (sé quién eres, pero no puedes). El nombre de 401 es históricamente confuso.

💡 Consejo: un `fetch` en JavaScript **no lanza error** con 404 o 500: solo con fallos de red. Comprueba siempre `if (!res.ok) throw new Error(res.status)`.

🇬🇧 Frase para un issue: "The endpoint returns **a** `422 Unprocessable Content` **when** the `email` field is empty, **but** it should return **a** `400`."

## 📖 Leer documentación

Las docs siempre tienen las mismas partes y usan las mismas fórmulas. Si sabes **dónde** está cada cosa, no lees la doc entera: saltas directo a lo que necesitas. Los programadores con experiencia rara vez leen de arriba abajo; van a **Usage**, **Parameters** y **Examples**.

### 🗂️ Partes de una página de documentación

| Sección | Traducción | Qué encuentras | Cuándo ir ahí |
|---|---|---|---|
| Overview / Introduction | Visión general | Qué es y para qué sirve | Para decidir si te sirve |
| Getting started | Primeros pasos | Tutorial guiado mínimo | Tu primer contacto |
| Quickstart | Inicio rápido | El ejemplo más corto que funciona | Quieres verlo andar ya |
| Prerequisites / Requirements | Requisitos previos | Versiones, cuentas, conocimientos | **Antes** de instalar |
| Installation | Instalación | Comandos `pip`, `npm`, `pacman` | Para instalar |
| Configuration | Configuración | Opciones, archivos, variables de entorno | Ajustar el comportamiento |
| Usage | Uso | Cómo se usa en casos normales | El día a día |
| Tutorial / Guide / How-to | Tutorial / guía | Paso a paso de un caso concreto | Aprender una tarea |
| Concepts / Core concepts | Conceptos | Las ideas de fondo | Entender el porqué |
| API Reference | Referencia de la API | Cada función, clase y parámetro | Buscar un detalle exacto |
| Signature | Firma | Nombre, parámetros y tipos | Saber cómo llamarla |
| Parameters / Arguments | Parámetros | Qué recibe cada uno | Al llamar la función |
| Returns / Return value | Valor de retorno | Qué devuelve y de qué tipo | Usar el resultado |
| Raises / Throws / Exceptions | Lanza / excepciones | Errores que puede provocar | Escribir `try/except` |
| Example(s) | Ejemplos | Código para copiar | Siempre: es lo más útil |
| Notes | Notas | Detalles extra | Si algo no cuadra |
| Caveats / Pitfalls / Gotchas | Advertencias / trampas | Limitaciones y errores comunes | **Antes** de usarlo en serio |
| Best practices | Buenas prácticas | Cómo usarlo bien | Código profesional |
| Changelog / Release notes | Registro de cambios | Qué cambió en cada versión | Al actualizar |
| Breaking changes | Cambios incompatibles | Lo que rompe tu código | Al subir de versión mayor |
| Deprecated | Obsoleto | Lo que se va a eliminar | Para dejar de usarlo |
| Migration guide / Upgrading | Guía de migración | Cómo pasar de la v1 a la v2 | Cambio de versión mayor |
| FAQ | Preguntas frecuentes | Dudas típicas | Tu duda seguramente está |
| Troubleshooting | Solución de problemas | Errores comunes y arreglos | Algo falla |
| Known issues | Problemas conocidos | Bugs que aún no arreglan | No es culpa tuya |
| Contributing | Cómo contribuir | Normas para enviar PRs | Open source |
| See also / Related | Véase también | Funciones relacionadas | Alternativas |
| Glossary | Glosario | Definiciones de términos | Palabras nuevas |

### 📝 Fórmulas que se repiten en las docs

| En la doc | Traducción | Qué te está diciendo |
|---|---|---|
| Returns ... | Devuelve ... | El resultado |
| Returns `None` if ... | Devuelve None si ... | Caso sin resultado (compruébalo) |
| Raises `ValueError` if ... | Lanza ValueError si ... | Prepara un `try/except` |
| Defaults to ... | Por defecto vale ... | Valor si no lo pasas |
| If omitted / If not provided, ... | Si se omite, ... | Comportamiento por defecto |
| Optional / Required | Opcional / Obligatorio | Si puedes omitirlo |
| Must be one of ... | Debe ser uno de ... | Valores permitidos (enum) |
| Accepts ... | Acepta ... | Tipos permitidos |
| Takes ... as an argument | Recibe ... como argumento | Parámetro |
| Equivalent to ... | Equivale a ... | Atajo de otra cosa |
| Alias for ... | Alias de ... | Mismo comportamiento, otro nombre |
| Shorthand for ... | Forma abreviada de ... | Atajo |
| New in version 3.8 / Added in 3.8 | Nuevo en la 3.8 | No funciona en versiones anteriores |
| Changed in version 3.10 | Cambiado en la 3.10 | Ojo si usas una versión vieja |
| Deprecated since version 3.12 | Obsoleto desde la 3.12 | Busca la alternativa |
| Removed in 4.0 | Eliminado en la 4.0 | Ya no existe |
| Experimental / Unstable / Beta | Experimental | Puede cambiar sin aviso |
| Note that ... / Note: | Ten en cuenta que ... | Detalle importante |
| Warning: / Caution: | Advertencia | Puedes perder datos o romper algo |
| See also ... | Véase también | Relacionado |
| e.g. | por ejemplo | Ejemplos, no lista completa |
| i.e. | es decir | Aclaración exacta |
| etc. | etcétera | — |
| vs. | contra, frente a | Comparación |
| Under the hood | Por dentro | Cómo funciona internamente |
| Out of the box | De serie, sin configurar | Ya viene incluido |
| In-place | En el sitio | Modifica el original (no devuelve copia) |
| Idempotent | Idempotente | Ejecutarlo varias veces = una vez |
| Thread-safe | Seguro con hilos | Se puede usar en concurrencia |
| Blocking / Non-blocking | Bloqueante / no bloqueante | ¿Espera o sigue? |
| Lazy / Eager | Perezoso / ansioso | ¿Calcula al usarlo o al crearlo? |
| Case-sensitive / insensitive | Distingue / no distingue mayúsculas | `"A" == "a"` |
| Backwards compatible | Compatible hacia atrás | No rompe código viejo |
| Opt-in / Opt-out | Hay que activarlo / viene activado | ¿Por defecto sí o no? |
| Up to / At most / At least | Hasta / como máximo / al menos | Límites |
| Arbitrary | Arbitrario, cualquiera | "an arbitrary number of arguments" |
| Respectively | Respectivamente | En el mismo orden |
| Undefined behavior | Comportamiento indefinido | Puede pasar cualquier cosa: no lo hagas |
| Implementation-defined | Depende de la implementación | Cambia según compilador o plataforma |
| TBD / WIP | Por definir / en progreso | Doc incompleta |

### ✍️ Cómo leer una firma de función

Una **firma** (signature) es el "contrato" de una función: nombre, parámetros, tipos, valores por defecto y tipo de retorno. Aprende a leerla y no necesitarás el ejemplo.

```python
open(file, mode='r', buffering=-1, encoding=None, errors=None,
     newline=None, closefd=True, opener=None)
sorted(iterable, /, *, key=None, reverse=False)
def train(model: nn.Module, epochs: int = 10, *,
          lr: float = 1e-3, **kwargs) -> dict[str, float]: ...
```

| Pieza | Ejemplo | Significa |
|---|---|---|
| Parámetro sin `=` | `file` | Obligatorio |
| Parámetro con `=` | `mode='r'` | Opcional, con valor por defecto |
| `=None` | `encoding=None` | Opcional; None suele significar "decide tú (la librería)" |
| `/` | `sorted(iterable, /, ...)` | Lo de antes solo se pasa **por posición** |
| `*` | `*, key=None` | Lo de después solo se pasa **por nombre** (keyword-only) |
| `*args` | `print(*objects)` | Cualquier número de argumentos posicionales |
| `**kwargs` | `**kwargs` | Cualquier número de argumentos con nombre |
| `: tipo` | `epochs: int` | Tipo esperado (type hint) |
| `-> tipo` | `-> dict[str, float]` | Tipo de retorno |
| `X | None` / `Optional[X]` | `str | None` | Puede ser X o None |
| `Union[A, B]` | `int | float` | Uno u otro |
| `...` | `def f(): ...` | Cuerpo omitido (en docs y stubs) |

```ts
function fetch(input: RequestInfo | URL, init?: RequestInit): Promise<Response>
array.map<U>(callbackfn: (value: T, index: number, array: T[]) => U, thisArg?: any): U[]
```

| Pieza TS | Ejemplo | Significa |
|---|---|---|
| `nombre?:` | `init?: RequestInit` | Parámetro opcional |
| `A | B` | `RequestInfo | URL` | Acepta A o B |
| `Promise<T>` | `Promise<Response>` | Devuelve una promesa: usa `await` |
| `<U>` | `map<U>` | Genérico: U lo deduce del callback |
| `(value: T) => U` | callback | Función que recibe T y devuelve U |
| `T[]` / `Array<T>` | `U[]` | Array de ese tipo |
| `readonly` | `readonly string[]` | No se puede modificar |
| `void` | `(): void` | No devuelve nada útil |
| `never` | `(): never` | Nunca termina (lanza o bucle infinito) |

| Notación MDN | Ejemplo | Significa |
|---|---|---|
| Varias líneas de sintaxis | `map(callbackFn)` y `map(callbackFn, thisArg)` | Formas válidas de llamarla |
| Parameters | `callbackFn`, `thisArg` Optional | El segundo es opcional |
| Return value | "A new array with each element being the result of the callback function." | Devuelve un array nuevo |
| Exceptions | `TypeError` | Lo que puede lanzar |
| Browser compatibility | tabla de navegadores | Si funciona en Safari, Firefox... |

💡 Consejo: en VSCode, pasa el ratón sobre una función (o Ctrl+clic) para ver su firma y su docstring sin abrir el navegador. Es la doc más rápida que existe.

### 📏 RFC 2119: MUST, SHOULD y MAY en especificaciones

Las especificaciones oficiales (RFC de la IETF, W3C, OpenAPI, protocolos) usan palabras en **MAYÚSCULAS** con un significado exacto definido en el RFC 2119 (y aclarado en el RFC 8174: solo cuentan cuando van en mayúsculas).

| Palabra clave | Sinónimos | Nivel | Significa | Ejemplo |
|---|---|---|---|---|
| MUST | REQUIRED, SHALL | 🔴 Obligatorio absoluto | Si no lo cumples, no cumples la especificación | "The client MUST send a Host header." |
| MUST NOT | SHALL NOT | ⛔ Prohibición absoluta | Nunca | "Servers MUST NOT send this header twice." |
| SHOULD | RECOMMENDED | 🟡 Recomendado | Hazlo salvo que tengas una razón seria y entiendas las consecuencias | "Clients SHOULD retry with backoff." |
| SHOULD NOT | NOT RECOMMENDED | 🟠 Desaconsejado | No lo hagas salvo razón seria | "You SHOULD NOT cache this response." |
| MAY | OPTIONAL | 🟢 Opcional | Puedes hacerlo o no; los demás deben funcionar en ambos casos | "The server MAY include a body." |

```capas
MUST : sí o sí, si no, no cumples
SHOULD : recomendado, salvo razón seria
MAY : opcional, los demás deben tolerarlo
```

⚠️ Cuidado: en una especificación, **SHOULD** no es un simple consejo: si no lo haces, otros sistemas pueden comportarse mal. Trátalo como "obligatorio salvo excepción justificada".

📌 Lectura rápida de una especificación: subraya todos los **MUST** (lo mínimo para funcionar), luego los **MUST NOT** (lo que rompe), y deja los **MAY** para el final.

## 💻 Leer --help, man, README y licencias

La ayuda de la terminal y los README son documentación **comprimida**: usan una notación de símbolos que, una vez aprendida, te deja entender cualquier comando en segundos. Y la licencia te dice si **puedes** usar el código.

### ⌨️ Notación de la ayuda de comandos

```text
Usage: cp [OPTION]... [-T] SOURCE DEST
  or:  cp [OPTION]... SOURCE... DIRECTORY
  or:  cp [OPTION]... -t DIRECTORY SOURCE...
Copy SOURCE to DEST, or multiple SOURCE(s) to DIRECTORY.

Mandatory arguments to long options are mandatory for short options too.
  -a, --archive
         same as -dR --preserve=all
      --backup[=CONTROL]
         make a backup of each existing destination file
```

| Notación | Ejemplo | Significa |
|---|---|---|
| `[algo]` | `[OPTION]` | Opcional |
| `<algo>` | `<file>` | Obligatorio, lo sustituyes tú |
| `MAYÚSCULAS` | `SOURCE DEST` | Valor que escribes tú (placeholder) |
| `...` | `SOURCE...` | Se puede repetir (uno o más) |
| `[algo]...` | `[OPTION]...` | Cero o más veces |
| `a | b` | `[-a | --all]` | Una opción u otra |
| `{a,b,c}` | `{start,stop,status}` | Elige exactamente uno |
| `-x` | `-a` | Opción corta (una letra, un guion) |
| `--palabra` | `--archive` | Opción larga (dos guiones) |
| `-x, --palabra` | `-a, --archive` | Las dos formas hacen lo mismo |
| `--opcion=VALOR` | `--backup[=CONTROL]` | La opción recibe un valor (aquí opcional) |
| `-abc` | `ls -la` | Varias opciones cortas juntas = `-l -a` |
| `--` | `rm -- -archivo` | Fin de opciones: lo que sigue son argumentos |
| `-` | `cat -` | Leer de la entrada estándar (stdin) |
| `or:` | segunda línea de Usage | Otra forma válida de usarlo |

### 📕 Secciones de una página man

| Sección | Traducción | Qué tiene |
|---|---|---|
| NAME | Nombre | Nombre y resumen de una línea |
| SYNOPSIS | Sinopsis | Formas de uso con la notación de arriba |
| DESCRIPTION | Descripción | Qué hace en detalle |
| OPTIONS | Opciones | Cada flag explicada |
| EXIT STATUS | Estado de salida | Qué significa cada código (0 = éxito) |
| ENVIRONMENT | Entorno | Variables de entorno que lee |
| FILES | Archivos | Archivos de configuración que usa |
| EXAMPLES | Ejemplos | Casos de uso (no siempre existe) |
| SEE ALSO | Véase también | Comandos relacionados |
| BUGS | Errores conocidos | Limitaciones |

| Número de sección man | Contiene | Ejemplo |
|---|---|---|
| 1 | Comandos de usuario | `man 1 ls` |
| 2 | Llamadas al sistema | `man 2 open` |
| 3 | Funciones de librería (C) | `man 3 printf` |
| 5 | Formatos de archivo | `man 5 passwd` |
| 7 | Miscelánea, conceptos | `man 7 signal` |
| 8 | Comandos de administración | `man 8 mount` |

- `comando --help` :: Ayuda corta incluida en el programa (la más rápida)
- `comando -h` :: Igual en muchas herramientas (en algunas, -h es otra cosa: `ls -h`, `df -h` = tamaños legibles)
- `man comando` :: Manual completo; `/palabra` busca, `n` siguiente, `q` sale
- `tldr comando` :: Ejemplos prácticos resumidos (instalable)
- `comando help subcomando` :: En herramientas con subcomandos: `git help commit`, `docker help run`
- `echo $?` :: Código de salida del último comando: 0 = bien, distinto de 0 = error

### 📘 Cómo leer un README en 2 minutos

| Orden | Busca | Pregunta que responde |
|---|---|---|
| 1 | Título + primera frase + badges | ¿Qué es? ¿Está mantenido? (build passing, última versión) |
| 2 | Features | ¿Hace lo que necesito? |
| 3 | Requirements / Prerequisites | ¿Funciona con mi versión de Python/Node/SO? |
| 4 | Installation | ¿Cómo lo instalo? |
| 5 | Usage / Quickstart / Example | ¿Cómo se usa en lo básico? |
| 6 | Configuration | ¿Qué puedo ajustar? |
| 7 | License | ¿Puedo usarlo en mi proyecto? |
| 8 | Issues abiertos y último commit (en GitHub) | ¿Sigue vivo? ¿Tiene muchos bugs? |

| Badge o frase | Significa |
|---|---|
| build passing / failing | Los tests de CI pasan o fallan |
| coverage 85% | El 85% del código está cubierto por tests |
| PRs welcome | Aceptan contribuciones |
| maintained / unmaintained / archived | Mantenido / abandonado / solo lectura |
| stable / beta / alpha | Estable / en pruebas / muy temprano |
| work in progress (WIP) | Incompleto |
| Star history / downloads | Popularidad |

### ⚖️ Licencias de software en una tabla

| Licencia | Tipo | Puedes usarla en software cerrado y comercial | Obligación principal | Patentes |
|---|---|---|---|---|
| MIT | Permisiva | ✅ Sí | Conservar el aviso de copyright y la licencia | No menciona |
| BSD-2 / BSD-3 | Permisiva | ✅ Sí | Conservar el aviso; BSD-3: no usar su nombre para promocionarte | No menciona |
| Apache-2.0 | Permisiva | ✅ Sí | Conservar aviso, archivo NOTICE e indicar cambios | ✅ Concede licencia de patentes |
| MPL-2.0 | Copyleft débil (por archivo) | ✅ Sí | Los archivos MPL que modifiques siguen siendo MPL y abiertos | ✅ Sí |
| LGPL-3.0 | Copyleft débil (librería) | ✅ Sí, si solo la enlazas | Cambios a la librería misma: abiertos bajo LGPL | ✅ Sí |
| GPL-3.0 | Copyleft fuerte | ⚠️ Solo si liberas tu código bajo GPL al distribuir | Si **distribuyes** un derivado, das el código fuente bajo GPL | ✅ Sí |
| AGPL-3.0 | Copyleft de red | ⚠️ Solo si liberas tu código | Como GPL, y además si usuarios lo usan **por red** (SaaS) | ✅ Sí |
| Unlicense / CC0 | Dominio público | ✅ Sí | Ninguna | No |
| Sin licencia | Todos los derechos reservados | ❌ No | No puedes copiar, modificar ni redistribuir legalmente | — |

| Palabra de licencias | Significa |
|---|---|
| permissive | Permisiva: haz casi lo que quieras, conserva el aviso |
| copyleft | Los derivados deben mantener la misma licencia libre |
| derivative work | Obra derivada (código basado en el original) |
| distribute / redistribute | Distribuir (dar copias a otros) |
| attribution | Atribución: mencionar al autor |
| warranty / "AS IS" | Garantía / "tal cual": si falla, no responden |
| liability | Responsabilidad legal |
| sublicense | Sublicenciar: dar permisos a terceros |
| notice | Aviso de copyright que hay que conservar |
| proprietary / closed source | Propietario / código cerrado |
| dual-licensed | Doble licencia: eliges una de dos |

⚠️ Cuidado: código en GitHub **sin archivo LICENSE** no es libre: por defecto todos los derechos son del autor. Copiarlo en tu proyecto, aunque sea público, no es legal.

⚠️ Cuidado: usar una librería **GPL** en una app que **distribuyes** obliga a liberar tu código bajo GPL. Usarla en tu servidor sin distribuir no (salvo que sea **AGPL**).

💡 Consejo: para tus proyectos de estudiante, **MIT** es lo más simple; **Apache-2.0** si te importan las patentes; **GPL-3.0** si quieres que todos los derivados sigan siendo libres.

📌 Nota: esta tabla es un resumen para orientarte, no asesoría legal. Ante un uso comercial importante, lee el texto completo de la licencia.

## 🎭 Falsos amigos

Palabras que se parecen al español pero significan otra cosa. Causan malentendidos graves: puedes entender **lo contrario** de lo que dice una doc ("eventually" no es "quizás") o decir algo raro en una reunión ("I'm embarrassed" no es "estoy embarazado").

### 💻 Los que más aparecen en código y docs

| Palabra | Parece | Significa realmente | Ejemplo técnico |
|---|---|---|---|
| actually | actualmente | en realidad, de hecho | "**Actually**, the bug is in the parser." |
| currently | — | actualmente | "**Currently** supports Python 3.10+." |
| eventually | eventualmente (quizás) | al final, con el tiempo | "**eventually** consistent" = consistente con el tiempo |
| library | librería (tienda) | biblioteca | "a Python **library**"; librería = bookstore |
| argument | argumento (trama) | argumento de función o discusión | "pass two **arguments**" |
| sensible | sensible | sensato, razonable | "**sensible** defaults" = valores por defecto razonables |
| sensitive | — | sensible, delicado | "**case-sensitive**", "**sensitive** data" |
| support | soportar (aguantar) | ser compatible con, dar soporte | "**supports** ARM64"; aguantar = put up with, bear |
| exit | éxito | salida | "**exit** code 1"; éxito = success |
| success | suceso | éxito | "Build **succeeded**"; suceso = event |
| resume | resumen | reanudar | "**resume** the download"; resumen = summary |
| record | recordar | registro, grabar | "a database **record**"; recordar = remember |
| realize | realizar | darse cuenta | "I **realized** the loop never ends"; realizar = perform, carry out |
| assist | asistir (ir) | ayudar | "AI coding **assistant**"; asistir a = attend |
| attend | atender | asistir a | "**attend** a lecture"; atender = serve, handle |
| notice | noticia | darse cuenta, aviso | "copyright **notice**", "I **noticed** a bug"; noticia = news |
| advice | aviso | consejo | "any **advice**?"; aviso = warning, notice |
| compromise | compromiso | comprometer (seguridad), acuerdo con concesiones | "the server was **compromised**" = fue hackeado |
| commitment | — | compromiso | "a long-term **commitment**" |
| consistent | consistente (sólido) | coherente, uniforme | "**consistent** naming"; sólido = solid, robust |
| deprecate | depreciar (bajar de valor) | marcar como obsoleto | "**deprecated** API" |
| discuss | discutir (pelear) | hablar de, debatir | "let's **discuss** the design"; pelear = argue |
| introduce | introducir (meter) | presentar, añadir por primera vez | "**introduced** in v3.0"; meter datos = enter, insert |
| application | aplicación | aplicación o solicitud | "job **application**" |
| carpet | carpeta | alfombra | carpeta = **folder**, **directory** |
| file | fila | archivo | fila = **row** |
| target | tarjeta | objetivo, destino | "build **target**"; tarjeta = card |
| lecture | lectura | clase, conferencia | "an MIT **lecture**"; lectura = reading |
| career | carrera (universitaria) | trayectoria profesional | "a **career** in AI"; carrera = degree, major |
| facility | facilidad | instalación, recurso | "logging **facility**" (syslog); facilidad = ease |
| eventual | eventual | final | "the **eventual** result" |
| fabric | fábrica | tela, tejido (o red de servicios) | fábrica = **factory** (también patrón de diseño) |
| collapse | colapsar (atasco) | plegar, contraer | "**collapse** all folders" = contraer todo |
| expand | expandir | desplegar | "**expand** the section" |
| precise | preciso (necesario) | exacto | "**precise** timing"; necesario = necessary |
| prevent | prevenir (avisar) | impedir, evitar | "**prevent** SQL injection" |
| pretend | pretender | fingir | "**pretend** the API returns 200" (mocks); pretender = intend, aim |
| assume | asumir (responsabilidad) | suponer | "**assume** the input is sorted"; asumir culpa = take responsibility |
| contest | contestar | concurso | "a coding **contest**"; contestar = answer |
| demand | demanda judicial | exigir, demanda (economía) | "on-**demand** instances" |
| evidence | evidencia (obvio) | pruebas | "**evidence** of the bug" |
| extend | extender (papel) | ampliar, heredar | "`class B extends A`" |
| intoxicated | intoxicado | borracho | intoxicado = poisoned |
| large | largo | grande | "**large** files"; largo = **long** |
| parent | pariente | padre o madre, nodo padre | "**parent** directory", "parent node" |
| relative | relativo | pariente o relativo | "**relative** path" ✅, "my relatives" = mis parientes |
| remove | remover (agitar) | quitar, eliminar | "**remove** the file" |
| sane | sano | cuerdo, razonable | "**sane** defaults", "sanity check" = comprobación básica |
| spare | esparcir | de repuesto, sobrante | "a **spare** server" |
| sympathetic | simpático | comprensivo, que se compadece | simpático = nice, friendly |
| constipated | constipado (resfriado) | estreñido | resfriado = I have a **cold** |
| embarrassed | embarazada | avergonzado | embarazada = **pregnant** |
| disgust | disgusto | asco | disgusto = upset, displeasure |
| deception | decepción | engaño | decepción = **disappointment** |
| molest | molestar | abusar sexualmente | molestar = **bother**, **annoy** |
| exciting | excitante | emocionante | "an **exciting** project" |
| fault | falta | culpa, fallo | "segmentation **fault**", "it's my **fault**" |
| comprehensive | comprensivo | completo, exhaustivo | "a **comprehensive** guide" |
| ultimately | últimamente | en última instancia, al final | últimamente = **lately**, recently |
| topic | tópico (lugar común) | tema, asunto | "off-**topic**"; tópico = cliché |
| casualty | casualidad | víctima (accidente) | casualidad = **coincidence** |
| conductor | conductor (de auto) | director de orquesta, conductor eléctrico | conductor de auto = driver |
| sensibility | sensibilidad (física) | sensibilidad artística | sensibilidad de un modelo = **sensitivity** (recall) |

### 🧪 Ejemplos de cómo te engañan

| Frase en inglés | ❌ Lo que entiendes | ✅ Lo que dice de verdad |
|---|---|---|
| "The system is eventually consistent." | El sistema es consistente a veces | El sistema **acaba** siendo consistente (tras un tiempo) |
| "Actually, it's not deprecated." | Actualmente no está obsoleto | **En realidad** no está obsoleto |
| "We support Windows." | Aguantamos Windows | **Somos compatibles** con Windows |
| "This choice is sensible." | Esta opción es delicada | Esta opción es **razonable** |
| "Your account was compromised." | Tu cuenta se comprometió | **Han hackeado** tu cuenta |
| "I realized the test was wrong." | Realicé el test mal | **Me di cuenta** de que el test estaba mal |
| "Please resume the job." | Resume el job | **Reanuda** el job |
| "Collapse all." | Colapsa todo | **Contrae** todo |
| "Assume the list is non-empty." | Asume la lista | **Supón** que la lista no está vacía |
| "We need large datasets." | Necesitamos datasets largos | Necesitamos datasets **grandes** |

⚠️ Cuidado: "**I'm actually working on it**" no es "actualmente estoy en ello", sino "**en realidad** sí estoy en ello" (suena a que te defiendes). Para "actualmente" di **currently** o **right now**.

💡 Consejo: si una palabra inglesa se parece mucho al español y la frase no tiene sentido, sospecha de falso amigo y búscala en un diccionario monolingüe (Cambridge, Merriam-Webster).

## ✅ Ejemplos resueltos: traducir de verdad

La mejor forma de aprender es descomponer textos reales. Cada ejemplo sigue el mismo método: **leer el tipo**, **traducir las palabras clave**, **entender la causa**, **decidir qué hacer**.

### ✅ Ejemplo resuelto: un traceback de Python

```text
Traceback (most recent call last):
  File "/home/yafer/ml/train.py", line 41, in <module>
    loss = criterion(model(batch), labels)
                     ^^^^^^^^^^^^
  File ".../venv/lib/python3.12/site-packages/torch/nn/modules/module.py",
    line 1736, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
  File "/home/yafer/ml/model.py", line 15, in forward
    return self.fc(x)
RuntimeError: mat1 and mat2 shapes cannot be multiplied (32x784 and 128x10)
```

| Paso | Lo que lees | Traducción y deducción |
|---|---|---|
| 1. Tipo | `RuntimeError` | Error en tiempo de ejecución (el código es válido, falló al correr) |
| 2. Mensaje | `mat1 and mat2 shapes cannot be multiplied` | "Las formas de mat1 y mat2 no se pueden multiplicar" |
| 3. Datos | `(32x784 and 128x10)` | Entra un batch de 32 filas con 784 columnas; la capa espera 128 de entrada |
| 4. Tu línea | `model.py, line 15, in forward` | La capa `self.fc` recibe un tamaño que no espera |
| 5. Línea de librería | `site-packages/torch/...` | Código de PyTorch: **ignóralo** |
| 6. Causa | 784 ≠ 128 | Imágenes 28×28 = 784 aplanadas, pero definiste `nn.Linear(128, 10)` |
| 7. Arreglo | `nn.Linear(784, 10)` | O añade capas intermedias que lleven de 784 a 128 |

🇬🇧 Cómo lo contarías en un issue: "I'm getting a shape mismatch in the final linear layer: the input is `32x784` but the layer **expects** 128 features."

### ✅ Ejemplo resuelto: un error de TypeScript

```ts
interface User { id: number; name: string; email?: string }

function sendWelcome(email: string) { /* ... */ }

const user: User = await getUser(1);
sendWelcome(user.email);
```

```text
src/welcome.ts:6:13 - error TS2345: Argument of type 'string | undefined'
  is not assignable to parameter of type 'string'.
  Type 'undefined' is not assignable to type 'string'.
```

| Fragmento | Traducción | Qué te dice |
|---|---|---|
| `src/welcome.ts:6:13` | archivo, línea 6, columna 13 | Dónde |
| `error TS2345` | código de error 2345 | Para buscarlo exacto |
| `Argument of type 'string | undefined'` | El argumento es de tipo "string o undefined" | `email?` es opcional, puede faltar |
| `is not assignable to parameter of type 'string'` | no se puede asignar a un parámetro de tipo string | La función exige un string seguro |
| `Type 'undefined' is not assignable to type 'string'.` | undefined no se puede asignar a string | El caso concreto que falla |

```ts
if (user.email) {
  sendWelcome(user.email);        // ✅ dentro del if, TypeScript sabe que es string
}
sendWelcome(user.email ?? "no-reply@example.com"); // ✅ valor por defecto
```

⚠️ Cuidado: `sendWelcome(user.email!)` también compila, pero el `!` le dice a TypeScript "confía en mí". Si el email falta, fallará en producción. Es la "solución" que muchos copian y luego lamentan.

### ✅ Ejemplo resuelto: un párrafo de la doc de React

```text
The set function only updates the state variable for the next render.
If you read the state variable after calling the set function, you will
still get the old value that was on the screen before your call.
```

| Frase en inglés | Gramática | Traducción |
|---|---|---|
| The set function only updates the state variable | Presente simple + **-s** (updates) | La función set solo actualiza la variable de estado |
| for the next render | Preposición **for** + artículo **the** | para el próximo render |
| If you read the state variable after calling the set function | Condicional 1 + **after + -ing** | Si lees la variable de estado después de llamar a set |
| you will still get the old value | Futuro **will** + **still** (todavía) | seguirás obteniendo el valor viejo |
| that was on the screen before your call | Pasado + relativo **that** | que estaba en pantalla antes de tu llamada |

```js
const [count, setCount] = useState(0);
function handleClick() {
  setCount(count + 1);
  console.log(count); // 0, no 1: el nuevo valor llega en el próximo render
}
```

📌 Lección: la doc te avisa de un error que cometen casi todos los que empiezan con React (leer el estado justo después de cambiarlo). Leer la sección **Caveats** te ahorra horas.

### ✅ Ejemplo resuelto: un párrafo de MDN

```text
The map() method of Array instances creates a new array populated with the
results of calling a provided function on every element in the calling array.
```

| Fragmento | Significa | Detalle gramatical |
|---|---|---|
| The map() method of Array instances | El método map() de las instancias de Array | **of** = de (pertenencia) |
| creates a new array | crea un array **nuevo** | Presente con -s; "new" = no modifica el original |
| populated with the results | lleno con los resultados | **populated** = participio (pasiva reducida: "which is populated") |
| of calling a provided function | de llamar a una función proporcionada | **of + -ing**; **provided** = que tú pasas |
| on every element in the calling array | sobre cada elemento del array que la llama | **calling array** = el array sobre el que llamas `.map` |

💡 Consejo: "**populated with**" (rellenado con), "**provided**" (proporcionado, que pasas tú) y "**calling**" (el que llama) son palabras que verás en cientos de páginas de MDN.

### ✅ Ejemplo resuelto: entender un --help

```text
usage: git commit [-a | --interactive | --patch] [-s] [-v] [-u[<mode>]] [--amend]
                  [--dry-run] [(-c | -C | --squash) <commit> |
                  --fixup [(amend|reword):]<commit>]
                  [-F <file> | -m <msg>] [--reset-author] [--allow-empty]
                  [--allow-empty-message] [--no-verify] [-e] [--author=<author>]
                  [--date=<date>] [--cleanup=<mode>] [--[no-]status]
                  [-i | -o] [--pathspec-from-file=<file> [--pathspec-file-nul]]
                  [(--trailer <token>[(=|:)<value>])...] [-S[<keyid>]]
                  [--] [<pathspec>...]
```

| Pieza | Lectura | Traducción |
|---|---|---|
| `[-a | --interactive | --patch]` | Opcional; elige **una** de tres | Añadir todo, modo interactivo o por trozos |
| `[-F <file> | -m <msg>]` | Opcional; o un archivo o un mensaje | El mensaje del commit, de archivo o en línea |
| `<msg>` | Valor obligatorio si usas `-m` | Lo escribes tú: `-m "fix: typo"` |
| `[-u[<mode>]]` | La opción es opcional y su valor también | `-u` o `-uno` |
| `[--[no-]status]` | Existe `--status` y `--no-status` | Patrón típico on/off |
| `(...)...` | Grupo repetible | Puedes poner varios `--trailer` |
| `[--]` | Separador opcional | Lo que sigue son rutas, no opciones |
| `[<pathspec>...]` | Cero o más rutas | Archivos que incluir |

🇬🇧 Así se lee en voz alta: "git commit, optionally with dash a **or** interactive **or** patch, then **either** a file **or** a message, **followed by** any number of paths."

### ✅ Ejemplo resuelto: un aviso de deprecación y su migración

```text
FutureWarning: The frame.append method is deprecated and will be removed from
pandas in a future version. Use pandas.concat instead.
```

| Fragmento | Tiempo / estructura | Traducción |
|---|---|---|
| FutureWarning | Tipo de aviso | Aviso de algo que cambiará en el futuro |
| The frame.append method is deprecated | Presente + participio (pasiva) | El método frame.append está obsoleto |
| and will be removed | Futuro pasivo | y será eliminado |
| from pandas in a future version | Preposiciones from / in | de pandas en una versión futura |
| Use pandas.concat instead. | Imperativo + **instead** | Usa pandas.concat en su lugar |

```python
# ❌ Antes (pandas < 2.0): funcionaba con FutureWarning
df = df.append(new_row, ignore_index=True)

# ✅ Después: lo que pide el aviso
df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
```

```text
AttributeError: 'DataFrame' object has no attribute 'append'
```

| Versión | Qué pasa | Lección |
|---|---|---|
| pandas 1.4 – 1.5 | Funciona, pero muestra el FutureWarning | El aviso es tu oportunidad de migrar tranquilo |
| pandas 2.0+ | `AttributeError`: el método ya no existe | Quien ignoró el aviso, ahora tiene el código roto |

⚠️ Cuidado: miles de tutoriales y respuestas viejas de Stack Overflow siguen usando `df.append`. Mira siempre la **fecha** de la respuesta y la **versión** de la librería que tienes (`pip show pandas`).

🇬🇧 Frase para el commit de la migración: "refactor: **replace** deprecated `DataFrame.append` **with** `pd.concat`".

## 🤖 Traductores e IA sin dejar de aprender

Un traductor o un LLM te resuelve el momento, pero si lo usas para **todo**, en un año seguirás dependiendo de él. Úsalos como **profesor**, no como muleta: primero intenta tú, luego compara.

| Hacer ✅ | Evitar ❌ | Por qué |
|---|---|---|
| Intentar traducir tú y luego comprobar | Pegar todo en el traductor sin leer | Aprendes al equivocarte |
| Traducir solo las palabras que no sabes | Traducir la página entera | Mantienes el contexto en inglés |
| Pedir "explain this error in simple English" | Pedir "tradúcemelo al español" siempre | Practicas leer explicaciones en inglés |
| Escribir tú el issue y pedir "correct my English and explain the mistakes" | Pedir "escríbeme el issue" | Aprendes de **tus** errores |
| Pedir la regla: "why is it 'depends on' and not 'depends of'?" | Aceptar la corrección sin entenderla | La regla te sirve para mil frases |
| Guardar las correcciones en tu libreta o Anki | Olvidar lo corregido | Repetición espaciada |
| Desconfiar de mensajes de error inventados | Creer que la IA conoce todos los errores | Puede inventar flags o mensajes |
| Verificar en la doc oficial lo que dice la IA | Copiar código de IA sin probarlo | Las APIs cambian; la IA puede estar desactualizada |
| Buscar el error literal en inglés | Buscar el error traducido al español | Los resultados están en inglés |
| Usar el traductor para frases sueltas difíciles | Escribir en español y traducir el PR entero | Suena poco natural y no aprendes |
| Pedir varias versiones: "make it more formal / more concise" | Quedarte con la primera | Aprendes registros distintos |
| Leer la doc en inglés con el diccionario a mano | Leer docs traducidas automáticamente | Suelen estar desactualizadas o mal traducidas |

### 🧑‍🏫 Prompts para usar la IA como profesor

| Prompt | Para qué |
|---|---|
| "Correct my English and list each mistake with a short explanation." | Corregir tus textos y aprender las reglas |
| "Explain this error message in simple English, then tell me the likely cause." | Practicar lectura con ayuda |
| "Is this sentence natural for a GitHub issue? Suggest a more natural version." | Sonar como un nativo |
| "Give me 5 example sentences using 'unless' in technical documentation." | Aprender una estructura con ejemplos |
| "What's the difference between 'fetch', 'retrieve' and 'load' in code?" | Matices entre sinónimos |
| "Quiz me on these 10 words. Don't show the answers until I reply." | Repaso activo |
| "Rewrite this commit message following Conventional Commits." | Practicar el formato |
| "Which of these variable names is clearer and why?" | Mejorar nombres |

⚠️ Cuidado: la IA puede **inventar** mensajes de error, flags de comandos o funciones que no existen ("hallucinations"). Si un comando suena raro, compruébalo con `--help` o en la doc oficial antes de ejecutarlo, sobre todo si borra algo.

💡 Consejo: una regla práctica es el **3-2-1**: lee 3 veces el error tú solo, busca 2 minutos en la doc o en Google en inglés, y solo después pregunta a la IA. Así el músculo de leer inglés trabaja.

🇬🇧 Frase modelo para pedir corrección: "Here's my draft. Please **correct** the grammar, **keep** my tone, and **explain** each change in one line."

📌 Resumen final: lee el **tipo** y la **palabra clave** del error, busca **tu** línea, consulta **Parameters / Returns / Caveats** en la doc, desconfía de los **falsos amigos** y usa la IA para **aprender**, no para dejar de pensar.
