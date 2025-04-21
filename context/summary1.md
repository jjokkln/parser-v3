
# Zusammenfassung des CV2Profile Konverter-Projekts

## Projektübersicht

Das CV2Profile-Projekt ist ein leistungsstarker CV-Parser, der mit Hilfe von KI-Technologie (OpenAI) Lebensläufe automatisch analysiert und in standardisierte Profile konvertiert. Die Anwendung unterstützt verschiedene Dokumentformate (PDF, DOCX, JPG, PNG), extrahiert Text, identifiziert relevante Informationen und erstellt professionelle PDF-Profile.

## Kernfunktionalitäten

- **Dokumentenverarbeitung und Textextraktion** aus verschiedenen Dateiformaten
- **KI-gestützte Analyse** mittels OpenAI-API
- **Profilgenerierung** in verschiedenen Templates (Klassisch, Modern, Professionell, Minimalistisch)
- **Konfigurationsmanagement** mit sicherer API-Key-Speicherung
- **Anonymisierungsfunktion** für persönliche Daten
- **Ansprechpartner-Verwaltung** über Dropdown-Menü

## Projektstruktur

Das Projekt besteht aus folgenden Hauptkomponenten:

1. **document_processor.py**: Verarbeitet Dokumente und extrahiert Text mit direkter Extraktion oder OCR
2. **ai_extractor.py**: Analysiert den extrahierten Text mittels OpenAI und strukturiert die Daten
3. **template_generator.py**: Erstellt PDF-Profile mit ReportLab
4. **config.py**: Verwaltet Benutzereinstellungen und speichert sie in `~/.cv2profile/settings.json`
5. **app.py**: Streamlit-basierte Hauptanwendung mit Benutzeroberfläche

## Aktuelle Änderungen (parser-v2 Branch)

Während unserer Arbeit haben wir folgende Verbesserungen vorgenommen:

1. **Anonymisierungsmodus erweitert**:
   - Name wird zu "XXXXX XXXXX" anonymisiert
   - Wohnort wird zu "XXXXX XXXXX" anonymisiert
   - E-Mail wird zu "xxxxx@xxxxx.xx" anonymisiert
   - Telefonnummer wird zu "XXXX XXXXXXXX" anonymisiert

2. **Ansprechpartner-System verbessert**:
   - Dropdown-Menü mit festen Optionen (Kai Fischer, Melike Demirkol, Konrad Ruszyk, Alessandro Böhm, Salim Alizai)
   - Automatische E-Mail-Generierung nach dem Schema "nachname@galdora.de"
   - Telefonnummer ist für alle Ansprechpartner einheitlich "02161 62126-02"

3. **PDF-Vorschau-Probleme behoben**:
   - Verwendung von `<object>` statt `<iframe>` für bessere Browser-Kompatibilität
   - Alternative Anzeige-/Downloadoptionen für Fälle, in denen Chrome die Anzeige blockiert
   - Verbesserte Darstellung mit Rahmen und optimierter Höhe (850px)

4. **Fehlerbehandlung verbessert**:
   - Robustere Initialisierung der `st.session_state.temp_files` Variable
   - Überprüfung auf Existenz von temporären Dateien vor dem Löschen
   - Verbesserte Fehlerbehandlung in der cleanup-Funktion

## Bekannte Probleme

1. **PDF-Anzeige in Chrome**: Chrome blockiert manchmal die Anzeige von PDF-Dateien aus Sicherheitsgründen. Wir haben Alternativlösungen implementiert (direkter Download), aber die grundlegende Browser-Einschränkung bleibt bestehen.

2. **Session-State-Fehler**: Bei Streaming-Neustarts kann es zu Fehlern kommen, wenn auf `st.session_state.temp_files` zugegriffen wird, bevor es initialisiert wurde. Dies wurde mit robusteren Prüfungen behandelt.

## Zukünftige Verbesserungen

- Implementierung mehrsprachiger Unterstützung (aktuell nur Deutsch)
- Verbesserung der KI-Extraktion durch Feintuning
- Integration mit ATS (Applicant Tracking Systems)
- Migration auf HTTPS für bessere PDF-Vorschau

## Installation und Ausführung

1. Repository klonen
2. Virtuelle Umgebung aktivieren: `source venv/bin/activate`
3. Abhängigkeiten installieren: `pip install -r requirements.txt`
4. Anwendung starten: `streamlit run app.py`
5. Im Browser unter http://localhost:8501 aufrufen

## Branches

- **main**: Stabile Hauptversion
- **v2-funktioniert**: Branch mit den grundlegenden Funktionalitäten von v2
- **parser-v2**: Aktuelle Entwicklungsversion mit allen neuesten Verbesserungen

Diese Zusammenfassung sollte einem erfahrenen Programmierer einen guten Überblick über den aktuellen Stand des Projekts und die vorgenommenen Änderungen geben. Die Context.md-Datei bietet zusätzliche Details zur Anwendung und ihrer Architektur.
