# 🚀 **WebCrawler-Pro**

## 📌 **Einführung**
WebCrawler-Pro ist ein leistungsstarkes Werkzeug zur **automatischen Extraktion, Verarbeitung und Bereitstellung von Web-Daten** über eine API. Es kombiniert **Web-Scraping, Datenverarbeitung, API-Integration, Sicherheit und Task-Planung** in einem einzigen System. Die geplante Task-Ausführung und das Monitoring erfolgen direkt über die Datenbank.  Zusätzlich bietet WebCrawler-Pro eine **intuitive Web-Oberfläche mit Streamlit**, um geplante Tasks komfortabel zu verwalten.

### 🔹 **Hauptfunktionen**
✅ **Web-Scraping mit Selenium** (automatisiertes Abrufen von Webseiteninhalten)
✅ **Gezielte Datenextraktion mit CSS-Selektoren** (inkl. Typkonvertierung & Datenbereinigung)
✅ **Datenverarbeitung mit benutzerdefinierten Funktionen** (`processing.py`)
✅ **RESTful API zur Bereitstellung der Daten** (mit detaillierten Fehlermeldungen)
✅ **Automatisierte Task-Planung aus der Datenbank** (mit Monitoring & manueller Ausführung über die API)
✅ **API-Authentifizierung per API-Key** 🔑
✅ **Ratenbegrenzung zum Schutz vor Missbrauch** 🛡️
✅ **Caching zur Leistungssteigerung** ⚡
✅ **Datenbankintegration mit SQLite** 🗄️ (mit Transaktionssicherheit)
✅ **Erweiterbare Sicherheitsmaßnahmen gegen Path Traversal & CSS-Injection**
✅ **Monitoring für geplante Tasks und API-Status über API-Endpunkte** 📊 (inkl. Start-/Endzeiten, Logs, Fehlerberichte, letzter/nächster Ausführungszeit)
✅ **Einfache Konfiguration über YAML-Dateien & Umgebungsvariablen** ⚙️
✅ **Web-Oberfläche mit Streamlit zur Taskverwaltung** 🖥️

📖 Diese Dokumentation beschreibt die **Installation, Konfiguration und Nutzung** des Programms.

---

## 🔧 **1. Installation**
### 📂 **1.1 Voraussetzungen**
📌 **Erforderliche Software:**
- 🐍 **Python 3.7 oder höher** *(empfohlen: 3.9+)*
- 📦 **pip** *(Python-Paketmanager, sollte mit Python installiert sein)*
- 🌐 **Google Chrome + ChromeDriver** *(für Selenium-basiertes Scraping)*
- 🧠 **NLTK Data:** *(Für Keyword-Extraktion: `python -m nltk.downloader stopwords`)*
- 🖥️ **Streamlit:** *(Für die Web-Oberfläche: `pip install streamlit`)*

### 📥 **1.2 Abhängigkeiten installieren**
Führe folgenden Befehl aus, um alle benötigten Pakete zu installieren:
```bash
pip install -r requirements.txt
```


---

## ⚙️ **2. Konfiguration**
Das Programm wird über **YAML-Dateien & Umgebungsvariablen** konfiguriert:
- 📄 **`config.yaml`** → Enthält Einstellungen für Scraping, API, Datenbank & Sicherheit.
- 🔑 **`.env` Datei** → Speichert API-Keys & andere sensible Informationen. *(Umgebungsvariablen haben Vorrang vor `config.yaml`.)*  API-Keys können auch direkt in `config.yaml` unter `api_keys` eingetragen werden.

### 🛠 **2.1 `config.yaml` (Beispiel)**
```yaml
scraping:
  user_agent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
  timeout: 10

database:
  type: sqlite
  path: "data/webcrawler.db"

security:
  api_key_required: true
  rate_limit: 100
```

### 🔑 **2.2 `.env` Datei (Beispiel)**
```ini
API_KEY_1=mein_geheimer_api_key_1
API_KEY_2=mein_geheimer_api_key_2
API_KEY_3=mein_geheimer_api_key_3
```

---

## ▶️ **3. Nutzung**
### 🌍 **3.1 API-Modus** *(Startet den API-Server)*
```bash
python app.py --api
```

### 🕵️ **3.2 Kommandozeilenmodus** *(Einzelnes Scraping ausführen)*
```bash
python app.py https://example.com [Optionen]
```

### ⏳ **3.3 Geplanter Modus** *(Automatische Tasks aus der Datenbank ausführen)*
```bash
python app.py
```
📌 **Hinweis:** Geplante Tasks werden aus der Datenbank (`webdata.db`, konfigurierbar in `config.yaml`) geladen und ausgeführt. 
---


## 🛠 **4. Benutzerdefinierte Datenverarbeitung (`processing.py`)**
📌 **Ermöglicht benutzerdefinierte Verarbeitung gescrapter Daten.**

**Beispiel:**
```python
def process_data(data: dict) -> dict:
    """
    Verarbeitet gescrapte Daten. Muss ein Dictionary zurückgeben.
    Falls `None` zurückgegeben wird, erscheint eine Warnung im Log.
    """
    if not isinstance(data, dict):
        return None

    processed_data = {k: v.strip() if isinstance(v, str) else v for k, v in data.items()}
    return processed_data
```

---

## 🔒 **5. Sicherheitshinweise**
📌 **Schutzmechanismen:**
- 🔑 **API-Key-Authentifizierung** *(API-Endpunkte erfordern einen API-Key im Header)*
- 🛡 **Ratenbegrenzung** *(Maximal 100 Anfragen pro Minute, konfigurierbar in `config.yaml`)*
- 🚨 **Path Traversal-Schutz** *(Verhindert unautorisierten Zugriff auf Dateien)*
- 🔍 **CSS-Selektor-Validierung** *(Unsichere Selektoren werden ignoriert & protokolliert)*

**Beispiel für ein Sicherheitslog:**
```sh
2025-03-09 14:43:19,238 - WARNING - Unsicherer CSS-Selektor erkannt: div[onclick*=alert]
```

---

## 📊 **6. Fehlerbehandlung & Logging**
📌 **Wo werden Fehler protokolliert?**
- 🖥 **Konsolenausgabe** *(Standard, für schnelle Fehleranalyse)*
- 🗂 **Log-Datei `logs/webcrawler.log`** *(falls aktiviert)*

**Log-Level:**
- ✅ **INFO** → Allgemeine Statusmeldungen
- ⚠️ **WARNING** → Sicherheitswarnungen
- ❌ **ERROR** → Kritische Fehler


## 📡 7. API-Endpunkte
📌 **Übersicht der wichtigsten API-Endpunkte (aktualisiert):**
- 🌐 `/api/v1/` → API Root mit Übersicht aller Endpunkte
- 📄 `/api/v1/fetch-html` → HTML-Inhalt abrufen (Parameter: `url`, `stopwords`, `css-selectors`, `save_file`, `processing_function_path`)
- 📄 `/api/v1/fetch-text` → Textinhalt abrufen (Parameter: `url`, `stopwords`, `css-selectors`, `save_file`, `processing_function_path`)
- 🔄 `/api/v1/scheduled-tasks` → Aufgabenverwaltung (GET, POST, PUT, DELETE)
- 🔄 `/api/v1/scheduled-tasks/<task_id>` → Einzelne Task verwalten (GET, PUT, DELETE)
- 📊 `/api/v1/scheduled-tasks/status` → Status aller geplanten Tasks
- 📊 `/api/v1/scheduled-tasks/<task_id>/status` → Status eines spezifischen Tasks  (inkl. letzter/nächster Ausführungszeit und Fehlermeldungen)
- 📊 `/api/v1/scheduled-tasks/<task_id>/run` → Manuelles Ausführen eines Tasks
- ✅ `/api/v1/health` → API Health Check


🔐 **Alle API-Endpunkte erfordern API-Authentifizierung!**

---
## **Weboberfläche**

Mit dem Befehl `streamlit run app.py -- --streamlit` starten Sie die Weboberfläche zur bequemen Verwaltung Ihrer Webcrawling-Tasks.  Sie benötigen hierfür einen gültigen API-Key.

**API-Key Eingabe:**

Nach dem Start der Weboberfläche werden Sie aufgefordert, Ihren API-Key einzugeben.  Dieser dient zur Authentifizierung und Autorisierung des Zugriffs auf die Funktionen der Weboberfläche. Geben Sie Ihren API-Key in das dafür vorgesehene Feld ein und bestätigen Sie mit Enter. Ein ungültiger API Key führt zu einer Fehlermeldung.

**Anzeige geplanter Tasks:**

Die Weboberfläche listet alle geplanten Tasks übersichtlich auf. Für jeden Task werden folgende Informationen angezeigt:

* **Task ID:** Eindeutige Identifikationsnummer des Tasks.
* **URL:** Die zu crawlende Webseite.
* **Zeitplan:**  Definiert, wann der Task ausgeführt wird (z.B. stündlich, täglich um 10:00, alle 30 Minuten).
* **Nur Text:**  Gibt an, ob nur der Textinhalt oder der gesamte HTML-Code extrahiert werden soll.
* **Stopwörter:**  Auflistung der Stopwörter, die bei der Keyword-Extraktion ignoriert werden.
* **CSS-Selektoren:**  Die verwendeten CSS-Selektoren zur gezielten Datenextraktion.
* **Datei speichern:**  Gibt an, ob die extrahierten Daten zusätzlich zur Datenbank in einer Datei gespeichert werden sollen.
* **Verarbeitungsfunktion:**  Pfad zur benutzerdefinierten Verarbeitungsfunktion (optional).
* **Status:**  Aktueller Status des Tasks (z.B. `pending`, `running`, `success`, `failure`).
* **Letzte Ausführung:**  Zeitstempel der letzten Ausführung.
* **Nächste Ausführung:**  Zeitstempel der nächsten geplanten Ausführung.
* **Fehlermeldung:**  Anzeige von etwaigen Fehlermeldungen bei der Ausführung des Tasks.


**Aktionen für jeden Task:**

* **Löschen:**  Über den Button "Task [ID] löschen" kann ein geplanter Task entfernt werden.
* **Sofort ausführen:** Mit dem Button "Task [ID] sofort ausführen" kann ein Task unabhängig vom Zeitplan manuell gestartet werden.  Der Status aktualisiert sich nach der Ausführung.

**Hinzufügen eines neuen Tasks:**

Im Bereich "Neuen Task hinzufügen" können Sie neue Crawling-Tasks erstellen.  Füllen Sie die folgenden Felder aus:

* **URL:**  Die URL der zu crawlenden Webseite.
* **Zeitplan:**  Definieren Sie den Ausführungszeitplan des Tasks. Gültige Formate sind: "stündlich", "täglich um HH:MM" oder "alle X minuten".
* **Nur Text extrahieren:** Aktivieren Sie diese Option, um nur den Textinhalt der Webseite zu extrahieren.
* **Stopwörter:**  Geben Sie optional eine kommagetrennte Liste von Stopwörtern ein.
* **CSS-Selektoren:** Fügen Sie optional CSS-Selektoren im JSON-Format hinzu, um bestimmte Daten von der Webseite zu extrahieren.
* **Datei speichern:**  Aktivieren Sie diese Option, um die extrahierten Daten in einer Datei zu speichern.
* **Verarbeitungsfunktion:** Geben Sie optional den Pfad zu einer benutzerdefinierten Verarbeitungsfunktion an.


Nach dem Ausfüllen der Felder klicken Sie auf "Task hinzufügen", um den neuen Task zu speichern und zu planen.  Die Weboberfläche aktualisiert sich automatisch und zeigt den neu hinzugefügten Task an.  Fehler bei der Eingabe werden direkt angezeigt.

```
```bash
streamlit run app.py -- --streamlit
```

![image](https://github.com/user-attachments/assets/d2b6b9aa-ebaa-4450-8870-0096207fb2e1)

---
---
## **Hier sind einige Beispieleingaben für die Streamlit-Weboberfläche deines WebCrawler-Pro**

**Beispiel 1: Einfacher Webseiten-Crawl**

* **URL:** `https://www.example.com`
* **Zeitplan:** `täglich um 10:00`
* **Nur Text extrahieren:** (deaktiviert)
* **Stopwörter:**
* **CSS-Selektoren:**
* **Datei speichern:** (aktiviert)
* **Verarbeitungsfunktion:**


Dieser Task crawlt täglich um 10:00 Uhr die Webseite `https://www.example.com` und speichert den gesamten HTML-Inhalt in einer Datei.  Es werden keine Stopwörter, CSS-Selektoren oder Verarbeitungsfunktionen verwendet.

**Beispiel 2: Text-Extraktion mit Stopwörtern**

* **URL:** `https://www.wikipedia.org`
* **Zeitplan:** `alle 60 minuten`
* **Nur Text extrahieren:** (aktiviert)
* **Stopwörter:** `und, die, der, das, ist`
* **CSS-Selektoren:**
* **Datei speichern:** (aktiviert)
* **Verarbeitungsfunktion:**


Dieser Task extrahiert stündlich den Textinhalt von `https://www.wikipedia.org`. Die angegebenen Stopwörter werden bei der Keyword-Extraktion ignoriert. Der extrahierte Text wird in einer Datei gespeichert.

**Beispiel 3: Datenextraktion mit CSS-Selektoren**

* **URL:** `https://www.amazon.de/`
* **Zeitplan:** `stündlich`
* **Nur Text extrahieren:** (deaktiviert)
* **Stopwörter:**
* **CSS-Selektoren:**
```json
{
  "product_title": "h2.a-size-mini a.a-link-normal span",
  "product_price": "span.a-price span.a-offscreen"
}
```
* **Datei speichern:** (deaktiviert)
* **Verarbeitungsfunktion:** `./PROCESSING_FUNCTIONS_DIR/#1 custom_processing.py`


Dieser Task crawlt stündlich Amazon und extrahiert Produkttitel und -preise mithilfe der angegebenen CSS-Selektoren. Die extrahierten Daten werden mit der angegebenen Verarbeitungsfunktion weiterverarbeitet und in der Datenbank gespeichert. Beachte, dass der Pfad zur Verarbeitungsfunktion relativ zum Ausführungsverzeichnis des Crawlers sein muss.


**Beispiel 4:  Kombination aller Funktionen**

* **URL:** `https://www.heise.de`
* **Zeitplan:** `täglich um 06:00`
* **Nur Text extrahieren:** (aktiviert)
* **Stopwörter:** `mit, von, am, im`
* **CSS-Selektoren:** `{"article_title": "h2 a"}`
* **Datei speichern:** (aktiviert)
* **Verarbeitungsfunktion:** `./PROCESSING_FUNCTIONS_DIR/#2 custom_processing.py` (oder ein anderer gültiger Pfad)


Dieser Task kombiniert alle verfügbaren Funktionen. Er crawlt täglich um 6:00 Uhr heise.de, extrahiert den Textinhalt, filtert die angegebenen Stopwörter, extrahiert Artikeltitel mithilfe des CSS-Selektors, speichert den Textinhalt in einer Datei und verarbeitet die Daten mit der angegebenen Funktion.

**Wichtig:**

* **Gültige Pfade für Verarbeitungsfunktionen:** Achte darauf, dass die Pfade zu den Verarbeitungsfunktionen korrekt und relativ zum Ausführungsverzeichnis des Crawlers angegeben sind.  Die Beispiele oben gehen davon aus, dass sich die `custom_processing.py` Dateien im Verzeichnis `PROCESSING_FUNCTIONS_DIR` befinden.
* **JSON-Format für CSS-Selektoren:** Die CSS-Selektoren müssen in einem gültigen JSON-Format angegeben werden.
* **Testen:** Teste die Eingaben gründlich, um sicherzustellen, dass sie die gewünschten Ergebnisse liefern.
---
## 🏁 **9. WebCrawler-Pro**
✅ **Automatisierte Task-Planung direkt aus der Datenbank**
✅ **Erweiterbare Datenverarbeitung durch `processing.py`**
✅ **Detaillierte Logging- & Sicherheitsmaßnahmen**
✅ **Einfache Konfiguration über `config.yaml` & `.env`**

🚀 **WebCrawler-Pro ist die ideale Lösung für produktives, sicheres und flexibles Web-Scraping!**

