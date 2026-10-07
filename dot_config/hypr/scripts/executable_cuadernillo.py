#!/usr/bin/env python3
"""Arma el cuadernillo de apuntes de una clase: capturas importantes + lo que dijo el profe
+ resumen por temas hecho con IA (Claude por defecto; OpenCode con APUNTES_MOTOR=opencode).

    cuadernillo.py <carpeta_de_capturas> [--video clase.mp4] [--titulo T] [--sin-ia] [--forzar]
    cuadernillo.py --indice <carpeta capturas/ del curso>     # arma INDICE.md de todas las clases

Resultado: <carpeta_de_capturas>/apuntes.md (se ve en Obsidian, VS Code o cualquier visor
de Markdown). Los subtítulos se buscan en el video (pistas internas), al lado del video
(clase.es.srt / clase.en.srt) o en la carpeta de capturas (subtitulos.es.srt de YouTube).
"""
import argparse
import collections
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import time

import numpy as np
from PIL import Image

sys.stdout.reconfigure(line_buffering=True)  # que el log del curso se vea al momento
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from progreso import reportar  # barrita de progreso (no hace nada si no se pidió)
spec = importlib.util.spec_from_file_location("ac", os.path.join(AQUI, "auto-captura.py"))
ac = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ac)

CAPTURAS_A_LA_VISTA = 4   # capturas visibles por sección (el resto queda plegado)
TOLERANCIA_SUPERADA = 120  # pedazos de fila sin cubrir tolerados (~2 líneas: mouse, un número que cambió)


# ---------------------------------------------------------------- tiempos ----
def a_segundos(texto):
    partes = [float(p) for p in texto.replace(",", ".").split(":")]
    while len(partes) < 3:
        partes.insert(0, 0.0)
    h, m, s = partes
    return h * 3600 + m * 60 + s


def hms(seg):
    seg = int(seg)
    return f"{seg // 3600:d}:{seg % 3600 // 60:02d}:{seg % 60:02d}" if seg >= 3600 else f"{seg // 60:d}:{seg % 60:02d}"


def listar_capturas(carpeta):
    """[(nombre, segundo)] en orden. Capturas nuevas: 0012.webp + su minuto en .minutos.tsv;
    viejas: el minuto en el nombre (0012_01-23-45.png)."""
    minutos = {}
    try:
        for linea in open(os.path.join(carpeta, ac.MINUTOS), encoding="utf-8"):
            nombre, _, marca = linea.rstrip("\n").partition("\t")
            seg = tiempo_de_captura(f"0_{marca}.png")
            if seg is not None:
                minutos[nombre] = seg
    except OSError:
        pass
    salida = []
    for f in os.listdir(carpeta):
        seg = minutos.get(f) if f in minutos else tiempo_de_captura(f)
        if seg is not None and os.path.isfile(os.path.join(carpeta, f)):
            salida.append((f, seg))
    return sorted(salida, key=lambda x: int(re.match(r"\d+", x[0]).group()))


def tiempo_de_captura(nombre):
    """0012_01-23-45.webp -> 5025 s (minuto del video). También .png (capturas viejas)."""
    m = re.match(r"\d+_(\d\d)-(\d\d)-(\d\d)\.(?:webp|png)$", nombre)
    return int(m[1]) * 3600 + int(m[2]) * 60 + int(m[3]) if m else None


# ------------------------------------------------------------- subtítulos ----
def leer_srt(texto):
    """Lista de (inicio, fin, texto) sin etiquetas y sin las repeticiones de los subtítulos
    automáticos de YouTube (cada línea aparece dos veces, "rodando")."""
    cues = []
    for bloque in re.split(r"\n\s*\n", texto.replace("\r", "")):
        lineas = [l for l in bloque.strip().split("\n") if l.strip()]
        for k, l in enumerate(lineas):
            m = re.match(r"(\d+:\d\d:\d\d[,.]\d+)\s*-->\s*(\d+:\d\d:\d\d[,.]\d+)", l)
            if m:
                txt = " ".join(lineas[k + 1:])
                txt = re.sub(r"<[^>]+>|\{[^}]+\}", "", txt)
                txt = re.sub(r"\s+", " ", txt).strip()
                if txt:
                    cues.append((a_segundos(m[1]), a_segundos(m[2]), txt))
                break
    # quitar repeticiones: si un subtítulo empieza con el final del anterior, dejar solo lo nuevo
    limpio, anterior = [], ""
    for ini, fin, txt in cues:
        if txt == anterior:
            continue
        if anterior and txt.startswith(anterior):
            nuevo = txt[len(anterior):].strip()
        else:
            nuevo = txt
            for k in range(min(len(anterior), len(txt)), 10, -1):  # solapamiento parcial
                if anterior.endswith(txt[:k]):
                    nuevo = txt[k:].strip()
                    break
        if nuevo:
            limpio.append((ini, fin, nuevo))
        anterior = txt
    return limpio


def buscar_subtitulos(carpeta, video):
    """Devuelve {"es": cues, "en": cues} con lo que encuentre."""
    subs = {}
    candidatos = {"es": [], "en": []}
    import glob
    for idioma in ("es", "en"):
        # YouTube: subtitulos.es.srt, subtitulos.en-orig.srt...
        for ext in ("srt", "vtt"):  # YouTube a veces deja .vtt sin convertir
            candidatos[idioma] += sorted(glob.glob(os.path.join(glob.escape(carpeta), f"subtitulos.{idioma}*.{ext}")), key=len)
        if video:
            base = re.sub(r"\.(es|en)$", "", os.path.splitext(video)[0])
            candidatos[idioma] += [f"{base}.{idioma}.srt", f"{base}.{idioma}.vtt"]
    for idioma, rutas in candidatos.items():
        for r in rutas:
            if os.path.isfile(r):
                subs[idioma] = leer_srt(open(r, encoding="utf-8", errors="replace").read())
                break
    if video and os.path.isfile(video):
        for idioma, codigo in (("es", "spa"), ("en", "eng")):
            if idioma in subs:
                continue
            r = subprocess.run(["ffmpeg", "-v", "error", "-i", video, "-map", f"0:s:m:language:{codigo}",
                                "-f", "srt", "-"], capture_output=True)
            if r.returncode == 0 and r.stdout.strip():
                subs[idioma] = leer_srt(r.stdout.decode("utf-8", errors="replace"))
    return {k: v for k, v in subs.items() if v}


def texto_entre(cues, ini, fin):
    return " ".join(t for a, b, t in cues if ini <= a < fin)


def parrafos(cues, cada=45):
    """Agrupa subtítulos en párrafos de ~45 s: [(inicio, texto)]."""
    out, actual, t0 = [], [], None
    for a, b, t in cues:
        if t0 is None:
            t0 = a
        actual.append(t)
        if a - t0 >= cada and re.search(r"[.?!]$", t):
            out.append((t0, " ".join(actual)))
            actual, t0 = [], None
    if actual:
        out.append((t0, " ".join(actual)))
    return out


# ---------------------------------------------------------------- capturas ---
def detectar_webcam(det, reducidas):
    """Zona que se mueve siempre (la cara del profe): bloques que cambian aun entre capturas
    donde el resto de la pantalla casi no cambió. En un curso de diapositivas cambia todo de
    una captura a otra, y eso NO es una webcam (por eso se miran solo los pares "quietos").
    `reducidas` puede ser una lista o un generador (se recorre una sola vez, sin guardarlas)."""
    suma, quietos, anterior, vacia = None, 0, None, None
    for r in reducidas:
        if anterior is not None:
            c = det._cambios(anterior, r)
            if vacia is None:
                vacia = np.zeros(c.shape, dtype=bool)
                suma = np.zeros(c.shape)
            if c.mean() < 0.15:
                suma += c
                quietos += 1
        anterior = r
    if quietos < 5:
        return vacia if vacia is not None else np.zeros((1, 1), dtype=bool)
    candidata = suma / quietos > 0.6
    # una webcam es una mancha compacta (10+ bloques juntos: al menos la cara), no bloquecitos
    # sueltos (números que cambian de una diapositiva a otra)
    webcam = np.zeros_like(vacia)
    for m in det._manchas(candidata):
        if len(m) >= 10:
            for b in m:
                webcam[b] = True
    if not webcam.any() or webcam.mean() > 0.3:  # nada, o demasiado grande para ser una webcam
        return vacia
    return det._dilatar(det._dilatar(webcam))


def elegir_capturas(carpeta):
    """Marca cuáles capturas son importantes: una captura "superada" (todo lo que muestra
    sigue en alguna de las 2 siguientes, porque el profe siguió escribiendo sobre lo mismo)
    no va a la vista. Devuelve [(nombre, segundo, importante, novedad)].
    Carga pocas capturas a la vez (un curso de 8 h tiene miles: no entran todas en memoria)."""
    lista = listar_capturas(carpeta)
    nombres = [f for f, _ in lista]
    segundo = dict(lista)
    if not nombres:
        return []
    det = ac.Detector(ac.leer_conf())

    def reducir(i):
        return det._reducir(Image.open(os.path.join(carpeta, nombres[i])))

    reportar(0, "apuntes", "buscando la webcam")
    webcam = detectar_webcam(det, (reducir(i) for i in range(len(nombres))))
    if webcam.shape == (1, 1):
        webcam = np.zeros(det._cambios(reducir(0), reducir(0)).shape, dtype=bool)
    cache = {}  # i -> (reducida, resumen): solo las que hacen falta ahora

    def cargar(i):
        if i not in cache:
            r = reducir(i)
            cache[i] = (r, det._resumen(r))
        return cache[i]

    def sin_cubrir(i, vecinos):
        det.historial = collections.deque([cargar(j) for j in vecinos], maxlen=len(vecinos) + 1)
        det.parpadeo, det.puntero = webcam, np.zeros_like(webcam)
        r = cargar(i)[0]
        mapa = np.zeros((r.shape[0], r.shape[1] // 160), dtype=bool)
        det._ya_guardada(r, mapa)
        return int((~mapa).sum())

    salida, ultimas = [], []
    for i, f in enumerate(nombres):
        if i % 20 == 0:
            reportar(10 + 50 * i / len(nombres), "apuntes", f"eligiendo capturas ({i}/{len(nombres)})")
        siguientes = [j for j in (i + 1, i + 2) if j < len(nombres)]
        # superada: lo que muestra sigue en las 2 siguientes, salvo ~2 líneas (el profe siguió
        # escribiendo, re-ejecutó una celda, movió el mouse). Dos diapositivas distintas
        # difieren en mucho más que eso, así que las dos quedan.
        superada = bool(siguientes) and sin_cubrir(i, siguientes) <= TOLERANCIA_SUPERADA
        novedad = sin_cubrir(i, ultimas[-2:]) if ultimas else 10 ** 6
        if not superada:
            ultimas.append(i)
        # olvidar lo que ya no se va a usar (quedan la actual, las 2 siguientes y las 2 últimas elegidas)
        for k in [k for k in cache if k < i and k not in ultimas[-2:]]:
            del cache[k]
        salida.append((f, segundo[f], not superada, novedad))
    return salida


# -------------------------------------------------------------------- OCR ----
def leer_pantallas(carpeta, capturas, cada=240, maximo=60):
    """Lee el texto (código, diapositivas) de la última captura importante de cada tramo de
    ~4 min: es el estado final de lo que se mostró. Devuelve [(segundo, texto)]."""
    if not shutil.which("tesseract"):
        return []
    langs = subprocess.run(["tesseract", "--list-langs"], capture_output=True, text=True).stdout.split()
    lang = "+".join(l for l in ("eng", "spa") if l in langs)
    if not lang:
        return []
    tramos = {}
    for f, t, imp, _ in capturas:
        if imp:
            tramos[t // cada] = (f, t)  # queda la última de cada tramo
    if len(tramos) > maximo:
        elegidos = sorted(tramos)
        tramos = {k: tramos[k] for k in elegidos[::-(-len(elegidos) // maximo)]}
    import tempfile
    from concurrent.futures import ThreadPoolExecutor

    def ocr(item):
        f, t = item
        im = Image.open(os.path.join(carpeta, f)).convert("L")
        im = im.resize((im.width * 2, im.height * 2))
        with tempfile.NamedTemporaryFile(suffix=".png") as tmp:
            im.save(tmp.name)
            r = subprocess.run(["tesseract", tmp.name, "-", "-l", lang, "--psm", "6"],
                               capture_output=True, text=True, env=env_ocr)
        lineas = [l.rstrip() for l in r.stdout.splitlines() if len(l.strip()) > 2]
        return t, "\n".join(lineas)

    # Varios tesseract a la vez, cada uno con 1 hilo (OpenMP con varios procesos en paralelo
    # se pisa y va más lento). Laptop i7-1255U (12 hilos): 8 a la vez; OCR_HILOS lo cambia.
    env_ocr = dict(os.environ, OMP_THREAD_LIMIT="1")
    hilos = int(os.environ.get("OCR_HILOS", "0")) or max(1, min(8, (os.cpu_count() or 4) - 2))
    with ThreadPoolExecutor(max_workers=hilos) as ex:
        return sorted(x for x in ex.map(ocr, sorted(tramos.values(), key=lambda x: x[1])) if x[1])


# --------------------------------------------------------------------- IA ----
PROMPT = """Eres un profesor experto que arma APUNTES DE ESTUDIO en español a partir de la transcripción de una clase en video.
El alumno quiere estudiar RÁPIDO: lo importante, completo pero sin relleno. Nada de "en este video el profe dice...": escribe directo el contenido (qué es, cómo funciona, por qué, cómo se usa).

Clase: {titulo}
Duración: {duracion}

{transcripcion}{pantallas}
Responde SOLO con un objeto JSON válido (sin ``` ni texto extra) con esta forma:
{{
  "resumen": ["5 a 8 ideas clave de toda la clase, una frase cada una"],
  "conceptos": [{{"termino": "nombre", "definicion": "1-2 frases claras"}}],
  "secciones": [
    {{"inicio": "h:mm:ss", "titulo": "tema de la sección (corto)",
      "puntos": ["3 a 7 puntos esenciales: qué se hace, por qué, detalles técnicos que importan"],
      "lenguaje": "lenguaje del código (python, javascript, bash, ...) o cadena vacía",
      "codigo": "el código clave de la sección, corto (hasta ~25 líneas). Usa el código REAL del texto de pantalla cuando exista (corrigiendo errores de lectura e indentación). Si la sección no tiene código, cadena vacía"}}
  ],
  "practica": ["3 a 6 ejercicios concretos para practicar lo de la clase, de fácil a difícil"],
  "errores_comunes": ["0 a 5 errores o trampas típicas que se mencionan (si no hay, lista vacía)"],
  "corto": {{
    "idea": "la idea central de la clase en UNA frase",
    "esencial": ["4 a 8 cosas que hay que llevarse, una frase corta cada una"],
    "chuleta": [{{"quiero": "qué quiero hacer (corto)", "como": "cómo se hace: comando, función o sintaxis en `código`"}}],
    "codigo": [{{"titulo": "para qué sirve", "lenguaje": "javascript, python, bash...", "codigo": "hasta ~12 líneas"}}],
    "mapa": [{{"inicio": "h:mm:ss", "tema": "bloque grande de la clase (corto)"}}],
    "preguntas": [{{"pregunta": "pregunta para autoevaluarse", "respuesta": "respuesta corta"}}]
  }}
}}

Reglas:
- Secciones = temas reales de la clase (una cada 5-15 minutos aprox.; en videos cortos, menos), en orden, cubriendo TODO el video. "inicio" debe ser una marca de tiempo que aparezca en la transcripción o en el texto de pantalla.
- 6 a 12 conceptos. Términos técnicos en su forma original (backpropagation, tensor, loss...) con la explicación en español.
- Corrige errores obvios de la transcripción automática (nombres de funciones, términos técnicos).
- Si agregas algo que NO se dice ni se ve en la clase (un complemento útil), márcalo con "(extra)" al final del punto.
- "corto" es una hoja de repaso MUCHO más corta (3-5 minutos de lectura): "chuleta" 4 a 12 filas con lo más usado en la práctica; "codigo" 0 a 3 fragmentos que resumen la clase; "mapa" 3 a 8 bloques que agrupen las secciones; "preguntas" 3 a 6, de entender (por qué / qué pasa si), no de memorizar nombres.
- Todo en español, conciso, preciso."""

# Modelo para los apuntes: Sonnet gasta bastante menos cuota que el modelo por defecto de la
# cuenta y resume muy bien. Para un curso difícil: APUNTES_MODELO=opus (o "" = el de la cuenta).
MODELO = os.environ.get("APUNTES_MODELO", "sonnet")

# Motor de IA: "claude" (por defecto) u "opencode" (suscripción OpenCode Go, p.ej. Kimi K3).
# Con opencode el modelo se elige con APUNTES_MODELO_OPENCODE (formato proveedor/modelo).
MOTOR = os.environ.get("APUNTES_MOTOR", "claude")
# Lista separada por comas: se usa el primero y, si falla, el siguiente. El límite de OpenCode Go es del
# PLAN (ventana móvil de ~5 h + semanal + mensual), no de cada modelo: cambiar de modelo Go no lo evita,
# así que por defecto solo va el más barato (kimi-k3 cuesta ~10x más y agotó la ventana en las pruebas).
# Los "opencode/...-free" (Zen) no sirven desde la CLI ("free tier can only be used from within OpenCode"), pero
# opencode-go/longcat-2.5-preview-free sí funciona y no gastó la ventana de Go (estaba al 100 %).
MODELOS_OPENCODE = [m.strip() for m in os.environ.get(
    "APUNTES_MODELO_OPENCODE", "opencode-go/longcat-2.5-preview-free,opencode-go/deepseek-v4-flash",
).split(",") if m.strip()]
MODELO_OPENCODE = MODELOS_OPENCODE[0] if MODELOS_OPENCODE else ""


def nombre_motor():
    """Etiqueta para los mensajes: "Claude (sonnet)" u "OpenCode (opencode-go/kimi-k3)"."""
    if MOTOR == "opencode":
        return f"OpenCode ({MODELO_OPENCODE or 'modelo de la cuenta'})"
    return f"Claude ({MODELO or 'modelo de la cuenta'})"


def cargar_resumen_corto():
    """resumen-corto.py (el nombre con guion no se puede importar directo)."""
    spec = importlib.util.spec_from_file_location("resumen_corto", os.path.join(AQUI, "resumen-corto.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def idioma_original(carpeta):
    """"es"/"en" si se sabe el idioma original del video (subtítulos "-orig" de YouTube o
    .idioma), o None (p. ej. un video local doblado .es.mp4: no hay cómo saberlo)."""
    import glob
    for idioma in ("es", "en"):
        if glob.glob(os.path.join(glob.escape(carpeta), f"subtitulos.{idioma}-orig.*")):
            return idioma
    try:
        idioma = open(os.path.join(carpeta, ".idioma"), encoding="utf-8").read().strip()[:2]
        return idioma if idioma in ("es", "en") else None
    except OSError:
        return None


def subs_para_claude(carpeta, subs):
    """Los subtítulos del idioma ORIGINAL: la traducción automática confunde términos (en un
    curso en inglés, "xp" por exp; en uno en español, su "inglés" es una traducción). Si no se
    sabe el original, el inglés (videos doblados de cursos en inglés)."""
    orig = idioma_original(carpeta)
    return (subs.get(orig) if orig else None) or subs.get("en") or subs.get("es") or []


def ruta_claude():
    """El claude que de verdad funciona. Ojo: puede haber instalaciones viejas rotas en el PATH
    (ej. /usr/bin/claude de npm, que solo dice "native binary not installed")."""
    candidatos = [os.path.expanduser("~/.local/bin/claude"), shutil.which("claude"), "/usr/local/bin/claude"]
    for c in dict.fromkeys(x for x in candidatos if x):
        try:
            r = subprocess.run([c, "--version"], capture_output=True, text=True, timeout=30)
            if r.returncode == 0 and "Claude Code" in r.stdout:
                return c
        except (OSError, subprocess.TimeoutExpired):
            continue
    raise FileNotFoundError("no se encontró un 'claude' que funcione")


def pedir_a_claude(titulo, duracion, cues, pantallas):
    lineas = [f"[{hms(t)}] {txt}" for t, txt in parrafos(cues, cada=30)]
    transcripcion = ("Transcripción con marcas de tiempo [h:mm:ss]:\n<<<\n" + "\n".join(lineas) + "\n>>>\n"
                     if lineas else "(No hay transcripción del audio: arma los apuntes con lo que se ve en pantalla.)\n")
    extra = ""
    if pantallas:
        extra = ("\nTexto leído de la PANTALLA (OCR, puede tener errores de lectura) en algunos momentos;"
                 " sirve para el código exacto y los datos que se ven:\n<<<\n"
                 + "\n\n".join(f"[{hms(t)}]\n{txt}" for t, txt in pantallas) + "\n>>>\n")
    prompt = PROMPT.format(titulo=titulo, duracion=hms(duracion), transcripcion=transcripcion,
                           pantallas=extra)
    for intento in range(2):
        texto = consultar_ia(prompt)
        try:
            datos = json.loads(texto[texto.index("{"):texto.rindex("}") + 1])
            if datos.get("secciones"):
                return datos
        except (ValueError, TypeError, json.JSONDecodeError):
            pass
        print(f"  (respuesta de Claude inválida, intento {intento + 1})", file=sys.stderr)
    return None


ESPERA_CUOTA = 600  # s entre reintentos cuando se agotó la cuota de Claude
ESPERA_CUOTA_OC = 1200  # s entre reintentos cuando se agotó la ventana móvil (~5 h) de OpenCode Go
ESPERA_CUOTA_MAX = float(os.environ.get("APUNTES_ESPERA_MAX_H", "6")) * 3600  # la cuota se renueva cada ~5 h


def cuota_agotada(salida):
    """¿Claude contestó que se alcanzó el límite de uso? ("You've hit your session limit · resets 11pm")."""
    t = salida.lower()
    return ("limit" in t and ("hit your" in t or "resets" in t)) or "rate_limit" in t or "usage limit" in t


def llamar_claude(cmd, prompt, esperar=time.sleep):
    """Texto de la respuesta de `claude -p --output-format json`, o None si falló.
    Si se agotó la cuota NO sigue sin IA: espera a que se renueve y reintenta (hasta
    ESPERA_CUOTA_MAX). Así una playlist larga no deja clases sin resumen."""
    esperado = 0
    while True:
        r = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=1800)
        try:
            d = json.loads(r.stdout)
            texto, error = str(d.get("result", "")), bool(d.get("is_error"))
        except (ValueError, AttributeError):
            texto, error = r.stdout, True
        if not cuota_agotada(texto + " " + r.stderr if error or r.returncode else ""):
            return None if error else texto
        if esperado >= ESPERA_CUOTA_MAX:
            print("  (la cuota de Claude sigue agotada: sigo sin IA)", file=sys.stderr)
            return None
        aviso = texto.strip().splitlines()[0][:80] if texto.strip() else "límite de uso"
        print(f"  ⏳ Cuota de Claude agotada ({aviso}); reintento en {ESPERA_CUOTA // 60} min", file=sys.stderr)
        reportar(75, "apuntes", "⏳ esperando la cuota de Claude")
        esperar(ESPERA_CUOTA)
        esperado += ESPERA_CUOTA


def ruta_opencode():
    c = shutil.which("opencode")
    if not c:
        raise FileNotFoundError("no se encontró 'opencode' en el PATH")
    return c


def llamar_opencode(prompt, esperar=time.sleep, max_espera=None):
    """Texto de la respuesta de `opencode run`, o None si falló. Prueba los modelos de
    MODELOS_OPENCODE en orden; si TODOS dicen "usage limit" (el límite de Go es del plan, no del
    modelo, y se renueva por ventanas) espera y reintenta, como con Claude."""
    # --standalone: servidor propio (el servicio de fondo se cuelga con prompts largos y comparte
    # estado entre llamadas). El prompt va por stdin: como argumento, 5 de 5 llamadas largas se colgaron.
    esperado = 0
    while True:
        agotados = 0
        for modelo in MODELOS_OPENCODE or [""]:
            cmd = [ruta_opencode(), "run", "--standalone", "--agent", "apuntes"] + (["--model", modelo] if modelo else [])
            try:
                r = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=900)
            except (OSError, subprocess.TimeoutExpired) as e:
                print(f"  (opencode {modelo} falló: {e})", file=sys.stderr)
                continue
            salida = (r.stdout or "") + " " + (r.stderr or "")
            if r.returncode == 0 and r.stdout.strip():
                return r.stdout
            if cuota_agotada(salida) or "insufficient" in salida.lower():
                agotados += 1
                print(f"  (opencode {modelo}: cuota agotada, pruebo el siguiente)", file=sys.stderr)
                continue
            detalle = re.sub(r"\x1b\[[0-9;]*m", "", salida).strip().replace("\n", " ")[:120]
            print(f"  (opencode {modelo} falló: {detalle or 'sin detalle'})", file=sys.stderr)
        if agotados == len(MODELOS_OPENCODE or [""]):
            marcar_opencode_agotado()
        if agotados < len(MODELOS_OPENCODE or [""]) or esperado >= (ESPERA_CUOTA_MAX if max_espera is None else max_espera):
            return None
        print(f"  ⏳ Cuota de OpenCode Go agotada; reintento en {ESPERA_CUOTA_OC // 60} min", file=sys.stderr)
        reportar(75, "apuntes", "⏳ esperando la cuota de OpenCode")
        esperar(ESPERA_CUOTA_OC)
        esperado += ESPERA_CUOTA_OC


AGOTADO_OC = os.path.expanduser("~/.cache/auto-captura/opencode-agotado")
ENFRIAR_OC = 1800  # s sin tocar OpenCode después de que todos sus modelos dijeron "usage limit"
# Si OpenCode no puede (cuota), se usa Claude con un modelo barato. APUNTES_RESPALDO="" lo desactiva
# (entonces se espera la cuota de OpenCode). APUNTES_RESPALDO_EFFORT=low|medium para bajar el esfuerzo.
RESPALDO = os.environ.get("APUNTES_RESPALDO", "haiku")
RESPALDO_EFFORT = os.environ.get("APUNTES_RESPALDO_EFFORT", "")


def opencode_enfriando():
    try:
        return time.time() - os.path.getmtime(AGOTADO_OC) < ENFRIAR_OC
    except OSError:
        return False


def marcar_opencode_agotado():
    try:
        os.makedirs(os.path.dirname(AGOTADO_OC), exist_ok=True)
        open(AGOTADO_OC, "w").close()
    except OSError:
        pass


def consultar_ia(prompt, modelo=None):
    """Texto de la respuesta del motor configurado (APUNTES_MOTOR=claude|opencode), o None.
    Con claude espera a que se renueve la cuota; el modelo es APUNTES_MODELO salvo que se
    indique otro (practica.py usa PRACTICA_MODELO). Con opencode se usa APUNTES_MODELO_OPENCODE."""
    if MOTOR == "opencode":
        if not RESPALDO:
            return llamar_opencode(prompt)
        texto = None if opencode_enfriando() else llamar_opencode(prompt, max_espera=0)
        if texto is not None:
            return texto
        print(f"  (OpenCode no disponible: uso Claude {RESPALDO} como respaldo)", file=sys.stderr)
        modelo = RESPALDO
        extra = ["--effort", RESPALDO_EFFORT] if RESPALDO_EFFORT else []
        cmd = [ruta_claude(), "-p", "--output-format", "json", "--tools", "", "--strict-mcp-config",
               "--no-session-persistence", "--system-prompt",
               "Eres un asistente que responde exactamente en el formato pedido.", "--model", modelo] + extra
        return llamar_claude(cmd, prompt)
    cmd = [ruta_claude(), "-p", "--output-format", "json", "--tools", "", "--strict-mcp-config",
           "--no-session-persistence", "--system-prompt",
           "Eres un asistente que responde exactamente en el formato pedido."]
    m = MODELO if modelo is None else modelo
    if m:
        cmd += ["--model", m]
    return llamar_claude(cmd, prompt)


# ----------------------------------------------------------------- armado ----
def armar(carpeta, titulo, capturas, subs, datos, duracion):
    cues_es = subs.get("es") or subs.get("en") or []
    idioma_txt = "español" if subs.get("es") else ("inglés" if subs.get("en") else None)
    importantes = [c for c in capturas if c[2]]

    if datos:
        secciones = []
        for s in datos["secciones"]:
            try:
                secciones.append(dict(s, ini=a_segundos(str(s.get("inicio", "0")))))
            except ValueError:
                continue
        secciones.sort(key=lambda s: s["ini"])
        if secciones:
            secciones[0]["ini"] = 0
    else:  # sin IA: una sección cada 10 minutos
        secciones = [{"titulo": f"Minuto {hms(t)}", "ini": t, "puntos": [], "codigo": ""}
                     for t in range(0, int(duracion) + 1, 600)]
    for k, s in enumerate(secciones):
        s["fin"] = secciones[k + 1]["ini"] if k + 1 < len(secciones) else duracion + 1

    L = [f"# 📓 {titulo}", ""]
    L += [f"> ⏱️ **Duración:** {hms(duracion)} · 📸 **Capturas:** {len(importantes)} importantes "
          f"(de {len(capturas)}) · 📚 **Secciones:** {len(secciones)}", ""]
    if datos:
        L += ["## 🎯 Resumen de la clase", ""]
        L += [f"- {p}" for p in datos.get("resumen", [])] + [""]
        if datos.get("conceptos"):
            L += ["## 🧠 Conceptos clave", "", "| Concepto | Qué es |", "|---|---|"]
            L += [f"| **{c.get('termino', '')}** | {c.get('definicion', '')} |" for c in datos["conceptos"]]
            L += [""]
    L += ["## 🗂️ Índice", ""]
    L += [f"{k + 1}. [{s['titulo']}](#{k + 1}-{ancla(s['titulo'])}) · `{hms(s['ini'])}`" for k, s in enumerate(secciones)]
    L += ["", "---", ""]

    for k, s in enumerate(secciones):
        L += [f"## {k + 1}. {s['titulo']}", "", f"⏱️ `{hms(s['ini'])} – {hms(min(s['fin'], duracion))}`", ""]
        L += [f"- {p}" for p in s.get("puntos", [])]
        if s.get("puntos"):
            L += [""]
        if s.get("codigo", "").strip():
            L += [f"```{s.get('lenguaje') or ''}", s["codigo"].strip("\n"), "```", ""]
        caps = [c for c in importantes if s["ini"] <= c[1] < s["fin"]]
        if caps:
            # a la vista: la última de la sección (estado final) + las de más novedad
            elegidas = {caps[-1][0]} | {c[0] for c in sorted(caps[:-1], key=lambda c: -c[3])[:CAPTURAS_A_LA_VISTA - 1]}
            for c in caps:
                if c[0] in elegidas:
                    L += [f"![⏱️ {hms(c[1])}]({c[0]})", f"*⏱️ {hms(c[1])}*", ""]
            resto = [c for c in caps if c[0] not in elegidas]
            if resto:
                L += [f"> [!example]- 📸 Más capturas de esta sección ({len(resto)})"]
                for c in resto:
                    L += [f"> ![⏱️ {hms(c[1])}]({c[0]})", f"> *⏱️ {hms(c[1])}*", ">"]
                L += [""]
        texto = [(t, p) for t, p in parrafos(cues_es) if s["ini"] <= t < s["fin"]]
        if texto:
            L += [f"> [!quote]- 🗣️ Lo que dice el profe ({idioma_txt})"]
            for t, p in texto:
                L += [f"> `{hms(t)}` {p}", ">"]
            L += [""]
        L += ["---", ""]

    if datos:
        if datos.get("errores_comunes"):
            L += ["## ⚠️ Errores comunes", ""] + [f"- {e}" for e in datos["errores_comunes"]] + [""]
        if datos.get("practica"):
            L += ["## 🏋️ Para practicar", ""] + [f"- [ ] {e}" for e in datos["practica"]] + [""]
    else:
        L += ["> [!info] Apuntes sin resumen de IA (solo capturas y transcripción)", ""]
    return "\n".join(L)


def ancla(titulo):
    """Ancla estilo GitHub/Obsidian para el índice."""
    t = titulo.lower()
    t = re.sub(r"[^\w\s-]", "", t)
    return re.sub(r"\s+", "-", t.strip())


def indice(carpeta_capturas, nombre_curso):
    """INDICE.md en la carpeta capturas/: una línea por clase con link a sus apuntes."""
    L = [f"# 🎓 {nombre_curso}", "", "| # | Clase | Idea principal |", "|---|---|---|"]
    clases = sorted(d for d in os.listdir(carpeta_capturas)
                    if os.path.isfile(os.path.join(carpeta_capturas, d, "apuntes.md")))
    for k, d in enumerate(clases, 1):
        idea = ""
        try:
            datos = json.load(open(os.path.join(carpeta_capturas, d, ".apuntes-ia.json"), encoding="utf-8"))
            idea = (datos.get("resumen") or [""])[0]
        except (OSError, ValueError):
            pass
        link = "<" + d + "/apuntes.md>"  # <...> permite espacios en el link
        L.append(f"| {k} | [{d}]({link}) | {idea} |")
    L += ["", f"*{len(clases)} clases con apuntes · generado por cuadernillo.py*", ""]
    with open(os.path.join(carpeta_capturas, "INDICE.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print(f"🗂️ Índice: {os.path.join(carpeta_capturas, 'INDICE.md')} ({len(clases)} clases)")


def main():
    if len(sys.argv) >= 3 and sys.argv[1] == "--indice":
        carpeta = os.path.abspath(sys.argv[2])
        indice(carpeta, os.path.basename(os.path.dirname(carpeta)) if os.path.basename(carpeta) == "capturas"
               else os.path.basename(carpeta))
        return 0
    p = argparse.ArgumentParser()
    p.add_argument("carpeta")
    p.add_argument("--video")
    p.add_argument("--titulo")
    p.add_argument("--sin-ia", action="store_true")
    p.add_argument("--forzar", action="store_true")
    a = p.parse_args()

    carpeta = os.path.abspath(a.carpeta)
    salida = os.path.join(carpeta, "apuntes.md")
    if os.path.exists(salida) and not a.forzar:
        print(f"Ya existe {salida} (usar --forzar para rehacerlo)")
        return 0
    titulo = a.titulo or os.path.basename(carpeta)

    print("📸 Eligiendo capturas importantes…")
    capturas = elegir_capturas(carpeta)
    if not capturas:
        print("No hay capturas con minuto del video en la carpeta")
        return 1
    print(f"   {sum(c[2] for c in capturas)} importantes de {len(capturas)}")

    subs = buscar_subtitulos(carpeta, a.video)
    print(f"🗣️ Subtítulos: {', '.join(subs) or 'ninguno'}")
    duracion = max([capturas[-1][1]] + [c[1] for v in subs.values() for c in v[-1:]])

    datos = None
    try:
        ruta_opencode() if MOTOR == "opencode" else ruta_claude()
    except FileNotFoundError as e:
        print(f"   (sin IA: {e})")
        a.sin_ia = True
    if not a.sin_ia:
        print("🔎 Leyendo el código/texto de la pantalla (OCR)…")
        reportar(60, "apuntes", "leyendo el código de la pantalla")
        # sin subtítulos, la pantalla es la única fuente: se leen más capturas
        pantallas = leer_pantallas(carpeta, capturas, cada=240 if subs else 20)
        print(f"   {len(pantallas)} pantallas leídas")
        if subs or pantallas:
            print(f"🤖 Pidiendo a {nombre_motor()} apuntes + resumen corto…")
            reportar(75, "apuntes", f"{nombre_motor()} armando el resumen")
            datos = pedir_a_claude(titulo, duracion, subs_para_claude(carpeta, subs), pantallas)
        if datos:
            corto = datos.pop("corto", None)
            with open(os.path.join(carpeta, ".apuntes-ia.json"), "w", encoding="utf-8") as f:
                json.dump(datos, f, ensure_ascii=False, indent=1)
            if isinstance(corto, dict) and corto.get("esencial"):
                # el repaso corto viene en la MISMA respuesta: no hace falta otra llamada
                rc = cargar_resumen_corto()
                with open(os.path.join(carpeta, ".resumen-ia.json"), "w", encoding="utf-8") as f:
                    json.dump(corto, f, ensure_ascii=False, indent=1)
                with open(os.path.join(carpeta, "resumen.md"), "w", encoding="utf-8") as f:
                    f.write(rc.armar(titulo, hms(duracion), corto))
                print("⚡ Resumen corto armado en la misma llamada")
        else:
            print("   (sin resumen de IA: se arma solo con capturas y transcripción)")

    reportar(97, "apuntes", "armando el cuadernillo")
    with open(salida, "w", encoding="utf-8") as f:
        f.write(armar(carpeta, titulo, capturas, subs, datos, duracion))
    print(f"📓 Listo: {salida}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
