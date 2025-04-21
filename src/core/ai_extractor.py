import openai
import json
import os

class AIExtractor:
    """Klasse zur KI-gestützten Extraktion von Informationen aus Dokumenten"""
    
    def __init__(self, api_key=None):
        """
        Initialisiert den AI-Extraktor
        
        Args:
            api_key: OpenAI API Key
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API Key ist erforderlich")
        
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
                    "weiterbildungen": []
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
                "weiterbildungen": []
            }
