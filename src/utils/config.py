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

# Standardeinstellungen
DEFAULT_SETTINGS = {
    "openai_api_key": "",
    "default_template": "professional",
    "show_extracted_text": False
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