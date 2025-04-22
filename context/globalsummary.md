# CV2Profile: Globale Projektübersicht

## Projekteinführung

Das CV2Profile-Projekt ist ein KI-gestützter CV-Parser, der Lebensläufe analysiert und in standardisierte Profile konvertiert. Das System nutzt die OpenAI-API, um relevante Informationen aus verschiedenen Dokumenttypen (PDF, DOCX, JPG, PNG) zu extrahieren und daraus professionell gestaltete PDF-Profile zu generieren.

Diese globale Zusammenfassung bietet einen umfassenden Überblick über das Projekt, seine Funktionen, technische Architektur, Entwicklungsgeschichte und Zukunftsperspektiven. Sie basiert auf allen Kontextdokumenten im `context`-Verzeichnis des Projekts.

## Hauptfunktionen

- **Dokumentverarbeitung**: Unterstützung verschiedener Dateiformate mit direkter Textextraktion und OCR-Fallback
- **KI-gestützte Analyse**: Strukturierung der Lebenslaufdaten mittels OpenAI-API
- **Profilgenerierung**: Erstellung professioneller PDF-Profile in verschiedenen Designvorlagen
- **Benutzerfreundliche UI**: Streamlit-basierte Oberfläche mit modernem Glasmorphismus-Design
- **Konfigurationsmanagement**: Sichere Speicherung von API-Keys und Benutzereinstellungen
- **Ansprechpartner-Verwaltung**: Dropdown-Menü für verschiedene Ansprechpartner
- **Anonymisierungsoption**: Möglichkeit zur Anonymisierung persönlicher Daten
- **Demo-Modus**: Funktionsdemonstration ohne API-Key-Anforderung

## Projektarchitektur

Das Projekt ist modular aufgebaut und folgt einer klaren Verzeichnisstruktur:

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
├── sources/                    # Ressourcen für die Anwendung
│
├── context/                    # Projekt-Dokumentation
│
├── archive/                    # Archivierte Codeversionen
│
├── main.py                     # Haupteinstiegspunkt
├── run.sh                      # Ausführungsskript
└── requirements.txt            # Abhängigkeiten
```

### Kernkomponenten

1. **DocumentProcessor**: Extrahiert Text aus verschiedenen Dokumentformaten
2. **AIExtractor**: Analysiert den extrahierten Text mit OpenAI und strukturiert die Daten
3. **ProfileGenerator**: Erstellt PDF-Profile mit ReportLab
4. **Config**: Verwaltet Benutzereinstellungen und API-Keys
5. **App**: Streamlit-basierte Hauptanwendung mit Benutzeroberfläche

## Entwicklungsgeschichte

Das Projekt hat eine kontinuierliche Entwicklung durchlaufen, die in mehreren Versionen und Iterationen dokumentiert ist:

### Summary 1: Grundlegende Funktionalität (v2)

- Implementierung der Kernfunktionalitäten (Dokument-Parsing, KI-Extraktion, Profilerstellung)
- Einführung der Anonymisierungsfunktion für persönliche Daten
- Verbesserung des Ansprechpartner-Systems mit festen Optionen
- Behebung von PDF-Vorschau-Problemen und Session-State-Fehlern

### Summary 2: UI-Verbesserungen und Fehlerbehandlung

- Optimierung der Benutzeroberfläche mit Glasmorphismus-Effekten
- Verbesserte Fehlerbehandlung bei der Textextraktion
- Implementierung eines einheitlichen Styling-Systems
- Hinzufügung von benutzerfreundlichen Fehlermeldungen

### Summary 3: Konfigurationsmanagement

- Implementierung der config.py für sicheres Speichern des API-Keys
- Benutzereinstellungen für Template-Vorlieben und Anonymisierung
- Persistenz der Einstellungen über Sessions hinweg
- Einführung von Umgebungsvariablen-Priorität für API-Keys

### Summary 4: Template-Verbesserungen

- Layout-Verbesserungen im PDF-Generator
- Optimierte Darstellung von Berufserfahrung und Ausbildung
- Verbesserte Kontaktinformationen und Ansprechpartner-Darstellung
- Einheitlichere Formatierung und Abstände im PDF-Layout

### Summary 5: Demo-Modus und CSS-Verbesserungen

- Implementierung eines vollständigen Demo-Modus mit Beispieldaten
- Toggle-Schalter in der Seitenleiste für einfachen Zugriff
- Umfassende CSS-Optimierungen für bessere Benutzerfreundlichkeit
- Verfeinerung der Glasmorphismus-Effekte für modernere Optik

### Summary 6: Restrukturierung und Bereinigung

- Entfernung veralteter App-Versionen und redundanter Dateien
- Aktualisierung der Dokumentation für historische Referenz
- Klare Referenzierung der aktuellen Codebase in src/ui/app.py
- Beseitigung von Redundanzen und optimierte Importpfade

### Summary 7: Profilvorlage-Layout-Optimierungen

- Verbesserte Logo-Positionierung und Überschriften-Gestaltung
- Optimierung der Ansprechpartner-Sektion
- Anpassung der zweispaltigen Layout-Struktur
- Zusätzliche Trennlinien für bessere visuelle Organisation

## Installations- und Nutzungsanleitung

### Installation

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

### Anwendung starten

```
./run.sh
```
oder
```
python main.py
```
oder
```
streamlit run src/ui/app.py
```

### Nutzungsworkflow

1. OpenAI API-Key in der Seitenleiste eingeben (oder Demo-Modus aktivieren)
2. Lebenslauf hochladen (PDF, DOCX, JPG oder PNG)
3. Extrahierte Daten überprüfen und bei Bedarf bearbeiten
4. Template auswählen (Klassisch, Modern, Professionell, Minimalistisch)
5. Optional: Anonymisieren der persönlichen Daten aktivieren
6. Profil generieren und herunterladen

## Import-Pfadanweisungen

Bei der Entwicklung ist zu beachten, dass das Projekt strukturierte Import-Pfade verwendet:

```python
from src.core.document_processor import DocumentProcessor
from src.core.ai_extractor import AIExtractor
from src.core.combined_processor import CombinedProcessor
from src.templates.template_generator import ProfileGenerator
import src.utils.config as config
```

Die alten Dateien im Archiv verwendeten absolute Imports und sind nicht mehr kompatibel.

## Bekannte Probleme und Einschränkungen

- PDF-Vorschau: In manchen Browsern kann die Vorschau blockiert werden
- Session-State-Fehler: Bei Streamlit-Neustarts kann es zu Initialisierungsfehlern kommen
- Sprachunterstützung: Aktuell ist nur die deutsche Sprache vollständig unterstützt
- Browser-Kompatibilität: Einige CSS-Definitionen benötigen !important-Flags

## Zukünftige Entwicklungsmöglichkeiten

1. **Mehrsprachige Unterstützung**: Erweiterung um weitere Sprachen
2. **Verbesserung der KI-Extraktion**: Feintuning der Modelle für bessere Ergebnisse
3. **Integration mit ATS**: Anbindung an Applicant Tracking Systems
4. **Anpassbare Farbschemata**: Ermöglichung verschiedener Farbvarianten für die Profilvorlage
5. **Zusätzliche Vorlagenoptionen**: Erstellung weiterer Vorlagendesigns
6. **Mobile Optimierung**: Verbesserte Darstellung auf mobilen Geräten
7. **Automatisierte Tests**: Implementierung von Testsuites für robustere Entwicklung

## Datenschutz und Sicherheit

- Lokale Verarbeitung der Dokumente
- Temporäre Dateien werden nach der Verarbeitung gelöscht
- OpenAI API-Keys werden sicher im Benutzerverzeichnis gespeichert
- Nur für die KI-Analyse werden Daten an OpenAI übertragen
- Demo-Modus ermöglicht Testen ohne API-Nutzung

## Branches und Versionshinweise

- **main**: Stabile Hauptversion
- **v2**: Erweiterte Funktionalität mit Konfigurationsmanagement
- **v3**: Layout-Optimierungen der Profilvorlage

## Für Entwickler

Bei der Weiterentwicklung des Projekts sollten folgende Aspekte berücksichtigt werden:

1. **Modulare Struktur beibehalten**: Neue Funktionen sollten der bestehenden Architektur folgen
2. **Importpfade beachten**: Strukturierte Imports mit src.-Präfix verwenden
3. **Fehlerbehandlung implementieren**: Besonders bei der API-Nutzung und Dateiverarbeitung
4. **Dokumentation aktualisieren**: Bei größeren Änderungen neue Summary-Dateien erstellen
5. **CSS-Konsistenz bewahren**: Glasmorphismus-Effekte beibehalten und erweitern
6. **Templates erweitern**: Bei neuen Templates die Konsistenz mit bestehenden beachten

Dieses Projekt bietet eine solide Grundlage für die automatisierte Verarbeitung von Lebensläufen und kann durch die modulare Struktur leicht erweitert werden, um zusätzliche Funktionen und Verbesserungen zu implementieren. 