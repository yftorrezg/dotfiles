#!/usr/bin/env python3
"""Rearma apuntes.md con los niveles de capturas actuales, SIN llamar a la IA.

    rearmar-apuntes.py <curso o carpeta> [...]

Usa .apuntes-ia.json (+ subtitulos de la carpeta y .recursos.md) que ya existen. Sirve después de
capturas_clave.py: apuntes.md pasa a mostrar a la vista las esenciales y plegadas las clave.
Guarda el apuntes.md anterior en <clase>/.version-anterior/ la primera vez. Después rehace el INDICE del curso.
"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import cuadernillo as cu  # noqa: E402
import capturas_clave as cc  # noqa: E402


def clases(base):
    for raiz, _, archivos in os.walk(os.path.abspath(base)):
        if "apuntes.md" in archivos and ".apuntes-ia.json" in archivos and ".version-anterior" not in raiz:
            yield raiz


def es_suelto(carpeta):
    """Video suelto: la carpeta del curso ES la clase (las capturas están directo, sin capturas/<clase>/)."""
    return os.path.basename(os.path.dirname(carpeta)) != "capturas" and bool(cc.imagenes(carpeta)) \
        and os.path.isdir(os.path.join(carpeta, "capturas-clave"))


def sincronizar(carpeta, nombre, lista, padre=None):
    """Deja <clase>/<nombre>/ con las capturas de `lista` (enlaces duros 'NNNN · minuto.ext'). Lo que borró el
    usuario no vuelve (manifiesto .ya-agregadas.txt); lo que ya no corresponde se saca solo si es un enlace
    duro (nunca la única copia)."""
    destino = os.path.join(carpeta, nombre)
    os.makedirs(destino, exist_ok=True)
    manif = os.path.join(destino, cc.MANIFIESTO)
    ya = set(open(manif, encoding="utf-8").read().splitlines()) if os.path.exists(manif) else set()
    minutos = {}
    for l in open(os.path.join(carpeta, ".minutos.tsv"), encoding="utf-8").read().splitlines():
        if "\t" in l:
            a, b = l.split("\t")[:2]
            minutos[a] = b

    def nombre_de(f):
        base, ext = os.path.splitext(f)
        return f"{base} · {minutos[f]}{ext}" if f in minutos else f

    presentes = {f for f in os.listdir(destino) if f.lower().endswith(cc.EXT)}
    esperados, nuevas = set(), []
    for f in lista:
        n = nombre_de(f)
        if f in ya and n not in presentes:
            continue  # la borraste: no vuelve
        esperados.add(n)
        dst = os.path.join(destino, n)
        if not os.path.exists(dst):
            os.link(os.path.join(carpeta, f), dst)
        if f not in ya:
            nuevas.append(f)
    quitadas = 0
    for n in presentes - esperados:
        r = os.path.join(destino, n)
        if os.stat(r).st_nlink >= 2:
            os.remove(r)
            quitadas += 1
    with open(manif, "w", encoding="utf-8") as m:
        m.write("\n".join(sorted(ya | set(nuevas))) + "\n")
    return len(esperados), quitadas


def niveles_suelto(carpeta):
    esen = cc.esenciales(carpeta)
    if esen is None:
        raise SystemExit("Falta tesseract")
    clave = cc.elegir(carpeta)
    total = len(cc.imagenes(carpeta))
    n1, q1 = sincronizar(carpeta, "capturas-clave", clave)
    n2, q2 = sincronizar(carpeta, "capturas-esenciales", esen)
    for nombre, n in (("capturas-clave", n1), ("capturas-esenciales", n2)):
        with open(os.path.join(carpeta, nombre, "RESUMEN.md"), "w", encoding="utf-8") as h:
            h.write(f"# {nombre.replace('-', ' ').capitalize()} · {os.path.basename(carpeta)}\n\n"
                    f"**{n} de {total}** capturas ({100 * n // max(1, total)} %).\n")
    return total, n1, n2


def rearmar(carpeta):
    datos = json.load(open(os.path.join(carpeta, ".apuntes-ia.json"), encoding="utf-8"))
    if es_suelto(carpeta):
        total, n1, n2 = niveles_suelto(carpeta)
        print(f"   niveles: {total} → clave {n1} → esenciales {n2}", flush=True)
    capturas = cu.elegir_capturas(carpeta)
    if not capturas:
        return False
    subs = cu.buscar_subtitulos(carpeta, None)
    duracion = max([capturas[-1][1]] + [c[1] for v in subs.values() for c in v[-1:]])
    ruta_rec = os.path.join(carpeta, ".recursos.md")
    recursos = open(ruta_rec, encoding="utf-8").read() if os.path.exists(ruta_rec) else ""
    primera = open(os.path.join(carpeta, "apuntes.md"), encoding="utf-8").readline()
    titulo = primera.removeprefix("# 📓 ").strip() or os.path.basename(carpeta)
    resp = os.path.join(carpeta, ".version-anterior")
    if not os.path.exists(os.path.join(resp, "apuntes.md")):
        os.makedirs(resp, exist_ok=True)
        with open(os.path.join(resp, "apuntes.md"), "w", encoding="utf-8") as f:
            f.write(open(os.path.join(carpeta, "apuntes.md"), encoding="utf-8").read())
    nuevo = cu.armar(carpeta, titulo, capturas, subs, datos, duracion, recursos)
    with open(os.path.join(carpeta, "apuntes.md"), "w", encoding="utf-8") as f:
        f.write(nuevo)
    return True


def main():
    n, fallas = 0, []
    for base in sys.argv[1:]:
        for c in sorted(clases(base)):
            try:
                if rearmar(c):
                    n += 1
                    print("✔", os.path.relpath(c, base))
            except OSError as e:  # archivo ilegible (disco con errores): se salta y se avisa al final
                fallas.append(c)
                print("✘", os.path.relpath(c, base), "->", e, flush=True)
    print(f"{n} clases rearmadas" + (f", {len(fallas)} con error de lectura/escritura" if fallas else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
