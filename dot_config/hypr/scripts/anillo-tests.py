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
    nombres = set()
    for base in ("/usr/share/icons/Papirus", "/usr/share/icons/Adwaita"):
        for raiz, _, archivos in os.walk(base):
            for a in archivos:
                if a.endswith("-symbolic.svg"):
                    nombres.add(a[:-len("-symbolic.svg")])
    return nombres


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

if fallos:
    print("\n".join("✗ " + f for f in fallos))
    print(f"\n{len(fallos)} fallos")
    sys.exit(1)
print("✓ todo bien")
