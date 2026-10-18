#!/usr/bin/env python3
"""escritorios-vivos.py — cada escritorio virtual con su fondo y un aviso bonito.

Escucha los eventos de Hyprland (socket2). Al pasar a otro escritorio (SUPER+1..5):
  1. muestra una tarjeta flotante (icono, nombre, puntitos de posición) en el monitor activo;
  2. pide a noctalia el fondo de ese escritorio para cada monitor (claro u oscuro según el modo).
También vigila el modo de noctalia (settings.toml): al pasar a claro/oscuro cambia los fondos.

Config: ~/.config/hypr/escritorios-temas.toml (se recarga sola al guardarla).
Por qué GTK4 + layer-shell: es lo que ya está instalado y permite una ventana "capa"
transparente, sin foco y que no recibe clics, encima de todo (como el OSD de volumen).
"""
import ctypes

ctypes.CDLL("libgtk4-layer-shell.so")  # debe cargarse antes que GTK

import json
import os
import shutil
import socket
import subprocess
import threading
import tomllib
from pathlib import Path

import cairo
import gi

import temas_comun as tc

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
gi.require_version("Gtk4LayerShell", "1.0")
from gi.repository import Gdk, Gio, GLib, Gtk  # noqa: E402
from gi.repository import Gtk4LayerShell as LS  # noqa: E402

CONFIG = Path.home() / ".config/hypr/escritorios-temas.toml"
NOCT_SETTINGS = Path.home() / ".local/state/noctalia/settings.toml"
ESTADO, ESTILO = tc.ESTADO, tc.ESTILO   # estilo.json lo escribe estilos.py (SUPER+SHIFT+A)
DESTELLOS = Path(__file__).with_name("destellos-cursor.py")
# Eventos que pueden tapar o destapar el fondo (para pausar el video)
EVENTOS_VENTANAS = {"workspacev2", "openwindow", "closewindow", "movewindowv2", "changefloatingmode",
                    "fullscreen", "focusedmonv2"}
HYPR_DIR = Path(os.environ["XDG_RUNTIME_DIR"]) / "hypr" / os.environ["HYPRLAND_INSTANCE_SIGNATURE"]


def hypr_json(cmd):
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
        s.connect(str(HYPR_DIR / ".socket.sock"))
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


def terminar(proc):
    """Cierra un proceso hijo y lo recoge en segundo plano (si no, queda como zombi)."""
    proc.terminate()
    threading.Thread(target=proc.wait, daemon=True).start()


def mezclar(hex_color, otro, t):
    """Mezcla dos colores #rrggbb (t=0 → hex_color, t=1 → otro)."""
    a = [int(hex_color[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(otro[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(a, b))


CSS_BASE = """
window.escritorios-osd { background: transparent; }
.tarjeta {
  margin: 34px;
  padding: 26px 40px 22px 26px;
  min-width: 380px;
  border-radius: 34px;
  background-color: @fondo;
  border: 1px solid @borde;
  box-shadow: 0 18px 50px rgba(0,0,0,0.35), 0 0 0 1px alpha(@acento, 0.18);
  color: @texto;
  font-family: "Adwaita Sans", "Inter", "Cantarell", sans-serif;
  opacity: 1;
  transform: translateY(0) scale(1);
  transition: opacity 260ms cubic-bezier(.2,.8,.2,1), transform 360ms cubic-bezier(.2,1.3,.3,1);
}
.tarjeta.oculta { opacity: 0; transform: translateY(26px) scale(0.92); }
.insignia {
  min-width: 100px; min-height: 100px;
  border-radius: 30px;
  background-image: linear-gradient(135deg, @acento, @acento2);
  box-shadow: 0 8px 24px alpha(@acento, 0.45);
  font-family: "Noto Color Emoji";
  font-size: 52px;
}
.antetitulo { font-size: 13px; font-weight: 800; letter-spacing: 3px; color: @acento_texto; }
.titulo { font-size: 42px; font-weight: 800; letter-spacing: -0.5px; }
.detalle { font-size: 16px; opacity: 0.72; }
.punto {
  min-width: 9px; min-height: 9px; border-radius: 99px;
  background-color: alpha(@texto, 0.22);
  transition: all 300ms cubic-bezier(.2,1.2,.3,1);
}
.punto.activo { min-width: 34px; background-image: linear-gradient(90deg, @acento, @acento2); }
"""


class Aviso(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.add_css_class("escritorios-osd")
        LS.init_for_window(self)
        LS.set_namespace(self, "escritorios-osd")
        LS.set_layer(self, LS.Layer.OVERLAY)
        LS.set_keyboard_mode(self, LS.KeyboardMode.NONE)
        LS.set_exclusive_zone(self, -1)  # sin anclas = centrado en pantalla

        self.tarjeta = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        self.tarjeta.add_css_class("tarjeta")
        self.tarjeta.add_css_class("oculta")
        fila = Gtk.Box(spacing=24)
        self.insignia = Gtk.Label()
        self.insignia.add_css_class("insignia")
        self.insignia.set_valign(Gtk.Align.CENTER)
        textos = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2, valign=Gtk.Align.CENTER)
        self.antetitulo = Gtk.Label(xalign=0)
        self.antetitulo.add_css_class("antetitulo")
        self.titulo = Gtk.Label(xalign=0)
        self.titulo.add_css_class("titulo")
        self.detalle = Gtk.Label(xalign=0)
        self.detalle.add_css_class("detalle")
        for w in (self.antetitulo, self.titulo, self.detalle):
            textos.append(w)
        fila.append(self.insignia)
        fila.append(textos)
        self.puntos = Gtk.Box(spacing=7, halign=Gtk.Align.CENTER)
        self.tarjeta.append(fila)
        self.tarjeta.append(self.puntos)
        self.set_child(self.tarjeta)

        self.css = Gtk.CssProvider()
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(), self.css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.connect("realize", lambda *_: self.get_surface().set_input_region(cairo.Region()))
        self.t_ocultar = self.t_cerrar = None
        self.monitor_actual = None

    def colores(self, acento, modo):
        if modo == "light":
            fondo, borde, texto = "rgba(250,250,252,0.84)", "rgba(255,255,255,0.9)", "#1d1b22"
            acento_texto = mezclar(acento, "#000000", 0.45)
        else:
            fondo, borde, texto = "rgba(16,16,22,0.80)", "rgba(255,255,255,0.10)", "#f5f3fa"
            acento_texto = acento
        acento2 = mezclar(acento, "#ffffff", 0.35)
        defs = (f"@define-color fondo {fondo}; @define-color borde {borde}; @define-color texto {texto};"
                f"@define-color acento {acento}; @define-color acento2 {acento2};"
                f"@define-color acento_texto {acento_texto};")
        self.css.load_from_string(defs + CSS_BASE)

    def mostrar(self, info, modo, conector, segundos):
        self.colores(info["color"], modo)
        self.insignia.set_label(info["icono"])
        self.antetitulo.set_label(info["antetitulo"].upper())
        self.titulo.set_label(info["nombre"])
        self.detalle.set_label(info["detalle"])
        self.detalle.set_visible(bool(info["detalle"]))
        while (hijo := self.puntos.get_first_child()):
            self.puntos.remove(hijo)
        for i in range(1, info["total"] + 1):
            p = Gtk.Box()
            p.add_css_class("punto")
            if i == info["indice"]:
                p.add_css_class("activo")
            self.puntos.append(p)
        self.puntos.set_visible(info["total"] > 0)

        mon = next((m for m in Gdk.Display.get_default().get_monitors()
                    if m.get_connector() == conector), None)
        if mon is not None and mon != self.monitor_actual:
            if self.get_visible():
                self.set_visible(False)
            LS.set_monitor(self, mon)
            self.monitor_actual = mon
        for t in (self.t_ocultar, self.t_cerrar):
            if t:
                GLib.source_remove(t)
        self.t_cerrar = None
        if not self.get_visible():
            self.tarjeta.add_css_class("oculta")
            self.present()
            GLib.timeout_add(30, lambda: self.tarjeta.remove_css_class("oculta"))
        else:
            self.tarjeta.remove_css_class("oculta")
        self.t_ocultar = GLib.timeout_add(int(segundos * 1000), self.ocultar)

    def ocultar(self):
        self.t_ocultar = None
        self.tarjeta.add_css_class("oculta")
        self.t_cerrar = GLib.timeout_add(380, self._cerrar)
        return False

    def _cerrar(self):
        self.t_cerrar = None
        self.set_visible(False)
        return False


class App(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="dev.yafer.EscritoriosVivos",
                         flags=Gio.ApplicationFlags.NON_UNIQUE)
        self.actual = None          # clave del escritorio mostrado (int o nombre)
        self.modo = leer_modo()
        self.fondos_puestos = {}    # conector -> ruta
        self.t_fondos = None
        self.estilo = tc.leer_estilo()
        self.mpv = {}               # conector -> {"proc", "sock", "ruta"}
        self.destellos = None       # proceso de destellos-cursor.py

    def do_activate(self):
        self.hold()
        self.cargar_config()
        self.aviso = Aviso(self)
        self.vigilar(CONFIG, self.al_cambiar_config)
        self.vigilar(NOCT_SETTINGS, self.al_cambiar_noctalia)
        ESTADO.mkdir(parents=True, exist_ok=True)
        if not ESTILO.exists():
            tc.guardar_estilo(self.estilo)
        self.vigilar(ESTILO, self.al_cambiar_estilo)
        # Restos de una sesión anterior de este programa (si se reinició)
        subprocess.run(["pkill", "-x", "mpvpaper"], stderr=subprocess.DEVNULL)
        subprocess.run(["pkill", "-f", f"python3 {DESTELLOS}"], stderr=subprocess.DEVNULL)
        self.aplicar_destellos()
        # Vistas previas del selector de estilos (SUPER+SHIFT+A), en segundo plano y con baja prioridad
        subprocess.Popen(["nice", "-n", "15", "python3", str(Path(__file__).with_name("temas_comun.py"))],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        threading.Thread(target=self.escuchar_hyprland, daemon=True).start()
        # Al iniciar sesión: espera a que noctalia esté arriba y pone el fondo del escritorio actual.
        GLib.timeout_add_seconds(3, self.estado_inicial)

    # --- config y vigilancia de archivos -------------------------------------------------
    def cargar_config(self):
        try:
            with open(CONFIG, "rb") as f:
                self.cfg = tomllib.load(f)
        except (OSError, tomllib.TOMLDecodeError) as e:
            print("escritorios-vivos: config inválida:", e, flush=True)
            self.cfg = getattr(self, "cfg", {"general": {}, "escritorio": []})
        self.gen = self.cfg.get("general", {})
        self.n = int(self.gen.get("por_monitor", 5))
        self.carpeta = Path(os.path.expanduser(self.gen.get("carpeta", "~")))

    def vigilar(self, ruta, funcion):
        mon = Gio.File.new_for_path(str(ruta)).monitor_file(Gio.FileMonitorFlags.WATCH_MOVES, None)
        mon.connect("changed", lambda *_: self.retrasar(f"v-{ruta}", 250, funcion))
        setattr(self, f"_mon_{ruta.name}", mon)  # que no lo recolecte el GC

    def retrasar(self, clave, ms, funcion):
        attr = f"_t_{clave}"
        if getattr(self, attr, None):
            GLib.source_remove(getattr(self, attr))

        def correr():
            setattr(self, attr, None)
            funcion()
            return False
        setattr(self, attr, GLib.timeout_add(ms, correr))

    def al_cambiar_config(self):
        self.cargar_config()
        self.fondos_puestos.clear()
        self.poner_fondos()

    def al_cambiar_noctalia(self):
        modo = leer_modo()
        if modo == self.modo:
            return
        self.modo = modo
        claro = modo == "light"
        self.iconos(claro)
        # Tema del otro modo (p. ej. Sharingan en modo claro): saltar al último tema usado
        # de este modo. Se lee del disco porque estilos.py guarda el tema ANTES de cambiar el modo.
        nuevo = tc.leer_estilo()
        if nuevo.get("modo") != modo:  # cambio con SUPER+SHIFT+D / botón de la barra, no desde el selector
            ligado = tc.modo_de(nuevo["tema"], nuevo)
            destino = nuevo["ultimo"].get(modo) or (f"mezcla:{modo}" if ligado else nuevo["tema"])
            nuevo["tema"], nuevo["modo"] = destino, modo
            tc.guardar_estilo(nuevo)
        if self.aplicar_estilo(nuevo, forzar_fondos=True):
            return  # ya mostró el aviso del tema nuevo
        self.aviso.mostrar({
            "nombre": "Modo claro" if claro else "Modo oscuro",
            "icono": "☀️" if claro else "🌙",
            "detalle": "SUPER+SHIFT+D cambia · SUPER+SHIFT+A estilos",
            "antetitulo": "Apariencia",
            "color": "#ffb347" if claro else "#8fa8ff",
            "indice": 0, "total": 0,
        }, modo, self.monitor_activo(), self.gen.get("aviso_segundos", 1.6))

    @staticmethod
    def iconos(claro):
        """Iconos Papirus-Dark/Light (Qt/KDE y GTK) y cursor Bibata Ice/Classic según el modo."""
        tema = "Papirus-Light" if claro else "Papirus-Dark"
        cursor = "Bibata-Modern-Classic" if claro else "Bibata-Modern-Ice"
        for args in (["kwriteconfig6", "--file", "kdeglobals", "--group", "Icons", "--key", "Theme", tema],
                     ["gsettings", "set", "org.gnome.desktop.interface", "icon-theme", tema],
                     # cursor: blanco sobre oscuro, negro sobre claro (se ve siempre)
                     ["hyprctl", "setcursor", cursor, os.environ.get("XCURSOR_SIZE", "24")],
                     ["gsettings", "set", "org.gnome.desktop.interface", "cursor-theme", cursor]):
            subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def al_cambiar_estilo(self):
        self.aplicar_estilo(tc.leer_estilo())

    def aplicar_estilo(self, nuevo, forzar_fondos=False):
        """Aplica estilo.json; devuelve True si cambió de tema (y mostró su aviso)."""
        cambio_tema = nuevo["tema"] != self.estilo["tema"]
        cambio_mezcla = nuevo.get("mezcla") != self.estilo.get("mezcla")  # 1-5 en la Galería
        self.estilo = nuevo
        self.aplicar_destellos()
        if not cambio_tema:
            if forzar_fondos or cambio_mezcla:
                self.escribir_acento()
                self.poner_fondos()
            return False
        modo_tema = tc.modo_de(nuevo["tema"], nuevo) or nuevo.get("modo") or self.modo
        if self.estilo["ultimo"].get(modo_tema) != nuevo["tema"]:  # recordar para SUPER+SHIFT+D
            self.estilo["ultimo"][modo_tema] = nuevo["tema"]
            tc.guardar_estilo(self.estilo)
        self.escribir_acento()
        self.poner_fondos()
        col = tc.buscar_coleccion(nuevo["tema"], nuevo)
        fondo = tc.fondo_para(nuevo, self.escritorio())
        if col:
            info = {"nombre": col["nombre"], "icono": col["icono"],
                    "detalle": "Un fondo animado distinto en cada escritorio", "color": tc.acento(fondo) if fondo else tc.ACENTO_POR_DEFECTO}
        elif fondo:
            info = {"nombre": fondo["nombre"], "icono": "🌙" if fondo["modo"] == "dark" else "☀️",
                    "detalle": "Tema animado en todos tus escritorios", "color": tc.acento(fondo)}
        else:
            nombre, detalle, icono = tc.POR_ESCRITORIO[nuevo["tema"]]
            info = {"nombre": nombre, "icono": icono, "detalle": detalle, "color": "#c9a7ff"}
        self.aviso.mostrar({**info, "antetitulo": "Tema", "indice": 0, "total": 0},
                           self.modo, self.monitor_activo(), self.gen.get("aviso_segundos", 1.6))
        return True

    def escritorio(self):
        return self.actual if isinstance(self.actual, int) else 1

    def escribir_acento(self):
        """Color de los destellos del cursor: el del fondo de video de este escritorio, o el del escritorio."""
        t = tc.fondo_para(self.estilo, self.escritorio())
        color = tc.acento(t) if t else (self.info_de(self.actual)["color"] if self.actual else tc.ACENTO_POR_DEFECTO)
        try:
            (ESTADO / "acento").write_text(color)
        except OSError:
            pass

    def aplicar_destellos(self):
        vivo = self.destellos is not None and self.destellos.poll() is None
        if self.estilo["destellos"] and not vivo:
            self.destellos = subprocess.Popen(["python3", str(DESTELLOS)],
                                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif not self.estilo["destellos"] and vivo:
            terminar(self.destellos)
            self.destellos = None

    # --- hyprland --------------------------------------------------------------------------
    def escuchar_hyprland(self):
        while True:
            try:
                with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
                    s.connect(str(HYPR_DIR / ".socket2.sock"))
                    buf = b""
                    while chunk := s.recv(4096):
                        buf += chunk
                        *lineas, buf = buf.split(b"\n")
                        for l in lineas:
                            ev, _, datos = l.decode(errors="replace").partition(">>")
                            if ev == "workspacev2":
                                wid, _, nombre = datos.partition(",")
                                GLib.idle_add(self.al_cambiar_workspace, int(wid), nombre)
                            if ev in EVENTOS_VENTANAS:
                                GLib.idle_add(self.retrasar, "pausa", 250, self.revisar_pausa)
            except OSError as e:
                print("escritorios-vivos: socket2:", e, flush=True)
            threading.Event().wait(2)

    def clave_de(self, wid, nombre):
        if 1 <= wid <= self.n * 2:
            return (wid - 1) % self.n + 1
        if nombre.startswith("special"):
            return None
        return nombre if nombre in self.cfg.get("nombres", {}) else None

    def info_de(self, clave):
        if isinstance(clave, int):
            lista = self.cfg.get("escritorio", [])
            e = lista[clave - 1] if clave <= len(lista) else {}
            return {"nombre": e.get("nombre", f"Escritorio {clave}"), "icono": e.get("icono", "🖥️"),
                    "detalle": e.get("detalle", ""), "color": e.get("color", "#8fa8ff"),
                    "antetitulo": f"Escritorio {clave}", "indice": clave, "total": self.n}
        e = self.cfg["nombres"][clave]
        return {"nombre": e.get("nombre", clave), "icono": e.get("icono", "🖥️"),
                "detalle": e.get("detalle", ""), "color": e.get("color", "#8fa8ff"),
                "antetitulo": "Espacio", "indice": 0, "total": 0}

    def monitor_activo(self):
        try:
            return next(m["name"] for m in hypr_json("monitors") if m["focused"])
        except (OSError, StopIteration, ValueError):
            return None

    def al_cambiar_workspace(self, wid, nombre):
        clave = self.clave_de(wid, nombre)
        if clave is None or clave == self.actual:
            return False
        self.actual = clave
        if self.gen.get("aviso_activo", True):
            self.aviso.mostrar(self.info_de(clave), self.modo, self.monitor_activo(),
                               self.gen.get("aviso_segundos", 1.6))
        self.escribir_acento()
        if isinstance(clave, int):
            self.retrasar("fondos", 120, self.poner_fondos)
        return False

    def estado_inicial(self):
        try:
            ws = hypr_json("activeworkspace")
            self.actual = self.clave_de(ws["id"], ws["name"])
        except (OSError, ValueError, KeyError):
            self.actual = 1
        self.iconos(self.modo == "light")
        self.escribir_acento()
        self.poner_fondos()
        return False

    # --- fondos ----------------------------------------------------------------------------
    def poner_fondos(self):
        if not self.gen.get("fondos_activos", True) or not isinstance(self.actual, int):
            return
        lista = self.cfg.get("escritorio", [])
        if self.actual > len(lista):
            return
        e = lista[self.actual - 1]
        sufijo = "claro" if self.modo == "light" else "oscuro"
        try:
            monitores = hypr_json("monitors")
        except (OSError, ValueError):
            return
        tema = tc.fondo_para(self.estilo, self.actual)
        for m in monitores:
            vertical = m.get("transform", 0) % 2 == 1
            if tema:  # tema de video: su póster queda de respaldo bajo el video
                ruta = str(tc.rutas(tema)["poster"])
            else:
                rel = (e.get(f"vertical_{sufijo}") if vertical else None) or e.get(f"fondo_{sufijo}")
                if not rel:
                    continue
                ruta = str(self.carpeta / os.path.expanduser(rel))
            if self.fondos_puestos.get(m["name"]) == ruta or not os.path.exists(ruta):
                continue
            self.fondos_puestos[m["name"]] = ruta
            subprocess.Popen(["noctalia", "msg", "wallpaper-set", m["name"], ruta],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # El fondo fijo queda siempre debajo (respaldo); el video va encima en la capa "bottom".
        self.poner_videos(e, sufijo, monitores)

    # --- fondos animados (mpvpaper: mpv como fondo, decodifica con la GPU) ------------------
    def video_para(self, e, sufijo, vertical):
        tema = tc.fondo_para(self.estilo, self.escritorio())
        if tema:  # el video de este escritorio en todos los monitores; en el vertical mpv recorta el centro (panscan)
            ruta = tema["video"]
        elif self.estilo["tema"] == "escritorios:video":
            rel = e.get(f"video_vertical_{sufijo}" if vertical else f"video_{sufijo}")
            ruta = self.carpeta / os.path.expanduser(rel) if rel else None
        else:
            ruta = None
        return str(ruta) if ruta and ruta.exists() else None

    def poner_videos(self, e, sufijo, monitores):
        if not shutil.which("mpvpaper"):
            return
        nuevo = False
        for m in monitores:
            nombre = m["name"]
            ruta = self.video_para(e, sufijo, m.get("transform", 0) % 2 == 1)
            actual = self.mpv.get(nombre)
            vivo = actual is not None and actual["proc"].poll() is None
            if not ruta:
                if vivo:
                    terminar(actual["proc"])
                self.mpv.pop(nombre, None)
                continue
            if vivo and actual["ruta"] == ruta:
                continue
            if vivo and self.transicion(actual, ruta):
                continue
            if vivo:
                terminar(actual["proc"])
            sock = ESTADO / f"mpv-{nombre}.sock"
            # config=no: sin tu mpv.conf/scripts (velocidad 2x, uosc y el socket de notas son para tu mpv normal)
            opciones = (f"config=no load-scripts=no osc=no osd-level=0 no-audio loop-file=inf hwdec=auto-safe panscan=1.0 keep-open=yes "
                        f"input-ipc-server={sock} profile=fast")
            proc = subprocess.Popen(["mpvpaper", "-p", "-a", "FULL", "-l", "bottom", "-o", opciones, nombre, ruta],
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.mpv[nombre] = {"proc": proc, "sock": sock, "ruta": ruta}
            nuevo = True
        if nuevo:  # mpv recién lanzado tarda en abrir su socket
            self.retrasar("pausa", 1500, self.revisar_pausa)
        else:
            self.retrasar("pausa", 150, self.revisar_pausa)

    def transicion(self, info, ruta):
        """Cambia el video con estilo: el nuevo entra desde oscuro (o claro, en modo claro) con un
        leve zoom que se asienta, en vez de cortar de golpe. Usa el ecualizador y el zoom de mpv
        (los aplica la GPU al dibujar, no cuesta nada)."""
        sock = info["sock"]
        brillo0, zoom0, ms = tc.EFECTOS[self.estilo.get("efecto", "seda")]["fondo"]
        if brillo0 < 0 and self.modo == "light":
            brillo0 = -brillo0 // 2  # en modo claro entra desde claro, no desde negro
        if info.get("t_trans"):  # una transición a medias: se corta y se deja el video normal
            GLib.source_remove(info["t_trans"])
            info["t_trans"] = None
            self.mpv_comando(sock, ["set_property", "brightness", 0])
            self.mpv_comando(sock, ["set_property", "video-zoom", 0])
        if not ms:  # efecto "Rápido": sin animación del fondo
            if not self.mpv_comando(sock, ["loadfile", ruta]):
                return False
            info["ruta"] = ruta
            return True
        if not self.mpv_comando(sock, ["set_property", "brightness", brillo0]):
            return False
        self.mpv_comando(sock, ["set_property", "video-zoom", zoom0])
        if not self.mpv_comando(sock, ["loadfile", ruta]):
            return False
        info["ruta"] = ruta
        pasos, paso = max(1, ms // 16), [0]  # a ~60 fps

        def avanzar():
            paso[0] += 1
            t = paso[0] / pasos
            resto = (1 - t) ** 3  # ease-out cúbico: rápido al principio, se asienta suave
            self.mpv_comando(sock, ["set_property", "brightness", round(brillo0 * resto)])
            self.mpv_comando(sock, ["set_property", "video-zoom", zoom0 * resto])
            if paso[0] >= pasos:
                info["t_trans"] = None
                return False
            return True

        # pequeña espera: que el video nuevo muestre su primer cuadro antes de aclararse
        def empezar():
            info["t_trans"] = GLib.timeout_add(16, avanzar)
            return False
        info["t_trans"] = GLib.timeout_add(110, empezar)
        return True

    def revisar_pausa(self):
        """Pausa el video del monitor cuyo escritorio tiene ventanas en mosaico (lo tapan casi
        entero) y lo reanuda cuando queda vacío. mpvpaper -p no lo detecta en Hyprland."""
        if not self.mpv:
            return
        try:
            activos = {m["name"]: m["activeWorkspace"]["id"] for m in hypr_json("monitors")}
            ocupados = {c["workspace"]["id"] for c in hypr_json("clients")
                        if c.get("mapped", True) and not c.get("hidden") and not c.get("floating")}
        except (OSError, ValueError, KeyError):
            return
        for nombre, info in self.mpv.items():
            pausa = activos.get(nombre) in ocupados
            if info.get("pausa") != pausa and self.mpv_comando(info["sock"], ["set_property", "pause", pausa]):
                info["pausa"] = pausa

    @staticmethod
    def mpv_comando(sock, comando):
        try:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                s.connect(str(sock))
                s.sendall((json.dumps({"command": comando}) + "\n").encode())
            return True
        except OSError:
            return False


if __name__ == "__main__":
    App().run(None)
