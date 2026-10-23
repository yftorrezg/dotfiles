#!/usr/bin/env python3
"""Traductor EN/ES de selección para Hyprland: traducción, diccionario y voz offline."""
from __future__ import annotations

import atexit
import html
import json
import math
import os
import re
import shutil
import signal
import subprocess
import tempfile
import threading
import time
import unicodedata
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode, urlsplit
from urllib.request import Request, urlopen


MAX_SELECTION_CHARS = 4000
COPY_INITIAL_DELAY = 0.12  # segundos para soltar SUPER/SHIFT del atajo antes de copiar
COPY_RETRIES = 3  # intentos de Ctrl+C si el portapapeles sigue vacío
COPY_POLL_ATTEMPTS = 12  # lecturas del portapapeles por intento
COPY_POLL_INTERVAL = 0.02  # segundos entre lecturas
COPY_RETRY_DELAY = 0.15  # segundos entre reintentos
REQUEST_TIMEOUT = 7
GOOGLE_ENDPOINT = "https://clients5.google.com/translate_a/t?client=dict-chrome-ex"
MYMEMORY_ENDPOINT = "https://api.mymemory.translated.net/get"
DICTIONARY_ENDPOINT = "https://freedictionaryapi.com/api/v1/entries"
VOICE_ID = "en_US-lessac-high"
VOICE_MODEL_DEFAULT = Path.home() / ".local/share/piper-voices" / f"{VOICE_ID}.onnx"
VOICE_INSTALL_COMMAND = (
    'python3 -m piper.download_voices --download-dir '
    '"$HOME/.local/share/piper-voices" en_US-lessac-high'
)
CONFIG_PATH = Path.home() / ".config/hypr/scripts/traductor.json"

ENGLISH_STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "been", "but", "by", "can", "could",
    "did", "do", "does", "for", "from", "had", "has", "have", "he", "her", "here",
    "him", "his", "how", "i", "if", "in", "is", "it", "its", "me", "my", "not",
    "of", "on", "or", "our", "she", "should", "so", "that", "the", "their", "them",
    "there", "they", "this", "to", "was", "we", "were", "what", "when", "where",
    "which", "who", "will", "with", "would", "you", "your",
}
SPANISH_STOPWORDS = {
    "a", "al", "algo", "como", "con", "cuando", "de", "del", "donde", "dónde", "el",
    "ella", "ellas", "ellos", "en", "es", "esta", "está", "este", "esto", "la", "las",
    "lo", "los", "me", "mi", "muy", "no", "nos", "o", "para", "pero", "por", "que",
    "qué", "se", "si", "sí", "sin", "su", "sus", "te", "tiene", "tu", "tú", "un",
    "una", "unas", "uno", "unos", "y", "yo",
}
COMMON_ENGLISH_WORDS = {
    "after", "bad", "beautiful", "book", "child", "computer", "dog", "family", "food",
    "friend", "good", "hello", "help", "home", "house", "learn", "listen", "man", "morning",
    "people", "please", "school", "speak", "study", "thanks", "tomorrow", "understand",
    "water", "woman", "work", "yesterday",
}
COMMON_SPANISH_WORDS = {
    "agua", "amigo", "ayer", "bien", "buenos", "casa", "comer", "comida",
    "correr", "días", "escuela", "español", "familia", "gato", "gente", "gracias", "hola",
    "hombre", "inglés", "libro", "mañana", "mujer", "noche", "perro", "vivir",
}
TERMINAL_CLASSES = {
    "alacritty", "contour", "foot", "footclient", "gnome-terminal", "gnome-terminal-server",
    "kitty", "konsole", "org.wezfurlong.wezterm", "st", "terminator", "tilix", "urxvt",
    "wezterm", "wterm", "xterm",
}
_LAYER_SHELL_LIBRARY = None


def normalize_text(text: str, max_chars: int = MAX_SELECTION_CHARS) -> str:
    """Normaliza espacios sin alterar palabras ni puntuación de la selección."""
    if not isinstance(text, str):
        raise TypeError("La selección debe ser texto")
    text = unicodedata.normalize("NFC", text.replace("\x00", ""))
    text = re.sub(r"[\u200b\u200c\u200d\ufeff]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > max_chars:
        raise ValueError(f"La selección supera el límite de {max_chars} caracteres")
    return text


def is_dictionary_candidate(text: str) -> bool:
    """Admite una palabra o una expresión corta (incluidos phrasal verbs)."""
    candidate = normalize_text(text).strip(" \t.,!?;:()[]{}\"'“”‘’")
    if not candidate or not any(char.isalpha() for char in candidate):
        return False
    if not all(char.isalpha() or char.isspace() or char in {"'", "’", "-"} for char in candidate):
        return False
    return 1 <= len(candidate.split()) <= 4


def normalize_language_code(code: str | None) -> str | None:
    """Reduce etiquetas regionales como es-BO o en_US a es/en."""
    if not isinstance(code, str):
        return None
    match = re.match(r"^\s*(en|es)(?:[-_]|$)", code, re.IGNORECASE)
    return match.group(1).lower() if match else None


def detect_language_hint(text: str) -> str | None:
    """Detección local ligera; deja expresiones ambiguas para el proveedor."""
    normalized = normalize_text(text).lower()
    if not normalized:
        return None
    if any(mark in normalized for mark in "áéíóúüñ¿¡"):
        return "es"

    words = re.findall(r"[a-záéíóúüñ]+", normalized)
    if not words:
        return None
    if len(words) == 1:
        word = words[0]
        if word in COMMON_SPANISH_WORDS:
            return "es"
        if word in COMMON_ENGLISH_WORDS:
            return "en"

    spanish_score = sum(word in SPANISH_STOPWORDS for word in words)
    english_score = sum(word in ENGLISH_STOPWORDS for word in words)
    if spanish_score > english_score:
        return "es"
    if english_score > spanish_score:
        return "en"
    return None


def choose_source_language(text: str, detected_language: str | None, english_translation: str) -> str:
    """Combina indicios locales, detección del proveedor y el cambio de traducción."""
    hint = detect_language_hint(text)
    if hint:
        return hint
    detected = normalize_language_code(detected_language)
    if detected:
        return detected
    if normalize_text(english_translation).casefold() != normalize_text(text).casefold():
        return "es"
    return "en"


def parse_google_response(payload) -> tuple[str, str | None]:
    """Lee las variantes de respuesta de la API web de Google Translate."""
    def find_pair(value):
        if isinstance(value, list):
            if value and isinstance(value[0], str):
                detected = normalize_language_code(value[1]) if len(value) > 1 else None
                return value[0], detected
            for child in value:
                found = find_pair(child)
                if found and found[0].strip():
                    return found
        return None

    found = find_pair(payload)
    if not found or not found[0].strip():
        raise ValueError("El proveedor no devolvió una traducción válida")
    return normalize_text(found[0]), found[1]


def parse_mymemory_response(payload) -> str:
    """Extrae una traducción de la respuesta JSON de MyMemory."""
    try:
        status = int(payload.get("responseStatus", 0))
        translated = payload["responseData"]["translatedText"]
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        raise ValueError("Respuesta de MyMemory incompleta") from exc
    translated = normalize_text(html.unescape(str(translated)))
    if status != 200 or not translated:
        raise ValueError("MyMemory no pudo traducir el texto")
    return translated


def split_mymemory_text(text: str, max_bytes: int = 450) -> list[str]:
    """Divide texto por palabras bajo el límite documentado de 500 bytes UTF-8."""
    if max_bytes <= 0:
        raise ValueError("El límite debe ser mayor que cero")
    chunks = []
    current = []
    current_bytes = 0
    for word in normalize_text(text).split():
        word_bytes = len(word.encode("utf-8"))
        if word_bytes > max_bytes:
            raise ValueError(f"Una palabra supera el límite de {max_bytes} bytes de MyMemory")
        extra_bytes = word_bytes + (1 if current else 0)
        if current and current_bytes + extra_bytes > max_bytes:
            chunks.append(" ".join(current))
            current = []
            current_bytes = 0
            extra_bytes = word_bytes
        current.append(word)
        current_bytes += extra_bytes
    if current:
        chunks.append(" ".join(current))
    return chunks


def _plain_text(value) -> str:
    text = html.unescape(str(value or ""))
    text = re.sub(r"<[^>]*>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def parse_dictionary_entry(payload, max_definitions: int = 3, max_examples: int = 2) -> dict:
    """Aplana una entrada de FreeDictionaryAPI para usarla en la tarjeta."""
    if not isinstance(payload, dict) or not isinstance(payload.get("entries"), list):
        return {}

    entries = payload["entries"]
    if not entries:
        return {}

    part_of_speech = ""
    ipa = ""
    definitions = []
    examples = []

    def add_unique(items: list[str], value, limit: int) -> None:
        value = _plain_text(value)
        if value and value not in items and len(items) < limit:
            items.append(value)

    def visit_sense(sense) -> None:
        if not isinstance(sense, dict):
            return
        add_unique(definitions, sense.get("definition"), max_definitions)
        for example in sense.get("examples", []):
            add_unique(examples, example.get("text") if isinstance(example, dict) else example, max_examples)
        for child in sense.get("subsenses", []):
            visit_sense(child)

    for entry in entries:
        if not isinstance(entry, dict):
            continue
        if not part_of_speech:
            part_of_speech = _plain_text(entry.get("partOfSpeech", ""))
        if not ipa:
            for pronunciation in entry.get("pronunciations", []):
                if not isinstance(pronunciation, dict):
                    continue
                ipa = _plain_text(pronunciation.get("text") or pronunciation.get("ipa") or "")
                if ipa:
                    break
        for sense in entry.get("senses", []):
            visit_sense(sense)
            if len(definitions) >= max_definitions and len(examples) >= max_examples:
                break
        if len(definitions) >= max_definitions and len(examples) >= max_examples:
            break

    if not part_of_speech and not ipa and not definitions and not examples:
        return {}
    source = payload.get("source")
    source_url = safe_wiktionary_source_url(source.get("url")) if isinstance(source, dict) else None
    return {
        "part_of_speech": part_of_speech,
        "ipa": ipa,
        "definitions": definitions,
        "examples": examples,
        "source_url": source_url,
    }


def safe_wiktionary_source_url(url: str | None) -> str | None:
    """Solo convierte en enlace fuentes HTTPS de las ediciones oficiales de Wiktionary."""
    if not isinstance(url, str):
        return None
    try:
        parsed = urlsplit(url)
        valid_port = parsed.port in (None, 443)
    except ValueError:
        return None
    if (
        parsed.scheme == "https"
        and parsed.hostname in {"en.wiktionary.org", "es.wiktionary.org"}
        and parsed.username is None
        and parsed.password is None
        and valid_port
        and parsed.path.startswith("/wiki/")
    ):
        return url
    return None


def english_text_for_speech(source_language: str, source_text: str, translated_text: str) -> str:
    """El botón de audio siempre pronuncia el texto en inglés."""
    return translated_text if normalize_language_code(source_language) == "es" else source_text


def make_clipboard_content_provider(text: str):
    """Construye un proveedor de contenido GDK4 compatible con el portapapeles Wayland."""
    import gi

    gi.require_version("Gdk", "4.0")
    from gi.repository import Gdk, GObject

    value = GObject.Value()
    value.init(GObject.TYPE_STRING)
    value.set_string(text)
    return Gdk.ContentProvider.new_for_value(value)


def length_scale_for_speed(speed: float) -> float:
    """Piper usa length_scale inverso a la velocidad de reproducción."""
    try:
        value = float(speed)
    except (TypeError, ValueError) as exc:
        raise ValueError("Velocidad de voz no válida") from exc
    if not math.isfinite(value) or value <= 0:
        raise ValueError("La velocidad de voz debe ser mayor que cero")
    return round(1.0 / value, 3)


def is_terminal_class(window_class: str | None) -> bool:
    """Evita enviar Ctrl+C a una terminal, donde interrumpiría el proceso activo."""
    name = (window_class or "").strip().lower()
    return name in TERMINAL_CLASSES or any(
        fragment in name for fragment in ("terminal", "kitty", "alacritty", "wezterm", "footclient")
    )


def _run_command(args, *, input_text: str | None = None, timeout: float = 1.0):
    try:
        return subprocess.run(
            args,
            input=input_text,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None


def _run_binary_command(args, *, input_bytes: bytes | None = None, timeout: float = 1.0):
    """Ejecuta wl-paste/wl-copy sin decodificar imágenes u otros datos binarios."""
    try:
        return subprocess.run(
            args,
            input=input_bytes,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None


def _clipboard_text(primary: bool = False) -> str:
    args = ["wl-paste", "--no-newline"]
    if primary:
        args.insert(1, "--primary")
    result = _run_command(args)
    return result.stdout if result and result.returncode == 0 else ""


def _active_window_class() -> str:
    result = _run_command(["hyprctl", "activewindow", "-j"])
    if not result or result.returncode != 0:
        return ""
    try:
        return str(json.loads(result.stdout).get("class", ""))
    except (json.JSONDecodeError, AttributeError, TypeError):
        return ""


def _send_ctrl_c() -> bool:
    """Envía Ctrl+C con ydotool y, si no está disponible, con wtype."""
    if shutil.which("ydotool"):
        result = _run_command(["ydotool", "key", "29:1", "46:1", "46:0", "29:0"], timeout=1.5)
        if result and result.returncode == 0:
            return True
    if shutil.which("wtype"):
        result = _run_command(["wtype", "-M", "ctrl", "-k", "c", "-m", "ctrl"], timeout=1.5)
        return bool(result and result.returncode == 0)
    return False


def _copy_selection_via_ctrl_c() -> str:
    """Simula Ctrl+C esperando a que se suelten los modificadores del atajo y reintentando.

    Al pulsar SUPER+SHIFT+R/T, esas teclas físicas siguen apretadas cuando el script arranca;
    si lanzamos Ctrl+C de inmediato, la app recibe SUPER+SHIFT+Ctrl+C y no copia. Por eso se
    espera un instante y se reintenta la copia hasta que el portapapeles tenga texto.
    """
    time.sleep(COPY_INITIAL_DELAY)
    for _ in range(COPY_RETRIES):
        _send_ctrl_c()
        for _ in range(COPY_POLL_ATTEMPTS):
            selection = _clipboard_text()
            if selection.strip():
                return selection
            time.sleep(COPY_POLL_INTERVAL)
        time.sleep(COPY_RETRY_DELAY)
    return ""


def capture_selection() -> str:
    """Lee PRIMARY primero; si Chromium/Brave no la publica, simula Ctrl+C preservando el portapapeles."""
    primary = _clipboard_text(primary=True)
    if primary.strip():
        return primary

    if is_terminal_class(_active_window_class()):
        return ""  # Ctrl+C en una terminal interrumpe el proceso; solo se acepta PRIMARY.

    clipboard_types = _run_command(["wl-paste", "--list-types"])
    types = clipboard_types.stdout.splitlines() if clipboard_types and clipboard_types.returncode == 0 else []
    text_types = ("text/plain;charset=utf-8", "text/plain", "UTF8_STRING", "STRING", "TEXT")
    clipboard_type = next((mime for mime in text_types if mime in types), None)
    backup_type = clipboard_type
    if types and backup_type is None:
        # Brave no publica PRIMARY: permite copiar el texto incluso si el portapapeles
        # contiene una imagen, guardando antes sus bytes para restaurarlos después.
        preferred_types = ("image/png", "image/jpeg", "image/webp", "text/uri-list", "text/html")
        backup_type = next((mime for mime in preferred_types if mime in types), types[0])

    backup_args = ["wl-paste", "--no-newline"]
    if backup_type:
        backup_args.extend(["--type", backup_type])
    saved = _run_binary_command(backup_args)
    if types and (saved is None or saved.returncode != 0):
        return ""  # Si no podemos respaldarlo, no arriesgamos el portapapeles existente.
    backup = saved.stdout if saved and saved.returncode == 0 else None

    _run_command(["wl-copy", "--clear"])
    selection = _copy_selection_via_ctrl_c()

    if backup is not None:
        restore_args = ["wl-copy"]
        if backup_type:
            restore_args.extend(["--type", backup_type])
        _run_binary_command(restore_args, input_bytes=backup, timeout=2.0)
    return selection


def _request_json(url: str, data: bytes | None = None) -> dict | list:
    request = Request(
        url,
        data=data,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) EnglishPractice/1.0",
            "Accept": "application/json,text/plain,*/*",
            **({"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"} if data else {}),
        },
    )
    try:
        with urlopen(request, timeout=REQUEST_TIMEOUT) as response:
            return json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise RuntimeError("No se pudo conectar con el servicio de traducción") from exc


def google_translate(text: str, source_language: str, target_language: str) -> tuple[str, str | None]:
    """Traduce vía el endpoint web sin clave, aceptando auto/en/es como origen."""
    query = urlencode({"sl": source_language, "tl": target_language})
    body = urlencode({"q": text}).encode("utf-8")
    payload = _request_json(f"{GOOGLE_ENDPOINT}&{query}", data=body)
    return parse_google_response(payload)


def mymemory_translate(text: str, source_language: str, target_language: str) -> str:
    """Respaldo de traducción gratuito cuando Google no responde."""
    translations = []
    for chunk in split_mymemory_text(text):
        query = urlencode({"q": chunk, "langpair": f"{source_language}|{target_language}"})
        translations.append(parse_mymemory_response(_request_json(f"{MYMEMORY_ENDPOINT}?{query}")))
    return " ".join(translations)


def translate_with_fallback(text: str, source_language: str, target_language: str) -> str:
    try:
        translated, _detected = google_translate(text, source_language, target_language)
        if translated:
            return translated
    except (RuntimeError, ValueError, OSError):
        pass
    return mymemory_translate(text, source_language, target_language)


def lookup_dictionary(text: str, language: str) -> dict:
    candidate = normalize_text(text).strip(" \t.,!?;:()[]{}\"'“”‘’")
    encoded_candidate = quote(candidate, safe="'-")
    url = f"{DICTIONARY_ENDPOINT}/{language}/{encoded_candidate}"
    try:
        return parse_dictionary_entry(_request_json(url))
    except (RuntimeError, ValueError, OSError):
        return {}


def translate_selection(
    text: str,
    forced_source: str | None = None,
    *,
    google_translate_fn=None,
    translator_fn=None,
    dictionary_lookup_fn=None,
) -> dict:
    """Traduce una selección y añade diccionario/ejemplos si es una expresión corta."""
    text = normalize_text(text)
    if not text:
        raise ValueError("No hay texto seleccionado")

    google_fn = google_translate_fn or google_translate
    translate_fn = translator_fn or translate_with_fallback
    dictionary_fn = dictionary_lookup_fn or lookup_dictionary

    forced = normalize_language_code(forced_source)
    hint = normalize_language_code(forced) if forced else detect_language_hint(text)
    if hint:
        source_language = hint
        target_language = "en" if hint == "es" else "es"
        translation = translate_fn(text, source_language, target_language)
    else:
        try:
            english_guess, detected = google_fn(text, "auto", "en")
        except (RuntimeError, ValueError, OSError):
            english_guess, detected = text, None
        source_language = choose_source_language(text, detected, english_guess)
        target_language = "en" if source_language == "es" else "es"
        if source_language == "es":
            translation = english_guess
            if normalize_text(translation).casefold() == text.casefold():
                translation = translate_fn(text, "es", "en")
        else:
            translation = translate_fn(text, "en", "es")

    translation = normalize_text(translation)
    dictionary = {}
    examples = []
    if is_dictionary_candidate(text):
        try:
            dictionary = dictionary_fn(text, source_language) or {}
        except (RuntimeError, ValueError, OSError):
            dictionary = {}
        for example in dictionary.get("examples", [])[:2]:
            translated_example = ""
            try:
                translated_example = translate_fn(example, source_language, target_language)
            except (RuntimeError, ValueError, OSError):
                pass
            examples.append({"original": example, "translated": translated_example})

    return {
        "source_text": text,
        "translation": translation,
        "source_language": source_language,
        "target_language": target_language,
        "english_text": english_text_for_speech(source_language, text, translation),
        "dictionary": dictionary,
        "examples": examples,
    }


def load_settings(path: Path | str = CONFIG_PATH) -> dict:
    """Lee los ajustes personales, pero conserva defaults si el JSON está roto."""
    settings = {"piper_model": str(VOICE_MODEL_DEFAULT), "speech_speed": 0.9}
    try:
        loaded = json.loads(Path(path).expanduser().read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, TypeError):
        loaded = {}
    if isinstance(loaded, dict):
        if isinstance(loaded.get("piper_model"), str):
            settings["piper_model"] = str(Path(loaded["piper_model"]).expanduser())
        try:
            speed = float(loaded.get("speech_speed", settings["speech_speed"]))
            if math.isfinite(speed) and 0.5 <= speed <= 1.5:
                settings["speech_speed"] = speed
        except (TypeError, ValueError):
            pass
    override = os.environ.get("TRADUCTOR_PIPER_MODEL")
    if override:
        settings["piper_model"] = str(Path(override).expanduser())
    return settings


def _runtime_dir() -> Path:
    return Path(os.environ.get("XDG_RUNTIME_DIR", f"/run/user/{os.getuid()}"))


def _pid_file() -> Path:
    return _runtime_dir() / "traductor-seleccion.pid"


def _remove_pid_file(pid_file: Path, pid: int) -> None:
    try:
        if pid_file.read_text(encoding="ascii").strip() == str(pid):
            pid_file.unlink(missing_ok=True)
    except OSError:
        pass


def close_existing_popup() -> None:
    pid_file = _pid_file()
    try:
        pid = int(pid_file.read_text(encoding="ascii").strip())
    except (OSError, ValueError):
        return
    if pid <= 1 or pid == os.getpid():
        return
    try:
        cmdline = Path(f"/proc/{pid}/cmdline").read_bytes().replace(b"\0", b" ")
        if b"traducir_seleccion.py" not in cmdline:
            return
        os.kill(pid, signal.SIGTERM)
    except (OSError, ProcessLookupError):
        pass
    for _ in range(20):
        if not Path(f"/proc/{pid}").exists():
            break
        time.sleep(0.025)


def _notify(title: str, message: str) -> None:
    if shutil.which("notify-send"):
        subprocess.Popen(
            ["notify-send", "-a", "Traductor EN/ES", "-t", "3500", title, message],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


def _focused_monitor(display):
    result = _run_command(["hyprctl", "monitors", "-j"])
    if not result or result.returncode != 0:
        return None
    try:
        monitors = json.loads(result.stdout)
        focused_name = next(m["name"] for m in monitors if m.get("focused"))
        model = display.get_monitors()
        for index in range(model.get_n_items()):
            monitor = model.get_item(index)
            if monitor.get_connector() == focused_name:
                return monitor
    except (json.JSONDecodeError, KeyError, StopIteration, AttributeError, TypeError):
        pass
    return None


def initialize_layer_shell_library():
    """Precarga layer-shell antes de que GTK/GDK inicialicen libwayland."""
    global _LAYER_SHELL_LIBRARY
    if _LAYER_SHELL_LIBRARY is None:
        import ctypes

        _LAYER_SHELL_LIBRARY = ctypes.CDLL("libgtk4-layer-shell.so")
    return _LAYER_SHELL_LIBRARY


def launch_window(text: str, settings: dict, demo: bool = False) -> int:
    """Crea el recuadro de estudio GTK4 en la capa superior de Hyprland."""
    initialize_layer_shell_library()
    import gi

    gi.require_version("Gtk", "4.0")
    gi.require_version("Gdk", "4.0")
    gi.require_version("Gtk4LayerShell", "1.0")
    from gi.repository import Gdk, Gio, GLib, Gtk, Pango
    from gi.repository import Gtk4LayerShell as LayerShell

    css = Gtk.CssProvider()
    css.load_from_string(
        """
        window.traductor-window { background: transparent; }
        button.backdrop { background: rgba(12, 14, 21, 0.48); border: none; border-radius: 0; padding: 0; }
        .traductor-card {
            background: #282b38; color: #f4f2fa; border: 1px solid rgba(189, 178, 224, 0.34);
            border-radius: 24px; box-shadow: 0 20px 68px rgba(0, 0, 0, 0.5); padding: 0;
        }
        .header { padding: 19px 22px 13px 22px; }
        .brand { color: #c6b3ff; font-size: 11px; font-weight: 850; letter-spacing: 1.35px; }
        .subtitle { color: #aaaabd; font-size: 13px; }
        .pill { background: rgba(180, 158, 245, 0.16); color: #d5c7ff; border-radius: 99px;
                padding: 6px 10px; font-size: 12px; font-weight: 800; }
        .panel { background: rgba(255, 255, 255, 0.045); border: 1px solid rgba(220, 216, 241, 0.12);
                 border-radius: 16px; padding: 13px 16px; }
        .panel-title { color: #aaaabd; font-size: 10px; font-weight: 850; letter-spacing: 1.1px; }
        .source-text { color: #d0d0dd; font-size: 15px; }
        .translated-text { color: #ffffff; font-size: 23px; font-weight: 750; }
        .dict-title { color: #d6caff; font-size: 14px; font-weight: 750; }
        .definition { color: #e0deea; font-size: 13px; }
        .example-en { color: #f1eff8; font-size: 13px; font-weight: 650; }
        .example-es { color: #b8b7c8; font-size: 12px; }
        .muted { color: #a9a9bb; font-size: 12px; }
        .status { color: #c9c0df; font-size: 12px; }
        button.action { border-radius: 12px; padding: 9px 13px; background: rgba(255,255,255,0.075);
                        color: #eeedf5; border: 1px solid rgba(255,255,255,0.09); font-weight: 700; }
        button.primary-action { background: #ad96f2; color: #201a30; border: none; font-weight: 850; }
        button.close-action { padding: 5px 10px; min-width: 0; min-height: 0; border-radius: 99px;
                              background: rgba(255,255,255,0.08); color: #e7e3f1; border: none; }
        button.action:hover, button.close-action:hover { background: rgba(190, 170, 255, 0.22); }
        dropdown { min-width: 118px; }
        expander > title { color: #d8d0eb; font-weight: 700; padding-top: 5px; }
        scrolledwindow, scrolledwindow > viewport { background: transparent; }
        """
    )
    Gtk.StyleContext.add_provider_for_display(
        Gdk.Display.get_default(), css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )

    class TranslatorApp(Gtk.Application):
        def __init__(self):
            super().__init__(application_id="org.yafer.TraductorENES", flags=Gio.ApplicationFlags.FLAGS_NONE)
            self.original_text = text
            self.settings = settings
            self.demo = demo
            self.window = None
            self.result = None
            self.forced_source = None
            self.generation = 0
            self.audio_process = None
            self.audio_lock = threading.Lock()
            self.audio_cancel = threading.Event()
            self.audio_thread = None

        @staticmethod
        def label(text="", css_class=None, *, wrap=True, selectable=False):
            item = Gtk.Label(label=text)
            item.set_xalign(0)
            item.set_yalign(0.5)
            item.set_wrap(wrap)
            item.set_wrap_mode(Pango.WrapMode.WORD_CHAR)
            item.set_selectable(selectable)
            if css_class:
                item.add_css_class(css_class)
            return item

        @staticmethod
        def button(text, css_class="action"):
            item = Gtk.Button(label=text)
            item.add_css_class(css_class)
            return item

        def do_activate(self):
            if self.window:
                self.window.present()
                return
            window = Gtk.ApplicationWindow(application=self)
            self.window = window
            window.set_title("Traductor rápido · Inglés y español")
            window.set_decorated(False)
            window.add_css_class("traductor-window")
            window.set_default_size(800, 620)

            LayerShell.init_for_window(window)
            LayerShell.set_namespace(window, "traductor-ingles-espanol")
            LayerShell.set_layer(window, LayerShell.Layer.TOP)
            LayerShell.set_keyboard_mode(window, LayerShell.KeyboardMode.ON_DEMAND)
            LayerShell.set_exclusive_zone(window, 0)
            monitor = _focused_monitor(Gdk.Display.get_default())
            if monitor:
                LayerShell.set_monitor(window, monitor)
            for edge in (LayerShell.Edge.TOP, LayerShell.Edge.BOTTOM,
                         LayerShell.Edge.LEFT, LayerShell.Edge.RIGHT):
                LayerShell.set_anchor(window, edge, True)

            overlay = Gtk.Overlay()
            window.set_child(overlay)
            backdrop = Gtk.Button()
            backdrop.add_css_class("backdrop")
            backdrop.set_hexpand(True)
            backdrop.set_vexpand(True)
            backdrop.set_focusable(False)
            backdrop.connect("clicked", lambda *_: window.close())
            overlay.set_child(backdrop)

            card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            card.add_css_class("traductor-card")
            monitor_width = monitor.get_geometry().width if monitor else 760
            card.set_size_request(max(320, min(680, monitor_width - 40)), -1)
            card.set_halign(Gtk.Align.CENTER)
            card.set_valign(Gtk.Align.CENTER)
            card.set_margin_start(18)
            card.set_margin_end(18)
            card.set_margin_top(18)
            card.set_margin_bottom(18)
            overlay.add_overlay(card)

            header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
            header.add_css_class("header")
            brand_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
            brand_box.append(self.label("ENGLISH PRACTICE", "brand", wrap=False))
            brand_box.append(self.label("Traductor rápido · selecciona, aprende y escucha", "subtitle"))
            header.append(brand_box)
            header.append(Gtk.Box(hexpand=True))
            self.direction_badge = self.label("ES → EN", "pill", wrap=False)
            header.append(self.direction_badge)
            close_button = self.button("✕", "close-action")
            close_button.set_tooltip_text("Cerrar (Esc)")
            close_button.connect("clicked", lambda *_: window.close())
            header.append(close_button)
            card.append(header)

            body = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
            body.set_margin_start(22)
            body.set_margin_end(22)
            body.set_margin_bottom(14)
            body_scroll = Gtk.ScrolledWindow()
            body_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
            body_scroll.set_min_content_height(90)
            monitor_height = monitor.get_geometry().height if monitor else 900
            body_scroll.set_max_content_height(max(240, min(520, monitor_height - 270)))
            body_scroll.set_propagate_natural_height(True)
            body_scroll.set_child(body)
            card.append(body_scroll)

            source_panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
            source_panel.add_css_class("panel")
            source_head = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            source_head.append(self.label("SELECCIÓN", "panel-title", wrap=False))
            source_head.append(Gtk.Box(hexpand=True))
            source_panel.append(source_head)
            self.source_label = self.label(self.original_text, "source-text", selectable=True)
            self.source_label.set_max_width_chars(74)
            source_panel.append(self.source_label)
            body.append(source_panel)

            target_panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
            target_panel.add_css_class("panel")
            self.translation_title = self.label("TRADUCCIÓN", "panel-title", wrap=False)
            target_panel.append(self.translation_title)
            self.translation_label = self.label("Detectando idioma y traduciendo…", "translated-text", selectable=True)
            self.translation_label.set_max_width_chars(58)
            target_panel.append(self.translation_label)
            body.append(target_panel)

            self.spinner = Gtk.Spinner()
            self.spinner.set_halign(Gtk.Align.START)
            self.status_label = self.label("", "status")
            status_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            status_row.append(self.spinner)
            status_row.append(self.status_label)
            body.append(status_row)

            self.dictionary_expander = Gtk.Expander(label="📚 Diccionario y ejemplos de uso")
            self.dictionary_expander.set_visible(False)
            self.dictionary_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
            self.dictionary_box.set_margin_start(8)
            self.dictionary_box.set_margin_top(6)
            self.dictionary_expander.set_child(self.dictionary_box)
            body.append(self.dictionary_expander)

            actions = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            actions.set_margin_start(22)
            actions.set_margin_end(22)
            actions.set_margin_bottom(10)
            self.copy_button = self.button("⧉  Copiar traducción")
            self.copy_button.set_sensitive(False)
            self.copy_button.connect("clicked", self.copy_translation)
            actions.append(self.copy_button)
            self.swap_button = self.button("⇄  Invertir")
            self.swap_button.connect("clicked", self.swap_direction)
            actions.append(self.swap_button)
            actions.append(Gtk.Box(hexpand=True))

            speed_label = self.label("Voz", "muted", wrap=False)
            actions.append(speed_label)
            self.speed_dropdown = Gtk.DropDown.new_from_strings(
                ["0.75× · lento", "0.9× · claro", "1.0× · normal", "1.1× · rápido"]
            )
            speed_values = (0.75, 0.9, 1.0, 1.1)
            selected_speed = min(
                range(len(speed_values)),
                key=lambda index: abs(speed_values[index] - self.settings["speech_speed"]),
            )
            self.speed_dropdown.set_selected(selected_speed)
            actions.append(self.speed_dropdown)
            self.listen_button = self.button("🔊  Escuchar inglés", "primary-action")
            self.listen_button.set_tooltip_text("Pronuncia el texto en inglés con Piper offline")
            self.listen_button.connect("clicked", self.listen_english)
            actions.append(self.listen_button)
            card.append(actions)

            footer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            footer.set_margin_start(22)
            footer.set_margin_end(22)
            footer.set_margin_bottom(15)
            footer.append(self.label(
                "Esc para cerrar · traducción online · no uses texto sensible",
                "muted",
            ))
            footer.append(Gtk.Box(hexpand=True))
            self.voice_note = self.label("", "muted")
            footer.append(self.voice_note)
            card.append(footer)

            click_keys = Gtk.EventControllerKey()
            click_keys.connect("key-pressed", self.on_key_pressed)
            window.add_controller(click_keys)
            window.connect("close-request", self.on_close)
            window.present()
            if self.demo:
                result = {
                    "source_text": self.original_text,
                    "translation": "cuidar de",
                    "source_language": "en",
                    "target_language": "es",
                    "english_text": self.original_text,
                    "dictionary": {
                        "part_of_speech": "phrasal verb",
                        "ipa": "/lʊk ˈæftər/",
                        "definitions": ["To take care of someone or something."],
                        "source_url": "https://en.wiktionary.org/wiki/look_after",
                    },
                    "examples": [{
                        "original": "She looks after her little brother.",
                        "translated": "Ella cuida de su hermano pequeño.",
                    }],
                }
                self.show_result(result)
                GLib.timeout_add(1800, lambda: (window.close(), False)[1])
            else:
                self.start_translation()

        def on_key_pressed(self, _controller, keyval, _keycode, _state):
            if Gdk.keyval_name(keyval) == "Escape":
                self.window.close()
                return True
            return False

        def on_close(self, *_args):
            self.audio_cancel.set()
            with self.audio_lock:
                process = self.audio_process
            if process and process.poll() is None:
                try:
                    process.terminate()
                except OSError:
                    pass
            return False

        def start_translation(self):
            self.generation += 1
            generation = self.generation
            self.spinner.start()
            self.status_label.set_text("Detectando idioma y buscando traducción…")
            self.translation_label.set_text("Traduciendo…")
            self.copy_button.set_sensitive(False)
            threading.Thread(
                target=self.translate_worker,
                args=(generation, self.forced_source),
                daemon=True,
            ).start()

        def translate_worker(self, generation, forced_source):
            try:
                result = translate_selection(self.original_text, forced_source=forced_source)
            except Exception as exc:  # El popup muestra el error; el proceso no debe desaparecer.
                GLib.idle_add(self.show_error, generation, str(exc))
            else:
                GLib.idle_add(self.show_result, result, generation)

        def show_error(self, generation, message):
            if generation != self.generation or not self.window:
                return False
            self.spinner.stop()
            self.translation_label.set_text("No se pudo obtener la traducción.")
            detail = message.strip().replace("\n", " ")[:120]
            self.status_label.set_text(f"Comprueba la conexión y pulsa «Invertir» para reintentar. {detail}")
            self.copy_button.set_sensitive(False)
            return False

        def show_result(self, result, generation=None):
            if generation is not None and generation != self.generation:
                return False
            self.result = result
            self.spinner.stop()
            source = result["source_language"].upper()
            target = result["target_language"].upper()
            self.direction_badge.set_text(f"{source} → {target}")
            self.translation_title.set_text(f"TRADUCCIÓN · {target}")
            self.source_label.set_text(result["source_text"])
            self.translation_label.set_text(result["translation"])
            self.status_label.set_text("Traducción lista · el audio pronuncia siempre la parte en inglés.")
            self.copy_button.set_sensitive(bool(result["translation"]))
            self.render_dictionary(result)
            self.dictionary_expander.set_expanded(bool(result["dictionary"] or result["examples"]))
            if not Path(self.settings["piper_model"]).is_file():
                self.voice_note.set_text("Voz offline: copia el comando con 🔊")
            else:
                self.voice_note.set_text("Piper · sin conexión")
            return False

        def render_dictionary(self, result):
            while child := self.dictionary_box.get_first_child():
                self.dictionary_box.remove(child)
            dictionary = result.get("dictionary") or {}
            if not is_dictionary_candidate(result["source_text"]):
                self.dictionary_expander.set_visible(False)
                return
            self.dictionary_expander.set_visible(True)
            meta = " · ".join(filter(None, [
                dictionary.get("part_of_speech", ""),
                dictionary.get("ipa", "IPA no disponible"),
            ]))
            if meta:
                self.dictionary_box.append(self.label(meta, "dict-title"))
            for definition in dictionary.get("definitions", [])[:3]:
                self.dictionary_box.append(self.label("•  " + definition, "definition"))
            source_url = dictionary.get("source_url")
            if source_url:
                attribution = Gtk.LinkButton.new_with_label(
                    source_url,
                    "Fuente: FreeDictionaryAPI.com · Wiktionary (CC BY-SA 4.0)",
                )
                attribution.add_css_class("muted")
                attribution.set_halign(Gtk.Align.START)
                self.dictionary_box.append(attribution)
            elif dictionary:
                self.dictionary_box.append(self.label(
                    "Fuente: FreeDictionaryAPI.com · Wiktionary (CC BY-SA 4.0)",
                    "muted",
                ))
            examples = result.get("examples", [])
            if examples:
                self.dictionary_box.append(self.label("EJEMPLOS", "panel-title", wrap=False))
                for example in examples:
                    self.dictionary_box.append(self.label("EN  ·  " + example["original"], "example-en"))
                    if example.get("translated"):
                        self.dictionary_box.append(self.label("ES  ·  " + example["translated"], "example-es"))
            elif not dictionary:
                self.dictionary_box.append(self.label(
                    "No se encontró una entrada; la traducción sigue disponible.",
                    "muted",
                ))

        def copy_translation(self, *_args):
            if not self.result:
                return
            clipboard = Gdk.Display.get_default().get_clipboard()
            clipboard.set_content(make_clipboard_content_provider(self.result["translation"]))
            self.status_label.set_text("Traducción copiada al portapapeles.")

        def swap_direction(self, *_args):
            if self.result:
                self.forced_source = self.result["target_language"]
            else:
                self.forced_source = "en" if self.forced_source == "es" else "es"
            self.start_translation()

        def copy_voice_command(self, *_args):
            clipboard = Gdk.Display.get_default().get_clipboard()
            clipboard.set_content(make_clipboard_content_provider(VOICE_INSTALL_COMMAND))
            self.status_label.set_text("Comando copiado. Pégalo en una terminal; no requiere sudo.")

        def listen_english(self, *_args):
            model = Path(self.settings["piper_model"]).expanduser()
            if not model.is_file():
                self.copy_voice_command()
                return
            if self.audio_thread and self.audio_thread.is_alive():
                self.audio_cancel.set()
                with self.audio_lock:
                    process = self.audio_process
                if process and process.poll() is None:
                    try:
                        process.terminate()
                    except OSError:
                        pass
                self.status_label.set_text("Deteniendo audio…")
                return
            if not self.result or not self.result.get("english_text"):
                return
            if not shutil.which("piper-tts") or not shutil.which("pw-play"):
                self.status_label.set_text("Falta piper-tts o pw-play; instala el paquete piper-tts.")
                return
            speed_values = (0.75, 0.9, 1.0, 1.1)
            speed = speed_values[min(self.speed_dropdown.get_selected(), len(speed_values) - 1)]
            self.audio_cancel.clear()
            self.listen_button.set_label("⏹  Detener audio")
            self.status_label.set_text("Preparando voz inglesa local…")
            self.audio_thread = threading.Thread(
                target=self.speech_worker,
                args=(self.result["english_text"], str(model), speed),
                daemon=True,
            )
            self.audio_thread.start()

        def speech_worker(self, text, model, speed):
            audio_path = None
            message = "Audio finalizado."
            try:
                cache_dir = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "traductor" / "audio"
                cache_dir.mkdir(parents=True, exist_ok=True)
                with tempfile.NamedTemporaryFile(
                    prefix="voz-", suffix=".wav", dir=cache_dir, delete=False
                ) as audio_file:
                    audio_path = Path(audio_file.name)
                command = [
                    "piper-tts", "--model", model, "--output-file", str(audio_path),
                    "--length-scale", str(length_scale_for_speed(speed)), "--sentence-silence", "0.12",
                ]
                process = subprocess.Popen(
                    command,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.PIPE,
                    text=True,
                    encoding="utf-8",
                )
                with self.audio_lock:
                    self.audio_process = process
                _stdout, stderr = process.communicate(text, timeout=50)
                if self.audio_cancel.is_set():
                    message = "Audio detenido."
                    return
                if process.returncode != 0:
                    raise RuntimeError((stderr or "Piper no pudo generar el audio.").strip()[-260:])
                if self.audio_cancel.is_set():
                    message = "Audio detenido."
                else:
                    player = subprocess.Popen(
                        ["pw-play", str(audio_path)],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        text=True,
                        encoding="utf-8",
                    )
                    with self.audio_lock:
                        self.audio_process = player
                    while player.poll() is None:
                        if self.audio_cancel.wait(0.08):
                            player.terminate()
                            message = "Audio detenido."
                            break
                    if player.returncode not in (None, 0) and not self.audio_cancel.is_set():
                        message = "No se pudo reproducir el audio con PipeWire."
            except (OSError, RuntimeError, subprocess.TimeoutExpired) as exc:
                if isinstance(exc, subprocess.TimeoutExpired):
                    with self.audio_lock:
                        process = self.audio_process
                    if process and process.poll() is None:
                        process.kill()
                        try:
                            process.communicate(timeout=2)
                        except (OSError, subprocess.TimeoutExpired):
                            pass
                message = str(exc) or "Falló la generación de voz offline."
            finally:
                if audio_path:
                    audio_path.unlink(missing_ok=True)
                with self.audio_lock:
                    self.audio_process = None
                GLib.idle_add(self.speech_finished, message)

        def speech_finished(self, message):
            if self.window:
                self.listen_button.set_label("🔊  Escuchar inglés")
                self.status_label.set_text(message)
            return False

    app = TranslatorApp()
    return app.run(None)


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Traduce una selección ES/EN en Hyprland")
    parser.add_argument("--text", help=argparse.SUPPRESS)
    parser.add_argument("--demo", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()

    selected = args.text if args.text is not None else capture_selection()
    try:
        selected = normalize_text(selected)
    except ValueError as exc:
        _notify("Selección demasiado larga", str(exc))
        return 2
    if not selected:
        _notify("No hay texto seleccionado", "Selecciona una palabra o frase y vuelve a intentarlo.")
        return 1

    close_existing_popup()
    pid_file = _pid_file()
    try:
        pid_file.parent.mkdir(parents=True, exist_ok=True)
        pid_file.write_text(str(os.getpid()), encoding="ascii")
    except OSError:
        pass
    atexit.register(_remove_pid_file, pid_file, os.getpid())
    return launch_window(selected, load_settings(), demo=args.demo)


if __name__ == "__main__":
    raise SystemExit(main())
