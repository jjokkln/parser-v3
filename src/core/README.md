# core - Kernfunktionalität

Dieses Verzeichnis enthält die Kernfunktionalität des CV2Profile-Parsers, die für die Dokumentenverarbeitung und KI-gestützte Informationsextraktion zuständig ist.

## Enthaltene Dateien

- **ai_extractor.py**: Analysiert den extrahierten Text mittels KI
  - Verwendet OpenAI-API zur Strukturierung der Daten
  - Extrahiert persönliche Daten, Berufserfahrung, Ausbildung und Weiterbildungen
  - Formatiert die Daten in ein standardisiertes JSON-Format

- **combined_processor.py**: Kombinierte Verarbeitungslogik für den gesamten Extraktionsprozess
  - Koordiniert den Workflow zwischen Dokumentverarbeitung und KI-Extraktion
  - Organisiert die Prozessschritte von der Textextraktion bis zur strukturierten Datenausgabe
  - Enthält die Hauptlogik für die Verarbeitung von Lebensläufen

- **document_processor.py**: Verarbeitet Dokumente und extrahiert Text
  - Unterstützt PDF-Dokumente mit direkter Textextraktion und OCR-Fallback
  - Verarbeitet Bilddateien mittels OCR (Optical Character Recognition)
  - Extrahiert Text aus Word-Dokumenten (DOCX)

## Verwendung

Die Module in diesem Verzeichnis werden hauptsächlich durch die Hauptanwendung (`main.py`) oder durch den UI-Layer (`src/ui/app.py`) aufgerufen, um Dokumentenverarbeitung und Datenextraktion durchzuführen. 