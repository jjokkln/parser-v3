# templates - Profilgenerierung

Dieses Verzeichnis enthält die Funktionalität für die Generierung von strukturierten und gut gestalteten Profilen auf Basis der extrahierten Daten.

## Enthaltene Dateien

- **template_generator.py**: Erstellt ansprechende PDF-Profile
  - Generiert professionell gestaltete PDF-Dokumente
  - Verwendet ReportLab für die PDF-Erstellung
  - Unterstützt verschiedene Vorlagen (Templates):
    - Klassisch (Standard)
    - Modern (zweispaltig, weinrot/weiß)
    - Professionell
    - Minimalistisch
  - Erstellt ein einheitliches Layout für alle Profile
  - Unterstützt sowohl PDF- als auch DOCX-Export

## Funktionalität

Die Template-Generierung umfasst folgende Hauptfunktionen:

- Integration von Firmen- und Anwendungslogos
- Formatierung und Darstellung persönlicher Daten
- Strukturierte Darstellung von Berufserfahrungen, Ausbildung und Weiterbildungen
- Unterstützung für Profilbilder in bestimmten Templates
- Automatische Seitenumbruchverwaltung
- Einheitliche Fußzeilen auf allen Seiten
- Anpassung für verschiedene Anzeigeformate und -größen

## Verwendung

Die Template-Generierung wird hauptsächlich nach der Datenextraktion und -bearbeitung innerhalb der Hauptanwendung (`main.py` oder `src/ui/app.py`) verwendet, um die finalen Profile zu erstellen, die dem Benutzer zum Download angeboten werden. 