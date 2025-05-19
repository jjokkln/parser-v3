#!/bin/bash
# bot_run.sh - Skript zum Starten des Bot-Dienstes

# Umgebung aktivieren, falls vorhanden
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "Virtuelle Umgebung aktiviert."
elif [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "Virtuelle Umgebung aktiviert."
else
    echo "Keine virtuelle Umgebung gefunden. Führe mit System-Python aus."
fi

# Standardwerte
BOT_TYPE="telegram"  # telegram oder whatsapp

# Argumente verarbeiten
while [[ $# -gt 0 ]]; do
    case $1 in
        --telegram)
            BOT_TYPE="telegram"
            shift
            ;;
        --whatsapp)
            BOT_TYPE="whatsapp"
            shift
            ;;
        --token=*)
            TOKEN="${1#*=}"
            shift
            ;;
        --save-token)
            SAVE_TOKEN="--save-token"
            shift
            ;;
        --account-sid=*)
            ACCOUNT_SID="${1#*=}"
            shift
            ;;
        --auth-token=*)
            AUTH_TOKEN="${1#*=}"
            shift
            ;;
        --phone-number=*)
            PHONE_NUMBER="${1#*=}"
            shift
            ;;
        --save-credentials)
            SAVE_CREDENTIALS="--save-credentials"
            shift
            ;;
        --port=*)
            PORT="${1#*=}"
            shift
            ;;
        --debug)
            DEBUG="--debug"
            shift
            ;;
        --help)
            echo "Verwendung: $0 [Optionen]"
            echo ""
            echo "Optionen:"
            echo "  --telegram                 Telegram-Bot starten (Standard)"
            echo "  --whatsapp                 WhatsApp-Bot starten"
            echo ""
            echo "Telegram-Optionen:"
            echo "  --token=TOKEN              Telegram-Bot-Token"
            echo "  --save-token               Token speichern für zukünftige Verwendung"
            echo ""
            echo "WhatsApp-Optionen:"
            echo "  --account-sid=SID          Twilio Account SID"
            echo "  --auth-token=TOKEN         Twilio Auth Token"
            echo "  --phone-number=NUMBER      Twilio-Telefonnummer"
            echo "  --save-credentials         Credentials für zukünftige Verwendung speichern"
            echo "  --port=PORT                Port für den Webhook-Server (Standard: 5000)"
            echo "  --debug                    Debug-Modus aktivieren"
            echo ""
            echo "Beispiel:"
            echo "  $0 --telegram --token=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11 --save-token"
            echo "  $0 --whatsapp --account-sid=AC1234 --auth-token=abcd1234 --phone-number=+491234567890 --save-credentials"
            exit 0
            ;;
        *)
            echo "Unbekannte Option: $1"
            echo "Verwende --help für eine Liste der verfügbaren Optionen."
            exit 1
            ;;
    esac
done

# Bot-Dienst starten
if [ "$BOT_TYPE" = "telegram" ]; then
    echo "Starte Telegram-Bot..."
    python src/bot_service.py --telegram ${TOKEN:+--token "$TOKEN"} ${SAVE_TOKEN}
elif [ "$BOT_TYPE" = "whatsapp" ]; then
    echo "Starte WhatsApp-Bot..."
    python src/bot_service.py --whatsapp \
        ${ACCOUNT_SID:+--account-sid "$ACCOUNT_SID"} \
        ${AUTH_TOKEN:+--auth-token "$AUTH_TOKEN"} \
        ${PHONE_NUMBER:+--phone-number "$PHONE_NUMBER"} \
        ${SAVE_CREDENTIALS} \
        ${PORT:+--port "$PORT"} \
        ${DEBUG}
fi 