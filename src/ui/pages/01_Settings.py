import streamlit as st
import os
import sys
import tempfile
import json
from pathlib import Path

# Füge den übergeordneten Ordner zum Pythonpfad hinzu, um relative Importe zu ermöglichen
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Importe aus den reorganisierten Modulen
import src.utils.config as config  # Importiere das Konfigurationsmodul

# CSS für Farbverlaufshintergrund und weiße Schaltflächen (gleicher Stil wie in der Hauptapp)
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
    
    /* Platzhalter-Text für Inputs */
    input::placeholder, textarea::placeholder {
        color: rgba(255, 255, 255, 0.6) !important;
    }
    
    /* Weißer Text für Labels */
    label {
        color: white !important;
    }
    
    /* Checkbox-Stil anpassen */
    .stCheckbox > div > div > div {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 4px !important;
    }
    
    /* Container mit Glaseffekt */
    .glass-container {
        background: rgba(255, 255, 255, 0.15);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        backdrop-filter: blur(12px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
</style>
"""

# Seitenkonfiguration
st.set_page_config(
    page_title="CV2Profile - Einstellungen",
    page_icon="⚙️",
    layout="wide"
)

# CSS einbinden
st.markdown(custom_css, unsafe_allow_html=True)

# Header-Bereich
st.markdown("""
<div style="background-color: rgba(255, 255, 255, 0.15); padding: 2.5rem; border-radius: 15px; margin-bottom: 2rem; color: white; text-align: center; backdrop-filter: blur(12px); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25); border: 1px solid rgba(255, 255, 255, 0.18);">
    <h1 style="margin: 0; font-weight: 700; font-size: 2.8rem; text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);">CV2Profile - Einstellungen</h1>
    <p style="margin-top: 1rem; font-size: 1.2rem; opacity: 0.95;">Konfiguriere die Anwendung nach deinen Bedürfnissen</p>
</div>
""", unsafe_allow_html=True)

# Lade aktuelle Einstellungen
all_settings = config.get_all_settings()

# Hauptbereich mit 3 Spalten
col1, col2, col3 = st.columns([1, 1, 1])

# Allgemeine Einstellungen in der ersten Spalte
with col1:
    st.markdown("""
    <div class="glass-container">
        <h2 style="margin-top: 0;">Allgemeine Einstellungen</h2>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        
        # Template-Auswahl
        st.subheader("Vorlagen")
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
            key="template_select_settings"
        )
        
        # Anzeige des extrahierten Textes
        show_text_default = all_settings.get("show_extracted_text", False)
        show_text_setting = st.checkbox(
            "Extrahierten Text standardmäßig anzeigen", 
            value=show_text_default,
            key="show_text_setting"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)

# API-Einstellungen in der zweiten Spalte
with col2:
    st.markdown("""
    <div class="glass-container">
        <h2 style="margin-top: 0;">API-Einstellungen</h2>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        
        # API-Key Einstellungen
        st.subheader("OpenAI API")
        
        # Aktuellen API-Key aus der Konfiguration laden
        current_api_key = all_settings.get("openai_api_key", "")
        # Sternchen anzeigen, wenn ein API-Key gespeichert ist
        api_key_display = "********" if current_api_key else ""
        
        api_key_input = st.text_input(
            "OpenAI API Key", 
            value=api_key_display,
            type="password",
            help="Dein OpenAI API-Key wird benötigt, um Lebensläufe zu analysieren."
        )
        
        # Button zum Speichern des API-Keys
        if api_key_input and api_key_input != "********":
            save_key = st.checkbox("API-Key speichern", value=True,
                                   help="Der API-Key wird lokal auf deinem Computer gespeichert.")
            
            if save_key:
                if st.button("API-Key aktualisieren"):
                    st.info("Hinweis: Diese Funktion ist aktuell nur ein UI-Element ohne Funktionalität.")
        
        st.markdown('</div>', unsafe_allow_html=True)

# System-Einstellungen in der dritten Spalte
with col3:
    st.markdown("""
    <div class="glass-container">
        <h2 style="margin-top: 0;">System-Einstellungen</h2>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        
        # Cache-Management
        st.subheader("Cache & Speicher")
        
        # Cache-Größe (Dummy-Wert)
        cache_size = "1.2 MB"
        st.info(f"Aktueller Cache-Größe: {cache_size}")
        
        if st.button("Cache leeren"):
            st.info("Hinweis: Diese Funktion ist aktuell nur ein UI-Element ohne Funktionalität.")
        
        # Temporäre Dateien löschen
        if st.button("Temporäre Dateien löschen"):
            st.info("Hinweis: Diese Funktion ist aktuell nur ein UI-Element ohne Funktionalität.")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Unterer Bereich für zusätzliche Optionen
st.markdown("""
<div class="glass-container">
    <h2 style="margin-top: 0;">Erweiterte Einstellungen</h2>
    <p>Diese Einstellungen beeinflussen das Verhalten der Anwendung und die generierten Profile.</p>
</div>
""", unsafe_allow_html=True)

# Erweiterte Einstellungen in zwei Spalten
advanced_col1, advanced_col2 = st.columns(2)

with advanced_col1:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    
    # Profilgenerierungs-Einstellungen
    st.subheader("Profilgenerierung")
    
    # Dummy-Einstellungen
    st.slider("Qualität der PDF-Generierung", min_value=1, max_value=10, value=8,
              help="Höhere Werte erzeugen bessere Qualität, benötigen aber mehr Ressourcen.")
    
    st.selectbox(
        "Standardsprache",
        options=["Deutsch", "Englisch", "Französisch", "Spanisch"],
        index=0,
        help="Standardsprache für die Profilerstellung"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

with advanced_col2:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    
    # KI-Einstellungen
    st.subheader("KI-Einstellungen")
    
    # Dummy-Einstellungen
    st.slider("KI-Genauigkeit", min_value=0.1, max_value=1.0, value=0.7, step=0.1,
              help="Beeinflusst die Genauigkeit und Geschwindigkeit der KI-Extraktion.")
    
    st.selectbox(
        "KI-Modell",
        options=["GPT-3.5-turbo", "GPT-4", "GPT-4-turbo"],
        index=0,
        help="Wähle das zu verwendende OpenAI-Modell"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

# Fußzeile
st.markdown("""
<div style="margin-top: 50px; text-align: center; opacity: 0.8;">
    <p>CV2Profile - Einstellungen © 2023-2024</p>
</div>
""", unsafe_allow_html=True)

# Hinweis, dass dies eine Demoseite ist
st.sidebar.warning("Hinweis: Diese Einstellungsseite ist aktuell eine Demonstration ohne vollständige Funktionalität.") 