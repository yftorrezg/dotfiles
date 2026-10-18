#!/usr/bin/env python3
"""chuletas_md.py — lee las chuletas (~/.config/hypr/chuletas/*.md) en bloques que dibuja chuletas.py.

Formato completo en ~/.config/hypr/chuletas/FORMATO.md.
  python3 chuletas_md.py validar <archivo.md> [...]   revisa una hoja y muestra un resumen
"""
import re
import sys
from pathlib import Path

CARPETA = Path.home() / ".config/hypr/chuletas"
NOTAS = {"💡": "consejo", "⚠️": "cuidado", "⚠": "cuidado", "🇬🇧": "ingles", "📌": "nota"}
ENTRADA = re.compile(r"^- `(.+)` :: (.+)$")
FILA = re.compile(r"^\|(.+)\|\s*$")
SEPARADOR = re.compile(r"^\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$")


def celdas(linea):
    """Parte una fila de tabla por | sin romper el `código` que tenga | dentro."""
    partes, actual, en_codigo = [], "", False
    for ch in linea.strip().strip("|"):
        if ch == "`":
            en_codigo = not en_codigo
        if ch == "|" and not en_codigo:
            partes.append(actual.strip())
            actual = ""
        else:
            actual += ch
    partes.append(actual.strip())
    return partes


def leer(archivo):
    """→ {"titulo", "subtitulo", "archivo", "secciones": [{"titulo", "bloques": [...]}], "errores": [...]}
    Bloques: ("p", texto) ("entrada", codigo, explicacion) ("h3", texto) ("codigo", lenguaje, texto)
             ("nota", tipo, texto) ("tabla", filas)"""
    hoja = {"titulo": Path(archivo).stem, "subtitulo": "", "archivo": Path(archivo), "secciones": [], "errores": []}
    seccion = {"titulo": None, "bloques": []}
    hoja["secciones"].append(seccion)
    parrafo, tabla, codigo = [], None, None

    def cerrar_parrafo():
        if parrafo:
            seccion["bloques"].append(("p", " ".join(parrafo)))
            parrafo.clear()

    def cerrar_tabla():
        nonlocal tabla
        if tabla:
            anchos = {len(f) for f in tabla}
            if len(anchos) > 1:
                hoja["errores"].append(f"tabla con filas de distinto número de columnas: {tabla[0]}")
            seccion["bloques"].append(("tabla", tabla))
        tabla = None

    for n, linea in enumerate(Path(archivo).read_text(encoding="utf-8").splitlines(), 1):
        if codigo is not None:  # dentro de ```
            if linea.strip() == "```":
                seccion["bloques"].append(("codigo", codigo[0], "\n".join(codigo[1]).rstrip("\n")))
                codigo = None
            else:
                codigo[1].append(linea)
            continue
        s = linea.strip()
        if FILA.match(s):
            cerrar_parrafo()
            if SEPARADOR.match(s):
                continue
            tabla = (tabla or []) + [celdas(s)]
            continue
        cerrar_tabla()
        if s.startswith("```"):
            cerrar_parrafo()
            codigo = (s[3:].strip() or "text", [], n)
        elif not s:
            cerrar_parrafo()
        elif s.startswith("### "):
            cerrar_parrafo()
            seccion["bloques"].append(("h3", s[4:].strip()))
        elif s.startswith("## "):
            cerrar_parrafo()
            seccion = {"titulo": s[3:].strip(), "bloques": []}
            hoja["secciones"].append(seccion)
        elif s.startswith("# "):
            hoja["titulo"] = s[2:].strip()
        elif s.startswith("> "):
            hoja["subtitulo"] = s[2:].strip()
        elif m := ENTRADA.match(s):
            cerrar_parrafo()
            seccion["bloques"].append(("entrada", m.group(1), m.group(2).strip()))
        elif nota := next((t for e, t in NOTAS.items() if s.startswith(e)), None):
            cerrar_parrafo()
            seccion["bloques"].append(("nota", nota, s))
        else:
            if s.startswith("- ") and " :: " in s:
                hoja["errores"].append(f"línea {n}: parece entrada rápida pero falta `código`: {s[:60]}")
            parrafo.append(s)
    cerrar_parrafo()
    cerrar_tabla()
    if codigo is not None:
        hoja["errores"].append(f"bloque de código abierto en la línea {codigo[2]} sin cerrar con ```")
    if not hoja["secciones"][0]["bloques"]:
        hoja["secciones"].pop(0)
    return hoja


def hojas():
    return [leer(a) for a in sorted(CARPETA.glob("*.md")) if not a.name.startswith("FORMATO")]


def texto_de(bloque):
    """Texto plano de un bloque (para la búsqueda)."""
    if bloque[0] == "tabla":
        return " ".join(" ".join(f) for f in bloque[1])
    return " ".join(str(x) for x in bloque[1:])


if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] != "validar":
        print(__doc__)
        sys.exit(1)
    mal = False
    for a in sys.argv[2:]:
        h = leer(a)
        tipos = {}
        for sec in h["secciones"]:
            for b in sec["bloques"]:
                tipos[b[0]] = tipos.get(b[0], 0) + 1
        sin_emoji = [s["titulo"] for s in h["secciones"] if s["titulo"] and s["titulo"][0].isascii()]
        print(f"{Path(a).name}: «{h['titulo']}» · {len(h['secciones'])} secciones · {tipos}")
        if not h["subtitulo"]:
            h["errores"].append("falta el subtítulo (> ...)")
        if sin_emoji:
            h["errores"].append(f"secciones sin emoji al inicio: {sin_emoji[:5]}")
        for e in h["errores"]:
            print("  ERROR:", e)
            mal = True
    sys.exit(1 if mal else 0)
