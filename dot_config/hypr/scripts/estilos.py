#!/usr/bin/env python3
"""estilos.py — selector de temas (SUPER+SHIFT+A).

Dos pestañas, 🌙 Oscuros y ☀️ Claros. Cada una empieza con los temas "por escritorio"
(un fondo distinto en cada SUPER+1..5) y sigue con los temas de video de
~/Imágenes/Wallpapers/Temas/{Oscuros,Claros} (ver temas_comun.py).
Las tarjetas muestran un póster; solo la seleccionada se anima (ahorra GPU).

Teclas: flechas mover · Tab cambia de pestaña · Enter aplica · D destellos del cursor · Esc cierra.
También con el ratón (pasar por encima = seleccionar, clic = aplicar, rueda = desplazar).

Al aplicar guarda estilo.json y luego pone el modo de noctalia; escritorios-vivos.py hace el resto.
Para probar sin robar el teclado ni tapar tu monitor: ESTILOS_PRUEBA=DP-3 estilos.py
"""
import ctypes

ctypes.CDLL("libgtk4-layer-shell.so")

import json  # noqa: E402
import os  # noqa: E402
import socket  # noqa: E402
import subprocess  # noqa: E402
import tomllib  # noqa: E402
from pathlib import Path  # noqa: E402

import gi  # noqa: E402

import temas_comun as tc  # noqa: E402

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
gi.require_version("Gtk4LayerShell", "1.0")
from gi.repository import Gdk, GLib, Gtk  # noqa: E402
from gi.repository import Gtk4LayerShell as LS  # noqa: E402

CONFIG = Path.home() / ".config/hypr/escritorios-temas.toml"
NOCT_SETTINGS = Path.home() / ".local/state/noctalia/settings.toml"
HYPR = Path(os.environ["XDG_RUNTIME_DIR"]) / "hypr" / os.environ["HYPRLAND_INSTANCE_SIGNATURE"] / ".socket.sock"
PRUEBA = os.environ.get("ESTILOS_PRUEBA")

CSS = """
window.estilos { background: transparent; }
.velo { background-color: @velo; transition: opacity 250ms ease; }
.velo.oculto { opacity: 0; }
.panel {
  padding: 30px 34px 22px 34px; border-radius: 36px;
  background-color: @panel; border: 1px solid @borde; color: @texto;
  box-shadow: 0 30px 80px rgba(0,0,0,0.45);
  font-family: "Adwaita Sans", "Inter", "Cantarell", sans-serif;
  transition: opacity 280ms cubic-bezier(.2,.8,.2,1), transform 380ms cubic-bezier(.2,1.25,.3,1);
}
.oculto .panel { opacity: 0; transform: translateY(30px) scale(0.94); }
.titulo { font-size: 32px; font-weight: 800; letter-spacing: -0.5px; }
.subtitulo { font-size: 15px; opacity: 0.75; }
.pestana { font-size: 16px; font-weight: 750; padding: 8px 20px; border-radius: 99px;
           background: transparent; color: @texto; border: none; box-shadow: none; opacity: 0.7; }
.pestana.activa { background-color: @acento; color: @sobre_acento; opacity: 1; }
scrolledwindow, scrolledwindow > viewport { background: transparent; }
.tarjeta {
  padding: 8px 8px 12px 8px; border-radius: 22px;
  background-color: @tarjeta; border: 2px solid transparent;
  transition: all 220ms cubic-bezier(.2,1.2,.3,1);
}
.tarjeta.sel { border-color: @acento_tarjeta; background-color: @tarjeta_sel;
               box-shadow: 0 10px 30px alpha(@acento_tarjeta, 0.35); }
.vista { border-radius: 15px; background-color: #000; }
.nombre { font-size: 15px; font-weight: 700; }
.desc { font-size: 12.5px; opacity: 0.75; }
.actual { font-size: 11px; font-weight: 800; padding: 3px 9px; border-radius: 99px;
          background-color: @acento; color: @sobre_acento; margin: 8px; }
.punto { min-width: 12px; min-height: 12px; border-radius: 99px; margin: 4px 2px 0 0; }
.pie { font-size: 13px; opacity: 0.75; }
.destellos-lbl { font-size: 15px; font-weight: 650; }
.icono { font-family: "Noto Color Emoji"; font-size: 20px; }
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


def fondo_escritorio(cfg, modo, video):
    """Imagen (o video) del escritorio actual para la tarjeta 'por escritorio'."""
    n = int(cfg.get("general", {}).get("por_monitor", 5))
    try:
        wid = hypr_json("activeworkspace")["id"]
        idx = (wid - 1) % n + 1 if 1 <= wid <= 2 * n else 1
    except (OSError, ValueError, KeyError):
        idx = 1
    lista = cfg.get("escritorio", [])
    e = lista[idx - 1] if idx <= len(lista) else {}
    suf = "claro" if modo == "light" else "oscuro"
    rel = e.get(f"video_{suf}" if video else f"fondo_{suf}")
    carpeta = Path(os.path.expanduser(cfg.get("general", {}).get("carpeta", "~")))
    ruta = carpeta / rel if rel else None
    return ruta if ruta and ruta.exists() else None


class Tarjeta(Gtk.Box):
    def __init__(self, selector, item):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.item = item
        self.add_css_class("tarjeta")
        capas = Gtk.Overlay()
        self.pic = Gtk.Picture(content_fit=Gtk.ContentFit.COVER, can_shrink=True)
        self.pic.set_size_request(*selector.tam_vista)
        self.pic.add_css_class("vista")
        self.pic.set_overflow(Gtk.Overflow.HIDDEN)
        if item["poster"] and Path(item["poster"]).exists():
            self.pic.set_filename(str(item["poster"]))
        capas.set_child(self.pic)
        if item["actual"]:
            act = Gtk.Label(label="ACTUAL", halign=Gtk.Align.END, valign=Gtk.Align.START)
            act.add_css_class("actual")
            capas.add_overlay(act)
        self.append(capas)
        fila = Gtk.Box(spacing=8)
        punto = Gtk.Box(valign=Gtk.Align.START)  # color del tema (el de sus destellos)
        punto.add_css_class("punto")
        prov = Gtk.CssProvider()
        prov.load_from_string(f"box {{ background-color: {item['acento']}; }}")
        punto.get_style_context().add_provider(prov, 900)
        txt = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        nl = Gtk.Label(label=item["nombre"], xalign=0, ellipsize=3)
        nl.add_css_class("nombre")
        dl = Gtk.Label(label=item["desc"], xalign=0, ellipsize=3)
        dl.add_css_class("desc")
        txt.append(nl)
        txt.append(dl)
        fila.append(punto)
        fila.append(txt)
        self.append(fila)
        self.media = None

    def animar(self, si):
        """Solo la tarjeta seleccionada reproduce su clip; las demás muestran el póster."""
        clip = self.item["clip"]
        if si and clip and Path(clip).exists():
            if self.media is None:
                self.media = Gtk.MediaFile.new_for_filename(str(clip))
                self.media.set_loop(True)
                self.media.set_muted(True)
            self.pic.set_paintable(self.media)
            self.media.play()
        elif self.media is not None:
            self.media.pause()
            if self.item["poster"]:
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
        self.cerrando = False
        claro = self.modo == "light"
        css = Gtk.CssProvider()
        css.load_from_string(
            "@define-color acento #8b5cf6; @define-color sobre_acento #ffffff; @define-color acento_tarjeta #8b5cf6;"
            + ("@define-color velo rgba(235,230,222,0.55); @define-color panel rgba(250,247,241,0.96);"
               "@define-color borde rgba(255,255,255,1); @define-color texto #2f2b38;"
               "@define-color tarjeta rgba(60,50,40,0.05); @define-color tarjeta_sel rgba(60,50,40,0.09);"
               if claro else
               "@define-color velo rgba(5,5,12,0.6); @define-color panel rgba(20,20,28,0.95);"
               "@define-color borde rgba(255,255,255,0.08); @define-color texto #f4f2fa;"
               "@define-color tarjeta rgba(255,255,255,0.04); @define-color tarjeta_sel rgba(255,255,255,0.09);")
            + CSS)
        Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), css, 800)
        self.css_acento = Gtk.CssProvider()
        Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), self.css_acento, 850)

        self.velo = Gtk.Box(hexpand=True, vexpand=True)
        self.velo.add_css_class("velo")
        self.velo.add_css_class("oculto")
        clic_fuera = Gtk.GestureClick()
        clic_fuera.connect("released", self.clic_en_velo)
        self.velo.add_controller(clic_fuera)
        self.panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=18,
                             halign=Gtk.Align.CENTER, valign=Gtk.Align.CENTER, hexpand=True)
        self.panel.add_css_class("panel")
        self.velo.append(self.panel)

        cab = Gtk.Box(spacing=16)
        textos = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2, hexpand=True)
        t = Gtk.Label(label="Elige tu tema", xalign=0)
        t.add_css_class("titulo")
        st = Gtk.Label(label="Fondos animados en 4K · se aplica a todos tus escritorios", xalign=0)
        st.add_css_class("subtitulo")
        textos.append(t)
        textos.append(st)
        cab.append(textos)
        self.botones = {}
        for modo, etiqueta in (("dark", "🌙  Oscuros"), ("light", "☀️  Claros")):
            b = Gtk.Button(label=etiqueta, valign=Gtk.Align.CENTER)
            b.add_css_class("pestana")
            b.connect("clicked", lambda _b, m=modo: self.mostrar_pestana(m))
            cab.append(b)
            self.botones[modo] = b
        self.panel.append(cab)

        self.scroll = Gtk.ScrolledWindow(hscrollbar_policy=Gtk.PolicyType.NEVER)
        alto_tarjeta = self.tam_vista[1] + 80
        self.scroll.set_size_request(-1, min(int(alto_mon * 0.62), alto_tarjeta * (4 if self.vertical else 3)))
        self.panel.append(self.scroll)

        pie = Gtk.Box(spacing=12)
        chispa = Gtk.Label(label="✨")
        chispa.add_css_class("icono")
        lbl = Gtk.Label(label="Destellos del cursor", xalign=0)
        lbl.add_css_class("destellos-lbl")
        self.interruptor = Gtk.Switch(active=self.estilo["destellos"], valign=Gtk.Align.CENTER)
        self.interruptor.connect("notify::active", self.cambiar_destellos)
        ayuda = Gtk.Label(label="Flechas mover · Tab Oscuros/Claros · Enter aplicar · D destellos · Esc salir",
                          hexpand=True, xalign=1, wrap=True)
        ayuda.add_css_class("pie")
        for w in (chispa, lbl, self.interruptor, ayuda):
            pie.append(w)
        self.panel.append(pie)
        self.set_child(self.velo)

        teclas = Gtk.EventControllerKey()
        teclas.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)  # antes que el foco use Tab/flechas
        teclas.connect("key-pressed", self.tecla)
        self.add_controller(teclas)
        t_actual = tc.buscar(self.estilo["tema"])
        self.mostrar_pestana(t_actual["modo"] if t_actual else self.modo)

    # --- contenido ----------------------------------------------------------------------
    def items(self, modo):
        lista = []
        for tid, (nombre, desc, _icono) in tc.POR_ESCRITORIO.items():
            video = tid == "escritorios:video"
            origen = fondo_escritorio(self.cfg, modo, video)
            poster = clip = None
            if origen is not None:
                if video:
                    clip = origen
                    poster = Path(f"{tc.CACHE}/escritorio-{origen.stem}.jpg")
                    if not poster.exists():
                        tc.CACHE.mkdir(parents=True, exist_ok=True)
                        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "1", "-i", str(origen),
                                        "-frames:v", "1", "-vf", "scale=480:-2", str(poster)])
                else:
                    poster = origen
            lista.append({"id": tid, "modo": modo, "nombre": nombre, "desc": desc, "poster": poster,
                          "clip": clip, "acento": "#c9a7ff",
                          "actual": self.estilo["tema"] == tid and self.modo == modo})
        for t in tc.catalogo():
            if t["modo"] != modo:
                continue
            r = tc.rutas(t)
            lista.append({"id": t["id"], "modo": modo, "nombre": t["nombre"], "desc": "Animado · 4K",
                          "poster": r["mini"] if r["mini"].exists() else None, "clip": r["clip"],
                          "acento": tc.acento(t), "actual": self.estilo["tema"] == t["id"]})
        return lista

    def mostrar_pestana(self, modo):
        self.pestana = modo
        for m, b in self.botones.items():
            (b.add_css_class if m == modo else b.remove_css_class)("activa")
        grid = Gtk.Grid(column_spacing=14, row_spacing=14, margin_end=6)
        self.tarjetas = []
        for i, item in enumerate(self.items(modo)):
            tarjeta = Tarjeta(self, item)
            mov = Gtk.EventControllerMotion()
            mov.connect("enter", lambda *_, i=i: self.seleccionar(i, desplazar=False))
            tarjeta.add_controller(mov)
            clic = Gtk.GestureClick()
            clic.connect("released", lambda *_, i=i: self.aplicar(i))
            tarjeta.add_controller(clic)
            grid.attach(tarjeta, i % self.columnas, i // self.columnas, 1, 1)
            self.tarjetas.append(tarjeta)
        self.scroll.set_child(grid)
        self.sel = None
        self.seleccionar(next((i for i, t in enumerate(self.tarjetas) if t.item["actual"]), 0))

    def seleccionar(self, i, desplazar=True):
        if self.sel is not None and self.sel < len(self.tarjetas):
            self.tarjetas[self.sel].remove_css_class("sel")
            self.tarjetas[self.sel].animar(False)
        self.sel = i
        t = self.tarjetas[i]
        t.add_css_class("sel")
        t.animar(True)
        self.css_acento.load_from_string(f"@define-color acento_tarjeta {t.item['acento']};")
        if desplazar:
            GLib.idle_add(self.desplazar_a, t)

    def desplazar_a(self, tarjeta):
        ok, caja = tarjeta.compute_bounds(self.scroll.get_child())
        if ok:
            adj = self.scroll.get_vadjustment()
            arriba, abajo = caja.get_y(), caja.get_y() + caja.get_height()
            if arriba < adj.get_value():
                adj.set_value(arriba - 8)
            elif abajo > adj.get_value() + adj.get_page_size():
                adj.set_value(abajo - adj.get_page_size() + 8)
        return False

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
        self.estilo["destellos"] = sw.get_active()
        tc.guardar_estilo(self.estilo)

    def aplicar(self, i):
        item = self.tarjetas[i].item
        self.estilo["tema"] = item["id"]
        tc.guardar_estilo(self.estilo)  # primero el tema, luego el modo (ver escritorios-vivos)
        if item["modo"] != self.modo:
            subprocess.Popen(["noctalia", "msg", "theme-mode-set", item["modo"]],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.cerrar()

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

    def tecla(self, _ctl, keyval, _code, _state):
        nombre = Gdk.keyval_name(keyval) or ""
        n, c = len(self.tarjetas), self.columnas
        if nombre == "Escape":
            self.cerrar()
        elif nombre in ("Return", "KP_Enter", "space"):
            self.aplicar(self.sel)
        elif nombre in ("Tab", "ISO_Left_Tab"):
            self.mostrar_pestana("light" if self.pestana == "dark" else "dark")
        elif nombre in ("Right", "l"):
            self.seleccionar((self.sel + 1) % n)
        elif nombre in ("Left", "h"):
            self.seleccionar((self.sel - 1) % n)
        elif nombre in ("Down", "j"):
            self.seleccionar(min(n - 1, self.sel + c))
        elif nombre in ("Up", "k"):
            self.seleccionar(max(0, self.sel - c))
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
