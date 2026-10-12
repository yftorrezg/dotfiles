#!/usr/bin/env python3
"""Pruebas de repo-a-imagenes.py (sin red: repo local falso). Uso: python3 repo-a-imagenes-tests.py"""
import importlib.util
import os
import subprocess
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("rai", AQUI / "repo-a-imagenes.py")
rai = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rai)

fallas = []


def comprobar(nombre, cond, detalle=""):
    print(("✅ " if cond else "❌ ") + nombre + ("" if cond else f"  → {detalle}"))
    if not cond:
        fallas.append(nombre)


# --- links
u = rai.url_de_git("https://github.com/midudev/curso-python")
comprobar("link simple", u == ("https://github.com/midudev/curso-python.git", None, "", "curso-python"), u)
u = rai.url_de_git("https://github.com/Asabeneh/30-Days-Of-JavaScript/tree/master/Spanish")
comprobar("link con subcarpeta", u[1:3] == ("master", "Spanish"), u)
u = rai.url_de_git("https://gitlab.com/g/p/-/tree/main/a/b")
comprobar("gitlab con -/tree", u[1:3] == ("main", "a/b"), u)

# --- orden natural y paginado
comprobar("orden natural", sorted(["10_a", "2_b", "1_c"], key=rai.natural) == ["1_c", "2_b", "10_a"])
largo = [[("x", None, False)] for _ in range(100)]
rg = rai.partir(largo, 42)
comprobar("páginas cubren todo sin huecos", rg[0][0] == 0 and rg[-1][1] == 100 and all(a[1] == b[0] for a, b in zip(rg, rg[1:])), rg)
comprobar("48 líneas = una sola página", rai.partir(largo[:48], 42) == [(0, 48)])

# --- repo local falso
with tempfile.TemporaryDirectory() as d:
    d = Path(d)
    (d / "01_basic").mkdir()
    (d / "01_basic" / "a.py").write_text("print('hola ñandú ✅')\n")
    (d / "01_basic" / "b.js").write_text("console.log(2 + 3)\n")
    (d / "01_basic" / "img.png").write_bytes(b"\x89PNG\0\0")
    (d / "node_modules").mkdir()
    (d / "node_modules" / "x.js").write_text("x")
    (d / "Spanish").mkdir()
    (d / "Spanish" / "leeme.md").write_text("# Hola\n\nTexto con `código`.\n\n```js\nconsole.log('x')\n```\n")
    (d / "README.md").write_text("# Raíz\n\nIntro larga para pasar el filtro de tamaño mínimo del markdown.\n" * 3)
    o = rai.Origen(str(d), d / "no-se-usa")
    cod, mds, _b = rai.elegir_rutas(o, "", {"apuntes", "codigo", "tarjetas"})
    comprobar("código: solo a.py y b.js, sin node_modules ni png", cod == ["01_basic/a.py", "01_basic/b.js"], cod)
    comprobar("md: README primero y sin la carpeta de traducción", mds == ["README.md"], mds)
    cod, mds, _b = rai.elegir_rutas(o, "es", {"apuntes"})
    comprobar("--idioma es toma solo Spanish/", mds == ["Spanish/leeme.md"] and cod == [], (cod, mds))

    # salida completa sin apuntes (no depende de WebKit): código + tarjetas
    out = d / "salida"
    r = subprocess.run([sys.executable, "-I", str(AQUI / "repo-a-imagenes.py"), str(d), "--salida", str(out),
                        "--que", "codigo,tarjetas"], capture_output=True, text=True)
    comprobar("corre sin error", r.returncode == 0, r.stderr[-300:])
    comprobar("2 imágenes de código", len(list((out / "2 Código").glob("*.webp"))) == 2, os.listdir(out))
    tarj = sorted(p.name for p in (out / "3 Tarjetas").glob("*.webp")) if (out / "3 Tarjetas").exists() else []
    comprobar("tarjetas frente/dorso (2 archivos × 2)", len(tarj) == 4, tarj)

# --- ejecución aislada
ok, sal = rai.ejecutar("console.log(6 * 7)", "js")
comprobar("JS ejecuta", ok and sal == "42", (ok, sal))
ok, sal = rai.ejecutar("print(sum(range(5)))", "py")
comprobar("Python ejecuta", ok and sal == "10", (ok, sal))
ok, sal = rai.ejecutar("import os\nprint(os.path.exists('/home'))", "py")
comprobar("el entorno no ve /home", ok and sal == "False", (ok, sal))
ok, sal = rai.ejecutar("while True: pass", "py", tiempo=1)
comprobar("bucle infinito se corta", not ok)
comprobar("no ejecuta prompt()", rai.salida_de_bloque("let n = prompt('x'); console.log(n)", "js", []) is None)
comprobar("depende de bloques previos", rai.salida_de_bloque("console.log(a + 1)", "js", ["const a = 1", "console.log('antes')"]) == "2")

comprobar("nombre legible", rai.nombre_legible("Spanish/dia_05_Arreglos/dia_05_arreglos.md", "Spanish") == "dia_05_arreglos")
comprobar("nombre legible sin carpeta repetida", rai.nombre_legible("01_basic/a.py", "") == "01_basic - a.py")

# --- markdown
b, f = rai.md_a_bloques("# T\n\ntexto\n\n| a | b |\n|---|---|\n| 1 | 2 |\n\n```py\nprint(1)\n```\n")
comprobar("md: bloques y fence", len(b) == 4 and f == [("py", "print(1)\n", "T")], (len(b), f))

print("\n" + ("TODO OK" if not fallas else f"FALLAS: {fallas}"))
sys.exit(1 if fallas else 0)
