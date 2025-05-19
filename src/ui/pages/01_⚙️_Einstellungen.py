"""
Einstellungsseite für CV2Profile Konverter
"""

import streamlit as st
import os
import sys
from pathlib import Path

# Füge den übergeordneten Ordner zum Pythonpfad hinzu, um relative Importe zu ermöglichen
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from src.utils.config import (
    get_openai_api_key, save_openai_api_key, save_project_api_key, 
    get_all_settings, update_setting,
    get_telegram_bot_token, save_telegram_bot_token,
    get_twilio_credentials, save_twilio_credentials
)

# Seitentitel
st.set_page_config(
    page_title="CV2Profile Einstellungen",
    page_icon="⚙️",
    layout="wide"
)

# CSS für Glasmorphismus-Effekt
st.markdown("""
<style>
    .glass-container {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 15px;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        padding: 20px 25px;
        margin-bottom: 20px;
    }
    
    .glass-title {
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 15px;
        color: white;
    }
    
    .glass-header {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 30px;
        color: white;
        text-align: center;
    }
    
    .nav-button {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        backdrop-filter: blur(5px);
        -webkit-backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 10px 15px;
        color: white;
        text-align: center;
        margin: 5px 0;
        transition: all 0.3s ease;
    }
    
    .nav-button:hover {
        background: rgba(255, 255, 255, 0.3);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Zurück-Button
st.markdown("""
<div class="nav-button" onclick="window.location.href='/'">🔙 Zurück zum Konverter</div>
""", unsafe_allow_html=True)

# Überschrift
st.markdown("<div class='glass-header'>⚙️ Einstellungen</div>", unsafe_allow_html=True)

# Tabs für verschiedene Einstellungsbereiche
tabs = st.tabs(["Allgemein", "API-Keys", "Bots & Messengers"])

# Tab 1: Allgemeine Einstellungen
with tabs[0]:
    st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
    st.markdown("<div class='glass-title'>🔍 Anzeigeoptionen</div>", unsafe_allow_html=True)
    
    # Aktuellen Stand der Einstellungen laden
    settings = get_all_settings()
    
    # Zeige extrahierten Text an (ja/nein)
    show_text = st.checkbox(
        "Extrahierten Text anzeigen", 
        value=settings.get("show_extracted_text", False),
        help="Zeigt den extrahierten Rohtext zur Überprüfung an"
    )
    if show_text != settings.get("show_extracted_text", False):
        update_setting("show_extracted_text", show_text)
        st.success("Einstellung gespeichert!")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
    st.markdown("<div class='glass-title'>📋 Standard-Template</div>", unsafe_allow_html=True)
    
    # Auswahl des Standard-Templates
    template_options = ["Classic", "Modern", "Professional", "Minimalist"]
    default_template = st.selectbox(
        "Standard-Template für die Profilgenerierung", 
        options=template_options,
        index=template_options.index(settings.get("default_template", "professional").capitalize()) 
            if settings.get("default_template", "professional").capitalize() in template_options 
            else 2,
        help="Dieses Template wird standardmäßig für die Profilgenerierung verwendet"
    )
    
    # Template-Vorschau als Beispielbild
    template_images = {
        "Classic": "https://example.com/images/classic_template.jpg",
        "Modern": "https://example.com/images/modern_template.jpg",
        "Professional": "https://example.com/images/professional_template.jpg",
        "Minimalist": "https://example.com/images/minimalist_template.jpg"
    }
    
    # Wenn ein Button angeklickt wird, speichere die Auswahl
    if st.button("Als Standard speichern"):
        update_setting("default_template", default_template.lower())
        st.success(f"'{default_template}' wurde als Standard-Template gespeichert!")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Tab 2: API-Keys
with tabs[1]:
    st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
    st.markdown("<div class='glass-title'>🔑 OpenAI API-Key Verwaltung</div>", unsafe_allow_html=True)
    
    # Aktuellen API-Key anzeigen (teils maskiert)
    current_key = get_openai_api_key()
    if current_key:
        masked_key = current_key[:4] + "*" * (len(current_key) - 8) + current_key[-4:]
        st.info(f"Aktueller API-Key: {masked_key}")
    else:
        st.warning("Kein API-Key konfiguriert!")
    
    # API-Key eingeben
    with st.form("api_key_form"):
        api_key = st.text_input(
            "OpenAI API-Key eingeben",
            type="password",
            placeholder="sk-..."
        )
        
        col1, col2 = st.columns(2)
        with col1:
            save_to_user = st.form_submit_button("In Benutzereinstellungen speichern")
        with col2:
            save_to_project = st.form_submit_button("Im Projekt speichern")
        
        if save_to_user and api_key:
            if save_openai_api_key(api_key):
                st.success("API-Key wurde in den Benutzereinstellungen gespeichert!")
            else:
                st.error("Fehler beim Speichern des API-Keys.")
                
        if save_to_project and api_key:
            if save_project_api_key(api_key):
                st.success("API-Key wurde im Projekt gespeichert!")
            else:
                st.error("Fehler beim Speichern des API-Keys im Projekt.")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Tab 3: Bots & Messengers
with tabs[2]:
    st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
    st.markdown("<div class='glass-title'>🤖 Telegram Bot-Konfiguration</div>", unsafe_allow_html=True)
    
    # Aktuellen Token anzeigen (teils maskiert)
    current_token = get_telegram_bot_token()
    if current_token:
        masked_token = current_token[:4] + "*" * (len(current_token) - 8) + current_token[-4:]
        st.info(f"Aktueller Bot-Token: {masked_token}")
    else:
        st.info("Kein Telegram-Bot-Token konfiguriert. [So erstellen Sie einen Bot mit @BotFather](https://core.telegram.org/bots/tutorial)")
    
    # Bot Token eingeben
    with st.form("telegram_bot_form"):
        bot_token = st.text_input(
            "Telegram Bot-Token eingeben",
            type="password",
            placeholder="123456789:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
        )
        
        save_token = st.form_submit_button("Token speichern")
        
        if save_token and bot_token:
            if save_telegram_bot_token(bot_token):
                st.success("Telegram Bot-Token wurde gespeichert!")
            else:
                st.error("Fehler beim Speichern des Bot-Tokens.")
    
    # Anleitung zum Starten des Bots
    st.markdown("""
    ### Bot starten
    
    Um den Telegram-Bot zu starten, führen Sie diesen Befehl in einem Terminal aus:
    
    ```bash
    ./bot_run.sh --telegram
    ```
    
    Oder direkt mit Python:
    
    ```bash
    python src/bot_service.py --telegram
    ```
    """)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
    st.markdown("<div class='glass-title'>📱 WhatsApp-Integration (Twilio)</div>", unsafe_allow_html=True)
    
    # Aktuelle Twilio-Credentials anzeigen (teils maskiert)
    account_sid, auth_token, phone_number = get_twilio_credentials()
    
    if account_sid and auth_token and phone_number:
        masked_sid = account_sid[:4] + "*" * (len(account_sid) - 8) + account_sid[-4:]
        masked_token = auth_token[:4] + "*" * (len(auth_token) - 8) + auth_token[-4:]
        st.info(f"Aktuelle Twilio-Konfiguration:\n- Account SID: {masked_sid}\n- Auth Token: {masked_token}\n- Telefonnummer: {phone_number}")
    else:
        st.info("Keine Twilio-Credentials konfiguriert. [Registrieren Sie sich bei Twilio](https://www.twilio.com/)")
    
    # Twilio-Credentials eingeben
    with st.form("twilio_form"):
        twilio_sid = st.text_input(
            "Twilio Account SID",
            type="password",
            placeholder="ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        )
        
        twilio_token = st.text_input(
            "Twilio Auth Token",
            type="password",
            placeholder="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        )
        
        twilio_phone = st.text_input(
            "Twilio WhatsApp-Nummer",
            placeholder="+491234567890"
        )
        
        save_twilio = st.form_submit_button("Credentials speichern")
        
        if save_twilio and twilio_sid and twilio_token and twilio_phone:
            if save_twilio_credentials(twilio_sid, twilio_token, twilio_phone):
                st.success("Twilio-Credentials wurden gespeichert!")
            else:
                st.error("Fehler beim Speichern der Twilio-Credentials.")
    
    # Anleitung zum Starten des Webhook-Servers
    st.markdown("""
    ### Webhook-Server starten
    
    Um den WhatsApp-Webhook-Server zu starten, führen Sie diesen Befehl in einem Terminal aus:
    
    ```bash
    ./bot_run.sh --whatsapp
    ```
    
    Oder direkt mit Python:
    
    ```bash
    python src/bot_service.py --whatsapp
    ```
    
    #### Öffentlich zugänglich machen
    
    Damit Twilio Ihren Webhook erreichen kann, müssen Sie ihn öffentlich zugänglich machen. Dafür können Sie einen Dienst wie [ngrok](https://ngrok.com/) verwenden:
    
    ```bash
    ngrok http 5000
    ```
    
    Die generierte URL (z.B. `https://abc123.ngrok.io`) müssen Sie dann in Ihrem Twilio-Dashboard als Webhook-URL eintragen:
    
    ```
    https://abc123.ngrok.io/webhook/whatsapp
    ```
    """)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Footer-Informationen
st.markdown("""
---
<div style="text-align: center; color: rgba(255, 255, 255, 0.5); font-size: 0.8rem; margin-top: 20px;">
    CV2Profile Konverter • Version 6.0 • © 2023-2024
</div>
""", unsafe_allow_html=True) 