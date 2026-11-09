#!/usr/bin/env python3
"""Panel de trabajos de fondo (apuntes, rearmado, mapas…) abajo a la derecha del monitor vertical.

Tres tamaños, cambian con el mouse:
  • compacto   (al abrir): una línea "⚙️ 3 trabajos · 41 % · ~5 h" con su barrita.
  • expandido  (clic izquierdo en el compacto): una fila y una barra por trabajo, con avance y tiempo restante.
  • punto      (clic derecho, para cuando estudias): un círculo chiquito con el %; clic → compacto.
Se cierra solo un minuto después de que termine todo. Recuerda el último tamaño.

    panel-trabajos.py            # abre (si ya está abierto, no abre otro)
    panel-trabajos.py --ver      # lo mismo en la terminal, una vez

Trabajos: TRABAJOS (abajo). Cada uno dice de dónde sacar "hechas/total" (una función o el último "N/M" de un log).
"""
import glob, json, os, re, subprocess, sys, threading, time

CACHE = os.path.expanduser("~/.cache/auto-captura")
ESTADO = os.path.join(CACHE, "panel-trabajos.estado")
MONITOR = os.environ.get("PROGRESO_MONITOR", "HDMI-A-1")
LIB_CAPA = "/usr/lib/libgtk4-layer-shell.so"
ANCHO = 430
AQUI = os.path.dirname(os.path.abspath(__file__))


def _vivo(patron):
    return subprocess.run(["pgrep", "-f", patron], capture_output=True).returncode == 0


def _ultimo_nm(*logs):
    """(hechas, total) del último "N/M" de los logs (rearmar/migrar escriben "2200/3453 …"), o None."""
    for log in logs:
        try:
            with open(log, "rb") as f:
                f.seek(0, 2)
                f.seek(max(0, f.tell() - 4000))
                txt = f.read().decode("utf-8", "replace")
        except OSError:
            continue
        if re.search(r"^FIN\b|'cambiadas'|##### FIN", txt, re.M):
            m = re.findall(r"(\d+) clases (?:encontradas|por migrar)", open(log, encoding="utf-8", errors="replace").read(2000))
            n = int(m[0]) if m else 1
            return n, n
        m = re.findall(r"^(\d+)/(\d+)", txt, re.M)
        if m:
            return int(m[-1][0]), int(m[-1][1])
    return None


def t_apuntes():
    sys.path.insert(0, AQUI)
    import importlib.util
    sp = importlib.util.spec_from_file_location("rp", os.path.join(AQUI, "regeneracion-progreso.py"))
    rp = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(rp)
    h, t, pc = rp.contar()
    actual = ""  # el curso en el que trabajan las colas ahora (el del log más reciente)
    logs = sorted(glob.glob(os.path.join(CACHE, "regenerar-[A-Z].log")), key=os.path.getmtime)
    if logs:
        m = re.findall(r"^##### CURSO: (.+?) \(", open(logs[-1], encoding="utf-8", errors="replace").read(), re.M)
        actual = os.path.basename(m[-1]) if m else ""
    return h, t, actual[:34]


def t_log(*logs):
    def f():
        r = _ultimo_nm(*[os.path.join(CACHE, l) for l in logs])
        return (r[0], r[1], "") if r else None
    return f


def t_mapas():
    listas = [os.path.join(CACHE, x) for x in ("mapas-udemy.txt", "mapas-hack4u.txt")]
    cursos = [l.strip() for x in listas if os.path.exists(x) for l in open(x, encoding="utf-8") if l.strip()]
    hechos = sum(os.path.exists(os.path.join(c, "MAPA.md")) and not _mapa_a_medias(c) for c in cursos)
    actual = ""
    for log in sorted(glob.glob(os.path.join(CACHE, "mapas-*.log")), key=os.path.getmtime)[-1:]:
        m = re.findall(r"^=== (.+?):", open(log, encoding="utf-8", errors="replace").read()[-3000:], re.M)
        actual = m[-1][:34] if m else ""
    return hechos, len(cursos), actual


def _mapa_a_medias(curso):
    try:
        return "Sin mapa todavía" in open(os.path.join(curso, "MAPA.md"), encoding="utf-8").read()
    except OSError:
        return True


TRABAJOS = [  # (clave, nombre, cómo contar, patrón del proceso que lo hace: si no corre y no terminó → ⏸)
    ("apuntes", "📝 Apuntes por clase (IA)", t_apuntes, "regenerar-cola"),
    ("mapas", "🗺️ Mapas por módulo (IA)", t_mapas, "mapas-cola.sh|mapa-curso.py"),
    ("rearmar", "♻️ Rearmar apuntes (gratis)", t_log("rearmar-curso.log"), "rearmar-curso.py"),
]


class Medidor:
    """Lee cada trabajo en un hilo (contar en el disco externo tarda) y calcula el ritmo y lo que falta."""

    def __init__(self):
        self.datos, self.hist, self.lock = {}, {}, threading.Lock()

    def medir(self, avisar=None):
        # los rápidos primero (leen un log) y los apuntes al final (recorrer el disco externo tarda ~40 s)
        for clave, nombre, contar, patron in sorted(TRABAJOS, key=lambda x: x[0] == "apuntes"):
            try:
                r = contar()
            except Exception:
                r = None
            if not r or not r[1]:
                continue
            h, t, actual = r
            ahora = time.time()
            hs = self.hist.setdefault(clave, [])
            hs.append((ahora, h))
            hs[:] = [x for x in hs if ahora - x[0] <= 1800]
            falta = ""
            if h < t and len(hs) > 1 and hs[-1][1] > hs[0][1] and ahora - hs[0][0] >= 90:
                seg = (t - h) * (ahora - hs[0][0]) / (hs[-1][1] - hs[0][1])
                falta = f"~{int(seg // 3600)} h {int(seg % 3600 // 60):02d}" if seg >= 3600 else f"~{max(1, int(seg // 60))} min"
            vivo = _vivo(patron)
            with self.lock:
                self.datos[clave] = dict(nombre=nombre, h=h, t=t, actual=actual, falta=falta, vivo=vivo,
                                         listo=h >= t)
            if avisar:
                avisar()

    def foto(self):
        with self.lock:
            return [self.datos[c] for c, *_ in TRABAJOS if c in self.datos]


def resumen(trabajos):
    """(activos, principal): el principal es el trabajo que más tarda en terminar (los demás corren en paralelo y
    terminan antes); sin estimación todavía, el primero de la lista (los apuntes con IA)."""
    activos = [x for x in trabajos if not x["listo"]]
    if not activos:
        return activos, None
    return activos, max(activos, key=lambda x: (_a_seg(x["falta"]) if x["falta"] else -1, -activos.index(x)))


def _a_seg(f):
    m = re.match(r"~(?:(\d+) h )?(\d+)", f)
    if not m:
        return 0
    return int(m.group(1) or 0) * 3600 + int(m.group(2)) * (60 if " h " in f or "min" in f else 1)


def ver():
    m = Medidor()
    m.medir()
    for x in m.foto():
        estado = "✅" if x["listo"] else ("▶" if x["vivo"] else "⏸")
        print(f"{estado} {x['nombre']:34} {x['h']:6}/{x['t']:<6} {100 * x['h'] / x['t']:5.1f} %  {x['actual']}")


CSS = b"""
window.panel { background: transparent; }
.pastilla { background-color: rgba(18, 18, 24, 0.96); border-radius: 8px; padding: 4px 10px 5px 10px; }
.pastilla label { color: rgba(235, 235, 245, 0.90); font-size: 8.5pt; }
.pastilla label.tenue { color: rgba(235, 235, 245, 0.62); font-size: 8pt; }
.punto { background-color: rgba(18, 18, 24, 0.90); border-radius: 13px; padding: 3px 7px; }
.punto label { color: rgba(235, 235, 245, 0.90); font-size: 8pt; }
"""


def panel():
    import gi
    gi.require_version("Gtk", "4.0")
    gi.require_version("Gtk4LayerShell", "1.0")
    from gi.repository import GLib, Gtk, Gdk, Pango
    from gi.repository import Gtk4LayerShell as Capa
    import fcntl
    if not Gtk.init_check() or not Capa.is_supported():
        print("sin layer-shell: usa --ver", file=sys.stderr)
        return 1
    candado = open(os.path.join(os.environ.get("XDG_RUNTIME_DIR", "/tmp"), "panel-trabajos.lock"), "w")
    try:
        fcntl.flock(candado, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        return 0  # ya hay uno abierto
    prov = Gtk.CssProvider()
    prov.load_from_data(CSS, len(CSS))
    Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), prov, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
    try:
        modo = {"m": open(ESTADO).read().strip() or "compacto"}
    except OSError:
        modo = {"m": "compacto"}

    win = Gtk.Window(title="Trabajos de fondo")
    win.add_css_class("panel")
    Capa.init_for_window(win)
    Capa.set_namespace(win, "panel-trabajos")
    Capa.set_layer(win, Capa.Layer.OVERLAY)
    Capa.set_keyboard_mode(win, Capa.KeyboardMode.NONE)
    Capa.set_exclusive_zone(win, 0)
    Capa.set_anchor(win, Capa.Edge.BOTTOM, True)
    Capa.set_anchor(win, Capa.Edge.RIGHT, True)
    Capa.set_margin(win, Capa.Edge.RIGHT, 20)
    Capa.set_margin(win, Capa.Edge.BOTTOM, 44)  # encima de la barrita de los atajos (fila 0)
    mons = Gdk.Display.get_default().get_monitors()
    for i in range(mons.get_n_items()):
        if mons.get_item(i).get_connector() == MONITOR:
            Capa.set_monitor(win, mons.get_item(i))

    def barra(pct_ref, color=(0.49, 0.64, 0.97), alto=3):
        def dibujar(_a, cr, w, h):
            r = h / 2

            def pildora(x):
                cr.new_sub_path()
                cr.arc(r, r, r, 1.5708, 4.7124)
                cr.arc(max(r, x - r), r, r, 4.7124, 1.5708)
                cr.close_path()
            cr.set_source_rgba(1, 1, 1, 0.18)
            pildora(w)
            cr.fill()
            p = max(0.0, min(100.0, pct_ref()))
            if p > 0:
                cr.set_source_rgba(*color, 0.95)
                pildora(max(w * p / 100, h))
                cr.fill()
        a = Gtk.DrawingArea()
        a.set_content_height(alto)
        a.set_draw_func(dibujar)
        return a

    med = Medidor()
    foto = {"t": [], "pct": 0.0}

    def construir():
        """Rehace el contenido según el modo (son pocos widgets: más simple que mantenerlos)."""
        tr = foto["t"]
        activos, princ = resumen(tr)
        pct = 100 * princ["h"] / princ["t"] if princ else 100.0
        foto["pct"] = pct
        if modo["m"] == "punto":
            caja = Gtk.Box()
            caja.add_css_class("punto")
            caja.append(Gtk.Label(label=f"⚙️ {pct:.0f}%" if activos else "✅"))
            return caja
        caja = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
        caja.add_css_class("pastilla")
        caja.set_size_request(ANCHO, -1)
        cab = Gtk.Box(spacing=6)
        corto = re.sub(r"^\W+\s*", "", princ["nombre"]).split(" (")[0] if princ else ""  # "📝 Apuntes por clase (IA)" → "Apuntes por clase"
        titulo = (f"⚙️ {corto} {pct:.0f} %"
                  + (f" · falta {princ['falta']}" if princ["falta"] else "")
                  + (f" · +{len(activos) - 1} más" if len(activos) > 1 else "")) if activos else "✅ Todo terminado"
        if not tr:
            titulo = "⚙️ Midiendo…"
        lt = Gtk.Label(label=titulo, xalign=0, hexpand=True)
        flecha = Gtk.Label(label="▾" if modo["m"] == "expandido" else "▴")
        flecha.add_css_class("tenue")
        cab.append(lt)
        cab.append(flecha)
        caja.append(cab)
        caja.append(barra(lambda: foto["pct"], (0.45, 0.82, 0.50) if not activos and tr else (0.49, 0.64, 0.97)))
        if modo["m"] == "expandido":
            for x in tr:
                p = 100 * x["h"] / x["t"]
                estado = "✅" if x["listo"] else ("▶" if x["vivo"] else "⏸ pausado")
                f = Gtk.Box(spacing=6)
                n = Gtk.Label(label=f"{x['nombre']}", xalign=0, hexpand=True)
                n.set_ellipsize(Pango.EllipsizeMode.END)
                n.set_max_width_chars(1)
                d = Gtk.Label(label=f"{x['h']:,}/{x['t']:,} · {p:.0f} %".replace(",", ".") + (f" · {x['falta']}" if x["falta"] and not x["listo"] else ""))
                d.add_css_class("tenue")
                f.append(n)
                f.append(d)
                caja.append(f)
                caja.append(barra(lambda p=p: p, (0.45, 0.82, 0.50) if x["listo"] else (0.95, 0.75, 0.35) if not x["vivo"] else (0.49, 0.64, 0.97), 2))
                if x["actual"] and not x["listo"]:
                    a = Gtk.Label(label=f"   {estado} {x['actual']}", xalign=0)
                    a.add_css_class("tenue")
                    a.set_ellipsize(Pango.EllipsizeMode.END)
                    a.set_max_width_chars(1)
                    caja.append(a)
            pie = Gtk.Label(label="clic: achicar · clic derecho: punto", xalign=1)
            pie.add_css_class("tenue")
            caja.append(pie)
        return caja

    def pintar():
        win.set_child(construir())
        win.set_default_size(1, 1)  # que la ventana se ajuste al contenido nuevo (si no, el punto queda de 430 px)
        win.queue_resize()
        return False

    def clic(g, _n, _x, _y):
        b = g.get_current_button()
        modo["m"] = ("punto" if b == 3 else
                     "compacto" if modo["m"] in ("punto", "expandido") else "expandido")
        try:
            open(ESTADO, "w").write(modo["m"])
        except OSError:
            pass
        pintar()

    g = Gtk.GestureClick()
    g.set_button(0)
    g.connect("pressed", clic)
    win.add_controller(g)

    fin = {"desde": None}
    bucle = GLib.MainLoop()

    def hilo():
        while True:
            def avisar():
                foto["t"] = med.foto()
                GLib.idle_add(pintar)
            med.medir(avisar)
            activos = [x for x in foto["t"] if not x["listo"] and x["vivo"]]
            if foto["t"] and not activos:
                fin["desde"] = fin["desde"] or time.time()
                if time.time() - fin["desde"] > 60:
                    GLib.idle_add(bucle.quit)
                    return
            else:
                fin["desde"] = None
            time.sleep(20)

    pintar()
    win.present()
    threading.Thread(target=hilo, daemon=True).start()
    bucle.run()
    return 0


if __name__ == "__main__":
    if "--ver" in sys.argv:
        ver()
        sys.exit(0)
    # gtk4-layer-shell tiene que cargarse antes que libwayland: se relanza con LD_PRELOAD (igual que progreso.py)
    if os.path.exists(LIB_CAPA) and LIB_CAPA not in os.environ.get("LD_PRELOAD", ""):
        env = dict(os.environ, LD_PRELOAD=":".join(filter(None, [LIB_CAPA, os.environ.get("LD_PRELOAD")])))
        os.execve(sys.executable, [sys.executable, os.path.abspath(__file__)] + sys.argv[1:], env)
    sys.exit(panel())
