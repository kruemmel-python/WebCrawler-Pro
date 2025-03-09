
**Web-Scraping und API-Programm: Umfassende Anleitung**

**1. Einführung**

Dieses Programm ist ein vielseitiges Werkzeug zum Extrahieren von Daten aus dem Web und zur Bereitstellung dieser Daten über eine API. Es kombiniert Web-Scraping-Funktionen mit einer robusten API, um das Erfassen, Verarbeiten und Bereitstellen von Informationen zu vereinfachen. Zu den wichtigsten Funktionen gehören:

*   **Web-Scraping:** Automatisches Abrufen von Webseiteninhalten mithilfe von Selenium.
*   **Datenextraktion:** Extrahieren von Text, Titeln, Metadaten, Überschriften und Schlüsselwörtern.
*   **CSS-Selektoren:** Gezielte Extraktion von Daten mithilfe von CSS-Selektoren.
*   **Datenverarbeitung:** Anwenden benutzerdefinierter Funktionen zur Verarbeitung der extrahierten Daten.
*   **API:** Zugriff auf gescrapte und verarbeitete Daten über HTTP-Endpunkte.
*   **Task-Planung:** Automatisieren von Scraping-Aufgaben in regelmäßigen Abständen.
*   **API-Authentifizierung:** Schutz der API mithilfe von API-Keys.
*   **Ratenbegrenzung:** Begrenzung der Anzahl von API-Anfragen, um Missbrauch zu verhindern.
*   **Caching:** Speichern von Webseiteninhalten im Cache, um die Leistung zu verbessern.
*   **Datenbankintegration:** Speichern von gescrapeten Daten in einer SQLite-Datenbank.
*   **Sicherheit:** Robuste Massnahmen zum Schutz vor Sicherheitslücken wie Path Traversal und CSS-Injection.
*   **Monitoring:** Detaillierte Statusberichte für geplante Aufgaben.
*   **Konfiguration:** Umfassende Konfiguration über YAML-Dateien und Umgebungsvariablen.

**2. Voraussetzungen**

Bevor du beginnst, stelle sicher, dass du Folgendes installiert hast:

*   **Python:** Python 3.7 oder höher (empfohlen: 3.9+).
*   **pip:** Python-Paketmanager (sollte mit Python installiert werden).
*   **Chrome:** Google Chrome-Browser (für Selenium).

**3. Installation**

1.  **Klonen des Repository (Optional):**

```bash
git clone [repository-URL]
cd [repository-Verzeichnis]
```

2.  **Erstellen einer virtuellen Umgebung (Empfohlen):**

```bash
python3 -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate.bat  # Windows
```

3.  **Installieren der Abhängigkeiten:**

```bash
pip install -r requirements.txt
```

**4. Konfiguration**

Das Programm kann über zwei Hauptwege konfiguriert werden:

*   **YAML-Konfigurationsdatei (`config.yaml`):** Für die meisten Einstellungen.
*   **Umgebungsvariablen (`.env`-Datei):** Für sensible Informationen wie API-Keys.

**4.1 YAML-Konfigurationsdatei (`config.yaml`)**

Erstelle eine `config.yaml`-Datei im Hauptverzeichnis des Projekts (oder verwende die mitgelieferte Vorlage). Die YAML-Datei enthält verschiedene Konfigurationsoptionen:

```yaml
database_file: webdata.db
schedule_config_file: scheduled_tasks.json
max_retries: 3
retry_delay: 2
allowed_processing_function_name: process_data
processing_functions_dir: .
log_level: INFO
api_debug_mode: true
api_keys:
  - secret-api-key-1
  - secret-api-key-2
  - another-secret-key
rate_limit_enabled: true
rate_limit_requests_per_minute: 20
cache_enabled: true
cache_expiry_seconds: 600
selenium_config:
  headless: true
  disable_gpu: true
  disable_extensions: true
  no_sandbox: true
  disable_dev_shm_usage: true
  user_agent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
allowed_css_properties:
  - color
  - font-size
  - background-color
  - margin
  - padding
  - text-align
  - font-weight
  - text-decoration
  - font-family
  - border
  - border-radius
  - width
  - height
  - display
  - visibility
  - opacity
  - cursor
  - list-style-type
  - vertical-align
```

**Optionen:**

*   `database_file`: Pfad zur SQLite-Datenbankdatei.
*   `schedule_config_file`: (Veraltet) Pfad zur Konfigurationsdatei für geplante Tasks.
*   `max_retries`: Maximale Anzahl an Wiederholungsversuchen beim Abrufen einer Webseite.
*   `retry_delay`: Verzögerung (in Sekunden) zwischen den Wiederholungsversuchen.
*   `allowed_processing_function_name`: Name der Funktion, die für die Datenverarbeitung zulässig ist.
*   `processing_functions_dir`: Verzeichnis, in dem sich die benutzerdefinierten Verarbeitungsfunktionen befinden.
*   `log_level`: Logging-Level (INFO, DEBUG, WARNING, ERROR, CRITICAL).
*   `api_debug_mode`: Aktiviert den Debug-Modus für die Flask-API.
*   `api_keys`: Liste der API-Keys für die Authentifizierung.
*   `rate_limit_enabled`: Aktiviert oder deaktiviert die Ratenbegrenzung.
*   `rate_limit_requests_per_minute`: Anzahl der zulässigen API-Anfragen pro Minute.
*   `cache_enabled`: Aktiviert oder deaktiviert das Caching.
*   `cache_expiry_seconds`: Gültigkeitsdauer des Caches in Sekunden.
*   `selenium_config`: Konfiguration für Selenium (headless, User-Agent usw.).
*   `allowed_css_properties`: Eine Liste sicherer CSS-Eigenschaften.

**4.2 Umgebungsvariablen (`.env`-Datei)**

Erstelle eine `.env`-Datei im Hauptverzeichnis des Projekts. Umgebungsvariablen werden verwendet, um sensible Informationen wie API-Keys zu speichern.

```
API_KEY_1=secret-api-key-1
API_KEY_2=secret-api-key-2
API_KEY_3=another-secret-key
```

Das Programm liest die Umgebungsvariablen `API_KEY_1`, `API_KEY_2` und `API_KEY_3` und kombiniert diese mit den API-Keys aus der `config.yaml`-Datei. Umgebungsvariablen haben Vorrang vor den YAML-Konfigurationen.

**5. Ausführen des Programms**

Das Programm kann in drei Modi ausgeführt werden:

*   **API-Modus:** Startet die Web-API.
*   **Kommandozeilenmodus:** Extrahiert Daten von einer einzelnen URL.
*   **Geplanter Modus:** Führt geplante Scraping-Aufgaben aus.

**5.1 API-Modus**

Um die API zu starten, verwende den `--api`-Parameter:

```bash
python app.py --api
```

Die API wird unter `http://127.0.0.1:5000` (oder der konfigurierten Adresse) ausgeführt.

**5.2 Kommandozeilenmodus**

Um Daten von einer einzelnen URL zu extrahieren, gib die URL als Argument an:

```bash
python app.py [URL] [OPTIONS]
```

**Beispiel:**

```bash
python app.py https://www.example.com --text --save-file --stopwords "keyword1, keyword2" --css-selectors '{"title": "h1", "description": "p"}' --processing-function processing_function.py
```

**Optionen:**

*   `--text`: Speichert nur den extrahierten Textinhalt.
*   `--save-file`: Speichert den Inhalt in einer Datei.
*   `--stopwords`: Kommagetrennte Liste von zusätzlichen Stopwörtern.
*   `--css-selectors`: JSON-String von CSS-Selektoren.
*   `--processing-function`: Pfad zu einer Python-Datei mit einer benutzerdefinierten Verarbeitungsfunktion.

**5.3 Geplanter Modus**

Wenn keine URL und kein `--api`-Parameter angegeben werden, wird das Programm im geplanten Modus ausgeführt:

```bash
python app.py
```

Das Programm lädt die geplanten Tasks aus der Datenbank und führt sie gemäß ihren Zeitplänen aus.

**6. API-Endpunkte**

Die API bietet die folgenden Endpunkte:

*   `/api/v1/` (GET): Gibt eine Liste aller verfügbaren Endpunkte und Beschreibungen zurück.
*   `/api/v1/fetch-html?url=[URL]&stopwords=[STOPWORDS]&css_selectors=[CSS_SELECTORS]&save_file=[TRUE|FALSE]&processing_function_path=[PATH]` (GET): Ruft den HTML-Inhalt einer Webseite ab.
*   `/api/v1/fetch-text?url=[URL]&stopwords=[STOPWORDS]&css_selectors=[CSS_SELECTORS]&save_file=[TRUE|FALSE]&processing_function_path=[PATH]` (GET): Ruft den Textinhalt einer Webseite ab.
*   `/api/v1/scheduled-tasks` (GET): Listet alle geplanten Scraping-Tasks auf.
*   `/api/v1/scheduled-tasks` (POST): Fügt einen neuen geplanten Scraping-Task hinzu (erwartet JSON im Request Body).
*   `/api/v1/scheduled-tasks/[task_id]` (GET): Ruft Details eines geplanten Scraping-Tasks anhand der Task-ID ab.
*   `/api/v1/scheduled-tasks/[task_id]` (PUT): Aktualisiert einen bestehenden geplanten Scraping-Task anhand der Task-ID (erwartet JSON im Request Body).
*   `/api/v1/scheduled-tasks/[task_id]` (DELETE): Entfernt einen geplanten Scraping-Task anhand der Task-ID.
*   `/api/v1/scheduled-tasks/status` (GET): Listet den Status aller geplanten Tasks auf.
*   `/api/v1/scheduled-tasks/[task_id]/status` (GET): Ruft den detaillierten Status eines spezifischen Tasks anhand der Task-ID ab.
*   `/api/v1/scheduled-tasks/[task_id]/run` (POST): Löst die sofortige Ausführung eines geplanten Tasks aus.
*   `/api/v1/health` (GET): Gibt den grundlegenden Gesundheitszustand der API zurück.

**Beispiel-API-Nutzung (mit `curl`):**

Abrufen von HTML-Inhalt:

```bash
curl -H "X-API-Key: secret-api-key-1" "http://127.0.0.1:5000/api/v1/fetch-html?url=https://www.example.com"
```

Auflisten geplanter Tasks:

```bash
curl -H "X-API-Key: secret-api-key-1" "http://127.0.0.1:5000/api/v1/scheduled-tasks"
```

**7. Task-Planung**

Das Programm verwendet die `schedule`-Bibliothek für die Task-Planung. Geplante Tasks werden in der Datenbank gespeichert und beim Start des Programms geladen.

**7.1 Hinzufügen eines geplanten Tasks (über die API)**

Sende eine `POST`-Anfrage an den `/api/v1/scheduled-tasks`-Endpunkt mit einem JSON-Payload im Request Body:

```json
{
  "url": "https://www.example.com",
  "schedule_time": "stündlich",
  "text_only": false,
  "stopwords": "keyword1, keyword2",
  "css_selectors": "{\"title\": \"h1\", \"description\": \"p\"}",
  "save_file": false,
  "processing_function_path": null
}
```

**Felder:**

*   `url`: Die URL der Webseite, die gescrapet werden soll.
*   `schedule_time`: Der Zeitplan für die Ausführung des Tasks (z.B. "stündlich", "täglich um 08:00", "alle 30 minuten").
*   `text_only`: Gibt an, ob nur der Textinhalt extrahiert werden soll.
*   `stopwords`: Kommagetrennte Liste von zusätzlichen Stopwörtern.
*   `css_selectors`: JSON-String von CSS-Selektoren.
*   `save_file`: Gibt an, ob der Inhalt in einer Datei gespeichert werden soll.
*   `processing_function_path`: Pfad zu einer Python-Datei mit einer benutzerdefinierten Verarbeitungsfunktion.

**7.2 Unterstützte Zeitplanformate**

Die folgenden Zeitplanformate werden unterstützt:

*   `stündlich`: Führt den Task stündlich aus.
*   `täglich um HH:MM`: Führt den Task täglich um die angegebene Uhrzeit aus (z.B. "täglich um 08:00").
*   `alle X minuten`: Führt den Task alle X Minuten aus (z.B. "alle 30 minuten").

**8. Benutzerdefinierte Datenverarbeitung**

Das Programm ermöglicht die Verwendung von benutzerdefinierten Funktionen zur Verarbeitung der extrahierten Daten.

**8.1 Erstellen einer Verarbeitungsfunktion**

Erstelle eine Python-Datei (z.B. `processing_function.py`) mit einer Funktion namens `process_data(data)`. Die Funktion akzeptiert ein Dictionary mit den extrahierten Daten und gibt die verarbeiteten Daten zurück.

```python
def process_data(data):
    """
    Beispiel für eine Verarbeitungsfunktion.

    Args:
        data (dict): Ein Dictionary mit den extrahierten Daten.

    Returns:
        dict: Ein Dictionary mit den verarbeiteten Daten.
    """
    title = data.get("title", "Kein Titel gefunden")
    keywords = data.get("keywords", [])
    processed_keywords = [keyword.upper() for keyword in keywords]
    return {"processed_title": title.upper(), "processed_keywords": processed_keywords}
```

**8.2 Konfigurieren der Verarbeitungsfunktion**

Gib den Pfad zur Python-Datei im `--processing-function`-Parameter an (im Kommandozeilenmodus) oder im `processing_function_path`-Feld des JSON-Payloads (beim Hinzufügen eines geplanten Tasks über die API). Stelle sicher, dass sich die Datei im Verzeichnis befindet, das in der `processing_functions_dir`-Konfigurationsoption angegeben ist.

**Sicherheitshinweis:** Sei vorsichtig bei der Verwendung von benutzerdefinierten Verarbeitungsfunktionen. Stelle sicher, dass du nur vertrauenswürdigen Code ausführst, da dies die Sicherheit des Systems beeinträchtigen kann.

**9. CSS-Selektoren**

Das Programm ermöglicht die gezielte Extraktion von Daten mithilfe von CSS-Selektoren.

**9.1 Angeben von CSS-Selektoren**

Gib einen JSON-String von CSS-Selektoren im `--css-selectors`-Parameter an (im Kommandozeilenmodus) oder im `css_selectors`-Feld des JSON-Payloads (beim Hinzufügen eines geplanten Tasks über die API).

```json
{
  "title": "h1",
  "description": "p",
  "price": ".price",
  "images": "img[src]"
}
```

Die Schlüssel im JSON-Objekt sind die Namen der extrahierten Daten, und die Werte sind die CSS-Selektoren.

**9.2 Konfigurierte CSS-Selektoren (Erweitert)**

Du kannst CSS-Selektoren mit Datentypen und Bereinigungsfunktionen konfigurieren. Dies erfordert die Verwendung eines Dictionary für jeden Selektor:

```json
{
  "item_name": {
    "selector": ".item-name",
    "type": "string",
    "cleanup": ["lower"]
  },
  "item_price": {
    "selector": ".item-price",
    "type": "float"
  },
    "image_urls": {
    "selector": "img[src]",
    "type": "string" # Daten aber nicht weiterverarbeiten
  }
}
```

*   `selector`: Der CSS-Selektor.
*   `type`: Der Datentyp (z. B. "string", "integer", "float").
*   `cleanup`: Eine Liste von Bereinigungsfunktionen (z. B. "lower").

**Datentypen:**

*   `string`: Extrahiert den Text als String.
*   `integer`: Konvertiert den extrahierten Text in eine Ganzzahl.
*   `float`: Konvertiert den extrahierten Text in eine Gleitkommazahl.

**Bereinigungsfunktionen:**

*   `lower`: Konvertiert den extrahierten Text in Kleinbuchstaben.

**Sicherheitshinweis:** Validiere CSS-Selektoren sorgfältig, um Injection-Angriffe zu vermeiden. Verwende die `is_safe_css_selector`-Funktion, um sicherzustellen, dass die Selektoren sicher sind.

**10. Datenbankintegration**

Das Programm speichert die extrahierten Daten in einer SQLite-Datenbank.

**10.1 Datenbankschema**

Die Datenbank enthält zwei Tabellen:

*   `scheduled_tasks`: Speichert die geplanten Tasks.
*   `web_content`: Speichert die extrahierten Webseiteninhalte.

**10.2 Konfigurieren der Datenbank**

Der Pfad zur Datenbankdatei wird in der `database_file`-Konfigurationsoption in der `config.yaml`-Datei angegeben.

**11. Sicherheit**

Das Programm implementiert verschiedene Sicherheitsmaßnahmen, um es vor Sicherheitslücken zu schützen.

**11.1 API-Key-Authentifizierung**

Die API ist mithilfe von API-Keys geschützt. Um auf die API zuzugreifen, musst du einen gültigen API-Key im `X-API-Key`-Header angeben. Die API-Keys werden in der `.env`-Datei oder in der `config.yaml`-Datei konfiguriert.

**11.2 Ratenbegrenzung**

Die API ist mithilfe von Ratenbegrenzung geschützt. Die Anzahl der zulässigen API-Anfragen pro Minute wird in der `rate_limit_requests_per_minute`-Konfigurationsoption in der `config.yaml`-Datei angegeben.

**11.3 Path Traversal-Schutz**

Die `is_safe_path`-Funktion wird verwendet, um Path Traversal-Angriffe zu verhindern. Die Funktion stellt sicher, dass Dateipfade innerhalb des zulässigen Basisverzeichnisses liegen.

**11.4 CSS-Injection-Schutz**

Die `is_safe_css_selector`-Funktion wird verwendet, um CSS-Injection-Angriffe zu verhindern. Die Funktion prüft, ob CSS-Selektoren unsichere Muster enthalten (z. B. `script`, `expression`, `javascript:`). Zusätzlich wird eine Whitelist von sicheren CSS-Eigenschaften verwendet.

**11.5 Schutz vor der Ausführung von unsicherem Code**

Das Programm verwendet eine Whitelist für Funktionsnamen, um die Ausführung von unsicherem Code zu verhindern. Nur Funktionen mit dem in der `allowed_processing_function_name`-Konfigurationsoption angegebenen Namen dürfen ausgeführt werden.

**12. Überwachung**

Das Programm bietet detaillierte Statusberichte für geplante Tasks.

**12.1 Task-Statusübersicht**

Der `/api/v1/scheduled-tasks/status`-Endpunkt gibt eine Liste aller Tasks mit ihrem Status zurück.

**12.2 Detaillierter Task-Status**

Der `/api/v1/scheduled-tasks/[task_id]/status`-Endpunkt gibt den detaillierten Status eines spezifischen Tasks zurück.

**13. Fehlerbehandlung**

Das Programm verwendet Logging, um Fehler zu protokollieren. Das Logging-Level kann in der `log_level`-Konfigurationsoption in der `config.yaml`-Datei konfiguriert werden.

**14. Testen**

Das Programm enthält Unit-Tests für Sicherheitsfunktionen. Um die Tests auszuführen, verwende den folgenden Befehl:

```bash
python -m unittest tests/test_security.py
```

Es ist wichtig, das die Unit-Tests erfolgreich durchlaufen und die Sicherheitsfunktionen korrekt funktionieren.

**15. Erweiterungen**

Das Programm kann durch Hinzufügen von neuen Funktionen und Integrationen erweitert werden.

**Beispiele:**

*   Unterstützung für weitere Datenquellen (z. B. RSS-Feeds, APIs).
*   Integration mit anderen Diensten (z. B. Slack, E-Mail).
*   Implementierung von Machine-Learning-Algorithmen zur Datenanalyse.
*   GUI für die Task-Planung und Konfiguration.

**16. Tipps zur Fehlerbehebung**

*   **Überprüfe die Logs:** Die Logs enthalten wertvolle Informationen über Fehler und Warnungen.
*   **Überprüfe die Konfiguration:** Stelle sicher, dass die YAML-Datei und die Umgebungsvariablen korrekt konfiguriert sind.
*   **Überprüfe die Datenbankverbindung:** Stelle sicher, dass das Programm eine Verbindung zur Datenbank herstellen kann.
*   **Überprüfe die API-Keys:** Stelle sicher, dass die API-Keys korrekt konfiguriert sind und im `X-API-Key`-Header angegeben werden.
*   **Überprüfe die CSS-Selektoren:** Stelle sicher, dass die CSS-Selektoren korrekt sind und die gewünschten Elemente auf der Webseite auswählen.
*   **Aktualisiere die Abhängigkeiten:** Stelle sicher, dass alle Abhängigkeiten auf dem neuesten Stand sind.
*   **Prüfe das Selenium Setup:**  Stelle sicher, dass die richtige Chrome Version installiert ist und der ChromeDriver korrekt konfiguriert wurde.

**17. Wichtige Hinweise**

*   **Verantwortungsvolles Scraping:**  Respektiere die `robots.txt`-Datei und belaste Webserver nicht unnötig.
*   **Lizenzbedingungen:**  Achte auf die Lizenzbedingungen der Webseiten, von denen Du Daten scrapst.
*   **Sicherheit:**  Sei besonders vorsichtig bei der Verwendung von benutzerdefinierten Verarbeitungsfunktionen und CSS-Selektoren, um Sicherheitslücken zu vermeiden.


