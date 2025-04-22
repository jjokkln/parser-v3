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

# Ersetze die Verarbeitungsmodus-Auswahl mit einem festen Standard-Modus
# Suche nach dem Abschnitt
section_start = content.find("# Auswahlmöglichkeit für die Verarbeitungsreihenfolge hinzufügen")
section_end = content.find("uploaded_file = st.file_uploader", section_start)

# Wenn beide Punkte gefunden wurden, ersetze den Abschnitt
if section_start != -1 and section_end != -1:
    replacement = "# Standardmäßig wird der \"Standard (Extraktion → Analyse)\"-Modus verwendet\n    processing_mode = \"Standard (Extraktion → Analyse)\"\n\n    "
    content = content[:section_start] + replacement + content[section_end:]

# Suche nach dem ersten Verarbeitungsblock
process_start = content.find("# Verarbeite das Dokument im ausgewählten Modus")
if_statement = "if \"Umgekehrt\" in processing_mode:"
process_if_start = content.find(if_statement, process_start)
process_else = content.find("else:", process_if_start)
process_else_end = content.find("# Standard-Reihenfolge (Extraktion → Analyse)", process_else)
process_block_end = content.find("# Speichere Ergebnisse in der Session", process_else_end)

# Wenn alle relevanten Punkte gefunden wurden, ersetze den Abschnitt
if process_start != -1 and process_if_start != -1 and process_else != -1 and process_else_end != -1 and process_block_end != -1:
    # Extrahiere den Standard-Modus-Code
    standard_mode_start = content.find("# Standard-Reihenfolge (Extraktion → Analyse)", process_else)
    standard_mode_block = content[standard_mode_start:process_block_end]
    # Setze ein neues Block zusammen
    replacement = "# Standard-Reihenfolge (Extraktion → Analyse)\n                with st.spinner(\"Extrahiere Text und analysiere Lebenslauf...\"):\n                    extracted_text, profile_data = combined_processor.process_and_extract(temp_file_path, file_extension)\n                "
    content = content[:process_start] + replacement + content[process_block_end:]

# Suche nach dem zweiten Block (Anzeige der Ergebnisse)
results_start = content.find("# Zeige Ergebnisse basierend auf dem ausgewählten Modus")
results_if_start = content.find(if_statement, results_start)
results_else = content.find("else:", results_if_start)
results_else_content_start = content.find("# Zeige zuerst den extrahierten Text an", results_else)
results_block_end = content.find("# Zeige einen Erfolgshinweis an")

# Wenn alle relevanten Punkte gefunden wurden, ersetze den Abschnitt
if results_start != -1 and results_if_start != -1 and results_else != -1 and results_else_content_start != -1 and results_block_end != -1:
    # Extrahiere den Standard-Ansicht-Code
    standard_view_start = content.find("# Zeige zuerst den extrahierten Text an", results_else)
    standard_view_end = results_block_end
    standard_view_block = content[standard_view_start:standard_view_end]
    
    # Ersetze den gesamten Block
    replacement = "# Zeige Ergebnisse an\n                # Zeige zuerst den extrahierten Text an\n                st.subheader(\"Extrahierter Text\")\n                \n                # Verwende die Einstellung zur Anzeige des extrahierten Textes\n                show_text = config.get_all_settings().get(\"show_extracted_text\", False)\n                with st.expander(\"Extrahierten Text anzeigen\", expanded=show_text):\n                    st.text_area(\"Extrahierter Text\", extracted_text, height=300)\n                \n                # Dann die Profildaten\n                st.subheader(\"Analysierte Daten\")\n                with st.expander(\"Analysierte Daten anzeigen\", expanded=True):\n                    st.json(profile_data)\n                "
    content = content[:results_start] + replacement + content[results_block_end:]

# Schreibe die geänderte Datei
with open('app_ui_fixed_new.py', 'w') as f:
    f.write(content)

print("Die Datei wurde erfolgreich mit UI-Verbesserungen aktualisiert und als app_ui_fixed_new.py gespeichert!") 