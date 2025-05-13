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

# Führe die Anwendung aus
python main.py

# Deaktiviere die virtuelle Umgebung, falls aktiviert
if [ -n "$VIRTUAL_ENV" ]; then
    deactivate
fi 