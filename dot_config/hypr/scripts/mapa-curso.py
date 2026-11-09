#!/usr/bin/env python3
"""MAPA.md de un curso: una hoja por MÓDULO (no por clase) para cursos enormes (Udemy, 300-700 clases).

Por módulo (lo que va antes de " - " en el nombre de la clase): qué tienes que saber sin mirar, el proyecto
que lo integra (con criterio de "listo"), preguntas de aplicación, errores típicos y qué clases son clave
o se pueden saltar. Usa lo que ya está en cada .apuntes-ia.json (idea, esencial, secciones): NO lee video
ni transcripción → 1 llamada corta a la IA por módulo (Claude Haiku primero, sin Codex).

    mapa-curso.py <curso>... [--ver] [--forzar]

Caché por módulo en <curso>/.mapa/ (se reanuda; si cambian las clases del módulo, se rehace).
"""
import hashlib, json, os, re, sys, time
from pathlib import Path

os.environ.setdefault("APUNTES_MOTOR", "opencode")
os.environ.setdefault("APUNTES_RESPALDO", "haiku")
os.environ.setdefault("APUNTES_CODEX", "0")
sys.path.insert(0, str(Path(__file__).resolve().parent))
import cuadernillo as cu  # noqa: E402

PROMPT = """Eres un profesor experto en {area}. Te paso el contenido resumido de las clases de UN módulo del curso «{curso}».
El alumno ya vio (o verá) los videos. Quiere una hoja del módulo que lo prepare para TRABAJAR, sin releer todo.

Módulo: {modulo}  ({n} clases, {dur} de video)
Clases (número · título · duración · idea · lo esencial):
<<<
{clases}
>>>

Responde SOLO un JSON válido, sin texto antes ni después:
{{
 "objetivo": "qué podrá HACER al terminar el módulo (1 frase concreta)",
 "retener": ["lo que hay que saber sin mirar: conceptos, comandos, patrones, con el dato exacto (máx. {n_ret})"],
 "proyecto": {{"enunciado": "un ejercicio integrador pequeño que use lo del módulo (1-3 h)", "pasos": ["3-6 pasos"], "listo_si": "criterio verificable de que está bien"}},
 "preguntas": [{{"pregunta": "de aplicación o de por qué (no de memoria)", "respuesta": "breve"}}],
 "errores": ["errores típicos de este tema y cómo evitarlos (máx. 4)"],
 "clave": [números de las clases imprescindibles: COMO MÁXIMO 1 de cada 3 clases del módulo, las que no se pueden saltar],
 "saltables": [números de clases de trámite: bienvenida, instalación, repaso, despedida]
}}
Reglas: usa solo lo que dicen las clases (si añades algo tuyo, márcalo "(extra)"). {n_preg} preguntas. Nada de relleno ni
muletillas ("en este módulo veremos"). Si el módulo es solo de trámite (presentación, despedida), "retener" con 1-2 puntos,
"proyecto" null y "preguntas" vacío.
"""


def modulo_de(nombre):
    return nombre.split(" - ", 1)[0].strip() if " - " in nombre else nombre.strip()


def numero(nombre):
    resto = nombre.rsplit(" - ", 1)[1] if " - " in nombre else nombre  # "11 Genéricos - Generics - 1 Intro" → "1 Intro"
    m = re.match(r"\s*(\d+)", resto)
    return int(m.group(1)) if m else None


def _t(x):
    if isinstance(x, list):
        return "; ".join(_t(y) for y in x if _t(y))
    if isinstance(x, dict):
        return " ".join(_t(v) for v in x.values() if _t(v))
    return re.sub(r"\s+", " ", str(x or "")).strip()


def leer_clases(curso):
    base = next((curso / n for n in ("Apuntes", "capturas") if (curso / n).is_dir()), curso)
    mods = {}
    for d in sorted(base.iterdir(), key=lambda p: [int(x) if x.isdigit() else x for x in re.split(r"(\d+)", p.name)]):
        try:
            if not (d / ".apuntes-ia.json").is_file():
                continue
            j = json.loads((d / ".apuntes-ia.json").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        corto = j.get("corto") if isinstance(j.get("corto"), dict) else {}
        dur = cu.editorial.duracion_guardada(str(d)) or 0
        info = {"dir": d.name, "num": numero(d.name), "titulo": d.name.split(" - ", 1)[-1], "dur": dur,
                "idea": _t(corto.get("idea"))[:300],
                "esencial": _t(corto.get("esencial"))[:500] or _t([s.get("titulo") for s in j.get("secciones") or []])[:400],
                "ligera": bool(j.get("ligera") or j.get("sin_contenido"))}
        mods.setdefault(modulo_de(d.name), []).append(info)
    return base, mods


def pedir(curso, modulo, clases, area):
    lineas = [f"{c['num'] or '-'} · {c['titulo']} · {cu.hms(c['dur'])} · {c['idea']} · {c['esencial']}" for c in clases]
    texto = "\n".join(lineas)[:24000]
    total = sum(c["dur"] for c in clases)
    n_ret = max(3, min(10, round(2 + total / 600)))
    n_preg = 0 if total < 300 else max(2, min(8, round(1 + total / 900)))
    p = PROMPT.format(area=area, curso=curso, modulo=modulo, n=len(clases), dur=cu.hms(total), clases=texto,
                      n_ret=n_ret, n_preg=n_preg)
    for intento in range(3):
        r = cu.consultar_ia(p)
        try:
            d = json.loads(r[r.index("{"):r.rindex("}") + 1])
            if isinstance(d, dict) and d.get("retener"):
                return d
        except (ValueError, TypeError, AttributeError):
            pass
        print(f"    respuesta inválida (intento {intento + 1}/3)", flush=True)
    return None


def area_de(nombre):
    n = nombre.lower()
    for clave, area in (("hack", "ciberseguridad y hacking ético"), ("linux", "Linux y administración de sistemas"),
                        ("sql", "bases de datos"), ("flutter", "desarrollo móvil con Flutter"),
                        ("react native", "desarrollo móvil"), ("docker", "contenedores y DevOps")):
        if clave in n:
            return area
    return "programación y desarrollo de software"


def ancla(t):
    return re.sub(r"[^\w\s-]", "", t.lower()).strip().replace(" ", "-")


def armar_md(curso, base, mods, datos):
    total = sum(c["dur"] for cs in mods.values() for c in cs)
    L = [f"# 🗺️ Mapa del curso: {curso.name}", "",
         f"> ⏱️ {cu.hms(total)} de video · 📦 {len(mods)} módulos · 🎬 {sum(len(c) for c in mods.values())} clases",
         "> Cómo usarlo: ve el video del módulo → cierra todo y responde las preguntas → haz el proyecto →"
         " vuelve al apunte de una clase solo si te trabas.", ""]
    L += [f"> [!summary]- 📦 Módulos ({len(mods)})"] + \
         [f"> {k + 1}. [{m}](#{ancla(m)}) · {cu.hms(sum(c['dur'] for c in cs))}" for k, (m, cs) in enumerate(mods.items())] + ["", "---", ""]
    for m, cs in mods.items():
        d = datos.get(m) or {}
        L += [f"## {m}", "", f"⏱️ {cu.hms(sum(c['dur'] for c in cs))} · {len(cs)} clases", ""]
        if not d:
            L += ["> [!info] Sin mapa todavía (la IA no respondió): se rehace al volver a correr mapa-curso.py", ""]
        if _t(d.get("objetivo")):
            L += [f"🎯 **{_t(d['objetivo'])}**", ""]
        if d.get("retener"):
            L += ["**🔑 Saber sin mirar**", ""] + [f"- {_t(x)}" for x in d["retener"]] + [""]
        pj = d.get("proyecto")
        if isinstance(pj, dict) and _t(pj.get("enunciado")):
            L += [f"> [!todo] 🛠️ Proyecto del módulo: {_t(pj['enunciado'])}"]
            L += [f"> {k}. {_t(x)}" for k, x in enumerate(pj.get("pasos") or [], 1)]
            if _t(pj.get("listo_si")):
                L += [">", f"> ✅ **Listo si:** {_t(pj['listo_si'])}"]
            L += [""]
        qs = [q for q in d.get("preguntas") or [] if isinstance(q, dict) and _t(q.get("pregunta"))]
        if qs:
            L += ["> [!question] 🧠 Respóndete sin mirar"]
            for q in qs:
                L += [f"> - {_t(q['pregunta'])}", ">   > [!success]- Respuesta", f">   > {_t(q.get('respuesta'))}"]
            L += [""]
        if d.get("errores"):
            L += ["> [!warning]- ⚠️ Errores típicos"] + [f"> - {_t(x)}" for x in d["errores"]] + [""]
        clave = {int(x) for x in d.get("clave") or [] if str(x).isdigit()}
        salt = {int(x) for x in d.get("saltables") or [] if str(x).isdigit()}
        L += [f"> [!abstract]- 🎬 Clases del módulo ({len(cs)})", "> | | Clase | Dura |", "> |---|---|---|"]
        for c in cs:
            marca = "⭐" if c["num"] in clave else "💤" if (c["num"] in salt or c["ligera"]) else ""
            ruta = f"{base.name}/{c['dir']}/apuntes.md" if base != curso else f"{c['dir']}/apuntes.md"
            L += [f"> | {marca} | [{c['titulo'].replace('|', '/')}](<{ruta}>) | {cu.hms(c['dur'])} |"]
        L += ["", "---", ""]
    return "\n".join(L)


def hacer(curso, forzar=False, ver=False):
    curso = Path(curso)
    base, mods = leer_clases(curso)
    if not mods:
        print(f"(sin clases con apuntes) {curso}")
        return
    cache = curso / ".mapa"
    print(f"=== {curso.name}: {len(mods)} módulos, {sum(len(c) for c in mods.values())} clases", flush=True)
    if ver:
        for m, cs in mods.items():
            print(f"  {len(cs):3} · {m}")
        return
    cache.mkdir(exist_ok=True)
    datos, area = {}, area_de(str(curso))
    for k, (m, cs) in enumerate(mods.items(), 1):
        firma = hashlib.sha1("|".join(c["dir"] for c in cs).encode()).hexdigest()[:12]
        f = cache / f"{firma}.json"
        if f.is_file() and not forzar:
            datos[m] = json.loads(f.read_text(encoding="utf-8"))
            continue
        t0 = time.time()
        d = pedir(curso.name, m, cs, area)
        print(f"  [{k}/{len(mods)}] {m[:60]} → {'ok' if d else 'FALLÓ'} ({time.time() - t0:.0f}s)", flush=True)
        if d:
            d["_modulo"] = m
            f.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
            datos[m] = d
        (curso / "MAPA.md").write_text(armar_md(curso, base, mods, datos), encoding="utf-8")  # se ve crecer
    (curso / "MAPA.md").write_text(armar_md(curso, base, mods, datos), encoding="utf-8")
    print(f"  📄 {curso / 'MAPA.md'}", flush=True)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    for c in args:
        hacer(c, forzar="--forzar" in sys.argv, ver="--ver" in sys.argv)
