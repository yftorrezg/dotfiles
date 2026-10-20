#!/usr/bin/env python3
"""chuletas.py — chuletas de programación e inglés para estudiar (SUPER+SHIFT+C).

Lee ~/.config/hypr/chuletas/NN-tema.md (formato en chuletas/FORMATO.md, lo interpreta chuletas_md.py):
secciones con emoji, explicaciones, ejemplos resueltos, cajas 💡 ⚠️ 🇬🇧 📌 y tablas de vocabulario.

Dos modos (F11 o el botón ⛶ cambia; se recuerda):
  lateral   panel a la derecha que APARTA las ventanas: programas con la chuleta al lado.
  completo  toda la pantalla para estudiar: índice de temas y secciones a la izquierda,
            texto grande y centrado.
Usa los colores del esquema activo de noctalia (combina con tu tema y se lee bien en claro y oscuro).

Teclas: escribe para buscar en todas · Tab / Shift+Tab tema · ↑↓ PgUp PgDn Inicio Fin desplazar ·
Ctrl+↑↓ sección anterior/siguiente · Enter copia el primer resultado · Esc borra la búsqueda o cierra.
Clic en una entrada o en «Copiar» = copiar el código. El texto se puede seleccionar con el ratón.
"""
import ctypes

ctypes.CDLL("libgtk4-layer-shell.so")

import html  # noqa: E402
import json  # noqa: E402
import os  # noqa: E402
import re  # noqa: E402
import socket  # noqa: E402
import subprocess  # noqa: E402
import tomllib  # noqa: E402
import unicodedata  # noqa: E402
from pathlib import Path  # noqa: E402

import gi  # noqa: E402

import chuletas_dibujo as dib  # noqa: E402
import chuletas_md as md  # noqa: E402
import time  # noqa: E402

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
gi.require_version("Gsk", "4.0")
gi.require_version("Graphene", "1.0")
gi.require_version("Gtk4LayerShell", "1.0")
from gi.repository import Gdk, GLib, Graphene, Gsk, Gtk, Pango  # noqa: E402
from gi.repository import Gtk4LayerShell as LS  # noqa: E402

NOCT_SETTINGS = Path.home() / ".local/state/noctalia/settings.toml"
PALETAS = Path.home() / ".config/noctalia/palettes"
ESTADO = Path.home() / ".local/state/escritorios-vivos/chuletas.json"
HYPR = Path(os.environ["XDG_RUNTIME_DIR"]) / "hypr" / os.environ["HYPRLAND_INSTANCE_SIGNATURE"] / ".socket.sock"
MONO = "Adwaita Mono"

# --- resaltado de código ----------------------------------------------------------------
JS = ("const let var function return if else for of in while do switch case default break continue new class "
      "extends super async await try catch finally throw import export from as typeof instanceof null undefined "
      "true false this delete void yield static get set")
PALABRAS = {
    "python": "def class return if elif else for while in not and or import from as with try except finally raise "
              "lambda yield None True False pass break continue is async await global nonlocal assert del match case",
    "js": JS, "jsx": JS, "ts": JS + " interface type enum implements private public readonly number string boolean any",
    "css": "!important @media @keyframes @import @font-face @container @supports",
    "sql": "SELECT FROM WHERE AND OR NOT IN LIKE ILIKE BETWEEN ORDER BY DESC ASC LIMIT OFFSET GROUP HAVING JOIN INNER "
           "LEFT RIGHT FULL OUTER ON INSERT INTO VALUES UPDATE SET DELETE CREATE TABLE ALTER ADD COLUMN INDEX DROP "
           "DISTINCT COUNT AVG MAX MIN SUM AS PRIMARY KEY FOREIGN REFERENCES NULL UNIQUE CHECK DEFAULT INTEGER "
           "TEXT INT REAL VARCHAR BOOLEAN DATE WITH VIEW BEGIN COMMIT ROLLBACK CASE WHEN THEN END OVER PARTITION "
           "UNION ALL EXISTS IS EXPLAIN",
    "bash": "if then else elif fi for in do done while case esac function return export local echo sudo cd ls cat grep "
            "find rm cp mv mkdir git pip npm npx node python python3 docker chmod chown kill pkill systemctl "
            "pacman paru curl ssh tar set end",
    "dockerfile": "FROM RUN COPY ADD WORKDIR CMD ENTRYPOINT ENV ARG EXPOSE VOLUME USER LABEL HEALTHCHECK AS",
    "yaml": "true false null", "json": "true false null", "html": "", "text": "",
    "c": "int char float double void return if else for while do switch case break continue struct typedef const "
         "static unsigned long short sizeof NULL include define auto class public private template typename "
         "namespace using new delete nullptr bool true false std",
    "java": "public private protected class interface extends implements static final void int long double boolean "
            "char String new return if else for while do switch case break continue try catch finally throw throws "
            "import package null true false this super abstract enum record var",
    "go": "func package import return if else for range switch case default break continue go defer chan map struct "
          "interface type var const nil true false make new select",
}
ALIAS = {"py": "python", "javascript": "js", "typescript": "ts", "tsx": "jsx", "sh": "bash", "shell": "bash",
         "fish": "bash", "console": "bash", "docker": "dockerfile", "yml": "yaml", "postgres": "sql",
         "cpp": "c", "c++": "c", "golang": "go", "kotlin": "java", "csharp": "java", "cs": "java"}
COMENTARIO = {"python": r"#.*$", "bash": r"#.*$", "dockerfile": r"#.*$", "yaml": r"#.*$",
              "js": r"//.*$|/\*.*?\*/", "jsx": r"//.*$|/\*.*?\*/", "ts": r"//.*$|/\*.*?\*/",
              "css": r"/\*.*?\*/", "sql": r"--.*$", "c": r"//.*$|/\*.*?\*/", "java": r"//.*$|/\*.*?\*/",
              "go": r"//.*$|/\*.*?\*/", "html": r"<!--.*?-->", "json": r"(?!x)x", "text": r"(?!x)x"}


def _patron(leng):
    etiqueta_html = r"|(?P<tag></?[A-Za-z][\w.-]*>?|/?>)" if leng in ("html", "jsx") else ""
    clave_yaml = r"|(?P<prop>^\s*[\w.-]+(?=:))" if leng == "yaml" else ""
    prop_css = r"|(?P<prop>[\w-]+(?=\s*:[^:]))" if leng == "css" else ""
    return re.compile(rf"""(?P<com>{COMENTARIO[leng]}){etiqueta_html}{clave_yaml}{prop_css}"""
                      r"""|(?P<txt>"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|`[^`]*`)"""
                      r"""|(?P<num>\b\d+(?:\.\d+)?(?:px|rem|em|ms|s|fr|vh|vw|%)?\b)|(?P<pal>[@!]?[A-Za-z_][\w-]*)|(?P<otro>.|\n)""",
                      re.M | re.S if leng in ("css", "html") else re.M)


PATRONES = {k: _patron(k) for k in COMENTARIO}


def resaltar(codigo, leng, c):
    """Código → Pango markup coloreado con los colores de la terminal del esquema activo."""
    leng = ALIAS.get(leng, leng)
    if leng not in PATRONES:
        leng = "text"
    claves = set(PALABRAS[leng].split())
    if leng == "sql":
        claves |= {k.lower() for k in claves}
    partes = []
    for m in PATRONES[leng].finditer(codigo):
        t, g = html.escape(m.group()), m.lastgroup
        color = {"com": c["com"], "txt": c["txt"], "num": c["num"], "tag": c["tag"], "prop": c["prop"]}.get(g)
        if g == "pal" and m.group() in claves:
            partes.append(f'<span foreground="{c["clave"]}" weight="bold">{t}</span>')
        elif color:
            estilo = ' style="italic"' if g == "com" else ""
            partes.append(f'<span foreground="{color}"{estilo}>{t}</span>')
        else:
            partes.append(t)
    return "".join(partes)


def en_linea(texto, c):
    """Markdown mínimo de los párrafos: `código` y **negrita** → Pango markup (la negrita puede envolver código)."""
    trozos = []

    def guardar(m):
        trozos.append(f'<span font_family="{MONO}" background="{c["fondo_cod"]}" foreground="{c["cod_linea"]}">'
                      f' {html.escape(m.group(1))} </span>')
        return f"\x00{len(trozos) - 1}\x00"
    sin_codigo = re.sub(r"`([^`]+)`", guardar, texto)
    salida = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", html.escape(sin_codigo, quote=False))
    salida = re.sub(r"(?<![\w*])\*(?!\s)([^*\n]+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", salida)  # *cursiva*
    return re.sub(r"\x00(\d+)\x00", lambda m: trozos[int(m.group(1))], salida)


# --- utilidades -------------------------------------------------------------------------
def hypr_json(cmd):
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
        s.connect(str(HYPR))
        s.sendall(f"j/{cmd}".encode())
        data = b""
        while chunk := s.recv(65536):
            data += chunk
    return json.loads(data)


def paleta():
    """Colores del esquema activo de noctalia (custom) en el modo actual; si no, Yafer."""
    try:
        with open(NOCT_SETTINGS, "rb") as f:
            tema = tomllib.load(f).get("theme", {})
    except (OSError, tomllib.TOMLDecodeError):
        tema = {}
    modo = tema.get("mode", "dark")
    nombre = tema.get("custom_palette", "yafer") if tema.get("source") == "custom" else "yafer"
    for n in (nombre, "yafer"):
        try:
            return json.loads((PALETAS / f"{n}.json").read_text())[modo], modo
        except (OSError, ValueError, KeyError):
            continue
    return None, modo


def mezclar(a, b, t):
    x = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    y = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(p + (q - p) * t):02x}" for p, q in zip(x, y))


def sin_tildes(texto):
    return unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().casefold()


def leer_estado():
    try:
        return json.loads(ESTADO.read_text())
    except (OSError, ValueError):
        return {}


def guardar_estado(d):
    try:
        ESTADO.parent.mkdir(parents=True, exist_ok=True)
        ESTADO.write_text(json.dumps(d))
    except OSError:
        pass


def corto(titulo):
    """«🇬🇧 Inglés 1 · Sonidos y vocabulario» → «🇬🇧 Inglés 1» para pestañas e índice."""
    return titulo.split(" · ")[0]


def etiqueta(texto="", clases=(), markup=None, wrap=True, seleccionable=False):
    lbl = Gtk.Label(xalign=0, wrap=wrap, selectable=seleccionable)
    if wrap:
        lbl.set_wrap_mode(Pango.WrapMode.WORD_CHAR)
    if markup is not None:
        lbl.set_markup(markup)
    else:
        lbl.set_label(texto)
    for c in clases:
        lbl.add_css_class(c)
    return lbl


PALETA_DEFECTO = ('{"mSurface":"#1a1c23","mSurfaceVariant":"#2b2e3b","mOnSurface":"#f2f2f3",'
                  '"mOnSurfaceVariant":"#b4b5bd","mPrimary":"#8fa0ec","mOnPrimary":"#16161c","mOutline":"#61677a",'
                  '"terminal":{"normal":{"red":"#ff6b81","green":"#8fd18a","yellow":"#f2c46d",'
                  '"blue":"#82aaff","magenta":"#c79bf2","cyan":"#7fd6d0"},"bright":{"black":"#70758a"}}}')


def hoja_css(p, claro, c):
    t = p["terminal"]["normal"]
    f, f2, pri, txt, txt2, borde = (p[k] for k in ("mSurface", "mSurfaceVariant", "mPrimary", "mOnSurface",
                                                   "mOnSurfaceVariant", "mOutline"))
    notas = {"consejo": t["green"], "cuidado": t["red"] if claro else t["yellow"], "ingles": t["blue"], "nota": pri,
             "bien": t["green"], "mal": t["red"], "concepto": t["magenta"], "futuro": t["cyan"]}
    css_notas = "".join(
        f".nota-{k} {{ border-left: 4px solid {col}; background-color: alpha({col}, {0.10 if claro else 0.12}); }}"
        for k, col in notas.items())
    return f"""
window.chuletas {{ background: transparent; }}
.caja {{ background-color: alpha({f}, 0.975); color: {txt};
        border-radius: 26px; border: 1px solid alpha({borde}, 0.45);
        font-family: "Adwaita Sans", "Inter", sans-serif;
        box-shadow: 0 16px 50px rgba(0,0,0,{0.18 if claro else 0.45});
        transition: opacity 220ms ease, transform 320ms cubic-bezier(.2,1.2,.3,1); }}
.caja.oculta {{ opacity: 0; transform: translateX(40px); }}
.completo .caja.oculta {{ transform: scale(0.97); }}
.cabecera {{ padding: 18px 18px 0 20px; }}
.marca {{ font-size: 22px; font-weight: 800; }}
.boton {{ font-size: 15px; font-weight: 700; padding: 4px 12px; border-radius: 99px; min-height: 0;
         background-color: {f2}; color: {txt}; border: none; box-shadow: none; }}
.boton:hover {{ background-color: alpha({pri}, 0.25); }}
.pestana {{ font-size: 14px; font-weight: 700; padding: 5px 11px; border-radius: 99px; min-height: 0;
           background: transparent; color: {txt2}; border: none; box-shadow: none; }}
.pestana:hover {{ background-color: {f2}; }}
.pestana.activa {{ background-color: {pri}; color: {p['mOnPrimary']}; }}
.lateral-izq {{ background-color: alpha({f2}, 0.55); border-radius: 26px 0 0 26px; padding: 20px 12px; }}
flowboxchild {{ padding: 0; }}
.selector-tema {{ font-size: 15px; font-weight: 750; border-radius: 99px; padding: 2px 6px; min-height: 0;
                 background-color: {pri}; color: {p['mOnPrimary']}; border: none; box-shadow: none; }}
.selector-tema:hover {{ background-color: alpha({pri}, 0.85); }}
popover.selector-pop > contents {{ background-color: {f}; border-radius: 18px; padding: 10px; border: 1px solid alpha({borde}, 0.5); }}
.nav {{ font-size: 14px; font-weight: 650; padding: 6px 10px; border-radius: 11px; min-height: 0;
       background: transparent; color: {txt}; border: none; box-shadow: none; }}
.nav:hover {{ background-color: alpha({pri}, 0.14); }}
.nav.activa {{ background-color: {pri}; color: {p['mOnPrimary']}; }}
.toc {{ font-size: 14px; font-weight: 500; padding: 5px 12px; border-radius: 10px; min-height: 0;
       background: transparent; color: {txt2}; border: none; box-shadow: none; }}
.toc:hover {{ background-color: alpha({pri}, 0.12); color: {txt}; }}
.toc.activa {{ color: {pri}; font-weight: 800; background-color: alpha({pri}, 0.10); }}
.nav-titulo {{ font-size: 12px; font-weight: 800; letter-spacing: 1.5px; color: {txt2}; margin: 14px 12px 6px 12px; }}
.busqueda {{ font-size: 15px; font-weight: 600; padding: 9px 16px; border-radius: 14px;
            background-color: {f2}; color: {txt2}; }}
.busqueda.activa {{ color: {txt}; box-shadow: inset 0 0 0 2px {pri}; }}
scrolledwindow, scrolledwindow > viewport {{ background: transparent; }}
.hoja-titulo {{ font-size: 30px; font-weight: 800; letter-spacing: -0.5px; }}
.hoja-sub {{ font-size: 16px; color: {txt2}; margin-bottom: 6px; }}
.h2 {{ font-size: 22px; font-weight: 800; margin-top: 26px; padding-bottom: 8px;
      border-bottom: 2px solid alpha({pri}, 0.35); }}
.h3 {{ font-size: 17.5px; font-weight: 750; margin-top: 14px; color: {pri}; }}
.p {{ font-size: 15.5px; }}
.entrada {{ padding: 10px 14px; border-radius: 14px; background-color: alpha({f2}, 0.6); border: 1px solid transparent; }}
.entrada:hover {{ background-color: {f2}; border-color: alpha({pri}, 0.5); }}
.copiada {{ border-color: {pri}; box-shadow: 0 0 0 2px alpha({pri}, 0.35); }}
.e-codigo {{ font-family: "{MONO}", monospace; font-size: 14.5px; }}
.e-exp {{ font-size: 14px; color: {txt2}; margin-top: 3px; }}
.bloque {{ border-radius: 16px; background-color: {c['fondo_cod']}; border: 1px solid alpha({borde}, 0.35); }}
.bloque-cab {{ padding: 6px 8px 0 14px; }}
.leng {{ font-size: 11.5px; font-weight: 800; letter-spacing: 1px; color: {txt2}; }}
.copiar {{ font-size: 12.5px; font-weight: 700; padding: 2px 10px; border-radius: 99px; min-height: 0;
          background: transparent; color: {txt2}; border: none; box-shadow: none; }}
.copiar:hover {{ background-color: alpha({pri}, 0.2); color: {txt}; }}
.codigo {{ font-family: "{MONO}", monospace; font-size: 14.5px; padding: 6px 16px 14px 16px; }}
.nota {{ border-radius: 12px; padding: 10px 14px; font-size: 15px; }}
{css_notas}
.tabla {{ border-radius: 14px; border: 1px solid alpha({borde}, 0.45); }}
.fila {{ border-bottom: 1px solid alpha({borde}, 0.22); }}
.fila:last-child {{ border-bottom: none; }}
.fila.cab {{ font-weight: 800; background-color: alpha({pri}, 0.18); border-bottom: 2px solid alpha({pri}, 0.45); }}
.fila.par {{ background-color: alpha({f2}, 0.55); }}
.fila.copiable:hover {{ background-color: alpha({pri}, 0.13); }}
.fila.copiada {{ background-color: alpha({pri}, 0.25); }}
.celda {{ padding: 8px 13px; font-size: 14.5px; }}
.celda.con-borde {{ border-left: 1px solid alpha({borde}, 0.22); }}
.celda.e-exp {{ margin-top: 0; }}
.lista {{ margin-left: 4px; }}
.vineta {{ font-size: 15.5px; font-weight: 800; color: {pri}; min-width: 22px; }}
.imagen {{ background-color: #f7f8fb; border-radius: 16px; padding: 12px; border: 1px solid alpha({borde}, 0.35); }}
.pie-img {{ font-size: 13.5px; color: {txt2}; font-style: italic; }}
.dibujo {{ border-radius: 16px; padding: 16px; border: 1px solid alpha({borde}, 0.4); }}
.dibujo-error {{ color: {t["red"]}; font-size: 13px; }}
expander.desplegable {{ border-radius: 14px; border: 1px solid alpha({pri}, 0.35); background-color: alpha({pri}, 0.05); }}
expander.desplegable > title {{ padding: 10px 14px; border-radius: 14px; }}
expander.desplegable > title:hover {{ background-color: alpha({pri}, 0.12); }}
.desp-titulo {{ font-size: 15.5px; font-weight: 750; }}
.desp-cuerpo {{ padding: 4px 14px 14px 14px; }}
.columna {{ border-radius: 16px; padding: 14px; background-color: alpha({f2}, 0.38); border: 1px solid alpha({borde}, 0.25); }}
.completo .vineta, .completo .desp-titulo {{ font-size: 17px; }}
.pie {{ font-size: 12.5px; color: {txt2}; padding: 0 20px 12px 20px; }}
.copiado {{ font-size: 13px; font-weight: 700; color: {pri}; }}
.vacio {{ font-size: 16px; color: {txt2}; margin: 40px; }}
.completo .p {{ font-size: 17px; }}
.completo .nota {{ font-size: 16.5px; }}
.completo .h2 {{ font-size: 27px; }}
.completo .h3 {{ font-size: 19.5px; }}
.completo .codigo, .completo .e-codigo {{ font-size: 15.5px; }}
.completo .e-exp, .completo .celda {{ font-size: 15.5px; }}
.completo .hoja-titulo {{ font-size: 38px; }}
.completo .hoja-sub {{ font-size: 18px; }}
"""


# --- tablas -----------------------------------------------------------------------------
# Gtk.Grid pide como alto mínimo el de sus celdas al ancho mínimo (una palabra por renglón):
# las tablas quedaban con huecos enormes debajo. Estas filas reparten el ancho por columnas
# según lo que mide el texto de cada una y piden exactamente el alto que necesitan.
class Columnas:
    """Anchos compartidos por todas las filas de una tabla."""
    def __init__(self):
        self.filas, self.medidas = [], None

    def medir(self):
        if self.medidas is None:
            n = max(len(f) for f in self.filas)
            mins, nats = [0] * n, [0] * n
            for fila in self.filas:
                for i, celda in enumerate(fila):
                    mn, nt, *_ = celda.measure(Gtk.Orientation.HORIZONTAL, -1)
                    mins[i], nats[i] = max(mins[i], mn), max(nats[i], nt)
            self.medidas = mins, nats
        return self.medidas

    def anchos(self, total):
        mins, nats = self.medir()
        if sum(nats) <= total:  # cabe todo: el sobrante, proporcional
            extra = total - sum(nats)
            return [nt + extra * nt // max(1, sum(nats)) for nt in nats]
        # no cabe: las columnas cortas se quedan con lo suyo y las largas se reparten el resto
        anchos, libres, resto = [0] * len(nats), set(range(len(nats))), total
        while libres:
            parte = resto / len(libres)
            cortas = [i for i in libres if nats[i] <= parte]
            if not cortas:
                for i in libres:
                    anchos[i] = max(mins[i], int(parte))
                break
            for i in cortas:
                anchos[i] = nats[i]
                resto -= nats[i]
                libres.discard(i)
        return anchos


class FilaLayout(Gtk.LayoutManager):
    def __init__(self, columnas):
        super().__init__()
        self.columnas = columnas

    def do_get_request_mode(self, _widget):
        return Gtk.SizeRequestMode.HEIGHT_FOR_WIDTH

    def celdas(self, widget):
        hijo, lista = widget.get_first_child(), []
        while hijo:
            lista.append(hijo)
            hijo = hijo.get_next_sibling()
        return lista

    def do_measure(self, widget, orientacion, para):
        mins, nats = self.columnas.medir()
        if orientacion == Gtk.Orientation.HORIZONTAL:
            return sum(mins), sum(nats), -1, -1
        anchos = self.columnas.anchos(para if para >= 0 else sum(nats))
        alto = max((c.measure(Gtk.Orientation.VERTICAL, a)[1] for c, a in zip(self.celdas(widget), anchos)),
                   default=0)
        return alto, alto, -1, -1

    def do_allocate(self, widget, ancho, alto, _base):
        x = 0
        for celda, a in zip(self.celdas(widget), self.columnas.anchos(ancho)):
            celda.allocate(a, alto, -1, Gsk.Transform().translate(Graphene.Point().init(x, 0)))
            x += a


class Panel(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.add_css_class("chuletas")
        LS.init_for_window(self)
        LS.set_namespace(self, "chuletas")
        LS.set_layer(self, LS.Layer.TOP)
        LS.set_keyboard_mode(self, LS.KeyboardMode.ON_DEMAND)  # puedes seguir escribiendo en tu editor
        self.vertical, self.ancho_mon = False, 1920
        try:
            info = next(m for m in hypr_json("monitors") if m["focused"])
            self.vertical = info.get("transform", 0) % 2 == 1
            self.ancho_mon = round((info["height"] if self.vertical else info["width"]) / info.get("scale", 1))
            mon = next((m for m in Gdk.Display.get_default().get_monitors()
                        if m.get_connector() == info["name"]), None)
            if mon:
                LS.set_monitor(self, mon)
        except (OSError, ValueError, StopIteration, KeyError):
            pass
        self.ancho_lateral = 520 if self.vertical else 640

        p, modo = paleta()
        claro = modo == "light"
        p = p or json.loads(PALETA_DEFECTO)
        t = p["terminal"]["normal"]
        f, f2 = p["mSurface"], p["mSurfaceVariant"]
        self.c = {"clave": t["magenta"], "txt": t["green"], "num": t["yellow"], "tag": t["red"], "prop": t["blue"],
                  "com": p["terminal"]["bright"]["black"],
                  "fondo_cod": mezclar(f, "#000000", 0.05) if claro else mezclar(f, "#000000", 0.32),
                  "cod_linea": t["blue"] if claro else t["cyan"]}
        self.col_dib = {"texto": p["mOnSurface"], "texto2": p["mOnSurfaceVariant"], "fondo": f,
                        "borde": p["mOutline"],
                        "acentos": [t["blue"], t["magenta"], t["cyan"], t["green"], t["yellow"], t["red"]]}
        self.generacion, self.pendiente = 0, iter(())  # generacion cambia al cambiar de hoja: cancela la construcción por partes anterior
        css = Gtk.CssProvider()
        css.load_from_string(hoja_css(p, claro, self.c))
        Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), css, 800)

        self.hojas = md.hojas()
        estado = leer_estado()
        nombres = [h["archivo"].name for h in self.hojas]
        self.hoja = nombres.index(estado["hoja"]) if estado.get("hoja") in nombres else 0
        self.modo = estado.get("modo", "lateral")
        self.busqueda = ""
        self.mostrado = False
        self.copiables, self.anclas = [], []
        self._indice, self._t_busqueda = None, 0
        self.construir()
        GLib.idle_add(lambda: self.indice_busqueda() and False, priority=GLib.PRIORITY_LOW)

        teclas = Gtk.EventControllerKey()
        teclas.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
        teclas.connect("key-pressed", self.tecla)
        self.add_controller(teclas)

    # --- estructura según el modo ------------------------------------------------------
    def colocar(self):
        completo = self.modo == "completo"
        for borde in (LS.Edge.TOP, LS.Edge.BOTTOM, LS.Edge.RIGHT, LS.Edge.LEFT):
            LS.set_anchor(self, borde, completo or borde != LS.Edge.LEFT)
            LS.set_margin(self, borde, 14 if completo else 8)
        LS.set_exclusive_zone(self, 0 if completo else self.ancho_lateral + 8)  # lateral: aparta las ventanas
        self.set_default_size(-1 if completo else self.ancho_lateral, -1)
        (self.add_css_class if completo else self.remove_css_class)("completo")

    def construir(self):
        self.colocar()
        completo = self.modo == "completo"
        self.caja = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL if completo else Gtk.Orientation.VERTICAL)
        self.caja.add_css_class("caja")
        if not self.mostrado:
            self.caja.add_css_class("oculta")

        cab = Gtk.Box(spacing=8)
        cab.add_css_class("cabecera")
        cab.append(etiqueta("📒 Chuletas", ("marca",), wrap=False))
        cab.append(Gtk.Box(hexpand=True))
        self.copiado = etiqueta("", ("copiado",), wrap=False)
        cab.append(self.copiado)
        b_modo = Gtk.Button(label="◧ Lateral" if completo else "⛶ Pantalla completa")
        b_modo.set_tooltip_text("F11: cambiar entre panel lateral y pantalla completa")
        b_modo.add_css_class("boton")
        b_modo.connect("clicked", lambda *_: self.cambiar_modo())
        b_cerrar = Gtk.Button(label="✕")
        b_cerrar.add_css_class("boton")
        b_cerrar.connect("clicked", lambda *_: self.cerrar())
        cab.append(b_modo)
        cab.append(b_cerrar)

        self.lbl_busqueda = etiqueta("", ("busqueda",), wrap=False)
        self.scroll = Gtk.ScrolledWindow(hscrollbar_policy=Gtk.PolicyType.NEVER, vexpand=True, hexpand=True)
        self.scroll.get_vadjustment().connect("value-changed", lambda *_: self.marcar_toc())
        pie = etiqueta("Escribe para buscar · Tab tema · Ctrl+↑↓ sección · clic copia · F11 modo · Esc cierra",
                       ("pie",))
        self.botones_hoja, self.botones_toc = [], []

        if completo:
            izq = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
            izq.add_css_class("lateral-izq")
            izq.set_size_request(320, -1)
            izq.append(etiqueta("TEMAS", ("nav-titulo",)))
            temas = Gtk.FlowBox(selection_mode=Gtk.SelectionMode.NONE, min_children_per_line=2,
                                max_children_per_line=2, homogeneous=True, row_spacing=2, column_spacing=2)
            for i, h in enumerate(self.hojas):  # dos columnas: caben ~20 temas y queda sitio para el índice
                b = Gtk.Button()
                b.set_child(etiqueta(corto(h["titulo"]), wrap=False))
                b.set_tooltip_text(h["titulo"])
                b.add_css_class("nav")
                b.connect("clicked", lambda _b, i=i: self.mostrar_hoja(i))
                temas.append(b)
                self.botones_hoja.append(b)
            izq.append(temas)
            izq.append(etiqueta("EN ESTE TEMA", ("nav-titulo",)))
            self.caja_toc = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
            toc_scroll = Gtk.ScrolledWindow(hscrollbar_policy=Gtk.PolicyType.NEVER, vexpand=True)
            toc_scroll.set_child(self.caja_toc)
            izq.append(toc_scroll)
            self.caja.append(izq)
            der = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12, hexpand=True)
            der.append(cab)
            centro = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12, halign=Gtk.Align.CENTER,
                             vexpand=True, margin_start=24, margin_end=24)
            centro.set_size_request(min(1000, self.ancho_mon - 290 - 120), -1)  # renglones cómodos de leer
            centro.append(self.lbl_busqueda)
            centro.append(self.scroll)
            der.append(centro)
            der.append(pie)
            self.caja.append(der)
        else:
            self.caja.set_spacing(10)
            self.caja.append(cab)
            # 21 temas no caben en una fila: un botón con el tema actual y una lista que se despliega
            self.menu_tema = Gtk.MenuButton(halign=Gtk.Align.FILL, margin_start=16, margin_end=16)
            self.menu_tema.add_css_class("selector-tema")
            self.menu_tema.set_direction(Gtk.ArrowType.DOWN)
            pop = Gtk.Popover()
            pop.add_css_class("selector-pop")
            fluir = Gtk.FlowBox(selection_mode=Gtk.SelectionMode.NONE, min_children_per_line=2,
                                max_children_per_line=3, homogeneous=True, column_spacing=2, row_spacing=2)
            for i, h in enumerate(self.hojas):
                b = Gtk.Button()
                b.set_child(etiqueta(corto(h["titulo"]), wrap=False))
                b.add_css_class("nav")
                b.connect("clicked", lambda _b, i=i, pop=pop: (pop.popdown(), self.mostrar_hoja(i)))
                fluir.append(b)
                self.botones_hoja.append(b)
            pop.set_child(fluir)
            self.menu_tema.set_popover(pop)
            self.caja.append(self.menu_tema)
            self.lbl_busqueda.set_margin_start(16)
            self.lbl_busqueda.set_margin_end(16)
            self.caja.append(self.lbl_busqueda)
            self.scroll.set_margin_start(16)
            self.scroll.set_margin_end(8)
            self.caja.append(self.scroll)
            self.caja.append(pie)
            self.caja_toc = None
        self.set_child(self.caja)
        self.mostrar_hoja(self.hoja)

    # --- contenido ----------------------------------------------------------------------
    def indice_busqueda(self):
        """Texto normalizado de cada bloque, calculado una sola vez (buscar en 49 000 líneas cada tecla era lento)."""
        if self._indice is None:
            self._indice = []
            for i, h in enumerate(self.hojas):
                for sec in h["secciones"]:
                    tit = sin_tildes(sec["titulo"] or "")
                    for b in sec["bloques"]:
                        if b[0] != "h3":
                            self._indice.append((i, sec, b, tit, sin_tildes(md.texto_de(b))))
        return self._indice

    def buscar_luego(self):
        """Agrupa las teclas rápidas: se busca cuando dejas de teclear 90 ms."""
        if self._t_busqueda:
            GLib.source_remove(self._t_busqueda)
        self.lbl_busqueda.set_label(f"🔍  {self.busqueda}")
        self.lbl_busqueda.add_css_class("activa")

        def hacer():
            self._t_busqueda = 0
            self.refrescar()
            return False
        self._t_busqueda = GLib.timeout_add(90, hacer)

    def copiable(self, caja, texto):
        k = len(self.copiables)
        self.copiables.append((caja, texto))
        return k

    def bloques_en(self, caja, bloques, leng):
        for b in self.agrupar(bloques):
            caja.append(self.bloque(b, leng))

    def bloque(self, b, leng_hoja):
        """Un bloque de chuletas_md → widget."""
        tipo = b[0]
        if tipo == "lista":
            caja = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
            caja.add_css_class("lista")
            for i, item in enumerate(b[1], 1):
                fila = Gtk.Box(spacing=6)
                fila.append(etiqueta(f"{i}." if b[2] else "•", ("vineta",), wrap=False))
                lbl = etiqueta(markup=en_linea(item, self.c), clases=("p",), seleccionable=True)
                lbl.set_hexpand(True)
                fila.append(lbl)
                caja.append(fila)
            return caja
        if tipo == "imagen":
            caja = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
            try:
                tex = Gdk.Texture.new_from_filename(b[2])
            except GLib.Error:
                return etiqueta(f"⚠️ No se pudo abrir la imagen {b[2]}", ("dibujo-error",))
            # Gtk.Picture no reserva alto propio dentro de una caja vertical: se lo damos según la proporción
            ancho = min(tex.get_width(), self.ancho_contenido() - 30, 900)
            foto = Gtk.Picture.new_for_paintable(tex)
            foto.set_can_shrink(True)
            foto.set_content_fit(Gtk.ContentFit.CONTAIN)
            foto.set_size_request(-1, round(tex.get_height() * ancho / tex.get_width()))
            foto.add_css_class("imagen")
            caja.append(foto)
            if b[1]:
                pie = etiqueta(b[1], ("pie-img",))
                pie.set_xalign(0.5)
                caja.append(pie)
            return caja
        if tipo == "desplegable":  # el contenido se construye al abrirlo (abre más rápido la hoja)
            exp = Gtk.Expander()
            exp.add_css_class("desplegable")
            exp.set_label_widget(etiqueta(b[1], ("desp-titulo",)))
            exp.set_cursor(Gdk.Cursor.new_from_name("pointer"))

            def abrir(e, _p=None):
                if e.get_expanded() and e.get_child() is None:
                    cuerpo = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
                    cuerpo.add_css_class("desp-cuerpo")
                    self.bloques_en(cuerpo, b[2], leng_hoja)
                    e.set_child(cuerpo)
            exp.connect("notify::expanded", abrir)
            if self.busqueda:
                exp.set_expanded(True)
            return exp
        if tipo == "columnas":
            fila = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL if self.modo == "completo" else
                           Gtk.Orientation.VERTICAL, spacing=14, homogeneous=self.modo == "completo")
            for col in b[1]:
                caja = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10, hexpand=True)
                caja.add_css_class("columna")
                self.bloques_en(caja, col, leng_hoja)
                fila.append(caja)
            return fila
        if tipo == "codigo" and b[1] in md.DIBUJOS:
            return self.dibujo(b[1], b[2])
        if tipo == "p":
            return etiqueta(markup=en_linea(b[1], self.c), clases=("p",), seleccionable=True)
        if tipo == "h3":
            return etiqueta(b[1], ("h3",))
        if tipo == "nota":
            caja = Gtk.Box()
            caja.add_css_class("nota")
            caja.add_css_class(f"nota-{b[1]}")
            texto = etiqueta(markup=en_linea(b[2], self.c), seleccionable=True)
            texto.set_hexpand(True)  # sin esto el renglón largo no se parte y se sale de la caja
            caja.append(texto)
            return caja
        if tipo == "entrada":
            caja = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            caja.add_css_class("entrada")
            caja.append(etiqueta(markup=resaltar(b[1], leng_hoja, self.c), clases=("e-codigo",)))
            caja.append(etiqueta(markup=en_linea(b[2], self.c), clases=("e-exp",)))
            k = self.copiable(caja, b[1])
            clic = Gtk.GestureClick()
            clic.connect("released", lambda *_a: self.copiar(k))
            caja.add_controller(clic)
            caja.set_cursor(Gdk.Cursor.new_from_name("pointer"))
            return caja
        if tipo == "codigo":
            caja = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            caja.add_css_class("bloque")
            cab = Gtk.Box()
            cab.add_css_class("bloque-cab")
            cab.append(etiqueta(b[1].upper(), ("leng",), wrap=False))
            cab.append(Gtk.Box(hexpand=True))
            k = self.copiable(caja, b[2])
            boton = Gtk.Button(label="📋 Copiar")
            boton.add_css_class("copiar")
            boton.connect("clicked", lambda *_a: self.copiar(k))
            cab.append(boton)
            caja.append(cab)
            caja.append(etiqueta(markup=resaltar(b[2], b[1], self.c), clases=("codigo",), seleccionable=True))
            return caja
        if tipo == "tabla":
            return self.tabla([[etiqueta(markup=en_linea(c, self.c), clases=("celda",), seleccionable=True)
                                for c in fila] for fila in b[1]], cabecera=True)
        if tipo == "entradas":  # varias entradas rápidas seguidas → tabla código | explicación
            filas = [[etiqueta(markup=resaltar(cod, leng_hoja, self.c), clases=("celda", "e-codigo")),
                      etiqueta(markup=en_linea(exp, self.c), clases=("celda", "e-exp"))] for cod, exp in b[1]]
            return self.tabla(filas, copiar=[cod for cod, _e in b[1]])
        return etiqueta(str(b))

    def ancho_contenido(self):
        if self.modo == "completo":
            return min(1000, self.ancho_mon - 290 - 120) - 10
        return self.ancho_lateral - 50

    def dibujo(self, tipo, cuerpo):
        caja = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        caja.add_css_class("dibujo")
        try:
            d = dib.analizar(tipo, cuerpo)
        except ValueError as e:
            caja.append(etiqueta(f"⚠️ ```{tipo}: {e}", ("dibujo-error",)))
            return caja
        area = Gtk.DrawingArea(hexpand=True)
        area.set_content_height(d.alto(self.ancho_contenido() - 34))

        def pintar(_a, cr, ancho, _alto):
            try:
                d.pintar(cr, ancho, self.col_dib)
            except Exception as e:  # noqa: BLE001 — un dibujo roto no debe tumbar el panel
                print("dibujo:", e)

        def al_cambiar(a, ancho, _alto):
            h = d.alto(ancho)
            if h != a.get_content_height():
                a.set_content_height(h)
        area.set_draw_func(pintar)
        area.connect("resize", al_cambiar)
        caja.append(area)
        return caja

    def tabla(self, filas, cabecera=False, copiar=None):
        """Filas de etiquetas → tabla con columnas alineadas. copiar = código que copia cada fila al hacer clic."""
        marco = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        marco.add_css_class("tabla")
        marco.set_overflow(Gtk.Overflow.HIDDEN)
        columnas = Columnas()
        for r, celdas in enumerate(filas):
            fila = Gtk.Box()
            fila.set_layout_manager(FilaLayout(columnas))
            fila.add_css_class("fila")
            if cabecera and r == 0:
                fila.add_css_class("cab")
            elif (r % 2 == 0) == cabecera:
                fila.add_css_class("par")
            for i, celda in enumerate(celdas):
                if i:
                    celda.add_css_class("con-borde")
                fila.append(celda)
            columnas.filas.append(celdas)
            if copiar:
                k = self.copiable(fila, copiar[r])
                clic = Gtk.GestureClick()
                clic.connect("released", lambda *_a, k=k: self.copiar(k))
                fila.add_controller(clic)
                fila.set_cursor(Gdk.Cursor.new_from_name("pointer"))
                fila.add_css_class("copiable")
            marco.append(fila)
        return marco

    @staticmethod
    def agrupar(bloques):
        """Junta las entradas rápidas seguidas en un solo bloque «entradas» (se dibuja como tabla)."""
        salida = []
        for b in bloques:
            if b[0] == "entrada":
                if salida and salida[-1][0] == "entradas":
                    salida[-1][1].append(b[1:])
                else:
                    salida.append(("entradas", [b[1:]]))
            else:
                salida.append(b)
        return salida

    @staticmethod
    def lenguaje_hoja(hoja):
        """Lenguaje de las entradas rápidas de la hoja (los bloques ``` dicen el suyo)."""
        nombre = hoja["archivo"].stem
        for clave, leng in (("python", "python"), ("javascript", "js"), ("node", "js"), ("react", "jsx"),
                            ("css", "css"), ("html", "html"), ("sql", "sql")):
            if clave in nombre:
                return leng
        return "bash"

    def mostrar_hoja(self, i):
        if not self.hojas:
            self.refrescar()
            return
        self.hoja = i
        guardar_estado({"hoja": self.hojas[i]["archivo"].name, "modo": self.modo})
        for k, b in enumerate(self.botones_hoja):
            (b.add_css_class if k == i else b.remove_css_class)("activa")
        if getattr(self, "menu_tema", None) is not None and self.modo != "completo":
            self.menu_tema.set_label(f"{corto(self.hojas[i]['titulo'])}   ▾  cambiar de tema (Tab)")
        self.refrescar()

    def refrescar(self):
        """Sin búsqueda: el tema elegido entero. Con búsqueda: lo que coincida en TODOS los temas."""
        if self.busqueda:
            self.lbl_busqueda.set_label(f"🔍  {self.busqueda}")
            self.lbl_busqueda.add_css_class("activa")
        else:
            self.lbl_busqueda.set_label("🔍  Escribe para buscar en todos los temas (ej. «flex», «commit», «queue»)")
            self.lbl_busqueda.remove_css_class("activa")
        contenido = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10, margin_end=10, margin_bottom=30)
        self.copiables, self.anclas = [], []
        self.generacion += 1
        self.pendiente = iter(())
        q = sin_tildes(self.busqueda)
        if not self.hojas:
            contenido.append(etiqueta(f"No hay chuletas en {md.CARPETA}", ("vacio",)))
        elif q:
            encontrados, ultima = 0, None
            for i, sec, bl, tit, txt in self.indice_busqueda():
                if q not in txt and not (q in tit and bl is sec["bloques"][0]):
                    continue
                if encontrados >= (120 if len(q) >= 3 else 25):  # 1-2 letras: pocos, para que sea inmediato
                    break
                if ultima is not sec:
                    contenido.append(etiqueta(f"{self.hojas[i]['titulo']}  ›  {sec['titulo'] or ''}", ("h3",)))
                    ultima = sec
                for pieza in self.agrupar([bl]):
                    contenido.append(self.bloque(pieza, self.lenguaje_hoja(self.hojas[i])))
                encontrados += 1
            if not encontrados:
                contenido.append(etiqueta("Nada con esa búsqueda 🙂 Prueba otra palabra (también en inglés).",
                                          ("vacio",)))
        else:
            h = self.hojas[self.hoja]
            contenido.append(etiqueta(h["titulo"], ("hoja-titulo",)))
            if h["subtitulo"]:
                contenido.append(etiqueta(markup=en_linea(h["subtitulo"], self.c), clases=("hoja-sub",)))
            self.anclas = [[None, sec["titulo"]] for sec in h["secciones"] if sec["titulo"]]
            self.pendiente = self.piezas(h)
        self.contenido = contenido
        self.scroll.set_child(contenido)
        self.scroll.get_vadjustment().set_value(0)
        self.llenar_toc()
        if not q and self.hojas:
            # lo primero que se ve, ya; el resto en ratos libres (la hoja abre al instante y no se traba)
            self.generacion += 1
            self.construir_hasta(limite=40)
            GLib.idle_add(self.construir_resto, self.generacion, priority=GLib.PRIORITY_LOW)

    def piezas(self, h):
        leng = self.lenguaje_hoja(h)
        k = 0
        for sec in h["secciones"]:
            if sec["titulo"]:
                yield ("h2", k, sec["titulo"])
                k += 1
            for b in self.agrupar(sec["bloques"]):
                yield ("bloque", b, leng)

    def construir_hasta(self, basta=lambda: False, limite=None):
        """Añade piezas pendientes hasta que basta() o se acaben. → True si quedan."""
        hechas = 0
        for pieza in self.pendiente:
            if pieza[0] == "h2":
                titulo = etiqueta(pieza[2], ("h2",))
                self.contenido.append(titulo)
                self.anclas[pieza[1]][0] = titulo
            else:
                self.contenido.append(self.bloque(pieza[1], pieza[2]))
            hechas += 1
            if basta() or (limite and hechas >= limite):
                return True
        return False

    def construir_resto(self, gen):
        if gen != self.generacion:
            return False
        t0 = time.monotonic()
        quedan = self.construir_hasta(lambda: time.monotonic() - t0 > 0.012)
        return quedan

    def terminar_construccion(self):
        self.generacion += 1
        self.construir_hasta()

    def llenar_toc(self):
        if self.caja_toc is None:
            return
        while (hijo := self.caja_toc.get_first_child()):
            self.caja_toc.remove(hijo)
        self.botones_toc = []
        for k, (_w, titulo) in enumerate(self.anclas):
            b = Gtk.Button()
            b.set_child(etiqueta(titulo))
            b.add_css_class("toc")
            b.connect("clicked", lambda _b, k=k: self.ir_a_seccion(k))
            self.caja_toc.append(b)
            self.botones_toc.append(b)
        GLib.idle_add(self.marcar_toc)

    def y_de(self, widget):
        ok, caja = widget.compute_bounds(self.contenido)
        return caja.get_y() if ok else 0

    def ir_a_seccion(self, k):
        if not 0 <= k < len(self.anclas):
            return
        if self.anclas[k][0] is None:  # aún no construida: se construye y se salta tras medirla
            self.construir_hasta(lambda: self.anclas[k][0] is not None)
            GLib.timeout_add(40, lambda: self.ir_a_seccion(k) and False)
            return
        self.scroll.get_vadjustment().set_value(max(0, self.y_de(self.anclas[k][0]) - 10))

    def seccion_actual(self):
        valor = self.scroll.get_vadjustment().get_value() + 40
        actual = 0
        for k, (w, _t) in enumerate(self.anclas):
            if w is not None and self.y_de(w) <= valor:
                actual = k
        return actual

    def marcar_toc(self):
        if self.botones_toc:
            k = self.seccion_actual()
            for j, b in enumerate(self.botones_toc):
                (b.add_css_class if j == k else b.remove_css_class)("activa")
        return False

    # --- acciones -----------------------------------------------------------------------
    def copiar(self, k):
        if not 0 <= k < len(self.copiables):
            return
        caja, codigo = self.copiables[k]
        subprocess.Popen(["wl-copy", "--", codigo], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        caja.add_css_class("copiada")
        self.copiado.set_label("Copiado ✓")

        def limpiar():
            self.copiado.set_label("")
            caja.remove_css_class("copiada")
            return False
        GLib.timeout_add(1500, limpiar)

    def cambiar_modo(self):
        self.modo = "lateral" if self.modo == "completo" else "completo"
        self.construir()

    def mostrar(self):
        self.present()

        def aparecer():
            self.mostrado = True
            self.caja.remove_css_class("oculta")
            return False
        GLib.timeout_add(30, aparecer)

    def cerrar(self):
        self.caja.add_css_class("oculta")
        LS.set_exclusive_zone(self, 0)
        GLib.timeout_add(230, lambda: self.get_application().quit() or False)

    def desplazar(self, dy=0, pagina=0, extremo=None):
        adj = self.scroll.get_vadjustment()
        if extremo == "inicio":
            adj.set_value(0)
        elif extremo == "fin":
            self.terminar_construccion()
            GLib.timeout_add(60, lambda: adj.set_value(adj.get_upper()) or False)
        else:
            adj.set_value(adj.get_value() + dy + pagina * adj.get_page_size() * 0.9)

    def tecla(self, _ctl, keyval, _code, estado):
        nombre = Gdk.keyval_name(keyval) or ""
        ctrl = estado & Gdk.ModifierType.CONTROL_MASK
        n = len(self.hojas)
        if nombre == "Escape":
            if self.busqueda:
                self.busqueda = ""
                self.refrescar()
            else:
                self.cerrar()
        elif nombre == "F11":
            self.cambiar_modo()
        elif nombre in ("Tab", "ISO_Left_Tab") and n:
            self.busqueda = ""
            self.mostrar_hoja((self.hoja + (-1 if nombre == "ISO_Left_Tab" else 1)) % n)
        elif ctrl and nombre in ("Down", "Up"):
            self.ir_a_seccion(self.seccion_actual() + (1 if nombre == "Down" else -1))
        elif nombre in ("Down", "Up"):
            self.desplazar(dy=70 if nombre == "Down" else -70)
        elif nombre in ("Page_Down", "Page_Up"):
            self.desplazar(pagina=1 if nombre == "Page_Down" else -1)
        elif nombre in ("Home", "End"):
            self.desplazar(extremo="inicio" if nombre == "Home" else "fin")
        elif nombre in ("Return", "KP_Enter"):
            if self.busqueda and self.copiables:
                self.copiar(0)
        elif nombre == "BackSpace":
            if self.busqueda:
                self.busqueda = self.busqueda[:-1]
                self.buscar_luego() if self.busqueda else self.refrescar()
        elif estado & (Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.ALT_MASK | Gdk.ModifierType.SUPER_MASK):
            return False  # Ctrl+C sobre texto seleccionado, etc.
        else:
            ch = chr(Gdk.keyval_to_unicode(keyval) or 0)
            if ch.isprintable() and (ch.strip() or self.busqueda):
                self.busqueda += ch
                self.buscar_luego()
            else:
                return False
        return True


class App(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="dev.yafer.Chuletas")  # única: SUPER+SHIFT+C otra vez la cierra

    def do_activate(self):
        if self.get_windows():
            self.get_windows()[0].cerrar()
            return
        Panel(self).mostrar()


if __name__ == "__main__":
    App().run(None)
