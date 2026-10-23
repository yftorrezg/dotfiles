#!/usr/bin/env python3
"""Agrega preguntas a las clases ya hechas, hasta las que les tocan por su duración.

    mas-preguntas.py <curso o carpeta> [--ver] [--forzar-n N]

Una clase de 1 h debe tener ~15 preguntas (cuadernillo.n_preguntas), pero las clases hechas antes del
20/10/2026 tienen 3-6. Esto NO vuelve a mirar el video: manda a la IA solo .apuntes-ia.json (resumen,
conceptos y puntos de cada sección) + las preguntas que ya hay, y pide las que faltan sin repetir.
Escribe en .resumen-ia.json (corto.preguntas), rehace resumen.md y las tarjetas (tarjetas.py --forzar
conserva el progreso de repaso <!--SR:). Se puede cortar y retomar: las clases completas se saltean.
--ver  solo muestra cuántas preguntas faltan, sin llamar a la IA.
"""
import fcntl
import json
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import cuadernillo as cu  # noqa: E402

PROMPT = """Eres un profesor que arma preguntas de autoevaluación en español sobre una clase en video.
Clase: {titulo}
Duración: {duracion}

Apuntes de la clase (JSON):
<<<
{apuntes}
>>>

Preguntas que YA existen (no las repitas ni las reformules):
{existentes}

Escribe EXACTAMENTE {n} preguntas NUEVAS. Reglas:
- Repartidas por TODA la clase (usa las secciones en orden: no todas del principio), más donde la clase es larga.
- De entender (por qué, qué pasa si, cuándo usar uno u otro, qué imprime este código), no de memorizar nombres.
- Cada respuesta es corta y completa (1-3 frases), con el código/valor exacto si hace falta.
Responde SOLO con un objeto JSON válido (sin ``` ni texto extra):
{{"preguntas": [{{"pregunta": "...", "respuesta": "..."}}]}}"""


def segundos(clase):
    """Duración de la clase: el minuto de la última captura (.minutos.tsv)."""
    try:
        with open(os.path.join(clase, ".minutos.tsv"), encoding="utf-8") as f:
            ultima = [l for l in f.read().splitlines() if l.strip()][-1]
        h, m, s = (int(x) for x in ultima.split("\t")[1].split("-"))
        return h * 3600 + m * 60 + s
    except (OSError, IndexError, ValueError):
        return 0


def leer(ruta):
    try:
        with open(ruta, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def titulo_de(clase):
    try:
        primera = open(os.path.join(clase, "apuntes.md"), encoding="utf-8").readline()
        return primera.removeprefix("# 📓 ").strip() or os.path.basename(clase)
    except OSError:
        return os.path.basename(clase)


def pendientes(base, n_fijo=None):
    """[(clase, segundos, tiene, quiere)] de las clases con apuntes de IA a las que les faltan preguntas."""
    salida = []
    for raiz, _, archivos in os.walk(os.path.abspath(base)):
        if ".apuntes-ia.json" not in archivos or ".resumen-ia.json" not in archivos:
            continue
        corto = leer(os.path.join(raiz, ".resumen-ia.json"))
        if not isinstance(corto, dict):
            continue
        seg = segundos(raiz)
        tiene = len([p for p in corto.get("preguntas") or [] if isinstance(p, dict) and p.get("pregunta")])
        quiere = n_fijo or cu.n_preguntas(seg)
        if tiene < quiere:
            salida.append((raiz, seg, tiene, quiere))
    return sorted(salida)


def agregar(clase, seg, tiene, quiere):
    """Pide las preguntas que faltan y las guarda. True si quedó hecho."""
    ruta = os.path.join(clase, ".resumen-ia.json")
    corto = leer(ruta)
    apuntes = leer(os.path.join(clase, ".apuntes-ia.json")) or {}
    existentes = [p for p in corto.get("preguntas") or [] if isinstance(p, dict) and p.get("pregunta")]
    resumen_apuntes = {
        "resumen": apuntes.get("resumen"),
        "conceptos": apuntes.get("conceptos"),
        "secciones": [{"inicio": s.get("inicio"), "titulo": s.get("titulo"), "puntos": s.get("puntos")}
                      for s in apuntes.get("secciones") or [] if isinstance(s, dict)],
    }
    falta = quiere - len(existentes)
    prompt = PROMPT.format(titulo=titulo_de(clase), duracion=cu.hms(seg) if seg else "?",
                           apuntes=json.dumps(resumen_apuntes, ensure_ascii=False),
                           existentes="\n".join(f"- {p['pregunta']}" for p in existentes) or "(ninguna)", n=falta)
    texto = cu.consultar_ia(prompt)
    try:
        nuevas = json.loads(texto[texto.index("{"):texto.rindex("}") + 1]).get("preguntas") or []
    except (ValueError, AttributeError, TypeError):
        print("   (la IA no respondió con JSON válido)")
        return False
    vistas = {p["pregunta"].strip().lower() for p in existentes}
    nuevas = [p for p in nuevas if isinstance(p, dict) and str(p.get("pregunta", "")).strip()
              and str(p.get("respuesta", "")).strip() and p["pregunta"].strip().lower() not in vistas][:falta]
    if not nuevas:
        print("   (sin preguntas nuevas útiles)")
        return False
    corto["preguntas"] = existentes + [{"pregunta": p["pregunta"].strip(), "respuesta": p["respuesta"].strip()} for p in nuevas]
    with open(ruta + ".tmp", "w", encoding="utf-8") as f:
        json.dump(corto, f, ensure_ascii=False, indent=1)
    os.replace(ruta + ".tmp", ruta)
    rc = cu.cargar_resumen_corto()
    with open(os.path.join(clase, "resumen.md"), "w", encoding="utf-8") as f:
        f.write(rc.armar(titulo_de(clase), cu.hms(seg) if seg else "?", corto))
    subprocess.run([sys.executable, os.path.join(AQUI, "tarjetas.py"), clase, "--forzar"],
                   stdout=subprocess.DEVNULL, check=False)
    print(f"   ✅ +{len(nuevas)} preguntas ({len(corto['preguntas'])} en total)")
    return True


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 1
    n_fijo = None
    if "--forzar-n" in sys.argv:
        n_fijo = int(sys.argv[sys.argv.index("--forzar-n") + 1])
        args = [a for a in args if a != str(n_fijo)]
    lista = [x for base in args for x in pendientes(base, n_fijo)]
    if not lista:
        print("✅ Todas las clases tienen las preguntas que les tocan")
        return 0
    print(f"❓ {len(lista)} clases con menos preguntas de las que les tocan "
          f"({sum(q - t for _, _, t, q in lista)} preguntas por agregar)")
    if "--ver" in sys.argv:
        for clase, seg, tiene, quiere in lista[:40]:
            print(f"  {tiene:2d} → {quiere:2d}  ({cu.hms(seg) if seg else '?'})  {os.path.basename(clase)}")
        if len(lista) > 40:
            print(f"  … y {len(lista) - 40} más")
        return 0
    candado = open(os.path.join(os.environ.get("XDG_RUNTIME_DIR", "/tmp"), "mas-preguntas.lock"), "w")
    fcntl.flock(candado, fcntl.LOCK_EX)  # una corrida a la vez
    hechas = 0
    for k, (clase, seg, tiene, quiere) in enumerate(lista, 1):
        print(f"[{k}/{len(lista)}] {os.path.basename(clase)} ({tiene} → {quiere})", flush=True)
        hechas += agregar(clase, seg, tiene, quiere)
    subprocess.run([sys.executable, os.path.join(AQUI, "panel-cursos.py")], stdout=subprocess.DEVNULL, check=False)
    print(f"❓ Listo: {hechas} de {len(lista)} clases con preguntas nuevas")
    return 0 if hechas == len(lista) else 1


if __name__ == "__main__":
    sys.exit(main())
