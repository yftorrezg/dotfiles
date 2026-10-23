#!/usr/bin/env python3
"""Pruebas de la lógica pura del traductor rápido (sin red ni sesión gráfica)."""
import unittest
import os
import subprocess
import sys

from traducir_seleccion import (
    choose_source_language,
    detect_language_hint,
    english_text_for_speech,
    is_dictionary_candidate,
    is_terminal_class,
    length_scale_for_speed,
    make_clipboard_content_provider,
    normalize_language_code,
    normalize_text,
    parse_dictionary_entry,
    parse_google_response,
    parse_mymemory_response,
    split_mymemory_text,
    safe_wiktionary_source_url,
    translate_selection,
)


class SelectionTests(unittest.TestCase):
    def test_normalize_text_collapses_whitespace_without_losing_punctuation(self):
        self.assertEqual(
            normalize_text("  I don't know.\n  ¿Dónde está?  "),
            "I don't know. ¿Dónde está?",
        )

    def test_normalize_text_rejects_a_selection_over_the_translation_limit(self):
        with self.assertRaisesRegex(ValueError, "4000"):
            normalize_text("a" * 4001)

    def test_dictionary_lookup_accepts_words_and_phrasal_verbs(self):
        self.assertTrue(is_dictionary_candidate("look after"))
        self.assertTrue(is_dictionary_candidate("give up!"))
        self.assertFalse(is_dictionary_candidate("How can I get to the station?"))

    def test_terminal_detection_prevents_synthetic_ctrl_c(self):
        self.assertTrue(is_terminal_class("kitty"))
        self.assertTrue(is_terminal_class("org.wezfurlong.wezterm"))
        self.assertFalse(is_terminal_class("brave-browser"))


class LanguageDetectionTests(unittest.TestCase):
    def test_language_hint_recognizes_a_spanish_sentence(self):
        self.assertEqual(detect_language_hint("¿Dónde está la casa?"), "es")

    def test_language_hint_recognizes_common_single_words(self):
        self.assertEqual(detect_language_hint("casa"), "es")
        self.assertEqual(detect_language_hint("house"), "en")

    def test_language_hint_leaves_ambiguous_words_for_the_translation_service(self):
        self.assertIsNone(detect_language_hint("run"))

    def test_language_codes_accept_regional_variants(self):
        self.assertEqual(normalize_language_code("es-BO"), "es")
        self.assertEqual(normalize_language_code("EN_us"), "en")
        self.assertIsNone(normalize_language_code("pt-BR"))

    def test_local_language_evidence_overrides_an_unreliable_api_guess(self):
        self.assertEqual(choose_source_language("casa", "en", "house"), "es")

    def test_google_detection_is_used_when_local_text_is_ambiguous(self):
        self.assertEqual(choose_source_language("run", "en", "run"), "en")

    def test_changed_translation_to_english_is_a_spanish_fallback_signal(self):
        self.assertEqual(choose_source_language("correr", "pt", "run"), "es")


class ProviderParsingTests(unittest.TestCase):
    def test_google_dictionary_client_response_includes_detected_language(self):
        self.assertEqual(
            parse_google_response([["I would like to learn English this year", "es"]]),
            ("I would like to learn English this year", "es"),
        )

    def test_google_response_without_metadata_is_still_usable(self):
        self.assertEqual(
            parse_google_response(["Esta es una oración de prueba."]),
            ("Esta es una oración de prueba.", None),
        )

    def test_google_response_rejects_an_empty_payload(self):
        with self.assertRaisesRegex(ValueError, "traducción"):
            parse_google_response([])

    def test_dictionary_parser_collects_ipa_definitions_and_examples(self):
        payload = {
            "word": "give up",
            "source": {
                "url": "https://en.wiktionary.org/wiki/give_up",
                "license": {"name": "CC BY-SA 4.0", "url": "https://creativecommons.org/licenses/by-sa/4.0/"},
            },
            "entries": [
                {
                    "partOfSpeech": "verb",
                    "pronunciations": [{"type": "ipa", "text": "/ɡɪv ˈʌp/", "tags": []}],
                    "senses": [
                        {
                            "definition": "To surrender.",
                            "examples": ["He gave up."],
                            "subsenses": [
                                {
                                    "definition": "To relinquish.",
                                    "examples": ["She gave up her seat."],
                                }
                            ],
                        }
                    ],
                }
            ],
        }
        self.assertEqual(
            parse_dictionary_entry(payload),
            {
                "part_of_speech": "verb",
                "ipa": "/ɡɪv ˈʌp/",
                "definitions": ["To surrender.", "To relinquish."],
                "examples": ["He gave up.", "She gave up her seat."],
                "source_url": "https://en.wiktionary.org/wiki/give_up",
            },
        )

    def test_dictionary_source_link_only_accepts_https_wiktionary(self):
        self.assertEqual(
            safe_wiktionary_source_url("https://en.wiktionary.org/wiki/give_up"),
            "https://en.wiktionary.org/wiki/give_up",
        )
        self.assertIsNone(safe_wiktionary_source_url("https://example.com/steal-data"))

    def test_dictionary_parser_handles_not_found_responses(self):
        self.assertEqual(parse_dictionary_entry({"title": "No Definitions Found"}), {})

    def test_mymemory_parser_reads_its_translation_field(self):
        payload = {"responseStatus": 200, "responseData": {"translatedText": "rendir"}}
        self.assertEqual(parse_mymemory_response(payload), "rendir")

    def test_mymemory_chunks_respect_the_documented_utf8_byte_limit(self):
        self.assertEqual(
            split_mymemory_text("one two three four", max_bytes=7),
            ["one two", "three", "four"],
        )
        self.assertEqual(split_mymemory_text("café casa", max_bytes=7), ["café", "casa"])

    def test_mymemory_chunking_rejects_a_single_oversized_token(self):
        with self.assertRaisesRegex(ValueError, "5 bytes"):
            split_mymemory_text("wordtoolong", max_bytes=5)

    def test_translation_uses_spanish_selection_as_source_and_speaks_english(self):
        calls = []

        def translate(text, source, target):
            calls.append((text, source, target))
            return "house"

        result = translate_selection(
            "casa",
            translator_fn=translate,
            dictionary_lookup_fn=lambda *_: {},
        )
        self.assertEqual(result["source_language"], "es")
        self.assertEqual(result["target_language"], "en")
        self.assertEqual(result["translation"], "house")
        self.assertEqual(result["english_text"], "house")
        self.assertEqual(calls, [("casa", "es", "en")])

    def test_ambiguous_english_selection_uses_provider_detection(self):
        calls = []

        def google(text, source, target):
            self.assertEqual((text, source, target), ("run", "auto", "en"))
            return "run", "en"

        def translate(text, source, target):
            calls.append((text, source, target))
            return "correr"

        result = translate_selection(
            "run",
            google_translate_fn=google,
            translator_fn=translate,
            dictionary_lookup_fn=lambda *_: {},
        )
        self.assertEqual(result["source_language"], "en")
        self.assertEqual(result["target_language"], "es")
        self.assertEqual(result["english_text"], "run")
        self.assertEqual(calls, [("run", "en", "es")])

    def test_dictionary_examples_are_translated_for_bilingual_practice(self):
        payload = {
            "word": "give up",
            "entries": [
                {
                    "partOfSpeech": "verb",
                    "pronunciations": [],
                    "senses": [{"definition": "To surrender.", "examples": ["He gave up."]}],
                }
            ],
        }
        seen = []

        def translate(text, source, target):
            seen.append((text, source, target))
            return {"give up": "rendirse", "He gave up.": "Él se rindió."}[text]

        result = translate_selection(
            "give up",
            google_translate_fn=lambda *_: ("give up", "en"),
            translator_fn=translate,
            dictionary_lookup_fn=lambda *_: parse_dictionary_entry(payload),
        )
        self.assertEqual(result["dictionary"]["part_of_speech"], "verb")
        self.assertEqual(result["examples"], [{"original": "He gave up.", "translated": "Él se rindió."}])
        self.assertIn(("He gave up.", "en", "es"), seen)


class ListeningTests(unittest.TestCase):
    def test_layer_shell_library_loads_before_gtk_imports(self):
        code = (
            "import sys, traducir_seleccion as t; "
            "t.initialize_layer_shell_library(); "
            "assert 'gi' not in sys.modules; "
            "assert 'libgtk4-layer-shell.so' in open('/proc/self/maps').read()"
        )
        subprocess.run(
            [sys.executable, "-c", code],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            capture_output=True,
            text=True,
            check=True,
        )

    def test_translation_clipboard_provider_is_a_real_gdk_text_provider(self):
        import gi
        gi.require_version("Gdk", "4.0")
        from gi.repository import Gdk, GObject

        provider = make_clipboard_content_provider("cuidar de")
        self.assertIsInstance(provider, Gdk.ContentProvider)
        self.assertTrue(provider.ref_formats().contain_gtype(GObject.TYPE_STRING))

    def test_speech_always_reads_the_english_side(self):
        self.assertEqual(english_text_for_speech("es", "casa", "house"), "house")
        self.assertEqual(english_text_for_speech("en", "house", "casa"), "house")

    def test_piper_length_scale_slows_the_model_for_listening_practice(self):
        self.assertEqual(length_scale_for_speed(1.0), 1.0)
        self.assertEqual(length_scale_for_speed(0.8), 1.25)


if __name__ == "__main__":
    unittest.main(verbosity=2)
