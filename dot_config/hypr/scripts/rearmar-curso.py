#!/usr/bin/env python3
"""rearmar-curso.py <carpeta del curso o su carpeta de apuntes> [más…]
Re-arma apuntes.md, transcripcion.md y tarjetas.md de cada clase con el diseño actual (presupuesto de lectura) a partir
del .apuntes-ia.json YA guardado. SIN IA, sin cuota, sin tocar videos ni capturas. Sin respaldo, a propósito: el JSON
conserva el texto completo de la IA, así que se puede volver a armar cuando se quiera.
resumen.md solo queda en clases de 20+ min (en las cortas repetía los apuntes)."""
import json, os, re, subprocess, sys
from pathlib import Path

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import cuadernillo as cu


def clases_de(ruta):
    ruta = Path(ruta)
    for nombre in ("Apuntes", "capturas"):
        if (ruta / nombre).is_dir() and ruta.name not in ("Apuntes", "capturas"):
            ruta = ruta / nombre
            break
    return sorted(p for p in ruta.iterdir() if p.is_dir() and (p / ".apuntes-ia.json").is_file())


def titulo_de(c):
    md = c / "apuntes.md"
    if md.is_file():
        t = md.read_text(encoding="utf-8").splitlines()[0].removeprefix("# 📓 ").removeprefix("# ").strip()
        if t:
            return t
    m = re.match(r"^.+? - (\d{1,3})\s+(.*)$", c.name)  # "13 - Triggers - 004 Clase" → "004. Clase"
    return f"{m.group(1)}. {m.group(2)}" if m else c.name


def enlaces_relativos(md, clase):
    """Los recursos guardaban rutas absolutas del disco donde se procesó (file:///run/media/yafer/SuperYafer/…), que ya no
    existen. Se vuelven relativas al curso actual: <curso>/Apuntes/<clase>/ → ../../<tema>/<archivo>."""
    curso = clase.parent.parent.name
    return re.sub(r"<file://[^>]*?/" + re.escape(curso) + r"/([^>]*)>", lambda m: "<../../" + m.group(1) + ">", md)


def rearmar(c):
    datos = json.loads((c / ".apuntes-ia.json").read_text(encoding="utf-8"))
    datos.pop("corto", None)
    titulo = titulo_de(c)
    dur = cu.editorial.duracion_guardada(str(c))
    rec = c / ".recursos.md"
    cod = rec.read_text(encoding="utf-8") if rec.is_file() else ""
    cod = enlaces_relativos(cod, c)
    subs = cu.buscar_subtitulos(str(c), None)
    if dur < 1200 and (c / "resumen.md").exists():
        (c / "resumen.md").unlink()  # antes de armar: así el apunte no enlaza a un resumen que no existe
    md = cu.armar(str(c), titulo, [], subs, datos, dur, cod)
    tmp = c / ".apuntes.md.tmp"
    tmp.write_text(md, encoding="utf-8")
    os.replace(tmp, c / "apuntes.md")  # atómico: un corte no deja un apunte a medias
    r = subprocess.run([sys.executable, os.path.join(AQUI, "tarjetas.py"), str(c), "--forzar"],
                       capture_output=True, text=True, timeout=120)
    if "No salió ninguna tarjeta" in r.stdout:  # v10: 0 tarjetas es válido (antes salía relleno): se quitan las viejas
        for f in ("tarjetas.md", "tarjetas-anki.txt"):
            (c / f).unlink(missing_ok=True)
    elif r.returncode != 0 or "🃏" not in r.stdout:
        raise RuntimeError("tarjetas.py: " + (r.stderr or r.stdout).strip()[-200:])
    return dur, cu.palabras_a_la_vista(md), cu.presupuesto_lectura(dur)


def main():
    rutas = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not rutas:
        sys.exit(__doc__)
    for ruta in rutas:
        n = pasadas = fallos = 0
        seg = vista = 0
        for c in clases_de(ruta):
            try:
                dur, pal, tope = rearmar(c)
            except Exception as e:  # una clase rota no frena el curso
                print(f"FALLÓ {c.name}: {e}")
                fallos += 1
                continue
            n += 1
            seg += dur
            vista += pal
            if pal > tope * 1.05:
                pasadas += 1
                print(f"  sobre el presupuesto: {c.name} ({pal} > {tope})")
        print(f"{Path(ruta).name}: {n} clases · {seg / 3600:.1f} h de video · apuntes {vista / 200 / 60:.1f} h de lectura · "
              f"{pasadas} sobre el presupuesto · {fallos} fallos")


if __name__ == "__main__":
    main()
