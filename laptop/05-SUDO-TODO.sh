#!/usr/bin/env bash
# Fase 2 — TODO lo que necesita sudo, en un solo paso. Lo ejecuta el usuario:
#   bash ~/migracion-laptop/05-SUDO-TODO.sh
set -euo pipefail
cd "$HOME/migracion-laptop"

echo "==> Paquetes que faltaban (cookies de yt-dlp, OCR inglés, descargas)"
sudo pacman -S --needed --noconfirm python-secretstorage tesseract-data-eng aria2 \
    python-pycryptodomex python-mutagen

echo "==> Sistema: PAM, thermald, udev Stream Deck, huella"
bash ./03-sistema.sh

echo "==> Voz/servicios: grupos input+audio, uinput (ydotool), logid (M720)"
bash ./04-voz-servicios.sh sistema

echo
echo "==> LISTO. Avísale a Claude (él copia las configs). Luego CIERRA SESIÓN y vuelve a entrar."
