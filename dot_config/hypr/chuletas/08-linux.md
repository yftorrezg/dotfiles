# 🐧 Linux
> Domina la terminal de CachyOS: archivos, permisos, procesos, pacman, systemd, red, fish y scripts.

## 🗂️ Estructura de carpetas

En Linux **todo cuelga de una sola raíz**: `/`. No hay `C:` ni `D:`; los discos y USB se "enganchan" (montan) como carpetas dentro de ese árbol. Piensa en un edificio: `/` es la planta baja y cada carpeta es un piso con su función.

```text
/
├── home/          🏠 casas de los usuarios: /home/yafer (tu ~)
├── root/          👑 casa del administrador (root)
├── etc/           ⚙️ configuración del sistema (pacman.conf, fstab, hosts)
├── usr/           📦 programas instalados
│   ├── bin/       ejecutables (ls, git, python...)
│   ├── lib/       librerías
│   └── share/     iconos, manuales, temas
├── var/           📈 datos que cambian: logs, cachés, bases de datos
│   ├── log/       registros
│   └── cache/pacman/pkg/   paquetes descargados
├── tmp/           🗑️ temporales (se borra al reiniciar)
├── boot/          🥾 kernel y gestor de arranque
├── dev/           🔌 dispositivos como archivos (/dev/sda, /dev/nvme0n1)
├── proc/ sys/     🧠 info en vivo del kernel y procesos (archivos virtuales)
├── run/           ⏱️ datos de la sesión actual (sockets, PIDs)
├── mnt/ media/    💾 puntos de montaje de discos y USB
└── opt/           📦 programas de terceros "todo en uno"
```

- `~` :: Tu carpeta personal: /home/yafer
- `~/.config/` :: Configuración de TUS programas (hypr, fish, nvim, kitty...)
- `~/.local/share/` :: Datos de tus programas (fuentes, apps, papelera)
- `~/.local/bin/` :: Tus scripts propios ejecutables
- `~/.cache/` :: Cachés (se puede borrar si necesitas espacio)
- `/etc/` :: Configuración global (necesitas sudo para editar)

📌 Archivos y carpetas que empiezan con punto (`.config`, `.bashrc`) son **ocultos**. `ls -a` los muestra.

💡 Consejo: regla práctica: si es tuyo, vive en `~`. Si es del sistema, en `/etc` o `/usr`, y solo se toca con `sudo`.

⚠️ Cuidado: Linux distingue mayúsculas: `Foto.png` y `foto.png` son archivos distintos.

🇬🇧 **root** /rut/ = raíz / superusuario · **home** /jóum/ = casa (carpeta personal) · **directory** /dairéktori/ = carpeta · **path** /paz/ = ruta · **mount** /máunt/ = montar · **hidden** /jíden/ = oculto

## 🧭 Navegar

La terminal siempre está "parada" en una carpeta (el directorio actual). Moverte es como caminar por pasillos: `cd` para ir, `pwd` para preguntar dónde estás, `ls` para mirar alrededor.

- `pwd` :: Mostrar en qué carpeta estás
- `ls` :: Listar el contenido
- `ls -la` :: Lista larga (permisos, tamaño, fecha) incluyendo ocultos
- `ls -lh` :: Tamaños legibles (K, M, G)
- `ls -lt` :: Ordenar por fecha (lo más nuevo primero)
- `cd Proyectos` :: Entrar a una carpeta (ruta relativa)
- `cd /etc` :: Ir a una ruta absoluta (empieza con /)
- `cd ..` :: Subir un nivel
- `cd` :: Volver a tu casa (~)
- `cd -` :: Volver a la carpeta anterior
- `tree -L 2` :: Ver el árbol de carpetas (2 niveles)
- `eza -la --icons --git` :: ls moderno con iconos y estado de git
- `z proy` :: Con zoxide: saltar a la carpeta más usada que coincida con "proy"
- `prevd` :: En fish: carpeta anterior del historial (Alt+←; `nextd` o Alt+→ va adelante)

### 📍 Rutas absolutas y relativas

| Ruta | Tipo | Significa |
|---|---|---|
| `/home/yafer/Proyectos` | absoluta | desde la raíz, funciona desde cualquier lugar |
| `Proyectos/ia` | relativa | desde donde estás ahora |
| `.` | relativa | la carpeta actual |
| `..` | relativa | la carpeta de arriba |
| `~/Descargas` | absoluta | atajo de /home/yafer/Descargas |
| `../../otro` | relativa | sube dos niveles y entra a otro |

💡 Consejo: usa **Tab** siempre. Completa nombres y evita errores de tipeo. En fish, la sugerencia gris se acepta con → (flecha derecha).

⚠️ Cuidado: los nombres con espacios necesitan comillas: `cd "Mis Documentos"` o `cd Mis\ Documentos`.

🇬🇧 **list** /list/ = listar · **change directory (cd)** /chéinch dairéktori/ = cambiar de carpeta · **print working directory (pwd)** /print uérkin dairéktori/ = mostrar carpeta actual · **relative** /rélativ/ = relativa · **absolute** /ábsolut/ = absoluta

## 📁 Archivos y carpetas

Crear, copiar, mover y borrar. Recuerda: en la terminal **no hay papelera**; lo borrado con `rm` desaparece.

- `mkdir proyecto` :: Crear una carpeta
- `mkdir -p proyecto/src/utils` :: Crear carpetas anidadas de una vez
- `touch notas.txt` :: Crear un archivo vacío (o actualizar su fecha)
- `cp a.txt b.txt` :: Copiar un archivo
- `cp -r carpeta/ copia/` :: Copiar una carpeta entera (recursivo)
- `cp -i a.txt b.txt` :: Preguntar antes de sobrescribir
- `mv viejo.txt nuevo.txt` :: Renombrar
- `mv archivo.txt ~/Documentos/` :: Mover a otra carpeta
- `rm archivo.txt` :: Borrar un archivo (sin papelera)
- `rm -r carpeta/` :: Borrar una carpeta con todo dentro
- `rm -i *.log` :: Borrar preguntando uno por uno
- `rmdir vacia/` :: Borrar una carpeta solo si está vacía
- `trash-put archivo` :: Mandar a la papelera (paquete trash-cli)
- `ln -s /ruta/real enlace` :: Crear un enlace simbólico (acceso directo)
- `file foto.png` :: Decir qué tipo de archivo es realmente
- `stat app.py` :: Información detallada (tamaño, permisos, fechas)
- `realpath archivo` :: Mostrar la ruta absoluta completa

### 🃏 Comodines (globbing)

- `*` :: Cualquier texto: `*.py` = todos los .py
- `?` :: Un solo carácter: `foto?.png` = foto1.png, fotoA.png
- `[0-9]` :: Un carácter del rango: `clase[1-3].md`
- `{a,b}` :: Varias opciones: `cp app.{py,bak}` copia app.py a app.bak
- `**` :: En fish: cualquier subcarpeta: `ls **/*.py`

### ✅ Ejemplo resuelto: organizar un proyecto nuevo

```bash
mkdir -p ~/Proyectos/clasificador/{datos,src,notebooks,modelos}
cd ~/Proyectos/clasificador
touch src/{entrenar,evaluar}.py README.md
mv ~/Descargas/iris.csv datos/
tree
```

```text
.
├── datos
│   └── iris.csv
├── modelos
├── notebooks
├── README.md
└── src
    ├── entrenar.py
    └── evaluar.py
```

⚠️ Cuidado: `rm -rf` borra sin preguntar y sin vuelta atrás. Jamás ejecutes `rm -rf /` ni `rm -rf ~` ni un `rm -rf $VAR/` con una variable que podría estar vacía.

💡 Consejo: antes de un `rm` con comodines, cambia `rm` por `ls` con el mismo patrón para ver qué se borraría.

🇬🇧 **copy** /kópi/ = copiar · **move** /muv/ = mover · **remove** /rimúv/ = eliminar · **recursive** /rikérsiv/ = recursivo · **symbolic link** /simbólik link/ = enlace simbólico · **wildcard** /uáildkard/ = comodín

## 📖 Ver y editar texto

En Linux casi todo es texto: configuraciones, logs, scripts. Saber leer y editar texto desde la terminal es superpoder básico.

- `cat archivo.txt` :: Mostrar todo el archivo
- `bat app.py` :: cat con colores y números de línea
- `less /var/log/pacman.log` :: Leer archivos largos: espacio avanza, b retrocede, /texto busca, q sale
- `head -n 20 datos.csv` :: Primeras 20 líneas
- `tail -n 20 datos.csv` :: Últimas 20 líneas
- `tail -f app.log` :: Ver un archivo en vivo mientras crece (Ctrl+C para salir)
- `wc -l datos.csv` :: Contar líneas (-w palabras, -c bytes)
- `sort nombres.txt` :: Ordenar líneas (-n numérico, -r al revés)
- `uniq -c` :: Contar líneas repetidas consecutivas (usa antes sort)
- `cut -d, -f1,3 datos.csv` :: Sacar las columnas 1 y 3 de un CSV
- `diff a.txt b.txt` :: Diferencias entre dos archivos
- `nano notas.txt` :: Editor sencillo (Ctrl+O guarda, Ctrl+X sale)
- `nvim app.py` :: Neovim: editor potente basado en modos
- `sudoedit /etc/hosts` :: Editar un archivo del sistema de forma segura

### ✍️ nano en 30 segundos

| Tecla | Acción |
|---|---|
| `Ctrl+O` y Enter | guardar |
| `Ctrl+X` | salir |
| `Ctrl+W` | buscar |
| `Ctrl+K` | cortar línea |
| `Ctrl+U` | pegar |
| `Alt+U` | deshacer |

### 🟢 nvim básico: sobrevivir y avanzar

Neovim tiene **modos**: en modo Normal las teclas son órdenes; en modo Insertar escribes texto. Por eso "no puedo salir de vim" es un meme: hay que volver al modo Normal con `Esc` primero.

| Tecla (modo Normal) | Acción |
|---|---|
| `i` | insertar antes del cursor (`a` después, `o` línea nueva) |
| `Esc` | volver a modo Normal |
| `:w` | guardar |
| `:q` | salir (`:q!` sale sin guardar) |
| `:wq` o `ZZ` | guardar y salir |
| `h j k l` | izquierda, abajo, arriba, derecha |
| `w` / `b` | palabra siguiente / anterior |
| `gg` / `G` | inicio / final del archivo |
| `dd` | borrar (cortar) línea |
| `yy` | copiar línea |
| `p` | pegar |
| `u` / `Ctrl+r` | deshacer / rehacer |
| `/texto` | buscar (`n` siguiente) |
| `:%s/viejo/nuevo/g` | reemplazar en todo el archivo |
| `v` | seleccionar (modo visual) |

💡 Consejo: ejecuta `nvim +Tutor` (o `vimtutor`): un tutorial interactivo de 30 minutos que vale oro.

⚠️ Cuidado: no uses `cat` para archivos binarios (imágenes, .pt): llena la terminal de basura. Si pasa, escribe `reset`.

🇬🇧 **editor** /éditor/ = editor · **insert** /insért/ = insertar · **quit** /kuít/ = salir · **write** /ráit/ = escribir/guardar · **search** /serch/ = buscar · **replace** /ripléis/ = reemplazar · **tail** /teil/ = cola/final

## 🔒 Permisos

Cada archivo tiene **dueño**, **grupo** y **permisos** para tres tipos de personas: el dueño (**u**ser), el grupo (**g**roup) y los demás (**o**thers). Cada uno puede tener **r** (leer), **w** (escribir) y **x** (ejecutar). Como un edificio: tú tienes llave de tu depa, tu familia de algunas puertas y los visitantes de casi nada.

```text
$ ls -l script.sh
-rwxr-xr-- 1 yafer users 512 oct 18 10:00 script.sh
│└┬┘└┬┘└┬┘   └─┬─┘ └─┬─┘
│ │  │  │      │     └── grupo
│ │  │  │      └──────── dueño
│ │  │  └── otros:  r-- (solo leer)
│ │  └───── grupo:  r-x (leer y ejecutar)
│ └──────── dueño:  rwx (todo)
└────────── tipo: - archivo, d carpeta, l enlace
```

### 🔢 chmod numérico

Cada permiso vale un número: **r = 4, w = 2, x = 1**. Se suman para cada grupo de personas.

| Número | Permisos | Significa |
|---|---|---|
| `7` | `rwx` | 4+2+1: leer, escribir, ejecutar |
| `6` | `rw-` | 4+2: leer y escribir |
| `5` | `r-x` | 4+1: leer y ejecutar |
| `4` | `r--` | solo leer |
| `0` | `---` | nada |
| `755` | `rwxr-xr-x` | típico de scripts y carpetas |
| `644` | `rw-r--r--` | típico de archivos normales |
| `600` | `rw-------` | privado (llaves SSH, .env) |
| `700` | `rwx------` | carpeta privada (~/.ssh) |

- `chmod +x script.sh` :: Dar permiso de ejecución (para poder hacer ./script.sh)
- `chmod u+x,g-w archivo` :: Simbólico: dueño gana x, grupo pierde w
- `chmod 644 notas.txt` :: Numérico: rw-r--r--
- `chmod -R 755 carpeta/` :: Aplicar a toda una carpeta (recursivo)
- `chown yafer:users archivo` :: Cambiar dueño y grupo (necesita sudo)
- `sudo chown -R yafer:yafer ~/Proyectos` :: Recuperar la propiedad de tus archivos
- `id` :: Ver tu usuario, tus grupos y sus números
- `groups` :: Ver a qué grupos perteneces
- `sudo usermod -aG docker yafer` :: Añadirte a un grupo (cierra sesión para que aplique)

### 👑 sudo: poderes de administrador

- `sudo comando` :: Ejecutar UN comando como root
- `sudo !!` :: En bash: repetir el último comando con sudo (en fish: escribe sudo y pulsa ↑, o Alt+S)
- `sudo -i` :: Abrir una shell de root (sal con exit; úsalo poco)
- `sudo -l` :: Ver qué puedes hacer con sudo

### ✅ Ejemplo resuelto: "Permission denied" al ejecutar un script

```bash
./respaldo.sh
```

```text
fish: Comando desconocido. ‘./respaldo.sh’ existe pero no es un archivo ejecutable.
```

```bash
ls -l respaldo.sh               # -rw-r--r--  → falta la x
chmod +x respaldo.sh
ls -l respaldo.sh               # -rwxr-xr-x  → ahora sí
./respaldo.sh
```

⚠️ Cuidado: `chmod 777` "lo arregla todo" pero deja el archivo abierto a cualquiera. Casi nunca es la respuesta correcta.

⚠️ Cuidado: no uses `sudo` para cosas de tu carpeta personal (pip, npm, git). Crea archivos de root en tu `~` y luego tendrás "Permission denied" por todas partes.

🇬🇧 **permission** /permíshon/ = permiso · **owner** /óuner/ = dueño · **read** /rid/ = leer · **write** /ráit/ = escribir · **execute** /éksekiut/ = ejecutar · **superuser** /súperiuser/ = superusuario · **denied** /dináid/ = denegado

## 🔎 Buscar archivos y texto

Dos preguntas distintas: **¿dónde está el archivo?** (find, fd) y **¿qué archivo contiene este texto?** (grep, rg). `fd` y `rg` son versiones modernas, rápidas y que respetan `.gitignore`.

### 📂 Buscar archivos

- `find . -name "*.py"` :: Buscar .py desde la carpeta actual
- `find ~ -iname "*tesis*"` :: Sin distinguir mayúsculas
- `find . -type d -name node_modules` :: Solo carpetas
- `find . -size +100M` :: Archivos de más de 100 MB
- `find . -mtime -1` :: Modificados en las últimas 24 horas
- `find . -name "*.tmp" -delete` :: Buscar y borrar
- `find . -name "*.py" -exec wc -l {} +` :: Ejecutar un comando con los resultados
- `fd modelo` :: fd: buscar archivos cuyo nombre contenga "modelo"
- `fd -e py` :: Por extensión
- `fd -H config` :: Incluir ocultos
- `fd -e log -x rm` :: Ejecutar rm sobre cada resultado
- `locate pacman.conf` :: Búsqueda instantánea en una base de datos (actualízala con sudo updatedb)

### 📝 Buscar texto dentro de archivos

- `grep "error" app.log` :: Líneas que contienen "error"
- `grep -i "error" app.log` :: Sin distinguir mayúsculas
- `grep -rn "def entrenar" .` :: Recursivo y con número de línea
- `grep -v "DEBUG" app.log` :: Líneas que NO contienen DEBUG
- `grep -c "200" access.log` :: Contar coincidencias
- `grep -E "error|warning" app.log` :: Expresión regular extendida (o una cosa u otra)
- `grep -l "import torch" *.py` :: Solo los nombres de los archivos
- `rg "TODO"` :: ripgrep: buscar en todo el proyecto, rapidísimo
- `rg -t py "import numpy"` :: Solo en archivos Python
- `rg -i -C 2 "timeout"` :: Con 2 líneas de contexto alrededor
- `rg -l "api_key"` :: Qué archivos contienen api_key (¡revisa secretos!)

### ✅ Ejemplo resuelto: ¿dónde definí esa función?

Situación: tienes un proyecto grande y no recuerdas en qué archivo está `normalizar`.

```bash
rg -n "def normalizar"
```

```text
src/preprocesado.py
42:def normalizar(datos, media=None):
```

Y si quieres los 5 archivos más pesados del proyecto:

```bash
fd -t f -x du -h {} | sort -rh | head -5
```

💡 Consejo: instala los modernos: `sudo pacman -S fd ripgrep bat eza zoxide fzf`. Con `fzf` puedes buscar archivos de forma interactiva con Ctrl+T.

⚠️ Cuidado: en `find` pon el patrón entre comillas (`"*.py"`); sin ellas, la shell expande el comodín antes y el resultado es raro.

🇬🇧 **find** /fáind/ = encontrar · **search** /serch/ = buscar · **match** /mach/ = coincidencia · **regular expression (regex)** /réguiular ekspréshon/ = expresión regular · **case-insensitive** /kéis insénsitiv/ = sin distinguir mayúsculas

## 🔗 Tuberías y redirecciones

La filosofía Unix: **programas pequeños que hacen una cosa bien**, conectados como piezas de LEGO. La tubería `|` pasa la salida de un comando como entrada del siguiente, como una línea de montaje.

Cada programa tiene tres "canales": **stdin** (0, entrada), **stdout** (1, salida normal) y **stderr** (2, errores).

- `comando > archivo.txt` :: Guardar la salida en un archivo (lo SOBRESCRIBE)
- `comando >> archivo.txt` :: Añadir la salida al final del archivo
- `comando 2> errores.txt` :: Guardar solo los errores
- `comando > todo.txt 2>&1` :: Guardar salida y errores juntos (bash y fish)
- `comando &> todo.txt` :: Atajo para lo mismo (bash y fish)
- `comando 2>/dev/null` :: Tirar los errores a la basura
- `comando < entrada.txt` :: Usar un archivo como entrada
- `cmd1 | cmd2` :: Tubería: la salida de cmd1 entra en cmd2
- `comando | tee salida.txt` :: Ver en pantalla Y guardar en archivo
- `comando | xargs rm` :: Convertir líneas en argumentos de otro comando
- `cmd1 && cmd2` :: Ejecutar cmd2 solo si cmd1 salió bien
- `cmd1 || cmd2` :: Ejecutar cmd2 solo si cmd1 falló
- `cmd1; cmd2` :: Ejecutar uno tras otro, pase lo que pase
- `echo $status` :: En fish: código de salida del último comando (0 = éxito); en bash es $?
- `wl-copy < archivo.txt` :: Copiar un archivo al portapapeles (Wayland)
- `wl-paste > pegado.txt` :: Guardar el portapapeles en un archivo

### ✅ Ejemplo resuelto: las 5 IPs que más visitan tu servidor

```bash
cat access.log | cut -d' ' -f1 | sort | uniq -c | sort -rn | head -5
```

Paso a paso: `cut` saca la primera columna (la IP), `sort` las agrupa, `uniq -c` cuenta cuántas veces aparece cada una, `sort -rn` ordena de mayor a menor y `head -5` muestra las 5 primeras.

```text
    842 181.115.12.4
    310 200.87.45.10
    122 190.129.3.77
     41 8.8.8.8
      9 127.0.0.1
```

### ✅ Ejemplo resuelto: guardar el log de un entrenamiento

```bash
python entrenar.py 2>&1 | tee entrenamiento.log
```

Ves el progreso en vivo y además queda guardado en `entrenamiento.log`, errores incluidos.

⚠️ Cuidado: `sort datos.txt > datos.txt` deja el archivo VACÍO: la shell lo vacía antes de que sort lo lea. Usa otro nombre o `sort -o datos.txt datos.txt`.

💡 Consejo: construye tuberías de a poco: ejecuta el primer comando, mira la salida, añade `| siguiente`, y así.

🇬🇧 **pipe** /páip/ = tubería · **redirect** /ridairékt/ = redirigir · **standard output** /stándard áutput/ = salida estándar · **append** /apénd/ = añadir al final · **overwrite** /ouverráit/ = sobrescribir · **exit code** /éksit cóud/ = código de salida

## ⚙️ Procesos

Un **proceso** es un programa en ejecución. Cada uno tiene un **PID** (número de identificación). Puedes verlos, pausarlos, mandarlos al fondo o matarlos.

- `ps aux` :: Todos los procesos del sistema
- `ps aux | grep python` :: Buscar procesos de python
- `pgrep -a python` :: Lo mismo, más limpio: PID y comando
- `htop` :: Monitor interactivo (F9 matar, F6 ordenar, q salir)
- `btop` :: Monitor bonito: CPU, RAM, disco, red y procesos
- `nvtop` :: Monitor de la GPU (útil para entrenar modelos)
- `kill 1234` :: Pedir amablemente al proceso 1234 que termine (SIGTERM)
- `kill -9 1234` :: Matarlo a la fuerza (SIGKILL, último recurso)
- `pkill -f entrenar.py` :: Matar por nombre o por la línea de comando
- `killall firefox` :: Matar todos los procesos con ese nombre
- `hyprctl kill` :: Hyprland: clic en una ventana para matarla
- `uptime` :: Cuánto lleva encendido y la carga del sistema
- `free -h` :: Memoria RAM usada y libre
- `nice -n 10 comando` :: Ejecutar con menos prioridad (no molesta al resto)
- `time python script.py` :: Medir cuánto tarda un comando

### 📡 Señales principales

| Señal | Número | Cómo se envía | Qué hace |
|---|---|---|---|
| `SIGINT` | 2 | `Ctrl+C` | interrumpir (el programa puede limpiar) |
| `SIGTERM` | 15 | `kill PID` | pedir que termine (por defecto) |
| `SIGKILL` | 9 | `kill -9 PID` | matar sin opción a limpiar |
| `SIGTSTP` | 20 | `Ctrl+Z` | pausar y mandar al fondo |
| `SIGCONT` | 18 | `fg` o `bg` | continuar un proceso pausado |
| `SIGHUP` | 1 | cerrar la terminal | colgar; muchos servicios lo usan para recargar config |

### 🎭 Trabajos en primer y segundo plano

- `comando &` :: Ejecutar en segundo plano (la terminal queda libre)
- `Ctrl+Z` :: Pausar el proceso que está en primer plano
- `jobs` :: Listar los trabajos de esta terminal
- `bg` :: Continuar el último pausado en segundo plano
- `fg` :: Traer el último trabajo al primer plano
- `fg %2` :: Traer el trabajo número 2 (el número sale en jobs)
- `disown` :: Desligar el trabajo de la terminal (sobrevive si la cierras)
- `nohup python entrenar.py > log.txt 2>&1 &` :: Proceso que sigue aunque cierres la terminal o la sesión SSH

### ✅ Ejemplo resuelto: un programa colgado

Situación: un script de Python se quedó congelado y Ctrl+C no responde.

```bash
pgrep -a python
```

```text
48213 python entrenar.py --epochs 100
48890 python -m http.server
```

```bash
kill 48213                      # primero amablemente
sleep 3; pgrep -a python        # ¿sigue ahí?
kill -9 48213                   # si sigue, a la fuerza
```

💡 Consejo: para entrenamientos largos usa `tmux` o `zellij`: dejas el proceso corriendo dentro, te desconectas y vuelves cuando quieras (incluso por SSH).

⚠️ Cuidado: `kill -9` no deja al programa guardar nada; puede corromper archivos. Úsalo solo si `kill` normal no funciona.

🇬🇧 **process** /próses/ = proceso · **kill** /kil/ = matar · **signal** /sígnal/ = señal · **background** /bákgraund/ = segundo plano · **foreground** /fórgraund/ = primer plano · **hang/frozen** /jang, fróuzen/ = colgado, congelado · **job** /yob/ = trabajo

## 📦 Paquetes en Arch: pacman y paru

CachyOS es Arch: los programas se instalan con **pacman** desde los repositorios oficiales (y los de CachyOS, optimizados). Lo que no está ahí suele estar en el **AUR** (Arch User Repository), hecho por la comunidad, y se instala con un *AUR helper* como **paru**.

Analogía: pacman es la tienda oficial del supermercado; el AUR es la feria donde la comunidad vende sus recetas. paru te ayuda a cocinarlas (compilarlas) en casa.

### 🧾 Tabla de comandos

| Quiero… | pacman | paru |
|---|---|---|
| actualizar todo el sistema | `sudo pacman -Syu` | `paru` (incluye AUR) |
| instalar | `sudo pacman -S btop` | `paru -S visual-studio-code-bin` |
| buscar en repos | `pacman -Ss nombre` | `paru -Ss nombre` (también AUR) |
| info de un paquete | `pacman -Si nombre` | `paru -Si nombre` |
| desinstalar | `sudo pacman -R nombre` | `paru -R nombre` |
| desinstalar con dependencias y config | `sudo pacman -Rns nombre` | `paru -Rns nombre` |
| listar instalados | `pacman -Q` | `paru -Q` |
| listar instalados a mano | `pacman -Qe` | `paru -Qe` |
| listar instalados del AUR | `pacman -Qm` | `paru -Qm` |
| ¿qué paquete instaló este archivo? | `pacman -Qo /usr/bin/git` | igual |
| archivos de un paquete | `pacman -Ql git` | igual |
| huérfanos (dependencias sin uso) | `pacman -Qdt` | `paru -Qdt` |
| borrar huérfanos | `sudo pacman -Rns (pacman -Qdtq)` en fish | `paru -c` |
| limpiar caché de paquetes | `sudo paccache -rk2` | `paru -Sc` |

📌 Las letras: **S** = sync (repos), **Q** = query (instalados), **R** = remove. Modificadores: y = refrescar base de datos, u = actualizar, s = buscar, i = info, n = sin respaldos de config, s (en -R) = dependencias.

- `sudo pacman -Syu` :: Actualizar todo. Hazlo antes de instalar cosas nuevas
- `checkupdates` :: Ver qué se actualizaría sin tocar nada (pacman-contrib)
- `paru -Gp nombre` :: Ver el PKGBUILD de un paquete del AUR antes de instalarlo
- `pacman -Qi nombre` :: Info del paquete instalado (versión, tamaño, quién lo necesita)
- `expac -H M '%m\t%n' | sort -h | tail -20` :: Los 20 paquetes que más ocupan (paquete expac)
- `cat /var/log/pacman.log | tail -50` :: Historial de lo último que se instaló o actualizó

### ✅ Ejemplo resuelto: instalar herramientas para IA

```bash
sudo pacman -Syu                                   # 1. sistema al día
sudo pacman -S python python-pip uv cuda nvtop     # 2. oficiales
paru -S visual-studio-code-bin                     # 3. del AUR
uv venv && source .venv/bin/activate.fish          # 4. entorno virtual del proyecto
uv pip install torch numpy pandas                  # 5. librerías de Python dentro del venv
```

⚠️ Cuidado: NUNCA hagas `sudo pacman -Sy paquete` (actualización parcial). Mezcla versiones y puede romper el sistema. Siempre `-Syu`.

⚠️ Cuidado: no instales librerías de Python con `sudo pip install`. Usa entornos virtuales (`uv venv` o `python -m venv .venv`) o el paquete `python-xxx` de pacman.

💡 Consejo: antes de una actualización grande, revisa las noticias en archlinux.org y ten un snapshot (CachyOS suele traer Btrfs + snapper para volver atrás desde el arranque).

🇬🇧 **package** /pákech/ = paquete · **dependency** /dipéndensi/ = dependencia · **upgrade** /ápgreid/ = actualizar (versión) · **orphan** /órfan/ = huérfano · **repository** /ripózitori/ = repositorio · **build** /bild/ = compilar/construir

## 🛎️ Servicios con systemd

**systemd** es el "gerente" que arranca el sistema y cuida los **servicios** (programas que corren en el fondo: red, bluetooth, docker, ssh). Cada servicio es una **unit** descrita en un archivo `.service`.

Dos ideas que se confunden: **start** = arrancar AHORA; **enable** = arrancar automáticamente en cada encendido.

- `systemctl status bluetooth` :: Ver si un servicio está activo, sus últimos logs y su PID
- `sudo systemctl start docker` :: Arrancar ahora
- `sudo systemctl stop docker` :: Parar ahora
- `sudo systemctl restart NetworkManager` :: Reiniciar
- `sudo systemctl reload sshd` :: Recargar su configuración sin cortarlo
- `sudo systemctl enable docker` :: Activar al arrancar el sistema
- `sudo systemctl enable --now docker` :: Activar y arrancar de una vez (el más usado)
- `sudo systemctl disable --now docker` :: Desactivar y parar
- `systemctl list-units --type=service --state=running` :: Servicios corriendo
- `systemctl --failed` :: Servicios que fallaron
- `systemctl is-enabled sshd` :: Saber si arranca solo
- `sudo systemctl daemon-reload` :: Releer archivos .service tras editarlos
- `systemctl --user status pipewire` :: Servicios de TU usuario (sin sudo)
- `systemctl --user enable --now syncthing` :: Activar un servicio de usuario
- `systemd-analyze blame` :: Qué servicios hacen lento el arranque

### 📜 journalctl: los logs de systemd

- `journalctl -u docker` :: Logs de un servicio
- `journalctl -u docker -f` :: Seguirlos en vivo
- `journalctl -b` :: Logs desde el último arranque
- `journalctl -b -1 -p err` :: Errores del arranque ANTERIOR (útil si se colgó)
- `journalctl -p warning --since "1 hour ago"` :: Avisos y errores de la última hora
- `journalctl --user -u mi-servicio` :: Logs de un servicio de usuario
- `journalctl -k` :: Mensajes del kernel (como dmesg)
- `journalctl --disk-usage` :: Cuánto ocupan los logs
- `sudo journalctl --vacuum-time=2weeks` :: Borrar logs de más de 2 semanas

### ✅ Ejemplo resuelto: servicio de usuario propio

Situación: quieres que un script tuyo (por ejemplo un bot) arranque solo al iniciar sesión.

```text
# ~/.config/systemd/user/bot.service
[Unit]
Description=Mi bot de Telegram

[Service]
ExecStart=/home/yafer/Proyectos/bot/.venv/bin/python /home/yafer/Proyectos/bot/bot.py
Restart=on-failure

[Install]
WantedBy=default.target
```

```bash
systemctl --user daemon-reload
systemctl --user enable --now bot
systemctl --user status bot
```

```text
● bot.service - Mi bot de Telegram
     Loaded: loaded (/home/yafer/.config/systemd/user/bot.service; enabled)
     Active: active (running) since Sat 2026-10-18 10:30:12 -04; 5s ago
   Main PID: 51234 (python)
```

💡 Consejo: si el estado dice `failed`, la explicación casi siempre está en `journalctl --user -u bot -e` (la -e salta al final).

⚠️ Cuidado: en `ExecStart` usa rutas absolutas. systemd no lee tu `config.fish`, así que no conoce tus alias ni tu PATH personalizado.

🇬🇧 **service** /sérvis/ = servicio · **daemon** /dímon/ = demonio (proceso de fondo) · **enable** /enéibol/ = habilitar · **unit** /iúnit/ = unidad · **boot** /but/ = arranque · **failed** /féild/ = falló · **journal** /yérnal/ = diario/bitácora

## 🌐 Red

Comandos para saber si tienes internet, qué IP tienes, descargar cosas y conectarte a otras máquinas.

- `ip a` :: Ver tus interfaces de red y sus IPs
- `ip r` :: Ver la ruta por defecto (tu router)
- `nmcli device wifi list` :: Redes Wi-Fi disponibles
- `nmcli device wifi connect "MiWifi" password "clave"` :: Conectarse a una Wi-Fi
- `ping -c 4 google.com` :: ¿Hay conexión? (4 intentos)
- `curl ifconfig.me` :: Tu IP pública
- `curl -I https://ejemplo.com` :: Ver solo las cabeceras HTTP (¿responde el sitio?)
- `curl -s https://api.github.com/users/yftorrezg | jq .name` :: Llamar a una API y sacar un campo del JSON
- `curl -X POST -H "Content-Type: application/json" -d '{"x":1}' localhost:8000/predecir` :: Probar tu API
- `curl -LO https://url/archivo.zip` :: Descargar conservando el nombre (-L sigue redirecciones)
- `wget -c https://url/dataset.tar.gz` :: Descargar (con -c reanuda si se cortó)
- `ss -tulpn` :: Qué programas escuchan en qué puertos
- `ss -tulpn | grep 8000` :: ¿Quién está usando el puerto 8000?
- `dig ejemplo.com` :: Consultar DNS (paquete bind)
- `traceroute google.com` :: Ver el camino de saltos hasta un servidor
- `python -m http.server 8000` :: Servidor web instantáneo de la carpeta actual

### 🔑 ssh, scp y rsync

- `ssh usuario@192.168.1.50` :: Conectarse a otra máquina
- `ssh -p 2222 usuario@servidor` :: Con un puerto distinto
- `ssh-copy-id usuario@servidor` :: Copiar tu llave pública para no escribir contraseña
- `ssh -L 8888:localhost:8888 usuario@servidor` :: Túnel: abrir el Jupyter del servidor en tu navegador
- `scp archivo.txt usuario@servidor:~/` :: Copiar un archivo al servidor
- `scp -r usuario@servidor:~/resultados ./` :: Traer una carpeta del servidor
- `rsync -avh --progress origen/ destino/` :: Sincronizar carpetas (solo copia lo que cambió)
- `rsync -avh --delete origen/ destino/` :: Espejo exacto (borra en destino lo que no esté en origen)
- `rsync -avhn origen/ destino/` :: Simulación (-n): muestra qué haría sin hacerlo
- `rsync -avz proyecto/ usuario@servidor:~/proyecto/` :: Subir por SSH comprimiendo

Con `~/.ssh/config` te ahorras escribir todo cada vez:

```text
Host lab
    HostName 192.168.1.50
    User yafer
    Port 22
    IdentityFile ~/.ssh/id_ed25519
```

Ahora basta con `ssh lab`, `scp archivo lab:~/` o `rsync -avh datos/ lab:~/datos/`.

### ✅ Ejemplo resuelto: "Address already in use"

Situación: lanzas tu API con FastAPI y dice que el puerto 8000 está ocupado.

```bash
ss -tulpn | grep :8000
```

```text
tcp   LISTEN 0  2048  127.0.0.1:8000  0.0.0.0:*  users:(("python",pid=48890,fd=3))
```

```bash
kill 48890                       # era un servidor viejo olvidado
```

⚠️ Cuidado: con rsync, la barra final importa: `origen/` copia el CONTENIDO; `origen` (sin barra) copia la carpeta misma dentro de destino.

💡 Consejo: prueba siempre `rsync` con `-n` (dry run) antes de usar `--delete`.

🇬🇧 **network** /nétuerk/ = red · **port** /port/ = puerto · **download** /dáunloud/ = descargar · **upload** /áploud/ = subir · **listen** /lísen/ = escuchar · **tunnel** /tánel/ = túnel · **dry run** /drái ran/ = simulacro · **host** /jóust/ = anfitrión/máquina

## 💾 Discos y espacio

¿Cuánto espacio me queda? ¿Qué carpeta se comió mi disco? ¿Dónde está mi USB?

- `df -h` :: Espacio libre de cada disco/partición
- `df -h ~` :: Espacio del disco donde está tu carpeta personal
- `du -sh ~/Descargas` :: Cuánto ocupa una carpeta
- `du -sh * | sort -rh | head` :: Qué ocupa más en la carpeta actual
- `ncdu ~` :: Explorador interactivo de espacio (muy útil)
- `dust` :: Alternativa moderna y visual a du
- `lsblk` :: Discos y particiones en árbol
- `lsblk -f` :: Con sistema de archivos, etiqueta y UUID
- `sudo fdisk -l` :: Detalles de las particiones
- `sudo mount /dev/sdb1 /mnt` :: Montar una partición en /mnt
- `sudo umount /mnt` :: Desmontar (antes de sacar el USB)
- `udisksctl mount -b /dev/sdb1` :: Montar un USB sin sudo (en /run/media/yafer/)
- `findmnt` :: Ver qué está montado y dónde
- `cat /etc/fstab` :: Discos que se montan solos al arrancar
- `sudo btrfs filesystem usage /` :: Uso real en Btrfs (df puede engañar)
- `sudo smartctl -a /dev/nvme0n1` :: Salud del disco (paquete smartmontools)

### ✅ Ejemplo resuelto: disco lleno

Situación: aparece "No space left on device".

```bash
df -h /                           # 1. confirmar: Use% al 98 %
ncdu ~                            # 2. explorar tu carpeta (flechas, d para borrar)
du -sh ~/.cache                   # 3. sospechosos habituales
sudo paccache -rk1                # 4. caché de pacman: deja solo 1 versión
sudo journalctl --vacuum-size=200M # 5. recortar logs
```

Los culpables típicos en IA: `~/.cache/huggingface`, `~/.cache/pip`, entornos `.venv` duplicados, checkpoints `.pt` viejos y la caché de Docker (`docker system prune`).

⚠️ Cuidado: `dd` y `mkfs` escriben directamente en el disco. Equivocarte de `/dev/sdX` borra el disco equivocado. Revisa con `lsblk` dos veces.

💡 Consejo: saca el USB solo después de `umount` (o `sync`): Linux guarda escrituras en caché y podrías perder archivos.

🇬🇧 **disk** /disk/ = disco · **partition** /partíshon/ = partición · **free space** /fri spéis/ = espacio libre · **usage** /iúsech/ = uso · **unmount** /anmáunt/ = desmontar · **device** /diváis/ = dispositivo · **filesystem** /fáilsistem/ = sistema de archivos

## 🗜️ Comprimir y descomprimir

En Linux se usa mucho **tar**: junta muchos archivos en uno (como meterlos en una caja) y opcionalmente lo comprime (gzip, xz, zstd). `zip` es el formato universal para compartir con Windows.

- `tar -czvf proyecto.tar.gz proyecto/` :: Crear .tar.gz (c = crear, z = gzip, v = ver, f = archivo)
- `tar -xzvf proyecto.tar.gz` :: Extraer un .tar.gz
- `tar -xvf archivo.tar.xz` :: Extraer (tar moderno detecta el formato solo)
- `tar -xvf datos.tar.gz -C ~/datos/` :: Extraer en otra carpeta
- `tar -tvf archivo.tar.gz` :: Ver el contenido sin extraer
- `tar --zstd -cvf respaldo.tar.zst carpeta/` :: Crear con zstd (rápido y muy bueno)
- `tar -cvf - carpeta | zstd -T0 -19 > r.tar.zst` :: zstd con todos los núcleos y compresión alta
- `zstd archivo` :: Comprimir un archivo a .zst
- `zstd -d archivo.zst` :: Descomprimir .zst
- `zip -r tarea.zip tarea/` :: Crear un .zip (para entregar tareas)
- `unzip tarea.zip` :: Extraer un .zip
- `unzip -l tarea.zip` :: Ver contenido del zip
- `7z x archivo.7z` :: Extraer .7z (paquete 7zip)
- `unrar x archivo.rar` :: Extraer .rar
- `gzip archivo` :: Comprimir un solo archivo (`gunzip archivo.gz` lo descomprime)

### 📊 ¿Qué formato uso?

| Formato | Velocidad | Compresión | Úsalo para |
|---|---|---|---|
| `.tar.gz` | buena | media | lo más compatible en Linux |
| `.tar.zst` | muy rápida | muy buena | respaldos y datasets (moderno) |
| `.tar.xz` | lenta | máxima | archivos para distribuir |
| `.zip` | buena | media | compartir con Windows o entregar tareas |
| `.7z` | lenta | muy alta | archivos grandes para compartir |

💡 Consejo: para recordar tar: "**c**rear **z**ip **v**erboso **f**ile" y "e**x**traer". La f siempre va al final porque le sigue el nombre del archivo.

⚠️ Cuidado: algunos .zip descargados extraen archivos sueltos por toda la carpeta. Mira primero con `unzip -l` o extrae en una carpeta nueva con `unzip x.zip -d x/`.

🇬🇧 **compress** /komprés/ = comprimir · **extract** /ekstrákt/ = extraer · **archive** /árkaiv/ = archivo empaquetado · **verbose** /verbóus/ = detallado · **backup** /bákap/ = respaldo

## 🌱 Variables de entorno y PATH

Las **variables de entorno** son ajustes que heredan todos los programas que lanzas: tu idioma, tu editor, dónde buscar ejecutables. La más famosa es **PATH**: la lista de carpetas donde la shell busca los comandos. Cuando escribes `git`, la shell recorre esas carpetas hasta encontrar `/usr/bin/git`.

- `echo $HOME` :: Ver una variable
- `env` :: Ver todas las variables de entorno
- `echo $PATH` :: Carpetas donde se buscan comandos
- `which python` :: Qué ejecutable se usa exactamente
- `type ls` :: Si es alias, función, builtin o ejecutable
- `set -gx EDITOR nvim` :: Fish: definir y exportar una variable
- `set -e MI_VAR` :: Fish: borrar una variable
- `fish_add_path ~/.local/bin` :: Fish: añadir una carpeta al PATH (permanente)
- `export EDITOR=nvim` :: Bash: definir y exportar
- `export PATH="$HOME/.local/bin:$PATH"` :: Bash: añadir al PATH (en ~/.bashrc)
- `MI_VAR=1 comando` :: Variable solo para ese comando (bash y fish modernos)
- `env -u DISPLAY comando` :: Ejecutar sin una variable

### 🔤 Variables útiles

| Variable | Contiene | Ejemplo |
|---|---|---|
| `HOME` | tu carpeta personal | `/home/yafer` |
| `USER` | tu usuario | `yafer` |
| `PATH` | carpetas de comandos | `/usr/local/bin /usr/bin ...` |
| `EDITOR` | editor por defecto | `nvim` |
| `SHELL` | tu shell de inicio | `/bin/fish` |
| `LANG` | idioma y codificación | `es_ES.UTF-8` |
| `XDG_CONFIG_HOME` | carpeta de config | `~/.config` |
| `WAYLAND_DISPLAY` | sesión Wayland activa | `wayland-1` |
| `CUDA_VISIBLE_DEVICES` | qué GPU ve PyTorch | `0` |

### ✅ Ejemplo resuelto: claves de API sin escribirlas en el código

```bash
# .env del proyecto (¡en .gitignore!)
OPENAI_API_KEY=sk-...
```

```python
import os
clave = os.environ["OPENAI_API_KEY"]
```

```bash
set -gx OPENAI_API_KEY (cat ~/.secretos/openai)   # fish: solo en esta sesión
python app.py
```

⚠️ Cuidado: "command not found" justo tras instalar con pip o cargo suele ser PATH: el ejecutable está en `~/.local/bin` o `~/.cargo/bin` y esa carpeta no está en el PATH.

💡 Consejo: en fish no uses `set -U` para PATH a lo loco; `fish_add_path` evita duplicados y es la forma recomendada.

🇬🇧 **environment variable** /enváironment vérriabol/ = variable de entorno · **export** /ekspórt/ = exportar · **path** /paz/ = ruta · **command not found** /cománd not fáund/ = comando no encontrado · **set** /set/ = asignar

## 🐟 fish shell

**fish** (friendly interactive shell) es tu shell: la que interpreta lo que escribes. Es muy cómoda: sugerencias automáticas en gris según tu historial, colores de sintaxis y completado inteligente sin configurar nada. A cambio, su sintaxis **no es compatible con bash**.

- `→` :: Aceptar la sugerencia gris completa (también `Ctrl+F`)
- `Alt+→` :: Aceptar solo la siguiente palabra de la sugerencia
- `↑` :: Tras escribir el inicio de un comando: busca en el historial los que empiezan así
- `Tab` :: Completar; Tab otra vez muestra un menú navegable
- `Alt+S` :: Anteponer sudo al comando actual
- `Alt+E` :: Abrir el comando actual en tu editor
- `Alt+L` :: Ejecutar ls en el momento
- `Alt+H` :: Ver la ayuda (man) del comando que estás escribiendo
- `fish_config` :: Configurar colores y prompt desde el navegador
- `history search git` :: Buscar en el historial
- `funced nombre` :: Editar una función (luego `funcsave nombre` la guarda para siempre)
- `abbr -a gs 'git status'` :: Abreviatura: escribes gs + espacio y se expande
- `abbr --list` :: Ver tus abreviaturas
- `exec fish` :: Recargar fish (tras editar config.fish)

### 📄 config.fish

Tu configuración vive en `~/.config/fish/config.fish`. Las funciones van en `~/.config/fish/functions/<nombre>.fish` (se cargan solas cuando las usas) y los fragmentos extra en `~/.config/fish/conf.d/`.

```bash
# ~/.config/fish/config.fish
if status is-interactive
    set -gx EDITOR nvim
    fish_add_path ~/.local/bin
    abbr -a gst 'git status -sb'
    abbr -a ll 'eza -la --icons --git'
    abbr -a up 'paru'
    zoxide init fish | source
end
```

### 🧩 Funciones en fish

```bash
# ~/.config/fish/functions/mkcd.fish
function mkcd --description "Crea una carpeta y entra en ella"
    mkdir -p $argv[1]
    and cd $argv[1]
end
```

```bash
# ~/.config/fish/functions/venv.fish
function venv --description "Crea o activa el .venv del proyecto"
    if not test -d .venv
        uv venv
    end
    source .venv/bin/activate.fish
end
```

### 🆚 fish vs bash

| Qué | bash | fish |
|---|---|---|
| asignar variable | `x=5` | `set x 5` |
| exportar | `export X=5` | `set -gx X 5` |
| usar argumentos | `$1`, `$@` | `$argv[1]`, `$argv` |
| sustitución de comando | `$(date)` | `(date)` (fish 3.4+ acepta también `$(date)`) |
| código de salida | `$?` | `$status` |
| y lógico | `cmd1 && cmd2` | `cmd1 && cmd2` o `cmd1; and cmd2` |
| if | `if [ -f x ]; then ...; fi` | `if test -f x; ...; end` |
| for | `for i in 1 2 3; do ...; done` | `for i in 1 2 3; ...; end` |
| función | `f() { ...; }` | `function f; ...; end` |
| alias | `alias ll='ls -l'` | `abbr -a ll 'ls -l'` (o alias) |
| config | `~/.bashrc` | `~/.config/fish/config.fish` |
| repetir con sudo | `sudo !!` | `Alt+S` o escribir sudo y pulsar ↑ |

📌 Los scripts `.sh` con `#!/bin/bash` en la primera línea se ejecutan con bash aunque tu shell sea fish. Solo lo que escribes directamente en la terminal usa la sintaxis de fish.

⚠️ Cuidado: los tutoriales de internet dan comandos de bash. Si un `export` o un `$(...)` antiguo falla en fish, tradúcelo con la tabla o ejecútalo dentro de `bash -c '...'`.

💡 Consejo: prefiere `abbr` a `alias`: al expandirse ves el comando real, lo aprendes y queda bien guardado en el historial.

🇬🇧 **shell** /shel/ = intérprete de comandos · **friendly** /fréndli/ = amigable · **autosuggestion** /otosayéschon/ = autosugerencia · **abbreviation** /abriviéishon/ = abreviatura · **prompt** /prompt/ = indicador de la terminal · **source** /sórs/ = cargar/ejecutar en la shell actual

## 📜 Scripts bash

Un script es una **receta**: una lista de comandos guardados en un archivo para repetirlos cuando quieras. Aunque uses fish a diario, los scripts suelen escribirse en **bash** porque funcionan en cualquier Linux, servidor o contenedor Docker.

```bash
#!/usr/bin/env bash
# La primera línea (shebang) dice qué intérprete usar
set -euo pipefail   # para al primer error, variables sin definir = error, fallos en tuberías

nombre="Yafer"               # variable: SIN espacios alrededor del =
echo "Hola, $nombre"
hoy=$(date +%F)              # guardar la salida de un comando: 2026-10-18
echo "Hoy es $hoy"
```

- `chmod +x script.sh` :: Hacerlo ejecutable
- `./script.sh` :: Ejecutarlo
- `bash -x script.sh` :: Ejecutarlo mostrando cada línea (depurar)
- `shellcheck script.sh` :: Revisar errores típicos (paquete shellcheck). ¡Úsalo siempre!
- `"$variable"` :: Siempre entre comillas dobles (por si tiene espacios)
- `${variable:-defecto}` :: Valor por defecto si está vacía
- `$1 $2 ... $#` :: Argumentos posicionales y cuántos hay
- `"$@"` :: Todos los argumentos, respetando espacios
- `$0` :: Nombre del script
- `$?` :: Código de salida del último comando
- `read -rp "¿Nombre? " nombre` :: Pedir datos al usuario
- `exit 1` :: Terminar con error (0 = éxito)

### 🔀 if, for, while y funciones

```bash
# if con archivos y números
if [[ -f "datos.csv" ]]; then
    echo "existe"
elif [[ -d "datos" ]]; then
    echo "es una carpeta"
else
    echo "no existe"
fi

if (( $# < 1 )); then
    echo "Uso: $0 <archivo>" >&2
    exit 1
fi

# for sobre archivos y rangos
for f in *.png; do
    echo "Procesando $f"
done

for i in {1..5}; do
    echo "Época $i"
done

# while leyendo un archivo línea por línea
while IFS= read -r linea; do
    echo "> $linea"
done < lista.txt

# función con variables locales
saludar() {
    local nombre="$1"
    echo "Hola, $nombre"
}
saludar "Mundo"
```

### 🧪 Pruebas más comunes en [[ ]]

| Prueba | Verdadero si… |
|---|---|
| `-f ruta` | existe y es archivo |
| `-d ruta` | existe y es carpeta |
| `-e ruta` | existe (lo que sea) |
| `-z "$x"` | la cadena está vacía |
| `-n "$x"` | la cadena NO está vacía |
| `"$a" == "$b"` | cadenas iguales |
| `$a -eq $b` | números iguales (`-ne -lt -le -gt -ge`) |
| `-x ruta` | es ejecutable |

### ✅ Ejemplo resuelto: script de respaldo

Situación: quieres respaldar tus carpetas de proyectos en un disco externo, con fecha, comprimido y borrando los respaldos de más de 30 días.

```bash
#!/usr/bin/env bash
# respaldo.sh — uso: ./respaldo.sh [destino]
set -euo pipefail

ORIGEN="$HOME/Proyectos"
DESTINO="${1:-/run/media/$USER/Respaldo}"
FECHA=$(date +%F_%H-%M)
ARCHIVO="$DESTINO/proyectos_$FECHA.tar.zst"

log() { echo "[$(date +%T)] $*"; }

if [[ ! -d "$DESTINO" ]]; then
    echo "❌ No encuentro el destino: $DESTINO (¿conectaste el disco?)" >&2
    exit 1
fi

log "Respaldando $ORIGEN → $ARCHIVO"
tar --zstd -cf "$ARCHIVO" \
    --exclude='.venv' --exclude='node_modules' --exclude='__pycache__' \
    -C "$HOME" Proyectos

TAMANO=$(du -h "$ARCHIVO" | cut -f1)
log "Listo: $TAMANO"

log "Borrando respaldos de más de 30 días"
find "$DESTINO" -name 'proyectos_*.tar.zst' -mtime +30 -print -delete

notify-send "Respaldo terminado" "$ARCHIVO ($TAMANO)"
```

```bash
chmod +x respaldo.sh
./respaldo.sh
```

```text
[10:42:01] Respaldando /home/yafer/Proyectos → /run/media/yafer/Respaldo/proyectos_2026-10-18_10-42.tar.zst
[10:42:37] Listo: 1,3G
[10:42:37] Borrando respaldos de más de 30 días
/run/media/yafer/Respaldo/proyectos_2026-09-10_09-15.tar.zst
```

Para restaurarlo: `tar --zstd -xf proyectos_2026-10-18_10-42.tar.zst -C ~/restaurado/`.

⚠️ Cuidado: `x = 5` (con espacios) en bash NO asigna: intenta ejecutar un comando llamado x. Debe ser `x=5`.

⚠️ Cuidado: sin comillas, `rm $archivo` con un nombre como "mis datos.csv" intenta borrar "mis" y "datos.csv". Escribe siempre `"$archivo"`.

💡 Consejo: `set -euo pipefail` al inicio te ahorra horas: el script se detiene en el primer fallo en vez de seguir haciendo destrozos.

🇬🇧 **script** /skript/ = guion/programa · **shebang** /shibáng/ = línea #! inicial · **argument** /árguiument/ = argumento · **loop** /lup/ = bucle · **statement** /stéitment/ = sentencia · **quote** /kuóut/ = comillas · **exit status** /éksit stéitus/ = estado de salida

## ⌨️ Atajos de teclado de la terminal

Estos atajos (estilo Emacs, vía readline) funcionan en bash, fish, Python interactivo y muchos programas más. Te hacen 3 veces más rápido.

| Atajo | Acción |
|---|---|
| `Ctrl+C` | cancelar el comando en curso |
| `Ctrl+D` | fin de entrada / salir de la shell |
| `Ctrl+L` | limpiar la pantalla |
| `Ctrl+A` | ir al inicio de la línea |
| `Ctrl+E` | ir al final de la línea |
| `Alt+B` / `Alt+F` | palabra atrás / adelante |
| `Ctrl+W` | borrar la palabra anterior |
| `Ctrl+U` | borrar hasta el inicio de la línea |
| `Ctrl+K` | borrar hasta el final de la línea |
| `Ctrl+Y` | pegar lo último borrado |
| `Ctrl+R` | buscar en el historial (en fish abre búsqueda interactiva) |
| `Ctrl+Z` | pausar el programa (fg para volver) |
| `Ctrl+S` / `Ctrl+Q` | congelar / descongelar la salida (si "se colgó" la terminal, prueba Ctrl+Q) |
| `Tab` | completar |
| `↑` / `↓` | comandos anteriores / siguientes |
| `Ctrl+Shift+C` / `Ctrl+Shift+V` | copiar / pegar en la terminal (Ctrl+C solo NO copia) |
| `Alt+.` | insertar el último argumento del comando anterior |

- `!!` :: Bash: el último comando completo
- `!$` :: Bash: el último argumento del comando anterior
- `history` :: Ver el historial
- `clear` :: Limpiar pantalla (igual que Ctrl+L)
- `reset` :: Arreglar una terminal que muestra caracteres raros

💡 Consejo: aprende primero estos cinco: `Ctrl+A`, `Ctrl+E`, `Ctrl+W`, `Ctrl+U`, `Ctrl+R`. Notarás la diferencia el mismo día.

⚠️ Cuidado: en la terminal `Ctrl+C` NO copia, interrumpe. Para copiar usa `Ctrl+Shift+C` (o selecciona con el mouse).

🇬🇧 **shortcut** /shórtcat/ = atajo · **keystroke** /kístrouk/ = pulsación · **clear** /klír/ = limpiar · **history** /jístori/ = historial · **cursor** /kérsor/ = cursor · **cancel** /kánsel/ = cancelar

## ⏰ Tareas programadas: cron y timers

Para ejecutar algo **automáticamente cada cierto tiempo** (respaldos, limpiezas, descargas) hay dos opciones: el clásico **cron** y los **timers de systemd**, que en Arch son los preferidos (tienen logs y recuperan ejecuciones perdidas si el PC estaba apagado).

### 🕐 cron

Instálalo con `sudo pacman -S cronie` y actívalo con `sudo systemctl enable --now cronie`.

- `crontab -e` :: Editar tus tareas programadas
- `crontab -l` :: Ver tus tareas
- `crontab -r` :: Borrar TODAS tus tareas (cuidado)

```text
# ┌──── minuto (0-59)
# │ ┌──── hora (0-23)
# │ │ ┌──── día del mes (1-31)
# │ │ │ ┌──── mes (1-12)
# │ │ │ │ ┌──── día de la semana (0-6, 0 = domingo)
# │ │ │ │ │
  0 21 * * *   /home/yafer/.local/bin/respaldo.sh >> /home/yafer/respaldo.log 2>&1
  */15 * * * * /home/yafer/.local/bin/sync-notas.sh
  0 8 * * 1    /home/yafer/.local/bin/resumen-semanal.sh
```

| Expresión | Significa |
|---|---|
| `0 21 * * *` | todos los días a las 21:00 |
| `*/15 * * * *` | cada 15 minutos |
| `0 8 * * 1` | los lunes a las 8:00 |
| `0 0 1 * *` | el día 1 de cada mes a medianoche |
| `@reboot` | al arrancar el equipo |

### ⏲️ Timers de systemd (recomendado)

Necesitas dos archivos: el `.service` (qué hacer) y el `.timer` (cuándo).

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
Description=Respaldo diario a las 21:00

[Timer]
OnCalendar=*-*-* 21:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

```bash
systemctl --user daemon-reload
systemctl --user enable --now respaldo.timer
systemctl --user list-timers
systemctl --user start respaldo.service      # probarlo ya, sin esperar
journalctl --user -u respaldo.service        # ver cómo le fue
```

- `systemd-analyze calendar "Mon *-*-* 08:00"` :: Comprobar cuándo se ejecutará una expresión OnCalendar
- `OnCalendar=daily` :: Una vez al día (medianoche)
- `OnCalendar=hourly` :: Cada hora
- `OnUnitActiveSec=30min` :: Cada 30 minutos desde la última ejecución
- `Persistent=true` :: Si el PC estaba apagado, ejecuta al encender

💡 Consejo: en cron y en systemd usa **rutas absolutas** y redirige la salida a un log; si no, los errores se pierden en silencio.

⚠️ Cuidado: los servicios de usuario se paran cuando cierras sesión. Para que corran siempre: `sudo loginctl enable-linger yafer`.

🇬🇧 **schedule** /skéchul/ = programar (en el tiempo) · **timer** /táimer/ = temporizador · **daily** /déili/ = diario · **hourly** /áuerli/ = cada hora · **weekly** /uíkli/ = semanal · **oneshot** /uán shot/ = una sola vez

## 🩺 Logs y depurar problemas

Cuando algo falla, **no adivines: lee los mensajes**. Linux registra casi todo. El método: 1) reproducir el problema, 2) leer el error completo, 3) buscar en los logs, 4) cambiar una cosa a la vez.

- `journalctl -b -p err` :: Errores desde que encendiste
- `journalctl -f` :: Todo lo que pasa en vivo (provoca el fallo y míralo)
- `journalctl -u NetworkManager --since today` :: Logs de un servicio hoy
- `sudo dmesg -w` :: Mensajes del kernel en vivo (conectar USB, GPU, discos)
- `systemctl --failed` :: Servicios caídos
- `coredumpctl list` :: Programas que se estrellaron (crash)
- `coredumpctl info` :: Detalles del último crash
- `hyprctl rollinglog` :: Log de Hyprland
- `cat /var/log/pacman.log | rg -i "upgraded" | tail` :: Qué se actualizó últimamente (¿se rompió tras actualizar?)
- `programa --verbose` :: Muchos programas explican más con -v o --verbose
- `strace -f -e trace=openat programa` :: Ver qué archivos intenta abrir un programa
- `ldd /usr/bin/programa` :: Librerías que necesita (busca "not found")
- `lspci -k` :: Hardware PCI y qué driver usa (GPU, Wi-Fi)
- `lsusb` :: Dispositivos USB conectados
- `inxi -Fxz` :: Resumen completo del hardware (para pedir ayuda en foros)
- `nvidia-smi` :: Estado de la GPU NVIDIA (memoria, procesos, temperatura)
- `sensors` :: Temperaturas (paquete lm_sensors)

### ✅ Ejemplo resuelto: el Wi-Fi dejó de funcionar tras actualizar

```bash
nmcli device                                        # 1. ¿la tarjeta aparece?
journalctl -b -u NetworkManager -p warning          # 2. errores del servicio
sudo dmesg | rg -i "wlan|iwlwifi|firmware"          # 3. ¿el kernel cargó el driver?
rg -i "upgraded (linux|.*firmware)" /var/log/pacman.log | tail -3   # 4. ¿qué cambió?
```

```text
[    4.120] iwlwifi 0000:00:14.3: Direct firmware load for iwlwifi-so-a0-gf-a0-89.ucode failed with error -2
```

El kernel no encuentra el firmware: se actualizó el kernel pero falta `linux-firmware`. Solución:

```bash
sudo pacman -Syu linux-firmware
reboot
```

📌 Si el sistema no arranca tras una actualización, en CachyOS puedes elegir un snapshot anterior de Btrfs en el menú de arranque o entrar con el USB de instalación y usar `arch-chroot`.

💡 Consejo: cuando pidas ayuda (foros, Discord, IA), pega el comando exacto, el error completo y la salida de `inxi -Fxz`. "No funciona" no se puede depurar.

⚠️ Cuidado: no copies "soluciones" con `sudo` de foros sin entender qué hacen. Lee cada comando; si no sabes qué hace, busca en `man`.

🇬🇧 **log** /log/ = registro · **debug** /dibág/ = depurar · **crash** /krash/ = estrellarse/fallo · **driver** /dráiver/ = controlador · **troubleshoot** /trábolshut/ = solucionar problemas · **warning** /uórnin/ = aviso · **stack trace** /stak tréis/ = traza de llamadas

## 🛡️ Seguridad básica

Linux es seguro por diseño, pero la seguridad depende sobre todo de **tus hábitos**. Lo esencial: sistema actualizado, sudo con cuidado, firewall activo, llaves SSH en vez de contraseñas y nunca ejecutar scripts que no entiendes.

- `sudo pacman -Syu` :: Actualizar a menudo: la mayoría de ataques usan fallos ya corregidos
- `sudo ufw enable` :: Activar el firewall (paquete ufw)
- `sudo ufw default deny incoming` :: Bloquear todo lo que entra por defecto
- `sudo ufw allow ssh` :: Permitir SSH (si lo necesitas)
- `sudo ufw status verbose` :: Ver las reglas
- `ss -tulpn` :: Revisar qué puertos están abiertos (cierra lo que no uses)
- `chmod 600 ~/.ssh/id_ed25519` :: La llave privada solo legible por ti
- `chmod 700 ~/.ssh` :: La carpeta .ssh privada
- `last` :: Últimos inicios de sesión
- `journalctl -u sshd | rg "Failed"` :: Intentos fallidos de entrar por SSH
- `passwd` :: Cambiar tu contraseña
- `gpg -c secreto.txt` :: Cifrar un archivo con contraseña (crea secreto.txt.gpg)
- `gpg -d secreto.txt.gpg > secreto.txt` :: Descifrarlo
- `sha256sum archivo.iso` :: Verificar que una descarga no fue alterada
- `paru -Gp paquete` :: Leer el PKGBUILD de un paquete del AUR ANTES de instalarlo
- `keepassxc` :: Gestor de contraseñas gráfico (o `pass` en terminal), en vez de un .txt

### 🔐 Endurecer SSH (si tienes un servidor)

```text
# /etc/ssh/sshd_config
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
```

```bash
sudo systemctl restart sshd
```

### 📋 Checklist del buen hábito

| Hábito | Por qué |
|---|---|
| Actualizar al menos una vez por semana | parches de seguridad |
| No ejecutar `curl ... | sh` de sitios desconocidos | ejecutas código ajeno sin verlo |
| Revisar PKGBUILD del AUR | cualquiera puede subir paquetes |
| No trabajar como root | un error como root rompe el sistema |
| Secretos en `.env` + `.gitignore` | no filtrar claves a GitHub |
| Contraseñas distintas + gestor | si cae una, no caen todas |
| Respaldos automáticos (3-2-1) | 3 copias, 2 medios, 1 fuera de casa |

⚠️ Cuidado: un comando con `curl https://... | sudo bash` le da control total de tu PC a un script de internet. Descárgalo primero, léelo y luego ejecútalo.

💡 Consejo: activa la verificación en dos pasos (2FA) en GitHub y en tu correo; es lo que más protege tus cuentas de estudiante.

🇬🇧 **security** /sekiúriti/ = seguridad · **firewall** /fáieruol/ = cortafuegos · **encrypt** /enkrípt/ = cifrar · **password** /pásuerd/ = contraseña · **vulnerability** /valnerabíliti/ = vulnerabilidad · **two-factor authentication** /tu fáktor ozentikéishon/ = verificación en dos pasos · **hardening** /járdenin/ = endurecimiento

## 🧰 Ayuda y aprender más

Nadie memoriza todas las opciones. Lo importante es **saber dónde buscar** rápido desde la terminal.

- `man tar` :: El manual oficial de un comando (/ para buscar, q para salir)
- `man -k comprimir` :: Buscar manuales por palabra clave (apropos)
- `tldr tar` :: Ejemplos prácticos y cortos (paquete tealdeer)
- `comando --help` :: Ayuda rápida de casi cualquier programa
- `help` :: En fish: abre la documentación de fish
- `whatis ls` :: Descripción de una línea
- `type -a python` :: Todas las versiones de un comando en el PATH
- `cheat.sh/tar` :: `curl cheat.sh/tar` da una chuleta al instante
- `wiki.archlinux.org` :: La Arch Wiki: la mejor documentación de Linux que existe

📌 En los manuales: `[opción]` entre corchetes es opcional, `<archivo>` es obligatorio y `...` significa "uno o más".

💡 Consejo: cuando aprendas un comando nuevo, haz primero `tldr comando`, luego pruébalo en una carpeta de pruebas en `/tmp`, y por último lee el `man` para los detalles.

🇬🇧 **manual (man)** /mániual/ = manual · **help** /jelp/ = ayuda · **option** /ópshon/ = opción · **flag** /flag/ = bandera/opción · **usage** /iúsech/ = modo de uso · **keyword** /kíuerd/ = palabra clave
