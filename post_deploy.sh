#!/bin/bash

# Dieses Skript stellt nach dem Deployment die Originaldateien wieder her
# Es wird nur in der Entwicklungsumgebung ausgeführt, nicht in Produktion

# Prüfen, ob wir in der Entwicklungsumgebung sind
if [ "$ENVIRONMENT" = "development" ]; then
  echo "=== CV2Profile Entwicklungs-Wiederherstellung ==="
  
  # Original app.py wiederherstellen, falls Backup existiert
  if [ -f "src/ui/app.py.bak" ]; then
    cp src/ui/app.py.bak src/ui/app.py
    rm src/ui/app.py.bak
    echo "✓ src/ui/app.py wiederhergestellt"
  fi
  
  # Original main.py wiederherstellen, falls Backup existiert
  if [ -f "main.py.bak" ]; then
    cp main.py.bak main.py
    rm main.py.bak
    echo "✓ main.py wiederhergestellt"
  fi
  
  echo "Originaldateien wurden wiederhergestellt."
  echo "=== Wiederherstellung abgeschlossen ==="
else
  echo "In Produktionsumgebung: Keine Wiederherstellung erforderlich."
fi 