#!/usr/bin/env python3
"""
Einstellungsseite für CV2Profile

Diese Seite bietet Konfigurationsoptionen für die CV2Profile-Anwendung.
"""

import streamlit as st
import os
import sys

# Den Hauptpfad zum Importieren hinzufügen
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

# Importe aus den reorganisierten Modulen
from src.core.document_processor import DocumentProcessor
from src.core.ai_extractor import AIExtractor
from src.core.combined_processor import CombinedProcessor
from src.templates.template_generator import ProfileGenerator
import src.utils.config as config

# Seitenkonfiguration
st.set_page_config(
    page_title="CV2Profile - Einstellungen",
    page_icon="⚙️",
    layout="wide"
)

# Custom CSS für konsistentes Design
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
    
    /* Glasmorphismus-Container */
    .settings-container {
        background: rgba(255, 255, 255, 0.1) !important;
        padding: 20px !important;
        border-radius: 16px !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
        margin-bottom: 20px !important;
    }
    
    /* Textfarbe für die Hauptseite auf weiß setzen */
    .stMarkdown, .stText, h1, h2, h3, p, span, div {
        color: white !important;
    }
    
    /* Sidebar dunkler gestalten */
    [data-testid="stSidebar"] {
        background-color: rgba(20, 20, 26, 0.8) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
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
</style>
"""

# CSS einbinden
st.markdown(custom_css, unsafe_allow_html=True)

# Seitentitel mit Icon
st.markdown("""
    <h1 style='text-align: center;'>
        <span style='margin-right: 10px;'>⚙️</span>Einstellungen
    </h1>
    <p style='text-align: center; font-size: 1.2em; margin-bottom: 40px;'>
        Konfigurieren Sie Ihre CV2Profile-Anwendung
    </p>
""", unsafe_allow_html=True)

# Container für die Einstellungen im Glasmorphismus-Stil
st.markdown("<div class='settings-container'>", unsafe_allow_html=True)

# Allgemeine Einstellungen
st.markdown("## 🔧 Allgemeine Einstellungen")
st.markdown("### Profilgenerierung")

# Placeholder für Einstellungen (keine Funktionalität implementiert)
col1, col2 = st.columns(2)
with col1:
    st.selectbox("Standard-Template", 
                ["Klassisch", "Modern", "Professionell", "Minimalistisch"], 
                disabled=True,
                help="Wählen Sie das Standard-Template für neu generierte Profile")
    
    st.selectbox("Standard-Exportformat", 
                ["PDF", "DOCX"], 
                disabled=True,
                help="Wählen Sie das Standard-Exportformat für neu generierte Profile")

with col2:
    st.toggle("Logo automatisch einfügen", 
             value=True, 
             disabled=True,
             help="Fügt automatisch das Logo in alle generierten Profile ein")
    
    st.toggle("Speichern vor Export bestätigen", 
             value=True, 
             disabled=True,
             help="Fragt vor dem Export nach, ob das Profil gespeichert werden soll")

st.markdown("</div>", unsafe_allow_html=True)

# Container für KI-Einstellungen
st.markdown("<div class='settings-container'>", unsafe_allow_html=True)
st.markdown("## 🧠 KI-Einstellungen")

# KI-Modell-Einstellungen (Placeholder)
st.selectbox("KI-Modell", 
            ["gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"], 
            disabled=True,
            help="Wählen Sie das zu verwendende KI-Modell für die Textextraktion")

# API-Key (Placeholder)
api_key = st.text_input("OpenAI API-Key", 
                        type="password", 
                        disabled=True,
                        help="Ihr OpenAI API-Key für den Zugriff auf die KI-Modelle")

# Erweiterte KI-Einstellungen
with st.expander("Erweiterte KI-Einstellungen"):
    st.slider("Temperatur", 
              min_value=0.0, 
              max_value=1.0, 
              value=0.7, 
              step=0.1, 
              disabled=True,
              help="Bestimmt die Kreativität der KI-Antworten")
    
    st.slider("Max Tokens", 
              min_value=100, 
              max_value=4000, 
              value=2000, 
              step=100, 
              disabled=True,
              help="Maximale Länge der KI-Antwort in Tokens")

st.markdown("</div>", unsafe_allow_html=True)

# Container für Benutzereinstellungen
st.markdown("<div class='settings-container'>", unsafe_allow_html=True)
st.markdown("## 👤 Benutzereinstellungen")

# Ansprechpartner-Verwaltung (Placeholder)
st.markdown("### Ansprechpartner verwalten")
st.info("Hier können Sie Ihre Ansprechpartner für die Profile verwalten.")

# Platzhaltertabelle für Ansprechpartner
data = {
    "Name": ["Max Mustermann", "Anna Schmidt"],
    "Position": ["Senior Consultant", "HR Manager"],
    "Kontakt": ["max@example.com", "anna@example.com"]
}
df = st.dataframe(data, use_container_width=True)

# Buttons für Ansprechpartner-Verwaltung (Placeholder)
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.button("Hinzufügen", disabled=True)
with col2:
    st.button("Bearbeiten", disabled=True)
with col3:
    st.button("Löschen", disabled=True)

st.markdown("</div>", unsafe_allow_html=True)

# Container für System-Informationen
st.markdown("<div class='settings-container'>", unsafe_allow_html=True)
st.markdown("## 🖥️ System-Information")

# Platzhalter für Systeminformationen
col1, col2 = st.columns(2)
with col1:
    st.markdown("**Version:** 1.0.0")
    st.markdown("**Letztes Update:** 2023-11-15")
with col2:
    st.markdown("**Python Version:** 3.9.x")
    st.markdown("**Streamlit Version:** 1.28.x")

# Platzhalter für Exportpfad
st.text_input("Standard-Exportpfad", 
             value="./exports", 
             disabled=True,
             help="Standardpfad für den Export von Profilen")

st.markdown("</div>", unsafe_allow_html=True)

# Container für Hilfe und Support
st.markdown("<div class='settings-container'>", unsafe_allow_html=True)
st.markdown("## ❓ Hilfe & Support")

# Hilfe und Support-Links (Placeholder)
st.markdown("""
- **Dokumentation:** [Link zur Dokumentation](#)
- **Support kontaktieren:** [Email an Support](#)
- **Probleme melden:** [Issue Tracker](#)
""")

st.button("Zurücksetzen auf Standardeinstellungen", disabled=True)

st.markdown("</div>", unsafe_allow_html=True)

# Speichern-Button am Ende (Placeholder)
st.button("Einstellungen speichern", disabled=True)

# Footer
st.markdown("""
---
<p style='text-align: center; font-size: 0.8em; opacity: 0.7;'>
    CV2Profile - Einstellungsbereich - © 2023
</p>
""", unsafe_allow_html=True) 