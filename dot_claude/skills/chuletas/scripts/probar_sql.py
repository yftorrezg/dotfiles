#!/usr/bin/env python3
"""probar_sql.py — ejecuta cada bloque ```sql de una hoja en una base NUEVA y compara con su salida.

Uso:
  python3 probar_sql.py hoja.md --base 179            usa el bloque de la línea 179 como esquema/datos
  python3 probar_sql.py hoja.md --base 179 --solo 1149   probar un solo bloque
  python3 probar_sql.py hoja.md --base 179 --motor postgres --contenedor pg-auditoria

Motores:
  sqlite    (por defecto) sqlite3 de la terminal con .mode table y .nullvalue NULL, igual que las hojas
  postgres  psql dentro de un contenedor Docker (docker run -d --rm --name pg-auditoria -e POSTGRES_PASSWORD=x postgres:18-alpine)
            cada bloque corre en una base recién creada; el esquema se adapta solo lo mínimo (PRAGMA fuera)

Resultado por bloque: OK (salida idéntica), DIFIERE (muestra las dos), SIN SALIDA (no había ```text debajo:
solo se comprueba que no falle) o ERROR. Las diferencias NO siempre son errores de la hoja: un bloque puede
depender de otro anterior, o la salida puede ser un recorte a propósito. Revísalas a mano.
"""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from bloques import bloques  # noqa: E402


def normalizar(texto):
    return "\n".join(l.rstrip() for l in texto.strip().splitlines() if l.strip())


def correr_sqlite(esquema, codigo):
    script = ".mode table\n.nullvalue NULL\n" + esquema + "\n" + codigo + "\n"
    p = subprocess.run(["sqlite3", ":memory:"], input=script, capture_output=True, text=True)
    return (p.stdout + p.stderr).strip()


def correr_postgres(contenedor, esquema, codigo, n):
    base = f"prueba_{n}"
    psql = ["docker", "exec", "-i", contenedor, "psql", "-U", "postgres", "-X", "-q"]
    subprocess.run(psql + ["-c", f"DROP DATABASE IF EXISTS {base}", "-c", f"CREATE DATABASE {base}"],
                   capture_output=True, text=True)
    esquema = "\n".join(l for l in esquema.splitlines() if not l.strip().upper().startswith("PRAGMA"))
    p = subprocess.run(psql + ["-d", base, "-P", "null=NULL"], input=esquema + "\n" + codigo + "\n",
                       capture_output=True, text=True)
    subprocess.run(psql + ["-c", f"DROP DATABASE IF EXISTS {base}"], capture_output=True, text=True)
    return (p.stdout + p.stderr).strip()


def main():
    a = sys.argv
    if len(a) < 2:
        print(__doc__)
        sys.exit(1)
    hoja = a[1]
    base_linea = int(a[a.index("--base") + 1]) if "--base" in a else None
    solo = int(a[a.index("--solo") + 1]) if "--solo" in a else None
    motor = a[a.index("--motor") + 1] if "--motor" in a else "sqlite"
    cont = a[a.index("--contenedor") + 1] if "--contenedor" in a else "pg-auditoria"
    bs = [b for b in bloques(hoja) if b["lenguaje"] == "sql"]
    esquema = next((b["codigo"] for b in bs if b["linea"] == base_linea), "") if base_linea else ""
    cuenta = {"OK": 0, "DIFIERE": 0, "SIN SALIDA": 0, "ERROR": 0}
    for b in bs:
        if b["linea"] == base_linea or (solo and b["linea"] != solo):
            continue
        if motor == "postgres":
            obtenido = correr_postgres(cont, esquema, b["codigo"], b["linea"])
        else:
            obtenido = correr_sqlite(esquema, b["codigo"])
        hay_error = "error" in obtenido.lower()
        if b["salida"] is None:
            estado = "ERROR" if hay_error else "SIN SALIDA"
        else:
            estado = "OK" if normalizar(obtenido) == normalizar(b["salida"]) else "DIFIERE"
        cuenta[estado] += 1
        if estado != "OK" and (estado != "SIN SALIDA" or solo):
            print(f"\n===== línea {b['linea']}: {estado}")
            if b["salida"] is not None:
                print("--- esperado:\n" + b["salida"])
            print("--- obtenido:\n" + (obtenido or "(nada)"))
        elif solo:
            print(f"línea {b['linea']}: {estado}\n{obtenido}")
    print(f"\nResumen ({motor}): {cuenta}")


if __name__ == "__main__":
    main()
