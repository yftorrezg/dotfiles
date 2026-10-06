#!/usr/bin/env bash
# Auditoría de la laptop: revisa que la migración siga sana. Sin sudo, no cambia nada.
#   bash ~/migracion-laptop/auditoria.sh
export PATH="$HOME/.local/bin:$PATH"
ok=0; mal=0; avisos=0
bien()  { printf '  \e[32m✔\e[0m %s\n' "$*"; ok=$((ok+1)); }
falla() { printf '  \e[31m✘\e[0m %s\n' "$*"; mal=$((mal+1)); }
aviso() { printf '  \e[33m!\e[0m %s\n' "$*"; avisos=$((avisos+1)); }
check() { local d=$1; shift; if "$@" >/dev/null 2>&1; then bien "$d"; else falla "$d"; fi; }
sec()   { printf '\n\e[1m%s\e[0m\n' "$*"; }

sec "Hyprland"
errs=$(hyprctl configerrors 2>/dev/null | grep -v '^\s*$')
[[ -z $errs ]] && bien "config sin errores" || falla "errores de config: $errs"
hyprctl monitors | grep -qE 'scale: 1(\.0+)?$' && bien "eDP-1 a escala 1" || aviso "escala de eDP-1 distinta de 1"
[[ $(hyprctl getoption input:kb_layout | awk '/str:/{print $2}') == gb ]] && bien "teclado gb" || falla "teclado no es gb"
check "luac: todos los .lua de Hyprland" bash -c 'for f in ~/.config/hypr/hyprland.lua ~/.config/hypr/config/*.lua; do luac -p "$f" || exit 1; done'

sec "Gráficos / video"
vainfo 2>/dev/null | grep -q 'iHD' && bien "VA-API driver Intel iHD" || falla "vainfo no muestra iHD"
grep -q VaapiOnNvidia ~/.config/brave-flags.conf 2>/dev/null && falla "brave-flags aún tiene NVIDIA" || bien "brave-flags sin NVIDIA"
grep -rqi nvidia ~/.config/hypr/config/environment.lua && grep -v '^\s*--' ~/.config/hypr/config/environment.lua | grep -qi nvidia \
  && falla "variables NVIDIA activas en Hyprland" || bien "sin variables NVIDIA"
check "mpv carga la config" bash -c 'timeout 20 mpv --vo=null --ao=null --keep-open=no --idle=no --frames=1 av://lavfi:testsrc=duration=1 2>&1 | grep -qiE "error parsing|unknown option" && exit 1 || exit 0'

sec "Energía / batería"
[[ $(cat /sys/class/power_supply/BAT0/charge_control_end_threshold) == 80 ]] && bien "batería limitada al 80%" || falla "umbral de batería no es 80"
check "power-profiles-daemon activo" systemctl is-active power-profiles-daemon
echo "    perfil actual: $(powerprofilesctl get 2>/dev/null)  |  batería: $(cat /sys/class/power_supply/BAT0/capacity)%"
pacman -Q thermald >/dev/null 2>&1 && aviso "thermald instalado (no sirve en esta ThinkPad)" || bien "sin thermald (firmware Lenovo DYTC)"

sec "Seguridad / bloqueo"
[[ -f /etc/pam.d/noctalia ]] && bien "PAM de la pantalla de bloqueo" || falla "falta /etc/pam.d/noctalia (¡te puedes quedar fuera!)"
if fprintd-list "$USER" 2>/dev/null | grep -q 'no fingers'; then aviso "sin huella registrada → fprintd-enroll"; else bien "huella registrada"; fi
check "firewall ufw activo" systemctl is-active ufw

sec "Voz y dictado"
id -nG | grep -qw input && bien "usuario en grupo input" || aviso "grupo input no activo aún (cierra sesión y entra)"
for s in ydotool piper-voz-daemon hyprwhspr; do check "servicio de usuario $s" systemctl --user is-active $s; done
check "edge-tts instalado" command -v edge-tts
check "piper sintetiza (voz Daniela)" bash -c 'echo prueba | piper -m ~/.local/share/piper-voices/es/es_AR/daniela/high/es_AR-daniela-high.onnx -f /tmp/.aud-piper.wav && test -s /tmp/.aud-piper.wav'
check "logid (mouse M720)" systemctl is-active logid

sec "Apps por defecto"
for m in image/png video/mp4 application/pdf text/html inode/directory text/markdown; do
  printf '    %-16s → %s\n' "$m" "$(xdg-mime query default $m)"
done

sec "Scripts de estudio (tests)"
S=~/.config/hypr/scripts; T=$(mktemp -d)
for t in auto-captura-tests.py cuadernillo-tests.py estudiar-tests.py practica-tests.py resumen-corto-tests.py tarjetas-panel-tests.py; do
  (cd "$T" && timeout 300 python3 "$S/$t" >"$T/$t.log" 2>&1) && bien "$t" || falla "$t (log: $T/$t.log)"
done
for t in cola-capturas-tests.sh playlist-a-apuntes-tests.sh; do
  (cd "$T" && timeout 300 bash "$S/$t" >"$T/$t.log" 2>&1) && bien "$t" || falla "$t (log: $T/$t.log)"
done

sec "Sistema"
f=$(systemctl --failed --no-legend | wc -l); [[ $f == 0 ]] && bien "sin servicios de sistema fallidos" || falla "$f servicios fallidos: $(systemctl --failed --no-legend | awk '{print $2}' | xargs)"
f=$(systemctl --user --failed --no-legend | wc -l); [[ $f == 0 ]] && bien "sin servicios de usuario fallidos" || falla "$f servicios de usuario fallidos: $(systemctl --user --failed --no-legend | awk '{print $2}' | xargs)"
echo "    snapshots btrfs: ver con  sudo snapper list  (o en el menú de arranque Limine)"
swapon --show | grep -q zram && bien "zram activo" || aviso "sin zram"
echo "    disco /: $(df -h / | awk 'NR==2{print $3" usados de "$2}')"

printf '\n\e[1mResultado:\e[0m %d ✔   %d ✘   %d !\n' $ok $mal $avisos
exit $(( mal > 0 ))
