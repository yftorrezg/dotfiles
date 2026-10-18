# 🐧 Terminal
Cada línea: código :: explicación. Edita este archivo para añadir las tuyas.

## Moverse y mirar
pwd; ls -la; cd carpeta; cd .. :: Dónde estoy / listar / entrar / subir
cd -; cd ~ :: Volver a la anterior / ir a tu carpeta personal
tree -L 2 :: Árbol de carpetas (2 niveles)
cat archivo; less archivo :: Ver un archivo (less: q para salir)
head -n 20 archivo; tail -f log.txt :: Primeras líneas / seguir un log en vivo

## Archivos
mkdir -p a/b/c :: Crear carpetas (con las intermedias)
touch notas.txt :: Crear archivo vacío
cp -r origen destino; mv viejo nuevo :: Copiar (carpetas con -r) / mover o renombrar
rm archivo; rm -r carpeta :: Borrar (¡no hay papelera!)
gio trash archivo :: Mandar a la papelera (recuperable)

## Buscar
grep -rn "texto" . :: Buscar texto en todos los archivos
find . -name "*.py" :: Buscar archivos por nombre
fd py; rg "texto" :: Versiones rápidas (si están instaladas)
history | grep git :: Buscar en tus comandos anteriores

## Procesos y sistema
htop; btop :: Ver procesos y consumo
kill 1234; pkill firefox :: Cerrar un proceso por número / por nombre
df -h; du -sh * :: Espacio en disco / cuánto ocupa cada cosa
sudo pacman -Syu :: Actualizar Arch
paru -S paquete :: Instalar desde AUR

## Redirección y tuberías
comando > salida.txt :: Guardar la salida (reemplaza)
comando >> salida.txt :: Añadir al final
comando1 | comando2 :: Pasar la salida de uno al otro
comando && otro :: El segundo solo si el primero salió bien
chmod +x script.sh; ./script.sh :: Hacer ejecutable y ejecutar

## Atajos de teclado
Ctrl+C / Ctrl+D :: Cancelar / cerrar la terminal o salir
Ctrl+R :: Buscar en el historial
Ctrl+L :: Limpiar pantalla
Tab :: Autocompletar
↑ / ↓ :: Comandos anteriores
