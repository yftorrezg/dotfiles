#!/usr/bin/env python3
"""generar-auroras.py — crea los fondos "Aurora": degradados vivos en bucle perfecto.

Para cada escritorio de escritorios-temas.toml genera un video con manchas de color
(su color de acento + tonos vecinos) que flotan despacio, en versión oscura y clara,
horizontal (1920x1080) y vertical (1080x1920).

Por qué así: se calcula a baja resolución (los degradados no tienen detalle) y el
movimiento usa senos con frecuencias enteras, así el último cuadro empalma con el
primero (bucle sin salto). El video pesa ~1 MB y la GPU lo decodifica casi gratis.

Uso: generar-auroras.py            (solo crea los que faltan)
     generar-auroras.py --todo     (rehace todos, p. ej. tras cambiar colores)
"""
import colorsys
import os
import subprocess
import sys
import tomllib
from pathlib import Path

import numpy as np

CONFIG = Path.home() / ".config/hypr/escritorios-temas.toml"
SALIDA = Path.home() / "Imágenes/Wallpapers/Animados/Aurora"
SEG, FPS = 24, 24          # duración del bucle y cuadros por segundo
ESCALA = 6                 # se calcula a 1/6 de la resolución final


def hex_rgb(h):
    return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], float) / 255


def girar(rgb, grados, sat=1.0, luz=1.0):
    h, l, s = colorsys.rgb_to_hls(*rgb)
    r = colorsys.hls_to_rgb((h + grados / 360) % 1, min(1, l * luz), min(1, s * sat))
    return np.array(r)


def paleta(acento, modo):
    a = hex_rgb(acento)
    if modo == "oscuro":
        # Vecinos de tono (nada de complementarios: se ensucian) sobre un índigo profundo
        fondo = np.array([0.03, 0.03, 0.09])
        manchas = [girar(a, 0, 1.15, 0.75), girar(a, -30, 1.2, 0.6), girar(a, -65, 1.2, 0.5),
                   np.array([0.09, 0.07, 0.30]), girar(a, 20, 1.1, 0.4)]
    else:
        fondo = np.array([0.97, 0.96, 0.99])
        pastel = lambda c, t: c + (1 - c) * t  # noqa: E731
        manchas = [pastel(a, 0.35), pastel(girar(a, 45), 0.5), pastel(girar(a, -60), 0.45),
                   pastel(girar(a, 160), 0.6), pastel(a, 0.15)]
    return fondo, manchas


def generar(destino, acento, modo, ancho, alto, semilla):
    rng = np.random.default_rng(semilla)
    fondo, manchas = paleta(acento, modo)
    w, h = ancho // ESCALA, alto // ESCALA
    yy, xx = np.mgrid[0:h, 0:w].astype(float)
    xx /= w
    yy /= h
    aspecto = w / h
    params = [(rng.uniform(0.2, 0.8), rng.uniform(0.2, 0.8),       # centro
               rng.uniform(0.15, 0.35), rng.uniform(0.12, 0.3),     # amplitud x, y
               rng.integers(1, 3), rng.integers(1, 3),              # frecuencias enteras → bucle
               rng.uniform(0, 2 * np.pi), rng.uniform(0, 2 * np.pi),
               rng.uniform(0.28, 0.45)) for _ in manchas]           # tamaño
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}",
           "-r", str(FPS), "-i", "-", "-vf", f"scale={ancho}:{alto}:flags=bicubic,noise=alls=2:allf=t",
           "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-pix_fmt", "yuv420p",
           "-movflags", "+faststart", str(destino)]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = SEG * FPS
    for f in range(n):
        t = 2 * np.pi * f / n
        peso_total = np.full((h, w), 0.6 if modo == "oscuro" else 0.55)
        color = peso_total[..., None] * fondo
        for c, (cx, cy, ax, ay, fx, fy, px, py, r) in zip(manchas, params):
            x = cx + ax * np.sin(fx * t + px)
            y = cy + ay * np.cos(fy * t + py)
            d2 = ((xx - x) * aspecto) ** 2 + (yy - y) ** 2
            p = np.exp(-d2 / (2 * (r * (aspecto if aspecto < 1 else 1)) ** 2))
            peso_total += p
            color += p[..., None] * c
        img = color / peso_total[..., None]
        ff.stdin.write((np.clip(img, 0, 1) * 255).astype(np.uint8).tobytes())
    ff.stdin.close()
    ff.wait()


def main():
    todo = "--todo" in sys.argv
    with open(CONFIG, "rb") as f:
        cfg = tomllib.load(f)
    SALIDA.mkdir(parents=True, exist_ok=True)
    for i, e in enumerate(cfg.get("escritorio", []), 1):
        for modo in ("oscuro", "claro"):
            for orient, (an, al) in (("h", (1920, 1080)), ("v", (1080, 1920))):
                destino = SALIDA / f"{i}-{modo}-{orient}.mp4"
                if destino.exists() and not todo:
                    continue
                print("generando", destino.name, flush=True)
                generar(destino, e.get("color", "#8fa8ff"), modo, an, al, semilla=i * 10 + (orient == "v"))


if __name__ == "__main__":
    main()
