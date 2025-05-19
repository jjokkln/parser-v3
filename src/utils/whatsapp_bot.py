import os
import tempfile
import logging
import requests
from twilio.rest import Client
from flask import Flask, request, jsonify
import json

# Projektspezifische Importe
from ..core.combined_processor import CombinedProcessor
from ..templates.template_generator import TemplateGenerator
from .config import get_openai_api_key, get_twilio_credentials

class WhatsAppBot:
    """
    Ein WhatsApp-Bot zum Empfangen und Verarbeiten von Lebensläufen über Twilio.
    """
    
    def __init__(self):
        """Initialisiert den WhatsApp-Bot mit Twilio-Credentials."""
        # Twilio Konfiguration laden
        account_sid, auth_token, phone_number = get_twilio_credentials()
        self.phone_number = phone_number  # Twilio WhatsApp-Nummer
        
        # OpenAI API-Key
        self.openai_api_key = get_openai_api_key()
        
        if not account_sid or not auth_token or not phone_number:
            raise ValueError("Twilio-Credentials nicht vollständig. Bitte in der Konfiguration einstellen.")
        
        if not self.openai_api_key:
            raise ValueError("OpenAI API-Key nicht gefunden. Bitte in der Konfiguration einstellen.")
        
        # Twilio Client initialisieren
        self.client = Client(account_sid, auth_token)
        
        # Logger konfigurieren
        self.logger = logging.getLogger("whatsapp_bot")
        self.logger.setLevel(logging.INFO)
    
    def send_message(self, to_number, message):
        """Sendet eine Textnachricht an die angegebene Nummer."""
        try:
            message = self.client.messages.create(
                from_=f'whatsapp:{self.phone_number}',
                body=message,
                to=f'whatsapp:{to_number}'
            )
            self.logger.info(f"Nachricht gesendet an {to_number}, SID: {message.sid}")
            return True
        except Exception as e:
            self.logger.error(f"Fehler beim Senden der Nachricht an {to_number}: {str(e)}")
            return False
    
    def send_document(self, to_number, document_url, caption=None):
        """Sendet ein Dokument an die angegebene Nummer."""
        try:
            message = self.client.messages.create(
                from_=f'whatsapp:{self.phone_number}',
                media_url=[document_url],
                body=caption,
                to=f'whatsapp:{to_number}'
            )
            self.logger.info(f"Dokument gesendet an {to_number}, SID: {message.sid}")
            return True
        except Exception as e:
            self.logger.error(f"Fehler beim Senden des Dokuments an {to_number}: {str(e)}")
            return False
    
    def process_incoming_message(self, from_number, message_body, media_url=None, media_content_type=None):
        """
        Verarbeitet eine eingehende Nachricht und Medien.
        
        Args:
            from_number: Die Telefonnummer des Absenders (ohne 'whatsapp:' Präfix)
            message_body: Der Text der Nachricht
            media_url: Die URL des angehängten Medienobjekts (wenn vorhanden)
            media_content_type: Der Medientyp (z.B. 'application/pdf')
        """
        # Begrüßungsnachricht, wenn kein Medium, aber Text vorhanden ist
        if not media_url and message_body:
            if "start" in message_body.lower() or "hallo" in message_body.lower() or "hi" in message_body.lower():
                self.send_message(
                    from_number,
                    "👋 Willkommen beim CV2Profile Bot!\n\n"
                    "Sende mir einen Lebenslauf als PDF, DOCX, JPG oder PNG, "
                    "und ich werde ihn automatisch in ein standardisiertes Profil umwandeln.\n\n"
                    "Unterstützte Formate: PDF, DOCX, JPG, PNG"
                )
                return True
            elif "hilfe" in message_body.lower() or "help" in message_body.lower():
                self.send_message(
                    from_number,
                    "📋 *CV2Profile Bot - Hilfe*\n\n"
                    "*Unterstützte Formate:*\n"
                    "- PDF-Dokumente\n"
                    "- Word-Dokumente (DOCX)\n"
                    "- Bilder (JPG, PNG)\n\n"
                    "*Verwendung:*\n"
                    "1. Sende einfach deinen Lebenslauf als Dokument oder Foto\n"
                    "2. Warte, während ich ihn analysiere (dies kann einige Sekunden dauern)\n"
                    "3. Erhalte ein professionell formatiertes Profil als PDF\n\n"
                    "Bei Problemen oder Fragen wende dich bitte an support@example.com"
                )
                return True
            else:
                self.send_message(
                    from_number,
                    "Bitte sende einen Lebenslauf als Dokument oder Foto. "
                    "Sende 'hilfe' für weitere Informationen."
                )
                return True
        
        # Wenn keine Medien-URL vorhanden ist, beenden
        if not media_url:
            self.send_message(
                from_number, 
                "Ich konnte keine Medien in deiner Nachricht finden. "
                "Bitte sende einen Lebenslauf als Dokument oder Foto."
            )
            return False
        
        # Format überprüfen basierend auf Content-Type oder Dateiendung
        supported_types = [
            'application/pdf', 
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'image/jpeg',
            'image/jpg',
            'image/png'
        ]
        
        if media_content_type and media_content_type not in supported_types:
            self.send_message(
                from_number,
                "❌ Nicht unterstütztes Dateiformat. Bitte sende einen Lebenslauf als PDF, DOCX, JPG oder PNG."
            )
            return False
        
        # Statusnachricht senden
        self.send_message(
            from_number,
            "🔄 Dein Lebenslauf wird verarbeitet... Bitte warte einen Moment."
        )
        
        # Medien herunterladen und verarbeiten
        try:
            # Dateiendung bestimmen
            if media_content_type == 'application/pdf':
                file_extension = '.pdf'
            elif media_content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                file_extension = '.docx'
            elif media_content_type in ['image/jpeg', 'image/jpg']:
                file_extension = '.jpg'
            elif media_content_type == 'image/png':
                file_extension = '.png'
            else:
                # Fallback: Versuch, die Endung aus der URL zu extrahieren
                file_extension = os.path.splitext(media_url)[1].lower()
                if not file_extension or file_extension not in ['.pdf', '.docx', '.jpg', '.jpeg', '.png']:
                    file_extension = '.pdf'  # Standard-Fallback
            
            # Medien herunterladen
            response = requests.get(media_url)
            if response.status_code != 200:
                self.send_message(
                    from_number,
                    f"❌ Fehler beim Herunterladen der Datei (Status: {response.status_code})."
                )
                return False
            
            # Datei in temporäres Verzeichnis speichern
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
                tmp_file.write(response.content)
                temp_file_path = tmp_file.name
                
                # Statusnachricht aktualisieren
                self.send_message(
                    from_number,
                    "🔍 Dokument empfangen. Analysiere Inhalte..."
                )
                
                # Dokument verarbeiten
                success = self._process_file(from_number, temp_file_path, file_extension)
                
                # Temporäre Datei löschen
                os.remove(temp_file_path)
                
                return success
                
        except Exception as e:
            self.logger.error(f"Fehler bei der Dateiverarbeitung: {str(e)}")
            self.send_message(
                from_number,
                f"❌ Bei der Verarbeitung ist ein Fehler aufgetreten: {str(e)}\n"
                "Bitte versuche es später erneut oder kontaktiere den Support."
            )
            return False
    
    def _process_file(self, from_number, file_path, file_extension):
        """Verarbeitet die temporäre Datei mit dem CV-Parser."""
        try:
            # Statusnachricht aktualisieren
            self.send_message(
                from_number,
                "⚙️ Extrahiere Informationen aus dem Lebenslauf..."
            )
            
            # Combined Processor initialisieren und Dokument verarbeiten
            combined_processor = CombinedProcessor(self.openai_api_key)
            extracted_text, profile_data = combined_processor.process_and_extract(file_path, file_extension)
            
            # Statusnachricht aktualisieren
            self.send_message(
                from_number,
                "📄 Erstelle standardisiertes Profil..."
            )
            
            # Template Generator initialisieren und Profil erstellen
            template_gen = TemplateGenerator()
            # Standard-Template verwenden (kann später angepasst werden)
            pdf_path = template_gen.generate_pdf(profile_data, template_name="Classic")
            
            # Profildaten für Dateinamen verwenden
            person_name = profile_data.get('persönliche_daten', {}).get('name', 'Profil')
            
            # Datei hochladen und Link erhalten (z.B. zu einem Cloud-Storage - Beispielimplementierung)
            try:
                # In einer realen Implementierung würden wir die Datei auf einen Server hochladen
                # und eine öffentlich zugängliche URL zurückgeben
                # Hier ein Platzhalter für den tatsächlichen Upload-Prozess:
                #
                # upload_url = upload_to_cloud_storage(pdf_path, f"{person_name}.pdf")
                #
                # Für diese Beispielimplementierung verwenden wir eine lokale URL
                # (die in Produktionsumgebungen durch einen tatsächlichen Upload-Prozess ersetzt werden sollte)
                upload_url = f"https://example.com/uploads/{os.path.basename(pdf_path)}"
                
                # PDF über WhatsApp senden
                self.send_document(
                    from_number,
                    upload_url,
                    "🎉 Hier ist dein standardisiertes Profil!"
                )
                
                # Erfolgsinfo senden
                self.send_message(
                    from_number,
                    "✅ Verarbeitung abgeschlossen! Das generierte Profil wurde gesendet."
                )
                
                # Temporäre PDF-Datei löschen
                os.remove(pdf_path)
                
                return True
                
            except Exception as e:
                self.logger.error(f"Fehler beim Datei-Upload: {str(e)}")
                # Als Fallback, erklären wir dem Benutzer, dass wir die Datei nicht senden konnten
                self.send_message(
                    from_number,
                    f"⚠️ Profil erstellt, aber ein Fehler trat beim Senden auf: {str(e)}\n"
                    "Bitte versuche es später erneut."
                )
                # Temporäre PDF-Datei löschen
                os.remove(pdf_path)
                return False
            
        except Exception as e:
            self.logger.error(f"Fehler bei der Dateiverarbeitung: {str(e)}")
            self.send_message(
                from_number,
                f"❌ Bei der Verarbeitung ist ein Fehler aufgetreten: {str(e)}\n"
                "Bitte versuche es später erneut oder kontaktiere den Support."
            )
            return False


# Flask-App für den Webhook-Endpunkt
app = Flask(__name__)
whatsapp_bot = None

@app.route('/webhook/whatsapp', methods=['POST'])
def whatsapp_webhook():
    """Webhook für WhatsApp-Updates (via Twilio)"""
    global whatsapp_bot
    
    # Wenn der Bot noch nicht initialisiert wurde
    if whatsapp_bot is None:
        try:
            whatsapp_bot = WhatsAppBot()
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    
    # Formular-Daten auslesen
    from_number = request.form.get('From', '').replace('whatsapp:', '')
    body = request.form.get('Body', '')
    
    # Mediendaten prüfen
    num_media = int(request.form.get('NumMedia', '0'))
    
    if num_media > 0:
        media_url = request.form.get('MediaUrl0', None)
        media_content_type = request.form.get('MediaContentType0', None)
        whatsapp_bot.process_incoming_message(from_number, body, media_url, media_content_type)
    else:
        # Nachricht ohne Medien
        whatsapp_bot.process_incoming_message(from_number, body)
    
    return jsonify({"status": "ok"})


def run_whatsapp_webhook(host='0.0.0.0', port=5000, debug=False):
    """Startet den Flask-Server für den WhatsApp-Webhook."""
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    # Direkte Ausführung dieser Datei startet den Webhook-Server
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    run_whatsapp_webhook(debug=True) 