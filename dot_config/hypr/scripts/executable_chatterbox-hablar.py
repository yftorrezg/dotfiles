#!/usr/bin/env python3
# Usado por leer-seleccion.sh (motor "chatterbox"). No se llama a mano.
import sys
import soundfile as sf
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

def main():
    if len(sys.argv) < 3:
        print("uso: chatterbox-hablar.py <texto> <salida.wav>", file=sys.stderr)
        sys.exit(1)
    text = sys.argv[1]
    out_path = sys.argv[2]
    model = ChatterboxMultilingualTTS.from_pretrained(device="cpu")
    wav = model.generate(text, language_id="es")
    sf.write(out_path, wav.squeeze(0).cpu().numpy(), model.sr)

if __name__ == "__main__":
    main()
