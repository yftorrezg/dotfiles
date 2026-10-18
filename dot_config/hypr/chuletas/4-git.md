# 🌿 Git
Cada línea: código :: explicación. Edita este archivo para añadir las tuyas.

## Empezar
git init :: Crear un repositorio en la carpeta actual
git clone https://github.com/usuario/repo.git :: Descargar un repositorio
git config --global user.name "Tu Nombre" :: Configurar tu nombre (una vez)

## Día a día
git status :: Qué cambió y qué está preparado
git add archivo.py; git add . :: Preparar un archivo / todo
git commit -m "Añade login" :: Guardar una versión con mensaje
git push :: Subir tus commits
git pull :: Bajar y unir los cambios del remoto
git diff; git diff --staged :: Ver cambios sin preparar / preparados
git log --oneline --graph :: Historial compacto con ramas

## Ramas
git switch -c nueva-funcion :: Crear rama y pasarte a ella
git switch main :: Cambiar de rama
git branch -a :: Listar ramas
git merge nueva-funcion :: Unir esa rama a la actual
git branch -d nueva-funcion :: Borrar rama ya unida
git push -u origin nueva-funcion :: Subir una rama nueva

## Deshacer
git restore archivo.py :: Descartar cambios no guardados de un archivo
git restore --staged archivo.py :: Sacar del "add" (sin perder cambios)
git commit --amend :: Corregir el último commit (antes de subirlo)
git revert abc123 :: Commit que deshace otro (seguro si ya subiste)
git stash; git stash pop :: Guardar cambios aparte / recuperarlos

## Remoto y GitHub
git remote -v :: Ver a dónde sube
git fetch :: Bajar novedades sin unirlas
gh repo create :: Crear repo en GitHub (con gh)
gh pr create :: Abrir un pull request
