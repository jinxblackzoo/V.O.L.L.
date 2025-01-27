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

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
import json
import random
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
            'vokabeltrainer'
        )
        self.data_dir = os.path.join(
            os.environ.get('XDG_DATA_HOME', os.path.expanduser('~/.local/share')),
            'vokabeltrainer'
        )
        
        # Erstelle die Verzeichnisse
        os.makedirs(self.config_dir, exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)
        
        self.config_file = os.path.join(self.config_dir, 'databases.json')
        self.load_config()

    def load_config(self):
        """Lädt die Konfiguration oder erstellt eine neue"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = {
                'databases': {},
                'active_db': None
            }
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
    """Initialisiert die Datenbank für die angegebene Sprache"""
    db_path = db_manager.get_db_path(language)
    engine = create_engine(f'sqlite:///{db_path}')
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()

def add_vocabulary(session, german, foreign, language):
    vocab = Vocabulary(german=german, foreign=foreign, language=language)
    session.add(vocab)
    session.commit()

def get_all_vocabulary(session):
    return session.query(Vocabulary).all()

def update_vocabulary_stats(session, vocab_id, correct):
    """Aktualisiert die Statistiken einer Vokabel nach einer Antwort"""
    vocab = session.query(Vocabulary).get(vocab_id)
    
    if correct:
        vocab.correct_count += 1
        vocab.consecutive_correct += 1
        
        # Prüfe ob die Vokabel gemeistert wurde (4 mal in Folge richtig)
        if vocab.consecutive_correct >= 4:
            vocab.mastered = True
    else:
        vocab.wrong_count += 1
        vocab.consecutive_correct = 0  # Zurücksetzen bei falscher Antwort
        vocab.mastered = False
    
    vocab.last_practiced = datetime.now()
    session.commit()

def get_vocab_for_practice(session):
    """
    Wählt eine Vokabel zum Üben aus.
    Nicht gemeisterte Vokabeln (weniger als 4 richtige Antworten) werden häufiger gewählt.
    """
    from sqlalchemy.sql.expression import func
    
    # Hole alle Vokabeln
    all_vocab = session.query(Vocabulary).all()
    if not all_vocab:
        return None
        
    # Gewichte die Vokabeln basierend auf ihrem Status
    weighted_vocab = []
    for vocab in all_vocab:
        # Neu hinzugefügte oder nicht gemeisterte Vokabeln bekommen mehr Gewicht
        if vocab.correct_count == 0:
            weight = 5  # Höheres Gewicht für neue Vokabeln
        elif not vocab.mastered:
            weight = 3  # Höheres Gewicht für nicht gemeisterte Vokabeln
        else:
            weight = 1  # Geringeres Gewicht für gemeisterte Vokabeln
        
        weighted_vocab.extend([vocab] * weight)
    
    # Wähle eine zufällige Vokabel aus der gewichteten Liste
    return random.choice(weighted_vocab) if weighted_vocab else None

def get_vocabulary_stats(session):
    """Gibt Statistiken über den Lernfortschritt zurück"""
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
