#!/usr/bin/env python3
"""Una sola carpeta con las capturas de un curso, en orden, para estudiarlas y filtrarlas.

Desde el 20/10/2026 "todas" = las capturas AMPLIAS de cada clase (la regla clave v3 de antes: se quitan solo
las repetidas casi idénticas). Cada clase conserva todas las suyas en capturas/<clase>/. Hay tres niveles,
cada uno más chico: todas-las-capturas/ ⊇ capturas-clave/ ⊇ capturas-esenciales/. TODAS_COMPLETO=1 vuelve
a poner absolutamente todas (sin OCR).

Uso: todas-las-capturas.py [--podar] <carpeta capturas/ del curso (o el curso)> [más cursos…]
--podar saca de la carpeta las que ya no son amplias (para cursos armados cuando "todas" era todas).

Resultado: <curso>/todas-las-capturas/NNN <clase> · CCCC · hh-mm-ss.webp
  NNN   = número de la clase en el orden del INDICE.md (ordena igual que el curso)
  CCCC  = número de la captura dentro de la clase
  hh-mm-ss = minuto del video (si se sabe)

Son enlaces duros (no ocupan espacio extra; si no se puede, copia). Borrar una imagen de la carpeta
NO la borra de los apuntes. Volver a correr solo agrega capturas nuevas: lo que borraste no vuelve
(se acuerda en .ya-agregadas.txt). Borra ese archivo si quieres empezar de cero.
Al final arma también <curso>/capturas-clave/ y capturas-esenciales/ (capturas_clave.py; SIN_CLAVE=1 para no hacerlo).
"""
import os
import re
import shutil
import sys

EXT = (".webp", ".png", ".jpg", ".jpeg")
SALIDA = "todas-las-capturas"
MANIFIESTO = ".ya-agregadas.txt"


def natural(s):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", s)]


def limpio(t, tope=70):
    t = re.sub(r'[\\/:*?"<>|\n\r\t]', "-", t).strip(" .-")
    t = re.sub(r"\s{2,}", " ", t)
    return t.encode()[:tope * 2].decode(errors="ignore")[:tope].rstrip(" .-")


def minutos(clase_dir):
    m = {}
    try:
        for linea in open(os.path.join(clase_dir, ".minutos.tsv"), encoding="utf-8"):
            p = linea.rstrip("\n").split("\t")
            if len(p) == 2:
                m[p[0]] = p[1]
    except OSError:
        pass
    return m


def procesar(carpeta, podar=False):
    carpeta = os.path.abspath(carpeta)
    if os.path.basename(carpeta) != "capturas" and os.path.isdir(os.path.join(carpeta, "capturas")):
        carpeta = os.path.join(carpeta, "capturas")
    curso = os.path.dirname(carpeta)
    clases = sorted((d for d in os.listdir(carpeta) if os.path.isfile(os.path.join(carpeta, d, "apuntes.md"))),
                    key=natural)
    if not clases:
        print(f"(sin clases con apuntes en {carpeta})")
        return 0, 0
    destino = os.path.join(curso, SALIDA)
    os.makedirs(destino, exist_ok=True)
    manif_ruta = os.path.join(destino, MANIFIESTO)
    ya = set()
    if os.path.exists(manif_ruta):
        ya = {l.rstrip("\n") for l in open(manif_ruta, encoding="utf-8")}
    nuevas, esperados = [], set()
    ancho = max(3, len(str(len(clases))))
    for k, clase in enumerate(clases, 1):
        cdir = os.path.join(carpeta, clase)
        mins = minutos(cdir)
        imgs = sorted((f for f in os.listdir(cdir) if f.lower().endswith(EXT)), key=natural)
        if os.environ.get("TODAS_COMPLETO") != "1":
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            import capturas_clave
            amplia = capturas_clave.elegir(cdir, nivel="amplia")  # None si no hay tesseract: entonces todas
            if amplia is not None:
                imgs = amplia
        for f in imgs:
            clave = f"{clase}/{f}"
            base, ext = os.path.splitext(f)
            minuto = mins.get(f) or (re.search(r"\d\d-\d\d-\d\d", base) or [None])[0]
            n = re.match(r"\d+", base)
            numero = f"{int(n.group()):04d}" if n else limpio(base, 10)
            nombre = f"{k:0{ancho}d} {limpio(clase)} · {numero}" + (f" · {minuto}" if minuto else "") + ext.lower()
            esperados.add(nombre)
            if clave in ya:
                continue
            dst = os.path.join(destino, nombre)
            if os.path.exists(dst):
                continue
            src = os.path.join(cdir, f)
            try:
                os.link(src, dst)
            except OSError:
                shutil.copy2(src, dst)
            nuevas.append(clave)
    if nuevas:
        with open(manif_ruta, "a", encoding="utf-8") as m:
            m.write("\n".join(nuevas) + "\n")
    quitadas = 0
    if podar and os.environ.get("TODAS_COMPLETO") != "1":
        # lo que quedó de cuando "todas" eran absolutamente todas: sale (solo si la captura sigue en su clase,
        # o sea si el archivo tiene otro enlace duro: nunca se pierde una captura)
        for f in os.listdir(destino):
            ruta = os.path.join(destino, f)
            if f.lower().endswith(EXT) and f not in esperados and os.stat(ruta).st_nlink >= 2:
                os.remove(ruta)
                quitadas += 1
    total = sum(1 for f in os.listdir(destino) if f.lower().endswith(EXT))
    print(f"🖼️ {destino}: +{len(nuevas)} nuevas" + (f", -{quitadas} que ya no son amplias" if podar else "")
          + f", {total} en la carpeta ({len(clases)} clases)")
    return len(nuevas), total


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for c in (a for a in sys.argv[1:] if a != "--podar"):
        procesar(c, podar="--podar" in sys.argv)
        # y al lado, capturas-clave/: solo el estado final de cada cosa (ver capturas_clave.py).
        # Las clases hechas con cuadernillo ya traen su .clave.txt: esto solo arma la carpeta.
        if os.environ.get("SIN_CLAVE") != "1":
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            import capturas_clave
            capturas_clave.procesar(c)
