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
# Quellcode herunterladen
curl -L -o v.o.l.l.zip https://github.com/jinxblackzoo/V.O.L.L/archive/refs/tags/v1.0.0.zip
unzip v.o.l.l.zip
cd V.O.L.L-1.0.0

# Paket erstellen und installieren
makepkg -si
```

### Debian/Ubuntu
```bash
# System-Abhängigkeiten installieren
sudo apt update
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 libadwaita-1-0 python3-sqlalchemy python3-reportlab

# Quellcode herunterladen und installieren
curl -L -o v.o.l.l.zip https://github.com/jinxblackzoo/V.O.L.L/archive/refs/tags/v1.0.0.zip
unzip v.o.l.l.zip
cd V.O.L.L-1.0.0
pip install .

# Desktop-Integration
mkdir -p ~/.local/share/applications ~/.local/share/icons/hicolor/scalable/apps
cp desktop/voll.desktop ~/.local/share/applications/
cp desktop/voll.svg ~/.local/share/icons/hicolor/scalable/apps/
```

### Update auf die neueste Version

#### Arch Linux
```bash
cd V.O.L.L-1.0.0
curl -L -o v.o.l.l.zip https://github.com/jinxblackzoo/V.O.L.L/archive/refs/tags/v1.0.0.zip
unzip -o v.o.l.l.zip --strip-components=1
makepkg -si
```

#### Debian/Ubuntu
```bash
cd V.O.L.L-1.0.0
curl -L -o v.o.l.l.zip https://github.com/jinxblackzoo/V.O.L.L/archive/refs/tags/v1.0.0.zip
unzip -o v.o.l.l.zip --strip-components=1
pip install .
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

#### Debian/Ubuntu
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
