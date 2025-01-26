#!/bin/bash

# Farben für die Ausgabe
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}V.O.L.L. - Update${NC}"
echo "====================>"

# Prüfe, ob wir auf einem Arch-Linux-System sind
if ! command -v pacman &> /dev/null; then
    echo "Dieses Skript ist nur für Arch Linux gedacht!"
    exit 1
fi

# Prüfe, ob V.O.L.L. installiert ist
if ! pacman -Qi voll &> /dev/null; then
    echo "V.O.L.L. ist nicht installiert!"
    echo "Bitte installieren Sie es zuerst mit:"
    echo "curl -s https://raw.githubusercontent.com/jinxblackzoo/V.O.L.L./main/install.sh | bash"
    exit 1
fi

# Temporäres Verzeichnis erstellen
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR" || exit 1

echo -e "${GREEN}✓${NC} Temporäres Verzeichnis erstellt"

# Repository klonen
git clone https://github.com/jinxblackzoo/V.O.L.L..git || exit 1
cd V.O.L.L. || exit 1

echo -e "${GREEN}✓${NC} Repository geklont"

# PKGBUILD verwenden
makepkg -si --noconfirm || exit 1

echo -e "${GREEN}✓${NC} V.O.L.L. aktualisiert"

# Aufräumen
cd ..
rm -rf "$TEMP_DIR"

echo -e "${GREEN}✓${NC} Update abgeschlossen"
echo ""
echo "V.O.L.L. wurde erfolgreich auf die neueste Version aktualisiert!"
