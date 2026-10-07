#!/usr/bin/env python3
"""Notas de video para mpv: guarda notas con tiempo + captura y las muestra en un panel web.

  servidor.py serve                       arranca el panel en http://127.0.0.1:47831
  servidor.py nota VIDEO T TITULO TEXTO CAPTURA   crea una nota (lo usa notas.lua con Ctrl+n)

Todo vive en ~/Documentos/Notas-cursos/<nombre del video>/ :
  notas.json   fuente de verdad (el panel lo lee y lo edita)
  notas.md     resumen legible (Obsidian, VSCode, Drive...), se regenera solo
  capturas/    una imagen por nota
y ~/Documentos/Notas-cursos/indice.json enlaza cada ruta de video con su carpeta.
El panel habla con mpv por su socket IPC ($XDG_RUNTIME_DIR/mpv-notas.sock).
"""
import json, os, re, shutil, socket, subprocess, sys, threading, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs, unquote

PUERTO = 47831
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.expanduser("~/Documentos/Notas-cursos")
SOCK = os.path.join(os.environ.get("XDG_RUNTIME_DIR", "/tmp"), "mpv-notas.sock")
CERRAR_SIN_USO = 20 * 60  # segundos sin peticiones -> el servidor se apaga solo
_candado = threading.Lock()


# ---------- utilidades ----------
def fmt(t):
    t = int(t)
    h, m, s = t // 3600, t % 3600 // 60, t % 60
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def normalizar(ruta):
    return ruta if re.match(r"^\w[\w+.-]*://", ruta) else os.path.normpath(ruta)


def escribir_json(ruta, datos):
    tmp = ruta + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=1)
    os.replace(tmp, ruta)


def leer_json(ruta, defecto):
    try:
        with open(ruta, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return defecto


def indice():
    return leer_json(os.path.join(RAIZ, "indice.json"), {})


def hacer_slug(video, usados):
    base = os.path.splitext(os.path.basename(video.rstrip("/")))[0]
    base = re.sub(r'[/\\:*?"<>|\x00-\x1f]', "-", base)
    base = re.sub(r"\s+", " ", base).strip(" .")[:90] or "video"
    slug, n = base, 2
    while slug in usados:
        slug, n = f"{base} ({n})", n + 1
    return slug


# ---------- notas ----------
def carpeta(slug):
    return os.path.join(RAIZ, slug)


def cargar(slug):
    return leer_json(os.path.join(carpeta(slug), "notas.json"), None)


def guardar(slug, datos):
    datos["notas"].sort(key=lambda n: n["t"])
    escribir_json(os.path.join(carpeta(slug), "notas.json"), datos)
    escribir_md(slug, datos)


def escribir_md(slug, datos):
    l = [f"# {datos['nombre']}", "", f"Video: `{datos['video']}`", f"Notas: {len(datos['notas'])}", ""]
    for n in datos["notas"]:
        l += [f"## ⏱ {fmt(n['t'])} — {n['titulo']}", ""]
        if n.get("texto"):
            l += [n["texto"], ""]
        if n.get("captura"):
            l += [f"![{fmt(n['t'])}](capturas/{n['captura']})", ""]
    with open(os.path.join(carpeta(slug), "notas.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(l))


def crear_nota(video, t, titulo, texto, captura_tmp):
    video, t = normalizar(video), float(t)  # por la línea de comandos t llega como texto ("14779.27")
    with _candado:
        idx = indice()
        slug = idx.get(video)
        if not slug:
            slug = hacer_slug(video, set(idx.values()))
            idx[video] = slug
            os.makedirs(os.path.join(carpeta(slug), "capturas"), exist_ok=True)
            escribir_json(os.path.join(RAIZ, "indice.json"), idx)
        os.makedirs(os.path.join(carpeta(slug), "capturas"), exist_ok=True)
        datos = cargar(slug) or {"video": video, "nombre": os.path.splitext(os.path.basename(video))[0], "notas": []}
        nid = max([n["id"] for n in datos["notas"]] + [0]) + 1
        archivo = ""
        if captura_tmp and os.path.isfile(captura_tmp):
            archivo = f"{nid:03d}-{int(t)}.jpg"
            shutil.move(captura_tmp, os.path.join(carpeta(slug), "capturas", archivo))
        datos["notas"].append({
            "id": nid, "t": round(float(t), 2),
            "titulo": (titulo or "").strip() or f"Nota {fmt(t)}",
            "texto": (texto or "").strip(), "captura": archivo,
            "creada": time.strftime("%Y-%m-%d %H:%M"),
        })
        guardar(slug, datos)
    return slug


def editar_nota(video, nid, titulo, texto):
    with _candado:
        slug = indice().get(normalizar(video))
        datos = slug and cargar(slug)
        if not datos:
            return False
        for n in datos["notas"]:
            if n["id"] == nid:
                n["titulo"] = (titulo or "").strip() or f"Nota {fmt(n['t'])}"
                n["texto"] = (texto or "").strip()
                guardar(slug, datos)
                return True
    return False


def borrar_nota(video, nid):
    with _candado:
        slug = indice().get(normalizar(video))
        datos = slug and cargar(slug)
        if not datos:
            return False
        quedan = []
        for n in datos["notas"]:
            if n["id"] == nid:
                if n.get("captura"):
                    try:
                        os.remove(os.path.join(carpeta(slug), "capturas", n["captura"]))
                    except OSError:
                        pass
            else:
                quedan.append(n)
        datos["notas"] = quedan
        guardar(slug, datos)
        return True


def listar_videos():
    res = []
    for video, slug in indice().items():
        d = cargar(slug)
        if not d or not d["notas"]:
            continue
        mt = os.path.getmtime(os.path.join(carpeta(slug), "notas.json"))
        res.append({"video": video, "nombre": d["nombre"], "n": len(d["notas"]),
                    "existe": os.path.exists(video) or "://" in video, "mt": mt})
    res.sort(key=lambda v: -v["mt"])
    return res


# ---------- mpv (IPC) ----------
def ipc(*cmd):
    """Manda un comando a mpv; devuelve 'data' o None si mpv no responde."""
    try:
        s = socket.socket(socket.AF_UNIX)
        s.settimeout(1.5)
        s.connect(SOCK)
        s.sendall((json.dumps({"command": list(cmd), "request_id": 77}) + "\n").encode())
        buf = b""
        while True:
            chunk = s.recv(65536)
            if not chunk:
                return None
            buf += chunk
            for linea in buf.split(b"\n"):
                try:
                    r = json.loads(linea)
                except ValueError:
                    continue
                if r.get("request_id") == 77:
                    s.close()
                    if r.get("error") != "success":
                        return None
                    return True if r.get("data") is None else r["data"]  # comandos como seek no devuelven dato
    except OSError:
        return None


def video_actual():
    p = ipc("get_property", "path")
    if not p:
        return None
    if not re.match(r"^\w[\w+.-]*://", p) and not p.startswith("/"):
        p = os.path.join(ipc("get_property", "working-directory") or "", p)
    return normalizar(p)


def enfocar_mpv():
    subprocess.Popen(["hyprctl", "dispatch", 'hl.dsp.focus({ window = "class:^mpv$" })'],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def estado():
    v = video_actual()
    if not v:
        return {"mpv": False}
    slug = indice().get(v)
    version = 0
    if slug:
        try:
            version = os.path.getmtime(os.path.join(carpeta(slug), "notas.json"))
        except OSError:
            pass
    return {"mpv": True, "video": v, "nombre": os.path.splitext(os.path.basename(v))[0],
            "t": ipc("get_property", "time-pos") or 0, "dur": ipc("get_property", "duration") or 0,
            "pausa": bool(ipc("get_property", "pause")), "version": version}


# ---------- HTTP ----------
ultimo_uso = time.time()


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _json(self, datos, codigo=200):
        cuerpo = json.dumps(datos, ensure_ascii=False).encode()
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(cuerpo)))
        self.end_headers()
        self.wfile.write(cuerpo)

    def _archivo(self, ruta, tipo, cache="no-cache"):
        try:
            with open(ruta, "rb") as f:
                cuerpo = f.read()
        except OSError:
            return self._json({"error": "no existe"}, 404)
        self.send_response(200)
        self.send_header("Content-Type", tipo)
        self.send_header("Cache-Control", cache)
        self.send_header("Content-Length", str(len(cuerpo)))
        self.end_headers()
        self.wfile.write(cuerpo)

    def do_GET(self):
        global ultimo_uso
        ultimo_uso = time.time()
        u = urlparse(self.path)
        q = parse_qs(u.query)
        if u.path == "/":
            return self._archivo(os.path.join(AQUI, "panel.html"), "text/html; charset=utf-8")
        if u.path == "/api/estado":
            return self._json(estado())
        if u.path == "/api/videos":
            return self._json(listar_videos())
        if u.path == "/api/notas":
            video = normalizar(q.get("video", [""])[0])
            slug = indice().get(video)
            d = slug and cargar(slug)
            if not d:
                return self._json({"video": video, "slug": None, "notas": []})
            return self._json({"video": video, "slug": slug, "nombre": d["nombre"], "notas": d["notas"]})
        if u.path.startswith("/img/"):
            ruta = os.path.realpath(os.path.join(RAIZ, unquote(u.path[5:])))
            if not ruta.startswith(os.path.realpath(RAIZ) + os.sep):
                return self._json({"error": "no"}, 403)
            return self._archivo(ruta, "image/jpeg", "max-age=3600")
        self._json({"error": "no existe"}, 404)

    def do_POST(self):
        global ultimo_uso
        ultimo_uso = time.time()
        try:
            n = int(self.headers.get("Content-Length", 0))
            d = json.loads(self.rfile.read(n) or b"{}")
        except ValueError:
            return self._json({"error": "json"}, 400)
        p = urlparse(self.path).path
        if p == "/api/saltar":
            ok = ipc("seek", float(d["t"]), "absolute+exact") is not None
            enfocar_mpv()
            return self._json({"ok": ok})
        if p == "/api/abrir":
            video, t = d["video"], float(d.get("t", 0))
            if ipc("get_property", "pid") is not None:
                ipc("loadfile", video, "replace", -1, f"start={t}")
            else:
                subprocess.Popen(["setsid", "mpv", f"--start={t}", video],
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
            return self._json({"ok": True})
        if p == "/api/editar":
            return self._json({"ok": editar_nota(d["video"], int(d["id"]), d.get("titulo"), d.get("texto"))})
        if p == "/api/borrar":
            return self._json({"ok": borrar_nota(d["video"], int(d["id"]))})
        if p == "/api/nueva":  # nota creada desde el panel: la captura la saca mpv
            v, t = video_actual(), ipc("get_property", "time-pos")
            if not v or t is None:
                return self._json({"ok": False})
            tmp = os.path.join(os.path.dirname(SOCK), f"nota-panel-{os.getpid()}.jpg")
            ipc("screenshot-to-file", tmp, "video")
            crear_nota(v, t, d.get("titulo"), d.get("texto"), tmp)
            return self._json({"ok": True})
        self._json({"error": "no existe"}, 404)


def vigilar():
    while True:
        time.sleep(60)
        if time.time() - ultimo_uso > CERRAR_SIN_USO:
            os._exit(0)


def servir():
    os.makedirs(RAIZ, exist_ok=True)
    threading.Thread(target=vigilar, daemon=True).start()
    ThreadingHTTPServer(("127.0.0.1", PUERTO), H).serve_forever()


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "serve":
        servir()
    elif len(sys.argv) == 7 and sys.argv[1] == "nota":
        print(crear_nota(*sys.argv[2:7]))
    else:
        print(__doc__)
        sys.exit(1)
