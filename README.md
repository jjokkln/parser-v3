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
│   └── galdoralogo.png         # Logo für PDF-Dokumente
│
├── context/                    # Projekt-Dokumentation
│   └── summary*.md             # Zusammenfassungen der Projektentwicklung
│
├── archive/                    # Archivierte Codeversionen
│   ├── app_versions/          # Alte Versionen der Hauptapp
│   └── ui_fixes/              # UI-Verbesserungen
│
├── main.py                     # Haupteinstiegspunkt
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
