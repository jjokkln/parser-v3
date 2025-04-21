import io
import os
from PIL import Image
import pytesseract
import PyPDF2
from pdf2image import convert_from_path
from docx import Document
import openai
import json

class CombinedProcessor:
    """
    Kombinierte Klasse zur Verarbeitung von Dokumenten und KI-Extraktion in einem Schritt.
    Diese Klasse verbindet die Funktionalitäten des DocumentProcessor und AIExtractor.
    """
    
    def __init__(self, api_key=None):
        """
        Initialisiert den kombinierten Prozessor
        
        Args:
            api_key: OpenAI API Key (optional, kann auch aus Umgebungsvariable geladen werden)
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API Key ist erforderlich")
        
        openai.api_key = self.api_key
    
    def process_and_extract(self, file_path, file_extension):
        """
        Hauptfunktion, die sowohl die Textextraktion als auch die KI-Analyse in einem Schritt durchführt.
        
        Args:
            file_path: Pfad zur Datei
            file_extension: Dateierweiterung
        
        Returns:
            Tuple mit (extrahierter Text, strukturierte Profildaten)
        """
        # Schritt 1: Text aus Dokument extrahieren
        extracted_text = self._process_document(file_path, file_extension)
        
        # Schritt 2: KI-Analyse der extrahierten Daten
        profile_data = self._extract_profile_data(extracted_text, file_extension)
        
        return extracted_text, profile_data
    
    def extract_and_process(self, file_path, file_extension):
        """
        Alternative Hauptfunktion, die die KI-Analyse und Textextraktion in umgekehrter Reihenfolge durchführt.
        In der Praxis führt diese Methode zuerst die Extraktion durch (technisch nicht anders möglich)
        und liefert die Ergebnisse in umgekehrter Reihenfolge zurück.
        
        Args:
            file_path: Pfad zur Datei
            file_extension: Dateierweiterung
        
        Returns:
            Tuple mit (strukturierte Profildaten, extrahierter Text)
        """
        # Tatsächlich muss zuerst der Text extrahiert werden, bevor die KI-Analyse erfolgen kann
        extracted_text = self._process_document(file_path, file_extension)
        profile_data = self._extract_profile_data(extracted_text, file_extension)
        
        # Gebe die Ergebnisse in umgekehrter Reihenfolge zurück
        return profile_data, extracted_text
    
    # ---- Dokumentenverarbeitung (aus DocumentProcessor) ----
    
    def _process_document(self, file_path, file_extension):
        """
        Extrahiert Text aus Dokumenten verschiedenen Typs
        
        Args:
            file_path: Pfad zur Datei
            file_extension: Dateierweiterung
        
        Returns:
            String mit extrahiertem Text
        """
        if file_extension.lower() in ['.pdf']:
            return self._extract_from_pdf(file_path)
        elif file_extension.lower() in ['.jpg', '.jpeg', '.png']:
            return self._extract_from_image(file_path)
        elif file_extension.lower() in ['.docx']:
            return self._extract_from_docx(file_path)
        else:
            raise ValueError(f"Nicht unterstützter Dateityp: {file_extension}")
    
    def _extract_from_pdf(self, file_path):
        """Extrahiert Text aus PDF-Dateien"""
        text = ""
        
        # Versuche zunächst direkte Textextraktion
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:  # Wenn Text erfolgreich extrahiert wurde
                        text += page_text + "\n"
        except Exception as e:
            print(f"Fehler bei direkter PDF-Textextraktion: {str(e)}")
        
        # Falls kein oder wenig Text extrahiert wurde, OCR verwenden
        if len(text.strip()) < 100:  # Heuristik: Weniger als 100 Zeichen bedeutet wahrscheinlich ein Scan
            try:
                # PDF in Bilder umwandeln und OCR durchführen
                images = convert_from_path(file_path)
                for i, image in enumerate(images):
                    page_text = pytesseract.image_to_string(image, lang='deu')  # Deutsch für deutsche Dokumente
                    text += page_text + "\n"
            except Exception as e:
                print(f"Fehler bei PDF-OCR: {str(e)}")
                # Wenn auch OCR fehlschlägt, zurückgeben was wir haben
        
        return text
    
    def _extract_from_image(self, file_path):
        """Extrahiert Text aus Bilddateien mit OCR"""
        try:
            image = Image.open(file_path)
            # OCR für deutsche Dokumente
            text = pytesseract.image_to_string(image, lang='deu')
            return text
        except Exception as e:
            raise Exception(f"Fehler bei der Bildverarbeitung: {str(e)}")
    
    def _extract_from_docx(self, file_path):
        """Extrahiert Text aus Word-Dokumenten"""
        try:
            doc = Document(file_path)
            full_text = []
            
            # Text aus Absätzen extrahieren
            for para in doc.paragraphs:
                full_text.append(para.text)
            
            # Text aus Tabellen extrahieren
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        full_text.append(cell.text)
            
            return '\n'.join(full_text)
        except Exception as e:
            raise Exception(f"Fehler bei der Word-Dokumentverarbeitung: {str(e)}")
    
    # ---- KI-Extraktion (aus AIExtractor) ----
    
    def _extract_profile_data(self, text, document_type):
        """
        Extrahiert strukturierte Profildaten aus Text mit KI-Unterstützung
        
        Args:
            text: Extrahierter Text aus dem Dokument
            document_type: Typ des Dokuments (Dateiendung)
        
        Returns:
            Dictionary mit strukturierten Profildaten
        """
        # Bereite den Prompt für die KI vor
        prompt = self._create_extraction_prompt(text, document_type)
        
        try:
            # OpenAI API-Aufruf
            response = openai.chat.completions.create(
                model="gpt-4o-mini",  # Verwende ein kostengünstiges Modell
                messages=[
                    {"role": "system", "content": "Du bist ein präziser Datenextraktions-Assistent für Lebensläufe."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1  # Niedrige Temperatur für konsistente Ergebnisse
            )
            
            # Extrahiere den Antworttext
            response_text = response.choices[0].message.content
            
            # Versuche JSON zu parsen
            try:
                extracted_data = json.loads(response_text)
                return extracted_data
            except json.JSONDecodeError:
                # Fallback-Mechanismus: Versuche JSON aus Freitext zu extrahieren
                return self._extract_json_from_text(response_text)
                
        except Exception as e:
            raise Exception(f"Fehler bei der KI-Extraktion: {str(e)}")
    
    def _create_extraction_prompt(self, text, document_type):
        """Erstellt einen Prompt für die KI-Extraktion"""
        return f"""
Du bist ein Assistent für die Extraktion von Lebenslaufdaten. Analysiere den folgenden Text aus einem {document_type}-Dokument und extrahiere alle relevanten Informationen in das spezifizierte JSON-Format.

Der Text stammt aus einem Lebenslauf und enthält Informationen über eine Person, ihre Berufserfahrung, Ausbildung und Qualifikationen.

Extrahierter Text:
{text}

Liefere das Ergebnis ausschließlich im folgenden JSON-Format ohne zusätzlichen Text oder Erklärungen:
{{
  "persönliche_daten": {{
    "name": "",
    "wohnort": "",
    "jahrgang": "",
    "führerschein": "",
    "kontakt": {{
      "ansprechpartner": "",
      "telefon": "",
      "email": ""
    }}
  }},
  "berufserfahrung": [
    {{
      "zeitraum": "",
      "unternehmen": "",
      "position": "",
      "aufgaben": []
    }}
  ],
  "ausbildung": [
    {{
      "zeitraum": "",
      "institution": "",
      "schwerpunkte": "",
      "abschluss": "",
      "note": ""
    }}
  ],
  "weiterbildungen": [
    {{
      "zeitraum": "",
      "bezeichnung": "",
      "abschluss": ""
    }}
  ]}},
  "wunschgehalt": ""
}}

Hinweise:
- Achte darauf, das exakte JSON-Format zu verwenden
- Vervollständige alle Felder, die im Text identifiziert werden können
- Lasse Felder leer, wenn keine Information vorhanden ist
- Organisiere die berufliche Erfahrung chronologisch (neueste zuerst)
- Bei Studiengängen extrahiere auch die Studienschwerpunkte, falls angegeben
- Beim Führerschein gib auch an, ob ein PKW vorhanden ist, falls diese Information verfügbar ist
- Falls der Zeitraum als "Seit MM/JJJJ" angegeben ist, erfasse nur den Zeitpunkt (z.B. "07/2020")
- Versuche, die Aufgaben als einzelne Punkte zu strukturieren, statt als einen langen Text
- Das Wunschgehalt, falls erwähnt, sollte als Jahresgehalt in Euro extrahiert werden
"""
    
    def _extract_json_from_text(self, text):
        """
        Fallback-Methode zur Extraktion von JSON aus Freitext
        Nützlich, wenn das KI-Modell nicht nur JSON zurückgibt
        """
        # Versuche JSON-Daten aus dem Text zu extrahieren
        try:
            # Suche nach geschweiften Klammern, die JSON umschließen könnten
            start_idx = text.find('{')
            end_idx = text.rfind('}') + 1
            
            if start_idx >= 0 and end_idx > start_idx:
                json_str = text[start_idx:end_idx]
                return json.loads(json_str)
            else:
                # JSON nicht gefunden, einfache Struktur zurückgeben
                return {
                    "persönliche_daten": {
                        "name": "Nicht erkannt",
                        "wohnort": "",
                        "jahrgang": "",
                        "führerschein": "Klasse B (Pkw vorhanden)",
                        "kontakt": {
                            "ansprechpartner": "Fischer",
                            "telefon": "02161 62126-02",
                            "email": "fischer@galdora.de"
                        }
                    },
                    "berufserfahrung": [],
                    "ausbildung": [],
                    "weiterbildungen": [],
                    "wunschgehalt": ""
                }
        except Exception:
            # Bei Fehlern leere Struktur zurückgeben
            return {
                "persönliche_daten": {
                    "name": "Nicht erkannt",
                    "wohnort": "",
                    "jahrgang": "",
                    "führerschein": "Klasse B (Pkw vorhanden)",
                    "kontakt": {
                        "ansprechpartner": "Fischer",
                        "telefon": "02161 62126-02",
                        "email": "fischer@galdora.de"
                    }
                },
                "berufserfahrung": [],
                "ausbildung": [],
                "weiterbildungen": [],
                "wunschgehalt": ""
            } 