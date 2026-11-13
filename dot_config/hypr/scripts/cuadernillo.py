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
import unicodedata
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
import apuntes_politica as editorial
spec = importlib.util.spec_from_file_location("ac", os.path.join(AQUI, "auto-captura.py"))
ac = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ac)

CAPTURAS_A_LA_VISTA = 4   # capturas visibles por sección si no hay esenciales (el resto queda plegado)


def _interp(m, puntos):
    """Interpolación lineal por tramos: puntos = [(minutos, valor), …] ordenados; fuera de rango se queda en el extremo."""
    if m <= puntos[0][0]:
        return puntos[0][1]
    for (m0, v0), (m1, v1) in zip(puntos, puntos[1:]):
        if m <= m1:
            return v0 + (v1 - v0) * (m - m0) / (m1 - m0)
    return puntos[-1][1]


# v8 (08/11/2026): UNA curva de densidad por duración (la densidad baja a medida que el video crece) y menos andamiaje
# en lo corto. Medido en 12 clases de 1 min a 8 h: el apunte pesaba como la transcripción entera en lo corto y era
# demasiado delgado (3-5 palabras/min) en lo muy largo.
def presupuesto_paquete(segundos):
    """v9 (08/11/2026): palabras TOTALES que debería leer el alumno por clase (apuntes a la vista + repaso + preguntas).
    Regla del usuario: estudiar no puede costar casi lo que dura el video. A 200 palabras/min el tiempo de lectura
    queda en ~22 % del video a 1 min, 15 % a 8 min, 11 % a 20 min, 8 % a 45 min, 6 % a 2 h, 4 % a 5 h."""
    m = segundos / 60
    return int(_interp(m, [(0, 40), (1, 70), (3, 220), (8, 360), (12, 500), (20, 650), (45, 950), (120, 1900), (300, 3700), (600, 4800)]))


def n_preguntas(segundos):
    """Preguntas de autoevaluación (única fuente de las tarjetas): el 25 % del presupuesto a ~30 palabras cada una, 1 a 20."""
    m = segundos / 60
    return max(2 if m >= 2 else 1, min(20, round(0.22 * presupuesto_paquete(segundos) / 30)))


def n_pretest(segundos):
    """Preguntas del pre-test (SUPER+I): 0 por debajo de 1 h (la autoevaluación ya cubre), 4 de ahí."""
    return 0 if segundos / 60 < 60 else 4


def n_ejercicios(segundos):
    """Ejercicios de "Para practicar": 0 (<5 min), 1 (<20), 2 (<45), 4 (<90), 6."""
    m = segundos / 60
    return 0 if m < 10 else 1 if m < 20 else 2 if m < 45 else 4 if m < 90 else 6


def n_errores(segundos):
    """Errores comunes (solo los que el profe advierte): 0 (<5 min), 1 (<10), 2 (<45), 4 (<120), 5."""
    m = segundos / 60
    return 0 if m < 10 else 1 if m < 45 else 3 if m < 120 else 5


def n_diagramas(segundos):
    """Tope de diagramas mermaid: 0 (<10 min), 1 (<45), de ahí 1 cada 30 min hasta 4."""
    m = segundos / 60
    return 0 if m < 10 else 1 if m < 45 else min(4, int(m // 30))


def rango_diagramas(segundos):
    n = n_diagramas(segundos)
    return f"como máximo {n}" if n else "ninguno"


def n_vocabulario(segundos):
    """Términos en inglés: 0 por debajo de 1 h, 3 de ahí."""
    return 0 if segundos / 60 < 60 else 3


def tope_palabras(segundos):
    """Palabras de TODOS los "puntos" juntos (sin código ni lo demás): ~40 % del presupuesto del paquete."""
    return int(max(40, round(0.42 * presupuesto_paquete(segundos), -1)))


def presupuesto_lectura(segundos):
    """Palabras A LA VISTA de apuntes.md (código y plegados cuentan menos, ver palabras_a_la_vista): 60 % del paquete.
    Si el apunte se pasa, armar() recorta (nivel 4-6) lo menos importante; el JSON de la IA conserva todo."""
    return int((0.62 if segundos < 1200 else 0.55) * presupuesto_paquete(segundos))


def n_tarjetas(segundos):
    """Tope de tarjetas por clase: las mismas que preguntas de autoevaluación."""
    return n_preguntas(segundos)


def regla_secciones(segundos):
    m = segundos / 60
    if m < 3:
        return "UNA sola sección, con todos los datos concretos del profe (cifras, versiones, herramientas, requisitos)."
    if m < 8:
        return "1 o 2 secciones; no partas un mismo tema en varias."
    if m < 12:
        return ("entre 3 y 5 secciones (una cada ~2-3 min), cada una con sus propios datos y su marca de tiempo; no metas dos temas "
                "distintos en una sola sección (v10: antes salían 2 secciones para 10 min y se perdía el detalle).")
    if m < 20:
        return ("entre 4 y 6 secciones (una cada ~2-4 min), cada una con sus propios datos y su marca de tiempo; no metas dos temas "
                "distintos en una sola sección.")
    if m < 45:
        return ("entre 4 y 6 secciones (una cada ~6-8 min), cada una de más de 4 min con al menos 3 puntos; NINGUNA de más de 8 min: un tema que el profe explica más adelante va "
                "en SU sección con su marca de tiempo; junta los pasos pequeños del mismo mecanismo.")
    if m < 120:
        return ("entre 6 y 10 secciones; cada una cubre entre ~5 y 12 min; ninguna con un solo punto. Reparte las secciones "
                "por TODO el video: cada tema importante debe tener la suya y ningún tramo largo puede quedar sin cubrir.")
    return ("entre 20 y 35 secciones (una cada 12-15 min); ninguna con un solo punto. Cubre TODO el video: cada tema, herramienta "
            "o concepto que se explica debe tener su sección; ningún tramo de más de 20 min puede quedar sin sección.")


def regla_extras(segundos):
    m = segundos / 60
    base = ("Sin relleno: NO inventes ejemplos, errores comunes, ejercicios ni definiciones que no salgan de lo que se hace "
            "en el video; `errores_comunes` y `practica` solo si el profe los plantea o advierte (si no, vacíos). Datos que solo "
            "estén en el OCR y no en lo que dice el profe no se afirman (salvo el código). NO escribas metacomentarios sobre la "
            "fuente (\"dato que no se confirma\", \"el profe no desarrolla\"): di el dato o calla. Una pregunta NO se repite entre "
            "`corto.preguntas`, `pretest`, `errores_comunes` y `practica`. CONSERVA siempre toda cifra, versión, herramienta, "
            "requisito, advertencia, alternativa, tabla y ejemplo numérico que el profe muestre, y SIEMPRE las conclusiones o "
            "recomendaciones finales: se resume el relleno, no los datos. La ÚLTIMA sección tiene una viñeta PROPIA con los resultados, cifras finales, "
            "conclusiones y recomendaciones del cierre del video, y las advertencias del profe (\"evita…\", \"cuidado con…\") van como "
            "viñeta en los apuntes (no solo en las tarjetas). El título de cada sección debe corresponder a lo que sus puntos "
            "desarrollan (no prometas algo que el cuerpo no explica). Una de las preguntas cubre el resultado o la conclusión final. ")
    if m < 20:
        return base + ("NO incluyas conceptos (glosario) ni vocabulario. `ejemplo` solo si el profe resuelve casos con cifras (conserva hasta 3, "
                       "cada uno en una línea con sus valores y resultado reales); `comparativa` sirve también como TABLA DE REFERENCIA "
                       "del profe (hasta 16 filas). Todo caso de uso que el profe menciona va como punto. Los ejemplos numéricos que el "
                       "profe resuelve (p. ej. 0110 = 4+2 = 6) van como punto con su cálculo: no se recortan.")
    if m < 60:
        return base + ("NO incluyas conceptos (glosario) ni vocabulario. Ejemplo resuelto solo si el profe hace un cálculo o prueba "
                       "paso a paso cuyo resultado no se ve en el código; comparativa solo si el profe compara alternativas.")
    return base + ("Glosario: como máximo 6 términos, solo los que las secciones explican. Ejemplo resuelto y comparativa "
                   "solo si el profe los hace.")


def regla_presupuesto(segundos):
    w = presupuesto_paquete(segundos)
    return (f"PRESUPUESTO TOTAL DE LECTURA de esta clase (apuntes + repaso + preguntas): {w} palabras, ~{max(0.2, w / 200):.1f} min de lectura "
            f"para un video de {segundos / 60:.0f} min. Es un tope DURO: escribe lo mínimo que permite recordar el video. Prioriza cifras, "
            "versiones, pasos, código esencial, advertencias y conclusiones; elimina narración, contexto y repeticiones. Cada punto es una "
            "idea concreta de una línea. NO recortes datos duros para ahorrar palabras: cifras, versiones, requisitos, a quién va dirigido, "
            "temario, pasos, tablas de referencia, resultados de los ejemplos del profe y su conclusión o advertencia final (aunque sea en "
            "una línea); se recorta la narración, no los datos. Tampoco te quedes corto: usa al menos el 70 % del presupuesto si el video "
            "tiene datos concretos. El alumno ya ve el video y tiene las capturas: los apuntes solo refuerzan.")


def regla_resumen(segundos):
    m = segundos / 60
    if m < 20:
        return ("El repaso (`corto`) es mínimo: idea en una frase, 2 o 3 puntos en `esencial`, sin chuleta, mapa, código ni diagrama; "
                "las preguntas son pocas y concretas.")
    if m < 45:
        return ("El repaso (`corto`) es corto: idea, 3 a 5 puntos en `esencial`, chuleta solo si hay sintaxis o comandos; sin mapa, "
                "código ni diagrama (ya están en las secciones).")
    return ("El repaso (`corto`) es un mapa de bloques del video: idea, 5 a 8 puntos en `esencial` repartidos por TODO el video; "
            "chuleta y código mínimo solo lo imprescindible.")


FORMATO = 10  # v10: recorte que cumple el presupuesto sí o sí, sin metacomentarios ni '(extra)'; v6: menos andamiaje en clases cortas, diagramas solo si explican, "primero recuerda", soluciones comprobadas, "(extra)"; v5: cero imágenes; v4: relevancia ⭐🔸💤, comentarios 👉 en el código, intuición, tope de lectura; v3: + objetivos, comparativas, solución de ejercicios, vocabulario; v2 del formato de apuntes.md (v2: sin transcripción adentro, ejemplos, diagramas, errores con arreglo)
SISTEMA = ("Eres un docente experto en la disciplina de la clase. Priorizas precisión, comprensión y práctica. "
           "Usas la transcripción y el código original como evidencia; adaptas ejemplos, diagramas y tareas "
           "al nivel y a la materia. No inventas APIs, métodos, resultados, citas ni mediciones. "
           "Separas el contenido del curso de los complementos. No afirmas verificar algo que no comprobaste.")

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
    video = video or editorial.resolver_video(carpeta)
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
                with open(r, encoding="utf-8", errors="replace") as archivo_sub:
                    subs[idioma] = leer_srt(archivo_sub.read())
                break
    if video and os.path.isfile(video) and not subs:
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
        # los subtítulos automáticos de YouTube no llevan puntuación: sin el corte por tiempo (cada + 15 s)
        # toda la clase quedaba en UN párrafo a 0:02 y la IA perdía los tiempos
        if a - t0 >= cada and (re.search(r"[.?!]$", t) or a - t0 >= cada + 15):
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
class _Plantilla(str):
    """PROMPT.format(...) añade solo las reglas que dependen de la duración (regla_secciones/extras/resumen)."""
    def format(self, **kw):
        d = kw.get("duracion")
        seg = a_segundos(d) if isinstance(d, str) and d else float(d or 0)
        kw.setdefault("regla_secciones", regla_secciones(seg))
        kw.setdefault("regla_extras", regla_extras(seg))
        kw.setdefault("regla_resumen", regla_resumen(seg))
        kw.setdefault("regla_presupuesto", regla_presupuesto(seg))
        return str.format(self, **kw)


with open(os.path.join(AQUI, "apuntes-prompt-v5.txt"), encoding="utf-8") as _prompt:
    PROMPT = _Plantilla(_prompt.read())

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
    # 08/11/2026: probado en la misma clase de 10 min: claude-haiku-5-5 37 s y el más fiel (cifras, posiciones y colores exactos),
    # gpt-6-luna 28 s pero parafrasea el código, deepseek-v4.1-flash 90 s, glm-5.3-flash 85 s. Por eso va primero haiku.
    # 08/11/2026: la cuota de OpenCode Go está agotada (semanal/mensual). Por defecto solo los gratuitos que responden
    # (probados: beam-free y crouton-alpha-free contestan en ~5 s; glm-5.3-flash-free ya dice "Free usage limit reached").
    "APUNTES_MODELO_OPENCODE",
    "opencode-go/longcat-2.5-free,opencode-go/iceman-contributor-free,opencode-go/beam-free,"
    "opencode/iceman-free,opencode/inkling-2-small-free,opencode/longcat-2.5-free,opencode/flint-40b-free,"
    "opencode/minimax-m3.1-flash-free,opencode/deepseek-v4.1-flash-free,opencode/nemotron-3.5-super-vl-free,"
    "opencode/beam-free,opencode/mimo-v2.6-flash-free,opencode/glm-5.3-flash-free,"
    "opencode-go/gpt-6-luna,opencode-go/minimax-m3.1-flash,opencode-go/deepseek-v4.1-flash,"
    "opencode-go/mimo-v2.5,opencode-go/qwen3.8-flash,opencode-go/glm-5.3-flash,opencode-go/muse-spark-1.3-contributor",
).split(",") if m.strip()]
MODELO_OPENCODE = MODELOS_OPENCODE[0] if MODELOS_OPENCODE else ""


def nombre_motor():
    """Etiqueta para los mensajes: "Claude (sonnet)" u "OpenCode (opencode-go/kimi-k3)"."""
    if MOTOR == "codex":
        return f"Codex ({CODEX_MODELO}, {CODEX_EFFORT})"
    if MOTOR == "opencode":
        if RESPALDO:
            return f"OpenCode ({MODELO_OPENCODE or 'modelo de la cuenta'}) → Claude {RESPALDO} si falla"
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
    lig = es_ligera(titulo, duracion)
    if not lig and duracion >= SEG_TROCEO and os.environ.get("APUNTES_SIN_TROCEO") != "1":
        return pedir_por_tramos(titulo, duracion, cues, pantallas, codigo)  # v8: videos largos, una llamada por tramo
    if lig:  # bienvenida / instalación / despedida / clase muy corta: apunte mínimo
        cant = dict(n_preg=2, n_pre=0, n_ejer=0, n_err=0, n_diag=0, n_voc=0, tope=90, rango_diag="ninguno")
    else:
        cant = dict(n_preg=n_preguntas(duracion), n_pre=n_pretest(duracion), n_ejer=n_ejercicios(duracion),
                    n_err=n_errores(duracion), n_diag=n_diagramas(duracion), n_voc=n_vocabulario(duracion),
                    tope=tope_palabras(duracion), rango_diag=rango_diagramas(duracion))
    prompt = PROMPT.format(titulo=titulo, duracion=hms(duracion), **cant, transcripcion=transcripcion,
                           pantallas=extra + (f"\nMaterial que entrega el curso (recursos.py):\n<<<\n{codigo}\n>>>\n" if codigo else ""))
    prompt += REGLA_LIGERA if lig else ""
    pobre = None
    for intento in range(3):  # v8: 3 intentos (una respuesta inválida suelta no debe dejar la clase sin IA)
        texto = consultar_ia(prompt) or ""  # v9c: sin respuesta de la IA → reintento, no un AttributeError
        try:
            datos = json.loads(texto[texto.index("{"):texto.rindex("}") + 1])
            if isinstance(datos, dict) and not datos.get("secciones") and datos.get("resumen"):
                # v8: con sin_contenido=true la IA deja la información en `resumen` y ninguna sección → no se tira, se rescata
                datos["secciones"] = [{"inicio": "0:00", "titulo": titulo_propio(titulo) or "Contenido", "relevancia": "raro",
                                       "puntos": [str(x) for x in datos["resumen"]][:5]}]
            # los modelos débiles a veces mandan secciones sin título: se reintenta en vez de romper el armado
            if datos.get("secciones") and all(isinstance(x, dict) and x.get("titulo") for x in datos["secciones"]):
                if lig:
                    aplicar_ligera(datos)
                else:
                    aplicar_perfil(datos, duracion)
                    fuente = " ".join(c[-1] for c in cues) + " " + " ".join(x for _, x in pantallas) + " " + (codigo or "")
                    quitadas = verificar_fidelidad(datos, fuente)
                    if quitadas:
                        print(f"   🧹 {quitadas} afirmaciones sin respaldo en el video quitadas")
                    etiquetar_pantalla(datos, " ".join(c[-1] for c in cues), " ".join(x for _, x in pantallas))
                verificar_salidas(datos)
                verificar_practica(datos)
                if not lig and duracion >= 480 and len(datos["secciones"]) < 3 and intento < 2:
                    # v10: un video de 8+ min con 1-2 secciones pierde detalle (medido en OpenCode): un reintento pidiendo más
                    pobre = pobre or datos
                    prompt += "\n\nATENCIÓN: la respuesta anterior tenía muy pocas secciones. Esta clase dura más de 8 minutos: divide en AL MENOS 3 secciones de temas distintos, cada una con su marca de tiempo."
                    print(f"  (solo {len(datos['secciones'])} secciones para {hms(duracion)}: reintento pidiendo más)", file=sys.stderr)
                    continue
                return datos
        except (ValueError, TypeError, json.JSONDecodeError):
            pass
        print(f"  (respuesta de Claude inválida, intento {intento + 1})", file=sys.stderr)
    return pobre


SEG_TROCEO = 3600  # v8: desde 1 h, una llamada por tramo (una sola llamada dejaba horas enteras sin cubrir)


def _json_de(texto):
    try:
        return json.loads(texto[texto.index("{"):texto.rindex("}") + 1])
    except (ValueError, TypeError, json.JSONDecodeError):
        return None


def _prompt_para(titulo, duracion, lineas, pantallas, codigo, **reglas):
    transcripcion = "Transcripción con marcas de tiempo [h:mm:ss]:\n<<<\n" + "\n".join(lineas) + "\n>>>\n"
    extra = ""
    if pantallas:
        extra = ("\nTexto leído de la PANTALLA (OCR, puede tener errores de lectura) en algunos momentos;"
                 " sirve para el código exacto y los datos que se ven:\n<<<\n"
                 + "\n\n".join(f"[{hms(t)}]\n{txt}" for t, txt in pantallas) + "\n>>>\n")
    if codigo:
        extra += f"\nMaterial que entrega el curso (recursos.py):\n<<<\n{codigo}\n>>>\n"
    cant = dict(n_preg=n_preguntas(duracion), n_pre=n_pretest(duracion), n_ejer=n_ejercicios(duracion),
                n_err=n_errores(duracion), n_diag=n_diagramas(duracion), n_voc=n_vocabulario(duracion),
                tope=tope_palabras(duracion), rango_diag=rango_diagramas(duracion))
    cant.update(reglas)
    return PROMPT.format(titulo=titulo, duracion=hms(duracion), transcripcion=transcripcion, pantallas=extra, **cant)


def pedir_por_tramos(titulo, duracion, cues, pantallas, codigo=""):
    """Video largo: cada tramo (20-25 min) se resume por separado (secciones con SU parte del video y cobertura
    completa) y una última llamada arma el repaso global (corto, práctica, errores, glosario) desde esas secciones."""
    largo_tramo = (25 if duracion >= 7200 else 20) * 60
    n = max(2, int(round(duracion / largo_tramo)))
    largo_tramo = duracion / n
    lineas_todas = [(t, f"[{hms(t)}] {txt}") for t, txt in parrafos(cues, cada=30)]
    secciones, falta = [], []
    frac_tope = tope_palabras(duracion) / max(1, n)
    for k in range(n):
        t0, t1 = k * largo_tramo, (k + 1) * largo_tramo
        lineas = [l for t, l in lineas_todas if t0 <= t < t1 or (k == n - 1 and t >= t0)]
        pant = [(t, x) for t, x in pantallas if t0 <= t < t1 or (k == n - 1 and t >= t0)]
        if not lineas and not pant:
            continue
        print(f"   tramo {k + 1}/{n} ({hms(t0)}–{hms(t1)})", flush=True)
        reglas = dict(n_preg=0, n_pre=0, n_ejer=0, n_err=0, n_voc=0, tope=int(max(150, frac_tope)),
                      n_diag=max(0, round(n_diagramas(duracion) / n)), rango_diag="como máximo 1",
                      regla_secciones=((f"1 o 2 secciones para ESTE tramo (cada una de 6 a 12 min)" if duracion < 7200 else
                                        f"1 a 3 secciones para ESTE tramo (cada una de 8 a 15 min)") +
                                       "; ninguna de más de 8 min con menos de 3 puntos. Cubre TODO el tramo: cada tema o herramienta que se explica "
                                       "tiene su sección y no queda ningún hueco de más de 8 min. Marcas de tiempo absolutas del "
                                       "video completo."),
                      regla_resumen="Para `corto` basta idea de una frase y 2 puntos en `esencial`; el repaso global se arma después.",
                      regla_extras="No incluyas ejemplos resueltos, comparativas, conceptos ni vocabulario; solo secciones con puntos y código.")
        prompt = _prompt_para(f"{titulo} (tramo {k + 1} de {n}, {hms(t0)}–{hms(t1)})", largo_tramo, lineas, pant,
                              codigo if k == 0 else "", **reglas)
        # las marcas deben ser las del video completo: el prompt usa la duración del tramo solo para los topes
        datos = None
        for intento in range(3):
            d = _json_de(consultar_ia(prompt) or "")
            if d and d.get("secciones") and all(isinstance(x, dict) and x.get("titulo") for x in d["secciones"]):
                datos = d
                break
            print(f"  (tramo {k + 1}: respuesta inválida, intento {intento + 1})", file=sys.stderr)
        if not datos:
            falta.append((t0, t1))
            secciones.append({"inicio": hms(t0), "titulo": f"Tramo {hms(t0)}–{hms(t1)} (sin resumen de IA)", "relevancia": "raro",
                              "puntos": ["La IA no devolvió el resumen de este tramo; consulta la transcripción."]})
            continue
        for s in datos["secciones"]:
            try:
                ini = a_segundos(str(s.get("inicio", "0")))
            except ValueError:
                ini = t0
            if not (t0 - 60 <= ini <= t1 + 60):   # marcas relativas al tramo → se corrigen al video completo
                ini = t0 + min(ini, largo_tramo)
            s["inicio"] = hms(max(0, ini))
            for campo in ("ejemplo", "comparativa"):
                s[campo] = None
            secciones.append(s)
    if not secciones:
        return None
    secciones.sort(key=_seg_seccion)
    esquema = [f"[{s['inicio']}] {s['titulo']}: " + " ".join(str(x) for x in (s.get("puntos") or [])[:4]) for s in secciones]
    prompt = _prompt_para(titulo, duracion, esquema, [], "",
                          regla_secciones="deja `secciones` con UNA sola sección mínima (ya están hechas aparte); concéntrate en lo global.")
    prompt = ("NOTA: en lugar de la transcripción recibes el ESQUEMA de secciones ya resumidas del video completo; úsalo para el repaso "
              f"global (idea, esencial por bloques, chuleta, preguntas, pretest, práctica, errores, conceptos). Devuelve EXACTAMENTE "
              f"{n_preguntas(duracion)} preguntas en `corto.preguntas`, repartidas por TODO el video (una por cada ~{max(5, int(duracion / 60 / max(1, n_preguntas(duracion))))} min), "
              "incluidas las últimas partes; elige el código mínimo y la chuleta de todo el video, no solo del principio.\n") + prompt
    glob = None
    for intento in range(3):
        d = _json_de(consultar_ia(prompt) or "")
        if d and isinstance(d.get("corto"), dict):
            glob = d
            break
        print(f"  (repaso global: respuesta inválida, intento {intento + 1})", file=sys.stderr)
    if not glob or len(falta) > max(1, n // 4):
        # v9c: si la IA falló (cuota agotada…) en el repaso global o en más de 1/4 de los tramos, NO se guarda un apunte degradado
        # como terminado: se devuelve None y la clase queda pendiente de rehacer
        print("  (la IA falló en demasiados tramos o en el repaso global: no se guarda un apunte incompleto)", file=sys.stderr)
        return None
    glob["secciones"] = secciones
    glob.pop("sin_contenido", None)
    aplicar_perfil(glob, duracion)
    fuente = " ".join(c[-1] for c in cues) + " " + " ".join(x for _, x in pantallas) + " " + (codigo or "")
    quitadas = verificar_fidelidad(glob, fuente)
    if quitadas:
        print(f"   🧹 {quitadas} afirmaciones sin respaldo en el video quitadas")
    verificar_salidas(glob)
    verificar_practica(glob)
    if falta:
        glob["_tramos_sin_resumen"] = [f"{hms(a)}–{hms(b)}" for a, b in falta]
    return glob


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


# ------------------------------------------------------- clases ligeras ---
# Decisión del usuario (07/11/2026): bienvenidas, introducciones al curso, instalaciones y despedidas
# "con ver el video recordaré" → apunte mínimo (1 sección, pasos/comandos clave), sin ejercicios ni glosario.
LIGERA = re.compile(r"bienvenid|presentaci[oó]n|introducci[oó]n al curso|despedid|cierre|conclusi[oó]n|certificad|requisitos"
                    r"|material(es)? del curso|qu[eé] vas a aprender|agradecim|pr[oó]ximos pasos|siguientes pasos"
                    r"|instalaci[oó]n|instalando|instalar |configuraci[oó]n del entorno|preparaci[oó]n del entorno"
                    r"|welcome|goodbye|\bsetup\b|\binstall", re.I)
SEG_LIGERA = 120  # más cortas que esto: siempre ligeras (v8: 150 → 120; de 2 a 4 min manda la curva, sin andamiaje)
REGLA_LIGERA = """

CLASE LIGERA (bienvenida, introducción, instalación, despedida o clase muy corta): el alumno ya verá el video y lo recordará.
- UNA sola sección con 2 a 5 puntos MUY breves (qué se hace / qué se necesita) que conserven TODA cifra, versión, herramienta, requisito y alternativa que se mencione.
- Si es una instalación o configuración: lista corta de los pasos y comandos clave EXACTOS (en un bloque de código si hay comandos).
- Sin ejercicios, sin errores comunes, sin glosario ni vocabulario, sin diagramas, sin comparativas, sin ejemplos resueltos.
- corto.pretest vacío; 2 preguntas de DATO concreto (cifra, requisito, alternativa, advertencia) en corto.preguntas. Si no hay nada que rescatar, usa "sin_contenido".
"""


def titulo_propio(nombre):
    """Título de la clase sin la sección: "02 Instalación… - 05 Visual Studio Code" → "05 Visual Studio Code"."""
    return (nombre or "").rsplit(" - ", 1)[-1]


def es_ligera(titulo, duracion=0):
    if duracion and duracion >= 900:  # un video de 15 min o más nunca es "ligero" aunque diga "instalación" en el título
        return False
    return bool(duracion and duracion < SEG_LIGERA) or bool(LIGERA.search(titulo_propio(titulo)))


def aplicar_ligera(datos):
    """Deja en el JSON solo lo que le toca a una clase ligera (aunque la IA haya mandado más)."""
    for k in ("practica", "errores_comunes", "vocabulario", "conceptos"):
        datos[k] = []
    datos["secciones"] = (datos.get("secciones") or [])[:1]
    for s in datos["secciones"]:
        s["diagrama"], s["comparativa"], s["ejemplo"] = "", None, None
    (datos.get("corto") or {}).pop("pretest", None)
    datos["ligera"] = True


def _seg_seccion(s):
    try:
        return a_segundos(str(s.get("inicio", "0")))
    except ValueError:
        return 0


def fusionar_secciones(datos, segundos):
    """Una sección de pocos segundos o con un solo punto y sin código se une a la anterior (no hay secciones-migaja)."""
    m = segundos / 60
    if m < 8:
        return
    minimo = (5 if m >= 120 else 3) * 60
    secs = [s for s in datos.get("secciones") or [] if isinstance(s, dict)]
    secs.sort(key=_seg_seccion)
    piso = 3 if m < 20 else max(3, int(-(-m // 12)))  # v9d: un video de 12 min nunca queda en una sola sección
    sal = []
    for k, s in enumerate(secs):
        fin = _seg_seccion(secs[k + 1]) if k + 1 < len(secs) else segundos
        corta = fin - _seg_seccion(s) < minimo
        migaja = len(s.get("puntos") or []) <= 1 and not str(s.get("codigo") or "").strip()
        if sal and (migaja or (corta and not str(s.get("codigo") or "").strip())) and len(sal) + (len(secs) - k - 1) >= piso:
            prev = sal[-1]
            prev["puntos"] = list(prev.get("puntos") or []) + list(s.get("puntos") or [])
            if not prev.get("diagrama") and s.get("diagrama"):
                prev["diagrama"] = s["diagrama"]
            continue
        sal.append(s)
    datos["secciones"] = sal
    # v8: tope duro de secciones por duración; se une la más corta con la anterior (puntos y código se conservan)
    tope = 6 if m < 45 else 10 if m < 120 else 35
    while len(sal) > tope:
        durs = [((_seg_seccion(sal[k + 1]) if k + 1 < len(sal) else segundos) - _seg_seccion(sal[k]), k) for k in range(1, len(sal))]
        _, k = min(durs)
        prev, cur = sal[k - 1], sal.pop(k)
        prev["puntos"] = list(prev.get("puntos") or []) + [f"**{cur.get('titulo', '')}:**"] * 0 + list(cur.get("puntos") or [])
        if str(cur.get("codigo") or "").strip():
            if not str(prev.get("codigo") or "").strip():
                prev["codigo"], prev["lenguaje"] = cur["codigo"], cur.get("lenguaje")
            elif (prev.get("lenguaje") or "") == (cur.get("lenguaje") or ""):
                prev["codigo"] = str(prev["codigo"]).rstrip("\n") + "\n\n" + str(cur["codigo"])
        if not prev.get("diagrama") and cur.get("diagrama"):
            prev["diagrama"] = cur["diagrama"]
        prev["titulo"] = f"{prev.get('titulo', '')} y {str(cur.get('titulo', '')).lower()}" if len(prev.get("titulo", "")) < 55 else prev.get("titulo", "")
    datos["secciones"] = sal


META = re.compile(r"no se confirma|dato (dudoso|no verificado|no confirmado)|no aparece en (la|las) (fuente|transcripci)|seg[úu]n la transcripci[oó]n|"
                  r"transcripci[oó]n (dudosa|poco clara|ambigua)|la transcripci[oó]n (dice|indica|muestra|parece)", re.I)


def _norm_num(x):
    return re.sub(r"[.,\s]", "", x)


def etiquetar_pantalla(datos, voz, ocr):
    """v10: un punto cuyos datos concretos (cifras, `código`, nombres con dígitos) están en la PANTALLA (OCR) y en nada de lo que dijo el
    profe se marca *(pantalla)*: el alumno distingue lo que el profe argumenta de lo que solo se ve. Si la voz y la pantalla chocan,
    el prompt manda la voz."""
    v, o = voz.lower(), ocr.lower()
    n = 0
    for s in datos.get("secciones") or []:
        if not isinstance(s, dict):
            continue
        nuevos = []
        for p in s.get("puntos") or []:
            t = str(p)
            toks = {x.lower() for x in re.findall(r"`([^`]{3,40})`", t)} | {x.lower() for x in re.findall(r"\b[\w.-]*\d[\w.-]*\b", t) if len(x) >= 3}
            if (toks and "(pantalla)" not in t and not t.lstrip().lower().startswith("pantalla")
                    and all(k in o for k in toks) and not any(k in v for k in toks)):
                t += " *(pantalla)*"
                n += 1
            nuevos.append(t)
        s["puntos"] = nuevos
    return n


def verificar_fidelidad(datos, fuente):
    """v9c: lo que NO sale del video se quita. Una viñeta/pregunta se descarta si trae (a) una cifra de 3+ dígitos, un decimal o una
    notación 1e-3 que no está en la transcripción/OCR/material, o (b) un `identificador` entre backticks (5+ letras) que tampoco
    está. También se quitan las viñetas que son puro meta-aviso ('la transcripción dice…', 'dato no verificado'). Devuelve cuántas quitó."""
    f = (fuente or "").lower()
    f_sin = re.sub(r"[-\s]", "", f)
    f_ent = "".join(c for c in unicodedata.normalize("NFD", f) if unicodedata.category(c) != "Mn")
    nums = {_norm_num(x) for x in re.findall(r"\d[\d.,]*", f)}
    quitadas = [0]

    def ok(txt):
        txt = str(txt or "")
        if META.search(txt):
            return False
        for n in re.findall(r"\d+[.,]\d+|\d+e-?\d+|\d{4,}", txt):  # v9d: 4+ dígitos (3 dígitos daba falsos positivos: se dicen en voz)
            if re.fullmatch(r"[01]+", n) or (_norm_num(n) in nums) or n.lower() in f:  # los binarios 0110/1100 se dictan, no se escriben
                continue
            return False
        sin_tilde = lambda s: "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
        for ent in re.findall(r"\b[a-z]+[A-Z]\w+\b|\b[A-Z][a-z]+[A-Z]\w*\b|(?<=[a-záéíóúñ,;:] )[A-ZÁÉÍÓÚÑ][a-záéíóúñ]{5,}\b", txt):
            b = sin_tilde(ent.lower())
            if b not in f_ent and b.rstrip("s") not in f_ent:
                return False
        for pc in re.findall(r"\d+(?:[.,]\d+)?\s?%", txt):  # v9e: los porcentajes ("67 %") también deben salir del video
            num = re.sub(r"[\s%]", "", pc).replace(",", ".")
            if not re.search(r"(?<![\d.,])" + re.escape(num).replace(r"\.", r"[.,]") + r"\s?(%|por ?ciento)", f):
                return False
        for tok in re.findall(r"\b[A-Za-z]+-?\d+[A-Za-z]*\b|\b\d+[A-Za-z]+\b", txt):
            base = re.sub(r"[-\s]", "", tok.lower())
            if len(base) >= 3 and base not in f_sin and not base.isdigit():
                return False
        for ident in re.findall(r"`([A-Za-z_][\w.]{4,})(?:\(\))?`", txt):
            base = ident.split(".")[-1].lower()
            if len(base) >= 5 and base not in f:
                return False
        return True

    for s in datos.get("secciones") or []:
        if isinstance(s, dict) and s.get("puntos"):
            buenos = [p for p in s["puntos"] if ok(p)]
            quitadas[0] += len(s["puntos"]) - len(buenos)
            s["puntos"] = buenos or s["puntos"][:1]  # una sección nunca queda sin nada
    # v9e: también el resumen ("En 30 segundos"), objetivos, porqués, ejemplos, errores, conceptos y comparativas
    for campo in ("resumen", "objetivos"):
        if isinstance(datos.get(campo), list):
            buenos = [x for x in datos[campo] if ok(x)]
            quitadas[0] += len(datos[campo]) - len(buenos)
            datos[campo] = buenos
    for s in datos.get("secciones") or []:
        if not isinstance(s, dict):
            continue
        for campo in ("porque", "intuicion"):
            if s.get(campo) and not ok(s[campo]):
                s[campo] = ""
                quitadas[0] += 1
        ej = s.get("ejemplo")
        if isinstance(ej, dict) and not all(ok(x) for x in [ej.get("enunciado"), ej.get("salida")] + list(ej.get("pasos") or [])):
            s["ejemplo"] = None
            quitadas[0] += 1
        comp = s.get("comparativa")
        if isinstance(comp, dict) and not all(ok(c) for fila in comp.get("filas") or [] for c in fila):
            s["comparativa"] = None
            quitadas[0] += 1
    for campo, claves in (("errores_comunes", ("error", "porque", "arreglo")), ("conceptos", ("termino", "definicion"))):
        if isinstance(datos.get(campo), list):
            buenos = [e for e in datos[campo] if not isinstance(e, dict) or all(ok(e.get(k)) for k in claves)]
            quitadas[0] += len(datos[campo]) - len(buenos)
            datos[campo] = buenos
    corto = datos.get("corto")
    if isinstance(corto, dict):
        buenas = [e for e in corto.get("esencial") or [] if ok(e)]
        quitadas[0] += len(corto.get("esencial") or []) - len(buenas)
        corto["esencial"] = buenas
        qs = [q for q in corto.get("preguntas") or [] if isinstance(q, dict) and ok(q.get("pregunta")) and ok(q.get("respuesta"))]
        quitadas[0] += len(corto.get("preguntas") or []) - len(qs)
        corto["preguntas"] = qs
    return quitadas[0]


def _limitar_codigo(datos, segundos):
    """v9c: en videos largos el código de cada sección no pasa de 15 líneas (CSS: 8); no se vuelcan hojas de estilo enteras."""
    m = segundos / 60
    if m < 45:
        return
    for s in datos.get("secciones") or []:
        cod = str(s.get("codigo") or "")
        lim = 8 if str(s.get("lenguaje") or "").lower() in ("css", "scss") else 15
        lineas = cod.split("\n")
        if len(lineas) > lim:
            s["codigo"] = "\n".join(lineas[:lim] + ["…"])
            s["linea_a_linea"] = []


def aplicar_perfil(datos, segundos):
    """v8: hace cumplir la curva de la duración aunque la IA no obedezca el prompt (topes, piezas que no van, secciones-migaja)."""
    m = segundos / 60
    datos["practica"] = (datos.get("practica") or [])[:n_ejercicios(segundos)]
    datos["errores_comunes"] = (datos.get("errores_comunes") or [])[:n_errores(segundos)]
    datos["vocabulario"] = (datos.get("vocabulario") or [])[:n_vocabulario(segundos)]
    datos["conceptos"] = [] if m < 60 else (datos.get("conceptos") or [])[:6]
    # ejemplos, comparativas y diagramas: máximos por duración
    max_ej = 0 if m < 5 else 2 if m < 20 else 3 if m < 45 else max(2, int(m // 40))
    max_comp = 0 if m < 5 else 1 if m < 120 else max(1, int(m // 60))
    max_diag = n_diagramas(segundos)
    for s in datos.get("secciones") or []:
        if not isinstance(s, dict):
            continue
        if s.get("ejemplo"):
            if max_ej > 0:
                max_ej -= 1
            else:
                s["ejemplo"] = None
        if s.get("comparativa"):
            if max_comp > 0:
                max_comp -= 1
            else:
                s["comparativa"] = None
        if s.get("diagrama"):
            if max_diag > 0:
                max_diag -= 1
            else:
                s["diagrama"] = ""
    for s in datos.get("secciones") or []:  # ejemplo que solo repite un bloque corto, y tablas de una sola fila: ruido
        if isinstance(s, dict):
            if s.get("ejemplo") and str(s.get("codigo") or "").strip() and len(str(s["codigo"]).strip().split("\n")) <= 8:
                s["ejemplo"] = None
            comp = s.get("comparativa")
            if isinstance(comp, dict) and len(comp.get("filas") or []) < 2:
                s["comparativa"] = None
    _limitar_codigo(datos, segundos)
    fusionar_secciones(datos, segundos)
    corto = datos.get("corto")
    if isinstance(corto, dict):
        corto["preguntas"] = (corto.get("preguntas") or [])[:n_preguntas(segundos)]
        corto["pretest"] = (corto.get("pretest") or [])[:n_pretest(segundos)]
        corto["esencial"] = (corto.get("esencial") or [])[:3 if m < 20 else 5 if m < 45 else 8]
        if m < 8:
            corto["chuleta"] = []
        if m < 45:
            corto["codigo"], corto["mapa"], corto["diagrama"] = [], [], ""
        elif m < 120:
            corto["codigo"], corto["diagrama"] = (corto.get("codigo") or [])[:1], ""


def verificar_practica(datos):
    """Las soluciones de práctica con código JS/Python se ejecutan (bwrap, sin red): e["verificada"] = True si
    corren sin error, False si fallan por un error propio (sintaxis, nombre, tipo), sin marcar si dependen del
    navegador o de entrada del usuario."""
    try:
        ri = None
        for e in datos.get("practica") or []:
            if not isinstance(e, dict):
                continue
            sol = str(e.get("solucion") or "")
            m = re.search(r"```(js|javascript|node|py|python|python3)\s*\n(.*?)```", sol, re.S | re.I)
            if not m:
                continue
            lang = "js" if m.group(1).lower() in ("js", "javascript", "node") else "python"
            codigo = m.group(2)
            ri = ri or _repo_img()
            if ri.NO_EJECUTAR.search(re.sub(r"(//|#).*", "", codigo)):
                continue
            ok, out = ri.ejecutar(codigo, lang)
            if ok:
                e["verificada"] = True
            elif re.search(r"SyntaxError|ReferenceError|TypeError|NameError|IndentationError|AttributeError", out or ""):
                e["verificada"] = False
                e["error_ejecucion"] = (out or "").strip().splitlines()[-1][:200]
    except Exception as ex:  # nunca rompe los apuntes
        print(f"  (no se pudo comprobar la práctica: {ex})", file=sys.stderr)


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
    if not opencode_enfriando():  # primera vez en esta ventana: avisar al usuario (una sola notificación)
        try:
            subprocess.run(["notify-send", "-u", "critical", "-t", "10000", "OpenCode Go: cuota agotada",
                            "Sigo con el respaldo (Claude) si lo hay; si no, la clase queda para reintentar."], timeout=5)
        except (OSError, subprocess.SubprocessError):
            pass
    try:
        os.makedirs(os.path.dirname(AGOTADO_OC), exist_ok=True)
        open(AGOTADO_OC, "w").close()
    except OSError:
        pass


CODEX = os.environ.get("APUNTES_CODEX", "1" if MOTOR == "codex" else "0") != "0"  # motor principal si APUNTES_MOTOR=codex; respaldo opcional en otros modos
CODEX_MODELO = os.environ.get("APUNTES_CODEX_MODELO", "gpt-6-luna")
CODEX_EFFORT = os.environ.get("APUNTES_CODEX_EFFORT", "none")  # Luna admite none: mínimo consumo de razonamiento
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
               "-o", salida] + (["-m", CODEX_MODELO] if CODEX_MODELO else [])
        if CODEX_EFFORT:
            cmd += ["-c", f'model_reasoning_effort="{CODEX_EFFORT}"']
        cmd += ["-"]
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
    if MOTOR == "codex":
        return llamar_codex(prompt)  # una llamada directa, sin reintentos ni otros proveedores
    if MOTOR == "opencode":
        # Cadena (v10): 1) modelos de OpenCode Go en orden (haiku-5-5 primero), 2) Claude RESPALDO si OpenCode falla o se agotó
        # (usa TU plan de Claude; APUNTES_RESPALDO= lo desactiva); antes iba al revés. Detalle anterior: modelos de
        # OpenCode Go en orden (MODELOS_OPENCODE; el gratuito LongCat va al final: se cuelga seguido).
        # Cada paso falla rápido (timeout corto, sin esperar cuota) y se pasa al siguiente. Si TODOS
        # fallan se repite la cadena tras una pausa (los cuelgues suelen ser pasajeros); si aun así
        # no hay respuesta, la clase sigue sin IA y rehacer-sin-ia.py la rehace al final del curso.
        for ronda in range(RONDAS_CADENA):
            if ronda:
                print(f"  (todos los modelos fallaron: reintento la cadena en {PAUSA_CADENA} s, ronda {ronda + 1}/{RONDAS_CADENA})", file=sys.stderr)
                reportar(75, "apuntes", "reintentando la IA")
                time.sleep(PAUSA_CADENA)
            # Orden (pedido del usuario): 1) modelos GRATUITOS de OpenCode (todos los disponibles), 2) modelos de
            # OpenCode Go de mejor calidad/precio, 3) haiku de Claude Code como respaldo, 4) Codex (si está encendido).
            # Sin sonnet: la cuota de sonnet se agota rápido.
            texto = None if opencode_enfriando() else llamar_opencode(prompt, max_espera=0)
            if texto is not None:
                return texto
            if RESPALDO:
                extra = ["--effort", RESPALDO_EFFORT] if RESPALDO_EFFORT else []
                cmd = [ruta_claude(), "-p", "--output-format", "json", "--tools", "", "--strict-mcp-config",
                       "--no-session-persistence", "--system-prompt", SISTEMA, "--model", RESPALDO] + extra
                texto = llamar_claude(cmd, prompt, max_espera=0, timeout=TIMEOUT_CLAUDE)
                if texto is not None:
                    return texto
                print(f"  (Claude {RESPALDO} no respondió: reintento OpenCode)", file=sys.stderr)
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
def _top_puntos(puntos, k):
    """Se queda con k puntos, en su orden; los que traen cifras, código o un 'no/nunca/siempre' (datos duros) se salvan primero."""
    puntos = list(puntos)
    if len(puntos) <= k:
        return puntos
    duro = [i for i, p in enumerate(puntos) if re.search(
        r"\d|`|\b(nunca|siempre|no se|no uses|no lo|evita|evitar|ojo|cuidado|advert\w*|recomiend\w*|recomendad\w*|conclus\w*|importante|error|requisito\w*)\b",
        str(p), re.I)]
    elegidos = set(duro[:k]) | set(range(max(0, k - len(duro))))
    return [p for i, p in enumerate(puntos) if i in elegidos][:k]


def _tokens_en_codigo(md):
    """v9b: tokens como <|reward|> o <script> sueltos (fuera de bloques y de `código`) se pierden al verse como HTML: van entre
    backticks. No toca lo que ya está entre backticks, los destinos de enlaces ](<…>) ni los comentarios HTML."""
    def envolver(trozo):
        return re.sub(r"(?<![`\w(<])<(?![<!])(/?[\w|][^<>`\n]{0,40})>(?![`>)])", lambda m: f"`<{m.group(1)}>`", trozo)
    sal, en_codigo = [], False
    for l in md.split("\n"):
        if l.lstrip("> ").startswith("```"):
            en_codigo = not en_codigo
        elif not en_codigo and "<" in l and not l.lstrip().startswith("<!--"):
            partes = re.split(r"(`[^`\n]*`|\]\(<[^)\n]*>\)|<<[^<>\n]*>>)", l)  # lo protegido queda como está
            l = "".join(p if k % 2 else envolver(p) for k, p in enumerate(partes))
        sal.append(l)
    return "\n".join(sal)


NIVELES = 10  # 0 todo · 1-3 pliega · 4-6 recorta lo de adorno · 7-9 recorta hasta cumplir sí o sí (v10)
LINEAS_CODIGO = {8: 14, 9: 8}


def _cortar_codigo(codigo, maximo, fin, lenguaje=""):
    """Código largo → las primeras líneas hasta una frontera completa (paréntesis y llaves cerrados) + un comentario que manda al video.
    Nunca corta a mitad de estructura ni por 1-3 líneas; JSON/YAML/TOML no se parten (se dejan enteros o, si son enormes, solo
    el comentario). La marca de tiempo no pasa de la duración de la clase."""
    lineas = str(codigo or "").strip("\n").split("\n")
    lang = str(lenguaje or "").lower().strip()
    if len(lineas) <= maximo + 3:
        return codigo
    if lang in ("json", "yaml", "yml", "toml", "xml", "html"):
        return codigo if len(lineas) <= 40 else ""
    abre, cierra = COMENTARIO.get(lang, ("//", ""))
    corte = maximo
    prof = 0
    mejor = None
    for k, l in enumerate(lineas[:maximo + 8]):
        prof += sum(l.count(c) for c in "({[") - sum(l.count(c) for c in ")}]")
        if prof <= 0 and k + 1 <= maximo + 3:
            mejor = k + 1
    corte = mejor or maximo
    if corte >= len(lineas) - 1:
        return codigo
    return "\n".join(lineas[:corte] + [f"{abre} 👉 +{len(lineas) - corte} líneas: completo en el video{cierra}"])


def _recortar(datos, secciones, nivel):
    """v9: si el apunte se pasa del presupuesto de lectura, se RECORTA (no solo se pliega) lo menos importante, de a poco.
    v10 (08/11/2026): los niveles 7-9 cumplen el presupuesto aunque haya que tocar lo ⭐ y el código (antes el nivel 6
    se quedaba corto en 134 de 141 clases de un curso real). Opera sobre copias: .apuntes-ia.json conserva todo."""
    if nivel < 4 or not datos:
        return datos, secciones
    import copy
    d, sec = copy.deepcopy(datos), copy.deepcopy(secciones)
    for k, s in enumerate(sec):
        diario = s.get("relevancia") == "diario"
        cierre = k == len(sec) - 1  # v9c: el cierre del video (resultados, conclusiones, advertencias) pierde menos
        base = {4: 5, 5: 4, 6: 3, 7: 3, 8: 2, 9: 2}[nivel]
        s["puntos"] = _top_puntos(s.get("puntos") or [], base + (1 if diario and nivel < 8 else 0) + ((2 if nivel < 8 else 1) if cierre else 0))
        if not diario or nivel >= 7:
            s["intuicion"] = ""
            if nivel >= 8:
                s["porque"] = ""  # v10: el "por qué" del profe es lo último que se recorta
            if nivel >= 5:
                s["ejemplo"], s["comparativa"], s["diagrama"] = None, None, ""
        if nivel >= 8:  # v10: los comentarios 👉 del código se conservan hasta el último recurso (explican el porqué de cada línea)
            s["linea_a_linea"] = []
            if s.get("relevancia") == "raro" and len(sec) > 1:
                s["codigo"] = ""
            s["codigo"] = _cortar_codigo(s.get("codigo"), LINEAS_CODIGO[nivel], s.get("fin", 0), s.get("lenguaje"))
    if nivel >= 5:
        d["errores_comunes"] = (d.get("errores_comunes") or [])[:1] if nivel == 5 else []
        d["practica"] = (d.get("practica") or [])[:1] if nivel < 7 else []
    if nivel >= 7:
        d["conceptos"], d["vocabulario"], d["objetivos"] = [], [], []
    return d, sec


# v10: lo que habla del PROCESO (OCR, capturas, el apunte anterior) y no del tema es ruido para estudiar
META_ARMADO = re.compile(META.pattern + r"|\bOCR\b|la captura (muestra|dice|se lee)|fotograma|apunte (previo|anterior)|"
                         r"el apunte usa|en pantalla solo se ley[oó]|se lee con dudas", re.I)
EXTRA = re.compile(r"\*?\((?:extra|[Cc]omplemento[^)]{0,60}|[Ee]jemplo adicional|[Ee]jercicio adicional)\)\*?")


def _limpiar_punto(p):
    """Viñeta → sin aclaraciones sobre el proceso; None si toda ella es sobre el proceso o es material extra
    (lo que el profe NO dijo: el usuario estudia el video, no un libro)."""
    t = str(p)
    if EXTRA.search(t):
        return None
    t = re.sub(r"\s*\((?:[^()]*?)(?:\bOCR\b|lectura|no verificad|la captura)(?:[^()]*?)\)", "", t)
    t = re.sub(r"[,;:]?\s*(?:porque\s+)?en pantalla solo se ley[oó] con OCR\.?", ".", t)
    t2 = re.sub(r"\b[Ee]n (?:la|esta|una) captura,?\s*", "", t)  # "en la captura, el error…" → "el error…"
    if t2 != t:
        t = re.sub(r"(^|[:.]\s+)([a-záéíóú])", lambda m: m.group(1) + m.group(2).upper(), t2)
    return None if META_ARMADO.search(t) else t.strip()


def limpiar_titulo(t):
    """'001. @RecursosCompartidos Operadores' → '001. Operadores' (firmas de canales de Telegram en los nombres)."""
    t = re.sub(r"\s{2,}", " ", re.sub(r"(^|\s)@\w+", r"\1", str(t))).strip()
    return re.sub(r"\s*[-–]\s*copia(\s*\(\d+\))?$", "", t, flags=re.I)  # "… - copia" (copias de Windows) tampoco es parte del nombre


def _limpiar_datos(datos):
    """Aplica _limpiar_punto a las viñetas y al resumen (sobre una copia)."""
    if not datos:
        return datos
    import copy
    d = copy.deepcopy(datos)
    for s in d.get("secciones") or []:
        if isinstance(s, dict):
            s["puntos"] = [x for x in (_limpiar_punto(p) for p in s.get("puntos") or []) if x]
            s["titulo"] = limpiar_titulo(s.get("titulo") or "")  # v10: sin "@Canal" en los títulos de sección (ni en transcripcion.md)
            if s.get("porque") and not _limpiar_punto(s["porque"]):
                s["porque"] = ""
            ej = s.get("ejemplo")
            if isinstance(ej, dict) and EXTRA.search(str(ej.get("enunciado") or "")):
                s["ejemplo"] = None
            cod = str(s.get("codigo") or "")
            if re.search(r"\(extra\)|\bIlustrativo\b", cod[:300], re.I):  # código que el profe no mostró
                s["codigo"], s["linea_a_linea"] = "", []
            elif "OCR" in cod:
                s["codigo"] = re.sub(r"\s*\([^()\n]*\bOCR\b[^()\n]*\)", "", cod)
    d["resumen"] = [x for x in (_limpiar_punto(p) for p in d.get("resumen") or []) if x]
    return d


def armar(carpeta, titulo, capturas, subs, datos, duracion, recursos_md=""):
    titulo = limpiar_titulo(titulo)
    datos = _limpiar_datos(editorial.revisar_apis(datos))
    recursos_md = editorial.recursos_sin_imagenes(recursos_md)
    recursos_md = re.sub(r"\*\*📦 Proyecto completo de la sección\*\*[^\n]*\n(?:\s*\n)?(?:- [^\n]*\n?)+\s*", "", recursos_md)  # v10
    if recursos_md.strip() == "## 📎 Recursos de la clase":
        recursos_md = ""
    cues_es = subs.get("es") or subs.get("en") or []
    idioma_txt = "español" if subs.get("es") else ("inglés" if subs.get("en") else None)
    importantes, motivos = editorial.imagenes_esenciales(datos, capturas)
    esenciales = {c[0] for c in importantes}
    datos = dict(datos, _motivos_capturas=motivos) if datos else datos

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
    for nivel in range(NIVELES):  # si se pasa del presupuesto: 1-3 pliega lo menos importante; 4-9 lo RECORTA (v9/v10)
        d_n, sec_n = _recortar(datos, secciones, nivel)
        md = _armar_md(titulo, capturas, d_n, duracion, recursos_md, sec_n, importantes, esenciales,
                       voz, idioma_txt, hay_resumen, min(nivel, 3))
        if palabras_a_la_vista(md) <= presupuesto:
            break
    escribir_transcripcion(carpeta, titulo, secciones, voz, idioma_txt, duracion)
    return _tokens_en_codigo(md)


# los valores del JSON siguen siendo diario/a-veces/raro (compatibles); lo que se muestra dice IMPORTANCIA:
# en teoría (backprop, complejidad) algo es "clave" aunque no se escriba todos los días
REL = {"diario": "⭐ **Clave**", "a-veces": "🔸 **Útil**", "raro": "💤 **De paso**"}


def palabras_a_la_vista(md):
    """Palabras que se leen de corrido: sin bloques plegados ([!x]-), imágenes ni rótulos de minuto."""
    n, plegado, en_codigo = 0, False, False
    for l in md.split("\n"):
        if l.lstrip().startswith("```"):
            en_codigo = not en_codigo
        if re.match(r"\s*> \[!\w+\]-", l):
            plegado = True
            continue
        if plegado and re.match(r"\s*>", l):
            n += 0.5 * len(l.split()) * (0.5 if en_codigo else 1)  # v9: lo plegado también se lee: cuenta la mitad
            if l.lstrip("> ").startswith("```"):
                en_codigo = not en_codigo
            continue
        plegado = False
        # rótulos y navegación (minutos, enlaces, cabecera): se miran, no se leen
        if l.startswith(("![", "*⏱️", "<!--", "⏱️", "> ⏱️", "> ⚡", "> 🗣️", "---")):
            continue
        n += len(l.split()) * (0.5 if en_codigo else 1)
    return int(n)


COMENTARIO = {**dict.fromkeys(("python", "py", "bash", "sh", "shell", "zsh", "fish", "yaml", "yml", "toml", "r", "ruby",
                               "rb", "dockerfile", "makefile", "perl", "powershell", "ps1", "ini", "conf", "gitignore",
                               "dockerignore", "env", "properties", "nginx"), ("#", "")),
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
    enlaces = (["⚡ [Repaso rápido](resumen.md)"] if hay_resumen else [])
    if enlaces:
        L += ["> " + " · ".join(enlaces)]
    L += [""]
    for aviso in (datos or {}).get("_revision_api") or []:
        L += ["> [!warning] Revisar compatibilidad", "> " + aviso, ""]
    if (datos or {}).get("sin_contenido"):  # bienvenida / despedida / anuncio: apenas nada
        for s in secciones:
            L += [f"- {p}" for p in (s.get("puntos") or [])[:2]]
        return "\n".join(L + ["", f"<!-- formato v{FORMATO} -->", ""])
    L += _primero_recuerda(datos, duracion)
    objetivos = [o for o in (datos or {}).get("objetivos") or [] if _txt(o)][:3] if duracion >= 2700 else []
    if objetivos:
        L += ["## 🎯 Al terminar podrás", ""] + [f"- [ ] {_txt(o)}" for o in objetivos][:3 if nivel < 3 else 2] + [""]
    if datos and datos.get("resumen") and not hay_resumen and len(secciones) >= 2 and duracion >= 480:  # solo en clases de 8+ min (en las cortas repite las viñetas)
        L += ["## 🎯 En 30 segundos", ""] + [f"- {p}" for p in datos["resumen"][:3 if duracion < 900 else 5]] + [""]
    if len(secciones) >= 4 and duracion >= 900:  # navegación, no lectura: plegado (en clases cortas sobra)
        L += [f"> [!summary]- 🗂️ Índice ({len(secciones)} temas)"]
        L += [f"> {k + 1}. [{s['titulo']}](#{k + 1}-{ancla(s['titulo'])}) · `{hms(s['ini'])}`" for k, s in enumerate(secciones)]
        L += [""]
    L += ["---", ""]
    if recursos_md:
        L += [recursos_md, "---", ""]

    n_diag = [0]
    for k, s in enumerate(secciones):
        dur = min(s["fin"], duracion) - s["ini"]
        rel = str(s.get("relevancia") or "").strip().lower()
        L += [f"## {k + 1}. {s['titulo']}", ""]
        # (líneas de duración y "lo que dice el profe" eliminadas a petición del usuario)
        porque = _txt(s.get("porque"))
        if rel in ("diario", "raro") and len(secciones) > 1 and not (rel == "diario" and not porque):  # ⭐ y 💤 orientan; sin porqué no se rotula
            L += ["> " + " — ".join(x for x in (REL[rel], porque if rel == "diario" else "") if x), ""]
        if porque and rel != "diario" and duracion >= 180:
            L += [f"> 💡 {porque}", ""]  # v10: el porqué que el profe argumenta se ve en TODA sección, no solo en las ⭐
        plegar = (rel == "raro" and nivel >= 1 and len(secciones) > 1 and len(s.get("puntos") or []) >= 4
                  and not str(s.get("codigo") or "").strip())  # v10: lo que trae código del profe no se esconde
        cuerpo = []
        # presupuesto de la sección según lo que dura: los puntos que se pasan van plegados (no se pierden)
        tope = max(30, 20 * dur / 60) * (1.5, 1.2, 1.0, 0.8)[nivel] * (1.3 if rel == "diario" else 1.0)
        vis, mas, usadas = [], [], 0
        for p in (s.get("puntos") or []):
            n = len(_txt(p).split())
            (vis if len(s.get("puntos") or []) <= 6 or ((not vis or usadas + n <= tope) and len(vis) < 5) else mas).append(p)  # v9c: pocos puntos → todos a la vista
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
            L += ["> [!note]- 💤 Ver el detalle"] + [f"> {ln}" if ln else ">" for x in cuerpo for ln in x.split("\n")] + [""]  # v8: cada línea del código lleva el '>' (antes solo la primera → el bloque se rompía)
        else:
            L += cuerpo
        if sobran:
            L += ["> [!tip]- 🔍 Más detalle del código"] + [f"> - {x}" for x in sobran] + [""]
        if _txt(s.get("intuicion")) and duracion >= 600:  # v10: en clases cortas "La idea" repite las viñetas
            L += [f"> [!abstract] 🧠 La idea", f"> {_txt(s['intuicion'])}", ""]
        diag = _mermaid(s.get("diagrama"))
        if diag and _diagrama_vale(diag, rel, dur) and n_diag[0] < n_diagramas(duracion):
            n_diag[0] += 1
            L += ["```mermaid", diag, "```", ""]
        comp = s.get("comparativa")
        if dur >= 180 and not _repite(comp, s.get("puntos")):
            tabla = _tabla_comparativa(comp)
            if tabla and (plegar or (nivel >= 2 and rel != "diario")):
                L += ["> [!info]- ⚖️ Comparativa"] + [f"> {x}" for x in tabla] + [""]
            else:
                L += tabla
        ej = s.get("ejemplo") if duracion >= 600 else None  # v10: en clases cortas el ejemplo resuelto es andamiaje
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
                    L += [f"![⏱️ {hms(c[1])}]({c[0]})", f"*{(datos or {}).get('_motivos_capturas', {}).get(c[0], hms(c[1]))}*", ""]
            resto = [c for c in caps if c[0] not in elegidas]
            if resto:
                L += [f"> [!example]- 📸 Más capturas de esta sección ({len(resto)})"]
                for c in resto:
                    L += [f"> ![⏱️ {hms(c[1])}]({c[0]})", f"> *⏱️ {hms(c[1])}*", ">"]
                L += [""]
        L += ["---", ""]

    if datos:
        # clases cortas: se muestra solo lo que les toca (lo demás queda en el JSON), aunque se hayan hecho con más
        # v10: los topes por duración de siempre (antes un tope_l propio dejaba práctica y errores en clases de 3 min)
        tope_l = n_ejercicios(duracion)
        errores = [e for e in datos.get("errores_comunes") or [] if e][:n_errores(duracion)]
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
                    sol = editorial.solucion_markdown(sol, secciones)
                    if sol.strip():
                        rot = {True: "✅ Solución (comprobada: se ejecutó sin errores)",
                               False: "⚠️ Solución (NO pasó al ejecutarla: revísala)"}.get(e.get("verificada"), "✅ Solución")
                        P += [f"  > [!success]- {rot}"] + [f"  > {x}" for x in sol.split("\n")]
                    continue
                txt = _txt(e)
                if " — 💡 Pista:" in txt:
                    enun, pista = txt.split(" — 💡 Pista:", 1)
                    P += [f"- [ ] {enun.strip()}", "  > [!hint]- 💡 Pista", f"  > {pista.strip()}"]
                else:
                    P += [f"- [ ] {txt}"]
            L += ["## 🏋️ Para practicar", ""]
            if nivel >= 2:  # la práctica se HACE, no se lee: plegada no cuenta como lectura
                n_p = len(datos['practica'][:tope_l])
                L += [f"> [!todo]- {n_p} ejercicio{'s' if n_p != 1 else ''} con pista y solución"] + \
                     [f"> {x}" for x in P] + [""]
            else:
                L += P + [""]
            if any(str(x.get("lenguaje", "")).lower() in ("js", "javascript", "python", "py") for x in secciones):
                L += ["> Con el botón **Práctica** de SUPER+I salen ejercicios con tests (JS/Python).", ""]
        if datos.get("conceptos") and duracion >= 2700:  # v10: glosario solo en clases de 45+ min (en las cortas repite)
            conc = [c for c in datos["conceptos"] if isinstance(c, dict)][:12]
            # material de consulta: plegado (no se lee de corrido, se abre cuando hace falta)
            L += ["## 🧠 Glosario", "", f"> [!abstract]- {len(conc)} términos de la clase", "> | Concepto | Qué es |", "> |---|---|"]
            L += [f"> | **{_celda(c.get('termino', ''))}** | {_celda(c.get('definicion', ''))} |" for c in conc]
            L += [""]
        voc = [v for v in datos.get("vocabulario") or [] if isinstance(v, dict) and _txt(v.get("en"))]
        voc = voc[:n_vocabulario(duracion)]
        if voc:
            L += ["## 🇬🇧 Vocabulario", "", f"> [!abstract]- {len(voc)} términos en inglés (con pronunciación)",
                  "> | English | Suena | Español |", "> |---|---|---|"]
            L += [f"> | **{_celda(v.get('en'))}** | {_celda(v.get('suena'))} | {_celda(v.get('es'))} |" for v in voc]
            L += [""]
    else:
        L += ["> [!info] Apuntes sin resumen de IA (solo capturas y transcripción)", ""]
    L += [f"<!-- formato v{FORMATO} -->", ""]
    return _etiquetas_cortas("\n".join(L))


def _etiquetas_cortas(md):
    """"(complemento; no verificado externamente)" / "(ejemplo adicional)" → "*(extra)*" (la marca larga era ruido)."""
    md = re.sub(r"\((?:[Cc]omplemento|[Aa]mpliación)[^)]{0,40}no verificad[oa][^)]{0,30}\)", "*(extra)*", md)
    return re.sub(r"\((?:[Ee]jemplo|[Ee]jercicio) adicional\)", "*(extra)*", md)


def _diagrama_vale(diag, rel, dur):
    """Un diagrama se muestra si explica algo: sección ⭐ o de 3+ min, y al menos 4 nodos con una decisión
    o 4 flechas (una cadena de 3 cajas es una lista dibujada)."""
    flechas = len(re.findall(r"-->|-\.->|==>|--\s*\"", diag))
    decision = bool(re.search(r"\{[^}]+\}", diag)) or diag.lstrip().startswith(("sequenceDiagram", "classDiagram", "erDiagram", "stateDiagram"))
    return (rel == "diario" or dur >= 180) and (flechas >= 4 or (decision and flechas >= 3))


def _primero_recuerda(datos, duracion):
    """Antes de leer: 2-3 preguntas para responder SIN mirar (respuesta plegada). Recordar fija más que releer."""
    if not datos or duracion < 300:
        return []
    corto = datos.get("corto") if isinstance(datos.get("corto"), dict) else {}
    qs = [q for q in corto.get("preguntas") or [] if isinstance(q, dict) and _txt(q.get("pregunta"))]
    qs = sorted(qs, key=lambda q: q.get("tipo") == "definicion")[:3 if duracion >= 600 else 2]
    if not qs:
        return []
    L = ["> [!question] 🧠 Antes de leer: respóndete sin mirar"]
    for q in qs:
        L += [f"> - {_txt(q['pregunta'])}"]
        if str(q.get("codigo") or "").strip():
            L += [f">   ```{q.get('lenguaje') or ''}"] + [f">   {x}" for x in str(q["codigo"]).strip().split("\n")] + [">   ```"]
        L += [f">   > [!success]- Respuesta", f">   > {_txt(q.get('respuesta'))}"]
    return L + [""]


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
    return t.strip().replace(" ", "-")  # v10: cada espacio es un guion (como GitHub/Obsidian); antes "a := b" → "a-b" y no "a--b"


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


def _ocr_guardado(carpeta, max_pantallas=25, max_chars=1200):
    """[(segundo, texto)] de .ocr-capturas.json + .minutos.tsv: la pantalla de la clase sin necesidad de las imágenes
    (mismo criterio que regenerar-curso.leer_ocr: sin OCR ilegible, repartido por toda la clase)."""
    try:
        datos = json.load(open(os.path.join(carpeta, ".ocr-capturas.json"), encoding="utf-8"))
    except (OSError, ValueError):
        return []
    tiempos = {}
    try:
        for linea in open(os.path.join(carpeta, ".minutos.tsv"), encoding="utf-8").read().splitlines():
            f, sep, t = linea.partition("\t")
            if sep:
                try:
                    tiempos[os.path.basename(f)] = a_segundos(t)
                except ValueError:
                    pass
    except OSError:
        pass
    pantallas = []
    for nombre, texto in datos.items():
        texto = " ".join(str(texto or "").split())
        alfa = sum(c.isalnum() for c in texto)
        if alfa < 40 or alfa / max(1, len(texto)) < 0.45:
            continue
        pantallas.append((tiempos.get(os.path.basename(nombre), 0), texto[:max_chars]))
    pantallas.sort()
    if len(pantallas) > max_pantallas:
        paso = len(pantallas) / max_pantallas
        pantallas = [pantallas[int(i * paso)] for i in range(max_pantallas)]
    return pantallas


def main():
    if len(sys.argv) >= 3 and sys.argv[1] == "--indice":
        carpeta = os.path.abspath(sys.argv[2])
        indice(carpeta, os.path.basename(os.path.dirname(carpeta)) if os.path.basename(carpeta) in ("Apuntes", "capturas")
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
    if not capturas and not editorial.duracion_guardada(carpeta):
        print("No hay capturas con minuto del video en la carpeta")
        return 1
    # v10: tras ordenar-curso.py las capturas sueltas ya no están (viven en capturas-clave/): se sigue con la voz
    print(f"   {sum(c[2] for c in capturas)} importantes de {len(capturas)}") if capturas else None

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
    duracion = max(([capturas[-1][1]] if capturas else []) + [editorial.duracion_guardada(carpeta)] + [c[1] for v in subs.values() for c in v[-1:]])
    editorial.registrar_fuentes(carpeta, a.video, duracion)

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
        if not pantallas and not capturas:  # v10: sin capturas sueltas (ya limpiadas), el OCR que se guardó al procesar la clase
            pantallas = _ocr_guardado(carpeta)
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
            if isinstance(corto, dict):
                # v10: las preguntas de la IA (de ahí salen las tarjetas) se guardan SIEMPRE; antes solo desde 20 min y en las cortas
                # las tarjetas caían al relleno "¿Qué explicó el profe sobre…?"
                with open(os.path.join(carpeta, ".resumen-ia.json"), "w", encoding="utf-8") as f:
                    json.dump(corto, f, ensure_ascii=False, indent=1)
                if corto.get("esencial") and duracion >= 1200:  # v9: solo desde 20 min hay resumen.md aparte
                    rc = cargar_resumen_corto()
                    with open(os.path.join(carpeta, "resumen.md"), "w", encoding="utf-8") as f:
                        f.write(rc.armar(titulo, hms(duracion), corto, con_preguntas=False))
                    print("⚡ Resumen corto armado en la misma llamada")
        else:
            print("   (sin resumen de IA: se arma solo con capturas y transcripción)")

    if not datos and not a.sin_ia and os.path.exists(os.path.join(carpeta, ".apuntes-ia.json")) and os.path.exists(salida):
        # v10: la IA no respondió y esta clase YA tiene apuntes buenos: no se pisan con una versión sin IA (se pierde lo bueno);
        # queda marcada (.rehacer) para el próximo intento y el curso no la cuenta como hecha
        print("   ⚠️ la IA no respondió: se conservan los apuntes que ya tenía (reintenta cuando haya cuota)", file=sys.stderr)
        return 3
    reportar(97, "apuntes", "armando el cuadernillo")
    with open(salida, "w", encoding="utf-8") as f:
        f.write(armar(carpeta, titulo, capturas, subs, datos, duracion, recursos_md))
    if os.path.exists(rehacer) and (datos or a.sin_ia):
        os.remove(rehacer)  # sin IA por un fallo: queda marcada para el próximo intento
    print(f"📓 Listo: {salida}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
