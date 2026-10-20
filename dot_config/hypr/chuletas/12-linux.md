# 🐧 Linux · La terminal sin miedo
> Del kernel a tus scripts: archivos, permisos, procesos, texto, pacman, systemd, red y servidores, pensado para CachyOS + fish.

## 🐧 Qué es Linux y por qué existe

🧠 Concepto: **Linux** es, estrictamente, un **kernel** (núcleo): el programa que habla con el hardware y reparte CPU, memoria, discos y red entre los programas. Lo que instalas (CachyOS, Ubuntu, Fedora) es una **distribución**: kernel + herramientas GNU + gestor de paquetes + escritorio + configuración.

Antes de Linux, los sistemas Unix eran caros y cerrados, y MINIX (el Unix de enseñanza de Tanenbaum) no se podía modificar libremente. En 1991 un estudiante finlandés, **Linus Torvalds**, escribió su propio kernel "por hobby" y lo publicó con código abierto. El proyecto **GNU** (Richard Stallman, 1983) ya tenía casi todo lo demás: compilador `gcc`, shell `bash`, `ls`, `cp`, `grep`… Faltaba justo el kernel. Juntos formaron un sistema completo, libre y gratis.

![Tux, la mascota de Linux (dibujada por Larry Ewing en 1996). Fuente: Wikimedia Commons, «Tux.svg»](img/linux/tux.png)

### 🧱 Las capas: quién habla con quién

Cuando escribes `ls` en la terminal, tu orden baja por varias capas hasta el disco y la respuesta sube de vuelta. Entender estas capas explica casi todo: por qué existe `sudo`, por qué un programa "no tiene permiso", por qué la shell y el kernel son cosas distintas.

```capas
Apps : Brave, VS Code, Python, tus scripts — lo que usas
Shell : fish, bash, zsh — traduce lo que escribes en programas que se ejecutan
Bibliotecas : glibc, libssl… — funciones comunes; envuelven las llamadas al sistema
Llamadas al sistema : open, read, write, fork, execve — la única puerta al kernel
Kernel Linux : procesos, memoria, archivos, red, drivers — modo privilegiado
Hardware : CPU, RAM, SSD NVMe, GPU, Wi-Fi — lo físico
```

🧠 Concepto: **llamada al sistema** (system call, syscall) = petición que un programa hace al kernel ("ábreme este archivo", "crea un proceso"). Los programas normales corren en **modo usuario** y no pueden tocar el hardware directamente; solo el kernel corre en **modo kernel**.

```secuencia
actores: Tú, fish, ls, Kernel, Disco
Tú -> fish : escribes ls ~/Proyectos
fish -> Kernel : fork() + execve("/usr/bin/ls")
ls -> Kernel : openat() + getdents64()
Kernel -> Disco : lee el directorio (driver NVMe)
Disco --> Kernel : bloques de datos
Kernel --> ls : lista de nombres
ls --> Tú : imprime en la terminal (write)
```

💡 Consejo: puedes ver estas llamadas de verdad con `strace -f ls` (paquete strace). Es la mejor forma de entender qué hace un programa "por dentro".

### 🕰️ Historia en una línea de tiempo

```tiempo
1969 : Ken Thompson y Dennis Ritchie crean Unix en Bell Labs
1972 : Nace el lenguaje C; Unix se reescribe en C (1973)
1983 : Richard Stallman anuncia el proyecto GNU (software libre)
1987 : Andrew Tanenbaum publica MINIX para enseñar sistemas operativos
1991 : Linus Torvalds anuncia Linux (25 de agosto) en comp.os.minix
1992 : Linux pasa a licencia GPL; nacen las primeras distros
1993 : Nacen Debian y Slackware
1994 : Linux 1.0
2002 : Nace Arch Linux (Judd Vinet)
2004 : Primera versión de Ubuntu
2008 : Primer teléfono Android (kernel Linux)
2010 : Aparece systemd
2016 : WSL: Linux dentro de Windows
2017 : Los 500 supercomputadores del TOP500 usan Linux
2022 : Rust entra al kernel (Linux 6.1); Steam Deck con SteamOS (basado en Arch)
2026 : Tú, con CachyOS y Hyprland
```

![Ken Thompson (izquierda) y Dennis Ritchie, creadores de Unix y del lenguaje C. Foto de dominio público, Wikimedia Commons](img/linux/thompson-ritchie.jpg)

### 🌍 Dónde se usa (casos reales)

| Dónde | Ejemplo real | Por qué Linux |
|---|---|---|
| Servidores y nube | AWS, Google Cloud, Azure ofrecen sobre todo VMs Linux | gratis, estable, automatizable |
| Móviles | Android usa el kernel Linux | adaptable a cualquier hardware |
| Supercomputadores | 100 % del TOP500 desde noviembre de 2017 | rendimiento y control total |
| Contenedores | Docker y Kubernetes usan namespaces y cgroups del kernel | aislamiento ligero |
| Consolas y gaming | Steam Deck (SteamOS + Proton) | sin licencias, optimizable |
| Embebidos | routers, TVs, autos (Automotive Grade Linux) | pequeño y modificable |
| IA | entrenar modelos en GPUs NVIDIA/AMD, clusters | drivers, CUDA/ROCm, scripts |

📌 Resumen: como programador vas a desplegar casi todo en Linux (servidores, contenedores, CI). Dominar la terminal no es opcional: es el idioma de los servidores.

### 🆚 Linux frente a Windows y macOS

::: columnas
### 🐧 Linux
- Kernel libre (GPLv2), cientos de distros
- Todo es archivo; configuración en texto
- Terminal de primera clase
- Gratis, ideal para servidores y desarrollo
::: siguiente
### 🪟 Windows
- Cerrado, kernel NT
- Configuración en el Registro y paneles
- PowerShell potente; WSL para Linux
- Dominante en escritorio y juegos de PC
::: siguiente
### 🍎 macOS
- Basado en Darwin (Unix certificado, BSD)
- Terminal con zsh por defecto desde 2019
- Muy usado por desarrolladores
- Solo en hardware Apple
:::

🇬🇧 **kernel** /kérnel/ = núcleo · **distribution (distro)** /distribiúshon/ = distribución · **system call** /sístem col/ = llamada al sistema · **open source** /óupen sórs/ = código abierto · **user space** /iúser spéis/ = espacio de usuario

## 🧬 Distribuciones: ¿cuál y por qué?

🧠 Concepto: una **distro** decide tres cosas grandes: **qué gestor de paquetes** usa, **cada cuánto actualiza** (rolling release vs versiones fijas) y **qué trae por defecto** (escritorio, kernel, configuración).

```arbol
Linux (kernel)
  Familia Debian (.deb, apt)
    Debian
    Ubuntu
      Linux Mint
      Pop!_OS
  Familia Red Hat (.rpm, dnf)
    Fedora
    RHEL
      Rocky / AlmaLinux
  Familia Arch (pacman)
    Arch Linux
    CachyOS
    EndeavourOS
    SteamOS 3
  Independientes
    openSUSE (zypper)
    Alpine (apk, musl)
    NixOS (nix)
    Gentoo (compila todo)
```

![Logos de Arch Linux, Debian, Ubuntu y Fedora: las cuatro familias que más verás. Fuente: Wikimedia Commons](img/linux/logos-distros.png)

| Distro | Paquetes | Modelo | Ideal para |
|---|---|---|---|
| **Arch** | `pacman` + AUR | rolling | aprender a fondo, control total |
| **CachyOS** (la tuya) | `pacman` + paru | rolling | Arch optimizado: kernel y paquetes x86-64-v3 |
| **Debian** | `apt` (.deb) | estable cada ~2 años | servidores que no deben romperse |
| **Ubuntu** | `apt` + snap | LTS cada 2 años | servidores en la nube, principiantes |
| **Fedora** | `dnf` (.rpm) | cada ~6 meses | escritorio moderno, tecnología nueva |
| **RHEL / Rocky** | `dnf` | soporte ~10 años | empresas, bancos |
| **Alpine** | `apk` | estable | imágenes Docker diminutas |
| **NixOS** | `nix` | declarativo | sistemas reproducibles |

### 🔄 Rolling release vs versiones fijas

::: columnas
### 🌊 Rolling (Arch, CachyOS)
- Actualizas paquete a paquete, siempre lo último
- No hay "reinstalar para la versión 2"
- ✅ software nuevo (kernel, Mesa, Python) en días
- ⚠️ a veces algo se rompe: lee las noticias y ten snapshots
::: siguiente
### 🧊 Versiones fijas (Debian, Ubuntu LTS)
- Congelan versiones y solo aplican parches de seguridad
- Saltas de versión cada pocos años
- ✅ muy predecible: ideal para servidores
- ⚠️ software "viejo" (Python, Node) salvo que uses repos extra
:::

🧠 Concepto: **x86-64-v3** = nivel de CPU que asume instrucciones modernas (AVX2, etc.). CachyOS compila paquetes para ese nivel (repos `cachyos-v3`), por eso algunos programas rinden algo más que en Arch genérico. Lo comprobé en este PC:

```bash
grep -E "^\[" /etc/pacman.conf
```

```text
[options]
[cachyos-v3]
[cachyos-extra-v3]
[cachyos-core-v3]
[cachyos]
[core]
[extra]
[multilib]
```

📌 Resumen: el orden importa. pacman busca primero en `cachyos-v3`; si el paquete no está ahí, usa los repos normales de Arch (`core`, `extra`).

### 🎯 ¿Qué distro uso para qué?

| Situación | Elige | Por qué NO otra |
|---|---|---|
| Tu PC de estudio/desarrollo | CachyOS / Arch / Fedora | Debian estable te daría versiones viejas |
| VPS para tu API | Ubuntu LTS o Debian | Arch en servidor exige actualizar seguido |
| Imagen Docker pequeña | Alpine o `debian:slim` | Ubuntu completa pesa más |
| Empresa con soporte pagado | RHEL | sin contrato no hay a quién llamar |
| Laboratorio reproducible | NixOS | en las demás, cada máquina "deriva" |

⚠️ Cuidado: Alpine usa **musl** en vez de glibc. Algunos binarios (y ruedas de Python con código C) que funcionan en Ubuntu fallan en Alpine. Si tu imagen Docker de Python da errores raros, prueba `python:3.x-slim` (Debian).

🇬🇧 **rolling release** /róulin rilís/ = actualización continua · **LTS (Long Term Support)** /long term sapórt/ = soporte a largo plazo · **package manager** /pákech mánayer/ = gestor de paquetes · **upstream** /ápstrim/ = proyecto original

## 🐚 Shells: bash, zsh y fish

🧠 Concepto: la **shell** es el programa que lee lo que escribes, lo interpreta (variables, comodines, tuberías) y lanza los programas. La **terminal** (kitty, foot, Konsole) es solo la ventana que dibuja texto. Puedes cambiar de shell sin cambiar de terminal.

```flujo
Escribes -> Shell : texto
Shell -> Expande : variables, comodines, (comandos)
Expande -> Busca : en PATH o builtin
Busca -> Kernel : fork + exec
Kernel -> Programa : se ejecuta
Programa --> Shell : código de salida ($status)
```

En este PC hay tres instaladas (versiones reales):

```bash
fish --version; bash --version | head -1; zsh --version
```

```text
fish, versión 4.9.3
GNU bash, versión 5.3.20(1)-release (x86_64-pc-linux-gnu)
zsh 5.9.2 (x86_64-pc-linux-gnu)
```

| Shell | Fortaleza | Debilidad | Dónde la verás |
|---|---|---|---|
| **bash** | está en TODOS lados; estándar de scripts | interactiva sobria sin plugins | servidores, Docker, CI, tutoriales |
| **zsh** | compatible con bash casi siempre; muy configurable (oh-my-zsh) | lenta si cargas muchos plugins | macOS (por defecto desde 2019) |
| **fish** | sugerencias y colores sin configurar nada | NO es compatible con bash/POSIX | tu terminal diaria en CachyOS |
| **sh (dash)** | POSIX puro, muy rápida | pocas comodidades | `/bin/sh` en Debian/Ubuntu |

💡 Consejo: la regla de oro: **fish para escribir a mano, bash para scripts**. Un script con `#!/usr/bin/env bash` en la primera línea se ejecuta con bash aunque tu shell sea fish.

### 🔤 Diferencias de sintaxis que te van a morder

| Qué | bash / zsh | fish |
|---|---|---|
| asignar | `x=5` (sin espacios) | `set x 5` |
| exportar | `export EDITOR=nvim` | `set -gx EDITOR nvim` |
| borrar variable | `unset x` | `set -e x` |
| salida de comando | `$(date +%F)` | `(date +%F)` (también `$(...)` desde fish 3.4) |
| código de salida | `$?` | `$status` |
| argumentos | `$1`, `"$@"`, `$#` | `$argv[1]`, `$argv`, `(count $argv)` |
| if | `if [ -f x ]; then …; fi` | `if test -f x; …; end` |
| for | `for f in *.py; do …; done` | `for f in *.py; …; end` |
| función | `f() { …; }` | `function f; …; end` |
| PATH | `export PATH="$HOME/.local/bin:$PATH"` | `fish_add_path ~/.local/bin` |
| config | `~/.bashrc` / `~/.zshrc` | `~/.config/fish/config.fish` |
| repetir con sudo | `sudo !!` | `Alt+S` o escribe sudo y pulsa ↑ |

### ✅ Ejemplo resuelto: lo mismo en bash y en fish

Comprobado en este PC con `fish -c` y `bash -c`:

::: columnas
### 🟩 bash
```bash
nombre="mis notas.txt"
touch "$nombre"      # ¡comillas obligatorias!
hoy=$(date +%F)
lista=(a b c)
echo "${lista[1]}"   # b (empieza en 0)
for f in *.csv; do
  echo "archivo: $f"
done
```
::: siguiente
### 🐟 fish
```bash
set nombre "mis notas.txt"
touch $nombre        # fish NO parte variables
set hoy (date +%F)
set lista a b c
echo $lista[2]       # b (empieza en 1)
for f in *.csv
    echo "archivo: $f"
end
```
:::

🧠 Concepto: **word splitting** (división en palabras): en bash, una variable sin comillas se parte por los espacios. `ls $nombre` con `nombre="mis notas.txt"` busca dos archivos, `mis` y `notas.txt`. fish no hace eso: cada variable es una lista y no se parte nunca.

```text
$ bash -c 'nombre="mis notas.txt"; ls $nombre'
ls: no se puede acceder a 'mis': No existe el fichero o el directorio
ls: no se puede acceder a 'notas.txt': No existe el fichero o el directorio
```

### 🐟 Superpoderes de fish

- `→` o `Ctrl+F` :: Aceptar la sugerencia gris (sale de tu historial)
- `Alt+→` :: Aceptar solo la siguiente palabra de la sugerencia
- `Alt+S` :: Anteponer sudo al comando actual
- `Alt+E` :: Editar el comando en tu editor
- `Alt+H` :: Abrir el manual del comando que estás escribiendo
- `abbr -a gst 'git status -sb'` :: Abreviatura: escribes gst + espacio y se expande
- `funced mkcd; funcsave mkcd` :: Editar una función y guardarla para siempre
- `string replace -r '\.py$' '.bak' app.py` :: Herramientas de texto integradas (da app.bak)
- `math "2^10"` :: Calculadora integrada (da 1024)
- `type ls` :: ¿Es función, builtin o ejecutable? En tu fish, ls es una función que llama a eza
- `exec fish` :: Recargar la shell tras editar config.fish

### ⌨️ Atajos de la línea de comandos (bash, zsh y fish)

| Atajo | Acción |
|---|---|
| `Ctrl+A` / `Ctrl+E` | inicio / final de la línea |
| `Alt+B` / `Alt+F` | palabra atrás / adelante |
| `Ctrl+W` | borrar la palabra anterior |
| `Ctrl+U` / `Ctrl+K` | borrar hasta el inicio / el final |
| `Ctrl+R` | buscar en el historial |
| `Ctrl+L` | limpiar la pantalla |
| `Ctrl+C` | interrumpir el programa (señal SIGINT) |
| `Ctrl+D` | fin de entrada; en una línea vacía cierra la shell |
| `Ctrl+Z` | pausar el programa (vuelve con `fg`) |
| `Ctrl+Shift+C` / `Ctrl+Shift+V` | copiar / pegar en la terminal |
| `Alt+.` | pegar el último argumento del comando anterior |

### 🆘 Pedir ayuda sin salir de la terminal

- `man tar` :: Manual completo (`/` busca, `n` siguiente, `q` sale)
- `man -k comprimir` :: Buscar manuales por palabra clave
- `tldr tar` :: Ejemplos prácticos y cortos (instalado en este PC)
- `comando --help` :: Ayuda rápida de casi cualquier programa
- `help` :: En fish: abre la documentación de fish
- `type -a python` :: Todas las versiones de un comando en el PATH

📌 Resumen: en los manuales, `[opción]` entre corchetes es opcional, `<archivo>` es obligatorio y `...` significa "uno o más". La **Arch Wiki** es la mejor documentación de Linux que existe, sirve aunque no uses Arch.

⚠️ Cuidado: casi todo lo que copias de internet es bash. Si un `export X=1` o un `VAR=$(...)` falla en fish, tradúcelo con la tabla o ejecútalo con `bash -c '...'`.

🇬🇧 **shell** /shel/ = intérprete de comandos · **prompt** /prompt/ = indicador donde escribes · **builtin** /bíltin/ = orden integrada en la shell · **word splitting** /uérd splítin/ = división en palabras · **POSIX** /pósix/ = estándar común de los Unix

## 🗂️ El árbol de directorios

🧠 Concepto: en Linux hay **un solo árbol** que empieza en `/` (la raíz). No existen `C:` ni `D:`: los discos, USB y particiones se **montan** como carpetas dentro de ese árbol. El reparto de carpetas sigue el estándar **FHS** (Filesystem Hierarchy Standard).

```arbol
/
  boot (kernel y arranque)
  etc (configuración del sistema)
  home
    yafer (tu ~)
      .config
      .local/bin
  root (casa del admin)
  usr (programas)
    bin
    lib
    share
  var (datos que cambian)
    log
    cache
  tmp (temporales)
  dev (dispositivos)
  proc / sys (kernel en vivo)
  run (sesión actual)
  mnt / media (montajes)
  opt (apps de terceros)
```

| Carpeta | Qué guarda | Ejemplo real |
|---|---|---|
| `/etc` | configuración global (texto) | `/etc/pacman.conf`, `/etc/fstab`, `/etc/hosts` |
| `/usr/bin` | casi todos los ejecutables | `/usr/bin/git`, `/usr/bin/python` |
| `/usr/lib` | bibliotecas y módulos | `/usr/lib/libc.so.6` |
| `/var/log` | registros | `/var/log/pacman.log` |
| `/var/cache/pacman/pkg` | paquetes descargados | se llena con el tiempo |
| `/tmp` | temporales (en RAM, se borra al reiniciar) | sockets, descargas a medias |
| `/dev` | dispositivos como archivos | `/dev/nvme0n1`, `/dev/null` |
| `/proc` | info viva de procesos y kernel | `/proc/cpuinfo`, `/proc/loadavg` |
| `/boot` | kernel e initramfs | `vmlinuz-linux-cachyos` |
| `/run/media/yafer` | USB y discos montados por ti | tu disco `SuperYafer` |

### 🏠 Tu carpeta personal (lo que más tocas)

- `~` :: Tu casa: /home/yafer
- `~/.config/` :: Configuración de tus programas (hypr, fish, kitty, nvim)
- `~/.local/bin/` :: Tus scripts ejecutables (ya está en tu PATH)
- `~/.local/share/` :: Datos de apps (fuentes, papelera, apps .desktop)
- `~/.cache/` :: Cachés: se puede borrar para liberar espacio
- `~/.ssh/` :: Llaves SSH (permisos 700 en la carpeta, 600 en la llave privada)

🧠 Concepto: **"todo es un archivo"**: en Unix, discos (`/dev/sda`), procesos (`/proc/1234`), el generador aleatorio (`/dev/urandom`) y hasta "la nada" (`/dev/null`) se manejan como archivos. Por eso las mismas herramientas (`cat`, `>`, `|`) sirven para todo.

```bash
cat /proc/loadavg          # carga del sistema, leída como si fuera un archivo
```

```text
2.29 1.77 1.53 9/1487 974983
```

💡 Consejo: regla práctica: si es tuyo, vive en `~` y no necesita sudo. Si es del sistema, está en `/etc` o `/usr` y lo administra pacman: no lo edites a mano salvo en `/etc`.

⚠️ Cuidado: Linux distingue mayúsculas: `Foto.png` y `foto.png` son dos archivos distintos. Y los archivos que empiezan con punto (`.config`) están ocultos: `ls -a` los muestra.

🇬🇧 **root directory** /rut dairéktori/ = directorio raíz · **mount point** /máunt póint/ = punto de montaje · **hidden file** /jíden fáil/ = archivo oculto · **home directory** /jóum dairéktori/ = carpeta personal

## 🧭 Navegar y manipular archivos

La terminal siempre está "parada" en una carpeta: el **directorio de trabajo**. Cada comando que escribes actúa desde ahí, salvo que le des una ruta absoluta.

- `pwd` :: Mostrar en qué carpeta estás
- `ls -la` :: Lista larga con ocultos (permisos, dueño, tamaño, fecha)
- `ls -lh` :: Tamaños legibles (K, M, G)
- `ls -lt` :: Ordenar por fecha, lo más nuevo arriba
- `cd ~/Proyectos` :: Ir a una carpeta
- `cd ..` :: Subir un nivel
- `cd -` :: Volver a la carpeta anterior
- `cd` :: Volver a tu casa
- `z proy` :: zoxide: saltar a la carpeta más usada que contenga "proy"
- `eza -la --icons --git` :: ls moderno con iconos y estado de git (tu `ls` de fish ya lo usa)

| Ruta | Tipo | Significa |
|---|---|---|
| `/home/yafer/Proyectos` | absoluta | desde la raíz, funciona en cualquier lugar |
| `Proyectos/ia` | relativa | desde donde estás ahora |
| `.` | relativa | la carpeta actual |
| `..` | relativa | la carpeta padre |
| `~/Descargas` | absoluta | atajo de /home/yafer/Descargas |

### 🛠️ Crear, copiar, mover, borrar

- `mkdir -p api/src/rutas` :: Crear carpetas anidadas de una vez
- `touch notas.md` :: Crear archivo vacío (o actualizar su fecha)
- `cp -i a.txt b.txt` :: Copiar preguntando antes de sobrescribir
- `cp -r src/ respaldo/` :: Copiar una carpeta entera
- `cp -a src/ respaldo/` :: Copiar conservando permisos, fechas y enlaces
- `mv viejo.py nuevo.py` :: Renombrar
- `mv *.pdf ~/Documentos/` :: Mover varios
- `rm -i *.log` :: Borrar preguntando uno por uno
- `rm -r carpeta/` :: Borrar carpeta con todo (sin papelera)
- `trash-put archivo` :: Mandar a la papelera (paquete trash-cli)
- `ln -s ~/dotfiles/kitty ~/.config/kitty` :: Enlace simbólico (acceso directo)
- `file foto.png` :: Qué tipo de archivo es en realidad
- `stat app.py` :: Tamaño, permisos, dueño y fechas

### 🃏 Comodines (globbing)

🧠 Concepto: **globbing** = la SHELL (no el programa) expande los comodines a nombres de archivo antes de ejecutar. `rm *.log` llega a `rm` como `rm a.log b.log c.log`.

- `*.py` :: Cualquier texto: todos los .py de esta carpeta
- `foto?.png` :: Un solo carácter: foto1.png, fotoA.png
- `clase[1-3].md` :: Un carácter del rango
- `app.{py,bak}` :: Varias opciones (expansión de llaves): app.py app.bak
- `**/*.py` :: En fish (y bash con globstar): .py en todas las subcarpetas

### ✅ Ejemplo resuelto: armar un proyecto en un comando

```bash
mkdir -p ~/Proyectos/clasificador/{datos,src,notebooks,modelos}
cd ~/Proyectos/clasificador
touch src/{entrenar,evaluar}.py README.md
eza --tree
```

```text
.
├── datos
├── modelos
├── notebooks
├── README.md
└── src
    ├── entrenar.py
    └── evaluar.py
```

### 🔗 Enlaces duros vs simbólicos (e inodos)

🧠 Concepto: un **inodo** es la ficha del archivo en el disco (permisos, dueño, tamaño, dónde están los datos). El **nombre** del archivo es solo una entrada de directorio que apunta a un inodo.

::: columnas
### 🔗 Simbólico (`ln -s`)
- Es un archivo pequeño que guarda una RUTA
- Puede apuntar a carpetas y a otros discos
- Si borras el original, queda "roto"
- Lo que usa chezmoi y los dotfiles
::: siguiente
### 🧷 Duro (`ln`)
- Otro nombre para el MISMO inodo
- Solo archivos y en el mismo sistema de archivos
- El dato vive mientras quede un nombre
- `ls -li` muestra el número de inodo
:::

💡 Consejo: antes de un `rm` con comodines, escribe el mismo patrón con `ls` (o `echo`) para ver qué se borraría. `ls *.tmp` primero, `rm *.tmp` después.

⚠️ Cuidado: los nombres con espacios necesitan comillas: `cd "Mis Documentos"` o `cd Mis\ Documentos`. Mejor aún: no uses espacios en nombres de archivos de código.

🇬🇧 **working directory** /uérkin dairéktori/ = carpeta actual · **wildcard / glob** /uáildkard, glob/ = comodín · **symlink** /símlink/ = enlace simbólico · **inode** /áinoud/ = inodo · **recursive** /rikérsiv/ = recursivo

## 🔎 Ver y buscar: cat, less, find, grep, rg, fd

Dos preguntas distintas que se confunden: **¿dónde está el archivo?** (find, fd) y **¿qué archivo contiene este texto?** (grep, rg).

### 👀 Ver contenido

- `cat config.toml` :: Mostrar todo (para archivos cortos)
- `bat app.py` :: cat con colores y números de línea
- `less /var/log/pacman.log` :: Paginador: espacio avanza, `/texto` busca, `G` al final, `q` sale
- `head -n 20 datos.csv` :: Primeras 20 líneas
- `tail -n 50 app.log` :: Últimas 50 líneas
- `tail -f app.log` :: Seguir un archivo mientras crece (Ctrl+C sale)
- `wc -l datos.csv` :: Contar líneas (`-w` palabras, `-c` bytes)
- `diff -u viejo.conf nuevo.conf` :: Diferencias en formato "parche"

### 📂 Buscar archivos: find y fd

- `find . -name "*.py"` :: Por nombre (¡el patrón entre comillas!)
- `find ~ -iname "*tesis*"` :: Sin distinguir mayúsculas
- `find . -type d -name node_modules` :: Solo carpetas
- `find . -size +100M` :: Más de 100 MB
- `find . -mtime -1` :: Modificados en las últimas 24 h
- `find . -name "*.pyc" -delete` :: Buscar y borrar
- `find . -name "*.py" -exec wc -l {} +` :: Ejecutar un comando con todos los resultados
- `fd modelo` :: fd: nombres que contienen "modelo" (respeta .gitignore)
- `fd -e py` :: Por extensión
- `fd -H -t f config` :: Incluir ocultos, solo archivos
- `fd -e tmp -X rm` :: Pasar todos los resultados a un comando
- `locate pacman.conf` :: Instantáneo (base de datos de plocate, se actualiza con un timer diario)

### 📝 Buscar texto: grep y rg

- `grep -n "error" app.log` :: Líneas con "error" y su número
- `grep -i "error" app.log` :: Sin distinguir mayúsculas
- `grep -rn "def entrenar" src/` :: Recursivo
- `grep -v "DEBUG" app.log` :: Las que NO contienen DEBUG
- `grep -c " 200 " access.log` :: Contar coincidencias
- `grep -E "error|warn" app.log` :: Regex extendida: una u otra
- `grep -l "import torch" *.py` :: Solo nombres de archivo
- `rg "TODO"` :: ripgrep: busca en todo el proyecto, rapidísimo
- `rg -t py "import numpy"` :: Solo en archivos Python
- `rg -C 2 "timeout"` :: Con 2 líneas de contexto
- `rg -l "api_key"` :: ¿Qué archivos tienen api_key? (revisa secretos antes de un commit)

### ✅ Ejemplo resuelto: encontrar TODOs y funciones

Proyecto de prueba creado en el borrador y comandos ejecutados de verdad:

```bash
rg -n "TODO" proyecto
grep -rn "def normalizar" proyecto
fd -e py . proyecto
find proyecto -size +1M
```

```text
proyecto/src/prepro.py:2:# TODO: validar
proyecto/src/entrenar.py:2:    pass  # TODO
proyecto/src/prepro.py:3:def normalizar(x):
proyecto/src/entrenar.py
proyecto/src/prepro.py
proyecto/datos/grande.bin
```

### 🆚 Clásicos vs modernos

| Tarea | Clásico (siempre está) | Moderno (instálalo) | Diferencia clave |
|---|---|---|---|
| buscar archivos | `find` | `fd` | fd: sintaxis corta, ignora .gitignore y ocultos |
| buscar texto | `grep -rn` | `rg` | rg: multihilo, salta .git y binarios |
| ver archivo | `cat` / `less` | `bat` | colores, números, integración git |
| listar | `ls -la` | `eza` | iconos, árbol, estado git |
| saltar carpetas | `cd` | `zoxide` (`z`) | aprende tus carpetas frecuentes |
| elegir de una lista | ninguno | `fzf` | buscador difuso interactivo (Ctrl+T, Ctrl+R) |

💡 Consejo: en un servidor recién creado solo tendrás los clásicos. Aprende `find` y `grep` aunque uses `fd` y `rg` a diario: en una entrevista o un SSH de emergencia es lo que habrá.

⚠️ Cuidado: `find . -name *.py` sin comillas: si en la carpeta actual hay un `app.py`, la shell lo expande antes y find busca literalmente "app.py". Pon siempre el patrón entre comillas.

🇬🇧 **pattern** /pátern/ = patrón · **match** /mach/ = coincidencia · **case-insensitive** /kéis insénsitiv/ = sin distinguir mayúsculas · **regex** /réyex/ = expresión regular · **pager** /péiyer/ = paginador

## 🔒 Permisos y propietarios

🧠 Concepto: cada archivo tiene un **dueño** (user), un **grupo** (group) y permisos para tres clases de personas: **u** (dueño), **g** (grupo) y **o** (otros). Para cada una hay tres permisos: **r** leer, **w** escribir, **x** ejecutar.

¿Por qué existe esto? Linux nació **multiusuario**: muchas personas (y servicios como `nginx` o `postgres`) comparten la misma máquina. Los permisos impiden que un servicio comprometido lea tus llaves SSH o que un usuario borre lo de otro.

```text
$ ls -l saludo.sh
-rwxr-xr-x 1 yafer yafer 30 oct 19 16:44 saludo.sh
│└┬┘└┬┘└┬┘   └─┬─┘ └─┬─┘
│ │  │  │      │     └── grupo dueño
│ │  │  │      └──────── usuario dueño
│ │  │  └── otros:  r-x (leer y ejecutar)
│ │  └───── grupo:  r-x
│ └──────── dueño:  rwx (todo)
└────────── tipo: - archivo, d carpeta, l enlace
```

| Permiso | En un archivo | En una carpeta |
|---|---|---|
| `r` (4) | leer el contenido | listar los nombres (`ls`) |
| `w` (2) | modificarlo | crear, borrar y renombrar dentro |
| `x` (1) | ejecutarlo como programa | entrar (`cd`) y acceder a lo de dentro |

### 🔢 chmod en octal

Cada permiso vale un número: **r = 4, w = 2, x = 1**. Se suman por clase y se escriben tres cifras: dueño, grupo, otros.

| Octal | Letras | Suma | Uso típico |
|---|---|---|---|
| `7` | `rwx` | 4+2+1 | todo |
| `6` | `rw-` | 4+2 | leer y escribir |
| `5` | `r-x` | 4+1 | leer y ejecutar |
| `4` | `r--` | 4 | solo leer |
| `0` | `---` | 0 | nada |
| `755` | `rwxr-xr-x` | | scripts y carpetas |
| `644` | `rw-r--r--` | | archivos normales |
| `600` | `rw-------` | | llaves SSH, `.env` |
| `700` | `rwx------` | | `~/.ssh`, carpetas privadas |
| `640` | `rw-r-----` | | config legible por un grupo de servicio |

- `chmod +x deploy.sh` :: Dar ejecución a todos (u, g y o)
- `chmod u+x,g-w,o= archivo` :: Simbólico: dueño gana x, grupo pierde w, otros nada
- `chmod 644 notas.txt` :: Octal
- `chmod -R u+rwX,go-rwx privado/` :: Recursivo; X mayúscula = x solo en carpetas (y ya ejecutables)
- `chown yafer:yafer archivo` :: Cambiar dueño y grupo (sudo si no es tuyo)
- `stat -c '%A %a %U:%G %n' archivo` :: Ver permisos en letras y en octal
- `umask` :: Máscara que quita permisos a lo que creas (aquí 022)

### ✅ Ejemplo resuelto: "Permiso denegado" al ejecutar un script

Lo que pasó de verdad en este PC:

```bash
printf '#!/usr/bin/env bash\necho hola\n' > saludo.sh
ls -l saludo.sh
./saludo.sh
```

```text
-rw-r--r-- 1 yafer yafer 30 oct 19 16:44 saludo.sh
bash: línea 1: ./saludo.sh: Permiso denegado          ← en bash (código 126)
fish: Comando desconocido. ‘./saludo.sh’ existe pero no es un archivo ejecutable.   ← en fish
```

```bash
chmod +x saludo.sh && ls -l saludo.sh && ./saludo.sh
chmod 640 saludo.sh && stat -c '%A %a %U:%G %n' saludo.sh
```

```text
-rwxr-xr-x 1 yafer yafer 30 oct 19 16:44 saludo.sh
hola
-rw-r----- 640 yafer:yafer saludo.sh
```

### 🧮 umask: por qué lo nuevo nace con 644

🧠 Concepto: los archivos se crean pidiendo `666` y las carpetas `777`; la **umask** quita bits. Con umask `022` (la de este PC): 666 − 022 = **644** para archivos y 777 − 022 = **755** para carpetas. Lo comprobé con `touch nuevo.txt; mkdir nuevadir`.

::: desplegable 🔬 Avanzado: setuid, setgid y sticky bit
| Bit | Octal | Se ve como | Efecto | Ejemplo real |
|---|---|---|---|---|
| setuid | `4000` | `rws` en dueño | el programa corre con los permisos de su DUEÑO | `/usr/bin/passwd`, `/usr/bin/sudo` (dueño root) |
| setgid | `2000` | `rws` en grupo | en carpetas: lo nuevo hereda el grupo | carpetas compartidas de un equipo |
| sticky | `1000` | `rwt` en otros | en carpetas: solo el dueño borra sus archivos | `/tmp` es `1777` |

Por eso puedes cambiar tu contraseña con `passwd` aunque `/etc/shadow` solo lo escriba root: `passwd` tiene setuid root. Y por eso un binario setuid con un fallo es un objetivo jugoso para atacantes.

- `find / -perm -4000 -type f 2>/dev/null` :: Listar binarios setuid (auditoría)
- `chmod 1777 /compartido` :: Carpeta tipo /tmp (con sudo)
:::

### 🛡️ ACL y atributos (cuando rwx no alcanza)

- `getfacl archivo` :: Ver listas de control de acceso (permisos para usuarios concretos)
- `setfacl -m u:ana:r informe.pdf` :: Dar lectura solo a ana sin cambiar el grupo
- `lsattr archivo` :: Atributos especiales del sistema de archivos
- `chattr +i archivo` :: Inmutable: ni root lo borra hasta quitarlo (sudo)

⚠️ Cuidado: `chmod -R 777` "arregla" un "Permission denied" abriendo el archivo a cualquier usuario y proceso. En un servidor web significa que cualquier script comprometido puede reescribir tu código. Casi nunca es la respuesta: arregla el dueño (`chown`) o el grupo.

⚠️ Cuidado: SSH se niega a usar una llave privada con permisos abiertos ("UNPROTECTED PRIVATE KEY FILE!"). Solución: `chmod 600 ~/.ssh/id_ed25519` y `chmod 700 ~/.ssh`.

🇬🇧 **permission denied** /permíshon dináid/ = permiso denegado · **owner** /óuner/ = dueño · **read / write / execute** /rid, ráit, éksekiut/ = leer, escribir, ejecutar · **mode** /móud/ = modo (permisos) · **sticky bit** /stíki bit/ = bit pegajoso

## 👥 Usuarios, grupos y sudo

🧠 Concepto: **root** (UID 0) es el superusuario: el kernel no le aplica restricciones de permisos. **sudo** te deja ejecutar UN comando como root (o como otro usuario) tras comprobar que estás autorizado en `/etc/sudoers`, y deja registro de lo que hiciste.

¿Por qué no trabajar siempre como root? Porque cualquier error (un `rm` mal escrito, un script malicioso, un paquete con un bug) tendría poder total sobre el sistema. Con sudo, el poder es **puntual, explícito y registrado**: principio de **mínimo privilegio**.

```secuencia
actores: Tú, sudo, sudoers, Kernel
Tú -> sudo : sudo pacman -Syu
sudo -> sudoers : ¿yafer puede? (grupo wheel)
sudoers --> sudo : sí, pide contraseña
sudo -> Tú : [sudo] contraseña para yafer
Tú --> sudo : contraseña (de TU usuario)
sudo -> Kernel : ejecuta pacman como UID 0
nota sudo : queda registrado en el journal
```

### 🗃️ Dónde viven los usuarios

| Archivo | Contiene | ¿Quién lo lee? |
|---|---|---|
| `/etc/passwd` | usuario, UID, GID, casa, shell (sin contraseñas) | todos |
| `/etc/shadow` | hashes de contraseñas | solo root |
| `/etc/group` | grupos y sus miembros | todos |
| `/etc/sudoers` + `/etc/sudoers.d/` | quién puede usar sudo y cómo | solo root |

```text
yafer:x:1000:1000:Yafer:/home/yafer:/bin/fish
│     │ │    │    │     │           └── shell de inicio
│     │ │    │    │     └── carpeta personal
│     │ │    │    └── comentario (nombre)
│     │ │    └── GID del grupo principal
│     │ └── UID (los humanos empiezan en 1000)
│     └── x = la contraseña está en /etc/shadow
└── nombre de usuario
```

- `whoami` :: Tu usuario
- `id` :: Tu UID, GID y todos tus grupos
- `groups` :: Grupos a los que perteneces
- `getent passwd yafer` :: Tu línea en la base de usuarios
- `sudo useradd -m -s /bin/bash ana` :: Crear usuario con carpeta personal
- `sudo passwd ana` :: Ponerle contraseña
- `sudo usermod -aG docker yafer` :: Añadirte a un grupo (`-a` = añadir, ¡sin él te QUITA de los demás!)
- `newgrp docker` :: Activar el grupo nuevo sin cerrar sesión (o cierra sesión)
- `sudo userdel -r ana` :: Borrar usuario y su casa
- `sudo -l` :: Qué puedes hacer con sudo
- `sudo -i` :: Shell de root (úsala poco y sal con exit)
- `sudo -u postgres psql` :: Ejecutar como OTRO usuario (no root)
- `sudoedit /etc/hosts` :: Editar un archivo del sistema con TU editor, de forma segura
- `su - ana` :: Cambiar de usuario (pide la contraseña de ana)

### ✍️ Editar sudoers SIN romperlo

```bash
sudo EDITOR=nvim visudo                      # edita /etc/sudoers con chequeo de sintaxis
sudo visudo -f /etc/sudoers.d/10-yafer       # mejor: un archivo aparte
sudo visudo -c                               # solo comprobar que todo es válido
```

```text
# /etc/sudoers.d/10-yafer
%wheel ALL=(ALL:ALL) ALL                          # el grupo wheel puede todo (con contraseña)
yafer ALL=(root) NOPASSWD: /usr/bin/systemctl restart nginx   # SOLO ese comando sin contraseña
```

::: columnas
### ❌ Mal
- `sudo nano /etc/sudoers` y guardar con un error de sintaxis
- Resultado: sudo deja de funcionar para TODOS
- `yafer ALL=(ALL) NOPASSWD: ALL` "por comodidad"
- Cualquier proceso tuyo comprometido es root sin preguntar
::: siguiente
### ✅ Bien
- `visudo` revisa la sintaxis antes de guardar
- Archivos pequeños en `/etc/sudoers.d/`
- `NOPASSWD` solo para comandos concretos y con ruta absoluta
- Ten otra sesión de root abierta mientras pruebas
:::

💡 Consejo: si rompiste sudoers y sudo ya no funciona: en Arch arranca con el USB, monta la partición y usa `arch-chroot` para arreglarlo; en Ubuntu, `pkexec visudo` a veces salva el día.

⚠️ Cuidado: `sudo pip install`, `sudo npm install -g` o `sudo git clone` dentro de tu casa crean archivos de root en `~`. Luego tendrás "Permission denied" en tus propios proyectos. Arreglo: `sudo chown -R yafer:yafer ~/Proyectos`.

🇬🇧 **superuser** /súperiuser/ = superusuario · **least privilege** /list prívilech/ = mínimo privilegio · **wheel group** /uíl grup/ = grupo de administradores · **impersonate** /impérsoneit/ = actuar como otro usuario

## ⚙️ Procesos y señales

🧠 Concepto: un **proceso** es un programa en ejecución, con su memoria, su **PID** (identificador) y su **PPID** (el PID de su padre). Todos descienden del proceso 1 (`systemd`). Un programa es la receta; el proceso es la receta cocinándose.

Así nace cada comando que escribes: la shell se **clona** (`fork`) y el clon se **transforma** en el programa (`exec`). Por eso las variables exportadas se heredan: el hijo nace como copia del padre.

```flujo
dir: abajo
systemd PID 1 -> Hyprland
Hyprland -> kitty
kitty -> fish
fish -> fork : clona
fork -> exec : execve(python)
exec -> python entrenar.py
python entrenar.py --> fish : exit 0 (wait)
```

### 🔍 Ver procesos

- `ps aux` :: Todos los procesos (usuario, PID, %CPU, %MEM, comando)
- `ps -eo pid,comm,%mem --sort=-%mem | head` :: Los que más RAM usan
- `pgrep -a python` :: PID y comando de los procesos python
- `pstree -p` :: Árbol de procesos con PID
- `top` :: Monitor clásico (siempre está; `q` sale, `M` ordena por memoria)
- `htop` :: Monitor interactivo (F6 ordenar, F9 matar)
- `btop` :: Monitor bonito: CPU, RAM, red, discos (instalado aquí)
- `nvtop` :: GPU: memoria y procesos (útil al entrenar modelos)

Salida real de este PC (los que más memoria usaban):

```text
    PID COMMAND         %MEM
 920196 qemu-system-x86 34.0
 888752 electron         2.9
 923882 brave            2.3
```

### 🚦 Estados de un proceso

| Letra (`ps`) | Estado | Significa |
|---|---|---|
| `R` | running | ejecutándose o listo para CPU |
| `S` | sleeping | esperando algo (teclado, red): lo normal |
| `D` | disk sleep | esperando E/S, no se puede matar hasta que termine |
| `T` | stopped | pausado (Ctrl+Z o SIGSTOP) |
| `Z` | zombie | terminó pero su padre no recogió el resultado |

### 📡 Señales

🧠 Concepto: una **señal** es un aviso asíncrono que el kernel entrega a un proceso. Algunas se pueden capturar (el programa limpia antes de salir); `SIGKILL` y `SIGSTOP` no.

| Señal | Nº | Cómo se envía | Qué hace |
|---|---|---|---|
| `SIGINT` | 2 | `Ctrl+C` | interrumpir; el programa puede limpiar |
| `SIGTERM` | 15 | `kill PID` | pedir que termine (la educada, por defecto) |
| `SIGKILL` | 9 | `kill -9 PID` | matar sin opción a limpiar |
| `SIGHUP` | 1 | cerrar la terminal | colgar; muchos demonios lo usan para recargar config |
| `SIGTSTP` | 20 | `Ctrl+Z` | pausar desde el teclado |
| `SIGCONT` | 18 | `fg` / `bg` | reanudar |

- `kill 48213` :: Enviar SIGTERM (primero siempre esta)
- `kill -9 48213` :: SIGKILL, último recurso
- `pkill -f entrenar.py` :: Por patrón de la línea de comandos
- `killall firefox` :: Todos los procesos con ese nombre
- `kill -l` :: Listar todas las señales
- `hyprctl kill` :: Hyprland: clic en una ventana para matarla

### ✅ Ejemplo resuelto: códigos de salida al matar

Ejecutado de verdad con bash:

```bash
sleep 300 & kill -TERM $!; wait $!; echo "salió con $?"
sleep 300 & kill -9 $!;   wait $!; echo "salió con $?"
```

```text
salió con 143      ← 128 + 15 (SIGTERM)
salió con 137      ← 128 + 9  (SIGKILL)
```

📌 Resumen: cuando un proceso muere por una señal, la shell reporta **128 + número de señal**. 130 = Ctrl+C, 137 = matado con -9 (típico del **OOM killer** cuando se acaba la RAM, o de Docker al pasarse del límite de memoria), 143 = SIGTERM.

### 🎭 Primer y segundo plano (jobs)

- `comando &` :: Lanzar en segundo plano
- `Ctrl+Z` :: Pausar el que está en primer plano
- `jobs -l` :: Trabajos de ESTA terminal
- `bg` / `fg` :: Reanudar en segundo / primer plano
- `fg %2` :: Traer el trabajo 2
- `disown` :: Desligarlo de la terminal (sobrevive al cerrarla)
- `nohup python entrenar.py > log.txt 2>&1 &` :: Sigue aunque cierres la sesión SSH
- `nice -n 10 make -j8` :: Lanzar con menos prioridad
- `renice -n 10 -p 48213` :: Bajar prioridad a uno que ya corre
- `timeout 60 python script.py` :: Matarlo si tarda más de 60 s

### 🧹 trap: limpiar al recibir una señal

```bash
#!/usr/bin/env bash
tmp=$(mktemp -d)
trap 'echo "limpiando $tmp"; rm -rf "$tmp"' EXIT   # se ejecuta al salir, pase lo que pase
trap 'echo "interrumpido"; exit 130' INT TERM
# ... trabajo largo usando "$tmp" ...
```

💡 Consejo: para entrenamientos o servidores en una VM remota usa `tmux` (o `zellij`): el proceso vive dentro de una sesión a la que te reconectas. `nohup` sirve, pero no te deja volver a ver la pantalla.

⚠️ Cuidado: `kill -9` no deja al programa guardar ni cerrar archivos: puede corromper bases de datos (SQLite, Postgres) o checkpoints. Primero `kill`, espera unos segundos, y solo entonces `-9`.

🇬🇧 **process ID (PID)** /próses ai di/ = identificador de proceso · **signal** /sígnal/ = señal · **background / foreground** /bákgraund, fórgraund/ = segundo / primer plano · **zombie** /zómbi/ = zombi · **OOM killer** /ou ou em kíler/ = asesino por falta de memoria

## 🔗 Tuberías y redirecciones

🧠 Concepto: todo proceso nace con tres **descriptores de archivo**: **0 stdin** (entrada), **1 stdout** (salida normal) y **2 stderr** (errores). Las **redirecciones** (`>`, `<`, `2>`) los conectan a archivos; la **tubería** `|` conecta el stdout de un programa con el stdin del siguiente.

La filosofía Unix (Doug McIlroy): *"escribe programas que hagan una cosa y la hagan bien; que trabajen juntos; que manejen flujos de texto"*. Con 5 comandos pequeños resuelves lo que en otro sistema pediría un programa entero.

```flujo
Teclado -> cut : stdin 0
access.log -> cut : < archivo
cut -> sort : |
sort -> uniq -c : |
uniq -c -> Pantalla : stdout 1
cut --> errores.txt : 2> stderr
```

- `cmd > salida.txt` :: stdout a un archivo (lo SOBRESCRIBE)
- `cmd >> salida.txt` :: Añadir al final
- `cmd 2> errores.txt` :: Solo los errores
- `cmd > todo.txt 2>&1` :: Salida y errores al mismo archivo (el orden importa)
- `cmd &> todo.txt` :: Atajo de lo mismo (bash y fish)
- `cmd 2>/dev/null` :: Tirar los errores
- `cmd < entrada.txt` :: Archivo como entrada
- `cmd1 | cmd2` :: Tubería
- `cmd | tee copia.txt` :: Ver en pantalla Y guardar
- `cmd | xargs -n1 echo` :: Convertir líneas en argumentos
- `cmd1 && cmd2` :: cmd2 solo si cmd1 salió bien (código 0)
- `cmd1 || cmd2` :: cmd2 solo si cmd1 falló
- `cmd1; cmd2` :: Uno tras otro pase lo que pase
- `diff <(sort a.txt) <(sort b.txt)` :: Bash: sustitución de procesos (en fish: `diff (sort a.txt | psub) (sort b.txt | psub)`)
- `wl-copy < clave.pub` :: Copiar un archivo al portapapeles (Wayland)

### ✅ Ejemplo resuelto: separar salida y errores

Ejecutado en el borrador (`noexiste` no existe a propósito):

```bash
ls notas.csv noexiste > salida.txt 2> errores.txt
cat salida.txt; cat errores.txt
```

```text
notas.csv
ls: no se puede acceder a 'noexiste': No existe el fichero o el directorio
```

### 🧠 ¿Por qué `2>&1` va al final?

::: columnas
### ❌ `cmd 2>&1 > todo.txt`
1. 2>&1: stderr apunta a donde apunta stdout AHORA (la pantalla)
2. > todo.txt: stdout pasa al archivo
3. Los errores siguen saliendo en pantalla
::: siguiente
### ✅ `cmd > todo.txt 2>&1`
1. > todo.txt: stdout al archivo
2. 2>&1: stderr apunta a donde apunta stdout (el archivo)
3. Todo queda en todo.txt
:::

### 🔢 Códigos de salida

| Código | Significa | Ejemplo |
|---|---|---|
| `0` | éxito | todo bien |
| `1` | error general | `grep` sin coincidencias, `false` |
| `2` | mal uso del comando | opción inválida |
| `126` | no ejecutable | falta `chmod +x` |
| `127` | comando no encontrado | typo o no está en el PATH |
| `130` | Ctrl+C | 128 + 2 |
| `137` | matado con -9 / OOM | 128 + 9 |

⚠️ Cuidado: `sort datos.txt > datos.txt` deja el archivo VACÍO: la shell trunca `datos.txt` antes de que sort lo lea. Lo comprobé: el archivo quedó en 0 bytes. Usa `sort -o datos.txt datos.txt` o escribe a otro archivo y luego `mv`.

💡 Consejo: construye tuberías de a poco: ejecuta el primer comando, mira la salida, añade `| siguiente`, mira otra vez. Así depuras cada eslabón.

🇬🇧 **pipe** /páip/ = tubería · **standard input / output / error** /stándard ínput, áutput, érror/ = entrada, salida y error estándar · **redirect** /ridairékt/ = redirigir · **exit code** /éksit kóud/ = código de salida · **append** /apénd/ = añadir al final

## ✂️ Procesar texto: cut, sort, uniq, awk, sed, jq

En Linux los logs, CSV, configuraciones y respuestas de APIs son texto. Con estas herramientas respondes preguntas en segundos sin abrir Python. Todos los ejemplos de esta sección los ejecuté sobre archivos de prueba y la salida es la real.

| Herramienta | Piensa en ella como | Úsala para |
|---|---|---|
| `cut` | tijeras de columnas | sacar campos con un separador fijo |
| `sort` / `uniq` | ordenar y agrupar | rankings, quitar duplicados, contar |
| `tr` | cambiar caracteres | mayúsculas, separadores |
| `grep` | filtro de líneas | quedarte con lo que coincide |
| `sed` | editor de flujo | buscar y reemplazar, borrar líneas |
| `awk` | mini lenguaje de columnas | filtrar por condición, sumar, agrupar |
| `jq` | grep + awk para JSON | APIs, configuraciones, logs JSON |

### 📄 Datos de prueba

```text
# access.log (formato de nginx/Apache)
181.115.12.4 - - [19/Oct/2026:10:00:01 -0400] "GET /api/notas HTTP/1.1" 200 512
200.87.45.10 - - [19/Oct/2026:10:00:03 -0400] "GET /login HTTP/1.1" 200 1024
181.115.12.4 - - [19/Oct/2026:10:00:05 -0400] "POST /api/notas HTTP/1.1" 201 128
190.129.3.77 - - [19/Oct/2026:10:00:09 -0400] "GET /admin HTTP/1.1" 403 64
181.115.12.4 - - [19/Oct/2026:10:00:11 -0400] "GET /api/notas/7 HTTP/1.1" 404 32
200.87.45.10 - - [19/Oct/2026:10:00:15 -0400] "GET /api/notas HTTP/1.1" 500 16
181.115.12.4 - - [19/Oct/2026:10:00:20 -0400] "GET /api/notas HTTP/1.1" 200 512
```

Con espacios como separador: `$1` = IP, `$7` = ruta, `$9` = código HTTP, `$10` = bytes.

### ✅ Ejemplo resuelto 1: ranking de IPs (cut + sort + uniq)

```bash
cut -d' ' -f1 access.log | sort | uniq -c | sort -rn
```

```text
      4 181.115.12.4
      2 200.87.45.10
      1 190.129.3.77
```

1. `cut -d' ' -f1` saca la columna 1 (la IP).
2. `sort` pone juntas las IPs iguales (uniq solo cuenta repeticiones SEGUIDAS).
3. `uniq -c` cuenta cada grupo.
4. `sort -rn` ordena por número, de mayor a menor.

### ✅ Ejemplo resuelto 2: errores y bytes (awk)

🧠 Concepto: **awk** lee línea por línea, parte cada una en campos `$1, $2…` y ejecuta `patrón { acción }`. `NR` = número de línea, `NF` = número de campos, `-F,` cambia el separador, `END { }` corre al final.

```bash
awk '$9 >= 400 {print $1, $7, $9}' access.log                 # solo errores 4xx/5xx
awk '{b[$1]+=$10} END {for (ip in b) print ip, b[ip]}' access.log | sort -k2 -rn   # bytes por IP
```

```text
190.129.3.77 /admin 403
181.115.12.4 /api/notas/7 404
200.87.45.10 /api/notas 500
181.115.12.4 1184
200.87.45.10 1040
190.129.3.77 64
```

### ✅ Ejemplo resuelto 3: notas de un CSV

```text
# notas.csv
nombre,materia,nota
Ana,Calculo,78
Luis,Calculo,55
Ana,Fisica,91
Marta,Calculo,64
Luis,Fisica,49
Marta,Fisica,88
```

```bash
# promedio por alumno (NR>1 salta la cabecera)
awk -F, 'NR>1 {s[$1]+=$3; c[$1]++}
  END {for (n in s) printf "%s %.1f\n", n, s[n]/c[n]}' notas.csv | sort -k2 -rn
# reprobados (nota < 51)
awk -F, 'NR>1 && $3<51 {print $1" reprobó "$2" con "$3}' notas.csv
# top 3 notas
tail -n +2 notas.csv | sort -t, -k3 -rn | head -3
# materias sin repetir
tail -n +2 notas.csv | cut -d, -f2 | sort -u
```

```text
Ana 84.5
Marta 76.0
Luis 52.0
Luis reprobó Fisica con 49
Ana,Fisica,91
Marta,Fisica,88
Ana,Calculo,78
Calculo
Fisica
```

### ✅ Ejemplo resuelto 4: sed para editar sin abrir el archivo

🧠 Concepto: **sed** (stream editor) aplica órdenes a cada línea. La más usada: `s/buscar/reemplazar/g`. Con `-E` usas regex extendidas; con `-i` modifica el archivo en su sitio.

```bash
sed -i 's/^DEBUG=true/DEBUG=false/' .env.ejemplo                # cambiar un valor de config
sed -E 's/^([0-9]+\.[0-9]+)\.[0-9]+\.[0-9]+/\1.x.x/' access.log | head -2   # anonimizar IPs
sed -n '10,20p' app.log                                          # imprimir solo líneas 10 a 20
sed '/^#/d; /^$/d' nginx.conf                                    # quitar comentarios y líneas vacías
```

```text
PUERTO=3000
DEBUG=false
181.115.x.x - - [19/Oct/2026:10:00:01 -0400] "GET /api/notas HTTP/1.1" 200 512
200.87.x.x - - [19/Oct/2026:10:00:03 -0400] "GET /login HTTP/1.1" 200 1024
```

⚠️ Cuidado: `sed -i` no tiene deshacer. Prueba primero sin `-i` (solo imprime) o usa `sed -i.bak` para que deje una copia `.bak`. Y en macOS `sed -i` exige un argumento (`sed -i ''`), así que los scripts "portables" fallan allí.

### ✅ Ejemplo resuelto 5: jq con una respuesta de API

```text
# repos.json (estilo de la API de GitHub)
[
  {"name": "dotfiles", "stargazers_count": 12, "language": "Shell", "fork": false},
  {"name": "clasificador-iris", "stargazers_count": 3, "language": "Python", "fork": false},
  {"name": "awesome-linux", "stargazers_count": 0, "language": null, "fork": true},
  {"name": "api-notas", "stargazers_count": 7, "language": "TypeScript", "fork": false}
]
```

```bash
jq -r '.[].name' repos.json                                       # solo nombres
jq -r '.[] | select(.fork == false) | "\(.stargazers_count)\t\(.name)"' repos.json | sort -rn
jq '[.[].stargazers_count] | add' repos.json                      # total de estrellas
jq -c 'map({name, lang: (.language // "?")})' repos.json          # remodelar; // = valor por defecto
```

```text
dotfiles
clasificador-iris
awesome-linux
api-notas
12	dotfiles
7	api-notas
3	clasificador-iris
22
[{"name":"dotfiles","lang":"Shell"},{"name":"clasificador-iris","lang":"Python"},
 {"name":"awesome-linux","lang":"?"},{"name":"api-notas","lang":"TypeScript"}]
```

💡 Consejo: con una API real es igual: `curl -s https://api.github.com/users/USUARIO/repos | jq -r '.[].name'`. `-r` (raw) quita las comillas para seguir encadenando.

### 🔤 Otros imprescindibles

- `tr 'a-z' 'A-Z'` :: Mayúsculas ("Hola Mundo" → "HOLA MUNDO")
- `tr ' ' '\n' | sort | uniq -c | sort -rn` :: Frecuencia de palabras
- `sort -u` :: Ordenar quitando duplicados
- `sort -t, -k3 -n` :: Ordenar CSV por la 3.ª columna, numérico
- `sort -h` :: Ordenar tamaños humanos (1K, 2M, 3G)
- `paste -sd+ numeros.txt | bc` :: Sumar una columna de números
- `column -t -s,` :: Mostrar un CSV alineado como tabla
- `comm -12 a.txt b.txt` :: Líneas comunes a dos archivos ordenados
- `rev` / `tac` :: Invertir cada línea / invertir el orden de las líneas

::: desplegable 🤔 ¿Cuándo dejar awk y pasar a Python?
- **awk/sed/jq**: preguntas de una línea, en un servidor sin nada instalado, sobre datos "bien formados".
- **Python (pandas / polars)**: CSV con comillas y comas dentro de los campos, fechas, joins entre varios archivos, gráficas, o cuando el script pasa de ~10 líneas.
- `cut -d,` NO entiende comillas: con `"Pérez, Ana",90` parte mal. Para CSV de verdad: `python -c`, `mlr` (Miller), `xsv`/`qsv` o `duckdb`.
:::

🇬🇧 **field** /fild/ = campo · **delimiter** /delímiter/ = separador · **stream editor** /strim éditor/ = editor de flujo · **in-place** /in pléis/ = en el mismo archivo · **raw output** /ro áutput/ = salida en crudo

## 🌱 Variables de entorno y PATH

🧠 Concepto: las **variables de entorno** son pares `NOMBRE=valor` que un proceso hereda de su padre: idioma, editor, rutas, claves. **PATH** es la lista de carpetas donde la shell busca los ejecutables, en orden; gana la primera coincidencia.

```secuencia
actores: Tú, fish, PATH, Disco
Tú -> fish : escribes python
nota fish : ¿alias, función o builtin? no
fish -> PATH : ~/.local/bin/python?
PATH --> fish : no existe
fish -> PATH : /usr/local/bin/python?
PATH --> fish : no existe
fish -> Disco : /usr/bin/python
Disco --> fish : ¡encontrado! lo ejecuta
```

El PATH real de este PC (en fish es una lista; en bash, texto separado por `:`):

```text
fish → /home/yafer/.local/bin /usr/local/sbin /usr/local/bin /usr/bin /usr/bin/site_perl ...
bash → /home/yafer/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/usr/bin/site_perl:...
```

- `echo $PATH` :: Ver el PATH
- `env` o `printenv` :: Todas las variables de entorno
- `command -v python` :: Qué ejecutable se usaría (/usr/bin/python aquí)
- `type -a python` :: Todas las coincidencias en orden
- `MI_VAR=1 comando` :: Variable solo para ese comando (bash y fish)
- `env -i bash --norc` :: Shell con el entorno vacío (para probar)

| Acción | bash / zsh | fish |
|---|---|---|
| ver | `echo $HOME` | `echo $HOME` |
| crear local | `x=5` | `set x 5` |
| exportar | `export API_URL=http://localhost:8000` | `set -gx API_URL http://localhost:8000` |
| permanente | línea en `~/.bashrc` | `set -Ux` o línea en `config.fish` |
| añadir al PATH | `export PATH="$HOME/.local/bin:$PATH"` | `fish_add_path ~/.local/bin` |
| borrar | `unset x` | `set -e x` |

| Variable | Contiene | Valor aquí |
|---|---|---|
| `HOME` | tu carpeta | `/home/yafer` |
| `USER` | tu usuario | `yafer` |
| `SHELL` | shell de inicio | según la sesión |
| `LANG` | idioma y codificación | `es_BO.UTF-8` |
| `EDITOR` | editor por defecto | `nvim` (si lo defines) |
| `XDG_CURRENT_DESKTOP` | escritorio | `Hyprland` |
| `CUDA_VISIBLE_DEVICES` | GPUs visibles para PyTorch | `0` |

### ✅ Ejemplo resuelto: "command not found" tras instalar

Instalaste una herramienta con `pip install --user`, `cargo install` o `npm i -g` y la shell no la encuentra: el binario está en `~/.local/bin`, `~/.cargo/bin` o similar y esa carpeta no está en el PATH.

```bash
ls ~/.cargo/bin                  # 1. ¿dónde quedó el binario?
fish_add_path ~/.cargo/bin       # 2. fish: añadir (persistente, sin duplicados)
command -v ripgrep-all           # 3. comprobar
```

💡 Consejo: secretos (tokens, claves de API) en variables de entorno o en un `.env` listado en `.gitignore`, nunca en el código. En Python: `os.environ["API_KEY"]`.

⚠️ Cuidado: systemd, cron y los atajos de Hyprland NO leen tu `config.fish`: no conocen tu PATH personalizado ni tus abreviaturas. En scripts lanzados por ellos usa rutas absolutas.

⚠️ Cuidado: nunca pongas `.` (la carpeta actual) al inicio del PATH: un archivo malicioso llamado `ls` en una carpeta descargada se ejecutaría en lugar del real.

🇬🇧 **environment variable** /enváironment vériabol/ = variable de entorno · **export** /ekspórt/ = exportar · **lookup** /lúkap/ = búsqueda · **command not found** /kománd not fáund/ = orden no encontrada

## 📜 Scripts de bash (y su versión en fish)

🧠 Concepto: un **script** es un archivo de texto con comandos. La primera línea, el **shebang** (`#!/usr/bin/env bash`), le dice al kernel qué intérprete usar. Se escriben en bash (no en fish) porque bash está en cualquier servidor, contenedor y CI.

### 🛡️ La cabecera que todo script debería tener

```bash
#!/usr/bin/env bash
set -euo pipefail          # modo estricto
IFS=$'\n\t'                # (opcional) partir solo por saltos de línea y tabs
```

| Opción | Sin ella… | Con ella… |
|---|---|---|
| `-e` | el script sigue tras un error y hace destrozos | se detiene en el primer comando que falla |
| `-u` | una variable mal escrita vale "" en silencio | error: "variable sin asignar" |
| `-o pipefail` | una tubería con un comando que falla (`false` seguido de `true`) cuenta como éxito | la tubería falla si falla cualquier eslabón |

Comprobado en este PC:

```text
$ bash -c 'false | true; echo "sin pipefail: $?"'
sin pipefail: 0
$ bash -c 'set -o pipefail; false | true; echo "con pipefail: $?"'
con pipefail: 1
$ bash -c 'set -u; echo "$NO_DEFINIDA"'
bash: línea 1: NO_DEFINIDA: variable sin asignar
```

### 🧱 Lo esencial de la sintaxis

```bash
#!/usr/bin/env bash
set -euo pipefail

nombre="Yafer"                    # SIN espacios alrededor del =
hoy=$(date +%F)                   # salida de un comando
echo "Hola, $nombre: hoy es $hoy"

destino="${1:-$HOME/respaldos}"   # 1.er argumento o valor por defecto
: "${API_KEY:?Falta API_KEY}"     # aborta con mensaje si no está definida

if [[ -f "datos.csv" ]]; then     # [[ ]] es más seguro que [ ]
  echo "existe"
elif [[ -d "datos" ]]; then
  echo "es carpeta"
fi

for f in *.png; do                # comodín, sin ls
  echo "procesando $f"
done

while IFS= read -r linea; do      # leer un archivo línea a línea
  echo "> $linea"
done < lista.txt

saludar() {                       # función
  local quien="$1"                # variable local
  echo "Hola, $quien"
}
saludar "Mundo"
```

| Prueba `[[ ]]` | Verdadero si… |
|---|---|
| `-f ruta` / `-d ruta` / `-e ruta` | es archivo / es carpeta / existe |
| `-x ruta` | es ejecutable |
| `-z "$x"` / `-n "$x"` | cadena vacía / no vacía |
| `"$a" == "$b"` | cadenas iguales (`==` admite comodines a la derecha) |
| `$a -lt $b` | números: `-eq -ne -lt -le -gt -ge` (o usa `(( a < b ))`) |

### 🗨️ Comillas: la causa número 1 de bugs

::: columnas
### ❌ Sin comillas
```bash
archivo="mis datos.csv"
rm $archivo
# rm recibe "mis" y "datos.csv"
for f in $(ls *.txt); do …
# se rompe con espacios
```
::: siguiente
### ✅ Con comillas
```bash
archivo="mis datos.csv"
rm -- "$archivo"
# un solo argumento; -- = fin de opciones
for f in *.txt; do …
# el glob ya respeta espacios
```
:::

📌 Resumen: comillas dobles `"$x"` = expande variables pero no parte; comillas simples `'$x'` = texto literal; sin comillas = se parte y se expanden comodines. **Regla: siempre `"$var"` y `"$@"`.**

### ✅ Ejemplo resuelto: script de respaldo completo

```bash
#!/usr/bin/env bash
# respaldo.sh — uso: ./respaldo.sh [destino]
set -euo pipefail

ORIGEN="$HOME/Proyectos"
DESTINO="${1:-/run/media/$USER/SuperYafer/respaldos}"
FECHA=$(date +%F_%H-%M)
ARCHIVO="$DESTINO/proyectos_$FECHA.tar.zst"

log() { printf '[%s] %s\n' "$(date +%T)" "$*"; }

[[ -d "$DESTINO" ]] || { echo "❌ No existe $DESTINO (¿conectaste el disco?)" >&2; exit 1; }

log "Respaldando $ORIGEN → $ARCHIVO"
tar --zstd -cf "$ARCHIVO" \
    --exclude='.venv' --exclude='node_modules' --exclude='__pycache__' \
    -C "$HOME" Proyectos

log "Listo: $(du -h "$ARCHIVO" | cut -f1)"
find "$DESTINO" -name 'proyectos_*.tar.zst' -mtime +30 -print -delete   # rotación: 30 días
```

### 🐟 Lo mismo en fish (para funciones de tu terminal)

```bash
# ~/.config/fish/functions/respaldo.fish   (sintaxis fish)
function respaldo --description "Respalda ~/Proyectos" --argument-names destino
    set -q destino[1]; or set destino /run/media/$USER/SuperYafer/respaldos
    if not test -d $destino
        echo "❌ No existe $destino" >&2
        return 1
    end
    set archivo $destino/proyectos_(date +%F_%H-%M).tar.zst
    tar --zstd -cf $archivo --exclude=.venv --exclude=node_modules -C $HOME Proyectos
    and echo "Listo: "(du -h $archivo | cut -f1)
end
```

| Concepto | bash | fish |
|---|---|---|
| modo estricto | `set -euo pipefail` | no existe: comprueba `$status` o usa `; or return` |
| argumento por defecto | `${1:-valor}` | `set -q argv[1]; or set argv[1] valor` |
| variable local | `local x=1` | `set -l x 1` |
| devolver error | `return 1` / `exit 1` | `return 1` / `exit 1` |
| leer línea | `read -r linea` | `read linea` |
| aritmética | `$(( a + b ))` | `math $a + $b` |

### 🧰 Herramientas para escribir mejores scripts

- `bash -n script.sh` :: Solo revisar la sintaxis, sin ejecutar
- `bash -x script.sh` :: Ejecutar mostrando cada línea (depurar)
- `shellcheck script.sh` :: Linter que detecta comillas olvidadas y más (instálalo: `sudo pacman -S shellcheck`)
- `shfmt -w script.sh` :: Formatear el script
- `mktemp -d` :: Crear carpeta temporal segura (y bórrala con trap EXIT)

💡 Consejo: si tu script pasa de ~100 líneas, maneja JSON, o necesita estructuras de datos, pásate a Python. bash es pegamento, no un lenguaje para lógica compleja.

⚠️ Cuidado: `x = 5` con espacios NO asigna: bash busca un comando llamado `x` ("x: orden no encontrada", código 127). Lo comprobé.

🇬🇧 **shebang** /shibáng/ = línea #! inicial · **strict mode** /strikt móud/ = modo estricto · **quoting** /kuóutin/ = uso de comillas · **linter** /línter/ = analizador de estilo y errores · **unbound variable** /anbáund vériabol/ = variable sin asignar

## 📦 Paquetes: pacman, paru, apt y flatpak

🧠 Concepto: un **gestor de paquetes** instala programas desde **repositorios** firmados, resuelve sus **dependencias** (las bibliotecas que necesitan), los actualiza todos juntos y sabe qué archivo pertenece a qué paquete. Es la razón por la que en Linux casi nunca descargas un `.exe` de una web.

```flujo
dir: abajo
Tú -> pacman : sudo pacman -S btop
pacman -> Repos : descarga base de datos
Repos -> Firma : verifica con llaves GPG
Firma -> Dependencias : resuelve
Dependencias -> Instala : en /usr
Instala -> Hooks : actualiza caches, initramfs
```

En este PC (consultas sin sudo):

```bash
pacman -Q | wc -l          # paquetes instalados en total
pacman -Qe | wc -l         # instalados a mano (explícitos)
pacman -Qm | wc -l         # que no vienen de repos (AUR)
pacman -Qo /usr/bin/rg     # ¿qué paquete puso este archivo?
```

```text
1479
252
21
/usr/bin/rg está contenido en ripgrep 15.2.0-1
```

### 🧾 Tabla de equivalencias

| Quiero… | pacman / paru (Arch, CachyOS) | apt (Debian, Ubuntu) | dnf (Fedora) |
|---|---|---|---|
| actualizar todo | `sudo pacman -Syu` / `paru` | `sudo apt update && sudo apt upgrade` | `sudo dnf upgrade` |
| instalar | `sudo pacman -S htop` | `sudo apt install htop` | `sudo dnf install htop` |
| buscar | `pacman -Ss texto` | `apt search texto` | `dnf search texto` |
| info | `pacman -Si nombre` | `apt show nombre` | `dnf info nombre` |
| quitar con dependencias | `sudo pacman -Rns nombre` | `sudo apt autoremove --purge nombre` | `sudo dnf remove nombre` |
| ¿de qué paquete es? | `pacman -Qo /ruta` | `dpkg -S /ruta` | `rpm -qf /ruta` |
| archivos de un paquete | `pacman -Ql nombre` | `dpkg -L nombre` | `rpm -ql nombre` |
| huérfanos | `pacman -Qdtq` | `apt autoremove` | `dnf autoremove` |
| limpiar caché | `paccache -rk2` | `apt clean` | `dnf clean all` |

📌 Las letras de pacman: **S** = sync (repos), **Q** = query (instalado), **R** = remove. Modificadores: `y` refrescar bases, `u` actualizar, `s` buscar, `i` info, `n` sin respaldos de config, `s` (en -R) dependencias sin uso.

### 🧩 Formatos universales y otras fuentes

| Fuente | Qué es | Ventaja | Pega |
|---|---|---|---|
| **Repos oficiales** | paquetes de la distro | integrados, firmados, rápidos | puede no estar todo |
| **AUR** (paru) | recetas PKGBUILD de la comunidad | casi todo existe | cualquiera puede subir: léelas |
| **Flatpak** (Flathub) | apps de escritorio en sandbox | igual en todas las distros | más espacio, temas a veces raros |
| **Snap** | formato de Canonical | por defecto en Ubuntu | arranque más lento, tienda centralizada |
| **AppImage** | un archivo ejecutable | sin instalar | sin actualizaciones automáticas |
| **pip / npm / cargo** | paquetes de un lenguaje | lo último de cada librería | ¡en entornos virtuales, no en el sistema! |

- `paru -S visual-studio-code-bin` :: Instalar del AUR
- `paru -Gp nombre` :: Ver el PKGBUILD ANTES de instalar
- `paru -Qua` :: Actualizaciones pendientes del AUR
- `checkupdates` :: Ver qué se actualizaría sin tocar nada (pacman-contrib)
- `flatpak install flathub org.gimp.GIMP` :: Instalar una app de Flathub (flatpak no está instalado en este PC)
- `tail -n 30 /var/log/pacman.log` :: Qué se instaló o actualizó últimamente

### ✅ Ejemplo resuelto: preparar el PC para un proyecto de IA

```bash
sudo pacman -Syu                                 # 1. sistema al día (siempre primero)
sudo pacman -S python uv nvtop                   # 2. herramientas desde repos
paru -S visual-studio-code-bin                   # 3. lo que solo está en el AUR
uv venv && source .venv/bin/activate.fish        # 4. entorno virtual del proyecto (fish)
uv pip install torch numpy pandas                # 5. librerías DENTRO del venv
```

::: columnas
### ❌ Mal
- `sudo pacman -Sy paquete` (actualización parcial)
- `sudo pip install paquete` en el sistema
- Instalar del AUR sin leer el PKGBUILD
- Borrar con `-R` y dejar dependencias huérfanas
::: siguiente
### ✅ Bien
- Siempre `sudo pacman -Syu` antes de instalar
- `uv` / `venv` por proyecto, o `python-xxx` de pacman
- `paru -Gp` y revisar de dónde descarga
- `sudo pacman -Rns` y revisar `pacman -Qdt` cada tanto
:::

⚠️ Cuidado: la **actualización parcial** (`-Sy` sin `u`) no está soportada en Arch: refresca la lista de paquetes pero no actualiza el sistema, así que un paquete nuevo puede pedir bibliotecas más nuevas que las que tienes. Resultado típico: un programa que no arranca por "error while loading shared libraries".

💡 Consejo: antes de una actualización grande lee las noticias de archlinux.org. CachyOS trae Btrfs + snapper (en este PC hay un timer `snapper-cleanup.timer` y `limine-snapper-notify`): si algo se rompe puedes arrancar un snapshot anterior desde el menú de arranque.

🇬🇧 **package** /pákech/ = paquete · **dependency** /dipéndensi/ = dependencia · **partial upgrade** /párshal ápgreid/ = actualización parcial · **orphan** /órfan/ = huérfano · **sandbox** /sándbox/ = entorno aislado

## 🛎️ systemd: servicios, logs y timers

🧠 Concepto: **systemd** es el proceso 1 (PID 1): arranca el sistema y administra los **servicios** (demonios: red, ssh, docker, bases de datos). Cada cosa que gestiona es una **unit** descrita en un archivo de texto (`.service`, `.timer`, `.mount`, `.socket`).

```secuencia
actores: Firmware, Limine, Kernel, systemd, Servicios
Firmware -> Limine : UEFI carga el gestor de arranque
Limine -> Kernel : carga vmlinuz + initramfs
Kernel -> systemd : ejecuta /sbin/init (PID 1)
systemd -> Servicios : arranca units en paralelo
Servicios --> systemd : NetworkManager, sshd, docker listos
nota systemd : graphical.target = escritorio
```

📌 Resumen: **start** = arrancar AHORA; **enable** = arrancar en cada encendido. Son independientes: puedes tener un servicio habilitado pero parado, o corriendo pero no habilitado.

- `systemctl status nginx` :: Estado, PID, memoria y últimos logs
- `sudo systemctl start nginx` :: Arrancar ahora
- `sudo systemctl stop nginx` :: Parar
- `sudo systemctl restart nginx` :: Reiniciar
- `sudo systemctl reload nginx` :: Recargar config sin cortar conexiones
- `sudo systemctl enable --now docker` :: Habilitar y arrancar de una vez
- `sudo systemctl disable --now docker` :: Deshabilitar y parar
- `systemctl is-active NetworkManager` :: ¿Corre? (aquí: active)
- `systemctl is-enabled NetworkManager` :: ¿Arranca solo? (aquí: enabled)
- `systemctl --failed` :: Units que fallaron
- `sudo systemctl daemon-reload` :: Releer archivos tras editarlos
- `systemctl --user status pipewire` :: Servicios de TU usuario (sin sudo)
- `systemd-analyze blame` :: Qué hace lento el arranque
- `systemctl cat sshd` :: Ver el archivo de la unit

### 📜 journalctl: los logs

- `journalctl -u nginx -e` :: Logs de un servicio, saltando al final
- `journalctl -u nginx -f` :: Seguir en vivo
- `journalctl -b -p err` :: Errores desde el último arranque
- `journalctl -b -1 -p warning` :: Avisos del arranque ANTERIOR (si se colgó)
- `journalctl --since "1 hour ago"` :: Lo de la última hora
- `journalctl -k` :: Mensajes del kernel (como dmesg)
- `journalctl --user -u bot` :: Logs de un servicio de usuario
- `journalctl --disk-usage` :: Cuánto ocupan
- `sudo journalctl --vacuum-time=2weeks` :: Borrar los de más de 2 semanas

### ✅ Ejemplo resuelto: tu API como servicio de usuario

```text
# ~/.config/systemd/user/api-notas.service
[Unit]
Description=API de notas (FastAPI)
After=network-online.target

[Service]
WorkingDirectory=/home/yafer/Proyectos/api-notas
ExecStart=/home/yafer/Proyectos/api-notas/.venv/bin/uvicorn main:app --port 8000
Environment=ENTORNO=desarrollo
Restart=on-failure
RestartSec=3

[Install]
WantedBy=default.target
```

```bash
systemctl --user daemon-reload
systemctl --user enable --now api-notas
systemctl --user status api-notas
journalctl --user -u api-notas -f        # ver qué pasa si falla
```

⚠️ Cuidado: en `ExecStart` van rutas absolutas: systemd no lee tu `config.fish`, no conoce tu PATH ni tu venv activado. Y los servicios de usuario se paran al cerrar sesión salvo que actives `sudo loginctl enable-linger yafer`.

### ⏰ Timers de systemd vs cron

::: columnas
### 🕐 cron (clásico)
- Una línea: `0 21 * * * /ruta/respaldo.sh`
- Está en casi todo Unix
- Sin logs propios: redirige la salida
- Si el PC estaba apagado, la tarea se pierde
- En Arch hay que instalar `cronie`
::: siguiente
### ⏲️ systemd timer (recomendado en Arch)
- Dos archivos: `.service` (qué) y `.timer` (cuándo)
- Logs en journalctl, estado con systemctl
- `Persistent=true` recupera ejecuciones perdidas
- Dependencias, límites de CPU/RAM, aleatoriedad
- Este PC ya usa varios: logrotate, man-db, plocate…
:::

```text
# ~/.config/systemd/user/respaldo.timer   (+ respaldo.service con Type=oneshot)
[Unit]
Description=Respaldo diario a las 21:00

[Timer]
OnCalendar=*-*-* 21:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

| cron | OnCalendar equivalente | Significa |
|---|---|---|
| `0 21 * * *` | `*-*-* 21:00:00` | todos los días 21:00 |
| `*/15 * * * *` | `*:0/15` | cada 15 minutos |
| `0 8 * * 1` | `Mon *-*-* 08:00` | lunes 8:00 |
| `0 0 1 * *` | `monthly` | día 1 de cada mes |
| `@reboot` | `OnBootSec=1min` | al arrancar |

- `systemd-analyze calendar "Mon *-*-* 08:00"` :: Comprobar cuándo dispara (aquí: próximo lunes 08:00, "6 days left")
- `systemctl list-timers` :: Timers del sistema y cuándo tocan
- `systemctl --user enable --now respaldo.timer` :: Activar tu timer
- `systemctl --user start respaldo.service` :: Probar la tarea ya, sin esperar

⚠️ Cuidado: `crontab -r` BORRA todas tus tareas sin preguntar, y la `r` está al lado de la `e` (`crontab -e` = editar). Guarda una copia: `crontab -l > ~/crontab.bak`.

🇬🇧 **daemon** /dímon/ = demonio (proceso de fondo) · **unit** /iúnit/ = unidad · **enable** /enéibol/ = habilitar · **boot** /but/ = arranque · **schedule** /skéchul/ = programar en el tiempo · **linger** /língüer/ = quedarse (seguir tras cerrar sesión)

## 🌐 Redes: ip, ss, ping, dig, curl, ssh

🧠 Concepto: para que tu `curl https://api.github.com` funcione, pasan varias cosas: tu PC necesita una **IP** e **interfaz** activa, una **ruta** por defecto (el router), un **DNS** que traduzca el nombre a IP, y un **puerto** abierto en el servidor. Cada comando de esta sección revisa una de esas piezas.

```flujo
dir: abajo
¿Interfaz con IP? -> ¿Ruta al router? : ip -br a
¿Ruta al router? -> ¿Llego a internet? : ip r
¿Llego a internet? -> ¿Resuelve DNS? : ping 1.1.1.1
¿Resuelve DNS? -> ¿Responde el servicio? : dig dominio
¿Responde el servicio? -> Funciona : curl -I url
```

- `ip -br a` :: Interfaces e IPs en una línea cada una
- `ip r` :: Rutas (la "default via" es tu router)
- `nmcli device wifi list` :: Redes Wi-Fi
- `ping -c 4 1.1.1.1` :: ¿Hay conexión? (IP: no depende del DNS)
- `dig +short archlinux.org` :: Resolver un nombre (aquí devolvió 209.126.35.79)
- `resolvectl status` :: Qué DNS usa systemd-resolved
- `curl -I https://archlinux.org` :: Solo cabeceras: ¿responde y con qué código?
- `curl -sS https://api.github.com/users/torvalds | jq .name` :: Llamar a una API
- `curl -X POST -H "Content-Type: application/json" -d '{"texto":"hola"}' localhost:8000/notas` :: Probar tu API
- `curl -LO https://url/archivo.zip` :: Descargar conservando el nombre
- `ss -tulpn` :: Qué programas escuchan en qué puertos (`-p` muestra el proceso si es tuyo)
- `ss -tlnp 'sport = :8000'` :: ¿Quién usa el puerto 8000?
- `tracepath archlinux.org` :: Saltos hasta un servidor
- `python -m http.server 8000` :: Servidor web instantáneo de la carpeta actual

Salidas reales de este PC (resumidas):

```text
$ ip -br a
lo        UNKNOWN  127.0.0.1/8 ::1/128
enp2s0    UP       192.168.100.244/24 ...
wlan0     UP       192.168.100.63/24 ...
$ curl -sI https://archlinux.org | head -2
HTTP/2 200
server: nginx
$ ping -c 2 1.1.1.1 | tail -1
rtt min/avg/max/mdev = 59.519/59.604/59.689/0.085 ms
```

| Puerto | Servicio | Nota |
|---|---|---|
| `22` | SSH | el que más ataques automáticos recibe |
| `53` | DNS | aquí lo atiende systemd-resolved en 127.0.0.53 |
| `80` / `443` | HTTP / HTTPS | web |
| `5432` | PostgreSQL | nunca abierto a internet |
| `6379` | Redis | nunca abierto a internet |
| `3000` / `5173` / `8000` | dev servers (Node, Vite, FastAPI) | solo en localhost |

### 🔑 SSH y llaves

🧠 Concepto: **SSH** abre una shell cifrada en otra máquina. Con **llaves** (par pública/privada) no envías contraseña: el servidor guarda tu llave **pública** en `~/.ssh/authorized_keys` y te reta a demostrar que tienes la **privada**, que nunca sale de tu PC.

```secuencia
actores: Tu PC, Servidor
Tu PC -> Servidor : conecto como yafer
Servidor --> Tu PC : mi llave de host (¿la conoces?)
nota Tu PC : compara con ~/.ssh/known_hosts
Tu PC -> Servidor : quiero entrar con esta llave pública
Servidor --> Tu PC : reto: firma esto
Tu PC -> Servidor : firma hecha con la llave privada
Servidor --> Tu PC : firma válida, shell abierta
```

```bash
ssh-keygen -t ed25519 -C "yafer@laptop"      # crea ~/.ssh/id_ed25519 (privada) y .pub (pública)
ssh-copy-id yafer@203.0.113.10               # copia la pública al servidor
ssh yafer@203.0.113.10                       # entrar ya sin contraseña
```

```text
# ~/.ssh/config: alias para no escribir todo
Host vps
    HostName 203.0.113.10
    User yafer
    IdentityFile ~/.ssh/id_ed25519
```

- `ssh vps` :: Usar el alias
- `ssh -L 8888:localhost:8888 vps` :: Túnel: el Jupyter del servidor en tu localhost:8888
- `scp informe.pdf vps:~/` :: Copiar un archivo
- `scp -r vps:~/resultados ./` :: Traer una carpeta
- `rsync -avh --progress datos/ vps:~/datos/` :: Sincronizar (solo copia lo que cambió)
- `rsync -avhn --delete origen/ destino/` :: Simular (-n) un espejo exacto antes de hacerlo
- `ssh-keygen -R 203.0.113.10` :: Borrar la llave de host vieja (tras reinstalar el servidor)

⚠️ Cuidado: en rsync la barra final importa: `datos/` copia el CONTENIDO; `datos` (sin barra) copia la carpeta misma dentro del destino. Y `--delete` sin probar con `-n` puede borrar tu respaldo.

⚠️ Cuidado: si SSH grita "REMOTE HOST IDENTIFICATION HAS CHANGED!", no lo ignores a ciegas: o reinstalaste el servidor (entonces `ssh-keygen -R`), o alguien se está haciendo pasar por él.

🇬🇧 **network interface** /nétuerk ínterfeis/ = interfaz de red · **gateway** /guéituei/ = puerta de enlace · **port** /port/ = puerto · **listen** /lísen/ = escuchar · **key pair** /ki per/ = par de llaves · **tunnel** /tánel/ = túnel

## 💾 Discos, espacio y compresión

¿Cuánto me queda? ¿Qué carpeta se comió el disco? ¿Dónde está mi USB? Salidas reales de este PC:

```bash
lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS
df -h --output=source,fstype,size,used,avail,pcent,target /
```

```text
NAME          SIZE TYPE FSTYPE MOUNTPOINTS
sda           1,8T disk
└─sda1        1,8T part exfat  /mnt/backups
sdb           3,6T disk
└─sdb2        3,6T part ntfs   /run/media/yafer/SuperYafer
zram0        23,4G disk swap   [SWAP]
nvme0n1     931,5G disk
├─nvme0n1p1     4G part vfat   /boot
└─nvme0n1p2 927,5G part btrfs  /home  /  /var/log  /var/cache ...
S.ficheros     Tipo  Tamaño Usados  Disp Uso% Montado en
/dev/nvme0n1p2 btrfs   928G   589G  338G  64% /
```

🧠 Concepto: **Btrfs** permite **subvolúmenes** (por eso `/`, `/home`, `/var/log` salen del mismo `nvme0n1p2`) y **snapshots** instantáneos. **zram** es swap comprimida en RAM: más rápida que swap en disco.

- `df -h` :: Espacio libre por sistema de archivos
- `duf` :: df bonito (instalado aquí)
- `du -sh ~/Descargas` :: Cuánto ocupa una carpeta
- `du -h --max-depth=1 ~ | sort -rh | head` :: Las carpetas más pesadas de tu casa
- `ncdu ~` :: Explorador interactivo (instálalo: muy útil)
- `lsblk -f` :: Discos con sistema de archivos y UUID
- `findmnt` :: Qué está montado y dónde
- `udisksctl mount -b /dev/sdc1` :: Montar un USB sin sudo
- `sudo btrfs filesystem usage /` :: Uso real en Btrfs (df puede engañar con snapshots)
- `sudo smartctl -a /dev/nvme0n1` :: Salud del disco (smartmontools)

### ✅ Ejemplo resuelto: "No space left on device"

```bash
df -h /                                   # 1. confirmar que está lleno
du -h --max-depth=1 ~ 2>/dev/null | sort -rh | head   # 2. ¿qué carpeta?
du -sh ~/.cache/* | sort -rh | head -5    # 3. sospechosos: huggingface, pip, uv
sudo paccache -rk1                        # 4. caché de pacman: deja 1 versión
sudo journalctl --vacuum-size=200M        # 5. recortar logs
docker system prune                       # 6. si usas Docker: imágenes y capas viejas
```

Culpables típicos de un estudiante de IA: `~/.cache/huggingface`, `.venv` duplicados, checkpoints `.pt`, datasets descomprimidos dos veces y snapshots de Btrfs viejos.

### 🗜️ Comprimir y descomprimir

🧠 Concepto: **tar** junta muchos archivos en uno (empaqueta); **gzip/xz/zstd** lo comprimen. Por eso existen `.tar.gz`, `.tar.xz`, `.tar.zst`. `zip` empaqueta y comprime a la vez y es lo universal con Windows.

- `tar -czf proyecto.tar.gz proyecto/` :: Crear .tar.gz (c crear, z gzip, f archivo)
- `tar --zstd -cf respaldo.tar.zst carpeta/` :: Crear con zstd (rápido y muy bueno)
- `tar -xf archivo.tar.xz` :: Extraer (tar detecta el formato solo)
- `tar -xf datos.tar.gz -C ~/datos/` :: Extraer en otra carpeta
- `tar -tf archivo.tar.gz` :: Ver contenido sin extraer
- `zip -r tarea.zip tarea/` :: Crear zip
- `unzip -l tarea.zip` :: Ver contenido del zip
- `unzip tarea.zip -d tarea/` :: Extraer en una carpeta nueva
- `7z x archivo.7z` :: Extraer 7z
- `sha256sum ubuntu.iso` :: Verificar una descarga contra el hash publicado

Medí los compresores en este PC con 37,6 MB de textos de licencias de `/usr/share/licenses` (texto muy repetitivo, así que las diferencias se exageran):

```grafica
tipo: barras
titulo: Tamaño final al comprimir 37,6 MB de texto (medido en este PC, oct 2026)
unidad: MB
gzip -6 : 6.1
zstd -3 : 2.36
zstd -19 : 1.46
xz -6 : 1.41
```

```grafica
tipo: barras
titulo: Tiempo de compresión, 1 hilo (mismo archivo, medido en este PC)
unidad: ms
zstd -3 : 61
gzip -6 : 795
zstd -19 : 3512
xz -6 : 5167
```

| Formato | Velocidad | Compresión | Úsalo para |
|---|---|---|---|
| `.tar.gz` | buena | media | compatibilidad máxima |
| `.tar.zst` | muy rápida | muy buena | respaldos, datasets, paquetes de Arch |
| `.tar.xz` | lenta | máxima | distribuir archivos una vez, descargar muchas |
| `.zip` | buena | media | compartir con Windows, entregar tareas |

📌 Resumen: zstd es el equilibrio moderno: los paquetes de Arch se distribuyen como `.pkg.tar.zst`. Con un archivo de números (`seq 1 200000`, 1,3 MB) obtuve: gzip 429 KB, zstd 106 KB, xz 66 KB.

⚠️ Cuidado: `dd` y `mkfs` escriben directo en el disco. Si te equivocas de `/dev/sdX`, borras el disco equivocado (¡en este PC `sda` y `sdb` son tus respaldos!). Revisa `lsblk` dos veces antes de flashear un USB.

🇬🇧 **mount** /máunt/ = montar · **partition** /partíshon/ = partición · **filesystem** /fáilsistem/ = sistema de archivos · **archive** /árkaiv/ = archivo empaquetado · **compression ratio** /kompréshon réishio/ = tasa de compresión

## 📈 Rendimiento y diagnóstico

Cuando algo va lento, **mide antes de adivinar**. El método **USE** (de Brendan Gregg): para cada recurso (CPU, memoria, disco, red) mira **U**tilización, **S**aturación (cola de espera) y **E**rrores.

```flujo
dir: abajo
Va lento -> CPU : uptime, btop
Va lento -> Memoria : free -h
Va lento -> Disco : iostat, df
Va lento -> Red : ss, ping
CPU -> Culpable : ps --sort=-%cpu
Memoria -> Culpable : ps --sort=-%mem
Disco -> Culpable : iotop
```

- `uptime` :: Tiempo encendido y carga media de 1, 5 y 15 minutos
- `nproc` :: Núcleos (aquí 8): una carga sostenida mayor que esto = CPU saturada
- `free -h` :: RAM: mira la columna "disponible", no "libre"
- `btop` :: Todo en una pantalla
- `vmstat 1 5` :: CPU, memoria, swap y E/S cada segundo
- `iostat -xz 1` :: Uso de discos (paquete sysstat)
- `sudo iotop` :: Qué proceso escribe al disco
- `time python script.py` :: Cuánto tarda (real, user, sys)
- `hyperfine 'fd -e py' 'find . -name "*.py"'` :: Comparar comandos con estadística
- `strace -c ls` :: Resumen de llamadas al sistema de un programa
- `perf top` :: Qué funciones consumen CPU ahora mismo
- `journalctl -b -p err` :: Errores del arranque actual
- `sudo dmesg -w` :: Kernel en vivo: USB, GPU, discos, OOM
- `coredumpctl list` :: Programas que se estrellaron
- `lspci -k` / `lsusb` :: Hardware y driver en uso
- `inxi -Fxz` :: Resumen del hardware para pedir ayuda en foros

### ✅ Ejemplo resuelto: "Linux se comió mi RAM"

```text
$ free -h
               total       usado       libre  compartido   búf/caché  disponible
Mem:            23Gi        19Gi       450Mi       8,9Gi        13Gi       4,0Gi
Inter:          23Gi       2,1Gi        21Gi
```

Parece que solo quedan 450 MiB, pero no: Linux usa la RAM libre como **caché de disco** (13 GiB aquí) y la devuelve en cuanto un programa la pide. La cifra que importa es **disponible** (4 GiB). En este PC el culpable real era una máquina virtual (`qemu-system-x86` con 34 % de la memoria). "Inter" es el swap (zram).

🧠 Concepto: **carga media** (load average) = promedio de procesos ejecutándose o esperando CPU/disco. Con 8 núcleos, una carga de 2,29 (la que vi aquí) significa holgura; 8 sería al tope; 16 sería cola de espera.

::: desplegable 🔬 Avanzado: el OOM killer y los cgroups
Cuando la RAM y el swap se agotan, el kernel elige un proceso y lo mata (**OOM killer**). Verás `Out of memory: Killed process 1234 (python)` en `journalctl -k`, y el proceso sale con código 137. systemd-oomd (y en CachyOS a veces earlyoom/ananicy) actúan antes para que el escritorio no se congele.
Los **cgroups** (control groups) limitan CPU y RAM por grupo de procesos: es lo que usan Docker (`--memory=2g`) y systemd (`MemoryMax=2G` en un .service). Por eso un contenedor "muere sin error": llegó a su límite.
:::

💡 Consejo: al pedir ayuda, pega el comando exacto, el error completo y la salida de `inxi -Fxz` o `journalctl -b -p err`. "No funciona" no se puede depurar.

🇬🇧 **load average** /loud ávrech/ = carga media · **bottleneck** /bótelnek/ = cuello de botella · **throughput** /zrúput/ = rendimiento (volumen por segundo) · **latency** /léitensi/ = latencia · **profiling** /próufailin/ = perfilado

## 🛡️ Seguridad básica

Linux es seguro por diseño (usuarios separados, permisos, software firmado), pero la seguridad real depende de **hábitos**. Casi todos los ataques exitosos usan fallos ya parcheados, contraseñas débiles o servicios expuestos sin querer.

```capas
Actualizaciones : sudo pacman -Syu seguido; parches de kernel y OpenSSL
Firewall : solo los puertos que necesitas (ufw o firewalld)
Acceso : SSH con llaves, sin root, sin contraseñas
Mínimo privilegio : sudo puntual, servicios con su propio usuario
Secretos : .env fuera de git, permisos 600, gestor de contraseñas
Respaldos : regla 3-2-1, probados
```

- `sudo ufw default deny incoming` :: Firewall: bloquear lo que entra por defecto
- `sudo ufw allow ssh` :: Permitir solo SSH
- `sudo ufw enable && sudo ufw status verbose` :: Activar y revisar
- `ss -tulpn` :: Qué escucha y en qué dirección (0.0.0.0 = toda la red; 127.0.0.1 = solo tu PC)
- `last -n 10` :: Últimos inicios de sesión
- `journalctl -u sshd | rg "Failed password"` :: Intentos fallidos por SSH
- `sha256sum archivo.iso` :: Verificar descargas
- `gpg -c secreto.txt` :: Cifrar un archivo con contraseña
- `chmod 600 .env` :: Secretos legibles solo por ti

### 🔐 Endurecer SSH en un servidor

```text
# /etc/ssh/sshd_config  (o un archivo en /etc/ssh/sshd_config.d/)
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
```

```bash
sudo sshd -t && sudo systemctl reload sshd    # -t valida la config ANTES de recargar
```

⚠️ Cuidado: antes de poner `PasswordAuthentication no` o activar el firewall en un VPS, comprueba en OTRA terminal que puedes entrar con llave y que el puerto 22 está permitido. Si no, te quedas fuera de tu propio servidor.

| Hábito | Por qué |
|---|---|
| Actualizar al menos semanalmente | la mayoría de ataques usan fallos ya corregidos |
| Escuchar en `127.0.0.1`, no en `0.0.0.0` | tu servidor de desarrollo no debe verse en la red del café |
| Leer el PKGBUILD del AUR | cualquiera puede subir paquetes |
| No usar root ni `NOPASSWD: ALL` | un error o un malware tendría poder total |
| Secretos en `.env` + `.gitignore` | evitar filtrar claves a GitHub |
| Respaldos 3-2-1 | 3 copias, 2 medios distintos, 1 fuera de casa |

💡 Consejo: activa 2FA en GitHub y en tu correo; para un estudiante es lo que más protege. Y usa un gestor de contraseñas (KeePassXC, Bitwarden, `pass`).

🇬🇧 **firewall** /fáieruol/ = cortafuegos · **hardening** /járdenin/ = endurecimiento · **attack surface** /aták sérfis/ = superficie de ataque · **patch** /pach/ = parche · **brute force** /brut fors/ = fuerza bruta

## 💥 Errores famosos de otros programadores

Aprende de los desastres ajenos. Todos estos pasaron de verdad o son errores clásicos que se repiten cada semana en foros.

### 🧨 rm -rf con una variable vacía

```bash
# Así se ve el bug (simulado con echo en el borrador; NO lo ejecutes con rm)
CARPETA=$(cat ruta_que_no_existe.txt 2>/dev/null)   # falla en silencio → CARPETA=""
echo "Se ejecutaría: rm -rf $CARPETA/"
```

```text
Se ejecutaría: rm -rf /
```

- **Caso real, Steam para Linux (enero 2015)**: el script `steam.sh` hacía `rm -rf "$STEAMROOT/"*`. Si el usuario había movido la carpeta de Steam, `STEAMROOT` quedaba vacía y el comando se convertía en `rm -rf "/"*`: borró todos los archivos del usuario, incluidos discos externos montados.
- **Caso real, Bumblebee (2011)**: el script `install.sh` (rama de Ubuntu) tenía `rm -rf /usr /lib/nvidia-current/xorg/xorg`: un espacio de más convirtió "borrar una carpeta" en "borrar todo /usr".

✅ Bien: `set -u` + `${CARPETA:?}` aborta si la variable está vacía. Lo comprobé:

```text
$ bash seguro.sh                       # con "${CARPETA:?Falta la variable CARPETA}"
seguro.sh: línea 3: CARPETA: Falta la variable CARPETA
$ CARPETA=/tmp/demo bash seguro.sh
Se ejecutaría: rm -rf /tmp/demo/
```

### 🗄️ Borrar en el servidor equivocado

- **Caso real, GitLab.com (31 de enero de 2017)**: un ingeniero, cansado y de noche, ejecutó `rm -rf` sobre el directorio de datos de PostgreSQL pensando que estaba en la réplica secundaria, pero estaba en la **primaria**. Se perdieron unas 6 horas de datos de producción, y además descubrieron que varios mecanismos de respaldo no estaban funcionando. Lo documentaron públicamente en su post-mortem.
- **Caso real, Toy Story 2 (1998)**: un comando de borrado recursivo (suele citarse como `rm -rf *`) ejecutado en la carpeta equivocada eliminó cerca del 90 % de los archivos de la película, y los respaldos oficiales no funcionaban. Se salvó gracias a una copia (de una o dos semanas de antigüedad) en el equipo de casa de la directora técnica Galyn Susman.

✅ Bien: un prompt que muestre el host en color (rojo en producción), `hostname` antes de borrar, respaldos **probados** (restaurar de verdad, no solo "que exista el archivo").

### 📋 Tabla de errores clásicos

| Error | Causa | Consecuencia | Cómo evitarlo |
|---|---|---|---|
| `chmod -R 777` | "arreglar" un Permission denied | cualquiera escribe tu código o tus secretos | corrige dueño/grupo; 755/644/600 |
| `curl url | sh` sin leer | confiar ciegamente | ejecutas código ajeno (a veces con sudo) | descarga, lee, luego ejecuta |
| editar `/etc/sudoers` con nano | sin chequeo de sintaxis | sudo deja de funcionar | `visudo` / `visudo -c` |
| `sudo pacman -Sy paquete` | actualización parcial | bibliotecas incompatibles | siempre `-Syu` |
| `sort f > f` | la shell trunca antes de leer | archivo vacío | `sort -o f f` |
| `crontab -r` | tecla al lado de `-e` | pierdes todas tus tareas | `crontab -l > respaldo` |
| `dd of=/dev/sdb` equivocado | confundir discos | disco borrado | `lsblk` dos veces |
| `kill -9` de entrada | impaciencia | archivos o BD corruptos | primero `kill` (SIGTERM) |
| `usermod -G docker` sin `-a` | olvidar "append" | pierdes el grupo wheel (y sudo) | `usermod -aG` |
| cambiar `sshd_config` y salir | no probar | te quedas fuera del VPS | `sshd -t` y otra sesión abierta |

### 🐚 Más sustos clásicos

- **Fork bomb** (`:(){ :|:& };:`): Función que se llama a sí misma dos veces en segundo plano hasta agotar los procesos. Si un "truco" de internet se parece a esto, no lo pegues. Defensa: límites de procesos (`ulimit -u`, `TasksMax` de systemd).
- **Shellshock** (2014, CVE-2014-6271): Un fallo de bash ejecutaba código escondido en variables de entorno. Afectó servidores web con CGI. Lección: actualizar bash también importa.
- **Puerta trasera en xz-utils** (marzo 2024, CVE-2024-3094): Un colaborador que se ganó la confianza durante dos años metió código malicioso en el sistema de compilación de xz/liblzma, apuntando a sshd en algunas distros. Lo descubrió Andres Freund (Microsoft) al notar que las conexiones SSH iban más lentas de lo normal y gastaban CPU de más. Lección: la cadena de suministro también es superficie de ataque.
- **Malware en el AUR**: Se han encontrado paquetes del AUR modificados para descargar malware (por ejemplo `acroread` en 2018). Lección: lee el PKGBUILD, sobre todo de paquetes nuevos o que cambiaron de mantenedor.

### 🌍 curl | sh: ¿siempre malo?

::: columnas
### ❌ Peligroso
```bash
curl -fsSL https://sitio-raro.xyz/install | sudo bash
# código ajeno, como root, sin leerlo
```
::: siguiente
### ✅ Más seguro
```bash
curl -fsSLo install.sh https://sh.rustup.rs
less install.sh        # léelo
bash install.sh        # sin sudo si se puede
```
:::

📌 Resumen: el patrón se repite: **variables vacías, falta de comillas, sudo innecesario, no probar antes (`-n`, `--dry-run`, `echo`) y respaldos que nadie restauró nunca**.

🇬🇧 **post-mortem** /póust mórtem/ = análisis tras un incidente · **dry run** /drái ran/ = simulacro · **supply chain attack** /saplái chéin aták/ = ataque a la cadena de suministro · **backdoor** /bákdor/ = puerta trasera · **blast radius** /blast réidius/ = alcance del daño

## ☁️ WSL, servidores en la nube y el futuro

### 🪟 WSL: Linux dentro de Windows

🧠 Concepto: **WSL 2** (Windows Subsystem for Linux) ejecuta un **kernel Linux real** dentro de una máquina virtual ligera de Windows. Tienes Ubuntu (o Arch, Debian, Fedora…) con su terminal, sin arranque dual.

- `wsl --install` :: Instalar WSL con Ubuntu (en PowerShell como administrador)
- `wsl -l -v` :: Distros instaladas y versión de WSL
- `wsl --shutdown` :: Apagar la VM (libera RAM)
- `\\wsl$\Ubuntu\home\usuario` :: Tus archivos Linux vistos desde el Explorador de Windows
- `/mnt/c/Users/usuario` :: El disco C: visto desde Linux
- `code .` :: Abrir VS Code conectado a WSL

⚠️ Cuidado: trabaja tus proyectos DENTRO del sistema de archivos de Linux (`~/proyectos`), no en `/mnt/c/...`: cruzar entre Windows y Linux es mucho más lento (git, npm install) y da problemas de permisos y finales de línea (CRLF vs LF).

### 🖥️ Tu primer VPS: los primeros 10 minutos

Un **VPS** (servidor virtual: DigitalOcean, Hetzner, AWS EC2, Oracle Cloud…) suele traer Ubuntu o Debian y un usuario root. Receta segura:

1. Entra como root con la llave que te pidió el panel: `ssh root@IP`.
2. Actualiza: `apt update && apt upgrade -y`.
3. Crea tu usuario: `adduser yafer && usermod -aG sudo yafer`.
4. Copia tu llave: desde tu PC `ssh-copy-id yafer@IP` y prueba entrar en OTRA terminal.
5. Endurece SSH: `PermitRootLogin no`, `PasswordAuthentication no`, `sshd -t`, `systemctl reload ssh`.
6. Firewall: `ufw allow OpenSSH && ufw allow 80,443/tcp && ufw enable`.
7. Actualizaciones automáticas de seguridad: `apt install unattended-upgrades`.
8. Opcional: `fail2ban` para banear IPs que prueban contraseñas.
9. Despliega con Docker o un servicio systemd detrás de nginx/Caddy con HTTPS.

```capas
Internet : usuarios → DNS → IP pública
Firewall : solo 22, 80 y 443
Proxy inverso : nginx o Caddy — HTTPS, dominios
Tu app : servicio systemd o contenedor Docker en 127.0.0.1:8000
Datos : PostgreSQL solo en localhost + respaldos
Sistema : Ubuntu LTS / Debian, actualizaciones automáticas
```

| Servicio | Tipo | Cuándo |
|---|---|---|
| VPS (Hetzner, DigitalOcean) | una VM Linux para ti | aprender, proyectos personales, control total |
| AWS EC2 / Google Compute | VM en una nube grande | empresas, integrarse con otros servicios de la nube |
| PaaS (Vercel, Render, Fly.io) | subes código, ellos gestionan Linux | web/APIs sin administrar servidores |
| Kubernetes | muchos contenedores en muchos nodos | equipos grandes; demasiado para empezar |

### 🚀 Ecosistema y futuro

🚀 Futuro: **Rust en el kernel**: desde Linux 6.1 (diciembre 2022) se pueden escribir partes del kernel (sobre todo drivers) en Rust, por seguridad de memoria. Va creciendo driver a driver.

🚀 Futuro: **herramientas reescritas en Rust**: fish 4.0 (2025) se reescribió en Rust; `ripgrep`, `fd`, `bat`, `eza` y `zoxide` son Rust; Ubuntu 25.10 adoptó por defecto `sudo-rs` y los coreutils de uutils (también en Rust).

🚀 Futuro: **planificadores a medida (sched_ext)**: desde Linux 6.12 se pueden cargar planificadores de CPU como programas eBPF. CachyOS los aprovecha con los planificadores `scx` (por ejemplo, para juegos).

🚀 Futuro: **distros inmutables/atómicas**: Fedora Silverblue, SteamOS o NixOS tratan el sistema base como una imagen de solo lectura que se actualiza entera y se puede revertir; las apps van por Flatpak o contenedores.

🚀 Futuro: **eBPF** permite ejecutar programas verificados dentro del kernel para observabilidad, redes y seguridad sin escribir módulos; lo usan herramientas como Cilium y bpftrace.

🚀 Futuro: **Wayland** ya es el estándar en los escritorios principales (tú lo usas con Hyprland); X11 queda como compatibilidad vía XWayland.

🇬🇧 **virtual machine** /vérchual mashín/ = máquina virtual · **VPS (Virtual Private Server)** /vi pi es/ = servidor privado virtual · **reverse proxy** /rivérs próxi/ = proxy inverso · **immutable** /imiútabol/ = inmutable · **cloud provider** /kláud prováider/ = proveedor de nube

## 🏋️ Ejercicios prácticos

Hazlos en una carpeta de pruebas (`mkdir -p /tmp/practica && cd /tmp/practica`). Intenta resolverlos ANTES de abrir la solución. Las soluciones las ejecuté en este PC.

### 🟢 Nivel fácil

1. Crea `ej/a/x.txt`, `ej/a/y.txt` y `ej/b/z.log` con UN solo comando y luego lista solo los `.txt`.
2. Cambia los permisos de `p.txt` a "dueño todo, grupo leer y ejecutar, otros nada" y compruébalo en octal.

::: desplegable 🧩 Solución ejercicios 1 y 2
```bash
mkdir -p ej/{a,b} && touch ej/a/{x,y}.txt ej/b/z.log
find ej -name "*.txt" | sort

touch p.txt
chmod 750 p.txt             # u=rwx (7), g=r-x (5), o=--- (0)
stat -c '%A %a' p.txt
```

```text
ej/a/x.txt
ej/a/y.txt
-rwxr-x--- 750
```
:::

### 🟡 Nivel medio

3. Con el `access.log` de la sección de texto: ¿cuáles son las rutas más pedidas?
4. ¿Cuántas peticiones terminaron en error (códigos 4xx o 5xx)?
5. Renombra todos los `foto*.JPG` a `.jpg` sin repetir el nombre a mano.

::: desplegable 🧩 Solución ejercicios 3, 4 y 5
```bash
awk '{print $7}' access.log | sort | uniq -c | sort -rn | head -3
awk '$9 ~ /^[45]/' access.log | wc -l
for f in *.JPG; do mv -- "$f" "${f%.JPG}.jpg"; done
```

```text
      4 /api/notas
      1 /login
      1 /api/notas/7
3
foto1.jpg
foto2.jpg
```

`${f%.JPG}` quita el sufijo `.JPG` del valor de `f` (expansión de parámetros de bash). El `--` evita que un nombre que empiece por `-` se confunda con una opción.
:::

6. Escribe un script `contar.sh` que reciba una carpeta como argumento, falle con un mensaje claro si no se da o no existe, y muestre cuántos archivos `.py` hay (cuenta recursiva).

::: desplegable 🧩 Solución ejercicio 6
```bash
#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
    echo "Uso: $0 <carpeta>" >&2
    exit 2
fi
carpeta="$1"
[[ -d "$carpeta" ]] || { echo "No existe la carpeta: $carpeta" >&2; exit 1; }

total=$(find "$carpeta" -name '*.py' -type f | wc -l)
echo "$total archivos .py en $carpeta"
```

Con `shellcheck contar.sh` no debería dar avisos. Código 2 = mal uso; código 1 = error de ejecución.
:::

### 🔴 Nivel difícil

7. Cada noche a las 03:30 quieres ejecutar `~/.local/bin/respaldo.sh` con un **timer de systemd de usuario**, que se recupere si el PC estaba apagado. Escribe los dos archivos y los comandos para activarlo y comprobarlo.
8. Un servidor de desarrollo dice `Address already in use` en el puerto 8000. Encuentra qué proceso lo usa y ciérralo de forma educada. Explica por qué no empiezas con `kill -9`.
9. Un VPS nuevo tiene solo root con contraseña. Enumera, en orden, qué haces para que quede razonablemente seguro sin quedarte fuera.

::: desplegable 🧩 Solución ejercicios 7, 8 y 9
**7.**
```text
# ~/.config/systemd/user/respaldo.service
[Unit]
Description=Respaldo de proyectos

[Service]
Type=oneshot
ExecStart=/home/yafer/.local/bin/respaldo.sh
```

```text
# ~/.config/systemd/user/respaldo.timer
[Unit]
Description=Respaldo nocturno

[Timer]
OnCalendar=*-*-* 03:30:00
Persistent=true

[Install]
WantedBy=timers.target
```

```bash
systemctl --user daemon-reload
systemd-analyze calendar "*-*-* 03:30:00"      # ¿cuándo dispara?
systemctl --user enable --now respaldo.timer
systemctl --user list-timers
systemctl --user start respaldo.service         # prueba inmediata
journalctl --user -u respaldo.service -e
```

**8.**
```bash
ss -tlnp 'sport = :8000'          # muestra users:(("python",pid=48890,fd=3))
kill 48890                        # SIGTERM: el programa puede cerrar conexiones y archivos
sleep 3; ss -tlnp 'sport = :8000' # ¿sigue?
kill -9 48890                     # solo si no respondió
```
SIGKILL no deja limpiar: puede dejar archivos temporales, sockets o una base de datos a medio escribir.

**9.** (1) entrar con la llave del panel; (2) `apt update && apt upgrade`; (3) crear usuario con sudo; (4) `ssh-copy-id` y PROBAR en otra terminal; (5) `PermitRootLogin no` y `PasswordAuthentication no`, `sshd -t`, recargar; (6) firewall: permitir SSH, 80 y 443, y recién entonces activarlo; (7) actualizaciones automáticas; (8) respaldos probados.
:::

10. **Reto**: escribe una línea que, a partir de `access.log`, muestre cuántos bytes en total descargó cada IP, ordenada de mayor a menor.

::: desplegable 🧩 Solución ejercicio 10
```bash
awk '{b[$1]+=$10} END {for (ip in b) print ip, b[ip]}' access.log | sort -k2 -rn
```

```text
181.115.12.4 1184
200.87.45.10 1040
190.129.3.77 64
```
`b` es un arreglo asociativo: la clave es la IP y el valor, la suma de bytes (`$10`).
:::

## 🎤 Preguntas de entrevista

::: desplegable ❓ ¿Qué diferencia hay entre Linux, una distribución y GNU?
**Linux** es el kernel. **GNU** aporta gran parte de las herramientas (bash, coreutils, gcc). Una **distribución** empaqueta kernel + herramientas + gestor de paquetes + configuración. Por eso se discute "GNU/Linux" como nombre del sistema completo.
:::

::: desplegable ❓ ¿Qué pasa exactamente cuando escribes `ls` y pulsas Enter?
La shell lee la línea, expande variables y comodines, busca `ls` (alias/función/builtin, luego cada carpeta del PATH), hace `fork()` para clonarse, el hijo hace `execve()` del binario, el kernel carga el programa, `ls` pide el contenido del directorio con llamadas al sistema y escribe en stdout, y al terminar la shell recoge su código de salida (`$?` / `$status`).
:::

::: desplegable ❓ Explica `chmod 754 archivo` y qué significa `x` en una carpeta.
7 = rwx para el dueño, 5 = r-x para el grupo, 4 = r-- para otros. En una carpeta, `x` permite **entrar** (`cd`) y acceder a lo que hay dentro; `r` solo permite listar nombres; `w` permite crear, borrar y renombrar entradas.
:::

::: desplegable ❓ ¿Diferencia entre `>`, `>>`, `|` y `2>&1`?
`>` redirige stdout a un archivo sobrescribiéndolo; `>>` añade al final; `|` conecta stdout de un comando con stdin del siguiente; `2>&1` hace que stderr vaya adonde va stdout ahora mismo, por eso el orden importa (`cmd > f 2>&1`).
:::

::: desplegable ❓ ¿Cómo encuentras qué proceso usa el puerto 8080 y lo cierras?
`ss -tlnp 'sport = :8080'` (o `lsof -i :8080`) da el PID. Luego `kill PID` (SIGTERM); si no responde tras unos segundos, `kill -9 PID`. En un servicio gestionado por systemd, mejor `systemctl stop servicio`, porque si no se reinicia solo.
:::

::: desplegable ❓ ¿Diferencia entre un enlace duro y uno simbólico?
El **duro** es otro nombre para el mismo inodo (mismos datos; solo archivos y mismo sistema de archivos; borrar un nombre no borra los datos mientras quede otro). El **simbólico** es un archivo que contiene una ruta; puede apuntar a carpetas o a otros discos y queda roto si se borra el destino.
:::

::: desplegable ❓ ¿Qué hace `set -euo pipefail` y por qué usarlo?
`-e` aborta ante el primer comando que falla; `-u` trata variables sin definir como error; `pipefail` hace que una tubería falle si falla cualquier eslabón. Evitan que un script siga ejecutando tras un error (por ejemplo, un `rm -rf "$VAR/"` con `VAR` vacío). Caveat: `-e` tiene casos raros (`if`, `&&`, subshells), así que no sustituye a probar y a usar `shellcheck`.
:::

::: desplegable ❓ ¿Cron o timer de systemd? ¿Cuándo cada uno?
Cron: simple, portable, ideal para tareas rápidas en cualquier Unix. Timers: logs en el journal, `Persistent=true` para recuperar ejecuciones perdidas, dependencias y límites de recursos; preferibles en distros con systemd. Ambos requieren rutas absolutas.
:::

::: desplegable ❓ Un servidor está lento. ¿Qué miras primero?
`uptime` y `btop` (carga, CPU), `free -h` (columna "disponible", no "libre"), `df -h` y `iostat` (disco lleno o saturado), `ss`/`ping` (red), `journalctl -p err -b` y `dmesg` (errores, OOM). Mido antes de cambiar nada y cambio una cosa a la vez.
:::

::: desplegable ❓ ¿Por qué `sudo pip install` o `sudo npm install -g` son mala idea?
Mezclan archivos de root en tu casa y pisan paquetes del gestor del sistema (en Arch, pip ya lo bloquea con el error `externally-managed-environment`). Usa entornos virtuales (`uv venv`, `python -m venv`) o los paquetes del sistema.
:::

::: desplegable ❓ ¿Cómo aseguras un servidor SSH?
Llaves en vez de contraseñas, `PermitRootLogin no`, usuario normal con sudo, firewall que solo abre lo necesario, actualizaciones automáticas, opcionalmente `fail2ban`, y siempre validar con `sshd -t` y mantener otra sesión abierta mientras pruebas.
:::

## 🇬🇧 Vocabulario esencial

| English | Suena | Español |
|---|---|---|
| kernel | /kérnel/ | núcleo del sistema |
| shell | /shel/ | intérprete de comandos |
| pipe | /páip/ | tubería |
| redirect | /ridairékt/ | redirigir |
| permission | /permíshon/ | permiso |
| owner | /óuner/ | dueño |
| daemon | /dímon/ | proceso de fondo |
| mount | /máunt/ | montar |
| package | /pákech/ | paquete |
| repository (repo) | /ripózitori/ | repositorio |
| dependency | /dipéndensi/ | dependencia |
| rolling release | /róulin rilís/ | actualización continua |
| root | /rut/ | superusuario / raíz |
| path | /paz/ | ruta |
| stdin / stdout / stderr | /es-ti-di-in.../ | entrada / salida / error estándar |
| exit code | /éksit kóud/ | código de salida |
| symlink | /símlink/ | enlace simbólico |
| firewall | /fáieruol/ | cortafuegos |
| log | /log/ | registro |
| dry run | /drái ran/ | simulacro |

🇬🇧 Frases útiles en foros y documentación: **"permission denied"** = permiso denegado · **"command not found"** = orden no encontrada · **"no such file or directory"** = no existe el archivo o carpeta · **"works on my machine"** = en mi máquina funciona · **"RTFM (read the f... manual)"** = lee el manual.

## 📌 Resumen final tipo chuleta

| Necesito… | Comando |
|---|---|
| saber dónde estoy / qué hay | `pwd` · `ls -la` · `eza --tree` |
| buscar archivo / texto | `fd nombre` · `rg "texto"` · `find . -name "*.py"` |
| ver un archivo grande | `less` · `bat` · `tail -f` |
| permisos | `chmod 644/755/600` · `chown usuario:grupo` |
| procesos | `ps aux` · `btop` · `kill PID` · `pkill -f nombre` |
| texto | `cut` · `sort | uniq -c` · `awk` · `sed` · `jq` |
| paquetes (CachyOS) | `sudo pacman -Syu` · `paru -S` · `pacman -Qo` |
| servicios y logs | `systemctl status/enable --now` · `journalctl -u x -e` |
| red | `ip -br a` · `ss -tulpn` · `ping` · `dig` · `curl -I` |
| remoto | `ssh` · `scp` · `rsync -avhn` |
| disco | `df -h` · `du -sh * | sort -rh` · `lsblk` |
| comprimir | `tar --zstd -cf x.tar.zst dir/` · `tar -xf` · `zip -r` |

```capas
Hábitos : comillas, set -euo pipefail, probar con echo / -n antes de borrar
Seguridad : sudo puntual, llaves SSH, firewall, actualizar, respaldos 3-2-1
Diagnóstico : leer el error completo, journalctl, ss, btop, una cosa a la vez
Automatización : scripts bash + timers de systemd
Base : todo es un archivo; programas pequeños conectados con tuberías
```

💡 Consejo: la mejor forma de aprender es romper cosas en un lugar seguro: una carpeta en `/tmp`, una máquina virtual o un contenedor. Usa `tldr comando` y `man comando`, y consulta la **Arch Wiki** cuando algo falle.

📌 Resumen: Linux = kernel; la distro lo empaqueta; la shell lo maneja; todo se compone con tuberías; los permisos protegen; systemd mantiene vivo lo importante; y los errores famosos casi siempre son una variable vacía, un `sudo` de más o un respaldo que nunca se probó.
