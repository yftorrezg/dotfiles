#!/usr/bin/env python3
"""Genera ~/.config/solaar/rules.yaml para el MX Master 4 (6 botones × clic + 4 gestos + rueda del pulgar).

Cada regla de Solaar solo llama a mx-accion.py con un evento ("haptico-arriba"...); la acción según
el programa con foco se decide allí. Solaar recarga rules.yaml solo al cambiar el archivo.
Uso:  python3 mx-reglas.py          (escribe el archivo)
"""
import os

SCRIPT = os.path.expanduser("~/.config/hypr/scripts/mx-accion.py")
SALIDA = os.path.expanduser("~/.config/solaar/rules.yaml")

# nombre del botón en Solaar -> nombre en mx-accion.py
BOTONES = {
    "Middle Button": "rueda",
    "Smart Shift": "superior",
    "Mouse Gesture Button": "gestos",
    "Back Button": "atras",
    "Forward Button": "adelante",
    "Haptic": "haptico",
}
DIRECCIONES = {"": "click", "Mouse Up": "arriba", "Mouse Down": "abajo",
               "Mouse Left": "izq", "Mouse Right": "der"}


def regla(condicion, evento):
    return (f"- Rule:\n  - {condicion}\n"
            f"  - Execute: [python3, {SCRIPT}, {evento}]\n")


def main():
    partes = ["%YAML 1.3\n---\n"]
    for boton, nombre in BOTONES.items():
        if boton == "Haptic":
            # El panel háptico NO lleva reglas: lo lee anillo.py directo del mouse (hidraw) y abre el anillo
            # radial. Solaar solo lo mantiene "desviado" (config.yaml: divert-keys 416: 1).
            continue
        for mov, direccion in DIRECCIONES.items():
            movs = f"{boton}, {mov}" if mov else boton
            partes.append(regla(f"MouseGesture: [{movs}]", f"{nombre}-{direccion}"))
    # Rueda del pulgar: un evento cada 12 unidades de giro
    partes.append(regla("Test: [thumb_wheel_up, 12]", "pulgar-der"))
    partes.append(regla("Test: [thumb_wheel_down, 12]", "pulgar-izq"))
    partes.append("...\n")
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    with open(SALIDA, "w") as f:
        f.write("".join(partes))
    print(f"escrito {SALIDA}: {(len(BOTONES) - 1) * len(DIRECCIONES) + 2} reglas")


if __name__ == "__main__":
    main()
