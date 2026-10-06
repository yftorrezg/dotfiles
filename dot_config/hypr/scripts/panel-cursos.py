#!/usr/bin/env python3
"""Panel "Mis cursos": una nota de Obsidian con todos los cursos, sus clases y el progreso.

    panel-cursos.py [--base ~/Vídeos]
    panel-cursos.py --marcar "<carpeta de la clase>" hecha|sabida|pendiente   (lo usa estudiar.py)

Resultado: <base>/Mis cursos.md (la raíz de la bóveda "Vídeos"). Curso = carpeta capturas/
con INDICE.md (o con clases adentro), o carpeta suelta con apuntes.md (curso de una sola
clase). Por clase: una casilla "- [ ]" + links a apuntes, resumen y tarjetas.

Se regenera solo al terminar cada video/curso, así que respeta lo del usuario:
  - las casillas tildadas se conservan, reconocidas por la CARPETA de la clase (no por la
    posición): da igual que cambie el orden o aparezcan cursos nuevos;
  - la sección "## 📝 Mis notas" (del título hasta el final) se copia tal cual;
  - todo lo demás se reescribe.

Estados de una clase = la letra de su casilla (este archivo ES la fuente de verdad: lo que
tildás a mano en Obsidian y lo que marca estudiar.py conviven en el mismo lugar):
  - [ ]  pendiente
  - [x]  hecha: la estudiaste y practicaste (también "X")
  - [s]  sabida: la salteaste porque ya la sabías (pre-test de estudiar.py). Obsidian la
         dibuja tildada igual que [x], y el panel le agrega "⏭️ ya la sabía" para distinguirla.
Hechas + sabidas cuentan como completadas en el progreso. Para no pisarse con otro que regenera
a la vez (el final de cada video, o estudiar.py), leer → cambiar → escribir va con un candado.
Rápido (no llama a Claude) y nunca falla feo: ante un error avisa en una línea y sale con 0.
"""
import argparse
import os
import re
import sys

NOMBRE = "Mis cursos.md"
MARCA_NOTAS = "## 📝 Mis notas"
MARCAS = {"pendiente": " ", "hecha": "x", "sabida": "s"}  # estado → letra de la casilla


def estado_de(marca):
    """Letra de la casilla → 'hecha' | 'sabida' | 'pendiente' (cualquier otra letra = hecha,
    como la dibuja Obsidian: tildada)."""
    m = (marca or " ").lower()
    return "pendiente" if m == " " else "sabida" if m == "s" else "hecha"


def hms(seg):
    return f"{seg // 3600:d}:{seg % 3600 // 60:02d}:{seg % 60:02d}"


def duracion(carpeta):
    """Segundos de la línea **Duración:** de apuntes.md (None si no está)."""
    try:
        with open(os.path.join(carpeta, "apuntes.md"), encoding="utf-8") as f:
            m = re.search(r"\*\*Duración:\*\*\s*(\d+(?::\d+){1,2})", f.read(4000))
    except OSError:
        return None
    if not m:
        return None
    seg = 0
    for p in m.group(1).split(":"):
        seg = seg * 60 + int(p)
    return seg


def nombre_curso(carpeta_capturas):
    try:
        with open(os.path.join(carpeta_capturas, "INDICE.md"), encoding="utf-8") as f:
            nombre = f.readline().removeprefix("# 🎓 ").strip()
            if nombre:
                return nombre
    except OSError:
        pass
    return os.path.basename(os.path.dirname(carpeta_capturas))


def buscar_cursos(base):
    """[{nombre, carpeta, indice, clases: [carpeta, …]}] ordenados por nombre."""
    cursos = {}
    for raiz, dirs, archivos in os.walk(base):
        dirs[:] = sorted(d for d in dirs if not d.startswith("."))
        es_curso = "INDICE.md" in archivos and (os.path.basename(raiz) == "capturas"
                                               or any(os.path.exists(os.path.join(raiz, d, "apuntes.md")) for d in dirs))
        if es_curso:
            cursos.setdefault(raiz, {"clases": []})["indice"] = os.path.join(raiz, "INDICE.md")
        if "apuntes.md" not in archivos:
            continue
        arriba = os.path.dirname(raiz)
        if os.path.basename(arriba) == "capturas" or os.path.exists(os.path.join(arriba, "INDICE.md")):
            cursos.setdefault(arriba, {"clases": []})["clases"].append(raiz)   # clase de un curso
        else:
            cursos.setdefault(raiz, {"clases": []})["clases"].append(raiz)     # curso de una sola clase
    lista = []
    for carpeta, c in cursos.items():
        if c["clases"] == [carpeta]:
            try:
                with open(os.path.join(carpeta, "apuntes.md"), encoding="utf-8") as f:
                    nombre = f.readline().removeprefix("# 📓 ").strip()
            except OSError:
                nombre = ""
            c["nombre"] = nombre or os.path.basename(carpeta)
        else:
            c["nombre"] = nombre_curso(carpeta)
        c["carpeta"] = carpeta
        c["clases"].sort()
        lista.append(c)
    return sorted(lista, key=lambda c: c["nombre"].casefold())


def estado_viejo(texto, base):
    """({carpeta de clase (relativa a la base): marca de la casilla}, sección 'Mis notas' o None)."""
    notas = None
    if MARCA_NOTAS in texto:
        i = texto.index(MARCA_NOTAS)
        texto, notas = texto[:i], texto[i:].rstrip("\n")
    marcas = {}
    for linea in texto.splitlines():
        m = re.match(r"\s*[-*+] \[(.)\] (.*)", linea)
        if not m:
            continue
        # el primer link de la línea apunta a un archivo de la clase: su carpeta la identifica
        link = re.search(r"\]\(<([^>]+)>\)|\]\(([^)\s]+)\)|\[\[([^|\]]+)", m.group(2))
        if link:
            ruta = next(g for g in link.groups() if g)
            marcas[os.path.dirname(ruta.replace("%20", " "))] = m.group(1)
    return marcas, notas


def link(texto, ruta_rel):
    """Link Markdown relativo a la raíz de la bóveda. Con <…> sirven espacios, ：, ｜, (), ' …"""
    return f"[{texto}](<{ruta_rel}>)"


def barra(hechas, total, largo=10):
    llenas = round(largo * hechas / total) if total else 0
    return "▰" * llenas + "▱" * (largo - llenas)


def armar(base, cursos, marcas, notas):
    rel = lambda p: os.path.relpath(p, base)
    total_clases = sum(len(c["clases"]) for c in cursos)
    hechas_total, sabidas_total, seg_total, cuerpo = 0, 0, 0, []
    for c in cursos:
        lineas, hechas, sabidas, seg, sin_dur = [], 0, 0, 0, False
        for clase in c["clases"]:
            marca = marcas.get(rel(clase), " ")
            estado = estado_de(marca)
            hechas += estado == "hecha"
            sabidas += estado == "sabida"
            d = duracion(clase)
            seg += d or 0
            sin_dur |= d is None
            nombre = c["nombre"] if clase == c["carpeta"] else os.path.basename(clase)
            partes = [nombre.replace("[", "(").replace("]", ")")]
            if estado == "sabida":
                partes.append("⏭️ ya la sabía")
            if d:
                partes.append(f"⏱️ {hms(d)}")
            for archivo, texto in (("apuntes.md", "📓 Apuntes"), ("resumen.md", "⚡ Resumen"),
                                   ("tarjetas.md", "🃏 Tarjetas")):
                if os.path.exists(os.path.join(clase, archivo)):
                    partes.append(link(texto, rel(os.path.join(clase, archivo))))
            lineas.append(f"- [{marca}] " + " · ".join(partes))
        n = len(c["clases"])
        hechas_total += hechas
        sabidas_total += sabidas
        seg_total += seg
        pl = "s" if n != 1 else ""
        if sabidas:  # 12/166 clases completadas · ✅ 9 estudiadas · ⏭️ 3 ya sabidas
            info = [f"**Progreso:** {hechas + sabidas}/{n} clase{pl} completada{pl} · ✅ {hechas} "
                    f"estudiada{'s' if hechas != 1 else ''} · ⏭️ {sabidas} ya sabida{'s' if sabidas != 1 else ''} "
                    f"`{barra(hechas + sabidas, n)}`"]
        else:
            info = [f"**Progreso:** {hechas}/{n} clase{pl} estudiada{pl} `{barra(hechas, n)}`"]
        if seg:
            info.append(f"⏱️ {'≥ ' if sin_dur else ''}{hms(seg)}")
        if c.get("indice"):
            info.append(link("📋 Índice del curso", rel(c["indice"])))
        cuerpo += [f"## {c['nombre']}", "", " · ".join(info), ""]
        cuerpo += (lineas or ["*(todavía sin clases con apuntes)*"]) + [""]
    L = ["# 🎓 Mis cursos", "",
         "*Panel generado por panel-cursos.py (se rehace solo al terminar cada video o curso). "
         "Tildá cada clase al estudiarla: las casillas se conservan al regenerar (se reconocen por "
         "la carpeta de la clase). `[s]` = ⏭️ ya la sabías (la marca el Centro de estudio, "
         "estudiar.py). Todo lo demás se reescribe, salvo la sección «📝 Mis notas» del "
         "final, que nunca se toca. Los contadores se actualizan al regenerarse.*", ""]
    if sabidas_total:
        completas = f"✅ {hechas_total + sabidas_total}/{total_clases} completadas ({hechas_total} estudiadas · ⏭️ {sabidas_total} ya sabidas)"
    else:
        completas = f"✅ {hechas_total}/{total_clases} estudiadas"
    resumen = [f"📚 **{len(cursos)} curso{'s' if len(cursos) != 1 else ''}**",
               f"{total_clases} clases", completas]
    if seg_total:
        resumen.insert(2, f"⏱️ {hms(seg_total)} de video")
    L += ["> " + " · ".join(resumen), ""]
    if not cursos:
        L += ["*Todavía no hay cursos con apuntes.*", ""]
    L += cuerpo
    L += [notas or (MARCA_NOTAS + "\n\n*Escribí acá lo que quieras: esta sección no se regenera.*"), ""]
    return "\n".join(L)


class _Candado:
    """flock exclusivo mientras se lee-cambia-escribe el panel (dos procesos que regeneran a la
    vez perderían la casilla que marcó el otro). Va en XDG_RUNTIME_DIR: nada que ensucie la bóveda."""

    def __init__(self, base):
        import hashlib
        carpeta = os.environ.get("XDG_RUNTIME_DIR") or "/tmp"
        clave = hashlib.md5(base.encode()).hexdigest()[:12]
        self.ruta = os.path.join(carpeta, f"panel-cursos-{clave}.lock")

    def __enter__(self):
        import fcntl
        self.fd = os.open(self.ruta, os.O_CREAT | os.O_RDWR, 0o600)
        fcntl.flock(self.fd, fcntl.LOCK_EX)  # espera (regenerar tarda milisegundos)
        return self

    def __exit__(self, *_):
        os.close(self.fd)  # cerrar libera el flock


def generar(base, cambios=None):
    """Regenera el panel. cambios = {carpeta de la clase (absoluta o relativa a la base): estado
    ('hecha'|'sabida'|'pendiente') o letra de casilla}: se aplican sobre las casillas actuales."""
    base = os.path.abspath(os.path.expanduser(base))
    if not os.path.isdir(base):
        print(f"panel-cursos: no existe {base}")
        return None
    with _Candado(base):
        return _generar(base, cambios or {})


def _generar(base, cambios):
    salida = os.path.join(base, NOMBRE)
    viejo = ""
    try:
        with open(salida, encoding="utf-8") as f:
            viejo = f.read()
    except OSError:
        pass
    marcas, notas = estado_viejo(viejo, base)
    for clase, estado in cambios.items():
        ruta = os.path.relpath(os.path.abspath(os.path.expanduser(clase)), base)
        marcas[ruta] = MARCAS.get(estado, estado if len(estado) == 1 else " ")
    cursos = buscar_cursos(base)
    texto = armar(base, cursos, marcas, notas)
    if texto == viejo:
        print(f"🎓 Panel sin cambios: {salida}")
        return salida
    tmp = os.path.join(base, "." + NOMBRE + ".tmp")  # atómico: Obsidian puede estar mirándolo
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(texto)
    os.replace(tmp, salida)
    print(f"🎓 Panel con {len(cursos)} cursos: {salida}")
    return salida


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--base", default="~/Vídeos", help="raíz de la bóveda (por defecto ~/Vídeos)")
    p.add_argument("--marcar", nargs=2, metavar=("CLASE", "ESTADO"),
                   help="cambia el estado de una clase: hecha | sabida | pendiente")
    a = p.parse_args()
    cambios = {}
    if a.marcar:
        if a.marcar[1] not in MARCAS:
            print(f"panel-cursos: estado desconocido «{a.marcar[1]}» (hecha | sabida | pendiente)", file=sys.stderr)
            return 2
        cambios[a.marcar[0]] = a.marcar[1]
    try:
        generar(a.base, cambios)
    except Exception as e:  # es un extra: nunca cortar el script que lo llamó
        print(f"panel-cursos: no se pudo armar el panel ({type(e).__name__}: {e})", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
