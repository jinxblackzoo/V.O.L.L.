# V.O.L.L. - Vokabeln Ohne Langeweile Lernen

Ein kinderfreundlicher Vokabeltrainer mit moderner GTK4-Oberfläche, der das Lernen von Vokabeln spannend und unterhaltsam macht.

## Autor
jinx@blackzoo.de

## Entwicklung
Dieses Projekt wurde mit Unterstützung von Künstlicher Intelligenz (Codeium Cascade) entwickelt.

## Lizenz
Dieses Projekt steht unter der [GNU General Public License v3 (GPLv3)](LICENSE).
Copyright (C) 2025 jinx@blackzoo.de

## Features

- Mehrsprachige Vokabeldatenbanken
- Einfache und intuitive Benutzeroberfläche
- Intelligentes Lernsystem
- Fortschrittsüberwachung und PDF-Reports
- Exportfunktion für Vokabeln

## Dateispeicherorte

Das Programm speichert Daten an folgenden Orten:

### Persönliche Daten
- `~/.local/share/voll/databases/`: Vokabeldatenbanken
- `~/.local/share/voll/exports/`: Exportierte PDF-Dateien und CSV-Listen
- `~/.local/share/voll/reports/`: Lernfortschritte und Statistiken

### Konfiguration
- `~/.config/voll/settings.ini`: Programmeinstellungen
- `~/.config/voll/themes/`: Benutzerdefinierte Themes (optional)

Die Datenbanken können einfach gesichert werden, indem der komplette `~/.local/share/voll` Ordner kopiert wird.

## Installation

### Arch Linux
```bash
# System-Abhängigkeiten installieren
sudo pacman -S python gtk4 libadwaita python-gobject python-sqlalchemy python-reportlab git

# Repository klonen
git clone https://github.com/jinxblackzoo/V.O.L.L.
cd V.O.L.L.

# Paket erstellen und installieren
makepkg -si
```

### Ubuntu
Öffne ein Terminal (Strg+Alt+T) und kopiere diese Befehle:

```bash
# Alles in einem Schritt installieren
wget -O install.sh https://raw.githubusercontent.com/jinxblackzoo/V.O.L.L./main/scripts/install_ubuntu.sh
chmod +x install.sh
./install.sh
```

Das Programm ist jetzt installiert! Du findest es im Startmenü unter "V.O.L.L."

### Update auf die neueste Version

#### Arch Linux
```bash
cd V.O.L.L.
git pull
makepkg -si
```

#### Ubuntu
Öffne ein Terminal und führe aus:
```bash
cd V.O.L.L.
./update.sh
```

### Deinstallation

#### Arch Linux
```bash
# Deinstalliert nur das Programm, behält persönliche Datenbanken
sudo pacman -R voll

# Deinstalliert das Programm und ALLE Daten (Vokabeldatenbanken, Einstellungen, etc.)
sudo pacman -R voll
rm -rf ~/.local/share/voll       # Persönliche Datenbanken
rm -rf ~/.config/voll           # Programmeinstellungen
```

#### Ubuntu
```bash
# Deinstalliert nur das Programm, behält persönliche Datenbanken
pip uninstall voll
rm ~/.local/share/applications/voll.desktop
rm ~/.local/share/icons/hicolor/scalable/apps/voll.svg

# Deinstalliert das Programm und ALLE Daten (Vokabeldatenbanken, Einstellungen, etc.)
pip uninstall voll
rm ~/.local/share/applications/voll.desktop
rm ~/.local/share/icons/hicolor/scalable/apps/voll.svg
rm -rf ~/.local/share/voll       # Persönliche Datenbanken
rm -rf ~/.config/voll           # Programmeinstellungen
```

## Erste Schritte

1. Starten Sie den Vokabeltrainer:
   ```bash
   voll
   ```

2. Klicken Sie auf "Neue Datenbank hinzufügen" und wählen Sie die gewünschte Sprache

3. Fügen Sie Ihre ersten Vokabeln hinzu

## Daten

- Vokabeln werden in `~/.local/share/vokabeltrainer` gespeichert
- Einstellungen befinden sich in `~/.config/vokabeltrainer`

## Entwicklung

Möchten Sie zum Projekt beitragen? Hier sind die Schritte:

1. Repository klonen
2. Virtuelle Umgebung erstellen:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -e .
   ```
3. Änderungen vornehmen
4. Pull Request erstellen
