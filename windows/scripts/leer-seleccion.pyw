"""SUPER+R en Windows: lee en voz alta el texto que yafer.ahk dejó en un archivo.

Versión de leer-seleccion.sh (CachyOS): limpia el texto con limpiar-texto.py
(la fuente común del repo chezmoi) y lo lee con edge-tts, mandando el
audio por streaming a ffplay para que empiece a sonar enseguida.
Uso: leer-seleccion.pyw <texto.txt> <yafer.ini>
"""
import asyncio
import configparser
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

import edge_tts

sys.dont_write_bytecode = True  # no dejar __pycache__ en la carpeta común de scripts de Linux
AQUI = Path(__file__).resolve().parent
_RUTA_WIN = re.compile(r"[A-Za-z]:\\(?:[^\\\s]+\\)*[^\\\s]*")


def cargar_limpiar_texto():
    """El mismo limpiar-texto.py de CachyOS (emojis, URLs, rutas Unix), desde la fuente común del repo."""
    ruta = AQUI.parents[1] / "dot_config" / "hypr" / "scripts" / "executable_limpiar-texto.py"
    if not ruta.exists():
        return None
    spec = importlib.util.spec_from_file_location("limpiar_texto", ruta)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def limpiar(texto: str) -> str:
    lt = cargar_limpiar_texto()
    if lt:  # mismo orden que main() de limpiar-texto.py
        texto = lt._EMOJI_RE.sub(" ", texto)
        texto = lt._URL_RE.sub(lt._replace_url, texto)
        texto = lt._PATH_RE.sub(lt._replace_path, texto)
    else:
        texto = re.sub(r"https?://\S+", " este enlace ", texto)
    texto = _RUTA_WIN.sub(" esta ruta ", texto)
    # Lo que en leer-seleccion.sh hacían los sed: símbolos de Markdown y código.
    texto = re.sub(r"[`*_#>|~=]+", " ", texto)
    return re.sub(r"\s+", " ", texto).strip()


def leer_config(ini: Path) -> tuple[str, str]:
    cfg = configparser.ConfigParser()
    if ini.exists():
        cfg.read(ini, encoding="utf-16") if ini.read_bytes()[:2] in (b"\xff\xfe", b"\xfe\xff") else cfg.read(ini, encoding="utf-8")
    voz = cfg.get("voz", "voz", fallback="es-AR-ElenaNeural")
    vel = int(cfg.get("voz", "velocidad", fallback="40"))
    return voz, f"{vel:+d}%"


async def hablar(texto: str, voz: str, rate: str) -> None:
    ffplay = subprocess.Popen(
        ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", "-i", "pipe:0"],
        stdin=subprocess.PIPE,
        creationflags=subprocess.CREATE_NO_WINDOW,
    )
    try:
        async for parte in edge_tts.Communicate(texto, voz, rate=rate).stream():
            if parte["type"] == "audio":
                ffplay.stdin.write(parte["data"])
    finally:
        ffplay.stdin.close()
        ffplay.wait()


def main() -> int:
    texto = Path(sys.argv[1]).read_text(encoding="utf-8-sig")
    voz, rate = leer_config(Path(sys.argv[2]))
    texto = limpiar(texto)
    if texto:
        asyncio.run(hablar(texto, voz, rate))
    return 0


if __name__ == "__main__":
    sys.exit(main())
