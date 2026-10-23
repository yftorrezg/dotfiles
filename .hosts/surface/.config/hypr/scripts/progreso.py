#!/usr/bin/env python3
"""Barrita de progreso discreta en la pantalla de la laptop (o una notificación de respaldo).

Los que trabajan (yt-dlp, auto-captura.py, cuadernillo.py) escriben su avance en un archivo;
este script lo lee y muestra una barrita fina, semitransparente, abajo a la derecha de la
pantalla interna de la laptop (eDP-1). No toma el foco ni los clics (pasan a la ventana de abajo):

    📚 Título del video…   3/10 · 📸 48 guardadas · 48% · ~12 min
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━───────────────────────────────

Durante el proceso NO manda notificaciones; al terminar muestra "✅ Listo"/"❌ Falló" unos
segundos, se cierra y ahí sí manda UNA notificación breve con el resultado.

Variables de entorno (las pone video-a-capturas.sh / curso-a-apuntes.sh):
    PROGRESO_ARCHIVO   archivo de estado ("pct|etapa|detalle|clase")
    PROGRESO_RANGO     "25 85": esta etapa ocupa del 25 % al 85 % de la barra
    PROGRESO_CLASE     "3/10": en qué clase del curso va
Opcionales (para "seguir"):
    PROGRESO_MODO      "notificacion": la notificación de siempre en vez de la barrita
    PROGRESO_MONITOR   conector del monitor (por defecto eDP-1 = la pantalla de la laptop; si
                       está apagada —tapa cerrada con la Arzopa— o no existe, el que elija
                       Hyprland = el enfocado). "enfocado" = siempre el monitor con el foco
Uso:
    progreso.py seguir <archivo> <título>     # muestra/actualiza la barrita hasta "fin"
    progreso.py poner <pct 0-100> <etapa> [detalle]   # desde bash (usa PROGRESO_ARCHIVO/RANGO)
"""
import os
import subprocess
import sys
import time

ETAPAS = {"descarga": "📥 Descargando", "capturas": "📸 Capturas", "apuntes": "🤖 Apuntes",
          "fin": "✅ Listo", "error": "❌ Falló"}
LIB_CAPA = "/usr/lib/libgtk4-layer-shell.so"  # tiene que cargarse ANTES que GTK (ver main)
# Laptop: la interna está siempre (con o sin la Arzopa, que entra como HDMI-A-1 o DP-x)
MONITOR = os.environ.get("PROGRESO_MONITOR", "eDP-1")
ANCHO, ALTO, MARGEN, SEPARACION = 420, 28, 8, 4  # px: la barrita mide ~ 420 x 28
SIN_NOVEDAD = 60 * 60  # si el archivo no cambia en 1 h, el que escribía murió: cerrar


def reportar(pct, etapa, detalle=""):
    """Escribe el avance (pct de ESTA etapa, 0-100) mapeado al rango global de la barra."""
    archivo = os.environ.get("PROGRESO_ARCHIVO")
    if not archivo:
        return
    try:
        ini, fin = (float(x) for x in os.environ.get("PROGRESO_RANGO", "0 100").split())
        total = ini + max(0.0, min(100.0, float(pct))) * (fin - ini) / 100
        tmp = archivo + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(f"{total:.1f}|{etapa}|{detalle}|{os.environ.get('PROGRESO_CLASE', '')}")
        os.replace(tmp, archivo)
    except (OSError, ValueError):
        pass  # el progreso nunca debe frenar el trabajo


def barra(pct, ancho=10):
    llenos = int(round(pct / 100 * ancho))
    return "▰" * llenos + "▱" * (ancho - llenos)


def notificar(nid, titulo, cuerpo, persistente=True, urgente=False):
    cmd = ["notify-send", "-p", "-a", "Auto-captura", "-t", "0" if persistente else "15000"]
    if nid:
        cmd += ["-r", str(nid)]
    if urgente:
        cmd += ["-u", "critical"]
    entorno = {k: v for k, v in os.environ.items() if k != "LD_PRELOAD"}  # no heredar la precarga
    r = subprocess.run(cmd + [titulo, cuerpo], capture_output=True, text=True, env=entorno)
    return r.stdout.strip() or nid


class Estado:
    """Lee el archivo de estado y calcula lo que se muestra (lo comparten barrita y notificación)."""

    def __init__(self, archivo, titulo):
        self.archivo, self.titulo = archivo, titulo
        self.t0, self.pct_prev, self.clase_prev = time.time(), 0.0, None
        self.visto = time.time()  # última vez que el archivo existía / cambió
        self.mtime = None

    def leer(self):
        """-> (pct, etapa, detalle, clase, falta). etapa "error" si el que escribía desapareció."""
        try:
            mtime = os.path.getmtime(self.archivo)
            pct, etapa, detalle, clase = open(self.archivo, encoding="utf-8").read().split("|", 3)
            pct = float(pct)
            if mtime != self.mtime:
                self.mtime, self.visto = mtime, time.time()
        except (OSError, ValueError):
            pct, etapa, detalle, clase = self.pct_prev, "descarga", "", self.clase_prev or ""
            if not os.path.exists(self.archivo) and time.time() - self.visto > 30:
                return 0.0, "error", "Se cortó el proceso (sin archivo de progreso)", clase, ""
        if time.time() - self.visto > SIN_NOVEDAD:
            return pct, "error", "Sin novedades hace una hora: ¿se colgó?", clase, ""
        if clase != self.clase_prev or pct < self.pct_prev - 5:  # empezó otra clase: reiniciar el reloj
            self.t0, self.clase_prev = time.time(), clase
        self.pct_prev = pct
        falta = ""
        transcurrido = time.time() - self.t0
        if pct >= 3 and transcurrido > 20:
            minutos = transcurrido / pct * (100 - pct) / 60
            falta = f"~{minutos:.0f} min" if minutos >= 1 else "< 1 min"
        return pct, etapa, detalle, clase, falta

    def final(self, etapa, detalle):
        """Notificación breve del resultado (única notificación de todo el proceso)."""
        corto = self.titulo if len(self.titulo) <= 45 else self.titulo[:44] + "…"
        cuerpo = detalle or ("Capturas y apuntes listos" if etapa == "fin"
                             else "Revisá el log en ~/.cache/auto-captura/")
        notificar(None, f"{ETAPAS[etapa]} · {corto}", cuerpo, persistente=False, urgente=etapa == "error")

    def borrar(self):
        try:
            os.remove(self.archivo)
        except OSError:
            pass


def seguir_notificacion(archivo, titulo):
    """Respaldo: la notificación de siempre, que se actualiza sola (PROGRESO_MODO=notificacion)."""
    est, nid, ultimo = Estado(archivo, titulo), None, None
    corto = titulo if len(titulo) <= 45 else titulo[:44] + "…"
    while True:
        pct, etapa, detalle, clase, falta = est.leer()
        if etapa in ("fin", "error"):
            cuerpo = detalle or ("Capturas y apuntes listos" if etapa == "fin" else "Revisá el log en ~/.cache/auto-captura/")
            notificar(nid, f"{ETAPAS[etapa]} · {corto}", cuerpo, persistente=False, urgente=etapa == "error")
            break
        cab = f"{corto} · clase {clase}" if clase else corto
        linea2 = ETAPAS.get(etapa, etapa) + (f" · {detalle}" if detalle else "") + (f" · faltan {falta}" if falta else "")
        estado = (int(pct), etapa, detalle, clase, falta)
        if estado != ultimo:  # solo si cambió algo (no molestar de más)
            nid = notificar(nid, f"📚 {cab}", f"{barra(pct)}  {pct:.0f}%\n{linea2}")
            ultimo = estado
        time.sleep(3)
    est.borrar()


def _lugar(nombre):
    """Toma un "lugar" con un candado (flock) que dura lo que vive el proceso.
    Devuelve el descriptor, o None si ya está tomado."""
    import fcntl
    carpeta = os.path.join(os.environ.get("XDG_RUNTIME_DIR", "/tmp"), "progreso-barritas")
    os.makedirs(carpeta, exist_ok=True)
    fd = os.open(os.path.join(carpeta, nombre), os.O_CREAT | os.O_RDWR, 0o600)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return fd
    except OSError:
        os.close(fd)
        return None


CSS = b"""
window.progreso { background: transparent; }
.pastilla {
    background-color: rgba(18, 18, 24, 0.55);
    border-radius: 7px;
    padding: 3px 10px 4px 10px;
}
.pastilla label { color: rgba(235, 235, 245, 0.88); font-size: 8.5pt; }
.pastilla label.datos { color: rgba(235, 235, 245, 0.70); }
"""


def seguir_barrita(archivo, titulo):
    """Barrita layer-shell en la pantalla de la laptop. Devuelve False si no se pudo mostrar
    (sin Wayland, sin layer-shell…) para caer a la notificación."""
    import gi
    gi.require_version("Gtk", "4.0")
    gi.require_version("Gtk4LayerShell", "1.0")
    gi.require_foreign("cairo")
    import cairo
    from gi.repository import GLib, Gtk, Gdk, Pango
    from gi.repository import Gtk4LayerShell as Capa

    if not Gtk.init_check() or not Capa.is_supported():
        return False
    # Una sola barrita por archivo de estado (si ya hay una siguiéndolo, no abrir otra)
    candado = "archivo-" + os.path.basename(archivo)
    if _lugar(candado) is None:
        return True
    # Si hay varias a la vez (otro video en paralelo), se apilan hacia arriba sin encimarse
    fila = next((i for i in range(8) if _lugar(f"fila-{i}") is not None), 0)

    est = Estado(archivo, titulo)
    prov = Gtk.CssProvider()
    prov.load_from_data(CSS, len(CSS))
    Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), prov,
                                              Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
    app_loop = GLib.MainLoop()
    ui = {"pct": 0.0, "color": (0.49, 0.64, 0.97)}  # azul mientras trabaja

    win = Gtk.Window(title="Progreso auto-captura")
    win.add_css_class("progreso")
    Capa.init_for_window(win)
    Capa.set_namespace(win, "progreso-cursos")
    Capa.set_layer(win, Capa.Layer.OVERLAY)       # encima de todo, pero…
    Capa.set_keyboard_mode(win, Capa.KeyboardMode.NONE)  # …sin robar el teclado
    Capa.set_exclusive_zone(win, 0)                # no empuja ventanas
    Capa.set_anchor(win, Capa.Edge.BOTTOM, True)   # abajo a la derecha: la zona menos leída
    Capa.set_anchor(win, Capa.Edge.RIGHT, True)
    Capa.set_margin(win, Capa.Edge.RIGHT, 20)      # deja libre la barra de desplazamiento
    Capa.set_margin(win, Capa.Edge.BOTTOM, MARGEN + fila * (ALTO + SEPARACION))

    def elegir_monitor():
        """El monitor por conector (no por índice); si no está, None = el que elija Hyprland."""
        if MONITOR in ("", "enfocado"):
            return None
        mons = Gdk.Display.get_default().get_monitors()
        for i in range(mons.get_n_items()):
            m = mons.get_item(i)
            if m.get_connector() == MONITOR:
                return m
        return None

    Capa.set_monitor(win, elegir_monitor())

    caja = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
    caja.add_css_class("pastilla")
    caja.set_size_request(ANCHO, -1)
    fila_txt = Gtk.Box(spacing=6)
    lbl_titulo = Gtk.Label(label=f"📚 {titulo}", xalign=0, hexpand=True)
    lbl_titulo.set_ellipsize(Pango.EllipsizeMode.END)  # el título se corta; los datos no
    lbl_titulo.set_max_width_chars(1)  # que no agrande la ventana: ocupa lo que sobre de ANCHO
    lbl_datos = Gtk.Label(label="", xalign=1)
    lbl_datos.add_css_class("datos")
    fila_txt.append(lbl_titulo)
    fila_txt.append(lbl_datos)

    def dibujar(_area, cr, ancho, alto):  # barra de verdad: 3 px, redondeada
        r = alto / 2
        def pildora(w):
            cr.new_sub_path()
            cr.arc(r, r, r, 0.5 * 3.1416, 1.5 * 3.1416)
            cr.arc(max(r, w - r), r, r, 1.5 * 3.1416, 0.5 * 3.1416)
            cr.close_path()
        cr.set_source_rgba(1, 1, 1, 0.18)
        pildora(ancho)
        cr.fill()
        lleno = ancho * max(0.0, min(100.0, ui["pct"])) / 100
        if lleno > 0:
            cr.set_source_rgba(*ui["color"], 0.95)
            pildora(max(lleno, alto))
            cr.fill()

    area = Gtk.DrawingArea()
    area.set_content_height(3)
    area.set_draw_func(dibujar)
    caja.append(fila_txt)
    caja.append(area)
    win.set_child(caja)

    def sin_clics(*_):  # región de entrada vacía: los clics pasan a la ventana de abajo
        try:
            win.get_surface().set_input_region(cairo.Region())
        except Exception:
            pass
    win.connect("realize", sin_clics)
    win.connect("map", sin_clics)

    def monitores_cambiaron(*_):  # enchufaron/desenchufaron: volver a ubicarla
        Capa.set_monitor(win, elegir_monitor())
        win.present()
    Gdk.Display.get_default().get_monitors().connect("items-changed", monitores_cambiaron)

    def terminar(etapa, detalle):
        ui["pct"] = 100.0
        ui["color"] = (0.45, 0.82, 0.50) if etapa == "fin" else (0.93, 0.38, 0.38)
        lbl_titulo.set_label(f"{ETAPAS[etapa]} · {titulo}")
        lbl_datos.set_label("")
        area.queue_draw()
        est.final(etapa, detalle)  # la única notificación: el resultado
        est.borrar()
        GLib.timeout_add_seconds(6, lambda: app_loop.quit() or False)

    ultimo = [None]

    def actualizar():
        pct, etapa, detalle, clase, falta = est.leer()
        if etapa in ("fin", "error"):
            terminar(etapa, detalle)
            return False
        icono, nombre = (ETAPAS.get(etapa, etapa) + " ").split(" ", 1)
        texto = detalle if detalle and len(detalle) <= 26 else (detalle[:25] + "…" if detalle else nombre.strip())
        partes = ([clase] if clase else []) + [f"{icono} {texto}", f"{pct:.0f}%"] + ([falta] if falta else [])
        estado = (round(pct, 1), " · ".join(partes))
        if estado != ultimo[0]:  # solo si cambió algo
            ui["pct"] = pct
            lbl_datos.set_label(estado[1])
            area.queue_draw()
            ultimo[0] = estado
        return True

    actualizar()
    GLib.timeout_add_seconds(1, actualizar)
    try:
        gi.require_version("GLibUnix", "2.0")
        from gi.repository import GLibUnix
        agregar_senal = GLibUnix.signal_add
    except (ImportError, ValueError):
        agregar_senal = GLib.unix_signal_add
    for sen in (2, 15):  # SIGINT / SIGTERM: cerrar prolijo
        agregar_senal(GLib.PRIORITY_DEFAULT, sen, lambda *_: app_loop.quit() or False)
    win.present()
    app_loop.run()
    win.destroy()
    try:  # el candado de este archivo ya no hace falta (los de "fila-N" se reusan)
        os.remove(os.path.join(os.environ.get("XDG_RUNTIME_DIR", "/tmp"), "progreso-barritas", candado))
    except OSError:
        pass
    return True


def seguir(archivo, titulo):
    if os.environ.get("PROGRESO_MODO", "barrita") != "notificacion":
        try:
            if seguir_barrita(archivo, titulo):
                return
        except Exception as e:  # sin GTK / sin layer-shell / sin Wayland: la notificación
            print(f"progreso: barrita no disponible ({e}); uso la notificación", file=sys.stderr)
    seguir_notificacion(archivo, titulo)


if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "seguir":
        # gtk4-layer-shell tiene que cargarse antes que libwayland/GTK; desde python la única
        # forma segura es LD_PRELOAD. Así que el propio script se re-lanza con la precarga.
        if (os.environ.get("PROGRESO_MODO") != "notificacion" and os.path.exists(LIB_CAPA)
                and LIB_CAPA not in os.environ.get("LD_PRELOAD", "")):
            entorno = dict(os.environ)
            entorno["LD_PRELOAD"] = ":".join(filter(None, [LIB_CAPA, entorno.get("LD_PRELOAD")]))
            try:
                os.execve(sys.executable, [sys.executable, os.path.abspath(__file__)] + sys.argv[1:], entorno)
            except OSError:
                pass  # sin re-lanzar: seguir() cae a la notificación si hace falta
        seguir(sys.argv[2], sys.argv[3])
    elif len(sys.argv) >= 4 and sys.argv[1] == "poner":
        reportar(sys.argv[2], sys.argv[3], " ".join(sys.argv[4:]))
    else:
        print(__doc__)
