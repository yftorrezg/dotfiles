#!/usr/bin/env python3
"""Repositorio de GitHub/GitLab/Codeberg (o carpeta local) → imágenes del código, en orden.

    repo-a-imagenes.py <link o carpeta> [--salida DIR] [--md] [--forzar] [--si]
                       [--lineas 40] [--columnas 100] [--max-imagenes 400]

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


def clonar(arg, destino):
    """Devuelve (carpeta con el código, nombre del repo)."""
    if Path(arg).expanduser().is_dir():
        p = Path(arg).expanduser().resolve()
        return p, p.name
    url, rama, sub, nombre = url_de_git(arg)
    cmd = ["git", "clone", "--depth", "1", "--quiet"] + (["--branch", rama] if rama else []) + [url, str(destino)]
    r = subprocess.run(cmd, capture_output=True, text=True, env={**os.environ, "GIT_TERMINAL_PROMPT": "0"})
    if r.returncode != 0 and rama:  # la "rama" era en realidad parte de la ruta, o no existe
        r = subprocess.run(["git", "clone", "--depth", "1", "--quiet", url, str(destino)],
                           capture_output=True, text=True, env={**os.environ, "GIT_TERMINAL_PROMPT": "0"})
    if r.returncode != 0:
        raise SystemExit(f"No pude clonar {url}: {r.stderr.strip()[:300]}")
    carpeta = destino / sub if sub else destino
    if not carpeta.is_dir():
        raise SystemExit(f"La subcarpeta '{sub}' no existe en el repo")
    return carpeta, nombre + (f" - {sub.replace('/', ' - ')}" if sub else "")


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

    def imagen(self, lineas, primero, titulo, pagina):
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
        alto = barra + (len(filas) + 1) * self.alto + 10
        im = Image.new("RGB", (ancho, alto), self.bg)
        d = ImageDraw.Draw(im)
        d.rectangle([0, 0, ancho, barra], fill=self.barra)
        d.text((margen, barra // 2), titulo, font=self.titulo, fill=self.fg, anchor="lm")
        if pagina:
            d.text((ancho - margen, barra // 2), pagina, font=self.titulo, fill=self.tenue, anchor="rm")
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
        return im


def es_emoji(ch):
    o = ord(ch)
    return o >= 0x1F000 or 0x2600 <= o <= 0x27BF or o in (0x2B50, 0x2B06, 0x2B07, 0x2B05, 0x2934, 0x2935, 0x203C, 0x2049, 0xFE0F, 0x200D)


def limpiar(s):
    return re.sub(r'[\\/:*?"<>|\n]', "-", s).strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("origen")
    ap.add_argument("--salida", type=Path)
    ap.add_argument("--md", action="store_true", help="incluir .md/.txt")
    ap.add_argument("--forzar", action="store_true")
    ap.add_argument("--si", action="store_true", help="no frenar si salen muchas imágenes")
    ap.add_argument("--lineas", type=int, default=42)
    ap.add_argument("--columnas", type=int, default=100)
    ap.add_argument("--max-imagenes", type=int, default=400)
    a = ap.parse_args()

    tmp = Path(tempfile.mkdtemp(prefix="repo-imagenes-"))
    try:
        carpeta, nombre = clonar(a.origen, tmp / "repo")
        archivos = listar(carpeta, a.md)
        if not archivos:
            print("No encontré archivos de código en ese repo.", file=sys.stderr)
            return 1
        r = Renderizador(a.columnas)
        trabajo = []  # (archivo, rel, lineas, rangos)
        for p in archivos:
            t = leer(p)
            if t is None or not t.strip():
                continue
            ls = lineas_resaltadas(t, p.name, r.estilo)
            trabajo.append((p, str(p.relative_to(carpeta)), ls, partir(ls, a.lineas)))
        total = sum(len(rg) for *_, rg in trabajo)
        print(f"{len(trabajo)} archivos → {total} imágenes")
        if total > a.max_imagenes and not a.si:
            print(f"Son más de {a.max_imagenes}: repetí con --si (o pasá una subcarpeta con /tree/rama/carpeta).",
                  file=sys.stderr)
            return 2
        salida = a.salida or Path.home() / "Vídeos" / "Código de repos" / limpiar(nombre)
        if a.forzar and salida.exists():
            shutil.rmtree(salida)
        salida.mkdir(parents=True, exist_ok=True)
        n = hechas = 0
        for p, rel, ls, rangos in trabajo:
            partes = rel.split("/")
            legible = " - ".join(partes[:-1] + [partes[-1]])
            for k, (ini, fin) in enumerate(rangos, 1):
                n += 1
                sufijo = f" ({k} de {len(rangos)})" if len(rangos) > 1 else ""
                destino = salida / f"{n:03d} {limpiar(legible)}{sufijo}.webp"
                if destino.exists():
                    continue
                pag = f"{k} de {len(rangos)}" if len(rangos) > 1 else ""
                im = r.imagen(ls[ini:fin], ini + 1, rel, pag)
                im.save(destino, "WEBP", lossless=True, quality=50, method=1)
                hechas += 1
        print(f"Listo: {hechas} imágenes nuevas en {salida}")
        print(salida)
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
