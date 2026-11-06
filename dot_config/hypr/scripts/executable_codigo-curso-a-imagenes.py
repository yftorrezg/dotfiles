#!/usr/bin/env python3
"""Código y diapositivas que entrega el curso → imágenes en orden de clase + un .md con todo.

Lee `<curso>/capturas/<clase>/codigo-del-curso/` (lo copia recursos.py) y arma:
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


def clases(curso):
    cap = curso / "capturas"
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

    cls = clases(curso)
    if not cls:
        print(f"Sin codigo-del-curso/ en {curso}/capturas")
        return 0
    salida = curso / "codigo-en-imagenes"
    manif = salida / ".ya-agregadas.txt"
    ya = set() if a.forzar or not manif.exists() else set(manif.read_text().split("\n"))
    r = ri.Renderizador(columnas, tamano)
    md = [f"# 💻 Código del curso — {curso.name}\n",
          "> Todo el código que entrega el curso, en orden de clase. Las imágenes están en "
          "`codigo-en-imagenes/` (una tecla = siguiente).\n"]
    nuevas = n_cod = n_pdf = 0
    if not a.ver:
        salida.mkdir(exist_ok=True)
    for i, clase in enumerate(cls, 1):
        titulo = clase.name
        piezas = []
        for f in archivos(clase / "codigo-del-curso"):
            rel = f.relative_to(clase / "codigo-del-curso")
            base = f"{i:03d} {ri.limpiar(ri.corto(titulo, 70))} · {ri.limpiar(ri.corto(str(rel), 50))}"
            ext = f.suffix.lower()
            if ext == ".pdf" and not a.sin_pdf:
                n_pdf += 1
                piezas.append(f"- 📄 [{rel}](<capturas/{clase.name}/codigo-del-curso/{rel}>) (páginas en imágenes)")
                if a.ver or base + ".pdf" in ya:
                    continue
                with tempfile.TemporaryDirectory() as tmp:
                    subprocess.run(["pdftoppm", "-r", "110", "-png", "-l", str(MAX_PAGINAS_PDF), str(f),
                                    f"{tmp}/p"], capture_output=True)
                    pags = sorted(Path(tmp).glob("p-*.png"), key=lambda p: ri.natural(p.name))
                    for k, png in enumerate(pags, 1):
                        destino = salida / f"{base} · pág {k:02d}.webp"
                        if not destino.exists():
                            guardar(Image.open(png), destino)
                            nuevas += 1
                ya.add(base + ".pdf")
                continue
            es_nb = ext == ".ipynb"
            if not es_nb and ext not in ri.EXT_CODIGO and f.name not in ri.NOMBRES_CODIGO:
                continue
            if not es_nb and f.stat().st_size > ri.MAX_BYTES:
                piezas.append(f"- 📦 [{rel}](<capturas/{clase.name}/codigo-del-curso/{rel}>) (muy grande, solo enlace)")
                continue
            texto = notebook_a_texto(f) if es_nb else ri.leer(f)
            if not texto or not texto.strip():
                continue
            if es_volcado_de_datos(texto):
                piezas.append(f"- 🗄️ [{rel}](<capturas/{clase.name}/codigo-del-curso/{rel}>) (script de datos, solo enlace)")
                continue
            n_cod += 1
            piezas.append(f"### `{rel}`\n\n```{'python' if es_nb else lenguaje_md(f)}\n{texto}\n```")
            if a.ver:
                continue
            ls = ri.lineas_resaltadas(texto, f.stem + ".py" if es_nb else f.name, r.estilo)
            rangos = ri.partir(ls, lineas)[:MAX_PAGINAS_NOTEBOOK if es_nb else MAX_PAGINAS_ARCHIVO]
            for k, (ini, fin) in enumerate(rangos, 1):
                suf = f" ({k} de {len(rangos)})" if len(rangos) > 1 else ""
                nombre = f"{base}{suf}.webp"
                destino = salida / nombre
                if nombre in ya or destino.exists():
                    continue
                guardar(r.imagen(ls[ini:fin], ini + 1, ri.corto(f"{rel} · {titulo}", columnas - (10 if suf else 2)), f"{k} de {len(rangos)}" if suf else ""),
                        destino)
                ya.add(nombre)
                nuevas += 1
        if piezas:
            md.append(f"\n## {i:03d} · {titulo}\n")
            md.extend(p + "\n" for p in piezas)
    print(f"{len(cls)} clases con material · {n_cod} archivos de código · {n_pdf} PDF · {nuevas} imágenes nuevas")
    if not a.ver:
        manif.write_text("\n".join(sorted(x for x in ya if x)))
        (curso / "codigo-del-curso.md").write_text("".join(md))
        print(salida)
    return 0


if __name__ == "__main__":
    sys.exit(main())
