#!/usr/bin/env python3
"""separar-curso.py <carpeta con varios cursos> [--ver]
Una carpeta "padre" con VARIOS cursos en subcarpetas (CodificandoBits/{Python, Deep_learning, …}) que se procesó como UN
solo curso (un Apuntes/ y un capturas-clave/ compartidos) → un curso por subcarpeta, cada uno con su propio Apuntes/,
capturas-clave/, capturas-esenciales/ (v10, 08/11/2026). Mueve (mismo disco: instantáneo, enlaces duros intactos):
  Apuntes/<clase>          → <sub>/Apuntes/<nombre nuevo>   (nombres() de normalizar-curso.py, sin el prefijo del padre)
  capturas-*/NNN <clase> · … → <sub>/capturas-*/<nuevo NNN> <clase nueva> · …
  codigo-en-imagenes y codigo-del-curso.md se vuelven a generar por curso.
Después pasa arreglar-curso.sh a cada curso (colores, índice, .hidden…). Sin IA. Idempotente: si ya está separado no hace nada."""
import importlib.util, os, re, shutil, subprocess, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent


def cargar(nombre, archivo):
    sp = importlib.util.spec_from_file_location(nombre, AQUI / archivo)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


nz = cargar("nz", "normalizar-curso.py")
tl = cargar("tl", "todas-las-capturas.py")
SISTEMA = nz.SISTEMA


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    ver = "--ver" in sys.argv
    padre = Path(args[0]).resolve()
    ap = next((padre / n for n in ("Apuntes", "capturas") if (padre / n).is_dir()), None)
    subs = sorted(d for d in padre.iterdir() if d.is_dir() and d.name not in SISTEMA and not d.name.startswith(".")
                  and nz.videos(str(d)))
    if not ap or len(subs) < 2:
        print("nada que separar (no hay Apuntes/ compartido o menos de 2 subcursos)")
        return
    names_p = nz.nombres(str(padre))  # {ruta relativa al padre: carpeta de Apuntes}
    hay = {d.name for d in ap.iterdir() if d.is_dir()}
    plan = {}  # sub -> [(old, new, k)]
    sin = 0
    for sub in subs:
        nx = nz.nombres(str(sub))  # {ruta relativa a sub: nombre nuevo}
        orden = sorted(set(nx.values()), key=tl.natural)
        for rel, nuevo in nx.items():
            old = names_p.get(f"{sub.name}/{rel}")
            if old in hay:
                plan.setdefault(sub, []).append((old, nuevo, orden.index(nuevo) + 1, len(orden)))
            else:
                sin += 1
    usados = {o for v in plan.values() for o, *_ in v}
    print(f"{padre.name}: {len(subs)} subcursos, {sum(len(v) for v in plan.values())} clases con apuntes, "
          f"{sin} videos sin carpeta de apuntes, {len(hay - usados)} carpetas de apuntes sin video")
    for sub, v in plan.items():
        print(f"  · {sub.name}: {len(v)} clases")
    if ver:
        return
    # 1) Apuntes
    for sub, v in plan.items():
        (sub / "Apuntes").mkdir(exist_ok=True)
        for old, nuevo, k, n in v:
            dst = sub / "Apuntes" / nuevo
            if dst.exists():
                print(f"  ⚠️ ya existe {dst}: se deja {old} en el padre")
                continue
            os.rename(ap / old, dst)
    # 2) capturas clave / esenciales
    mapa = {}  # limpio(old) -> (sub, limpio(new), k, ancho)
    choques = set()
    for sub, v in plan.items():
        for old, nuevo, k, n in v:
            clave = tl.limpio(old)
            if clave in mapa or clave in choques:  # v10: dos clases con el mismo nombre recortado (70 car.): NO se adivina; sus capturas se quedan
                choques.add(clave)                  # sin mover (antes se asignaban todas a una sola clase y se pisaban entre sí)
                mapa.pop(clave, None)
                continue
            mapa[clave] = (sub, tl.limpio(nuevo), k, max(3, len(str(n))))
    movidas = 0
    for carpeta in ("capturas-clave", "capturas-esenciales"):
        d = padre / carpeta
        if not d.is_dir():
            continue
        for f in os.listdir(d):
            m = re.match(r"^\d+ (.*?) · (.*)$", f)
            if not m or m.group(1) not in mapa:
                continue
            sub, nuevo, k, ancho = mapa[m.group(1)]
            (sub / carpeta).mkdir(exist_ok=True)
            os.rename(d / f, sub / carpeta / f"{k:0{ancho}d} {nuevo} · {m.group(2)}")
            movidas += 1
    print(f"  {movidas} capturas movidas")
    if choques:
        print(f"  ⚠️ {len(choques)} nombres de clase chocan al recortarse a 70 caracteres: sus capturas no se movieron "
              "(reasígnalas con .clave.txt + .minutos.tsv de cada clase)")
    # 3) lo del padre que ya no corresponde
    for n in ("codigo-en-imagenes", "codigo-del-curso.md", "MAPA.md", "INDICE.md"):
        p = padre / n
        if p.is_dir():
            shutil.rmtree(p)
        elif p.is_file():
            p.unlink()
    if (ap / "INDICE.md").is_file():
        (ap / "INDICE.md").unlink()
    for n in ("capturas-clave", "capturas-esenciales", "Apuntes", "capturas"):
        p = padre / n
        if p.is_dir() and not any(x for x in p.iterdir() if x.name not in (".directory", ".candado", ".ya-agregadas.txt", "RESUMEN.md")):
            shutil.rmtree(p)
        elif p.is_dir():
            print(f"  ⚠️ {n}/ del padre conserva {sum(1 for _ in p.iterdir())} elementos (revisar)")
    # 4) cada subcurso queda ordenado
    for sub in plan:
        subprocess.run(["bash", str(AQUI / "arreglar-curso.sh"), str(sub)], stdout=subprocess.DEVNULL)
        sys.stdout.write(f"  ✔ {sub.name} ordenado\n")


if __name__ == "__main__":
    main()
