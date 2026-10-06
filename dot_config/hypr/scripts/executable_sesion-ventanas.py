#!/usr/bin/env python3
# Recuerda en qué escritorio estaba cada ventana y la devuelve ahí cuando se reabre:
#  - Al prender la PC (sesión anterior) y también a mitad de sesión: si cerrás
#    Brave y lo reabrís, o cerrás una ventana y la recuperás (Ctrl+Shift+T),
#    vuelve a su workspace. Lo cerrado se recuerda RECORDAR_CERRADAS seg.
#  - Compara clase + título (exacto, o parecido si el título cambió un poco).
#  - Las apps con escritorio fijo (windowrules.lua) no se tocan: las ubican las reglas.
#  - Cada GUARDAR_CADA seg guarda la distribución en actual.json.
# Se lanza desde config/autostart.lua.
import difflib, json, os, re, subprocess, time

ESTADO = os.path.expanduser("~/.local/state/hypr-sesion")
ACTUAL = os.path.join(ESTADO, "actual.json")
ANTERIOR = os.path.join(ESTADO, "anterior.json")
GUARDAR_CADA = 20
CONSULTAR_CADA = 2
RECORDAR_CERRADAS = 15 * 60
REINTENTO_TITULO = 60  # seg que se espera a que una ventana nueva tenga su título real
SIMILITUD_MINIMA = 0.6
LOG = os.path.join(ESTADO, "movimientos.log")
# Solo se restauran ventanas normales de Brave (las que Brave reabre solo). No se tocan:
# terminales/editores nuevos, las apps con escritorio fijo (windowrules.lua) ni las
# ventanas de app de YouTube (SUPER+ALT+Q, libres en cualquier escritorio).
RESTAURABLES = re.compile(r"^brave-browser$")
# Títulos mientras la ventana todavía no cargó nada: esperar
CARGANDO = {"", "brave"}
# Ventana que nace como pestaña nueva = la abrió el usuario (SUPER+W, Ctrl+N): nunca moverla
NUEVA = {"nueva pestaña - brave", "new tab - brave", "nueva pestaña", "new tab", "about:blank - brave"}


def clientes():
    try:
        out = subprocess.run(["hyprctl", "clients", "-j"], capture_output=True, text=True, timeout=5).stdout
        return json.loads(out)
    except Exception:
        return None


def normalizar(titulo):
    # "(7)TikTok - Brave" y "TikTok - Brave" son la misma ventana
    return re.sub(r"^\(\d+\)\s*", "", titulo or "").strip().lower()


def destino(ws):
    nombre, wid = ws.get("name", ""), ws.get("id", 0)
    if nombre.startswith("special"):
        return nombre
    if wid > 0:
        return str(wid)
    return "name:" + nombre


def entrada(c):
    return {"clase": c["class"], "titulo": normalizar(c["title"]), "ws": destino(c["workspace"])}


def validas(lista):
    return [c for c in lista if c.get("mapped", True) and c["workspace"].get("name")]


def guardar(lista, ultimo_total):
    datos = [entrada(c) for c in validas(lista)]
    # Si de golpe desaparece más de la mitad (ej. apagando la PC), no pisar la sesión buena
    if not datos or (ultimo_total >= 4 and len(datos) < ultimo_total / 2):
        return ultimo_total
    tmp = ACTUAL + ".tmp"
    with open(tmp, "w") as f:
        json.dump(datos, f, ensure_ascii=False, indent=1)
    os.replace(tmp, ACTUAL)
    return len(datos)


def mover(direccion, ws):
    cmd = f'hl.dsp.window.move({{ workspace = "{ws}", window = "address:{direccion}", follow = false }})'
    subprocess.run(["hyprctl", "dispatch", cmd], capture_output=True, timeout=5)


def registrar(texto):
    try:
        with open(LOG, "a") as f:
            f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + texto + "\n")
    except OSError:
        pass


def buscar(pendientes, clase, titulo):
    candidatos = [(i, p) for i, p in enumerate(pendientes) if p["clase"] == clase]
    for i, p in candidatos:
        if p["titulo"] == titulo:
            return i
    # Título parecido solo para la sesión anterior (al prender la PC); lo cerrado
    # a mitad de sesión exige título exacto para no arrastrar ventanas nuevas.
    mejor, puntaje = None, SIMILITUD_MINIMA
    for i, p in candidatos:
        if not p.get("parecido"):
            continue
        r = difflib.SequenceMatcher(None, p["titulo"], titulo).ratio()
        if r >= puntaje:
            mejor, puntaje = i, r
    return mejor


def main():
    os.makedirs(ESTADO, exist_ok=True)
    if os.path.exists(ACTUAL):
        os.replace(ACTUAL, ANTERIOR)
    # pendientes: [{clase, titulo, ws, vence}] — sesión anterior (vence al rato) + cerradas recientes
    pendientes = []
    inicio = time.time()
    if os.path.exists(ANTERIOR):
        with open(ANTERIOR) as f:
            for p in json.load(f):
                p["vence"] = inicio + 30 * 60
                p["parecido"] = True
                pendientes.append(p)

    iniciales = validas(clientes() or [])
    vivas = {c["address"]: entrada(c) for c in iniciales}  # última info conocida de cada ventana abierta
    nuevas = {}  # address -> momento en que apareció (aún sin resolver)
    ultimo_guardado, ultimo_total = inicio, len(iniciales)

    while True:
        ahora = time.time()
        lista = clientes()
        if lista is not None:
            lista = validas(lista)
            actuales = {c["address"]: c for c in lista}

            # Ventanas que se cerraron: recordarlas por si se reabren
            for dirc, info in list(vivas.items()):
                if dirc not in actuales:
                    del vivas[dirc]
                    nuevas.pop(dirc, None)
                    if RESTAURABLES.match(info["clase"]) and info["titulo"] not in CARGANDO | NUEVA:
                        pendientes.append(dict(info, vence=ahora + RECORDAR_CERRADAS))

            pendientes = [p for p in pendientes if p["vence"] > ahora]

            for dirc, c in actuales.items():
                if dirc not in vivas:
                    nuevas[dirc] = ahora
                vivas[dirc] = entrada(c)
                if dirc not in nuevas:
                    continue
                if not RESTAURABLES.match(c["class"]) or ahora - nuevas[dirc] > REINTENTO_TITULO:
                    del nuevas[dirc]
                    continue
                titulo = normalizar(c["title"])
                # initialTitle: con qué título NACIÓ la ventana (Brave carga la página de
                # inicio en 1-2 s, así que el título actual ya no dice "Nueva pestaña")
                if normalizar(c.get("initialTitle")) in NUEVA or titulo in NUEVA:
                    del nuevas[dirc]  # la abrió el usuario: se queda donde está, para siempre
                    continue
                if titulo in CARGANDO:
                    continue  # esperar a que cargue el título real
                i = buscar(pendientes, c["class"], titulo)
                if i is not None:
                    del nuevas[dirc]
                    p = pendientes.pop(i)
                    if destino(c["workspace"]) != p["ws"]:
                        mover(dirc, p["ws"])
                        vivas[dirc]["ws"] = p["ws"]
                        registrar(f'{destino(c["workspace"])} -> {p["ws"]}  "{titulo}" (coincide con "{p["titulo"]}")')

            if ahora - ultimo_guardado >= GUARDAR_CADA:
                ultimo_total = guardar(lista, ultimo_total)
                ultimo_guardado = ahora
        time.sleep(CONSULTAR_CADA)


if __name__ == "__main__":
    main()
