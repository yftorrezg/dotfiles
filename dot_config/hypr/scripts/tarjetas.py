#!/usr/bin/env python3
"""Tarjetas de repaso (repetición espaciada) de una clase, SIN llamar a Claude.

    tarjetas.py <carpeta_de_la_clase> [--forzar]
    tarjetas.py --todos <carpeta>          # todas las clases de adentro que tengan apuntes de IA

Arma las tarjetas con lo que ya existe: las preguntas de autoevaluación (.resumen-ia.json),
los conceptos (.apuntes-ia.json) y la chuleta ("¿Cómo …?"). Si falta un JSON usa el otro.
Resultado, en la carpeta de la clase:
  - tarjetas.md        → para el plugin "Spaced Repetition" de Obsidian (mazo por tag
                         #flashcards/<curso>/<clase>; tarjetas de varias líneas con "?").
  - tarjetas-anki.txt  → para Anki: Archivo → Importar (texto con encabezado #separator/#deck…).

El plugin guarda el progreso de cada tarjeta como comentario <!--SR:...--> debajo de ella,
EN el mismo tarjetas.md. Por eso al regenerar se leen esos comentarios y se vuelven a pegar
en la tarjeta con la misma pregunta (las que desaparecen pierden su progreso, obvio), y la
sección "## ✍️ Mis tarjetas" (tarjetas propias) se copia tal cual. Sin --forzar, solo se
regenera si los JSON son más nuevos que tarjetas.md (el plugin lo reescribe al repasar, así
que una edición a mano de una tarjeta generada dura hasta que cambien los apuntes).
Código de salida: siempre 0 salvo error inesperado (sin JSON no es error: no hay nada que hacer;
lo llaman los .sh con set -e).
"""
import argparse
import hashlib
import html
import json
import os
import re
import sys
import unicodedata

MARCA_MIAS = "## ✍️ Mis tarjetas"
ARCHIVO = "tarjetas.md"
ANKI = "tarjetas-anki.txt"


# ------------------------------------------------- parser del plugin (portado) ----
# Copia en Python de parse() de obsidian-spaced-repetition 1.15.4 (src/parser.ts), con los
# separadores por defecto. Sirve para leer el progreso viejo y, en las pruebas, para
# comprobar que lo que escribimos se parsea exactamente como queremos.
def _marca_en_linea(linea, marca):
    """hasInlineMarker: la primera aparición cuenta, salvo que esté dentro de `código`."""
    i = linea.find(marca)
    if i == -1:
        return False
    antes, despues = linea[:i].count("`"), linea[i + len(marca):].count("`")
    return not (antes % 2 == 1 and despues % 2 == 1)


def parsear(texto):
    """[(tipo, texto, primera_linea, ultima_linea)], tipo: 'una' | 'una-inv' | 'multi' | 'multi-inv' | 'cloze'."""
    tarjetas, actual, tipo, primera = [], "", None, 0
    lineas = texto.replace("\r\n", "\n").split("\n")
    i = 0
    while i < len(lineas):
        linea, limpia = lineas[i], lineas[i].strip()
        if linea.startswith("<!--") and not linea.startswith("<!--SR:"):
            # (el plugin tiene un bug: si el comentario no cierra en la misma línea salta hasta el final)
            while i + 1 < len(lineas) and "-->" not in linea:
                i += 1
            i += 2
            continue
        if not limpia:
            if tipo:
                tarjetas.append((tipo, actual.rstrip(), primera, i - 1))
                tipo = None
            actual, primera = "", i + 1
            i += 1
            continue
        actual = (actual + "\n" if actual else "") + linea.rstrip()
        for marca, t in ((":::", "una-inv"), ("::", "una")):
            if _marca_en_linea(linea, marca):
                tipo = t
                break
        if tipo in ("una", "una-inv"):
            actual, primera = linea, i
            if i + 1 < len(lineas) and lineas[i + 1].startswith("<!--SR:"):
                actual += "\n" + lineas[i + 1]
                i += 1
            tarjetas.append((tipo, actual, primera, i))
            tipo, actual = None, ""
        elif limpia == "?":
            if len(actual) > 1:
                tipo = "multi"
        elif limpia == "??":
            if len(actual) > 1:
                tipo = "multi-inv"
        elif linea.startswith("```") or linea.startswith("~~~"):
            cierre = re.match(r"`+|~+", linea).group(0)
            while i + 1 < len(lineas) and not lineas[i + 1].startswith(cierre):
                i += 1
                actual += "\n" + lineas[i]
            actual += "\n" + cierre
            i += 1
        elif tipo is None and re.search(r"==.+?==", linea):
            tipo = "cloze"  # resaltado ==así== = tarjeta de huecos (convertHighlightsToClozes)
        i += 1
    if tipo and actual:
        tarjetas.append((tipo, actual.rstrip(), primera, len(lineas) - 1))
    return tarjetas


# ------------------------------------------------------------- escapado ----
def _escapar_prosa(t):
    t = re.sub(r":(?=:)", r":\\", t)             # ::  → :\:   (se ve igual; no es separador)
    t = re.sub(r"=(?==)", r"=\\", t)             # ==  → =\=   (no es resaltado/hueco)
    t = re.sub(r"<(?=[A-Za-z/!])", r"\\<", t)     # <div>, <!-- … se ven como texto (ni HTML ni comentario)
    t = re.sub(r"(?<![\w\\&])#(?=[^\s#])", r"\\#", t)  # #algo no es tag (ni heading)
    t = re.sub(r" \^(?=[A-Za-z0-9-]+$)", r" \\^", t)   # no es id de bloque
    return t


def escapar_linea(linea, es_pregunta=False):
    """Una línea de texto lista para el parser del plugin: sin separadores ni huecos accidentales.
    El `código` en línea queda intacto (el plugin ignora separadores ahí), salvo casos raros."""
    partes = re.split(r"(`+[^`]*?`+)", linea)
    out = "".join(p if p.startswith("`") else _escapar_prosa(p) for p in partes)
    if out.strip() in ("?", "??"):
        out = out.replace("?", "\\?")
    if out.startswith(("```", "~~~")):
        out = "\\" + out
    # red de seguridad: si igual quedó un separador visible para el plugin (backticks
    # desparejos, ==x== dentro de código en la pregunta…) se corta con un espacio de ancho cero
    if _marca_en_linea(out, "::"):
        out = out.replace("::", ":\u200b:")
    if es_pregunta and re.search(r"==.+?==", out):
        out = re.sub(r"=(?==)", "=\u200b", out)
    return out


def escapar_bloque(texto, es_pregunta=False):
    """Texto de varias líneas: sin líneas en blanco (cortarían la tarjeta) salvo dentro de
    bloques ``` (el parser los salta enteros); un bloque sin cerrar se cierra."""
    L, en_codigo = [], None
    for linea in str(texto).replace("\r\n", "\n").strip("\n").split("\n"):
        if en_codigo:
            L.append(linea)
            if linea.startswith(en_codigo):
                en_codigo = None
        elif re.match(r"^(```|~~~)", linea):
            en_codigo = linea[:3]
            L.append(linea)
        elif linea.strip():
            L.append(escapar_linea(linea.rstrip(), es_pregunta))
    if en_codigo:
        L.append(en_codigo)
    return "\n".join(L)


def clave(pregunta):
    """Identidad de una tarjeta para reencontrar su progreso: la pregunta sin formato."""
    t = unicodedata.normalize("NFKD", pregunta.replace("\u200b", "").replace("\\", "")).lower()
    return re.sub(r"[\W_]+", "", t)


def slug(texto, largo=60):
    """Parte de tag de Obsidian: sin espacios ni símbolos (solo a-z 0-9 -), no solo números."""
    t = unicodedata.normalize("NFKD", re.sub(r"['’]", "", texto))  # Let's → lets
    t = "".join(c for c in t if not unicodedata.combining(c)).lower()
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    if len(t) > largo:
        t = t[:largo].rsplit("-", 1)[0] if "-" in t[:largo] else t[:largo]
    t = t or "clase"
    return "c" + t if t.replace("-", "").isdigit() else t


# ------------------------------------------------------------- tarjetas ----
def _txt(v):
    return str(v or "").strip()


def _como_pregunta(quiero):
    q = _txt(quiero).rstrip(".:?¿ ")
    if len(q) > 1 and q[0].isupper() and q[1].islower():
        q = q[0].lower() + q[1:]  # "Tokenizar…" → "¿Cómo tokenizar…?" (pero "API…" queda)
    return f"¿Cómo {q}?"


def juntar(corto, largo):
    """[(sección, pregunta, respuesta)] sin duplicados ni tarjetas vacías/triviales."""
    tarjetas, vistas, respuestas = [], set(), set()

    def poner(seccion, p, r):
        p, r = _txt(p), _txt(r)
        k, kr = clave(p), clave(r)
        if len(k) < 4 or len(kr) < 3 or k == kr or k in vistas or kr in respuestas:
            return
        vistas.add(k)
        respuestas.add(kr)
        tarjetas.append((seccion, p, r))

    for q in (corto or {}).get("preguntas") or []:
        if isinstance(q, dict):
            poner("🔁 Preguntas de la clase", q.get("pregunta"), q.get("respuesta"))
    for c in (largo or {}).get("conceptos") or []:
        if isinstance(c, dict) and len(_txt(c.get("definicion"))) >= 15:
            poner("📖 Conceptos", f"¿Qué es **{_txt(c.get('termino'))}**?", c.get("definicion"))
    for c in (corto or {}).get("chuleta") or []:
        if isinstance(c, dict) and len(_txt(c.get("quiero"))) >= 4:
            poner("🧩 ¿Cómo se hace?", _como_pregunta(c.get("quiero")), c.get("como"))
    return tarjetas


# -------------------------------------------------- progreso ya guardado ----
def progreso_viejo(texto):
    """({clave de pregunta: [líneas con el progreso]}, texto de 'Mis tarjetas' o None)."""
    mias = None
    if MARCA_MIAS in texto:
        i = texto.index(MARCA_MIAS)
        texto, mias = texto[:i], texto[i:].rstrip("\n")
    progreso = {}
    for tipo, t, _, _ in parsear(texto):
        comentarios = re.findall(r"<!--SR:.+?-->", t)
        if not comentarios:
            continue
        lineas = t.split("\n")
        if tipo.startswith("multi"):
            sep = "?" if tipo == "multi" else "??"
            pregunta = "\n".join(lineas[:[l.strip() for l in lineas].index(sep)])
        else:
            pregunta = re.split(":::|::", lineas[0], maxsplit=1)[0]
        guardar = comentarios
        if "[!sr|card-metadata]" in t:  # ajuste "usar callouts" del plugin
            guardar = ["> [!sr|card-metadata]", "> " + " ".join(comentarios)]
        progreso.setdefault(clave(pregunta), guardar)
    return progreso, mias


# ------------------------------------------------------------- salidas ----
def nombres(carpeta):
    """(curso, clase, título): la clase es la carpeta; el curso, el INDICE.md de capturas/ si hay."""
    titulo = os.path.basename(carpeta)
    try:
        primera = open(os.path.join(carpeta, "apuntes.md"), encoding="utf-8").readline()
        titulo = primera.removeprefix("# 📓 ").strip() or titulo
    except OSError:
        pass
    arriba = os.path.dirname(carpeta)
    indice = os.path.join(arriba, "INDICE.md")
    if os.path.basename(arriba) == "capturas" or os.path.exists(indice):
        curso = os.path.basename(os.path.dirname(arriba))
        try:
            curso = open(indice, encoding="utf-8").readline().removeprefix("# 🎓 ").strip() or curso
        except OSError:
            pass
        return curso, titulo, titulo
    return titulo, None, titulo  # curso de una sola clase: la carpeta es el curso


def armar_md(titulo, tag, tarjetas, progreso, mias):
    L = [f"# 🃏 Tarjetas: {escapar_linea(titulo)}", "", tag, "",
         "*Repaso espaciado con el plugin Spaced Repetition: ícono de tarjetas de la barra izquierda "
         "o Ctrl+P → «Revisar tarjetas en esta nota» / «…de todas las notas» (en inglés: «Review flashcards…»). Las genera tarjetas.py a partir de "
         "[📓 los apuntes](apuntes.md) y [⚡ el resumen](resumen.md); al regenerarlas se conserva tu "
         "progreso y la sección «Mis tarjetas» (lo demás se pisa).*", ""]
    seccion, conservadas = None, 0
    for sec, p, r in tarjetas:
        if sec != seccion:
            L += [f"## {sec}", ""]
            seccion = sec
        pregunta = escapar_bloque(p, es_pregunta=True)
        L += [pregunta, "?", escapar_bloque(r)]
        viejo = progreso.get(clave(pregunta))
        if viejo:
            L += viejo
            conservadas += 1
        L += [""]
    L += [mias or (MARCA_MIAS + "\n\n*Tus tarjetas (pregunta, una línea con `?` sola, respuesta; "
                   "una línea en blanco entre tarjetas). Esta sección nunca se regenera.*"), ""]
    return "\n".join(L), conservadas


def a_html(texto):
    """Markdown mínimo → HTML para Anki (#html:true): ```bloques```, `código`, **negrita**."""
    out = []
    for i, trozo in enumerate(re.split(r"```[^\n]*\n(.*?)\n?```", texto, flags=re.S)):
        if i % 2:
            out.append(f"<pre><code>{html.escape(trozo)}</code></pre>")
            continue
        t = html.escape(trozo.strip("\n"), quote=True)
        t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
        t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
        out.append(t.replace("\n", "<br>"))
    return "".join(out).replace("\t", "    ")


def armar_anki(mazo, tag_anki, tarjetas):
    """Texto importable por Anki (≥2.1.55). guid estable: reimportar actualiza, no duplica."""
    L = ["#separator:tab", "#html:true", "#notetype:Basic", f"#deck:{mazo}",
         "#guid column:1", "#tags column:4"]
    for _, p, r in tarjetas:
        guid = hashlib.sha1(f"{mazo}\n{clave(p)}".encode()).hexdigest()[:20]
        L.append("\t".join((guid, a_html(p), a_html(r), tag_anki)))
    return "\n".join(L) + "\n"


def escribir(ruta, texto):
    """Escritura atómica (Obsidian puede estar mirando el archivo)."""
    tmp = os.path.join(os.path.dirname(ruta), "." + os.path.basename(ruta) + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(texto)
    os.replace(tmp, ruta)


def leer_json(ruta):
    try:
        return json.load(open(ruta, encoding="utf-8"))
    except (OSError, ValueError):
        return None


def generar(carpeta, forzar=False):
    """Arma tarjetas.md y tarjetas-anki.txt. Devuelve la cantidad de tarjetas (0 = nada)."""
    rutas = [os.path.join(carpeta, n) for n in (".resumen-ia.json", ".apuntes-ia.json")]
    corto, largo = (leer_json(r) for r in rutas)
    if not corto and not largo:
        print(f"Sin .resumen-ia.json ni .apuntes-ia.json en {carpeta}: no hay de dónde sacar tarjetas")
        return 0
    salida = os.path.join(carpeta, ARCHIVO)
    if os.path.exists(salida) and not forzar:
        nuevo = max(os.path.getmtime(r) for r in rutas if os.path.exists(r))
        if nuevo <= os.path.getmtime(salida):
            print(f"Ya existe {salida} y los apuntes no cambiaron (usar --forzar para rehacerlo)")
            return 0
    tarjetas = juntar(corto, largo)
    if not tarjetas:
        print(f"No salió ninguna tarjeta de {carpeta}")
        return 0
    curso, clase, titulo = nombres(carpeta)
    tag = "#flashcards/" + slug(curso) + (f"/{slug(clase)}" if clase else "")
    progreso, mias = {}, None
    if os.path.exists(salida):
        progreso, mias = progreso_viejo(open(salida, encoding="utf-8").read())
    md, conservadas = armar_md(titulo, tag, tarjetas, progreso, mias)
    escribir(salida, md)
    mazo = "Cursos::" + "::".join(n.replace("::", ":") for n in ([curso, clase] if clase else [curso]))
    escribir(os.path.join(carpeta, ANKI), armar_anki(mazo, tag[1:].replace("/", "::"), tarjetas))
    extra = f", {conservadas} con progreso conservado" if progreso else ""
    print(f"🃏 {len(tarjetas)} tarjetas{extra}: {salida}")
    return len(tarjetas)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("carpeta")
    p.add_argument("--forzar", action="store_true")
    p.add_argument("--todos", action="store_true", help="todas las clases con apuntes de IA dentro de la carpeta")
    a = p.parse_args()
    carpeta = os.path.abspath(a.carpeta)
    if not a.todos:
        generar(carpeta, a.forzar)
        return 0
    clases = sorted({r for r, ds, fs in os.walk(carpeta)
                     if not os.path.basename(r).startswith(".")
                     and (".apuntes-ia.json" in fs or ".resumen-ia.json" in fs)})
    total = sum(generar(c, a.forzar) for c in clases)
    print(f"{len(clases)} clases revisadas, {total} tarjetas (re)generadas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
