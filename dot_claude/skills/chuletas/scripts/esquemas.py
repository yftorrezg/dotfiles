#!/usr/bin/env python3
"""esquemas.py — dibuja a PNG todos los esquemas (flujo, secuencia, arbol, capas, tiempo, grafica) de una o más hojas.

Uso: python3 esquemas.py <carpeta_salida> <ancho_px> hoja1.md [hoja2.md ...]
     900 px ≈ pantalla completa · 420 px ≈ panel lateral. Luego mira los PNG (Read) buscando textos encimados o cortados.
No abre ninguna ventana ni toca el escritorio.
"""
import sys, cairo
sys.path.insert(0, "/home/yafer/.config/hypr/scripts")
import chuletas_md as md, chuletas_dibujo as dib
col = {"texto": "#e6e1e5", "texto2": "#cac4d0", "fondo": "#1c1b1f", "borde": "#938f99",
       "acentos": ["#7aa2f7", "#bb9af7", "#7dcfff", "#9ece6a", "#e0af68", "#f7768e"]}
salida, ancho = sys.argv[1], int(sys.argv[2])
i = 0
for a in sys.argv[3:]:
    h = md.leer(a)
    for sec in h["secciones"]:
        for b in md.recorrer(sec["bloques"]):
            if b[0] == "codigo" and b[1] in md.DIBUJOS:
                d = dib.analizar(b[1], b[2]); alto = d.alto(ancho)
                s = cairo.ImageSurface(cairo.FORMAT_ARGB32, ancho, alto); cr = cairo.Context(s)
                cr.set_source_rgb(0.11, 0.105, 0.12); cr.paint(); d.pintar(cr, ancho, col)
                i += 1; s.write_to_png(f"{salida}/{i:02d}-{a.split('/')[-1][:5]}-{b[1]}.png")
print(i, "esquemas")
