#!/usr/bin/env python3
"""Centro de estudio: una ventana que te lleva de la mano por UNA clase a la vez.

    estudiar.py               abre la ventana (si ya está abierta, la trae al frente)
    estudiar.py --siguiente   abre la ventana en la próxima clase pendiente
    estudiar.py --terminar    marca la clase actual como hecha y avisa cuál sigue (sin ventana)
    estudiar.py --tests       corre los tests de práctica de la clase actual y avisa (sin ventana)
    estudiar.py --estado      imprime curso, clase actual y progreso (sin ventana)
    estudiar.py --repasar     abre en Obsidian el tarjetas.md con más para repasar (sin ventana)

El flujo de cada clase:
  1. 🤔 Pre-test "¿Ya lo sabés?": 3 preguntas de la clase. Pensás, mostrás la respuesta
     (Espacio) y te autoevaluás (1 = la sabía, 2 = no). 3/3 → la marcás como sabida y pasás a
     la siguiente sin verla. Así no perdés tiempo en lo que ya dominás.
  2. 📚 Estudiar: idea central + mapa de la clase a la vista, y botones grandes para ver el
     video, abrir resumen/apuntes, generar la práctica y correr sus tests.
  3. ✅ Terminé → queda hecha y aparece la siguiente.

Dónde vive cada cosa:
  - Estado de cada clase (pendiente / hecha / sabida): la casilla de ~/Vídeos/Mis cursos.md
    ([ ], [x], [s]). Es la única fuente de verdad: lo que tildás a mano en Obsidian y lo que
    marca esta ventana conviven. Se cambia con panel-cursos.generar(base, cambios).
  - "Clase actual" (la última abierta acá), curso elegido y fase: ~/.local/state/estudiar/estado.json
  - Práctica y tests: practica.py (otro script); si no está o falla, se avisa y nada más.

Variables de entorno (para las pruebas): ESTUDIAR_BASE (bóveda, por defecto ~/Vídeos),
ESTUDIAR_ESTADO (archivo de estado), ESTUDIAR_PRACTICA (ruta de practica.py),
ESTUDIAR_NOTIFICAR=0 (imprime en vez de notify-send).
"""
import contextlib
import datetime
import html
import importlib.util
import io
import json
import os
import re
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.abspath(os.path.expanduser(os.environ.get("ESTUDIAR_BASE", "~/Vídeos")))
ESTADO = os.path.expanduser(os.environ.get("ESTUDIAR_ESTADO", "~/.local/state/estudiar/estado.json"))
PRACTICA = os.environ.get("ESTUDIAR_PRACTICA", os.path.join(AQUI, "practica.py"))
ABRIR_MD = os.path.join(AQUI, "abrir-markdown.py")
APP_ID = "estudiar.centro"
N_PRETEST = 3
INACTIVA_MIN = 30  # oculta con Esc: el proceso queda vivo 30 min para reabrir al instante


def _cargar(nombre, archivo):
    spec = importlib.util.spec_from_file_location(nombre, os.path.join(AQUI, archivo))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


pc = _cargar("panel_cursos", "panel-cursos.py")  # buscar cursos, leer/cambiar casillas
_ta = None


def ta():
    """tarjetas.py (su parser del plugin Spaced Repetition), cargado solo si hace falta."""
    global _ta
    if _ta is None:
        _ta = _cargar("tarjetas_mod", "tarjetas.py")
    return _ta


# ------------------------------------------------------------------ datos ----
def leer_json(ruta):
    try:
        with open(ruta, encoding="utf-8") as f:
            d = json.load(f)
        return d if isinstance(d, (dict, list)) else {}
    except (OSError, ValueError):
        return {}


def cargar_estado():
    d = leer_json(ESTADO)
    return d if isinstance(d, dict) else {}


def guardar_estado(**cambios):
    """Mezcla los cambios en estado.json (escritura atómica). Devuelve el estado nuevo."""
    e = cargar_estado()
    e.update(cambios)
    os.makedirs(os.path.dirname(ESTADO), exist_ok=True)
    tmp = ESTADO + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(e, f, ensure_ascii=False, indent=1)
    os.replace(tmp, ESTADO)
    return e


def cursos(base=None):
    """Los cursos del panel que tienen al menos una clase con apuntes."""
    return [c for c in pc.buscar_cursos(base or BASE) if c["clases"]]


def leer_marcas(base=None):
    """{carpeta de clase relativa a la base: letra de la casilla} de Mis cursos.md."""
    base = base or BASE
    try:
        with open(os.path.join(base, pc.NOMBRE), encoding="utf-8") as f:
            texto = f.read()
    except OSError:
        return {}
    return pc.estado_viejo(texto, base)[0]


def estado_clase(clase, marcas, base=None):
    """'pendiente' | 'hecha' | 'sabida'."""
    return pc.estado_de(marcas.get(os.path.relpath(clase, base or BASE), " "))


def marcar(clase, estado, base=None):
    """Cambia la casilla de la clase en Mis cursos.md (regenera el panel con candado)."""
    with contextlib.redirect_stdout(io.StringIO()):  # el panel imprime una línea: acá sobra
        pc.generar(base or BASE, {clase: estado})


def progreso(curso, marcas, base=None):
    cuenta = {"pendiente": 0, "hecha": 0, "sabida": 0}
    for c in curso["clases"]:
        cuenta[estado_clase(c, marcas, base)] += 1
    cuenta["total"] = len(curso["clases"])
    return cuenta


def texto_progreso(p):
    """12/166 · ✅ 9 estudiadas · ⏭️ 3 ya sabidas"""
    return (f"{p['hecha'] + p['sabida']}/{p['total']} · ✅ {p['hecha']} estudiada{'s' if p['hecha'] != 1 else ''}"
            f" · ⏭️ {p['sabida']} ya sabida{'s' if p['sabida'] != 1 else ''}")


def proxima(curso, marcas, base=None):
    """Primera clase EN ORDEN que no está hecha ni sabida (None si el curso está completo)."""
    return next((c for c in curso["clases"] if estado_clase(c, marcas, base) == "pendiente"), None)


def elegir_curso(lista, estado):
    """El último usado; si no hay (o ya no existe), el curso con más clases."""
    for c in lista:
        if c["carpeta"] == estado.get("curso"):
            return c
    return max(lista, key=lambda c: len(c["clases"])) if lista else None


def clase_a_mostrar(curso, estado, marcas, base=None):
    """La clase actual guardada si sigue pendiente; si no, la próxima pendiente."""
    actual = estado.get("clase")
    if actual in curso["clases"] and estado_clase(actual, marcas, base) == "pendiente":
        return actual
    return proxima(curso, marcas, base)


def curso_de_clase(clase, lista):
    return next((c for c in lista if clase in c["clases"]), None)


def numero(clase, curso):
    """(posición 1..N, N)"""
    return curso["clases"].index(clase) + 1, len(curso["clases"])


def _sufijo_comun(curso):
    """Firma repetida al final de casi todas las clases (" - #jonmircha") para no mostrarla."""
    finales = {}
    for c in curso["clases"]:
        partes = os.path.basename(c).rsplit(" - ", 1)
        if len(partes) == 2 and len(partes[1]) < 30:
            finales[partes[1]] = finales.get(partes[1], 0) + 1
    if not finales or len(curso["clases"]) < 3:
        return None
    fin, n = max(finales.items(), key=lambda kv: kv[1])
    return fin if n >= 0.6 * len(curso["clases"]) else None


def titulo_corto(clase, curso):
    """'004 - Curso JavaScript- 3. Variables- var 🥊VS🥊 let - #jonmircha' → '3. Variables- var 🥊VS🥊 let'.
    Saca el número, el nombre del curso repetido al principio y la firma repetida al final."""
    t = os.path.basename(clase)
    if clase == curso["carpeta"]:
        return curso["nombre"]
    t = re.sub(r"^\d{1,4}\s*-\s*", "", t)
    fin = _sufijo_comun(curso)
    if fin and t.endswith(" - " + fin):
        t = t[: -len(fin) - 3]
    nombre = curso["nombre"]
    if t.casefold().startswith(nombre.casefold()):
        resto = t[len(nombre):].lstrip(" -:：|｜.")
        if len(resto) > 3:
            t = resto
    return t.strip() or os.path.basename(clase)


def _texto(v):
    return v.strip() if isinstance(v, str) else ""


def preguntas_pretest(clase, n=N_PRETEST):
    """[(pregunta, respuesta)] para el pre-test. Primero las preguntas del resumen (repartidas:
    primera, del medio y última, así cubren toda la clase); si faltan, conceptos de los apuntes
    como '¿Qué es X?' (los de definición más larga: los triviales no sirven para decidir)."""
    corto = leer_json(os.path.join(clase, ".resumen-ia.json"))
    preg = [(_texto(p.get("pregunta")), _texto(p.get("respuesta")))
            for p in (corto.get("preguntas") or []) if isinstance(p, dict)] if isinstance(corto, dict) else []
    preg = [p for p in preg if p[0] and p[1]]
    if len(preg) > n:
        idx = sorted({round(i * (len(preg) - 1) / (n - 1)) for i in range(n)}) if n > 1 else [0]
        preg = [preg[i] for i in idx]
    if len(preg) < n:
        largo = leer_json(os.path.join(clase, ".apuntes-ia.json"))
        conceptos = [(_texto(c.get("termino")), _texto(c.get("definicion")))
                     for c in (largo.get("conceptos") or []) if isinstance(c, dict)] if isinstance(largo, dict) else []
        conceptos = [c for c in conceptos if c[0] and len(c[1]) >= 25]
        conceptos.sort(key=lambda c: -len(c[1]))
        for termino, definicion in conceptos[: n - len(preg)]:
            preg.append((f"¿Qué es **{termino}**?", definicion))
    return preg[:n]


def youtube_url(clase):
    try:
        with open(os.path.join(clase, ".youtube-id"), encoding="utf-8") as f:
            vid = f.read().strip()
    except OSError:
        return None
    return f"https://www.youtube.com/watch?v={vid}" if re.fullmatch(r"[\w-]{6,20}", vid) else None


VIDEOS = (".mp4", ".mkv", ".webm", ".mov", ".avi", ".m4v")


def video_local(clase):
    """El video de la clase si está descargado: <curso>/<nombre de la clase>[.es].mp4 (prefiere
    el doblado .es), o un video dentro de la carpeta de la clase."""
    nombre = os.path.basename(clase)
    candidatos = []
    for carpeta in (os.path.dirname(os.path.dirname(clase)), os.path.dirname(clase), clase):
        try:
            archivos = os.listdir(carpeta)
        except OSError:
            continue
        for a in archivos:
            if not a.lower().endswith(VIDEOS) or a.endswith(".part"):
                continue
            tallo = a.rsplit(".", 1)[0]
            if carpeta == clase or tallo == nombre or tallo.removesuffix(".es") == nombre:
                candidatos.append((not tallo.endswith(".es"), os.path.join(carpeta, a)))
    return min(candidatos)[1] if candidatos else None


def info_clase(clase):
    corto = leer_json(os.path.join(clase, ".resumen-ia.json"))
    corto = corto if isinstance(corto, dict) else {}
    mapa = [(_texto(m.get("inicio")), _texto(m.get("tema"))) for m in corto.get("mapa") or [] if isinstance(m, dict)]
    return {"idea": _texto(corto.get("idea")), "mapa": [m for m in mapa if m[1]],
            "esencial": [_texto(e) for e in corto.get("esencial") or [] if _texto(e)],
            "youtube": youtube_url(clase), "video": video_local(clase)}


_FECHA_SR = re.compile(r"!(?:fsrs,)?(\d{4}-\d{2}-\d{2})")


def tarjetas_pendientes(curso, marcas, base=None, hoy=None):
    """Tarjetas para repasar hoy en el curso:
    vencidas = las que ya tienen progreso del plugin (<!--SR:!AAAA-MM-DD,…-->) con fecha <= hoy
               (en cualquier clase: si las repasaste alguna vez, te tocan);
    nuevas   = sin progreso todavía, pero solo de clases hechas o sabidas (las de clases que
               no viste no cuentan: no tiene sentido repasar lo que no estudiaste).
    Devuelve {vencidas, nuevas, archivo}: archivo = el tarjetas.md con más para repasar."""
    hoy = hoy or datetime.date.today().isoformat()
    total_venc = total_nuev = 0
    mejor, mejor_n = None, 0
    for clase in curso["clases"]:
        ruta = os.path.join(clase, "tarjetas.md")
        try:
            with open(ruta, encoding="utf-8") as f:
                texto = f.read()
        except OSError:
            continue
        vista = estado_clase(clase, marcas, base) != "pendiente"
        venc = nuev = 0
        for _, t, _, _ in ta().parsear(texto):
            fechas = _FECHA_SR.findall(t)
            if fechas:
                venc += min(fechas) <= hoy
            elif vista:
                nuev += 1
        total_venc += venc
        total_nuev += nuev
        if venc + nuev > mejor_n:
            mejor, mejor_n = ruta, venc + nuev
    return {"vencidas": total_venc, "nuevas": total_nuev, "archivo": mejor}


def resultado_practica(clase):
    """Lee practica/.resultado.json (lo escribe practica.py --correr; formato en su docstring:
    {"ok", "total", "ejercicios": [{"id", "nombre", "titulo", "ok", "pasan", "tests", "error"}]}).
    Tolerante por si cambia: también una lista, o {nombre: bool}.
    Devuelve [(nombre, ok, detalle)] o None si no hay resultado."""
    d = leer_json(os.path.join(clase, "practica", ".resultado.json"))
    if not d:
        return None
    items = d
    if isinstance(d, dict):
        items = next((d[k] for k in ("ejercicios", "resultados", "tests", "pruebas") if k in d), d)
    filas = []
    if isinstance(items, dict):
        items = [{"nombre": k, "ok": v} for k, v in items.items()]
    for i, e in enumerate(items if isinstance(items, list) else []):
        if not isinstance(e, dict):
            continue
        nombre = next((str(e[k]) for k in ("titulo", "nombre", "ejercicio", "archivo") if e.get(k)), f"Ejercicio {i + 1}")
        if e.get("id") and str(e["id"]) not in nombre:
            nombre = f"{e['id']} · {nombre}"
        if isinstance(e.get("pasan"), int) and isinstance(e.get("tests"), int):
            nombre += f"  ({e['pasan']}/{e['tests']} tests)"
        ok = next((e[k] for k in ("ok", "paso", "pasa", "aprobado", "passed") if k in e), None)
        if ok is None and "estado" in e:
            ok = str(e["estado"]).lower() in ("ok", "pasa", "paso", "aprobado", "passed", "✅")
        if isinstance(ok, dict):
            continue
        detalle = next((str(e[k]) for k in ("mensaje", "detalle", "error", "salida") if e.get(k)), "")
        filas.append((nombre, bool(ok), detalle))
    return filas or None


# ------------------------------------------------------------------ acciones ----
def notificar(titulo, cuerpo="", urgente=False):
    if os.environ.get("ESTUDIAR_NOTIFICAR") == "0":
        print(f"[notificación] {titulo} · {cuerpo}")
        return
    cmd = ["notify-send", "-a", "Centro de estudio", "-t", "8000"] + (["-u", "critical"] if urgente else [])
    try:
        subprocess.run(cmd + [titulo, cuerpo], timeout=5)
    except (OSError, subprocess.SubprocessError):
        print(f"{titulo} · {cuerpo}")


def abrir_md(ruta):
    """Obsidian si está en una bóveda, si no VS Code (lo decide abrir-markdown.py)."""
    subprocess.Popen([sys.executable, ABRIR_MD, ruta], start_new_session=True,
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def abrir(cmd):
    try:
        subprocess.Popen(cmd, start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except OSError:
        return False


def contexto(base=None):
    """(estado, cursos, curso, clase actual, marcas) resueltos para la CLI."""
    base = base or BASE
    estado, lista, marcas = cargar_estado(), cursos(base), leer_marcas(base)
    clase = estado.get("clase")
    curso = curso_de_clase(clase, lista) if clase else None
    if not curso:
        curso = elegir_curso(lista, estado)
        clase = clase_a_mostrar(curso, estado, marcas, base) if curso else None
    return estado, lista, curso, clase, marcas


def describir(clase, curso):
    i, n = numero(clase, curso)
    return f"Clase {i}/{n}: {titulo_corto(clase, curso)}"


def cli_estado(base=None):
    base = base or BASE
    _, _, curso, clase, marcas = contexto(base)
    if not curso:
        print("📭 No hay cursos con apuntes todavía.")
        return 1
    p = progreso(curso, marcas, base)
    print(f"📚 {curso['nombre']}")
    if clase:
        print(f"📍 {describir(clase, curso)} ({estado_clase(clase, marcas, base)})")
    else:
        print("🎉 Curso completo: no quedan clases pendientes")
    print(f"📊 {texto_progreso(p)}")
    t = tarjetas_pendientes(curso, marcas, base)
    print(f"🃏 {t['vencidas']} tarjetas vencidas · {t['nuevas']} nuevas")
    return 0


def cli_terminar(base=None):
    base = base or BASE
    _, _, curso, clase, _ = contexto(base)
    if not clase:
        notificar("🎓 Centro de estudio", "No hay una clase actual para terminar")
        return 1
    ya = estado_clase(clase, leer_marcas(base), base)
    if ya == "pendiente":
        marcar(clase, "hecha", base)
    marcas = leer_marcas(base)
    siguiente = proxima(curso, marcas, base)
    guardar_estado(curso=curso["carpeta"], clase=siguiente, fase="pretest")
    p = progreso(curso, marcas, base)
    cabeza = (f"✅ Terminaste: {titulo_corto(clase, curso)}" if ya == "pendiente" else
              f"{'✅' if ya == 'hecha' else '⏭️'} «{titulo_corto(clase, curso)}» ya estaba {ya}")
    if siguiente:
        notificar(cabeza,
                  f"Sigue → {describir(siguiente, curso)}\n{texto_progreso(p)}")
    else:
        notificar(f"🎉 ¡Curso completo! {curso['nombre']}", f"{cabeza}\n{texto_progreso(p)}")
    return 0


def cli_tests(base=None):
    _, _, curso, clase, _ = contexto(base)
    if not clase:
        notificar("🧪 Tests", "No hay una clase actual", urgente=True)
        return 1
    if not os.path.exists(PRACTICA):
        notificar("🧪 Tests", "practica.py todavía no está instalado", urgente=True)
        return 1
    if not os.path.isdir(os.path.join(clase, "practica")):
        notificar("🧪 Tests", f"Primero generá la práctica de {titulo_corto(clase, curso)} (botón 🏋️ del Centro de estudio)")
        return 1
    return subprocess.run([sys.executable, PRACTICA, "--correr", clase, "--notificar"]).returncode


def cli_repasar(base=None):
    """Abre en Obsidian el tarjetas.md con más para repasar (o el de la clase actual)."""
    _, _, curso, clase, marcas = contexto(base)
    t = tarjetas_pendientes(curso, marcas, base) if curso else {}
    ruta = t.get("archivo") or (os.path.join(clase, "tarjetas.md") if clase else None)
    if not ruta or not os.path.exists(ruta):
        notificar("🃏 Repasar", "No hay tarjetas para repasar todavía (se cuentan las de clases hechas o sabidas)")
        return 1
    abrir_md(ruta)
    n = t.get("vencidas", 0) + t.get("nuevas", 0)
    notificar("🃏 Repasar", (f"{n} tarjetas para hoy. " if n else "") + "En Obsidian: Ctrl+P → «Revisar tarjetas»")
    return 0


# ------------------------------------------------------------------ ventana ----
CSS = """
window.estudiar { background: #15171c; color: #e8eaef; }
window.estudiar headerbar { background: #15171c; box-shadow: none; border-bottom: 1px solid #23262e; min-height: 46px; }
.contenido { padding: 20px 28px 16px 28px; }
.eyebrow { font-size: 10pt; font-weight: 700; letter-spacing: 1px; color: #8a93a4; }
.titulo-clase { font-size: 20pt; font-weight: 800; color: #f3f5f9; }
.chip { border-radius: 999px; padding: 2px 11px; font-size: 9.5pt; font-weight: 700; }
.chip.pendiente { background: #262a33; color: #b9c0cc; }
.chip.hecha { background: rgba(74,222,128,0.14); color: #74e3a0; }
.chip.sabida { background: rgba(110,168,254,0.15); color: #93bcff; }
.muted { color: #8a93a4; }
.progreso-texto { color: #a9b1bf; font-size: 10.5pt; }
.tarjeta { background: #1c1f26; border-radius: 14px; padding: 18px 20px; border: 1px solid #272b34; }
.seccion { font-size: 12.5pt; font-weight: 700; color: #e8eaef; }
.pregunta { font-size: 16pt; font-weight: 600; color: #f3f5f9; }
.respuesta { font-size: 12.5pt; color: #cfd5df; }
.idea { font-size: 13pt; color: #eef1f6; }
.mapa-min { font-family: monospace; color: #7fa6e8; font-size: 10.5pt; }
.mapa-tema { color: #c9cfda; font-size: 11pt; }
.puntaje { font-size: 44pt; font-weight: 800; }
.puntaje.bien { color: #74e3a0; }
.puntaje.mas-o-menos { color: #f3c969; }
.puntaje.mal { color: #f28b82; }
.mensaje { font-size: 13pt; color: #cfd5df; }
.punto { font-size: 13pt; color: #3a404c; }
.punto.actual { color: #8a93a4; }
.punto.si { color: #74e3a0; }
.punto.no { color: #f28b82; }
button.grande { min-height: 52px; border-radius: 12px; font-size: 12pt; font-weight: 600; background: #22262f;
                color: #e8eaef; border: 1px solid #2d323d; box-shadow: none; padding: 0 16px; }
button.grande:hover { background: #2a2f3a; }
button.grande:focus-visible { outline: 2px solid #6ea8fe; }
button.primario { background: #3565c9; border-color: #4476dc; color: #ffffff; }
button.primario:hover { background: #3d70d8; }
button.exito { background: #1e6b43; border-color: #26804f; color: #ffffff; }
button.exito:hover { background: #237a4d; }
button.peligro { background: #5a2a2a; border-color: #6d3434; }
button.peligro:hover { background: #683131; }
button.chico { min-height: 30px; border-radius: 8px; font-size: 10pt; background: transparent; color: #a9b1bf;
               border: 1px solid #2d323d; box-shadow: none; padding: 0 12px; }
button.chico:hover { background: #22262f; }
.tecla { font-family: monospace; font-size: 9pt; font-weight: 600; background: rgba(255,255,255,0.08);
         border-radius: 6px; padding: 1px 7px; color: #b3bac6; }
button.primario .tecla, button.exito .tecla { background: rgba(255,255,255,0.18); color: #ffffff; }
.salida { font-size: 11pt; color: #cfd5df; }
.aviso { background: #2b3040; color: #e8eaef; border-radius: 12px; padding: 8px 10px 8px 16px; border: 1px solid #3a4152; }
.pie { font-size: 9.5pt; color: #6f7788; }
"""


def md_pango(texto):
    """Markdown mínimo → Pango: `código`, **negrita**, y el resto escapado."""
    t = html.escape(texto, quote=False)
    t = re.sub(r"`([^`]+)`", r"<tt>\1</tt>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)
    return t


def gui():
    import gi
    gi.require_version("Gtk", "4.0")
    try:
        gi.require_version("Adw", "1")
        from gi.repository import Adw
    except (ValueError, ImportError):
        Adw = None
    from gi.repository import Gdk, Gio, GLib, Gtk, Pango

    def etiqueta(texto="", clases=(), xalign=0.0, wrap=True, markup=False, **kw):
        lbl = Gtk.Label(xalign=xalign, wrap=wrap, **kw)
        if wrap:
            lbl.set_wrap_mode(Pango.WrapMode.WORD_CHAR)
        (lbl.set_markup if markup else lbl.set_text)(texto)
        for c in clases:
            lbl.add_css_class(c)
        return lbl

    def boton(texto, tecla, al_click, clases=("grande",)):
        """Botón grande: 'emoji + texto' a la izquierda y la tecla a la derecha."""
        b = Gtk.Button()
        caja = Gtk.Box(spacing=10)
        lbl = etiqueta(texto, wrap=False, hexpand=True, ellipsize=Pango.EllipsizeMode.END)
        caja.append(lbl)
        b.tecla = etiqueta(tecla, ("tecla",), wrap=False, valign=Gtk.Align.CENTER)
        b.tecla.set_visible(bool(tecla))
        caja.append(b.tecla)
        b.set_child(caja)
        b.texto = lbl
        for c in clases:
            b.add_css_class(c)
        b.connect("clicked", lambda *_: al_click())
        return b

    class Centro:
        def __init__(self, app):
            self.app = app
            self.lista, self.marcas, self.curso, self.clase = [], {}, None, None
            self.preguntas, self.i_preg, self.respuestas = [], 0, []
            self.deshacer = None      # (texto, función) de la última marca
            self.procesos = {}        # clase → "practica" | "tests" corriendo
            self.salidas = {}         # clase → texto del último resultado de práctica/tests
            self.t_cierre = None

            win = (Adw.ApplicationWindow if Adw else Gtk.ApplicationWindow)(application=app)
            self.win = win
            win.set_title("Centro de estudio")
            win.set_default_size(760, 760)
            win.add_css_class("estudiar")
            win.set_hide_on_close(True)  # cerrar = ocultar: reabrir es instantáneo
            win.connect("hide", lambda *_: self._programar_salida())

            # --- cabecera: selector de curso + tarjetas para repasar
            cab = Gtk.HeaderBar()
            self.selector = Gtk.DropDown.new_from_strings([])
            self.selector.set_tooltip_text("Cambiar de curso")
            self.id_selector = self.selector.connect("notify::selected", self._al_elegir_curso)
            cab.set_title_widget(self.selector)
            self.btn_tarjetas = Gtk.Button(label="🃏 Repasar")
            self.btn_tarjetas.add_css_class("chico")
            self.btn_tarjetas.set_tooltip_text("Abrir las tarjetas en Obsidian (tecla K) · Ctrl+P → «Revisar tarjetas»")
            self.btn_tarjetas.connect("clicked", lambda *_: self.repasar())
            cab.pack_end(self.btn_tarjetas)
            ico = etiqueta("🎓 Centro de estudio", ("muted",), wrap=False)
            cab.pack_start(ico)

            # --- contenido
            raiz = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
            raiz.add_css_class("contenido")

            self.lbl_eyebrow = etiqueta("", ("eyebrow",), wrap=False, ellipsize=Pango.EllipsizeMode.END)
            fila_tit = Gtk.Box(spacing=12)
            self.lbl_titulo = etiqueta("", ("titulo-clase",), hexpand=True)
            self.lbl_titulo.set_lines(3)
            self.lbl_titulo.set_ellipsize(Pango.EllipsizeMode.END)
            self.chip = etiqueta("", ("chip",), wrap=False, valign=Gtk.Align.START)
            fila_tit.append(self.lbl_titulo)
            fila_tit.append(self.chip)
            self.barra = Gtk.DrawingArea(content_height=8, hexpand=True)
            self.barra.set_draw_func(self._dibujar_barra)
            self.lbl_progreso = etiqueta("", ("progreso-texto",), wrap=False)
            cabeza = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
            for w in (self.lbl_eyebrow, fila_tit, self.barra, self.lbl_progreso):
                cabeza.append(w)
            raiz.append(cabeza)

            self.pila = Gtk.Stack(transition_type=Gtk.StackTransitionType.CROSSFADE, transition_duration=120,
                                  vexpand=True, vhomogeneous=False, margin_top=8)
            self.pila.add_named(self._pagina_pretest(), "pretest")
            self.pila.add_named(self._pagina_resultado(), "resultado")
            self.pila.add_named(self._pagina_estudiar(), "estudiar")
            self.pila.add_named(self._pagina_vacia(), "vacia")
            raiz.append(self.pila)

            pie = Gtk.Box(spacing=10)
            self.lbl_pie = etiqueta("← → otra clase · K tarjetas · Esc cerrar", ("pie",), wrap=False, hexpand=True)
            self.btn_pendiente = Gtk.Button(label="↩ Volver a pendiente")
            self.btn_pendiente.add_css_class("chico")
            self.btn_pendiente.connect("clicked", lambda *_: self.cambiar_estado(self.clase, "pendiente"))
            pie.append(self.lbl_pie)
            pie.append(self.btn_pendiente)
            raiz.append(pie)

            scroll = Gtk.ScrolledWindow(hscrollbar_policy=Gtk.PolicyType.NEVER)
            scroll.set_child(raiz)
            self.scroll = scroll

            # aviso inferior ("Marcada como sabida · Deshacer")
            capa = Gtk.Overlay()
            capa.set_child(scroll)
            self.aviso = Gtk.Revealer(transition_type=Gtk.RevealerTransitionType.SLIDE_UP,
                                      valign=Gtk.Align.END, halign=Gtk.Align.CENTER, margin_bottom=18)
            caja_aviso = Gtk.Box(spacing=12)
            caja_aviso.add_css_class("aviso")
            self.lbl_aviso = etiqueta("", wrap=False, valign=Gtk.Align.CENTER)
            self.btn_deshacer = Gtk.Button(label="Deshacer  Ctrl+Z")
            self.btn_deshacer.add_css_class("chico")
            self.btn_deshacer.connect("clicked", lambda *_: self.hacer_deshacer())
            caja_aviso.append(self.lbl_aviso)
            caja_aviso.append(self.btn_deshacer)
            self.aviso.set_child(caja_aviso)
            capa.add_overlay(self.aviso)

            if Adw:
                vista = Adw.ToolbarView()
                vista.add_top_bar(cab)
                vista.set_content(capa)
                win.set_content(vista)
            else:
                win.set_titlebar(cab)
                win.set_child(capa)

            teclas = Gtk.EventControllerKey()
            teclas.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
            teclas.connect("key-pressed", self._tecla)
            win.add_controller(teclas)

            # si otro proceso cambia el panel (Obsidian, --terminar, fin de un video) o el estado
            self.monitores = []
            for ruta in (os.path.join(BASE, pc.NOMBRE), ESTADO):
                os.makedirs(os.path.dirname(ruta), exist_ok=True)
                m = Gio.File.new_for_path(ruta).monitor_file(Gio.FileMonitorFlags.NONE, None)
                m.connect("changed", self._al_cambiar_archivo)
                self.monitores.append(m)
            self.t_recarga = None

        # ---------------- páginas
        def _pagina_pretest(self):
            p = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
            fila = Gtk.Box(spacing=10)
            fila.append(etiqueta("🤔 ¿Ya lo sabés?", ("seccion",), wrap=False, hexpand=True))
            self.lbl_n_preg = etiqueta("", ("muted",), wrap=False)
            fila.append(self.lbl_n_preg)
            self.puntos = Gtk.Box(spacing=4)
            fila.append(self.puntos)
            p.append(fila)

            t = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
            t.add_css_class("tarjeta")
            self.lbl_pregunta = etiqueta("", ("pregunta",), markup=True, selectable=False)
            t.append(self.lbl_pregunta)
            self.rev_respuesta = Gtk.Revealer(transition_type=Gtk.RevealerTransitionType.SLIDE_DOWN, transition_duration=150)
            caja = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            caja.append(Gtk.Separator())
            self.lbl_respuesta = etiqueta("", ("respuesta",), markup=True)
            caja.append(self.lbl_respuesta)
            self.rev_respuesta.set_child(caja)
            t.append(self.rev_respuesta)
            p.append(t)

            self.pila_botones = Gtk.Stack(vhomogeneous=True)
            self.btn_mostrar = boton("👀  Mostrar respuesta", "Espacio", self.mostrar_respuesta, ("grande", "primario"))
            self.pila_botones.add_named(self.btn_mostrar, "mostrar")
            dos = Gtk.Box(spacing=12, homogeneous=True)
            dos.append(boton("✅  La sabía", "1", lambda: self.autoevaluar(True), ("grande", "exito")))
            dos.append(boton("❌  No la sabía", "2", lambda: self.autoevaluar(False), ("grande", "peligro")))
            self.pila_botones.add_named(dos, "evaluar")
            p.append(self.pila_botones)

            abajo = Gtk.Box(spacing=10)
            abajo.append(etiqueta("Pensá la respuesta antes de mostrarla. Si sabés las 3, salteás la clase.",
                                  ("muted",), hexpand=True))
            saltar = Gtk.Button(label="Saltear → estudiar  (S)")
            saltar.add_css_class("chico")
            saltar.connect("clicked", lambda *_: self.ir_a_estudiar())
            abajo.append(saltar)
            p.append(abajo)
            return p

        def _pagina_resultado(self):
            p = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16, valign=Gtk.Align.START)
            t = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
            t.add_css_class("tarjeta")
            self.lbl_puntaje = etiqueta("", ("puntaje",), xalign=0.5, wrap=False)
            self.lbl_mensaje = etiqueta("", ("mensaje",), xalign=0.5)
            self.lbl_mensaje.set_justify(Gtk.Justification.CENTER)
            t.append(self.lbl_puntaje)
            t.append(self.lbl_mensaje)
            p.append(t)
            self.btn_res_1 = boton("", "Enter", lambda: self._accion_res(0), ("grande", "primario"))
            self.btn_res_2 = boton("", "E", lambda: self._accion_res(1))
            p.append(self.btn_res_1)
            p.append(self.btn_res_2)
            self.acciones_res = []
            return p

        def _pagina_estudiar(self):
            p = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
            t = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            t.add_css_class("tarjeta")
            t.append(etiqueta("💡 En una frase", ("seccion",), wrap=False))
            self.lbl_idea = etiqueta("", ("idea",), markup=True)
            t.append(self.lbl_idea)
            self.caja_mapa_tit = etiqueta("🗺️ Mapa de la clase", ("seccion",), wrap=False, margin_top=6)
            t.append(self.caja_mapa_tit)
            self.grilla_mapa = Gtk.Grid(column_spacing=14, row_spacing=4)
            t.append(self.grilla_mapa)
            p.append(t)

            g = Gtk.Grid(column_spacing=12, row_spacing=12, column_homogeneous=True)
            self.btn_ver = boton("▶️  Ver la clase", "V", self.ver_clase)
            self.btn_resumen = boton("⚡  Resumen", "R", lambda: self.abrir_archivo("resumen.md"))
            self.btn_apuntes = boton("📓  Apuntes", "A", lambda: self.abrir_archivo("apuntes.md"))
            self.btn_practica = boton("🏋️  Práctica", "P", self.practica)
            self.btn_tests = boton("🧪  Correr tests", "T", self.correr_tests)
            self.btn_terminar = boton("✅  Terminé esta clase", "Ctrl+Enter", self.terminar, ("grande", "exito"))
            for i, b in enumerate((self.btn_ver, self.btn_resumen, self.btn_apuntes, self.btn_practica, self.btn_tests)):
                g.attach(b, i % 2, i // 2, 1, 1)
            g.attach(self.btn_terminar, 1, 2, 1, 1)
            p.append(g)

            self.caja_salida = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
            self.caja_salida.add_css_class("tarjeta")
            self.lbl_salida = etiqueta("", ("salida",), markup=True, selectable=True)
            self.caja_salida.append(self.lbl_salida)
            p.append(self.caja_salida)
            return p

        def _pagina_vacia(self):
            p = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14, valign=Gtk.Align.CENTER)
            self.lbl_vacia = etiqueta("", ("mensaje",), xalign=0.5)
            self.lbl_vacia.set_justify(Gtk.Justification.CENTER)
            p.append(self.lbl_vacia)
            return p

        # ---------------- carga de datos
        def recargar(self, clase=None):
            """Relee cursos, casillas y estado; muestra `clase` (o la que corresponda)."""
            self.lista = cursos()
            self.marcas = leer_marcas()
            estado = cargar_estado()
            if clase:
                self.curso = curso_de_clase(clase, self.lista)
            else:
                self.curso = elegir_curso(self.lista, estado)
                clase = clase_a_mostrar(self.curso, estado, self.marcas) if self.curso else None
            self._llenar_selector()
            if clase and clase == self.clase and self.pila.get_visible_child_name() != "vacia":
                self._pintar_cabeza()  # misma clase (reabrir tras Esc): seguir donde estaba
                return
            self.mostrar_clase(clase)

        def _llenar_selector(self):
            self.selector.handler_block(self.id_selector)
            nombres = [(c["nombre"] if len(c["nombre"]) <= 44 else c["nombre"][:43] + "…") for c in self.lista]
            self.selector.set_model(Gtk.StringList.new(nombres))
            if self.curso in self.lista:
                self.selector.set_selected(self.lista.index(self.curso))
            self.selector.handler_unblock(self.id_selector)

        def _al_elegir_curso(self, *_):
            i = self.selector.get_selected()
            if 0 <= i < len(self.lista) and self.lista[i] is not self.curso:
                self.curso = self.lista[i]
                guardar_estado(curso=self.curso["carpeta"])
                self.mostrar_clase(clase_a_mostrar(self.curso, cargar_estado(), self.marcas))

        def _al_cambiar_archivo(self, _m, _f, _o, evento):
            if evento not in (Gio.FileMonitorEvent.CHANGES_DONE_HINT, Gio.FileMonitorEvent.CREATED,
                              Gio.FileMonitorEvent.RENAMED, Gio.FileMonitorEvent.MOVED_IN):
                return
            if self.t_recarga:
                GLib.source_remove(self.t_recarga)
            self.t_recarga = GLib.timeout_add(250, self._recarga_externa)

        def _recarga_externa(self):
            """Cambió Mis cursos.md o estado.json desde afuera: refrescar sin perder el pre-test
            en curso; si --terminar/--siguiente cambió la clase actual, mostrar esa."""
            self.t_recarga = None
            self.lista = cursos()
            self.marcas = leer_marcas()
            if self.curso:
                self.curso = next((c for c in self.lista if c["carpeta"] == self.curso["carpeta"]), None)
            actual = cargar_estado().get("clase")
            if actual and actual != self.clase and curso_de_clase(actual, self.lista):
                self.curso = curso_de_clase(actual, self.lista)
                self._llenar_selector()
                self.mostrar_clase(actual)
            else:
                self._llenar_selector()
                self._pintar_cabeza()
            return False

        # ---------------- mostrar una clase
        def mostrar_clase(self, clase, fase=None):
            self.clase = clase
            if not self.curso:
                self._vacia("📭 Todavía no hay cursos con apuntes.\n\nProcesá uno con SUPER+ALT+A o SUPER+ALT+Y.")
                return
            if not clase:
                self._vacia(f"🎉 ¡Terminaste «{self.curso['nombre']}»!\n\nTodas las clases están hechas o sabidas.\n"
                            "Repasá las tarjetas (K) o elegí otro curso arriba.")
                guardar_estado(curso=self.curso["carpeta"], clase=None)
                return
            estado = cargar_estado()
            if fase is None:
                fase = estado.get("fase") if estado.get("clase") == clase else None
            self.info = info_clase(clase)
            self._pintar_cabeza()
            pendiente = estado_clase(clase, self.marcas) == "pendiente"
            self.preguntas = preguntas_pretest(clase)
            if fase != "estudiar" and pendiente and self.preguntas:
                self.empezar_pretest()
                fase = "pretest"
            else:
                self.ir_a_estudiar(guardar=False)
                fase = "estudiar"
            guardar_estado(curso=self.curso["carpeta"], clase=clase, fase=fase)

        def _vacia(self, texto):
            self.info = {}
            self._pintar_cabeza()
            self.lbl_vacia.set_text(texto)
            self.pila.set_visible_child_name("vacia")

        def _pintar_cabeza(self):
            c, clase = self.curso, self.clase
            if not c:
                self.lbl_eyebrow.set_text("")
                self.lbl_titulo.set_text("Centro de estudio")
                self.chip.set_visible(False)
                self.lbl_progreso.set_text("")
                self.btn_pendiente.set_visible(False)
                return
            self.progreso = progreso(c, self.marcas)
            self.barra.queue_draw()
            self.lbl_progreso.set_text(texto_progreso(self.progreso) + f" · {self.progreso['pendiente']} pendientes")
            if clase and clase in c["clases"]:
                i, n = numero(clase, c)
                self.lbl_eyebrow.set_text(f"{c['nombre'].upper()}  ·  CLASE {i} DE {n}")
                self.lbl_titulo.set_text(titulo_corto(clase, c))
                est = estado_clase(clase, self.marcas)
                self.chip.set_text({"pendiente": "Pendiente", "hecha": "✅ Hecha", "sabida": "⏭️ Ya la sabías"}[est])
                for e in ("pendiente", "hecha", "sabida"):
                    self.chip.remove_css_class(e)
                self.chip.add_css_class(est)
                self.chip.set_visible(True)
                self.btn_pendiente.set_visible(est != "pendiente")
            else:
                self.lbl_eyebrow.set_text(c["nombre"].upper())
                self.lbl_titulo.set_text("Curso completo")
                self.chip.set_visible(False)
                self.btn_pendiente.set_visible(False)
            GLib.idle_add(self._contar_tarjetas)

        def _contar_tarjetas(self):
            if not self.curso:
                return False
            try:
                t = tarjetas_pendientes(self.curso, self.marcas)
            except Exception:  # el conteo es un extra: nunca romper la ventana
                t = {"vencidas": 0, "nuevas": 0, "archivo": None}
            self.tarjetas = t
            n = t["vencidas"] + t["nuevas"]
            self.btn_tarjetas.set_label(f"🃏 {n} para repasar" if n else "🃏 Repasar")
            self.btn_tarjetas.set_tooltip_text(
                f"{t['vencidas']} vencidas hoy · {t['nuevas']} nuevas (de clases hechas o sabidas)\n"
                "Tecla K: abre las tarjetas en Obsidian → Ctrl+P → «Revisar tarjetas»")
            return False

        def _dibujar_barra(self, _area, cr, ancho, alto):
            p = getattr(self, "progreso", None)
            r = alto / 2

            def pastilla(x, w, rgb):
                if w <= 0:
                    return
                w = max(w, alto)
                cr.set_source_rgb(*rgb)
                cr.new_sub_path()
                cr.arc(x + r, r, r, 1.5708, 4.7124)
                cr.arc(x + w - r, r, r, 4.7124, 1.5708)
                cr.close_path()
                cr.fill()

            pastilla(0, ancho, (0.16, 0.18, 0.22))
            if p and p["total"]:
                wh = ancho * p["hecha"] / p["total"]
                ws = ancho * p["sabida"] / p["total"]
                pastilla(0, wh + ws, (0.36, 0.58, 0.96))  # sabidas (azul) debajo…
                pastilla(0, wh, (0.29, 0.78, 0.50))       # …hechas (verde) arriba

        # ---------------- pre-test
        def empezar_pretest(self):
            self.i_preg, self.respuestas = 0, []
            self._pintar_pregunta()
            self.pila.set_visible_child_name("pretest")

        def _pintar_pregunta(self):
            n = len(self.preguntas)
            preg, resp = self.preguntas[self.i_preg]
            self.lbl_n_preg.set_text(f"Pregunta {self.i_preg + 1} de {n}")
            hijo = self.puntos.get_first_child()
            while hijo:
                sig = hijo.get_next_sibling()
                self.puntos.remove(hijo)
                hijo = sig
            for i in range(n):
                clase = "si" if i < len(self.respuestas) and self.respuestas[i] else \
                        "no" if i < len(self.respuestas) else "actual" if i == self.i_preg else ""
                self.puntos.append(etiqueta("●", ("punto",) + ((clase,) if clase else ()), wrap=False))
            self.lbl_pregunta.set_markup(md_pango(preg))
            self.lbl_respuesta.set_markup(md_pango(resp))
            self.rev_respuesta.set_reveal_child(False)
            self.pila_botones.set_visible_child_name("mostrar")

        def mostrar_respuesta(self):
            self.rev_respuesta.set_reveal_child(True)
            self.pila_botones.set_visible_child_name("evaluar")

        def autoevaluar(self, la_sabia):
            if not self.rev_respuesta.get_reveal_child():
                return  # primero hay que mostrar la respuesta
            self.respuestas.append(la_sabia)
            if self.i_preg + 1 < len(self.preguntas):
                self.i_preg += 1
                self._pintar_pregunta()
            else:
                self._resultado()

        def _resultado(self):
            bien, n = sum(self.respuestas), len(self.respuestas)
            self.lbl_puntaje.set_text(f"{bien}/{n}")
            for c in ("bien", "mas-o-menos", "mal"):
                self.lbl_puntaje.remove_css_class(c)
            if bien == n:
                self.lbl_puntaje.add_css_class("bien")
                self.lbl_mensaje.set_text("¡Las sabías todas! Esta clase ya la dominás:\nno hace falta verla.")
                self.btn_res_1.texto.set_text("⏭️  Ya lo sabés: marcar como sabida y pasar a la siguiente")
                self.btn_res_2.texto.set_text("📚  Estudiarla igual")
                self._tecla_res2 = "E"
                self.acciones_res = [self.marcar_sabida, self.ir_a_estudiar]
            else:
                self.lbl_puntaje.add_css_class("mas-o-menos" if bien else "mal")
                self.lbl_mensaje.set_text("Hay cosas nuevas acá: vale la pena estudiarla." if bien
                                          else "Esta clase es nueva para vos: a estudiarla.")
                self.btn_res_1.texto.set_text("📚  Estudiar esta clase")
                self.btn_res_2.texto.set_text("⏭️  Marcarla como sabida igual")
                self._tecla_res2 = "S"
                self.acciones_res = [self.ir_a_estudiar, self.marcar_sabida]
            self.btn_res_2.tecla.set_text(self._tecla_res2)
            self.pila.set_visible_child_name("resultado")
            self.btn_res_1.grab_focus()

        def _accion_res(self, i):
            if i < len(self.acciones_res):
                self.acciones_res[i]()

        # ---------------- estudiar
        def ir_a_estudiar(self, guardar=True):
            if not self.clase:
                return
            info = self.info
            self.lbl_idea.set_markup(md_pango(info.get("idea") or "(Esta clase no tiene resumen de IA: abrí los apuntes.)"))
            hijo = self.grilla_mapa.get_first_child()
            while hijo:
                sig = hijo.get_next_sibling()
                self.grilla_mapa.remove(hijo)
                hijo = sig
            for fila, (ini, tema) in enumerate(info.get("mapa", [])):
                self.grilla_mapa.attach(etiqueta(ini or "·", ("mapa-min",), wrap=False, xalign=1), 0, fila, 1, 1)
                self.grilla_mapa.attach(etiqueta(tema, ("mapa-tema",), hexpand=True), 1, fila, 1, 1)
            hay_mapa = bool(info.get("mapa"))
            self.caja_mapa_tit.set_visible(hay_mapa)
            self.grilla_mapa.set_visible(hay_mapa)
            self.btn_ver.texto.set_text("▶️  Ver la clase (mpv)" if info.get("video") else
                                        "▶️  Ver la clase (YouTube)" if info.get("youtube") else "▶️  Ver la clase (sin video)")
            self.btn_ver.set_sensitive(bool(info.get("video") or info.get("youtube")))
            self.btn_resumen.set_sensitive(os.path.exists(os.path.join(self.clase, "resumen.md")))
            pendiente = estado_clase(self.clase, self.marcas) == "pendiente"
            self.btn_terminar.texto.set_text("✅  Terminé esta clase" if pendiente else "⏩  Ir a la próxima pendiente")
            self._pintar_practica()
            self.pila.set_visible_child_name("estudiar")
            if guardar:
                guardar_estado(curso=self.curso["carpeta"], clase=self.clase, fase="estudiar")

        def _pintar_practica(self):
            clase = self.clase
            corriendo = self.procesos.get(clase)
            hay = os.path.isdir(os.path.join(clase, "practica"))
            self.btn_practica.texto.set_text("⏳  Generando práctica…" if corriendo == "practica" else
                                             "🏋️  Abrir práctica" if hay else "🏋️  Generar práctica")
            self.btn_tests.texto.set_text("⏳  Corriendo tests…" if corriendo == "tests" else "🧪  Correr tests")
            self.btn_practica.set_sensitive(corriendo is None)
            self.btn_tests.set_sensitive(corriendo is None and hay)
            salida = self.salidas.get(clase)
            if salida is None and hay:
                filas = resultado_practica(clase)
                if filas:
                    salida = self._formatear_resultado(filas, previo=True)
            self.caja_salida.set_visible(bool(salida))
            if salida:
                self.lbl_salida.set_markup(salida)

        def ver_clase(self):
            info = self.info
            if info.get("video"):
                ok = abrir(["mpv", "--save-position-on-quit", info["video"]])
            elif info.get("youtube"):
                ok = abrir(["xdg-open", info["youtube"]])
            else:
                ok = False
            if not ok:
                self.avisar("No encontré el video de esta clase")

        def abrir_archivo(self, nombre):
            ruta = os.path.join(self.clase, nombre)
            if os.path.exists(ruta):
                abrir_md(ruta)
            else:
                self.avisar(f"Esta clase no tiene {nombre}")

        def practica(self):
            clase = self.clase
            carpeta = os.path.join(clase, "practica")
            if os.path.isdir(carpeta):
                self._abrir_practica(carpeta)
                return
            if not os.path.exists(PRACTICA):
                self._salida(clase, "⚠️ <b>practica.py</b> todavía no está instalado: no se puede generar la práctica.")
                return
            self.procesos[clase] = "practica"
            self._salida(clase, "⏳ Generando la práctica con Claude (≈ 1 min). Podés seguir usando la ventana…")
            ultimas = []

            def linea(texto):
                ultimas.append(texto)
                del ultimas[:-6]
                self._salida(clase, "⏳ Generando la práctica (≈ 1 min)…\n" + html.escape("\n".join(ultimas)))

            def fin(codigo):
                self.procesos.pop(clase, None)
                if codigo == 0 and os.path.isdir(carpeta):
                    self._salida(clase, "✅ Práctica lista: se abre en VS Code (y su README en Obsidian).")
                    self._abrir_practica(carpeta)
                else:
                    self._salida(clase, f"❌ No se pudo generar la práctica (código {codigo}).\n"
                                        + html.escape("\n".join(ultimas[-6:])))

            self._correr([sys.executable, PRACTICA, clase], linea, fin)

        def _abrir_practica(self, carpeta):
            abrir(["code", carpeta])
            readme = os.path.join(carpeta, "README.md")
            if os.path.exists(readme):
                abrir_md(readme)

        def correr_tests(self):
            clase = self.clase
            if not os.path.exists(PRACTICA):
                self._salida(clase, "⚠️ <b>practica.py</b> todavía no está instalado.")
                return
            if not os.path.isdir(os.path.join(clase, "practica")):
                self._salida(clase, "Primero generá la práctica (P).")
                return
            self.procesos[clase] = "tests"
            self._salida(clase, "⏳ Corriendo los tests…")
            ultimas = []

            def linea(texto):
                ultimas.append(texto)
                del ultimas[:-12]

            def fin(codigo):
                self.procesos.pop(clase, None)
                filas = resultado_practica(clase)
                if filas:
                    self._salida(clase, self._formatear_resultado(filas))
                else:
                    cab = "✅ Todos los tests pasan" if codigo == 0 else f"❌ Hay tests que fallan (código {codigo})"
                    self._salida(clase, f"<b>{cab}</b>\n" + html.escape("\n".join(ultimas[-12:])))

            self._correr([sys.executable, PRACTICA, "--correr", clase], linea, fin)

        def _formatear_resultado(self, filas, previo=False):
            bien = sum(ok for _, ok, _ in filas)
            cab = (f"🧪 <b>{bien}/{len(filas)} ejercicios pasan</b>" + (" 🎉" if bien == len(filas) else "")
                   + ("  <span foreground='#8a93a4'>(última corrida)</span>" if previo else ""))
            lineas = [cab]
            for nombre, ok, detalle in filas:
                lineas.append(f"{'✅' if ok else '❌'} {html.escape(nombre)}")
                if detalle and not ok:
                    d = detalle.strip().splitlines()[0][:120]
                    lineas.append(f"<span foreground='#8a93a4' size='small'><tt>      {html.escape(d)}</tt></span>")
            return "\n".join(lineas)

        def _salida(self, clase, markup):
            self.salidas[clase] = markup
            if clase == self.clase and self.pila.get_visible_child_name() == "estudiar":
                self._pintar_practica()
                # el resultado queda abajo de los botones: bajar hasta verlo
                GLib.timeout_add(60, self._bajar)

        def _bajar(self):
            adj = self.scroll.get_vadjustment()
            adj.set_value(adj.get_upper() - adj.get_page_size())
            return False

        def _correr(self, argv, al_linea, al_terminar):
            """Subproceso asíncrono (la ventana no se congela): línea a línea y al final el código."""
            clase = self.clase
            try:
                proc = Gio.Subprocess.new(argv, Gio.SubprocessFlags.STDOUT_PIPE | Gio.SubprocessFlags.STDERR_MERGE)
            except GLib.Error as e:
                self.procesos.pop(clase, None)
                self._salida(clase, f"❌ No se pudo ejecutar: {html.escape(e.message)}")
                return
            flujo = Gio.DataInputStream.new(proc.get_stdout_pipe())
            self._pintar_practica()

            def leer(_s, res):
                try:
                    texto, _ = flujo.read_line_finish_utf8(res)
                except GLib.Error:
                    texto = None
                if texto is None:
                    proc.wait_async(None, lambda p, r: (p.wait_finish(r), al_terminar(p.get_exit_status()),
                                                        self._pintar_si(clase)))
                    return
                if texto.strip():
                    al_linea(texto.rstrip())
                flujo.read_line_async(GLib.PRIORITY_DEFAULT, None, leer)

            flujo.read_line_async(GLib.PRIORITY_DEFAULT, None, leer)

        def _pintar_si(self, clase):
            if clase == self.clase and self.pila.get_visible_child_name() == "estudiar":
                self._pintar_practica()

        # ---------------- cambiar estados
        def cambiar_estado(self, clase, estado, aviso=None):
            if not clase:
                return
            antes = estado_clase(clase, self.marcas)
            marcar(clase, estado)
            self.marcas = leer_marcas()
            if aviso:
                self.deshacer = (clase, antes)
                self.avisar(aviso, con_deshacer=True)
            self._pintar_cabeza()

        def marcar_sabida(self):
            clase = self.clase
            self.cambiar_estado(clase, "sabida", f"⏭️ «{titulo_corto(clase, self.curso)}» marcada como sabida")
            self.mostrar_clase(proxima(self.curso, self.marcas), fase="pretest")

        def terminar(self):
            clase = self.clase
            if not clase:
                return
            if estado_clase(clase, self.marcas) != "pendiente":  # ya hecha/sabida: solo avanzar
                self.mostrar_clase(proxima(self.curso, self.marcas), fase="pretest")
                return
            self.cambiar_estado(clase, "hecha", f"✅ «{titulo_corto(clase, self.curso)}» terminada")
            self.mostrar_clase(proxima(self.curso, self.marcas), fase="pretest")

        def hacer_deshacer(self):
            if not self.deshacer:
                return
            clase, antes = self.deshacer
            self.deshacer = None
            marcar(clase, antes)
            self.marcas = leer_marcas()
            self.aviso.set_reveal_child(False)
            self.mostrar_clase(clase, fase="estudiar")

        def avisar(self, texto, con_deshacer=False):
            self.lbl_aviso.set_text(texto)
            self.btn_deshacer.set_visible(con_deshacer)
            self.aviso.set_reveal_child(True)
            if getattr(self, "t_aviso", None):
                GLib.source_remove(self.t_aviso)
            self.t_aviso = GLib.timeout_add_seconds(6, self._ocultar_aviso)

        def _ocultar_aviso(self):
            self.t_aviso = None
            self.aviso.set_reveal_child(False)
            return False

        def navegar(self, paso):
            """← →: mirar otra clase del curso (no cambia su estado)."""
            if not self.curso:
                return
            clases = self.curso["clases"]
            i = clases.index(self.clase) if self.clase in clases else (len(clases) if paso < 0 else -1)
            j = max(0, min(len(clases) - 1, i + paso))
            if clases[j] != self.clase:
                self.mostrar_clase(clases[j])

        def repasar(self):
            t = getattr(self, "tarjetas", None) or {}
            ruta = t.get("archivo")
            if not ruta and self.clase:
                ruta = os.path.join(self.clase, "tarjetas.md")
            if ruta and os.path.exists(ruta):
                abrir_md(ruta)
                self.avisar("🃏 En Obsidian: Ctrl+P → «Revisar tarjetas» (de la nota o de todas)")
            else:
                self.avisar("No encontré tarjetas.md para repasar")

        # ---------------- teclado
        def _tecla(self, _c, tecla, _cod, mods):
            nombre = (Gdk.keyval_name(tecla) or "").lower()
            ctrl = bool(mods & Gdk.ModifierType.CONTROL_MASK)
            pagina = self.pila.get_visible_child_name()
            if nombre == "escape":
                self.win.set_visible(False)
                return True
            if ctrl and nombre == "z":
                self.hacer_deshacer()
                return True
            if ctrl and nombre in ("return", "kp_enter"):
                if pagina == "estudiar":
                    self.terminar()
                return True
            if ctrl or mods & Gdk.ModifierType.ALT_MASK:
                return False
            if self.selector.get_focus_child() or (self.selector.has_focus() and nombre in ("return", "space")):
                return False
            if nombre in ("left", "right"):
                self.navegar(-1 if nombre == "left" else 1)
                return True
            if nombre == "k":
                self.repasar()
                return True
            if pagina == "pretest":
                revelada = self.rev_respuesta.get_reveal_child()
                if nombre in ("space", "return", "kp_enter") and not revelada:
                    self.mostrar_respuesta()
                elif nombre in ("1", "kp_1") and revelada:
                    self.autoevaluar(True)
                elif nombre in ("2", "kp_2") and revelada:
                    self.autoevaluar(False)
                elif nombre == "s":
                    self.ir_a_estudiar()
                else:
                    return False
                return True
            if pagina == "resultado":
                if nombre in ("return", "kp_enter", "space"):
                    self._accion_res(0)
                elif nombre == getattr(self, "_tecla_res2", "").lower():
                    self._accion_res(1)
                else:
                    return False
                return True
            if pagina == "estudiar":
                accion = {"v": self.ver_clase, "r": lambda: self.abrir_archivo("resumen.md"),
                          "a": lambda: self.abrir_archivo("apuntes.md"), "p": self.practica,
                          "t": self.correr_tests}.get(nombre)
                if accion:
                    if nombre == "p" and self.procesos.get(self.clase):
                        return True
                    if nombre == "t" and (self.procesos.get(self.clase) or not self.btn_tests.get_sensitive()):
                        if not self.btn_tests.get_sensitive() and not self.procesos.get(self.clase):
                            self.correr_tests()  # muestra por qué no se puede
                        return True
                    accion()
                    return True
            return False

        # ---------------- ciclo de vida
        def presentar(self):
            if self.t_cierre:
                GLib.source_remove(self.t_cierre)
                self.t_cierre = None
            # ocultar + mostrar = volver a mapear: Hyprland la pone en el monitor/escritorio
            # actual y le da el foco (present() solo no siempre lo consigue en Wayland)
            if self.win.get_visible():
                self.win.set_visible(False)
            self.win.present()

        def _programar_salida(self):
            if self.t_cierre:
                GLib.source_remove(self.t_cierre)
            self.t_cierre = GLib.timeout_add_seconds(INACTIVA_MIN * 60, self._salir)

        def _salir(self):
            self.t_cierre = None
            if not self.win.get_visible():
                self.app.quit()
            return False

    prov = Gtk.CssProvider()
    prov.load_from_string(CSS) if hasattr(prov, "load_from_string") else prov.load_from_data(CSS.encode(), -1)
    App = Adw.Application if Adw else Gtk.Application
    app = App(application_id=APP_ID, flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
    estado = {"centro": None}

    def al_iniciar(a):
        if Adw:
            Adw.StyleManager.get_default().set_color_scheme(Adw.ColorScheme.FORCE_DARK)
        else:
            Gtk.Settings.get_default().set_property("gtk-application-prefer-dark-theme", True)
        Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), prov,
                                                  Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION + 1)
        a.hold()  # sigue vivo con la ventana oculta (se va solo tras INACTIVA_MIN)

    def al_activar(a):
        # cada activación (también la que llega de otro `estudiar.py` por D-Bus) relee todo
        if estado["centro"] is None:
            estado["centro"] = Centro(a)
        c = estado["centro"]
        c.recargar()
        c.presentar()

    def al_tecla(_accion, param):
        # acción D-Bus "tecla": simula una tecla por el mismo camino que el teclado real
        # (pruebas sin robar el foco; también sirve para un botón del Stream Deck):
        # gdbus call --session --dest estudiar.centro --object-path /estudiar/centro \
        #   --method org.gtk.Actions.Activate tecla "[<'space'>]" "{}"
        c = estado["centro"]
        if c is None:
            return
        nombre = param.get_string()
        mods = Gdk.ModifierType(0)
        if nombre.startswith("ctrl+"):
            nombre, mods = nombre[5:], Gdk.ModifierType.CONTROL_MASK
        c._tecla(None, Gdk.keyval_from_name(nombre), 0, mods)

    accion = Gio.SimpleAction.new("tecla", GLib.VariantType.new("s"))
    accion.connect("activate", al_tecla)
    app.add_action(accion)
    app.connect("startup", al_iniciar)
    app.connect("activate", al_activar)
    return app.run([sys.argv[0]])


def main():
    args = sys.argv[1:]
    try:
        if "--estado" in args:
            return cli_estado()
        if "--terminar" in args:
            return cli_terminar()
        if "--tests" in args:
            return cli_tests()
        if "--repasar" in args:
            return cli_repasar()
        if "--siguiente" in args:
            # la próxima pendiente pasa a ser la clase actual; la ventana (nueva o ya abierta) la muestra
            _, _, curso, _, marcas = contexto()
            if curso:
                guardar_estado(curso=curso["carpeta"], clase=proxima(curso, marcas), fase="pretest")
        if any(a in ("-h", "--help") for a in args):
            print(__doc__)
            return 0
    except Exception as e:
        notificar("🎓 Centro de estudio", f"Error: {type(e).__name__}: {e}", urgente=True)
        raise
    return gui()


if __name__ == "__main__":
    sys.exit(main())
