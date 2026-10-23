#!/usr/bin/env python3
"""Daemon que mantiene los modelos de voz de Piper cargados en memoria.

Invocar `piper-tts` directamente carga el modelo ONNX en cada lectura
(~1.7-2.4s de arranque, medido en este hardware, antes de generar audio).
Este daemon lo hace una sola vez por modelo y lo mantiene cacheado; después
solo queda la inferencia (mucho más rápida). Usado por leer-seleccion.sh
a través de piper-client.py.

Protocolo: socket unix, una línea JSON de pedido
  {"text": "...", "model": "/ruta/al/modelo.onnx", "length_scale": 1.0}
seguida de la respuesta en PCM crudo (s16le, mono, sample_rate del modelo)
hasta que el server cierra la conexión.
"""
import json
import logging
import os
import socket
import socketserver
import sys
import threading

from piper import PiperVoice, SynthesisConfig

SOCK_PATH = os.environ.get("PIPER_DAEMON_SOCK") or os.path.expanduser(
    "~/.cache/piper-voz.sock"
)

# Voces bajadas de Hugging Face (rhasspy/piper-voices) a una ruta de usuario,
# con la misma estructura de carpetas que el paquete AUR de la PC. El módulo
# `piper` viene de `pipx install piper-tts` (el servicio corre con el python
# de ese venv, ver piper-voz-daemon.service).
VOICES_DIR = os.environ.get("PIPER_VOICES_DIR") or os.path.expanduser(
    "~/.local/share/piper-voices"
)

# Se precargan al arrancar el daemon (no en el primer pedido) para que la
# primera lectura de la sesión ya sea rápida. En una laptop con poca RAM
# libre se puede dejar solo Daniela.
PRELOAD_VOICES = [
    os.path.join(VOICES_DIR, "es/es_AR/daniela/high/es_AR-daniela-high.onnx"),
    os.path.join(VOICES_DIR, "es/es_MX/claude/high/es_MX-claude-high.onnx"),
]


def resolve_model(model_path: str) -> str:
    """Si llega una ruta vieja (p. ej. la del paquete AUR), busca el mismo
    modelo (subruta después de 'piper-voices/') dentro de VOICES_DIR."""
    if os.path.isfile(model_path):
        return model_path
    marker = "/piper-voices/"
    if marker in model_path:
        candidate = os.path.join(VOICES_DIR, model_path.split(marker, 1)[1])
        if os.path.isfile(candidate):
            return candidate
    return model_path

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
_log = logging.getLogger("piper-daemon")

_voices: dict[str, PiperVoice] = {}
_lock = threading.Lock()


def get_voice(model_path: str) -> PiperVoice:
    with _lock:
        voice = _voices.get(model_path)
        if voice is None:
            _log.info("Cargando modelo: %s", model_path)
            voice = PiperVoice.load(model_path)
            _voices[model_path] = voice
        return voice


class Handler(socketserver.BaseRequestHandler):
    def handle(self) -> None:
        f = self.request.makefile("rb")
        line = f.readline()
        if not line:
            return
        try:
            req = json.loads(line)
            text = req["text"]
            model_path = resolve_model(req["model"])
            length_scale = float(req.get("length_scale", 1.0))
            voice = get_voice(model_path)
            syn_config = SynthesisConfig(length_scale=length_scale)
            for chunk in voice.synthesize(text, syn_config):
                self.request.sendall(chunk.audio_int16_bytes)
        except Exception:
            _log.exception("Error generando audio")


class Server(socketserver.ThreadingUnixStreamServer):
    daemon_threads = True
    allow_reuse_address = True


def main() -> None:
    os.makedirs(os.path.dirname(SOCK_PATH), exist_ok=True)
    if os.path.exists(SOCK_PATH):
        os.remove(SOCK_PATH)

    for model_path in PRELOAD_VOICES:
        if os.path.isfile(model_path):
            get_voice(model_path)

    server = Server(SOCK_PATH, Handler)
    _log.info("Escuchando en %s", SOCK_PATH)
    try:
        server.serve_forever()
    finally:
        server.server_close()
        if os.path.exists(SOCK_PATH):
            os.remove(SOCK_PATH)


if __name__ == "__main__":
    main()
