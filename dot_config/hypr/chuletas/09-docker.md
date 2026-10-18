# 🐳 Docker
> Empaqueta tu app con todo lo que necesita y córrela igual en tu laptop, en la de tu compañero y en el servidor.

## 🤔 Qué es Docker y por qué usarlo

El problema clásico: "en mi máquina sí funciona". Tu app usa Python 3.12, una librería concreta y Postgres 16; en el servidor hay Python 3.9 y otra versión de todo. Docker resuelve esto metiendo tu app **junto con todo lo que necesita** (sistema base, librerías, configuración) en una caja estándar llamada **contenedor**.

Analogía: piensa en los **contenedores de carga** de un barco que llega a Arica. Al puerto no le importa si dentro hay quinua, televisores o ropa: todos los contenedores tienen el mismo tamaño y se mueven con la misma grúa. Docker hace lo mismo con el software: da igual si es Python, Node o Java, se arranca, se para y se mueve con los mismos comandos.

### 🆚 Contenedor vs máquina virtual

Una **máquina virtual (VM)** emula un computador entero: tiene su propio kernel y su propio sistema operativo completo (pesa GB y tarda en arrancar). Un **contenedor** comparte el kernel de Linux de tu máquina y solo aísla los procesos, archivos y red: pesa MB y arranca en segundos.

Analogía: una VM es **una casa completa** (cimientos, tuberías, techo propios); un contenedor es **un departamento en un edificio**: cada uno tiene su llave y sus cosas, pero comparten los cimientos (el kernel).

| Aspecto | Máquina virtual | Contenedor |
|---|---|---|
| Qué virtualiza | El hardware entero | Solo el sistema operativo (procesos) |
| Kernel | Propio | Compartido con el anfitrión |
| Tamaño típico | Varios GB | Decenas a cientos de MB |
| Arranque | Minutos | Segundos o menos |
| Aislamiento | Muy fuerte | Fuerte, pero menor que una VM |
| Ejemplo | VirtualBox, VMware, QEMU | Docker, Podman |

```text
   MÁQUINA VIRTUAL                  CONTENEDORES
 +-------+ +-------+            +-------+ +-------+
 | App A | | App B |            | App A | | App B |
 | Libs  | | Libs  |            | Libs  | | Libs  |
 | SO    | | SO    |            +-------+ +-------+
 +-------+ +-------+            |   Docker Engine   |
 |   Hipervisor    |            |  SO anfitrión     |
 |  SO anfitrión   |            |  (kernel Linux)   |
 |   Hardware      |            |    Hardware       |
 +-----------------+            +-------------------+
```

📌 Docker no es magia: usa funciones del kernel Linux (namespaces para aislar y cgroups para limitar CPU/RAM). Por eso en Windows y Mac corre dentro de una VM Linux pequeña.

💡 Consejo: en IA y ciencia de datos Docker es oro: congelas la versión exacta de Python, CUDA y librerías y tu experimento se puede repetir meses después.

🇬🇧 **container** /kontéiner/ = contenedor · **virtual machine** /vérchual mashín/ = máquina virtual · **host** /jóust/ = anfitrión · **kernel** /kérnel/ = núcleo del SO · **lightweight** /láit-uéit/ = ligero

## 🛠️ Instalación en Arch Linux

En Arch (y CachyOS) Docker está en los repos oficiales. El servicio `docker` es un **daemon** (programa en segundo plano) que hace el trabajo; el comando `docker` solo le manda órdenes.

```bash
# 1. Instalar Docker y el plugin de compose
sudo pacman -S docker docker-compose docker-buildx

# 2. Arrancar el servicio ahora y en cada encendido
sudo systemctl enable --now docker.service

# 3. Usar docker sin sudo: entrar al grupo docker
sudo usermod -aG docker $USER

# 4. Cerrar sesión y volver a entrar (o reiniciar) para que el grupo se aplique
#    Comprobar:
groups              # debe aparecer "docker"
docker run --rm hello-world
```

- `systemctl status docker` :: Ver si el daemon está corriendo
- `docker version` :: Versión del cliente y del servidor (si falla el servidor, el daemon no corre)
- `docker info` :: Resumen: contenedores, imágenes, driver de almacenamiento
- `newgrp docker` :: Aplica el grupo docker en la terminal actual sin cerrar sesión
- `sudo systemctl stop docker.socket docker.service` :: Apagar Docker del todo

⚠️ Cuidado: estar en el grupo `docker` equivale a tener root (puedes montar `/` dentro de un contenedor). Solo añade usuarios de confianza.

⚠️ Cuidado: el error "permission denied while trying to connect to the Docker daemon socket" casi siempre significa que aún no cerraste sesión tras `usermod -aG docker`.

💡 Consejo: en fish la variable `$USER` funciona igual; si dudas, escribe tu usuario directamente: `sudo usermod -aG docker yafer`.

🇬🇧 **daemon** /dímon/ = proceso en segundo plano · **socket** /sóket/ = punto de conexión · **group** /grup/ = grupo · **permission denied** /permíshon dinái/ = permiso denegado

## 📦 Imágenes vs contenedores

Esta es LA idea clave de Docker:

- Una **imagen** es una plantilla de solo lectura: el sistema de archivos con tu app y sus dependencias, más la instrucción de qué ejecutar.
- Un **contenedor** es una imagen **en ejecución**: un proceso vivo con una capa propia donde puede escribir.

Analogía de programación: la imagen es la **clase** y el contenedor es el **objeto** (instancia). De una imagen `python:3.12` puedes crear 10 contenedores, igual que de una clase `Perro` creas 10 perros. Otra analogía: la imagen es la **receta/molde de un pastel**; el contenedor es el pastel que estás comiendo.

```text
 Dockerfile  --docker build-->  IMAGEN  --docker run-->  CONTENEDOR(es)
 (receta)                       (molde)                  (pasteles)
```

### 🏷️ Nombres de imágenes y etiquetas

Una imagen se nombra `usuario/repositorio:etiqueta`. La **etiqueta** (tag) suele ser la versión. Si no pones etiqueta, Docker usa `latest`.

| Nombre | Significado |
|---|---|
| `python:3.12-slim` | Imagen oficial de Python 3.12, versión reducida |
| `node:20-alpine` | Node 20 sobre Alpine Linux (muy pequeña, ~50 MB) |
| `postgres:16` | Postgres versión 16 |
| `yafer/miapi:1.0` | Tu imagen `miapi` en tu cuenta de Docker Hub, versión 1.0 |
| `ghcr.io/user/app:main` | Imagen alojada en GitHub Container Registry |

- `docker pull python:3.12-slim` :: Descarga una imagen sin ejecutarla
- `docker images` :: Lista las imágenes locales (también `docker image ls`)
- `docker ps` :: Contenedores en ejecución
- `docker ps -a` :: Todos los contenedores, incluidos los detenidos

💡 Consejo: prefiere las variantes `-slim` para Python (basadas en Debian, compatibles con casi todo) y `-alpine` para Node. Alpine usa `musl` en vez de `glibc` y algunas librerías de Python con C (numpy, pandas) dan problemas ahí.

⚠️ Cuidado: no uses `latest` en producción: hoy es Python 3.12 y mañana puede ser 3.14 y romper tu app. Fija la versión.

🇬🇧 **image** /ímich/ = imagen · **tag** /tag/ = etiqueta · **pull** /pul/ = descargar (jalar) · **registry** /réyistri/ = registro (almacén de imágenes) · **read-only** /ríd ónli/ = solo lectura

## ⌨️ Comandos esenciales

Estos son los que usarás el 90 % del tiempo. Casi todos aceptan el **nombre** o el **ID** (basta con los primeros 3-4 caracteres del ID).

| Comando | Qué hace | Ejemplo |
|---|---|---|
| `docker run` | Crea y arranca un contenedor desde una imagen | `docker run -d nginx` |
| `docker ps` | Lista contenedores vivos (`-a` todos) | `docker ps -a` |
| `docker stop` | Detiene un contenedor (amable, SIGTERM) | `docker stop web` |
| `docker start` | Vuelve a arrancar uno detenido | `docker start web` |
| `docker restart` | Detiene y arranca | `docker restart web` |
| `docker rm` | Borra un contenedor detenido (`-f` fuerza) | `docker rm web` |
| `docker images` | Lista imágenes | `docker images` |
| `docker rmi` | Borra una imagen | `docker rmi nginx:latest` |
| `docker build` | Construye una imagen desde un Dockerfile | `docker build -t miapp .` |
| `docker logs` | Muestra la salida del contenedor | `docker logs -f web` |
| `docker exec` | Ejecuta un comando dentro de un contenedor vivo | `docker exec -it web bash` |
| `docker pull` / `push` | Descarga / sube imágenes | `docker push yafer/miapp:1.0` |
| `docker inspect` | Todo el detalle en JSON | `docker inspect web` |
| `docker stats` | Uso de CPU/RAM en vivo | `docker stats` |
| `docker cp` | Copia archivos entre host y contenedor | `docker cp web:/app/log.txt .` |

- `docker stop $(docker ps -q)` :: Detiene todos los contenedores en ejecución (en fish: `docker stop (docker ps -q)`)
- `docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"` :: Lista compacta con nombre, estado y puertos
- `docker container ls -a --filter status=exited` :: Solo los contenedores detenidos
- `docker history miapp` :: Muestra las capas de una imagen y cuánto pesa cada una

📌 Hay dos estilos de comandos: el corto (`docker ps`, `docker rmi`) y el agrupado (`docker container ls`, `docker image rm`). Hacen lo mismo; el agrupado es más claro cuando aprendes.

🇬🇧 **run** /ran/ = ejecutar · **stop** /stop/ = detener · **remove (rm)** /rimúv/ = quitar · **build** /bild/ = construir · **push** /push/ = empujar (subir) · **inspect** /inspékt/ = inspeccionar

## 🚀 docker run a fondo

`docker run` es el comando más importante y el que más opciones tiene. Su forma general es:

```bash
docker run [OPCIONES] IMAGEN [COMANDO] [ARGUMENTOS]
```

Si la imagen no está en tu PC, la descarga sola. Cada `docker run` crea un contenedor **nuevo**; para reusar uno detenido se usa `docker start`.

| Opción | Para qué sirve | Ejemplo |
|---|---|---|
| `-d` | Modo "detached": corre en segundo plano | `docker run -d nginx` |
| `-p HOST:CONT` | Publica un puerto: el del host apunta al del contenedor | `-p 8080:80` |
| `-v ORIGEN:DESTINO` | Monta un volumen o carpeta | `-v $PWD:/app` |
| `-e CLAVE=valor` | Define una variable de entorno | `-e DEBUG=1` |
| `--env-file .env` | Carga variables desde un archivo | `--env-file .env` |
| `--name NOMBRE` | Nombre fijo (si no, Docker inventa uno) | `--name web` |
| `--rm` | Borra el contenedor al terminar | `--rm` |
| `-it` | Interactivo + terminal (para shells) | `-it ubuntu bash` |
| `-w RUTA` | Directorio de trabajo dentro | `-w /app` |
| `--network RED` | Conecta a una red concreta | `--network mired` |
| `--restart POLÍTICA` | Reinicio automático | `--restart unless-stopped` |
| `-m 512m` / `--cpus 1.5` | Límite de RAM / CPU | `-m 512m --cpus 1` |
| `-u UID:GID` | Ejecutar como otro usuario | `-u 1000:1000` |
| `--gpus all` | Dar acceso a la GPU NVIDIA | `--gpus all` |

### 🔌 Los puertos explicados

Un contenedor tiene su propia red. Si tu app escucha en el puerto 80 **dentro** del contenedor, desde tu navegador no la ves hasta que publicas el puerto. Con `-p 8080:80` dices: "lo que llegue al puerto 8080 de mi laptop, mándalo al 80 del contenedor". Truco para recordarlo: **afuera:adentro** (host primero).

```bash
# Servidor web nginx en http://localhost:8080
docker run -d --name web -p 8080:80 nginx:1.27

# Ubuntu interactivo y desechable: al salir (exit) se borra
docker run --rm -it ubuntu:24.04 bash

# Python rápido sin instalar nada
docker run --rm -it python:3.12-slim python

# Ejecutar un script de tu carpeta actual dentro de un contenedor
docker run --rm -v "$PWD":/app -w /app python:3.12-slim python hola.py

# Postgres con contraseña, datos persistentes y nombre fijo
docker run -d --name db \
  -e POSTGRES_PASSWORD=secreto \
  -e POSTGRES_DB=tienda \
  -v pgdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:16
```

### ✅ Ejemplo resuelto: un servidor web con tu propia página

Queremos servir un `index.html` que está en la carpeta actual, sin instalar ningún servidor.

```bash
mkdir -p ~/pruebas/web && cd ~/pruebas/web
echo "<h1>Hola desde Docker</h1>" > index.html

docker run -d --rm --name mi-web \
  -p 8080:80 \
  -v "$PWD":/usr/share/nginx/html:ro \
  nginx:1.27

curl http://localhost:8080
docker stop mi-web
```

Qué hace cada parte: `-d` lo deja en segundo plano; `--rm` lo borra al detenerlo; `--name mi-web` permite referirse a él por nombre; `-p 8080:80` publica el puerto 80 de nginx en el 8080 de tu laptop; `-v "$PWD":/usr/share/nginx/html:ro` monta tu carpeta donde nginx busca las páginas, en solo lectura (`:ro`); `nginx:1.27` es la imagen.

Salida esperada de `curl`: `<h1>Hola desde Docker</h1>`. Si editas `index.html` y recargas, ves el cambio al instante porque la carpeta está montada, no copiada.

⚠️ Cuidado: el orden importa. Las opciones van **antes** del nombre de la imagen; todo lo que va **después** se le pasa al contenedor como comando. `docker run nginx -p 8080:80` está mal.

⚠️ Cuidado: "port is already allocated" significa que otro programa (o contenedor) ya usa ese puerto del host. Cambia el de la izquierda: `-p 8081:80`.

💡 Consejo: si la app dentro del contenedor escucha en `127.0.0.1`, no se verá desde afuera. Haz que escuche en `0.0.0.0` (todas las interfaces). Es el error número uno con Flask y FastAPI.

🇬🇧 **detached** /ditácht/ = desacoplado (en segundo plano) · **port** /port/ = puerto · **publish** /páblish/ = publicar · **interactive** /interáktiv/ = interactivo · **mount** /máunt/ = montar

## 📝 Dockerfile instrucción por instrucción

Un **Dockerfile** es la receta para construir una imagen: un archivo de texto (se llama exactamente `Dockerfile`, sin extensión) con instrucciones que se ejecutan de arriba abajo. Cada instrucción crea una **capa**.

| Instrucción | Qué hace | Ejemplo |
|---|---|---|
| `FROM` | Imagen base de la que partes (siempre la primera) | `FROM python:3.12-slim` |
| `WORKDIR` | Carpeta de trabajo (la crea si no existe) | `WORKDIR /app` |
| `COPY` | Copia archivos del proyecto a la imagen | `COPY . .` |
| `ADD` | Como COPY pero además descomprime .tar y baja URLs | `ADD datos.tar.gz /datos` |
| `RUN` | Ejecuta un comando **al construir** | `RUN pip install -r requirements.txt` |
| `ENV` | Variable de entorno fija | `ENV PYTHONUNBUFFERED=1` |
| `ARG` | Variable solo durante el build | `ARG VERSION=1.0` |
| `EXPOSE` | Documenta en qué puerto escucha (no lo publica) | `EXPOSE 8000` |
| `CMD` | Comando por defecto **al arrancar** (se puede sobrescribir) | `CMD ["python", "app.py"]` |
| `ENTRYPOINT` | Programa fijo; CMD pasa a ser sus argumentos | `ENTRYPOINT ["python"]` |
| `USER` | Usuario con el que corren las siguientes instrucciones | `USER app` |
| `VOLUME` | Marca una carpeta como volumen | `VOLUME /data` |
| `HEALTHCHECK` | Comando para saber si la app está sana | `HEALTHCHECK CMD curl -f localhost:8000` |
| `LABEL` | Metadatos (autor, versión) | `LABEL maintainer="yafer"` |

### 🔁 RUN vs CMD vs ENTRYPOINT

Esta confusión es muy común:

- `RUN` se ejecuta **una vez, al construir** la imagen (instalar paquetes). Su resultado queda guardado en la imagen.
- `CMD` se ejecuta **cada vez que arranca** un contenedor. Si haces `docker run imagen otro-comando`, CMD se reemplaza.
- `ENTRYPOINT` también se ejecuta al arrancar, pero no se reemplaza fácilmente: lo que pongas tras la imagen se le pasa como argumento.

```dockerfile
# Con ENTRYPOINT + CMD la imagen se comporta como un programa
FROM python:3.12-slim
ENTRYPOINT ["python", "-m", "http.server"]
CMD ["8000"]
# docker run img        -> python -m http.server 8000
# docker run img 9000   -> python -m http.server 9000
```

📌 Usa la **forma JSON** (`CMD ["python", "app.py"]`) en vez de la forma shell (`CMD python app.py`). Con la forma JSON tu programa recibe bien las señales de `docker stop` y se apaga limpio.

⚠️ Cuidado: `EXPOSE 8000` NO abre el puerto. Es solo documentación. Para acceder desde afuera sigues necesitando `-p 8000:8000`.

⚠️ Cuidado: dentro de JSON van comillas **dobles**. `CMD ['python', 'app.py']` con comillas simples falla de forma rara.

🇬🇧 **instruction** /instrákshon/ = instrucción · **layer** /léier/ = capa · **entrypoint** /éntri-póint/ = punto de entrada · **expose** /ikspóus/ = exponer · **working directory** /uórking dairéktori/ = carpeta de trabajo

## 🧪 Ejemplos: apps Python y Node

Tres Dockerfiles reales que puedes copiar y adaptar: FastAPI, Flask y Express. Fíjate en que todos siguen el mismo patrón: base, carpeta, dependencias, código, usuario, puerto, comando.

### ✅ Ejemplo resuelto: API con FastAPI

Estructura del proyecto:

```text
mi-api/
├── app/
│   └── main.py
├── requirements.txt
├── .dockerignore
└── Dockerfile
```

Archivo `app/main.py`:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def inicio():
    return {"mensaje": "Hola desde un contenedor", "pais": "Bolivia"}

@app.get("/suma/{a}/{b}")
def suma(a: int, b: int):
    return {"resultado": a + b}
```

Archivo `requirements.txt`:

```text
fastapi==0.115.0
uvicorn[standard]==0.30.6
```

Archivo `Dockerfile`:

```dockerfile
# 1. Imagen base pequeña con Python 3.12
FROM python:3.12-slim

# 2. Variables útiles para Python en contenedores
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3. Carpeta de trabajo
WORKDIR /app

# 4. Primero SOLO las dependencias (aprovecha la caché)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Luego el código (cambia seguido)
COPY app/ ./app/

# 6. Usuario sin privilegios
RUN useradd --create-home appuser
USER appuser

# 7. Documentar el puerto y arrancar
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Construir y ejecutar:

```bash
cd mi-api
docker build -t mi-api:1.0 .
docker run -d --name api -p 8000:8000 mi-api:1.0
curl http://localhost:8000/
curl http://localhost:8000/suma/2/3
```

Qué hace cada parte: `PYTHONDONTWRITEBYTECODE=1` evita archivos `.pyc` inútiles; `PYTHONUNBUFFERED=1` hace que los `print` salgan al instante en `docker logs`; copiar `requirements.txt` antes que el código hace que `pip install` solo se repita cuando cambian las dependencias; `--no-cache-dir` no guarda la caché de pip (imagen más pequeña); `--host 0.0.0.0` es imprescindible para que se vea desde fuera del contenedor. El `.` final de `docker build` es el **contexto**: la carpeta que se envía a Docker.

Salida esperada:

```text
{"mensaje":"Hola desde un contenedor","pais":"Bolivia"}
{"resultado":5}
```

💡 Consejo: con FastAPI abre `http://localhost:8000/docs` y tendrás la documentación interactiva (Swagger) gratis.

### ✅ Ejemplo resuelto: app Flask con gunicorn

Archivo `app.py`:

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def inicio():
    return jsonify(estado="ok", mensaje="Flask en Docker")
```

Archivo `Dockerfile`:

```dockerfile
FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
# gunicorn: servidor de producción (flask run es solo para desarrollo)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
```

Con `requirements.txt` conteniendo `flask==3.0.3` y `gunicorn==23.0.0`, ejecutas `docker build -t mi-flask .` y `docker run --rm -p 5000:5000 mi-flask`. Salida esperada en `curl localhost:5000`: `{"estado":"ok","mensaje":"Flask en Docker"}`. El `app:app` significa "del módulo `app.py`, el objeto `app`".

⚠️ Cuidado: `flask run` sin `--host=0.0.0.0` escucha solo en `127.0.0.1` del contenedor y verás "connection reset" desde el navegador.

🇬🇧 **requirements** /rikuáirments/ = requisitos · **build context** /bild kóntekst/ = contexto de construcción · **unbuffered** /anbáferd/ = sin búfer · **worker** /uórker/ = trabajador (proceso)

### ✅ Ejemplo resuelto: API Express

Archivo `server.js`:

```js
const express = require("express");
const app = express();
const PORT = process.env.PORT || 3000;

app.get("/", (req, res) => {
  res.json({ mensaje: "Hola desde Express en Docker" });
});

app.listen(PORT, "0.0.0.0", () => {
  console.log(`Escuchando en el puerto ${PORT}`);
});
```

Archivo `package.json` (lo mínimo):

```json
{
  "name": "mi-express",
  "version": "1.0.0",
  "main": "server.js",
  "scripts": { "start": "node server.js" },
  "dependencies": { "express": "^4.19.2" }
}
```

Archivo `Dockerfile`:

```dockerfile
FROM node:20-alpine
WORKDIR /app

# Dependencias primero (caché)
COPY package*.json ./
RUN npm ci --omit=dev

# Código
COPY . .

ENV NODE_ENV=production PORT=3000
EXPOSE 3000
# La imagen node ya trae un usuario "node" sin privilegios
USER node
CMD ["node", "server.js"]
```

```bash
npm install          # genera package-lock.json (necesario para npm ci)
docker build -t mi-express .
docker run --rm -p 3000:3000 mi-express
```

Qué hace cada parte: `package*.json` copia `package.json` y `package-lock.json`; `npm ci` instala exactamente lo del lock (reproducible) y `--omit=dev` salta las dependencias de desarrollo; `USER node` evita correr como root. Salida esperada en los logs: `Escuchando en el puerto 3000`; y en `curl localhost:3000`: `{"mensaje":"Hola desde Express en Docker"}`.

⚠️ Cuidado: nunca copies tu carpeta `node_modules` local a la imagen: puede tener binarios compilados para tu sistema. Ponla en `.dockerignore`.

💡 Consejo: usa `CMD ["node", "server.js"]` en vez de `CMD ["npm", "start"]`: npm no reenvía bien las señales y el contenedor tarda 10 s en detenerse.

🇬🇧 **lockfile** /lók-fáil/ = archivo de versiones fijadas · **dependency** /dipéndensi/ = dependencia · **production** /prodákshon/ = producción · **listen** /lísen/ = escuchar

### 🙈 .dockerignore

Cuando haces `docker build .`, Docker envía **toda** la carpeta (el contexto) al daemon. El archivo `.dockerignore` funciona como `.gitignore`: dice qué NO enviar. Así el build es más rápido, la imagen más pequeña y no se cuelan secretos.

```text
# .dockerignore
.git
.gitignore
__pycache__/
*.pyc
.venv/
venv/
node_modules/
.env
*.log
.pytest_cache/
.mypy_cache/
dist/
build/
Dockerfile
docker-compose.yml
README.md
datos_grandes/
```

- `.env` :: Excluir SIEMPRE: tiene contraseñas y claves de API
- `node_modules/` :: Se reinstala dentro con npm ci
- `.venv/` :: El entorno virtual local no sirve dentro del contenedor
- `!importante.txt` :: El `!` vuelve a incluir algo que una regla anterior excluyó

⚠️ Cuidado: si ves "Sending build context to Docker daemon 2.3GB", te falta un `.dockerignore` (probablemente estás enviando datasets o `node_modules`).

💡 Consejo: con `COPY . .` y un buen `.dockerignore` tienes un Dockerfile corto y seguro a la vez.

🇬🇧 **ignore** /ignór/ = ignorar · **context** /kóntekst/ = contexto · **secret** /síkret/ = secreto · **leak** /lík/ = filtrar (fuga de datos)

## 🧱 Capas y caché

Cada instrucción del Dockerfile (`RUN`, `COPY`, `ADD`...) crea una **capa**: una "foto" de los cambios en el sistema de archivos. La imagen es una pila de capas. Docker guarda cada capa en caché y, al reconstruir, **reutiliza** las que no cambiaron.

La regla de oro: **cuando una capa cambia, todas las de debajo se reconstruyen**. Por eso el orden importa: lo que cambia poco va arriba y lo que cambia mucho (tu código) va abajo.

Analogía: es como una torre de panqueques. Si quieres cambiar el tercero, tienes que quitar y volver a poner todos los que están encima.

### ❌ Orden malo vs ✅ orden bueno

```dockerfile
# ❌ MALO: cualquier cambio en el código invalida la caché del pip install
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```

```dockerfile
# ✅ BUENO: pip install solo se repite si cambia requirements.txt
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

Con el orden bueno, cambiar una línea de `main.py` reconstruye en 1 segundo en vez de 2 minutos. En la salida de `docker build` verás `CACHED` en los pasos reutilizados.

### 🧹 Unir RUN para capas limpias

```dockerfile
# Instalar paquetes del sistema y limpiar en LA MISMA capa
RUN apt-get update \
 && apt-get install -y --no-install-recommends gcc libpq-dev \
 && rm -rf /var/lib/apt/lists/*
```

Si borras archivos en un `RUN` posterior, la capa anterior ya los guardó y la imagen sigue pesando lo mismo. Por eso se limpia en la misma línea con `&&`.

- `docker build --no-cache -t app .` :: Reconstruye todo ignorando la caché
- `docker history app` :: Ver qué capa pesa más
- `docker build --progress=plain .` :: Salida completa de cada paso (útil para depurar)

⚠️ Cuidado: `apt-get update` en una capa y `apt-get install` en otra provoca que la caché use listas de paquetes viejas. Siempre juntos.

🇬🇧 **cache** /kash/ = caché · **layer** /léier/ = capa · **invalidate** /inválideit/ = invalidar · **rebuild** /ribíld/ = reconstruir · **stack** /stak/ = pila

## 💾 Volúmenes y bind mounts

Los contenedores son **efímeros**: si borras el contenedor, se pierde todo lo que escribió dentro. Para guardar datos (una base de datos, subidas de usuarios, modelos entrenados) se usan montajes:

| Tipo | Sintaxis | Dónde vive | Para qué |
|---|---|---|---|
| **Volumen** | `-v pgdata:/var/lib/postgresql/data` | Lo gestiona Docker (`/var/lib/docker/volumes`) | Datos de bases de datos, producción |
| **Bind mount** | `-v "$PWD":/app` | Una carpeta tuya concreta | Desarrollo: editar código y verlo al instante |
| **tmpfs** | `--tmpfs /tmp` | En RAM, se borra al parar | Archivos temporales rápidos |

Cómo distinguirlos: si lo de la izquierda es una **ruta** (empieza por `/` o `./`), es bind mount; si es un **nombre**, es un volumen.

- `docker volume create misdatos` :: Crea un volumen con nombre
- `docker volume ls` :: Lista volúmenes
- `docker volume inspect misdatos` :: Ver dónde está en disco
- `docker volume rm misdatos` :: Borra un volumen (¡y sus datos!)
- `-v "$PWD":/app:ro` :: Bind mount en solo lectura
- `--mount type=bind,src="$PWD",dst=/app` :: Sintaxis larga, más explícita

### ✅ Ejemplo resuelto: los datos sobreviven al contenedor

```bash
# 1. Crear un contenedor que escribe en un volumen
docker run --rm -v notas:/datos alpine sh -c 'echo "hola volumen" > /datos/nota.txt'

# 2. El contenedor ya no existe (--rm). Leemos con OTRO contenedor
docker run --rm -v notas:/datos alpine cat /datos/nota.txt

# 3. Limpiar
docker volume rm notas
```

Qué hace cada parte: el primer contenedor monta el volumen `notas` en `/datos`, escribe un archivo y se borra; el segundo, totalmente nuevo, monta el mismo volumen y lee el archivo. Salida esperada del paso 2: `hola volumen`.

⚠️ Cuidado: con bind mounts los archivos creados dentro como root aparecen en tu carpeta con dueño root. Usa `-u $(id -u):$(id -g)` (en fish: `-u (id -u):(id -g)`) para crearlos con tu usuario.

⚠️ Cuidado: montar una carpeta encima de otra **la tapa**. Si montas `-v "$PWD":/app` y la imagen tenía `node_modules` dentro de `/app`, desaparecen. Solución típica: añadir `-v /app/node_modules`.

🇬🇧 **volume** /vóliumm/ = volumen · **bind mount** /báind máunt/ = montaje enlazado · **persistent** /persístent/ = persistente · **ephemeral** /ifémeral/ = efímero

## 🌐 Redes

Cada contenedor tiene su IP interna. Para que dos contenedores se hablen (tu API y su base de datos) lo mejor es ponerlos en la misma **red definida por el usuario**: ahí Docker trae un **DNS interno** y cada contenedor se encuentra por su **nombre**.

| Driver | Qué es | Cuándo usarlo |
|---|---|---|
| `bridge` (por defecto) | Red privada en tu host | Lo normal para apps en una máquina |
| red bridge propia | Igual pero con DNS por nombre | Siempre que conectes contenedores |
| `host` | El contenedor usa la red del host directamente | Rendimiento máximo, sin aislamiento de red |
| `none` | Sin red | Tareas aisladas por seguridad |
| `overlay` | Red entre varias máquinas | Docker Swarm / clústeres |

- `docker network create mired` :: Crea una red bridge propia
- `docker network ls` :: Lista redes
- `docker network inspect mired` :: Ver qué contenedores están conectados y sus IPs
- `docker network connect mired api` :: Conecta un contenedor existente a una red
- `docker run --network mired --name db postgres:16` :: Arranca directamente en esa red

### ✅ Ejemplo resuelto: dos contenedores que se encuentran por nombre

```bash
docker network create labred
docker run -d --name servidor --network labred nginx:1.27
docker run --rm --network labred alpine wget -qO- http://servidor
docker rm -f servidor && docker network rm labred
```

Qué hace cada parte: creamos la red `labred`; arrancamos nginx con el nombre `servidor`; un segundo contenedor en la misma red pide `http://servidor` y el DNS de Docker traduce ese nombre a la IP de nginx. Salida esperada: el HTML de bienvenida de nginx (`<title>Welcome to nginx!</title>`...).

📌 Dentro de un contenedor, `localhost` es **el propio contenedor**, no tu laptop. Para hablar con otro contenedor usa su nombre; para hablar con tu laptop usa `host.docker.internal` (añade `--add-host=host.docker.internal:host-gateway` en Linux).

⚠️ Cuidado: en la red `bridge` por defecto los nombres NO se resuelven. Crea siempre una red propia (compose lo hace solo).

🇬🇧 **network** /nét-uork/ = red · **bridge** /brich/ = puente · **resolve** /risólv/ = resolver (traducir un nombre) · **hostname** /jóust-néim/ = nombre del equipo

## 🔐 Variables de entorno

Las **variables de entorno** son la forma estándar de configurar un contenedor sin cambiar la imagen: la misma imagen sirve para desarrollo y producción, solo cambian las variables (URL de la base, claves, modo debug). Es la idea de "The Twelve-Factor App": la configuración vive fuera del código.

```bash
# Una a una
docker run -e DEBUG=1 -e DB_HOST=db miapp

# Pasar una variable que ya existe en tu terminal (sin escribir el valor)
docker run -e API_KEY miapp

# Desde un archivo
docker run --env-file .env miapp
```

```text
# .env  (¡nunca a git ni a la imagen!)
DB_HOST=db
DB_USER=postgres
DB_PASSWORD=supersecreto
DEBUG=0
```

```python
# Leerlas en Python
import os

db_host = os.environ.get("DB_HOST", "localhost")   # con valor por defecto
debug = os.getenv("DEBUG", "0") == "1"
clave = os.environ["API_KEY"]                       # falla si no existe (bien para obligatorias)
```

- `ENV PUERTO=8000` :: En el Dockerfile: valor por defecto incluido en la imagen
- `ARG VERSION` :: Solo existe durante `docker build --build-arg VERSION=2`
- `docker exec api env` :: Ver las variables dentro de un contenedor vivo

⚠️ Cuidado: no pongas contraseñas en `ENV` ni en `ARG` del Dockerfile: quedan grabadas en la imagen y cualquiera las ve con `docker history`. Pásalas al ejecutar o usa secretos de compose.

💡 Consejo: guarda un `.env.example` en git con las claves pero valores falsos, para que tu equipo sepa qué variables hacen falta.

🇬🇧 **environment variable** /enváironment vériabol/ = variable de entorno · **default value** /difólt váliu/ = valor por defecto · **credentials** /kredénshals/ = credenciales · **config** /kónfig/ = configuración

## 🎼 Docker Compose

Cuando tu proyecto tiene varios contenedores (API + base de datos + panel), escribir `docker run` largos para cada uno es un infierno. **Docker Compose** te deja describirlos todos en un archivo `compose.yaml` (o `docker-compose.yml`) y levantarlos con un solo comando. Compose crea automáticamente una red donde cada **servicio** se encuentra por su nombre.

Analogía: si `docker run` es tocar un instrumento, Compose es la **partitura de la orquesta** entera.

| Comando | Qué hace |
|---|---|
| `docker compose up -d` | Crea y arranca todo en segundo plano |
| `docker compose up -d --build` | Igual, reconstruyendo imágenes |
| `docker compose down` | Para y borra contenedores y la red (los volúmenes quedan) |
| `docker compose down -v` | Además borra los volúmenes (¡borra los datos!) |
| `docker compose ps` | Estado de los servicios |
| `docker compose logs -f api` | Logs en vivo de un servicio |
| `docker compose exec db psql -U postgres` | Entrar a un servicio |
| `docker compose restart api` | Reiniciar un servicio |
| `docker compose build` | Solo construir imágenes |
| `docker compose config` | Muestra el archivo final ya interpretado (detecta errores) |

### ✅ Ejemplo resuelto: API + Postgres + Adminer

Estructura:

```text
proyecto/
├── compose.yaml
├── .env
└── api/
    ├── Dockerfile
    ├── requirements.txt
    └── main.py
```

Archivo `compose.yaml`:

```yaml
services:
  db:
    image: postgres:16
    restart: unless-stopped
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: escuela
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER} -d escuela"]
      interval: 5s
      timeout: 3s
      retries: 10

  api:
    build: ./api
    restart: unless-stopped
    environment:
      DATABASE_URL: postgresql://${DB_USER}:${DB_PASSWORD}@db:5432/escuela
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy

  adminer:
    image: adminer:4
    restart: unless-stopped
    ports:
      - "8080:8080"
    depends_on:
      - db

volumes:
  pgdata:
```

Archivo `.env` (en la misma carpeta; compose lo lee solo):

```text
DB_USER=yafer
DB_PASSWORD=cambia_esto
```

Archivo `api/main.py`:

```python
import os
import psycopg
from fastapi import FastAPI

app = FastAPI()
URL = os.environ["DATABASE_URL"]

@app.get("/")
def inicio():
    with psycopg.connect(URL) as conn:
        version = conn.execute("SELECT version()").fetchone()[0]
    return {"postgres": version}
```

El `api/Dockerfile` es el de FastAPI de la sección anterior (con `CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]`) y `requirements.txt` lleva `fastapi`, `uvicorn` y `psycopg[binary]`.

```bash
docker compose up -d --build
docker compose ps
curl http://localhost:8000/
# Adminer: http://localhost:8080  (Sistema: PostgreSQL, Servidor: db, Usuario/clave del .env)
docker compose down
```

Qué hace cada parte: `services` define tres contenedores; `db` usa la imagen oficial de Postgres y guarda sus datos en el volumen `pgdata`; `${DB_USER}` se reemplaza con el valor del `.env`; el `healthcheck` pregunta a Postgres si ya acepta conexiones; `api` se construye desde la carpeta `./api` y se conecta a la base usando el **nombre del servicio** `db` como host; `depends_on` con `service_healthy` espera a que Postgres esté listo de verdad; `adminer` es un panel web para ver las tablas; el bloque `volumes:` final declara el volumen con nombre.

Salida esperada de `docker compose ps`: los tres servicios con estado `running` (y `db` como `healthy`). En `curl`: `{"postgres":"PostgreSQL 16.x on x86_64-pc-linux-gnu..."}`.

⚠️ Cuidado: en YAML la **indentación** es la sintaxis. Usa espacios (nunca tabs) y sé consistente (2 espacios). Un espacio de más y compose dice "additional properties not allowed".

⚠️ Cuidado: `depends_on` sin `condition: service_healthy` solo espera a que el contenedor **arranque**, no a que Postgres esté listo; tu API puede fallar al conectar las primeras veces.

💡 Consejo: para desarrollo añade a `api` un bind mount `- ./api:/app` y en el comando `--reload` de uvicorn: editas el código y el servidor se recarga solo.

🇬🇧 **service** /sérvis/ = servicio · **depends on** /dipénds on/ = depende de · **healthcheck** /jélz-chek/ = chequeo de salud · **orchestrate** /órkestreit/ = orquestar · **up / down** /ap / dáun/ = levantar / bajar

## 🔍 Logs y depuración

Cuando algo falla (y fallará), estas son tus herramientas. El orden lógico: ¿está corriendo? (`ps`) → ¿qué dijo? (`logs`) → ¿qué hay dentro? (`exec`) → ¿cómo está configurado? (`inspect`).

- `docker ps -a` :: ¿Está vivo? Mira la columna STATUS: `Exited (1)` = terminó con error
- `docker logs api` :: Todo lo que la app imprimió (stdout y stderr)
- `docker logs -f --tail 50 api` :: Seguir en vivo, empezando por las últimas 50 líneas
- `docker logs --since 10m api` :: Solo los últimos 10 minutos
- `docker exec -it api bash` :: Abrir una terminal dentro (en alpine usa `sh`)
- `docker exec api ls -la /app` :: Ejecutar un comando suelto dentro
- `docker exec -u root -it api sh` :: Entrar como root aunque la imagen use otro usuario
- `docker inspect api` :: Todo: IP, volúmenes, variables, comando, estado
- `docker inspect -f '{{.State.ExitCode}}' api` :: Extraer un dato concreto con plantilla Go
- `docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' api` :: La IP del contenedor
- `docker stats --no-stream` :: CPU, RAM y red de cada contenedor
- `docker top api` :: Procesos dentro del contenedor
- `docker events` :: Eventos en vivo (arranques, muertes, OOM)
- `docker run --rm -it --entrypoint sh miapp` :: Entrar a una imagen cuyo CMD falla al arrancar

### ✅ Ejemplo resuelto: el contenedor se apaga solo

Síntoma: haces `docker run -d --name api miapp` y en `docker ps` no aparece.

```bash
docker ps -a --filter name=api
# STATUS: Exited (1) 3 seconds ago

docker logs api
# ModuleNotFoundError: No module named 'fastapi'

docker run --rm -it --entrypoint sh miapp
# dentro:  pip list | grep -i fastapi   -> no sale nada
```

Diagnóstico: el contenedor arrancó, Python falló al importar y como el proceso principal murió, el contenedor se detuvo. La causa: `requirements.txt` no tenía `fastapi` o el `COPY` del archivo estaba mal. Arreglas, `docker build` de nuevo y listo.

📌 Un contenedor vive **mientras viva su proceso principal** (PID 1). Si tu `CMD` termina (o falla), el contenedor se detiene. Por eso `docker run ubuntu` termina al instante: no hay nada que hacer.

| Código de salida | Significado habitual |
|---|---|
| `0` | Terminó bien (pero terminó: ¿tu CMD no es un servidor?) |
| `1` | Error de la aplicación (mira los logs) |
| `126` | El comando no se puede ejecutar (permisos) |
| `127` | Comando no encontrado (typo en CMD o falta instalarlo) |
| `137` | Matado con SIGKILL: casi siempre falta de memoria (OOM) |
| `143` | Detenido con SIGTERM (`docker stop` normal) |

🇬🇧 **logs** /logs/ = registros · **debug** /dibág/ = depurar · **exit code** /éksit kóud/ = código de salida · **out of memory** /áut of mémori/ = sin memoria · **tail** /téil/ = cola (últimas líneas)

## 🧹 Limpiar espacio

Docker acumula imágenes viejas, contenedores detenidos y caché de builds. Después de unas semanas puede comerse 30-50 GB sin que te des cuenta.

- `docker system df` :: Cuánto ocupa cada cosa (imágenes, contenedores, volúmenes, caché)
- `docker container prune` :: Borra los contenedores detenidos
- `docker image prune` :: Borra imágenes "colgantes" (sin etiqueta, `<none>`)
- `docker image prune -a` :: Borra TODAS las imágenes que no use ningún contenedor
- `docker volume prune` :: Borra volúmenes sin usar (¡cuidado con datos!)
- `docker builder prune` :: Borra la caché de construcción
- `docker network prune` :: Borra redes sin usar
- `docker system prune` :: Contenedores parados + redes + imágenes colgantes + caché
- `docker system prune -a --volumes` :: Limpieza nuclear: todo lo que no esté en uso
- `docker image prune -a --filter "until=168h"` :: Solo imágenes de hace más de una semana

```bash
docker system df
# TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
# Images          23        4         12.4GB    10.1GB (81%)
# Containers      9         2         150MB     120MB (80%)
# Local Volumes   6         2         2.1GB     1.3GB (61%)
# Build Cache     140       0         5.2GB     5.2GB
```

La columna RECLAIMABLE (recuperable) te dice cuánto ganarías limpiando.

⚠️ Cuidado: `docker volume prune` y `--volumes` borran las bases de datos de los proyectos que no estén corriendo en ese momento. Antes de usarlos, revisa `docker volume ls`.

💡 Consejo: usa `--rm` en todos los contenedores de prueba y nunca acumularás basura.

🇬🇧 **prune** /prun/ = podar · **dangling** /dángling/ = colgante (huérfana) · **reclaimable** /rikléimabol/ = recuperable · **disk space** /disk spéis/ = espacio en disco

## 🏗️ Multi-stage builds

Para compilar o instalar dependencias necesitas herramientas pesadas (compiladores, npm, cabeceras de C) que **no** necesitas para ejecutar. Un **multi-stage build** usa varias etapas `FROM` en un mismo Dockerfile: la primera construye, la última solo copia el resultado. La imagen final es la de la última etapa.

Analogía: cocinas en la cocina (con ollas, cuchillos, harina por todos lados) pero al comedor solo llevas el plato servido.

### ✅ Ejemplo resuelto: frontend con Node servido por nginx

```dockerfile
# ---- Etapa 1: construir ----
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build          # genera /app/dist

# ---- Etapa 2: servir ----
FROM nginx:1.27-alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
```

Qué hace cada parte: `AS build` le da nombre a la etapa; ahí se instalan las dependencias y se compila; `COPY --from=build` copia solo la carpeta `dist` a una imagen nginx limpia. Resultado esperado: la imagen final pesa unos 50 MB en vez de más de 500 MB, y no contiene ni Node ni `node_modules` ni tu código fuente.

### ✅ Ejemplo resuelto: Python con dependencias compiladas

```dockerfile
# ---- Etapa 1: crear un venv con todo instalado ----
FROM python:3.12-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends gcc \
 && rm -rf /var/lib/apt/lists/*
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Etapa 2: imagen final sin gcc ----
FROM python:3.12-slim
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH" PYTHONUNBUFFERED=1
WORKDIR /app
COPY . .
RUN useradd -m app
USER app
CMD ["python", "main.py"]
```

El truco es instalar todo en un **entorno virtual** (`/opt/venv`) y copiar esa carpeta entera a la imagen final; `gcc` se queda en la etapa 1.

- `docker build --target build -t app:dev .` :: Construir solo hasta una etapa concreta
- `FROM gcr.io/distroless/python3` :: Imágenes "distroless": sin shell ni gestor de paquetes, mínimas

💡 Consejo: para Go o Rust el resultado es espectacular: compilas en una imagen de 1 GB y la final es `FROM scratch` (vacía) con solo el binario, menos de 20 MB.

🇬🇧 **stage** /stéich/ = etapa · **builder** /bílder/ = constructor · **artifact** /ártifakt/ = artefacto (resultado del build) · **footprint** /fút-print/ = huella (tamaño)

## ☁️ Subir a Docker Hub

**Docker Hub** es el "GitHub de las imágenes": un registro público donde están las imágenes oficiales (`python`, `postgres`...) y donde puedes subir las tuyas. Alternativas: GitHub Container Registry (`ghcr.io`), GitLab, AWS ECR.

### ✅ Ejemplo resuelto: publicar tu imagen

```bash
# 1. Iniciar sesión (usa un Access Token, no tu contraseña)
docker login -u yafer

# 2. Construir con el nombre usuario/repositorio:versión
docker build -t yafer/mi-api:1.0 .

# 3. Añadir también la etiqueta latest (misma imagen, otro nombre)
docker tag yafer/mi-api:1.0 yafer/mi-api:latest

# 4. Subir ambas etiquetas
docker push yafer/mi-api:1.0
docker push yafer/mi-api:latest

# 5. En cualquier otra máquina:
docker run -d -p 8000:8000 yafer/mi-api:1.0
```

Qué hace cada parte: `login` guarda tus credenciales en `~/.docker/config.json`; el nombre debe empezar por tu usuario o el push falla con "denied: requested access to the resource is denied"; `tag` crea un alias sin copiar nada; `push` sube solo las capas que el registro no tiene. Salida esperada del push: una lista de capas con `Pushed` (o `Layer already exists`) y al final un `digest: sha256:...`.

- `docker tag origen destino` :: Ponerle otro nombre a una imagen local
- `docker logout` :: Cerrar sesión
- `docker buildx build --platform linux/amd64,linux/arm64 -t yafer/app:1.0 --push .` :: Imagen para PC y para ARM (Raspberry, Mac M) a la vez
- `docker login ghcr.io -u usuario` :: Iniciar sesión en GitHub Container Registry

⚠️ Cuidado: los repositorios de Docker Hub son **públicos** por defecto. Revisa que tu imagen no tenga `.env`, claves ni datos privados antes de hacer push.

🇬🇧 **push** /push/ = subir · **repository** /ripósitori/ = repositorio · **access token** /ákses tóuken/ = token de acceso · **digest** /dáiyest/ = huella (hash) · **public / private** /páblik / práivet/ = público / privado

## 🛡️ Buenas prácticas y seguridad

| Práctica | Por qué |
|---|---|
| Fijar versiones: `python:3.12.7-slim` | Builds reproducibles; nada se rompe solo |
| Imágenes base pequeñas (`slim`, `alpine`, distroless) | Menos tamaño y menos vulnerabilidades |
| Un proceso por contenedor | Más fácil de escalar, reiniciar y depurar |
| `USER` sin privilegios | Si atacan tu app, no son root |
| `.dockerignore` siempre | Sin secretos ni basura en la imagen |
| Dependencias antes que el código | Caché efectiva, builds rápidos |
| Multi-stage para compilar | Imagen final mínima |
| Secretos por variables o secrets, nunca en la imagen | `docker history` lo revela todo |
| `HEALTHCHECK` | Docker y compose saben si tu app responde |
| Logs a stdout/stderr | `docker logs` los recoge; no escribas a archivos |
| Escanear vulnerabilidades | `docker scout cves miapp` o `trivy image miapp` |
| Limitar recursos (`-m`, `--cpus`) | Un fallo no se come toda la máquina |

```dockerfile
# Plantilla "buena" para Python
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
RUN useradd --create-home --uid 1000 app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=app:app . .
USER app
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/')"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

- `docker run --read-only --tmpfs /tmp miapp` :: Sistema de archivos de solo lectura (más seguro)
- `docker run --cap-drop ALL miapp` :: Quita todos los permisos especiales del kernel
- `docker run --security-opt no-new-privileges miapp` :: Impide escalar privilegios con sudo/setuid
- `docker scout quickview miapp` :: Resumen de vulnerabilidades de la imagen

⚠️ Cuidado: nunca montes el socket `-v /var/run/docker.sock:/var/run/docker.sock` en un contenedor que no sea de total confianza: le das control total de tu máquina.

💡 Consejo: también existe **Podman**, compatible con los mismos comandos (`alias docker=podman`) y que corre sin daemon ni root por defecto. Útil si te piden más seguridad.

🇬🇧 **best practices** /best práktises/ = buenas prácticas · **vulnerability** /valnerabíliti/ = vulnerabilidad · **least privilege** /líst prívilech/ = mínimo privilegio · **hardening** /járdening/ = endurecimiento (hacer más seguro)

## 🚨 Errores frecuentes

| Error / síntoma | Causa | Solución |
|---|---|---|
| `permission denied ... docker.sock` | No estás en el grupo docker o no cerraste sesión | `sudo usermod -aG docker $USER` y volver a entrar |
| `Cannot connect to the Docker daemon` | El servicio no corre | `sudo systemctl start docker` |
| `port is already allocated` | Puerto del host ocupado | Cambia `-p 8081:80` o para el otro contenedor |
| `Conflict. The container name "/web" is already in use` | Ya existe un contenedor con ese nombre (aunque esté parado) | `docker rm web` o usa `--rm` |
| La página no carga pero el contenedor corre | La app escucha en 127.0.0.1 | Haz que escuche en `0.0.0.0` |
| `exec format error` | Imagen de otra arquitectura (ARM vs x86) | Construye con `--platform linux/amd64` |
| `no space left on device` | Docker llenó el disco | `docker system prune -a` |
| El contenedor sale con `Exited (0)` al instante | El CMD no es un proceso que se quede corriendo | Usa un servidor o `-it` con una shell |
| `Exited (137)` | Sin memoria (OOM) | Más RAM con `-m` o reduce el consumo |
| Los cambios en el código no se ven | La imagen tiene la copia vieja | `docker compose up -d --build` o usa bind mount |
| `ModuleNotFoundError` dentro | Falta en requirements o COPY mal | Revisa el Dockerfile y reconstruye |
| `could not translate host name "db"` | Contenedores en redes distintas o nombre mal escrito | Misma red / mismo compose, nombre del servicio |
| `connection refused` a la base al arrancar | La base todavía no estaba lista | `depends_on` con `condition: service_healthy` |
| `denied: requested access to the resource is denied` | Push sin login o nombre sin tu usuario | `docker login` y `docker tag` a `usuario/repo` |

### 🧭 Rutina de diagnóstico en 5 pasos

1) `docker ps -a` para ver el estado y el código de salida. 2) `docker logs <nombre>` para leer el error real. 3) `docker exec -it <nombre> sh` para mirar archivos y variables dentro. 4) `docker inspect <nombre>` para revisar puertos, volúmenes y red. 5) Si no arranca ni para entrar, `docker run --rm -it --entrypoint sh <imagen>`.

💡 Consejo: copia el mensaje de error exacto en inglés al buscar en internet; casi siempre alguien tuvo el mismo problema en Stack Overflow o en los issues de GitHub.

📌 Resumen del flujo diario: escribes el `Dockerfile` → `docker build -t app .` → `docker run -p ... app` (o `docker compose up -d --build`) → miras `docker logs` → limpias con `docker system prune`.

🇬🇧 **troubleshooting** /trábol-shúting/ = resolución de problemas · **already in use** /olrédi in iús/ = ya en uso · **refused** /rifiúsd/ = rechazado · **"It works on my machine"** /it uórks on mái mashín/ = "en mi máquina funciona"
