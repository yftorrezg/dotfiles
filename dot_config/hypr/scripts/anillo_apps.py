"""anillo_apps.py — qué muestra el anillo radial (anillo.py) en cada programa.

Cada perfil tiene 12 sectores en sentido horario empezando ARRIBA (como las horas del reloj: 0 = 12 en punto,
3 = las 3, 6 = abajo, 9 = izquierda). Un sector es S(icono, nombre, acción, sub=[...], rueda=(subir, bajar)):

  icono   nombre de icono simbólico (Papirus/Adwaita, sin "-symbolic")
  acción  "ctrl+t" · ["ctrl+l", "alt+return"] (varias teclas seguidas) · ("cmd", [...]) lanzar ·
          ("esperar", [...]) lanzar y esperar a que termine (útil antes de pegar) · NOC("volume-up") = noctalia msg
  sub     sub-opciones: salen en un arco exterior; las eliges alejando más el mouse en esa dirección
  rueda   girar la rueda del mouse con ese sector elegido (ej. volumen, zoom, pestañas)

El perfil se elige por la clase de la ventana con foco (regex) y, si se indica, por el título.
Con el anillo abierto, la rueda en el CENTRO siempre cambia el volumen.
"""
import os

H = os.path.expanduser("~/.config/hypr/scripts")


def S(icono, nombre, accion=None, sub=None, rueda=None):
    return {"icono": icono, "nombre": nombre, "accion": accion, "sub": sub or [], "rueda": rueda}


def NOC(*args):
    return ("cmd", ["noctalia", "msg", *args])


def SH(script, *args):
    return ("cmd", ["bash", f"{H}/{script}", *args])


# Captura de una región al portapapeles y pegarla en el chat (espera a que elijas la región)
PEGAR_CAPTURA = [("esperar", ["bash", f"{H}/captura-portapapeles.sh"]), "ctrl+v"]

VOLUMEN = (NOC("volume-up"), NOC("volume-down"))


# ---- Global: cualquier programa sin perfil propio -------------------------------------------------
GLOBAL = {
    "nombre": "Sistema", "tono": 250,
    "sectores": [
        S("audio-volume-high", "Volumen", NOC("volume-mute"), rueda=VOLUMEN,
          sub=[S("audio-input-microphone-muted", "Silenciar micrófono", NOC("mic-mute")),
               S("audio-volume-muted", "Silenciar", NOC("volume-mute"))]),
        S("display-brightness", "Luz nocturna", NOC("nightlight-toggle"),
          rueda=(NOC("brightness-up"), NOC("brightness-down"))),
        S("media-playback-start", "Play / pausa", NOC("media", "toggle"),
          rueda=(NOC("media", "next"), NOC("media", "previous")),
          sub=[S("media-skip-backward", "Anterior", NOC("media", "previous")),
               S("media-skip-forward", "Siguiente", NOC("media", "next"))]),
        S("notification-active", "Notificaciones", NOC("panel-toggle", "control-center", "notifications"),
          sub=[S("notification-disabled", "No molestar", NOC("notification-dnd-toggle")),
               S("mail-reply-sender", "Abrir la última", NOC("notification-invoke-latest")),
               S("edit-clear-all", "Limpiar todas", NOC("notification-clear-history"))]),
        S("accessories-screenshot", "Captura al portapapeles", SH("captura-portapapeles.sh"),
          sub=[S("document-save", "Captura a carpeta", SH("captura-guardar.sh")),
               S("view-fullscreen", "Pantalla completa", NOC("screenshot-fullscreen")),
               S("document-edit", "Captura y anotar", NOC("screenshot-annotate")),
               S("edit-select-all", "Dibujar en pantalla", NOC("annotate"))]),
        S("edit-paste", "Portapapeles", NOC("panel-toggle", "clipboard")),
        S("focus-windows", "Cambiar ventana", NOC("window-switcher"),
          sub=[S("view-fullscreen", "Pantalla completa", "super+f"),
               S("window-restore", "Flotante", "super+alt+space"),
               S("view-dual", "Girar división", "super+j"),
               S("window-close", "Cerrar ventana", "super+q")]),
        S("system-file-manager", "Archivos", "super+e"),
        S("utilities-terminal", "Terminal", "super+return"),
        S("system-search", "Lanzador", NOC("panel-toggle", "launcher")),
        S("weather-clear-night", "Modo enfoque", ("cmd", ["python3", f"{H}/modo-enfoque.py"])),
        S("lucide-settings", "Centro de control", NOC("panel-toggle", "control-center"),
          sub=[S("system-lock-screen", "Bloquear", NOC("session", "lock")),
               S("weather-clear", "Claro / oscuro", NOC("theme-mode-toggle")),
               S("preferences-desktop-wallpaper", "Fondo siguiente", NOC("wallpaper-next")),
               S("feather-zap", "Cafeína (no suspender)", NOC("caffeine-toggle")),
               S("input-mouse", "Ajustes del mouse", ("cmd", ["solaar"]))]),
    ],
}

# ---- Brave ----------------------------------------------------------------------------------------
BRAVE = {
    "nombre": "Brave", "tono": 18,
    "sectores": [
        S("tab-new", "Nueva pestaña", "ctrl+t"),
        S("go-next", "Pestaña siguiente", "ctrl+tab", rueda=("ctrl+shift+tab", "ctrl+tab"),
          sub=[S("go-previous", "Pestaña anterior", "ctrl+shift+tab"),
               S("edit-copy", "Duplicar pestaña", ["ctrl+l", "alt+return"]),
               S("go-last", "Última pestaña", "ctrl+9"),
               S("window-new", "Pestaña a ventana nueva", None)]),
        S("view-refresh", "Recargar", "f5",
          sub=[S("view-refresh", "Recargar sin caché", "ctrl+shift+r"),
               S("process-stop", "Detener carga", "esc")]),
        S("edit-find", "Buscar en la página", "ctrl+f"),
        S("zoom-in", "Zoom normal", "ctrl+0", rueda=("ctrl+equal", "ctrl+minus")),
        S("document-save", "Guardar y ver", "ctrl+d",
          sub=[S("bookmarks", "Marcadores", "ctrl+shift+o"),
               S("document-open-recent", "Historial", "ctrl+h"),
               S("folder-download", "Descargas", "ctrl+j"),
               S("document-print", "Imprimir / PDF", "ctrl+p")]),
        S("window-close", "Cerrar pestaña", "ctrl+w"),
        S("edit-undo", "Reabrir pestaña", "ctrl+shift+t"),
        S("go-previous", "Atrás", "alt+left", sub=[S("go-next", "Adelante", "alt+right"),
                                                   S("go-home", "Inicio", "alt+home")]),
        S("system-search", "Buscar pestaña", "ctrl+shift+a"),
        S("view-reveal", "Barra de direcciones", "ctrl+l"),
        S("lucide-wrench", "Herramientas", "ctrl+shift+i",
          sub=[S("feather-eye-off", "Ventana privada", "ctrl+shift+n"),
               S("text-x-generic", "Ver código fuente", "ctrl+u"),
               S("edit-clear-all", "Borrar datos", "ctrl+shift+delete"),
               S("bookmark-new", "Barra de marcadores", "ctrl+shift+b")]),
    ],
}
# "Pestaña a ventana nueva" no tiene atajo en Chromium: se quita para no dejar un botón muerto
BRAVE["sectores"][1]["sub"] = [s for s in BRAVE["sectores"][1]["sub"] if s["accion"]]

# ---- YouTube (app web o pestaña de Brave) + Video Speed Controller ------------------------------------
YOUTUBE = {
    "nombre": "YouTube", "tono": 0,
    "sectores": [
        S("media-playback-start", "Play / pausa", "k"),
        S("media-seek-forward", "+10 s", "l", rueda=("l", "j")),
        S("speedometer", "Más rápido", "d", rueda=("d", "s"),
          sub=[S("media-seek-backward", "Más lento", "s"),
               S("zoom-original", "Velocidad normal", "r"),
               S("feather-zap", "Velocidad preferida", "g"),
               S("feather-eye", "Mostrar control", "v")]),
        S("view-fullscreen", "Pantalla completa", "f",
          sub=[S("view-dual", "Modo cine", "t"),
               S("window-restore", "Miniplayer", "i")]),
        S("media-view-subtitles", "Subtítulos", "c"),
        S("media-skip-forward", "Siguiente video", "shift+n",
          sub=[S("media-skip-backward", "Video anterior", "shift+p")]),
        S("media-seek-backward", "-10 s", "j"),
        S("audio-volume-muted", "Silenciar", "m"),
        S("go-first", "Ir a…", "0",
          sub=[S("go-first", "Inicio", "0"), S("go-jump", "Mitad", "5"),
               S("go-last", "90 %", "9")]),
        S("system-search", "Buscar", "slash"),
        S("camera-photo", "Capturas del video", SH("youtube-capturas.sh")),
        S("go-previous", "Atrás", "alt+left"),
    ],
}

# ---- mpv (cursos) — tus atajos de ~/.config/mpv/input.conf ------------------------------------------
MPV = {
    "nombre": "mpv", "tono": 285,
    "sectores": [
        S("media-playback-start", "Play / pausa", "space"),
        S("media-seek-forward", "+10 s", "ctrl+right", rueda=("right", "left")),
        S("speedometer", "Velocidad 2x", "e", rueda=("d", "a"),
          sub=[S("speedometer", "Velocidad 1.5x", "w"),
               S("go-up", "+0.1", "d"), S("go-down", "-0.1", "a"),
               S("zoom-original", "Velocidad normal", "backspace")]),
        S("view-fullscreen", "Pantalla completa", "f"),
        S("view-pin", "Poner marca", "b",
          sub=[S("go-jump", "Ir a la marca", "n"),
               S("view-list", "Capítulos y marcas", "shift+c"),
               S("go-next", "Marca siguiente", "pageup"),
               S("go-previous", "Marca anterior", "pagedown")]),
        S("view-list", "Lista de videos", "tab"),
        S("media-seek-backward", "-10 s", "ctrl+left"),
        S("document-edit", "Notas", "h"),
        S("media-skip-forward", "Siguiente video", "shift+n",
          sub=[S("media-skip-backward", "Video anterior", "shift+p")]),
        S("go-jump", "Saltos", "alt+right",
          sub=[S("go-next", "+30 s", "alt+right"), S("go-previous", "-30 s", "alt+left"),
               S("edit-undo", "Deshacer salto", "ctrl+z"), S("go-first", "Al inicio", "home")]),
        S("camera-photo", "Captura", "s", rueda=("up", "down")),
        S("document-open", "Abrir archivo", "ctrl+o"),
    ],
}

# ---- WhatsApp Web ---------------------------------------------------------------------------------
WHATSAPP = {
    "nombre": "WhatsApp", "tono": 140,
    "sectores": [
        S("chat-message-new", "Nuevo chat", "ctrl+alt+n",
          sub=[S("feather-users", "Nuevo grupo", "ctrl+alt+shift+n")]),
        S("go-down", "Chat siguiente", "ctrl+alt+shift+]",
          rueda=("ctrl+alt+shift+[", "ctrl+alt+shift+]")),
        S("view-pin", "Fijar chat", "ctrl+alt+shift+p"),
        S("audio-volume-muted", "Silenciar chat", "ctrl+alt+shift+m"),
        S("mail-archive", "Archivar chat", "ctrl+alt+e"),
        S("mail-unread", "Marcar no leído", "ctrl+alt+shift+u"),
        S("accessories-screenshot", "Pegar captura", PEGAR_CAPTURA),
        S("speedometer", "Audio más rápido", "shift+period",
          sub=[S("media-seek-backward", "Audio más lento", "shift+comma")]),
        S("go-up", "Chat anterior", "ctrl+alt+shift+["),
        S("system-search", "Buscar chats", "ctrl+alt+slash",
          sub=[S("edit-find", "Buscar en este chat", "ctrl+alt+shift+f")]),
        S("window-close", "Cerrar chat", "esc",
          sub=[S("user-trash", "Eliminar chat", "ctrl+alt+backspace")]),
        S("lucide-user-cog", "Perfil", "ctrl+alt+p",
          sub=[S("lucide-settings", "Ajustes", "ctrl+alt+comma")]),
    ],
}

# ---- Telegram Desktop (atajos por defecto de tdesktop) -----------------------------------------------
TELEGRAM = {
    "nombre": "Telegram", "tono": 205,
    "sectores": [
        S("system-search", "Buscar", "ctrl+f"),
        S("go-down", "Chat siguiente", "alt+down", rueda=("alt+up", "alt+down")),
        S("bookmarks", "Mensajes guardados", "ctrl+0"),
        S("folder", "Carpeta siguiente", "ctrl+shift+down", rueda=("ctrl+shift+up", "ctrl+shift+down"),
          sub=[S("go-first", "Carpeta 1", "ctrl+1"), S("go-previous", "Carpeta 2", "ctrl+2"),
               S("go-next", "Carpeta 3", "ctrl+3"), S("go-last", "Carpeta 4", "ctrl+4")]),
        S("mail-archive", "Archivados", "ctrl+9"),
        S("feather-check-double", "Marcar leído", "ctrl+r"),
        S("accessories-screenshot", "Pegar captura", PEGAR_CAPTURA),
        S("format-text-bold", "Formato", "ctrl+b",
          sub=[S("format-text-bold", "Negrita", "ctrl+b"), S("format-text-italic", "Cursiva", "ctrl+i"),
               S("format-text-strikethrough", "Tachado", "ctrl+shift+x"),
               S("text-x-generic", "Código", "ctrl+shift+m"),
               S("feather-eye-off", "Spoiler", "ctrl+shift+p"),
               S("insert-link", "Enlace", "ctrl+k")]),
        S("go-up", "Chat anterior", "alt+up"),
        S("lucide-reply", "Responder último", "ctrl+up",
          sub=[S("document-edit", "Editar mi último", "up")]),
        S("gnome-contacts", "Contactos", "ctrl+j"),
        S("feather-lock", "Bloquear", "ctrl+l",
          sub=[S("window-minimize", "Minimizar", "ctrl+m"),
               S("window-close", "Cerrar ventana", "ctrl+w")]),
    ],
}

# ---- Dolphin ----------------------------------------------------------------------------------------
DOLPHIN = {
    "nombre": "Dolphin", "tono": 215,
    "sectores": [
        S("folder-new", "Carpeta nueva", "ctrl+shift+n"),
        S("document-edit", "Renombrar", "f2"),
        S("view-dual", "Dividir vista", "f3"),
        S("edit-find", "Buscar", "ctrl+f", sub=[S("feather-filter", "Filtrar", "ctrl+i")]),
        S("tab-new", "Nueva pestaña", "ctrl+t", rueda=("ctrl+shift+tab", "ctrl+tab"),
          sub=[S("go-previous", "Pestaña anterior", "ctrl+shift+tab"),
               S("go-next", "Pestaña siguiente", "ctrl+tab"),
               S("window-close", "Cerrar pestaña", "ctrl+w")]),
        S("view-grid", "Vista", "ctrl+1", rueda=("ctrl+equal", "ctrl+minus"),
          sub=[S("view-grid", "Iconos", "ctrl+1"), S("view-list", "Compacta", "ctrl+2"),
               S("view-column", "Detalles", "ctrl+3"),
               S("view-reveal", "Mostrar ocultos", "alt+period")]),
        S("go-up", "Carpeta superior", "alt+up"),
        S("go-previous", "Atrás", "alt+left", sub=[S("go-next", "Adelante", "alt+right")]),
        S("view-sort-ascending", "Ordenar por nombre", "ctrl+alt+n",
          sub=[S("view-sort-descending", "Ordenar por tipo", "ctrl+alt+t")]),
        S("utilities-terminal", "Terminal aquí", "alt+shift+f4", sub=[S("utilities-terminal", "Panel terminal", "f4")]),
        S("view-reveal", "Barra de direcciones", "ctrl+l"),
        S("user-trash", "A la papelera", "delete",
          sub=[S("edit-undo", "Deshacer", "ctrl+z"), S("edit-copy", "Duplicar", "ctrl+d"),
               S("document-properties", "Propiedades", "alt+return")]),
    ],
}

# ---- Gwenview (fotos) — tus atajos de kxmlgui5 --------------------------------------------------------
GWENVIEW = {
    "nombre": "Fotos", "tono": 330,
    "sectores": [
        S("go-next", "Siguiente foto", "d", rueda=("a", "d")),
        S("object-rotate-right", "Rotar derecha", "e"),
        S("image-crop", "Recortar", "c"),
        S("zoom-fit-best", "Ajustar", "w",
          sub=[S("zoom-in", "Rellenar", "shift+w"), S("zoom-original", "Tamaño real", "ctrl+0")]),
        S("view-fullscreen", "Pantalla completa", "f"),
        S("user-trash", "A la papelera", "x"),
        S("go-previous", "Foto anterior", "a"),
        S("object-rotate-left", "Rotar izquierda", "q"),
        S("image-flip-horizontal", "Editar", "m",
          sub=[S("image-flip-horizontal", "Reflejar", "m"), S("zoom-fit-best", "Redimensionar", "r"),
               S("edit-undo", "Deshacer", "ctrl+z"), S("document-save", "Guardar", "ctrl+s")]),
        S("view-grid", "Miniaturas", "t",
          sub=[S("view-dual", "Barra lateral", "i"), S("feather-eye", "Modo foco", "s")]),
        S("edit-copy", "Copiar imagen", "ctrl+c"),
        S("folder-open", "Archivo", "ctrl+alt+o",
          sub=[S("edit-copy", "Copiar a…", "f7"), S("go-jump", "Mover a…", "ctrl+alt+m"),
               S("window-new", "Abrir en otra ventana", "ctrl+alt+n")]),
    ],
}

# ---- kitty (terminal) ---------------------------------------------------------------------------------
KITTY = {
    "nombre": "Terminal", "tono": 165,
    "sectores": [
        S("tab-new", "Nueva pestaña", "ctrl+shift+t"),
        S("go-next", "Pestaña siguiente", "ctrl+shift+right", rueda=("ctrl+shift+left", "ctrl+shift+right")),
        S("window-new", "Nueva ventana", "ctrl+shift+return"),
        S("edit-copy", "Copiar", "ctrl+shift+c"),
        S("edit-paste", "Pegar", "ctrl+shift+v"),
        S("format-text-larger", "Letra normal", "ctrl+shift+backspace",
          rueda=("ctrl+shift+equal", "ctrl+shift+minus"),
          sub=[S("zoom-in", "Más grande", "ctrl+shift+equal"), S("zoom-out", "Más chica", "ctrl+shift+minus")]),
        S("window-close", "Cerrar pestaña", "ctrl+shift+q"),
        S("process-stop", "Interrumpir", "ctrl+c", sub=[S("go-jump", "Salir (EOF)", "ctrl+d")]),
        S("go-previous", "Pestaña anterior", "ctrl+shift+left"),
        S("document-open-recent", "Historial", "ctrl+shift+h",
          sub=[S("go-up", "Arriba", "ctrl+shift+pageup"), S("go-down", "Abajo", "ctrl+shift+pagedown")]),
        S("edit-clear-all", "Limpiar", "ctrl+l"),
        S("system-search", "Buscar comando", "ctrl+r",
          sub=[S("go-first", "Inicio de línea", "ctrl+a"), S("go-last", "Fin de línea", "ctrl+e")]),
    ],
}

# ---- VS Code ----------------------------------------------------------------------------------------
CODE = {
    "nombre": "VS Code", "tono": 205,
    "sectores": [
        S("system-search", "Comandos", "ctrl+shift+p"),
        S("document-open", "Abrir archivo", "ctrl+p"),
        S("utilities-terminal", "Terminal", "ctrl+grave"),
        S("view-dual", "Barra lateral", "ctrl+b", sub=[S("view-dual", "Dividir editor", "ctrl+backslash")]),
        S("edit-find", "Buscar en todo", "ctrl+shift+f",
          sub=[S("edit-find-replace", "Reemplazar", "ctrl+h"), S("edit-find", "Buscar aquí", "ctrl+f")]),
        S("format-justify-left", "Formatear", "ctrl+shift+i"),
        S("go-jump", "Ir a definición", "f12", sub=[S("go-previous", "Volver", "ctrl+alt+minus"),
                                                    S("view-list", "Ir a símbolo", "ctrl+shift+o")]),
        S("text-x-generic", "Comentar", "ctrl+slash"),
        S("document-edit", "Renombrar símbolo", "f2"),
        S("document-save", "Guardar", "ctrl+s"),
        S("window-close", "Cerrar editor", "ctrl+w", sub=[S("edit-undo", "Reabrir", "ctrl+shift+t")]),
        S("go-down", "Mover línea abajo", "alt+down", rueda=("alt+up", "alt+down"),
          sub=[S("go-up", "Mover línea arriba", "alt+up"), S("edit-copy", "Duplicar línea", "shift+alt+down")]),
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
