# CV Parser und Profilgenerator

## Übersicht

Diese Anwendung ist ein leistungsstarker CV-Parser, der Lebensläufe automatisch analysiert und in ein standardisiertes Format umwandelt. Die Software nutzt KI-Technologie (OpenAI), um relevante Informationen aus verschiedenen Dokumenttypen zu extrahieren und in strukturierte Daten zu konvertieren.

## Hauptfunktionen

- **Dokumentverarbeitung**: Unterstützung verschiedener Formate wie PDF, DOCX, JPG und PNG
- **Text-Extraktion**: Intelligente Extraktion von Text aus allen unterstützten Dokumentformaten
- **KI-gestützte Analyse**: Nutzung von OpenAI-Modellen zur Identifizierung von Schlüsselinformationen
- **Strukturierte Profilerstellung**: Generierung standardisierter Profile im PDF-Format
- **Benutzerfreundliche Oberfläche**: Einfache Handhabung durch Streamlit-Frontend

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

1. OpenAI API-Schlüssel in der Seitenleiste eingeben
2. Lebenslauf hochladen (PDF, DOCX, JPG oder PNG)
3. Extrahierte Daten überprüfen und bei Bedarf bearbeiten
4. Profil generieren und herunterladen

## Aktuelle Grenzen und zukünftige Erweiterungen

- Aktuell nur deutsche Sprache vollständig unterstützt
- Erweiterung um mehrsprachige Unterstützung geplant
- Verbesserung der KI-Extraktion durch Feintuning geplant
- Integration mit ATS (Applicant Tracking Systems) möglich

## Datenschutz und Sicherheit

- Lokale Verarbeitung der Dokumente
- Temporäre Dateien werden nach der Verarbeitung gelöscht
- Nur für die KI-Analyse werden Daten an OpenAI übertragen (gemäß deren Datenschutzrichtlinien)
- Keine dauerhafte Speicherung von Bewerberdaten in der Anwendung 