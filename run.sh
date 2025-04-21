#!/bin/bash

# CV2Profile Starter-Skript

# Aktiviere die virtuelle Umgebung, falls sie existiert
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Führe die Anwendung aus
python main.py

# Deaktiviere die virtuelle Umgebung, falls aktiviert
if [ -n "$VIRTUAL_ENV" ]; then
    deactivate
fi 