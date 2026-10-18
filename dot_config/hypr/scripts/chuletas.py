#!/usr/bin/env python3
"""chuletas.py — chuletas de programación en un panel lateral (SUPER+SHIFT+C).

Lee ~/.config/hypr/chuletas/*.md (una pestaña por archivo). Formato de cada archivo:
  # 🐍 Título            ← nombre de la pestaña
  ## Sección
  código :: explicación   ← una línea por entrada (edítalas o añade las tuyas)

El panel reserva su espacio a la derecha: las ventanas se apartan, no las tapa (puedes
programar con la chuleta abierta). Usa los colores del esquema activo de noctalia, así que
combina con tu tema y en modo claro/oscuro sigue leyéndose bien.
Teclas: escribe para buscar · Tab / Shift+Tab pestaña · ↑↓ elegir · Enter o clic copia ·
Esc borra la búsqueda o cierra. SUPER+SHIFT+C otra vez también lo cierra.
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

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
gi.require_version("Gtk4LayerShell", "1.0")
from gi.repository import Gdk, GLib, Gtk, Pango  # noqa: E402
from gi.repository import Gtk4LayerShell as LS  # noqa: E402

CARPETA = Path.home() / ".config/hypr/chuletas"
NOCT_SETTINGS = Path.home() / ".local/state/noctalia/settings.toml"
PALETAS = Path.home() / ".config/noctalia/palettes"
HYPR = Path(os.environ["XDG_RUNTIME_DIR"]) / "hypr" / os.environ["HYPRLAND_INSTANCE_SIGNATURE"] / ".socket.sock"
ANCHO = 600

PALABRAS = {  # se colorean como palabras clave (lo demás: textos, números y comentarios)
    "py": "def class return if elif else for while in not and or import from as with try except finally raise "
          "lambda yield None True False pass break continue is async await",
    "js": "const let var function return if else for of in while switch case default break new class extends "
          "async await try catch finally import export from typeof null undefined true false this",
    "css": "display flex grid position color background margin padding border gap font width height transition "
           "transform animation content",
    "sql": "SELECT FROM WHERE AND OR IN LIKE BETWEEN ORDER BY DESC ASC LIMIT GROUP HAVING JOIN LEFT ON INSERT "
           "INTO VALUES UPDATE SET DELETE CREATE TABLE ALTER ADD COLUMN INDEX DROP DISTINCT COUNT AVG MAX AS "
           "PRIMARY KEY NOT NULL INTEGER TEXT INT",
    "sh": "git sudo cd ls cat grep find rm cp mv mkdir pip npm node python gh chmod kill pkill",
}


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


def sin_tildes(texto):
    return unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().casefold()


def leer_chuletas():
    hojas = []
    for archivo in sorted(CARPETA.glob("*.md")):
        titulo, secciones, actual = archivo.stem, [], None
        for linea in archivo.read_text(encoding="utf-8").splitlines():
            if linea.startswith("## "):
                actual = (linea[3:].strip(), [])
                secciones.append(actual)
            elif linea.startswith("# "):
                titulo = linea[2:].strip()
            elif actual is not None and " :: " in linea:
                codigo, explicacion = linea.rsplit(" :: ", 1)
                actual[1].append((codigo.strip(), explicacion.strip()))
        lenguaje = next((k for k, pista in (("py", "python"), ("js", "javascript"), ("css", "css"),
                                             ("sql", "sql")) if pista in archivo.stem), "sh")
        hojas.append({"titulo": titulo, "secciones": secciones, "lenguaje": lenguaje})
    return hojas


COMENTARIO = {"py": r"#\s.*$", "sh": r"#\s.*$", "js": r"//\s.*$", "css": r"/\*.*?\*/", "sql": r"--\s.*$"}
TOKEN = {leng: re.compile(rf"""(?P<com>{com})|(?P<txt>"[^"]*"|'[^']*'|`[^`]*`)|"""
                          r"""(?P<num>\b\d+(?:\.\d+)?(?:px|rem|ms|s|fr|%)?\b)|(?P<pal>[A-Za-z_][\w-]*)|(?P<otro>.)""")
         for leng, com in COMENTARIO.items()}


def resaltar(codigo, lenguaje, c):
    """Colorea el código con Pango markup (simple: palabras clave, textos, números, comentarios)."""
    claves = set(PALABRAS[lenguaje].split())
    partes = []
    for m in TOKEN[lenguaje].finditer(codigo):
        t = html.escape(m.group())
        if m.lastgroup == "com":
            partes.append(f'<span foreground="{c["com"]}">{t}</span>')
        elif m.lastgroup == "txt":
            partes.append(f'<span foreground="{c["txt"]}">{t}</span>')
        elif m.lastgroup == "num":
            partes.append(f'<span foreground="{c["num"]}">{t}</span>')
        elif m.lastgroup == "pal" and m.group() in claves:
            partes.append(f'<span foreground="{c["clave"]}" weight="bold">{t}</span>')
        else:
            partes.append(t)
    return "".join(partes)


class Panel(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.add_css_class("chuletas")
        LS.init_for_window(self)
        LS.set_namespace(self, "chuletas")
        LS.set_layer(self, LS.Layer.TOP)
        LS.set_keyboard_mode(self, LS.KeyboardMode.ON_DEMAND)  # puedes seguir escribiendo en tu editor
        for borde in (LS.Edge.TOP, LS.Edge.BOTTOM, LS.Edge.RIGHT):
            LS.set_anchor(self, borde, True)
        for borde, m in ((LS.Edge.TOP, 8), (LS.Edge.BOTTOM, 8), (LS.Edge.RIGHT, 8)):
            LS.set_margin(self, borde, m)
        ancho = ANCHO
        try:
            info = next(m for m in hypr_json("monitors") if m["focused"])
            if info.get("transform", 0) % 2 == 1:  # monitor vertical: más angosto
                ancho = 500
            mon = next((m for m in Gdk.Display.get_default().get_monitors()
                        if m.get_connector() == info["name"]), None)
            if mon:
                LS.set_monitor(self, mon)
        except (OSError, ValueError, StopIteration):
            pass
        LS.set_exclusive_zone(self, ancho + 8)  # las ventanas se apartan
        self.set_default_size(ancho, -1)

        p, modo = paleta()
        claro = modo == "light"
        p = p or {"mSurface": "#1a1c23", "mSurfaceVariant": "#2b2e3b", "mOnSurface": "#f2f2f3",
                  "mOnSurfaceVariant": "#b4b5bd", "mPrimary": "#8fa0ec", "mOnPrimary": "#16161c",
                  "mOutline": "#61677a", "terminal": {"normal": {"green": "#8fd18a", "yellow": "#f2c46d",
                                                                 "magenta": "#c79bf2", "blue": "#82aaff"},
                                                      "bright": {"black": "#70758a"}}}
        t = p["terminal"]
        self.c = {"clave": t["normal"]["magenta"], "txt": t["normal"]["green"], "num": t["normal"]["yellow"],
                  "com": t["bright"]["black"], "codigo": p["mOnSurface"]}
        css = Gtk.CssProvider()
        css.load_from_string(f"""
window.chuletas {{ background: transparent; }}
.caja {{ background-color: alpha({p['mSurface']}, 0.97); color: {p['mOnSurface']};
        border-radius: 26px; border: 1px solid alpha({p['mOutline']}, 0.45);
        padding: 20px 18px 14px 20px; font-family: "Adwaita Sans", "Inter", sans-serif;
        box-shadow: 0 16px 50px rgba(0,0,0,{0.18 if claro else 0.45});
        transition: opacity 220ms ease, transform 300ms cubic-bezier(.2,1.2,.3,1); }}
.caja.oculta {{ opacity: 0; transform: translateX(40px); }}
.titulo {{ font-size: 24px; font-weight: 800; }}
.pestana {{ font-size: 14.5px; font-weight: 700; padding: 6px 12px; border-radius: 99px; min-height: 0;
           background: transparent; color: {p['mOnSurfaceVariant']}; border: none; box-shadow: none; }}
.pestana:hover {{ background-color: {p['mSurfaceVariant']}; }}
.pestana.activa {{ background-color: {p['mPrimary']}; color: {p['mOnPrimary']}; }}
.busqueda {{ font-size: 15px; font-weight: 600; padding: 8px 14px; border-radius: 14px;
            background-color: {p['mSurfaceVariant']}; color: {p['mOnSurfaceVariant']}; }}
.busqueda.activa {{ color: {p['mOnSurface']}; }}
scrolledwindow, scrolledwindow > viewport {{ background: transparent; }}
.seccion {{ font-size: 13px; font-weight: 800; letter-spacing: 1.5px; color: {p['mPrimary']};
           margin: 16px 4px 6px 4px; }}
.entrada {{ padding: 10px 14px; border-radius: 14px; background-color: alpha({p['mSurfaceVariant']}, 0.55);
           margin: 0 6px 6px 0; border: 1px solid transparent; }}
.entrada:hover {{ background-color: {p['mSurfaceVariant']}; }}
.entrada.sel {{ background-color: {p['mSurfaceVariant']}; border-color: {p['mPrimary']}; }}
.codigo {{ font-family: "Adwaita Mono", "JetBrains Mono", monospace; font-size: 15px; color: {p['mOnSurface']}; }}
.explicacion {{ font-size: 14px; color: {p['mOnSurfaceVariant']}; margin-top: 3px; }}
.hoja {{ font-size: 12.5px; font-weight: 700; color: {p['mPrimary']}; }}
.pie {{ font-size: 12.5px; color: {p['mOnSurfaceVariant']}; }}
.copiado {{ font-size: 13px; font-weight: 700; color: {p['mPrimary']}; }}
""")
        Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), css, 800)

        self.hojas = leer_chuletas()
        self.hoja = 0
        self.busqueda = ""
        self.caja = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.caja.add_css_class("caja")
        self.caja.add_css_class("oculta")
        cab = Gtk.Box(spacing=8)
        titulo = Gtk.Label(label="📒 Chuletas", xalign=0, hexpand=True)
        titulo.add_css_class("titulo")
        cab.append(titulo)
        self.copiado = Gtk.Label(label="")
        self.copiado.add_css_class("copiado")
        cab.append(self.copiado)
        self.caja.append(cab)
        pestanas = Gtk.FlowBox(selection_mode=Gtk.SelectionMode.NONE, max_children_per_line=6,
                               column_spacing=2, row_spacing=4, homogeneous=False)
        self.botones = []
        for i, h in enumerate(self.hojas):
            b = Gtk.Button(label=h["titulo"])
            b.add_css_class("pestana")
            b.connect("clicked", lambda _b, i=i: self.mostrar_hoja(i))
            pestanas.append(b)
            self.botones.append(b)
        self.caja.append(pestanas)
        self.lbl_busqueda = Gtk.Label(xalign=0)
        self.lbl_busqueda.add_css_class("busqueda")
        self.caja.append(self.lbl_busqueda)
        self.scroll = Gtk.ScrolledWindow(hscrollbar_policy=Gtk.PolicyType.NEVER, vexpand=True)
        self.caja.append(self.scroll)
        pie = Gtk.Label(label="Escribe para buscar · Tab cambia · ↑↓ elegir · Enter/clic copia · Esc cierra",
                        xalign=0, wrap=True)
        pie.add_css_class("pie")
        self.caja.append(pie)
        self.set_child(self.caja)

        teclas = Gtk.EventControllerKey()
        teclas.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
        teclas.connect("key-pressed", self.tecla)
        self.add_controller(teclas)
        self.mostrar_hoja(0)

    def mostrar_hoja(self, i):
        self.hoja = i
        for k, b in enumerate(self.botones):
            (b.add_css_class if k == i else b.remove_css_class)("activa")
        self.refrescar()

    def refrescar(self):
        """Sin búsqueda: la pestaña elegida. Con búsqueda: lo que coincida en TODAS las pestañas."""
        if self.busqueda:
            self.lbl_busqueda.set_label(f"🔍  {self.busqueda}")
            self.lbl_busqueda.add_css_class("activa")
        else:
            self.lbl_busqueda.set_label("🔍  Escribe para buscar en todas (ej. «lista», «flex», «commit»)")
            self.lbl_busqueda.remove_css_class("activa")
        q = sin_tildes(self.busqueda)
        lista = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.entradas = []
        hojas = self.hojas if q else [self.hojas[self.hoja]] if self.hojas else []
        for h in hojas:
            for seccion, entradas in h["secciones"]:
                visibles = [(cod, exp) for cod, exp in entradas
                            if not q or q in sin_tildes(f"{cod} {exp} {seccion}")]
                if not visibles:
                    continue
                s = Gtk.Label(label=(f"{h['titulo']} · {seccion}" if q else seccion).upper(), xalign=0)
                s.add_css_class("seccion")
                lista.append(s)
                for cod, exp in visibles:
                    caja = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
                    caja.add_css_class("entrada")
                    lc = Gtk.Label(xalign=0, wrap=True, wrap_mode=Pango.WrapMode.WORD_CHAR, selectable=False)
                    lc.set_markup(resaltar(cod, h["lenguaje"], self.c))
                    lc.add_css_class("codigo")
                    le = Gtk.Label(label=exp, xalign=0, wrap=True)
                    le.add_css_class("explicacion")
                    caja.append(lc)
                    caja.append(le)
                    clic = Gtk.GestureClick()
                    clic.connect("released", lambda *_a, k=len(self.entradas): self.copiar(k))
                    caja.add_controller(clic)
                    lista.append(caja)
                    self.entradas.append((caja, cod))
        if not self.entradas:
            v = Gtk.Label(label="Nada con esa búsqueda 🙂", margin_top=30)
            v.add_css_class("explicacion")
            lista.append(v)
        self.scroll.set_child(lista)
        self.scroll.get_vadjustment().set_value(0)
        self.sel = None
        if self.entradas and q:
            self.seleccionar(0)

    def seleccionar(self, k):
        if not self.entradas:
            return
        if self.sel is not None:
            self.entradas[self.sel][0].remove_css_class("sel")
        self.sel = max(0, min(len(self.entradas) - 1, k))
        caja = self.entradas[self.sel][0]
        caja.add_css_class("sel")

        def desplazar():
            ok, r = caja.compute_bounds(self.scroll.get_child())
            if ok:
                adj = self.scroll.get_vadjustment()
                if r.get_y() < adj.get_value() + 40:
                    adj.set_value(max(0, r.get_y() - 50))
                elif r.get_y() + r.get_height() > adj.get_value() + adj.get_page_size():
                    adj.set_value(r.get_y() + r.get_height() - adj.get_page_size() + 8)
            return False
        GLib.idle_add(desplazar)

    def copiar(self, k):
        self.seleccionar(k)
        codigo = self.entradas[k][1]
        subprocess.Popen(["wl-copy", "--", codigo], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.copiado.set_label("Copiado ✓")
        GLib.timeout_add(1500, lambda: self.copiado.set_label("") or False)

    def mostrar(self):
        self.present()
        GLib.timeout_add(30, lambda: self.caja.remove_css_class("oculta"))

    def cerrar(self):
        self.caja.add_css_class("oculta")
        LS.set_exclusive_zone(self, 0)
        GLib.timeout_add(230, lambda: self.get_application().quit() or False)

    def tecla(self, _ctl, keyval, _code, estado):
        nombre = Gdk.keyval_name(keyval) or ""
        n = len(self.hojas)
        if nombre == "Escape":
            if self.busqueda:
                self.busqueda = ""
                self.refrescar()
            else:
                self.cerrar()
        elif nombre in ("Tab", "ISO_Left_Tab") and n:
            self.busqueda = ""
            self.mostrar_hoja((self.hoja + (-1 if nombre == "ISO_Left_Tab" else 1)) % n)
        elif nombre == "Down":
            self.seleccionar(0 if self.sel is None else self.sel + 1)
        elif nombre == "Up":
            self.seleccionar(0 if self.sel is None else self.sel - 1)
        elif nombre in ("Return", "KP_Enter"):
            if self.entradas:
                self.copiar(self.sel or 0)
        elif nombre == "BackSpace":
            self.busqueda = self.busqueda[:-1]
            self.refrescar()
        elif estado & (Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.ALT_MASK | Gdk.ModifierType.SUPER_MASK):
            return False
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
