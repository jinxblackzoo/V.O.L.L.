#!/bin/bash

# V.O.L.L. Restore Script
# Stellt ein Backup der Benutzerdaten wieder her
# Copyright (C) 2025 jinx@blackzoo.de

set -e  # Beende bei Fehlern

echo "V.O.L.L. Restore-Tool"
echo "===================="
echo

# Parameter prüfen
if [ $# -ne 1 ]; then
    echo "❌ Fehler: Backup-Verzeichnis als Parameter angeben!"
    echo "Verwendung: $0 <backup-verzeichnis>"
    echo
    echo "Beispiel: $0 ~/voll_backups/backup_20250831_213000"
    exit 1
fi

BACKUP_DIR="$1"

# Prüfe ob Backup-Verzeichnis existiert
if [ ! -d "$BACKUP_DIR" ]; then
    echo "❌ Backup-Verzeichnis nicht gefunden: $BACKUP_DIR"
    exit 1
fi

# Prüfe Backup-Struktur
if [ ! -d "$BACKUP_DIR/data" ] && [ ! -d "$BACKUP_DIR/config" ]; then
    echo "❌ Ungültiges Backup! Weder data/ noch config/ Verzeichnis gefunden."
    exit 1
fi

echo "📁 Backup-Verzeichnis: $BACKUP_DIR"

# Zielverzeichnisse
DATA_DIR="$HOME/.local/share/voll"
CONFIG_DIR="$HOME/.config/voll"

# Sicherheitsabfrage
echo
echo "⚠️  WARNUNG: Diese Aktion überschreibt alle aktuellen V.O.L.L. Daten!"
echo "   Aktuelle Datenbanken in: $DATA_DIR"
echo "   Aktuelle Konfiguration in: $CONFIG_DIR"
echo
read -p "Möchtest du fortfahren? (ja/nein): " CONFIRM

if [ "$CONFIRM" != "ja" ]; then
    echo "❌ Wiederherstellung abgebrochen."
    exit 0
fi

# Erstelle Backup der aktuellen Daten (falls vorhanden)
if [ -d "$DATA_DIR" ] || [ -d "$CONFIG_DIR" ]; then
    CURRENT_BACKUP="$HOME/voll_backups/current_backup_$(date +%Y%m%d_%H%M%S)"
    echo "💾 Erstelle Backup der aktuellen Daten: $CURRENT_BACKUP"
    mkdir -p "$CURRENT_BACKUP"
    
    [ -d "$DATA_DIR" ] && cp -r "$DATA_DIR" "$CURRENT_BACKUP/data"
    [ -d "$CONFIG_DIR" ] && cp -r "$CONFIG_DIR" "$CURRENT_BACKUP/config"
    
    echo "   ✅ Aktueller Zustand gesichert"
fi

# Wiederherstellung durchführen
echo
echo "🔄 Stelle Backup wieder her..."

# Datenbanken wiederherstellen
if [ -d "$BACKUP_DIR/data" ]; then
    echo "📦 Stelle Datenbanken wieder her..."
    rm -rf "$DATA_DIR" 2>/dev/null || true
    cp -r "$BACKUP_DIR/data" "$DATA_DIR"
    echo "   ✅ Datenbanken wiederhergestellt"
else
    echo "⚠️  Keine Datenbanken im Backup gefunden"
fi

# Konfiguration wiederherstellen
if [ -d "$BACKUP_DIR/config" ]; then
    echo "⚙️  Stelle Konfiguration wieder her..."
    rm -rf "$CONFIG_DIR" 2>/dev/null || true
    cp -r "$BACKUP_DIR/config" "$CONFIG_DIR"
    echo "   ✅ Konfiguration wiederhergestellt"
else
    echo "⚠️  Keine Konfiguration im Backup gefunden"
fi

echo
echo "✅ Wiederherstellung erfolgreich abgeschlossen!"
echo
echo "Du kannst V.O.L.L. jetzt normal verwenden:"
echo "   voll"
echo
