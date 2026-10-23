#!/bin/bash
# Corre TODAS las pruebas del sistema de capturas/apuntes y dice si todo está bien.
# Uso: pruebas-cursos.sh        (correrlo después de cualquier cambio en estos scripts; ~1 min)
cd "$(dirname "$0")" || exit 1
MAL=0
for t in auto-captura-tests.py estudiar-tests.py cuadernillo-tests.py resumen-corto-tests.py tarjetas-panel-tests.py; do
    if python3 "$t" > /tmp/pruebas-cursos.$$ 2>&1 && ! grep -qE "MAL|FALLAN|Traceback" /tmp/pruebas-cursos.$$; then
        echo "✅ $t"
    else
        echo "❌ $t"; grep -E "MAL|FALLAN|Traceback|Error" /tmp/pruebas-cursos.$$ | head -5; MAL=1
    fi
done
for t in cola-capturas-tests.sh playlist-a-apuntes-tests.sh; do
    if bash "$t" > /tmp/pruebas-cursos.$$ 2>&1 && ! grep -qE "FAIL|✘|Traceback" /tmp/pruebas-cursos.$$; then echo "✅ $t"
    else echo "❌ $t"; tail -5 /tmp/pruebas-cursos.$$; MAL=1; fi
done
rm -f /tmp/pruebas-cursos.$$
[ $MAL = 0 ] && echo "TODO OK" || { echo "HAY PRUEBAS QUE FALLAN"; exit 1; }
