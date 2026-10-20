#!/usr/bin/env python3
"""cursor-llamas.py — genera los cursores de llamas (Llama-Oscura y Llama-Brasa) a partir de Bibata-Modern-Classic.

Recolorea todos los cursores: cuerpo casi negro, borde con degradado de fuego y un brillo exterior.
`left_ptr` y las manos (pointer/hand2) se animan: las llamas "reptan" por el borde.
Salida: ~/.local/share/icons/<tema>/cursors. Uso: cursor-llamas.py  (tarda ~30 s)
"""
import math
import shutil
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

BASE = Path.home() / ".local/share/icons/Bibata-Modern-Classic"
SALIDA = Path.home() / ".local/share/icons"
ANIMADOS = {"left_ptr", "default", "arrow", "hand2", "pointer", "hand1", "center_ptr"}
FASES = 10

TEMAS = {
    # nombre: (cuerpo, rampa de fuego de punta a base, color del brillo)
    "Llama-Oscura": ((14, 6, 24), [(233, 213, 255), (168, 85, 247), (220, 38, 38), (76, 5, 25)], (150, 40, 220)),
    "Llama-Brasa": ((20, 8, 6), [(255, 244, 176), (255, 176, 32), (255, 90, 31), (185, 28, 28)], (255, 110, 20)),
}


def rampa(colores, t):
    t = np.clip(t, 0, 0.9999) * (len(colores) - 1)
    i = t.astype(int)
    f = (t - i)[..., None]
    c = np.array(colores, float)
    return c[i] * (1 - f) + c[np.minimum(i + 1, len(colores) - 1)] * f


def pintar(img, tema, fase):
    """img RGBA (premultiplicado ya deshecho por PIL) -> cursor de fuego; fase 0..1 anima las llamas."""
    cuerpo, fuego, brillo = TEMAS[tema]
    a = np.asarray(img.convert("RGBA"), float) / 255
    h, w = a.shape[:2]
    lum = a[..., :3].mean(axis=2)
    borde = np.clip((lum - 0.35) / 0.4, 0, 1)[..., None]          # 1 = borde claro, 0 = cuerpo oscuro
    y = np.linspace(0, 1, h)[:, None] * np.ones((1, w))
    x = np.ones((h, 1)) * np.linspace(0, 1, w)[None, :]
    onda = 0.5 + 0.5 * np.sin((y * 5 + x * 3) * math.pi - fase * 2 * math.pi)
    t = np.clip(y * 0.75 + 0.25 * onda - 0.12 * math.sin(fase * 2 * math.pi), 0, 1)
    color = rampa(fuego, t) / 255
    cuerpo_c = np.array(cuerpo, float) / 255
    rgb = cuerpo_c * (1 - borde) + color * borde
    rgb = np.clip(rgb * (1 + 0.12 * math.sin(fase * 2 * math.pi)), 0, 1)
    out = np.dstack([rgb, a[..., 3]])
    base = Image.fromarray((out * 255).astype("uint8"), "RGBA")
    # brillo exterior (más fuerte cuando la llama "late")
    radio = max(1.0, w / 22)
    alfa = base.getchannel("A").filter(ImageFilter.GaussianBlur(radio))
    fuerza = 0.75 + 0.25 * math.sin(fase * 2 * math.pi + 1)
    g = np.asarray(alfa, float) / 255 * fuerza * 1.4
    m = max(2, w // 10)                                             # el brillo se apaga hacia el borde (si no, se ve el recuadro)
    d = np.minimum(np.minimum(np.arange(h)[:, None], h - 1 - np.arange(h)[:, None]),
                   np.minimum(np.arange(w)[None, :], w - 1 - np.arange(w)[None, :]))
    g = g * np.clip(d / m, 0, 1)
    glow = np.dstack([np.ones((h, w)) * brillo[0], np.ones((h, w)) * brillo[1], np.ones((h, w)) * brillo[2], np.clip(g, 0, 0.85) * 255])
    capa = Image.fromarray(glow.astype("uint8"), "RGBA")
    capa.alpha_composite(base)
    return capa


def escribir_xcursor(ruta, cuadros):
    """cuadros: [(tam_nominal, xhot, yhot, retardo_ms, Image RGBA)] -> archivo Xcursor."""
    trozos = []
    for tam, xh, yh, ms, im in cuadros:
        px = np.asarray(im.convert("RGBA"), float)
        al = px[..., 3:4] / 255
        pre = np.dstack([px[..., :3] * al, px[..., 3:4]]).round().astype("uint8")
        argb = (pre[..., 3].astype("uint32") << 24) | (pre[..., 0].astype("uint32") << 16) | \
               (pre[..., 1].astype("uint32") << 8) | pre[..., 2].astype("uint32")
        cab = struct.pack("<IIIIIIIII", 36, 0xFFFD0002, tam, 1, im.width, im.height, xh, yh, ms)
        trozos.append((tam, cab + argb.astype("<u4").tobytes()))
    n = len(trozos)
    pos = 16 + 12 * n
    toc, cuerpo = b"", b""
    for tam, datos in trozos:
        toc += struct.pack("<III", 0xFFFD0002, tam, pos + len(cuerpo))
        cuerpo += datos
    Path(ruta).write_bytes(b"Xcur" + struct.pack("<III", 16, 0x10000, n) + toc + cuerpo)


def extraer(archivo, carpeta):
    subprocess.run(["xcur2png", "-d", str(carpeta), "-c", str(carpeta / "c.conf"), str(archivo)],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    cuadros = []
    for lin in (carpeta / "c.conf").read_text().splitlines():
        if lin.startswith("#") or not lin.strip():
            continue
        tam, xh, yh, png, ms = lin.split()
        cuadros.append((int(tam), int(xh), int(yh), int(ms), Image.open(carpeta / png).convert("RGBA")))
    return cuadros


def generar(tema):
    destino = SALIDA / tema
    if destino.exists():
        shutil.rmtree(destino)
    (destino / "cursors").mkdir(parents=True)
    (destino / "index.theme").write_text(f"[Icon Theme]\nName={tema}\nComment=Cursor de llamas (generado por cursor-llamas.py)\nInherits=Bibata-Modern-Classic\n")
    for f in sorted((BASE / "cursors").iterdir()):
        dest = destino / "cursors" / f.name
        if f.is_symlink():
            dest.symlink_to(f.readlink())
            continue
        with tempfile.TemporaryDirectory() as tmp:
            cuadros = extraer(f, Path(tmp))
            tamanos = sorted({c[0] for c in cuadros})
            animado_origen = len(cuadros) > len(tamanos)           # ya tiene varios cuadros (espera/progreso)
            if f.name in ANIMADOS and not animado_origen:
                nuevos = [(t, xh, yh, 70, pintar(im, tema, k / FASES))
                          for k in range(FASES) for (t, xh, yh, _, im) in cuadros]
                # xcursor agrupa por tamaño: cada tamaño con sus FASES cuadros seguidos
                nuevos.sort(key=lambda c: c[0])
                # el orden por fase dentro de cada tamaño se conserva (sort estable)
            else:
                nuevos = [(t, xh, yh, ms, pintar(im, tema, 0.15)) for (t, xh, yh, ms, im) in cuadros]
            escribir_xcursor(dest, nuevos)
    print("listo", destino)


if __name__ == "__main__":
    for t in (sys.argv[1:] or TEMAS):
        generar(t)
