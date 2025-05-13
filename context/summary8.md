# Zusammenfassung: HTTPS-Kompatibilität für Bilder

## Überblick

In dieser Aktualisierung wurde ein Problem behoben, das auftrat, wenn die Anwendung auf einem HTTPS-Server ausgeführt wurde. Bilder, die zuvor nur lokal funktioniert haben, werden jetzt auch auf HTTPS-Servern korrekt angezeigt, indem sie in einem speziellen `static/images`-Verzeichnis abgelegt werden.

## Implementierte Änderungen

### 1. Neue Verzeichnisstruktur

Es wurde ein neues `static/images`-Verzeichnis eingerichtet, das als zentraler Speicherort für alle Bilder dient, die sowohl lokal als auch über HTTPS zugänglich sein müssen. Dieses Verzeichnis wird nun automatisch erstellt und mit Bildern aus dem `sources`-Verzeichnis gefüllt.

### 2. Neue Hilfsfunktionen für die Bildverwaltung

Eine neue Datei `src/utils/image_utils.py` wurde erstellt, die zwei Hauptfunktionen bereitstellt:

- `get_image_path(image_name, use_static=False)`: Gibt den Pfad zu einem Bild zurück und kopiert es bei Bedarf in das static-Verzeichnis
- `ensure_images_in_static()`: Stellt sicher, dass alle Bilder aus dem `sources`-Verzeichnis in das `static/images`-Verzeichnis kopiert werden

### 3. Integration der Bildfunktionen

Die neuen Bildfunktionen wurden in folgende Dateien integriert:

- `src/templates/template_generator.py`: Verwendet die Funktionen, um Bilder in generierten PDFs korrekt zu finden
- `src/ui/app.py`: Initialisiert die Bild-Utilities beim Anwendungsstart und verwendet sie für das App-Logo

### 4. Automatische Initialisierung beim Start

- `run.sh`: Das Startskript kopiert nun automatisch alle relevanten Bilddateien in das static-Verzeichnis
- `src/ui/app.py`: Beim Starten der Anwendung wird `ensure_images_in_static()` aufgerufen

## Technische Details

### 1. Bildpfad-Management

```python
def get_image_path(image_name, use_static=False):
    """
    Get the path to an image, with an option to use the static directory for HTTP/HTTPS serving
    
    Args:
        image_name: The name of the image file (e.g., 'galdoralogo.png')
        use_static: If True, use the static/images path for HTTPS compatibility
        
    Returns:
        str: The path to the image file
    """
    # Get the project root directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    
    # Define paths
    sources_dir = os.path.join(project_root, 'sources')
    static_dir = os.path.join(project_root, 'static', 'images')
    
    # Ensure static/images directory exists
    if not os.path.exists(static_dir):
        os.makedirs(static_dir, exist_ok=True)
    
    # Source file path
    source_path = os.path.join(sources_dir, image_name)
    
    # If using static path for HTTPS
    if use_static:
        static_path = os.path.join(static_dir, image_name)
        
        # Copy the file to static directory if it doesn't exist there
        if os.path.exists(source_path) and not os.path.exists(static_path):
            shutil.copy2(source_path, static_path)
            
        return static_path
    
    # Otherwise return the original path
    return source_path
```

### 2. Automatische Bildkopie in statisches Verzeichnis

```python
def ensure_images_in_static():
    """
    Copy all images from sources directory to static/images directory 
    to ensure they are available for HTTPS serving
    """
    # Get the project root directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    
    # Define paths
    sources_dir = os.path.join(project_root, 'sources')
    static_dir = os.path.join(project_root, 'static', 'images')
    
    # Ensure static/images directory exists
    if not os.path.exists(static_dir):
        os.makedirs(static_dir, exist_ok=True)
    
    # Copy all image files from sources to static/images
    for file in os.listdir(sources_dir):
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            source_file = os.path.join(sources_dir, file)
            target_file = os.path.join(static_dir, file)
            
            # Copy file if it doesn't exist or is newer
            if not os.path.exists(target_file) or os.path.getmtime(source_file) > os.path.getmtime(target_file):
                shutil.copy2(source_file, target_file)
                
    return static_dir
```

### 3. Aktualisierung des Startskripts (run.sh)

```bash
# Stelle sicher, dass das static/images Verzeichnis existiert
mkdir -p static/images

# Kopiere Bilder aus dem sources-Verzeichnis in das static/images Verzeichnis
if [ -d "sources" ]; then
    cp -f sources/*.png static/images/ 2>/dev/null || true
    cp -f sources/*.jpg static/images/ 2>/dev/null || true
    cp -f sources/*.jpeg static/images/ 2>/dev/null || true
    cp -f sources/*.gif static/images/ 2>/dev/null || true
    echo "Bilder in static/images kopiert für HTTPS-Kompatibilität"
fi
```

## Vorteile der Implementierung

1. **Cross-Platform-Kompatibilität**: Bilder funktionieren jetzt sowohl lokal als auch auf HTTPS-Servern
2. **Automatische Verwaltung**: Kein manuelles Kopieren von Bildern erforderlich
3. **Verbesserte Wartbarkeit**: Zentralisierte Bildverwaltung durch dedizierte Funktionen
4. **Aktualität gewährleistet**: Automatisches Update von Bildern, wenn Quelldateien aktualisiert werden

## Zusammenfassung

Diese Implementierung löst das Problem, dass Bilder auf einem HTTPS-Server nicht angezeigt wurden, indem alle Bilder automatisch in ein `static/images`-Verzeichnis kopiert werden. Die Anwendung wurde mit neuen Hilfsfunktionen erweitert, die sowohl für den lokalen Betrieb als auch für die Ausführung auf HTTPS-Servern optimiert sind. Durch diese Änderungen ist die Anwendung nun vollständig für den Einsatz im Web vorbereitet und bietet eine konsistente Benutzererfahrung unabhängig von der Bereitstellungsumgebung. 