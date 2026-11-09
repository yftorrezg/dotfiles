#!/usr/bin/env python3
"""ordenar-curso.py <carpeta del curso> [--ver]
Deja un curso ordenado y sin ruido (v10, 08/11/2026). Lo corre el final de SUPER+ALT+A / SUPER+ALT+Y y sirve para los
cursos ya hechos. Idempotente: correrlo dos veces no cambia nada. --ver: solo dice qué haría.

Cómo queda un curso:
  <curso>/
    01 - Tema/ …                videos, PDF, código del curso (los subtítulos .srt quedan ocultos con .hidden)
    Apuntes/<clase>/            apuntes.md · tarjetas.md · transcripcion.md · resumen.md (solo clases de 20+ min)
    capturas-clave/             las capturas que valen la pena (≈1,8 por minuto)
    capturas-esenciales/        la mitad de las clave, para repasar apurado
    codigo-en-imagenes/         código y PDF del curso en imágenes (solo si el curso los trae)
    codigo-del-curso.md         todo el código del curso en un solo archivo (ídem)
    MAPA.md                     mapa por módulo (cursos de 30+ clases)

Qué hace:
  1. capturas/ → Apuntes/ (y corrige los enlaces de MAPA.md y codigo-del-curso.md).
  2. Arma capturas-clave/ y capturas-esenciales/ si alguna clase tiene sus capturas sueltas, y después borra las
     sueltas (quedan las clave/esenciales; el texto OCR sigue guardado en .ocr-capturas.json).
  3. Borra todas-las-capturas/ (1 de cada 3 era el mismo editor con el cursor movido) y la basura de versiones
     anteriores (.antes-*, marcas, candados, logs de regeneración).
  4. Oculta los subtítulos (.srt/.vtt) y tarjetas-anki.txt con un archivo .hidden (Dolphin no los muestra; mpv y los
     scripts los siguen usando: borrarlos obligaría a volver a transcribir).
Sin respaldos, a propósito: lo único que importa son los videos, y de ellos sale todo lo demás."""
import os, re, shutil, sys
from pathlib import Path

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

IMG = (".webp", ".png", ".jpg", ".jpeg")
SUBS = (".srt", ".vtt", ".ass")
VIDEO = (".mp4", ".mkv", ".webm", ".mov", ".avi", ".ts")
BASURA_CURSO = ("regeneracion.log", "resultado-regeneracion.json", ".INDICE-viejo.md")
CARPETAS_FUERA = ("todas-las-capturas", "capturas-estudio-codigos")
BASURA_CLASE = re.compile(r"^\.(antes-.*|version-anterior.*|saneado-v\d+|regenerado-v\d+|mejorando\.lock|regenerando\.lock|"
                          r"INDICE-viejo\.md|sin-voz|.*\.tmp)$")
OCULTAR_CLASE = re.compile(r"^(subtitulos.*\.(srt|vtt)|tarjetas-anki\.txt)$")
NO_ENTRAR = {"Apuntes", "capturas", "capturas-clave", "capturas-esenciales", "todas-las-capturas", "codigo-en-imagenes",
             "capturas-estudio-codigos", "node_modules", ".git", "__pycache__"}


class Orden:
    def __init__(self, curso, ver):
        self.curso, self.ver, self.hechos = Path(curso).resolve(), ver, []

    def hacer(self, que, fn=None):
        self.hechos.append(que)
        if not self.ver and fn:
            fn()

    # 1 ---------------------------------------------------------------------------------------------------------
    def migrar(self):
        viejo, nuevo = self.curso / "capturas", self.curso / "Apuntes"
        if not viejo.is_dir() or nuevo.exists():
            return
        if not any((d / "apuntes.md").is_file() or (d / ".apuntes-ia.json").is_file() for d in viejo.iterdir() if d.is_dir()):
            return
        self.hacer("capturas/ → Apuntes/", lambda: viejo.rename(nuevo))
        for md in ("MAPA.md", "codigo-del-curso.md"):
            p = self.curso / md
            if p.is_file():
                def fix(p=p):
                    t = p.read_text(encoding="utf-8")
                    p.write_text(re.sub(r"\]\((<?)capturas/", r"](\1Apuntes/", t), encoding="utf-8")
                self.hacer(f"enlaces de {md} → Apuntes/", fix)

    def apuntes(self):
        return next((self.curso / n for n in ("Apuntes", "capturas") if (self.curso / n).is_dir()), None)

    # 2 ---------------------------------------------------------------------------------------------------------
    def capturas(self):
        ap = self.apuntes()
        if not ap:
            return
        con_img = [d for d in ap.iterdir() if d.is_dir() and any(f.suffix.lower() in IMG for f in d.iterdir() if f.is_file())]
        if not con_img:
            return
        self.hacer(f"capturas-clave/ y capturas-esenciales/ de {len(con_img)} clases con capturas sueltas")
        if self.ver:
            self.hechos.append(f"borrar las capturas sueltas de {len(con_img)} clases")
            return
        import capturas_clave
        try:
            capturas_clave.procesar(str(ap))
        except SystemExit as e:  # sin tesseract: no se borra nada
            print(f"capturas clave: {e} — las capturas sueltas se conservan")
            return
        if not (self.curso / "capturas-clave").is_dir():
            return
        n = 0
        for d in con_img:
            for f in d.iterdir():
                if f.is_file() and f.suffix.lower() in IMG:
                    f.unlink()
                    n += 1
        self.hechos.append(f"{n} capturas sueltas borradas (las que valen están en capturas-clave/)")

    # 3 ---------------------------------------------------------------------------------------------------------
    def basura(self):
        for n in CARPETAS_FUERA:
            p = self.curso / n
            if p.is_dir():
                self.hacer(f"borrar {n}/ ({sum(1 for _ in p.iterdir())} archivos)", lambda p=p: shutil.rmtree(p))
        for n in BASURA_CURSO:
            p = self.curso / n
            if p.exists():
                self.hacer(f"borrar {n}", p.unlink)
        self._codigo_duplicado()
        ap = self.apuntes()
        n = 0
        for d in (ap.iterdir() if ap else []):
            if not d.is_dir():
                continue
            for f in d.iterdir():
                if BASURA_CLASE.match(f.name):
                    n += 1
                    if not self.ver:
                        shutil.rmtree(f) if f.is_dir() else f.unlink()
        if n:
            self.hechos.append(f"{n} restos de versiones anteriores en las clases")
        for sub in self._carpetas_de_videos():  # restos de versiones de antes dentro de cada tema
            for nombre in ("capturas", "todas-las-capturas", "capturas-clave", "capturas-esenciales"):
                p = sub / nombre
                if p.is_dir() and sub != self.curso and not any(p.rglob("apuntes.md")):
                    self.hacer(f"borrar {p.relative_to(self.curso)}/ (resto de una versión anterior)", lambda p=p: shutil.rmtree(p))
        for p in self.curso.glob("auditoria-*.json"):
            self.hacer(f"borrar {p.name}", p.unlink)
        cod = self.curso / "codigo-del-curso.md"
        if cod.is_file() and cod.stat().st_size < 600 and "```" not in cod.read_text(encoding="utf-8", errors="ignore") and "](" not in cod.read_text(encoding="utf-8", errors="ignore"):
            self.hacer("borrar codigo-del-curso.md (vacío: el curso no trae código)", cod.unlink)

    def _codigo_duplicado(self):
        """CODIGO-COMPLETO-*.md hecho a mano: sobra si codigo-del-curso.md ya tiene todas sus líneas de código."""
        nuevo = self.curso / "codigo-del-curso.md"
        if not nuevo.is_file():
            return
        def lineas(p):
            bl = re.findall(r"```[^\n]*\n(.*?)```", p.read_text(encoding="utf-8", errors="ignore"), re.S)
            return {re.sub(r"\s+", " ", x).strip() for b in bl for x in b.split("\n") if x.strip()}
        tiene = lineas(nuevo)
        for p in self.curso.glob("CODIGO-COMPLETO*.md"):
            if lineas(p) <= tiene:
                self.hacer(f"borrar {p.name} (codigo-del-curso.md ya tiene todo)", p.unlink)
            else:
                print(f"(se conserva {p.name}: tiene código que codigo-del-curso.md no)")

    # 4 ---------------------------------------------------------------------------------------------------------
    def _carpetas_de_videos(self):
        for raiz, dirs, archivos in os.walk(self.curso):
            dirs[:] = sorted(d for d in dirs if d not in NO_ENTRAR and not d.startswith("."))
            if any(a.lower().endswith(VIDEO + SUBS) for a in archivos):
                yield Path(raiz)

    def _ocultar(self, carpeta, nombres):
        nombres = sorted(nombres)
        if not nombres:
            return 0
        h = carpeta / ".hidden"
        previo = set(h.read_text(encoding="utf-8").split("\n")) if h.is_file() else set()
        faltan = [n for n in nombres if n not in previo]
        if faltan and not self.ver:
            h.write_text("\n".join(sorted(previo - {""} | set(nombres))) + "\n", encoding="utf-8")
        return len(faltan)

    COLORES = {"Apuntes": "folder-red", "capturas-clave": "folder-yellow", "capturas-esenciales": "folder-yellow",
               "codigo-en-imagenes": "folder-green"}

    def colores(self):
        """Colores de Dolphin (.directory): apuntes rojo, capturas amarillo, código verde (los eligió el usuario)."""
        n = 0
        for carpeta, icono in self.COLORES.items():
            p = self.curso / carpeta
            if not p.is_dir():
                continue
            d = p / ".directory"
            if d.is_file() and f"Icon={icono}" in d.read_text(encoding="utf-8", errors="ignore"):
                continue
            n += 1
            if not self.ver:
                d.write_text(f"[Desktop Entry]\nIcon={icono}\n", encoding="utf-8")
        if n:
            self.hechos.append(f"{n} carpetas con su color")

    def ocultar(self):
        n = sum(self._ocultar(d, [a.name for a in d.iterdir() if a.is_file() and a.suffix.lower() in SUBS])
                for d in self._carpetas_de_videos())
        ap = self.apuntes()
        n += sum(self._ocultar(d, [a.name for a in d.iterdir() if OCULTAR_CLASE.match(a.name)])
                 for d in (ap.iterdir() if ap else []) if d.is_dir())
        if n:
            self.hechos.append(f"{n} subtítulos/archivos técnicos ocultos (.hidden)")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    ver = "--ver" in sys.argv
    for c in args:
        o = Orden(c, ver)
        if not o.curso.is_dir():
            print(f"No existe: {c}")
            continue
        o.migrar()
        o.capturas()
        o.basura()
        o.ocultar()
        o.colores()
        print(f"{'(simulación) ' if ver else ''}{o.curso.name}:")
        for h in o.hechos or ["ya estaba ordenado"]:
            print(f"  · {h}")


if __name__ == "__main__":
    main()
