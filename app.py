import streamlit as st
import os
import tempfile
import json
import base64
from PIL import Image
import io
from document_processor import DocumentProcessor
from ai_extractor import AIExtractor
from template_generator import ProfileGenerator
import config  # Importiere das neue Konfigurationsmodul

# Session State für den mehrstufigen Prozess initialisieren
if 'step' not in st.session_state:
    st.session_state.step = 1  # Schritt 1: Datei hochladen
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

# Header-Bereich
st.markdown("""
<div style="background-color: #4527A0; padding: 1.5rem; border-radius: 5px; margin-bottom: 1rem; color: white; text-align: center;">
    <h1 style="margin: 0;">CV2Profile Konverter</h1>
    <p style="margin-top: 0.5rem;">Konvertiere deinen Lebenslauf in ein professionelles Profil. Lade deine Datei hoch, wähle die gewünschten Informationen aus und gestalte dein Profil.</p>
</div>
""", unsafe_allow_html=True)

# Prozess-Schritte anzeigen
col1, col2, col3 = st.columns(3)
with col1:
    step1_style = "background-color: #4527A0; color: white;" if st.session_state.step == 1 else "color: gray;"
    st.markdown(f'<div style="text-align: center;"><div style="display: inline-block; border-radius: 50%; width: 30px; height: 30px; line-height: 30px; {step1_style}">1</div><p>Lebenslauf hochladen</p></div>', unsafe_allow_html=True)
with col2:
    step2_style = "background-color: #4527A0; color: white;" if st.session_state.step == 2 else "color: gray;"
    st.markdown(f'<div style="text-align: center;"><div style="display: inline-block; border-radius: 50%; width: 30px; height: 30px; line-height: 30px; {step2_style}">2</div><p>Informationen auswählen</p></div>', unsafe_allow_html=True)
with col3:
    step3_style = "background-color: #4527A0; color: white;" if st.session_state.step == 3 else "color: gray;"
    st.markdown(f'<div style="text-align: center;"><div style="display: inline-block; border-radius: 50%; width: 30px; height: 30px; line-height: 30px; {step3_style}">3</div><p>Profil generieren</p></div>', unsafe_allow_html=True)

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
    # Schritt 1: Datei hochladen und Text extrahieren
    st.subheader("1. Lebenslauf hochladen")
    
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
                # Datei verarbeiten und Text extrahieren
                processor = DocumentProcessor()
                extracted_text = processor.process_document(temp_file_path, file_extension)
                
                # Extrahierten Text in der Session speichern
                st.session_state.extracted_text = extracted_text
                
                # Zeige den extrahierten Text an, basierend auf der Einstellung
                st.subheader("Extrahierter Text")
                st.write(f"Wir haben folgenden Text aus deinem Lebenslauf extrahiert:")
                
                # Verwende die Einstellung zur Anzeige des extrahierten Textes
                show_text = config.get_all_settings().get("show_extracted_text", False)
                with st.expander("Extrahierten Text anzeigen", expanded=show_text):
                    st.text_area("Extrahierter Text", extracted_text, height=300)
                
                # KI-Extraktion der Profildaten
                extractor = AIExtractor(openai_api_key)
                
                # Extrahiere alle verfügbaren Informationen
                with st.spinner("Analysiere Lebenslauf mit KI..."):
                    profile_data = extractor.extract_profile_data(extracted_text, file_extension)
                    st.session_state.profile_data = profile_data
                
                # Zeige einen Erfolgshinweis an
                st.success("Dein Lebenslauf wurde erfolgreich analysiert. Jetzt kannst du die gewünschten Informationen auswählen.")
                
                # Button für den nächsten Schritt
                if st.button("Weiter zu Schritt 2: Informationen auswählen"):
                    st.session_state.step = 2
                    st.rerun()
            
            except Exception as e:
                st.error(f"Fehler bei der Verarbeitung: {str(e)}")
    
    elif uploaded_file and not openai_api_key:
        st.warning("Bitte gib einen OpenAI API Key in der Seitenleiste ein, um fortzufahren.")

elif st.session_state.step == 2:
    # Schritt 2: Informationen auswählen und bearbeiten
    st.subheader("2. Gewünschte Informationen auswählen")
    
    profile_data = st.session_state.profile_data
    edited_data = {}
    
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
        "weiterbildungen": edited_training
    }
    
    # Speichern der bearbeiteten Daten in der Session
    st.session_state.edited_data = complete_edited_data
    
    # Prüfen auf Vollständigkeit der kritischen Daten
    validation_errors = []
    if not edited_data.get("name"):
        validation_errors.append("Name fehlt")
    if not edited_data.get("email") and not edited_data.get("telefon"):
        validation_errors.append("Mindestens eine Kontaktmöglichkeit (E-Mail oder Telefon) wird benötigt")
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Zurück zu Schritt 1"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        # Wenn es Validierungsfehler gibt, diese anzeigen
        if validation_errors:
            for error in validation_errors:
                st.error(error)
            st.button("Weiter zu Schritt 3: Profil generieren", disabled=True)
        else:
            if st.button("Weiter zu Schritt 3: Profil generieren"):
                st.session_state.step = 3
                st.rerun()

elif st.session_state.step == 3:
    # Schritt 3: Profil generieren und Vorschau anzeigen
    st.subheader("3. Profil generieren")
    
    # Profildaten aus der Session holen
    edited_data = st.session_state.edited_data
    
    # Vorlage auswählen
    st.markdown("### Vorlage auswählen")
    
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
                
                profile_path = generator.generate_profile(profile_data_to_use, output_path)
                st.session_state.preview_pdf = profile_path
            except Exception as e:
                st.error(f"Fehler bei der Generierung des Profils: {str(e)}")
                st.session_state.preview_pdf = None
    
    # Vorschau anzeigen
    st.markdown("### Vorschau")
    st.components.v1.html(display_pdf(st.session_state.preview_pdf), height=850)
    
    # Alternative PDF-Anzeige
    if st.session_state.preview_pdf and os.path.exists(st.session_state.preview_pdf):
        st.markdown("#### Falls die PDF-Vorschau nicht angezeigt wird:")
        col1, col2 = st.columns([1, 3])
        with col1:
            with open(st.session_state.preview_pdf, "rb") as file:
                st.download_button(
                    label="PDF direkt herunterladen",
                    data=file,
                    file_name="vorschau.pdf",
                    mime="application/pdf"
                )
        with col2:
            st.markdown("Chrome blockiert manchmal die Anzeige von PDFs aus Sicherheitsgründen. "
                      "Sie können die PDF-Datei herunterladen und auf Ihrem Computer öffnen.")
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Zurück zu Schritt 2"):
            st.session_state.step = 2
            st.rerun()
    with col2:
        # Download-Button für das generierte Profil
        if st.session_state.preview_pdf and os.path.exists(st.session_state.preview_pdf):
            with open(st.session_state.preview_pdf, "rb") as file:
                name = profile_data_to_use.get("persönliche_daten", {}).get("name", "profil")
                st.download_button(
                    label="PDF herunterladen",
                    data=file,
                    file_name=f"{name}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
        else:
            st.button("PDF herunterladen", disabled=True, use_container_width=True)
            st.info("Bitte aktualisieren Sie die Vorschau, um das PDF herunterzuladen.")

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
