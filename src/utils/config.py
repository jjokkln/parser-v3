"""
Konfigurationsdatei für CV2Profile Konverter
Hier werden Einstellungen wie API-Keys gespeichert
"""

import os
from pathlib import Path
import json

# Pfad zum Konfigurationsverzeichnis und zur Konfigurationsdatei
CONFIG_DIR = Path.home() / ".cv2profile"
CONFIG_FILE = CONFIG_DIR / "settings.json"

# Projektspezifische Konfigurationsdatei
PROJECT_ROOT = Path(__file__).parent.parent.parent  # Gehe von src/utils zu Projektroot
PROJECT_CONFIG_FILE = PROJECT_ROOT / "api_key.json"
BOT_CONFIG_FILE = PROJECT_ROOT / "bot_config.json"

# Standardeinstellungen
DEFAULT_SETTINGS = {
    "openai_api_key": "",
    "default_template": "professional",
    "show_extracted_text": False
}

# Standard Bot-Konfiguration
DEFAULT_BOT_CONFIG = {
    "telegram_token": "",
    "twilio": {
        "account_sid": "",
        "auth_token": "",
        "phone_number": ""
    }
}

def ensure_config_dir():
    """Stellt sicher, dass das Konfigurationsverzeichnis existiert"""
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)

def load_settings():
    """Lädt die Einstellungen aus der Konfigurationsdatei"""
    ensure_config_dir()
    
    if not CONFIG_FILE.exists():
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()
    
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Fehler beim Laden der Einstellungen: {e}")
        return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    """Speichert die Einstellungen in der Konfigurationsdatei"""
    ensure_config_dir()
    
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(settings, f, indent=4)
        return True
    except Exception as e:
        print(f"Fehler beim Speichern der Einstellungen: {e}")
        return False

def get_openai_api_key():
    """Holt den OpenAI API Key aus verschiedenen Quellen in Prioritätsreihenfolge:
    1. Umgebungsvariable
    2. Projektspezifische API-Key-Datei
    3. Streamlit Secrets
    4. Gespeicherte Benutzereinstellungen
    """
    # 1. Zuerst in der Umgebungsvariablen nachsehen (hat höchste Priorität)
    env_key = os.environ.get("OPENAI_API_KEY")
    if env_key:
        return env_key
    
    # 2. Projektspezifische API-Key-Datei prüfen
    if PROJECT_CONFIG_FILE.exists():
        try:
            with open(PROJECT_CONFIG_FILE, "r") as f:
                project_settings = json.load(f)
                if project_settings.get("openai_api_key"):
                    return project_settings["openai_api_key"]
        except Exception as e:
            print(f"Fehler beim Laden der Projekt-API-Key-Datei: {e}")
    
    # 3. Streamlit Secrets prüfen
    try:
        import streamlit as st
        if "openai" in st.secrets and "api_key" in st.secrets["openai"]:
            if st.secrets["openai"]["api_key"]:  # Nur zurückgeben, wenn nicht leer
                return st.secrets["openai"]["api_key"]
    except Exception:
        pass  # Keine Streamlit-Umgebung oder keine Secrets konfiguriert
    
    # 4. Dann in den gespeicherten Benutzereinstellungen nachsehen
    settings = load_settings()
    return settings.get("openai_api_key", "")

def save_openai_api_key(api_key):
    """Speichert den OpenAI API Key in den Einstellungen"""
    settings = load_settings()
    settings["openai_api_key"] = api_key
    return save_settings(settings)

def save_project_api_key(api_key):
    """Speichert den OpenAI API Key in der projektspezifischen Datei"""
    try:
        with open(PROJECT_CONFIG_FILE, "w") as f:
            json.dump({"openai_api_key": api_key}, f, indent=4)
        return True
    except Exception as e:
        print(f"Fehler beim Speichern des Projekt-API-Keys: {e}")
        return False

def get_all_settings():
    """Gibt alle Einstellungen zurück"""
    return load_settings()

def update_setting(key, value):
    """Aktualisiert eine einzelne Einstellung"""
    settings = load_settings()
    settings[key] = value
    return save_settings(settings) 

# Neue Funktionen für Bot-Konfiguration

def load_bot_config():
    """Lädt die Bot-Konfiguration aus der entsprechenden Datei"""
    if not BOT_CONFIG_FILE.exists():
        save_bot_config(DEFAULT_BOT_CONFIG)
        return DEFAULT_BOT_CONFIG.copy()
    
    try:
        with open(BOT_CONFIG_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Fehler beim Laden der Bot-Konfiguration: {e}")
        return DEFAULT_BOT_CONFIG.copy()

def save_bot_config(config):
    """Speichert die Bot-Konfiguration in der entsprechenden Datei"""
    try:
        with open(BOT_CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)
        return True
    except Exception as e:
        print(f"Fehler beim Speichern der Bot-Konfiguration: {e}")
        return False

def get_telegram_bot_token():
    """Holt das Telegram-Bot-Token aus verschiedenen Quellen in Prioritätsreihenfolge:
    1. Umgebungsvariable
    2. Bot-Konfigurationsdatei
    3. Streamlit Secrets
    """
    # 1. Zuerst in der Umgebungsvariablen nachsehen (hat höchste Priorität)
    env_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if env_token:
        return env_token
    
    # 2. Bot-Konfigurationsdatei prüfen
    bot_config = load_bot_config()
    if bot_config.get("telegram_token"):
        return bot_config["telegram_token"]
    
    # 3. Streamlit Secrets prüfen
    try:
        import streamlit as st
        if "telegram" in st.secrets and "bot_token" in st.secrets["telegram"]:
            if st.secrets["telegram"]["bot_token"]:  # Nur zurückgeben, wenn nicht leer
                return st.secrets["telegram"]["bot_token"]
    except Exception:
        pass  # Keine Streamlit-Umgebung oder keine Secrets konfiguriert
    
    return ""

def save_telegram_bot_token(token):
    """Speichert das Telegram-Bot-Token in der Konfiguration"""
    bot_config = load_bot_config()
    bot_config["telegram_token"] = token
    return save_bot_config(bot_config)

def get_twilio_credentials():
    """Holt die Twilio-Credentials aus verschiedenen Quellen in Prioritätsreihenfolge:
    1. Umgebungsvariablen
    2. Bot-Konfigurationsdatei
    3. Streamlit Secrets
    
    Returns:
        tuple: (account_sid, auth_token, phone_number)
    """
    # 1. Zuerst in den Umgebungsvariablen nachsehen (hat höchste Priorität)
    env_account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    env_auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    env_phone_number = os.environ.get("TWILIO_PHONE_NUMBER")
    
    if env_account_sid and env_auth_token and env_phone_number:
        return env_account_sid, env_auth_token, env_phone_number
    
    # 2. Bot-Konfigurationsdatei prüfen
    bot_config = load_bot_config()
    if "twilio" in bot_config:
        twilio_config = bot_config["twilio"]
        account_sid = twilio_config.get("account_sid", "")
        auth_token = twilio_config.get("auth_token", "")
        phone_number = twilio_config.get("phone_number", "")
        
        if account_sid and auth_token and phone_number:
            return account_sid, auth_token, phone_number
    
    # 3. Streamlit Secrets prüfen
    try:
        import streamlit as st
        if "twilio" in st.secrets:
            twilio_secrets = st.secrets["twilio"]
            account_sid = twilio_secrets.get("account_sid", "")
            auth_token = twilio_secrets.get("auth_token", "")
            phone_number = twilio_secrets.get("phone_number", "")
            
            if account_sid and auth_token and phone_number:
                return account_sid, auth_token, phone_number
    except Exception:
        pass  # Keine Streamlit-Umgebung oder keine Secrets konfiguriert
    
    # Wenn keine Credentials gefunden wurden, leere Strings zurückgeben
    return "", "", ""

def save_twilio_credentials(account_sid, auth_token, phone_number):
    """Speichert die Twilio-Credentials in der Konfiguration"""
    bot_config = load_bot_config()
    
    if "twilio" not in bot_config:
        bot_config["twilio"] = {}
    
    bot_config["twilio"]["account_sid"] = account_sid
    bot_config["twilio"]["auth_token"] = auth_token
    bot_config["twilio"]["phone_number"] = phone_number
    
    return save_bot_config(bot_config) 