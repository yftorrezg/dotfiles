#!/usr/bin/env python3
"""atajos-doc.py — genera las hojas de atajos de Hyprland a partir de los binds REALES.

Lee config/binds.lua y config/binds_equipo.lua (cada línea  hl.bind("SUPER + X", ...)  ) y escribe:
    chuletas/26-hyprland-atajos.md   ventanas, escritorios, apps, sistema, mouse, hardware
    chuletas/27-estudio-atajos.md    cursos, capturas, voz, traductor, descargas, anillo
    (y una copia en ~/Documentos/, como mx-doc.py)

Así no se desactualiza: cambias un atajo en binds.lua, ejecutas este script y la hoja se actualiza.
  python3 atajos-doc.py            regenera las hojas
  python3 atajos-doc.py --revisar  solo muestra qué atajos no tienen nombre/grupo (no escribe nada)

Si aparece un atajo nuevo sin entrada en NOMBRES, el script AVISA y lo deja en «Sin clasificar»
con el comentario del código. Solo tienes que añadir una línea a NOMBRES.

Los binds generados en bucle (SUPER+1..0, SUPER+CTRL+1..0, teclas del mouse code:192..202) no son
literales, así que se listan a mano en BUCLES (abajo).
"""
import os
import re
import sys

HOME = os.path.expanduser("~")
HYPR = os.path.join(HOME, ".config", "hypr")
FUENTES = [os.path.join(HYPR, "config", "binds.lua"), os.path.join(HYPR, "config", "binds_equipo.lua")]
CHULETAS = os.path.join(HYPR, "chuletas")
COPIAS = [os.path.join(HOME, "Documentos", "26-hyprland-atajos.md"),
          os.path.join(HOME, "Documentos", "27-estudio-atajos.md")]

# hl.bind(mainMod .. " + X", ...)   o   hl.bind("CONTROL + X", ...)
BIND = re.compile(r'^\s*hl\.bind\(\s*(mainMod\s*\.\.\s*)?"([^"]*)"\s*,')

H = "🪟 Ventanas"
F = "🧭 Foco y escritorios"
A = "🚀 Abrir apps"
S = "🎨 Sistema y pantalla"
M = "🖱️ Mouse y hardware"
E = "🎓 Estudio y cursos"
C = "📸 Capturas"
V = "🗣️ Voz, traducción y resumen"
D = "📥 Descargas, repos y anillo"
X = "❓ Sin clasificar"

# combo (tal como sale en binds.lua, con SUPER delante cuando usa mainMod) -> (hoja, grupo, qué hace, mnemotecnia)
NOMBRES = {
    # --- ventanas ---
    "SUPER + Q": ("26", H, "Cerrar la ventana enfocada", "Q = Quit"),
    "SUPER + ALT + Space": ("26", H, "Ventana flotante (alternar)", "Space = la barra espaciadora"),
    "SUPER + F": ("26", H, "Pantalla completa de la ventana", "F = Full"),
    "SUPER + J": ("26", H, "Alternar división de la ventana (split)", "J = (sin mnemotecnia; solo se acuerda)"),
    "ALT + Tab": ("26", H, "Ciclar entre ventanas", "Tab = siguiente"),
    "SUPER + mouse:272": ("26", H, "Arrastrar ventana con el mouse (mantén y mueve)", "Clic izq. = mover"),
    "SUPER + mouse:273": ("26", H, "Redimensionar ventana con el mouse", "Clic der. = tamaño"),
    "SUPER + Minus": ("26", H, "Zoom de la pantalla (alejar)", "− = menos"),
    "SUPER + Plus": ("26", H, "Zoom de la pantalla (acercar)", "+ = más"),
    # --- foco y escritorios ---
    "SUPER + Left": ("26", F, "Enfocar la ventana a la izquierda", "Flechas = dirección"),
    "SUPER + Right": ("26", F, "Enfocar la ventana a la derecha", "Flechas = dirección"),
    "SUPER + Up": ("26", F, "Enfocar la ventana de arriba", "Flechas = dirección"),
    "SUPER + Down": ("26", F, "Enfocar la ventana de abajo", "Flechas = dirección"),
    "SUPER + SHIFT + Up": ("26", F, "Mover la ventana hacia arriba", "SHIFT = mover ventana"),
    "SUPER + SHIFT + Down": ("26", F, "Mover la ventana hacia abajo", "SHIFT = mover ventana"),
    "SUPER + SHIFT + Left": ("26", F, "Mover la ventana a la izquierda", "SHIFT = mover ventana"),
    "SUPER + SHIFT + Right": ("26", F, "Mover la ventana a la derecha", "SHIFT = mover ventana"),
    "SUPER + CONTROL + SHIFT + Right": ("26", F, "Mandar la ventana al escritorio siguiente del monitor", "CTRL+SHIFT = mover de escritorio"),
    "SUPER + CONTROL + SHIFT + Left": ("26", F, "Mandar la ventana al escritorio anterior del monitor", "CTRL+SHIFT = mover de escritorio"),
    "SUPER + CONTROL + Right": ("26", F, "Escritorio virtual siguiente (todos los monitores)", "CTRL + flechas = cambiar escritorio"),
    "SUPER + CONTROL + Left": ("26", F, "Escritorio virtual anterior (todos los monitores)", "CTRL + flechas = cambiar escritorio"),
    "SUPER + Tab": ("26", F, "Ciclar ventanas del escritorio virtual actual", "Tab = siguiente ventana"),
    "SUPER + ALT + 1": ("26", F, "Enfocar el monitor 1", "ALT + número = monitor"),
    "SUPER + ALT + 2": ("26", F, "Enfocar el monitor 2", "ALT + número = monitor"),
    "SUPER + SHIFT + 1": ("26", F, "Mandar la ventana al monitor 1", "SHIFT + número = mandar ventana"),
    "SUPER + SHIFT + 2": ("26", F, "Mandar la ventana al monitor 2", "SHIFT + número = mandar ventana"),
    "SUPER + S": ("26", F, "Mostrar/ocultar el escritorio especial (scratchpad)", "S = Scratchpad"),
    "SUPER + mouse_down": ("26", F, "Escritorio anterior con la rueda", "Rueda = escritorios"),
    "SUPER + mouse_up": ("26", F, "Escritorio siguiente con la rueda", "Rueda = escritorios"),
    # --- abrir apps ---
    "SUPER + Return": ("26", A, "Terminal (kitty)", "Return = Enter, abre terminal"),
    "SUPER + E": ("26", A, "Explorador de archivos (Dolphin)", "E = Explorador"),
    "SUPER + W": ("26", A, "Navegador (Brave)", "W = Web"),
    "SUPER + N": ("26", A, "Obsidian (notas)", "N = Notas"),
    "XF86Calculator": ("26", A, "Calculadora (tecla física)", "Tecla de calculadora del teclado"),
    "SUPER + G": ("26", A, "VS Code (escritorio fijo de código)", "G = Código"),
    "SUPER + T": ("26", A, "TikTok (escritorio fijo)", "T = TikTok"),
    "SUPER + ALT + Q": ("26", A, "YouTube (enfocar o abrir)", "ALT + Q = YouTube (Q no tiene relación)"),
    "SUPER + ALT + W": ("26", A, "WhatsApp Web (enfocar o abrir)", "W = WhatsApp"),
    "SUPER + ALT + T": ("26", A, "Telegram (enfocar o abrir)", "T = Telegram"),
    "SUPER + ALT + F": ("26", A, "Facebook (enfocar o abrir)", "F = Facebook"),
    "SUPER + ALT + I": ("26", A, "Instagram (enfocar o abrir)", "I = Instagram"),
    "SUPER + ALT + D": ("26", A, "Google Drive (enfocar o abrir)", "D = Drive"),
    "SUPER + ALT + E": ("26", A, "Ir al escritorio «estudio» (nombrado)", "E = Estudio"),
    "SUPER + V": ("26", A, "Panel del portapapeles (historial)", "V = Ver el portapapeles"),
    "SUPER + A": ("26", A, "Panel de notificaciones", "A = Avisos"),
    "SUPER + X": ("26", A, "Centro de control (sonido, red, etc.)", "X = eXtra/Control"),
    "SUPER + Z": ("26", A, "Ajustes de Noctalia", "Z = Zona de ajustes"),
    "SUPER + Super_L": ("26", A, "Buscador / lanzador (tocar SUPER solo y soltar)", "Solo SUPER = buscar"),
    "SUPER + period": ("26", A, "Lanzador en la pestaña de emojis", ". = emojis"),
    "SUPER + K": ("26", A, "Stream Deck (OpenDeck): abrir la ventana de configuración", "K = Keypad (teclado de deck)"),
    "SUPER + C": ("26", A, "Abrir el curso y los apuntes de la sesión de estudio", "C = Curso (ver hoja 27)"),
    "SUPER + ALT + C": ("26", A, "Configurar links del curso", "ALT + C = Configurar curso"),
    "CONTROL + SHIFT + Escape": ("26", A, "Monitor de procesos (btop)", "Ctrl+Shift+Esc = ver procesos"),
    "CONTROL + ALT + Escape": ("26", A, "Matar LibreOffice colgado (un paso)", "Ctrl+Alt+Esc = matar colgado"),
    # --- sistema y pantalla ---
    "SUPER + L": ("26", S, "Bloquear la sesión", "L = Lock"),
    "SUPER + SHIFT + D": ("26", S, "Cambiar modo claro / oscuro", "SHIFT + D = Dark"),
    "SUPER + SHIFT + A": ("26", S, "Selector de estilos (temas, fondos, colores)", "SHIFT + A = Apariencia"),
    "SUPER + SHIFT + C": ("26", S, "Abrir las chuletas (esta ventana)", "SHIFT + C = Chuletas"),
    "SUPER + SHIFT + W": ("26", S, "Editar/mover los widgets del escritorio con el mouse", "SHIFT + W = Widgets"),
    "SUPER + ALT + N": ("26", S, "Modo enfoque (todo negro, sin barra ni widgets)", "N = eNfoque"),
    "SUPER + ALT + O": ("27", D, "Anillo radial: mantén y elige (al soltar ejecuta)", "O = anillO"),
    "Print": ("26", S, "Captura de región (Noctalia)", "Print = Impr Pant"),
    "SUPER + Print": ("26", S, "Captura de pantalla completa (Noctalia)", "SUPER + Print = todo"),
    # --- hardware ---
    "XF86AudioRaiseVolume": ("26", M, "Subir volumen", "Tecla física"),
    "XF86AudioLowerVolume": ("26", M, "Bajar volumen", "Tecla física"),
    "XF86AudioMute": ("26", M, "Silenciar", "Tecla física"),
    "XF86AudioMicMute": ("26", M, "Silenciar micrófono", "Tecla física"),
    "XF86AudioPlay": ("26", M, "Reproducir / pausar", "Tecla física ▶"),
    "XF86AudioPause": ("26", M, "Reproducir / pausar", "Tecla física ⏸"),
    "XF86AudioNext": ("26", M, "Pista siguiente", "Tecla física ⏭"),
    "XF86AudioPrev": ("26", M, "Pista anterior", "Tecla física ⏮"),
    "XF86MonBrightnessUp": ("26", M, "Subir brillo", "Tecla física"),
    "XF86MonBrightnessDown": ("26", M, "Bajar brillo", "Tecla física"),
    "code:192": ("26", M, "Mouse Scimitar botón 2 → escritorio 2 fijo", "Teclas F14… del keyd (ver hoja 33)"),
    "code:193": ("26", M, "Mouse Scimitar botón 3 → escritorio 3 fijo", "Teclas F15… del keyd (ver hoja 33)"),
    "code:195": ("26", M, "Mouse Scimitar botón 5 → escritorio 4 fijo", "Teclas F17… del keyd (ver hoja 33)"),
    "code:196": ("26", M, "Mouse Scimitar botón 6 → escritorio 5 fijo", "Teclas F18… del keyd (ver hoja 33)"),
    "code:197": ("26", M, "Mouse Scimitar botón 7 (acción de la capa actual)", "Capa M1/M2/M3 (ver hoja 33)"),
    "code:198": ("26", M, "Mouse Scimitar botón 8 (acción de la capa actual)", "Capa M1/M2/M3 (ver hoja 33)"),
    "code:199": ("26", M, "Mouse Scimitar botón 9 (acción de la capa actual)", "Capa M1/M2/M3 (ver hoja 33)"),
    "code:200": ("26", M, "Mouse Scimitar botón 10 → capa M1", "Capa M1 (ver hoja 33)"),
    "code:201": ("26", M, "Mouse Scimitar botón 11 → capa M2", "Capa M2 (ver hoja 33)"),
    "code:202": ("26", M, "Mouse Scimitar botón 12 → capa M3", "Capa M3 (ver hoja 33)"),
    # --- estudio y cursos ---
    "SUPER + I": ("27", E, "Centro de estudio: abre la próxima clase (pre-test, apuntes, práctica, tests)", "I = Ir a clase"),
    "SUPER + ALT + V": ("27", E, "Verificar (correr) los tests de la práctica de la clase actual", "V = Verificar"),
    "SUPER + ALT + A": ("27", E, "Elegir la carpeta de un curso: capturas + apuntes de todas las clases", "A = Apuntes de todo el curso"),
    "SUPER + ALT + P": ("27", E, "Retomar apuntes tras reiniciar (las clases hechas se saltan)", "P = Pendientes / Proseguir"),
    "SUPER + ALT + S": ("27", C, "Auto-captura: activar/desactivar (captura al ver la clase)", "S = Screenshots automáticas"),
    "SUPER + ALT + Y": ("27", C, "Capturas de un video de YouTube", "Y = YouTube"),
    "CONTROL + SHIFT + D": ("27", C, "Elegir la carpeta donde se guardan las capturas", "D = Dónde"),
    "CONTROL + SHIFT + S": ("27", C, "Captura y guardarla en archivo", "S = Save (guardar)"),
    "SUPER + SHIFT + S": ("27", C, "Captura de región solo al portapapeles (sin archivo)", "SHIFT + S = Screenshot (como en Windows)"),
    # --- voz, traducción, resumen ---
    "SUPER + R": ("27", V, "Leer en voz alta el texto seleccionado (otra vez = parar)", "R = Read (leer)"),
    "SUPER + ALT + R": ("27", V, "Elegir la voz (edge-tts online o Piper offline)", "ALT + R = voz de Read"),
    "SUPER + SHIFT + T": ("27", V, "Traductor flotante EN/ES de la selección", "SHIFT + T = Traducir"),
    "SUPER + SHIFT + R": ("27", V, "Resumir la selección", "SHIFT + R = Resumir"),
    "SUPER + SHIFT + mouse:273": ("27", V, "Menú de resumen con clic derecho (con SUPER+SHIFT)", "SHIFT + clic der. = menú de resumir"),
    # --- descargas, repos, anillo ---
    "SUPER + D": ("27", D, "Menú de descargas (link copiado → video, 720p, MP3, lista)", "D = Descargar"),
    "SUPER + ALT + G": ("27", D, "Link de GitHub → carpeta con imágenes del código (sin IA)", "G = código (GitHub)"),
}

# Binds que se generan en bucle (no son literales en el código): se listan aquí a mano.
BUCLES = {
    "26": [
        ("SUPER + 1 … 0", F, "Escritorio virtual 1…10 (todos los monitores a la vez)", "Número = escritorio"),
        ("SUPER + CONTROL + 1 … 0", F, "Mandar la ventana enfocada al escritorio N (mismo monitor)", "CTRL + número = mandar a N"),
    ],
}

GRUPOS = {
    "26": [H, F, A, S, M, X],
    "27": [E, C, V, D, X],
}

TITULOS = {
    "26": ("🪟 Hyprland · Ventanas, escritorios y apps",
           "Todos los atajos del escritorio, leídos de binds.lua. Se regenera sola con scripts/atajos-doc.py."),
    "27": ("🎓 Estudio · Cursos, capturas, voz y descargas",
           "Los atajos que usas para estudiar: cursos, capturas automáticas, leer en voz alta, traducir y descargar."),
}

ARCHIVOS = {
    "26": "26-hyprland-atajos.md",
    "27": "27-estudio-atajos.md",
}


def leer_binds():
    """Devuelve [(combo, comentario_del_codigo)] de todos los hl.bind literales, sin repetir."""
    vistos, salida = set(), []
    for ruta in FUENTES:
        with open(ruta, encoding="utf-8") as f:
            for linea in f:
                m = BIND.match(linea)
                if not m:
                    continue
                prefijo, texto = m.group(1), m.group(2)
                combo = (("SUPER" + texto) if prefijo else texto).strip()
                combo = re.sub(r"\s+", " ", combo)
                if combo in vistos:
                    continue
                vistos.add(combo)
                comentario = ""
                if "--" in linea:
                    comentario = linea.split("--", 1)[1].strip()
                salida.append((combo, comentario))
    return salida


def escapar(texto):
    return texto.replace("|", "\\|")


def construir(hoja, binds):
    titulo, subtitulo = TITULOS[hoja]
    sin_clasificar = []
    por_grupo = {g: [] for g in GRUPOS[hoja]}

    for combo, comentario in binds:
        if combo in NOMBRES:
            h, grupo, que, mnemo = NOMBRES[combo]
            if h != hoja:
                continue
        else:
            if hoja != "26":
                continue
            grupo, que, mnemo = X, (comentario or "¡sin nombre! añádelo a NOMBRES"), "—"
            sin_clasificar.append(combo)
        por_grupo.setdefault(grupo, []).append((combo, que, mnemo))

    for combo, grupo, que, mnemo in BUCLES.get(hoja, []):
        por_grupo.setdefault(grupo, []).append((combo, que, mnemo))

    out = [f"# {titulo}", "", f"> {subtitulo}", ""]
    out += ["## 🧭 Cómo leer las teclas", "",
            "- `SUPER` = sistema (ventanas, escritorios, apps). `SUPER + ALT` = apps web y estudio.",
            "- `SUPER + SHIFT` = acciones sobre la ventana o la selección. `SUPER + CTRL` = escritorios.",
            "- 💡 Consejo: si no recuerdas un atajo, búscalo por la letra: casi todos usan la inicial de lo que hacen.",
            ""]
    for grupo in GRUPOS[hoja]:
        filas = por_grupo.get(grupo, [])
        if not filas:
            continue
        out += [f"## {grupo}", "", "| Atajo | Qué hace | Mnemotecnia |", "|---|---|---|"]
        for combo, que, mnemo in filas:
            out.append(f"| `{escapar(combo)}` | {escapar(que)} | {escapar(mnemo)} |")
        out.append("")
    return "\n".join(out).rstrip() + "\n", sin_clasificar


def main():
    revisar = "--revisar" in sys.argv
    binds = leer_binds()
    print(f"binds literales leídos: {len(binds)} (de {len(FUENTES)} archivos)")
    # Atajos que están en NOMBRES pero ya no existen en el código
    existen = {c for c, _ in binds}
    for combo in NOMBRES:
        if combo not in existen:
            print(f"  aviso: en NOMBRES pero no está en binds.lua: {combo}")

    if revisar:
        for combo, _ in binds:
            if combo not in NOMBRES:
                print(f"  sin nombre: {combo}")
        return 0

    for hoja in ("26", "27"):
        texto, sin = construir(hoja, binds)
        if sin:
            for c in sin:
                print(f"  ⚠ sin nombre (queda en 'Sin clasificar'): {c}")
        ruta = os.path.join(CHULETAS, ARCHIVOS[hoja])
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(texto)
        print("escrito:", ruta)
        copia = COPIAS[int(hoja) - 26]
        if os.path.isdir(os.path.dirname(copia)):
            with open(copia, "w", encoding="utf-8") as f:
                f.write(texto)
    return 0


if __name__ == "__main__":
    sys.exit(main())
