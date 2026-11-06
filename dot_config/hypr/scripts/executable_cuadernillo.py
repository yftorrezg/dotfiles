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
import glob
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
import capturas_clave as cc  # estado final de cada cosa (OCR + píxeles): las capturas importantes
import transcribir as tr     # Whisper en la GPU para los videos sin subtítulos
import recursos as rec_curso  # código del profe, lecturas y enlaces que trae el curso
spec = importlib.util.spec_from_file_location("ac", os.path.join(AQUI, "auto-captura.py"))
ac = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ac)

CAPTURAS_A_LA_VISTA = 4   # capturas visibles por sección si no hay esenciales (el resto queda plegado)


def n_preguntas(segundos):
    """Preguntas de autoevaluación/tarjetas: 1 (video de menos de 1 min), 2 (menos de 2), de ahí 3 hasta 40 (~3 h)."""
    m = segundos / 60
    return 1 if m < 1 else 2 if m < 2 else max(3, min(40, round(3 + m / 5)))


def n_pretest(segundos):
    """Preguntas del pre-test (SUPER+I): 0 en menos de 3 min (no tiene sentido), si no 3 hasta 10 (~1 h 45)."""
    m = segundos / 60
    return 0 if m < 3 else max(3, min(10, round(3 + m / 15)))


def n_ejercicios(segundos):
    """Ejercicios de "Para practicar": 0 (menos de 2 min), 1 (menos de 5), 2 (menos de 10), de ahí 3 hasta 10."""
    m = segundos / 60
    return 0 if m < 2 else 1 if m < 5 else 2 if m < 10 else max(3, min(14, round(2 + m / 10)))


def n_errores(segundos):
    """Errores comunes: 0 (menos de 2 min), 1 (menos de 5), 2 (menos de 10), de ahí 2 hasta 8."""
    m = segundos / 60
    return 0 if m < 2 else 1 if m < 5 else max(2, min(10, round(2 + m / 15)))


def n_diagramas(segundos):
    """Tope de diagramas mermaid: 1 cada ~20 min (1 a 6)."""
    return max(1, min(6, round(segundos / 60 / 20)))


def rango_diagramas(segundos):
    """Texto para el prompt: en clases largas se piden al menos la mitad del tope (si no, la IA no dibuja ninguno)."""
    hi = n_diagramas(segundos)
    lo = hi // 2 if segundos >= 40 * 60 else 0
    return (f"entre {lo} y {hi}" if lo else f"como máximo {hi}")


def n_vocabulario(segundos):
    """Términos en inglés: 3 hasta 10."""
    return 0 if segundos < 180 else max(3, min(10, round(3 + segundos / 60 / 15)))


def tope_palabras(segundos):
    """Palabras de TODOS los "puntos" juntos: ~25 por minuto de video (mín. 150). Con lo demás (código,
    ejemplos, por qué) los apuntes quedan en ~1/3 del tiempo del video."""
    return int(max(60, round(25 * segundos / 60, -1)))


FORMATO = 4  # v4: relevancia ⭐🔸💤, comentarios 👉 en el código, intuición, tope de lectura; v3: + objetivos, comparativas, solución de ejercicios, vocabulario; v2 del formato de apuntes.md (v2: sin transcripción adentro, ejemplos, diagramas, errores con arreglo)
SISTEMA = ("Eres un profesor experto en Ingeniería en Ciencias de la Computación y un programador senior que "
           "enseña con el tiempo justo: claro, exacto y sin relleno. Respondes exactamente en el formato pedido. "
           "Nunca inventas código, APIs, salidas ni datos: lo que no sale de la clase o no es un hecho técnico "
           "comprobable y estándar, no lo escribes; lo que agregas por tu cuenta lo marcas \"(extra)\".")
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
            m = re.match(r"((?:\d+:)?\d\d:\d\d[,.]\d+)\s*-->\s*((?:\d+:)?\d\d:\d\d[,.]\d+)", l)  # VTT de Udemy: 00:04.320 (sin horas)
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
        if video:  # al lado del video: clase.es.srt (Whisper), clase-es.srt (Udemy), clase.srt…
            al_lado = tr.subtitulos_al_lado(video).get(idioma)
            candidatos[idioma] += [al_lado] if al_lado else []
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


def elegir_clave(carpeta, nombres, segundo):
    """Importantes = capturas clave (capturas_clave.py: OCR + píxeles). Novedad = palabras que no
    estaban en la clave anterior (para elegir cuáles van a la vista). None si no hay OCR
    (o CAPTURAS_CLAVE=0): se usa el método viejo, solo por píxeles."""
    if os.environ.get("CAPTURAS_CLAVE") == "0":
        return None
    reportar(5, "apuntes", "leyendo las capturas (OCR)")
    clave = cc.elegir(carpeta, avisar=lambda k, n: reportar(5 + 50 * k / max(1, n), "apuntes",
                                                            f"leyendo las capturas ({k}/{n})"))
    if clave is None:
        return None
    clave = set(clave)
    cc.esenciales(carpeta)  # la mitad de las clave: son las que quedan a la vista en apuntes.md
    tx = cc.textos(carpeta, nombres) or {}
    salida, anterior = [], collections.Counter()
    for f in nombres:
        p = cc.palabras(tx.get(f, ""))
        novedad = sum((p - anterior).values()) if f in clave else 0
        if f in clave:
            anterior = p
        salida.append((f, segundo[f], f in clave, novedad))
    return salida


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
    clave = elegir_clave(carpeta, nombres, segundo)
    if clave is not None:
        return clave
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
    # si la pantalla de un tramo sigue completa en la del tramo siguiente (el mismo archivo, que
    # siguió creciendo), mandar las dos a la IA es repetir: queda solo la más completa
    tx = cc.textos(carpeta, [f for f, _ in tramos.values()]) if os.environ.get("CAPTURAS_CLAVE") != "0" else None
    if tx:
        orden = sorted(tramos)
        for a, b in zip(orden, orden[1:]):
            pa, pb = cc.palabras(tx[tramos[a][0]]), cc.palabras(tx[tramos[b][0]])
            if sum(pa.values()) >= cc.POCAS_PALABRAS and cc.cobertura(pa, pb) >= cc.COBERTURA:
                del tramos[a]
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
PROMPT = """Arma APUNTES DE ESTUDIO en español de una clase en video (área: programación / ciencias de la computación).
El alumno estudia con poco tiempo: los apuntes deben leerse en ~1/4 de lo que dura el video SIN perder lo que
importa (cada variable, parámetro o línea de código que se explica). Escribe directo el contenido (qué es, cómo
funciona, por qué, cómo se usa); nada de "en este video el profe dice...". No repitas lo mismo en dos lugares:
cada idea va UNA vez, en la sección donde se explica.

Clase: {titulo}
Duración: {duracion}

{transcripcion}{pantallas}
Responde SOLO con un objeto JSON válido (sin ``` ni texto extra) con esta forma:
{{
  "sin_contenido": false,
  "objetivos": ["2 a 4 cosas que el alumno PUEDE HACER al terminar (verbo de acción: escribir, explicar, depurar, elegir entre...)"],
  "resumen": ["3 a 6 ideas clave de toda la clase, una frase cada una"],
  "conceptos": [{{"termino": "nombre", "definicion": "1 frase clara"}}],
  "secciones": [
    {{"inicio": "h:mm:ss", "titulo": "tema de la sección (corto)",
      "relevancia": "diario | a-veces | raro  (diario = clave: se usa seguido O es base para entender lo que sigue)",
      "porque": "UNA línea: el beneficio concreto o el problema que evita (no repitas el título); si no hay nada útil, cadena vacía",
      "puntos": ["1 a 5 puntos (máx. ~20 palabras cada uno), ~20 palabras por cada minuto de la sección: lo que hay que retener, con los términos clave en **negrita**"],
      "lenguaje": "lenguaje del código (python, javascript, sql, bash, ...) o cadena vacía",
      "codigo": "el código clave de la sección (hasta ~25 líneas), el REAL de la clase. Si no tiene código, cadena vacía",
      "linea_a_linea": ["comentarios para el código: '`fragmento EXACTO de una línea del código` → por qué (máx. 12 palabras)'; solo en código de 3+ líneas y solo lo no obvio; 0 a 6"],
      "intuicion": "solo en el concepto MÁS difícil de la clase: la idea con una analogía, 2-3 frases; en las demás secciones cadena vacía",
      "ejemplo": {{"enunciado": "caso concreto", "pasos": ["paso a paso: valores de las variables / qué pasa en cada paso"], "salida": "resultado final"}},
      "diagrama": "diagrama mermaid (flowchart, sequenceDiagram, classDiagram, erDiagram o stateDiagram) o cadena vacía",
      "comparativa": {{"titulo": "X vs Y: cuándo usar cuál", "columnas": ["", "X", "Y"], "filas": [["criterio", "...", "..."]]}}}}
  ],
  "practica": [{{"nivel": "🟢 | 🟡 | 🔴", "enunciado": "ejercicio concreto", "pista": "una pista que no regale la respuesta", "solucion": "la solución (código corto o pasos)"}}],
  "errores_comunes": [{{"error": "el error o la trampa", "porque": "por qué pasa / qué síntoma da", "arreglo": "cómo se evita o corrige"}}],
  "corto": {{
    "idea": "la idea central de la clase en UNA frase",
    "esencial": ["4 a 8 cosas que hay que llevarse, una frase corta cada una"],
    "chuleta": [{{"quiero": "qué quiero hacer (corto)", "como": "cómo se hace: comando, función o sintaxis en `código`"}}],
    "codigo": [{{"titulo": "para qué sirve", "lenguaje": "javascript, python, bash...", "codigo": "hasta ~12 líneas"}}],
    "diagrama": "UN diagrama mermaid que muestre cómo se conectan las piezas de toda la clase, o cadena vacía",
    "mapa": [{{"inicio": "h:mm:ss", "tema": "bloque grande de la clase (corto)"}}],
    "preguntas": [{{"tipo": "porque | que-imprime | error | definicion", "pregunta": "pregunta para autoevaluarse",
                    "lenguaje": "solo si trae código", "codigo": "solo en que-imprime / error: código AUTOCONTENIDO (hasta ~12 líneas: con las definiciones que use y que imprima con console.log / print)",
                    "respuesta": "respuesta corta"}}],
    "pretest": [{{"pregunta": "pregunta DISTINTA de las de 'preguntas'", "respuesta": "respuesta corta"}}]
  }},
  "vocabulario": [{{"en": "término técnico en inglés", "suena": "pronunciación escrita a la española (database → déita-beis)", "es": "qué significa"}}]
}}

Reglas:
- Secciones = temas reales de la clase (una cada 5-15 minutos aprox.; en videos cortos, menos), en orden, cubriendo TODO el video. "inicio" debe ser una marca de tiempo que aparezca en la transcripción o en el texto de pantalla.
- "conceptos" = glosario corto: 4 a 10 términos (hasta 15 si dura más de 1 hora), en su forma original (backpropagation, closure, JOIN...) con la explicación en español. No repitas su definición en los puntos.
- Corrige errores obvios de la transcripción automática (nombres de funciones, términos técnicos).
- Si agregas algo que NO se dice ni se ve en la clase (un complemento útil), márcalo con "(extra)" al final.
- "codigo": usa el del texto de pantalla (corrigiendo errores de lectura e indentación) o el "CÓDIGO DE ESTA CLASE (exacto)" si está. Nunca código inventado que no se vio.
- "relevancia": "diario" = CLAVE: se usa seguido en el trabajo real o es la base para entender lo que viene (en una clase de teoría, el concepto central es "diario"); "a-veces" = útil en casos concretos; "raro" = histórico, obsoleto, de nicho o un desvío del tema (basta saber que existe). Sé honesto y equilibrado: lo central de la clase es "diario", lo accesorio no.
- Los apuntes NO reemplazan al video (el alumno también lo ve): no narres, deja solo lo que hay que retener. Sin relleno ni frases vacías.
- "ejemplo": SOLO en las secciones donde el profe resuelve o ejecuta algo (o donde hay código con una entrada concreta); en las demás, null. La traza sale de lo que pasa en la clase o de ejecutar mentalmente ESE código: valores reales, nada inventado.
- "diagrama": {rango_diag} en toda la clase, donde un dibujo aclara más que el texto (flujo de un algoritmo, request/response, arquitectura, relaciones entre tablas o clases, estados, capas de una red). Mermaid válido: ids sin espacios, textos con espacios entre comillas, sin paréntesis sueltos dentro de [ ]. Si tiene más de 5 cajas usa vertical (flowchart TD) para que se lea en pantalla angosta; el salto de línea es un salto real, no "\\n".
- "practica": EXACTAMENTE {n_ejer} ejercicios de fácil (🟢) a difícil (🔴), que se resuelvan con lo de esta clase y se parezcan a lo que se hace en el trabajo real; la "solucion" es correcta, con el código COMENTADO (por qué de cada paso) o los pasos explicados.
- "comparativa": solo si la sección dura 3+ minutos y el alumno tiene que ELEGIR entre opciones (let/const/var, INNER/LEFT JOIN, lista/tupla, SGD/Adam...), con datos que NO estén ya en los puntos; si no, null.
- "objetivos": concretos y verificables, nada genérico ("entender X" no vale; "escribir una función que..." sí).
- "sin_contenido": true SOLO si la clase no enseña nada técnico (bienvenida, presentación del curso o del profe, despedida, certificado, anuncios, "qué veremos"). Entonces: 1 sola sección con 1-2 puntos, y "objetivos", "practica", "errores_comunes", "vocabulario" y "pretest" vacíos ([]), 1-2 "preguntas"; ignora los EXACTAMENTE de arriba. Si enseña algo técnico, aunque sea corto, va false.
- Con EXACTAMENTE 0 en "practica", "errores_comunes", "vocabulario" o "pretest": lista vacía [].
- Presupuesto: los "puntos" de TODAS las secciones suman como máximo {tope} palabras (un tema por punto, sin repetir lo que ya muestra el código).
- "vocabulario": EXACTAMENTE {n_voc} términos en inglés que se usan en la clase (los que aparecen en código, documentación o mensajes de error), con su pronunciación escrita a la española, nunca en IPA.
- "errores_comunes": EXACTAMENTE {n_err}: errores que de verdad comete un programador con esto, con su síntoma concreto (mensaje de error o comportamiento raro) en "porque". Primero los de la clase; si faltan, clásicos REALES del tema marcados "(extra)". Nunca uno sacado de una mala transcripción ni uno trivial.
- "corto" es una hoja de repaso MUCHO más corta (3-5 minutos de lectura): "chuleta" 4 a 12 filas con lo más usado en la práctica; "codigo" 0 a 3 fragmentos que resumen la clase; "mapa" 3 a 8 bloques que agrupen las secciones.
- "preguntas": EXACTAMENTE {n_preg}, repartidas por TODO el video (al menos una por cada bloque del "mapa"). Mezcla de tipos: ~40 % "porque" (por qué / qué pasa si / cuándo conviene), ~30 % "que-imprime" (código real de la clase con su salida exacta; en clases sin código, "¿qué resultado da...?"), ~20 % "error" (código o situación con un error: ¿cuál es y cómo se arregla?), ~10 % "definicion". De entender, no de memorizar nombres.
- "pretest": EXACTAMENTE {n_pre} preguntas de diagnóstico, distintas de "preguntas", para saber si el alumno ya domina la clase antes de verla.
- Si hay "CÓDIGO DE ESTA CLASE (exacto)", es el código que entregó el profe: el "codigo" de las secciones, de los ejemplos y del repaso debe salir de ahí, tal cual (nombres, valores), en el orden en que se explica en la clase.
- Si hay "PROYECTO TERMINADO", es más avanzado que esta clase: úsalo solo para corregir errores del OCR y nombres; NO pongas código que todavía no se escribió en esta clase.
- Si hay "LECTURA DEL CURSO", es parte de la clase: inclúyela en los apuntes (resumen, conceptos y una sección propia).
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
    # 06/11/2026: deepseek-v4-flash y longcat ya no existen en OpenCode Go (fallaban en silencio)
    "APUNTES_MODELO_OPENCODE", "opencode-go/deepseek-v4.1-flash,opencode-go/gpt-6-luna,opencode-go/claude-haiku-5-5,opencode-go/glm-5.3-flash",
).split(",") if m.strip()]
MODELO_OPENCODE = MODELOS_OPENCODE[0] if MODELOS_OPENCODE else ""


def nombre_motor():
    """Etiqueta para los mensajes: "Claude (sonnet)" u "OpenCode (opencode-go/kimi-k3)"."""
    if MOTOR == "opencode":
        if RESPALDO:
            return f"Claude {RESPALDO} → OpenCode ({MODELO_OPENCODE or 'modelo de la cuenta'})"
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


def pedir_a_claude(titulo, duracion, cues, pantallas, codigo=""):
    lineas = [f"[{hms(t)}] {txt}" for t, txt in parrafos(cues, cada=30)]
    transcripcion = ("Transcripción con marcas de tiempo [h:mm:ss]:\n<<<\n" + "\n".join(lineas) + "\n>>>\n"
                     if lineas else "(No hay transcripción del audio: arma los apuntes con lo que se ve en pantalla.)\n")
    extra = ""
    if pantallas:
        extra = ("\nTexto leído de la PANTALLA (OCR, puede tener errores de lectura) en algunos momentos;"
                 " sirve para el código exacto y los datos que se ven:\n<<<\n"
                 + "\n\n".join(f"[{hms(t)}]\n{txt}" for t, txt in pantallas) + "\n>>>\n")
    prompt = PROMPT.format(titulo=titulo, duracion=hms(duracion), n_preg=n_preguntas(duracion), n_pre=n_pretest(duracion),
                           n_ejer=n_ejercicios(duracion), n_err=n_errores(duracion), n_diag=n_diagramas(duracion),
                           n_voc=n_vocabulario(duracion), tope=tope_palabras(duracion), rango_diag=rango_diagramas(duracion),
                           transcripcion=transcripcion,
                           pantallas=extra + (f"\nMaterial que entrega el curso (recursos.py):\n<<<\n{codigo}\n>>>\n" if codigo else ""))
    for intento in range(2):
        texto = consultar_ia(prompt)
        try:
            datos = json.loads(texto[texto.index("{"):texto.rindex("}") + 1])
            # los modelos débiles a veces mandan secciones sin título: se reintenta en vez de romper el armado
            if datos.get("secciones") and all(isinstance(x, dict) and x.get("titulo") for x in datos["secciones"]):
                verificar_salidas(datos)
                return datos
        except (ValueError, TypeError, json.JSONDecodeError):
            pass
        print(f"  (respuesta de Claude inválida, intento {intento + 1})", file=sys.stderr)
    return None


_ri = None


def _repo_img():
    """repo-a-imagenes.py (ejecutar() en bwrap: sin red, sin /home, 5 s). Se carga solo si hace falta."""
    global _ri
    if _ri is None:
        sp = importlib.util.spec_from_file_location("repo_img", os.path.join(AQUI, "repo-a-imagenes.py"))
        _ri = importlib.util.module_from_spec(sp)
        sp.loader.exec_module(_ri)
    return _ri


def _normal(t):
    return re.sub(r"\s+", " ", str(t)).strip().strip("`").strip()


def _salida_real(ri, codigo, lang, previos):
    """Salida real de `codigo` (o None). Si usa funciones de la clase, se antepone solo el código de las
    secciones que las definen; una expresión suelta sin print/console.log se prueba también impresa."""
    if ri.NO_EJECUTAR.search(re.sub(r"(//|#).*", "", codigo)):
        return None
    impr = "console.log" if lang == "js" else "print"
    cands = [codigo]
    if "\n" not in codigo and impr not in codigo and not re.match(r"\s*(let|const|var|def|class|function|import)\b", codigo):
        cands.append(f"{impr}({codigo.rstrip(';').strip()})")
    usados = set(re.findall(r"\b([A-Za-z_]\w*)\s*\(", codigo))
    ctx = "\n".join(p for p in previos if any(re.search(r"\b" + re.escape(u) + r"\b\s*[=(]", p) for u in usados)
                    and not ri.NO_EJECUTAR.search(re.sub(r"(//|#).*", "", p)))
    for contexto in ([""] + ([ctx] if ctx else [])):
        ok0, out0 = ri.ejecutar(contexto, lang) if contexto else (True, "")
        if not ok0:
            continue
        for c in cands:
            ok, out = ri.ejecutar((contexto + "\n" + c) if contexto else c, lang)
            if ok and out.startswith(out0):
                out = out[len(out0):].strip("\n")
                out = re.sub(r"\nundefined$", "", out) if lang == "js" and c is not codigo else out
                if out.strip() and out.strip() != "undefined":
                    return out
    return None


def _coincide(real, respuesta):
    """¿La respuesta de la IA dice la salida real? Varias líneas valen si aparecen todas EN ORDEN
    ("4 y luego 101" = "4\\n101")."""
    r_ia = _normal(respuesta)
    pos = 0
    for linea in [_normal(x) for x in str(real).split("\n") if x.strip()]:
        m = re.compile(r"(?<![\w.])" + re.escape(linea) + r"(?!\w|\.\d)").search(r_ia, pos)
        if not m:
            return False
        pos = m.end()
    return True


def verificar_salidas(datos):
    """Las preguntas "¿qué imprime?" de JS/Python se ejecutan de verdad: si la salida real no es la que dijo
    la IA, se corrige la respuesta (nada inventado). Marca q["verificada"]=True cuando la salida es real."""
    corto = datos.get("corto") if isinstance(datos.get("corto"), dict) else {}
    try:
        ri = None
        for q in corto.get("preguntas") or []:
            if not isinstance(q, dict) or q.get("tipo") != "que-imprime" or not str(q.get("codigo", "")).strip():
                continue
            lang = str(q.get("lenguaje", "")).lower()
            if lang not in ("js", "javascript", "node", "py", "python", "python3"):
                continue
            ri = ri or _repo_img()
            lang = "js" if lang in ("js", "javascript", "node") else "py"
            if lang == "js" and not shutil.which("node"):
                continue
            previos = [str(x.get("codigo")) for x in datos.get("secciones") or []
                       if isinstance(x, dict) and str(x.get("codigo") or "").strip()
                       and (str(x.get("lenguaje", "")).lower() in ("js", "javascript", "node")) == (lang == "js")]
            real = _salida_real(ri, str(q["codigo"]).strip(), lang, previos)
            if real is None or not real.strip():
                continue
            q["verificada"] = True
            if not _coincide(real, q.get("respuesta", "")):
                q["respuesta_ia"] = q.get("respuesta", "")
                q["respuesta"] = f"`{real}`" if "\n" not in real else "\n" + real
    except Exception as e:  # la verificación nunca debe romper los apuntes
        print(f"  (no se pudieron verificar las salidas: {e})", file=sys.stderr)


TIMEOUT_OC = int(os.environ.get("APUNTES_TIMEOUT_OC", "150"))  # s por llamada a OpenCode antes de darla por colgada
RONDAS_CADENA = int(os.environ.get("APUNTES_RONDAS", "2"))  # veces que se recorre la cadena antes de rendirse
PAUSA_CADENA = int(os.environ.get("APUNTES_PAUSA", "45"))  # s entre rondas
TIMEOUT_CLAUDE = int(os.environ.get("APUNTES_TIMEOUT_CLAUDE", "300"))
ESPERA_CUOTA = 600  # s entre reintentos cuando se agotó la cuota de Claude
ESPERA_CUOTA_OC = 1200  # s entre reintentos cuando se agotó la ventana móvil (~5 h) de OpenCode Go
ESPERA_CUOTA_MAX = float(os.environ.get("APUNTES_ESPERA_MAX_H", "6")) * 3600  # la cuota se renueva cada ~5 h


def cuota_agotada(salida):
    """¿Claude contestó que se alcanzó el límite de uso? ("You've hit your session limit · resets 11pm")."""
    t = salida.lower()
    return ("limit" in t and ("hit your" in t or "resets" in t)) or "rate_limit" in t or "usage limit" in t


def llamar_claude(cmd, prompt, esperar=time.sleep, max_espera=None, timeout=1800):
    """Texto de la respuesta de `claude -p --output-format json`, o None si falló.
    Si se agotó la cuota NO sigue sin IA: espera a que se renueve y reintenta (hasta
    ESPERA_CUOTA_MAX). Así una playlist larga no deja clases sin resumen."""
    esperado = 0
    while True:
        try:
            r = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            print(f"  (claude no respondió en {timeout} s)", file=sys.stderr)
            return None
        try:
            d = json.loads(r.stdout)
            texto, error = str(d.get("result", "")), bool(d.get("is_error"))
        except (ValueError, AttributeError):
            texto, error = r.stdout, True
        if not cuota_agotada(texto + " " + r.stderr if error or r.returncode else ""):
            return None if error else texto
        if esperado >= (ESPERA_CUOTA_MAX if max_espera is None else max_espera):
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
                r = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=TIMEOUT_OC)  # normal: 40-90 s; si pasa de TIMEOUT_OC está colgado: mejor probar otro modelo
            except (OSError, subprocess.TimeoutExpired) as e:
                print(f"  (opencode {modelo} falló: {e})", file=sys.stderr)
                continue
            salida = (r.stdout or "") + " " + (r.stderr or "")
            if r.stdout.strip() and (r.returncode == 0 or ("{" in r.stdout and "}" in r.stdout)):
                return r.stdout  # a veces sale con código ≠ 0 pero con la respuesta completa
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


CODEX = os.environ.get("APUNTES_CODEX", "1") != "0"
CODEX_MODELO = os.environ.get("APUNTES_CODEX_MODELO", "")  # "" = el de la cuenta
TIMEOUT_CODEX = int(os.environ.get("APUNTES_TIMEOUT_CODEX", "300"))


def llamar_codex(prompt):
    """Respuesta de `codex exec` (sin herramientas: sandbox de solo lectura, sesión efímera), o None."""
    exe = shutil.which("codex") or os.path.expanduser("~/.local/bin/codex")
    if not CODEX or not os.path.exists(exe):
        return None
    import tempfile
    with tempfile.TemporaryDirectory(prefix="codex-apuntes-") as tmp:
        salida = os.path.join(tmp, "respuesta.txt")
        cmd = [exe, "exec", "--skip-git-repo-check", "--sandbox", "read-only", "--ephemeral", "-C", tmp,
               "-o", salida] + (["-m", CODEX_MODELO] if CODEX_MODELO else []) + ["-"]
        try:
            r = subprocess.run(cmd, input=SISTEMA + "\n\n" + prompt, capture_output=True, text=True, timeout=TIMEOUT_CODEX)
        except (OSError, subprocess.TimeoutExpired):
            print("  (Codex no respondió a tiempo)", file=sys.stderr)
            return None
        try:
            texto = open(salida, encoding="utf-8").read().strip()
        except OSError:
            texto = ""
        if r.returncode != 0 or not texto:
            print(f"  (Codex falló: {(r.stderr or '').strip().splitlines()[-1:] or r.returncode})", file=sys.stderr)
            return None
        return texto


def consultar_ia(prompt, modelo=None):
    """Texto de la respuesta del motor configurado (APUNTES_MOTOR=claude|opencode), o None.
    Con claude espera a que se renueve la cuota; el modelo es APUNTES_MODELO salvo que se
    indique otro (practica.py usa PRACTICA_MODELO). Con opencode se usa APUNTES_MODELO_OPENCODE."""
    if MOTOR == "opencode":
        # Cadena por velocidad y fiabilidad: 1) Claude RESPALDO (haiku: rápido y barato), 2) modelos de
        # OpenCode Go en orden (MODELOS_OPENCODE; el gratuito LongCat va al final: se cuelga seguido).
        # Cada paso falla rápido (timeout corto, sin esperar cuota) y se pasa al siguiente. Si TODOS
        # fallan se repite la cadena tras una pausa (los cuelgues suelen ser pasajeros); si aun así
        # no hay respuesta, la clase sigue sin IA y rehacer-sin-ia.py la rehace al final del curso.
        for ronda in range(RONDAS_CADENA):
            if ronda:
                print(f"  (todos los modelos fallaron: reintento la cadena en {PAUSA_CADENA} s, ronda {ronda + 1}/{RONDAS_CADENA})", file=sys.stderr)
                reportar(75, "apuntes", "reintentando la IA")
                time.sleep(PAUSA_CADENA)
            if RESPALDO:
                extra = ["--effort", RESPALDO_EFFORT] if RESPALDO_EFFORT else []
                cmd = [ruta_claude(), "-p", "--output-format", "json", "--tools", "", "--strict-mcp-config",
                       "--no-session-persistence", "--system-prompt", SISTEMA, "--model", RESPALDO] + extra
                texto = llamar_claude(cmd, prompt, max_espera=0, timeout=TIMEOUT_CLAUDE)
                if texto is not None:
                    return texto
                print(f"  (Claude {RESPALDO} no disponible: sigo con OpenCode)", file=sys.stderr)
            texto = None if opencode_enfriando() else llamar_opencode(prompt, max_espera=0)
            if texto is not None:
                return texto
            texto = llamar_codex(prompt)  # último respaldo: la cuota de ChatGPT (Codex CLI)
            if texto is not None:
                return texto
        return llamar_opencode(prompt) if not RESPALDO else None
    cmd = [ruta_claude(), "-p", "--output-format", "json", "--tools", "", "--strict-mcp-config",
           "--no-session-persistence", "--system-prompt", SISTEMA]
    m = MODELO if modelo is None else modelo
    if m:
        cmd += ["--model", m]
    return llamar_claude(cmd, prompt)


# ----------------------------------------------------------------- armado ----
def armar(carpeta, titulo, capturas, subs, datos, duracion, recursos_md=""):
    cues_es = subs.get("es") or subs.get("en") or []
    idioma_txt = "español" if subs.get("es") else ("inglés" if subs.get("en") else None)
    importantes = [c for c in capturas if c[2]]
    esenciales = set()
    if os.environ.get("CAPTURAS_CLAVE") != "0":
        try:  # las deja capturas_clave.esenciales() al elegir las importantes
            esenciales = set(open(os.path.join(carpeta, cc.ESENCIALES), encoding="utf-8").read().splitlines()[1:])
        except OSError:
            pass

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

    voz = [(t, p) for t, p in parrafos(cues_es)]
    hay_resumen = os.path.exists(os.path.join(carpeta, "resumen.md"))
    hay_voz = bool(voz)

    presupuesto = presupuesto_lectura(duracion)
    for nivel in range(4):  # si se pasa del presupuesto se pliega lo menos importante, de a poco
        md = _armar_md(titulo, capturas, datos, duracion, recursos_md, secciones, importantes, esenciales,
                       voz, idioma_txt, hay_resumen, nivel)
        if palabras_a_la_vista(md) <= presupuesto:
            break
    escribir_transcripcion(carpeta, titulo, secciones, voz, idioma_txt, duracion)
    return md


# los valores del JSON siguen siendo diario/a-veces/raro (compatibles); lo que se muestra dice IMPORTANCIA:
# en teoría (backprop, complejidad) algo es "clave" aunque no se escriba todos los días
REL = {"diario": "⭐ **Clave**", "a-veces": "🔸 **Útil**", "raro": "💤 **De paso**"}


def presupuesto_lectura(segundos):
    """Palabras A LA VISTA (lo plegado no cuenta): ~35 % del video a 200 palabras/min, mín. 120."""
    return max(120, int(70 * segundos / 60))


def palabras_a_la_vista(md):
    """Palabras que se leen de corrido: sin bloques plegados ([!x]-), imágenes ni rótulos de minuto."""
    n, plegado = 0, False
    for l in md.split("\n"):
        if re.match(r"\s*> \[!\w+\]-", l):
            plegado = True
            continue
        if plegado and re.match(r"\s*>", l):
            continue
        plegado = False
        # rótulos y navegación (minutos, enlaces, cabecera): se miran, no se leen
        if l.startswith(("![", "*⏱️", "<!--", "⏱️", "> ⏱️", "> ⚡", "> 🗣️", "---")):
            continue
        n += len(l.split())
    return n


COMENTARIO = {**dict.fromkeys(("python", "py", "bash", "sh", "shell", "zsh", "fish", "yaml", "yml", "toml", "r", "ruby",
                               "rb", "dockerfile", "makefile", "perl", "powershell", "ps1", "ini", "conf"), ("#", "")),
              **dict.fromkeys(("sql", "plsql", "mysql", "postgresql", "lua", "haskell"), ("--", "")),
              **dict.fromkeys(("html", "xml", "vue", "svelte", "markdown", "md"), ("<!--", " -->")),
              **dict.fromkeys(("css", "scss", "sass", "less"), ("/*", " */"))}
SIN_COMENTARIOS = {"", "text", "txt", "json", "plaintext", "console", "output", "csv"}


def _comentar(codigo, lenguaje, lal):
    """Mete cada explicación "`fragmento` → por qué" como comentario 👉 en la línea del código que la tiene
    (el código del profe no cambia: solo se agregan comentarios, marcados con 👉). Devuelve (código, sobrantes)."""
    lang = str(lenguaje or "").lower().strip()
    if lang in SIN_COMENTARIOS:
        return codigo, [_txt(x) for x in lal if _txt(x)]
    abre, cierra = COMENTARIO.get(lang, ("//", ""))
    lineas, sobran = codigo.split("\n"), []
    for item in lal:
        t = _txt(item)
        m = re.match(r"`([^`]+)`\s*(?:→|->|:|—|-)\s*(.+)", t)
        if not m:
            sobran.append(t) if t else None
            continue
        frag, expl = m.group(1).strip(), m.group(2).strip().rstrip(".")
        idx = next((k for k, l in enumerate(lineas) if frag in l and "👉" not in l), None)
        if idx is None and len(frag) > 12:
            idx = next((k for k, l in enumerate(lineas) if frag[:12] in l and "👉" not in l), None)
        if idx is None:
            sobran.append(t)
            continue
        com = f"{abre} 👉 {expl}{cierra}"
        if len(lineas[idx]) + len(com) + 2 <= 100:
            lineas[idx] = f"{lineas[idx]}  {com}"
        else:  # línea larga: el comentario va arriba, con la misma sangría
            sangria = re.match(r"\s*", lineas[idx]).group(0)
            lineas.insert(idx, f"{sangria}{com}")
    return "\n".join(lineas), sobran


def _repite(comp, puntos):
    """¿La tabla comparativa solo repite lo que ya dicen los puntos?"""
    celdas = [_txt(x) for f in (comp or {}).get("filas") or [] if isinstance(f, list) for x in f[1:]]
    texto = " ".join(_txt(p) for p in puntos or []).lower()
    pal = [w for c in celdas for w in re.findall(r"\w{4,}", c.lower())]
    return bool(pal) and sum(1 for w in pal if w in texto) / len(pal) >= 0.6


def _armar_md(titulo, capturas, datos, duracion, recursos_md, secciones, importantes, esenciales,
              voz, idioma_txt, hay_resumen, nivel):
    """nivel 0 = todo a la vista · 1 = pliega lo 💤 y el índice · 2 = también ejemplos/comparativas de lo 🔸 y
    la práctica · 3 = también los errores después del 3.º (lo ⭐ nunca se pliega)."""
    hay_voz = bool(voz)
    L = [f"# 📓 {titulo}", ""]
    L += [f"> ⏱️ **Duración:** {hms(duracion)} · 📸 **Capturas:** {len(esenciales) or len(importantes)} a la vista "
          f"({len(importantes)} clave de {len(capturas)}) · 📚 **Secciones:** {len(secciones)}"]
    enlaces = (["⚡ [Repaso rápido](resumen.md)"] if hay_resumen else []) + \
              ([f"🗣️ [Lo que dice el profe](transcripcion.md) ({idioma_txt})"] if hay_voz else [])
    if enlaces:
        L += ["> " + " · ".join(enlaces)]
    L += [""]
    if (datos or {}).get("sin_contenido"):  # bienvenida / despedida / anuncio: apenas nada
        for s in secciones:
            L += [f"- {p}" for p in (s.get("puntos") or [])[:2]]
        return "\n".join(L + ["", f"<!-- formato v{FORMATO} -->", ""])
    objetivos = [o for o in (datos or {}).get("objetivos") or [] if _txt(o)][:3] if duracion >= 180 else []
    if objetivos:
        L += ["## 🎯 Al terminar podrás", ""] + [f"- [ ] {_txt(o)}" for o in objetivos][:3 if nivel < 3 else 2] + [""]
    if datos and datos.get("resumen") and not hay_resumen:  # el resumen ya está en resumen.md: no se repite
        L += ["## 🎯 En 30 segundos", ""] + [f"- {p}" for p in datos["resumen"]] + [""]
    if len(secciones) >= 4:  # navegación, no lectura: plegado
        L += [f"> [!summary]- 🗂️ Índice ({len(secciones)} temas)"]
        L += [f"> {k + 1}. [{s['titulo']}](#{k + 1}-{ancla(s['titulo'])}) · `{hms(s['ini'])}`" for k, s in enumerate(secciones)]
        L += [""]
    L += ["---", ""]
    if recursos_md:
        L += [recursos_md, "---", ""]

    for k, s in enumerate(secciones):
        dur = min(s["fin"], duracion) - s["ini"]
        rel = str(s.get("relevancia") or "").strip().lower()
        L += [f"## {k + 1}. {s['titulo']}", ""]
        cab = f"⏱️ `{hms(s['ini'])} – {hms(min(s['fin'], duracion))}`"
        if hay_voz and any(s["ini"] <= t < s["fin"] for t, _ in voz):
            cab += f" · 🗣️ [lo que dice el profe](transcripcion.md#{k + 1}-{ancla(s['titulo'])})"
        L += [cab, ""]
        porque = _txt(s.get("porque"))
        if (rel in REL or porque) and not (dur < 90 and nivel >= 2 and rel != "diario"):
            L += ["> " + " — ".join(x for x in (REL.get(rel, ""), porque) if x), ""]
        plegar = (rel == "raro" and nivel >= 1)
        cuerpo = []
        # presupuesto de la sección según lo que dura: los puntos que se pasan van plegados (no se pierden)
        tope = max(30, 20 * dur / 60) * (1.5, 1.2, 1.0, 0.8)[nivel] * (1.3 if rel == "diario" else 1.0)
        vis, mas, usadas = [], [], 0
        for p in (s.get("puntos") or []):
            n = len(_txt(p).split())
            (vis if (not vis or usadas + n <= tope) and len(vis) < 5 else mas).append(p)
            usadas += n if p in vis else 0
        cuerpo += [f"- {p}" for p in vis]
        if mas:
            cuerpo += [f"> [!note]- ➕ {len(mas)} punto{'s' if len(mas) > 1 else ''} más"] + [f"> - {p}" for p in mas]
        if s.get("puntos"):
            cuerpo += [""]
        sobran = []
        if str(s.get("codigo") or "").strip():
            lal = [x for x in (s.get("linea_a_linea") or []) if _txt(x)]
            codigo, sobran = _comentar(str(s["codigo"]).strip("\n"), s.get("lenguaje"), lal)
            cuerpo += [f"```{s.get('lenguaje') or ''}", codigo, "```", ""]
        if plegar:
            L += ["> [!note]- 💤 Ver el detalle"] + [f"> {x}" if x else ">" for x in cuerpo] + [""]
        else:
            L += cuerpo
        if sobran:
            L += ["> [!tip]- 🔍 Más detalle del código"] + [f"> - {x}" for x in sobran] + [""]
        if _txt(s.get("intuicion")):
            L += [f"> [!abstract] 🧠 La idea", f"> {_txt(s['intuicion'])}", ""]
        diag = _mermaid(s.get("diagrama"))
        if diag:
            L += ["```mermaid", diag, "```", ""]
        comp = s.get("comparativa")
        if dur >= 180 and not _repite(comp, s.get("puntos")):
            tabla = _tabla_comparativa(comp)
            if tabla and (plegar or (nivel >= 2 and rel != "diario")):
                L += ["> [!info]- ⚖️ Comparativa"] + [f"> {x}" for x in tabla] + [""]
            else:
                L += tabla
        ej = s.get("ejemplo")
        if isinstance(ej, dict) and (ej.get("pasos") or ej.get("salida")):
            marca = "-" if (plegar or (nivel >= 2 and rel != "diario")) else ""
            L += [f"> [!example]{marca} 🧪 Ejemplo resuelto: {_txt(ej.get('enunciado'))}"]
            L += [f"> {n}. {_txt(x)}" for n, x in enumerate(ej.get("pasos") or [], 1)]
            if _txt(ej.get("salida")):
                L += [">", f"> **➜ Resultado:** {_txt(ej['salida'])}"]
            L += [""]
        caps = [c for c in importantes if s["ini"] <= c[1] < s["fin"]]
        if caps:
            # a la vista: las esenciales de la sección (la mitad de las clave); si no hay, la última
            # (estado final) + las de más novedad. El resto queda plegado.
            elegidas = {c[0] for c in caps if c[0] in esenciales}
            if not elegidas:
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
        L += ["---", ""]

    if datos:
        # clases cortas: se muestra solo lo que les toca (lo demás queda en el JSON), aunque se hayan hecho con más
        tope_l = 0 if duracion < 120 else 1 if duracion < 300 else 2 if duracion < 600 else None
        errores = [e for e in datos.get("errores_comunes") or [] if e][:tope_l]
        if errores:
            def linea_error(e):
                if not isinstance(e, dict):
                    return f"- {_txt(e)}"
                por = f" *({_txt(e.get('porque'))})*" if _txt(e.get("porque")) else ""
                arr = f" → ✅ {_txt(e.get('arreglo'))}" if _txt(e.get("arreglo")) else ""
                return f"- ❌ **{_txt(e.get('error'))}**{arr}{por}"
            corte = {0: len(errores), 1: len(errores), 2: 3, 3: 2}[nivel]
            vis, resto = errores[:corte], errores[corte:]
            L += ["## ⚠️ Errores comunes", ""] + [linea_error(e) for e in vis]
            if resto:
                L += ["", f"> [!warning]- {len(resto)} errores más"] + [f"> {linea_error(e)}" for e in resto]
            L += [""]
        if (datos.get("practica") or [])[:tope_l]:
            P = []
            for e in datos["practica"][:tope_l]:
                if isinstance(e, dict):  # nivel + pista + solución, ambas plegadas (primero intentarlo solo)
                    P += [f"- [ ] {_txt(e.get('nivel'))} {_txt(e.get('enunciado'))}".replace("[ ]  ", "[ ] ")]
                    if _txt(e.get("pista")):
                        P += ["  > [!hint]- 💡 Pista", f"  > {_txt(e['pista'])}"]
                    sol = str(e.get("solucion") or "").strip("\n")
                    if sol.strip():
                        P += ["  > [!success]- ✅ Solución"] + [f"  > {x}" for x in sol.split("\n")]
                    continue
                txt = _txt(e)
                if " — 💡 Pista:" in txt:
                    enun, pista = txt.split(" — 💡 Pista:", 1)
                    P += [f"- [ ] {enun.strip()}", "  > [!hint]- 💡 Pista", f"  > {pista.strip()}"]
                else:
                    P += [f"- [ ] {txt}"]
            L += ["## 🏋️ Para practicar", ""]
            if nivel >= 2:  # la práctica se HACE, no se lee: plegada no cuenta como lectura
                L += [f"> [!todo]- {len(datos['practica'][:tope_l])} ejercicios con pista y solución"] + \
                     [f"> {x}" for x in P] + [""]
            else:
                L += P + [""]
            if any(str(x.get("lenguaje", "")).lower() in ("js", "javascript", "python", "py") for x in secciones):
                L += ["> Con el botón **Práctica** de SUPER+I salen ejercicios con tests (JS/Python).", ""]
        if datos.get("conceptos") and duracion >= 180:
            conc = [c for c in datos["conceptos"] if isinstance(c, dict)]
            # material de consulta: plegado (no se lee de corrido, se abre cuando hace falta)
            L += ["## 🧠 Glosario", "", f"> [!abstract]- {len(conc)} términos de la clase", "> | Concepto | Qué es |", "> |---|---|"]
            L += [f"> | **{_celda(c.get('termino', ''))}** | {_celda(c.get('definicion', ''))} |" for c in conc]
            L += [""]
        voc = [v for v in datos.get("vocabulario") or [] if isinstance(v, dict) and _txt(v.get("en"))]
        if voc and duracion >= 180:
            L += ["## 🇬🇧 Vocabulario", "", f"> [!abstract]- {len(voc)} términos en inglés (con pronunciación)",
                  "> | English | Suena | Español |", "> |---|---|---|"]
            L += [f"> | **{_celda(v.get('en'))}** | {_celda(v.get('suena'))} | {_celda(v.get('es'))} |" for v in voc]
            L += [""]
    else:
        L += ["> [!info] Apuntes sin resumen de IA (solo capturas y transcripción)", ""]
    L += [f"<!-- formato v{FORMATO} -->", ""]
    return "\n".join(L)


def _tabla_comparativa(c):
    """{titulo, columnas, filas} → tabla Markdown (2-5 columnas), o [] si no sirve."""
    if not isinstance(c, dict):
        return []
    cols = [_celda(x) for x in c.get("columnas") or []]
    filas = [f for f in c.get("filas") or [] if isinstance(f, list) and f]
    if not 2 <= len(cols) <= 5 or not filas:
        return []
    L = [f"**⚖️ {_txt(c.get('titulo'))}**", "", "| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for f in filas:
        f = [_celda(x) for x in f][:len(cols)]
        L += ["| " + " | ".join(f + [""] * (len(cols) - len(f))) + " |"]
    return L + [""]


def _txt(x):
    return re.sub(r"\s*\n\s*", " ", str(x)).strip() if x is not None else ""


def _celda(x):
    return _txt(x).replace("|", "\\|")


def _mermaid(texto):
    """Diagrama mermaid limpio (sin ```), o "" si no parece mermaid."""
    t = str(texto or "").strip()
    if "\n" not in t and "\\n" in t:  # la IA a veces escapa de más: "a\\nb" literal en vez de salto de línea
        t = t.replace("\\n", "\n")
    t = re.sub(r"^```(mermaid)?\s*|\s*```$", "", t).strip()
    primera = t.split("\n", 1)[0].strip().split(" ")[0] if t else ""
    validos = ("flowchart", "graph", "sequenceDiagram", "classDiagram", "erDiagram", "stateDiagram",
               "stateDiagram-v2", "mindmap", "timeline", "gantt", "pie", "journey")
    return t if primera in validos and "\n" in t else ""


def escribir_transcripcion(carpeta, titulo, secciones, voz, idioma_txt, duracion):
    """transcripcion.md: lo que dice el profe, por sección (fuera de apuntes.md: era ~70 % de sus palabras)."""
    ruta = os.path.join(carpeta, "transcripcion.md")
    if not voz:
        return
    L = [f"# 🗣️ Lo que dice el profe: {titulo}", "",
         f"> ⏱️ {hms(duracion)} · idioma: {idioma_txt} · 📓 [Volver a los apuntes](apuntes.md)", ""]
    for k, s in enumerate(secciones):
        texto = [(t, p) for t, p in voz if s["ini"] <= t < s["fin"]]
        if not texto:
            continue
        L += [f"## {k + 1}. {s['titulo']}", ""]
        for t, p in texto:
            L += [f"`{hms(t)}` {p}", ""]
    try:
        with open(ruta, "w", encoding="utf-8") as f:
            f.write("\n".join(L))
    except OSError as e:
        print(f"  (no se pudo escribir transcripcion.md: {e})", file=sys.stderr)


def ancla(titulo):
    """Ancla estilo GitHub/Obsidian para el índice."""
    t = titulo.lower()
    t = re.sub(r"[^\w\s-]", "", t)
    return re.sub(r"\s+", "-", t.strip())


def _idea(carpeta_capturas, d):
    try:
        datos = json.load(open(os.path.join(carpeta_capturas, d, ".apuntes-ia.json"), encoding="utf-8"))
        return (datos.get("resumen") or [""])[0].replace("|", "/")
    except (OSError, ValueError):
        return ""


def _tema_y_clase(nombre):
    """'05 Tema - 003 Clase' -> ('05 Tema', '003 Clase'); sin tema -> ('', nombre)."""
    m = re.match(r"^(.+?) - (\d{1,3}\s.*)$", nombre)
    if m and not re.fullmatch(r"\d+", m.group(1).strip()):
        return m.group(1).strip(), m.group(2).strip()
    return "", nombre


def indice(carpeta_capturas, nombre_curso):
    """INDICE.md en la carpeta capturas/: clases con link a sus apuntes, agrupadas por tema
    cuando los nombres son 'Tema - NNN Clase' (cursos con una carpeta por tema)."""
    clases = sorted(d for d in os.listdir(carpeta_capturas)
                    if os.path.isfile(os.path.join(carpeta_capturas, d, "apuntes.md")))
    pares = [(d,) + _tema_y_clase(d) for d in clases]
    temas = list(dict.fromkeys(t for _, t, _ in pares))
    agrupar = len([t for t in temas if t]) >= 2
    L = [f"# 🎓 {nombre_curso}", "",
         f"> 📚 **{len(clases)} clases**" + (f" en **{len(temas)} temas**" if agrupar else "") +
         " · cada clase tiene sus apuntes completos, `resumen.md` (repaso rápido) y `tarjetas.md` (para repasar con memoria espaciada).",
         "", "> [!tip] Cómo estudiar con esto",
         "> 1. Mira el video (o salta directo a los apuntes si ya lo viste).",
         "> 2. Lee `🎯 Resumen` y `🧠 Conceptos clave`; tapa la tabla e intenta explicarlos con tus palabras.",
         "> 3. Escribe el código tú mismo antes de mirar la solución.",
         "> 4. Repasa las `tarjetas.md` a los 1, 3 y 7 días.", ""]
    if agrupar:
        L += ["## 🧭 Temas", ""]
        for k, t in enumerate(temas, 1):
            n = sum(1 for _, tt, _ in pares if tt == t)
            L.append(f"{k}. [{t or 'Otras clases'}](#{ancla(t or 'Otras clases')}) · {n} clases")
        L.append("")
    n_global = 0
    for t in temas:
        grupo = [(d, c) for d, tt, c in pares if tt == t]
        if agrupar:
            L += [f"## {t or 'Otras clases'}", ""]
        L += ["| # | Clase | Idea principal |", "|---|---|---|"]
        for d, c in grupo:
            n_global += 1
            L.append(f"| {n_global} | [{c}](<{d}/apuntes.md>) | {_idea(carpeta_capturas, d)} |")
        L.append("")
    L += [f"*{len(clases)} clases con apuntes · generado por cuadernillo.py*", ""]
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
    rehacer = os.path.join(carpeta, ".rehacer")  # marcada por rehacer-con-voz.py: se rehace aunque exista
    if os.path.exists(salida) and not a.forzar and not os.path.exists(rehacer):
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
    if not subs and a.video and tr.disponible():
        # sin subtítulos los apuntes salen solo de la pantalla: se transcribe el audio con Whisper (GPU)
        print("🎙️ Sin subtítulos: transcribiendo con Whisper (GPU)…")
        reportar(57, "apuntes", "transcribiendo el audio (Whisper)")
        if tr.transcribir(os.path.abspath(a.video)):
            subs = buscar_subtitulos(carpeta, a.video)
    if a.video:
        # copia en la carpeta de la clase: rehacer-sin-ia.py y --forzar los encuentran sin el video
        for idioma, ruta in tr.subtitulos_al_lado(a.video).items():
            dst = os.path.join(carpeta, f"subtitulos.{idioma}{os.path.splitext(ruta)[1].lower()}")
            if not glob.glob(os.path.join(glob.escape(carpeta), f"subtitulos.{idioma}*")):
                shutil.copyfile(ruta, dst)
    print(f"🗣️ Subtítulos: {', '.join(subs) or 'ninguno'}")

    # Material del curso junto al video (código del profe, lecturas, enlaces). Se guarda en la clase
    # (codigo-del-curso/ y .recursos.md) para poder rehacer los apuntes sin el video.
    codigo_curso, recursos_md = "", ""
    ruta_md = os.path.join(carpeta, ".recursos.md")
    if a.video and os.environ.get("SIN_RECURSOS") != "1":
        rec = rec_curso.de_la_clase(a.video)
        copiados = rec_curso.copiar_a_clase(rec, carpeta) if any(rec[k] for k in ("clase", "lecturas", "pdf", "imagenes")) else []
        recursos_md = rec_curso.seccion_md(rec, copiados)
        pantalla = "\n".join((cc.textos(carpeta, [c[0] for c in capturas if c[2]]) or {}).values()) \
            if os.environ.get("CAPTURAS_CLAVE") != "0" else ""
        codigo_curso = rec_curso.codigo_para_ia(rec, pantalla)
        with open(ruta_md, "w", encoding="utf-8") as f:
            f.write(recursos_md)
        if codigo_curso or recursos_md:
            print(f"📎 Recursos del curso: {len(rec['clase'])} de la clase, {len(rec['proyecto'])} del proyecto, "
                  f"{len(rec['lecturas'])} lecturas, {len(rec['enlaces'])} enlaces")
    elif os.path.exists(ruta_md):
        recursos_md = open(ruta_md, encoding="utf-8").read()
        dcc = os.path.join(carpeta, "codigo-del-curso")
        if os.path.isdir(dcc):  # sin el video: el código que ya se copió a la clase
            codigo_curso = rec_curso.codigo_para_ia({"clase": [dcc], "lecturas": [], "pdf": [], "proyecto": []})
    # video de YouTube: enlaces de la descripción y capítulos del autor (video.info.json, lo deja video-a-capturas.sh)
    enl_yt, capitulos = rec_curso.de_youtube(carpeta)
    if enl_yt:
        recursos_md = (recursos_md + "\n" if recursos_md else "## 📎 Recursos de la clase\n\n") + \
            "**🔗 De la descripción del video:**\n\n" + "\n".join(f"- [{t}]({u})" for t, u in enl_yt) + "\n"
    if capitulos:
        codigo_curso += ("\n--- CAPÍTULOS DEL VIDEO (los puso el autor: úsalos como las secciones, con estos tiempos) ---\n"
                         + "\n".join(f"[{hms(t)}] {n}" for t, n in capitulos) + "\n")
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
        # cada 2 min: con las capturas clave cada pantalla es un estado final, y las repetidas se quitan
        pantallas = leer_pantallas(carpeta, capturas, cada=120 if subs else 20)
        print(f"   {len(pantallas)} pantallas leídas")
        if subs or pantallas:
            print(f"🤖 Pidiendo a {nombre_motor()} apuntes + resumen corto…")
            reportar(75, "apuntes", f"{nombre_motor()} armando el resumen")
            datos = pedir_a_claude(titulo, duracion, subs_para_claude(carpeta, subs), pantallas, codigo_curso)
        if datos:
            corto = datos.pop("corto", None)
            datos["formato"] = FORMATO  # mejorar-apuntes.py salta las que ya tienen el formato actual
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
        f.write(armar(carpeta, titulo, capturas, subs, datos, duracion, recursos_md))
    if os.path.exists(rehacer) and (datos or a.sin_ia):
        os.remove(rehacer)  # sin IA por un fallo: queda marcada para el próximo intento
    print(f"📓 Listo: {salida}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
