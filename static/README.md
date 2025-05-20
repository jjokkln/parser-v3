# static - Statische Dateien für HTTPS-Kompatibilität

Dieses Verzeichnis enthält statische Dateien, die für die HTTPS-Kompatibilität der Anwendung benötigt werden, insbesondere Bilder.

## Struktur

- **images/**: Verzeichnis für Bilder
  - Enthält Kopien der Bilder aus dem `sources/`-Verzeichnis
  - Dient als Speicherort für HTTPS-kompatible Bilddateien
  - Enthält in der Regel die folgenden Dateien:
    - `galdoralogo.png`: Firmenlogo für PDF-Dokumente
    - `cv2profile-loho.png`: Anwendungslogo
    - `Profilvorlage Seite 1.png` und `Profilvorlage Seite 2.png`: Designvorlagen

## Zweck

Der Hauptzweck dieses Verzeichnisses ist es, statische Dateien bereitzustellen, die sowohl in lokalen als auch in HTTPS-Umgebungen (wie Streamlit Cloud) korrekt angezeigt werden können. Das ist wichtig, da bei der Bereitstellung über HTTPS (sichere Verbindung) Ressourcen ebenfalls über HTTPS geladen werden müssen, um gemischten Inhalt zu vermeiden.

## Funktionsweise

Die Anwendung verwendet die Hilfsfunktionen in `src/utils/image_utils.py`, um sicherzustellen, dass alle Bilder automatisch in dieses Verzeichnis kopiert werden. Während der Laufzeit werden Bilder aus diesem Verzeichnis anstelle des ursprünglichen `sources/`-Verzeichnisses geladen, wenn eine HTTPS-Umgebung erkannt wird.

## Hinweise

- Dieses Verzeichnis sollte nicht direkt bearbeitet werden, da sein Inhalt automatisch aus dem `sources/`-Verzeichnis generiert wird.
- Wenn neue Bilder oder andere statische Dateien zur Anwendung hinzugefügt werden, sollten sie im `sources/`-Verzeichnis platziert werden, und die Anwendung wird sie automatisch hierher kopieren.
- Bei Problemen mit der Bildanzeige in HTTPS-Umgebungen sollte überprüft werden, ob die Bilder korrekt in dieses Verzeichnis kopiert wurden. 