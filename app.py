import streamlit as st
import os
import tempfile
import json
from PIL import Image
import io
from document_processor import DocumentProcessor
from ai_extractor import AIExtractor
from template_generator import ProfileGenerator

# Seitentitel und Konfiguration
st.set_page_config(page_title="CV Parser", layout="wide")
st.title("Dokumentenanalyse und Profilgenerator")

# Sidebar für Einstellungen
with st.sidebar:
    st.header("Einstellungen")
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    if not openai_api_key:
        st.warning("Bitte gib deinen OpenAI API Key ein")
    
    st.divider()
    st.markdown("### Über diese App")
    st.markdown("""
    Diese App extrahiert Daten aus Lebensläufen (PDF, JPEG, PNG, DOCX) 
    und erstellt daraus standardisierte Profile.
    """)

# Hauptbereich
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
        
        try:
            # Datei verarbeiten und Text extrahieren
            processor = DocumentProcessor()
            extracted_text = processor.process_document(temp_file_path, file_extension)
            
            # KI-Extraktion der Profildaten
            extractor = AIExtractor(openai_api_key)
            profile_data = extractor.extract_profile_data(extracted_text, file_extension)
            
            # Anzeige der extrahierten Daten zur Überprüfung
            st.subheader("Extrahierte Daten")
            
            # Bearbeitbare Ansicht der extrahierten Daten
            with st.expander("Daten bearbeiten", expanded=True):
                edited_data = {}
                
                # Persönliche Daten
                st.markdown("#### Persönliche Daten")
                col1, col2 = st.columns(2)
                with col1:
                    edited_data["name"] = st.text_input("Name", value=profile_data.get("persönliche_daten", {}).get("name", ""))
                    edited_data["wohnort"] = st.text_input("Wohnort", value=profile_data.get("persönliche_daten", {}).get("wohnort", ""))
                with col2:
                    edited_data["jahrgang"] = st.text_input("Jahrgang", value=profile_data.get("persönliche_daten", {}).get("jahrgang", ""))
                    edited_data["führerschein"] = st.text_input("Führerschein", value=profile_data.get("persönliche_daten", {}).get("führerschein", ""))
                
                # Kontakt
                st.markdown("#### Kontaktinformationen")
                kontakt = profile_data.get("persönliche_daten", {}).get("kontakt", {})
                col1, col2 = st.columns(2)
                with col1:
                    edited_data["ansprechpartner"] = st.text_input("Ansprechpartner", value=kontakt.get("ansprechpartner", ""))
                with col2:
                    edited_data["telefon"] = st.text_input("Telefon", value=kontakt.get("telefon", ""))
                edited_data["email"] = st.text_input("E-Mail", value=kontakt.get("email", ""))
                
                # Berufserfahrung
                st.markdown("#### Berufserfahrung")
                # Im echten Projekt würden hier editierbare Felder für alle Berufserfahrungen stehen
                
                # Beispielhafte Ansicht der Berufserfahrung
                for idx, erfahrung in enumerate(profile_data.get("berufserfahrung", [])):
                    st.markdown(f"**{erfahrung.get('zeitraum')}: {erfahrung.get('position')} bei {erfahrung.get('unternehmen')}**")
                    st.markdown("Aufgaben:")
                    for aufgabe in erfahrung.get("aufgaben", []):
                        st.markdown(f"- {aufgabe}")
                    st.divider()
            
            # Generiere Profil-Dokument
            if st.button("Profil generieren"):
                with st.spinner("Profil wird erstellt..."):
                    generator = ProfileGenerator()
                    output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                    output_path = output_file.name
                    output_file.close()
                    
                    # Profil mit aktualisierten Daten generieren
                    # Für dieses Beispiel nutzen wir die ursprünglichen Daten
                    # In einer vollständigen Implementierung würden die bearbeiteten Daten verwendet
                    profile_path = generator.generate_profile(profile_data, output_path)
                    
                    # Download-Button für das generierte Profil
                    with open(profile_path, "rb") as file:
                        st.download_button(
                            label="Profil herunterladen",
                            data=file,
                            file_name=f"{profile_data.get('persönliche_daten', {}).get('name', 'profil')}.pdf",
                            mime="application/pdf"
                        )
        
        except Exception as e:
            st.error(f"Fehler bei der Verarbeitung: {str(e)}")
        
        finally:
            # Temporäre Dateien aufräumen
            try:
                os.unlink(temp_file_path)
            except:
                pass

elif uploaded_file and not openai_api_key:
    st.warning("Bitte gib einen OpenAI API Key in der Seitenleiste ein, um fortzufahren.")

# Footer
st.divider()
st.markdown("Dokumentenanalyse-App mit KI-Integration | 2025")

if __name__ == "__main__":
    # Hier könnten Initialisierungen stehen, wenn nötig
    pass
