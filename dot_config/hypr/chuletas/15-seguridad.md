# 🔐 Seguridad · Programar sin abrir puertas
> Entiende cada ataque para no dejarlo entrar: OWASP, inyecciones, XSS, CSRF, contraseñas, JWT, secretos, TLS, dependencias y la checklist antes de publicar.

## 🧠 Mentalidad de seguridad

La seguridad no es un producto que se instala al final: es una **forma de programar**. Cada línea que recibe datos de fuera (un formulario, una URL, un archivo, una cabecera HTTP, un JSON de otra API) es una puerta. El atacante no necesita que tu app esté "mal hecha" en general: le basta **una** puerta mal cerrada. Tú tienes que cerrarlas todas; él solo tiene que encontrar una. Por eso se trabaja con hábitos y capas, no con fe.

📌 Enfoque de esta hoja: **defensivo y educativo**. Cada ataque se explica lo justo para entender POR QUÉ funciona, siempre con el código vulnerable al lado del corregido. Practica solo en tus propios proyectos o en laboratorios hechos para eso (OWASP Juice Shop, DVWA, PortSwigger Web Security Academy). Atacar sistemas ajenos sin permiso escrito es delito en casi todos los países.

🧠 Concepto: **vulnerabilidad** = debilidad del sistema · **amenaza** = quién o qué podría aprovecharla · **exploit** = la técnica concreta que la aprovecha · **riesgo** = probabilidad × impacto.

### 🔺 La tríada CIA

Todo problema de seguridad rompe al menos una de estas tres propiedades (en inglés CIA: **Confidentiality, Integrity, Availability**):

| Propiedad | Pregunta | Se rompe cuando… | Defensa típica |
|---|---|---|---|
| 🔒 Confidencialidad | ¿Solo lo ven quienes deben? | Se filtra una base de datos | Cifrado, control de acceso |
| ✍️ Integridad | ¿Nadie lo cambió sin permiso? | Alguien edita su nota a 100 | Firmas, hashes, autorización |
| ⚡ Disponibilidad | ¿Funciona cuando se necesita? | Un DDoS tumba la web | Rate limiting, réplicas, backups |

💡 Consejo: cuando revises una funcionalidad pregunta las tres cosas: "¿alguien podría **ver**, **cambiar** o **tumbar** esto sin permiso?".

### 🗺️ Modelo de amenazas (threat modeling)

🧠 Concepto: **modelo de amenazas** = pensar ANTES de programar qué vale la pena proteger, quién lo atacaría, por dónde entraría y qué harás al respecto.

Cuatro preguntas (popularizadas por Adam Shostack) bastan para empezar:

1. ¿Qué estamos construyendo? (dibuja el flujo de datos)
2. ¿Qué puede salir mal? (recorre cada flecha y cada caja)
3. ¿Qué vamos a hacer al respecto? (mitigar, aceptar, transferir, eliminar)
4. ¿Lo hicimos bien? (revisar, probar)

```flujo
Usuario -> Navegador : escribe
Navegador -> API : HTTPS ⚠️ frontera
API -> BD : SQL ⚠️ inyección
API -> Pagos : API externa ⚠️ SSRF
API -> Logs : ⚠️ datos sensibles
```

Las **fronteras de confianza** (trust boundaries) son las líneas donde los datos pasan de "no confiable" a "confiable": del navegador a tu API, de tu API a la base, de un archivo subido a tu disco. Ahí van las validaciones.

Para la pregunta 2 se usa la lista **STRIDE** (de Microsoft):

| Letra | Amenaza | Ejemplo | Rompe |
|---|---|---|---|
| S | Spoofing (suplantar) | Entrar con la sesión de otro | Autenticación |
| T | Tampering (manipular) | Cambiar el precio en la petición | Integridad |
| R | Repudiation (negar) | "Yo no hice esa transferencia" | Registro (logs) |
| I | Information disclosure | Error que muestra la contraseña de la BD | Confidencialidad |
| D | Denial of service | 10 000 logins por segundo | Disponibilidad |
| E | Elevation of privilege | Un alumno se vuelve admin | Autorización |

### 🧅 Defensa en profundidad

Ninguna defensa es perfecta. La idea es poner **varias capas independientes**: si una falla, la siguiente frena o al menos detecta el ataque. Como un castillo: foso, muralla, guardias y caja fuerte.

```capas
Personas : MFA, formación contra phishing, revisión de código
Perímetro : firewall, WAF, rate limiting, HTTPS
Aplicación : validación, consultas parametrizadas, escapado, autorización
Datos : cifrado en reposo, hash de contraseñas, backups
Monitoreo : logs sin datos sensibles, alertas, respuesta a incidentes
```

⚠️ Cuidado: un WAF (Web Application Firewall) **no** reemplaza escribir código seguro. Es una capa extra, no la solución.

### 🔑 Mínimo privilegio y otros principios

🧠 Concepto: **mínimo privilegio** (least privilege) = cada usuario, proceso, token o contenedor tiene SOLO los permisos que necesita para su tarea, y nada más.

- **Mínimo privilegio**: la app usa un usuario de BD que puede `SELECT/INSERT` en sus tablas, no `DROP DATABASE`.
- **Denegar por defecto**: si no hay una regla que permita algo, se prohíbe (lista blanca, no lista negra).
- **Fallar de forma segura**: si el chequeo de permisos lanza un error, la respuesta es "denegado", nunca "pase".
- **No confiar en el cliente**: todo lo que llega del navegador o la app móvil puede estar manipulado.
- **Seguridad por diseño, no por oscuridad**: esconder la URL `/admin-secreto` no es protección.
- **Superficie de ataque mínima**: cada endpoint, puerto o dependencia que no usas es una puerta extra: quítalo.

```python
# ❌ Fallar abierto: si algo explota, deja pasar
def puede_editar(usuario, curso):
    try:
        return consultar_permiso(usuario, curso)
    except Exception:
        return True          # "para no molestar al usuario"... y deja pasar a cualquiera

# ✅ Fallar cerrado: ante la duda, denegar y registrar
def puede_editar(usuario, curso):
    try:
        return consultar_permiso(usuario, curso)
    except Exception:
        log.exception("Fallo al comprobar permiso de %s en %s", usuario.id, curso.id)
        return False
```

🇬🇧 **threat model** /zret módel/ = modelo de amenazas · **attack surface** /aták sérfis/ = superficie de ataque · **least privilege** /list prívilech/ = mínimo privilegio · **defense in depth** /difens in dez/ = defensa en profundidad

## 📋 OWASP Top 10

**OWASP** (Open Worldwide Application Security Project) es una fundación sin fines de lucro que publica guías gratuitas. Su **Top 10** es la lista de los riesgos más críticos en aplicaciones web, armada con datos de miles de aplicaciones analizadas. No es una norma completa, pero es el "temario mínimo" que todo programador web debería conocer y que aparece en entrevistas.

📌 La edición vigente es la **OWASP Top 10:2025** (publicada en noviembre de 2025, la primera desde 2021). Abajo va la tabla 2025 y un resumen de qué cambió respecto a 2021. Muchas empresas y apuntes siguen citando los códigos 2021, así que conviene conocer ambos.

| Código 2025 | Riesgo | En palabras simples | Sección de esta hoja |
|---|---|---|---|
| A01 | Broken Access Control (incluye SSRF) | Ves o haces lo que no te toca | 🚪 Autorización, 🛰️ SSRF |
| A02 | Security Misconfiguration | Configuración por defecto, debug activo | 🛡️ Cabeceras, 🐳 Docker |
| A03 | Software Supply Chain Failures | Dependencias y build sin confianza verificada | 🔗 Dependencias |
| A04 | Cryptographic Failures | Datos sin cifrar o mal cifrados | 🔑 Contraseñas, 🔒 TLS |
| A05 | Injection | Tu dato se ejecuta como código (SQL, XSS…) | 💉 SQL, 🕸️ XSS |
| A06 | Insecure Design | El diseño ya nace inseguro | 🧠 Mentalidad |
| A07 | Authentication Failures | Login débil, sesiones mal hechas | 🎫 Sesiones y JWT |
| A08 | Software or Data Integrity Failures | Confiar en código o datos sin verificar | 📦 Deserialización |
| A09 | Security Logging and Alerting Failures | No te enteras del ataque | 📜 Logs |
| A10 | Mishandling of Exceptional Conditions | Errores mal manejados: fallar abierto, filtrar datos | 🧠 Fallar cerrado |

💡 Consejo: cambios de 2021 a 2025: **Security Misconfiguration** sube del 5.º al 2.º puesto; **Software Supply Chain Failures** reemplaza y amplía a «Vulnerable and Outdated Components» (A06:2021); **Mishandling of Exceptional Conditions** es categoría nueva; **SSRF** (A10:2021) se absorbe en Broken Access Control; Injection baja del 3.º al 5.º y Cryptographic Failures del 2.º al 4.º. En 2021 el orden era: A01 Access Control, A02 Cryptographic Failures, A03 Injection, A04 Insecure Design, A05 Misconfiguration, A06 Vulnerable Components, A07 Identification and Authentication Failures, A08 Integrity Failures, A09 Logging and Monitoring Failures, A10 SSRF.

```tiempo
2003 : Primer OWASP Top 10
2013 : Edición 2013 (A1 = Injection)
2017 : Edición 2017 (entra XXE y deserialización)
2021 : Edición 2021 (A01 = Broken Access Control, entra SSRF)
2025 : Edición 2025 (entran Supply Chain y Exceptional Conditions; SSRF se integra en A01)
```

💡 Consejo: además del Top 10 web existen el **OWASP API Security Top 10** (para APIs REST/GraphQL, donde el número 1 es justamente BOLA, el IDOR de las APIs), el **OWASP Top 10 for LLM Applications** (prompt injection, etc.) y el **ASVS** (Application Security Verification Standard), una checklist detallada para auditar.

### 🧭 ¿Qué cambió de 2017 a 2021?

::: columnas
### 📉 Bajó o se fusionó
- Injection pasó del 1.º al 3.º puesto y absorbió a XSS.
- XXE (XML External Entities) se fusionó con Security Misconfiguration.
- Insecure Deserialization quedó dentro de A08.
::: siguiente
### 📈 Subió o entró
- Broken Access Control subió al n.º 1.
- Entró Insecure Design (pensar seguridad desde el diseño).
- Entró SSRF por la comunidad (encuestas), por su auge con la nube.
:::

🧠 Concepto: **CVE** (Common Vulnerabilities and Exposures) = identificador público de una vulnerabilidad concreta (ej. `CVE-2021-44228` es Log4Shell). **CWE** = tipo de debilidad (ej. `CWE-89` = inyección SQL). **CVSS** = puntaje de gravedad de 0 a 10.

## 💉 Inyección SQL

🧠 Concepto: **inyección** = el dato que envía el usuario termina siendo interpretado como **código** (SQL, comandos del sistema, LDAP, plantillas…). La raíz siempre es la misma: **mezclar datos y código en el mismo texto**.

![xkcd 327 «Exploits of a Mom»: el colegio pierde su tabla de alumnos por un nombre con SQL dentro (xkcd.com, CC BY-NC 2.5)](img/seguridad/xkcd-bobby-tables.png)

### 🔬 Por qué funciona

Si armas la consulta pegando strings, el motor de la base no puede saber dónde termina tu SQL y dónde empieza el texto del usuario. Una comilla `'` en el dato **cierra** tu string y lo que sigue se ejecuta como SQL.

```secuencia
actores: Atacante, API, BD
Atacante -> API : email = x' OR '1'='1
nota API : f"... WHERE email = '{email}'"
API -> BD : WHERE email = 'x' OR '1'='1'
nota BD : '1'='1' siempre es verdadero
BD --> API : TODAS las filas
API --> Atacante : datos de todos los usuarios
```

### ✅ Ejemplo resuelto: vulnerable vs parametrizado (ejecutado en este PC)

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE usuarios (id INTEGER PRIMARY KEY, email TEXT, rol TEXT)")
con.executemany("INSERT INTO usuarios (email, rol) VALUES (?, ?)", [
    ("ana@uni.bo", "alumno"), ("luis@uni.bo", "alumno"), ("admin@uni.bo", "admin"),
])

entrada = "x' OR '1'='1"          # lo que escribe el atacante en el buscador

# ❌ VULNERABLE: el dato se pega dentro del texto SQL
sql = f"SELECT email, rol FROM usuarios WHERE email = '{entrada}'"
print("SQL armado :", sql)
print("Vulnerable :", con.execute(sql).fetchall())

# ✅ PARAMETRIZADO: el dato viaja aparte, nunca se interpreta como SQL
print("Seguro     :", con.execute(
    "SELECT email, rol FROM usuarios WHERE email = ?", (entrada,)).fetchall())
```

```text
SQL armado : SELECT email, rol FROM usuarios WHERE email = 'x' OR '1'='1'
Vulnerable : [('ana@uni.bo', 'alumno'), ('luis@uni.bo', 'alumno'), ('admin@uni.bo', 'admin')]
Seguro     : []
```

Con la consulta parametrizada la base busca un usuario cuyo email sea **literalmente** `x' OR '1'='1`. No existe, así que devuelve vacío. El dato nunca toca el analizador de SQL.

### 🌐 Lo mismo en varios lenguajes

::: columnas
### ❌ Vulnerable
```js
// Node + pg
const r = await db.query(
  `SELECT * FROM notas WHERE alumno_id = ${req.query.id}`
);
```
```java
// Java JDBC
Statement st = con.createStatement();
st.executeQuery("SELECT * FROM notas WHERE alumno_id = " + id);
```
::: siguiente
### ✅ Parametrizado
```js
// Node + pg: $1, $2... son marcadores
const r = await db.query(
  "SELECT * FROM notas WHERE alumno_id = $1", [req.query.id]
);
```
```java
// Java JDBC: PreparedStatement
PreparedStatement ps = con.prepareStatement(
  "SELECT * FROM notas WHERE alumno_id = ?");
ps.setInt(1, id);
```
:::

| Lenguaje / librería | Marcador | Ejemplo seguro |
|---|---|---|
| Python `sqlite3` | `?` | `cur.execute("... = ?", (x,))` |
| Python `psycopg` | `%s` | `cur.execute("... = %s", (x,))` |
| Node `pg` | `$1` | `db.query("... = $1", [x])` |
| Node `mysql2` | `?` | `db.execute("... = ?", [x])` |
| Java JDBC | `?` | `PreparedStatement` |
| ORMs (Prisma, SQLAlchemy, Django) | automático | `User.objects.filter(email=x)` |

⚠️ Cuidado: en `psycopg` el `%s` se pasa como **segundo argumento**, NO con el operador `%` de Python. `cur.execute("... = %s" % x)` es igual de vulnerable que un f-string.

⚠️ Cuidado: los **nombres** de tablas, columnas u `ORDER BY` no se pueden parametrizar. Usa una **lista blanca**:

```python
COLUMNAS_ORDEN = {"nombre", "fecha", "nota"}          # lista blanca

def listar(orden: str):
    if orden not in COLUMNAS_ORDEN:
        orden = "fecha"                                # valor por defecto seguro
    return con.execute(f"SELECT * FROM notas ORDER BY {orden}").fetchall()
```

⚠️ Cuidado: los ORM protegen... hasta que usas su "escape hatch" de SQL crudo. `Model.objects.raw(f"...{x}...")`, `sequelize.query("..." + x)` o `prisma.$queryRawUnsafe(...)` vuelven a ser vulnerables. En Prisma, `$queryRaw` con plantilla etiquetada sí parametriza.

### 🐚 Inyección de comandos del sistema

Mismo error, otro intérprete: pegar el dato del usuario en un comando de shell.

::: columnas
### ❌ Vulnerable
```python
import os
# El usuario manda: "google.com; whoami"  (el shell ejecuta también el 2.º comando)
os.system(f"ping -c 1 {host}")
```
::: siguiente
### ✅ Corregido
```python
import subprocess
# Lista de argumentos, sin shell: ";" es solo texto
subprocess.run(["ping", "-c", "1", host],
               check=True, timeout=5)
```
:::

✅ Bien: valida además que `host` parezca un dominio o IP (regex o `ipaddress.ip_address`) y, mejor aún, evita llamar al shell si existe una librería que haga lo mismo.

### 📌 Defensas contra inyección, en orden

1. **Consultas parametrizadas** (o un ORM bien usado). Es la defensa principal.
2. **Lista blanca** para lo que no se puede parametrizar (columnas, orden, nombres de archivo).
3. **Mínimo privilegio** en el usuario de la base: si igual hay inyección, que no pueda borrar tablas ni leer otras bases.
4. **Errores genéricos** al usuario: nunca muestres el error SQL completo (le da pistas al atacante).
5. **Escaneo**: Semgrep / CodeQL detectan concatenaciones de SQL en el código.

❌ Mal: "escapar las comillas a mano" con `replace("'", "''")`. Siempre hay un caso que se te escapa (codificaciones, barras invertidas, números sin comillas).

🧠 Caso real: en **mayo de 2023** una inyección SQL en **MOVEit Transfer** (software de transferencia de archivos de Progress, `CVE-2023-34362`) fue explotada masivamente por el grupo de ransomware Cl0p para robar datos de cientos de organizaciones. Una vulnerabilidad "de libro", en 2023.

## 🕸️ XSS: Cross-Site Scripting

🧠 Concepto: **XSS** = el atacante consigue que **tu** página ejecute **su** JavaScript en el navegador de **otros** usuarios. Como el script corre con el origen de tu web, puede leer el DOM, hacer peticiones como la víctima, robar tokens guardados en `localStorage` o cambiar lo que ve.

Es una inyección más: el dato del usuario termina interpretado como HTML/JS.

### 🧬 Los tres tipos

| Tipo | Dónde vive el script | Ejemplo | Quién lo arregla |
|---|---|---|---|
| Almacenado (stored) | En tu base de datos | Comentario con `<script>` que ven todos | Backend + plantillas |
| Reflejado (reflected) | En la URL / petición | `?q=<script>…` devuelto en la página | Backend |
| Basado en DOM | Solo en el navegador | JS que hace `innerHTML = location.hash` | Frontend |

```secuencia
actores: Atacante, Web, Víctima
Atacante -> Web : comentario con script malicioso
nota Web : lo guarda sin escapar
Víctima -> Web : abre la página del foro
Web --> Víctima : HTML + script del atacante
nota Víctima : el script corre con TU origen
Víctima -> Atacante : (el script) envía datos de la víctima
```

🧠 Caso real: en **2005** el "gusano Samy" en **MySpace** usó XSS almacenado en un perfil: cada visitante se añadía a Samy como amigo y copiaba el script a su propio perfil. Superó el millón de víctimas en unas 20 horas y MySpace tuvo que apagarse un tiempo.

### 🧯 Defensa 1: escapar según el contexto

**Escapar** = convertir los caracteres especiales en entidades para que se muestren como texto y no se interpreten.

```python
import html
comentario = '<script>alert("hola")</script>'
print(html.escape(comentario))
```

```text
&lt;script&gt;alert(&quot;hola&quot;)&lt;/script&gt;
```

::: columnas
### ❌ Vulnerable (DOM)
```js
// Inserta HTML: cualquier etiqueta se ejecuta
caja.innerHTML = comentario.texto;

// jQuery igual de peligroso
$("#caja").html(comentario.texto);
```
::: siguiente
### ✅ Corregido
```js
// Inserta TEXTO: < y > se muestran tal cual
caja.textContent = comentario.texto;

// Si de verdad necesitas HTML (editor rico):
caja.innerHTML = DOMPurify.sanitize(comentario.html);
```
:::

Los frameworks modernos **escapan por defecto**: React (`{texto}`), Vue (`{{ texto }}`), Angular, Jinja2 y Django (autoescape). El peligro aparece cuando desactivas esa protección:

| Framework | Escapa por defecto | Puerta peligrosa |
|---|---|---|
| React | `{variable}` | `dangerouslySetInnerHTML` |
| Vue | `{{ variable }}` | `v-html` |
| Angular | `{{ variable }}` | `bypassSecurityTrustHtml` |
| Jinja2 / Flask | autoescape en `.html` | filtro `| safe`, `Markup()` |
| Django | autoescape | `mark_safe`, `{% autoescape off %}` |

⚠️ Cuidado: escapar HTML no basta en todos los contextos. Dentro de un atributo `href`, el valor `javascript:alert(1)` no tiene ni `<` ni `>` y se ejecuta al hacer clic. Valida que las URLs empiecen con `https://` o `/`.

```jsx
// ❌ React no te salva aquí
<a href={usuario.web}>Mi web</a>      // web = "javascript:robar()"

// ✅ Valida el esquema antes de usarla
const segura = /^https?:\/\//i.test(usuario.web) ? usuario.web : "#";
<a href={segura} rel="noopener noreferrer">Mi web</a>
```

### 🛡️ Defensa 2: Content Security Policy (CSP)

🧠 Concepto: **CSP** = cabecera HTTP con la que el servidor le dice al navegador **de dónde** puede cargar y ejecutar scripts, estilos, imágenes, etc. Si se cuela un `<script>` inyectado que no cumple la política, el navegador **no lo ejecuta**. Es la segunda capa contra XSS.

```text
Content-Security-Policy: default-src 'self';
  script-src 'self' 'nonce-r4nd0m123';
  object-src 'none';
  base-uri 'self';
  frame-ancestors 'none'
```

- `default-src 'self'` :: Por defecto, solo recursos de tu propio origen
- `script-src 'self' 'nonce-…'` :: Solo scripts propios o con el nonce aleatorio de esta respuesta
- `object-src 'none'` :: Prohíbe Flash/plugins antiguos
- `frame-ancestors 'none'` :: Nadie puede meter tu web en un iframe (anti-clickjacking)
- `'unsafe-inline'` :: ❌ Permite scripts en línea: anula gran parte de la protección
- `Content-Security-Policy-Report-Only` :: Modo prueba: solo informa, no bloquea

💡 Consejo: empieza con `Report-Only` para ver qué se rompería, ajusta, y luego actívala de verdad.

### 🍪 Defensa 3: limitar el daño

- Cookies de sesión con `HttpOnly`: el JavaScript (incluido el inyectado) no puede leerlas.
- No guardes tokens de larga duración en `localStorage` (cualquier XSS los lee).
- Sanitiza HTML enriquecido con una librería mantenida (DOMPurify en JS, `nh3`/`bleach` en Python), nunca con regex propias.

## 🎭 CSRF: Cross-Site Request Forgery

🧠 Concepto: **CSRF** = una web maliciosa hace que el navegador de la víctima envíe una petición a **tu** web, y el navegador adjunta **automáticamente** las cookies de sesión. Tu servidor ve una petición "auténtica" de la víctima, aunque ella nunca la quiso hacer.

A diferencia del XSS, el atacante **no ve** la respuesta: solo logra que se ejecute una acción (cambiar el email, transferir dinero, borrar algo).

```secuencia
actores: Víctima, Banco, SitioMalo
Víctima -> Banco : inicia sesión
Banco --> Víctima : Set-Cookie: sesion=abc
Víctima -> SitioMalo : abre un enlace "gana un premio"
SitioMalo --> Víctima : página con formulario oculto auto-enviado
Víctima -> Banco : POST /transferir + cookie sesion=abc (automática)
nota Banco : cookie válida → ejecuta la transferencia ❌
```

### 🧯 Defensas

| Defensa | Cómo funciona | Nota |
|---|---|---|
| Cookie `SameSite=Lax` o `Strict` | El navegador no envía la cookie en peticiones desde otros sitios | Lax es el valor por defecto en Chrome desde 2020 |
| Token anti-CSRF | Valor secreto por sesión que el formulario debe reenviar | El sitio malo no puede leerlo |
| Revisar `Origin` / `Referer` | Rechazar POST cuyo origen no sea el tuyo | Capa extra |
| No cambiar estado con GET | `GET /borrar?id=5` se dispara con una simple imagen | Usa POST/PUT/DELETE |
| Pedir reautenticación | Contraseña o MFA para acciones críticas | Cambiar email, pagos |

::: columnas
### ❌ Vulnerable
```python
# Flask: acepta el POST solo con la cookie
@app.post("/cuenta/email")
def cambiar_email():
    usuario = usuario_actual()      # por cookie
    usuario.email = request.form["email"]
    db.commit()
    return "ok"
```
::: siguiente
### ✅ Corregido
```python
# Flask-WTF valida un token CSRF en cada POST
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)

app.config.update(
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
)
```
:::

```html
<!-- El formulario incluye el token oculto que solo tu página conoce -->
<form method="post" action="/cuenta/email">
  <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
  <input type="email" name="email">
  <button>Guardar</button>
</form>
```

💡 Consejo: Django, Rails, Laravel y Spring Security traen protección CSRF activada por defecto. No la desactives "porque da error": arregla el formulario para que envíe el token.

⚠️ Cuidado: si tu API usa `Authorization: Bearer <token>` en una cabecera (no cookies), el CSRF clásico no aplica, porque el navegador no añade esa cabecera solo. Pero entonces el token suele vivir en JS, y quedas más expuesto a XSS. Todo es un intercambio.

## 🛰️ SSRF: Server-Side Request Forgery

🧠 Concepto: **SSRF** = tu servidor descarga una URL que elige el usuario (para una vista previa, un webhook, importar una imagen…), y el atacante le pasa una URL **interna** a la que él no llega pero tu servidor sí: el panel de administración interno, la base de datos, o el servicio de **metadatos de la nube**, que entrega credenciales.

```flujo
Atacante -> API : url=http://169.254.169.254/...
API -> Metadatos : GET interno
Metadatos -> API : credenciales temporales
API -> Atacante : "vista previa" con las credenciales
```

🧠 Caso real: la filtración de **Capital One (2019)**, con datos de unos 100 millones de personas en EE. UU. y unos 6 millones en Canadá, se produjo por un SSRF a través de un WAF mal configurado en AWS que permitió pedir credenciales al servicio de metadatos (IMDS) y con ellas leer buckets S3. Tras casos así AWS impulsó **IMDSv2**, que exige un token previo obtenido con PUT.

### 🧯 Defensas

::: columnas
### ❌ Vulnerable
```python
import requests

@app.get("/preview")
def preview():
    url = request.args["url"]
    # Descarga lo que sea: interno o externo
    r = requests.get(url, timeout=5)
    return r.text[:500]
```
::: siguiente
### ✅ Más seguro
```python
import ipaddress, socket
from urllib.parse import urlparse

PERMITIDOS = {"https"}

def url_publica(url: str) -> bool:
    p = urlparse(url)
    if p.scheme not in PERMITIDOS or not p.hostname:
        return False
    for info in socket.getaddrinfo(p.hostname, 443):
        ip = ipaddress.ip_address(info[4][0])
        if (ip.is_private or ip.is_loopback
                or ip.is_link_local or ip.is_reserved):
            return False
    return True
```
:::

1. **Lista blanca** de dominios cuando sea posible (ej. solo `api.github.com`). Es lo más fuerte.
2. Solo esquemas `https` (no `file://`, `gopher://`, `ftp://`).
3. Resolver el DNS y **bloquear IPs privadas** (10.x, 172.16–31.x, 192.168.x, 127.x, 169.254.x, `::1`).
4. **No seguir redirecciones** automáticamente (`allow_redirects=False`) o revalidar cada salto.
5. A nivel de red: el servicio que descarga URLs no debería poder hablar con la red interna (egress filtering).
6. En la nube: IMDSv2 obligatorio y roles con mínimo privilegio.

⚠️ Cuidado: validar el DNS y luego descargar deja una ventana para el **DNS rebinding** (el dominio resuelve a una IP pública al validar y a una privada al descargar). La defensa robusta es conectarse a la IP ya validada o filtrar a nivel de red.

## 📂 Path traversal y subida de archivos

🧠 Concepto: **path traversal** (recorrido de directorios) = el usuario controla parte de una ruta de archivo y usa `../` (o una ruta absoluta) para **salir** de la carpeta prevista y leer o escribir archivos del sistema: `/etc/passwd`, el `.env`, el código fuente, claves SSH.

```arbol
/srv/app
  subidas  ← carpeta permitida
    tarea.pdf
  .env  ← ../.env
  app.py
/etc
  passwd  ← ../../../etc/passwd
```

### ✅ Ejemplo resuelto: confinar la ruta (ejecutado en este PC)

```python
from pathlib import Path

BASE = Path("/srv/app/subidas").resolve()

def ruta_insegura(nombre: str) -> Path:
    return BASE / nombre                      # ❌ confía en el nombre

def ruta_segura(nombre: str) -> Path:
    ruta = (BASE / nombre).resolve()          # normaliza ../ y enlaces
    if not ruta.is_relative_to(BASE):         # ✅ ¿sigue dentro de BASE?
        raise PermissionError(f"Ruta fuera de la carpeta: {nombre}")
    return ruta

for nombre in ["tarea.pdf", "../../../etc/passwd", "/etc/shadow"]:
    print(f"{nombre!r:24} -> insegura: {ruta_insegura(nombre).resolve()}")
    try:
        print(f"{'':24}    segura  : {ruta_segura(nombre)}")
    except PermissionError as e:
        print(f"{'':24}    segura  : ⛔ {e}")
```

```text
'tarea.pdf'              -> insegura: /srv/app/subidas/tarea.pdf
                            segura  : /srv/app/subidas/tarea.pdf
'../../../etc/passwd'    -> insegura: /etc/passwd
                            segura  : ⛔ Ruta fuera de la carpeta: ../../../etc/passwd
'/etc/shadow'            -> insegura: /etc/shadow
                            segura  : ⛔ Ruta fuera de la carpeta: /etc/shadow
```

💡 Fíjate: con `pathlib`, `BASE / "/etc/shadow"` **descarta** BASE porque el segundo trozo es absoluto. Lo mismo pasa con `os.path.join`. Mucha gente no lo sabe.

⚠️ Cuidado: comprobar con `startswith("/srv/app/subidas")` sobre el texto falla: `/srv/app/subidas_privadas/x` también empieza así. Compara rutas ya resueltas (`is_relative_to`, o `os.path.commonpath`).

### 📤 Subida de archivos segura

| Riesgo | Ejemplo | Defensa |
|---|---|---|
| Nombre malicioso | `../../app.py` | Genera tú el nombre (UUID), guarda el original en la BD |
| Tipo falso | `foto.jpg` que es un `.php` | Lista blanca de extensiones + revisar el contenido (magic bytes) |
| Ejecución | Subir a una carpeta que el servidor ejecuta | Guardar fuera del webroot o en un bucket (S3) |
| Archivo enorme | 10 GB llenan el disco | Límite de tamaño en el proxy y en la app |
| XSS con SVG/HTML | SVG con `<script>` servido desde tu dominio | `Content-Disposition: attachment`, dominio aparte |
| Zip bomb | Zip de 1 MB que se descomprime en GB | Limitar tamaño descomprimido y número de archivos |

```python
import uuid
from pathlib import Path

EXT_PERMITIDAS = {".pdf", ".png", ".jpg"}
MAX_BYTES = 5 * 1024 * 1024                        # 5 MB

def guardar_subida(archivo):
    ext = Path(archivo.filename).suffix.lower()
    if ext not in EXT_PERMITIDAS:
        raise ValueError("Tipo de archivo no permitido")
    datos = archivo.read(MAX_BYTES + 1)
    if len(datos) > MAX_BYTES:
        raise ValueError("Archivo demasiado grande")
    nombre = f"{uuid.uuid4().hex}{ext}"            # nombre generado por nosotros
    (BASE / nombre).write_bytes(datos)
    return nombre                                  # el nombre original va a la BD
```

## 📦 Deserialización insegura

🧠 Concepto: **serializar** = convertir un objeto en bytes o texto para guardarlo o enviarlo; **deserializar** = reconstruirlo. Algunos formatos (pickle en Python, `ObjectInputStream` en Java, `unserialize` en PHP, `Marshal` en Ruby) pueden reconstruir **cualquier objeto** y llamar métodos durante el proceso. Si los datos vienen del usuario, el atacante elige qué se ejecuta: ejecución remota de código (RCE).

### ✅ Ejemplo resuelto: pickle ejecuta código al cargar (inofensivo, ejecutado en este PC)

```python
import pickle, json

class Trampa:
    # pickle llama a __reduce__ al reconstruir el objeto: puede ejecutar CUALQUIER función
    def __reduce__(self):
        return (print, ("⚠️ ¡Código ejecutado solo por hacer pickle.loads!",))

datos_del_atacante = pickle.dumps(Trampa())
pickle.loads(datos_del_atacante)          # ❌ nunca con datos que no controlas

# ✅ JSON solo crea datos (dict, list, str, números), nunca ejecuta código
print(json.loads('{"usuario": "ana", "puntos": 10}'))
```

```text
⚠️ ¡Código ejecutado solo por hacer pickle.loads!
{'usuario': 'ana', 'puntos': 10}
```

Aquí la función es un inocente `print`, pero podría ser cualquier otra del sistema. Por eso la documentación oficial de Python advierte: "The pickle module is not secure. Only unpickle data you trust."

| Formato / función | ¿Seguro con datos externos? | Alternativa |
|---|---|---|
| `json.loads` | ✅ Sí (solo datos) | — |
| `pickle.loads`, `joblib.load` | ❌ No | JSON, MessagePack, Protobuf |
| `yaml.load` (sin `Loader` seguro) | ❌ No | `yaml.safe_load` |
| `yaml.safe_load` | ✅ Sí | — |
| `torch.load` de modelos ajenos | ⚠️ Usa pickle | `weights_only=True`, formato safetensors |
| Java `ObjectInputStream` | ❌ Peligroso | JSON con esquema, filtros de clases |
| `eval(texto)` | ❌ Nunca | `ast.literal_eval`, `json.loads` |

```python
import yaml
txt = "!!python/object/apply:os.getcwd []"   # etiqueta que pide ejecutar una función
try:
    print(yaml.safe_load(txt))
except yaml.YAMLError as e:
    print("safe_load rechaza:", type(e).__name__)
```

```text
safe_load rechaza: ConstructorError
```

🚀 Futuro: en IA esto importa mucho. Los modelos de PyTorch tradicionales (`.pt`, `.bin`) son pickles: descargar y cargar un modelo de un desconocido es ejecutar su código. Por eso Hugging Face impulsó el formato **safetensors** (solo tensores, sin código) y PyTorch cambió en la versión 2.6 el valor por defecto de `torch.load` a `weights_only=True`.

✅ Bien: si necesitas que un dato serializado no sea manipulado (por ejemplo, en una cookie), **fírmalo** (HMAC, `itsdangerous`) y verifica la firma antes de usarlo. La firma garantiza integridad, no confidencialidad.

## 🔑 Contraseñas: guardar y comprobar

Regla de oro: **nunca guardes contraseñas**, ni en texto plano ni "cifradas". Guarda un **hash lento con salt**, y al hacer login calcula el hash de lo que escribió el usuario y compáralo.

🧠 Concepto: **hash** = función de una sola vía: de la contraseña sale una huella de tamaño fijo, pero de la huella no se puede volver a la contraseña. **Cifrar** sí es reversible con la clave (y si roban la clave, roban todo).

🧠 Concepto: **salt** (sal) = valor aleatorio distinto por usuario que se mezcla con la contraseña antes del hash. Hace que dos usuarios con `123456` tengan hashes distintos e inutiliza las **rainbow tables** (tablas precalculadas de hash → contraseña).

🧠 Concepto: **pepper** (pimienta) = secreto extra igual para todos, guardado FUERA de la base (en un gestor de secretos). Si roban solo la base, les falta el pepper. Es opcional.

### ⚖️ Por qué MD5 o SHA-256 no sirven aquí

MD5 y SHA-256 están diseñados para ser **rápidos** (verificar archivos, firmas). Para contraseñas, rápido es malo: una GPU moderna prueba miles de millones de hashes MD5 por segundo. Los algoritmos para contraseñas son **lentos a propósito** y, los modernos, además gastan mucha **memoria**, lo que encarece los ataques con GPU o hardware especial.

### ✅ Ejemplo resuelto: MD5 vs bcrypt vs Argon2id (ejecutado en este PC)

```python
import hashlib, time, bcrypt                 # pip install bcrypt argon2-cffi
from argon2 import PasswordHasher

clave = "cambia_esto_123"

# ❌ MD5 / SHA-256 "pelados": rapidísimos (malo para contraseñas) y sin salt
print("MD5     :", hashlib.md5(clave.encode()).hexdigest())
print("SHA-256 :", hashlib.sha256(clave.encode()).hexdigest()[:32], "...")

t = time.perf_counter()
for _ in range(100_000):
    hashlib.sha256(clave.encode()).digest()
print(f"100 000 SHA-256 en {time.perf_counter() - t:.2f} s")

# ✅ bcrypt: lento a propósito y con salt aleatorio incluido en el hash
t = time.perf_counter()
h = bcrypt.hashpw(clave.encode(), bcrypt.gensalt(rounds=12))
print(f"bcrypt  : {h.decode()}  ({time.perf_counter() - t:.2f} s)")
print("bcrypt otra vez:", bcrypt.hashpw(clave.encode(), bcrypt.gensalt(rounds=12)).decode()[:29], "... (salt distinto)")
print("¿Correcta?", bcrypt.checkpw(clave.encode(), h), "| ¿'hola'?", bcrypt.checkpw(b"hola", h))

# ✅ Argon2id (primera opción recomendada hoy por OWASP)
ph = PasswordHasher()
ha = ph.hash(clave)
print("argon2id:", ha)
print("Verifica:", ph.verify(ha, clave))
```

```text
MD5     : 96a599ffcfe330ed3b037aa7ae9e7965
SHA-256 : 071c7aa013becc05ae0401ea5ee389e7 ...
100 000 SHA-256 en 0.06 s
bcrypt  : $2b$12$xNF7g8.E62zub1zvg.t.Nujx1ch5IfFHk47y6WJUYZtrHbSURPgS2  (0.23 s)
bcrypt otra vez: $2b$12$iRtnxt2g36.9qn5BNIFwL. ... (salt distinto)
¿Correcta? True | ¿'hola'? False
argon2id: $argon2id$v=19$m=65536,t=3,p=4$iHTPomBpWdH5FnBM8YPnlw$gS8N9cpyTMbV+inTS4EaXgzNjoIM56NKYW66bYf1pho
Verifica: True
```

Lee el hash de bcrypt por partes: `$2b$` (versión) · `12$` (coste: 2¹² rondas) · 22 caracteres de **salt** · el resto es el hash. Todo va junto en una columna: no necesitas guardar el salt aparte. Argon2id igual: `m=65536` (64 MiB de memoria), `t=3` (iteraciones), `p=4` (hilos).

```grafica
tipo: barras
titulo: Tiempo para calcular UN hash en este PC (medido, ilustrativo)
unidad: ms
SHA-256 : 0.0006
bcrypt coste 12 : 230
```

Con SHA-256 un atacante con tu base robada prueba millones de contraseñas por segundo en una sola CPU (y muchísimas más en una GPU); con bcrypt coste 12, unas pocas decenas. Esa diferencia de ~400 000 veces es justo lo que quieres.

| Algoritmo | ¿Para contraseñas? | Por qué |
|---|---|---|
| Texto plano | ❌ Jamás | Una filtración = todas las contraseñas |
| Cifrado (AES, 3DES) | ❌ No | Reversible: si roban la clave, se descifra todo |
| MD5, SHA-1 | ❌ No | Rápidos y rotos para colisiones |
| SHA-256 / SHA-512 sin más | ❌ No | Rápidos: ideales para fuerza bruta |
| PBKDF2-HMAC-SHA256 | ⚠️ Aceptable | Lento por iteraciones (OWASP pide 600 000), sin coste de memoria |
| bcrypt | ✅ Sí | Probado desde 1999; límite de 72 bytes |
| scrypt | ✅ Sí | Lento y usa memoria |
| Argon2id | ✅ Mejor opción | Ganó la Password Hashing Competition (2015); memoria configurable |

⚠️ Cuidado: bcrypt solo usa los primeros **72 bytes** de la contraseña. Con frases muy largas o muchos emojis (4 bytes cada uno) el resto se ignora. Argon2id no tiene ese límite.

💡 Consejo: compara secretos (tokens, firmas) con `hmac.compare_digest(a, b)` y no con `==`: `==` termina en el primer carácter distinto, y midiendo tiempos se puede adivinar poco a poco (ataque de temporización). `bcrypt.checkpw` y `ph.verify` ya lo hacen bien.

### 📏 Política de contraseñas moderna (NIST SP 800-63B)

::: columnas
### ❌ Lo de antes
- Obligar mayúscula + número + símbolo
- Cambio obligatorio cada 90 días
- Máximo 16 caracteres
- Preguntas de seguridad ("¿tu mascota?")
::: siguiente
### ✅ Lo recomendado hoy
- Mínimo 8 (mejor 12+) y permitir largas (64+)
- Cambio solo si hay indicios de filtración
- Rechazar contraseñas filtradas o comunes
- Permitir pegar (gestores de contraseñas) y ofrecer MFA
:::

![xkcd 936 «Password Strength»: una frase de 4 palabras al azar es más fuerte y fácil de recordar que «Tr0ub4dor&3» (xkcd.com, CC BY-NC 2.5)](img/seguridad/xkcd-password-strength.png)

🧠 Caso real: en **2012** se filtraron unos 6,5 millones de hashes de **LinkedIn** guardados con **SHA-1 sin salt**; en 2016 apareció que el robo afectaba a más de 100 millones de cuentas. Sin salt y con un hash rápido, la mayoría se crackeó enseguida. En **2013 Adobe** perdió más de 150 millones de registros con contraseñas **cifradas** (3DES en modo ECB, no hasheadas) y las pistas en texto plano: contraseñas iguales daban el mismo resultado cifrado, y las pistas ayudaban a adivinarlas.

## 🎫 Sesiones vs JWT

Después del login, el servidor necesita reconocer al usuario en cada petición (HTTP no tiene memoria). Hay dos grandes estilos:

::: columnas
### 🍪 Sesión con estado (stateful)
- El servidor guarda la sesión (Redis, BD) y da un **id aleatorio** en una cookie.
- Cerrar sesión = borrar la fila: efecto inmediato.
- Hay que consultar el almacén en cada petición.
- Ideal para webs clásicas y monolitos.
::: siguiente
### 🎟️ Token autocontenido (JWT)
- El servidor **firma** un token con los datos (`sub`, `rol`, `exp`) y no guarda nada.
- Cualquier servicio con la clave puede verificarlo sin consultar la BD.
- Revocar antes de `exp` es difícil (necesitas lista negra).
- Útil entre microservicios, APIs y apps móviles.
:::

```secuencia
actores: Navegador, API, Redis
Navegador -> API : POST /login (email, contraseña)
API -> Redis : guarda sesion 9f2c… → usuario 42
API --> Navegador : Set-Cookie: sid=9f2c…; HttpOnly; Secure; SameSite=Lax
Navegador -> API : GET /notas + cookie sid
API -> Redis : ¿quién es 9f2c…?
Redis --> API : usuario 42
API --> Navegador : notas del usuario 42
```

### 🍪 Cookies de sesión bien configuradas

- `HttpOnly` :: El JavaScript no puede leerla (frena el robo por XSS)
- `Secure` :: Solo viaja por HTTPS
- `SameSite=Lax` :: No se envía en peticiones cruzadas peligrosas (frena CSRF)
- `Max-Age=3600` :: Caduca sola
- `__Host-sid` :: Prefijo que obliga a Secure, Path=/ y sin Domain

✅ Bien: **regenera el id de sesión al iniciar sesión** (y al subir de privilegios). Si no, un atacante que fijó un id antes del login lo hereda autenticado (**session fixation**).

### 🧬 Anatomía de un JWT

Un JWT son tres trozos en Base64URL separados por puntos: `cabecera.payload.firma`. La firma (HMAC o RSA/ECDSA) garantiza que nadie cambió el contenido, pero el contenido **no está cifrado**: cualquiera lo lee.

### ✅ Ejemplo resuelto: leer, verificar y rechazar tokens (ejecutado en este PC)

```python
import base64, json, time, jwt          # pip install pyjwt

SECRETO = "cambia_esto_por_32_bytes_aleatorios!!"
token = jwt.encode({"sub": "42", "rol": "alumno", "exp": int(time.time()) + 900},
                   SECRETO, algorithm="HS256")
print("Token:", token[:60], "...")

# Un JWT NO está cifrado: cualquiera lee el payload con base64
payload = token.split(".")[1]
payload += "=" * (-len(payload) % 4)
print("Payload leído sin la clave:", json.loads(base64.urlsafe_b64decode(payload)))

# ✅ Verificar SIEMPRE fijando el algoritmo permitido
print("Verificado:", jwt.decode(token, SECRETO, algorithms=["HS256"]))

# Token manipulado: cambiamos rol a admin y quitamos la firma (alg none)
cab = base64.urlsafe_b64encode(b'{"alg":"none","typ":"JWT"}').rstrip(b"=").decode()
cuerpo = base64.urlsafe_b64encode(b'{"sub":"42","rol":"admin"}').rstrip(b"=").decode()
falso = f"{cab}.{cuerpo}."
try:
    jwt.decode(falso, SECRETO, algorithms=["HS256"])
except jwt.InvalidTokenError as e:
    print("Rechazado:", type(e).__name__, "-", e)

# Token vencido
viejo = jwt.encode({"sub": "42", "exp": int(time.time()) - 10}, SECRETO, algorithm="HS256")
try:
    jwt.decode(viejo, SECRETO, algorithms=["HS256"])
except jwt.ExpiredSignatureError as e:
    print("Rechazado:", e)
```

```text
Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0MiIsInJvbCI ...
Payload leído sin la clave: {'sub': '42', 'rol': 'alumno', 'exp': 1792443636}
Verificado: {'sub': '42', 'rol': 'alumno', 'exp': 1792443636}
Rechazado: InvalidAlgorithmError - The specified alg value is not allowed
Rechazado: Signature has expired
```

### 🚨 Errores clásicos con JWT

| Error | Qué pasa | Cómo evitarlo |
|---|---|---|
| Aceptar `alg: none` | Token sin firma aceptado: cualquiera se pone `rol: admin` | `algorithms=["HS256"]` explícito |
| Confusión RS256 → HS256 | Se usa la clave PÚBLICA como secreto HMAC | Fijar el algoritmo esperado por clave |
| `jwt.decode` sin verificar | Leer el payload y confiar en él | Usar siempre la función que verifica la firma |
| Sin `exp` o `exp` de meses | Un token robado sirve para siempre | Access token de 5–15 min + refresh token |
| Guardarlo en `localStorage` | Cualquier XSS lo roba | Cookie `HttpOnly` o memoria + refresh en cookie |
| Datos sensibles en el payload | Se leen con base64 | Solo ids y roles, nada secreto |
| Secreto débil (`secret`) | Se adivina por fuerza bruta offline | 32+ bytes aleatorios, en un gestor de secretos |
| No poder revocar | Usuario baneado sigue entrando | Expiración corta, lista de revocación, rotar refresh |

🧠 Caso real: en **2015** se publicó que varias librerías JWT populares aceptaban tokens con `"alg": "none"` o se dejaban engañar con la confusión RS256/HS256, porque confiaban en el algoritmo que decía **el propio token**. Por eso las librerías actuales te obligan a pasar la lista de algoritmos permitidos.

```flujo
dir: abajo
Login -> Access : 15 min
Login -> Refresh : 7 días, cookie HttpOnly
Access -> API : Authorization Bearer
Access -> Expira : 401
Expira -> Refresh : POST /refresh
Refresh -> Access : nuevo + rota refresh
```

💡 Consejo: si tu web y tu API viven en el mismo dominio, la opción más simple y segura suele ser **sesión en cookie HttpOnly**. Usa JWT cuando de verdad necesites verificar sin estado entre varios servicios. "JWT es más moderno" no es un motivo.

## 🤝 OAuth 2.0, OpenID Connect y MFA

🧠 Concepto: **OAuth 2.0** = protocolo de **autorización delegada**: tú permites que una app (ej. un editor de fotos) acceda a algo tuyo en otro servicio (ej. tu Google Drive) **sin darle tu contraseña**, sino un **access token** con permisos limitados (**scopes**).

🧠 Concepto: **OpenID Connect (OIDC)** = capa sobre OAuth 2.0 para **autenticación**: además del access token entrega un **ID token** (un JWT) que dice quién es el usuario. Es lo que hay detrás del botón "Iniciar sesión con Google".

| Pregunta | OAuth 2.0 | OIDC |
|---|---|---|
| ¿Qué resuelve? | ¿Qué puede hacer esta app? | ¿Quién es este usuario? |
| Token principal | Access token | ID token (JWT) + access token |
| Ejemplo | App lee tu calendario | Login con Google / GitHub / Microsoft |

### 🔁 Flujo Authorization Code + PKCE (el recomendado hoy)

```secuencia
actores: Usuario, App, Google
Usuario -> App : clic en "Entrar con Google"
nota App : crea code_verifier y state aleatorios
App --> Usuario : redirige a Google con code_challenge y state
Usuario -> Google : inicia sesión y acepta permisos
Google --> Usuario : redirige a la App con ?code=…&state=…
Usuario -> App : entrega code y state
nota App : comprueba que state coincide
App -> Google : code + code_verifier
Google --> App : ID token + access token
nota App : verifica firma, iss, aud, exp del ID token
```

- `state` :: Valor aleatorio contra CSRF en el login: compruébalo al volver
- `PKCE (code_verifier, code_challenge)` :: Impide que alguien que intercepte el `code` lo canjee
- `redirect_uri exacta` :: Registra URLs exactas, sin comodines: si no, el code puede ir al atacante
- `scope mínimo` :: Pide solo lo que necesitas (`openid email`, no todo el Drive)
- `response_type=token (implicit)` :: ❌ Obsoleto: entregaba el token en la URL

💡 Consejo: no implementes OAuth/OIDC a mano. Usa una librería certificada o un proveedor (Auth.js/NextAuth, Authlib, Spring Security, Keycloak, Auth0, Clerk, Supabase Auth, Firebase Auth). El protocolo está lleno de detalles finos.

### 📲 MFA: autenticación multifactor

🧠 Concepto: **MFA** = pedir dos o más factores de tipos distintos: algo que **sabes** (contraseña), algo que **tienes** (celular, llave física) y algo que **eres** (huella, rostro). Si roban la contraseña, todavía falta el otro factor.

| Factor | Cómo funciona | Resiste phishing | Nota |
|---|---|---|---|
| SMS | Código por mensaje | ❌ No | SIM swapping; mejor que nada |
| TOTP (app) | Código de 6 dígitos cada 30 s | ❌ No | Google Authenticator, Aegis, 2FAS |
| Push | "¿Eres tú?" en el celular | ⚠️ Poco | Fatiga MFA: el usuario acepta por cansancio |
| Llave FIDO2 / WebAuthn | Firma ligada al dominio | ✅ Sí | YubiKey, Titan |
| Passkeys | WebAuthn con clave sincronizada | ✅ Sí | Sin contraseña; Apple, Google, Microsoft |

```python
# TOTP en Python (pip install pyotp): el servidor y la app comparten un secreto
import pyotp
secreto = pyotp.random_base32()          # se guarda cifrado, por usuario
totp = pyotp.TOTP(secreto)
print(totp.provisioning_uri(name="ana@uni.bo", issuer_name="MiApp"))  # va en un QR
print(totp.verify("123456", valid_window=1))   # acepta el código actual ±30 s
```

🚀 Futuro: las **passkeys** (WebAuthn/FIDO2) son la apuesta de Apple, Google y Microsoft para reemplazar contraseñas: la clave privada nunca sale del dispositivo y la firma está atada al dominio real, así que una web falsa de phishing no puede usarla.

## 🚪 Autorización: IDOR y acceso roto

🧠 Concepto: **autenticación** = ¿quién eres? (login). **Autorización** = ¿qué puedes hacer? (permisos). Son cosas distintas: estar logueado no significa poder ver todo.

🧠 Concepto: **IDOR** (Insecure Direct Object Reference) = la API usa un id que viene del cliente (`/api/facturas/1043`) y **no comprueba** que ese objeto pertenezca al usuario. Basta cambiar el número para ver datos de otro. En APIs se llama **BOLA** (Broken Object Level Authorization) y es el n.º 1 del OWASP API Top 10.

Control de acceso roto es el **A01** del OWASP Top 10 (2021 y 2025): el más frecuente en las aplicaciones analizadas.

```secuencia
actores: Ana, API, BD
Ana -> API : GET /api/notas/1043 (su nota)
API --> Ana : 200 OK
Ana -> API : GET /api/notas/1044 (¿y si cambio el número?)
API -> BD : SELECT … WHERE id = 1044
nota API : ❌ nunca pregunta de quién es
API --> Ana : 200 OK con la nota de Luis
```

::: columnas
### ❌ Vulnerable (IDOR)
```python
@app.get("/api/notas/<int:nota_id>")
@login_required
def ver_nota(nota_id):
    nota = Nota.query.get_or_404(nota_id)
    return nota.to_dict()
```
::: siguiente
### ✅ Corregido
```python
@app.get("/api/notas/<int:nota_id>")
@login_required
def ver_nota(nota_id):
    # filtra por dueño EN la consulta
    nota = Nota.query.filter_by(
        id=nota_id, alumno_id=current_user.id
    ).first_or_404()       # 404: no revela si existe
    return nota.to_dict()
```
:::

### 🧩 Formas típicas de control de acceso roto

| Fallo | Ejemplo | Defensa |
|---|---|---|
| IDOR / BOLA | Cambiar el id en la URL | Filtrar por dueño en cada consulta |
| Escalada vertical | Alumno llama a `DELETE /api/admin/usuarios/7` | Chequeo de rol en el backend en CADA endpoint |
| Asignación masiva | Enviar `{"nombre":"Ana","rol":"admin"}` en el perfil | Lista blanca de campos editables (DTO / esquema) |
| Solo esconder el botón | El menú no muestra "Admin", pero la API responde | La UI no es seguridad: valida en el servidor |
| Confiar en cabeceras | `X-User-Id: 1` enviado por el cliente | La identidad sale de la sesión/token verificado |
| Multi-inquilino (multi-tenant) | Empresa A ve datos de empresa B | `tenant_id` en cada consulta, Row Level Security |

```js
// ❌ Asignación masiva (mass assignment): copia TODO lo que manda el cliente
await prisma.usuario.update({ where: { id: req.user.id }, data: req.body });

// ✅ Solo los campos permitidos, validados con un esquema (zod)
const Perfil = z.object({ nombre: z.string().max(80), bio: z.string().max(500) });
const datos = Perfil.parse(req.body);              // ignora "rol", "esAdmin", etc.
await prisma.usuario.update({ where: { id: req.user.id }, data: datos });
```

💡 Consejo: centraliza la autorización (middleware, políticas, decoradores, Row Level Security de PostgreSQL) en vez de repetir `if` en cada ruta: el endpoint que olvidaste es el que encontrarán. Y escribe **tests** que prueben que el usuario B recibe 403/404 con los recursos de A.

⚠️ Cuidado: usar UUID en vez de ids numéricos dificulta adivinar, pero **no es autorización**. Un UUID filtrado en un log o en un enlace compartido sigue abriendo la puerta si no compruebas el dueño.

## 🤫 Secretos: claves, tokens y .env

🧠 Concepto: **secreto** = cualquier dato que da acceso: contraseña de la BD, API key de Stripe u OpenAI, clave privada SSH, `JWT_SECRET`, credenciales de AWS, token de GitHub. Quien lo tiene **es** tu aplicación a ojos del otro servicio.

Regla: **los secretos nunca van en el código ni en git**. Van en variables de entorno o en un gestor de secretos, y el código solo sabe su **nombre**.

```bash
# .env (local, NUNCA se sube a git)
DATABASE_URL=postgresql://app:cambia_esto@localhost:5432/escuela
JWT_SECRET=cambia_esto_por_algo_aleatorio
STRIPE_API_KEY=sk_test_cambia_esto
```

```bash
# .gitignore
.env
.env.*
!.env.example        # el ejemplo SÍ se sube, con valores falsos
*.pem
*.key
```

```python
import os
from dotenv import load_dotenv     # pip install python-dotenv (solo en desarrollo)

load_dotenv()
DATABASE_URL = os.environ["DATABASE_URL"]       # falla al arrancar si falta: mejor que fallar después
```

```bash
# Generar un secreto aleatorio fuerte
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
openssl rand -base64 32
```

### 🏦 Dónde guardar secretos según el entorno

```capas
Desarrollo : .env local en .gitignore, valores de prueba
CI/CD : GitHub Actions secrets, GitLab CI variables (enmascaradas)
Producción : AWS Secrets Manager, GCP Secret Manager, Azure Key Vault, HashiCorp Vault, Doppler, Infisical
Kubernetes : Secrets + External Secrets o Sealed Secrets (los Secrets son base64, no cifrado)
```

| Opción | Ventaja | Cuidado |
|---|---|---|
| Variables de entorno | Simple, universal | Pueden salir en logs, `docker inspect`, volcados |
| Gestor de secretos | Auditoría, rotación, permisos finos | Coste y algo de complejidad |
| Archivo montado (Docker/K8s secret) | No queda en el entorno del proceso | Permisos del archivo |
| En el código / repo | ❌ Nunca | Queda en el historial para siempre |
| En el frontend | ❌ Nunca | Todo lo que va al navegador es público |

⚠️ Cuidado: en frontend, las variables `VITE_*`, `NEXT_PUBLIC_*` o `REACT_APP_*` se **incrustan en el JavaScript** que descarga cualquiera. Ahí solo van claves públicas (ej. la publishable key de Stripe), nunca la secreta.

### 🚒 Se filtró un secreto: qué hacer (en este orden)

```flujo
dir: abajo
Detectas -> Revocar : 1 ya
Revocar -> Generar : 2 clave nueva
Generar -> Desplegar : 3 actualizar apps
Desplegar -> Revisar : 4 logs de uso
Revisar -> Limpiar : 5 historial git
Limpiar -> Prevenir : 6 escáner + hooks
```

1. **Revoca/rota la clave inmediatamente** en el servicio (AWS, GitHub, Stripe…). Es lo único que de verdad corta el acceso.
2. Genera una nueva y actualiza todos los lugares que la usan.
3. Revisa los logs del servicio: ¿alguien la usó? ¿qué hizo? (facturas de la nube, accesos raros).
4. Limpia el historial con `git filter-repo` o BFG y fuerza el push, avisando al equipo. Pero asume que **ya fue copiada**: hay bots que escanean GitHub en tiempo real.
5. Prevén: escáner de secretos en pre-commit y en CI.

❌ Mal: hacer un commit nuevo que borra la clave y seguir igual. El commit anterior sigue en el historial (y en los forks y clones).

- `gitleaks detect` :: Busca secretos en el repo y su historial
- `gitleaks protect --staged` :: Revisa lo que vas a commitear (ideal en pre-commit)
- `trufflehog git file://.` :: Escáner de secretos que además verifica si siguen activos
- `git filter-repo --path .env --invert-paths` :: Borra un archivo de todo el historial
- `GitHub push protection` :: Bloquea el push si detecta claves de proveedores conocidos

🧠 Caso real: en **2016** atacantes encontraron **credenciales de AWS** en un repositorio **privado** de GitHub que usaban ingenieros de **Uber**; con ellas descargaron datos de unos 57 millones de usuarios y conductores. Uber además pagó a los atacantes para que callaran y lo ocultó un año, lo que empeoró las consecuencias legales. Lección: "es un repo privado" no protege un secreto.

## 🔒 HTTPS y TLS

🧠 Concepto: **TLS** (Transport Layer Security, sucesor de SSL) = protocolo que cifra la conexión entre cliente y servidor. **HTTPS** = HTTP dentro de TLS. Da tres garantías: **confidencialidad** (nadie en el wifi del café lee los datos), **integridad** (nadie los cambia en el camino) y **autenticidad** (hablas con el servidor real, gracias al certificado).

Sin HTTPS, cualquiera en la misma red (o tu proveedor, o un router comprometido) puede leer contraseñas y cookies, o inyectar código en la página: un ataque de **intermediario** (Man-in-the-Middle, MITM).

### 🤝 Handshake TLS 1.3 simplificado

```secuencia
actores: Navegador, Servidor
Navegador -> Servidor : ClientHello: versiones, cifrados, clave pública efímera (ECDHE)
Servidor --> Navegador : ServerHello: elige cifrado + su clave efímera
nota Navegador : ambos calculan el MISMO secreto compartido (Diffie-Hellman)
Servidor --> Navegador : certificado + firma que prueba que tiene la clave privada
nota Navegador : verifica la cadena de certificados hasta una CA de confianza y el dominio
Servidor --> Navegador : Finished (cifrado)
Navegador -> Servidor : Finished (cifrado)
Navegador -> Servidor : GET /login (todo cifrado con claves simétricas AES-GCM o ChaCha20)
```

| Pieza | Para qué | Tipo de cripto |
|---|---|---|
| Intercambio ECDHE | Acordar un secreto sin enviarlo | Asimétrica (curvas elípticas) |
| Certificado X.509 | Probar que el dominio es tuyo | Firma digital de una CA |
| AES-GCM / ChaCha20-Poly1305 | Cifrar los datos de verdad | Simétrica (rápida) |
| Claves efímeras | Forward secrecy: robar la clave privada después no descifra lo pasado | — |

```tiempo
1995 : SSL 2.0 (Netscape)
1999 : TLS 1.0
2008 : TLS 1.2 (todavía muy usado)
2014 : Heartbleed en OpenSSL y ataque POODLE contra SSL 3.0
2015 : Nace Let's Encrypt (certificados gratis; emite desde 2015-2016)
2018 : TLS 1.3 (RFC 8446): handshake más rápido, quita cifrados viejos
2021 : RFC 8996 declara obsoletos TLS 1.0 y 1.1
```

![Logo de Heartbleed (CVE-2014-0160): un fallo en la extensión heartbeat de OpenSSL dejaba leer hasta 64 KB de memoria del servidor por petición, incluidas claves privadas y contraseñas (Wikimedia Commons, CC0)](img/seguridad/heartbleed-logo.png)

### ✅ Buenas prácticas de TLS

- `HSTS` :: `Strict-Transport-Security: max-age=31536000; includeSubDomains` obliga a HTTPS siempre
- `Let's Encrypt + certbot / Caddy` :: Certificados gratis que se renuevan solos (Caddy lo hace automático)
- `TLS 1.2 mínimo, ideal 1.3` :: Desactiva SSLv3, TLS 1.0 y 1.1
- `Redirigir 80 → 443` :: Todo el tráfico HTTP pasa a HTTPS
- `verify=True` :: Nunca desactives la verificación de certificados en clientes

```python
import requests

# ❌ "Arreglar" un error de certificado así: desactiva TODA la protección contra MITM
requests.get("https://api.banco.bo/saldo", verify=False)

# ✅ Si es un certificado interno, indica la CA de tu empresa
requests.get("https://api.interna.local/saldo", verify="/etc/ssl/certs/mi-ca-interna.pem")
```

⚠️ Cuidado: HTTPS protege el **viaje**, no el **destino**. Si tu servidor tiene una inyección SQL, HTTPS te entrega el ataque perfectamente cifrado. El candado del navegador solo dice "la conexión es privada", no "esta web es honesta": los sitios de phishing también tienen HTTPS.

🚀 Futuro: criptografía **post-cuántica**. En 2024 el NIST publicó sus primeros estándares (ML-KEM, antes Kyber; ML-DSA, antes Dilithium) y navegadores como Chrome y Firefox ya ofrecen intercambios híbridos (X25519 + ML-KEM) en TLS para proteger hoy datos que alguien podría guardar y descifrar con un ordenador cuántico futuro ("harvest now, decrypt later").

## 🌍 CORS y cabeceras de seguridad

### 🚧 CORS no es seguridad (de tu servidor)

🧠 Concepto: **Same-Origin Policy** (política del mismo origen) = regla del navegador: el JavaScript de `https://malo.com` no puede **leer** respuestas de `https://tubanco.com`. Origen = esquema + dominio + puerto.

🧠 Concepto: **CORS** (Cross-Origin Resource Sharing) = mecanismo para **relajar** esa regla: tu servidor responde `Access-Control-Allow-Origin: https://mi-frontend.com` para decir "a esta web sí le dejo leer mis respuestas".

Errores de concepto muy comunes:

1. CORS **no protege tu API**: `curl`, Postman, un script de Python o un servidor ignoran CORS por completo. Solo lo aplica el navegador.
2. CORS no impide que la petición **llegue**: en peticiones "simples" (un POST de formulario), el servidor la procesa y el navegador solo oculta la respuesta. Por eso CORS no sustituye la protección CSRF.
3. Es una forma de **abrir** permisos: la configuración segura es la más restrictiva que funcione.

```secuencia
actores: Navegador, API
nota Navegador : JS de https://app.uni.bo quiere PUT a la API
Navegador -> API : OPTIONS /notas (preflight) Origin: https://app.uni.bo
API --> Navegador : Allow-Origin: https://app.uni.bo, Allow-Methods: PUT
Navegador -> API : PUT /notas + cookie
API --> Navegador : 200 OK (el JS puede leer la respuesta)
```

::: columnas
### ❌ Peligroso
```js
// Refleja cualquier origen Y permite cookies:
// cualquier web lee los datos del usuario logueado
app.use(cors({
  origin: (origin, cb) => cb(null, true),
  credentials: true,
}));
```
::: siguiente
### ✅ Restrictivo
```js
const PERMITIDOS = ["https://app.uni.bo"];
app.use(cors({
  origin: (origin, cb) =>
    cb(null, PERMITIDOS.includes(origin)),
  credentials: true,
}));
```
:::

💡 Consejo: el típico error "blocked by CORS policy" en desarrollo se arregla permitiendo **tu** origen (`http://localhost:5173`) o usando el proxy de Vite/Next, no con `*` en producción. Y `*` no se puede combinar con `credentials: true` (el navegador lo rechaza), por eso algunos "reflejan" el origen... que es aún peor.

### 🛡️ Cabeceras HTTP de seguridad

| Cabecera | Valor recomendado | Protege contra |
|---|---|---|
| `Content-Security-Policy` | `default-src 'self'; …` | XSS, inyección de recursos |
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` | Bajar a HTTP, MITM |
| `X-Content-Type-Options` | `nosniff` | El navegador "adivina" el tipo y ejecuta |
| `X-Frame-Options` | `DENY` (o CSP `frame-ancestors`) | Clickjacking (tu web en un iframe trampa) |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | Filtrar URLs con tokens a otros sitios |
| `Permissions-Policy` | `camera=(), geolocation=()` | Uso de APIs del navegador que no necesitas |
| `Cache-Control` | `no-store` en páginas privadas | Datos sensibles en cachés compartidas |

```js
// Express: helmet pone buenas cabeceras por defecto
import helmet from "helmet";
app.use(helmet());
app.disable("x-powered-by");       // no anuncies "Express" a los atacantes
```

```python
# Django settings.py (producción)
DEBUG = False                      # ❌ DEBUG=True muestra trazas, rutas y configuración
SECURE_HSTS_SECONDS = 31536000
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
```

```bash
# Revisa las cabeceras de tu propia web
curl -sI https://tu-dominio.bo | grep -iE "strict|content-security|x-frame|x-content|referrer"
```

💡 Consejo: `python manage.py check --deploy` (Django) revisa la configuración de producción y te avisa de lo que falta.

## 🧹 Validación de entrada y rate limiting

### ✅ Validar en la frontera

🧠 Concepto: **validar** = comprobar que el dato tiene la forma esperada (tipo, longitud, rango, formato) y **rechazar** lo demás. **Sanitizar** = limpiar o transformar el dato. **Escapar** = codificarlo para un contexto de salida concreto (HTML, SQL, shell). Son tres cosas distintas y se complementan.

Regla práctica: **valida a la entrada, escapa a la salida**. La validación no reemplaza la consulta parametrizada ni el escapado: un nombre válido como `O'Brien` lleva una comilla.

::: columnas
### ❌ Lista negra
```python
# Intenta adivinar todo lo malo...
PROHIBIDO = ["<script>", "DROP", "--"]
if any(p in texto for p in PROHIBIDO):
    abort(400)
# <ScRiPt>, <img onerror=…>, drop… pasan
```
::: siguiente
### ✅ Lista blanca + esquema
```python
from pydantic import BaseModel, EmailStr, Field

class Registro(BaseModel):
    email: EmailStr
    nombre: str = Field(min_length=1, max_length=80)
    edad: int = Field(ge=16, le=100)

datos = Registro.model_validate(request.json)
```
:::

| Herramienta | Lenguaje | Ejemplo |
|---|---|---|
| Pydantic | Python (FastAPI) | `class Registro(BaseModel)` |
| Zod | TypeScript | `z.object({ email: z.string().email() })` |
| Joi / Yup | JavaScript | `Joi.string().email()` |
| Bean Validation | Java (Spring) | `@Email @NotBlank` |
| JSON Schema | Cualquiera | Esquema compartido entre servicios |

- Valida **en el servidor** siempre. La validación del frontend es solo comodidad para el usuario: se salta con DevTools o `curl`.
- Limita **longitudes y tamaños** (cuerpo de la petición, arrays, archivos): evita agotar memoria.
- Cuidado con las **regex** complejas: algunas tardan tiempo exponencial con ciertas entradas (**ReDoS**).
- Normaliza antes de comparar (mayúsculas en emails, Unicode NFC) para que `Admin` y `admin` no sean dos usuarios.

### 🚦 Rate limiting y fuerza bruta

🧠 Concepto: **rate limiting** = limitar cuántas peticiones puede hacer un cliente (IP, usuario, API key) en un periodo. Frena la **fuerza bruta** (probar contraseñas), el **credential stuffing** (probar pares email/contraseña filtrados de otros sitios), el scraping y parte de la denegación de servicio.

### ✅ Ejemplo resuelto: ventana deslizante (ejecutado en este PC)

```python
import time
from collections import defaultdict, deque

class LimiteVentana:
    """Permite `maximo` intentos por `ventana` segundos para cada clave (IP, usuario...)."""
    def __init__(self, maximo: int, ventana: float):
        self.maximo, self.ventana = maximo, ventana
        self.intentos = defaultdict(deque)

    def permitir(self, clave: str) -> bool:
        ahora = time.monotonic()
        cola = self.intentos[clave]
        while cola and ahora - cola[0] > self.ventana:   # olvida intentos viejos
            cola.popleft()
        if len(cola) >= self.maximo:
            return False                                  # 429 Too Many Requests
        cola.append(ahora)
        return True

login = LimiteVentana(maximo=5, ventana=60)
for i in range(1, 8):
    print(f"Intento {i} desde 200.87.1.10:", "✅ pasa" if login.permitir("200.87.1.10") else "⛔ 429")
print("Otra IP:", "✅ pasa" if login.permitir("181.115.2.3") else "⛔ 429")
```

```text
Intento 1 desde 200.87.1.10: ✅ pasa
Intento 2 desde 200.87.1.10: ✅ pasa
Intento 3 desde 200.87.1.10: ✅ pasa
Intento 4 desde 200.87.1.10: ✅ pasa
Intento 5 desde 200.87.1.10: ✅ pasa
Intento 6 desde 200.87.1.10: ⛔ 429
Intento 7 desde 200.87.1.10: ⛔ 429
Otra IP: ✅ pasa
```

⚠️ Cuidado: este limitador vive en la memoria de UN proceso. Con varias réplicas detrás de un balanceador cada una cuenta por separado. En producción se usa **Redis** como contador compartido, o el limitador del proxy/CDN (Nginx `limit_req`, Cloudflare, AWS WAF).

```js
// Express: express-rate-limit en la ruta de login
import rateLimit from "express-rate-limit";
const limiteLogin = rateLimit({ windowMs: 15 * 60 * 1000, limit: 10 });
app.post("/login", limiteLogin, iniciarSesion);
```

| Técnica | Frena | Cuidado |
|---|---|---|
| Límite por IP | Un atacante desde una máquina | Botnets con miles de IPs; NAT compartido (universidades) |
| Límite por cuenta | Fuerza bruta a un usuario | Un atacante puede bloquear cuentas ajenas a propósito |
| Retraso progresivo | Hace lento cada intento | Mejor que bloquear en seco |
| CAPTCHA tras N fallos | Bots simples | Molesta; hay servicios que los resuelven |
| MFA | Credential stuffing | La defensa más fuerte |
| Contraseñas filtradas (HIBP) | Reutilización de claves | Usa la API k-anonymity, nunca envíes la contraseña |

💡 Consejo: responde lo mismo para "usuario no existe" y "contraseña incorrecta" ("Email o contraseña incorrectos") y tarda lo mismo. Si no, el atacante puede **enumerar** qué emails están registrados. Lo mismo en "olvidé mi contraseña": "Si el email existe, te enviamos un enlace".

## 🔗 Dependencias y cadena de suministro

🧠 Concepto: **cadena de suministro de software** (software supply chain) = todo lo que no escribiste tú pero acaba en producción: librerías y sus dependencias transitivas, imágenes de Docker, acciones de GitHub, el compilador, el CI. Un proyecto típico de Node tiene cientos de paquetes en `node_modules`; cada uno es código ajeno ejecutándose con tus permisos.

![xkcd 2347 «Dependency»: toda la infraestructura digital moderna apoyada en un proyecto pequeño que mantiene una persona desde 2003 (xkcd.com, CC BY-NC 2.5)](img/seguridad/xkcd-dependency.png)

### 📰 Incidentes reales

```tiempo
2016 : left-pad: un paquete de 11 líneas retirado de npm rompe miles de builds
2017 : Equifax: Apache Struts sin parchear → datos de ~147 millones de personas
2018 : event-stream: nuevo mantenedor añade malware dirigido a una billetera bitcoin
2020 : SolarWinds: el build de Orion comprometido distribuye una puerta trasera
2021 : Log4Shell (CVE-2021-44228) en Log4j 2: ejecución remota con solo loguear un texto
2024 : xz-utils (CVE-2024-3094): puerta trasera tras ~2 años de ingeniería social
```

| Incidente | Qué pasó | Lección |
|---|---|---|
| **Equifax 2017** | Vulnerabilidad de Apache Struts (`CVE-2017-5638`) con parche disponible desde marzo; no se aplicó y los atacantes entraron entre mayo y julio | Inventario de dependencias y parchear rápido |
| **event-stream 2018** | El autor original cedió el paquete npm a un desconocido, que añadió la dependencia `flatmap-stream` con código que robaba fondos de la billetera Copay | Quién mantiene importa; fija versiones y revisa cambios |
| **Log4Shell 2021** | Log4j interpretaba `${jndi:ldap://…}` dentro de los mensajes logueados y cargaba código remoto; CVSS 10 | Las librerías "aburridas" son críticas; SBOM para saber dónde está |
| **xz-utils 2024** | Un colaborador ("Jia Tan") ganó la confianza del mantenedor y metió una puerta trasera en las versiones 5.6.0 y 5.6.1 que afectaba a sshd en algunas distros; la descubrió Andres Freund al notar que SSH tardaba ~0,5 s más | El open source depende de mantenedores agotados; los tarballs pueden diferir del repo |

```secuencia
actores: Atacante, Paquete, Registro, TuApp
Atacante -> Paquete : se gana la confianza o roba la cuenta del mantenedor
Atacante -> Registro : publica versión con código malicioso
TuApp -> Registro : npm install (rango ^1.2.0 acepta la nueva)
Registro --> TuApp : versión maliciosa + script postinstall
nota TuApp : se ejecuta en tu PC y en tu CI con tus secretos
```

### 🧯 Defensas prácticas

- `package-lock.json` / `poetry.lock` / `uv.lock` :: Commitea el lockfile: versiones exactas y hashes
- `npm ci` :: Instala exactamente lo del lockfile (úsalo en CI, no `npm install`)
- `npm audit` :: Lista dependencias con vulnerabilidades conocidas
- `pip-audit` :: Lo mismo para Python (base de datos de PyPA/OSV)
- `npm install --ignore-scripts` :: No ejecuta scripts `postinstall` (vector común de malware)
- `Dependabot / Renovate` :: PRs automáticos para actualizar dependencias
- `Syft / CycloneDX` :: Generan el SBOM (lista de ingredientes del software)
- `Trivy / Grype` :: Escanean imágenes Docker y sistemas de archivos
- `Sigstore / cosign` :: Firmar y verificar artefactos e imágenes

⚠️ Cuidado con el **typosquatting**: paquetes con nombres casi iguales a los populares (`reqeusts` en vez de `requests`) que contienen malware. Copia el nombre desde la documentación oficial. Y con la **confusión de dependencias**: si tu empresa usa un paquete interno `empresa-utils` y alguien publica uno con el mismo nombre en el registro público con versión mayor, algunos instaladores mal configurados eligen el público.

💡 Consejo: antes de añadir una dependencia pregúntate: ¿la necesito o son 10 líneas? ¿está mantenida (último commit, número de mantenedores)? ¿cuántas dependencias trae ella? Menos dependencias = menos superficie de ataque.

🚀 Futuro: tras el ataque a xz y varias olas de paquetes npm comprometidos (incluido el phishing a un mantenedor que en septiembre de 2025 publicó versiones maliciosas de paquetes muy usados como `chalk` y `debug`), los registros empujan **publicación con provenance** (npm `--provenance`, Trusted Publishing en PyPI) y MFA obligatoria para mantenedores. Las normativas (como la Cyber Resilience Act de la UE) piden SBOM y gestión de vulnerabilidades.

## 🐳 Seguridad básica en Docker y Linux

Un contenedor **no es una máquina virtual**: comparte el kernel con el host. Si corre como root y hay una fuga, el atacante está muy cerca del sistema.

::: columnas
### ❌ Dockerfile inseguro
```dockerfile
FROM node:latest
WORKDIR /app
COPY . .
ENV API_KEY=sk_live_cambia_esto
RUN npm install
EXPOSE 3000
CMD ["node", "server.js"]
```
::: siguiente
### ✅ Dockerfile endurecido
```dockerfile
FROM node:22-slim
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev --ignore-scripts
COPY --chown=node:node src/ ./src/
USER node
EXPOSE 3000
CMD ["node", "src/server.js"]
```
:::

| Problema | Por qué es grave | Solución |
|---|---|---|
| `:latest` | No sabes qué versión corre; cambios sorpresa | Etiqueta fija (o digest `@sha256:`) |
| `COPY . .` | Mete `.env`, `.git`, claves en la imagen | `.dockerignore` + copiar solo lo necesario |
| `ENV API_KEY=…` | Queda en las capas: `docker history` lo muestra | Secretos en tiempo de ejecución o `--mount=type=secret` |
| Corre como root | Una fuga da root en el contenedor | `USER` sin privilegios |
| `--privileged` | Casi sin aislamiento con el host | Nunca en producción |
| Montar `docker.sock` | Controlar Docker = ser root del host | Evitarlo |
| Imagen enorme | Más paquetes = más CVE | `slim`, `alpine`, distroless, multi-stage |

```bash
# Ejecutar con menos privilegios
docker run --read-only --cap-drop=ALL --security-opt no-new-privileges \
  --user 1000:1000 -p 127.0.0.1:3000:3000 mi-app:1.4.2

# Escanear la imagen en busca de vulnerabilidades conocidas
trivy image mi-app:1.4.2
```

⚠️ Cuidado: `-p 5432:5432` publica Postgres en **todas** las interfaces, y Docker inserta sus propias reglas de iptables, así que puede quedar expuesto aunque tengas `ufw` activo. Si solo lo usa tu app, no lo publiques, o usa `127.0.0.1:5432:5432`.

### 🐧 Linux en el servidor: lo mínimo

- `ssh-keygen -t ed25519` :: Usa claves SSH, no contraseñas
- `PasswordAuthentication no` :: En `/etc/ssh/sshd_config`: solo claves
- `PermitRootLogin no` :: Entra con tu usuario y usa sudo
- `ufw default deny incoming` :: Firewall: cerrar todo y abrir solo 22, 80, 443
- `unattended-upgrades` / `dnf-automatic` :: Parches de seguridad automáticos
- `chmod 600 .env` :: Solo el dueño puede leer archivos con secretos
- `fail2ban` :: Banea IPs con muchos intentos fallidos de SSH
- `ss -tulpn` :: Revisa qué puertos están escuchando (y cierra lo que sobre)

💡 Consejo: cada servicio con su propio usuario sin login (`useradd --system`), nunca la app corriendo como root. Mínimo privilegio también en el sistema operativo.

## 📜 Logs, monitoreo y privacidad

Si no registras, no te enteras del ataque. Según el informe de IBM sobre el coste de las filtraciones, las empresas tardan del orden de **meses** en identificar y contener una brecha. El fallo de registro y alertas ("Security Logging and Alerting Failures") es el A09 del OWASP Top 10:2025.

### ✅ Qué registrar y qué no

::: columnas
### ✅ Sí registrar
- Logins exitosos y fallidos (usuario, IP, hora)
- Cambios de contraseña, email, MFA
- Accesos denegados (403) y errores de validación repetidos
- Acciones de administración
- Errores 500 con un id de petición
::: siguiente
### ❌ Nunca registrar
- Contraseñas (ni las fallidas)
- Tokens, cookies de sesión, API keys
- Números de tarjeta, CVV
- Datos de salud o documentos completos
- El cuerpo completo de las peticiones sin filtrar
:::

```python
import logging
log = logging.getLogger("auth")

# ❌ Mal: la contraseña y el token terminan en archivos, en el SIEM y en backups
log.info(f"Login fallido: {email} con clave {password}, headers={request.headers}")

# ✅ Bien: lo justo para investigar, sin secretos
log.warning("login_fallido", extra={"email": email, "ip": request.remote_addr,
                                    "request_id": request_id})
```

⚠️ Cuidado con la **inyección en logs**: si registras texto del usuario con saltos de línea, puede falsificar entradas (`"ana\nINFO login_ok admin"`). Usa logs estructurados (JSON), que escapan esos caracteres. Y recuerda Log4Shell: el propio sistema de logs puede ser vulnerable.

🧠 Caso real: en **2019** Facebook reconoció que **cientos de millones** de contraseñas de usuarios se habían guardado en **texto plano en logs internos** accesibles por empleados durante años. No hubo atacante externo: fue un fallo de logging. Twitter reportó un problema parecido en 2018 y pidió a todos sus usuarios cambiar la contraseña.

### 🚨 Monitoreo y respuesta

```flujo
Logs -> Centralizar : ELK, Loki, Datadog
Centralizar -> Alertas : reglas
Alertas -> Humano : 50 logins fallidos/min
Humano -> Respuesta : bloquear, rotar, avisar
```

- Centraliza los logs fuera del servidor (si el atacante entra, no podrá borrarlos tan fácil).
- Define alertas simples: picos de 401/403, logins desde países nuevos, errores 500 en masa.
- Ten un **plan de respuesta a incidentes** escrito antes de necesitarlo: quién decide, a quién se avisa, cómo se rota.

### 🕵️ Privacidad de datos

🧠 Concepto: **privacidad por diseño** = recoger **solo** los datos necesarios, guardarlos el tiempo necesario y protegerlos. El dato más seguro es el que no guardaste.

| Principio | En la práctica |
|---|---|
| Minimización | ¿Necesitas la fecha de nacimiento completa o solo saber si es mayor de edad? |
| Finalidad | Usar los datos solo para lo que se dijo al usuario |
| Retención | Borrar logs y datos viejos automáticamente (ej. 90 días) |
| Seudonimizar | Analítica con ids en vez de nombres y emails |
| Cifrado en reposo | Discos y backups cifrados; columnas muy sensibles cifradas aparte |
| Derechos del usuario | Exportar y borrar su cuenta de verdad (también en backups según política) |

📌 Leyes: en Europa el **RGPD/GDPR** (2018) multa con hasta el 4 % de la facturación anual global; en California la **CCPA**. En Bolivia la Constitución reconoce la protección de datos personales (acción de protección de privacidad) (art. 130), aunque a la fecha de esta hoja no conozco con certeza una ley general equivalente al RGPD: verifícalo. Si trabajas para clientes extranjeros, aplicarás sus leyes igual.

💡 Consejo: no uses datos reales de producción en desarrollo ni en pruebas. Genera datos falsos (Faker) o anonimiza el volcado.

## 🧰 Herramientas y checklist antes de publicar

### 🔧 Herramientas por tipo

🧠 Concepto: **SAST** (Static Application Security Testing) = analiza el **código fuente** sin ejecutarlo. **DAST** (Dynamic) = ataca la aplicación **en marcha** desde fuera, como haría un atacante. **SCA** (Software Composition Analysis) = revisa tus **dependencias** contra bases de vulnerabilidades conocidas (CVE).

```flujo
dir: abajo
Editor -> PreCommit : Semgrep, gitleaks
PreCommit -> CI : SAST + SCA
CI -> Staging : imagen escaneada (Trivy)
Staging -> DAST : OWASP ZAP
DAST -> Produccion : despliegue
Produccion -> Monitoreo : alertas, Dependabot
```

| Herramienta | Tipo | Qué hace | Coste |
|---|---|---|---|
| `npm audit` | SCA | Vulnerabilidades en paquetes npm | Gratis, viene con npm |
| `pip-audit` | SCA | Vulnerabilidades en paquetes Python | Gratis (PyPA) |
| Dependabot | SCA | Alertas y PRs de actualización en GitHub | Gratis en GitHub |
| Snyk | SCA + SAST | Dependencias, código, contenedores | Plan gratis limitado |
| Semgrep | SAST | Reglas por patrones (SQL concatenado, `eval`…) | Motor libre + reglas comunitarias |
| CodeQL | SAST | Análisis de flujo de datos (de dónde viene cada valor) | Gratis en repos públicos de GitHub |
| Bandit | SAST | Errores típicos de seguridad en Python | Gratis |
| OWASP ZAP | DAST | Proxy y escáner de apps web en marcha | Gratis, open source |
| Burp Suite | DAST / manual | Proxy para pruebas manuales | Community gratis, Pro de pago |
| Trivy | Contenedores / IaC | CVE en imágenes, Dockerfile, Terraform | Gratis |
| gitleaks / trufflehog | Secretos | Claves en el repo y su historial | Gratis |

```bash
# Node: ver vulnerabilidades y arreglar las que no rompen versiones mayores
npm audit
npm audit fix

# Python: auditar el entorno actual o un requirements
pip install pip-audit
pip-audit -r requirements.txt

# Semgrep con las reglas de seguridad de la comunidad
semgrep scan --config auto .

# Bandit (Python)
bandit -r src/

# OWASP ZAP baseline (pasivo) contra TU entorno de pruebas, en Docker
docker run --rm -t ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t https://staging.tu-app.bo
```

```yaml
# .github/dependabot.yml: PRs semanales para npm y pip
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
```

⚠️ Cuidado: los escáneres dan **falsos positivos** (avisos que no aplican) y **falsos negativos** (no ven fallos de lógica como un IDOR). Son una red de seguridad, no un reemplazo de entender el código. Un `npm audit` con 0 avisos no significa "app segura".

⚠️ Cuidado: escanea (ZAP, Burp, sqlmap…) **solo tus propios sistemas** o los que tengas permiso escrito para probar. Para practicar existen OWASP Juice Shop, DVWA y los laboratorios de PortSwigger.

### ✅ Checklist antes de publicar

📌 Copia esta lista en la plantilla de tus Pull Requests o en el README del proyecto.

**Código**
1. ¿Todas las consultas SQL están parametrizadas (o usan el ORM sin SQL crudo concatenado)?
2. ¿Nada de `innerHTML`, `v-html`, `dangerouslySetInnerHTML` con datos de usuario sin sanitizar?
3. ¿Cada endpoint comprueba **autenticación y autorización** (dueño del recurso, rol)?
4. ¿Los datos de entrada se validan en el servidor con un esquema (tipos, longitudes, rangos)?
5. ¿Nada de `eval`, `pickle.loads`, `yaml.load` o `os.system` con datos externos?
6. ¿Las rutas de archivos y las URLs que descarga el servidor están confinadas (path traversal, SSRF)?

**Autenticación y sesiones**
7. ¿Contraseñas con Argon2id o bcrypt? ¿Rate limiting en login, registro y "olvidé mi contraseña"?
8. ¿Cookies `HttpOnly`, `Secure`, `SameSite`? ¿Protección CSRF activa?
9. ¿JWT con algoritmo fijo, `exp` corto y verificación de firma?
10. ¿MFA disponible (al menos para administradores)?

**Configuración**
11. ¿`DEBUG` apagado y errores genéricos para el usuario?
12. ¿HTTPS en todo, HSTS y cabeceras de seguridad (CSP, nosniff, frame-ancestors)?
13. ¿CORS solo con los orígenes necesarios?
14. ¿Puertos de BD, Redis y paneles de admin cerrados a internet?

**Secretos y dependencias**
15. ¿Cero secretos en el repo (gitleaks limpio) y `.env` en `.gitignore`?
16. ¿Lockfile commiteado y `npm audit` / `pip-audit` sin vulnerabilidades críticas?
17. ¿Imagen Docker con versión fija, usuario no root y escaneada?

**Operación**
18. ¿Logs de eventos de seguridad, sin contraseñas ni tokens?
19. ¿Backups probados (restaurar al menos una vez) y cifrados?
20. ¿Sabes a quién avisar y qué rotar si mañana hay un incidente?

## 🚨 Errores de otros programadores

Aprender de los fallos ajenos es mucho más barato que de los propios. Cada fila: **causa → consecuencia → cómo evitarlo**.

| Error | Causa | Consecuencia | Cómo evitarlo |
|---|---|---|---|
| Parche sin aplicar | "Ya lo actualizamos el mes que viene" | Equifax 2017: ~147 M de personas | SCA + política de parcheo (críticos en días) |
| Secreto en el repo | Commit rápido con la clave dentro | Uber 2016: 57 M de usuarios | gitleaks en pre-commit, gestor de secretos |
| Contraseñas con hash rápido sin salt | SHA-1 "porque ya es hash" | LinkedIn 2012: hashes crackeados en masa | Argon2id / bcrypt |
| Contraseñas cifradas y no hasheadas | Confundir cifrar con hashear | Adobe 2013: >150 M de registros expuestos | Hash lento con salt |
| Contraseñas en logs | Loguear la petición entera | Facebook 2019: cientos de millones en texto plano interno | Filtrar campos sensibles en el logger |
| SSRF + permisos amplios en la nube | Rol de IAM con demasiado acceso | Capital One 2019: ~100 M de personas | IMDSv2, mínimo privilegio, egress filtering |
| Confiar en el `alg` del JWT | Librería que acepta lo que diga el token | Tokens falsificados de admin | `algorithms=["HS256"]` explícito |
| Bucket S3 público | "Para que el frontend descargue más fácil" | Filtraciones de backups enteros (casos muy repetidos) | Block Public Access, URLs firmadas temporales |
| Base de datos expuesta sin contraseña | MongoDB/Elasticsearch abiertos a internet | Bots que borran y piden rescate | No publicar puertos, autenticación siempre |
| `verify=False` "temporal" | Error de certificado en desarrollo | MITM en producción | Instalar la CA correcta |
| Esconder el botón de admin | Confundir UI con seguridad | Cualquiera llama a la API de admin | Autorización en el backend |
| Mensajes de error detallados | `DEBUG=True` en producción | Rutas, versiones y SQL a la vista | Error genérico + log interno con id |

### 🧠 Historias que conviene conocer

::: desplegable 📖 Equifax 2017: un parche de dos meses
En marzo de 2017 Apache publicó el aviso y el parche de `CVE-2017-5638`, una ejecución remota de código en el parser multipart de **Apache Struts** (a través de la cabecera `Content-Type`). Equifax, una de las grandes agencias de crédito de EE. UU., tenía un portal de disputas con esa versión. Los atacantes entraron a partir de mayo y estuvieron semanas extrayendo datos sin ser detectados (un certificado vencido en su herramienta de inspección de tráfico hizo que no vieran el tráfico cifrado). Resultado: datos de unos **147 millones** de personas (nombres, números de seguro social, fechas de nacimiento), la salida de varios directivos y un acuerdo con reguladores de EE. UU. de cientos de millones de dólares.

Lecciones: inventario de qué librerías usa cada sistema, parchear lo crítico en días, monitoreo que funcione (y certificados que no venzan sin aviso).
:::

::: desplegable 📖 Log4Shell 2021: el log que ejecutaba código
Log4j 2 (librería de logs de Java usadísima) soportaba "lookups": expresiones como `${java:version}` dentro del texto logueado se sustituían. Una de ellas, JNDI, podía consultar un servidor LDAP remoto y cargar una clase Java desde él. Bastaba que la app **logueara** un texto controlado por el atacante (un user-agent, un nombre de usuario, un mensaje de chat de Minecraft) para que el servidor descargara y ejecutara código. Se publicó en diciembre de 2021 con CVSS 10.0; hubo varias versiones de parche seguidas (2.15, 2.16, 2.17) porque los primeros arreglos fueron incompletos.

Lecciones: una dependencia indirecta puede ser crítica; necesitas un **SBOM** para responder en horas "¿dónde usamos Log4j?"; y las funciones "mágicas" sobre datos externos (interpretar el texto logueado) son peligrosas.
:::

::: desplegable 📖 event-stream 2018: confiar en un desconocido
`event-stream` era un paquete npm con millones de descargas semanales. Su autor, sin tiempo para mantenerlo, aceptó la ayuda de un usuario que se ofreció y le dio permisos de publicación. El nuevo mantenedor añadió una dependencia, `flatmap-stream`, cuyo código ofuscado solo se activaba dentro de la aplicación de la billetera bitcoin **Copay** para robar fondos. Se descubrió en noviembre de 2018, semanas después.

Lecciones: los rangos `^` aceptan versiones nuevas sin que te enteres; revisa los cambios de dependencias críticas; el ataque fue social, no técnico.
:::

::: desplegable 📖 xz-utils 2024: dos años de paciencia
xz/liblzma es una librería de compresión presente en casi todas las distribuciones Linux. Una cuenta llamada "Jia Tan" contribuyó durante unos dos años, mientras otras cuentas presionaban al mantenedor original (agotado) para que sumara ayuda. Jia Tan terminó como co-mantenedor y en 2024 publicó las versiones **5.6.0 y 5.6.1** con una puerta trasera escondida en archivos de prueba binarios y en el script de build de los tarballs (no visible en el repositorio git normal). En algunas distribuciones, sshd carga liblzma a través de un parche con libsystemd, y la puerta trasera interceptaba la autenticación de SSH. El 29 de marzo de 2024 **Andres Freund**, ingeniero de Microsoft que trabaja en PostgreSQL, notó que los logins por SSH en Debian testing tardaban unos 500 ms más y usaban más CPU; investigó y lo destapó antes de que llegara a las versiones estables de las grandes distros (`CVE-2024-3094`, CVSS 10).

Lecciones: el open source crítico depende de pocas personas cansadas; los artefactos publicados deben poder reconstruirse desde el código (builds reproducibles); y medir el rendimiento también detecta ataques.
:::

## 🏋️ Ejercicios: encuentra la vulnerabilidad

📌 Para cada fragmento: (1) nombra la vulnerabilidad, (2) explica cómo la aprovecharía alguien y qué rompe de la CIA, (3) escribe la corrección. Intenta antes de abrir la solución.

### 1️⃣ Fácil: el buscador de libros

```python
@app.get("/buscar")
def buscar():
    titulo = request.args.get("q", "")
    filas = db.execute(f"SELECT titulo, autor FROM libros WHERE titulo LIKE '%{titulo}%'")
    return {"resultados": [dict(f) for f in filas]}
```

::: desplegable 🧩 Ver la solución
**Inyección SQL**: el texto de búsqueda se pega dentro de la consulta. Una comilla cierra el string y el resto se ejecuta como SQL (podría unir con `UNION SELECT` otra tabla como `usuarios`). Rompe la **confidencialidad** (y la integridad si el usuario de la BD puede modificar).

```python
@app.get("/buscar")
def buscar():
    titulo = request.args.get("q", "")[:100]          # límite de longitud
    filas = db.execute(
        "SELECT titulo, autor FROM libros WHERE titulo LIKE ?",
        (f"%{titulo}%",),                              # los % van en el PARÁMETRO
    )
    return {"resultados": [dict(f) for f in filas]}
```
:::

### 2️⃣ Fácil: el saludo

```js
const params = new URLSearchParams(location.search);
document.getElementById("saludo").innerHTML = "Hola, " + params.get("nombre");
```

::: desplegable 🧩 Ver la solución
**XSS basado en DOM** (reflejado en la URL). Un enlace con `?nombre=<img src=x onerror=…>` ejecuta JavaScript en tu origen cuando la víctima lo abre: puede leer datos de la página y hacer peticiones como ella. Rompe confidencialidad e integridad.

```js
const params = new URLSearchParams(location.search);
document.getElementById("saludo").textContent = "Hola, " + (params.get("nombre") ?? "");
```

Capa extra: una CSP sin `'unsafe-inline'` habría bloqueado el manejador `onerror` en línea.
:::

### 3️⃣ Medio: descargar facturas

```python
@app.get("/facturas/<int:factura_id>/pdf")
@login_required
def descargar(factura_id):
    factura = Factura.query.get_or_404(factura_id)
    return send_file(f"/srv/facturas/{factura.archivo}")
```

::: desplegable 🧩 Ver la solución
**IDOR / control de acceso roto**: cualquier usuario logueado descarga cualquier factura cambiando el número. Rompe la **confidencialidad**. Además, si `factura.archivo` alguna vez viene del usuario, hay riesgo de path traversal.

```python
from flask import send_from_directory

@app.get("/facturas/<int:factura_id>/pdf")
@login_required
def descargar(factura_id):
    factura = Factura.query.filter_by(
        id=factura_id, cliente_id=current_user.id
    ).first_or_404()
    # send_from_directory rechaza rutas que salgan de la carpeta
    return send_from_directory("/srv/facturas", factura.archivo)
```

Y un test: el usuario B pide la factura de A y debe recibir 404.
:::

### 4️⃣ Medio: el registro de usuarios

```python
import hashlib

def registrar(email, password):
    h = hashlib.sha256(password.encode()).hexdigest()
    db.execute("INSERT INTO usuarios (email, pass) VALUES (?, ?)", (email, h))
    log.info(f"Nuevo usuario {email} con contraseña {password}")
```

::: desplegable 🧩 Ver la solución
Dos fallos:
1. **Hash inadecuado**: SHA-256 es rápido y sin salt. Si roban la base, las contraseñas comunes se crackean en minutos y usuarios con la misma contraseña tienen el mismo hash.
2. **Contraseña en el log**: queda en texto plano en archivos, sistemas de logs y backups.

```python
from argon2 import PasswordHasher
ph = PasswordHasher()

def registrar(email, password):
    if len(password) < 12:
        raise ValueError("La contraseña debe tener al menos 12 caracteres")
    h = ph.hash(password)                              # Argon2id con salt incluido
    db.execute("INSERT INTO usuarios (email, pass) VALUES (?, ?)", (email.lower(), h))
    log.info("usuario_registrado", extra={"email": email.lower()})
```
:::

### 5️⃣ Medio: la API de perfil

```js
app.put("/api/perfil", auth, async (req, res) => {
  const usuario = await Usuario.findByIdAndUpdate(req.user.id, req.body, { new: true });
  res.json(usuario);
});
```

::: desplegable 🧩 Ver la solución
**Asignación masiva** (mass assignment, una forma de control de acceso roto): el cliente puede enviar `{"rol": "admin"}` o `{"saldo": 99999}` y se guarda. Además la respuesta devuelve el documento entero, quizá con el hash de la contraseña (**exposición de datos**).

```js
const Perfil = z.object({
  nombre: z.string().min(1).max(80),
  bio: z.string().max(500).optional(),
});

app.put("/api/perfil", auth, async (req, res) => {
  const datos = Perfil.parse(req.body);                       // solo campos permitidos
  const u = await Usuario.findByIdAndUpdate(req.user.id, datos, { new: true })
    .select("nombre bio email");                              // solo campos públicos
  res.json(u);
});
```
:::

### 6️⃣ Medio: el verificador de tokens

```python
import jwt

def usuario_del_token(token):
    datos = jwt.decode(token, options={"verify_signature": False})
    return Usuario.get(datos["sub"])
```

::: desplegable 🧩 Ver la solución
**Autenticación rota**: lee el JWT **sin verificar la firma**. Cualquiera puede fabricar un token con `"sub": "1"` (el admin) y entrar como él. Rompe todo: confidencialidad, integridad y suplantación (la S de STRIDE).

```python
import jwt, os

SECRETO = os.environ["JWT_SECRET"]

def usuario_del_token(token):
    datos = jwt.decode(token, SECRETO, algorithms=["HS256"],
                       options={"require": ["exp", "sub"]})
    return Usuario.get(datos["sub"])
```
:::

### 7️⃣ Difícil: la vista previa de enlaces

```python
@app.post("/preview")
@login_required
def preview():
    url = request.json["url"]
    r = requests.get(url, timeout=5, allow_redirects=True)
    titulo = re.search(r"<title>(.*?)</title>", r.text)
    return {"titulo": titulo.group(1) if titulo else url}
```

::: desplegable 🧩 Ver la solución
**SSRF**: el servidor descarga cualquier URL, incluidas `http://localhost:8080/admin`, `http://10.0.0.5:9200` (Elasticsearch interno) o el servicio de metadatos de la nube `169.254.169.254`. Las redirecciones permiten saltarse una validación superficial. Rompe la confidencialidad de la red interna.

Corrección por capas:
1. Solo `https`, y resolver el host y rechazar IPs privadas, loopback y link-local (ver la sección 🛰️ SSRF).
2. `allow_redirects=False` (o revalidar cada salto).
3. Limitar el tamaño de la respuesta (`stream=True` y leer como máximo, p. ej., 1 MB).
4. Ejecutar el servicio de vistas previas en una red sin acceso a la interna, e IMDSv2 en la nube.
5. Escapar `titulo` al mostrarlo (si no, es además un XSS almacenado o reflejado).
:::

### 8️⃣ Difícil: el Dockerfile y el compose

```dockerfile
FROM python:latest
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV DB_PASSWORD=cambia_esto
CMD ["python", "app.py"]
```

```yaml
services:
  db:
    image: postgres:16
    ports:
      - "5432:5432"
    environment:
      POSTGRES_PASSWORD: cambia_esto
```

::: desplegable 🧩 Ver la solución
1. `python:latest`: versión impredecible, imagen grande con muchos CVE → `python:3.13-slim` (versión fija).
2. `COPY . /app` sin `.dockerignore`: mete `.env`, `.git` y claves en la imagen → `.dockerignore` y copiar solo `src/` y `requirements.txt`.
3. `ENV DB_PASSWORD`: el secreto queda en la imagen y en `docker inspect` / `docker history` → pasarlo en tiempo de ejecución (secret de compose, gestor de secretos).
4. Corre como **root** → `RUN useradd --system app` y `USER app`.
5. `ports: "5432:5432"`: la base queda expuesta a internet (y Docker puede saltarse ufw) → quitar `ports` (la app la alcanza por la red interna de compose) o `127.0.0.1:5432:5432`.
6. Contraseña débil y en texto plano en el compose → `secrets:` con archivo fuera del repo.
:::

### 9️⃣ Difícil: restablecer la contraseña

```python
import random

@app.post("/olvide")
def olvide():
    u = Usuario.por_email(request.form["email"])
    if not u:
        return "Ese email no está registrado", 404
    u.token_reset = str(random.randint(100000, 999999))
    db.commit()
    enviar_email(u.email, f"https://app.bo/reset?token={u.token_reset}")
    return "Te enviamos un enlace"
```

::: desplegable 🧩 Ver la solución
Varios fallos de lógica:
1. **Enumeración de usuarios**: el 404 revela qué emails existen. Responde siempre igual.
2. **Token predecible y corto**: `random` no es criptográfico y 6 dígitos son solo un millón de opciones (fuerza bruta). Usa `secrets.token_urlsafe(32)`.
3. **Sin expiración ni un solo uso**: el token sirve para siempre. Guarda la fecha y bórralo al usarlo.
4. **Token en texto plano en la BD**: guarda su hash (SHA-256 sirve aquí porque el token ya es aleatorio y largo).
5. **Sin rate limiting**: permite bombardear el correo de alguien.

```python
import secrets, hashlib
from datetime import datetime, timedelta, timezone

@app.post("/olvide")
@limitar(5, por_minutos=15)
def olvide():
    u = Usuario.por_email(request.form["email"].lower())
    if u:
        token = secrets.token_urlsafe(32)
        u.reset_hash = hashlib.sha256(token.encode()).hexdigest()
        u.reset_expira = datetime.now(timezone.utc) + timedelta(minutes=30)
        db.commit()
        enviar_email(u.email, f"https://app.bo/reset?token={token}")
    return "Si el email existe, te enviamos un enlace (válido 30 minutos)"
```
:::

### 🔟 Reto de diseño: modelo de amenazas

Dibuja el flujo de datos de una app de **notas universitarias** (alumnos ven sus notas, docentes las ponen, admin gestiona cursos) y aplica STRIDE a cada flecha.

::: desplegable 🧩 Ver una propuesta
| STRIDE | Amenaza en la app de notas | Mitigación |
|---|---|---|
| Spoofing | Un alumno roba la sesión de un docente | Cookies HttpOnly/Secure, MFA para docentes |
| Tampering | Alumno cambia su nota con `PUT /notas/123` | Solo el docente del curso puede escribir; validar en backend |
| Repudiation | Docente niega haber cambiado una nota | Tabla de auditoría (quién, cuándo, valor anterior y nuevo) |
| Information disclosure | Alumno ve notas de otros (IDOR) | Filtrar por `alumno_id` en cada consulta |
| Denial of service | Bots saturan el sistema el día de publicación | Rate limiting, caché, escalado |
| Elevation of privilege | Alumno se pone `rol: docente` vía asignación masiva | Lista blanca de campos, roles solo los cambia admin |
:::

## 🎤 Preguntas de entrevista

::: desplegable ❓ ¿Cuál es la diferencia entre autenticación y autorización?
**Autenticación** responde "¿quién eres?" (login con contraseña, MFA, OIDC). **Autorización** responde "¿qué puedes hacer?" (roles, permisos, ser dueño del recurso). Ejemplo: estar logueado como alumno (autenticado) no te autoriza a ver las notas de otro alumno. El fallo n.º 1 del OWASP Top 10 (A01, en 2021 y 2025) es de autorización, no de autenticación.
:::

::: desplegable ❓ ¿Cómo previenes una inyección SQL? ¿Basta con escapar comillas?
Con **consultas parametrizadas** (prepared statements) o un ORM bien usado: el SQL y los datos viajan separados y el dato nunca se interpreta como código. Escapar a mano no basta: hay codificaciones, números sin comillas y casos que se escapan. Para lo que no se puede parametrizar (nombres de columna, `ORDER BY`), lista blanca. Como defensa en profundidad: usuario de BD con mínimo privilegio y errores genéricos.
:::

::: desplegable ❓ Explica XSS y cómo lo mitigarías en una app React
XSS es cuando el atacante logra ejecutar su JavaScript en tu origen, en el navegador de otro usuario. React escapa por defecto lo que pones en `{}`, así que el riesgo aparece en `dangerouslySetInnerHTML` (sanitizar con DOMPurify), en atributos como `href` con `javascript:` (validar el esquema), en librerías que manipulan el DOM directamente y en el HTML que genera el servidor. Además: CSP estricta sin `'unsafe-inline'`, cookies `HttpOnly` y no guardar tokens de larga vida en `localStorage`.
:::

::: desplegable ❓ ¿Qué es CSRF y por qué SameSite ayuda?
CSRF es cuando otra web hace que el navegador de la víctima envíe una petición a tu sitio, y el navegador adjunta automáticamente sus cookies, así que tu servidor cree que la víctima la quiso hacer. `SameSite=Lax/Strict` le dice al navegador que no envíe la cookie en peticiones iniciadas desde otros sitios (salvo navegación GET de primer nivel en Lax). Se complementa con tokens anti-CSRF y con no cambiar estado mediante GET.
:::

::: desplegable ❓ ¿Cómo guardarías las contraseñas de los usuarios?
Nunca en texto plano ni cifradas. Con una función de hash de contraseñas **lenta y con salt**: Argon2id (primera opción de OWASP), scrypt o bcrypt; PBKDF2 si hay requisitos FIPS. El salt es aleatorio por usuario y va dentro del hash. Verificar con la función de la librería (comparación en tiempo constante). Además: rate limiting en el login, bloquear contraseñas filtradas, ofrecer MFA y rehashear con parámetros más fuertes cuando el usuario inicie sesión si el coste quedó viejo.
:::

::: desplegable ❓ ¿JWT o sesiones? ¿Dónde guardas el token en el frontend?
Depende. Sesiones en cookie `HttpOnly` son simples, revocables al instante e inmunes a que un XSS lea el token: ideales para una web con su propio backend. JWT sirve cuando varios servicios deben verificar sin consultar un almacén central. Si uso JWT: algoritmo fijo, `exp` corto (5–15 min), refresh token rotado en cookie `HttpOnly; Secure; SameSite`, y el access token en memoria, no en `localStorage`. Nunca datos sensibles en el payload: no está cifrado.
:::

::: desplegable ❓ ¿Qué es CORS? ¿Protege mi API?
CORS es un mecanismo del **navegador** para permitir que JavaScript de otro origen lea respuestas de tu API, relajando la Same-Origin Policy. No protege la API: `curl` o un servidor ignoran CORS, y en peticiones simples la petición llega igual al servidor. La seguridad de la API sale de la autenticación, la autorización y la protección CSRF. CORS debe configurarse lo más restrictivo posible (lista de orígenes exacta, nunca reflejar cualquier origen con credenciales).
:::

::: desplegable ❓ Subiste por error una API key a un repo público. ¿Qué haces?
1. **Revocarla/rotarla de inmediato** en el proveedor (lo primero, porque hay bots que escanean GitHub en segundos). 2. Poner la nueva en el gestor de secretos y desplegar. 3. Revisar logs de uso y facturación del proveedor para ver si alguien la usó. 4. Limpiar el historial con `git filter-repo`, sabiendo que ya pudo copiarse. 5. Prevenir: gitleaks en pre-commit, push protection, `.env` en `.gitignore`. Y avisar al equipo de seguridad: ocultarlo empeora todo (caso Uber 2016).
:::

::: desplegable ❓ ¿Qué es SSRF y por qué es tan peligroso en la nube?
Es cuando tu servidor hace peticiones a URLs elegidas por el usuario y el atacante lo usa para llegar a servicios internos. En la nube, el servicio de metadatos (por ejemplo `169.254.169.254` en AWS) entrega credenciales temporales del rol de la máquina: con ellas se puede leer almacenamiento y otros recursos (caso Capital One 2019). Mitigación: lista blanca de dominios, bloquear IPs privadas tras resolver DNS, sin redirecciones, aislamiento de red, IMDSv2 y roles con mínimo privilegio.
:::

::: desplegable ❓ ¿Qué aprendiste de Log4Shell o xz-utils como desarrollador?
Que las dependencias son parte de tu superficie de ataque, incluidas las indirectas. Hay que saber qué usas (lockfiles, SBOM), poder actualizar rápido (tests, CI, Dependabot) y desconfiar de funcionalidades "mágicas" sobre datos externos (Log4j interpretaba el texto logueado). xz-utils mostró que un ataque puede ser de ingeniería social a largo plazo contra un mantenedor agotado, y que medir anomalías (SSH 500 ms más lento) puede destapar algo enorme.
:::

::: desplegable ❓ ¿Qué es defensa en profundidad? Pon un ejemplo
Poner varias capas de protección independientes para que el fallo de una no comprometa todo. Ejemplo contra XSS: escapado automático del framework + sanitización de HTML enriquecido + CSP estricta + cookies `HttpOnly`. Si un desarrollador usa `innerHTML` por error, la CSP frena el script; si la CSP tiene un hueco, el atacante igual no puede leer la cookie de sesión.
:::

::: desplegable ❓ ¿Qué es el principio de mínimo privilegio? Dame tres ejemplos en un proyecto web
Cada componente solo tiene los permisos que necesita. Ejemplos: (1) el usuario de la base de datos de la app no puede hacer `DROP` ni leer otras bases; (2) el contenedor corre con `USER` no root, `--cap-drop=ALL` y sistema de archivos de solo lectura; (3) el token de CI que despliega solo puede escribir en ese proyecto y los scopes de OAuth piden solo `openid email`. Así, si algo se compromete, el daño queda acotado.
:::

## 🇬🇧 Vocabulario y resumen final

| English | Suena | Español |
|---|---|---|
| vulnerability | /vulnerabíliti/ | vulnerabilidad |
| threat | /zret/ | amenaza |
| attack surface | /aták sérfis/ | superficie de ataque |
| injection | /inyékshon/ | inyección |
| cross-site scripting | /kros sáit skrípting/ | XSS, scripts entre sitios |
| request forgery | /rikuést fórcheri/ | falsificación de peticiones |
| path traversal | /paz travérsal/ | recorrido de directorios |
| deserialization | /diserialaiséishon/ | deserialización |
| hashing | /háshing/ | calcular el hash |
| salt | /solt/ | sal (valor aleatorio) |
| brute force | /brut fors/ | fuerza bruta |
| credential stuffing | /kredénshal stáfing/ | relleno de credenciales filtradas |
| access control | /ákses kontróul/ | control de acceso |
| privilege escalation | /prívilech eskaléishon/ | escalada de privilegios |
| secret leak | /síkret lik/ | filtración de un secreto |
| to rotate a key | /tu róteit a ki/ | rotar (cambiar) una clave |
| handshake | /jándsheik/ | saludo inicial (TLS) |
| supply chain | /suplái chéin/ | cadena de suministro |
| backdoor | /bákdor/ | puerta trasera |
| patch | /pach/ | parche |
| breach | /brich/ | brecha, filtración |
| incident response | /ínsident rispóns/ | respuesta a incidentes |
| rate limiting | /réit límiting/ | limitación de frecuencia |
| least privilege | /list prívilech/ | mínimo privilegio |

🇬🇧 Frases útiles: "**We need to rotate this key, it was leaked in a commit**" (hay que rotar esta clave, se filtró en un commit) · "**This endpoint is missing an authorization check**" (a este endpoint le falta comprobar permisos) · "**Always use parameterized queries**" (usa siempre consultas parametrizadas) · "**Never trust user input**" (nunca confíes en la entrada del usuario).

### 📌 Resumen tipo chuleta

| Ataque | Idea en una línea | Defensa principal |
|---|---|---|
| Inyección SQL | El dato se ejecuta como SQL | Consultas parametrizadas |
| Inyección de comandos | El dato se ejecuta en la shell | `subprocess.run([...])` sin shell |
| XSS | Tu web ejecuta JS del atacante | Escapar salida + CSP + HttpOnly |
| CSRF | Otra web usa tus cookies | SameSite + token anti-CSRF |
| SSRF | Tu servidor pide URLs internas | Lista blanca + bloquear IPs privadas |
| Path traversal | `../` sale de la carpeta | `resolve()` + comprobar que sigue dentro |
| Deserialización | Cargar objetos ejecuta código | JSON, `safe_load`, nunca pickle externo |
| Contraseñas débiles | Hash rápido o sin salt | Argon2id / bcrypt + MFA + rate limit |
| JWT mal usado | `alg none`, sin `exp`, en localStorage | Algoritmo fijo, exp corto, cookie HttpOnly |
| IDOR | Cambiar el id y ver lo ajeno | Filtrar por dueño en cada consulta |
| Secretos filtrados | Claves en git o en el frontend | Gestor de secretos + rotar al filtrarse |
| Dependencias | Código ajeno vulnerable o malicioso | Lockfile + audit + Dependabot + SBOM |

```capas
1 Nunca confíes en la entrada : valida en el servidor, escapa en la salida
2 Separa datos y código : parametriza SQL, sin shell, sin eval ni pickle
3 Quién eres y qué puedes : autenticación fuerte + autorización en cada endpoint
4 Protege lo guardado : hash lento, cifrado, secretos fuera del código
5 Protege el viaje : HTTPS, HSTS, cookies Secure
6 Vigila lo ajeno : dependencias, imágenes, CI
7 Entérate y reacciona : logs sin secretos, alertas, plan de incidentes
```

💡 La pregunta que resume toda la hoja, para cada línea que recibe datos de fuera: **"¿Y si quien envía esto no es quien creo, y lo que envía no es lo que espero?"**
