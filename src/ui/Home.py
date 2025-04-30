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

# Importe aus der app.py
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

# Zahnrad-Symbol zur Seitenleiste hinzufügen
with st.sidebar:
    st.title("CV2Profile")
    
    # Link zur Einstellungsseite mit Zahnrad-Icon
    st.markdown("""
    <style>
    .sidebar-option {
        display: flex;
        align-items: center;
        padding: 10px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        margin-bottom: 10px;
        color: white;
        text-decoration: none;
        transition: all 0.3s ease;
    }
    .sidebar-option:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateY(-2px);
    }
    .sidebar-option svg {
        margin-right: 10px;
    }
    </style>
    
    <a href="/Einstellungen" class="sidebar-option">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="white" viewBox="0 0 24 24">
            <path d="M19.14,12.94c0.04-0.3,0.06-0.61,0.06-0.94c0-0.32-0.02-0.64-0.07-0.94l2.03-1.58c0.18-0.14,0.23-0.41,0.12-0.61 l-1.92-3.32c-0.12-0.22-0.37-0.29-0.59-0.22l-2.39,0.96c-0.5-0.38-1.03-0.7-1.62-0.94L14.4,2.81c-0.04-0.24-0.24-0.41-0.48-0.41 h-3.84c-0.24,0-0.43,0.17-0.47,0.41L9.25,5.35C8.66,5.59,8.12,5.92,7.63,6.29L5.24,5.33c-0.22-0.08-0.47,0-0.59,0.22L2.74,8.87 C2.62,9.08,2.66,9.34,2.86,9.48l2.03,1.58C4.84,11.36,4.8,11.69,4.8,12s0.02,0.64,0.07,0.94l-2.03,1.58 c-0.18,0.14-0.23,0.41-0.12,0.61l1.92,3.32c0.12,0.22,0.37,0.29,0.59,0.22l2.39-0.96c0.5,0.38,1.03,0.7,1.62,0.94l0.36,2.54 c0.05,0.24,0.24,0.41,0.48,0.41h3.84c0.24,0,0.44-0.17,0.47-0.41l0.36-2.54c0.59-0.24,1.13-0.56,1.62-0.94l2.39,0.96 c0.22,0.08,0.47,0,0.59-0.22l1.92-3.32c0.12-0.22,0.07-0.47-0.12-0.61L19.14,12.94z M12,15.6c-1.98,0-3.6-1.62-3.6-3.6 s1.62-3.6,3.6-3.6s3.6,1.62,3.6,3.6S13.98,15.6,12,15.6z"/>
        </svg>
        Einstellungen
    </a>
    """, unsafe_allow_html=True)

# Starte die Hauptanwendung
# Die Funktion run_main_app muss in app.py implementiert werden
run_main_app() 