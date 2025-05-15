#!/bin/bash

# CV2Profile Starter-Skript

# Aktiviere die virtuelle Umgebung, falls sie existiert
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Stelle sicher, dass das static/images Verzeichnis existiert
mkdir -p static/images

# Kopiere Bilder aus dem sources-Verzeichnis in das static/images Verzeichnis
if [ -d "sources" ]; then
    cp -f sources/*.png static/images/ 2>/dev/null || true
    cp -f sources/*.jpg static/images/ 2>/dev/null || true
    cp -f sources/*.jpeg static/images/ 2>/dev/null || true
    cp -f sources/*.gif static/images/ 2>/dev/null || true
    echo "Bilder in static/images kopiert für HTTPS-Kompatibilität"
fi

# Falls nicht gesetzt, Standardwert verwenden
if [ -z "$CV2PROFILE_ENTRY_POINT" ]; then
  export CV2PROFILE_ENTRY_POINT="konverter"
fi

# Python-Pfad festlegen, damit Module korrekt gefunden werden
export PYTHONPATH="$PWD:$PYTHONPATH"

# Starte die Anwendung basierend auf der Umgebungsvariable
if [ "$CV2PROFILE_ENTRY_POINT" = "app" ]; then
  echo "Starte CV2Profile mit app.py als Einstiegspunkt..."
  streamlit run main.py
else
  echo "Starte CV2Profile mit Konverter als Einstiegspunkt..."
  cd $(dirname "$0")  # Wechsle ins Hauptverzeichnis
  streamlit run src/ui/pages/01_Konverter.py
fi

# Deaktiviere die virtuelle Umgebung, falls aktiviert
if [ -n "$VIRTUAL_ENV" ]; then
    deactivate
fi 