# sources - Ressourcen und Assets

Dieses Verzeichnis enthält verschiedene Ressourcen und Assets, die vom CV2Profile-Parser verwendet werden, insbesondere Bilder und Vorlagen.

## Enthaltene Dateien

- **galdoralogo.png**: Firmenlogo für PDF-Dokumente
  - Wird in den generierten Profilen verwendet
  - Erscheint typischerweise in der Kopfzeile oder an anderen prominenten Stellen in den Dokumenten

- **cv2profile-loho.png**: Anwendungslogo
  - Logo der CV2Profile-Anwendung
  - Wird in der Benutzeroberfläche und möglicherweise auch in generierten Dokumenten verwendet

- **Profilvorlage Seite 1.png** und **Profilvorlage Seite 2.png**: Designvorlagen
  - Visuelle Vorlagen für das Design der generierten Profile
  - Dienen als Referenz für das Layout und Design der PDF- und DOCX-Ausgaben
  - Zeigen das gewünschte Erscheinungsbild der ersten und zweiten Seite der Profile

## Verwendung

Die Ressourcen in diesem Verzeichnis werden hauptsächlich von folgenden Komponenten verwendet:

- Die Template-Generierung (`src/templates/template_generator.py`) verwendet die Logos und möglicherweise auch die Designvorlagen als Referenz.
- Die Benutzeroberfläche verwendet das Anwendungslogo für die visuelle Identität.
- Die Bild-Utilities (`src/utils/image_utils.py`) kopieren diese Bilder in das `static/images/`-Verzeichnis für die HTTPS-Kompatibilität.

## Hinweis

Diese Dateien werden in der Regel nicht direkt im Code geändert, sondern durch neue Versionen ersetzt, wenn ein Redesign oder eine Aktualisierung erforderlich ist. Die Pfade zu diesen Dateien werden jedoch im Code referenziert, daher sollten die Dateinamen bei Änderungen beibehalten oder die entsprechenden Referenzen im Code aktualisiert werden. 