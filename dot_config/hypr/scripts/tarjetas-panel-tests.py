#!/usr/bin/env python3
"""Pruebas de tarjetas.py y panel-cursos.py (sin red ni Claude). Usa el parser del plugin
Spaced Repetition portado en tarjetas.parsear() para comprobar el formato."""
import importlib.util, json, os, re, sys, tempfile, time
AQUI = os.path.dirname(os.path.abspath(__file__))


def cargar(nombre, archivo):
    spec = importlib.util.spec_from_file_location(nombre, os.path.join(AQUI, archivo))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


ta = cargar("ta", "tarjetas.py")
pc = cargar("pc", "panel-cursos.py")
ok = 0


def clase(d, corto=None, largo=None, titulo=None):
    os.makedirs(d, exist_ok=True)
    if titulo:
        open(os.path.join(d, "apuntes.md"), "w").write(f"# 📓 {titulo}\n\n> ⏱️ **Duración:** 1:02:03 · x\n")
    if corto is not None:
        json.dump(corto, open(os.path.join(d, ".resumen-ia.json"), "w"), ensure_ascii=False)
    if largo is not None:
        json.dump(largo, open(os.path.join(d, ".apuntes-ia.json"), "w"), ensure_ascii=False)
    return d


def multis(texto):
    """[(pregunta, respuesta_sin_SR)] de las tarjetas que ve el plugin; falla si hay de otro tipo."""
    out = []
    for tipo, t, _, _ in ta.parsear(texto):
        assert tipo == "multi", (tipo, t)
        L = t.split("\n")
        k = L.index("?")
        out.append(("\n".join(L[:k]), "\n".join(l for l in L[k + 1:] if not l.startswith("<!--SR:"))))
    return out


def ver(md):
    """Texto como se ve renderizado (sin escapes)."""
    return md.replace("\u200b", "").replace("\\", "")


CORTO = {"preguntas": [{"pregunta": "¿Por qué X?", "respuesta": "Porque Y."},
                       {"pregunta": "¿Por qué X?", "respuesta": "Duplicada."},
                       {"pregunta": "¿Vacía?", "respuesta": ""}],
         "chuleta": [{"quiero": "Crear un array", "como": "`np.array([1, 2])`"},
                     {"quiero": "API de fetch", "como": "`fetch(url)`"}]}
LARGO = {"conceptos": [{"termino": "Tensor", "definicion": "Arreglo de n dimensiones con dtype y device."},
                       {"termino": "Corto", "definicion": "muy corto"}]}

# 1) formato: solo las tarjetas esperadas, multi-línea, sin duplicados/vacías/triviales
with tempfile.TemporaryDirectory() as d:
    c = clase(os.path.join(d, "Curso X"), CORTO, LARGO, "Curso X")
    assert ta.generar(c) == 4
    md = open(os.path.join(c, "tarjetas.md")).read()
    cards = multis(md)
    assert [p for p, _ in cards] == ["¿Por qué X?", "¿Qué es **Tensor**?", "¿Cómo crear un array?", "¿Cómo API de fetch?"], cards
    assert cards[0][1] == "Porque Y." and cards[2][1] == "`np.array([1, 2])`"
    assert "\n#flashcards/curso-x\n" in md and "## ✍️ Mis tarjetas" in md
    ok += 1

# 2) progreso <!--SR: conservado al regenerar (aunque cambie el orden y se agreguen/quiten tarjetas);
#    "Mis tarjetas" intacta; sin --forzar y sin cambios en los JSON no se toca
with tempfile.TemporaryDirectory() as d:
    c = clase(os.path.join(d, "Curso X"), CORTO, LARGO, "Curso X")
    ta.generar(c)
    ruta = os.path.join(c, "tarjetas.md")
    md = open(ruta).read()
    sr1, sr2 = "<!--SR:!2026-10-05,4,270-->", "<!--SR:!fsrs,2026-10-09,3,1,5.2,4.1,0,0,2026-09-28-->"
    md = md.replace("Porque Y.\n", "Porque Y.\n" + sr1 + "\n")
    md = md.replace("`np.array([1, 2])`\n", "`np.array([1, 2])` " + sr2 + "\n")  # ajuste "misma línea"
    md = md.replace("nunca se regenera.*", "nunca se regenera.*\n\nMi pregunta\n?\nMi respuesta\n<!--SR:!2026-10-01,1,230-->")
    open(ruta, "w").write(md)
    antes = os.path.getmtime(ruta)
    assert ta.generar(c) == 0 and open(ruta).read() == md  # sin --forzar: no se pisa
    time.sleep(0.01)
    nuevo = dict(CORTO, preguntas=[{"pregunta": "¿Nueva?", "respuesta": "Sí, nueva."}] + CORTO["preguntas"][:1],
                 chuleta=CORTO["chuleta"][:1])
    clase(c, nuevo)  # JSON más nuevo que tarjetas.md → se regenera solo
    os.utime(ruta, (antes - 10, antes - 10))
    assert ta.generar(c) == 4
    md2 = open(ruta).read()
    assert "Porque Y.\n" + sr1 + "\n" in md2 and "`np.array([1, 2])`\n" + sr2 + "\n" in md2
    assert md2.count("<!--SR:") == 3 and "Mi pregunta\n?\nMi respuesta\n<!--SR:!2026-10-01,1,230-->" in md2
    assert len(multis(md2)) == 5 and "API de fetch" not in md2
    ok += 1

# 3) caracteres problemáticos: ::, ==, ?, #, <!--, |, código con líneas en blanco, backticks desparejos
RARO = {"preguntas": [
    {"pregunta": "¿Qué hace x::y en C++?", "respuesta": "Resuelve el ámbito: std::vector. Y `a::b` en código."},
    {"pregunta": "¿Diferencia entre `==` y `===`?", "respuesta": "== compara con coerción, ==x== no es hueco."},
    {"pregunta": "¿Rebanadas?", "respuesta": "`x[::2]` y `x[::-1]` | columna | otra"},
    {"pregunta": "¿Y esto?", "respuesta": "Mirá:\n?\n??\nfin"},
    {"pregunta": "¿Tags?", "respuesta": "#include <stdio.h> y un #tag, C# y <!-- comentario"},
    {"pregunta": "¿Código?", "respuesta": "Así:\n\n```python\ndef f():\n\n    return {1: 2}\n```\n\nY listo."},
    {"pregunta": "¿Backtick suelto?", "respuesta": "`a::b` y un ` suelto, y c::d"},
    {"pregunta": "¿Sin cerrar?", "respuesta": "```js\nconst a = 1"},
    {"pregunta": "¿Id de bloque?", "respuesta": "termina con ^abc-1"}]}
with tempfile.TemporaryDirectory() as d:
    c = clase(os.path.join(d, "Raro"), RARO, None)
    assert ta.generar(c) == 9
    md = open(os.path.join(c, "tarjetas.md")).read()
    cards = multis(md)
    assert len(cards) == 9, cards
    r = {p: ver(a) for p, a in cards}
    assert "std::vector" in r["¿Qué hace x:\\:y en C++?"] and "`a::b`" in md
    assert "=\\= compara" in md and "`x[::2]`" in md and "| columna |" in md
    assert r["¿Y esto?"] == "Mirá:\n?\n??\nfin" and "\\#include" in md and "\\#tag" in md and "C# y" in md and "\\<!--" in md and "\\<stdio.h>" in md
    assert "def f():\n\n    return {1: 2}\n```\nY listo." in md  # blanco dentro del ``` sí; afuera no
    assert "```js\nconst a = 1\n```" in md and " \\^abc-1" in md
    assert ":\u200b:" in md  # backtick suelto: el :: de afuera se corta con espacio de ancho cero
    assert not re.search(r"^#(?![ #]|flashcards/)", md, re.M), "ningún # al inicio salvo títulos y el tag"
    ok += 1

# 4) tags normalizados (sin espacios ni símbolos; mazo curso/clase dentro de capturas/)
assert ta.slug("Neural Networks： Zero to Hero") == "neural-networks-zero-to-hero"
assert ta.slug("Nodejs Curso Práctico (Javascript)") == "nodejs-curso-practico-javascript"
assert ta.slug("007 - Let's build GPT： from scratch, in code, spelled out.") == "007-lets-build-gpt-from-scratch-in-code-spelled-out"
assert ta.slug("2024") == "c2024" and ta.slug("¿¡!?") == "clase" and len(ta.slug("a" * 30 + " " + "b" * 40)) <= 60
with tempfile.TemporaryDirectory() as d:
    cap = os.path.join(d, "Mi Curso ｜ 2", "capturas")
    os.makedirs(cap)
    open(os.path.join(cap, "INDICE.md"), "w").write("# 🎓 Mi Curso ｜ Nivel #2\n")
    c = clase(os.path.join(cap, "001 - Intro： ¿qué es?"), CORTO, None, "001 - Intro： ¿qué es?")
    ta.generar(c)
    md = open(os.path.join(c, "tarjetas.md")).read()
    tag = next(l for l in md.splitlines() if l.startswith("#flashcards"))
    assert tag == "#flashcards/mi-curso-nivel-2/001-intro-que-es" and re.fullmatch(r"#[a-z0-9/-]+", tag)
    anki = open(os.path.join(c, "tarjetas-anki.txt")).read().splitlines()
    assert anki[:4] == ["#separator:tab", "#html:true", "#notetype:Basic", "#deck:Cursos::Mi Curso ｜ Nivel #2::001 - Intro： ¿qué es?"]
    filas = [l.split("\t") for l in anki if not l.startswith("#")]
    assert len(filas) == 3 and all(len(f) == 4 and '"' not in "".join(f) for f in filas)
    assert filas[1][2] == "<code>np.array([1, 2])</code>" and filas[0][3] == "flashcards::mi-curso-nivel-2::001-intro-que-es"
    ok += 1

# 5) sin JSON no hace nada (código 0, sin archivos); con uno solo usa ese
with tempfile.TemporaryDirectory() as d:
    assert ta.generar(d) == 0 and not os.listdir(d)
    c = clase(os.path.join(d, "Solo apuntes"), None, LARGO)
    assert ta.generar(c) == 1 and len(multis(open(os.path.join(c, "tarjetas.md")).read())) == 1
    ok += 1

# 6) Anki: html escapado, bloque de código, guid estable
assert ta.a_html("a <b> & \"c\"\n```py\nx < 1\n```") == "a &lt;b&gt; &amp; &quot;c&quot;<pre><code>x &lt; 1</code></pre>"
g1 = ta.armar_anki("M", "t", [("s", "¿P?", "R")]).splitlines()[-1].split("\t")[0]
g2 = ta.armar_anki("M", "t", [("s", "¿P?", "otra R")]).splitlines()[-1].split("\t")[0]
assert g1 == g2 and g1.isalnum(); ok += 1

# 7) las tarjetas reales (si existen) se parsean completas y sin tarjetas fantasma
reales = 0
for r, _, fs in os.walk(os.path.expanduser("~/Vídeos")):
    if "tarjetas.md" in fs and ".resumen-ia.json" in fs:
        md = open(os.path.join(r, "tarjetas.md"), encoding="utf-8").read()
        antes_mias = md.split(ta.MARCA_MIAS)[0]
        esperadas = len(ta.juntar(ta.leer_json(os.path.join(r, ".resumen-ia.json")),
                                  ta.leer_json(os.path.join(r, ".apuntes-ia.json"))))
        assert len(multis(antes_mias)) == esperadas, r
        reales += 1
ok += 1


# ------------------------------------------------------------------ panel ----
def curso_indexado(base, carpeta, nombre, clases):
    cap = os.path.join(base, carpeta, "capturas")
    os.makedirs(cap, exist_ok=True)
    open(os.path.join(cap, "INDICE.md"), "w").write(f"# 🎓 {nombre}\n")
    for c in clases:
        clase(os.path.join(cap, c), titulo=c)
        open(os.path.join(cap, c, "resumen.md"), "w").write("x")
    return cap


RAROS = ["001 - Intro： building micrograd", "002 - State of GPT ｜ BRK", "003 - Let's go (124M) & more, spelled out."]
with tempfile.TemporaryDirectory() as base:
    curso_indexado(base, "Descargas/Neural Networks： Zero to Hero", "Neural Networks： Zero to Hero", RAROS)
    clase(os.path.join(base, "Capturas de YouTube", "Node (Backend)"), titulo="Node (Backend)")
    salida = pc.generar(base)
    md = open(salida).read()
    # 8) links relativos a la bóveda, con <…>, y todos apuntan a archivos que existen
    links = re.findall(r"\]\(<([^>]+)>\)", md)
    assert len(links) == 3 * 2 + 1 + 1 and all(os.path.exists(os.path.join(base, l)) for l in links), links
    assert md.count("- [ ] ") == 4 and "0/3 clases estudiadas" in md and "0/1 clase estudiada" in md
    assert "⏱️ 3:06:09" in md and not [f for f in os.listdir(base) if f.endswith(".tmp")]
    ok += 1
    # 9) tildo 2 clases (una con X) + escribo notas; aparece un curso nuevo que va primero y
    #    una clase nueva que va ANTES de las tildadas → las casillas siguen en su clase
    md = md.replace("- [ ] 002 - State", "- [x] 002 - State").replace("- [ ] Node (Backend)", "- [X] Node (Backend)")
    md = md.replace("esta sección no se regenera.*", "esta sección no se regenera.*\n\n- [x] mi tarea propia\nNota mía con [[link]].")
    open(salida, "w").write(md)
    curso_indexado(base, "Descargas/Neural Networks： Zero to Hero", "Neural Networks： Zero to Hero", ["000 - Nueva"])
    curso_indexado(base, "Capturas de YouTube/AAA playlist", "AAA playlist", ["001 - Uno", "002 - Dos"])
    pc.generar(base)
    md2 = open(salida).read()
    assert md2.index("## AAA playlist") < md2.index("## Neural")
    assert "- [ ] 000 - Nueva" in md2 and "- [x] 002 - State of GPT ｜ BRK" in md2 and "- [ ] 003 - Let's" in md2
    assert "- [X] Node (Backend)" in md2 and "1/4 clases estudiadas" in md2 and "1/1 clase estudiada" in md2
    assert "✅ 2/7 estudiadas" in md2 and md2.rstrip().endswith("- [x] mi tarea propia\nNota mía con [[link]].")
    ok += 1
    # 10) sin cambios no reescribe; si se borra una clase tildada, desaparece sin error
    t = os.path.getmtime(salida)
    time.sleep(0.01)
    pc.generar(base)
    assert os.path.getmtime(salida) == t
    import shutil
    shutil.rmtree(os.path.join(base, "Capturas de YouTube", "Node (Backend)"))
    pc.generar(base)
    md3 = open(salida).read()
    assert "Node (Backend)" not in md3 and "✅ 1/6 estudiadas" in md3
    ok += 1

# 11) bóveda vacía o inexistente: no revienta
with tempfile.TemporaryDirectory() as base:
    assert "Todavía no hay cursos" in open(pc.generar(base)).read()
    sys.argv = ["panel-cursos.py", "--base", os.path.join(base, "no-existe")]
    assert pc.main() == 0
    ok += 1

print(f"{ok}/11 pruebas OK ({reales} tarjetas.md reales verificadas con el parser del plugin)")
