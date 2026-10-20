#!/usr/bin/env python3
"""Pruebas de estudiar.py (Centro de estudio) y de los estados del panel (sin ventana, sin Claude).
Todo en carpetas temporales: nunca toca ~/Vídeos/Mis cursos.md ni el estado real."""
import importlib.util, json, multiprocessing, os, re, subprocess, sys, tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
TMP = tempfile.mkdtemp(prefix="estudiar-tests-")
# antes de cargar el módulo: que lea/escriba solo en temporales
os.environ.update(ESTUDIAR_BASE=os.path.join(TMP, "boveda-vacia"), ESTUDIAR_ESTADO=os.path.join(TMP, "estado.json"),
                  ESTUDIAR_NOTIFICAR="0", ESTUDIAR_PRACTICA=os.path.join(TMP, "no-existe-practica.py"))
os.makedirs(os.environ["ESTUDIAR_BASE"])


def cargar(nombre, archivo):
    spec = importlib.util.spec_from_file_location(nombre, os.path.join(AQUI, archivo))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


es = cargar("es", "estudiar.py")
pc = es.pc
ok = 0

PREG = [{"pregunta": f"¿P{i}?", "respuesta": f"R{i}."} for i in range(5)]
CONC = [{"termino": "Corto", "definicion": "muy corto"},
        {"termino": "Hoisting", "definicion": "Mecanismo que sube las declaraciones de var al inicio del ámbito."},
        {"termino": "Scope", "definicion": "Zona del código donde una variable existe y se puede usar."},
        {"termino": "Bloque", "definicion": "Lo que está entre llaves { } en el código."}]


def clase(d, titulo=None, corto=None, largo=None, yt=None):
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "apuntes.md"), "w").write(f"# 📓 {titulo or os.path.basename(d)}\n\n> ⏱️ **Duración:** 10:00 · x\n")
    open(os.path.join(d, "resumen.md"), "w").write("x")
    if corto is not None:
        json.dump(corto, open(os.path.join(d, ".resumen-ia.json"), "w"), ensure_ascii=False)
    if largo is not None:
        json.dump(largo, open(os.path.join(d, ".apuntes-ia.json"), "w"), ensure_ascii=False)
    if yt:
        open(os.path.join(d, ".youtube-id"), "w").write(yt + "\n")
    return d


NOMBRES = ["001 - Curso JavaScript- 1. Introducción - #jonmircha", "002 - AprendeJavascript.org - #jonmircha",
           "003 - Curso JavaScript- 3. Variables- var 🥊VS🥊 let - #jonmircha", "004 - Curso JavaScript- 11. Arreglos [Arrays] - #jonmircha"]


def boveda():
    """Bóveda de prueba: curso JS de 4 clases + curso de una clase suelta."""
    base = tempfile.mkdtemp(dir=TMP)
    cap = os.path.join(base, "Capturas de YouTube", "Curso JavaScript", "capturas")
    os.makedirs(cap)
    open(os.path.join(cap, "INDICE.md"), "w").write("# 🎓 Curso JavaScript\n")
    clases = [clase(os.path.join(cap, n), corto={"preguntas": PREG, "idea": "Idea", "mapa": [{"inicio": "0:02", "tema": "T"}]},
                    largo={"conceptos": CONC}, yt="tmRa0_EvMoc") for n in NOMBRES]
    suelta = clase(os.path.join(base, "Capturas de YouTube", "Node (Backend)"))
    with open(os.devnull, "w") as nulo:
        subprocess.run([sys.executable, os.path.join(AQUI, "panel-cursos.py"), "--base", base], stdout=nulo, check=True)
    return base, cap, clases, suelta


def panel(base):
    return open(os.path.join(base, "Mis cursos.md"), encoding="utf-8").read()


def linea_de(md, nombre):
    return next(l for l in md.splitlines() if l.startswith("- [") and nombre.replace("[", "(").replace("]", ")") in l)


def cli(base, *args):
    env = dict(os.environ, ESTUDIAR_BASE=base)
    r = subprocess.run([sys.executable, os.path.join(AQUI, "estudiar.py"), *args], env=env,
                       capture_output=True, text=True, timeout=60)
    return r.returncode, r.stdout + r.stderr


# 1) cursos, próxima clase pendiente, clase a mostrar y curso por defecto
base, cap, C, suelta = boveda()
lista = es.cursos(base)
js = next(c for c in lista if c["nombre"] == "Curso JavaScript")
assert [c["nombre"] for c in lista] == ["Curso JavaScript", "Node (Backend)"] and js["clases"] == C
assert es.elegir_curso(lista, {}) is js                       # sin estado: el de más clases
assert es.elegir_curso(lista, {"curso": suelta})["nombre"] == "Node (Backend)"
m = es.leer_marcas(base)
assert es.proxima(js, m, base) == C[0]
es.marcar(C[0], "hecha", base); es.marcar(C[2], "sabida", base)
m = es.leer_marcas(base)
assert es.proxima(js, m, base) == C[1]                        # primera EN ORDEN no hecha ni sabida
assert es.clase_a_mostrar(js, {"clase": C[3]}, m, base) == C[3]  # la actual sigue pendiente → esa
assert es.clase_a_mostrar(js, {"clase": C[2]}, m, base) == C[1]  # la actual ya está sabida → la próxima
assert es.numero(C[2], js) == (3, 4)
ok += 1

# 2) estados reflejados en Mis cursos.md: [x], [s] + "⏭️ ya la sabía", progreso con sabidas
md = panel(base)
assert linea_de(md, NOMBRES[0]).startswith("- [x] ") and "ya la sabía" not in linea_de(md, NOMBRES[0])
assert linea_de(md, NOMBRES[2]).startswith("- [s] 003 - ") and " · ⏭️ ya la sabía · " in linea_de(md, NOMBRES[2])
assert "**Progreso:** 2/4 clases completadas · ✅ 1 estudiada · ⏭️ 1 ya sabida `" in md, md
assert "✅ 2/5 completadas (1 estudiadas · ⏭️ 1 ya sabidas)" in md
p = es.progreso(js, m, base)
assert (p["hecha"], p["sabida"], p["pendiente"], p["total"]) == (1, 1, 2, 4)
assert es.texto_progreso(p) == "2/4 · ✅ 1 estudiada · ⏭️ 1 ya sabida"
es.marcar(C[2], "pendiente", base)
assert linea_de(panel(base), NOMBRES[2]).startswith("- [ ] ") and "ya la sabía" not in linea_de(panel(base), NOMBRES[2])
assert "1/4 clases estudiadas" in panel(base)                 # sin sabidas: el formato de siempre
ok += 1

# 3) convivencia con lo que el usuario tilda a mano en Obsidian (y con clases nuevas)
es.marcar(C[2], "sabida", base)
md = panel(base)
md = md.replace(linea_de(md, NOMBRES[1]), linea_de(md, NOMBRES[1]).replace("- [ ] ", "- [X] ", 1))  # tilde a mano
md = md.replace(linea_de(md, NOMBRES[2]), linea_de(md, NOMBRES[2]).replace("- [s] ", "- [ ] ", 1))  # destilda la sabida
open(os.path.join(base, "Mis cursos.md"), "w", encoding="utf-8").write(md)
m = es.leer_marcas(base)
assert [es.estado_clase(c, m, base) for c in C] == ["hecha", "hecha", "pendiente", "pendiente"]
es.marcar(C[3], "sabida", base)                               # estudiar.py marca otra: lo manual queda
nueva = clase(os.path.join(cap, "000 - Nueva - #jonmircha"))  # llega una clase nueva (antes que las demás)
subprocess.run([sys.executable, os.path.join(AQUI, "panel-cursos.py"), "--base", base], capture_output=True, check=True)
md = panel(base)
assert linea_de(md, NOMBRES[1]).startswith("- [X] ") and linea_de(md, NOMBRES[3]).startswith("- [s] ")
assert linea_de(md, NOMBRES[2]).startswith("- [ ] ") and linea_de(md, "000 - Nueva").startswith("- [ ] ")
assert "3/5 clases completadas · ✅ 2 estudiadas · ⏭️ 1 ya sabida" in md
js = next(c for c in es.cursos(base) if c["nombre"] == "Curso JavaScript")
assert es.proxima(js, es.leer_marcas(base), base) == nueva
# panel-cursos.py --marcar (CLI) y estado desconocido
r = subprocess.run([sys.executable, os.path.join(AQUI, "panel-cursos.py"), "--base", base, "--marcar", nueva, "hecha"], capture_output=True)
assert r.returncode == 0 and linea_de(panel(base), "000 - Nueva").startswith("- [x] ")
r = subprocess.run([sys.executable, os.path.join(AQUI, "panel-cursos.py"), "--base", base, "--marcar", nueva, "cualquiera"], capture_output=True)
assert r.returncode == 2 and linea_de(panel(base), "000 - Nueva").startswith("- [x] ")
import shutil; shutil.rmtree(nueva)
ok += 1


# 4) dos procesos marcando a la vez no se pisan (candado en panel-cursos)
def _marcar_varias(base, clases, estado):
    for c in clases:
        es.marcar(c, estado, base)


base4, cap4, _, _ = boveda()
muchas = [clase(os.path.join(cap4, f"{i:03d} - Extra {i}")) for i in range(10, 30)]
subprocess.run([sys.executable, os.path.join(AQUI, "panel-cursos.py"), "--base", base4], capture_output=True, check=True)
ctx = multiprocessing.get_context("fork")
ps = [ctx.Process(target=_marcar_varias, args=(base4, muchas[i::2], ("hecha", "sabida")[i])) for i in range(2)]
[p.start() for p in ps]; [p.join() for p in ps]
m4 = es.leer_marcas(base4)
assert [es.estado_clase(c, m4, base4) for c in muchas] == ["hecha", "sabida"] * 10, "se perdió una marca"
ok += 1

# 5) pre-test: 3 preguntas repartidas; si faltan, conceptos "¿Qué es X?" (los más largos); sin nada, []
d = clase(os.path.join(TMP, "pre", "a"), corto={"preguntas": PREG}, largo={"conceptos": CONC})
assert es.preguntas_pretest(d) == [("¿P0?", "R0."), ("¿P2?", "R2."), ("¿P4?", "R4.")]
d = clase(os.path.join(TMP, "pre", "b"), corto={"preguntas": PREG[:1] + [{"pregunta": "¿Vacía?", "respuesta": ""}]},
          largo={"conceptos": CONC})
assert es.preguntas_pretest(d) == [("¿P0?", "R0."), ("¿Qué es **Hoisting**?", CONC[1]["definicion"]),
                                   ("¿Qué es **Scope**?", CONC[2]["definicion"])]
d = clase(os.path.join(TMP, "pre", "c"), largo={"conceptos": CONC})           # sin .resumen-ia.json
assert [p for p, _ in es.preguntas_pretest(d)] == ["¿Qué es **Hoisting**?", "¿Qué es **Scope**?", "¿Qué es **Bloque**?"]
d = clase(os.path.join(TMP, "pre", "d"))                                      # sin ningún JSON
assert es.preguntas_pretest(d) == []
open(os.path.join(d, ".resumen-ia.json"), "w").write("{roto")                 # JSON roto: no revienta
assert es.preguntas_pretest(d) == [] and es.info_clase(d)["idea"] == ""
# más preguntas en clases largas: n según la duración (.minutos.tsv), repartidas por toda la clase
largas = [{"pregunta": f"¿Q{i}?", "respuesta": f"R{i}."} for i in range(30)]
d = clase(os.path.join(TMP, "pre", "e"), corto={"preguntas": largas})
open(os.path.join(d, ".minutos.tsv"), "w").write("0001.webp\t00-00-05\n0002.webp\t01-30-00\n")
assert es.duracion_clase(d) == 5400 and es.n_pretest(5400) == 9 and es.n_pretest(120) == 3 and es.n_pretest(99999) == 10
got = es.preguntas_pretest(d)
assert len(got) == 9 and got[0][0] == "¿Q0?" and got[-1][0] == "¿Q29?", got
assert len(es.preguntas_pretest(d, n=3)) == 3 and es.duracion_clase(os.path.join(TMP, "no-existe")) == 0
assert es.md_pango("¿Qué es **x** y `a<b>`?") == "¿Qué es <b>x</b> y <tt>a&lt;b&gt;</tt>?"
ok += 1

# 6) títulos cortos, número de clase, video (local / YouTube)
base6, cap6, C6, suelta6 = boveda()
js6 = next(c for c in es.cursos(base6) if c["nombre"] == "Curso JavaScript")
assert [es.titulo_corto(c, js6) for c in C6] == ["1. Introducción", "AprendeJavascript.org",
                                                  "3. Variables- var 🥊VS🥊 let", "11. Arreglos [Arrays]"]
node = next(c for c in es.cursos(base6) if c["nombre"] == "Node (Backend)")
assert es.titulo_corto(suelta6, node) == "Node (Backend)"
assert es.youtube_url(C6[0]) == "https://www.youtube.com/watch?v=tmRa0_EvMoc" and es.youtube_url(suelta6) is None
curso_local = os.path.join(TMP, "Karpathy")
cl = clase(os.path.join(curso_local, "capturas", "001 - Intro： micrograd"))
for v in ("001 - Intro： micrograd.mp4", "001 - Intro： micrograd.es.mp4", "002 - Otra.es.mp4", "001 - Intro： micrograd.es.mp4.part"):
    open(os.path.join(curso_local, v), "w").close()
assert es.video_local(cl) == os.path.join(curso_local, "001 - Intro： micrograd.es.mp4")  # prefiere el doblado
assert es.video_local(C6[0]) is None
ok += 1

# 7) CLI --estado / --terminar (sin ventana); "clase actual" = la guardada en el estado
base7, cap7, C7, _ = boveda()
if os.path.exists(os.environ["ESTUDIAR_ESTADO"]):
    os.remove(os.environ["ESTUDIAR_ESTADO"])
cod, out = cli(base7, "--estado")
assert cod == 0 and "📚 Curso JavaScript" in out and "📍 Clase 1/4: 1. Introducción (pendiente)" in out, out
assert "📊 0/4 · ✅ 0 estudiadas · ⏭️ 0 ya sabidas" in out
cod, out = cli(base7, "--terminar")
assert cod == 0 and "✅ Terminaste: 1. Introducción" in out and "Sigue → Clase 2/4: AprendeJavascript.org" in out, out
assert linea_de(panel(base7), NOMBRES[0]).startswith("- [x] ")
est = json.load(open(os.environ["ESTUDIAR_ESTADO"]))
assert est["clase"] == C7[1] and est["fase"] == "pretest"
es.marcar(C7[1], "sabida", base7)                              # la actual se marcó en otro lado (Obsidian)
cod, out = cli(base7, "--terminar")                           # no la convierte en hecha: solo avanza
assert cod == 0 and "ya estaba sabida" in out and "Clase 3/4" in out, out
assert linea_de(panel(base7), NOMBRES[1]).startswith("- [s] ")
for _ in range(2):
    cod, out = cli(base7, "--terminar")
assert "🎉 ¡Curso completo! Curso JavaScript" in out and json.load(open(os.environ["ESTUDIAR_ESTADO"]))["clase"] is None, out
cod, out = cli(base7, "--estado")
assert "🎉 Curso completo" in out and "4/4 · ✅ 3 estudiadas · ⏭️ 1 ya sabida" in out, out
# --tests sin practica.py: avisa y sale con 1 (no revienta)
es.marcar(C7[3], "pendiente", base7)
json.dump({"clase": C7[3]}, open(os.environ["ESTUDIAR_ESTADO"], "w"))
cod, out = cli(base7, "--tests")
assert cod == 1 and "practica.py todavía no está instalado" in out, out
# bóveda sin cursos
cod, out = cli(tempfile.mkdtemp(dir=TMP), "--estado")
assert cod == 1 and "No hay cursos" in out
ok += 1

# 8) tarjetas para repasar: vencidas (<= hoy, en cualquier clase) + nuevas (solo de clases vistas)
base8, cap8, C8, _ = boveda()
TARJ = """# 🃏 Tarjetas

#flashcards/curso

¿Vencida?
?
Sí
<!--SR:!2026-09-01,4,270-->

¿Hoy?
?
Sí <!--SR:!fsrs,2026-09-29,3,1,5.2,4.1,0,0,2026-09-20-->

¿Futura?
?
No
<!--SR:!2026-12-01,40,270-->

¿Nueva?
?
Sin progreso

## ✍️ Mis tarjetas

Mía::respuesta
"""
for c in C8[:2]:
    open(os.path.join(c, "tarjetas.md"), "w").write(TARJ)
js8 = next(c for c in es.cursos(base8) if c["nombre"] == "Curso JavaScript")
t = es.tarjetas_pendientes(js8, es.leer_marcas(base8), base8, hoy="2026-09-29")
assert (t["vencidas"], t["nuevas"]) == (4, 0), t              # 2 por archivo; clases no vistas: sin nuevas
es.marcar(C8[1], "sabida", base8)
t = es.tarjetas_pendientes(js8, es.leer_marcas(base8), base8, hoy="2026-09-29")
assert (t["vencidas"], t["nuevas"]) == (4, 2) and t["archivo"] == os.path.join(C8[1], "tarjetas.md"), t
t = es.tarjetas_pendientes(js8, es.leer_marcas(base8), base8, hoy="2026-08-01")
assert t["vencidas"] == 0
ok += 1

# 9) resultado de los tests de práctica (formato del docstring de practica.py; tolerante)
d = clase(os.path.join(TMP, "res", "a"))
assert es.resultado_practica(d) is None
os.makedirs(os.path.join(d, "practica"))
json.dump({"ok": 1, "total": 2, "todos_ok": False, "ejercicios": [
    {"id": "ej01", "nombre": "suma-pares", "titulo": "Sumar los pares", "ok": True, "pasan": 4, "tests": 4, "error": ""},
    {"id": "ej02", "nombre": "invertir", "titulo": "Invertir", "ok": False, "pasan": 1, "tests": 3,
     "error": "invierte vacío: AssertionError: esperado [], obtenido undefined"}]},
    open(os.path.join(d, "practica", ".resultado.json"), "w"))
assert es.resultado_practica(d) == [("ej01 · Sumar los pares  (4/4 tests)", True, ""),
                                    ("ej02 · Invertir  (1/3 tests)", False, "invierte vacío: AssertionError: esperado [], obtenido undefined")]
json.dump({"a": True, "b": False}, open(os.path.join(d, "practica", ".resultado.json"), "w"))
assert es.resultado_practica(d) == [("a", True, ""), ("b", False, "")]
open(os.path.join(d, "practica", ".resultado.json"), "w").write("[roto")
assert es.resultado_practica(d) is None
ok += 1

# 10) estado.json: escritura atómica y mezcla de claves
os.remove(os.environ["ESTUDIAR_ESTADO"])
es.guardar_estado(curso="A", clase="B")
e = es.guardar_estado(fase="estudiar")
assert e == {"curso": "A", "clase": "B", "fase": "estudiar"} and es.cargar_estado() == e
assert not [f for f in os.listdir(os.path.dirname(es.ESTADO)) if f.endswith(".tmp")]
ok += 1

shutil.rmtree(TMP, ignore_errors=True)
print(f"{ok}/10 pruebas OK")
