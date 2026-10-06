#!/usr/bin/env python3
"""Cliente del daemon de Piper (ver piper-daemon.py).

Uso: piper-client.py <modelo.onnx> <length_scale>   (texto por stdin)
Escribe el audio (PCM crudo s16le mono) a stdout. Sale con código != 0
si no logra conectar al daemon (por ejemplo si no está corriendo), para
que quien lo llama pueda usar un fallback.
"""
import json
import os
import socket
import sys


def main() -> int:
    if len(sys.argv) != 3:
        print("uso: piper-client.py <modelo.onnx> <length_scale>", file=sys.stderr)
        return 2

    model_path, length_scale = sys.argv[1], sys.argv[2]
    text = sys.stdin.read()

    sock_path = os.environ.get("PIPER_DAEMON_SOCK") or os.path.expanduser(
        "~/.cache/piper-voz.sock"
    )
    req = json.dumps(
        {"text": text, "model": model_path, "length_scale": float(length_scale)}
    ) + "\n"

    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
        s.connect(sock_path)
        s.sendall(req.encode("utf-8"))
        s.shutdown(socket.SHUT_WR)
        while True:
            chunk = s.recv(65536)
            if not chunk:
                break
            sys.stdout.buffer.write(chunk)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except OSError as e:
        print(f"piper-client: no se pudo conectar al daemon: {e}", file=sys.stderr)
        sys.exit(1)
