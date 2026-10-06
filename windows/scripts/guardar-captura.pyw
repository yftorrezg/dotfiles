"""Guarda la imagen del portapapeles en la ruta dada (Ctrl+Shift+S de yafer.ahk).

La imagen sigue en el portapapeles, así que también queda lista para pegar.
"""
import sys

from PIL import ImageGrab


def main() -> int:
    destino = sys.argv[1]
    img = ImageGrab.grabclipboard()
    if img is None or isinstance(img, list):
        return 1
    img.save(destino)
    return 0


if __name__ == "__main__":
    sys.exit(main())
