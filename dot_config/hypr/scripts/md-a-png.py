#!/usr/bin/env python3
"""Motor de dibujo de Markdown → PNG (lo usa repo-a-imagenes.py). Sin ventana: WebKitGTK offscreen.

    md-a-png.py trabajos.json

trabajos.json = {"ancho": 1100, "alto_max": 1500, "docs": [
    {"titulo": "02_Day/02_day.md", "base": "file:///ruta/de/la/carpeta/", "bloques": ["<h1>…</h1>", "<p>…</p>"],
     "salida": "/tmp/x/doc-0001"}]}
Cada documento se parte en páginas de a lo sumo `alto_max` px SIN cortar un bloque (los títulos se
pegan al bloque que sigue) y se escribe <salida>-01.png, -02.png… Imprime por stdout una línea
JSON por documento: {"salida": …, "paginas": ["…-01.png", …]}.
Variables: WEBKIT_DISABLE_COMPOSITING_MODE=1 (se pone solo; sin eso WebKit pide OpenGL y aborta).
"""
import html
import json
import os
import sys
import time

os.environ.setdefault("WEBKIT_DISABLE_COMPOSITING_MODE", "1")
os.environ.setdefault("WEBKIT_DISABLE_DMABUF_RENDERER", "1")
import gi  # noqa: E402

gi.require_version("Gtk", "3.0")
gi.require_version("WebKit2", "4.1")
from gi.repository import GLib, Gtk, WebKit2  # noqa: E402

CSS = """
:root{--bg:#1e2128;--panel:#282c34;--fg:#dfe3ea;--tenue:#8b93a5;--acento:#61afef;--verde:#98c379;
--rojo:#e06c75;--amarillo:#e5c07b;--borde:#3a404c}
*{box-sizing:border-box}
html,body{margin:0;background:var(--bg);color:var(--fg)}
body{font:21px/1.62 "Noto Sans","Inter","DejaVu Sans",sans-serif;-webkit-font-smoothing:antialiased}
.barra{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:14px 34px;
background:#252932;border-bottom:1px solid var(--borde);font:600 17px/1.2 "DejaVu Sans Mono","Noto Sans Mono",monospace;
color:var(--fg)}
.barra .pag{color:var(--tenue);font-weight:500;white-space:nowrap}
.barra .ruta{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
main{padding:26px 44px 40px}
main>*:first-child{margin-top:0}
h1,h2,h3,h4{line-height:1.25;margin:1.5em 0 .55em;font-weight:700}
h1{font-size:2em;color:#fff;border-bottom:2px solid var(--acento);padding-bottom:.25em}
h2{font-size:1.55em;color:var(--acento);border-bottom:1px solid var(--borde);padding-bottom:.2em}
h3{font-size:1.25em;color:var(--amarillo)}
h4{font-size:1.1em;color:var(--verde)}
p{margin:.7em 0}
a{color:var(--acento);text-decoration:none}
strong{color:#fff}
ul,ol{padding-left:1.5em;margin:.6em 0}
li{margin:.25em 0}
li>p{margin:.2em 0}
code{font:0.86em "MesloLGM Nerd Font Mono","DejaVu Sans Mono",monospace;background:#323844;color:#f0c987;
padding:.12em .38em;border-radius:5px}
pre{background:var(--panel);border:1px solid var(--borde);border-left:4px solid var(--acento);border-radius:10px;
padding:16px 20px;margin:1em 0;overflow:hidden;font:0.82em/1.5 "MesloLGM Nerd Font Mono","DejaVu Sans Mono",monospace;
white-space:pre-wrap;word-break:break-word}
pre code{background:none;padding:0;color:inherit;font:inherit;border-radius:0}
blockquote{margin:1em 0;padding:.4em 1.1em;border-left:4px solid var(--amarillo);background:#262a33;
border-radius:0 10px 10px 0;color:#cfd5e1}
blockquote p{margin:.4em 0}
table{border-collapse:collapse;margin:1em 0;font-size:.92em;width:auto;max-width:100%}
th,td{border:1px solid var(--borde);padding:.45em .8em;text-align:left;vertical-align:top}
th{background:#2d323d;color:#fff}
tr:nth-child(even) td{background:#23272f}
hr{border:0;border-top:1px solid var(--borde);margin:1.6em 0}
img{max-width:100%;height:auto;border-radius:8px;display:inline-block;vertical-align:middle}
div[align=center],p[align=center],center{text-align:center}
details{margin:.7em 0}
kbd{background:#323844;border:1px solid var(--borde);border-radius:4px;padding:0 .35em;font-size:.85em}
"""


class Motor:
    def __init__(self, ancho):
        self.ancho = ancho
        self.win = Gtk.OffscreenWindow()
        self.win.set_default_size(ancho, 100)
        self.wv = WebKit2.WebView()
        s = self.wv.get_settings()
        for p in ("allow_file_access_from_file_urls", "allow_universal_access_from_file_urls"):
            try:
                s.set_property(p, True)
            except TypeError:
                pass
        self.win.add(self.wv)
        self.win.show_all()

    @staticmethod
    def esperar(cond, timeout):
        t = time.time()
        while not cond() and time.time() - t < timeout:
            Gtk.main_iteration_do(False)
            time.sleep(0.004)
        return cond()

    def cargar(self, archivo, timeout=40):
        listo = []

        def cambio(_v, ev):
            if ev == WebKit2.LoadEvent.FINISHED:
                listo.append(1)
        h = self.wv.connect("load-changed", cambio)
        self.wv.load_uri("file://" + archivo)
        self.esperar(lambda: listo, timeout)
        self.wv.disconnect(h)
        self.pausa(0.15)  # deja pintar las imágenes decodificadas

    def pausa(self, s):
        t = time.time()
        while time.time() - t < s:
            Gtk.main_iteration_do(False)
            time.sleep(0.004)

    def js(self, codigo):
        res = []
        self.wv.run_javascript(codigo, None, lambda v, r: res.append(v.run_javascript_finish(r)))
        self.esperar(lambda: res, 15)
        return res[0].get_js_value().to_string() if res else None

    def foto(self, salida):
        res = []
        self.wv.get_snapshot(WebKit2.SnapshotRegion.FULL_DOCUMENT, WebKit2.SnapshotOptions.NONE, None,
                             lambda v, r: res.append(v.get_snapshot_finish(r)))
        self.esperar(lambda: res, 20)
        if not res:
            raise RuntimeError("sin captura")
        res[0].write_to_png(salida)


def pagina_html(base, titulo, bloques, pagina=None, medir=False):
    barra = ""
    if not medir:
        barra = (f'<div class="barra"><span class="ruta">📘 {html.escape(titulo)}</span>'
                 f'<span class="pag">{html.escape(pagina or "")}</span></div>')
    cuerpo = "".join(f'<div class="b" data-i="{i}">{b}</div>' if medir else b for i, b in enumerate(bloques))
    return (f'<!doctype html><html><head><meta charset="utf-8"><base href="{html.escape(base)}">'
            f'<style>{CSS}</style></head><body>{barra}<main>{cuerpo}</main></body></html>')


def empaquetar(alturas, textos_titulo, alto_max, cabecera):
    """alturas[i] = alto del bloque i (con márgenes). Devuelve lista de páginas = listas de índices."""
    paginas, actual, usado = [], [], 0
    i, n = 0, len(alturas)
    while i < n:
        grupo = [i]  # un título se pega al bloque siguiente (y varios títulos seguidos juntos)
        while textos_titulo[grupo[-1]] and grupo[-1] + 1 < n:
            grupo.append(grupo[-1] + 1)
        h = sum(alturas[j] for j in grupo)
        if actual and usado + h > alto_max - cabecera:
            paginas.append(actual)
            actual, usado = [], 0
        actual += grupo
        usado += h
        i = grupo[-1] + 1
    if actual:
        paginas.append(actual)
    return paginas


def main():
    cfg = json.load(open(sys.argv[1]))
    ancho, alto_max = cfg.get("ancho", 1100), cfg.get("alto_max", 1500)
    m = Motor(ancho)
    tmp = os.path.dirname(os.path.abspath(sys.argv[1]))
    for d_i, d in enumerate(cfg["docs"]):
        base, bloques = d["base"], d["bloques"]
        es_titulo = [b.lstrip().startswith(("<h1", "<h2", "<h3", "<h4")) for b in bloques]
        # 1) medir: todo el documento en una página, alto de cada bloque
        arch = os.path.join(tmp, f"medir-{d_i}.html")
        open(arch, "w").write(pagina_html(base, d["titulo"], bloques, medir=True))
        m.cargar(arch)
        tops = json.loads(m.js("JSON.stringify([...document.querySelectorAll('.b')].map(e=>e.getBoundingClientRect().top+window.scrollY)"
                               ".concat([document.querySelector('main').getBoundingClientRect().bottom+window.scrollY-40]))") or "[]")
        if len(tops) != len(bloques) + 1:
            tops = [i * 200 for i in range(len(bloques) + 1)]
        alturas = [max(10, tops[i + 1] - tops[i]) for i in range(len(bloques))]
        paginas = empaquetar(alturas, es_titulo, alto_max, cabecera=70)
        # 2) dibujar cada página
        salidas = []
        for k, idx in enumerate(paginas, 1):
            etiqueta = f"{k} de {len(paginas)}" if len(paginas) > 1 else ""
            arch = os.path.join(tmp, f"pag-{d_i}-{k}.html")
            open(arch, "w").write(pagina_html(base, d["titulo"], [bloques[j] for j in idx], etiqueta))
            m.cargar(arch)
            out = f'{d["salida"]}-{k:02d}.png'
            m.foto(out)
            salidas.append(out)
        print(json.dumps({"salida": d["salida"], "paginas": salidas}), flush=True)


if __name__ == "__main__":
    GLib.set_prgname("md-a-png")
    main()
