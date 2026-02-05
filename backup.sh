#!/bin/bash

BACKUP_DIR="$HOME/Documents/Server Minecraft/backups"
DATE=$(date +%Y-%m-%d_%H-%M-%S)
SERVER_DIR="$HOME/Documents/Server Minecraft"

mkdir -p "$BACKUP_DIR"

tar -czf "$BACKUP_DIR/backup_$DATE.tar.gz" \
    -C "$SERVER_DIR" \
    world world_nether world_the_end plugins server.properties

echo "Backup created: backup_$DATE.tar.gz"

cd "$BACKUP_DIR"
ls -t backup_*.tar.gz | tail -n +8 | xargs rm -f 2>/dev/null || true
