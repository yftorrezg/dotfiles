#!/usr/bin/env python3
"""estilos.py — personaliza tu escritorio (SUPER+SHIFT+A).

Cuatro pestañas:
  🌙 Oscuros / ☀️ Claros  temas: cada uno pone un fondo animado DISTINTO en cada escritorio
                          (la tira de 5 miniaturas = SUPER+1..5). Enter lo aplica.
  🖼️ Galería              todos los fondos: los tuyos y ~300 para descubrir (vista previa animada).
                          1-5 = ponerlo en ese escritorio (si no lo tienes, se baja en 4K) ·
                          Enter = en el escritorio actual · Supr = quitarlo · escribe para buscar.
  🎨 Colores              esquemas de color de toda la interfaz (barra, terminal, Dolphin…).

Las tarjetas muestran una imagen; solo la seleccionada se anima (ahorra GPU).
Teclas: flechas mover · Tab pestaña siguiente · Esc cerrar (o borrar la búsqueda).
Al aplicar guarda estilo.json; escritorios-vivos.py pone los fondos y el modo claro/oscuro.
Para probar sin robar el teclado ni tapar tu monitor: ESTILOS_PRUEBA=DP-3 [ESTILOS_PESTANA=galeria] estilos.py
"""
import ctypes

ctypes.CDLL("libgtk4-layer-shell.so")

import importlib.util  # noqa: E402
import json  # noqa: E402
import os  # noqa: E402
import socket  # noqa: E402
import subprocess  # noqa: E402
import sys  # noqa: E402
import tomllib  # noqa: E402
import unicodedata  # noqa: E402
from pathlib import Path  # noqa: E402

import gi  # noqa: E402

import temas_comun as tc  # noqa: E402

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
gi.require_version("Gtk4LayerShell", "1.0")
gi.require_version("PangoCairo", "1.0")
from gi.repository import Gdk, GLib, Gtk, Pango, PangoCairo  # noqa: E402
from gi.repository import Gtk4LayerShell as LS  # noqa: E402

AQUI = Path(__file__).parent
CONFIG = Path.home() / ".config/hypr/escritorios-temas.toml"
NOCT_SETTINGS = Path.home() / ".local/state/noctalia/settings.toml"
PALETAS = Path.home() / ".config/noctalia/palettes"
HYPR = Path(os.environ["XDG_RUNTIME_DIR"]) / "hypr" / os.environ["HYPRLAND_INSTANCE_SIGNATURE"] / ".socket.sock"
PRUEBA = os.environ.get("ESTILOS_PRUEBA")


def modulo(nombre):
    """Importa un script con guiones en el nombre (descubrir-fondos.py, generar-paletas.py)."""
    spec = importlib.util.spec_from_file_location(nombre.replace("-", "_"), AQUI / f"{nombre}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


descubrir = modulo("descubrir-fondos")
paletas = modulo("generar-paletas")

PESTANAS = (("dark", "🌙  Oscuros"), ("light", "☀️  Claros"), ("galeria", "🖼️  Galería"), ("colores", "🎨  Colores"))
SUBTITULOS = {
    "dark": "Cada tema pone un fondo animado 4K distinto en cada escritorio (SUPER+1…5)",
    "light": "Cada tema pone un fondo animado 4K distinto en cada escritorio (SUPER+1…5)",
    "galeria": "Elige tus fondos: pulsa 1-5 para ponerlo en ese escritorio · escribe para buscar",
    "colores": "Colores de toda la interfaz: barra, terminal, Dolphin y apps · todos probados para leer bien",
}
AYUDAS = {
    "dark": "Flechas mover · Enter aplicar · Tab pestaña · D destellos · Esc salir",
    "light": "Flechas mover · Enter aplicar · Tab pestaña · D destellos · Esc salir",
    "galeria": "1-5 poner en ese escritorio · Enter en este escritorio · Supr quitar · Tab pestaña · Esc salir",
    "colores": "Flechas mover · Enter aplicar · Tab pestaña · Esc salir",
}

CSS = """
window.estilos { background: transparent; }
.velo { background-color: @velo; transition: opacity 250ms ease; }
.velo.oculto { opacity: 0; }
.panel {
  padding: 28px 32px 20px 32px; border-radius: 36px;
  background-color: @panel; border: 1px solid @borde; color: @texto;
  box-shadow: 0 30px 80px rgba(0,0,0,0.45);
  font-family: "Adwaita Sans", "Inter", "Cantarell", sans-serif;
  transition: opacity 280ms cubic-bezier(.2,.8,.2,1), transform 380ms cubic-bezier(.2,1.25,.3,1);
}
.oculto .panel { opacity: 0; transform: translateY(30px) scale(0.94); }
.titulo { font-size: 30px; font-weight: 800; letter-spacing: -0.5px; }
.subtitulo { font-size: 15px; color: @texto2; }
.pestana { font-size: 15.5px; font-weight: 750; padding: 8px 18px; border-radius: 99px;
           background: transparent; color: @texto2; border: none; box-shadow: none; }
.pestana:hover { background-color: @tarjeta_sel; }
.pestana.activa { background-color: @acento; color: @sobre_acento; }
scrolledwindow, scrolledwindow > viewport { background: transparent; }
.seccion { font-size: 17px; font-weight: 800; margin: 14px 4px 2px 4px; }
.seccion-n { font-size: 14px; font-weight: 600; color: @texto2; margin: 14px 4px 2px 0; }
.tarjeta {
  padding: 8px 8px 12px 8px; border-radius: 22px;
  background-color: @tarjeta; border: 2px solid transparent;
  transition: all 220ms cubic-bezier(.2,1.2,.3,1);
}
.tarjeta.sel { border-color: @acento_tarjeta; background-color: @tarjeta_sel;
               box-shadow: 0 10px 30px alpha(@acento_tarjeta, 0.35); }
.vista { border-radius: 15px; background-color: #000; }
.mini { border-radius: 7px; background-color: #000; }
.mini.aqui { outline: 2px solid @acento_tarjeta; outline-offset: 1px; }
.num { font-size: 11px; font-weight: 800; color: #fff; background-color: rgba(0,0,0,0.55);
       border-radius: 99px; padding: 0 5px; margin: 3px; }
.nombre { font-size: 15px; font-weight: 700; }
.desc { font-size: 13px; color: @texto2; }
.insignia { font-size: 11.5px; font-weight: 800; padding: 3px 9px; border-radius: 99px;
            background-color: @acento; color: @sobre_acento; margin: 8px; }
.insignia.suave { background-color: rgba(0,0,0,0.62); color: #fff; }
.punto { min-width: 12px; min-height: 12px; border-radius: 99px; margin: 4px 2px 0 0; }
.icono-tema { font-family: "Noto Color Emoji"; font-size: 18px; }
.pie { font-size: 13.5px; color: @texto2; }
.busqueda { font-size: 15px; font-weight: 650; padding: 6px 14px; border-radius: 99px;
            background-color: @tarjeta_sel; }
.mensaje { font-size: 14px; font-weight: 650; color: @acento_texto; }
.destellos-lbl { font-size: 15px; font-weight: 650; }
.icono { font-family: "Noto Color Emoji"; font-size: 20px; }
.vacio { font-size: 16px; color: @texto2; margin: 40px; }
"""


def hypr_json(cmd):
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
        s.connect(str(HYPR))
        s.sendall(f"j/{cmd}".encode())
        data = b""
        while chunk := s.recv(65536):
            data += chunk
    return json.loads(data)


def leer_modo():
    try:
        with open(NOCT_SETTINGS, "rb") as f:
            return tomllib.load(f).get("theme", {}).get("mode", "dark")
    except (OSError, tomllib.TOMLDecodeError):
        return "dark"


def escritorio_actual(n=5):
    try:
        wid = hypr_json("activeworkspace")["id"]
        return (wid - 1) % n + 1 if 1 <= wid <= 2 * n else 1
    except (OSError, ValueError, KeyError):
        return 1


def sin_tildes(texto):
    return unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().casefold()


def esquema_actual():
    try:
        salida = subprocess.run(["noctalia", "msg", "color-scheme-get"], capture_output=True,
                                text=True, timeout=2).stdout.split()
        return salida[1] if len(salida) >= 2 and salida[0] == "custom" else None
    except (OSError, subprocess.TimeoutExpired):
        return None


def rgb(h):
    return tuple(int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))


def dibujar_esquema(_area, cr, w, h, datos):
    """Vista previa de un esquema: mitad oscura y mitad clara, cada una como una mini ventana."""
    mitad = w / 2
    for i, modo in enumerate(("dark", "light")):
        p = datos[modo]
        x0 = i * mitad
        cr.set_source_rgb(*rgb(p["mSurface"]))
        cr.rectangle(x0, 0, mitad, h)
        cr.fill()
        # ventana de terminal
        cr.set_source_rgb(*rgb(p["mSurfaceVariant"]))
        cr.rectangle(x0 + 12, 12, mitad - 24, h - 24)
        cr.fill()
        y = 22
        lay = PangoCairo.create_layout(cr)
        lay.set_font_description(Pango.FontDescription.from_string("Adwaita Sans Bold 11"))
        lay.set_text("Oscuro" if modo == "dark" else "Claro", -1)
        cr.set_source_rgb(*rgb(p["mOnSurface"]))
        cr.move_to(x0 + 22, y)
        PangoCairo.show_layout(cr, lay)
        y += 22
        lay.set_font_description(Pango.FontDescription.from_string("Adwaita Mono 9"))
        t = p["terminal"]["normal"]
        for partes in ((("def ", t["magenta"]), ("leer", t["blue"]), ("():", p["mOnSurface"])),
                       (("  print(", p["mOnSurface"]), ('"hola"', t["green"]), (")", p["mOnSurface"])),
                       (("# listo ✓", p["terminal"]["bright"]["black"]),)):
            x = x0 + 22
            for texto, color in partes:
                lay.set_text(texto, -1)
                cr.set_source_rgb(*rgb(color))
                cr.move_to(x, y)
                PangoCairo.show_layout(cr, lay)
                x += lay.get_pixel_size()[0]
            y += 17
        # botón con el color principal + puntos de la paleta de la terminal
        cr.set_source_rgb(*rgb(p["mPrimary"]))
        cr.arc(x0 + 30, h - 30, 8, 0, 6.2832)
        cr.fill()
        for j, k in enumerate(("red", "green", "yellow", "blue", "magenta", "cyan")):
            cr.set_source_rgb(*rgb(t[k]))
            cr.arc(x0 + 52 + j * 15, h - 30, 5, 0, 6.2832)
            cr.fill()


class Tarjeta(Gtk.Box):
    def __init__(self, selector, item):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.item = item
        self.selector = selector
        self.add_css_class("tarjeta")
        self.capas = Gtk.Overlay()
        w, h = selector.tam_vista
        if item.get("esquema"):
            vista = Gtk.DrawingArea(content_width=w, content_height=h)
            vista.set_draw_func(dibujar_esquema, item["esquema"])
            vista.add_css_class("vista")
            vista.set_overflow(Gtk.Overflow.HIDDEN)
            self.pic = None
            self.capas.set_child(vista)
        else:
            self.pic = Gtk.Picture(content_fit=Gtk.ContentFit.COVER, can_shrink=True)
            self.pic.set_size_request(w, h)
            self.pic.add_css_class("vista")
            self.pic.set_overflow(Gtk.Overflow.HIDDEN)
            self.capas.set_child(self.pic)
        self.lbl_insignia = Gtk.Label(halign=Gtk.Align.END, valign=Gtk.Align.START, visible=False)
        self.lbl_insignia.add_css_class("insignia")
        self.capas.add_overlay(self.lbl_insignia)
        self.append(self.capas)
        self.minis = []
        if item.get("tira"):  # los 5 fondos del tema: uno por escritorio
            tira = Gtk.Box(spacing=5, homogeneous=True)
            for n, ruta in enumerate(item["tira"], 1):
                o = Gtk.Overlay()
                m = Gtk.Picture(content_fit=Gtk.ContentFit.COVER, can_shrink=True)
                m.set_size_request(-1, int(h * 0.19))
                m.add_css_class("mini")
                m.set_overflow(Gtk.Overflow.HIDDEN)
                if n == selector.escritorio:
                    m.add_css_class("aqui")
                o.set_child(m)
                num = Gtk.Label(label=str(n), halign=Gtk.Align.START, valign=Gtk.Align.END)
                num.add_css_class("num")
                o.add_overlay(num)
                tira.append(o)
                self.minis.append((m, ruta))
            self.append(tira)
        fila = Gtk.Box(spacing=8)
        if item.get("icono"):
            ic = Gtk.Label(label=item["icono"], valign=Gtk.Align.START)
            ic.add_css_class("icono-tema")
            fila.append(ic)
        else:
            punto = Gtk.Box(valign=Gtk.Align.START)
            punto.add_css_class("punto")
            punto.add_css_class(selector.clase_color(item.get("acento", tc.ACENTO_POR_DEFECTO)))
            fila.append(punto)
        txt = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        nl = Gtk.Label(label=item["nombre"], xalign=0, ellipsize=Pango.EllipsizeMode.END)
        nl.add_css_class("nombre")
        self.dl = Gtk.Label(label=item["desc"], xalign=0, ellipsize=Pango.EllipsizeMode.END)
        self.dl.add_css_class("desc")
        txt.append(nl)
        txt.append(self.dl)
        fila.append(txt)
        self.append(fila)
        self.media = None
        self.cargada = False
        self.insignia(item.get("insignia"), item.get("insignia_suave", False))

    def insignia(self, texto, suave=False):
        self.lbl_insignia.set_visible(bool(texto))
        if texto:
            self.lbl_insignia.set_label(texto)
            (self.lbl_insignia.add_css_class if suave else self.lbl_insignia.remove_css_class)("suave")

    def cargar(self):
        """Carga las imágenes (se hace por tandas, para que la Galería abra al instante)."""
        if self.cargada:
            return
        self.cargada = True
        poster = self.item.get("poster")
        if self.pic is not None and poster and Path(poster).exists():
            self.pic.set_filename(str(poster))
        for m, ruta in self.minis:
            if ruta and Path(ruta).exists():
                m.set_filename(str(ruta))

    def animar(self, si):
        """Solo la tarjeta seleccionada reproduce su clip; las demás muestran el póster."""
        clip = self.item.get("clip")
        if self.pic is None:
            return
        if si and clip and Path(clip).exists():
            if self.media is None:
                self.media = Gtk.MediaFile.new_for_filename(str(clip))
                self.media.set_loop(True)
                self.media.set_muted(True)
            self.pic.set_paintable(self.media)
            self.media.play()
        elif self.media is not None:
            self.media.pause()
            if self.item.get("poster"):
                self.pic.set_filename(str(self.item["poster"]))


class Selector(Gtk.ApplicationWindow):
    def __init__(self, app, cfg):
        super().__init__(application=app)
        self.add_css_class("estilos")
        LS.init_for_window(self)
        LS.set_namespace(self, "estilos")
        LS.set_layer(self, LS.Layer.OVERLAY)
        LS.set_keyboard_mode(self, LS.KeyboardMode.NONE if PRUEBA else LS.KeyboardMode.EXCLUSIVE)
        LS.set_exclusive_zone(self, -1)
        for borde in (LS.Edge.TOP, LS.Edge.BOTTOM, LS.Edge.LEFT, LS.Edge.RIGHT):
            LS.set_anchor(self, borde, True)
        self.vertical, alto_mon = False, 1080
        try:
            monitores = hypr_json("monitors")
            foco = PRUEBA or next(m["name"] for m in monitores if m["focused"])
            info = next(m for m in monitores if m["name"] == foco)
            self.vertical = info.get("transform", 0) % 2 == 1
            alto_mon = info["width"] if self.vertical else info["height"]
            mon = next((m for m in Gdk.Display.get_default().get_monitors() if m.get_connector() == foco), None)
            if mon:
                LS.set_monitor(self, mon)
        except (OSError, ValueError, StopIteration, KeyError):
            pass
        self.columnas = 3 if self.vertical else 4
        self.tam_vista = (290, 163) if self.vertical else (300, 169)

        self.cfg = cfg
        self.estilo = tc.leer_estilo()
        self.modo = leer_modo()
        self.escritorio = escritorio_actual(int(cfg.get("general", {}).get("por_monitor", 5)))
        self.cerrando = False
        self.busqueda = os.environ.get("ESTILOS_BUSCAR", "")  # para pruebas
        self.bajando = {}       # id del catálogo -> escritorio al que irá
        self.colores_css = {}   # color -> clase CSS
        claro = self.modo == "light"
        css = Gtk.CssProvider()
        css.load_from_string(
            "@define-color acento #8b5cf6; @define-color sobre_acento #ffffff; @define-color acento_tarjeta #8b5cf6;"
            + ("@define-color velo rgba(235,230,222,0.55); @define-color panel rgba(250,247,241,0.97);"
               "@define-color borde rgba(255,255,255,1); @define-color texto #2f2b38; @define-color texto2 #5a5468;"
               "@define-color tarjeta rgba(60,50,40,0.05); @define-color tarjeta_sel rgba(60,50,40,0.09);"
               "@define-color acento_texto #6a3fc4;"
               if claro else
               "@define-color velo rgba(5,5,12,0.6); @define-color panel rgba(20,20,28,0.96);"
               "@define-color borde rgba(255,255,255,0.08); @define-color texto #f4f2fa; @define-color texto2 #bdb8cc;"
               "@define-color tarjeta rgba(255,255,255,0.04); @define-color tarjeta_sel rgba(255,255,255,0.09);"
               "@define-color acento_texto #c4adff;")
            + CSS)
        pantalla = Gdk.Display.get_default()
        Gtk.StyleContext.add_provider_for_display(pantalla, css, 800)
        self.css_acento = Gtk.CssProvider()
        Gtk.StyleContext.add_provider_for_display(pantalla, self.css_acento, 850)
        self.css_colores = Gtk.CssProvider()
        Gtk.StyleContext.add_provider_for_display(pantalla, self.css_colores, 860)

        self.velo = Gtk.Box(hexpand=True, vexpand=True)
        self.velo.add_css_class("velo")
        self.velo.add_css_class("oculto")
        clic_fuera = Gtk.GestureClick()
        clic_fuera.connect("released", self.clic_en_velo)
        self.velo.add_controller(clic_fuera)
        self.panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16,
                             halign=Gtk.Align.CENTER, valign=Gtk.Align.CENTER, hexpand=True)
        self.panel.add_css_class("panel")
        self.velo.append(self.panel)

        cab = Gtk.Box(spacing=16)
        textos = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2, hexpand=True)
        t = Gtk.Label(label="Personaliza tu escritorio", xalign=0)
        t.add_css_class("titulo")
        self.subtitulo = Gtk.Label(xalign=0, wrap=True)
        self.subtitulo.add_css_class("subtitulo")
        textos.append(t)
        textos.append(self.subtitulo)
        cab.append(textos)
        pestanas = Gtk.Box(spacing=4, valign=Gtk.Align.CENTER)
        self.botones = {}
        for clave, etiqueta in PESTANAS:
            b = Gtk.Button(label=etiqueta, valign=Gtk.Align.CENTER)
            b.add_css_class("pestana")
            b.connect("clicked", lambda _b, k=clave: self.mostrar_pestana(k))
            pestanas.append(b)
            self.botones[clave] = b
        if self.vertical:  # en el monitor vertical las pestañas van debajo del título
            self.panel.append(cab)
            self.panel.append(pestanas)
        else:
            cab.append(pestanas)
            self.panel.append(cab)

        self.barra_busqueda = Gtk.Label(xalign=0, visible=False)
        self.barra_busqueda.add_css_class("busqueda")
        self.panel.append(self.barra_busqueda)

        self.scroll = Gtk.ScrolledWindow(hscrollbar_policy=Gtk.PolicyType.NEVER)
        alto_tarjeta = self.tam_vista[1] + 120
        self.scroll.set_size_request(-1, min(int(alto_mon * 0.64), alto_tarjeta * (4 if self.vertical else 3)))
        self.scroll.get_vadjustment().connect("value-changed", lambda *_: self.cargar_visibles())
        self.panel.append(self.scroll)

        pie = Gtk.Box(spacing=12)
        chispa = Gtk.Label(label="✨")
        chispa.add_css_class("icono")
        lbl = Gtk.Label(label="Destellos del cursor", xalign=0)
        lbl.add_css_class("destellos-lbl")
        self.interruptor = Gtk.Switch(active=self.estilo["destellos"], valign=Gtk.Align.CENTER)
        self.interruptor.connect("notify::active", self.cambiar_destellos)
        self.mensaje = Gtk.Label(xalign=0, hexpand=True, ellipsize=Pango.EllipsizeMode.END)
        self.mensaje.add_css_class("mensaje")
        self.ayuda = Gtk.Label(xalign=1, wrap=True)
        self.ayuda.add_css_class("pie")
        for w in (chispa, lbl, self.interruptor, self.mensaje, self.ayuda):
            pie.append(w)
        self.panel.append(pie)
        self.set_child(self.velo)

        teclas = Gtk.EventControllerKey()
        teclas.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)  # antes que el foco use Tab/flechas
        teclas.connect("key-pressed", self.tecla)
        self.add_controller(teclas)
        modo_tema = tc.modo_de(self.estilo["tema"], self.estilo)
        self.mostrar_pestana(os.environ.get("ESTILOS_PESTANA") or modo_tema or self.modo)

    def clase_color(self, color):
        """Clase CSS para un color (un solo proveedor para todos: nada de estilos por widget)."""
        if color not in self.colores_css:
            self.colores_css[color] = f"c-{color.lstrip('#')}"
            self.css_colores.load_from_string("".join(
                f".{c} {{ background-color: {col}; }}" for col, c in self.colores_css.items()))
        return self.colores_css[color]

    # --- contenido ----------------------------------------------------------------------
    def items_temas(self, modo):
        lista = []
        cat = tc.catalogo()
        for col in tc.colecciones(self.estilo):
            if col["modo"] != modo:
                continue
            fondos = tc.fondos_de(col, cat)
            if not fondos:
                continue
            primero = fondos[self.escritorio - 1]
            r = tc.rutas(primero)
            lista.append({"id": col["id"], "tipo": "tema", "modo": modo, "nombre": col["nombre"],
                          "icono": col["icono"], "desc": col["desc"],
                          "poster": r["mini"], "clip": r["clip"], "acento": tc.acento(primero),
                          "tira": [tc.rutas(f)["mini"] for f in fondos],
                          "insignia": "ACTUAL" if self.estilo["tema"] == col["id"] else None})
        suf = "claro" if modo == "light" else "oscuro"
        carpeta = Path(os.path.expanduser(self.cfg.get("general", {}).get("carpeta", "~")))
        escritorios = self.cfg.get("escritorio", [])
        for tid, (nombre, desc, icono) in tc.POR_ESCRITORIO.items():
            video = tid == "escritorios:video"
            tira = []
            for e in escritorios[:tc.ESCRITORIOS]:
                rel = e.get(f"video_{suf}" if video else f"fondo_{suf}")
                ruta = carpeta / rel if rel else None
                tira.append(None if not ruta or not ruta.exists() else (tc.poster_video(ruta) if video else ruta))
            if not any(tira):
                continue
            aqui = tira[self.escritorio - 1] if self.escritorio <= len(tira) else None
            clip = None
            if video and self.escritorio <= len(escritorios):
                rel = escritorios[self.escritorio - 1].get(f"video_{suf}")
                clip = carpeta / rel if rel else None
            lista.append({"id": tid, "tipo": "tema", "modo": modo, "nombre": nombre, "icono": icono,
                          "desc": desc, "poster": aqui, "clip": clip, "tira": tira,
                          "insignia": "ACTUAL" if self.estilo["tema"] == tid and self.modo == modo else None})
        return [(None, lista)]

    def items_galeria(self):
        mezcla = self.estilo["mezcla"][self.modo]
        secciones = []
        for carpeta, modo in tc.GRUPOS:
            mios = []
            for t in tc.catalogo():
                if t["modo"] != modo:
                    continue
                r = tc.rutas(t)
                en = [str(i + 1) for i, f in enumerate(mezcla) if f == t["id"]]
                mios.append({"id": t["id"], "tipo": "mio", "modo": modo, "nombre": t["nombre"],
                             "desc": f"Tuyo · {carpeta.lower()[:-1]} · 4K", "poster": r["mini"], "clip": r["clip"],
                             "acento": tc.acento(t), "buscar": sin_tildes(t["nombre"] + " " + carpeta),
                             "insignia": f"EN {', '.join(en)}" if en else None})
            secciones.append((f"Tus fondos · {carpeta.lower()}", mios))
        descartados = set(descubrir.leer_json(descubrir.DESCARTADOS, []))
        por_cat = {}
        for e in descubrir.leer_json(descubrir.CATALOGO, []):
            if e.get("tengo") or e["id"] in descartados:
                continue
            base = descubrir.CARPETA / e["id"]
            bajando = self.bajando.get(e["id"])
            por_cat.setdefault(e["categoria"], []).append({
                "id": e["id"], "tipo": "descubrir", "modo": e.get("modo", "dark"), "nombre": e["titulo"],
                "desc": f"{e['categoria']} · {'oscuro' if e.get('modo') == 'dark' else 'claro'} · 4K",
                "poster": base.with_suffix(".jpg"), "clip": base.with_suffix(".mp4"),
                "acento": "#8fa8ff" if e.get("modo") == "dark" else "#ffb347",
                "buscar": sin_tildes(e["titulo"] + " " + e["categoria"]),
                "insignia": f"BAJANDO → {bajando}" if bajando else "NUEVO", "insignia_suave": not bajando})
        for cat, lista in por_cat.items():
            secciones.append((f"Descubrir · {cat}", lista))
        if self.busqueda:
            q = sin_tildes(self.busqueda)
            secciones = [(s, [i for i in l if q in i["buscar"]]) for s, l in secciones]
        return [(s, l) for s, l in secciones if l]

    def items_colores(self):
        actual = esquema_actual()
        lista = []
        for clave, e in paletas.ESQUEMAS.items():
            try:
                datos = json.loads((PALETAS / f"{clave}.json").read_text())
            except (OSError, ValueError):
                continue
            lista.append({"id": clave, "tipo": "color", "nombre": e["nombre"], "icono": e["icono"],
                          "desc": e["desc"], "esquema": datos, "acento": datos[self.modo]["mPrimary"],
                          "insignia": "ACTUAL" if clave == actual else None})
        return [(None, lista)]

    def mostrar_pestana(self, clave, conservar=False):
        anterior = self.sel if conservar and getattr(self, "sel", None) is not None else None
        if getattr(self, "tarjetas", None):
            for t in self.tarjetas:
                t.animar(False)
        self.pestana = clave
        for k, b in self.botones.items():
            (b.add_css_class if k == clave else b.remove_css_class)("activa")
        self.subtitulo.set_label(SUBTITULOS[clave])
        self.ayuda.set_label(AYUDAS[clave])
        if clave != "galeria":
            self.busqueda = ""
        self.barra_busqueda.set_visible(clave == "galeria")
        self.barra_busqueda.set_label(f"🔍  {self.busqueda}" if self.busqueda else "🔍  Escribe para buscar (Itachi, Miku, Blue Archive…)")
        if clave in ("dark", "light"):
            secciones = self.items_temas(clave)
        elif clave == "galeria":
            secciones = self.items_galeria()
        else:
            secciones = self.items_colores()

        grid = Gtk.Grid(column_spacing=14, row_spacing=14, margin_end=6)
        self.tarjetas, self.pos = [], []
        fila = 0
        for titulo, lista in secciones:
            if titulo:
                cab = Gtk.Box(spacing=8)
                s = Gtk.Label(label=titulo, xalign=0)
                s.add_css_class("seccion")
                n = Gtk.Label(label=str(len(lista)), xalign=0)
                n.add_css_class("seccion-n")
                cab.append(s)
                cab.append(n)
                grid.attach(cab, 0, fila, self.columnas, 1)
                fila += 1
            for j, item in enumerate(lista):
                i = len(self.tarjetas)
                tarjeta = Tarjeta(self, item)
                mov = Gtk.EventControllerMotion()
                mov.connect("enter", lambda *_, i=i: self.seleccionar(i, desplazar=False))
                tarjeta.add_controller(mov)
                clic = Gtk.GestureClick()
                clic.connect("released", lambda *_, i=i: self.activar(i))
                tarjeta.add_controller(clic)
                r, c = fila + j // self.columnas, j % self.columnas
                grid.attach(tarjeta, c, r, 1, 1)
                self.tarjetas.append(tarjeta)
                self.pos.append((r, c))
            fila += (len(lista) + self.columnas - 1) // self.columnas
        if not self.tarjetas:
            v = Gtk.Label(label="Nada por aquí con esa búsqueda 🙂" if self.busqueda else "Nada por aquí todavía")
            v.add_css_class("vacio")
            grid.attach(v, 0, 0, self.columnas, 1)
        self.scroll.set_child(grid)
        self.scroll.get_vadjustment().set_value(0)
        self.sel = None
        if self.tarjetas:
            if anterior is not None:
                inicio = min(anterior, len(self.tarjetas) - 1)
            else:
                inicio = next((i for i, t in enumerate(self.tarjetas) if t.item.get("insignia") == "ACTUAL"), 0)
            self.seleccionar(inicio)
        GLib.idle_add(self.cargar_visibles)

    def cargar_visibles(self):
        """Carga las imágenes de lo que se ve (y un poco más); el resto al desplazarse."""
        adj = self.scroll.get_vadjustment()
        abajo = adj.get_value() + adj.get_page_size() * 2.5
        grid = self.scroll.get_child()
        for t in self.tarjetas:
            if t.cargada:
                continue
            ok, caja = t.compute_bounds(grid)
            if not ok or caja.get_y() <= abajo:
                t.cargar()
        return False

    def seleccionar(self, i, desplazar=True):
        if not self.tarjetas:
            return
        if self.sel is not None and self.sel < len(self.tarjetas):
            self.tarjetas[self.sel].remove_css_class("sel")
            self.tarjetas[self.sel].animar(False)
        self.sel = i
        t = self.tarjetas[i]
        t.cargar()
        t.add_css_class("sel")
        t.animar(True)
        self.css_acento.load_from_string(f"@define-color acento_tarjeta {t.item.get('acento', '#8b5cf6')};")
        if desplazar:
            GLib.idle_add(self.desplazar_a, t)

    def desplazar_a(self, tarjeta):
        ok, caja = tarjeta.compute_bounds(self.scroll.get_child())
        if ok:
            adj = self.scroll.get_vadjustment()
            arriba, abajo = caja.get_y(), caja.get_y() + caja.get_height()
            if arriba < adj.get_value() + 40:
                adj.set_value(max(0, arriba - 50))  # deja ver el título de la sección
            elif abajo > adj.get_value() + adj.get_page_size():
                adj.set_value(abajo - adj.get_page_size() + 8)
        return False

    def mover_vertical(self, paso):
        """Arriba/abajo por filas reales (las secciones de la Galería tienen filas incompletas)."""
        fila, col = self.pos[self.sel]
        filas = sorted({r for r, _ in self.pos})
        k = filas.index(fila) + paso
        if not 0 <= k < len(filas):
            return
        candidatos = [(abs(c - col), i) for i, (r, c) in enumerate(self.pos) if r == filas[k]]
        self.seleccionar(min(candidatos)[1])

    # --- acciones -----------------------------------------------------------------------
    def mostrar(self):
        self.present()
        GLib.timeout_add(30, lambda: self.velo.remove_css_class("oculto"))

    def clic_en_velo(self, _g, _n, x, y):
        ok, caja = self.panel.compute_bounds(self.velo)
        if ok and not (caja.get_x() <= x <= caja.get_x() + caja.get_width()
                       and caja.get_y() <= y <= caja.get_y() + caja.get_height()):
            self.cerrar()

    def cambiar_destellos(self, sw, _param):
        self.estilo = tc.leer_estilo()
        self.estilo["destellos"] = sw.get_active()
        tc.guardar_estilo(self.estilo)

    def decir(self, texto):
        self.mensaje.set_label(texto)

    def activar(self, i):
        item = self.tarjetas[i].item
        if item["tipo"] == "tema":
            self.aplicar_tema(item)
        elif item["tipo"] == "color":
            self.aplicar_colores(item)
        else:
            self.poner_en(i, self.escritorio)

    def aplicar_tema(self, item):
        self.estilo = tc.leer_estilo()
        self.estilo["tema"] = item["id"]
        self.estilo["modo"] = item["modo"]
        tc.guardar_estilo(self.estilo)  # primero el tema, luego el modo (ver escritorios-vivos)
        if item["modo"] != self.modo:
            subprocess.Popen(["noctalia", "msg", "theme-mode-set", item["modo"]],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.cerrar()

    def aplicar_colores(self, item):
        subprocess.Popen(["noctalia", "msg", "color-scheme-set", "custom", item["id"]],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for t in self.tarjetas:
            t.insignia("ACTUAL" if t is self.tarjetas[self.sel] else None)
        self.decir(f"{item['icono']} {item['nombre']} aplicado")

    def poner_en(self, i, n):
        """Galería: pone el fondo en el escritorio n de "Mi selección" (del modo actual)."""
        item = self.tarjetas[i].item
        modo = self.modo
        if item["tipo"] == "descubrir":
            if item["id"] in self.bajando:
                return
            self.bajando[item["id"]] = n
            subprocess.Popen([sys.executable, str(AQUI / "descubrir-fondos.py"), "poner", item["id"], str(n), modo],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
            self.tarjetas[i].insignia(f"BAJANDO → {n}")
            self.decir(f"⬇️ Bajando «{item['nombre']}» en 4K → escritorio {n} (te aviso al terminar)")
            return
        self.estilo = tc.leer_estilo()
        self.estilo["mezcla"][modo][n - 1] = item["id"]
        self.estilo["tema"], self.estilo["modo"] = f"mezcla:{modo}", modo
        self.estilo["ultimo"][modo] = self.estilo["tema"]
        tc.guardar_estilo(self.estilo)
        mezcla = self.estilo["mezcla"][modo]
        for t in self.tarjetas:
            if t.item["tipo"] == "mio":
                en = [str(k + 1) for k, f in enumerate(mezcla) if f == t.item["id"]]
                t.insignia(f"EN {', '.join(en)}" if en else None)
        self.decir(f"✅ «{item['nombre']}» en el escritorio {n}")

    def quitar(self, i):
        """Supr: los tuyos van a la papelera; los de Descubrir dejan de aparecer."""
        item = self.tarjetas[i].item
        if item["tipo"] == "mio":
            t = tc.buscar(item["id"])
            if t and subprocess.run(["gio", "trash", str(t["video"])]).returncode == 0:
                self.decir(f"🗑️ «{item['nombre']}» a la papelera (puedes recuperarlo)")
        elif item["tipo"] == "descubrir":
            lista = descubrir.leer_json(descubrir.DESCARTADOS, [])
            lista.append(item["id"])
            descubrir.guardar_json(descubrir.DESCARTADOS, lista)
            self.decir(f"🙈 «{item['nombre']}» ya no se mostrará")
        else:
            return
        self.mostrar_pestana("galeria", conservar=True)

    def cerrar(self):
        if self.cerrando:
            return
        self.cerrando = True
        LS.set_keyboard_mode(self, LS.KeyboardMode.NONE)  # devolver el teclado ya
        for t in self.tarjetas:
            t.animar(False)
        self.velo.add_css_class("oculto")

        def fin():
            self.set_visible(False)
            self.get_application().quit()
            return False
        GLib.timeout_add(260, fin)

    def tecla(self, _ctl, keyval, _code, estado):
        nombre = Gdk.keyval_name(keyval) or ""
        n, c = len(self.tarjetas), self.columnas
        galeria = self.pestana == "galeria"
        orden = [k for k, _ in PESTANAS]
        if nombre == "Escape":
            if galeria and self.busqueda:
                self.busqueda = ""
                self.mostrar_pestana("galeria")
            else:
                self.cerrar()
        elif nombre in ("Tab", "ISO_Left_Tab"):
            paso = -1 if nombre == "ISO_Left_Tab" else 1
            self.mostrar_pestana(orden[(orden.index(self.pestana) + paso) % len(orden)])
        elif not n:
            if galeria and nombre == "BackSpace":
                self.busqueda = self.busqueda[:-1]
                self.mostrar_pestana("galeria")
            elif galeria and (ch := chr(Gdk.keyval_to_unicode(keyval) or 0)).isprintable() and ch.strip():
                self.busqueda += ch
                self.mostrar_pestana("galeria")
        elif nombre in ("Return", "KP_Enter"):
            self.activar(self.sel)
        elif nombre in ("Right",):
            self.seleccionar((self.sel + 1) % n)
        elif nombre in ("Left",):
            self.seleccionar((self.sel - 1) % n)
        elif nombre in ("Down",):
            self.mover_vertical(1)
        elif nombre in ("Up",):
            self.mover_vertical(-1)
        elif nombre in ("Page_Down", "Page_Up"):
            self.seleccionar(max(0, min(n - 1, self.sel + (3 * c if nombre == "Page_Down" else -3 * c))))
        elif galeria and nombre in ("1", "2", "3", "4", "5", "KP_1", "KP_2", "KP_3", "KP_4", "KP_5"):
            self.poner_en(self.sel, int(nombre[-1]))
        elif galeria and nombre == "Delete":
            self.quitar(self.sel)
        elif galeria and nombre == "BackSpace":
            if self.busqueda:
                self.busqueda = self.busqueda[:-1]
                self.mostrar_pestana("galeria")
        elif galeria:
            ch = chr(Gdk.keyval_to_unicode(keyval) or 0)
            if ch.isprintable() and (ch.strip() or self.busqueda) and not ch.isdigit():
                self.busqueda += ch
                self.mostrar_pestana("galeria")
        elif nombre == "space":
            self.activar(self.sel)
        elif nombre.lower() == "d":
            self.interruptor.set_active(not self.interruptor.get_active())
        return True


class App(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="dev.yafer.Estilos")  # única: SUPER+SHIFT+A otra vez la cierra

    def do_activate(self):
        if self.get_windows():
            self.get_windows()[0].cerrar()
            return
        with open(CONFIG, "rb") as f:
            cfg = tomllib.load(f)
        Selector(self, cfg).mostrar()


if __name__ == "__main__":
    App().run(None)
