# Implementierungsplan für CV2Profile

Dieser Plan beschreibt die schrittweise Umsetzung der in progress.md gewünschten Funktionen und enthält konkrete Maßnahmen und Codebeispiele für die Implementierung.

## 1. PDF-Vorschau überall sichtbar machen

### Aktuelles Problem
Die PDF-Vorschau funktioniert nur im lokalen Betrieb (localhost), nicht jedoch in der gehosteten Streamlit-Version aufgrund von HTTPS-Einschränkungen.

### Lösungsansatz
1. **Aktuelle Implementierung analysieren**:
   - In `app.py` wird die Funktion `display_pdf()` verwendet, die einen iframe mit lokaler Dateireferenz erstellt
   - Bei HTTPS sind direkte iframe-Einbindungen lokaler Dateien aus Sicherheitsgründen nicht möglich

2. **Alternative Implementierung**:
   ```python
   def display_pdf_base64(pdf_file):
       """Zeigt ein PDF als Base64-kodierte Einbettung an (funktioniert auch mit HTTPS)"""
       with open(pdf_file, "rb") as f:
           base64_pdf = base64.b64encode(f.read()).decode('utf-8')
       
       # Einbettung über data URI Schema
       pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
       st.markdown(pdf_display, unsafe_allow_html=True)
   ```

3. **Erweiterung für PDF.js Support**:
   ```python
   def display_pdf_pdfjs(pdf_file):
       """Zeigt ein PDF mit PDF.js an (HTTPS-kompatibel)"""
       with open(pdf_file, "rb") as f:
           base64_pdf = base64.b64encode(f.read()).decode('utf-8')
       
       # PDF.js Viewer für bessere Kompatibilität
       html_string = f'''
       <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.11.338/pdf.min.js"></script>
       <script>
           const pdfData = atob('{base64_pdf}');
           const pdfjsLib = window['pdfjs-dist/build/pdf'];
           pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.11.338/pdf.worker.min.js';
           
           const loadingTask = pdfjsLib.getDocument({{data: pdfData}});
           loadingTask.promise.then(pdf => {{
               const container = document.getElementById('pdf-viewer');
               for(let i = 1; i <= pdf.numPages; i++) {{
                   pdf.getPage(i).then(page => {{
                       const scale = 1.5;
                       const viewport = page.getViewport({{scale}});
                       const canvas = document.createElement('canvas');
                       container.appendChild(canvas);
                       const context = canvas.getContext('2d');
                       canvas.height = viewport.height;
                       canvas.width = viewport.width;
                       const renderContext = {{
                           canvasContext: context,
                           viewport: viewport
                       }};
                       page.render(renderContext);
                   }});
               }}
           }});
       </script>
       <div id="pdf-viewer" style="width:100%; height:800px;"></div>
       '''
       st.components.v1.html(html_string, height=800)
   ```

4. **Integration in `app.py`**:
   - Bestehende `display_pdf()`-Funktion durch die neue HTTPS-kompatible Version ersetzen
   - Eine Null-Überprüfung für `st.session_state.preview_pdf` hinzufügen, um Fehler zu vermeiden

### Testplan
1. Lokale Überprüfung der PDF-Anzeige
2. Test in einer HTTPS-Umgebung (z.B. Streamlit Cloud)
3. Test mit verschiedenen Dateitypen und -größen

## 2. Eigene Templates erstellen können

### Lösungsansatz
1. **Template-System erweitern**:
   - Aktualisierung des `template_generator.py`, um benutzerdefinierte Templates zu unterstützen
   - Speicherung der benutzerdefinierten Templates im Benutzerverzeichnis

2. **Template-Editor erstellen**:
   ```python
   def template_editor():
       """Benutzeroberfläche zum Erstellen und Bearbeiten von Templates"""
       st.subheader("Template-Editor")
       
       # Template-Name
       template_name = st.text_input("Template-Name", "Mein_Template")
       
       # Grundlegende Eigenschaften
       col1, col2 = st.columns(2)
       with col1:
           primary_color = st.color_picker("Primärfarbe", "#4A6EE0")
           font = st.selectbox("Hauptschriftart", ["Helvetica", "Times", "Courier", "Arial", "Verdana"])
       with col2:
           secondary_color = st.color_picker("Sekundärfarbe", "#7B1FA2")
           title_font = st.selectbox("Titelschriftart", ["Helvetica-Bold", "Times-Bold", "Arial-Bold"])
       
       # Layout-Optionen
       layout_type = st.radio("Layout-Typ", ["Einspaltig", "Zweispaltig", "Dreispaltig"])
       
       # Vorschau und Speichern
       if st.button("Vorschau generieren"):
           # Hier den Code zur Generierung einer Vorschau einfügen
           st.success("Vorschau generiert!")
       
       if st.button("Template speichern"):
           # Template-Daten sammeln
           template_data = {
               "name": template_name,
               "primary_color": primary_color,
               "secondary_color": secondary_color,
               "font": font,
               "title_font": title_font,
               "layout_type": layout_type
           }
           
           # In eine JSON-Datei speichern
           save_custom_template(template_data)
           st.success(f"Template '{template_name}' erfolgreich gespeichert!")
   ```

3. **Integration in die Benutzeroberfläche**:
   - Neue Seite in der Streamlit-App erstellen (z.B. `02_🧩_Templates.py`)
   - Link zur Template-Verwaltung in der Seitenleiste hinzufügen

4. **Backend-Funktionen**:
   ```python
   def save_custom_template(template_data):
       """Speichert ein benutzerdefiniertes Template"""
       # Verzeichnis für benutzerdefinierte Templates
       custom_templates_dir = os.path.join(config.CONFIG_DIR, "templates")
       os.makedirs(custom_templates_dir, exist_ok=True)
       
       # Template-Datei erstellen
       template_file = os.path.join(custom_templates_dir, f"{template_data['name']}.json")
       with open(template_file, "w") as f:
           json.dump(template_data, f, indent=4)
       
       return template_file
   
   def load_custom_templates():
       """Lädt alle benutzerdefinierten Templates"""
       custom_templates_dir = os.path.join(config.CONFIG_DIR, "templates")
       if not os.path.exists(custom_templates_dir):
           return []
       
       templates = []
       for file in os.listdir(custom_templates_dir):
           if file.endswith(".json"):
               with open(os.path.join(custom_templates_dir, file), "r") as f:
                   templates.append(json.load(f))
       
       return templates
   ```

### Testplan
1. Testen der Erstellung eigener Templates
2. Überprüfen, ob Templates korrekt gespeichert werden
3. Testen der Verwendung benutzerdefinierter Templates bei der Profilerstellung

## 3. Standard-Templates bearbeiten können

### Lösungsansatz
1. **Editor für Standard-Templates entwickeln**:
   - Bearbeitungsmöglichkeiten für bestehende Vorlagen hinzufügen
   - Einstellungen für Farben, Schriftarten und Layout

2. **GUI für Template-Anpassungen**:
   ```python
   def edit_standard_template():
       """Benutzeroberfläche zum Bearbeiten von Standard-Templates"""
       templates = ["professional", "classic", "modern", "minimalist"]
       selected_template = st.selectbox("Template auswählen", templates)
       
       # Template-Daten laden
       template_data = load_template_data(selected_template)
       
       st.subheader(f"Template '{template_data['name']}' bearbeiten")
       
       # Tabs für verschiedene Anpassungskategorien
       tab1, tab2, tab3 = st.tabs(["Farben & Schriften", "Layout", "Elemente"])
       
       with tab1:
           # Farben und Schriften bearbeiten
           template_data["primary_color"] = st.color_picker("Primärfarbe", template_data.get("primary_color", "#4A6EE0"))
           template_data["text_color"] = st.color_picker("Textfarbe", template_data.get("text_color", "#333333"))
           template_data["font"] = st.selectbox("Schriftart", ["Helvetica", "Times", "Arial"], 
                                               index=["Helvetica", "Times", "Arial"].index(template_data.get("font", "Helvetica")))
       
       with tab2:
           # Layout-Einstellungen
           template_data["margin"] = st.slider("Seitenrand (mm)", 5, 30, template_data.get("margin", 15))
           template_data["column_ratio"] = st.slider("Spaltenverhältnis (%)", 10, 50, template_data.get("column_ratio", 30))
       
       with tab3:
           # Element-Optionen
           template_data["show_logo"] = st.checkbox("Logo anzeigen", template_data.get("show_logo", True))
           template_data["show_contact"] = st.checkbox("Kontaktdaten anzeigen", template_data.get("show_contact", True))
       
       # Template speichern
       if st.button("Änderungen speichern"):
           save_template_changes(selected_template, template_data)
           st.success(f"Änderungen an Template '{selected_template}' erfolgreich gespeichert!")
   ```

3. **Implementierung der Backend-Funktionen**:
   ```python
   def load_template_data(template_name):
       """Lädt die Daten eines bestehenden Templates"""
       # Standardmäßig haben wir einige Voreinstellungen
       standard_templates = {
           "professional": {
               "name": "Professionell",
               "primary_color": "#1973B8",
               "text_color": "#333333",
               "font": "Helvetica",
               "margin": 15,
               "column_ratio": 30,
               "show_logo": True,
               "show_contact": True
           },
           # Weitere Templates hier...
       }
       
       # Gespeicherte Anpassungen laden
       custom_templates_dir = os.path.join(config.CONFIG_DIR, "template_edits")
       os.makedirs(custom_templates_dir, exist_ok=True)
       
       custom_file = os.path.join(custom_templates_dir, f"{template_name}.json")
       if os.path.exists(custom_file):
           with open(custom_file, "r") as f:
               custom_data = json.load(f)
               return {**standard_templates.get(template_name, {}), **custom_data}
       
       return standard_templates.get(template_name, {})
   
   def save_template_changes(template_name, template_data):
       """Speichert Änderungen an einem Template"""
       custom_templates_dir = os.path.join(config.CONFIG_DIR, "template_edits")
       os.makedirs(custom_templates_dir, exist_ok=True)
       
       custom_file = os.path.join(custom_templates_dir, f"{template_name}.json")
       with open(custom_file, "w") as f:
           json.dump(template_data, f, indent=4)
   ```

### Testplan
1. Bearbeitung verschiedener Aspekte von Standard-Templates
2. Überprüfen, ob Änderungen korrekt gespeichert werden
3. Testen, ob die bearbeiteten Templates korrekt angewendet werden

## 4. Profilbilder hinzufügen

### Lösungsansatz
1. **Erweiterung der Benutzeroberfläche**:
   - Upload-Funktion für Profilbilder hinzufügen
   - Vorschau des Bildes vor dem Einfügen
   - Positionierungsoptionen anbieten

2. **Integration in UI**:
   ```python
   # In der Profilgenerierung (Schritt 2)
   st.subheader("Profilbild")
   
   use_profile_image = st.checkbox("Profilbild hinzufügen")
   
   if use_profile_image:
       uploaded_image = st.file_uploader("Profilbild hochladen", type=["jpg", "jpeg", "png"])
       
       if uploaded_image is not None:
           # Bild anzeigen
           image = Image.open(uploaded_image)
           col1, col2 = st.columns([1, 2])
           
           with col1:
               st.image(image, width=150, caption="Vorschau")
               
           with col2:
               image_position = st.radio("Position", ["Oben links", "Oben rechts", "Unter dem Namen"])
               image_size = st.slider("Größe (%)", 5, 30, 15)
               
           # Bild temporär speichern
           temp_img_path = os.path.join(tempfile.gettempdir(), "profile_image.png")
           image.save(temp_img_path)
           
           # In Session-State speichern
           st.session_state.profile_image = {
               "path": temp_img_path,
               "position": image_position,
               "size": image_size
           }
           
           st.success("Profilbild wurde hochgeladen und wird im Profil verwendet.")
   ```

3. **Aktualisierung des PDF-Generators**:
   ```python
   # In template_generator.py
   def add_profile_image(self, canvas, image_data):
       """Fügt ein Profilbild zum PDF hinzu"""
       if not image_data or "path" not in image_data:
           return
       
       # Bild-Pfad und Einstellungen
       img_path = image_data["path"]
       position = image_data.get("position", "Oben links")
       size_percent = image_data.get("size", 15)
       
       # Bildgröße basierend auf Prozentangabe
       page_width, page_height = A4
       img_width = page_width * (size_percent / 100)
       
       # Bild-Objekt erstellen
       img = Image(img_path, width=img_width)
       
       # Position bestimmen
       if position == "Oben links":
           x = 20 * mm
           y = page_height - 40 * mm
       elif position == "Oben rechts":
           x = page_width - img_width - 20 * mm
           y = page_height - 40 * mm
       else:  # Unter dem Namen
           x = 20 * mm
           y = page_height - 80 * mm
       
       # Bild zum Canvas hinzufügen
       canvas.drawImage(img_path, x, y, width=img_width, preserveAspectRatio=True)
   ```

### Testplan
1. Hochladen verschiedener Bildformate und -größen
2. Testen verschiedener Positionierungsoptionen
3. Überprüfen der Skalierung und Bildqualität im generierten PDF

## 5. Login-/Registrierungsbereich einbauen

### Lösungsansatz
1. **Benutzerverwaltungssystem entwickeln**:
   - Einfache lokale Benutzerverwaltung mit Streamlit-Authenticator
   - Speicherung der Benutzerkonten im Benutzerverzeichnis

2. **Installation der benötigten Bibliothek**:
   ```bash
   pip install streamlit-authenticator
   ```

3. **Implementierung des Login-Systems**:
   ```python
   # In einer neuen Datei auth.py
   import streamlit as st
   import streamlit_authenticator as stauth
   import yaml
   from yaml.loader import SafeLoader
   import os
   import bcrypt
   from pathlib import Path
   
   # Verzeichnis für Benutzerkonten
   USERS_DIR = Path.home() / ".cv2profile" / "users"
   USERS_FILE = USERS_DIR / "users.yaml"
   
   def ensure_users_dir():
       """Stellt sicher, dass das Benutzerverzeichnis existiert"""
       if not USERS_DIR.exists():
           USERS_DIR.mkdir(parents=True, exist_ok=True)
       
       # Erstelle eine Standard-Benutzerdatei, wenn sie nicht existiert
       if not USERS_FILE.exists():
           default_users = {
               'credentials': {
                   'usernames': {
                       'admin': {
                           'name': 'Administrator',
                           'password': stauth.Hasher(['admin']).generate()[0],
                           'email': 'admin@example.com'
                       }
                   }
               }
           }
           with open(USERS_FILE, 'w') as file:
               yaml.dump(default_users, file, default_flow_style=False)
   
   def get_authenticator():
       """Erstellt und konfiguriert den Authenticator"""
       ensure_users_dir()
       
       with open(USERS_FILE, 'r') as file:
           config = yaml.load(file, Loader=SafeLoader)
       
       authenticator = stauth.Authenticate(
           config['credentials'],
           cookie_name='cv2profile_auth',
           key='cv2profile_auth',
           cookie_expiry_days=30
       )
       
       return authenticator
   
   def create_new_user(username, name, password, email):
       """Erstellt einen neuen Benutzer"""
       ensure_users_dir()
       
       with open(USERS_FILE, 'r') as file:
           config = yaml.load(file, Loader=SafeLoader)
       
       if username in config['credentials']['usernames']:
           return False, "Benutzername existiert bereits"
       
       # Neuen Benutzer hinzufügen
       hashed_password = stauth.Hasher([password]).generate()[0]
       config['credentials']['usernames'][username] = {
           'name': name,
           'password': hashed_password,
           'email': email
       }
       
       # Konfiguration speichern
       with open(USERS_FILE, 'w') as file:
           yaml.dump(config, file, default_flow_style=False)
       
       return True, "Benutzer erfolgreich erstellt"
   ```

4. **Integration in die Hauptapp**:
   ```python
   # In app.py am Anfang
   from src.utils import auth
   
   # Initialisiere den Authenticator
   authenticator = auth.get_authenticator()
   
   # Platziere die Login-Widget in der Sidebar
   with st.sidebar:
       st.title("CV2Profile")
       
       # Login-Formular
       name, authentication_status, username = authenticator.login('Login', 'main')
       
       if authentication_status == False:
           st.error('Benutzername/Passwort ist falsch')
       
       if authentication_status == None:
           st.warning('Bitte geben Sie Ihren Benutzernamen und Passwort ein')
       
       # Registrierungslink anzeigen
       if authentication_status != True:
           st.markdown("[Neues Konto erstellen](/Registrieren)")
   
   # Hauptinhalt nur für angemeldete Benutzer anzeigen
   if authentication_status:
       # Benutzermenü in der Sidebar anzeigen
       with st.sidebar:
           authenticator.logout('Abmelden', 'sidebar')
           st.write(f'Willkommen *{name}*')
       
       # HIER DEN BESTEHENDEN APP-CODE EINFÜGEN
   ```

5. **Registrierungsseite erstellen**:
   ```python
   # In pages/03_Registrieren.py
   import streamlit as st
   from src.utils import auth
   
   st.title("Registrierung")
   
   with st.form("registration_form"):
       st.subheader("Neues Konto erstellen")
       
       new_username = st.text_input("Benutzername")
       new_name = st.text_input("Vollständiger Name")
       new_email = st.text_input("E-Mail")
       new_password = st.text_input("Passwort", type="password")
       new_password_repeat = st.text_input("Passwort wiederholen", type="password")
       
       submit = st.form_submit_button("Registrieren")
       
       if submit:
           if not new_username or not new_name or not new_email or not new_password:
               st.error("Bitte füllen Sie alle Felder aus.")
           elif new_password != new_password_repeat:
               st.error("Die Passwörter stimmen nicht überein.")
           else:
               success, message = auth.create_new_user(
                   new_username, new_name, new_password, new_email
               )
               
               if success:
                   st.success(message)
                   st.info("Sie können sich jetzt anmelden.")
               else:
                   st.error(message)
   ```

6. **Datenspeicherung pro Benutzer**:
   ```python
   # Funktion zum Speichern von Benutzerdaten in auth.py
   def get_user_data_dir(username):
       """Gibt das Verzeichnis für benutzerspezifische Daten zurück"""
       user_dir = USERS_DIR / username
       user_dir.mkdir(parents=True, exist_ok=True)
       return user_dir
   
   def save_user_data(username, data_key, data):
       """Speichert benutzerspezifische Daten"""
       user_dir = get_user_data_dir(username)
       data_file = user_dir / f"{data_key}.json"
       
       with open(data_file, 'w') as file:
           json.dump(data, file, indent=4)
   
   def load_user_data(username, data_key, default=None):
       """Lädt benutzerspezifische Daten"""
       user_dir = get_user_data_dir(username)
       data_file = user_dir / f"{data_key}.json"
       
       if data_file.exists():
           with open(data_file, 'r') as file:
               return json.load(file)
       return default
   ```

### Testplan
1. Registrierung neuer Benutzer
2. Login mit verschiedenen Benutzerkonten
3. Test der Datenspeicherung pro Benutzer
4. Überprüfung der Passwortänderungsfunktion

## Zusammenfassung

Die beschriebenen Implementierungsschritte ermöglichen die Umsetzung aller gewünschten Funktionen. Die Implementierung erfolgt modular, sodass jede Funktion einzeln entwickelt und getestet werden kann. Die wichtigsten Dateien, die angepasst werden müssen, sind:

1. **PDF-Vorschau verbessern**:
   - `src/ui/app.py` (Funktion `display_pdf()`)

2. **Template-Verwaltung**:
   - Neue Datei: `src/ui/pages/02_🧩_Templates.py`
   - Erweiterung: `src/templates/template_generator.py`
   - Erweiterung: `src/utils/config.py`

3. **Profilbild-Integration**:
   - Erweiterung: `src/ui/app.py`
   - Erweiterung: `src/templates/template_generator.py`

4. **Login-System**:
   - Neue Datei: `src/utils/auth.py`
   - Neue Datei: `src/ui/pages/03_Registrieren.py`
   - Anpassung: `src/ui/app.py`

Die Implementierung erfolgt schrittweise und mit Fokus auf intuitive Benutzerführung und robuste Funktionalität. 