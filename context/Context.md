# CV Parser und Profilgenerator

## Übersicht

Diese Anwendung ist ein leistungsstarker CV-Parser, der Lebensläufe automatisch analysiert und in ein standardisiertes Format umwandelt. Die Software nutzt KI-Technologie (OpenAI), um relevante Informationen aus verschiedenen Dokumenttypen zu extrahieren und in strukturierte Daten zu konvertieren.

## Hauptfunktionen

- **Dokumentverarbeitung**: Unterstützung verschiedener Formate wie PDF, DOCX, JPG und PNG
- **Text-Extraktion**: Intelligente Extraktion von Text aus allen unterstützten Dokumentformaten
- **KI-gestützte Analyse**: Nutzung von OpenAI-Modellen zur Identifizierung von Schlüsselinformationen
- **Strukturierte Profilerstellung**: Generierung standardisierter Profile im PDF-Format
- **Benutzerfreundliche Oberfläche**: Einfache Handhabung durch Streamlit-Frontend
- **Benutzerverwaltete Einstellungen**: Speichern von Voreinstellungen wie API-Keys und bevorzugten Templates
- **HTTPS-Kompatibilität**: Bilder werden auf HTTP- und HTTPS-Servern korrekt angezeigt

## Detaillierte Projektstruktur

```
CV2Profile/
│
├── src/                           # Quellcode-Verzeichnis
│   ├── core/                      # Kernfunktionalität für Dokumentenverarbeitung
│   │   ├── __init__.py           # Package-Initialisierung
│   │   ├── document_processor.py  # Dokumentenverarbeitung (PDF, DOCX, Bilder)
│   │   ├── ai_extractor.py       # KI-gestützte Informationsextraktion (OpenAI)
│   │   └── combined_processor.py # Kombinierte Verarbeitungslogik
│   │
│   ├── ui/                        # Benutzeroberflächen-Module
│   │   ├── __init__.py           # Package-Initialisierung
│   │   ├── app.py                # Hauptanwendung (Streamlit-Oberfläche)
│   │   ├── Home.py               # Homepage der Anwendung
│   │   └── pages/                # Zusätzliche Seiten
│   │       ├── README.md         # Dokumentation zu Seiten
│   │       └── 01_⚙️_Einstellungen.py  # Einstellungen-Seite
│   │
│   ├── utils/                     # Hilfsfunktionen
│   │   ├── __init__.py           # Package-Initialisierung
│   │   ├── config.py             # Konfigurationsmanagement (API-Keys, etc.)
│   │   └── image_utils.py        # Bild-Utilities für HTTPS-Kompatibilität
│   │
│   ├── templates/                 # Template-Generierung
│   │   ├── __init__.py           # Package-Initialisierung
│   │   └── template_generator.py # PDF-Profilgenerierung
│   │
│   └── __init__.py               # Hauptpackage-Initialisierung
│
├── sources/                       # Ressourcen und Assets
│   ├── galdoralogo.png           # Firmenlogo für PDF-Dokumente
│   ├── cv2profile-loho.png       # Anwendungslogo
│   ├── Profilvorlage Seite 1.png # Designvorlagen
│   └── Profilvorlage Seite 2.png # Designvorlagen
│
├── static/                        # Statische Dateien für HTTPS-Server
│   └── images/                    # Bilder für HTTPS-Kompatibilität
│
├── context/                       # Projektdokumentation und -kontext
│   ├── Context.md                # Hauptdokumentation (diese Datei)
│   ├── README.md                 # Zusätzliche Dokumentation
│   ├── progress.md               # Fortschrittsverfolgung und Aufgabenplanung
│   ├── activecontext.md          # Aktiver Arbeitskontext
│   ├── globalsummary.md          # Globale Zusammenfassung
│   └── summary*.md               # Versionsbasierte Zusammenfassungen
│
├── .streamlit/                    # Streamlit-Konfiguration
│   ├── config.toml               # UI-Einstellungen
│   ├── secrets.toml              # Anwendungsgeheimnisse (API-Keys etc.)
│   └── secrets_template.toml     # Vorlage für secrets.toml
│
├── venv/ und .venv/              # Virtuelle Umgebungen
│
└── Hauptdateien
    ├── main.py                   # Einstiegspunkt der Anwendung
    ├── run.sh                    # Skript zum Starten der Anwendung
    ├── requirements.txt          # Projektabhängigkeiten
    ├── packages.txt              # Systemabhängigkeiten
    ├── README.md                 # Projektübersicht
    ├── archive_notice.py         # Archivierungshinweis
    └── LICENSE                   # Lizenzinformationen
```

## Dateipfade für häufige Änderungen

### Benutzeroberfläche anpassen
- **Hauptanwendung**: `src/ui/app.py` - Enthält die gesamte Streamlit-Hauptoberfläche
- **Homepage**: `src/ui/Home.py` - Startseite der Anwendung
- **Einstellungen**: `src/ui/pages/01_⚙️_Einstellungen.py` - Einstellungsseite

### KI-Funktionalität anpassen
- **Extraktor**: `src/core/ai_extractor.py` - OpenAI-Integration und Datenextraktion
- **Prompts ändern**: `src/core/ai_extractor.py` - Enthält die Prompt-Templates für OpenAI

### PDF-Vorlagen anpassen
- **Template-Generator**: `src/templates/template_generator.py` - PDF-Generierung und Design
- **Verfügbare Templates**: Classic (Standard), Modern (zweispaltig, weinrot/weiß), Professional, Minimalist
- **Logos und Bilder**: `sources/` - Bilder und Logos für die PDF-Vorlagen

### Bild-Verwaltung anpassen
- **Bild-Utilities**: `src/utils/image_utils.py` - Funktionen für die HTTPS-kompatible Bildverwaltung
- **Statische Bilder**: `static/images/` - Speicherort für HTTPS-kompatible Bilddateien

### Konfiguration anpassen
- **Konfigurationsmanagement**: `src/utils/config.py` - Verwaltet Benutzereinstellungen
- **Streamlit-Konfiguration**: `.streamlit/config.toml` - Ändert Streamlit-Verhalten
- **Geheime Schlüssel**: `.streamlit/secrets.toml` - Für API-Keys und Geheimnisse

### Dokument-Verarbeitung anpassen
- **Dokumentenprozessor**: `src/core/document_processor.py` - Text aus verschiedenen Formaten extrahieren
- **Kombinierter Prozessor**: `src/core/combined_processor.py` - Hauptworkflow der Anwendung

## Technische Komponenten

Die Anwendung besteht aus mehreren Modulen:

1. **document_processor.py**: Verarbeitet Dokumente und extrahiert Text
   - Unterstützt PDF-Dokumente mit direkter Textextraktion und OCR-Fallback
   - Verarbeitet Bilddateien mittels OCR (Optical Character Recognition)
   - Extrahiert Text aus Word-Dokumenten (DOCX)

2. **ai_extractor.py**: Analysiert den extrahierten Text mittels KI
   - Verwendet OpenAI-API zur Strukturierung der Daten
   - Extrahiert persönliche Daten, Berufserfahrung, Ausbildung und Weiterbildungen
   - Formatiert die Daten in ein standardisiertes JSON-Format

3. **template_generator.py**: Erstellt ansprechende PDF-Profile
   - Generiert professionell gestaltete PDF-Dokumente
   - Verwendet ReportLab für die PDF-Erstellung
   - Erstellt ein einheitliches Layout für alle Profile

4. **app.py**: Hauptanwendung mit Benutzeroberfläche
   - Streamlit-basierte Oberfläche für einfache Bedienung
   - Upload-Funktion für Dokumente
   - Bearbeitungsmöglichkeiten für extrahierte Daten
   - Download-Option für generierte Profile

5. **config.py**: Verwaltung von Benutzereinstellungen
   - Speichert den OpenAI API-Key sicher im Benutzerverzeichnis
   - Verwaltet benutzerdefinierte Einstellungen wie Template-Voreinstellungen
   - Ermöglicht das Anpassen von Optionen wie Textanzeige und Anonymisierung

6. **image_utils.py** (NEU): Verwaltung von Bildern für verschiedene Umgebungen
   - Stellt HTTPS-Kompatibilität für Bilder sicher
   - Kopiert Bilder automatisch in das static-Verzeichnis
   - Ermöglicht konsistente Bildanzeige auf allen Plattformen

## Anwendungsfälle

- **Personalvermittlung**: Schnelle Verarbeitung und Standardisierung von Bewerber-CVs
- **HR-Abteilungen**: Effiziente Verwaltung von Bewerbungsunterlagen
- **Recruiting**: Vereinfachung des Bewerbungsprozesses
- **Talent-Management**: Erstellung einheitlicher Mitarbeiterprofile

## Voraussetzungen

- Python 3.7 oder höher
- Installierte Abhängigkeiten (siehe requirements.txt)
- OpenAI API-Schlüssel für die KI-Funktionalität
- Für die OCR-Funktionalität: Tesseract OCR installiert

## Installation und Ausführung

1. Repository klonen oder Dateien herunterladen
2. Virtuelle Umgebung erstellen und aktivieren:
   ```
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```
3. Abhängigkeiten installieren:
   ```
   pip install -r requirements.txt
   ```
4. Anwendung starten:
   ```
   streamlit run app.py
   ```
5. Im Browser öffnen (standardmäßig unter http://localhost:8501)

## Beispielhafte Nutzung

1. OpenAI API-Schlüssel in der Seitenleiste eingeben (kann für spätere Verwendung gespeichert werden)
2. Lebenslauf hochladen (PDF, DOCX, JPG oder PNG)
3. Extrahierte Daten überprüfen und bei Bedarf bearbeiten
4. Template auswählen (kann als Standard gespeichert werden)
5. Optional: Anonymisieren der persönlichen Daten aktivieren
6. Profil generieren und herunterladen

## Aktuelle Version (v3)

Die aktuelle Version (v3) enthält folgende Verbesserungen:

- **HTTPS-Kompatibilität**: Bilder werden sowohl lokal als auch auf HTTPS-Servern korrekt angezeigt
- **Automatische Bildverwaltung**: Bilder werden automatisch in das static-Verzeichnis kopiert
- **Verbesserte Profilvorlagen**: 
  - Optimiertes Layout für bessere Lesbarkeit
  - Neues modernes Template im zweispaltigen Design (weinrot/weiß)
  - Verbesserte visuelle Darstellung von Fähigkeiten und Sprachen
- **API-Key-Verwaltung**: Der OpenAI API-Key wird sicher in `~/.cv2profile/settings.json` gespeichert
- **Benutzerverwaltete Einstellungen**: 
  - Auswahl des Standard-Templates (Klassisch, Modern, Professionell, Minimalistisch)
  - Option zur Anonymisierung der Daten
  - Option zur Anzeige des extrahierten Textes
- **Verbesserte Benutzeroberfläche**:
  - Hervorhebung des ausgewählten Standard-Templates
  - Speichern von bevorzugten Templates für zukünftige Verwendung
  - Eindeutige Schlüssel für Checkbox-Widgets zur Vermeidung von Konflikten

## Bekannte Probleme in v3

- Fehler bei der PDF-Vorschau: In Schritt 3 kann es zu einem Fehler kommen, wenn `st.session_state.preview_pdf` den Wert `None` hat
- Der Fehler tritt auf in der Funktion `display_pdf()` in Zeile 48 der app.py
- Fehlermeldung: `TypeError: expected str, bytes or os.PathLike object, not NoneType`
- Eine Überprüfung auf `None` sollte implementiert werden, bevor versucht wird, die Datei zu öffnen

## Aktuelle Grenzen und zukünftige Erweiterungen

- Aktuell nur deutsche Sprache vollständig unterstützt
- Erweiterung um mehrsprachige Unterstützung geplant
- Verbesserung der KI-Extraktion durch Feintuning geplant
- Integration mit ATS (Applicant Tracking Systems) möglich
- Behebung des PDF-Vorschau-Fehlers für die nächste Version geplant

## Datenschutz und Sicherheit

- Lokale Verarbeitung der Dokumente
- Temporäre Dateien werden nach der Verarbeitung gelöscht
- Nur für die KI-Analyse werden Daten an OpenAI übertragen (gemäß deren Datenschutzrichtlinien)
- Keine dauerhafte Speicherung von Bewerberdaten in der Anwendung
- OpenAI API-Keys werden sicher im Benutzerverzeichnis gespeichert 