"""
Hauptseite des CV2Profile Konverters

Diese Datei stellt die Hauptseite der Anwendung dar und dient als Einstiegspunkt für die 
Multipage-App-Struktur von Streamlit.
"""

import streamlit as st
import os
import sys
from pathlib import Path

# Füge den übergeordneten Ordner zum Pythonpfad hinzu, um relative Importe zu ermöglichen
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import der run_main_app Funktion aus app.py
from src.ui.app import run_main_app

# Seitentitel und Konfiguration
st.set_page_config(
    page_title="CV2Profile Konverter", 
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.example.com/help',
        'Report a bug': "https://www.example.com/bug",
        'About': "# CV2Profile Konverter\nEin KI-gestützter CV-Parser, der Lebensläufe analysiert und in standardisierte Profile konvertiert."
    }
)

# Nur den Titel zur Seitenleiste hinzufügen, ohne Statusanzeige
with st.sidebar:
    st.title("CV2Profile")

# Starte die Hauptanwendung mit Redirect zur Konverter-Seite
run_main_app() 