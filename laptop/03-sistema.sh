#!/usr/bin/env bash
# Fase 3 — archivos de /etc para la ThinkPad E14 Gen4 (parte "escritorio / sistema").
# Lo ejecuta el usuario:  bash ~/migracion-laptop/03-sistema.sh
#
# Qué se copia (y por qué) — todo sale de ~/migracion-laptop/staging-system/etc/:
#   - pam.d/greetd: igual al de la laptop + pam_gnome_keyring (desbloquea el llavero al iniciar
#     sesión; sin esto Brave/VS Code/yt-dlp piden la contraseña del llavero en cada arranque).
#   - udev/rules.d/40-opendeck-*.rules: permisos para el Mirabox HSV293S y el Fifine D6
#     (Stream Deck). La regla de Elgato (40-streamdeck.rules) ya la instala opendeck-bin.
#
# Qué NO se copia de la PC (decidido comparando con el /etc de la laptop):
#   - vconsole.conf / X11 00-keyboard.conf: la PC tenía "es"; la laptop ya tiene "uk"/"gb" (correcto).
#   - locale.conf y greetd/config.toml: idénticos a los de la laptop.
#   - limine-snapper-sync.conf: el de la laptop es más nuevo; la PC solo añadía excluir "Windows*".
#   - modules-load.d/i2c-dev.conf: era para ddcutil (brillo de monitores externos por DDC); no hace falta.
#   - modprobe.d/disable_btusb-autosuspend.conf: gasta batería; ver sección opcional al final.
#   - logind.conf.d/no-teclas-fantasma.conf: dejaría muerto el botón de encendido (era un problema de la PC).
#   - logid.cfg y 99-logid-m720.rules: los instala 04-voz-servicios.sh (otro bloque).
# Tapa: se deja el comportamiento por defecto de logind (cerrar = suspender; con la Arzopa
# conectada = no suspende y Hyprland apaga la interna). Noctalia bloquea antes de suspender.
set -euo pipefail

ETC="$HOME/migracion-laptop/staging-system/etc"
paso() { printf '\n==> %s\n' "$*"; }

[[ -d $ETC ]] || { echo "No existe $ETC" >&2; exit 1; }

paso "PAM de greetd con gnome-keyring (copia de seguridad del actual en /etc/pam.d/greetd.bak-migracion)"
if ! cmp -s "$ETC/pam.d/greetd" /etc/pam.d/greetd; then
    sudo cp -a /etc/pam.d/greetd /etc/pam.d/greetd.bak-migracion
    sudo install -m644 "$ETC/pam.d/greetd" /etc/pam.d/greetd
else
    echo "    ya estaba igual, no se toca"
fi

paso "PAM de la pantalla de bloqueo de Noctalia (evita quedar bloqueado fuera de la sesión)"
# Noctalia llama a pam_start con su propio nombre de servicio; si /etc/pam.d/noctalia no existe,
# PAM usa /etc/pam.d/other, que lo deniega todo. Lo apuntamos a 'login' (contraseña normal).
if [[ ! -e /etc/pam.d/noctalia ]]; then
    printf '#%%PAM-1.0\nauth      include   login\naccount   include   login\n' \
        | sudo install -m644 /dev/stdin /etc/pam.d/noctalia
else
    echo "    ya existe, no se toca"
fi

paso "thermald fuera: en esta ThinkPad la temperatura la gestiona el firmware Lenovo (DYTC)"
sudo systemctl disable --now thermald 2>/dev/null || true
sudo pacman -Rns --noconfirm thermald 2>/dev/null || true

paso "Reglas udev del Stream Deck (Mirabox AKP153 y Fifine D6)"
sudo install -Dm644 "$ETC/udev/rules.d/40-opendeck-akp153.rules" /etc/udev/rules.d/40-opendeck-akp153.rules
sudo install -Dm644 "$ETC/udev/rules.d/40-opendeck-ampgd6.rules" /etc/udev/rules.d/40-opendeck-ampgd6.rules
sudo udevadm control --reload-rules
sudo udevadm trigger --subsystem-match=usb --subsystem-match=hidraw || true
echo "    Desenchufa y vuelve a enchufar los Stream Deck y reinicia OpenDeck (pkill opendeck)."

paso "Huella (lector Elan): registrar un dedo para desbloquear Noctalia y para sudo"
# CachyOS ya trae 'auth sufficient pam_fprintd.so' en /etc/pam.d/sudo, y la pantalla de bloqueo
# de Noctalia usa fprintd directamente (lockscreen.fingerprint = true en noctalia/config.toml).
# NO se agrega huella al login de greetd a propósito: con huella el llavero (gnome-keyring)
# no se desbloquea y te lo pediría igual. El login sigue siendo con contraseña.
if fprintd-list "$USER" 2>/dev/null | grep -q 'no fingers enrolled'; then
    echo "    No hay huellas registradas. Ejecuta (sin sudo) cuando quieras:  fprintd-enroll"
    echo "    y pruébala con:  fprintd-verify"
else
    echo "    Ya hay huella registrada."
fi

# ---------------------------------------------------------------------------------------
# OPCIONAL (descomentar solo si hace falta):
#
# Si el teclado K380 o el mouse M720 por Bluetooth se desconectan solos, desactivar el
# autosuspend del Bluetooth (cuesta un poco de batería):
#   sudo install -Dm644 /dev/stdin /etc/modprobe.d/disable_btusb-autosuspend.conf <<<'options btusb enable_autosuspend=0'
#
# Si la Arzopa soportara DDC/CI y quisieras su brillo desde Noctalia:
#   echo i2c-dev | sudo tee /etc/modules-load.d/i2c-dev.conf && sudo usermod -aG i2c "$USER"
#   (y en noctalia/config.toml: [brightness] enable_ddcutil = true)
# ---------------------------------------------------------------------------------------

paso "Listo. Cierra sesión y vuelve a entrar para que el llavero se desbloquee solo."
