#!/usr/bin/env python3
"""destellos-cursor.py — el cursor deja una estela de chispas al moverse.

Una capa transparente (layer-shell OVERLAY, no recibe clics) por monitor. Cada ~16 ms
lee la posición del cursor por el socket de Hyprland; si se movió, suelta chispas que
caen y se apagan. Las dibuja GTK con la GPU (Gsk), no con cairo.
Para no gastar: sin movimiento la capa se oculta (cero cuadros), y en pantalla
completa (juegos, videos) se desactiva.
Color: el acento del escritorio actual (lo escribe escritorios-vivos.py en
~/.local/state/escritorios-vivos/acento), con variaciones de tono.
Efecto: ~/.local/state/escritorios-vivos/cursor.json {"efecto": ...}; lo cambia SUPER+SHIFT+A → pestaña Cursor (estilos.py)
(chispas, llamas oscuras, fuego, brasas, humo, sakura, hielo). Se relee cada segundo.
"""
import ctypes

ctypes.CDLL("libgtk4-layer-shell.so")

import colorsys  # noqa: E402
import json  # noqa: E402
import math  # noqa: E402
import os  # noqa: E402
import random  # noqa: E402
import socket  # noqa: E402
import time  # noqa: E402
from pathlib import Path  # noqa: E402

import cairo  # noqa: E402
import gi  # noqa: E402

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
gi.require_version("Gsk", "4.0")
gi.require_version("Graphene", "1.0")
gi.require_version("Gtk4LayerShell", "1.0")
from gi.repository import Gdk, Gio, GLib, Graphene, Gsk, Gtk  # noqa: E402
from gi.repository import Gtk4LayerShell as LS  # noqa: E402

HYPR = Path(os.environ["XDG_RUNTIME_DIR"]) / "hypr" / os.environ["HYPRLAND_INSTANCE_SIGNATURE"] / ".socket.sock"
ACENTO = Path.home() / ".local/state/escritorios-vivos/acento"
CURSOR_JSON = Path.home() / ".local/state/escritorios-vivos/cursor.json"
MAX_CHISPAS = 140

# grav: aceleración vertical (negativa = sube) · freno: (x, y) por tick · n: partículas máximas por tick
# dur / tam: rangos · color: ("acento",) o rampa fija de colores sueltos
EFECTOS = {
    "chispas": dict(dibujo="chispa", grav=160, freno=(0.92, 0.94), n=5, dur=(0.6, 1.1), tam=(2.4, 5.0), estrella=0.3),
    "llamas": dict(dibujo="llama", grav=-230, freno=(0.90, 0.97), n=4, dur=(0.55, 1.0), tam=(4.5, 8.0),
                   paleta=[(0.66, 0.33, 0.97), (0.86, 0.15, 0.15), (0.75, 0.1, 0.4), (0.45, 0.1, 0.9)]),
    "fuego": dict(dibujo="llama", grav=-260, freno=(0.90, 0.97), n=4, dur=(0.5, 0.9), tam=(4.5, 8.0),
                  paleta=[(1.0, 0.55, 0.12), (1.0, 0.35, 0.1), (0.95, 0.75, 0.2), (0.85, 0.15, 0.1)]),
    "brasas": dict(dibujo="brasa", grav=-70, freno=(0.95, 0.985), n=3, dur=(0.9, 1.7), tam=(1.4, 3.0),
                   paleta=[(1.0, 0.6, 0.15), (1.0, 0.4, 0.1), (1.0, 0.8, 0.3)]),
    "humo": dict(dibujo="humo", grav=-45, freno=(0.94, 0.97), n=2, dur=(0.9, 1.6), tam=(5.0, 9.0),
                 paleta=[(0.1, 0.1, 0.12), (0.18, 0.17, 0.2)]),
    "sakura": dict(dibujo="petalo", grav=55, freno=(0.96, 0.985), n=2, dur=(1.3, 2.2), tam=(3.0, 5.0),
                   paleta=[(1.0, 0.72, 0.8), (1.0, 0.6, 0.72), (1.0, 0.85, 0.9)]),
    "hielo": dict(dibujo="chispa", grav=40, freno=(0.93, 0.96), n=4, dur=(0.7, 1.2), tam=(2.4, 4.8), estrella=0.55,
                  paleta=[(0.55, 0.85, 1.0), (0.7, 0.92, 1.0), (0.4, 0.7, 1.0)]),
}


def hypr(cmd):
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
        s.connect(str(HYPR))
        s.sendall(cmd.encode())
        data = b""
        while chunk := s.recv(65536):
            data += chunk
    return data.decode()


def parada(offset, color):
    p = Gsk.ColorStop()
    p.offset, p.color = offset, color
    return p


def rgba(r, g, b, a):
    c = Gdk.RGBA()
    c.red, c.green, c.blue, c.alpha = r, g, b, a
    return c


class Lienzo(Gtk.Widget):
    def __init__(self, app, origen):
        super().__init__()
        self.app = app
        self.origen = origen  # (x, y) lógico del monitor

    def do_snapshot(self, snap):
        ox, oy = self.origen
        for c in self.app.chispas:
            if c["mon"] != self.origen:
                continue
            vida = c["t"] / c["dur"]           # 0 → 1
            alfa = (1 - vida) ** 1.6
            x, y = c["x"] - ox, c["y"] - oy
            getattr(self, "dib_" + c["dib"])(snap, c, x, y, vida, alfa)

    @staticmethod
    def halo(snap, x, y, radio, paradas):
        centro = Graphene.Point().init(x, y)
        caja = Graphene.Rect().init(x - radio, y - radio, radio * 2, radio * 2)
        snap.append_radial_gradient(caja, centro, radio, radio, 0, 1, [parada(o, col) for o, col in paradas])

    @staticmethod
    def disco(snap, x, y, r, color):
        rr = Gsk.RoundedRect()
        rr.init_from_rect(Graphene.Rect().init(x - r, y - r, r * 2, r * 2), r)
        snap.push_rounded_clip(rr)
        snap.append_color(color, Graphene.Rect().init(x - r, y - r, r * 2, r * 2))
        snap.pop()

    def dib_chispa(self, snap, c, x, y, vida, alfa):
        r, g, b = c["rgb"]
        tam = c["tam"] * (1 - 0.5 * vida)
        self.halo(snap, x, y, tam * 3.2, [(0, rgba(r, g, b, 0.55 * alfa)), (1, rgba(r, g, b, 0))])
        # destello en cruz (estrellita de 4 puntas) para las chispas "estrella"
        if c["estrella"]:
            largo, grosor = tam * 2.6, max(1.0, tam * 0.32)
            blanco = rgba(1, 1, 1, 0.9 * alfa)
            snap.save()
            snap.translate(Graphene.Point().init(x, y))
            snap.rotate(c["giro"] + vida * 90)
            for w, h in ((largo, grosor), (grosor, largo)):
                snap.append_color(blanco, Graphene.Rect().init(-w / 2, -h / 2, w, h))
            snap.restore()
        self.disco(snap, x, y, tam * 0.7, rgba(min(1, r + 0.35), min(1, g + 0.35), min(1, b + 0.35), alfa))

    def dib_llama(self, snap, c, x, y, vida, alfa):
        """Lengua de fuego (alargada, se mece al subir). 'oscura': centro negro y borde encendido que acaba
        en ceniza; 'viva' (fuego): centro claro y caliente."""
        r, g, b = c["rgb"]
        k = vida ** 1.3                      # el color se apaga hacia negro-rojizo
        r, g, b = r * (1 - 0.7 * k), g * (1 - 0.7 * k), b * (1 - 0.7 * k)
        tam = c["tam"] * (0.55 + 0.9 * math.sin(math.pi * min(1, vida * 1.1)))
        a = min(1, alfa * 1.3)
        if c["oscura"]:
            centro = [(0, rgba(0.02, 0.0, 0.05, 0.9 * a)), (0.35, rgba(0.04, 0.0, 0.07, 0.72 * a)),
                      (0.6, rgba(r, g, b, 0.7 * a)), (0.85, rgba(r, g, b, 0.25 * a)), (1, rgba(r, g, b, 0))]
        else:
            centro = [(0, rgba(1, 0.95, 0.7, 0.95 * a)), (0.3, rgba(1, min(1, g + 0.25), 0.25, 0.85 * a)),
                      (0.65, rgba(r, g, b, 0.5 * a)), (1, rgba(r, g, b, 0))]
        snap.save()
        snap.translate(Graphene.Point().init(x, y))
        snap.rotate(12 * math.sin(c["t"] * 13 + c["giro"]))          # se mece como llama
        snap.scale(0.7, 1.55)                                        # alargada hacia arriba
        self.halo(snap, 0, -tam * 0.4, tam * 2.2, centro)
        snap.restore()

    def dib_brasa(self, snap, c, x, y, vida, alfa):
        r, g, b = c["rgb"]
        parpadeo = 0.65 + 0.35 * math.sin(c["t"] * 28 + c["giro"])
        tam = c["tam"] * (1 - 0.6 * vida)
        self.halo(snap, x, y, tam * 3.0, [(0, rgba(r, g, b, 0.5 * alfa * parpadeo)), (1, rgba(r, g, b, 0))])
        self.disco(snap, x, y, tam * 0.8, rgba(1, min(1, g + 0.3), min(1, b + 0.3), alfa * parpadeo))

    def dib_humo(self, snap, c, x, y, vida, alfa):
        r, g, b = c["rgb"]
        tam = c["tam"] * (1 + 1.6 * vida)
        self.halo(snap, x, y, tam * 2.0, [(0, rgba(r, g, b, 0.55 * alfa)), (1, rgba(r, g, b, 0))])

    def dib_petalo(self, snap, c, x, y, vida, alfa):
        r, g, b = c["rgb"]
        tam = c["tam"]
        snap.save()
        snap.translate(Graphene.Point().init(x, y))
        snap.rotate(c["giro"] + vida * 280)
        w, h = tam * 2.2, tam * (0.9 + 0.5 * math.sin(vida * 14 + c["giro"]))   # aletea al caer
        h = max(1.0, abs(h))
        rr = Gsk.RoundedRect()
        rr.init_from_rect(Graphene.Rect().init(-w / 2, -h / 2, w, h), h / 2)
        snap.push_rounded_clip(rr)
        snap.append_color(rgba(r, g, b, 0.95 * alfa), Graphene.Rect().init(-w / 2, -h / 2, w, h))
        snap.pop()
        snap.restore()


class App(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="dev.yafer.Destellos", flags=Gio.ApplicationFlags.NON_UNIQUE)
        self.chispas = []
        self.ventanas = {}     # nombre monitor -> (ventana, lienzo, geometría)
        self.ultimo = None
        self.quieto_desde = time.monotonic()
        self.pantalla_completa = False
        self.acento = (0.79, 0.65, 1.0)
        self.efecto = "chispas"
        self.t_prev = time.monotonic()

    def do_activate(self):
        self.hold()
        self.crear_ventanas()
        Gdk.Display.get_default().get_monitors().connect("items-changed", lambda *_: self.crear_ventanas())
        GLib.timeout_add(16, self.tick)
        GLib.timeout_add(1000, self.revisar_entorno)
        self.revisar_entorno()

    def crear_ventanas(self):
        for v, _, _ in self.ventanas.values():
            v.destroy()
        self.ventanas.clear()
        try:
            mons = {m["name"]: m for m in json.loads(hypr("j/monitors"))}
        except (OSError, ValueError):
            return
        for gm in Gdk.Display.get_default().get_monitors():
            m = mons.get(gm.get_connector())
            if not m:
                continue
            ancho, alto = m["width"], m["height"]
            if m.get("transform", 0) % 2 == 1:
                ancho, alto = alto, ancho
            geo = (m["x"], m["y"], ancho / m["scale"], alto / m["scale"])
            v = Gtk.Window(application=self)
            v.set_css_classes(["destellos"])
            LS.init_for_window(v)
            LS.set_namespace(v, "destellos")
            LS.set_layer(v, LS.Layer.OVERLAY)
            LS.set_keyboard_mode(v, LS.KeyboardMode.NONE)
            LS.set_exclusive_zone(v, -1)
            LS.set_monitor(v, gm)
            for borde in (LS.Edge.TOP, LS.Edge.BOTTOM, LS.Edge.LEFT, LS.Edge.RIGHT):
                LS.set_anchor(v, borde, True)
            lienzo = Lienzo(self, (geo[0], geo[1]))
            v.set_child(lienzo)
            v.connect("realize", lambda w: w.get_surface().set_input_region(cairo.Region()))
            self.ventanas[m["name"]] = (v, lienzo, geo)
        css = Gtk.CssProvider()
        css.load_from_string("window.destellos { background: transparent; }")
        Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), css, 800)

    def revisar_entorno(self):
        try:
            w = json.loads(hypr("j/activewindow") or "{}")
            self.pantalla_completa = bool(w.get("fullscreen"))
        except (OSError, ValueError):
            self.pantalla_completa = False
        try:
            e = json.loads(CURSOR_JSON.read_text()).get("efecto", "chispas")
            self.efecto = e if e in EFECTOS else "chispas"
        except (OSError, ValueError):
            self.efecto = "chispas"
        try:
            h = ACENTO.read_text().strip()
            self.acento = tuple(int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))
        except (OSError, ValueError):
            pass
        return True

    def monitor_de(self, x, y):
        for nombre, (_, _, (mx, my, mw, mh)) in self.ventanas.items():
            if mx <= x < mx + mw and my <= y < my + mh:
                return nombre
        return None

    def color(self):
        paleta = EFECTOS[self.efecto].get("paleta")
        if paleta:
            r, g, b = random.choice(paleta)
            v = random.uniform(0.85, 1.1)
            return min(1, r * v), min(1, g * v), min(1, b * v)
        h, l, s = colorsys.rgb_to_hls(*self.acento)
        h = (h + random.uniform(-0.08, 0.08)) % 1
        return colorsys.hls_to_rgb(h, min(0.82, max(0.55, l + random.uniform(-0.05, 0.15))), min(1, s + 0.1))

    def tick(self):
        ahora = time.monotonic()
        # Ratón quieto y sin chispas: consultar solo 1 de cada 4 ticks (~15/s) para no gastar
        self.n_tick = getattr(self, "n_tick", 0) + 1
        if not self.chispas and ahora - self.quieto_desde > 1.5 and self.n_tick % 4:
            return True
        dt = min(0.05, ahora - self.t_prev)
        self.t_prev = ahora
        try:
            x, y = (float(v) for v in hypr("cursorpos").split(","))
        except (OSError, ValueError):
            return True
        if self.ultimo and not self.pantalla_completa:
            dx, dy = x - self.ultimo[0], y - self.ultimo[1]
            dist = math.hypot(dx, dy)
            mon = self.monitor_de(x, y)
            if dist > 1.5:
                self.quieto_desde = ahora
            if dist > 1.5 and mon:
                origen = self.ventanas[mon][1].origen
                ef = EFECTOS[self.efecto]
                n = min(ef["n"], max(1, int(dist / 14)))
                for i in range(n):
                    f = i / n  # repartir a lo largo del trazo
                    self.chispas.append({
                        "x": x - dx * f + random.uniform(-3, 3), "y": y - dy * f + random.uniform(-3, 3),
                        "vx": random.uniform(-40, 40) - dx * 0.8, "vy": random.uniform(-50, 20) - dy * 0.8,
                        "t": 0.0, "dur": random.uniform(*ef["dur"]), "tam": random.uniform(*ef["tam"]),
                        "rgb": self.color(), "estrella": random.random() < ef.get("estrella", 0),
                        "giro": random.uniform(0, 90), "mon": origen, "dib": ef["dibujo"],
                        "grav": ef["grav"], "freno": ef["freno"], "oscura": self.efecto == "llamas"})
                del self.chispas[:-MAX_CHISPAS]
        self.ultimo = (x, y)

        for c in self.chispas:
            c["t"] += dt
            c["vy"] += c["grav"] * dt    # gravedad suave (negativa = sube, como el fuego)
            c["vx"] *= c["freno"][0]
            c["vy"] *= c["freno"][1]
            c["x"] += c["vx"] * dt
            c["y"] += c["vy"] * dt
        self.chispas = [c for c in self.chispas if c["t"] < c["dur"]]

        activos = {c["mon"] for c in self.chispas}
        for v, lienzo, geo in self.ventanas.values():
            if lienzo.origen in activos:
                if not v.get_visible():
                    v.present()
                lienzo.queue_draw()
            elif v.get_visible():
                lienzo.queue_draw()
                v.set_visible(False)
        return True


if __name__ == "__main__":
    App().run(None)
