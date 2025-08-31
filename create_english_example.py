#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Skript zum Erstellen einer Englisch-Beispieldatenbank für V.O.L.L.
Erstellt eine Englisch-Datenbank mit 20 Standardvokabeln.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'voll'))

from voll.database import init_db, add_vocabulary, db_manager

def create_english_example_database():
    """Erstellt eine Englisch-Beispieldatenbank mit 20 Standardvokabeln"""
    
    print("Erstelle Englische Beispieldatenbank...")
    try:
        # Datenbank erstellen falls sie nicht existiert
        if 'Englisch' not in db_manager.get_available_languages():
            db_manager.create_database("Englisch", "Englisch")
        
        db_manager.set_active_language('Englisch')
        session = init_db('Englisch')
        
        # 20 Standardvokabeln
        english_vocabulary = [
            ("Hallo", "hello"),
            ("Tschüss", "goodbye"),
            ("Danke", "thank you"),
            ("Bitte", "please"),
            ("Entschuldigung", "excuse me"),
            ("Familie", "family"),
            ("Mutter", "mother"),
            ("Vater", "father"),
            ("Haus", "house"),
            ("Wasser", "water"),
            ("Brot", "bread"),
            ("Apfel", "apple"),
            ("rot", "red"),
            ("blau", "blue"),
            ("grün", "green"),
            ("Hund", "dog"),
            ("Katze", "cat"),
            ("Schule", "school"),
            ("Buch", "book"),
            ("Zeit", "time")
        ]
        
        for german, english in english_vocabulary:
            add_vocabulary(session, german, english, 'Englisch')
            print(f"✓ {german} - {english}")
        
        session.close()
        print(f"✅ Englisch-Beispieldatenbank erstellt ({len(english_vocabulary)} Vokabeln)")
        print("\nStarte V.O.L.L. mit: voll")
        
    except Exception as e:
        print(f"❌ Fehler: {e}")

if __name__ == "__main__":
    create_english_example_database()
