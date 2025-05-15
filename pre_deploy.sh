#!/bin/bash

# Dieses Skript bereitet das Repository für das Deployment vor, 
# indem es den Konverter als Haupteinstiegspunkt konfiguriert

echo "=== CV2Profile Deployment-Vorbereitung ==="
echo "Konfiguriere Konverter als Haupteinstiegspunkt..."

# Backup der ursprünglichen app.py erstellen
if [ -f "src/ui/app.py" ]; then
  cp src/ui/app.py src/ui/app.py.bak
  echo "✓ Backup von src/ui/app.py erstellt"
fi

# Konverter als Haupteinstiegspunkt verwenden
cp src/ui/pages/01_Konverter.py src/ui/app.py
echo "✓ Konverter nach src/ui/app.py kopiert"

# Streamlit Cloud benötigt main.py, daher auch hier kopieren
if [ -f "main.py" ]; then
  cp main.py main.py.bak
  echo "✓ Backup von main.py erstellt"
fi

cp src/ui/pages/01_Konverter.py main.py
echo "✓ Konverter nach main.py kopiert"

echo "Die Konverter-Seite wurde erfolgreich als Haupteinstiegspunkt konfiguriert."
echo "=== Deployment-Vorbereitung abgeschlossen ===" 