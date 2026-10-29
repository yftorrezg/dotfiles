#!/usr/bin/env python3
"""Pinta las carpetas de los cursos según el avance de sus apuntes (Dolphin las muestra de color).

  verde    terminado: tiene capturas/INDICE.md y apuntes.md en (casi) todas las clases
  naranja  procesándose ahora o a medias (tiene apuntes pero faltan clases)
  azul     en la cola, esperando su turno
  rojo     todavía sin procesar (ni en la cola)

Escribe `Icon=folder-<color>` en el `.directory` de la carpeta del curso (conserva lo demás que tenga) y
una marca X-Apuntes-Estado para reconocer lo suyo. Si el curso ya tenía un color puesto a mano, lo
guarda en ~/.local/state/estado-carpetas/originales.json antes de cambiarlo.
Uso: estado-carpetas.py [--ver] [--quitar]    (--ver: solo muestra; --quitar: deja todo como estaba)
Lo corre estado-carpetas.timer cada 3 min; es barato (solo `find` y comparar).
"""
import json
import os
import re
import sys
import time
from pathlib import Path

HOME = Path.home()
CACHE = HOME / ".cache/auto-captura"
ESTADO = HOME / ".local/state/estado-carpetas/originales.json"
RAICES = [Path("/run/media/yafer/SuperYafer"), HOME / "Vídeos/Descargas"]
LISTAS = [CACHE / "trabajo/a-encolar.tsv"]
VIDEO_EXT = {".mp4", ".mkv", ".webm", ".mov", ".ts"}
COLOR = {"verde": "folder-green", "naranja": "folder-orange", "azul": "folder-blue", "rojo": "folder-red"}
MARCA = "X-Apuntes-Estado"
ARCHIVO_VIDEOS = HOME / ".local/state/estado-carpetas/videos.json"
CACHE_VIDEOS = {}  # curso -> (cuándo, cantidad de videos)


def rutas_de_colas():
    """(en_marcha, en_cola): rutas de curso de todas las colas (principal + cola-N)."""
    marcha, cola = set(), set()
    dirs = [CACHE] + sorted(CACHE.glob("cola-*"))
    for d in dirs:
        for nombre, destino in (("actual.txt", marcha), ("cola.txt", cola)):
            try:
                for linea in (d / nombre).read_text().splitlines():
                    campos = linea.split("\t")
                    if len(campos) >= 4 and campos[1] == "curso":
                        destino.add(os.path.realpath(campos[3]))
            except OSError:
                pass
        # actual.txt de un trabajador muerto no cuenta (sin trabajador.lock tomado)
    return marcha, cola


def trabajador_vivo(d):
    import fcntl
    try:
        with open(d / "trabajador.lock", "w") as f:
            try:
                fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
                return False
            except OSError:
                return True
    except OSError:
        return False


def en_marcha_real():
    marcha = set()
    for d in [CACHE] + sorted(CACHE.glob("cola-*")):
        if not trabajador_vivo(d):
            continue
        try:
            for linea in (d / "actual.txt").read_text().splitlines():
                c = linea.split("\t")
                if len(c) >= 4 and c[1] == "curso":
                    marcha.add(os.path.realpath(c[3]))
        except OSError:
            pass
    return marcha


def cursos_conocidos():
    """Carpetas de curso: las que ya tienen capturas/, las de la lista de pendientes y las de las colas."""
    cursos = set()
    for raiz in RAICES:
        if not raiz.is_dir():
            continue
        for raiz_dir, dirs, _ in os.walk(raiz):
            prof = len(Path(raiz_dir).relative_to(raiz).parts)
            if "capturas" in dirs and prof >= 1:
                cursos.add(os.path.realpath(raiz_dir))
            # capturas/ de un curso nunca tiene otro curso adentro; y no hace falta bajar más de 3 niveles
            dirs[:] = [x for x in dirs if x != "capturas" and prof < 3 and not x.startswith(".")
                       and x not in ("$RECYCLE.BIN", "System Volume Information")]
    for lista in LISTAS:
        try:
            for linea in lista.read_text().splitlines():
                c = linea.split("\t")
                if len(c) >= 3 and os.path.isdir(c[2]):
                    cursos.add(os.path.realpath(c[2]))
        except OSError:
            pass
    marcha, cola = rutas_de_colas()
    cursos |= {r for r in marcha | cola if os.path.isdir(r)}
    # una subcarpeta de un curso (ej. "Clase Maestra de CSS" dentro de Academia_X) ya es parte de él
    return {c for c in cursos if not any(c.startswith(o + os.sep) for o in cursos)}


def videos_del_curso(curso):
    """Misma regla que curso-a-apuntes.sh: un video por clase (el .es/.en gana), sin entrar a capturas/
    ni node_modules/; un .ts solo cuenta si pesa >5 MB (si no es TypeScript). Se cachea 12 h: recorrer
    el NTFS entero cada pocos minutos es lo que tarda."""
    c = CACHE_VIDEOS.get(curso)
    if c and time.time() - c[0] < 12 * 3600:
        return c[1]
    vistos = set()
    for raiz, dirs, archivos in os.walk(curso):
        dirs[:] = [d for d in dirs if d not in ("capturas", "node_modules")]
        for a in archivos:
            ext = Path(a).suffix.lower()
            if ext not in VIDEO_EXT or a.endswith(".part") or ".temp." in a:
                continue
            if ext == ".ts":
                try:
                    if a.lower().endswith(".d.ts") or os.path.getsize(os.path.join(raiz, a)) < 5_000_000:
                        continue
                except OSError:
                    continue
            vistos.add(re.sub(r"\.(es|en)$", "", str(Path(raiz, a).with_suffix(""))))
    CACHE_VIDEOS[curso] = (time.time(), len(vistos))
    return len(vistos)


def clases_con_apuntes(curso):
    cap = Path(curso) / "capturas"
    if not cap.is_dir():
        return 0, False
    n = 0
    try:
        for d in cap.iterdir():
            if (d / "apuntes.md").is_file():
                n += 1
    except OSError:
        pass
    return n, (cap / "INDICE.md").is_file()


def estado_de(curso, marcha, cola):
    total = videos_del_curso(curso)
    hechas, indice = clases_con_apuntes(curso)
    if curso in marcha:
        return "naranja", hechas, total
    if total and hechas >= max(total - 2, int(total * 0.97)) and indice:
        return "verde", hechas, total
    if curso in cola:
        return "azul", hechas, total
    if hechas:
        return "naranja", hechas, total  # a medias y parado
    return "rojo", hechas, total


def leer_directory(p):
    try:
        return p.read_text().splitlines()
    except OSError:
        return []


def escribir_icono(carpeta, color, originales):
    """Pone Icon y la marca en [Desktop Entry] sin tocar las demás líneas. True si cambió algo."""
    p = Path(carpeta) / ".directory"
    lineas = leer_directory(p)
    icono_previo = next((l.split("=", 1)[1] for l in lineas if l.startswith("Icon=")), None)
    nuestra = any(l.startswith(MARCA + "=") for l in lineas)
    if icono_previo and not nuestra and carpeta not in originales:
        originales[carpeta] = icono_previo  # color puesto a mano: se recuerda
    # sin las líneas viejas de Icon/marca (también duplicadas), y puestas una sola vez bajo la cabecera
    resto = [l for l in lineas if not l.startswith(("Icon=", MARCA + "="))]
    if "[Desktop Entry]" not in resto:
        resto.insert(0, "[Desktop Entry]")
    i = resto.index("[Desktop Entry]") + 1
    nuevo = resto[:i] + [f"Icon={COLOR[color]}", f"{MARCA}={color}"] + resto[i:]
    if nuevo == leer_directory(p):
        return False
    tmp = p.with_name(".directory.tmp")
    tmp.write_text("\n".join(nuevo) + "\n")
    os.replace(tmp, p)
    return True


def quitar(carpeta, originales):
    p = Path(carpeta) / ".directory"
    lineas = leer_directory(p)
    if not any(l.startswith(MARCA + "=") for l in lineas):
        return
    resto = [l for l in lineas if not l.startswith((MARCA + "=", "Icon="))]
    if carpeta in originales:
        resto.insert(1, f"Icon={originales[carpeta]}")
    if [l for l in resto if l.strip() and l != "[Desktop Entry]"]:
        p.write_text("\n".join(resto) + "\n")
    else:
        p.unlink()


def main():
    ver, quitar_todo = "--ver" in sys.argv, "--quitar" in sys.argv
    try:
        originales = json.loads(ESTADO.read_text())
    except (OSError, ValueError):
        originales = {}
    try:
        CACHE_VIDEOS.update({k: tuple(v) for k, v in json.loads(ARCHIVO_VIDEOS.read_text()).items()})
    except (OSError, ValueError):
        pass
    cursos = sorted(cursos_conocidos())
    if quitar_todo:
        for c in cursos:
            quitar(c, originales)
        print(f"{len(cursos)} carpetas restauradas")
        return
    marcha = en_marcha_real()
    _, cola = rutas_de_colas()
    cuenta, cambios = {}, 0
    for c in cursos:
        est, hechas, total = estado_de(c, marcha, cola)
        cuenta[est] = cuenta.get(est, 0) + 1
        if ver:
            print(f"{est:8} {hechas:4}/{total:<4} {c}")
        else:
            try:
                cambios += escribir_icono(c, est, originales)
            except OSError as e:
                print(f"no pude escribir en {c}: {e}", file=sys.stderr)
    ARCHIVO_VIDEOS.parent.mkdir(parents=True, exist_ok=True)
    ARCHIVO_VIDEOS.write_text(json.dumps(CACHE_VIDEOS))
    if not ver and originales:
        ESTADO.parent.mkdir(parents=True, exist_ok=True)
        ESTADO.write_text(json.dumps(originales, ensure_ascii=False, indent=1))
    print(" · ".join(f"{k} {v}" for k, v in sorted(cuenta.items())), f"| cambiadas: {cambios}")


if __name__ == "__main__":
    main()
