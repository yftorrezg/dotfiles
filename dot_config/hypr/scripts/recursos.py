#!/usr/bin/env python3
"""Recursos que el curso trae junto a los videos: código del profe, enlaces, PDFs, lecturas.

Uso: recursos.py <video>                 # muestra qué recursos encontró para esa clase
     recursos.py --curso <carpeta curso>  # resumen de recursos del curso entero

Cómo se asocian a una clase (todo en la MISMA carpeta que el video):
  - De la clase: archivos con el mismo número que el video ("001. …zip" con "001. …mp4",
    "1.5 x.zip" con "1.5 y.mp4"). Es el código EXACTO de esa clase (así viene en los cursos de Udemy).
  - Lecturas: un .txt largo y sin enlaces cuyo número no tiene video ("02.txt" entre 01.mp4 y
    03.mp4, Academia X) va con la clase anterior.
  - Del proyecto: zips/código de la carpeta que no son de esta clase (p. ej. "001 citas-FIN.zip",
    el proyecto terminado de toda la sección). Más avanzado que la clase: sirve para corregir el
    OCR y los nombres, no para adelantar contenido. Se eligen los archivos que más se parecen a lo
    que se ve en pantalla.
  - Enlaces: .url, "Enlace-a-X.txt" y las líneas de external-links.txt con el número de la clase.
Se saltan .git, node_modules, dist/build, archivos minificados, locks y binarios.
"""
import os
import re
import shutil
import subprocess
import sys
import zipfile

VIDEO = {".mp4", ".mkv", ".webm", ".ts", ".mov"}
CODIGO = {".js", ".jsx", ".ts", ".tsx", ".mjs", ".html", ".htm", ".css", ".scss", ".sass", ".py", ".php",
          ".sql", ".json", ".vue", ".java", ".c", ".cpp", ".h", ".cs", ".sh", ".md", ".txt", ".ipynb", ".xml",
          ".yml", ".yaml", ".env.example", ".graphql", ".prisma", ".blade.php", ".twig"}
SALTAR_DIR = {".git", "node_modules", "dist", "build", "vendor", ".next", "__pycache__", ".vscode", ".idea",
              "__MACOSX", "coverage", ".cache"}
SALTAR_ARCH = {"package-lock.json", "yarn.lock", "pnpm-lock.yaml", "composer.lock", ".ds_store", "desktop.ini"}
CARPETAS_COMUNES = {"css", "js", "src", "img", "images", "imagenes", "assets", "public", "scss", "sass", "styles",
                    "lib", "app", "components", "pages", "views", "routes", "models", "controllers", "static"}
MAX_ARCHIVO = 60_000      # bytes: más grande suele ser una librería o datos, no el código de la clase
URL = re.compile(r"https?://[^\s\]\)\"'<>]+")
PROYECTO = re.compile(r"(?<![a-z])(fin|final|terminad[oa]|complet[oa]|soluci[oó]n|materiales?|proyecto)(?![a-z])", re.I)
SPAM = ("t.me/", "telegram")  # firmas de los canales que reparten los cursos, no son recursos


REDES = ("twitter.com", "x.com/", "instagram.com", "facebook.com", "discord", "patreon.com", "linkedin.com",
         "tiktok.com", "youtube.com/@", "youtube.com/channel", "youtube.com/c/", "t.me/", "paypal", "ko-fi",
         "buymeacoffee", "amzn.to", "bit.ly", "goo.gl", "twitch.tv", "wa.me")


def de_youtube(carpeta):
    """(enlaces, capitulos) de un video de YouTube a partir de <carpeta>/video.info.json (lo deja
    video-a-capturas.sh). enlaces = [(título, url)] de la descripción, sin redes sociales (los repos de
    GitHub primero); capitulos = [(segundo, título)] que puso el autor. ([], []) si no hay."""
    import json
    try:
        d = json.load(open(os.path.join(carpeta, "video.info.json"), encoding="utf-8"))
    except (OSError, ValueError):
        return [], []
    enlaces, vistos = [], set()
    for linea in (d.get("description") or "").splitlines():
        for u in _urls(linea):
            if u in vistos or any(r in u.lower() for r in REDES):
                continue
            vistos.add(u)
            titulo = re.sub(r"[:\-–•*\s]*" + re.escape(u) + r".*$", "", linea).strip(" -–•*:") or u
            enlaces.append((titulo[:80], u))
    enlaces.sort(key=lambda e: "github.com" not in e[1])
    caps = [(int(c.get("start_time") or 0), str(c.get("title") or "").strip()) for c in (d.get("chapters") or [])]
    return enlaces, [c for c in caps if c[1]]


def numero(nombre):
    """'001. X' -> '1', '1.5 X' -> '1.5', '02.txt' -> '2', 'X' -> None."""
    m = re.match(r"\s*(\d+(?:\.\d+)?)(?=[\s._-]|$)", nombre)
    if not m:
        return None
    partes = m.group(1).split(".")
    if len(partes) == 2 and partes[1] == "":
        partes = partes[:1]
    return ".".join(str(int(p)) for p in partes if p != "")


def _limpio(nombre):
    """'001. @RecursosCompartidos Enlace-a-Gist.url' -> 'Enlace a Gist'."""
    n = os.path.splitext(nombre)[0]
    n = re.sub(r"^\s*\d+(\.\d+)?\.?\s*", "", n)
    n = re.sub(r"@\w+\s*", "", n)
    return re.sub(r"[-_]+", " ", n).strip() or nombre


def _urls(texto):
    return [u.rstrip(".,;") for u in URL.findall(texto) if not any(s in u.lower() for s in SPAM)]


def _es_codigo(nombre):
    n = nombre.lower()
    if os.path.basename(n) in ("apuntes.md", "resumen.md", "tarjetas.md", "indice.md"):
        return False  # lo que genera este mismo sistema (en un video de YouTube conviven en la carpeta)
    if n.endswith(".info.json") or os.path.basename(n).startswith(("subtitulos.", ".")):
        return False  # metadatos de YouTube / archivos de este sistema, no código del curso
    if os.path.basename(n) in SALTAR_ARCH or ".min." in n:
        return False
    return any(n.endswith(e) for e in CODIGO)


def _leer_texto(datos):
    if b"\0" in datos[:4000]:
        return None
    return datos.decode("utf-8", errors="replace")


def archivos_de_codigo(ruta):
    """[(nombre relativo, texto)] de un archivo de código, un zip o una carpeta."""
    salida = []
    if ruta.lower().endswith(".zip"):
        try:
            with zipfile.ZipFile(ruta) as z:
                for info in z.infolist():
                    partes = info.filename.split("/")
                    if info.is_dir() or any(p in SALTAR_DIR for p in partes) or not _es_codigo(info.filename):
                        continue
                    if info.file_size > MAX_ARCHIVO:
                        continue
                    t = _leer_texto(z.read(info))
                    if t and t.strip():
                        salida.append((info.filename, t))
        except (zipfile.BadZipFile, OSError, RuntimeError, NotImplementedError):
            pass
    elif os.path.isdir(ruta):
        for raiz, dirs, fs in os.walk(ruta):
            dirs[:] = [d for d in dirs if d not in SALTAR_DIR]
            for f in fs:
                p = os.path.join(raiz, f)
                if _es_codigo(f) and os.path.getsize(p) <= MAX_ARCHIVO:
                    t = _leer_texto(open(p, "rb").read())
                    if t and t.strip():
                        salida.append((os.path.relpath(p, ruta), t))
    elif _es_codigo(ruta) and os.path.getsize(ruta) <= MAX_ARCHIVO:
        t = _leer_texto(open(ruta, "rb").read())
        if t and t.strip():
            salida.append((os.path.basename(ruta), t))
    return salida


def _pdf_texto(ruta, tope=6000):
    if not shutil.which("pdftotext"):
        return ""
    r = subprocess.run(["pdftotext", "-layout", "-l", "15", ruta, "-"], capture_output=True, text=True)
    return r.stdout[:tope] if r.returncode == 0 else ""


def de_la_clase(video):
    """{"clase": [rutas], "lecturas": [rutas], "proyecto": [rutas], "pdf": [rutas], "imagenes": [rutas],
        "enlaces": [(titulo, url)]} para el video de una clase."""
    carpeta = os.path.dirname(os.path.abspath(video))
    num = numero(os.path.basename(video))
    res = {"clase": [], "lecturas": [], "proyecto": [], "pdf": [], "imagenes": [], "enlaces": []}
    try:
        nombres = sorted(os.listdir(carpeta))
    except OSError:
        return res
    nums_video = sorted({numero(f) for f in nombres if os.path.splitext(f)[1].lower() in VIDEO} - {None},
                        key=lambda n: [int(x) for x in n.split(".")])
    clave = lambda n: [int(x) for x in n.split(".")]
    vistos = set()
    for f in nombres:
        p = os.path.join(carpeta, f)
        ext = os.path.splitext(f)[1].lower()
        if not os.path.isfile(p) or ext in VIDEO or ext in (".srt", ".vtt") or f.lower() in SALTAR_ARCH:
            continue
        n = numero(f)
        mia = num is not None and n == num
        if ext in (".url", ".txt", ".webloc"):
            texto = open(p, encoding="utf-8", errors="replace").read(200_000)
            urls = _urls(texto)
            if ext == ".txt" and len(texto) > 300 and n is not None and num is not None and n not in nums_video:
                # lección de lectura (sin video, p. ej. "05.txt" de Academia X): va con el video anterior
                anteriores = [v for v in nums_video if clave(v) < clave(n)]
                if anteriores and anteriores[-1] == num:
                    res["lecturas"].append(p)
                    for u in urls:
                        if u not in vistos:
                            vistos.add(u)
                            res["enlaces"].append((f"Lectura {f}", u))
                continue
            if f.lower().startswith(("external-links", "external-assets-links")) or (
                    "@" in f and "external" in f.lower()):
                # "001 Titulo\nhttps://…" por bloques: solo los de esta clase
                for bloque in re.split(r"\n\s*\n", texto):
                    lineas = [l.strip() for l in bloque.strip().splitlines() if l.strip()]
                    if len(lineas) >= 2 and num is not None and numero(lineas[0]) == num:
                        for u in _urls("\n".join(lineas[1:])):
                            if u not in vistos:
                                vistos.add(u)
                                res["enlaces"].append((_limpio(lineas[0]), u))
            elif urls and mia:
                for u in urls:
                    if u not in vistos:
                        vistos.add(u)
                        res["enlaces"].append((_limpio(f), u))
            continue
        if ext == ".pdf":
            if mia:
                res["pdf"].append(p)
            elif n is None:  # material de toda la sección: se lista, no va a cada prompt
                res["proyecto"].append(p)
        elif ext in (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"):
            if mia:
                res["imagenes"].append(p)
        elif ext == ".zip" or _es_codigo(f):
            if PROYECTO.search(f) or n is None:
                res["proyecto"].append(p)   # el proyecto terminado de la sección (o material sin número)
            elif mia:
                res["clase"].append(p)      # el código de OTRA clase no se usa
    return res


def _palabras(texto):
    return set(re.findall(r"[A-Za-z_][A-Za-z0-9_]{3,}", texto))


def codigo_para_ia(rec, texto_pantalla="", tope=14000):
    """Texto con el código del curso para el prompt (o ""). Primero el de la clase (exacto); después,
    del proyecto, los archivos que más palabras comparten con lo que se ve en pantalla."""
    partes, usado = [], 0

    def agregar(titulo, nombre, texto):
        nonlocal usado
        bloque = f"--- {titulo}: {nombre} ---\n{texto.strip()}\n"
        if usado + len(bloque) > tope:
            bloque = bloque[:max(0, tope - usado)]
        if bloque:
            partes.append(bloque)
            usado += len(bloque)

    for ruta in rec["clase"]:
        for nombre, t in archivos_de_codigo(ruta):
            agregar("CÓDIGO DE ESTA CLASE (exacto)", f"{os.path.basename(ruta)} › {nombre}", t)
    for ruta in rec["lecturas"]:
        agregar("LECTURA DEL CURSO (va con esta clase)", os.path.basename(ruta),
                open(ruta, encoding="utf-8", errors="replace").read())
    for ruta in rec["pdf"]:
        t = _pdf_texto(ruta)
        if t.strip():
            agregar("PDF DEL CURSO", os.path.basename(ruta), t)
    pantalla = _palabras(texto_pantalla)
    if pantalla and usado < tope:
        candidatos = []
        for ruta in rec["proyecto"]:
            for nombre, t in archivos_de_codigo(ruta):
                comunes = len(_palabras(t) & pantalla)
                if comunes >= 5:
                    candidatos.append((comunes, os.path.basename(ruta), nombre, t))
        for _, zipname, nombre, t in sorted(candidatos, reverse=True)[:6]:
            agregar("PROYECTO TERMINADO (más avanzado que esta clase)", f"{zipname} › {nombre}", t)
    return "\n".join(partes)


def copiar_a_clase(rec, carpeta_clase):
    """Copia el código, PDFs, imágenes y lecturas DE LA CLASE a <clase>/codigo-del-curso/ (los zips,
    descomprimidos sin .git ni node_modules). Devuelve la lista de rutas relativas a la clase."""
    destino = os.path.join(carpeta_clase, "codigo-del-curso")
    hechos = []
    for ruta in rec["clase"] + rec["lecturas"] + rec["pdf"] + rec["imagenes"]:
        base = os.path.basename(ruta)
        if ruta.lower().endswith(".zip"):
            sub = os.path.join(destino, _limpio(base))
            archivos = archivos_de_codigo(ruta)
            raices = {n.split("/")[0] for n, _ in archivos}
            if len(raices) == 1 and all("/" in n for n, _ in archivos) and \
                    next(iter(raices)).lower() not in CARPETAS_COMUNES:  # zip con la carpeta del proyecto: sin repetirla
                sub = os.path.join(destino, raices.pop())
                archivos = [(n.split("/", 1)[1], t) for n, t in archivos]
            for nombre, t in archivos:
                p = os.path.normpath(os.path.join(sub, nombre))
                if not p.startswith(sub + os.sep):  # zip con rutas raras (../): no se escribe fuera
                    continue
                os.makedirs(os.path.dirname(p), exist_ok=True)
                with open(p, "w", encoding="utf-8") as h:
                    h.write(t)
                hechos.append(os.path.relpath(p, carpeta_clase))
        else:
            os.makedirs(destino, exist_ok=True)
            p = os.path.join(destino, re.sub(r"@\w+\s*", "", base).strip())
            if os.path.getsize(ruta) <= 30_000_000:
                shutil.copy2(ruta, p)
                hechos.append(os.path.relpath(p, carpeta_clase))
    return hechos


def seccion_md(rec, copiados):
    """Sección "📎 Recursos de la clase" para apuntes.md (o "")."""
    L = []
    if copiados:
        L += ["**💾 Archivos del profe** (copiados en `codigo-del-curso/`):", ""]
        L += [f"- [{os.path.relpath(c, 'codigo-del-curso')}](<{c}>)" for c in copiados[:40]]
        if len(copiados) > 40:
            L += [f"- … y {len(copiados) - 40} más en `codigo-del-curso/`"]
        L += [""]
    if rec["enlaces"]:
        L += ["**🔗 Enlaces:**", ""] + [f"- [{t}]({u})" for t, u in rec["enlaces"]] + [""]
    if rec["proyecto"]:
        L += ["**📦 Proyecto completo de la sección** (código terminado):", ""]
        L += [f"- [{os.path.basename(p)}](<file://{p}>)" for p in rec["proyecto"]] + [""]
    return ("## 📎 Recursos de la clase\n\n" + "\n".join(L)) if L else ""


def main():
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    if a[0] == "--curso":
        totales = {"clase": 0, "lecturas": 0, "proyecto": 0, "pdf": 0, "imagenes": 0, "enlaces": 0}
        con = n = 0
        for raiz, dirs, fs in os.walk(a[1]):
            dirs[:] = [d for d in dirs if d not in {"capturas", "todas-las-capturas", "capturas-clave", "capturas-esenciales"} | SALTAR_DIR]
            for f in sorted(fs):
                if os.path.splitext(f)[1].lower() in VIDEO and not re.search(r"\.(es|en)\.\w+$", f):
                    n += 1
                    r = de_la_clase(os.path.join(raiz, f))
                    con += any(r[k] for k in ("clase", "lecturas", "enlaces", "pdf"))
                    for k in totales:
                        totales[k] += len(r[k])
        print(f"{n} clases, {con} con recursos propios · {totales}")
        return
    r = de_la_clase(a[0])
    for k, v in r.items():
        print(f"{k}: {v}")
    print(codigo_para_ia(r, " ".join(a[1:]))[:3000])


if __name__ == "__main__":
    main()
