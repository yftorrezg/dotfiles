#!/usr/bin/env bash
# Backup diario de /home/yafer al disco externo vía restic.
# restic se usa (en vez de rsync -aAX) porque el destino es exFAT: no soporta
# permisos Unix/symlinks/xattrs, y restic los guarda dentro de su propio
# formato de repositorio en vez de depender del filesystem destino.
#
# Laptop (oct-2026): el disco externo NO siempre está conectado. Si no está,
# el script anota una línea en el log y sale con 0 (sin unidad "failed", sin
# notificaciones): el timer lo vuelve a intentar al día siguiente.
# Dónde busca el disco, en orden:
#   1. /mnt/backups si está montado (entrada en /etc/fstab, como en la PC).
#   2. El disco por UUID donde sea que esté montado (p. ej. automontado por
#      udisks al enchufarlo desde el gestor de archivos).
#   3. Si está enchufado pero sin montar, lo monta con udisksctl (sin sudo).
set -euo pipefail

DISK_UUID="${BACKUP_DISK_UUID:-7FDC-A53B}"   # disco exFAT de 2 TB "backups"
REPO_SUBDIR="restic-home"
export RESTIC_PASSWORD_FILE="$HOME/.config/restic/home-backup.pass"
LOG="$HOME/.local/state/backup-home.log"
LOCK="${XDG_RUNTIME_DIR:-/tmp}/backup-home.lock"
mkdir -p "$(dirname "$LOG")"

log() { echo "$(date '+%Y-%m-%d %H:%M:%S') $*" >> "$LOG"; }

# Evita dos corridas a la vez (timer + manual): la segunda sale sin hacer nada.
exec 9>"$LOCK"
if ! flock -n 9; then
  log "otro backup ya está corriendo, se omite."
  exit 0
fi

find_mount() {
  if mountpoint -q /mnt/backups 2>/dev/null; then
    echo /mnt/backups; return 0
  fi
  local target
  target=$(findmnt -rn -S "UUID=$DISK_UUID" -o TARGET 2>/dev/null | head -n1 || true)
  if [ -n "$target" ]; then echo "$target"; return 0; fi
  if [ -e "/dev/disk/by-uuid/$DISK_UUID" ] && command -v udisksctl >/dev/null 2>&1; then
    udisksctl mount --no-user-interaction -b "/dev/disk/by-uuid/$DISK_UUID" >/dev/null 2>&1 || true
    target=$(findmnt -rn -S "UUID=$DISK_UUID" -o TARGET 2>/dev/null | head -n1 || true)
    if [ -n "$target" ]; then echo "$target"; return 0; fi
  fi
  return 1
}

if ! MNT=$(find_mount); then
  log "disco de backup (UUID $DISK_UUID) no conectado, se omite."
  exit 0
fi
export RESTIC_REPOSITORY="$MNT/$REPO_SUBDIR"

if [ ! -f "$RESTIC_PASSWORD_FILE" ]; then
  log "ERROR: falta $RESTIC_PASSWORD_FILE (contraseña del repo restic)."
  exit 1
fi
if [ ! -f "$RESTIC_REPOSITORY/config" ]; then
  log "ERROR: $RESTIC_REPOSITORY no es un repo restic (¿otro disco?)."
  exit 1
fi

{
  echo "=== $(date '+%Y-%m-%d %H:%M:%S') — inicio backup ($RESTIC_REPOSITORY) ==="

  # En la PC el backup falló semanas por un lock viejo nunca borrado.
  # `restic unlock` (sin --remove-all) solo borra locks de procesos muertos.
  restic unlock

  # --one-file-system: no entra a otros montajes dentro de $HOME (Google Drive
  # de rclone, discos externos, etc.). GoogleDrive además está en el excludes.
  restic backup "$HOME" \
    --one-file-system \
    --exclude-file="$HOME/.config/restic/home-excludes.txt" \
    --exclude-caches

  restic forget --keep-daily 7 --keep-weekly 4 --keep-monthly 6 --prune

  echo "=== $(date '+%Y-%m-%d %H:%M:%S') — fin backup ==="
} >> "$LOG" 2>&1
