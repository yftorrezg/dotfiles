#!/usr/bin/env python3
"""Pruebas de practica.py (sin llamar a Claude: la respuesta se simula con texto fijo).
Sí corre node y python de verdad (la verificación de los tests es justamente lo que se prueba)."""
import contextlib, importlib.util, io, json, os, sys, tempfile
AQUI = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("pr", os.path.join(AQUI, "practica.py"))
pr = importlib.util.module_from_spec(spec); spec.loader.exec_module(pr)
ok = 0


def bloque(nombre, arranque, tests, solucion, dif="fácil"):
    return (f"@@@ EJERCICIO\nnombre: {nombre}\ntitulo: Título de {nombre}\ndificultad: {dif}\n"
            f"@@@ ENUNCIADO\nHacé `{nombre}`. Ejemplo: `x → y`\n@@@ PISTA\nPensalo.\n"
            f"@@@ ARRANQUE\n{arranque}\n@@@ TESTS\n{tests}\n@@@ SOLUCION\n{solucion}\n@@@ FIN\n")


# --- JavaScript: dos buenos y uno cuyo test PASA con el arranque vacío (no sirve) ---
JS_SUMA = bloque("suma-pares",
                 "// suma los pares\nfunction sumaPares(nums) {\n  // TODO\n}\nmodule.exports = { sumaPares };",
                 "const test = require('node:test');\nconst assert = require('node:assert/strict');\n"
                 "const { sumaPares } = require('__MODULO__');\n"
                 "test('lista normal', () => { assert.equal(sumaPares([1, 2, 3, 4]), 6); });\n"
                 "test('sin pares', () => { assert.equal(sumaPares([1, 3]), 0); });",
                 "```js\nfunction sumaPares(nums) {\n  return nums.filter((n) => n % 2 === 0).reduce((a, b) => a + b, 0);\n}\n"
                 "module.exports = { sumaPares };\n```")
JS_INV = bloque("invertir",
                "function invertir(t) {\n  // TODO\n}\nmodule.exports = { invertir };",
                "const test = require('node:test');\nconst assert = require('node:assert/strict');\n"
                "const { invertir } = require('./__MODULO__');\n"
                "test('invierte hola', () => { assert.equal(invertir('hola'), 'aloh'); });\n"
                "test('vacío', () => { assert.equal(invertir(''), ''); });",
                "function invertir(t) {\n  return [...t].reverse().join('');\n}\nmodule.exports = { invertir };", "media")
JS_MALO = bloque("no-sirve",
                 "function nada() {\n  // TODO\n}\nmodule.exports = { nada };",
                 "const test = require('node:test');\nconst assert = require('node:assert/strict');\n"
                 "const { nada } = require('__MODULO__');\n"
                 "test('no tira error', () => { assert.doesNotThrow(() => nada()); });\n"
                 "test('da 1', () => { assert.equal(nada(), 1); });",
                 "function nada() { return 1; }\nmodule.exports = { nada };", "difícil")

PY_DOBLE = bloque("doble",
                  "def doble(x):\n    \"\"\"El doble de x.\"\"\"\n    # TODO\n    pass",
                  "import unittest\nfrom __MODULO__ import doble\n\n\nclass T(unittest.TestCase):\n"
                  "    def test_dos(self):\n        self.assertEqual(doble(2), 4)\n\n"
                  "    def test_negativo(self):\n        self.assertEqual(doble(-3), -6)",
                  "def doble(x):\n    return 2 * x")
PY_PROM = bloque("promedio",
                 "def promedio(xs):\n    # TODO\n    pass",
                 "import unittest\nfrom __MODULO__ import promedio\n\n\nclass T(unittest.TestCase):\n"
                 "    def test_basico(self):\n        self.assertAlmostEqual(promedio([1, 2]), 1.5)\n\n"
                 "    def test_uno(self):\n        self.assertEqual(promedio([7]), 7)",
                 "def promedio(xs):\n    return sum(xs) / len(xs)")
PY_MAL_SOL = bloque("mal-solucion",  # el test falla con la solución (valor esperado equivocado)
                    "def f():\n    pass",
                    "import unittest\nfrom __MODULO__ import f\n\n\nclass T(unittest.TestCase):\n"
                    "    def test_a(self):\n        self.assertEqual(f(), 3)\n\n    def test_b(self):\n        self.assertEqual(f(), 3)",
                    "def f():\n    return 2")


def clase(d, lenguaje="javascript", codigo="x"):
    c = os.path.join(d, "001 - Clase de prueba")
    os.makedirs(c)
    with open(os.path.join(c, "apuntes.md"), "w") as f:
        f.write("# 📓 Clase de prueba\n")
    json.dump({"resumen": ["r"], "secciones": [{"titulo": "t", "lenguaje": lenguaje, "codigo": codigo}],
               "practica": ["p"]}, open(os.path.join(c, ".apuntes-ia.json"), "w"))
    return c


def silencio(fn, *a, **k):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        r = fn(*a, **k)
    return r, buf.getvalue()


def claude_falso(*respuestas):
    """Devuelve las respuestas en orden y cuenta las llamadas."""
    llamadas = []
    def f(prompt):
        llamadas.append(prompt)
        return respuestas[min(len(llamadas), len(respuestas)) - 1]
    pr.consultar_claude = f
    return llamadas


# 1) parser: bloques, cercas ``` quitadas, slug limpio, incompletos ignorados
ejs = pr.parsear("basura antes\n" + JS_SUMA + bloque("Ñandú Ágil!", "a", "t", "s") + "@@@ EJERCICIO\nnombre: roto\n@@@ ENUNCIADO\nx\n@@@ FIN\n")
assert [e["nombre"] for e in ejs] == ["suma-pares", "nandu-agil"], ejs
assert not ejs[0]["solucion"].startswith("```") and ejs[0]["dificultad"] == "fácil"; ok += 1

# 2) verificación: bueno pasa; test que pasa con el arranque → rechazado; test que falla con la solución → rechazado
assert pr.verificar(pr.parsear(JS_SUMA)[0], "javascript") == ""
p = pr.verificar(pr.parsear(JS_MALO)[0], "javascript")
assert "ARRANQUE" in p and "no tira error" in p, p
assert pr.verificar(pr.parsear(PY_DOBLE)[0], "python") == ""
p = pr.verificar(pr.parsear(PY_MAL_SOL)[0], "python")
assert "SOLUCION" in p and "2 != 3" in p, p; ok += 1

# 3) generación JS completa: se descarta el malo (el reintento también viene malo), archivos correctos
with tempfile.TemporaryDirectory() as d:
    c = clase(d)
    llamadas = claude_falso(JS_SUMA + JS_MALO + JS_INV, JS_MALO)
    r, out = silencio(pr.generar, c)
    assert r == 0 and len(llamadas) == 2 and "PASAN estos tests" in llamadas[1], out
    pd = os.path.join(c, "practica")
    esperados = {"README.md", "package.json", ".practica.json", ".soluciones", "ej01-suma-pares.js",
                 "ej01-suma-pares.test.js", "ej02-invertir.js", "ej02-invertir.test.js"}
    assert set(os.listdir(pd)) == esperados, os.listdir(pd)
    assert "require('./ej02-invertir.js')" in open(os.path.join(pd, "ej02-invertir.test.js")).read()
    assert "// TODO" in open(os.path.join(pd, "ej01-suma-pares.js")).read()
    assert "reverse" in open(os.path.join(pd, ".soluciones", "ej02-invertir.js")).read()
    readme = open(os.path.join(pd, "README.md")).read()
    assert "> [!tip]- 💡 Pista" in readme and "## 2. Título de invertir · 🟡 media" in readme and "--correr" in readme
    assert not [f for f in os.listdir(c) if f.startswith(".practica-nueva")]  # no quedan temporales
    ok += 1

    # 4) --correr: uno bien (copio la solución) y uno mal (arranque) → 1/2, código 1, .resultado.json
    open(os.path.join(pd, "ej01-suma-pares.js"), "w").write(open(os.path.join(pd, ".soluciones", "ej01-suma-pares.js")).read())
    r, out = silencio(pr.correr, c)
    res = json.load(open(os.path.join(pd, ".resultado.json")))
    ultima = out.strip().splitlines()[-1]
    assert r == 1 and res["ok"] == 1 and res["total"] == 2 and not res["todos_ok"], out
    assert ultima.startswith("✅ ej01 suma-pares · ❌ ej02 invertir (AssertionError: esperado 'aloh', obtenido undefined)") \
        and ultima.endswith(" · 1/2"), ultima
    assert res["ejercicios"][1]["error"].startswith("invierte hola: AssertionError") and res["ejercicios"][1]["pasan"] == 0
    ok += 1

    # 5) sin --forzar NO pisa nada (ni llama a Claude); con --forzar lo viejo se guarda
    open(os.path.join(pd, "ej02-invertir.js"), "w").write("// mi código a medias\n")
    llamadas = claude_falso(JS_SUMA + JS_INV)
    r, out = silencio(pr.generar, c)
    assert r == 0 and not llamadas and open(os.path.join(pd, "ej02-invertir.js")).read() == "// mi código a medias\n"
    r, out = silencio(pr.generar, c, forzar=True)
    viejas = [f for f in os.listdir(c) if f.startswith("practica.viejo-")]
    assert r == 0 and len(viejas) == 1 and len(llamadas) == 1, out
    assert open(os.path.join(c, viejas[0], "ej02-invertir.js")).read() == "// mi código a medias\n"
    assert "TODO" in open(os.path.join(pd, "ej02-invertir.js")).read(); ok += 1

# 6) si quedan menos de 2 buenos: falla y NO crea practica/
with tempfile.TemporaryDirectory() as d:
    c = clase(d)
    claude_falso(JS_SUMA + JS_MALO, JS_MALO)
    r, out = silencio(pr.generar, c)
    assert r == 1 and not os.path.exists(os.path.join(c, "practica")) and "mínimo 2" in out, out; ok += 1

# 7) Python: generación + --correr (uno resuelto, uno con error de ejecución que dice dónde) + todo bien → 0
with tempfile.TemporaryDirectory() as d:
    c = clase(d, "python")
    claude_falso(PY_DOBLE + PY_MAL_SOL + PY_PROM, PY_MAL_SOL)
    r, out = silencio(pr.generar, c)
    pd = os.path.join(c, "practica")
    assert r == 0 and sorted(f for f in os.listdir(pd) if f.endswith(".py")) == \
        ["ej01_doble.py", "ej02_promedio.py", "test_ej01_doble.py", "test_ej02_promedio.py"], out
    assert "from ej02_promedio import promedio" in open(os.path.join(pd, "test_ej02_promedio.py")).read()
    open(os.path.join(pd, "ej01_doble.py"), "w").write("def doble(x):\n    return x * 2\n")
    open(os.path.join(pd, "ej02_promedio.py"), "w").write("def promedio(xs):\n    return sum(xs) / len(xz)\n")
    r, out = silencio(pr.correr, c)
    res = json.load(open(os.path.join(pd, ".resultado.json")))
    assert r == 1 and res["lenguaje"] == "python" and res["ejercicios"][0]["ok"], out
    assert "NameError" in res["ejercicios"][1]["error"] and "(ej02_promedio.py:2)" in res["ejercicios"][1]["error"], res
    assert not os.path.exists(os.path.join(pd, "__pycache__"))
    open(os.path.join(pd, "ej02_promedio.py"), "w").write("def promedio(xs):\n    return sum(xs) / len(xs)\n")
    r, out = silencio(pr.correr, c)
    assert r == 0 and out.strip().endswith("✅ ej01 doble · ✅ ej02 promedio · 2/2"), out; ok += 1

# 8) --correr con código que se cuelga o no carga: no se cuelga el programa, lo dice
with tempfile.TemporaryDirectory() as d:
    c = clase(d)
    claude_falso(JS_SUMA + JS_INV)
    silencio(pr.generar, c)
    pd = os.path.join(c, "practica")
    open(os.path.join(pd, "ej01-suma-pares.js"), "w").write("function sumaPares(n) { while (true) {} }\nmodule.exports = { sumaPares };\n")
    open(os.path.join(pd, "ej02-invertir.js"), "w").write("function invertir(t) {\n  return t.split(''.reverse()\n}\n")
    viejo = pr.correr_tests.__defaults__
    pr.correr_tests.__defaults__ = (3,)  # que la prueba no tarde 20 s
    r, out = silencio(pr.correr, c)
    pr.correr_tests.__defaults__ = viejo
    res = json.load(open(os.path.join(pd, ".resultado.json")))
    assert r == 1 and "se colgó" in res["ejercicios"][0]["error"], res
    assert "no carga: SyntaxError" in res["ejercicios"][1]["error"] and "ej02-invertir.js:2" in res["ejercicios"][1]["error"], res
    ok += 1

# 9) detección de lenguaje y "no aplica"
assert pr.detectar_lenguaje({"secciones": [{"lenguaje": "JavaScript", "codigo": "x"}, {"lenguaje": "python", "codigo": ""}]}, "")[0] == "javascript"
assert pr.detectar_lenguaje({"secciones": [{"lenguaje": "", "codigo": ""}]}, "/Curso JavaScript/001 - Intro")[0] == "javascript"
assert pr.detectar_lenguaje({"secciones": [{"lenguaje": "", "codigo": ""}], "conceptos": [{"termino": "PyTorch"}]}, "/x")[0] == "python"
assert pr.detectar_lenguaje({"secciones": [{"lenguaje": "bash", "codigo": "ls"}]}, "/Curso JavaScript")[0] is None
with tempfile.TemporaryDirectory() as d:
    c = clase(d, "rust", "fn main() {}")
    llamadas = claude_falso("")
    r, out = silencio(pr.generar, c)
    assert r == 2 and not llamadas and "rust" in out and not os.path.exists(os.path.join(c, "practica")), out
    r, out = silencio(pr.correr, c)
    assert r == 2, out
    os.remove(os.path.join(c, ".apuntes-ia.json"))
    assert silencio(pr.generar, c)[0] == 2
ok += 1

# 10) clases anteriores (para no pedir temas que el curso no vio): solo en cursos numerados
with tempfile.TemporaryDirectory() as d:
    for n in ("001 - Intro", "002 - Variables", "010 - Objetos", "notas"):
        os.makedirs(os.path.join(d, n))
    assert pr.clases_anteriores(os.path.join(d, "010 - Objetos")) == ["Intro", "Variables"]
    assert pr.clases_anteriores(os.path.join(d, "001 - Intro")) == []
    assert pr.clases_anteriores(os.path.join(d, "notas")) is None
    assert "PRIMERA clase" in pr.armar_prompt("T", {"secciones": []}, "python", os.path.join(d, "001 - Intro"))
    assert "- Variables" in pr.armar_prompt("T", {"secciones": []}, "javascript", os.path.join(d, "010 - Objetos"))
ok += 1

print(f"{ok}/10 pruebas OK")
