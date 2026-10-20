# 🐳 Docker · Contenedores y despliegue
> Empaqueta tu app con todo lo que necesita, córrela igual en cualquier máquina y llévala a producción: Dockerfile, Compose, seguridad, Kubernetes, CI/CD y dónde desplegar.

## 🤔 El problema: "en mi máquina funciona"

Escribes una API en tu laptop con Python 3.12, `psycopg` 3, Postgres 16 y una librería de C que instalaste hace meses con `pacman`. Funciona perfecto. Se la pasas a tu compañero (Windows, Python 3.10) y no arranca. La subes al servidor (Ubuntu con Python 3.9) y falla de otra forma. Nadie mintió: **el código es el mismo, el entorno no**.

El entorno es todo lo que tu programa usa sin que lo veas: versión del intérprete, librerías del sistema (`glibc`, `libssl`), variables de entorno, rutas, zona horaria, otros servicios (base de datos, Redis). Docker resuelve esto empaquetando **la app + su entorno** en una unidad estándar que corre igual en todas partes.

🧠 Concepto: un **contenedor** es un proceso normal de Linux al que el kernel le hace creer que está solo en la máquina (su propio sistema de archivos, su red, sus procesos) y al que le limita los recursos. No es una máquina virtual: es aislamiento.

🧠 Concepto: una **imagen** es el paquete de solo lectura con el sistema de archivos de la app (sistema base + librerías + tu código) y la instrucción de qué ejecutar. De una imagen se crean contenedores.

![Un buque portacontenedores en el puerto de Los Ángeles: a la grúa no le importa qué hay dentro, todos los contenedores tienen el mismo tamaño y se mueven igual. Docker copió esa idea para el software (foto: Wikimedia Commons)](img/docker/buque-contenedores.jpg)

Antes de los contenedores de carga (años 50-60), cada barco se cargaba bulto por bulto: sacos, cajas, barriles, cada uno distinto. El contenedor estándar hizo que da igual si llevas quinua o televisores: se mueve con la misma grúa, el mismo camión y el mismo barco. Docker hace lo mismo: da igual si dentro hay Python, Node, Java o Go; se construye, se mueve y se arranca con los mismos comandos.

```flujo
dir: abajo
Código -> Dockerfile : describes el entorno
Dockerfile -> Imagen : docker build
Imagen -> Laptop : docker run
Imagen -> CI : docker run (tests)
Imagen -> Servidor : docker run (producción)
```

La gran idea: **construyes una vez y ejecutas en todas partes** la misma imagen exacta (mismo hash). Lo que pasó los tests en CI es, byte a byte, lo que corre en producción.

| Sin Docker | Con Docker |
|---|---|
| "Instala Python 3.12, Postgres 16, Redis, libpq..." | `docker compose up` |
| README de 40 pasos que nadie actualiza | El `Dockerfile` ES la documentación |
| Servidor configurado a mano ("servidor mascota") | Imagen reproducible ("ganado": se reemplaza) |
| Dos proyectos con versiones de Node distintas chocan | Cada uno en su contenedor |
| Volver a una versión anterior = rezar | `docker run app:1.4.2` (la imagen vieja sigue ahí) |

### 📜 De dónde sale Docker

Docker no inventó el aislamiento: juntó piezas que el kernel de Linux y otros Unix ya tenían y las hizo **fáciles de usar** con un formato de imagen y un registro para compartirlas.

```tiempo
1979 : chroot en Unix V7 (cambiar la raíz de archivos)
2000 : FreeBSD Jails
2004 : Solaris Zones
2008 : cgroups llegan a Linux 2.6.24 (Google) y nace LXC
2013 : Docker se presenta en PyCon (dotCloud, Solomon Hykes)
2014 : Google anuncia Kubernetes
2015 : OCI: estándar abierto de imágenes y runtimes
2017 : Docker dona containerd a la CNCF
2022 : Kubernetes 1.24 quita dockershim
2026 : contenedores = forma estándar de desplegar
```

📌 Resumen: Docker = **imágenes** (el paquete) + **contenedores** (el paquete corriendo) + **registros** (dónde se guardan y comparten) + herramientas (`build`, `run`, `compose`).

💡 Consejo: en IA y ciencia de datos Docker es oro: congelas la versión exacta de Python, CUDA y librerías, y tu experimento se puede repetir meses después (o en el servidor con GPU de la universidad).

🇬🇧 **container** /kontéiner/ = contenedor · **image** /ímich/ = imagen · **"works on my machine"** /uórks on mái mashín/ = "en mi máquina funciona" · **environment** /enváironment/ = entorno · **reproducible** /ripródiusibol/ = reproducible

## 🆚 Contenedores vs máquinas virtuales

Una **máquina virtual (VM)** emula un computador entero: un **hipervisor** reparte el hardware y cada VM arranca **su propio kernel** y su sistema operativo completo. Un **contenedor** no emula nada: es un proceso que **comparte el kernel** del anfitrión y solo está aislado.

Analogía: una VM es **una casa completa** (cimientos, tuberías y techo propios). Un contenedor es **un departamento en un edificio**: cada uno tiene su llave y sus muebles, pero comparten cimientos y tuberías (el kernel).

::: columnas
### 🖥️ Máquinas virtuales
```capas
App A + App B : cada una en su VM
Libs : librerías de cada VM
SO invitado : un kernel COMPLETO por VM
Hipervisor : KVM, VMware, Hyper-V
SO anfitrión : o hipervisor "bare metal"
Hardware : CPU, RAM, disco
```
::: siguiente
### 🐳 Contenedores
```capas
App A + App B : cada una en su contenedor
Libs : solo lo que la app necesita
Runtime : Docker / containerd / runc
Kernel Linux : UNO, compartido por todos
Hardware : CPU, RAM, disco
```
:::

| Aspecto | Máquina virtual | Contenedor |
|---|---|---|
| Qué virtualiza | El hardware | El sistema operativo (vista de procesos) |
| Kernel | Propio por VM | Compartido con el anfitrión |
| Tamaño típico | Varios GB | De pocos MB a cientos de MB |
| Arranque | Decenas de segundos a minutos | Milisegundos a segundos |
| Aislamiento | Muy fuerte (frontera de hardware) | Fuerte, pero menor (mismo kernel) |
| Densidad | Decenas por servidor | Cientos por servidor |
| Otro SO (Windows en Linux) | Sí | No: un contenedor Linux necesita kernel Linux |
| Ejemplos | VirtualBox, VMware, QEMU/KVM, EC2 | Docker, Podman, containerd |

```grafica
tipo: barras
titulo: Arranque típico hasta que la app responde (ilustrativo, orden de magnitud)
unidad: s
VM con SO completo : 40
Contenedor Python slim : 1.5
Contenedor Go estático : 0.2
```

### 🤝 No compiten: se combinan

En la nube casi siempre corres contenedores **dentro** de VMs: AWS te alquila una VM (EC2) y en ella corren tus contenedores. La VM da el aislamiento fuerte entre clientes; el contenedor da empaquetado y densidad dentro de tu VM.

📌 En Windows y macOS no hay kernel Linux, así que Docker Desktop (y Podman Desktop, OrbStack, Colima) corre una **VM Linux pequeña** y los contenedores van dentro. Por eso en Mac los bind mounts son más lentos que en Linux.

🧠 Concepto: **microVM** (Firecracker de AWS, usado en Lambda y Fargate; Kata Containers; gVisor de Google como "kernel" en espacio de usuario) = soluciones intermedias: arrancan casi tan rápido como un contenedor pero con aislamiento cercano al de una VM. Se usan cuando corres código de desconocidos (serverless, sandboxes de IA).

| Elige... | Cuando... |
|---|---|
| Contenedor | Empaquetar y desplegar tus apps, CI, desarrollo local, microservicios |
| VM | Necesitas otro SO o kernel, aislamiento fuerte entre clientes, software legado |
| MicroVM / gVisor | Ejecutar código no confiable (sandboxes, funciones serverless multi-cliente) |

⚠️ Cuidado: "el contenedor es una frontera de seguridad tan fuerte como una VM" es falso. Un fallo del kernel afecta a todos los contenedores del host. No ejecutes código de desconocidos en contenedores normales con privilegios.

🇬🇧 **virtual machine** /vérchual mashín/ = máquina virtual · **hypervisor** /jáiper-váisor/ = hipervisor · **host** /jóust/ = anfitrión · **guest** /gest/ = invitado · **kernel** /kérnel/ = núcleo del SO · **overhead** /óver-jed/ = coste extra

## ⚙️ Cómo funciona por dentro: namespaces, cgroups y capas

Un contenedor es la suma de tres funciones del kernel Linux. Entenderlas explica casi todos los "comportamientos raros" de Docker.

```capas
Namespaces : QUÉ ve el proceso (aislamiento)
cgroups : CUÁNTO puede usar (límites de CPU, RAM, PIDs)
Sistema de archivos por capas : DE DÓNDE salen sus archivos (OverlayFS)
Extras de seguridad : capabilities, seccomp, AppArmor/SELinux
```

### 👁️ Namespaces: lo que el proceso puede ver

🧠 Concepto: un **namespace** (espacio de nombres) es una "vista privada" de un recurso del sistema. Un proceso dentro de un namespace PID nuevo cree que es el PID 1 y no ve los procesos del anfitrión.

| Namespace | Aísla | Efecto en el contenedor |
|---|---|---|
| `pid` | Números de proceso | Tu app es el PID 1; no ve otros procesos |
| `net` | Interfaces, IPs, puertos | Su propia IP y su propio `localhost` |
| `mnt` | Puntos de montaje | Su propio `/` (el de la imagen) |
| `uts` | Nombre del equipo | Su propio `hostname` |
| `ipc` | Memoria compartida, colas | No interfiere con otros |
| `user` | IDs de usuario | root dentro puede ser un usuario normal fuera |
| `cgroup` | Vista de cgroups | Ve solo su rama |

### ✅ Ejemplo resuelto: un "contenedor" sin Docker

Puedes crear namespaces tú mismo con `unshare` (sin sudo, gracias al namespace de usuario). Esto es lo que hace Docker por debajo, en miniatura. Ejecutado en este PC:

```bash
# Nuevo namespace de PIDs: ps solo ve UN proceso, y es el PID 1
unshare --user --map-root-user --pid --fork --mount-proc ps aux
# USER   PID %CPU %MEM    VSZ   RSS TTY  STAT START   TIME COMMAND
# root     1  0.0  0.0  12120  4428 ?    R<   16:44   0:00 ps aux

# Nuevo namespace UTS: cambio el hostname SOLO dentro
unshare --user --map-root-user --uts sh -c 'hostname contenedor-falso; hostname'
# contenedor-falso
hostname
# yf        <- el anfitrión no se enteró

# Los namespaces de tu shell actual
ls -l /proc/self/ns
# ... net -> net:[4026531833]   pid -> pid:[4026531836]   uts -> uts:[4026531838] ...
```

Qué pasa: `--user --map-root-user` crea un namespace de usuario donde tú eres "root" (pero fuera sigues siendo `yafer`); `--pid --fork --mount-proc` crea un namespace de PIDs y monta un `/proc` nuevo, por eso `ps` ve un solo proceso con PID 1. Fíjate: "root" dentro, usuario normal fuera. Esa es la base de los **contenedores rootless**.

### 📏 cgroups: cuánto puede gastar

🧠 Concepto: los **cgroups** (control groups) agrupan procesos y les ponen límites y contabilidad de CPU, memoria, E/S y número de procesos. Si un contenedor pasa su límite de RAM, el kernel lo mata (OOM, código 137).

```bash
# Tu terminal ya vive en un cgroup (systemd los usa para todo)
cat /proc/self/cgroup
# 0::/user.slice/user-1000.slice/user@1000.service/app.slice/app-graphical.slice/kitty-2442-0.scope

# Con Docker, los límites se traducen a cgroups
docker run --rm -m 256m --cpus 0.5 --pids-limit 100 python:3.12-slim python -c "print('limitado')"
```

### 🥞 Capas: de dónde salen los archivos

Una imagen es una **pila de capas de solo lectura**. Al crear un contenedor, Docker pone encima una **capa fina de escritura**. OverlayFS las "aplasta" en una sola vista: si un archivo está en varias capas, gana la de más arriba. Escribir un archivo de una capa inferior lo copia a la capa de escritura (**copy-on-write**).

```capas
Capa de escritura : SOLO de este contenedor (se pierde con docker rm)
COPY . . : tu código (cambia seguido)
RUN pip install : dependencias
COPY requirements.txt : la lista de dependencias
FROM python:3.12-slim : sistema base Debian + Python (compartida)
```

Por eso: 10 contenedores de la misma imagen **no ocupan 10 veces** el disco (comparten las capas de solo lectura), y por eso lo que escribes dentro se pierde al borrar el contenedor (salvo que uses volúmenes).

### 🏛️ La arquitectura de Docker

Cuando escribes `docker run`, el comando no ejecuta nada: le pide al **daemon** que lo haga, y este delega en capas cada vez más bajas.

```flujo
dir: abajo
CLI docker -> dockerd : API REST por /var/run/docker.sock
dockerd -> containerd : gestiona imágenes y ciclo de vida
containerd -> runc : crea el contenedor (estándar OCI)
runc -> Kernel : namespaces + cgroups
```

- `docker` :: El cliente (CLI): traduce tus comandos a llamadas HTTP al daemon
- `dockerd` :: El daemon (servicio en segundo plano): red, volúmenes, builds, API
- `containerd` :: Runtime de alto nivel; Kubernetes lo usa directamente sin dockerd
- `runc` :: Runtime de bajo nivel (OCI): habla con el kernel y termina
- `BuildKit` :: El motor de construcción moderno (caché, etapas en paralelo, secretos)

📌 Gracias al estándar **OCI** (Open Container Initiative), una imagen construida con Docker la ejecutan Podman, containerd, Kubernetes o cualquier nube. Docker es una herramienta; el formato es abierto.

::: desplegable 🔬 ¿Por qué Kubernetes "quitó Docker" en 2022 y no se rompió nada?
Kubernetes habla con los runtimes mediante una interfaz llamada **CRI**. Docker no la implementaba, así que Kubernetes mantenía un adaptador llamado `dockershim`. En la versión 1.24 lo eliminaron y los clústeres pasaron a usar **containerd** (que ya estaba dentro de Docker) o CRI-O directamente.

Las imágenes siguieron funcionando porque son imágenes **OCI**: el formato no es "de Docker". Para ti como desarrollador no cambió nada: sigues construyendo con `docker build` y Kubernetes ejecuta esa imagen con containerd.
:::

🇬🇧 **namespace** /néim-spéis/ = espacio de nombres · **control group** /kontróul grup/ = grupo de control · **copy-on-write** /kópi on ráit/ = copiar al escribir · **daemon** /dímon/ = proceso en segundo plano · **runtime** /rán-táim/ = entorno de ejecución · **rootless** /rút-les/ = sin root

## 📦 Imagen vs contenedor vs registro

Las tres palabras que tienes que tener clarísimas:

🧠 Concepto: **imagen** = plantilla de solo lectura (sistema de archivos + metadatos: qué comando ejecutar, puertos, variables). Se identifica por nombre:etiqueta y por un **digest** (`sha256:...`) inmutable.

🧠 Concepto: **contenedor** = una instancia de una imagen en ejecución (o detenida), con su capa de escritura, su red y su estado.

🧠 Concepto: **registro** (registry) = servidor que guarda y reparte imágenes: Docker Hub, GitHub Container Registry (`ghcr.io`), AWS ECR, Google Artifact Registry...

Analogía de programación: la imagen es la **clase**, el contenedor es el **objeto** (`new`), y el registro es **npm/PyPI** pero de imágenes.

```flujo
Dockerfile -> Imagen : docker build
Imagen -> Registro : docker push
Registro -> Imagen en servidor : docker pull
Imagen en servidor -> Contenedor : docker run
Contenedor --> Imagen : docker commit (evítalo)
```

### 🏷️ Anatomía del nombre de una imagen

```text
ghcr.io / yftorrezg / mi-api : 1.4.2 @ sha256:9f86d08...
 │          │          │        │       │
 │          │          │        │       └─ digest: hash del contenido (inmutable)
 │          │          │        └───────── etiqueta (tag): mutable, normalmente la versión
 │          │          └────────────────── repositorio
 │          └───────────────────────────── usuario u organización
 └──────────────────────────────────────── registro (si falta: docker.io = Docker Hub)
```

| Nombre | Qué significa |
|---|---|
| `python:3.12-slim` | Oficial de Docker Hub (`docker.io/library/python`), Debian reducido |
| `node:22-alpine` | Node 22 sobre Alpine Linux (muy pequeña) |
| `postgres:16` | Postgres 16 (el último parche de la rama 16) |
| `yafer/mi-api:1.0` | Tu imagen en tu cuenta de Docker Hub |
| `ghcr.io/org/app:sha-3f2a1c9` | En GitHub Container Registry, etiquetada con el commit |
| `nginx@sha256:...` | Fijada por digest: siempre exactamente la misma |

⚠️ Cuidado: una **etiqueta se puede mover**. `postgres:16` hoy apunta a un parche y mañana a otro; `latest` no significa "la más nueva", es solo la etiqueta por defecto. En producción usa versiones concretas y, para máxima reproducibilidad, el digest.

### 🔄 Ciclo de vida de un contenedor

```flujo
Creado -> Corriendo : docker start
Corriendo -> Detenido : docker stop / el proceso termina
Detenido -> Corriendo : docker start
Corriendo -> Pausado : docker pause
Pausado -> Corriendo : docker unpause
Detenido -> Borrado : docker rm
```

📌 Un contenedor vive **mientras vive su proceso principal** (PID 1). Si tu `CMD` termina o falla, el contenedor se detiene. Por eso `docker run ubuntu` termina al instante: no tiene nada que hacer.

🇬🇧 **registry** /réyistri/ = registro · **tag** /tag/ = etiqueta · **digest** /dáiyest/ = resumen (hash) · **pull / push** /pul / push/ = descargar / subir · **instance** /ínstans/ = instancia · **immutable** /imiútabol/ = inmutable

## ⌨️ Comandos esenciales

### 🛠️ Instalar en Arch / CachyOS

El servicio `docker` es un daemon; el comando `docker` solo le manda órdenes. En este PC el cliente está instalado, pero el daemon está **apagado** (por eso los ejemplos de contenedores de esta hoja no se pudieron ejecutar aquí; los de `unshare`, Python y `docker compose config` sí).

```bash
sudo pacman -S docker docker-compose docker-buildx
sudo systemctl enable --now docker.service   # o solo docker.socket: arranca al primer uso
sudo usermod -aG docker $USER                 # usar docker sin sudo (cierra sesión después)
docker run --rm hello-world                   # prueba
```

⚠️ Cuidado: estar en el grupo `docker` **equivale a ser root** (puedes montar `/` del host en un contenedor). Alternativa más segura: Docker en modo rootless o Podman.

💡 Consejo: si no lo usas a diario, habilita solo `docker.socket`: el daemon arranca cuando lo llamas y no consume nada mientras tanto.

### ⭐ Los que usarás el 90 % del tiempo

| Comando | Qué hace | Ejemplo |
|---|---|---|
| `docker run` | Crea y arranca un contenedor | `docker run -d -p 8080:80 nginx` |
| `docker ps` | Contenedores vivos (`-a`: todos) | `docker ps -a` |
| `docker logs` | Lo que imprimió la app | `docker logs -f api` |
| `docker exec` | Ejecuta algo dentro de uno vivo | `docker exec -it api sh` |
| `docker stop` / `start` | Detiene (SIGTERM) / arranca | `docker stop api` |
| `docker rm` | Borra un contenedor (`-f` fuerza) | `docker rm -f api` |
| `docker build` | Construye una imagen | `docker build -t mi-api:1.0 .` |
| `docker images` | Lista imágenes | `docker images` |
| `docker rmi` | Borra una imagen | `docker rmi mi-api:0.9` |
| `docker pull` / `push` | Descarga / sube | `docker push ghcr.io/yo/app:1.0` |
| `docker compose up` | Levanta un proyecto entero | `docker compose up -d --build` |

### 🚀 docker run a fondo

```bash
docker run [OPCIONES] IMAGEN [COMANDO] [ARGUMENTOS]
```

Todo lo que va **antes** de la imagen son opciones de Docker; todo lo que va **después** es el comando para el contenedor. `docker run nginx -p 8080:80` está mal: le pasa `-p 8080:80` a nginx.

- `-d` :: Detached: en segundo plano
- `-p 8080:80` :: Publica puerto: **afuera:adentro** (host:contenedor)
- `-p 127.0.0.1:5432:5432` :: Publica solo en tu máquina, no en toda la red
- `-v pgdata:/var/lib/postgresql/data` :: Volumen con nombre
- `-v "$PWD":/app` :: Bind mount de tu carpeta (en fish: `-v (pwd):/app`)
- `-e DEBUG=1` / `--env-file .env` :: Variables de entorno
- `--name api` :: Nombre fijo (si no, Docker inventa uno tipo `sad_turing`)
- `--rm` :: Borra el contenedor al terminar (ideal para pruebas)
- `-it` :: Interactivo con terminal (para shells)
- `--network mired` :: Lo conecta a una red
- `--restart unless-stopped` :: Reinicio automático si se cae o reinicia el host
- `-m 512m --cpus 1` :: Límites de RAM y CPU (cgroups)
- `-u 1000:1000` :: Ejecuta como otro usuario
- `--gpus all` :: Acceso a la GPU NVIDIA (requiere NVIDIA Container Toolkit)
- `--entrypoint sh` :: Reemplaza el ENTRYPOINT (para entrar a imágenes que no arrancan)

### ✅ Ejemplo resuelto: cinco usos reales en una línea

```bash
# 1. Servidor web con tu carpeta, en http://localhost:8080 (solo lectura)
docker run -d --rm --name web -p 8080:80 -v "$PWD":/usr/share/nginx/html:ro nginx:1.27-alpine

# 2. Probar una versión de Python sin instalarla
docker run --rm -it python:3.13-slim python -c "import sys; print(sys.version)"

# 3. Postgres para desarrollo, accesible solo desde tu PC
docker run -d --name pg -e POSTGRES_PASSWORD=cambia_esto \
  -v pgdata:/var/lib/postgresql/data -p 127.0.0.1:5432:5432 postgres:16

# 4. Redis en segundos
docker run -d --name redis -p 127.0.0.1:6379:6379 redis:7-alpine

# 5. Una herramienta sin instalarla (ej. convertir con ffmpeg tu carpeta actual)
docker run --rm -v "$PWD":/w -w /w jrottenberg/ffmpeg -i video.mp4 audio.mp3
```

Qué hace cada parte: en (1) `:ro` monta en solo lectura y `--rm` limpia al parar; en (3) el volumen `pgdata` guarda los datos aunque borres el contenedor y `127.0.0.1:` evita exponer la base a la red del laboratorio o del café; en (5) `-w /w` es la carpeta de trabajo dentro, así ffmpeg ve tus archivos.

- `docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"` :: Lista compacta
- `docker stop $(docker ps -q)` :: Detiene todo (en fish: `docker stop (docker ps -q)`)
- `docker system df` :: Cuánto disco usa Docker
- `docker system prune` :: Borra contenedores parados, redes sin usar, imágenes colgantes y caché
- `docker image prune -a` :: Borra todas las imágenes sin contenedor
- `docker init` :: Genera Dockerfile, compose y .dockerignore de partida para tu proyecto

⚠️ Cuidado: "port is already allocated" = ese puerto del host ya está en uso. Cambia el de la izquierda (`-p 8081:80`), nunca el de la derecha (es donde escucha la app).

⚠️ Cuidado: si la app escucha en `127.0.0.1` **dentro** del contenedor, no se verá desde fuera aunque publiques el puerto. Tiene que escuchar en `0.0.0.0`. Es el error número uno con Flask, FastAPI, Vite y Next en Docker.

🇬🇧 **detached** /ditácht/ = desacoplado · **publish** /páblish/ = publicar · **bind** /báind/ = enlazar · **prune** /prun/ = podar (limpiar) · **allocated** /álokeitid/ = asignado

## 📝 Dockerfile instrucción por instrucción

🧠 Concepto: un **Dockerfile** es la receta para construir una imagen: un archivo de texto llamado exactamente `Dockerfile` (sin extensión) con instrucciones que se ejecutan de arriba abajo. Las que cambian el sistema de archivos (`RUN`, `COPY`, `ADD`) crean una **capa**; las demás solo guardan metadatos.

| Instrucción | Qué hace | Cuándo corre |
|---|---|---|
| `FROM` | Imagen base (siempre la primera; puede haber varias) | Build |
| `WORKDIR` | Carpeta de trabajo (la crea si no existe) | Build y run |
| `COPY` | Copia archivos del contexto a la imagen | Build |
| `ADD` | Como COPY + descomprime `.tar` y baja URLs | Build |
| `RUN` | Ejecuta un comando y guarda el resultado como capa | Build |
| `ENV` | Variable de entorno (queda en la imagen) | Build y run |
| `ARG` | Variable solo durante el build | Build |
| `EXPOSE` | Documenta el puerto (NO lo publica) | Metadato |
| `USER` | Usuario para lo que sigue y para el contenedor | Build y run |
| `CMD` | Comando por defecto al arrancar (reemplazable) | Run |
| `ENTRYPOINT` | Programa fijo; CMD pasa a ser sus argumentos | Run |
| `HEALTHCHECK` | Comando que dice si la app está sana | Run |
| `LABEL` | Metadatos (autor, repo, versión) | Metadato |
| `VOLUME` | Marca una carpeta como volumen | Run |
| `STOPSIGNAL` | Señal para detener (por defecto SIGTERM) | Run |

### ✅ Ejemplo resuelto: API FastAPI comentada línea a línea

Proyecto:

```arbol
mi-api/
  app/
    __init__.py
    main.py
  requirements.txt
  .dockerignore
  Dockerfile
```

Archivo `app/main.py` (lee la configuración de variables de entorno, como debe ser):

```python
import os
from fastapi import FastAPI

app = FastAPI(title="mi-api")
ENTORNO = os.getenv("APP_ENV", "desarrollo")


@app.get("/health")
def health():
    # Endpoint barato para que Docker/Kubernetes sepan si estamos vivos
    return {"ok": True}


@app.get("/suma/{a}/{b}")
def suma(a: int, b: int):
    return {"resultado": a + b, "entorno": ENTORNO}
```

Archivo `requirements.txt` (versiones fijadas):

```text
fastapi==0.115.6
uvicorn[standard]==0.34.0
```

Archivo `Dockerfile`:

```dockerfile
# syntax=docker/dockerfile:1
# 1. Base: versión concreta, variante slim (Debian reducido, glibc)
FROM python:3.12-slim

# 2. Python en contenedores: sin .pyc y con salida inmediata a los logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# 3. Carpeta de trabajo
WORKDIR /app

# 4. Usuario sin privilegios (lo creamos pronto, se usa al final)
RUN useradd --create-home --uid 10001 app

# 5. PRIMERO solo las dependencias: esta capa se cachea mientras
#    requirements.txt no cambie
COPY requirements.txt .
RUN pip install -r requirements.txt

# 6. DESPUÉS el código (cambia en cada commit)
COPY --chown=app:app app/ ./app/

# 7. Cambiamos a usuario normal
USER app

# 8. Documentación del puerto + chequeo de salud
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')"

# 9. Forma exec (JSON): uvicorn es el PID 1 y recibe bien SIGTERM
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t mi-api:1.0 .
docker run -d --name api -p 8000:8000 -e APP_ENV=produccion mi-api:1.0
curl localhost:8000/suma/2/3
# {"resultado":5,"entorno":"produccion"}
docker ps        # la columna STATUS dirá "Up 1 minute (healthy)"
```

El `.` final de `docker build` es el **contexto de construcción**: la carpeta que se envía al motor de build. `COPY` solo puede copiar cosas que están dentro de ese contexto.

### 🔁 RUN vs CMD vs ENTRYPOINT

::: columnas
### 🔨 RUN
- Se ejecuta **una vez, al construir**.
- Su resultado queda guardado en una capa.
- Para instalar cosas: `RUN apt-get install ...`
::: siguiente
### ▶️ CMD
- Se ejecuta **cada vez que arranca** un contenedor.
- `docker run img otro-comando` lo **reemplaza**.
- Solo cuenta el último CMD del archivo.
::: siguiente
### 🚪 ENTRYPOINT
- También al arrancar, pero **no se reemplaza** fácil.
- Lo que pongas tras la imagen se le pasa como argumento.
- La imagen se comporta como un programa.
:::

```dockerfile
FROM python:3.12-slim
ENTRYPOINT ["python", "-m", "http.server"]
CMD ["8000"]
# docker run img          -> python -m http.server 8000
# docker run img 9000     -> python -m http.server 9000
# docker run --entrypoint sh -it img   -> shell para depurar
```

::: columnas
### ❌ Forma shell
```dockerfile
CMD uvicorn app.main:app --host 0.0.0.0
```
- Docker ejecuta `/bin/sh -c "uvicorn ..."`.
- El PID 1 es `sh`, que **no reenvía SIGTERM**.
- `docker stop` espera 10 s y mata con SIGKILL.
::: siguiente
### ✅ Forma exec (JSON)
```dockerfile
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
```
- Tu programa es el PID 1.
- Recibe SIGTERM y se apaga limpio (cierra conexiones).
- Comillas **dobles** obligatorias (es JSON).
:::

### 🧐 COPY vs ADD, ARG vs ENV

| Par | Usa | Por qué |
|---|---|---|
| `COPY` vs `ADD` | `COPY` casi siempre | `ADD` descomprime y baja URLs "por arte de magia": sorpresas |
| `ARG` vs `ENV` | `ARG` para el build, `ENV` para la app | `ARG` no existe al ejecutar; `ENV` sí |
| `CMD` vs `ENTRYPOINT` | `CMD` para apps; `ENTRYPOINT` para herramientas | CMD es más fácil de sobrescribir |
| `alpine` vs `slim` | `slim` para Python; `alpine` si todo es puro | Alpine usa musl: ruedas de pip con C fallan o compilan lento |

⚠️ Cuidado: `EXPOSE 8000` NO abre ningún puerto. Es documentación. Para entrar desde fuera sigues necesitando `-p 8000:8000`.

⚠️ Cuidado: `WORKDIR` en vez de `RUN cd /app`: cada `RUN` es una shell nueva, así que el `cd` se olvida en la línea siguiente.

💡 Consejo: añade `# syntax=docker/dockerfile:1` en la primera línea: activa las funciones modernas de BuildKit (`--mount=type=cache`, `--mount=type=secret`, heredocs).

🇬🇧 **build context** /bild kóntekst/ = contexto de construcción · **entrypoint** /éntri-póint/ = punto de entrada · **exec form** /egsék form/ = forma de ejecución directa · **signal** /sígnal/ = señal · **graceful shutdown** /gréisful shát-dáun/ = apagado ordenado

## 🧱 Caché de capas, orden y .dockerignore

Docker guarda cada capa en caché. Al reconstruir, recorre las instrucciones en orden y **reutiliza** cada capa si la instrucción y sus archivos de entrada no cambiaron. La regla de oro: **cuando una capa cambia, todas las que vienen después se reconstruyen**.

🧠 Concepto: **invalidación de caché**: para `COPY`/`ADD`, Docker compara el contenido (checksum) de los archivos copiados; para `RUN`, compara el texto del comando. Si algo difiere, esa capa y todas las siguientes se rehacen.

```flujo
dir: abajo
FROM -> COPY requirements : CACHED
COPY requirements -> RUN pip install : CACHED (2 min ahorrados)
RUN pip install -> COPY código : cambió main.py
COPY código -> CMD : se rehace solo esto (1 s)
```

::: columnas
### ❌ Orden malo
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```
Cambias una coma en `main.py` → `COPY . .` cambia → `pip install` se repite entero. Cada build: minutos.
::: siguiente
### ✅ Orden bueno
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```
Cambias `main.py` → solo se rehace `COPY . .`. Cada build: segundos.
:::

```grafica
tipo: barras
titulo: Rebuild tras cambiar una línea de código (ilustrativo, API con pandas + torch)
unidad: s
Orden malo : 240
Orden bueno : 3
Orden bueno + cache mount : 3
```

### 🧹 Reglas para capas limpias

```dockerfile
# ✅ update + install + limpieza en LA MISMA capa
RUN apt-get update \
 && apt-get install -y --no-install-recommends libpq5 curl \
 && rm -rf /var/lib/apt/lists/*

# ✅ Caché de pip que persiste entre builds pero NO entra en la imagen (BuildKit)
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# ✅ Lo mismo para npm
RUN --mount=type=cache,target=/root/.npm npm ci
```

📌 Borrar archivos en un `RUN` posterior **no adelgaza** la imagen: la capa anterior ya los guardó y sigue dentro. Las capas solo suman. Por eso se limpia en el mismo `RUN` con `&&` (o se usa multi-stage).

⚠️ Cuidado: `RUN apt-get update` en una capa y `RUN apt-get install` en otra hace que la caché reutilice listas de paquetes viejas y un día la instalación falla con 404. Siempre juntos.

⚠️ Cuidado: `RUN git clone https://...` o `RUN curl .../latest.tar.gz` se cachean por el **texto** del comando: aunque el repo cambie, Docker reutiliza la capa vieja. Fija versiones o usa `--no-cache`.

- `docker build --no-cache -t app .` :: Ignora toda la caché
- `docker build --progress=plain .` :: Muestra la salida completa de cada paso
- `docker history app` :: Capas y tamaño de cada una
- `docker buildx du` :: Cuánto ocupa la caché de BuildKit

### 🙈 .dockerignore

Antes de construir, Docker envía **todo el contexto** (la carpeta del `.`) al motor de build. `.dockerignore` funciona como `.gitignore`: dice qué NO enviar. Tres beneficios: build más rápido, imagen más pequeña y **sin secretos colados**. Además evita que cambios en archivos irrelevantes (logs, `.git`) invaliden la caché de `COPY . .`.

```text
# .dockerignore
.git
.gitignore
.github/
**/__pycache__/
**/*.pyc
.venv/
venv/
node_modules/
.next/
dist/
build/
coverage/
.pytest_cache/
.env
.env.*
!.env.example
*.log
*.pem
*.key
datos/
modelos/*.pt
Dockerfile*
compose*.yaml
README.md
```

- `.env` :: Excluir SIEMPRE: contraseñas y claves de API
- `node_modules/` :: Se reinstala dentro con `npm ci` (binarios de tu SO no sirven en Linux musl/glibc)
- `.git` :: Puede pesar cientos de MB y contiene todo el historial (¡con secretos viejos!)
- `!.env.example` :: El `!` vuelve a incluir algo excluido antes
- `**/*.pyc` :: `**` = en cualquier subcarpeta

💡 Consejo: si la primera línea del build dice que transfiere un contexto de varios GB, te falta `.dockerignore` (casi siempre: datasets, `node_modules` o `.git`).

🇬🇧 **cache hit / miss** /kash jit / mis/ = acierto / fallo de caché · **invalidate** /inválideit/ = invalidar · **checksum** /chék-sam/ = suma de comprobación · **layer** /léier/ = capa · **ignore file** /ignór fáil/ = archivo de exclusiones

## 🏗️ Multi-stage builds

Para **construir** necesitas herramientas pesadas (compiladores, TypeScript, npm, cabeceras de C, `gcc`) que **no** necesitas para **ejecutar**. Un multi-stage build usa varias etapas `FROM` en un mismo Dockerfile: las primeras construyen y la última solo copia el resultado. La imagen final es la última etapa; lo demás se descarta.

Analogía: cocinas en la cocina (ollas, cuchillos, harina por todas partes), pero al comedor solo llevas el plato servido.

```flujo
dir: abajo
Código + node:22 -> dist/ : npm run build (etapa build)
dist/ -> nginx:alpine : COPY --from=build
nginx:alpine -> Imagen final : ~55 MB, sin Node
```

### ✅ Ejemplo resuelto: frontend React (Vite) servido por nginx

```dockerfile
# syntax=docker/dockerfile:1
# ---------- Etapa 1: construir ----------
FROM node:22-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN --mount=type=cache,target=/root/.npm npm ci
COPY . .
RUN npm run build                 # genera /app/dist (HTML, JS y CSS estáticos)

# ---------- Etapa 2: servir ----------
FROM nginx:1.27-alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
# nginx ya tiene su CMD por defecto
```

### ✅ Ejemplo resuelto: API Node con TypeScript

```dockerfile
# syntax=docker/dockerfile:1
# ---- deps: dependencias completas para compilar ----
FROM node:22-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

# ---- build: compila TypeScript a JavaScript ----
FROM deps AS build
COPY . .
RUN npm run build && npm prune --omit=dev   # quita devDependencies

# ---- final: solo runtime ----
FROM node:22-alpine
ENV NODE_ENV=production
WORKDIR /app
COPY --from=build --chown=node:node /app/node_modules ./node_modules
COPY --from=build --chown=node:node /app/dist ./dist
COPY --chown=node:node package.json ./
USER node
EXPOSE 3000
CMD ["node", "dist/server.js"]
```

### ✅ Ejemplo resuelto: Python con dependencias compiladas

El truco en Python: instalar todo en un **entorno virtual** (`/opt/venv`) en la etapa de build (que tiene `gcc`) y copiar esa carpeta a una imagen final limpia.

```dockerfile
# syntax=docker/dockerfile:1
# ---------- Etapa 1: compilar ----------
FROM python:3.12-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev \
 && rm -rf /var/lib/apt/lists/*
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

# ---------- Etapa 2: ejecutar (sin gcc ni cabeceras) ----------
FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends libpq5 \
 && rm -rf /var/lib/apt/lists/* \
 && useradd --create-home --uid 10001 app
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH" PYTHONUNBUFFERED=1
WORKDIR /app
COPY --chown=app:app app/ ./app/
USER app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

📌 Fíjate: en la etapa de build va `libpq-dev` (cabeceras para compilar) y en la final solo `libpq5` (la librería para ejecutar). Ese patrón "`-dev` para compilar, sin `-dev` para correr" es la clave.

### 📉 Tamaños antes y después

```grafica
tipo: barras
titulo: Tamaño de imagen (aproximado, sin comprimir; varía por versión y arquitectura)
unidad: MB
Vite en node:22 (1 etapa) : 1250
Vite multi-stage nginx:alpine : 55
API TS en node:22 (1 etapa) : 1300
API TS multi-stage alpine : 190
Python en python:3.12 (1 etapa) : 1100
Python multi-stage slim : 210
```

| Caso | Antes | Después | Qué se quedó fuera |
|---|---|---|---|
| Frontend Vite | ~1,2 GB | ~50–60 MB | Node, `node_modules`, código fuente |
| API Node + TS | ~1,3 GB | ~150–250 MB | TypeScript, devDependencies, Debian completo |
| API Python | ~1,1 GB | ~150–250 MB | gcc, cabeceras, caché de pip |
| Go / Rust | ~1 GB | ~10–25 MB | Todo el compilador (final `FROM scratch` o distroless) |

📌 Cifras **aproximadas** (orden de magnitud). Mide las tuyas con `docker images` y `docker history`: dependen de tus librerías (con `torch` la imagen Python pasa fácil de 2 GB, y con CUDA de 5 GB).

- `docker build --target build -t app:debug .` :: Construye solo hasta una etapa (útil para depurar o para tests)
- `COPY --from=nginx:1.27-alpine /etc/nginx/nginx.conf .` :: Copiar desde OTRA imagen, sin etapa propia
- `FROM gcr.io/distroless/python3-debian12` :: Base distroless: sin shell ni gestor de paquetes

💡 Consejo: añade una etapa `test` (`FROM build AS test` + `RUN pytest`) y en CI ejecuta `docker build --target test .`: los tests corren en el mismo entorno que producción.

🇬🇧 **multi-stage build** /múlti stéich bild/ = construcción en varias etapas · **stage** /stéich/ = etapa · **artifact** /ártifakt/ = artefacto · **footprint** /fút-print/ = huella (tamaño) · **prune** /prun/ = recortar

## 💾 Volúmenes vs bind mounts

Los contenedores son **efímeros** (ephemeral): todo lo escrito en su capa de escritura se pierde con `docker rm`. Y eso es **bueno**: puedes destruir y recrear contenedores sin miedo. Los datos que deben sobrevivir (la base de datos, archivos subidos, modelos entrenados) se guardan **fuera**, en montajes.

| Tipo | Sintaxis | Dónde vive | Para qué |
|---|---|---|---|
| Volumen | `-v pgdata:/var/lib/postgresql/data` | Gestionado por Docker | Bases de datos, producción |
| Bind mount | `-v "$PWD":/app` | Una carpeta tuya concreta | Desarrollo: editar y ver al instante |
| tmpfs | `--tmpfs /tmp` | En RAM | Temporales rápidos o sensibles |

🧠 Concepto: **volumen** = almacenamiento con nombre que Docker crea y gestiona (en Linux, bajo `/var/lib/docker/volumes`). Es portable, se puede respaldar y no depende de la estructura de tu disco.

🧠 Concepto: **bind mount** = enlazar una ruta exacta de tu disco dentro del contenedor. Lo que cambies en un lado se ve al instante en el otro.

Cómo distinguirlos: si lo de la izquierda empieza por `/`, `./` o `~`, es **bind mount**; si es un **nombre**, es un volumen.

::: columnas
### 📦 Volumen
- ✅ Datos de Postgres, MySQL, Redis.
- ✅ Funciona igual en Linux, Mac y Windows.
- ✅ Docker inicializa el volumen con el contenido de la imagen.
- ❌ No lo editas cómodamente desde tu editor.
::: siguiente
### 📁 Bind mount
- ✅ Código en desarrollo con recarga en caliente.
- ✅ Pasar un archivo de config concreto (`:ro`).
- ❌ Depende de la ruta del host (no portable).
- ❌ Problemas de permisos (UID) y lento en Mac/Windows.
:::

### ✅ Ejemplo resuelto: los datos sobreviven al contenedor

```bash
# 1. Un contenedor escribe en el volumen "notas" y se borra (--rm)
docker run --rm -v notas:/datos alpine sh -c 'echo "hola volumen" > /datos/nota.txt'

# 2. OTRO contenedor, totalmente nuevo, monta el mismo volumen y lee
docker run --rm -v notas:/datos alpine cat /datos/nota.txt
# hola volumen

# 3. Copia de seguridad del volumen a un .tar en tu carpeta
docker run --rm -v notas:/datos:ro -v "$PWD":/backup alpine \
  tar czf /backup/notas.tar.gz -C /datos .

# 4. Limpiar
docker volume rm notas
```

- `docker volume ls` :: Lista volúmenes
- `docker volume inspect pgdata` :: Dónde está en disco y quién lo usa
- `docker volume rm pgdata` :: Lo borra (¡y sus datos!)
- `-v "$PWD"/nginx.conf:/etc/nginx/nginx.conf:ro` :: Bind mount de UN archivo en solo lectura
- `--mount type=volume,src=pgdata,dst=/var/lib/postgresql/data` :: Sintaxis larga (más explícita, falla si algo está mal)

⚠️ Cuidado: montar una carpeta **tapa** lo que había en esa ruta de la imagen. Si haces `-v "$PWD":/app` y la imagen tenía `/app/node_modules`, desaparece. Solución típica en compose: añadir un volumen anónimo `- /app/node_modules`.

⚠️ Cuidado: con bind mounts, los archivos creados dentro como root aparecen en tu carpeta con dueño root. Ejecuta con `-u "$(id -u):$(id -g)"` (en fish: `-u (id -u):(id -g)`).

⚠️ Cuidado: no guardes la base de datos de producción en un bind mount de una carpeta cualquiera, ni corras dos contenedores de Postgres sobre el mismo volumen: corrupción garantizada.

🇬🇧 **volume** /vólium/ = volumen · **bind mount** /báind máunt/ = montaje enlazado · **ephemeral** /ifémeral/ = efímero · **persistent** /persístent/ = persistente · **read-only** /ríd ónli/ = solo lectura · **backup** /bák-ap/ = copia de seguridad

## 🌐 Redes

Cada contenedor tiene su propio namespace de red: su IP, sus puertos y **su propio `localhost`**. Para que dos contenedores se hablen (la API con Postgres) se ponen en la misma **red definida por el usuario**: ahí Docker trae un **DNS interno** y cada contenedor se encuentra por su **nombre**.

```flujo
Navegador -> Puerto 8000 del host : http://localhost:8000
Puerto 8000 del host -> api : -p 8000:8000
api -> db : postgres://db:5432 (DNS interno)
api -> redis : redis://redis:6379
```

| Driver | Qué es | Cuándo |
|---|---|---|
| `bridge` por defecto | Red privada en el host, SIN DNS por nombre | Pruebas sueltas |
| bridge propia | Igual, pero CON DNS por nombre | Siempre que conectes contenedores |
| `host` | Usa la red del host directamente (sin `-p`) | Rendimiento máximo, sin aislamiento |
| `none` | Sin red | Tareas aisladas por seguridad |
| `overlay` | Red entre varias máquinas | Docker Swarm |

### ✅ Ejemplo resuelto: dos contenedores que se encuentran por nombre

```bash
docker network create labred
docker run -d --name servidor --network labred nginx:1.27-alpine
docker run --rm --network labred alpine wget -qO- http://servidor | head -4
# <!DOCTYPE html>
# <html>
# <head>
# <title>Welcome to nginx!</title>
docker rm -f servidor && docker network rm labred
```

📌 Dentro de un contenedor, `localhost` es **el propio contenedor**. Para hablar con otro contenedor usa su **nombre** (o el nombre del servicio en compose). Para hablar con tu laptop usa `host.docker.internal` (en Linux hay que añadirlo con la opción de abajo).

- `--add-host=host.docker.internal:host-gateway` :: En Linux: hace que `host.docker.internal` apunte a tu PC

::: columnas
### ❌ Mal
```text
DATABASE_URL=postgresql://user:pass@localhost:5432/app
```
Desde el contenedor `api`, `localhost` es `api`: ahí no hay Postgres. Error: `connection refused`.
::: siguiente
### ✅ Bien
```text
DATABASE_URL=postgresql://user:pass@db:5432/app
```
`db` es el nombre del servicio; el DNS de Docker lo traduce a la IP del contenedor de Postgres.
:::

### 🔒 Publicar puertos con cuidado

- `-p 5432:5432` :: Escucha en TODAS las interfaces del host: cualquiera en tu red llega a la base
- `-p 127.0.0.1:5432:5432` :: Solo desde tu máquina
- `(sin -p)` :: Solo accesible desde otros contenedores de la misma red (lo correcto para la base en producción)

⚠️ Cuidado: Docker escribe sus propias reglas de iptables/nftables y los puertos publicados **se saltan** muchos firewalls como UFW. Hay servidores "protegidos con UFW" con su Redis o su Postgres abiertos a internet por un `-p 6379:6379`. Publica solo lo que debe ser público (normalmente el proxy en 80/443).

🇬🇧 **network** /nét-uork/ = red · **bridge** /brich/ = puente · **DNS resolution** /di en es rezolúshon/ = resolución de nombres · **expose / publish** /ikspóus / páblish/ = exponer / publicar · **firewall** /fáier-uól/ = cortafuegos

## 🔐 Variables de entorno y secretos

La misma imagen debe servir para desarrollo, staging y producción: lo que cambia es la **configuración**, y esta entra desde fuera como variables de entorno (principio de la **Twelve-Factor App**: la config vive en el entorno, no en el código).

```bash
docker run -e APP_ENV=produccion -e LOG_LEVEL=info mi-api
docker run -e API_KEY mi-api              # pasa la que ya tienes en tu terminal
docker run --env-file .env mi-api         # desde archivo
```

```python
import os

APP_ENV = os.getenv("APP_ENV", "desarrollo")        # opcional, con valor por defecto
DATABASE_URL = os.environ["DATABASE_URL"]           # obligatoria: falla rápido si falta
DEBUG = os.getenv("DEBUG", "0") == "1"              # las variables siempre son TEXTO
```

### 🗝️ Niveles de secreto (de peor a mejor)

| Método | Riesgo | Uso |
|---|---|---|
| `ENV CLAVE=...` o `ARG` en el Dockerfile | Queda grabado en la imagen (`docker history`, `inspect`) | NUNCA para secretos |
| `COPY .env .` | Queda en una capa; si publicas la imagen, lo publicas | NUNCA |
| `-e` / `--env-file` al ejecutar | Visible en `docker inspect` y en `/proc` | Aceptable en desarrollo |
| Secretos de compose (archivo montado) | Solo un archivo en `/run/secrets/` | Bueno en un servidor |
| Gestor de secretos (Vault, AWS Secrets Manager, secretos de K8s/PaaS) | Rotación, auditoría | Producción seria |

### ✅ Ejemplo resuelto: secreto en tiempo de build (sin dejar rastro)

Necesitas un token para instalar un paquete privado de npm o pip, pero no quieres que quede en la imagen:

```dockerfile
# syntax=docker/dockerfile:1
FROM node:22-alpine
WORKDIR /app
COPY package.json package-lock.json ./
# El .npmrc se monta SOLO durante este RUN; no queda en ninguna capa
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc npm ci
COPY . .
CMD ["node", "server.js"]
```

```bash
docker build --secret id=npmrc,src=$HOME/.npmrc -t app .
```

### ✅ Ejemplo resuelto: secreto en tiempo de ejecución con compose

Muchas imágenes oficiales aceptan la variante `_FILE`: leen el valor de un archivo en vez de una variable.

```yaml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt   # en .gitignore y .dockerignore
```

💡 Consejo: sube a git un `.env.example` con las claves y valores falsos (`DB_PASSWORD=cambia_esto`) para que el equipo sepa qué variables existen. El `.env` real, nunca.

⚠️ Cuidado: `ARG` "para no dejar la clave en la imagen" no sirve: el valor de un `ARG` usado en un `RUN` queda en los metadatos de la capa. Usa `--mount=type=secret`.

⚠️ Cuidado: si un secreto llegó alguna vez a una imagen publicada o a git, **rótalo** (cámbialo). Borrarlo en una capa nueva no lo elimina de las anteriores.

🇬🇧 **environment variable** /enváironment vériabol/ = variable de entorno · **secret** /síkret/ = secreto · **rotate** /róuteit/ = rotar (cambiar una clave) · **leak** /lík/ = fuga · **twelve-factor app** /tuélv fáktor ap/ = app de doce factores

## 🎼 Docker Compose: app + Postgres + Redis

Cuando tu proyecto tiene varios contenedores, escribir un `docker run` largo para cada uno es un infierno. **Docker Compose** los describe todos en un archivo `compose.yaml` y los levanta con un comando. Compose crea solo una red donde cada **servicio** se encuentra por su nombre, y volúmenes con nombre del proyecto.

Analogía: si `docker run` es tocar un instrumento, Compose es la **partitura de la orquesta** entera.

🧠 Concepto: **servicio** = un contenedor (o varias réplicas) definido en compose, con su imagen, puertos, variables, volúmenes y dependencias.

🧠 Concepto: **healthcheck** = comando que Docker ejecuta periódicamente dentro del contenedor; si sale con código 0, el contenedor está sano (healthy). Con la condición `service_healthy` en `depends_on`, un servicio espera a que otro esté **listo de verdad**, no solo arrancado.

```secuencia
actores: Compose, db, redis, api
Compose -> db : arranca Postgres
Compose -> redis : arranca Redis
nota db : pg_isready cada 5 s
db --> Compose : healthy
redis --> Compose : healthy (PONG)
Compose -> api : ahora sí, arranca la API
nota api : /health responde 200
api --> Compose : healthy
```

### ✅ Ejemplo resuelto: el proyecto completo

```arbol
tienda/
  compose.yaml
  compose.override.yaml
  .env
  .env.example
  secrets/
    db_password.txt
  api/
    Dockerfile
    requirements.txt
    app/
      __init__.py
      main.py
```

Archivo `compose.yaml` (producción y base común):

```yaml
name: tienda

services:
  api:
    build:
      context: ./api
    image: ghcr.io/yftorrezg/tienda-api:${TAG:-dev}
    restart: unless-stopped
    environment:
      APP_ENV: ${APP_ENV:-produccion}
      DB_HOST: db
      DB_NAME: tienda
      DB_USER: tienda
      DB_PASSWORD_FILE: /run/secrets/db_password
      REDIS_URL: redis://redis:6379/0
    secrets:
      - db_password
    ports:
      - "127.0.0.1:8000:8000"
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "python", "-c",
             "import urllib.request as u; u.urlopen('http://127.0.0.1:8000/health')"]
      interval: 10s
      timeout: 3s
      start_period: 15s
      retries: 3
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: "1.0"

  db:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      POSTGRES_DB: tienda
      POSTGRES_USER: tienda
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U tienda -d tienda"]
      interval: 5s
      timeout: 3s
      retries: 10

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    command: ["redis-server", "--appendonly", "yes"]
    volumes:
      - redisdata:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 10

volumes:
  pgdata:
  redisdata:

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

Archivo `api/app/main.py` (cuenta visitas en Redis y lee productos de Postgres):

```python
import os
from contextlib import asynccontextmanager

import psycopg
import redis
from fastapi import FastAPI


def leer_secreto(nombre: str) -> str:
    # Admite VAR=valor o VAR_FILE=/run/secrets/...
    ruta = os.getenv(f"{nombre}_FILE")
    if ruta:
        with open(ruta) as f:
            return f.read().strip()
    return os.environ[nombre]


DSN = (
    f"host={os.environ['DB_HOST']} dbname={os.environ['DB_NAME']} "
    f"user={os.environ['DB_USER']} password={leer_secreto('DB_PASSWORD')}"
)
cache = redis.Redis.from_url(os.environ["REDIS_URL"], decode_responses=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crea la tabla al arrancar (en un proyecto real: migraciones con Alembic)
    with psycopg.connect(DSN) as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS productos ("
            " id SERIAL PRIMARY KEY, nombre TEXT NOT NULL, precio NUMERIC(10,2))"
        )
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/productos")
def productos():
    visitas = cache.incr("visitas")
    with psycopg.connect(DSN) as conn:
        filas = conn.execute("SELECT id, nombre, precio FROM productos ORDER BY id").fetchall()
    return {
        "visitas": visitas,
        "productos": [{"id": i, "nombre": n, "precio": float(p)} for i, n, p in filas],
    }
```

`api/requirements.txt`: `fastapi`, `uvicorn[standard]`, `psycopg[binary]` y `redis` con versiones fijadas; `api/Dockerfile` es el de la sección del Dockerfile (con `CMD ["uvicorn", "app.main:app", ...]`).

Archivo `compose.override.yaml` (solo desarrollo; compose lo mezcla **automáticamente** con `compose.yaml`):

```yaml
services:
  api:
    environment:
      APP_ENV: desarrollo
    command: ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
    volumes:
      - ./api/app:/app/app        # editas en tu editor y uvicorn recarga
  db:
    ports:
      - "127.0.0.1:5432:5432"     # para conectarte con DBeaver/psql desde tu PC
```

```bash
echo "cambia_esto" > secrets/db_password.txt
docker compose up -d --build        # construye y levanta (con override: modo desarrollo)
docker compose ps                   # db y redis "healthy", luego api "healthy"
curl localhost:8000/productos       # {"visitas":1,"productos":[]}
docker compose logs -f api          # logs en vivo
docker compose exec db psql -U tienda -d tienda \
  -c "INSERT INTO productos(nombre,precio) VALUES ('Api de quinua', 7.50);"
docker compose down                 # para y borra contenedores y red (los volúmenes se quedan)

# Producción: SOLO el archivo base, sin override
docker compose -f compose.yaml up -d
```

Qué hace cada parte: `name:` fija el nombre del proyecto (prefijo de contenedores, red y volúmenes); `${TAG:-dev}` usa la variable `TAG` del entorno o del `.env` con `dev` por defecto; `127.0.0.1:8000:8000` publica la API solo localmente (delante iría un proxy con HTTPS); `db` y `redis` **no publican puertos** en producción: solo la API los alcanza por la red interna; `depends_on` con `service_healthy` evita el clásico `connection refused` del primer arranque; `deploy.resources.limits` pone límites de cgroups; el bloque `secrets` monta el archivo en `/run/secrets/db_password` dentro de ambos servicios.

✅ Verificado en este PC: `docker compose config` (que no necesita el daemon) acepta los dos archivos y muestra el resultado ya mezclado. Los contenedores no se pudieron levantar porque el daemon de Docker está apagado aquí.

| Comando | Qué hace |
|---|---|
| `docker compose up -d --build` | Construye si hace falta y levanta todo en segundo plano |
| `docker compose down` | Para y borra contenedores y red (volúmenes quedan) |
| `docker compose down -v` | Además borra los volúmenes: **adiós datos** |
| `docker compose ps` | Estado y salud de cada servicio |
| `docker compose logs -f api` | Logs en vivo de un servicio |
| `docker compose exec api sh` | Shell dentro de un servicio vivo |
| `docker compose run --rm api pytest` | Contenedor temporal del servicio para una tarea |
| `docker compose config` | Archivo final interpretado (detecta errores de YAML) |
| `docker compose pull` | Baja las imágenes nuevas (antes de actualizar) |
| `docker compose watch` | Sincroniza cambios de código sin bind mounts (sección `develop.watch`) |

⚠️ Cuidado: `depends_on` sin `condition: service_healthy` solo espera a que el contenedor **arranque**, no a que Postgres acepte conexiones. Y aun así, tu app debe **reintentar** conexiones: en producción la base puede reiniciarse en cualquier momento.

⚠️ Cuidado: la clave `version: "3.8"` arriba del archivo es obsoleta: Compose v2 la ignora y avisa. Y el comando viejo `docker-compose` (con guion, escrito en Python) dejó de mantenerse; usa `docker compose`.

⚠️ Cuidado: en YAML la indentación ES la sintaxis: espacios (nunca tabs), siempre 2. Los puertos van entre comillas (`"8000:8000"`): sin comillas, YAML 1.1 lee algunos valores como `22:22` como números en base 60.

🇬🇧 **service** /sérvis/ = servicio · **healthy** /jélzi/ = sano · **depends on** /dipénds on/ = depende de · **override** /óuver-ráid/ = sobrescribir · **orchestrate** /órkestreit/ = orquestar

## 🔍 Depurar contenedores

Cuando algo falla, sigue siempre el mismo orden: ¿está vivo? → ¿qué dijo? → ¿qué hay dentro? → ¿cómo está configurado?

```flujo
dir: abajo
docker ps -a -> ¿Exited? : mira STATUS y código
¿Exited? -> docker logs : lee el error real
docker logs -> docker exec : entra a mirar archivos y variables
docker exec -> docker inspect : red, montajes, comando, env
docker inspect -> Imagen con --entrypoint sh : si ni siquiera arranca
```

- `docker ps -a` :: Estado: `Up`, `Exited (1)`, `Restarting`, `(unhealthy)`
- `docker logs --tail 100 -f api` :: Últimas 100 líneas y seguir en vivo
- `docker logs --since 10m api` :: Solo los últimos 10 minutos
- `docker exec -it api sh` :: Shell dentro (`bash` si la imagen lo trae)
- `docker exec -u root -it api sh` :: Entrar como root aunque la imagen use otro usuario
- `docker exec api env` :: Variables de entorno reales dentro
- `docker inspect -f '{{.State.ExitCode}} {{.State.OOMKilled}}' api` :: Código de salida y si lo mató la memoria
- `docker inspect -f '{{json .State.Health}}' api` :: Historial del healthcheck con su salida
- `docker inspect -f '{{json .Mounts}}' api` :: Qué está montado y dónde
- `docker stats` :: CPU, RAM, red y E/S en vivo
- `docker top api` :: Procesos dentro del contenedor
- `docker events` :: Eventos en vivo: arranques, muertes, OOM, healthchecks
- `docker cp api:/app/logs/error.log .` :: Sacar un archivo del contenedor
- `docker run --rm -it --entrypoint sh mi-api:1.0` :: Entrar a una imagen cuyo CMD falla
- `docker debug api` :: (Docker Desktop/Pro) shell con herramientas incluso en imágenes sin shell

### 🩺 Códigos de salida

| Código | Significado habitual | Qué hacer |
|---|---|---|
| `0` | Terminó bien... pero terminó | Tu CMD no es un proceso que se quede corriendo |
| `1` | Error de la aplicación | `docker logs` |
| `126` | No se puede ejecutar (permisos) | `chmod +x`, usuario correcto |
| `127` | Comando no encontrado | Typo en CMD o no está instalado en la imagen |
| `137` | SIGKILL: casi siempre OOM o `docker kill` | Sube `-m` o baja el consumo; mira `OOMKilled` |
| `139` | Segfault | Librería nativa incompatible (¿alpine/musl?) |
| `143` | SIGTERM: parada normal | Nada, es `docker stop` |

### ✅ Ejemplo resuelto: "mi contenedor se apaga solo"

```bash
docker ps -a --filter name=api
# STATUS: Exited (1) 4 seconds ago

docker logs api
# KeyError: 'DATABASE_URL'

docker inspect -f '{{json .Config.Env}}' api
# ["PATH=...","PYTHONUNBUFFERED=1"]     <- no le pasamos la variable
```

Diagnóstico: la app exige `DATABASE_URL` (bien hecho: falla rápido) y no se la pasamos al `docker run`. Solución: `-e DATABASE_URL=...` o `--env-file .env`. Si en vez de `KeyError` vieras `ModuleNotFoundError`, el problema estaría en la imagen: faltaba la dependencia en `requirements.txt` o el `COPY` iba a otra carpeta.

### 🧰 Imágenes sin shell (distroless)

En imágenes distroless no hay `sh` para hacer `exec`. Opciones: construir una variante `:debug` (distroless trae etiquetas `debug` con busybox), o lanzar un contenedor de herramientas que comparta el namespace del que falla:

```bash
# netshoot trae curl, dig, tcpdump...; comparte la red y los procesos de "api"
docker run --rm -it --network container:api --pid container:api nicolaka/netshoot
```

💡 Consejo: copia el mensaje de error exacto (en inglés) al buscar: casi siempre alguien tuvo el mismo problema en los issues de GitHub de la imagen.

🇬🇧 **troubleshoot** /trábol-shút/ = diagnosticar · **exit code** /éksit kóud/ = código de salida · **OOM killed** /ou ou em kild/ = matado por falta de memoria · **unhealthy** /an-jélzi/ = no sano · **tail** /téil/ = cola (últimas líneas)

## 🛡️ Seguridad de contenedores

Un contenedor reduce la superficie de ataque, pero **no es seguro por defecto**. Por defecto corre como **root**, con todo lo que traiga la imagen base, y cualquiera con acceso al daemon controla el host.

```capas
Código y dependencias : vulnerabilidades en tus librerías (escaneo, actualizar)
Imagen : base mínima, sin secretos, usuario no root, firmada
Contenedor : sin privilegios, capabilities mínimas, solo lectura, límites
Host y daemon : socket protegido, rootless, kernel actualizado
Registro y CI : quién puede publicar, tokens mínimos, escaneo antes de desplegar
```

### 👤 1. Usuario no root

```dockerfile
# Debian/Ubuntu
RUN useradd --create-home --uid 10001 app
USER app

# Alpine
RUN addgroup -S app && adduser -S -G app -u 10001 app
USER app

# Imágenes oficiales de Node ya traen el usuario "node"
USER node
```

Si un atacante explota tu app, queda como un usuario sin privilegios dentro de un contenedor, no como root. Combinado con namespaces de usuario o Docker rootless, root dentro ni siquiera es root fuera.

### 🪶 2. Imágenes mínimas

🧠 Concepto: **distroless** = imágenes (de Google, `gcr.io/distroless/...`) que solo traen tu runtime y sus librerías: sin shell, sin gestor de paquetes, sin `curl`. Si un atacante entra, no tiene herramientas, y hay muchos menos paquetes con CVEs.

| Base | Tamaño aprox. | Shell | Ideal para |
|---|---|---|---|
| `ubuntu` / `debian` | ~75–80 MB | Sí | Cuando necesitas muchas herramientas |
| `python:3.12-slim` | ~120–150 MB | Sí | La opción por defecto en Python |
| `alpine` | ~8 MB | Sí (busybox) | Binarios puros, Node, herramientas |
| distroless | ~2–60 MB | No | Producción endurecida |
| `scratch` | 0 MB | No | Binarios estáticos (Go, Rust) |

Otras familias de imágenes endurecidas: Chainguard Images (Wolfi) y las Docker Hardened Images, con muy pocos CVEs y actualizadas a diario.

### 🔎 3. Escaneo de vulnerabilidades

- `docker scout cves mi-api:1.0` :: CVEs de la imagen (Docker Scout)
- `docker scout quickview mi-api:1.0` :: Resumen y recomendación de base mejor
- `trivy image mi-api:1.0` :: Escáner open source (Aqua): CVEs, secretos y malas configuraciones
- `grype mi-api:1.0` :: Otro escáner open source (Anchore)
- `syft mi-api:1.0 -o spdx-json` :: SBOM: lista de todo lo que hay dentro
- `hadolint Dockerfile` :: Linter del Dockerfile (malas prácticas)
- `cosign sign ghcr.io/yo/app@sha256:...` :: Firmar la imagen (Sigstore) para verificar su origen

🧠 Concepto: **SBOM** (Software Bill of Materials) = el "listado de ingredientes" de tu imagen: todos los paquetes y versiones. Cuando sale una vulnerabilidad nueva (como Log4Shell en 2021), con el SBOM sabes en minutos qué imágenes están afectadas.

### 🚫 4. Nunca secretos en la imagen

Ya lo vimos en variables: ni `ENV`, ni `ARG`, ni `COPY .env`. Para el build, `--mount=type=secret`; para ejecutar, secretos del orquestador o del PaaS.

### 🔒 5. Ejecución con privilegios mínimos

```bash
docker run -d --name api \
  --read-only --tmpfs /tmp \
  --cap-drop ALL \
  --security-opt no-new-privileges \
  --pids-limit 200 -m 512m --cpus 1 \
  -p 127.0.0.1:8000:8000 \
  mi-api:1.0
```

- `--read-only --tmpfs /tmp` :: Sistema de archivos de solo lectura salvo `/tmp`
- `--cap-drop ALL` :: Quita todas las capabilities de root (añade solo las necesarias con `--cap-add`)
- `--security-opt no-new-privileges` :: Impide escalar con binarios setuid (`sudo`, `su`)
- `--pids-limit 200` :: Corta las fork bombs
- `--privileged` :: ⛔ Apaga casi todo el aislamiento: solo si sabes exactamente por qué

⚠️ Cuidado: montar `/var/run/docker.sock` dentro de un contenedor (lo piden Portainer, Traefik, algunos CI) le da **control total del host**. Solo a software de total confianza, y mejor a través de un proxy del socket con permisos limitados.

⚠️ Cuidado: el puerto `2375` (API de Docker sin TLS) expuesto a internet es una de las formas más comunes de que te instalen un minero de criptomonedas en minutos: hay bots escaneando internet buscándolo todo el tiempo.

| Riesgo | Mitigación |
|---|---|
| Correr como root | `USER` no root, rootless |
| Base con cientos de CVEs | slim/distroless, rebuild periódico, escaneo en CI |
| Secretos en capas | `.dockerignore`, `--mount=type=secret`, escáner de secretos |
| Imagen de origen dudoso | Imágenes oficiales/verificadas, fijar digest, firmas |
| Contenedor comprometido escapa | Kernel al día, `--cap-drop ALL`, sin `--privileged`, gVisor si es código ajeno |
| Daemon expuesto | Nunca `2375` público; socket solo para root/grupo docker |

🇬🇧 **least privilege** /líst prívilech/ = mínimo privilegio · **hardening** /járdening/ = endurecimiento · **vulnerability (CVE)** /valnerabíliti/ = vulnerabilidad · **attack surface** /aták sérfes/ = superficie de ataque · **supply chain** /saplái chéin/ = cadena de suministro · **escape** /eskéip/ = escapar (salir del contenedor al host)

## ⚡ Tamaño y rendimiento

Una imagen pequeña no es solo vanidad: se descarga más rápido (despliegues y autoescalado más ágiles), cuesta menos en el registro y tiene menos paquetes vulnerables.

```grafica
tipo: barras
titulo: Tamaño de imágenes base (aproximado, sin comprimir, amd64)
unidad: MB
python:3.12 : 1000
python:3.12-slim : 130
python:3.12-alpine : 55
node:22 : 1100
node:22-slim : 220
node:22-alpine : 160
alpine : 8
distroless/static : 2
```

📌 Cifras aproximadas: cambian con cada versión. Compruébalas con `docker images`. Además, lo que se descarga va comprimido (suele ser bastante menos).

### 🧪 Checklist de tamaño

1. Base mínima adecuada (`-slim`, `-alpine`, distroless).
2. Multi-stage: compiladores y devDependencies fuera de la imagen final.
3. `.dockerignore` completo (sin `.git`, `node_modules`, datasets).
4. `--no-install-recommends` en apt y limpiar `/var/lib/apt/lists/*` en el mismo `RUN`.
5. `pip install --no-cache-dir` (o cache mount) y `npm ci --omit=dev`.
6. No metas datos ni modelos grandes en la imagen: descárgalos al arrancar o móntalos como volumen.
7. Revisa qué capa pesa más con `docker history --no-trunc` o la herramienta `dive`.

### 🏎️ Rendimiento en tiempo de ejecución

- CPU: un contenedor en Linux corre a velocidad **casi nativa** (es un proceso normal). El coste está en red (NAT del bridge) y E/S de la capa overlay.
- Escribe datos intensivos (bases de datos) en **volúmenes**, no en la capa de escritura del contenedor.
- En Mac/Windows, los bind mounts con muchísimos archivos (`node_modules`) son lentos: deja `node_modules` en un volumen o usa `docker compose watch`.
- Pon límites (`-m`, `--cpus`) **y** dile a tu runtime cuánta memoria tiene: Node con `--max-old-space-size`, la JVM con `-XX:MaxRAMPercentage`, gunicorn con un número de workers acorde a las CPUs del contenedor (no del host).
- `docker buildx build --platform linux/amd64,linux/arm64` construye para PC y para ARM (Mac M, Raspberry Pi, servidores Graviton/Ampere, que suelen ser más baratos).

### ⏱️ Builds rápidos

- `--mount=type=cache` :: Caché de pip/npm/go entre builds sin engordar la imagen
- `--cache-from type=registry,ref=ghcr.io/yo/app:cache` :: Reutilizar caché desde el registro (CI)
- `cache-from: type=gha` :: Caché de GitHub Actions para BuildKit
- `etapas independientes` :: BuildKit construye en paralelo etapas que no dependen entre sí

⚠️ Cuidado: alpine no siempre es más rápido ni más pequeño **para Python**: muchas ruedas (wheels) de pip vienen precompiladas para glibc (manylinux); en alpine (musl) pueden compilar desde el código fuente durante minutos y necesitar `gcc`. Para Python, `-slim` suele ser la mejor opción.

🇬🇧 **footprint** /fút-print/ = huella · **bloat** /blóut/ = inflado · **near-native** /nír néitiv/ = casi nativo · **throughput** /zrú-put/ = rendimiento (trabajo por segundo) · **cold start** /kóuld start/ = arranque en frío

## ☁️ Registries y CI/CD con GitHub Actions

🧠 Concepto: un **registry** (registro) guarda imágenes por repositorio y etiqueta. `docker push` sube solo las capas que el registro no tiene; `docker pull` baja solo las que te faltan.

| Registro | Dirección | Ideal para | Nota |
|---|---|---|---|
| Docker Hub | `docker.io` (por defecto) | Imágenes públicas, oficiales | Límite de descargas anónimas: inicia sesión en CI |
| GitHub Container Registry | `ghcr.io` | Proyectos en GitHub | Se autentica con el `GITHUB_TOKEN` de Actions |
| GitLab Registry | `registry.gitlab.com` | Proyectos en GitLab | Integrado con GitLab CI |
| AWS ECR | `<cuenta>.dkr.ecr.<región>.amazonaws.com` | Desplegar en AWS | Permisos con IAM |
| Google Artifact Registry | `<región>-docker.pkg.dev` | Cloud Run, GKE | |
| Azure Container Registry | `<nombre>.azurecr.io` | Azure | |
| Harbor (self-hosted) | El tuyo | Empresas que quieren control total | Open source (CNCF) |

### ✅ Ejemplo resuelto: publicar a mano en GHCR

```bash
# 1. Token de GitHub con permiso write:packages (NO tu contraseña)
echo "$GHCR_TOKEN" | docker login ghcr.io -u yftorrezg --password-stdin

# 2. Construir con el nombre completo y dos etiquetas
docker build -t ghcr.io/yftorrezg/tienda-api:1.0.0 -t ghcr.io/yftorrezg/tienda-api:latest ./api

# 3. Subir
docker push ghcr.io/yftorrezg/tienda-api:1.0.0
docker push ghcr.io/yftorrezg/tienda-api:latest
```

### 🏷️ Estrategia de etiquetas

| Etiqueta | Ejemplo | Para qué |
|---|---|---|
| Versión semántica | `1.4.2`, `1.4`, `1` | Releases: los usuarios eligen cuánto se mueve |
| Commit | `sha-3f2a1c9` | Trazabilidad exacta: qué código hay en producción |
| Rama | `main`, `staging` | Entornos de prueba que siguen una rama |
| `latest` | `latest` | Comodidad para humanos; NUNCA en producción |

🧠 Concepto: **CI/CD** = Integración Continua (cada push compila y corre tests automáticamente) + Entrega/Despliegue Continuo (lo que pasa los tests se empaqueta y se despliega solo). Con Docker, el artefacto que viaja por el pipeline es la **imagen**.

```flujo
dir: abajo
git push -> GitHub Actions : dispara el workflow
GitHub Actions -> Tests : docker build --target test
Tests -> Build y push : ✅ pasan
Tests --> git push : ❌ fallan, avisa en el PR
Build y push -> GHCR : imagen sha-xxxx + versión
GHCR -> Servidor/PaaS : pull de la imagen nueva
```

### ✅ Ejemplo resuelto: workflow que construye, prueba y publica

Archivo `.github/workflows/docker.yml`:

```yaml
name: docker

on:
  push:
    branches: [main]
    tags: ["v*.*.*"]
  pull_request:

permissions:
  contents: read
  packages: write          # necesario para subir a ghcr.io

env:
  IMAGE: ghcr.io/${{ github.repository }}

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: docker/setup-qemu-action@v3      # emulación para construir linux/arm64
      - uses: docker/setup-buildx-action@v3

      - name: Login en GHCR
        if: github.event_name != 'pull_request'
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Etiquetas automáticas
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.IMAGE }}
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=sha

      - name: Tests dentro de la imagen
        uses: docker/build-push-action@v6
        with:
          context: ./api
          target: test         # requiere una etapa "test" en api/Dockerfile
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Construir y publicar
        uses: docker/build-push-action@v6
        with:
          context: ./api
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          platforms: linux/amd64,linux/arm64
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

Qué hace cada parte: `on` dispara en pushes a `main`, en tags `v1.2.3` y en PRs (en PRs construye y prueba pero **no publica**); `permissions` da al `GITHUB_TOKEN` permiso solo para subir paquetes (mínimo privilegio, sin tokens personales); `metadata-action` genera etiquetas como `main`, `1.2.3` y `sha-3f2a1c9`; `target: test` ejecuta la etapa de tests del Dockerfile multi-stage; `cache-from/cache-to: type=gha` guarda la caché de capas entre ejecuciones; `platforms` construye para x86 y ARM.

✅ Verificado en este PC: el YAML del workflow se parsea sin errores (con PyYAML). No se ejecutó en GitHub.

### 🚚 ¿Y cómo llega al servidor?

| Modelo | Cómo | Ejemplo |
|---|---|---|
| Push (el CI despliega) | El workflow entra por SSH y hace `docker compose pull && up -d` | VPS pequeño |
| Pull (el servidor vigila) | Watchtower, o un agente GitOps (Argo CD, Flux) detecta la imagen nueva | Kubernetes |
| PaaS | El PaaS recibe la imagen o el repo y despliega | Railway, Render, Fly.io, Cloud Run |

```bash
# Paso de despliegue típico en un VPS (lo ejecuta el CI por SSH)
cd /srv/tienda
export TAG=sha-3f2a1c9
docker compose pull api
docker compose up -d api          # recrea solo la API con la imagen nueva
docker image prune -f             # limpia imágenes viejas
```

💡 Consejo: despliega por **etiqueta de commit** (`sha-...`), no por `latest`. Para volver atrás (rollback) solo cambias `TAG` al commit anterior y vuelves a hacer `up -d`.

⚠️ Cuidado: los secretos del workflow van en **Settings → Secrets** del repo y se usan como `${{ secrets.NOMBRE }}`. Nunca en el YAML ni impresos con `echo` en los logs.

🇬🇧 **pipeline** /páip-láin/ = cadena de pasos · **workflow** /uórk-flóu/ = flujo de trabajo · **continuous integration** /kontíniuos integréishon/ = integración continua · **rollback** /róul-bak/ = volver a la versión anterior · **artifact** /ártifakt/ = artefacto

## 🦭 Docker vs Podman y alternativas

![Logo de Podman, la alternativa de Red Hat sin daemon (Wikimedia Commons)](img/docker/podman-logo.png)

**Podman** (de Red Hat) ejecuta las mismas imágenes OCI con casi los mismos comandos (`alias docker=podman` funciona en la mayoría de casos), pero con dos diferencias de diseño importantes: **no tiene daemon** y está pensado para correr **sin root** desde el principio.

::: columnas
### 🐳 Docker
- Arquitectura cliente → daemon (`dockerd`) que corre como root.
- Ecosistema enorme: Docker Desktop, Compose, Hub, Scout, documentación y tutoriales.
- Rootless existe, pero no es el modo por defecto.
- Docker Desktop es de pago para empresas grandes (desde 2021); el motor (Docker Engine) en Linux es libre.
::: siguiente
### 🦭 Podman
- Sin daemon: cada contenedor es un proceso hijo de tu comando (via `conmon`).
- Rootless por defecto: más seguro en servidores compartidos.
- Concepto de **pods** (como en Kubernetes) y `podman generate kube`.
- Se integra con systemd (Quadlet): contenedores como servicios.
- Compose vía `podman compose`; algunas funciones de Docker cambian o faltan.
:::

| Herramienta | Qué es | Cuándo |
|---|---|---|
| Docker Engine | El estándar en Linux | Por defecto: más tutoriales y compatibilidad |
| Docker Desktop | Docker con VM y GUI para Mac/Windows | Desarrollo en Mac/Windows (revisa la licencia) |
| Podman / Podman Desktop | Sin daemon, rootless | Servidores RHEL/Fedora, seguridad, systemd |
| OrbStack | Alternativa ligera en macOS | Mac: más rápida y ligera que Docker Desktop |
| Colima / Rancher Desktop | Alternativas libres en Mac | Si no quieres Docker Desktop |
| containerd + nerdctl | El runtime directo, CLI tipo docker | Nodos de Kubernetes, entornos mínimos |
| Buildah / Kaniko | Construir imágenes sin daemon | CI dentro de Kubernetes |

📌 Lo que aprendes con Docker vale para todos: Dockerfile (Podman lo llama también `Containerfile`), imágenes OCI, volúmenes, redes y registros son los mismos conceptos.

🇬🇧 **daemonless** /dímon-les/ = sin daemon · **drop-in replacement** /drop in ripléisment/ = reemplazo directo · **pod** /pod/ = vaina (grupo de contenedores) · **licensing** /láisensing/ = licencias

## ☸️ Kubernetes en simple (y cuándo NO necesitarlo)

![Logo de Kubernetes: un timón, porque "kubernetes" significa timonel en griego (Wikimedia Commons)](img/docker/kubernetes-logo.png)

Docker corre contenedores en **una** máquina. ¿Y si tienes 50 servidores, quieres 10 copias de tu API, que se reparta el tráfico, que si una se cae otra la reemplace y que al actualizar no haya caída? Eso es **orquestar**, y el estándar de facto es **Kubernetes** (K8s: K + 8 letras + s), creado por Google a partir de su sistema interno Borg y donado a la CNCF.

🧠 Concepto: Kubernetes es **declarativo**: no le dices "arranca 3 contenedores"; le dices "quiero que SIEMPRE haya 3 réplicas de esta imagen" y sus controladores trabajan en bucle para que la realidad coincida con lo declarado (si un nodo muere, recrea las réplicas en otro).

### 🧩 Las piezas mínimas

| Objeto | Qué es | Analogía |
|---|---|---|
| Node | Una máquina (VM o física) del clúster | Un edificio |
| Pod | Uno o más contenedores que comparten red y volúmenes; la unidad mínima | Un departamento |
| Deployment | Declara "N réplicas de este pod con esta imagen" y gestiona actualizaciones | El administrador que garantiza N departamentos ocupados |
| Service | IP y nombre DNS estables que reparten tráfico entre los pods | El número de teléfono fijo del edificio |
| Ingress / Gateway | Entrada HTTP(S) desde internet hacia los Services | La portería |
| ConfigMap / Secret | Configuración y secretos inyectados a los pods | Los avisos en el tablón / la caja fuerte |

```arbol
Clúster
  Plano de control
    API server
    etcd (estado deseado)
    scheduler
    controladores
  Nodo 1
    kubelet + containerd
    Pod api-7d4f (réplica 1)
    Pod api-9c2b (réplica 2)
  Nodo 2
    kubelet + containerd
    Pod api-1a8e (réplica 3)
    Pod postgres-0
```

```flujo
dir: abajo
Usuario -> Ingress : https://tienda.bo
Ingress -> Service api : tienda-api:80
Service api -> Pod 1 : reparte
Service api -> Pod 2 : reparte
Service api -> Pod 3 : reparte
```

Los pods son **desechables**: mueren, se mueven de nodo y cambian de IP. Por eso nunca se habla con un pod directamente, sino con el **Service**, que siempre tiene el mismo nombre.

### ✅ Ejemplo resuelto: Deployment + Service

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: tienda-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: tienda-api
  template:
    metadata:
      labels:
        app: tienda-api
    spec:
      containers:
        - name: api
          image: ghcr.io/yftorrezg/tienda-api:sha-3f2a1c9
          ports:
            - containerPort: 8000
          envFrom:
            - secretRef:
                name: tienda-secretos
          resources:
            requests: { cpu: "100m", memory: "128Mi" }
            limits: { memory: "512Mi" }
          readinessProbe:
            httpGet: { path: /health, port: 8000 }
          livenessProbe:
            httpGet: { path: /health, port: 8000 }
            initialDelaySeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: tienda-api
spec:
  selector:
    app: tienda-api
  ports:
    - port: 80
      targetPort: 8000
```

Qué hace cada parte: el Deployment pide 3 réplicas del pod etiquetado `app: tienda-api`; `requests` le dice al scheduler cuánto reservar y `limits` el máximo (cgroups); la **readinessProbe** decide si el pod recibe tráfico y la **livenessProbe** si hay que reiniciarlo; el Service selecciona los pods por la etiqueta y expone el puerto 80 apuntando al 8000. Para actualizar, cambias la imagen y Kubernetes hace un **rolling update**: sube pods nuevos y baja los viejos de a poco, sin caída.

- `kubectl apply -f k8s/` :: Aplica (crea o actualiza) lo declarado en los YAML
- `kubectl get pods -o wide` :: Pods, estado y en qué nodo están
- `kubectl logs -f deploy/tienda-api` :: Logs de un pod del deployment
- `kubectl describe pod tienda-api-7d4f` :: Eventos: por qué no arranca (`ImagePullBackOff`, `CrashLoopBackOff`)
- `kubectl rollout undo deploy/tienda-api` :: Volver a la versión anterior
- `kubectl scale deploy/tienda-api --replicas=5` :: Escalar a mano
- `kubectl port-forward svc/tienda-api 8000:80` :: Probar el Service desde tu PC
- `kind create cluster` :: Clúster de juguete dentro de Docker para practicar (también minikube, k3d)

### 🛑 Cuándo NO necesitas Kubernetes

Kubernetes resuelve problemas de **escala y de equipos grandes**, y cobra su precio en complejidad: redes, almacenamiento, certificados, actualizaciones del clúster, observabilidad, permisos (RBAC)... En un clúster gestionado, solo el plano de control ya cuesta dinero (en EKS de AWS, unos 70 USD/mes aprox. antes de pagar un solo nodo).

```flujo
dir: abajo
¿Un solo servidor basta? -> Docker Compose en un VPS : sí
¿Un solo servidor basta? -> ¿Quieres operar infraestructura? : no
¿Quieres operar infraestructura? -> PaaS o Cloud Run : no
¿Quieres operar infraestructura? -> ¿Muchos servicios y equipos? : sí
¿Muchos servicios y equipos? -> Kubernetes gestionado : sí
¿Muchos servicios y equipos? -> ECS / Nomad / PaaS : no
```

| Situación | Mejor opción |
|---|---|
| Proyecto personal, tesis, startup con pocos usuarios | Compose en un VPS o un PaaS |
| API que debe escalar a cero y crecer sola | Cloud Run, Azure Container Apps, Fly.io |
| Decenas de microservicios, varios equipos, multi-nube | Kubernetes gestionado (GKE, EKS, AKS) |
| Necesitas aprender K8s para el trabajo | `kind` o `k3s` en tu PC: practica sin pagar |

❌ Mal: "vamos a empezar el MVP con Kubernetes, microservicios y service mesh por si acaso escalamos". Muchos equipos pequeños pasan meses manteniendo infraestructura en vez de producto.

✅ Bien: empieza con un monolito en contenedor + Compose o PaaS; migra a un orquestador cuando duela de verdad (y entonces tus imágenes ya están listas: es la ventaja de haber usado Docker desde el principio).

🇬🇧 **orchestration** /orkestréishon/ = orquestación · **replica** /réplika/ = réplica · **rolling update** /róuling ápdeit/ = actualización gradual · **desired state** /disáierd stéit/ = estado deseado · **probe** /próub/ = sonda (chequeo) · **cluster** /kláster/ = clúster

## 🚀 Opciones de despliegue

No existe "el mejor" sitio: depende de qué despliegas (frontend estático, API, base de datos), cuánto tráfico, tu presupuesto y cuánto quieres administrar.

```capas
IaaS (VM / VPS) : tú gestionas SO, Docker, proxy, backups. Máximo control, más trabajo
CaaS (contenedores gestionados) : das la imagen; la nube la corre y escala (Cloud Run, Fargate)
PaaS : das el repo o la imagen; ellos hacen casi todo (Railway, Render, Fly.io)
Frontend / edge : das el frontend; CDN global + funciones (Vercel, Netlify, Cloudflare Pages)
```

### 🧭 Tabla de decisión

| Opción | Cuándo usarla | Costo aproximado (2025-2026) | Ojo con |
|---|---|---|---|
| VPS (Hetzner, DigitalOcean, Contabo...) + Compose | Control total, varios proyectos en una máquina, aprender | Desde ~4–6 USD/mes por VM pequeña | Tú haces seguridad, backups, HTTPS, actualizaciones |
| Railway | Prototipos y APIs con base de datos en minutos | Plan de pago desde ~5 USD/mes + uso | El costo crece con el uso; vigílalo |
| Render | Apps web y APIs con Postgres gestionado | Gratis con límites (se duerme sin tráfico); pago desde ~7 USD/mes | El plan gratis "despierta" lento |
| Fly.io | Contenedores cerca del usuario, varias regiones | Pago por uso; una máquina pequeña ~2–5 USD/mes | Más configuración (fly.toml) |
| Vercel / Netlify | Frontend (Next.js, React, Astro) y funciones serverless | Gratis para hobby; equipos ~19–20 USD/usuario/mes | No son para contenedores de larga duración ni WebSockets pesados |
| Cloudflare Pages/Workers | Frontend estático y lógica en el edge | Plan gratis generoso; pago desde ~5 USD/mes | Workers no son contenedores Docker clásicos |
| Google Cloud Run / Azure Container Apps | API en contenedor que escala a cero | Capa gratis mensual; luego por uso (céntimos con poco tráfico) | Arranque en frío; la base de datos va aparte |
| AWS (ECS Fargate, App Runner, EKS) | Empresas ya en AWS, requisitos de cumplimiento | Fargate por vCPU/GB-hora; EKS ~70 USD/mes solo el plano de control | Complejidad de IAM, red (VPC) y facturas sorpresa |
| Kubernetes gestionado (GKE, EKS, AKS) | Muchos servicios y equipos | Desde decenas a cientos de USD/mes | Necesitas alguien que lo opere |

📌 Precios **aproximados e indicativos**: cambian a menudo y dependen de la región. Revisa siempre la página de precios oficial antes de decidir y pon **alertas de presupuesto** en cualquier nube.

```grafica
tipo: barras
titulo: Costo mensual aproximado para una API pequeña (ilustrativo, USD)
unidad: USD
VPS pequeño + Compose : 6
Railway (uso bajo) : 5
Render (pago básico) : 7
Cloud Run (poco tráfico) : 1
EKS (solo plano de control) : 73
```

### ✅ Ejemplo resuelto: arquitectura típica de un proyecto estudiantil serio

```flujo
Usuario -> Vercel : frontend React/Next
Vercel -> API : fetch https://api.tienda.bo
API -> Postgres gestionado : Neon / Supabase / Render
API -> Redis : caché y colas
```

- Frontend en **Vercel o Netlify**: CDN global, previews por cada PR, HTTPS gratis.
- API en contenedor en **Railway, Render, Fly.io o Cloud Run** (la misma imagen que pruebas en local).
- Base de datos **gestionada** (Neon, Supabase, RDS...): backups y actualizaciones hechas por otros. Una base de datos en tu VPS sin backups es una bomba de tiempo.

### 🖥️ Si eliges VPS: lo mínimo indispensable

1. Usuario no root, acceso SSH solo con llave, firewall (y recuerda que Docker se salta UFW con `-p`).
2. Un **proxy inverso** con HTTPS automático delante: Caddy o Traefik (obtienen certificados de Let's Encrypt solos).
3. Solo el proxy publica puertos (80/443); API y base de datos sin `-p`, en la red interna.
4. `restart: unless-stopped` en todos los servicios y logs con rotación.
5. **Backups** automáticos de los volúmenes (`pg_dump` diario a otro sitio) y prueba de restauración.
6. Actualizaciones del SO y de las imágenes base (rebuild periódico).

```yaml
# Fragmento: Caddy como proxy con HTTPS automático delante de la API
services:
  caddy:
    image: caddy:2-alpine
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile:ro
      - caddy_data:/data
volumes:
  caddy_data:
```

```text
# Caddyfile
api.tienda.bo {
    reverse_proxy api:8000
}
```

🇬🇧 **deploy** /diplói/ = desplegar · **PaaS** /pas/ = plataforma como servicio · **scale to zero** /skéil tu sírou/ = escalar a cero · **reverse proxy** /rivérs próksi/ = proxy inverso · **managed** /mánachd/ = gestionado · **billing alert** /bíling alért/ = alerta de facturación

## 🏢 Casos reales, ecosistema y futuro

![Logo de Docker: la ballena Moby cargando contenedores (Wikimedia Commons)](img/docker/docker-logo.png)

### 🌍 Quién lo usa y para qué

- **Google**: todo corre en contenedores desde mucho antes de Docker (su sistema Borg). En 2014 dijeron que arrancaban del orden de **dos mil millones de contenedores por semana**; de esa experiencia nació Kubernetes.
- **OpenAI**: publicó en 2021 cómo escaló Kubernetes a **7.500 nodos** para entrenar e investigar modelos (incluyendo cargas con GPU).
- **Spotify**: pasó de su orquestador propio (Helios) a Kubernetes para sus servicios de backend.
- **CI de casi todo el mundo**: GitHub Actions, GitLab CI y similares ejecutan los trabajos en contenedores o con servicios en contenedores (Postgres de prueba, etc.).
- **IA y ciencia de datos**: imágenes con CUDA (`nvidia/cuda`), Jupyter (`jupyter/...`), servidores de inferencia como vLLM, Ollama o Text Generation Inference se distribuyen como imágenes Docker.
- **Desarrollo local**: Dev Containers (VS Code), Testcontainers (levanta bases reales en contenedores durante los tests en Java, Go, Python, Node...).

### 🧰 Mapa del ecosistema

| Necesidad | Herramientas |
|---|---|
| Construir imágenes | Docker/BuildKit, Buildah, Kaniko, ko (Go), Jib (Java), Cloud Native Buildpacks |
| Ejecutar | Docker, Podman, containerd, CRI-O |
| Orquestar | Kubernetes, Docker Swarm, Nomad, ECS |
| Empaquetar para K8s | Helm, Kustomize |
| GitOps | Argo CD, Flux |
| Seguridad | Trivy, Grype, Docker Scout, cosign, Falco |
| Desarrollo | Dev Containers, Tilt, Skaffold, Testcontainers, Compose Watch |

### 🚀 Hacia dónde va

🚀 Futuro: **imágenes mínimas y endurecidas por defecto** (distroless, Chainguard/Wolfi, Docker Hardened Images): la presión de la seguridad de la cadena de suministro hace que "imagen con cero CVEs conocidos" sea cada vez más el estándar exigido.

🚀 Futuro: **SBOM y firmas obligatorias**: regulaciones y clientes grandes piden saber qué hay dentro de cada imagen (SBOM) y quién la construyó (firmas con Sigstore/cosign, atestaciones de BuildKit).

🚀 Futuro: **contenedores para IA**: GPUs en contenedores (NVIDIA Container Toolkit, GPUs en Cloud Run), modelos empaquetados como artefactos OCI y sandboxes aislados (microVMs, gVisor) para que los agentes de IA ejecuten código de forma segura.

🚀 Futuro: **WebAssembly (Wasm)** como complemento de los contenedores para funciones muy ligeras y portables; convive con ellos (containerd puede ejecutar Wasm), no los reemplaza a corto plazo.

🚀 Futuro: **ARM en servidores** (AWS Graviton, Ampere, Mac con Apple Silicon): construir imágenes multi-arquitectura (`linux/amd64,linux/arm64`) pasa a ser lo normal.

```tiempo
2013 : docker run se vuelve popular
2015 : OCI y Kubernetes 1.0
2017 : Kubernetes gana la "guerra de orquestadores"
2021 : Log4Shell: escanear imágenes se vuelve obligatorio
2022 : dockershim fuera; containerd en todas partes
2024 : SBOM, firmas e imágenes endurecidas se generalizan
2026 : contenedores + GPUs + sandboxes para agentes de IA
```

🇬🇧 **ecosystem** /íkosistem/ = ecosistema · **supply chain security** /saplái chéin sekiúriti/ = seguridad de la cadena de suministro · **attestation** /atestéishon/ = atestación (prueba firmada) · **multi-arch** /múlti ark/ = multiarquitectura · **sandbox** /sánd-boks/ = caja de arena (entorno aislado)

## 🚨 Errores de otros programadores

Aprende de los golpes ajenos. Formato: **causa → consecuencia → cómo evitarlo**.

### 📰 Incidentes reales

| Incidente | Qué pasó | Lección |
|---|---|---|
| Tesla, 2018 | Investigadores (RedLock) encontraron una consola de Kubernetes de Tesla sin contraseña; los atacantes la usaban para minar criptomonedas y había credenciales de la nube en el clúster | Nunca paneles de administración públicos sin autenticación; secretos fuera de lugares accesibles |
| Docker Hub, 2019 | Acceso no autorizado a una base de datos con datos de unas 190.000 cuentas, incluidos tokens de GitHub/Bitbucket para builds automáticos | Tokens con permisos mínimos y rotación; asume que un tercero puede filtrarse |
| Codecov, 2021 | Un error en el proceso de creación de su imagen Docker permitió extraer una credencial; con ella modificaron su script de subida y robaron variables de entorno de los CI de sus clientes durante unos dos meses | Los secretos dentro de imágenes acaban saliendo; en CI, mínimos secretos y verifica lo que descargas |
| Log4Shell, 2021 | Vulnerabilidad crítica en Log4j presente en innumerables imágenes Java | Sin inventario (SBOM) y escaneo, no sabes qué imágenes parchear |
| Puertos 2375 abiertos (continuo) | APIs de Docker sin TLS expuestas a internet: bots las encuentran y lanzan mineros o botnets | Nunca expongas el daemon; acceso remoto solo por SSH (`DOCKER_HOST=ssh://...`) o TLS |

### 🧯 Errores típicos del día a día

| Error | Consecuencia | Cómo evitarlo |
|---|---|---|
| `COPY . .` sin `.dockerignore` | `.env`, `.git` y llaves dentro de la imagen publicada | `.dockerignore` desde el primer commit |
| Secretos en `ENV`/`ARG` | Cualquiera los lee con `docker history` | Secretos al ejecutar o `--mount=type=secret` |
| Usar `latest` en producción | Un día el despliegue trae otra versión y se rompe | Versión concreta o digest; etiqueta por commit |
| Datos de la base en la capa del contenedor | `docker rm` o `compose down -v` = datos perdidos | Volumen con nombre + backups probados |
| `docker compose down -v` "para limpiar" | Borra los volúmenes: la base de desarrollo (o peor) desaparece | Entiende `-v`; backups antes de limpiar |
| `docker system prune -a --volumes` a ciegas | Lo mismo, a escala de toda la máquina | Revisa `docker volume ls` antes |
| App escuchando en `127.0.0.1` | "El contenedor corre pero no responde" | Escuchar en `0.0.0.0` |
| `localhost` para hablar con otro contenedor | `connection refused` | Nombre del servicio (`db`, `redis`) |
| `-p 5432:5432` en un servidor | Base de datos expuesta a internet (Docker se salta UFW) | Sin `-p` o `127.0.0.1:` |
| Forma shell en CMD / `npm start` como PID 1 | `docker stop` tarda 10 s y mata a lo bruto; peticiones cortadas | Forma JSON, `node server.js`, o `--init` |
| Orden malo de capas | Builds de minutos en cada cambio | Dependencias antes que el código |
| `apt-get update` en otra capa | Instalaciones que fallan semanas después | update + install en el mismo `RUN` |
| Imagen construida en Mac M y desplegada en x86 | `exec format error` | `--platform linux/amd64` o multi-arch |
| Sin límites de memoria | Una fuga de memoria tumba todo el servidor | `-m` / `deploy.resources.limits` |
| Logs a archivos dentro del contenedor | Se llena el disco y no ves nada en `docker logs` | Logs a stdout/stderr + rotación |
| Una imagen por entorno (dev, prod) con código distinto | Lo que probaste no es lo que despliegas | Una imagen, distinta configuración |
| Kubernetes para un proyecto de 3 personas | Meses manteniendo infraestructura | Compose/PaaS hasta que haga falta |

::: columnas
### ❌ Dockerfile con 6 errores
```dockerfile
FROM python:latest
COPY . /app
RUN cd /app
RUN apt-get update
RUN apt-get install -y gcc
ENV API_KEY=sk-cambia_esto
RUN pip install -r /app/requirements.txt
CMD python /app/main.py
```
::: siguiente
### ✅ Corregido
```dockerfile
FROM python:3.12-slim
WORKDIR /app
RUN useradd -m -u 10001 app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=app:app . .
USER app
CMD ["python", "main.py"]
```
:::

::: desplegable 🔎 Los 6 errores del Dockerfile de la izquierda
1. `python:latest`: versión flotante y enorme (sin `-slim`).
2. `COPY . /app` antes de instalar: invalida la caché de `pip install` en cada cambio (y sin `.dockerignore` mete `.env` y `.git`).
3. `RUN cd /app`: no sirve, cada `RUN` es una shell nueva; se usa `WORKDIR`.
4. `apt-get update` y `install` en capas separadas, y `gcc` en la imagen final (si hace falta, en una etapa de build).
5. `ENV API_KEY=...`: secreto grabado en la imagen.
6. `CMD` en forma shell y ejecutando como root.
:::

💡 Consejo: pasa `hadolint` por tus Dockerfiles en CI: detecta automáticamente buena parte de estos errores.

🇬🇧 **postmortem** /póust-mórtem/ = análisis tras un incidente · **misconfiguration** /mis-konfiguréishon/ = mala configuración · **exposed** /ikspóusd/ = expuesto · **data loss** /déita los/ = pérdida de datos · **leak** /lík/ = fuga

## 🏋️ Ejercicios prácticos

Ordenados de fácil a difícil. Intenta cada uno antes de abrir la solución.

### 1️⃣ Tu primer contenedor útil

Sirve la carpeta actual por HTTP en el puerto 9000 con la imagen oficial de Python, sin instalar nada, y que el contenedor se borre al pararlo.

::: desplegable 🧩 Ver la solución
```bash
docker run --rm -p 9000:8000 -v "$PWD":/srv:ro -w /srv python:3.12-slim \
  python -m http.server 8000 --bind 0.0.0.0
```
`-p 9000:8000` publica el 8000 del contenedor en tu 9000; `-v ...:ro` monta la carpeta en solo lectura; `-w /srv` hace que el servidor sirva esa carpeta; `--bind 0.0.0.0` para que sea accesible desde fuera del contenedor. Abre `http://localhost:9000`.
:::

### 2️⃣ Ordena el Dockerfile

Reordena estas líneas para que la caché funcione bien: `COPY . .`, `FROM node:22-alpine`, `RUN npm ci --omit=dev`, `CMD ["node","server.js"]`, `WORKDIR /app`, `COPY package*.json ./`, `USER node`.

::: desplegable 🧩 Ver la solución
```dockerfile
FROM node:22-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev
COPY . .
USER node
CMD ["node", "server.js"]
```
Lo que cambia poco (base, dependencias) arriba; el código, que cambia en cada commit, abajo. `USER node` al final para que `npm ci` tenga permisos de escritura en `/app` (o usa `COPY --chown=node:node`).
:::

### 3️⃣ ¿Por qué no conecta?

Tu `compose.yaml` tiene los servicios `web` y `db`. En `web` pusiste `DATABASE_URL=postgresql://u:p@localhost:5432/app` y obtienes `connection refused`. Explica y corrige.

::: desplegable 🧩 Ver la solución
Dentro del contenedor `web`, `localhost` es el propio `web`, donde no hay Postgres. Compose crea una red con DNS en la que cada servicio se llama como su clave: usa `postgresql://u:p@db:5432/app`. Además añade a `web` un `depends_on: db: condition: service_healthy` con un healthcheck `pg_isready` en `db`, para no conectar antes de que Postgres esté listo.
:::

### 4️⃣ Adelgaza la imagen

Una API en Go se construye con `FROM golang:1.23` y `RUN go build -o /app/server .` y la imagen final pesa unos 900 MB. Llévala a menos de 30 MB.

::: desplegable 🧩 Ver la solución
```dockerfile
# syntax=docker/dockerfile:1
FROM golang:1.23 AS build
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
# Binario estático (sin depender de glibc)
RUN CGO_ENABLED=0 go build -ldflags="-s -w" -o /server .

FROM gcr.io/distroless/static-debian12:nonroot
COPY --from=build /server /server
USER nonroot
ENTRYPOINT ["/server"]
```
El compilador se queda en la etapa `build`; la final solo tiene el binario y lo mínimo (certificados, zona horaria, usuario `nonroot`). `-ldflags="-s -w"` quita símbolos de depuración. El tamaño queda típicamente en el rango de 10–25 MB según la app.
:::

### 5️⃣ Encuentra el secreto filtrado

Te pasan una imagen y sospechas que alguien dejó una clave dentro. ¿Cómo lo compruebas sin ejecutar la app?

::: desplegable 🧩 Ver la solución
```bash
docker history --no-trunc imagen:tag          # ENV/ARG y comandos RUN de cada capa
docker inspect -f '{{json .Config.Env}}' imagen:tag
trivy image --scanners secret imagen:tag      # busca claves, tokens y llaves en los archivos
docker run --rm --entrypoint sh imagen:tag -c 'ls -la /app; cat /app/.env 2>/dev/null'
```
Si encuentras algo: **rota** la clave (cámbiala en el servicio), corrige el Dockerfile y el `.dockerignore`, reconstruye y borra las etiquetas viejas del registro. Borrar el archivo en una capa nueva no sirve: sigue en las anteriores.
:::

### 6️⃣ Compose de desarrollo con recarga

Partiendo del `compose.yaml` de producción de la tienda, haz que en desarrollo el código se recargue al guardar y que puedas conectarte a Postgres desde DBeaver, sin tocar el archivo de producción.

::: desplegable 🧩 Ver la solución
Crea `compose.override.yaml` (compose lo mezcla solo al hacer `docker compose up`):
```yaml
services:
  api:
    command: ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
    volumes:
      - ./api/app:/app/app
  db:
    ports:
      - "127.0.0.1:5432:5432"
```
En producción ejecuta `docker compose -f compose.yaml up -d` para ignorar el override. Alternativa moderna sin bind mounts: una sección `develop: watch:` con `action: sync` y `docker compose watch`.
:::

### 7️⃣ Pipeline completo

Diseña los pasos de CI/CD para que: los PR solo construyan y prueben; un push a `main` publique `ghcr.io/tu/app:sha-<commit>`; y un tag `v1.2.0` publique también `1.2.0`. ¿Cómo harías rollback?

::: desplegable 🧩 Ver la solución
Es el workflow de la sección de CI/CD: `on: pull_request` + `push` a `main` + `tags: v*.*.*`; `push: ${{ github.event_name != 'pull_request' }}`; `metadata-action` con `type=sha` y `type=semver,pattern={{version}}`; `permissions: packages: write`. Rollback: desplegar de nuevo la etiqueta `sha-` anterior (en Compose: `TAG=sha-anterior docker compose up -d`; en Kubernetes: `kubectl rollout undo` o cambiar la imagen). Funciona porque las imágenes viejas siguen en el registro y son inmutables por digest.
:::

### 8️⃣ Reto: Kubernetes local

Con `kind`, despliega 3 réplicas de `nginx:1.27-alpine` detrás de un Service y comprueba que si borras un pod, aparece otro.

::: desplegable 🧩 Ver la solución
```bash
kind create cluster --name practica
kubectl create deployment web --image=nginx:1.27-alpine --replicas=3
kubectl expose deployment web --port=80
kubectl get pods                       # 3 pods Running
kubectl delete pod -l app=web --wait=false
kubectl get pods -w                    # aparecen pods nuevos: el Deployment repone las réplicas
kubectl port-forward svc/web 8080:80   # y abre http://localhost:8080
kind delete cluster --name practica
```
Esto demuestra el modelo **declarativo**: declaraste 3 réplicas y el controlador del Deployment las mantiene, pase lo que pase con cada pod.
:::

🇬🇧 **exercise** /éksersais/ = ejercicio · **hands-on** /jands on/ = práctico · **hot reload** /jot rilóud/ = recarga en caliente · **troubleshooting** /trábol-shúting/ = resolución de problemas

## 🎤 Preguntas de entrevista

::: desplegable ❓ ¿Qué diferencia hay entre un contenedor y una máquina virtual?
La VM virtualiza el hardware y trae su propio kernel y SO completo (GB, arranque lento, aislamiento fuerte). El contenedor es un proceso aislado con namespaces y limitado con cgroups que **comparte el kernel** del host (MB, arranque en segundos, aislamiento menor). En la nube se combinan: contenedores dentro de VMs.
:::

::: desplegable ❓ ¿Qué es una imagen y qué es una capa?
Una imagen es un sistema de archivos de solo lectura más metadatos (comando, variables, puertos), formado por una pila de capas. Cada instrucción que modifica archivos (`RUN`, `COPY`, `ADD`) crea una capa con los cambios. Las capas se comparten entre imágenes y se cachean; el contenedor añade una capa de escritura encima (copy-on-write).
:::

::: desplegable ❓ ¿Diferencia entre CMD y ENTRYPOINT? ¿Y RUN?
`RUN` se ejecuta al construir y deja su resultado en una capa. `CMD` es el comando por defecto al arrancar y se reemplaza con argumentos de `docker run`. `ENTRYPOINT` fija el ejecutable y lo de `CMD` (o lo que pases) se le añade como argumentos. Se recomienda la forma JSON para que el proceso sea PID 1 y reciba las señales.
:::

::: desplegable ❓ ¿Cómo reduces el tamaño de una imagen?
Base mínima (slim/alpine/distroless), multi-stage builds para dejar compiladores y devDependencies fuera, `.dockerignore`, limpiar cachés de apt/pip en el mismo `RUN`, `--no-install-recommends`, no meter datos ni modelos en la imagen, e inspeccionar capas con `docker history` o `dive`.
:::

::: desplegable ❓ ¿Volumen o bind mount?
Volumen: gestionado por Docker, portable, ideal para datos persistentes (bases de datos) en producción. Bind mount: una ruta concreta del host, ideal para desarrollo (editar código y verlo al instante) o para inyectar un archivo de configuración en solo lectura.
:::

::: desplegable ❓ ¿Cómo manejas secretos con Docker?
Nunca en la imagen (`ENV`, `ARG`, `COPY .env`). En build: `RUN --mount=type=secret`. En ejecución: variables inyectadas por el orquestador/PaaS, secretos de Compose/Swarm/Kubernetes montados como archivos, o un gestor (Vault, Secrets Manager). Si uno se filtra: rotarlo.
:::

::: desplegable ❓ ¿Por qué tu contenedor no debería correr como root?
Si un atacante explota la app, obtiene los permisos del proceso. Como root dentro del contenedor, cualquier fallo del kernel o mala configuración (socket de Docker montado, `--privileged`) le facilita escapar al host. Con `USER` no root, `--cap-drop ALL` y `no-new-privileges` se aplica el principio de mínimo privilegio.
:::

::: desplegable ❓ ¿Qué hace depends_on y por qué no basta?
Ordena el arranque de servicios en Compose. Sin condición solo espera a que el contenedor **arranque**; con `condition: service_healthy` espera a que su healthcheck pase. Aun así la app debe reintentar conexiones, porque las dependencias pueden reiniciarse en cualquier momento en producción.
:::

::: desplegable ❓ Explica Pod, Deployment y Service en Kubernetes
Pod: uno o más contenedores que comparten red y volúmenes; la unidad mínima y desechable. Deployment: declara cuántas réplicas de un pod quieres y gestiona las actualizaciones graduales y los rollbacks. Service: nombre DNS e IP estables que balancean el tráfico entre los pods que coinciden con su selector de etiquetas.
:::

::: desplegable ❓ ¿Cuándo NO usarías Kubernetes?
Cuando el sistema cabe en uno o pocos servidores, el equipo es pequeño o no hay nadie para operarlo. Compose en un VPS, un PaaS o Cloud Run dan el 90 % del valor con una fracción de la complejidad y del costo. Kubernetes compensa con muchos servicios, equipos, necesidades de autoescalado y alta disponibilidad.
:::

::: desplegable ❓ La imagen funciona en tu Mac M pero en el servidor da "exec format error". ¿Por qué?
La imagen se construyó para `linux/arm64` (Apple Silicon) y el servidor es `linux/amd64`. Solución: `docker buildx build --platform linux/amd64` o multi-arquitectura `--platform linux/amd64,linux/arm64`, normalmente en CI.
:::

::: desplegable ❓ ¿Qué pasa al hacer docker stop y por qué importa?
Docker envía SIGTERM al PID 1 y espera (10 s por defecto); si no termina, envía SIGKILL. Si tu app es PID 1 (forma JSON) y maneja SIGTERM, cierra conexiones y termina peticiones en curso (apagado ordenado). Si el PID 1 es una shell o npm que no reenvía señales, se corta todo a lo bruto tras 10 s. `docker run --init` añade un mini init (tini) que reenvía señales y recoge procesos zombis.
:::

🇬🇧 **"Walk me through..."** /uók mi zrú/ = "explícame paso a paso..." · **trade-off** /tréid-of/ = compromiso (ganas algo, pierdes algo) · **"It depends on..."** /it dipénds on/ = "depende de..." · **scalability** /skeilabíliti/ = escalabilidad

## 🇬🇧 Vocabulario y resumen final

| English | Suena | Español |
|---|---|---|
| container | /kontéiner/ | contenedor |
| image | /ímich/ | imagen |
| layer | /léier/ | capa |
| registry | /réyistri/ | registro (almacén de imágenes) |
| tag / digest | /tag/ /dáiyest/ | etiqueta / hash del contenido |
| build context | /bild kóntekst/ | contexto de construcción |
| multi-stage build | /múlti stéich bild/ | construcción en varias etapas |
| volume / bind mount | /vólium/ /báind máunt/ | volumen / montaje enlazado |
| port mapping | /port máping/ | publicación de puertos |
| healthcheck | /jélz-chek/ | chequeo de salud |
| orchestration | /orkestréishon/ | orquestación |
| rolling update | /róuling ápdeit/ | actualización gradual |
| rollback | /róul-bak/ | volver atrás |
| least privilege | /líst prívilech/ | mínimo privilegio |
| supply chain | /saplái chéin/ | cadena de suministro |
| ephemeral | /ifémeral/ | efímero |
| reverse proxy | /rivérs próksi/ | proxy inverso |
| scale to zero | /skéil tu sírou/ | escalar a cero |

🇬🇧 Frases útiles: "**It works on my machine, but not in the container**" = funciona en mi máquina pero no en el contenedor · "**The container keeps restarting**" = el contenedor se reinicia sin parar · "**We pinned the base image to a digest**" = fijamos la imagen base a un digest · "**Let's ship it as a Docker image**" = entreguémoslo como imagen Docker.

### 📌 La chuleta en una pantalla

```text
IMAGEN = plantilla (capas de solo lectura)   CONTENEDOR = imagen corriendo   REGISTRO = almacén
docker build -t app:1.0 .        construir           docker run -d -p 8000:8000 app:1.0   ejecutar
docker ps -a / logs -f / exec -it sh / inspect        depurar (en ese orden)
docker compose up -d --build / ps / logs -f / down    proyecto multi-servicio (down -v BORRA datos)

DOCKERFILE BUENO: FROM versión-slim → WORKDIR → COPY deps → RUN install → COPY código → USER → CMD JSON
CACHÉ: lo que cambia poco arriba, el código abajo · update+install+limpieza en un RUN · .dockerignore
MULTI-STAGE: compilar en una etapa, copiar solo el resultado (1 GB → 50-200 MB)
DATOS: volumen con nombre + backups · bind mount solo en desarrollo
REDES: servicios se llaman por NOMBRE · localhost = el propio contenedor · app en 0.0.0.0
SECRETOS: nunca ENV/ARG/COPY .env · --mount=type=secret · secretos del orquestador · rotar si se filtra
SEGURIDAD: no root · imagen mínima · escanear (trivy/scout) · sin -p para la BD · nunca 2375 público
DESPLIEGUE: VPS+Compose | PaaS (Railway/Render/Fly) | Vercel/Netlify (frontend) | Cloud Run | K8s si duele
```

📌 Resumen: Docker resuelve "en mi máquina funciona" empaquetando la app con su entorno en una **imagen** inmutable que corre igual en tu laptop, en CI y en producción. Domina el Dockerfile (orden de capas, multi-stage, usuario no root), Compose para varios servicios con healthchecks, y la disciplina de secretos y seguridad. Para desplegar, empieza simple (VPS con Compose o un PaaS) y sube a Kubernetes solo cuando tu escala y tu equipo lo justifiquen.
