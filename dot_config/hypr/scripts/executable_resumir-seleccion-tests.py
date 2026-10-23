#!/usr/bin/env python3
"""Pruebas de resumen, formato, chunking y salida de OpenCode sin red ni GTK."""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest.mock import patch


MODULE_PATH = Path(__file__).with_name("resumir_seleccion.py")


def load_summarizer():
    if not MODULE_PATH.is_file():
        raise AssertionError("El motor de resumen aún no está instalado")
    spec = importlib.util.spec_from_file_location("resumir_seleccion", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError("No se pudo cargar el motor de resumen")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SAMPLE_SUMMARY = {
    "titulo": "Cómo se relacionan presión y profundidad",
    "idea": "La presión de un fluido aumenta al aumentar la profundidad.",
    "puntos": [
        {"emoji": "🌊", "texto": "Las capas superiores ejercen peso sobre las inferiores."},
        {"emoji": "📈", "texto": "Más profundidad implica más fluido encima y mayor presión."},
    ],
    "explicacion": "La causa es el peso acumulado del fluido; por eso la presión crece hacia abajo.",
    "pasos": [{"titulo": "Compara", "detalle": "Observa la profundidad de cada punto."}],
    "tabla": {
        "encabezados": ["Punto", "Profundidad"],
        "filas": [["A", "poca"], ["B", "mucha | mayor presión"]],
    },
    "ejemplo": "Una persona siente más presión en los oídos al bucear más profundo.",
    "terminos": [{"termino": "Presión", "definicion": "Fuerza ejercida por unidad de área."}],
    "conclusion": "La profundidad permite anticipar cómo cambia la presión.",
    "pregunta": {"pregunta": "¿Por qué aumenta la presión?", "respuesta": "Por el peso del fluido que queda encima."},
}


class SelectionTextTests(unittest.TestCase):
    def test_normalize_selection_preserves_paragraphs_and_normalizes_line_endings(self):
        module = load_summarizer()
        self.assertEqual(
            module.normalize_selection("  Primer párrafo.\r\n\r\nSegundo párrafo.\x00  "),
            "Primer párrafo.\n\nSegundo párrafo.",
        )

    def test_normalize_selection_rejects_text_over_the_limit(self):
        module = load_summarizer()
        with self.assertRaisesRegex(ValueError, "4"):
            module.normalize_selection("cinco!", max_chars=4)

    def test_split_text_respects_chunk_limit_without_losing_words_or_order(self):
        module = load_summarizer()
        text = "Primero empieza.\n\n" + ("Una frase larga conserva todas sus palabras. " * 3) + "\n\nAl final termina."

        chunks = module.split_text(text, max_chars=38)

        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(0 < len(chunk) <= 38 for chunk in chunks))
        self.assertEqual(text.split(), " ".join(chunks).split())

    def test_overlapping_monitors_choose_the_focused_monitor_under_the_cursor(self):
        module = load_summarizer()
        monitors = [
            {"name": "HDMI-A-1", "x": 0, "y": 0, "width": 1920, "height": 1080, "focused": False},
            {"name": "DP-3", "x": 1080, "y": 148, "width": 1920, "height": 1080, "focused": True},
        ]

        selected = module.select_monitor_at_position(monitors, 1631, 755)

        self.assertEqual(selected["name"], "DP-3")


class SelectionCaptureTests(unittest.TestCase):
    def test_brave_selection_is_copied_and_image_clipboard_is_restored(self):
        spec = importlib.util.spec_from_file_location(
            "traducir_seleccion", Path(__file__).with_name("traducir_seleccion.py")
        )
        translator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(translator)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            clipboard_file = root / "clipboard.bin"
            types_file = root / "clipboard-types.txt"
            selection_file = root / "selection.txt"
            clipboard_file.write_bytes(b"\x89PNG\r\n\x1a\nimage bytes")
            types_file.write_text("image/png\n", encoding="utf-8")
            selection_file.write_text("Texto seleccionado en Brave", encoding="utf-8")

            fake_tool = bin_dir / "clipboard-tool"
            fake_tool.write_text(
                "#!/usr/bin/env python3\n"
                "import json, os, sys\n"
                "from pathlib import Path\n"
                "name = Path(sys.argv[0]).name\n"
                "clipboard = Path(os.environ['CLIPBOARD_FILE'])\n"
                "types = Path(os.environ['CLIPBOARD_TYPES_FILE'])\n"
                "selection = Path(os.environ['SELECTION_FILE'])\n"
                "args = sys.argv[1:]\n"
                "if name == 'hyprctl':\n"
                "  print(json.dumps({'class':'brave-browser'}))\n"
                "elif name == 'wl-paste':\n"
                "  if '--list-types' in args: sys.stdout.write(types.read_text())\n"
                "  elif '--primary' in args: sys.exit(1)\n"
                "  else: sys.stdout.buffer.write(clipboard.read_bytes())\n"
                "elif name == 'wl-copy':\n"
                "  if '--clear' in args:\n"
                "    clipboard.write_bytes(b''); types.write_text('')\n"
                "  else:\n"
                "    clipboard.write_bytes(sys.stdin.buffer.read())\n"
                "    mime = args[args.index('--type') + 1] if '--type' in args else 'text/plain;charset=utf-8'\n"
                "    types.write_text(mime + '\\n')\n"
                "elif name == 'ydotool':\n"
                "  clipboard.write_bytes(selection.read_bytes())\n"
                "  types.write_text('text/plain;charset=utf-8\\n')\n"
                "else: sys.exit(2)\n",
                encoding="utf-8",
            )
            fake_tool.chmod(0o755)
            for name in ("hyprctl", "wl-paste", "wl-copy", "ydotool"):
                (bin_dir / name).symlink_to(fake_tool)

            original_image = clipboard_file.read_bytes()
            with patch.dict(
                os.environ,
                {
                    "PATH": f"{bin_dir}:/usr/bin:/bin",
                    "CLIPBOARD_FILE": str(clipboard_file),
                    "CLIPBOARD_TYPES_FILE": str(types_file),
                    "SELECTION_FILE": str(selection_file),
                },
            ):
                selected = translator.capture_selection()

            self.assertEqual(selected, "Texto seleccionado en Brave")
            self.assertEqual(clipboard_file.read_bytes(), original_image)
            self.assertEqual(types_file.read_text(encoding="utf-8"), "image/png\n")

    def test_capture_retries_ctrl_c_until_the_shortcut_modifiers_are_released(self):
        spec = importlib.util.spec_from_file_location(
            "traducir_seleccion", Path(__file__).with_name("traducir_seleccion.py")
        )
        translator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(translator)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            clipboard_file = root / "clipboard.txt"
            count_file = root / "ydotool-count.txt"
            selection_file = root / "selection.txt"
            clipboard_file.write_text("")
            count_file.write_text("0")
            selection_file.write_text("Texto copiado al segundo intento", encoding="utf-8")

            fake_tool = bin_dir / "tool"
            fake_tool.write_text(
                "#!/usr/bin/env python3\n"
                "import json, os, sys\n"
                "from pathlib import Path\n"
                "name = Path(sys.argv[0]).name\n"
                "clip = Path(os.environ['CLIPBOARD_FILE'])\n"
                "cnt = Path(os.environ['COUNT_FILE'])\n"
                "sel = Path(os.environ['SELECTION_FILE'])\n"
                "args = sys.argv[1:]\n"
                "if name == 'hyprctl':\n"
                "  print(json.dumps({'class':'brave-browser'}))\n"
                "elif name == 'wl-paste':\n"
                "  if '--list-types' in args: pass\n"
                "  elif '--primary' in args: sys.exit(1)\n"
                "  else: sys.stdout.write(clip.read_text())\n"
                "elif name == 'wl-copy':\n"
                "  if '--clear' in args: clip.write_text('')\n"
                "  else: clip.write_text(sys.stdin.read())\n"
                "elif name == 'ydotool':\n"
                "  n = int(cnt.read_text()) + 1\n"
                "  cnt.write_text(str(n))\n"
                "  if n >= 2: clip.write_text(sel.read_text())\n"
                "else: sys.exit(2)\n",
                encoding="utf-8",
            )
            fake_tool.chmod(0o755)
            for name in ("hyprctl", "wl-paste", "wl-copy", "ydotool"):
                (bin_dir / name).symlink_to(fake_tool)

            with (
                patch.dict(
                    os.environ,
                    {
                        "PATH": f"{bin_dir}:/usr/bin:/bin",
                        "CLIPBOARD_FILE": str(clipboard_file),
                        "COUNT_FILE": str(count_file),
                        "SELECTION_FILE": str(selection_file),
                    },
                ),
                patch.object(translator.time, "sleep", return_value=None),
            ):
                selected = translator.capture_selection()
                copies = int(count_file.read_text())

        self.assertEqual(selected, "Texto copiado al segundo intento")
        self.assertGreaterEqual(copies, 2)


class SummaryResponseTests(unittest.TestCase):
    def test_prompt_sets_a_tight_word_budget_and_discourages_repetition(self):
        module = load_summarizer()
        text = " ".join(["palabra"] * 82)

        prompt = module.build_prompt(text)

        self.assertEqual(module.summary_word_budget(text), 21)
        self.assertIn("máximo 21 palabras", prompt)
        self.assertIn("No repitas", prompt)

    def test_compaction_respects_the_length_of_a_short_three_word_selection(self):
        module = load_summarizer()
        text = "React crea interfaces"

        compact = module.compact_summary(SAMPLE_SUMMARY, text)

        self.assertLessEqual(module.summary_word_count(compact), 3)

    def test_verbose_model_output_is_compacted_before_return_and_cache(self):
        module = load_summarizer()
        text = " ".join(["original"] * 82)
        calls = []
        config = {"modelos": ["modelo-test"], "chunk_chars": 20_000, "cache_days": 7}

        def model_runner(prompt, _config):
            calls.append(prompt)
            return SAMPLE_SUMMARY

        with tempfile.TemporaryDirectory() as cache_dir:
            summary, from_cache = module.generate_summary(
                text, config=config, model_call=model_runner, cache_dir=cache_dir
            )
            cached_summary, cached = module.generate_summary(
                text,
                config=config,
                model_call=lambda *_args: self.fail("el resumen compacto debió salir de caché"),
                cache_dir=cache_dir,
            )

        self.assertFalse(from_cache)
        self.assertTrue(cached)
        self.assertEqual(len(calls), 1)
        self.assertLessEqual(module.summary_word_count(summary), 21)
        self.assertEqual(cached_summary, summary)
        self.assertIsNone(summary["pregunta"])
        self.assertFalse(summary["conclusion"])

    def test_default_chunk_size_reduces_model_round_trips_for_long_selections(self):
        module = load_summarizer()
        calls = []
        text = "palabra " * 7_500

        self.assertEqual(module.DEFAULT_CONFIG["chunk_chars"], 20_000)
        self.assertEqual(module.load_config()["chunk_chars"], 20_000)

        def model_runner(prompt, _config):
            calls.append(prompt)
            return SAMPLE_SUMMARY

        module.generate_summary(
            text,
            config={"modelos": ["modelo-test"], "chunk_chars": 20_000, "cache_days": 0},
            model_call=model_runner,
        )

        self.assertEqual(len(calls), 4, "60.000 caracteres requieren 3 fragmentos y 1 integración")

    def test_parser_extracts_summary_json_surrounded_by_prose_and_fences(self):
        module = load_summarizer()
        raw = "Resultado:\n```json\n" + json.dumps(SAMPLE_SUMMARY, ensure_ascii=False) + "\n```"

        parsed = module.parse_summary_response(raw)

        self.assertEqual(parsed["idea"], SAMPLE_SUMMARY["idea"])
        self.assertEqual(parsed["puntos"][1]["emoji"], "📈")
        self.assertEqual(parsed["tabla"]["filas"][1][1], "mucha | mayor presión")

    def test_parser_rejects_invalid_or_empty_summary_instead_of_showing_garbage(self):
        module = load_summarizer()
        with self.assertRaisesRegex(ValueError, "JSON|idea|puntos"):
            module.parse_summary_response("No es un resumen estructurado")

    def test_opencode_jsonl_parser_returns_only_completed_assistant_text(self):
        module = load_summarizer()
        output = "\n".join(
            json.dumps(event)
            for event in (
                {"type": "step_start", "part": {"type": "step-start"}},
                {"type": "text", "part": {"type": "text", "text": "{\"idea\":\"La idea\"}"}},
                {"type": "step_finish", "part": {"type": "step-finish"}},
            )
        )

        self.assertEqual(module.extract_cli_text(output), '{"idea":"La idea"}')

    def test_long_selection_is_integrated_and_progress_is_reported_for_each_chunk(self):
        module = load_summarizer()
        calls = []
        progress = []

        def model_runner(prompt, _config):
            calls.append(prompt)
            return SAMPLE_SUMMARY

        with tempfile.TemporaryDirectory() as cache_dir:
            summary, from_cache = module.generate_summary(
                "Primero explica la causa. Después muestra el efecto.",
                context={"aplicacion": "Test"},
                config={"modelos": ["modelo-test"], "chunk_chars": 38, "cache_days": 0},
                progress=progress.append,
                model_call=model_runner,
                cache_dir=cache_dir,
            )

        self.assertFalse(from_cache)
        self.assertIn("La presión", summary["idea"])
        self.assertLessEqual(
            module.summary_word_count(summary),
            module.summary_word_budget("Primero explica la causa. Después muestra el efecto."),
        )
        self.assertEqual(len(calls), 3)
        self.assertTrue(any("parte 1 de 2" in item for item in progress))
        self.assertIn("Integra estos resúmenes parciales", calls[-1])

    def test_opencode_call_keeps_provider_config_and_deletes_its_temporary_session(self):
        module = load_summarizer()
        with tempfile.TemporaryDirectory() as directory:
            executable = Path(directory) / "opencode"
            cleanup_file = Path(directory) / "deleted-session.txt"
            executable.write_text(
                "#!/usr/bin/env python3\n"
                "import json, os, sys\n"
                "run_args = ['run', '--agent', 'resumidor', '--model', 'model-test', '--format', 'json']\n"
                "if sys.argv[1:] == ['models']:\n"
                "  print('model-test')\n"
                "elif sys.argv[1:2] == ['run']:\n"
                "  if sys.argv[1:] != run_args or os.environ.get('OPENCODE_DB') == ':memory:': sys.exit(3)\n"
                "  if sys.stdin.read() != 'prompt de prueba': sys.exit(4)\n"
                "  response = {'titulo':'Prueba','idea':'La salida llega bien.','puntos':[{'emoji':'✅','texto':'stdin recibido'}]}\n"
                "  event = {'type':'text','sessionID':'ses_testResumen123','part':{'type':'text','text':json.dumps(response, ensure_ascii=False)}}\n"
                "  print(json.dumps(event, ensure_ascii=False))\n"
                "elif sys.argv[1:3] == ['session', 'delete']:\n"
                "  if sys.argv[2:] != ['delete', 'ses_testResumen123']: sys.exit(5)\n"
                "  open(os.environ['SESSION_CLEANUP_FILE'], 'w').write(sys.argv[-1])\n"
                "else: sys.exit(6)\n",
                encoding="utf-8",
            )
            executable.chmod(0o755)

            with (
                patch.object(module.shutil, "which", return_value=str(executable)),
                patch.dict(os.environ, {"SESSION_CLEANUP_FILE": str(cleanup_file)}),
            ):
                try:
                    result = module.call_opencode(
                        "prompt de prueba",
                        {"modelos": ["model-test"], "timeout_seconds": 3},
                    )
                    error = ""
                except RuntimeError as exc:
                    result = None
                    error = str(exc)

            self.assertIsNotNone(result, f"OpenCode no recibió su configuración: {error}")
            self.assertTrue(cleanup_file.is_file(), "no se borró la sesión temporal")
            self.assertEqual(cleanup_file.read_text(encoding="utf-8"), "ses_testResumen123")
        self.assertEqual(result["idea"], "La salida llega bien.")
        self.assertEqual(result["puntos"][0]["texto"], "stdin recibido")

    def test_opencode_falls_back_to_standalone_when_service_is_down(self):
        module = load_summarizer()
        with tempfile.TemporaryDirectory() as directory:
            executable = Path(directory) / "opencode"
            executable.write_text(
                "#!/usr/bin/env python3\n"
                "import json, os, sys\n"
                "if sys.argv[1:] == ['models']:\n"
                "  sys.exit(1)\n"
                "elif sys.argv[1:2] == ['run']:\n"
                "  if sys.argv[1:3] != ['run', '--standalone']: sys.exit(3)\n"
                "  response = {'titulo':'P','idea':'La salida llega bien.','puntos':[{'emoji':'✅','texto':'ok'}]}\n"
                "  event = {'type':'text','sessionID':'ses_testStandalone123','part':{'type':'text','text':json.dumps(response, ensure_ascii=False)}}\n"
                "  print(json.dumps(event, ensure_ascii=False))\n"
                "elif sys.argv[1:3] == ['session', 'delete']:\n"
                "  if sys.argv[2:] != ['delete', '--standalone', 'ses_testStandalone123']: sys.exit(5)\n"
                "else: sys.exit(6)\n",
                encoding="utf-8",
            )
            executable.chmod(0o755)

            with patch.object(module.shutil, "which", return_value=str(executable)):
                result = module.call_opencode("prompt", {"modelos": ["model-test"], "timeout_seconds": 3})

        self.assertEqual(result["idea"], "La salida llega bien.")


class LocalStorageTests(unittest.TestCase):
    def test_summary_cache_round_trip_keeps_the_selected_text_out_of_cache_files(self):
        module = load_summarizer()
        original = "Texto privado que no debe quedar escrito en la caché."
        config = {"modelos": ["modelo-test"], "cache_days": 7}

        with tempfile.TemporaryDirectory() as cache_dir:
            module.save_summary_cache(original, config, SAMPLE_SUMMARY, cache_dir, now=1_000)
            cached = module.load_cached_summary(original, config, cache_dir, now=1_100)
            cache_files = list(Path(cache_dir).glob("*.json"))

            self.assertEqual(cached["idea"], SAMPLE_SUMMARY["idea"])
            self.assertEqual(len(cache_files), 1)
            self.assertNotIn(original, cache_files[0].read_text(encoding="utf-8"))

    def test_expired_summary_cache_is_ignored(self):
        module = load_summarizer()
        config = {"modelos": ["modelo-test"], "cache_days": 1}

        with tempfile.TemporaryDirectory() as cache_dir:
            module.save_summary_cache("texto", config, SAMPLE_SUMMARY, cache_dir, now=1_000)
            self.assertIsNone(module.load_cached_summary("texto", config, cache_dir, now=87_401))

    def test_old_verbose_cache_is_compacted_without_regenerating(self):
        module = load_summarizer()
        text = " ".join(["original"] * 82)
        config = {"modelos": ["modelo-test"], "cache_days": 7}

        with tempfile.TemporaryDirectory() as cache_dir:
            module.save_summary_cache(text, config, SAMPLE_SUMMARY, cache_dir, now=time.time())
            path = module._cache_path(text, config["modelos"], cache_dir)
            payload = json.loads(path.read_text(encoding="utf-8"))
            payload["version"] = 1
            path.write_text(json.dumps(payload), encoding="utf-8")

            summary, cached = module.generate_summary(
                text,
                config=config,
                model_call=lambda *_args: self.fail("el caché antiguo no debe llamar al modelo"),
                cache_dir=cache_dir,
            )

        self.assertTrue(cached)
        self.assertLessEqual(module.summary_word_count(summary), 21)

    def test_manual_save_writes_a_readable_markdown_note_to_the_chosen_folder(self):
        module = load_summarizer()

        with tempfile.TemporaryDirectory() as directory:
            path = module.save_summary(
                SAMPLE_SUMMARY,
                "Texto original que elegí guardar.",
                {"aplicacion": "Documento de prueba"},
                save_dir=directory,
            )

            self.assertEqual(path.parent, Path(directory))
            self.assertTrue(path.name.endswith(".md"))
            content = path.read_text(encoding="utf-8")
            self.assertIn("# 🧠 Cómo se relacionan presión y profundidad", content)
            self.assertIn("Texto original que elegí guardar.", content)


class CancellationTests(unittest.TestCase):
    def test_closing_summary_can_terminate_a_running_model_process_promptly(self):
        module = load_summarizer()
        cancel_event = threading.Event()
        timer = threading.Timer(0.15, cancel_event.set)
        started = time.monotonic()
        timer.start()
        try:
            with self.assertRaises(module.SummaryCancelled):
                module.run_text_process(
                    [sys.executable, "-c", "import time; time.sleep(5)"],
                    "texto de prueba",
                    timeout=8,
                    cancel_event=cancel_event,
                )
        finally:
            timer.cancel()

        self.assertLess(time.monotonic() - started, 2.0)


class ReaderIntegrationTests(unittest.TestCase):
    def test_super_r_reads_the_open_summary_instead_of_the_stale_clipboard(self):
        reader = Path.home() / ".config/hypr/scripts/leer-seleccion.sh"
        self.assertTrue(reader.is_file())
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bin_dir = root / "bin"
            runtime_dir = root / "runtime"
            bin_dir.mkdir()
            runtime_dir.mkdir()
            captured = root / "read-by-piper.txt"
            (runtime_dir / "resumidor-seleccion.txt").write_text(
                "Resumen listo: idea central importante.", encoding="utf-8"
            )
            (runtime_dir / "resumidor-seleccion.pid").write_text(str(os.getpid()), encoding="ascii")

            stubs = {
                "pgrep": "#!/bin/sh\n[ \"${AUDIO_ALREADY_PLAYING:-0}\" = 1 ] && exit 0\nexit 1\n",
                "pkill": "#!/bin/sh\nexit 0\n",
                "hyprctl": (
                    "#!/bin/sh\n"
                    "case \"$1\" in\n"
                    "  activewindow) printf '{\\\"class\\\":\\\"mpv\\\",\\\"title\\\":\\\"Video\\\"}' ;;\n"
                    "  layers) printf 'namespace: resumen-seleccion, pid: %s\\n' \"$SUMMARY_PID\" ;;\n"
                    "esac\n"
                ),
                "wl-paste": "#!/bin/sh\nprintf 'PORTAPAPELES VIEJO'\n",
                "piper-tts": "#!/bin/sh\ncat > \"$CAPTURE_TEXT_FILE\"\n",
                "pw-play": "#!/bin/sh\ncat >/dev/null\n",
                "systemctl": "#!/bin/sh\nexit 0\n",
            }
            for name, content in stubs.items():
                path = bin_dir / name
                path.write_text(content, encoding="utf-8")
                path.chmod(0o755)

            env = os.environ.copy()
            env.update({
                "PATH": f"{bin_dir}:/usr/bin:/bin",
                "XDG_RUNTIME_DIR": str(runtime_dir),
                "PIPER_DAEMON_SOCK": str(root / "no-daemon.sock"),
                "CAPTURE_TEXT_FILE": str(captured),
                "SUMMARY_PID": str(os.getpid()),
            })
            result = subprocess.run(
                ["bash", str(reader)],
                env=env,
                capture_output=True,
                text=True,
                timeout=8,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("idea central importante", captured.read_text(encoding="utf-8"))
            self.assertNotIn("PORTAPAPELES VIEJO", captured.read_text(encoding="utf-8"))

            captured.unlink()
            replacement = root / "nuevo-resumen.txt"
            replacement.write_text("Nuevo resumen que debe leerse ahora.", encoding="utf-8")
            env["AUDIO_ALREADY_PLAYING"] = "1"
            result = subprocess.run(
                ["bash", str(reader), "--texto-archivo", str(replacement)],
                env=env,
                capture_output=True,
                text=True,
                timeout=8,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(captured.is_file(), "la acción de leer solo detuvo el audio anterior")
            self.assertIn("Nuevo resumen", captured.read_text(encoding="utf-8"))


class RuntimeFileSafetyTests(unittest.TestCase):
    def test_text_file_argument_does_not_delete_a_file_outside_the_private_runtime_directory(self):
        module = load_summarizer()
        with tempfile.TemporaryDirectory() as directory:
            external_file = Path(directory) / "not-a-runtime-selection.txt"
            external_file.write_text("No borrar este archivo", encoding="utf-8")
            argv = [str(MODULE_PATH), "--text-file", str(external_file)]
            with (
                patch.object(sys, "argv", argv),
                patch.object(module, "_notify"),
                patch.object(module, "capture_context", return_value={}),
                patch.object(module, "close_existing_popup"),
                patch.object(module, "_register_instance"),
                patch.object(module, "launch_window", return_value=0),
                patch.object(module.signal, "signal"),
            ):
                result = module.main()

            self.assertEqual(result, 2)
            self.assertTrue(external_file.exists())


class PresentationTests(unittest.TestCase):
    def test_inline_markup_escapes_html_and_keeps_bold_and_code_styled(self):
        module = load_summarizer()
        self.assertEqual(
            module.inline_pango_markup("**causa & efecto** <script> `x < y`"),
            "<b>causa &amp; efecto</b> &lt;script&gt; <tt>x &lt; y</tt>",
        )

    def test_markdown_export_includes_structured_sections_and_escapes_table_pipes(self):
        module = load_summarizer()

        markdown = module.summary_to_markdown(SAMPLE_SUMMARY, original_text="Texto original.")

        self.assertIn("## 🎯 Idea central", markdown)
        self.assertIn("## ✨ Puntos clave", markdown)
        self.assertIn("## 📊 Comparación", markdown)
        self.assertIn("mucha \\| mayor presión", markdown)
        self.assertIn("<details>", markdown)
        self.assertIn("Texto original.", markdown)

    def test_speech_reads_only_the_compact_core_and_obeys_a_word_limit(self):
        module = load_summarizer()

        spoken = module.summary_to_speech(SAMPLE_SUMMARY, max_words=12)

        self.assertIn("La presión de un fluido", spoken)
        self.assertLessEqual(len(__import__("re").findall(r"\b\w+\b", spoken)), 12)
        self.assertNotIn("Conclusión", spoken)
        self.assertNotIn("Ejemplo", spoken)
        self.assertNotIn("Términos importantes", spoken)
        self.assertNotIn("**", spoken)
        self.assertNotIn("🌊", spoken)

    def test_summary_progress_messages_map_to_a_fraction_for_the_progress_bar(self):
        module = load_summarizer()
        first = module.progress_fraction("Analizando parte 1 de 4…")
        second = module.progress_fraction("Analizando parte 2 de 4…")
        integrating = module.progress_fraction("Conectando las ideas y preparando la explicación final…")

        self.assertAlmostEqual(first, 0.25)
        self.assertAlmostEqual(second, 0.50)
        self.assertGreater(integrating, second)
        self.assertIsNone(module.progress_fraction("Analizando el texto…"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
