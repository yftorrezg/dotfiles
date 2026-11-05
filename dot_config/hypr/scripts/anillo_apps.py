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


def TXT(texto, enter=True):
    """Escribe texto (y Enter) en la ventana con foco: TXT('/clear'), TXT('/btw ', False)."""
    return ("texto", texto, enter)


def TK(*combos):
    """Teclas seguidas en una sola ráfaga: TK('ctrl+x', 'n') = tecla líder y luego n."""
    return list(combos)


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
    "nombre": "mpv", "logo": "movie", "acento": "#8b5cf6",
    "sectores": [
        S("notes", "Nueva nota", "ctrl+n", color=ROSA),
        S("bookmarks", "Menú de marcas", "shift+b", color=AZUL,
          sub=[S("list-details", "Capítulos y marcas", "shift+c", color=AZUL), S("arrow-right", "Marca siguiente", "pageup", color=AZUL),
               S("arrow-left", "Marca anterior", "pagedown", color=AZUL)]),
        S("arrow-back-up", "Deshacer salto", "ctrl+z", color=AZUL),
        S("repeat", "Bucle A-B", "c", color=MORADO,
          sub=[S("repeat-once", "Últimos 15 s", "ctrl+c", color=MORADO), S("history", "Bucles guardados", "shift+l", color=MORADO)]),
        S("zoom-reset", "Velocidad 1×", "r", color=MORADO),
        S("player-skip-forward", "Cuadro a cuadro", "period", color=MORADO, sub=[S("player-skip-back", "Cuadro atrás", "comma", color=MORADO)]),
        S("camera", "Captura", "s", color=NARANJA, sub=[S("camera-off", "Sin subtítulos", "shift+s", color=NARANJA)]),
        S("folder-open", "Abrir carpeta / curso", "alt+c", color=VERDE, sub=[S("folder-plus", "Carpeta actual", "alt+shift+c", color=VERDE)]),
        S("badge-cc", "Subtítulos", "shift+j", color=MORADO, sub=[S("eye-off", "Mostrar / ocultar", "shift+v", color=MORADO)]),
        S("arrows-maximize", "Pantalla completa", "f", color=CIAN, sub=[S("chart-bar", "Estadísticas", "ctrl+i", color=CIAN)]),
        S("player-skip-forward", "Siguiente video", "shift+n", color=MORADO, sub=[S("player-skip-back", "Video anterior", "shift+p", color=MORADO)]),
        S("door-exit", "Salir recordando", "ctrl+q", color=ROJO, sub=[S("x", "Salir sin recordar", "ctrl+shift+q", color=ROJO)]),
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
        S("archive", "Archivar chat", "ctrl+alt+shift+e", color=CIAN),
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
        S("search", "Buscar", "ctrl+f", color=AMARILLO,
          sub=[S("filter", "Filtrar esta carpeta", "ctrl+i", color=AMARILLO), S("command", "Buscar una acción", "ctrl+alt+i", color=AMARILLO)]),
        S("checks", "Invertir selección", "ctrl+shift+a", color=ROSA, sub=[S("select-all", "Seleccionar todo", "ctrl+a", color=ROSA)]),
        S("layout-sidebar", "Panel de información", "f11", color=CIAN,
          sub=[S("bookmarks", "Panel de lugares", "f9", color=CIAN), S("list-tree", "Árbol de carpetas", "f7", color=CIAN),
               S("eye", "Vistas previas", "f12", color=CIAN)]),
        S("list-details", "Vista detalles", "ctrl+3", color=CIAN,
          sub=[S("layout-grid", "Iconos", "ctrl+1", color=CIAN), S("layout-list", "Compacta", "ctrl+2", color=CIAN)]),
        S("copy", "Copiar ruta", "ctrl+alt+c", color=TURQUESA,
          sub=[S("copy-plus", "Copiar al otro panel", "shift+f5", color=VERDE), S("arrow-forward-up", "Mover al otro panel", "shift+f6", color=AZUL)]),
        S("info-circle", "Propiedades", "alt+return", color=TURQUESA),
        S("trash", "A la papelera", "delete", color=ROJO),
        S("app-window", "Ventana nueva", "ctrl+n", color=VERDE),
        S("arrow-back-up", "Reabrir pestaña", "ctrl+shift+t", color=VERDE),
        S("terminal-2", "Terminal aquí", "alt+shift+f4", color=TURQUESA),
        S("arrow-back-up", "Deshacer", "ctrl+z", color=AZUL),
        S("menu-2", "Menú del archivo", "menu", color=TURQUESA),
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

# ---- kitty (terminal): 3 perfiles según lo que corre dentro (se detecta en mx-accion.clase_efectiva) -------
# Las burbujas comunes están a la MISMA hora en los tres: 1 = insertar ruta (hints de kitty), 3 = captura/Claude,
# 6 = @ archivo. Hora 12 = nuevo/arranque, hora 9 = compactar/reiniciar.
RUTA = S("file-search", "Insertar ruta", TK("ctrl+shift+p", "f"), color=AMARILLO,
         sub=[S("hash", "Hash de git", TK("ctrl+shift+p", "h")),
              S("list-search", "Línea de pantalla", TK("ctrl+shift+p", "l")),
              S("external-link", "Abrir URL", "ctrl+shift+e", color=AZUL)])

KITTY = {
    "nombre": "Terminal", "logo": "terminal-2", "acento": "#2ee6c5",
    "sectores": [
        S("file-search", "Archivo (fzf)", "ctrl+t", color=AMARILLO,
          sub=[S("folder-search", "Carpeta (fzf)", "alt+c", color=AZUL),
               S("folder", "Carpeta frecuente", TXT("zi"), color=AZUL)]),
        RUTA,
        S("git-branch", "Git estado", TXT("git status -sb"), color=CIAN,
          sub=[S("file-diff", "Diff", TXT("git diff")), S("history", "Log", TXT("git log --oneline -15"), color=AZUL),
               S("arrow-down", "Pull", TXT("git pull"), color=VERDE), S("arrow-up", "Push", TXT("git push"), color=VERDE)]),
        S("sparkles", "Claude Code", TXT("claude"), color=VERDE,
          sub=[S("history", "Continuar", TXT("claude --continue"), color=AZUL),
               S("robot", "opencode", TXT("opencode")),
               S("history", "opencode continuar", TXT("opencode -c"), color=AZUL)]),
        S("list-details", "Salida del último comando", "ctrl+shift+g", color=CIAN,
          sub=[S("history", "Scrollback completo", "ctrl+shift+h", color=AZUL)]),
        S("app-window", "Nueva ventana kitty", "ctrl+shift+return", color=VERDE,
          sub=[S("layout-columns", "Siguiente layout", "ctrl+shift+l", color=CIAN),
               S("arrows-split", "Redimensionar", "ctrl+shift+r", color=CIAN),
               S("x", "Cerrar ventana", "ctrl+shift+w", color=ROJO)]),
        S("pencil", "Editar comando", "alt+e", color=ROSA,
          sub=[S("arrow-bar-to-up", "Inicio de línea", "ctrl+a", color=AZUL),
               S("arrow-bar-to-down", "Fin de línea", "ctrl+e", color=AZUL)]),
        S("player-pause", "Suspender", "ctrl+z", color=ROJO,
          sub=[S("player-play", "Reanudar (fg)", TXT("fg"), color=MORADO), S("door-exit", "Salir (EOF)", "ctrl+d", color=ROJO)]),
        S("cpu", "Monitor", TXT("btop"), color=CIAN,
          sub=[S("box-multiple", "Contenedores", TXT("docker ps"), color=CIAN)]),
        S("eraser", "Reiniciar terminal", TXT("reset"), color=ROJO,
          sub=[S("clear-all", "Limpiar todo", "ctrl+shift+delete", color=ROJO)]),
        S("text-size", "Letra normal", "ctrl+shift+backspace", color=ROSA,
          rueda=("ctrl+shift+equal", "ctrl+shift+minus"),
          sub=[S("text-increase", "Más grande", "ctrl+shift+equal"), S("text-decrease", "Más chica", "ctrl+shift+minus")]),
        S("folder-open", "Abrir en Dolphin", TXT("xdg-open ."), color=AZUL,
          sub=[S("brand-vscode", "VS Code aquí", TXT("code ."), color=ROSA)]),
    ],
}

CLAUDE = {
    "nombre": "Claude Code", "logo": "sparkles", "acento": "#d97757",
    "sectores": [
        S("message-plus", "Nueva conversación", TXT("/clear"), color=VERDE,
          sub=[S("history", "Retomar", TXT("/resume"), color=AZUL), S("git-branch", "Ramificar", TXT("/branch"), color=VERDE),
               S("pencil", "Nombrar sesión", TXT("/rename"), color=ROSA), S("door-exit", "Salir", TXT("/exit"), color=ROJO)]),
        RUTA,
        S("file-diff", "Ver cambios", TXT("/diff"), color=CIAN,
          sub=[S("microscope", "Revisar", TXT("/review"), color=CIAN), S("shield-check", "Seguridad", TXT("/security-review")),
               S("wand", "Simplificar", TXT("/simplify"), color=ROSA)]),
        S("photo-plus", "Captura y pegar", PEGAR_CAPTURA, color=NARANJA),
        S("copy", "Copiar respuesta", TXT("/copy"),
          sub=[S("file-export", "Exportar", TXT("/export")), S("clipboard", "Copiar selección", "ctrl+shift+c")]),
        S("shield-check", "Permisos", TXT("/permissions"),
          sub=[S("brain", "Memoria", TXT("/memory"), color=ROSA), S("robot", "Agentes", TXT("/agents")),
               S("plug-connected", "MCP", TXT("/mcp")), S("settings", "Ajustes", TXT("/config"))]),
        S("at", "@ Archivo", TK("shift+apostrophe"), color=AMARILLO,
          sub=[S("terminal", "! Comando", TK("shift+1")), S("search", "Buscar prompt", "ctrl+r", color=AMARILLO),
               S("list-search", "Buscar en conversación", TK("ctrl+o", "slash"), color=AMARILLO)]),
        S("list-check", "Tareas", TXT("/tasks"), color=CIAN,
          sub=[S("route", "Plan", TXT("/plan"), color=AZUL), S("file-code", "Crear CLAUDE.md", TXT("/init"), color=VERDE)]),
        S("adjustments-bolt", "Esfuerzo", TXT("/effort"),
          sub=[S("bolt", "Modo rápido", "alt+o", color=AMARILLO), S("coin", "Uso y cuota", TXT("/usage"))]),
        S("arrows-minimize", "Compactar", TXT("/compact"),
          sub=[S("chart-pie", "Contexto", TXT("/context"), color=CIAN),
               S("message-circle-question", "Pregunta lateral", TXT("/btw ", False))]),
        S("sparkles", "Skills", TXT("/skills"), sub=[S("repeat", "Bucle", TXT("/loop ", False))]),
        S("stethoscope", "Diagnóstico", TXT("/doctor"),
          sub=[S("info-circle", "Estado", TXT("/status")), S("help-circle", "Ayuda", TXT("/help"))]),
    ],
}

OPENCODE = {
    "nombre": "opencode", "logo": "robot", "acento": "#3b82f6",
    "sectores": [
        S("message-plus", "Nueva sesión", TK("ctrl+x", "n"), color=VERDE,
          sub=[S("history", "Sesiones", TK("ctrl+x", "l"), color=AZUL), S("file-export", "Exportar", TK("ctrl+x", "x"))]),
        RUTA,
        S("cpu", "Modelos", TK("ctrl+x", "m"),
          sub=[S("plug-connected", "Conectar proveedor", TXT("/connect")), S("sparkles", "Temas", TK("ctrl+x", "t"), color=ROSA)]),
        S("photo-plus", "Captura y pegar", PEGAR_CAPTURA, color=NARANJA),
        S("copy", "Copiar mensaje", TK("ctrl+x", "y"), sub=[S("clipboard", "Copiar selección", "ctrl+shift+c")]),
        S("info-circle", "Estado", TK("ctrl+x", "s"),
          sub=[S("file-code", "Crear AGENTS.md", TXT("/init"), color=VERDE), S("reload", "Actualizar", TXT("/update"))]),
        S("at", "@ Archivo", TK("shift+apostrophe"), color=AMARILLO, sub=[S("terminal", "! Comando", TK("shift+1"))]),
        S("eye", "Detalles de herramientas", TXT("/details"), color=CIAN,
          sub=[S("brain", "Razonamiento", TXT("/thinking"), color=ROSA)]),
        S("robot", "Agentes", TK("ctrl+x", "a"), sub=[S("hierarchy-3", "Subagente (hijo)", TK("ctrl+x", "down"), color=CIAN)]),
        S("arrows-minimize", "Compactar", TK("ctrl+x", "c"), sub=[S("file-export", "Exportar", TK("ctrl+x", "x"))]),
        S("door-exit", "Salir", TK("ctrl+x", "q"), color=ROJO, sub=[S("player-pause", "Suspender", "ctrl+z", color=ROJO)]),
        S("keyboard", "Chuleta de atajos", "ctrl+alt+k", sub=[S("help-circle", "Ayuda", TXT("/help"))]),
    ],
}

# ---- VS Code ----------------------------------------------------------------------------------------
# Atajos de fábrica de Linux + ~/.config/Code/User/keybindings.json (Ctrl+Alt+...). Terminal-alternar, paleta,
# abrir archivo, definición, depurar y pestañas viven en los botones del mouse (mx-accion.py), no aquí.
# Solo la hora 7 cambia según el archivo del editor activo (título de la ventana): Python / Web / otro.
def _code(contextual):
    return {
    "nombre": "VS Code", "logo": "brand-vscode", "acento": "#23a9f2",
    "sectores": [
        S("message-chatbot", "Chat IA", "ctrl+alt+i", color=MORADO,
          sub=[S("sparkles", "Chat en línea", "ctrl+i"), S("settings", "Ajustes", "ctrl+comma"),
               S("keyboard", "Atajos", ["ctrl+k", "ctrl+s"]), S("puzzle", "Extensiones", "ctrl+shift+x"),
               S("tools", "Tareas / Build", "ctrl+shift+b")]),
        S("terminal-2", "Nueva terminal", "ctrl+shift+grave", color=VERDE,
          sub=[S("layout-columns", "Dividir", "ctrl+shift+5"), S("arrows-maximize", "Maximizar panel", "ctrl+alt+m", color=CIAN),
               S("focus-2", "Foco terminal", "ctrl+alt+j", color=AZUL), S("arrow-right", "Terminal siguiente", "ctrl+alt+pagedown"),
               S("arrow-left", "Terminal anterior", "ctrl+alt+pageup")]),
        S("layout-sidebar-right", "Explorador", "ctrl+shift+e", color=CIAN,
          sub=[S("brand-git", "Git", "ctrl+shift+g", color=CIAN), S("bug", "Depurar", "ctrl+shift+d", color=CIAN),
               S("alert-triangle", "Problemas", "ctrl+shift+m", color=ROJO), S("folder-search", "Revelar archivo", "ctrl+alt+e", color=AZUL),
               S("terminal", "Salida", "ctrl+shift+u", color=CIAN)]),
        S("search", "Buscar en proyecto", "ctrl+shift+f",
          sub=[S("zoom-replace", "Reemplazar en proyecto", "ctrl+shift+h"), S("search", "Buscar en archivo", "ctrl+f"),
               S("replace", "Reemplazar en archivo", "ctrl+h"), S("arrow-down", "Siguiente coincidencia", "f3", color=AZUL),
               S("arrow-up", "Anterior coincidencia", "shift+f3", color=AZUL), S("regex", "Regex", "alt+r", color=AMARILLO)]),
        S("sitemap", "Ir a símbolo", "ctrl+shift+o", color=AZUL, rueda=("ctrl+alt+minus", "ctrl+shift+minus"),
          sub=[S("code-dots", "Símbolo en proyecto", "ctrl+t"), S("arrow-bar-to-right", "Ir a línea", "ctrl+g"),
               S("arrow-forward-up", "Implementación", "ctrl+f12"), S("history", "Archivos recientes", "ctrl+r"),
               S("pencil", "Última edición", ["ctrl+k", "ctrl+q"], color=AZUL), S("brackets-contain", "Corchete par", "ctrl+shift+backslash")]),
        S("alert-triangle", "Siguiente problema", "f8", color=ROJO, rueda=("shift+f8", "f8"),
          sub=[S("arrow-up", "Problema anterior", "shift+f8", color=AZUL), S("bulb", "Arreglo rápido", "ctrl+period", color=ROSA),
               S("eye", "Mostrar hover", ["ctrl+k", "ctrl+i"]), S("arrows-maximize", "Desplegar todo", ["ctrl+k", "ctrl+j"]),
               S("arrows-minimize", "Plegar todo", ["ctrl+k", "ctrl+0"])]),
        S("player-stop", "Parar depuración", "shift+f5", color=ROJO,
          sub=[S("rotate-clockwise-2", "Reiniciar", "ctrl+shift+f5", color=CIAN), S("player-play", "Ejecutar sin depurar", "ctrl+f5", color=MORADO),
               S("terminal", "Consola de depuración", "ctrl+shift+y"), S("tools", "Build", "ctrl+shift+b")]),
        contextual,
        S("cursor-text", "Multicursor", "ctrl+d", color=ROSA, rueda=("ctrl+alt+up", "ctrl+alt+down"),
          sub=[S("select-all", "Todas las ocurrencias", "ctrl+shift+l"), S("arrow-up", "Cursor arriba", "ctrl+alt+up", color=ROSA),
               S("arrow-down", "Cursor abajo", "ctrl+alt+down", color=ROSA), S("arrow-back-up", "Deshacer cursor", "ctrl+u", color=ROSA),
               S("arrow-bar-to-right", "Cursores al fin de línea", "shift+alt+i"), S("arrows-maximize", "Expandir selección", "shift+alt+right")]),
        S("align-justified", "Formatear", "ctrl+shift+i",
          sub=[S("cursor-text", "Renombrar símbolo", "f2"), S("code", "Comentar línea", "ctrl+slash"),
               S("brackets-angle", "Comentario de bloque", "shift+alt+a"), S("align-justified", "Formatear selección", ["ctrl+k", "ctrl+f"]),
               S("text-wrap", "Ajuste de línea", "alt+z"), S("eraser", "Quitar espacios finales", ["ctrl+k", "ctrl+x"], color=ROSA)]),
        S("arrow-down", "Mover línea", "alt+down", color=ROSA, rueda=("alt+up", "alt+down"),
          sub=[S("arrow-up", "Mover arriba", "alt+up", color=ROSA), S("copy-plus", "Duplicar abajo", "shift+alt+down"),
               S("trash", "Borrar línea", "ctrl+shift+k"), S("file-plus", "Línea debajo", "ctrl+return", color=VERDE),
               S("file-plus", "Línea encima", "ctrl+shift+return", color=VERDE), S("cursor-text", "Seleccionar línea", "ctrl+l", color=ROSA)]),
        S("x", "Cerrar editor", "ctrl+w",
          sub=[S("arrow-back-up", "Reabrir", "ctrl+shift+t", color=VERDE), S("x", "Cerrar otros", "ctrl+alt+t"),
               S("pinned", "Anclar pestaña", ["ctrl+k", "shift+return"], color=CIAN), S("layout-columns", "Mover a grupo derecho", ["ctrl+k", "ctrl+right"], color=CIAN),
               S("focus-2", "Foco al editor", "ctrl+1", color=AZUL)]),
    ],
    }


_ZEN = S("arrows-maximize", "Modo Zen", ["ctrl+k", "z"], color=CIAN,
         sub=[S("player-play", "Ejecutar sin depurar", "ctrl+f5", color=MORADO), S("tools", "Build", "ctrl+shift+b"),
              S("layout-columns", "Dividir editor", "ctrl+backslash"), S("focus-2", "Foco grupo 2", "ctrl+2", color=AZUL),
              S("command", "Paleta", "ctrl+shift+p", color=AMARILLO)])
_PY = S("brand-python", "Ejecutar .py", "ctrl+alt+r", color=MORADO,
        sub=[S("player-play", "Ejecutar selección en REPL", "shift+return", color=MORADO),
             S("arrows-sort", "Organizar imports", "shift+alt+o", color=ROSA),
             S("brand-python", "Elegir intérprete", "ctrl+alt+shift+i", color=AZUL), S("terminal", "Abrir REPL", "ctrl+alt+shift+r")])
_WEB = S("brackets-angle", "Emmet: envolver", "ctrl+alt+w", color=ROSA,
         sub=[S("brackets-contain", "Corchete par", "ctrl+shift+backslash"), S("arrows-sort", "Organizar imports", "shift+alt+o", color=ROSA),
              S("bulb", "Arreglo rápido", "ctrl+period", color=ROSA),
              S("world-www", "Abrir Live Server", ["alt+l", "alt+o"], color=CIAN),
              S("player-stop", "Cerrar Live Server", ["alt+l", "alt+c"], color=ROJO)])
CODE = _code(_ZEN)
CODE_PY = _code(_PY)
CODE_WEB = _code(_WEB)

# ---- Obsidian ---------------------------------------------------------------------------------------
# Atajos: de fábrica + ~/Vídeos/.obsidian/hotkeys.json (Ctrl+Alt+... generales, Ctrl+Alt+Shift+... tablas).
# Las operaciones de TABLA (fila/columna) están en los botones del mouse (mx-accion.py), no aquí.
OBSIDIAN = {
    "nombre": "Obsidian", "logo": "notebook", "acento": "#7c3aed",
    "sectores": [
        S("file-search", "Ir a nota", "ctrl+o",
          sub=[S("command", "Paleta", "ctrl+p"), S("file-plus", "Nota nueva", "ctrl+n", color=VERDE),
               S("calendar-event", "Nota diaria", "ctrl+alt+7", color=AZUL), S("bookmarks", "Marcadores", "ctrl+alt+6", color=AZUL),
               S("arrow-back-up", "Reabrir pestaña", "ctrl+alt+r", color=VERDE), S("template", "Plantilla", "ctrl+alt+8", color=ROSA)]),
        S("search", "Buscar en el vault", "ctrl+shift+f",
          sub=[S("search", "En esta nota", "ctrl+f"), S("replace", "Reemplazar", "ctrl+h"), S("tags", "Etiquetas", "ctrl+alt+5", color=AZUL)]),
        S("cursor-text", "Seleccionar línea", ["home", "shift+end"], color=ROSA, rueda=("ctrl+alt+up", "ctrl+alt+down"),
          sub=[S("copy", "Copiar línea", ["home", "shift+end", "ctrl+c"]), S("cut", "Cortar línea", ["home", "shift+end", "ctrl+x"]),
               S("eraser", "Borrar línea", "ctrl+d"),
               S("copy-plus", "Duplicar línea", ["home", "shift+end", "ctrl+c", "end", "return", "ctrl+v"], color=VERDE),
               S("clipboard-text", "Pegar sin formato", "ctrl+shift+v", color=ROSA), S("select-all", "Seleccionar todo", "ctrl+a", color=ROSA)]),
        S("table-plus", "Insertar tabla", "ctrl+alt+t", color=ROSA,
          sub=[S("info-square-rounded", "Callout", "ctrl+alt+l"), S("code-dots", "Bloque de código", "ctrl+alt+b"),
               S("math-function", "Fórmula", "ctrl+alt+m"), S("link-plus", "Enlace [[ ]]", "ctrl+alt+i"),
               S("blockquote", "Cita", "ctrl+shift+9", color=ROSA), S("separator-horizontal", "Línea horizontal", ["minus", "minus", "minus"], color=ROSA)]),
        S("bold", "Negrita", "ctrl+b",
          sub=[S("italic", "Cursiva", "ctrl+i"), S("highlight", "Resaltar", "ctrl+alt+h"), S("code", "Código", "ctrl+alt+k"),
               S("strikethrough", "Tachado", "ctrl+alt+x"), S("link", "Enlace", "ctrl+k"), S("eraser", "Limpiar formato", "ctrl+alt+c", color=ROSA)]),
        S("heading", "Encabezado H2", "ctrl+alt+2",
          sub=[S("heading", "H1", "ctrl+alt+1"), S("heading", "H3", "ctrl+alt+3"), S("heading", "H4", "ctrl+alt+4"),
               S("text-size", "Texto normal", "ctrl+alt+0")]),
        S("checkbox", "Tarea", "ctrl+return", color=VERDE,
          sub=[S("list", "Viñetas", "ctrl+alt+u", color=ROSA), S("list-numbers", "Numerada", "ctrl+alt+n", color=ROSA),
               S("list-check", "Lista a tarea", "ctrl+alt+j", color=ROSA), S("arrow-right", "Sangrar", "tab"),
               S("arrow-left", "Quitar sangría", "shift+tab")]),
        S("book", "Lectura / edición", "ctrl+e",
          sub=[S("code", "Modo fuente", "ctrl+alt+e", color=CIAN), S("layout", "Ancho legible", "ctrl+alt+y"),
               S("layout-sidebar", "Panel izquierdo", "ctrl+alt+v"), S("layout-sidebar-right", "Panel derecho", "ctrl+alt+g"),
               S("fold-up", "Plegar todo", "ctrl+alt+comma", color=CIAN), S("fold-down", "Desplegar todo", "ctrl+alt+period", color=CIAN)],
          rueda=("ctrl+alt+[", "ctrl+alt+]")),
        S("browser-plus", "Pestaña nueva", "ctrl+t", color=VERDE, rueda=("ctrl+shift+tab", "ctrl+tab"),
          sub=[S("x", "Cerrar", "ctrl+w"), S("arrow-back-up", "Reabrir", "ctrl+alt+r", color=VERDE),
               S("arrow-bar-to-right", "Última", "ctrl+9", color=AZUL), S("pin", "Fijar", "ctrl+alt+p", color=CIAN),
               S("x", "Cerrar otras", "ctrl+alt+o")]),
        S("layout-columns", "Dividir a la derecha", "ctrl+alt+d",
          sub=[S("layout-rows", "Dividir abajo", "ctrl+alt+s"), S("x", "Cerrar panel", "ctrl+alt+w")]),
        S("hierarchy-2", "Backlinks", "ctrl+alt+q", color=AZUL,
          sub=[S("topology-star-3", "Grafo", "ctrl+g", color=AZUL), S("topology-star-3", "Grafo local", "ctrl+alt+z", color=AZUL),
               S("link", "Enlaces salientes", "ctrl+alt+9", color=AZUL), S("list-tree", "Esquema", "ctrl+alt+a", color=AZUL)]),
        S("brain", "Repasar esta nota (SR)", "ctrl+alt+4", color=MORADO,
          sub=[S("cards", "Repasar todas", "ctrl+alt+3", color=MORADO), S("stack-2", "Cola de repaso", "ctrl+alt+2", color=MORADO),
               S("notes", "Siguiente nota a repasar", "ctrl+alt+1", color=MORADO)]),
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
    {"clase": r"^kitty:claude$", **CLAUDE},
    {"clase": r"^kitty:opencode$", **OPENCODE},
    {"clase": r"^kitty(:shell)?$", **KITTY},
    {"clase": r"^(com\.microsoft\.VSCode|code|Code|code-oss)$", "titulo": r"\.(py|ipynb)\b", **CODE_PY},
    {"clase": r"^(com\.microsoft\.VSCode|code|Code|code-oss)$", "titulo": r"\.(html?|css|scss|jsx|tsx|vue|svelte)\b", **CODE_WEB},
    {"clase": r"^(com\.microsoft\.VSCode|code|Code|code-oss)$", **CODE},
    {"clase": r"^md\.obsidian\.Obsidian$", **OBSIDIAN},
]


def perfil_para(clase, titulo=""):
    import re
    for p in PERFILES:
        if re.search(p["clase"], clase or "") and (not p.get("titulo") or re.search(p["titulo"], titulo or "")):
            return p
    return GLOBAL
