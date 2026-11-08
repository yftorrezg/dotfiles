#!/usr/bin/env python3
"""Código y diapositivas que entrega el curso → imágenes en orden de clase + un .md con todo.

Lee `<curso>/Apuntes/<clase>/codigo-del-curso/` (lo copia recursos.py; antes `capturas/`) y, desde v10, también el
código y los PDF del curso que no quedaron asignados a ninguna clase (p. ej. una "Práctica final" sin video). Arma:
  <curso>/codigo-en-imagenes/NNN clase · archivo (k de N).webp   código resaltado (one-dark)
  <curso>/codigo-en-imagenes/NNN clase · archivo · pág P.webp     páginas de los PDF del curso
  <curso>/codigo-del-curso.md                                     todo el código, por clase
Pensado para estudiar pasando imágenes con una tecla (Gwenview, celular).

Uso: codigo-curso-a-imagenes.py <curso> [--movil|--pc] [--sin-pdf] [--forzar] [--ver]
  --movil (por defecto): 60 columnas, letra 30 px, ≤30 líneas → se lee sin zoom en el celular
  --pc: 100 columnas, letra 22 px, ≤42 líneas
Lo que borres en codigo-en-imagenes/ no vuelve (.ya-agregadas.txt).
"""
import argparse
import json
import importlib.util
import re
import subprocess
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("repo_img", AQUI / "repo-a-imagenes.py")
ri = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ri)
from PIL import Image  # noqa: E402

MAX_PAGINAS_ARCHIVO = 12      # un .sql de 2000 líneas de INSERT no es para estudiar
MAX_PAGINAS_NOTEBOOK = 30     # un notebook de una clase es largo pero es TODO el código de la clase
MAX_PAGINAS_PDF = 60


def es_volcado_de_datos(texto):
    """Scripts de datos (miles de INSERT) → no se dibujan; se enlazan en el .md."""
    ls = [x for x in texto.split("\n") if x.strip()]
    if len(ls) < 80:
        return False
    datos = sum(1 for x in ls if re.match(r"\s*(insert\s+into|values\s*\(|\(\s*['\d])", x, re.I))
    return datos / len(ls) > 0.5


CARPETAS_APUNTES = ("Apuntes", "capturas")
FUERA = {"Apuntes", "capturas", "capturas-clave", "capturas-esenciales", "todas-las-capturas", "codigo-en-imagenes",
         "capturas-estudio-codigos", "node_modules", "__pycache__", ".git", "Extras"}


def carpeta_apuntes(curso):
    return next((curso / n for n in CARPETAS_APUNTES if (curso / n).is_dir()), curso / "Apuntes")


def sueltos(curso, ya_vistos):
    """Código y PDF del curso que no está en ninguna clase: (carpeta relativa, archivo), en orden."""
    out = []
    for p in sorted(curso.rglob("*"), key=lambda p: ri.natural(str(p.relative_to(curso)))):
        partes = p.relative_to(curso).parts
        if not p.is_file() or len(partes) < 2 and p.suffix.lower() != ".pdf" or any(x in FUERA or x.startswith(".") for x in partes):
            continue
        if len(partes) == 1:  # en la raíz solo los PDF del curso, no lo que genera este sistema
            continue
        ext = p.suffix.lower()
        if ext in (".html", ".htm"):  # páginas de la plataforma (avisos, enunciados con enlaces): se abren en el navegador
            continue
        if ext != ".pdf" and ext != ".ipynb" and ext not in ri.EXT_CODIGO and p.name not in ri.NOMBRES_CODIGO:
            continue
        if (p.name, p.stat().st_size) in ya_vistos:
            continue
        out.append(p)
    return out


def clases(curso):
    cap = carpeta_apuntes(curso)
    if not cap.is_dir():
        return []
    return sorted((d for d in cap.iterdir() if d.is_dir() and (d / "codigo-del-curso").is_dir()),
                  key=lambda d: ri.natural(d.name))


def archivos(dir_cod):
    out = []
    for p in sorted(dir_cod.rglob("*"), key=lambda p: ri.natural(str(p.relative_to(dir_cod)))):
        if not p.is_file() or any(x in ri.DIRS_FUERA for x in p.relative_to(dir_cod).parts):
            continue
        out.append(p)
    return out


def notebook_a_texto(p, max_salida=8):
    """.ipynb → código Python de las celdas, separadas por '# ── [N]', con la salida REAL guardada en el
    notebook como comentario '# ▶ …' (recortada). Las celdas de texto van como comentarios cortos."""
    try:
        nb = json.loads(p.read_text(encoding="utf-8", errors="replace"))
    except (OSError, ValueError):
        return None
    out, n = [], 0
    for celda in nb.get("cells") or []:
        fuente = "".join(celda.get("source") or [])
        if not fuente.strip():
            continue
        if celda.get("cell_type") == "markdown":
            primera = next((x.strip("# ").strip() for x in fuente.split("\n") if x.strip()), "")
            if primera:
                out.append(f"# 📝 {primera[:90]}")
            continue
        if celda.get("cell_type") != "code":
            continue
        n += 1
        out.append(f"# ── [{n}]")
        out.append(fuente.rstrip())
        salida = []
        for o in celda.get("outputs") or []:
            if o.get("output_type") == "stream":
                salida += "".join(o.get("text") or []).split("\n")
            elif o.get("output_type") in ("execute_result", "display_data"):
                salida += "".join((o.get("data") or {}).get("text/plain") or []).split("\n")
        salida = [x for x in salida if x.strip()]
        if salida:
            out += [f"# ▶ {x[:100]}" for x in salida[:max_salida]]
            if len(salida) > max_salida:
                out.append(f"# ▶ … ({len(salida) - max_salida} líneas más)")
        out.append("")
    return "\n".join(out).rstrip() if n else None


def lenguaje_md(p):
    ext = p.suffix.lower().lstrip(".")
    return {"js": "javascript", "mjs": "javascript", "py": "python", "sh": "bash", "yml": "yaml",
            "htm": "html", "ts": "typescript", "kt": "kotlin", "rs": "rust", "rb": "ruby"}.get(ext, ext)


def guardar(img, destino):
    img.convert("RGB").save(destino, "WEBP", lossless=True, quality=50, method=1)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("curso", type=Path)
    ap.add_argument("--pc", action="store_true")
    ap.add_argument("--movil", action="store_true")
    ap.add_argument("--sin-pdf", action="store_true")
    ap.add_argument("--forzar", action="store_true")
    ap.add_argument("--ver", action="store_true", help="solo contar, no escribir nada")
    a = ap.parse_args()
    curso = a.curso.resolve()
    columnas, tamano, lineas = (100, 22, 42) if a.pc else (60, 30, 30)
    salida = curso / "codigo-en-imagenes"
    manif = salida / ".ya-agregadas.txt"
    ya = set() if a.forzar or not manif.exists() else set(manif.read_text().split("\n"))
    r = ri.Renderizador(columnas, tamano)
    cont = {"nuevas": 0, "cod": 0, "pdf": 0}

    def pieza(f, rel, enlace, base, titulo):
        """Un archivo → su entrada del .md (o None) y sus imágenes."""
        ext = f.suffix.lower()
        if ext == ".pdf":
            if a.sin_pdf:
                return None
            cont["pdf"] += 1
            if not (a.ver or base + ".pdf" in ya):
                with tempfile.TemporaryDirectory() as tmp:
                    subprocess.run(["pdftoppm", "-r", "110", "-png", "-l", str(MAX_PAGINAS_PDF), str(f), f"{tmp}/p"],
                                   capture_output=True)
                    for k, png in enumerate(sorted(Path(tmp).glob("p-*.png"), key=lambda p: ri.natural(p.name)), 1):
                        destino = salida / f"{base} · pág {k:02d}.webp"
                        if not destino.exists():
                            guardar(Image.open(png), destino)
                            cont["nuevas"] += 1
                ya.add(base + ".pdf")
            return f"- 📄 [{rel}](<{enlace}>) (páginas en imágenes)"
        es_nb = ext == ".ipynb"
        if not es_nb and ext not in ri.EXT_CODIGO and f.name not in ri.NOMBRES_CODIGO:
            return None
        if not es_nb and f.stat().st_size > ri.MAX_BYTES:
            return f"- 📦 [{rel}](<{enlace}>) (muy grande, solo enlace)"
        texto = notebook_a_texto(f) if es_nb else ri.leer(f)
        if not texto or not texto.strip():
            return None
        if es_volcado_de_datos(texto):
            return f"- 🗄️ [{rel}](<{enlace}>) (script de datos, solo enlace)"
        cont["cod"] += 1
        if not a.ver:
            ls = ri.lineas_resaltadas(texto, f.stem + ".py" if es_nb else f.name, r.estilo)
            rangos = ri.partir(ls, lineas)[:MAX_PAGINAS_NOTEBOOK if es_nb else MAX_PAGINAS_ARCHIVO]
            for k, (ini, fin) in enumerate(rangos, 1):
                suf = f" ({k} de {len(rangos)})" if len(rangos) > 1 else ""
                nombre = f"{base}{suf}.webp"
                destino = salida / nombre
                if nombre in ya or destino.exists():
                    continue
                guardar(r.imagen(ls[ini:fin], ini + 1, ri.corto(f"{rel} · {titulo}", columnas - (10 if suf else 2)),
                                 f"{k} de {len(rangos)}" if suf else ""), destino)
                ya.add(nombre)
                cont["nuevas"] += 1
        return f"### `{rel}`\n\n```{'python' if es_nb else lenguaje_md(f)}\n{texto}\n```"

    cls = clases(curso)
    if not a.ver:
        salida.mkdir(exist_ok=True)
    md = [f"# 💻 Código del curso — {curso.name}\n",
          "> Todo el código que entrega el curso, en orden de clase. Las imágenes están en "
          "`codigo-en-imagenes/` (una tecla = siguiente).\n"]
    vistos, n = set(), 0
    for clase in cls:
        n += 1
        piezas = []
        for f in archivos(clase / "codigo-del-curso"):
            rel = f.relative_to(clase / "codigo-del-curso")
            vistos.add((f.name, f.stat().st_size))
            base = f"{n:03d} {ri.limpiar(ri.corto(clase.name, 70))} · {ri.limpiar(ri.corto(str(rel), 50))}"
            x = pieza(f, rel, f"{clase.parent.name}/{clase.name}/codigo-del-curso/{rel}", base, clase.name)
            piezas += [x] if x else []
        if piezas:
            md.append(f"\n## {n:03d} · {clase.name}\n")
            md.extend(x + "\n" for x in piezas)
    # v10: lo que el curso trae y no quedó en ninguna clase (práctica final, material de una sección sin video…)
    grupos = {}
    for f in sueltos(curso, vistos):
        grupos.setdefault(str(f.parent.relative_to(curso)), []).append(f)
    for carpeta, fs in grupos.items():
        n += 1
        piezas = []
        for f in fs:
            base = f"{n:03d} {ri.limpiar(ri.corto(carpeta, 70))} · {ri.limpiar(ri.corto(f.name, 50))}"
            x = pieza(f, f.name, str(f.relative_to(curso)), base, carpeta)
            piezas += [x] if x else []
        if piezas:
            md.append(f"\n## {n:03d} · {carpeta} (material sin clase)\n")
            md.extend(x + "\n" for x in piezas)
    if not cont["cod"] and not cont["pdf"]:
        print(f"(sin código ni PDF del curso en {curso})")
        return 0
    print(f"{len(cls)} clases con material + {len(grupos)} carpetas sueltas · {cont['cod']} archivos de código · "
          f"{cont['pdf']} PDF · {cont['nuevas']} imágenes nuevas")
    if not a.ver:
        manif.write_text("\n".join(sorted(x for x in ya if x)))
        (curso / "codigo-del-curso.md").write_text("".join(md))
        print(salida)
    return 0


if __name__ == "__main__":
    sys.exit(main())
