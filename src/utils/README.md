# utils - Hilfsfunktionen

Dieses Verzeichnis enthält verschiedene Hilfsfunktionen und Dienstprogramme für den CV2Profile-Parser.

## Enthaltene Dateien

- **config.py**: Verwaltung von Benutzereinstellungen
  - Speichert den OpenAI API-Key sicher im Benutzerverzeichnis oder in projektspezifischen Dateien
  - Verwaltet benutzerdefinierte Einstellungen wie Template-Voreinstellungen
  - Ermöglicht das Anpassen von Optionen wie Textanzeige und Anonymisierung
  - Implementiert eine priorisierte Ladereihenffolge für API-Keys aus verschiedenen Quellen

- **image_utils.py**: Verwaltung von Bildern für verschiedene Umgebungen
  - Stellt HTTPS-Kompatibilität für Bilder sicher
  - Kopiert Bilder automatisch in das static-Verzeichnis
  - Ermöglicht konsistente Bildanzeige auf allen Plattformen (lokal und im Web)
  - Bietet Hilfsfunktionen zum Finden und Verarbeiten von Bildern

- **telegram_bot.py**: Funktionalität für Telegram-Bot-Integration
  - Implementiert einen Telegram-Bot für die Interaktion mit dem CV2Profile-Parser
  - Ermöglicht das Hochladen und Verarbeiten von Dokumenten über Telegram
  - Bietet Benutzerinteraktion und Steuerung über Telegram-Nachrichten

- **whatsapp_bot.py**: Funktionalität für WhatsApp-Bot-Integration
  - Implementiert einen WhatsApp-Bot für die Interaktion mit dem CV2Profile-Parser
  - Ermöglicht das Hochladen und Verarbeiten von Dokumenten über WhatsApp
  - Bietet Benutzerinteraktion und Steuerung über WhatsApp-Nachrichten

## Verwendung

Die Hilfsfunktionen werden von verschiedenen Teilen der Anwendung verwendet:

- `config.py` wird für die Verwaltung von Benutzereinstellungen und API-Keys verwendet
- `image_utils.py` wird für die Bildverwaltung in der gesamten Anwendung verwendet, insbesondere für die HTTPS-Kompatibilität
- `telegram_bot.py` und `whatsapp_bot.py` werden für die Bot-Integration verwendet, die über `bot_service.py` koordiniert wird 