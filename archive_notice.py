#!/usr/bin/env python3
"""
CV2Profile - Archiv-Hinweis

Dieses Skript warnt vor der Verwendung alter/archivierter Dateien und verweist auf die korrekte Struktur.
"""

import os
import sys
import textwrap

def print_warning():
    """
    Gibt eine Warnung aus, dass alte Dateien nicht verwendet werden sollten
    """
    warning = """
    ⚠️  ACHTUNG: VERALTETE DATEIVERSIONEN ⚠️
    
    Sie versuchen möglicherweise, auf eine archivierte Version der CV2Profile-Anwendung zuzugreifen.
    
    Die aktuelle Projektstruktur verwendet die Module im src-Verzeichnis:
    
    - src/core/ai_extractor.py         - KI-Extraktionslogik
    - src/core/combined_processor.py   - Kombinierte Prozessorversion
    - src/utils/config.py              - Konfigurationsversion
    - src/core/document_processor.py   - Dokumentenprozessorversion  
    - src/templates/template_generator.py - Template-Generator-Version
    - src/ui/app.py                    - Hauptanwendung
    
    Bitte verwenden Sie die aktuelle Version mit:
    
    python main.py
    
    oder
    
    streamlit run src/ui/app.py
    
    HINWEIS: Alte Versionen im 'archive'-Verzeichnis sind nur für historische Referenzzwecke aufbewahrt
    und nicht mehr mit der aktuellen Struktur kompatibel.
    """
    
    # Formatiere die Warnung für bessere Lesbarkeit
    print("\033[91m" + textwrap.dedent(warning) + "\033[0m")

if __name__ == "__main__":
    print_warning()
    sys.exit(1) 