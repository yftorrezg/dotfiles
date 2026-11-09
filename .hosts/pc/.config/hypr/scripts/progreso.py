#!/usr/bin/env python3
"""Barrita de progreso discreta en el monitor vertical (o una notificación de respaldo).

Los que trabajan (yt-dlp, auto-captura.py, cuadernillo.py) escriben su avance en un archivo;
este script lo lee y muestra una barrita fina, semitransparente, abajo a la derecha del
monitor vertical (HDMI-A-1). No toma el foco. Clic en la barrita: despliega la cola de cursos (y la reordenás); clic derecho:
la achica a un punto. Mismo flujo que el panel de trabajos (panel-trabajos.py):

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
    PROGRESO_MONITOR   conector del monitor (por defecto HDMI-A-1; si no está, el que haya)
Uso:
    progreso.py seguir <archivo> <título>     # muestra/actualiza la barrita hasta "fin"
    progreso.py poner <pct 0-100> <etapa> [detalle]   # desde bash (usa PROGRESO_ARCHIVO/RANGO)
"""
import os, re
import subprocess
import sys
import time

ETAPAS = {"descarga": "📥 Descargando", "capturas": "📸 Capturas", "apuntes": "🤖 Apuntes",
          "fin": "✅ Listo", "error": "❌ Falló"}
LIB_CAPA = "/usr/lib/libgtk4-layer-shell.so"  # tiene que cargarse ANTES que GTK (ver main)
MONITOR = os.environ.get("PROGRESO_MONITOR", "HDMI-A-1")  # el vertical
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
        if os.environ.get("PROGRESO_CURSO"):  # v10: la clase ocupa un tramo de la barra del CURSO entero (clase i de N → i/N…(i+1)/N)
            c0, c1 = (float(x) for x in os.environ["PROGRESO_CURSO"].split())
            total = c0 + total * (c1 - c0) / 100
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
        # Quien escribe el avance: PROGRESO_PID, o el número al final del nombre del archivo
        # ("curso-a-apuntes-progreso.<pid>"). Si sigue vivo, una etapa larga (Whisper, la IA) no es un cuelgue.
        try:
            self.dueno = int(os.environ.get("PROGRESO_PID") or archivo.rsplit(".", 1)[1])
        except (IndexError, ValueError):
            self.dueno = None

    def dueno_vivo(self):
        if not self.dueno:
            return None  # no se sabe
        try:
            os.kill(self.dueno, 0)
            return True
        except ProcessLookupError:
            return False
        except OSError:
            return True  # existe pero no es nuestro

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
        vivo = self.dueno_vivo()
        if etapa not in ("fin", "error") and vivo is False:
            return pct, "error", "El proceso terminó sin avisar el resultado", clase, ""
        quieto = time.time() - self.visto
        if quieto > SIN_NOVEDAD and vivo is not True:
            return pct, "error", "Sin novedades hace una hora: ¿se colgó?", clase, ""
        if quieto > 180 and vivo is True and etapa not in ("fin", "error"):
            # Honesto: el proceso vive pero esta etapa no reporta pasos; se dice cuánto lleva igual.
            aviso = f"sigue, {int(quieto // 60)} min sin cambios"
            detalle = f"{detalle} ({aviso})" if detalle else aviso
        por_curso = bool(re.match(r"^\d+/\d+$", clase or "")) and int(clase.split("/")[1]) > 1  # v10: la barra es del curso entero
        if (clase != self.clase_prev and not por_curso) or pct < self.pct_prev - 5:  # empezó otra clase (o curso): reiniciar el reloj
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
.pastilla.expandida { background-color: rgba(18, 18, 24, 0.94); }
.pastilla label.tenue { color: rgba(235, 235, 245, 0.62); font-size: 8pt; }
.pastilla label.arrastre { color: rgba(235, 235, 245, 0.45); font-size: 9pt; }
.cola-fila label { color: rgba(235, 235, 245, 0.90); font-size: 8pt; }
.cola-fila button {
    min-height: 0; min-width: 0; padding: 0 5px; margin: 0;
    font-size: 7.5pt; color: rgba(235, 235, 245, 0.90);
    background: rgba(255, 255, 255, 0.10); border: none; border-radius: 4px; box-shadow: none;
}
.cola-fila button:hover { background: rgba(255, 255, 255, 0.22); }
.cola-fila button:disabled { color: rgba(235, 235, 245, 0.25); }
.punto { background-color: rgba(18, 18, 24, 0.90); border-radius: 13px; padding: 3px 7px; }
.punto label { color: rgba(235, 235, 245, 0.90); font-size: 8pt; }
"""

CACHE = os.path.expanduser("~/.cache/auto-captura")
MODO_BARRITA = os.path.join(CACHE, "progreso-barrita.modo")  # último tamaño: compacto / expandido / punto
AQUI = os.path.dirname(os.path.abspath(__file__))


def cola_actual():
    """(carpeta, [(clave, nombre)]) de lo que espera en la cola de cursos (cola-capturas.sh)."""
    carpeta = os.environ.get("DIR_COLA") or CACHE
    try:
        filas = [f.split("\t") for f in open(os.path.join(carpeta, "cola.txt"), encoding="utf-8").read().splitlines() if f.strip()]
    except OSError:
        filas = []
    return carpeta, [(f[0], re.sub(r"^\W+\s*", "", f[4] if len(f) > 4 else f[0]) or f[0]) for f in filas]


def mover_en_cola(carpeta, clave, posicion):
    entorno = {k: v for k, v in os.environ.items() if k != "LD_PRELOAD"}
    entorno["DIR_COLA"] = carpeta
    subprocess.run(["bash", os.path.join(AQUI, "cola-capturas.sh"), "mover", clave, str(posicion)],
                   env=entorno, capture_output=True)


def leer_modo():
    try:
        m = open(MODO_BARRITA, encoding="utf-8").read().strip()
    except OSError:
        m = ""
    return m if m in ("compacto", "expandido", "punto") else "compacto"


def guardar_modo(m):
    try:
        os.makedirs(CACHE, exist_ok=True)
        with open(MODO_BARRITA, "w", encoding="utf-8") as f:
            f.write(m)
    except OSError:
        pass


def seguir_barrita(archivo, titulo):
    """Barrita layer-shell en el monitor vertical. Devuelve False si no se pudo mostrar
    (sin Wayland, sin layer-shell…) para caer a la notificación."""
    import gi
    gi.require_version("Gtk", "4.0")
    gi.require_version("Gtk4LayerShell", "1.0")
    gi.require_foreign("cairo")
    from gi.repository import GLib, GObject, Gtk, Gdk, Pango
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
        mons = Gdk.Display.get_default().get_monitors()
        for i in range(mons.get_n_items()):
            m = mons.get_item(i)
            if m.get_connector() == MONITOR:
                return m
        return None

    Capa.set_monitor(win, elegir_monitor())

    modo = {"m": leer_modo()}
    caja = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
    caja.add_css_class("pastilla")
    caja.set_size_request(ANCHO, -1)
    fila_txt = Gtk.Box(spacing=6)
    lbl_titulo = Gtk.Label(label=f"📚 {titulo}", xalign=0, hexpand=True)
    lbl_titulo.set_ellipsize(Pango.EllipsizeMode.END)  # el título se corta; los datos no
    lbl_titulo.set_max_width_chars(1)  # que no agrande la ventana: ocupa lo que sobre de ANCHO
    lbl_datos = Gtk.Label(label="", xalign=1)
    lbl_datos.add_css_class("datos")
    lbl_cola = Gtk.Label(label="", xalign=1)
    lbl_cola.add_css_class("tenue")
    flecha = Gtk.Label(label="▴")
    flecha.add_css_class("tenue")
    fila_txt.append(lbl_titulo)
    fila_txt.append(lbl_datos)
    fila_txt.append(lbl_cola)
    fila_txt.append(flecha)

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
    cabecera = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)  # clic aquí: despliega / pliega
    cabecera.append(fila_txt)
    cabecera.append(area)
    cab_cola = Gtk.Label(label="En cola (arrastrá ⠿ o usá ▲ ▼ ⤒)", xalign=0)
    cab_cola.add_css_class("tenue")
    lista = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
    sw = Gtk.ScrolledWindow(hscrollbar_policy=Gtk.PolicyType.NEVER, propagate_natural_height=True,
                            max_content_height=260)
    sw.set_child(lista)
    pie = Gtk.Label(label="clic: pliega · clic derecho: punto", xalign=1)
    pie.add_css_class("tenue")
    cola_panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
    cola_panel.append(cab_cola)
    cola_panel.append(sw)
    cola_panel.append(pie)
    caja.append(cabecera)
    caja.append(cola_panel)
    lbl_punto = Gtk.Label(label="")
    punto = Gtk.Box()
    punto.add_css_class("punto")
    punto.append(lbl_punto)
    raiz = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    raiz.append(caja)
    raiz.append(punto)
    win.set_child(raiz)

    cola = {"firma": None}

    def reordenar(carpeta, clave, posicion):
        mover_en_cola(carpeta, clave, posicion)
        GLib.idle_add(renderizar_cola, True)  # después del clic: el botón que lo pidió se destruye al redibujar

    def fila_cola(carpeta, clave, nombre, i, n):
        f = Gtk.Box(spacing=4)
        f.add_css_class("cola-fila")
        agarre = Gtk.Label(label="⠿")
        agarre.add_css_class("arrastre")
        agarre.set_tooltip_text("Arrastrá para cambiar el orden")
        num = Gtk.Label(label=f"{i + 1}.", xalign=1)
        num.add_css_class("tenue")
        nom = Gtk.Label(label=nombre, xalign=0, hexpand=True)
        nom.set_ellipsize(Pango.EllipsizeMode.END)
        nom.set_max_width_chars(1)
        f.append(agarre)
        f.append(num)
        f.append(nom)
        for txt, pos, tip, activo in (("⤒", 1, "Pasar al primero", i > 0),
                                      ("▲", i, "Subir", i > 0),
                                      ("▼", i + 2, "Bajar", i < n - 1)):
            b = Gtk.Button(label=txt)
            b.set_tooltip_text(tip)
            b.set_sensitive(activo)
            b.connect("clicked", lambda _b, p=pos: reordenar(carpeta, clave, p))
            f.append(b)
        arrastre = Gtk.DragSource()
        arrastre.set_actions(Gdk.DragAction.MOVE)
        arrastre.connect("prepare", lambda *_: Gdk.ContentProvider.new_for_value(GObject.Value(GObject.TYPE_STRING, clave)))
        agarre.add_controller(arrastre)
        destino = Gtk.DropTarget.new(GObject.TYPE_STRING, Gdk.DragAction.MOVE)
        destino.connect("drop", lambda _t, origen, *_: reordenar(carpeta, origen, i + 1) or True)
        f.add_controller(destino)
        return f

    def renderizar_cola(forzar=False):
        carpeta, pedidos = cola_actual()
        lbl_cola.set_label(f"⏳ {len(pedidos)}" if pedidos else "")
        firma = (carpeta, tuple(pedidos))
        if modo["m"] != "expandido" or (firma == cola["firma"] and not forzar):
            return False
        cola["firma"] = firma
        hijo = lista.get_first_child()
        while hijo:
            siguiente = hijo.get_next_sibling()
            lista.remove(hijo)
            hijo = siguiente
        if not pedidos:
            vacio = Gtk.Label(label="Nada esperando", xalign=0)
            vacio.add_css_class("tenue")
            lista.append(vacio)
        for i, (clave, nombre) in enumerate(pedidos):
            lista.append(fila_cola(carpeta, clave, nombre, i, len(pedidos)))
        return False

    def aplicar_modo():
        m = modo["m"]
        caja.set_visible(m != "punto")
        punto.set_visible(m == "punto")
        cola_panel.set_visible(m == "expandido")
        caja.set_css_classes(["pastilla", "expandida"] if m == "expandido" else ["pastilla"])
        flecha.set_label("▾" if m == "expandido" else "▴")
        guardar_modo(m)
        win.set_default_size(1, 1)  # que se ajuste al contenido (si no, queda del tamaño anterior)
        renderizar_cola(True)

    def clic(g, _n, _x, _y):  # izquierdo: despliega / pliega · derecho: punto · en el punto: vuelve
        m, b = modo["m"], g.get_current_button()
        if m == "punto":
            modo["m"] = "compacto"
        elif b == 3:
            modo["m"] = "punto"
        else:
            modo["m"] = "compacto" if m == "expandido" else "expandido"
        aplicar_modo()

    for widget in (cabecera, punto):
        gesto = Gtk.GestureClick()
        gesto.set_button(0)
        gesto.connect("pressed", clic)
        widget.add_controller(gesto)

    def monitores_cambiaron(*_):  # enchufaron/desenchufaron: volver a ubicarla
        Capa.set_monitor(win, elegir_monitor())
        win.present()
    Gdk.Display.get_default().get_monitors().connect("items-changed", monitores_cambiaron)

    def terminar(etapa, detalle):
        ui["pct"] = 100.0
        ui["color"] = (0.45, 0.82, 0.50) if etapa == "fin" else (0.93, 0.38, 0.38)
        lbl_titulo.set_label(f"{ETAPAS[etapa]} · {titulo}")
        lbl_datos.set_label("")
        lbl_punto.set_label("✅" if etapa == "fin" else "❌")
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
            lbl_punto.set_label(f"{pct:.0f}%")
            area.queue_draw()
            ultimo[0] = estado
        renderizar_cola()
        return True

    aplicar_modo()
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
