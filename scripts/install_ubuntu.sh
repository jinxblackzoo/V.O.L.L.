#!/bin/bash

echo "V.O.L.L. - Installation für Ubuntu"
echo "================================="

# Systemabhängigkeiten installieren
echo "1. Installiere benötigte Programme..."
sudo apt update
sudo apt install -y python3-gi python3-gi-cairo gir1.2-gtk-4.0 libadwaita-1-0 \
                    python3-sqlalchemy python3-reportlab python3-pip git

# Repository klonen
echo "2. Lade V.O.L.L. herunter..."
git clone https://github.com/jinxblackzoo/V.O.L.L.
cd V.O.L.L.

# Installation
echo "3. Installiere V.O.L.L..."
pip3 install --user .

# Desktop-Integration
echo "4. Erstelle Startmenü-Eintrag..."
mkdir -p ~/.local/share/applications ~/.local/share/icons/hicolor/scalable/apps
cp desktop/voll.desktop ~/.local/share/applications/
cp desktop/voll.svg ~/.local/share/icons/hicolor/scalable/apps/
gtk-update-icon-cache -f -t ~/.local/share/icons/hicolor/

# PATH anpassen
if ! grep -q "export PATH=\"\$HOME/.local/bin:\$PATH\"" ~/.bashrc; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    export PATH="$HOME/.local/bin:$PATH"
fi

echo ""
echo "Installation abgeschlossen! 🎉"
echo "Du findest V.O.L.L. jetzt im Startmenü."
echo "Viel Spaß beim Vokabeln lernen! 📚"
