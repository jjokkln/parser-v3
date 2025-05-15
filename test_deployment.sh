#!/bin/bash

# Dieses Skript testet die Deployment-Konfiguration lokal

echo "=== CV2Profile Deployment-Test ==="
echo "Teste die Deployment-Skripte in der lokalen Umgebung..."

# 1. Ausführen des Pre-Deployment-Skripts
echo -e "\n>> Pre-Deployment-Skript ausführen"
chmod +x pre_deploy.sh
./pre_deploy.sh

# 2. Prüfen, ob die Dateien kopiert wurden
echo -e "\n>> Prüfe, ob die Dateien korrekt kopiert wurden"
if [ -f "src/ui/app.py.bak" ]; then
  echo "✓ Backup von app.py wurde erstellt"
fi

if grep -q "01_Konverter.py" "src/ui/app.py"; then
  echo "✓ app.py enthält jetzt den Inhalt von 01_Konverter.py"
else
  echo "✗ app.py wurde nicht korrekt aktualisiert"
fi

if grep -q "01_Konverter.py" "main.py"; then
  echo "✓ main.py enthält jetzt den Inhalt von 01_Konverter.py"
else
  echo "✗ main.py wurde nicht korrekt aktualisiert"
fi

# 3. Ausführen des Post-Deployment-Skripts
echo -e "\n>> Post-Deployment-Skript ausführen"
export ENVIRONMENT="development"
chmod +x post_deploy.sh
./post_deploy.sh

# 4. Prüfen, ob die Dateien wiederhergestellt wurden
echo -e "\n>> Prüfe, ob die Dateien wiederhergestellt wurden"
if [ ! -f "src/ui/app.py.bak" ]; then
  echo "✓ Backup von app.py wurde entfernt"
else
  echo "✗ Backup von app.py wurde nicht entfernt"
fi

if [ ! -f "main.py.bak" ]; then
  echo "✓ Backup von main.py wurde entfernt"
else
  echo "✗ Backup von main.py wurde nicht entfernt"
fi

echo -e "\n>> Starte Test des run.sh-Skripts mit verschiedenen Umgebungsvariablen"
echo "1. Test mit CV2PROFILE_ENTRY_POINT=konverter (Standard)"
export CV2PROFILE_ENTRY_POINT="konverter"
echo "./run.sh würde den Konverter als Einstiegspunkt verwenden"

echo -e "\n2. Test mit CV2PROFILE_ENTRY_POINT=app"
export CV2PROFILE_ENTRY_POINT="app"
echo "./run.sh würde app.py als Einstiegspunkt verwenden"

echo -e "\n=== Test abgeschlossen ==="
echo "Die Deployment-Konfiguration wurde getestet. Bitte überprüfen Sie die Ausgabe auf Fehler."
echo "Um die Anwendung zu starten, verwenden Sie das run.sh-Skript." 