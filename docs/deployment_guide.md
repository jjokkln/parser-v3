# CV2Profile Deployment-Anleitung

Diese Anleitung beschreibt, wie die Codebasis von CV2Profile verwaltet und deployed wird, um mit der Redundanz zwischen `app.py` und `01_Konverter.py` umzugehen.

## Hintergrund

Die Anwendung enthält zwei nahezu identische Dateien:
- `src/ui/app.py`: Ursprünglicher Einstiegspunkt 
- `src/ui/pages/01_Konverter.py`: Teil der Seitenstruktur mit gleicher Funktionalität

Um diese Redundanz zu bewältigen, ohne die bestehenden Dateien zu ändern, wurden zwei Lösungsansätze implementiert:

## 1. Entwicklungsumgebung: Umgebungsvariable (Option 4)

Während der Entwicklung kann die Anwendung entweder mit `app.py` oder mit dem `Konverter` als Einstiegspunkt gestartet werden:

```bash
# Starten mit dem Konverter als Einstiegspunkt (Standard)
./run.sh

# ODER

# Starten mit app.py als Einstiegspunkt
export CV2PROFILE_ENTRY_POINT="app"
./run.sh
```

**Wichtig:** Alle Änderungen sollten immer in der `01_Konverter.py` vorgenommen werden, da diese Datei als Quelle der Wahrheit gilt.

## 2. Produktionsumgebung: Automatisches Deployment (Option 5)

Der CI/CD-Prozess (GitHub Actions) verwendet das `pre_deploy.sh`-Skript, um die Anwendung für das Deployment vorzubereiten:

1. Vor dem Deployment wird `01_Konverter.py` nach `app.py` und `main.py` kopiert, um sicherzustellen, dass die Anwendung einen konsistenten Einstiegspunkt hat.
2. Diese Änderungen werden nur für das Deployment vorgenommen und nicht ins Repository zurückgeführt.

Das `post_deploy.sh`-Skript kann verwendet werden, um die ursprünglichen Dateien in der Entwicklungsumgebung wiederherzustellen.

## Richtlinien für Entwickler

1. **Änderungen nur in `01_Konverter.py` vornehmen**. Diese Datei wird bei jedem Deployment als Haupteinstiegspunkt verwendet.

2. **`app.py` nicht direkt bearbeiten**. Diese Datei wird beim Deployment überschrieben.

3. **GitHub Actions Workflow beachten**. Der Workflow in `.github/workflows/streamlit_deploy.yml` übernimmt die automatische Konfiguration für das Deployment.

4. **Lokal testen mit dem bevorzugten Einstiegspunkt**:
   ```bash
   # Für Konverter (empfohlen)
   export CV2PROFILE_ENTRY_POINT="konverter"
   ./run.sh
   
   # Für app.py
   export CV2PROFILE_ENTRY_POINT="app"
   ./run.sh
   ```

## Langfristige Lösung

Langfristig sollte eine Refaktorierung in Betracht gezogen werden, bei der die gemeinsame Funktionalität in eine separate Bibliothek ausgelagert wird. Dies würde die Redundanz vollständig beseitigen.

Bis dahin stellt dieser Ansatz sicher, dass die Anwendung konsistent funktioniert, ohne dass wir in die bestehenden Dateien eingreifen müssen. 