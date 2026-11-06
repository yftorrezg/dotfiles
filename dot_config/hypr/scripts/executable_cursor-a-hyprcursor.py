#!/usr/bin/env python3
"""Agrega el formato hyprcursor a un tema de cursor que solo tiene Xcursor.

Por qué: las apps Wayland (kitty, Brave, Dolphin…) piden el cursor por el
protocolo cursor-shape y lo dibuja Hyprland, que con enable_hyprcursor busca
`manifest.hl` + `hyprcursors/`. Si el tema no lo tiene, hyprcursor cae al primer
tema que sí lo tenga (Bibata) y el cursor elegido solo se ve en apps que dibujan
el suyo (LibreOffice).

Uso: cursor-a-hyprcursor.py <tema|ruta> [--forzar]
     cursor-a-hyprcursor.py --aplicar <tema> [tamaño]
       (asegura el formato y aplica el cursor en TODAS partes: Hyprland,
        gsettings, ~/.icons/default y gtk-3.0/4.0 settings.ini)
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ICONOS = [Path.home() / ".local/share/icons", Path.home() / ".icons", Path("/usr/share/icons")]


def carpeta_tema(tema):
    p = Path(tema)
    if p.is_dir():
        return p
    for base in ICONOS:
        if (base / tema / "cursors").is_dir():
            return base / tema
    return None


def asegurar(tema, forzar=False):
    """Devuelve True si el tema queda con formato hyprcursor."""
    d = carpeta_tema(tema)
    if d is None or not (d / "cursors").is_dir():
        return False
    if (d / "manifest.hl").exists() and (d / "hyprcursors").is_dir() and not forzar:
        return True
    if not os.access(d, os.W_OK) or not shutil.which("hyprcursor-util"):
        return False
    with tempfile.TemporaryDirectory(prefix="hyprcursor-") as tmp:
        tmp = Path(tmp)
        ok = lambda *a: subprocess.run(["hyprcursor-util", *a], cwd=tmp, capture_output=True).returncode == 0
        if not ok("--extract", str(d), "-o", str(tmp)):
            return False
        ext = next(tmp.glob("extracted_*"), None)
        if ext is None:
            return False
        man = ext / "manifest.hl"
        man.write_text(re.sub(r"(?m)^name = .*$", f"name = {d.name}", man.read_text()))
        if not ok("--create", str(ext), "-o", str(tmp)):
            return False
        hecho = next(tmp.glob("theme_*"), None)
        if hecho is None or not (hecho / "manifest.hl").exists():
            return False
        shutil.rmtree(d / "hyprcursors", ignore_errors=True)
        shutil.copytree(hecho / "hyprcursors", d / "hyprcursors")
        shutil.copy2(hecho / "manifest.hl", d / "manifest.hl")
    return True


def aplicar(tema, tam=None):
    tam = str(tam or os.environ.get("XCURSOR_SIZE", "24"))
    asegurar(tema)
    for args in (["hyprctl", "setcursor", tema, tam],
                 ["gsettings", "set", "org.gnome.desktop.interface", "cursor-theme", tema]):
        subprocess.run(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # apps X11 sin tema propio heredan de ~/.icons/default
    por_defecto = Path.home() / ".icons/default/index.theme"
    try:
        por_defecto.parent.mkdir(parents=True, exist_ok=True)
        por_defecto.write_text(f"[Icon Theme]\nName=Default\nComment=Default Cursor Theme\nInherits={tema}\n")
    except OSError:
        pass
    for ini in (Path.home() / ".config/gtk-3.0/settings.ini", Path.home() / ".config/gtk-4.0/settings.ini"):
        try:
            txt = ini.read_text()
        except OSError:
            continue
        nuevo = re.sub(r"(?m)^gtk-cursor-theme-name=.*$", f"gtk-cursor-theme-name={tema}", txt)
        if nuevo != txt:
            ini.write_text(nuevo)


if __name__ == "__main__":
    if "--aplicar" in sys.argv:
        resto = sys.argv[sys.argv.index("--aplicar") + 1:]
        if not resto:
            sys.exit(__doc__)
        aplicar(resto[0], resto[1] if len(resto) > 1 else None)
        sys.exit(0)
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    fallos = [t for t in args if not asegurar(t, "--forzar" in sys.argv)]
    for t in args:
        print(("✗ " if t in fallos else "✓ ") + t)
    sys.exit(1 if fallos else 0)
