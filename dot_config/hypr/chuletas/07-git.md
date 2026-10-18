# 🌿 Git
> Guarda la historia de tu código, trabaja en ramas sin miedo y colabora en GitHub como un profesional.

## 🧠 Cómo funciona Git

Git es una **máquina del tiempo para carpetas**. Cada vez que haces un *commit* sacas una "foto" completa de tu proyecto, y puedes volver a cualquier foto cuando quieras. No guarda copias tontas tipo `final_v2_ahora_si.py`: guarda solo lo que cambió y lo encadena.

Piensa en una **sesión de fotos**: el escenario es tu carpeta (working directory), el grupo que pones delante de la cámara es el *staging area* (con `git add` eliges quién sale en la foto) y el álbum es el repositorio (con `git commit` pegas la foto en el álbum para siempre).

```text
 TU CARPETA              ZONA DE PREPARACIÓN        REPOSITORIO (.git)
 (working directory)     (staging / index)          (historial de commits)

  app.py  ✏️ editado  ── git add ──▶  app.py  ── git commit ──▶  ● a1b2c3 "feat: login"
  test.py ✏️ editado                                               │
                       ◀── git restore --staged ──                 ● 9f8e7d "fix: typo"
           ◀──────────── git restore ───────────                    │
                                                                    ● 1a2b3c "primer commit"
                                         git push ▼   ▲ git pull / fetch
                                   ┌────────────────────────────┐
                                   │ REMOTO (GitHub: origin)    │
                                   └────────────────────────────┘
```

Cada archivo está en uno de estos estados: **untracked** (Git no lo conoce), **modified** (cambió pero no está preparado), **staged** (preparado para el próximo commit) y **committed** (guardado en el historial).

### 🔑 Conceptos clave

- `commit` :: Foto del proyecto con autor, fecha, mensaje y un ID único (hash SHA, ej. a1b2c3d)
- `HEAD` :: Puntero que dice "estás aquí": normalmente apunta a la rama actual
- `branch` :: Etiqueta móvil que apunta a un commit; avanza sola cuando haces commits
- `origin` :: Nombre por defecto del repositorio remoto (normalmente GitHub)
- `main` :: Nombre habitual de la rama principal (antes se usaba master)
- `.git/` :: Carpeta oculta donde vive TODO el historial; si la borras, pierdes el historial

📌 Git es local: funciona sin internet. GitHub es solo un servidor donde guardas una copia para compartirla. Git ≠ GitHub.

💡 Consejo: ejecuta `git status` cada vez que dudes. Es gratis, no rompe nada y casi siempre te dice qué comando usar a continuación.

⚠️ Cuidado: Git solo protege lo que está en un commit. Si editas un archivo y lo descartas antes de hacer commit, eso no se puede recuperar.

🇬🇧 **repository** /ripózitori/ = repositorio · **working directory** /uérkin dairéktori/ = carpeta de trabajo · **staging area** /stéiyin éria/ = zona de preparación · **snapshot** /snápshot/ = foto/instantánea · **track** /trak/ = seguir/rastrear

## ⚙️ Configuración inicial y SSH con GitHub

Lo primero en una máquina nueva: decirle a Git quién eres (sale en cada commit) y conectar tu PC con GitHub por SSH, para no escribir contraseñas nunca más. Se hace **una sola vez** por computadora.

- `git config --global user.name "Yafer Torrez"` :: Tu nombre para todos los repos
- `git config --global user.email "tu@correo.com"` :: Tu correo (usa el mismo de GitHub)
- `git config --global init.defaultBranch main` :: Que los repos nuevos empiecen con la rama main
- `git config --global core.editor nvim` :: Editor para mensajes de commit (o nano, o "code --wait")
- `git config --global pull.rebase false` :: git pull hace merge (comportamiento clásico y predecible)
- `git config --global push.autoSetupRemote true` :: El primer push de una rama crea su upstream solo
- `git config --global color.ui auto` :: Colores en la salida
- `git config --list --show-origin` :: Ver toda tu configuración y de qué archivo sale
- `git config user.email "otro@uni.edu"` :: Sin --global: solo para el repo actual (útil para la universidad)

La configuración global se guarda en `~/.gitconfig`. Puedes abrirlo y editarlo a mano.

### 🔐 Conectar con GitHub por SSH

SSH funciona con un par de llaves: la **privada** se queda en tu PC (como la llave de tu casa) y la **pública** se la das a GitHub (como la cerradura). Solo quien tenga la privada puede abrir.

```bash
# 1. Crear el par de llaves (Enter para aceptar la ruta; pon una frase de paso)
ssh-keygen -t ed25519 -C "tu@correo.com"

# 2. Ver la llave PÚBLICA (la que termina en .pub) y copiarla
cat ~/.ssh/id_ed25519.pub
wl-copy < ~/.ssh/id_ed25519.pub      # en Hyprland/Wayland la copia al portapapeles

# 3. Pegarla en GitHub: Settings → SSH and GPG keys → New SSH key
#    (o con gh CLI:)
gh ssh-key add ~/.ssh/id_ed25519.pub --title "CachyOS PC"

# 4. Probar la conexión
ssh -T git@github.com
```

Salida esperada del paso 4:

```text
Hi yftorrezg! You've successfully authenticated, but GitHub does not provide shell access.
```

- `git clone git@github.com:usuario/repo.git` :: Clonar por SSH (no pide contraseña)
- `git remote set-url origin git@github.com:usuario/repo.git` :: Pasar un repo de HTTPS a SSH
- `gh auth login` :: Alternativa: iniciar sesión con la CLI de GitHub (elige SSH)

⚠️ Cuidado: NUNCA compartas ni subas `~/.ssh/id_ed25519` (sin .pub). Esa es la llave privada. Solo la `.pub` va a GitHub.

💡 Consejo: si `ssh -T` dice "Permission denied (publickey)", revisa que copiaste la `.pub` correcta y que el agente la tiene cargada con `ssh-add -l`.

🇬🇧 **key pair** /ki per/ = par de llaves · **passphrase** /pásfreis/ = frase de paso · **authenticate** /ozéntikeit/ = autenticar · **settings** /sétins/ = ajustes · **global** /glóubal/ = global

## 🔄 Flujo diario

El 90 % de tu vida con Git es este ciclo: **editar → ver qué cambió → preparar → guardar → subir**. Apréndelo de memoria.

- `git init` :: Convierte la carpeta actual en repositorio (crea .git/)
- `git clone <url>` :: Descarga un repo completo con todo su historial
- `git status` :: Qué cambió, qué está preparado y en qué rama estás
- `git status -s` :: Versión corta: M = modificado, A = añadido, ?? = no rastreado
- `git add app.py` :: Preparar un archivo concreto
- `git add .` :: Preparar todo lo que cambió en la carpeta actual (y subcarpetas)
- `git add -p` :: Preparar por trozos: Git te pregunta pedazo por pedazo (y/n). ¡Muy útil!
- `git commit -m "feat: añade login"` :: Guardar la foto con un mensaje
- `git commit` :: Sin -m: abre tu editor para escribir un mensaje largo
- `git commit -am "fix: corrige suma"` :: add + commit de archivos YA rastreados (no incluye nuevos)
- `git push` :: Subir tus commits al remoto
- `git pull` :: Bajar los commits del remoto y unirlos a tu rama
- `git rm archivo.txt` :: Borrar un archivo y preparar el borrado
- `git rm --cached secreto.env` :: Dejar de rastrear un archivo sin borrarlo del disco
- `git mv viejo.py nuevo.py` :: Renombrar/mover y que Git lo registre

### ✅ Ejemplo resuelto: tu primer repositorio y subirlo a GitHub

Situación: tienes una carpeta `tarea-ia` con un script de Python y quieres versionarla y subirla.

```bash
cd ~/Proyectos/tarea-ia
git init
echo "__pycache__/" > .gitignore
git add .
git status -s
git commit -m "feat: primer modelo de regresión"
gh repo create tarea-ia --private --source=. --push
```

Salida esperada de `git status -s` y del commit:

```text
A  .gitignore
A  modelo.py
[main (commit-raíz) 3f2a1bc] feat: primer modelo de regresión
 2 files changed, 41 insertions(+)
 create mode 100644 .gitignore
 create mode 100644 modelo.py
```

Al día siguiente, el ciclo normal es:

```bash
git pull                         # 1. traer lo último (por si trabajaste en la laptop)
nvim modelo.py                   # 2. trabajar
git status                       # 3. ver qué cambió
git diff                         # 4. revisar los cambios exactos
git add modelo.py                # 5. preparar
git commit -m "feat: añade normalización de datos"
git push                         # 6. subir
```

💡 Consejo: haz commits **pequeños y frecuentes**, uno por idea. "feat: añade login" es mejor que un commit gigante "cambios del lunes".

⚠️ Cuidado: `git add .` añade TODO, incluso archivos de 2 GB o un `.env` con contraseñas. Mira `git status` antes y usa un buen `.gitignore`.

🇬🇧 **stage** /stéich/ = preparar · **commit** /komít/ = confirmar/guardar versión · **push** /push/ = empujar/subir · **pull** /pul/ = jalar/bajar · **clone** /klóun/ = clonar · **untracked** /antrákt/ = sin rastrear

## 🔍 Ver historial y diferencias

El historial es tu diario de desarrollo. Saber leerlo te permite responder: ¿qué cambió?, ¿quién lo cambió?, ¿cuándo se rompió?

- `git log` :: Historial completo (q para salir, espacio para avanzar)
- `git log --oneline` :: Una línea por commit: hash corto + mensaje
- `git log --oneline --graph --all` :: Dibujo de todas las ramas como un árbol
- `git log -5` :: Solo los últimos 5 commits
- `git log -p app.py` :: Historial de un archivo con los cambios de cada commit
- `git log --author="Yafer"` :: Commits de un autor
- `git log --since="2 weeks ago"` :: Commits de las últimas dos semanas
- `git log --grep="login"` :: Commits cuyo mensaje contiene "login"
- `git log -S "def entrenar"` :: Commits que añadieron o quitaron ese texto (buscador de código)
- `git log main..mi-rama` :: Commits que están en mi-rama pero no en main
- `git show a1b2c3d` :: Ver un commit concreto: mensaje y cambios
- `git show HEAD~1:app.py` :: Ver cómo era app.py hace un commit
- `git diff` :: Cambios NO preparados (carpeta vs staging)
- `git diff --staged` :: Cambios preparados (lo que entrará en el próximo commit)
- `git diff main..mi-rama` :: Diferencias entre dos ramas
- `git diff --stat` :: Resumen: qué archivos cambiaron y cuántas líneas
- `git blame app.py` :: Quién escribió cada línea y en qué commit
- `git shortlog -sn` :: Ranking de commits por autor

### 🧭 Cómo nombrar commits

| Forma | Significa | Ejemplo |
|---|---|---|
| `a1b2c3d` | hash (basta con 7 caracteres) | `git show a1b2c3d` |
| `HEAD` | el commit donde estás | `git show HEAD` |
| `HEAD~1` | el padre de HEAD (uno atrás) | `git diff HEAD~1` |
| `HEAD~3` | tres commits atrás | `git reset --soft HEAD~3` |
| `main` | último commit de la rama main | `git log main` |
| `origin/main` | main del remoto (según el último fetch) | `git diff origin/main` |
| `v1.0` | un tag | `git checkout v1.0` |

### ✅ Ejemplo resuelto: leer un diff

```text
diff --git a/calc.py b/calc.py
index 3b18e51..a9c2f04 100644
--- a/calc.py
+++ b/calc.py
@@ -1,4 +1,4 @@
 def promedio(notas):
-    return sum(notas) / 10
+    return sum(notas) / len(notas)
```

Se lee así: `---` es la versión vieja y `+++` la nueva. `@@ -1,4 +1,4 @@` indica que el trozo empieza en la línea 1. Las líneas con `-` (rojo) se quitaron y las de `+` (verde) se añadieron. Aquí se corrigió un bug: el promedio dividía siempre entre 10.

💡 Consejo: instala `git-delta` (`sudo pacman -S git-delta`) y configúralo con `git config --global core.pager delta`: los diffs salen con colores y resaltado de sintaxis.

⚠️ Cuidado: `git diff` sin opciones NO muestra lo que ya preparaste con `git add`. Si "no ves nada", prueba `git diff --staged`.

🇬🇧 **log** /log/ = registro · **diff** /dif/ = diferencia · **blame** /bleim/ = culpar · **author** /ózor/ = autor · **since** /sins/ = desde · **show** /shou/ = mostrar

## 🌱 Ramas

Una rama es una **línea de tiempo paralela**. Imagina que escribes una tesis: en vez de arriesgar el documento bueno, haces una copia para probar un capítulo nuevo. Si sale bien, la unes; si sale mal, la tiras. Con Git eso cuesta cero: una rama es solo una etiqueta de 41 bytes que apunta a un commit.

```text
               ● ─ ● ─ ●   feature/login   (tu experimento)
              /
  ● ─ ● ─ ● ─ ● ─ ●        main            (lo que funciona)
                  ▲
                 HEAD
```

- `git branch` :: Listar ramas locales (la actual con *)
- `git branch -a` :: Listar también las remotas (remotes/origin/...)
- `git branch -vv` :: Ramas con su último commit y a qué rama remota siguen
- `git switch -c feature/login` :: Crear una rama nueva y pasarte a ella
- `git switch main` :: Cambiar a la rama main
- `git switch -` :: Volver a la rama anterior (como cd -)
- `git branch -m nuevo-nombre` :: Renombrar la rama actual
- `git branch -d feature/login` :: Borrar una rama ya fusionada (seguro)
- `git branch -D experimento` :: Borrar una rama aunque no esté fusionada (¡pierdes sus commits!)
- `git branch --merged` :: Ramas ya unidas a la actual (se pueden borrar)
- `git push origin --delete feature/login` :: Borrar la rama en GitHub
- `git checkout -b feature/login` :: Forma antigua de crear y cambiar (equivale a switch -c)

### 🏷️ Nombres de rama recomendados

| Prefijo | Para qué | Ejemplo |
|---|---|---|
| `feature/` | funcionalidad nueva | `feature/chat-ia` |
| `fix/` | corregir un bug | `fix/division-cero` |
| `docs/` | documentación | `docs/readme-instalacion` |
| `refactor/` | reorganizar código sin cambiar qué hace | `refactor/separar-modelos` |
| `exp/` | experimento que quizá tires | `exp/probar-transformer` |

📌 `git switch` y `git restore` son los comandos modernos (desde Git 2.23). `git checkout` hace las dos cosas a la vez y por eso confunde; lo verás mucho en tutoriales viejos.

💡 Consejo: crea una rama para cada tarea, aunque trabajes solo. Así `main` siempre funciona y puedes entregar a tiempo aunque el experimento esté a medias.

⚠️ Cuidado: si cambias de rama con cambios sin guardar, Git los lleva contigo o se niega ("Your local changes would be overwritten"). Haz commit o `git stash` antes.

🇬🇧 **branch** /branch/ = rama · **switch** /suítch/ = cambiar · **feature** /fícher/ = funcionalidad · **checkout** /chékaut/ = sacar/cambiar a · **delete** /dilít/ = borrar

## 🔀 Merge y resolver conflictos

`git merge` **une** el trabajo de otra rama en la rama donde estás. Siempre se hace "desde el destino": te paras en `main` y traes la otra rama.

Hay dos casos. **Fast-forward**: main no avanzó mientras trabajabas, así que Git solo mueve la etiqueta hacia adelante (no hay commit nuevo). **Merge de tres vías**: ambas ramas avanzaron, así que Git crea un *commit de merge* con dos padres.

```text
Antes:                         Después de git merge feature:
      ● ─ ●  feature                 ● ─ ● ───┐
     /                              /          \
● ─ ● ─ ●    main            ● ─ ● ─ ● ──────── ◆  main (commit de merge)
```

- `git merge feature/login` :: Unir feature/login a la rama actual
- `git merge --no-ff feature/login` :: Forzar un commit de merge aunque se pudiera hacer fast-forward
- `git merge --squash feature/login` :: Juntar todos sus commits en cambios preparados (luego haces 1 commit)
- `git merge --abort` :: Cancelar un merge con conflictos y volver a como estabas
- `git diff --name-only --diff-filter=U` :: Listar solo los archivos en conflicto
- `git checkout --ours app.py` :: En un conflicto: quedarte con TU versión del archivo
- `git checkout --theirs app.py` :: En un conflicto: quedarte con la versión de la OTRA rama
- `git mergetool` :: Abrir una herramienta visual para resolver conflictos

Un **conflicto** ocurre cuando las dos ramas cambiaron **las mismas líneas** de distinta forma. Git no adivina cuál es la buena: te marca el trozo y te deja decidir a ti. No es un error, es una pregunta.

### ✅ Ejemplo resuelto: conflicto real

Situación: en `main` cambiaste el saludo a "Buenas" y tu compañera, en la rama `ingles`, lo cambió a "Hello". Ahora fusionas:

```bash
git switch main
git merge ingles
```

Salida esperada (Git en español):

```text
Auto-fusionando app.py
CONFLICTO (contenido): Conflicto de fusión en app.py
Fusión automática falló; arregle los conflictos y luego realice un commit con el resultado.
```

Abres `app.py` y ves las marcas de conflicto:

```text
<<<<<<< HEAD
saludo = 'Buenas'
=======
saludo = 'Hello'
>>>>>>> ingles
```

Se lee así: entre `<<<<<<< HEAD` y `=======` está **tu versión** (la rama donde estás, main). Entre `=======` y `>>>>>>> ingles` está **la versión que llega** de la otra rama.

Paso 1: edita el archivo y deja el resultado final, **borrando las tres marcas**. Puedes elegir una, la otra o combinarlas:

```text
saludo = 'Buenas / Hello'
```

Paso 2: marca el conflicto como resuelto y termina el merge:

```bash
git add app.py
git status                  # ya no dice "Rutas no fusionadas"
git commit                  # Git propone el mensaje "Merge branch 'ingles'"
git log --oneline --graph -4
```

```text
*   7c1d9e2 (HEAD -> main) Merge branch 'ingles'
|\
| * 4b2a8f1 (ingles) feat: saludo en inglés
* | 9e0f3a7 feat: saludo boliviano
|/
* 3f2a1bc feat: saludo
```

💡 Consejo: en VS Code, los conflictos salen con botones "Accept Current / Accept Incoming / Accept Both". En nvim, busca `<<<<` con `/<<<<` para saltar entre conflictos.

⚠️ Cuidado: no hagas `git add` hasta borrar TODAS las marcas `<<<<<<<`, `=======` y `>>>>>>>`. Si las dejas, el código se rompe y Git no te avisa. Busca restos con `rg '^(<<<<<<<|>>>>>>>)'`.

⚠️ Cuidado: si te asustas a mitad, `git merge --abort` te devuelve exactamente a como estabas antes del merge.

🇬🇧 **merge** /merch/ = fusionar · **conflict** /cónflikt/ = conflicto · **ours** /áuers/ = lo nuestro · **theirs** /zérs/ = lo de ellos · **incoming** /íncomin/ = entrante · **resolve** /rizólv/ = resolver · **abort** /abórt/ = abortar

## 📐 Rebase: historial limpio

`git rebase main` toma tus commits y los **vuelve a aplicar encima** del último main, como si hubieras empezado tu rama hoy. El resultado es un historial recto, sin commits de merge.

Analogía: merge es decir "estas dos historias se juntaron aquí". Rebase es **reescribir** tu historia para que parezca que siempre fue después. Por eso los commits rebasados reciben hashes nuevos: son commits distintos.

```text
Antes:                          Después de git rebase main (en feature):
      A ─ B   feature                         A' ─ B'  feature
     /                                       /
● ─ ● ─ C     main               ● ─ ● ─ C   main
```

- `git rebase main` :: Reaplicar los commits de tu rama encima de main
- `git pull --rebase` :: Bajar cambios y poner tus commits locales encima (sin commit de merge)
- `git rebase -i HEAD~3` :: Rebase interactivo: editar, unir o reordenar los últimos 3 commits
- `git rebase --continue` :: Seguir después de resolver un conflicto (tras git add)
- `git rebase --skip` :: Saltar el commit que da conflicto
- `git rebase --abort` :: Cancelar todo el rebase y volver a como estabas
- `git push --force-with-lease` :: Subir una rama rebasada (forzado, pero seguro si nadie más subió)

### 🧹 Rebase interactivo: limpiar antes del PR

```text
pick 1a2b3c4 feat: añade modelo
pick 5d6e7f8 wip
pick 9a8b7c6 arreglo typo
# Cambia "pick" por:
#   reword (r) = cambiar el mensaje      squash (s) = unir con el anterior
#   fixup  (f) = unir y tirar el mensaje drop   (d) = borrar el commit
#   edit   (e) = parar para modificarlo  (también puedes reordenar las líneas)
```

Si cambias `pick` por `f` en las dos últimas líneas y guardas, te queda un solo commit limpio "feat: añade modelo".

### ✅ ¿Cuándo sí y cuándo no?

| Situación | ¿Rebase? | Por qué |
|---|---|---|
| Tu rama local aún no subida | ✅ sí | nadie más la tiene |
| Actualizar tu rama de PR con main | ✅ sí (con force-with-lease) | historial limpio para revisar |
| Limpiar commits "wip" antes del PR | ✅ sí (`-i`) | se ve profesional |
| main o una rama compartida | ❌ nunca | cambias hashes que otros ya tienen |
| No entiendes bien qué pasa | ❌ usa merge | merge no reescribe nada |

📌 Regla de oro: **no hagas rebase de commits que otros ya bajaron**. Rebase solo en lo tuyo y local.

💡 Consejo: si un rebase salió mal, `git reflog` muestra dónde estabas antes y puedes volver con `git reset --hard HEAD@{n}`.

⚠️ Cuidado: nunca uses `git push --force` a secas en una rama compartida: borra los commits que otros subieron. Usa `--force-with-lease`, que se niega si el remoto cambió.

🇬🇧 **rebase** /ribéis/ = cambiar la base · **squash** /skuásh/ = aplastar/unir · **reword** /riuérd/ = reescribir · **pick** /pik/ = escoger · **lease** /lis/ = arriendo (aquí: garantía) · **rewrite history** /riráit jístori/ = reescribir historia

## ↩️ Deshacer cosas

Git casi nunca pierde nada que esté en un commit. La clave es saber **en qué zona** está lo que quieres deshacer: carpeta, staging, commit local o commit ya subido.

### 🗺️ Tabla: quiero… → comando

| Quiero… | Comando | ¿Peligroso? |
|---|---|---|
| descartar cambios de un archivo sin commit | `git restore app.py` | ⚠️ pierdes esos cambios |
| sacar un archivo del staging (deshacer add) | `git restore --staged app.py` | no |
| cambiar el mensaje del último commit | `git commit --amend -m "nuevo msg"` | solo si no lo subiste |
| añadir un archivo olvidado al último commit | `git add olvidado.py` y `git commit --amend --no-edit` | solo si no lo subiste |
| deshacer el último commit pero conservar los cambios preparados | `git reset --soft HEAD~1` | no |
| deshacer el último commit y dejar los cambios sin preparar | `git reset HEAD~1` (es --mixed) | no |
| borrar el último commit Y sus cambios | `git reset --hard HEAD~1` | ⚠️ sí |
| dejar todo igual al remoto | `git fetch` y `git reset --hard origin/main` | ⚠️ sí |
| deshacer un commit ya subido | `git revert a1b2c3d` | no (crea commit nuevo) |
| recuperar un archivo de un commit viejo | `git restore --source=a1b2c3d app.py` | no |
| borrar archivos no rastreados (basura) | `git clean -n` y luego `git clean -fd` | ⚠️ sí |
| rescatar algo que "perdí" con reset | `git reflog` y `git reset --hard HEAD@{2}` | no |
| recuperar una rama borrada | `git reflog` y `git branch rama a1b2c3d` | no |

### 🎚️ Los tres reset

`git reset` mueve la rama hacia atrás. La opción decide qué pasa con los cambios de los commits que "quitas":

| Opción | Historial | Staging | Tu carpeta | Úsalo para |
|---|---|---|---|---|
| `--soft` | retrocede | conserva los cambios preparados | intacta | rehacer el commit (unir varios en uno) |
| `--mixed` (por defecto) | retrocede | se vacía | intacta | volver a elegir qué preparar |
| `--hard` | retrocede | se vacía | ⚠️ se borra | tirar todo a la basura |

### 🛟 reflog: la caja negra

`git reflog` registra **cada movimiento de HEAD** (commits, resets, rebases, cambios de rama) durante unos 90 días. Aunque un commit ya no aparezca en `git log`, sigue en el reflog.

### ✅ Ejemplo resuelto: rescatar commits tras un reset --hard

Situación: hiciste `git reset --hard HEAD~2` por error y desaparecieron dos commits con tu trabajo de la semana.

```bash
git reflog
```

```text
3f2a1bc (HEAD -> main) HEAD@{0}: reset: moving to HEAD~2
8d7e6f5 HEAD@{1}: commit: feat: evaluación del modelo
c4b3a21 HEAD@{2}: commit: feat: entrenamiento
3f2a1bc HEAD@{3}: commit: feat: carga de datos
```

El estado bueno es `HEAD@{1}` (antes del reset). Vuelves allí:

```bash
git reset --hard HEAD@{1}       # o: git reset --hard 8d7e6f5
git log --oneline -3
```

```text
8d7e6f5 (HEAD -> main) feat: evaluación del modelo
c4b3a21 feat: entrenamiento
3f2a1bc feat: carga de datos
```

¡Recuperado! 🎉

### ✅ Ejemplo resuelto: revertir un commit que ya está en GitHub

Situación: subiste `a1b2c3d` y rompió la app. Tus compañeros ya hicieron pull, así que no puedes reescribir la historia.

```bash
git revert a1b2c3d              # crea un commit nuevo que hace lo contrario
git push
```

```text
[main 5e6f7a8] Revert "feat: cache agresiva"
 1 file changed, 3 insertions(+), 12 deletions(-)
```

📌 Resumen: **¿ya lo subiste? → revert.** ¿Solo está en tu PC? → reset o amend.

💡 Consejo: antes de algo arriesgado (reset --hard, rebase), crea una rama de respaldo: `git branch respaldo`. Si algo sale mal, `git reset --hard respaldo`.

⚠️ Cuidado: `git reset --hard` y `git clean -fd` borran cambios **no guardados en commits**, y esos NO están en el reflog. Ejecuta `git clean -n` primero para ver qué borraría.

🇬🇧 **undo** /andú/ = deshacer · **restore** /ristór/ = restaurar · **reset** /risét/ = reiniciar · **revert** /rivért/ = revertir · **amend** /aménd/ = enmendar/corregir · **discard** /diskárd/ = descartar · **rescue** /réskiu/ = rescatar

## 📦 Stash: guardar cambios a un lado

`git stash` es un **cajón**: guardas ahí tus cambios a medias, dejas la carpeta limpia, haces otra cosa (cambiar de rama, hacer pull, arreglar un bug urgente) y después sacas los cambios del cajón.

- `git stash` :: Guardar cambios de archivos rastreados y limpiar la carpeta
- `git stash -u` :: Incluir también archivos nuevos (untracked)
- `git stash push -m "mitad del login"` :: Guardar con una descripción
- `git stash list` :: Ver todo lo guardado (stash@{0} es el más reciente)
- `git stash show -p stash@{0}` :: Ver los cambios de un stash
- `git stash pop` :: Sacar el último y borrarlo del cajón
- `git stash apply stash@{1}` :: Aplicar uno concreto sin borrarlo
- `git stash drop stash@{1}` :: Borrar un stash
- `git stash branch nueva-rama` :: Crear una rama a partir del stash (si al aplicarlo hay conflictos)
- `git stash clear` :: Vaciar el cajón entero (cuidado)

### ✅ Ejemplo resuelto: bug urgente a mitad de trabajo

Situación: estás a medio programar en `feature/chat` y te avisan que `main` tiene un bug que hay que arreglar YA.

```bash
git stash push -u -m "chat a medias"
git switch main
git switch -c fix/division-cero
# ... arreglas el bug ...
git commit -am "fix: evita división por cero en promedio"
git switch feature/chat
git stash pop
```

```text
En la rama feature/chat
Cambios no rastreados para el commit:
        modificados:     chat.py
Descartando refs/stash@{0} (b1c2d3e...)
```

Tu trabajo a medias volvió intacto.

💡 Consejo: dale siempre un mensaje con `-m`. Tres semanas después, "WIP on main" no te dice nada.

⚠️ Cuidado: el stash no es un respaldo a largo plazo. Si algo te importa más de un día, mejor haz un commit en una rama ("wip: chat a medias").

🇬🇧 **stash** /stash/ = esconder/guardar a un lado · **pop** /pop/ = sacar · **apply** /aplái/ = aplicar · **drop** /drop/ = soltar/borrar · **WIP (work in progress)** /uérk in prógres/ = trabajo en curso

## 🌐 Remotos: fetch, pull y push

Un remoto es otra copia del repo (normalmente en GitHub). Tu repo local y el remoto **no se sincronizan solos**: tú decides cuándo bajar (`fetch`/`pull`) y cuándo subir (`push`).

`git fetch` baja las novedades pero **no toca tu código** (las guarda en `origin/main`). `git pull` = `fetch` + `merge` (o rebase). Es como revisar el correo (fetch) frente a abrirlo y aplicarlo (pull).

- `git remote -v` :: Ver los remotos y sus URLs
- `git remote add origin git@github.com:yo/repo.git` :: Conectar tu repo local con uno de GitHub
- `git remote add upstream git@github.com:original/repo.git` :: Añadir el repo original (cuando haces fork)
- `git remote rename origin github` :: Renombrar un remoto
- `git remote remove upstream` :: Quitar un remoto
- `git fetch` :: Bajar novedades de origin sin unirlas
- `git fetch --all --prune` :: Bajar de todos los remotos y limpiar ramas borradas allá
- `git pull` :: Bajar y unir a tu rama actual
- `git pull --rebase` :: Bajar y poner tus commits encima (historial recto)
- `git push` :: Subir la rama actual a su upstream
- `git push -u origin feature/login` :: Primer push de una rama: la sube y la enlaza (upstream)
- `git push --tags` :: Subir los tags
- `git status -sb` :: Ver si vas adelante/atrás del remoto (ahead/behind)
- `git log --oneline HEAD..origin/main` :: Ver qué commits hay en el remoto que tú no tienes

### 🔗 ¿Qué es el upstream?

El **upstream** es la rama remota "pareja" de tu rama local. Cuando `main` sigue a `origin/main`, puedes escribir solo `git push` y `git pull` sin decir a dónde. Se configura con `-u` en el primer push (o automáticamente si activaste `push.autoSetupRemote`).

```text
$ git status
En la rama main
Tu rama está adelantada a 'origin/main' por 2 commits.
  (usa "git push" para publicar tus commits locales)
```

### ✅ Ejemplo resuelto: mantener tu fork al día

Situación: hiciste fork de un proyecto de IA open source y el original avanzó.

```bash
git remote add upstream https://github.com/original/proyecto.git
git fetch upstream
git switch main
git merge upstream/main         # trae lo nuevo del original
git push origin main            # actualiza tu fork en GitHub
```

💡 Consejo: acostúmbrate a `git fetch` + `git status` antes de empezar a trabajar. Te enteras de los cambios sin sorpresas.

⚠️ Cuidado: "fatal: The current branch X has no upstream branch" significa que es la primera vez que subes esa rama. Usa `git push -u origin X`.

🇬🇧 **remote** /rimóut/ = remoto · **fetch** /fech/ = ir a buscar · **upstream** /ápstrim/ = río arriba (rama remota de referencia) · **ahead** /ajéd/ = adelante · **behind** /bijáind/ = atrás · **fork** /fork/ = bifurcar/copiar un repo ajeno · **prune** /prun/ = podar

## 🐙 GitHub flow, pull requests y gh CLI

El **GitHub flow** es la forma estándar de trabajar en equipo: `main` siempre funciona; cada cambio va en una rama; se propone con un **pull request (PR)**; alguien lo revisa; se fusiona; se borra la rama.

```text
1. git switch -c feature/x   →  2. commits  →  3. git push -u origin feature/x
4. gh pr create              →  5. revisión y CI  →  6. merge en GitHub
7. git switch main && git pull  →  8. git branch -d feature/x
```

Un **pull request** es decir "por favor, jala (pull) mis cambios a main". En GitHub se ve el diff, se comenta línea por línea y se ejecutan las pruebas automáticas.

### 🛠️ gh: GitHub desde la terminal

Instálala con `sudo pacman -S github-cli` y luego `gh auth login`.

- `gh auth login` :: Iniciar sesión en GitHub
- `gh repo create mi-repo --public --source=. --push` :: Crear el repo en GitHub desde tu carpeta y subirlo
- `gh repo clone usuario/repo` :: Clonar sin copiar la URL completa
- `gh repo fork usuario/repo --clone` :: Hacer fork y clonarlo (configura upstream solo)
- `gh repo view --web` :: Abrir el repo en el navegador
- `gh pr create --fill` :: Crear un PR usando los mensajes de commit como título y descripción
- `gh pr create --title "feat: login" --body "Cierra #12"` :: PR con título y texto propios
- `gh pr list` :: Ver los PR abiertos
- `gh pr checkout 42` :: Bajar el PR número 42 a tu PC para probarlo
- `gh pr view 42 --web` :: Abrir el PR en el navegador
- `gh pr diff 42` :: Ver el diff de un PR
- `gh pr review 42 --approve` :: Aprobar un PR
- `gh pr merge 42 --squash --delete-branch` :: Fusionar (aplastado) y borrar la rama
- `gh pr status` :: Estado de tus PR y los que te piden revisar
- `gh issue create` :: Crear un issue (tarea o bug)
- `gh issue list` :: Ver issues abiertos
- `gh run list` :: Ver las ejecuciones de GitHub Actions (CI)
- `gh run watch` :: Ver en vivo cómo corre la CI

### ✅ Ejemplo resuelto: tu primer pull request

```bash
git switch main && git pull
git switch -c feature/exportar-csv
# ... programas ...
git add exportar.py
git commit -m "feat: exporta resultados a CSV"
git push -u origin feature/exportar-csv
gh pr create --fill
```

```text
Creating pull request for feature/exportar-csv into main in yftorrezg/proyecto

https://github.com/yftorrezg/proyecto/pull/7
```

Tras la aprobación:

```bash
gh pr merge 7 --squash --delete-branch
git switch main && git pull
```

📌 Escribir "Closes #12" o "Fixes #12" en la descripción del PR cierra el issue 12 automáticamente al fusionar.

💡 Consejo: PRs pequeños (menos de 300 líneas) se revisan rápido y con más cuidado. Un PR de 3000 líneas recibe un "LGTM" sin que nadie lo lea.

⚠️ Cuidado: después de fusionar en GitHub, tu `main` local sigue viejo. Haz `git switch main && git pull` antes de crear la siguiente rama.

🇬🇧 **pull request** /pul rikuést/ = solicitud de incorporación · **review** /riviú/ = revisión · **approve** /aprúv/ = aprobar · **issue** /íshu/ = incidencia/tarea · **LGTM (looks good to me)** /luks gud tu mi/ = me parece bien · **CI** /si ái/ = integración continua

## 🙈 .gitignore: lo que Git no debe ver

`.gitignore` es un archivo de texto en la raíz del repo con patrones de archivos que Git debe **ignorar**: dependencias, entornos virtuales, archivos compilados, datasets pesados y, sobre todo, **secretos**.

- `*.log` :: Ignora todos los archivos que terminan en .log
- `build/` :: Ignora la carpeta build (la barra final indica carpeta)
- `/config.local` :: La barra inicial: solo en la raíz del repo
- `**/temp` :: En cualquier nivel de carpetas
- `!importante.log` :: El signo ! hace una excepción (sí rastrear este)
- `git check-ignore -v archivo` :: Saber qué regla ignora un archivo
- `git status --ignored` :: Ver también los archivos ignorados
- `git rm -r --cached .` :: Dejar de rastrear todo (luego git add . aplica el nuevo .gitignore)

### 🐍 Ejemplo para Python / IA

```text
# Entornos y caché
.venv/
venv/
__pycache__/
*.pyc
.pytest_cache/
.ipynb_checkpoints/

# Secretos
.env
*.key

# Datos y modelos pesados
data/raw/
*.csv
*.parquet
*.pt
*.ckpt
*.safetensors
wandb/
mlruns/

# Editor y sistema
.vscode/
.idea/
.DS_Store
```

### 🟩 Ejemplo para Node / JavaScript

```text
node_modules/
dist/
build/
.next/
coverage/
.env
.env.local
npm-debug.log*
yarn-error.log*
.cache/
```

### ✅ Ejemplo resuelto: subí .env por error

Situación: hiciste commit de `.env` con tu API key y ahora lo añades al `.gitignore`, pero Git lo sigue rastreando.

```bash
echo ".env" >> .gitignore
git rm --cached .env            # deja de rastrearlo (el archivo sigue en tu disco)
git commit -m "chore: deja de rastrear .env"
git push
```

📌 `.gitignore` solo afecta a archivos **no rastreados**. Si ya estaba en un commit, necesitas `git rm --cached`.

⚠️ Cuidado: si la clave ya llegó a GitHub, **considérala robada**: revócala y genera una nueva. Borrarla en un commit nuevo no la quita del historial (para eso existe `git filter-repo`).

💡 Consejo: gitignore.io (o `gh repo create --gitignore Python`) genera plantillas listas. Para ignorar algo solo en tu PC sin tocar el repo, usa `.git/info/exclude`.

🇬🇧 **ignore** /ignór/ = ignorar · **pattern** /pátern/ = patrón · **secret** /síkret/ = secreto · **leak** /lik/ = filtración · **revoke** /rivóuk/ = revocar · **dependency** /dipéndensi/ = dependencia

## 🏷️ Tags y versiones

Un **tag** es un marcador fijo en un commit, normalmente para versiones: `v1.0.0`. A diferencia de una rama, un tag **no se mueve**. Es como poner un post-it de "entregado" en una página del cuaderno.

Se usa **versionado semántico** (SemVer): `MAYOR.MENOR.PARCHE`.

| Sube… | Cuándo | Ejemplo |
|---|---|---|
| **MAYOR** | cambias algo incompatible (rompes la API) | `1.4.2` → `2.0.0` |
| **MENOR** | añades funcionalidad compatible | `1.4.2` → `1.5.0` |
| **PARCHE** | corriges bugs sin cambiar la API | `1.4.2` → `1.4.3` |

- `git tag` :: Listar tags
- `git tag -a v1.0.0 -m "Primera versión estable"` :: Crear un tag anotado (con autor, fecha y mensaje)
- `git tag v1.0.0` :: Tag ligero (solo un nombre, sin metadatos)
- `git tag -a v0.9.0 a1b2c3d -m "Beta"` :: Etiquetar un commit antiguo
- `git show v1.0.0` :: Ver el tag y su commit
- `git push origin v1.0.0` :: Subir un tag (git push normal NO sube tags)
- `git push --follow-tags` :: Subir commits y sus tags anotados
- `git tag -d v1.0.0` :: Borrar un tag local
- `git push origin --delete v1.0.0` :: Borrar un tag en GitHub
- `git describe --tags` :: Decir dónde estás respecto al último tag (ej. v1.0.0-3-ga1b2c3d)
- `gh release create v1.0.0 --generate-notes` :: Crear un release en GitHub con notas automáticas

💡 Consejo: usa tags anotados (`-a`) para versiones públicas; guardan quién y cuándo.

⚠️ Cuidado: no muevas ni borres un tag que ya publicaste. Si te equivocaste, crea `v1.0.1`.

🇬🇧 **tag** /tag/ = etiqueta · **release** /rilís/ = lanzamiento/versión publicada · **annotated** /ánoteitid/ = anotado · **semantic versioning** /simántik vérshonin/ = versionado semántico · **breaking change** /bréikin cheinch/ = cambio que rompe

## 🍒 Cherry-pick: copiar un commit suelto

`git cherry-pick` copia **un commit concreto** de otra rama a la tuya, sin traer todo lo demás. Como escoger una sola cereza del árbol.

- `git cherry-pick a1b2c3d` :: Aplicar ese commit en la rama actual (crea un commit nuevo)
- `git cherry-pick a1b2c3d e4f5g6h` :: Aplicar varios commits
- `git cherry-pick a1b2c3d..e4f5g6h` :: Un rango (sin incluir el primero)
- `git cherry-pick -n a1b2c3d` :: Aplicar los cambios sin hacer commit todavía
- `git cherry-pick -x a1b2c3d` :: Añade al mensaje "(cherry picked from commit ...)"
- `git cherry-pick --continue` :: Seguir tras resolver un conflicto
- `git cherry-pick --abort` :: Cancelar

### ✅ Ejemplo resuelto: llevar un fix a la versión estable

Situación: arreglaste un bug en `develop` (commit `9e0f3a7`) y también lo necesitas en la rama `release/1.0` sin traer las funciones a medio hacer.

```bash
git log --oneline develop -3        # encuentras el hash del fix: 9e0f3a7
git switch release/1.0
git cherry-pick -x 9e0f3a7
```

```text
[release/1.0 2b3c4d5] fix: evita división por cero
 Date: Sat Oct 18 10:12:03 2026 -0400
 1 file changed, 2 insertions(+), 1 deletion(-)
```

⚠️ Cuidado: abusar de cherry-pick duplica commits (mismo cambio, distinto hash) y complica merges futuros. Úsalo para casos puntuales como hotfixes.

🇬🇧 **cherry-pick** /chéri pik/ = escoger a dedo · **hotfix** /jótfiks/ = arreglo urgente · **range** /reinch/ = rango · **stable** /stéibol/ = estable

## 🐞 Bisect: encontrar qué commit rompió todo

`git bisect` hace **búsqueda binaria** en tu historial. Le dices un commit bueno y uno malo; Git te lleva al del medio, tú pruebas y respondes "good" o "bad", y repite. Con 1000 commits encuentra el culpable en unos 10 pasos (log₂ 1000 ≈ 10). ¡Algoritmos de clase aplicados!

- `git bisect start` :: Empezar la búsqueda
- `git bisect bad` :: El commit actual tiene el bug
- `git bisect good v1.0.0` :: Este commit (o tag) funcionaba bien
- `git bisect good` :: (o `git bisect bad`) Responder tras probar cada commit que te propone
- `git bisect skip` :: Este commit no se puede probar (no compila, etc.)
- `git bisect run pytest tests/test_calc.py` :: Automático: Git ejecuta el comando (código 0 = bueno)
- `git bisect log` :: Ver los pasos dados
- `git bisect reset` :: Terminar y volver a tu rama

### ✅ Ejemplo resuelto: bisect automático con pytest

Situación: los tests pasaban en `v1.2.0` y hoy fallan. Hay 64 commits en medio.

```bash
git bisect start
git bisect bad                   # HEAD está roto
git bisect good v1.2.0           # esta versión funcionaba
git bisect run pytest -q tests/test_calc.py
```

```text
Bisecting: 31 revisions left to test after this (roughly 5 steps)
...
c4b3a21 is the first bad commit
commit c4b3a21
Author: Yafer <tu@correo.com>
    refactor: simplifica promedio
```

```bash
git show c4b3a21                 # ves exactamente qué rompió
git bisect reset                 # vuelves a tu rama
```

💡 Consejo: bisect funciona mejor con commits pequeños: si el culpable es un commit de 2 líneas, el bug salta a la vista.

🇬🇧 **bisect** /baiséct/ = partir en dos · **binary search** /báineri serch/ = búsqueda binaria · **culprit** /cálprit/ = culpable · **skip** /skip/ = saltar

## ✍️ Mensajes de commit: Conventional Commits

Un buen mensaje explica **qué y por qué**, no cómo (el cómo ya está en el diff). **Conventional Commits** es un estándar muy usado: `tipo(ámbito): descripción`. Permite generar changelogs y versiones automáticamente.

```text
feat(auth): añade inicio de sesión con Google

Los usuarios pedían no crear otra contraseña. Se usa OAuth2
con la librería authlib. El token se guarda cifrado.

Closes #23
```

| Tipo | Para qué | Ejemplo |
|---|---|---|
| `feat` | nueva funcionalidad (sube MENOR) | `feat: añade exportar a PDF` |
| `fix` | corrige un bug (sube PARCHE) | `fix: evita división por cero` |
| `docs` | solo documentación | `docs: explica instalación en Arch` |
| `style` | formato, espacios (sin cambiar lógica) | `style: aplica black` |
| `refactor` | reorganiza sin cambiar comportamiento | `refactor: separa modelo y datos` |
| `perf` | mejora rendimiento | `perf: vectoriza con numpy` |
| `test` | añade o corrige tests | `test: cubre casos vacíos` |
| `build` | dependencias, empaquetado | `build: actualiza torch a 2.5` |
| `ci` | GitHub Actions y similares | `ci: ejecuta pytest en cada PR` |
| `chore` | tareas de mantenimiento | `chore: limpia archivos viejos` |
| `feat!` | cambio incompatible (sube MAYOR) | `feat!: cambia formato de la API` |

### 📏 Reglas de oro

- `Primera línea ≤ 50 caracteres` :: Se lee entera en git log --oneline y en GitHub
- `Modo imperativo` :: "añade login", no "añadí" ni "añadiendo" (en inglés: "add", no "added")
- `Línea en blanco tras el título` :: Separa el resumen del cuerpo explicativo
- `Cuerpo: el porqué` :: Qué problema resuelve y qué decisiones tomaste
- `Un commit = una idea` :: Si tu mensaje necesita "y", quizá son dos commits

🇬🇧 Frases típicas en inglés: "Add user login" · "Fix crash when list is empty" · "Update README with setup steps" · "Remove unused imports" · "Refactor data loader" · "Bump version to 1.2.0"

⚠️ Cuidado: mensajes como "cambios", "asdf", "ya funciona" o "final final" no sirven a nadie, ni a ti dentro de un mes.

💡 Consejo: en proyectos open source escribe los commits en inglés; es la práctica habitual y te sirve de práctica diaria del idioma.

🇬🇧 **imperative mood** /impérativ mud/ = modo imperativo · **scope** /skóup/ = ámbito · **body** /bódi/ = cuerpo · **changelog** /chéinchlog/ = registro de cambios · **bump** /bamp/ = subir (versión)

## ⚡ Alias y configuración útil

Los alias son **atajos** para comandos largos. Se guardan en `~/.gitconfig` y funcionan en cualquier repo.

- `git config --global alias.st "status -sb"` :: git st = estado corto con rama
- `git config --global alias.co switch` :: git co main
- `git config --global alias.br "branch -vv"` :: git br = ramas con detalle
- `git config --global alias.lg "log --oneline --graph --decorate --all"` :: git lg = árbol bonito
- `git config --global alias.last "log -1 HEAD --stat"` :: git last = último commit
- `git config --global alias.unstage "restore --staged"` :: git unstage archivo
- `git config --global alias.undo "reset --soft HEAD~1"` :: git undo = deshace el último commit sin perder nada
- `git config --global alias.amend "commit --amend --no-edit"` :: git amend = añade lo preparado al último commit
- `git config --global rerere.enabled true` :: Git recuerda cómo resolviste un conflicto y lo repite
- `git config --global fetch.prune true` :: fetch limpia ramas remotas borradas
- `git config --global diff.colorMoved zebra` :: Colorea distinto las líneas que solo se movieron

Así queda tu `~/.gitconfig`:

```text
[user]
    name = Yafer Torrez
    email = tu@correo.com
[init]
    defaultBranch = main
[pull]
    rebase = false
[push]
    autoSetupRemote = true
[alias]
    st = status -sb
    lg = log --oneline --graph --decorate --all
    undo = reset --soft HEAD~1
    amend = commit --amend --no-edit
```

### 🐟 Abreviaturas en fish

En fish puedes ir más lejos con `abbr`: escribes `gst`, pulsas espacio y se expande al comando completo (así aprendes el comando real).

```bash
abbr -a gst 'git status -sb'
abbr -a ga 'git add'
abbr -a gc 'git commit -m'
abbr -a gp 'git push'
abbr -a gl 'git pull'
abbr -a glg 'git log --oneline --graph --all'
abbr -a gsw 'git switch'
```

💡 Consejo: pon esas líneas en `~/.config/fish/config.fish` (o en `conf.d/`) para que sean permanentes.

💡 Consejo: prueba `lazygit` (`sudo pacman -S lazygit`): una interfaz de terminal para Git muy rápida, ideal para hacer add por trozos y ver ramas.

🇬🇧 **alias** /éilias/ = alias/apodo · **shortcut** /shórtcat/ = atajo · **decorate** /dékoreit/ = decorar · **reuse** /riiús/ = reutilizar

## 👥 Trabajo en equipo

Git en equipo es más **acuerdos** que comandos. Estas prácticas evitan el 90 % de los dramas en proyectos de la universidad o del trabajo.

- `git pull --rebase` :: Antes de subir, ponte al día con historial recto
- `git switch main && git pull && git switch -c feature/x` :: Empieza cada tarea desde un main actualizado
- `git rebase main` :: Actualiza tu rama de trabajo con lo último de main
- `git log --oneline origin/main..HEAD` :: Revisa qué vas a subir antes del push
- `git commit --signoff` :: Añade "Signed-off-by" (algunos proyectos lo exigen)
- `git log --format='%an' | sort | uniq -c` :: Ver cuántos commits hizo cada persona
- `gh pr list --search "review-requested:@me"` :: PRs que te piden revisar

### 🤝 Acuerdos del equipo

| Acuerdo | Por qué |
|---|---|
| Nadie hace push directo a main | todo pasa por PR y revisión |
| Proteger main en GitHub (Settings → Branches) | GitHub impide push y force-push a main |
| Una rama por tarea/issue | cambios aislados, fáciles de revisar |
| PRs pequeños y frecuentes | menos conflictos, revisiones rápidas |
| CI con tests en cada PR | nadie fusiona algo roto |
| Mismo formateador (black, prettier) | los diffs muestran lógica, no espacios |
| Convención de commits acordada | historial legible para todos |

### ✅ Ejemplo resuelto: tu rama se quedó atrás de main

Situación: llevas 3 días en `feature/dashboard` y tus compañeros fusionaron 10 PRs en main.

```bash
git fetch
git switch feature/dashboard
git rebase origin/main          # si hay conflictos: resolver, git add, git rebase --continue
pytest                          # comprueba que todo sigue funcionando
git push --force-with-lease     # tu rama ya existía en GitHub, por eso hay que forzar
```

📌 Revisar código de otros también es aprender: lee PRs con calma, pregunta "¿por qué?" y comenta con amabilidad.

💡 Consejo: si vas a tocar un archivo que todos usan (por ejemplo `config.py`), avisa en el grupo. Comunicarse evita más conflictos que cualquier comando.

⚠️ Cuidado: `git push --force-with-lease` solo en TU rama. En una rama que comparten varios, coordina antes.

🇬🇧 **code review** /cóud riviú/ = revisión de código · **teammate** /tímmeit/ = compañero de equipo · **protected branch** /protéktid branch/ = rama protegida · **pair programming** /per prógramin/ = programar en pareja · **nitpick (nit)** /nítpik/ = detalle menor

## 🚨 Errores frecuentes y cómo salir

Cuando Git se queja, **lee el mensaje entero**: casi siempre incluye el comando para salir. Aquí van los clásicos.

### 🔌 detached HEAD (HEAD desacoplado)

Pasa cuando haces `git checkout a1b2c3d` o `git switch --detach v1.0`: estás mirando un commit concreto, no una rama. Puedes curiosear, pero los commits que hagas quedan "flotando".

```bash
git switch -c rescate           # si hiciste commits aquí y quieres conservarlos
git switch main                 # si solo estabas mirando: vuelve a tu rama
```

### ⛔ push rechazado (rejected)

```text
 ! [rejected]        main -> main (fetch first)
error: failed to push some refs to 'github.com:yftorrezg/proyecto.git'
hint: Updates were rejected because the remote contains work that you do not have locally.
```

Significa: alguien (o tú desde la laptop) subió commits que no tienes. Solución:

```bash
git pull --rebase               # trae lo del remoto y pone lo tuyo encima
git push
```

### 🔁 merge o rebase en curso

Si `git status` dice "Tienes rutas no fusionadas" o "rebase interactivo en progreso", estás a mitad de algo:

- `git merge --abort` :: Cancelar el merge y volver al estado anterior
- `git rebase --abort` :: Cancelar el rebase
- `git cherry-pick --abort` :: Cancelar el cherry-pick
- `git add . && git commit` :: Terminar el merge tras resolver los conflictos
- `git add . && git rebase --continue` :: Seguir con el rebase tras resolver

### 📋 Tabla de rescate

| Mensaje o problema | Qué pasa | Solución |
|---|---|---|
| `fatal: not a git repository` | no estás dentro de un repo | `cd` a la carpeta correcta o `git init` |
| `has no upstream branch` | primer push de una rama | `git push -u origin rama` |
| `Your local changes would be overwritten` | cambios sin guardar al cambiar de rama o pull | `git stash`, luego `git stash pop` |
| `refusing to merge unrelated histories` | dos repos sin historia común | `git pull origin main --allow-unrelated-histories` |
| `Permission denied (publickey)` | SSH no configurado | revisa la llave con `ssh -T git@github.com` |
| `Author identity unknown` | falta tu nombre/correo | `git config --global user.name ...` |
| `nothing to commit, working tree clean` | no hay cambios | ¡todo bien! ya está guardado |
| `CONFLICT (content)` | ambos cambiaron las mismas líneas | editar, `git add`, `git commit` |
| hice commit en main en vez de en mi rama | commit en rama equivocada | `git branch mi-rama`, `git reset --hard origin/main`, `git switch mi-rama` |
| `file exceeds GitHub's file size limit of 100 MB` | archivo enorme en un commit | quitarlo del commit (`git reset --soft`) y usar Git LFS |
| `index.lock: File exists` | un git anterior quedó colgado | cerrar otros git y borrar `.git/index.lock` |

### ✅ Ejemplo resuelto: hice commit en main por error

Situación: hiciste 2 commits en `main` que debían ir en una rama nueva, y aún no los subiste.

```bash
git branch feature/graficos     # 1. la rama nueva apunta a tus commits (los "salvas")
git reset --hard origin/main    # 2. main vuelve a como está en GitHub
git switch feature/graficos     # 3. sigues trabajando en la rama correcta
git log --oneline -3
```

```text
8d7e6f5 (HEAD -> feature/graficos) feat: gráfico de pérdida
c4b3a21 feat: gráfico de precisión
3f2a1bc (origin/main, main) feat: carga de datos
```

💡 Consejo: copia el mensaje de error y busca tal cual. Casi todos los errores de Git ya tienen respuesta en Stack Overflow, y leerlas en inglés es buena práctica.

⚠️ Cuidado: nunca borres la carpeta `.git` "para empezar de cero" ni clones encima: perderías historial y ramas locales. Pregunta antes o mira `git reflog`.

🇬🇧 **detached** /ditácht/ = desacoplado · **rejected** /riyéktid/ = rechazado · **hint** /jint/ = pista · **refs (references)** /refs/ = referencias · **unrelated** /anriléitid/ = sin relación · **in progress** /in prógres/ = en curso · **fatal** /féital/ = fatal/grave
