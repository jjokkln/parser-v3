# ui - Benutzeroberfläche

Dieses Verzeichnis enthält die Komponenten für die Benutzeroberfläche des CV2Profile-Parsers, basierend auf dem Streamlit-Framework.

## Enthaltene Dateien und Verzeichnisse

- **app.py**: Hauptanwendung mit Benutzeroberfläche
  - Streamlit-basierte Oberfläche für einfache Bedienung
  - Upload-Funktion für Dokumente
  - Bearbeitungsmöglichkeiten für extrahierte Daten
  - Download-Option für generierte Profile
  - Enthält den Hauptteil der UI-Logik

- **Home.py**: Homepage der Anwendung
  - Dient als Einstiegspunkt für die Anwendung
  - Enthält grundlegende Informationen und Navigationsoptionen

- **pages/**: Verzeichnis für zusätzliche Seiten
  - **01_Konverter.py**: Hauptkonverterseite für die Dokumentenverarbeitung
  - **02_⚙️_Einstellungen.py**: Einstellungsseite für Benutzereinstellungen
  - **README.md**: Dokumentation zu den Seiten

- **app.py.bak** und **app.py.backup**: Backup-Dateien der Hauptanwendung
  - Dienen als Sicherungskopien früherer Versionen

## Funktionalität

Die UI-Komponenten bieten:

- Eine intuitive Benutzeroberfläche für den gesamten Workflow der Anwendung
- Benutzerfreundliche Upload- und Download-Funktionen
- Möglichkeiten zur Dateneditierung und -anpassung
- Einstellungen für die Anpassung der Anwendungsfunktionalität
- Visualisierung der extrahierten Daten
- Vorschau für die generierten Profile

## Verwendung

Die UI-Komponenten sind der Haupteinstiegspunkt für Benutzer und werden beim Start der Anwendung über die Hauptdatei (`main.py`) geladen. Die Hauptlogik für die Benutzeroberfläche ist entweder in `main.py` direkt implementiert oder in `src/ui/app.py` bzw. den entsprechenden Seiten in `pages/`. 