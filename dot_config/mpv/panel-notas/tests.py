#!/usr/bin/env python3
"""Pruebas del panel de notas:  python3 tests.py   (usan carpetas temporales; no tocan tus notas)."""
import sys
sys.dont_write_bytecode = True
import atexit, datetime, os, shutil, sys, tempfile, unittest

TMP = tempfile.mkdtemp(prefix="notas-test-")
atexit.register(shutil.rmtree, TMP, ignore_errors=True)
os.environ["NOTAS_RAIZ"] = os.path.join(TMP, "boveda", "Notas de videos")
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
