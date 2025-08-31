#!/bin/bash

# V.O.L.L. Backup Script
# Erstellt ein vollständiges Backup aller Benutzerdaten
# Copyright (C) 2025 jinx@blackzoo.de

set -e  # Beende bei Fehlern

echo "V.O.L.L. Backup-Tool"
echo "==================="
echo

# Zeitstempel für eindeutige Backup-Namen
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_BASE_DIR="$HOME/voll_backups"
BACKUP_DIR="$BACKUP_BASE_DIR/backup_$TIMESTAMP"

# Quellverzeichnisse
DATA_DIR="$HOME/.local/share/voll"
CONFIG_DIR="$HOME/.config/voll"

echo "Erstelle Backup-Verzeichnis: $BACKUP_DIR"
mkdir -p "$BACKUP_DIR"

# Prüfe ob Daten vorhanden sind
if [ ! -d "$DATA_DIR" ] && [ ! -d "$CONFIG_DIR" ]; then
    echo "❌ Keine V.O.L.L. Daten gefunden!"
    echo "   Weder $DATA_DIR noch $CONFIG_DIR existieren."
    exit 1
fi

# Backup der Datenbanken und Exports
if [ -d "$DATA_DIR" ]; then
    echo "📦 Sichere Datenbanken und Exports..."
    cp -r "$DATA_DIR" "$BACKUP_DIR/data"
    echo "   ✅ Datenbanken gesichert"
else
    echo "⚠️  Keine Datenbanken gefunden in $DATA_DIR"
fi

# Backup der Konfiguration
if [ -d "$CONFIG_DIR" ]; then
    echo "⚙️  Sichere Konfiguration..."
    cp -r "$CONFIG_DIR" "$BACKUP_DIR/config"
    echo "   ✅ Konfiguration gesichert"
else
    echo "⚠️  Keine Konfiguration gefunden in $CONFIG_DIR"
fi

# Backup-Info erstellen
cat > "$BACKUP_DIR/backup_info.txt" << EOF
V.O.L.L. Backup Information
==========================
Erstellt am: $(date)
Backup-Verzeichnis: $BACKUP_DIR

Gesicherte Verzeichnisse:
- Datenbanken: $DATA_DIR
- Konfiguration: $CONFIG_DIR

Wiederherstellung:
./scripts/restore.sh $BACKUP_DIR
EOF

echo
echo "✅ Backup erfolgreich erstellt!"
echo "📁 Backup-Pfad: $BACKUP_DIR"
echo
echo "Wiederherstellung mit:"
echo "   ./scripts/restore.sh $BACKUP_DIR"
echo

# Zeige Backup-Größe
BACKUP_SIZE=$(du -sh "$BACKUP_DIR" | cut -f1)
echo "📊 Backup-Größe: $BACKUP_SIZE"

# Alte Backups auflisten (optional)
echo
echo "Vorhandene Backups:"
ls -la "$BACKUP_BASE_DIR" 2>/dev/null | grep "backup_" || echo "   Keine älteren Backups gefunden"
