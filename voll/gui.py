#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Vokabeltrainer - Ein kinderfreundlicher Vokabeltrainer mit GTK4-Oberfläche
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

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib, Gio, Gdk
from voll.database import (
    init_db, add_vocabulary, get_all_vocabulary, update_vocabulary_stats,
    db_manager, get_vocab_for_practice, get_vocabulary_stats, get_language_stats,
    export_vocabulary_to_csv
)
import os
import subprocess
from datetime import datetime, timedelta
import random
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.set_title("Vokabeltrainer")
        self.set_default_size(800, 600)
        
        # Datenbank-Session
        self.session = init_db()
        
        # Hauptbox
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.main_box.set_margin_top(30)
        self.main_box.set_margin_bottom(30)
        self.main_box.set_margin_start(30)
        self.main_box.set_margin_end(30)
        self.set_child(self.main_box)
        
        # Content Stack für verschiedene Ansichten
        self.content_stack = Gtk.Stack()
        self.content_stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.main_box.append(self.content_stack)
        
        # Zurück-Button (anfangs versteckt)
        self.back_button = Gtk.Button(label="Zurück zum Hauptmenü")
        self.back_button.connect("clicked", self.show_main_menu)
        self.back_button.set_visible(False)
        self.back_button.set_margin_bottom(20)
        self.main_box.prepend(self.back_button)
        
        # Hauptmenü erstellen
        self.create_main_menu()
    
    def create_main_menu(self):
        """Erstellt das Hauptmenü"""
        menu_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        menu_box.set_margin_top(30)
        menu_box.set_margin_bottom(30)
        menu_box.set_margin_start(30)
        menu_box.set_margin_end(30)
        
        # Willkommenstext
        welcome_label = Gtk.Label()
        welcome_label.set_markup(
            "<span size='xx-large' weight='bold'>Willkommen beim Vokabeltrainer</span>"
        )
        menu_box.append(welcome_label)
        
        # Menü-Buttons
        button_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        button_box.set_margin_top(30)
        button_box.set_halign(Gtk.Align.CENTER)
        menu_box.append(button_box)
        
        # Existierende Datenbanken
        if db_manager.get_available_languages():
            db_button = Gtk.Button(label="Existierende Datenbanken")
            db_button.set_size_request(300, 50)
            db_button.connect("clicked", self.show_databases_menu)
            button_box.append(db_button)
        
        # Neue Datenbank
        new_db_button = Gtk.Button(label="Neue Datenbank hinzufügen")
        new_db_button.set_size_request(300, 50)
        new_db_button.connect("clicked", self.show_new_database_dialog)
        button_box.append(new_db_button)
        
        # Reports ansehen
        reports_button = Gtk.Button(label="Reports ansehen")
        reports_button.set_size_request(300, 50)
        reports_button.connect("clicked", self.show_reports)
        button_box.append(reports_button)
        
        self.content_stack.add_named(menu_box, "main_menu")
        self.content_stack.set_visible_child_name("main_menu")
    
    def show_main_menu(self, button=None):
        """Zeigt das Hauptmenü"""
        # Content Stack leeren
        while child := self.content_stack.get_first_child():
            self.content_stack.remove(child)
            
        # Hauptmenü neu erstellen
        self.create_main_menu()
        self.back_button.set_visible(False)
    
    def show_database_content(self, language):
        """Zeigt den Inhalt einer Datenbank"""
        # Hauptmenü verstecken
        self.back_button.set_visible(True)
        
        # Content Stack leeren
        while child := self.content_stack.get_first_child():
            self.content_stack.remove(child)
        
        # Datenbank-Inhalt erstellen
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        content_box.set_margin_top(20)
        content_box.set_margin_bottom(20)
        content_box.set_margin_start(20)
        content_box.set_margin_end(20)
        
        # Titel
        title_label = Gtk.Label()
        title_label.set_markup(f"<span size='x-large' weight='bold'>{language}</span>")
        content_box.append(title_label)
        
        # Aktionsbuttons
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        button_box.set_halign(Gtk.Align.CENTER)
        button_box.set_margin_top(20)
        
        add_button = Gtk.Button(label="Vokabeln hinzufügen")
        add_button.connect("clicked", self.show_add_dialog)
        button_box.append(add_button)
        
        practice_button = Gtk.Button(label="Vokabeln üben")
        practice_button.connect("clicked", self.show_practice_dialog)
        button_box.append(practice_button)
        
        edit_button = Gtk.Button(label="Datenbank bearbeiten")
        edit_button.connect("clicked", self.edit_database)
        button_box.append(edit_button)
        
        content_box.append(button_box)
        
        self.content_stack.add_named(content_box, "database")
        self.content_stack.set_visible_child_name("database")
    
    def edit_database(self, button):
        """Öffnet ein Fenster zum Bearbeiten der Vokabeln"""
        # Content Stack leeren
        while child := self.content_stack.get_first_child():
            self.content_stack.remove(child)
        
        # Bearbeitungs-Box erstellen
        edit_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        edit_box.set_margin_top(20)
        edit_box.set_margin_bottom(20)
        edit_box.set_margin_start(20)
        edit_box.set_margin_end(20)
        
        # Titel
        title_label = Gtk.Label()
        title_label.set_markup(f"<span size='x-large' weight='bold'>Vokabeln bearbeiten - {db_manager.get_active_language()}</span>")
        edit_box.append(title_label)
        
        # Scrollbare Liste erstellen
        scroll = Gtk.ScrolledWindow()
        scroll.set_vexpand(True)
        
        # Liste für Vokabeln
        list_box = Gtk.ListBox()
        list_box.set_selection_mode(Gtk.SelectionMode.NONE)
        scroll.set_child(list_box)
        
        # Vokabeln laden und anzeigen
        vocabulary = get_all_vocabulary(self.session)
        for vocab in vocabulary:
            # Box für Vokabelpaar
            vocab_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            vocab_box.set_margin_top(5)
            vocab_box.set_margin_bottom(5)
            vocab_box.set_margin_start(10)
            vocab_box.set_margin_end(10)
            
            # Deutsch-Eingabefeld
            german_entry = Gtk.Entry()
            german_entry.set_text(vocab.german)
            german_entry.set_hexpand(True)
            german_entry.connect('activate', self.on_vocab_changed, vocab, 'german')
            vocab_box.append(german_entry)
            
            # Fremdsprachen-Eingabefeld
            foreign_entry = Gtk.Entry()
            foreign_entry.set_text(vocab.foreign)
            foreign_entry.set_hexpand(True)
            foreign_entry.connect('activate', self.on_vocab_changed, vocab, 'foreign')
            vocab_box.append(foreign_entry)
            
            # Statistik-Label
            stats_label = Gtk.Label()
            stats_label.set_markup(
                f"<span size='small'>✓ {vocab.correct_count} | ✗ {vocab.wrong_count}</span>"
            )
            stats_label.set_margin_start(10)
            stats_label.set_margin_end(10)
            vocab_box.append(stats_label)
            
            # Löschen-Button
            delete_button = Gtk.Button()
            delete_button.set_icon_name("user-trash-symbolic")
            delete_button.connect('clicked', self.on_vocab_delete, vocab, list_box, vocab_box)
            vocab_box.append(delete_button)
            
            # Zur Liste hinzufügen
            list_box.append(vocab_box)
        
        edit_box.append(scroll)
        
        # Button-Box
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        button_box.set_margin_top(10)
        button_box.set_halign(Gtk.Align.CENTER)
        
        # Abbrechen-Button
        cancel_button = Gtk.Button(label="Abbrechen")
        cancel_button.connect('clicked', lambda b: self.show_main_menu())
        button_box.append(cancel_button)
        
        # Speichern-Button
        save_button = Gtk.Button(label="Speichern")
        save_button.connect('clicked', self.save_vocab_changes)
        button_box.append(save_button)
        
        # Datenbank löschen-Button
        delete_db_button = Gtk.Button(label="Datenbank löschen")
        delete_db_button.get_style_context().add_class("destructive-action")
        delete_db_button.connect('clicked', self.show_delete_database_dialog)
        button_box.append(delete_db_button)
        
        edit_box.append(button_box)
        
        self.content_stack.add_named(edit_box, "edit")
        self.content_stack.set_visible_child_name("edit")
    
    def show_delete_database_dialog(self, button):
        """Zeigt den Bestätigungsdialog zum Löschen der Datenbank"""
        current_language = db_manager.get_active_language()
        
        # Dialog erstellen
        dialog = Gtk.Dialog(
            title="Datenbank löschen",
            parent=self,
            modal=True
        )
        dialog.set_default_size(400, 200)
        
        # Content-Bereich
        content_area = dialog.get_content_area()
        content_area.set_spacing(20)
        content_area.set_margin_top(20)
        content_area.set_margin_bottom(20)
        content_area.set_margin_start(20)
        content_area.set_margin_end(20)
        
        # Warnung
        warning_label = Gtk.Label()
        warning_label.set_markup(
            f"<span size='large' weight='bold' foreground='red'>ACHTUNG!</span>\n\n"
            f"Sie sind dabei, die Datenbank <b>'{current_language}'</b> zu löschen.\n"
            f"Alle Vokabeln und Lernfortschritte gehen unwiderruflich verloren!\n\n"
            f"Geben Sie <b>'Löschen'</b> ein, um zu bestätigen:"
        )
        warning_label.set_justify(Gtk.Justification.CENTER)
        content_area.append(warning_label)
        
        # Eingabefeld
        confirmation_entry = Gtk.Entry()
        confirmation_entry.set_placeholder_text("Geben Sie 'Löschen' ein...")
        content_area.append(confirmation_entry)
        
        # Buttons
        dialog.add_button("Abbrechen", Gtk.ResponseType.CANCEL)
        delete_button = dialog.add_button("Datenbank löschen", Gtk.ResponseType.OK)
        delete_button.get_style_context().add_class("destructive-action")
        delete_button.set_sensitive(False)  # Anfangs deaktiviert
        
        # Eingabefeld-Handler
        def on_entry_changed(entry):
            text = entry.get_text().strip()
            delete_button.set_sensitive(text == "Löschen")
        
        confirmation_entry.connect("changed", on_entry_changed)
        confirmation_entry.connect("activate", lambda e: dialog.response(Gtk.ResponseType.OK) if confirmation_entry.get_text().strip() == "Löschen" else None)
        
        # Dialog-Handler
        def on_dialog_response(dialog, response):
            if response == Gtk.ResponseType.OK and confirmation_entry.get_text().strip() == "Löschen":
                self.delete_current_database()
            dialog.destroy()
        
        dialog.connect("response", on_dialog_response)
        dialog.show()
        confirmation_entry.grab_focus()
    
    def delete_current_database(self):
        """Löscht die aktuelle Datenbank"""
        current_language = db_manager.get_active_language()
        
        try:
            # Datenbank löschen
            db_manager.remove_language(current_language)
            
            # Erfolgsmeldung
            success_dialog = Gtk.MessageDialog(
                parent=self,
                modal=True,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text=f"Die Datenbank '{current_language}' wurde erfolgreich gelöscht!"
            )
            success_dialog.connect("response", lambda d, r: d.destroy())
            success_dialog.show()
            
            # Zurück zum Hauptmenü
            self.show_main_menu()
            
        except Exception as e:
            # Fehlermeldung
            error_dialog = Gtk.MessageDialog(
                parent=self,
                modal=True,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text=f"Fehler beim Löschen der Datenbank: {str(e)}"
            )
            error_dialog.connect("response", lambda d, r: d.destroy())
            error_dialog.show()
    
    def on_vocab_changed(self, entry, vocab, field):
        """Handler für Änderungen an Vokabeln"""
        new_text = entry.get_text().strip()
        # Wenn der Text bereits markiert ist, ignorieren
        if new_text.startswith('⟨') and new_text.endswith('⟩'):
            return
            
        old_text = vocab.german if field == 'german' else vocab.foreign
        
        if new_text != old_text:
            # Text mit Klammern markieren
            entry.set_text(f"⟨{new_text}⟩")
            # Textfarbe auf Blau setzen
            entry.get_style_context().add_class("modified-vocab")
            css_provider = Gtk.CssProvider()
            css_provider.load_from_data(b"entry.modified-vocab { color: blue; }")
            entry.get_style_context().add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
            
            # Vokabel aktualisieren aber noch nicht speichern
            if field == 'german':
                vocab.german = new_text
            else:
                vocab.foreign = new_text

            # Felder für neue Eingabe vorbereiten
            entry.grab_focus()
    
    def on_vocab_delete(self, button, vocab, list_box, vocab_box):
        """Handler für das Löschen von Vokabeln"""
        # Bestätigungsdialog anzeigen
        dialog = Gtk.MessageDialog(
            parent=self,
            modal=True,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text=f"Möchten Sie die Vokabel '{vocab.german} - {vocab.foreign}' wirklich löschen?"
        )
        dialog.connect("response", self.on_delete_confirm, vocab, list_box, vocab_box)
        dialog.show()
    
    def on_delete_confirm(self, dialog, response, vocab, list_box, vocab_box):
        """Handler für die Bestätigung des Löschens"""
        dialog.destroy()
        if response == Gtk.ResponseType.YES:
            # Aus der Datenbank löschen
            self.session.delete(vocab)
            
            # Eingabefelder deaktivieren und Text durchstreichen
            for child in vocab_box:
                if isinstance(child, Gtk.Entry):
                    text = child.get_text()
                    child.set_text(f"⟨{text}⟩")
                    child.set_sensitive(False)
                    child.get_style_context().add_class("deleted-vocab")
                    # Textfarbe auf Rot setzen
                    css_provider = Gtk.CssProvider()
                    css_provider.load_from_data(b"entry.deleted-vocab { color: red; }")
                    child.get_style_context().add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
            
            # Aus der Liste entfernen
            list_box.remove(vocab_box)
    
    def save_vocab_changes(self, button):
        """Speichert die Änderungen in der Datenbank"""
        try:
            self.session.commit()
            # Erfolgsmeldung
            dialog = Gtk.MessageDialog(
                parent=self,
                modal=True,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text="Änderungen wurden gespeichert!"
            )
            dialog.connect("response", lambda d, r: d.destroy())
            dialog.show()
            # Zurück zum Hauptmenü
            self.show_main_menu()
        except Exception as e:
            # Fehlermeldung
            dialog = Gtk.MessageDialog(
                parent=self,
                modal=True,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text=f"Fehler beim Speichern: {str(e)}"
            )
            dialog.connect("response", lambda d, r: d.destroy())
            dialog.show()
    
    def show_databases_menu(self, button):
        """Zeigt das Menü mit verfügbaren Datenbanken"""
        # Hauptmenü verstecken
        self.back_button.set_visible(True)
        
        # Content Stack leeren
        while child := self.content_stack.get_first_child():
            self.content_stack.remove(child)
        
        # Datenbank-Menü erstellen
        menu_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        menu_box.set_margin_top(20)
        menu_box.set_margin_bottom(20)
        menu_box.set_margin_start(20)
        menu_box.set_margin_end(20)
        
        # Titel
        title_label = Gtk.Label()
        title_label.set_markup("<span size='x-large' weight='bold'>Verfügbare Datenbanken</span>")
        menu_box.append(title_label)
        
        # Liste der Datenbanken
        languages = db_manager.get_available_languages()
        for lang in languages:
            lang_button = Gtk.Button(label=lang)
            lang_button.set_size_request(200, 40)
            lang_button.connect("clicked", lambda b, l=lang: self.open_database(l))
            menu_box.append(lang_button)
        
        self.content_stack.add_named(menu_box, "databases")
        self.content_stack.set_visible_child_name("databases")
    
    def open_database(self, language):
        """Öffnet eine Datenbank"""
        db_manager.set_active_language(language)
        self.show_database_content(language)
    
    def show_new_database_dialog(self, button):
        """Zeigt die Ansicht zum Erstellen einer neuen Datenbank"""
        self.back_button.set_visible(True)
        
        # Content Stack leeren
        while child := self.content_stack.get_first_child():
            self.content_stack.remove(child)
        
        # Neue Datenbank Box erstellen
        new_db_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        new_db_box.set_margin_top(20)
        new_db_box.set_margin_bottom(20)
        new_db_box.set_margin_start(20)
        new_db_box.set_margin_end(20)
        
        # Titel
        title_label = Gtk.Label()
        title_label.set_markup("<span size='x-large' weight='bold'>Neue Datenbank erstellen</span>")
        new_db_box.append(title_label)
        
        # Eingabefeld für Datenbankname
        name_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        name_label = Gtk.Label(label="Name der Datenbank:")
        name_box.append(name_label)
        self.name_entry = Gtk.Entry()
        self.name_entry.set_hexpand(True)
        name_box.append(self.name_entry)
        new_db_box.append(name_box)
        
        # Eingabefeld für Sprache
        language_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        language_label = Gtk.Label(label="Sprache:")
        language_box.append(language_label)
        self.language_entry = Gtk.Entry()
        self.language_entry.set_hexpand(True)
        language_box.append(self.language_entry)
        new_db_box.append(language_box)
        
        # Buttons
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        button_box.set_halign(Gtk.Align.CENTER)
        button_box.set_margin_top(20)
        
        save_button = Gtk.Button(label="Speichern")
        save_button.connect("clicked", self.save_new_database)
        button_box.append(save_button)
        
        new_db_box.append(button_box)
        
        # Enter-Taste Handling
        self.name_entry.connect("activate", lambda w: self.language_entry.grab_focus())
        self.language_entry.connect("activate", lambda w: self.save_new_database(None))
        
        self.content_stack.add_named(new_db_box, "new_database")
        self.content_stack.set_visible_child_name("new_database")
        
        # Fokus auf das erste Eingabefeld
        self.name_entry.grab_focus()
    
    def save_new_database(self, button):
        """Speichert die neue Datenbank"""
        name = self.name_entry.get_text().strip()
        language = self.language_entry.get_text().strip()
        
        if name and language:
            try:
                db_manager.create_database(name, language)
                # Zurück zum Hauptmenü
                self.show_main_menu()
            except Exception as e:
                error_dialog = Gtk.MessageDialog(
                    parent=self,
                    modal=True,
                    message_type=Gtk.MessageType.ERROR,
                    buttons=Gtk.ButtonsType.OK,
                    text=str(e)
                )
                error_dialog.connect("response", lambda d, r: d.destroy())
                error_dialog.show()
        else:
            error_dialog = Gtk.MessageDialog(
                parent=self,
                modal=True,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text="Bitte füllen Sie alle Felder aus!"
            )
            error_dialog.connect("response", lambda d, r: d.destroy())
            error_dialog.show()
    
    def show_add_dialog(self, button):
        """Zeigt die Ansicht zum Hinzufügen neuer Vokabeln"""
        # Hauptmenü verstecken
        self.back_button.set_visible(True)
        
        # Content Stack leeren
        while child := self.content_stack.get_first_child():
            self.content_stack.remove(child)
        
        # Vokabel-Eingabe-Box erstellen
        add_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        add_box.set_margin_top(20)
        add_box.set_margin_bottom(20)
        add_box.set_margin_start(20)
        add_box.set_margin_end(20)
        
        # Titel
        title_label = Gtk.Label()
        title_label.set_markup("<span size='x-large' weight='bold'>Neue Vokabeln hinzufügen</span>")
        add_box.append(title_label)
        
        # Eingabefelder
        foreign_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        foreign_label = Gtk.Label(label=f"{db_manager.get_active_language()}:")
        foreign_box.append(foreign_label)
        self.foreign_entry = Gtk.Entry()
        self.foreign_entry.set_hexpand(True)
        foreign_box.append(self.foreign_entry)
        add_box.append(foreign_box)
        
        german_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        german_label = Gtk.Label(label="Deutsch:")
        german_box.append(german_label)
        self.german_entry = Gtk.Entry()
        self.german_entry.set_hexpand(True)
        german_box.append(self.german_entry)
        add_box.append(german_box)
        
        # Buttons
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        button_box.set_halign(Gtk.Align.CENTER)
        button_box.set_margin_top(20)
        
        save_button = Gtk.Button(label="Speichern")
        save_button.connect("clicked", self.save_vocabulary)
        button_box.append(save_button)
        
        add_box.append(button_box)
        
        # Enter-Taste Handling
        self.foreign_entry.connect("activate", lambda w: self.german_entry.grab_focus())
        self.german_entry.connect("activate", lambda w: self.save_vocabulary(None))
        
        self.content_stack.add_named(add_box, "add")
        self.content_stack.set_visible_child_name("add")
        
        # Fokus auf das erste Eingabefeld
        self.foreign_entry.grab_focus()
    
    def save_vocabulary(self, button):
        """Speichert ein neues Vokabelpaar"""
        foreign = self.foreign_entry.get_text().strip()
        german = self.german_entry.get_text().strip()
        language = db_manager.get_active_language()
        
        if foreign and german and language:
            try:
                # Speichere Vokabel in der Datenbank mit Sprache
                add_vocabulary(self.session, german, foreign, language)
                self.session.commit()
                
                # Felder leeren und Fokus setzen
                self.foreign_entry.set_text("")
                self.german_entry.set_text("")
                self.foreign_entry.grab_focus()
            except Exception as e:
                error_dialog = Gtk.MessageDialog(
                    parent=self,
                    modal=True,
                    message_type=Gtk.MessageType.ERROR,
                    buttons=Gtk.ButtonsType.OK,
                    text=f"Fehler beim Speichern: {str(e)}"
                )
                error_dialog.connect("response", lambda d, r: d.destroy())
                error_dialog.show()
        else:
            error_dialog = Gtk.MessageDialog(
                parent=self,
                modal=True,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text="Bitte füllen Sie alle Felder aus!"
            )
            error_dialog.connect("response", lambda d, r: d.destroy())
            error_dialog.show()
    
    def show_practice_dialog(self, button):
        """Zeigt die Übungsansicht"""
        # Hauptmenü verstecken
        self.back_button.set_visible(True)
        
        # Content Stack leeren
        while child := self.content_stack.get_first_child():
            self.content_stack.remove(child)
        
        # Übungs-Box erstellen
        practice_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        practice_box.set_margin_top(20)
        practice_box.set_margin_bottom(20)
        practice_box.set_margin_start(20)
        practice_box.set_margin_end(20)
        
        # Titel
        title_label = Gtk.Label()
        title_label.set_markup("<span size='x-large' weight='bold'>Vokabeln üben</span>")
        practice_box.append(title_label)
        
        # Vokabel-Anzeige
        self.word_label = Gtk.Label()
        self.word_label.set_markup("<span size='x-large' weight='bold'>Lade Vokabel...</span>")
        practice_box.append(self.word_label)
        
        # Richtungs-Label
        self.direction_label = Gtk.Label()
        self.direction_label.set_markup("<span size='small'>Übersetzen Sie ins Deutsche</span>")
        practice_box.append(self.direction_label)
        
        # Eingabefeld
        self.practice_entry = Gtk.Entry()
        self.practice_entry.set_margin_top(10)
        practice_box.append(self.practice_entry)
        
        # Feedback-Label
        self.feedback_label = Gtk.Label()
        self.feedback_label.set_margin_top(10)
        practice_box.append(self.feedback_label)
        
        # Statistik-Label
        self.stats_label = Gtk.Label()
        self.stats_label.set_markup("<span size='small'>Richtig: 0 | Falsch: 0</span>")
        self.stats_label.set_margin_top(10)
        practice_box.append(self.stats_label)
        
        # Statistik-Variablen
        self.correct_count = 0
        self.wrong_count = 0
        self.current_vocab = None
        self.is_german_to_foreign = None
        self.next_vocab_timer = None  # Timer für die nächste Vokabel
        
        # Enter-Taste zum Bestätigen
        self.practice_entry.connect("activate", self.check_answer)
        
        self.content_stack.add_named(practice_box, "practice")
        self.content_stack.set_visible_child_name("practice")
        
        # Erste Vokabel laden
        self.load_next_vocab()
    
    def load_next_vocab(self):
        """Lädt die nächste Vokabel zum Üben"""
        # Timer stoppen, falls einer läuft
        if self.next_vocab_timer:
            GLib.source_remove(self.next_vocab_timer)
            self.next_vocab_timer = None
            
        vocab = get_vocab_for_practice(self.session)
        if not vocab:
            self.word_label.set_markup(
                "<span size='large'>Keine Vokabeln zum Üben verfügbar</span>"
            )
            self.practice_entry.set_sensitive(False)
            return False
        
        self.current_vocab = vocab
        
        # Richtung nur beim ersten Mal oder nach einer Antwort ändern
        if self.is_german_to_foreign is None:
            self.is_german_to_foreign = random.choice([True, False])
        
        if self.is_german_to_foreign:
            self.word_label.set_markup(
                f"<span size='x-large' weight='bold'>{vocab.german}</span>"
            )
            self.direction_label.set_markup(
                f"<span size='small'>Übersetzen Sie ins {db_manager.get_active_language()}</span>"
            )
        else:
            self.word_label.set_markup(
                f"<span size='x-large' weight='bold'>{vocab.foreign}</span>"
            )
            self.direction_label.set_markup(
                "<span size='small'>Übersetzen Sie ins Deutsche</span>"
            )
        
        self.practice_entry.set_text("")
        self.practice_entry.set_sensitive(True)
        self.practice_entry.grab_focus()
        self.feedback_label.set_markup("")
        return False  # Verhindert, dass der Timer weiterläuft
    
    def check_answer(self, widget):
        """Überprüft die eingegebene Antwort"""
        if not self.current_vocab:
            return
        
        # Deaktiviere das Eingabefeld während der Überprüfung
        self.practice_entry.set_sensitive(False)
        
        answer = self.practice_entry.get_text().strip()
        correct = False
        
        if self.is_german_to_foreign:
            correct = answer == self.current_vocab.foreign
            correct_answer = self.current_vocab.foreign
        else:
            correct = answer == self.current_vocab.german
            correct_answer = self.current_vocab.german
        
        if correct:
            self.feedback_label.set_markup(
                "<span foreground='green'>Richtig!</span>"
            )
            self.correct_count += 1
            update_vocabulary_stats(self.session, self.current_vocab.id, True)
        else:
            self.feedback_label.set_markup(
                f"<span foreground='red'>Falsch! Richtige Antwort: {correct_answer}</span>"
            )
            self.wrong_count += 1
            update_vocabulary_stats(self.session, self.current_vocab.id, False)
        
        self.stats_label.set_markup(
            f"<span size='small'>Richtig: {self.correct_count} | Falsch: {self.wrong_count}</span>"
        )
        
        # Zufällige Richtung für die nächste Vokabel
        self.is_german_to_foreign = random.choice([True, False])
        
        # Nächste Vokabel nach kurzer Verzögerung
        self.next_vocab_timer = GLib.timeout_add(1500, self.load_next_vocab)
    
    def show_reports(self, button):
        """Zeigt die Reports"""
        # Hauptmenü verstecken
        self.back_button.set_visible(True)
        
        # Content Stack leeren
        while child := self.content_stack.get_first_child():
            self.content_stack.remove(child)
        
        # Reports Box erstellen
        reports_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        reports_box.set_margin_top(20)
        reports_box.set_margin_bottom(20)
        reports_box.set_margin_start(20)
        reports_box.set_margin_end(20)
        
        # Notebook für Tabs
        notebook = Gtk.Notebook()
        notebook.set_vexpand(True)
        reports_box.append(notebook)
        
        # Statistiken laden
        stats = get_language_stats(self.session)
        
        for language, lang_stats in stats.items():
            # Tab-Inhalt
            scroll = Gtk.ScrolledWindow()
            content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            content_box.set_margin_top(20)
            content_box.set_margin_bottom(20)
            content_box.set_margin_start(20)
            content_box.set_margin_end(20)
            scroll.set_child(content_box)
            
            # Überschrift
            header = Gtk.Label()
            header.set_markup(f"<span size='x-large' weight='bold'>{language}</span>")
            content_box.append(header)
            
            # Zeitliche Statistiken
            time_stats = Gtk.Label()
            time_stats.set_markup(
                "<span weight='bold'>Zeitliche Statistiken:</span>\n"
                f"Heute: {sum(1 for v in lang_stats['vocab_stats'] if v['last_practiced'] and v['last_practiced'].date() == datetime.now().date())} Vokabeln geübt\n"
                f"Gestern: {sum(1 for v in lang_stats['vocab_stats'] if v['last_practiced'] and v['last_practiced'].date() == datetime.now().date() - timedelta(days=1))} Vokabeln geübt\n"
                f"Letzte Woche: {sum(1 for v in lang_stats['vocab_stats'] if v['last_practiced'] and v['last_practiced'].date() >= datetime.now().date() - timedelta(days=7))} Vokabeln geübt\n"
                f"Letzter Monat: {sum(1 for v in lang_stats['vocab_stats'] if v['last_practiced'] and v['last_practiced'].date() >= datetime.now().date() - timedelta(days=30))} Vokabeln geübt\n"
                f"Letztes Jahr: {sum(1 for v in lang_stats['vocab_stats'] if v['last_practiced'] and v['last_practiced'].date() >= datetime.now().date() - timedelta(days=365))} Vokabeln geübt\n"
            )
            time_stats.set_margin_top(20)
            content_box.append(time_stats)
            
            # Gesamtstatistik
            summary = Gtk.Label()
            summary.set_markup(
                "<span weight='bold'>Gesamtstatistik:</span>\n"
                f"Vokabeln gesamt: {lang_stats['total_words']}\n"
                f"Gemeisterte Vokabeln: {lang_stats['mastered_words']}\n"
                f"Richtige Antworten: {lang_stats['total_correct']}"
            )
            summary.set_margin_top(20)
            content_box.append(summary)
            
            # PDF-Report Button
            pdf_button = Gtk.Button(label="PDF-Report")
            pdf_button.connect("clicked", self.create_pdf_report, language)
            content_box.append(pdf_button)
            
            # Tab hinzufügen
            tab_label = Gtk.Label(label=language)
            notebook.append_page(scroll, tab_label)
        
        self.content_stack.add_named(reports_box, "reports")
        self.content_stack.set_visible_child_name("reports")
    
    def create_pdf_report(self, button, language):
        """Erstellt einen PDF-Report"""
        from datetime import datetime
        import os
        import subprocess
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import cm
        from reportlab.pdfgen import canvas
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        
        try:
            print("Starting PDF report generation...")
            
            # Home-Verzeichnis ermitteln
            home_dir = os.path.expanduser("~")
            print(f"Home directory: {home_dir}")
            
            # Dateinamen und Pfad festlegen
            date_str = datetime.now().strftime("%d-%m-%Y")
            filepath = os.path.join(home_dir, "Downloads", f"{date_str}-{language}.pdf")
            print(f"Target file path: {filepath}")
            
            # Generiere den PDF-Report
            print("Getting language stats...")
            all_stats = get_language_stats(self.session, language)
            stats = all_stats[language]
            
            print("Creating PDF...")
            c = canvas.Canvas(filepath, pagesize=A4)
            width, height = A4
            
            # Titel
            c.setFont("Helvetica-Bold", 24)
            c.drawString(2*cm, height-3*cm, f"Vokabeltrainer Report - {language}")
            c.setFont("Helvetica", 14)
            c.drawString(2*cm, height-4*cm, f"Erstellt am {date_str}")
            
            # Zeitliche Statistiken
            c.setFont("Helvetica-Bold", 16)
            c.drawString(2*cm, height-6*cm, "Zeitliche Statistiken")
            c.setFont("Helvetica", 12)
            
            today = datetime.now().date()
            y_position = height-7*cm
            
            stats_text = [
                f"Heute: {sum(1 for v in stats['vocab_stats'] if v['last_practiced'] and v['last_practiced'].date() == today)} Vokabeln geübt",
                f"Gestern: {sum(1 for v in stats['vocab_stats'] if v['last_practiced'] and v['last_practiced'].date() == today - timedelta(days=1))} Vokabeln geübt",
                f"Letzte Woche: {sum(1 for v in stats['vocab_stats'] if v['last_practiced'] and v['last_practiced'].date() >= today - timedelta(days=7))} Vokabeln geübt",
                f"Letzter Monat: {sum(1 for v in stats['vocab_stats'] if v['last_practiced'] and v['last_practiced'].date() >= today - timedelta(days=30))} Vokabeln geübt",
                f"Letztes Jahr: {sum(1 for v in stats['vocab_stats'] if v['last_practiced'] and v['last_practiced'].date() >= today - timedelta(days=365))} Vokabeln geübt"
            ]
            
            for line in stats_text:
                c.drawString(2*cm, y_position, line)
                y_position -= 0.8*cm
            
            # Gesamtstatistik
            c.setFont("Helvetica-Bold", 16)
            c.drawString(2*cm, y_position-1.5*cm, "Gesamtstatistik")
            c.setFont("Helvetica", 12)
            y_position -= 2.5*cm
            
            total_stats = [
                f"Vokabeln gesamt: {stats['total_words']}",
                f"Gemeisterte Vokabeln: {stats['mastered_words']}",
                f"Richtige Antworten: {stats['total_correct']}",
                f"Goldene Sterne: {stats['golden_stars']}",
                f"Rote Sterne: {stats['red_stars']}",
                f"Einhornpupse: {stats['unicorn_farts']}"
            ]
            
            for line in total_stats:
                c.drawString(2*cm, y_position, line)
                y_position -= 0.8*cm
            
            c.save()
            print(f"File created: {os.path.exists(filepath)}")
            
            # Öffne die PDF-Datei
            print("Trying to open file...")
            result = subprocess.run(['xdg-open', filepath], capture_output=True, text=True)
            print(f"Open command result: {result.returncode}")
            if result.stderr:
                print(f"Error opening file: {result.stderr}")
            
            print("PDF report generation completed")
            
        except Exception as e:
            print(f"Error during PDF report generation: {str(e)}")
    
class VocabTrainerApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()

def main():
    app = VocabTrainerApp(application_id="de.blackzoo.voll")
    return app.run(None)

if __name__ == "__main__":
    main()
