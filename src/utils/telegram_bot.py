import os
import tempfile
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Projektspezifische Importe
from ..core.combined_processor import CombinedProcessor
from ..templates.template_generator import TemplateGenerator
from .config import get_openai_api_key, get_telegram_bot_token

class TelegramBot:
    """
    Ein Telegram-Bot zum Empfangen und Verarbeiten von Lebensläufen.
    """
    
    def __init__(self):
        """Initialisiert den Telegram-Bot mit Token und richtet Handler ein."""
        self.token = get_telegram_bot_token()
        self.openai_api_key = get_openai_api_key()
        
        if not self.token:
            raise ValueError("Telegram Bot Token nicht gefunden. Bitte in der Konfiguration einstellen.")
        
        if not self.openai_api_key:
            raise ValueError("OpenAI API-Key nicht gefunden. Bitte in der Konfiguration einstellen.")
        
        # Logger konfigurieren
        self.logger = logging.getLogger("telegram_bot")
        self.logger.setLevel(logging.INFO)
        
        # Telegram Application erstellen
        self.application = ApplicationBuilder().token(self.token).build()
        
        # Handler registrieren
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(MessageHandler(filters.Document.ALL, self.process_document))
        self.application.add_handler(MessageHandler(filters.PHOTO, self.process_photo))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Sendet eine Begrüßungsnachricht, wenn der Benutzer den /start Befehl verwendet."""
        await update.message.reply_text(
            "👋 Willkommen beim CV2Profile Bot!\n\n"
            "Sende mir einen Lebenslauf als PDF, DOCX, JPG oder PNG, "
            "und ich werde ihn automatisch in ein standardisiertes Profil umwandeln.\n\n"
            "Unterstützte Formate: PDF, DOCX, JPG, PNG\n"
            "Verwende /help für weitere Informationen."
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Sendet eine Hilfenachricht mit verfügbaren Befehlen und Funktionen."""
        await update.message.reply_text(
            "📋 *CV2Profile Bot - Hilfe*\n\n"
            "*Verfügbare Befehle:*\n"
            "/start - Bot starten\n"
            "/help - Diese Hilfenachricht anzeigen\n\n"
            "*Unterstützte Formate:*\n"
            "- PDF-Dokumente\n"
            "- Word-Dokumente (DOCX)\n"
            "- Bilder (JPG, PNG)\n\n"
            "*Verwendung:*\n"
            "1. Sende einfach deinen Lebenslauf als Dokument oder Foto\n"
            "2. Warte, während ich ihn analysiere (dies kann einige Sekunden dauern)\n"
            "3. Erhalte ein professionell formatiertes Profil als PDF\n\n"
            "Bei Problemen oder Fragen wende dich bitte an support@example.com",
            parse_mode="Markdown"
        )
    
    async def process_document(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Verarbeitet ein hochgeladenes Dokument (PDF, DOCX)."""
        # Nachricht senden, dass Verarbeitung gestartet wurde
        processing_message = await update.message.reply_text(
            "🔄 Dein Lebenslauf wird verarbeitet... Bitte warte einen Moment."
        )
        
        try:
            # Dokument herunterladen
            document = update.message.document
            file_name = document.file_name
            file_extension = os.path.splitext(file_name)[1].lower()
            
            # Überprüfen, ob das Format unterstützt wird
            if file_extension not in ['.pdf', '.docx', '.jpg', '.jpeg', '.png']:
                await processing_message.edit_text(
                    "❌ Nicht unterstütztes Dateiformat. Bitte sende einen Lebenslauf als PDF, DOCX, JPG oder PNG."
                )
                return
            
            # Datei herunterladen
            file = await context.bot.get_file(document.file_id)
            
            # Datei in temporäres Verzeichnis speichern
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
                await file.download_to_drive(tmp_file.name)
                temp_file_path = tmp_file.name
                
                # Statusnachricht aktualisieren
                await processing_message.edit_text(
                    "🔍 Dokument empfangen. Analysiere Inhalte..."
                )
                
                # Dokument verarbeiten
                await self._process_file(update, context, temp_file_path, file_extension, processing_message)
                
                # Temporäre Datei löschen
                os.remove(temp_file_path)
        
        except Exception as e:
            self.logger.error(f"Fehler bei der Dokumentverarbeitung: {str(e)}")
            await processing_message.edit_text(
                f"❌ Bei der Verarbeitung ist ein Fehler aufgetreten: {str(e)}\n"
                "Bitte versuche es später erneut oder kontaktiere den Support."
            )
    
    async def process_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Verarbeitet ein hochgeladenes Foto (als Lebenslauf-Scan)."""
        # Nachricht senden, dass Verarbeitung gestartet wurde
        processing_message = await update.message.reply_text(
            "🔄 Dein Lebenslauf wird verarbeitet... Bitte warte einen Moment."
        )
        
        try:
            # Größtes Foto auswählen
            photo = update.message.photo[-1]
            
            # Datei herunterladen
            file = await context.bot.get_file(photo.file_id)
            
            # Datei in temporäres Verzeichnis speichern
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                await file.download_to_drive(tmp_file.name)
                temp_file_path = tmp_file.name
                
                # Statusnachricht aktualisieren
                await processing_message.edit_text(
                    "🔍 Bild empfangen. Analysiere Inhalte..."
                )
                
                # Dokument verarbeiten
                await self._process_file(update, context, temp_file_path, '.jpg', processing_message)
                
                # Temporäre Datei löschen
                os.remove(temp_file_path)
        
        except Exception as e:
            self.logger.error(f"Fehler bei der Bildverarbeitung: {str(e)}")
            await processing_message.edit_text(
                f"❌ Bei der Verarbeitung ist ein Fehler aufgetreten: {str(e)}\n"
                "Bitte versuche es später erneut oder kontaktiere den Support."
            )
    
    async def _process_file(self, update, context, file_path, file_extension, processing_message):
        """Verarbeitet die temporäre Datei mit dem CV-Parser."""
        try:
            # Statusnachricht aktualisieren
            await processing_message.edit_text(
                "⚙️ Extrahiere Informationen aus dem Lebenslauf..."
            )
            
            # Combined Processor initialisieren und Dokument verarbeiten
            combined_processor = CombinedProcessor(self.openai_api_key)
            extracted_text, profile_data = combined_processor.process_and_extract(file_path, file_extension)
            
            # Statusnachricht aktualisieren
            await processing_message.edit_text(
                "📄 Erstelle standardisiertes Profil..."
            )
            
            # Template Generator initialisieren und Profil erstellen
            template_gen = TemplateGenerator()
            # Standard-Template verwenden (kann später angepasst werden)
            pdf_path = template_gen.generate_pdf(profile_data, template_name="Classic")
            
            # Statusnachricht aktualisieren
            await processing_message.edit_text(
                "✅ Profil erstellt! Sende generiertes Dokument..."
            )
            
            # Profildaten für Dateinamen verwenden
            person_name = profile_data.get('persönliche_daten', {}).get('name', 'Profil')
            
            # PDF senden
            with open(pdf_path, 'rb') as pdf_file:
                await context.bot.send_document(
                    chat_id=update.effective_chat.id,
                    document=pdf_file,
                    filename=f"{person_name}.pdf",
                    caption="🎉 Hier ist dein standardisiertes Profil!"
                )
            
            # Erfolgsinfo senden
            await processing_message.edit_text(
                "✅ Verarbeitung abgeschlossen! Das generierte Profil wurde gesendet."
            )
            
            # Temporäre PDF-Datei löschen
            os.remove(pdf_path)
            
        except Exception as e:
            self.logger.error(f"Fehler bei der Dateiverarbeitung: {str(e)}")
            await processing_message.edit_text(
                f"❌ Bei der Verarbeitung ist ein Fehler aufgetreten: {str(e)}\n"
                "Bitte versuche es später erneut oder kontaktiere den Support."
            )
    
    def start(self):
        """Startet den Bot und beginnt mit dem Polling für Nachrichten."""
        self.logger.info("Starte Telegram Bot...")
        self.application.run_polling()


# Funktion zum einfachen Starten des Bots aus anderen Modulen
def run_telegram_bot():
    bot = TelegramBot()
    bot.start()


if __name__ == "__main__":
    # Direkte Ausführung dieser Datei startet den Bot
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    run_telegram_bot() 