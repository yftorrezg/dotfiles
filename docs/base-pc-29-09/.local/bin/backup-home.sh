#!/usr/bin/env bash
# Backup diario de /home/yafer al disco externo (/mnt/backups) vía restic.
# restic se usa (en vez de rsync -aAX) porque el destino es exFAT: no soporta
# permisos Unix/symlinks/xattrs, y restic los guarda dentro de su propio
# formato de repositorio en vez de depender del filesystem destino.
set -euo pipefail

export RESTIC_REPOSITORY=/mnt/backups/restic-home
export RESTIC_PASSWORD_FILE="$HOME/.config/restic/home-backup.pass"
LOG="$HOME/.local/state/backup-home.log"
mkdir -p "$(dirname "$LOG")"

{
  echo "=== $(date '+%Y-%m-%d %H:%M:%S') — inicio backup ==="

  if ! mountpoint -q /mnt/backups; then
    echo "ERROR: /mnt/backups no está montado, se aborta este backup."
    exit 1
  fi

  restic backup "$HOME" \
    --exclude-file="$HOME/.config/restic/home-excludes.txt" \
    --exclude-caches

  restic forget --keep-daily 7 --keep-weekly 4 --keep-monthly 6 --prune

  echo "=== $(date '+%Y-%m-%d %H:%M:%S') — fin backup ==="
} >> "$LOG" 2>&1
