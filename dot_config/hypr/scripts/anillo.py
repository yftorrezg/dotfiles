#!/usr/bin/env python3
"""anillo.py — anillo radial del MX Master 4 (como el "Actions Ring" de Logi Options+, pero por programa).

TOCA el panel háptico → aparece un anillo de 12 acciones del programa con foco y se queda abierto →
mueve el mouse hacia una (el mouse vibra al cambiar) → CLICK (o vuelve a tocar el panel) y se ejecuta.
  · Las burbujas con un puntito tienen sub-opciones: aleja más el mouse en esa dirección y salen en un arco.
  · Click en el centro, click derecho o 10 s sin moverte = cerrar.
  · Rápido para expertos: MANTÉN el panel, apunta y suelta (si lo mantuviste más de 0,35 s, soltar ejecuta).
  · Rueda sobre una burbuja = su ajuste (volumen, zoom, pestañas…) · rueda en el centro = volumen.

Qué hay en cada programa: anillo_apps.py. Iconos: fuente Tabler de Noctalia (se carga sola).

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

FUENTE_ICONOS = "/usr/share/noctalia/assets/fonts/noctalia-tabler.ttf"
MAPA_ICONOS = "/usr/share/noctalia/assets/fonts/tabler.json"
FAMILIA_ICONOS = "noctalia-tabler-icons"

# ---- Geometría (px lógicos) ------------------------------------------------------------------------
N = 12
PASO = 360 / N
R1 = 168            # centro → burbujas
RB = 34             # radio de burbuja
R2 = 258            # centro → sub-opciones
RS = 26             # radio de sub-opción
ANCHO_TXT = 108     # ancho máximo del texto junto a cada burbuja
SUB_PASO = 25       # grados entre sub-opciones
HUB = 58            # disco central
ZONA_MUERTA = 36    # dentro = nada elegido
UMBRAL_SUB = (R1 + R2) / 2 + 6
LADO = int(2 * max(R2 + RS * 1.35 + 34, R1 + RB + 10 + ANCHO_TXT + 12))
REBOTE_S = 0.14     # el sensor de fuerza del panel rebota: un soltar solo vale si no vuelve a pulsar en este tiempo
MANTENER_S = 0.35   # mantenido más que esto + algo elegido → soltar ejecuta; si no, queda abierto
AUTOCIERRE_S = 10
ONDA_CAMBIO, ONDA_SUB, ONDA_EJECUTAR = 4, 0x1B, 7   # formas de onda HID++ del motor háptico
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


def hex_rgb(c):
    c = c.lstrip("#")
    return int(c[0:2], 16) / 255, int(c[2:4], 16) / 255, int(c[4:6], 16) / 255


def mezclar(a, b, t):
    return tuple(x + (y - x) * t for x, y in zip(a, b))


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


def cargar_iconos():
    """{nombre: carácter} de la fuente Tabler y la registra en fontconfig solo para este proceso."""
    import ctypes
    import json
    try:
        fc = ctypes.CDLL("libfontconfig.so.1")
        fc.FcConfigAppFontAddFile.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        fc.FcConfigAppFontAddFile(None, FUENTE_ICONOS.encode())
        with open(MAPA_ICONOS) as f:
            return {k: chr(int(v["codepoint"][2:], 16)) for k, v in json.load(f).items()}
    except Exception as e:
        _log(f"iconos: {e}")
        return {}


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
        self.timer_soltar = None
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
        self.pulsado = False
        if self.timer_soltar:
            self.GLib.source_remove(self.timer_soltar)
            self.timer_soltar = None

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
            if CID_HAPTICO in cids:
                if self.timer_soltar:                    # volvió a pulsar enseguida: era rebote, ignorar
                    self.GLib.source_remove(self.timer_soltar)
                    self.timer_soltar = None
                elif not self.pulsado:
                    self.pulsado = True
                    self.al_pulsar()
            elif self.pulsado and not self.timer_soltar:
                self.timer_soltar = self.GLib.timeout_add(int(REBOTE_S * 1000), self._soltar_real)
        elif d[2] == self.f_wds:                        # se reconectó: volver a desviar el botón
            self.GLib.timeout_add(400, lambda: (self._desviar(), False)[1])

    def _soltar_real(self):
        self.timer_soltar = None
        self.pulsado = False
        self.al_soltar()
        return False

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

    iconos = cargar_iconos()           # antes de que Pango cree su mapa de fuentes

    import gi
    gi.require_version("Gtk", "4.0")
    gi.require_version("Gdk", "4.0")
    gi.require_version("Gsk", "4.0")
    gi.require_version("Graphene", "1.0")
    gi.require_version("Gtk4LayerShell", "1.0")
    from gi.repository import Gdk, GLib, Graphene, Gsk, Gtk, Pango
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
    # Ojo: Graphene.Rect().init(...) encadenado devuelve una copia que PyGObject puede liberar → basura.
    def rgba(r, g, b, a=1.0):
        c = Gdk.RGBA()
        c.red, c.green, c.blue, c.alpha = r, g, b, max(0.0, min(1.0, a))
        return c

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

    def sombra(col, radio):
        s = Gsk.Shadow()
        s.color, s.dx, s.dy, s.radius = col, 0, 0, radio
        return s

    OSCURO = (0.07, 0.07, 0.10)

    class Lienzo(Gtk.Widget):
        __gtype_name__ = "AnilloLienzo"

        def __init__(self, anillo):
            super().__init__()
            self.a = anillo
            self.cache = {}

        def _layout(self, txt, desc, ancho=None, absoluto=None):
            clave = (txt, desc, ancho, absoluto)
            lay = self.cache.get(clave)
            if lay is None:
                lay = self.create_pango_layout(txt)
                fd = Pango.FontDescription.from_string(desc)
                if absoluto:
                    fd.set_absolute_size(absoluto * Pango.SCALE)
                lay.set_font_description(fd)
                if ancho:
                    lay.set_width(int(ancho * Pango.SCALE))
                    lay.set_alignment(Pango.Alignment.CENTER)
                    lay.set_wrap(Pango.WrapMode.WORD_CHAR)
                    lay.set_ellipsize(Pango.EllipsizeMode.END)
                    lay.set_height(-2)
                if len(self.cache) > 600:
                    self.cache.clear()
                self.cache[clave] = lay
            return lay

        def texto(self, snap, txt, desc, cx, cy, ancho, color):
            lay = self._layout(txt, desc, ancho)
            _, alto = lay.get_pixel_size()
            snap.save()
            snap.translate(punto(cx - ancho / 2, cy - alto / 2))
            snap.append_layout(lay, color)
            snap.restore()

        def glifo(self, snap, nombre, x, y, tam, color, brillo=None, radio=0.0):
            ch = iconos.get(nombre)
            if not ch:
                return
            tam = max(6, int(round(tam)))
            lay = self._layout(ch, FAMILIA_ICONOS, None, tam)
            tinta, _ = lay.get_pixel_extents()
            snap.save()
            snap.translate(punto(x - tinta.x - tinta.width / 2, y - tinta.y - tinta.height / 2))
            if brillo is not None and radio > 0.5:
                snap.push_shadow([sombra(brillo, radio)])
                snap.append_layout(lay, color)
                snap.pop()
            else:
                snap.append_layout(lay, color)
            snap.restore()

        def etiqueta(self, snap, txt, x, y, r, ang, col, hv, alfa):
            """Nombre de la acción pegado a la burbuja, hacia fuera del anillo."""
            if alfa < 0.03:
                return
            lay = self._layout(txt, "Sans Bold 9.5", ANCHO_TXT)
            lay.set_alignment(Pango.Alignment.LEFT if math.sin(math.radians(ang)) > 0.3
                              else Pango.Alignment.RIGHT if math.sin(math.radians(ang)) < -0.3
                              else Pango.Alignment.CENTER)
            tw, th = lay.get_pixel_size()
            sa, ca = math.sin(math.radians(ang)), -math.cos(math.radians(ang))
            if abs(sa) > 0.3:
                tx = x + r + 9 if sa > 0 else x - r - 9 - ANCHO_TXT
                ty = y - th / 2
            else:
                tx = x - ANCHO_TXT / 2
                ty = y - r - 7 - th if ca < 0 else y + r + 7
            snap.save()
            snap.translate(punto(tx, ty))
            snap.push_opacity(alfa)
            snap.push_shadow([sombra(rgba(0, 0, 0, 0.95), 3), sombra(rgba(0, 0, 0, 0.7), 7)])
            snap.append_layout(lay, rgba(*mezclar((0.86, 0.88, 0.93), col, 0.55 * hv + 0.15), 1))
            snap.pop()
            snap.pop()
            snap.restore()

        def burbuja(self, snap, x, y, r, col, hv, alfa, icono, tam_icono, con_sub, ang, osc=1.0):
            """Estilo neón: vidrio oscuro + aro de color brillante; elegida = se enciende entera."""
            c = circ(x, y, r)
            vivo = mezclar(col, (1, 1, 1), 0.25 * hv)
            snap.push_opacity(alfa)
            snap.append_outset_shadow(c, rgba(0, 0, 0, 0.55), 0, 5, 0, 14)
            snap.append_outset_shadow(c, rgba(*col, (0.30 + 0.55 * hv) * osc), 0, 0, 1 + 3 * hv, 9 + 20 * hv)
            snap.push_rounded_clip(c)
            arriba = mezclar(mezclar(OSCURO, col, 0.16), col, 0.80 * hv)
            abajo = mezclar(mezclar((0.03, 0.03, 0.05), col, 0.06), tuple(v * 0.7 for v in col), 0.80 * hv)
            snap.append_linear_gradient(rect(x - r, y - r, 2 * r, 2 * r), punto(x, y - r), punto(x, y + r),
                                        paradas((0, rgba(*arriba, 0.97)), (1, rgba(*abajo, 0.97))))
            snap.append_radial_gradient(rect(x - r, y - r, 2 * r, 2 * r), punto(x, y - r * 0.55),
                                        r * 0.95, r * 0.55, 0, 1,
                                        paradas((0, rgba(1, 1, 1, 0.10 + 0.12 * hv)), (1, rgba(1, 1, 1, 0))))
            snap.pop()
            ancho = 2.0 + 1.0 * hv
            snap.append_border(c, [ancho] * 4, [rgba(*vivo, (0.55 + 0.45 * hv) * (0.5 + 0.5 * osc))] * 4)
            color_ic = mezclar(mezclar(col, (1, 1, 1), 0.15), (1, 1, 1), hv)
            self.glifo(snap, icono, x, y, tam_icono, rgba(*color_ic, 0.55 + 0.45 * osc),
                       rgba(*col, 0.9), 5 + 4 * (1 - hv))
            if con_sub:  # puntito = tiene sub-opciones (como en Logi Options+)
                a = math.radians(ang)
                px, py = x + (r + 7) * math.sin(a), y - (r + 7) * math.cos(a)
                pc = circ(px, py, 3.4)
                snap.append_outset_shadow(pc, rgba(*col, 0.9), 0, 0, 0, 6)
                snap.push_rounded_clip(pc)
                snap.append_color(rgba(*vivo, 1), rect(px - 4, py - 4, 8, 8))
                snap.pop()
            snap.pop()

        def do_snapshot(self, snap):
            a = self.a
            if not a.visible:
                return
            cx, cy = LADO / 2, LADO / 2
            t_ab = a.t_abre
            fade = ease_out(t_ab * 1.6) * (1 - ease_out(a.t_cierre))
            escala = 0.90 + 0.10 * ease_out_back(t_ab, 1.2) - 0.07 * a.t_cierre
            snap.save()
            snap.translate(punto(cx, cy))
            snap.scale(escala, escala)
            snap.translate(punto(-cx, -cy))
            snap.push_opacity(max(0.0, fade))
            ac = a.acento

            # velo circular (con desenfoque del compositor detrás) que crece con las sub-opciones
            rv = a.r_velo
            snap.append_radial_gradient(rect(cx - rv, cy - rv, 2 * rv, 2 * rv), punto(cx, cy), rv, rv, 0, 1,
                                        paradas((0, rgba(0.03, 0.03, 0.06, 0.94)),
                                                (0.82, rgba(0.03, 0.03, 0.06, 0.88)),
                                                (1, rgba(0.03, 0.03, 0.06, 0))))
            # haz de luz desde el centro hacia la selección
            if a.haz > 0.01:
                rb = R2 + RS + 14 if a.sub_vis is not None and a.t_sub > 0.2 else R1 + RB + 18
                snap.push_rounded_clip(circ(cx, cy, rb))
                hc = a.col_haz
                snap.append_conic_gradient(rect(cx - rb, cy - rb, 2 * rb, 2 * rb), punto(cx, cy), a.ang_haz - 20,
                                           paradas((0, rgba(*hc, 0)), (20 / 360, rgba(*hc, 0.38 * a.haz)),
                                                   (40 / 360, rgba(*hc, 0)), (1, rgba(*hc, 0))))
                snap.pop()
            # pistas finas
            snap.append_border(circ(cx, cy, R1), [1.0] * 4, [rgba(*ac, 0.10)] * 4)

            secs = a.sectores
            for i in sorted(range(N), key=lambda i: a.hv[i]):
                ti = ease_out_back((t_ab * 0.24 - i * 0.011) / 0.17)
                if ti <= 0:
                    continue
                ang = i * PASO
                rad = math.radians(ang)
                d = R1 * (0.55 + 0.45 * ti)
                x, y = cx + d * math.sin(rad), cy - d * math.cos(rad)
                hv = a.hv[i]
                osc = 1.0 - 0.45 * a.foco * (1 - hv)
                r = RB * (0.35 + 0.65 * ti) * (1 + 0.22 * hv + 0.14 * a.flash[i])
                self.burbuja(snap, x, y, r, a.colores[i], hv, min(1.0, ti * 1.5), secs[i]["icono"],
                             29 * (1 + 0.12 * hv), bool(secs[i]["sub"]), ang, osc)
                # los nombres se apartan cuando salen sub-opciones (para no taparlas)
                vis = ease_out(t_ab * 1.4 - 0.3) * (1 - 0.92 * max(a.t_sub, 0.0) * (0 if i == a.sub_vis else 1)) \
                    * (1 - 0.6 * a.t_sub * (1 if i == a.sub_vis else 0)) * (1 - ease_out(a.t_cierre))
                self.etiqueta(snap, secs[i]["nombre"], x, y, r, ang, a.colores[i], hv, vis)

            # sub-opciones en arco exterior
            p = a.sub_vis
            if p is not None and a.t_sub > 0.01:
                subs = secs[p]["sub"]
                pr = math.radians(p * PASO)
                for k, ang in enumerate(angulos_sub(p, len(subs))):
                    tk = ease_out_back((a.t_sub * 0.2 - k * 0.018) / 0.14)
                    if tk <= 0:
                        continue
                    rad = math.radians(ang)
                    x = cx + R1 * math.sin(pr) * (1 - tk) + R2 * math.sin(rad) * tk
                    y = cy - R1 * math.cos(pr) * (1 - tk) - R2 * math.cos(rad) * tk
                    hv = a.hv_sub[k] if k < len(a.hv_sub) else 0
                    r = RS * (0.4 + 0.6 * tk) * (1 + 0.26 * hv)
                    self.burbuja(snap, x, y, r, hex_rgb(subs[k]["color"]), hv, min(1.0, tk * 1.4),
                                 subs[k]["icono"], 22 * (1 + 0.12 * hv), False, ang)
                    if hv > 0.5:   # nombre de la sub-opción elegida, junto a ella
                        self.etiqueta(snap, subs[k]["nombre"], x, y, r, ang, hex_rgb(subs[k]["color"]), hv, hv)

            # centro: logo de la app (o la acción elegida) con brillo
            hcirc = circ(cx, cy, HUB * (0.7 + 0.3 * ease_out(t_ab * 1.3)))
            snap.append_outset_shadow(hcirc, rgba(0, 0, 0, 0.6), 0, 6, 0, 28)
            snap.append_outset_shadow(hcirc, rgba(*ac, 0.35), 0, 0, 0, 18)
            snap.push_rounded_clip(hcirc)
            snap.append_linear_gradient(rect(cx - HUB, cy - HUB, 2 * HUB, 2 * HUB), punto(cx, cy - HUB),
                                        punto(cx, cy + HUB),
                                        paradas((0, rgba(*mezclar((0.13, 0.13, 0.18), ac, 0.10), 0.98)),
                                                (1, rgba(0.05, 0.05, 0.08, 0.98))))
            snap.pop()
            snap.append_border(hcirc, [1.8] * 4, [rgba(*ac, 0.75)] * 4)
            el = a.elegido()
            if el:
                col = hex_rgb(el["color"])
                self.glifo(snap, el["icono"], cx, cy - 15, 32, rgba(*mezclar(col, (1, 1, 1), 0.2)),
                           rgba(*col, 0.9), 8)
                self.texto(snap, el["nombre"], "Sans Bold 9", cx, cy + 18, HUB * 1.62, rgba(1, 1, 1, 0.95))
            else:
                self.glifo(snap, a.logo, cx, cy - 12, 34, rgba(*mezclar(ac, (1, 1, 1), 0.15)), rgba(*ac, 0.95), 10)
                pista = "clic = elegir" if a.toque else a.nombre_app
                self.texto(snap, pista, "Sans Bold 8.5", cx, cy + 22, HUB * 1.7, rgba(*mezclar(ac, (1, 1, 1), 0.4)))
            # indicador que orbita el centro
            if a.haz > 0.01:
                ra = math.radians(a.ang_haz)
                ix, iy = cx + (HUB + 8) * math.sin(ra), cy - (HUB + 8) * math.cos(ra)
                ic = circ(ix, iy, 3.4)
                snap.append_outset_shadow(ic, rgba(*a.col_haz, a.haz), 0, 0, 0, 7)
                snap.push_rounded_clip(ic)
                snap.append_color(rgba(*mezclar(a.col_haz, (1, 1, 1), 0.4), a.haz), rect(ix - 4, iy - 4, 8, 8))
                snap.pop()
            snap.pop()
            snap.restore()

    class Anillo:
        def __init__(self):
            self.visible = False
            self.cerrando = False
            self.tick_id = None
            self.monitor = None
            self._cargar(apps.GLOBAL)
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

        def _cargar(self, perfil):
            self.sectores = perfil["sectores"]
            self.nombre_app = perfil["nombre"]
            self.logo = perfil["logo"]
            self.acento = hex_rgb(perfil["acento"])
            self.colores = [hex_rgb(s["color"]) for s in self.sectores]

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
            self.r_velo = R1 + RB + 50
            self.toque = False
            self.ignorar_soltar = False
            self.ax = self.ay = LADO / 2
            self.t0 = self.actividad = time.time()

        def elegido(self):
            if self.sel is None:
                return None
            s = self.sectores[self.sel]
            return s["sub"][self.sub] if self.sub is not None else s

        # -- abrir / cerrar --
        def pulsar(self):
            """Botón háptico (o SUPER+ALT+O) pulsado."""
            if self.visible and not self.cerrando:
                # ya estaba abierto (modo toque): este toque confirma lo elegido, o cierra
                self.ignorar_soltar = True
                if self.elegido():
                    self.ejecutar()
                else:
                    self.cerrar()
                return
            self.abrir()

        def abrir(self):
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
            mon, mw, mh = None, 0, 0
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
            self._cargar(perfil)
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
            """Botón soltado: si lo mantuvo y apuntó a algo, ejecuta; si fue un toque, queda abierto."""
            if self.ignorar_soltar:
                self.ignorar_soltar = False
                return
            if not self.visible or self.cerrando or self.toque:
                return
            if time.time() - self.t0 >= MANTENER_S and self.elegido():
                self.ejecutar()
            else:
                self.toque = True
                self.actividad = time.time()

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
            if prueba and os.environ.get("ANILLO_DEPURAR"):
                print(f"mover x={x:.0f} y={y:.0f} ancla={self.ax:.0f},{self.ay:.0f}", flush=True)
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
            if g.get_current_button() == 1 and self.elegido():
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
            self.t_abre = min(1.0, self.t_abre + dt / 0.24)
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
                self.hv_sub[j] += ((1.0 if self.sub == j else 0.0) - self.hv_sub[j]) * k
            self.foco += ((1.0 if self.sel is not None else 0.0) - self.foco) * k
            # sub-opciones: entra la nueva cuando la anterior ya salió
            if self.sub_abierto != self.sub_vis:
                self.t_sub = max(0.0, self.t_sub - dt / 0.08)
                if self.t_sub <= 0:
                    self.sub_vis = self.sub_abierto
                    self.hv_sub = [0.0] * 8
            elif self.sub_vis is not None:
                self.t_sub = min(1.0, self.t_sub + dt / 0.2)
            r_obj = (R2 + RS + 50) if self.sub_vis is not None else (R1 + RB + 50)
            self.r_velo += (r_obj - self.r_velo) * k
            # haz de luz
            el = self.elegido()
            if el is not None:
                ang_obj = (angulos_sub(self.sel, len(self.sectores[self.sel]["sub"]))[self.sub]
                           if self.sub is not None else self.sel * PASO)
                if self.haz < 0.02:
                    self.ang_haz = ang_obj
                self.ang_haz = (self.ang_haz + dif_ang(ang_obj, self.ang_haz) * min(1.0, dt * 22)) % 360
                self.col_haz = mezclar(self.col_haz, hex_rgb(el["color"]), k)
            self.haz += ((1.0 if el is not None else 0.0) - self.haz) * k
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
        raton = Mouse(GLib, lambda: anillo.pulsar(), lambda: anillo.soltar())
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
                    {"abrir": anillo.pulsar, "soltar": anillo.soltar, "cancelar": anillo.cerrar}.get(cmd, lambda: 0)()
            except BlockingIOError:
                pass
            return True
        GLib.io_add_watch(srv.fileno(), GLib.IO_IN, recibir)
        _log("servicio listo")

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
