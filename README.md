# 🚀 **WebCrawler-Pro**

## 📌 **Einführung**
WebCrawler-Pro ist ein leistungsstarkes Werkzeug zur **automatischen Extraktion, Verarbeitung und Bereitstellung von Web-Daten** über eine API. Es kombiniert **Web-Scraping, Datenverarbeitung, API-Integration, Sicherheit und Task-Planung** in einem einzigen System. Die geplante Task-Ausführung und das Monitoring erfolgen direkt über die Datenbank.

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

📖 Diese Dokumentation beschreibt die **Installation, Konfiguration und Nutzung** des Programms.

---

## 🔧 **1. Installation**
### 📂 **1.1 Voraussetzungen**
📌 **Erforderliche Software:**
- 🐍 **Python 3.7 oder höher** *(empfohlen: 3.9+)*
- 📦 **pip** *(Python-Paketmanager, sollte mit Python installiert sein)*
- 🌐 **Google Chrome + ChromeDriver** *(für Selenium-basiertes Scraping)*
- 🧠 **NLTK Data:** *(Für Keyword-Extraktion: `python -m nltk.downloader stopwords`)*

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
**Weboberfläche**
```sh
streamlit run app.py -- --streamlit
```

![image](https://github.com/user-attachments/assets/d2b6b9aa-ebaa-4450-8870-0096207fb2e1)

---

## 🏁 **9. WebCrawler-Pro**
✅ **Automatisierte Task-Planung direkt aus der Datenbank**
✅ **Erweiterbare Datenverarbeitung durch `processing.py`**
✅ **Detaillierte Logging- & Sicherheitsmaßnahmen**
✅ **Einfache Konfiguration über `config.yaml` & `.env`**

🚀 **WebCrawler-Pro ist die ideale Lösung für produktives, sicheres und flexibles Web-Scraping!**

