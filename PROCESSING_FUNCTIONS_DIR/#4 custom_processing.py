# 4 processing_function.py
import csv
import json
import logging
import os
import re
import langdetect
import nltk
from bs4 import BeautifulSoup
import unicodedata

# Sicherstellen, dass NLTK-Module vorhanden sind
def ensure_nltk_resources():
    """Stellt sicher, dass die notwendigen NLTK-Ressourcen heruntergeladen sind."""
    resources = {"tokenizers/punkt": "punkt", "corpora/stopwords": "stopwords", "corpora/wordnet": "wordnet"}
    for path, resource in resources.items():
        try:
            nltk.data.find(path)
        except LookupError:
            nltk.download(resource)

ensure_nltk_resources()

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("german"))

# Konfiguration
TRAINING_DATA_FILE = os.environ.get('TRAINING_DATA_FILE', 'training_data.json')
CSV_OUTPUT_FILE = os.environ.get('CSV_OUTPUT_FILE', 'training_data.csv')
JSON_OUTPUT_DIR = os.environ.get("JSON_OUTPUT_DIR", "json_output")
MAX_TEXT_LENGTH = int(os.environ.get('MAX_TEXT_LENGTH', 1000))

# -------------------- Hilfsfunktionen --------------------

def clean_text(text):
    """Entfernt HTML-Tags und unnötige Leerzeichen aus dem Text.

    Args:
        text (str): Der zu bereinigende Text.

    Returns:
        str: Der bereinigte Text oder "Error" im Fehlerfall.  Die Länge des Textes wird durch MAX_TEXT_LENGTH begrenzt.
    """
    if not text:
        return ""
    try:
        text = BeautifulSoup(text, "html.parser").get_text()
        text = re.sub(r"\s+", " ", text).strip()
        return text[:MAX_TEXT_LENGTH]
    except Exception as e:
        logging.error(f"Fehler beim Cleanen des Textes: {e}")
        return "Error"

def preprocess_text(text):
    """Bereitet den Text für NLP-Training vor.

    Konvertiert in Kleinbuchstaben, entfernt Zahlen, Sonderzeichen, Stoppwörter und lemmatisiert die Wörter.

    Args:
        text (str): Der zu verarbeitende Text.

    Returns:
        str: Der verarbeitete Text oder "Error" im Fehlerfall.
    """
    try:
        text = unicodedata.normalize("NFKD", text.lower())
        text = re.sub(r"\d+", "", text)
        text = re.sub(r"[^\w\s]", "", text)
        tokens = word_tokenize(text)
        return " ".join([lemmatizer.lemmatize(w) for w in tokens if w not in stop_words])
    except Exception as e:
        logging.error(f"Fehler bei der Aufbereitung des Textes: {e}")
        return "Error"

def detect_language(text):
    """Erkennt die Sprache des Textes.

    Args:
        text (str): Der Text, dessen Sprache erkannt werden soll.

    Returns:
        str: Der Sprachcode (z.B. "de", "en") oder "unknown", wenn die Sprache nicht erkannt werden konnte.
    """
    if len(text) < 30:
        return "unknown"
    try:
        return langdetect.detect(text[:100])
    except Exception as e:
        logging.warning(f"Sprache konnte nicht erkannt werden: {e}. Verwende 'unknown'.")
        return "unknown"

# -------------------- Verbesserte Speicherfunktionen --------------------

def is_url_in_json(file_path, url):
    """Prüft, ob eine URL bereits in der JSON-Datei existiert.

    Args:
        file_path (str): Pfad zur JSON-Datei.
        url (str): Die zu prüfende URL.

    Returns:
        bool: True, wenn die URL bereits vorhanden ist, False sonst.
    """
    if not os.path.exists(file_path):
        return False
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return any(entry["url"] == url for entry in data)
    except (json.JSONDecodeError, FileNotFoundError):
        return False

def save_to_json(file_path, data):
    """Speichert die Daten als JSON-Liste.  Fügt Daten an eine bestehende Datei an oder erstellt eine neue.

    Args:
        file_path (str): Der Basisdateiname für die JSON-Datei. Der endgültige Pfad wird im JSON_OUTPUT_DIR liegen.
        data (dict): Die zu speichernden Daten als Dictionary.

    Returns:
        dict: Ein Dictionary mit dem Status und dem Dateipfad bei Erfolg, oder einem Fehlerstring bei Misserfolg.
    """
    try:
        os.makedirs(JSON_OUTPUT_DIR, exist_ok=True)
        file_path = os.path.join(JSON_OUTPUT_DIR, os.path.basename(file_path).replace(".csv", ".json"))

        existing_data = []
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    existing_data = json.load(f)
                except json.JSONDecodeError:
                    logging.error("Fehler beim Laden der JSON-Datei. Erstelle eine neue.")

        if any(entry["url"] == data["url"] for entry in existing_data):
            logging.info(f"URL bereits vorhanden: {data['url']}")
            return {"status": "skipped", "message": "URL existiert bereits"}

        existing_data.append(data)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=4)

        return {"status": "success", "file": file_path}
    except Exception as e:
        logging.exception(f"Fehler beim Speichern als JSON: {e}")
        return {"error": f"Fehler beim Speichern als JSON: {str(e)}"}

def save_to_csv(file_path, data):
    """Speichert die Daten als CSV.  Fügt Daten an eine bestehende Datei an oder erstellt eine neue mit Header.

    Args:
        file_path (str): Der Dateipfad für die CSV-Datei.
        data (list): Die zu speichernden Daten als Liste.

    Returns:
        dict: Ein Dictionary mit dem Status und dem Dateipfad bei Erfolg, oder einem Fehlerstring bei Misserfolg.
    """
    try:
        file_exists = os.path.exists(file_path)
        with open(file_path, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["URL", "Title", "Meta_Description", "Text", "Language", "Keywords"])
            writer.writerow(data)

        return {"status": "success", "file": file_path}
    except Exception as e:
        logging.exception(f"Fehler beim Speichern in CSV: {e}")
        return {"error": f"Fehler beim Speichern in CSV: {str(e)}"}

# -------------------- Hauptverarbeitung --------------------

def process_data(data):
    """Verarbeitet Webseitendaten und speichert sie für KI-Training.

    Extrahiert URL, Titel, Meta-Beschreibung, Textinhalt, Sprache und Keywords aus den Eingabedaten,
    bereinigt und verarbeitet den Text und speichert die Daten im angegebenen Format (JSON oder CSV).

    Args:
        data (dict): Ein Dictionary mit den Webseitendaten, die verarbeitet werden sollen.
                      Erwartet die Schlüssel "url", "title", "meta_description", "text_content" und "keywords".

    Returns:
        dict: Ein Dictionary mit dem Status und dem Dateipfad bei Erfolg, oder einem Fehlerstring bei Misserfolg.
    """
    logging.info("Starte KI-Trainingsdaten Verarbeitung...")

    try:
        # Daten extrahieren & verarbeiten
        url = data.get("url", "N/A")
        title = data.get("title", "N/A")
        meta_description = data.get("meta_description", "N/A")
        text_content = preprocess_text(clean_text(data.get("text_content", "")))
        language = detect_language(text_content)
        keywords = json.dumps(data.get("keywords", []), ensure_ascii=False)

        # Vorbereiten der Daten für die Speicherung
        processed_data = {
            "url": url,
            "title": title,
            "meta_description": meta_description,
            "text": text_content,
            "language": language,
            "keywords": keywords
        }

        # Speichern basierend auf Umgebungsvariable
        save_format = os.environ.get("SAVE_FORMAT", "json").lower()
        if save_format == "json":
            return save_to_json(TRAINING_DATA_FILE, processed_data)
        elif save_format == "csv":
            return save_to_csv(CSV_OUTPUT_FILE, [url, title, meta_description, text_content, language, keywords])
        else:
            logging.warning(f"Unbekanntes Speicherformat '{save_format}'. Standard: JSON")
            return save_to_json(TRAINING_DATA_FILE, processed_data)

    except Exception as e:
        logging.exception(f"Fehler bei der Verarbeitung der Trainingsdaten: {e}")
        return {"error": f"Fehler bei der Datenverarbeitung: {str(e)}"}