#!/usr/bin/env bash
# Lo que no se ejecutó de la fase 1 porque piper-tts (AUR) falló al compilar.
# Uso:  bash ~/migracion-laptop/02-pendientes-fase1.sh
set -uo pipefail

echo "==> Quitando duplicados (Brave y kitty son los que usas)"
sudo pacman -Rns --noconfirm firefox alacritty

echo "==> Docker sin sudo (arranca solo al usarlo)"
sudo usermod -aG docker "$USER"
sudo systemctl enable docker.socket

echo "==> Energía y temperatura"
sudo systemctl enable --now power-profiles-daemon thermald

echo "==> Batería: carga hasta 80% (recarga si baja de 75%), persistente"
sudo tee /etc/tmpfiles.d/thinkpad-bateria.conf >/dev/null <<'EOF'
w /sys/class/power_supply/BAT0/charge_control_start_threshold - - - - 75
w /sys/class/power_supply/BAT0/charge_control_end_threshold - - - - 80
EOF
sudo systemd-tmpfiles --create /etc/tmpfiles.d/thinkpad-bateria.conf

echo
echo "Comprobación:"
echo "  batería máx: $(cat /sys/class/power_supply/BAT0/charge_control_end_threshold)%"
systemctl is-active thermald power-profiles-daemon docker.socket
echo "==> Listo. Avísale a Claude."
