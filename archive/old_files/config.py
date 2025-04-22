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

# Standardeinstellungen
DEFAULT_SETTINGS = {
    "openai_api_key": "",
    "default_template": "professional",
    "show_extracted_text": False,
    "anonymize_by_default": False
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
    """Holt den OpenAI API Key aus den Einstellungen oder der Umgebungsvariablen"""
    # Zuerst in der Umgebungsvariablen nachsehen (hat Vorrang)
    env_key = os.environ.get("OPENAI_API_KEY")
    if env_key:
        return env_key
    
    # Dann in den gespeicherten Einstellungen nachsehen
    settings = load_settings()
    return settings.get("openai_api_key", "")

def save_openai_api_key(api_key):
    """Speichert den OpenAI API Key in den Einstellungen"""
    settings = load_settings()
    settings["openai_api_key"] = api_key
    return save_settings(settings)

def get_all_settings():
    """Gibt alle Einstellungen zurück"""
    return load_settings()

def update_setting(key, value):
    """Aktualisiert eine einzelne Einstellung"""
    settings = load_settings()
    settings[key] = value
    return save_settings(settings) 