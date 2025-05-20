# Design-Vorlagen für CV2Profile

Dieser Ordner enthält verschiedene Design-Vorlagen für das CV2Profile-System. Jede Vorlage hat ihren eigenen Unterordner mit spezifischen Assets und Konfigurationen.

## Verfügbare Designs

- **classic/** - Klassisches Design mit traditionellem Layout
- **modern/** - Modernes zweispaltiges Design in Weinrot/Weiß
- **professional/** - Professionelles Business-Design
- **minimalist/** - Minimalistisches Design mit klarem, reduziertem Layout

## Hinzufügen neuer Designs

Um ein neues Design hinzuzufügen, folgen Sie diesen Schritten:

1. Erstellen Sie einen neuen Ordner im `designs`-Verzeichnis mit dem Namen Ihres Designs (z.B. `elegant/`)
2. Fügen Sie alle benötigten Assets (Bilder, Hintergründe, Schriften) in den Ordner ein
3. Erstellen Sie eine `config.json`-Datei im Design-Ordner mit folgenden Einstellungen:
   ```json
   {
     "name": "Elegant",
     "description": "Elegantes Design mit goldenen Akzenten",
     "primary_color": "#D4AF37",
     "secondary_color": "#1E1E1E",
     "font": "Palatino",
     "version": "1.0"
   }
   ```
4. Optional: Erstellen Sie eine `preview.png`-Datei im Design-Ordner als Vorschaubild
5. Passen Sie den `template_generator.py` an, um Ihr neues Design zu unterstützen:
   - Fügen Sie Ihr Design zur Liste der verfügbaren Templates hinzu
   - Implementieren Sie die Renderlogik für Ihr Design in der `_create_document_elements`-Methode

## Designrichtlinien

Alle Designs sollten:
- A4-Format unterstützen
- Konsistente Schriftarten und -größen verwenden
- Responsive Layouts haben, die mit unterschiedlichen Inhaltsmengen umgehen können
- Eine klare visuelle Hierarchie bieten
- Mit PDF- und DOCX-Export kompatibel sein

## Testen

Testen Sie neue Designs mit verschiedenen Datenmengen, um sicherzustellen, dass sie mit kurzen und langen Lebensläufen funktionieren. Insbesondere sollten Sie prüfen:
- Umgang mit langen Listen von Berufserfahrungen
- Korrekte Seitenumbrüche
- Darstellung von Profilbildern
- Konsistente Darstellung in verschiedenen Ausgabeformaten 