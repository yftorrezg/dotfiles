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

import chuletas_md as md  # noqa: E402

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
gi.require_version("Gtk4LayerShell", "1.0")
from gi.repository import Gdk, GLib, Gtk, Pango  # noqa: E402
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
}
ALIAS = {"py": "python", "javascript": "js", "typescript": "ts", "tsx": "jsx", "sh": "bash", "shell": "bash",
         "fish": "bash", "console": "bash", "docker": "dockerfile", "yml": "yaml", "postgres": "sql"}
COMENTARIO = {"python": r"#.*$", "bash": r"#.*$", "dockerfile": r"#.*$", "yaml": r"#.*$",
              "js": r"//.*$|/\*.*?\*/", "jsx": r"//.*$|/\*.*?\*/", "ts": r"//.*$|/\*.*?\*/",
              "css": r"/\*.*?\*/", "sql": r"--.*$", "html": r"<!--.*?-->", "json": r"(?!x)x", "text": r"(?!x)x"}


def _patron(leng):
    etiqueta_html = r"|(?P<tag></?[A-Za-z][\w.-]*>?|/?>)" if leng in ("html", "jsx") else ""
    clave_yaml = r"|(?P<prop>^\s*[\w.-]+(?=:))" if leng == "yaml" else ""
    prop_css = r"|(?P<prop>[\w-]+(?=\s*:[^:]))" if leng == "css" else ""
    return re.compile(rf"""(?P<com>{COMENTARIO[leng]}){etiqueta_html}{clave_yaml}{prop_css}"""
                      r"""|(?P<txt>"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|`[^`]*`)"""
                      r"""|(?P<num>\b\d+(?:\.\d+)?(?:px|rem|em|ms|s|fr|vh|vw|%)?\b)|(?P<pal>[@!]?[A-Za-z_][\w-]*)|(?P<otro>.)""",
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
    """Markdown mínimo de los párrafos: `código` y **negrita** → Pango markup."""
    salida = []
    for p in re.split(r"(`[^`]+`)", texto):
        if p.startswith("`") and p.endswith("`") and len(p) > 1:
            salida.append(f'<span font_family="{MONO}" background="{c["fondo_cod"]}" foreground="{c["cod_linea"]}">'
                          f' {html.escape(p[1:-1])} </span>')
        else:
            salida.append(re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", html.escape(p)))
    return "".join(salida)


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
    notas = {"consejo": t["green"], "cuidado": t["red"] if claro else t["yellow"], "ingles": t["blue"], "nota": pri}
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
.nav {{ font-size: 15.5px; font-weight: 650; padding: 8px 12px; border-radius: 12px; min-height: 0;
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
.tabla {{ border-radius: 14px; border: 1px solid alpha({borde}, 0.4); }}
.celda {{ padding: 7px 12px; font-size: 14.5px; }}
.celda.cab {{ font-weight: 800; background-color: alpha({pri}, 0.16); }}
.celda.par {{ background-color: alpha({f2}, 0.55); }}
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
        self.construir()

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
            izq.set_size_request(290, -1)
            izq.append(etiqueta("TEMAS", ("nav-titulo",)))
            for i, h in enumerate(self.hojas):
                b = Gtk.Button()
                b.set_child(etiqueta(h["titulo"], wrap=False))
                b.add_css_class("nav")
                b.connect("clicked", lambda _b, i=i: self.mostrar_hoja(i))
                izq.append(b)
                self.botones_hoja.append(b)
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
            fluir = Gtk.FlowBox(selection_mode=Gtk.SelectionMode.NONE, max_children_per_line=8,
                                column_spacing=2, row_spacing=4, margin_start=16, margin_end=16)
            for i, h in enumerate(self.hojas):
                b = Gtk.Button(label=h["titulo"])
                b.add_css_class("pestana")
                b.connect("clicked", lambda _b, i=i: self.mostrar_hoja(i))
                fluir.append(b)
                self.botones_hoja.append(b)
            self.caja.append(fluir)
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
    def copiable(self, caja, texto):
        k = len(self.copiables)
        self.copiables.append((caja, texto))
        return k

    def bloque(self, b, leng_hoja):
        """Un bloque de chuletas_md → widget."""
        tipo = b[0]
        if tipo == "p":
            return etiqueta(markup=en_linea(b[1], self.c), clases=("p",), seleccionable=True)
        if tipo == "h3":
            return etiqueta(b[1], ("h3",))
        if tipo == "nota":
            caja = Gtk.Box()
            caja.add_css_class("nota")
            caja.add_css_class(f"nota-{b[1]}")
            caja.append(etiqueta(markup=en_linea(b[2], self.c), seleccionable=True))
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
            marco = Gtk.Box()
            marco.add_css_class("tabla")
            marco.set_overflow(Gtk.Overflow.HIDDEN)
            grid = Gtk.Grid(hexpand=True)
            for r, fila in enumerate(b[1]):
                for col, celda in enumerate(fila):
                    lbl = etiqueta(markup=en_linea(celda, self.c), clases=("celda",), seleccionable=True)
                    lbl.set_hexpand(True)
                    if r == 0:
                        lbl.add_css_class("cab")
                    elif r % 2 == 0:
                        lbl.add_css_class("par")
                    grid.attach(lbl, col, r, 1, 1)
            marco.append(grid)
            return marco
        return etiqueta(str(b))

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
        q = sin_tildes(self.busqueda)
        if not self.hojas:
            contenido.append(etiqueta(f"No hay chuletas en {md.CARPETA}", ("vacio",)))
        elif q:
            encontrados = 0
            for h in self.hojas:
                leng = self.lenguaje_hoja(h)
                for sec in h["secciones"]:
                    titulo_sec = sec["titulo"] or ""
                    coinciden = [b for b in sec["bloques"] if b[0] != "h3" and q in sin_tildes(md.texto_de(b))]
                    if not coinciden and q in sin_tildes(titulo_sec):
                        coinciden = sec["bloques"][:6]
                    if not coinciden or encontrados > 120:
                        continue
                    contenido.append(etiqueta(f"{h['titulo']}  ›  {titulo_sec}", ("h3",)))
                    for b in coinciden:
                        contenido.append(self.bloque(b, leng))
                        encontrados += 1
            if not encontrados:
                contenido.append(etiqueta("Nada con esa búsqueda 🙂 Prueba otra palabra (también en inglés).",
                                          ("vacio",)))
        else:
            h = self.hojas[self.hoja]
            leng = self.lenguaje_hoja(h)
            contenido.append(etiqueta(h["titulo"], ("hoja-titulo",)))
            if h["subtitulo"]:
                contenido.append(etiqueta(markup=en_linea(h["subtitulo"], self.c), clases=("hoja-sub",)))
            for sec in h["secciones"]:
                if sec["titulo"]:
                    titulo = etiqueta(sec["titulo"], ("h2",))
                    contenido.append(titulo)
                    self.anclas.append((titulo, sec["titulo"]))
                for b in sec["bloques"]:
                    contenido.append(self.bloque(b, leng))
        self.scroll.set_child(contenido)
        self.scroll.get_vadjustment().set_value(0)
        self.llenar_toc()

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
        ok, caja = widget.compute_bounds(self.scroll.get_child())
        return caja.get_y() if ok else 0

    def ir_a_seccion(self, k):
        if 0 <= k < len(self.anclas):
            self.scroll.get_vadjustment().set_value(max(0, self.y_de(self.anclas[k][0]) - 10))

    def seccion_actual(self):
        valor = self.scroll.get_vadjustment().get_value() + 40
        actual = 0
        for k, (w, _t) in enumerate(self.anclas):
            if self.y_de(w) <= valor:
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
            adj.set_value(adj.get_upper())
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
                self.refrescar()
        elif estado & (Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.ALT_MASK | Gdk.ModifierType.SUPER_MASK):
            return False  # Ctrl+C sobre texto seleccionado, etc.
        else:
            ch = chr(Gdk.keyval_to_unicode(keyval) or 0)
            if ch.isprintable() and (ch.strip() or self.busqueda):
                self.busqueda += ch
                self.refrescar()
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
