#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Vokabeltrainer - Datenbankmodul für den Vokabeltrainer
Copyright (C) 2025 jinx@blackzoo.de

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import os
import json
import shutil
from datetime import datetime, timedelta
import random
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Float
from sqlalchemy.orm import declarative_base, sessionmaker
import csv

Base = declarative_base()

class Vocabulary(Base):
    __tablename__ = 'vocabulary'
    
    id = Column(Integer, primary_key=True)
    german = Column(String, nullable=False)
    foreign = Column(String, nullable=False)
    language = Column(String, nullable=False)
    correct_count = Column(Integer, default=0)
    wrong_count = Column(Integer, default=0)
    consecutive_correct = Column(Integer, default=0)  # Anzahl aufeinanderfolgender richtiger Antworten
    last_practiced = Column(DateTime, nullable=True)
    mastered = Column(Boolean, default=False)  # True wenn 4 mal korrekt beantwortet
    
    # Neues Level-basiertes Lernsystem
    level = Column(Integer, default=1)  # Level 1-4
    level_correct_count = Column(Integer, default=0)  # Richtige Antworten im aktuellen Level
    level_total_count = Column(Integer, default=0)  # Gesamte Abfragen im aktuellen Level
    level_wrong_streak = Column(Integer, default=0)  # Falsche Antworten in Folge für Rückstufung
    frequency_multiplier = Column(Float, default=1.0)  # Faktor für Abfragefrequenz

class StudySession(Base):
    __tablename__ = 'study_sessions'
    
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.now)
    duration = Column(Float)  # in minutes
    words_practiced = Column(Integer)
    correct_answers = Column(Integer)

class DatabaseManager:
    def __init__(self):
        self.config_dir = os.path.join(
            os.environ.get('XDG_CONFIG_HOME', os.path.expanduser('~/.config')),
            'voll'
        )
        self.data_dir = os.path.join(
            os.environ.get('XDG_DATA_HOME', os.path.expanduser('~/.local/share')),
            'voll'
        )
        
        # Erstelle die Verzeichnisse
        os.makedirs(self.config_dir, exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)
        
        self.config_file = os.path.join(self.config_dir, 'databases.json')
        self.load_config()

    def load_config(self):
        """Lädt die Konfiguration oder erstellt eine neue"""
        config_exists = os.path.exists(self.config_file)
        
        if config_exists:
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                
                # Überprüfe, ob die aktive Datenbank tatsächlich existiert
                if self.config['active_db']:
                    db_file = self.config['databases'].get(self.config['active_db'])
                    if db_file:
                        db_path = os.path.join(self.data_dir, db_file)
                        if not os.path.exists(db_path):
                            print(f"Warnung: Aktive Datenbank {db_path} nicht gefunden")
                            self.config['active_db'] = None
                            self.save_config()
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Fehler beim Laden der Konfiguration: {e}")
                config_exists = False  # Behandle es wie eine nicht existierende Konfiguration
                
        if not config_exists:
            # Erstelle eine neue Konfiguration mit Englisch als Standardsprache
            self.config = {
                'databases': {},
                'active_db': None
            }
            
            # Erstelle die Englisch-Datenbank beim ersten Start
            try:
                language = "Englisch"
                db_file = "Englisch.db"
                db_path = os.path.join(self.data_dir, db_file)
                
                # Überprüfe, ob die Datenbankdatei bereits existiert
                if os.path.exists(db_path):
                    print(f"Warnung: Datenbank {db_path} existiert bereits")
                    # Füge sie einfach zur Konfiguration hinzu
                else:
                    # Erstelle die physische Datenbank
                    engine = create_engine(f'sqlite:///{db_path}')
                    Base.metadata.create_all(engine)
                    print(f"Neue {language}-Datenbank wurde erstellt")
                
                # Aktualisiere die Konfiguration
                self.config['databases'][language] = db_file
                self.config['active_db'] = language
                self.save_config()
                print(f"{language}-Datenbank wurde als aktiv gesetzt")
                
            except Exception as e:
                print(f"Fehler beim Erstellen der Standarddatenbank: {e}")
                # Stelle sicher, dass wir eine gültige (wenn auch leere) Konfiguration haben
                self.config = {'databases': {}, 'active_db': None}
        
        self.save_config()

    def save_config(self):
        """Speichert die Konfiguration"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4)

    def get_db_path(self, language=None):
        """Gibt den Pfad zur Datenbank zurück"""
        if language is None:
            language = self.config['active_db']
        
        db_file = self.config['databases'].get(language)
        if not db_file:
            raise ValueError(f"Keine Datenbank für {language} gefunden")
            
        return os.path.join(self.data_dir, db_file)

    def get_available_languages(self):
        """Gibt eine Liste aller verfügbaren Sprachen zurück"""
        return list(self.config['databases'].keys())

    def get_active_language(self):
        """Gibt die aktive Sprache zurück"""
        return self.config['active_db']

    def set_active_language(self, language):
        """Setzt die aktive Sprache"""
        if language not in self.config['databases']:
            raise ValueError(f"Sprache {language} nicht gefunden")
        
        self.config['active_db'] = language
        self.save_config()

    def add_language(self, language, db_file=None):
        """Fügt eine neue Sprache hinzu"""
        if language in self.config['databases']:
            raise ValueError(f"Sprache {language} existiert bereits")
            
        if db_file is None:
            db_file = language.lower().replace(' ', '_') + '.db'
            
        self.config['databases'][language] = db_file
        self.save_config()
        
        # Initialisiere die neue Datenbank
        db_path = os.path.join(self.data_dir, db_file)
        engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(engine)

    def remove_language(self, language):
        """Entfernt eine Sprache"""
        if language not in self.config['databases']:
            raise ValueError(f"Sprache {language} nicht gefunden")
            
        db_path = self.get_db_path(language)
        
        # Lösche die Datenbankdatei
        if os.path.exists(db_path):
            os.remove(db_path)
            
        # Entferne den Eintrag aus der Konfiguration
        del self.config['databases'][language]
        
        # Wenn die aktive Datenbank gelöscht wurde, wähle eine andere
        if self.config['active_db'] == language and self.config['databases']:
            self.config['active_db'] = next(iter(self.config['databases']))
            
        self.save_config()

    def create_database(self, name, language):
        """Erstellt eine neue Datenbank"""
        # Überprüfe ob der Name gültig ist
        if not name or not language:
            raise ValueError("Name und Sprache dürfen nicht leer sein")
        
        # Überprüfe ob die Datenbank bereits existiert
        if language in self.config['databases']:
            raise ValueError(f"Eine Datenbank für {language} existiert bereits")
        
        # Erstelle die Datenbankdatei
        db_file = f"{language}.db"
        db_path = os.path.join(self.data_dir, db_file)
        engine = create_engine(f'sqlite:///{db_path}')
        
        # Erstelle die Tabellen
        Base.metadata.create_all(engine)
        
        # Füge die Datenbank zum Manager hinzu
        self.config['databases'][language] = db_file
        
        # Setze die neue Datenbank als aktiv
        self.config['active_db'] = language
        self.save_config()
        
        return True

# Globale Instanz des DatabaseManager
db_manager = DatabaseManager()

def init_db(language=None):
    """Initialisiert die Datenbank für die angegebene Sprache oder die aktive Sprache"""
    if language is None:
        language = db_manager.get_active_language()
        if language is None:
            # Wenn keine aktive Sprache gesetzt ist, setze Englisch als Standard
            db_manager.add_language('Englisch')
            db_manager.set_active_language('Englisch')
            language = 'Englisch'
    
    db_path = db_manager.get_db_path(language)
    engine = create_engine(f'sqlite:///{db_path}')
    
    # Sichere Migration: Prüfe und erweitere bestehende Datenbanken
    _migrate_database_if_needed(engine)
    
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()

def _migrate_database_if_needed(engine):
    """Sichere Migration bestehender Datenbanken auf das neue Level-System"""
    try:
        # Prüfe, ob die Tabelle 'vocabulary' existiert
        with engine.connect() as conn:
            result = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='vocabulary'"
            )
            if not result.fetchone():
                # Neue Datenbank, keine Migration nötig
                return
            
            # Prüfe, ob die neuen Level-Spalten bereits existieren
            result = conn.execute("PRAGMA table_info(vocabulary)")
            columns = [row[1] for row in result.fetchall()]
            
            new_columns = {
                'level': 'INTEGER DEFAULT 1',
                'level_correct_count': 'INTEGER DEFAULT 0',
                'level_total_count': 'INTEGER DEFAULT 0', 
                'level_wrong_streak': 'INTEGER DEFAULT 0',
                'frequency_multiplier': 'REAL DEFAULT 1.0'
            }
            
            # Füge fehlende Spalten hinzu
            for column_name, column_def in new_columns.items():
                if column_name not in columns:
                    print(f"Migration: Füge Spalte '{column_name}' zur Vocabulary-Tabelle hinzu")
                    conn.execute(f"ALTER TABLE vocabulary ADD COLUMN {column_name} {column_def}")
                    conn.commit()
            
            print("Datenbank-Migration erfolgreich abgeschlossen!")
            
    except Exception as e:
        print(f"Warnung: Migration fehlgeschlagen: {e}")
        print("Die Datenbank wird trotzdem versucht zu initialisieren...")

def create_database_backup(language=None):
    """Erstellt ein Backup einer Vokabeldatenbank"""
    if language is None:
        language = db_manager.get_active_language()
    
    if not language:
        print("Keine aktive Sprache gefunden")
        return False
    
    try:
        # Quell-Datenbankpfad
        source_path = db_manager.get_db_path(language)
        if not os.path.exists(source_path):
            print(f"Datenbank für {language} nicht gefunden: {source_path}")
            return False
        
        # Backup-Pfad mit Zeitstempel
        backup_dir = os.path.join(db_manager.data_dir, 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"{language}_backup_{timestamp}.db"
        backup_path = os.path.join(backup_dir, backup_filename)
        
        # Backup erstellen
        shutil.copy2(source_path, backup_path)
        
        print(f"Backup erfolgreich erstellt: {backup_path}")
        return True
        
    except Exception as e:
        print(f"Fehler beim Erstellen des Backups: {e}")
        return False

def add_vocabulary(session, german, foreign, language):
    vocab = Vocabulary(german=german, foreign=foreign, language=language)
    session.add(vocab)
    session.commit()

def get_all_vocabulary(session):
    return session.query(Vocabulary).all()

def update_vocabulary_stats(session, vocab_id, correct):
    """Aktualisiert die Statistiken einer Vokabel nach einer Antwort im Level-basierten System"""
    vocab = session.query(Vocabulary).get(vocab_id)
    
    # Allgemeine Statistiken aktualisieren
    vocab.last_practiced = datetime.now()
    vocab.level_total_count += 1
    
    if correct:
        vocab.correct_count += 1
        vocab.consecutive_correct += 1
        vocab.level_correct_count += 1
        vocab.level_wrong_streak = 0  # Zurücksetzen bei richtiger Antwort
        
        # Prüfung für Level-Aufstieg
        _check_level_promotion(vocab)
        
    else:
        vocab.wrong_count += 1
        vocab.consecutive_correct = 0
        vocab.level_wrong_streak += 1
        
        # Prüfung für Level-Rückstufung oder Frequenz-Erhöhung
        _check_level_demotion(vocab)
    
    # Mastered-Status basierend auf Level 4
    vocab.mastered = (vocab.level >= 4)
    
    session.commit()

def _check_level_promotion(vocab):
    """Prüft und führt Level-Aufstieg durch"""
    promotion_requirements = {
        1: {'min_total': 5, 'required_correct': 4},
        2: {'min_total': 10, 'required_correct': 6}, 
        3: {'min_total': 15, 'required_correct': 10}
    }
    
    if vocab.level <= 3:  # Level 4 ist das Maximum
        req = promotion_requirements[vocab.level]
        if (vocab.level_total_count >= req['min_total'] and 
            vocab.level_correct_count >= req['required_correct']):
            
            vocab.level += 1
            vocab.level_correct_count = 0
            vocab.level_total_count = 0
            vocab.frequency_multiplier = 1.0  # Zurücksetzen
            print(f"Vokabel '{vocab.german}' auf Level {vocab.level} aufgestiegen!")

def _check_level_demotion(vocab):
    """Prüft und führt Level-Rückstufung oder Frequenz-Erhöhung durch"""
    if vocab.level == 1:
        # Level 1: Erhöhung der Abfragefrequenz um Faktor 2
        if vocab.level_wrong_streak >= 1:
            vocab.frequency_multiplier = min(vocab.frequency_multiplier * 2, 8.0)  # Max 8x
            print(f"Vokabel '{vocab.german}' Frequenz erhöht auf {vocab.frequency_multiplier}x")
            
    elif vocab.level == 2:
        # Level 2: 1 mal falsch > Rückstufung auf Level 1
        if vocab.level_wrong_streak >= 1:
            vocab.level = 1
            vocab.level_correct_count = 0
            vocab.level_total_count = 0
            vocab.frequency_multiplier = 2.0  # Erhöhte Frequenz nach Rückstufung
            print(f"Vokabel '{vocab.german}' auf Level 1 zurückgestuft!")
            
    elif vocab.level >= 3:
        # Level 3&4: 2 mal falsch > Rückstufung um ein Level
        if vocab.level_wrong_streak >= 2:
            vocab.level -= 1
            vocab.level_correct_count = 0
            vocab.level_total_count = 0
            vocab.frequency_multiplier = 1.5  # Leicht erhöhte Frequenz nach Rückstufung
            print(f"Vokabel '{vocab.german}' auf Level {vocab.level} zurückgestuft!")

def get_vocab_for_practice(session):
    """
    Wählt eine Vokabel zum Üben aus basierend auf dem neuen Level-System.
    Level 1: Gewichtung 4, Level 2: Gewichtung 3, Level 3: Gewichtung 2, Level 4: Gewichtung 1
    Berücksichtigt auch Frequenz-Multiplikatoren für besonders schwierige Vokabeln.
    """
    from sqlalchemy.sql.expression import func
    
    # Hole alle Vokabeln der aktiven Sprache
    active_language = db_manager.get_active_language()
    if not active_language:
        return None
        
    all_vocab = session.query(Vocabulary).filter(Vocabulary.language == active_language).all()
    if not all_vocab:
        return None
        
    # Gewichte die Vokabeln basierend auf ihrem Level und Frequenz-Multiplikator
    weighted_vocab = []
    for vocab in all_vocab:
        # Basis-Gewichtung nach Level (umgekehrt: niedrigeres Level = höhere Priorität)
        level_weights = {1: 4, 2: 3, 3: 2, 4: 1}
        base_weight = level_weights.get(vocab.level, 1)
        
        # Anpassung durch Frequenz-Multiplikator
        final_weight = int(base_weight * vocab.frequency_multiplier)
        
        # Mindestgewicht von 1, um sicherzustellen, dass alle Vokabeln gelegentlich abgefragt werden
        final_weight = max(final_weight, 1)
        
        # Vokabel entsprechend ihrem Gewicht zur Liste hinzufügen
        weighted_vocab.extend([vocab] * final_weight)
    
    # Wähle eine zufällige Vokabel aus der gewichteten Liste
    return random.choice(weighted_vocab) if weighted_vocab else None

def get_vocabulary_stats(session, language=None):
    """Gibt Statistiken über den Lernfortschritt zurück"""
    # Verwende die aktive Sprache, wenn keine spezifiziert wurde
    if language is None:
        language = db_manager.get_active_language()
    
    # Filtere nach der angegebenen Sprache
    if language:
        total = session.query(Vocabulary).filter(Vocabulary.language == language).count()
        mastered = session.query(Vocabulary).filter(
            Vocabulary.language == language,
            Vocabulary.mastered == True
        ).count()
    else:
        # Fallback: alle Sprachen (wenn keine aktive Sprache gesetzt ist)
        total = session.query(Vocabulary).count()
        mastered = session.query(Vocabulary).filter(Vocabulary.mastered == True).count()
    
    in_progress = total - mastered
    
    return {
        'total': total,
        'mastered': mastered,
        'in_progress': in_progress,
        'mastered_percentage': (mastered / total * 100) if total > 0 else 0
    }

def add_study_session(session, duration, words_practiced, correct_answers):
    study_session = StudySession(
        duration=duration,
        words_practiced=words_practiced,
        correct_answers=correct_answers
    )
    session.add(study_session)
    session.commit()

def get_weekly_stats(session):
    """Hole die Statistiken der letzten 7 Tage"""
    from datetime import timedelta
    week_ago = datetime.now() - timedelta(days=7)
    return session.query(StudySession).filter(StudySession.date >= week_ago).all()

def get_language_stats(session, language=None):
    """Hole Statistiken für eine bestimmte Sprache oder alle Sprachen"""
    if language:
        languages = [language]
    else:
        languages = db_manager.get_available_languages()
    
    stats = {}
    for lang in languages:
        vocab_list = (
            session.query(Vocabulary)
            .filter(Vocabulary.language == lang)
            .all()
        )
        
        total_correct = sum(v.correct_count for v in vocab_list)
        total_words = len(vocab_list)
        mastered_words = sum(1 for v in vocab_list if v.mastered)
        
        # Sterne berechnen
        golden_stars = total_correct // 50  # Ein goldener Stern für je 50 richtige Antworten
        red_stars = total_words // 50  # Ein roter Stern für je 50 eingegebene Vokabelpaare
        
        # Einhornpupse berechnen (min von goldenen und roten Sternen)
        unicorn_farts = min(golden_stars, red_stars)
        # Verbleibende Sterne nach Einhornpups-Berechnung
        remaining_golden_stars = golden_stars - unicorn_farts
        remaining_red_stars = red_stars - unicorn_farts
        
        stats[lang] = {
            'total_words': total_words,
            'mastered_words': mastered_words,
            'total_correct': total_correct,
            'golden_stars': remaining_golden_stars,  # Verbleibende goldene Sterne
            'red_stars': remaining_red_stars,  # Verbleibende rote Sterne
            'unicorn_farts': unicorn_farts,  # Anzahl der Einhornpupse
            'vocab_stats': [
                {
                    'foreign': v.foreign,
                    'german': v.german,
                    'correct_answers': v.correct_count,
                    'wrong_answers': v.wrong_count,
                    'mastered': v.mastered,
                    'last_practiced': v.last_practiced
                }
                for v in sorted(vocab_list, key=lambda x: x.foreign.lower())
            ]
        }
    
    return stats

def export_vocabulary_to_csv(session, filepath):
    """Exportiert die Vokabeln in eine CSV-Datei"""
    vocabulary = session.query(Vocabulary).all()
    
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        # Header
        writer.writerow(['Deutsch', db_manager.get_active_language(), 'Richtige', 'Falsche'])
        # Daten
        for vocab in vocabulary:
            writer.writerow([vocab.german, vocab.foreign, vocab.correct_count, vocab.wrong_count])
