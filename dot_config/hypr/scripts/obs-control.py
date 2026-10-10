#!/usr/bin/env python3
"""Controla OBS Studio desde las teclas del deck (WebSocket de OBS, puerto 4455, sin dependencias).

  obs-control.py grabar            empieza o para la grabación (si OBS está cerrado, lo abre grabando)
  obs-control.py pausar            pausa / reanuda la grabación
  obs-control.py escena-siguiente  cambia a la escena siguiente (da la vuelta al final)
  obs-control.py escena-anterior
  obs-control.py estado            imprime si graba y la escena actual
  obs-control.py --preparar        crea la config del WebSocket de OBS (contraseña aleatoria) si no existe

La contraseña vive en ~/.config/obs-studio/plugin_config/obs-websocket/config.json (modo 600);
este script la lee de ahí. Variables solo para pruebas: OBS_PUERTO, OBS_CONFIG, OBS_SIN_AVISO=1.
"""
import base64
import hashlib
import json
import os
import secrets
import socket
import struct
import subprocess
import sys

PUERTO = int(os.environ.get("OBS_PUERTO", "4455"))
CONFIG = os.environ.get("OBS_CONFIG") or os.path.expanduser(
    "~/.config/obs-studio/plugin_config/obs-websocket/config.json")
GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"


def avisar(msg):
    print(msg)
    if not os.environ.get("OBS_SIN_AVISO"):
        subprocess.run(["notify-send", "-t", "2500", "-u", "low", "OBS", msg], check=False)


class WS:
    """Cliente WebSocket mínimo (texto, sin fragmentación) suficiente para obs-websocket v5."""

    def __init__(self, puerto):
        self.s = socket.create_connection(("127.0.0.1", puerto), timeout=4)
        clave = base64.b64encode(os.urandom(16)).decode()
        self.s.sendall((
            "GET / HTTP/1.1\r\nHost: 127.0.0.1\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {clave}\r\nSec-WebSocket-Version: 13\r\n"
            "Sec-WebSocket-Protocol: obswebsocket.json\r\n\r\n").encode())
        cab = b""
        while b"\r\n\r\n" not in cab:
            trozo = self.s.recv(4096)
            if not trozo:
                raise ConnectionError("OBS cerró la conexión")
            cab += trozo
        if b" 101 " not in cab.split(b"\r\n")[0]:
            raise ConnectionError("OBS no aceptó el WebSocket")
        self.resto = cab.split(b"\r\n\r\n", 1)[1]

    def _leer(self, n):
        while len(self.resto) < n:
            trozo = self.s.recv(4096)
            if not trozo:
                raise ConnectionError("conexión cerrada")
            self.resto += trozo
        dato, self.resto = self.resto[:n], self.resto[n:]
        return dato

    def enviar(self, obj):
        datos = json.dumps(obj).encode()
        n = len(datos)
        cab = bytearray([0x81])
        if n < 126:
            cab.append(0x80 | n)
        elif n < 65536:
            cab += bytes([0x80 | 126]) + struct.pack(">H", n)
        else:
            cab += bytes([0x80 | 127]) + struct.pack(">Q", n)
        mascara = os.urandom(4)
        cab += mascara
        self.s.sendall(bytes(cab) + bytes(b ^ mascara[i % 4] for i, b in enumerate(datos)))

    def recibir(self):
        while True:
            b0, b1 = self._leer(2)
            op, n = b0 & 0x0F, b1 & 0x7F
            if n == 126:
                n = struct.unpack(">H", self._leer(2))[0]
            elif n == 127:
                n = struct.unpack(">Q", self._leer(8))[0]
            datos = self._leer(n)
            if op == 0x8:
                raise ConnectionError("OBS cerró la conexión")
            if op == 0x1:
                return json.loads(datos)
            # ping/pong u otros: se ignoran

    def cerrar(self):
        try:
            self.s.close()
        except OSError:
            pass


def contrasena():
    try:
        return json.load(open(CONFIG, encoding="utf-8")).get("server_password", "")
    except (OSError, ValueError):
        return ""


def conectar():
    ws = WS(PUERTO)
    hello = ws.recibir()
    d = {"rpcVersion": 1, "eventSubscriptions": 0}
    auth = hello["d"].get("authentication")
    if auth:
        secreto = base64.b64encode(hashlib.sha256((contrasena() + auth["salt"]).encode()).digest()).decode()
        d["authentication"] = base64.b64encode(hashlib.sha256((secreto + auth["challenge"]).encode()).digest()).decode()
    ws.enviar({"op": 1, "d": d})
    r = ws.recibir()
    if r.get("op") != 2:
        raise ConnectionError("OBS rechazó la contraseña (revisa config.json del WebSocket)")
    return ws


def pedir(ws, tipo, datos=None):
    rid = secrets.token_hex(4)
    ws.enviar({"op": 6, "d": {"requestType": tipo, "requestId": rid, "requestData": datos or {}}})
    while True:
        r = ws.recibir()
        if r.get("op") == 7 and r["d"].get("requestId") == rid:
            est = r["d"]["requestStatus"]
            if not est.get("result"):
                raise RuntimeError(est.get("comment") or f"error {est.get('code')}")
            return r["d"].get("responseData") or {}


def obs_abierto():
    return subprocess.run(["pgrep", "-x", "obs"], capture_output=True).returncode == 0


def preparar():
    if os.path.exists(CONFIG):
        print("Ya existe:", CONFIG)
        return
    os.makedirs(os.path.dirname(CONFIG), exist_ok=True)
    cfg = {"alerts_enabled": False, "auth_required": True, "first_load": False,
           "server_enabled": True, "server_password": secrets.token_urlsafe(18), "server_port": 4455}
    fd = os.open(CONFIG, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=4)
    print("Config creada:", CONFIG)


def escenas(ws):
    r = pedir(ws, "GetSceneList")
    lista = sorted(r["scenes"], key=lambda s: s["sceneIndex"])
    return [s["sceneName"] for s in lista], r["currentProgramSceneName"]


def accion(ws, cmd):
    if cmd == "grabar":
        if pedir(ws, "GetRecordStatus")["outputActive"]:
            ruta = pedir(ws, "StopRecord").get("outputPath", "")
            avisar("■ Grabación guardada\n" + os.path.basename(ruta))
        else:
            pedir(ws, "StartRecord")
            avisar("● Grabando")
    elif cmd == "pausar":
        if not pedir(ws, "GetRecordStatus")["outputActive"]:
            avisar("No estás grabando")
            return
        pedir(ws, "ToggleRecordPause")
        avisar("⏸ En pausa" if pedir(ws, "GetRecordStatus")["outputPaused"] else "▶ Grabando de nuevo")
    elif cmd in ("escena-siguiente", "escena-anterior"):
        nombres, actual = escenas(ws)
        if len(nombres) < 2:
            avisar("Solo hay una escena en OBS")
            return
        paso = 1 if cmd == "escena-siguiente" else -1
        nueva = nombres[(nombres.index(actual) + paso) % len(nombres)]
        pedir(ws, "SetCurrentProgramScene", {"sceneName": nueva})
        avisar("Escena: " + nueva)
    elif cmd == "estado":
        est = pedir(ws, "GetRecordStatus")
        print("grabando" if est["outputActive"] else "sin grabar", "| escena:", escenas(ws)[1])
    else:
        sys.exit(__doc__)


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    cmd = sys.argv[1]
    if cmd == "--preparar":
        return preparar()
    try:
        ws = conectar()
    except (ConnectionError, OSError) as e:
        if not obs_abierto() and cmd == "grabar":
            avisar("Abriendo OBS y empezando a grabar…")
            subprocess.Popen(["uwsm", "app", "--", "obs", "--startrecording"], start_new_session=True,
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
        elif not obs_abierto():
            avisar("OBS está cerrado: ábrelo con la tecla OBS")
        else:
            avisar(f"No puedo hablar con OBS: {e}\nActiva Herramientas → Ajustes del servidor WebSocket")
        return
    try:
        accion(ws, cmd)
    except (RuntimeError, ConnectionError, KeyError) as e:
        avisar(f"OBS: {e}")
    finally:
        ws.cerrar()


if __name__ == "__main__":
    main()
