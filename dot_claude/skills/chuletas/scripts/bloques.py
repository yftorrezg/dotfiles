#!/usr/bin/env python3
"""bloques.py — lista los bloques de código de una hoja de chuletas con su línea y la salida esperada.

Uso:
  python3 bloques.py hoja.md                 resumen: línea, lenguaje, nº de líneas, si trae salida
  python3 bloques.py hoja.md --lenguaje sql  solo ese lenguaje
  python3 bloques.py hoja.md --ver 179       muestra el bloque que empieza en la línea 179 y su salida

"Salida esperada" = el primer bloque ```text que aparece después del bloque (sin otro bloque de código
en medio y a menos de 6 líneas de texto). Es la convención de las hojas: código y debajo "salida real".
También lo importan otros scripts (probar_sql.py): bloques(ruta) -> lista de dicts.
"""
import re
import sys
from pathlib import Path

ESQUEMAS = {"flujo", "secuencia", "arbol", "capas", "tiempo", "grafica"}


def bloques(ruta):
    lineas = Path(ruta).read_text(encoding="utf-8").splitlines()
    res, i = [], 0
    while i < len(lineas):
        m = re.match(r"^```(\w*)\s*$", lineas[i])
        if not m:
            i += 1
            continue
        lang, ini, cuerpo = m.group(1) or "text", i + 1, []
        i += 1
        while i < len(lineas) and not lineas[i].startswith("```"):
            cuerpo.append(lineas[i])
            i += 1
        res.append({"linea": ini, "lenguaje": lang, "codigo": "\n".join(cuerpo), "fin": i + 1})
        i += 1
    # emparejar cada bloque de código con la salida text que le sigue
    for k, b in enumerate(res):
        b["salida"] = None
        if b["lenguaje"] in ESQUEMAS or b["lenguaje"] == "text":
            continue
        if k + 1 < len(res) and res[k + 1]["lenguaje"] == "text":
            if res[k + 1]["linea"] - b["fin"] <= 6:
                b["salida"] = res[k + 1]["codigo"]
                b["salida_linea"] = res[k + 1]["linea"]
    return res


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    bs = bloques(sys.argv[1])
    if "--ver" in sys.argv:
        n = int(sys.argv[sys.argv.index("--ver") + 1])
        for b in bs:
            if b["linea"] == n:
                print(f"--- bloque {b['lenguaje']} (línea {n})\n{b['codigo']}")
                if b["salida"] is not None:
                    print(f"--- salida esperada (línea {b['salida_linea']})\n{b['salida']}")
        sys.exit(0)
    filtro = sys.argv[sys.argv.index("--lenguaje") + 1] if "--lenguaje" in sys.argv else None
    for b in bs:
        if filtro and b["lenguaje"] != filtro:
            continue
        print(f"{b['linea']:>5}  {b['lenguaje']:<10} {b['codigo'].count(chr(10)) + 1:>3} líneas  "
              f"{'con salida' if b['salida'] is not None else ''}")
