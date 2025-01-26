#!/bin/bash

# Farben für die Ausgabe
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}V.O.L.L. - Vokabeln Ohne Langeweile Lernen${NC}"
echo "====================>"

# Prüfe, ob wir auf einem Arch-Linux-System sind
if ! command -v pacman &> /dev/null; then
    echo "Dieses Skript ist nur für Arch Linux gedacht!"
    exit 1
fi

# Temporäres Verzeichnis erstellen
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR" || exit 1

echo -e "${GREEN}✓${NC} Temporäres Verzeichnis erstellt"

# Abhängigkeiten installieren
echo "Installing dependencies..."
sudo pacman -S --needed --noconfirm python-gobject gtk4 libadwaita python-sqlalchemy python-reportlab git base-devel || exit 1

echo -e "${GREEN}✓${NC} Abhängigkeiten installiert"

# Repository klonen
git clone https://github.com/jinxblackzoo/V.O.L.L..git || exit 1
cd V.O.L.L. || exit 1

echo -e "${GREEN}✓${NC} Repository geklont"

# PKGBUILD verwenden
makepkg -si --noconfirm || exit 1

echo -e "${GREEN}✓${NC} V.O.L.L. installiert"

# Aufräumen
cd ..
rm -rf "$TEMP_DIR"

echo -e "${GREEN}✓${NC} Installation abgeschlossen"
echo ""
echo "Sie können V.O.L.L. jetzt über das Anwendungsmenü starten"
echo "oder durch Eingabe von 'voll' in einem Terminal."
