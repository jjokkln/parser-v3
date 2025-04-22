import streamlit as st
import os
import tempfile
import json
import base64
from PIL import Image
import io
from document_processor import DocumentProcessor
from ai_extractor import AIExtractor
from combined_processor import CombinedProcessor  # Import des neuen kombinierten Prozessors
from template_generator import ProfileGenerator
import config  # Importiere das neue Konfigurationsmodul

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
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Sidebar Elemente */
    .sidebar .sidebar-content {
        background-color: transparent !important;
    }
    
    /* Sidebar Header */
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: white !important;
        font-weight: 600 !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
        padding-bottom: 10px !important;
        margin-bottom: 20px !important;
    }
    
    /* Sidebar Divider */
    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.1) !important;
        margin: 20px 0 !important;
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

# Hilfsfunktionen
def reset_session():
    """Setzt die Session zurück"""
    st.session_state.step = 1
    st.session_state.extracted_text = ""
    st.session_state.profile_data = {}
    st.session_state.edited_data = {}
    st.session_state.preview_pdf = None
    # Temporäre Dateien aufräumen
    for temp_file in st.session_state.temp_files:
        try:
            os.unlink(temp_file)
        except:
            pass
    st.session_state.temp_files = []

def display_pdf(file_path):
    """Zeigt ein PDF als Base64-String an"""
    # Prüfe, ob ein gültiger Dateipfad vorhanden ist
    if file_path is None:
        # Zeige eine Fehlermeldung statt des PDFs an
        return '<div style="text-align: center; padding: 20px; background-color: #f8d7da; color: #721c24; border-radius: 5px;">PDF-Vorschau nicht verfügbar. Bitte aktualisieren Sie die Vorschau.</div>'
    
    try:
        with open(file_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        
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

# CSS einbinden
st.markdown(custom_css, unsafe_allow_html=True)

# Header-Bereich mit verbessertem Glasmorphismus-Effekt
st.markdown("""
<div style="background-color: rgba(255, 255, 255, 0.15); padding: 2.5rem; border-radius: 15px; margin-bottom: 2rem; color: white; text-align: center; backdrop-filter: blur(12px); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25); border: 1px solid rgba(255, 255, 255, 0.18);">
    <h1 style="margin: 0; font-weight: 700; font-size: 2.8rem; text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);">CV2Profile Konverter</h1>
    <p style="margin-top: 1rem; font-size: 1.2rem; opacity: 0.95;">Konvertiere deinen Lebenslauf in ein professionelles Profil. Lade deine Datei hoch, wähle die gewünschten Informationen aus und gestalte dein Profil.</p>
</div>
""", unsafe_allow_html=True)

# Prozess-Schritte anzeigen mit verbessertem Design
col1, col2 = st.columns(2)
with col1:
    step1_style = "background-color: white; color: #4527A0; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); transform: scale(1.05);" if st.session_state.step == 1 else "background-color: rgba(255, 255, 255, 0.2); color: white; border: 1px solid rgba(255, 255, 255, 0.3);"
    st.markdown(f'''
    <div style="text-align: center;">
        <div style="display: inline-block; border-radius: 50%; width: 50px; height: 50px; line-height: 50px; font-weight: bold; font-size: 20px; {step1_style}">1</div>
        <p style="color: white; margin-top: 10px; font-weight: {600 if st.session_state.step == 1 else 400}; font-size: 16px; text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);">Analyse & Extraktion</p>
    </div>
    ''', unsafe_allow_html=True)
with col2:
    step2_style = "background-color: white; color: #4527A0; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); transform: scale(1.05);" if st.session_state.step == 2 else "background-color: rgba(255, 255, 255, 0.2); color: white; border: 1px solid rgba(255, 255, 255, 0.3);"
    st.markdown(f'''
    <div style="text-align: center;">
        <div style="display: inline-block; border-radius: 50%; width: 50px; height: 50px; line-height: 50px; font-weight: bold; font-size: 20px; {step2_style}">2</div>
        <p style="color: white; margin-top: 10px; font-weight: {600 if st.session_state.step == 2 else 400}; font-size: 16px; text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);">Profil erstellen</p>
    </div>
    ''', unsafe_allow_html=True)

# Sidebar für Einstellungen
with st.sidebar:
    st.header("Einstellungen")
    
    # Lade den gespeicherten API-Key oder verwende den leeren String
    api_key_value = st.session_state.saved_api_key
    
    # API-Key Eingabefeld
    api_key_input = st.text_input("OpenAI API Key", 
                                 value=api_key_value,
                                 type="password",
                                 help="Dein OpenAI API-Key wird benötigt, um Lebensläufe zu analysieren.")
    
    # Option zum Speichern des API-Keys
    if api_key_input:
        if api_key_input != st.session_state.saved_api_key:
            save_key = st.checkbox("API-Key für zukünftige Sitzungen speichern", value=True,
                                  help="Der API-Key wird lokal auf deinem Computer gespeichert.")
            
            if save_key and st.button("API-Key speichern"):
                # Speichere den API-Key
                config.save_openai_api_key(api_key_input)
                st.session_state.saved_api_key = api_key_input
                st.success("API-Key erfolgreich gespeichert!")
    
    # Zeige Warnung an, wenn kein API-Key vorhanden ist
    if not api_key_input:
        st.warning("Bitte gib deinen OpenAI API Key ein")
    
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
        index=list(template_options.keys()).index(default_template)
    )
    
    # Speichere die Template-Voreinstellung, wenn sie sich geändert hat
    if selected_template != default_template:
        config.update_setting("default_template", selected_template)
    
    # Option zum Anonymisieren als Voreinstellung
    anonymize_default = all_settings.get("anonymize_by_default", False)
    anonymize_setting = st.checkbox(
        "Anonymisierung standardmäßig aktivieren", 
        value=anonymize_default
    )
    
    # Speichere die Anonymisierungseinstellung, wenn sie sich geändert hat
    if anonymize_setting != anonymize_default:
        config.update_setting("anonymize_by_default", anonymize_setting)
    
    # Einstellung zum Anzeigen des extrahierten Textes
    show_text_default = all_settings.get("show_extracted_text", False)
    show_text_setting = st.checkbox(
        "Extrahierten Text standardmäßig anzeigen", 
        value=show_text_default
    )
    
    # Speichere die Textanzeige-Einstellung, wenn sie sich geändert hat
    if show_text_setting != show_text_default:
        config.update_setting("show_extracted_text", show_text_setting)
    
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
    st.subheader("1. Lebenslauf hochladen und analysieren")
    
    # Standardmäßig wird der "Standard (Extraktion → Analyse)"-Modus verwendet
    processing_mode = "Standard (Extraktion → Analyse)"
    
    uploaded_file = st.file_uploader(
        "Wähle eine Datei (PDF, JPEG, PNG oder DOCX)",
        type=["pdf", "jpg", "jpeg", "png", "docx"]
    )
    
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
                
                # Standard-Reihenfolge (Extraktion → Analyse)
                with st.spinner("Extrahiere Text und analysiere Lebenslauf..."):
                    extracted_text, profile_data = combined_processor.process_and_extract(temp_file_path, file_extension)
                # Speichere Ergebnisse in der Session
                st.session_state.extracted_text = extracted_text
                st.session_state.profile_data = profile_data
                
                # Zeige Ergebnisse an
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
                st.success("Dein Lebenslauf wurde erfolgreich analysiert. Jetzt kannst du die gewünschten Informationen auswählen.")
                
                # Großer, zentrierter Button für den Übergang zu Schritt 2
                st.markdown("""
                <style>
                .stButton > button {
                    background-color: rgba(255, 255, 255, 0.7) !important;
                    color: #4527A0 !important;
                    padding: 0.75rem 1.5rem !important;
                    font-size: 1.125rem !important;
                    font-weight: 600 !important;
                    border-radius: 12px !important;
                    border: none !important;
                    cursor: pointer !important;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
                    transition: all 0.3s ease !important;
                    backdrop-filter: blur(10px) !important;
                    -webkit-backdrop-filter: blur(10px) !important;
                    min-width: 300px !important;
                    text-align: center !important;
                }
                .stButton > button:hover {
                    background-color: white !important;
                    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3) !important;
                    transform: translateY(-2px) !important;
                }
                .stButton > button p {
                    color: #4527A0 !important;
                    font-weight: 600 !important;
                }
                </style>
                """, unsafe_allow_html=True)
                
                # Verwende Spalten für Zentrierung
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("Weiter zu Schritt 2: Informationen auswählen"):
                        st.session_state.step = 2
                        st.rerun()
            
            except Exception as e:
                st.error(f"Fehler bei der Verarbeitung: {str(e)}")
    
    elif uploaded_file and not openai_api_key:
        st.warning("Bitte gib einen OpenAI API Key in der Seitenleiste ein, um fortzufahren.")

elif st.session_state.step == 2:
    # Schritt 2: Kombiniert Informationen auswählen und Profil generieren
    st.subheader("2. Profil erstellen und exportieren")
    
    # Profildaten aus der Session holen
    profile_data = st.session_state.profile_data
    edited_data = {}
    
    # Zwei Tabs erstellen für Informationsauswahl und Profil-Generierung
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
        
        # Weitere persönliche Daten
        col1, col2 = st.columns(2)
        with col1:
            edited_data["führerschein"] = st.text_input("Führerschein", value=personal_data.get("führerschein", ""))
        with col2:
            edited_data["wunschgehalt"] = st.text_input("Wunschgehalt", value=profile_data.get("wunschgehalt", ""))
        
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
                index=default_index
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
                }
            },
            "berufserfahrung": edited_experience,
            "ausbildung": edited_education,
            "weiterbildungen": edited_training,
            "wunschgehalt": edited_data.get("wunschgehalt", "")
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
        
        # Profildaten aus der Session holen
        edited_data = st.session_state.edited_data
        
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
                
        with col2:
            modern = st.button("🟢 🟢\nModern", 
                              use_container_width=True,
                              type="primary" if default_template == "modern" else "secondary")
            if modern:
                template_to_use = "modern"
                
        with col3:
            professional = st.button("🟣 🟣\nProfessionell", 
                                   use_container_width=True,
                                   type="primary" if default_template == "professional" else "secondary")
            if professional:
                template_to_use = "professional"
                
        with col4:
            minimalistic = st.button("⚫ ⚫\nMinimalistisch", 
                                   use_container_width=True,
                                   type="primary" if default_template == "minimalist" else "secondary")
            if minimalistic:
                template_to_use = "minimalist"
                
        # Als Standard für zukünftige Verwendung speichern
        if template_to_use != default_template:
            if st.button("Als Standard-Vorlage festlegen"):
                config.update_setting("default_template", template_to_use)
                st.success(f"'{template_to_use}' wurde als Standard-Vorlage gespeichert!")
        
        # Option zum Anonymisieren der persönlichen Daten
        anonymize = st.checkbox("Persönliche Daten anonymisieren", value=False)
        st.caption("Maskiert Name, Wohnort, Kontaktdaten und andere persönliche Informationen im generierten Profil.")
        
        # Wenn anonymisieren gewählt wurde, die Daten entsprechend anpassen
        if anonymize:
            edited_data_copy = edited_data.copy()
            # Persönliche Daten anonymisieren
            edited_data_copy["persönliche_daten"]["name"] = "XXXXX XXXXX"
            edited_data_copy["persönliche_daten"]["wohnort"] = "XXXXX XXXXX"
            edited_data_copy["persönliche_daten"]["kontakt"]["email"] = "xxxxx@xxxxx.xx"
            edited_data_copy["persönliche_daten"]["kontakt"]["telefon"] = "XXXX XXXXXXXX"
            profile_data_to_use = edited_data_copy
        else:
            profile_data_to_use = edited_data
        
        # Profil-Vorschau generieren und anzeigen
        if 'preview_pdf' not in st.session_state or st.button("Vorschau aktualisieren"):
            with st.spinner("Profil wird generiert..."):
                try:
                    generator = ProfileGenerator()
                    output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                    output_path = output_file.name
                    output_file.close()
                    st.session_state.temp_files.append(output_path)
                    
                    # Generiere Profil mit dem ausgewählten Template
                    profile_path = generator.generate_profile(profile_data_to_use, output_path, template=template_to_use)
                    st.session_state.preview_pdf = profile_path
                    
                    # Zeige eine Erfolgsmeldung an
                    st.success("Profil erfolgreich generiert!")
                except Exception as e:
                    st.error(f"Fehler bei der Generierung des Profils: {str(e)}")
        
        # PDF-Vorschau anzeigen
        if st.session_state.preview_pdf:
            st.markdown("#### Profil-Vorschau")
            pdf_display = display_pdf(st.session_state.preview_pdf)
            st.markdown(pdf_display, unsafe_allow_html=True)
            
            # Download-Button für die PDF-Datei
            name = profile_data_to_use["persönliche_daten"]["name"].replace(" ", "_")
            if name == "XXXXX_XXXXX":
                name = "Anonymes_Profil"
            elif not name or name == "":
                name = "Profil"
            
            with open(st.session_state.preview_pdf, "rb") as file:
                st.download_button(
                    label="Profil herunterladen",
                    data=file,
                    file_name=f"{name}_Profil.pdf",
                    mime="application/pdf"
                )
    
    # Navigation
    if st.button("Zurück zu Schritt 1"):
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
                except Exception as e:
                    print(f"Fehler beim Löschen der temporären Datei {temp_file}: {str(e)}")
    except Exception as e:
        print(f"Fehler beim Aufräumen: {str(e)}")

# Cleanup-Funktion registrieren
import atexit
atexit.register(cleanup)
