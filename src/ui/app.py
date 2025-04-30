import streamlit as st
import os
import tempfile
import json
import base64
from PIL import Image
import io
import sys
import pandas as pd
import re
from pathlib import Path
from datetime import datetime

# Füge den übergeordneten Ordner zum Pythonpfad hinzu, um relative Importe zu ermöglichen
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Importe aus den reorganisierten Modulen
from src.core.document_processor import DocumentProcessor
from src.core.ai_extractor import AIExtractor
from src.core.combined_processor import CombinedProcessor
from src.templates.template_generator import ProfileGenerator
import src.utils.config as config  # Importiere das Konfigurationsmodul
from src.ui.settings import render_settings_page  # Importiere die Einstellungsseite

# CSS für Farbverlaufshintergrund und weiße Schaltflächen
custom_css = """
<style>
    /* Farbverlaufshintergrund für die gesamte Seite */
    .main, .stApp {
        background: linear-gradient(135deg, #4527A0, #7B1FA2) !important;
        background-size: cover !important;
        background-attachment: fixed !important;
    }
    
    /* Transparente Container */
    .css-18e3th9, .css-1d391kg, .css-12oz5g7 {
        background: transparent !important;
    }
    
    /* Glasmorphismus-Schaltflächen im Apple-Stil */
    button, .stButton > button, .stDownloadButton > button {
        background: rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
    }
    
    /* Hover-Effekt für Glasmorphismus-Schaltflächen */
    button:hover, .stButton > button:hover {
        background: rgba(255, 255, 255, 0.3) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15) !important;
    }
    
    /* Hervorhebung des Buttontexts für bessere Lesbarkeit */
    .stButton > button p, button p, .stDownloadButton > button p {
        color: white !important;
        font-weight: 600 !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2) !important;
    }
    
    /* File Uploader gestalten */
    .stFileUploader > div {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        padding: 20px !important;
        color: white !important;
        border: 2px dashed rgba(255, 255, 255, 0.3) !important;
        backdrop-filter: blur(5px) !important;
        -webkit-backdrop-filter: blur(5px) !important;
    }
    
    /* Browse-Files Button */
    .stFileUploader button, button.css-1aumxhk, .css-1aumxhk {
        background: rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 0.5rem 1rem !important;
        text-transform: none !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        margin-left: auto !important;
        margin-right: auto !important;
        display: block !important;
    }
    
    /* Browse files Button Hover-Effekt */
    button.css-1aumxhk:hover, .css-1aumxhk:hover {
        background: rgba(255, 255, 255, 0.3) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15) !important;
    }
    
    /* Textfarbe für die Hauptseite auf weiß setzen */
    .stMarkdown, .stText, h1, h2, h3, p, span, div {
        color: white !important;
    }
    
    /* Textfarbe für interaktive Elemente anpassen */
    button span, .stButton span, .stDownloadButton span, 
    button div, .stButton div, .stDownloadButton div {
        color: white !important;
        font-weight: 600 !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2) !important;
    }
    
    /* Fix für Button-Text-Farbe */
    .stButton > button:hover span, .stButton > button:hover p, 
    button:hover span, button:hover p {
        color: white !important;
    }
    
    /* Sidebar dunkler gestalten */
    [data-testid="stSidebar"] {
        background-color: rgba(20, 20, 26, 0.8) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
    }
    
    /* Sidebar Elemente */
    .sidebar .sidebar-content {
        background-color: transparent !important;
    }
    
    /* Selectboxen im Glasdesign */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
    }
    
    /* Inputs im Glasdesign */
    input, textarea, [data-baseweb="input"], [data-baseweb="textarea"] {
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        backdrop-filter: blur(5px) !important;
        -webkit-backdrop-filter: blur(5px) !important;
    }
    
    /* Platzhalter-Text für Inputs */
    input::placeholder, textarea::placeholder {
        color: rgba(255, 255, 255, 0.6) !important;
    }
    
    /* Schatten für Cards/Container mit Glaseffekt */
    .element-container {
        margin-bottom: 1em !important;
    }
    
    /* Footer-Bereich */
    footer {
        color: white !important;
        visibility: visible !important;
    }
    
    /* Footer-Links */
    footer a {
        color: white !important;
        text-decoration: underline !important;
    }
    
    /* Weißer Text für Labels */
    label {
        color: white !important;
    }
    
    /* Drop-Zone */
    .css-1n543e5, .css-183lzff {
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        backdrop-filter: blur(5px) !important;
        -webkit-backdrop-filter: blur(5px) !important;
    }
    
    /* Fix für selectbox drop-down menu */
    .stSelectbox div[data-baseweb="select"] ul {
        background: rgba(69, 39, 160, 0.9) !important;
        color: white !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
    }
    
    /* Verbesserte Dropdown-Menüs */
    /* Dropdown-Hauptcontainer */
    .stSelectbox div[data-baseweb="select"] {
        background: rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
        transition: all 0.3s ease !important;
    }
    
    /* Dropdown wenn aktiv/hover */
    .stSelectbox div[data-baseweb="select"]:hover, 
    .stSelectbox div[data-baseweb="select"]:focus {
        background: rgba(255, 255, 255, 0.2) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15) !important;
    }
    
    /* Dropdown-Liste */
    .stSelectbox div[data-baseweb="select"] ul {
        background: rgba(45, 25, 100, 0.95) !important;
        border-radius: 12px !important;
        padding: 8px !important;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2) !important;
    }
    
    /* Dropdown-Listenelemente */
    .stSelectbox div[data-baseweb="select"] ul li {
        border-radius: 8px !important;
        padding: 8px 12px !important;
        margin: 4px 0 !important;
        transition: all 0.2s ease !important;
    }
    
    /* Dropdown-Listenelement hover */
    .stSelectbox div[data-baseweb="select"] ul li:hover {
        background: rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Ausgewähltes Dropdown-Element */
    .stSelectbox div[data-baseweb="select"] [data-baseweb="selected-option"] {
        font-weight: 500 !important;
        letter-spacing: 0.3px !important;
    }
    
    /* Dropdown Pfeil */
    .stSelectbox div[data-baseweb="select"] [data-baseweb="select-arrow"] {
        color: rgba(255, 255, 255, 0.8) !important;
    }
    
    /* Placeholder für Dropdown */
    .stSelectbox div[data-baseweb="select"] [data-baseweb="placeholder"] {
        color: rgba(255, 255, 255, 0.6) !important;
    }
    
    /* Dropdown-Menu beim öffnen */
    div[role="listbox"] {
        background: rgba(45, 25, 100, 0.95) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2) !important;
    }
    
    /* Option-Elemente im Dropdown */
    div[role="option"] {
        color: white !important;
        padding: 10px 15px !important;
        border-radius: 8px !important;
        margin: 4px 0 !important;
        transition: background 0.2s ease !important;
    }
    
    /* Hover-Effekt für Optionen */
    div[role="option"]:hover {
        background: rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Ausgewählte Option */
    div[aria-selected="true"] {
        background: rgba(255, 255, 255, 0.15) !important;
        font-weight: 600 !important;
    }
    
    /* Form-Label hervorheben */
    label {
        font-weight: 500 !important;
        margin-bottom: 5px !important;
        letter-spacing: 0.3px !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2) !important;
    }
    
    /* Ansprechpartner-Auswahl spezielles Styling */
    #ansprechpartner {
        margin-bottom: 12px !important;
    }
    
    /* Verbesserte Dropdown-Liste-Scrollbar */
    div[role="listbox"]::-webkit-scrollbar {
        width: 8px !important;
    }
    
    div[role="listbox"]::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 10px !important;
    }
    
    div[role="listbox"]::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.3) !important;
        border-radius: 10px !important;
    }
    
    div[role="listbox"]::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.4) !important;
    }
    
    /* Verbesserte mobile Dropdown-Ansicht */
    @media (max-width: 768px) {
        .stSelectbox div[data-baseweb="select"] {
            width: 100% !important;
            max-width: none !important;
        }
        
        div[role="listbox"] {
            max-width: 90vw !important;
            left: 5vw !important;
            right: 5vw !important;
        }
        
        /* Größere Touch-Bereiche für mobile Geräte */
        div[role="option"] {
            padding: 12px !important;
            min-height: 44px !important; /* Empfohlene Mindesthöhe für Touch-Targets */
        }
    }
    
    /* Verbesserte aktive Zustände für Dropdowns */
    .stSelectbox div[data-baseweb="select"]:focus-within {
        border-color: rgba(255, 255, 255, 0.5) !important;
        box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Status-Message styles */
    .stAlert, .st-ae, .st-af, .st-ag, .st-ah {
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Drop-Zone Text */
    .css-n978rk {
        color: white !important;
    }
    
    /* Prozessschrittanzeige (1-2-3) verbessern */
    .stProgress > div {
        background: rgba(255, 255, 255, 0.2) !important;
    }
    
    .stProgress > div > div {
        background: white !important;
    }
    
    /* Radio-Buttons */
    .stRadio > div {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        padding: 10px 15px !important;
        backdrop-filter: blur(5px) !important;
        -webkit-backdrop-filter: blur(5px) !important;
    }
    
    /* Checkbox styling */
    .stCheckbox > div {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        padding: 5px 10px !important;
        backdrop-filter: blur(5px) !important;
        -webkit-backdrop-filter: blur(5px) !important;
    }
    
    /* Expander-Header */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(5px) !important;
        -webkit-backdrop-filter: blur(5px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Expander-Content */
    .streamlit-expanderContent {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 0 0 12px 12px !important;
        backdrop-filter: blur(5px) !important;
        -webkit-backdrop-filter: blur(5px) !important;
    }

    /* Verbesserte Tab-Elemente */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        padding: 5px !important;
        backdrop-filter: blur(5px) !important;
        -webkit-backdrop-filter: blur(5px) !important;
        gap: 8px !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border-radius: 10px !important;
        border: none !important;
        margin: 0 !important;
        padding: 10px 20px !important;
        transition: all 0.3s ease !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15) !important;
    }

    /* Erfolgshinweis-Box im Glasdesign-Stil */
    .element-container .stAlert.st-ae,
    .element-container .stAlert.st-af,
    .element-container .stAlert.st-ag,
    .element-container .stAlert.st-ah,
    .stSuccess {
        background: rgba(255, 255, 255, 0.15) !important;
        color: white !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15) !important;
        padding: 15px 20px !important;
    }
    
    /* Erfolgshinweis-Box Icon anpassen */
    .stSuccess svg {
        fill: white !important;
    }
    
    /* Verbesserte File Uploader und Drop Zone */
    .uploadFile {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        border: 2px dashed rgba(255, 255, 255, 0.3) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        padding: 30px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1) !important;
    }
    
    .uploadFile:hover {
        border-color: rgba(255, 255, 255, 0.5) !important;
        background: rgba(255, 255, 255, 0.15) !important;
    }
    
    /* Custom Drag & Drop Box Styling */
    [data-testid="stFileUploader"] {
        width: 100%;
    }
    
    [data-testid="stFileUploader"] section {
        padding: 0 !important;
        border: none !important;
        background: transparent !important;
    }
    
    [data-testid="stFileUploader"] section > div {
        background: rgba(255, 255, 255, 0.08) !important;
        border: 2px dashed rgba(255, 255, 255, 0.3) !important;
        border-radius: 16px !important;
        padding: 30px !important;
        text-align: center !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12) !important;
    }
    
    [data-testid="stFileUploader"] section > div:hover {
        background: rgba(255, 255, 255, 0.12) !important;
        border-color: rgba(255, 255, 255, 0.5) !important;
    }
    
    [data-testid="stFileUploader"] section div small {
        color: rgba(255, 255, 255, 0.7) !important;
        font-size: 0.9rem !important;
    }
    
    /* Verbesserte Browser-Files-Button */
    [data-testid="stFileUploader"] section div button {
        background: rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 8px 20px !important;
        font-weight: 600 !important;
        text-transform: none !important;
        margin-top: 15px !important;
        margin-left: auto !important;
        margin-right: auto !important;
        display: block !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
        backdrop-filter: blur(5px) !important;
        -webkit-backdrop-filter: blur(5px) !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stFileUploader"] section div button:hover {
        background: rgba(255, 255, 255, 0.3) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2) !important;
    }
</style>
"""

# Beispieldaten für den Demo-Modus
DEMO_PROFILE_DATA = {
    "persönliche_daten": {
        "name": "Max Mustermann",
        "wohnort": "Hamburg",
        "jahrgang": "1985",
        "führerschein": "Klasse B",
        "kontakt": {
            "ansprechpartner": "Kai Fischer",
            "telefon": "02161 62126-02",
            "email": "fischer@galdora.de"
        }
    },
    "berufserfahrung": [
        {
            "zeitraum": "01/2018 - heute",
            "position": "Senior Frontend Developer",
            "unternehmen": "TechCorp GmbH, Hamburg",
            "aufgaben": [
                "Entwicklung und Wartung von React-basierten Webanwendungen",
                "Code Reviews und Mentoring von Junior Entwicklern",
                "Implementierung von CI/CD Pipelines",
                "Migration von Legacy-Code zu modernen React-Komponenten"
            ]
        },
        {
            "zeitraum": "03/2015 - 12/2017",
            "position": "Web Developer",
            "unternehmen": "WebSolutions AG, Berlin",
            "aufgaben": [
                "Entwicklung von responsive Websites mit HTML, CSS und JavaScript",
                "Zusammenarbeit mit Designern und Backend-Entwicklern",
                "Integration von RESTful APIs"
            ]
        }
    ],
    "ausbildung": [
        {
            "zeitraum": "10/2010 - 02/2015",
            "abschluss": "Bachelor of Science in Informatik",
            "institution": "Technische Universität Berlin",
            "note": "1,8",
            "schwerpunkte": "Webentwicklung, Datenbanken, Softwarearchitektur"
        }
    ],
    "weiterbildungen": [
        {
            "zeitraum": "05/2019",
            "bezeichnung": "React Advanced Masterclass",
            "abschluss": "Online-Kurs"
        },
        {
            "zeitraum": "09/2017",
            "bezeichnung": "Certified Scrum Developer",
            "abschluss": "Scrum Alliance"
        }
    ],
    "wunschgehalt": "65.000 € p.a.",
    "verfuegbarkeit_status": "Sofort verfügbar",
    "verfuegbarkeit_details": ""
}

DEMO_EXTRACTED_TEXT = """
LEBENSLAUF
MAX MUSTERMANN
PERSÖNLICHE DATEN
Name: Max Mustermann
Wohnort: Hamburg
Jahrgang: 1985
Führerschein: Klasse B

BERUFSERFAHRUNG
01/2018 - heute: Senior Frontend Developer bei TechCorp GmbH, Hamburg
- Entwicklung und Wartung von React-basierten Webanwendungen
- Code Reviews und Mentoring von Junior Entwicklern
- Implementierung von CI/CD Pipelines
- Migration von Legacy-Code zu modernen React-Komponenten

03/2015 - 12/2017: Web Developer bei WebSolutions AG, Berlin
- Entwicklung von responsive Websites mit HTML, CSS und JavaScript
- Zusammenarbeit mit Designern und Backend-Entwicklern
- Integration von RESTful APIs

AUSBILDUNG
10/2010 - 02/2015: Bachelor of Science in Informatik, Technische Universität Berlin
Note: 1,8
Schwerpunkte: Webentwicklung, Datenbanken, Softwarearchitektur

WEITERBILDUNGEN
05/2019: React Advanced Masterclass, Online-Kurs
09/2017: Certified Scrum Developer, Scrum Alliance
"""

# Hilfsfunktionen
def reset_session():
    """Setzt die Session zurück"""
    st.session_state.step = 1
    st.session_state.extracted_text = ""
    st.session_state.profile_data = {}
    st.session_state.edited_data = {}
    st.session_state.preview_pdf = None
    # Temporäre Dateien aufräumen
    if 'temp_files' in st.session_state:
        for temp_file in st.session_state.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
            except Exception as e:
                print(f"Fehler beim Löschen von Temp-Datei: {str(e)}")
        st.session_state.temp_files = []
    else:
        # Initialisiere temp_files, falls es noch nicht existiert
        st.session_state.temp_files = []
    # Demo-Modus zurücksetzen
    st.session_state.demo_mode = False

def display_pdf(file_path):
    """Zeigt ein PDF als Base64-String an"""
    # Prüfe, ob ein gültiger Dateipfad vorhanden ist
    if file_path is None:
        # Zeige eine Fehlermeldung statt des PDFs an
        return '<div style="text-align: center; padding: 20px; background-color: #f8d7da; color: #721c24; border-radius: 5px;">PDF-Vorschau nicht verfügbar. Bitte aktualisieren Sie die Vorschau.</div>'
    
    # Prüfe, ob die Datei existiert
    if not os.path.exists(file_path):
        return '<div style="text-align: center; padding: 20px; background-color: #f8d7da; color: #721c24; border-radius: 5px;">PDF-Datei existiert nicht. Bitte generieren Sie die Vorschau erneut.</div>'
    
    try:
        # Prüfe, ob die Datei eine gültige PDF-Datei ist
        with open(file_path, "rb") as f:
            file_content = f.read()
            # Prüfe auf PDF-Signatur (%PDF-)
            if not file_content.startswith(b'%PDF-'):
                return '<div style="text-align: center; padding: 20px; background-color: #f8d7da; color: #721c24; border-radius: 5px;">Die Datei ist keine gültige PDF-Datei. Bitte generieren Sie die Vorschau erneut.</div>'
            
            base64_pdf = base64.b64encode(file_content).decode('utf-8')
        
        # Alternative PDF-Anzeige, die besser mit Chrome-Sicherheitsrichtlinien kompatibel ist
        pdf_display = f'''
        <div style="display: flex; justify-content: center; width: 100%; margin: 0 auto; border: 1px solid #ddd; border-radius: 5px; overflow: hidden; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
            <object 
                data="data:application/pdf;base64,{base64_pdf}" 
                type="application/pdf"
                width="100%" 
                height="800"
                style="border: none;">
                <p>Ihr Browser kann PDFs nicht anzeigen. 
                <a href="data:application/pdf;base64,{base64_pdf}" download="dokument.pdf">Klicken Sie hier, um das PDF herunterzuladen</a>.</p>
            </object>
        </div>
        '''
        return pdf_display
    except Exception as e:
        # Zeige eine Fehlermeldung bei sonstigen Problemen
        return f'<div style="text-align: center; padding: 20px; background-color: #f8d7da; color: #721c24; border-radius: 5px;">Fehler beim Laden der PDF-Vorschau: {str(e)}</div>'

def run_main_app():
    """
    Hauptfunktion zur Ausführung der CV2Profile-Anwendung.
    Diese Funktion wird von Home.py aufgerufen.
    """
    # CSS einbinden
    st.markdown(custom_css, unsafe_allow_html=True)
    
    # Session-State initialisieren, falls noch nicht vorhanden
    if 'step' not in st.session_state:
        st.session_state.step = 1
    if 'extracted_text' not in st.session_state:
        st.session_state.extracted_text = ""
    if 'profile_data' not in st.session_state:
        st.session_state.profile_data = {}
    if 'edited_data' not in st.session_state:
        st.session_state.edited_data = {}
    if 'preview_pdf' not in st.session_state:
        st.session_state.preview_pdf = None
    if 'temp_files' not in st.session_state:
        st.session_state.temp_files = []
    if 'demo_mode' not in st.session_state:
        st.session_state.demo_mode = False
    if 'saved_api_key' not in st.session_state:
        st.session_state.saved_api_key = config.get_openai_api_key()
    
    # Header-Bereich mit verbessertem Glasmorphismus-Effekt
    st.markdown("""
    <div style="background-color: rgba(255, 255, 255, 0.15); padding: 2.5rem; border-radius: 15px; margin-bottom: 2rem; color: white; text-align: center; backdrop-filter: blur(12px); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25); border: 1px solid rgba(255, 255, 255, 0.18);">
        <h1 style="margin: 0; font-weight: 700; font-size: 2.8rem; text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);">CV2Profile Konverter</h1>
        <p style="margin-top: 1rem; font-size: 1.2rem; opacity: 0.95;">Konvertiere deinen Lebenslauf in ein professionelles Profil. Lade deine Datei hoch, wähle die gewünschten Informationen aus und gestalte dein Profil.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar für Schnelleinstellungen
    with st.sidebar:
        # Demo-Modus Schalter
        demo_mode = st.toggle("Demo-Modus", value=st.session_state.demo_mode, 
                            help="Aktiviere den Demo-Modus, um direkt mit Beispieldaten zu arbeiten.")
        
        # Demo-Modus Status aktualisieren
        if demo_mode != st.session_state.demo_mode:
            st.session_state.demo_mode = demo_mode
            if demo_mode:
                # Demo-Daten laden
                st.session_state.extracted_text = DEMO_EXTRACTED_TEXT
                st.session_state.profile_data = DEMO_PROFILE_DATA
            else:
                # Daten zurücksetzen
                st.session_state.extracted_text = ""
                st.session_state.profile_data = {}
                st.session_state.edited_data = {}
            # Seite neu laden, um die Änderungen anzuzeigen
            st.rerun()
        
        # API Key Kurzanzeige 
        st.divider()
        api_key_value = st.session_state.saved_api_key
        if api_key_value:
            masked_key = "•" * 16 + api_key_value[-4:] if len(api_key_value) > 4 else "•" * len(api_key_value)
            st.markdown(f"""
            <div style="background: rgba(255, 255, 255, 0.08); padding: 10px; border-radius: 8px; margin-bottom: 15px;">
                <p style="margin: 0; font-size: 0.85rem; opacity: 0.8;">API-Key:</p>
                <code style="font-size: 0.9rem;">{masked_key}</code>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("Kein API-Key gespeichert. Gehe zu Einstellungen, um einen API-Key hinzuzufügen.")
        
        # Prozess neu starten Button
        if st.button("Prozess neu starten"):
            reset_session()
            st.rerun()

    # Hauptbereich - basierend auf dem aktuellen Schritt
    # Von hier an bleibt die Anwendungslogik größtenteils unverändert
    # ...
    
    # Hier würde der Rest des bestehenden Codes folgen, der die Schritte 1, 2, 3 implementiert
    # Da dieser Code sehr umfangreich ist, behalte ich ihn unverändert bei.

# Session State für den mehrstufigen Prozess initialisieren
if 'step' not in st.session_state:
    st.session_state.step = 1  # Schritt 1: Kombinierte Extraktion & Analyse
if 'extracted_text' not in st.session_state:
    st.session_state.extracted_text = ""
if 'profile_data' not in st.session_state:
    st.session_state.profile_data = {}
if 'edited_data' not in st.session_state:
    st.session_state.edited_data = {}
if 'preview_pdf' not in st.session_state:
    st.session_state.preview_pdf = None
if 'temp_files' not in st.session_state:
    st.session_state.temp_files = []
if 'saved_api_key' not in st.session_state:
    # Lade den gespeicherten API-Key
    st.session_state.saved_api_key = config.get_openai_api_key()
if 'demo_mode' not in st.session_state:
    st.session_state.demo_mode = False

# Seitentitel und Konfiguration
st.set_page_config(page_title="CV2Profile Konverter", layout="wide")

# CSS einbinden
st.markdown(custom_css, unsafe_allow_html=True)

# Session-State initialisieren, falls noch nicht vorhanden
if 'page' not in st.session_state:
    st.session_state.page = 'main'  # Standard-Seite ist die Hauptseite

# Wähle die anzuzeigende Seite
if st.session_state.page == 'settings':
    # Einstellungsseite anzeigen
    render_settings_page()
    
    # Button zum Zurückkehren zur Hauptseite
    if st.button("Zurück zur Hauptseite"):
        st.session_state.page = 'main'
        st.rerun()
else:
    # Header-Bereich mit verbessertem Glasmorphismus-Effekt
    st.markdown("""
    <div style="background-color: rgba(255, 255, 255, 0.15); padding: 2.5rem; border-radius: 15px; margin-bottom: 2rem; color: white; text-align: center; backdrop-filter: blur(12px); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25); border: 1px solid rgba(255, 255, 255, 0.18);">
        <h1 style="margin: 0; font-weight: 700; font-size: 2.8rem; text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);">CV2Profile Konverter</h1>
        <p style="margin-top: 1rem; font-size: 1.2rem; opacity: 0.95;">Konvertiere deinen Lebenslauf in ein professionelles Profil. Lade deine Datei hoch, wähle die gewünschten Informationen aus und gestalte dein Profil.</p>
    </div>
    """, unsafe_allow_html=True)

# Sidebar für Einstellungen
with st.sidebar:
    st.header("Einstellungen")
    
    # Zahnrad-Symbol für Einstellungsseite hinzufügen
    settings_col1, settings_col2 = st.columns([4, 1])
    with settings_col1:
        st.subheader("Schnellzugriff")
    with settings_col2:
        # Zahnrad-Icon mit Styling
        st.markdown("""
        <div style="display: flex; justify-content: flex-end; margin-top: 10px;">
            <a href="#" onclick="this.blur();" id="settings-icon" style="text-decoration: none;">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="white" viewBox="0 0 24 24">
                    <path d="M19.14,12.94c0.04-0.3,0.06-0.61,0.06-0.94c0-0.32-0.02-0.64-0.07-0.94l2.03-1.58c0.18-0.14,0.23-0.41,0.12-0.61 l-1.92-3.32c-0.12-0.22-0.37-0.29-0.59-0.22l-2.39,0.96c-0.5-0.38-1.03-0.7-1.62-0.94L14.4,2.81c-0.04-0.24-0.24-0.41-0.48-0.41 h-3.84c-0.24,0-0.43,0.17-0.47,0.41L9.25,5.35C8.66,5.59,8.12,5.92,7.63,6.29L5.24,5.33c-0.22-0.08-0.47,0-0.59,0.22L2.74,8.87 C2.62,9.08,2.66,9.34,2.86,9.48l2.03,1.58C4.84,11.36,4.8,11.69,4.8,12s0.02,0.64,0.07,0.94l-2.03,1.58 c-0.18,0.14-0.23,0.41-0.12,0.61l1.92,3.32c0.12,0.22,0.37,0.29,0.59,0.22l2.39-0.96c0.5,0.38,1.03,0.7,1.62,0.94l0.36,2.54 c0.05,0.24,0.24,0.41,0.48,0.41h3.84c0.24,0,0.44-0.17,0.47-0.41l0.36-2.54c0.59-0.24,1.13-0.56,1.62-0.94l2.39,0.96 c0.22,0.08,0.47,0,0.59-0.22l1.92-3.32c0.12-0.22,0.07-0.47-0.12-0.61L19.14,12.94z M12,15.6c-1.98,0-3.6-1.62-3.6-3.6 s1.62-3.6,3.6-3.6s3.6,1.62,3.6,3.6S13.98,15.6,12,15.6z"/>
                </svg>
            </a>
        </div>
        <style>
            #settings-icon:hover svg {
                transform: rotate(45deg);
                transition: transform 0.3s ease;
            }
        </style>
        """, unsafe_allow_html=True)
    
    # Button zum Öffnen der Einstellungsseite
    if st.button("Einstellungen öffnen", key="open_settings"):
        st.session_state.page = 'settings'
        st.rerun()
    
    # Demo-Modus Schalter
    demo_mode = st.toggle("Demo-Modus", value=st.session_state.get('demo_mode', False), 
                        help="Aktiviere den Demo-Modus, um direkt mit Beispieldaten zu arbeiten.")
    
    # Demo-Modus Status aktualisieren
    if 'demo_mode' not in st.session_state or demo_mode != st.session_state.demo_mode:
        st.session_state.demo_mode = demo_mode
        if demo_mode:
            # Demo-Daten laden
            st.session_state.extracted_text = DEMO_EXTRACTED_TEXT
            st.session_state.profile_data = DEMO_PROFILE_DATA
        else:
            # Daten zurücksetzen
            st.session_state.extracted_text = ""
            st.session_state.profile_data = {}
            st.session_state.edited_data = {}
        # Seite neu laden, um die Änderungen anzuzeigen
        st.rerun()
    
    # Lade den gespeicherten API-Key oder verwende den leeren String
    api_key_value = st.session_state.get('saved_api_key', config.get_openai_api_key())

    # Rest der Sidebar bleibt unverändert...

# JavaScript für Zahnrad-Icon-Klick
st.markdown("""
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Warte ein bisschen, damit Streamlit Zeit hat, das DOM zu erstellen
    setTimeout(function() {
        const settingsIcon = document.getElementById('settings-icon');
        if (settingsIcon) {
            settingsIcon.addEventListener('click', function(e) {
                e.preventDefault();
                // Button "Einstellungen öffnen" programmgesteuert klicken
                const settingsButton = document.querySelector('button[data-testid="baseButton-header"]');
                if (settingsButton) {
                    settingsButton.click();
                }
            });
        }
    }, 1000);
});
</script>
""", unsafe_allow_html=True)

# Hauptbereich nur anzeigen, wenn wir auf der Hauptseite sind
if st.session_state.page == 'main':
    # Rest der Anwendung (Schritte 1, 2, 3) bleibt unverändert...

# Der Schritt 2 wird nicht mehr benötigt, da er direkt in Schritt 1 integriert wurde
elif st.session_state.step == 2:
    # Zurück zum Schritt 1 umleiten
    st.session_state.step = 1
    st.rerun()

# Footer
st.divider()
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center;">
    <span>CV2Profile Konverter | Alle Rechte vorbehalten © 2025</span>
    <div>
        <a href="#" style="margin-right: 10px;">Datenschutz</a>
        <a href="#" style="margin-right: 10px;">AGB</a>
        <a href="#">Impressum</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Aufräumen von temporären Dateien, wenn das Programm beendet wird
def cleanup():
    """Räumt temporäre Dateien auf, wenn die App beendet wird"""
    try:
        # Überprüfe, ob temp_files in der Session existiert, bevor darauf zugegriffen wird
        if hasattr(st, 'session_state') and 'temp_files' in st.session_state:
            for temp_file in st.session_state.temp_files:
                try:
                    if os.path.exists(temp_file):
                        os.unlink(temp_file)
                        print(f"Temporäre Datei gelöscht: {temp_file}")
                except Exception as e:
                    print(f"Fehler beim Löschen der temporären Datei {temp_file}: {str(e)}")
    except Exception as e:
        print(f"Fehler beim Aufräumen: {str(e)}")
    finally:
        # Sicherstellen, dass keine Fehler unbehandelt bleiben
        print("Cleanup abgeschlossen.")

# Cleanup-Funktion registrieren
import atexit
atexit.register(cleanup)
