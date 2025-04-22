# CV2Profile

Ein KI-gestützter CV-Parser, der Lebensläufe analysiert und in standardisierte Profile konvertiert.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://cv2profile.streamlit.app/)

## Projektbeschreibung

CV2Profile ist ein leistungsstarker CV-Parser, der mit Hilfe von KI-Technologie (OpenAI) Lebensläufe automatisch analysiert und in standardisierte Profile konvertiert. Die Anwendung unterstützt verschiedene Dokumentformate (PDF, DOCX, JPG, PNG), extrahiert Text, identifiziert relevante Informationen und erstellt professionelle PDF-Profile.

## Kernfunktionalitäten

- **Dokumentenverarbeitung und Textextraktion** aus verschiedenen Dateiformaten
- **KI-gestützte Analyse** mittels OpenAI-API
- **Profilgenerierung** in verschiedenen Templates (Klassisch, Modern, Professionell, Minimalistisch)
- **Konfigurationsmanagement** mit sicherer API-Key-Speicherung
- **Ansprechpartner-Verwaltung** über Dropdown-Menü
- **Moderne UI** mit Glasmorphismus-Design

## Anwendung lokal starten

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

5. Streamlit starten:
   ```
   streamlit run src/ui/app.py
   ```

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
│   └── weitere Ressourcen      # Weitere Bilder und Assets
│
└── .streamlit/                 # Streamlit-Konfiguration
    └── config.toml             # Streamlit-Einstellungen
```

## Online-Version

Die Anwendung ist online unter [cv2profile.streamlit.app](https://cv2profile.streamlit.app/) verfügbar.

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz - siehe die [LICENSE](LICENSE)-Datei für Details. 