# 🇬🇧 Inglés 1 · Sonidos y vocabulario
> Cómo estudiar, los sonidos que el español no tiene, pronunciar y leer código en voz alta, y el vocabulario técnico por áreas.

## 🧭 Cómo estudiar inglés programando

El inglés técnico es **mucho más fácil** que el inglés general: unas 1500–2000 palabras cubren casi toda la documentación, las frases se repiten y la gramática de las docs es simple. Ya lo practicas cada vez que lees un error o escribes `return`; el truco es hacerlo **a propósito**, **en voz alta** y **todos los días**.

### 🔁 El método de 20 minutos al día

El cerebro aprende por repetición espaciada: 20 minutos diarios rinden más que 3 horas el domingo. Reparte así tu rato:

| ⏱️ Minutos | 🎯 Qué hacer | 🧪 Ejemplo concreto | 🧠 Por qué funciona |
|---|---|---|---|
| 0–5 | Leer algo técnico real | Un apartado de la doc de Python o un README | Vocabulario en contexto real |
| 5–8 | Anotar 3–5 frases nuevas | "Defaults to `None`" = "por defecto vale None" | Frases enteras se recuerdan mejor que palabras |
| 8–12 | Escuchar e imitar (shadowing) | 1 minuto de un video técnico, repitiendo encima | Entrena oído y boca a la vez |
| 12–16 | Repasar tarjetas Anki | Las que tocan hoy, diciéndolas en voz alta | Repetición espaciada: no olvidas |
| 16–20 | Escribir o hablar | Un commit, un comentario o explicar tu código en voz alta | Pasas de entender a producir |

```flujo
dir: derecha
Leer -> Anotar : frases
Anotar -> Imitar : shadowing
Imitar -> Anki : repasar
Anki -> Producir : escribir o hablar
Producir --> Leer : mañana otra vez
```

### 📅 Repetición espaciada: cuándo repasar

Cada repaso justo antes de olvidar multiplica cuánto dura el recuerdo. Anki lo calcula solo; si usas libreta, sigue esta tabla:

| 🔁 Repaso | 📆 Cuándo | ✅ Qué haces | 💬 Ejemplo |
|---|---|---|---|
| 1º | El mismo día | Lees la frase y la dices 3 veces | "The function **returns** a list" |
| 2º | Al día siguiente | Tapas el inglés y lo reconstruyes | "La función devuelve…" → "returns" |
| 3º | A los 3 días | La usas en una frase tuya | "My parser returns a dict" |
| 4º | A la semana | La buscas en código real | grep `returns` en una doc |
| 5º | A las 2 semanas | La dices sin pensar | En tu standup imaginario |
| 6º | Al mes | Ya es tuya: sale de la libreta | — |

```tiempo
Día 0 : 1º repaso, la dices 3 veces
Día 1 : 2º, reconstruyes la frase
Día 3 : 3º, la usas en una frase tuya
Día 7 : 4º, la buscas en código real
Día 14 : 5º, la dices sin pensar
Día 30 : 6º, ya es tuya
```

### 🃏 Cómo hacer buenas tarjetas Anki

| 🪪 Frente | 🔙 Reverso | 💡 Por qué |
|---|---|---|
| "Esta función **lanza** un error si…" | "This function **raises** an error if…" | Frase completa, no palabra suelta |
| queue (con audio) | **kiú** · cola · `queue.put(job)` | Sonido + significado + código |
| "¿Cómo se lee `a[i]`?" | "a sub i" / "a at index i" | Practica leer código |
| Imagen de un árbol binario | binary tree · root · leaf · node | Imagen → inglés, sin español en medio |
| "set up (verbo) vs setup (sustantivo)" | "Let's set up the DB" / "The setup is easy" | Contrastes que confunden |

💡 Consejo: una tarjeta = una idea. Si una tarjeta te cuesta mucho, pártela en dos más pequeñas.

### 🛠️ Inmersión sin esfuerzo

| 🔧 Qué cambiar | 🪄 Cómo | 🎁 Qué ganas |
|---|---|---|
| Sistema operativo | Idioma del sistema, teléfono y navegador en inglés | Aprendes menús sin darte cuenta: Settings, Preferences, Display |
| Editor / IDE | VS Code: "Configure Display Language" → English | Los mensajes coinciden con lo que buscas en Google |
| Buscador | Busca SIEMPRE en inglés | "python read csv" da muchos más resultados que en español |
| Errores | Copia el mensaje literal en el buscador | Llegas directo a Stack Overflow y GitHub Issues |
| Código | Variables, comentarios y commits en inglés | Práctica de escritura diaria gratis |
| Videos | Subtítulos en inglés, no en español | Conectas sonido con escritura |
| Tu voz | Explica tu código en voz alta (rubber duck en inglés) | Preparas entrevistas y reuniones |
| Asistente de IA | Pídele que te responda en inglés y te corrija | Corrección inmediata y sin vergüenza |
| Juegos y series | Audio en inglés con subtítulos en inglés | Oído para acentos y velocidad real |

### 🗓️ Plan semanal

| 📆 Día | 🎯 Foco | 🧪 Actividad | ⏱️ Tiempo |
|---|---|---|---|
| Lunes | Sonidos | Practica 2 sonidos de la sección de sonidos con sus palabras | 20 min |
| Martes | Lectura | Lee una página de documentación y anota 5 frases | 20 min |
| Miércoles | Vocabulario | Una tabla de vocabulario por área: léela en voz alta y haz tarjetas | 20 min |
| Jueves | Escucha | Un video técnico con shadowing de 2–3 frases | 20 min |
| Viernes | Leer código | Lee en voz alta 10 líneas de tu propio código | 20 min |
| Sábado | Producción | Graba 2 minutos explicando un proyecto tuyo y escúchate | 30 min |
| Domingo | Repaso | Solo Anki y repasar lo que más te costó | 15 min |

### 🎧 Podcasts y canales para el oído técnico

| 📺 Nombre | 🧩 Tipo | 📚 Tema | 🗣️ Nivel de inglés |
|---|---|---|---|
| CS50 (Harvard, David Malan) | Curso en video | Fundamentos de CS | Claro y pausado: ideal para empezar |
| 3Blue1Brown | YouTube | Matemáticas, álgebra lineal, redes neuronales | Claro, con animaciones |
| StatQuest with Josh Starmer | YouTube | Estadística y ML explicados paso a paso | Lento y muy claro |
| Corey Schafer | YouTube | Python | Claro y pausado |
| Andrej Karpathy | YouTube | Redes neuronales y LLMs desde cero | Medio, muy técnico |
| Computerphile | YouTube | Conceptos de CS con profesores | Medio, acento británico |
| freeCodeCamp.org | YouTube | Cursos largos de todo | Variado |
| Fireship | YouTube | Tecnologías en 100 segundos | Rápido: para cuando ya entiendas |
| Ben Eater | YouTube | Hardware y electrónica digital | Claro y detallado |
| Hussein Nasser | YouTube / podcast | Backend, bases de datos, redes | Medio |
| Talk Python To Me | Podcast | Ecosistema Python | Medio, conversacional |
| Syntax | Podcast | Desarrollo web | Rápido y coloquial |
| Practical AI | Podcast | IA aplicada | Medio |
| Latent Space | Podcast | Ingeniería de IA y LLMs | Rápido y técnico |
| Lex Fridman Podcast | Podcast | IA, ciencia, entrevistas largas | Lento: bueno para practicar |

💡 Consejo: empieza con los de inglés claro (CS50, StatQuest, Corey Schafer) a velocidad 0.9x; sube a 1x cuando entiendas el 80 %.

⚠️ Cuidado: no traduzcas palabra por palabra desde el español. Pregúntate "¿cómo lo diría una doc?" y copia ese patrón: **"make sure"**, no "assure you of".

🇬🇧 Frase modelo para practicar todos los días: "Today I worked on ___. I ran into ___, and I fixed it by ___."

📌 Objetivo realista: en 3 meses leer docs sin traductor; en 6 escribir issues y PRs; en 12 defenderte en una entrevista técnica.

## 🔊 Los sonidos del inglés que no existen en español

El español tiene 5 vocales y casi todas sus consonantes se pronuncian "como se escriben". El inglés tiene unas **12 vocales**, varios diptongos y consonantes que tu boca no ha practicado nunca. Si aprendes estos sonidos una vez, todas las palabras técnicas se vuelven más fáciles.

### 🗝️ Cómo leer la columna «Suena» en toda esta hoja

| ✍️ Se escribe | 🔊 Sonido real | 🧪 Ejemplo | 🗣️ Cómo hacerlo |
|---|---|---|---|
| MAYÚSCULAS o tilde | Sílaba fuerte | di-PLÓI (deploy) | Más fuerte, más larga y más aguda |
| z | th sorda (como la "z" de España) | zred (thread) | Lengua entre los dientes, soplando |
| dh | th sonora | dhis (this) | Igual que "z" pero vibrando la garganta |
| sh | sh inglesa | shel (shell) | Como cuando pides silencio |
| zh | como la "y" argentina de "yo" | Á-zher (Azure) | Una "sh" con vibración |
| y | j o g inglesa (dy) | YÉI-son (JSON) | Una "ch" con vibración, como "dy" |
| j | h inglesa | jash (hash) | Solo aire, como empañar un vidrio, nunca la jota raspada |
| i (delante de vocal) | y de "yes" | kiú (queue) | Como la "i" de "hielo" |
| r | r inglesa | ran (run) | Lengua curvada hacia atrás sin tocar nada, nunca vibra |
| a / e sin acento | schwa, vocal neutra | DÉI-ta (la -a final) | Una "e/a" floja y corta, casi no se oye |

### 👅 Consonantes que no tienes

| 🔊 Sonido | 👄 Cómo se hace | 💻 Palabras de programación | ⚠️ Error típico del hispanohablante |
|---|---|---|---|
| th sorda (z) | Punta de la lengua entre los dientes y soplar | thread, throw, through, math, path, width, length, depth, auth, method, Python | Decir "t" o "s": "tred", "sred", "mat" |
| th sonora (dh) | Misma posición pero vibrando la garganta | the, this, that, then, than, other, either, whether, with | Una "d" fuerte: "de", "dis" |
| v | Dientes de arriba sobre el labio de abajo, vibrando | void, value, variable, vector, version, view, server, private, move | Decir "b": "boid", "bálue" |
| z | Zumbido de abeja, con vibración | zero, zip, size, resize, use (verbo), is, has, users, files | Decir "s" sorda: "sero", "sáis" |
| sh | Labios hacia adelante, como pedir silencio | shell, push, hash, flush, crash, session, function, cache | Decir "ch": "chel" en vez de "shel" |
| ch | Como en "chico" | fetch, branch, catch, match, switch, batch, check, patch, search | Confundir **cache** (kash) con **catch** (kech) |
| zh | Una "sh" con vibración | Azure, usually, version, decision, precision, visual, measure | Decir "s": "versión" en vez de "VÉR-zhon" |
| j/g inglesa (y) | Una "ch" con vibración | JSON, Java, jQuery, Django, object, page, edge, merge, image, package | Decir jota española: "jéison", "jáva" |
| h | Solo aire, suave | hash, heap, host, header, hidden, hook, handler, hello | Hacerla muda ("ash") o raspada como jota |
| r | Lengua curvada atrás, sin tocar el paladar | run, return, error, array, request, string, server, render | La "rr" vibrante: "rrrun", "errrror" |
| ng final | Como la "n" de "tengo", sin decir la "g" | string, thing, loading, parsing, long, ping, logging | Decir "strin" o "string-gue" |
| p, t, k aspiradas | Con un soplo de aire al inicio de sílaba fuerte | push, type, key, code, token, compile | Sin aire: "type" suena a "daip" para un nativo |
| w | Labios redondos, como "u" rápida | while, web, window, wait, swap, await, wire | Una "gü" fuerte: "güeb", "güail" |

### 🅰️ Vocales: largas, cortas y las que no tienes

| 🔊 Sonido | 👄 Cómo se hace | 💻 Palabras de programación | ⚠️ Error típico |
|---|---|---|---|
| i larga | "i" tensa y larga, sonriendo | key, seed, read, keep, delete, free, tree, need | Hacerla corta: "least" suena a "list" |
| i corta | Entre "i" y "e", relajada y breve | bit, list, int, fix, build, git, script, big | Hacerla larga: "list" suena a "least" |
| a de "cat" (æ) | Boca muy abierta, entre "a" y "e" | hash, cache, stack, class, app, bash, map, match, back, batch | Una "a" española corta: se acerca a otra palabra |
| a corta (ʌ) | "a" breve y floja, boca poco abierta | bug, run, null, function, public, buffer, sum, cut, number | Decir "u": "bug" con u, "nul" |
| a larga de la "o" (EE. UU.) | "a" abierta y larga; la letra **o** suena así | Docker, job, lock, block, stop, object, dot, box, model, module, comment | Decir "o" española: "dóker", "blok" |
| ou (diptongo) | "o" que se cierra en "u" | code, node, mode, load, go, token, local, open, close | "o" pura: "code" sonaría a "cod" |
| ei (diptongo) | "e" que se cierra en "i" | name, case, table, save, state, data, make, page | "e" pura: "nem", "tébol" |
| ai (diptongo) | La letra **i** en sílaba fuerte | type, file, line, size, while, find, byte, library | Leer "i" española: "tipe", "file" |
| u larga | "u" tensa y larga | loop, root, tool, boot, new, true, route, use | — |
| u corta (ʊ) | "u" floja y breve | push, pull, full, book, look, cookie, hook, put | Hacerla larga: "full" suena a "fool" |
| er (ɜr) | Vocal neutra + r inglesa, sin vibrar | first, term, server, worker, merge, turn, word, work | "work" con "o" suena a "walk" |
| schwa (ə) | Vocal neutra y floja | **a**bout, dat**a**, param**e**ter, func**tion**, read**able** | Pronunciar todas las vocales igual de fuerte |

💡 Consejo: el **schwa** es el sonido más común del inglés. Las sílabas sin acento casi desaparecen: "pa-RÁ-mi-ter" suena "pə-RÁ-mə-tər". Si dices todas las vocales claras, sonarás "robótico".

### ✏️ La terminación -ed (pasado)

Depende del último sonido del verbo. Solo se añade una sílaba "id" cuando termina en **t** o **d**.

| 🔊 Suena | 📏 Regla | 💻 Ejemplos | ⚠️ Error típico |
|---|---|---|---|
| **t** | Tras sonido sordo: p, k, f, s, sh, ch | fixed (fikst), pushed (pusht), parsed (parst), cached (kasht), stashed, fetched | "fik-sed", "push-ed" |
| **d** | Tras sonido sonoro o vocal | logged (logd), deployed (di-PLÓID), merged (merdyd), called, saved, configured | "di-ploi-ed" con sílaba extra |
| **id** | Tras t o d | updated (ap-DÉI-tid), deleted, added (Á-did), loaded, imported, deprecated, started | Comerse la sílaba: "updat" |

```flujo
dir: abajo
Verbo en pasado -> ¿Acaba en t o d? : mira el último sonido
¿Acaba en t o d? -> id : sí (updated, added)
¿Acaba en t o d? -> ¿Sonido sordo? : no
¿Sonido sordo? -> t : sí (fixed, pushed)
¿Sonido sordo? -> d : no (logged, saved)
```

### ✏️ La terminación -s / -es (plural y 3ª persona)

| 🔊 Suena | 📏 Regla | 💻 Ejemplos | ⚠️ Error típico |
|---|---|---|---|
| **s** | Tras p, t, k, f | types (taips), commits, tests, scripts, hooks, chunks | Comerse la s final: "tes", "scrip" |
| **z** | Tras sonido sonoro o vocal | files (failz), nodes, bugs, runs, rows, arrays, keys | Decir "s" sorda: "bugs" como "bags" con s |
| **iz** | Tras s, z, sh, ch, x, ge | hashes (JÁ-shiz), caches (KÁ-shiz), classes, branches, matches, indexes, pages | Olvidar la sílaba extra: "clas", "brach" |

### 🎵 Ritmo: dónde va el golpe

| 📏 Regla | 💻 Ejemplos | 🗣️ Suena | 💡 Truco |
|---|---|---|---|
| Sustantivo compuesto: golpe en la 1ª parte | database, keyboard, password, username, laptop, backend | DÉI-ta-beis, KÍ-bord, PÁS-uerd | "Una cosa" = golpe al inicio |
| Phrasal verb: golpe en la partícula | set **UP**, log **IN**, back **UP**, roll **BACK** | "Let's set ÁP the server" | Es una acción |
| El sustantivo del phrasal verb: golpe al inicio | **SET**up, **LOG**in, **BACK**up, **ROLL**back | "The SÉT-ap is easy" | Es una cosa |
| Números -teen vs -ty | thirteen vs thirty, fifteen vs fifty | zer-TÍN vs ZÉR-di | -teen golpe al final; -ty al inicio |
| Siglas: golpe en la última letra | API, CLI, SQL, URL, HTML | ei-pi-ÁI, si-el-ÁI, es-kiu-ÉL | Igual en todas las siglas deletreadas |
| Palabras de función se debilitan | "a list of nodes", "to the server" | "ə LÍST əv NÓUDZ" | Solo suenan fuertes las palabras con significado |

### 😬 Malentendidos reales (aprende de los errores de otros)

Estos errores son clásicos entre hispanohablantes en reuniones técnicas. No son graves, pero mejor evitarlos:

| 🎯 Querías decir | 😬 Se entendió | 🔊 Diferencia | ✅ Cómo decirlo bien |
|---|---|---|---|
| sheet (spreadsheet) | una grosería | i larga vs i corta | Alarga y sonríe: "shiiit" con i tensa |
| piece (of code) | una grosería | i larga vs i corta | "piis", larga y tensa |
| focus | una grosería | La o es diptongo "ou" | **FÓU-kas**, nunca "fókus" con o abierta |
| can't | can (lo contrario) | La t final y la vocal | "I can't" más largo y con t; "I can" se debilita a "kən" |
| thirteen | thirty | Golpe | zer-**TÍN** vs **ZÉR**-di |
| a bug | a bag (una bolsa) | ʌ vs æ | bug = "bag" corta y floja; bag = boca muy abierta |
| full (lleno) | fool (tonto) | u corta vs u larga | full corta y floja |
| live demo | "liv" (vivir) | Adjetivo: ai | **láiv** demo, go **láiv** |
| work | walk (caminar) | Vocal "er" | "uerk" con la r inglesa, sin "o" |
| lock | luck / lack | o americana = a abierta | lock = "lak" (boca abierta); luck = "lak" corta y floja; lack = æ, entre a y e |
| sixty | sixteen | Golpe | **SÍKS**-ti vs siks-**TÍN** |

⚠️ Cuidado: la "s" inicial va pegada. "String", "stack", "script" nunca llevan una "e" delante: di **sss-tring**, no "e-string".

🇬🇧 Trabalenguas para la th: "I think this thread throws three things through the method."

📌 Resumen: domina primero **th**, **v**, la **i corta/larga**, el **schwa** y el **golpe**; con eso te entienden casi siempre.

## 🗣️ Pronunciación de palabras técnicas

Muchas palabras técnicas las decimos "como se escriben" en español, y en una reunión o entrevista suena raro o no te entienden. Pronunciación estándar americana; cuando hay dos formas aceptadas, aparecen ambas.

### 🧰 Lenguajes, frameworks y herramientas

| English | Suena | Qué es | Ejemplo en frase |
|---|---|---|---|
| Linux | **LÍ**-nax | Sistema operativo | "I run Arch Linux" (no "láinux") |
| GNU | gu-**NÚ** | Proyecto de software libre | "GNU slash Linux" |
| Ubuntu | u-**BÚN**-tu | Distro | "an Ubuntu server" |
| Debian | **DÉ**-bi-an | Distro | "Debian stable" |
| Arch | arch (ch de "chico") | Distro | "I use Arch, by the way" |
| Fedora | fe-**DÓ**-ra | Distro | "Fedora Workstation" |
| Windows | **UÍN**-dous | Sistema operativo | "it only fails on Windows" |
| macOS | mak-ou-**ÉS** | Sistema operativo | "tested on macOS" |
| nginx | **ÉN**-yin-éks ("engine x") | Servidor web | "the nginx config" |
| Apache | a-**PÁ**-chi | Servidor web / fundación | "Apache Kafka" |
| SQL | **ÉS**-kiu-él o **SÍ**-kuel | Lenguaje de consultas | "write a SQL query" |
| MySQL | mai-es-kiu-**ÉL** | Base de datos | "a MySQL dump" |
| PostgreSQL / Postgres | **PÓUST**-gres-kiu-él / **PÓUST**-gres | Base de datos | "we migrated to Postgres" |
| SQLite | es-kiu-el-**ÁIT** o **SÍ**-kue-lait | Base de datos en un archivo | "a local SQLite file" |
| MongoDB | **MÁN**-gou-di-bi | Base de datos NoSQL | "a Mongo collection" |
| Redis | **RÉ**-dis | Caché en memoria | "cache it in Redis" |
| Kafka | **KÁF**-ka | Cola de mensajes | "a Kafka topic" |
| GraphQL | **GRAF**-kiu-el | Lenguaje de APIs | "a GraphQL endpoint" |
| GUI | **GÚ**-i ("gooey") | Interfaz gráfica | "a GUI app" |
| GIF | guif o yif | Formato de imagen animada | "send a GIF" (las dos valen) |
| sudo | **SÚ**-du o **SÚ**-dou | Ejecutar como superusuario | "run it with sudo" |
| Git | guit (g de "gato") | Control de versiones | "push it to Git" |
| GitHub | **GUIT**-jab | Plataforma de repos | "it's on GitHub" |
| Python | **PÁI**-zan | Lenguaje | "I code in Python" |
| Java | **YÁ**-va | Lenguaje | "a Java backend" |
| JavaScript | **YÁ**-va-skript | Lenguaje | "plain JavaScript" |
| TypeScript | **TÁIP**-skript | JS con tipos | "migrate to TypeScript" |
| C / C++ / C# | si / si plas plas / si sharp | Lenguajes | "a C sharp project" |
| Rust | rast | Lenguaje | "rewrite it in Rust" |
| Go / Golang | gou / **GÓU**-lang | Lenguaje | "a Go microservice" |
| Kotlin | **KÁT**-lin | Lenguaje (Android) | "Kotlin coroutines" |
| Haskell | **JÁS**-kel | Lenguaje funcional | "Haskell is pure" |
| Ruby | **RÚ**-bi | Lenguaje | "Ruby on Rails" |
| Lua | **LÚ**-a | Lenguaje de scripts | "my Neovim config is in Lua" |
| PHP | pi-eich-**PÍ** | Lenguaje web | "a legacy PHP site" |
| Node.js | **NÓUD** yei-es | Entorno de JS | "a Node server" |
| npm | en-pi-**ÉM** | Gestor de paquetes JS | "npm install" |
| React | ri-**ÁKT** | Biblioteca de UI | "a React component" |
| Vue | viú (como "view") | Framework de UI | "a Vue app" |
| Angular | **ÁN**-giu-ler | Framework de UI | "an Angular service" |
| Svelte | svelt | Framework de UI | "Svelte stores" |
| Next.js | nekst yei-es | Framework de React | "a Next app" |
| Vite | vit (como "veet") | Herramienta de build | "start the Vite dev server" |
| Django | **YÁN**-gou (la D es muda) | Framework web de Python | "a Django model" |
| Tailwind | **TÉIL**-uind | Framework de CSS | "Tailwind classes" |
| Docker | **DÁ**-ker | Contenedores | "run it in Docker" |
| Kubernetes / k8s | ku-ber-**NÉ**-tis / kei-ÉITS ("k-eights") | Orquestador de contenedores | "deploy to Kubernetes" |
| Terraform | **TÉ**-ra-form | Infraestructura como código | "a Terraform plan" |
| Ansible | **ÁN**-si-bol | Automatización | "an Ansible playbook" |
| Jenkins | **YÉN**-kins | CI | "the Jenkins job failed" |
| Azure | **Á**-zher | Nube de Microsoft | "hosted on Azure" |
| Vercel | ver-**SÉL** | Hosting | "deployed on Vercel" |
| Heroku | je-**RÓU**-ku | Hosting | "a Heroku dyno" |
| YAML | **YÁ**-mel | Formato de configuración | "edit the YAML file" |
| JSON | **YÉI**-son | Formato de datos | "send it as JSON" |
| TOML | **TÁ**-mel | Formato de configuración | "pyproject.toml" |
| regex | **RÉ**-yeks o **RÉ**-gueks | Expresión regular | "a simple regex" |
| Vim / Neovim | vim / ni-ou-**VÍM** | Editores | "I live in Neovim" |
| Emacs | **Í**-maks | Editor | "Emacs vs Vim" |
| LaTeX | **LÁ**-tek o **LÉI**-tek | Tipografía científica | "write the paper in LaTeX" |
| Qt | kiút ("cute") | Framework de UI | "a Qt app" |
| GNOME | gui-**NÓUM** o nóum | Escritorio Linux | "GNOME Shell" |
| Wayland | **UÉI**-land | Protocolo gráfico | "it breaks on Wayland" |
| Wi-Fi | **UÁI**-fai | Red inalámbrica | "the Wi-Fi is down" |
| Bluetooth | **BLÚ**-tuz (z = th sorda) | Conexión inalámbrica | "Bluetooth pairing" |
| NVIDIA | en-**VÍ**-dia | Fabricante de GPUs | "an NVIDIA driver" |
| CUDA | **KÚ**-da | Plataforma de cómputo en GPU | "CUDA out of memory" |

### 🤖 Herramientas de IA y datos

| English | Suena | Qué es | Ejemplo en frase |
|---|---|---|---|
| PyTorch | **PÁI**-torch | Framework de deep learning | "a PyTorch model" |
| TensorFlow | **TÉN**-ser-flou | Framework de deep learning | "TensorFlow Lite" |
| Keras | **KÉ**-ras | API de redes neuronales | "a Keras layer" |
| Jupyter | **YÚ**-pi-ter | Notebooks | "open a Jupyter notebook" |
| NumPy | **NÁM**-pai | Arrays numéricos | "a NumPy array" |
| SciPy | **SÁI**-pai | Cómputo científico | "scipy.stats" |
| pandas | **PÁN**-das | DataFrames | "load it into pandas" |
| Matplotlib | **MÁT**-plat-lib | Gráficas | "plot it with Matplotlib" |
| scikit-learn | **SÁI**-kit lern | ML clásico | "a scikit-learn pipeline" |
| Hugging Face | **JÁ**-guing féis | Hub de modelos | "download it from Hugging Face" |
| Kaggle | **KÁ**-guel | Competencias de datos | "a Kaggle dataset" |
| Colab | **KÓU**-lab | Notebooks en la nube | "run it on Colab" |
| conda / Anaconda | **KÁN**-da / a-na-**KÁN**-da | Gestor de entornos | "a conda environment" |
| LangChain | **LÁNG**-chein | Framework de LLMs | "a LangChain agent" |
| XGBoost | eks-yi-**BÚST** | Gradient boosting | "an XGBoost classifier" |
| Ollama | ou-**LÁ**-ma | LLMs en local | "pull a model with Ollama" |
| Llama | **LÁ**-ma | Familia de modelos | "a Llama fine-tune" |
| Gemini | **YÉ**-mi-nai | Modelo de Google | "Gemini API" |
| Claude | klod | Modelo de Anthropic | "ask Claude" |
| Anthropic | an-**ZRÁ**-pik | Empresa de IA | "the Anthropic API" |
| Whisper | **UÍS**-per | Transcripción de voz | "transcribe it with Whisper" |

### 💻 Comandos de terminal (cómo los dice la gente)

| Comando | Suena | Qué hace | Frase hablada |
|---|---|---|---|
| `ls` | el-és | Lista archivos | "just el-és the folder" |
| `cd` | si-dí | Cambia de carpeta | "si-dí into src" |
| `pwd` | pi-dábol-iu-dí | Carpeta actual | "run pwd" |
| `mkdir` | **MÉIK**-dir o em-kei-dír | Crea carpeta | "mkdir a new folder" |
| `rm -rf` | ar-em ar-ef | Borra recursivo y forzado | "careful with rm -rf" |
| `chmod` | **CH**-mad o si-eich-mad | Cambia permisos | "chmod plus x the script" |
| `grep` | grep | Busca texto | "grep for the error" |
| `sed` | sed | Edita texto en flujo | "a sed one-liner" |
| `awk` | ok (como "talk") | Procesa columnas | "awk the second column" |
| `curl` | kerl | Peticiones HTTP | "curl the endpoint" |
| `wget` | dábol-iu-guet | Descarga | "wget the tarball" |
| `ssh` | es-es-**ÉICH** | Conexión remota | "ssh into the box" |
| `tmux` | **TÍ**-maks | Multiplexor de terminal | "a tmux session" |
| `htop` | **ÉICH**-tap | Monitor de procesos | "check htop" |
| `cron` | kran | Tareas programadas | "a cron job" |
| `zsh` | zi-shel o zed-shel | Shell | "switch to zsh" |
| `/etc` | et-si o **ÉT**-si | Carpeta de configuración | "it's in slash etc" |
| `/usr` | **IÚ**-ser | Carpeta de programas | "slash user slash bin" |
| `/var` | var | Datos variables, logs | "slash var slash log" |
| `/tmp` | temp | Temporales | "slash temp" |

### 🎯 Palabras de código que se dicen mal

| English | Suena | Español | Ejemplo en código |
|---|---|---|---|
| queue | kiú | cola | `queue.put(task)` |
| cache | kash (como "cash") | caché | `@lru_cache` — nunca "cachÉ" ni "cachi" |
| cached / caching | kasht / **KÁ**-shing | en caché / cacheo | "the result is cached" |
| char | char, kar o ker | carácter | `char c = 'a';` |
| character | **KÉ**-rak-ter | carácter | "an invalid character" |
| width | uídz | ancho | `width: 100%` |
| height | jáit (rima con "light") | alto | `height: 50px` |
| length | lenkz | longitud | `arr.length` |
| depth | depz | profundidad | `max_depth=5` |
| null | nal | nulo | "it returns null" |
| void | void (v de labio) | vacío | `void main()` |
| suite | suít (como "sweet") | conjunto | "the test suite" |
| schema | **SKÍ**-ma | esquema | "the database schema" |
| daemon | **DÍ**-mon o **DÉI**-mon | servicio de fondo | `dockerd` daemon |
| async | **ÉI**-sink | asíncrono | `async def main():` |
| await | a-**UÉIT** | esperar | `await fetch(url)` |
| synchronous | **SÍN**-kro-nas | síncrono | "a synchronous call" |
| enum | **Í**-nam o **Í**-num | enumeración | `enum Color` |
| tuple | **TÚ**-pol o **TÁ**-pol | tupla | `(1, 2)` |
| alias | **ÉI**-li-as | alias | `alias ll='ls -la'` |
| boolean | **BÚ**-li-an | booleano | `bool` |
| integer | **ÍN**-ti-yer | entero | `int` |
| array | a-**RÉI** | arreglo | `const arr = []` |
| variable | **VÉ**-ri-a-bol | variable | "declare a variable" |
| function | **FÁNK**-shon | función | "call the function" |
| method | **MÉ**-zad | método | "a method of the class" |
| object | **ÁB**-yekt | objeto | "an object in memory" |
| module | **MÁ**-yul | módulo | "the os module" |
| private | **PRÁI**-vet | privado | `private int x;` |
| key | ki | clave, llave | "the API key" |
| lambda | **LÁM**-da | lambda | `lambda x: x * 2` |
| binary | **BÁI**-na-ri | binario | "a binary file" |
| buffer | **BÁ**-fer | búfer | "flush the buffer" |
| cursor | **KÉR**-ser | cursor | `db.cursor()` |
| mutex | **MIÚ**-teks | candado de hilos | "acquire the mutex" |
| pixel | **PÍK**-sel | píxel | "a 1-pixel border" |
| vector | **VÉK**-ter | vector | `std::vector` |
| matrix / matrices | **MÉI**-triks / **MÉI**-tri-siz | matriz / matrices | "a 3x3 matrix" |
| index / indices | **ÍN**-deks / **ÍN**-di-siz | índice / índices | "the indices of the array" |
| vertex / vertices | **VÉR**-teks / **VÉR**-ti-siz | vértice / vértices | "graph vertices" |
| axis / axes | **ÁK**-sis / **ÁK**-siz | eje / ejes | `axis=0` |
| route | rut o raut | ruta | `@app.route("/")` |
| router | **RÁU**-ter | enrutador | "the React router" |
| query | **KUÍ**-ri | consulta | "run the query" |
| data | **DÉI**-ta o **DÁ**-ta | datos | "load the data" |
| algorithm | **ÁL**-go-ri-dhem | algoritmo | "a sorting algorithm" |
| parameter | pa-**RÁ**-mi-ter | parámetro | "the second parameter" |
| library | **LÁI**-bre-ri | biblioteca | "import the library" |
| image | **Í**-midy | imagen | "a Docker image" |
| package | **PÁ**-kidy | paquete | "install the package" |
| message | **MÉ**-sidy | mensaje | "the error message" |
| language | **LÁN**-guidy | lenguaje | "a programming language" |
| storage | **STÓ**-ridy | almacenamiento | "cloud storage" |
| average | **Á**-ve-ridy | promedio | "the average loss" |
| cipher | **SÁI**-fer | cifrado | "a block cipher" |
| hierarchy | **JÁI**-rar-ki | jerarquía | "class hierarchy" |
| architecture | **ÁR**-ki-tek-cher | arquitectura | "a clean architecture" |
| archive | **ÁR**-kaiv | archivo comprimido | "extract the archive" |
| schedule | **SKÉ**-yul | programar, horario | "schedule a job" |
| technique | tek-**NÍK** | técnica | "a caching technique" |
| feature | **FÍ**-cher | función, característica | "a new feature" |
| exception | ik-**SÉP**-shon | excepción | "raise an exception" |
| recursion | ri-**KÉR**-zhon | recursión | "use recursion" |
| execute | **ÉK**-se-kiut | ejecutar | "execute the script" |
| executable | ig-**ZÉ**-kiu-ta-bol | ejecutable | "an executable file" |
| exit | **ÉG**-zit o **ÉK**-sit | salir | `exit(1)` |
| thread | zred | hilo | "spawn a new thread" |
| through | zru | a través de | "iterate through the list" |
| though / thought | dhou / zat | aunque / pensé | "it works, though" |
| width vs with | uídz / uidh | ancho / con | "with a width of 10" |
| epoch | **É**-pak o **Í**-pak | época | `epochs=10` |
| Euler | **ÓI**-ler | Euler | "Euler's number" |
| Dijkstra | **DÁIK**-stra | Dijkstra | "Dijkstra's algorithm" |
| Gaussian | **GÁU**-si-an | gaussiano | "Gaussian noise" |
| Bayes | beiz | Bayes | "naive Bayes" |
| Fourier | **FÚ**-ri-ei | Fourier | "Fourier transform" |
| Turing | **TÚ**-ring | Turing | "Turing complete" |
| Raspberry Pi | **RÁZ**-be-ri pai (p muda) | Raspberry Pi | "a Raspberry Pi cluster" |
| Arduino | ar-**DUÍ**-nou | Arduino | "an Arduino sketch" |

### 🎢 Acento en la sílaba sorpresa

En estas palabras el golpe cae donde un hispanohablante no lo espera.

| English | Suena | ⚠️ No digas | Ejemplo |
|---|---|---|---|
| develop / developer | di-**VÉ**-lop / di-**VÉ**-lo-per | "de-ve-LOP" | "a backend developer" |
| component | kom-**PÓU**-nent | "kom-po-NENT" | "a React component" |
| compiler | kom-**PÁI**-ler | "kom-pi-LER" | "the compiler complains" |
| interface | **ÍN**-ter-feis | "in-ter-FEIS" | "a clean interface" |
| analysis / analyze | a-**NÁ**-li-sis / **Á**-na-laiz | "a-na-LI-sis" | "analyze the logs" |
| determine | di-**TÉR**-min | "de-ter-MAIN" | "determine the type" |
| event | i-**VÉNT** | "É-vent" | "an event listener" |
| success | sak-**SÉS** | "SÁK-ses" | "success rate" |
| install | in-**STÓL** | "ÍN-stal" | "install the package" |
| Wednesday | **UÉNZ**-dei | "uéd-nes-dei" | "deploy on Wednesday" |
| comfortable | **KÁMF**-ter-bol | "kom-for-TÉI-bol" | "comfortable with Python" |
| hotel / career | jou-**TÉL** / ka-**RÍR** | "KÁ-rrier" | "a career in AI" |
| photograph / photography | **FÓU**-to-graf / fo-**TÁ**-gra-fi | Dejar el golpe en el mismo sitio | El golpe se mueve al añadir sufijo |
| economy / economic | i-**KÁ**-no-mi / i-ko-**NÁ**-mik | Dejar el golpe en el mismo sitio | El golpe se mueve al añadir sufijo |

### 🔄 Mismo escrito, distinto golpe: sustantivo vs verbo

Regla: **sustantivo** con golpe al inicio, **verbo** con golpe al final.

| Palabra | Sustantivo (cosa) | Verbo (acción) | Ejemplo |
|---|---|---|---|
| record | **RÉ**-kord (registro) | ri-**KÓRD** (grabar) | "record a new record" |
| object | **ÁB**-yekt (objeto) | ob-**YÉKT** (objetar) | "I object to this object" |
| import | **ÍM**-port | im-**PÓRT** | "fix the imports / import os" |
| export | **ÉKS**-port | eks-**PÓRT** | "export default" |
| update | **ÁP**-deit | ap-**DÉIT** | "an update / update the deps" |
| upgrade | **ÁP**-greid | ap-**GRÉID** | "upgrade the system" |
| insert | **ÍN**-sert | in-**SÉRT** | "insert a row" |
| progress | **PRÁ**-gres | pro-**GRÉS** | "a progress bar" |
| project | **PRÁ**-yekt | pro-**YÉKT** | "a side project" |
| address | **Á**-dres | a-**DRÉS** | "an IP address / address the issue" |
| increase | **ÍN**-kris | in-**KRÍS** | "increase the timeout" |
| conflict | **KÁN**-flikt | kon-**FLÍKT** | "a merge conflict" |
| contract | **KÁN**-trakt | kon-**TRÁKT** | "an API contract" |
| permit | **PÉR**-mit | per-**MÍT** | "permit access" |
| convert | **KÁN**-vert | kon-**VÉRT** | "convert to int" |

### 🎭 Se escribe igual, suena distinto

| Palabra | Sonido 1 | Sonido 2 | Ejemplo técnico |
|---|---|---|---|
| read | rid (presente) | red (pasado) | "read-only" = **rid**-óunli |
| lead | lid (liderar) | led (plomo) | "tech lead" = tek **lid** |
| live | liv (vivir) | láiv (en vivo) | "live reload" = **láiv** ri-loud |
| close | klouz (cerrar) | klous (cerca) | "close the file" = **klouz** |
| use | iuz (usar) | ius (uso) | "use case" = **ius** keis |
| minute | **MÍ**-nit (minuto) | mai-**NIÚT** (diminuto) | "a minute change" = mai-NIÚT |
| content | **KÁN**-tent (contenido) | kon-**TÉNT** (contento) | "content type" = KÁN-tent |
| invalid | in-**VÁ**-lid (no válido) | **ÍN**-va-lid (persona enferma) | "invalid input" = in-VÁ-lid |
| tear | ter (romper) | tir (lágrima) | "tear down" = **ter** daun |
| row | rou (fila) | rau (pelea) | "a table row" = **rou** |
| resume | ri-**ZÚM** (reanudar) | **RÉ**-zu-mei (currículum) | "send your résumé" |

### 🤫 Letras mudas

| English | Suena | Letra muda | Ejemplo |
|---|---|---|---|
| pseudocode | **SÚ**-dou-koud | p | "write the pseudocode" |
| wrapper / wrap | **RÁ**-per / rap | w | "a wrapper function" |
| write / wrong | rait / rong | w | "write to disk" |
| knowledge / know | **NÁ**-lidy / nou | k | "knowledge base" |
| design / sign | di-**SÁIN** / sain | g | "system design" |
| align / assign | a-**LÁIN** / a-**SÁIN** | g | "assign a value" |
| foreign | **FÓ**-ren | g | "foreign key" |
| column | **KÁ**-lam | n | "add a column" |
| debt | det | b | "tech debt" |
| doubt | daut | b | "no doubt" |
| subtle | **SÁ**-tel | b | "a subtle bug" |
| half | jaf | l | "half the time" |
| could / should / would | kud / shud / uud | l | "it should work" |
| honest / hour | **Á**-nest / áur | h | "an hour ago" |
| island | **ÁI**-land | s | "an island of code" |
| receipt | ri-**SÍT** | p | "payment receipt" |
| often | **Á**-fen o **ÁF**-ten | t (opcional) | "it often fails" |

🇬🇧 Letras para deletrear: A (ei), E (i), I (ái), G (yi), J (yei), H (eich), R (ar), W (dábol-iu), Y (uái), Z (zi en EE. UU., zed en UK), Q (kiú), X (eks).

⚠️ Cuidado: en EE. UU. la letra **o** acentuada casi siempre suena "a" abierta: Docker = DÁ-ker, job = yab, model = MÁ-del, block = blak. Decir "o" española delata el acento al instante.

💡 Consejo: si dudas de una palabra, búscala en YouGlish: te muestra videos reales de nativos diciéndola en contexto técnico.

📌 Resumen: la letra "a" puede sonar a, ei o æ; la "i" puede ser i o ai; la "o" puede ser a, ou o ʌ. Por eso hay que aprender cada palabra con su sonido.

## ⌨️ Leer símbolos en voz alta

En pair programming, en clase o en una entrevista tienes que **dictar código**. Cada símbolo tiene un nombre (y a veces dos: el formal y el de la jerga). Si sabes los nombres, también entiendes cuando otro te dicta.

### 🔣 Paréntesis, llaves y corchetes

| Símbolo | Nombre en inglés | Suena | Cómo se dicta |
|---|---|---|---|
| `( )` | parentheses / parens | pa-**RÉN**-dhe-siz / pa-**RÉNZ** | "open paren… close paren" |
| `(` | parenthesis (singular) | pa-**RÉN**-dhe-sis | "left paren" |
| `[ ]` | square brackets | skuer **BRÁ**-kets | "open bracket, zero, close bracket" |
| `{ }` | curly braces / curly brackets | **KÉR**-li **BRÉI**-siz | "open curly… close curly" |
| `< >` | angle brackets | **ÁN**-guel **BRÁ**-kets | "vector, angle bracket, int" |
| `" "` | double quotes | **DÁ**-bol kuouts | "in double quotes" |
| `' '` | single quotes | **SÍN**-guel kuouts | "single-quoted string" |
| comilla invertida | backtick | **BÁK**-tik | "wrap it in backticks" |

### ➕ Operadores

| Símbolo | Nombre | Se lee en una expresión | Ejemplo leído en voz alta |
|---|---|---|---|
| `=` | equals sign | "equals", "is set to", "gets" | `x = 5` → "x equals five" |
| `==` | double equals | "is equal to", "equals equals" | `a == b` → "a is equal to b" |
| `===` | triple equals | "strictly equals", "triple equals" | `a === b` → "a triple-equals b" |
| `!=` | not equal | "is not equal to", "bang equals" | `x != 0` → "x is not equal to zero" |
| `!` | bang / exclamation mark | "not", "bang" | `!done` → "not done" |
| `&&` | double ampersand | "and" | `a && b` → "a and b" |
| `&` | ampersand | "ampersand", "bitwise and" | `x & 1` → "x bitwise-and one" |
| `||` | double pipe | "or" | `a || b` → "a or b" |
| `|` | pipe / vertical bar | "pipe", "bitwise or" | `ls | grep py` → "ls pipe grep py" |
| `^` | caret | "caret", "xor", "to the power of" | `a ^ b` → "a xor b" |
| `~` | tilde | "tilde", en shell "home" | `~/code` → "home slash code" |
| `<` / `>` | less than / greater than | "less than", "greater than" | `i < n` → "i is less than n" |
| `<=` / `>=` | less/greater than or equal to | "less than or equal to" | `x >= 10` → "x is greater than or equal to ten" |
| `+` / `-` | plus / minus | "plus", "minus" | `n - 1` → "n minus one" |
| `*` | asterisk / star | "times", "star" | `a * b` → "a times b" |
| `/` | slash / forward slash | "divided by", "over", "slash" | `a / b` → "a divided by b" o "a over b" |
| `\` | backslash | "backslash" | `\n` → "backslash n" o "newline" |
| `%` | percent sign | "mod", "modulo", "percent" | `n % 2` → "n mod two" |
| `**` | double star | "to the power of", "star star" | `x ** 2` → "x squared" |
| `//` | double slash | "floor divided by", o comentario | `7 // 2` → "seven floor-div two" |
| `+=` | plus equals | "plus equals", "increment by" | `i += 1` → "i plus-equals one" |
| `++` | plus plus | "plus plus", "increment" | `i++` → "i plus plus" |
| `<<` / `>>` | left / right shift | "shift left", "shift right" | `1 << 3` → "one shifted left by three" |
| `=>` | fat arrow | "arrow", "fat arrow", "maps to" | `x => x * 2` → "x arrow x times two" |
| `->` | arrow / thin arrow | "arrow", "returns" | `-> int` → "returns int" |
| `?` / `:` | question mark / colon | "then… else" | `a ? b : c` → "if a then b else c" |
| `?.` | optional chaining | "question dot", "optional chaining" | `user?.name` → "user, optional name" |
| `??` | nullish coalescing | "double question mark", "or else" | `x ?? 0` → "x, or zero if null" |
| `...` | spread / ellipsis | "spread", "dot dot dot" | `...args` → "spread args" |

### 🔤 Signos sueltos

| Símbolo | Nombre | Suena | Dónde lo oirás |
|---|---|---|---|
| `.` | dot / period / point | dat / **PÍ**-ri-od / point | "dot" en código, "point" en números, "period" al final de frase |
| `,` | comma | **KÁ**-ma | "a comma b" |
| `:` | colon | **KÓU**-lon | "colon at the end of the if" |
| `;` | semicolon | **SÉ**-mi-kou-lon | "missing semicolon" |
| `::` | double colon | **DÁ**-bol **KÓU**-lon | `std::cout` → "std colon colon cout" |
| `#` | hash / pound / number sign | jash / paund | "hash include"; en C# se dice "sharp" |
| `@` | at sign | at | `@property` → "at property" |
| `$` | dollar sign | **DÁ**-ler sain | `$HOME` → "dollar home" |
| `_` | underscore | **ÁN**-der-skor | `my_var` → "my underscore var" |
| `__init__` | dunder init | **DÁN**-der init | "double underscore" abreviado: dunder |
| `-` | dash / hyphen / minus | dash / **JÁI**-fen | `--help` → "dash dash help" |
| `'` | apostrophe / single quote | a-**PÁS**-tro-fi | "it's" lleva apostrophe |
| `&` | ampersand | **ÁM**-per-sand | "and" en nombres: AT&T |
| `*` | asterisk | **ÁS**-te-risk | nunca "asterix" |

💡 Consejo: en código dictado se usa casi siempre la forma corta: "paren", "curly", "bracket", "bang", "dot", "star". Suena natural y rápido.

⚠️ Cuidado: **asterisk** termina en "risk", no "asterix". Y en inglés "#" casi nunca se llama "hashtag" en código: di "hash" o "pound".

## 🔢 Leer código, números, versiones y direcciones

Leer en voz alta una línea completa es un ejercicio clave para entrevistas y pair programming. Además, el inglés escribe los números al revés que nosotros: **la coma separa miles y el punto separa decimales**.

### 🧑‍💻 Líneas de código leídas en voz alta

| Código | Lectura natural | Lectura más literal |
|---|---|---|
| `a[i]` | "a sub i" / "a at index i" | "a, open bracket, i, close bracket" |
| `matrix[i][j]` | "matrix i j" / "the element at row i, column j" | "matrix bracket i bracket j" |
| `obj.prop` | "obj dot prop" | "the prop property of obj" |
| `f(x, y)` | "f of x and y" / "call f with x and y" | "f, open paren, x comma y, close paren" |
| `x = 5` | "x equals five" / "set x to five" | "x gets five" |
| `if x != 0:` | "if x is not zero" | "if x bang-equals zero, colon" |
| `for i in range(10):` | "for i in range ten" | "loop i from zero to nine" |
| `def add(a, b):` | "define add, taking a and b" | "def add, paren a comma b, colon" |
| `return a + b` | "return a plus b" | — |
| `nums[1:3]` | "nums from one to three" | "nums slice one colon three" |
| `arr.length - 1` | "arr dot length minus one" | "the last index" |
| `x ** 2` | "x squared" | "x to the power of two" |
| `x ** n` | "x to the n" / "x to the nth power" | "x star star n" |
| `n % 2 == 0` | "n mod two equals zero" / "n is even" | — |
| `i++` | "i plus plus" / "increment i" | — |
| `const sum = (a, b) => a + b;` | "const sum equals a, b arrow a plus b" | "an arrow function that adds a and b" |
| `user?.name ?? "anon"` | "user's name, or anon if it's null" | "user question-dot name, double question mark, anon" |
| `*args, **kwargs` | "star args, star star kwargs" | "args and keyword args" |
| `std::vector<int>` | "a vector of int" | "std colon colon vector, angle bracket int" |
| `#include <stdio.h>` | "hash include standard I/O dot h" | "pound include stdio dot h" |
| `@app.route("/")` | "at app dot route, slash" | "a route decorator for the root" |
| `ls -la ~/.config` | "ls dash la, home dot config" | "el-es minus el-ei, tilde slash dot config" |
| `git commit -m "fix"` | "git commit dash m, fix" | — |
| `cat log.txt | grep error` | "cat log dot txt, pipe, grep error" | — |
| `0x1F` | "hex one F" | "zero x one F" |
| `x >= 10 && x < 20` | "x is between ten and twenty" | "x greater-or-equal ten and x less than twenty" |
| `O(n log n)` | "O of n log n" / "n log n time" | "big O of n log n" |

### 🔢 Números

| Escrito | Se lee | ⚠️ Nota |
|---|---|---|
| `3.14` | "three point one four" | Tras el punto, dígito por dígito |
| `0.5` | "zero point five" / "point five" | En UK también "nought point five" |
| `1,500` | "one thousand five hundred" / "fifteen hundred" | En inglés **1,500 = mil quinientos**, no 1,5 |
| `1,000,000` | "one million" | La coma separa miles |
| `10^9` / `1B` | "one billion" | **billion = mil millones**, no "billón" |
| `10^12` / `1T` | "one trillion" | trillion = nuestro "billón" |
| `7B` (modelo) | "seven B" / "seven billion parameters" | "a 7B model" |
| `1e6` | "one e six" / "a million" | Notación científica |
| `1e-3` | "one e minus three" / "ten to the minus three" | `lr=1e-3` = "learning rate one e minus three" |
| `2^32` | "two to the thirty-second" | "two to the power of thirty-two" |
| `-5` | "minus five" / "negative five" | — |
| `1/2` · `1/3` · `3/4` | "one half" · "one third" · "three quarters" | — |
| `2x faster` | "two times faster" / "twice as fast" | — |
| `99.9%` | "ninety-nine point nine percent" / "three nines" | "three nines of uptime" |
| `0` | "zero" / "oh" | "oh" en códigos: 404 = "four oh four" |
| `16 GB` | "sixteen gigs" / "sixteen gigabytes" | **GUÍ**-ga-bait, g de "gato" |
| `500 ms` | "five hundred milliseconds" | — |
| `4K` | "four K" | — |
| `1st, 2nd, 3rd, 4th` | "first, second, third, fourth" | Ordinales para fechas y posiciones |

### 🏷️ Versiones, fechas y horas

| Escrito | Se lee | ⚠️ Nota |
|---|---|---|
| `v2.10.3` | "version two point ten point three" | "ten", no "one zero": cada parte es un número |
| `Python 3.12` | "Python three twelve" / "three point twelve" | — |
| `v1.0.0-beta` | "version one point oh, beta" | — |
| `2026` | "twenty twenty-six" | Años se leen en pares |
| `2005` | "two thousand five" / "twenty oh five" | — |
| `the 1990s` | "the nineties" | — |
| `10/19/2026` | "October nineteenth, twenty twenty-six" | EE. UU.: **mes/día/año** |
| `19/10/2026` | "the nineteenth of October" | UK y Bolivia: día/mes/año. Usa ISO para evitar líos |
| `2026-10-19` | "twenty twenty-six, ten, nineteen" | ISO 8601: el formato seguro en código |
| `10:30` | "ten thirty" | — |
| `14:00` | "two p.m." / "fourteen hundred" | En EE. UU. se usa a.m./p.m. |
| `UTC-4` | "UTC minus four" | La hora de Bolivia |
| `Q3` | "Q three" / "the third quarter" | Trimestre |

### 🌐 IPs, URLs, emails y rutas

| Escrito | Se lee | ⚠️ Nota |
|---|---|---|
| `192.168.1.1` | "one ninety-two dot one sixty-eight dot one dot one" | Cada bloque como número |
| `127.0.0.1` | "one twenty-seven dot zero dot zero dot one" / "localhost" | — |
| `localhost:8080` | "localhost port eighty eighty" | "colon" casi nunca se dice |
| `https://api.github.com/users` | "api dot github dot com slash users" | "https colon slash slash" se omite al hablar |
| `www` | "double-u double-u double-u" / "dub dub dub" | — |
| `yafer@mail.com` | "yafer at mail dot com" | @ = "at" |
| `/etc/nginx/nginx.conf` | "slash etc slash nginx slash nginx dot conf" | — |
| `C:\Users\yafer` | "C colon backslash users backslash yafer" | Windows usa backslash |
| `main.py` | "main dot py" | py = "pai" |
| `my-app` | "my dash app" / "my hyphen app" | — |
| `file_name` | "file underscore name" | — |
| `camelCase` | "camel case" | Para describir estilos de nombres |
| `snake_case` / `kebab-case` | "snake case" / "kebab case" | — |
| `404` | "four oh four" | Códigos HTTP: dígito por dígito o "four hundred four" |
| `500` | "five hundred" | "a five hundred error" |

### ✅ Ejemplo resuelto: dictar una línea en una entrevista

Línea: `if len(nums) > 0 and nums[0] % 2 == 0:`

| Paso | Lo que dices |
|---|---|
| Natural | "If nums isn't empty and its first element is even…" |
| Literal | "if len of nums is greater than zero, and nums sub zero mod two equals zero, colon" |
| Para un compañero | "check that the list is non-empty and the first item is even" |

🇬🇧 Frase modelo: "On line twelve, we check whether the list is empty before accessing index zero."

⚠️ Cuidado: el error más caro es leer `1,500` como "uno coma cinco". En inglés **1,500 = 1500** y **1.5 = uno coma cinco**. Lo mismo con "billion": un modelo de "7 billion parameters" tiene **7 mil millones**.

📌 Resumen: punto = "point" en números y "dot" en código y URLs; coma = miles; versiones parte por parte; fechas en ISO.

## 🧱 Vocabulario: tipos y estructuras de datos

Estas palabras salen en cualquier curso, doc o entrevista. Apréndelas directamente en inglés: muchas veces la traducción suena peor y nadie la usa.

### 🔢 Tipos de datos

| English | Suena | Español | Ejemplo real |
|---|---|---|---|
| integer / int | **ÍN**-ti-yer / int | entero | `age = 21` |
| float / double | flout / **DÁ**-bol | decimal de coma flotante | `pi = 3.14` |
| string | string | cadena de texto | `name = "Yafer"` |
| boolean / bool | **BÚ**-li-an / bul | verdadero o falso | `is_ready = True` |
| null / None / nil | nal / nan / nil | nulo | `user = None` |
| undefined | an-di-**FÁIND** | no definido | `let x;` en JS |
| character / char | **KÉ**-rak-ter / char | carácter | `'a'` |
| byte | bait | byte (8 bits) | `b"hello"` |
| bit | bit | bit (0 o 1) | "a 64-bit CPU" |
| signed / unsigned | saind / an-**SÁIND** | con signo / sin signo | `unsigned int` |
| type | taip | tipo | `type(x)` |
| cast | kast | convertir de tipo | `int("42")` |
| primitive | **PRÍ**-mi-tiv | tipo primitivo | `int`, `bool` |
| literal | **LÍ**-te-ral | valor escrito directo | `"hi"` es un string literal |
| mutable / immutable | **MIÚ**-ta-bol / i-**MIÚ**-ta-bol | modificable / no modificable | strings son immutable en Python |
| constant | **KÁNS**-tant | constante | `const MAX = 10` |
| generic | ye-**NÉ**-rik | genérico | `List<T>` |
| type hint / annotation | taip jint / a-no-**TÉI**-shon | anotación de tipo | `def f(x: int) -> str:` |
| overflow | **ÓU**-ver-flou | desbordamiento | "integer overflow" |
| NaN | nan | "no es un número" | `float("nan")`, o `0 / 0` en JS |

### 🧱 Estructuras de datos

| English | Suena | Español | Ejemplo real |
|---|---|---|---|
| array | a-**RÉI** | arreglo | `[1, 2, 3]` |
| list | list | lista | `nums.append(4)` |
| linked list | linkt list | lista enlazada | nodos con `next` |
| doubly linked list | **DÁ**-bli linkt list | lista doblemente enlazada | `prev` y `next` |
| stack | stak | pila (LIFO) | `stack.pop()` |
| queue | kiú | cola (FIFO) | `queue.popleft()` |
| deque | dek | cola de dos extremos | `collections.deque` |
| priority queue | prai-**Ó**-ri-ti kiú | cola de prioridad | `heapq` |
| heap | jip | montículo | `heapq.heappush(h, x)` |
| hash map / hash table | jash map / jash **TÉI**-bol | tabla hash | `{"key": "value"}` |
| dictionary | **DÍK**-sho-ne-ri | diccionario | `dict()` |
| set | set | conjunto sin repetidos | `{1, 2, 3}` |
| tuple | **TÚ**-pol | tupla | `(lat, lon)` |
| tree | tri | árbol | `root`, `leaf`, `child` |
| binary tree | **BÁI**-na-ri tri | árbol binario | `node.left`, `node.right` |
| binary search tree (BST) | **BÁI**-na-ri serch tri | árbol binario de búsqueda | izquierda menor, derecha mayor |
| trie | trai o tri | árbol de prefijos | autocompletado |
| graph | graf | grafo | `nodes` y `edges` |
| node | noud | nodo | `node.value` |
| edge | edy | arista | conexión entre nodos |
| vertex / vertices | **VÉR**-teks / **VÉR**-ti-siz | vértice(s) | otro nombre de node |
| adjacency list | a-**YÉI**-sen-si list | lista de adyacencia | `graph[u] = [v, w]` |
| root / leaf / parent / child | rut / lif / **PÉ**-rent / chaild | raíz / hoja / padre / hijo | partes de un árbol |
| children / leaves | **CHÍL**-dren / livz | hijos / hojas (plural irregular) | "the node's children" |
| sibling | **SÍ**-bling | hermano | nodos con el mismo padre |
| index / indices | **ÍN**-deks / **ÍN**-di-siz | índice(s) | `arr[0]` |
| key / value | ki / **VÁ**-liu | clave / valor | `d.items()` |
| element / item | **É**-le-ment / **ÁI**-tem | elemento | "the first item" |
| length / size | lenkz / saiz | longitud / tamaño | `len(arr)` |
| slice | slais | porción | `arr[1:3]` |
| matrix | **MÉI**-triks | matriz | `grid[i][j]` |
| buffer | **BÁ**-fer | memoria intermedia | "a ring buffer" |
| pointer / reference | **PÓIN**-ter / **RÉ**-fe-rens | puntero / referencia | `int *p` |
| empty / full | **ÉMP**-ti / ful | vacío / lleno | "the stack is empty" |

```arbol
binary tree
  root
    left child
      leaf
      leaf
    right child
      leaf
```

💡 Consejo: los plurales irregulares salen mucho: index → indices, vertex → vertices, matrix → matrices, child → children, leaf → leaves, datum → data, axis → axes.

⚠️ Cuidado: **"arreglo"** en inglés es array, no "arrangement". Y "data" es plural en lo formal ("the data are"), pero en código se usa como singular: "the data is loaded". Las dos se aceptan.

## ⏱️ Vocabulario: algoritmos y complejidad

En entrevistas técnicas tendrás que explicar **cuánto cuesta** tu solución. Este vocabulario es casi obligatorio para LeetCode y para cualquier curso de algoritmos.

### 📈 Big O: cómo decir cada complejidad

| Notación | Se dice | Nombre | Ejemplo típico |
|---|---|---|---|
| `O(1)` | "O of one" | constant time | acceso por índice, buscar en un hash map |
| `O(log n)` | "O of log n" | logarithmic | binary search |
| `O(n)` | "O of n" | linear | recorrer una lista una vez |
| `O(n log n)` | "O of n log n" | linearithmic / "n log n" | merge sort, heapsort |
| `O(n^2)` | "O of n squared" | quadratic | dos bucles anidados |
| `O(n^3)` | "O of n cubed" | cubic | multiplicar matrices de forma ingenua |
| `O(2^n)` | "O of two to the n" | exponential | probar todos los subconjuntos |
| `O(n!)` | "O of n factorial" | factorial | probar todas las permutaciones |
| `O(V + E)` | "O of V plus E" | linear en el grafo | BFS y DFS |

### 🧠 Vocabulario de algoritmos

| English | Suena | Español | Ejemplo real |
|---|---|---|---|
| time complexity | taim kom-**PLÉK**-si-ti | complejidad temporal | "it runs in linear time" |
| space complexity | speis kom-**PLÉK**-si-ti | complejidad espacial | "O of one extra space" |
| worst / best / average case | uerst / best / **Á**-ve-ridy keis | peor / mejor / caso medio | "quicksort is n squared in the worst case" |
| amortized | **Á**-mor-taizd | amortizado | "append is amortized O of one" |
| brute force | brut fors | fuerza bruta | "start with a brute-force solution" |
| naive | nai-**ÍV** | ingenuo, directo | "the naive approach" |
| greedy | **GRÍ**-di | voraz | "a greedy algorithm" |
| divide and conquer | di-**VÁID** and **KÁN**-ker | divide y vencerás | merge sort |
| dynamic programming (DP) | dai-**NÁ**-mik **PRÓU**-gra-ming | programación dinámica | "a DP table" |
| memoization | me-mou-ai-**ZÉI**-shon | memoización | `@cache` |
| recursion / recursive | ri-**KÉR**-zhon / ri-**KÉR**-siv | recursión / recursivo | `fib(n-1) + fib(n-2)` |
| base case | beis keis | caso base | `if n <= 1: return n` |
| backtracking | **BÁK**-tra-king | vuelta atrás | sudoku, N-queens |
| binary search | **BÁI**-na-ri serch | búsqueda binaria | `bisect` |
| two pointers | tu **PÓIN**-ters | dos punteros | `left`, `right` |
| sliding window | **SLÁI**-ding **UÍN**-dou | ventana deslizante | subarray de suma máxima |
| prefix sum | **PRÍ**-fiks sam | suma acumulada | `prefix[i]` |
| breadth-first search (BFS) | bredz ferst serch | búsqueda en anchura | con una queue |
| depth-first search (DFS) | depz ferst serch | búsqueda en profundidad | con recursión o una stack |
| shortest path | **SHÓR**-test paz | camino más corto | Dijkstra |
| topological sort | ta-po-**LÁ**-yi-kal sort | orden topológico | dependencias de paquetes |
| traversal / traverse | tra-**VÉR**-sal / tra-**VÉRS** | recorrido / recorrer | "in-order traversal" |
| sort / sorted | sort / **SÓR**-tid | ordenar / ordenado | `sorted(nums)` |
| stable sort | **STÉI**-bol sort | orden estable | mantiene el orden de los iguales |
| in-place | in-pleis | en el sitio, sin memoria extra | `nums.sort()` |
| swap | suap | intercambiar | `a, b = b, a` |
| hash collision | jash ko-**LÍ**-zhon | colisión de hash | dos claves, mismo hash |
| heuristic | jiu-**RÍS**-tik | heurística | A* search |
| invariant | in-**VÉ**-ri-ant | invariante | "the loop invariant" |
| edge case | ech keis | caso límite | lista vacía, n = 0 |
| bottleneck | **BÁ**-tel-nek | cuello de botella | "the DB is the bottleneck" |
| trade-off | **TRÉID**-of | compromiso, contrapartida | "a time-space trade-off" |
| optimal | **ÁP**-ti-mal | óptimo | "an optimal solution" |
| upper / lower bound | **Á**-per / **LÓU**-er baund | cota superior / inferior | "an upper bound of n squared" |
| scale | skeil | escalar, crecer | "it doesn't scale to a million users" |

🇬🇧 Frase modelo en entrevista: "My first idea is brute force, which is O of n squared. We can do better with a hash map, which brings it down to O of n time and O of n space."

⚠️ Cuidado: "complexity" se pronuncia kom-**PLÉK**-si-ti, con el golpe en "plek". Y "O" se dice "ou", nunca "o" española.

📌 Resumen: di siempre **tiempo y espacio**, el **peor caso** y el **trade-off**; es lo que el entrevistador quiere oír.

## 🧩 Vocabulario: control de flujo, funciones y POO

### 🔀 Control de flujo

| English | Suena | Español | Ejemplo real |
|---|---|---|---|
| if / else / elif | if / els / **É**-lif | si / si no / si no, si | `if x > 0:` |
| condition | kon-**DÍ**-shon | condición | `x == 5` |
| statement | **STÉIT**-ment | sentencia, instrucción | "an if statement" |
| expression | iks-**PRÉ**-shon | expresión | `a + b` |
| loop | lup | bucle | `for`, `while` |
| iterate / iteration | **Í**-te-reit / i-te-**RÉI**-shon | iterar / iteración | "iterate over the list" |
| nested | **NÉS**-tid | anidado | "a nested loop" |
| break / continue | breik / kon-**TÍ**-niu | salir / saltar a la siguiente | `break` |
| infinite loop | **ÍN**-fi-nit lup | bucle infinito | `while True:` sin break |
| branch | branch | rama (de un if) | "the else branch" |
| switch / case / match | suich / keis / mach | selección múltiple | `match command:` |
| ternary | **TÉR**-na-ri | operador ternario | `a if c else b` |
| early return | **ÉR**-li ri-**TÉRN** | salida temprana | `if not x: return` |
| guard clause | gard kloz | cláusula de guarda | comprobar y salir al inicio |
| exception | ik-**SÉP**-shon | excepción | `try` / `except` |
| throw / raise / catch | zrou / reiz / kech | lanzar / lanzar / capturar | `raise ValueError()` |
| finally | **FÁI**-na-li | al final, siempre | `finally: f.close()` |
| short-circuit | short **SÉR**-kit | cortocircuito lógico | `a and b` no evalúa b si a es falso |
| truthy / falsy | **TRÚ**-zi / **FÓL**-si | que cuenta como verdadero / falso | `""` es falsy |

### 🧩 Funciones

| English | Suena | Español | Ejemplo real |
|---|---|---|---|
| function | **FÁNK**-shon | función | `def add(a, b):` |
| argument | **ÁR**-giu-ment | argumento (valor que pasas) | `add(2, 3)` |
| parameter | pa-**RÁ**-mi-ter | parámetro (nombre en la definición) | `a`, `b` |
| keyword argument | **KÍ**-uerd **ÁR**-giu-ment | argumento con nombre | `f(x=1)` |
| default value | di-**FÓLT** **VÁ**-liu | valor por defecto | `def f(x=0):` |
| return value | ri-**TÉRN** **VÁ**-liu | valor de retorno | `return a + b` |
| call / invoke | kol / in-**VÓUK** | llamar | "call the function" |
| signature | **SÍG**-na-cher | firma | `f(x: int) -> str` |
| side effect | said i-**FÉKT** | efecto secundario | escribir en un archivo |
| pure function | piur **FÁNK**-shon | función pura | sin side effects |
| callback | **KÓL**-bak | función que se llama luego | `onClick={handle}` |
| closure | **KLÓU**-zher | clausura | función que recuerda su entorno |
| higher-order function | **JÁI**-er **ÓR**-der **FÁNK**-shon | función de orden superior | `map(f, xs)` |
| decorator | **DÉ**-ko-rei-ter | decorador | `@cache` |
| generator | **YÉ**-ne-rei-ter | generador | `yield` |
| anonymous function | a-**NÁ**-ni-mas **FÁNK**-shon | función anónima | `lambda x: x + 1` |
| recursion | ri-**KÉR**-zhon | recursión | la función se llama a sí misma |
| scope | skoup | ámbito | "global scope" |
| overload | ou-ver-**LÓUD** | sobrecargar | mismo nombre, otros parámetros |

### 🏛️ Programación orientada a objetos (OOP)

| English | Suena | Español | Ejemplo real |
|---|---|---|---|
| class | klas | clase | `class User:` |
| object / instance | **ÁB**-yekt / **ÍNS**-tans | objeto / instancia | `u = User()` |
| instantiate | ins-**TÁN**-shi-eit | instanciar | "instantiate the class" |
| attribute / property / field | **Á**-tri-biut / **PRÁ**-per-ti / fild | atributo / propiedad / campo | `u.name` |
| method | **MÉ**-zad | método | `u.save()` |
| constructor | kon-**STRÁK**-ter | constructor | `__init__` |
| inheritance / inherit | in-**JÉ**-ri-tans / in-**JÉ**-rit | herencia / heredar | `class Admin(User):` |
| parent / base class | **PÉ**-rent / beis klas | clase padre / base | `User` |
| child / subclass | chaild / **SÁB**-klas | clase hija / subclase | `Admin` |
| override | ou-ver-**RÁID** | sobrescribir | redefinir un método heredado |
| encapsulation | in-kap-siu-**LÉI**-shon | encapsulamiento | atributos privados |
| polymorphism | pa-li-**MÓR**-fi-zem | polimorfismo | mismo método, varios tipos |
| abstraction | ab-**STRÁK**-shon | abstracción | ocultar detalles |
| abstract class | **ÁB**-strakt klas | clase abstracta | `ABC` en Python |
| interface | **ÍN**-ter-feis | interfaz | contrato de métodos |
| static method | **STÁ**-tik **MÉ**-zad | método estático | `@staticmethod` |
| getter / setter | **GUÉ**-ter / **SÉ**-ter | lector / modificador | `@property` |
| composition | kam-po-**SÍ**-shon | composición | un objeto que contiene otros |
| design pattern | di-**SÁIN** **PÁ**-tern | patrón de diseño | Singleton, Factory, Observer |
| coupling / cohesion | **KÁ**-pling / kou-**JÍ**-zhon | acoplamiento / cohesión | "loose coupling, high cohesion" |
| dependency injection | di-**PÉN**-den-si in-**YÉK**-shon | inyección de dependencias | pasar la DB al constructor |

💡 Consejo: **argument** vs **parameter**: el parameter es el nombre en la definición (`def f(x)`), el argument es el valor real en la llamada (`f(5)`). En entrevistas se nota si los distingues.

🇬🇧 Frase modelo: "This method overrides the parent class's implementation and raises an exception if the argument is null."

## 🌐 Vocabulario: web, frontend y backend

La web es donde más inglés vas a leer: MDN, docs de frameworks, APIs. Casi todo el vocabulario viene de HTTP, que es una "conversación" entre cliente y servidor.

### 📡 HTTP y la web

| English | Suena | Español | Ejemplo real |
|---|---|---|---|
| request / response | ri-**KUÉST** / ris-**PÁNS** | petición / respuesta | `GET /users` |
| client / server | **KLÁI**-ent / **SÉR**-ver | cliente / servidor | navegador / backend |
| endpoint | **ÉND**-point | punto de acceso de una API | `/api/login` |
| header | **JÉ**-der | cabecera | `Content-Type: application/json` |
| body / payload | **BÁ**-di / **PÉI**-loud | cuerpo / carga útil | el JSON que envías |
| status code | **STÁ**-tus koud | código de estado | `200`, `404` |
| method / verb | **MÉ**-zad / verb | método HTTP | GET, POST, PUT, PATCH, DELETE |
| query string / query param | **KUÍ**-ri string | parámetros de la URL | `?page=2&limit=10` |
| path param | paz pa-**RÁ**-mi-ter | parámetro en la ruta | `/users/42` |
| cookie | **KÚ**-ki | cookie | sesión persistente |
| session | **SÉ**-shon | sesión | "the session expired" |
| token | **TÓU**-ken | credencial | `Authorization: Bearer <token>` |
| domain / subdomain | dou-**MÉIN** / sab-dou-**MÉIN** | dominio / subdominio | `api.example.com` |
| hosting | **JÓUS**-ting | alojamiento | "free hosting" |
| redirect | ri-dai-**RÉKT** | redirección | `301 Moved Permanently` |
| browser | **BRÁU**-zer | navegador | Brave, Firefox |
| static / dynamic | **STÁ**-tik / dai-**NÁ**-mik | estático / dinámico | "a static site" |
| CORS | kors | política de orígenes cruzados | "blocked by CORS policy" |
| websocket | **UÉB**-sa-ket | conexión bidireccional | chat en tiempo real |
| polling | **PÓU**-ling | consultar cada cierto tiempo | "long polling" |

```secuencia
Navegador -> Servidor : GET /users/42
Servidor --> Navegador : 200 OK + JSON
Navegador -> Servidor : GET /users/999
Servidor --> Navegador : 404 Not Found
```

### 🚦 Códigos de estado HTTP que más verás

| Código | Se lee | Nombre | Significa |
|---|---|---|---|
| `200` | "two hundred" | OK | Todo bien |
| `201` | "two oh one" | Created | Se creó el recurso |
| `204` | "two oh four" | No Content | Bien, pero sin cuerpo |
| `301` | "three oh one" | Moved Permanently | Redirección permanente |
| `304` | "three oh four" | Not Modified | Usa tu caché |
| `400` | "four hundred" | Bad Request | La petición está mal formada |
| `401` | "four oh one" | Unauthorized | No estás autenticado (falta login) |
| `403` | "four oh three" | Forbidden | Estás autenticado pero sin permiso |
| `404` | "four oh four" | Not Found | No existe |
| `409` | "four oh nine" | Conflict | Choca con el estado actual |
| `422` | "four twenty-two" | Unprocessable Content | Datos válidos en forma pero no en contenido |
| `429` | "four twenty-nine" | Too Many Requests | Te pasaste del rate limit |
| `500` | "five hundred" | Internal Server Error | El servidor falló |
| `502` | "five oh two" | Bad Gateway | El proxy recibió mala respuesta |
| `503` | "five oh three" | Service Unavailable | Servidor caído o saturado |
| `504` | "five oh four" | Gateway Timeout | El proxy se cansó de esperar |

⚠️ Cuidado: **401 Unauthorized** en realidad significa "no autenticado" (no sé quién eres) y **403 Forbidden** "no autorizado" (sé quién eres, pero no puedes). El nombre de 401 confunde incluso a nativos.

### 🎨 Frontend y UI

| English | Suena | Español | Ejemplo real |
|---|---|---|---|
| component | kom-**PÓU**-nent | componente | `<Button />` |
| props | props | propiedades que recibe | `<Card title="Hi" />` |
| state | steit | estado | `useState(0)` |
| hook | juk | gancho (función especial) | `useEffect` |
| render / re-render | **RÉN**-der / ri-**RÉN**-der | dibujar / volver a dibujar | "it re-renders on every keystroke" |
| DOM | dam | árbol de la página | `document.querySelector()` |
| event listener / handler | i-**VÉNT** **LÍS**-ne-ner / **JÁND**-ler | escuchador / manejador de eventos | `addEventListener("click", f)` |
| layout | **LÉI**-aut | disposición | "a two-column layout" |
| responsive | ris-**PÁN**-siv | adaptable a pantallas | "a responsive navbar" |
| viewport | **VIÚ**-port | área visible | `100vh` |
| breakpoint | **BRÉIK**-point | punto de quiebre (CSS) o de parada (debugger) | `@media (min-width: 768px)` |
| margin / padding / border | **MÁR**-yin / **PÁ**-ding / **BÓR**-der | margen / relleno / borde | `padding: 1rem` |
| font / font weight | fant / fant ueit | fuente / grosor | `font-weight: 700` |
| dark mode | dark moud | modo oscuro | `prefers-color-scheme` |
| accessibility (a11y) | ak-se-si-**BÍ**-li-ti | accesibilidad | `aria-label` |
| tooltip | **TÚL**-tip | globo de ayuda | aparece al pasar el mouse |
| dropdown | **DRÁP**-daun | menú desplegable | `<select>` |
| modal / dialog | **MÓU**-del / **DÁI**-a-log | ventana emergente | "close the modal" |
| toggle | **TÁ**-guel | interruptor | "toggle dark mode" |
| checkbox / radio button | **CHÉK**-baks / **RÉI**-di-ou | casilla / botón de opción | `<input type="checkbox">` |
| input field / placeholder | **ÍN**-put fild / **PLÉIS**-joul-der | campo / texto de ejemplo | `placeholder="Email"` |
| spinner / loader | **SPÍ**-ner / **LÓU**-der | indicador de carga | mientras llega el fetch |
| toast | toust | aviso flotante breve | "Saved!" |
| navbar / sidebar / footer | **NÁV**-bar / **SÁID**-bar / **FÚ**-ter | barra de navegación / lateral / pie | partes de la página |
| hover / focus | **JÁ**-ver / **FÓU**-kas | pasar el mouse / foco | `:hover`, `:focus` |
| scroll | skroul | desplazar | `overflow-y: scroll` |
| bundle / bundler | **BÁN**-del / **BÁND**-ler | paquete / empaquetador | Vite, webpack |
| hydration | jai-**DRÉI**-shon | hidratación (SSR → interactivo) | "hydration mismatch" |

### 🛠️ Backend y APIs

| English | Suena | Español | Ejemplo real |
|---|---|---|---|
| route / handler | rut / **JÁND**-ler | ruta / función que la atiende | `@app.get("/users")` |
| middleware | **MÍ**-del-uer | capa intermedia | auth, logging, CORS |
| controller | kon-**TRÓU**-ler | controlador | MVC |
| business logic | **BÍZ**-nes **LÁ**-yik | lógica de negocio | reglas de la app |
| serialize / deserialize | **SÍ**-ri-a-laiz / di-**SÍ**-ri-a-laiz | convertir a/desde texto o bytes | `json.dumps(obj)` |
| rate limit | reit **LÍ**-mit | límite de peticiones | "100 requests per minute" |
| pagination | pa-yi-**NÉI**-shon | paginación | `?page=2` |
| webhook | **UÉB**-juk | aviso HTTP automático | GitHub avisa a tu server |
| background job / worker | **BÁK**-graund yab / **UÉR**-ker | tarea en segundo plano / proceso trabajador | enviar emails |
| cron job | kran yab | tarea programada | `0 3 * * *` |
| message queue | **MÉ**-sidy kiú | cola de mensajes | RabbitMQ, Kafka |
| microservices / monolith | **MÁI**-krou-ser-vi-siz / **MÁ**-no-liz | microservicios / monolito | arquitectura |
| scalability | skei-la-**BÍ**-li-ti | escalabilidad | "built for scalability" |
| latency / throughput | **LÉI**-ten-si / **ZRÚ**-put | latencia / rendimiento | "p99 latency" |
| versioning | **VÉR**-zho-ning | control de versiones de la API | `/api/v2/` |
| deprecated | **DÉ**-pre-kei-tid | obsoleto, se quitará | "this endpoint is deprecated" |
| backward compatible | **BÁK**-uerd kom-**PÁ**-ti-bol | compatible hacia atrás | no rompe clientes viejos |
| breaking change | **BRÉI**-king cheinj | cambio que rompe | "v3 has breaking changes" |
| idempotent | ai-dem-**PÓU**-tent | idempotente | PUT dos veces = mismo resultado |
| health check | jelz chek | comprobación de salud | `/healthz` |

🇬🇧 Frase modelo: "The endpoint returns a 401 because the token in the Authorization header has expired."

## 🗄️ Vocabulario: bases de datos y Git

### 🗄️ Bases de datos

| English | Suena | Español | Ejemplo real |
|---|---|---|---|
| table / row / column | **TÉI**-bol / rou / **KÁ**-lam | tabla / fila / columna | `users` |
| record / entry | **RÉ**-kord / **ÉN**-tri | registro | una fila |
| primary key | **PRÁI**-me-ri ki | clave primaria | `id` |
| foreign key | **FÓ**-ren ki | clave foránea | `user_id` |
| query | **KUÍ**-ri | consulta | `SELECT * FROM users` |
| clause | kloz | cláusula | "the WHERE clause" |
| join | yoin | unir tablas | `INNER JOIN` |
| aggregate | **Á**-gre-guet | función de agregado | `COUNT`, `SUM`, `AVG` |
| subquery | sab-**KUÍ**-ri | subconsulta | `WHERE id IN (SELECT …)` |
| index | **ÍN**-deks | índice (acelera búsquedas) | `CREATE INDEX` |
| constraint | kon-**STRÉINT** | restricción | `UNIQUE`, `NOT NULL` |
| schema | **SKÍ**-ma | esquema | tablas y tipos |
| migration | mai-**GRÉI**-shon | migración de esquema | `alembic upgrade head` |
| transaction | tran-**ZÁK**-shon | transacción | `BEGIN` … `COMMIT` |
| rollback | **RÓUL**-bak | deshacer | `ROLLBACK` |
| seed | sid | datos iniciales | `seed.sql` |
| normalization | nor-ma-li-**ZÉI**-shon | normalización | evitar datos repetidos |
| view | viú | vista | `CREATE VIEW` |
| stored procedure | stord pro-**SÍ**-yer | procedimiento almacenado | lógica dentro de la DB |
| trigger | **TRÍ**-guer | disparador | se ejecuta al insertar |
| replica | **RÉ**-pli-ka | réplica | "a read replica" |
| sharding | **SHÁR**-ding | partición horizontal | datos repartidos en servidores |
| connection pool | ko-**NÉK**-shon pul | grupo de conexiones | reutilizar conexiones |
| dump / backup | damp / **BÁK**-ap | volcado / copia | `pg_dump` |
| NoSQL / document | nou-es-kiu-**ÉL** / **DÁ**-kiu-ment | no relacional / documento | MongoDB |
| key-value store | ki **VÁ**-liu stor | almacén clave-valor | Redis |
| vector database | **VÉK**-ter **DÉI**-ta-beis | base de datos vectorial | pgvector, para RAG |
| deadlock | **DÉD**-lak | bloqueo mutuo | dos transacciones se esperan |

### 🌿 Git

| English | Suena | Español | Ejemplo real |
|---|---|---|---|
| repository / repo | ri-**PÁ**-zi-to-ri / **RÍ**-pou | repositorio | `git clone` |
| commit | ko-**MÍT** | confirmar, guardar versión | `git commit -m` |
| branch | branch | rama | `git switch -c fix` |
| merge | merdy | fusionar | `git merge dev` |
| rebase | ri-**BÉIS** | reaplicar commits encima | `git rebase main` |
| pull / push | pul / push | traer / subir | `git push` |
| fetch | fech | descargar sin fusionar | `git fetch` |
| clone | kloun | clonar | `git clone <url>` |
| remote / origin | ri-**MÓUT** / **Ó**-ri-yin | remoto / el remoto por defecto | `git remote -v` |
| upstream | **ÁP**-strim | repositorio original | `git pull upstream main` |
| fork | fork | copia propia de un repo ajeno | botón Fork |
| stash | stash | guardar aparte | `git stash` |
| staging area / stage | **STÉI**-ying **É**-ri-a / steidy | zona de preparación | `git add` |
| staged / unstaged / untracked | steidyd / an-**STÉIDYD** / an-**TRÁKT** | preparado / sin preparar / sin seguimiento | `git status` |
| working tree | **UÉR**-king tri | árbol de trabajo | tus archivos actuales |
| HEAD | jed | el commit actual | `git reset HEAD~1` |
| detached HEAD | di-**TÁCHT** jed | HEAD suelto, fuera de rama | tras `git checkout <hash>` |
| conflict | **KÁN**-flikt | conflicto | `<<<<<<< HEAD` |
| resolve | ri-**ZÁLV** | resolver | "resolve the merge conflict" |
| diff | dif | diferencias | `git diff` |
| log / history | lag / **JÍS**-to-ri | historial | `git log --oneline` |
| blame | bleim | ver quién cambió cada línea | `git blame file.py` |
| cherry-pick | **CHÉ**-ri pik | traer un commit suelto | `git cherry-pick abc123` |
| squash | skuash | aplastar varios commits en uno | "squash and merge" |
| amend | a-**MÉND** | corregir el último commit | `git commit --amend` |
| revert / reset | ri-**VÉRT** / ri-**SÉT** | revertir / reiniciar | `git revert abc123` |
| tag / release | tag / ri-**LÍS** | etiqueta / versión publicada | `git tag v1.0.0` |
| fast-forward | fast **FÓR**-uerd | avance rápido | merge sin commit extra |
| hash / SHA | jash / sha | identificador del commit | `a1b2c3d` |
| .gitignore | dat-guit-ig-**NÓR** | archivo de ignorados | `node_modules/` |

⚠️ Cuidado: **commit** lleva el golpe al final (ko-**MÍT**). "KÓ-mit" suena a otra cosa para un nativo. Igual: **resolve** = ri-ZÁLV, **remote** = ri-MÓUT.

## 💻 Vocabulario: terminal, SO, redes y hardware

### 🐧 Terminal y sistema operativo

| English | Suena | Español | Ejemplo real |
|---|---|---|---|
| shell | shel | intérprete de comandos | bash, fish, zsh |
| terminal / console | **TÉR**-mi-nal / **KÁN**-soul | terminal / consola | kitty, Windows Terminal |
| command | ko-**MÁND** | comando | `ls` |
| flag / option | flag / **ÁP**-shon | opción | `-l`, `--help` |
| path | paz | ruta | `/home/yafer` |
| absolute / relative path | **ÁB**-so-lut / **RÉ**-la-tiv paz | ruta absoluta / relativa | `/etc` vs `./src` |
| directory / folder | di-**RÉK**-to-ri / **FÓUL**-der | carpeta | `cd docs` |
| home directory | joum di-**RÉK**-to-ri | carpeta personal | `~` |
| root / superuser | rut / **SÚ**-per-iu-zer | administrador | `sudo` |
| permission | per-**MÍ**-shon | permiso | `chmod +x` |
| environment variable | en-**VÁI**-ron-ment **VÉ**-ri-a-bol | variable de entorno | `$PATH` |
| pipe / redirect | paip / ri-dai-**RÉKT** | tubería / redirigir | `cmd > out.txt` |
| stdin / stdout / stderr | standard in / out / error | entrada / salida / errores | `2>&1` |
| exit code / status | **ÉG**-zit koud | código de salida | `0` = éxito |
| process / PID | **PRÁ**-ses / pi-ai-**DÍ** | proceso / su número | `ps aux` |
| kill / signal | kil / **SÍG**-nal | terminar / señal | `kill -9 1234` |
| background / foreground | **BÁK**-graund / **FÓR**-graund | segundo / primer plano | `cmd &` |
| service / daemon | **SÉR**-vis / **DÍ**-mon | servicio | `systemctl status` |
| kernel | **KÉR**-nel | núcleo del SO | `uname -r` |
| distro | **DÍS**-trou | distribución de Linux | Arch, Debian |
| boot / reboot | but / ri-**BÚT** | arrancar / reiniciar | "it fails on boot" |
| file system | fail **SÍS**-tem | sistema de archivos | ext4, btrfs |
| mount / unmount | maunt / an-**MÁUNT** | montar / desmontar | `mount /dev/sdb1 /mnt` |
| symlink | **SÍM**-link | enlace simbólico | `ln -s` |
| dotfile / hidden file | **DÁT**-fail / **JÍ**-den fail | archivo oculto | `.bashrc` |
| executable | ig-**ZÉ**-kiu-ta-bol | ejecutable | `./run.sh` |
| wildcard / glob | **UÁILD**-kard / glab | comodín | `*.py` |
| tab completion | tab kom-**PLÍ**-shon | autocompletar con Tab | — |
| package manager | **PÁ**-kidy **MÁ**-ne-yer | gestor de paquetes | `pacman`, `pip`, `npm` |
| dependency | di-**PÉN**-den-si | dependencia | `requirements.txt` |
| clipboard | **KLÍP**-bord | portapapeles | `wl-copy` |
| shortcut / keybinding | **SHÓRT**-kat / **KÍ**-bain-ding | atajo de teclado | `Ctrl+C` |
| workspace | **UÉRK**-speis | escritorio virtual | Hyprland workspaces |

### 🌍 Redes

| English | Suena | Español | Ejemplo real |
|---|---|---|---|
| IP address | ai-pi **Á**-dres | dirección IP | `192.168.1.10` |
| subnet | **SÁB**-net | subred | `/24` |
| gateway | **GUÉIT**-uei | puerta de enlace | el router |
| router / switch | **RÁU**-ter / suich | enrutador / conmutador | — |
| host / hostname | joust / **JÓUST**-neim | equipo / nombre del equipo | `localhost` |
| port | port | puerto | `:443` |
| firewall | **FÁIR**-uol | cortafuegos | `ufw allow 22` |
| packet | **PÁ**-ket | paquete | "packet loss" |
| protocol | **PRÓU**-to-kal | protocolo | TCP, UDP, HTTP |
| handshake | **JÁND**-sheik | saludo inicial | "TLS handshake" |
| bandwidth | **BÁND**-uidz | ancho de banda | "100 Mbps" |
| latency / ping | **LÉI**-ten-si / ping | latencia | "high ping" |
| timeout | **TÁIM**-aut | tiempo agotado | "connection timed out" |
| proxy / reverse proxy | **PRÁK**-si / ri-**VÉRS** **PRÁK**-si | intermediario / proxy inverso | nginx delante de tu app |
| load balancer | loud **BÁ**-lan-ser | balanceador de carga | reparte el tráfico |
| socket | **SÁ**-ket | conector de red | `socket.connect()` |
| upload / download | **ÁP**-loud / **DÁUN**-loud | subir / bajar | — |
| peer-to-peer | pir tu pir | entre iguales | BitTorrent |
| DNS lookup | di-en-es **LÚK**-ap | resolver un nombre | `dig example.com` |

### 🖥️ Hardware

| English | Suena | Español | Ejemplo real |
|---|---|---|---|
| CPU / core | si-pi-**IÚ** / kor | procesador / núcleo | "an 8-core CPU" |
| thread (hardware) | zred | hilo | "16 threads" |
| clock speed | klak spid | frecuencia | "3.5 GHz" = "three point five gigahertz" |
| GPU / VRAM | yi-pi-**IÚ** / **VÍ**-ram | tarjeta gráfica / su memoria | "24 GB of VRAM" |
| RAM / memory | ram / **MÉ**-mo-ri | memoria | "16 gigs of RAM" |
| storage / drive / disk | **STÓ**-ridy / draiv / disk | almacenamiento / unidad / disco | SSD, HDD |
| motherboard | **MÁ**-dher-bord | placa base | — |
| power supply (PSU) | **PÁU**-er sa-**PLÁI** | fuente de poder | "a 750 W PSU" |
| fan / heatsink | fan / **JÍT**-sink | ventilador / disipador | — |
| overheating / thermal throttling | ou-ver-**JÍ**-ting / **ZÉR**-mal **ZRÁ**-tling | sobrecalentamiento / bajada de frecuencia por calor | laptop lenta al jugar |
| firmware / BIOS | **FÉRM**-uer / **BÁI**-os | firmware / BIOS | "update the BIOS" |
| driver | **DRÁI**-ver | controlador | "an NVIDIA driver" |
| peripheral | pe-**RÍ**-fe-ral | periférico | teclado, mouse |
| keyboard / mouse / mice | **KÍ**-bord / maus / mais | teclado / ratón / ratones | — |
| battery / charger | **BÁ**-te-ri / **CHÁR**-yer | batería / cargador | — |
| port / cable | port / **KÉI**-bol | puerto / cable | USB-C, HDMI |
| chip / transistor | chip / tran-**ZÍS**-ter | chip / transistor | — |
| register | **RÉ**-yis-ter | registro (de CPU) | `eax` |
| cache L1 / L2 | kash el-uan / el-tu | caché de CPU | — |
| benchmark | **BÉNCH**-mark | prueba de rendimiento | "run a benchmark" |

## 🔐 Vocabulario: seguridad, nube, DevOps y testing

### 🔐 Seguridad

| English | Suena | Español | Ejemplo real |
|---|---|---|---|
| authentication (authn) | o-zen-ti-**KÉI**-shon | autenticación (quién eres) | login |
| authorization (authz) | o-zo-ri-**ZÉI**-shon | autorización (qué puedes hacer) | roles |
| credentials | kre-**DÉN**-shalz | credenciales | usuario y contraseña |
| password / passphrase | **PÁS**-uerd / **PÁS**-freiz | contraseña / frase de paso | — |
| hash / salt | jash / solt | resumen / sal | bcrypt |
| encryption / encrypt | in-**KRÍP**-shon / in-**KRÍPT** | cifrado / cifrar | AES |
| decrypt | di-**KRÍPT** | descifrar | — |
| plaintext / ciphertext | **PLÉIN**-tekst / **SÁI**-fer-tekst | texto plano / cifrado | — |
| public / private key | **PÁ**-blik / **PRÁI**-vet ki | clave pública / privada | `id_ed25519.pub` |
| certificate | ser-**TÍ**-fi-ket | certificado | Let's Encrypt |
| vulnerability | val-ne-ra-**BÍ**-li-ti | vulnerabilidad | CVE |
| exploit | **ÉKS**-ploit / iks-**PLÓIT** | explotar un fallo | sustantivo / verbo |
| patch | pach | parche | "a security patch" |
| SQL injection | és-kiu-él in-**YÉK**-shon | inyección SQL | `' OR 1=1 --` |
| sanitize / escape | **SÁ**-ni-taiz / is-**KÉIP** | limpiar / escapar | entrada de usuario |
| leak / breach | lik / brich | fuga / brecha | "a data breach" |
| phishing / malware | **FÍ**-shing / **MÁL**-uer | suplantación / software malicioso | — |
| brute-force attack | brut fors a-**TÁK** | ataque de fuerza bruta | probar contraseñas |
| two-factor auth (2FA) | tu **FÁK**-ter oz | doble factor | código del celular |
| least privilege | list **PRÍ**-vi-lidy | mínimo privilegio | solo los permisos necesarios |
| sandbox | **SÁND**-baks | entorno aislado | — |
| secret | **SÍ**-kret | secreto (clave, token) | `.env` |

### ☁️ Nube y DevOps

| English | Suena | Español | Ejemplo real |
|---|---|---|---|
| cloud | klaud | nube | AWS, GCP, Azure |
| instance / VM | **ÍNS**-tans / vi-**ÉM** | instancia / máquina virtual | EC2 |
| container | kon-**TÉI**-ner | contenedor | Docker |
| image / registry | **Í**-midy / **RÉ**-yis-tri | imagen / registro | Docker Hub |
| cluster | **KLÁS**-ter | clúster | Kubernetes |
| pod | pad | pod | la unidad mínima en k8s |
| orchestration | or-kes-**TRÉI**-shon | orquestación | Kubernetes |
| environment | en-**VÁI**-ron-ment | entorno | dev, staging, prod |
| staging / production | **STÉI**-ying / pro-**DÁK**-shon | preproducción / producción | "it works in staging" |
| pipeline | **PÁIP**-lain | tubería de CI/CD | GitHub Actions |
| build / artifact | bild / **ÁR**-ti-fakt | compilación / resultado | `dist/` |
| release / rollout | ri-**LÍS** / **RÓUL**-aut | publicación / despliegue gradual | — |
| deploy / deployment | di-**PLÓI** / di-**PLÓI**-ment | desplegar / despliegue | "deploy to prod" |
| scale up / scale out | skeil ap / skeil aut | escalar vertical / horizontal | más CPU / más máquinas |
| autoscaling | **Ó**-tou-skei-ling | escalado automático | — |
| uptime / downtime | **ÁP**-taim / **DÁUN**-taim | tiempo activo / caído | "99.9% uptime" |
| outage / incident | **ÁU**-tidy / **ÍN**-si-dent | caída / incidente | "a major outage" |
| monitoring / alert | **MÁ**-ni-to-ring / a-**LÉRT** | monitoreo / alerta | Grafana |
| logging / logs | **LÁ**-guing / lagz | registro / registros | `journalctl` |
| on-call | an-kol | de guardia | atender incidentes |
| serverless | **SÉR**-ver-les | sin servidor propio | AWS Lambda |
| region | **RÍ**-yon | región | `us-east-1` |
| bucket | **BÁ**-ket | contenedor de archivos | S3 bucket |
| provisioning | pro-**VÍ**-zho-ning | aprovisionar recursos | Terraform |
| infrastructure as code | **ÍN**-fra-strak-cher az koud | infraestructura como código | IaC |

### 🧪 Testing

| English | Suena | Español | Ejemplo real |
|---|---|---|---|
| unit test | **IÚ**-nit test | prueba unitaria | `def test_add():` |
| integration test | in-te-**GRÉI**-shon test | prueba de integración | API + DB |
| end-to-end test (E2E) | end tu end test | prueba de punta a punta | Playwright |
| test case / test suite | test keis / test suit | caso / conjunto de pruebas | — |
| assertion / assert | a-**SÉR**-shon / a-**SÉRT** | afirmación | `assert x == 2` |
| mock / stub | mak / stab | doble falso | `unittest.mock` |
| fixture | **FÍKS**-cher | dato o estado preparado | `@pytest.fixture` |
| coverage | **KÁ**-ve-ridy | cobertura | "80% coverage" |
| regression | ri-**GRÉ**-shon | regresión (algo que volvió a fallar) | "a regression in v2" |
| flaky test | **FLÉI**-ki test | prueba inestable | falla a veces |
| pass / fail | pas / feil | pasar / fallar | "all tests pass" |
| happy path | **JÁ**-pi paz | caso normal sin errores | — |
| smoke test | smouk test | prueba rápida básica | "does it even start?" |
| test-driven development | test **DRÍ**-ven di-**VÉ**-lop-ment | TDD | test primero |
| linter / type checker | **LÍN**-ter / taip **CHÉ**-ker | analizador de estilo / de tipos | ruff, mypy |
| reproduce / repro | ri-pro-**DIÚS** / **RÍ**-prou | reproducir | "a minimal repro" |

🇬🇧 Frase modelo: "The deploy failed in staging because a flaky integration test timed out, so we rolled back."

## 🤖 Vocabulario: IA, Machine Learning y datos

Es tu carrera: los papers, cursos y librerías de IA están **solo en inglés**, y muchas palabras ni siquiera tienen traducción estable al español. Aprende estas tal cual.

### 📊 Datos y preparación

| English | Suena | Español | Ejemplo real |
|---|---|---|---|
| dataset | **DÉI**-ta-set | conjunto de datos | MNIST, ImageNet |
| sample / data point | **SÁM**-pol / **DÉI**-ta point | muestra / ejemplo | una fila del dataset |
| feature | **FÍ**-cher | característica, variable de entrada | edad, precio |
| label / target | **LÉI**-bel / **TÁR**-guet | etiqueta / variable objetivo | "cat", "dog" |
| ground truth | graund truz | la respuesta correcta real | etiquetas humanas |
| annotation | a-no-**TÉI**-shon | anotación | etiquetar imágenes |
| train / validation / test split | trein / va-li-**DÉI**-shon / test split | división entrenamiento / validación / prueba | 80/10/10 |
| data cleaning | **DÉI**-ta **KLÍ**-ning | limpieza de datos | quitar nulos |
| missing values | **MÍ**-sing **VÁ**-liuz | valores faltantes | `df.isna()` |
| outlier | **ÁUT**-lai-er | valor atípico | un precio de 1e9 |
| normalization / scaling | nor-ma-li-**ZÉI**-shon / **SKÉI**-ling | normalización / escalado | `StandardScaler` |
| one-hot encoding | uan-hat in-**KÓU**-ding | codificación one-hot | `[0, 1, 0]` |
| data augmentation | **DÉI**-ta og-men-**TÉI**-shon | aumento de datos | rotar imágenes |
| imbalanced dataset | im-**BÁ**-lanst **DÉI**-ta-set | dataset desbalanceado | 99% de una clase |
| feature engineering | **FÍ**-cher en-yi-**NÍ**-ring | ingeniería de características | crear columnas nuevas |
| pipeline | **PÁIP**-lain | flujo de procesos | `sklearn.pipeline` |
| DataFrame | **DÉI**-ta-freim | tabla de pandas | `df.head()` |
| data leakage | **DÉI**-ta **LÍ**-kidy | fuga de datos | info del test en el train |

### 🏋️ Entrenamiento

| English | Suena | Español | Ejemplo real |
|---|---|---|---|
| model | **MÁ**-del | modelo | `model = Net()` |
| training / train | **TRÉI**-ning / trein | entrenamiento / entrenar | `model.fit()` |
| inference | **ÍN**-fe-rens | inferencia (usar el modelo) | `model.predict()` |
| weights / parameters | ueits / pa-**RÁ**-mi-terz | pesos / parámetros | lo que el modelo aprende |
| bias | **BÁI**-as | sesgo (término o prejuicio) | `y = wx + b` |
| hyperparameter | jai-per-pa-**RÁ**-mi-ter | hiperparámetro | lo eliges tú |
| loss function | los **FÁNK**-shon | función de pérdida | cross-entropy |
| optimizer | **ÁP**-ti-mai-zer | optimizador | Adam, SGD |
| gradient descent | **GRÉI**-di-ent di-**SÉNT** | descenso de gradiente | — |
| backpropagation | bak-pra-pa-**GUÉI**-shon | retropropagación | `loss.backward()` |
| learning rate | **LÉR**-ning reit | tasa de aprendizaje | `lr=1e-3` |
| epoch | **É**-pak | época (una pasada por los datos) | `epochs=10` |
| batch / batch size | bach / bach saiz | lote / tamaño de lote | `batch_size=32` |
| iteration / step | i-te-**RÉI**-shon / step | iteración / paso | un batch procesado |
| converge | kon-**VÉRDY** | converger | "the loss converges" |
| overfitting | ou-ver-**FÍ**-ting | sobreajuste (memoriza) | train 99%, test 60% |
| underfitting | an-der-**FÍ**-ting | subajuste (no aprende) | malo en ambos |
| regularization | re-giu-la-ri-**ZÉI**-shon | regularización | L2, weight decay |
| dropout | **DRÁP**-aut | apagar neuronas al azar | `nn.Dropout(0.5)` |
| early stopping | **ÉR**-li **STÁ**-ping | parada temprana | cuando val loss sube |
| checkpoint | **CHÉK**-point | punto de guardado | `model.pt` |
| fine-tuning | fain **TÚ**-ning | ajuste fino | adaptar un modelo preentrenado |
| pretrained | pri-**TRÉIND** | preentrenado | `from_pretrained()` |
| transfer learning | **TRÁNS**-fer **LÉR**-ning | aprendizaje por transferencia | — |
| vanishing gradient | **VÁ**-ni-shing **GRÉI**-di-ent | gradiente que desaparece | redes muy profundas |
| exploding gradient | iks-**PLÓU**-ding **GRÉI**-di-ent | gradiente que explota | `clip_grad_norm_` |

### 🧠 Arquitecturas y tipos de aprendizaje

| English | Suena | Español | Ejemplo real |
|---|---|---|---|
| neural network | **NÚ**-ral **NÉT**-uerk | red neuronal | — |
| neuron / layer | **NÚ**-ran / **LÉI**-er | neurona / capa | `nn.Linear(784, 128)` |
| hidden layer | **JÍ**-den **LÉI**-er | capa oculta | — |
| activation function | ak-ti-**VÉI**-shon **FÁNK**-shon | función de activación | ReLU, sigmoid |
| convolutional (CNN) | kan-vo-**LÚ**-sho-nal | convolucional | imágenes |
| recurrent (RNN, LSTM) | ri-**KÉ**-rent | recurrente | secuencias |
| transformer | trans-**FÓR**-mer | transformer | GPT, BERT |
| attention / self-attention | a-**TÉN**-shon | atención | "attention is all you need" |
| encoder / decoder | in-**KÓU**-der / di-**KÓU**-der | codificador / decodificador | — |
| embedding | im-**BÉ**-ding | vector que representa algo | texto → números |
| latent space | **LÉI**-tent speis | espacio latente | VAEs |
| diffusion model | di-**FIÚ**-zhon **MÁ**-del | modelo de difusión | Stable Diffusion |
| GAN | gan | red generativa adversarial | generador vs discriminador |
| supervised / unsupervised | **SÚ**-per-vaizd / an-**SÚ**-per-vaizd | supervisado / no supervisado | con o sin labels |
| reinforcement learning | ri-in-**FÓRS**-ment **LÉR**-ning | aprendizaje por refuerzo | agente, reward |
| agent / reward / policy | **ÉI**-yent / ri-**UÓRD** / **PÁ**-li-si | agente / recompensa / política | RL |
| classification / regression | kla-si-fi-**KÉI**-shon / ri-**GRÉ**-shon | clasificación / regresión | categoría vs número |
| clustering | **KLÁS**-te-ring | agrupamiento | k-means |
| decision tree / random forest | di-**SÍ**-zhon tri / **RÁN**-dom **FÓ**-rest | árbol de decisión / bosque aleatorio | — |

### 💬 LLMs y procesamiento de lenguaje

| English | Suena | Español | Ejemplo real |
|---|---|---|---|
| large language model | lardy **LÁN**-guidy **MÁ**-del | modelo de lenguaje grande | LLM |
| token / tokenizer | **TÓU**-ken / **TÓU**-ke-nai-zer | token / tokenizador | `tokenizer.encode()` |
| context window | **KÁN**-tekst **UÍN**-dou | ventana de contexto | "200K tokens" |
| prompt / prompting | prampt / **PRÁMP**-ting | instrucción / dar instrucciones | — |
| system prompt | **SÍS**-tem prampt | instrucción de sistema | rol del asistente |
| few-shot / zero-shot | fiú shat / **ZÍ**-rou shat | con pocos / sin ejemplos | ejemplos en el prompt |
| chain of thought | chein av zat | cadena de razonamiento | "think step by step" |
| hallucination | ja-lu-si-**NÉI**-shon | alucinación | inventa datos |
| retrieval | ri-**TRÍ**-val | recuperación | la R de RAG |
| chunk / chunking | chank / **CHÁN**-king | fragmento / fragmentar | trocear documentos |
| temperature | **TÉM**-pe-ra-cher | temperatura (aleatoriedad) | `temperature=0.7` |
| sampling | **SÁM**-pling | muestreo | top-k, top-p |
| logits | **LÓU**-yits | puntuaciones antes del softmax | `outputs.logits` |
| next-token prediction | nekst **TÓU**-ken pri-**DÍK**-shon | predicción del siguiente token | — |
| alignment | a-**LÁIN**-ment | alineamiento | RLHF |
| quantization | kuan-ti-**ZÉI**-shon | cuantización | 4-bit, GGUF |
| distillation | dis-ti-**LÉI**-shon | destilación | modelo pequeño aprende de uno grande |
| benchmark / eval | **BÉNCH**-mark / i-**VÁL** | prueba estándar / evaluación | MMLU |
| tool use / function calling | tul ius / **FÁNK**-shon **KÓ**-ling | uso de herramientas | agentes |
| knowledge cutoff | **NÁ**-lidy **KÁT**-of | fecha límite de conocimiento | — |

### 📏 Evaluación

| English | Suena | Español | Ejemplo real |
|---|---|---|---|
| accuracy | **Á**-kiu-ra-si | exactitud | aciertos / total |
| precision | pri-**SÍ**-zhon | precisión | de los positivos predichos, cuántos son reales |
| recall | **RÍ**-kol | exhaustividad, sensibilidad | de los positivos reales, cuántos encontraste |
| F1 score | ef-uan skor | media armónica de precisión y recall | — |
| confusion matrix | kon-**FIÚ**-zhon **MÉI**-triks | matriz de confusión | TP, FP, TN, FN |
| true / false positive | tru / fols **PÁ**-zi-tiv | verdadero / falso positivo | — |
| baseline | **BÉIS**-lain | modelo de referencia | "beats the baseline" |
| cross-validation | kros va-li-**DÉI**-shon | validación cruzada | k-fold |
| ROC curve / AUC | rak kerv / ei-iu-**SÍ** | curva ROC / área bajo la curva | — |
| generalize | **YÉ**-ne-ra-laiz | generalizar | funcionar con datos nuevos |

⚠️ Cuidado: **precision** no es "precisión" en general: en ML es una métrica concreta. Y **accuracy** no es "precisión" sino "exactitud". Confundirlas en una entrevista de ML es un error clásico.

📌 En ML, **weights** y **parameters** suelen ser lo mismo (lo que el modelo aprende); los **hyperparameters** los fijas tú antes de entrenar.

🇬🇧 Frase modelo: "The model overfits after epoch five, so I added dropout and early stopping, and validation accuracy went up to 92 percent."

## 📐 Vocabulario: matemáticas para IA

Los cursos de IA asumen álgebra lineal, cálculo y probabilidad **en inglés**. Saber leer las fórmulas en voz alta te ayuda a seguir los videos de 3Blue1Brown o StatQuest y los papers.

### 🧮 Álgebra lineal

| English | Suena | Español | Ejemplo real |
|---|---|---|---|
| scalar | **SKÉI**-ler | escalar | `3.0` |
| vector | **VÉK**-ter | vector | `[1, 2, 3]` |
| matrix / matrices | **MÉI**-triks / **MÉI**-tri-siz | matriz / matrices | `np.eye(3)` |
| tensor | **TÉN**-ser | tensor | `torch.zeros(2, 3, 4)` |
| dimension / shape | dai-**MÉN**-shon / sheip | dimensión / forma | `x.shape` |
| row / column vector | rou / **KÁ**-lam **VÉK**-ter | vector fila / columna | — |
| dot product | dat **PRÁ**-dakt | producto punto | `a @ b` |
| cross product | kros **PRÁ**-dakt | producto cruz | `np.cross` |
| matrix multiplication | **MÉI**-triks mal-ti-pli-**KÉI**-shon | multiplicación de matrices | `A @ B` |
| transpose | trans-**PÓUZ** | traspuesta | `A.T` |
| inverse | in-**VÉRS** | inversa | `np.linalg.inv(A)` |
| identity matrix | ai-**DÉN**-ti-ti **MÉI**-triks | matriz identidad | `np.eye(n)` |
| determinant | di-**TÉR**-mi-nant | determinante | `np.linalg.det(A)` |
| eigenvalue / eigenvector | **ÁI**-guen-va-liu / **ÁI**-guen-vek-ter | valor / vector propio | PCA |
| rank | rank | rango | — |
| norm | norm | norma | `np.linalg.norm(v)` |
| linear combination | **LÍ**-ni-er kam-bi-**NÉI**-shon | combinación lineal | — |
| span / basis | span / **BÉI**-sis | espacio generado / base | — |
| orthogonal | or-**ZÁ**-go-nal | ortogonal | producto punto = 0 |
| element-wise | **É**-le-ment uaiz | elemento a elemento | `a * b` en NumPy |
| broadcasting | **BRÓD**-kas-ting | expansión automática de formas | NumPy |

### 📉 Cálculo y optimización

| English | Suena | Español | Ejemplo real |
|---|---|---|---|
| function | **FÁNK**-shon | función | f(x) = "f of x" |
| derivative | di-**RÍ**-va-tiv | derivada | f'(x) = "f prime of x" |
| partial derivative | **PÁR**-shal di-**RÍ**-va-tiv | derivada parcial | ∂f/∂x = "partial f partial x" |
| gradient | **GRÉI**-di-ent | gradiente | ∇f = "nabla f" / "grad f" |
| chain rule | chein rul | regla de la cadena | base de backprop |
| slope | sloup | pendiente | — |
| integral | **ÍN**-te-gral | integral | — |
| limit | **LÍ**-mit | límite | "as x approaches zero" |
| minimum / maximum | **MÍ**-ni-mam / **MÁK**-si-mam | mínimo / máximo | "a local minimum" |
| local vs global minimum | **LÓU**-kal / **GLÓU**-bal | mínimo local / global | — |
| convex | kan-**VÉKS** | convexo | un solo mínimo |
| saddle point | **SÁ**-del point | punto de silla | — |
| exponent / exponential | iks-**PÓU**-nent / eks-po-**NÉN**-shal | exponente / exponencial | e^x |
| logarithm / log | **LÁ**-ga-ri-dhem / lag | logaritmo | `np.log` |
| sum / summation | sam / sa-**MÉI**-shon | suma / sumatoria | ∑ = "the sum of" |
| product | **PRÁ**-dakt | producto | ∏ |
| sigmoid / softmax | **SÍG**-moid / **SÓFT**-maks | sigmoide / softmax | — |
| ReLU | **RÉ**-lu | unidad lineal rectificada | `max(0, x)` |

### 🎲 Probabilidad y estadística

| English | Suena | Español | Ejemplo real |
|---|---|---|---|
| probability | pra-ba-**BÍ**-li-ti | probabilidad | P(A) = "probability of A" |
| conditional probability | kon-**DÍ**-sho-nal | probabilidad condicional | P(A given B) |
| random variable | **RÁN**-dom **VÉ**-ri-a-bol | variable aleatoria | — |
| distribution | dis-tri-**BIÚ**-shon | distribución | — |
| normal / Gaussian | **NÓR**-mal / **GÁU**-si-an | normal / gaussiana | campana |
| uniform | **IÚ**-ni-form | uniforme | `np.random.rand` |
| mean / median / mode | min / **MÍ**-di-an / moud | media / mediana / moda | — |
| variance | **VÉ**-ri-ans | varianza | σ² = "sigma squared" |
| standard deviation | **STÁN**-dard di-vi-**ÉI**-shon | desviación estándar | σ |
| expected value | iks-**PÉK**-tid **VÁ**-liu | valor esperado | E[X] |
| likelihood | **LÁIK**-li-jud | verosimilitud | maximum likelihood |
| prior / posterior | **PRÁI**-er / pas-**TÍ**-ri-er | a priori / a posteriori | Bayes |
| Bayes' theorem | **BÉI**-ziz **ZÍ**-rem | teorema de Bayes | — |
| independent | in-di-**PÉN**-dent | independiente | — |
| sample / population | **SÁM**-pol / pa-piu-**LÉI**-shon | muestra / población | — |
| correlation / covariance | ko-re-**LÉI**-shon / kou-**VÉ**-ri-ans | correlación / covarianza | — |
| hypothesis / hypotheses | jai-**PÁ**-ze-sis / jai-**PÁ**-ze-siz | hipótesis (sing. / pl.) | p-value |
| entropy / cross-entropy | **ÉN**-tro-pi / kros **ÉN**-tro-pi | entropía / entropía cruzada | loss de clasificación |
| Euclidean distance | iu-**KLÍ**-di-an **DÍS**-tans | distancia euclidiana | — |
| cosine similarity | **KÓU**-sain si-mi-**LÁ**-ri-ti | similitud coseno | embeddings |

### 🔣 Leer fórmulas y letras griegas

| Escrito | Se lee | Suena | Dónde aparece |
|---|---|---|---|
| x² / x³ | "x squared" / "x cubed" | — | — |
| xᵢ | "x sub i" | — | elemento i |
| x̂ / ŷ | "x hat" / "y hat" | — | predicción |
| x̄ | "x bar" | — | media |
| f'(x) | "f prime of x" | — | derivada |
| ∑ᵢ | "the sum over i" | — | sumatoria |
| ∂ | "partial" | **PÁR**-shal | derivada parcial |
| ∇ | "nabla" / "del" / "grad" | **NÁ**-bla | gradiente |
| ∈ | "in" / "is an element of" | — | x ∈ ℝ = "x in R" |
| ≈ / ≠ | "approximately" / "not equal to" | — | — |
| → | "tends to" / "maps to" | — | límites |
| π | pi | **pai** (no "pi") | — |
| α / β / γ | alpha / beta / gamma | **ÁL**-fa / **BÉI**-ta / **GÁ**-ma | learning rate, momentum |
| θ | theta | **ZÉI**-ta | parámetros del modelo |
| λ | lambda | **LÁM**-da | regularización |
| σ / μ | sigma / mu | **SÍG**-ma / miú | desviación / media |
| ε | epsilon | **ÉP**-si-lan | número muy pequeño |
| η | eta | **ÉI**-ta | learning rate |
| Δ / δ | delta | **DÉL**-ta | cambio |
| φ / ψ / χ | phi / psi / chi | fai / sai / kai | — |
| ρ / τ / ω | rho / tau / omega | rou / tau / ou-**MÉI**-ga | — |

⚠️ Cuidado: en inglés **π se dice "pai"**, **β "béita"**, **θ "zéita"**, **μ "miú"**. Si dices "pi" o "beta" a la española, en un video no reconocerás la letra cuando el profesor la nombre.

## 🧬 Familias de palabras, prefijos y sufijos

El inglés técnico construye palabras como piezas de LEGO: raíz + prefijo + sufijo. Si conoces las piezas, entiendes palabras nuevas sin diccionario y nombras mejor tus variables.

### 🌳 Una raíz, muchas palabras

| Verbo | Quién/qué lo hace | El proceso | Adjetivo | Ejemplo en código |
|---|---|---|---|---|
| parse | parser | parsing | parsable | `parser.parse(text)` |
| compile | compiler | compilation | compiled | "a compiled language" |
| execute | executor | execution | executable | `ThreadPoolExecutor` |
| validate | validator | validation | valid / invalid | `validator.validate(data)` |
| serialize | serializer | serialization | serializable | `UserSerializer` |
| initialize | initializer | initialization | initial | `__init__` |
| optimize | optimizer | optimization | optimal | `torch.optim` |
| iterate | iterator | iteration | iterable | `iter(xs)` |
| deploy | deployer | deployment | deployable | "a deployable artifact" |
| configure | configurator | configuration | configurable | `config.yaml` |
| authenticate | authenticator | authentication | authentic | `authenticate(user)` |
| encrypt | encryptor | encryption | encrypted | "encrypted at rest" |
| allocate | allocator | allocation | allocated | `malloc` |
| install | installer | installation | installable | "the installer" |
| render | renderer | rendering | renderable | `renderer.render()` |
| schedule | scheduler | scheduling | scheduled | "a scheduled job" |
| connect | connector | connection | connected | `db.connect()` |
| compute | computer | computation | computable | "computationally expensive" |
| predict | predictor | prediction | predictable | `model.predict(X)` |
| train | trainer | training | trainable | `Trainer(model)` |
| tokenize | tokenizer | tokenization | — | `tokenizer(text)` |
| mutate | mutator | mutation | mutable / immutable | "mutable state" |
| handle | handler | handling | — | "error handling" |
| depend | dependent | dependency | dependent | "a dependency graph" |

### ➕ Sufijos

| Sufijo | Qué hace | Ejemplos | En código |
|---|---|---|---|
| -er / -or | El que hace la acción | parser, compiler, handler, listener, iterator | `class EventListener` |
| -able / -ible | Que se puede | callable, iterable, readable, hashable, nullable, accessible | `typing.Callable` |
| -tion / -sion | El proceso o resultado | validation, iteration, conversion, permission | `PermissionError` |
| -ize | Convertir en, hacer | initialize, serialize, normalize, tokenize, sanitize | `normalize(x)` |
| -ify | Hacer, convertir | stringify, minify, simplify, notify, verify, prettify | `JSON.stringify()` |
| -ment | Resultado o lugar | deployment, assignment, environment, statement | "an assignment statement" |
| -ity | Cualidad | complexity, capacity, security, visibility, scalability | "time complexity" |
| -ness | Estado | readiness, correctness, robustness, freshness | "readiness probe" |
| -less | Sin | stateless, serverless, headless, passwordless | "a headless browser" |
| -ful | Con | stateful, useful, RESTful | "a RESTful API" |
| -al | Relativo a | optional, internal, external, global, local | `Optional[int]` |
| -ing | Acción como cosa | logging, caching, routing, loading | `import logging` |
| -ed | Estado resultante | cached, deprecated, nested, typed, compiled | `@deprecated` |
| -ly | Modo (adverbio) | lazily, recursively, asynchronously | "lazily loaded" |
| -wise | En cuanto a | element-wise, pairwise, row-wise | "element-wise addition" |

### 🔙 Prefijos

| Prefijo | Significa | Ejemplos | En código |
|---|---|---|---|
| re- | Otra vez | rebuild, rerun, retry, refactor, rename, reload, rebase | `retry(times=3)` |
| un- | Lo contrario, no | undo, unset, uninstall, unused, unknown, unhandled | "unhandled exception" |
| de- | Deshacer, quitar | decode, decrypt, deserialize, deprecate, dequeue, debug | `bytes.decode()` |
| dis- | Contrario | disable, disconnect, discard, dismiss | `disabled={true}` |
| pre- | Antes | preprocess, prefetch, preview, prefix, preload, pretrained | `prefetch_factor` |
| post- | Después | postprocess, postinstall, postfix | `"postinstall"` en npm |
| over- | Demasiado, encima | override, overflow, overfitting, overhead, overwrite | `@override` |
| under- | Debajo, poco | underflow, underfitting, underscore | — |
| sub- | Debajo, parte de | subclass, subprocess, subquery, subnet, substring | `subprocess.run()` |
| super- | Por encima | superclass, superuser, superset | `super().__init__()` |
| multi- | Muchos | multithreading, multiline, multimodal | "a multimodal model" |
| non- | No | non-blocking, nonzero, non-null | `np.nonzero()` |
| in- / im- / ir- | No | invalid, immutable, irreversible, inactive | `InvalidArgument` |
| inter- | Entre | interface, interop, internet | — |
| auto- | Por sí mismo | autocomplete, autosave, autoscaling, autograd | `torch.autograd` |
| mis- | Mal | misconfigured, mismatch, misuse | "type mismatch" |
| out- | Fuera, más allá | output, outdated, outage, outlier | "an outdated package" |
| up- / down- | Arriba / abajo | upload/download, upgrade/downgrade, upstream/downstream | `pip install --upgrade` |
| cross- | A través | cross-platform, cross-validation, cross-entropy | — |
| bi- / uni- / tri- | Dos / uno / tres | bidirectional, unidirectional, trigram | `nn.LSTM(bidirectional=True)` |

💡 Consejo: cuando veas una palabra larga como **"deserialization"**, pártela: de- (deshacer) + serial + -ize (convertir) + -ation (proceso) = "el proceso de deshacer la serialización".

⚠️ Cuidado: no inventes palabras con sufijos que no existen: es **"configurable"**, no "configurationable". Y no mezcles **optimize** (verbo: optimizar) con **optimal** (adjetivo: óptimo).

## 🔗 Phrasal verbs de programación

Un **phrasal verb** es verbo + partícula (up, out, in, down…) con un significado propio. Los nativos los usan muchísimo en docs y reuniones. Muchos tienen un **sustantivo** que se escribe junto: el verbo va separado (`set up`), la cosa va junta (`setup`).

### 🧰 Los esenciales

| Phrasal verb | Significa | Frase técnica | Sustantivo / adjetivo |
|---|---|---|---|
| set up | configurar, montar | "Let's set up the dev environment." | setup |
| log in / log out | iniciar / cerrar sesión | "Log in with your GitHub account." | login / logout |
| sign up | registrarse | "Sign up for an API key." | signup / sign-up |
| sign in / sign out | entrar / salir | "Sign in to the dashboard." | sign-in |
| back up | hacer copia de seguridad | "Back up the database first." | backup |
| roll back | revertir a la versión anterior | "We rolled back the release." | rollback |
| roll out | lanzar gradualmente | "We'll roll out the feature to 10% of users." | rollout |
| spin up | levantar rápido | "Spin up a container for testing." | — |
| tear down | desmontar, destruir | "Tear down the test cluster." | teardown |
| shut down | apagar | "Shut down the server gracefully." | shutdown |
| start up / boot up | arrancar | "It runs a migration on start up." | startup |
| clean up | limpiar | "Clean up temp files after the run." | cleanup |
| figure out | averiguar, entender | "I can't figure out why it fails." | — |
| look up | buscar (un dato) | "Look up the user by email." | lookup |
| look into | investigar | "I'll look into the memory leak." | — |
| check out | revisar / cambiar de rama | "Check out the feature branch." | checkout |
| run into | toparse con | "I ran into a CORS error." | — |
| fall back (to) | recurrir a la alternativa | "It falls back to the CPU if there's no GPU." | fallback |
| opt in / opt out | aceptar / rechazar | "Users can opt out of telemetry." | opt-in / opt-out |
| plug in | conectar, enchufar | "Plug in your own model." | plugin |
| break down | descomponer | "Break down the task into steps." | breakdown |
| narrow down | acotar | "Narrow down the bug to one commit." | — |
| drill down | profundizar en detalle | "Drill down into the metrics." | drill-down |
| step through / into / over | avanzar en el debugger | "Step through the loop line by line." | — |
| time out | agotarse el tiempo | "The request timed out after 30 s." | timeout |
| run out of | quedarse sin | "We ran out of memory." | — |
| free up | liberar | "Free up some disk space." | — |
| work around | rodear un problema | "We worked around the bug with a flag." | workaround |
| follow up | dar seguimiento | "I'll follow up on this tomorrow." | follow-up |
| kick off | arrancar, comenzar | "Kick off the build." | kickoff |
| wrap up | terminar, cerrar | "Let's wrap up the meeting." | wrap-up |
| lay out | disponer, organizar | "Lay out the components in a grid." | layout |
| mock up | hacer una maqueta | "Mock up the login screen." | mockup |
| hand off | pasar a otro | "Hand off the task to QA." | handoff |
| print out | imprimir | "Print out the variable." | printout |
| back off | retroceder, esperar más | "Back off and retry exponentially." | backoff |
| cut off | cortar | "The output gets cut off." | cutoff |
| drop out | abandonar, apagar | "Neurons drop out during training." | dropout |
| blow up | explotar, crecer sin control | "The gradients blow up." | — |
| scale up / out | escalar vertical / horizontal | "Scale out to five replicas." | — |
| phase out | retirar gradualmente | "We're phasing out Python 2." | — |
| come up with | idear | "Come up with a better name." | — |
| get rid of | deshacerse de | "Get rid of the dead code." | — |
| carry out | llevar a cabo | "Carry out the migration at night." | — |
| point out | señalar | "The reviewer pointed out a bug." | — |
| sort out | resolver, ordenar | "Let's sort out the merge conflict." | — |
| fill in / fill out | rellenar | "Fill in the env variables." | — |
| turn on / turn off | encender / apagar | "Turn off the cache in dev." | — |
| pick up | tomar, detectar | "The watcher picks up file changes." | pickup |
| catch up | ponerse al día | "Rebase to catch up with main." | catch-up |

::: columnas
### ❌ Mal
- "I need to setup the server."
- "Please login."
- "Backup your files."
::: siguiente
### ✅ Bien
- "I need to **set up** the server."
- "Please **log in**."
- "**Back up** your files."
:::

### 🎯 Verbo separado vs sustantivo junto

| Verbo (acción) | Sustantivo (cosa) | ✅ Correcto | ❌ Error típico |
|---|---|---|---|
| set up | setup | "I need to **set up** the **setup** script." | "I need to setup the server." |
| log in | login | "**Log in** on the **login** page." | "Please login." |
| back up | backup | "**Back up** your files to a **backup** drive." | "Backup your files." |
| check out | checkout | "**Check out** the branch; the **checkout** is instant." | "Checkout the branch." |
| shut down | shutdown | "**Shut down** the server; the **shutdown** takes 5 s." | "Shutdown the server." |
| roll back | rollback | "**Roll back** the deploy; the **rollback** worked." | "We need to rollback." |
| clean up | cleanup | "**Clean up** after tests in the **cleanup** step." | "Cleanup the files." |
| look up | lookup | "**Look up** the key; the **lookup** is O(1)." | "Lookup the key." |
| work around | workaround | "We **worked around** it; the **workaround** is ugly." | "We workarounded it." |

💡 Consejo: muchos phrasal verbs son **separables**: "set the server up" = "set up the server". Con pronombre, va en medio: "set **it** up", nunca "set up it".

⚠️ Cuidado: "setup", "login" y "backup" como verbo (escritos juntos) se ven mucho en internet, pero en docs bien escritas son error. Verbo separado, sustantivo junto.

🇬🇧 Frase modelo: "I ran into a timeout, looked into the logs, and figured out the DB was running out of connections."

## 🤝 Collocations: combinaciones naturales

Una **collocation** es una combinación de palabras que los nativos usan juntas "porque sí". Puedes ser gramaticalmente correcto y aun así sonar raro si eliges otro verbo. Aquí están los calcos del español más típicos.

### ✅ Verbo + sustantivo

| ✅ Se dice | ❌ No se dice (calco) | Español | Ejemplo |
|---|---|---|---|
| run a command | make a command | ejecutar un comando | "Run `npm install`." |
| run the tests | do the tests | ejecutar las pruebas | "Run the tests before pushing." |
| the tests pass | the tests approve | las pruebas pasan | "All tests pass." |
| raise an exception (Python) | launch an exception | lanzar una excepción | `raise ValueError` |
| throw an error (JS, Java) | launch an error | lanzar un error | `throw new Error()` |
| catch / handle an exception | capture an exception | capturar / manejar | `try/except` |
| fix a bug | repair a bug | arreglar un bug | "I fixed the bug." |
| file a bug / open an issue | put a bug | reportar un bug | "File a bug on GitHub." |
| make a request / send a request | do a request | hacer una petición | "Make a GET request." |
| pass an argument | give / send a parameter | pasar un argumento | "Pass the URL as an argument." |
| call a function | use / launch a function | llamar a una función | "Call `main()`." |
| return a value | give back a value | devolver un valor | "It returns `None`." |
| assign a value | give a value | asignar un valor | "Assign 0 to x." |
| push changes / push a commit | upload the changes | subir cambios | "Push your changes." |
| open a pull request | send a pull request | abrir un PR | "Open a PR against main." |
| resolve a conflict | solve a conflict | resolver un conflicto | "Resolve the merge conflict." |
| set a breakpoint / hit a breakpoint | put a stop | poner / llegar a un breakpoint | "Execution hits the breakpoint." |
| kill a process | close a process | matar un proceso | `kill -9 PID` |
| allocate / free memory | reserve / liberate memory | reservar / liberar memoria | `free(ptr)` |
| take up space | occupy space | ocupar espacio | "Logs take up 20 GB." |
| train a model | teach a model | entrenar un modelo | `trainer.train()` |
| fit a model / fit the data | adjust the model | ajustar un modelo | `model.fit(X, y)` |
| run inference | do inference | hacer inferencia | "Run inference on the GPU." |
| tune hyperparameters | regulate hyperparameters | ajustar hiperparámetros | "Tune the learning rate." |
| deploy to production | upload to production | desplegar en producción | "Deploy on Friday? Never." |
| the server is down / goes down | the server fell | el servidor se cayó | "Prod went down at 3 a.m." |
| the app crashes | the app breaks down | la app se cae | "It crashes on startup." |
| make a mistake | do a mistake | cometer un error | "I made a mistake in the query." |
| do research | make a research | investigar | "I did some research." |
| ask a question | make a question | hacer una pregunta | "Can I ask a question?" |
| pay attention | put attention | prestar atención | "Pay attention to the indentation." |
| have a meeting | make a meeting | tener una reunión | "We have a standup at 9." |
| take a look | give a look | echar un vistazo | "Can you take a look at my PR?" |
| save time | win time | ahorrar tiempo | "Caching saves time." |
| gain experience | win experience | ganar experiencia | "I gained experience with Docker." |
| meet requirements | comply requirements | cumplir requisitos | "It meets the requirements." |
| hit / reach a limit | arrive to a limit | alcanzar un límite | "We hit the rate limit." |
| lose data | loss data | perder datos | "We lost data in the crash." |
| make sense | have sense | tener sentido | "That makes sense." |
| trigger / fire an event | shoot an event | disparar un evento | "Clicking fires a `click` event." |

### 🧷 Preposiciones que van con cada palabra

| ✅ Se dice | ❌ Calco del español | Ejemplo |
|---|---|---|
| depend **on** | depend of | "It depends on the input." |
| consist **of** | consist in | "A tree consists of nodes." |
| based **on** | based in | "Based on the docs…" |
| different **from** | different of | "Python is different from Java." |
| compatible **with** | compatible to | "Compatible with Python 3.10+." |
| interested **in** | interested on | "I'm interested in ML." |
| good **at** | good in | "She's good at algorithms." |
| listen **to** | listen (sin to) | "Listen to this podcast." |
| explain **something to** someone | explain me | "Can you explain it to me?" |
| **on** line 5 | in line 5 | "The error is on line 5." |
| **in** the file / **in** the terminal | on the file | "Search in the file." |
| **on** GitHub / **on** Linux | in GitHub | "It's on GitHub." |
| **in** Python | on Python | "Written in Python." |
| **at** runtime / **at** compile time | in runtime | "It fails at runtime." |
| **in** production | on production | "A bug in production." |
| **by** default | for default | "Disabled by default." |
| **on** startup / **on** click | at startup (válido, menos común) | "Runs on startup." |
| **in** the background | on the background | "Runs in the background." |
| **at** index 0 | in index 0 | "The value at index 0." |
| **by** value / **by** reference | for value | "Passed by reference." |
| **in** parallel | on parallel | "Run jobs in parallel." |
| **over** HTTP / **via** SSH | by HTTP | "Connect via SSH." |
| **from** scratch | from zero | "Built from scratch." |
| **out of** memory | without memory | "CUDA out of memory." |
| **up to** date | to date | "Keep packages up to date." |
| **in** real time | on real time | "Updates in real time." |

⚠️ Cuidado: **"depend of"** es el calco más común de hispanohablantes. Siempre es **depend on**, y su sustantivo **dependency on**.

💡 Consejo: cuando leas docs, anota **el verbo junto con su sustantivo** ("raise an exception") y no la palabra sola. Así nunca dudarás qué verbo usar.

🇬🇧 Frase modelo: "Based on the logs, the job depends on a service that goes down at night, so it throws a timeout error."

## 🔠 Siglas técnicas y cómo se dicen

Unas siglas se **deletrean** (API = ei-pi-ái) y otras se dicen **como palabra** (JSON = yéison). Si las dices al revés, la gente tarda en entenderte. Regla general: si se puede pronunciar fácil, suele decirse como palabra.

### 🌐 Desarrollo y web

| Sigla | Se dice | Significa | Para qué sirve |
|---|---|---|---|
| API | ei-pi-**ÁI** | Application Programming Interface | Contrato para que programas hablen entre sí |
| SDK | es-di-**KÉI** | Software Development Kit | Librerías y herramientas para una plataforma |
| CLI | si-el-**ÁI** | Command-Line Interface | Programa que se usa desde la terminal |
| GUI | **GÚ**-i | Graphical User Interface | Programa con ventanas y botones |
| IDE | ai-di-**Í** | Integrated Development Environment | Editor completo: VS Code, PyCharm |
| CRUD | krad | Create, Read, Update, Delete | Las 4 operaciones básicas de datos |
| REST | rest | Representational State Transfer | Estilo de APIs sobre HTTP |
| JSON | **YÉI**-son | JavaScript Object Notation | Formato de datos de texto |
| YAML | **YÁ**-mel | YAML Ain't Markup Language | Formato de configuración |
| HTML | eich-ti-em-**ÉL** | HyperText Markup Language | Estructura de páginas web |
| CSS | si-es-**ÉS** | Cascading Style Sheets | Estilos de páginas web |
| DOM | dam | Document Object Model | Árbol de la página en memoria |
| HTTP / HTTPS | eich-ti-ti-**PÍ** / …-**ÉS** | HyperText Transfer Protocol (Secure) | Protocolo de la web |
| URL | iu-ar-**ÉL** | Uniform Resource Locator | Dirección web |
| UUID | iu-iu-ai-**DÍ** | Universally Unique Identifier | ID único de 128 bits |
| ORM | ou-ar-**ÉM** | Object-Relational Mapping | Usar la DB como objetos: SQLAlchemy |
| MVC | em-vi-**SÍ** | Model-View-Controller | Patrón de arquitectura |
| SPA | es-pi-**ÉI** | Single-Page Application | App web que no recarga la página |
| SSR / CSR | es-es-**ÁR** / si-es-**ÁR** | Server-Side / Client-Side Rendering | Dónde se genera el HTML |
| SSG | es-es-**YÍ** | Static Site Generation | HTML generado al compilar |
| PWA | pi-dábol-iu-**ÉI** | Progressive Web App | Web instalable como app |
| CORS | kors | Cross-Origin Resource Sharing | Permisos entre dominios |
| AJAX | **ÉI**-yaks | Asynchronous JavaScript and XML | Peticiones sin recargar |
| WASM | **UÁ**-zem | WebAssembly | Código rápido en el navegador |
| SEO | es-i-**ÓU** | Search Engine Optimization | Salir alto en Google |
| UX / UI | iu-**ÉKS** / iu-**ÁI** | User Experience / Interface | Experiencia / interfaz de usuario |
| OOP | ou-ou-**PÍ** | Object-Oriented Programming | Programación orientada a objetos |
| REPL | **RÉ**-pel | Read-Eval-Print Loop | Consola interactiva: `python` |
| JIT / AOT | yit / ei-ou-**TÍ** | Just-In-Time / Ahead-Of-Time | Cuándo se compila |
| GC | yi-**SÍ** | Garbage Collector | Libera memoria automáticamente |
| ASCII | **ÁS**-ki | American Standard Code for Information Interchange | Codificación de 128 caracteres |
| UTF-8 | iu-ti-ef-**ÉIT** | Unicode Transformation Format 8-bit | Codificación de texto universal |
| EOF | i-ou-**ÉF** | End Of File | Fin de archivo |
| CSV | si-es-**VÍ** | Comma-Separated Values | Tabla en texto |
| TODO | **TÚ**-du | To do | Comentario de tarea pendiente |
| a11y / i18n | **Á**-li o ei-i-lé-ven-uái / ai-ei-**TÍN**-en | accessibility / internationalization | Número = letras omitidas |

### ☁️ Infraestructura, redes y seguridad

| Sigla | Se dice | Significa | Para qué sirve |
|---|---|---|---|
| CI/CD | si-ai si-**DÍ** | Continuous Integration / Delivery | Probar y desplegar automáticamente |
| DNS | di-en-**ÉS** | Domain Name System | Traduce dominios a IPs |
| CDN | si-di-**ÉN** | Content Delivery Network | Servidores cercanos al usuario |
| VPN | vi-pi-**ÉN** | Virtual Private Network | Red privada cifrada |
| SSH | es-es-**ÉICH** | Secure Shell | Terminal remota segura |
| TCP / UDP | ti-si-**PÍ** / iu-di-**PÍ** | Transmission Control / User Datagram Protocol | Transporte fiable / rápido |
| IP | ai-**PÍ** | Internet Protocol | Direcciones de red |
| LAN / WAN | lan / uan | Local / Wide Area Network | Red local / extensa |
| NAT | nat | Network Address Translation | Varias IPs privadas tras una pública |
| DHCP | di-eich-si-**PÍ** | Dynamic Host Configuration Protocol | Asigna IPs automáticamente |
| TLS / SSL | ti-el-**ÉS** / es-es-**ÉL** | Transport Layer Security / Secure Sockets Layer | Cifrado de conexiones |
| JWT | yi-dábol-iu-**TÍ** o "jot" | JSON Web Token | Token firmado de sesión |
| OAuth | **ÓU**-oz | Open Authorization | "Login con Google" |
| 2FA / MFA | tu-ef-**ÉI** / em-ef-**ÉI** | Two-Factor / Multi-Factor Authentication | Segundo código |
| XSS | eks-es-**ÉS** | Cross-Site Scripting | Inyectar JS en otra web |
| CSRF | si-es-ar-**ÉF** o "sea-surf" | Cross-Site Request Forgery | Peticiones falsas en tu nombre |
| CVE | si-vi-**Í** | Common Vulnerabilities and Exposures | Catálogo de vulnerabilidades |
| VM | vi-**ÉM** | Virtual Machine | Computadora virtual |
| k8s | kei-ÉITS | Kubernetes (k + 8 letras + s) | Orquestar contenedores |
| AWS | ei-dábol-iu-**ÉS** | Amazon Web Services | Nube de Amazon |
| GCP | yi-si-**PÍ** | Google Cloud Platform | Nube de Google |
| S3 | es-**ZRÍ** | Simple Storage Service | Almacenamiento de archivos en AWS |
| IaC | ai-ei-**SÍ** | Infrastructure as Code | Terraform, Ansible |
| SaaS / PaaS / IaaS | sas / pas / ai-as | Software / Platform / Infrastructure as a Service | Modelos de nube |
| SLA | es-el-**ÉI** | Service Level Agreement | Uptime garantizado |
| TTL | ti-ti-**ÉL** | Time To Live | Cuánto dura algo en caché |
| SRE | es-ar-**Í** | Site Reliability Engineering | Ingeniería de fiabilidad |
| POSIX | **PÁ**-ziks | Portable Operating System Interface | Estándar de sistemas tipo Unix |

### 🤖 IA y hardware

| Sigla | Se dice | Significa | Para qué sirve |
|---|---|---|---|
| AI / ML / DL | ei-**ÁI** / em-**ÉL** / di-**ÉL** | Artificial Intelligence / Machine / Deep Learning | Tu carrera |
| LLM | el-el-**ÉM** | Large Language Model | GPT, Claude, Llama |
| GPT | yi-pi-**TÍ** | Generative Pre-trained Transformer | Familia de modelos de OpenAI |
| RAG | rag | Retrieval-Augmented Generation | LLM + búsqueda en tus documentos |
| NLP | en-el-**PÍ** | Natural Language Processing | Procesar texto |
| CV | si-**VÍ** | Computer Vision | Procesar imágenes |
| CNN / RNN | si-en-**ÉN** / ar-en-**ÉN** | Convolutional / Recurrent Neural Network | Imágenes / secuencias |
| LSTM | el-es-ti-**ÉM** | Long Short-Term Memory | RNN con memoria |
| GAN | gan | Generative Adversarial Network | Generar imágenes |
| RL / RLHF | ar-**ÉL** / ar-el-eich-**ÉF** | Reinforcement Learning (from Human Feedback) | Alinear modelos |
| MLP | em-el-**PÍ** | Multi-Layer Perceptron | Red densa básica |
| SGD | es-yi-**DÍ** | Stochastic Gradient Descent | Optimizador |
| MSE | em-es-**Í** | Mean Squared Error | Pérdida de regresión |
| PCA | pi-si-**ÉI** | Principal Component Analysis | Reducir dimensiones |
| LoRA | **LÓU**-ra | Low-Rank Adaptation | Fine-tuning barato |
| MLOps | em-el-**ÁPS** | Machine Learning Operations | Llevar modelos a producción |
| GPU / CPU / TPU | yi-pi-**IÚ** / si-pi-**IÚ** / ti-pi-**IÚ** | Graphics / Central / Tensor Processing Unit | Hardware de cómputo |
| CUDA | **KÚ**-da | Compute Unified Device Architecture | Programar GPUs NVIDIA |
| RAM / VRAM | ram / **VÍ**-ram | (Video) Random Access Memory | Memoria |
| SSD / HDD | es-es-**DÍ** / eich-di-**DÍ** | Solid-State / Hard Disk Drive | Almacenamiento |
| NVMe | en-vi-em-**Í** | Non-Volatile Memory Express | SSD muy rápido |
| BIOS / UEFI | **BÁI**-os / iu-i-ef-**ÁI** | Basic Input/Output System / Unified Extensible Firmware Interface | Arranque del PC |
| USB | iu-es-**BÍ** | Universal Serial Bus | Conector |
| IoT | ai-ou-**TÍ** | Internet of Things | Dispositivos conectados |
| NaN | nan | Not a Number | Resultado numérico inválido |

💡 Consejo: si no sabes cómo se dice una sigla, escucha cómo la dice el creador o la doc oficial en un video; en caso de duda, **deletrearla** siempre se entiende.

⚠️ Cuidado: no leas las letras a la española. "API" no es "a-pe-i" sino **ei-pi-ái**; "SQL" no es "ese-cu-ele"; "HTML" no es "hache-te-eme-ele".

## 🧘 Principios y leyes con nombre propio

Los programadores citan estas frases en code reviews, reuniones y blogs como si todos las conocieran. Si las conoces, entiendes la referencia y además **aprendes de los errores que otros ya cometieron**.

### 🧱 Principios de diseño de código

| Principio | Dice (en inglés) | La idea | Úsalo cuando |
|---|---|---|---|
| DRY | Don't Repeat Yourself | No dupliques lógica: extráela a una función | Copias y pegas el mismo bloque 3 veces |
| KISS | Keep It Simple, Stupid | La solución simple suele ser la mejor | Tu diseño necesita un diagrama para explicarse |
| YAGNI | You Aren't Gonna Need It | No programes lo que todavía no necesitas | Quieres añadir "por si acaso" |
| SoC | Separation of Concerns | Cada parte se encarga de una cosa | Mezclas SQL con HTML |
| SRP (la S de SOLID) | Single Responsibility Principle | Una clase, un motivo para cambiar | Tu clase `UserManager` hace de todo |
| OCP (la O) | Open/Closed Principle | Abierto a extensión, cerrado a modificación | Añadir un caso te obliga a editar un `if` gigante |
| LSP (la L) | Liskov Substitution Principle | Una subclase debe poder sustituir a su padre | `Square` hereda de `Rectangle` y rompe cosas |
| ISP (la I) | Interface Segregation Principle | Interfaces pequeñas y específicas | Una interfaz te obliga a implementar 20 métodos |
| DIP (la D) | Dependency Inversion Principle | Depende de abstracciones, no de implementaciones | Tu código crea la conexión a la DB dentro |
| Composition over inheritance | Prefer composition to inheritance | Mejor "tiene un" que "es un" | Árboles de herencia profundos |
| Law of Demeter | Talk only to your friends | No encadenes `a.b().c().d()` | Tu código conoce el interior de todo |
| Fail fast | Fail early and loudly | Detecta errores pronto y con un mensaje claro | Validar la entrada al inicio |
| Principle of least astonishment | Don't surprise the user | El código debe hacer lo que su nombre dice | `get_user()` que también borra datos |
| Boy Scout rule | Leave the code cleaner than you found it | Mejora un poco lo que tocas | En cada PR |
| Premature optimization | "Premature optimization is the root of all evil" (Knuth) | Primero que funcione, luego mide, luego optimiza | Optimizas sin un benchmark |

### 📜 Leyes y efectos famosos

| Ley | Dice (en inglés) | La idea | Lección para ti |
|---|---|---|---|
| Murphy's law | Anything that can go wrong will go wrong | Si algo puede fallar, fallará | Maneja errores y haz backups |
| Conway's law | Organizations design systems that mirror their communication structure | El software copia la estructura del equipo | 3 equipos = 3 servicios |
| Hofstadter's law | It always takes longer than you expect, even when you take into account Hofstadter's law | Siempre tardarás más de lo que crees | Multiplica tus estimaciones |
| Brooks's law | Adding people to a late project makes it later | Más gente no acelera un proyecto atrasado | Planifica, no "agregues manos" |
| Pareto principle | 80% of the effects come from 20% of the causes | Regla 80/20 | El 20% del código causa el 80% de los bugs |
| Ninety-ninety rule | The first 90% of the code takes 90% of the time; the remaining 10% takes the other 90% | Lo último siempre tarda muchísimo | Los detalles finales cuestan |
| Goodhart's law | When a measure becomes a target, it ceases to be a good measure | Si optimizas una métrica, deja de medir bien | Cuidado con "100% coverage" o benchmarks de IA |
| Hyrum's law | With enough users, every observable behavior will be depended on by somebody | Alguien dependerá hasta de tus bugs | Todo cambio rompe a alguien |
| Linus's law | Given enough eyeballs, all bugs are shallow | Muchos revisores encuentran los bugs | Pide code review |
| Kernighan's law | Debugging is twice as hard as writing the code | Si escribes código "ingenioso", no podrás depurarlo | Escribe código claro |
| Gall's law | A complex system that works evolved from a simple system that worked | Empieza simple y crece | No diseñes todo desde el inicio |
| Postel's law | Be conservative in what you send, liberal in what you accept | Principio de robustez | APIs tolerantes a la entrada |
| Moore's law | Transistor counts double about every two years | El hardware crecía exponencialmente | Contexto histórico del cómputo |
| Amdahl's law | Speedup is limited by the part that can't be parallelized | Paralelizar tiene un límite | Mide qué parte es secuencial |
| Parkinson's law | Work expands to fill the time available | El trabajo ocupa todo el tiempo que le des | Ponte plazos cortos |
| The Bitter Lesson (Rich Sutton) | General methods that leverage computation win in the long run | En IA, escalar cómputo y datos vence al conocimiento a mano | Clave para entender los LLMs |
| Occam's razor | The simplest explanation is usually the right one | La causa más simple suele ser la real | Al depurar: ¿guardaste el archivo? |
| Chesterton's fence | Don't remove a fence until you know why it was put up | No borres código que no entiendes | Investiga antes de borrar |

### 🗯️ Expresiones con nombre que oirás

| Expresión | Significa | Ejemplo de uso |
|---|---|---|
| Rubber duck debugging | Explicar tu código a un patito (o a quien sea) para encontrar el bug | "I found it while rubber-ducking." |
| Bus factor | Cuánta gente tendría que desaparecer para que el proyecto muera | "Our bus factor is one." |
| Not Invented Here (NIH) | Rechazar lo que no se hizo en casa | "Don't rewrite it; that's NIH." |
| Cargo cult programming | Copiar código sin entender por qué funciona | "That's cargo-cult code." |
| Dunning–Kruger effect | Quien sabe poco sobreestima lo que sabe | "Classic Dunning–Kruger." |
| Bikeshedding | Discutir horas lo trivial | "We're bikeshedding the button color." |
| Yak shaving | Cadena de tareas antes de la tarea real | "I spent the day yak shaving." |
| Heisenbug | Bug que desaparece cuando lo depuras | "It's a heisenbug: it vanishes with prints." |
| Works on my machine | Funciona en mi PC y en otra no | "Works on my machine, so let's use Docker." |
| Footgun | Algo fácil de usar mal | "Mutable default args are a footgun." |
| Tech debt | Atajos que habrá que pagar después | "We're paying off tech debt." |
| Spaghetti code | Código enredado | "This module is spaghetti." |
| Boilerplate | Código repetitivo de plantilla | "Too much boilerplate." |
| Happy path / edge case | El caso normal / un caso raro | "It only handles the happy path." |

🇬🇧 Frase modelo en una review: "This feels like premature optimization; let's keep it simple and follow YAGNI until we have a benchmark."

📌 Resumen: DRY, KISS y YAGNI para el día a día; SOLID para diseño OOP; Murphy, Hofstadter y Brooks para estimar con humildad.

## 🔀 Palabras que se confunden entre sí

Estas palabras se confunden incluso entre nativos, y en un README o un PR se notan muchísimo. Muchas aparecen en programación: **lose** data vs **loose** coupling.

| Palabra 1 | Palabra 2 | Diferencia | Ejemplo técnico |
|---|---|---|---|
| lose (luz) | loose (lus) | perder / suelto | "lose data" · "loose coupling" |
| affect | effect | afectar (verbo) / efecto (sustantivo) | "It affects performance" · "a side effect" |
| then | than | luego / que (comparar) | "build, then deploy" · "faster than C" |
| its | it's | su (posesivo) / it is | "the list and its length" · "it's empty" |
| your | you're | tu / you are | "your token" · "you're logged out" |
| their / there / they're | — | su de ellos / allí / they are | "their API" · "there is a bug" · "they're online" |
| whose | who's | de quién / who is | "whose PR is this?" · "who's on call?" |
| advice | advise | consejo (sust.) / aconsejar (verbo) | "good advice" · "I advise against it" |
| lead (lid) | led (led) | liderar / lideró (pasado) | "she leads the team" · "she led the migration" |
| quite | quiet / quit | bastante / silencioso / dejar | "quite fast" · "quiet mode `-q`" · "quit Vim" |
| principal | principle | principal, director / principio | "principal engineer" · "SOLID principles" |
| accept | except | aceptar / excepto | "accepts a list" · "all except one" |
| access | assess | acceder / evaluar | "access the DB" · "assess the risk" |
| ensure | assure / insure | asegurarse / tranquilizar / asegurar con póliza | "ensure the file exists" |
| every day | everyday | cada día / cotidiano | "I code every day" · "everyday tools" |
| later | latter | más tarde / el segundo de dos | "try again later" · "the latter option" |
| former | latter | el primero / el segundo | "of Vim and Emacs, the former…" |
| raise | rise | levantar algo (transitivo) / subir solo | "raise an error" · "costs rise" |
| fewer | less | menos (contables) / menos (no contables) | "fewer bugs" · "less memory" |
| weather | whether | clima / si (condicional) | "check whether the key exists" |
| choose (chuz) | chose (chouz) | elegir / eligió | "choose a model" · "we chose Postgres" |
| discrete | discreet | discreto (matemático, separado) / discreto (reservado) | "discrete math" |
| continuous | continual | sin interrupción / repetido con pausas | "continuous integration" |
| precede | proceed | ir antes / proceder, continuar | "the header precedes the body" · "proceed with install?" |
| sensitive | sensible | sensible a / sensato | "case-sensitive" (nunca "case-sensible") |
| e.g. | i.e. | por ejemplo / es decir | "a DB, e.g. Postgres" · "the root, i.e. `/`" |
| maybe | may be | quizás / puede ser | "maybe it's cached" · "it may be cached" |
| alternate | alternative | alternar, alterno / alternativa | "alternate rows" · "an alternative library" |
| dependent | dependency | que depende (adj.) / dependencia (sust.) | "dependent on X" · "install the dependencies" |
| complement | compliment | complementar / elogiar | "tools that complement each other" |
| breath | breathe | aliento / respirar | — |
| borrow | lend | pedir prestado / prestar | "can you lend me your laptop?" |
| setup | set up | sustantivo / verbo | "the setup" · "set up the repo" |
| login | log in | sustantivo / verbo | "login page" · "log in to continue" |

💡 Consejo: truco para **affect/effect**: **A**ffect = **A**ction (verbo), **E**ffect = **E**nd result (sustantivo).

⚠️ Cuidado: **"it's"** con apóstrofo solo cuando puedes decir "it is". En "the function and its arguments" no lleva apóstrofo.

🇬🇧 Frase modelo: "It's not a loose comparison; its effect is to lose the type information."

📌 Resumen: revisa estas parejas antes de publicar un README o un PR; un corrector como LanguageTool detecta muchas.

## 🧪 Pon a prueba tu inglés

Tapa la columna de la solución, intenta responder **en voz alta** y luego compara. Repite estos retos cada semana: verás cómo mejoras.

### ✅ Ejemplo resuelto: adivina cómo suena

| Palabra | Tu intento | ✅ Solución | Pista |
|---|---|---|---|
| queue | … | kiú | Solo suena la "q" y la "u" |
| cache | … | kash | Igual que "cash" |
| height | … | jáit | Rima con "light" |
| Linux | … | **LÍ**-nax | No "láinux" |
| Django | … | **YÁN**-gou | La D es muda |
| suite | … | suít | Como "sweet" |
| Kubernetes | … | ku-ber-**NÉ**-tis | Golpe en "ne" |
| pseudocode | … | **SÚ**-dou-koud | La p es muda |
| Azure | … | **Á**-zher | zh = "y" argentina |
| Jupyter | … | **YÚ**-pi-ter | Como el planeta Jupiter |
| epoch | … | **É**-pak | No "é-poch" |
| Docker | … | **DÁ**-ker | La o americana suena "a" |

### ✅ Ejemplo resuelto: lee esta línea en voz alta

Código: `for (let i = 0; i < arr.length; i++) { sum += arr[i]; }`

| Parte | Se lee |
|---|---|
| `for (let i = 0;` | "for, let i equal zero" |
| `i < arr.length;` | "while i is less than arr dot length" |
| `i++)` | "i plus plus" |
| `{ sum += arr[i]; }` | "sum plus-equals arr sub i" |
| Versión natural | "Loop over the array and add each element to sum." |

### ✅ Ejemplo resuelto: -ed y -s

| Palabra | ¿t, d o id? / ¿s, z o iz? | ✅ Suena |
|---|---|---|
| fixed | t | fikst |
| deployed | d | di-**PLÓID** |
| updated | id | ap-**DÉI**-tid |
| merged | d | merdyd |
| parsed | t | parst |
| tests | s | tests |
| files | z | failz |
| branches | iz | **BRÁN**-chiz |
| caches | iz | **KÁ**-shiz |

### ✅ Ejemplo resuelto: elige el verbo correcto

| Frase con hueco | ✅ Solución | Por qué |
|---|---|---|
| "If the input is invalid, the function ___ a ValueError." | raises | Python usa "raise" |
| "Please ___ the tests before you push." | run | "run the tests" |
| "Can you ___ a look at my PR?" | take | "take a look", no "give" |
| "The result ___ on the batch size." | depends | "depend **on**" |
| "We need to ___ ___ the server before the demo." | set up | Verbo separado |
| "The ___ took five minutes." | setup | Sustantivo junto |
| "I ___ a mistake in the migration." | made | "make a mistake" |
| "The model ___ after epoch 3." | overfits | Sobreajusta |

### ✅ Ejemplo resuelto: números y versiones

| Escrito | ✅ Se lee |
|---|---|
| `v3.11.2` | "version three point eleven point two" |
| `1,024` | "one thousand twenty-four" |
| `0.001` | "zero point zero zero one" / "one e minus three" |
| `70B` | "seventy billion" (setenta mil millones) |
| `10.0.0.1:5432` | "ten dot oh dot oh dot one, port fifty-four thirty-two" |
| `O(n^2)` | "O of n squared" |
| `2026-03-05` | "March fifth, twenty twenty-six" |

### ✅ Ejemplo resuelto: ¿cuál es la palabra correcta?

| Frase | ✅ Solución |
|---|---|
| "We don't want to (lose / loose) any data." | lose |
| "This change will (affect / effect) every user." | affect |
| "Rust is faster (then / than) Python." | than |
| "The array and (its / it's) length." | its |
| "Check (weather / whether) the file exists." | whether |
| "Usernames are case-(sensible / sensitive)." | sensitive |
| "We need (fewer / less) dependencies." | fewer |

### ✅ Ejemplo resuelto: explica tu código en 3 frases

Código: `def is_palindrome(s): return s == s[::-1]`

| Paso | Lo que dices en voz alta |
|---|---|
| Qué hace | "This function checks whether a string is a palindrome." |
| Cómo | "It compares the string with its reverse, using a slice with a step of minus one." |
| Coste | "It runs in O of n time and uses O of n extra space for the reversed copy." |

💡 Consejo: graba tus respuestas con el celular o transcríbelas con Whisper. Si la transcripción sale mal, ahí está la palabra que debes practicar.

📌 Resumen: si aciertas el 80 % de estas tablas sin mirar, ya tienes la base de sonidos y vocabulario. Vuelve a ellas cada mes.

## 🧰 Recursos para practicar

Herramientas concretas y gratuitas (o con versión gratis) que de verdad ayudan. Mejor usar 2 o 3 con constancia que 10 una sola vez.

### 🔊 Pronunciación

| Recurso | Para qué | Cómo usarlo |
|---|---|---|
| Cambridge Dictionary | Definición, IPA y audio UK y US | Busca la palabra y pulsa el altavoz "US" |
| Merriam-Webster | Diccionario americano con audio | Para la pronunciación de EE. UU. |
| Oxford Learner's Dictionaries | Definiciones simples para estudiantes | Lee el ejemplo de uso además de la definición |
| Longman Dictionary | Ejemplos y collocations | Mira la sección de collocations |
| Forvo | Audios de hablantes nativos | Nombres propios y marcas: "Kubernetes", "nginx" |
| YouGlish | Busca una palabra en miles de videos de YouTube | Escribe "idempotent" y oye cómo la dicen en charlas reales |
| Google "how to pronounce X" | Audio y animación de la boca | Rápido para una palabra suelta |
| Rachel's English (YouTube) | Pronunciación americana detallada | Videos sobre th, schwa, r y ritmo |
| BBC Learning English | Pronunciación y gramática | Su serie de pronunciación tiene videos cortos por sonido |

### 📚 Vocabulario y escritura

| Recurso | Para qué | Cómo usarlo |
|---|---|---|
| Anki | Tarjetas con repetición espaciada | 10–20 tarjetas nuevas por semana con audio y código |
| Reverso Context / Linguee | Ver frases traducidas en contexto real | Busca "lanzar una excepción" y mira cómo se dice |
| DeepL | Traducción de calidad | Para comprobar, no para escribir todo por ti |
| LanguageTool | Corrector de gramática y estilo (open source) | Extensión del navegador para issues y PRs |
| Grammarly | Corrector en el navegador | Revisa READMEs y emails |
| Wiktionary | Etimología y pronunciación IPA | Para entender de dónde viene una palabra |
| Asistente de IA | Conversar y corregir | "Correct my English and explain each mistake." |

### 🎧 Oído y práctica real

| Recurso | Para qué | Cómo usarlo |
|---|---|---|
| Language Reactor | Subtítulos dobles en YouTube y Netflix | Activa subtítulos en inglés + español y pausa en cada frase nueva |
| YouTube a 0.9x | Bajar la velocidad sin perder calidad | Shadowing: repite cada frase justo después |
| Whisper | Transcribir tu voz | Graba una explicación técnica y compara el texto con lo que quisiste decir |
| CS50 | Curso de CS en inglés claro | Activa subtítulos en inglés y toma notas en inglés |
| Exercism | Ejercicios con enunciados en inglés y mentores | Lee los enunciados en voz alta antes de programar |
| LeetCode | Problemas de entrevista | Explica tu solución en voz alta en inglés antes de enviarla |
| GitHub Issues | Inglés técnico real | Lee issues de proyectos que usas: cómo se describe un bug |
| Stack Overflow | Preguntas y respuestas técnicas | Copia patrones de frases de las mejores respuestas |

💡 Consejo: combina un recurso de **pronunciación** (YouGlish), uno de **memoria** (Anki) y uno de **producción** (explicar en voz alta y transcribir). Esa tríada cubre oír, recordar y hablar.

⚠️ Cuidado: los traductores automáticos te dan la palabra pero no la pronunciación ni la collocation. Úsalos para comprobar, no como muleta.

🇬🇧 Frase modelo para pedir ayuda a una IA: "Here's my explanation of my code. Please correct my English, keep it technical, and list my three most common mistakes."

📌 Resumen final: 20 minutos al día, sonidos primero, vocabulario con frases completas y siempre en voz alta. En un año, el inglés deja de ser un obstáculo y se vuelve tu herramienta.
