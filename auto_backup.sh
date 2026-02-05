#!/bin/bash
# Auto-backup helper for the PaperMC server directory.
# Usage: ./auto_backup.sh [interval_minutes]
# Default interval is 60 minutes. Script must keep running (e.g., in screen/tmux).

set -euo pipefail

DEFAULT_INTERVAL_MINUTES=60
INTERVAL_MINUTES="${1:-$DEFAULT_INTERVAL_MINUTES}"

if ! [[ "$INTERVAL_MINUTES" =~ ^[0-9]+$ ]] || [ "$INTERVAL_MINUTES" -le 0 ]; then
  echo "Usage: $0 [interval_minutes>0]" >&2
  exit 1
fi

INTERVAL_SECONDS=$((INTERVAL_MINUTES * 60))
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKUP_SCRIPT="$SCRIPT_DIR/backup.sh"

if [ ! -x "$BACKUP_SCRIPT" ]; then
  echo "Error: backup.sh not found or not executable at $BACKUP_SCRIPT" >&2
  exit 1
fi

log() {
  printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$1"
}

log "Auto-backup running every $INTERVAL_MINUTES minute(s). Press Ctrl+C to stop."

while true; do
  log "Starting backup run"
  if "$BACKUP_SCRIPT"; then
    log "Backup finished successfully"
  else
    log "Backup script exited with an error" >&2
  fi
  sleep "$INTERVAL_SECONDS"
done
