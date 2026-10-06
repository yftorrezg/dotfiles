#!/usr/bin/env bash
# =============================================================================
# 04 — Voz (SUPER+R lectura, dictado hyprwhspr), servicios de usuario,
#      backup restic y mouse M720 (logid) en la ThinkPad E14 Gen4.
#
# Uso (en este orden):
#   bash ~/migracion-laptop/04-voz-servicios.sh sistema   # pide sudo
#   -> CERRAR SESIÓN y volver a entrar (grupos input/audio)
#   -> copiar los dotfiles de staging/ a ~ (si no se hizo ya)
#   bash ~/migracion-laptop/04-voz-servicios.sh usuario   # SIN sudo
#   bash ~/migracion-laptop/04-voz-servicios.sh probar    # comprobaciones
#
# Opcionales, cuando quieras (sin sudo):
#   bash ~/migracion-laptop/04-voz-servicios.sh drive     # Google Drive (rclone)
#   bash ~/migracion-laptop/04-voz-servicios.sh backup    # backup diario restic
#
# Ya hecho por Claude el 05-10-2026 (no hace falta repetir, la parte "usuario"
# lo verifica y lo rehace solo si falta):
#   pipx install piper-tts   (1.8.0, trae espeak-ng adentro; el AUR no compila)
#   pipx install edge-tts    (7.2.8)
#   voces es_AR-daniela-high y es_MX-claude-high en ~/.local/share/piper-voices/
#   (sha256 verificado contra Hugging Face rhasspy/piper-voices)
# =============================================================================
set -uo pipefail

STAGING_SYS="$HOME/migracion-laptop/staging-system/etc"
VOICES_DIR="$HOME/.local/share/piper-voices"
HF="https://huggingface.co/rhasspy/piper-voices/resolve/main"

paso() { echo; echo "==> $*"; }

# -----------------------------------------------------------------------------
# PARTE 1 — SISTEMA (necesita sudo)
# -----------------------------------------------------------------------------
parte_sistema() {
    paso "Grupos: input (ydotool, hyprwhspr leen/escriben /dev/input y /dev/uinput) y audio"
    # hyprwhspr también sugiere 'tty'; en la PC no se usaba (el aviso de 'status' es normal).
    sudo usermod -aG input,audio "$USER"

    paso "Permisos de /dev/uinput"
    # El paquete ydotool trae /usr/lib/udev/rules.d/80-uinput.rules (grupo input, 0660),
    # pero se instaló con el sistema ya arrancado: hoy /dev/uinput sigue root:root 0600.
    # En el kernel de CachyOS uinput viene integrado (no hace falta modules-load.d).
    # Reaplicar la regla ahora (también se arregla solo al reiniciar):
    sudo udevadm control --reload
    sudo udevadm trigger --action=add --name-match=uinput 2>/dev/null \
        || sudo udevadm trigger --action=add --subsystem-match=misc
    ls -l /dev/uinput    # debe decir: crw-rw---- root input

    paso "Mouse M720: logid (logiops) + regla udev que lo reinicia al reconectar"
    sudo install -Dm644 "$STAGING_SYS/logid.cfg" /etc/logid.cfg
    sudo install -Dm644 "$STAGING_SYS/udev/rules.d/99-logid-m720.rules" /etc/udev/rules.d/99-logid-m720.rules
    sudo udevadm control --reload
    sudo systemctl enable --now logid.service
    # Emparejar el M720 por Bluetooth (en un canal libre del mouse, botón Easy-Switch):
    #   bluetoothctl → scan on → pair <MAC> → trust <MAC> → connect <MAC>
    # Ver: journalctl -u logid -f   →  "Device found: M720 Triathlon ..."
    # NO correr solaar a la vez que logid (pelean por el desvío de botones).

    # (Opcional) Disco de backup en /mnt/backups como en la PC. No es obligatorio:
    # backup-home.sh también encuentra el disco por UUID si lo monta udisks al enchufarlo.
    # Si lo querés en fstab, 'nofail' evita que el arranque se trabe sin el disco:
    #   sudo mkdir -p /mnt/backups
    #   echo 'UUID=7FDC-A53B /mnt/backups exfat nofail,x-systemd.device-timeout=5s,uid=1000,gid=1000,umask=022 0 0' | sudo tee -a /etc/fstab
    #   sudo systemctl daemon-reload

    echo
    echo "Listo la parte de sistema. CERRÁ SESIÓN y volvé a entrar para que tomen los grupos."
}

# -----------------------------------------------------------------------------
# PARTE 2 — USUARIO (sin sudo; después de re-login y de copiar los dotfiles)
# -----------------------------------------------------------------------------
bajar_voz() {   # $1 = subruta sin extensión, $2 = sha256 del .onnx
    local rel="$1" sha="$2" f="$VOICES_DIR/$1.onnx"
    if [ -f "$f" ] && echo "$sha  $f" | sha256sum -c --quiet 2>/dev/null; then
        echo "   ok: $rel"
        return
    fi
    mkdir -p "$(dirname "$f")"
    curl -fL --retry 3 -o "$f" "$HF/$rel.onnx"
    curl -fL --retry 3 -o "$f.json" "$HF/$rel.onnx.json"
    echo "$sha  $f" | sha256sum -c
}

parte_usuario() {
    export PATH="$HOME/.local/bin:$PATH"

    for f in ~/.config/hypr/scripts/leer-seleccion.sh ~/.config/hyprwhspr/config.json \
             ~/.config/systemd/user/piper-voz-daemon.service; do
        [ -e "$f" ] || { echo "Falta $f: copiá primero los dotfiles de staging/ a ~"; exit 1; }
    done
    id -nG | grep -qw input || echo "AVISO: todavía no estás en el grupo 'input' (¿cerraste sesión?)"

    paso "Piper (lectura offline) y edge-tts (online) con pipx"
    command -v piper >/dev/null 2>&1 && [ -x ~/.local/share/pipx/venvs/piper-tts/bin/python ] \
        || pipx install piper-tts
    command -v edge-tts >/dev/null 2>&1 || pipx install edge-tts

    paso "Voces Piper en $VOICES_DIR"
    bajar_voz es/es_AR/daniela/high/es_AR-daniela-high 7ceb1fc0dab349418c5b54a639ae9ee595212d7c9ea422220d8419163d5cc985
    bajar_voz es/es_MX/claude/high/es_MX-claude-high   3ef40a71ea63852cd8ab7e6fa7d2ecdcfa67a0b47c9c48e3f10e02ee02083ea0

    paso "Dictado hyprwhspr: backend CPU (whisper.cpp) + modelo small"
    # 'setup auto' crea el venv ~/.local/share/hyprwhspr/venv, compila pywhispercpp, baja el
    # modelo (466 MB) y el VAD, instala el plugin de Noctalia y la unit de systemd.
    # Puede pedir sudo para permisos (grupos/regla uinput): ya se hizo en la parte 'sistema'.
    cp -a ~/.config/hyprwhspr/config.json ~/.config/hyprwhspr/config.json.antes-setup
    hyprwhspr setup auto --backend cpu --model small
    # OJO: 'setup auto' cambia recording_mode "toggle" → "auto" (porque toggle es el default).
    # Se restaura la config de la migración (toggle, atajos SUPER+ALT+Z/X, etc.):
    python3 - <<'EOF'
import json, os
p = os.path.expanduser("~/.config/hyprwhspr/config.json")
b = os.path.expanduser("~/.config/hyprwhspr/config.json.antes-setup")
cfg = json.load(open(p)); mig = json.load(open(b))
cfg.update(mig)                      # lo de la migración manda
cfg.pop("audio_device_name", None)   # sigue al micrófono por defecto de PipeWire
cfg["transcription_backend"] = "pywhispercpp"
json.dump(cfg, open(p, "w"), indent=2, ensure_ascii=False)
print("config.json restaurada:", {k: cfg.get(k) for k in ("model", "recording_mode", "primary_shortcut", "secondary_shortcut")})
EOF

    paso "Servicios de usuario"
    systemctl --user daemon-reload
    # ydotool: servicio de USUARIO que trae el paquete (/usr/lib/systemd/user/ydotool.service),
    # igual que en la PC. Socket: /run/user/$UID/.ydotool_socket (lo usa leer-seleccion.sh).
    systemctl --user enable --now ydotool.service
    systemctl --user enable --now piper-voz-daemon.service   # Piper con la voz en memoria (SUPER+R)
    systemctl --user enable --now hyprwhspr.service          # dictado SUPER+ALT+Z / SUPER+ALT+X
    # NO se habilitan acá (ver 'drive' y 'backup'): rclone-gdrive, backup-home.timer.
    # NO van a la laptop: teclas-fantasma (diagnóstico de la PC), xremap (config vacía).
}

# -----------------------------------------------------------------------------
# OPCIONAL — Google Drive con rclone (sin sudo; interactivo)
# -----------------------------------------------------------------------------
parte_drive() {
    if [ ! -f ~/.config/rclone/rclone.conf ] || ! rclone listremotes | grep -qx 'gdrive:'; then
        echo "Configurar el remote 'gdrive' (tus client_id/secret propios de Google Cloud):"
        echo "  n → nombre: gdrive → storage: drive → client_id/secret → scope: 1 (drive)"
        echo "  → sin service account → auto config: y (abre Brave) → shared drive: n"
        rclone config
    fi
    # Para abrir Google Docs en Brave (como en la PC):
    grep -q '^export_formats' ~/.config/rclone/rclone.conf \
        || sed -i '/^\[gdrive\]/a export_formats = link.html' ~/.config/rclone/rclone.conf
    mkdir -p ~/GoogleDrive
    systemctl --user daemon-reload
    systemctl --user enable --now rclone-gdrive.service   # caché bajada a 10G para el SSD de la laptop
    sleep 3; ls ~/GoogleDrive | head
}

# -----------------------------------------------------------------------------
# OPCIONAL — Backup diario restic al disco externo (sin sudo)
# -----------------------------------------------------------------------------
parte_backup() {
    # La contraseña del repo NO viene en la migración: copiala de la PC o de tu gestor.
    if [ ! -f ~/.config/restic/home-backup.pass ]; then
        echo "Falta ~/.config/restic/home-backup.pass (contraseña del repo restic de la PC)."
        echo "Crealo con:  install -Dm600 /dev/stdin ~/.config/restic/home-backup.pass  (pegar, Enter, Ctrl+D)"
        exit 1
    fi
    # El script: si el disco (UUID 7FDC-A53B) no está, anota "se omite" en
    # ~/.local/state/backup-home.log y sale OK (sin unidades failed ni avisos).
    # Si está enchufado pero sin montar, lo monta con udisksctl. Hace 'restic unlock'
    # (locks viejos), usa --one-file-system y excluye ~/GoogleDrive.
    # El .service solo corre enchufado a corriente (ConditionACPower) y con prioridad baja.
    systemctl --user daemon-reload
    systemctl --user enable --now backup-home.timer
    systemctl --user list-timers backup-home.timer
    # Probar ya (con el disco enchufado):  systemctl --user start backup-home.service; tail ~/.local/state/backup-home.log
}

# -----------------------------------------------------------------------------
# PRUEBAS
# -----------------------------------------------------------------------------
parte_probar() {
    export PATH="$HOME/.local/bin:$PATH"
    local v="$VOICES_DIR/es/es_AR/daniela/high/es_AR-daniela-high.onnx"
    paso "Estado de servicios"
    systemctl --user is-active ydotool piper-voz-daemon hyprwhspr
    ls -l /dev/uinput "/run/user/$(id -u)/.ydotool_socket" ~/.cache/piper-voz.sock
    paso "Piper directo (genera WAV, no reproduce)"
    echo "Hola, esto es una prueba" | piper -m "$v" -f /tmp/prueba-piper.wav && file /tmp/prueba-piper.wav
    paso "Piper vía daemon (reproduce bajito)"
    echo "Prueba del daemon" | python3 ~/.config/hypr/scripts/piper-client.py "$v" 0.83 \
        | pw-play --volume=0.3 --rate=22050 --format=s16 --channels=1 --raw -
    paso "Micrófono por defecto (el interno, o el Maono si está enchufado y elegido)"
    pactl get-default-source
    paso "hyprwhspr"
    hyprwhspr status
    journalctl --user -u hyprwhspr -n 20 --no-pager | grep -E 'READY|BACKEND|device' || true
    echo
    echo "A mano: seleccionar texto en Brave / VSCode (Markdown Preview) / kitty y SUPER+R;"
    echo "SUPER+ALT+R abre el selector de voz; SUPER+ALT+Z dicta en español, SUPER+ALT+X en inglés."
}

case "${1:-}" in
    sistema) parte_sistema ;;
    usuario) parte_usuario ;;
    drive)   parte_drive ;;
    backup)  parte_backup ;;
    probar)  parte_probar ;;
    *) sed -n '2,24p' "$0"; exit 1 ;;
esac
