#!/usr/bin/env python3
"""Tests del anillo radial (anillo.py + anillo_apps.py). Uso: python3 anillo-tests.py"""
import importlib.util
import math
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)


def cargar(nombre, archivo):
    spec = importlib.util.spec_from_file_location(nombre, os.path.join(AQUI, archivo))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


anillo = cargar("anillo", "anillo.py")
mx = cargar("mx_accion", "mx-accion.py")
import anillo_apps as apps  # noqa: E402

fallos = []


def ok(cond, msg):
    if not cond:
        fallos.append(msg)


def iconos_disponibles():
    import json
    with open(anillo.MAPA_ICONOS) as f:
        return set(json.load(f))


def teclas(accion):
    """Todas las combinaciones de teclas dentro de una acción."""
    if accion is None:
        return []
    if isinstance(accion, str):
        return [accion]
    if isinstance(accion, list):
        return [t for a in accion for t in teclas(a)]
    return []


# -- geometría --
for i in range(12):
    a = math.radians(i * 30)
    s, sub = anillo.seleccion(100 * math.sin(a), -100 * math.cos(a), apps.GLOBAL["sectores"], None)
    ok(s == i and sub is None, f"sector {i} por ángulo dio {s}")
ok(anillo.seleccion(5, 5, apps.GLOBAL["sectores"], None) == (None, None), "zona muerta")
# sub-opciones: sector 4 del global (Captura) tiene 4
angs = anillo.angulos_sub(4, 4)
for k, ang in enumerate(angs):
    r = math.radians(ang)
    s, sub = anillo.seleccion(240 * math.sin(r), -240 * math.cos(r), apps.GLOBAL["sectores"], 4)
    ok((s, sub) == (4, k), f"sub {k} de captura dio {(s, sub)}")

# -- perfiles --
iconos = iconos_disponibles()
for p in [apps.GLOBAL] + apps.PERFILES:
    n = p["nombre"]
    secs = p["sectores"]
    ok(p["logo"] in iconos, f"{n}: logo inexistente {p['logo']!r}")
    ok(len(secs) == 12, f"{n}: {len(secs)} sectores (deben ser 12)")
    ok(sum(1 for s in secs if s["sub"]) >= 4, f"{n}: menos de 4 sectores con sub-opciones")
    for s in secs:
        for e in [s] + s["sub"]:
            ok(e["icono"] in iconos, f"{n}: icono inexistente {e['icono']!r} ({e['nombre']})")
            ok(e["accion"] is not None, f"{n}: {e['nombre']} sin acción")
            for combo in teclas(e["accion"]) + [t for r in (e.get("rueda") or ()) for t in teclas(r)]:
                for parte in combo.split("+"):
                    ok(parte in mx.K, f"{n}: tecla desconocida {parte!r} en {combo!r} ({e['nombre']})")
        ok(len(s["sub"]) <= 6, f"{n}: {s['nombre']} tiene más de 6 sub-opciones")

ok(apps.perfil_para("brave-browser", "Mr Robot - YouTube - Brave")["nombre"] == "YouTube", "YouTube por título")
ok(apps.perfil_para("brave-browser", "Nueva pestaña - Brave")["nombre"] == "Brave", "Brave")
ok(apps.perfil_para("brave-www.youtube.com__-Default", "")["nombre"] == "YouTube", "YouTube app")
ok(apps.perfil_para("brave-web.whatsapp.com__-Default", "")["nombre"] == "WhatsApp", "WhatsApp")
ok(apps.perfil_para("org.telegram.desktop", "")["nombre"] == "Telegram", "Telegram")
ok(apps.perfil_para("loquesea", "")["nombre"] == "Sistema", "global")


# -- anti-rebote del panel: ráfaga pulsar/soltar/pulsar/soltar = UN solo pulsar y UN solo soltar --
class GLibFalso:
    def __init__(self):
        self.timers, self.n = {}, 0

    def timeout_add(self, ms, f):
        self.n += 1
        self.timers[self.n] = f
        return self.n

    def source_remove(self, i):
        self.timers.pop(i, None)

    def disparar(self):
        for i, f in list(self.timers.items()):
            self.timers.pop(i, None)
            f()


def paquete(m, pulsado):
    d = bytearray(20)
    d[0], d[2], d[3] = 0x11, m.f_rep, 0x00
    if pulsado:
        d[4], d[5] = anillo.CID_HAPTICO >> 8, anillo.CID_HAPTICO & 0xFF
    return bytes(d)


eventos = []
m = object.__new__(anillo.Mouse)
m.GLib = GLibFalso()
m.al_pulsar, m.al_soltar = (lambda: eventos.append("P")), (lambda: eventos.append("S"))
m.f_rep, m.f_wds, m.pulsado, m.timer_soltar = 13, 14, False, None
for estado in (True, False, True, False, True, False, True):   # rebote del sensor
    m._procesar(paquete(m, estado))
ok(eventos == ["P"], f"rebote: antes de soltar de verdad solo debe haber un P, hubo {eventos}")
m._procesar(paquete(m, False))
m.GLib.disparar()
ok(eventos == ["P", "S"], f"rebote: tras soltar debe quedar P,S, quedó {eventos}")
m._procesar(paquete(m, True))
ok(eventos == ["P", "S", "P"], "un toque nuevo después sí vale")

if fallos:
    print("\n".join("✗ " + f for f in fallos))
    print(f"\n{len(fallos)} fallos")
    sys.exit(1)
print("✓ todo bien")
