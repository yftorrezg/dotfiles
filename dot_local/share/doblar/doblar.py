#!/usr/bin/env python3
"""doblar: dobla videos del inglés al español manteniendo el timing.

Uso: doblar video.mp4 [otro.mp4 | carpeta/ ...]
     doblar --seguir carpeta/   (dobla cada video apenas termina de descargarse)
Variables: MODELO (small), VOZ (es-MX-JorgeNeural), FONDO (0 = sin inglés de fondo), SOLO_SUBS (1 = solo .srt),
           BORRAR_ORIGINAL (0 = por defecto, conserva el original; 1 = lo borra si el .es.mp4 salió bien),
           HILOS (hilos de CPU para Whisper/NLLB; por defecto núcleos-2 = 10 en el i7-1255U),
           ADELANTAR (1 = transcribe el siguiente video en paralelo; por defecto solo enchufada)
"""
import asyncio
import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path

import numpy as np
import soundfile as sf

MODELO = os.environ.get("MODELO", "small")
VOZ = os.environ.get("VOZ", "es-MX-JorgeNeural")
FONDO = float(os.environ.get("FONDO", "0"))  # volumen del inglés original de fondo
SOLO_SUBS = os.environ.get("SOLO_SUBS") == "1"
# Laptop: por defecto NO borra el original (si algo sale mal no se pierde el video).
BORRAR_ORIGINAL = os.environ.get("BORRAR_ORIGINAL", "0") == "1"
# i7-1255U = 12 hilos (2 P-cores con HT + 8 E-cores): deja 2 libres para el escritorio/edge-tts/ffmpeg.
HILOS = max(1, int(os.environ.get("HILOS", "0")) or max(2, (os.cpu_count() or 4) - 2))
VELOCIDAD = int(os.environ.get("VELOCIDAD", "10"))  # % extra de velocidad de la voz
SR = 24000  # frecuencia de las voces de edge-tts
MAX_TEMPO = 1.3  # aceleración máxima de la voz (más rápido suena atropellado)
MAX_ALCANCE = 1.45  # solo cuando la voz va atrasada más de 1 s, para alcanzar al video
EXTS = {".mp4", ".mkv", ".webm", ".mov", ".avi"}
NLLB = Path(__file__).resolve().parent / "nllb"
WHISPER = Path(__file__).resolve().parent / "whisper"
GPU_OK = shutil.which("whisper-cli") is not None and (WHISPER / "ggml-large-v3-turbo-q8_0.bin").exists()


def en_bateria():
    """True si hay cargadores conocidos (AC o USB-C) y ninguno está conectado."""
    fuentes = [d for d in Path("/sys/class/power_supply").glob("*")
               if (d / "type").exists() and (d / "type").read_text().strip() in ("Mains", "USB")]
    try:
        return bool(fuentes) and not any((d / "online").read_text().strip() == "1" for d in fuentes)
    except OSError:
        return False


# Transcribir el siguiente video mientras el actual se traduce = dos trabajos pesados a la vez:
# en la laptop solo si está enchufada (ADELANTAR=1/0 lo fuerza).
ADELANTAR = os.environ.get("ADELANTAR", "auto")
ADELANTAR = (not en_bateria()) if ADELANTAR == "auto" else ADELANTAR == "1"


def log(msg):
    print(f"  → {msg}", flush=True)


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, **kw)


def duracion(path):
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
               "-of", "csv=p=0", str(path)]).stdout
    return float(out.strip())


def cache_dir(video):
    st = video.stat()
    # Nombre + tamaño (no la ruta): mover la carpeta del curso no pierde el trabajo hecho.
    h = hashlib.sha1(f"{video.name}|{st.st_size}".encode()).hexdigest()[:16]
    d = Path.home() / ".cache" / "doblar" / h
    d.mkdir(parents=True, exist_ok=True)
    return d


# ---------- 1. Transcripción ----------

def transcribir(video, cache, hilos=None):
    f = cache / "transcripcion.json"
    if f.exists():
        return json.loads(f.read_text())
    wav = cache / "audio16k.wav"
    run(["ffmpeg", "-y", "-i", str(video), "-vn", "-ac", "1", "-ar", "16000", str(wav)])
    try:
        words = transcribir_gpu(video, wav, cache, hilos) if GPU_OK else transcribir_cpu(wav, hilos)
    except (subprocess.CalledProcessError, KeyError, ValueError) as e:
        log(f"La GPU falló ({type(e).__name__}); usando CPU...")
        words = transcribir_cpu(wav, hilos)
    wav.unlink(missing_ok=True)
    if words is not None:
        f.write_text(json.dumps(words))
    return words  # None = ya está en otro idioma (p. ej. español): no se dobla


def transcribir_gpu(video, wav, cache, hilos=None):
    """whisper.cpp por Vulkan (opcional en la laptop: Iris Xe con vulkan-intel; ver doc 06 §2)."""
    log(f"Transcribiendo {video.name[:50]} (GPU, large-v3-turbo)...")
    base = cache / "whisper"
    # -ml 1 -sow: una palabra por segmento; VAD corrige el inicio de las frases tras silencios.
    run(["whisper-cli", "-m", str(WHISPER / "ggml-large-v3-turbo-q8_0.bin"), "-f", str(wav),
         "-l", "auto", "-ml", "1", "-sow", "-oj", "-of", str(base), "-np", "-t", str(hilos or HILOS),
         "--vad", "-vm", str(WHISPER / "ggml-silero-v5.1.2.bin")])
    datos = json.loads(Path(str(base) + ".json").read_text(errors="replace"))
    Path(str(base) + ".json").unlink(missing_ok=True)
    if datos["result"]["language"] != "en":
        return None
    return [{"s": w["offsets"]["from"] / 1000, "e": w["offsets"]["to"] / 1000, "w": w["text"]}
            for w in datos["transcription"] if w["text"].strip()]


def transcribir_cpu(wav, hilos=None):
    from faster_whisper import WhisperModel
    hilos = hilos or HILOS
    log(f"Transcribiendo inglés (CPU, Whisper {MODELO}, {hilos} hilos)...")
    # int8 en CPU: lo más rápido en Intel 12ª gen (AVX2/VNNI) sin perder precisión apreciable.
    model = WhisperModel(MODELO, device="cpu", compute_type="int8", cpu_threads=hilos)
    # Sin forzar idioma: Whisper lo detecta en los primeros 30 s.
    segs, info = model.transcribe(str(wav), vad_filter=True,
                                  word_timestamps=True, beam_size=5)
    if info.language != "en" and info.language_probability > 0.6:
        return None
    words = []
    for s in segs:
        for w in s.words or []:
            words.append({"s": w.start, "e": w.end, "w": w.word})
        print(f"\r     {s.end/60:5.1f} / {info.duration/60:.1f} min", end="", flush=True)
    print()
    return words


_adelantados = {}


def adelantar(video):
    """Transcribe el siguiente video mientras el actual se traduce y se le pone voz
    (con la mitad de los hilos, para no pisarse con la traducción)."""
    if ADELANTAR and video and video not in _adelantados and video.exists():
        t = threading.Thread(target=lambda: _silencioso(transcribir, video, cache_dir(video), max(2, HILOS // 2)),
                             daemon=True)
        t.start()
        _adelantados[video] = t


def _silencioso(fn, *a):
    try:
        fn(*a)
    except Exception:
        pass  # si falla, se reintenta al procesar ese video


def agrupar(words):
    """Une palabras en frases completas para traducir con contexto."""
    frases, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        txt = w["w"].strip()
        nxt = words[i + 1] if i + 1 < len(words) else None
        gap = (nxt["s"] - w["e"]) if nxt else 99
        dur = w["e"] - cur[0]["s"]
        fin = txt.endswith((".", "?", "!")) and len(cur) >= 3
        coma = txt.endswith((",", ";", ":")) and dur > 6
        if fin or coma or gap > 0.8 or dur > 12 or nxt is None:
            texto = "".join(x["w"] for x in cur).strip()
            if texto:
                frases.append({"s": cur[0]["s"], "e": cur[-1]["e"], "en": texto})
            cur = []
    return frases


# ---------- 2. Traducción ----------

def traducir(frases, cache):
    f = cache / "traduccion.json"
    if f.exists():
        cached = json.loads(f.read_text())
        if len(cached) == len(frases):
            for fr, es in zip(frases, cached):
                fr["es"] = es
            return
    # NLLB-200 de Meta, local (sin internet ni límites de peticiones).
    import ctranslate2
    import sentencepiece as spm
    log(f"Traduciendo {len(frases)} frases al español (NLLB)...")
    sp = spm.SentencePieceProcessor(model_file=str(NLLB / "sentencepiece.bpe.model"))
    tr = ctranslate2.Translator(str(NLLB), device="cpu", compute_type="int8",
                                intra_threads=HILOS)
    res = []
    for i in range(0, len(frases), 32):
        lote = frases[i:i + 32]
        src = [["eng_Latn", *sp.encode(fr["en"], out_type=str), "</s>"] for fr in lote]
        out = tr.translate_batch(src, target_prefix=[["spa_Latn"]] * len(src),
                                 beam_size=4, max_decoding_length=256)
        res += [sp.decode(o.hypotheses[0][1:]) for o in out]
        print(f"\r     {len(res)}/{len(frases)} frases", end="", flush=True)
    print()
    for fr, es in zip(frases, res):
        fr["es"] = es
    f.write_text(json.dumps(res, ensure_ascii=False))


def srt(frases, key, path):
    def ts(t):
        ms = int(round(t * 1000))
        return f"{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}"
    lines = []
    for i, fr in enumerate(frases, 1):
        lines += [str(i), f"{ts(fr['s'])} --> {ts(fr['e'])}", fr[key], ""]
    path.write_text("\n".join(lines), encoding="utf-8")


# ---------- 3. Voz y sincronización ----------

async def tts_todas(frases, cache):
    import edge_tts
    sem = asyncio.Semaphore(6)

    async def una(i, texto, rate=f"+{VELOCIDAD}%"):
        mp3 = cache / f"tts_{i:05}_{rate}.mp3"
        if mp3.exists() and mp3.stat().st_size > 0:
            return mp3
        async with sem:
            for intento in range(4):
                try:
                    await edge_tts.Communicate(texto, VOZ, rate=rate).save(str(mp3))
                    return mp3
                except Exception:
                    await asyncio.sleep(2 * (intento + 1))
        return None

    return una


def cargar(mp3, tempo=1.0):
    af = ["-af", f"atempo={tempo:.4f}"] if tempo > 1.001 else []
    raw = run(["ffmpeg", "-v", "error", "-i", str(mp3), *af, "-ac", "1", "-ar", str(SR),
               "-f", "f32le", "-"]).stdout
    return np.frombuffer(raw, dtype=np.float32)


def generar_voz(frases, total, cache):
    log(f"Generando voz en español ({VOZ})...")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    una = loop.run_until_complete(tts_todas(frases, cache))
    mp3s = loop.run_until_complete(asyncio.gather(
        *(una(i, fr["es"]) for i, fr in enumerate(frases))))

    pista = np.zeros(int((total + 30) * SR), dtype=np.float32)
    cursor = 0.0
    acelerados = 0
    retrasos = []
    for i, (fr, mp3) in enumerate(zip(frases, mp3s)):
        if mp3 is None:
            continue
        sig = frases[i + 1]["s"] if i + 1 < len(frases) else total
        inicio = max(fr["s"], cursor)
        hueco = max(sig - inicio, 0.3)
        audio = cargar(mp3)
        dur = len(audio) / SR
        if dur > hueco * 1.02:
            # La voz habla más rápido (suena natural) hasta MAX_TEMPO; lo que no entre
            # se desplaza un poco y se recupera en la siguiente pausa del docente.
            # Si ya va atrasada (orador sin pausas), se permite un poco más para alcanzarlo.
            tope = MAX_TEMPO if inicio - fr["s"] < 1.0 else MAX_ALCANCE
            factor = min(dur / hueco, tope)
            pct = int(((1 + VELOCIDAD / 100) * factor - 1) * 100)
            mp3r = loop.run_until_complete(una(i, fr["es"], f"+{pct}%"))
            if mp3r:
                audio = cargar(mp3r)
            resto = len(audio) / SR / hueco
            if resto > 1.02:
                audio = cargar_tempo(audio, min(resto, 1.1))
            acelerados += 1
        retrasos.append(inicio - fr["s"])
        a = int(inicio * SR)
        if a + len(audio) > len(pista):  # la voz se pasó del final: extender la pista
            pista = np.concatenate([pista, np.zeros(a + len(audio) - len(pista), np.float32)])
        pista[a:a + len(audio)] += audio
        cursor = inicio + len(audio) / SR
        if i % 20 == 0:
            print(f"\r     {i+1}/{len(frases)} frases", end="", flush=True)
    print(f"\r     {len(frases)}/{len(frases)} frases ({acelerados} aceleradas, "
          f"desfase medio {np.mean(retrasos):.1f}s, máximo {max(retrasos):.1f}s)")
    if np.mean(retrasos) > 3:
        print("  ⚠ El orador habla demasiado rápido y el doblaje quedó desfasado.\n"
              "    Mejor verlo con audio en inglés (pista 2) + subtítulos en español.")
    loop.close()
    pista = np.clip(pista[: int(total * SR)], -1, 1)
    wav = cache / "voz_es.wav"
    sf.write(wav, pista, SR)
    return wav


def cargar_tempo(audio, tempo):
    raw = run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-",
               "-af", f"atempo={tempo:.4f}", "-f", "f32le", "-"],
              input=audio.tobytes()).stdout
    return np.frombuffer(raw, dtype=np.float32)


# ---------- 4. Unir todo ----------

def mezclar(video, voz, srt_es, srt_en, salida):
    log("Uniendo video + audio español + subtítulos...")
    mp4 = salida.suffix == ".mp4"
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(video), "-i", str(voz),
           "-i", str(srt_es), "-i", str(srt_en),
           "-filter_complex",
           f"[0:a]volume={FONDO}[bg];[1:a][bg]amix=inputs=2:duration=first:normalize=0[es]"
           if FONDO > 0 else "[1:a]anull[es]",
           "-map", "0:v", "-map", "[es]", "-map", "0:a", "-map", "2", "-map", "3",
           "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
           "-c:s", "mov_text" if mp4 else "srt",
           "-metadata:s:a:0", "language=spa", "-metadata:s:a:0", "title=Español (doblado)",
           "-metadata:s:a:1", "language=eng", "-metadata:s:a:1", "title=Inglés (original)",
           "-metadata:s:s:0", "language=spa", "-metadata:s:s:1", "language=eng",
           "-disposition:a:0", "default", "-disposition:a:1", "0",
           "-disposition:s:0", "0", "-disposition:s:1", "0",
           str(salida)]
    run(cmd)


def doblar(video, siguiente=None):
    video = Path(video)
    ext = ".mp4" if video.suffix.lower() == ".mp4" else ".mkv"
    salida = video.with_name(video.stem + ".es" + ext)
    srt_es = video.with_name(video.stem + ".es.srt")
    srt_en = video.with_name(video.stem + ".en.srt")
    if (SOLO_SUBS and srt_es.exists()) or (not SOLO_SUBS and salida.exists()):
        print(f"✔ Ya existe, salto: {video.name}")
        return
    print(f"\n🎬 {video.name}")
    cache = cache_dir(video)
    total = duracion(video)
    if video in _adelantados:
        _adelantados.pop(video).join()  # su transcripción ya se hizo (o sigue) en segundo plano
    words = transcribir(video, cache)
    adelantar(siguiente)
    if words is None:
        print("  ⏭ No está en inglés, no hace falta doblarlo.")
        return
    frases = agrupar(words)
    if not frases:
        print("  ✘ No se detectó voz en inglés.")
        return
    traducir(frases, cache)
    srt(frases, "es", srt_es)
    srt(frases, "en", srt_en)
    if SOLO_SUBS:
        print(f"✔ Subtítulos: {srt_es.name}")
        return
    voz = generar_voz(frases, total, cache)
    parcial = video.with_name(video.stem + ".es.parcial" + ext)
    mezclar(video, voz, srt_es, srt_en, parcial)
    if not verificar(parcial, total):
        print("  ✘ El video doblado salió incompleto; se conserva el original.")
        parcial.unlink(missing_ok=True)
        return
    parcial.rename(salida)
    for tmp in [voz, *cache.glob("tts_*.mp3")]:
        tmp.unlink(missing_ok=True)
    if BORRAR_ORIGINAL:
        # El doblado ya lleva el video, el audio en inglés y ambos subtítulos.
        for f in (video, srt_es, srt_en):
            f.unlink(missing_ok=True)
        print(f"✔ Listo: {salida.name} (original reemplazado)")
    else:
        print(f"✔ Listo: {salida.name}")


def verificar(path, total):
    """Comprueba que el doblado dura lo mismo que el original y tiene las 2 pistas de audio."""
    try:
        out = run(["ffprobe", "-v", "error", "-select_streams", "a",
                   "-show_entries", "stream=index", "-of", "csv=p=0", str(path)]).stdout
        return len(out.split()) == 2 and abs(duracion(path) - total) < 3
    except subprocess.CalledProcessError:
        return False


def pendientes(carpeta):
    return sorted(x for x in carpeta.rglob("*") if x.suffix.lower() in EXTS
                  and not x.stem.endswith((".es", ".es.parcial"))
                  and not re.search(r"\.(f\d+|temp)$", x.stem))


def listo(video):
    """Un video está completo si yt-dlp ya no tiene archivos a medias con su nombre."""
    if time.time() - video.stat().st_mtime < 60:
        return False
    # Subtítulos sueltos (.vtt/.srt) no indican descarga a medias.
    return not any(x != video and not x.stem.startswith(video.stem + ".es")
                   and x.suffix.lower() not in {".vtt", ".srt", ".ass"}
                   for x in video.parent.glob(glob.escape(video.stem) + ".*"))


def seguir(carpeta):
    """Dobla cada video apenas termina de descargarse, hasta que yt-dlp acaba."""
    print(f"👀 Vigilando {carpeta} (se detiene cuando termine la descarga)...")
    esperas = 0
    vistos = set()  # procesados (bien o con error): no se reintentan en esta sesión
    while True:
        descargando = subprocess.run(["pgrep", "-f", "bin/yt-dlp"],
                                     capture_output=True).returncode == 0
        cola = [v for v in pendientes(carpeta) if v not in vistos]
        preparados = [v for v in cola if listo(v)]
        for v in preparados[:1]:
            vistos.add(v)
            try:
                doblar(v, preparados[1] if len(preparados) > 1 else None)
            except Exception as e:
                detalle = e.stderr.decode()[-500:] if isinstance(e, subprocess.CalledProcessError) else repr(e)
                print(f"  ✘ Error en {v.name}: {detalle} (sigo con el siguiente)")
        if not preparados:
            if not descargando and not cola:
                print("✔ Descarga terminada y todo doblado.")
                return
            esperas = 0 if descargando else esperas + 1
            if esperas > 6:  # descarga acabada pero quedan videos a medias
                print("✘ La descarga terminó, pero estos videos quedaron incompletos:")
                for v in cola:
                    print(f"   - {v.name}")
                return
            time.sleep(30)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    if en_bateria():
        print("🔋 Estás con batería: doblar usa mucha CPU (mejor enchufada). "
              "No se adelanta el siguiente video.")
    if sys.argv[1] == "--seguir" and len(sys.argv) == 3:
        try:
            return seguir(Path(sys.argv[2]))
        except KeyboardInterrupt:
            print("\nCancelado. Si lo vuelves a lanzar, sigue donde quedó.")
            sys.exit(130)
    videos = []
    for a in sys.argv[1:]:
        p = Path(a)
        if p.is_dir():
            videos += pendientes(p)
        elif p.exists():
            videos.append(p)
        else:
            print(f"✘ No existe: {a}")
    if not videos:
        print("✔ Nada nuevo para doblar (todo ya está en español).")
    for i, v in enumerate(videos):
        try:
            doblar(v, videos[i + 1] if i + 1 < len(videos) else None)
        except KeyboardInterrupt:
            print("\nCancelado. Si lo vuelves a lanzar, sigue donde quedó.")
            sys.exit(130)
        except Exception as e:
            detalle = e.stderr.decode()[-500:] if isinstance(e, subprocess.CalledProcessError) else repr(e)
            print(f"  ✘ Error en {v.name}: {detalle} (sigo con el siguiente)")


if __name__ == "__main__":
    main()
