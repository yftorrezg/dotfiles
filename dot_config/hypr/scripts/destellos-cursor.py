#!/usr/bin/env python3
"""destellos-cursor.py — el cursor deja una estela de chispas al moverse.

Una capa transparente (layer-shell OVERLAY, no recibe clics) por monitor. Cada ~16 ms
lee la posición del cursor por el socket de Hyprland; si se movió, suelta chispas que
caen y se apagan. Las dibuja GTK con la GPU (Gsk), no con cairo.
Para no gastar: sin movimiento la capa se oculta (cero cuadros), y en pantalla
completa (juegos, videos) se desactiva.
Color: el acento del escritorio actual (lo escribe escritorios-vivos.py en
~/.local/state/escritorios-vivos/acento), con variaciones de tono.
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
MAX_CHISPAS = 140


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
            r, g, b = c["rgb"]
            x, y, tam = c["x"] - ox, c["y"] - oy, c["tam"] * (1 - 0.5 * vida)
            # halo suave
            halo = tam * 3.2
            centro = Graphene.Point().init(x, y)
            caja = Graphene.Rect().init(x - halo, y - halo, halo * 2, halo * 2)
            snap.append_radial_gradient(caja, centro, halo, halo, 0, 1, [
                parada(0, rgba(r, g, b, 0.55 * alfa)), parada(1, rgba(r, g, b, 0))])
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
            # núcleo brillante
            n = tam * 0.7
            rr = Gsk.RoundedRect()
            rr.init_from_rect(Graphene.Rect().init(x - n, y - n, n * 2, n * 2), n)
            snap.push_rounded_clip(rr)
            snap.append_color(rgba(min(1, r + 0.35), min(1, g + 0.35), min(1, b + 0.35), alfa),
                              Graphene.Rect().init(x - n, y - n, n * 2, n * 2))
            snap.pop()


class App(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="dev.yafer.Destellos", flags=Gio.ApplicationFlags.NON_UNIQUE)
        self.chispas = []
        self.ventanas = {}     # nombre monitor -> (ventana, lienzo, geometría)
        self.ultimo = None
        self.quieto_desde = time.monotonic()
        self.pantalla_completa = False
        self.acento = (0.79, 0.65, 1.0)
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
                n = min(5, max(1, int(dist / 14)))
                for i in range(n):
                    f = i / n  # repartir a lo largo del trazo
                    self.chispas.append({
                        "x": x - dx * f + random.uniform(-3, 3), "y": y - dy * f + random.uniform(-3, 3),
                        "vx": random.uniform(-40, 40) - dx * 0.8, "vy": random.uniform(-50, 20) - dy * 0.8,
                        "t": 0.0, "dur": random.uniform(0.6, 1.1), "tam": random.uniform(2.4, 5.0),
                        "rgb": self.color(), "estrella": random.random() < 0.3,
                        "giro": random.uniform(0, 90), "mon": origen})
                del self.chispas[:-MAX_CHISPAS]
        self.ultimo = (x, y)

        for c in self.chispas:
            c["t"] += dt
            c["vy"] += 160 * dt          # gravedad suave
            c["vx"] *= 0.92
            c["vy"] *= 0.94
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
