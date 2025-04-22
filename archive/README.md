# Archiv für CV2Profile

Dieses Verzeichnis enthält archivierte Dateien und Versionen des CV2Profile-Projekts.

## WICHTIGER HINWEIS

Diese Dateien werden NUR für historische Referenzzwecke aufbewahrt und sollten NICHT direkt verwendet werden. Sie sind nicht mit der aktuellen Projektstruktur kompatibel, da sie auf alte Pfade und möglicherweise veraltete API-Aufrufe verweisen.

## Archivinhalt

### app_versions/
Dieses Verzeichnis enthält ältere Versionen der Hauptanwendung und UI-Fixes:

- `app_original.py` - Die ursprüngliche App-Version
- `app_new.py` - Eine neuere App-Version
- `app.py.bak` - Ein Backup der App
- `app_ui_fixed.py` - Version mit UI-Fixes
- `app_ui_fixed_new.py` - Neuere Version mit UI-Fixes
- `fix_app_ui.py` - UI-Fix-Skript
- `fix_app_ui_improved.py` - Verbessertes UI-Fix-Skript

### old_files/
Dieses Verzeichnis enthält alte Versionen der Core-Dateien aus dem Hauptverzeichnis:

- `ai_extractor.py` - Alte KI-Extraktionslogik
- `combined_processor.py` - Alte kombinierte Prozessorversion
- `config.py` - Alte Konfigurationsversion
- `document_processor.py` - Alte Dokumentenprozessorversion
- `template_generator.py` - Alte Template-Generator-Version
- `app.py` - Alte Hauptanwendung

## Import-Probleme

Die archivierten Dateien verwenden absolute Imports direkt aus dem Hauptverzeichnis, z.B.:

```python
from document_processor import DocumentProcessor
from ai_extractor import AIExtractor
from combined_processor import CombinedProcessor
from template_generator import ProfileGenerator
import config
```

Die aktuelle Codebase verwendet hingegen die strukturierten Imports aus den entsprechenden Paketen:

```python
from src.core.document_processor import DocumentProcessor
from src.core.ai_extractor import AIExtractor
from src.core.combined_processor import CombinedProcessor
from src.templates.template_generator import ProfileGenerator
import src.utils.config as config
```

Falls Sie Code aus den archivierten Dateien wiederverwenden möchten, passen Sie die Import-Pfade entsprechend an die aktuelle Projektstruktur an. 