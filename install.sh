#!/bin/bash

echo "V.O.L.L. - Installation"
echo "===================="
echo "Vokabeln Ohne Langeweile Lernen - Installations-Assistent"
echo

# Prüfe ob dies ein Update ist (V.O.L.L. bereits installiert)
DATA_DIR="$HOME/.local/share/voll"
CONFIG_DIR="$HOME/.config/voll"
IS_UPDATE=false

if [ -d "$DATA_DIR" ] || [ -d "$CONFIG_DIR" ]; then
    IS_UPDATE=true
    echo "🔄 Update-Modus erkannt - Bestehende V.O.L.L. Installation gefunden"
    echo
    
    # Automatisches Backup vor Update
    echo "📦 Erstelle automatisches Backup vor Update..."
    BACKUP_TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    BACKUP_DIR="$HOME/voll_backups/auto_backup_$BACKUP_TIMESTAMP"
    
    mkdir -p "$BACKUP_DIR"
    
    if [ -d "$DATA_DIR" ]; then
        cp -r "$DATA_DIR" "$BACKUP_DIR/data"
        echo "   ✅ Datenbanken gesichert"
    fi
    
    if [ -d "$CONFIG_DIR" ]; then
        cp -r "$CONFIG_DIR" "$BACKUP_DIR/config"
        echo "   ✅ Konfiguration gesichert"
    fi
    
    # Backup-Info erstellen
    cat > "$BACKUP_DIR/backup_info.txt" << EOF
V.O.L.L. Automatisches Update-Backup
===================================
Erstellt am: $(date)
Grund: Update-Installation
Backup-Verzeichnis: $BACKUP_DIR

Wiederherstellung bei Problemen:
./scripts/restore.sh $BACKUP_DIR
EOF
    
    echo "   📁 Backup erstellt: $BACKUP_DIR"
    echo
else
    echo "🆕 Neuinstallation erkannt"
    echo
fi

# Distributions-Erkennung
if [ -f /etc/os-release ]; then
    . /etc/os-release
    DISTRO=$ID
    echo "Linux-Distribution erkannt: $PRETTY_NAME"
else
    echo "Konnte die Linux-Distribution nicht erkennen."
    DISTRO="unknown"
fi

# Abhängigkeiten installieren
echo
echo "1. Installiere benötigte Programme..."
case $DISTRO in
    "ubuntu"|"debian"|"linuxmint")
        echo "Verwende apt für die Installation..."
        sudo apt update
        sudo apt install -y python3-gi python3-gi-cairo gir1.2-gtk-4.0 libadwaita-1-0 python3-sqlalchemy python3-reportlab
        ;;
    "arch"|"manjaro")
        echo "Verwende pacman für die Installation..."
        sudo pacman -S --needed python gtk4 libadwaita python-gobject python-sqlalchemy python-reportlab
        ;;
    "fedora")
        echo "Verwende dnf für die Installation..."
        sudo dnf install -y python3 gtk4 libadwaita python3-gobject python3-sqlalchemy python3-reportlab
        ;;
    *)
        echo " Distribution nicht erkannt. Bitte installiere diese Pakete manuell:"
        echo "- Python 3"
        echo "- GTK 4"
        echo "- libadwaita"
        echo "- Python GObject"
        echo "- SQLAlchemy"
        echo "- ReportLab"
        read -p "Drücke ENTER wenn du die Pakete installiert hast..."
        ;;
esac

# Programm installieren
echo
echo "2. Installiere V.O.L.L..."

# Verzeichnisse erstellen
echo "Erstelle Programm-Verzeichnisse..."
mkdir -p ~/.local/bin
PYTHON_SITE_PACKAGES=$(python3 -c "import site; print(site.USER_SITE)")
mkdir -p "$PYTHON_SITE_PACKAGES/voll"
mkdir -p ~/.local/share/applications
mkdir -p ~/.local/share/icons/hicolor/scalable/apps

# Bei Updates: Sichere Datenverzeichnisse vor Überschreibung
if [ "$IS_UPDATE" = true ]; then
    echo "🔒 Schütze bestehende Datenbanken vor Überschreibung..."
    
    # Temporäre Sicherung der Datenverzeichnisse
    TEMP_BACKUP="/tmp/voll_temp_$(date +%s)"
    mkdir -p "$TEMP_BACKUP"
    
    if [ -d "$DATA_DIR" ]; then
        cp -r "$DATA_DIR" "$TEMP_BACKUP/data"
    fi
    
    if [ -d "$CONFIG_DIR" ]; then
        cp -r "$CONFIG_DIR" "$TEMP_BACKUP/config"
    fi
fi

# Python-Dateien kopieren
echo "Kopiere Programm-Dateien..."
cp -r voll/* "$PYTHON_SITE_PACKAGES/voll/"

# Starter-Skript erstellen
echo "Erstelle Starter-Skript..."
cat > ~/.local/bin/voll << 'EOF'
#!/usr/bin/env python3
from voll.main import main
if __name__ == "__main__":
    main()
EOF
chmod +x ~/.local/bin/voll

# Desktop-Integration
echo "Erstelle Desktop-Integration..."
cp desktop/voll.desktop ~/.local/share/applications/
cp desktop/voll.svg ~/.local/share/icons/hicolor/scalable/apps/
gtk-update-icon-cache -f -t ~/.local/share/icons/hicolor/

# PATH-Variable prüfen und ggf. setzen
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    export PATH="$HOME/.local/bin:$PATH"
    echo "PATH-Variable wurde aktualisiert."
fi

# Bei Updates: Stelle Datenverzeichnisse wieder her
if [ "$IS_UPDATE" = true ] && [ -d "$TEMP_BACKUP" ]; then
    echo "🔄 Stelle bestehende Datenbanken wieder her..."
    
    # Stelle Daten wieder her (überschreibt keine neuen Strukturen)
    if [ -d "$TEMP_BACKUP/data" ]; then
        # Erstelle Datenverzeichnis falls es nicht existiert
        mkdir -p "$DATA_DIR"
        
        # Kopiere nur bestehende Datenbanken zurück, überschreibe keine neuen
        cp -r "$TEMP_BACKUP/data"/* "$DATA_DIR/" 2>/dev/null || true
        echo "   ✅ Datenbanken wiederhergestellt"
    fi
    
    if [ -d "$TEMP_BACKUP/config" ]; then
        # Erstelle Konfigurationsverzeichnis falls es nicht existiert
        mkdir -p "$CONFIG_DIR"
        
        # Kopiere Konfiguration zurück
        cp -r "$TEMP_BACKUP/config"/* "$CONFIG_DIR/" 2>/dev/null || true
        echo "   ✅ Konfiguration wiederhergestellt"
    fi
    
    # Temporäres Backup löschen
    rm -rf "$TEMP_BACKUP"
    echo "   🧹 Temporäre Dateien bereinigt"
    echo
fi

echo
echo "✅ Installation abgeschlossen!"
echo

if [ "$IS_UPDATE" = true ]; then
    echo "🔄 Update erfolgreich! Deine Vokabeln und Einstellungen wurden beibehalten."
    echo "📁 Backup verfügbar unter: $BACKUP_DIR"
    echo
    echo "Bei Problemen kannst du das Backup wiederherstellen:"
    echo "   ./scripts/restore.sh $BACKUP_DIR"
else
    echo "🆕 Neuinstallation abgeschlossen!"
fi

echo
echo "Du findest V.O.L.L. jetzt im Startmenü oder kannst es mit 'voll' im Terminal starten."
echo "Falls das Programm nicht startet, öffne ein neues Terminal oder melde dich neu an."
echo
echo "Viel Spaß beim Vokabeln lernen! 📚"
