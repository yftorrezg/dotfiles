#!/usr/bin/env python3
"""Capturas CLAVE de un curso: solo el estado final de cada cosa que se mostró.

Uso: capturas_clave.py <curso o su carpeta capturas/> [más cursos…]

Cuando el profe escribe un bloque de código hay 10-20 capturas seguidas que muestran el bloque a
medio escribir; la última ya lo tiene completo. Una captura se descarta si una de las 2 siguientes
la "contiene":
  - texto (OCR): casi todas sus palabras siguen en la siguiente (el profe siguió escribiendo), y
    además la pantalla se parece (mismo escenario: el resultado en el navegador NO lo "contiene"
    el código aunque tenga las mismas palabras), o
  - píxeles: es prácticamente igual a la siguiente (se movió el cursor, parpadeó algo).
La webcam del profe se detecta sola (zona que cambia aunque el resto esté quieto) y no cuenta.

Tres niveles, cada uno más chico que el anterior (20/10/2026: el usuario sentía demasiadas capturas):
  amplia      regla v3 de antes (solo quita las repetidas casi idénticas)  -> .clave-amplia.txt
  clave       regla v4 más estricta (mira 4 capturas adelante, cobertura 80 %; en videos de cámara compara
              con la última que quedó), siempre dentro de amplia              -> .clave.txt
  esenciales  la mitad de las clave (ESENCIALES_PCT): las que más texto nuevo traen + la última -> .esenciales.txt
Por clase también: .ocr-capturas.json  texto leído de cada captura (caché: no se vuelve a leer)
Por curso: todas-las-capturas/ (amplia, la arma todas-las-capturas.py), capturas-clave/ y
capturas-esenciales/ con los mismos nombres (enlaces duros, 0 espacio extra) + RESUMEN.md.
Lo que borres de un nivel no vuelve a agregarse, y desaparece de los niveles más chicos.
Uso extra: capturas_clave.py --esenciales <curso> = lo mismo (recalcula lo que falte).
Variables: OCR_HILOS (tesseract a la vez).
"""
import collections
import fcntl
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

import numpy as np
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
EXT = (".webp", ".png", ".jpg", ".jpeg")
SALIDA = "capturas-clave"
SALIDA_ESENCIALES = "capturas-esenciales"
MANIFIESTO = ".ya-agregadas.txt"
CACHE_OCR = ".ocr-capturas.json"
CLAVE = ".clave.txt"
VERSION = "v4"
ESENCIALES = ".esenciales.txt"
VERSION_ESENCIALES = "e1"

# Umbrales (probados en "Universidad Desarrollo Web": 16.073 → 5.799 capturas sin perder estados)
COBERTURA = 0.90       # tanto de sus palabras que debe seguir en la siguiente para darla por superada
COBERTURA_BAJA = 0.78  # ...o este tanto si además la pantalla casi no cambió (PIX_POCO)
PIX_IGUAL = 0.004      # fracción de píxeles distintos por debajo de la cual son la misma pantalla
PIX_POCO = 0.06
PIX_ESCENA = 0.30      # más de esto distinto = otro escenario (editor vs navegador): no se compara texto
MUCHAS_PALABRAS = 20   # desde acá la regla estricta (nivel clave) puede perder 1 de cada 5 palabras
MEDIANA_CAMARA = 12    # mediana de palabras por captura por debajo de la cual la clase es de cámara (OCR = ruido)
PIX_CAMARA = 0.03      # nivel "clave": hasta este cambio de píxeles sigue siendo la misma escena de cámara
POCAS_PALABRAS = 8     # con menos palabras (diagrama, cámara) solo vale la comparación de píxeles
# Niveles de capturas por clase: amplia (la regla v3 de antes) ⊇ clave (más estricta) ⊇ esenciales (la mitad)
NIVELES = {
    "amplia": dict(archivo=".clave-amplia.txt", version="v3", adelante=2, cob=COBERTURA, cob_baja=COBERTURA_BAJA,
                   camara=False, pix_camara=PIX_IGUAL, pix_cambio=0),
    "clave": dict(archivo=CLAVE, version=VERSION, adelante=4, cob=0.80, cob_baja=0.68,
                  camara=True, pix_camara=0.06, pix_cambio=0.25),
}
TOK = re.compile(r"[a-záéíóúñü0-9_#.\-]{3,}|\d+")  # palabras de 3+ letras y cualquier número (x = 1 → x = 2)


def natural(s):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", s)]


def imagenes(carpeta):
    return sorted((f for f in os.listdir(carpeta) if f.lower().endswith(EXT)), key=natural)


# ----------------------------------------------------------------------- OCR ---
def _idioma_ocr():
    if not shutil.which("tesseract"):
        return None
    langs = subprocess.run(["tesseract", "--list-langs"], capture_output=True, text=True).stdout.split()
    return "spa" if "spa" in langs else ("eng" if "eng" in langs else None)


def _ocr(ruta, lang):
    with tempfile.NamedTemporaryFile(suffix=".png") as tmp:
        Image.open(ruta).convert("L").save(tmp.name)
        r = subprocess.run(["tesseract", tmp.name, "-", "-l", lang, "--psm", "11"], capture_output=True,
                           text=True, env=dict(os.environ, OMP_THREAD_LIMIT="1"))
    return r.stdout


def _guardar_json(ruta, datos):
    with open(ruta + ".tmp", "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False)
    os.replace(ruta + ".tmp", ruta)


def textos(carpeta, nombres=None, avisar=None):
    """{captura: texto OCR} de la clase, leyendo solo lo que no está en la caché. None si no hay tesseract."""
    nombres = nombres if nombres is not None else imagenes(carpeta)
    ruta = os.path.join(carpeta, CACHE_OCR)
    try:
        cache = json.load(open(ruta, encoding="utf-8"))
    except (OSError, ValueError):
        cache = {}
    faltan = [f for f in nombres if f not in cache]
    if faltan:
        lang = _idioma_ocr()
        if not lang:
            return None
        hilos = int(os.environ.get("OCR_HILOS", "0")) or max(1, min(8, (os.cpu_count() or 4) - 2))
        with ThreadPoolExecutor(max_workers=hilos) as ex:
            for k, (f, t) in enumerate(zip(faltan, ex.map(lambda f: _ocr(os.path.join(carpeta, f), lang), faltan))):
                cache[f] = t
                if avisar and k % 20 == 0:
                    avisar(k, len(faltan))
                if k % 200 == 199:  # si se corta a la mitad, no se pierde lo leído
                    _guardar_json(ruta, cache)
        _guardar_json(ruta, cache)
    return {f: cache.get(f, "") for f in nombres}


def palabras(texto):
    return collections.Counter(TOK.findall(texto.lower()))


def cobertura(a, b):
    """Qué parte de las palabras de `a` sigue en `b` (0..1)."""
    n = sum(a.values())
    return sum(min(c, b[w]) for w, c in a.items()) / n if n else 1.0


# ------------------------------------------------------------------ píxeles ---
def _chica(ruta):
    return np.asarray(Image.open(ruta).convert("L").resize((240, 135)), dtype=np.int16)


def _distintos(a, b):
    return np.abs(a - b) > 40


def mascara_webcam(chicas):
    """Píxeles de la webcam: bloques que cambian en la mayoría de los pares de capturas "quietas"
    (donde casi nada más cambió). En un curso de diapositivas cambia todo y no hay webcam."""
    suma, quietos = None, 0
    for a, b in zip(chicas, chicas[1:]):
        d = _distintos(a, b)
        bloques = d.reshape(9, 15, 16, 15).mean(axis=(1, 3)) > 0.02
        if bloques.mean() < 0.15:
            suma = bloques.astype(float) if suma is None else suma + bloques
            quietos += 1
    vacia = np.zeros((135, 240), dtype=bool)
    if quietos < 5:
        return vacia
    web = suma / quietos > 0.5
    if not web.any() or web.mean() > 0.3:
        return vacia
    grande = web.copy()  # un bloque de margen alrededor
    grande[1:] |= web[:-1]; grande[:-1] |= web[1:]; grande[:, 1:] |= grande[:, :-1].copy(); grande[:, :-1] |= grande[:, 1:].copy()
    return np.kron(grande, np.ones((15, 15), dtype=bool)).astype(bool)


# ------------------------------------------------------------------ elegir ---
def _migrar_amplia(carpeta):
    """Las .clave.txt de antes (v3) pasan a ser .clave-amplia.txt: es la regla de antes, no se recalcula."""
    amplia = os.path.join(carpeta, NIVELES["amplia"]["archivo"])
    viejo = os.path.join(carpeta, CLAVE)
    if os.path.exists(amplia) or not os.path.exists(viejo):
        return
    with open(viejo, encoding="utf-8") as f:
        primera = f.readline()
    if primera.startswith("# v3 "):
        shutil.copyfile(viejo, amplia)


def _decidir(nombres, T, P, p):
    """Lista de capturas que quedan con los parámetros `p` de un nivel (ver NIVELES)."""
    def pix(i, j):
        return float(_distintos(P[i], P[j]).mean())

    clave = []
    if p["camara"] and len(nombres) > 3 and float(np.median([sum(t.values()) for t in T])) < MEDIANA_CAMARA:
        # video de cámara (celular, taller): el OCR solo lee ruido. Se compara con la última que quedó:
        # entra si la escena cambió de verdad, no por cada movimiento de la mano.
        ultima = 0
        clave = [nombres[0]]
        for i in range(1, len(nombres) - 1):
            if pix(ultima, i) >= p["pix_cambio"]:
                clave.append(nombres[i])
                ultima = i
        clave.append(nombres[-1])
        return clave
    for i, f in enumerate(nombres):
        if i == len(nombres) - 1:
            clave.append(f)
            continue
        n = sum(T[i].values())
        siguientes = [j for j in range(i + 1, i + 1 + p["adelante"]) if j < len(nombres)]
        if n < POCAS_PALABRAS:
            # cámara, diagrama o poco texto: casi igual en píxeles y sin perder ni una palabra.
            # (Achicada, una línea de código distinta cambia muy pocos píxeles: por eso el texto manda.)
            if p["camara"]:
                # misma escena aunque la persona se mueva un poco: poco cambio en las siguientes
                superada = any(pix(i, j) < p["pix_camara"] and (n == 0 or cobertura(T[i], T[j]) >= 1.0)
                               for j in siguientes)
            else:
                superada = pix(i, i + 1) < PIX_IGUAL and (n == 0 or cobertura(T[i], T[i + 1]) >= 1.0)
        else:
            superada = False
            for j in siguientes:
                pj, c = pix(i, j), cobertura(T[i], T[j])
                # con poco texto una palabra es mucho (un valor que cambió, 240 -> 348, es otro estado):
                # la regla estricta solo vale desde MUCHAS_PALABRAS
                cob, baja = (p["cob"], p["cob_baja"]) if n >= MUCHAS_PALABRAS else (COBERTURA, COBERTURA_BAJA)
                if pj < PIX_ESCENA and (c >= cob or (c >= baja and pj < PIX_POCO)):
                    superada = True
                    break
        if not superada:
            clave.append(f)
    return clave


def elegir(carpeta, avisar=None, forzar=False, nivel="clave"):
    """Lista ordenada de las capturas de un nivel de una clase ("amplia" o "clave"; se guarda en su
    archivo). None si no se puede (sin tesseract): quien llama decide qué hacer."""
    nombres = imagenes(carpeta)
    if not nombres:
        return []
    p = NIVELES[nivel]
    _migrar_amplia(carpeta)  # antes de que la v4 pise la .clave.txt vieja
    ruta = os.path.join(carpeta, p["archivo"])
    if not forzar and os.path.exists(ruta):
        lineas = open(ruta, encoding="utf-8").read().splitlines()
        if lineas and lineas[0] == f"# {p['version']} {len(nombres)}":
            return lineas[1:]
    tx = textos(carpeta, nombres, avisar)
    if tx is None:
        return None
    T = [palabras(tx[f]) for f in nombres]
    # decodificar las capturas es lo lento (WebP de 1080p): varias a la vez (Pillow suelta el GIL)
    with ThreadPoolExecutor(max_workers=max(1, min(8, (os.cpu_count() or 4) - 1))) as ex:
        P = list(ex.map(lambda f: _chica(os.path.join(carpeta, f)), nombres))
    web = mascara_webcam(P)
    for q in P:
        q[web] = 0
    clave = _decidir(nombres, T, P, p)
    if nivel == "clave":
        amplia = set(elegir(carpeta, avisar, nivel="amplia") or nombres)  # clave ⊆ amplia: lo que sobra en una no vuelve en otra
        clave = [f for f in clave if f in amplia]
    with open(ruta + ".tmp", "w", encoding="utf-8") as h:
        h.write("\n".join([f"# {p['version']} {len(nombres)}"] + clave) + "\n")
    os.replace(ruta + ".tmp", ruta)
    return clave


def esenciales(carpeta, avisar=None, forzar=False):
    """La mitad (ESENCIALES_PCT %) de las capturas clave: las que más texto nuevo traen, más la última
    de la clase. Con poco texto (cámara, diapositivas sin letra) reparte parejo por la clase.
    Se guarda en .esenciales.txt. None si no hay OCR."""
    nombres = imagenes(carpeta)
    if not nombres:
        return []
    clave = elegir(carpeta, avisar, forzar)
    if clave is None:
        return None
    ruta = os.path.join(carpeta, ESENCIALES)
    pct = int(os.environ.get("ESENCIALES_PCT", "50"))
    cabecera = f"# {VERSION_ESENCIALES} {len(clave)} {pct}"
    if not forzar and os.path.exists(ruta):
        lineas = open(ruta, encoding="utf-8").read().splitlines()
        if lineas and lineas[0] == cabecera:
            return lineas[1:]
    tx = textos(carpeta, clave, avisar) or {}
    T = {f: palabras(tx.get(f, "")) for f in clave}
    cuota = min(len(clave), max(3, -(-len(clave) * pct // 100)))
    if len(clave) <= cuota:
        elegidas = list(clave)
    else:
        con_texto = sum(1 for f in clave if sum(T[f].values()) >= POCAS_PALABRAS)
        if con_texto < len(clave) / 2:
            # casi sin texto: parejo a lo largo de la clase, incluida la última
            elegidas = [clave[round(k * (len(clave) - 1) / (cuota - 1))] for k in range(cuota)] if cuota > 1 else [clave[-1]]
        else:
            cubierto = collections.Counter()
            elegidas = [clave[-1]]  # el estado final de la clase siempre
            cubierto |= T[clave[-1]]
            restantes = set(clave[:-1])
            while len(elegidas) < cuota and restantes:
                mejor = max(restantes, key=lambda f: (sum((T[f] - cubierto).values()), -clave.index(f)))
                elegidas.append(mejor)
                restantes.discard(mejor)
                cubierto |= T[mejor]
    orden = {f: i for i, f in enumerate(clave)}
    elegidas = sorted(set(elegidas), key=orden.get)
    with open(ruta + ".tmp", "w", encoding="utf-8") as h:
        h.write("\n".join([cabecera] + elegidas) + "\n")
    os.replace(ruta + ".tmp", ruta)
    return elegidas


# ------------------------------------------------------------------- curso ---
def _todas():
    spec = importlib.util.spec_from_file_location("todas_las_capturas", os.path.join(AQUI, "todas-las-capturas.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _armar(curso, carpeta, clases, tl, salida, padre, obtener, titulo, nota):
    """Arma <curso>/<salida>/ con las capturas que devuelve obtener(carpeta de la clase) (None = no se pudo).
    Enlaces duros con los mismos nombres que todas-las-capturas/. Lo que borres de la carpeta `padre`
    (el nivel más grande) tampoco va acá; lo que borres acá no vuelve a agregarse."""
    destino = os.path.join(curso, salida)
    os.makedirs(destino, exist_ok=True)
    candado = open(os.path.join(destino, ".candado"), "w")
    fcntl.flock(candado, fcntl.LOCK_EX)  # dos corridas sobre el mismo curso: una espera a la otra
    manif = os.path.join(destino, MANIFIESTO)
    ya = set(open(manif, encoding="utf-8").read().splitlines()) if os.path.exists(manif) else set()
    dir_padre = os.path.join(curso, padre)
    manif_padre = os.path.join(dir_padre, MANIFIESTO)
    agregadas_padre = set(open(manif_padre, encoding="utf-8").read().splitlines()) if os.path.exists(manif_padre) else set()
    borradas = 0
    ancho = max(3, len(str(len(clases))))
    nuevas, filas, total_c, total, esperados = [], [], 0, 0, set()
    for k, clase in enumerate(clases, 1):
        cdir = os.path.join(carpeta, clase)
        n = len(imagenes(cdir))
        print(f"[{k}/{len(clases)}] {clase} ({n} capturas)", flush=True)
        lista = obtener(cdir)
        if lista is None:
            sys.exit("Falta tesseract (pacman -S tesseract tesseract-data-spa)")
        mins = tl.minutos(cdir)
        cuenta = 0
        for f in lista:
            llave = f"{clase}/{f}"
            base, ext = os.path.splitext(f)
            minuto = mins.get(f) or (re.search(r"\d\d-\d\d-\d\d", base) or [None])[0]
            m = re.match(r"\d+", base)
            numero = f"{int(m.group()):04d}" if m else tl.limpio(base, 10)
            nombre = f"{k:0{ancho}d} {tl.limpio(clase)} · {numero}" + (f" · {minuto}" if minuto else "") + ext.lower()
            if llave in agregadas_padre and not os.path.exists(os.path.join(dir_padre, nombre)):
                borradas += 1  # la borraste del nivel más grande
                continue
            cuenta += 1
            esperados.add(nombre)
            if llave in ya:
                continue
            dst = os.path.join(destino, nombre)
            if not os.path.exists(dst):
                try:
                    os.link(os.path.join(cdir, f), dst)
                except OSError:
                    shutil.copy2(os.path.join(cdir, f), dst)
            nuevas.append(llave)
        filas.append(f"| {k:0{ancho}d} {clase} | {cuenta} | {n} |")
        total_c += cuenta; total += n
    if nuevas:
        with open(manif, "a", encoding="utf-8") as m:
            m.write("\n".join(nuevas) + "\n")
    quitadas = 0
    for f in os.listdir(destino):  # lo que ya no corresponde a este nivel (regla nueva, o borrado más arriba)
        ruta = os.path.join(destino, f)
        if f.lower().endswith(EXT) and f not in esperados and os.stat(ruta).st_nlink >= 2:  # nunca la única copia
            os.remove(ruta)
            quitadas += 1
    with open(os.path.join(destino, "RESUMEN.md"), "w", encoding="utf-8") as h:
        h.write(f"# {titulo} · {os.path.basename(curso)}\n\n"
                f"**{total_c} de {total}** capturas ({100 * total_c // max(1, total)} %). {nota}\n\n"
                "| Clase | En esta carpeta | Total de la clase |\n|---|---|---|\n" + "\n".join(filas) + "\n")
    print(f"{titulo.split()[0]} {destino}: {total_c} de {total} (+{len(nuevas)} nuevas en la carpeta"
          + (f", {borradas} que borraste del nivel más grande no se agregan" if borradas else "")
          + (f", -{quitadas} que ya no corresponden" if quitadas else "") + ")")
    return total_c, total


def procesar(carpeta):
    """Arma <curso>/capturas-clave/ y <curso>/capturas-esenciales/ (y calcula lo que falte de cada clase).
    todas-las-capturas/ (el nivel más grande) lo arma todas-las-capturas.py."""
    tl = _todas()
    carpeta = os.path.abspath(carpeta)
    if os.path.basename(carpeta) != "capturas" and os.path.isdir(os.path.join(carpeta, "capturas")):
        carpeta = os.path.join(carpeta, "capturas")
    curso = os.path.dirname(carpeta)
    # mismas clases y mismo orden que todas-las-capturas (así los nombres coinciden)
    clases = sorted((d for d in os.listdir(carpeta) if os.path.isfile(os.path.join(carpeta, d, "apuntes.md"))),
                    key=tl.natural)
    if not clases:
        print(f"(sin clases con apuntes en {carpeta})")
        return 0, 0

    r = _armar(curso, carpeta, clases, tl, SALIDA, tl.SALIDA, elegir, "🔑 Capturas clave",
               "Se quitaron los pasos intermedios: capturas cuyo contenido sigue en las siguientes (código a "
               "medio escribir, cursor que se movió). Todas las capturas siguen en cada clase.")
    _armar(curso, carpeta, clases, tl, SALIDA_ESENCIALES, SALIDA, esenciales, "⭐ Capturas esenciales",
           f"La mitad de las clave ({os.environ.get('ESENCIALES_PCT', '50')} %): las que más contenido nuevo "
           "traen, más el estado final de cada clase. Para repasar rápido.")
    return r


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for c in (a for a in sys.argv[1:] if not a.startswith("--")):  # --esenciales: es lo mismo (procesar arma ambos)
        procesar(c)
