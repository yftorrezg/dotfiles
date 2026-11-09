#!/usr/bin/env python3
"""normalizar-curso.py <carpeta del curso> [--ver]
Arregla la ESTRUCTURA de un curso descargado/descomprimido (v10, 08/11/2026). --ver: solo dice qué haría.

  1. Copias repetidas de una carpeta ("02 - Tema (1)", "02 - Tema (2)" junto a "02 - Tema", típico de descomprimir dos
     veces): si todo lo que tienen ya está en la original (mismo nombre y tamaño) se borran; si traen algo que falta, eso
     se mueve a la original y la copia se borra. Sus apuntes repetidos (se hicieron con IA, por duplicado) también.
  2. Carpetas metidas dentro de otra con el mismo nombre ("Tema/Tema/videos", "Curso/Curso/…"): se aplanan.
  3. Como el nombre de la carpeta de apuntes de cada clase sale de la ruta del video (misma regla que
     curso-a-apuntes.sh), se renombran las carpetas de Apuntes/ para que SUPER+ALT+A las siga reconociendo (si no,
     rehace con IA clases ya hechas), y se corrigen los enlaces de MAPA.md y codigo-del-curso.md.
Nunca toca un video que no sea una copia idéntica de otro."""
import os, re, shutil, sys
from pathlib import Path

VIDEO = (".mp4", ".mkv", ".webm", ".mov")
SISTEMA = {"Apuntes", "capturas", "capturas-clave", "capturas-esenciales", "todas-las-capturas", "codigo-en-imagenes",
           "capturas-estudio-codigos", "node_modules", "Extras"}
SISTEMA_ARCH = {"MAPA.md", "codigo-del-curso.md", "INDICE.md", "regeneracion.log", "resultado-regeneracion.json"}


# ---------------------------------------------------------------- nombres (copia de curso-a-apuntes.sh) ----
def _limpia(t):
    t = re.sub(r"@\w+\s*", "", t)
    t = re.sub(r"^\s*(\d+)\s*[.)]\s+", r"\1 ", t)
    t = re.sub(r"[\s/]*-\s*$", "", t)
    return re.sub(r"\s{2,}", " ", t).strip()


def nombre_corto(prefijo, sub, clase):
    if prefijo and (sub + "/").startswith(prefijo):
        sub = (sub + "/")[len(prefijo):].rstrip("/") or "."
    partes = [_limpia(x) for x in sub.split("/")] if sub != "." else []
    partes = [x for x in partes if x]
    c = _limpia(clase) or clase
    sin_num = lambda t: re.sub(r"^\d+(\s*[-.]\s*|\s+)", "", t).strip().lower()
    if partes and (sin_num(c) == sin_num(partes[-1]) or c.lower() == partes[-1].lower()):
        nom = " - ".join(partes)
    else:
        nom = " - ".join(partes + [c])
    nom = nom.replace("/", "-")
    if len(nom.encode()) > 120:
        nom = nom.encode()[:120].decode(errors="ignore").rstrip(" -.")
    return nom


def _natural(s):
    return [int(x) if x.isdigit() else x.lower() for x in re.split(r"(\d+)", s)]


def videos(curso):
    """Videos del curso como los ve curso-a-apuntes.sh (rutas relativas, el .es/.en gana, orden natural)."""
    elegido = {}
    for raiz, dirs, archivos in os.walk(curso):
        dirs[:] = [d for d in dirs if d not in ("capturas", "Apuntes", "node_modules") and not d.startswith("capturas-")
                   and d != "codigo-en-imagenes"]
        for a in archivos:
            p = os.path.join(raiz, a)
            low = a.lower()
            es_ts = low.endswith(".ts") and not low.endswith(".d.ts") and os.path.getsize(p) > 5e6
            if not (low.endswith(VIDEO) or es_ts) or low.endswith(".part") or ".temp." in low:
                continue
            rel = os.path.relpath(p, curso)
            clase = re.sub(r"\.[^./]*$", "", rel)
            es = bool(re.search(r"\.(es|en)$", clase))
            clase = re.sub(r"\.(es|en)$", "", clase)
            if clase not in elegido or es:
                elegido[clase] = rel
    return sorted(elegido.values(), key=_natural)


def nombres(curso):
    """{ruta relativa del video: nombre de su carpeta en Apuntes/}"""
    vs = videos(curso)
    dirs = [os.path.dirname(v).split("/") for v in vs]
    dirs = [d for d in dirs if d != [""]]
    pref = os.path.commonprefix(dirs) if dirs else []
    prefijo = "/".join(pref) + "/" if pref and len(dirs) == len(vs) else ""
    usados, out = {}, {}
    for v in vs:
        sub = os.path.dirname(v) or "."
        clase = re.sub(r"\.(es|en)$", "", os.path.splitext(os.path.basename(v))[0])
        base = nom = nombre_corto(prefijo, sub, clase)
        n = 2
        while nom in usados and usados[nom] != v:
            nom, n = f"{base} ({n})", n + 1
        usados[nom] = v
        out[v] = nom
    return out


# ---------------------------------------------------------------------------------------------- arreglos ----
def _firma(d):
    """{ruta relativa: tamaño} de lo que hay en d (sin ocultos)."""
    out = {}
    for raiz, dirs, archivos in os.walk(d):
        dirs[:] = [x for x in dirs if not x.startswith(".")]
        for a in archivos:
            if not a.startswith("."):
                p = os.path.join(raiz, a)
                out[os.path.relpath(p, d)] = os.path.getsize(p)
    return out


def _norm(t):
    return re.sub(r"\s+", " ", t).strip().lower()


class Normalizar:
    def __init__(self, curso, ver):
        self.curso, self.ver, self.hechos = os.path.realpath(curso), ver, []
        self.copias_borradas = []  # rutas relativas de carpetas copia borradas

    def log(self, t):
        self.hechos.append(t)

    def copias(self):
        for raiz, dirs, _ in os.walk(self.curso):
            dirs[:] = sorted(d for d in dirs if d not in SISTEMA and not d.startswith("."))
            for d in list(dirs):
                m = re.match(r"^(.*?) \((\d+)\)$", d)
                if not m or m.group(1) not in dirs:
                    continue
                copia, orig = os.path.join(raiz, d), os.path.join(raiz, m.group(1))
                fc, fo = _firma(copia), _firma(orig)
                faltan = [r for r, t in fc.items() if fo.get(r) != t]
                choques = [r for r in faltan if r in fo]  # mismo nombre, otro tamaño: no se adivina
                rel = os.path.relpath(copia, self.curso)
                if choques:
                    self.log(f"⚠️ NO se toca {rel}: {len(choques)} archivos con el mismo nombre y otro tamaño que en la original")
                    continue
                gb = sum(fc.values()) / 1e9
                self.log(f"copia repetida {rel} ({len(fc)} archivos, {gb:.1f} GB)"
                         + (f": {len(faltan)} que faltaban pasan a la original" if faltan else ": todo ya estaba en la original"))
                self.copias_borradas.append(rel)
                dirs.remove(d)
                if self.ver:
                    continue
                for r in faltan:
                    os.makedirs(os.path.dirname(os.path.join(orig, r)), exist_ok=True)
                    shutil.move(os.path.join(copia, r), os.path.join(orig, r))
                shutil.rmtree(copia)

    def anidadas(self):
        """D/D/… → D/… (solo si D no tiene nada más que la carpeta de igual nombre, sin contar lo del sistema)."""
        cambios = True
        while cambios:
            cambios = False
            for raiz, dirs, archivos in os.walk(self.curso):
                dirs[:] = sorted(d for d in dirs if d not in SISTEMA and not d.startswith("."))
                propios = [a for a in archivos if not a.startswith(".") and not (raiz == self.curso and a in SISTEMA_ARCH)]
                if len(dirs) != 1 or propios or _norm(dirs[0]) != _norm(os.path.basename(raiz)):
                    continue
                interna = os.path.join(raiz, dirs[0])
                hijos = os.listdir(interna)
                if any(os.path.exists(os.path.join(raiz, h)) and h != dirs[0] for h in hijos):
                    self.log(f"⚠️ NO se aplana {os.path.relpath(interna, self.curso)}: choca con algo de afuera")
                    continue
                self.log(f"aplanar {os.path.relpath(interna, self.curso)}/ → {os.path.relpath(raiz, self.curso) if raiz != self.curso else '(raíz)'}")
                if self.ver:
                    dirs[:] = []
                    continue
                tmp = interna + ".__aplanando"
                os.rename(interna, tmp)
                for h in os.listdir(tmp):
                    os.rename(os.path.join(tmp, h), os.path.join(raiz, h))
                os.rmdir(tmp)
                cambios = True
                break

    def apuntes(self):
        return next((os.path.join(self.curso, n) for n in ("Apuntes", "capturas")
                     if os.path.isdir(os.path.join(self.curso, n))), None)

    def sincronizar(self):
        """Carpetas de Apuntes/ cuyo nombre ya no sale de ninguna ruta (alguien renombró un tema después): se emparejan
        con la clase sin carpeta que termina igual ("… - 007 Cargar las tablas"), si es la única."""
        ap = self.apuntes()
        if not ap:
            return
        calc = set(nombres(self.curso).values())
        hay = {d for d in os.listdir(ap) if os.path.isdir(os.path.join(ap, d)) and not d.startswith(".")}
        sueltas, sin = sorted(hay - calc), sorted(calc - hay)
        cola = lambda t: t.rsplit(" - ", 1)[-1].strip().lower()
        n = 0
        for s in sueltas:
            # igual, o uno es el otro cortado (los nombres se truncan a 120 bytes)
            par = lambda a, b: a == b or (min(len(a), len(b)) >= 12 and (a.startswith(b) or b.startswith(a)))
            cand = [c for c in sin if par(cola(c), cola(s))]
            if len(cand) != 1 or sum(1 for x in sueltas if par(cola(x), cola(s))) != 1:
                continue
            n += 1
            sin.remove(cand[0])
            if not self.ver:
                os.rename(os.path.join(ap, s), os.path.join(ap, cand[0]))
                self._enlaces({s: cand[0]})
        if n:
            self.log(f"{n} carpetas de apuntes vueltas a emparejar con su video (tema renombrado)")
        resto = len(sueltas) - n
        if resto:
            self.log(f"⚠️ {resto} carpetas de apuntes sin un video que las genere (revisar a mano)")

    def _enlaces(self, renombres):
        """MAPA.md y codigo-del-curso.md apuntan a Apuntes/<clase>/…: se corrigen cuando una carpeta cambia de nombre."""
        for md in ("MAPA.md", "codigo-del-curso.md"):
            p = os.path.join(self.curso, md)
            if os.path.isfile(p):
                t = open(p, encoding="utf-8").read()
                t2 = t
                for viejo, nuevo in renombres.items():
                    t2 = t2.replace(f"/{viejo}/", f"/{nuevo}/")
                if t2 != t:
                    open(p, "w", encoding="utf-8").write(t2)

    def reparar_enlaces(self):
        """Enlaces de MAPA.md / codigo-del-curso.md a Apuntes/<clase>/ que ya no existen: se apuntan a la carpeta real
        que termina igual (misma clase, nombre largo o cortado distinto). Si no hay una sola candidata, se dejan."""
        ap = self.apuntes()
        if not ap:
            return
        reales = [d for d in os.listdir(ap) if os.path.isdir(os.path.join(ap, d))]
        cola = lambda t: t.rsplit(" - ", 1)[-1].strip().lower()
        base = os.path.basename(ap)
        n = 0
        for md in ("MAPA.md", "codigo-del-curso.md"):
            p = os.path.join(self.curso, md)
            if not os.path.isfile(p):
                continue
            t = open(p, encoding="utf-8").read()
            def arreglar(m):
                nonlocal n
                carpeta = m.group(2)
                if os.path.isdir(os.path.join(ap, carpeta)):
                    return m.group(0)
                c = [r for r in reales if cola(r) == cola(carpeta) or (len(cola(carpeta)) >= 12 and (cola(r).startswith(cola(carpeta)) or cola(carpeta).startswith(cola(r))))]
                if len(c) != 1:
                    return m.group(0)
                n += 1
                return f"{m.group(1)}{c[0]}/"
            t2 = re.sub(r"(\]\(<?(?:%s|capturas|Apuntes)/)([^/>]+)/" % re.escape(base), arreglar, t)
            if t2 != t and not self.ver:
                open(p, "w", encoding="utf-8").write(t2)
        if n:
            self.log(f"{n} enlaces de MAPA/código vueltos a apuntar a su clase")

    def envoltorio(self):
        """<curso>/<otra carpeta>/… cuando la raíz no tiene nada más (típico de descomprimir "X_part01.zip" → carpeta "X"):
        sube el contenido un nivel. Los nombres de Apuntes/ no cambian (nombres() ya quita el prefijo común)."""
        hijos = [h for h in os.listdir(self.curso) if not h.startswith(".")]
        dirs = [h for h in hijos if os.path.isdir(os.path.join(self.curso, h)) and h not in SISTEMA]
        otros = [h for h in hijos if h not in dirs and h not in SISTEMA and h not in SISTEMA_ARCH]
        if len(dirs) != 1 or otros or _norm(dirs[0]) == _norm(os.path.basename(self.curso)):
            return
        interna = os.path.join(self.curso, dirs[0])
        sub = os.listdir(interna)
        if not any(os.path.isdir(os.path.join(interna, x)) for x in sub) or any(os.path.exists(os.path.join(self.curso, x)) for x in sub):
            return
        self.log(f"subir el contenido de «{dirs[0]}/» a la raíz del curso")
        if self.ver:
            return
        for x in sub:
            os.rename(os.path.join(interna, x), os.path.join(self.curso, x))
        os.rmdir(interna)

    def correr(self):
        self.envoltorio()
        self.reparar_enlaces()
        antes = nombres(self.curso)
        self.copias()
        self.anidadas()
        if not self.hechos:
            self.sincronizar()
            return
        if self.hechos and not self.apuntes():
            return
        ap = self.apuntes()
        if not ap:
            return
        if self.ver:
            self.log(f"(se renombrarían las carpetas de {os.path.basename(ap)}/ según las rutas nuevas)")
            return
        despues = nombres(self.curso)
        # video viejo → video nuevo: el mismo archivo, con la ruta sin la carpeta repetida / la copia
        def clave(v):
            return os.path.basename(v)
        nuevos_por_base = {}
        for v in despues:
            nuevos_por_base.setdefault(clave(v), []).append(v)
        renombres, borrar, copias = {}, [], []
        for v, viejo in antes.items():
            es_copia = any(v.startswith(c + "/") for c in self.copias_borradas)
            cand = nuevos_por_base.get(clave(v), [])
            # el mismo video en su ruta nueva: misma ruta, o la única con ese nombre de archivo
            nuevo = v if v in despues else (cand[0] if len(cand) == 1 else None)
            if es_copia:
                copias.append((viejo, despues[nuevo] if nuevo else None))
            elif nuevo and despues[nuevo] != viejo:
                renombres[viejo] = despues[nuevo]
        for viejo, destino in copias:
            if not destino:
                borrar.append(viejo)
                continue
            # la original: la carpeta (con su nombre de AHORA) que va a terminar llamándose `destino`
            orig = next((o for o, n in renombres.items() if n == destino), destino)
            if os.path.isfile(os.path.join(ap, orig, "apuntes.md")) or not os.path.isdir(os.path.join(ap, viejo)):
                borrar.append(viejo)
            else:  # la original nunca tuvo apuntes: se aprovechan los de la copia
                renombres.pop(orig, None)
                if os.path.isdir(os.path.join(ap, orig)):
                    borrar.append(orig)
                renombres[viejo] = destino
        n_ren = n_bor = 0
        for viejo in borrar:
            p = os.path.join(ap, viejo)
            if os.path.isdir(p) and viejo not in renombres.values():
                shutil.rmtree(p)
                n_bor += 1
        tmp = {}
        for viejo, nuevo in renombres.items():  # en dos pasos: un nombre nuevo puede ser el viejo de otra clase
            p = os.path.join(ap, viejo)
            if os.path.isdir(p):
                t = p + ".__renombrando"
                os.rename(p, t)
                tmp[t] = os.path.join(ap, nuevo)
        for t, dst in tmp.items():
            if os.path.exists(dst):
                self.log(f"⚠️ ya existía {os.path.basename(dst)}: queda {os.path.basename(t)} para revisar")
                continue
            os.rename(t, dst)
            n_ren += 1
        if n_bor:
            self.log(f"{n_bor} carpetas de apuntes repetidos borradas")
        if n_ren:
            self.log(f"{n_ren} carpetas de apuntes renombradas")
        for md in ("MAPA.md", "codigo-del-curso.md"):
            p = os.path.join(self.curso, md)
            if os.path.isfile(p):
                t = open(p, encoding="utf-8").read()
                t2 = t
                for viejo, nuevo in sorted(renombres.items(), key=lambda x: -len(x[0])):
                    t2 = t2.replace(f"/{viejo}/", f"/{nuevo}/")
                fuera = [f"/{b}/" for b in borrar if b not in renombres]
                t2 = "\n".join(l for l in t2.split("\n") if not any(f in l for f in fuera))
                if t2 != t:
                    open(p, "w", encoding="utf-8").write(t2)
                    self.log(f"enlaces de {md} corregidos")
        self._capturas_de_copias(borrar)
        self.sincronizar()

    def _capturas_de_copias(self, borrar):
        """Las capturas clave/esenciales de las clases repetidas también sobran."""
        if not borrar:
            return
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import importlib.util
        spec = importlib.util.spec_from_file_location("tl", os.path.join(os.path.dirname(os.path.abspath(__file__)), "todas-las-capturas.py"))
        tl = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(tl)
        marcas = tuple(f" {tl.limpio(c)} · " for c in borrar)
        n = 0
        for carpeta in ("capturas-clave", "capturas-esenciales"):
            d = os.path.join(self.curso, carpeta)
            if not os.path.isdir(d):
                continue
            for f in os.listdir(d):
                if any(m in f for m in marcas):
                    os.remove(os.path.join(d, f))
                    n += 1
        if n:
            self.log(f"{n} capturas de clases repetidas borradas")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    ver = "--ver" in sys.argv
    for c in args:
        n = Normalizar(c, ver)
        n.correr()
        print(f"{'(simulación) ' if ver else ''}{os.path.basename(n.curso)}:")
        for h in n.hechos or ["estructura bien"]:
            print(f"  · {h}")


if __name__ == "__main__":
    main()
