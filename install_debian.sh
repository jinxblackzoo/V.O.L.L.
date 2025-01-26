#!/bin/bash

# Farben für die Ausgabe
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}V.O.L.L. - Vokabeln Ohne Langeweile Lernen${NC}"
echo "====================>"

# Prüfe, ob wir auf einem Debian/Ubuntu System sind
if ! command -v apt-get &> /dev/null; then
    echo "Dieses Skript ist nur für Debian/Ubuntu gedacht!"
    exit 1
fi

# Temporäres Verzeichnis erstellen
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR" || exit 1

echo -e "${GREEN}✓${NC} Temporäres Verzeichnis erstellt"

# System-Abhängigkeiten installieren
echo "Installing dependencies..."
sudo apt-get update
sudo apt-get install -y \
    python3-gi \
    python3-gi-cairo \
    gir1.2-gtk-4.0 \
    libadwaita-1-0 \
    python3-sqlalchemy \
    python3-reportlab \
    python3-pip \
    git \
    || exit 1

echo -e "${GREEN}✓${NC} Abhängigkeiten installiert"

# Repository klonen
git clone https://github.com/jinxblackzoo/V.O.L.L..git || exit 1
cd V.O.L.L. || exit 1

echo -e "${GREEN}✓${NC} Repository geklont"

# Installation mit pip
pip3 install --user . || exit 1

# Desktop-Integration
mkdir -p ~/.local/share/applications
cp desktop/voll.desktop ~/.local/share/applications/
mkdir -p ~/.local/share/icons/hicolor/scalable/apps
cp desktop/voll.svg ~/.local/share/icons/hicolor/scalable/apps/

echo -e "${GREEN}✓${NC} V.O.L.L. installiert"

# Aufräumen
cd ..
rm -rf "$TEMP_DIR"

echo -e "${GREEN}✓${NC} Installation abgeschlossen"
echo ""
echo "Sie können V.O.L.L. jetzt über das Anwendungsmenü starten"
echo "oder durch Eingabe von 'voll' in einem Terminal."
