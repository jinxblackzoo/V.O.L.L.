#!/bin/bash

echo "V.O.L.L. - Update"
echo "================"

echo "1. Lade neue Version herunter..."
git pull

echo "2. Installiere Update..."
pip3 install --user .

echo "3. Aktualisiere Icons..."
gtk-update-icon-cache -f -t ~/.local/share/icons/hicolor/

echo ""
echo "Update abgeschlossen! 🎉"
echo "Viel Spaß beim Vokabeln lernen! 📚"
