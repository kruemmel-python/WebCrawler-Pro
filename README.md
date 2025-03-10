Okay, hier ist die ausführliche Dokumentation und Bedienungsanleitung als `README.md` im Markdown-Format mit Symbolen, wie gewünscht:

# 🚀 WebCrawler-Pro – Dokumentation und Bedienungsanleitung

## 1. Einleitung

**WebCrawler-Pro** ist eine hochentwickelte und robuste Anwendung für das automatisierte Web-Scraping. Es ermöglicht das effiziente Erfassen von Webinhalten, von einfachem Text bis hin zu komplexen HTML-Strukturen, und bietet dabei eine Vielzahl von Funktionen für die Datenextraktion, -verarbeitung und -verwaltung. WebCrawler-Pro zeichnet sich durch seine Flexibilität in der Nutzung aus – ob über die Kommandozeile für schnelle Aufgaben, als programmatische API für Integrationen oder über eine intuitive Streamlit-Admin-Oberfläche für umfassende Task-Verwaltung.

**🎯 Hauptmerkmale und Verbesserungen:**

*   **Integrierter API-Key Generator:** Beinhaltet ein `key_generator.py` Skript zum einfachen Generieren und Verwalten von API-Keys.
*   **Datenbankunterstützung mit SQLite:** Verwendet eine leichtgewichtige SQLite-Datenbank für die Speicherung der gescrapten Inhalte und Task-Konfigurationen.
*   **Erweiterte Task-Verwaltung:**  Umfassendes CRUD-Management für geplante Web-Scraping-Tasks über API und Streamlit UI. Speichern von Task-Konfigurationen und Status in der Datenbank.
*   **Verbesserte Robustheit und Leistung:**
    *   **Asynchrone Web-Requests (aiohttp):**  Primärer Web-Abrufmechanismus für hohe Performance und Effizienz.
    *   **Selenium Fallback:**  Automatischer Fallback auf Selenium für dynamische Webseiten mit JavaScript-Rendering.
    *   **Erhöhte Wiederholungsversuche & Verzögerungen:**  Anpassbare `max_retries` (Standard: 5) und `retry_delay` (Standard: 3 Sekunden) für zuverlässigeren Webseitenabruf.
    *   **Effizientes Caching:**  Zwischenspeicherung von Webseiteninhalten zur Reduzierung von redundanten Anfragen und zur Performance-Steigerung (anpassbare `cache_expiry_seconds`, Standard: 10 Minuten).
    *   **Rate Limiting:**  Schutz der API durch konfigurierbares Rate Limiting (Standard: 20 Anfragen pro Minute), um Überlastungen zu vermeiden.
*   **Umfassende API mit API-Key-Authentifizierung:**  Gesicherte Web-API für programmatischen Zugriff auf alle Kernfunktionen, inklusive Task-Management und Web-Scraping. API-Key-Authentifizierung und Rate Limiting für Sicherheit und Stabilität.
*   **Intuitive Streamlit Admin-Oberfläche:**  Web-basierte UI zur einfachen Verwaltung und Überwachung von geplanten Tasks, inklusive Task-Erstellung, -Bearbeitung, -Löschung und manueller Ausführung. Zusätzlich eine Datenbankbrowser-Oberfläche für die Inhaltsrecherche.
*   **Erweiterte Datenextraktion:**
    *   **CSS-Selektoren mit Sicherheitsvalidierung:**  Flexible Extraktion strukturierter Daten mittels CSS-Selektoren, inklusive konfigurierbarer Datentypen und Bereinigungsfunktionen. Sicherheitsprüfungen zum Schutz vor CSS-Injection.
    *   **Keyword-Extraktion:**  Automatische Keyword-Analyse extrahierter Textinhalte.
    *   **Benutzerdefinierte Datenverarbeitung:**  Option zur Integration eigener Python-Funktionen zur individuellen Verarbeitung der gescrapten Daten.
*   **Verbesserte Fehlerbehandlung und Logging:**  Detaillierte Protokollierung mit konfigurierbaren Log-Leveln (DEBUG, INFO, WARNING, ERROR, CRITICAL) für effektive Fehleranalyse und -behebung. Datenbank-Transaktionen für Datensicherheit.
*   **Sicherheitsfokus:**  API-Key-Authentifizierung, Rate Limiting, CSS-Selektor-Validierung, Pfadvalidierung für Processing-Funktionen, Datenbank-Transaktionen.
*   **Flexibilität in der Nutzung:**  Kommandozeile, Web-API und Streamlit Admin-Oberfläche für unterschiedliche Anwendungsfälle und Benutzerpräferenzen.

**🎯 Zweck:**

*   ✅ Automatisierte Datenerfassung aus dem Web für anspruchsvolle Forschungs- und Analysezwecke, erweiterte Marktanalysen, umfassende Content-Aggregation und mehr.
*   ⏱️ Zuverlässige und regelmäßige Überwachung von Webseiteninhalten durch flexible, zeitgesteuerte Tasks mit robuster Task-Verwaltung.
*   🌐 Professionelle API-Bereitstellung für den sicheren und effizienten Zugriff auf Web-Scraping-Funktionalitäten in Enterprise-Anwendungen und komplexen Systemen.
*   🖥️ Benutzerfreundliche und effiziente Verwaltung und Überwachung umfangreicher geplanter Web-Scraping-Aufgaben über eine moderne Web-Oberfläche mit integriertem Datenbankbrowser und API-Key Generator.

**👥 Zielgruppe:**

*   📊 Fortgeschrittene Datenanalysten und Wissenschaftler, die hochvolumige und komplexe Webinhalte für tiefgehende Analysen und Forschungsprojekte benötigen.
*   🧑‍💻 Softwareentwickler und Systemarchitekten, die robuste und skalierbare Web-Scraping-Funktionalitäten in ihre professionellen Anwendungen und Services integrieren möchten.
*   📢 Enterprise Content-Manager und Marketingstrategen, die umfassende Web-Intelligence-Lösungen zur Wettbewerbsanalyse und Marktbeobachtung benötigen.
*   🛠️ Technische Experten und DevOps-Teams, die eine hochflexible, konfigurierbare und sichere Lösung für Enterprise-Web-Scraping-Anforderungen suchen.

## 2. Systemanforderungen

Um WebCrawler-Pro in vollem Umfang nutzen zu können, sind folgende Systemvoraussetzungen empfehlenswert:

**💻 Hardware:**

*   **Prozessor:** Intel Core i5 oder vergleichbarer Mehrkernprozessor (empfohlen: Intel Core i7 oder Xeon für hochvolumige Scraping-Aufgaben und API-Last)
*   **Arbeitsspeicher:** Mindestens 8 GB RAM (empfohlen: 16 GB RAM oder mehr, insbesondere für parallele Scraping-Prozesse, API-Betrieb unter Last und Datenbankoperationen)
*   **Festplattenspeicher:** Mindestens 5 GB freier, schneller Festplattenspeicher (SSD empfohlen) für die Programminstallation, Datenbank und Caching (der benötigte Speicherplatz kann je nach Umfang der gescrapten Daten und Cache-Größe variieren)

**💾 Software:**

*   **Betriebssystem:** Windows 10/11 oder Server-Äquivalent, macOS 11 (Big Sur) oder höher, Linux (getestet auf aktuellen Ubuntu LTS und CentOS/RHEL)
*   **Python:** Python 3.9, 3.10 oder 3.11 (empfohlen: Python 3.10 für optimale Performance und Kompatibilität). Stellen Sie sicher, dass Python und `pip` im Systempfad verfügbar sind.
*   **Webbrowser:** Google Chrome (neueste stabile Version für optimale Selenium-Kompatibilität und Performance).
*   **ChromeDriver:** Aktuelle ChromeDriver-Version, automatisch verwaltet durch `webdriver-manager`.
*   **Datenbank-System (optional):**
    *   **SQLite (Standard):** Für kleinere bis mittlere Scraping-Projekte und Einzelplatzinstallationen ausreichend.
    *   **PostgreSQL oder MySQL:**  Empfohlen für Enterprise-Umgebungen, hochvolumige Daten, API-Betrieb unter Last und verbesserte Datenbank-Performance und -Zuverlässigkeit. Datenbankserver muss separat installiert und konfiguriert werden. **Hinweis:** PostgreSQL und MySQL-Unterstützung ist aktuell nur rudimentär implementiert.

**🐍 Python Bibliotheken:**

Die folgenden Python-Bibliotheken sind zwingend erforderlich und werden typischerweise bei der Installation automatisch durch `pip` installiert:

*   `streamlit` (für Admin- und Datenbankbrowser-Oberfläche)
*   `pandas` (für Datenmanipulation und -darstellung)
*   `beautifulsoup4` (für HTML-Parsing)
*   `selenium` (für dynamisches Web-Scraping und JavaScript-Rendering)
*   `webdriver_manager` (für automatische ChromeDriver-Verwaltung)
*   `flask` (für Web-API)
*   `sqlite3` (für SQLite-Datenbank)
*   `nltk` (für Keyword-Extraktion)
*   `pyyaml` (für Konfigurationsmanagement)
*   `pydantic` (für Datenvalidierung)
*   `python-dotenv` (für Umgebungsvariablen-Management)
*   `aiohttp` (für asynchrone HTTP-Requests)
*   `chardet` (für Zeichenkodierungserkennung)
*   `mimetypes` (für MIME-Type-Erkennung)

## 3. Installation

Befolgen Sie diese detaillierten Schritte, um WebCrawler-Pro optimal zu installieren und für Ihre Anforderungen zu konfigurieren:

**Schritt 1: Python installieren (und `venv`, `pip` sicherstellen)**

Laden Sie eine der empfohlenen Python-Versionen (3.9, 3.10 oder 3.11) von der offiziellen Python-Webseite ([https://www.python.org/downloads/](https://www.python.org/downloads/)) herunter und installieren Sie diese.

*   **Wichtig:** Aktivieren Sie unbedingt die Option "Add Python to PATH" während der Installation, damit Python und `pip` über die Kommandozeile zugänglich sind.
*   **Virtuelle Umgebung (`venv`) und Paketmanager (`pip`):**  Moderne Python-Installationen beinhalten in der Regel bereits `venv` (für virtuelle Umgebungen) und `pip` (Paketmanager). Stellen Sie sicher, dass diese verfügbar sind, indem Sie `python -m venv --version` und `pip --version` in Ihrem Terminal ausführen.

**Schritt 2: Projektdateien herunterladen und entpacken**

Laden Sie die WebCrawler-Pro Projektdateien als ZIP-Archiv herunter und entpacken Sie dieses in einen lokalen Ordner Ihrer Wahl (z.B. `C:\webcrawler-pro` unter Windows oder `/home/user/webcrawler-pro` unter Linux/macOS).

**Schritt 3: Virtuelle Umgebung erstellen (stark empfohlen)**

Wechseln Sie im Terminal/Eingabeaufforderung in den entpackten Projektordner. Erstellen Sie eine isolierte virtuelle Umgebung, um die Projekt-Abhängigkeiten von Ihrem globalen Python-System zu trennen:

```bash
python -m venv venv
```

**Schritt 4: Virtuelle Umgebung aktivieren**

Aktivieren Sie die neu erstellte virtuelle Umgebung, um nachfolgende `pip`-Befehle innerhalb dieser isolierten Umgebung auszuführen:

*   **Windows (Eingabeaufforderung):** `venv\Scripts\activate`
*   **Windows (PowerShell):** `venv\Scripts\Activate.ps1`
*   **macOS/Linux (Bash/Zsh):** `source venv/bin/activate`

    *   **Hinweis:** Nach der Aktivierung sollte der Name der virtuellen Umgebung `(venv)` am Anfang Ihrer Terminal-Prompt angezeigt werden.

**Schritt 5: Python-Bibliotheken installieren**

Installieren Sie alle erforderlichen Python-Bibliotheken und deren Abhängigkeiten aus der `requirements.txt` Datei des Projekts:

```bash
pip install -r requirements.txt
```

    *   **Alternativ (falls keine `requirements.txt` vorhanden):**
        ```bash
        pip install streamlit pandas beautifulsoup4 selenium webdriver-manager flask sqlite3 nltk pyyaml pydantic python-dotenv aiohttp chardet mimetypes
        ```

**Schritt 6: Konfigurationsdatei `config.yaml` anpassen (optional, aber empfohlen)**

Öffnen Sie die `config.yaml` Datei im Projektordner mit einem Texteditor. Überprüfen und passen Sie die folgenden wichtigen Konfigurationsoptionen nach Bedarf an:

*   **`database_file`:**  Pfad zur SQLite-Datenbankdatei. Standardmäßig `webdata.db`.
*   **`database_type`:**  Datenbanktyp. Standardmäßig `sqlite`. Aktuell ist nur SQLite vollständig unterstützt. Optionen `postgresql` und `mysql` sind rudimentär vorhanden, aber noch nicht vollständig funktionsfähig.
*   **`schedule_config_file`:** Pfad zur Datei für die Task-Zeitplankonfiguration (JSON-Format). Standardmäßig `scheduled_tasks.json`.
*   **`api_keys`:**  Liste der API-Keys für die Authentifizierung.  Sicherer ist die Verwendung von Umgebungsvariablen (siehe Abschnitt 3.1).
*   **`rate_limit_requests_per_minute`:**  Maximale Anzahl API-Anfragen pro Minute. Anpassen nach Bedarf.
*   **`cache_expiry_seconds`:**  Gültigkeitsdauer des Webseiten-Caches in Sekunden. Standardmäßig 600 Sekunden (10 Minuten).
*   **`selenium_config`:**  Konfiguration für Selenium (z.B. `headless`, `user_agent`).
*   **`allowed_css_properties`:**  Whitelist für erlaubte CSS-Eigenschaften in CSS-Selektoren (Sicherheitsmaßnahme).
*   **`processing_functions_dir`:**  Verzeichnis für benutzerdefinierte Processing-Funktionen.
*   **`log_level`:**  Log-Level für die Anwendung (z.B. `INFO`, `DEBUG`, `WARNING`).

**Schritt 7: API-Keys generieren (optional, aber empfohlen)**

Für den Zugriff auf die Web-API und die Streamlit Admin-Oberfläche benötigen Sie API-Keys. Verwenden Sie das mitgelieferte `key_generator.py` Skript, um API-Keys zu generieren und in der `.env`-Datei und `config.yaml` zu speichern:

1.  **Terminal öffnen und zum Projektordner navigieren:**  Öffnen Sie Ihr Terminal/Eingabeaufforderung und wechseln Sie in das Hauptverzeichnis des WebCrawler-Pro Projekts.
2.  **Virtuelle Umgebung aktivieren (falls verwendet):**  Aktivieren Sie die virtuelle Umgebung, falls Sie eine erstellt haben (siehe Schritt 4 der Installation).
3.  **`key_generator.py` ausführen:** Führen Sie das Key-Generator-Skript aus, um standardmäßig 3 API-Keys zu generieren und zu speichern:

    ```bash
    python key_generator.py
    ```

    *   Sie können die Anzahl der zu generierenden Keys optional anpassen, indem Sie den Parameter `num_keys` im Skript ändern.
    *   Die generierten API-Keys werden sowohl in der `.env`-Datei (für Umgebungsvariablen) als auch in der `config.yaml` unter `api_keys` gespeichert.

**Schritt 8: ChromeDriver Installation (automatisch durch `webdriver-manager`)**

ChromeDriver wird beim ersten Start von Selenium automatisch durch `webdriver-manager` heruntergeladen und installiert, passend zu Ihrer installierten Chrome-Version. Sie müssen ChromeDriver nicht manuell installieren.

**Schritt 9: Installation abschließen**

WebCrawler-Pro ist nun erfolgreich installiert und konfiguriert. Sie können das Programm im Kommandozeilenmodus, als Web-API oder über die Streamlit Admin-Oberfläche starten.

### 3.1 API-Keys sicher über Umgebungsvariablen konfigurieren 🔑

Für erhöhte Sicherheit und einfachere Verwaltung empfiehlt es sich, API-Keys über Umgebungsvariablen zu konfigurieren, anstatt sie direkt in der `config.yaml` Datei zu hinterlegen. Das `key_generator.py` Skript (Schritt 7 der Installation) unterstützt dies automatisch und speichert die Keys sowohl in `.env` als auch in `config.yaml`.

**Manuelle Konfiguration über `.env` Datei (Alternative):**

1.  **`.env` Datei erstellen:**  Erstellen Sie im Hauptprojektordner eine neue Datei namens `.env` (ohne Dateiendung).
2.  **API-Keys in `.env` eintragen:** Fügen Sie Ihre API-Keys in die `.env` Datei ein, wobei jeder Key in einer separaten Zeile im Format `API_KEY_NUMMER=IhrAPIKey` definiert wird:

    ```dotenv
    API_KEY_1=IhrErsterAPIKey
    API_KEY_2=IhrZweiterAPIKey
    API_KEY_3=IhrDritterAPIKey
    # ... weitere API-Keys bei Bedarf
    ```

    *   **Ersetzen Sie `IhrErsterAPIKey`, `IhrZweiterAPIKey`, `IhrDritterAPIKey` durch Ihre tatsächlichen API-Keys.**
3.  **Umgebungsvariablen laden:**  WebCrawler-Pro lädt beim Start automatisch die in der `.env` Datei definierten Umgebungsvariablen und verwendet diese für die API-Key-Authentifizierung.

### 3.2 Fehlerbehebung bei der Installation und häufige Probleme 🛠️

*   **Fehlende Python-Bibliotheken:** Stellen Sie sicher, dass Sie alle Bibliotheken gemäß Schritt 5 installiert haben (`pip install -r requirements.txt` oder manuell). Überprüfen Sie die Fehlermeldungen im Terminal auf fehlende Bibliotheken.
*   **ChromeDriver-Probleme:** Wenn Selenium-Operationen fehlschlagen, stellen Sie sicher, dass Sie eine kompatible Version von Google Chrome installiert haben. `webdriver-manager` sollte ChromeDriver automatisch verwalten. Überprüfen Sie die Logs auf ChromeDriver-bezogene Fehlermeldungen.
*   **Datenbankverbindungsfehler (PostgreSQL/MySQL):**  Vergewissern Sie sich, dass der PostgreSQL- oder MySQL-Datenbankserver läuft und die in `database_url` angegebenen Verbindungsinformationen korrekt sind (Hostname, Port, Benutzername, Passwort, Datenbankname). Testen Sie die Datenbankverbindung separat mit einem Datenbank-Client-Tool. **Hinweis:** Aktuell wird nur SQLite vollständig unterstützt.
*   **Berechtigungsfehler:**  Stellen Sie sicher, dass das Python-Skript Schreibrechte im Projektordner hat (z.B. für die SQLite-Datenbankdatei oder Logdateien).
*   **Portkonflikte (API/Streamlit):**  Wenn die API oder Streamlit Admin-Oberfläche nicht starten, könnte der Standardport (API: 5000, Streamlit: 8501) bereits von einer anderen Anwendung verwendet werden. Sie können versuchen, die Ports in der Anwendungskonfiguration zu ändern (falls konfigurierbar) oder die konkurrierende Anwendung zu stoppen.
*   **`config.yaml` Fehler:**  Überprüfen Sie die `config.yaml` Datei auf Syntaxfehler (z.B. falsche YAML-Formatierung). Verwenden Sie einen YAML-Validator online, um die Syntax zu prüfen.
*   **Log-Dateien prüfen:**  Überprüfen Sie die Log-Dateien (falls aktiviert) auf detailliertere Fehlermeldungen und Hinweise zur Fehlerursache. Konfigurieren Sie den `log_level` in `config.yaml` auf `DEBUG` für detailliertere Protokollierung bei Problemen.

Für weitere detaillierte Fehlerbehebungshinweise und spezifische Probleme konsultieren Sie bitte die vollständige Dokumentation (falls vorhanden) oder die Online-Community/Support-Kanäle von WebCrawler-Pro.

## 4. Benutzerführung

WebCrawler-Pro bietet drei Hauptnutzungsmodi, die jeweils für unterschiedliche Szenarien und Benutzerpräferenzen optimiert sind: Kommandozeilenmodus, Web-API und Streamlit Admin-Oberfläche.

### 4.1 Kommandozeilenmodus ⌨️ – Für schnelle, einmalige Aufgaben

Der Kommandozeilenmodus eignet sich ideal für das schnelle Ausführen von Web-Scraping-Aufgaben, insbesondere für einmalige Abrufe oder Testzwecke.

1.  **Terminal öffnen und zum Projektordner navigieren:**  Öffnen Sie Ihr Terminal/Eingabeaufforderung und wechseln Sie in das Hauptverzeichnis des WebCrawler-Pro Projekts.
2.  **Virtuelle Umgebung aktivieren (falls verwendet):**  Aktivieren Sie die virtuelle Umgebung, falls Sie eine erstellt haben (siehe Schritt 4 der Installation).
3.  **Kommando ausführen:**  Verwenden Sie den `python app.py` Befehl gefolgt von der URL und optionalen Argumenten.

**Grundlegende Nutzung (URL als erstes Argument):**

```bash
python app.py <URL_der_zu_scrapen_Webseite>
```

    *   **Beispiel:** `python app.py https://www.example.com`
        *   Dieser Befehl startet den Web-Scraping-Prozess für die angegebene URL, extrahiert Inhalte und speichert diese (standardmäßig in der Datenbank).

**Optionale Argumente (nach `app.py` und URL):**

| Argument               | Kurzbeschreibung                                                                                                                                         | Beispiel                                                                                                   |
| :--------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------- |
| `--text`               | Speichert nur den extrahierten Textinhalt (anstatt des gesamten HTML-Codes) in der Datenbank und optional in einer Datei.                                 | `python app.py --text https://www.example.com`                                                           |
| `--save-file`          | Speichert den extrahierten Inhalt (HTML oder Text, abhängig von `--text`) zusätzlich zur Datenbank in einer Textdatei im Projektverzeichnis.            | `python app.py --save-file https://www.example.com`                                                      |
| `--stopwords "<Liste>"` | Verwendet eine kommagetrennte Liste von zusätzlichen Stopwörtern für die Keyword-Extraktion. Ersetzt `<Liste>` durch Ihre Stopwörter in Anführungszeichen. | `python app.py --stopwords "zusätzlich,weiteres,unwichtig" https://www.example.com`                      |
| `--css-selectors '<JSON>'` | Verwendet einen JSON-String zur Definition von CSS-Selektoren für die strukturierte Datenextraktion. Ersetzt `<JSON>` durch Ihren JSON-String.                                      | `python app.py --css-selectors '{"title": "h1", "paragraph": ".article-text p"}' https://www.example.com` |
| `--processing-function <Pfad>` | Verwendet eine benutzerdefinierte Python-Funktion zur Datenverarbeitung. Ersetzt `<Pfad>` durch den relativen Pfad zur Python-Datei mit der Funktion `process_data(data)`.                     | `python app.py --processing-function custom_processing.py https://www.example.com`                       |
| `--api`                | Startet WebCrawler-Pro im Web-API-Modus.                                                                                                               | `python app.py --api`                                                                                     |
| `--streamlit`          | Startet die Streamlit Admin-Oberfläche im Webbrowser.                                                                                                   | `python app.py --streamlit`                                                                               |
| `--db-browser`         | Startet die Streamlit Datenbankbrowser-Oberfläche im Webbrowser.                                                                                         | `python app.py --db-browser`                                                                            |
| *(keine URL, keine Option)* | Startet WebCrawler-Pro im Scheduled Mode (geplante Tasks aus Datenbank werden ausgeführt).                                                              | `python app.py`                                                                                           |

**Beispiele für Kommandozeilenbefehle:**

*   **Nur Text von einer Webseite extrahieren und in der Datenbank speichern:**
    ```bash
    python app.py --text https://www.example.com/artikel
    ```

*   **HTML-Inhalt extrahieren, in Datenbank speichern und zusätzlich als Datei speichern:**
    ```bash
    python app.py --save-file https://www.example.com/produktseite
    ```

*   **Keywords extrahieren mit zusätzlichen Stopwörtern:**
    ```bash
    python app.py --stopwords "sonderangebot,rabatt,aktion" https://www.example.com/angebote
    ```

*   **Strukturierte Daten mit CSS-Selektoren extrahieren (Titel und Artikeltext):**
    ```bash
    python app.py --css-selectors '{"artikel_titel": "h1.title", "artikel_inhalt": ".article-body"}' https://www.example.com/news/artikel123
    ```

*   **Daten mit einer benutzerdefinierten Python-Funktion verarbeiten:**
    ```bash
    python app.py --processing-function benutzerdefinierte_verarbeitung.py https://www.example.com/daten
    ```

*   **WebCrawler-Pro im API-Modus starten:**
    ```bash
    python app.py --api
    ```

*   **Streamlit Admin-Oberfläche starten:**
    ```bash
    python app.py --streamlit
    ```

*   **Streamlit Datenbankbrowser starten:**
    ```bash
    python app.py --db-browser
    ```

*   **Scheduled Mode starten (geplante Tasks ausführen):**
    ```bash
    python app.py
    ```

### 4.3 Streamlit Admin-Oberfläche 🖥️ – Task- und Datenbankverwaltung

Die Streamlit Admin-Oberfläche bietet eine benutzerfreundliche Weboberfläche zur Verwaltung von geplanten Tasks und zur Datenbankrecherche.

1.  **Admin-Oberfläche starten:** Starten Sie die Streamlit Admin-Oberfläche über die Kommandozeile:

    ```bash
    python app.py --streamlit
    ```

    *   Die Admin-Oberfläche ist nun unter der Adresse `http://localhost:8501` erreichbar.

2.  **API-Key eingeben:**  Geben Sie auf der Startseite der Admin-Oberfläche einen gültigen API-Key in das Textfeld "API-Key eingeben" ein. Dies authentifiziert Ihre Sitzung für den Zugriff auf die API-Funktionen.

3.  **Geplante Tasks verwalten:**  Im Bereich "Geplante Tasks" können Sie:
    *   **Tasks anzeigen:**  Eine Liste aller geplanten Tasks mit Details wie URL, Zeitplan, Status etc. wird angezeigt.
    *   **Task-Details erweitern:**  Klicken Sie auf den Expander-Button neben der Task-ID, um detaillierte Informationen zu einem Task anzuzeigen (URL, Zeitplan, Parameter, Status, letzte Ausführung, nächste Ausführung, Fehlermeldungen).
    *   **Tasks löschen:**  Klicken Sie innerhalb der erweiterten Task-Details auf den "Task [Task-ID] löschen" Button, um einen Task dauerhaft zu entfernen.
    *   **Tasks sofort ausführen:** Klicken Sie innerhalb der erweiterten Task-Details auf den "Task [Task-ID] sofort ausführen" Button, um einen Task manuell und unabhängig vom Zeitplan zu starten.

4.  **Neue Tasks hinzufügen:**  Im Bereich "Neuen Task hinzufügen" können Sie über ein Formular neue geplante Tasks erstellen:
    *   **URL:** Geben Sie die Start-URL der Webseite ein, die gescraped werden soll.
    *   **Zeitplan:** Definieren Sie den Zeitplan für die Task-Ausführung. Unterstützte Formate sind: `stündlich`, `täglich um HH:MM`, `alle X minuten`.
    *   **Nur Text extrahieren:**  Aktivieren Sie diese Checkbox, um nur den Textinhalt anstelle des gesamten HTML-Codes zu extrahieren und zu speichern.
    *   **Stopwörter:**  Optional: Geben Sie eine kommagetrennte Liste von zusätzlichen Stopwörtern für die Keyword-Extraktion an.
    *   **CSS-Selektoren (JSON):** Optional: Geben Sie einen JSON-String mit CSS-Selektoren an, um strukturierte Daten von den Webseiten zu extrahieren.
    *   **Datei speichern:**  Aktivieren Sie diese Checkbox, um den extrahierten Inhalt zusätzlich zur Datenbank in einer Datei zu speichern.
    *   **Verarbeitungsfunktion (Pfad):** Optional: Geben Sie den Pfad zu einer Python-Datei an, die eine benutzerdefinierte Verarbeitungsfunktion (`process_data`) enthält.
    *   **Task hinzufügen Button:**  Klicken Sie auf diesen Button, um den neuen Task zu erstellen und in der Datenbank zu speichern.

5.  **Datenbank Browser Oberfläche 🖥️⌨️ – Datenbankinhalte durchsuchen:**

    1.  **Datenbankbrowser starten:** Starten Sie die Streamlit Datenbankbrowser-Oberfläche über die Kommandozeile:

        ```bash
        streamlit run db_browser.py
        ```

        *   Die Datenbankbrowser-Oberfläche ist nun unter der Adresse `http://localhost:8501` erreichbar (kann je nach Streamlit Konfiguration variieren).

    2.  **API-Key eingeben:** Geben Sie auf der Startseite den benötigten API-Key ein, um sich zu authentifizieren.

    3.  **Suchparameter festlegen:**
        *   **Suchbegriff:** Geben Sie im Textfeld "Suchbegriff" den Suchbegriff ein, nach dem Sie in der Datenbank suchen möchten (z.B. ein Wort, eine URL, ein Teil eines Titels).
        *   **Suchfeld:** Wählen Sie im Dropdown-Menü "Suchfeld" das Feld aus, in dem gesucht werden soll. Verfügbare Optionen sind: `url`, `title`, `meta_description`, `text_content`, `domain`.

    4.  **Suche starten:** Klicken Sie auf den Button "Suchen", um die Datenbankabfrage mit den angegebenen Parametern zu starten.

    5.  **Suchergebnisse anzeigen:**
        *   **DataFrame-Anzeige:** Die Suchergebnisse werden als interaktiver Pandas DataFrame unterhalb des Suchformulars angezeigt. Die Tabelle enthält Spalten für `url`, `title`, `meta_description`, `domain` und (gekürzt) `text_content`.
        *   **Keine Ergebnisse:** Wenn keine Einträge gefunden werden, die dem Suchbegriff entsprechen, wird eine entsprechende Meldung "Keine Ergebnisse gefunden." angezeigt.
        *   **Fehlermeldungen:** Bei Fehlern während der Datenbankabfrage oder API-Kommunikation werden Fehlermeldungen oberhalb der Suchergebnisse angezeigt, um den Benutzer über Probleme zu informieren.

**Bedienungshinweise für die Admin- und Datenbankbrowser-Oberfläche:**

*   **API-Key erforderlich:**  Für den Zugriff auf die Funktionen der Admin- und Datenbankbrowser-Oberfläche ist die Eingabe eines gültigen API-Keys erforderlich. Stellen Sie sicher, dass die API-Keys korrekt in der `.env` Datei oder `config.yaml` konfiguriert sind und der API-Server läuft.
*   **Echtzeit-Aktualisierung:**  Änderungen an geplanten Tasks (Hinzufügen, Aktualisieren, Löschen) in der Admin-Oberfläche werden in Echtzeit in der Datenbank gespeichert und vom Scheduler berücksichtigt.
*   **Browser-Neuladen:**  In einigen Fällen kann es notwendig sein, die Seite im Browser neu zu laden, um sicherzustellen, dass die aktuellsten Daten und Task-Listen angezeigt werden.
*   **Zeitpläne und CSS-Selektoren:**  Achten Sie darauf, Zeitpläne im korrekten Format einzugeben und CSS-Selektoren als validen JSON-String zu formatieren, um Validierungsfehler zu vermeiden.
*   **Lange `text_content` Spalten:**  Im Datenbankbrowser wird die Spalte `text_content` aus Performance- und Darstellungsgründen auf die ersten 200 Zeichen gekürzt. Um den vollständigen Textinhalt anzuzeigen, verwenden Sie ein externes Datenbank-Tool oder passen Sie den Code der `db_browser.py` App an.

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
3.  Webseitenabruf (aiohttp primär, Selenium Fallback bei Bedarf) 🌐
4.  HTML-Parsing (Beautiful Soup) 🥣
5.  Datenextraktion (Text, Titel, Meta-Description, H1-Headings, Keywords, CSS-Daten) 📄
6.  Benutzerdefinierte Datenverarbeitung (optional) ⚙️
7.  Datenbank-Speicherung (SQLite) 💾
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
*   Datenbankinhalte mit Streamlit Datenbankbrowser durchsuchen ⌨️🖥️

## 7. Fehlerbehebung

**Häufige Fehlermeldungen und Lösungen:**

*   "Ungültige URL" ❌🌐 - Überprüfen Sie die eingegebene URL auf Korrektheit und Format. Stellen Sie sicher, dass die URL mit `http://` oder `https://` beginnt.
*   "Webseiteninhalt konnte nicht abgerufen werden" ❌ - Mögliche Ursachen: Webseite nicht erreichbar, Serverprobleme, Netzwerkprobleme, blockiert durch Firewall/Robot.txt. Überprüfen Sie die Webseite manuell im Browser. Erhöhen Sie ggf. `max_retries` und `retry_delay` in `config.yaml`.
*   "API-Key fehlt oder ist ungültig." ❌🔑 - Stellen Sie sicher, dass Sie einen gültigen API-Key im `X-API-Key` Header (API-Anfragen) oder im Streamlit UI eingegeben haben. Überprüfen Sie die API-Key Konfiguration in `.env` und `config.yaml`. Generieren Sie ggf. neue Keys mit `key_generator.py`.
*   "Rate Limit überschritten. Bitte warten Sie eine Minute." ⏳ - Die API ist ratenlimitiert. Reduzieren Sie die Anfragerate oder erhöhen Sie `rate_limit_requests_per_minute` in `config.yaml` (mit Vorsicht!).
*   "Ungültiges JSON-Format für CSS-Selektoren." ❌🧱 - Überprüfen Sie den JSON-String für CSS-Selektoren auf korrekte Syntax. Verwenden Sie einen JSON-Validator, um Fehler zu finden.
*   "Ungültiger Pfad zur Processing-Funktion" ❌⚙️ - Stellen Sie sicher, dass der angegebene Pfad zur Python-Datei der Processing-Funktion korrekt ist und die Datei existiert. Stellen Sie sicher, dass der Pfad relativ zum `processing_functions_dir` in `config.yaml` korrekt ist oder ein absoluter Pfad verwendet wird.
*   "Fehler beim Speichern in die Datenbank" ❌💾 - Mögliche Datenbankfehler. Überprüfen Sie die Datenbankdatei (`webdata.db`) auf Integrität und Berechtigungen. Prüfen Sie die Server-Logs auf detailliertere Datenbankfehlermeldungen.
*   "Fehler in der Datenverarbeitungsfunktion" ❌⚙️ - Überprüfen Sie die Log-Ausgabe auf Fehlermeldungen aus Ihrer benutzerdefinierten Processing-Funktion. Debuggen Sie die Funktion auf Fehler.
*   "Kritischer Datenbankfehler im Scheduled Mode. Programm wird beendet." ☠️💾 - Ein schwerwiegender Datenbankfehler ist aufgetreten, der den Scheduled Mode beeinträchtigt. Überprüfen Sie die Datenbankintegrität und -konfiguration. Starten Sie das Programm neu. Prüfen Sie die Logs auf detaillierte Fehlermeldungen.

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

A: API-Keys können in der `config.yaml` Datei unter `api_keys` als Liste von Strings oder sicherer über Umgebungsvariablen (siehe Abschnitt 3.1) konfiguriert werden. Der empfohlene Weg ist die Verwendung des `key_generator.py` Skripts (siehe Installationsschritt 7).

**F: Wie ändere ich das Rate Limit der API?**

A: Das Rate Limit (maximale Anfragen pro Minute) kann in der `config.yaml` Datei unter `rate_limit_requests_per_minute` konfiguriert werden.

**F: Wie lange werden Webseiten im Cache gespeichert?**

A: Die Gültigkeitsdauer des Caches (in Sekunden) kann in der `config.yaml` Datei unter `cache_expiry_seconds` konfiguriert werden. Standardmäßig sind es 600 Sekunden (10 Minuten).

**F: Wie kann ich geplante Tasks verwalten?**

A: Geplante Tasks können über die Streamlit Admin-Oberfläche (empfohlen) oder über die Web-API verwaltet werden (erstellen, aktualisieren, löschen, auflisten, manuell ausführen, Status abrufen).

**F: Wo werden die gescrapten Daten gespeichert?**

A: Die gescrapten Daten werden in einer SQLite-Datenbank gespeichert. Der Pfad zur Datenbankdatei kann in der `config.yaml` Datei unter `database_file` konfiguriert werden. Standardmäßig ist dies `webdata.db` im Projektverzeichnis.

**F: Kann ich nur Textinhalte extrahieren?**

A: Ja, Sie können nur Textinhalte extrahieren, indem Sie die Option `--text` in der Kommandozeile verwenden, `text_only=true` im Request Body für die API-Endpunkte `/fetch-html` und `/fetch-text` setzen oder die Checkbox "Nur Text extrahieren" in der Streamlit Admin-Oberfläche aktivieren.

**F: Wie kann ich benutzerdefinierte Stopwörter verwenden?**

A: Benutzerdefinierte Stopwörter können als kommagetrennte Liste über die Option `--stopwords` in der Kommandozeile, den Parameter `stopwords` in den API-Endpunkten `/fetch-html` und `/fetch-text` oder das Textfeld "Stopwörter" in der Streamlit Admin-Oberfläche angegeben werden.

**F: Sind CSS-Selektoren sicher zu verwenden?**

A: WebCrawler-Pro implementiert Sicherheitsprüfungen für CSS-Selektoren, um potenziell unsichere Selektoren zu erkennen und zu verhindern. Dennoch sollten Sie bei der Verwendung von CSS-Selektoren Vorsicht walten lassen und nur vertrauenswürdige Selektoren verwenden.

**F: Sind benutzerdefinierte Processing-Funktionen sicher?**

A: Benutzerdefinierte Processing-Funktionen können beliebigen Python-Code ausführen. Verwenden Sie diese Funktion nur mit Bedacht und stellen Sie sicher, dass Sie nur vertrauenswürdigen Code ausführen, um Sicherheitsrisiken zu vermeiden. WebCrawler-Pro validiert den Pfad zur Processing-Funktion, um unsichere Pfade zu verhindern.

**F: Unterstützt WebCrawler-Pro JavaScript-Rendering?**

A: Ja, WebCrawler-Pro verwendet `aiohttp` für schnelle Abrufe und Selenium und ChromeDriver als Fallback, um auch Webseiten mit dynamischen JavaScript-Inhalten abzurufen und zu verarbeiten.

## 9. Glossar

*   **API (Application Programming Interface):** 🌐 Eine Schnittstelle, die es Softwareanwendungen ermöglicht, miteinander zu kommunizieren. Im Kontext von WebCrawler-Pro ermöglicht die API den programmatischen Zugriff auf Web-Scraping-Funktionalitäten.
*   **CSS-Selektor:** 🧱 Ein Muster, das verwendet wird, um HTML-Elemente auf einer Webseite auszuwählen und zu formatieren oder Daten aus diesen Elementen zu extrahieren.
*   **ChromeDriver:** 🌐 Ein separates ausführbares Programm, das von Selenium verwendet wird, um Chrome-Browser zu steuern.
*   **JSON (JavaScript Object Notation):** 📄 Ein leichtgewichtiges Datenformat, das für den Datenaustausch im Web verwendet wird.
*   **Rate Limiting:** ⏳ Eine Technik zur Begrenzung der Anzahl von Anfragen, die ein Benutzer oder eine Anwendung innerhalb eines bestimmten Zeitraums an eine API senden kann. Dies dient dem Schutz vor Überlastung und Missbrauch.
*   **Caching:** 🗄️ Eine Technik zur Speicherung häufig abgerufener Daten (z.B. Webseiteninhalte) in einem temporären Speicher (Cache), um den Zugriff zu beschleunigen und die Last auf den ursprünglichen Datenquelle zu reduzieren.
*   **Scheduled Task (Geplanter Task):** ⏱️📝 Eine Aufgabe, die automatisch zu einem vordefinierten Zeitpunkt oder in regelmäßigen Intervallen ausgeführt wird. Im Kontext von WebCrawler-Pro sind geplante Tasks Web-Scraping-Aufgaben, die automatisch nach Zeitplan ausgeführt werden.
*   **Selenium:** 🌐 Ein Framework für die Automatisierung von Webbrowsern. WebCrawler-Pro verwendet Selenium als Fallback, um Webseiten dynamisch abzurufen und JavaScript-Inhalte zu rendern, falls der primäre Abruf mit `aiohttp` fehlschlägt.
*   **aiohttp:** 🚀 Eine Python-Bibliothek für asynchrone HTTP-Client-/Server-Kommunikation. WebCrawler-Pro verwendet `aiohttp` als primäre Methode für schnelle und effiziente Webseitenabrufe.

## 10. Kontakt und Support

**E-Mail:** 📧 support@ciphercore.de

**Webseite:** 🌐 www.ciphercore.de 

Bitte beschreiben Sie Ihr Problem/Anfrage detailliert.
