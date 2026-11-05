#!/usr/bin/env python3
"""anillo.py — anillo radial del MX Master 4 (como el "Actions Ring" de Logi Options+, pero por programa).

Mantienes el panel háptico → aparece un anillo de 12 burbujas bajo el cursor con las acciones del programa
que tiene el foco → mueves el mouse hacia una (el mouse vibra al cambiar) → sueltas y se ejecuta.
Las burbujas con un puntito tienen sub-opciones: aleja más el mouse en esa dirección y salen en un arco.
  · soltar en el centro = cancelar          · toque corto = queda abierto; eliges con click (click en el centro cierra)
  · rueda sobre una burbuja = su ajuste (volumen, zoom, pestañas…) · rueda en el centro = volumen

Qué hay en cada programa: anillo_apps.py.

    anillo.py --demonio     servicio (autostart). Lee el botón háptico directo del mouse (hidraw, HID++)
    anillo.py abrir|soltar|cancelar    control manual (atajo SUPER+ALT+O)
Probar sin tocar nada:  ANILLO_PRUEBA=1 [ANILLO_APP=Brave] [ANILLO_SEL=4 | 4.1] python3 anillo.py --demonio
"""
import math
import os
import socket
import sys
import time

SOCK = os.path.join(os.environ.get("XDG_RUNTIME_DIR", "/tmp"), "anillo.sock")

if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] in ("abrir", "soltar", "cancelar"):
    try:  # cliente: sin GTK, tarda pocos ms
        socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM).sendto(sys.argv[1].encode(), SOCK)
    except OSError as e:
        print(f"anillo: el servicio no está corriendo ({e})", file=sys.stderr)
        sys.exit(1)
    sys.exit(0)

# ---- Geometría (px lógicos) ------------------------------------------------------------------------
N = 12
PASO = 360 / N
R1 = 150            # centro → burbujas
RB = 30             # radio de burbuja
R2 = 236            # centro → sub-opciones
RS = 23             # radio de sub-opción
SUB_PASO = 25       # grados entre sub-opciones
HUB = 56            # disco central
ZONA_MUERTA = 34    # dentro = cancelar
UMBRAL_SUB = (R1 + R2) / 2 + 6
LADO = int(2 * (R2 + RS * 1.35 + 30))
TOQUE_S = 0.28
AUTOCIERRE_S = 8
ONDA_ABRIR, ONDA_CAMBIO, ONDA_SUB, ONDA_EJECUTAR = 0, 4, 0x1B, 7   # formas de onda HID++ del motor háptico
CID_HAPTICO = 0x01A0


def angulo(dx, dy):
    """0° = arriba, sentido horario."""
    return math.degrees(math.atan2(dx, -dy)) % 360


def dif_ang(a, b):
    return (a - b + 180) % 360 - 180


def angulos_sub(i, n):
    base = i * PASO
    return [base + (k - (n - 1) / 2) * SUB_PASO for k in range(n)]


def seleccion(dx, dy, sectores, sub_abierto):
    """(sector, sub) elegidos por el desplazamiento desde el punto de partida."""
    d = math.hypot(dx, dy)
    if d < ZONA_MUERTA:
        return None, None
    a = angulo(dx, dy)
    if sub_abierto is not None and d > UMBRAL_SUB:
        angs = angulos_sub(sub_abierto, len(sectores[sub_abierto]["sub"]))
        mejor = min(range(len(angs)), key=lambda k: abs(dif_ang(a, angs[k])))
        if abs(dif_ang(a, angs[mejor])) <= SUB_PASO * 0.85:
            return sub_abierto, mejor
    return int((a + PASO / 2) // PASO) % N, None


def _log(msg):
    try:
        p = os.path.expanduser("~/.local/state/mx-accion.log")
        with open(p, "a") as f:
            f.write(time.strftime("%H:%M:%S ") + "anillo: " + msg + "\n")
    except OSError:
        pass


def _importar_mx():
    import importlib.util
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mx-accion.py")
    spec = importlib.util.spec_from_file_location("mx_accion", ruta)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def ease_out_back(t, c=1.55):
    t = max(0.0, min(1.0, t))
    return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2


def ease_out(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def color_sector(tono, i, claro=0.0):
    import colorsys
    h = ((tono + i * PASO) % 360) / 360
    r, g, b = colorsys.hls_to_rgb(h, 0.47 + 0.16 * claro, 0.62 + 0.1 * claro)
    return r, g, b


# ---- El mouse: botón háptico + motor, por HID++ directo ----------------------------------------------
class Mouse:
    """Lee el panel háptico (CID 0x1A0, desviado) y hace vibrar el motor. Se reconecta solo."""

    def __init__(self, GLib, al_pulsar, al_soltar):
        self.GLib = GLib
        self.al_pulsar, self.al_soltar = al_pulsar, al_soltar
        self.fd = None
        self.watch = None
        self.disp = 0xFF
        self.f_hap = self.f_rep = self.f_wds = None
        self.pulsado = False
        self.ultimo = 0.0
        GLib.timeout_add_seconds(3, self._vigilar)
        self.conectar()

    def _buscar(self):
        import glob
        for ruta in sorted(glob.glob("/sys/class/hidraw/hidraw*")):
            try:
                with open(ruta + "/device/uevent") as f:
                    u = f.read().upper()
            except OSError:
                continue
            if "046D" in u and "B042" in u:
                return "/dev/" + os.path.basename(ruta)
        return None

    def _tx(self, feat, fn, *p, swid=0x05):
        b = bytearray(20)
        b[0], b[1], b[2], b[3] = 0x11, self.disp, feat, (fn << 4) | swid
        b[4:4 + len(p)] = bytes(p)
        os.write(self.fd, bytes(b))

    def _pedir(self, feat, fn, *p, espera=0.5):
        import select
        self._tx(feat, fn, *p)
        fin = time.time() + espera
        while time.time() < fin:
            r, _, _ = select.select([self.fd], [], [], 0.05)
            if not r:
                continue
            try:
                d = os.read(self.fd, 64)
            except BlockingIOError:
                continue
            if len(d) >= 4 and d[0] == 0x11 and d[2] == feat and d[3] == ((fn << 4) | 0x05):
                return d
            if len(d) >= 4 and d[0] == 0x11 and d[2] == 0xFF:
                return None  # error HID++
            self._procesar(d)
        return None

    def _indice(self, feature):
        d = self._pedir(0x00, 0, feature >> 8, feature & 0xFF)
        return d[4] if d and d[4] else None

    def conectar(self):
        ruta = self._buscar()
        if not ruta:
            return
        try:
            self.fd = os.open(ruta, os.O_RDWR | os.O_NONBLOCK)
            self.f_hap = self._indice(0x19B0)
            self.f_rep = self._indice(0x1B04)
            self.f_wds = self._indice(0x1D4B)
            if self.f_rep is None:
                raise OSError("el mouse no respondió")
            self._desviar()
            self.watch = self.GLib.io_add_watch(
                self.fd, self.GLib.IO_IN | self.GLib.IO_HUP | self.GLib.IO_ERR, self._leer)
            _log(f"mouse conectado {ruta} haptic={self.f_hap} reprog={self.f_rep}")
        except OSError as e:
            _log(f"mouse: {e}")
            self._perder()

    def _desviar(self):
        # setCidReporting(CID háptico, divert=1 + dvalid) para recibir pulsar/soltar aquí
        if self.fd is not None and self.f_rep is not None:
            self._tx(self.f_rep, 3, CID_HAPTICO >> 8, CID_HAPTICO & 0xFF, 0x03)

    def _perder(self):
        if self.watch:
            self.GLib.source_remove(self.watch)
        self.watch = None
        if self.fd is not None:
            try:
                os.close(self.fd)
            except OSError:
                pass
        self.fd = None
        if self.pulsado:
            self.pulsado = False
            self.al_soltar()

    def _vigilar(self):
        if self.fd is None:
            self.conectar()
        return True

    def _leer(self, _fd, cond):
        if cond & (self.GLib.IO_HUP | self.GLib.IO_ERR):
            self._perder()
            return False
        try:
            while True:
                self._procesar(os.read(self.fd, 64))
        except BlockingIOError:
            pass
        except OSError:
            self._perder()
            return False
        return True

    def _procesar(self, d):
        if len(d) < 12 or d[0] != 0x11 or (d[3] & 0x0F) != 0:
            return
        if d[2] == self.f_rep and d[3] >> 4 == 0:      # divertedButtonsEvent: CIDs pulsados ahora
            cids = {(d[4 + 2 * k] << 8) | d[5 + 2 * k] for k in range(4)}
            p = CID_HAPTICO in cids
            if p != self.pulsado:
                self.pulsado = p
                (self.al_pulsar if p else self.al_soltar)()
        elif d[2] == self.f_wds:                        # se reconectó: volver a desviar el botón
            self.GLib.timeout_add(400, lambda: (self._desviar(), False)[1])

    def pulso(self, onda, min_gap=0.03):
        ahora = time.time()
        if self.fd is None or self.f_hap is None or ahora - self.ultimo < min_gap:
            return
        self.ultimo = ahora
        try:
            self._tx(self.f_hap, 4, onda)
        except OSError:
            pass


def demonio():
    import ctypes
    ctypes.CDLL("libgtk4-layer-shell.so")
    import json
    import queue
    import subprocess
    import threading

    import gi
    gi.require_version("Gtk", "4.0")
    gi.require_version("Gdk", "4.0")
    gi.require_version("Gsk", "4.0")
    gi.require_version("Graphene", "1.0")
    gi.require_version("Gtk4LayerShell", "1.0")
    from gi.repository import Gdk, GLib, GObject, Graphene, Gsk, Gtk, Pango
    from gi.repository import Gtk4LayerShell as LS

    import anillo_apps as apps

    mx = _importar_mx()
    prueba = bool(os.environ.get("ANILLO_PRUEBA"))
    HYPR = os.path.join(os.environ["XDG_RUNTIME_DIR"], "hypr",
                        os.environ.get("HYPRLAND_INSTANCE_SIGNATURE", ""), ".socket.sock")

    def hypr(cmd):
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect(HYPR)
            s.sendall(f"j/{cmd}".encode())
            datos = b""
            while True:
                trozo = s.recv(65536)
                if not trozo:
                    break
                datos += trozo
        return json.loads(datos)

    # -- acciones en un hilo aparte (ydotool tarda ~40 ms; la animación no se traba) --
    cola = queue.Queue()

    def correr(acc):
        if acc is None:
            return
        if isinstance(acc, list):
            for a in acc:
                correr(a)
                time.sleep(0.03)
            return
        if isinstance(acc, tuple) and acc[0] == "esperar":
            subprocess.run(acc[1], timeout=120, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return
        mx.ejecutar(acc)

    def trabajador():
        while True:
            acc = cola.get()
            try:
                correr(acc)
            except Exception as e:
                _log(f"acción {acc!r} falló: {e}")

    threading.Thread(target=trabajador, daemon=True).start()

    # -- utilidades de dibujo --
    def rgba(r, g, b, a=1.0):
        c = Gdk.RGBA()
        c.red, c.green, c.blue, c.alpha = r, g, b, a
        return c

    # Ojo: Graphene.Rect().init(...) encadenado devuelve una copia que PyGObject puede liberar → basura.
    def punto(x, y):
        p = Graphene.Point()
        p.init(x, y)
        return p

    def rect(x, y, w, h):
        r = Graphene.Rect()
        r.init(x, y, w, h)
        return r

    def circ(x, y, r):
        rr = Gsk.RoundedRect()
        rr.init_from_rect(rect(x - r, y - r, 2 * r, 2 * r), r)
        return rr

    def paradas(*pares):
        out = []
        for off, col in pares:
            s = Gsk.ColorStop()
            s.offset, s.color = off, col
            out.append(s)
        return out

    temas = []
    for nombre in ("Papirus-Dark", "Adwaita"):
        t = Gtk.IconTheme.new()
        t.set_theme_name(nombre)
        temas.append(t)
    cache_iconos = {}

    def icono(nombre, tam):
        clave = (nombre, tam)
        if clave not in cache_iconos:
            p = None
            for t in temas:
                if t.has_icon(nombre + "-symbolic"):
                    p = t.lookup_icon(nombre + "-symbolic", None, tam, 2, Gtk.TextDirection.NONE,
                                      Gtk.IconLookupFlags(0))
                    break
            cache_iconos[clave] = p
        return cache_iconos[clave]

    BLANCO = rgba(1, 1, 1, 1)

    class Lienzo(Gtk.Widget):
        __gtype_name__ = "AnilloLienzo"

        def __init__(self, anillo):
            super().__init__()
            self.a = anillo
            self.fuentes = {}

        def fuente(self, desc):
            if desc not in self.fuentes:
                self.fuentes[desc] = Pango.FontDescription.from_string(desc)
            return self.fuentes[desc]

        def texto(self, snap, txt, desc, cx, cy, ancho, color):
            lay = self.create_pango_layout(txt)
            lay.set_font_description(self.fuente(desc))
            lay.set_width(int(ancho * Pango.SCALE))
            lay.set_alignment(Pango.Alignment.CENTER)
            lay.set_wrap(Pango.WrapMode.WORD_CHAR)
            lay.set_ellipsize(Pango.EllipsizeMode.END)
            lay.set_height(-2)
            _, alto = lay.get_pixel_size()
            snap.save()
            snap.translate(punto(cx - ancho / 2, cy - alto / 2))
            snap.append_layout(lay, color)
            snap.restore()

        def dibujar_icono(self, snap, nombre, x, y, tam, alfa):
            p = icono(nombre, tam)
            if p is None:
                return
            snap.save()
            snap.translate(punto(x - tam / 2, y - tam / 2))
            p.snapshot_symbolic(snap, tam, tam, [rgba(1, 1, 1, alfa)])
            snap.restore()

        def burbuja(self, snap, x, y, r, col, hv, alfa, nombre_icono, tam_icono, con_sub, ang, osc=1.0):
            cr, cg, cb = (v * osc for v in col)
            c = circ(x, y, r)
            snap.push_opacity(alfa)
            snap.append_outset_shadow(c, rgba(0, 0, 0, 0.45), 0, 4, 0, 12)
            if hv > 0.01:
                snap.append_outset_shadow(c, rgba(cr, cg, cb, 0.85 * hv), 0, 0, 2 * hv, 22 * hv)
            snap.push_rounded_clip(c)
            k = 0.22 + 0.25 * hv
            claro = rgba(cr + (1 - cr) * k, cg + (1 - cg) * k, cb + (1 - cb) * k, 1)
            snap.append_linear_gradient(rect(x - r, y - r, 2 * r, 2 * r), punto(x, y - r), punto(x, y + r),
                                        paradas((0, claro), (1, rgba(cr * 0.82, cg * 0.82, cb * 0.82, 1))))
            # brillo de vidrio arriba
            snap.append_radial_gradient(rect(x - r, y - r, 2 * r, 2 * r), punto(x - r * 0.25, y - r * 0.55),
                                        r * 0.9, r * 0.6, 0, 1,
                                        paradas((0, rgba(1, 1, 1, 0.28)), (1, rgba(1, 1, 1, 0))))
            snap.pop()
            w = 1.2 + 1.3 * hv
            bc = rgba(1, 1, 1, 0.16 + 0.6 * hv)
            snap.append_border(c, [w] * 4, [bc] * 4)
            self.dibujar_icono(snap, nombre_icono, x, y, tam_icono, 0.75 + 0.25 * osc)
            if con_sub:  # puntito = tiene sub-opciones (como en Logi Options+)
                a = math.radians(ang)
                px, py = x + (r + 6) * math.sin(a), y - (r + 6) * math.cos(a)
                pc = circ(px, py, 3.6)
                snap.push_rounded_clip(pc)
                snap.append_color(rgba(1, 1, 1, 0.92), rect(px - 4, py - 4, 8, 8))
                snap.pop()
            snap.pop()

        def do_snapshot(self, snap):
            a = self.a
            if not a.visible:
                return
            cx, cy = LADO / 2, LADO / 2
            t_ab = a.t_abre
            fade = ease_out(t_ab * 1.6) * (1 - ease_out(a.t_cierre))
            escala = 0.92 + 0.08 * ease_out(t_ab) - 0.06 * a.t_cierre
            snap.save()
            snap.translate(punto(cx, cy))
            snap.scale(escala, escala)
            snap.translate(punto(-cx, -cy))
            snap.push_opacity(max(0.0, fade))

            # velo circular que crece cuando hay sub-opciones
            rv = a.r_velo
            snap.append_radial_gradient(rect(cx - rv, cy - rv, 2 * rv, 2 * rv), punto(cx, cy), rv, rv, 0, 1,
                                        paradas((0, rgba(0.03, 0.03, 0.06, 0.82)),
                                                (0.80, rgba(0.03, 0.03, 0.06, 0.70)),
                                                (1, rgba(0.03, 0.03, 0.06, 0))))
            # haz de luz desde el centro hacia la selección
            if a.haz > 0.01:
                hr, hg, hb = a.col_haz
                rb = R2 + RS + 12 if a.sub_vis is not None and a.t_sub > 0.2 else R1 + RB + 16
                snap.push_rounded_clip(circ(cx, cy, rb))
                snap.append_conic_gradient(rect(cx - rb, cy - rb, 2 * rb, 2 * rb), punto(cx, cy), a.ang_haz - 20,
                                           paradas((0, rgba(hr, hg, hb, 0)), (20 / 360, rgba(hr, hg, hb, 0.42 * a.haz)),
                                                   (40 / 360, rgba(hr, hg, hb, 0)), (1, rgba(hr, hg, hb, 0))))
                snap.pop()
            # pista fina del anillo
            snap.append_border(circ(cx, cy, R1), [1.2] * 4, [rgba(1, 1, 1, 0.07)] * 4)

            secs = a.sectores
            orden = sorted(range(N), key=lambda i: a.hv[i])
            for i in orden:
                ti = ease_out_back((t_ab * 0.24 - i * 0.011) / 0.17)
                if ti <= 0:
                    continue
                ang = i * PASO
                rad = math.radians(ang)
                d = R1 * (0.55 + 0.45 * ti)
                x, y = cx + d * math.sin(rad), cy - d * math.cos(rad)
                hv = a.hv[i]
                osc = 1.0 - 0.38 * a.foco * (1 - hv)
                r = RB * (0.35 + 0.65 * ti) * (1 + 0.24 * hv + 0.12 * a.flash[i])
                self.burbuja(snap, x, y, r, a.colores[i], hv, min(1.0, ti * 1.5),
                             secs[i]["icono"], int(22 * (1 + 0.14 * hv)), bool(secs[i]["sub"]), ang, osc)

            # sub-opciones en arco exterior
            p = a.sub_vis
            if p is not None and a.t_sub > 0.01:
                subs = secs[p]["sub"]
                for k, ang in enumerate(angulos_sub(p, len(subs))):
                    tk = ease_out_back((a.t_sub * 0.2 - k * 0.018) / 0.14)
                    if tk <= 0:
                        continue
                    rad = math.radians(ang)
                    pr = math.radians(p * PASO)
                    d = R1 + (R2 - R1) * tk
                    x = cx + (R1 * math.sin(pr)) * (1 - tk) + d * math.sin(rad) * tk
                    y = cy - (R1 * math.cos(pr)) * (1 - tk) - d * math.cos(rad) * tk
                    hv = a.hv_sub[k] if k < len(a.hv_sub) else 0
                    r = RS * (0.4 + 0.6 * tk) * (1 + 0.26 * hv)
                    col = color_sector(a.tono, p, 0.35 + 0.5 * hv)
                    self.burbuja(snap, x, y, r, col, hv, min(1.0, tk * 1.4), subs[k]["icono"],
                                 int(17 * (1 + 0.15 * hv)), False, ang)

            # centro
            hc = circ(cx, cy, HUB * (0.7 + 0.3 * ease_out(t_ab * 1.3)))
            snap.append_outset_shadow(hc, rgba(0, 0, 0, 0.55), 0, 6, 0, 26)
            snap.push_rounded_clip(hc)
            snap.append_linear_gradient(rect(cx - HUB, cy - HUB, 2 * HUB, 2 * HUB), punto(cx, cy - HUB),
                                        punto(cx, cy + HUB),
                                        paradas((0, rgba(0.16, 0.16, 0.21, 0.97)), (1, rgba(0.07, 0.07, 0.1, 0.97))))
            snap.pop()
            ac = color_sector(a.tono, 0, 0.3)
            snap.append_border(hc, [1.4] * 4, [rgba(*ac, 0.55)] * 4)
            elegido = a.elegido()
            if elegido:
                self.dibujar_icono(snap, elegido["icono"], cx, cy - 15, 24, 1)
                self.texto(snap, elegido["nombre"], "Sans Bold 9", cx, cy + 16, HUB * 1.62, BLANCO)
            else:
                self.texto(snap, a.nombre_app, "Sans Bold 10.5", cx, cy - 7, HUB * 1.7, rgba(*ac, 1))
                self.texto(snap, "×  soltar = salir", "Sans 7.5", cx, cy + 13, HUB * 1.7, rgba(1, 1, 1, 0.55))
            # indicador que orbita el centro
            if a.haz > 0.01:
                ra = math.radians(a.ang_haz)
                ix, iy = cx + (HUB + 7) * math.sin(ra), cy - (HUB + 7) * math.cos(ra)
                ic = circ(ix, iy, 3.2)
                snap.push_rounded_clip(ic)
                snap.append_color(rgba(*a.col_haz, a.haz), rect(ix - 4, iy - 4, 8, 8))
                snap.pop()
            snap.pop()
            snap.restore()

    class Anillo:
        def __init__(self):
            self.visible = False
            self.cerrando = False
            self.tick_id = None
            self.monitor = None
            self.sectores = apps.GLOBAL["sectores"]
            self.tono = apps.GLOBAL["tono"]
            self.nombre_app = ""
            self._reset()
            w = Gtk.Window()
            self.win = w
            w.set_decorated(False)
            w.set_default_size(LADO, LADO)
            LS.init_for_window(w)
            LS.set_namespace(w, "anillo")
            LS.set_layer(w, LS.Layer.OVERLAY)
            LS.set_keyboard_mode(w, LS.KeyboardMode.NONE)
            LS.set_anchor(w, LS.Edge.TOP, True)
            LS.set_anchor(w, LS.Edge.LEFT, True)
            LS.set_exclusive_zone(w, -1)
            css = Gtk.CssProvider()
            css.load_from_string("window.anillo, window.anillo > * { background: transparent; box-shadow: none; }")
            Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), css,
                                                      Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
            w.add_css_class("anillo")
            self.lienzo = Lienzo(self)
            self.lienzo.set_size_request(LADO, LADO)
            w.set_child(self.lienzo)
            mov = Gtk.EventControllerMotion()
            mov.connect("motion", self.al_mover)
            mov.connect("enter", self.al_mover)
            self.lienzo.add_controller(mov)
            clic = Gtk.GestureClick()
            clic.set_button(0)
            clic.connect("pressed", self.al_clic)
            self.lienzo.add_controller(clic)
            rueda = Gtk.EventControllerScroll.new(Gtk.EventControllerScrollFlags.VERTICAL
                                                  | Gtk.EventControllerScrollFlags.DISCRETE)
            rueda.connect("scroll", self.al_rodar)
            self.lienzo.add_controller(rueda)

        def _reset(self):
            self.sel = self.sub = None
            self.sub_abierto = None
            self.sub_vis = None
            self.t_abre = 0.0
            self.t_cierre = 0.0
            self.t_sub = 0.0
            self.hv = [0.0] * N
            self.flash = [0.0] * N
            self.hv_sub = [0.0] * 8
            self.foco = 0.0
            self.haz = 0.0
            self.ang_haz = 0.0
            self.col_haz = (1, 1, 1)
            self.r_velo = R1 + RB + 40
            self.toque = False
            self.ax = self.ay = LADO / 2
            self.t0 = self.actividad = time.time()

        def elegido(self):
            if self.sel is None:
                return None
            s = self.sectores[self.sel]
            return s["sub"][self.sub] if self.sub is not None else s

        # -- abrir / cerrar --
        def abrir(self):
            if self.visible and not self.cerrando:
                self.toque = False            # pulsó otra vez en modo toque: vuelve a "mantener y soltar"
                self.t0 = self.actividad = time.time()
                return
            try:
                cur = hypr("cursorpos")
                mons = hypr("monitors")
                act = hypr("activewindow") or {}
            except Exception as e:
                _log(f"abrir: Hyprland no respondió ({e})")
                return
            if os.environ.get("ANILLO_APP"):
                perfil = next((p for p in apps.PERFILES if p["nombre"] == os.environ["ANILLO_APP"]), apps.GLOBAL)
            else:
                perfil = apps.perfil_para(act.get("class", ""), act.get("title", ""))
            mon = None
            for m in mons:
                w, h = m["width"] / m["scale"], m["height"] / m["scale"]
                if m.get("transform", 0) % 2:
                    w, h = h, w
                if m["x"] <= cur["x"] < m["x"] + w and m["y"] <= cur["y"] < m["y"] + h:
                    mon, mw, mh = m, w, h
                    break
            if mon is None:
                m = mons[0]
                mon, mw, mh = m, m["width"] / m["scale"], m["height"] / m["scale"]
            if self.visible:                  # estaba cerrándose: ocultar ya
                self._ocultar()
            self._reset()
            self.sectores = perfil["sectores"]
            self.tono = perfil["tono"]
            self.nombre_app = perfil["nombre"]
            self.colores = [color_sector(self.tono, i) for i in range(N)]
            px, py = cur["x"] - mon["x"], cur["y"] - mon["y"]
            izq = int(min(max(px - LADO / 2, 0), mw - LADO))
            arr = int(min(max(py - LADO / 2, 0), mh - LADO))
            self.ax, self.ay = px - izq, py - arr          # dónde está el puntero dentro del anillo
            LS.set_margin(self.win, LS.Edge.LEFT, izq)
            LS.set_margin(self.win, LS.Edge.TOP, arr)
            if mon["name"] != self.monitor:
                mons_gdk = Gdk.Display.get_default().get_monitors()
                for i in range(mons_gdk.get_n_items()):
                    g = mons_gdk.get_item(i)
                    if g.get_connector() == mon["name"]:
                        LS.set_monitor(self.win, g)
                        self.monitor = mon["name"]
            self.visible = True
            self.cerrando = False
            self.win.set_visible(True)
            if self.tick_id is None:
                self._t = None
                self.tick_id = self.lienzo.add_tick_callback(self.tick)
            raton.pulso(ONDA_ABRIR, 0)
            _log(f"abrir {perfil['nombre']} ({act.get('class', '')})")

        def cerrar(self):
            if self.visible and not self.cerrando:
                self.cerrando = True

        def _ocultar(self):
            self.visible = False
            self.cerrando = False
            self.win.set_visible(False)
            if self.tick_id is not None:
                self.lienzo.remove_tick_callback(self.tick_id)
                self.tick_id = None

        def soltar(self):
            if not self.visible or self.cerrando:
                return
            if self.sel is None and not self.toque and time.time() - self.t0 < TOQUE_S:
                self.toque = True             # toque corto: queda abierto para elegir con click
                self.actividad = time.time()
                return
            self.ejecutar()

        def ejecutar(self):
            el = self.elegido()
            if el is None:
                self.cerrar()
                return
            _log(f"elegido {self.nombre_app}: {el['nombre']} -> {el['accion']!r}")
            raton.pulso(ONDA_EJECUTAR, 0)
            self.flash[self.sel] = 1.0
            cola.put(el["accion"])
            self.cerrar()

        # -- eventos --
        def al_mover(self, _c, x, y):
            self.actividad = time.time()
            if self.cerrando:
                return
            sel, sub = seleccion(x - self.ax, y - self.ay, self.sectores, self.sub_abierto)
            if (sel, sub) != (self.sel, self.sub):
                if sub is not None:
                    raton.pulso(ONDA_SUB)
                elif sel is not None:
                    raton.pulso(ONDA_CAMBIO)
                self.sel, self.sub = sel, sub
                if sel is not None and sub is None:
                    self.sub_abierto = sel if self.sectores[sel]["sub"] else None
                elif sel is None:
                    self.sub_abierto = None

        def al_clic(self, g, _n, _x, _y):
            if g.get_current_button() == 1 and self.sel is not None:
                self.ejecutar()
            else:
                self.cerrar()

        def al_rodar(self, _c, _dx, dy):
            self.actividad = time.time()
            if dy == 0:
                return True
            if self.sel is None:
                rueda = apps.VOLUMEN
            else:
                rueda = self.sectores[self.sel].get("rueda") if self.sub is None else None
            if rueda:
                cola.put(rueda[0] if dy < 0 else rueda[1])
                raton.pulso(ONDA_CAMBIO, 0.02)
                if self.sel is not None:
                    self.flash[self.sel] = 0.6
            return True

        # -- animación --
        def tick(self, widget, clock):
            t = clock.get_frame_time() / 1e6
            dt = 0.016 if self._t is None else min(0.05, t - self._t)
            self._t = t
            k = min(1.0, dt * 18)
            self.t_abre = min(1.0, self.t_abre + dt / 0.24) if self.t_abre < 1 else 1.0
            if self.cerrando:
                self.t_cierre = min(1.0, self.t_cierre + dt / 0.13)
                if self.t_cierre >= 1.0:
                    self._ocultar()
                    return GLib.SOURCE_REMOVE
            elif time.time() - self.actividad > AUTOCIERRE_S:
                self.cerrar()
            for i in range(N):
                obj = (1.0 if self.sub is None else 0.55) if self.sel == i else 0.0
                self.hv[i] += (obj - self.hv[i]) * k
                self.flash[i] *= max(0.0, 1 - dt * 7)
            for j in range(len(self.hv_sub)):
                obj = 1.0 if self.sub == j else 0.0
                self.hv_sub[j] += (obj - self.hv_sub[j]) * k
            self.foco += ((1.0 if self.sel is not None else 0.0) - self.foco) * k
            # sub-opciones: entra la nueva cuando la anterior ya salió
            if self.sub_abierto != self.sub_vis:
                self.t_sub = max(0.0, self.t_sub - dt / 0.08)
                if self.t_sub <= 0:
                    self.sub_vis = self.sub_abierto
                    self.hv_sub = [0.0] * 8
            elif self.sub_vis is not None:
                self.t_sub = min(1.0, self.t_sub + dt / 0.2)
            r_obj = (R2 + RS + 40) if self.sub_vis is not None else (R1 + RB + 40)
            self.r_velo += (r_obj - self.r_velo) * k
            # haz de luz
            if self.sel is not None:
                ang_obj = (angulos_sub(self.sel, len(self.sectores[self.sel]["sub"]))[self.sub]
                           if self.sub is not None else self.sel * PASO)
                if self.haz < 0.02:
                    self.ang_haz = ang_obj
                self.ang_haz = (self.ang_haz + dif_ang(ang_obj, self.ang_haz) * min(1.0, dt * 22)) % 360
                obj_col = color_sector(self.tono, self.sel, 0.4)
                self.col_haz = tuple(c + (o - c) * k for c, o in zip(self.col_haz, obj_col))
            self.haz += ((1.0 if self.sel is not None else 0.0) - self.haz) * k
            widget.queue_draw()
            return GLib.SOURCE_CONTINUE

    anillo = Anillo()

    class SinMouse:
        def pulso(self, *a, **k):
            pass

    global raton
    if prueba:
        raton = SinMouse()

        def abrir_prueba():
            anillo.abrir()
            s = os.environ.get("ANILLO_SEL")
            if s:
                i, _, j = s.partition(".")
                anillo.sel = int(i)
                anillo.sub_abierto = int(i) if anillo.sectores[int(i)]["sub"] else None
                anillo.sub = int(j) if j else None
            GLib.timeout_add(int(float(os.environ.get("ANILLO_SEG", "6")) * 1000), lambda: sys.exit(0))
            return False
        GLib.timeout_add(300, abrir_prueba)
    else:
        raton = Mouse(GLib, lambda: anillo.abrir(), lambda: anillo.soltar())
        try:
            os.unlink(SOCK)
        except OSError:
            pass
        srv = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        srv.bind(SOCK)
        srv.setblocking(False)

        def recibir(_fd, _cond):
            try:
                while True:
                    cmd = srv.recv(64).decode().strip()
                    {"abrir": anillo.abrir, "soltar": anillo.soltar, "cancelar": anillo.cerrar}.get(cmd, lambda: 0)()
            except BlockingIOError:
                pass
            return True
        GLib.io_add_watch(srv.fileno(), GLib.IO_IN, recibir)
        _log("servicio listo")

    GObject  # noqa: B018  (import usado por el subclassing de Gtk.Widget)
    try:
        GLib.MainLoop().run()
    except KeyboardInterrupt:
        pass


raton = None

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--demonio":
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        demonio()
    else:
        print(__doc__)
