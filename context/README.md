# CV2Profile

Ein KI-gestützter CV-Parser, der Lebensläufe analysiert und in standardisierte Profile konvertiert.

## Projektbeschreibung

CV2Profile ist ein leistungsstarker CV-Parser, der mit Hilfe von KI-Technologie (OpenAI) Lebensläufe automatisch analysiert und in standardisierte Profile konvertiert. Die Anwendung unterstützt verschiedene Dokumentformate (PDF, DOCX, JPG, PNG), extrahiert Text, identifiziert relevante Informationen und erstellt professionelle PDF-Profile.

## Projektstruktur

Die Anwendung ist wie folgt organisiert:

```
CV2Profile/
│
├── src/                        # Quellcode-Verzeichnis
│   ├── core/                   # Kernfunktionen
│   │   ├── document_processor.py  # Dokumentenverarbeitung
│   │   ├── ai_extractor.py        # KI-basierte Datenextraktion
│   │   └── combined_processor.py  # Kombinierte Verarbeitung
│   │
│   ├── ui/                     # Benutzeroberfläche
│   │   └── app.py              # Streamlit-basierte Hauptanwendung
│   │
│   ├── utils/                  # Hilfsfunktionen
│   │   └── config.py           # Konfigurationsverwaltung
│   │
│   └── templates/              # Template-Generierung
│       └── template_generator.py  # PDF-Profilgenerierung
│
├── sources/                    # Ressourcen
│   ├── Galdoralogo.png         # Logo für PDF-Dokumente
│   ├── Profilvorlage Seite 1.png # Vorlagendesign Seite 1
│   └── Profilvorlage Seite 2.png # Vorlagendesign Seite 2
│
├── context/                    # Projekt-Dokumentation
│   ├── Context.md              # Hauptprojektkontext
│   ├── summary*.md             # Zusammenfassungen der Projektentwicklung
│   └── README.md               # Diese Datei
│
├── archive/                    # Archivierte Codeversionen
│   ├── README.md               # Hinweise zu archivierten Dateien
│   ├── app_versions/          # Alte Versionen der Hauptapp und UI-Fixes
│   │   ├── README.md           # Warnhinweis zu alten App-Versionen
│   │   ├── app_original.py    # Ursprüngliche App-Version
│   │   ├── app_new.py         # Neuere App-Version
│   │   ├── app.py.bak         # Backup der App
│   │   ├── app_ui_fixed.py    # Version mit UI-Fixes
│   │   ├── app_ui_fixed_new.py # Neuere Version mit UI-Fixes
│   │   ├── fix_app_ui.py      # UI-Fix-Skript
│   │   └── fix_app_ui_improved.py # Verbessertes UI-Fix-Skript
│   │
│   └── old_files/             # Alte Dateien aus dem Hauptverzeichnis
│       ├── README.md           # Warnhinweis zu alten Moduldateien
│       ├── ai_extractor.py    # Alte KI-Extraktionslogik
│       ├── combined_processor.py # Alte kombinierte Prozessorversion
│       ├── config.py          # Alte Konfigurationsversion
│       ├── document_processor.py # Alte Dokumentenprozessorversion
│       ├── template_generator.py # Alte Template-Generator-Version
│       └── app.py             # Alte Hauptanwendung
│
├── main.py                     # Haupteinstiegspunkt
├── run.sh                      # Ausführungsskript
├── archive_notice.py           # Warnhinweis zu archivierten Dateien
└── requirements.txt            # Abhängigkeiten
```

## Installation

1. Repository klonen
2. Virtuelle Umgebung erstellen und aktivieren:
   ```
   python -m venv venv
   source venv/bin/activate  # Unter Windows: venv\Scripts\activate
   ```
3. Abhängigkeiten installieren:
   ```
   pip install -r requirements.txt
   ```
4. OpenAI API-Key einrichten:
   - Setze die Umgebungsvariable `OPENAI_API_KEY`
   - Oder speichere den Key über die Anwendung

## Anwendung starten

Mit dem run.sh-Skript:
```
./run.sh
```

Oder mit Python:
```
python main.py
```

Oder direkt mit Streamlit:
```
streamlit run src/ui/app.py
```

## Kernfunktionalitäten

- **Dokumentenverarbeitung und Textextraktion** aus verschiedenen Dateiformaten
- **KI-gestützte Analyse** mittels OpenAI-API
- **Profilgenerierung** in verschiedenen Templates (Klassisch, Modern, Professionell, Minimalistisch)
- **Konfigurationsmanagement** mit sicherer API-Key-Speicherung
- **Ansprechpartner-Verwaltung** über Dropdown-Menü
- **Moderne UI** mit Glasmorphismus-Design

## Hinweise zur Projektstruktur

Die Anwendung wurde aufgeräumt und neu strukturiert. Alle Dateien aus dem Hauptverzeichnis wurden in die entsprechenden Unterverzeichnisse verschoben oder archiviert. Ältere Versionen wurden im `archive`-Verzeichnis gesammelt, um die Projekthistorie zu bewahren, aber die Struktur übersichtlicher zu gestalten.

Die aktuelle Version der Anwendung basiert vollständig auf den Dateien im `src`-Verzeichnis und nutzt den standardisierten Import-Pfad des Pakets.

## Import-Pfade

Bei der Entwicklung ist zu beachten, dass die Anwendung jetzt strukturierte Import-Pfade verwendet:

```python
from src.core.document_processor import DocumentProcessor
from src.core.ai_extractor import AIExtractor
from src.core.combined_processor import CombinedProcessor
from src.templates.template_generator import ProfileGenerator
import src.utils.config as config
```

Die alten Dateien im Archiv verwendeten absolute Imports und sind nicht mehr kompatibel:

```python
from document_processor import DocumentProcessor
from ai_extractor import AIExtractor
from combined_processor import CombinedProcessor
from template_generator import ProfileGenerator
import config
```

Um versehentliche Verwendung der alten Dateien zu verhindern, wurden Warnhinweise in den Archivverzeichnissen platziert.
