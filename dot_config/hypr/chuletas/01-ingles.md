# 🇬🇧 Inglés
> Inglés técnico para programar: pronunciación, vocabulario, errores, docs, commits, PRs, reuniones y entrevistas.

## 🧭 Cómo estudiar inglés programando

El inglés técnico es **mucho más fácil** que el inglés general: el vocabulario es limitado (unas 1500 palabras cubren casi toda la documentación), las frases se repiten y la gramática de las docs es simple. Ya lo estás practicando cada vez que lees un error o escribes `return`. La clave es hacerlo **a propósito** y **todos los días**, aunque sea poco.

### 🔁 El método de 15 minutos al día

Mejor 15 minutos diarios que 3 horas el domingo: el cerebro aprende por repetición espaciada. Divide así tu rato:

| Minutos | Qué hacer | Ejemplo concreto |
|---|---|---|
| 0-5 | Leer algo técnico real en inglés | Un apartado de la doc de Python, un README de GitHub |
| 5-8 | Anotar 3-5 palabras nuevas con su frase | **"Defaults to `None`"** → "Por defecto vale None" |
| 8-12 | Escuchar o repetir en voz alta | Un trozo de video técnico, imitando la pronunciación (shadowing) |
| 12-15 | Escribir 2-3 frases tuyas | Un commit, un comentario o tu "standup" del día |

### 🛠️ Inmersión sin esfuerzo

- `Sistema operativo en inglés` :: Cambia el idioma del sistema, del teléfono y del navegador: aprendes menús sin darte cuenta
- `Editor/IDE en inglés` :: VSCode, Android Studio, etc. en inglés: los mensajes coinciden con lo que buscas en Google
- `Buscar SIEMPRE en inglés` :: "python read csv file" da 10 veces mejores resultados que "python leer archivo csv"
- `Copiar el error literal` :: Pega el mensaje de error tal cual en el buscador, entre comillas si es largo
- `Comentarios y commits en inglés` :: Práctica diaria de escritura sin coste extra
- `Videos con subtítulos en inglés` :: No en español: así conectas sonido con escritura
- `Hablar solo explicando tu código` :: "This function takes a list and returns..." — prepara para entrevistas
- `Anki o una libreta` :: Repite las palabras nuevas a los 1, 3, 7 y 15 días

💡 Consejo: aprende **frases completas**, no palabras sueltas. "Raises an error if..." se recuerda mejor y te sirve para leer y para escribir.

⚠️ Cuidado: no traduzcas palabra por palabra desde el español. Piensa "¿cómo lo diría un nativo en una doc?" y copia ese patrón (por ejemplo **"make sure"**, no "assure you of").

📌 Objetivo realista: en 3 meses leer docs sin traductor; en 6, escribir issues y PRs; en 12, defenderte en una entrevista técnica.

## 🗣️ Pronunciación de palabras técnicas

Muchas palabras técnicas las decimos "como se escriben" en español, y en una reunión o entrevista suena raro o no te entienden. La columna **Suena** es una aproximación para hispanohablantes: la sílaba en mayúsculas o con tilde es la fuerte. "z" = como la "z" de España (lengua entre los dientes, sonido **th**), "sh" = como pedir silencio, "y" = como en "yo" rioplatense suave (sonido **j/g** inglés).

### 🔤 Las que más se dicen mal

| English | Suena | Español | Ejemplo |
|---|---|---|---|
| queue | **kiú** | cola | `queue.put(task)` — "add it to the kiú" |
| cache | **kash** (como "cash") | caché | "clear the kash" — nunca "cachÉ" ni "cachi" |
| char | **char** o **kar** | carácter | `char c = 'a';` |
| character | **KÉ-rak-ter** | carácter | "an invalid KÉrakter" |
| width | **uídz** | ancho | `width: 100%` |
| height | **jáit** | alto | `height: 50px` — rima con "light", no "jéiyt" |
| null | **nal** | nulo | "it returns nal" |
| sudo | **SÚ-du** | superusuario hace | `sudo pacman -Syu` |
| GUI | **GÚ-i** | interfaz gráfica | "a GÚi app" |
| SQL | **és-kiu-él** o **SÍ-kuel** | SQL | "a SÍkuel query" |
| Linux | **LÍ-nux** | Linux | "I use LÍnux" (no "láinux") |
| Git | **guit** (g de "gato") | Git | "push it to guit" |
| GitHub | **GUIT-jab** | GitHub | "it's on GUITjab" |
| Python | **PÁI-zon** | Python | "I code in PÁIzon" |
| array | **a-RRÉI** | arreglo, vector | `const arr = []` |
| variable | **VÉ-ria-bol** | variable | "declare a VÉriabol" |
| function | **FÁNK-shon** | función | "call the FÁNKshon" |
| method | **MÉ-zod** | método | "a MÉzod of the class" |
| async | **ÉI-sink** | asíncrono | `async def main():` |
| await | **a-UÉIT** | esperar | `await fetch(url)` |
| debug | **di-BÁG** | depurar | "let me diBÁG this" |
| deploy | **di-PLÓI** | desplegar | "we diPLÓI on Fridays" |
| router | **RÁU-ter** (EE.UU.) / **RÚ-ter** (UK) | enrutador | "the ráuter handles the URL" |
| route | **raut** o **rut** | ruta | `@app.route("/")` |
| query | **KUÍ-ri** | consulta | "run the KUÍri" |
| string | **string** (g casi muda) | cadena de texto | "it's a string, not a number" |
| integer | **ÍN-ti-yer** | entero | `int` = "an ÍNtiyer" |
| boolean | **BÚ-lian** | booleano | `True` o `False` |
| through | **zrú** | a través de | "iterate zrú the list" |
| thread | **zred** | hilo | "spawn a new zred" |
| though | **dóu** | aunque | "it works, dóu" |
| thought | **zot** | pensé | "I zot it was fixed" |
| tuple | **TÁ-pol** o **TÚ-pol** | tupla | `(1, 2)` |
| enum | **Í-nam** | enumeración | `enum Color` |
| JSON | **YÉI-son** | JSON | "send it as YÉIson" |
| YAML | **YÁ-mel** | YAML | "edit the YÁmel file" |
| regex | **RÉ-yex** | expresión regular | "a simple RÉyex" |
| daemon | **DÍ-mon** | servicio en segundo plano | `systemd` daemon |
| schema | **SKÍ-ma** | esquema | "the database SKÍma" |
| data | **DÉI-ta** o **DÉ-ra** | datos | "load the DÉIta" |
| algorithm | **ÁL-go-ri-dzm** | algoritmo | "a sorting ÁLgoridzm" |
| parameter | **pa-RÁ-mi-ter** | parámetro | "the second paRÁmiter" |
| library | **LÁI-bre-ri** | biblioteca | "import the LÁIbreri" |
| module | **MÁ-yul** | módulo | "the os MÁyul" |
| object | **ÁB-yekt** | objeto | "an ÁByekt in memory" |
| private | **PRÁI-vet** | privado | `private int x;` |
| key | **ki** | clave, llave | "the API ki" |
| lambda | **LÁM-da** | lambda | `lambda x: x * 2` |
| Docker | **DÁ-ker** | Docker | "run it in DÁker" |
| Kubernetes | **ku-ber-NÉ-tis** | Kubernetes | "deploy to kuberNÉtis" |
| nginx | **ÉN-yin-éks** ("engine x") | nginx | "ÉNyin éks config" |
| Vue | **viú** (como "view") | Vue | "a viú component" |
| Azure | **Á-zher** | Azure | "hosted on Ázher" |
| suite | **suít** (como "sweet") | conjunto | "the test suít" |
| Wi-Fi | **uái-fái** | wifi | "the uáifái is down" |
| developer | **di-VÉ-lo-per** | desarrollador | "a backend diVÉloper" |
| science | **SÁI-ens** | ciencia | "computer SÁIens" |
| island / debris | **ÁI-land** / **de-BRÍ** | isla / escombros | letras mudas: la "s" y la "s" final no suenan |

### 🎯 Reglas rápidas de pronunciación

- `-tion` :: Suena **shon**: function = fánkshon, exception = iksépshon, iteration = iteréishon
- `-ture` :: Suena **cher**: feature = fícher, architecture = árkitekcher
- `th` :: Lengua entre los dientes: **th**read, **th**rough, ma**th**, wid**th**, leng**th**
- `-ed` :: Tras t/d suena **id** (deployed = diplóid, updated = ápdeitid); si no, solo "t" o "d" (fixed = fikst)
- `i larga vs i corta` :: "beat" (bit largo) vs "bit" (corto); ship ≠ sheep, list ≠ least
- `e final muda` :: code = koud, file = fáil, type = táip, cache = kash
- `Siglas` :: Se deletrean en inglés: API = ei-pi-ái, CLI = si-el-ái, URL = iu-ar-él, HTTP = eich-ti-ti-pi
- `s- inicial` :: Sin "e" delante: **s**tring, **s**tack, **s**cript — no "estring", "estack"

⚠️ Cuidado: el error más típico es decir "e-string", "e-script", "e-stack". La "s" va pegada: **sss-tring**.

🇬🇧 Letras en inglés para deletrear: A (ei), E (i), I (ái), G (yi), J (yei), H (eich), R (ar), W (dábol-iu), Y (uái), Z (zi en EE.UU., zed en UK).

💡 Consejo: si dudas, busca la palabra en un diccionario con audio (Cambridge, Google "how to pronounce X") o en YouGlish, que te muestra videos reales donde se dice.

## 📚 Vocabulario esencial por áreas

Estas palabras salen en cualquier curso, doc o entrevista. Apréndelas en inglés directamente: muchas veces la traducción al español suena peor y nadie la usa.

### 🔢 Tipos de datos

| English | Suena | Español | Ejemplo |
|---|---|---|---|
| integer / int | ín-ti-yer | entero | `age = 21` |
| float / double | flout / dábol | decimal (coma flotante) | `pi = 3.14` |
| string | string | cadena de texto | `name = "Yafer"` |
| boolean / bool | bú-lian | verdadero/falso | `is_ready = True` |
| null / None | nal / nan | nulo, vacío | `user = None` |
| undefined | an-di-FÁINT | no definido | `let x;` en JS |
| character / char | ké-rak-ter | carácter | `'a'` |
| byte | báit | byte (8 bits) | `b"hello"` |
| type | táip | tipo | `type(x)` |
| cast / convert | kast / kon-vért | convertir tipo | `int("42")` |

### 🧱 Estructuras de datos

| English | Suena | Español | Ejemplo |
|---|---|---|---|
| array | a-rréi | arreglo | `[1, 2, 3]` |
| list | list | lista | `nums.append(4)` |
| linked list | linkt list | lista enlazada | nodos con `next` |
| stack | stak | pila (LIFO) | `stack.pop()` |
| queue | kiú | cola (FIFO) | `queue.popleft()` |
| hash map / dictionary | jash map / DÍK-sho-ne-ri | mapa, diccionario | `{"key": "value"}` |
| set | set | conjunto (sin repetidos) | `{1, 2, 3}` |
| tree | tri | árbol | `root`, `leaf`, `child` |
| graph | graf | grafo | `nodes` y `edges` |
| heap | jip | montículo | `heapq.heappush()` |
| node | nóud | nodo | `node.left` |
| edge | edch | arista | conexión entre nodos |
| index / indices | ín-dex / ín-di-sis | índice / índices | `arr[0]` |
| key / value | ki / vá-liu | clave / valor | `dict.items()` |
| element / item | é-le-ment / ái-tem | elemento | "the first item" |
| length / size | lenz / sáiz | longitud / tamaño | `len(arr)` |

### 🔀 Control de flujo

| English | Suena | Español | Ejemplo |
|---|---|---|---|
| if / else | if / els | si / si no | `if x > 0:` |
| loop | lup | bucle | `for`, `while` |
| iterate | í-te-reit | recorrer, iterar | "iterate over the list" |
| condition | kon-dí-shon | condición | `x == 5` |
| statement | stéit-ment | sentencia, instrucción | "an if statement" |
| expression | iks-pré-shon | expresión | `a + b` |
| break / continue | breik / kon-tí-niu | salir / saltar al siguiente | `break` |
| nested | nés-tid | anidado | "a nested loop" |
| branch | branch | rama (de un if o de Git) | "the else branch" |
| exception | ik-sép-shon | excepción | `try` / `except` |
| infinite loop | ín-fi-nit lup | bucle infinito | `while True:` sin break |

### 🧩 Funciones y POO

| English | Suena | Español | Ejemplo |
|---|---|---|---|
| function | fánk-shon | función | `def add(a, b):` |
| argument | ÁR-giu-ment | argumento (valor que pasas) | `add(2, 3)` |
| parameter | pa-rá-mi-ter | parámetro (nombre en la definición) | `a`, `b` |
| return value | ri-térn vá-liu | valor de retorno | `return a + b` |
| call / invoke | kol / in-vóuk | llamar | "call the function" |
| class | klas | clase | `class User:` |
| instance | íns-tans | instancia | `u = User()` |
| attribute / property | á-tri-biut / prá-per-ti | atributo / propiedad | `u.name` |
| method | mé-zod | método | `u.save()` |
| constructor | kons-trák-ter | constructor | `__init__` |
| inheritance | in-jé-ri-tans | herencia | `class Admin(User):` |
| override | ou-ver-ráid | sobrescribir | redefinir un método |
| interface | ín-ter-feis | interfaz | contrato de métodos |
| scope | skoup | ámbito, alcance | "global scope" |
| callback | kól-bak | función que se pasa para llamarla luego | `onClick={handleClick}` |

### 🌐 Web

| English | Suena | Español | Ejemplo |
|---|---|---|---|
| request / response | ri-kuést / ris-páns | petición / respuesta | `GET /users` |
| endpoint | énd-point | punto de acceso de una API | `/api/login` |
| header | jé-der | cabecera | `Content-Type` |
| body / payload | bá-di / péi-loud | cuerpo / carga útil | el JSON enviado |
| status code | stá-tus koud | código de estado | `200`, `404` |
| server / client | sér-ver / klái-ent | servidor / cliente | backend / navegador |
| frontend / backend | frant-end / bak-end | parte visible / parte servidor | React / Django |
| browser | bráu-ser | navegador | Brave, Firefox |
| cookie / session | kú-ki / sé-shon | cookie / sesión | login persistente |
| token | tóu-ken | ficha, credencial | `Bearer <token>` |
| hosting / domain | jóus-ting / dou-méin | alojamiento / dominio | `ejemplo.com` |
| render | rén-der | dibujar, generar la vista | "the page renders" |

### 🗄️ Bases de datos

| English | Suena | Español | Ejemplo |
|---|---|---|---|
| table / row / column | téi-bol / rou / ká-lum | tabla / fila / columna | `users` |
| record | ré-kord | registro | una fila |
| primary key | prái-me-ri ki | clave primaria | `id` |
| foreign key | fó-ren ki | clave foránea | `user_id` |
| query | kuí-ri | consulta | `SELECT * FROM users` |
| join | yoin | unir tablas | `INNER JOIN` |
| index | ín-dex | índice (acelera búsquedas) | `CREATE INDEX` |
| migration | mai-gréi-shon | migración (cambio de esquema) | `alembic upgrade` |
| transaction | tran-sák-shon | transacción | `BEGIN` ... `COMMIT` |
| rollback | ról-bak | deshacer | `ROLLBACK` |
| seed | sid | datos iniciales de prueba | `seed.sql` |

### 🌿 Git

| English | Suena | Español | Ejemplo |
|---|---|---|---|
| repository / repo | ri-PÁ-si-to-ri | repositorio | `git clone` |
| commit | ko-mít | confirmar, guardar versión | `git commit -m` |
| branch | branch | rama | `git switch -c fix` |
| merge | merch | fusionar | `git merge dev` |
| pull / push | pul / push | traer / subir | `git push` |
| fetch | fech | descargar sin fusionar | `git fetch` |
| stash | stash | guardar aparte | `git stash` |
| staging area | stéi-ying é-ria | zona de preparación | `git add` |
| conflict | kán-flikt | conflicto | `<<<<<<< HEAD` |
| fork | fork | copia propia de un repo ajeno | botón Fork |
| upstream | áp-strim | repositorio original | `git pull upstream main` |
| revert | ri-vért | revertir con un commit nuevo | `git revert abc123` |

### 💻 Terminal

| English | Suena | Español | Ejemplo |
|---|---|---|---|
| shell | shel | intérprete de comandos | bash, fish, zsh |
| command | ko-mánd | comando | `ls` |
| flag / option | flag / áp-shon | opción | `-l`, `--help` |
| path | paz | ruta | `/home/yafer` |
| directory / folder | di-rék-to-ri / fóul-der | carpeta | `cd docs` |
| permission | per-mí-shon | permiso | `chmod +x` |
| environment variable | en-vái-ron-ment vé-ria-bol | variable de entorno | `$PATH` |
| pipe | páip | tubería | `ls` seguido de `grep` |
| output / input | áut-put / ín-put | salida / entrada | `stdout` |
| process | prá-ses | proceso | `ps aux` |
| package manager | pá-kech má-ne-yer | gestor de paquetes | `pacman`, `pip`, `npm` |

### 🤖 IA y Machine Learning

| English | Suena | Español | Ejemplo |
|---|---|---|---|
| dataset | déi-ta-set | conjunto de datos | MNIST |
| training | tréi-ning | entrenamiento | `model.fit()` |
| inference | ín-fe-rens | inferencia (usar el modelo) | `model.predict()` |
| weights | ueits | pesos | parámetros aprendidos |
| bias | bái-as | sesgo (término o prejuicio) | `y = wx + b` |
| loss function | los fánk-shon | función de pérdida | cross-entropy |
| overfitting | óu-ver-fi-ting | sobreajuste (memoriza) | train 99%, test 60% |
| underfitting | án-der-fi-ting | subajuste (no aprende) | malo en ambos |
| feature | fí-cher | característica, variable de entrada | edad, precio |
| label | léi-bol | etiqueta | "cat", "dog" |
| epoch | í-pok | época (una pasada por los datos) | `epochs=10` |
| batch size | bach sáiz | tamaño de lote | `batch_size=32` |
| learning rate | lér-ning reit | tasa de aprendizaje | `lr=1e-3` |
| gradient descent | gréi-di-ent di-sént | descenso de gradiente | optimizador |
| neural network | niú-ral nét-uork | red neuronal | capas y neuronas |
| layer | léi-er | capa | `nn.Linear` |
| fine-tuning | fáin tiú-ning | ajuste fino | adaptar un modelo preentrenado |
| embedding | im-bé-ding | vector que representa algo | texto → números |
| prompt | prompt | instrucción para un LLM | "Summarize this..." |
| accuracy / precision / recall | á-kiu-ra-si / pri-sí-shon / rí-kol | exactitud / precisión / exhaustividad | métricas |
| train / validation / test split | — | división entrenamiento / validación / prueba | 80/10/10 |
| hyperparameter | jái-per-pa-rá-mi-ter | hiperparámetro | lo eliges tú, no se aprende |

📌 En ML, **weights** y **parameters** suelen ser lo mismo (lo que el modelo aprende); los **hyperparameters** los fijas tú antes de entrenar.

## ⚙️ Verbos de código y documentación

Los nombres de funciones casi siempre empiezan con un **verbo en imperativo**. Si conoces estos verbos, entiendes qué hace una función solo con leer su nombre.

| Verbo | Español | Uso típico | Nombres reales |
|---|---|---|---|
| get | obtener | leer un valor (rápido, sin efectos) | `getUserById`, `get_config` |
| set | asignar, establecer | cambiar un valor | `setState`, `setTimeout` |
| fetch | traer (de fuera, por red) | pedir datos a una API | `fetchPosts`, `fetch(url)` |
| load / save | cargar / guardar | leer o escribir en disco o BD | `loadModel`, `save_checkpoint` |
| create / add | crear / añadir | nuevo elemento | `createUser`, `addItem` |
| update | actualizar | modificar existente | `updateProfile` |
| delete / remove | borrar / quitar | eliminar | `deletePost`, `removeListener` |
| handle | manejar, gestionar | responder a un evento | `handleClick`, `handleSubmit` |
| parse | analizar, interpretar | texto → estructura | `JSON.parse`, `parse_args` |
| render | renderizar, dibujar | generar la vista | `render()`, `renderTemplate` |
| return | devolver | salir de la función con un valor | `return result` |
| throw / raise | lanzar | provocar un error | `throw new Error()`, `raise ValueError` |
| catch | atrapar | capturar un error | `try { } catch (e) { }` |
| trigger | disparar | provocar un evento | `triggerBuild` |
| emit | emitir | enviar un evento | `socket.emit("msg")` |
| spawn | lanzar, generar | crear un proceso o hilo | `subprocess`, `spawnWorker` |
| deploy | desplegar | publicar en producción | `deploy.sh` |
| merge | fusionar | unir ramas o datos | `mergeConfigs` |
| validate | validar | comprobar que es correcto | `validateEmail` |
| check / verify | comprobar / verificar | revisar algo | `checkPermissions` |
| init / initialize | inicializar | preparar al empezar | `initApp`, `__init__` |
| reset / clear | reiniciar / vaciar | volver al estado inicial | `resetForm`, `clearCache` |
| build | construir, compilar | generar el producto | `npm run build` |
| run / execute | ejecutar | correr código | `runTests`, `execute_query` |
| compute / calculate | calcular | operaciones | `computeLoss` |
| convert / transform | convertir / transformar | cambiar formato | `toString`, `transformData` |
| map / filter / reduce | mapear / filtrar / reducir | operar sobre colecciones | `arr.map(fn)` |
| sort | ordenar | ordenar | `sortByDate` |
| find / search | encontrar / buscar | localizar | `findIndex`, `search_users` |
| format | formatear | presentar bonito | `formatDate` |
| log | registrar | escribir en logs | `console.log`, `logger.info` |
| subscribe / listen | suscribirse / escuchar | esperar eventos | `addEventListener` |
| mount / unmount | montar / desmontar | conectar al DOM o disco | `onMount` |
| wrap | envolver | rodear con otra cosa | `wrapper`, `withAuth` |
| toggle | alternar | on ↔ off | `toggleMenu` |
| hydrate | hidratar | dar interactividad o datos | `hydrateRoot` |
| serialize | serializar | objeto → texto o bytes | `json.dumps` |

### 🔍 Ejemplo resuelto: entender funciones por su nombre

```js
const user = await fetchUserById(42);     // trae (por red) el usuario con id 42
if (isValidEmail(user.email)) {          // ¿el email es válido? (devuelve bool)
  setCurrentUser(user);                  // asigna el usuario actual
  renderProfile(user);                   // dibuja el perfil en pantalla
}
button.addEventListener("click", handleLogout); // al hacer clic, maneja el logout
```

💡 Consejo: **get** suele ser local y barato; **fetch** implica red o espera (normalmente `async`). Si una función tarda, llámala `fetchX` o `loadX`, no `getX`.

## 🏷️ Nombrar variables y funciones en inglés

Un buen nombre explica el código sin comentarios. Reglas de oro: **funciones = verbo**, **variables = sustantivo**, **booleanos = pregunta**, **listas = plural**.

### 🐫 Convenciones de escritura

| Estilo | Ejemplo | Dónde se usa |
|---|---|---|
| camelCase | `userName`, `getUserById` | variables y funciones en JS, Java, Kotlin |
| PascalCase | `UserProfile`, `HttpClient` | clases, tipos, componentes React |
| snake_case | `user_name`, `get_user_by_id` | Python, Rust, SQL |
| SCREAMING_SNAKE_CASE | `MAX_RETRIES`, `API_KEY` | constantes |
| kebab-case | `user-profile.css`, `my-repo` | archivos, URLs, clases CSS, ramas Git |

### ✅ Booleanos: is, has, can, should

- `isLoading` :: ¿Está cargando? (estado actual)
- `hasPermission` :: ¿Tiene permiso? (posesión)
- `canEdit` :: ¿Puede editar? (capacidad)
- `shouldRetry` :: ¿Debería reintentar? (decisión)
- `wasDeleted` :: ¿Fue borrado? (pasado)
- `isEnabled / isDisabled` :: Elige uno y úsalo siempre; evita dobles negaciones como `!isNotEnabled`

### ❌ Mal vs ✅ bien

```python
# ❌ Mal: spanglish, abreviaturas raras, nombres sin significado
def calc(l):
    tot = 0
    for x in l:
        tot += x.precio
    return tot

usuarioActivo = True
lista_users = get_usuarios()
flag = False
data2 = procesarData(data)

# ✅ Bien: inglés consistente, nombres que explican
def calculate_total_price(products):
    total = 0
    for product in products:
        total += product.price
    return total

is_user_active = True
users = get_users()
has_unsaved_changes = False
cleaned_data = clean_data(raw_data)
```

```js
// ❌ Mal
const d = new Date();             // ¿d de qué?
const arr = getStuff();           // ¿qué hay dentro?
function procesar(x) { }          // ¿procesar qué?
const userList = ["Ana", "Luis"]; // "List" sobra si ya es plural

// ✅ Bien
const createdAt = new Date();
const pendingOrders = getPendingOrders();
function formatInvoice(invoice) { }
const userNames = ["Ana", "Luis"];
```

### 📏 Más reglas útiles

- `Plurales para colecciones` :: `users`, `items`, `orders`; un elemento en singular: `for user in users`
- `Unidades en el nombre` :: `timeoutMs`, `delaySeconds`, `sizeInBytes` — evita bugs de unidades
- `Sin abreviar de más` :: `button` mejor que `btn`, `message` mejor que `msg` (salvo convenciones: `i`, `id`, `url`, `db`)
- `Contadores` :: `count`, `total`, `numUsers` o `userCount`
- `Eventos` :: `onClick` (la prop que recibe) y `handleClick` (la función que lo maneja)
- `Fechas` :: `createdAt`, `updatedAt`, `expiresAt`
- `Nada de ñ ni tildes` :: `año` → `year`; nunca identificadores con caracteres no ASCII

⚠️ Cuidado: no mezcles idiomas en el mismo proyecto (`getUsuarios`, `lista_users`). Elige inglés para todo el código; los textos que ve el usuario sí pueden estar en español.

🇬🇧 Palabras para nombres: **current** (actual), **previous** (anterior), **next** (siguiente), **temp** (temporal), **default** (por defecto), **max / min**, **raw** (sin procesar), **parsed** (ya interpretado), **pending** (pendiente), **selected** (seleccionado).

## 🚨 Leer mensajes de error

Un error en inglés casi siempre tiene la forma **TipoDeError: qué pasó + dónde**. No te asustes con el texto largo: lee la **última línea** primero (el tipo y el mensaje) y luego busca la línea de **tu** archivo en el traceback.

### 🐍 Python

```text
SyntaxError: invalid syntax
```
Error de sintaxis: escribiste algo que Python no puede leer. Falta `:`, un paréntesis, una comilla, o hay un `=` donde va `==`. Mira la línea indicada y la anterior.

```text
IndentationError: expected an indented block
```
Se esperaba un bloque con sangría: después de `if`, `for`, `def` debe haber código con espacios delante. No mezcles tabs y espacios.

```text
NameError: name 'pirnt' is not defined
```
El nombre no está definido: error de tipeo, variable que no existe todavía o falta un `import`.

```text
TypeError: unsupported operand type(s) for +: 'int' and 'str'
```
Tipo incorrecto: intentas sumar un número y un texto. Convierte uno: `str(5) + "a"` o `5 + int("3")`.

```text
TypeError: greet() missing 1 required positional argument: 'name'
```
Falta un argumento obligatorio posicional: llamaste a la función con menos argumentos de los que pide.

```text
AttributeError: 'NoneType' object has no attribute 'split'
```
El objeto es `None` y no tiene ese atributo. Algo que esperabas que devolviera un valor devolvió `None` (por ejemplo una función sin `return`).

```text
IndexError: list index out of range
```
Índice fuera de rango: pediste `lista[5]` y la lista tiene menos elementos. Recuerda que empieza en 0.

```text
KeyError: 'email'
```
La clave no existe en el diccionario. Usa `d.get("email")` o revisa con `"email" in d`.

```text
ValueError: invalid literal for int() with base 10: 'abc'
```
Valor inválido: el tipo es correcto (un texto), pero el contenido no se puede convertir a entero.

```text
ModuleNotFoundError: No module named 'numpy'
```
No se encuentra el módulo: no está instalado en **este** entorno. `pip install numpy` (y revisa que el venv esté activado).

```text
FileNotFoundError: [Errno 2] No such file or directory: 'data.csv'
```
No existe el archivo en esa ruta. Revisa el directorio actual (`pwd`) y la ruta relativa.

```text
ZeroDivisionError: division by zero
```
División entre cero. Comprueba el divisor antes de dividir.

```text
RecursionError: maximum recursion depth exceeded
```
Se superó la profundidad máxima de recursión: tu función recursiva no tiene caso base o nunca llega a él.

### 🟨 JavaScript

```text
TypeError: undefined is not a function
TypeError: user.getName is not a function
```
Intentas llamar como función algo que no lo es (es `undefined` o es otra cosa). Nombre mal escrito, método que no existe o import incorrecto.

```text
TypeError: Cannot read properties of undefined (reading 'map')
```
No se pueden leer propiedades de `undefined`: haces `data.map(...)` pero `data` todavía no existe (típico en React antes de que llegue el fetch). Usa `data?.map(...)` o un valor inicial `[]`.

```text
ReferenceError: x is not defined
```
Error de referencia: la variable no existe en ese ámbito (scope).

```text
Uncaught SyntaxError: Unexpected token '}'
```
Token inesperado: sobra o falta una llave, paréntesis o coma. "Uncaught" = nadie atrapó el error.

```text
Access to fetch at 'http://api.com' from origin 'http://localhost:3000' has been blocked by CORS policy
```
Bloqueado por la política CORS: el **servidor** no permite peticiones desde tu origen. Se arregla en el backend añadiendo la cabecera `Access-Control-Allow-Origin`, no en el frontend.

### 💻 Terminal y sistema

```text
bash: nmp: command not found
```
Comando no encontrado: está mal escrito o el programa no está instalado o no está en el `PATH`.

```text
bash: ./script.sh: Permission denied
```
Permiso denegado: el archivo no es ejecutable (`chmod +x script.sh`) o necesitas permisos de administrador (`sudo`).

```text
Segmentation fault (core dumped)
```
Fallo de segmentación: el programa accedió a memoria que no le pertenece (típico en C/C++: puntero nulo, array fuera de límites). "Core dumped" = guardó una imagen de la memoria para depurar.

```text
Error: listen EADDRINUSE: address already in use :::3000
```
La dirección ya está en uso: otro proceso ocupa el puerto 3000. Ciérralo o usa otro puerto.

```text
Killed
```
Matado: normalmente el sistema se quedó sin memoria (OOM, Out Of Memory) y terminó tu proceso. Común al entrenar modelos grandes.

### 🌐 HTTP

| Código | Nombre en inglés | Significa | Qué hacer |
|---|---|---|---|
| 200 | OK | Todo bien | Nada |
| 201 | Created | Recurso creado | Nada |
| 301 / 302 | Moved Permanently / Found | Redirección | Sigue la nueva URL |
| 400 | Bad Request | Petición mal formada | Revisa el JSON o los parámetros |
| 401 | Unauthorized | No autenticado | Falta o caducó el token, inicia sesión |
| 403 | Forbidden | Prohibido (sí te conoce, pero no tienes permiso) | Revisa roles y permisos |
| 404 | Not Found | No existe | Revisa la URL o la ruta |
| 405 | Method Not Allowed | Método no permitido | Usaste GET donde va POST |
| 409 | Conflict | Conflicto (p. ej. ya existe) | Revisa duplicados |
| 422 | Unprocessable Entity | Datos con formato bien pero inválidos | Revisa la validación |
| 429 | Too Many Requests | Demasiadas peticiones | Espera, hay límite (rate limit) |
| 500 | Internal Server Error | Error interno del servidor | Mira los logs del backend |
| 502 | Bad Gateway | El proxy recibió mala respuesta | El backend está caído |
| 503 | Service Unavailable | Servicio no disponible | Sobrecarga o mantenimiento |
| 504 | Gateway Timeout | Se agotó el tiempo de espera | El backend tarda demasiado |

### 🌿 Git

```text
CONFLICT (content): Merge conflict in app.py
Automatic merge failed; fix conflicts and then commit the result.
```
Conflicto de fusión: dos ramas cambiaron las mismas líneas. Abre el archivo, elige entre `<<<<<<<`, `=======` y `>>>>>>>`, guarda, `git add` y `git commit`.

```text
You are in 'detached HEAD' state.
```
Estado "HEAD separado": estás en un commit concreto, no en una rama. Si haces commits aquí se pueden perder; crea una rama con `git switch -c nueva-rama`.

```text
! [rejected] main -> main (fetch first)
error: failed to push some refs
```
Push rechazado: el remoto tiene commits que tú no tienes. Haz `git pull` (o `git pull --rebase`) y luego `git push`.

```text
fatal: not a git repository (or any of the parent directories): .git
```
No es un repositorio Git: estás en la carpeta equivocada o falta `git init`.

### ✅ Ejemplo resuelto: traducir un traceback paso a paso

```text
Traceback (most recent call last):
  File "/home/yafer/app/main.py", line 12, in <module>
    total = sum_prices(cart)
  File "/home/yafer/app/utils.py", line 4, in sum_prices
    return sum(item["price"] for item in items)
  File "/home/yafer/app/utils.py", line 4, in <genexpr>
    return sum(item["price"] for item in items)
TypeError: string indices must be integers, not 'str'
```

1. **Traceback (most recent call last)** = "rastro de llamadas (la más reciente al final)". Lo importante está abajo.
2. **Última línea**: `TypeError: string indices must be integers` = "los índices de un string deben ser enteros". Es decir, hiciste `algo["price"]` y `algo` es un **string**, no un diccionario.
3. **Tu línea**: `utils.py`, línea 4. `item` debería ser un diccionario, pero es texto.
4. **Causa probable**: `cart` es una lista de strings (`["pan", "leche"]`) o es un JSON sin parsear. Solución: `json.loads(...)` o revisar cómo construyes `cart`.

💡 Consejo: para buscar en Google, copia **solo** la última línea sin tus nombres propios: `TypeError: string indices must be integers python`.

🇬🇧 Palabras de errores: **expected** (se esperaba), **unexpected** (inesperado), **missing** (falta), **invalid** (inválido), **unsupported** (no soportado), **out of range** (fuera de rango), **not found** (no encontrado), **denied** (denegado), **failed** (falló), **timeout** (tiempo agotado), **deprecated** (obsoleto).

## 📖 Leer documentación

Las docs usan siempre las mismas fórmulas. Si las reconoces, lees el doble de rápido.

| En la doc | Traducción | Comentario |
|---|---|---|
| Returns ... | Devuelve ... | Qué sale de la función |
| Raises / Throws ... | Lanza ... | Qué error puede provocar |
| Defaults to ... | Por defecto vale ... | Valor si no lo pasas |
| Optional | Opcional | Puedes omitirlo |
| Required | Obligatorio | Si falta, error |
| Deprecated | Obsoleto | Aún funciona pero se eliminará; no lo uses |
| Since version 3.8 | Desde la versión 3.8 | Disponible a partir de ahí |
| e.g. | por ejemplo | Del latín "exempli gratia" |
| i.e. | es decir | Del latín "id est" |
| Note that ... | Ten en cuenta que ... | Detalle importante |
| See also ... | Véase también ... | Funciones relacionadas |
| If omitted, ... | Si se omite, ... | Comportamiento por defecto |
| If not provided, ... | Si no se proporciona, ... | Igual que el anterior |
| Accepts ... | Acepta ... | Tipos permitidos |
| Takes ... as an argument | Recibe ... como argumento | Parámetros |
| Must be ... | Debe ser ... | Restricción obligatoria |
| Should be ... | Debería ser ... | Recomendación fuerte |
| May / might ... | Puede (que) ... | Posibilidad |
| Out of the box | Listo para usar, sin configurar | Viene incluido |
| Under the hood | Por dentro, internamente | Cómo funciona realmente |
| Thread-safe | Seguro con varios hilos | Se puede usar en concurrencia |
| In-place | En el sitio (modifica el original) | `list.sort()` vs `sorted()` |
| Backwards compatible | Compatible con versiones anteriores | No rompe código viejo |
| Breaking change | Cambio que rompe compatibilidad | Hay que adaptar tu código |
| Caveat | Advertencia, salvedad | Limitación a tener en cuenta |
| Prerequisites | Requisitos previos | Instala esto antes |
| Getting started | Primeros pasos | Tutorial inicial |
| Quickstart | Inicio rápido | Ejemplo mínimo |
| Troubleshooting | Solución de problemas | Errores comunes |
| Changelog / Release notes | Registro de cambios / Notas de versión | Qué cambió en cada versión |
| TBD | Por definir | "To Be Determined" |
| Under construction | En construcción | Doc incompleta |

### ✅ Ejemplo resuelto: leer una firma de función

```text
sorted(iterable, /, *, key=None, reverse=False)

Return a new sorted list from the items in iterable.
Has two optional arguments which must be specified as keyword arguments.
key specifies a function of one argument that is used to extract a
comparison key from each element in iterable (for example, key=str.lower).
The default value is None (compare the elements directly).
reverse is a boolean value. If set to True, then the list elements are
sorted as if each comparison were reversed.
```

Traducción guiada: **"Return a new sorted list"** = devuelve una lista **nueva** ordenada (no modifica la original). **"Two optional arguments which must be specified as keyword arguments"** = dos argumentos opcionales que hay que pasar **por nombre** (`key=...`, no por posición). **"The default value is None"** = por defecto vale None. **"If set to True"** = si se pone a True.

```python
sorted(["b", "A", "c"], key=str.lower, reverse=True)  # ['c', 'b', 'A']
```

⚠️ Cuidado: "**eventually**" en una doc no es "eventualmente" (quizás); significa "**al final**, tarde o temprano". "Eventually consistent" = se vuelve consistente con el tiempo.

## 📝 Mensajes de commit

Los commits se escriben en **imperativo** y en presente, como una orden: "**Add** login page", no "Added" ni "Adding". Truco: la frase debe completar **"If applied, this commit will ___"**.

### 📐 Conventional Commits

```text
<tipo>(<ámbito opcional>): <descripción corta en imperativo>

<cuerpo opcional: qué y por qué, no cómo>

<pie opcional: BREAKING CHANGE, Closes #123>
```

| Tipo | Cuándo | Ejemplo |
|---|---|---|
| feat | Nueva funcionalidad | `feat: add dark mode toggle` |
| fix | Corrección de bug | `fix: prevent crash on empty input` |
| docs | Solo documentación | `docs: update installation steps` |
| style | Formato, espacios (sin cambiar lógica) | `style: format with black` |
| refactor | Reestructurar sin cambiar comportamiento | `refactor: extract auth logic into service` |
| perf | Mejora de rendimiento | `perf: cache user queries` |
| test | Añadir o corregir tests | `test: add unit tests for parser` |
| build | Sistema de build, dependencias | `build: bump numpy to 2.1` |
| ci | Integración continua | `ci: run tests on pull requests` |
| chore | Tareas de mantenimiento | `chore: remove unused files` |
| revert | Deshacer un commit | `revert: undo "feat: add dark mode"` |

### ✅ 20 ejemplos buenos

```text
feat(auth): add Google sign-in
feat: allow users to export notes as PDF
feat(api): add pagination to /users endpoint
fix: handle null response from weather API
fix(ui): align buttons on mobile screens
fix: correct off-by-one error in pagination
fix(db): close connection after each request
docs: add usage examples to README
docs: fix typos in contributing guide
refactor: rename getData to fetchUserProfile
refactor(model): split training loop into smaller functions
perf: reduce image size with lazy loading
test: cover edge cases for date parser
build: upgrade React to 19
ci: cache pip dependencies in GitHub Actions
chore: update .gitignore for venv
style: apply prettier to src folder
feat(ml): add early stopping to training script
fix(ml): normalize images before inference
feat!: drop support for Python 3.8
```

- `Primera línea ≤ 50-72 caracteres` :: Corta y clara; el detalle va en el cuerpo
- `Sin punto final` :: `fix: handle empty list` (no `handle empty list.`)
- `Minúscula tras los dos puntos` :: Convención habitual en Conventional Commits
- `! o BREAKING CHANGE` :: Marca un cambio que rompe compatibilidad
- `Closes #12` :: En el pie: cierra el issue 12 al fusionar

⚠️ Cuidado: evita commits como `fix`, `cambios`, `asdf`, `update stuff` o `final final v2`. Nadie (ni tú en un mes) sabrá qué hiciste.

🇬🇧 Verbos de commit: **add, remove, fix, update, rename, move, refactor, improve, handle, prevent, allow, support, drop, bump, revert, clean up, simplify**.

## 🐙 Issues, pull requests y preguntas

Pedir ayuda bien escrita en inglés multiplica las respuestas. Fórmula: **contexto → qué esperabas → qué pasó → qué probaste → código mínimo**.

### 🐛 Plantilla de issue (reporte de bug)

```text
Title: Crash when uploading files larger than 10 MB

**Description**
When I upload a file larger than 10 MB, the app crashes with a 500 error.

**Steps to reproduce**
1. Go to /upload
2. Select a file of 15 MB
3. Click "Upload"

**Expected behavior**
The file should be uploaded, or a clear error message should be shown.

**Actual behavior**
The server returns "500 Internal Server Error" and the page goes blank.

**Environment**
- OS: Arch Linux (CachyOS)
- Browser: Brave 1.70
- Version: v2.3.1

**Logs**
(paste the error here)

**Additional context**
It works fine with files smaller than 5 MB.
```

### ✅ Ejemplo resuelto: un pull request completo

```text
Title: feat: add dark mode toggle to settings page

## Summary
This PR adds a dark mode toggle to the settings page.
The selected theme is saved in localStorage, so it persists between sessions.

## Changes
- Add `ThemeToggle` component
- Add `useTheme` hook to read and save the theme
- Update CSS variables for dark colors
- Add unit tests for `useTheme`

## Why
Several users requested a dark theme (see #42).

## How to test
1. Run `npm install` and `npm run dev`
2. Go to Settings
3. Click the toggle and reload the page: the theme should stay the same

## Screenshots
(before / after)

## Notes
I wasn't sure about the color of the links in dark mode.
Feedback is welcome!

Closes #42
```

### ❓ Preguntar en Stack Overflow o GitHub Discussions

```text
Title: FastAPI returns 422 when sending JSON from fetch()

I'm building a small API with FastAPI and a React frontend.
When I send a POST request with fetch(), I get a 422 Unprocessable Entity error.

What I expected: the user to be created and a 201 response.
What happens: 422 with the message "field required".

Here is a minimal example:

    (backend code)
    (frontend code)

What I've tried:
- Checking the Content-Type header (it's application/json)
- Sending the same request with curl (it works!)

Am I missing something in the request body?
Any help would be appreciated. Thanks in advance!
```

### 💬 Frases para reviews y comentarios

| Frase | Traducción | Cuándo |
|---|---|---|
| Could you take a look at this PR? | ¿Puedes revisar este PR? | Pedir revisión |
| I've addressed your comments. | He atendido tus comentarios. | Tras corregir |
| Nice catch! | ¡Bien visto! | Te encontraron un bug |
| What do you think about ...? | ¿Qué te parece ...? | Proponer algo |
| Nit: ... | Detalle menor: ... | Sugerencia pequeña, no bloqueante |
| Would it make sense to ...? | ¿Tendría sentido ...? | Sugerir con tacto |
| I'm not sure I understand this part. | No estoy seguro de entender esta parte. | Pedir aclaración |
| Good point, I'll change it. | Buen punto, lo cambio. | Aceptar sugerencia |
| I'd prefer to keep it because ... | Prefiero mantenerlo porque ... | Discrepar con respeto |
| Is this still relevant? | ¿Esto sigue siendo relevante? | Issue antiguo |
| Any updates on this? | ¿Alguna novedad sobre esto? | Preguntar avance |

💡 Consejo: en open source, sé breve y concreto; agradece siempre ("Thanks for the review!"). Un ejemplo mínimo reproducible (**minimal reproducible example**) vale más que mil palabras.

⚠️ Cuidado: no escribas "Please help me urgent!!!" ni todo en mayúsculas. Suena exigente y recibe menos ayuda. Mejor: "Any help would be appreciated."

## 👥 Comunicación en equipo y reuniones

### ☀️ Daily standup

Responde siempre a tres preguntas: qué hiciste ayer, qué harás hoy, qué te bloquea.

```text
Yesterday I worked on the login page and fixed the validation bug.
Today I'm going to write tests for the auth service.
I'm blocked by the API keys. I'm waiting for access from DevOps.
```

```text
Yesterday I finished the data preprocessing script.
Today I'll start training the baseline model.
No blockers for now.
```

| Frase | Traducción |
|---|---|
| I'm working on ... | Estoy trabajando en ... |
| I'm almost done with ... | Casi termino ... |
| I'm blocked by ... / I'm stuck on ... | Estoy bloqueado por ... / Estoy atascado con ... |
| I'm waiting for ... | Estoy esperando ... |
| It's taking longer than expected. | Está tardando más de lo esperado. |
| I'll have it ready by Friday. | Lo tendré listo para el viernes. |
| No blockers. | Sin bloqueos. |

### 🙋 Pedir ayuda y aclarar

| Frase | Traducción |
|---|---|
| Do you have a minute? | ¿Tienes un minuto? |
| Could you help me with ...? | ¿Me podrías ayudar con ...? |
| Can you walk me through it? | ¿Me lo explicas paso a paso? |
| Sorry, could you repeat that? | Perdón, ¿lo puedes repetir? |
| Could you speak a bit slower, please? | ¿Podrías hablar un poco más despacio? |
| Just to make sure I understand: ... | Para asegurarme de que entiendo: ... |
| What do you mean by ...? | ¿Qué quieres decir con ...? |
| Can you share your screen? | ¿Puedes compartir pantalla? |
| I'll look into it. | Lo investigo. |
| Let me get back to you on that. | Te respondo sobre eso luego. |

### 🗨️ Dar opiniones y discrepar

| Frase | Traducción |
|---|---|
| I think we should ... | Creo que deberíamos ... |
| In my opinion, ... | En mi opinión, ... |
| I agree. / I totally agree. | Estoy de acuerdo. / Totalmente. |
| I see your point, but ... | Entiendo tu punto, pero ... |
| What if we ...? | ¿Y si ...? |
| Have we considered ...? | ¿Hemos considerado ...? |
| That makes sense. | Tiene sentido. |
| I'm not sure that's the best approach. | No sé si es el mejor enfoque. |
| Let's take this offline. | Hablemos de esto aparte (después de la reunión). |
| Let's circle back to this later. | Volvamos a esto más tarde. |

🇬🇧 Muletillas para ganar tiempo al hablar: **"Let me think..."**, **"That's a good question."**, **"How can I put it..."**, **"What I mean is..."** — mucho mejor que quedarse callado o decir "eeeh".

⚠️ Cuidado: "**I have a doubt**" suena raro (en inglés "doubt" es desconfiar). Di "**I have a question**".

## 🎤 Entrevistas técnicas en inglés

### 🙂 "Tell me about yourself": respuesta modelo para estudiante

Estructura: **presente → pasado → futuro** (quién eres hoy, qué has hecho, qué buscas). Máximo 1-2 minutos.

```text
Hi, I'm Yafer. I'm a Computer Science student from Bolivia,
and I'm especially interested in artificial intelligence and backend development.

During my studies I've built several projects. For example, I built a tool
that automatically captures and transcribes my online classes using Whisper,
and I've worked with Python, JavaScript, SQL and Linux every day.

I also like automating my workflow, so I customize my Linux environment
and write scripts to save time.

Right now I'm looking for an internship where I can learn from experienced
engineers and contribute to real AI or backend projects.
```

### 🧠 Pensar en voz alta (think out loud)

En una entrevista técnica valoran **cómo piensas**, no solo el resultado. Narra lo que haces:

| Momento | Frase |
|---|---|
| Entender el problema | "Let me make sure I understand the problem." |
| Preguntar restricciones | "Can I assume the input is always sorted?" / "What should happen if the list is empty?" |
| Ejemplo | "Let me try a small example first." |
| Primera idea | "My first idea is a brute-force approach, which would be O(n²)." |
| Mejorar | "We could improve this by using a hash map to store the values we've seen." |
| Escribiendo | "Now I'm going to iterate through the array..." |
| Duda | "I'm not 100% sure about this part, but I think..." |
| Probar | "Let me walk through the code with this example." |
| Complejidad | "The time complexity is O(n) and the space complexity is O(n)." |
| Caso borde | "One edge case is when the input is empty." |
| No sabes | "I haven't used that before, but I would approach it like this..." |

### ✅ Ejemplo resuelto: explicar tu código en voz alta

```python
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
```

🇬🇧 "I create a dictionary called seen to store each number and its index. Then I iterate through the list. For each number, I compute the complement, which is the target minus the current number. If the complement is already in the dictionary, I return both indices. Otherwise, I store the current number. This runs in O(n) time because dictionary lookups are O(1) on average."

📌 Cómo se leen: O(n) = "**O of n**" (ou ov en), O(n²) = "**O of n squared**", O(log n) = "**O of log n**", O(1) = "**constant time**".

### ❓ Preguntas típicas de entrevista

| Pregunta | Qué buscan |
|---|---|
| Why do you want to work here? | Que conozcas la empresa |
| What's your biggest strength / weakness? | Autoconocimiento honesto |
| Tell me about a challenging project. | Problema, acción, resultado (método STAR) |
| Tell me about a time you made a mistake. | Que aprendes de los errores |
| Where do you see yourself in five years? | Ambición realista |
| Do you have any questions for us? | Interés real: ten 2 preguntas preparadas |

🇬🇧 Preguntas para hacer tú: "What does a typical day look like for this role?", "What technologies does the team use?", "How do you support junior developers?"

💡 Consejo: prepara y **graba** tus respuestas en voz alta. Escúchalas: notarás pausas y pronunciaciones a corregir.

## 🎭 Falsos amigos

Palabras que parecen españolas pero significan otra cosa. Son la fuente número uno de malentendidos.

| English | Parece | Significa realmente | Ejemplo |
|---|---|---|---|
| actually | actualmente | en realidad, de hecho | "Actually, it's a bug." |
| currently | — | actualmente | "I'm currently studying." |
| library | librería | biblioteca (de código o de libros) | "a Python library" |
| bookstore | — | librería (tienda) | — |
| eventually | eventualmente | al final, con el tiempo | "It will eventually fail." |
| argument | argumento (de película) | argumento (de función) o discusión | "pass two arguments" / "we had an argument" |
| assist | asistir (ir a) | ayudar | "Can I assist you?" |
| attend | atender | asistir (a clase o reunión) | "I attended the meeting." |
| realize | realizar | darse cuenta | "I realized the bug was in the loop." |
| sensible | sensible | sensato, razonable | "a sensible default" |
| sensitive | — | sensible (delicado) | "case-sensitive", "sensitive data" |
| support | soportar (aguantar) | dar soporte, ser compatible con, apoyar | "supports Python 3.12" |
| exit | éxito | salida | "exit code 1" |
| success | — | éxito | "build succeeded" |
| record | recordar | grabar, registro | "record a video", "a database record" |
| remember | — | recordar | "remember me" |
| carpet | carpeta | alfombra | usa **folder** para carpeta |
| file | fila | archivo | usa **row** para fila |
| advice | aviso | consejo | "any advice?" |
| notice / warning | — | aviso | "deprecation warning" |
| commodity | comodidad | mercancía básica | usa **comfort** o **convenience** |
| application | aplicación | aplicación o solicitud (de empleo) | "job application" |
| introduce | introducir (meter) | presentar (a alguien) o lanzar | "introduced in v3.0" |
| enter / insert | — | introducir datos | "enter your password" |
| compromise | compromiso | acuerdo con concesiones, comprometer (seguridad) | "the server was compromised" |
| commitment | — | compromiso | — |
| consistent | consistente (sólido) | coherente, uniforme | "consistent naming" |
| deprecate | depreciar | marcar como obsoleto | "this API is deprecated" |
| discuss | discutir (pelear) | hablar de, debatir | "let's discuss the design" |
| embarrassed | embarazada | avergonzado | pregnant = embarazada |
| fabric | fábrica | tela | usa **factory** (también un patrón de diseño) |
| lecture | lectura | clase magistral, conferencia | reading = lectura |
| resume | resumen | reanudar / currículum (résumé) | "resume download" |
| summary | — | resumen | "TL;DR summary" |
| target | tarjeta | objetivo, destino | "build target" |
| card | — | tarjeta | "credit card" |

⚠️ Cuidado: "**I'm actually working on it**" no es "actualmente estoy en ello" sino "**en realidad** sí estoy en ello". Para "actualmente" usa **currently** o **right now**.

## ✏️ Gramática mínima para docs y código

No necesitas toda la gramática: con estas cinco estructuras entiendes el 90% de la documentación.

### 1️⃣ Presente simple (descripciones de la doc)

La doc describe lo que la función **hace siempre**, en tercera persona con **-s**.

```text
This function returns a list.
The method takes two arguments.
It raises a ValueError if the input is empty.
```

⚠️ Cuidado: no olvides la **-s** en tercera persona: "it return**s**", "the function take**s**". Es el error más común de hispanohablantes.

### 2️⃣ Imperativo (commits, instrucciones, tutoriales)

Verbo sin sujeto: es una orden o un paso.

```text
Install the package with pip.
Run the following command.
Make sure Docker is running.
Add login validation.
```

### 3️⃣ Voz pasiva (muy común en docs)

Se usa cuando importa **qué** pasa, no **quién** lo hace: **is/are + participio** (called, returned, used...).

| Pasiva | Traducción | Activa equivalente |
|---|---|---|
| The function is called when ... | La función se llama cuando ... | The system calls the function when ... |
| A new list is returned. | Se devuelve una lista nueva. | It returns a new list. |
| This value is ignored. | Este valor se ignora. | — |
| The file is created automatically. | El archivo se crea automáticamente. | — |
| It was deprecated in version 2.0. | Se marcó como obsoleto en la 2.0. | — |
| Errors are logged to stderr. | Los errores se registran en stderr. | — |

💡 Consejo: cuando en español dirías "**se** + verbo" (se llama, se devuelve, se crea), en inglés casi siempre es pasiva: **is called, is returned, is created**.

### 4️⃣ Modales: qué tan obligatorio es

| Modal | Fuerza | Ejemplo | Traducción |
|---|---|---|---|
| must | Obligatorio | "The key must be a string." | Debe ser un string. |
| must not | Prohibido | "You must not share your token." | No debes compartir tu token. |
| should | Recomendado | "You should use a virtual environment." | Deberías usar un entorno virtual. |
| may | Permitido o posible | "This may take a few minutes." | Esto puede tardar unos minutos. |
| can | Capacidad | "You can pass a list." | Puedes pasar una lista. |
| might | Posibilidad baja | "It might not work on Windows." | Puede que no funcione en Windows. |
| will | Futuro, seguro | "This will delete all files." | Esto borrará todos los archivos. |
| don't need to | No hace falta | "You don't need to restart." | No hace falta reiniciar. |

📌 En especificaciones oficiales (RFC), **MUST**, **SHOULD** y **MAY** en mayúsculas tienen significado exacto: obligatorio, recomendado y opcional.

### 5️⃣ Condicionales y conectores

| Inglés | Español | Ejemplo |
|---|---|---|
| if / unless | si / a menos que | "unless specified" = salvo que se indique |
| otherwise | si no, de lo contrario | "Otherwise, returns None." |
| whether | si (entre dos opciones) | "whether to include headers" |
| however | sin embargo | "However, this is slower." |
| therefore | por lo tanto | — |
| instead | en su lugar | "Use `pathlib` instead." |
| rather than | en vez de | "rather than a list" |
| as long as | siempre que | "as long as it's valid" |
| such as | como (ejemplos) | "such as JSON or YAML" |
| whereas | mientras que (contraste) | "`list` is mutable, whereas `tuple` is not" |
| respectively | respectivamente | "x and y, respectively" |

## 🔠 Abreviaturas y jerga

### 💬 En chats, PRs e issues

- `LGTM` :: Looks Good To Me — "me parece bien", aprobación de un PR
- `WIP` :: Work In Progress — trabajo en curso, aún no revisar
- `PR / MR` :: Pull Request / Merge Request — solicitud para fusionar cambios
- `TL;DR` :: Too Long; Didn't Read — resumen corto
- `AFAIK` :: As Far As I Know — que yo sepa
- `IMO / IMHO` :: In My (Humble) Opinion — en mi (humilde) opinión
- `IIRC` :: If I Recall Correctly — si mal no recuerdo
- `FYI` :: For Your Information — para tu información
- `RTFM` :: Read The F... Manual — lee el manual (algo grosero)
- `ETA` :: Estimated Time of Arrival — cuándo estará listo
- `ASAP` :: As Soon As Possible — lo antes posible
- `PTAL` :: Please Take A Look — por favor revisa
- `nit` :: Nitpick — detalle menor, no bloqueante
- `TBD / TBA` :: To Be Determined / Announced — por definir / anunciar
- `OOO` :: Out Of Office — fuera de la oficina
- `EOD` :: End Of Day — al final del día
- `ACK` :: Acknowledged — recibido, entendido
- `+1` :: Estoy de acuerdo, a mí también me pasa
- `repro` :: Reproduction — ejemplo que reproduce el bug
- `TIL` :: Today I Learned — hoy aprendí

### 🧰 Siglas técnicas

| Sigla | Significa | Español |
|---|---|---|
| API | Application Programming Interface | Interfaz de programación de aplicaciones |
| SDK | Software Development Kit | Kit de desarrollo |
| CLI | Command-Line Interface | Interfaz de línea de comandos |
| GUI | Graphical User Interface | Interfaz gráfica |
| IDE | Integrated Development Environment | Entorno de desarrollo integrado |
| CRUD | Create, Read, Update, Delete | Crear, leer, actualizar, borrar |
| REST | Representational State Transfer | Estilo de API web |
| ORM | Object-Relational Mapping | Mapeo objeto-relacional |
| CI/CD | Continuous Integration / Delivery | Integración y entrega continuas |
| OOP | Object-Oriented Programming | Programación orientada a objetos |
| MVP | Minimum Viable Product | Producto mínimo viable |
| PoC | Proof of Concept | Prueba de concepto |
| UX / UI | User Experience / User Interface | Experiencia / interfaz de usuario |
| LLM | Large Language Model | Modelo de lenguaje grande |
| RAG | Retrieval-Augmented Generation | Generación aumentada con recuperación |
| GPU / CPU | Graphics / Central Processing Unit | Tarjeta gráfica / procesador |
| OS | Operating System | Sistema operativo |
| QA | Quality Assurance | Control de calidad |
| SaaS | Software as a Service | Software como servicio |

### 🧘 Principios con nombre propio

| Principio | Significa | Idea |
|---|---|---|
| DRY | Don't Repeat Yourself | No repitas código: extrae funciones |
| KISS | Keep It Simple, Stupid | Mantenlo simple |
| YAGNI | You Aren't Gonna Need It | No programes lo que aún no necesitas |
| SOLID | Cinco principios de diseño POO | Responsabilidad única, abierto/cerrado, etc. |
| SoC | Separation of Concerns | Separa responsabilidades |

### 🗯️ Jerga hablada

| Jerga | Significa |
|---|---|
| It works on my machine | Funciona en mi PC (y en otro no) |
| Rubber duck debugging | Explicarle el código a un patito para encontrar el bug |
| Bikeshedding | Discutir detalles triviales |
| Spaghetti code | Código enredado |
| Boilerplate | Código repetitivo de plantilla |
| Tech debt | Deuda técnica (atajos que habrá que arreglar) |
| Edge case / corner case | Caso límite o raro |
| Happy path | El caso normal, sin errores |
| Hotfix | Arreglo urgente en producción |
| Ship it | Publícalo, sácalo |
| Footgun | Algo fácil de usar mal y dispararse en el pie |
| Yak shaving | Cadena de tareas tontas antes de la real |

## 🗓️ Plan de práctica de 30 días

Un plan de **15-20 minutos al día**. Marca cada día cumplido; si fallas uno, sigue al día siguiente sin culpa.

| Semana | Foco | Tareas diarias |
|---|---|---|
| 1 | Leer y pronunciar | Cambia el sistema a inglés. Lee 1 página de docs. Repite en voz alta 10 palabras de la tabla de pronunciación. |
| 2 | Vocabulario y errores | Aprende 10 palabras de una tabla de vocabulario. Cada error que tengas, tradúcelo y escríbelo en tu libreta. |
| 3 | Escribir | Todos tus commits en Conventional Commits. Escribe 1 issue o pregunta de práctica. Comenta tu código en inglés. |
| 4 | Hablar | Graba tu standup diario (1 min). Practica "Tell me about yourself". Explica en voz alta una función tuya. |

### 📅 Detalle día a día

- `Día 1` :: Cambia sistema, navegador y editor a inglés
- `Día 2-3` :: Pronunciación: repite toda la tabla de palabras mal dichas, grábate
- `Día 4-5` :: Lee el README de un repo que uses (por ejemplo requests o FastAPI) y anota 10 palabras
- `Día 6-7` :: Vocabulario de estructuras de datos y control de flujo
- `Día 8-10` :: Mensajes de error: provoca 5 errores a propósito y tradúcelos
- `Día 11-12` :: Frases de documentación: lee la doc de 3 funciones (`sorted`, `open`, `print`)
- `Día 13-14` :: Vocabulario de IA/ML: lee el "Quickstart" de PyTorch o scikit-learn
- `Día 15-17` :: Renombra variables de un proyecto viejo tuyo a buen inglés
- `Día 18-20` :: Escribe 10 commits con Conventional Commits y un PR completo de práctica
- `Día 21` :: Escribe una pregunta estilo Stack Overflow sobre un bug real tuyo
- `Día 22-24` :: Graba tu daily standup cada día
- `Día 25-27` :: Practica "Tell me about yourself" y una pregunta STAR
- `Día 28-29` :: Resuelve un problema de LeetCode fácil pensando en voz alta en inglés
- `Día 30` :: Repaso: vuelve a grabarte el día 2 y compara. ¡Notarás la diferencia!

### 🔗 Recursos recomendados

- `Documentación oficial` :: docs.python.org, MDN Web Docs (JS/CSS/HTML), Git Book: el mejor inglés técnico, gratis
- `YouGlish` :: Escribe una palabra y te muestra videos de YouTube donde se pronuncia
- `Cambridge Dictionary` :: Definiciones simples y audio en inglés británico y americano
- `Anki` :: Tarjetas con repetición espaciada para vocabulario
- `freeCodeCamp` :: Cursos completos en inglés, con artículos y videos
- `CS50 (Harvard)` :: Curso de introducción a la computación en inglés, con subtítulos
- `Fireship, ThePrimeagen, 3Blue1Brown` :: Canales técnicos en inglés (rápido, moderno, visual)
- `Podcasts` :: Syntax, Changelog, Lex Fridman (IA)
- `Exercism / LeetCode` :: Enunciados en inglés: practicas leer problemas
- `Contribuir a open source` :: Busca issues con la etiqueta "good first issue" en GitHub
- `Pramp / Interviewing.io` :: Simulacros de entrevistas técnicas en inglés

💡 Consejo: usa un LLM como tutor: pídele "Correct my English and explain the mistakes" después de escribir un PR o un mensaje. Aprendes de tus propios errores.

📌 Resumen: **lee docs todos los días, busca en inglés, escribe commits en inglés y habla en voz alta explicando tu código**. La constancia gana a la intensidad.
