# 🚀 WebCrawler-Pro – Dokumentation und Bedienungsanleitung

## 1. Einleitung

**WebCrawler-Pro** ist ein vielseitiges und leistungsstarkes Programm zum automatisierten Extrahieren von Webinhalten. Es ermöglicht das Abrufen von HTML- und Textinhalten von Webseiten, die Extraktion strukturierter Daten mithilfe von CSS-Selektoren, die Keyword-Analyse und die optionale benutzerdefinierte Verarbeitung der gewonnenen Daten. WebCrawler-Pro bietet eine flexible Nutzung über die Kommandozeile, eine programmatische API und eine intuitive Streamlit-basierte Admin-Oberfläche.

**🎯 Zweck:**

*   ✅ Automatisierte Datenerfassung aus dem Web für Forschungszwecke, Marktanalysen, Content-Aggregation und mehr.
*   ⏱️ Regelmäßige Überwachung von Webseiteninhalten durch zeitgesteuerte Tasks.
*   🌐 Bereitstellung einer API für den Zugriff auf Web-Scraping-Funktionalitäten in anderen Anwendungen.
*   🖥️ Einfache Verwaltung und Überwachung geplanter Web-Scraping-Aufgaben über eine Web-Oberfläche.

**👥 Zielgruppe:**

*   📊 Datenanalysten und Wissenschaftler, die große Mengen an Webinhalten für ihre Analysen benötigen.
*   🧑‍💻 Softwareentwickler, die Web-Scraping-Funktionalitäten in ihre Anwendungen integrieren möchten.
*   📢 Content-Manager und Marketingexperten, die Webinhalte überwachen und analysieren müssen.
*   🛠️ Technische Anwender, die eine flexible und konfigurierbare Lösung für Web-Scraping suchen.

## 2. Systemanforderungen

Um WebCrawler-Pro nutzen zu können, müssen folgende Systemvoraussetzungen erfüllt sein:

**💻 Hardware:**

*   **Prozessor:** Intel Core i3 oder vergleichbarer Prozessor (empfohlen: Intel Core i5 oder besser)
*   **Arbeitsspeicher:** Mindestens 4 GB RAM (empfohlen: 8 GB RAM oder mehr, insbesondere für umfangreiche Scraping-Aufgaben und den API-Betrieb)
*   **Festplattenspeicher:** Mindestens 1 GB freier Festplattenspeicher für die Programminstallation und die Datenbank (der benötigte Speicherplatz kann je nach Umfang der gescrapten Daten variieren)

**💾 Software:**

*   **Betriebssystem:** Windows 10 oder höher, macOS 10.15 oder höher, Linux (getestet auf Ubuntu 20.04 und neuer)
*   **Python:** Python 3.8 oder höher (empfohlen: Python 3.9 oder 3.10). Stellen Sie sicher, dass Python und `pip` im Systempfad verfügbar sind.
*   **Webbrowser:** Google Chrome (für den Betrieb mit Selenium). Es wird empfohlen, die aktuellste stabile Version von Chrome zu verwenden.
*   **ChromeDriver:** Der zu Ihrer Chrome-Version passende ChromeDriver wird automatisch durch `webdriver-manager` installiert.

**🐍 Python Bibliotheken:**

Die folgenden Python-Bibliotheken sind für den Betrieb von WebCrawler-Pro erforderlich und werden in der Regel bei der Installation automatisch installiert:

*   `streamlit`
*   `pandas`
*   `beautifulsoup4`
*   `selenium`
*   `webdriver_manager`
*   `flask`
*   `sqlite3`
*   `nltk`
*   `pyyaml`
*   `pydantic`
*   `python-dotenv`

## 3. Installation

Folgen Sie diesen Schritten, um WebCrawler-Pro zu installieren:

**Schritt 1: Python installieren**

Laden Sie die aktuelle Version von Python 3.x von der offiziellen Python-Webseite ([https://www.python.org/downloads/](https://www.python.org/downloads/)) herunter und installieren Sie diese. Achten Sie darauf, bei der Installation die Option "Add Python to PATH" zu aktivieren.

**Schritt 2: Projektdateien herunterladen**

Laden Sie die Projektdateien von WebCrawler-Pro herunter und entpacken Sie das Archiv in einen lokalen Ordner.

**Schritt 3: Virtuelle Umgebung erstellen (empfohlen)**

Navigieren Sie im Terminal/Eingabeaufforderung in den Projektordner und erstellen Sie eine virtuelle Umgebung:

```bash
python -m venv venv
```

Aktivieren Sie die virtuelle Umgebung:

*   **Windows (Eingabeaufforderung):** `venv\Scripts\activate`
*   **Windows (PowerShell):** `venv\Scripts\Activate.ps1`
*   **macOS/Linux:** `source venv/bin/activate`

**Schritt 4: Bibliotheken installieren**

Installieren Sie die benötigten Python-Bibliotheken:

```bash
pip install streamlit pandas beautifulsoup4 selenium webdriver-manager flask pyyaml pydantic nltk python-dotenv
```

**Schritt 5: Konfiguration anpassen (optional)**

Passen Sie die `config.yaml` Datei bei Bedarf an. Wichtige Optionen:

*   `database_file`
*   `api_keys` (oder Umgebungsvariablen verwenden)
*   `rate_limit_requests_per_minute`
*   `cache_expiry_seconds`
*   `selenium_config`
*   `allowed_css_properties`
*   `processing_functions_dir`
*   `log_level`

**Schritt 6: ChromeDriver Installation**

ChromeDriver wird automatisch von `webdriver-manager` installiert.

**Schritt 7: Installation abschließen**

WebCrawler-Pro ist nun installiert.

### 3.1 API-Keys über Umgebungsvariablen konfigurieren 🔑

Erstellen Sie eine `.env` Datei im Projektordner und fügen Sie API-Keys hinzu:

```dotenv
API_KEY_1=IhrErsterAPIKey
API_KEY_2=IhrZweiterAPIKey
API_KEY_3=IhrDritterAPIKey
```

### 3.2 Fehlerbehebung bei der Installation 🛠️

Siehe vollständige Dokumentation für detaillierte Fehlerbehebungshinweise.

## 4. Benutzerführung

WebCrawler-Pro kann über Kommandozeile, Web-API oder Streamlit Admin-Oberfläche verwendet werden.

### 4.1 Kommandozeilenmodus ⌨️

Navigieren Sie zum Projektordner und aktivieren Sie die virtuelle Umgebung.

**Grundlegende Nutzung:**

```bash
python app.py <URL>
```

**Optionale Argumente:**

*   `--text`
*   `--save-file`
*   `--stopwords <Stopwörter>`
*   `--css-selectors <JSON-String>`
*   `--processing-function <Pfad>`
*   `--api`
*   `--streamlit`

**Beispiele:**

*   `python app.py --text https://www.example.com`
*   `python app.py --save-file --stopwords "zusätzlich,weiteres" https://www.example.com`
*   `python app.py --css-selectors '{"title": "h1", "paragraph": "p"}' https://www.example.com`
*   `python app.py --processing-function custom_processing.py https://www.example.com`
*   `python app.py --api`
*   `python app.py --streamlit`
*   `python app.py` (für Scheduled Mode)

### 4.2 Web-API 🌐

Starten Sie die API:

```bash
python app.py --api
```

API ist unter `http://localhost:5000` erreichbar.

**Authentifizierung:** API-Key im `X-API-Key` Header erforderlich (außer `/api/v1/health`).

**Rate Limiting & Caching:** Aktiv. Konfigurierbar in `config.yaml`.

**API Endpunkte:**

*   `/api/v1/` (GET) - API Übersicht
*   `/api/v1/fetch-html` (GET) - HTML Inhalt abrufen
*   `/api/v1/fetch-text` (GET) - Text Inhalt abrufen
*   `/api/v1/fetch-links` (GET) - Links extrahieren
*   `/api/v1/scheduled-tasks` (GET, POST) - Geplante Tasks verwalten (Liste, Erstellen)
*   `/api/v1/scheduled-tasks/<task_id>` (GET, PUT, DELETE) - Geplante Tasks verwalten (Details, Aktualisieren, Löschen)
*   `/api/v1/scheduled-tasks/status` (GET) - Task Status Übersicht
*   `/api/v1/scheduled-tasks/<task_id>/status` (GET) - Task Detail Status
*   `/api/v1/scheduled-tasks/<task_id>/run` (POST) - Task manuell ausführen
*   `/api/v1/health` (GET) - Health Check (kein API-Key benötigt)

**Beispiele für API-Anfragen:**

**Linux/macOS (curl):**

```bash
curl -X GET \
  'http://localhost:5000/api/v1/fetch-text?url=https://www.example.com&stopwords=example,test&css_selectors={"title": "h1"}' \
  -H 'X-API-Key: IhrAPIKey'
```

**Windows (PowerShell - Invoke-WebRequest):**

```powershell
$API_KEY = "IhrAPIKey" # Ersetzen Sie dies mit Ihrem API-Key
$API_HOST = "http://localhost:5000"

$response = Invoke-WebRequest -Uri "$API_HOST/api/v1/fetch-text?url=https://www.example.com&stopwords=example,test&css_selectors={\"title\": \"h1\"}" `
    -Headers @{'X-API-Key' = $API_KEY}

# Antwortinhalt als JSON ausgeben (optional)
$response.Content | ConvertFrom-Json
```

**Weitere Windows/PowerShell Beispiele (Invoke-WebRequest):**

*   **Links von einer Webseite abrufen:**

    ```powershell
    $API_KEY = "IhrAPIKey"
    $API_HOST = "http://localhost:5000"
    $BASE_URL = "https://www.example.com"

    $links_response = Invoke-WebRequest -Uri "$API_HOST/api/v1/fetch-links?url=$BASE_URL" `
        -Headers @{'X-API-Key' = $API_KEY} | ConvertFrom-Json

    # Links ausgeben (optional)
    $links_response.data.links
    ```

*   **HTML-Inhalt abrufen und in Datei speichern:**

    ```powershell
    $API_KEY = "IhrAPIKey"
    $API_HOST = "http://localhost:5000"
    $URL_TO_FETCH = "https://www.example.com"

    Invoke-WebRequest -Uri "$API_HOST/api/v1/fetch-html?url=$URL_TO_FETCH&save_file=true" `
        -Headers @{'X-API-Key' = $API_KEY}
    ```

### 4.3 Streamlit Admin-Oberfläche 🖥️

Starten Sie die Admin-Oberfläche:

```bash
python app.py --streamlit
```

Zugriff über `http://localhost:8501`.

**Benutzeroberfläche:**

1.  **API-Key Eingabe** 🔑
2.  **Geplante Tasks Übersicht** 📝 (mit Details und Aktionen)
3.  **Neuen Task hinzufügen**➕ (Formular)

**Bedienungshinweise:**

*   API-Key zu Beginn eingeben.
*   "Geplante Tasks" Übersicht für Task-Management.
*   "Neuen Task hinzufügen" für neue Tasks.
*   Zeitpläne und CSS-Selektoren korrekt formatieren.
*   Seite wird nach Task-Änderungen neu geladen.

## 5. Funktionsbeschreibung

### 5.1 Geplante Tasks erstellen (API und Admin-Oberfläche) ➕📝

**Request Body (JSON) für API Task-Erstellung:**

```json
{
  "url": "https://www.example.com",
  "schedule_time": "täglich um 08:00",
  "text_only": false,
  "stopwords": "example,test",
  "css_selectors": "{\"title\": \"h1\"}",
  "save_file": true,
  "processing_function_path": "custom_processing.py"
}
```

**Parameter:** `url`, `schedule_time`, `text_only`, `stopwords`, `css_selectors`, `save_file`, `processing_function_path`.

### 5.2 Geplante Tasks aktualisieren (API und Admin-Oberfläche) 🔄📝

**Request Body (JSON) für API Task-Aktualisierung:**

```json
{
  "schedule_time": "stündlich",
  "stopwords": "neue,stopwörter"
}
```

**Parameter:** `task_id` (Pfadparameter), Request Body (JSON) mit zu aktualisierenden Feldern.

### 5.3 Geplante Tasks löschen (API und Admin-Oberfläche) ❌📝

**Parameter:** `task_id` (Pfadparameter).

### 5.4 Geplante Tasks manuell ausführen (API und Admin-Oberfläche) ▶️📝

**Parameter:** `task_id` (Pfadparameter).

### 5.5 Webseiteninhalt abrufen und extrahieren (API und Kommandozeile) 🌐➡️📄

**Prozessablauf:**

1.  URL-Validierung ✅
2.  Cache-Prüfung 🗄️
3.  Webseitenabruf (Selenium) 🌐
4.  HTML-Parsing (Beautiful Soup) 🥣
5.  Datenextraktion (Text, Titel, Meta-Description, H1-Headings, Keywords, CSS-Daten) 📄
6.  Benutzerdefinierte Datenverarbeitung (optional) ⚙️
7.  Datenbank-Speicherung 💾
8.  Datei-Speicherung (optional) 🗂️
9.  Antwortgenerierung (API) / Ausgabe (Kommandozeile) 📤

### 5.6 Keyword-Extraktion 🔑🧮

*   Textvorverarbeitung, Stopwortfilterung, alphabetische Filterung, Worthäufigkeitszählung, Top-N Keywords.

### 5.7 CSS-Datenextraktion 🧱

*   Einfache und konfigurierte Selektoren (mit `selector`, `type`, `cleanup`).
*   Sicherheitsprüfung für CSS-Selektoren.

### 5.8 Benutzerdefinierte Datenverarbeitung ⚙️

*   `process_data(data)` Funktion in Python-Datei definieren.
*   Pfad zur Datei in Programm/Task konfigurieren.
*   Sicherheitswarnung beachten.⚠️

## 6. Beispielhafte Anwendungsfälle

*   Einmaliges Scrapen über Kommandozeile 🚀
*   Regelmäßiges Scrapen mit geplantem Task ⏱️
*   Extrahieren von Produktinformationen mit CSS-Selektoren 🛍️
*   Datenanalyse mit benutzerdefinierter Processing-Funktion 📊
*   Abrufen von Links über API 🔗

## 7. Fehlerbehebung

**Häufige Fehlermeldungen und Lösungen:**

*   "Ungültige URL" ❌🌐
*   "Webseiteninhalt konnte nicht abgerufen werden" ❌
*   "API-Key fehlt oder ist ungültig." ❌🔑
*   "Rate Limit überschritten. Bitte warten Sie eine Minute." ⏳
*   "Ungültiges JSON-Format für CSS-Selektoren." ❌🧱
*   "Ungültiger Pfad zur Processing-Funktion" ❌⚙️
*   "Fehler beim Speichern in die Datenbank" ❌💾
*   "Fehler in der Datenverarbeitungsfunktion" ❌⚙️
*    "Kritischer Datenbankfehler im Scheduled Mode. Programm wird beendet." ☠️💾

**Log-Level Konfiguration:**

Konfigurierbar in `config.yaml` unter `log_level`.

**Verfügbare Log-Level:**

*   `DEBUG` (detaillierteste Protokollierung) 🐛
*   `INFO` (Standard) ℹ️
*   `WARNING` ⚠️
*   `ERROR` ❌
*   `CRITICAL` ☠️

**Beispiel `config.yaml` für `DEBUG` Log-Level:**

```yaml
log_level: DEBUG
```

## 8. FAQ (Häufig gestellte Fragen)

**F: Wie konfiguriere ich API-Keys?**

A: API-Keys können in der `config.yaml` Datei unter `api_keys` als Liste von Strings oder sicherer über Umgebungsvariablen (siehe Abschnitt 3.1) konfiguriert werden.

**F: Wie ändere ich das Rate Limit der API?**

A: Das Rate Limit (maximale Anfragen pro Minute) kann in der `config.yaml` Datei unter `rate_limit_requests_per_minute` konfiguriert werden.

**F: Wie lange werden Webseiten im Cache gespeichert?**

A: Die Gültigkeitsdauer des Caches (in Sekunden) kann in der `config.yaml` Datei unter `cache_expiry_seconds` konfiguriert werden. Standardmäßig sind es 600 Sekunden (10 Minuten).

**F: Wie kann ich geplante Tasks verwalten?**

A: Geplante Tasks können über die Streamlit Admin-Oberfläche (empfohlen) oder über die Web-API verwaltet werden (erstellen, aktualisieren, löschen, auflisten, manuell ausführen, Status abrufen).

**F: Wo werden die gescrapten Daten gespeichert?**

A: Die gescrapten Daten werden in einer SQLite-Datenbank gespeichert. Der Pfad zur Datenbankdatei kann in der `config.yaml` Datei unter `database_file` konfiguriert werden.

**F: Kann ich nur Textinhalte extrahieren?**

A: Ja, Sie können nur Textinhalte extrahieren, indem Sie die Option `--text` in der Kommandozeile verwenden, `text_only=true` im Request Body für die API-Endpunkte `/fetch-html` und `/fetch-text` setzen oder die Checkbox "Nur Text extrahieren" in der Streamlit Admin-Oberfläche aktivieren.

**F: Wie kann ich benutzerdefinierte Stopwörter verwenden?**

A: Benutzerdefinierte Stopwörter können als kommagetrennte Liste über die Option `--stopwords` in der Kommandozeile, den Parameter `stopwords` in den API-Endpunkten `/fetch-html` und `/fetch-text` oder das Textfeld "Stopwörter" in der Streamlit Admin-Oberfläche angegeben werden.

**F: Sind CSS-Selektoren sicher zu verwenden?**

A: WebCrawler-Pro implementiert Sicherheitsprüfungen für CSS-Selektoren, um potenziell unsichere Selektoren zu erkennen und zu verhindern. Dennoch sollten Sie bei der Verwendung von CSS-Selektoren Vorsicht walten lassen und nur vertrauenswürdige Selektoren verwenden.

**F: Sind benutzerdefinierte Processing-Funktionen sicher?**

A: Benutzerdefinierte Processing-Funktionen können beliebigen Python-Code ausführen. Verwenden Sie diese Funktion nur mit Bedacht und stellen Sie sicher, dass Sie nur vertrauenswürdigen Code ausführen, um Sicherheitsrisiken zu vermeiden. WebCrawler-Pro validiert den Pfad zur Processing-Funktion, um unsichere Pfade zu verhindern.

**F: Unterstützt WebCrawler-Pro JavaScript-Rendering?**

A: Ja, WebCrawler-Pro verwendet Selenium und ChromeDriver, um Webseiten abzurufen, was das Rendering von JavaScript-Inhalten ermöglicht.

## 9. Glossar

*   **API (Application Programming Interface):** 🌐 Eine Schnittstelle, die es Softwareanwendungen ermöglicht, miteinander zu kommunizieren. Im Kontext von WebCrawler-Pro ermöglicht die API den programmatischen Zugriff auf Web-Scraping-Funktionalitäten.
*   **CSS-Selektor:** 🧱 Ein Muster, das verwendet wird, um HTML-Elemente auf einer Webseite auszuwählen und zu formatieren oder Daten aus diesen Elementen zu extrahieren.
*   **ChromeDriver:** 🌐 Ein separates ausführbares Programm, das von Selenium verwendet wird, um Chrome-Browser zu steuern.
*   **JSON (JavaScript Object Notation):** 📄 Ein leichtgewichtiges Datenformat, das für den Datenaustausch im Web verwendet wird.
*   **Rate Limiting:** ⏳ Eine Technik zur Begrenzung der Anzahl von Anfragen, die ein Benutzer oder eine Anwendung innerhalb eines bestimmten Zeitraums an eine API senden kann. Dies dient dem Schutz vor Überlastung und Missbrauch.
*   **Caching:** 🗄️ Eine Technik zur Speicherung häufig abgerufener Daten (z.B. Webseiteninhalte) in einem temporären Speicher (Cache), um den Zugriff zu beschleunigen und die Last auf den ursprünglichen Datenquelle zu reduzieren.
*   **Scheduled Task (Geplanter Task):** ⏱️📝 Eine Aufgabe, die automatisch zu einem vordefinierten Zeitpunkt oder in regelmäßigen Intervallen ausgeführt wird. Im Kontext von WebCrawler-Pro sind geplante Tasks Web-Scraping-Aufgaben, die automatisch nach Zeitplan ausgeführt werden.
*   **Selenium:** 🌐 Ein Framework für die Automatisierung von Webbrowsern. WebCrawler-Pro verwendet Selenium, um Webseiten dynamisch abzurufen und JavaScript-Inhalte zu rendern.

## 10. Kontakt und Support

**E-Mail:** 📧 support@webcrawler-pro.example.com (Platzhalter E-Mail Adresse)

**Webseite:** 🌐 www.webcrawler-pro.example.com (Platzhalter Webseite)

Bitte beschreiben Sie Ihr Problem/Anfrage detailliert.


