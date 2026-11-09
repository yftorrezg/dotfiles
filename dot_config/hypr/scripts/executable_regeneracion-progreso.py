#!/usr/bin/env python3
"""Barrita de progreso de la regeneración de apuntes (colas regenerar-cola.sh).

    regeneracion-progreso.py [--ver]      # --ver: una línea en la terminal y sale

Cuenta clases con `.regenerado-v6` sobre las clases con `.apuntes-ia.json` de los cursos de
~/.cache/auto-captura/regenerar-cursos.txt (una ruta por línea, admite * ) y alimenta la misma
barrita de los atajos (progreso.py seguir). ETA = ritmo de los últimos 20 min.
"""
import glob, os, subprocess, sys, time

LISTA = os.path.expanduser("~/.cache/auto-captura/regenerar-cursos.txt")
SCRIPTS = os.path.dirname(os.path.abspath(__file__))


def contar():
    hechas = total = 0
    por_curso = []
    for linea in open(LISTA, encoding="utf-8").read().splitlines():
        for curso in sorted(glob.glob(linea.strip())) if linea.strip() else []:
            ds = [d for n in ("Apuntes", "capturas") for d in glob.glob(glob.escape(curso) + f"/{n}/*/") if os.path.exists(d + ".apuntes-ia.json")]
            h = sum(os.path.exists(d + ".regenerado-v6") for d in ds)
            hechas, total = hechas + h, total + len(ds)
            por_curso.append((os.path.basename(curso), h, len(ds)))
    return hechas, total, por_curso


def eta(hist, hechas, total):
    ahora = time.time()
    hist.append((ahora, hechas))
    hist[:] = [x for x in hist if ahora - x[0] <= 1200]
    t0, h0 = hist[0]
    if ahora - t0 < 120 or hechas <= h0:
        return ""
    falta_s = (total - hechas) * (ahora - t0) / (hechas - h0)
    return f"~{int(falta_s // 3600)} h {int(falta_s % 3600 // 60):02d} min" if falta_s >= 3600 else f"~{int(falta_s // 60)} min"


def main():
    if "--ver" in sys.argv:
        h, t, pc = contar()
        for n, a, b in pc:
            print(f"{a:4}/{b:<4} {n[:70]}")
        print(f"TOTAL {h}/{t} ({100 * h // max(1, t)} %)")
        return
    archivo = os.path.expanduser(f"~/.cache/auto-captura/regeneracion-progreso.{os.getpid()}")
    env = dict(os.environ, PROGRESO_PID=str(os.getpid()))
    subprocess.Popen([sys.executable, os.path.join(SCRIPTS, "progreso.py"), "seguir", archivo, "Regenerando apuntes"],
                     env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    hist = []
    while True:
        h, t, pc = contar()
        actual = next((n for n, a, b in pc if a < b), "")
        etapa = "fin" if h >= t else "apuntes"
        pct = 100 * h / max(1, t)
        det = f"{h}/{t} clases · {actual[:28]}" + (f" · faltan {eta(hist, h, t)}" if etapa != "fin" and eta(hist, h, t) else "")
        tmp = archivo + ".tmp"
        open(tmp, "w", encoding="utf-8").write(f"{pct:.1f}|{etapa}|{det}|")
        os.replace(tmp, archivo)
        if etapa == "fin":
            return
        time.sleep(20)


if __name__ == "__main__":
    main()
