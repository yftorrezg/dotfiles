#!/usr/bin/env python3
"""Repositorio de GitHub/GitLab/Codeberg (o carpeta local) → imágenes del código, en orden.

    repo-a-imagenes.py <link o carpeta> [--que apuntes,codigo,tarjetas] [--idioma es] [--salida DIR]
                       [--forzar] [--si] [--lineas 42] [--columnas 100] [--max-imagenes 400]

Tres cosas, cada una en su subcarpeta (se pasan con Gwenview, D/A):
  1 Apuntes/   los .md del repo dibujados con diseño (WebKitGTK, tema oscuro), en páginas sin cortar bloques
  2 Código/    cada archivo de código, resaltado y con sus números de línea
  3 Tarjetas/  "¿qué imprime?": frente (código) y dorso (código + SALIDA REAL, ejecutada en un entorno
               aislado con bwrap: sin red y sin tu /home) de cada archivo .py/.js y de cada bloque de
               código de los .md. Si un bloque depende de los anteriores se prueba con ellos.
Repos con traducciones (Spanish/, French/…): sin --idioma se ignoran; con --idioma es solo esa carpeta.
Los repos grandes se bajan parcialmente (solo los archivos usados).

Renderiza el TEXTO real de cada archivo (no es una captura ni pasa por OCR/IA: el código sale
exacto), con resaltado de sintaxis (Pygments) y números de línea reales del archivo. Los archivos
largos se parten en páginas "(1 de 3)" en límites naturales (línea en blanco / antes de un
def, class, function), nunca en medio de un bloque si se puede evitar.

Salida: UNA carpeta plana, ordenada como el curso (orden natural: 2 antes que 10):
    ~/Vídeos/Código de repos/<repo>/001 01_basic - 01_print.py.webp
    ~/Vídeos/Código de repos/<repo>/012 02_loops - 03_range.py (2 de 3).webp
Se pasan con Gwenview (D/A). Si la imagen ya existe no se rehace (--forzar: borrar y rehacer).

Links aceptados: https://github.com/u/repo · …/tree/<rama>/<subcarpeta> (solo esa parte) ·
GitLab · Codeberg · cualquier URL de git. Con --si no pregunta cuando salen más de
--max-imagenes. Código de salida 0 = bien, 1 = error, 2 = demasiadas imágenes (sin --si).
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from pygments import lex
from pygments.lexers import TextLexer, get_lexer_for_filename
from pygments.styles import get_style_by_name
from pygments.token import Token
from pygments.util import ClassNotFound

EXT_CODIGO = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".html", ".htm", ".css", ".scss", ".sass",
    ".php", ".java", ".kt", ".c", ".h", ".cpp", ".hpp", ".cs", ".go", ".rs", ".rb", ".swift",
    ".sql", ".sh", ".bash", ".fish", ".json", ".yml", ".yaml", ".toml", ".vue", ".svelte", ".lua",
    ".r", ".dart", ".ipynb_nunca", ".blade.php", ".ini", ".env.example",
}
NOMBRES_CODIGO = {"Dockerfile", "Makefile", "Procfile", "Gemfile", "Rakefile"}
EXT_TEXTO = {".md", ".txt"}
DIRS_FUERA = {".git", "node_modules", "vendor", "dist", "build", "__pycache__", ".venv", "venv",
              ".idea", ".vscode", ".next", "target", ".github"}
ARCHIVOS_FUERA = {"package-lock.json", "yarn.lock", "pnpm-lock.yaml", "composer.lock", "poetry.lock",
                  "Cargo.lock", "Pipfile.lock"}
MAX_BYTES = 80 * 1024
FUENTES = ["/usr/share/fonts/TTF/MesloLGMNerdFontMono-Regular.ttf",
           "/usr/share/fonts/TTF/DejaVuSansMono.ttf", "/usr/share/fonts/liberation/LiberationMono-Regular.ttf"]
FUENTE_EMOJI = "/usr/share/fonts/noto/NotoColorEmoji.ttf"  # solo existe en tamaño 109
FUENTES_NEGRITA = ["/usr/share/fonts/TTF/MesloLGMNerdFontMono-Bold.ttf",
                   "/usr/share/fonts/TTF/DejaVuSansMono-Bold.ttf"]
INICIO_BLOQUE = re.compile(r"^(def |class |async def |function |export |const \w+ *= *(async )?\(|@|public |private |"
                           r"protected |func |fn |impl |<\?php|<template|<script|<style|#{1,3} )")


def natural(s):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", s)]


def url_de_git(arg):
    """(url_clon, rama|None, subcarpeta, nombre) a partir de un link web de GitHub/GitLab/Codeberg."""
    arg = arg.strip()
    m = re.match(r"^(https?://[^/]+/[^/]+/[^/#?]+?)(?:\.git)?(?:/(?:-/)?(?:tree|blob)/([^/]+)/?(.*?))?/?(?:[#?].*)?$", arg)
    if not m:
        raise SystemExit(f"No entiendo el link: {arg}")
    base, rama, sub = m.group(1), m.group(2), (m.group(3) or "")
    if "/blob/" in arg and sub:  # link a un archivo: se toma su carpeta
        sub = sub.rsplit("/", 1)[0] if "/" in sub else ""
    return base + ".git", rama, sub.strip("/"), base.rsplit("/", 1)[1]


IMG_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}
IDIOMAS = {  # carpetas de traducciones en la raíz de un repo → por defecto se ignoran (salvo --idioma)
    "es": {"spanish", "español", "espanol", "es", "es-es", "spanish-es", "castellano"},
    "en": {"english", "en"},
    "fr": {"french", "français", "francais", "fr"}, "it": {"italian", "italiano", "it"},
    "pt": {"portuguese", "português", "portugues", "pt", "pt-br", "ptbr"}, "ru": {"ru", "russian", "русский"},
    "tr": {"turkish", "türkçe", "tr"}, "pl": {"polish", "polski", "pl"}, "de": {"german", "deutsch", "de"},
    "ko": {"korea", "korean", "ko", "kr"}, "ja": {"japanese", "ja", "jp"}, "zh": {"chinese", "zh", "zh-cn", "zh-tw", "cn"},
    "vi": {"vietnamese", "vi"}, "az": {"azerbaijani", "az"}, "ar": {"arabic", "ar"}, "hi": {"hindi", "hi"},
    "id": {"indonesian", "id"}, "uk": {"ukrainian", "uk"}, "fa": {"persian", "fa"}, "nl": {"dutch", "nl"},
}
TODOS_IDIOMAS = set().union(*IDIOMAS.values()) - {"en", "english"}


def git(*args, cwd=None, entrada=None, check=True):
    r = subprocess.run(["git", *args], cwd=cwd, input=entrada, capture_output=True,
                       env={**os.environ, "GIT_TERMINAL_PROMPT": "0"})
    if check and r.returncode != 0:
        raise SystemExit(f"git {' '.join(args[:2])} falló: {r.stderr.decode(errors='replace').strip()[:300]}")
    return r


class Origen:
    """Un repo (clon parcial: solo trae los archivos que se piden; hay repos de 600 MB por sus imágenes)
    o una carpeta local. `rutas` = todas las rutas del repo (relativas a la raíz), `sub` = subcarpeta pedida."""

    def __init__(self, arg, destino):
        self.local = Path(arg).expanduser().is_dir()
        self.sub = ""
        if self.local:
            self.raiz = Path(arg).expanduser().resolve()
            self.nombre = self.raiz.name
            self.rutas = {}
            for dp, dirs, files in os.walk(self.raiz):
                dirs[:] = [d for d in dirs if d not in DIRS_FUERA and not d.startswith(".")]
                for f in files:
                    q = Path(dp) / f
                    self.rutas[str(q.relative_to(self.raiz))] = q.stat().st_size
            return
        url, rama, sub, nombre = url_de_git(arg)
        self.raiz, self.sub, self.nombre = destino, sub, nombre
        base = ["clone", "--depth", "1", "--quiet", "--filter=blob:none", "--no-checkout"]
        r = git(*base, *(["--branch", rama] if rama else []), url, str(destino), check=False)
        if r.returncode != 0 and rama:  # la "rama" era parte de la ruta, o no existe
            shutil.rmtree(destino, ignore_errors=True)
            r = git(*base, url, str(destino), check=False)
        if r.returncode != 0:
            raise SystemExit(f"No pude clonar {url}: {r.stderr.decode(errors='replace').strip()[:300]}")
        self.rutas = {}
        # sin -l: pedir el tamaño de cada blob obligaría a bajarlos todos uno por uno (clon parcial)
        for linea in git("ls-tree", "-r", "-z", "HEAD", cwd=destino).stdout.decode(errors="replace").split("\0"):
            if "\t" in linea:
                self.rutas[linea.split("\t", 1)[1]] = -1  # -1 = tamaño desconocido hasta traerlo
        if sub and not any(r.startswith(sub + "/") for r in self.rutas):
            raise SystemExit(f"La subcarpeta '{sub}' no existe en el repo")
        if nombre and sub:
            self.nombre = f"{nombre} - {sub.replace('/', ' - ')}"

    def traer(self, rutas):
        """Descarga (checkout) esas rutas; en carpeta local no hace nada."""
        if self.local:
            return
        pendientes = [r for r in rutas if r in self.rutas and not (self.raiz / r).exists()]
        for i in range(0, len(pendientes), 2000):
            git("checkout", "HEAD", "--pathspec-from-file=-", "--pathspec-file-nul", cwd=self.raiz,
                entrada=("\0".join(pendientes[i:i + 2000]) + "\0").encode())


def elegir_rutas(o, idioma, que):
    """Rutas a procesar: (codigo, markdown) ya filtradas, en orden de curso."""
    cod, mds = [], []
    carpeta_idioma = ""
    if idioma and idioma != "en":
        nombres = IDIOMAS.get(idioma, {idioma.lower()})
        for r in o.rutas:
            top = r.split("/")[0].lower()
            if "/" in r and top in nombres:
                carpeta_idioma = r.split("/")[0]
                break
        if not carpeta_idioma:
            raise SystemExit(f"No hay carpeta de '{idioma}' en ese repo")
    for r, tam in o.rutas.items():
        partes = r.split("/")
        if o.sub and not r.startswith(o.sub + "/"):
            continue
        if carpeta_idioma and partes[0] != carpeta_idioma:
            continue
        # sin --idioma: las carpetas de traducciones de la raíz no entran (salvo que el link ya apunte adentro)
        if not carpeta_idioma and not o.sub and len(partes) > 1 and partes[0].lower() in TODOS_IDIOMAS:
            continue
        if any(d in DIRS_FUERA or d.startswith(".") for d in partes[:-1]):
            continue
        f = partes[-1]
        ext = Path(f).suffix.lower()
        if f in ARCHIVOS_FUERA or ".min." in f or f.startswith(".") or tam == 0 or tam > MAX_BYTES:
            continue
        if ext in (".md", ".markdown"):
            if "apuntes" in que and not re.match(r"(?i)(license|licence|code_of_conduct|contributing|changelog|security|"
                                                  r"pull_request|issue_template)", f) and tam != 0:
                mds.append(r)
        elif ext in EXT_CODIGO or f in NOMBRES_CODIGO:
            cod.append(r)
    base = (carpeta_idioma or o.sub).strip("/")

    def clave(r):  # el README de la carpeta base primero (es el índice del curso)
        rel = r[len(base) + 1:] if base and r.startswith(base + "/") else r
        es_indice = "/" not in rel and rel.lower().startswith(("readme", "readme", "index", "leeme"))
        return (0 if es_indice else 1, natural(rel))
    return sorted(cod, key=clave), sorted(mds, key=clave), base


def es_binario(b):
    return b"\0" in b[:4096]


def listar(raiz, con_md):
    archivos = []
    for dp, dirs, files in os.walk(raiz):
        dirs[:] = [d for d in dirs if d not in DIRS_FUERA and not d.startswith(".")]
        for f in files:
            p = Path(dp) / f
            ext = p.suffix.lower()
            if f in ARCHIVOS_FUERA or ".min." in f or f.startswith("."):
                continue
            if not (ext in EXT_CODIGO or f in NOMBRES_CODIGO or (con_md and ext in EXT_TEXTO)):
                continue
            try:
                if p.stat().st_size > MAX_BYTES or p.stat().st_size == 0:
                    continue
            except OSError:
                continue
            archivos.append(p)
    archivos.sort(key=lambda p: natural(str(p.relative_to(raiz))))
    return archivos


def leer(p):
    b = p.read_bytes()
    if es_binario(b):
        return None
    try:
        t = b.decode("utf-8")
    except UnicodeDecodeError:
        t = b.decode("latin-1")
    return t.replace("\r\n", "\n").replace("\r", "\n").replace("\t", "    ").rstrip("\n")


def lineas_resaltadas(texto, nombre, estilo):
    """Lista de líneas; cada línea = lista de (texto, color_rgb, negrita)."""
    try:
        lexer = get_lexer_for_filename(nombre, texto)
    except ClassNotFound:
        lexer = TextLexer()
    lexer.stripnl = False
    lexer.ensurenl = False
    estilos = {}
    for tok, st in estilo:
        c = st["color"]
        estilos[tok] = (tuple(int(c[i:i + 2], 16) for i in (0, 2, 4)) if c else None, bool(st["bold"]))
    lineas, actual = [], []
    for tok, valor in lex(texto, lexer):
        t = tok
        while t not in estilos and t.parent:
            t = t.parent
        color, neg = estilos.get(t, (None, False))
        partes = valor.split("\n")
        for i, parte in enumerate(partes):
            if i > 0:
                lineas.append(actual)
                actual = []
            if parte:
                actual.append((parte, color, neg))
    lineas.append(actual)
    texto_lineas = texto.split("\n")
    return lineas[:len(texto_lineas)] if len(lineas) >= len(texto_lineas) else lineas + [[] for _ in range(len(texto_lineas) - len(lineas))]


def texto_de(linea):
    return "".join(t for t, _, _ in linea)


def partir(lineas, tope):
    """Rangos (ini, fin) de páginas de a lo sumo `tope` líneas, cortando en límites naturales."""
    n, rangos, ini = len(lineas), [], 0
    while ini < n:
        if n - ini <= tope + 10:  # el resto entra (con margen: evita partir un archivo por 3 líneas)
            rangos.append((ini, n))
            break
        fin = ini + tope
        corte = None
        for j in range(fin, ini + tope * 6 // 10, -1):  # buscar hacia atrás un buen corte
            if j >= n:
                continue
            prev, sig = texto_de(lineas[j - 1]), texto_de(lineas[j])
            if sig.strip() == "" and prev.strip() != "":
                corte = j + 1  # la línea en blanco queda al final de la página
                break
            if INICIO_BLOQUE.match(sig) and not sig.startswith(" "):
                corte = j
                break
        fin = corte if corte else fin
        rangos.append((ini, fin))
        ini = fin
    return rangos


class Renderizador:
    def __init__(self, columnas, tamano=22, estilo="one-dark"):
        ruta = next((f for f in FUENTES if Path(f).exists()), None)
        if not ruta:
            raise SystemExit("No encuentro una fuente monoespaciada")
        negrita = next((f for f in FUENTES_NEGRITA if Path(f).exists()), ruta)
        self.fuente = ImageFont.truetype(ruta, tamano)
        self.negrita = ImageFont.truetype(negrita, tamano)
        self.titulo = ImageFont.truetype(negrita, tamano - 2)
        self.ancho_car = self.fuente.getlength("M")
        self.tamano = tamano
        try:
            self.emoji = ImageFont.truetype(FUENTE_EMOJI, 109)
        except OSError:
            self.emoji = None
        self.cache_emoji = {}
        self.alto = int(tamano * 1.55)
        self.columnas = columnas
        try:
            st = get_style_by_name(estilo)
        except ClassNotFound:
            st = get_style_by_name("monokai")
        self.estilo = st
        self.bg = tuple(int(st.background_color.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)) \
            if st.background_color and st.background_color.startswith("#") and len(st.background_color) == 7 else (40, 44, 52)
        lum = sum(self.bg) / 3
        self.fg = (230, 230, 230) if lum < 128 else (30, 30, 30)
        self.tenue = (130, 135, 150) if lum < 128 else (120, 120, 120)
        self.barra = tuple(min(255, c + 14) if lum < 128 else max(0, c - 14) for c in self.bg)

    def emoji_img(self, ch):
        if ch not in self.cache_emoji:
            g = Image.new("RGBA", (136, 128), (0, 0, 0, 0))
            ImageDraw.Draw(g).text((0, 0), ch, font=self.emoji, embedded_color=True)
            lado = int(self.tamano * 1.25)
            self.cache_emoji[ch] = g.resize((int(lado * 136 / 128), lado), Image.LANCZOS)
        return self.cache_emoji[ch]

    def texto(self, im, d, x, y, t, c, b):
        """Dibuja t desde x; los emojis (que la fuente mono no tiene) van como imagen. Devuelve el nuevo x."""
        fuente = self.negrita if b else self.fuente
        tramo = ""
        for ch in t:
            if self.emoji and es_emoji(ch):
                if tramo:
                    d.text((x, y), tramo, font=fuente, fill=c or self.fg, anchor="lm")
                    x += len(tramo) * self.ancho_car
                    tramo = ""
                if ch not in ("\ufe0f", "\u200d"):
                    e = self.emoji_img(ch)
                    im.paste(e, (int(x), int(y - e.height / 2)), e)
                    x += 2 * self.ancho_car
            else:
                tramo += ch
        if tramo:
            d.text((x, y), tramo, font=fuente, fill=c or self.fg, anchor="lm")
            x += len(tramo) * self.ancho_car
        return x

    def imagen(self, lineas, primero, titulo, pagina, salida=None, rotulo_color=None):
        margen, num_ancho = 26, len(str(primero + len(lineas))) + 1
        ancho = int(margen * 2 + (num_ancho + self.columnas) * self.ancho_car + 8)
        barra = int(self.alto * 1.7)
        # líneas largas: se parten en trozos de `columnas` (con ↪ al principio de la continuación)
        filas = []
        for i, l in enumerate(lineas):
            pos, primera = 0, True
            segmentos = list(l) or [("", None, False)]
            cola = [(t, c, b) for t, c, b in segmentos]
            while True:
                fila, usados = [], 0
                cap = self.columnas - (0 if primera else 2)
                while cola and usados < cap:
                    t, c, b = cola[0]
                    libre = cap - usados
                    if len(t) <= libre:
                        fila.append((t, c, b)); usados += len(t); cola.pop(0)
                    else:
                        fila.append((t[:libre], c, b)); cola[0] = (t[libre:], c, b); usados = cap
                filas.append((primero + i if primera else None, fila, primera))
                primera = False
                if not cola:
                    break
        out_filas = []
        if salida is not None:
            for ln in salida:
                ln = ln.replace("\t", "    ")
                out_filas += [ln[k:k + self.columnas] for k in range(0, max(len(ln), 1), self.columnas)]
        alto = barra + (len(filas) + 1) * self.alto + 10
        if salida is not None:
            alto += self.alto * (len(out_filas) + 1) + 24
        im = Image.new("RGB", (ancho, alto), self.bg)
        d = ImageDraw.Draw(im)
        d.rectangle([0, 0, ancho, barra], fill=self.barra)
        d.text((margen, barra // 2), titulo, font=self.titulo, fill=self.fg, anchor="lm")
        if pagina:
            d.text((ancho - margen, barra // 2), pagina, font=self.titulo, fill=rotulo_color or self.tenue, anchor="rm")
        y = barra + self.alto // 2 + 6
        for num, fila, primera in filas:
            if num is not None:
                d.text((margen + (num_ancho - 1) * self.ancho_car, y), str(num), font=self.fuente,
                       fill=self.tenue, anchor="rm")
            x = margen + num_ancho * self.ancho_car
            if not primera:
                d.text((x, y), "↪ ", font=self.fuente, fill=self.tenue, anchor="lm")
                x += 2 * self.ancho_car
            for t, c, b in fila:
                x = self.texto(im, d, x, y, t, c, b)
            y += self.alto
        if salida is not None:  # panel "salida" (resultado real de ejecutar el código)
            y += 14
            top = y - self.alto // 2
            d.rectangle([margen - 10, top, ancho - margen + 10, alto - 12], fill=self.barra, outline=(80, 160, 90), width=2)
            d.text((margen + 6, y + self.alto // 2 - 4), "▶ SALIDA", font=self.titulo, fill=(120, 200, 130), anchor="lm")
            y += self.alto + 6
            for ln in out_filas:
                d.text((margen + 6, y), ln, font=self.fuente, fill=(190, 235, 195), anchor="lm")
                y += self.alto
        return im


def es_emoji(ch):
    o = ord(ch)
    return o >= 0x1F000 or 0x2600 <= o <= 0x27BF or o in (0x2B50, 0x2B06, 0x2B07, 0x2B05, 0x2934, 0x2935, 0x203C, 0x2049, 0xFE0F, 0x200D)


def limpiar(s):
    return re.sub(r'[\\/:*?"<>|\n]', "-", s).strip()


def nombre_legible(rel, base=""):
    """'Spanish/dia_05_Arreglos/dia_05_arreglos.md' → 'dia_05_arreglos' (sin la carpeta base ni la que repite el archivo)."""
    if base and rel.startswith(base + "/"):
        rel = rel[len(base) + 1:]
    partes = rel.split("/")
    partes[-1] = Path(partes[-1]).stem if partes[-1].lower().endswith((".md", ".markdown")) else partes[-1]
    if len(partes) > 1 and partes[-2].lower().replace("-", "_") in partes[-1].lower().replace("-", "_") + "_":
        partes.pop(-2)
    elif len(partes) > 1 and partes[-1].lower().replace("-", "_") in partes[-2].lower().replace("-", "_"):
        partes.pop(-2)
    return " - ".join(partes)


def corto(s, n=70):
    return s if len(s) <= n else s[:n - 1] + "…"


# ------------------------------------------------------------- Markdown ----
def md_a_bloques(texto):
    """Markdown → (lista de bloques HTML de primer nivel, lista de (lenguaje, código, sección) de los fences)."""
    from markdown_it import MarkdownIt
    from pygments import highlight
    from pygments.formatters import HtmlFormatter
    from pygments.lexers import get_lexer_by_name

    def resaltar(codigo, lang, _attrs):
        try:
            lx = get_lexer_by_name((lang or "text").split()[0])
        except ClassNotFound:
            lx = TextLexer()
        return highlight(codigo, lx, HtmlFormatter(noclasses=True, style="one-dark", nowrap=True))

    md = MarkdownIt("commonmark", {"html": True, "highlight": resaltar}).enable("table").enable("strikethrough")
    toks = md.parse(texto)
    bloques, cur, nivel, seccion, fences, vistos_h = [], [], 0, "", [], False
    for i, t in enumerate(toks):
        cur.append(t)
        nivel += t.nesting
        if t.type == "inline" and i and toks[i - 1].type == "heading_open":
            seccion = t.content.strip()
        if t.type == "fence":
            fences.append(((t.info or "").strip().split(" ")[0].lower(), t.content, seccion))
        if nivel == 0:
            html = md.renderer.render(cur, md.options, {})
            if html.strip():
                bloques.append(html)
            cur = []
    return bloques, fences


def renderizar_markdown(o, mds, salida, ancho=1100, alto_max=1500, avisar=print):
    """Dibuja los .md con md-a-png.py. Devuelve {ruta_md: [png, …]} y los fences por md."""
    aqui = Path(__file__).resolve().parent
    tmp = Path(tempfile.mkdtemp(prefix="md-png-"))
    docs, fences_por_md = [], {}
    for k, r in enumerate(mds):
        texto = (o.raiz / r).read_text(encoding="utf-8", errors="replace")
        bloques, fences = md_a_bloques(texto)
        fences_por_md[r] = fences
        if not bloques:
            continue
        base = (o.raiz / r).parent.as_uri() + "/"
        docs.append({"titulo": r, "base": base, "bloques": bloques, "salida": str(tmp / f"d{k:04d}")})
    if not docs:
        return {}, fences_por_md
    (tmp / "trabajos.json").write_text(__import__("json").dumps({"ancho": ancho, "alto_max": alto_max, "docs": docs}))
    p = subprocess.Popen([sys.executable, "-W", "ignore", str(aqui / "md-a-png.py"), str(tmp / "trabajos.json")],
                         stdout=subprocess.PIPE, text=True)
    por_salida = {d["salida"]: d["titulo"] for d in docs}
    res = {}
    for linea in p.stdout:
        try:
            j = __import__("json").loads(linea)
        except ValueError:
            continue
        res[por_salida[j["salida"]]] = j["paginas"]
        avisar(f"  📘 {por_salida[j['salida']]} → {len(j['paginas'])} páginas")
    p.wait()
    if p.returncode != 0 and not res:
        raise SystemExit("md-a-png.py falló (¿WebKitGTK instalado?)")
    return res, fences_por_md


# --------------------------------------------------- ejecutar (tarjetas) ----
RUN_JS = {"js", "javascript", "node", "mjs"}
RUN_PY = {"py", "python", "python3"}
BWRAP = ["bwrap", "--unshare-all", "--die-with-parent", "--new-session", "--ro-bind", "/usr", "/usr",
         "--symlink", "usr/bin", "/bin", "--symlink", "usr/lib", "/lib", "--symlink", "usr/lib64", "/lib64",
         "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp"]
NO_EJECUTAR = re.compile(r"\b(prompt|alert|confirm|require|import\s+[\w{*]|input|open|fetch|XMLHttpRequest|"
                         r"localStorage|sessionStorage|document|window|setInterval|readline|process\.stdin|"
                         r"subprocess|os\.system|__import__|eval|exec)\b\s*[(.]?", re.I)


def ejecutar(codigo, lang, tiempo=5):
    """(ok, salida) corriendo el código en un entorno aislado (bwrap: sin red, sin tu /home, /tmp vacío)."""
    ext, cmd = (".js", ["node"]) if lang in RUN_JS else (".py", ["python3", "-I"])
    if not shutil.which("bwrap"):
        return False, ""
    with tempfile.TemporaryDirectory(prefix="run-") as d:
        f = Path(d) / ("snippet" + ext)
        f.write_text(codigo)
        try:
            r = subprocess.run(["timeout", "-k", "1", str(tiempo), *BWRAP, "--ro-bind", str(f), "/tmp/snippet" + ext,
                                *cmd, "/tmp/snippet" + ext],
                               capture_output=True, text=True, timeout=tiempo + 3, stdin=subprocess.DEVNULL,
                               env={"PATH": "/usr/bin", "LANG": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"})
        except subprocess.TimeoutExpired:
            return False, ""
    if r.returncode != 0:
        return False, r.stderr
    return True, r.stdout.rstrip("\n")


def salida_de_bloque(codigo, lang, previos):
    """Salida real del bloque; si solo falla por depender de bloques anteriores del mismo .md, los antepone
    (y le quita a la salida lo que ya imprimían ellos)."""
    if NO_EJECUTAR.search(re.sub(r"(//|#).*", "", codigo)):
        return None
    ok, out = ejecutar(codigo, lang)
    if ok:
        return out
    if previos and re.search(r"ReferenceError|NameError|is not defined|not defined", out):
        ctx = "\n".join(previos)
        ok0, out0 = ejecutar(ctx, lang)
        ok1, out1 = ejecutar(ctx + "\n" + codigo, lang)
        if ok0 and ok1 and out1.startswith(out0):
            return out1[len(out0):].lstrip("\n")
    return None


def tarjetas(r, trabajo_codigo, fences_por_md, o, salida, avisar=print):
    """Pares frente/dorso '¿qué imprime?' con la salida REAL. Devuelve cuántas tarjetas hizo."""
    items = []  # (título, lang, código)
    for p, rel, ls, rangos in trabajo_codigo:
        ext = Path(rel).suffix.lower().lstrip(".")
        lang = "js" if ext in ("js", "mjs") else "py" if ext == "py" else None
        if lang:
            items.append((rel, lang, p.read_text(errors="replace").replace("\t", "    "), []))
    for md, fences in fences_por_md.items():
        previos = {"js": [], "py": []}
        for lang, codigo, seccion in fences:
            lg = "js" if lang in RUN_JS else "py" if lang in RUN_PY else None
            if not lg:
                continue
            items.append((f"{md} › {seccion}" if seccion else md, lg, codigo.replace("\t", "    "), list(previos[lg])))
            previos[lg].append(codigo)
    hechas = 0
    for titulo, lang, codigo, previos in items:
        lineas_cod = codigo.rstrip("\n").split("\n")
        if len(lineas_cod) > 38 or len(lineas_cod) < 1 or not codigo.strip():
            continue
        if not re.search(r"console\.log|print\(", codigo) and lang in ("js", "py") and not previos:
            continue
        out = salida_de_bloque(codigo, lang, previos)
        if not out or not out.strip():
            continue
        salida_lineas = out.split("\n")
        if len(salida_lineas) > 18:
            salida_lineas = salida_lineas[:18] + [f"… (+{len(out.split(chr(10))) - 18} líneas)"]
        yield titulo, lang, codigo.rstrip("\n"), salida_lineas


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("origen")
    ap.add_argument("--salida", type=Path)
    ap.add_argument("--que", default="apuntes,codigo,tarjetas",
                    help="qué armar: apuntes (los .md dibujados), codigo (archivos) y/o tarjetas (¿qué imprime?)")
    ap.add_argument("--idioma", default="", help="es, en, fr…: usar esa carpeta de traducción del repo")
    ap.add_argument("--md", action="store_true", help="(ya no hace falta: los .md van en 'apuntes')")
    ap.add_argument("--forzar", action="store_true")
    ap.add_argument("--si", action="store_true", help="no frenar si salen muchas imágenes")
    ap.add_argument("--lineas", type=int, default=42)
    ap.add_argument("--columnas", type=int, default=100)
    ap.add_argument("--max-imagenes", type=int, default=400)
    a = ap.parse_args()
    que = {x.strip() for x in a.que.split(",")}
    p = lambda *x: print(*x, flush=True)  # noqa: E731

    tmp = Path(tempfile.mkdtemp(prefix="repo-imagenes-"))
    try:
        p("📥 Leyendo el repositorio…")
        o = Origen(a.origen, tmp / "repo")
        cod, mds, base = elegir_rutas(o, a.idioma.lower(), que)
        if not cod and not mds:
            print("No encontré archivos de código ni apuntes en ese repo.", file=sys.stderr)
            return 1
        # imágenes de los .md: se piden después de leerlos; primero lo que hay que leer
        o.traer(cod + mds)
        r = Renderizador(a.columnas)
        trabajo = []  # (archivo, rel, lineas, rangos)
        if "codigo" in que or "tarjetas" in que:
            for rel in cod:
                q = o.raiz / rel
                t = leer(q) if q.exists() and q.stat().st_size <= MAX_BYTES else None
                if t is None or not t.strip():
                    continue
                ls = lineas_resaltadas(t, q.name, r.estilo)
                trabajo.append((q, rel, ls, partir(ls, a.lineas)))
        total_cod = sum(len(rg) for *_, rg in trabajo) if "codigo" in que else 0
        est_md = sum(max(1, (o.raiz / m).stat().st_size // 2600 + 1) for m in mds if (o.raiz / m).exists())
        p(f"{len(trabajo) if 'codigo' in que else 0} archivos de código → {total_cod} imágenes · "
          f"{len(mds)} documentos .md → ~{est_md} páginas de apuntes")
        if total_cod + est_md > a.max_imagenes and not a.si:
            print(f"Son más de {a.max_imagenes}: repetí con --si (o pasá una subcarpeta con /tree/rama/carpeta, "
                  f"o --idioma es).", file=sys.stderr)
            return 2
        salida = a.salida or Path.home() / "Vídeos" / "Código de repos" / limpiar(o.nombre + (f" [{a.idioma}]" if a.idioma else ""))
        if a.forzar and salida.exists():
            shutil.rmtree(salida)
        salida.mkdir(parents=True, exist_ok=True)
        dir_apuntes, dir_codigo, dir_tarj = salida / "1 Apuntes", salida / "2 Código", salida / "3 Tarjetas"
        nuevas = 0

        fences_por_md = {}
        # ---- 1) apuntes: markdown dibujado
        if mds:
            # imágenes que citan los .md (locales del repo) → se traen todas de una vez
            refs = set()
            for m in mds:
                txt = (o.raiz / m).read_text(encoding="utf-8", errors="replace")
                for ref in re.findall(r'(?:\]\(|src=["\'])(?!https?:|data:|#|/)([^)"\'#?\s]+)', txt):
                    ref = ref.split(" ")[0]
                    ruta = os.path.normpath(os.path.join(os.path.dirname(m), ref))
                    if not ruta.startswith(".."):
                        refs.add(ruta)
            o.traer(sorted(x for x in refs if x in o.rutas and Path(x).suffix.lower() in IMG_EXT))
            if "apuntes" in que:
                p("📘 Dibujando los apuntes (Markdown)…")
                dir_apuntes.mkdir(exist_ok=True)
                pngs, fences_por_md = renderizar_markdown(o, mds, salida, avisar=p)
                n = 0
                for m in mds:
                    for k, png in enumerate(pngs.get(m, []), 1):
                        n += 1
                        dest = dir_apuntes / f"{n:03d} {limpiar(nombre_legible(m, base))}" \
                                             f"{f' ({k} de {len(pngs[m])})' if len(pngs[m]) > 1 else ''}.webp"
                        if not dest.exists():
                            Image.open(png).convert("RGB").save(dest, "WEBP", lossless=True, quality=50, method=1)
                            nuevas += 1
            elif "tarjetas" in que:  # solo los fences, sin dibujar
                for m in mds:
                    fences_por_md[m] = md_a_bloques((o.raiz / m).read_text(encoding="utf-8", errors="replace"))[1]

        # ---- 2) código de los archivos
        if "codigo" in que and trabajo:
            dir_codigo.mkdir(exist_ok=True)
            n = 0
            for q, rel, ls, rangos in trabajo:
                legible = nombre_legible(rel, base)
                for k, (ini, fin) in enumerate(rangos, 1):
                    n += 1
                    sufijo = f" ({k} de {len(rangos)})" if len(rangos) > 1 else ""
                    destino = dir_codigo / f"{n:03d} {limpiar(legible)}{sufijo}.webp"
                    if destino.exists():
                        continue
                    pag = f"{k} de {len(rangos)}" if len(rangos) > 1 else ""
                    r.imagen(ls[ini:fin], ini + 1, rel, pag).save(destino, "WEBP", lossless=True, quality=50, method=1)
                    nuevas += 1

        # ---- 3) tarjetas ¿qué imprime? (salida real, en un entorno aislado)
        if "tarjetas" in que:
            p("🃏 Armando tarjetas (ejecutando el código en un entorno aislado)…")
            n = 0
            for titulo, lang, codigo, sal in tarjetas(None, trabajo, fences_por_md, o, salida, avisar=p):
                n += 1
                dir_tarj.mkdir(exist_ok=True)
                try:
                    ls = lineas_resaltadas(codigo, "x." + ("js" if lang == "js" else "py"), r.estilo)
                except Exception:
                    continue
                nombre = limpiar(corto(nombre_legible(titulo.split(" › ")[0], base) + (" › " + titulo.split(" › ", 1)[1] if " › " in titulo else ""), 90))
                f1 = dir_tarj / f"{n:03d}a ❓ {nombre}.webp"
                f2 = dir_tarj / f"{n:03d}b ✅ {nombre}.webp"
                if f1.exists() and f2.exists():
                    continue
                r.imagen(ls, 1, corto(titulo, 95), "¿QUÉ IMPRIME?", rotulo_color=(229, 192, 123)) \
                    .save(f1, "WEBP", lossless=True, quality=50, method=1)
                r.imagen(ls, 1, corto(titulo, 95), "RESPUESTA", salida=sal, rotulo_color=(152, 195, 121)) \
                    .save(f2, "WEBP", lossless=True, quality=50, method=1)
                nuevas += 2
            p(f"   {n} tarjetas")
        p(f"Listo: {nuevas} imágenes nuevas en {salida}")
        p(salida)
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
