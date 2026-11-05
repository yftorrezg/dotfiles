#!/usr/bin/env python3
"""MX Master 4: acción de un botón/gesto según el programa que tiene el foco.

Lo llama Solaar (~/.config/solaar/rules.yaml, generado por mx-reglas.py) con un evento
"<boton>-<dir>":
    boton: rueda  superior  gestos  atras  adelante  haptico        (+ "pulgar-izq" / "pulgar-der")
    dir:   click  arriba  abajo  izq  der

Por qué un script y no reglas de Solaar por app: la condición "Process" de Solaar no
funciona en Wayland/Hyprland. Aquí preguntamos a Hyprland cuál es la ventana activa
(hyprctl) y mandamos la tecla con ydotool.

Esquema (chuleta completa: SUPER+SHIFT+C → "MX Master 4"):
    GLOBALES (igual en todo el sistema): rueda = pantalla · superior = ventanas · gestos = lanzadores
    DE LA APP (cambian según el programa): atras = navegar · adelante = pestañas/ver · haptico = acciones

Para cambiar algo: edita PERFILES. Cada botón es una lista de 5 acciones, en el orden
[click, arriba, abajo, izq, der]. None = hereda la acción del perfil "global". Una acción es:
    "ctrl+t"                       -> pulsa esa combinación
    ("click", "middle|back|forward") -> clic nativo del mouse (ydotool)
    ("cmd", ["prog", "arg"])       -> ejecuta un comando
    ("rueda-libre",)               -> alterna la rueda entre carraca y giro libre
Probar sin mover el mouse:  MX_CLASE=mpv python3 mx-accion.py haptico-arriba
"""
import json
import os
import re
import subprocess
import sys
import time

LOG = os.path.expanduser("~/.local/state/mx-accion.log")
os.environ.setdefault("YDOTOOL_SOCKET", f"/run/user/{os.getuid()}/.ydotool_socket")

DIRS = ["click", "arriba", "abajo", "izq", "der"]
ATRAS = ("click", "back")
ADELANTE = ("click", "forward")

# ---- Perfiles ---------------------------------------------------------------
APPWEB = os.path.expanduser("~/.config/hypr/scripts/app-web.sh")


def web(sitio):
    """Enfoca o abre una app web de Brave (gemini, chatgpt, claude, deepseek, youtube...)."""
    return ("cmd", ["bash", APPWEB, sitio])


UDEMY = ("https://www.udemy.com/course/curso-de-raspberry-pi-3-model-b-con-python-iot-y-domotica-d/"
         "learn/lecture/22949520#overview")

PERFILES = {
    # Cualquier programa sin perfil propio (y lo que un perfil deje en None)
    "global": {
        #            click              arriba             abajo            izq                der
        "rueda":    ["super+shift+s",   "super+f",         "super+q",       "super+ctrl+left", "super+ctrl+right"],
        # captura al portapapeles · pantalla completa · cerrar ventana · escritorio anterior · siguiente
        "superior": ["esc",             web("gemini"),     web("chatgpt"),  web("claude"),     web("deepseek")],
        "gestos":   ["super+v",         web("youtube"),    "super+return",  "super+e",         "super+alt+w"],
        # portapapeles · YouTube · terminal · archivos · WhatsApp
        "atras":    [ATRAS,             "home",            "end",           "alt+left",        "alt+right"],
        "adelante": [ADELANTE,          "ctrl+t",          "ctrl+w",        "ctrl+shift+tab",  "ctrl+tab"],
        "haptico":  ["playpause",       "volumeup",        "volumedown",    "prevsong",        "nextsong"],
        "pulgar":   ["volumedown", "volumeup"],
    },
    # Brave (ventana normal con pestañas)
    r"^brave-browser$": {
        "atras":    ["alt+left",        "ctrl+a",          "return",        "ctrl+c",          "ctrl+v"],
        # atrás · seleccionar todo · Enter · copiar · pegar
        "adelante": ["alt+right",       "ctrl+l",          "ctrl+d",        "f5",              "ctrl+f"],
        # adelante · barra de direcciones · añadir a marcadores · recargar · buscar en la página
        "haptico":  ["ctrl+shift+t",    "ctrl+t",          "ctrl+w",        "ctrl+shift+a",    ("cmd", ["brave", UDEMY])],
        # reabrir pestaña · nueva · cerrar · buscar pestaña · curso de estudio (Udemy)
        "pulgar":   ["ctrl+pageup", "ctrl+pagedown"],
    },
    # WhatsApp Web (ventana de app de Brave). Atajos oficiales de WhatsApp Web. (pendiente de revisar)
    r"^brave-web\.whatsapp\.com": {
        "atras":    ["esc",             "ctrl+alt+shift+[", "ctrl+alt+shift+]", "esc",        "ctrl+alt+slash"],
        # esc · chat anterior · chat siguiente · esc · buscar
        "adelante": ["ctrl+alt+n",      "ctrl+alt+shift+p", "ctrl+alt+e",   "ctrl+alt+shift+m", "ctrl+alt+shift+u"],
        # chat nuevo · fijar · archivar · silenciar · marcar no leído
        "haptico":  ["ctrl+alt+slash",  "ctrl+alt+p",      None,            None,              None],
        "pulgar":   ["ctrl+alt+shift+[", "ctrl+alt+shift+]"],
    },
    # mpv (cursos): usa tus atajos de ~/.config/mpv/input.conf
    r"^mpv$": {
        "atras":    [ATRAS,             "alt+right",       "alt+left",      "ctrl+left",       "ctrl+right"],
        # video anterior (MBTN_BACK) · +30 s · -30 s · -10 s · +10 s
        "adelante": [ADELANTE,          "e",               "w",             "d",               "a"],
        # video siguiente (MBTN_FORWARD) · velocidad 2x · 1.5x · +0.1 · -0.1
        "haptico":  ["space",           "b",               "n",             "tab",             "h"],
        # pausa/play · marca · ir a marca · lista de videos (uosc/items) · panel de notas
        "pulgar":   ["left", "right"],                       # -5 s / +5 s
    },
    # Gwenview (fotos): atajos propios en ~/.local/share/kxmlgui5/gwenview/gwenviewui.rc
    r"^org\.kde\.gwenview$": {
        "atras":    ["ctrl+z",          "t",               "ctrl+alt+n",    "ctrl+c",          "ctrl+alt+o"],
        # deshacer · miniaturas · abrir en nueva ventana · copiar · abrir carpeta contenedora
        "adelante": ["ctrl+s",          "s",               "m",             "f7",              "ctrl+alt+m"],
        # guardar · modo foco · reflejar · copiar a... · mover a...
        "haptico":  ["x",               "r",               "c",             "q",               "e"],
        # papelera · redimensionar · recortar · rotar izquierda · rotar derecha
        "pulgar":   ["a", "d"],                              # foto anterior / siguiente
    },
    # Dolphin (archivos). Ordenar: atajos propios en ~/.config/dolphinrc [Shortcuts]
    r"^org\.kde\.dolphin$": {
        "atras":    ["alt+left",        "f6",              "alt+up",        "f2",              "ctrl+d"],
        # atrás · barra de direcciones · carpeta superior · renombrar · duplicar
        "adelante": ["alt+right",       "ctrl+t",          "ctrl+w",        "ctrl+shift+tab",  "ctrl+tab"],
        "haptico":  ["ctrl+shift+n",    "f3",              "alt+period",    "ctrl+alt+n",      "ctrl+alt+t"],
        # carpeta nueva · dividir vista · mostrar ocultos · ordenar por nombre · ordenar por tipo
        "pulgar":   ["ctrl+minus", "ctrl+equal"],            # iconos más chicos / más grandes
    },
}

# ---- Teclas (códigos evdev) -------------------------------------------------
K = {
    "ctrl": 29, "shift": 42, "alt": 56, "super": 125,
    "esc": 1, "tab": 15, "return": 28, "space": 57, "backspace": 14,
    "home": 102, "end": 107, "pageup": 104, "pagedown": 109,
    "up": 103, "down": 108, "left": 105, "right": 106,
    "[": 26, "]": 27, "slash": 53, "minus": 12, "equal": 13, "period": 52,
    "volumedown": 114, "volumeup": 115, "playpause": 164, "prevsong": 165, "nextsong": 163,
}
for i, c in enumerate("qwertyuiop"):
    K[c] = 16 + i
for i, c in enumerate("asdfghjkl"):
    K[c] = 30 + i
for i, c in enumerate("zxcvbnm"):
    K[c] = 44 + i
for i in range(1, 11):
    K[f"f{i}"] = 58 + i
K["f11"], K["f12"] = 87, 88
for i, c in enumerate("1234567890"):
    K[c] = 2 + i
K.update({"comma": 51, "semicolon": 39, "apostrophe": 40, "grave": 41, "backslash": 43,
          "delete": 111, "insert": 110, "print": 99, "menu": 127})
MODS = {"ctrl", "shift", "alt", "super"}

# Clics nativos de ydotool: 0xC0 = pulsar y soltar. 0x02 medio · 0x03 lateral (atrás) · 0x04 extra (adelante)
CLICS = {"middle": "0xC2", "back": "0xC3", "forward": "0xC4"}

# Eventos de rueda: evitar ráfagas (el pulgar manda varios eventos por muesca)
ESPERA_S = {"pulgar-izq": 0.12, "pulgar-der": 0.12}


def log(msg):
    try:
        os.makedirs(os.path.dirname(LOG), exist_ok=True)
        with open(LOG, "a") as f:
            f.write(time.strftime("%H:%M:%S ") + msg + "\n")
        if os.path.getsize(LOG) > 200_000:
            os.replace(LOG, LOG + ".old")
    except OSError:
        pass


def clase_activa():
    if os.environ.get("MX_CLASE"):
        return os.environ["MX_CLASE"]
    try:
        out = subprocess.run(["hyprctl", "activewindow", "-j"], capture_output=True,
                             text=True, timeout=2).stdout
        return json.loads(out).get("class", "") if out.strip() else ""
    except Exception:
        return ""


def pulsar(combo):
    partes = combo.split("+")
    mods = [K[p] for p in partes if p in MODS]
    resto = [K[p] for p in partes if p not in MODS]
    seq = [f"{c}:1" for c in mods + resto] + [f"{c}:0" for c in reversed(resto + mods)]
    # --key-delay 12 ms: algunas apps (Electron/Chromium) pierden teclas muy seguidas
    subprocess.run(["ydotool", "key", "--key-delay", "12", *seq], timeout=3,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def alternar_rueda():
    """Carraca <-> giro libre (lo que hacía el botón SmartShift antes de desviarlo)."""
    cmd = ["solaar", "config", "MX Master 4", "scroll-ratchet"]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=10).stdout
        actual = out.strip().splitlines()[-1].split("=")[-1].strip()
        nuevo = "Giro libre" if actual == "Carraca" else "Carraca"
        subprocess.run([*cmd, nuevo], capture_output=True, timeout=10)
        subprocess.run(["notify-send", "-t", "1200", "-a", "MX Master 4", f"Rueda: {nuevo}"],
                       timeout=3, capture_output=True)
    except Exception as e:
        log(f"alternar_rueda falló: {e}")


def limitar(evento):
    espera = ESPERA_S.get(evento)
    if not espera:
        return True
    marca = f"/tmp/mx-accion-{os.getuid()}-{evento}"
    try:
        if time.time() - os.path.getmtime(marca) < espera:
            return False
    except OSError:
        pass
    open(marca, "w").close()
    return True


def buscar(clase, boton, indice):
    """Devuelve (perfil, acción) del programa con foco; si no define esa acción, la del global."""
    for patron, tabla in PERFILES.items():
        if patron == "global" or not re.search(patron, clase):
            continue
        fila = tabla.get(boton)
        if fila and indice < len(fila) and fila[indice] is not None:
            return patron, fila[indice]
    return "global", PERFILES["global"][boton][indice]


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    evento = sys.argv[1]
    if not limitar(evento):
        return 0
    if evento in ("pulgar-izq", "pulgar-der"):
        boton, indice = "pulgar", 0 if evento == "pulgar-izq" else 1
    else:
        boton, _, direccion = evento.partition("-")
        if boton not in PERFILES["global"] or direccion not in DIRS:
            print(f"evento desconocido: {evento}", file=sys.stderr)
            return 2
        indice = DIRS.index(direccion)
    clase = clase_activa()
    perfil, accion = buscar(clase, boton, indice)
    log(f"{evento:16} clase={clase!r:36} perfil={perfil} accion={accion}")
    ejecutar(accion)
    return 0


def ejecutar(accion):
    """Ejecuta una acción del vocabulario de PERFILES (también la usa anillo.py)."""
    if isinstance(accion, tuple) and accion[0] == "cmd":
        subprocess.Popen(accion[1], start_new_session=True,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    elif isinstance(accion, tuple) and accion[0] == "rueda-libre":
        alternar_rueda()
    elif isinstance(accion, tuple) and accion[0] == "click":
        subprocess.run(["ydotool", "click", CLICS[accion[1]]], timeout=3,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        pulsar(accion)


if __name__ == "__main__":
    sys.exit(main())
