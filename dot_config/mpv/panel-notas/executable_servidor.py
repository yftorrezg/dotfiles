#!/usr/bin/env python3
"""Notas de video para mpv: guarda notas con tiempo + captura y las muestra en un panel web.

  servidor.py serve                       arranca el panel en http://127.0.0.1:47831
  servidor.py nota VIDEO T TITULO TEXTO CAPTURA   crea una nota (lo usa notas.lua con Ctrl+n)

Todo vive en ~/Vídeos/Notas de videos/<nombre del video>/ (dentro de la bóveda de Obsidian):
  notas.json     fuente de verdad (el panel lo lee y lo edita)
  notas.md       resumen legible, se regenera solo
  tarjetas.md    las notas "?" como tarjetas del plugin Spaced Repetition (conserva tu progreso)
  capturas/      una imagen por nota
y indice.json enlaza cada ruta de video con su carpeta. Si el video tiene su cuadernillo en
~/Vídeos/Capturas de YouTube/, se escribe también ahí un mis-notas.md (apuntes.md no se toca).

Tipos de nota: el título puede empezar con  ?  (duda) ·  !  (clave) ·  p  (practicar).
El panel habla con mpv por su socket IPC ($XDG_RUNTIME_DIR/mpv-notas.sock).
"""
import datetime, hashlib, importlib.util, json, os, re, shutil, socket, subprocess, sys, threading, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs, unquote

PUERTO = int(os.environ.get("NOTAS_PUERTO", 47831))
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.environ.get("NOTAS_RAIZ") or os.path.expanduser("~/Vídeos/Notas de videos")
BOVEDA = os.path.dirname(RAIZ)  # raíz de la bóveda de Obsidian (para los enlaces ![[...]])
CLASES = os.environ.get("NOTAS_CLASES") or os.path.expanduser("~/Vídeos/Capturas de YouTube")
TARJETAS_PY = os.environ.get("TARJETAS_PY") or os.path.expanduser("~/.config/hypr/scripts/tarjetas.py")
TIPOS = {"?": ("duda", "❓"), "!": ("clave", "🔑"), "p": ("practicar", "🛠️")}
MAX_INTERVALO = 60  # días
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


# ---------- tipos y repaso ----------
def separar_tipo(titulo):
    """('?'|'!'|'p'|'', título limpio). '? algo' / '!algo' / 'p algo'; '¿…' cuenta como duda sin recortar."""
    t = (titulo or "").strip()
    m = re.match(r"^([?!])\s*(.+)$", t) or re.match(r"^(p)\s+(.+)$", t)
    if m:
        return m.group(1), m.group(2).strip()
    if t.startswith("¿"):
        return "?", t
    return "", t


def hoy():
    return datetime.date.today()


def sumar_dias(dias):
    return (hoy() + datetime.timedelta(days=dias)).isoformat()


def completar(n):
    """Rellena los campos de las notas viejas (sin tipo/intervalo/proximo)."""
    n.setdefault("tipo", "")
    n.setdefault("intervalo", 1)
    if not n.get("proximo"):
        n["proximo"] = sumar_dias(1)
    return n


def siguiente_repaso(n, sabe):
    """Leitner sencillo: 'Ya lo sé' duplica el intervalo (1,2,4,8… máx. 60 días); 'Repetir' vuelve a 1 día."""
    n["intervalo"] = min(max(int(n.get("intervalo", 1)) * 2, 2), MAX_INTERVALO) if sabe else 1
    n["proximo"] = sumar_dias(n["intervalo"])
    return n


# ---------- notas ----------
def carpeta(slug):
    return os.path.join(RAIZ, slug)


def cargar(slug):
    d = leer_json(os.path.join(carpeta(slug), "notas.json"), None)
    if d:
        for n in d["notas"]:
            completar(n)
    return d


def guardar(slug, datos):
    datos["notas"].sort(key=lambda n: n["t"])
    escribir_json(os.path.join(carpeta(slug), "notas.json"), datos)
    escribir_md(slug, datos)
    for extra in (escribir_tarjetas, escribir_mis_notas):  # nunca deben impedir guardar la nota
        try:
            extra(slug, datos)
        except Exception as e:
            print("aviso:", extra.__name__, e, file=sys.stderr)


def etiqueta(n):
    return f"{TIPOS[n['tipo']][1]} " if n.get("tipo") in TIPOS else ""


def cuerpo_notas(datos, ruta_captura):
    l = []
    for n in datos["notas"]:
        l += [f"## ⏱ {fmt(n['t'])} — {etiqueta(n)}{n['titulo']}", ""]
        if n.get("texto"):
            l += [n["texto"], ""]
        if n.get("captura"):
            l += [ruta_captura(n["captura"], n["t"]), ""]
    return l


def escribir_md(slug, datos):
    l = [f"# {datos['nombre']}", "", f"Video: `{datos['video']}`", f"Notas: {len(datos['notas'])}", ""]
    l += cuerpo_notas(datos, lambda c, t: f"![{fmt(t)}](capturas/{c})")
    with open(os.path.join(carpeta(slug), "notas.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(l))


def _tarjetas_mod():
    if not os.path.isfile(TARJETAS_PY):
        return None
    spec = importlib.util.spec_from_file_location("tarjetas_estudio", TARJETAS_PY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def tarjetas_de(datos):
    """[(sección, pregunta, respuesta)] con las notas de tipo duda."""
    res = []
    for n in datos["notas"]:
        if n.get("tipo") != "?":
            continue
        p = n["titulo"].strip()
        if not p.endswith("?"):
            p += "?"
        if not p.startswith("¿"):
            p = "¿" + p.lstrip("¿")
        r = n.get("texto") or f"(sin respuesta escrita: míralo en el video, ⏱ {fmt(n['t'])})"
        res.append(("❓ Mis dudas", p, r))
    return res


def escribir_tarjetas(slug, datos):
    """tarjetas.md para el plugin Spaced Repetition; reutiliza tarjetas.py para conservar el progreso."""
    mod = _tarjetas_mod()
    if mod is None:
        return
    salida = os.path.join(carpeta(slug), "tarjetas.md")
    tarjetas = tarjetas_de(datos)
    if not tarjetas and not os.path.exists(salida):
        return
    progreso, mias = {}, None
    if os.path.exists(salida):
        with open(salida, encoding="utf-8") as f:
            progreso, mias = mod.progreso_viejo(f.read())
    tag = "#flashcards/notas/" + mod.slug(datos["nombre"])
    md, _ = mod.armar_md(datos["nombre"], tag, tarjetas, progreso, mias)
    md = re.sub(r"^\*Repaso espaciado.*\*$",
                "*Tarjetas de tus notas «?» de mpv (se regeneran solas al crear, editar o borrar notas). "
                "Repaso con el plugin Spaced Repetition: Ctrl+P → «Revisar tarjetas en esta nota». "
                "Se conserva tu progreso y la sección «Mis tarjetas».*", md, count=1, flags=re.M)
    mod.escribir(salida, md)


def _norm(t):
    t = re.sub(r"^\d+\s*-\s*", "", t)  # playlists: "003 - título"
    return re.sub(r"[\W_]+", "", t.casefold())


def buscar_clase(nombre, profundidad=3):
    """Carpeta de clase del cuadernillo cuyo nombre coincide con el del video (o None)."""
    objetivo = _norm(nombre)
    if not objetivo or not os.path.isdir(CLASES):
        return None
    pendientes = [(CLASES, 0)]
    while pendientes:
        base, nivel = pendientes.pop(0)
        try:
            entradas = sorted(os.scandir(base), key=lambda e: e.name)
        except OSError:
            continue
        for e in entradas:
            if not e.is_dir(follow_symlinks=False):
                continue
            if _norm(e.name) == objetivo:
                return e.path
            if nivel + 1 < profundidad:
                pendientes.append((e.path, nivel + 1))
    return None


def escribir_mis_notas(slug, datos):
    """mis-notas.md junto al cuadernillo del video, si existe (apuntes.md no se toca)."""
    clase = buscar_clase(datos["nombre"])
    if not clase:
        return
    def captura(c, t):
        rel = os.path.relpath(os.path.join(carpeta(slug), "capturas", c), BOVEDA)
        return f"![[{rel}]]"
    l = [f"# 📝 Mis notas: {datos['nombre']}", "",
         "*Las escribes tú en mpv (Ctrl+n); se regeneran solas. [📓 Apuntes](apuntes.md)*", ""]
    l += cuerpo_notas(datos, captura)
    with open(os.path.join(clase, "mis-notas.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(l))


def crear_nota(video, t, titulo, texto, captura_tmp, tipo=None):
    video, t = normalizar(video), float(t)  # por la línea de comandos t llega como texto ("14779.27")
    tipo_t, limpio = separar_tipo(titulo)
    tipo = tipo_t or (tipo if tipo in TIPOS else "")
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
            "id": nid, "t": round(t, 2), "tipo": tipo,
            "titulo": limpio or f"Nota {fmt(t)}",
            "texto": (texto or "").strip(), "captura": archivo,
            "creada": time.strftime("%Y-%m-%d %H:%M"), "intervalo": 1, "proximo": sumar_dias(1),
        })
        guardar(slug, datos)
    return slug


def _con_nota(video, nid, fn):
    """Aplica fn(nota) a una nota y guarda; devuelve la nota o None."""
    with _candado:
        slug = indice().get(normalizar(video))
        datos = slug and cargar(slug)
        if not datos:
            return None
        for n in datos["notas"]:
            if n["id"] == nid:
                fn(n)
                guardar(slug, datos)
                return n
    return None


def editar_nota(video, nid, titulo, texto, tipo=None):
    def cambiar(n):
        tipo_t, limpio = separar_tipo(titulo)
        n["tipo"] = tipo_t or (tipo if tipo in TIPOS else "" if tipo == "" else n.get("tipo", ""))
        n["titulo"] = limpio or f"Nota {fmt(n['t'])}"
        n["texto"] = (texto or "").strip()
    return _con_nota(video, nid, cambiar) is not None


def repasado(video, nid, sabe):
    n = _con_nota(video, nid, lambda n: siguiente_repaso(n, sabe))
    return n["intervalo"] if n else None


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


def repaso_pendiente():
    """Notas con tipo (?, !, p) de todos los videos cuyo próximo repaso es hoy o antes."""
    limite, res = hoy().isoformat(), []
    for video, slug in indice().items():
        d = cargar(slug)
        for n in (d or {"notas": []})["notas"]:
            if n.get("tipo") and n["proximo"] <= limite:
                res.append(dict(n, video=video, slug=d.get("slug", slug), nombre=d["nombre"]))
    res.sort(key=lambda n: (n["proximo"], n["nombre"], n["t"]))
    return res


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


# ---------- lista de reproducción ----------
CACHE_MINI = os.path.expanduser("~/.cache/mpv-lista")
_mini_candado = threading.Lock()


def lista_reproduccion():
    """Lista actual de mpv: [{i, nombre, ruta, actual}] con el nombre sin extensión."""
    pl = ipc("get_property", "playlist") or []
    if pl is True:
        pl = []
    wd = ipc("get_property", "working-directory") or ""
    out = []
    for i, e in enumerate(pl):
        ruta = e.get("filename", "")
        if not re.match(r"^\w[\w+.-]*://", ruta) and not ruta.startswith("/"):
            ruta = os.path.join(wd, ruta)
        nombre = e.get("title") or os.path.splitext(os.path.basename(ruta))[0]
        out.append({"i": i, "nombre": nombre, "ruta": normalizar(ruta),
                    "actual": bool(e.get("current")), "dur": duracion(ruta)})
    return out


def miniatura(i):
    """Ruta del JPG de la miniatura del item i de la lista (la crea la primera vez); None si falla."""
    item = next((x for x in lista_reproduccion() if x["i"] == i), None)  # solo videos de la lista
    if not item or not os.path.isfile(item["ruta"]):
        return None
    st = os.stat(item["ruta"])
    clave = hashlib.sha1(f"{item['ruta']}|{st.st_size}|{st.st_mtime_ns}".encode()).hexdigest() + ".jpg"
    destino = os.path.join(CACHE_MINI, clave)
    with _mini_candado:
        if not os.path.exists(destino):
            os.makedirs(CACHE_MINI, exist_ok=True)
            r = subprocess.run(["ffmpegthumbnailer", "-i", item["ruta"], "-o", destino, "-s", "320", "-t", "10%"],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30)
            if r.returncode != 0 or not os.path.exists(destino):
                return None
    return destino


# ---------- duración (ffprobe, cacheada) ----------
CACHE_DUR = os.path.join(CACHE_MINI, "duraciones.json")
_dur_candado = threading.Lock()
_dur_cache = None


def _duraciones():
    global _dur_cache
    if _dur_cache is None:
        _dur_cache = leer_json(CACHE_DUR, {})
    return _dur_cache


def duracion(ruta):
    """Duración en segundos del video local (ffprobe + caché); None si es URL o falla."""
    if not ruta or re.match(r"^\w[\w+.-]*://", ruta) or not os.path.isfile(ruta):
        return None
    try:
        st = os.stat(ruta)
    except OSError:
        return None
    clave = hashlib.sha1(f"{ruta}|{st.st_size}|{st.st_mtime_ns}".encode()).hexdigest()
    with _dur_candado:
        cache = _duraciones()
        if clave in cache:
            return cache[clave]
        r = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", ruta],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=15)
        if r.returncode != 0:
            return None
        try:
            seg = float(r.stdout.decode().strip().splitlines()[0])
        except (ValueError, IndexError):
            return None
        cache[clave] = seg
        os.makedirs(CACHE_MINI, exist_ok=True)
        escribir_json(CACHE_DUR, cache)
        return seg


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
        if u.path == "/api/repaso":
            return self._json(repaso_pendiente())
        if u.path == "/api/lista":
            return self._json(lista_reproduccion())
        if u.path == "/mini":
            try:
                ruta = miniatura(int(q.get("i", ["-1"])[0]))
            except (ValueError, subprocess.SubprocessError):
                ruta = None
            if not ruta:
                return self._json({"error": "sin miniatura"}, 404)
            return self._archivo(ruta, "image/jpeg", "max-age=86400")
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
        if p == "/api/ir":
            ok = ipc("playlist-play-index", int(d["i"])) is not None
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
            return self._json({"ok": editar_nota(d["video"], int(d["id"]), d.get("titulo"), d.get("texto"), d.get("tipo"))})
        if p == "/api/repasado":
            dias = repasado(d["video"], int(d["id"]), bool(d.get("sabe")))
            return self._json({"ok": dias is not None, "dias": dias})
        if p == "/api/borrar":
            return self._json({"ok": borrar_nota(d["video"], int(d["id"]))})
        if p == "/api/nueva":  # nota creada desde el panel: la captura la saca mpv
            v, t = video_actual(), ipc("get_property", "time-pos")
            if not v or t is None:
                return self._json({"ok": False})
            tmp = os.path.join(os.path.dirname(SOCK), f"nota-panel-{os.getpid()}.jpg")
            ipc("screenshot-to-file", tmp, "video")
            crear_nota(v, t, d.get("titulo"), d.get("texto"), tmp, d.get("tipo"))
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
