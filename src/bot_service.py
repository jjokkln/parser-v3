#!/usr/bin/env python3
"""
CV2Profile Bot-Dienst

Dieses Skript dient als Kommandozeilen-Schnittstelle zum Starten und Konfigurieren der Bots.
Es unterstützt sowohl Telegram als auch WhatsApp (über Twilio).
"""

import os
import sys
import argparse
import logging
from utils.config import (
    get_openai_api_key, save_telegram_bot_token, get_telegram_bot_token,
    save_twilio_credentials, get_twilio_credentials
)

# Den src-Ordner zum Pfad hinzufügen
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def setup_logger():
    """Richtet den Logger für das Skript ein"""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger

def setup_telegram_bot(args, logger):
    """Konfiguriert und startet den Telegram Bot"""
    # Token überprüfen/speichern
    if args.token:
        if args.save_token:
            logger.info("Speichere Telegram-Bot-Token für zukünftige Verwendung...")
            save_telegram_bot_token(args.token)
    
    # Prüfen, ob Token vorhanden
    token = args.token or get_telegram_bot_token()
    if not token:
        logger.error("Fehler: Kein Telegram-Bot-Token gefunden. Bitte geben Sie ein Token mit --token an.")
        return False
    
    # API-Key prüfen
    api_key = args.api_key or get_openai_api_key()
    if not api_key:
        logger.error("Fehler: Kein OpenAI API-Key gefunden.")
        return False
    
    logger.info("Starte Telegram Bot...")
    # Import hier, um Abhängigkeiten nur bei Bedarf zu laden
    from utils.telegram_bot import run_telegram_bot
    run_telegram_bot()
    return True

def setup_whatsapp_bot(args, logger):
    """Konfiguriert und startet den WhatsApp Bot"""
    # Twilio-Credentials überprüfen/speichern
    if args.account_sid and args.auth_token and args.phone_number:
        if args.save_credentials:
            logger.info("Speichere Twilio-Credentials für zukünftige Verwendung...")
            save_twilio_credentials(args.account_sid, args.auth_token, args.phone_number)
    
    # Prüfen, ob Credentials vorhanden
    account_sid, auth_token, phone_number = get_twilio_credentials()
    if not all([account_sid, auth_token, phone_number]):
        account_sid = args.account_sid or ""
        auth_token = args.auth_token or ""
        phone_number = args.phone_number or ""
        
        if not all([account_sid, auth_token, phone_number]):
            logger.error("Fehler: Twilio-Credentials nicht vollständig.")
            logger.error("Bitte geben Sie alle Credentials an: --account-sid, --auth-token, --phone-number")
            return False
    
    # API-Key prüfen
    api_key = args.api_key or get_openai_api_key()
    if not api_key:
        logger.error("Fehler: Kein OpenAI API-Key gefunden.")
        return False
    
    logger.info("Starte WhatsApp Webhook-Server...")
    # Import hier, um Abhängigkeiten nur bei Bedarf zu laden
    from utils.whatsapp_bot import run_whatsapp_webhook
    run_whatsapp_webhook(host=args.host, port=args.port, debug=args.debug)
    return True

def main():
    """Hauptfunktion zum Parsen der Argumente und Starten des entsprechenden Bots"""
    parser = argparse.ArgumentParser(description="CV2Profile Bot-Dienst")
    
    # Gemeinsame Argumente
    parser.add_argument("--api-key", help="OpenAI API-Key")
    
    # Bot-Typ-Auswahl
    bot_type = parser.add_mutually_exclusive_group(required=True)
    bot_type.add_argument("--telegram", action="store_true", help="Telegram-Bot starten")
    bot_type.add_argument("--whatsapp", action="store_true", help="WhatsApp-Bot (Twilio) starten")
    
    # Telegram-spezifische Argumente
    telegram_group = parser.add_argument_group("Telegram-Bot Optionen")
    telegram_group.add_argument("--token", help="Telegram-Bot-Token")
    telegram_group.add_argument("--save-token", action="store_true", help="Token für zukünftige Verwendung speichern")
    
    # WhatsApp/Twilio-spezifische Argumente
    whatsapp_group = parser.add_argument_group("WhatsApp-Bot Optionen (Twilio)")
    whatsapp_group.add_argument("--account-sid", help="Twilio Account SID")
    whatsapp_group.add_argument("--auth-token", help="Twilio Auth Token")
    whatsapp_group.add_argument("--phone-number", help="Twilio Telefonnummer (mit Ländervorwahl, ohne führendes +)")
    whatsapp_group.add_argument("--save-credentials", action="store_true", help="Twilio-Credentials für zukünftige Verwendung speichern")
    whatsapp_group.add_argument("--host", default="0.0.0.0", help="Host für den Webhook-Server (Standard: 0.0.0.0)")
    whatsapp_group.add_argument("--port", type=int, default=5000, help="Port für den Webhook-Server (Standard: 5000)")
    whatsapp_group.add_argument("--debug", action="store_true", help="Debug-Modus aktivieren")
    
    args = parser.parse_args()
    logger = setup_logger()
    
    # Entsprechenden Bot starten
    if args.telegram:
        setup_telegram_bot(args, logger)
    elif args.whatsapp:
        setup_whatsapp_bot(args, logger)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBot-Dienst wurde beendet.")
        sys.exit(0) 