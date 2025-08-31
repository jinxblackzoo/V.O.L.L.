# V.O.L.L. - Vokabeln Ohne Langeweile Lernen

Ein kinderfreundlicher Vokabeltrainer mit moderner GTK4-Oberfläche, der das Lernen von Vokabeln spannend und unterhaltsam macht.

## Autor
jinx@blackzoo.de

## Entwicklung
Dieses Projekt wurde mit Unterstützung von Künstlicher Intelligenz (Codeium Cascade) entwickelt.

## Lizenz
Dieses Projekt steht unter der [GNU General Public License v3 (GPLv3)](LICENSE).
Copyright (C) 2025 jinx@blackzoo.de <https://github.com/jinxblackzoo/V.O.L.L/>

## Features

- **Mehrsprachige Vokabeldatenbanken** - Erstelle separate Datenbanken für verschiedene Sprachen
- **Einfache und intuitive Benutzeroberfläche** - Moderne GTK4-Oberfläche mit libadwaita
- **Intelligentes 4-Level-Lernsystem** - Adaptive Wiederholung basierend auf Lernfortschritt
- **Fortschrittsüberwachung und PDF-Reports** - Detaillierte Statistiken und exportierbare Berichte
- **Sichere Datenverwaltung** - Backup, Export und sichere Löschfunktion mit Bestätigung
- **Vokabel-Import/Export** - CSV-Export für externe Bearbeitung

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

## Update & Backup (Sehr wichtig!)

**WICHTIG:** Mache immer ein Backup deiner Vokabeln, bevor du ein Update installierst! So gehen keine Daten verloren, auch wenn etwas schiefgeht.

### Backup vor dem Update

**Automatisches Backup (empfohlen):**
```bash
./scripts/backup.sh
```

**Manuelles Backup:**
```bash
# Vollständiges Backup mit Zeitstempel
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
mkdir -p ~/voll_backups/backup_$TIMESTAMP
cp -r ~/.local/share/voll ~/voll_backups/backup_$TIMESTAMP/data
cp -r ~/.config/voll ~/voll_backups/backup_$TIMESTAMP/config
```

### Update durchführen (Sichere Methode)

**Das install.sh erstellt jetzt automatisch ein Backup vor jedem Update!**

1. Gehe ins V.O.L.L.-Verzeichnis:
   ```bash
   cd V.O.L.L.
   ```
2. Hole die neueste Version:
   ```bash
   git pull
   ```
3. Installiere das Update (mit automatischem Backup):
   ```bash
   ./install.sh
   ```

**Nach dem Update:** Das Installationsprogramm erkennt automatisch Updates und:
- Erstellt ein vollständiges Backup deiner Daten
- Behält alle Vokabeln und Einstellungen bei
- Aktiviert neue Funktionen automatisch

### Backup wiederherstellen
```bash
# Verwende das neue Restore-Script
./scripts/restore.sh ~/voll_backups/backup_ZEITSTEMPEL

# Oder manuell:
cp -r ~/voll_backups/backup_ZEITSTEMPEL/data ~/.local/share/voll
cp -r ~/voll_backups/backup_ZEITSTEMPEL/config ~/.config/voll
```

## Deinstallation

**WICHTIG:** Erstelle vor der Deinstallation ein Backup deiner Vokabeln (siehe oben), falls du sie später noch brauchst!

1. Lösche die Programmdateien:
   ```bash
   # Python-Modul entfernen
   rm -rf ~/.local/lib/python*/site-packages/voll*
   
   # Ausführbare Datei entfernen
   rm -f ~/.local/bin/voll
   
   # Desktop-Integration entfernen
   rm -f ~/.local/share/applications/voll.desktop
   rm -f ~/.local/share/icons/hicolor/scalable/apps/voll.svg
   gtk-update-icon-cache -f -t ~/.local/share/icons/hicolor/
   ```

2. Optional: Persönliche Daten löschen (Achtung: Dies löscht alle Vokabeln und Einstellungen!)
   ```bash
   rm -rf ~/.local/share/voll    # Vokabeldatenbank
   rm -rf ~/.config/voll         # Einstellungen
   ```

3. Optional: Backup löschen, wenn du es nicht mehr brauchst:
   ```bash
   rm -rf ~/voll_backup
   ```

**Hinweis:** Die Systemabhängigkeiten (GTK4, etc.) werden nicht entfernt, da sie auch von anderen Programmen genutzt werden könnten.

## Häufige Fragen (FAQ)

### Wie funktioniert das Level-System?
V.O.L.L. nutzt ein intelligentes Lernsystem mit 4 Stufen (Level 1-4):
- **Level 1**: Neue Vokabeln - erscheinen sehr häufig
- **Level 2**: Teilweise gelernt - erscheinen regelmäßig
- **Level 3**: Gut gelernt - erscheinen gelegentlich
- **Level 4**: Gemeistert - erscheinen selten zur Auffrischung

Bei richtigen Antworten steigen Vokabeln im Level auf, bei Fehlern sinken sie wieder. So konzentrierst du dich automatisch auf schwierige Wörter.

### Wie mache ich ein Backup meiner Vokabeln?
Verwende das neue Backup-Script:
```bash
./scripts/backup.sh
```
Oder siehe Abschnitt "Update & Backup" oben für manuelle Methoden.

### Wie stelle ich ein Backup wieder her?
Verwende das neue Restore-Script:
```bash
./scripts/restore.sh ~/voll_backups/backup_ZEITSTEMPEL
```

### Was passiert beim Update mit meinen alten Vokabeln?
Deine alten Vokabeln bleiben erhalten. Neue Funktionen (wie das Level-System) werden automatisch aktiviert. Es empfiehlt sich trotzdem immer ein Backup zu machen.

### Programm startet nicht?
1. **Fehlende Abhängigkeiten:** Installationsskript erneut ausführen:
   ```bash
   ./install.sh
   ```
2. **Programm nicht im PATH:**
   - Terminal neu öffnen oder Rechner neu starten
   - Oder diese Zeile in `~/.bashrc` einfügen:
     ```bash
     export PATH="$HOME/.local/bin:$PATH"
     ```
3. **Fehlermeldungen anzeigen:**
   ```bash
   voll
   ```

### Wie lösche ich eine Datenbank sicher?
V.O.L.L. hat eine sichere Löschfunktion:
1. Gehe zu "Datenbank bearbeiten"
2. Klicke auf "Datenbank löschen" (roter Button)
3. Gib "Löschen" in das Bestätigungsfeld ein
4. Bestätige mit "Datenbank löschen"

**Wichtig**: Gelöschte Datenbanken können nicht wiederhergestellt werden!

### Weitere Hilfe
- [GitHub-Issue öffnen](https://github.com/jinxblackzoo/V.O.L.L./issues)
- Problem und Fehlermeldung beschreiben

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
