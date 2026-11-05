"""anillo_apps.py — qué muestra el anillo radial (anillo.py) en cada programa.

Cada perfil tiene 12 sectores en sentido horario empezando ARRIBA (como un reloj: 0 = las 12, 3 = las 3,
6 = abajo, 9 = izquierda). Un sector es S(icono, nombre, acción, sub=[...], rueda=(subir, bajar), color=...):

  icono   nombre de icono Tabler (lista: /usr/share/noctalia/assets/fonts/tabler.json)
  acción  "ctrl+t" · ["ctrl+l", "alt+return"] (varias teclas seguidas) · ("cmd", [...]) lanzar ·
          ("esperar", [...]) lanzar y esperar a que termine (útil antes de pegar) · NOC("volume-up") = noctalia msg
  sub     sub-opciones: salen en un arco exterior; las eliges alejando más el mouse en esa dirección
  rueda   girar la rueda del mouse con ese sector elegido (volumen, zoom, pestañas…)
  color   opcional; si no se da, sale del TIPO de acción (ver COLOR_POR) para que sea fácil de memorizar:
          rojo = cerrar/borrar · verde = nuevo · amarillo = buscar · azul = moverse · morado = multimedia ·
          naranja = capturas · rosa = editar/formato · cian = vistas/ventanas · turquesa = el resto

El perfil se elige por la clase de la ventana con foco (regex) y, si se indica, por el título.
Con el anillo abierto, la rueda en el CENTRO siempre cambia el volumen.
"""
import os

H = os.path.expanduser("~/.config/hypr/scripts")

ROJO, NARANJA, AMARILLO = "#ff4d6d", "#ff9f43", "#ffd43b"
VERDE, TURQUESA, CIAN = "#4ade80", "#2ee6c5", "#38bdf8"
AZUL, MORADO, ROSA, BLANCO = "#6b8cff", "#b07cff", "#ff6ad5", "#e8ecf4"

# Color según el icono (primera coincidencia gana)
COLOR_POR = [
    (("x", "trash", "square-rounded-x", "eraser", "clear-all", "door-exit", "hand-stop", "lock", "logout",
      "backspace", "bell-x", "player-stop"), ROJO),
    (("plus", "message-plus", "folder-plus", "users-group", "bookmark-plus", "copy-plus"), VERDE),
    (("search", "list-search", "file-search", "filter", "zoom", "replace"), AMARILLO),
    (("player", "volume", "microphone", "music", "brand-speedtest", "gauge", "rewind", "movie", "playlist",
      "badge-cc", "video"), MORADO),
    (("camera", "screenshot", "photo", "crop"), NARANJA),
    (("bold", "italic", "strikethrough", "code", "link", "pencil", "edit", "writing", "cursor-text", "eye-off",
      "rotate", "flip", "resize", "align", "braces", "text"), ROSA),
    (("layout", "maximize", "window", "app-window", "grid", "list", "columns", "picture-in-picture", "focus",
      "eye", "sort", "browser", "arrows"), CIAN),
    (("arrow", "chevron", "corner", "home", "player-track", "history", "folder", "bookmark"), AZUL),
]


def color_de(icono):
    partes = icono.split("-")
    for claves, color in COLOR_POR:
        if any(icono == k or icono.startswith(k + "-") or k in partes for k in claves):
            return color
    return TURQUESA


def S(icono, nombre, accion=None, sub=None, rueda=None, color=None):
    return {"icono": icono, "nombre": nombre, "accion": accion, "sub": sub or [], "rueda": rueda,
            "color": color or color_de(icono)}


def NOC(*args):
    return ("cmd", ["noctalia", "msg", *args])


def SH(script, *args):
    return ("cmd", ["bash", f"{H}/{script}", *args])


# Captura de una región al portapapeles y pegarla en el chat (espera a que elijas la región)
PEGAR_CAPTURA = [("esperar", ["bash", f"{H}/captura-portapapeles.sh"]), "ctrl+v"]
VOLUMEN = (NOC("volume-up"), NOC("volume-down"))


# ---- Global: cualquier programa sin perfil propio -------------------------------------------------
GLOBAL = {
    "nombre": "Sistema", "logo": "device-desktop", "acento": "#8b9cff",
    "sectores": [
        S("volume", "Volumen", NOC("volume-mute"), rueda=VOLUMEN,
          sub=[S("microphone-off", "Silenciar micrófono", NOC("mic-mute")),
               S("volume-off", "Silenciar", NOC("volume-mute"))]),
        S("sun", "Luz nocturna", NOC("nightlight-toggle"), color=AMARILLO,
          rueda=(NOC("brightness-up"), NOC("brightness-down"))),
        S("player-play", "Play / pausa", NOC("media", "toggle"),
          rueda=(NOC("media", "next"), NOC("media", "previous")),
          sub=[S("player-track-prev", "Anterior", NOC("media", "previous"), color=MORADO),
               S("player-track-next", "Siguiente", NOC("media", "next"), color=MORADO)]),
        S("bell", "Notificaciones", NOC("panel-toggle", "control-center", "notifications"), color=AZUL,
          sub=[S("bell-off", "No molestar", NOC("notification-dnd-toggle"), color=ROJO),
               S("bell-ringing", "Abrir la última", NOC("notification-invoke-latest"), color=AZUL),
               S("clear-all", "Limpiar todas", NOC("notification-clear-history"))]),
        S("screenshot", "Captura al portapapeles", SH("captura-portapapeles.sh"),
          sub=[S("device-floppy", "Captura a carpeta", SH("captura-guardar.sh"), color=NARANJA),
               S("maximize", "Pantalla completa", NOC("screenshot-fullscreen"), color=NARANJA),
               S("pencil", "Captura y anotar", NOC("screenshot-annotate")),
               S("writing", "Dibujar en pantalla", NOC("annotate"))]),
        S("clipboard-list", "Portapapeles", NOC("panel-toggle", "clipboard")),
        S("app-window", "Cambiar ventana", NOC("window-switcher"),
          sub=[S("arrows-maximize", "Pantalla completa", "super+f"),
               S("picture-in-picture", "Flotante", "super+alt+space"),
               S("layout-columns", "Girar división", "super+j"),
               S("x", "Cerrar ventana", "super+q")]),
        S("folder", "Archivos", "super+e"),
        S("terminal-2", "Terminal", "super+return", color=TURQUESA),
        S("rocket", "Lanzador", NOC("panel-toggle", "launcher"), color=AMARILLO),
        S("moon-stars", "Modo enfoque", ("cmd", ["python3", f"{H}/modo-enfoque.py"]), color=MORADO),
        S("settings", "Centro de control", NOC("panel-toggle", "control-center"),
          sub=[S("lock", "Bloquear", NOC("session", "lock")),
               S("contrast-2", "Claro / oscuro", NOC("theme-mode-toggle"), color=BLANCO),
               S("wallpaper", "Fondo siguiente", NOC("wallpaper-next"), color=NARANJA),
               S("coffee", "Cafeína (no suspender)", NOC("caffeine-toggle"), color=AMARILLO),
               S("mouse", "Ajustes del mouse", ("cmd", ["solaar"]), color=TURQUESA)]),
    ],
}

# ---- Brave ----------------------------------------------------------------------------------------
BRAVE = {
    "nombre": "Brave", "logo": "world-www", "acento": "#fb542b",
    "sectores": [
        S("browser-plus", "Nueva pestaña", "ctrl+t", color=VERDE),
        S("arrow-right", "Pestaña siguiente", "ctrl+tab", rueda=("ctrl+shift+tab", "ctrl+tab"),
          sub=[S("arrow-left", "Pestaña anterior", "ctrl+shift+tab"),
               S("copy-plus", "Duplicar pestaña", ["ctrl+l", "alt+return"]),
               S("arrow-bar-to-down", "Última pestaña", "ctrl+9")]),
        S("refresh", "Recargar", "f5", color=TURQUESA,
          sub=[S("reload", "Recargar sin caché", "ctrl+shift+r", color=TURQUESA),
               S("hand-stop", "Detener carga", "esc")]),
        S("search", "Buscar en la página", "ctrl+f"),
        S("zoom-reset", "Zoom normal", "ctrl+0", rueda=("ctrl+equal", "ctrl+minus")),
        S("bookmark-plus", "Guardar en marcadores", "ctrl+d",
          sub=[S("bookmarks", "Marcadores", "ctrl+shift+o"),
               S("history", "Historial", "ctrl+h"),
               S("download", "Descargas", "ctrl+j", color=AZUL),
               S("printer", "Imprimir / PDF", "ctrl+p", color=BLANCO)]),
        S("x", "Cerrar pestaña", "ctrl+w"),
        S("arrow-back-up", "Reabrir pestaña", "ctrl+shift+t", color=VERDE),
        S("arrow-left", "Atrás", "alt+left",
          sub=[S("arrow-right", "Adelante", "alt+right"), S("home", "Inicio", "alt+home")]),
        S("list-search", "Buscar pestaña", "ctrl+shift+a"),
        S("link", "Barra de direcciones", "ctrl+l", color=AZUL),
        S("tools", "Herramientas", "ctrl+shift+i", color=TURQUESA,
          sub=[S("spy", "Ventana privada", "ctrl+shift+n", color=MORADO),
               S("source-code", "Ver código fuente", "ctrl+u"),
               S("eraser", "Borrar datos", "ctrl+shift+delete"),
               S("bookmarks", "Barra de marcadores", "ctrl+shift+b", color=CIAN)]),
    ],
}

# ---- YouTube (app web o pestaña de Brave) + Video Speed Controller ------------------------------------
YOUTUBE = {
    "nombre": "YouTube", "logo": "brand-youtube", "acento": "#ff2d55",
    "sectores": [
        S("player-play", "Play / pausa", "k"),
        S("rewind-forward-10", "+10 s", "l", rueda=("l", "j"), color=AZUL),
        S("brand-speedtest", "Más rápido", "d", rueda=("d", "s"),
          sub=[S("gauge", "Más lento", "s"),
               S("zoom-reset", "Velocidad normal", "r", color=MORADO),
               S("bolt", "Velocidad preferida", "g", color=AMARILLO),
               S("eye", "Mostrar control", "v")]),
        S("arrows-maximize", "Pantalla completa", "f",
          sub=[S("layout-board-split", "Modo cine", "t"),
               S("picture-in-picture", "Miniplayer", "i")]),
        S("badge-cc", "Subtítulos", "c"),
        S("player-skip-forward", "Siguiente video", "shift+n",
          sub=[S("player-skip-back", "Video anterior", "shift+p")]),
        S("rewind-backward-10", "-10 s", "j", color=AZUL),
        S("volume-off", "Silenciar", "m"),
        S("clock", "Ir a…", "0", color=AZUL,
          sub=[S("arrow-bar-to-up", "Inicio", "0", color=AZUL), S("player-track-next", "Mitad", "5", color=AZUL),
               S("arrow-bar-to-down", "90 %", "9", color=AZUL)]),
        S("search", "Buscar", "slash"),
        S("camera", "Capturas del video", SH("youtube-capturas.sh")),
        S("arrow-left", "Atrás", "alt+left"),
    ],
}

# ---- mpv (cursos) — tus atajos de ~/.config/mpv/input.conf ------------------------------------------
MPV = {
    "nombre": "mpv", "logo": "movie", "acento": "#b07cff",
    "sectores": [
        S("player-play", "Play / pausa", "space"),
        S("rewind-forward-10", "+10 s", "ctrl+right", rueda=("right", "left"), color=AZUL),
        S("brand-speedtest", "Velocidad 2x", "e", rueda=("d", "a"),
          sub=[S("gauge", "Velocidad 1.5x", "w"),
               S("arrow-up", "+0.1", "d", color=MORADO), S("arrow-down", "-0.1", "a", color=MORADO),
               S("zoom-reset", "Velocidad normal", "backspace", color=MORADO)]),
        S("arrows-maximize", "Pantalla completa", "f"),
        S("bookmark-plus", "Poner marca", "b",
          sub=[S("bookmark", "Ir a la marca", "n"),
               S("list-details", "Capítulos y marcas", "shift+c"),
               S("arrow-right", "Marca siguiente", "pageup"),
               S("arrow-left", "Marca anterior", "pagedown")]),
        S("playlist", "Lista de videos", "tab"),
        S("rewind-backward-10", "-10 s", "ctrl+left", color=AZUL),
        S("notes", "Notas", "h", color=ROSA),
        S("player-skip-forward", "Siguiente video", "shift+n",
          sub=[S("player-skip-back", "Video anterior", "shift+p")]),
        S("rewind-forward-30", "Saltos", "alt+right", color=AZUL,
          sub=[S("rewind-forward-30", "+30 s", "alt+right", color=AZUL),
               S("rewind-backward-30", "-30 s", "alt+left", color=AZUL),
               S("arrow-back-up", "Deshacer salto", "ctrl+z", color=AZUL),
               S("arrow-bar-to-up", "Al inicio", "home", color=AZUL)]),
        S("camera", "Captura", "s", rueda=("up", "down")),
        S("folder-open", "Abrir archivo", "ctrl+o"),
    ],
}

# ---- WhatsApp Web ---------------------------------------------------------------------------------
WHATSAPP = {
    "nombre": "WhatsApp", "logo": "brand-whatsapp", "acento": "#25d366",
    "sectores": [
        S("message-plus", "Nuevo chat", "ctrl+alt+n",
          sub=[S("users-group", "Nuevo grupo", "ctrl+alt+shift+n")]),
        S("arrow-down", "Chat siguiente", "ctrl+alt+shift+]",
          rueda=("ctrl+alt+shift+[", "ctrl+alt+shift+]")),
        S("pin", "Fijar chat", "ctrl+alt+shift+p", color=AMARILLO),
        S("bell-off", "Silenciar chat", "ctrl+alt+shift+m", color=MORADO),
        S("archive", "Archivar chat", "ctrl+alt+e", color=CIAN),
        S("mail-opened", "Marcar no leído", "ctrl+alt+shift+u", color=VERDE),
        S("screenshot", "Pegar captura", PEGAR_CAPTURA),
        S("brand-speedtest", "Audio más rápido", "shift+period",
          sub=[S("gauge", "Audio más lento", "shift+comma")]),
        S("arrow-up", "Chat anterior", "ctrl+alt+shift+["),
        S("search", "Buscar chats", "ctrl+alt+slash",
          sub=[S("file-search", "Buscar en este chat", "ctrl+alt+shift+f")]),
        S("x", "Cerrar chat", "esc",
          sub=[S("trash", "Eliminar chat", "ctrl+alt+backspace")]),
        S("user-circle", "Perfil", "ctrl+alt+p", color=TURQUESA,
          sub=[S("settings", "Ajustes", "ctrl+alt+comma", color=TURQUESA)]),
    ],
}

# ---- Telegram Desktop (atajos por defecto de tdesktop) -----------------------------------------------
TELEGRAM = {
    "nombre": "Telegram", "logo": "brand-telegram", "acento": "#2aabee",
    "sectores": [
        S("search", "Buscar", "ctrl+f"),
        S("arrow-down", "Chat siguiente", "alt+down", rueda=("alt+up", "alt+down")),
        S("bookmark", "Mensajes guardados", "ctrl+0", color=AMARILLO),
        S("folder", "Carpeta siguiente", "ctrl+shift+down", rueda=("ctrl+shift+up", "ctrl+shift+down"),
          sub=[S("folder", "Carpeta 1", "ctrl+1"), S("folder", "Carpeta 2", "ctrl+2"),
               S("folder", "Carpeta 3", "ctrl+3"), S("folder", "Carpeta 4", "ctrl+4")]),
        S("archive", "Archivados", "ctrl+9", color=CIAN),
        S("checks", "Marcar leído", "ctrl+r", color=VERDE),
        S("screenshot", "Pegar captura", PEGAR_CAPTURA),
        S("bold", "Formato", "ctrl+b",
          sub=[S("bold", "Negrita", "ctrl+b"), S("italic", "Cursiva", "ctrl+i"),
               S("strikethrough", "Tachado", "ctrl+shift+x"), S("code", "Código", "ctrl+shift+m"),
               S("eye-off", "Spoiler", "ctrl+shift+p"), S("link", "Enlace", "ctrl+k")]),
        S("arrow-up", "Chat anterior", "alt+up"),
        S("corner-up-left", "Responder último", "ctrl+up", color=AZUL,
          sub=[S("edit", "Editar mi último", "up")]),
        S("address-book", "Contactos", "ctrl+j", color=TURQUESA),
        S("lock", "Bloquear", "ctrl+l",
          sub=[S("window-minimize", "Minimizar", "ctrl+m", color=CIAN),
               S("x", "Cerrar ventana", "ctrl+w")]),
    ],
}

# ---- Dolphin ----------------------------------------------------------------------------------------
DOLPHIN = {
    "nombre": "Dolphin", "logo": "folder", "acento": "#1d99f3",
    "sectores": [
        S("folder-plus", "Carpeta nueva", "ctrl+shift+n"),
        S("cursor-text", "Renombrar", "f2"),
        S("layout-columns", "Dividir vista", "f3"),
        S("search", "Buscar", "ctrl+f", sub=[S("filter", "Filtrar", "ctrl+i")]),
        S("browser-plus", "Nueva pestaña", "ctrl+t", color=VERDE, rueda=("ctrl+shift+tab", "ctrl+tab"),
          sub=[S("arrow-left", "Pestaña anterior", "ctrl+shift+tab"),
               S("arrow-right", "Pestaña siguiente", "ctrl+tab"),
               S("x", "Cerrar pestaña", "ctrl+w")]),
        S("layout-grid", "Vista", "ctrl+1", rueda=("ctrl+equal", "ctrl+minus"),
          sub=[S("layout-grid", "Iconos", "ctrl+1"), S("list", "Compacta", "ctrl+2"),
               S("list-details", "Detalles", "ctrl+3"), S("eye", "Mostrar ocultos", "alt+period")]),
        S("arrow-up", "Carpeta superior", "alt+up"),
        S("arrow-left", "Atrás", "alt+left", sub=[S("arrow-right", "Adelante", "alt+right")]),
        S("sort-ascending-letters", "Ordenar por nombre", "ctrl+alt+n",
          sub=[S("sort-descending", "Ordenar por tipo", "ctrl+alt+t")]),
        S("terminal-2", "Terminal aquí", "alt+shift+f4", color=TURQUESA,
          sub=[S("terminal-2", "Panel terminal", "f4", color=TURQUESA)]),
        S("link", "Barra de direcciones", "ctrl+l", color=AZUL),
        S("trash", "A la papelera", "delete",
          sub=[S("arrow-back-up", "Deshacer", "ctrl+z"), S("copy-plus", "Duplicar", "ctrl+d"),
               S("info-circle", "Propiedades", "alt+return", color=TURQUESA)]),
    ],
}

# ---- Gwenview (fotos) — tus atajos de kxmlgui5 --------------------------------------------------------
GWENVIEW = {
    "nombre": "Fotos", "logo": "photo", "acento": "#ff6ad5",
    "sectores": [
        S("arrow-right", "Siguiente foto", "d", rueda=("a", "d")),
        S("rotate-clockwise", "Rotar derecha", "e"),
        S("crop", "Recortar", "c"),
        S("arrows-diagonal-minimize-2", "Ajustar", "w", color=CIAN,
          sub=[S("arrows-maximize", "Rellenar", "shift+w"), S("zoom-reset", "Tamaño real", "ctrl+0")]),
        S("maximize", "Pantalla completa", "f"),
        S("trash", "A la papelera", "x"),
        S("arrow-left", "Foto anterior", "a"),
        S("rotate", "Rotar izquierda", "q"),
        S("flip-vertical", "Editar", "m",
          sub=[S("flip-vertical", "Reflejar", "m"), S("resize", "Redimensionar", "r"),
               S("arrow-back-up", "Deshacer", "ctrl+z"), S("device-floppy", "Guardar", "ctrl+s", color=VERDE)]),
        S("layout-grid", "Miniaturas", "t",
          sub=[S("layout-sidebar", "Barra lateral", "i"), S("focus-2", "Modo foco", "s")]),
        S("copy", "Copiar imagen", "ctrl+c", color=TURQUESA),
        S("folder-open", "Archivo", "ctrl+alt+o",
          sub=[S("copy", "Copiar a…", "f7", color=AZUL), S("arrow-forward-up", "Mover a…", "ctrl+alt+m"),
               S("app-window", "Abrir en otra ventana", "ctrl+alt+n")]),
    ],
}

# ---- kitty (terminal) ---------------------------------------------------------------------------------
KITTY = {
    "nombre": "Terminal", "logo": "terminal-2", "acento": "#2ee6c5",
    "sectores": [
        S("browser-plus", "Nueva pestaña", "ctrl+shift+t", color=VERDE),
        S("arrow-right", "Pestaña siguiente", "ctrl+shift+right", rueda=("ctrl+shift+left", "ctrl+shift+right")),
        S("app-window", "Nueva ventana", "ctrl+shift+return", color=VERDE),
        S("copy", "Copiar", "ctrl+shift+c", color=TURQUESA),
        S("clipboard", "Pegar", "ctrl+shift+v", color=TURQUESA),
        S("text-size", "Letra normal", "ctrl+shift+backspace", color=ROSA,
          rueda=("ctrl+shift+equal", "ctrl+shift+minus"),
          sub=[S("text-increase", "Más grande", "ctrl+shift+equal"),
               S("text-decrease", "Más chica", "ctrl+shift+minus")]),
        S("x", "Cerrar pestaña", "ctrl+shift+q"),
        S("hand-stop", "Interrumpir", "ctrl+c", sub=[S("door-exit", "Salir (EOF)", "ctrl+d")]),
        S("arrow-left", "Pestaña anterior", "ctrl+shift+left"),
        S("history", "Historial", "ctrl+shift+h",
          sub=[S("arrow-up", "Arriba", "ctrl+shift+pageup"), S("arrow-down", "Abajo", "ctrl+shift+pagedown")]),
        S("clear-all", "Limpiar", "ctrl+l"),
        S("search", "Buscar comando", "ctrl+r",
          sub=[S("arrow-bar-to-up", "Inicio de línea", "ctrl+a"),
               S("arrow-bar-to-down", "Fin de línea", "ctrl+e")]),
    ],
}

# ---- VS Code ----------------------------------------------------------------------------------------
CODE = {
    "nombre": "VS Code", "logo": "brand-vscode", "acento": "#23a9f2",
    "sectores": [
        S("command", "Comandos", "ctrl+shift+p", color=AMARILLO),
        S("file-search", "Abrir archivo", "ctrl+p"),
        S("terminal-2", "Terminal", "ctrl+grave", color=TURQUESA),
        S("layout-sidebar", "Barra lateral", "ctrl+b",
          sub=[S("layout-columns", "Dividir editor", "ctrl+backslash")]),
        S("search", "Buscar en todo", "ctrl+shift+f",
          sub=[S("replace", "Reemplazar", "ctrl+h"), S("search", "Buscar aquí", "ctrl+f")]),
        S("align-justified", "Formatear", "ctrl+shift+i"),
        S("arrow-forward-up", "Ir a definición", "f12",
          sub=[S("arrow-back-up", "Volver", "ctrl+alt+minus"),
               S("sitemap", "Ir a símbolo", "ctrl+shift+o", color=AZUL)]),
        S("code", "Comentar", "ctrl+slash"),
        S("cursor-text", "Renombrar símbolo", "f2"),
        S("device-floppy", "Guardar", "ctrl+s", color=VERDE),
        S("x", "Cerrar editor", "ctrl+w", sub=[S("arrow-back-up", "Reabrir", "ctrl+shift+t", color=VERDE)]),
        S("arrow-down", "Mover línea abajo", "alt+down", rueda=("alt+up", "alt+down"),
          sub=[S("arrow-up", "Mover línea arriba", "alt+up"),
               S("copy-plus", "Duplicar línea", "shift+alt+down")]),
    ],
}

# Orden = prioridad (el primero que coincide gana). titulo es opcional.
PERFILES = [
    {"clase": r"^brave-www\.youtube\.com__", **YOUTUBE},
    {"clase": r"^brave-browser$", "titulo": r"YouTube", **YOUTUBE},
    {"clase": r"^brave-web\.whatsapp\.com__", **WHATSAPP},
    {"clase": r"^(org\.telegram\.desktop|brave-web\.telegram\.org__.*)$", **TELEGRAM},
    {"clase": r"^brave-browser$", **BRAVE},
    {"clase": r"^mpv$", **MPV},
    {"clase": r"^org\.kde\.dolphin$", **DOLPHIN},
    {"clase": r"^org\.kde\.gwenview$", **GWENVIEW},
    {"clase": r"^kitty$", **KITTY},
    {"clase": r"^(code|Code|code-oss)$", **CODE},
]


def perfil_para(clase, titulo=""):
    import re
    for p in PERFILES:
        if re.search(p["clase"], clase or "") and (not p.get("titulo") or re.search(p["titulo"], titulo or "")):
            return p
    return GLOBAL
