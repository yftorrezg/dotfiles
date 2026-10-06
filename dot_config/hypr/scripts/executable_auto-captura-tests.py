#!/usr/bin/env python3
"""Pruebas del detector de auto-captura con videos simulados de código.

Correr después de cualquier cambio en auto-captura.py:
    python3 ~/.config/hypr/scripts/auto-captura-tests.py
Cada prueba dice qué capturas DEBEN salir (ningún estado del código perdido) y cuántas
repetidas se toleran.
"""
import importlib.util
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

spec = importlib.util.spec_from_file_location(
    "ac", os.path.join(os.path.dirname(os.path.abspath(__file__)), "auto-captura.py"))
ac = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ac)

try:
    FUENTE = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSansMono.ttf", 18)
except OSError:
    FUENTE = ImageFont.load_default()


class Video:
    """Genera frames de un 'editor' y los pasa por el detector."""

    def __init__(self):
        self.det = ac.Detector(dict(ac.DEFAULTS))
        self.lineas = ["def f(x):"]
        self.scroll = 0
        self.webcam = False
        self.mouse = None
        self.panel = None  # texto de un panel fijo a la derecha (otra ventana)
        self.t = 0
        self.guardadas = []  # (t, texto visible en ESE frame)
        self.texto = {}      # t -> texto visible en el frame t
        self.rng = np.random.default_rng(1)

    def _frame(self):
        im = Image.new("RGB", (1920, 1080), (30, 30, 30))
        d = ImageDraw.Draw(im)
        visibles = self.lineas[self.scroll:self.scroll + 38]  # como un editor real: la última queda cortada
        for i, l in enumerate(visibles):
            d.text((100, 100 + i * 26), l, fill=(220, 220, 220), font=FUENTE)
        if self.t % 2 == 0 and visibles:  # cursor de texto parpadeando
            i = len(visibles) - 1
            w = d.textlength(visibles[-1], font=FUENTE)
            d.line([(102 + w, 100 + i * 26), (102 + w, 120 + i * 26)], fill="white", width=2)
        if self.panel:
            for i, l in enumerate(self.panel):
                d.text((1450, 150 + i * 26), l, fill=(200, 200, 120), font=FUENTE)
        if self.mouse:
            x, y = self.mouse
            d.polygon([(x, y), (x, y + 22), (x + 6, y + 17), (x + 14, y + 17)], fill="white", outline="black")
        a = np.asarray(im).astype(np.int16)
        if self.webcam:  # cara moviéndose abajo a la derecha
            a[780:1060, 1500:1900] = self.rng.integers(60, 200, (280, 400, 1))
        a += self.rng.integers(-12, 13, (1080, 1920, 1))  # ruido de compresión
        return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

    def pasar(self, segundos=1):
        for _ in range(segundos):
            self.texto[self.t] = list(self.lineas[self.scroll:self.scroll + 36]) + list(self.panel or [])
            for _img, t in self.det.alimentar(self._frame(), self.t):
                self.guardadas.append((t, self.texto[t]))
            self.t += 1

    def tipear(self, linea, cps=3):
        self.lineas.append("")
        for k in range(0, len(linea) + 1, cps):
            self.lineas[-1] = linea[:k]
            self.pasar()
        self.lineas[-1] = linea

    def fin(self):
        for _img, t in self.det.cerrar():
            self.guardadas.append((t, self.texto[t]))

    def alguna_con(self, texto):
        return any(texto in l for _, ls in self.guardadas for l in ls)


def prueba(nombre, video, deben, max_capturas):
    video.fin()
    faltan = [d for d in deben if not video.alguna_con(d)]
    ok = not faltan and len(video.guardadas) <= max_capturas
    print(f"{'OK ' if ok else 'MAL'} {nombre}: {len(video.guardadas)} capturas "
          f"(máx {max_capturas}), repetidas descartadas {video.det.repetidas}"
          + (f", FALTAN: {faltan}" if faltan else ""))
    return ok


def main():
    res = []

    v = Video()  # tipear líneas con pausas
    v.pasar(3)
    v.tipear("    y = x * 2")
    v.pasar(4)
    v.tipear("    return y")
    v.pasar(4)
    res.append(prueba("tipear 2 líneas", v, ["y = x * 2", "return y"], 4))

    v = Video()  # cambiar 1 carácter y después hacer scroll enseguida
    v.lineas += [f"    a{n} = {n}" for n in range(10)]
    v.pasar(4)
    v.lineas[3] = "    a2 = 9"
    v.pasar(1)
    v.scroll = 8
    v.pasar(4)
    res.append(prueba("1 carácter antes de scroll", v, ["a2 = 9"], 3))

    v = Video()  # webcam moviéndose todo el tiempo mientras explica
    v.webcam = True
    v.lineas += [f"    b{n} = {n}" for n in range(5)]
    v.pasar(60)
    v.tipear("    c = b1 + b2")
    v.pasar(30)
    res.append(prueba("webcam + tipear", v, ["c = b1 + b2"], 4))

    v = Video()  # scroll de ida y vuelta varias veces, y después un cambio chico arriba
    v.lineas += [f"    d{n} = x * {n}" for n in range(60)]
    v.pasar(4)
    for _ in range(4):
        v.scroll = 30
        v.pasar(4)
        v.scroll = 0
        v.pasar(4)
    v.lineas[5] = "    d4 = x * 5"
    v.pasar(4)
    res.append(prueba("ida y vuelta + 1 carácter", v, ["d4 = x * 5", "d40 = x * 40"], 4))

    v = Video()  # mouse del profe moviéndose sobre el código sin cambiarlo
    v.lineas += [f"    e{n} = {n}" for n in range(8)]
    v.pasar(3)
    for k in range(30):
        v.mouse = (300 + 23 * k, 150 + 11 * (k % 9))
        v.pasar()
    v.mouse = None
    v.pasar(3)
    res.append(prueba("mouse moviéndose", v, ["e7 = 7"], 3))

    v = Video()  # tipeo largo sin pausas: no debe perder estados intermedios grandes
    for n in range(20):
        v.tipear(f"    f{n} = f{n - 1} + {n}", cps=8)
    v.pasar(3)
    res.append(prueba("tipeo largo sin pausa", v, ["f10 = f9", "f19 = f18"], 30))

    v = Video()  # vuelve a código ya visto pero con el scroll en otra altura
    v.lineas += [f"    g{n} = x ** {n} - {n * 7}" for n in range(80)]
    v.pasar(4)
    v.scroll = 36
    v.pasar(4)
    for s in (10, 23, 5, 30, 17):
        v.scroll = s
        v.pasar(4)
    res.append(prueba("volver a código visto (otra altura)", v, ["g0 = x", "g40 = x"], 2))

    v = Video()  # lo mismo, pero con 1 carácter cambiado: SÍ debe guardarse
    v.lineas += [f"    h{n} = x ** {n} - {n * 7}" for n in range(80)]
    v.pasar(4)
    v.scroll = 36
    v.pasar(4)
    v.lineas[20] = "    h19 = x ** 19 - 134"  # antes 133
    v.scroll = 12
    v.pasar(4)
    res.append(prueba("otra altura + 1 carácter", v, ["h19 = x ** 19 - 134"], 3))

    v = Video()  # scroll continuo varios segundos: no guardar los frames intermedios
    v.lineas += [f"    k{n} = {n} * x + {n}" for n in range(200)]
    v.pasar(4)
    for s in range(10, 160, 15):
        v.scroll = s
        v.pasar()
    v.pasar(4)
    # (a mitad de un scroll de más de TOPE segundos se guarda 1: puede ser código nunca visto)
    res.append(prueba("scroll continuo", v, ["k150 = 150"], 3))

    v = Video()  # panel fijo al costado que cambia una vez; después vuelve a código ya visto
    v.lineas += [f"    p{n} = x ** {n} - {n * 3}" for n in range(80)]
    v.panel = [f"derivada {k}: d/dx" for k in range(10)]
    v.pasar(4)
    v.scroll = 36
    v.pasar(4)
    v.panel = [f"otra pagina {k}" for k in range(10)]
    v.pasar(4)
    for s in (10, 23):
        v.scroll = s
        v.pasar(4)
    res.append(prueba("panel al costado + volver a código visto", v, ["p0 = x", "p40 = x", "otra pagina 3"], 3))

    print("\nTODO OK" if all(res) else "\nHAY PRUEBAS QUE FALLAN")
    return 0 if all(res) else 1


if __name__ == "__main__":
    raise SystemExit(main())
