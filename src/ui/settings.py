"""
Einstellungsseite für CV2Profile Konverter

Diese Datei enthält die Einstellungsseite für den CV2Profile Konverter.
Sie ermöglicht die Verwaltung der API-Keys, Templates und anderen Einstellungen.
"""

import streamlit as st
import os
import sys
from pathlib import Path

# Füge den übergeordneten Ordner zum Pythonpfad hinzu, um relative Importe zu ermöglichen
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Importe aus den reorganisierten Modulen
import src.utils.config as config

def render_settings_page():
    """
    Rendert die Einstellungsseite mit verschiedenen Konfigurationsoptionen
    """
    # Header für die Einstellungsseite mit Glasmorphismus-Effekt
    st.markdown("""
    <div style="background-color: rgba(255, 255, 255, 0.15); padding: 2rem; border-radius: 15px; margin-bottom: 2rem; color: white; text-align: center; backdrop-filter: blur(12px); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25); border: 1px solid rgba(255, 255, 255, 0.18);">
        <h1 style="margin: 0; font-weight: 700; font-size: 2.5rem; text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);">Einstellungen</h1>
        <p style="margin-top: 1rem; font-size: 1.1rem; opacity: 0.95;">Passe die Anwendung an deine Bedürfnisse an und verwalte deine API-Keys.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Lade alle Einstellungen
    all_settings = config.get_all_settings()
    
    # Container für die Einstellungsbereiche
    settings_container = st.container()
    
    with settings_container:
        # OpenAI API Key-Verwaltung
        api_section, template_section, display_section, cache_section = st.tabs([
            "API Einstellungen", 
            "Template-Einstellungen", 
            "Anzeigeoptionen", 
            "Cache-Verwaltung"
        ])
        
        # API Einstellungen
        with api_section:
            st.markdown("""
            <div style="padding: 1rem 0;">
                <h3 style="border-bottom: 1px solid rgba(255, 255, 255, 0.2); padding-bottom: 8px;">OpenAI API Konfiguration</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Lade den aktuellen API-Key
            current_api_key = all_settings.get("openai_api_key", "")
            masked_key = "•" * 16 + current_api_key[-4:] if current_api_key and len(current_api_key) > 4 else ""
            
            # Anzeige des aktuellen Schlüssels
            st.markdown("""
            <div style="background: rgba(255, 255, 255, 0.08); padding: 15px; border-radius: 10px; margin-bottom: 20px;">
                <p style="margin: 0; font-size: 0.9rem; opacity: 0.8;">Aktueller API-Key:</p>
                <p style="margin: 5px 0 0 0; font-family: monospace; font-size: 1rem; letter-spacing: 1px;">
            """, unsafe_allow_html=True)
            
            if current_api_key:
                st.markdown(f"<code>{masked_key}</code>", unsafe_allow_html=True)
            else:
                st.markdown("<em>Kein API-Key gespeichert</em>", unsafe_allow_html=True)
            
            st.markdown("</p></div>", unsafe_allow_html=True)
            
            # Neuen API-Key eingeben
            st.subheader("API-Key bearbeiten")
            new_api_key = st.text_input(
                "Neuer OpenAI API-Key",
                type="password",
                help="Dein API-Key wird benötigt, um die OpenAI-Dienste zu nutzen."
            )
            
            # API-Key speichern
            if new_api_key:
                save_key = st.checkbox("API-Key für zukünftige Sitzungen speichern", value=True,
                                    help="Der API-Key wird lokal auf deinem Computer gespeichert.")
                
                if save_key and st.button("API-Key speichern", key="save_api_key"):
                    # Speichere den API-Key
                    if config.save_openai_api_key(new_api_key):
                        st.session_state.saved_api_key = new_api_key
                        st.success("API-Key erfolgreich gespeichert!")
                    else:
                        st.error("Fehler beim Speichern des API-Keys.")
            
            # Umgebungsvariable Information
            st.divider()
            st.markdown("""
            <div style="background: rgba(255, 255, 255, 0.08); padding: 15px; border-radius: 10px;">
                <h4 style="margin-top: 0;">Alternative: Umgebungsvariable</h4>
                <p>Du kannst deinen API-Key auch als Umgebungsvariable festlegen:</p>
                <code>export OPENAI_API_KEY=sk-...</code>
                <p>Die Umgebungsvariable hat Vorrang vor dem gespeicherten Schlüssel.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Template-Einstellungen
        with template_section:
            st.markdown("""
            <div style="padding: 1rem 0;">
                <h3 style="border-bottom: 1px solid rgba(255, 255, 255, 0.2); padding-bottom: 8px;">Template-Einstellungen</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Template-Auswahl als Voreinstellung
            template_options = {
                "professional": "Professionell", 
                "classic": "Klassisch", 
                "modern": "Modern", 
                "minimalist": "Minimalistisch"
            }
            default_template = all_settings.get("default_template", "professional")
            
            st.markdown("### Standard-Vorlage")
            st.markdown("Wähle die Standard-Vorlage für neue Profile:")
            
            selected_template = st.selectbox(
                "Standard-Vorlage",
                options=list(template_options.keys()),
                format_func=lambda x: template_options[x],
                index=list(template_options.keys()).index(default_template),
                key="settings_template_select"
            )
            
            # Template-Vorschaubilder
            st.markdown("### Vorschau der Vorlagen")
            templates_col1, templates_col2 = st.columns(2)
            
            with templates_col1:
                st.markdown("#### Professionell")
                st.markdown('<div style="background: rgba(255, 255, 255, 0.1); height: 180px; border-radius: 8px; display: flex; align-items: center; justify-content: center;"><p>Vorschau: Professionell</p></div>', unsafe_allow_html=True)
                
                st.markdown("#### Modern")
                st.markdown('<div style="background: rgba(255, 255, 255, 0.1); height: 180px; border-radius: 8px; display: flex; align-items: center; justify-content: center;"><p>Vorschau: Modern</p></div>', unsafe_allow_html=True)
            
            with templates_col2:
                st.markdown("#### Klassisch")
                st.markdown('<div style="background: rgba(255, 255, 255, 0.1); height: 180px; border-radius: 8px; display: flex; align-items: center; justify-content: center;"><p>Vorschau: Klassisch</p></div>', unsafe_allow_html=True)
                
                st.markdown("#### Minimalistisch")
                st.markdown('<div style="background: rgba(255, 255, 255, 0.1); height: 180px; border-radius: 8px; display: flex; align-items: center; justify-content: center;"><p>Vorschau: Minimalistisch</p></div>', unsafe_allow_html=True)
            
            # Speichere die Template-Voreinstellung, wenn sie sich geändert hat
            if selected_template != default_template and st.button("Template-Einstellung speichern", key="save_template"):
                if config.update_setting("default_template", selected_template):
                    st.success(f"Standard-Template auf '{template_options[selected_template]}' gesetzt.")
                else:
                    st.error("Fehler beim Speichern der Template-Einstellung.")
        
        # Anzeigeoptionen
        with display_section:
            st.markdown("""
            <div style="padding: 1rem 0;">
                <h3 style="border-bottom: 1px solid rgba(255, 255, 255, 0.2); padding-bottom: 8px;">Anzeigeoptionen</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Einstellung zum Anzeigen des extrahierten Textes
            show_text_default = all_settings.get("show_extracted_text", False)
            
            st.markdown("### Textextraktion")
            show_text_setting = st.checkbox(
                "Extrahierten Text standardmäßig anzeigen", 
                value=show_text_default,
                key="settings_show_text"
            )
            
            st.markdown("""
            <div style="background: rgba(255, 255, 255, 0.08); padding: 12px; border-radius: 8px; margin: 15px 0;">
                <p style="margin: 0; font-size: 0.95rem;">
                    Diese Option beeinflusst, ob der aus dem Dokument extrahierte Text nach dem Hochladen
                    angezeigt wird. Nützlich zur Überprüfung, ob das Dokument korrekt verarbeitet wurde.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Speichere die Textanzeige-Einstellung, wenn sie sich geändert hat
            if show_text_setting != show_text_default and st.button("Anzeigeoptionen speichern", key="save_display"):
                if config.update_setting("show_extracted_text", show_text_setting):
                    st.success("Anzeigeoptionen erfolgreich gespeichert.")
                else:
                    st.error("Fehler beim Speichern der Anzeigeoptionen.")
            
            # Weitere Anzeigeoptionen könnten hier hinzugefügt werden
            st.markdown("### Weitere Anzeigeoptionen")
            st.markdown("Weitere Anzeigeoptionen werden in zukünftigen Versionen hinzugefügt.")
        
        # Cache-Verwaltung
        with cache_section:
            st.markdown("""
            <div style="padding: 1rem 0;">
                <h3 style="border-bottom: 1px solid rgba(255, 255, 255, 0.2); padding-bottom: 8px;">Cache-Verwaltung</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Cache-Statistiken anzeigen (Dummy-Daten, in einer realen Anwendung würden hier echte Daten angezeigt)
            st.markdown("### Cache-Statistiken")
            
            cache_dir = Path.home() / ".cv2profile" / "cache"
            cache_exists = cache_dir.exists()
            
            if cache_exists:
                cache_files = list(cache_dir.iterdir()) if cache_dir.exists() else []
                cache_size = sum(f.stat().st_size for f in cache_files if f.is_file())
                cache_size_mb = cache_size / (1024 * 1024)
                
                st.markdown(f"""
                <div style="background: rgba(255, 255, 255, 0.08); padding: 15px; border-radius: 10px; margin-bottom: 20px;">
                    <p><strong>Cache-Verzeichnis:</strong> <code>{cache_dir}</code></p>
                    <p><strong>Cache-Größe:</strong> {cache_size_mb:.2f} MB</p>
                    <p><strong>Anzahl der Dateien:</strong> {len(cache_files)}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background: rgba(255, 255, 255, 0.08); padding: 15px; border-radius: 10px; margin-bottom: 20px;">
                    <p>Kein Cache-Verzeichnis gefunden. Es werden noch keine Daten zwischengespeichert.</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Cache leeren
            if st.button("Cache leeren", key="clear_cache"):
                if cache_exists:
                    try:
                        for cache_file in cache_dir.iterdir():
                            if cache_file.is_file():
                                cache_file.unlink()
                        st.success("Cache erfolgreich geleert.")
                    except Exception as e:
                        st.error(f"Fehler beim Leeren des Caches: {str(e)}")
                else:
                    st.info("Kein Cache vorhanden, der geleert werden könnte.")
    
    # Informations-Footer
    st.divider()
    st.markdown("""
    <div style="background: rgba(255, 255, 255, 0.08); padding: 15px; border-radius: 10px; margin-top: 30px;">
        <h4 style="margin-top: 0;">Über CV2Profile</h4>
        <p>CV2Profile ist ein KI-gestützter CV-Parser, der Lebensläufe analysiert und in standardisierte Profile konvertiert.</p>
        <p>Die Anwendung unterstützt verschiedene Dokumentformate (PDF, DOCX, JPG, PNG), extrahiert Text, identifiziert relevante Informationen und erstellt professionelle PDF- und Word-Profile.</p>
    </div>
    """, unsafe_allow_html=True) 