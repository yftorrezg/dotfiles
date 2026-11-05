#!/usr/bin/env python3
"""mx-doc.py — genera la documentación del MX Master 4 a partir de las tablas REALES.

Lee PERFILES (mx-accion.py: gestos / atrás / adelante / rueda / pulgar) y los perfiles del anillo
(anillo_apps.py) y escribe el mismo documento en DOS sitios:
    ~/Documentos/20-mx-master-4.md              (tu documento)
    ~/.config/hypr/chuletas/20-mx-master-4.md    (la chuleta de SUPER+SHIFT+C)

Así la documentación no se desactualiza: cambias una tabla, ejecutas  python3 mx-doc.py  y listo.
El texto explicativo (cómo se usa, recetas, problemas) está en este archivo, en las funciones de abajo.
Los NOMBRES legibles de los gestos están en NOMBRES: si añades un gesto nuevo sin nombre, el script avisa.
"""
import importlib.util
import os
import re
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
SALIDAS = [os.path.expanduser("~/Documentos/20-mx-master-4.md"),
           os.path.expanduser("~/.config/hypr/chuletas/20-mx-master-4.md")]


def cargar(nombre, archivo):
    spec = importlib.util.spec_from_file_location(nombre, os.path.join(AQUI, archivo))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


mx = cargar("mx_accion", "mx-accion.py")
import anillo_apps as ap  # noqa: E402

# ---- Nombres legibles de los gestos (en el mismo orden que PERFILES: clic ↑ ↓ ← →) ---------------------
# None = hereda el nombre del perfil global.
G = "global"
BR, WA, MP, GW, DO = (r"^brave-browser$", r"^brave-web\.whatsapp\.com", r"^mpv$",
                      r"^org\.kde\.gwenview$", r"^org\.kde\.dolphin$")
OB = r"^md\.obsidian\.Obsidian$"
VS, KS, KC, KO = (r"^(com\.microsoft\.VSCode|code|Code|code-oss)$", r"^kitty:shell$", r"^kitty:claude$",
                  r"^kitty:opencode$")
NOMBRES = {
    G: {
        "rueda": ["Captura al portapapeles", "Pantalla completa", "Cerrar ventana", "Escritorio anterior",
                  "Escritorio siguiente"],
        "superior": ["Esc", "Gemini + ChatGPT (las 2)", "Dictado (SUPER+ALT+Z)", "Claude", "DeepSeek"],
        "gestos": ["Play / pausa", "Volumen +", "Volumen −", "Pista anterior", "Pista siguiente"],
        "atras": ["Atrás (nativo)", "Inicio", "Fin", "Atrás", "Adelante"],
        "adelante": ["Adelante (nativo)", "Nueva pestaña", "Cerrar pestaña", "Pestaña anterior", "Pestaña siguiente"],
        "pulgar": ["Volumen −", "Volumen +"],
    },
    BR: {
        "atras": ["Atrás", "Seleccionar todo", "Enter", "Copiar", "Pegar"],
        "adelante": ["Adelante", "Barra de direcciones", "Añadir a marcadores", "Recargar", "Buscar en la página"],
        "gestos": ["Reabrir pestaña", "Nueva pestaña", "Cerrar pestaña", "Buscar pestaña", "Curso de estudio (Udemy)"],
        "pulgar": ["Pestaña anterior", "Pestaña siguiente"],
    },
    WA: {
        "atras": ["Esc", "Chat anterior", "Chat siguiente", "Esc", "Buscar"],
        "adelante": ["Chat nuevo", "Fijar chat", "Archivar chat", "Silenciar chat", "Marcar no leído"],
        "gestos": ["Buscar chat", "Perfil", None, None, None],
        "pulgar": ["Chat anterior", "Chat siguiente"],
    },
    MP: {
        "atras": ["Video anterior", "+30 s", "−30 s", "−10 s", "+10 s"],
        "adelante": ["Video siguiente", "Velocidad x2", "Velocidad x1.5", "Velocidad +0.1", "Velocidad −0.1"],
        "gestos": ["Pausa / play", "Poner marca", "Ir a la marca", "Lista de videos", "Panel de notas"],
        "pulgar": ["−5 s", "+5 s"],
    },
    GW: {
        "atras": ["Deshacer", "Miniaturas", "Abrir en ventana nueva", "Copiar", "Abrir carpeta contenedora"],
        "adelante": ["Guardar", "Modo foco", "Reflejar", "Copiar a…", "Mover a…"],
        "gestos": ["Papelera", "Redimensionar", "Recortar", "Rotar izquierda", "Rotar derecha"],
        "pulgar": ["Foto anterior", "Foto siguiente"],
    },
    DO: {
        "atras": ["Atrás", "Barra de direcciones", "Carpeta superior", "Renombrar", "Duplicar"],
        "adelante": ["Adelante", "Nueva pestaña", "Cerrar pestaña", "Pestaña anterior", "Pestaña siguiente"],
        "gestos": ["Carpeta nueva", "Dividir vista", "Mostrar ocultos", "Ordenar por nombre", "Ordenar por tipo"],
        "pulgar": ["Iconos más chicos", "Iconos más grandes"],
    },
    VS: {
        "gestos": ["Terminal", "Paleta de comandos", "Abrir archivo", "Barra lateral", "Dividir editor"],
        "atras": ["Atrás (navegación)", "Ir a definición", "Ver definición (peek)", "Referencias", "Adelante (navegación)"],
        "adelante": ["Depurar: continuar", "Punto de interrupción", "Paso sobre", "Paso dentro", "Paso fuera"],
        "pulgar": ["Pestaña anterior", "Pestaña siguiente"],
    },
    OB: {
        "gestos": ["Deshacer", "Fila encima", "Fila debajo", "Columna a la izquierda", "Columna a la derecha"],
        "atras": ["Atrás (historial)", "Mover fila arriba", "Mover fila abajo", "Mover columna izquierda",
                  "Mover columna derecha"],
        "adelante": ["Adelante (historial)", "Borrar fila", "Borrar columna", "Duplicar fila", "Duplicar columna"],
        "pulgar": ["Pestaña anterior", "Pestaña siguiente"],
    },
    KS: {
        "gestos": ["Interrumpir", "Historial (fzf)", "Limpiar", "Borrar línea", "Último argumento"],
        "atras": ["Directorio anterior", "Copiar", "Pegar", "Borrar palabra", "Anteponer sudo"],
        "adelante": ["Directorio siguiente", "Pestaña nueva", "Cerrar pestaña", "Pestaña anterior", "Pestaña siguiente"],
        "pulgar": ["Prompt anterior", "Prompt siguiente"],
    },
    KC: {
        "gestos": ["Cambiar modo (editar / plan)", "Transcript", "Pasar a segundo plano", "Cambiar modelo",
                   "Checklist de tareas"],
        "atras": ["Pegar imagen", "Editar prompt en editor", "Pegar texto", "Borrar línea", "Guardar borrador"],
        "adelante": ["Último mensaje", "Inicio de la conversación", "Redibujar", "Rewind (Esc Esc)", "Enviar cola ya"],
        "pulgar": ["Subir (media pantalla)", "Bajar (media pantalla)"],
    },
    KO: {
        "gestos": ["Agente build / plan", "Variante de esfuerzo", "Paleta de comandos", "Modelo reciente",
                   "Agente anterior"],
        "atras": ["Deshacer mensaje", "Pegar imagen", "Pegar texto", "Borrar línea", "Editor externo"],
        "adelante": ["Rehacer", "Primer mensaje", "Último mensaje", "Barra lateral", "Línea de tiempo"],
        "pulgar": ["Subir (media pantalla)", "Bajar (media pantalla)"],
    },
}
APPS_GESTOS = [(BR, "🦁 Brave"), (WA, "💬 WhatsApp"), (MP, "🎬 mpv"), (GW, "🖼️ Fotos (Gwenview)"),
               (DO, "📁 Dolphin"), (VS, "🧑‍💻 VS Code"), (OB, "📓 Obsidian"), (KS, "⌨️ Terminal (shell)"),
               (KC, "✳️ Claude Code"), (KO, "🤖 opencode")]
# programa del anillo → clase de ventana de ejemplo (para comparar con los gestos)
CLASE_EJEMPLO = {"Sistema": "", "Brave": "brave-browser", "YouTube": "brave-www.youtube.com__-Default",
                 "WhatsApp": "brave-web.whatsapp.com__-Default", "Telegram": "org.telegram.desktop", "mpv": "mpv",
                 "Dolphin": "org.kde.dolphin", "Fotos": "org.kde.gwenview", "Terminal": "kitty:shell", "VS Code": "com.microsoft.VSCode",
                 "Obsidian": "md.obsidian.Obsidian", "Claude Code": "kitty:claude", "opencode": "kitty:opencode"}

# ---- Descripción de atajos -----------------------------------------------------------------------------
TECLAS = {"return": "Enter", "esc": "Esc", "tab": "Tab", "space": "Espacio", "left": "←", "right": "→", "up": "↑",
          "down": "↓", "pageup": "Re Pág", "pagedown": "Av Pág", "home": "Inicio", "end": "Fin", "delete": "Supr",
          "backspace": "Retroceso", "slash": "/", "period": ".", "comma": ",", "minus": "-", "equal": "=",
          "grave": "acento grave", "backslash": "\\", "playpause": "Play/Pausa", "volumeup": "Vol +",
          "volumedown": "Vol −", "prevsong": "Pista ant.", "nextsong": "Pista sig.", "super": "Super"}


def combo(c):
    return "+".join(TECLAS.get(p, p.upper() if len(p) <= 2 and p[0] == "f" and p[1:].isdigit() else
                               p.capitalize() if len(p) > 1 else p.upper()) for p in c.split("+"))


def describir(a):
    """Texto corto de lo que dispara una acción (el atajo, o el comando)."""
    if a is None:
        return ""
    if isinstance(a, str):
        return combo(a)
    if isinstance(a, list):
        return " → ".join(describir(x) for x in a)
    if a[0] == "click":
        return {"back": "clic nativo Atrás", "forward": "clic nativo Adelante", "middle": "clic central"}[a[1]]
    if a[0] == "rueda-libre":
        return "rueda libre/carraca"
    if a[0] == "esperar":
        return "captura de región y pegar"
    if a[0] == "texto":
        return a[1].strip()
    c = a[1]
    if c[:2] == ["noctalia", "msg"]:
        return "noctalia msg " + " ".join(c[2:])
    if c[0] == "bash" and c[1].endswith("app-web.sh"):
        return "app web " + c[2]
    if c[0] in ("bash", "python3"):
        return os.path.basename(c[1])
    if c[0] == "brave":
        return "abre el enlace"
    return " ".join(c)


def cod(txt):
    return f"`{txt}`" if txt else ""


def celda_gesto(nombre, accion):
    """Nombre + atajo; sin atajo si sería repetir lo mismo (Esc / Esc) o si es un comando que no es una tecla."""
    d = describir(accion)
    if not d or isinstance(accion, tuple) and accion[0] in ("click", "cmd"):
        return nombre
    plano = lambda t: re.sub(r"[^a-z0-9]", "", t.lower())
    if plano(d) == plano(nombre) or plano(d) in plano(nombre) or d in ("Vol +", "Vol −", "Pista ant.", "Pista sig.", "Play/Pausa"):
        return nombre
    return f"{nombre} {cod(d)}"


# ---- Tablas de gestos ---------------------------------------------------------------------------------
BOTONES = [("rueda", "Rueda (clic central)"), ("superior", "Superior"), ("gestos", "Gestos"),
           ("atras", "Atrás"), ("adelante", "Adelante")]
ENCAB = "| Botón | Clic | ↑ Arriba | ↓ Abajo | ← Izquierda | → Derecha |\n|---|---|---|---|---|---|"
problemas = []


def fila(clase_regex, boton, etiqueta):
    """Fila de tabla (clic ↑ ↓ ← →) con nombre + atajo; hereda lo que el perfil deja en None."""
    celdas = []
    for i in range(5):
        if clase_regex == G:
            acc = mx.PERFILES[G][boton][i]
            nom = NOMBRES[G][boton][i]
        else:
            fila_p = mx.PERFILES[clase_regex].get(boton)
            acc = fila_p[i] if fila_p and i < len(fila_p) and fila_p[i] is not None else mx.PERFILES[G][boton][i]
            propio = bool(fila_p and fila_p[i] is not None)
            nom = (NOMBRES[clase_regex].get(boton, [None] * 5)[i] if propio else NOMBRES[G][boton][i])
            if propio and nom is None:
                problemas.append(f"falta el nombre de {clase_regex} {boton}[{i}]")
        celdas.append(celda_gesto(nom or "?", acc))
    return f"| {etiqueta} | " + " | ".join(celdas) + " |"


def tabla_app(clase_regex):
    filas = [ENCAB]
    for boton, etiqueta in (("gestos", "Gestos"), ("atras", "Atrás"), ("adelante", "Adelante")):
        filas.append(fila(clase_regex, boton, etiqueta))
    pul = mx.PERFILES.get(clase_regex, {}).get("pulgar") or mx.PERFILES[G]["pulgar"]
    nom = NOMBRES.get(clase_regex, {}).get("pulgar") or NOMBRES[G]["pulgar"]
    return "\n".join(filas) + f"\n\n- `Rueda del pulgar` :: {nom[0]} ({cod(describir(pul[0]))}) / {nom[1]} ({cod(describir(pul[1]))})"


# ---- Tablas del anillo --------------------------------------------------------------------------------
def hora(i):
    return str(i if i else 12)


def tabla_anillo(p):
    filas = ["| Hora | Acción | Atajo | Sub-opciones (aleja más el mouse) | Rueda del mouse |", "|---|---|---|---|---|"]
    for i, s in enumerate(p["sectores"]):
        subs = " · ".join(f"{x['nombre']} {cod(describir(x['accion']))}" for x in s["sub"]) or "—"
        rueda = (f"↑ {describir(s['rueda'][0])} / ↓ {describir(s['rueda'][1])}" if s["rueda"] else "—")
        filas.append(f"| {hora(i)} | **{s['nombre']}** | {cod(describir(s['accion']))} | {subs} | {cod(rueda) if s['rueda'] else rueda} |")
    return "\n".join(filas)


def repetidos():
    """Acciones que están a la vez en el anillo y en un botón (candidatas a cambiar por algo nuevo)."""
    filas = ["| Programa | Acción repetida | En el anillo | En el botón |", "|---|---|---|---|"]
    n = 0
    hechos = set()
    for p in [ap.GLOBAL] + ap.PERFILES:
        if p["nombre"] in hechos:
            continue
        hechos.add(p["nombre"])
        clase = CLASE_EJEMPLO.get(p["nombre"], "")
        botones = {}
        for boton, etiqueta in (("gestos", "Gestos"), ("atras", "Atrás"), ("adelante", "Adelante")):
            for i, d in enumerate(("clic", "↑", "↓", "←", "→")):
                acc = mx.buscar(clase, boton, i)[1]
                if isinstance(acc, str):
                    botones.setdefault(acc, f"{etiqueta} {d}")
        vistos = set()
        for i, s in enumerate(p["sectores"]):
            for e in [s] + s["sub"]:
                if isinstance(e["accion"], str) and e["accion"] in botones and (p["nombre"], e["accion"]) not in vistos:
                    vistos.add((p["nombre"], e["accion"]))
                    n += 1
                    filas.append(f"| {p['nombre']} | {cod(describir(e['accion']))} | {e['nombre']} (hora {hora(i)}) | {botones[e['accion']]} |")
    return "\n".join(filas) if n else "Ninguna: cada acción está solo en un sitio. 👍"


def comprobar_nombres():
    for clase in mx.PERFILES:
        if clase == G:
            continue
        if clase not in NOMBRES:
            problemas.append(f"perfil de gestos sin nombres: {clase}")


# ---- Documento ----------------------------------------------------------------------------------------
def documento():
    comprobar_nombres()
    t = []
    a = t.append
    a("""# 🖱️ MX Master 4 · Botones, gestos y anillo

> Todo lo que hace el mouse: cada botón, cada gesto por programa y el anillo radial. Este documento se genera solo con `mx-doc.py`.

## 🧭 Resumen en 30 segundos

| Control | Dónde está | Qué hace | Alcance |
|---|---|---|---|
| Rueda | Clic central | Pantalla y escritorios | Global |
| Superior | Botón plano detrás de la rueda | Abrir IAs | Global |
| Gestos | Apoyo del pulgar | Acciones del programa con foco | Por programa |
| Atrás | Lateral | Navegar | Por programa |
| Adelante | Lateral | Pestañas y vistas | Por programa |
| Panel háptico | Panel con puntitos | **Anillo radial** de 12 acciones | Por programa |
| Rueda del pulgar | Rueda horizontal | Según el programa | Por programa |

🧠 Concepto: **global** = hace lo mismo en cualquier ventana. **Por programa** = el mouse mira qué ventana tiene el foco y cambia lo que hace.

## 🤏 Cómo se usa un botón de gestos
Sirve para Rueda, Superior, Gestos, Atrás y Adelante. Cada uno tiene **5 acciones**: clic y 4 direcciones.

1. **Clic**: pulsa y suelta sin mover el mouse.
2. **Gesto**: mantén el botón, mueve el mouse unos 2 cm hacia arriba, abajo, izquierda o derecha y suelta.
3. Las diagonales no hacen nada.

💡 Consejo: no hace falta un gesto largo; con 2 cm basta. Si mueves poco, cuenta como clic.

## 🌐 Botones globales (iguales en todo)
""")
    a(ENCAB)
    for boton, etiqueta in (("rueda", "Rueda"), ("superior", "Superior")):
        a(fila(G, boton, etiqueta))
    a("""
📌 Nota: las IAs se abren como ventana de app de Brave; si ya está abierta, la enfoca en vez de abrir otra.

## 📱 Gestos, Atrás y Adelante por programa
El botón **Gestos** es el que cambia más: cada programa tiene sus 5 acciones más útiles. Atrás y Adelante también cambian.
""")
    for regex, titulo in APPS_GESTOS:
        a(f"### {titulo}\n")
        a(tabla_app(regex))
        a("")
    a("### 🧰 Resto de programas\n")
    a("Lo que no tiene perfil propio usa esto (también Telegram, terminal, VS Code y YouTube para estos botones; su anillo sí es propio).\n")
    a(tabla_app(G))
    a("""
⚠️ Cuidado: los atajos de WhatsApp (fijar, archivar, silenciar, no leído) son los oficiales de WhatsApp Web; si alguno no responde, se corrige en `mx-accion.py`.

## 🎯 El anillo radial (panel háptico)

### ¿Qué es?
Un anillo de **12 burbujas** que aparece alrededor del cursor al tocar el panel háptico. Las 12 acciones **cambian según el programa**: en WhatsApp salen acciones de chats, en mpv acciones de video, en Dolphin acciones de archivos. Es la forma más rápida de tener a mano decenas de atajos sin memorizarlos.

### Cómo se usa
1. **Toca** el panel háptico (un toque, sin mantener). El anillo aparece y se queda abierto.
2. **Mueve el mouse** hacia una burbuja. No hace falta llegar a ella: cuenta la **dirección**. La elegida crece, se enciende y el mouse vibra suave.
3. **Confirma** con un clic izquierdo o tocando otra vez el panel. Se ejecuta y el anillo se cierra.

Para cerrar sin hacer nada: clic en el centro, clic derecho o 10 segundos sin moverte.

⚡ Modo rápido: **mantén** el panel, apunta hacia la burbuja y suelta. Funciona si lo mantuviste más de 0,35 s; si soltaste antes, cuenta como un toque y el anillo se queda abierto.

### Las 12 posiciones (como un reloj)
Las burbujas se numeran como las horas: **12** arriba, **3** a la derecha, **6** abajo y **9** a la izquierda. En las tablas de abajo, la columna **Hora** dice dónde está cada una. Con el tiempo tu mano aprende «la hora de» las que más usas.

### Sub-opciones (burbujas con un puntito)
Una burbuja con un **puntito** guarda más acciones. Apunta a ella y **aleja más el mouse** en esa misma dirección: salen en un arco por fuera. Elige una y confirma igual que antes. Ejemplo: en Telegram, **Formato** tiene negrita, cursiva, tachado, código, spoiler y enlace.

### Rueda del mouse
- Sobre una burbuja con rueda (columna **Rueda del mouse**) la rueda hace su ajuste: pestañas, zoom, velocidad, chat siguiente…
- En el **centro** (sin elegir nada) la rueda siempre sube o baja el volumen, en cualquier programa.

### Colores y centro
Cada color es un **tipo** de acción, igual en todos los programas:

| Color | Tipo de acción |
|---|---|
| 🔴 Rojo | Cerrar, borrar, bloquear |
| 🟢 Verde | Nuevo, crear, reabrir |
| 🟡 Amarillo | Buscar |
| 🔵 Azul | Moverse, navegar, ir a |
| 🟣 Morado | Multimedia: play, volumen, velocidad |
| 🟠 Naranja | Capturas y fotos |
| 🩷 Rosa | Editar, formato, rotar |
| 🩵 Cian | Vistas, ventanas, pestañas |

El **centro** muestra el logo del programa activo. Al elegir una burbuja muestra su icono y su nombre.

### Si vibra raro o no abre
El sensor del panel es de **fuerza** y puede rebotar (mandar varios toques seguidos); el anillo los filtra (0,14 s). Si en alguna zona del panel no abre, mira la tabla de problemas más abajo.

## 🧩 Qué hay en cada programa (el anillo)
Cada tabla es el anillo de ese programa. «Atajo» es lo que se ejecuta; si pone `noctalia msg …` es un comando del escritorio.
""")
    perfiles = [ap.GLOBAL] + ap.PERFILES
    vistos = set()
    for p in perfiles:
        if p["nombre"] in vistos:
            continue
        vistos.add(p["nombre"])
        extra = " (el de cualquier programa sin perfil propio)" if p is ap.GLOBAL else (
            " (también en las pestañas de Brave con YouTube)" if p["nombre"] == "YouTube" else "")
        a(f"### {p['nombre']}{extra}\n")
        a(tabla_anillo(p))
        a("")
    a("""## ⚙️ Cómo cambiar cosas

### Qué archivo toca qué

| Archivo | Qué contiene |
|---|---|
| `~/.config/hypr/scripts/mx-accion.py` | Gestos, Atrás, Adelante, Rueda, Superior y rueda del pulgar (tabla `PERFILES`) |
| `~/.config/hypr/scripts/anillo_apps.py` | Las 12 burbujas de cada programa, sub-opciones, colores e iconos |
| `~/.config/hypr/scripts/anillo.py` | El anillo en sí: tamaño, animación, vibración, tiempos |
| `~/.config/hypr/scripts/mx-reglas.py` | Reglas de Solaar (solo si cambian los botones, casi nunca) |
| `~/.config/hypr/scripts/mx-doc.py` | Genera este documento |
| `~/.local/state/mx-accion.log` | Registro de lo que se abre y ejecuta (para depurar) |

### Cómo se escribe una acción

| Escribes | Qué hace | Ejemplo |
|---|---|---|
| `"ctrl+t"` | Pulsa esa combinación | `"ctrl+shift+t"` |
| `["ctrl+l", "alt+return"]` | Varias combinaciones seguidas | duplicar pestaña |
| `("cmd", ["prog", "arg"])` | Ejecuta un programa | `("cmd", ["solaar"])` |
| `NOC("volume-up")` | Comando de Noctalia (volumen, brillo, notificaciones…) | `NOC("brightness-up")` |
| `SH("captura-guardar.sh")` | Script de `~/.config/hypr/scripts` | captura a carpeta |
| `web("claude")` | Abre o enfoca una app web (solo en `mx-accion.py`) | `web("gemini")` |

Las teclas se escriben en minúscula: `ctrl`, `shift`, `alt`, `super`, `return`, `esc`, `tab`, `space`, `left`, `pageup`, `delete`, `slash`, `comma`, `period`, `f1`…`f12`, `0`…`9`. Si usas una tecla nueva y no existe, el test te avisa.

### Receta 1 · Cambiar una burbuja del anillo
Abre `anillo_apps.py`, busca el programa y edita la línea. Cada burbuja es `S(icono, "Nombre", acción, sub=[…], rueda=(subir, bajar))`.

```python
S("browser-plus", "Nueva pestaña", "ctrl+t", color=VERDE),
```

### Receta 2 · Añadir sub-opciones a una burbuja
```python
S("search", "Buscar", "ctrl+f",
  sub=[S("filter", "Filtrar", "ctrl+i"),
       S("replace", "Reemplazar", "ctrl+h")]),
```
Pon entre 1 y 6 sub-opciones; salen abiertas en abanico.

### Receta 3 · Añadir un programa nuevo
1. Enfoca el programa y averigua su **clase**:

```bash
hyprctl activewindow | grep class
```

2. En `anillo_apps.py` copia un perfil (por ejemplo `KITTY`), cámbiale nombre, `logo` y las 12 burbujas.
3. Añádelo a la lista `PERFILES` del final con su clase. El primero que coincide gana, y se puede afinar por título con `"titulo"`.

```python
{"clase": r"^obsidian$", **OBSIDIAN},
```

### Receta 4 · Cambiar un gesto (Gestos, Atrás, Adelante…)
Abre `mx-accion.py`, busca el programa en `PERFILES` y edita la lista `[clic, arriba, abajo, izquierda, derecha]`. `None` = usa la del perfil global. Después actualiza el nombre en `NOMBRES` de `mx-doc.py` para que el documento lo diga bien.

### Receta 5 · Elegir otro icono
Los iconos son de la colección **Tabler** (casi 6000). Busca por palabra:

```bash
grep -i "camera" /usr/share/noctalia/assets/fonts/tabler.json | head
```

Usa el nombre sin más, por ejemplo `"camera"`. El color sale solo del icono; para forzarlo añade `color=ROJO` (colores: `ROJO NARANJA AMARILLO VERDE TURQUESA CIAN AZUL MORADO ROSA BLANCO`).

### Receta 6 · Probar y aplicar
```bash
# comprobar que los iconos y las teclas existen
python3 ~/.config/hypr/scripts/anillo-tests.py

# ver un programa sin tocar el mouse (6 s)
ANILLO_PRUEBA=1 ANILLO_APP=Brave python3 ~/.config/hypr/scripts/anillo.py --demonio

# aplicar los cambios del anillo
pkill -f "[a]nillo.py --demonio"; setsid python3 ~/.config/hypr/scripts/anillo.py --demonio &

# regenerar este documento
python3 ~/.config/hypr/scripts/mx-doc.py
```

Los gestos (`mx-accion.py`) se aplican solos: el archivo se lee en cada gesto.

## 🔧 Problemas típicos

| Síntoma | Causa | Solución |
|---|---|---|
| El anillo no abre | El servicio no corre | Mira el registro; reinícialo con el comando de la receta 6 |
| Abre a veces y a veces no | Rebote del sensor de fuerza del panel | Ya se filtra; si sigue, baja el umbral con `solaar config "MX Master 4" force-sensing N` |
| Una acción no hace nada | Atajo equivocado para ese programa | Abre `~/.local/state/mx-accion.log`, mira qué ejecutó y corrige la tecla |
| Salen mal los iconos | Fuente Tabler no encontrada | Comprueba que existe `/usr/share/noctalia/assets/fonts/noctalia-tabler.ttf` |
| Un gesto no responde | Solaar no corre | Debe estar corriendo (arranca con Hyprland): `solaar -w hide` |

📌 Nota: Solaar no puede guardar perfiles por programa en Wayland, por eso el script pregunta a Hyprland cuál es la ventana activa.

## 🔍 Para optimizar

### Acciones repetidas
Estas acciones están a la vez en el anillo y en un botón. Es duplicar esfuerzo: cambia una de las dos por algo que todavía no tengas a mano.

""")
    a(repetidos())
    a("""
### Por revisar
- **WhatsApp · Archivar chat**: dos fuentes dicen `Ctrl+Alt+E` y otras `Ctrl+Alt+Shift+E`; comprueba cuál funciona.
- **Telegram · Carpetas 1 a 4** (`Ctrl+1…4`): en Telegram también fijan chats; si chocan, usa Carpeta siguiente.
- **Brave · Duplicar pestaña**: es la combinación `Ctrl+L` y `Alt+Enter`; si no te gusta, quítala.
- **Gestos globales antiguos** (portapapeles, YouTube, terminal, archivos, WhatsApp): se quitaron de Gestos. Siguen en teclado: `Super+V`, `Super+Alt+Q`, `Super+Enter`, `Super+E`, `Super+Alt+W`.

### Ideas
- Poner en el anillo lo que más usas y quitar lo que no: el anillo cambia con `anillo_apps.py`, sin tocar nada más.
- Pasar al anillo los gestos que casi no usas, y dejar en los gestos solo lo imprescindible.
- Añadir perfiles para Obsidian, el editor de código o cualquier programa que uses a diario.
""")
    return "\n".join(t).replace("\n\n\n", "\n\n") + "\n"


def main():
    txt = documento()
    if problemas:
        print("⚠️  Revisa:\n  - " + "\n  - ".join(problemas), file=sys.stderr)
    for ruta in SALIDAS:
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w") as f:
            f.write(txt)
        print("escrito", ruta)
    r = subprocess.run([sys.executable, os.path.join(AQUI, "chuletas_md.py"), "validar", SALIDAS[1]],
                       capture_output=True, text=True)
    print((r.stdout + r.stderr).strip()[-600:])
    return 1 if problemas or r.returncode else 0


if __name__ == "__main__":
    sys.exit(main())
