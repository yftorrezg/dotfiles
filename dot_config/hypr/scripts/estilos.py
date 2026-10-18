#!/usr/bin/env python3
"""estilos.py — selector de estilo de personalización (SUPER+SHIFT+A).

Muestra 6 tarjetas con vista previa animada del escritorio actual:
  Noche/Día × Clásico (fondos fijos) / Animado (videos) / Aurora (degradados vivos)
y un interruptor para los destellos del cursor.
Teclas: flechas o 1-6 para elegir, Enter aplica, D destellos, Esc cierra. También con clic.

Al aplicar escribe ~/.local/state/escritorios-vivos/estilo.json y pone el modo de noctalia;
escritorios-vivos.py ve el cambio y pone los fondos.
Las vistas previas (clips cortos de 480 px) se guardan en ~/.cache/escritorios-vivos/.
`estilos.py --preparar` solo genera esas vistas (lo lanza escritorios-vivos al iniciar).
"""
import ctypes

ctypes.CDLL("libgtk4-layer-shell.so")

import hashlib  # noqa: E402
import json  # noqa: E402
import os  # noqa: E402
import socket  # noqa: E402
import subprocess  # noqa: E402
import sys  # noqa: E402
import threading  # noqa: E402
import tomllib  # noqa: E402
from pathlib import Path  # noqa: E402

import gi  # noqa: E402

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
gi.require_version("Gtk4LayerShell", "1.0")
from gi.repository import Gdk, Gio, GLib, Gtk  # noqa: E402
from gi.repository import Gtk4LayerShell as LS  # noqa: E402

CONFIG = Path.home() / ".config/hypr/escritorios-temas.toml"
ESTADO = Path.home() / ".local/state/escritorios-vivos"
ESTILO = ESTADO / "estilo.json"
CACHE = Path.home() / ".cache/escritorios-vivos"
NOCT_SETTINGS = Path.home() / ".local/state/noctalia/settings.toml"
HYPR = Path(os.environ["XDG_RUNTIME_DIR"]) / "hypr" / os.environ["HYPRLAND_INSTANCE_SIGNATURE"] / ".socket.sock"

ESTILOS = [  # (fondo, modo, título, icono, descripción) — en pares noche/día
    ("estatico", "dark", "Noche clásica", "🌙", "Fondos fijos oscuros"),
    ("estatico", "light", "Día clásico", "☀️", "Fondos fijos claros"),
    ("video", "dark", "Noche animada", "🎞️", "Escenas en movimiento"),
    ("video", "light", "Día animado", "🌸", "Escenas en movimiento"),
    ("aurora", "dark", "Aurora nocturna", "🌌", "Degradados vivos"),
    ("aurora", "light", "Aurora de día", "🌈", "Degradados pastel"),
]
# Para probar sin robar el teclado ni tapar tu monitor: ESTILOS_PRUEBA=DP-3 estilos.py
PRUEBA = os.environ.get("ESTILOS_PRUEBA")

CSS = """
window.estilos { background: transparent; }
.velo { background-color: @velo; transition: opacity 250ms ease; }
.velo.oculto { opacity: 0; }
.panel {
  padding: 34px 38px 26px 38px; border-radius: 36px;
  background-color: @panel; border: 1px solid @borde; color: @texto;
  box-shadow: 0 30px 80px rgba(0,0,0,0.45);
  font-family: "Adwaita Sans", "Inter", "Cantarell", sans-serif;
  transition: opacity 280ms cubic-bezier(.2,.8,.2,1), transform 380ms cubic-bezier(.2,1.25,.3,1);
}
.oculto .panel { opacity: 0; transform: translateY(30px) scale(0.94); }
.titulo { font-size: 34px; font-weight: 800; letter-spacing: -0.5px; }
.subtitulo { font-size: 15px; opacity: 0.65; }
.tarjeta {
  padding: 10px 10px 14px 10px; border-radius: 26px;
  background-color: @tarjeta; border: 2px solid transparent;
  transition: all 260ms cubic-bezier(.2,1.2,.3,1);
}
.tarjeta.sel { border-color: @acento; background-color: @tarjeta_sel;
               box-shadow: 0 12px 34px alpha(@acento, 0.35); transform: scale(1.04); }
.vista { border-radius: 18px; background-color: #000; }
.icono { font-family: "Noto Color Emoji"; font-size: 22px; }
.nombre { font-size: 18px; font-weight: 750; }
.desc { font-size: 13px; opacity: 0.65; }
.num { font-size: 12px; font-weight: 800; padding: 3px 9px; border-radius: 99px;
       background-color: rgba(0,0,0,0.55); color: #fff; margin: 10px; }
.actual { font-size: 12px; font-weight: 800; padding: 3px 10px; border-radius: 99px;
          background-color: @acento; color: #111; margin: 10px; }
.pie { font-size: 13px; opacity: 0.7; }
.destellos-lbl { font-size: 16px; font-weight: 650; }
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


def leer_estilo():
    try:
        return json.loads(ESTILO.read_text())
    except (OSError, ValueError):
        return {"fondo": "estatico", "destellos": False}


def escritorio_actual(n):
    try:
        wid = hypr_json("activeworkspace")["id"]
        return (wid - 1) % n + 1 if 1 <= wid <= 2 * n else 1
    except (OSError, ValueError, KeyError):
        return 1


def fuentes(cfg, idx):
    """Ruta original (imagen o video) de cada estilo para el escritorio idx."""
    carpeta = Path(os.path.expanduser(cfg.get("general", {}).get("carpeta", "~")))
    lista = cfg.get("escritorio", [])
    e = lista[idx - 1] if idx <= len(lista) else {}
    salida = []
    for fondo, modo, *_ in ESTILOS:
        suf = "claro" if modo == "light" else "oscuro"
        if fondo == "estatico":
            rel = e.get(f"fondo_{suf}")
        elif fondo == "video":
            rel = e.get(f"video_{suf}")
        else:
            rel = f"Animados/Aurora/{idx}-{suf}-h.mp4"
        ruta = carpeta / rel if rel else None
        salida.append(ruta if ruta and ruta.exists() else None)
    return salida


def vista_previa(origen):
    """Clip corto (o imagen) de 480 px en caché; lo crea con ffmpeg si falta."""
    if origen is None:
        return None
    st = origen.stat()
    clave = hashlib.sha1(f"{origen}{st.st_mtime}".encode()).hexdigest()[:16]
    es_video = origen.suffix.lower() in (".mp4", ".webm", ".mkv")
    destino = CACHE / f"{clave}.{'mp4' if es_video else 'jpg'}"
    if not destino.exists():
        CACHE.mkdir(parents=True, exist_ok=True)
        tmp = destino.with_suffix(".tmp" + destino.suffix)
        if es_video:
            cmd = ["ffmpeg", "-v", "error", "-y", "-i", str(origen), "-t", "6", "-an",
                   "-vf", "scale=480:270:force_original_aspect_ratio=increase,crop=480:270,fps=30",
                   "-c:v", "libx264", "-preset", "veryfast", "-crf", "26", "-pix_fmt", "yuv420p", str(tmp)]
        else:
            cmd = ["ffmpeg", "-v", "error", "-y", "-i", str(origen),
                   "-vf", "scale=480:270:force_original_aspect_ratio=increase,crop=480:270", str(tmp)]
        if subprocess.run(cmd).returncode != 0:
            return None
        tmp.rename(destino)
    return destino


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
        try:
            monitores = hypr_json("monitors")
            foco = PRUEBA or next(m["name"] for m in monitores if m["focused"])
            info = next(m for m in monitores if m["name"] == foco)
            # Monitor vertical: 2 columnas (filas = tipo); horizontal: 3 columnas (filas = noche/día)
            self.vertical = info.get("transform", 0) % 2 == 1
            mon = next((m for m in Gdk.Display.get_default().get_monitors() if m.get_connector() == foco), None)
            if mon:
                LS.set_monitor(self, mon)
        except (OSError, ValueError, StopIteration):
            self.vertical = False

        self.cfg = cfg
        self.estilo = leer_estilo()
        self.modo = leer_modo()
        n = int(cfg.get("general", {}).get("por_monitor", 5))
        self.idx = escritorio_actual(n)
        lista = cfg.get("escritorio", [])
        acento = (lista[self.idx - 1] if self.idx <= len(lista) else {}).get("color", "#c9a7ff")
        claro = self.modo == "light"
        css = Gtk.CssProvider()
        css.load_from_string(
            f"@define-color acento {acento};"
            + ("@define-color velo rgba(235,235,245,0.55); @define-color panel rgba(252,252,255,0.94);"
               "@define-color borde rgba(255,255,255,1); @define-color texto #1b1a22;"
               "@define-color tarjeta rgba(0,0,0,0.04); @define-color tarjeta_sel rgba(0,0,0,0.07);"
               if claro else
               "@define-color velo rgba(5,5,12,0.6); @define-color panel rgba(20,20,28,0.94);"
               "@define-color borde rgba(255,255,255,0.08); @define-color texto #f4f2fa;"
               "@define-color tarjeta rgba(255,255,255,0.04); @define-color tarjeta_sel rgba(255,255,255,0.09);")
            + CSS)
        Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), css, 800)

        self.velo = Gtk.Box(halign=Gtk.Align.FILL, valign=Gtk.Align.FILL, hexpand=True, vexpand=True)
        self.velo.add_css_class("velo")
        self.velo.add_css_class("oculto")
        clic_fuera = Gtk.GestureClick()
        clic_fuera.connect("released", self.clic_en_velo)
        self.velo.add_controller(clic_fuera)

        self.panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=22,
                             halign=Gtk.Align.CENTER, valign=Gtk.Align.CENTER, hexpand=True)
        self.panel.add_css_class("panel")
        self.velo.append(self.panel)

        cab = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        t = Gtk.Label(label="Elige tu estilo", xalign=0)
        t.add_css_class("titulo")
        st = Gtk.Label(label=f"Vista previa del escritorio {self.idx} · se aplica a todos tus escritorios", xalign=0)
        st.add_css_class("subtitulo")
        cab.append(t)
        cab.append(st)
        self.panel.append(cab)

        grid = Gtk.Grid(column_spacing=18, row_spacing=18)
        self.panel.append(grid)
        self.tarjetas = []
        actual = next((i for i, (f, m, *_) in enumerate(ESTILOS)
                       if f == self.estilo.get("fondo", "estatico") and m == self.modo), 0)
        self.sel = actual
        for i, (fondo, modo, nombre, icono, desc) in enumerate(ESTILOS):
            tarjeta = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            tarjeta.add_css_class("tarjeta")
            capas = Gtk.Overlay()
            pic = Gtk.Picture(content_fit=Gtk.ContentFit.COVER, can_shrink=True)
            pic.set_size_request(*((280, 158) if self.vertical else (300, 169)))
            pic.add_css_class("vista")
            pic.set_overflow(Gtk.Overflow.HIDDEN)
            capas.set_child(pic)
            num = Gtk.Label(label=str(i + 1), halign=Gtk.Align.START, valign=Gtk.Align.START)
            num.add_css_class("num")
            capas.add_overlay(num)
            if i == actual:
                act = Gtk.Label(label="ACTUAL", halign=Gtk.Align.END, valign=Gtk.Align.START)
                act.add_css_class("actual")
                capas.add_overlay(act)
            tarjeta.append(capas)
            fila = Gtk.Box(spacing=10)
            ic = Gtk.Label(label=icono)
            ic.add_css_class("icono")
            txt = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            nl = Gtk.Label(label=nombre, xalign=0)
            nl.add_css_class("nombre")
            dl = Gtk.Label(label=desc, xalign=0)
            dl.add_css_class("desc")
            txt.append(nl)
            txt.append(dl)
            fila.append(ic)
            fila.append(txt)
            tarjeta.append(fila)
            mov = Gtk.EventControllerMotion()
            mov.connect("enter", lambda *_, i=i: self.seleccionar(i))
            tarjeta.add_controller(mov)
            clic = Gtk.GestureClick()
            clic.connect("released", lambda *_, i=i: self.aplicar(i))
            tarjeta.add_controller(clic)
            grid.attach(tarjeta, *self.posicion(i), 1, 1)
            self.tarjetas.append((tarjeta, pic))

        pie = Gtk.Box(spacing=14)
        chispa = Gtk.Label(label="✨")
        chispa.add_css_class("icono")
        lbl = Gtk.Label(label="Destellos del cursor", xalign=0)
        lbl.add_css_class("destellos-lbl")
        self.interruptor = Gtk.Switch(active=bool(self.estilo.get("destellos")), valign=Gtk.Align.CENTER)
        self.interruptor.connect("notify::active", self.cambiar_destellos)
        ayuda = Gtk.Label(label="← → ↑ ↓ o 1-6 elegir · Enter aplicar · D destellos · Esc salir",
                          hexpand=True, xalign=1)
        ayuda.add_css_class("pie")
        ayuda.set_wrap(True)
        ayuda.set_max_width_chars(34 if self.vertical else 70)
        ayuda.set_justify(Gtk.Justification.RIGHT)
        for w in (chispa, lbl, self.interruptor, ayuda):
            pie.append(w)
        self.panel.append(pie)
        self.set_child(self.velo)

        teclas = Gtk.EventControllerKey()
        teclas.connect("key-pressed", self.tecla)
        self.add_controller(teclas)
        self.seleccionar(self.sel)
        threading.Thread(target=self.cargar_vistas, daemon=True).start()

    def posicion(self, i):
        """(columna, fila) de la tarjeta i."""
        return (i % 2, i // 2) if self.vertical else (i // 2, i % 2)

    def mover(self, dc, df):
        col, fila = self.posicion(self.sel)
        cols, filas = (2, 3) if self.vertical else (3, 2)
        destino = ((col + dc) % cols, (fila + df) % filas)
        self.seleccionar(next(i for i in range(len(ESTILOS)) if self.posicion(i) == destino))

    def clic_en_velo(self, _g, _n, x, y):
        ok, caja = self.panel.compute_bounds(self.velo)
        if ok and not (caja.get_x() <= x <= caja.get_x() + caja.get_width()
                       and caja.get_y() <= y <= caja.get_y() + caja.get_height()):
            self.cerrar()

    def mostrar(self):
        self.present()
        GLib.timeout_add(30, lambda: self.velo.remove_css_class("oculto"))

    def cargar_vistas(self):
        for (tarjeta, pic), origen in zip(self.tarjetas, fuentes(self.cfg, self.idx)):
            ruta = vista_previa(origen)
            if ruta:
                GLib.idle_add(self.poner_vista, pic, ruta)

    @staticmethod
    def poner_vista(pic, ruta):
        if ruta.suffix == ".mp4":
            media = Gtk.MediaFile.new_for_filename(str(ruta))
            media.set_loop(True)
            media.set_muted(True)
            media.play()
            pic.set_paintable(media)
        else:
            pic.set_filename(str(ruta))
        return False

    def seleccionar(self, i):
        self.sel = i
        for j, (tarjeta, _) in enumerate(self.tarjetas):
            (tarjeta.add_css_class if j == i else tarjeta.remove_css_class)("sel")

    def cambiar_destellos(self, sw, _param):
        self.estilo["destellos"] = sw.get_active()
        self.guardar_estilo()

    def guardar_estilo(self):
        ESTADO.mkdir(parents=True, exist_ok=True)
        tmp = ESTILO.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.estilo))
        tmp.replace(ESTILO)

    def aplicar(self, i):
        fondo, modo, *_ = ESTILOS[i]
        self.estilo["fondo"] = fondo
        self.guardar_estilo()
        if modo != self.modo:
            subprocess.Popen(["noctalia", "msg", "theme-mode-set", modo],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.cerrar()

    def cerrar(self):
        if getattr(self, "cerrando", False):
            return
        self.cerrando = True
        LS.set_keyboard_mode(self, LS.KeyboardMode.NONE)  # devolver el teclado ya, no tras el cierre
        for _, pic in self.tarjetas:
            media = pic.get_paintable()
            if isinstance(media, Gtk.MediaStream):
                media.pause()
        self.velo.add_css_class("oculto")

        def fin():
            self.set_visible(False)
            self.get_application().quit()
            return False
        GLib.timeout_add(260, fin)

    def tecla(self, _ctl, keyval, _code, _state):
        nombre = Gdk.keyval_name(keyval) or ""
        if nombre == "Escape":
            self.cerrar()
        elif nombre in ("Return", "KP_Enter", "space"):
            self.aplicar(self.sel)
        elif nombre in ("Right", "l"):
            self.mover(1, 0)
        elif nombre in ("Left", "h"):
            self.mover(-1, 0)
        elif nombre in ("Down", "j"):
            self.mover(0, 1)
        elif nombre in ("Up", "k"):
            self.mover(0, -1)
        elif nombre in [str(n) for n in range(1, len(ESTILOS) + 1)]:
            self.aplicar(int(nombre) - 1)
        elif nombre.lower() == "d":
            self.interruptor.set_active(not self.interruptor.get_active())
        return True


class App(Gtk.Application):
    def __init__(self):
        # Única: si ya está abierto, el segundo SUPER+SHIFT+A no abre otro.
        super().__init__(application_id="dev.yafer.Estilos")

    def do_activate(self):
        if self.get_windows():
            self.get_windows()[0].cerrar()
            return
        with open(CONFIG, "rb") as f:
            cfg = tomllib.load(f)
        Selector(self, cfg).mostrar()


def preparar():
    with open(CONFIG, "rb") as f:
        cfg = tomllib.load(f)
    for idx in range(1, len(cfg.get("escritorio", [])) + 1):
        for origen in fuentes(cfg, idx):
            vista_previa(origen)


if __name__ == "__main__":
    if "--preparar" in sys.argv:
        preparar()
    else:
        App().run(None)
