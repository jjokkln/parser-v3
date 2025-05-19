#!/usr/bin/env python3
"""
CV2Profile - Haupteinstiegspunkt

Dieses Skript startet die CV2Profile-Anwendung.
Die Anwendung unterstützt jetzt Multipage mit der Hauptseite und Einstellungsseite.
"""

import os
import sys
import subprocess

def main():
    """
    Hauptfunktion zum Starten der CV2Profile-Anwendung
    """
    # Den src-Ordner zum Pfad hinzufügen
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    
    try:
        # Streamlit mit der UI-App starten
        # Die Hauptseite ist src/ui/app.py, zusätzliche Seiten werden aus dem pages/ Ordner geladen
        subprocess.run(["streamlit", "run", "src/ui/app.py"], check=True)
    except KeyboardInterrupt:
        print("\nAnwendung wurde beendet.")
    except Exception as e:
        print(f"Fehler beim Starten der Anwendung: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 