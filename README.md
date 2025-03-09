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
*   **Sicherheit:** Robuste Maßnahmen zum Schutz vor Sicherheitslücken wie Path Traversal und CSS-Injection.
*   **Monitoring:** Detaillierte Statusberichte für geplante Aufgaben (einschließlich Start-/Endzeiten, letzter Ausführungszeit, nächster Ausführungszeit und Fehlermeldungen).
*   **Konfiguration:** Umfassende Konfiguration über YAML-Dateien und Umgebungsvariablen.


**2. Voraussetzungen**

Bevor du beginnst, stelle sicher, dass du Folgendes installiert hast:

*   **Python:** Python 3.7 oder höher (empfohlen: 3.9+).
*   **pip:** Python-Paketmanager (sollte mit Python installiert werden).
*   **Chrome:** Google Chrome-Browser (für Selenium) und ein kompatibler ChromeDriver.
*   **NLTK Data:**  Die `stopwords` sollten für die Keyword-Extraktion heruntergeladen sein (`nltk.download('stopwords')`).
*   **PyYAML:** Für die YAML-Konfiguration (`pip install pyyaml`).
*   **python-dotenv:** Für das Laden von Umgebungsvariablen aus der `.env`-Datei (`pip install python-dotenv`).
*   **Pydantic:** Für Datenvalidierung und -parsing (`pip install pydantic`).


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
*   **Umgebungsvariablen (`.env`-Datei):** Für sensible Informationen wie API-Keys.  Umgebungsvariablen überschreiben die YAML-Konfiguration.


**4.1 YAML-Konfigurationsdatei (`config.yaml`)**

Erstelle eine `config.yaml`-Datei im Hauptverzeichnis des Projekts (oder verwende die mitgelieferte Vorlage).  


**4.2 Umgebungsvariablen (`.env`-Datei)**

Erstelle eine `.env`-Datei im Hauptverzeichnis des Projekts. Umgebungsvariablen werden verwendet, um sensible Informationen wie API-Keys zu speichern. Das Programm liest Umgebungsvariablen, die mit `API_KEY_` beginnen, und fügt sie zu den in der `config.yaml`-Datei definierten API-Keys hinzu.


**5. Ausführen des Programms**

Das Programm kann in drei Modi ausgeführt werden:

*   **API-Modus:** Startet die Web-API.
*   **Kommandozeilenmodus:** Extrahiert Daten von einer einzelnen URL.
*   **Geplanter Modus:** Führt geplante Scraping-Aufgaben aus.

**5.1 API-Modus**

```bash
python app.py --api
```

**5.2 Kommandozeilenmodus**

```bash
python app.py [URL] [OPTIONS]
```

**5.3 Geplanter Modus**

```bash
python app.py
```

**6. API-Endpunkte**

*   Alle API-Endpunkte erfordern einen gültigen API-Key im `X-API-Key`-Header und unterliegen der Ratenbegrenzung.
*   Der Endpunkt `/api/v1/` bietet eine Beschreibung aller verfügbaren Endpunkte.

**7. Task-Planung**

Geplante Tasks werden über die API hinzugefügt, aktualisiert, gelöscht und verwaltet.  Details zu den JSON-Payloads für die API-Requests finden Sie in der Dokumentation des Endpunkts `/api/v1/`.


**8. Benutzerdefinierte Datenverarbeitung**

Benutzerdefinierte Verarbeitungsfunktionen müssen die Signatur `process_data(data)` haben und im Verzeichnis `processing_functions_dir` (wie in der `config.yaml` konfiguriert) abgelegt werden. Sicherheitshinweis: Seien Sie vorsichtig bei der Verwendung von benutzerdefinierten Verarbeitungsfunktionen und stellen Sie sicher, dass Sie nur vertrauenswürdigen Code ausführen.


**9. CSS-Selektoren**

CSS-Selektoren werden verwendet, um bestimmte Datenelemente von Webseiten zu extrahieren. Sicherheitshinweis:  Validieren Sie CSS-Selektoren sorgfältig, um Injection-Angriffe zu vermeiden. Verwenden Sie die Funktion `is_safe_css_selector`, um die Sicherheit von CSS-Selektoren zu überprüfen.


**10. Datenbankintegration**

Das Programm verwendet eine SQLite-Datenbank, um gescrapte Daten und geplante Tasks zu speichern. Der Datenbankpfad wird in der `config.yaml`-Datei konfiguriert.


**11. Sicherheit**

*   **API-Key-Authentifizierung:** Alle API-Endpunkte erfordern einen gültigen API-Key.
*   **Ratenbegrenzung:**  Die API-Nutzung ist ratenbegrenzt, um Missbrauch zu verhindern.
*   **Path Traversal-Schutz:**  Die Funktion `is_safe_path` verhindert Path Traversal-Angriffe.
*   **CSS-Injection-Schutz:**  Die Funktion `is_safe_css_selector` verhindert CSS-Injection-Angriffe.  Zusätzlich wird eine Whitelist für CSS-Eigenschaften verwendet.
*   **Whitelist für Verarbeitungsfunktionen:**  Nur Funktionen mit dem in der `config.yaml`-Datei konfigurierten Namen dürfen als Verarbeitungsfunktionen verwendet werden.

**12. Monitoring**

Der API-Endpunkt `/api/v1/scheduled-tasks/status` bietet eine Übersicht über den Status aller geplanten Tasks. Der Endpunkt `/api/v1/scheduled-tasks/[task_id]/status` liefert detaillierte Informationen zu einem bestimmten Task.

**13. Fehlerbehandlung**

Fehler werden protokolliert, und das Logging-Level kann in der `config.yaml`-Datei konfiguriert werden.

**14. Testen**

Das Programm enthält Unit-Tests für Sicherheitsfunktionen im Verzeichnis `tests`. Führen Sie `python -m unittest discover tests` aus, um die Tests auszuführen.

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


