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

Die Installation ist ganz einfach und funktioniert auf allen Linux-Systemen:

1. Öffne ein Terminal (meist mit Strg+Alt+T)

2. Lade V.O.L.L. herunter:
   ```bash
   git clone https://github.com/jinxblackzoo/V.O.L.L.
   cd V.O.L.L.
   ```

3. Starte die Installation:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

Das Installationsprogramm erkennt deine Linux-Version automatisch und installiert alle benötigten Programme. Folge einfach den Anweisungen auf dem Bildschirm.

Nach der Installation findest du V.O.L.L. im Startmenü oder kannst es mit dem Befehl `voll` im Terminal starten.

## Update

Um V.O.L.L. zu aktualisieren:

1. Gehe in das V.O.L.L.-Verzeichnis:
   ```bash
   cd V.O.L.L.
   ```

2. Hole die neueste Version:
   ```bash
   git pull
   ```

3. Installiere das Update:
   ```bash
   ./install.sh
   ```

## Deinstallation

1. Lösche die Programmdateien:
   ```bash
   rm -rf ~/.local/lib/python3/site-packages/voll
   rm ~/.local/bin/voll
   rm ~/.local/share/applications/voll.desktop
   rm ~/.local/share/icons/hicolor/scalable/apps/voll.svg
   ```

2. Optional: Lösche deine persönlichen Daten:
   ```bash
   rm -rf ~/.local/share/voll    # Vokabeldatenbank
   rm -rf ~/.config/voll         # Einstellungen
   ```

## Probleme?

### Programm startet nicht
1. **Fehlende Abhängigkeiten**: 
   Starte das Installationsskript erneut:
   ```bash
   ./install.sh
   ```

2. **Programm nicht im PATH**:
   - Öffne ein neues Terminal oder starte deinen Computer neu
   - Oder füge diese Zeile in deine `~/.bashrc` ein:
     ```bash
     export PATH="$HOME/.local/bin:$PATH"
     ```

3. **Fehlermeldungen anzeigen**:
   Starte das Programm im Terminal:
   ```bash
   voll
   ```

### Weitere Hilfe
Wenn du weitere Hilfe brauchst:
1. Öffne ein [Issue auf GitHub](https://github.com/jinxblackzoo/V.O.L.L./issues)
2. Beschreibe dein Problem
3. Füge die Fehlermeldung aus dem Terminal hinzu

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
