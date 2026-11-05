#!/usr/bin/env python3
"""MX Master 4: acción de un botón/gesto según el programa que tiene el foco.

Lo llama Solaar (~/.config/solaar/rules.yaml, generado por mx-reglas.py) con un evento
"<boton>-<dir>":
    boton: rueda  superior  gestos  atras  adelante        (+ "pulgar-izq" / "pulgar-der")
    dir:   click  arriba  abajo  izq  der

Por qué un script y no reglas de Solaar por app: la condición "Process" de Solaar no
funciona en Wayland/Hyprland. Aquí preguntamos a Hyprland cuál es la ventana activa
(hyprctl) y mandamos la tecla con ydotool.

Esquema (chuleta completa: SUPER+SHIFT+C → "MX Master 4"):
    GLOBALES (igual en todo el sistema): rueda = pantalla · superior = IAs
    DE LA APP (cambian según el programa): gestos = acciones · atras = navegar · adelante = pestañas/ver
El panel háptico NO pasa por aquí: abre el anillo radial (anillo.py, perfiles en anillo_apps.py).

Para cambiar algo: edita PERFILES. Cada botón es una lista de 5 acciones, en el orden
[click, arriba, abajo, izq, der]. None = hereda la acción del perfil "global". Una acción es:
    "ctrl+t"                       -> pulsa esa combinación
    ("click", "middle|back|forward") -> clic nativo del mouse (ydotool)
    ("cmd", ["prog", "arg"])       -> ejecuta un comando
    ("rueda-libre",)               -> alterna la rueda entre carraca y giro libre
Probar sin mover el mouse:  MX_CLASE=mpv python3 mx-accion.py gestos-arriba
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


# Abre (o enfoca) las dos IAs; la última (ChatGPT) queda con el foco.
GEMINI_Y_CHATGPT = ("cmd", ["bash", "-c", f"bash {APPWEB} gemini; sleep 0.4; bash {APPWEB} chatgpt"])


UDEMY = ("https://www.udemy.com/course/curso-de-raspberry-pi-3-model-b-con-python-iot-y-domotica-d/"
         "learn/lecture/22949520#overview")

PERFILES = {
    # Cualquier programa sin perfil propio (y lo que un perfil deje en None)
    "global": {
        #            click              arriba             abajo            izq                der
        "rueda":    ["super+shift+s",   "super+f",         "super+q",       "super+ctrl+left", "super+ctrl+right"],
        # captura al portapapeles · pantalla completa · cerrar ventana · escritorio anterior · siguiente
        "superior": ["esc",             GEMINI_Y_CHATGPT,  "super+alt+z",   web("claude"),     web("deepseek")],
        # Esc · Gemini + ChatGPT (las 2) · dictado (hyprwhspr) · Claude · DeepSeek
        "atras":    [ATRAS,             "home",            "end",           "alt+left",        "alt+right"],
        "adelante": [ADELANTE,          "ctrl+t",          "ctrl+w",        "ctrl+shift+tab",  "ctrl+tab"],
        "gestos":    ["playpause",       "volumeup",        "volumedown",    "prevsong",        "nextsong"],
        "pulgar":   ["volumedown", "volumeup"],
    },
    # Brave (ventana normal con pestañas)
    r"^brave-browser$": {
        "atras":    ["alt+left",        "ctrl+a",          "return",        "ctrl+c",          "ctrl+v"],
        # atrás · seleccionar todo · Enter · copiar · pegar
        "adelante": ["alt+right",       "ctrl+l",          "ctrl+d",        "f5",              "ctrl+f"],
        # adelante · barra de direcciones · añadir a marcadores · recargar · buscar en la página
        "gestos":    ["ctrl+shift+t",    "ctrl+t",          "ctrl+w",        "ctrl+shift+a",    ("cmd", ["brave", UDEMY])],
        # reabrir pestaña · nueva · cerrar · buscar pestaña · curso de estudio (Udemy)
        "pulgar":   ["ctrl+pageup", "ctrl+pagedown"],
    },
    # WhatsApp Web (ventana de app de Brave). Atajos oficiales de WhatsApp Web. (pendiente de revisar)
    r"^brave-web\.whatsapp\.com": {
        "atras":    ["esc",             "ctrl+alt+shift+[", "ctrl+alt+shift+]", "esc",        "ctrl+alt+slash"],
        # esc · chat anterior · chat siguiente · esc · buscar
        "adelante": ["ctrl+alt+n",      "ctrl+alt+shift+p", "ctrl+alt+shift+e", "ctrl+alt+shift+m", "ctrl+alt+shift+u"],
        # chat nuevo · fijar · archivar · silenciar · marcar no leído
        "gestos":    ["ctrl+alt+slash",  "ctrl+alt+p",      None,            None,              None],
        "pulgar":   ["ctrl+alt+shift+[", "ctrl+alt+shift+]"],
    },
    # mpv (cursos): usa tus atajos de ~/.config/mpv/input.conf
    r"^mpv$": {
        "atras":    [ATRAS,             "alt+right",       "alt+left",      "ctrl+left",       "ctrl+right"],
        # video anterior (MBTN_BACK) · +30 s · -30 s · -10 s · +10 s
        "adelante": [ADELANTE,          "e",               "w",             "d",               "a"],
        # video siguiente (MBTN_FORWARD) · velocidad 2x · 1.5x · +0.1 · -0.1
        "gestos":    ["space",           "b",               "n",             "tab",             "h"],
        # pausa/play · marca · ir a marca · lista de videos (uosc/items) · panel de notas
        "pulgar":   ["left", "right"],                       # -5 s / +5 s
    },
    # Gwenview (fotos): atajos propios en ~/.local/share/kxmlgui5/gwenview/gwenviewui.rc
    r"^org\.kde\.gwenview$": {
        "atras":    ["ctrl+z",          "t",               "ctrl+alt+n",    "ctrl+c",          "ctrl+alt+o"],
        # deshacer · miniaturas · abrir en nueva ventana · copiar · abrir carpeta contenedora
        "adelante": ["ctrl+s",          "s",               "m",             "f7",              "ctrl+alt+m"],
        # guardar · modo foco · reflejar · copiar a... · mover a...
        "gestos":    ["x",               "r",               "c",             "q",               "e"],
        # papelera · redimensionar · recortar · rotar izquierda · rotar derecha
        "pulgar":   ["a", "d"],                              # foto anterior / siguiente
    },
    # Dolphin (archivos). Ordenar: atajos propios en ~/.local/share/kxmlgui5/dolphin/dolphinui.rc
    r"^org\.kde\.dolphin$": {
        "atras":    ["alt+left",        "f6",              "alt+up",        "f2",              "ctrl+d"],
        # atrás · barra de direcciones · carpeta superior · renombrar · duplicar
        "adelante": ["alt+right",       "ctrl+t",          "ctrl+w",        "ctrl+pageup",     "ctrl+pagedown"],
        "gestos":    ["ctrl+shift+n",    "f3",              "alt+period",    "ctrl+alt+n",      "ctrl+alt+t"],
        # carpeta nueva · dividir vista · mostrar ocultos · ordenar por nombre · ordenar por tipo
        "pulgar":   ["ctrl+minus", "ctrl+equal"],            # iconos más chicos / más grandes
    },
    # VS Code (clase real com.microsoft.VSCode). Alt+← NO navega en Linux: es Ctrl+Alt+- / Ctrl+Shift+-
    r"^(com\.microsoft\.VSCode|code|Code|code-oss)$": {
        "gestos":   ["ctrl+grave",      "ctrl+shift+p",    "ctrl+p",        "ctrl+b",          "ctrl+backslash"],
        # terminal · paleta · abrir archivo · barra lateral · dividir editor
        "atras":    ["ctrl+alt+minus",  "f12",             "alt+f12",       "shift+f12",       "ctrl+shift+minus"],
        # atrás · definición · peek · referencias · adelante
        "adelante": ["f5",              "f9",              "f10",           "f11",             "shift+f11"],
        # continuar · breakpoint · step over · step into · step out
        "pulgar":   ["ctrl+pageup", "ctrl+pagedown"],
    },
    # Obsidian: el mouse se queda con la estructura de TABLAS (hotkeys.json en ~/Vídeos/.obsidian):
    # arriba/abajo = filas, izquierda/derecha = columnas. El texto, formato y navegación van en el anillo.
    r"^md\.obsidian\.Obsidian$": {
        "gestos":   ["ctrl+z",          "ctrl+alt+shift+up",        "ctrl+alt+shift+down",      "ctrl+alt+shift+left",  "ctrl+alt+shift+right"],
        # deshacer · fila encima · fila debajo · columna izquierda · columna derecha
        "atras":    [ATRAS,             "ctrl+alt+shift+pageup",    "ctrl+alt+shift+pagedown",  "ctrl+alt+shift+home",  "ctrl+alt+shift+end"],
        # atrás nativo · mover fila arriba · abajo · mover columna izquierda · derecha
        "adelante": [ADELANTE,          "ctrl+alt+shift+backspace", "ctrl+alt+shift+delete",    "ctrl+alt+shift+d",     "ctrl+alt+shift+c"],
        # adelante nativo · borrar fila · borrar columna · duplicar fila · duplicar columna
        "pulgar":   ["ctrl+shift+tab", "ctrl+tab"],
    },
    # kitty con fish: el panel de atrás es edición de línea; los atajos de fish 4 son los de fábrica
    r"^kitty:shell$": {
        "gestos":   ["ctrl+c",          "ctrl+r",          "ctrl+l",        "ctrl+u",          "alt+period"],
        # interrumpir · historial fzf · limpiar · borrar línea · último argumento
        "atras":    ["alt+left",        "ctrl+shift+c",    "ctrl+shift+v",  "ctrl+w",          "alt+s"],
        # cd atrás · copiar · pegar · borrar palabra · anteponer sudo
        "adelante": ["alt+right",       "ctrl+shift+t",    "ctrl+shift+q",  "ctrl+shift+left", "ctrl+shift+right"],
        # cd adelante · pestaña nueva · cerrar · anterior · siguiente
        "pulgar":   ["ctrl+shift+z", "ctrl+shift+x"],        # prompt anterior / siguiente (shell integration)
    },
    # Claude Code (TUI en pantalla completa). Superior-clic = Esc = interrumpir (global)
    r"^kitty:claude$": {
        "gestos":   ["shift+tab",       "ctrl+o",          "ctrl+b",        "alt+p",           "ctrl+t"],
        # modo (editar/plan) · transcript · a segundo plano · cambiar modelo · checklist de tareas
        "atras":    ["ctrl+v",          "ctrl+g",          "ctrl+shift+v",  "ctrl+u",          "ctrl+s"],
        # pegar imagen · editar prompt en editor · pegar texto · borrar línea · guardar borrador
        "adelante": ["ctrl+end",        "ctrl+home",       "ctrl+l",        ["esc", "esc"],    "ctrl+return"],
        # último mensaje · inicio · redibujar · rewind · enviar cola ya
        "pulgar":   ["pageup", "pagedown"],
    },
    r"^kitty:opencode$": {
        "gestos":   ["tab",             "ctrl+t",          "ctrl+p",        "f2",              "shift+tab"],
        # agente build/plan · variante de esfuerzo · paleta · modelo reciente · agente anterior
        "atras":    [["ctrl+x", "u"],   "ctrl+v",          "ctrl+shift+v",  "ctrl+u",          ["ctrl+x", "e"]],
        # deshacer · pegar imagen · pegar texto · borrar línea · editor externo
        "adelante": [["ctrl+x", "r"],   "ctrl+g",          "ctrl+alt+g",    ["ctrl+x", "b"],   ["ctrl+x", "g"]],
        # rehacer · primer mensaje · último mensaje · barra lateral · línea de tiempo
        "pulgar":   ["pageup", "pagedown"],
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


def ventana_activa():
    """(clase, título, pid) de la ventana con foco. MX_CLASE / MX_TITULO sirven para probar."""
    if os.environ.get("MX_CLASE"):
        return os.environ["MX_CLASE"], os.environ.get("MX_TITULO", ""), 0
    try:
        out = subprocess.run(["hyprctl", "activewindow", "-j"], capture_output=True,
                             text=True, timeout=2).stdout
        d = json.loads(out) if out.strip() else {}
        return d.get("class", ""), d.get("title", ""), d.get("pid", 0)
    except Exception:
        return "", "", 0


def clase_activa():
    return ventana_activa()[0]


def herramienta_kitty(pid):
    """Qué corre en primer plano dentro de una kitty: 'claude', 'opencode' o 'shell'.
    Recorre los procesos hijos en /proc (unos 3 ms); el título no sirve porque Claude cambia de glifo."""
    nombres = {"claude": "claude", "opencode": "opencode", ".opencode": "opencode"}
    try:
        hijos = {}
        for d in os.listdir("/proc"):
            if d.isdigit():
                try:
                    st = open(f"/proc/{d}/stat").read()
                    resto = st[st.rindex(")") + 2:].split()
                    hijos.setdefault(int(resto[1]), []).append((int(d), st[st.index("(") + 1:st.rindex(")")]))
                except OSError:
                    pass
        pila, vistos = [pid], set()
        while pila:
            p = pila.pop()
            for h, comm in hijos.get(p, []):
                if h not in vistos:
                    vistos.add(h)
                    if comm in nombres:
                        return nombres[comm]
                    pila.append(h)
    except Exception:
        pass
    return "shell"


def clase_efectiva(clase, pid):
    """kitty -> 'kitty:shell' | 'kitty:claude' | 'kitty:opencode' (el resto queda igual)."""
    if clase == "kitty" and pid:
        return f"kitty:{herramienta_kitty(pid)}"
    if clase == "kitty":
        return "kitty:shell"
    return clase


def pulsar(combo):
    partes = combo.split("+")
    mods = [K[p] for p in partes if p in MODS]
    resto = [K[p] for p in partes if p not in MODS]
    seq = [f"{c}:1" for c in mods + resto] + [f"{c}:0" for c in reversed(resto + mods)]
    # --key-delay 12 ms: algunas apps (Electron/Chromium) pierden teclas muy seguidas
    subprocess.run(["ydotool", "key", "--key-delay", "12", *seq], timeout=3,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


SIMBOLO = {"/": "slash", "-": "minus", ".": "period", " ": "space", ",": "comma", "=": "equal",
           "@": "shift+apostrophe", "!": "shift+1", "#": "backslash"}      # teclado gb extd


def combos_de_texto(texto):
    """'/clear' -> ['slash','c','l','e','a','r']. Solo minúsculas, dígitos y los símbolos de SIMBOLO."""
    sal = []
    for ch in texto:
        c = SIMBOLO.get(ch, ch)
        if all(p in K for p in c.split("+")):
            sal.append(c)
        else:
            log(f"texto: carácter no soportado {ch!r}")
    return sal


def pulsar_varias(combos, retardo=15):
    """Varias combinaciones en UN solo ydotool (escribir '/compact' tarda ~0,15 s en vez de ~0,6 s)."""
    seq = []
    for combo in combos:
        partes = combo.split("+")
        mods = [K[p] for p in partes if p in MODS]
        resto = [K[p] for p in partes if p not in MODS]
        seq += [f"{c}:1" for c in mods + resto] + [f"{c}:0" for c in reversed(resto + mods)]
    if seq:
        subprocess.run(["ydotool", "key", "--key-delay", str(retardo), *seq], timeout=10,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def escribir(texto, enter=True):
    """Escribe el texto y, si enter, pulsa Enter APARTE: pegado a las letras, Claude Code/opencode
    lo toman como parte de un pegado y meten un salto de línea en vez de enviar."""
    pulsar_varias(combos_de_texto(texto))
    if enter:
        time.sleep(0.1)
        pulsar("return")


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


def buscar(clase, boton, indice, titulo=""):
    """Devuelve (perfil, acción) del programa con foco; si no define esa acción, la del global.
    Una clave "clase@@titulo" solo vale si además el título coincide (p. ej. Google Docs dentro de Brave).
    Un perfil con celda None cae al siguiente perfil que coincida y, al final, al global."""
    for patron, tabla in PERFILES.items():
        if patron == "global":
            continue
        rc, _, rt = patron.partition("@@")
        if not re.search(rc, clase) or (rt and not re.search(rt, titulo)):
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
    clase, titulo, pid = ventana_activa()
    clase = clase_efectiva(clase, pid)
    perfil, accion = buscar(clase, boton, indice, titulo)
    log(f"{evento:16} clase={clase!r:36} perfil={perfil} accion={accion}")
    ejecutar(accion)
    return 0


def ejecutar(accion):
    """Ejecuta una acción del vocabulario de PERFILES (también la usa anillo.py)."""
    if isinstance(accion, list):                       # varias combinaciones seguidas
        if all(isinstance(a, str) for a in accion):
            pulsar_varias(accion, retardo=30)
        else:
            for a in accion:
                ejecutar(a)
                time.sleep(0.03)
    elif isinstance(accion, tuple) and accion[0] == "texto":
        escribir(accion[1], enter=accion[2] if len(accion) > 2 else True)
    elif isinstance(accion, tuple) and accion[0] == "cmd":
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
