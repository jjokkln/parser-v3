#!/usr/bin/env python3
"""
Einstellungsseite für CV2Profile

Diese Seite bietet Konfigurationsoptionen für die CV2Profile-Anwendung.
"""

import streamlit as st
import os
import sys

# Den Hauptpfad zum Importieren hinzufügen
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

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

# Initialisiere die Einstellungen aus dem Konfigurationsmodul
all_settings = config.get_all_settings()

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

# Template-Optionen
template_options = {
    "professional": "Professionell", 
    "classic": "Klassisch", 
    "modern": "Modern", 
    "minimalist": "Minimalistisch"
}

# Ermittle den aktuellen Template-Wert aus den Einstellungen
default_template = all_settings.get("default_template", "professional")

col1, col2 = st.columns(2)
with col1:
    # Template-Auswahl
    selected_template = st.selectbox(
        "Standard-Template", 
        options=list(template_options.keys()),
        format_func=lambda x: template_options[x],
        index=list(template_options.keys()).index(default_template),
        help="Wählen Sie das Standard-Template für neu generierte Profile"
    )
    
    # Speichere die Template-Voreinstellung, wenn sie sich geändert hat
    if selected_template != default_template:
        config.update_setting("default_template", selected_template)
        st.success(f"Standard-Template auf {template_options[selected_template]} gesetzt!")
    
    st.selectbox("Standard-Exportformat", 
                ["PDF", "DOCX"], 
                index=0,
                help="Wählen Sie das Standard-Exportformat für neu generierte Profile")

with col2:
    # Einstellung zum Anzeigen des extrahierten Textes
    show_text_default = all_settings.get("show_extracted_text", False)
    show_text_setting = st.toggle(
        "Extrahierten Text standardmäßig anzeigen", 
        value=show_text_default,
        help="Automatisch den extrahierten Text anzeigen, wenn ein Dokument verarbeitet wird"
    )
    
    # Speichere die Textanzeige-Einstellung, wenn sie sich geändert hat
    if show_text_setting != show_text_default:
        config.update_setting("show_extracted_text", show_text_setting)
        st.success("Textanzeige-Einstellung gespeichert!")
    
    logo_setting = st.toggle("Logo automatisch einfügen", 
             value=True, 
             help="Fügt automatisch das Logo in alle generierten Profile ein")

st.markdown("</div>", unsafe_allow_html=True)

# Container für KI-Einstellungen
st.markdown("<div class='settings-container'>", unsafe_allow_html=True)
st.markdown("## 🧠 KI-Einstellungen")

# KI-Modell-Einstellungen
ai_models = ["gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"]
current_model = all_settings.get("ai_model", "gpt-4-turbo")

selected_model = st.selectbox(
    "KI-Modell", 
    options=ai_models,
    index=ai_models.index(current_model) if current_model in ai_models else 0,
    help="Wählen Sie das zu verwendende KI-Modell für die Textextraktion"
)

# Speichere das ausgewählte Modell, wenn es sich geändert hat
if selected_model != current_model:
    config.update_setting("ai_model", selected_model)
    st.success(f"KI-Modell auf {selected_model} gesetzt!")

# API-Key
api_key = config.get_openai_api_key()
api_key_input = st.text_input(
    "OpenAI API-Key", 
    value=api_key,
    type="password",
    help="Ihr OpenAI API-Key für den Zugriff auf die KI-Modelle"
)

# Speicher-Button für den API-Key
if api_key_input and api_key_input != api_key:
    if st.button("API-Key speichern"):
        config.save_openai_api_key(api_key_input)
        st.success("API-Key erfolgreich gespeichert!")

# Erweiterte KI-Einstellungen
with st.expander("Erweiterte KI-Einstellungen"):
    # Temperatur-Einstellung
    current_temp = all_settings.get("temperature", 0.7)
    temp = st.slider(
        "Temperatur", 
        min_value=0.0, 
        max_value=1.0, 
        value=current_temp, 
        step=0.1,
        help="Bestimmt die Kreativität der KI-Antworten (niedrigere Werte = präzisere Antworten)"
    )
    
    if temp != current_temp:
        config.update_setting("temperature", temp)
    
    # Max Tokens-Einstellung
    current_max_tokens = all_settings.get("max_tokens", 2000)
    max_tokens = st.slider(
        "Max Tokens", 
        min_value=100, 
        max_value=4000, 
        value=current_max_tokens, 
        step=100, 
        help="Maximale Länge der KI-Antwort in Tokens"
    )
    
    if max_tokens != current_max_tokens:
        config.update_setting("max_tokens", max_tokens)

st.markdown("</div>", unsafe_allow_html=True)

# Container für Benutzereinstellungen
st.markdown("<div class='settings-container'>", unsafe_allow_html=True)
st.markdown("## 👤 Benutzereinstellungen")

# Ansprechpartner-Verwaltung
st.markdown("### Ansprechpartner verwalten")
st.info("Hier können Sie Ihre Ansprechpartner für die Profile verwalten.")

# Lade bestehende Ansprechpartner oder erstelle ein leeres Dictionary
contacts = all_settings.get("contacts", [])
if not contacts:
    contacts = [
        {"name": "Max Mustermann", "position": "Senior Consultant", "kontakt": "max@example.com"},
        {"name": "Anna Schmidt", "position": "HR Manager", "kontakt": "anna@example.com"}
    ]

# Erstelle eine Tabelle für die Ansprechpartner
import pandas as pd
if contacts:
    df = pd.DataFrame(contacts)
    edited_df = st.data_editor(
        df, 
        use_container_width=True,
        num_rows="dynamic",
        key="contacts_editor"
    )
    
    # Wenn Änderungen vorgenommen wurden, speichere sie
    if not df.equals(edited_df):
        contacts = edited_df.to_dict('records')
        config.update_setting("contacts", contacts)
        st.success("Ansprechpartner aktualisiert!")

# Buttons für Ansprechpartner-Verwaltung
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Zurücksetzen"):
        default_contacts = [
            {"name": "Max Mustermann", "position": "Senior Consultant", "kontakt": "max@example.com"},
            {"name": "Anna Schmidt", "position": "HR Manager", "kontakt": "anna@example.com"}
        ]
        config.update_setting("contacts", default_contacts)
        st.experimental_rerun()

with col2:
    if st.button("Änderungen speichern"):
        st.success("Alle Änderungen wurden gespeichert!")

st.markdown("</div>", unsafe_allow_html=True)

# Container für System-Informationen
st.markdown("<div class='settings-container'>", unsafe_allow_html=True)
st.markdown("## 🖥️ System-Information")

# Tatsächliche Systeminfos anzeigen
import platform
import streamlit as st
import sys

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"**Version:** 2.0.0")
    st.markdown(f"**Letztes Update:** 2025-05-13")
with col2:
    st.markdown(f"**Python Version:** {platform.python_version()}")
    st.markdown(f"**Streamlit Version:** {st.__version__}")

# Exportpfad
export_path = all_settings.get("export_path", "./exports")
new_export_path = st.text_input(
    "Standard-Exportpfad", 
    value=export_path, 
    help="Standardpfad für den Export von Profilen"
)

if new_export_path != export_path:
    config.update_setting("export_path", new_export_path)
    st.success("Exportpfad aktualisiert!")

st.markdown("</div>", unsafe_allow_html=True)

# Container für Hilfe und Support
st.markdown("<div class='settings-container'>", unsafe_allow_html=True)
st.markdown("## ❓ Hilfe & Support")

# Hilfe und Support-Links
st.markdown("""
- **Dokumentation:** [Link zur Dokumentation](https://github.com/yourusername/cv2profile)
- **Support kontaktieren:** support@example.com
- **Probleme melden:** [Issue Tracker](https://github.com/yourusername/cv2profile/issues)
""")

# Zurücksetzen auf Standardeinstellungen
if st.button("Zurücksetzen auf Standardeinstellungen"):
    # Alle Einstellungen auf Standardwerte zurücksetzen
    config.save_settings(config.DEFAULT_SETTINGS)
    st.success("Alle Einstellungen wurden auf Standardwerte zurückgesetzt!")
    st.experimental_rerun()

st.markdown("</div>", unsafe_allow_html=True)

# Speichern-Button am Ende
if st.button("Einstellungen speichern"):
    st.balloons()
    st.success("Alle Einstellungen wurden erfolgreich gespeichert!")

# Footer
st.markdown("""
---
<p style='text-align: center; font-size: 0.8em; opacity: 0.7;'>
    CV2Profile - Einstellungsbereich - © 2025
</p>
""", unsafe_allow_html=True) 