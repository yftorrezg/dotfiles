#!/usr/bin/env python3
"""Práctica con tests automáticos para la clase que estás estudiando: ejercicios cortos
(archivo de arranque con `TODO`) + tests que dicen ✅/❌ al instante.

    practica.py <carpeta_de_la_clase> [--forzar] [--lenguaje javascript|python]
    practica.py --correr <carpeta_de_la_clase> [--notificar]

Generar (1 llamada a Claude, ~1 min; imprime el progreso en líneas simples):
  parte de .apuntes-ia.json (lo que armó cuadernillo.py: práctica sugerida, código de las
  secciones, conceptos) y arma <clase>/practica/:
    README.md                 enunciados, dificultad, pista plegada y cómo correr los tests
    ej01-nombre.js            arranque (firma + // TODO) ··· Python: ej01_nombre.py
    ej01-nombre.test.js       tests node:test + node:assert ··· Python: test_ej01_nombre.py (unittest)
    .soluciones/              solución de referencia de cada ejercicio (mirar SOLO si te trabaste)
    .practica.json            metadatos: lenguaje, título, ejercicios [{id, nombre, titulo, dificultad, archivo, test}]
    package.json              (solo JS) {"type": "commonjs"}: que node no adivine el tipo de módulo
  ANTES de entregar, cada ejercicio se verifica en una carpeta temporal: los tests tienen que
  PASAR con la solución y FALLAR TODOS con el arranque (si uno pasa con el arranque vacío, el
  test no sirve). Lo que no cumple se le devuelve a Claude UNA vez con el error; si sigue mal,
  se descarta. Quedan 3 a 5 ejercicios (mínimo 2 buenos; si no, falla sin tocar nada).
  Si ya existe practica/ no hace nada (puede haber código tuyo a medias). Con --forzar, lo
  viejo se mueve a practica.viejo-<fecha>/ (nunca se borra).
  Código de salida: 0 = hecha (o ya existía) · 1 = falló · 2 = no aplica (sin apuntes de IA,
  o la clase no es de JavaScript ni Python).

Correr (--correr): corre los tests de cada ejercicio contra TU código y muestra
    ✅ ej01 suma-pares · ❌ ej02 invertir (AssertionError: esperado [], obtenido undefined) · 1/2
  Código de salida: 0 = todos pasan · 1 = alguno falla · 2 = no hay práctica.
  --notificar además manda el resumen con notify-send (botón del Stream Deck, Centro de estudio).
  El resultado queda en practica/.resultado.json:
    {
      "fecha": "2026-09-29T14:03:12",        # hora local, ISO sin zona
      "clase": "/ruta/absoluta/de/la/clase",
      "lenguaje": "javascript",              # o "python"
      "ok": 1, "total": 2, "todos_ok": false,
      "ejercicios": [
        {"id": "ej01", "nombre": "suma-pares", "titulo": "Sumar los pares",
         "archivo": "ej01-suma-pares.js", "ok": true, "pasan": 4, "tests": 4, "error": ""},
        {"id": "ej02", "nombre": "invertir", "titulo": "…", "archivo": "ej02-invertir.js",
         "ok": false, "pasan": 1, "tests": 3,
         "error": "invierte vacío: AssertionError: esperado [], obtenido undefined"}
      ]
    }
  ("error" = primera línea útil del primer test que falla, o "se colgó…" / error al cargar).
"""
import argparse
import datetime
import importlib.util
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
spec = importlib.util.spec_from_file_location("cuadernillo", os.path.join(AQUI, "cuadernillo.py"))
cu = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cu)  # (de paso deja la salida con line_buffering: el progreso se ve al momento)

# Sonnet escribe muy bien tests chicos y gasta menos cuota. PRACTICA_MODELO=opus para otra cosa.
MODELO = os.environ.get("PRACTICA_MODELO", cu.MODELO)
TIEMPO_MAX = 20        # s por archivo de tests (código generado o del alumno podría colgarse)
MIN_EJERCICIOS, MAX_EJERCICIOS = 2, 5
MIN_TESTS = 2          # un ejercicio con 1 solo test verifica muy poco
DIFICULTAD = {"fácil": "🟢", "facil": "🟢", "media": "🟡", "medio": "🟡", "difícil": "🔴", "dificil": "🔴"}
MARCA = "@@PRACTICA@@ "  # prefijo de las líneas de resultado (los print del alumno no se confunden)


# ------------------------------------------------------------ lenguajes ----
def lenguaje_de(nombre):
    """'javascript' | 'python' | None (no soportado) | '' (vacío)."""
    n = (nombre or "").strip().lower()
    if not n:
        return ""
    if n in ("js", "javascript", "node", "nodejs", "node.js", "jsx", "ecmascript", "mjs", "cjs"):
        return "javascript"
    if n in ("py", "python", "python3", "pytorch", "numpy", "ipython", "jupyter"):
        return "python"
    return None


def detectar_lenguaje(datos, carpeta):
    """(lenguaje, motivo). Primero el código de las secciones; si la clase es pura teoría, las
    palabras del título/curso/conceptos (ej. la intro del curso de JavaScript)."""
    votos, otros = {"javascript": 0, "python": 0}, {}
    for s in datos.get("secciones", []):
        if not str(s.get("codigo", "")).strip():
            continue
        l = lenguaje_de(s.get("lenguaje"))
        if l:
            votos[l] += 1
        elif l is None:
            otros[s["lenguaje"].strip().lower()] = otros.get(s["lenguaje"].strip().lower(), 0) + 1
    if max(votos.values()):
        return max(votos, key=votos.get), "por el código de la clase"
    if otros:
        return None, f"la clase es de {max(otros, key=otros.get)} (solo hay práctica para JavaScript y Python)"
    texto = " ".join([carpeta] + [str(c.get("termino", "")) for c in datos.get("conceptos", [])]
                     + [str(r) for r in datos.get("resumen", [])]).lower()
    votos = {"javascript": len(re.findall(r"javascript|node\.?js|ecmascript", texto)),
             "python": len(re.findall(r"python|pytorch|numpy", texto))}
    if max(votos.values()):
        return max(votos, key=votos.get), "por el tema (la clase casi no tiene código)"
    return None, "no se pudo saber el lenguaje (la clase no tiene código)"


def version(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=15).stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        return ""


def hay_modulo(nombre):
    return importlib.util.find_spec(nombre) is not None


def nombres_de_archivo(lenguaje, num, slug):
    """(arranque, test, módulo para importar) del ejercicio número `num`."""
    if lenguaje == "javascript":
        base = f"ej{num:02d}-{slug}"
        return f"{base}.js", f"{base}.test.js", f"./{base}.js"
    base = f"ej{num:02d}_{slug.replace('-', '_')}"
    return f"{base}.py", f"test_{base}.py", base


def poner_modulo(test, lenguaje, modulo):
    """Los tests de Claude importan '__MODULO__': acá va el nombre real (así se puede renumerar)."""
    if lenguaje == "javascript":
        return re.sub(r"(\./)?__MODULO__(\.js)?", modulo, test)
    return re.sub(r"__MODULO__(\.py)?", modulo, test)


# ---------------------------------------------------------- correr tests ----
# Reporter propio de node:test: una línea JSON por test con la primera línea ÚTIL del error
# (esperado/obtenido en vez del diff gigante) y, si el error viene del código del alumno, dónde.
REPORTER_JS = r"""
import { inspect } from 'node:util';
const OPS = ['strictEqual', 'deepStrictEqual', 'equal', 'deepEqual'];
const corto = (v) => { const s = inspect(v, { depth: 3, breakLength: Infinity }); return s.length > 80 ? s.slice(0, 77) + '…' : s; };
function linea(c) {
  if (c == null) return '';
  if (typeof c !== 'object') return String(c);
  const primera = String(c.message ?? '').split('\n').find((l) => l.trim()) ?? '';
  let txt;
  if (c.code === 'ERR_ASSERTION' && OPS.includes(c.operator)) {
    txt = `${c.name}: ${c.generatedMessage === false ? primera + ' — ' : ''}esperado ${corto(c.expected)}, obtenido ${corto(c.actual)}`;
  } else {
    txt = `${c.name || 'Error'}: ${primera}`;
  }
  if (c.code !== 'ERR_ASSERTION') {  // un TypeError en el código del alumno: decir en qué línea
    const m = String(c.stack ?? '').split('\n').map((l) => l.match(/\/([^\/()]+\.js):(\d+)/))
      .find((m) => m && !m[1].endsWith('.test.js'));
    if (m) txt += ` (${m[1]}:${m[2]})`;
  }
  return txt;
}
export default async function* (source) {
  for await (const ev of source) {
    const d = ev.data ?? {};
    if ((ev.type === 'test:pass' || ev.type === 'test:fail') && d.details?.type !== 'suite') {
      const e = d.details?.error;
      yield '@@PRACTICA@@ ' + JSON.stringify({ nombre: d.name, ok: ev.type === 'test:pass', error: e ? linea(e.cause ?? e) : '' }) + '\n';
    } else if (ev.type === 'test:stderr') {
      yield '@@PRACTICA@@ ' + JSON.stringify({ stderr: d.message }) + '\n';
    }
  }
}
"""

# Lo mismo para Python: corre un módulo de unittest y emite una línea JSON por test.
RUNNER_PY = r"""
import importlib, json, os, sys, traceback, unittest
sys.path.insert(0, os.getcwd())
MARCA, modulo = "@@PRACTICA@@ ", sys.argv[1]

def linea(err):
    tipo, exc, tb = err
    lineas = "".join(traceback.format_exception_only(tipo, exc)).splitlines()
    txt = next((l for l in lineas if l.strip() and not l.startswith(" ")), lineas[-1] if lineas else str(tipo))
    if not issubclass(tipo, AssertionError):  # dónde: la última línea en código que no es el test
        if isinstance(exc, SyntaxError) and exc.filename:
            txt += f" ({os.path.basename(exc.filename)}:{exc.lineno})"
        else:
            marcos = [f for f in traceback.extract_tb(tb) if f.filename.startswith(os.getcwd())
                      and not os.path.basename(f.filename).startswith("test_")]
            if marcos:
                txt += f" ({os.path.basename(marcos[-1].filename)}:{marcos[-1].lineno})"
            elif "NoneType" in txt:  # el error salta en el test porque la función devolvió None
                txt += " — ¿falta el return?"
    return txt[:300]

try:
    mod = importlib.import_module(modulo)
except BaseException:
    print(MARCA + json.dumps({"carga": linea(sys.exc_info())}))
    sys.exit(0)
suite = unittest.defaultTestLoader.loadTestsFromModule(mod)
fallos = {}

class Resultado(unittest.TestResult):
    def addFailure(self, t, err): fallos.setdefault(t.id(), linea(err))
    def addError(self, t, err): fallos.setdefault(t.id(), linea(err))
    def addSubTest(self, t, sub, err):
        if err is not None:
            fallos.setdefault(t.id(), linea(err))

def aplanar(s):
    for t in s:
        yield from (aplanar(t) if isinstance(t, unittest.TestSuite) else [t])

tests = list(aplanar(suite))
suite.run(Resultado())
for t in tests:
    print(MARCA + json.dumps({"nombre": getattr(t, "_testMethodName", t.id()), "ok": t.id() not in fallos,
                              "error": fallos.get(t.id(), "")}))
for id_, err in fallos.items():  # errores fuera de un test (setUpClass...)
    if id_ not in {t.id() for t in tests}:
        print(MARCA + json.dumps({"nombre": id_, "ok": False, "error": err}))
"""


def ejecutar(cmd, cwd, timeout):
    """(salida, colgado). Mata el grupo de procesos entero si se pasa del tiempo."""
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", NODE_NO_WARNINGS="1")
    p = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL,
                         text=True, env=env, start_new_session=True)
    try:
        out, err = p.communicate(timeout=timeout)
        return out + "\n" + err, False
    except subprocess.TimeoutExpired:
        try:
            os.killpg(p.pid, signal.SIGKILL)
        except OSError:
            pass
        p.communicate()
        return "", True


def correr_tests(carpeta, archivo_test, lenguaje, timeout=TIEMPO_MAX):
    """Corre un archivo de tests. Devuelve {"tests": [{nombre, ok, error}], "error": str}.
    "error" es un problema de todo el archivo: se colgó o el código no carga."""
    aux = tempfile.mkdtemp(prefix="practica-")
    try:
        if lenguaje == "javascript":
            rep = os.path.join(aux, "reporter.mjs")
            with open(rep, "w", encoding="utf-8") as f:
                f.write(REPORTER_JS)
            cmd = ["node", "--test", f"--test-timeout={timeout * 1000 // 2}", f"--test-reporter={rep}", archivo_test]
        else:
            modulo = os.path.splitext(archivo_test)[0]
            cmd = [sys.executable, "-c", RUNNER_PY, modulo]
        salida, colgado = ejecutar(cmd, carpeta, timeout)
    finally:
        shutil.rmtree(aux, ignore_errors=True)
    if colgado:
        return {"tests": [], "error": f"se colgó (más de {timeout} s): ¿un ciclo infinito?"}
    tests, stderr, carga = [], [], ""
    for l in salida.splitlines():
        if not l.startswith(MARCA):
            continue
        try:
            d = json.loads(l[len(MARCA):])
        except ValueError:
            continue
        if "stderr" in d:
            stderr.append(d["stderr"])
        elif "carga" in d:
            carga = d["carga"]
        else:
            tests.append(d)
    # node: si el archivo ni carga, aparece un "test" con el nombre del archivo y el error real en stderr
    fallo_archivo = [t for t in tests if t["nombre"] and t["nombre"].endswith(archivo_test)]
    if fallo_archivo:
        tests = [t for t in tests if t not in fallo_archivo]
        lineas = "".join(stderr).splitlines()
        carga = next((l.strip() for l in lineas if re.match(r"\s*\w*(Error|Exception)\b", l)),
                     fallo_archivo[0]["error"] or "no carga")
        donde = next((m for m in (re.match(r"(/.*?\.js):(\d+)", l) for l in lineas) if m), None)
        if donde and not donde[1].endswith(".test.js"):
            carga += f" ({os.path.basename(donde[1])}:{donde[2]})"
    if carga:
        return {"tests": tests, "error": f"no carga: {carga}"}
    if not tests:
        return {"tests": [], "error": "no se encontró ningún test"}
    return {"tests": tests, "error": ""}


def primer_error(r):
    """La línea útil para mostrar: problema del archivo, o el primer test que falla."""
    if r["error"]:
        return r["error"]
    for t in r["tests"]:
        if not t["ok"]:
            return f"{t['nombre']}: {t['error']}" if t["error"] else t["nombre"]
    return ""


# ------------------------------------------------------------------- IA ----
PROMPT = """Eres un profesor de programación que arma PRÁCTICA CON TESTS AUTOMÁTICOS para un alumno que acaba de ver una clase en video.
El alumno aprende escribiendo código y equivocándose: cada ejercicio trae un archivo de ARRANQUE (firma + TODO) que él completa y TESTS que le dicen al instante si está bien.

Clase: {titulo}
Lenguaje: {lenguaje}
{anteriores}

Apuntes de la clase (JSON):
<<<
{apuntes}
>>>

Arma 4 ejercicios (mínimo 3, máximo 5) sobre ESTA clase:
- Basados en lo que se ve en la clase: usa "practica", el código de "secciones" y "conceptos". Para resolverlos solo debe hacer falta lo de esta clase y lo de las clases anteriores (si no hay lista de clases anteriores, lo básico del lenguaje): nada de temas que el curso todavía no vio.
- Si la clase es casi pura teoría, haz ejercicios de "predecí el resultado" (una función que devuelve lo que daría un fragmento de código de la clase) o funciones pequeñas que usen sus conceptos.
- Progresivos: el primero fácil, el último el más difícil. Cada uno se resuelve en 5 a 15 minutos.
- Cada ejercicio = una o dos funciones PURAS y testeables: reciben datos y DEVUELVEN el resultado. Nada de imprimir, pedir datos al usuario, DOM, red, archivos, fecha/hora actual ni azar.
- El enunciado dice EXACTAMENTE lo que verifican los tests (nombre de la función, parámetros, qué devuelve y en qué formato) y trae al menos un ejemplo `entrada → salida`.

{reglas}

Reglas de los TESTS:
- 3 a 6 tests por ejercicio, con nombres descriptivos en español: casos normales y bordes (vacío, negativos, etc. si aplican).
- CADA test debe FALLAR con el arranque tal cual (que no devuelve nada): nunca un test que solo compare con {nada}, que solo verifique que "no tira error", que "no modifica la entrada" o el tipo de algo, sin exigir además el resultado correcto.
- Los valores esperados tienen que ser correctos: calculalos con cuidado paso a paso. Con decimales, comparación aproximada.

Responde SOLO con los ejercicios en este formato de bloques (sin JSON, sin ``` ni texto antes o después). Cada marcador @@@ va solo, al principio de su línea:

@@@ EJERCICIO
nombre: suma-pares
titulo: Sumar los números pares
dificultad: fácil
@@@ ENUNCIADO
(Markdown en español, 3 a 8 líneas: qué hacer, la firma y un ejemplo entrada → salida)
@@@ PISTA
(1 a 3 líneas que orienten sin dar la solución)
@@@ ARRANQUE
(código)
@@@ TESTS
(código)
@@@ SOLUCION
(código)
@@@ FIN

"nombre": minúsculas sin acentos, 1 a 3 palabras separadas con guiones. "dificultad": fácil, media o difícil."""

REGLAS_JS = """Archivos en JavaScript para Node {node} con CommonJS (require / module.exports), sin paquetes de npm:
- ARRANQUE: las mismas funciones que la SOLUCION, con sus parámetros, un comentario corto arriba de cada una y el cuerpo vacío salvo `// TODO` (sin return). Termina con `module.exports = {{ nombreFuncion }};`.
- SOLUCION: el mismo archivo resuelto (misma firma, mismo module.exports), claro, con comentarios en español y el estilo de la clase.
- TESTS, exactamente con esta estructura (la ruta '__MODULO__' la reemplaza el programa; no la cambies):
const test = require('node:test');
const assert = require('node:assert/strict');
const {{ nombreFuncion }} = require('__MODULO__');

test('suma los pares de una lista normal', () => {{
  assert.equal(nombreFuncion([1, 2, 3, 4]), 6);
}});
  Usa assert.equal / assert.deepEqual (son estrictos: el primer argumento es lo obtenido, el segundo lo esperado) y assert.throws para errores esperados."""

REGLAS_PY = """Archivos en Python {python}, solo librería estándar{numpy}:
- ARRANQUE: las mismas funciones que la SOLUCION, con su firma, un docstring corto en español y el cuerpo `# TODO` + `pass`.
- SOLUCION: el mismo archivo resuelto (misma firma), claro, con comentarios en español y el estilo de la clase.
- TESTS con unittest, exactamente con esta estructura (el módulo '__MODULO__' lo reemplaza el programa; no lo cambies):
import unittest
from __MODULO__ import nombre_funcion


class TestNombreFuncion(unittest.TestCase):
    def test_suma_los_pares_de_una_lista_normal(self):
        self.assertEqual(nombre_funcion([1, 2, 3, 4]), 6)
  Primero lo obtenido y después lo esperado; assertAlmostEqual para decimales, assertRaises para errores esperados. Sin docstrings en los tests y sin `if __name__ == "__main__"`."""

REINTENTO = """

----
Ya generaste estos ejercicios, pero NO pasaron la verificación automática (los tests se corren contra la SOLUCION —tienen que pasar todos— y contra el ARRANQUE —tienen que fallar todos—):

{problemas}

Corregilos (podés cambiar tests, solución o arranque: si un test pasa con el arranque vacío, hacé que exija el resultado correcto; si falla con la solución, revisá el valor esperado o la solución).
Responde SOLO con los {n} ejercicios corregidos, en el mismo formato de bloques @@@, en el mismo orden."""


def armar_prompt(titulo, datos, lenguaje, carpeta=""):
    apuntes = {k: datos.get(k) for k in ("resumen", "conceptos", "secciones", "practica", "errores_comunes")}
    if lenguaje == "javascript":
        reglas = REGLAS_JS.format(node=version(["node", "--version"]) or "18+")
        nombre, nada = "JavaScript (Node)", "undefined"
    else:
        extra = ("; numpy está instalado y podés usarlo si la clase lo usa" if hay_modulo("numpy") else "; numpy NO está instalado")
        if not hay_modulo("torch"):
            extra += ". PyTorch NO está instalado: si la clase usa torch, hacé los ejercicios en Python puro (o numpy) con la misma idea"
        reglas = REGLAS_PY.format(python=".".join(map(str, sys.version_info[:2])), numpy=extra)
        nombre, nada = "Python", "None"
    previas = clases_anteriores(carpeta)
    if previas is None:
        anteriores = ""
    elif not previas:
        anteriores = ("Es la PRIMERA clase del curso: el alumno recién empieza. Si la clase es de pura teoría, "
                      "ejercicios MUY básicos (devolver un valor, una cuenta simple, un string) sin estructuras que aún no vio.\n")
    else:
        anteriores = "Clases anteriores del curso (lo que el alumno ya vio):\n" + "\n".join(f"- {c}" for c in previas) + "\n"
    return PROMPT.format(titulo=titulo, lenguaje=nombre, apuntes=json.dumps(apuntes, ensure_ascii=False, indent=1),
                         reglas=reglas, nada=nada, anteriores=anteriores)


def clases_anteriores(carpeta, maximo=40):
    """Títulos de las clases anteriores del curso (carpetas hermanas "NNN - …" con número menor),
    para que los ejercicios no pidan cosas que todavía no se vieron. None = no es un curso numerado
    (ej. un video suelto: sus "hermanas" serían otros cursos)."""
    m = re.match(r"(\d{2,}) - ", os.path.basename(carpeta))
    if not m:
        return None
    try:
        hermanas = os.listdir(os.path.dirname(carpeta))
    except OSError:
        return None
    previas = sorted(h for h in hermanas if (n := re.match(r"(\d{2,}) - (.+)", h)) and int(n[1]) < int(m[1])
                     and os.path.isdir(os.path.join(os.path.dirname(carpeta), h)))
    return [re.sub(r"^\d+ - ", "", h) for h in previas][-maximo:]


def consultar_claude(prompt):
    """Texto de la respuesta, o None. Espera si se agotó la cuota (llamar_claude de cuadernillo).
    Las pruebas reemplazan esta función por una respuesta fija."""
    cmd = [cu.ruta_claude(), "-p", "--output-format", "json", "--tools", "", "--strict-mcp-config",
           "--no-session-persistence", "--system-prompt",
           "Eres un asistente que responde exactamente en el formato pedido."]
    if MODELO:
        cmd += ["--model", MODELO]
    return cu.llamar_claude(cmd, prompt)


def slug(texto):
    t = unicodedata.normalize("NFKD", str(texto)).encode("ascii", "ignore").decode().lower()
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:30].strip("-")
    return t or "ejercicio"


def sin_cercas(codigo):
    """Claude a veces envuelve el código en ```js … ``` aunque se le pida que no."""
    lineas = codigo.strip("\n").split("\n")
    if lineas and lineas[0].strip().startswith("```"):
        lineas = lineas[1:]
    if lineas and lineas[-1].strip() == "```":
        lineas = lineas[:-1]
    return "\n".join(lineas).strip("\n") + "\n"


def parsear(texto):
    """Respuesta en bloques @@@ → [{nombre, titulo, dificultad, enunciado, pista, arranque, tests,
    solucion, crudo}]. Ejercicios incompletos se ignoran. (Bloques y no JSON: el código dentro de
    un JSON obliga a escapar comillas y saltos de línea, y ahí es donde más se equivoca.)"""
    ejercicios = []
    for trozo in re.split(r"^@@@ *EJERCICIO *$", texto or "", flags=re.M)[1:]:
        trozo = re.split(r"^@@@ *FIN *$", trozo, flags=re.M)[0]
        partes = re.split(r"^@@@ *([A-ZÓ]+) *$", trozo, flags=re.M)
        ej = {"crudo": "@@@ EJERCICIO" + trozo.rstrip() + "\n@@@ FIN"}
        for linea in partes[0].splitlines():  # cabecera "clave: valor"
            k, _, v = linea.partition(":")
            if v.strip() and k.strip().lower() in ("nombre", "titulo", "título", "dificultad"):
                ej[k.strip().lower().replace("í", "i")] = v.strip()
        for clave, contenido in zip(partes[1::2], partes[2::2]):
            clave = clave.lower().replace("ó", "o")
            ej[clave] = contenido.strip("\n") if clave in ("enunciado", "pista") else sin_cercas(contenido)
        if all(ej.get(k, "").strip() for k in ("enunciado", "arranque", "tests", "solucion")):
            ej["nombre"] = slug(ej.get("nombre") or ej.get("titulo") or "")
            ej.setdefault("titulo", ej["nombre"].replace("-", " ").capitalize())
            ej["dificultad"] = ej.get("dificultad", "media").lower()
            ejercicios.append(ej)
    return ejercicios


# ---------------------------------------------------------- verificación ----
def verificar(ej, lenguaje):
    """"" si el ejercicio sirve; si no, el problema (para mostrárselo a Claude)."""
    arranque, test, modulo = nombres_de_archivo(lenguaje, 1, ej["nombre"])
    with tempfile.TemporaryDirectory(prefix="practica-verif-") as d:
        with open(os.path.join(d, test), "w", encoding="utf-8") as f:
            f.write(poner_modulo(ej["tests"], lenguaje, modulo))
        if lenguaje == "javascript":
            with open(os.path.join(d, "package.json"), "w") as f:
                f.write('{"type": "commonjs"}\n')
        # 1) con la solución: tienen que pasar TODOS
        with open(os.path.join(d, arranque), "w", encoding="utf-8") as f:
            f.write(ej["solucion"])
        r = correr_tests(d, test, lenguaje)
        if r["error"]:
            return f"con la SOLUCION: {r['error']}"
        malos = [t for t in r["tests"] if not t["ok"]]
        if malos:
            return "con la SOLUCION fallan estos tests: " + "; ".join(f"«{t['nombre']}»: {t['error']}" for t in malos)
        if len(r["tests"]) < MIN_TESTS:
            return f"tiene solo {len(r['tests'])} test(s): hacen falta al menos {MIN_TESTS}"
        # 2) con el arranque: tienen que fallar TODOS (y el arranque tiene que cargar)
        with open(os.path.join(d, arranque), "w", encoding="utf-8") as f:
            f.write(ej["arranque"])
        r = correr_tests(d, test, lenguaje)
        if r["error"]:
            return f"con el ARRANQUE: {r['error']} (el arranque tiene que cargar sin errores)"
        buenos = [t for t in r["tests"] if t["ok"]]
        if buenos:
            return ("con el ARRANQUE vacío PASAN estos tests (no verifican nada): "
                    + "; ".join(f"«{t['nombre']}»" for t in buenos))
    return ""


def generar_ejercicios(titulo, datos, lenguaje, carpeta=""):
    """1 llamada a Claude (+1 si hace falta corregir). Devuelve los ejercicios verificados."""
    prompt = armar_prompt(titulo, datos, lenguaje, carpeta)
    print(f"🤖 Pidiendo los ejercicios a Claude ({MODELO or 'modelo de la cuenta'})… (~1 min)")
    ejercicios = parsear(consultar_claude(prompt))
    reintento_usado = False
    if not ejercicios:  # respuesta ilegible: se usa el reintento en pedir todo de nuevo
        print("   (respuesta de Claude inválida: pido de nuevo)")
        reintento_usado = True
        ejercicios = parsear(consultar_claude(prompt))
        if not ejercicios:
            return []
    print(f"🧪 Verificando {len(ejercicios)} ejercicios (tests con la solución y con el arranque)…")
    buenos, malos = {}, {}
    for k, ej in enumerate(ejercicios):
        problema = verificar(ej, lenguaje)
        print(f"   {'✅' if not problema else '❌'} {ej['nombre']}" + (f" — {problema[:150]}" if problema else ""))
        (malos if problema else buenos)[k] = (ej, problema)
    if malos and not reintento_usado:
        print(f"🔁 Pidiendo a Claude que corrija {len(malos)} ejercicio(s)…")
        problemas = "\n\n".join(f"{ej['crudo']}\nPROBLEMA: {p}" for ej, p in malos.values())
        arreglados = parsear(consultar_claude(prompt + REINTENTO.format(problemas=problemas, n=len(malos))))
        for k, ej in zip(list(malos), arreglados):  # en el mismo orden: vuelven a su lugar
            problema = verificar(ej, lenguaje)
            print(f"   {'✅' if not problema else '🗑️'} {ej['nombre']}"
                  + (f" — descartado: {problema[:150]}" if problema else " (corregido)"))
            if not problema:
                buenos[k] = (ej, "")
    elif malos:
        print(f"🗑️ Descartados {len(malos)} ejercicio(s) que no pasaron la verificación")
    return [buenos[k][0] for k in sorted(buenos)][:MAX_EJERCICIOS]


# ---------------------------------------------------------------- armado ----
def armar_readme(titulo, carpeta_clase, lenguaje, ejercicios):
    practica = os.path.join(carpeta_clase, "practica")
    script = os.path.join(AQUI, "practica.py").replace(os.path.expanduser("~"), "~")
    L = [f"# 🏋️ Práctica: {titulo}", ""]
    L += ["> 📓 [Apuntes](../apuntes.md) · ⚡ [Repaso rápido](../resumen.md) · "
          f"💻 {'JavaScript (Node)' if lenguaje == 'javascript' else 'Python'} · {len(ejercicios)} ejercicios", ""]
    L += ["Escribí tu código en cada archivo de arranque (buscá `TODO`), corré los tests y repetí hasta "
          "que den ✅. Equivocarse es parte: leé el error, pensá por qué, corregí.", ""]
    L += ["## ▶️ Cómo correr los tests", ""]
    L += ["Todos, con resumen ✅/❌:", "", "```bash", f'python3 {script} --correr "{carpeta_clase}"', "```", ""]
    if lenguaje == "javascript":
        uno, todos = "node --test ej01-….test.js", "node --test"
    else:
        uno, todos = "python3 -m unittest test_ej01_…", "python3 -m unittest"
    L += ["Desde la carpeta `practica/` (con todo el detalle del error):", "", "```bash",
          f'cd "{practica}"', f"{todos}          # todos", f"{uno}   # uno solo", "```", ""]
    L += ["> [!warning]- 🔒 Soluciones", "> Están en la carpeta oculta `.soluciones/`. Miralas SOLO si te trabaste "
          "de verdad (después de intentarlo un rato y de usar la pista): primero peleala.", ""]
    L += ["---", ""]
    for k, ej in enumerate(ejercicios, 1):
        arranque, test, _ = nombres_de_archivo(lenguaje, k, ej["nombre"])
        dif = ej["dificultad"]
        L += [f"## {k}. {ej['titulo']} · {DIFICULTAD.get(dif, '⚪')} {dif}", ""]
        L += [f"📝 **Tu archivo:** `{arranque}` · 🧪 **Tests:** `{test}`", ""]
        L += [ej["enunciado"].strip(), ""]
        if ej.get("pista", "").strip():
            L += ["> [!tip]- 💡 Pista"] + [f"> {l}" for l in ej["pista"].strip().splitlines()] + [""]
        L += ["- [ ] Resuelto", "", "---", ""]
    L += [f"*Generado por practica.py · tests verificados contra la solución y el arranque*", ""]
    return "\n".join(L)


def escribir_practica(destino, titulo, carpeta_clase, lenguaje, ejercicios):
    os.makedirs(os.path.join(destino, ".soluciones"))
    meta = {"lenguaje": lenguaje, "titulo": titulo, "modelo": MODELO or "",
            "generado": datetime.datetime.now().isoformat(timespec="seconds"), "ejercicios": []}
    for k, ej in enumerate(ejercicios, 1):
        arranque, test, modulo = nombres_de_archivo(lenguaje, k, ej["nombre"])
        for ruta, contenido in ((arranque, ej["arranque"]), (test, poner_modulo(ej["tests"], lenguaje, modulo)),
                                (os.path.join(".soluciones", arranque), ej["solucion"])):
            with open(os.path.join(destino, ruta), "w", encoding="utf-8") as f:
                f.write(contenido)
        meta["ejercicios"].append({"id": f"ej{k:02d}", "nombre": ej["nombre"], "titulo": ej["titulo"],
                                   "dificultad": ej["dificultad"], "archivo": arranque, "test": test})
    if lenguaje == "javascript":
        with open(os.path.join(destino, "package.json"), "w", encoding="utf-8") as f:
            f.write('{"type": "commonjs"}\n')
    with open(os.path.join(destino, ".practica.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
    with open(os.path.join(destino, "README.md"), "w", encoding="utf-8") as f:
        f.write(armar_readme(titulo, carpeta_clase, lenguaje, ejercicios))


def titulo_de(carpeta):
    try:  # el título real está en la primera línea de apuntes.md (como en resumen-corto.py)
        primera = open(os.path.join(carpeta, "apuntes.md"), encoding="utf-8").readline()
        return primera.removeprefix("# 📓 ").strip() or os.path.basename(carpeta)
    except OSError:
        return os.path.basename(carpeta)


def generar(carpeta, forzar=False, lenguaje=None):
    """0 = hecha o ya estaba · 1 = falló · 2 = no aplica."""
    destino = os.path.join(carpeta, "practica")
    if os.path.exists(destino) and not forzar:
        print(f"Ya existe {destino} (usar --forzar para rehacerla; lo viejo se guarda aparte)")
        return 0
    try:
        datos = json.load(open(os.path.join(carpeta, ".apuntes-ia.json"), encoding="utf-8"))
    except (OSError, ValueError):
        print("Sin .apuntes-ia.json (la clase no tiene apuntes de IA): no hay de dónde sacar ejercicios")
        return 2
    titulo = titulo_de(carpeta)
    print(f"🏋️ Práctica de: {titulo}")
    if lenguaje:
        motivo = "elegido a mano"
    else:
        lenguaje, motivo = detectar_lenguaje(datos, carpeta)
    if not lenguaje:
        print(f"⚠️ No aplica: {motivo}")
        return 2
    if not shutil.which("node" if lenguaje == "javascript" else sys.executable):
        print("⚠️ No está instalado node: no se pueden correr los tests de JavaScript")
        return 1
    print(f"💻 Lenguaje: {lenguaje} ({motivo})")
    try:
        ejercicios = generar_ejercicios(titulo, datos, lenguaje, carpeta)
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        print(f"❌ No se pudo usar Claude: {e}")
        return 1
    if len(ejercicios) < MIN_EJERCICIOS:
        print(f"❌ Solo {len(ejercicios)} ejercicio(s) pasaron la verificación (mínimo {MIN_EJERCICIOS}): "
              "no se creó la práctica. Probá de nuevo más tarde.")
        return 1
    # se arma todo aparte y recién al final se pone en su lugar (si algo falla, no queda a medias)
    nueva = tempfile.mkdtemp(prefix=".practica-nueva-", dir=carpeta)
    try:
        escribir_practica(nueva, titulo, carpeta, lenguaje, ejercicios)
        if os.path.exists(destino):  # --forzar: lo viejo (quizá con tu código) se guarda, no se borra
            viejo = os.path.join(carpeta, "practica.viejo-" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
            os.rename(destino, viejo)
            print(f"📦 La práctica anterior quedó en {os.path.basename(viejo)}/")
        os.rename(nueva, destino)
    finally:
        shutil.rmtree(nueva, ignore_errors=True)
    print(f"🏋️ Listo: {len(ejercicios)} ejercicios en {destino}")
    print(f"   Leé {os.path.join(destino, 'README.md')} y corré: practica.py --correr \"{carpeta}\"")
    return 0


# ---------------------------------------------------------------- correr ----
def buscar_ejercicios(practica):
    """[(id, nombre, titulo, archivo, test, lenguaje)] de los archivos que hay en practica/."""
    meta = {}
    try:
        for e in json.load(open(os.path.join(practica, ".practica.json"), encoding="utf-8")).get("ejercicios", []):
            meta[e["test"]] = e
    except (OSError, ValueError, KeyError, TypeError):
        pass
    salida = []
    for f in sorted(os.listdir(practica)):
        m = re.fullmatch(r"(ej\d+)-(.+)\.test\.js", f)
        if m:
            lenguaje, archivo = "javascript", f"{m[1]}-{m[2]}.js"
        else:
            m = re.fullmatch(r"test_(ej\d+)_(.+)\.py", f)
            if not m:
                continue
            lenguaje, archivo = "python", f"{m[1]}_{m[2]}.py"
        e = meta.get(f, {})
        nombre = e.get("nombre") or m[2].replace("_", "-")
        salida.append((m[1], nombre, e.get("titulo", nombre), archivo, f, lenguaje))
    return salida


def correr(carpeta, notificar=False):
    practica = os.path.join(carpeta, "practica")
    ejercicios = buscar_ejercicios(practica) if os.path.isdir(practica) else []
    if not ejercicios:
        print(f"No hay práctica en {carpeta} (generala con: practica.py \"{carpeta}\")")
        if notificar:
            avisar("🏋️ Práctica", "Esta clase todavía no tiene práctica")
        return 2
    resultados = []
    for id_, nombre, titulo, archivo, test, lenguaje in ejercicios:
        r = correr_tests(practica, test, lenguaje)
        pasan = sum(t["ok"] for t in r["tests"])
        ok = not r["error"] and bool(r["tests"]) and pasan == len(r["tests"])
        resultados.append({"id": id_, "nombre": nombre, "titulo": titulo, "archivo": archivo, "ok": ok,
                           "pasan": pasan, "tests": len(r["tests"]), "error": "" if ok else primer_error(r)})
        lenguaje_clase = lenguaje
    bien = sum(r["ok"] for r in resultados)
    for r in resultados:  # una línea por ejercicio, con el detalle
        detalle = "" if r["ok"] else f" — {r['error']}"
        print(f"{'✅' if r['ok'] else '❌'} {r['id']} {r['nombre']} ({r['pasan']}/{r['tests']} tests){detalle}")
    print(resumen(resultados))
    with open(os.path.join(practica, ".resultado.json"), "w", encoding="utf-8") as f:
        json.dump({"fecha": datetime.datetime.now().isoformat(timespec="seconds"), "clase": carpeta,
                   "lenguaje": lenguaje_clase, "ok": bien, "total": len(resultados),
                   "todos_ok": bien == len(resultados), "ejercicios": resultados}, f, ensure_ascii=False, indent=1)
    if notificar:
        titulo = f"🏋️ Práctica: {bien}/{len(resultados)} " + ("🎉 ¡todo bien!" if bien == len(resultados) else "")
        cuerpo = "\n".join(f"{'✅' if r['ok'] else '❌'} {r['id']} {r['nombre']}"
                           + ("" if r["ok"] else f" · {acortar(error_corto(r['error']), 80)}") for r in resultados)
        avisar(titulo.strip(), cuerpo)
    return 0 if bien == len(resultados) else 1


def acortar(texto, n):
    return texto if len(texto) <= n else texto[:n - 1] + "…"


def error_corto(error):
    """El error sin el nombre del test (para la línea de resumen y la notificación)."""
    if ": " in error and not error.startswith(("no carga", "se colgó")):
        return error.split(": ", 1)[1]
    return error


def resumen(resultados):
    """✅ ej01 suma-pares · ❌ ej02 invertir (AssertionError: esperado …, obtenido …) · 1/2"""
    partes = []
    for r in resultados:  # en la línea corta va solo el error; el detalle está en las líneas de arriba
        partes.append(f"✅ {r['id']} {r['nombre']}" if r["ok"]
                      else f"❌ {r['id']} {r['nombre']} ({acortar(error_corto(r['error']), 90)})")
    return " · ".join(partes + [f"{sum(r['ok'] for r in resultados)}/{len(resultados)}"])


def avisar(titulo, cuerpo):
    try:
        subprocess.run(["notify-send", "-a", "Práctica", titulo, cuerpo], timeout=10)
    except (OSError, subprocess.TimeoutExpired):
        pass


def main():
    p = argparse.ArgumentParser(description="Práctica con tests automáticos de una clase")
    p.add_argument("carpeta", help="carpeta de la clase (la que tiene apuntes.md y .apuntes-ia.json)")
    p.add_argument("--correr", action="store_true", help="correr los tests de tu código y mostrar ✅/❌")
    p.add_argument("--notificar", action="store_true", help="(con --correr) mandar el resumen con notify-send")
    p.add_argument("--forzar", action="store_true", help="rehacer la práctica (la vieja se guarda en practica.viejo-<fecha>/)")
    p.add_argument("--lenguaje", choices=["javascript", "python"], help="no detectarlo: usar este")
    a = p.parse_args()
    carpeta = os.path.abspath(a.carpeta).rstrip("/")
    if a.correr:
        return correr(carpeta, a.notificar)
    return generar(carpeta, a.forzar, a.lenguaje)


if __name__ == "__main__":
    sys.exit(main())
