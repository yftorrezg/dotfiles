#!/usr/bin/env python3
"""Pruebas de resumen-corto.py (sin llamar a Claude)."""
import importlib.util, json, os, sys, tempfile
AQUI = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("rc", os.path.join(AQUI, "resumen-corto.py"))
rc = importlib.util.module_from_spec(spec); spec.loader.exec_module(rc)
ok = 0

# 1) el | dentro de la chuleta no rompe la tabla; sin código no sale la sección
md = rc.armar("Clase", "1:00:00", {"idea": "X", "esencial": ["a"], "chuleta": [{"quiero": "o lógico", "como": "`a || b`"}],
                                   "codigo": [{"titulo": "t", "codigo": "  "}], "preguntas": [{"pregunta": "p?", "respuesta": "r"}]})
assert "`a \\|\\| b`" in md and "Código mínimo" not in md and "> [!question]- 1. p?" in md and "(apuntes.md)" in md; ok += 1

# 2) sin .apuntes-ia.json no hace nada y no crea resumen.md
with tempfile.TemporaryDirectory() as d:
    assert rc.resumir(d) == 1 and not os.path.exists(os.path.join(d, "resumen.md")); ok += 1

# 3) resumen.md existente no se pisa sin --forzar (ni se llama a Claude)
with tempfile.TemporaryDirectory() as d:
    open(os.path.join(d, "resumen.md"), "w").write("mío")
    rc.pedir_a_claude = lambda *a: (_ for _ in ()).throw(AssertionError("no debía llamar a Claude"))
    assert rc.resumir(d) == 0 and open(os.path.join(d, "resumen.md")).read() == "mío"; ok += 1

# 4) título y duración salen de apuntes.md, que queda intacto
with tempfile.TemporaryDirectory() as d:
    ap = "# 📓 Curso de Node\n\n> ⏱️ **Duración:** 4:42:35 · 📸 ...\n"
    open(os.path.join(d, "apuntes.md"), "w").write(ap)
    json.dump({"secciones": []}, open(os.path.join(d, ".apuntes-ia.json"), "w"))
    visto = {}
    rc.pedir_a_claude = lambda t, du, datos: visto.update(t=t, du=du) or {"esencial": ["e"]}
    assert rc.resumir(d) == 0 and visto == {"t": "Curso de Node", "du": "4:42:35"}
    assert open(os.path.join(d, "apuntes.md")).read() == ap and "Curso de Node" in open(os.path.join(d, "resumen.md")).read(); ok += 1

print(f"{ok}/4 pruebas OK")
