# Parser v5 - Lebenslauf-Konvertierungs- und Profil-Generator

## Überblick

Diese Anwendung ist ein KI-gestützter Lebenslauf-Parser, der Dokumente analysiert und in strukturierte Daten konvertiert. Mit dem integrierten Profil-Generator können aus diesen Daten professionelle PDF- und DOCX-Profile erstellt werden.

## Hauptfunktionen

- **Dokumentenanalyse**: Unterstützt PDF, DOCX, JPG und PNG
- **KI-Extraktion**: Verwendet OpenAI API für präzise Datenextraktion
- **Profilgenerierung**: Erstellt professionelle Dokumente aus den extrahierten Daten
- **Vorlagenauswahl**: Verschiedene Vorlagen (Klassisch, Modern, Professionell, Minimalistisch)
- **Drag & Drop-Bearbeitung**: Einfache Anpassung der Reihenfolge von Berufserfahrungen
- **Deployment-kompatibel**: Funktioniert sowohl lokal als auch auf Streamlit Cloud
- **API-Key Verwaltung**: Einfaches Speichern des OpenAI API-Keys im Projektverzeichnis

## Neu in v5

- **Verbesserte API-Key Verwaltung**: Speichern des API-Keys im Projektverzeichnis für einfachere Nutzung
- **Robuste Bilddarstellung**: Verbesserte Kompatibilität mit Streamlit-Deployments
- **Zuverlässige PDF-Vorschau**: Alternative Anzeigemethoden für alle Browser
- **Fehlertolerante Bildverarbeitung**: Erweiterte Fallback-Mechanismen für fehlende Bilder
- **Optimierte DOCX-Generierung**: Verbesserte Integration von Logos in Word-Dokumente
- **Bessere Fehlermeldungen**: Benutzerfreundliche Hinweise bei Problemen
- **Automatische Cloud-Erkennung**: Anpassung an lokale oder Cloud-Umgebungen
- **Flexibles Deployment**: Neue Deployment-Skripte für konsistente Anwendungseinstiegspunkte

## API-Key Konfiguration

Der OpenAI API-Key kann auf mehrere Arten konfiguriert werden (in Prioritätsreihenfolge):

1. **Umgebungsvariable**: `OPENAI_API_KEY` in der Systemumgebung
2. **Projektspezifische Datei**: `api_key.json` im Hauptverzeichnis (für lokale Entwicklung empfohlen)
3. **Streamlit Secrets**: Über die Streamlit Cloud Konfiguration (für Deployment empfohlen)
4. **Benutzereinstellungen**: Gespeichert in `~/.cv2profile/settings.json`

Um den API-Key im Projekt zu speichern:
1. Gehen Sie zu "⚙️ Einstellungen"
2. Öffnen Sie "API-Key Verwaltung"
3. Geben Sie Ihren API-Key ein und klicken Sie auf "Im Projekt speichern"

Die Datei `api_key.json` ist in `.gitignore` eingetragen und wird nicht ins Repository übertragen.

## Technische Details

Die Anwendung besteht aus mehreren Modulen:

1. **document_processor.py**: Textextraktion aus verschiedenen Dokumentformaten
2. **ai_extractor.py**: KI-gestützte Datenanalyse mit OpenAI
3. **template_generator.py**: Erstellung von PDF- und DOCX-Profilen
4. **app.py**: Benutzerfreundliche Streamlit-Oberfläche
5. **config.py**: Konfigurationsmanagement für Benutzereinstellungen
6. **image_utils.py**: HTTPS-kompatible Bildverwaltung

## Start der Anwendung

Standardmäßig wird die Anwendung mit dem Konverter als Einstiegspunkt gestartet:

```bash
# Umgebung aktivieren (falls vorhanden)
source venv/bin/activate  # Linux/macOS
# ODER
venv\Scripts\activate     # Windows

# Anwendung starten mit Standard-Einstiegspunkt (Konverter)
./run.sh
```

Alternativ kann die Anwendung auch mit dem ursprünglichen `app.py` Einstiegspunkt gestartet werden:

```bash
# Umgebung aktivieren (falls vorhanden)
source venv/bin/activate  # Linux/macOS
# ODER
venv\Scripts\activate     # Windows

# Anwendung mit app.py als Einstiegspunkt starten
export CV2PROFILE_ENTRY_POINT="app"
./run.sh
```

Weitere Informationen zur Deployment-Strategie finden Sie in der [Deployment-Anleitung](docs/deployment_guide.md).

## Systemanforderungen

- Python 3.7+
- OpenAI API-Key
- Für OCR-Funktionalität: Tesseract OCR

## Projektbeschreibung

CV2Profile ist ein leistungsstarker CV-Parser, der mit Hilfe von KI-Technologie (OpenAI) Lebensläufe automatisch analysiert und in standardisierte Profile konvertiert. Die Anwendung unterstützt verschiedene Dokumentformate (PDF, DOCX, JPG, PNG), extrahiert Text, identifiziert relevante Informationen und erstellt professionelle PDF-Profile.

## Kernfunktionalitäten

- **Dokumentenverarbeitung und Textextraktion** aus verschiedenen Dateiformaten
- **KI-gestützte Analyse** mittels OpenAI-API
- **Profilgenerierung** in verschiedenen Templates (Klassisch, Modern, Professionell, Minimalistisch)
- **Konfigurationsmanagement** mit sicherer API-Key-Speicherung
- **Ansprechpartner-Verwaltung** über Dropdown-Menü
- **Moderne UI** mit Glasmorphismus-Design

## Projektstruktur

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
│   │   ├── app.py              # Streamlit-basierte Hauptanwendung
│   │   └── pages/              # Streamlit-Seiten
│   │       └── 01_Konverter.py # Konverter-Hauptfunktionalität
│   │
│   ├── utils/                  # Hilfsfunktionen
│   │   ├── config.py           # Konfigurationsverwaltung
│   │   └── image_utils.py      # Bild-Utilities für HTTPS-Kompatibilität
│   │
│   └── templates/              # Template-Generierung
│       └── template_generator.py  # PDF-Profilgenerierung
│
├── sources/                    # Ressourcen
│   ├── Galdoralogo.png         # Logo für PDF-Dokumente
│   └── weitere Ressourcen      # Weitere Bilder und Assets
│
├── static/                     # Statische Dateien für HTTPS-Server
│   └── images/                 # Bilder für HTTPS-Kompatibilität
│
├── api_key.json                # Lokale API-Key-Speicherung (in .gitignore)
│
├── .github/workflows/          # CI/CD-Konfiguration
│   └── streamlit_deploy.yml    # GitHub Actions Workflow für Deployment
│
├── docs/                       # Dokumentation
│   └── deployment_guide.md     # Anleitung zur Deployment-Strategie
│
├── pre_deploy.sh               # Skript zur Deployment-Vorbereitung
├── post_deploy.sh              # Skript zur Wiederherstellung nach Deployment
│
└── .streamlit/                 # Streamlit-Konfiguration
    └── config.toml             # Streamlit-Einstellungen
```

## Online-Version

Die Anwendung ist online unter [cv2profile.streamlit.app](https://cv2profile.streamlit.app/) verfügbar.

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz - siehe die [LICENSE](LICENSE)-Datei für Details. 