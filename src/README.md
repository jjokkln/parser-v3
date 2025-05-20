# src - Quellcode-Verzeichnis

Dieses Verzeichnis enthält den Hauptquellcode des CV2Profile-Parsers, der in verschiedene Module unterteilt ist.

## Struktur

- **core/**: Enthält die Kernfunktionalität für die Dokumentenverarbeitung und KI-gestützte Informationsextraktion
  - `ai_extractor.py` - OpenAI-Integration und Datenextraktion
  - `combined_processor.py` - Kombinierte Verarbeitungslogik
  - `document_processor.py` - Dokumentenverarbeitung (PDF, DOCX, Bilder)

- **templates/**: Enthält den Code für die Profilgenerierung
  - `template_generator.py` - Generierung von PDF-Profilen in verschiedenen Designs

- **ui/**: Enthält die Benutzeroberflächen-Module
  - `app.py` - Hauptanwendung (Streamlit-Oberfläche)
  - `Home.py` - Homepage der Anwendung
  - `pages/` - Enthält zusätzliche Seiten wie die Einstellungsseite

- **utils/**: Enthält verschiedene Hilfsfunktionen
  - `config.py` - Konfigurationsmanagement (API-Keys, etc.)
  - `image_utils.py` - Bild-Utilities für HTTPS-Kompatibilität
  - `telegram_bot.py` - Funktionalität für Telegram-Bot-Integration
  - `whatsapp_bot.py` - Funktionalität für WhatsApp-Bot-Integration

- `bot_service.py` - Service für die Bot-Funktionalität (Telegram, WhatsApp) 