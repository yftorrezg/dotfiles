#!/usr/bin/env python3
"""Pruebas del cuadernillo (sin IA): subtítulos, elección de capturas y detección de webcam.
    python3 ~/.config/hypr/scripts/cuadernillo-tests.py      # tiene que decir: TODO OK
"""
import importlib.util
import os
import shutil
import sys
import tempfile

import numpy as np
from PIL import Image, ImageDraw

AQUI = os.path.dirname(os.path.abspath(__file__))


def cargar(nombre, archivo):
    spec = importlib.util.spec_from_file_location(nombre, os.path.join(AQUI, archivo))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


c = cargar("c", "cuadernillo.py")
t = cargar("t", "auto-captura-tests.py")
res = []


def prueba(nombre, ok, detalle=""):
    print(f"{'OK ' if ok else 'MAL'} {nombre}" + (f": {detalle}" if detalle else ""))
    res.append(ok)


# 1) Subtítulos automáticos de YouTube ("rodando": cada línea sale dos veces)
yt = ("1\n00:00:01,000 --> 00:00:03,000\nhola a todos\n\n"
      "2\n00:00:03,000 --> 00:00:05,000\nhola a todos\nhoy vamos a ver\n\n"
      "3\n00:00:05,000 --> 00:00:07,000\nhoy vamos a ver\nredes <b>neuronales</b>\n")
cues = c.leer_srt(yt)
prueba("subtítulos de YouTube sin repetir", [x[2] for x in cues] == ["hola a todos", "hoy vamos a ver", "redes neuronales"],
       str([x[2] for x in cues]))
vtt = ("WEBVTT\nKind: captions\nLanguage: es\n\n"
       "00:00:00.140 --> 00:00:02.740 align:start position:0%\n \n"
       "hola<00:00:00.500><c> a</c><00:00:00.530><c> todos</c>\n\n"
       "00:00:02.740 --> 00:00:02.750 align:start position:0%\nhola a todos\n \n\n"
       "00:00:02.750 --> 00:00:05.000 align:start position:0%\nhola a todos\nhoy<00:00:03.100><c> vemos</c><00:00:03.500><c> React</c>\n")
prueba("subtítulos .vtt de YouTube", [x[2] for x in c.leer_srt(vtt)] == ["hola a todos", "hoy vemos React"],
       str([x[2] for x in c.leer_srt(vtt)]))
prueba("tiempos de subtítulos", cues[1][0] == 3.0 and c.a_segundos("1:02:03") == 3723 and c.hms(3723) == "1:02:03")


def carpeta_de(video):
    """Guarda los frames de un Video simulado como capturas con minuto del video."""
    d = tempfile.mkdtemp()
    c.ac.Guardador(d, en_vivo=False)([(img, tt) for tt, img in video])  # 0001.webp + .minutos.tsv
    return d


# 2) Tipear línea por línea: las capturas intermedias quedan "superadas", la final no
v = t.Video()
frames = []
for n in range(6):
    v.lineas.append(f"    z{n} = x ** {n} - {n * 11}")
    frames.append((10 * n, v._frame()))
d = carpeta_de(frames)
caps = c.elegir_capturas(d)
importantes = [x[0] for x in caps if x[2]]
prueba("tipeo: solo el estado final es importante", importantes == [caps[-1][0]], str(importantes))
shutil.rmtree(d)

# 3) Diapositivas: todas distintas -> todas importantes (no confundir con una webcam).
#    Las capturas clave comparan el TEXTO (OCR): cada diapositiva tiene su propio contenido.
temas = ["variables", "funciones", "objetos", "arreglos", "promesas", "eventos", "modulos", "clases"]
frames = []
for n, tema in enumerate(temas):
    v = t.Video()
    v.lineas = [f"Diapositiva: {tema}"] + [f"  {tema} ejemplo {palabra}" for palabra in
                                           ("declarar", "recorrer", "copiar", "comparar", "borrar", "mostrar")]
    frames.append((30 * n, v._frame()))
d = carpeta_de(frames)
caps = c.elegir_capturas(d)
prueba("diapositivas: todas importantes", all(x[2] for x in caps), f"{sum(x[2] for x in caps)}/{len(caps)}")
shutil.rmtree(d)

# 3b) Un valor que cambia (ancho = 240 -> ancho = 348) es otro estado: quedan las dos.
#     Frame sin el ruido artificial de t.Video (el ruido uniforme confunde al OCR; el de un video real no)
def editor_limpio(lineas):
    im = Image.new("RGB", (1920, 1080), (30, 30, 30))
    d = ImageDraw.Draw(im)
    for i, l in enumerate(lineas):
        d.text((100, 100 + i * 26), l, fill=(220, 220, 220), font=t.FUENTE)
    return im


codigo = ["const caja = {", "    ancho: 240,", "    alto: 120,", "};"]
d = carpeta_de([(10, editor_limpio(codigo)), (20, editor_limpio([codigo[0], "    ancho: 348,"] + codigo[2:]))])
caps = c.elegir_capturas(d)
prueba("valor que cambia: quedan los dos estados", all(x[2] for x in caps), f"{sum(x[2] for x in caps)}/{len(caps)}")
shutil.rmtree(d)

# 3c) Subtítulos de Udemy (clase-es.srt) y de Whisper (clase.es.srt) al lado del video
d = tempfile.mkdtemp()
for nombre in ("001 Intro.mp4", "001 Intro-es.srt", "002 Tema.mp4", "002 Tema.en.srt", "003 Otra.mp4", "003 Otra.srt",
               "001 Intro 2.mp4"):
    open(os.path.join(d, nombre), "w").close()
r1 = c.tr.subtitulos_al_lado(os.path.join(d, "001 Intro.mp4"))
r2 = c.tr.subtitulos_al_lado(os.path.join(d, "002 Tema.mp4"))
r3 = c.tr.subtitulos_al_lado(os.path.join(d, "003 Otra.mp4"))
r4 = c.tr.subtitulos_al_lado(os.path.join(d, "001 Intro 2.mp4"))  # no es de "001 Intro"
prueba("subtítulos al lado del video (-es, .en, sin idioma)",
       list(r1) == ["es"] and list(r2) == ["en"] and list(r3) == ["es"] and r4 == {}, f"{r1} {r2} {r3} {r4}")
shutil.rmtree(d)

# 3d) main() de punta a punta con un video y recursos del curso (sin IA ni Whisper): el código del profe
#     se copia a codigo-del-curso/ (sin .git), los apuntes traen "📎 Recursos" y al rehacer sin el video siguen
import subprocess
import zipfile
base = tempfile.mkdtemp()
tema = os.path.join(base, "01 Tema")
os.makedirs(tema)
open(os.path.join(tema, "001 Margin.mp4"), "w").close()
with zipfile.ZipFile(os.path.join(tema, "001 Margin-UHTML.zip"), "w") as z:
    z.writestr("css/estilos.css", "p { margin-top: 40px; }\n")
    z.writestr(".git/config", "x")
with zipfile.ZipFile(os.path.join(tema, "001 proyecto-FIN.zip"), "w") as z:
    z.writestr("src/App.jsx", "export default function App() {}\n")
open(os.path.join(tema, "002 Otra.mp4"), "w").close()
open(os.path.join(tema, "002 Otra-UHTML.js"), "w").write("const otra = 1;\n")
open(os.path.join(tema, "external-links.txt"), "w").write("001 Margin\nhttps://developer.mozilla.org/margin\n\n"
                                                         "002 Otra\nhttps://otra.example\n")
rec = c.rec_curso.de_la_clase(os.path.join(tema, "001 Margin.mp4"))
prueba("recursos: los de la clase, el proyecto y sus enlaces (no los de otra clase)",
       [os.path.basename(x) for x in rec["clase"]] == ["001 Margin-UHTML.zip"]
       and [os.path.basename(x) for x in rec["proyecto"]] == ["001 proyecto-FIN.zip"]
       and rec["enlaces"] == [("Margin", "https://developer.mozilla.org/margin")], str(rec))
clase = carpeta_de([(10, editor_limpio(codigo))])
env = dict(os.environ, SIN_WHISPER="1")
r = subprocess.run([sys.executable, os.path.join(AQUI, "cuadernillo.py"), clase, "--video",
                    os.path.join(tema, "001 Margin.mp4"), "--sin-ia"], capture_output=True, text=True, env=env)
ap = open(os.path.join(clase, "apuntes.md"), encoding="utf-8").read() if os.path.exists(os.path.join(clase, "apuntes.md")) else ""
copiado = os.path.join(clase, "codigo-del-curso", "Margin UHTML", "css", "estilos.css")
prueba("main con video: recursos copiados y en los apuntes", r.returncode == 0 and os.path.exists(copiado)
       and not os.path.exists(os.path.join(clase, "codigo-del-curso", "Margin UHTML", ".git"))
       and "📎 Recursos de la clase" in ap, (r.stderr or r.stdout)[-300:])
r = subprocess.run([sys.executable, os.path.join(AQUI, "cuadernillo.py"), clase, "--sin-ia", "--forzar"],
                   capture_output=True, text=True, env=env)
prueba("rehacer sin el video: los recursos siguen", r.returncode == 0 and
       "📎 Recursos de la clase" in open(os.path.join(clase, "apuntes.md"), encoding="utf-8").read(), r.stderr[-300:])
shutil.rmtree(base)
shutil.rmtree(clase)

# 3e) YouTube: capítulos del autor y enlaces de la descripción salen de video.info.json (sin redes sociales)
import json
yt = tempfile.mkdtemp()
json.dump({"description": "Links:\n- micrograd en github: https://github.com/karpathy/micrograd\n"
                          "- mi twitter: https://twitter.com/x\n- sitio: https://karpathy.ai",
           "chapters": [{"start_time": 0, "title": "intro"}, {"start_time": 25.5, "title": "overview"}]},
          open(os.path.join(yt, "video.info.json"), "w"))
enl, caps = c.rec_curso.de_youtube(yt)
prueba("YouTube: capítulos y enlaces (GitHub primero, sin redes)",
       caps == [(0, "intro"), (25, "overview")] and [u for _, u in enl] == ["https://github.com/karpathy/micrograd", "https://karpathy.ai"], f"{enl} {caps}")
shutil.rmtree(yt)

# 4) Webcam: con código que casi no cambia y una cara moviéndose, se detecta la zona
det = c.ac.Detector(c.ac.leer_conf())
v = t.Video()
v.webcam = True
v.lineas += [f"    w{n} = {n}" for n in range(10)]
red = []
for n in range(10):
    v.t = n
    red.append(det._reducir(v._frame()))
w = c.detectar_webcam(det, red)
fil, col = np.nonzero(w)
prueba("webcam detectada abajo a la derecha", w.any() and fil.min() >= 20 and col.min() >= 40,
       f"{int(w.sum())} bloques")

# 5) Nombres cortos (0001.webp + .minutos.tsv) y viejos (0001_00-01-40.png): los dos se leen
d = tempfile.mkdtemp()
img = Image.new("RGB", (64, 36))
c.ac.Guardador(d, en_vivo=False)([(img, 5), (img, 3723.4), (img, 3730)])
img.save(os.path.join(d, "0010_02-00-00.png"))  # vieja, del mismo curso
lista = c.listar_capturas(d)
prueba("nombres cortos: 0001.webp, 0002.webp…", sorted(os.listdir(d))[1:4] == ["0001.webp", "0002.webp", "0003.webp"],
       str(sorted(os.listdir(d))))
prueba("minutos desde .minutos.tsv (y de nombres viejos)",
       lista == [("0001.webp", 5), ("0002.webp", 3723), ("0003.webp", 3730), ("0010_02-00-00.png", 7200)], str(lista))
shutil.rmtree(d)

# 6) Cuota de Claude agotada: espera y reintenta (no sigue sin IA); un error común no espera
d = tempfile.mkdtemp()
falso = os.path.join(d, "claude-falso.py")
with open(falso, "w") as f:
    f.write("""import json, os, sys
cont = os.path.join(os.path.dirname(__file__), "n"); n = int(open(cont).read()) if os.path.exists(cont) else 0
open(cont, "w").write(str(n + 1))
if n < 2:
    print(json.dumps({"is_error": True, "result": "You've hit your session limit · resets 11pm"}))
else:
    print(json.dumps({"is_error": False, "result": "{\\"ok\\": 1}"}))
""")
esperas = []
texto = c.llamar_claude([sys.executable, falso], "hola", esperar=esperas.append)
prueba("cuota agotada: espera 2 veces y después responde", texto == '{"ok": 1}' and len(esperas) == 2, f"{texto!r} {esperas}")
prueba("error común no se toma por cuota", not c.cuota_agotada("Error: invalid JSON") and c.cuota_agotada("You've hit your session limit · resets 11pm"))
shutil.rmtree(d)

# 7) Subtítulos para Claude: el idioma original, no la traducción automática
d = tempfile.mkdtemp()
es, en = [(0, 1, "hola")], [(0, 1, "hello")]
prueba("sin pistas del idioma: inglés (videos doblados)", c.subs_para_claude(d, {"es": es, "en": en}) == en)
open(os.path.join(d, "subtitulos.es-orig.srt"), "w").close()
prueba("curso en español: el español original, no su traducción", c.subs_para_claude(d, {"es": es, "en": en}) == es)
os.remove(os.path.join(d, "subtitulos.es-orig.srt")); open(os.path.join(d, ".idioma"), "w").write("en\n")
prueba("curso en inglés (.idioma): el inglés", c.subs_para_claude(d, {"es": es, "en": en}) == en)
shutil.rmtree(d)

print("\nTODO OK" if all(res) else "\nHAY PRUEBAS QUE FALLAN")
raise SystemExit(0 if all(res) else 1)
