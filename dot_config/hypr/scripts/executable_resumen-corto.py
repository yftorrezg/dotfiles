#!/usr/bin/env python3
"""Segunda versión de los apuntes, MÁS RESUMIDA: una hoja de repaso rápido por clase.

    resumen-corto.py <carpeta_de_capturas> [--forzar]
    resumen-corto.py --todos <carpeta>     # todas las clases de adentro que tengan apuntes

Las clases nuevas ya lo traen: cuadernillo.py lo pide en la MISMA llamada que los apuntes.
Esto es para clases viejas: no toca apuntes.md, parte de lo que Claude ya armó para él
(.apuntes-ia.json) y le pide que lo condense. Resultado: <carpeta>/resumen.md (+ .resumen-ia.json). Como la entrada
es chica (no se relee el video, ni subtítulos, ni OCR) tarda ~1 minuto.
"""
import argparse
import importlib.util
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from progreso import reportar  # barrita de progreso (no hace nada si no se pidió)
spec = importlib.util.spec_from_file_location("cuadernillo", os.path.join(AQUI, "cuadernillo.py"))
cu = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cu)

PROMPT = """Eres un profesor experto. Abajo están los APUNTES COMPLETOS (en JSON) de una clase en video.
Haz una versión MUCHO MÁS CORTA: una hoja de repaso para leer en 3-5 minutos antes de practicar
o de pasar a la siguiente clase. Solo lo que un alumno necesita recordar; nada de relleno.

Clase: {titulo}
Duración: {duracion}

Apuntes completos:
<<<
{apuntes}
>>>

Responde SOLO con un objeto JSON válido (sin ``` ni texto extra) con esta forma:
{{
  "idea": "la idea central de la clase en UNA frase",
  "esencial": ["4 a 8 cosas que hay que llevarse, una frase corta cada una"],
  "chuleta": [{{"quiero": "qué quiero hacer (corto)", "como": "cómo se hace: comando, función o sintaxis en `código`"}}],
  "codigo": [{{"titulo": "para qué sirve", "lenguaje": "javascript, python, bash...", "codigo": "hasta ~12 líneas"}}],
  "mapa": [{{"inicio": "h:mm:ss", "tema": "bloque grande de la clase (corto)"}}],
  "preguntas": [{{"pregunta": "pregunta para autoevaluarse", "respuesta": "respuesta corta"}}]
}}

Reglas:
- "chuleta": 4 a 12 filas, lo más usado en la práctica (en clases sin código, las definiciones o pasos clave).
- "codigo": 0 a 3 fragmentos, los que resumen la clase; sale del código de los apuntes (no inventes APIs).
- "mapa": 3 a 8 bloques que agrupen las secciones; "inicio" es el de la primera sección del bloque.
- "preguntas": EXACTAMENTE {n_preg}, de entender (por qué / qué pasa si / qué imprime / dónde está el error), no de memorizar nombres.
- Si agregas algo que no está en los apuntes, márcalo con "(extra)".
- Todo en español; términos técnicos en su forma original."""


def pedir_a_claude(titulo, duracion, datos):
    apuntes = {k: datos.get(k) for k in ("resumen", "conceptos", "secciones", "errores_comunes")}
    try:
        n_preg = cu.n_preguntas(cu.a_segundos(duracion))
    except (ValueError, TypeError):
        n_preg = 5
    prompt = PROMPT.format(titulo=titulo, duracion=duracion, n_preg=n_preg,
                           apuntes=json.dumps(apuntes, ensure_ascii=False, indent=1))
    for intento in range(2):
        texto = cu.consultar_ia(prompt)  # espera si se agotó la cuota de Claude
        try:
            corto = json.loads(texto[texto.index("{"):texto.rindex("}") + 1])
            if corto.get("esencial"):
                return corto
        except (ValueError, TypeError, json.JSONDecodeError):
            pass
        print(f"  (respuesta de Claude inválida, intento {intento + 1})", file=sys.stderr)
    return None


def celda(texto):
    """Texto seguro dentro de una tabla Markdown (el | la rompe)."""
    t = str(texto).replace("|", "\\|").replace("\n", " ")
    if "<" in t and "`" not in t:  # v8: un <script> suelto se pierde al mostrarse como HTML
        t = "`" + t + "`"
    return t


ICONO_TIPO = {"porque": "🤔 ", "que-imprime": "🖨️ ", "error": "🐞 ", "definicion": "📖 "}


def armar(titulo, duracion, corto, con_preguntas=True):
    L = [f"# ⚡ Repaso rápido: {titulo}", ""]
    L += [f"> ⏱️ **Duración:** {duracion} · 📓 **Versión completa:** [apuntes.md](apuntes.md)", ""]
    if corto.get("idea"):
        L += ["## 💡 En una frase", "", corto["idea"], ""]
    L += ["## ✅ Lo esencial", ""] + [f"- {e}" for e in corto.get("esencial", [])] + [""]
    seg = cu.a_segundos(duracion) if isinstance(duracion, str) and duracion else float(duracion or 0)
    largo = seg >= 45 * 60  # v8: código mínimo y mapa solo en clases largas (en las demás ya están en los apuntes)
    if corto.get("chuleta") and seg >= 8 * 60:
        L += ["## 🧩 Chuleta", "", "| Quiero… | Cómo |", "|---|---|"]
        L += [f"| {celda(c.get('quiero', ''))} | {celda(c.get('como', ''))} |" for c in corto["chuleta"]]
        L += [""]
    codigos = [c for c in corto.get("codigo", []) if str(c.get("codigo", "")).strip()]
    if codigos and largo:
        L += ["## 💻 Código mínimo", ""]
        for c in codigos:
            L += [f"**{c.get('titulo', '')}**", "", f"```{c.get('lenguaje') or ''}",
                  str(c["codigo"]).strip("\n"), "```", ""]
    diag = cu._mermaid(corto.get("diagrama"))
    if largo and (corto.get("mapa") or diag):
        L += ["## 🗺️ Mapa de la clase", ""]
        if diag:
            L += ["```mermaid", diag, "```", ""]
        L += [f"- `{m.get('inicio', '')}` {m.get('tema', '')}" for m in corto.get("mapa") or []] + [""]
    if corto.get("preguntas") and con_preguntas:  # v8: las preguntas viven en tarjetas.md (aquí era la misma lista)
        L += ["## 🔁 Autoevaluación", "", "*Responde de memoria y después abre la respuesta.*", ""]
        for k, q in enumerate(corto["preguntas"], 1):
            if not isinstance(q, dict):
                continue
            icono = ICONO_TIPO.get(q.get("tipo"), "")
            L += [f"> [!question]- {k}. {icono}{cu._txt(q.get('pregunta', ''))}"]
            if str(q.get("codigo") or "").strip():
                L += [">", f"> ```{q.get('lenguaje') or ''}"] + [f"> {x}" for x in str(q["codigo"]).strip("\n").split("\n")] + ["> ```", ">"]
            resp = str(q.get("respuesta", "")).strip("\n")
            if "\n" in resp:
                L += ["> **Respuesta:**", "> ```"] + [f"> {x}" for x in resp.split("\n")] + ["> ```"]
            else:
                L += [f"> **Respuesta:** {resp}"]
            if q.get("verificada"):
                L += ["> *✔ salida comprobada ejecutando el código*"]
            L += [""]
    return "\n".join(L)


def resumir(carpeta, forzar=False):
    """0 = hecho o ya estaba · 1 = no se pudo (sin apuntes de IA o Claude falló)."""
    salida = os.path.join(carpeta, "resumen.md")
    if os.path.exists(salida) and not forzar:
        print(f"Ya existe {salida} (usar --forzar para rehacerlo)")
        return 0
    try:
        datos = json.load(open(os.path.join(carpeta, ".apuntes-ia.json"), encoding="utf-8"))
    except (OSError, ValueError):
        print("Sin .apuntes-ia.json (apuntes hechos sin IA): no hay de dónde resumir")
        return 1
    titulo = os.path.basename(carpeta)
    try:  # el título real está en la primera línea de apuntes.md
        primera = open(os.path.join(carpeta, "apuntes.md"), encoding="utf-8").readline()
        titulo = primera.removeprefix("# 📓 ").strip() or titulo
    except OSError:
        pass
    duracion = ""
    try:
        linea = open(os.path.join(carpeta, "apuntes.md"), encoding="utf-8").read().split("**Duración:** ", 1)[1]
        duracion = linea.split(" ", 1)[0]
    except (OSError, IndexError):
        pass
    print(f"⚡ Pidiendo a Claude el resumen corto de {titulo}…")
    reportar(98, "apuntes", "resumen corto")
    corto = pedir_a_claude(titulo, duracion or "?", datos)
    if not corto:
        print("   (no se pudo armar el resumen corto)")
        return 1
    with open(os.path.join(carpeta, ".resumen-ia.json"), "w", encoding="utf-8") as f:
        json.dump(corto, f, ensure_ascii=False, indent=1)
    with open(salida, "w", encoding="utf-8") as f:
        f.write(armar(titulo, duracion or "?", corto))
    print(f"⚡ Listo: {salida}")
    return 0


def main():
    p = argparse.ArgumentParser()
    p.add_argument("carpeta")
    p.add_argument("--forzar", action="store_true")
    p.add_argument("--todos", action="store_true", help="todas las clases con apuntes dentro de la carpeta")
    a = p.parse_args()
    carpeta = os.path.abspath(a.carpeta)
    if not a.todos:
        return resumir(carpeta, a.forzar)
    clases = sorted(os.path.dirname(os.path.join(r, ".apuntes-ia.json"))
                    for r, _, fs in os.walk(carpeta) if ".apuntes-ia.json" in fs)
    fallas = sum(resumir(c, a.forzar) for c in clases)
    print(f"{len(clases) - fallas} de {len(clases)} clases con resumen corto")
    return 1 if fallas else 0


if __name__ == "__main__":
    sys.exit(main())
