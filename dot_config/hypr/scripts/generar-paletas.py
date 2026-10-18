#!/usr/bin/env python3
"""generar-paletas.py — crea los esquemas de color de noctalia (~/.config/noctalia/palettes/*.json).

Cada esquema tiene versión oscura y clara. Se parte de los colores oficiales de cada tema
(Catppuccin, Dracula, Nord…) y se CORRIGE lo que no se lee bien: todo color que se usa como
texto debe tener contraste ≥ 4.5:1 con el fondo (norma WCAG AA); si no llega, se oscurece
(modo claro) o aclara (modo oscuro) lo justo. Así el verde de la terminal sigue siendo verde,
pero legible. El selector (SUPER+SHIFT+A → Colores) lee ESQUEMAS para dibujar las tarjetas.

  python3 generar-paletas.py          escribe los .json y muestra el contraste de cada uno
"""
import colorsys
import json
from pathlib import Path

DESTINO = Path.home() / ".config/noctalia/palettes"
ANSI = ("black", "red", "green", "yellow", "blue", "magenta", "cyan", "white")

# Por modo: fondo, fondo2 (tarjetas/paneles), texto, texto2 (secundario), borde,
# primario, secundario, terciario, error y los 8 colores ANSI (normal / brillante).
ESQUEMAS = {
    "yafer": {
        "nombre": "Yafer", "desc": "Violeta suave · papel", "icono": "💜",
        "dark": dict(fondo="#1a1c23", fondo2="#2b2e3b", texto="#f2f2f3", texto2="#b4b5bd", borde="#61677a",
                     pri="#8fa0ec", sec="#b48ae6", ter="#d48fd9", err="#fd5c75",
                     n=["#3b3f4e", "#ff6b81", "#8fd18a", "#f2c46d", "#82aaff", "#c79bf2", "#7fd6d0", "#c9cad3"],
                     b=["#70758a", "#ff8597", "#a6e3a1", "#f9d58a", "#9fbcff", "#d7b3f7", "#9ae6e0", "#f2f2f3"]),
        "light": dict(fondo="#f4efe6", fondo2="#e8e1d5", texto="#3a3644", texto2="#5c566a", borde="#a29bab",
                      pri="#6f45ad", sec="#b4334e", ter="#2c64a0", err="#b4334e",
                      n=["#5f5a6b", "#b4334e", "#3d7a37", "#9a600c", "#2c64a0", "#8547ad", "#1f7776", "#9d97a8"],
                      b=["#716b7d", "#a92c46", "#356c30", "#8a550a", "#275a91", "#783ea0", "#1b6a69", "#b8b2c2"]),
    },
    "pastel": {
        "nombre": "Pastel", "desc": "Lavanda · rosa · menta", "icono": "🌸",
        "dark": dict(fondo="#25212f", fondo2="#322c40", texto="#f3eef9", texto2="#c6bdd6", borde="#6e6684",
                     pri="#c9a8ff", sec="#ffb4c8", ter="#a8e6cf", err="#ff8fa3",
                     n=["#3d3650", "#ff9fb2", "#a8e6b4", "#ffe0a3", "#a9c7ff", "#d9b8ff", "#a3e4e0", "#d5cee3"],
                     b=["#7a7192", "#ffb8c6", "#c0f0c8", "#ffecbf", "#c2d7ff", "#e6ccff", "#bdf0ec", "#f3eef9"]),
        "light": dict(fondo="#f8f2f6", fondo2="#efe5ee", texto="#3d3447", texto2="#625870", borde="#b3a6bf",
                      pri="#7b54c4", sec="#b8457a", ter="#2f7d6b", err="#b83a55",
                      n=["#655b72", "#c2456a", "#3f8a5a", "#a8701c", "#4a6fc0", "#9a52c2", "#2c8a86", "#a79cb3"],
                      b=["#7b7088", "#b03a5e", "#357a4e", "#946214", "#3f62ad", "#8a46b0", "#267a76", "#c2b8cc"]),
    },
    "dracula": {
        "nombre": "Dracula", "desc": "Morado y neón · Alucard en claro", "icono": "🧛",
        "dark": dict(fondo="#282a36", fondo2="#343746", texto="#f8f8f2", texto2="#c0c3d6", borde="#6272a4",
                     pri="#bd93f9", sec="#ff79c6", ter="#8be9fd", err="#ff5555",
                     n=["#21222c", "#ff5555", "#50fa7b", "#f1fa8c", "#bd93f9", "#ff79c6", "#8be9fd", "#f8f8f2"],
                     b=["#6272a4", "#ff6e6e", "#69ff94", "#ffffa5", "#d6acff", "#ff92df", "#a4ffff", "#ffffff"]),
        "light": dict(fondo="#fffbeb", fondo2="#efeddc", texto="#1f1f1f", texto2="#4f4c5e", borde="#a8a6b8",
                      pri="#644ac9", sec="#a3144d", ter="#036a96", err="#cb3a2a",
                      n=["#635d97", "#cb3a2a", "#14710a", "#846e15", "#644ac9", "#a3144d", "#036a96", "#a8a6b8"],
                      b=["#7a75a8", "#b83325", "#126509", "#756212", "#5940b5", "#931245", "#035e85", "#c4c2d0"]),
    },
    "catppuccin": {
        "nombre": "Catppuccin", "desc": "Mocha en oscuro · Latte en claro", "icono": "🐱",
        "dark": dict(fondo="#1e1e2e", fondo2="#313244", texto="#cdd6f4", texto2="#a6adc8", borde="#6c7086",
                     pri="#cba6f7", sec="#f5c2e7", ter="#94e2d5", err="#f38ba8",
                     n=["#45475a", "#f38ba8", "#a6e3a1", "#f9e2af", "#89b4fa", "#f5c2e7", "#94e2d5", "#bac2de"],
                     b=["#6c7086", "#f38ba8", "#a6e3a1", "#f9e2af", "#89b4fa", "#f5c2e7", "#94e2d5", "#cdd6f4"]),
        "light": dict(fondo="#eff1f5", fondo2="#e6e9ef", texto="#4c4f69", texto2="#5c5f77", borde="#9ca0b0",
                      pri="#8839ef", sec="#ea76cb", ter="#179299", err="#d20f39",
                      n=["#5c5f77", "#d20f39", "#40a02b", "#df8e1d", "#1e66f5", "#ea76cb", "#179299", "#acb0be"],
                      b=["#6c6f85", "#d20f39", "#40a02b", "#df8e1d", "#1e66f5", "#ea76cb", "#179299", "#bcc0cc"]),
    },
    "tokyo": {
        "nombre": "Tokyo Night", "desc": "Noche de Tokio · Day en claro", "icono": "🌃",
        "dark": dict(fondo="#1a1b26", fondo2="#24283b", texto="#c0caf5", texto2="#a9b1d6", borde="#565f89",
                     pri="#7aa2f7", sec="#bb9af7", ter="#7dcfff", err="#f7768e",
                     n=["#414868", "#f7768e", "#9ece6a", "#e0af68", "#7aa2f7", "#bb9af7", "#7dcfff", "#a9b1d6"],
                     b=["#565f89", "#ff899d", "#9fe044", "#faba4a", "#8db0ff", "#c7a9ff", "#a4daff", "#c0caf5"]),
        "light": dict(fondo="#e1e2e7", fondo2="#d4d6e4", texto="#2e3c6e", texto2="#4a5585", borde="#9699a3",
                      pri="#2e7de9", sec="#9854f1", ter="#007197", err="#f52a65",
                      n=["#6172b0", "#f52a65", "#587539", "#8c6c3e", "#2e7de9", "#9854f1", "#007197", "#a1a6c5"],
                      b=["#7480b5", "#f52a65", "#587539", "#8c6c3e", "#2e7de9", "#9854f1", "#007197", "#b8bcd6"]),
    },
    "nord": {
        "nombre": "Nord", "desc": "Ártico, azules calmados", "icono": "❄️",
        "dark": dict(fondo="#2e3440", fondo2="#3b4252", texto="#eceff4", texto2="#d0d6e0", borde="#4c566a",
                     pri="#88c0d0", sec="#81a1c1", ter="#b48ead", err="#bf616a",
                     n=["#3b4252", "#bf616a", "#a3be8c", "#ebcb8b", "#81a1c1", "#b48ead", "#88c0d0", "#e5e9f0"],
                     b=["#616e88", "#d08770", "#b5cf9e", "#f2d9a5", "#8fbcbb", "#c6a0c0", "#9fd0de", "#eceff4"]),
        "light": dict(fondo="#eceff4", fondo2="#e0e5ed", texto="#2e3440", texto2="#4c566a", borde="#a7b1c2",
                      pri="#5e81ac", sec="#b48ead", ter="#3f8ea0", err="#bf616a",
                      n=["#4c566a", "#bf616a", "#5f8a3f", "#a37a1f", "#5e81ac", "#9a6b93", "#3f8ea0", "#aab3c4"],
                      b=["#616e88", "#b05560", "#557d38", "#946e1a", "#53749c", "#8c5f86", "#378092", "#c3cad6"]),
    },
    "rosepine": {
        "nombre": "Rosé Pine", "desc": "Pino y rosa · Dawn en claro", "icono": "🌹",
        "dark": dict(fondo="#191724", fondo2="#26233a", texto="#e0def4", texto2="#a8a4c2", borde="#6e6a86",
                     pri="#c4a7e7", sec="#ebbcba", ter="#9ccfd8", err="#eb6f92",
                     n=["#26233a", "#eb6f92", "#31748f", "#f6c177", "#9ccfd8", "#c4a7e7", "#ebbcba", "#e0def4"],
                     b=["#6e6a86", "#eb6f92", "#3e8fb0", "#f6c177", "#9ccfd8", "#c4a7e7", "#ebbcba", "#e0def4"]),
        "light": dict(fondo="#faf4ed", fondo2="#f2e9e1", texto="#575279", texto2="#6e6a8e", borde="#b4afc2",
                      pri="#907aa9", sec="#d7827e", ter="#286983", err="#b4637a",
                      n=["#6e6a86", "#b4637a", "#286983", "#ea9d34", "#56949f", "#907aa9", "#d7827e", "#b4afc2"],
                      b=["#797593", "#b4637a", "#286983", "#ea9d34", "#56949f", "#907aa9", "#d7827e", "#cecacd"]),
    },
    "gruvbox": {
        "nombre": "Gruvbox", "desc": "Retro cálido, tonos tierra", "icono": "🍂",
        "dark": dict(fondo="#282828", fondo2="#3c3836", texto="#ebdbb2", texto2="#d5c4a1", borde="#665c54",
                     pri="#fabd2f", sec="#fe8019", ter="#8ec07c", err="#fb4934",
                     n=["#3c3836", "#cc241d", "#98971a", "#d79921", "#458588", "#b16286", "#689d6a", "#a89984"],
                     b=["#7c6f64", "#fb4934", "#b8bb26", "#fabd2f", "#83a598", "#d3869b", "#8ec07c", "#ebdbb2"]),
        "light": dict(fondo="#fbf1c7", fondo2="#ebdbb2", texto="#3c3836", texto2="#504945", borde="#a89984",
                      pri="#af3a03", sec="#8f3f71", ter="#427b58", err="#9d0006",
                      n=["#665c54", "#9d0006", "#79740e", "#b57614", "#076678", "#8f3f71", "#427b58", "#a89984"],
                      b=["#7c6f64", "#9d0006", "#79740e", "#b57614", "#076678", "#8f3f71", "#427b58", "#bdae93"]),
    },
    "everforest": {
        "nombre": "Everforest", "desc": "Bosque verde, relajante", "icono": "🌲",
        "dark": dict(fondo="#2d353b", fondo2="#3d484d", texto="#d3c6aa", texto2="#a9b3a8", borde="#7a8478",
                     pri="#a7c080", sec="#83c092", ter="#dbbc7f", err="#e67e80",
                     n=["#475258", "#e67e80", "#a7c080", "#dbbc7f", "#7fbbb3", "#d699b6", "#83c092", "#d3c6aa"],
                     b=["#859289", "#f08b8d", "#b8d191", "#e8c98c", "#8fcac2", "#e2a8c3", "#94d0a3", "#e6dcc3"]),
        "light": dict(fondo="#fdf6e3", fondo2="#f0ead2", texto="#4d5a61", texto2="#5c6a72", borde="#bdc3af",
                      pri="#8da101", sec="#35a77c", ter="#dfa000", err="#f85552",
                      n=["#5c6a72", "#f85552", "#8da101", "#dfa000", "#3a94c5", "#df69ba", "#35a77c", "#bdc3af"],
                      b=["#829181", "#f85552", "#8da101", "#dfa000", "#3a94c5", "#df69ba", "#35a77c", "#d3d8c6"]),
    },
    "sweet": {
        "nombre": "Sweet", "desc": "Synthwave: rosa, morado y cian", "icono": "🍭",
        "dark": dict(fondo="#1b1529", fondo2="#2a2140", texto="#f5ecff", texto2="#c8b8e3", borde="#6a5a8c",
                     pri="#ff5fa2", sec="#c74ded", ter="#00d1e8", err="#ff4f6d",
                     n=["#3a2f55", "#ff4f6d", "#5fffa8", "#ffd36b", "#6d9bff", "#d36bff", "#3fe3f0", "#d8cce8"],
                     b=["#7a6a9c", "#ff7a90", "#8affc1", "#ffe08f", "#93b5ff", "#e094ff", "#7aeef6", "#f5ecff"]),
        "light": dict(fondo="#fbf3fb", fondo2="#f1e4f3", texto="#3a2547", texto2="#5d4570", borde="#c3a8cf",
                      pri="#c2185b", sec="#8e24aa", ter="#00838f", err="#c62828",
                      n=["#6a5578", "#c2185b", "#2e7d32", "#a15c00", "#3949ab", "#8e24aa", "#00838f", "#b9a6c4"],
                      b=["#7d688b", "#ad1457", "#276b2b", "#8d5000", "#303f9f", "#7b1fa2", "#00737d", "#d2c3da"]),
    },
    "macos": {
        "nombre": "Estilo macOS", "desc": "Limpio como WhiteSur", "icono": "🍎",
        "dark": dict(fondo="#1e1e20", fondo2="#2c2c2e", texto="#f5f5f7", texto2="#b0b0b5", borde="#5a5a5f",
                     pri="#0a84ff", sec="#bf5af2", ter="#ff9f0a", err="#ff453a",
                     n=["#3a3a3c", "#ff6961", "#5fd068", "#ffd60a", "#64a8ff", "#da8fff", "#70d7ff", "#c7c7cc"],
                     b=["#76767c", "#ff8a84", "#7fe08a", "#ffe24d", "#8cbfff", "#e5adff", "#9ae3ff", "#f5f5f7"]),
        "light": dict(fondo="#f5f5f7", fondo2="#e8e8ed", texto="#1d1d1f", texto2="#515154", borde="#b0b0b8",
                      pri="#0062cc", sec="#8944ab", ter="#c9341a", err="#d70015",
                      n=["#58585d", "#d70015", "#248a3d", "#a05a00", "#0062cc", "#8944ab", "#0071a4", "#a8a8ad"],
                      b=["#6e6e73", "#c20012", "#1f7a36", "#8f5000", "#0058b8", "#7a3c99", "#006592", "#c7c7cc"]),
    },
    "arc": {
        "nombre": "Arc", "desc": "Plano y minimalista", "icono": "🌀",
        "dark": dict(fondo="#2f343f", fondo2="#383c4a", texto="#e2e7ee", texto2="#b3bac5", borde="#5c6370",
                     pri="#5294e2", sec="#a67fd8", ter="#5fc1b5", err="#e2565a",
                     n=["#404552", "#f06e72", "#8fcf7a", "#efc471", "#6fa8ec", "#c19ae6", "#6fd0c4", "#c5ccd6"],
                     b=["#727a88", "#ff8b8e", "#a6dd94", "#f6d48f", "#8ebcf2", "#d3b4ee", "#8cdcd2", "#e2e7ee"]),
        "light": dict(fondo="#f5f6f7", fondo2="#e7e8eb", texto="#2f343f", texto2="#4b5162", borde="#b8bcc4",
                      pri="#2f6fbf", sec="#7a52b3", ter="#1f7f73", err="#c0392b",
                      n=["#5c6370", "#c0392b", "#2f7d32", "#9a6400", "#2f6fbf", "#7a52b3", "#1f7f73", "#aab0ba"],
                      b=["#707785", "#a93226", "#286b2b", "#865700", "#285fa6", "#6a479c", "#196b61", "#c6cad1"]),
    },
}


def rgb(h):
    return tuple(int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))


def hexa(c):
    return "#{:02x}{:02x}{:02x}".format(*(round(max(0, min(1, x)) * 255) for x in c))


def luminancia(h):
    def canal(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (canal(x) for x in rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contraste(a, b):
    la, lb = sorted((luminancia(a), luminancia(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def asegurar(color, fondo, minimo):
    """Ajusta la luminosidad (sin tocar el tono) hasta tener `minimo` de contraste con `fondo`."""
    if contraste(color, fondo) >= minimo:
        return color
    h, l, s = colorsys.rgb_to_hls(*rgb(color))
    oscurecer = luminancia(fondo) > 0.25
    for _ in range(100):
        l = l - 0.01 if oscurecer else l + 0.01
        c = hexa(colorsys.hls_to_rgb(h, max(0, min(1, l)), s))
        if contraste(c, fondo) >= minimo:
            return c
    return c


def mezclar(a, b, t):
    return hexa(tuple(x + (y - x) * t for x, y in zip(rgb(a), rgb(b))))


def sobre(color, claro="#ffffff", oscuro="#16161c"):
    """Texto encima de un color (botones): el que más contraste tenga."""
    return claro if contraste(color, claro) >= contraste(color, oscuro) else oscuro


def construir(m, modo):
    f = m["fondo"]
    claro = modo == "light"
    texto = asegurar(m["texto"], f, 7.0)          # texto principal: AAA, para leer tranquilo
    texto2 = asegurar(m["texto2"], m["fondo2"], 4.5)
    pri, sec, ter, err = (asegurar(m[k], f, 4.5) for k in ("pri", "sec", "ter", "err"))
    n, b = list(m["n"]), list(m["b"])
    for lista in (n, b):
        for i in range(1, 7):                       # rojo…cian: siempre legibles como texto
            lista[i] = asegurar(lista[i], f, 4.5)
    # negro brillante = comentarios y sugerencias de la terminal (atenuado pero legible)
    b[0] = asegurar(b[0], f, 3.5)
    if claro:
        n[0] = asegurar(n[0], f, 4.5)               # en claro el "negro" es texto
    else:
        n[7], b[7] = asegurar(n[7], f, 7.0), asegurar(b[7], f, 7.0)
    seleccion = mezclar(f, pri, 0.28 if claro else 0.35)
    term = {"normal": dict(zip(ANSI, n)), "bright": dict(zip(ANSI, b)),
            "foreground": texto, "background": f, "cursor": pri if claro else texto, "cursorText": f,
            "selectionFg": asegurar(texto, seleccion, 7.0), "selectionBg": seleccion}
    return {"mPrimary": pri, "mOnPrimary": sobre(pri), "mSecondary": sec, "mOnSecondary": sobre(sec),
            "mTertiary": ter, "mOnTertiary": sobre(ter), "mError": err, "mOnError": sobre(err),
            "mSurface": f, "mOnSurface": texto, "mSurfaceVariant": m["fondo2"], "mOnSurfaceVariant": texto2,
            "mOutline": m["borde"], "mShadow": mezclar(f, "#000000", 0.3) if not claro else mezclar(f, "#000000", 0.12),
            "mHover": pri, "mOnHover": sobre(pri), "terminal": term}


def main():
    DESTINO.mkdir(parents=True, exist_ok=True)
    for clave, e in ESQUEMAS.items():
        datos = {modo: construir(e[modo], modo) for modo in ("dark", "light")}
        (DESTINO / f"{clave}.json").write_text(json.dumps(datos, indent=2) + "\n")
        for modo, d in datos.items():
            peor = min(contraste(c, d["mSurface"]) for c in list(d["terminal"]["normal"].values())[1:7])
            print(f"{e['nombre']:<14} {modo:<5} texto {contraste(d['mOnSurface'], d['mSurface']):4.1f}:1 · "
                  f"acento {contraste(d['mPrimary'], d['mSurface']):4.1f}:1 · peor color terminal {peor:3.1f}:1")


if __name__ == "__main__":
    main()
