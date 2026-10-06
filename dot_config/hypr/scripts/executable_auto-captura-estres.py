#!/usr/bin/env python3
"""Prueba de estrés: cambia 1 carácter al azar (dígito, letra, insertar, borrar) en código
parecido, vuelve con scroll a otra altura y verifica que el cambio SIEMPRE se guarde.
    python3 auto-captura-estres.py        # 40 pruebas     N=200 python3 ...  # 200
    python3 auto-captura-estres.py 35     # repetir la prueba 35 mostrando detalles
"""
import importlib.util, os, random, sys
spec = importlib.util.spec_from_file_location(
    "t", os.path.join(os.path.dirname(os.path.abspath(__file__)), "auto-captura-tests.py"))
t = importlib.util.module_from_spec(spec); spec.loader.exec_module(t)

def prueba(k, debug=False):
    rnd = random.Random(k)
    v = t.Video()
    v.lineas += [f"    w{n} = x ** {n} - {n * 7} + y[{n % 5}]" for n in range(90)]
    v.pasar(3)
    for s in (20, 45, 10):
        v.scroll = s; v.pasar(3)
    n = rnd.randrange(5, 60); linea = v.lineas[n]
    tipo = k % 4
    pos = rnd.choice([i for i, c in enumerate(linea) if (c.isdigit() if tipo == 0 else c.isalnum())])
    if tipo == 0:    # cambiar un dígito
        nuevo = linea[:pos] + str((int(linea[pos]) + rnd.randint(1, 9)) % 10) + linea[pos + 1:]
    elif tipo == 1:  # cambiar una letra/dígito por otra letra
        nuevo = linea[:pos] + rnd.choice([c for c in "abcdefghijklmnopqrstuvwxyz" if c != linea[pos]]) + linea[pos + 1:]
    elif tipo == 2:  # insertar un carácter
        nuevo = linea[:pos] + rnd.choice("abcxyz0123_") + linea[pos:]
    else:            # borrar un carácter
        nuevo = linea[:pos] + linea[pos + 1:]
    v.lineas[n] = nuevo
    v.scroll = max(0, n - rnd.randrange(3, 30))
    if debug:
        d = v.det; orig = d._ya_guardada
        def ya(red):
            r = orig(red); print(f"  _ya_guardada t={v.t} -> {r}"); return r
        d._ya_guardada = ya
        print("cambio", linea, "->", v.lineas[n], "scroll", v.scroll, "fila en vista", n - v.scroll)
    v.pasar(4); v.fin()
    return v.alguna_con(v.lineas[n]), linea, v.lineas[n], v

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ok, a, b, v = prueba(int(sys.argv[1]), True); print("ok" if ok else "PERDIDO", [g[0] for g in v.guardadas]); sys.exit()
    perdidos = []
    N = int(__import__('os').environ.get('N', 40))
    for k in range(N):
        ok, a, b, _ = prueba(k)
        if not ok:
            perdidos.append(k); print(f"PERDIDO #{k}:", a.strip(), "->", b.strip())
    print(f"cambios perdidos: {len(perdidos)}/{N}")
