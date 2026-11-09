#!/usr/bin/env python3
"""Pruebas del panel de notas:  python3 tests.py   (usan carpetas temporales; no tocan tus notas)."""
import sys
sys.dont_write_bytecode = True
import atexit, datetime, os, shutil, sys, tempfile, unittest

TMP = tempfile.mkdtemp(prefix="notas-test-")
atexit.register(shutil.rmtree, TMP, ignore_errors=True)
os.environ["NOTAS_RAIZ"] = os.path.join(TMP, "boveda", "Notas de videos")
os.environ["NOTAS_IMPORTANTES"] = os.path.join(TMP, "importantes.json")
os.environ["NOTAS_CLASES"] = os.path.join(TMP, "boveda", "Capturas de YouTube")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import servidor as S  # noqa: E402

os.makedirs(S.RAIZ, exist_ok=True)


def foto(nombre="x.jpg"):
    ruta = os.path.join(TMP, nombre)
    open(ruta, "wb").write(b"\xff\xd8\xff\xd9")
    return ruta


class Tipos(unittest.TestCase):
    def test_prefijos(self):
        self.assertEqual(S.separar_tipo("? por qué className"), ("?", "por qué className"))
        self.assertEqual(S.separar_tipo("!useEffect limpia"), ("!", "useEffect limpia"))
        self.assertEqual(S.separar_tipo("p hacer el ejercicio"), ("p", "hacer el ejercicio"))
        self.assertEqual(S.separar_tipo("¿Qué es un hook?"), ("?", "¿Qué es un hook?"))
        self.assertEqual(S.separar_tipo("pantalla completa"), ("", "pantalla completa"))  # 'p' sin espacio no cuenta
        self.assertEqual(S.separar_tipo("  Hooks  "), ("", "Hooks"))


class Repaso(unittest.TestCase):
    def test_leitner(self):
        n = {"intervalo": 1}
        for esperado in (2, 4, 8, 16, 32, 60, 60):
            S.siguiente_repaso(n, True)
            self.assertEqual(n["intervalo"], esperado)
        S.siguiente_repaso(n, False)
        self.assertEqual(n["intervalo"], 1)
        self.assertEqual(n["proximo"], (datetime.date.today() + datetime.timedelta(days=1)).isoformat())


class Notas(unittest.TestCase):
    def test_flujo_completo(self):
        v = os.path.join(TMP, "videos", "Curso de Prueba.mp4")
        clase = os.path.join(S.CLASES, "Curso de Prueba")
        os.makedirs(clase)
        S.crear_nota(v, "754.5", "? por qué className", "porque class es palabra reservada", foto("a.jpg"))
        S.crear_nota(v, 100, "!clave", "", foto("b.jpg"))
        S.crear_nota(v, 50, "sin tipo", "", None)
        slug = S.indice()[S.normalizar(v)]
        d = S.cargar(slug)
        self.assertEqual([n["t"] for n in d["notas"]], [50, 100, 754.5])  # ordenadas
        self.assertEqual([n["tipo"] for n in d["notas"]], ["", "!", "?"])
        self.assertEqual(d["notas"][2]["titulo"], "por qué className")
        self.assertTrue(os.path.isfile(os.path.join(S.carpeta(slug), "capturas", "001-754.jpg")))
        # notas.md con insignias
        md = open(os.path.join(S.carpeta(slug), "notas.md"), encoding="utf-8").read()
        self.assertIn("## ⏱ 12:34 — ❓ por qué className", md)
        self.assertIn("## ⏱ 1:40 — 🔑 clave", md)
        # tarjetas: solo las "?" y se releen con el parser del plugin
        tj = open(os.path.join(S.carpeta(slug), "tarjetas.md"), encoding="utf-8").read()
        mod = S._tarjetas_mod()
        self.assertIsNotNone(mod, "falta tarjetas.py")
        cartas = mod.parsear(tj.split(mod.MARCA_MIAS)[0])
        self.assertEqual(len(cartas), 1)
        self.assertIn("¿por qué className?", cartas[0][1])
        self.assertIn("#flashcards/notas/", tj)
        # el progreso del plugin se conserva al regenerar
        tj2 = tj.replace("porque class es palabra reservada\n", "porque class es palabra reservada\n<!--SR:!2026-10-10,4,270-->\n")
        open(os.path.join(S.carpeta(slug), "tarjetas.md"), "w", encoding="utf-8").write(tj2)
        S.crear_nota(v, 200, "? otra duda", "", None)
        self.assertIn("<!--SR:!2026-10-10,4,270-->", open(os.path.join(S.carpeta(slug), "tarjetas.md"), encoding="utf-8").read())
        # mis-notas.md junto al cuadernillo, sin apuntes.md tocado
        mn = open(os.path.join(clase, "mis-notas.md"), encoding="utf-8").read()
        self.assertIn("![[Notas de videos/", mn)
        self.assertFalse(os.path.exists(os.path.join(clase, "apuntes.md")))
        # editar cambia el tipo; borrar quita la captura
        self.assertTrue(S.editar_nota(v, 1, "sin prefijo", "t", "p"))
        self.assertEqual([n["tipo"] for n in S.cargar(slug)["notas"] if n["id"] == 1], ["p"])
        self.assertTrue(S.editar_nota(v, 1, "! ahora clave", "t", None))
        self.assertEqual([n["tipo"] for n in S.cargar(slug)["notas"] if n["id"] == 1], ["!"])
        self.assertTrue(S.borrar_nota(v, 1))
        self.assertFalse(os.path.exists(os.path.join(S.carpeta(slug), "capturas", "001-754.jpg")))

    def test_repaso_pendiente(self):
        v = os.path.join(TMP, "videos", "Otro.mp4")
        S.crear_nota(v, 10, "? algo", "", None)
        S.crear_nota(v, 20, "nota sin tipo", "", None)
        self.assertEqual([n for n in S.repaso_pendiente() if n["nombre"] == "Otro"], [])  # mañana, no hoy
        slug = S.indice()[S.normalizar(v)]
        d = S.cargar(slug)
        d["notas"][0]["proximo"] = datetime.date.today().isoformat()
        d["notas"][1]["proximo"] = datetime.date.today().isoformat()
        S.guardar(slug, d)
        pend = [n for n in S.repaso_pendiente() if n["nombre"] == "Otro"]
        self.assertEqual([n["titulo"] for n in pend], ["algo"])  # la nota sin tipo no entra
        self.assertEqual(S.repasado(v, pend[0]["id"], True), 2)
        self.assertEqual([n for n in S.repaso_pendiente() if n["nombre"] == "Otro"], [])

    def test_buscar_clase_playlist(self):
        d = os.path.join(S.CLASES, "Lista", "capturas", "003 - Mi Video Único")
        os.makedirs(d)
        self.assertEqual(S.buscar_clase("Mi video único!"), d)
        self.assertIsNone(S.buscar_clase("No existe"))


class Marcas(unittest.TestCase):
    def test_sabido_y_dudo_se_excluyen(self):
        v = os.path.join(TMP, "curso", "01 - A", "001. x.mp4")
        self.assertEqual(S.alternar_marca(v, "imp"), ["imp"])
        self.assertEqual(S.alternar_marca(v, "dudo"), ["imp", "dudo"])
        self.assertEqual(S.alternar_marca(v, "sabido"), ["imp", "sabido"])  # sabido quita dudo
        self.assertEqual(S.alternar_marca(v, "dudo"), ["imp", "dudo"])      # y al revés
        self.assertEqual(S.alternar_marca(v, "imp"), ["dudo"])
        self.assertEqual(S.alternar_marca(v, "dudo"), [])
        self.assertNotIn(v, S.importantes())                                # sin marcas no queda rastro
        self.assertIsNone(S.alternar_marca(v, "otra"))

    def test_entrada_vieja_cuenta_como_importante(self):
        self.assertEqual(S.marcas_de({"/a.mp4": {"curso": "/", "cuando": "2026-11-08"}}, "/a.mp4"), ["imp"])


class Apuntes(unittest.TestCase):
    def test_tarjetas(self):
        md = """# 🃏 Tarjetas: x

#flashcards/x

## 🖨️ ¿Qué imprime?

¿Qué hace esto?
```sql
SELECT 1
?
FROM dual;
```
?
Devuelve 1.

## ✍️ Mis tarjetas

*Tus tarjetas (pregunta, una línea con `?` sola…)*

Capital de Perú::Lima

Sin respuesta
"""
        t = S.parsear_tarjetas(md)
        self.assertEqual(len(t), 2)
        self.assertTrue(t[0]["q"].startswith("¿Qué hace esto?") and "FROM dual;" in t[0]["q"])  # un «?» dentro del código no corta
        self.assertEqual(t[0]["a"], "Devuelve 1.")
        self.assertEqual((t[1]["q"], t[1]["a"], t[1]["sec"]), ("Capital de Perú", "Lima", "✍️ Mis tarjetas"))

    def test_apuntes_de_clase(self):
        raiz = os.path.join(TMP, "c2")
        v = os.path.join(raiz, "10 - Cursores", "009. Cursores con parámetros.mp4")
        os.makedirs(os.path.dirname(v))
        d = os.path.join(raiz, "Apuntes", "10 - Cursores - 009 Cursores con parámetros")
        os.makedirs(d)
        open(os.path.join(d, "apuntes.md"), "w").write("x")
        os.makedirs(os.path.join(raiz, "capturas-clave"))
        open(os.path.join(raiz, "capturas-clave", "002 10 - Cursores - 009 Cursores con parámetros · 0001 · 00-00-18.webp"), "w").write("")
        open(os.path.join(raiz, "capturas-clave", "003 10 - Cursores - 010 Otra · 0001 · 00-00-18.webp"), "w").write("")
        a = S.apuntes_de(v)
        self.assertEqual(a["dir"], d)
        self.assertEqual(len(a["extras"]), 1)  # solo las capturas de ESTA clase
        self.assertEqual(S.raiz_curso(v), raiz)


class Recorte(unittest.TestCase):
    def test_srt_se_desplaza_y_recorta(self):
        r = os.path.join(TMP, "a.es.srt")
        open(r, "w", encoding="utf-8").write("1\n00:00:05,000 --> 00:00:08,000\nantes\n\n2\n00:00:30,000 --> 00:00:33,000\ndentro\n\n3\n00:01:30,000 --> 00:01:33,000\ndespués\n")
        antes, S.a_papelera = S.a_papelera, lambda ruta: None
        try:
            S.cortar_srt(r, 10, 50)
        finally:
            S.a_papelera = antes
        t = open(r, encoding="utf-8").read()
        self.assertIn("00:00:20,000 --> 00:00:23,000", t)
        self.assertIn("dentro", t)
        self.assertNotIn("antes", t)
        self.assertNotIn("después", t)


class ApuntesYCapturasDelCurso(unittest.TestCase):
    """El panel (tecla i / Shift+I) encuentra los apuntes y las capturas de CUALQUIER video: nombres con '@Canal', 'NN.', punto final,
    nombres largos recortados, y las capturas siguen al minuto actual. Regresión del 09/11/2026 (decía 'sin apuntes' y mostraba la 1.ª captura)."""

    def curso(self, videos):
        raiz = os.path.join(TMP, "curso-" + str(len(os.listdir(TMP))))
        for v, mins in videos:
            os.makedirs(os.path.join(raiz, os.path.dirname(v)), exist_ok=True)
            open(os.path.join(raiz, v), "wb").write(b"x" * 10)
        os.makedirs(os.path.join(raiz, "Apuntes"))
        return raiz

    def hacer(self, raiz, video, minutos):
        n = S.carpeta_de_apuntes(raiz, os.path.join(raiz, video))
        os.makedirs(os.path.join(raiz, "Apuntes", n), exist_ok=True)
        open(os.path.join(raiz, "Apuntes", n, "apuntes.md"), "w").write("# x")
        for conj in ("clave", "esenciales"):
            d = os.path.join(raiz, "capturas-" + conj)
            os.makedirs(d, exist_ok=True)
            for k, t in enumerate(minutos, 1):
                open(os.path.join(d, f"001 {S._limpio_captura(n)} · {k:04d} · 00-{t:02d}-00.webp"), "wb").write(b"i")
        return n

    def test_nombres_dificiles(self):
        vids = [("06. Spec Driven _ Design/07. Opcional - Bloquear rama principal. @RecursosCompartidosOficial.mp4", 1),
                ("06. Spec Driven _ Design/08. Otra clase con un nombre larguísimo " + "palabra " * 14 + "@RecursosCompartidosOficial.mp4", 1),
                ("01. Intro/01. Introducción: ¿qué es?.mp4", 1)]
        raiz = self.curso(vids)
        for v, _ in vids:
            n = self.hacer(raiz, v, (1, 5, 9))
            a = S.apuntes_de(os.path.join(raiz, v))
            self.assertEqual(a["clase"], n, v)
            self.assertIn("apuntes.md", a["archivos"])
            self.assertEqual(len(a["extras"]), 6, v)  # clave + esenciales

    def test_capturas_siguen_al_minuto(self):
        v = "02 Tema/03. Clase de prueba. @Canal.mp4"
        raiz = self.curso([(v, 1)])
        self.hacer(raiz, v, (1, 5, 9))
        ruta = os.path.join(raiz, v)
        S.lista_reproduccion = lambda: [{"i": 0, "nombre": "x", "ruta": ruta, "actual": True, "dur": 0}]
        S.ipc = lambda *a, **k: 5 * 60
        d = S.capturas_de(0, "clave", 5 * 60)
        self.assertIsNotNone(d["cerca"])
        self.assertIn("00-05-00", d["items"][d["cerca"]]["f"])  # la captura del minuto 5, no la primera
        d = S.capturas_de(0, "clave", 9 * 60 + 20)
        self.assertIn("00-09-00", d["items"][d["cerca"]]["f"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
