# Streamlit Pages

Dieser Ordner enthält zusätzliche Seiten für die CV2Profile Anwendung, die über die Streamlit Multipage-Funktionalität zugänglich sind.

## Organisationsstruktur

Die Seiten werden in der Seitenleiste nach ihrem Dateinamen geordnet angezeigt. Das Format ist:

`XX_Pagename.py` wobei XX eine Zahl ist, die die Reihenfolge bestimmt.

## Verfügbare Seiten

- **01_Settings.py**: Einstellungsseite für die Anwendung (⚙️)
  - Allgemeine Einstellungen
  - API-Einstellungen
  - System-Einstellungen
  - Erweiterte Einstellungen

## Hinweise zur Entwicklung

- Alle Seiten sollten das gleiche CSS und Design wie die Hauptanwendung verwenden
- Seiten können auf das `src.utils.config`-Modul zugreifen, um Einstellungen zu lesen/schreiben
- Jede Seite muss unabhängig von der Hauptanwendung funktionieren

## Seitenkonfiguration

Die Seitennamen und Icons können in `.streamlit/config.toml` konfiguriert werden:

```toml
[pages]
01_Settings = "⚙️ Einstellungen"
``` 