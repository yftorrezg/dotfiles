#!/usr/bin/env python3
"""Transcribe videos con Whisper local en la GPU (whisper-cli, Vulkan) cuando no traen subtítulos.

Uso: transcribir.py <video> [más videos…]      transcribir.py --lista <archivo con un video por línea>

Deja <video sin extensión>.<idioma>.srt al lado del video (idioma detectado: es, en…), que es donde
cuadernillo.py los busca. Si la carpeta del video no se puede escribir, devuelve el .srt en una
carpeta temporal y quien llama lo copia. Un solo Whisper a la vez en la GPU (candado): curso-a-apuntes
lanza uno "adelantado" que transcribe las clases siguientes mientras la CPU hace las capturas y la IA
de la actual; si cuadernillo llega a una clase que se está transcribiendo, espera al candado.
GTX 980: ~6,5x más rápido que el video (9 min en 83 s), modelo large-v3-turbo.
"""
import fcntl
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile

MODELO = os.path.expanduser("~/.local/share/doblar/whisper/ggml-large-v3-turbo-q8_0.bin")
VAD = os.path.expanduser("~/.local/share/doblar/whisper/ggml-silero-v5.1.2.bin")
CANDADO = os.path.join(os.environ.get("XDG_RUNTIME_DIR", "/tmp"), "whisper-gpu.lock")
SUFIJO = re.compile(r"[._ -](es|spa|español|spanish|en|eng|english)([._-][a-z]+)?$", re.I)


def disponible():
    return bool(shutil.which("whisper-cli")) and os.path.isfile(MODELO) and os.environ.get("SIN_WHISPER") != "1"


def base_de(video):
    return re.sub(r"\.(es|en)$", "", os.path.splitext(video)[0])


def subtitulos_al_lado(video):
    """{"es"|"en": ruta} de los subtítulos que ya están junto al video, con los nombres que se ven en los
    cursos: clase.es.srt (Whisper, YouTube), clase-es.srt / clase_es.vtt (Udemy), clase.srt (sin idioma)."""
    base = base_de(video)
    res = {}
    for r in sorted(glob.glob(glob.escape(base) + "*"), key=len):
        ext = os.path.splitext(r)[1]
        resto = r[len(base):-len(ext)] if ext else r[len(base):]
        if ext.lower() not in (".srt", ".vtt") or not os.path.isfile(r):
            continue
        if not resto:
            res.setdefault("sin", r)
            continue
        m = SUFIJO.search(resto)
        if m and m.start() == 0:  # "clase-es.srt", no "clase 2-es.srt" (otra clase que empieza igual)
            res.setdefault("en" if m.group(1).lower() in ("en", "eng", "english") else "es", r)
    if "sin" in res:  # sin idioma en el nombre: se toma como español si no hay otro
        res.setdefault("es", res.pop("sin"))
    return res


def transcribir(video, hilos=4):
    """Ruta del .srt nuevo (o el que ya estaba), o None si falló (sin audio, sin Whisper)."""
    ya = subtitulos_al_lado(video)
    if ya:
        return next(iter(ya.values()))
    if not disponible() or not os.path.isfile(video):
        return None
    with open(CANDADO, "w") as c:
        fcntl.flock(c, fcntl.LOCK_EX)  # la GPU de a uno; si otro está con ESTE video, al soltar ya está
        ya = subtitulos_al_lado(video)
        if ya:
            return next(iter(ya.values()))
        with tempfile.TemporaryDirectory() as tmp:
            wav = os.path.join(tmp, "a.wav")
            if subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", video, "-vn", "-ac", "1",
                               "-ar", "16000", wav]).returncode or not os.path.exists(wav):
                return None
            cmd = ["whisper-cli", "-m", MODELO, "-f", wav, "-l", "auto", "-osrt", "-of", os.path.join(tmp, "a"),
                   "-t", str(hilos)]
            if os.path.isfile(VAD):
                cmd += ["--vad", "-vm", VAD]
            r = subprocess.run(["nice", "-n", "10"] + cmd, capture_output=True, text=True, stdin=subprocess.DEVNULL)
            srt = os.path.join(tmp, "a.srt")
            if r.returncode or not os.path.exists(srt) or not os.path.getsize(srt):
                return None
            # sin -np: con ese flag Whisper no informa el idioma detectado (y un curso en inglés quedaba como "es")
            m = re.search(r"auto-detected language:\s*([a-z]{2,3})", r.stderr + r.stdout)
            idioma = m.group(1) if m else "es"
            destino = f"{base_de(video)}.{idioma}.srt"
            try:
                shutil.copyfile(srt, destino + ".tmp")
                os.replace(destino + ".tmp", destino)
            except OSError:  # carpeta del video de solo lectura
                destino = os.path.join(tempfile.mkdtemp(), f"subtitulos.{idioma}.srt")
                shutil.copyfile(srt, destino)
            return destino


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    if args[0] == "--lista":
        args = [l.strip() for l in open(args[1], encoding="utf-8") if l.strip()]
    for k, v in enumerate(args, 1):
        if subtitulos_al_lado(v):
            continue
        r = transcribir(v)
        print(f"[{k}/{len(args)}] {'✓' if r else '✗'} {os.path.basename(v)}", flush=True)


if __name__ == "__main__":
    main()
