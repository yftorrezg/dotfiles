#!/usr/bin/env bash
# Fase 1 — paquetes para la ThinkPad E14 Gen4 (lo ejecuta el usuario con su contraseña)
# Uso:  bash ~/migracion-laptop/01-instalar-paquetes.sh
set -euo pipefail

echo "==> Actualizando sistema"
sudo pacman -Syu --noconfirm

echo "==> Apps del usuario (lista USA de la PC) + extras de laptop"
sudo pacman -S --needed --noconfirm \
  libva-utils intel-gpu-tools \
  ark gwenview mpv satty obsidian \
  libreoffice-fresh libreoffice-fresh-es keepassxc localsend obs-studio \
  wtype ydotool zenity inotify-tools restic rclone \
  python-numpy python-pillow yt-dlp ffmpeg \
  python-gobject gtk4-layer-shell tesseract tesseract-data-spa \
  github-cli nodejs npm python-pipx nwg-displays 7zip \
  thermald \
  gimp kdenlive meld opencode docker docker-compose

echo "==> AUR (paru)"
paru -S --needed --noconfirm \
  visual-studio-code-bin hyprwhspr \
  rustdesk-bin logiops opendeck-bin

echo "==> Quitando duplicados (Brave y kitty son los que usas)"
sudo pacman -Rns --noconfirm firefox alacritty || true

echo "==> Docker sin sudo para tu usuario (el servicio queda apagado; arranca solo al usarlo)"
sudo usermod -aG docker "$USER"
sudo systemctl enable docker.socket

echo "==> Mejoras de laptop: energía y temperatura"
# power-profiles-daemon: noctalia cambia el perfil (ahorro/equilibrado/rendimiento)
sudo systemctl enable --now power-profiles-daemon
# thermald: control térmico de Intel, evita picos de temperatura y bajones en la i7-1255U
sudo systemctl enable --now thermald

echo "==> Batería: carga hasta 80% (vuelve a cargar si baja de 75%), persistente en cada arranque"
sudo tee /etc/tmpfiles.d/thinkpad-bateria.conf >/dev/null <<'EOF'
w /sys/class/power_supply/BAT0/charge_control_start_threshold - - - - 75
w /sys/class/power_supply/BAT0/charge_control_end_threshold - - - - 80
EOF
sudo systemd-tmpfiles --create /etc/tmpfiles.d/thinkpad-bateria.conf

echo "==> Listo. Avísale a Claude."
