#!/usr/bin/env python3
"""chuletas_dibujo.py — esquemas y gráficas de las chuletas, dibujados con cairo (sin graphviz ni navegador).

Bloques ```flujo ```secuencia ```arbol ```capas ```tiempo ```grafica (sintaxis en chuletas/FORMATO.md).
  analizar(tipo, texto) → Dibujo   (ValueError si la sintaxis está mal; lo usa el validador)
  Dibujo.alto(ancho)               alto que necesita para ese ancho
  Dibujo.pintar(cr, ancho, colores)
colores = {"texto", "texto2", "fondo", "borde", "acentos": [hex, ...]}
"""
import ast
import math
import re

import cairo
import gi

gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")
from gi.repository import Pango, PangoCairo  # noqa: E402

FUENTE = "Adwaita Sans"
FLECHA = re.compile(r"\s*(<->|-->|->)\s*")
_cr_medir = cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 1, 1))


def rgb(hexa, a=1.0):
    h = hexa.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)) + (a,)


def texto(cr, cadena, tam=13.5, negrita=False, ancho=None, centrado=False):
    """Layout de Pango listo para medir (get_pixel_size) o pintar."""
    lay = PangoCairo.create_layout(cr or _cr_medir)
    fd = Pango.FontDescription.from_string(f"{FUENTE} {tam}px")
    fd.set_absolute_size(tam * Pango.SCALE)
    if negrita:
        fd.set_weight(Pango.Weight.BOLD)
    lay.set_font_description(fd)
    if ancho:
        lay.set_width(int(ancho * Pango.SCALE))
        lay.set_wrap(Pango.WrapMode.WORD_CHAR)
    if centrado:
        lay.set_alignment(Pango.Alignment.CENTER)
    lay.set_text(cadena, -1)
    return lay


def medir(cadena, tam=13.5, negrita=False, ancho=None):
    return texto(None, cadena, tam, negrita, ancho).get_pixel_size()


def poner(cr, lay, x, y, color):
    cr.set_source_rgba(*rgb(color))
    cr.move_to(x, y)
    PangoCairo.show_layout(cr, lay)


def caja(cr, x, y, w, h, r=10):
    r = min(r, h / 2, w / 2)
    cr.new_sub_path()
    cr.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    cr.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    cr.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    cr.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
    cr.close_path()


def punta(cr, x, y, ang, tam=9):
    cr.move_to(x, y)
    cr.line_to(x - tam * math.cos(ang - 0.42), y - tam * math.sin(ang - 0.42))
    cr.line_to(x - tam * math.cos(ang + 0.42), y - tam * math.sin(ang + 0.42))
    cr.close_path()
    cr.fill()


def etiqueta_flotante(cr, cad, cx, cy, col):
    lay = texto(cr, cad, 12, ancho=170, centrado=True)
    w, h = lay.get_pixel_size()
    cr.set_source_rgba(*rgb(col["fondo"], 0.92))
    caja(cr, cx - w / 2 - 6, cy - h / 2 - 2, w + 12, h + 4, 8)
    cr.fill()
    poner(cr, lay, cx - 85, cy - h / 2, col["texto2"])  # el layout mide 170 y va centrado


def lineas(cuerpo):
    return [ln.rstrip() for ln in cuerpo.splitlines() if ln.strip() and not ln.strip().startswith("//")]


def clave_valor(ln):
    if " : " in ln:
        a, b = ln.split(" : ", 1)
    elif ": " in ln:
        a, b = ln.split(": ", 1)
    else:
        return ln.strip(), ""
    return a.strip(), b.strip()


class Dibujo:
    escalable = False  # True: se dibuja a su tamaño natural y se encoge si no cabe

    def natural(self):
        return 600, 300

    def alto(self, ancho):
        if self.escalable:
            w, h = self.natural()
            return math.ceil(h * min(1.0, ancho / w)) + 8
        return math.ceil(self.alto_fluido(ancho))

    def pintar(self, cr, ancho, col):
        if self.escalable:
            w, _h = self.natural()
            e = min(1.0, ancho / w)
            cr.translate((ancho - w * e) / 2, 4)
            cr.scale(e, e)
            self.pintar_natural(cr, col)
        else:
            self.pintar_fluido(cr, ancho, col)


# --- flujo: cajas y flechas por niveles ------------------------------------------------------
class Flujo(Dibujo):
    escalable = True

    def __init__(self, cuerpo):
        self.cuerpo, self._alt = cuerpo, None
        self.nodos, self.aristas, self.dir = [], [], "derecha"
        for ln in lineas(cuerpo):
            if ln.startswith("dir:"):
                self.dir = ln[4:].strip()
                if self.dir not in ("derecha", "abajo"):
                    raise ValueError("dir debe ser «derecha» o «abajo»")
                continue
            etiqueta = ""
            if " : " in ln:
                ln, etiqueta = ln.split(" : ", 1)
            partes = FLECHA.split(ln.strip())
            nombres, flechas = partes[0::2], partes[1::2]
            if any(not n.strip() for n in nombres):
                raise ValueError(f"falta un nodo en «{ln}»")
            for nom in nombres:
                if nom.strip() not in self.nodos:
                    self.nodos.append(nom.strip())
            for i, fl in enumerate(flechas):
                self.aristas.append((nombres[i].strip(), nombres[i + 1].strip(), fl,
                                     etiqueta if i == len(flechas) - 1 else ""))
        if not self.nodos:
            raise ValueError("flujo vacío")
        self.calcular()

    def elegir(self, ancho):
        """Un flujo horizontal muy ancho se dibuja vertical si así se lee más grande (panel lateral)."""
        if self.dir != "derecha" or ancho >= self.W * 0.62:
            return self
        if self._alt is None:
            self._alt = Flujo("dir: abajo\n" + "\n".join(ln for ln in self.cuerpo.splitlines()
                                                         if not ln.strip().startswith("dir:")))
        e0, e1 = min(1.0, ancho / self.W), min(1.0, ancho / self._alt.W)
        return self._alt if e1 > e0 * 1.3 else self

    def alto(self, ancho):
        return Dibujo.alto(self.elegir(ancho), ancho)

    def pintar(self, cr, ancho, col):
        Dibujo.pintar(self.elegir(ancho), cr, ancho, col)

    def calcular(self):
        hijos = {n: [] for n in self.nodos}
        for a, b, _f, _e in self.aristas:
            hijos[a].append(b)
        # aristas hacia atrás (ciclos) no cuentan para los niveles
        atras, estado = set(), {}

        def dfs(n):
            estado[n] = 1
            for h in hijos[n]:
                if estado.get(h) == 1:
                    atras.add((n, h))
                elif h not in estado:
                    dfs(h)
            estado[n] = 2
        for n in self.nodos:
            if n not in estado:
                dfs(n)
        nivel = {n: 0 for n in self.nodos}
        for _ in self.nodos:
            for a, b, _f, _e in self.aristas:
                if (a, b) not in atras and a != b and nivel[b] < nivel[a] + 1:
                    nivel[b] = nivel[a] + 1
        self.nivel = nivel
        self.atras = atras
        self.capas = [[n for n in self.nodos if nivel[n] == k] for k in range(max(nivel.values()) + 1)]
        self.tam = {}
        for n in self.nodos:
            w, h = medir(n, 14, True, 190)
            self.tam[n] = (max(w + 28, 70), h + 18)
        # orden dentro de cada nivel por baricentro de los padres (menos cruces)
        for k in range(1, len(self.capas)):
            pos = {n: i for i, n in enumerate(self.capas[k - 1])}
            def bari(n):
                ps = [pos[a] for a, b, _f, _e in self.aristas if b == n and a in pos]
                return sum(ps) / len(ps) if ps else 1e9
            self.capas[k].sort(key=bari)
        self.posicionar()

    def posicionar(self):
        derecha = self.dir == "derecha"
        # entre niveles cabe la etiqueta más larga de sus flechas
        largo_et = max((medir(e, 12, ancho=170)[0 if derecha else 1] for _a, _b, _f, e in self.aristas if e),
                       default=0)
        hueco_niv = max(90 if derecha else 60, largo_et + (40 if derecha else 30))
        hueco = 34 if any(e for *_r, e in self.aristas) else 22
        self.xy, avance = {}, 0
        largo = []
        for capa in self.capas:
            if derecha:
                largo.append(sum(self.tam[n][1] for n in capa) + hueco * (len(capa) - 1))
            else:
                largo.append(sum(self.tam[n][0] for n in capa) + hueco * (len(capa) - 1))
        total = max(largo)
        for capa, lg in zip(self.capas, largo):
            grosor = max(self.tam[n][0] if derecha else self.tam[n][1] for n in capa)
            p = (total - lg) / 2
            for n in capa:
                w, h = self.tam[n]
                if derecha:
                    self.xy[n] = (avance + (grosor - w) / 2, p)
                    p += h + hueco
                else:
                    self.xy[n] = (p, avance + (grosor - h) / 2)
                    p += w + hueco
            avance += grosor + hueco_niv
        # lo que se dibuja fuera de las cajas (lazos, flechas de vuelta, arcos) necesita margen por su lado
        m = {"arriba": 6, "abajo": 6, "izq": 6, "der": 6}
        lado_vuelta = "arriba" if derecha else "der"
        self.lazo = {}
        for a, b, _f, e in self.aristas:
            if a == b:
                capa = self.capas[self.nivel[a]]
                primero = capa.index(a) == 0
                if derecha:
                    lado = "arriba" if primero or len(capa) == 1 else "abajo"
                    m[lado] = max(m[lado], 62)
                else:
                    lado = "izq" if primero and len(capa) > 1 else "der"
                    m[lado] = max(m[lado], 48 + (medir(e, 12, ancho=170)[0] + 16 if e else 0))
                self.lazo[a] = lado
            elif (a, b) in self.atras or self.nivel[a] == self.nivel[b]:
                i = 0 if derecha else 1
                dist = abs(self.xy[a][i] - self.xy[b][i])
                m[lado_vuelta] = max(m[lado_vuelta], 0.75 * (dist * 0.25 + 40) + 24)
        saltos = max((self.nivel[b] - self.nivel[a] for a, b, _f, _e in self.aristas
                      if (a, b) not in self.atras and self.nivel[b] - self.nivel[a] > 1), default=0)
        self.arco = 46 * min(saltos - 1, 2) + 24 if saltos > 1 else 0  # cuánto se aparta una arista que salta niveles
        if self.arco:
            m[lado_vuelta] = max(m[lado_vuelta], self.arco + 8)
        self.m = m
        self.W = (avance - hueco_niv if derecha else total) + m["izq"] + m["der"]
        self.H = (total if derecha else avance - hueco_niv) + m["arriba"] + m["abajo"]

    def natural(self):
        return self.W, self.H

    def borde(self, n, hacia):
        x, y = self.xy[n]
        w, h = self.tam[n]
        cx, cy = x + w / 2, y + h / 2
        dx, dy = hacia[0] - cx, hacia[1] - cy
        if dx == 0 and dy == 0:
            return cx, cy
        t = min(w / 2 / abs(dx) if dx else 1e9, h / 2 / abs(dy) if dy else 1e9)
        return cx + dx * t, cy + dy * t

    def pintar_natural(self, cr, col):
        cr.translate(self.m["izq"], self.m["arriba"])
        acentos = col["acentos"]
        centro = {n: (self.xy[n][0] + self.tam[n][0] / 2, self.xy[n][1] + self.tam[n][1] / 2) for n in self.nodos}
        etiquetas = []
        for a, b, fl, et in self.aristas:
            c = rgb(acentos[self.nivel[a] % len(acentos)], 0.85)
            cr.set_source_rgba(*c)
            cr.set_line_width(2)
            cr.set_dash([6, 5] if fl == "-->" else [])
            if a == b:  # a sí mismo: un lazo por el lado libre
                x, y = self.xy[a]
                w, h = self.tam[a]
                lado = self.lazo[a]
                if lado in ("arriba", "abajo"):
                    sg = -1 if lado == "arriba" else 1
                    y0 = y if sg < 0 else y + h
                    cr.move_to(x + w * 0.3, y0)
                    cr.curve_to(x + w * 0.3, y0 + sg * 42, x + w * 0.7, y0 + sg * 42, x + w * 0.7, y0)
                    cr.stroke()
                    cr.set_dash([])
                    punta(cr, x + w * 0.7, y0, -sg * math.pi / 2)
                    if et:
                        etiquetas.append((et, x + w / 2, y0 + sg * 48))
                else:
                    sg = -1 if lado == "izq" else 1
                    x0 = x if sg < 0 else x + w
                    cr.move_to(x0, y + h * 0.3)
                    cr.curve_to(x0 + sg * 42, y + h * 0.3, x0 + sg * 42, y + h * 0.7, x0, y + h * 0.7)
                    cr.stroke()
                    cr.set_dash([])
                    punta(cr, x0, y + h * 0.7, 0 if sg < 0 else math.pi)
                    if et:
                        etiquetas.append((et, x0 + sg * (52 + medir(et, 12, ancho=170)[0] / 2), y + h / 2))
                continue
            p0, p1 = self.borde(a, centro[b]), self.borde(b, centro[a])
            if (a, b) in self.atras or self.nivel[a] == self.nivel[b]:  # curva por fuera
                if self.dir == "derecha":
                    off = -(abs(p1[0] - p0[0]) * 0.25 + 40)
                    c0, c1 = (p0[0], p0[1] + off), (p1[0], p1[1] + off)
                    p0 = (centro[a][0], self.xy[a][1])
                    p1 = (centro[b][0], self.xy[b][1])
                    c0, c1 = (p0[0], p0[1] + off), (p1[0], p1[1] + off)
                else:
                    off = abs(p1[1] - p0[1]) * 0.25 + 40
                    p0 = (self.xy[a][0] + self.tam[a][0], centro[a][1])
                    p1 = (self.xy[b][0] + self.tam[b][0], centro[b][1])
                    c0, c1 = (p0[0] + off, p0[1]), (p1[0] + off, p1[1])
            elif self.dir == "derecha":
                dx = (p1[0] - p0[0]) * 0.45
                c0, c1 = (p0[0] + dx, p0[1]), (p1[0] - dx, p1[1])
                if self.nivel[b] - self.nivel[a] > 1:  # salta niveles: arco por arriba
                    c0, c1 = (c0[0], c0[1] - self.arco * 1.6), (c1[0], c1[1] - self.arco * 1.6)
            else:
                dy = (p1[1] - p0[1]) * 0.45
                c0, c1 = (p0[0], p0[1] + dy), (p1[0], p1[1] - dy)
                if self.nivel[b] - self.nivel[a] > 1:  # salta niveles: arco por la derecha
                    c0, c1 = (c0[0] + self.arco * 1.6, c0[1]), (c1[0] + self.arco * 1.6, c1[1])
            cr.move_to(*p0)
            cr.curve_to(*c0, *c1, *p1)
            cr.stroke()
            cr.set_dash([])
            ang = math.atan2(p1[1] - c1[1], p1[0] - c1[0])
            punta(cr, *p1, ang)
            if fl == "<->":
                punta(cr, *p0, math.atan2(p0[1] - c0[1], p0[0] - c0[0]))
            if et:  # punto medio de la curva de Bézier
                mx = 0.125 * p0[0] + 0.375 * c0[0] + 0.375 * c1[0] + 0.125 * p1[0]
                my = 0.125 * p0[1] + 0.375 * c0[1] + 0.375 * c1[1] + 0.125 * p1[1]
                etiquetas.append((et, mx, my))
        for n in self.nodos:
            x, y = self.xy[n]
            w, h = self.tam[n]
            acento = acentos[self.nivel[n] % len(acentos)]
            caja(cr, x, y, w, h, 12)
            cr.set_source_rgba(*rgb(col["fondo"]))
            cr.fill_preserve()
            cr.set_source_rgba(*rgb(acento, 0.18))
            cr.fill_preserve()
            cr.set_source_rgba(*rgb(acento))
            cr.set_line_width(2)
            cr.stroke()
            lay = texto(cr, n, 14, True, 190, centrado=True)
            tw, th = lay.get_pixel_size()
            poner(cr, lay, x + w / 2 - 95, y + (h - th) / 2, col["texto"])
        for et, mx, my in etiquetas:
            etiqueta_flotante(cr, et, mx, my, col)


# --- secuencia: quién le habla a quién y en qué orden ----------------------------------------
class Secuencia(Dibujo):
    escalable = True

    def __init__(self, cuerpo):
        self.actores, self.pasos = [], []
        for ln in lineas(cuerpo):
            if ln.startswith("actores:"):
                self.actores = [a.strip() for a in ln[8:].split(",") if a.strip()]
                continue
            if ln.startswith("nota "):
                quien, txt = clave_valor(ln[5:])
                if quien not in self.actores:
                    self.actores.append(quien)
                self.pasos.append(("nota", quien, None, txt))
                continue
            izq, txt = (ln.split(" : ", 1) + [""])[:2] if " : " in ln else (ln, "")
            partes = FLECHA.split(izq.strip())
            if len(partes) != 3:
                raise ValueError(f"cada línea es «A -> B : mensaje» (o -->): «{ln}»")
            a, fl, b = (p.strip() for p in partes)
            for x in (a, b):
                if x not in self.actores:
                    self.actores.append(x)
            self.pasos.append((fl, a, b, txt.strip()))
        if len(self.actores) < 1 or not self.pasos:
            raise ValueError("secuencia vacía")
        self.calcular()

    def calcular(self):
        n = len(self.actores)
        self.cab = [medir(a, 14, True, 150) for a in self.actores]
        huecos = [max(150, (self.cab[i][0] + self.cab[i + 1][0]) / 2 + 50) for i in range(n - 1)]
        idx = {a: i for i, a in enumerate(self.actores)}
        for fl, a, b, txt in self.pasos:
            if fl == "nota" or a == b:
                continue
            i, j = sorted((idx[a], idx[b]))
            necesita = medir(txt, 12.5, ancho=260)[0] + 50
            tiene = sum(huecos[i:j])
            if tiene < necesita:
                for k in range(i, j):
                    huecos[k] += (necesita - tiene) / (j - i)
        self.x = [max(80, self.cab[0][0] / 2 + 20)]
        for hq in huecos:
            self.x.append(self.x[-1] + hq)
        self.W = self.x[-1] + max(80, self.cab[-1][0] / 2 + 20) + 60
        self.alto_cab = max(h for _w, h in self.cab) + 22
        self.filas, y = [], self.alto_cab + 22
        for fl, a, b, txt in self.pasos:
            th = medir(txt, 12.5, ancho=260)[1] if txt else 0
            alto = th + (38 if a == b else 26) if fl != "nota" else th + 22
            self.filas.append(y)
            y += alto + 8
        self.H = y + 10

    def natural(self):
        return self.W, self.H

    def pintar_natural(self, cr, col):
        acentos = col["acentos"]
        idx = {a: i for i, a in enumerate(self.actores)}
        for i, a in enumerate(self.actores):  # líneas de vida
            cr.set_source_rgba(*rgb(acentos[i % len(acentos)], 0.45))
            cr.set_line_width(1.5)
            cr.set_dash([4, 5])
            cr.move_to(self.x[i], self.alto_cab)
            cr.line_to(self.x[i], self.H - 6)
            cr.stroke()
        cr.set_dash([])
        for i, a in enumerate(self.actores):
            w, h = self.cab[i]
            acento = acentos[i % len(acentos)]
            caja(cr, self.x[i] - w / 2 - 14, 2, w + 28, self.alto_cab - 4, 12)
            cr.set_source_rgba(*rgb(acento, 0.22))
            cr.fill_preserve()
            cr.set_source_rgba(*rgb(acento))
            cr.set_line_width(2)
            cr.stroke()
            lay = texto(cr, a, 14, True, 150, centrado=True)
            poner(cr, lay, self.x[i] - 75, (self.alto_cab - h) / 2, col["texto"])
        for k, ((fl, a, b, txt), y) in enumerate(zip(self.pasos, self.filas)):
            if fl == "nota":
                lay = texto(cr, txt, 12.5, ancho=240)
                w, h = lay.get_pixel_size()
                x = self.x[idx[a]] - w / 2 - 10
                caja(cr, x, y, w + 20, h + 14, 8)
                cr.set_source_rgba(*rgb(acentos[4 % len(acentos)], 0.25))
                cr.fill()
                poner(cr, lay, x + 10, y + 7, col["texto"])
                continue
            acento = acentos[idx[a] % len(acentos)]
            lay = texto(cr, f"{k + 1}. {txt}" if txt else f"{k + 1}.", 12.5, ancho=260, centrado=True)
            tw, th = lay.get_pixel_size()
            x0, x1 = self.x[idx[a]], self.x[idx[b]]
            cr.set_source_rgba(*rgb(acento))
            cr.set_line_width(2)
            cr.set_dash([6, 5] if fl == "-->" else [])
            ly = y + th + 8
            if a == b:
                cr.move_to(x0, ly)
                cr.curve_to(x0 + 60, ly, x0 + 60, ly + 22, x0 + 4, ly + 22)
                cr.stroke()
                cr.set_dash([])
                punta(cr, x0 + 2, ly + 22, math.pi)
                poner(cr, lay, x0 + 66 - (260 - tw) / 2, y + 8, col["texto"])
                continue
            cr.move_to(x0, ly)
            cr.line_to(x1, ly)
            cr.stroke()
            cr.set_dash([])
            punta(cr, x1, ly, 0 if x1 > x0 else math.pi)
            poner(cr, lay, (x0 + x1) / 2 - 130, y, col["texto"] if fl == "->" else col["texto2"])


# --- árbol: jerarquías (DOM, carpetas, herencia, árboles de datos) ----------------------------
class Arbol(Dibujo):
    escalable = True

    def __init__(self, cuerpo):
        self.raices, pila = [], []
        for ln in lineas(cuerpo):
            sangria = len(ln) - len(ln.lstrip())
            nodo = {"t": ln.strip(), "h": []}
            while pila and pila[-1][0] >= sangria:
                pila.pop()
            (pila[-1][1]["h"] if pila else self.raices).append(nodo)
            pila.append((sangria, nodo))
        if not self.raices:
            raise ValueError("árbol vacío")
        self.vertical = True
        self.calcular()

    def calcular(self):
        self.lista = []

        def medir_n(n, prof):
            n["w"], n["hh"] = medir(n["t"], 13.5, True, 170)
            n["w"] += 24
            n["hh"] += 14
            n["p"] = prof
            self.lista.append(n)
            for h in n["h"]:
                medir_n(h, prof + 1)
        for r in self.raices:
            medir_n(r, 0)
        prof_max = max(n["p"] for n in self.lista)
        alto_fila = max(n["hh"] for n in self.lista) + 46
        siguiente = [0.0]

        def colocar(n):
            if not n["h"]:
                n["x"] = siguiente[0] + n["w"] / 2
                siguiente[0] += n["w"] + 16
            else:
                for h in n["h"]:
                    colocar(h)
                n["x"] = (n["h"][0]["x"] + n["h"][-1]["x"]) / 2
                izq = n["x"] - n["w"] / 2
                if izq < 0:  # el padre más ancho que sus hijos
                    self.mover(n, -izq)
                    siguiente[0] = max(siguiente[0], n["x"] + n["w"] / 2 + 16)
            n["y"] = n["p"] * alto_fila
        for r in self.raices:
            colocar(r)
        self.W = max(n["x"] + n["w"] / 2 for n in self.lista) + 8
        self.H = (prof_max + 1) * alto_fila - 46 + max(n["hh"] for n in self.lista) + 8
        # muy ancho y profundo (carpetas): mejor como lista sangrada
        self.vertical = self.W <= 1100 or self.W <= self.H * 2.2
        if not self.vertical:
            y = 0
            for n in self.lista:
                n["lx"], n["ly"] = n["p"] * 30, y
                y += n["hh"] + 8
            self.W = max(n["lx"] + n["w"] for n in self.lista) + 8
            self.H = y

    def mover(self, n, dx):
        n["x"] += dx
        for h in n["h"]:
            self.mover(h, dx)

    def natural(self):
        return self.W, self.H

    def pintar_natural(self, cr, col):
        acentos = col["acentos"]
        cr.translate(4, 4)
        for n in self.lista:
            for h in n["h"]:
                cr.set_source_rgba(*rgb(acentos[n["p"] % len(acentos)], 0.7))
                cr.set_line_width(2)
                if self.vertical:
                    y0, y1 = n["y"] + n["hh"], h["y"]
                    cr.move_to(n["x"], y0)
                    cr.curve_to(n["x"], (y0 + y1) / 2, h["x"], (y0 + y1) / 2, h["x"], y1)
                else:
                    x0 = n["lx"] + 14
                    cr.move_to(x0, n["ly"] + n["hh"])
                    cr.line_to(x0, h["ly"] + h["hh"] / 2)
                    cr.line_to(h["lx"], h["ly"] + h["hh"] / 2)
                cr.stroke()
        for n in self.lista:
            acento = acentos[n["p"] % len(acentos)]
            x, y = (n["x"] - n["w"] / 2, n["y"]) if self.vertical else (n["lx"], n["ly"])
            caja(cr, x, y, n["w"], n["hh"], 10)
            cr.set_source_rgba(*rgb(col["fondo"]))
            cr.fill_preserve()
            cr.set_source_rgba(*rgb(acento, 0.2))
            cr.fill_preserve()
            cr.set_source_rgba(*rgb(acento))
            cr.set_line_width(1.8)
            cr.stroke()
            lay = texto(cr, n["t"], 13.5, True, 170)
            poner(cr, lay, x + 12, y + 7, col["texto"])


# --- capas: pilas y arquitecturas (OSI, frontend/backend, stack/heap) --------------------------
class Capas(Dibujo):
    def __init__(self, cuerpo):
        self.capas = [clave_valor(ln) for ln in lineas(cuerpo)]
        if not self.capas:
            raise ValueError("capas vacío")

    def medidas(self, ancho):
        col = min(260, max(medir(n, 15, True)[0] for n, _d in self.capas) + 30)
        filas = []
        for n, d in self.capas:
            hn = medir(n, 15, True, col - 24)[1]
            hd = medir(d, 13.5, ancho=max(80, ancho - col - 36))[1] if d else 0
            filas.append(max(hn, hd) + 22)
        return col, filas

    def alto_fluido(self, ancho):
        _c, filas = self.medidas(ancho)
        return sum(filas) + 6 * (len(filas) - 1) + 4

    def pintar_fluido(self, cr, ancho, col):
        cnom, filas = self.medidas(ancho)
        y = 0
        for i, ((n, d), h) in enumerate(zip(self.capas, filas)):
            acento = col["acentos"][i % len(col["acentos"])]
            caja(cr, 0, y, ancho, h, 12)
            cr.set_source_rgba(*rgb(acento, 0.16))
            cr.fill()
            caja(cr, 0, y, cnom, h, 12)
            cr.set_source_rgba(*rgb(acento, 0.85))
            cr.fill()
            lay = texto(cr, n, 15, True, cnom - 24)
            poner(cr, lay, 12, y + (h - lay.get_pixel_size()[1]) / 2, col["fondo"])
            if d:
                lay = texto(cr, d, 13.5, ancho=ancho - cnom - 36)
                poner(cr, lay, cnom + 16, y + (h - lay.get_pixel_size()[1]) / 2, col["texto"])
            y += h + 6


# --- tiempo: línea de tiempo (historia y futuro de una tecnología) ----------------------------
class Tiempo(Dibujo):
    def __init__(self, cuerpo):
        self.hitos = [clave_valor(ln) for ln in lineas(cuerpo)]
        if not self.hitos or any(not d for _f, d in self.hitos):
            raise ValueError("cada línea es «fecha : qué pasó»")

    def medidas(self, ancho):
        cf = max(medir(f, 14, True)[0] for f, _d in self.hitos) + 16
        return cf, [medir(d, 14, ancho=max(80, ancho - cf - 44))[1] + 16 for _f, d in self.hitos]

    def alto_fluido(self, ancho):
        return sum(self.medidas(ancho)[1]) + 4

    def pintar_fluido(self, cr, ancho, col):
        cf, filas = self.medidas(ancho)
        xl = cf + 14
        cr.set_source_rgba(*rgb(col["borde"], 0.7))
        cr.set_line_width(2)
        cr.move_to(xl, 10)
        cr.line_to(xl, sum(filas) - 8)
        cr.stroke()
        y = 0
        for i, ((f, d), h) in enumerate(zip(self.hitos, filas)):
            acento = col["acentos"][i % len(col["acentos"])]
            lay = texto(cr, f, 14, True)
            poner(cr, lay, cf - lay.get_pixel_size()[0] - 2, y + 4, acento)
            cr.set_source_rgba(*rgb(acento))
            cr.arc(xl, y + 13, 6, 0, 2 * math.pi)
            cr.fill()
            poner(cr, texto(cr, d, 14, ancho=ancho - cf - 44), xl + 18, y + 4, col["texto"])
            y += h


# --- gráficas: barras, líneas (crecimiento Big O…) y pastel -----------------------------------
FUNCIONES = {"log": math.log, "log2": math.log2, "log10": math.log10, "sqrt": math.sqrt, "exp": math.exp,
             "factorial": lambda v: math.gamma(v + 1), "abs": abs, "min": min, "max": max}
NODOS_OK = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Call, ast.Name, ast.Constant, ast.Load, ast.Add,
            ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.USub, ast.Mod, ast.FloorDiv)


def compilar(expr):
    arbol = ast.parse(expr.replace("^", "**"), mode="eval")
    for nodo in ast.walk(arbol):
        if not isinstance(nodo, NODOS_OK):
            raise ValueError(f"expresión no permitida: {expr}")
        if isinstance(nodo, ast.Name) and nodo.id not in FUNCIONES and nodo.id not in ("n", "x"):
            raise ValueError(f"variable desconocida «{nodo.id}» (usa n)")
    codigo = compile(arbol, "<grafica>", "eval")
    return lambda v: eval(codigo, {"__builtins__": {}}, {**FUNCIONES, "n": v, "x": v})


class Grafica(Dibujo):
    def __init__(self, cuerpo):
        self.op = {"tipo": "barras", "titulo": "", "unidad": ""}
        self.datos = []
        for ln in lineas(cuerpo):
            k, v = clave_valor(ln)
            if k in ("tipo", "titulo", "unidad", "x", "ymax", "ejex", "ejey"):
                self.op[k] = v
            else:
                self.datos.append((k, v))
        tipo = self.op["tipo"]
        if tipo not in ("barras", "lineas", "pastel"):
            raise ValueError("tipo: barras | lineas | pastel")
        if not self.datos:
            raise ValueError("gráfica sin datos")
        if tipo == "lineas":
            a, b = (self.op.get("x") or "1..10").split("..")
            self.x0, self.x1 = float(a), float(b)
            self.series = []
            for nom, expr in self.datos:
                if re.fullmatch(r"[\d.,\s-]+", expr):
                    ys = [float(v) for v in expr.split(",") if v.strip()]
                    pts = [(self.x0 + (self.x1 - self.x0) * i / max(1, len(ys) - 1), y) for i, y in enumerate(ys)]
                else:
                    f = compilar(expr)
                    pts = []
                    for i in range(121):
                        xv = self.x0 + (self.x1 - self.x0) * i / 120
                        try:
                            pts.append((xv, float(f(xv))))
                        except (ValueError, OverflowError, ZeroDivisionError):
                            pass
                self.series.append((nom, pts))
            todos = [y for _n, p in self.series for _x, y in p]
            self.ymax = float(self.op["ymax"]) if self.op.get("ymax") else max(todos)
            self.ymin = min(0.0, min(todos))
        else:
            try:
                self.valores = [(k, float(v.split()[0].replace(",", "."))) for k, v in self.datos]
            except (ValueError, IndexError):
                raise ValueError("cada línea es «Etiqueta : número»") from None

    def alto_fluido(self, ancho):
        tit = 30 if self.op["titulo"] else 0
        if self.op["tipo"] == "barras":
            return tit + len(self.valores) * 34 + 4
        if self.op["tipo"] == "pastel":
            return tit + max(230, len(self.valores) * 28 + 20)
        return tit + 300

    def pintar_fluido(self, cr, ancho, col):
        acentos = col["acentos"]
        if self.op["titulo"]:
            poner(cr, texto(cr, self.op["titulo"], 15, True), 0, 0, col["texto"])
            cr.translate(0, 30)
        tipo, u = self.op["tipo"], self.op["unidad"]
        if tipo == "barras":
            cnom = min(ancho * 0.4, max(medir(k, 13.5, True)[0] for k, _v in self.valores) + 16)
            vmax = max(v for _k, v in self.valores) or 1
            ancho_valor = max(medir(f"{v:g} {u}".strip(), 13, True)[0] for _k, v in self.valores) + 14
            for i, (k, v) in enumerate(self.valores):
                y = i * 34
                lay = texto(cr, k, 13.5, True, cnom - 10)
                poner(cr, lay, 0, y + 6, col["texto"])
                largo = (ancho - cnom - ancho_valor) * v / vmax
                caja(cr, cnom, y + 4, max(6, largo), 24, 7)
                cr.set_source_rgba(*rgb(acentos[i % len(acentos)], 0.9))
                cr.fill()
                poner(cr, texto(cr, f"{v:g} {u}".strip(), 13, True), cnom + largo + 8, y + 7, col["texto2"])
        elif tipo == "pastel":
            total = sum(v for _k, v in self.valores) or 1
            r, cx, cy = 100, 115, 115
            ang = -math.pi / 2
            for i, (k, v) in enumerate(self.valores):
                paso = 2 * math.pi * v / total
                cr.move_to(cx, cy)
                cr.arc(cx, cy, r, ang, ang + paso)
                cr.close_path()
                cr.set_source_rgba(*rgb(acentos[i % len(acentos)], 0.92))
                cr.fill()
                ang += paso
            cr.set_source_rgba(*rgb(col["fondo"]))
            cr.arc(cx, cy, r * 0.55, 0, 2 * math.pi)
            cr.fill()
            for i, (k, v) in enumerate(self.valores):
                y = 10 + i * 28
                cr.set_source_rgba(*rgb(acentos[i % len(acentos)]))
                caja(cr, 250, y + 3, 16, 16, 4)
                cr.fill()
                poner(cr, texto(cr, f"{k}  ·  {v:g}{u} ({100 * v / total:.0f} %)", 13.5, ancho=ancho - 280),
                      274, y, col["texto"])
        else:
            self.pintar_lineas(cr, ancho, col)

    def pintar_lineas(self, cr, ancho, col):
        acentos = col["acentos"]
        izq, abajo, alto = 52, 30, 300 - 30
        leyenda = 200 if ancho > 560 else 0
        ancho_g = ancho - izq - leyenda - 10
        cr.set_line_width(1)
        for k in range(5):  # rejilla y eje y
            yv = self.ymin + (self.ymax - self.ymin) * k / 4
            y = alto - abajo - (alto - abajo - 10) * k / 4
            cr.set_source_rgba(*rgb(col["borde"], 0.35))
            cr.move_to(izq, y)
            cr.line_to(izq + ancho_g, y)
            cr.stroke()
            lay = texto(cr, f"{yv:,.0f}" if abs(yv) >= 10 else f"{yv:.2g}", 11.5)
            poner(cr, lay, izq - 8 - lay.get_pixel_size()[0], y - 8, col["texto2"])
        for k in range(5):
            xv = self.x0 + (self.x1 - self.x0) * k / 4
            etq = f"{round(xv):g}" if self.x1 - self.x0 >= 8 else f"{xv:.3g}"
            poner(cr, texto(cr, etq, 11.5), izq + ancho_g * k / 4 - 6, alto - abajo + 6, col["texto2"])
        if self.op.get("ejex"):
            lay = texto(cr, self.op["ejex"], 12, True)
            poner(cr, lay, izq + ancho_g - lay.get_pixel_size()[0], alto - abajo + 6 + 16, col["texto2"])

        def punto(xv, yv):
            return (izq + ancho_g * (xv - self.x0) / (self.x1 - self.x0 or 1),
                    alto - abajo - (alto - abajo - 10) * (yv - self.ymin) / ((self.ymax - self.ymin) or 1))
        cr.save()
        cr.rectangle(izq, 4, ancho_g, alto - abajo - 4)
        cr.clip()
        for i, (_nom, pts) in enumerate(self.series):
            cr.set_source_rgba(*rgb(acentos[i % len(acentos)]))
            cr.set_line_width(3)
            for j, (xv, yv) in enumerate(pts):
                (cr.line_to if j else cr.move_to)(*punto(xv, min(yv, self.ymax * 3 + 1)))
            cr.stroke()
        cr.restore()
        for i, (nom, _p) in enumerate(self.series):
            if leyenda:
                x, y = izq + ancho_g + 18, 10 + i * 26
            else:
                x, y = izq + (i % 3) * 120, alto + 2 + (i // 3) * 22
            cr.set_source_rgba(*rgb(acentos[i % len(acentos)]))
            caja(cr, x, y + 4, 18, 8, 4)
            cr.fill()
            poner(cr, texto(cr, nom, 13, True, 170), x + 26, y - 2, col["texto"])

    def alto(self, ancho):
        h = Dibujo.alto(self, ancho)
        if self.op["tipo"] == "lineas" and ancho <= 560:
            h += 22 * ((len(self.series) + 2) // 3)
        return h


TIPOS = {"flujo": Flujo, "secuencia": Secuencia, "arbol": Arbol, "capas": Capas, "tiempo": Tiempo,
         "grafica": Grafica}


def analizar(tipo, cuerpo):
    try:
        return TIPOS[tipo](cuerpo)
    except ValueError:
        raise
    except Exception as e:  # cualquier otra cosa rara en la sintaxis
        raise ValueError(f"{type(e).__name__}: {e}") from None
