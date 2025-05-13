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
import atexit

# Füge den übergeordneten Ordner zum Pythonpfad hinzu, um relative Importe zu ermöglichen
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Importe aus den reorganisierten Modulen
from src.core.document_processor import DocumentProcessor
from src.core.ai_extractor import AIExtractor
from src.core.combined_processor import CombinedProcessor
from src.templates.template_generator import ProfileGenerator
import src.utils.config as config  # Importiere das Konfigurationsmodul
from src.utils.image_utils import get_image_path, ensure_images_in_static  # Importiere die Bild-Utilities

# Function to load and convert the logo to base64
def get_logo_as_base64():
    """Load and convert the logo to base64 for embedding in HTML"""
    try:
        # Make sure all images are available in the static directory for HTTPS compatibility
        ensure_images_in_static()
        
        # Try to find the logo using our image utility
        # For HTTPS compatibility, use_static=True
        logo_path = get_image_path('cv2profile-loho.png', use_static=True)
        
        # Fallback locations if the first path doesn't exist
        if not os.path.exists(logo_path):
            logo_path = get_image_path('Galdoralogo.png', use_static=True)
        
        if not os.path.exists(logo_path):
            # Final fallback: return an empty string if no logo is found
            return ""
        
        with open(logo_path, "rb") as f:
            logo_data = f.read()
            return base64.b64encode(logo_data).decode("utf-8")
    except Exception as e:
        print(f"Error loading logo: {e}")
        return ""

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
    "wunschgehalt": "65.000 € p.a."
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

# Seitentitel und Konfiguration
st.set_page_config(page_title="CV2Profile Konverter", layout="wide")

# Stelle sicher, dass alle Bilder im static-Verzeichnis verfügbar sind für HTTPS-Kompatibilität
ensure_images_in_static()

# CSS einbinden
st.markdown(custom_css, unsafe_allow_html=True)

# Header-Bereich mit verbessertem Glasmorphismus-Effekt
st.markdown("""
<div style="background-color: rgba(255, 255, 255, 0.15); padding: 2.5rem; border-radius: 15px; margin-bottom: 2rem; color: white; text-align: center; backdrop-filter: blur(12px); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25); border: 1px solid rgba(255, 255, 255, 0.18);">
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
        <img src="data:image/png;base64,{}" alt="CV2Profile Logo" style="max-width: 200px; margin-bottom: 1.5rem;">
        <h1 style="margin: 0; font-weight: 700; font-size: 2.8rem; text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);">CV2Profile Konverter</h1>
        <p style="margin-top: 1rem; font-size: 1.2rem; opacity: 0.95;">Konvertiere deinen Lebenslauf in ein professionelles Profil. Lade deine Datei hoch, wähle die gewünschten Informationen aus und gestalte dein Profil.</p>
    </div>
</div>
""".format(get_logo_as_base64()), unsafe_allow_html=True)

# Sidebar für Einstellungen
with st.sidebar:
    st.header("Einstellungen")
    
    # Link zur Einstellungsseite
    st.markdown("""
    <a href="/01_Settings" target="_self" style="text-decoration: none;">
        <div style="background: rgba(255, 255, 255, 0.15); padding: 10px 15px; border-radius: 12px; margin-bottom: 20px; display: flex; align-items: center; backdrop-filter: blur(5px); -webkit-backdrop-filter: blur(5px); border: 1px solid rgba(255, 255, 255, 0.1);">
            <span style="font-size: 24px; margin-right: 10px;">⚙️</span>
            <span style="color: white; font-weight: 500;">Einstellungen öffnen</span>
        </div>
    </a>
    """, unsafe_allow_html=True)
    
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
    
    # Lade den gespeicherten API-Key oder verwende den leeren String
    api_key_value = st.session_state.saved_api_key

    # API-Key Eingabefeld
    api_key_input = st.text_input("OpenAI API Key", 
                                 value=api_key_value,
                                 type="password",
                                 help="Dein OpenAI API-Key wird benötigt, um Lebensläufe zu analysieren.",
                                 disabled=st.session_state.demo_mode)

    # Option zum Speichern des API-Keys (nur wenn nicht im Demo-Modus)
    if api_key_input and not st.session_state.demo_mode:
        if api_key_input != st.session_state.saved_api_key:
            save_key = st.checkbox("API-Key für zukünftige Sitzungen speichern", value=True,
                                  help="Der API-Key wird lokal auf deinem Computer gespeichert.")
            
            if save_key and st.button("API-Key speichern"):
                # Speichere den API-Key
                config.save_openai_api_key(api_key_input)
                st.session_state.saved_api_key = api_key_input
                st.success("API-Key erfolgreich gespeichert!")

    # Zeige Warnung an, wenn kein API-Key vorhanden ist und nicht im Demo-Modus
    if not api_key_input and not st.session_state.demo_mode:
        st.warning("Bitte gib deinen OpenAI API Key ein")
    elif st.session_state.demo_mode:
        st.info("Im Demo-Modus wird kein OpenAI API Key benötigt")
    
    # Allgemeine Einstellungen
    st.divider()
    all_settings = config.get_all_settings()
    
    # Template-Auswahl als Voreinstellung
    st.subheader("Voreinstellungen")
    template_options = {
        "professional": "Professionell", 
        "classic": "Klassisch", 
        "modern": "Modern", 
        "minimalist": "Minimalistisch"
    }
    default_template = all_settings.get("default_template", "professional")
    selected_template = st.selectbox(
        "Standard-Vorlage",
        options=list(template_options.keys()),
        format_func=lambda x: template_options[x],
        index=list(template_options.keys()).index(default_template),
        key="template_select"
    )
    
    # Speichere die Template-Voreinstellung, wenn sie sich geändert hat
    if selected_template != default_template:
        config.update_setting("default_template", selected_template)
    
    # Einstellung zum Anzeigen des extrahierten Textes
    show_text_default = all_settings.get("show_extracted_text", False)
    show_text_setting = st.checkbox(
        "Extrahierten Text standardmäßig anzeigen", 
        value=show_text_default
    )
    
    # Speichere die Textanzeige-Einstellung, wenn sie sich geändert hat
    if show_text_setting != show_text_default:
        config.update_setting("show_extracted_text", show_text_setting)
    
    # Cache-Management in die Seitenleiste verschoben
    st.divider()
    st.subheader("Performance")

    if st.button("Cache leeren"):
        import shutil
        import tempfile
        cache_dir = os.path.join(tempfile.gettempdir(), 'parser_cache')
        if os.path.exists(cache_dir):
            try:
                shutil.rmtree(cache_dir)
                os.makedirs(cache_dir, exist_ok=True)
                st.success("Cache erfolgreich geleert")
            except Exception as e:
                st.error(f"Fehler beim Leeren des Caches: {str(e)}")

    st.divider()
    st.markdown("### Über diese App")
    st.markdown("""
    Diese App extrahiert Daten aus Lebensläufen (PDF, JPEG, PNG, DOCX) 
    und erstellt daraus standardisierte Profile.
    """)
    
    if st.button("Prozess neu starten"):
        reset_session()
        st.rerun()

# Verwende den gespeicherten API-Key oder den eingegebenen API-Key
openai_api_key = api_key_input or st.session_state.saved_api_key

# Hauptbereich - basierend auf dem aktuellen Schritt
if st.session_state.step == 1:
    # Schritt 1: Datei hochladen und Text extrahieren/analysieren
    st.subheader("1. Lebenslauf hochladen und verarbeiten")
    
    # Wenn Demo-Modus aktiv ist
    if st.session_state.demo_mode:
        # Banner anzeigen, dass Demo-Modus aktiv ist
        st.info("🚀 Demo-Modus ist aktiv. Keine API-Schlüssel oder Datei-Upload erforderlich.")
        
        # Profildaten und extrahierten Text aus den vordefinierten Demo-Daten setzen
        profile_data = DEMO_PROFILE_DATA
        extracted_text = DEMO_EXTRACTED_TEXT
        
        # Erfolgsmeldung nach der "Analyse" anzeigen
        st.success("Der Lebenslauf wurde erfolgreich analysiert!")
        
        # Springe zu Schritt 2
        st.subheader("2. Profil erstellen und exportieren")

        # Profildaten aus der Session holen
        edited_data = {}

        # Zwei Tabs erstellen für Informationsauswahl und Profil-Generierung mit verbessertem Stil
        st.markdown("""
        <style>
            .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
                background-color: rgba(255, 255, 255, 0.2) !important;
                color: white !important;
                font-weight: 600 !important;
            }
            .stTabs [data-baseweb="tab-list"] button {
                padding: 10px 20px !important;
            }
        </style>
        """, unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["Informationen bearbeiten", "Profil exportieren"])

        with tab1:
            # Persönliche Daten
            st.markdown("### Persönliche Daten")
            personal_data = profile_data.get("persönliche_daten", {})
            
            # Name und Grunddaten
            col1, col2, col3 = st.columns(3)
            with col1:
                edited_data["name"] = st.text_input("Name", value=personal_data.get("name", ""), key="name_input_normal")
            with col2:
                edited_data["wohnort"] = st.text_input("Wohnort", value=personal_data.get("wohnort", ""), key="wohnort_input_normal")
            with col3:
                edited_data["jahrgang"] = st.text_input("Jahrgang", value=personal_data.get("jahrgang", ""), key="jahrgang_input_normal")
            
            # Profilbild-Upload hinzufügen
            st.markdown("### Profilbild")
            st.markdown("Laden Sie optional ein Profilbild hoch (JPG, PNG):")
            
            # Profilbild-Upload
            profile_image = st.file_uploader("Profilbild hochladen", 
                                             type=["jpg", "jpeg", "png"], 
                                             key="profile_image_uploader_normal")
            
            # Bild anzeigen und in Session speichern, wenn hochgeladen
            if profile_image is not None:
                # Bild anzeigen
                st.image(profile_image, width=150, caption="Vorschau des Profilbilds")
                
                # Bild in Session speichern
                if 'profile_image' not in st.session_state or st.session_state.profile_image != profile_image:
                    # Temporäre Datei für das Bild erstellen
                    img_extension = os.path.splitext(profile_image.name)[1].lower()
                    with tempfile.NamedTemporaryFile(delete=False, suffix=img_extension) as tmp_file:
                        tmp_file.write(profile_image.getbuffer())
                        img_path = tmp_file.name
                        st.session_state.profile_image_path = img_path
                        st.session_state.temp_files.append(img_path)
                        st.session_state.profile_image = profile_image
            
            # Führerschein und Wunschgehalt
            col1, col2 = st.columns(2)
            with col1:
                edited_data["führerschein"] = st.text_input("Führerschein", value=personal_data.get("führerschein", ""), key="fuehrerschein_input_normal")
            with col2:
                edited_data["wunschgehalt"] = st.text_input("Wunschgehalt", value=profile_data.get("wunschgehalt", ""), key="gehalt_input_normal")
            
            # Verfügbarkeit des Bewerbers
            st.markdown("### Verfügbarkeit")
            # Dropdown für Verfügbarkeitsstatus
            verfuegbarkeit_optionen = [
                "Sofort verfügbar",
                "Kündigungsfrist 1 Monat",
                "Kündigungsfrist 2 Monate",
                "Kündigungsfrist 3 Monate",
                "Derzeit nicht verfügbar",
                "Verfügbar mit Einschränkungen"
            ]
            
            verfuegbarkeit_status = st.selectbox(
                "Verfügbarkeitsstatus",
                options=verfuegbarkeit_optionen,
                index=0,
                key="verfuegbarkeit_status"
            )
            
            # Zusätzliche Details zur Verfügbarkeit
            verfuegbarkeit_details = st.text_area(
                "Details zur Verfügbarkeit (optional)",
                value=profile_data.get("verfuegbarkeit_details", ""),
                help="Z.B. gesundheitliche Einschränkungen, spezielle Umstände, genaues Datum der Verfügbarkeit",
                key="verfuegbarkeit_details"
            )
            
            # Verfügbarkeitsdaten speichern
            edited_data["verfuegbarkeit_status"] = verfuegbarkeit_status
            edited_data["verfuegbarkeit_details"] = verfuegbarkeit_details

            # Kontaktinformationen
            st.markdown("### Kontaktinformationen")
            kontakt = personal_data.get("kontakt", {})
            
            # Ansprechpartner-Dropdown
            ansprechpartner_options = [
                "Kai Fischer", 
                "Melike Demirkol", 
                "Konrad Ruszyk", 
                "Alessandro Böhm", 
                "Salim Alizai"
            ]
            
            # Vorauswahl des Ansprechpartners (falls vorhanden)
            current_ansprechpartner = kontakt.get("ansprechpartner", "")
            default_index = 0
            if current_ansprechpartner in ansprechpartner_options:
                default_index = ansprechpartner_options.index(current_ansprechpartner)
            
            # Ansprechpartner auswählen
            col1, col2, col3 = st.columns(3)
            with col1:
                selected_ansprechpartner = st.selectbox(
                    "Ansprechpartner",
                    options=ansprechpartner_options,
                    index=default_index,
                    key="ansprechpartner_demo"
                )
                edited_data["ansprechpartner"] = selected_ansprechpartner
                
                # E-Mail-Adresse basierend auf dem Nachnamen generieren
                nachname = selected_ansprechpartner.split()[-1]
                email = f"{nachname.lower()}@galdora.de"
                edited_data["email"] = email
            
            with col2:
                # Telefonnummer ist für alle Ansprechpartner gleich
                telefon = "02161 62126-02"
                edited_data["telefon"] = st.text_input("Telefon", value=telefon, disabled=True)
            
            with col3:
                # E-Mail-Adresse anzeigen
                st.text_input("E-Mail", value=email, disabled=True)
            
            # Berufserfahrung
            st.markdown("### Berufserfahrung")
            
            # Liste für editierte Berufserfahrungen
            edited_experience = []
            
            for idx, erfahrung in enumerate(profile_data.get("berufserfahrung", [])):
                with st.expander(f"{erfahrung.get('zeitraum', 'Neue Erfahrung')}: {erfahrung.get('position', '')} bei {erfahrung.get('unternehmen', '')}", expanded=False):
                    exp_data = {}
                    col1, col2 = st.columns(2)
                    with col1:
                        exp_data["zeitraum"] = st.text_input(f"Zeitraum #{idx+1}", value=erfahrung.get("zeitraum", ""), key=f"zeit_demo_{idx}")
                        exp_data["unternehmen"] = st.text_input(f"Unternehmen #{idx+1}", value=erfahrung.get("unternehmen", ""), key=f"unternehmen_demo_{idx}")
                    with col2:
                        exp_data["position"] = st.text_input(f"Position #{idx+1}", value=erfahrung.get("position", ""), key=f"position_demo_{idx}")
                    
                    # Aufgaben als Textarea mit einer Aufgabe pro Zeile
                    aufgaben_text = "\n".join(erfahrung.get("aufgaben", []))
                    new_aufgaben = st.text_area(
                        f"Aufgaben #{idx+1} (eine Aufgabe pro Zeile)", 
                        value=aufgaben_text,
                        height=150,
                        key=f"aufgaben_demo_{idx}"
                    )
                    # Aufgaben zurück in eine Liste konvertieren
                    exp_data["aufgaben"] = [task.strip() for task in new_aufgaben.split("\n") if task.strip()]
                    
                    # Option zum Löschen dieser Berufserfahrung
                    include = st.checkbox(f"Diese Berufserfahrung einbeziehen", value=True, key=f"exp_demo_{idx}")
                    if include:
                        edited_experience.append(exp_data)
            
            # Button zum Hinzufügen einer neuen Berufserfahrung
            if st.button("+ Neue Berufserfahrung hinzufügen", key="add_exp_demo"):
                with st.expander("Neue Berufserfahrung", expanded=True):
                    new_exp = {}
                    col1, col2 = st.columns(2)
                    with col1:
                        new_exp["zeitraum"] = st.text_input("Zeitraum (neu)", key="new_zeit_demo")
                        new_exp["unternehmen"] = st.text_input("Unternehmen (neu)", key="new_unternehmen_demo")
                    with col2:
                        new_exp["position"] = st.text_input("Position (neu)", key="new_position_demo")
                        
                        new_aufgaben = st.text_area(
                            "Aufgaben (eine Aufgabe pro Zeile)", 
                            height=150,
                            key="new_aufgaben_demo"
                        )
                        new_exp["aufgaben"] = [task.strip() for task in new_aufgaben.split("\n") if task.strip()]
                        
                        if st.button("Berufserfahrung hinzufügen", key="save_exp_demo"):
                            edited_experience.append(new_exp)
            
            # Ausbildung
            st.markdown("### Ausbildung")
            
            # Liste für editierte Ausbildungen
            edited_education = []
            
            for idx, ausbildung in enumerate(profile_data.get("ausbildung", [])):
                with st.expander(f"{ausbildung.get('zeitraum', 'Neue Ausbildung')}: {ausbildung.get('abschluss', '')} - {ausbildung.get('institution', '')}", expanded=False):
                    edu_data = {}
                    col1, col2 = st.columns(2)
                    with col1:
                        edu_data["zeitraum"] = st.text_input(f"Zeitraum (Ausbildung) #{idx+1}", value=ausbildung.get("zeitraum", ""), key=f"edu_zeit_demo_{idx}")
                        edu_data["institution"] = st.text_input(f"Institution #{idx+1}", value=ausbildung.get("institution", ""), key=f"institution_demo_{idx}")
                    with col2:
                        edu_data["abschluss"] = st.text_input(f"Abschluss #{idx+1}", value=ausbildung.get("abschluss", ""), key=f"abschluss_demo_{idx}")
                        edu_data["note"] = st.text_input(f"Note #{idx+1}", value=ausbildung.get("note", ""), key=f"note_demo_{idx}")
                    
                    edu_data["schwerpunkte"] = st.text_input(f"Studienschwerpunkte #{idx+1}", value=ausbildung.get("schwerpunkte", ""), key=f"schwerpunkte_demo_{idx}")
                    
                    # Option zum Löschen dieser Ausbildung
                    include = st.checkbox(f"Diese Ausbildung einbeziehen", value=True, key=f"edu_demo_{idx}")
                    if include:
                        edited_education.append(edu_data)
            
            # Button zum Hinzufügen einer neuen Ausbildung
            if st.button("+ Neue Ausbildung hinzufügen", key="add_edu_demo"):
                with st.expander("Neue Ausbildung", expanded=True):
                    new_edu = {}
                    col1, col2 = st.columns(2)
                    with col1:
                        new_edu["zeitraum"] = st.text_input("Zeitraum (Ausbildung neu)", key="new_edu_zeit_demo")
                        new_edu["institution"] = st.text_input("Institution (neu)", key="new_institution_demo")
                    with col2:
                        new_edu["abschluss"] = st.text_input("Abschluss (neu)", key="new_abschluss_demo")
                        new_edu["note"] = st.text_input("Note (neu)", key="new_note_demo")
                    
                        new_edu["schwerpunkte"] = st.text_input("Studienschwerpunkte (neu)", key="new_schwerpunkte_demo")
                        
                        if st.button("Ausbildung hinzufügen", key="save_edu_demo"):
                            edited_education.append(new_edu)
            
            # Weiterbildung
            st.markdown("### Weiterbildung")
            
            # Liste für editierte Weiterbildungen
            edited_training = []
            
            for idx, weiterbildung in enumerate(profile_data.get("weiterbildungen", [])):
                with st.expander(f"{weiterbildung.get('zeitraum', 'Neue Weiterbildung')}: {weiterbildung.get('bezeichnung', '')}", expanded=False):
                    training_data = {}
                    col1, col2 = st.columns(2)
                    with col1:
                        training_data["zeitraum"] = st.text_input(f"Zeitraum (Weiterbildung) #{idx+1}", value=weiterbildung.get("zeitraum", ""), key=f"weiter_zeit_demo_{idx}")
                    with col2:
                        training_data["bezeichnung"] = st.text_input(f"Bezeichnung #{idx+1}", value=weiterbildung.get("bezeichnung", ""), key=f"bezeichnung_demo_{idx}")
                    
                    training_data["abschluss"] = st.text_input(f"Abschluss (Weiterbildung) #{idx+1}", value=weiterbildung.get("abschluss", ""), key=f"weiter_abschluss_demo_{idx}")
                    
                    # Option zum Löschen dieser Weiterbildung
                    include = st.checkbox(f"Diese Weiterbildung einbeziehen", value=True, key=f"train_demo_{idx}")
                    if include:
                        edited_training.append(training_data)
            
            # Button zum Hinzufügen einer neuen Weiterbildung
            if st.button("+ Neue Weiterbildung hinzufügen", key="add_weiter_demo"):
                with st.expander("Neue Weiterbildung", expanded=True):
                    new_training = {}
                    col1, col2 = st.columns(2)
                    with col1:
                        new_training["zeitraum"] = st.text_input("Zeitraum (Weiterbildung neu)", key="new_weiter_zeit_demo")
                    with col2:
                        new_training["bezeichnung"] = st.text_input("Bezeichnung (neu)", key="new_bezeichnung_demo")
                    
                    new_training["abschluss"] = st.text_input("Abschluss (Weiterbildung neu)", key="new_weiter_abschluss_demo")
                    
                    if st.button("Weiterbildung hinzufügen", key="save_weiter_demo"):
                        edited_training.append(new_training)

                                    # Zusammenführen der bearbeiteten Daten
                        complete_edited_data = {
                            "persönliche_daten": {
                                "name": edited_data.get("name", ""),
                                "wohnort": edited_data.get("wohnort", ""),
                                "jahrgang": edited_data.get("jahrgang", ""),
                                "führerschein": edited_data.get("führerschein", ""),
                                "kontakt": {
                                    "ansprechpartner": edited_data.get("ansprechpartner", ""),
                                    "telefon": edited_data.get("telefon", ""),
                                    "email": edited_data.get("email", "")
                                },
                                "profile_image": st.session_state.get("profile_image_path", None)
                            },
                "berufserfahrung": edited_experience,
                "ausbildung": edited_education,
                "weiterbildungen": edited_training,
                "wunschgehalt": edited_data.get("wunschgehalt", ""),
                "verfuegbarkeit_status": edited_data.get("verfuegbarkeit_status", "Sofort verfügbar"),
                "verfuegbarkeit_details": edited_data.get("verfuegbarkeit_details", "")
            }
            
            # Speichern der bearbeiteten Daten in der Session
            st.session_state.edited_data = complete_edited_data
            
            # Prüfen auf Vollständigkeit der kritischen Daten
            validation_errors = []
            if not edited_data.get("name"):
                validation_errors.append("Name fehlt")
            if not edited_data.get("email") and not edited_data.get("telefon"):
                validation_errors.append("Mindestens eine Kontaktmöglichkeit (E-Mail oder Telefon) wird benötigt")
            
            # Wenn es Validierungsfehler gibt, diese anzeigen
            if validation_errors:
                for error in validation_errors:
                    st.error(error)

        with tab2:
            # Profil generieren und Vorschau anzeigen
            st.markdown("### Profilvorschau und Export")
            
            # Profildaten aus der Session holen oder aus den aktuellen bearbeiteten Daten
            edited_data_to_use = st.session_state.edited_data if "edited_data" in st.session_state else complete_edited_data
            
            # Vorlage auswählen
            st.markdown("#### Vorlage auswählen")
            
            # Standard-Vorlage aus der Konfiguration holen
            default_template = config.get_all_settings().get("default_template", "professional")
            
            # Template-Auswahl als Variable speichern
            template_to_use = default_template
            
            # Vorlagenauswahl mit Standard-Voreinstellung
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                classic = st.button("🔵 🔵\nKlassisch", 
                                    use_container_width=True, 
                                    type="primary" if default_template == "classic" else "secondary",
                                    key="classic_demo")
                if classic:
                    template_to_use = "classic"
                    # Automatisch Vorschau aktualisieren, wenn Template geändert wird
                    st.session_state.update_preview = True
                    
            with col2:
                modern = st.button("🟢 🟢\nModern", 
                                use_container_width=True,
                                type="primary" if default_template == "modern" else "secondary",
                                key="modern_demo")
                if modern:
                    template_to_use = "modern"
                    # Automatisch Vorschau aktualisieren, wenn Template geändert wird
                    st.session_state.update_preview = True
                    
            with col3:
                professional = st.button("🟣 🟣\nProfessionell", 
                                    use_container_width=True,
                                    type="primary" if default_template == "professional" else "secondary",
                                    key="professional_demo")
                if professional:
                    template_to_use = "professional"
                    # Automatisch Vorschau aktualisieren, wenn Template geändert wird
                    st.session_state.update_preview = True
                    
            with col4:
                minimalistic = st.button("⚫ ⚫\nMinimalistisch", 
                                    use_container_width=True,
                                    type="primary" if default_template == "minimalist" else "secondary",
                                    key="minimalistic_demo")
                if minimalistic:
                    template_to_use = "minimalist"
                    # Automatisch Vorschau aktualisieren, wenn Template geändert wird
                    st.session_state.update_preview = True
            
                        # Profil-Vorschau generieren und anzeigen
            if 'preview_pdf' not in st.session_state or st.button("Vorschau aktualisieren", key="update_preview_demo") or st.session_state.get('update_preview', False):
                # Reset des Update-Flags
                st.session_state.update_preview = False
                with st.spinner("Profil wird generiert..."):
                    try:
                        generator = ProfileGenerator()
                        output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                        output_path = output_file.name
                        output_file.close()
                        st.session_state.temp_files.append(output_path)
                        
                        # Generiere Profil mit dem ausgewählten Template
                        profile_path = generator.generate_profile(edited_data_to_use, output_path, template=template_to_use)
                        st.session_state.preview_pdf = profile_path
                        
                        # Zeige eine Erfolgsmeldung an
                        st.success("Profil erfolgreich generiert!")
                        
                        # Speichere das ausgewählte Template für zukünftige Aktualisierungen
                        st.session_state.selected_template = template_to_use
                    except Exception as e:
                        st.error(f"Fehler bei der Generierung des Profils: {str(e)}")
            
            # PDF-Vorschau anzeigen
            if "preview_pdf" in st.session_state:
                st.markdown("#### Profil-Vorschau")
                pdf_display = display_pdf(st.session_state.preview_pdf)
                st.markdown(pdf_display, unsafe_allow_html=True)
                
                # Name für das Profil
                name = edited_data_to_use["persönliche_daten"]["name"].replace(" ", "_")
                if not name or name == "":
                    name = "Profil"
                
                # Auswahl des Formats mit RadioButtons
                st.markdown("#### Format wählen")
                format_option = st.radio(
                    "In welchem Format möchten Sie das Profil herunterladen?",
                    options=["PDF", "Word"],
                    horizontal=True,
                    key="format_choice_demo"
                )
                
                # Je nach Auswahl unterschiedlichen Download-Button anzeigen
                if format_option == "PDF":
                    # PDF-Download
                    if st.session_state.preview_pdf and os.path.exists(st.session_state.preview_pdf):
                        with open(st.session_state.preview_pdf, "rb") as file:
                            st.download_button(
                                label="Profil herunterladen",
                                data=file,
                                file_name=f"{name}_Profil.pdf",
                                mime="application/pdf",
                                key="download_pdf_demo"
                            )
                    else:
                        st.error("Bitte generieren Sie zuerst eine Vorschau des Profils.")
                else:
                    # Word-Dokument generieren und herunterladen
                    # Temporäre Datei für das Word-Dokument erstellen
                    output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
                    output_path = output_file.name
                    output_file.close()
                    st.session_state.temp_files.append(output_path)
                    
                    try:
                        # Word-Dokument mit dem gleichen Generator erstellen
                        docx_path = generator.generate_profile(
                            edited_data_to_use, 
                            output_path, 
                            template=template_to_use,
                            format="docx"
                        )
                        
                        # Word-Dokument zum Download anbieten
                        with open(docx_path, "rb") as file:
                            st.download_button(
                                label="Profil herunterladen",
                                data=file,
                                file_name=f"{name}_Profil.docx",
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                key="download_word_demo"
                            )
                    except Exception as e:
                        st.error(f"Fehler bei der Word-Dokument-Generierung: {str(e)}")
    else:
        # Normaler Modus - Standardmäßig wird der "Standard (Extraktion → Analyse)"-Modus verwendet
        processing_mode = "Standard (Extraktion → Analyse)"
        
        # Zentrale Spalte für den File Uploader
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            uploaded_file = st.file_uploader(
                "Wähle eine Datei (PDF, JPEG, PNG oder DOCX)",
                type=["pdf", "jpg", "jpeg", "png", "docx"]
            )
        
        # Wenn eine Datei hochgeladen wurde, zeige den Dateinamen kleiner und zentriert an
        if uploaded_file:
            st.markdown(f"""
            <div style="display: flex; justify-content: center; margin-top: 10px;">
                <div style="background: rgba(255, 255, 255, 0.15); border-radius: 8px; padding: 8px 16px; 
                     backdrop-filter: blur(5px); -webkit-backdrop-filter: blur(5px); 
                     border: 1px solid rgba(255, 255, 255, 0.1); max-width: 80%; text-align: center;">
                    <div style="display: flex; align-items: center; justify-content: center;">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16" fill="white" style="margin-right: 8px;">
                            <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
                        </svg>
                        <span style="color: white; font-size: 0.9rem;">{uploaded_file.name}</span>
                    </div>
                    <div style="font-size: 0.7rem; color: rgba(255,255,255,0.7); margin-top: 4px;">
                        {round(len(uploaded_file.getvalue())/1024, 1)} KB
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Im normalen Modus prüfen wir, ob File und API Key vorhanden sind
        if uploaded_file and openai_api_key:
            # Datei speichern und verarbeiten
            with st.spinner("Datei wird verarbeitet..."):
                # Temporäre Datei erstellen
                file_extension = os.path.splitext(uploaded_file.name)[1].lower()
                with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
                    tmp_file.write(uploaded_file.getbuffer())
                    temp_file_path = tmp_file.name
                    st.session_state.temp_files.append(temp_file_path)
                
                try:
                    # Initialisiere den kombinierten Prozessor
                    combined_processor = CombinedProcessor(openai_api_key)
                    
                    # Vor der Verarbeitung prüfen, ob die Datei im Cache ist
                    file_hash = combined_processor._get_file_hash(temp_file_path)
                    is_cached = combined_processor._check_cache(file_hash) is not None
                    
                    # Verarbeite das Dokument im ausgewählten Modus
                    if "Umgekehrt" in processing_mode:
                        # Umgekehrte Reihenfolge (Analyse → Extraktion)
                        cache_status = "aus Cache geladen" if is_cached else "wird verarbeitet"
                        with st.spinner(f"Analysiere Lebenslauf in umgekehrter Reihenfolge... ({cache_status})"):
                            profile_data, extracted_text = combined_processor.extract_and_process(temp_file_path, file_extension)
                    else:
                        # Standard-Reihenfolge (Extraktion → Analyse)
                        cache_status = "aus Cache geladen" if is_cached else "wird verarbeitet"
                        with st.spinner(f"Extrahiere Text und analysiere Lebenslauf... ({cache_status})"):
                            extracted_text, profile_data = combined_processor.process_and_extract(temp_file_path, file_extension)
                    
                    # Speichere Ergebnisse in der Session
                    st.session_state.extracted_text = extracted_text
                    st.session_state.profile_data = profile_data

                    # Zeige Ergebnisse basierend auf dem ausgewählten Modus
                    if "Umgekehrt" in processing_mode:
                        # Zeige zuerst die Profildaten an
                        st.subheader("Analysierte Daten")
                        st.json(profile_data)
                        
                        # Dann den extrahierten Text
                        show_text = config.get_all_settings().get("show_extracted_text", False)
                        with st.expander("Extrahierten Text anzeigen", expanded=False):
                            st.text_area("Extrahierter Text", extracted_text, height=300)
                    else:
                        # Zeige zuerst den extrahierten Text an
                        st.subheader("Extrahierter Text")
                        
                        # Verwende die Einstellung zur Anzeige des extrahierten Textes
                        show_text = config.get_all_settings().get("show_extracted_text", False)
                        with st.expander("Extrahierten Text anzeigen", expanded=False):
                            st.text_area("Extrahierter Text", extracted_text, height=300)
                        
                        # Dann die Profildaten
                        st.subheader("Analysierte Daten")
                        with st.expander("Analysierte Daten anzeigen", expanded=False):
                            st.json(profile_data)
                    
                    # Zeige einen Erfolgshinweis an
                    st.markdown("""
                    <div style="background: rgba(255, 255, 255, 0.15); border-radius: 12px; backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.2); box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15); padding: 15px 20px; margin-bottom: 20px;">
                        <div style="display: flex; align-items: center;">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="white" style="margin-right: 10px;">
                                <path d="M12 2C6.5 2 2 6.5 2 12S6.5 22 12 22 22 17.5 22 12 17.5 2 12 2M10 17L5 12L6.41 10.59L10 14.17L17.59 6.58L19 8L10 17Z"/>
                            </svg>
                            <span style="color: white; font-weight: 500;">Dein Lebenslauf wurde erfolgreich analysiert. Jetzt kannst du die gewünschten Informationen auswählen.</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Visueller Trenner und Abstand zwischen den Abschnitten
                    st.markdown("""
                    <div style="height: 30px;"></div>
                    <div style="background: rgba(255, 255, 255, 0.2); height: 2px; border-radius: 1px; margin: 10px 0;"></div>
                    <div style="height: 30px;"></div>
                    """, unsafe_allow_html=True)
                    
                    # Statt Button für nächsten Schritt direkt Schritt 2 (Profil erstellen) anzeigen
                    st.subheader("2. Profil erstellen und exportieren")
                    
                    # Profildaten aus der Session holen
                    edited_data = {}
                    
                    # Zwei Tabs erstellen für Informationsauswahl und Profil-Generierung mit verbessertem Stil
                    st.markdown("""
                    <style>
                        .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
                            background-color: rgba(255, 255, 255, 0.2) !important;
                            color: white !important;
                            font-weight: 600 !important;
                        }
                        .stTabs [data-baseweb="tab-list"] button {
                            padding: 10px 20px !important;
                        }
                    </style>
                    """, unsafe_allow_html=True)
                    tab1, tab2 = st.tabs(["Informationen bearbeiten", "Profil exportieren"])
                    
                    with tab1:
                        # Persönliche Daten
                        st.markdown("### Persönliche Daten")
                        personal_data = profile_data.get("persönliche_daten", {})
                        
                        # Name und Grunddaten
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            edited_data["name"] = st.text_input("Name", value=personal_data.get("name", ""))
                        with col2:
                            edited_data["wohnort"] = st.text_input("Wohnort", value=personal_data.get("wohnort", ""))
                        with col3:
                            edited_data["jahrgang"] = st.text_input("Jahrgang", value=personal_data.get("jahrgang", ""))
                        
                        # Profilbild-Upload hinzufügen
                        st.markdown("### Profilbild")
                        st.markdown("Laden Sie optional ein Profilbild hoch (JPG, PNG):")
                        
                        # Profilbild-Upload
                        profile_image = st.file_uploader("Profilbild hochladen", 
                                                         type=["jpg", "jpeg", "png"], 
                                                         key="profile_image_uploader")
                        
                        # Bild anzeigen und in Session speichern, wenn hochgeladen
                        if profile_image is not None:
                            # Bild anzeigen
                            st.image(profile_image, width=150, caption="Vorschau des Profilbilds")
                            
                            # Bild in Session speichern
                            if 'profile_image' not in st.session_state or st.session_state.profile_image != profile_image:
                                # Temporäre Datei für das Bild erstellen
                                img_extension = os.path.splitext(profile_image.name)[1].lower()
                                with tempfile.NamedTemporaryFile(delete=False, suffix=img_extension) as tmp_file:
                                    tmp_file.write(profile_image.getbuffer())
                                    img_path = tmp_file.name
                                    st.session_state.profile_image_path = img_path
                                    st.session_state.temp_files.append(img_path)
                                    st.session_state.profile_image = profile_image
                        
                        # Führerschein und Wunschgehalt
                        col1, col2 = st.columns(2)
                        with col1:
                            edited_data["führerschein"] = st.text_input("Führerschein", value=personal_data.get("führerschein", ""))
                        with col2:
                            edited_data["wunschgehalt"] = st.text_input("Wunschgehalt", value=profile_data.get("wunschgehalt", ""))
                        
                        # Verfügbarkeit des Bewerbers
                        st.markdown("### Verfügbarkeit")
                        # Dropdown für Verfügbarkeitsstatus
                        verfuegbarkeit_optionen = [
                            "Sofort verfügbar",
                            "Kündigungsfrist 1 Monat",
                            "Kündigungsfrist 2 Monate",
                            "Kündigungsfrist 3 Monate",
                            "Derzeit nicht verfügbar",
                            "Verfügbar mit Einschränkungen"
                        ]
                        
                        verfuegbarkeit_status = st.selectbox(
                            "Verfügbarkeitsstatus",
                            options=verfuegbarkeit_optionen,
                            index=0,
                            key="verfuegbarkeit_status"
                        )
                        
                        # Zusätzliche Details zur Verfügbarkeit
                        verfuegbarkeit_details = st.text_area(
                            "Details zur Verfügbarkeit (optional)",
                            value=profile_data.get("verfuegbarkeit_details", ""),
                            help="Z.B. gesundheitliche Einschränkungen, spezielle Umstände, genaues Datum der Verfügbarkeit",
                            key="verfuegbarkeit_details"
                        )
                        
                        # Verfügbarkeitsdaten speichern
                        edited_data["verfuegbarkeit_status"] = verfuegbarkeit_status
                        edited_data["verfuegbarkeit_details"] = verfuegbarkeit_details

                        # Kontaktinformationen
                        st.markdown("### Kontaktinformationen")
                        kontakt = personal_data.get("kontakt", {})
                        
                        # Ansprechpartner-Dropdown
                        ansprechpartner_options = [
                            "Kai Fischer", 
                            "Melike Demirkol", 
                            "Konrad Ruszyk", 
                            "Alessandro Böhm", 
                            "Salim Alizai"
                        ]
                        
                        # Vorauswahl des Ansprechpartners (falls vorhanden)
                        current_ansprechpartner = kontakt.get("ansprechpartner", "")
                        default_index = 0
                        if current_ansprechpartner in ansprechpartner_options:
                            default_index = ansprechpartner_options.index(current_ansprechpartner)
                        
                        # Ansprechpartner auswählen
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            selected_ansprechpartner = st.selectbox(
                                "Ansprechpartner",
                                options=ansprechpartner_options,
                                index=default_index,
                                key="ansprechpartner"
                            )
                            edited_data["ansprechpartner"] = selected_ansprechpartner
                            
                            # E-Mail-Adresse basierend auf dem Nachnamen generieren
                            nachname = selected_ansprechpartner.split()[-1]
                            email = f"{nachname.lower()}@galdora.de"
                            edited_data["email"] = email
                        
                        with col2:
                            # Telefonnummer ist für alle Ansprechpartner gleich
                            telefon = "02161 62126-02"
                            edited_data["telefon"] = st.text_input("Telefon", value=telefon, disabled=True)
                        
                        with col3:
                            # E-Mail-Adresse anzeigen
                            st.text_input("E-Mail", value=email, disabled=True)
                        
                        # Berufserfahrung
                        st.markdown("### Berufserfahrung")
                        
                        # Liste für editierte Berufserfahrungen
                        edited_experience = []
                        
                        for idx, erfahrung in enumerate(profile_data.get("berufserfahrung", [])):
                            with st.expander(f"{erfahrung.get('zeitraum', 'Neue Erfahrung')}: {erfahrung.get('position', '')} bei {erfahrung.get('unternehmen', '')}", expanded=False):
                                exp_data = {}
                                col1, col2 = st.columns(2)
                                with col1:
                                    exp_data["zeitraum"] = st.text_input(f"Zeitraum #{idx+1}", value=erfahrung.get("zeitraum", ""))
                                    exp_data["unternehmen"] = st.text_input(f"Unternehmen #{idx+1}", value=erfahrung.get("unternehmen", ""))
                                with col2:
                                    exp_data["position"] = st.text_input(f"Position #{idx+1}", value=erfahrung.get("position", ""))
                                
                                # Aufgaben als Textarea mit einer Aufgabe pro Zeile
                                aufgaben_text = "\n".join(erfahrung.get("aufgaben", []))
                                new_aufgaben = st.text_area(
                                    f"Aufgaben #{idx+1} (eine Aufgabe pro Zeile)", 
                                    value=aufgaben_text,
                                    height=150
                                )
                                # Aufgaben zurück in eine Liste konvertieren
                                exp_data["aufgaben"] = [task.strip() for task in new_aufgaben.split("\n") if task.strip()]
                                
                                # Option zum Löschen dieser Berufserfahrung
                                include = st.checkbox(f"Diese Berufserfahrung einbeziehen", value=True, key=f"exp_{idx}")
                                if include:
                                    edited_experience.append(exp_data)
                        
                        # Button zum Hinzufügen einer neuen Berufserfahrung
                        if st.button("+ Neue Berufserfahrung hinzufügen"):
                            with st.expander("Neue Berufserfahrung", expanded=True):
                                new_exp = {}
                                col1, col2 = st.columns(2)
                                with col1:
                                    new_exp["zeitraum"] = st.text_input("Zeitraum (neu)")
                                    new_exp["unternehmen"] = st.text_input("Unternehmen (neu)")
                                with col2:
                                    new_exp["position"] = st.text_input("Position (neu)")
                                
                                new_aufgaben = st.text_area(
                                    "Aufgaben (eine Aufgabe pro Zeile)", 
                                    height=150
                                )
                                new_exp["aufgaben"] = [task.strip() for task in new_aufgaben.split("\n") if task.strip()]
                                
                                if st.button("Berufserfahrung hinzufügen"):
                                    edited_experience.append(new_exp)
                        
                        # Ausbildung
                        st.markdown("### Ausbildung")
                        
                        # Liste für editierte Ausbildungen
                        edited_education = []
                        
                        for idx, ausbildung in enumerate(profile_data.get("ausbildung", [])):
                            with st.expander(f"{ausbildung.get('zeitraum', 'Neue Ausbildung')}: {ausbildung.get('abschluss', '')} - {ausbildung.get('institution', '')}", expanded=False):
                                edu_data = {}
                                col1, col2 = st.columns(2)
                                with col1:
                                    edu_data["zeitraum"] = st.text_input(f"Zeitraum (Ausbildung) #{idx+1}", value=ausbildung.get("zeitraum", ""))
                                    edu_data["institution"] = st.text_input(f"Institution #{idx+1}", value=ausbildung.get("institution", ""))
                                with col2:
                                    edu_data["abschluss"] = st.text_input(f"Abschluss #{idx+1}", value=ausbildung.get("abschluss", ""))
                                    edu_data["note"] = st.text_input(f"Note #{idx+1}", value=ausbildung.get("note", ""))
                                
                                edu_data["schwerpunkte"] = st.text_input(f"Studienschwerpunkte #{idx+1}", value=ausbildung.get("schwerpunkte", ""))
                                
                                # Option zum Löschen dieser Ausbildung
                                include = st.checkbox(f"Diese Ausbildung einbeziehen", value=True, key=f"edu_{idx}")
                                if include:
                                    edited_education.append(edu_data)
                        
                        # Button zum Hinzufügen einer neuen Ausbildung
                        if st.button("+ Neue Ausbildung hinzufügen"):
                            with st.expander("Neue Ausbildung", expanded=True):
                                new_edu = {}
                                col1, col2 = st.columns(2)
                                with col1:
                                    new_edu["zeitraum"] = st.text_input("Zeitraum (Ausbildung neu)")
                                    new_edu["institution"] = st.text_input("Institution (neu)")
                                with col2:
                                    new_edu["abschluss"] = st.text_input("Abschluss (neu)")
                                    new_edu["note"] = st.text_input("Note (neu)")
                                
                                new_edu["schwerpunkte"] = st.text_input("Studienschwerpunkte (neu)")
                                
                                if st.button("Ausbildung hinzufügen"):
                                    edited_education.append(new_edu)
                        
                        # Weiterbildung
                        st.markdown("### Weiterbildung")
                        
                        # Liste für editierte Weiterbildungen
                        edited_training = []
                        
                        for idx, weiterbildung in enumerate(profile_data.get("weiterbildungen", [])):
                            with st.expander(f"{weiterbildung.get('zeitraum', 'Neue Weiterbildung')}: {weiterbildung.get('bezeichnung', '')}", expanded=False):
                                training_data = {}
                                col1, col2 = st.columns(2)
                                with col1:
                                    training_data["zeitraum"] = st.text_input(f"Zeitraum (Weiterbildung) #{idx+1}", value=weiterbildung.get("zeitraum", ""))
                                with col2:
                                    training_data["bezeichnung"] = st.text_input(f"Bezeichnung #{idx+1}", value=weiterbildung.get("bezeichnung", ""))
                                    
                                training_data["abschluss"] = st.text_input(f"Abschluss (Weiterbildung) #{idx+1}", value=weiterbildung.get("abschluss", ""))
                                
                                # Option zum Löschen dieser Weiterbildung
                                include = st.checkbox(f"Diese Weiterbildung einbeziehen", value=True, key=f"train_{idx}")
                                if include:
                                    edited_training.append(training_data)
                        
                        # Button zum Hinzufügen einer neuen Weiterbildung
                        if st.button("+ Neue Weiterbildung hinzufügen"):
                            with st.expander("Neue Weiterbildung", expanded=True):
                                new_training = {}
                                col1, col2 = st.columns(2)
                                with col1:
                                    new_training["zeitraum"] = st.text_input("Zeitraum (Weiterbildung neu)")
                                with col2:
                                    new_training["bezeichnung"] = st.text_input("Bezeichnung (neu)")
                                    
                                new_training["abschluss"] = st.text_input("Abschluss (Weiterbildung neu)")
                                
                                if st.button("Weiterbildung hinzufügen"):
                                    edited_training.append(new_training)
                        
                        # Zusammenführen der bearbeiteten Daten
                        complete_edited_data = {
                            "persönliche_daten": {
                                "name": edited_data.get("name", ""),
                                "wohnort": edited_data.get("wohnort", ""),
                                "jahrgang": edited_data.get("jahrgang", ""),
                                "führerschein": edited_data.get("führerschein", ""),
                                "kontakt": {
                                    "ansprechpartner": edited_data.get("ansprechpartner", ""),
                                    "telefon": edited_data.get("telefon", ""),
                                    "email": edited_data.get("email", "")
                                },
                                "profile_image": st.session_state.get("profile_image_path", None)
                            },
                            "berufserfahrung": edited_experience,
                            "ausbildung": edited_education,
                            "weiterbildungen": edited_training,
                            "wunschgehalt": edited_data.get("wunschgehalt", ""),
                            "verfuegbarkeit_status": edited_data.get("verfuegbarkeit_status", "Sofort verfügbar"),
                            "verfuegbarkeit_details": edited_data.get("verfuegbarkeit_details", "")
                        }
                        
                        # Speichern der bearbeiteten Daten in der Session
                        st.session_state.edited_data = complete_edited_data
                        
                        # Prüfen auf Vollständigkeit der kritischen Daten
                        validation_errors = []
                        if not edited_data.get("name"):
                            validation_errors.append("Name fehlt")
                        if not edited_data.get("email") and not edited_data.get("telefon"):
                            validation_errors.append("Mindestens eine Kontaktmöglichkeit (E-Mail oder Telefon) wird benötigt")
                        
                        # Wenn es Validierungsfehler gibt, diese anzeigen
                        if validation_errors:
                            for error in validation_errors:
                                st.error(error)
                    
                    with tab2:
                        # Profil generieren und Vorschau anzeigen
                        st.markdown("### Profilvorschau und Export")
                        
                        # Profildaten aus der Session holen oder aus den aktuellen bearbeiteten Daten
                        edited_data_to_use = st.session_state.edited_data if "edited_data" in st.session_state else complete_edited_data
                        
                        # Vorlage auswählen
                        st.markdown("#### Vorlage auswählen")
                        
                        # Standard-Vorlage aus der Konfiguration holen
                        default_template = config.get_all_settings().get("default_template", "professional")
                        
                        # Template-Auswahl als Variable speichern
                        template_to_use = default_template
                        
                        # Vorlagenauswahl mit Standard-Voreinstellung
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            classic = st.button("🔵 🔵\nKlassisch", 
                                                use_container_width=True, 
                                                type="primary" if default_template == "classic" else "secondary")
                            if classic:
                                template_to_use = "classic"
                                # Automatisch Vorschau aktualisieren, wenn Template geändert wird
                                st.session_state.update_preview = True
                                
                        with col2:
                            modern = st.button("🟢 🟢\nModern", 
                                            use_container_width=True,
                                            type="primary" if default_template == "modern" else "secondary")
                            if modern:
                                template_to_use = "modern"
                                # Automatisch Vorschau aktualisieren, wenn Template geändert wird
                                st.session_state.update_preview = True
                                
                        with col3:
                            professional = st.button("🟣 🟣\nProfessionell", 
                                                use_container_width=True,
                                                type="primary" if default_template == "professional" else "secondary")
                            if professional:
                                template_to_use = "professional"
                                # Automatisch Vorschau aktualisieren, wenn Template geändert wird
                                st.session_state.update_preview = True
                                
                        with col4:
                            minimalistic = st.button("⚫ ⚫\nMinimalistisch", 
                                                use_container_width=True,
                                                type="primary" if default_template == "minimalist" else "secondary")
                            if minimalistic:
                                template_to_use = "minimalist"
                                # Automatisch Vorschau aktualisieren, wenn Template geändert wird
                                st.session_state.update_preview = True
                                
                        # Profil-Vorschau generieren und anzeigen
                        if 'preview_pdf' not in st.session_state or st.button("Vorschau aktualisieren") or st.session_state.get('update_preview', False):
                            # Reset des Update-Flags
                            st.session_state.update_preview = False
                            with st.spinner("Profil wird generiert..."):
                                try:
                                    generator = ProfileGenerator()
                                    output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                                    output_path = output_file.name
                                    output_file.close()
                                    st.session_state.temp_files.append(output_path)
                                    
                                    # Generiere Profil mit dem ausgewählten Template
                                    profile_path = generator.generate_profile(edited_data_to_use, output_path, template=template_to_use)
                                    st.session_state.preview_pdf = profile_path
                                    
                                    # Zeige eine Erfolgsmeldung an
                                    st.success("Profil erfolgreich generiert!")
                                    
                                    # Speichere das ausgewählte Template für zukünftige Aktualisierungen
                                    st.session_state.selected_template = template_to_use
                                except Exception as e:
                                    st.error(f"Fehler bei der Generierung des Profils: {str(e)}")
                        
                        # PDF-Vorschau anzeigen
                        if st.session_state.preview_pdf:
                            st.markdown("#### Profil-Vorschau")
                            pdf_display = display_pdf(st.session_state.preview_pdf)
                            st.markdown(pdf_display, unsafe_allow_html=True)
                            
                            # Name für das Profil
                            name = edited_data_to_use["persönliche_daten"]["name"].replace(" ", "_")
                            if not name or name == "":
                                name = "Profil"
                            
                            # Auswahl des Formats mit RadioButtons
                            st.markdown("#### Format wählen")
                            format_option = st.radio(
                                "In welchem Format möchten Sie das Profil herunterladen?",
                                options=["PDF", "Word"],
                                horizontal=True,
                                key="format_choice"
                            )
                            
                            # Je nach Auswahl unterschiedlichen Download-Button anzeigen
                            if format_option == "PDF":
                                # PDF-Download
                                if st.session_state.preview_pdf and os.path.exists(st.session_state.preview_pdf):
                                    with open(st.session_state.preview_pdf, "rb") as file:
                                        st.download_button(
                                            label="Profil herunterladen",
                                            data=file,
                                            file_name=f"{name}_Profil.pdf",
                                            mime="application/pdf",
                                            key="download_pdf"
                                        )
                                else:
                                    st.error("Bitte generieren Sie zuerst eine Vorschau des Profils.")
                            else:
                                # Word-Dokument generieren und herunterladen
                                # Temporäre Datei für das Word-Dokument erstellen
                                output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
                                output_path = output_file.name
                                output_file.close()
                                st.session_state.temp_files.append(output_path)
                                
                                try:
                                    # Stelle sicher, dass generator definiert ist
                                    generator = ProfileGenerator()
                                    
                                    # Word-Dokument mit dem gleichen Generator erstellen
                                    docx_path = generator.generate_profile(
                                        edited_data_to_use, 
                                        output_path, 
                                        template=template_to_use,
                                        format="docx"
                                    )
                                    
                                    # Word-Dokument zum Download anbieten
                                    with open(docx_path, "rb") as file:
                                        st.download_button(
                                            label="Profil herunterladen",
                                            data=file,
                                            file_name=f"{name}_Profil.docx",
                                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                            key="download_word"
                                        )
                                except Exception as e:
                                    st.error(f"Fehler bei der Word-Dokument-Generierung: {str(e)}")
                
                except Exception as e:
                    st.error(f"Fehler bei der Verarbeitung: {str(e)}")
        
        elif uploaded_file and not openai_api_key:
            st.warning("Bitte gib einen OpenAI API Key in der Seitenleiste ein, um fortzufahren.")

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
atexit.register(cleanup)
