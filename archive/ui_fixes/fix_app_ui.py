#!/usr/bin/env python3

import re

# Lese die Datei ein
with open('app_original.py', 'r') as f:
    content = f.read()

# Ersetze das CSS für Schaltflächen mit Glasmorphismus-Stil
glass_css = """<style>
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
</style>"""

# Ersetze das gesamte CSS mit dem neuen Glasmorphismus-CSS
content = re.sub(r'<style>.*?</style>', glass_css, content, flags=re.DOTALL)

# Entferne Verarbeitungsmodus-Auswahl
content = re.sub(
    r'# Auswahlmöglichkeit für die Verarbeitungsreihenfolge hinzufügen.*?uploaded_file = st\.file_uploader',
    '# Standardmäßig wird der "Standard (Extraktion → Analyse)"-Modus verwendet\n    processing_mode = "Standard (Extraktion → Analyse)"\n\n    uploaded_file = st.file_uploader',
    content,
    flags=re.DOTALL
)

# Entferne die erste Bedingungsprüfung für den Verarbeitungsmodus
content = re.sub(
    r'# Verarbeite das Dokument im ausgewählten Modus.*?else:.*?# Standard-Reihenfolge \(Extraktion → Analyse\)',
    '# Standard-Reihenfolge (Extraktion → Analyse)',
    content,
    flags=re.DOTALL
)

# Entferne die zweite Bedingungsprüfung für den Verarbeitungsmodus
content = re.sub(
    r'# Zeige Ergebnisse basierend auf dem ausgewählten Modus.*?else:',
    '# Zeige Ergebnisse an',
    content,
    flags=re.DOTALL
)

# Schreibe die geänderte Datei
with open('app_ui_fixed.py', 'w') as f:
    f.write(content)

print("Die Datei wurde erfolgreich mit UI-Verbesserungen aktualisiert und als app_ui_fixed.py gespeichert!")