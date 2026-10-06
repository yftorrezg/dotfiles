#!/usr/bin/env python3
"""Auto-captura de cursos: guarda una captura solo cuando la pantalla cambió de verdad.

Modo en vivo (lo lanza auto-captura-toggle.sh con SUPER+ALT+S):
    auto-captura.py --monitor eDP-1 --out <carpeta>
Modo video (lo usa video-a-capturas.sh):
    auto-captura.py --video archivo.mp4 --out <carpeta>

Idea: la pantalla se divide en bloques. Si cambia aunque sea 1 bloque (una variable, un
parámetro, un ';') hay cambio. No se guarda letra por letra: se espera a que la pantalla
quede quieta (línea terminada), con un tope por si el profe tipea sin parar. Antes de un
cambio grande (scroll, otro archivo, otra diapositiva) se guarda el último frame, que es
la versión más completa de lo que había.
"""
import argparse
import io
import json
import os
import signal
import subprocess
import sys
import time
from collections import deque

import numpy as np
from PIL import Image

CONF = os.path.expanduser("~/.config/hypr/scripts/auto-captura.conf")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from progreso import reportar  # barrita de progreso (no hace nada si no se pidió)
DEFAULTS = {
    "INTERVALO": 1.0,      # segundos entre capturas de pantalla (modo vivo)
    "ESTABLE": 2.0,        # segundos sin cambios para considerar "línea terminada"
    "TOPE": 6.0,           # si cambia sin parar, guardar igual cada TOPE segundos
    "GRANDE": 0.30,        # fracción de bloques que cuenta como cambio grande
    "RUIDO": 28,           # diferencia de gris (0-255) que se ignora (compresión del video)
    "MIN_PIXELES": 6,      # píxeles distintos para que un bloque cuente como cambiado
    "MASCARA_ABAJO": 0.0,  # fracción inferior ignorada (ej. 0.08 = barra del reproductor)
    "HISTORIAL": 30,       # no guardar si la pantalla es igual a alguna de las últimas N capturas
}
BLOQUE = 16  # px, sobre la imagen reducida a la mitad (= 32 px reales)


def leer_conf():
    conf = dict(DEFAULTS)
    try:
        with open(CONF) as f:
            for linea in f:
                linea = linea.split("#", 1)[0].strip()
                if "=" in linea:
                    k, v = (s.strip() for s in linea.split("=", 1))
                    if k in conf:
                        conf[k] = type(DEFAULTS[k])(float(v))
    except FileNotFoundError:
        pass
    return conf


class Detector:
    """Recibe frames (PIL.Image, tiempo) y devuelve los que hay que guardar."""

    def __init__(self, conf):
        self.c = conf
        self.guardado = None     # versión reducida de la última captura guardada
        self.prev = None         # (imagen, reducida, t) del frame anterior
        self.pendiente_desde = None
        self.ultimo_cambio = 0.0
        self.puntero = None       # bloques donde está ahora el mouse del profe
        self.sucio = None         # bloques con cambios reales (no del mouse) desde la última captura
        self.firma_prev = None    # resumen de cada bloque en el frame anterior
        self.firma_antes = None   # resumen de cada bloque antes de su último cambio
        self.oscila = None        # cuántas veces volvió cada bloque a su estado anterior (A→B→A)
        self.actividad = None     # qué tan seguido cambia cada bloque (promedio móvil, 0 a 1)
        self.historial = deque(maxlen=int(conf["HISTORIAL"]))  # últimas capturas guardadas
        self.parpadeo = None      # bloques ignorados en este frame (parpadeos, webcam)
        self.repetidas = 0        # capturas no guardadas por ser iguales a una anterior
        self.ultimo_grande = None  # momento del último cambio grande (scroll, diapositiva)

    def _reducir(self, img):
        g = np.asarray(img.convert("L").reduce(2), dtype=np.int16)
        h = g.shape[0] - int(g.shape[0] * self.c["MASCARA_ABAJO"])
        g = g[:h]
        return g[: h - h % BLOQUE, : g.shape[1] - g.shape[1] % BLOQUE]

    @staticmethod
    def _en_bloques(m):
        h, w = m.shape
        return m.reshape(h // BLOQUE, BLOQUE, w // BLOQUE, BLOQUE).swapaxes(1, 2)

    def _cambios(self, a, b):
        """Grilla booleana de bloques cambiados entre a y b."""
        return self._bloques_distintos(np.abs(a - b) > self.c["RUIDO"])

    def _bloques_distintos(self, dif):
        """De una máscara de píxeles distintos, a la grilla de bloques que cambiaron."""
        bl = self._en_bloques(self._quitar_cursor(dif))
        return bl.sum(axis=(2, 3)) >= self.c["MIN_PIXELES"]

    @staticmethod
    def _quitar_cursor(dif):
        """Quita el cursor de texto parpadeando del editor del video: una raya vertical de
        1-2 px de ancho y del alto de la línea (>= 8 px acá). El trazo que cambia entre dos
        caracteres (un 3 que pasa a 8) es más bajito, así que queda."""
        if not dif.any():
            return dif
        # raya vertical de >= 8 px: "erosión" vertical (8 filas seguidas distintas) y después
        # "dilatación" para marcar todos los píxeles de esa raya
        h = dif.shape[0]
        inicio = dif[:h - 7].copy()
        for k in range(1, 8):
            inicio &= dif[k:h - 7 + k]
        raya = np.zeros_like(dif)
        for k in range(8):
            raya[k:h - 7 + k] |= inicio
        # que sea finita: sin píxeles distintos a 2 columnas de distancia en esa fila
        lados = np.zeros_like(dif)
        lados[:, 2:] |= dif[:, :-2]
        lados[:, :-2] |= dif[:, 2:]
        return dif & ~(raya & ~lados)

    def _fraccion(self, cambiado, a, b):
        """Fracción de los bloques con contenido (texto, dibujos) que cambiaron.

        Se mide sobre el contenido, no sobre toda la pantalla: en un editor casi todo es
        fondo, y un scroll igual tiene que contar como cambio grande.
        """
        if not cambiado.any():
            return 0.0
        contenido = (self._en_bloques(a).std(axis=(2, 3)) > 10) | (self._en_bloques(b).std(axis=(2, 3)) > 10)
        return cambiado.sum() / max(contenido.sum(), cambiado.sum())

    @staticmethod
    def _manchas(grilla):
        """Grupos de bloques cambiados que se tocan (lista de listas de (fila, col))."""
        pendientes = set(zip(*np.nonzero(grilla)))
        grupos = []
        while pendientes:
            pila, grupo = [pendientes.pop()], []
            while pila:
                i, j = pila.pop()
                grupo.append((i, j))
                for v in [(i + di, j + dj) for di in (-1, 0, 1) for dj in (-1, 0, 1)]:
                    if v in pendientes:
                        pendientes.remove(v)
                        pila.append(v)
            grupos.append(grupo)
        return grupos

    def _clasificar(self, manchas, vs_guardado):
        """Separa las manchas (cambios entre dos frames) en mouse del profe y cambios reales.

        Una mancha chica (un puntero ocupa 1-2 bloques) es el mouse si además:
        - hay 2+ manchas chicas (desaparece en un lugar, aparece en otro), o
        - una parte volvió a como estaba en la captura guardada (el puntero se fue de ahí), o
        - toca donde ya sabíamos que estaba el puntero.
        Una letra tipeada aparece y se queda: no cumple nada de esto.
        Una mancha que volvió entera a como estaba guardado (un deshacer, algo que parpadea)
        no es cambio.
        """
        chicas = [m for m in manchas if self._chica(m)]
        cerca = self._dilatar(self.puntero)
        puntero, reales = [], []
        for m in manchas:
            revertida = [not vs_guardado[b] for b in m]
            if m in chicas and (len(chicas) >= 2 or any(revertida) or any(cerca[b] for b in m)):
                puntero.append(m)
            elif not all(revertida):
                reales.append(m)
        return puntero, reales

    @staticmethod
    def _chica(m):
        """Del tamaño de un puntero (o de una palabra corta): hasta ~3x3 bloques."""
        filas = [i for i, _ in m]
        cols = [j for _, j in m]
        return len(m) <= 6 and max(filas) - min(filas) <= 2 and max(cols) - min(cols) <= 2

    def _firma(self, red):
        """Resumen de cada bloque: promedio de sus 16 sub-bloques de 4x4 px."""
        b = self._en_bloques(red)
        r, c = b.shape[:2]
        return b.reshape(r, c, 4, 4, 4, 4).mean(axis=(3, 5)).reshape(r, c, 16)

    @staticmethod
    def _dilatar(g):
        d = g.copy()
        d[1:] |= g[:-1]
        d[:-1] |= g[1:]
        d[:, 1:] |= d[:, :-1]
        d[:, :-1] |= d[:, 1:]
        return d

    def _ya_guardada(self, red, mapa=None):
        """¿Todo lo que se ve ya está en las últimas capturas? (el profe volvió con scroll a
        una parte anterior, aunque quede unas líneas más arriba o más abajo).

        Cada parte de la pantalla tiene que aparecer igual en alguna captura anterior, en el
        mismo lugar o corrida verticalmente (scroll). Solo se ignoran la webcam, lo que
        parpadea y el mouse: un solo carácter distinto hace que se guarde.
        """
        # Unidad de comparación: un pedazo de fila de 1 px de alto x 160 px de ancho, que tiene
        # que coincidir entero, en UNA captura y UN corrimiento, junto con al menos 9 filas
        # vecinas: así un carácter cambiado arrastra a toda su línea y no puede "cubrirse" por
        # casualidad con pedazos de otras líneas. Como la unidad es la fila, una línea partida
        # entre dos capturas igual se reconoce. Ruido y cursor de texto se quitan antes.
        ignorar = self.parpadeo | self._dilatar(self.puntero)
        ignorar_px = np.repeat(np.repeat(ignorar, BLOQUE, axis=0), BLOQUE, axis=1)
        filas, franjas = red.shape[0], red.shape[1] // 160
        cubierto = np.zeros((filas, franjas), dtype=bool)
        # un pedazo que cae entero en zonas ignoradas no hace falta cubrirlo
        cubierto |= ignorar_px[:, :franjas * 160].reshape(filas, franjas, 160).all(axis=2)

        def ok_de(vieja):
            dif = self._sin_ruido_ni_cursor((np.abs(vieja - red) > self.c["RUIDO"]) & ~ignorar_px)
            return ~dif[:, :franjas * 160].reshape(filas, franjas, 160).any(axis=2)

        # Una línea de texto tiene que cubrirse entera con UNA captura y UN corrimiento: si no,
        # se podría "armar" una línea que nunca existió con la mitad izquierda de una y la
        # derecha de otra. Se "atan" dos franjas vecinas cuando el texto sigue de una a la otra
        # (hay texto a menos de 32 px del borde en las dos, en esa línea). Un panel al costado
        # separado por un espacio no queda atado al código, y puede estar en otro corrimiento.
        bordes_h = np.pad(np.abs(np.diff(red, axis=1)) > self.c["RUIDO"], ((0, 0), (0, 1)))
        atada = np.zeros((filas, max(franjas - 1, 0)), dtype=bool)
        for f in range(franjas - 1):
            corte = (f + 1) * 160
            atada[:, f] = bordes_h[:, corte - 32:corte].any(axis=1) & bordes_h[:, corte:corte + 32].any(axis=1)
        linea = atada.copy()  # extender a toda la línea (± 6 filas)
        for k in range(1, 7):
            linea[k:] |= atada[:-k]
            linea[:-k] |= atada[k:]
        atada = linea

        def cubrir(vieja):
            ok = ok_de(vieja)
            for _ in range(franjas - 1):  # propagar por cadenas de franjas atadas
                ok[:, :-1] &= ok[:, 1:] | ~atada
                ok[:, 1:] &= ok[:, :-1] | ~atada
            # Solo valen tramos de >= 10 filas seguidas (una línea de texto entera con su
            # espacio): una fila suelta de un dígito se puede parecer a la de otro dígito.
            for f in range(franjas):
                bordes = np.diff(np.concatenate(([0], ok[:, f].astype(np.int8), [0])))
                for ini, fin in zip(np.nonzero(bordes == 1)[0], np.nonzero(bordes == -1)[0]):
                    if fin - ini >= 10:
                        cubierto[ini:fin, f] = True
            if mapa is not None:  # para auditar: qué quedó sin cubrir (filas x franjas)
                mapa[:] = cubierto
            return cubierto.all()

        rn = self._resumen(red)
        for h, rv in reversed(self.historial):
            if cubrir(h):
                return True
            for dy in self._desplazamientos(h, red, rv, rn):
                corrida = np.full_like(red, -1000)  # -1000 = sin datos (fuera de la captura vieja)
                if dy > 0:
                    corrida[dy:] = h[:-dy]
                else:
                    corrida[:dy] = h[-dy:]
                if cubrir(corrida):
                    return True
        return False

    def _sin_ruido_ni_cursor(self, dif):
        """Quita de una máscara de píxeles distintos lo que no es un cambio: píxeles sueltos
        sin ningún vecino distinto (ruido de compresión) y el cursor de texto. Un carácter
        cambiado deja varios píxeles juntos, así que queda."""
        if not dif.any():
            return dif
        p = np.pad(dif, 1)
        vecinos = np.zeros_like(dif)
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dy or dx:
                    vecinos |= p[1 + dy:p.shape[0] - 1 + dy, 1 + dx:p.shape[1] - 1 + dx]
        return self._quitar_cursor(dif & vecinos)

    @staticmethod
    def _resumen(x):
        """Cada fila resumida en 6 franjas de 160 px, promedio cada 16 px: (filas, 6, 10).
        Es solo para proponer candidatos; la verificación después es píxel por píxel."""
        w = x.shape[1] // 160 * 160
        return x[:, :w].reshape(x.shape[0], w // 160, 10, 16).mean(axis=3).astype(np.int16)

    def _desplazamientos(self, vieja, nueva, rv=None, rn=None):
        """Scrolls verticales (px de la imagen reducida) que alinean la captura vieja con la
        nueva (hasta 6 candidatos).

        Cada fila se resume en franjas verticales (así un panel fijo al costado no molesta).
        Se arma la matriz "fila i de la nueva == fila j de la vieja" y cada scroll dy es una
        diagonal: se cuentan las filas con texto que coinciden. Las filas vacías no cuentan
        porque coinciden con cualquier cosa.
        """
        rv = self._resumen(vieja) if rv is None else rv
        rn = self._resumen(nueva) if rn is None else rn
        h, nf = rn.shape[0], rn.shape[1]
        con_texto = rn.std(axis=2) > 4  # (filas, franjas)
        puntaje = np.zeros(2 * h - 1)
        posibles = np.zeros(3 * h)  # filas con texto que se superponen en cada dy (diferencias)
        for f in range(nf):
            filas = np.nonzero(con_texto[:, f])[0][::2]  # 1 de cada 2 filas alcanza para proponer
            if len(filas) == 0:
                continue
            # iguales[i, j]: fila filas[i] de la nueva coincide con la fila j de la vieja
            iguales = np.abs(rn[filas, f][:, None, :] - rv[:, f][None, :, :]).max(axis=2) < self.c["RUIDO"] / 2
            ii, jj = np.nonzero(iguales)
            puntaje += np.bincount(filas[ii] - jj + h - 1, minlength=2 * h - 1)  # dy = i - j
            # con dy, la fila i de la nueva viene de la j = i - dy de la vieja: cada fila con
            # texto se superpone en los dy de i-(h-1) a i, o sea índices i .. i+h-1
            posibles += np.bincount(filas, minlength=3 * h) - np.bincount(filas + h, minlength=3 * h)
        posibles = np.cumsum(posibles)[:2 * h - 1]
        puntaje[h - 1] = 0  # dy = 0 ya se prueba aparte
        # Candidatos: los de más filas iguales (scroll chico) y los de mayor proporción
        # (scroll grande: se superponen pocas filas, pero todas coinciden).
        proporcion = np.where(posibles >= 4, puntaje / np.maximum(posibles, 1), 0)
        mejores = list(np.argsort(puntaje)[::-1][:3]) + list(np.argsort(proporcion)[::-1][:3])
        return list(dict.fromkeys(int(k - (h - 1)) for k in mejores if puntaje[k] >= 2))

    def _guardar(self, img, red, t, guardar):
        if self.historial and self._ya_guardada(red):
            self.repetidas += 1
        else:
            guardar.append((img, t))
            self.historial.append((red, self._resumen(red)))
        self.guardado = red
        self.pendiente_desde = None
        self.sucio[:] = False
        self.hay_pendiente = False

    def alimentar(self, img, t):
        red = self._reducir(img)
        guardar = []
        if self.guardado is None:
            self.guardado = red
            self.prev = (img, red, t)
            vacia = np.zeros(self._cambios(red, red).shape, dtype=bool)
            self.puntero, self.sucio = vacia, vacia.copy()
            self.firma_prev = self._firma(red)
            self.firma_antes = self.firma_prev.copy()
            self.oscila = np.zeros(vacia.shape)
            self.actividad = np.zeros(vacia.shape)
            self.historial.append((red, self._resumen(red)))
            return [(img, t)]

        vs_prev = self._cambios(self.prev[1], red)
        vs_guardado = self._cambios(self.guardado, red)
        # Bloques que van y vuelven entre dos estados (A→B→A: iconos que parpadean, el mouse
        # pasando): se ignoran mientras sigan haciéndolo. Tipear nunca vuelve a un estado viejo.
        # Solo cuentan zonas chicas: un scroll de ida y vuelta también vuelve a un estado
        # anterior, y no por eso hay que ignorar la pantalla entera.
        chico, mediano = np.zeros_like(vs_prev), np.zeros_like(vs_prev)
        for m in self._manchas(vs_prev):
            for b in m:
                chico[b] = len(m) <= 12
                mediano[b] = len(m) <= 250  # webcam ~120 bloques; un scroll, cientos o miles
        firma = self._firma(red)
        vuelve = chico & (np.abs(firma - self.firma_antes).max(axis=2) < self.c["RUIDO"] / 2)
        self.oscila *= 0.97
        self.oscila[vuelve] += 1
        self.firma_antes[vs_prev] = self.firma_prev[vs_prev]
        self.firma_prev = firma
        # Zonas que se mueven casi siempre (la webcam del profe, un video dentro del video):
        # el código se tipea y se queda quieto; una cara se mueve sin parar.
        self.actividad = self.actividad * 0.95 + 0.05 * mediano
        parpadeo = (self.oscila >= 2) | self._dilatar(self.actividad > 0.5)
        self.parpadeo = parpadeo
        vs_prev &= ~parpadeo
        vs_guardado &= ~parpadeo

        puntero, reales = self._clasificar(self._manchas(vs_prev), vs_guardado)
        if puntero:
            self.puntero[:] = False
            for m in puntero:
                for b in m:
                    self.puntero[b] = True
        if reales:
            self.ultimo_cambio = t
            reales_g = np.zeros_like(vs_prev)
            for m in reales:
                for b in m:
                    reales_g[b] = True
            # Cambio grande (scroll, otro archivo, otra diapositiva) y el frame anterior
            # tenía algo sin guardar: guardarlo, es la versión más completa.
            # (Si casi todo lo que cambió ya se venía moviendo, es la webcam arrancando, no un scroll.)
            # (Y si el frame anterior también era un cambio grande, está a mitad de un scroll:
            # ese no se guarda, se guarda donde la pantalla se quede quieta.)
            ya_se_movia = (self.actividad[reales_g] > 0.06).mean()
            grande = self._fraccion(reales_g, self.prev[1], red) >= self.c["GRANDE"] and ya_se_movia < 0.5
            if (grande and self.ultimo_grande != self.prev[2]
                    and (self._cambios(self.guardado, self.prev[1]) & self.sucio).any()):
                self._guardar(self.prev[0], self.prev[1], self.prev[2], guardar)
                vs_guardado = self._cambios(self.guardado, red) & ~parpadeo
            if grande:
                self.ultimo_grande = t
            self.sucio |= reales_g

        # Pendiente = algo cambió de verdad respecto de la última captura. Lo que hizo el
        # mouse nunca marca "sucio", así que no importa por dónde pasó. Una sola mancha
        # chica suelta (puntero que reaparece, una letra cambiada) no dispara sola: queda
        # esperando y entra en la próxima captura (o en la de antes de un scroll/cambio de
        # diapositiva), así no se pierde; si era el puntero, desaparece cuando se va.
        sucio = vs_guardado & self.sucio
        grupos = self._manchas(sucio)
        self.hay_pendiente = bool(grupos)
        if len(grupos) > 1 and sucio.sum() > 8 or any(not self._chica(g) for g in grupos):
            if self.pendiente_desde is None:
                self.pendiente_desde = t
            quieto = t - self.ultimo_cambio >= self.c["ESTABLE"]
            tope = t - self.pendiente_desde >= self.c["TOPE"]
            if quieto or tope:
                self._guardar(img, red, t, guardar)
        else:
            self.pendiente_desde = None

        self.prev = (img, red, t)
        return guardar

    def cerrar(self):
        """Al terminar: guardar lo que haya quedado sin guardar."""
        if getattr(self, "hay_pendiente", False) and self.prev:
            return [(self.prev[0], self.prev[2])]
        return []


MINUTOS = ".minutos.tsv"  # "0001.webp<TAB>01-23-45": minuto del video (en vivo: hora del día)


class Guardador:
    def __init__(self, carpeta, en_vivo):
        os.makedirs(carpeta, exist_ok=True)
        self.carpeta = carpeta
        self.en_vivo = en_vivo
        self.n = 0
        if os.path.exists(os.path.join(carpeta, MINUTOS)):  # de una corrida anterior cortada
            os.remove(os.path.join(carpeta, MINUTOS))

    def __call__(self, pares):
        for img, t in pares:
            self.n += 1
            if self.en_vivo:
                marca = time.strftime("%H-%M-%S", time.localtime(t))
            else:  # minuto del video: sirve para volver a ese punto
                s = int(t)
                marca = f"{s // 3600:02d}-{s % 3600 // 60:02d}-{s % 60:02d}"
            # Nombre corto (0001.webp); el minuto va en .minutos.tsv (lo usa cuadernillo.py).
            # WebP SIN pérdida: píxeles idénticos al PNG y ~43 % menos de espacio. method=1 es
            # casi tan chico como el máximo (6) y mucho más rápido (~0,5 s por captura 1080p).
            nombre = f"{self.n:04d}.webp"
            img.save(os.path.join(self.carpeta, nombre), "WEBP", lossless=True, method=1, quality=50)
            with open(os.path.join(self.carpeta, MINUTOS), "a", encoding="utf-8") as f:
                f.write(f"{nombre}\t{marca}\n")


def modo_vivo(monitor, conf, guardar):
    corriendo = [True]
    signal.signal(signal.SIGTERM, lambda *_: corriendo.__setitem__(0, False))
    signal.signal(signal.SIGINT, lambda *_: corriendo.__setitem__(0, False))
    det = Detector(conf)
    while corriendo[0]:
        inicio = time.time()
        r = subprocess.run(["grim", "-t", "ppm", "-o", monitor, "-"], capture_output=True)
        if r.returncode == 0:
            guardar(det.alimentar(Image.open(io.BytesIO(r.stdout)), inicio))
        resto = conf["INTERVALO"] - (time.time() - inicio)
        while resto > 0 and corriendo[0]:
            time.sleep(min(resto, 0.2))
            resto -= 0.2
    guardar(det.cerrar())


def modo_video(ruta, conf, guardar):
    info = json.loads(subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=width,height:format=duration", "-of", "json", ruta],
        capture_output=True, check=True).stdout)
    w, h = info["streams"][0]["width"], info["streams"][0]["height"]
    dur = float(info.get("format", {}).get("duration", 0) or 0)
    if w > 1920:  # 4K -> 1080p: el código se sigue leyendo y cada captura pesa ~4 veces menos
        w, h = 1920, int(h * 1920 / w) // 2 * 2
    ff = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-i", ruta, "-map", "0:v:0", "-vf", f"fps=1,scale={w}:{h}",
         "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    det = Detector(conf)
    tam, t = w * h * 3, 0
    while True:
        buf = ff.stdout.read(tam)
        if len(buf) < tam:
            break
        guardar(det.alimentar(Image.frombytes("RGB", (w, h), buf), float(t)))
        t += 1
        if t % 60 == 0 and dur:
            print(f"\r{t / dur:5.1%}  ({guardar.n} capturas)", end="", flush=True)
            reportar(100 * t / dur, "capturas", f"{guardar.n} guardadas")
    guardar(det.cerrar())
    ff.wait()
    print(f"\rListo: {guardar.n} capturas ({det.repetidas} repetidas descartadas) en {guardar.carpeta}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", required=True)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--monitor")
    g.add_argument("--video")
    a = p.parse_args()
    conf = leer_conf()
    guardar = Guardador(a.out, en_vivo=bool(a.monitor))
    if a.monitor:
        modo_vivo(a.monitor, conf, guardar)
    else:
        modo_video(a.video, conf, guardar)
    with open(os.path.join(a.out, ".cantidad"), "w") as f:
        f.write(str(guardar.n))


if __name__ == "__main__":
    sys.exit(main())
