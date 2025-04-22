import openai
import json
import os
import time

class AIExtractor:
    """Klasse zur KI-gestützten Extraktion von Informationen aus Dokumenten"""
    
    def __init__(self, api_key=None):
        """
        Initialisiert den AI-Extraktor
        
        Args:
            api_key: OpenAI API Key
        """
        # Versuche, API-Key aus verschiedenen Quellen zu beziehen
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API Key ist erforderlich. Bitte geben Sie einen API-Key an oder setzen Sie die Umgebungsvariable OPENAI_API_KEY.")
        
        # API-Key setzen
        openai.api_key = self.api_key
    
    def extract_profile_data(self, text, document_type):
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
        
        # Mehrere Versuche bei API-Fehlern
        max_retries = 3
        retry_delay = 2  # Sekunden
        
        for attempt in range(max_retries):
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
                    
                    # Validiere die Struktur der extrahierten Daten
                    if not self._validate_extracted_data(extracted_data):
                        print("Warnung: Ungültige Datenstruktur nach Extraktion. Fallback wird verwendet.")
                        return self._create_default_data_structure()
                    
                    return extracted_data
                except json.JSONDecodeError:
                    # Fallback-Mechanismus: Versuche JSON aus Freitext zu extrahieren
                    return self._extract_json_from_text(response_text)
                    
            except Exception as e:
                print(f"Fehler bei der KI-Extraktion (Versuch {attempt+1}/{max_retries}): {str(e)}")
                if attempt < max_retries - 1:
                    print(f"Wiederholung in {retry_delay} Sekunden...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponentielles Backoff
                else:
                    print("Alle Wiederholungsversuche fehlgeschlagen. Verwende Standard-Datenstruktur.")
                    return self._create_default_data_structure()
        
        # Sollte nie hierher gelangen, aber als Fallback
        return self._create_default_data_structure()
    
    def _validate_extracted_data(self, data):
        """Überprüft, ob die extrahierten Daten die erwartete Struktur haben"""
        try:
            # Überprüfe grundlegende Struktur
            if not isinstance(data, dict):
                return False
                
            # Überprüfe, ob persönliche_daten vorhanden ist
            if 'persönliche_daten' not in data or not isinstance(data['persönliche_daten'], dict):
                return False
                
            # Überprüfe, ob die Listen für Berufserfahrung, Ausbildung und Weiterbildungen existieren
            for key in ['berufserfahrung', 'ausbildung', 'weiterbildungen']:
                if key not in data or not isinstance(data[key], list):
                    return False
            
            return True
        except:
            return False
    
    def _create_default_data_structure(self):
        """Erstellt eine Standard-Datenstruktur für den Fall, dass die Extraktion fehlschlägt"""
        return {
            "persönliche_daten": {
                "name": "Nicht erkannt",
                "wohnort": "",
                "jahrgang": "",
                "führerschein": "Klasse B",
                "kontakt": {
                    "ansprechpartner": "Fischer",
                    "telefon": "02161 62126-02",
                    "email": "fischer@galdora.de"
                }
            },
            "berufserfahrung": [],
            "ausbildung": [],
            "weiterbildungen": []
        }
    
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
  ]
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
                parsed_json = json.loads(json_str)
                
                # Validiere die extrahierten Daten
                if self._validate_extracted_data(parsed_json):
                    return parsed_json
            
            # JSON nicht gefunden oder ungültig, verwende Standardstruktur
            return self._create_default_data_structure()
        except Exception as e:
            print(f"Fehler beim Extrahieren von JSON aus Text: {str(e)}")
            # Bei Fehlern Standardstruktur zurückgeben
            return self._create_default_data_structure()
