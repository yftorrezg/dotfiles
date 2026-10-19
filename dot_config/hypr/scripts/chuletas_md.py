#!/usr/bin/env python3
"""chuletas_md.py — lee las chuletas (~/.config/hypr/chuletas/*.md) en bloques que dibuja chuletas.py.

Formato completo en ~/.config/hypr/chuletas/FORMATO.md.
  python3 chuletas_md.py validar <archivo.md> [...]   revisa una hoja y muestra un resumen
"""
import re
import sys
from pathlib import Path

CARPETA = Path.home() / ".config/hypr/chuletas"
NOTAS = {"💡": "consejo", "⚠️": "cuidado", "⚠": "cuidado", "🇬🇧": "ingles", "📌": "nota",
         "✅": "bien", "❌": "mal", "🧠": "concepto", "🚀": "futuro"}
ENTRADA = re.compile(r"^- `(.+)` :: (.+)$")
FILA = re.compile(r"^\|(.+)\|\s*$")
SEPARADOR = re.compile(r"^\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$")
IMAGEN = re.compile(r"^!\[(.*)\]\((.+)\)$")
VINETA = re.compile(r"^[-*] (.+)$")
NUMERO = re.compile(r"^\d+[.)] (.+)$")
DIBUJOS = ("flujo", "secuencia", "arbol", "capas", "tiempo", "grafica")


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
             ("nota", tipo, texto) ("tabla", filas) ("lista", items, numerada) ("imagen", pie, ruta)
             ("desplegable", titulo, bloques) ("columnas", [bloques, bloques, ...])
    Los dibujos (```flujo, ```grafica…) son bloques "codigo" con ese lenguaje."""
    hoja = {"titulo": Path(archivo).stem, "subtitulo": "", "archivo": Path(archivo), "secciones": [], "errores": []}
    seccion = {"titulo": None, "bloques": []}
    hoja["secciones"].append(seccion)
    parrafo, tabla, codigo, lista = [], None, None, None
    pila = []  # contenedores abiertos (::: desplegable / ::: columnas): [bloque, lista_destino, línea]

    def destino():
        return pila[-1][1] if pila else seccion["bloques"]

    def cerrar_parrafo():
        if parrafo:
            destino().append(("p", " ".join(parrafo)))
            parrafo.clear()

    def cerrar_lista():
        nonlocal lista
        if lista:
            destino().append(("lista", lista[1], lista[0]))
        lista = None

    def cerrar_tabla():
        nonlocal tabla
        if tabla:
            if len({len(f) for f in tabla}) > 1:
                hoja["errores"].append(f"tabla con filas de distinto número de columnas: {tabla[0]}")
            destino().append(("tabla", tabla))
        tabla = None

    def cerrar_todo():
        cerrar_parrafo()
        cerrar_lista()
        cerrar_tabla()

    for n, linea in enumerate(Path(archivo).read_text(encoding="utf-8").splitlines(), 1):
        if codigo is not None:  # dentro de ```
            if linea.strip() == "```":
                destino().append(("codigo", codigo[0], "\n".join(codigo[1]).rstrip("\n")))
                codigo = None
            else:
                codigo[1].append(linea)
            continue
        s = linea.strip()
        if FILA.match(s):
            cerrar_parrafo()
            cerrar_lista()
            if SEPARADOR.match(s):
                continue
            tabla = (tabla or []) + [celdas(s)]
            continue
        cerrar_tabla()
        if s.startswith(":::"):
            cerrar_todo()
            resto = s[3:].strip()
            if resto.startswith("desplegable"):
                bloque = ("desplegable", resto[len("desplegable"):].strip() or "Ver más", [])
                destino().append(bloque)
                pila.append([bloque, bloque[2], n])
            elif resto == "columnas":
                bloque = ("columnas", [[]])
                destino().append(bloque)
                pila.append([bloque, bloque[1][0], n])
            elif resto == "siguiente":
                if pila and pila[-1][0][0] == "columnas":
                    pila[-1][0][1].append([])
                    pila[-1][1] = pila[-1][0][1][-1]
                else:
                    hoja["errores"].append(f"línea {n}: «::: siguiente» fuera de «::: columnas»")
            elif resto == "":
                if pila:
                    pila.pop()
                else:
                    hoja["errores"].append(f"línea {n}: «:::» de cierre sin nada abierto")
            else:
                hoja["errores"].append(f"línea {n}: contenedor desconocido «{s}»")
            continue
        if s.startswith("```"):
            cerrar_todo()
            codigo = (s[3:].strip() or "text", [], n)
        elif not s:
            cerrar_parrafo()
            cerrar_lista()
        elif s.startswith("### "):
            cerrar_todo()
            destino().append(("h3", s[4:].strip()))
        elif s.startswith("## "):
            cerrar_todo()
            if pila:
                hoja["errores"].append(f"línea {n}: sección nueva con un ::: abierto en la línea {pila[-1][2]}")
                pila.clear()
            seccion = {"titulo": s[3:].strip(), "bloques": []}
            hoja["secciones"].append(seccion)
        elif s.startswith("# "):
            hoja["titulo"] = s[2:].strip()
        elif s.startswith("> "):
            hoja["subtitulo"] = s[2:].strip()
        elif m := ENTRADA.match(s):
            cerrar_parrafo()
            cerrar_lista()
            destino().append(("entrada", m.group(1), m.group(2).strip()))
        elif m := IMAGEN.match(s):
            cerrar_todo()
            ruta = Path(archivo).parent / m.group(2).strip()  # relativa a la carpeta de la hoja
            if not ruta.is_file():
                hoja["errores"].append(f"línea {n}: no existe la imagen {m.group(2).strip()}")
            destino().append(("imagen", m.group(1).strip(), str(ruta)))
        elif nota := next((t for e, t in NOTAS.items() if s.startswith(e)), None):
            cerrar_todo()
            destino().append(("nota", nota, s))
        elif (m := VINETA.match(s)) or (m := NUMERO.match(s)):
            cerrar_parrafo()
            numerada = not s.startswith(("-", "*"))
            if " :: " in s and s.startswith("- "):
                hoja["errores"].append(f"línea {n}: parece entrada rápida pero falta `código`: {s[:60]}")
            if lista is None or lista[0] != numerada:
                cerrar_lista()
                lista = (numerada, [])
            lista[1].append(m.group(1).strip())
        elif lista is not None and linea.startswith(("  ", "\t")):
            lista[1][-1] += " " + s  # continuación de la viñeta anterior
        else:
            cerrar_lista()
            parrafo.append(s)
    cerrar_todo()
    if codigo is not None:
        hoja["errores"].append(f"bloque de código abierto en la línea {codigo[2]} sin cerrar con ```")
    for bloque, _d, n in pila:
        hoja["errores"].append(f"«::: {bloque[0]}» de la línea {n} sin cerrar con :::")
    if not hoja["secciones"][0]["bloques"]:
        hoja["secciones"].pop(0)
    return hoja


def hojas():
    return [leer(a) for a in sorted(CARPETA.glob("*.md")) if not a.name.startswith("FORMATO")]


def texto_de(bloque):
    """Texto plano de un bloque (para la búsqueda)."""
    tipo = bloque[0]
    if tipo == "tabla":
        return " ".join(" ".join(f) for f in bloque[1])
    if tipo == "lista":
        return " ".join(bloque[1])
    if tipo == "desplegable":
        return bloque[1] + " " + " ".join(texto_de(b) for b in bloque[2])
    if tipo == "columnas":
        return " ".join(texto_de(b) for col in bloque[1] for b in col)
    return " ".join(str(x) for x in bloque[1:])


def recorrer(bloques):
    """Todos los bloques, también los que están dentro de desplegables y columnas."""
    for b in bloques:
        yield b
        if b[0] == "desplegable":
            yield from recorrer(b[2])
        elif b[0] == "columnas":
            for col in b[1]:
                yield from recorrer(col)


if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] != "validar":
        print(__doc__)
        sys.exit(1)
    sys.path.insert(0, str(Path(__file__).parent))
    import chuletas_dibujo as dib  # noqa: E402
    mal = False
    for a in sys.argv[2:]:
        h = leer(a)
        tipos = {}
        for sec in h["secciones"]:
            for b in recorrer(sec["bloques"]):
                clave = b[1] if b[0] == "codigo" and b[1] in DIBUJOS else b[0]
                tipos[clave] = tipos.get(clave, 0) + 1
                if b[0] == "codigo" and b[1] in DIBUJOS:
                    try:
                        dib.analizar(b[1], b[2])
                    except ValueError as e:
                        h["errores"].append(f"```{b[1]} en «{sec['titulo']}»: {e}")
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
