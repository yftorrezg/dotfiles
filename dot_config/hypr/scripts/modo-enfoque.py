#!/usr/bin/env python3
"""modo-enfoque.py — SUPER+ALT+N: fondo negro total para concentrarse (activa/desactiva).

Activo: cada monitor queda en negro (capa "bottom": debajo de las ventanas, encima del fondo,
del video de mpvpaper y de los widgets), se ocultan widgets y barra (el dock queda en auto-hide: aparece al pasar el mouse por el borde inferior), y solo queda la hora
chiquita abajo a la derecha del monitor principal. Al desactivar, todo vuelve como estaba.

El flag ~/.local/state/escritorios-vivos/enfoque guarda el pid del demonio; escritorios-vivos.py lo
vigila para no poner fondos ni tarjetas mientras dura el modo.
Uso: modo-enfoque.py [toggle]   (el modo demonio, --demonio, lo lanza el propio toggle)
"""
import ctypes

ctypes.CDLL("libgtk4-layer-shell.so")  # debe cargarse antes que GTK

import os
import subprocess
import sys
import time
from pathlib import Path

import cairo
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
gi.require_version("Gtk4LayerShell", "1.0")
from gi.repository import Gdk, Gio, GLib, Gtk  # noqa: E402
from gi.repository import Gtk4LayerShell as LS  # noqa: E402

FLAG = Path.home() / ".local/state/escritorios-vivos/enfoque"
PRINCIPAL = "DP-2"   # monitor del reloj; si no existe (laptop), el primero que haya
CSS = """
window.enfoque-negro { background: #000000; }
window.enfoque-reloj { background: transparent; }
.reloj { color: #6b6b6b; font-size: 15px; font-weight: 600; margin: 14px 18px;
         font-family: "Adwaita Sans", "Inter", "Cantarell", sans-serif; }
"""


def noctalia(*args):
    subprocess.run(["noctalia", "msg", *args], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def pid_vivo(pid):
    """True si pid es de verdad un demonio de este script (no un pid reciclado)."""
    try:
        return "modo-enfoque" in Path(f"/proc/{pid}/cmdline").read_text()
    except OSError:
        return False


def leer_pid():
    try:
        return int(FLAG.read_text().strip())
    except (OSError, ValueError):
        return None


def mostrar_interfaz():
    noctalia("desktop-widgets-show")
    noctalia("bar-show")
    noctalia("dock-show")


def desactivar(pid):
    FLAG.unlink(missing_ok=True)  # primero el flag: escritorios-vivos repone el fondo al verlo caer
    if pid and pid_vivo(pid):
        try:
            os.kill(pid, 15)
        except OSError:
            pass
    mostrar_interfaz()


def activar():
    FLAG.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.Popen([sys.executable, __file__, "--demonio"], start_new_session=True,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    FLAG.write_text(str(proc.pid))
    noctalia("desktop-widgets-hide")
    noctalia("bar-hide")
    noctalia("dock-show")  # el dock está en auto-hide (config.toml [dock]): solo sale al pasar el mouse por abajo


def toggle():
    pid = leer_pid()
    if FLAG.exists():  # activo (o restos de un demonio caído: se limpia igual)
        desactivar(pid)
    else:
        activar()


class Enfoque(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="dev.yafer.ModoEnfoque", flags=Gio.ApplicationFlags.NON_UNIQUE)

    def do_activate(self):
        self.hold()
        css = Gtk.CssProvider()
        css.load_from_string(CSS)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(), css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        monitores = list(Gdk.Display.get_default().get_monitors())
        principal = next((m for m in monitores if m.get_connector() == PRINCIPAL), monitores[0] if monitores else None)
        for mon in monitores:
            self.negro(mon)
        if principal is not None:
            self.reloj(principal)

    def capa(self, mon, nombre, capa):
        v = Gtk.ApplicationWindow(application=self)
        v.add_css_class(nombre)
        LS.init_for_window(v)
        LS.set_namespace(v, nombre)
        LS.set_layer(v, capa)
        LS.set_monitor(v, mon)
        LS.set_keyboard_mode(v, LS.KeyboardMode.NONE)
        v.connect("realize", lambda w: w.get_surface().set_input_region(cairo.Region()))  # click-through
        return v

    def negro(self, mon):
        v = self.capa(mon, "enfoque-negro", LS.Layer.BOTTOM)
        LS.set_exclusive_zone(v, -1)
        for borde in (LS.Edge.TOP, LS.Edge.BOTTOM, LS.Edge.LEFT, LS.Edge.RIGHT):
            LS.set_anchor(v, borde, True)
        v.present()

    def reloj(self, mon):
        v = self.capa(mon, "enfoque-reloj", LS.Layer.OVERLAY)
        LS.set_anchor(v, LS.Edge.BOTTOM, True)
        LS.set_anchor(v, LS.Edge.RIGHT, True)
        etiqueta = Gtk.Label(label=time.strftime("%H:%M"))
        etiqueta.add_css_class("reloj")
        v.set_child(etiqueta)

        def refrescar():
            etiqueta.set_label(time.strftime("%H:%M"))
            return True
        GLib.timeout_add_seconds(15, refrescar)
        v.present()


if __name__ == "__main__":
    if "--demonio" in sys.argv:
        Enfoque().run(None)
    else:
        toggle()
