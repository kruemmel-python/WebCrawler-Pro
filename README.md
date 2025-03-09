# Web-Scraping und API-Programm: Umfassende Anleitung

Dieses Programm ist ein vielseitiges Werkzeug zum Extrahieren von Daten aus dem Web und zur Bereitstellung dieser Daten über eine API. Es kombiniert Web-Scraping-Funktionen mit einer robusten API, um das Erfassen, Verarbeiten und Bereitstellen von Informationen zu vereinfachen. Zu den wichtigsten Funktionen gehören:

* **Web-Scraping:** Automatisches Abrufen von Webseiteninhalten mithilfe von Selenium.
* **Datenextraktion:** Extrahieren von Text, Titeln, Metadaten, Überschriften und Schlüsselwörtern.
* **CSS-Selektoren:** Gezielte Extraktion von Daten mithilfe von CSS-Selektoren.
* **Datenverarbeitung:** Anwenden benutzerdefinierter Funktionen zur Verarbeitung der extrahierten Daten.
* **API:** Zugriff auf gescrapte und verarbeitete Daten über HTTP-Endpunkte.
* **Task-Planung:** Automatisieren von Scraping-Aufgaben in regelmäßigen Abständen.
* **API-Authentifizierung:** Schutz der API mithilfe von API-Keys.
* **Ratenbegrenzung:** Begrenzung der Anzahl von API-Anfragen, um Missbrauch zu verhindern.
* **Caching:** Speichern von Webseiteninhalten im Cache, um die Leistung zu verbessern.
* **Datenbankintegration:** Speichern von gescrapten Daten in einer SQLite-Datenbank.
* **Sicherheit:** Robuste Maßnahmen zum Schutz vor Sicherheitslücken wie Path Traversal und CSS-Injection.
* **Monitoring:** Detaillierte Statusberichte für geplante Aufgaben (einschließlich Start-/Endzeiten, letzter Ausführungszeit, nächster Ausführungszeit und Fehlermeldungen).
* **Konfiguration:** Umfassende Konfiguration über YAML-Dateien und Umgebungsvariablen.


## Voraussetzungen

* **Python:** 3.7 oder höher (empfohlen: 3.9+).
* **pip:** Python-Paketmanager.
* **Chrome:** Google Chrome-Browser und ein kompatibler ChromeDriver.
* **NLTK Data:** `stopwords` für die Keyword-Extraktion (`nltk.download('stopwords')`).
* **Notwendige Python-Pakete:**
    ```bash
    pip install -r requirements.txt
    ```
    Die `requirements.txt` sollte folgende Pakete enthalten:
    ```
    beautifulsoup4
    flask
    nltk
    requests
    selenium
    webdriver-manager
    pyyaml
    python-dotenv
    pydantic
    schedule
    ```


## Installation

1. **Klonen des Repository (Optional):**
   ```bash
   git clone <Repository-URL>
   cd <Repository-Verzeichnis>
   ```

2. **Virtuelle Umgebung (Empfohlen):**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate     # Windows
   ```

3. **Abhängigkeiten installieren:**
   ```bash
   pip install -r requirements.txt
   ```

## Konfiguration

* **`config.yaml`:**  Die meisten Einstellungen werden hier konfiguriert. Siehe die mitgelieferte `config.yaml` als Vorlage. Wichtige Konfigurationsparameter sind:
    * `database_file`: Pfad zur SQLite-Datenbankdatei.
    * `schedule_config_file`: Pfad zur JSON-Datei mit den geplanten Tasks (wird nicht mehr direkt verwendet, sondern die Tasks werden in der Datenbank gespeichert).
    * `api_keys`: Liste der API-Keys für die API-Authentifizierung.
    * `processing_functions_dir`:  Verzeichnis, in dem sich benutzerdefinierte Verarbeitungsfunktionen befinden.
* **`.env`:** Für sensible Daten wie API-Keys.  Umgebungsvariablen überschreiben die YAML-Konfiguration.  Beispiel:
    ```
    API_KEY_1=<your_api_key_1>
    API_KEY_2=<your_api_key_2>
    API_KEY_3=<your_api_key_3>
    ```

## Ausführung

### API-Modus:

```bash
python app.py --api
```

### Kommandozeilenmodus (einmalige Ausführung):

```bash
python app.py <URL> [Optionen]
```

**Optionen:**

* `--text`: Nur Textinhalt extrahieren.
* `--save-file`: Inhalt in einer Datei speichern.
* `--stopwords "<kommagetrennte_stopwörter>"`: Zusätzliche Stopwörter für die Keyword-Extraktion.
* `--css-selectors "<JSON_mit_CSS_Selektoren>"`:  CSS-Selektoren für die Datenextraktion.
* `--processing-function <pfad_zur_python_datei>`: Pfad zu einer Python-Datei mit der Verarbeitungsfunktion `process_data(data)`.

**Beispiel:**

```bash
python app.py https://www.example.com --text --save-file --stopwords "und,die,der" --css-selectors '{"title": "title", "headings": "h1"}' --processing-function meine_verarbeitung.py
```

### Geplanter Modus:

```bash
python app.py 
```
Dieser Modus lädt geplante Tasks aus der Datenbank und führt sie nach dem definierten Zeitplan aus.


## API-Endpunkte

Alle API-Endpunkte erfordern einen gültigen API-Key im `X-API-Key` Header.  Die Ratenbegrenzung ist aktiv.

* `/api/v1/`:  API-Root mit Beschreibung aller Endpunkte.
* `/api/v1/fetch-html`:  HTML-Inhalt abrufen. Parameter: `url`, `stopwords`, `css-selectors`, `save-file`, `processing-function-path`.
* `/api/v1/fetch-text`: Textinhalt abrufen. Parameter:  `url`, `stopwords`, `css-selectors`, `save-file`, `processing-function-path`.
* `/api/v1/scheduled-tasks`:  Geplante Tasks verwalten (GET, POST, PUT, DELETE).
* `/api/v1/scheduled-tasks/<task_id>`:  Spezifischen Task verwalten (GET, PUT, DELETE).
* `/api/v1/scheduled-tasks/status`: Status aller geplanten Tasks abrufen.
* `/api/v1/scheduled-tasks/<task_id>/status`:  Status eines spezifischen Tasks abrufen.
* `/api/v1/scheduled-tasks/<task_id>/run`: Manuelles Ausführen eines geplanten Tasks.
* `/api/v1/health`: Health-Check der API.

## Benutzerdefinierte Datenverarbeitung (`processing.py`)

Erstelle eine Python-Datei (z.B. `meine_verarbeitung.py`) im konfigurierten `processing_functions_dir`.  Die Datei muss eine Funktion namens `process_data(data)` enthalten. Diese Funktion empfängt ein Dictionary mit den extrahierten Daten und gibt die verarbeiteten Daten als Dictionary oder serialisierbares Objekt zurück.

**Beispiel `meine_verarbeitung.py`:**

```python
import json

def process_data(data):
    """
    Beispielfunktion zur Datenverarbeitung.
    Extrahiert die Anzahl der Wörter im Titel und gibt sie zusammen mit dem Titel zurück.
    """
    title = data.get("title")
    if title:
        word_count = len(title.split())
        return {"title": title, "title_word_count": word_count}
    return None  # oder {} oder eine andere sinnvolle Rückgabe
```

## CSS-Selektoren

CSS-Selektoren ermöglichen die gezielte Extraktion von Daten. **Sicherheitshinweis:** Stellen Sie sicher, dass die CSS-Selektoren keine Sicherheitslücken öffnen.  Verwenden Sie die Funktion `is_safe_css_selector()` zur Überprüfung.  Ungültige oder unsichere Selektoren werden ignoriert.

**Beispiel für gültige CSS-Selektoren im JSON-Format:**

```json
{
  "title": {"selector": "title", "type": "string"},
  "h1": {"selector": "h1", "type": "string"},
  "preise": {"selector": ".preis", "type": "float", "cleanup": ["lower"]}
}
```

## Testen

Unit-Tests befinden sich im Verzeichnis `tests`.  Ausführen mit:

```bash
python -m unittest discover tests
```

## Sicherheit

* **API-Key Authentifizierung.**
* **Ratenbegrenzung.**
* **Path Traversal Schutz.**
* **CSS Injection Schutz.**
* **Whitelist für Verarbeitungsfunktionen.**
* **Sichere URL-Validierung:**  Es wird eine verbesserte URL-Validierung verwendet, um ungültige oder potenziell schädliche URLs zu erkennen.


## Monitoring

Über die API-Endpunkte `/api/v1/scheduled-tasks/status` und `/api/v1/scheduled-tasks/<task_id>/status` kann der Status der geplanten Tasks überwacht werden.  Es werden detaillierte Informationen wie Start-/Endzeiten, letzte und nächste Ausführungszeit sowie etwaige Fehlermeldungen angezeigt.


## Fehlerbehandlung

Fehler werden protokolliert.  Das Log-Level kann in der `config.yaml` konfiguriert werden.



## Beitrag leisten

Beiträge sind willkommen!  Bitte erstellen Sie ein Issue oder einen Pull Request.


## Kontakt

ralf.kruemmel+python@outlook.de

