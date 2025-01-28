#!/bin/bash

echo "V.O.L.L. - Installation"
echo "===================="
echo "Vokabeln Ohne Langeweile Lernen - Installations-Assistent"
echo

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

echo
echo " Installation abgeschlossen! "
echo
echo "Du findest V.O.L.L. jetzt im Startmenü oder kannst es mit 'voll' im Terminal starten."
echo "Falls das Programm nicht startet, öffne ein neues Terminal oder melde dich neu an."
echo
echo "Viel Spaß beim Vokabeln lernen! "
