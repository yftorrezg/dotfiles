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
MAPA_PY = os.environ.get("MAPA_PY") or os.path.expanduser("~/.config/hypr/scripts/mapa-tras-borrar.py")
LEER_SH = os.environ.get("LEER_SH") or os.path.expanduser("~/.config/hypr/scripts/leer-seleccion.sh")
MODAL_SH = os.path.join(AQUI, "modal-toggle.sh")
TARJETAS_PY = os.environ.get("TARJETAS_PY") or os.path.expanduser("~/.config/hypr/scripts/tarjetas.py")
TIPOS = {"?": ("duda", "❓"), "!": ("clave", "🔑"), "p": ("practicar", "🛠️")}
MAX_INTERVALO = 60  # días
SOCK = os.environ.get("NOTAS_SOCK") or os.path.join(os.environ.get("XDG_RUNTIME_DIR", "/tmp"), "mpv-notas.sock")
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


_ultimo_push = {"v": None}
VERSION = os.path.getmtime(os.path.abspath(__file__))


def estado():
    v = video_actual()
    if not v:
        _ultimo_push["v"] = None
        return {"mpv": False}
    if _filtro["f"] and _ultimo_push["v"] is None:  # mpv se reabrió: vuelve a decirle el filtro activo
        empujar_filtro()
    _ultimo_push["v"] = v
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
    out, imps = [], importantes()
    for i, e in enumerate(pl):
        ruta = e.get("filename", "")
        if not re.match(r"^\w[\w+.-]*://", ruta) and not ruta.startswith("/"):
            ruta = os.path.join(wd, ruta)
        nombre = e.get("title") or os.path.splitext(os.path.basename(ruta))[0]
        out.append({"i": i, "nombre": nombre, "ruta": normalizar(ruta),
                    "cap": os.path.basename(os.path.dirname(ruta)),  # capítulo (carpeta): el panel lo usa de título
                    "actual": bool(e.get("current")), "dur": duracion(ruta),
                    "marcas": marcas_de(imps, normalizar(ruta))})
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


# ---------- gestión de videos: importantes · borrar · recortar ----------
IMPORTANTES = os.environ.get("NOTAS_IMPORTANTES") or os.path.expanduser("~/.local/share/mpv-panel/importantes.json")
EXT_VIDEO = {"3g2", "3gp", "avi", "flv", "m2ts", "m4v", "mkv", "mov", "mp4", "mpeg", "mpg", "ogv", "ts", "webm", "wmv"}
EXT_SUBS = {"srt", "vtt", "ass"}
MARCAS = ("imp", "dudo", "sabido")
MARCAS_CURSO = ("Apuntes", "capturas", "capturas-clave")  # las mismas que usa curso.lua
CARPETAS_CLAVE = ("capturas-clave", "capturas-esenciales", "codigo-en-imagenes")
WATCH_LATER = os.path.expanduser("~/.local/state/mpv/watch_later")
_gest_candado = threading.Lock()


def _alnum(t):
    return re.sub(r"[\W_]+", "", t.casefold())


def importantes():
    """{ruta del video: {"curso": raíz, "marcas": ["imp"|"dudo"|"sabido"]}} (las entradas viejas sin 'marcas' eran 'imp')."""
    return leer_json(IMPORTANTES, {})


def marcas_de(d, ruta):
    e = d.get(ruta)
    return [] if not e else list(e.get("marcas", ["imp"]))


def alternar_marca(ruta, marca):
    """Pone / quita una marca. 'sabido' y 'dudo' (no lo entendí) se excluyen entre sí. Devuelve las marcas nuevas."""
    if marca not in MARCAS:
        return None
    with _gest_candado:
        d = importantes()
        ms = marcas_de(d, ruta)
        if marca in ms:
            ms.remove(marca)
        else:
            ms.append(marca)
            if marca == "sabido" and "dudo" in ms:
                ms.remove("dudo")
            if marca == "dudo" and "sabido" in ms:
                ms.remove("sabido")
        if ms:
            d[ruta] = {"curso": raiz_curso(ruta), "marcas": ms}
        else:
            d.pop(ruta, None)
        os.makedirs(os.path.dirname(IMPORTANTES), exist_ok=True)
        escribir_json(IMPORTANTES, d)
        return ms


def quitar_importante(ruta):
    with _gest_candado:
        d = importantes()
        if d.pop(ruta, None) is not None:
            escribir_json(IMPORTANTES, d)


def raiz_curso(ruta):
    """Carpeta raíz del curso del video (sube hasta 4 carpetas buscando Apuntes/…, como curso.lua)."""
    d = os.path.dirname(ruta)
    x = d
    for _ in range(5):
        if any(os.path.isdir(os.path.join(x, m)) for m in MARCAS_CURSO):
            return x
        p = os.path.dirname(x)
        if p == x:
            break
        x = p
    return d


def item_de_lista(i):
    """Item i de la lista de mpv si es un video local que existe (lo único que se puede tocar); si no, None."""
    item = next((x for x in lista_reproduccion() if x["i"] == i), None)
    if not item or re.match(r"^\w[\w+.-]*://", item["ruta"]) or not os.path.isfile(item["ruta"]):
        return None
    if os.path.splitext(item["ruta"])[1].lstrip(".").lower() not in EXT_VIDEO:
        return None
    return item


def _subtitulos_de(ruta):
    d, stem = os.path.split(ruta)
    stem = os.path.splitext(stem)[0]
    try:
        return [os.path.join(d, f) for f in sorted(os.listdir(d))
                if f.startswith(stem + ".") and f.rsplit(".", 1)[-1].lower() in EXT_SUBS]
    except OSError:
        return []


def apuntes_de(ruta):
    """Todo lo derivado de este video: carpeta de apuntes, capturas clave, notas del panel, fila del MAPA."""
    raiz = raiz_curso(ruta)
    stem = os.path.splitext(os.path.basename(ruta))[0]
    limpio = re.sub(r"^(\d+)\.\s*", r"\1 ", stem)  # "009. Cursores" → "009 Cursores"
    carpeta_v = os.path.dirname(ruta)
    cand = f"{os.path.basename(carpeta_v)} - {limpio}" if carpeta_v != raiz else limpio
    res = {"clase": None, "dir": None, "archivos": [], "extras": [], "mapa": None, "notas": 0, "slug": None}
    base = next((os.path.join(raiz, n) for n in ("Apuntes", "capturas") if os.path.isdir(os.path.join(raiz, n))), None)
    if base:
        try:
            nombres = os.listdir(base)
        except OSError:
            nombres = []
        hallado = cand if cand in nombres else next((n for n in nombres if _alnum(n) == _alnum(cand)), None)
        if hallado and os.path.isdir(os.path.join(base, hallado)):
            res["clase"], res["dir"] = hallado, os.path.join(base, hallado)
            res["archivos"] = sorted(f for f in os.listdir(res["dir"])
                                     if f in ("apuntes.md", "resumen.md", "tarjetas.md", "tarjetas-anki.txt", "transcripcion.md"))
    if res["clase"]:
        pref = re.compile(r"^\d+ " + re.escape(res["clase"]) + r" · ")
        for c in CARPETAS_CLAVE:
            cd = os.path.join(raiz, c)
            if os.path.isdir(cd):
                res["extras"] += [os.path.join(cd, f) for f in sorted(os.listdir(cd)) if pref.match(f)]
        mapa = os.path.join(raiz, "MAPA.md")
        if os.path.isfile(mapa):
            res["mapa"] = mapa
    slug = indice().get(ruta)
    d = slug and cargar(slug)
    if d:
        res["slug"], res["notas"] = slug, len(d["notas"])
    return res


def a_papelera(ruta):
    """Manda a la papelera (recuperable). Devuelve None si fue bien o el texto del error."""
    r = subprocess.run(["gio", "trash", ruta], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=120)
    return None if r.returncode == 0 else (r.stderr.decode(errors="replace").strip() or "gio trash falló")


def info_borrado(i):
    item = item_de_lista(i)
    if not item:
        return None
    a = apuntes_de(item["ruta"])
    return {"nombre": item["nombre"], "clase": a["clase"], "archivos": a["archivos"],
            "capturas": len(a["extras"]), "notas": a["notas"], "subs": len(_subtitulos_de(item["ruta"]))}


def borrar_video(i, con_apuntes):
    """Quita el video de la lista y lo manda a la papelera (+ subtítulos). Con con_apuntes: también sus apuntes."""
    item = item_de_lista(i)
    if not item:
        return {"ok": False, "error": "video no encontrado"}
    ruta = item["ruta"]
    a = apuntes_de(ruta) if con_apuntes else None
    archivos = [ruta] + _subtitulos_de(ruta)
    for f in archivos:
        err = a_papelera(f)
        if err:
            return {"ok": False, "error": err}
    ocultos = os.path.join(os.path.dirname(ruta), ".hidden")
    if os.path.isfile(ocultos):  # los .srt se ocultan en .hidden: limpia los nombres borrados
        quitar = {os.path.basename(f) for f in archivos}
        try:
            with open(ocultos, encoding="utf-8") as f:
                lineas = f.read().splitlines()
            if any(l in quitar for l in lineas):
                with open(ocultos, "w", encoding="utf-8") as f:
                    f.write("\n".join(l for l in lineas if l not in quitar) + "\n")
        except OSError:
            pass
    ipc("playlist-remove", i)
    quitar_importante(ruta)
    if _filtro["f"]:
        empujar_filtro()
    borrados = {"video": True, "apuntes": False, "capturas": 0, "notas": 0}
    if a:
        if a["dir"] and not a_papelera(a["dir"]):
            borrados["apuntes"] = True
        for f in a["extras"]:
            if not a_papelera(f):
                borrados["capturas"] += 1
        if a["clase"] and a["mapa"]:
            _quitar_de_mapa(a["mapa"], a["clase"])  # al instante; después se recompone entero (sin IA)
            if os.path.isfile(MAPA_PY):
                subprocess.Popen([sys.executable, MAPA_PY, os.path.dirname(a["mapa"]), a["clase"]],
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                                 start_new_session=True)
        if a["slug"]:
            with _candado:
                idx = indice()
                if idx.pop(ruta, None) is not None:
                    escribir_json(os.path.join(RAIZ, "indice.json"), idx)
            if not a_papelera(carpeta(a["slug"])):
                borrados["notas"] = a["notas"]
    return {"ok": True, **borrados}


def _quitar_de_mapa(mapa, clase):
    """Quita del MAPA.md la fila de la clase borrada (si no, el enlace quedaría roto)."""
    try:
        with open(mapa, encoding="utf-8") as f:
            lineas = f.read().split("\n")
        clave = f"Apuntes/{clase}/"
        nuevas = [l for l in lineas if clave not in l]
        if len(nuevas) != len(lineas):
            with open(mapa, "w", encoding="utf-8") as f:
                f.write("\n".join(nuevas))
    except OSError:
        pass


# ---------- recortar (principio y final) ----------
_recorte = {"activo": False, "pct": 0, "ok": None, "msg": "", "i": None}


def estado_recorte():
    return dict(_recorte)


def _ffmpeg(args, dur, al_progreso=None):
    p = subprocess.Popen(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-nostats", "-progress", "pipe:1"] + args,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    for l in p.stdout:
        if al_progreso and l.startswith("out_time_us="):
            try:
                al_progreso(min(0.99, int(l.split("=")[1]) / 1e6 / max(dur, 0.1)))
            except ValueError:
                pass
    err = p.stderr.read()
    return p.wait() == 0, err.strip()[-300:]


def _seg_srt(t):
    h, m, r = t.replace(",", ".").split(":")
    return int(h) * 3600 + int(m) * 60 + float(r)


def _txt_srt(t):
    t = max(0, round(t * 1000))
    return f"{t // 3600000:02d}:{t // 60000 % 60:02d}:{t // 1000 % 60:02d},{t % 1000:03d}"


def cortar_srt(ruta, ini, fin):
    """Deja en el .srt solo lo que cae entre ini y fin, con los tiempos desplazados (el original va a la papelera)."""
    with open(ruta, encoding="utf-8-sig") as f:
        bloques = re.split(r"\n\s*\n", f.read().strip().replace("\r\n", "\n"))
    salida = []
    for b in bloques:
        l = b.split("\n")
        k = next((j for j, x in enumerate(l) if "-->" in x), None)
        if k is None:
            continue
        a, z = (_seg_srt(x.strip()) for x in l[k].split("-->")[:2])
        if z <= ini or a >= fin:
            continue
        salida.append("\n".join([str(len(salida) + 1), f"{_txt_srt(max(a, ini) - ini)} --> {_txt_srt(min(z, fin) - ini)}"] + l[k + 1:]))
    if a_papelera(ruta):
        return
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("\n\n".join(salida) + "\n")


def _hilo_recorte(i, ruta, ini, fin, dur):
    nuevo = fin - ini
    d, base = os.path.split(ruta)
    tmp = os.path.join(d, f".recorte-{os.getpid()}-{base}")
    subs = _subtitulos_de(ruta)
    try:
        ok, err = _ffmpeg(["-ss", f"{ini:.3f}", "-i", ruta, "-t", f"{nuevo:.3f}", "-map", "0:v:0", "-map", "0:a?",
                           "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-c:a", "copy", tmp],
                          nuevo, lambda f: _recorte.update(pct=round(f * 100)))
        if not ok:
            raise RuntimeError("ffmpeg: " + err)
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", tmp],
                           stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=15)
        real = float(r.stdout.decode().strip().splitlines()[0])
        if abs(real - nuevo) > 3:
            raise RuntimeError(f"el resultado dura {fmt(real)} y se esperaba {fmt(nuevo)}")
        err = a_papelera(ruta)  # el original queda recuperable en la papelera
        if err:
            raise RuntimeError("no pude guardar el original en la papelera: " + err)
        os.replace(tmp, ruta)
        for sub in subs:  # los .srt siguen el mismo corte (vtt/ass no se tocan)
            if sub.lower().endswith(".srt"):
                try:
                    cortar_srt(sub, ini, fin)
                except (OSError, ValueError):
                    pass
        slug = indice().get(ruta)  # notas del panel: desplaza los tiempos
        d_notas = slug and cargar(slug)
        if d_notas:
            with _candado:
                for n in d_notas["notas"]:
                    n["t"] = round(min(max(0, n["t"] - ini), real), 1)
                guardar(slug, d_notas)
        try:  # posición guardada del video viejo (pasaría del final del nuevo)
            os.remove(os.path.join(WATCH_LATER, hashlib.md5(ruta.encode()).hexdigest().upper()))
        except OSError:
            pass
        if (item := next((x for x in lista_reproduccion() if x["ruta"] == ruta), None)) and item["actual"]:
            ipc("playlist-play-index", item["i"])  # recarga el archivo nuevo
        _recorte.update(activo=False, ok=True, pct=100, msg=f"Listo: {fmt(dur)} → {fmt(real)}")
    except Exception as e:
        if os.path.exists(tmp):
            os.remove(tmp)
        _recorte.update(activo=False, ok=False, msg=str(e))


def iniciar_recorte(i, ini, fin):
    if _recorte["activo"]:
        return {"ok": False, "error": "ya hay un recorte en curso"}
    item = item_de_lista(i)
    if not item:
        return {"ok": False, "error": "video no encontrado"}
    dur = duracion(item["ruta"]) or 0
    ini = max(0.0, float(ini or 0))
    fin = float(fin) if fin not in (None, "") else dur
    fin = min(fin, dur) if dur else fin
    if fin - ini < 2:
        return {"ok": False, "error": "no queda nada del video (mínimo 2 s)"}
    if ini < 0.5 and dur - fin < 0.5:
        return {"ok": False, "error": "no hay nada que recortar"}
    _recorte.update(activo=True, pct=0, ok=None, msg="", i=i)
    threading.Thread(target=_hilo_recorte, args=(i, item["ruta"], ini, fin, dur), daemon=True).start()
    return {"ok": True}


# ---------- reproducir solo los importantes ----------
def _clave_natural(s):
    return [int(x) if x.isdigit() else x for x in re.split(r"(\d+)", s.casefold())]


_filtro = {"f": ""}


def empujar_filtro():
    """Manda a mpv (filtro.lua) qué videos de la lista están permitidos: así > / < / Enter / el fin del video
    pasan solo por los del filtro activo. Filtro vacío = todos."""
    f = _filtro["f"]
    rutas = []
    if f:
        for x in lista_reproduccion():
            m = x["marcas"]
            if (f == "pend" and "sabido" not in m) or (f in MARCAS and f in m):
                rutas.append(x["ruta"])
    ipc("script-message", "filtro-rutas", json.dumps({"f": f, "rutas": rutas}, ensure_ascii=False))
    return len(rutas)


def reproducir_filtro(i_ref, filtro):
    """Reemplaza la lista de mpv por los videos del curso que cumplen el filtro (imp | dudo | sabido | pend = sin 'sabido')."""
    ref = next((x for x in lista_reproduccion() if x["i"] == i_ref), None)
    if not ref:
        return {"ok": False, "error": "sin lista"}
    raiz, d = raiz_curso(ref["ruta"]), importantes()
    if filtro == "pend":
        elegidos = [x["ruta"] for x in lista_reproduccion() if "sabido" not in marcas_de(d, x["ruta"])]
    elif filtro in MARCAS:
        elegidos = sorted((r for r in d if filtro in marcas_de(d, r) and raiz_curso(r) == raiz and os.path.isfile(r)),
                          key=_clave_natural)
    else:
        return {"ok": False, "error": "filtro desconocido"}
    if not elegidos:
        return {"ok": False, "error": "no hay videos con esa marca en este curso"}
    ipc("loadfile", elegidos[0], "replace")
    for r in elegidos[1:]:
        ipc("loadfile", r, "append")
    enfocar_mpv()
    return {"ok": True, "n": len(elegidos)}


# ---------- apuntes y tarjetas de la clase (tecla i) ----------
def parsear_tarjetas(md):
    """[{sec, q, a}] desde tarjetas.md: pregunta, una línea con «?» sola, respuesta; bloques separados por línea en blanco."""
    res, sec, bloque, cod = [], "", [], False

    def cerrar():
        nonlocal bloque
        if bloque:
            k, dentro = None, False  # primera línea «?» sola que no esté dentro de un bloque de código
            for n, l in enumerate(bloque):
                if l.lstrip().startswith("```"):
                    dentro = not dentro
                elif l.strip() == "?" and not dentro:
                    k = n
                    break
            if k is not None:
                q, a = "\n".join(bloque[:k]).strip(), "\n".join(bloque[k + 1:]).strip()
                if q and a:
                    res.append({"sec": sec, "q": q, "a": a})
            elif len(bloque) == 1 and "::" in bloque[0]:
                q, a = (x.strip() for x in bloque[0].split("::", 1))
                if q and a:
                    res.append({"sec": sec, "q": q, "a": a})
        bloque = []

    for l in md.split("\n"):
        if l.lstrip().startswith("```"):
            cod = not cod
        if not cod and l.startswith("#"):
            cerrar()
            if l.startswith("## "):
                sec = l[3:].strip()
            continue
        if not cod and not l.strip():
            cerrar()
            continue
        if not cod and re.match(r"^\*.*\*$", l.strip()):
            continue  # la nota en cursiva del encabezado
        bloque.append(l)
    cerrar()
    return res


def _leer_texto(ruta):
    try:
        with open(ruta, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return None


def datos_clase(i):
    item = item_de_lista(i)
    if not item:
        return None
    a = apuntes_de(item["ruta"])
    base = a["dir"]
    md = _leer_texto(os.path.join(base, "apuntes.md")) if base else None
    res = _leer_texto(os.path.join(base, "resumen.md")) if base else None
    tj = _leer_texto(os.path.join(base, "tarjetas.md")) if base else None
    return {"i": i, "nombre": item["nombre"], "clase": a["clase"], "dur": item["dur"], "actual": item["actual"],
            "apuntes": md, "resumen": res, "tarjetas": parsear_tarjetas(tj) if tj else [],
            "notas": a["notas"], "marcas": marcas_de(importantes(), item["ruta"])}


def indice_actual():
    return next((x["i"] for x in lista_reproduccion() if x["actual"]), None)


def leer_en_voz_alta(texto):
    """Lee el texto con la voz que el usuario eligió (leer-seleccion.sh); si ya está leyendo, lo corta."""
    if not os.path.isfile(LEER_SH):
        return False
    tmp = os.path.join(os.environ.get("XDG_RUNTIME_DIR", "/tmp"), f"leer-apuntes-{os.getpid()}.txt")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(texto)
    subprocess.Popen(["bash", LEER_SH, "--texto-archivo", tmp], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                     stdin=subprocess.DEVNULL, start_new_session=True)
    return True


def parar_lectura():
    if os.path.isfile(LEER_SH):
        subprocess.Popen(["bash", LEER_SH, "--stop"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                         stdin=subprocess.DEVNULL, start_new_session=True)


_pausa_modal = {"puse": False}


def pausa_modal(on):
    """El modal pausa el video al abrirse y lo reanuda al cerrarse (solo si lo pausó él)."""
    if on:
        if ipc("get_property", "pause") is False:
            ipc("set_property", "pause", True)
            _pausa_modal["puse"] = True
    elif _pausa_modal["puse"]:
        _pausa_modal["puse"] = False
        ipc("set_property", "pause", False)


def abrir_modal(vista, i=None):
    q = f"?v={vista}" + (f"&i={int(i)}" if i is not None else "")
    subprocess.Popen(["bash", MODAL_SH, "abrir", q], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                     stdin=subprocess.DEVNULL, start_new_session=True)


def cerrar_modal():
    subprocess.Popen(["bash", MODAL_SH, "cerrar"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                     stdin=subprocess.DEVNULL, start_new_session=True)


# ---------- capturas del curso (clave / esenciales) ----------
RE_CAP = re.compile(r"^(\d+) (.*) · (\d+) · (\d\d)-(\d\d)-(\d\d)\.(webp|jpg|jpeg|png)$")
_cap_cache = {}


def listar_capturas(raiz, conjunto):
    """[{f, clase, t, n, seq}] de capturas-<conjunto>/ en orden del curso (n = número de clase, seq = orden dentro)."""
    d = os.path.join(raiz, "capturas-" + conjunto)
    try:
        mt = os.stat(d).st_mtime
        nombres = os.listdir(d)
    except OSError:
        return []
    if _cap_cache.get(d, (None,))[0] == mt:
        return _cap_cache[d][1]
    res = []
    for f in nombres:
        m = RE_CAP.match(f)
        if m:
            res.append({"f": f, "clase": m.group(2), "t": int(m.group(4)) * 3600 + int(m.group(5)) * 60 + int(m.group(6)),
                        "n": int(m.group(1)), "seq": int(m.group(3))})
    res.sort(key=lambda c: (c["n"], c["seq"]))
    _cap_cache[d] = (mt, res)
    return res


def capturas_de(i, conjunto, t=None):
    item = item_de_lista(i)
    if not item or conjunto not in ("clave", "esenciales"):
        return None
    raiz = raiz_curso(item["ruta"])
    items = listar_capturas(raiz, conjunto)
    clase = apuntes_de(item["ruta"])["clase"]
    if t is None:
        t = (ipc("get_property", "time-pos") or 0) if item["actual"] else 0
    cerca = None
    propias = [k for k, c in enumerate(items) if clase and c["clase"] == clase]
    if propias:
        cerca = min(propias, key=lambda k: abs(items[k]["t"] - t))
    elif items and clase:  # la clase no tiene capturas en este conjunto: la más próxima por número de clase
        otro = listar_capturas(raiz, "esenciales" if conjunto == "clave" else "clave")
        n = next((c["n"] for c in otro + items if c["clase"] == clase), None)
        if n is not None:
            cerca = min(range(len(items)), key=lambda k: (abs(items[k]["n"] - n), items[k]["n"] < n, items[k]["seq"]))
    return {"conjunto": conjunto, "clase": clase, "items": items, "cerca": cerca, "t": t,
            "otros": {c: len(listar_capturas(raiz, c)) for c in ("clave", "esenciales")}}


def ruta_captura(i, conjunto, f):
    item = item_de_lista(i)
    if not item or conjunto not in ("clave", "esenciales") or f != os.path.basename(f) or not RE_CAP.match(f):
        return None
    ruta = os.path.join(raiz_curso(item["ruta"]), "capturas-" + conjunto, f)
    return ruta if os.path.isfile(ruta) else None


# ---------- detectar intro y final comparando con otros videos del curso ----------
FPS_DET, SEG_DET, LADO = 2, 60, 32


def _frames(ruta, del_final):
    args = ["ffmpeg", "-v", "error", "-an"] + (["-sseof", f"-{SEG_DET}"] if del_final else []) + ["-i", ruta] + \
           ([] if del_final else ["-t", str(SEG_DET)]) + \
           ["-vf", f"fps={FPS_DET},scale={LADO}:{LADO},format=gray", "-f", "rawvideo", "-"]
    try:
        out = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=180).stdout
    except subprocess.SubprocessError:
        return []
    n = LADO * LADO
    return [out[k:k + n] for k in range(0, len(out) - n + 1, n)]


def _dif(a, b):
    return sum(abs(x - y) for x, y in zip(a, b)) / len(a)


def _prefijo_comun(a, b, umbral=7.0):
    n = 0
    for x, y in zip(a, b):
        if _dif(x, y) > umbral:
            break
        n += 1
    return n


def detectar_cortes(i):
    """Sugiere cuánto quitar al principio y al final: lo que se repite igual al empezar/terminar otros videos del curso."""
    item = item_de_lista(i)
    if not item:
        return {"ok": False, "error": "video no encontrado"}
    dur = duracion(item["ruta"]) or 0
    todos = [x for x in lista_reproduccion() if x["i"] != i and os.path.isfile(x["ruta"])]
    mismo = [x for x in todos if os.path.dirname(x["ruta"]) == os.path.dirname(item["ruta"])]
    otros = (mismo + [x for x in todos if x not in mismo])
    # los vecinos primero (mismo capítulo); entre 4 y 7 videos de comparación
    otros = sorted(otros, key=lambda x: abs(x["i"] - i))[:7]
    if len(otros) < 2:
        return {"ok": False, "error": "hacen falta al menos 2 videos más en la lista para comparar"}
    res = {"ok": True, "ini": 0.0, "fin": 0.0, "comparados": len(otros), "coinc_ini": 0, "coinc_fin": 0, "dur": dur}
    for lado, final in (("ini", False), ("fin", True)):
        mio = _frames(item["ruta"], final)
        if final:
            mio = mio[::-1]
        largos = []
        for x in otros:
            f = _frames(x["ruta"], final)
            if final:
                f = f[::-1]
            largos.append(_prefijo_comun(mio, f))
        buenos = sorted(l for l in largos if l >= 3 * FPS_DET // 2)  # al menos ~1,5 s iguales
        res["coinc_" + lado] = len(buenos)
        if len(buenos) * 2 >= len(otros):  # lo comparte la mayoría
            seg = buenos[len(buenos) // 2] / FPS_DET  # mediana
            if seg < SEG_DET - 1:  # si llega al tope no es una intro: es una plantilla fija
                res[lado] = round(seg + (0.3 if not final else 0.2), 1)
    if dur and res["fin"]:
        res["fin_en"] = round(max(0.0, dur - res["fin"]), 1)
    return res


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
        if u.path == "/api/filtro":
            return self._json({"filtro": _filtro["f"]})
        if u.path == "/api/version":
            return self._json({"v": VERSION})
        if u.path == "/api/lista":
            return self._json(lista_reproduccion())
        if u.path == "/api/borrar-info":
            try:
                info = info_borrado(int(q.get("i", ["-1"])[0]))
            except ValueError:
                info = None
            return self._json(info or {"error": "video no encontrado"}, 200 if info else 404)
        if u.path == "/modal.html":
            return self._archivo(os.path.join(AQUI, "modal.html"), "text/html; charset=utf-8")
        if u.path == "/api/clase":
            try:
                i = int(q["i"][0]) if "i" in q else indice_actual()
                datos = datos_clase(i) if i is not None else None
            except (ValueError, IndexError):
                datos = None
            return self._json(datos or {"error": "no hay video"}, 200 if datos else 404)
        if u.path == "/api/capturas":
            try:
                t = float(q["t"][0]) if "t" in q else None
                datos = capturas_de(int(q["i"][0]), q.get("set", ["clave"])[0], t)
            except (ValueError, KeyError):
                datos = None
            return self._json(datos or {"error": "sin capturas"}, 200 if datos else 404)
        if u.path == "/api/captura":
            try:
                ruta = ruta_captura(int(q["i"][0]), q.get("set", [""])[0], q.get("f", [""])[0])
            except (ValueError, KeyError):
                ruta = None
            if not ruta:
                return self._json({"error": "no existe"}, 404)
            return self._archivo(ruta, {"webp": "image/webp", "png": "image/png"}.get(ruta.rsplit(".", 1)[-1], "image/jpeg"), "max-age=86400")
        if u.path == "/api/detectar-cortes":
            try:
                return self._json(detectar_cortes(int(q["i"][0])))
            except (ValueError, KeyError):
                return self._json({"ok": False, "error": "falta i"})
        if u.path == "/api/leyendo":
            r = subprocess.run(["pgrep", "-x", "piper-tts|edge-tts|ffplay|pw-play"], stdout=subprocess.DEVNULL)
            if r.returncode != 0:
                r = subprocess.run(["pgrep", "-f", "chatterbox-hablar[.]py"], stdout=subprocess.DEVNULL)
            return self._json({"leyendo": r.returncode == 0})
        if u.path == "/api/recorte-estado":
            return self._json(estado_recorte())
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
            if d.get("i") is not None and indice_actual() != int(d["i"]):  # el modal prueba un video que no está sonando
                ipc("playlist-play-index", int(d["i"]))
                time.sleep(0.8)
            ok = ipc("seek", float(d["t"]), "absolute+exact") is not None
            if d.get("play"):
                ipc("set_property", "pause", False)
                _pausa_modal["puse"] = False
            else:
                enfocar_mpv()
            return self._json({"ok": ok})
        if p == "/api/reiniciar":  # lo pide panel-toggle.sh cuando el código del servidor cambió
            self._json({"ok": True})
            threading.Timer(0.3, lambda: os._exit(0)).start()
            return
        if p == "/api/filtro":
            f = d.get("filtro", "")
            _filtro["f"] = f if f in MARCAS + ("pend",) else ""
            return self._json({"ok": True, "n": empujar_filtro()})
        if p == "/api/ir":
            ipc("script-message", "filtro-libre")  # elegido a mano: se reproduce aunque no cumpla el filtro
            ok = ipc("playlist-play-index", int(d["i"])) is not None
            enfocar_mpv()
            return self._json({"ok": ok})
        if p == "/api/marca":
            item = item_de_lista(int(d["i"]))
            ms = item and alternar_marca(item["ruta"], d.get("marca"))
            if _filtro["f"]:
                empujar_filtro()
            return self._json({"ok": ms is not None and bool(item), "marcas": ms or []})
        if p == "/api/borrar-video":
            return self._json(borrar_video(int(d["i"]), bool(d.get("apuntes"))))
        if p == "/api/recortar":
            return self._json(iniciar_recorte(int(d["i"]), d.get("ini"), d.get("fin")))
        if p == "/api/reproducir-filtro":
            return self._json(reproducir_filtro(int(d["i"]), d.get("filtro", "")))
        if p == "/api/curso-completo":
            return self._json({"ok": ipc("script-message", "curso-completo") is not None})
        if p == "/api/mover":  # video anterior / siguiente (respeta el filtro activo)
            ipc("script-message", "filtro-mover", str(1 if int(d.get("d", 1)) > 0 else -1))
            return self._json({"ok": True})
        if p == "/api/abrir-imagen":  # en el visor de fotos (Gwenview): ahí se navega por toda la carpeta
            ruta = ruta_captura(int(d["i"]), d.get("set", ""), d.get("f", ""))
            if ruta:
                subprocess.Popen(["gwenview", ruta], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                 stdin=subprocess.DEVNULL, start_new_session=True)
            return self._json({"ok": bool(ruta)})
        if p == "/api/leer":
            return self._json({"ok": leer_en_voz_alta(str(d.get("texto", "")))})
        if p == "/api/parar-lectura":
            parar_lectura()
            return self._json({"ok": True})
        if p == "/api/modal":
            abrir_modal(d.get("vista", "apuntes"), d.get("i"))
            return self._json({"ok": True})
        if p == "/api/cerrar-modal":
            parar_lectura()
            pausa_modal(False)
            cerrar_modal()
            enfocar_mpv()
            return self._json({"ok": True})
        if p == "/api/pausa":
            pausa_modal(bool(d.get("on")))
            return self._json({"ok": True})
        if p == "/api/borrar-actual":  # tecla Delete: video + apuntes, sin preguntar
            i = indice_actual()
            return self._json(borrar_video(i, True) if i is not None else {"ok": False, "error": "no hay video"})
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
