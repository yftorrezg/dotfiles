# 🌐 APIs y HTTP · Cómo hablan los sistemas
> De escribir una URL a diseñar tu propia API: DNS, TCP, TLS, HTTP, REST, GraphQL, gRPC, tiempo real, autenticación, curl y los errores que otros ya cometieron por ti.

## 🤝 Qué es una API y por qué existe

Cada app que usas es en realidad muchos programas hablando entre sí: la app del banco le pregunta tu saldo a un servidor, ese servidor le pregunta a una base de datos, y al pagar con QR habla con otro sistema de otra empresa. Para que dos programas escritos por personas distintas (y en lenguajes distintos) se entiendan, necesitan un **contrato**: qué se puede pedir, cómo se pide y qué se responde. Ese contrato es la API.

🧠 Concepto: una **API** (Application Programming Interface, interfaz de programación de aplicaciones) es el conjunto de reglas con el que un programa ofrece funciones o datos a otros programas, sin mostrar cómo están hechos por dentro.

🧠 Concepto: una **API web** es una API a la que se accede por la red, casi siempre usando **HTTP** (HyperText Transfer Protocol, protocolo de transferencia de hipertexto): el cliente manda un pedido (request) y el servidor devuelve una respuesta (response).

La analogía clásica es el **mesero de un restaurante**: tú (cliente) no entras a la cocina (servidor); miras el menú (documentación), pides algo concreto (request) y el mesero te trae el plato o te dice "no hay" (response con código de estado). La cocina puede cambiar de chef o de horno y a ti no te afecta mientras el menú siga igual. Esa es la gran idea: **separar el qué del cómo**.

```flujo
App móvil -> API : pide datos (HTTP)
Web React -> API : pide datos (HTTP)
Script Python -> API
API -> Base de datos : SQL
API -> Pagos : otra API
API -> Correo : otra API
```

### 🧩 Modelo cliente-servidor

🧠 Concepto: en el modelo **cliente-servidor**, el **cliente** inicia la conversación (navegador, app, script, otro servidor) y el **servidor** espera pedidos en un puerto y responde. Un mismo programa puede ser servidor para unos y cliente para otros.

- El servidor **no llama** al cliente por su cuenta en HTTP clásico: solo responde. (Para empujar datos existen WebSockets, SSE y webhooks; los vemos más adelante.)
- HTTP es **sin estado** (stateless): cada pedido llega solo, el servidor no "recuerda" el anterior. Para recordar quién eres se usan cookies o tokens.
- Un servidor atiende a **miles de clientes** a la vez; por eso se diseña para que cada pedido sea independiente y barato.

| Tipo de API | Ejemplo | Cómo se usa |
|---|---|---|
| Librería / SDK | `Array.map`, `pandas.read_csv` | Llamas funciones en tu código |
| Sistema operativo | `open()`, `fork()` (syscalls) | Tu programa le pide cosas al kernel |
| Navegador (Web APIs) | `fetch`, `localStorage`, `geolocation` | JS en la página |
| API web (remota) | Stripe, GitHub, OpenAI, Mercado Pago | HTTP por la red |

### 🏢 Casos de uso reales

- **Pagos**: Stripe, PayPal o Mercado Pago exponen APIs para cobrar; tu tienda nunca guarda la tarjeta.
- **Mapas**: Google Maps Platform y OpenStreetMap (Nominatim) para geocodificar direcciones.
- **Login con Google/GitHub**: OAuth 2.0 + OpenID Connect; tú no guardas su contraseña.
- **IA**: OpenAI, Anthropic y Hugging Face venden modelos por API: mandas texto, recibes texto.
- **Mensajería**: la API de WhatsApp Business o la Bot API de Telegram para bots y avisos.
- **Microservicios**: Netflix y Uber dividen su backend en muchos servicios que hablan entre sí por APIs internas (REST/gRPC).
- **Datos públicos**: GitHub, Wikipedia, Open-Meteo (clima) o la PokéAPI, perfectas para practicar.

💡 Consejo: cuando un producto dice "tiene integraciones", casi siempre significa "tiene una API pública y otros la usan".
🇬🇧 **request** /rikuést/ = pedido · **response** /rispóns/ = respuesta · **endpoint** /éndpoint/ = dirección concreta de la API · **client** /cláient/ = cliente · **stateless** /stéitles/ = sin estado

## 🧱 Capas de red: del cable a HTTP

HTTP no viaja solo: va "envuelto" dentro de otros protocolos, como una carta dentro de un sobre dentro de un camión. Cada capa resuelve un problema distinto y solo habla con la de arriba y la de abajo. Entender esto te ayuda a saber **dónde** está un error: ¿falla el DNS? ¿no conecta TCP? ¿certificado TLS vencido? ¿o la API devolvió 500?

```capas
Aplicación : HTTP, DNS, WebSocket, gRPC — el mensaje que entiende tu programa
Seguridad : TLS — cifra y comprueba que el servidor es quien dice ser
Transporte : TCP (fiable, ordenado) o UDP (rápido, sin garantías; QUIC va encima)
Red (Internet) : IP — direcciones y rutas entre redes (IPv4, IPv6)
Enlace / Físico : Ethernet, Wi-Fi, fibra — bits por el cable o el aire
```

🧠 Concepto: **IP** (Internet Protocol) da a cada máquina una dirección (`142.250.0.1`, `2800:cd0::1`) y lleva paquetes de red en red. No garantiza que lleguen ni en qué orden.
🧠 Concepto: **TCP** (Transmission Control Protocol) crea una **conexión** fiable sobre IP: numera los paquetes, reenvía los perdidos y los entrega en orden. Empieza con el saludo de 3 pasos (SYN, SYN-ACK, ACK).
🧠 Concepto: **UDP** (User Datagram Protocol) manda paquetes sin conexión ni reenvíos: más rápido, se usa en DNS, juegos, videollamadas y en **QUIC** (la base de HTTP/3).
🧠 Concepto: un **puerto** es un número (0–65535) que identifica a qué programa va el paquete dentro de la máquina: la IP es el edificio, el puerto es el departamento.

| Puerto | Servicio | Nota |
|---|---|---|
| `80` | HTTP | Sin cifrar: hoy solo redirige a 443 |
| `443` | HTTPS (TCP) y HTTP/3 (UDP) | El de casi todo |
| `53` | DNS | UDP normalmente |
| `22` | SSH | Acceso remoto |
| `5432` / `3306` | PostgreSQL / MySQL | Nunca abiertos a Internet |
| `3000`, `5173`, `8000`, `8080` | Servidores de desarrollo | Node, Vite, Django/FastAPI |

![Mapa de Internet del Opte Project (2005): cada línea une dos direcciones IP; así de grande es la red por la que viaja tu request (The Opte Project, CC BY 2.5, Wikimedia Commons)](img/apis/mapa-internet.jpg)

::: columnas
### 🔒 TCP
- Conexión previa (handshake)
- Entrega todo y en orden
- Reenvía lo perdido
- HTTP/1.1, HTTP/2, SSH, bases de datos
::: siguiente
### ⚡ UDP
- Sin conexión
- Puede perder o desordenar
- Menos latencia
- DNS, juegos, VoIP, QUIC (HTTP/3)
:::

💡 Consejo: "no conecta" y "conecta pero responde error" son problemas de capas distintas. `curl -v` te dice hasta dónde llegó.
🇬🇧 **handshake** /jándsheik/ = saludo inicial · **packet** /páket/ = paquete · **port** /port/ = puerto · **latency** /léitensi/ = latencia (demora) · **throughput** /zrúput/ = caudal

## 🔗 Anatomía de una URL

🧠 Concepto: una **URL** (Uniform Resource Locator) dice **dónde** está un recurso y **cómo** pedirlo. Cada parte tiene un trabajo.

```text
https://yafer:clave@api.ejemplo.dev:8443/v1/libros/42?campos=titulo,autor&idioma=es#resenas
└─┬─┘   └────┬────┘ └──────┬──────┘└─┬┘└──────┬─────┘└──────────────┬──────────────┘└──┬──┘
esquema   usuario       host       puerto   ruta (path)       query (parámetros)    fragmento
```

```arbol
URL
  esquema : https
  autoridad
    usuario:clave (obsoleto, evítalo)
    host : api.ejemplo.dev
      subdominio : api
      dominio : ejemplo.dev
    puerto : 8443 (si falta: 443)
  ruta : /v1/libros/42
  query : ?campos=titulo,autor&idioma=es
  fragmento : #resenas (no llega al servidor)
```

- `https` :: Esquema: protocolo a usar (http, https, ws, wss, ftp)
- `api.ejemplo.dev` :: Host: nombre que el DNS traduce a una IP
- `:8443` :: Puerto; si no se escribe, 443 para https y 80 para http
- `/v1/libros/42` :: Ruta: qué recurso quieres
- `?campos=titulo&idioma=es` :: Query string: filtros y opciones en pares clave=valor unidos con &
- `#resenas` :: Fragmento: lo usa solo el navegador (saltar a una sección); NO se envía al servidor

### 🔣 Codificación de URL (percent-encoding)

Una URL solo admite ciertos caracteres. Los espacios, tildes, `&`, `?` o `/` dentro de un valor se codifican como `%` + código hexadecimal en UTF-8. Si no lo haces, `?q=pan & leche` se rompe en dos parámetros.

```js
// JavaScript: arma URLs con URL y URLSearchParams (codifican por ti)
const url = new URL("https://api.ejemplo.dev/v1/buscar");
url.searchParams.set("q", "año & ñandú");
url.searchParams.set("pagina", 2);
console.log(url.href);
// → https://api.ejemplo.dev/v1/buscar?q=a%C3%B1o+%26+%C3%B1and%C3%BA&pagina=2
```

```python
from urllib.parse import urlencode, urlparse
print(urlencode({"q": "año & ñandú", "pagina": 2}))
# → q=a%C3%B1o+%26+%C3%B1and%C3%BA&pagina=2
print(urlparse("https://api.ejemplo.dev:8443/v1/libros/42?x=1#top").port)  # → 8443
```

❌ Mal: `fetch("/buscar?q=" + texto)` — si el usuario escribe `&admin=true`, inyecta parámetros.
✅ Bien: `url.searchParams.set("q", texto)` o `requests.get(url, params={"q": texto})`.
⚠️ Cuidado: nunca pongas tokens o contraseñas en la query: quedan en el historial, en los logs del servidor y en el header `Referer`.
🇬🇧 **query string** /kuíri string/ = cadena de consulta · **path** /paz/ = ruta · **encoding** /enkóuding/ = codificación · **domain** /doméin/ = dominio

## 🚀 Qué pasa al escribir una URL y dar Enter

Es la pregunta de entrevista más clásica de redes, y entenderla te permite depurar casi cualquier problema web. Resumen: **DNS → TCP → TLS → HTTP → render**.

```secuencia
actores: Navegador, DNS, Servidor
nota Navegador : ¿Está en caché? (HSTS, DNS, HTTP)
Navegador -> DNS : ¿IP de example.com?
DNS --> Navegador : 104.20.23.154
Navegador -> Servidor : TCP SYN (puerto 443)
Servidor --> Navegador : SYN-ACK
Navegador -> Servidor : ACK
Navegador -> Servidor : TLS ClientHello (ALPN: h2)
Servidor --> Navegador : ServerHello + certificado
nota Navegador : verifica certificado con sus CA
Navegador -> Servidor : GET / HTTP/2 (cifrado)
Servidor --> Navegador : 200 OK + HTML
nota Navegador : parsea HTML, pide CSS/JS/img y pinta
```

1. **Caché local**: el navegador mira si ya tiene la página o la IP guardadas, y si el dominio está en la lista HSTS (forzar HTTPS).
2. **DNS** (Domain Name System): traduce `example.com` a una IP. Pregunta al resolvedor (de tu ISP, `1.1.1.1` o `8.8.8.8`), que a su vez consulta servidores raíz → `.com` → servidor del dominio. Todo se cachea según el TTL.
3. **TCP**: saludo de 3 pasos con la IP en el puerto 443. Cuesta un viaje de ida y vuelta (RTT, round-trip time).
4. **TLS** (Transport Layer Security): acuerdan claves de cifrado y el servidor muestra su **certificado**, firmado por una autoridad (CA) en la que confía tu sistema. Con **ALPN** acuerdan HTTP/2 o 1.1. TLS 1.3 cuesta 1 RTT.
5. **HTTP**: ahora sí, el request viaja cifrado; el servidor (o una CDN delante) responde.
6. **Render**: el navegador lee el HTML, descubre CSS, JS e imágenes y lanza más requests (reutilizando la conexión).

### 🔬 Verlo de verdad con curl

`curl -w` mide cuánto tarda cada fase. Salida real desde este PC (Bolivia) contra example.com:

```bash
curl -s -o /dev/null -w "dns=%{time_namelookup}s tcp=%{time_connect}s tls=%{time_appconnect}s ttfb=%{time_starttransfer}s total=%{time_total}s http=%{http_version} code=%{http_code}\n" https://example.com
# dns=0.011663s tcp=0.151104s tls=0.307477s ttfb=0.474170s total=0.474225s http=2 code=200
```

```grafica
tipo: barras
titulo: ¿En qué se van los 474 ms? (medido con curl -w, example.com desde Bolivia, 2026)
unidad: ms
DNS : 12
TCP (1 RTT) : 139
TLS (1 RTT) : 156
Servidor + respuesta : 167
```

📌 Lo que enseña la gráfica: el servidor tardó poco; casi **dos tercios** del tiempo fueron **viajes de ida y vuelta** (TCP + TLS). Por eso existen las CDN (servidores cerca de ti), la reutilización de conexiones (keep-alive) y HTTP/3 (que junta TCP y TLS en un solo saludo).

```bash
curl -v https://example.com -o /dev/null   # fragmento real de la salida
# * IPv4: 104.20.23.154, 172.66.147.243
# * ALPN: curl offers h2,http/1.1
# * TLSv1.3 (OUT), TLS handshake, Client hello (1):
# * SSL connection using TLSv1.3 / TLS_AES_256_GCM_SHA384 / X25519MLKEM768
# * ALPN: server accepted h2
# *   subject: CN=example.com
# *   issuer: C=US; O=SSL Corporation; CN=Cloudflare TLS Issuing ECC CA 3
# > GET / HTTP/2
```

- `dig +short example.com` :: Ver la IP que devuelve el DNS
- `getent hosts example.com` :: Lo mismo usando la configuración del sistema
- `curl -v URL` :: Ver DNS, conexión, TLS, headers enviados (>) y recibidos (<)
- `openssl s_client -connect example.com:443` :: Inspeccionar el certificado TLS a mano

::: desplegable 🤔 ¿Qué es ese X25519MLKEM768 que salió en la salida?
Es el intercambio de claves **híbrido post-cuántico**: combina X25519 (curva elíptica clásica) con ML-KEM-768 (un algoritmo estandarizado por el NIST en 2024 como FIPS 203, pensado para resistir computadoras cuánticas). Navegadores y CDN grandes lo activaron por defecto entre 2024 y 2025 para que el tráfico grabado hoy no pueda descifrarse en el futuro ("harvest now, decrypt later"). Tú no tienes que hacer nada: lo negocian el cliente y el servidor.
:::

⚠️ Cuidado: "funciona con `curl` pero no en el navegador" casi siempre es **CORS**, cookies o caché; "no funciona en ningún lado" suele ser DNS, firewall o certificado.
🇬🇧 **round-trip time (RTT)** /ráund trip táim/ = tiempo de ida y vuelta · **resolver** /risólver/ = resolvedor DNS · **certificate authority (CA)** /sertífikeit ozóriti/ = autoridad certificadora · **TTFB (time to first byte)** = tiempo hasta el primer byte

## 📨 El mensaje HTTP y sus métodos

HTTP es **texto con estructura** (en HTTP/1.1 literalmente texto; en HTTP/2 y 3 es binario pero con las mismas partes). Todo request y toda response tienen 3 partes: **línea inicial**, **headers** (cabeceras) y, opcionalmente, **cuerpo** (body), separado por una línea en blanco.

::: columnas
### 📤 Request
```text
POST /api/v1/libros HTTP/1.1
Host: 127.0.0.1:8765
Authorization: Bearer token_de_prueba_123
Content-Type: application/json
Idempotency-Key: 7f3c2a10-pedido-42
Content-Length: 67

{"titulo":"Aluvión de fuego","autor":"Óscar Cerruto","anio":1935}
```
::: siguiente
### 📥 Response
```text
HTTP/1.1 201 Created
Server: LibrosAPI/1.0
Date: Mon, 19 Oct 2026 20:44:24 GMT
Location: /api/v1/libros/4
Content-Type: application/json; charset=utf-8
Content-Length: 81

{"id": 4, "titulo": "Aluvión de fuego", "autor": "Óscar Cerruto", "anio": 1935}
```
:::

📌 Este intercambio es real: lo hicimos con `curl -i` contra una API de prueba en Python (`servidor.py`, puerto 8765) que se usa en toda la hoja.

- **Línea de request**: `MÉTODO ruta VERSIÓN` → qué quieres hacer, sobre qué recurso.
- **Línea de estado**: `VERSIÓN código frase` → cómo salió.
- **Headers**: metadatos `Nombre: valor` (no distinguen mayúsculas; en HTTP/2 van en minúsculas).
- **Cuerpo**: los datos (JSON, HTML, imagen...). `Content-Type` dice qué formato y `Content-Length` cuántos bytes.

### 🔧 Métodos (verbos) HTTP

🧠 Concepto: un método es **seguro** (safe) si no cambia nada en el servidor (solo lee). Es **idempotente** si repetirlo 1 o 10 veces deja el servidor en el mismo estado. Esto importa muchísimo para los **reintentos**: un request idempotente se puede repetir sin miedo si se cortó la red.

| Método | Para qué | Seguro | Idempotente |
|---|---|---|---|
| `GET` | Leer un recurso o lista | ✅ | ✅ |
| `HEAD` | Como GET pero solo headers | ✅ | ✅ |
| `OPTIONS` | Preguntar qué se permite (CORS) | ✅ | ✅ |
| `POST` | Crear o ejecutar una acción | ❌ | ❌ |
| `PUT` | Reemplazar el recurso entero | ❌ | ✅ |
| `PATCH` | Modificar algunos campos | ❌ | ❌ (puede serlo) |
| `DELETE` | Borrar | ❌ | ✅ |

::: desplegable 🤔 ¿Por qué DELETE es idempotente si la segunda vez da 404?
Idempotencia habla del **estado del servidor**, no del código de respuesta. Borrar el libro 4 una vez o cinco veces deja el mismo estado: el libro 4 no existe. Que la primera respuesta sea 204 y las siguientes 404 está bien. En cambio, `POST /pedidos` repetido crea **dos pedidos**: estado distinto → no idempotente. Y `PATCH {"stock": "+1"}` (incrementar) tampoco lo es; `PATCH {"stock": 5}` (fijar) sí.
:::

::: columnas
### PUT (reemplaza todo)
```bash
curl -X PUT .../libros/2 \
  -H 'Content-Type: application/json' \
  -d '{"titulo":"Raza de bronce",
       "autor":"Alcides Arguedas",
       "anio":1919}'
# si olvidas "anio", queda vacío
```
::: siguiente
### PATCH (solo lo que mandas)
```bash
curl -X PATCH .../libros/2 \
  -H 'Content-Type: application/json' \
  -d '{"anio":1919}'
# titulo y autor no cambian
```
:::

❌ Mal: `GET /api/borrarUsuario?id=5` — los GET se precargan, se cachean y los rastreadores los siguen: alguien borrará datos sin querer.
✅ Bien: `DELETE /api/usuarios/5` con autenticación.
💡 Consejo: GET no debe llevar cuerpo. Si una búsqueda es tan compleja que no cabe en la query, usa `POST /busquedas` (o el método `QUERY`, estandarizado en 2026 como RFC 10008).
🇬🇧 **safe** /séif/ = seguro · **idempotent** /aidempóutent/ = idempotente · **header** /jéder/ = cabecera · **body** /bódi/ = cuerpo · **payload** /péilóud/ = carga útil

## 🚦 Códigos de estado

El código de 3 dígitos es lo primero que mira cualquier cliente: decide si hay que leer los datos, mostrar un error, pedir login o reintentar. El primer dígito dice la **familia**.

| Familia | Significa | Quién tiene la culpa |
|---|---|---|
| `1xx` | Información, sigue esperando | Nadie |
| `2xx` | Salió bien | Nadie 🎉 |
| `3xx` | Ve a otro lado o usa tu caché | Nadie |
| `4xx` | Pediste algo mal | El cliente: no reintentes igual |
| `5xx` | El servidor falló | El servidor: quizá reintentar |

### ✅ Los que vas a usar de verdad

- `200 OK` :: Éxito con cuerpo (GET, PATCH, PUT)
- `201 Created` :: Se creó un recurso (POST); incluye header Location con su URL
- `202 Accepted` :: Recibido, se procesará después (trabajos en cola)
- `204 No Content` :: Éxito sin cuerpo (DELETE, PUT sin respuesta)
- `301 Moved Permanently` :: Se mudó para siempre (SEO, http→https)
- `302 Found / 307 / 308` :: Redirección temporal (307/308 conservan el método)
- `304 Not Modified` :: Tu copia en caché sigue válida (ETag)
- `400 Bad Request` :: Request mal formado (JSON roto, tipo incorrecto)
- `401 Unauthorized` :: No autenticado: falta token o es inválido
- `403 Forbidden` :: Autenticado pero sin permiso
- `404 Not Found` :: No existe (o no quieres revelar que existe)
- `405 Method Not Allowed` :: Ese método no se acepta en esa ruta
- `409 Conflict` :: Choca con el estado actual (email repetido, versión vieja)
- `410 Gone` :: Existió y fue eliminado para siempre
- `415 Unsupported Media Type` :: Content-Type no aceptado
- `422 Unprocessable Content` :: JSON válido pero datos inválidos (validación)
- `429 Too Many Requests` :: Superaste el límite; mira Retry-After
- `500 Internal Server Error` :: Excepción no controlada en el servidor
- `502 Bad Gateway` :: El proxy recibió una respuesta inválida del servidor de atrás
- `503 Service Unavailable` :: Caído o saturado temporalmente; reintenta
- `504 Gateway Timeout` :: El proxy se cansó de esperar al servidor de atrás

```flujo
dir: abajo
¿Llegó el request? -> ¿Está autenticado? : sí
¿Está autenticado? -> 401 : no
¿Está autenticado? -> ¿Tiene permiso? : sí
¿Tiene permiso? -> 403 : no
¿Tiene permiso? -> ¿Existe el recurso? : sí
¿Existe el recurso? -> 404 : no
¿Existe el recurso? -> ¿Datos válidos? : sí
¿Datos válidos? -> 400/422 : no
¿Datos válidos? -> 200/201/204 : sí
```

::: columnas
### 🔑 401 Unauthorized
- "No sé quién eres"
- Falta el token, expiró o es falso
- Solución: inicia sesión / renueva el token
- Debe incluir `WWW-Authenticate`
::: siguiente
### ⛔ 403 Forbidden
- "Sé quién eres y no puedes"
- Usuario normal pidiendo algo de admin
- Volver a iniciar sesión NO ayuda
- A veces se usa 404 para no revelar que existe
:::

⚠️ Cuidado: el nombre "Unauthorized" del 401 es histórico y confuso: en realidad significa **no autenticado**.
💡 Consejo: `418 I'm a teapot` existe (broma del 1 de abril de 1998, RFC 2324) y httpbin.org lo devuelve: `curl -s -o /dev/null -w "%{http_code}" https://httpbin.org/status/418` → `418`. No lo uses en tu API 🫖.
🇬🇧 **status code** /stéitus kóud/ = código de estado · **redirect** /ridirékt/ = redirección · **gateway** /guéituei/ = puerta de enlace (proxy) · **retry** /ritrái/ = reintentar

## 🏷️ Headers, cuerpo y Content-Type

Los headers son los "metadatos" del mensaje: quién eres, qué formato mandas y aceptas, cuánto tiempo se puede guardar, de dónde vienes. Conocer 20 headers te da el 95 % del día a día.

### 📤 Headers de request

- `Host: api.ejemplo.dev` :: Obligatorio en HTTP/1.1: un mismo servidor aloja muchos sitios
- `Accept: application/json` :: Formatos que el cliente acepta en la respuesta
- `Content-Type: application/json` :: Formato del cuerpo que ENVÍAS
- `Authorization: Bearer <token>` :: Credenciales (token, Basic...)
- `User-Agent: mi-app/1.0` :: Quién hace el pedido (navegador, librería, bot)
- `Cookie: sesion=abc` :: Cookies que el navegador devuelve solo
- `Origin: http://localhost:5173` :: Origen de la página que hace el pedido (CORS)
- `If-None-Match: "c0be27da277c"` :: "Dámelo solo si cambió" (ETag)
- `Accept-Encoding: gzip, br, zstd` :: Compresiones que el cliente entiende
- `Idempotency-Key: <uuid>` :: Evita duplicar operaciones al reintentar POST

### 📥 Headers de response

- `Content-Type: application/json; charset=utf-8` :: Formato del cuerpo devuelto
- `Location: /api/v1/libros/4` :: URL del recurso creado o destino de la redirección
- `Cache-Control: max-age=60` :: Cuánto y quién puede guardar la respuesta
- `ETag: "c0be27da277c"` :: Huella de la versión del recurso
- `Set-Cookie: sesion=abc; HttpOnly; Secure` :: Guarda una cookie en el navegador
- `Access-Control-Allow-Origin: ...` :: Qué orígenes pueden leer la respuesta (CORS)
- `Retry-After: 60` :: Cuántos segundos esperar antes de reintentar (429/503)
- `WWW-Authenticate: Bearer` :: Cómo autenticarse (acompaña al 401)
- `Strict-Transport-Security: max-age=31536000` :: HSTS: usa siempre HTTPS
- `Content-Encoding: br` :: El cuerpo viene comprimido con Brotli

💡 Consejo: los headers propios ya no llevan el prefijo `X-` (se desaconsejó en 2012, RFC 6648): usa nombres claros como `Idempotency-Key` o `RateLimit-Remaining`.

### 📦 Formatos de cuerpo (Content-Type)

🧠 Concepto: el **Content-Type** (o MIME type) le dice al otro lado cómo interpretar los bytes del cuerpo. Si no coincide con lo que mandas, el servidor puede leerlo mal o rechazarlo con 415.

| Content-Type | Cuándo | Cómo se ve |
|---|---|---|
| `application/json` | APIs modernas | `{"nombre":"Ana","edad":21}` |
| `application/x-www-form-urlencoded` | Formularios HTML clásicos | `nombre=Ana&edad=21` |
| `multipart/form-data` | Subir archivos | Partes separadas por un boundary |
| `text/event-stream` | Server-Sent Events | `data: ...` línea a línea |
| `application/problem+json` | Errores estándar (RFC 9457) | `{"title":..., "status":...}` |
| `application/octet-stream` | Binario genérico (descargas) | Bytes |

```bash
# JSON (lo más común en APIs)
curl -X POST https://httpbin.org/post -H 'Content-Type: application/json' -d '{"nombre":"Yafer"}'
# Formulario clásico (-d sin header manda x-www-form-urlencoded)
curl -X POST https://httpbin.org/post -d 'nombre=Yafer&ciudad=Cochabamba'
# Subir un archivo (multipart): -F
curl -X POST https://httpbin.org/post -F 'foto=@perfil.jpg' -F 'descripcion=mi foto'
```

Prueba real del error 415 contra la API local (mandamos un formulario a un endpoint que exige JSON):

```bash
curl -s -X POST http://127.0.0.1:8765/api/v1/libros -H 'Authorization: Bearer token_de_prueba_123' -d 'titulo=x'
# {"type": ".../unsupported-media-type", "title": "Unsupported Media Type", "status": 415,
#  "detail": "Content-Type debe ser application/json", "instance": "/api/v1/libros"}
```

⚠️ Cuidado: en `fetch`, si mandas `body: JSON.stringify(datos)` **sin** `Content-Type: application/json`, se envía como `text/plain` y muchos backends (Express con `express.json()`) dejan `req.body` vacío. Error clásico.
🇬🇧 **MIME type** /máim táip/ = tipo de contenido · **boundary** /báundari/ = separador · **charset** /chárset/ = juego de caracteres · **upload** /áploud/ = subir archivo

## 🍪 Cookies y sesiones

HTTP no recuerda nada entre pedidos. Entonces, ¿cómo sabe Amazon que sigues logueado? Con **cookies**: el servidor le pide al navegador que guarde un dato pequeño, y el navegador lo devuelve **automáticamente** en cada pedido a ese sitio.

🧠 Concepto: una **cookie** es un par nombre=valor que el servidor crea con `Set-Cookie` y el navegador reenvía con `Cookie` a ese dominio. Una **sesión** es el estado del usuario guardado en el servidor (o en Redis), identificado por un ID aleatorio que viaja en la cookie.

```secuencia
actores: Navegador, Servidor, Redis
Navegador -> Servidor : POST /login (usuario + clave)
Servidor -> Redis : guarda sesión s_9f2c → user 42
Servidor --> Navegador : 200 + Set-Cookie: sid=s_9f2c; HttpOnly; Secure
nota Navegador : guarda la cookie
Navegador -> Servidor : GET /perfil + Cookie: sid=s_9f2c
Servidor -> Redis : ¿quién es s_9f2c?
Redis --> Servidor : user 42
Servidor --> Navegador : 200 + datos de user 42
```

```text
Set-Cookie: sid=s_9f2c8a71e0; Path=/; Max-Age=86400; HttpOnly; Secure; SameSite=Lax
```

- `HttpOnly` :: JavaScript NO puede leerla (document.cookie): protege del robo por XSS
- `Secure` :: Solo viaja por HTTPS
- `SameSite=Lax` :: No se envía en POST desde otros sitios: frena CSRF (por defecto en Chrome desde 2020)
- `SameSite=Strict` :: Ni siquiera al llegar desde un enlace externo
- `SameSite=None; Secure` :: Se envía siempre (widgets de terceros); requiere Secure
- `Max-Age=86400 / Expires=...` :: Caducidad; sin esto es cookie de sesión (muere al cerrar)
- `Domain=ejemplo.dev` :: Comparte con subdominios; sin esto, solo el host exacto
- `Path=/` :: Rutas en las que se envía

🧠 Concepto: **CSRF** (Cross-Site Request Forgery, falsificación de petición entre sitios): una página maliciosa hace que tu navegador envíe un pedido a tu banco y el navegador adjunta la cookie de sesión sola. Se mitiga con `SameSite`, tokens anti-CSRF y verificando `Origin`.

::: columnas
### 🍪 Sesión con cookie
- El servidor guarda el estado
- Cerrar sesión = borrar en el servidor (inmediato)
- El navegador la manda solo
- Ideal para webs del mismo dominio
- Riesgo: CSRF (usa SameSite)
::: siguiente
### 🎫 Token en header
- El cliente guarda el token
- El cliente lo pone en `Authorization`
- Funciona igual en apps móviles y scripts
- Ideal para APIs públicas y móviles
- Riesgo: si está en localStorage, un XSS lo roba
:::

⚠️ Cuidado: nunca guardes datos sensibles **dentro** de la cookie en texto plano (`rol=admin`): el usuario puede editarla. Guarda solo un ID aleatorio, o firma el contenido.
🇬🇧 **session** /séshon/ = sesión · **cookie** /kúki/ = galleta (dato guardado) · **same-site** /séim sáit/ = mismo sitio · **forgery** /fórlleri/ = falsificación

## 🛡️ CORS: por qué tu fetch "funciona en Postman pero no en el navegador"

El navegador aplica la **Same-Origin Policy** (política del mismo origen): un JS cargado desde `http://localhost:5173` NO puede leer respuestas de `http://localhost:8000` salvo que ese servidor lo permita. Sin esta regla, cualquier página que visitas podría leer tu Gmail usando tus cookies.

🧠 Concepto: un **origen** es la combinación **esquema + host + puerto**. `http://localhost:5173` y `http://localhost:8000` son orígenes **distintos** (cambia el puerto). `https://app.x.com` y `https://api.x.com` también (cambia el host).
🧠 Concepto: **CORS** (Cross-Origin Resource Sharing) es el mecanismo con el que el **servidor** dice, mediante headers, qué otros orígenes pueden leer sus respuestas. Lo hace cumplir el **navegador**; curl, Postman y tu backend lo ignoran.

### ✈️ El preflight (vuelo de prueba)

Si el pedido no es "simple" (usa PUT/PATCH/DELETE, `Content-Type: application/json` o un header como `Authorization`), el navegador primero manda un **OPTIONS** para preguntar si está permitido.

```secuencia
actores: JS en localhost:5173, Navegador, API en :8765
JS en localhost:5173 -> Navegador : fetch POST con JSON + Authorization
nota Navegador : no es simple → preflight
Navegador -> API en :8765 : OPTIONS /api/v1/libros + Origin + Access-Control-Request-Method: POST
API en :8765 --> Navegador : 204 + Allow-Origin: localhost:5173 + Allow-Methods + Allow-Headers
nota Navegador : ¿coinciden? sí → sigue
Navegador -> API en :8765 : POST /api/v1/libros (el de verdad)
API en :8765 --> Navegador : 201 + Access-Control-Allow-Origin
Navegador --> JS en localhost:5173 : entrega la respuesta
```

Preflight real contra la API de prueba:

```bash
curl -i -X OPTIONS http://127.0.0.1:8765/api/v1/libros \
  -H 'Origin: http://localhost:5173' \
  -H 'Access-Control-Request-Method: POST' \
  -H 'Access-Control-Request-Headers: content-type, authorization'
# HTTP/1.1 204 No Content
# Access-Control-Allow-Origin: http://localhost:5173
# Access-Control-Allow-Methods: GET, POST, PATCH, DELETE
# Access-Control-Allow-Headers: Content-Type, Authorization
# Access-Control-Max-Age: 600          ← el navegador recuerda la respuesta 10 min
# Vary: Origin

# Con un origen no permitido:
curl -i -X OPTIONS http://127.0.0.1:8765/api/v1/libros -H 'Origin: https://malicioso.example' -H 'Access-Control-Request-Method: POST'
# HTTP/1.1 403 Forbidden
```

### ⚙️ Configurarlo bien en el servidor

```js
// Node + Express con el paquete cors
import cors from "cors";
app.use(cors({
  origin: ["http://localhost:5173", "https://miapp.com"], // lista explícita
  credentials: true,           // permite cookies; exige origen exacto (no "*")
  maxAge: 600,
}));
```

```python
# FastAPI
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://miapp.com"],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
```

| Error en la consola | Causa | Solución |
|---|---|---|
| No 'Access-Control-Allow-Origin' header | El servidor no envía CORS | Configura CORS en el backend |
| Response to preflight ... doesn't pass | OPTIONS da 404/401/500 | Responde OPTIONS sin pedir auth |
| Wildcard '*' cannot be used ... credentials | `*` con cookies | Devuelve el origen exacto |
| Header authorization is not allowed | Falta en Allow-Headers | Agrégalo a Allow-Headers |
| Funciona en local, falla en producción | Lista de orígenes sin el dominio real | Agrega `https://tudominio.com` |

❌ Mal: "desactivar CORS" con una extensión del navegador o poner `Access-Control-Allow-Origin: *` con `credentials`. Lo primero solo te engaña a ti; lo segundo el navegador lo rechaza (y reflejar cualquier Origin con cookies es un agujero de seguridad).
✅ Bien: en desarrollo, usa el **proxy** del dev server (Vite `server.proxy`) para que el front y la API parezcan el mismo origen; en producción, lista blanca de orígenes.
💡 Consejo: CORS **no protege tu API** de bots ni de curl: solo impide que otras páginas web lean respuestas en el navegador de tus usuarios. La seguridad real es la autenticación.
🇬🇧 **origin** /óriyin/ = origen · **preflight** /prifláit/ = verificación previa · **cross-origin** /cros óriyin/ = entre orígenes · **allow** /aláu/ = permitir

## ⚡ Caché HTTP, ETag y CDN

La request más rápida es la que **no se hace**. HTTP trae un sistema de caché muy completo: el navegador, los proxies y las **CDN** (Content Delivery Network, red de distribución de contenido) pueden guardar respuestas y reutilizarlas.

🧠 Concepto: **Cache-Control** es el header con el que el servidor dice **quién** puede guardar la respuesta y **por cuánto tiempo**.
🧠 Concepto: un **ETag** es una huella (hash o versión) de la respuesta. El cliente la devuelve en `If-None-Match`; si no cambió, el servidor responde **304 Not Modified** sin cuerpo: ahorras ancho de banda.

- `Cache-Control: max-age=3600` :: Fresco durante 1 hora: ni pregunta al servidor
- `Cache-Control: no-cache` :: Puede guardarlo, pero debe revalidar SIEMPRE antes de usarlo
- `Cache-Control: no-store` :: No guardar nunca (datos bancarios, privados)
- `Cache-Control: private` :: Solo el navegador del usuario, no CDNs ni proxies
- `Cache-Control: public, s-maxage=600` :: CDN puede guardarlo 10 min (s- = shared)
- `Cache-Control: max-age=31536000, immutable` :: Archivos con hash en el nombre (app.3f9a.js): 1 año
- `stale-while-revalidate=60` :: Sirve la copia vieja mientras refresca por detrás
- `Vary: Accept-Encoding, Origin` :: La respuesta cambia según estos headers: guárdalas por separado

```secuencia
actores: Navegador, API
Navegador -> API : GET /api/v1/libros/1
API --> Navegador : 200 + ETag: "c0be27da277c" + cuerpo (87 bytes)
nota Navegador : guarda cuerpo + ETag
Navegador -> API : GET /api/v1/libros/1 + If-None-Match: "c0be27da277c"
nota API : calcula ETag: no cambió
API --> Navegador : 304 Not Modified (sin cuerpo)
nota Navegador : usa su copia
```

Prueba real:

```bash
curl -si http://127.0.0.1:8765/api/v1/libros/1 | grep -i etag
# ETag: "c0be27da277c"
curl -i -H 'If-None-Match: "c0be27da277c"' http://127.0.0.1:8765/api/v1/libros/1
# HTTP/1.1 304 Not Modified
# ETag: "c0be27da277c"
```

### 🌎 CDN: la caché cerca del usuario

```flujo
Usuario en La Paz -> CDN São Paulo : GET /logo.png
CDN São Paulo -> Origen en EE. UU. : solo si no lo tiene (MISS)
Origen en EE. UU. --> CDN São Paulo : logo + Cache-Control
CDN São Paulo --> Usuario en La Paz : HIT: rápido
```

Cloudflare, Fastly, Akamai, AWS CloudFront o la red de Vercel tienen cientos de servidores repartidos por el mundo. El primer usuario de una zona trae el archivo del origen (MISS); los siguientes lo reciben desde cerca (HIT), con menos RTT y menos carga en tu servidor. Las CDN modernas también terminan TLS, filtran ataques (DDoS) y ejecutan código en el borde (edge functions).

| Qué es | Cache-Control recomendado |
|---|---|
| JS/CSS con hash en el nombre | `public, max-age=31536000, immutable` |
| `index.html` | `no-cache` (siempre revalida) |
| Lista pública que cambia poco | `public, s-maxage=60, stale-while-revalidate=300` |
| Perfil del usuario | `private, no-cache` + ETag |
| Datos bancarios / tokens | `no-store` |

⚠️ Cuidado: cachear en la CDN una respuesta **personalizada** (con datos del usuario) sin `private` hace que otro usuario vea datos ajenos. Le pasó a Steam en Navidad de 2015: durante un ataque DDoS, una configuración de caché errónea hizo que unas 34 000 personas vieran páginas de la tienda con datos de otros usuarios (según el comunicado de Valve; no se expusieron contraseñas ni tarjetas completas).
💡 Consejo: si cambias un archivo estático y los usuarios siguen viendo la versión vieja, no pidas "Ctrl+F5": cambia su nombre (hash de build) o purga la CDN.
🇬🇧 **cache** /kash/ = caché · **stale** /stéil/ = viejo, pasado · **hit / miss** /jit, mis/ = acierto / fallo de caché · **edge** /ech/ = borde (servidor cercano) · **purge** /perch/ = purgar

## 🏎️ HTTP/1.1 vs HTTP/2 vs HTTP/3

```tiempo
1991 : HTTP/0.9 — solo GET, solo HTML
1996 : HTTP/1.0 — headers y códigos de estado
1997 : HTTP/1.1 — keep-alive, Host obligatorio (RFC 2068; hoy RFC 9112)
2009 : SPDY de Google — experimento que inspira HTTP/2
2015 : HTTP/2 — binario, multiplexado (RFC 7540; hoy RFC 9113)
2018 : TLS 1.3 — handshake de 1 RTT (RFC 8446)
2021 : QUIC estandarizado (RFC 9000)
2022 : HTTP/3 sobre QUIC (RFC 9114)
2026 : hoy: HTTP/2 y 3 dominan en navegadores
```

🧠 Concepto: **multiplexación** = mandar varios requests a la vez por **una sola conexión**, intercalando pedacitos (frames). HTTP/1.1 no lo hace: un request por conexión a la vez, por eso los navegadores abrían ~6 conexiones por dominio.
🧠 Concepto: **head-of-line blocking** (bloqueo de cabeza de fila): si el primer elemento de la fila se atasca, todos los de atrás esperan. HTTP/2 lo quitó a nivel HTTP, pero sigue en TCP (un paquete perdido frena todos los streams). HTTP/3 usa QUIC sobre UDP y lo elimina.

| | HTTP/1.1 | HTTP/2 | HTTP/3 |
|---|---|---|---|
| Formato | Texto | Binario (frames) | Binario (frames) |
| Transporte | TCP | TCP | QUIC (UDP) |
| Requests en paralelo | 1 por conexión | Muchos (streams) | Muchos, independientes |
| Compresión de headers | No | HPACK | QPACK |
| Handshake TCP + TLS | 2–3 RTT | 2–3 RTT | 1 RTT (0 al repetir) |
| Cambio de red (Wi-Fi → 4G) | Se corta | Se corta | Sobrevive (connection ID) |

```bash
curl -sI https://www.google.com | head -1           # HTTP/2 200
curl -sI https://www.cloudflare.com | grep -i alt-svc
# alt-svc: h3=":443"; ma=86400      ← "también hablo HTTP/3 en el 443 UDP"
curl -sI --http3-only https://www.cloudflare.com -o /dev/null -w "%{http_version}\n"   # 3
```

💡 Consejo: como programador de APIs casi no cambias nada: el servidor web o la CDN negocian la versión. Lo que sí cambia: con HTTP/2+ ya no hace falta juntar todos los JS en un solo archivo gigante ni usar "domain sharding".
⚠️ Cuidado: HTTP/2 sin TLS (h2c) casi no se usa en navegadores; en la práctica HTTP/2 y 3 implican HTTPS.
🇬🇧 **multiplexing** /múltiplexing/ = multiplexación · **stream** /strim/ = flujo · **head-of-line blocking** /jed ov láin bloking/ = bloqueo en cabeza de fila · **frame** /fréim/ = trama

## 🏗️ Diseño de APIs REST

🧠 Concepto: **REST** (REpresentational State Transfer) es un **estilo** de arquitectura (Roy Fielding, tesis doctoral del año 2000) donde todo es un **recurso** con su URL, se manipula con los métodos HTTP estándar, cada request es independiente (stateless) y las respuestas pueden cachearse. No es un estándar ni una librería: es un conjunto de convenciones.

La idea central: **sustantivos en la URL, verbos en el método**. La URL dice qué (los libros, el libro 42); el método dice qué hacer (leer, crear, borrar).

```arbol
/api/v1
  /libros  (colección)
    GET  → listar (filtros, paginación)
    POST → crear
    /{id}  (un libro)
      GET    → leer uno
      PATCH  → modificar campos
      PUT    → reemplazar
      DELETE → borrar
      /resenas  (subcolección)
        GET  → reseñas del libro
        POST → agregar reseña
  /autores
    /{id}/libros → libros de un autor
```

### 📏 Reglas de nombres

::: columnas
### ❌ Así no
```text
GET  /getLibros
POST /crearLibro
GET  /libro/borrar?id=4
POST /api/libros/4/update
GET  /Libros_Por_Autor
```
::: siguiente
### ✅ Así sí
```text
GET    /libros
POST   /libros
DELETE /libros/4
PATCH  /libros/4
GET    /autores/7/libros
```
:::

- **Plural y minúsculas**: `/libros`, `/ordenes-de-compra` (kebab-case en la URL).
- **Sin verbos** en la ruta… salvo **acciones** que no son CRUD: `POST /pedidos/42/cancelar` o `POST /pagos/9/reembolsos` (crear un reembolso) es aceptable y claro.
- **Anidar poco**: `/autores/7/libros` sí; `/paises/1/ciudades/3/autores/7/libros/2/resenas` no: más de 2 niveles es difícil de mantener.
- **Campos JSON consistentes**: elige `snake_case` o `camelCase` y no los mezcles. Fechas en **ISO 8601** con zona: `"2026-10-19T20:44:24Z"`.
- **IDs opacos**: mejor UUID o IDs aleatorios que números consecutivos si no quieres que adivinen cuántos clientes tienes (o que prueben `/facturas/1`, `/facturas/2`…).

### 🔢 Versionado

Tu API tendrá clientes que no puedes actualizar (apps móviles viejas, integraciones de otras empresas). Un cambio que rompe (renombrar un campo, quitar un endpoint) necesita una **nueva versión**.

| Estrategia | Ejemplo | Quién la usa |
|---|---|---|
| En la URL | `/api/v1/libros` | La más común y visible (Twitter/X, muchas APIs) |
| En un header | `X-GitHub-Api-Version: 2022-11-28` | GitHub |
| Por fecha en header | `Stripe-Version: ...` | Stripe (versiones por fecha) |
| Media type | `Accept: application/vnd.miapi.v2+json` | Menos común |

| Cambio | ¿Rompe? |
|---|---|
| Agregar un campo nuevo a la respuesta | No (los clientes lo ignoran) |
| Agregar un endpoint nuevo | No |
| Agregar parámetro opcional | No |
| Renombrar o quitar un campo | **Sí** |
| Cambiar el tipo (`"precio": "10"` → `10`) | **Sí** |
| Hacer obligatorio un campo que era opcional | **Sí** |
| Cambiar el significado de un código de estado | **Sí** |

### 📄 Paginación, filtros y orden

Nunca devuelvas una colección entera: hoy son 3 libros, mañana 3 millones y tu API se cae.

- `GET /libros?limite=20&pagina=3` :: Offset/página: simple, permite saltar a la página N; lento y con duplicados si insertan datos mientras paginas
- `GET /libros?limite=20&despues_de=420` :: Cursor/keyset: rápido y estable; no se puede saltar a la página 50
- `GET /libros?autor=arguedas&anio_min=1900` :: Filtros como parámetros de query
- `GET /libros?orden=-anio,titulo` :: Orden: - delante = descendente
- `GET /libros?campos=id,titulo` :: Selección de campos (respuestas más livianas)
- `GET /libros?q=bronce` :: Búsqueda de texto libre

Prueba real con paginación por cursor en la API local:

```bash
curl -s "http://127.0.0.1:8765/api/v1/libros?limite=2"
# {"datos": [{"id": 1, "titulo": "Cien años de soledad", ...}, {"id": 2, "titulo": "Raza de bronce", ...}],
#  "paginacion": {"limite": 2, "siguiente": "/api/v1/libros?limite=2&despues_de=2"}}
curl -s "http://127.0.0.1:8765/api/v1/libros?limite=2&despues_de=2"
# {"datos": [{"id": 3, "titulo": "Juan de la Rosa", ...}], "paginacion": {"limite": 2, "siguiente": null}}
```

::: desplegable 🤔 ¿Por qué el offset se vuelve lento?
`SELECT ... ORDER BY id LIMIT 20 OFFSET 100000` obliga a la base de datos a recorrer y descartar 100 000 filas antes de devolver 20. Con cursor, `WHERE id > 100000 ORDER BY id LIMIT 20` usa el índice y salta directo. Por eso las APIs grandes (Stripe con `starting_after`, Slack, GitHub en GraphQL) usan cursores.
:::

### 🚨 Errores con formato consistente (RFC 9457)

Si cada endpoint devuelve errores con forma distinta (`{"error": "..."}`, `{"msg": ...}`, texto plano), el cliente necesita un `if` por endpoint. El estándar **Problem Details** (RFC 9457, antes RFC 7807) define un formato común con `Content-Type: application/problem+json`.

```bash
curl -i http://127.0.0.1:8765/api/v1/libros/99
# HTTP/1.1 404 Not Found
# Content-Type: application/problem+json; charset=utf-8
#
# {"type": "https://api.ejemplo.dev/errores/not-found", "title": "Not Found", "status": 404,
#  "detail": "No existe el libro 99", "instance": "/api/v1/libros/99"}
```

```json
{
  "type": "https://api.ejemplo.dev/errores/validacion",
  "title": "Unprocessable Content",
  "status": 422,
  "detail": "Datos inválidos",
  "errores": [{ "campo": "autor", "mensaje": "es obligatorio" }]
}
```

- `type` :: URL que identifica el tipo de error (puede llevar a la documentación)
- `title` :: Resumen corto y fijo para ese tipo
- `status` :: El mismo código HTTP
- `detail` :: Explicación de ESTE caso concreto, legible por humanos
- `instance` :: Qué request o recurso falló (útil para soporte)
- `errores / trace_id` :: Campos extra permitidos (lista de validación, ID para buscar en logs)

⚠️ Cuidado: nunca devuelvas el stack trace, la consulta SQL o rutas internas en el error de producción: le regalas un mapa al atacante. Loguéalo en el servidor y devuelve un `trace_id`.

### 🔁 Idempotency keys: reintentar un POST sin cobrar dos veces

El cliente manda `POST /pagos`, la red se corta y no sabe si el pago se hizo. ¿Reintenta? Si el POST no es idempotente, podría **cobrar dos veces**. Solución popularizada por Stripe: el cliente genera un UUID por operación y lo manda en `Idempotency-Key`; el servidor guarda la respuesta asociada a esa clave y, si llega repetida, devuelve **la misma respuesta** sin volver a ejecutar.

```secuencia
actores: App, API, BD
App -> API : POST /pagos + Idempotency-Key: 7f3c...
API -> BD : ¿existe la clave 7f3c? no → cobrar y guardar resultado
API --> App : (se corta la red, la app no recibe nada)
App -> API : reintento: POST /pagos + misma Idempotency-Key
API -> BD : ¿existe 7f3c? sí
API --> App : 201 + la MISMA respuesta (sin cobrar de nuevo)
```

Prueba real (mismo POST dos veces con la misma clave → el mismo libro id 4, no se crea un 5):

```bash
curl -i -X POST http://127.0.0.1:8765/api/v1/libros \
  -H 'Authorization: Bearer token_de_prueba_123' -H 'Content-Type: application/json' \
  -H 'Idempotency-Key: 7f3c2a10-pedido-42' \
  -d '{"titulo":"Aluvión de fuego","autor":"Óscar Cerruto","anio":1935}'
# 1.ª vez: HTTP/1.1 201 Created · Location: /api/v1/libros/4
# 2.ª vez: HTTP/1.1 201 Created · Location: /api/v1/libros/4 · Idempotent-Replayed: true
```

### ✅ Ejemplo completo: API de libros en FastAPI

```python
# pip install fastapi uvicorn   ·   uvicorn libros:app --reload   ·   docs en /docs
from fastapi import FastAPI, HTTPException, Header, Query, Response, status
from pydantic import BaseModel, Field

app = FastAPI(title="Libros API", version="1.0.0")

class LibroNuevo(BaseModel):
    titulo: str = Field(min_length=1, max_length=200)
    autor: str
    anio: int | None = Field(default=None, ge=0, le=2100)

class Libro(LibroNuevo):
    id: int

LIBROS: dict[int, Libro] = {}
IDEMPOTENCIA: dict[str, Libro] = {}

@app.get("/api/v1/libros")
def listar(limite: int = Query(20, le=100), despues_de: int = 0, autor: str | None = None):
    datos = [l for l in sorted(LIBROS.values(), key=lambda l: l.id) if l.id > despues_de]
    if autor:
        datos = [l for l in datos if autor.lower() in l.autor.lower()]
    pagina = datos[:limite]
    siguiente = pagina[-1].id if len(datos) > limite else None
    return {"datos": pagina, "paginacion": {"limite": limite, "despues_de": siguiente}}

@app.get("/api/v1/libros/{libro_id}")
def leer(libro_id: int) -> Libro:
    if libro_id not in LIBROS:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"No existe el libro {libro_id}")
    return LIBROS[libro_id]

@app.post("/api/v1/libros", status_code=201)
def crear(nuevo: LibroNuevo, response: Response,
          idempotency_key: str | None = Header(default=None)) -> Libro:
    if idempotency_key and idempotency_key in IDEMPOTENCIA:
        return IDEMPOTENCIA[idempotency_key]           # misma respuesta, sin duplicar
    libro = Libro(id=max(LIBROS, default=0) + 1, **nuevo.model_dump())
    LIBROS[libro.id] = libro
    if idempotency_key:
        IDEMPOTENCIA[idempotency_key] = libro
    response.headers["Location"] = f"/api/v1/libros/{libro.id}"
    return libro

@app.delete("/api/v1/libros/{libro_id}", status_code=204)
def borrar(libro_id: int):
    LIBROS.pop(libro_id, None)                        # idempotente: 204 aunque no exista
```

```bash
# Probado en este PC (uvicorn libros:app --port 8767)
curl -si -X POST localhost:8767/api/v1/libros -H 'Content-Type: application/json' -H 'Idempotency-Key: k1' \
  -d '{"titulo":"Raza de bronce","autor":"Alcides Arguedas","anio":1919}'
# HTTP/1.1 201 Created
# location: /api/v1/libros/1
# {"titulo":"Raza de bronce","autor":"Alcides Arguedas","anio":1919,"id":1}
curl -s -X POST localhost:8767/api/v1/libros -H 'Content-Type: application/json' -d '{"titulo":"","autor":"x"}'
# 422 → {"detail":[{"type":"string_too_short","loc":["body","titulo"],"msg":"String should have at least 1 character",...}]}
curl -s localhost:8767/openapi.json | head -c 60
# {"openapi":"3.1.0","info":{"title":"Libros API","version":"1.0.0"},...
```

⚠️ Cuidado: los errores por defecto de FastAPI (`{"detail": ...}`) no siguen RFC 9457. En una API seria, registra un manejador de excepciones (`@app.exception_handler`) que los convierta a `application/problem+json`, así todos los errores tienen la misma forma.

💡 Consejo: FastAPI valida los datos con Pydantic (devuelve 422 solo) y genera la documentación OpenAPI en `/docs` sin escribir nada extra. En Node, lo equivalente es Express/Fastify/Hono + Zod.
📌 Checklist REST: sustantivos en plural · método correcto · código correcto · `Location` en 201 · paginación por defecto · errores en un solo formato · versión en la URL · idempotencia en pagos · nada de datos internos en la respuesta.
🇬🇧 **resource** /rísors/ = recurso · **breaking change** /bréiking chéinch/ = cambio que rompe · **pagination** /pallinéishon/ = paginación · **cursor** /kérsor/ = cursor · **backward compatible** /bákuord compátibol/ = compatible hacia atrás

## 🧬 GraphQL y gRPC: las alternativas a REST

![Logo de GraphQL (Facebook, licencia BSD de 3 cláusulas, Wikimedia Commons)](img/apis/graphql-logo.png)

### 🧬 GraphQL

🧠 Concepto: **GraphQL** es un lenguaje de consultas para APIs creado en Facebook (uso interno desde 2012, publicado en 2015). Hay **un solo endpoint** (`POST /graphql`) y el cliente escribe **exactamente qué campos quiere**, incluso de recursos relacionados, en un solo viaje.

Problemas de REST que resuelve:
- **Over-fetching** (traer de más): `GET /usuarios/7` devuelve 40 campos y tú solo querías el nombre.
- **Under-fetching** (traer de menos): para mostrar un usuario con sus 5 últimos posts y sus comentarios haces 1 + 5 + N requests.

::: columnas
### 📝 Consulta (query)
```text
query {
  autor(id: 7) {
    nombre
    libros(ultimos: 2) {
      titulo
      anio
    }
  }
}
```
::: siguiente
### 📦 Respuesta
```json
{
  "data": {
    "autor": {
      "nombre": "Alcides Arguedas",
      "libros": [
        { "titulo": "Raza de bronce", "anio": 1919 },
        { "titulo": "Pueblo enfermo", "anio": 1909 }
      ]
    }
  }
}
```
:::

```text
# Esquema (SDL): el contrato tipado que el servidor publica
type Autor { id: ID!  nombre: String!  libros(ultimos: Int): [Libro!]! }
type Libro { id: ID!  titulo: String!  anio: Int }
type Query { autor(id: ID!): Autor  libros(limite: Int = 20): [Libro!]! }
type Mutation { crearLibro(titulo: String!, autorId: ID!): Libro! }
type Subscription { libroCreado: Libro! }
```

```bash
# Probar la API pública de países (sin clave)
curl -s https://countries.trevorblades.com/ -H 'Content-Type: application/json' \
  -d '{"query":"{ country(code: \"BO\") { name capital currency } }"}'
```

⚠️ Cuidado (errores típicos con GraphQL):
- **Problema N+1**: resolver `libros` de 100 autores hace 100 consultas SQL. Se soluciona con **DataLoader** (agrupar en una sola consulta).
- **Consultas abusivas**: un cliente pide `amigos { amigos { amigos ... } }` 10 niveles y tumba el servidor. Limita profundidad y costo.
- **Caché HTTP**: todo es `POST /graphql`, así que la caché HTTP/CDN normal no sirve directo; se usan persisted queries o caché en el cliente (Apollo, urql, Relay).
- **Errores con 200**: GraphQL suele responder 200 con `{"errors": [...]}`. El cliente debe revisar `errors` siempre.

### 📡 gRPC

🧠 Concepto: **gRPC** es un framework de **RPC** (Remote Procedure Call: llamar a una función de otro servidor como si fuera local) creado por Google (código abierto desde 2015). Usa **Protocol Buffers** (protobuf, formato binario compacto y tipado) y viaja sobre **HTTP/2**. Del archivo `.proto` se **genera** el código cliente y servidor en Go, Java, Python, C++, etc.

```text
// libros.proto — el contrato
syntax = "proto3";
package libros.v1;

service LibrosService {
  rpc ObtenerLibro (ObtenerLibroRequest) returns (Libro);
  rpc ListarLibros (ListarRequest) returns (stream Libro);   // streaming del servidor
}
message ObtenerLibroRequest { int64 id = 1; }
message ListarRequest { int32 limite = 1; }
message Libro {
  int64 id = 1;
  string titulo = 2;
  string autor = 3;
  int32 anio = 4;
}
```

```bash
# grpcurl: el "curl" de gRPC
grpcurl -plaintext -d '{"id": 1}' localhost:50051 libros.v1.LibrosService/ObtenerLibro
```

💡 Consejo: gRPC brilla **entre microservicios** (rápido, tipado, streaming en ambos sentidos). Para navegadores no es directo (necesita gRPC-Web o Connect), por eso las APIs públicas siguen siendo REST.

### ⚖️ REST vs GraphQL vs gRPC

| | REST | GraphQL | gRPC |
|---|---|---|---|
| Formato | JSON (texto) | JSON (texto) | Protobuf (binario) |
| Contrato | OpenAPI (opcional) | Esquema SDL (obligatorio) | `.proto` (obligatorio) |
| Endpoints | Muchos (uno por recurso) | Uno (`/graphql`) | Métodos de un servicio |
| Caché HTTP | Excelente | Difícil | No aplica |
| Navegador | Nativo | Nativo | Necesita proxy |
| Ideal para | APIs públicas, CRUD | Frontends con datos anidados | Microservicios internos |

```flujo
dir: abajo
¿Quién consume la API? -> Público / terceros : REST
¿Quién consume la API? -> Mi frontend con datos anidados : GraphQL
¿Quién consume la API? -> Mis microservicios : gRPC
¿Quién consume la API? -> Front y back en TypeScript : tRPC
```

- **Casos reales**: GitHub ofrece API REST y API GraphQL (v4); Shopify empuja GraphQL en su Admin API; Netflix usa GraphQL federado en sus apps; Google expone sus APIs de Cloud con gRPC y REST a la vez; Kubernetes (etcd) y muchos sistemas internos hablan gRPC.
- **tRPC** (TypeScript): no es un protocolo nuevo sino tipos compartidos entre front y back en el mismo monorepo; cómodo pero solo TS.

🇬🇧 **over-fetching** /óver féching/ = traer de más · **resolver** /risólver/ = función que resuelve un campo · **schema** /skíma/ = esquema · **stub** /stab/ = cliente generado · **RPC (remote procedure call)** /rimóut prosíyur col/ = llamada a procedimiento remoto

## 🔌 Tiempo real: WebSockets, SSE, long polling y webhooks

HTTP clásico solo responde cuando el cliente pregunta. Pero un chat, el precio del dólar en vivo, el avance de una IA que escribe token a token o "tu pago fue aprobado" necesitan que el **servidor avise**. Hay cuatro formas, de la más vieja a la más usada hoy.

### 🔁 Polling y long polling

🧠 Concepto: **polling** = preguntar cada X segundos "¿hay algo nuevo?". Simple pero desperdicia requests. **Long polling** = el cliente pregunta y el servidor **retiene** la respuesta hasta que haya algo nuevo (o hasta un timeout); al recibirla, el cliente vuelve a preguntar al instante.

```secuencia
actores: Cliente, Servidor
Cliente -> Servidor : GET /mensajes?desde=41
nota Servidor : espera... (hasta 30 s)
Servidor --> Cliente : 200 [mensaje 42]
Cliente -> Servidor : GET /mensajes?desde=42
nota Servidor : espera... nada en 30 s
Servidor --> Cliente : 204 (vuelve a preguntar)
```

### 📻 SSE (Server-Sent Events)

🧠 Concepto: **SSE** es una respuesta HTTP que **no termina**: el servidor va escribiendo eventos de texto (`Content-Type: text/event-stream`) y el navegador los recibe con `EventSource`. Solo va del servidor al cliente. Reconecta solo y reanuda con `Last-Event-ID`. Es lo que usan las APIs de IA para el streaming de respuestas.

```js
// Servidor SSE mínimo en Node (probado en este PC)
import http from "node:http";
http.createServer((req, res) => {
  if (req.url !== "/eventos") return res.writeHead(404).end();
  res.writeHead(200, { "Content-Type": "text/event-stream", "Cache-Control": "no-cache", Connection: "keep-alive" });
  let n = 0;
  const t = setInterval(() => {
    n++;
    res.write(`id: ${n}\nevent: precio\ndata: ${JSON.stringify({ moneda: "USD", bob: (6.96 + n / 100).toFixed(2) })}\n\n`);
    if (n === 3) { clearInterval(t); res.end(); }
  }, 300);
  req.on("close", () => clearInterval(t));   // el cliente se fue: deja de emitir
}).listen(8766);
```

```bash
curl -N http://127.0.0.1:8766/eventos     # -N = no guardar en búfer, mostrar al llegar
# id: 1
# event: precio
# data: {"moneda":"USD","bob":"6.97"}
#
# id: 2 ...
```

```js
// En el navegador
const fuente = new EventSource("/eventos");
fuente.addEventListener("precio", (e) => console.log(JSON.parse(e.data)));
```

### 🔌 WebSockets

🧠 Concepto: un **WebSocket** empieza como un request HTTP con `Upgrade: websocket` (respuesta `101 Switching Protocols`) y luego la conexión TCP queda abierta en **ambos sentidos**: cliente y servidor mandan mensajes cuando quieran, con muy poco overhead. URLs `ws://` y `wss://` (con TLS).

```js
// Cliente (navegador o Node 22+, que trae WebSocket global)
const ws = new WebSocket("wss://chat.ejemplo.dev/sala/cochabamba");
ws.addEventListener("open", () => ws.send(JSON.stringify({ tipo: "unirse", usuario: "yafer" })));
ws.addEventListener("message", (e) => console.log("llegó:", JSON.parse(e.data)));
ws.addEventListener("close", (e) => console.log("cerrado", e.code)); // reconecta con backoff
```

```js
// Servidor con la librería ws (npm i ws)
import { WebSocketServer } from "ws";
const wss = new WebSocketServer({ port: 8080 });
wss.on("connection", (socket) => {
  socket.on("message", (datos) => {
    for (const cliente of wss.clients) cliente.send(datos.toString()); // difunde a todos
  });
});
```

### 🪝 Webhooks

🧠 Concepto: un **webhook** es "no me llames, yo te llamo": **tú** das una URL a otro servicio (Stripe, GitHub, Mercado Pago) y **él** te hace un `POST` cuando ocurre un evento (pago aprobado, push al repo). Servidor a servidor.

```secuencia
actores: Tu app, Pasarela de pago, Tu webhook
Tu app -> Pasarela de pago : crear cobro (notify_url = /webhooks/pagos)
Pasarela de pago --> Tu app : 201 pendiente
nota Pasarela de pago : el cliente paga minutos después
Pasarela de pago -> Tu webhook : POST /webhooks/pagos + firma HMAC
nota Tu webhook : verifica firma, guarda evento
Tu webhook --> Pasarela de pago : 200 rápido
nota Tu webhook : procesa en segundo plano
```

- **Verifica la firma** (HMAC con un secreto compartido, ej. header `Stripe-Signature` o `X-Hub-Signature-256` de GitHub): cualquiera puede hacer POST a tu URL.
- **Responde rápido** (2xx en < unos segundos) y procesa en una cola: si tardas, el proveedor reintenta.
- **Sé idempotente**: los proveedores reintentan y pueden mandar el mismo evento dos veces; guarda el `event_id` ya procesado.
- **No confíes solo en el webhook**: ante la duda, consulta el estado real a la API del proveedor.

### 📊 Cuándo usar cada uno

| Técnica | Dirección | Úsala para | Evítala si |
|---|---|---|---|
| Polling | Cliente pregunta | Estado de un trabajo cada 30 s | Necesitas inmediatez |
| Long polling | Cliente pregunta y espera | Entornos que bloquean WS | Hay miles de usuarios |
| SSE | Servidor → cliente | Notificaciones, streaming de IA, precios | Necesitas enviar mucho del cliente |
| WebSocket | Ambos sentidos | Chat, juegos, edición colaborativa | Solo empujas datos (SSE basta) |
| Webhook | Servidor → tu servidor | Pagos, CI/CD, eventos de SaaS | El receptor es un navegador |

💡 Consejo: si solo necesitas que el servidor empuje datos, empieza por **SSE**: es HTTP normal (pasa por proxies, usa la auth de siempre, reconecta solo). WebSocket añade estado y complejidad (escalar conexiones abiertas, balanceadores "sticky").
🇬🇧 **polling** /póuling/ = sondeo · **push** /push/ = empujar · **upgrade** /ápgreid/ = actualizar de protocolo · **broadcast** /bródkast/ = difundir · **webhook** /uébjuk/ = gancho web (callback HTTP)

## 🔐 Autenticación y autorización

🧠 Concepto: **autenticación** (authn) = comprobar **quién eres** (login, token). **Autorización** (authz) = decidir **qué puedes hacer** (¿puede este usuario borrar este libro?). Primero se autentica, después se autoriza en **cada** request.

::: columnas
### 🪪 Autenticación
- ¿Quién eres?
- Contraseña, token, huella, passkey
- Falla → `401 Unauthorized`
- Ej.: el portero revisa tu carnet
::: siguiente
### 🎟️ Autorización
- ¿Qué puedes hacer?
- Roles, permisos, dueño del recurso
- Falla → `403 Forbidden` (o 404)
- Ej.: tu entrada es de platea, no de VIP
:::

### 🧰 Los métodos, del más simple al más completo

| Método | Cómo viaja | Bueno para | Cuidado |
|---|---|---|---|
| API key | `Authorization: Bearer sk_...` o `X-API-Key` | Servidor a servidor, APIs de pago | Nunca en el frontend |
| HTTP Basic | `Authorization: Basic base64(user:clave)` | Herramientas internas, scripts | Base64 NO es cifrado |
| Sesión + cookie | `Cookie: sid=...` | Webs del mismo dominio | CSRF → SameSite |
| JWT (Bearer) | `Authorization: Bearer eyJ...` | APIs, móviles, microservicios | No se puede revocar fácil |
| OAuth 2.0 / OIDC | Tokens emitidos por un proveedor | "Entrar con Google", acceso de terceros | Flujo complejo: usa librerías |
| mTLS | Certificado del cliente en TLS | Bancos, servicio a servicio | Gestión de certificados |

### 🔑 API keys

Una cadena larga y aleatoria que identifica a **una aplicación** (no a un usuario). Sirve para cobrar por uso, aplicar límites y bloquear abusos.

```bash
curl https://api.ejemplo.dev/v1/clima?ciudad=Cochabamba -H "Authorization: Bearer $CLIMA_API_KEY"
```

- Guárdala en variables de entorno o un gestor de secretos, **nunca** en el código ni en git (`.env` en `.gitignore`).
- Usa **prefijos** que delaten el tipo (`sk_live_`, `ghp_`): GitHub y otros escanean repos públicos y revocan claves filtradas automáticamente (secret scanning).
- En el servidor guarda solo su **hash**, como una contraseña.
- Da **permisos mínimos** (scopes) y permite rotarlas.

### 🧾 HTTP Basic

```bash
echo -n 'yafer:cambia_esto' | base64          # eWFmZXI6Y2FtYmlhX2VzdG8=  ← reversible, NO es cifrado
curl -u 'yafer:cambia_esto' https://httpbin.org/basic-auth/yafer/cambia_esto
# {"authenticated": true, "user": "yafer"}
curl -s -o /dev/null -w "%{http_code}\n" -u 'yafer:otra' https://httpbin.org/basic-auth/yafer/cambia_esto
# 401
```

⚠️ Cuidado: Basic manda la contraseña en **cada** request; solo es aceptable sobre HTTPS y para cosas internas.

### 🎫 JWT (JSON Web Token)

🧠 Concepto: un **JWT** es un token con 3 partes en Base64URL separadas por puntos: `cabecera.carga.firma`. La **carga** (payload) lleva claims (afirmaciones) como `sub` (usuario), `exp` (expira) y `rol`. La **firma** demuestra que lo emitió quien tiene la clave y que nadie lo modificó. **No está cifrado**: cualquiera puede leerlo.

```text
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9 . eyJzdWIiOiI0MiIsIm5vbWJyZSI6IllhZmVy... . awnbktFt3J85KZdGch0ZAZFZ_swcqN2a0ILUKcbrCMU
└──────────── cabecera ────────────┘   └──────────── carga (claims) ──────┘   └──────────── firma HMAC-SHA256 ──────────┘
```

```js
// jwt.mjs — crear y verificar un JWT HS256 a mano para entenderlo (ejecutado con Node)
import { createHmac, timingSafeEqual } from "node:crypto";
const b64url = (obj) => Buffer.from(JSON.stringify(obj)).toString("base64url");
const SECRETO = "cambia_esto_por_un_secreto_largo";

const cabecera = { alg: "HS256", typ: "JWT" };
const carga = { sub: "42", nombre: "Yafer", rol: "lector", iat: 1760900000, exp: 1760903600 };
const datos = `${b64url(cabecera)}.${b64url(carga)}`;
const firma = createHmac("sha256", SECRETO).update(datos).digest("base64url");
const jwt = `${datos}.${firma}`;

// Cualquiera puede LEER la carga:
console.log(JSON.parse(Buffer.from(jwt.split(".")[1], "base64url").toString()));
// → { sub: '42', nombre: 'Yafer', rol: 'lector', iat: 1760900000, exp: 1760903600 }

function verificar(token) {
  const [h, p, f] = token.split(".");
  const esperada = createHmac("sha256", SECRETO).update(`${h}.${p}`).digest();
  const recibida = Buffer.from(f, "base64url");
  return recibida.length === esperada.length && timingSafeEqual(recibida, esperada);
}
console.log("válido:", verificar(jwt));                           // → válido: true
const trucho = b64url(cabecera) + "." + b64url({ ...carga, rol: "admin" }) + "." + firma;
console.log("con rol cambiado:", verificar(trucho));              // → con rol cambiado: false
```

```js
// En un proyecto real: la librería jose (npm i jose)
import { SignJWT, jwtVerify } from "jose";
const clave = new TextEncoder().encode(process.env.JWT_SECRETO);
const token = await new SignJWT({ rol: "lector" }).setProtectedHeader({ alg: "HS256" })
  .setSubject("42").setIssuedAt().setExpirationTime("15m").sign(clave);
const { payload } = await jwtVerify(token, clave, { algorithms: ["HS256"] }); // fija el algoritmo
```

| Claim | Significa |
|---|---|
| `sub` | Subject: a quién representa (ID de usuario) |
| `exp` | Expiration: hasta cuándo vale (segundos Unix) |
| `iat` | Issued at: cuándo se emitió |
| `iss` | Issuer: quién lo emitió |
| `aud` | Audience: para qué API es |

::: columnas
### 🎫 Access token
- Corto: 5–15 minutos
- Va en cada request (`Authorization`)
- Si lo roban, sirve poco tiempo
- Suele ser JWT
::: siguiente
### 🔄 Refresh token
- Largo: días o semanas
- Solo se usa para pedir un access token nuevo
- Guardado seguro (cookie HttpOnly)
- Revocable en el servidor; se rota en cada uso
:::

❌ Mal: meter el email, la contraseña o datos privados en la carga del JWT (es legible), usar `alg: none`, o aceptar el algoritmo que diga el token.
✅ Bien: carga mínima (`sub`, `rol`, `exp`), expiración corta, verificar firma **y** `exp`, `iss`, `aud`, y fijar la lista de algoritmos permitidos.
⚠️ Cuidado: un JWT no se puede "cerrar sesión" del lado del servidor hasta que expira (por eso access tokens cortos + refresh revocable, o una lista de bloqueados).

::: desplegable 🤔 ¿JWT o sesión? (la discusión eterna)
- **Sesión en servidor** (ID aleatorio en cookie + Redis): revocación instantánea, el token no lleva datos, muy simple para una web con su propio backend. Es la opción por defecto razonable.
- **JWT**: el servidor no necesita consultar una base para validar (útil entre microservicios o con muchos servicios que confían en un mismo emisor), funciona bien en apps móviles. A cambio: revocación difícil, tokens más grandes, más formas de configurarlo mal.
- Regla práctica: web monolítica → sesión con cookie. API pública / móvil / microservicios / login con terceros → tokens (normalmente emitidos vía OAuth/OIDC).
:::

### 🛂 Autorización: comprobar en cada recurso

🧠 Concepto: **BOLA** (Broken Object Level Authorization, autorización rota a nivel de objeto) es el riesgo **n.º 1** del OWASP API Security Top 10 (edición 2023): la API verifica que estás logueado pero no que **ese** objeto sea tuyo. Cambias `/facturas/1001` por `/facturas/1002` y ves la factura de otro.

```python
# ❌ Mal: solo verifica que hay usuario
@app.get("/api/v1/facturas/{factura_id}")
def ver(factura_id: int, usuario = Depends(usuario_actual)):
    return db.get(Factura, factura_id)

# ✅ Bien: verifica que la factura sea del usuario (o que sea admin)
@app.get("/api/v1/facturas/{factura_id}")
def ver(factura_id: int, usuario = Depends(usuario_actual)):
    factura = db.get(Factura, factura_id)
    if factura is None or (factura.cliente_id != usuario.id and usuario.rol != "admin"):
        raise HTTPException(404, "No existe")   # 404 para no confirmar que existe
    return factura
```

🇬🇧 **authentication** /ozentikéishon/ = autenticación · **authorization** /ozoriséishon/ = autorización · **claim** /cléim/ = afirmación · **scope** /scóup/ = alcance/permiso · **revoke** /rivóuk/ = revocar

## 🪪 OAuth 2.0 y OpenID Connect (con PKCE)

Problema: una app de impresión de fotos quiere leer tus fotos de Google. ¿Le das tu contraseña de Google? ¡No! Le daría acceso a todo (correo, Drive, pagos) y no podrías quitárselo sin cambiar la contraseña.

🧠 Concepto: **OAuth 2.0** (RFC 6749) es un protocolo de **autorización delegada**: el usuario autoriza a una app a acceder a **parte** de sus datos (scopes) en otro servicio, y la app recibe un **access token** limitado y revocable, sin ver nunca la contraseña.
🧠 Concepto: **OpenID Connect (OIDC)** es una capa encima de OAuth 2.0 para **autenticación**: además del access token, entrega un **ID token** (un JWT) que dice quién es el usuario (`sub`, `email`, `name`). "Iniciar sesión con Google" es OIDC.
🧠 Concepto: **PKCE** (Proof Key for Code Exchange, se pronuncia "pixy", RFC 7636) protege el flujo: si alguien roba el `code` de la redirección, no puede canjearlo sin el `code_verifier` secreto original.

### 🎭 Los 4 actores

- **Resource owner**: tú, el usuario dueño de los datos.
- **Client**: la app que quiere acceso (tu web, tu app móvil).
- **Authorization server**: quien autentica y emite tokens (Google, GitHub, Auth0, Keycloak, Supabase Auth).
- **Resource server**: la API con los datos (Google Photos API).

### 🔄 Flujo Authorization Code + PKCE (el recomendado hoy para todo)

```secuencia
actores: Usuario, App, Servidor de auth, API
nota App : genera code_verifier aleatorio y code_challenge = SHA256(verifier)
App -> Usuario : redirige a /authorize?client_id&redirect_uri&scope&state&code_challenge
Usuario -> Servidor de auth : inicia sesión y acepta permisos
Servidor de auth --> App : redirige a redirect_uri?code=abc&state=xyz
nota App : comprueba que state coincide
App -> Servidor de auth : POST /token (code + code_verifier)
nota Servidor de auth : SHA256(verifier) == challenge?
Servidor de auth --> App : access_token + refresh_token + id_token
App -> API : GET /fotos + Authorization: Bearer access_token
API --> App : 200 fotos
```

```text
1) Redirección al proveedor (todo en la URL, viaja por el navegador):
https://accounts.ejemplo-idp.com/authorize?response_type=code
  &client_id=mi-app-123
  &redirect_uri=https://miapp.com/callback
  &scope=openid%20email%20profile
  &state=Xk29dLq0            ← aleatorio: protege de CSRF
  &code_challenge=Qp2N7jemeJUHZQ7ZTA1x98sln4ZHDA8P0d7yZ4UI2ng
  &code_challenge_method=S256

2) Vuelta: https://miapp.com/callback?code=SplxlOBeZQQYbYS6WxSbIA&state=Xk29dLq0

3) Canje (servidor a servidor, o desde la app pública con PKCE):
POST /token
grant_type=authorization_code&code=SplxlOBeZQQYbYS6WxSbIA
&redirect_uri=https://miapp.com/callback&client_id=mi-app-123
&code_verifier=HpWyYrIuyza3LAcayY9If_g0wh69MFCw0wrjrQFG09E
```

```bash
# Generar un par PKCE real (Node): verifier aleatorio y challenge = base64url(SHA-256(verifier))
node -e 'const c=require("crypto");const v=c.randomBytes(32).toString("base64url");
console.log("verifier:",v);console.log("challenge:",c.createHash("sha256").update(v).digest("base64url"))'
# verifier: HpWyYrIuyza3LAcayY9If_g0wh69MFCw0wrjrQFG09E
# challenge: Qp2N7jemeJUHZQ7ZTA1x98sln4ZHDA8P0d7yZ4UI2ng
```

| Flujo (grant) | Para qué | Estado hoy |
|---|---|---|
| Authorization Code + PKCE | Webs, SPAs, apps móviles con usuario | ✅ El recomendado |
| Client Credentials | Servidor a servidor, sin usuario | ✅ Para máquinas |
| Device Code | Smart TVs, CLIs ("ve a esta URL y pon el código") | ✅ Para dispositivos sin teclado |
| Refresh Token | Renovar el access token | ✅ Con rotación |
| Implicit | Token directo en la URL (SPAs antiguas) | ❌ Desaconsejado |
| Password (ROPC) | La app pide tu usuario y clave | ❌ Desaconsejado |

⚠️ Cuidado: OAuth **por sí solo** no es login. Un access token dice "esta app puede leer fotos", no "este usuario es Juan". Para login usa **OIDC** y valida el **ID token** (firma, `iss`, `aud` = tu client_id, `exp`, `nonce`).
💡 Consejo: no implementes OAuth a mano en producción. Usa librerías certificadas o servicios: Auth.js (NextAuth), Better Auth, Clerk, Auth0, Keycloak, Supabase Auth, Firebase Auth; en Python, Authlib.
🚀 Futuro: OAuth 2.1 (aún borrador del IETF en 2026, no RFC) junta las buenas prácticas: PKCE obligatorio para todos, sin Implicit ni Password, y redirect_uri con coincidencia exacta.
🇬🇧 **grant** /grant/ = concesión (tipo de flujo) · **consent** /consént/ = consentimiento · **redirect URI** /ridirékt iu ar ái/ = URL de retorno · **identity provider (IdP)** /aidéntiti provaider/ = proveedor de identidad

## 🚧 Rate limiting y resiliencia

🧠 Concepto: el **rate limiting** (límite de tasa) restringe cuántos requests puede hacer un cliente en un período (ej. 100 por minuto por API key). Protege al servidor de abusos, bots y errores de clientes (un bucle infinito), y reparte la capacidad de forma justa.

| Algoritmo | Idea | Pro | Contra |
|---|---|---|---|
| Ventana fija | Contador por minuto (12:00–12:01) | Muy simple | Ráfaga doble en el borde |
| Ventana deslizante | Cuenta los últimos 60 s reales | Más justo | Más memoria/cálculo |
| Token bucket | Cubeta que se rellena N fichas/s; cada request gasta 1 | Permite ráfagas controladas | Algo más complejo |
| Leaky bucket | Cola que sale a ritmo constante | Suaviza el tráfico | Agrega espera |

```flujo
Request -> ¿Quedan fichas? : clave = API key o IP
¿Quedan fichas? -> Procesar : sí, gasta 1
¿Quedan fichas? -> 429 + Retry-After : no
Procesar --> Request : 200 + RateLimit-Remaining
```

Prueba real (la ruta `/limitado` permite 2 por minuto):

```bash
for i in 1 2 3; do curl -s -o /dev/null -w "%{http_code} " http://127.0.0.1:8765/limitado; done
# 200 200 429
curl -i http://127.0.0.1:8765/limitado
# HTTP/1.1 429 Too Many Requests
# Retry-After: 60
# RateLimit-Limit: 2
# RateLimit-Remaining: 0
```

### 🔁 Reintentos con backoff exponencial y jitter

Cuando algo falla temporalmente (503, 429, timeout), reintentar está bien, pero **no** inmediatamente ni todos a la vez: si mil clientes reintentan al mismo segundo, tumban de nuevo al servidor que se estaba recuperando (thundering herd, estampida).

🧠 Concepto: **backoff exponencial** = esperar cada vez el doble (0,5 s, 1 s, 2 s, 4 s…). **Jitter** = sumar un poco de azar para que los clientes no se sincronicen.

```grafica
tipo: lineas
titulo: Espera antes del reintento n (base 0,5 s, tope 30 s)
x: 1..8
ymax: 32
ejex: número de reintento
Backoff exponencial (s): 0.5*2^(n-1)
Fija de 1 s (mala idea): 1
```

| Reintenta | No reintentes |
|---|---|
| Timeout de conexión o lectura | `400`, `401`, `403`, `404`, `422` |
| `429` (respetando Retry-After) | Errores de validación |
| `502`, `503`, `504` | POST sin Idempotency-Key |
| Conexión reseteada | Cuando ya pasaste el máximo de intentos |

💡 Consejo: para dependencias que fallan mucho, añade un **circuit breaker** (cortacircuitos): tras N fallos seguidos deja de llamar durante un rato y devuelve un error rápido o un valor de respaldo, en vez de acumular requests colgados.
🇬🇧 **rate limit** /réit límit/ = límite de tasa · **throttling** /zrótling/ = estrangular (frenar) · **backoff** /bákof/ = retroceso (esperar más) · **jitter** /yíter/ = variación aleatoria · **circuit breaker** /sérkit bréiker/ = cortacircuitos

## 📘 Documentar APIs con OpenAPI (Swagger)

![Logotipo de la OpenAPI Initiative (marca de la Linux Foundation, vía Wikimedia Commons)](img/apis/openapi-logo.png)

Una API sin documentación no existe: nadie sabrá usarla. Y documentación escrita a mano en un Word se desactualiza en una semana.

🧠 Concepto: **OpenAPI** (antes llamada Swagger; versión actual 3.1) es un formato estándar en YAML/JSON que describe una API REST: rutas, parámetros, cuerpos, respuestas, errores y autenticación. Es un **contrato legible por máquinas**. **Swagger UI**, Redoc o Scalar lo convierten en una página interactiva donde puedes probar cada endpoint.

```yaml
openapi: 3.1.0
info:
  title: Libros API
  version: 1.0.0
servers:
  - url: https://api.ejemplo.dev/v1
paths:
  /libros/{id}:
    get:
      summary: Obtener un libro
      parameters:
        - name: id
          in: path
          required: true
          schema: { type: integer }
      responses:
        "200":
          description: El libro
          content:
            application/json:
              schema: { $ref: "#/components/schemas/Libro" }
        "404":
          description: No existe
          content:
            application/problem+json:
              schema: { $ref: "#/components/schemas/Problema" }
      security:
        - bearerAuth: []
components:
  securitySchemes:
    bearerAuth: { type: http, scheme: bearer, bearerFormat: JWT }
  schemas:
    Libro:
      type: object
      required: [id, titulo, autor]
      properties:
        id: { type: integer, example: 2 }
        titulo: { type: string, example: Raza de bronce }
        autor: { type: string, example: Alcides Arguedas }
        anio: { type: integer, example: 1919 }
    Problema:
      type: object
      properties:
        title: { type: string }
        status: { type: integer }
        detail: { type: string }
```

```flujo
Código (FastAPI, NestJS) -> openapi.json : genera
openapi.json -> Swagger UI : docs interactivas
openapi.json -> Clientes TS/Python : openapi-generator
openapi.json -> Tests de contrato : Schemathesis
openapi.json -> Mocks : Prism
```

::: columnas
### 🧑‍💻 Code-first
- Escribes el código y el framework genera el OpenAPI
- FastAPI (`/docs`), NestJS, Spring (springdoc)
- Rápido para empezar
- Riesgo: el diseño queda a merced del código
::: siguiente
### 📐 Design-first (contract-first)
- Escribes el YAML primero y lo revisa el equipo
- Front y back trabajan en paralelo con un mock
- Mejor para APIs públicas grandes
- Requiere disciplina para mantenerlo
:::

- `openapi-generator-cli generate -i openapi.json -g typescript-fetch -o cliente/` :: Genera un cliente tipado
- `npx @redocly/cli lint openapi.yaml` :: Revisa errores y malas prácticas del contrato
- `npx @stoplight/prism-cli mock openapi.yaml` :: Servidor falso que responde según el contrato
- `schemathesis run http://localhost:8000/openapi.json` :: Genera miles de requests para romper tu API

💡 Consejo: además del contrato, una buena documentación tiene **guía de inicio** ("tu primer request en 5 minutos"), ejemplos con curl, la lista de errores y un **changelog**. Stripe y Twilio son referentes clásicos de buena documentación.
🇬🇧 **spec (specification)** /spek/ = especificación · **contract** /cóntrakt/ = contrato · **mock** /mok/ = simulación · **changelog** /chéinchlog/ = registro de cambios

## 🧰 Herramientas: curl, HTTPie, Postman, Bruno y DevTools

![Logo de curl (Daniel Stenberg y colaboradores, licencia MIT, Wikimedia Commons)](img/apis/curl-logo.png)

### 🌀 curl a fondo

**curl** (client URL) es el cuchillo suizo de HTTP: viene en casi todos los sistemas, sirve para depurar y se usa en scripts y en la documentación de casi todas las APIs. Aprenderlo bien te ahorra horas.

- `curl URL` :: GET simple; imprime el cuerpo
- `curl -i URL` :: Incluye los headers de la respuesta
- `curl -I URL` :: Solo headers (hace HEAD)
- `curl -v URL` :: Verboso: DNS, TLS, headers enviados (>) y recibidos (<)
- `curl -s URL` :: Silencioso (sin barra de progreso); `-sS` muestra errores
- `curl -X POST URL` :: Elige el método
- `curl -H 'Accept: application/json' URL` :: Agrega un header
- `curl -d '{"a":1}' URL` :: Cuerpo (si hay -d el método pasa a POST solo)
- `curl --json '{"a":1}' URL` :: Atajo: pone Content-Type y Accept JSON (curl 7.82+)
- `curl -F 'foto=@a.jpg' URL` :: Subida multipart
- `curl -u user:clave URL` :: Basic auth
- `curl -L URL` :: Sigue redirecciones (301/302)
- `curl -o archivo URL` :: Guarda en archivo; `-O` usa el nombre remoto
- `curl -w '%{http_code}\n' -o /dev/null -s URL` :: Solo imprime el código de estado
- `curl --max-time 5 URL` :: Tiempo máximo total
- `curl --connect-timeout 3 URL` :: Tiempo máximo para conectar
- `curl --retry 3 --retry-all-errors URL` :: Reintenta automáticamente
- `curl -k URL` :: Ignora el certificado (SOLO pruebas locales)
- `curl --http2 / --http3 URL` :: Fuerza una versión de HTTP
- `curl -b cookies.txt -c cookies.txt URL` :: Lee y guarda cookies
- `curl --resolve api.x.com:443:127.0.0.1 https://api.x.com` :: Fuerza una IP sin tocar /etc/hosts

Todo lo siguiente se ejecutó contra la API de prueba local:

```bash
# POST con JSON + token + ver todo (-i)
curl -i -X POST http://127.0.0.1:8765/api/v1/libros \
  -H 'Authorization: Bearer token_de_prueba_123' \
  -H 'Content-Type: application/json' \
  -d '{"titulo":"Aluvión de fuego","autor":"Óscar Cerruto","anio":1935}'
# HTTP/1.1 201 Created
# Location: /api/v1/libros/4

# Timeout: /lento tarda 5 s y cortamos a los 2
curl -sS --max-time 2 http://127.0.0.1:8765/lento
# curl: (28) Operation timed out after 2000 milliseconds with 0 bytes received

# Reintentos: /inestable falla 2 de cada 3 veces con 503 y Retry-After: 1
curl -sS --retry 3 --retry-delay 1 --retry-all-errors http://127.0.0.1:8765/inestable
# (dos 503 impresos) y al tercer intento: {"ok": true, "intento": 3}

# Solo el código y los tiempos
curl -s -o /dev/null -w "code=%{http_code} ttfb=%{time_starttransfer}s total=%{time_total}s\n" http://127.0.0.1:8765/api/v1/libros/1
# code=200 ttfb=0.000510s total=0.000555s

# Autenticación: sin token → 401 con WWW-Authenticate
curl -si http://127.0.0.1:8765/api/v1/yo | head -1      # HTTP/1.1 401 Unauthorized
curl -s http://127.0.0.1:8765/api/v1/yo -H 'Authorization: Bearer token_de_prueba_123'
# {"usuario": "yafer", "rol": "lector"}
```

```bash
# Bonus: procesar el JSON con jq y guardar un token en una variable
TOKEN=$(curl -s https://api.ejemplo.dev/login --json '{"usuario":"yafer","clave":"cambia_esto"}' | jq -r .access_token)
curl -s https://api.ejemplo.dev/v1/yo -H "Authorization: Bearer $TOKEN" | jq '.usuario'
```

⚠️ Cuidado: lo que escribes en la terminal queda en el historial (`history`) y en la lista de procesos. Para claves reales usa variables de entorno o `-H @archivo` / `--netrc`, no las pegues sueltas.

### 🥧 HTTPie, Postman, Bruno e Insomnia

| Herramienta | Qué es | Gusta por | Cuidado |
|---|---|---|---|
| `curl` | CLI universal | Está en todos lados, scripts | Sintaxis áspera |
| HTTPie (`http`) | CLI amigable | `http POST url nombre=Ana` con color y JSON automático | Hay que instalarlo |
| Postman | App gráfica | Colecciones, entornos, tests, equipos | Pide cuenta y se volvió pesado |
| Bruno | App gráfica open source | Colecciones como archivos de texto (van a git), sin nube | Más joven |
| Insomnia | App gráfica | Ligera, soporta GraphQL/gRPC | Tuvo polémica por forzar cuenta en 2023 |
| Extensiones del editor | REST Client / Thunder Client (VS Code), archivos `.http` | Pruebas junto al código | Menos funciones |

```bash
# HTTPie (pip install httpie): lo mismo que el curl de arriba, más corto
http POST :8765/api/v1/libros Authorization:'Bearer token_de_prueba_123' titulo='Aluvión de fuego' autor='Óscar Cerruto' anio:=1935
# := manda número/JSON real; = manda texto
```

```text
### archivo requests.http (extensión REST Client de VS Code o JetBrains): vive en tu repo
@base = http://127.0.0.1:8765

GET {{base}}/api/v1/libros?limite=2

###
POST {{base}}/api/v1/libros
Authorization: Bearer token_de_prueba_123
Content-Type: application/json

{ "titulo": "Juan de la Rosa", "autor": "Nataniel Aguirre" }
```

![Logotipo de Postman (marca de Postman Inc.; logotipo simple alojado en Wikimedia Commons)](img/apis/postman-logo.png)

💡 Consejo: para un equipo, guarda las colecciones **en el repositorio** (Bruno o archivos `.http`), así se versionan junto al código y sirven de documentación ejecutable.

### 🔎 DevTools → pestaña Network

Es tu mejor herramienta para depurar un frontend: abre con `F12` (o `Ctrl+Shift+I`) y ve a **Network**.

- **Filtros**: `Fetch/XHR` muestra solo las llamadas a APIs; escribe texto para filtrar por URL.
- **Columnas útiles**: Status, Method, Type, Size, Time y Waterfall (cascada de tiempos).
- **Clic en un request**: pestañas Headers (request y response), Payload (lo que enviaste), Preview/Response (lo que volvió), Timing (DNS, conexión, TLS, espera, descarga) y Cookies.
- **Clic derecho → Copy → Copy as cURL**: reproduce el pedido **exacto** en la terminal, con cookies y token. Mágico para aislar si el problema es el front o el back.
- **Disable cache** (con DevTools abierto) y **Throttling** (simular 3G/offline) para ver cómo se porta tu app con mala conexión.
- **Preserve log**: no borra la lista al navegar o redirigir.
- Los requests **preflight** CORS aparecen como `OPTIONS`; si falla, mira ese primero.

```flujo
Falla algo en la web -> Network (F12) : ¿se hizo el request?
Network (F12) -> Status 4xx/5xx : leer Response
Network (F12) -> En rojo / CORS : mirar OPTIONS y headers
Network (F12) -> Copy as cURL : reproducir en terminal
Copy as cURL -> Aislado : ¿falla igual? es el backend
```

🇬🇧 **payload** /péiloud/ = carga enviada · **waterfall** /uóterfol/ = cascada · **throttling** /zrótling/ = limitar la velocidad · **collection** /colékshon/ = colección de requests

## 💻 Consumir APIs desde JavaScript y Python

Lo importante no es hacer el request (eso es una línea), sino todo lo que lo rodea: **timeout, errores HTTP, reintentos, JSON inválido y cancelación**. Ahí se rompen las apps reales.

### 🟨 JavaScript: fetch

```js
// ❌ El código "feliz" que se ve en tutoriales
const res = await fetch("/api/v1/libros/99");
const libro = await res.json();      // ¡fetch NO lanza error con 404 o 500!
console.log(libro.titulo);           // undefined... o explota en el siguiente paso
```

⚠️ Cuidado: `fetch` solo rechaza la promesa si falla la **red** (sin conexión, DNS, CORS). Un `404` o `500` es una respuesta "exitosa" para fetch: debes mirar `res.ok` o `res.status`.

```js
// ✅ cliente.mjs — timeout + reintentos con backoff + errores claros (ejecutado con Node 26)
const BASE = "http://127.0.0.1:8765";
const esperar = (ms) => new Promise((r) => setTimeout(r, ms));

class ErrorHttp extends Error {
  constructor(res, cuerpo) {
    super(`${res.status} ${cuerpo?.title ?? res.statusText}: ${cuerpo?.detail ?? ""}`);
    this.status = res.status;
    this.cuerpo = cuerpo;
  }
}

async function pedir(ruta, { metodo = "GET", datos, token, intentos = 3, timeoutMs = 3000 } = {}) {
  for (let intento = 1; ; intento++) {
    try {
      const res = await fetch(BASE + ruta, {
        method: metodo,
        headers: {
          Accept: "application/json",
          ...(datos && { "Content-Type": "application/json" }),
          ...(token && { Authorization: `Bearer ${token}` }),
        },
        body: datos ? JSON.stringify(datos) : undefined,
        signal: AbortSignal.timeout(timeoutMs),   // ⏱️ sin esto fetch puede esperar casi para siempre
      });
      if (res.ok) return res.status === 204 ? null : await res.json();
      const cuerpo = await res.json().catch(() => null);
      const reintentable = [429, 502, 503, 504].includes(res.status);
      if (!reintentable || intento >= intentos) throw new ErrorHttp(res, cuerpo);
      const retryAfter = Number(res.headers.get("Retry-After")) * 1000;
      const espera = retryAfter || 2 ** intento * 200 + Math.random() * 100;   // backoff + jitter
      console.log(`  intento ${intento}: ${res.status}, reintento en ${Math.round(espera)} ms`);
      await esperar(espera);
    } catch (e) {
      if (e instanceof ErrorHttp) throw e;                 // 4xx: no tiene sentido reintentar
      if (intento >= intentos) throw e;                    // TimeoutError o "fetch failed"
      console.log(`  intento ${intento}: ${e.name}, reintento`);
      await esperar(2 ** intento * 200);
    }
  }
}

console.log(await pedir("/api/v1/libros/2"));
console.log(await pedir("/inestable"));
try { await pedir("/api/v1/libros/99"); } catch (e) { console.log("Error:", e.message); }
try { await pedir("/lento", { intentos: 1, timeoutMs: 1000 }); } catch (e) { console.log("Error:", e.name); }
```

```text
{ id: 2, titulo: 'Raza de bronce', autor: 'Alcides Arguedas', anio: 1919 }
  intento 1: 503, reintento en 1000 ms        ← respetó Retry-After: 1
  intento 2: 503, reintento en 1000 ms
{ ok: true, intento: 3 }
Error: 404 Not Found: No existe el libro 99   ← 404: no reintenta
Error: TimeoutError                           ← /lento tarda 5 s, cortamos a 1 s
```

- `AbortSignal.timeout(ms)` :: Cancela el request al pasar el tiempo (lanza `TimeoutError`)
- `AbortController` :: Cancelar a mano (ej. el usuario escribe otra letra en el buscador)
- `Promise.all([...])` :: Varios requests en paralelo (si uno falla, falla todo); `allSettled` espera a todos
- `res.json()` :: Lanza error si el cuerpo no es JSON válido (por ejemplo una página HTML de error de un proxy)
- `await res.text()` :: Leer el cuerpo como texto cuando depuras

💡 Consejo: en React, no hagas `fetch` a mano en cada componente: usa **TanStack Query** (o SWR): da caché, reintentos, estados de carga/error y deduplica requests.

### 🐍 Python: requests y httpx

```python
# cliente.py — requests con Session, reintentos automáticos y timeouts (ejecutado en este PC)
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE = "http://127.0.0.1:8765"

def crear_sesion() -> requests.Session:
    s = requests.Session()                      # reutiliza conexiones TCP (keep-alive): más rápido
    reintentos = Retry(
        total=3,
        backoff_factor=0.5,                     # 0.5 s, 1 s, 2 s...
        status_forcelist=[429, 502, 503, 504],
        allowed_methods=["GET", "PUT", "DELETE"],   # solo idempotentes (POST NO)
        respect_retry_after_header=True,
    )
    s.mount("http://", HTTPAdapter(max_retries=reintentos))
    s.mount("https://", HTTPAdapter(max_retries=reintentos))
    s.headers.update({"Accept": "application/json", "User-Agent": "mi-app/1.0"})
    return s

s = crear_sesion()
TIMEOUT = (3.05, 10)      # (conectar, leer) en segundos. SIEMPRE pon timeout.

r = s.get(f"{BASE}/api/v1/libros", params={"limite": 2}, timeout=TIMEOUT)
r.raise_for_status()      # convierte 4xx/5xx en excepción HTTPError
print(r.status_code, [l["titulo"] for l in r.json()["datos"]])
# 200 ['Cien años de soledad', 'Raza de bronce']

r = s.get(f"{BASE}/inestable", timeout=TIMEOUT)     # 503, 503 → reintenta solo → 200
print(r.status_code, r.json())                      # 200 {'ok': True, 'intento': 9}

r = s.get(f"{BASE}/api/v1/libros/99", timeout=TIMEOUT)
if not r.ok:
    err = r.json()
    print(r.status_code, r.headers["Content-Type"], "->", err["detail"])
# 404 application/problem+json; charset=utf-8 -> No existe el libro 99

try:
    s.get(f"{BASE}/lento", timeout=(3.05, 1))
except requests.exceptions.RequestException as e:
    # OJO: tras agotar los reintentos, el timeout llega como ConnectionError (MaxRetryError por dentro)
    print("Falló:", type(e).__name__)               # Falló: ConnectionError

r = s.post(f"{BASE}/api/v1/libros", json={"titulo": "Los deshabitados", "autor": "Marcelo Quiroga Santa Cruz", "anio": 1959},
           headers={"Authorization": "Bearer token_de_prueba_123", "Idempotency-Key": "b1e9-pedido-77"}, timeout=TIMEOUT)
print(r.status_code, r.headers["Location"], r.json()["id"])    # 201 /api/v1/libros/4 4
```

⚠️ Cuidado: `requests.get(url)` **sin `timeout`** puede esperar para siempre: es el error más común de Python con APIs. Un servicio remoto colgado deja tus hilos esperando hasta tumbar tu propia app.

```python
# httpx: misma idea que requests pero con async (y HTTP/2 opcional). pip install httpx  (probado con 0.28)
import asyncio, httpx

async def main():
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8765",
                                 timeout=httpx.Timeout(5.0, connect=2.0)) as cliente:
        # 3 pedidos EN PARALELO: tardan lo que el más lento, no la suma
        respuestas = await asyncio.gather(*(cliente.get(f"/api/v1/libros/{i}") for i in (1, 2, 3)))
        for r in respuestas:
            print(r.status_code, r.json()["titulo"])
        try:
            await cliente.get("/lento", timeout=1.0)
        except httpx.TimeoutException as e:
            print("Timeout:", type(e).__name__)      # Timeout: ReadTimeout

asyncio.run(main())
# 200 Cien años de soledad · 200 Raza de bronce · 200 Juan de la Rosa
```

| | `requests` | `httpx` | `aiohttp` | `urllib` (stdlib) |
|---|---|---|---|---|
| Async | No | Sí y sync | Sí | No |
| HTTP/2 | No | Sí (opcional) | No | No |
| Timeout por defecto | **Ninguno** | 5 s | 5 min total | Ninguno |
| Úsalo para | Scripts, lo clásico | Proyectos nuevos | Servidores muy concurrentes | Sin dependencias |

📌 Resumen de un buen cliente: **timeout siempre · revisar el código de estado · reintentar solo lo idempotente (o con Idempotency-Key) · backoff con jitter · respetar Retry-After · reutilizar conexiones · loguear el error con el request-id**.
🇬🇧 **timeout** /táimaut/ = tiempo de espera límite · **abort** /abórt/ = abortar · **session** /séshon/ = sesión de conexión reutilizable · **retry** /ritrái/ = reintentar · **raise for status** /réis for stéitus/ = lanzar error si el estado es malo

## 💥 Errores comunes de otros programadores

Estos errores se repiten en equipos de todos los tamaños. Cada uno tiene causa, consecuencia y solución.

| Error | Consecuencia | Cómo evitarlo |
|---|---|---|
| Sin timeout en el cliente | Hilos colgados, app congelada cuando el otro servicio se atasca | Timeout de conexión y lectura en **toda** llamada |
| Reintentar sin límite ni pausa | Tormenta de requests que tumba al servidor (thundering herd) | Backoff exponencial + jitter + máximo de intentos |
| Responder `200` con el error dentro (`{"ok": false}`) | Clientes, monitoreo, caché y CDN creen que todo va bien | Usa 4xx/5xx reales y `problem+json` |
| Exponer de más (`SELECT *` → JSON) | Se filtran hashes de contraseñas, emails, campos internos | DTO/serializador con lista **explícita** de campos |
| IDs secuenciales sin chequear dueño (BOLA) | Cualquiera lee datos de otros cambiando el número | Verifica propiedad en cada objeto; IDs no adivinables |
| Romper compatibilidad sin avisar | Apps móviles viejas dejan de funcionar | Versiona, añade en vez de cambiar, anuncia deprecaciones (`Deprecation`, `Sunset`) |
| Claves de API en el frontend o en git | Te gastan la cuota o te cobran miles | Backend como intermediario; secret scanning; rotar |
| `Access-Control-Allow-Origin: *` con datos privados | Otros sitios leen datos del usuario | Lista blanca de orígenes |
| Sin límite de tamaño ni paginación | Una consulta devuelve 2 GB y tumba el servidor | Límite máximo de página y de cuerpo |
| POST de pago sin idempotencia | Doble cobro al reintentar | `Idempotency-Key` |
| Confiar en el cliente (precio, rol, id en el body) | Compras a precio 0, escalada a admin | Recalcula y valida todo en el servidor |
| Ignorar el JSON inválido o campos faltantes | 500 con stack trace | Validar el esquema → 400/422 claro |
| Loguear tokens, contraseñas y datos personales | Fuga de secretos desde los logs | Enmascarar headers `Authorization` y campos sensibles |
| Usar HTTP en vez de HTTPS | Tokens y cookies legibles en Wi-Fi públicas | HTTPS siempre + HSTS |

::: columnas
### ❌ 200 con el error dentro
```json
HTTP/1.1 200 OK

{ "ok": false,
  "error": "Usuario no encontrado" }
```
- El monitoreo no ve errores
- La caché guarda el error
- El cliente debe adivinar
::: siguiente
### ✅ El código dice la verdad
```json
HTTP/1.1 404 Not Found
Content-Type: application/problem+json

{ "title": "Not Found",
  "status": 404,
  "detail": "No existe el usuario 42" }
```
- Todos los clientes lo entienden
- Las métricas funcionan
:::

::: columnas
### ❌ Devolver el objeto de la base entero
```json
{ "id": 7, "nombre": "Ana",
  "email": "ana@x.com",
  "password_hash": "$2b$12$...",
  "es_admin": false,
  "token_reset": "9c1f..." }
```
::: siguiente
### ✅ Solo lo que el cliente necesita
```json
{ "id": "usr_7Hk2",
  "nombre": "Ana" }
```
- Lista explícita de campos
- El resto se queda en el servidor
:::

### 📰 Incidentes reales para aprender

- **Parler (enero de 2021)**: según los informes de la época, su API permitía recorrer los posts por IDs predecibles sin autenticación suficiente, y un grupo de archivistas los descargó masivamente. Lección: IDs predecibles + falta de autorización por objeto + sin rate limiting.
- **Facebook / Cambridge Analytica (2018)**: la API de Graph permitía a apps de terceros leer datos de los amigos de quien usaba la app. Lección: scopes mínimos y auditoría de permisos de terceros.
- **T-Mobile (enero de 2023)**: la empresa informó (formulario 8-K) que un atacante obtuvo datos básicos de unos 37 millones de cuentas a través de una API, durante semanas antes de ser detectado. Lección: las APIs también necesitan monitoreo y autenticación estricta.
- **Steam (diciembre de 2015)**: una mala configuración de caché sirvió páginas de usuarios a otros. Lección: respuestas personalizadas con `Cache-Control: private`/`no-store`.
- **Tormentas de reintentos**: varios cortes grandes de servicios en la nube se agravaron porque miles de clientes reintentaban sin backoff. Lección: jitter y circuit breakers.

📌 El **OWASP API Security Top 10** (edición 2023) es la lista de referencia: BOLA, autenticación rota, exposición excesiva de propiedades, consumo ilimitado de recursos, autorización rota a nivel de función, mala configuración de seguridad, SSRF, entre otros. Léela una vez: vale oro en entrevistas.

⚠️ Cuidado: **SSRF** (Server-Side Request Forgery): si tu API recibe una URL y hace el request por el usuario (`POST /importar {"url": "..."}`), podrían hacer que tu servidor pida `http://169.254.169.254/` (credenciales de la nube) o servicios internos. Valida con lista blanca y bloquea IPs privadas.
🇬🇧 **leak** /lik/ = fuga · **over-exposure** /óver expósher/ = exposición excesiva · **breaking change** /bréiking chéinch/ = cambio incompatible · **deprecation** /deprikéishon/ = anuncio de retiro · **sunset** /sánset/ = fecha de apagado

## 🆚 Cómo elegir (comparativa y futuro)

### 🧭 Elegir el estilo de API

| Situación | Elige | Por qué NO otra |
|---|---|---|
| API pública para terceros, CRUD típico | REST + OpenAPI | GraphQL complica caché y límites; gRPC no corre en navegadores |
| Frontend complejo (móvil + web) con muchas pantallas anidadas | GraphQL | REST obliga a muchos endpoints o a traer de más |
| Microservicios internos, baja latencia | gRPC | JSON es más pesado y sin contrato fuerte |
| Monorepo full-stack TypeScript | tRPC o server actions | Evita escribir contratos a mano |
| Notificaciones en vivo del servidor | SSE | WebSocket es más complejo si solo empujas |
| Chat, juegos, edición colaborativa | WebSocket | SSE es de un solo sentido |
| Que otro sistema te avise de eventos | Webhooks | Hacer polling cada segundo desperdicia recursos |
| Streaming de respuestas de IA | SSE (así lo hacen las APIs de IA) | WebSocket no hace falta |

### 🚀 Hacia dónde va

- 🚀 Futuro: **HTTP/3 y QUIC** se generalizan: ya lo habla buena parte del tráfico de las grandes CDN; para ti es transparente.
- 🚀 Futuro: **APIs para agentes de IA**: el protocolo **MCP** (Model Context Protocol, publicado por Anthropic en noviembre de 2024 y adoptado por varios proveedores) estandariza cómo un modelo descubre y llama herramientas; es una API con descubrimiento automático. Los modelos también consumen APIs vía function calling, así que un buen OpenAPI y errores claros importan más.
- 🚀 Futuro: **Passkeys** (WebAuthn) reemplazan contraseñas; **OAuth 2.1** consolida PKCE obligatorio.
- 🚀 Futuro: **Edge computing**: funciones que corren cerca del usuario (Cloudflare Workers, Vercel Edge, Deno Deploy).
- 🚀 Futuro: **Contrato primero**: OpenAPI y AsyncAPI (para eventos) generan docs, SDKs, mocks y pruebas automáticamente.
- 🚀 Futuro: **Seguridad post-cuántica** en TLS (ya visto en la salida de `curl -v`: `X25519MLKEM768`).
- **Tendencia estable**: REST/JSON sigue siendo, por mucho, lo más usado en APIs públicas; GraphQL y gRPC cubren nichos concretos (y muy importantes).

```tiempo
2000 : REST (tesis de Roy Fielding)
2006 : APIs públicas de Amazon S3, Twitter, Facebook
2011 : WebSockets estandarizados (RFC 6455, 2011)
2012 : OAuth 2.0 (RFC 6749)
2015 : GraphQL público, gRPC de código abierto, HTTP/2
2017 : OpenAPI 3.0 (Swagger pasa a ser OpenAPI)
2022 : HTTP/3 estandarizado (RFC 9114)
2024 : MCP, TLS híbrido post-cuántico en navegadores
2026 : APIs consumidas también por agentes de IA
```

## 🎯 APIs públicas para practicar

Todas gratuitas y sin clave (verifica los términos y la disponibilidad actuales, pueden cambiar):

| API | Qué ofrece | Prueba |
|---|---|---|
| JSONPlaceholder | Posts, usuarios, todos falsos (CRUD simulado) | `curl https://jsonplaceholder.typicode.com/posts/1` |
| httpbin.org | Espeja tu request: headers, auth, códigos, delays | `curl 'https://httpbin.org/get?ciudad=Cochabamba'` |
| PokéAPI | Datos de Pokémon, paginados | `curl https://pokeapi.co/api/v2/pokemon/pikachu` |
| Open-Meteo | Clima por coordenadas | `curl 'https://api.open-meteo.com/v1/forecast?latitude=-17.39&longitude=-66.16&current_weather=true'` |
| GitHub REST | Repos, usuarios, issues (60 req/h sin token) | `curl https://api.github.com/users/torvalds` |
| REST Countries | Datos de países | `curl -L https://restcountries.com/v3.1/name/bolivia` |
| Countries GraphQL | Práctica de GraphQL | Ver la consulta de la sección GraphQL |
| Wikipedia REST | Resúmenes de artículos | `curl https://es.wikipedia.org/api/rest_v1/page/summary/Cochabamba` |
| dog.ceo, catfact.ninja | APIs divertidas | `curl https://catfact.ninja/fact` |

```bash
# Ejemplo real de esta sesión: JSONPlaceholder
curl -s https://jsonplaceholder.typicode.com/posts/1
# {"userId": 1, "id": 1, "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit", "body": "quia et suscipit..."}

# httpbin refleja lo que mandas: ideal para ver tus headers
curl -s 'https://httpbin.org/get?ciudad=Cochabamba' -H 'Accept: application/json'
# {"args": {"ciudad": "Cochabamba"}, "headers": {"Accept": "application/json", "Host": "httpbin.org", ...}, ...}

# Un 418 de verdad
curl -s -o /dev/null -w "%{http_code}\n" https://httpbin.org/status/418     # 418
```

💡 Consejo: monta tu **propio** servidor de práctica, como el de esta hoja, en 40 líneas con `http.server` o FastAPI: ver ambos lados (cliente y servidor) es lo que te convierte en backend.

## 🏋️ Ejercicios prácticos

Usa la API de prueba de la hoja (`python3 servidor.py`, puerto 8765) o las APIs públicas. Intenta primero; luego abre la solución.

### 1️⃣ Fácil: lee un recurso y su código

Con curl, pide el libro 3 y muestra **solo** el código de estado. Luego pide el libro 99 y observa el código y el `Content-Type`.

::: desplegable 🧩 Ver la solución
```bash
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8765/api/v1/libros/3     # 200
curl -si http://127.0.0.1:8765/api/v1/libros/99 | head -5
# HTTP/1.1 404 Not Found
# Content-Type: application/problem+json; charset=utf-8
```
`-o /dev/null` descarta el cuerpo y `-w` imprime una plantilla con variables de curl. El 404 llega con formato `problem+json`, como recomienda la RFC 9457.
:::

### 2️⃣ Fácil: arma una URL sin romperla

Construye en JS la URL `https://api.ejemplo.dev/v1/buscar` con los parámetros `q = "café & té"` y `pagina = 2`.

::: desplegable 🧩 Ver la solución
```js
const url = new URL("https://api.ejemplo.dev/v1/buscar");
url.searchParams.set("q", "café & té");
url.searchParams.set("pagina", 2);
console.log(url.href);   // https://api.ejemplo.dev/v1/buscar?q=caf%C3%A9+%26+t%C3%A9&pagina=2
```
`URLSearchParams` codifica el `&` y las tildes por ti. Concatenar strings (`"?q=" + texto`) permite inyectar parámetros.
:::

### 3️⃣ Medio: ¿idempotente o no?

Clasifica y justifica: `GET /libros/2`, `PUT /libros/2`, `POST /libros`, `DELETE /libros/2`, `PATCH /contador {"sumar": 1}`.

::: desplegable 🧩 Ver la solución
| Request | ¿Idempotente? | Por qué |
|---|---|---|
| `GET /libros/2` | Sí | Solo lee |
| `PUT /libros/2` | Sí | Dejar el recurso con el mismo contenido da el mismo estado |
| `POST /libros` | No | Cada llamada crea otro libro (usa Idempotency-Key) |
| `DELETE /libros/2` | Sí | Tras borrar, el estado es el mismo aunque el 2.º devuelva 404 (probado: 204 y 204 en nuestra API) |
| `PATCH /contador {"sumar":1}` | No | Cada llamada incrementa; `{"valor": 5}` sí sería idempotente |
:::

### 4️⃣ Medio: pagina todos los libros

Escribe un script Python que recorra **todas** las páginas de `/api/v1/libros?limite=2` siguiendo el cursor `paginacion.siguiente` hasta que sea `null`, e imprima los títulos.

::: desplegable 🧩 Ver la solución
```python
import requests

BASE = "http://127.0.0.1:8765"
url = "/api/v1/libros?limite=2"
with requests.Session() as s:
    while url:
        r = s.get(BASE + url, timeout=(3, 10))
        r.raise_for_status()
        cuerpo = r.json()
        for libro in cuerpo["datos"]:
            print(libro["id"], libro["titulo"])
        url = cuerpo["paginacion"]["siguiente"]     # None cuando no hay más
```
Idea clave: el cliente no calcula páginas, **sigue el enlace** que da el servidor. Si el servidor cambia cómo pagina, tu cliente no se rompe.
:::

### 5️⃣ Medio: ETag y 304

Pide un libro, guarda su ETag y vuelve a pedirlo con `If-None-Match`. ¿Qué código recibes y cuántos bytes de cuerpo?

::: desplegable 🧩 Ver la solución
```bash
ET=$(curl -s -D - -o /dev/null http://127.0.0.1:8765/api/v1/libros/1 | grep -i '^etag' | cut -d' ' -f2 | tr -d '\r')
curl -si -H "If-None-Match: $ET" http://127.0.0.1:8765/api/v1/libros/1
# HTTP/1.1 304 Not Modified   (sin cuerpo)
```
Un 304 ahorra el cuerpo (87 bytes aquí; en una lista grande, megas). El navegador hace esto solo cuando la respuesta trae ETag.
:::

### 6️⃣ Difícil: cliente resistente

Escribe una función `pedir(url)` en JS o Python que: tenga timeout de 3 s, reintente hasta 3 veces solo en 429/502/503/504 o error de red, respete `Retry-After`, use backoff con jitter y lance un error claro en los 4xx. Pruébala contra `/inestable` (falla 2 de cada 3 veces) y `/lento` (cuelga 5 s).

::: desplegable 🧩 Ver la solución
Es el cliente de la sección "Consumir APIs desde JavaScript y Python" (`cliente.mjs` / `cliente.py`). Resultado real contra `/inestable`: dos 503 con espera de 1 s (por `Retry-After: 1`) y un 200 al tercer intento; contra `/lento`, `TimeoutError` al segundo. Puntos clave que debes poder explicar: por qué NO se reintenta un 404, por qué el POST necesita Idempotency-Key y por qué el jitter evita la estampida.
:::

### 7️⃣ Difícil: protege el endpoint

Añade a la API de FastAPI de la hoja autenticación con un Bearer token (header `Authorization`) y asegúrate de que un usuario solo pueda ver **sus** libros (evita BOLA).

::: desplegable 🧩 Ver la solución
```python
from fastapi import Depends, HTTPException, Header

USUARIOS = {"token_ana_123": 1, "token_luis_456": 2}      # token falso de ejemplo → id usuario

def usuario_actual(authorization: str = Header(default="")) -> int:
    esquema, _, token = authorization.partition(" ")
    if esquema != "Bearer" or token not in USUARIOS:
        raise HTTPException(401, "Token inválido", headers={"WWW-Authenticate": "Bearer"})
    return USUARIOS[token]

@app.get("/api/v1/libros/{libro_id}")
def leer(libro_id: int, uid: int = Depends(usuario_actual)):
    libro = LIBROS.get(libro_id)
    if libro is None or libro.dueno_id != uid:          # mismo 404: no confirma que existe
        raise HTTPException(404, "No existe")
    return libro
```
Se necesita un campo `dueno_id` en `Libro`. En producción: tokens JWT con expiración (librería `jose` / `pyjwt`) y comparación de hashes, no tokens fijos.
:::

### 8️⃣ Difícil: verifica un webhook

Un proveedor te envía `POST /webhooks` con el header `X-Firma: <hmac sha256 en hex del cuerpo>`. Escribe la verificación segura.

::: desplegable 🧩 Ver la solución
```python
import hmac, hashlib

SECRETO = b"cambia_esto_secreto_del_webhook"

def firma_valida(cuerpo_crudo: bytes, firma_recibida: str) -> bool:
    esperada = hmac.new(SECRETO, cuerpo_crudo, hashlib.sha256).hexdigest()
    return hmac.compare_digest(esperada, firma_recibida)    # tiempo constante

# Importante: firmar los BYTES CRUDOS del cuerpo, antes de parsearlo a JSON.
```
Dos detalles que fallan en la práctica: (1) reserializar el JSON cambia los bytes y la firma ya no coincide; (2) comparar con `==` filtra información por tiempo. Además guarda el ID del evento para ignorar repeticiones.
:::

## 🎤 Preguntas de entrevista

::: desplegable 🎤 ¿Qué pasa cuando escribes una URL en el navegador y das Enter?
Caché local y HSTS → **DNS** traduce el dominio a IP → **TCP** (3-way handshake) → **TLS** (certificado, claves, ALPN) → **HTTP** request → el servidor (tras CDN/balanceador) procesa y responde → el navegador parsea el HTML y pide CSS/JS/imágenes (reutilizando la conexión) → renderiza. Con HTTP/3, TCP+TLS se reemplazan por QUIC (1 RTT). Bonus: mencionar caché, keep-alive y que el fragmento `#` no se envía.
:::

::: desplegable 🎤 ¿Diferencia entre PUT, PATCH y POST?
`POST` crea (o ejecuta una acción), no es idempotente. `PUT` **reemplaza** el recurso completo y es idempotente. `PATCH` modifica solo algunos campos (idempotente según cómo se use). Si usas PUT con campos faltantes, los pierdes.
:::

::: desplegable 🎤 ¿401 vs 403? ¿400 vs 422?
401: no autenticado (falta o es inválido el token; incluye `WWW-Authenticate`). 403: autenticado pero sin permiso. 400: request mal formado (JSON roto, tipos incorrectos). 422: JSON válido pero que no cumple las reglas de negocio/validación. Muchos equipos usan 400 para ambos; lo importante es ser consistente.
:::

::: desplegable 🎤 ¿Qué significa que HTTP es stateless? ¿Cómo se mantiene la sesión?
Cada request es independiente: el servidor no guarda memoria entre ellos. El estado se simula con **cookies de sesión** (ID aleatorio, estado en el servidor) o **tokens** (JWT) que el cliente manda en cada request. Ventaja: cualquier servidor puede atender cualquier request, así se escala horizontalmente.
:::

::: desplegable 🎤 ¿Qué es CORS y por qué existe? ¿Lo protege curl?
Es el mecanismo con el que un servidor indica qué **orígenes** pueden leer sus respuestas desde JS del navegador, para relajar la Same-Origin Policy (que evita que un sitio malicioso use tus cookies para leer otro sitio). Lo aplica **solo el navegador**; curl o un backend no lo respetan, así que CORS no es seguridad de la API sino protección del usuario. Preflight: `OPTIONS` previo para métodos/headers no simples.
:::

::: desplegable 🎤 ¿Cómo evitarías cobrar dos veces si el cliente reintenta un POST?
Con una **Idempotency-Key** (UUID generado por el cliente por operación). El servidor guarda la respuesta junto a la clave (con caducidad, y en una transacción/constraint única) y, si recibe la misma clave, devuelve la misma respuesta sin repetir el efecto. Además, validar que el cuerpo coincida con el de la primera vez.
:::

::: desplegable 🎤 REST vs GraphQL vs gRPC: ¿cuándo cada uno?
REST para APIs públicas y CRUD (caché HTTP, simple, universal). GraphQL cuando muchos clientes con necesidades distintas piden datos anidados (evita over/under-fetching) a cambio de complejidad (N+1, caché, límites de costo). gRPC entre microservicios (binario, contrato fuerte, streaming, baja latencia) pero poco práctico en navegadores.
:::

::: desplegable 🎤 ¿Cómo funciona OAuth 2.0 con PKCE? ¿Qué problema resuelve PKCE?
Authorization Code: la app redirige al proveedor con `code_challenge = SHA256(code_verifier)`; el usuario se autentica y consiente; el proveedor redirige con un `code`; la app lo canjea enviando el `code_verifier`; el proveedor comprueba el hash y entrega tokens. PKCE evita que alguien que intercepte el `code` (apps públicas, redirecciones) lo canjee, porque no conoce el verifier. OIDC añade el ID token para autenticación.
:::

::: desplegable 🎤 ¿JWT o sesiones? ¿Cómo revocas un JWT?
Sesión: estado en servidor, revocación inmediata, simple en webs propias. JWT: sin estado, escala entre servicios, pero no se revoca antes de `exp`. Mitigaciones: access tokens de 5-15 min, refresh token revocable y rotado, lista de revocación (jti) o versión de token por usuario. Nunca datos sensibles en la carga y siempre fijar el algoritmo al verificar.
:::

::: desplegable 🎤 ¿Cómo diseñarías la paginación de una API con millones de filas?
Paginación por **cursor/keyset** (`WHERE id > :ultimo ORDER BY id LIMIT n`), con índice, límite máximo de página y un cursor opaco en la respuesta (`siguiente`). Offset se degrada (recorre y descarta filas) y duplica o salta elementos si hay inserciones durante la navegación. Se pierde el "saltar a la página 50", que casi nunca importa.
:::

::: desplegable 🎤 ¿Cómo manejas fallos de una API externa en tu servicio?
Timeouts cortos, reintentos solo de operaciones idempotentes con backoff exponencial y jitter (respetando Retry-After), **circuit breaker**, límite de concurrencia (bulkhead), caché o valor de respaldo (fallback), y degradar la funcionalidad en lugar de caer. Más métricas y alertas, y trazas con un `request-id`.
:::

::: desplegable 🎤 ¿Qué cambios rompen la compatibilidad de una API?
Quitar o renombrar campos o endpoints, cambiar tipos o significados, volver obligatorio un campo antes opcional, cambiar códigos de estado o formatos de error. Agregar campos, endpoints o parámetros opcionales no rompe. Se gestiona con versionado, periodo de deprecación (`Deprecation`/`Sunset`) y pruebas de contrato.
:::

## 🇬🇧 Vocabulario en inglés del tema

| English | Suena | Español |
|---|---|---|
| endpoint | /éndpoint/ | punto de acceso de una API |
| request / response | /rikuést/ /rispóns/ | pedido / respuesta |
| header | /jéder/ | cabecera |
| payload / body | /péiloud/ /bódi/ | carga útil / cuerpo |
| status code | /stéitus kóud/ | código de estado |
| authentication | /ozentikéishon/ | autenticación (quién eres) |
| authorization | /ozoriséishon/ | autorización (qué puedes) |
| token | /tóuken/ | ficha/credencial |
| rate limit | /réit límit/ | límite de peticiones |
| retry / backoff | /ritrái/ /bákof/ | reintentar / espera creciente |
| timeout | /táimaut/ | tiempo límite |
| idempotent | /aidémpotent/ | repetible sin efecto extra |
| pagination | /pallinéishon/ | paginación |
| webhook | /uébjuk/ | llamada que te hace otro sistema |
| payload too large | /péiloud tu larch/ | cuerpo demasiado grande (413) |
| breaking change | /bréiking chéinch/ | cambio que rompe compatibilidad |
| cross-origin | /cros óriyin/ | entre orígenes distintos |
| load balancer | /lóud bálanser/ | balanceador de carga |
| reverse proxy | /rivérs próksi/ | proxy inverso (Nginx, Caddy) |
| SDK | /es di kei/ | kit de desarrollo (librería cliente) |

🇬🇧 Frases útiles en reuniones: "The API returns a 500 when the payload is empty." · "We need to version the endpoint to avoid breaking clients." · "Could you share the OpenAPI spec?" · "It's idempotent, so it's safe to retry." · "The token expired; refresh it."

## 📌 Resumen final (la chuleta de la chuleta)

```flujo
URL -> DNS : ¿qué IP?
DNS -> TCP : conectar
TCP -> TLS : cifrar
TLS -> HTTP : request / response
HTTP -> Tu código : JSON
```

- `GET / POST / PUT / PATCH / DELETE` :: Leer / crear / reemplazar / modificar / borrar. Seguros: GET, HEAD, OPTIONS. Idempotentes: GET, PUT, DELETE
- `200 201 204` :: Éxito / creado (+Location) / sin cuerpo
- `301 304` :: Movido para siempre / usa tu caché (ETag)
- `400 401 403 404 409 422 429` :: Mal formado / sin autenticar / sin permiso / no existe / conflicto / datos inválidos / demasiadas
- `500 502 503 504` :: Falló el servidor / proxy / caído / timeout del proxy
- `Authorization: Bearer <token>` :: Credenciales en el header
- `Content-Type / Accept` :: Formato que envías / formato que aceptas
- `Cache-Control, ETag, If-None-Match` :: Caché y revalidación
- `Idempotency-Key` :: Reintentar POST sin duplicar
- `Retry-After, 429` :: Rate limit: espera antes de reintentar
- `curl -sS --max-time 5 --retry 3 -i URL` :: El curl razonable de cada día

✅ Checklist al **consumir** una API: timeout · revisar `res.ok` · reintentos solo idempotentes · backoff + jitter · secretos en variables de entorno · manejar JSON inválido · loguear request-id.
✅ Checklist al **crear** una API: sustantivos y plurales · código de estado correcto · errores `problem+json` · paginación con cursor · versión en la URL · autenticación + autorización por objeto · rate limit · CORS con lista blanca · OpenAPI · HTTPS · no exponer campos internos.
📌 Recuerda: **la API es un contrato**. Agregar es fácil; quitar rompe a alguien. Diseña pensando en el cliente que no puedes actualizar.
