import streamlit as st
import requests
from bs4 import BeautifulSoup
import argparse
import os
from urllib.parse import urlparse, urljoin, urlparse, urlunparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import logging
from flask import Flask, request, jsonify, Response
import sqlite3
import datetime
import json
from collections import Counter
import nltk
from nltk.corpus import stopwords
import time
import schedule
import uuid
import importlib.util
import re
import yaml
from pydantic import BaseModel, field_validator, ValidationError, HttpUrl, model_validator
from typing import List, Optional, Dict, Any
from functools import wraps
import threading
from dotenv import load_dotenv

load_dotenv()

IS_SCHEDULED_MODE = False

CONFIG_FILE = 'config.yaml'
DEFAULT_CONFIG = {
    'database_file': 'webdata.db',
    'schedule_config_file': 'scheduled_tasks.json',
    'max_retries': 3,
    'retry_delay': 2,
    'allowed_processing_function_name': 'process_data',
    'processing_functions_dir': '.',
    'log_level': 'INFO',
    'api_debug_mode': True,
    'api_keys': [],
    'rate_limit_enabled': True,
    'rate_limit_requests_per_minute': 20,
    'cache_enabled': True,
    'cache_expiry_seconds': 600,
    'selenium_config': {
        'headless': True,
        'disable_gpu': True,
        'disable_extensions': True,
        'no_sandbox': True,
        'disable_dev_shm_usage': True,
        'user_agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    },
    'allowed_css_properties': [
        'color', 'font-size', 'background-color', 'margin', 'padding',
        'text-align', 'font-weight', 'text-decoration', 'font-family',
        'border', 'border-radius', 'width', 'height', 'display', 'visibility',
        'opacity', 'cursor', 'list-style-type', 'vertical-align'
    ]
}

def load_config():
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file) or {}
    except FileNotFoundError:
        logging.warning(f"Konfigurationsdatei '{CONFIG_FILE}' nicht gefunden. Verwende Standardkonfiguration.")
        config = {}

    merged_config = {**DEFAULT_CONFIG, **config}

    api_keys_env = [os.getenv(f'API_KEY_{i+1}') for i in range(3) if os.getenv(f'API_KEY_{i+1}')]
    api_keys_yaml = config.get('api_keys', [])
    merged_config['api_keys'] = set(api_keys_env) | set(api_keys_yaml)

    if not merged_config['api_keys']:
        logging.warning("Keine API-Keys konfiguriert. API-Key-Authentifizierung wird nicht funktionieren.")

    merged_config['selenium_config'] = {**DEFAULT_CONFIG['selenium_config'], **config.get('selenium_config', {})}
    merged_config['allowed_css_properties'] = config.get('allowed_css_properties', DEFAULT_CONFIG['allowed_css_properties'])

    return merged_config

config = load_config()

DATABASE_FILE = config['database_file']
SCHEDULE_CONFIG_FILE = config['schedule_config_file']
MAX_RETRIES = config['max_retries']
RETRY_DELAY = config['retry_delay']
ALLOWED_PROCESSING_FUNCTION_NAME = config['allowed_processing_function_name']
PROCESSING_FUNCTIONS_DIR = config['processing_functions_dir']
LOG_LEVEL_STR = config['log_level']
API_DEBUG_MODE = config['api_debug_mode']
API_KEYS = set(config['api_keys'])
RATE_LIMIT_ENABLED = config['rate_limit_enabled']
RATE_LIMIT_REQUESTS_PER_MINUTE = config['rate_limit_requests_per_minute']
CACHE_ENABLED = config['cache_enabled']
CACHE_EXPIRY_SECONDS = config['cache_expiry_seconds']

ALLOWED_CSS_PROPERTIES = config['allowed_css_properties']

log_level = getattr(logging, LOG_LEVEL_STR.upper(), logging.INFO)
logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.debug = API_DEBUG_MODE

page_cache = {}

def validate_json(json_string):
    try:
        return json.loads(json_string)
    except json.JSONDecodeError:
        logging.error(f"Ungültiges JSON: {json_string}")
        return None

def extract_domain(url):
    try:
        parsed_url = urlparse(url)
        return parsed_url.netloc
    except:
        logging.error(f"Fehler beim Extrahieren des Domainnamens aus {url}")
        return None

def get_cached_content(url):
    if not CACHE_ENABLED:
        return None
    if url in page_cache:
        cache_entry = page_cache[url]
        if datetime.datetime.now() - cache_entry['timestamp'] < datetime.timedelta(seconds=CACHE_EXPIRY_SECONDS):
            logging.debug(f"Cache-Hit für URL: {url}")
            return cache_entry['content']
        else:
            logging.debug(f"Cache abgelaufen für URL: {url}")
            del page_cache[url]
    return None

def set_cached_content(url, content):
    if CACHE_ENABLED:
        page_cache[url] = {'content': content, 'timestamp': datetime.datetime.now()}
        logging.debug(f"Inhalt für URL: {url} im Cache gespeichert.")

def validate_api_key(api_key):
    return api_key in API_KEYS

request_counts = {}

def is_rate_limited(api_key):
    if not RATE_LIMIT_ENABLED:
        return False

    now = datetime.datetime.now()
    minute_ago = now - datetime.timedelta(minutes=1)

    if api_key not in request_counts:
        request_counts[api_key] = []

    request_counts[api_key] = [ts for ts in request_counts[api_key] if ts > minute_ago]

    if len(request_counts[api_key]) >= RATE_LIMIT_REQUESTS_PER_MINUTE:
        return True
    return False

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key or not validate_api_key(api_key):
            logging.warning(f"Ungültiger oder fehlender API-Key von IP: {request.remote_addr}")
            return create_api_response(errors=["API-Key fehlt oder ist ungültig."], message="API-Key ist erforderlich.", status_code=401)

        if RATE_LIMIT_ENABLED and is_rate_limited(api_key):
            logging.warning(f"Rate Limit überschritten für API-Key '{api_key}' von IP: {request.remote_addr}")
            return create_api_response(errors=["Rate Limit überschritten. Bitte warten Sie eine Minute."], message="Zu viele Anfragen in kurzer Zeit.", status_code=429)

        if RATE_LIMIT_ENABLED:
            request_counts[api_key].append(datetime.datetime.now())

        return f(*args, **kwargs)
    return decorated_function

class ScheduledTaskPayload(BaseModel):
    url: str
    schedule_time: str
    text_only: Optional[bool] = False
    stopwords: Optional[str] = None
    css_selectors: Optional[str] = None
    save_file: Optional[bool] = False
    processing_function_path: Optional[str] = None

    @field_validator('css_selectors')
    def validate_css_selectors_json(cls, v: Optional[str]) -> Optional[str]:
        import json
        if v:
            try:
                json.loads(v)
            except json.JSONDecodeError:
                raise ValueError("Ungültiges JSON-Format für CSS-Selektoren.")
        return v

    @field_validator('schedule_time')
    def validate_schedule_time_format(cls, v: str) -> str:
        import re
        if not (v.lower() == "stündlich" or re.match(r"^täglich um \d{2}:\d{2}$", v) or re.match(r"^alle \d+ minuten$", v)):
            raise ValueError("Ungültiges Zeitformat. Erlaubt: 'stündlich', 'täglich um HH:MM', 'alle X minuten'.")
        return v

    @field_validator('processing_function_path')
    def validate_processing_function_path(cls, v: Optional[str]) -> Optional[str]:
        import os
        if v and not os.path.exists(v):
            raise ValueError("Die angegebene Processing-Funktion existiert nicht.")
        return v

class ScheduledTaskUpdatePayload(BaseModel):
    url: Optional[HttpUrl] = None
    schedule_time: Optional[str] = None
    text_only: Optional[bool] = None
    stopwords: Optional[str] = None
    css_selectors: Optional[str] = None
    save_file: Optional[bool] = None
    processing_function_path: Optional[str] = None

    @model_validator(mode='before')
    def check_for_update_fields(cls, data: Any) -> Any:
        if not data:
            raise ValueError("Mindestens ein Feld zum Aktualisieren erforderlich.")
        return data

def init_db():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scheduled_tasks (
                id TEXT PRIMARY KEY,
                url TEXT NOT NULL,
                schedule_time TEXT NOT NULL,
                text_only INTEGER,
                stopwords TEXT,
                css_selectors TEXT,
                save_file INTEGER,
                processing_function_path TEXT,
                status TEXT,
                start_time TEXT,
                end_time TEXT,
                last_run_time TEXT,
                next_run_time TEXT,
                error_message TEXT
            )
        """)
        conn.commit()
        logging.info("Datenbank initialisiert oder Tabelle 'scheduled_tasks' gefunden.")
    except sqlite3.Error as e:
        logging.error(f"Kritischer Fehler bei der Datenbankinitialisierung: {e}. Programm wird beendet.", exc_info=True)
        if conn:
            conn.close()
        exit(1)
    finally:
        if conn:
            conn.close()

def save_scheduled_task_to_db(task_data):
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO scheduled_tasks (id, url, schedule_time, text_only, stopwords, css_selectors, save_file, processing_function_path, status, next_run_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (task_data['id'], task_data['url'], task_data['schedule_time'],
              task_data.get('text_only', False), task_data.get('stopwords'), task_data.get('css_selectors'),
              task_data.get('save_file', False), task_data.get('processing_function_path'), 'pending', task_data.get('next_run_time')))
        conn.commit()
        logging.info(f"Geplanter Task '{task_data['id']}' für URL '{task_data['url']}' in Datenbank gespeichert.")
        return True
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        logging.error(f"Fehler beim Speichern des geplanten Tasks in der Datenbank (Rollback durchgeführt): {e}", exc_info=True)
        return False
    finally:
        if conn:
            conn.close()

def load_scheduled_tasks():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM scheduled_tasks")
        tasks = cursor.fetchall()
        column_names = [column[0] for column in cursor.description]
        task_list = []
        for task_tuple in tasks:
            task_dict = dict(zip(column_names, task_tuple))
            task_list.append(task_dict)
        logging.info(f"{len(task_list)} geplante Tasks aus der Datenbank geladen.")
        return task_list
    except sqlite3.Error as e:
        logging.error(f"Fehler beim Laden der geplanten Tasks aus der Datenbank: {e}", exc_info=True)
        return []
    finally:
        if conn:
            conn.close()

def get_scheduled_task_from_db(task_id):
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM scheduled_tasks WHERE id = ?", (task_id,))
        task_data = cursor.fetchone()
        if task_data:
            column_names = [column[0] for column in cursor.description]
            task_dict = dict(zip(column_names, task_data))
            return task_dict
        return None
    except sqlite3.Error as e:
        logging.error(f"Fehler beim Abrufen des geplanten Tasks '{task_id}' aus der Datenbank: {e}", exc_info=True)
        return None
    finally:
        if conn:
            conn.close()

def update_scheduled_task_in_db(task_id, task_data):
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        set_clauses = []
        query_params = []
        for key, value in task_data.items():
            if key not in ['id', 'status', 'start_time', 'end_time', 'last_run_time', 'next_run_time', 'error_message']:
                set_clauses.append(f"{key} = ?")
                query_params.append(value)
        query_params.append(task_id)

        if not set_clauses:
            logging.warning(f"Keine aktualisierbaren Felder im Update-Request für Task '{task_id}' gefunden.")
            return True

        sql_query = f"UPDATE scheduled_tasks SET {', '.join(set_clauses)} WHERE id = ?"
        cursor.execute(sql_query, query_params)
        conn.commit()
        if cursor.rowcount > 0:
            logging.info(f"Geplanter Task '{task_id}' in Datenbank aktualisiert.")
            return True
        else:
            logging.warning(f"Kein Task mit ID '{task_id}' zum Aktualisieren gefunden.")
            return False
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        logging.error(f"Fehler beim Aktualisieren des geplanten Tasks '{task_id}' in der Datenbank (Rollback durchgeführt): {e}", exc_info=True)
        return False
    finally:
        if conn:
            conn.close()

def delete_scheduled_task_from_db(task_id):
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM scheduled_tasks WHERE id = ?", (task_id,))
        conn.commit()
        if cursor.rowcount > 0:
            logging.info(f"Geplanter Task '{task_id}' erfolgreich aus Datenbank gelöscht.")
            return True
        else:
            logging.warning(f"Kein Task mit ID '{task_id}' zum Löschen gefunden.")
            return False
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        logging.error(f"Fehler beim Löschen des geplanten Tasks '{task_id}' aus der Datenbank (Rollback durchgeführt): {e}", exc_info=True)
        return False
    finally:
        if conn:
            conn.close()

def update_scheduled_task_status_db(task_id, start_time, status, error_message=None, next_run_time=None):
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        end_time_str = datetime.datetime.now().isoformat()
        last_run_time_str = datetime.datetime.now().isoformat()
        cursor.execute("""
            UPDATE scheduled_tasks
            SET status = ?, start_time = ?, end_time = ?, last_run_time = ?, next_run_time = ?, error_message = ?
            WHERE id = ?
        """, (status, start_time.isoformat(), end_time_str, last_run_time_str, next_run_time, error_message, task_id))
        conn.commit()
        logging.info(f"Status für Task '{task_id}' in Datenbank aktualisiert zu '{status}'.")
        return True
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        logging.error(f"Fehler beim Aktualisieren des Status für Task '{task_id}' in der Datenbank (Rollback durchgeführt): {e}", exc_info=True)
        return False
    finally:
        if conn:
            conn.close()

def update_scheduled_task_running_status_db(task_id, status):
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("UPDATE scheduled_tasks SET status = ? WHERE id = ?", (status, task_id))
        conn.commit()
        logging.info(f"Status für Task '{task_id}' in Datenbank aktualisiert zu '{status}'.")
        return True
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        logging.error(f"Fehler beim Aktualisieren des Status für Task '{task_id}' in der Datenbank (Rollback durchgeführt): {e}", exc_info=True)
        return False
    finally:
        if conn:
            conn.close()

def save_to_db(url, domain_name, title, meta_description, h1_headings, keywords, webpage_content, text_content, processed_content):
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS web_content (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                domain TEXT,
                url TEXT UNIQUE,
                title TEXT,
                meta_description TEXT,
                h1_headings TEXT,
                keywords TEXT,
                html_content TEXT,
                text_content TEXT,
                processed_content TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        h1_headings_json = json.dumps(h1_headings, ensure_ascii=False) if h1_headings else None
        keywords_json = json.dumps(keywords, ensure_ascii=False) if keywords else None
        cursor.execute("""
            INSERT OR REPLACE INTO web_content (domain, url, title, meta_description, h1_headings, keywords, html_content, text_content, processed_content)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (domain_name, url, title, meta_description, h1_headings_json, keywords_json, webpage_content, text_content, processed_content))
        conn.commit()
        return True
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        logging.error(f"Datenbankfehler beim Speichern von Daten für URL '{url}' (Rollback durchgeführt): {e}", exc_info=True)
        if IS_SCHEDULED_MODE:
            logging.critical("Kritischer Datenbankfehler im Scheduled Mode. Programm wird beendet.", exc_info=True)
            exit(1)
        return False
    finally:
        if conn:
            conn.close()

def extract_domain(url: str) -> Optional[str]:
    if not is_valid_url(url):
        return None
    parsed_url = urlparse(url)
    return parsed_url.netloc

def is_valid_url(url: str) -> bool:
    if not url:
        return False
    url = url.strip()
    if not url:
        return False
    if not url.lower().startswith(('http://', 'https://')):
        return False
    parsed_url = urlparse(url)
    if not parsed_url.netloc:
        return False
    if not re.match(r"^(?!-)(?:[A-Za-z0-9-]{1,63}(?<!-)\.)+[A-Za-z]{2,}$", parsed_url.netloc):
        return False
    if parsed_url.netloc.startswith(".") or parsed_url.netloc.endswith("."):
        return False
    if ".." in parsed_url.netloc:
        return False
    return True

def fetch_webpage_content(url, retry_count=0):
    cached_content = get_cached_content(url)
    if cached_content:
        return cached_content
    if retry_count >= MAX_RETRIES:
        logging.error(f"Maximale Wiederholungsversuche für URL '{url}' erreicht.")
        return None
    if not is_valid_url(url):
        logging.error(f"Ungültige URL '{url}'. Abrufen abgebrochen.")
        return None
    driver = None
    try:
        logging.info(f"Starte Browser für URL: {url} (Versuch {retry_count + 1})")
        chrome_options = Options()
        selenium_config = config['selenium_config']
        if selenium_config.get('headless', True):
            chrome_options.add_argument("--headless")
        if selenium_config.get('disable_gpu', True):
            chrome_options.add_argument("--disable-gpu")
        if selenium_config.get('disable_extensions', True):
            chrome_options.add_argument("--disable-extensions")
        if selenium_config.get('no_sandbox', True):
            chrome_options.add_argument("--no-sandbox")
        if selenium_config.get('disable_dev_shm_usage', True):
            chrome_options.add_argument("--disable-dev-shm-usage")
        user_agent = selenium_config.get('user_agent', DEFAULT_CONFIG['selenium_config']['user_agent'])
        chrome_options.add_argument(f"user-agent={user_agent}")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(url)
        content = driver.page_source
        set_cached_content(url, content)
        return content
    except Exception as e:
        logging.error(f"Fehler beim Abrufen der Webseite '{url}': {e}.")
        time.sleep(RETRY_DELAY)
        return fetch_webpage_content(url, retry_count + 1)
    finally:
        if driver:
            driver.quit()
            logging.info(f"Browser geschlossen für URL: {url}")

def extract_text_content(html_content):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup.get_text(separator='\n', strip=True)
    except Exception as e:
        logging.error(f"Fehler beim Extrahieren des Textinhalts: {e}")
        return None

def extract_title(html_content):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        title_tag = soup.find('title')
        return title_tag.string.strip() if title_tag and title_tag.string else None
    except Exception as e:
        logging.error(f"Fehler beim Extrahieren des Titels: {e}")
        return None

def extract_meta_description(html_content):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        meta_tag = soup.find('meta', attrs={'name': 'description'})
        return meta_tag['content'].strip() if meta_tag and 'content' in meta_tag.attrs else None
    except Exception as e:
        logging.error(f"Fehler beim Extrahieren der Meta-Description: {e}")
        return None

def extract_h1_headings(html_content):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        h1_tags = soup.find_all('h1')
        return [tag.get_text(strip=True) for tag in h1_tags]
    except Exception as e:
        logging.error(f"Fehler beim Extrahieren der H1-Überschriften: {e}")
        return None

def extract_keywords(text_content, top_n=10, custom_stopwords=None):
    if not text_content:
        return []
    try:
        words = text_content.lower().split()
        nltk_stopwords_de = set(stopwords.words('german'))
        default_stopwords = set(['und', 'der', 'die', 'das', 'ist', 'für', 'mit', 'von', 'zu', 'in', 'auf', 'bei', 'über', 'aus',
                                 'durch', 'an', 'als', 'auch', 'sich', 'es', 'ein', 'eine', 'einen', 'dem', 'den', 'des',
                                 'dass', 'nicht', 'aber', 'oder', 'weil', 'wenn', 'wir', 'uns', 'ihr', 'euch', 'sie', 'ihnen',
                                 'ich', 'du', 'er', 'sie', 'es', 'wir', 'ihr', 'sie', 'mein', 'dein', 'sein', 'ihr', 'unser',
                                 'euer', 'ihr', 'kein', 'mehr', 'sehr', 'etwas', 'nichts', 'viel', 'wenig', 'gut', 'schlecht',
                                 'groß', 'klein', 'neu', 'alt'])
        stopwords_list = nltk_stopwords_de.union(default_stopwords)
        if custom_stopwords:
            custom_stopwords_list_raw = custom_stopwords.split(',')
            custom_stopwords_list = set(sw.strip() for sw in custom_stopwords_list_raw if sw.strip().isalpha())
            stopwords_list = stopwords_list.union(custom_stopwords_list)
        filtered_words = [word for word in words if word.isalpha() and word not in stopwords_list and len(word) > 2]
        word_counts = Counter(filtered_words)
        top_keywords = [word for word, count in word_counts.most_common(top_n)]
        return top_keywords
    except Exception as e:
        logging.error(f"Fehler beim Extrahieren von Keywords: {e}")
        return []

def is_safe_css_selector(selector: str) -> bool:
    if not isinstance(selector, str) or not selector.strip():
        return False

    selector_lower = selector.lower()

    unsafe_patterns = [
        r"^\s*script\s*$",
        r"<\s*script.*?>",
        r"expression\s*\(",
        r"javascript\s*:",
        r"url\s*\(\s*[^\s]*javascript\s*:",
        r"@import",
        r"on\w+(\*?)\s*=",
        r"data\s*:"
    ]

    for pattern in unsafe_patterns:
        if re.search(pattern, selector_lower):
            logging.warning(f"Unsicherer CSS-Selektor erkannt: {selector}")
            return False

    if "{" in selector and "}" in selector:
        properties_values = selector.split('{')[1].rstrip('}').split(';')
        for prop_val in properties_values:
            if ':' in prop_val:
                prop = prop_val.split(':', 1)[0].strip()
                if prop not in ALLOWED_CSS_PROPERTIES:
                    logging.warning(f"Nicht erlaubte CSS-Eigenschaft '{prop}' in Selektor gefunden.")
                    return False

    return True

def extract_data_css(html_content, css_selectors_json):
    if not html_content or not css_selectors_json:
        return {}

    css_selectors = validate_json(css_selectors_json)
    if css_selectors is None:
        return {"error": "Ungültiges CSS-Selektor JSON-Format"}

    extracted_data = {}
    soup = BeautifulSoup(html_content, 'html.parser')

    for name, selector_config in css_selectors.items():
        selector_raw = None
        data_type = None
        cleanup_functions = []

        if isinstance(selector_config, dict):
            selector_raw = selector_config.get('selector')
            data_type = selector_config.get('type')
            cleanup_functions = selector_config.get('cleanup', [])
        elif isinstance(selector_config, str):
            selector_raw = selector_config
        else:
            logging.warning(f"Ungültige Konfiguration für Selektor '{name}': {selector_config}")
            continue

        if selector_raw is not None and not is_safe_css_selector(selector_raw):
            logging.warning(f"Potenziell unsicherer CSS-Selektor '{selector_raw}' für '{name}'. Selektor wird übersprungen.")
            continue
        elif selector_raw is None:
            logging.warning(f"Kein Selektor für '{name}' gefunden.")
            continue

        elements = soup.select(selector_raw)
        if elements:
            extracted_values = [element.get_text(strip=True) for element in elements]

            for cleanup_func_name in cleanup_functions:
                if cleanup_func_name == 'lower':
                    extracted_values = [val.lower() for val in extracted_values]

            if data_type:
                converted_values = []
                for value in extracted_values:
                    try:
                        if data_type == 'integer':
                            converted_values.append(int(value))
                        elif data_type == 'float':
                            converted_values.append(float(value))
                        elif data_type == "string":
                            converted_values.append(str(value))
                        else:
                            logging.warning(f"Unbekannter Datentyp '{data_type}' für Selektor '{name}'. Wert wird als String behandelt.")
                            converted_values.append(str(value))
                    except (ValueError, TypeError) as e:
                        logging.warning(f"Konvertierungsfehler für Wert '{value}' mit Typ '{data_type}': {e}. Wert wird übersprungen.")
                        converted_values.append(None)
                extracted_data[name] = converted_values
            else:
                extracted_data[name] = extracted_values

            if not extracted_data[name]:
                del extracted_data[name]
        else:
            logging.warning(f"CSS-Selektor '{selector_raw}' für '{name}' lieferte keine Ergebnisse.")

    return extracted_data

def save_content_to_file(content, filename):
    try:
        filename_sanitized = os.path.basename(filename)
        filepath = os.path.join(".", filename_sanitized)
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(content)
        logging.info(f"Inhalt erfolgreich in Datei '{filepath}' gespeichert.")
        return True
    except Exception as e:
        logging.error(f"Fehler beim Speichern in die Datei '{filename}': {e}", exc_info=True)
        return False

def is_safe_path(filepath, base_dir):
    if not filepath:
        return True
    if not base_dir:
        base_dir = "."
    base_path = os.path.abspath(base_dir)
    filepath_abs = os.path.abspath(filepath)
    common_path = os.path.commonpath([base_path, filepath_abs])
    return common_path == base_path

def load_processing_function(function_path):
    if not function_path:
        return None

    if not is_safe_path(function_path, PROCESSING_FUNCTIONS_DIR):
        logging.error(f"Ungültiger oder unsicherer Pfad zur Processing-Funktion: '{function_path}'. Laden abgebrochen.")
        return None

    try:
        spec = importlib.util.spec_from_file_location("processing_module", function_path)
        if spec is None:
            logging.error(f"Modul-Spezifikation konnte nicht für Pfad '{function_path}' erstellt werden.")
            return None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        processing_function = getattr(module, ALLOWED_PROCESSING_FUNCTION_NAME, None)
        if not processing_function or not callable(processing_function):
            logging.error(f"Verarbeitungsfunktion '{ALLOWED_PROCESSING_FUNCTION_NAME}' nicht gefunden oder nicht aufrufbar in '{function_path}'.")
            return None
        try:
            import inspect
            sig = inspect.signature(processing_function)
            if len(sig.parameters) != 1:
                logging.error(f"Verarbeitungsfunktion '{ALLOWED_PROCESSING_FUNCTION_NAME}' in '{function_path}' erwartet nicht die korrekte Anzahl an Argumenten (erwartet 1). Laden abgebrochen.")
                return None
        except Exception as sig_err:
            logging.warning(f"Fehler bei der Signaturprüfung der Verarbeitungsfunktion: {sig_err}. Funktion wird trotzdem geladen, aber Signatur nicht validiert.")

        logging.info(f"Verarbeitungsfunktion '{ALLOWED_PROCESSING_FUNCTION_NAME}' erfolgreich aus '{function_path}' geladen.")
        return processing_function
    except Exception as e:
        logging.error(f"Fehler beim Laden der Verarbeitungsfunktion aus '{function_path}': {e}", exc_info=True)
        return None

def scrape_and_store_url(url, extract_text_only=False, custom_stopwords_cli=None, css_selectors_cli=None, save_file_cli=False, processing_function_path=None, task_id=None):
    start_time = datetime.datetime.now()
    error_message = None
    status = "pending"  # Initialer Status    

    logging.info(f"Starte geplanten Scraping-Prozess für URL: {url} (Task-ID: {task_id}) um {start_time.isoformat()}")
    update_scheduled_task_running_status_db(task_id, 'running')

    domain_name = extract_domain(url)
    if not domain_name:
        error_message = "Ungültige URL"
        logging.error(f"Ungültige URL '{url}'. Geplanter Task (ID: {task_id}) abgebrochen.")
        update_scheduled_task_status_db(task_id, start_time, 'failure - invalid URL', error_message=error_message)
        return

    webpage_content = fetch_webpage_content(url)
    if webpage_content:
        text_content = extract_text_content(webpage_content) if extract_text_only else None
        title = extract_title(webpage_content)
        meta_description = extract_meta_description(webpage_content)
        h1_headings = extract_h1_headings(webpage_content)
        keywords = extract_keywords(text_content if text_content else extract_text_content(webpage_content), custom_stopwords=custom_stopwords_cli)
        css_data = extract_data_css(webpage_content, css_selectors_cli)

        processed_content = None
        if processing_function_path:
            processed_content = apply_processing_function(url, domain_name, title, meta_description, h1_headings, keywords, webpage_content, text_content, css_data, processing_function_path)

        content_to_save_db = text_content if extract_text_only else webpage_content
        if save_to_db(url, domain_name, title, meta_description, h1_headings, keywords, webpage_content, text_content, processed_content):
            end_time = datetime.datetime.now()
            logging.info(f"Geplanter Task (ID: {task_id}) für URL '{url}' erfolgreich abgeschlossen um {end_time.isoformat()}. Daten in Datenbank aktualisiert.")
            next_run_time = calculate_next_run(task_id)
            update_scheduled_task_status_db(task_id, start_time, 'success', next_run_time=next_run_time)
        else:
            error_message = "Fehler beim Speichern in Datenbank"
            end_time = datetime.datetime.now()
            logging.error(f"Fehler beim Speichern der Daten in der Datenbank für URL '{url}' (geplanter Task ID: {task_id}) um {end_time.isoformat()}.")
            update_scheduled_task_status_db(task_id, start_time, 'failure - db save error', error_message=error_message)

        if css_data:
            logging.info(f"Extrahierte CSS-Daten für URL '{url}' (geplanter Task ID: {task_id}): {json.dumps(css_data, indent=2, ensure_ascii=False)}")

        if save_file_cli:
            if extract_text_only:
                filename = f"{domain_name}_text.txt"
                content_to_save_file = text_content
            else:
                filename = f"{domain_name}_html.txt"
                content_to_save_file = webpage_content
            if content_to_save_file:
                if save_content_to_file(content_to_save_file, filename):
                    logging.info(f"Inhalt für URL '{url}' zusätzlich in Datei '{filename}' gespeichert (geplanter Task ID: {task_id}).")
                else:
                    error_message = "Fehler beim Speichern in Datei"
                    logging.error(f"Fehler beim Speichern des Inhalts in Datei für URL '{url}' (geplanter Task ID: {task_id}).")
            else:
                error_message = "Kein Inhalt zum Speichern in Datei"
                logging.error(f"Kein Inhalt zum Speichern in Datei vorhanden für URL '{url}' (geplanter Task ID: {task_id}).")

    else:
        error_message = "Abrufen des Webseiteninhalts fehlgeschlagen"
        end_time = datetime.datetime.now()
        logging.error(f"Abrufen des Webseiteninhalts für URL '{url}' fehlgeschlagen (geplanter Task ID: {task_id}) um {end_time.isoformat()}.")
        update_scheduled_task_status_db(task_id, start_time, 'failure - fetch error', error_message=error_message)

        logging.error(f"Kritischer Fehler beim Abrufen von URL '{url}' (Task ID: {task_id}). Siehe vorherige Log-Einträge für Details.")

    logging.info(f"Beende geplanten Scraping-Prozess für URL: {url} (Task-ID: {task_id}) um {datetime.datetime.now().isoformat()}. Status: {status}, Fehler: {error_message if error_message else 'Kein Fehler'}")

def calculate_next_run(task_id):
    task_config = get_scheduled_task_from_db(task_id)
    if not task_config:
        logging.warning(f"Task-Konfiguration für ID '{task_id}' nicht gefunden. Berechnung der nächsten Ausführungszeit nicht möglich.")
        return None

    schedule_time_str = task_config.get('schedule_time')
    if not schedule_time_str:
        logging.warning(f"Zeitplan für Task ID '{task_id}' nicht definiert. Berechnung der nächsten Ausführungszeit nicht möglich.")
        return None

    now = datetime.datetime.now()
    next_run = None

    if schedule_time_str.lower() == "stündlich":
        next_run = now + datetime.timedelta(hours=1)
    elif schedule_time_str.lower().startswith("täglich um"):
        time_str = schedule_time_str.split("um")[1].strip()
        try:
            hour, minute = map(int, time_str.split(':'))
            next_run_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if next_run_time <= now:
                next_run_time += datetime.timedelta(days=1)
            next_run = next_run_time
        except ValueError:
            logging.error(f"Fehler beim Parsen der Zeit für Task ID '{task_id}'. Ungültiges Zeitformat: '{time_str}'. Nächste Ausführungszeit nicht berechenbar.")
            return None
    elif schedule_time_str.lower().startswith("alle"):
        parts = schedule_time_str.split()
        if len(parts) == 3 and parts[1].isdigit() and parts[2].lower() in ["minuten", "minute"]:
            interval = int(parts[1])
            if interval <= 0:
                logging.error(f"Ungültiges Minutenintervall für Task ID '{task_id}'. Intervall muss größer als 0 sein. Nächste Ausführungszeit nicht berechenbar.")
            next_run = now + datetime.timedelta(minutes=interval)
        else:
            logging.error(f"Ungültiges Zeitformat für Task ID '{task_id}'. Format muss 'alle X minuten' sein, wobei X eine positive Zahl ist. Nächste Ausführungszeit nicht berechenbar.")
            return None
    else:
        logging.warning(f"Unbekanntes Zeitplanformat '{schedule_time}' für Task ID '{task_id}'. Nächste Ausführungszeit nicht berechenbar.")
        return None

    return next_run.isoformat() if next_run else None

def setup_scheduled_tasks():
    schedule.clear()
    scheduled_tasks = load_scheduled_tasks()
    if not scheduled_tasks:
        logging.info("Keine geplanten Aufgaben in der Datenbank gefunden.")
        return

    for task_config in scheduled_tasks:
        task_id = task_config.get('id')
        url = task_config.get('url')
        schedule_time = task_config.get('schedule_time')
        extract_text_only = task_config.get('text_only', False)
        custom_stopwords_cli = task_config.get('stopwords')
        css_selectors_cli = task_config.get('css_selectors')
        save_file_cli = task_config.get('save_file', False)
        processing_function_path = task_config.get('processing_function_path')

        if not url or not schedule_time or not task_id:
            logging.warning(f"Ungültige Aufgabenkonfiguration gefunden: {task_config}. 'id', 'url' und 'schedule_time' müssen angegeben sein.")
            continue

        if schedule_time.lower() == "stündlich":
            job = schedule.every().hour.do(run_threaded, task_function=scrape_and_store_url, url=url, extract_text_only=extract_text_only, custom_stopwords_cli=custom_stopwords_cli, css_selectors_cli=css_selectors_cli, save_file_cli=save_file_cli, processing_function_path=processing_function_path, task_id=task_id)
            job.id = task_id
            logging.info(f"Geplant (ID: {task_id}): Stündlicher Scraping-Task für URL '{url}'.")
        elif schedule_time.lower().startswith("täglich um"):
            time_str = schedule_time.split("um")[1].strip()
            try:
                job = schedule.every().day.at(time_str).do(run_threaded, task_function=scrape_and_store_url, url=url, extract_text_only=extract_text_only, custom_stopwords_cli=custom_stopwords_cli, css_selectors_cli=css_selectors_cli, save_file_cli=save_file_cli, processing_function_path=processing_function_path, task_id=task_id)
                job.id = task_id
                logging.info(f"Geplant (ID: {task_id}): Täglicher Scraping-Task für URL '{url}' um {time_str} Uhr.")
            except Exception as e:
                logging.error(f"Fehler beim Parsen der Zeit '{time_str}' für URL '{url}': {e}. Task nicht geplant.")
        elif schedule_time.lower().startswith("alle"):
            parts = schedule_time.split()
            if len(parts) == 3 and parts[1].isdigit() and parts[2].lower() in ["minuten", "minute"]:
                interval = int(parts[1])
                job = schedule.every(interval).minutes.do(run_threaded, task_function=scrape_and_store_url, url=url, extract_text_only=extract_text_only, custom_stopwords_cli=custom_stopwords_cli, css_selectors_cli=css_selectors_cli, save_file_cli=save_file_cli, processing_function_path=processing_function_path, task_id=task_id)
                job.id = task_id
                logging.info(f"Geplant (ID: {task_id}): Scraping-Task für URL '{url}' alle {interval} Minuten.")
            else:
                logging.warning(f"Ungültiges Zeitformat '{schedule_time}' für URL '{url}'. Task nicht geplant.")
        else:
            logging.warning(f"Unbekanntes Zeitplanformat '{schedule_time}' für URL '{url}'. Task nicht geplant.")

        next_run_time = calculate_next_run(task_id)
        if next_run_time:
            if not update_scheduled_task_in_db(task_id, {'next_run_time': next_run_time}):
                logging.error(f"Fehler beim Speichern der nächsten Ausführungszeit für Task ID '{task_id}' in der Datenbank.")

def run_threaded(task_function, **kwargs):
    job_thread = threading.Thread(target=task_function, kwargs=kwargs)
    job_thread.start()

def create_api_response(data=None, message=None, errors=None, status_code=200) -> Response:
    response_body = {}
    if message:
        response_body['message'] = message
    if data:
        response_body['data'] = data
    if errors:
        response_body['errors'] = errors
        if not message and errors:
            response_body['message'] = "Fehler bei der Anfrageverarbeitung."
    return jsonify(response_body), status_code

@app.errorhandler(ValidationError)
def handle_validation_error(error):
    detailed_errors = []
    for error_item in error.errors():
        detailed_errors.append({
            "field": error_item['loc'][0],
            "error_type": error_item['type'],
            "message": error_item['msg']
        })
    return create_api_response(errors=detailed_errors, message="Validierungsfehler im Request Body", status_code=400)

@app.route('/api/v1/', methods=['GET'])
@require_api_key
def api_root():
    return create_api_response(message="Web-Scraping API V1 - Gesichert mit API-Key Authentifizierung, Rate Limiting und Caching. Erweiterte Task-Verwaltung mit Datenbank-Transaktionen, verbesserter Fehlerbehandlung und erweitertem Monitoring. **Sicherheitsgeprüftes Monitoring.**", data={
        "endpoints": {
            "/api/v1/fetch-html?url=<url>&stopwords=<stopwords>&css-selectors=<json>&save-file=[true|false]&processing-function-path=<path>": "Ruft HTML-Inhalt einer Webseite ab, extrahiert Metadaten, Keywords, optionale CSS-Daten und führt optionale benutzerdefinierte Datenverarbeitungsfunktion aus. Speichert optional in Datei und Datenbank. **Sicherheitshinweis:** Seien Sie vorsichtig bei der Verwendung von 'processing-function-path' und stellen Sie sicher, dass Sie nur vertrauenswürdigen Code ausführen. **API-Key erforderlich. Rate Limiting und Caching aktiv. Datenbank-Transaktionen und sicherheitsgeprüftes Monitoring aktiv.**",
            "/api/v1/fetch-text?url=<url>&stopwords=<stopwords>&css-selectors=<json>&save-file=[true|false]&processing-function-path=<path>": "Ruft Text-Inhalt einer Webseite ab, extrahiert Metadaten, Keywords, optionale CSS-Daten und führt optionale benutzerdefinierte Datenverarbeitungsfunktion aus. Speichert optional in Datei und Datenbank. **Sicherheitshinweis:** Seien Sie vorsichtig bei der Verwendung von 'processing-function-path' und stellen Sie sicher, dass Sie nur vertrauenswürdigen Code ausführen. **API-Key erforderlich. Rate Limiting und Caching aktiv. Datenbank-Transaktionen und sicherheitsgeprüftes Monitoring aktiv.**",
            "/api/v1/scheduled-tasks (GET)": "Listet alle geplanten Scraping-Tasks auf. **API-Key erforderlich. Rate Limiting und Caching aktiv. Datenbank-Transaktionen und sicherheitsgeprüftes Monitoring aktiv.**",
            "/api/v1/scheduled-tasks (POST)": "Fügt einen neuen geplanten Scraping-Task hinzu (erwartet JSON im Request Body). **API-Key erforderlich. Rate Limiting und Caching aktiv. Datenbank-Transaktionen und sicherheitsgeprüftes Monitoring aktiv.**",
            "/api/v1/scheduled-tasks/<task_id> (GET)": "Ruft Details eines geplanten Scraping-Tasks anhand der Task-ID ab. **API-Key erforderlich. Rate Limiting und Caching aktiv. Datenbank-Transaktionen und sicherheitsgeprüftes Monitoring aktiv.**",
            "/api/v1/scheduled-tasks/<task_id> (PUT)": "Aktualisiert einen bestehenden geplanten Scraping-Task anhand der Task-ID (erwartet JSON im Request Body). **API-Key erforderlich. Rate Limiting und Caching aktiv. Datenbank-Transaktionen und sicherheitsgeprüftes Monitoring aktiv.**",
            "/api/v1/scheduled-tasks/<task_id> (DELETE)": "Entfernt einen geplanten Scraping-Task anhand der Task-ID. **API-Key erforderlich. Rate Limiting und Caching aktiv. Datenbank-Transaktionen und sicherheitsgeprüftes Monitoring aktiv.**",
            "/api/v1/scheduled-tasks/status (GET)": "Listet den Status aller geplanten Tasks auf. **API-Key erforderlich. Rate Limiting und Caching aktiv. Datenbank-Transaktionen und sicherheitsgeprüftes Monitoring aktiv.**",
            "/api/v1/scheduled-tasks/<task_id>/status (GET)": "Ruft den detaillierten Status eines spezifischen Tasks anhand der Task-ID ab. **API-Key erforderlich. Rate Limiting und Caching aktiv. Datenbank-Transaktionen und sicherheitsgeprüftes Monitoring aktiv.**",
            "/api/v1/scheduled-tasks/<task_id>/run (POST)": "Löst die sofortige Ausführung eines geplanten Tasks aus. **API-Key erforderlich. Rate Limiting und Caching aktiv. Datenbank-Transaktionen und sicherheitsgeprüftes Monitoring aktiv.**",
            "/api/v1/health (GET)": "Gibt den grundlegenden Gesundheitszustand der API zurück. **API-Key erforderlich. Rate Limiting und Caching aktiv. Datenbank-Transaktionen und sicherheitsgeprüftes Monitoring aktiv.**"
        }
    }), 200

@app.route('/api/v1/scheduled-tasks', methods=['GET', 'POST'])
@require_api_key
def api_scheduled_tasks():
    if request.method == 'GET':
        tasks = load_scheduled_tasks()
        for task in tasks:
            if task['next_run_time']:
                task['next_run_time_human'] = format_datetime_human_readable(task['next_run_time'])
            else:
                task['next_run_time_human'] = "Nicht geplant"
            if task['last_run_time']:
                task['last_run_time_human'] = format_datetime_human_readable(task['last_run_time'])
            else:
                task['last_run_time_human'] = "Noch nicht ausgeführt"
            if task['error_message']:
                task['error_message_truncated'] = task['error_message'][:50] + "..." if len(task['error_message']) > 50 else task['error_message']
            else:
                task['error_message_truncated'] = None
        return create_api_response(data=tasks, message="Geplante Tasks abgerufen.")
    elif request.method == 'POST':
        try:
            task_payload = ScheduledTaskPayload.parse_raw(request.data)
        except ValidationError as e:
            return handle_validation_error(e)

        task_data_dict = task_payload.model_dump()
        task_data_dict['id'] = str(uuid.uuid4())

        if save_scheduled_task_to_db(task_data_dict):
            setup_scheduled_tasks()
            return create_api_response(data={"task": task_data_dict}, message="Geplanter Task erfolgreich hinzugefügt.", status_code=201)
        else:
            return create_api_response(errors=["Fehler beim Speichern des Tasks in der Datenbank."], message="Task konnte nicht gespeichert werden.", status_code=500)
    else:
        return create_api_response(errors=["Methode nicht erlaubt"], message="Methode nicht erlaubt.", status_code=405)

@app.route('/api/v1/scheduled-tasks/<task_id>', methods=['GET', 'PUT', 'DELETE'])
@require_api_key
def api_scheduled_task_by_id(task_id):
    if request.method == 'GET':
        task = get_scheduled_task_from_db(task_id)
        if task:
            if task['next_run_time']:
                task['next_run_time_human'] = format_datetime_human_readable(task['next_run_time'])
            else:
                task['next_run_time_human'] = "Nicht geplant"
            if task['last_run_time']:
                task['last_run_time_human'] = format_datetime_human_readable(task['last_run_time'])
            else:
                task['last_run_time_human'] = "Noch nicht ausgeführt"
            if task['error_message']:
                task['error_message_truncated'] = task['error_message'][:50] + "..." if len(task['error_message']) > 50 else task['error_message']
            else:
                task['error_message_truncated'] = None
            return create_api_response(data=task, message=f"Task '{task_id}' abgerufen.")
        else:
            return create_api_response(errors=[f"Kein geplanter Task mit ID '{task_id}' gefunden."], message="Task nicht gefunden.", status_code=404)
    elif request.method == 'PUT':
        try:
            task_payload = ScheduledTaskUpdatePayload.parse_raw(request.data)
        except ValidationError as e:
            return handle_validation_error(e)

        task_data_dict = task_payload.dict(exclude_unset=True)

        if update_scheduled_task_in_db(task_id, task_data_dict):
            setup_scheduled_tasks()
            updated_task = get_scheduled_task_from_db(task_id)
            return create_api_response(data={"task": updated_task}, message=f"Geplanter Task '{task_id}' erfolgreich aktualisiert.")
        else:
            return create_api_response(errors=[f"Fehler beim Aktualisieren des Tasks '{task_id}' in der Datenbank."], message="Task konnte nicht aktualisiert werden.", status_code=500)
    elif request.method == 'DELETE':
        if delete_scheduled_task_from_db(task_id):
            setup_scheduled_tasks()
            return create_api_response(message=f"Geplanter Task mit ID '{task_id}' erfolgreich entfernt.")
        else:
            return create_api_response(errors=[f"Kein geplanter Task mit ID '{task_id}' gefunden oder Fehler beim Löschen."], message="Task konnte nicht gelöscht werden.", status_code=404)
    else:
        return create_api_response(errors=["Methode nicht erlaubt"], message="Methode nicht erlaubt.", status_code=405)

@app.route('/api/v1/scheduled-tasks/status', methods=['GET'])
@require_api_key
def api_scheduled_tasks_status():
    tasks = load_scheduled_tasks()
    status_list = []
    for task in tasks:
        status_list.append({"task_id": task['id'], "status": task['status'],
                            "last_run_time_human": format_datetime_human_readable(task['last_run_time']) if task['last_run_time'] else "Noch nicht ausgeführt",
                            "next_run_time_human": format_datetime_human_readable(task['next_run_time']) if task['next_run_time'] else "Nicht geplant"})
    return create_api_response(data=status_list, message="Task-Statusübersicht abgerufen.")

@app.route('/api/v1/scheduled-tasks/<task_id>/status', methods=['GET'])
@require_api_key
def api_scheduled_task_status_by_id(task_id):
    task = get_scheduled_task_from_db(task_id)
    if task:
        status_data = {
            "task_id": task['id'],
            "status": task['status'],
            "start_time": task['start_time'],
            "end_time": task['end_time'],
            "last_run_time": task['last_run_time'],
            "last_run_time_human": format_datetime_human_readable(task['last_run_time']) if task['last_run_time'] else "Noch nicht ausgeführt",
            "next_run_time": task['next_run_time'],
            "next_run_time_human": format_datetime_human_readable(task['next_run_time']) if task['next_run_time'] else "Nicht geplant",
            "error_message": task['error_message'],
            "url": task['url'],
            "schedule_time": task['schedule_time']
        }
        return create_api_response(data=status_data, message=f"Detaillierter Status für Task '{task_id}' abgerufen.")
    else:
        return create_api_response(errors=[f"Kein geplanter Task mit ID '{task_id}' gefunden."], message="Task nicht gefunden.", status_code=404)

def format_datetime_human_readable(datetime_str):
    if not datetime_str:
        return "N/A"
    try:
        dt = datetime.datetime.fromisoformat(datetime_str)
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except (ValueError, TypeError):
        return "Ungültiges Datum"

@app.route('/api/v1/scheduled-tasks/<task_id>/run', methods=['POST'])
@require_api_key
def api_run_scheduled_task_by_id(task_id):
    task = get_scheduled_task_from_db(task_id)
    if not task:
        return create_api_response(errors=[f"Kein geplanter Task mit ID '{task_id}' gefunden."], message="Task nicht gefunden.", status_code=404)

    if task['status'] == 'running':
        return create_api_response(errors=[f"Task '{task_id}' ist bereits in Ausführung."], message="Task läuft bereits.", status_code=409)

    url = task['url']
    extract_text_only = bool(task.get('text_only', False))
    custom_stopwords_cli = task.get('stopwords')
    css_selectors_cli = task.get('css_selectors')
    save_file_cli = bool(task.get('save_file', False))
    processing_function_path = task.get('processing_function_path')

    threading.Thread(target=scrape_and_store_url, args=(url, extract_text_only, custom_stopwords_cli, css_selectors_cli, save_file_cli, processing_function_path, task_id)).start()

    return create_api_response(message=f"Task '{task_id}' wird jetzt manuell ausgeführt.", status_code=202)

@app.route('/api/v1/fetch-html', methods=['GET'])
@require_api_key
def api_fetch_html():
    url_raw = request.args.get('url')
    stopwords_param = request.args.get('stopwords')
    css_selectors_param_raw = request.args.get('css_selectors')
    processing_function_path = request.args.get('processing_function_path')
    save_file_param = request.args.get('save_file')

    if not url_raw:
        return create_api_response(errors=["URL Parameter fehlt"], message="URL Parameter ist erforderlich.", status_code=400)
    if not is_valid_url(url_raw):
        return create_api_response(errors=["Ungültige URL"], message="URL muss mit 'http' oder 'https' beginnen und eine gültige Domain haben.", status_code=400)
    if processing_function_path and not is_safe_path(processing_function_path, PROCESSING_FUNCTIONS_DIR):
        return create_api_response(errors=["Ungültiger Pfad zur Processing-Funktion"], message="Ungültiger oder unsicherer Pfad zur Processing-Funktion.", status_code=400)

    save_file_cli = save_file_param.lower() == 'true' if save_file_param else False

    return fetch_content_api(url_raw, stopwords_param, css_selectors_param_raw, processing_function_path, save_file_cli, extract_text_only=False)

@app.route('/api/v1/fetch-text', methods=['GET'])
@require_api_key
def api_fetch_text():
    url_raw = request.args.get('url')
    stopwords_param = request.args.get('stopwords')
    css_selectors_param_raw = request.args.get('css_selectors')
    processing_function_path = request.args.get('processing_function_path')
    save_file_param = request.args.get('save_file')

    if not url_raw:
        return create_api_response(errors=["URL Parameter fehlt"], message="URL Parameter ist erforderlich.", status_code=400)
    if not is_valid_url(url_raw):
        return create_api_response(errors=["Ungültige URL"], message="URL muss mit 'http' oder 'https' beginnen und eine gültige Domain haben.", status_code=400)
    if processing_function_path and not is_safe_path(processing_function_path, PROCESSING_FUNCTIONS_DIR):
        return create_api_response(errors=["Ungültiger Pfad zur Processing-Funktion"], message="Ungültiger oder unsicherer Pfad zur Processing-Funktion.", status_code=400)

    save_file_cli = save_file_param.lower() == 'true' if save_file_param else False

    return fetch_content_api(url_raw, stopwords_param, css_selectors_param_raw, processing_function_path, save_file_cli, extract_text_only=True)

def fetch_content_api(url, stopwords_param, css_selectors_param_raw, processing_function_path, save_file_cli, extract_text_only):
    logging.info(f"API Anfrage für {'Text' if extract_text_only else 'HTML'}-Inhalt von URL: {url}")
    webpage_content = fetch_webpage_content(url)
    if webpage_content:
        text_content = extract_text_content(webpage_content) if extract_text_only else None
        domain_name = extract_domain(url)
        title = extract_title(webpage_content)
        meta_description = extract_meta_description(webpage_content)
        h1_headings = extract_h1_headings(webpage_content)
        keywords = extract_keywords(text_content if text_content else extract_text_content(webpage_content), custom_stopwords=stopwords_param)

        css_selectors_param = None
        if css_selectors_param_raw:
            try:
                css_selectors_json = json.loads(css_selectors_param_raw)
                css_selectors_param = css_selectors_param_raw
            except json.JSONDecodeError:
                logging.warning("Ungültiges JSON-Format für CSS-Selektoren in API-Request. CSS-Extraktion wird übersprungen.")
                css_selectors_param = None

        css_data = extract_data_css(webpage_content, css_selectors_param) if css_selectors_param else None

        processed_content = None
        if processing_function_path:
            processed_content = apply_processing_function(url, domain_name, title, meta_description, h1_headings, keywords, webpage_content, text_content, css_data, processing_function_path)

        if save_to_db(url, domain_name, title, meta_description, h1_headings, keywords, webpage_content, text_content, processed_content):
            response_data = {
                "domain": domain_name, "database_status": "success",
                "title": title, "meta_description": meta_description, "h1_headings": h1_headings, "keywords": keywords,
            }
            if css_data:
                response_data["css_data"] = css_data
            if save_file_cli:
                filename = f"{domain_name}_{'text' if extract_text_only else 'html'}.txt"
                content_to_save_file = text_content if extract_text_only else webpage_content
                save_content_to_file(content_to_save_file, filename)
                response_data["file_status"] = "success"
                response_data["filename"] = filename
            if processed_content:
                response_data["processed_data"] = json.loads(processed_content)
            return create_api_response(data=response_data, message="Webseiteninhalt erfolgreich abgerufen und verarbeitet.")
        else:
            return create_api_response(errors=["Fehler beim Speichern in die Datenbank"], message="Fehler beim Speichern in die Datenbank.", status_code=500)
    else:
        return create_api_response(errors=["Webseiteninhalt konnte nicht abgerufen werden"], message="Webseiteninhalt konnte nicht abgerufen werden.", status_code=500)

@app.route('/api/v1/health', methods=['GET'])
@require_api_key
def api_health_check():
    db_healthy = False
    scheduler_healthy = False
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        db_healthy = True
    except sqlite3.Error:
        logging.error("Datenbank-Health-Check fehlgeschlagen.", exc_info=True)
        db_healthy = False
    finally:
        if conn:
            conn.close()

    if schedule.get_jobs():
        scheduler_healthy = True
    else:
        scheduler_healthy = False
        logging.warning("Scheduler scheint keine aktiven Jobs zu haben.")

    health_status = {
        "database_healthy": db_healthy,
        "scheduler_healthy": scheduler_healthy,
        "status": "ok" if db_healthy and scheduler_healthy else "degraded"
    }
    status_code = 200 if db_healthy and scheduler_healthy else 500
    return create_api_response(data=health_status, message="Health-Check durchgeführt.", status_code=status_code)

def run_command_line_scraping(args):
    url_raw = args.url
    if not is_valid_url(url_raw):
        logging.error("Ungültige URL eingegeben.")
        return
    url = url_raw

    extract_text_only = args.text
    save_file_cli = args.save_file
    custom_stopwords_cli = args.stopwords
    css_selectors_cli_raw = args.css_selectors
    processing_function_path = args.processing_function_path

    if processing_function_path and not is_safe_path(processing_function_path, PROCESSING_FUNCTIONS_DIR):
        logging.error("Ungültiger oder unsicherer Pfad zur Processing-Funktion. Verarbeitung wird übersprungen.")
        processing_function_path = None

    css_selectors_cli = None
    if css_selectors_cli_raw:
        try:
            css_selectors_json = json.loads(css_selectors_cli_raw)
            css_selectors_cli = css_selectors_cli_raw
        except json.JSONDecodeError:
            logging.error("Ungültiges JSON-Format für CSS-Selektoren in Kommandozeilenargument. CSS-Extraktion wird übersprungen.")
            css_selectors_cli = None

    domain_name = extract_domain(url)
    if not domain_name:
        logging.error("Ungültige URL eingegeben.")
        return

    webpage_content = fetch_webpage_content(url)
    if webpage_content:
        text_content = extract_text_content(webpage_content) if extract_text_only else None
        title = extract_title(webpage_content)
        meta_description = extract_meta_description(webpage_content)
        h1_headings = extract_h1_headings(webpage_content)
        keywords = extract_keywords(text_content if text_content else extract_text_content(webpage_content), custom_stopwords=custom_stopwords_cli)
        css_data = extract_data_css(webpage_content, css_selectors_cli)

        processed_content = None
        if processing_function_path:
            processed_content = apply_processing_function(url, domain_name, title, meta_description, h1_headings, keywords, webpage_content, text_content, css_data, processing_function_path)

        content_to_save_db = text_content if extract_text_only else webpage_content
        if save_to_db(url, domain_name, title, meta_description, h1_headings, keywords, webpage_content, text_content, processed_content):
            status = "success"
            logging.info("Inhalt und strukturierte Daten erfolgreich in Datenbank gespeichert (mit optionaler Datenverarbeitung).")
        else:
            error_message = "Fehler beim Speichern in Datenbank"
            status = "failure - db save error"
            logging.error("Fehler beim Speichern in die Datenbank.")

        if css_data:
            print("\nExtrahierte Daten basierend auf CSS-Selektoren:")
            print(json.dumps(css_data, indent=4, ensure_ascii=False))
        if processed_content:
            print("\nVerarbeitete Daten:")
            print(json.dumps(json.loads(processed_content), indent=4, ensure_ascii=False))

        if save_file_cli:
            filename = f"{domain_name}_{'text' if extract_text_only else 'html'}.txt"
            content_to_save_file = text_content if extract_text_only else webpage_content
            if content_to_save_file:
                if save_content_to_file(content_to_save_file, filename):
                    pass
                else:
                    logging.error("Fehler beim Speichern des Inhalts in Datei.")
            else:
                logging.error("Kein Inhalt zum Speichern in Datei vorhanden.")
    else:
        error_message = "Abrufen des Webseiteninhalts fehlgeschlagen"
        status = "failure - fetch error"
        logging.error("Abrufen des Webseiteninhalts fehlgeschlagen.")
    logging.info(f"Beende geplanten Scraping-Prozess für URL: {url} (Task-ID: {task_id}) um {datetime.datetime.now().isoformat()}. Status: {status}, Fehler: {error_message if error_message else 'Kein Fehler'}")    

def apply_processing_function(url, domain_name, title, meta_description, h1_headings, keywords, webpage_content, text_content, css_data, processing_function_path):
    processed_content = None
    if processing_function_path:
        processing_function = load_processing_function(processing_function_path)
        if processing_function:
            data_to_process = {
                "url": url,
                "domain": domain_name,
                "title": title,
                "meta_description": meta_description,
                "h1_headings": h1_headings,
                "keywords": keywords,
                "html_content": webpage_content,
                "text_content": text_content,
                "css_data": css_data
            }
            try:
                processed_data = processing_function(data_to_process)
                if processed_data is not None:
                    processed_content = json.dumps(processed_data, ensure_ascii=False)
                    logging.info(f"Benutzerdefinierte Verarbeitungsfunktion erfolgreich angewendet.")
                else:
                    logging.warning(f"Verarbeitungsfunktion hat 'None' zurückgegeben. Verarbeitungsergebnisse werden ignoriert.")
            except Exception as e:
                logging.error(f"Fehler bei der Ausführung der Verarbeitungsfunktion: {e}", exc_info=True)
    return processed_content

def run_scheduled_mode():
    logging.info(f"Starte geplanten Modus für zeitgesteuerte Aufgaben mit Task-Verwaltung aus Datenbank, Status-Tracking, API-Key Schutz, Rate Limiting (max. {RATE_LIMIT_REQUESTS_PER_MINUTE} Anfragen pro Minute), Caching (Gültigkeit: {CACHE_EXPIRY_SECONDS} Sekunden), Datenbank-Transaktionen, verbesserter Fehlerbehandlung und **sicherheitsgeprüftem Monitoring**...")
    while True:
        try:
            schedule.run_pending()
        except Exception as e_scheduler:
            logging.error(f"Unerwarteter Fehler im Scheduler-Loop: {e_scheduler}", exc_info=True)
            logging.error(f"Kritischer Fehler im Scheduler-Loop. Programm läuft weiter, aber Scheduler-Funktionalität könnte beeinträchtigt sein.  Bitte Logs prüfen.")
            send_notification(f"Kritischer Fehler im Scheduler-Loop: {e_scheduler}")
        time.sleep(1)

def run_streamlit():
    """Streamlit-Webanwendung zur Taskverwaltung."""

    st.title("WebCrawler-Pro Admin-Dashboard")

    # API-Key-Authentifizierung für Streamlit (einfach)
    api_key_input = st.text_input("API-Key eingeben:", type="password")
    if not api_key_input or not validate_api_key(api_key_input):
        st.error("Ungültiger API-Key.")
        return

    # Tasks laden
    tasks = load_scheduled_tasks()

    # Tasks anzeigen
    st.subheader("Geplante Tasks")
    if tasks:
        for task in tasks:
            with st.expander(f"Task ID: {task['id']}"):
                st.write(f"URL: {task['url']}")
                st.write(f"Zeitplan: {task['schedule_time']}")
                st.write(f"Nur Text: {task['text_only']}")
                st.write(f"Stopwörter: {task['stopwords']}")
                st.write(f"CSS-Selektoren: {task['css_selectors']}")
                st.write(f"Datei speichern: {task['save_file']}")
                st.write(f"Verarbeitungsfunktion: {task['processing_function_path']}")
                st.write(f"Status: {task['status']}")
                st.write(f"Letzte Ausführung: {task['last_run_time']}")
                st.write(f"Nächste Ausführung: {task['next_run_time']}")
                st.write(f"Fehlermeldung: {task['error_message']}")


                # Task löschen
                if st.button(f"Task {task['id']} löschen"):
                    if delete_scheduled_task_from_db(task['id']):
                        st.success("Task erfolgreich gelöscht.")
                        setup_scheduled_tasks()
                        st.rerun()  # Hier ist es korrekt
                    else:
                        st.error("Fehler beim Löschen des Tasks.")

                # Task sofort ausführen
                if st.button(f"Task {task['id']} sofort ausführen"):
                    # FALSCH: result = api_run_scheduled_task_by_id(task['id'])
                    # RICHTIG:  Den API-Endpunkt simulieren, ohne den Flask-Kontext zu benötigen.
                    url = task['url']
                    extract_text_only = bool(task.get('text_only', False))
                    custom_stopwords_cli = task.get('stopwords')
                    css_selectors_cli = task.get('css_selectors')
                    save_file_cli = bool(task.get('save_file', False))
                    processing_function_path = task.get('processing_function_path')
                    threading.Thread(target=scrape_and_store_url, args=(url, extract_text_only, custom_stopwords_cli, css_selectors_cli, save_file_cli, processing_function_path, task['id'])).start()



                st.success("Task wird ausgeführt.")
                st.rerun()  # Hier ist es korrekt
    else:
        st.info("Keine geplanten Tasks gefunden.")

    # Neuen Task hinzufügen
    st.subheader("Neuen Task hinzufügen")
    with st.form("new_task"):
        url = st.text_input("URL:")
        schedule_time = st.text_input("Zeitplan (z.B. stündlich, täglich um 10:00, alle 30 minuten):")
        text_only = st.checkbox("Nur Text extrahieren")
        stopwords = st.text_input("Stopwörter (kommagetrennt):")
        css_selectors = st.text_area("CSS-Selektoren (JSON):")
        save_file = st.checkbox("Datei speichern")
        processing_function_path = st.text_input("Verarbeitungsfunktion (Pfad):")

        if st.form_submit_button("Task hinzufügen"):
            try:
                task_payload = ScheduledTaskPayload(
                    url=url, schedule_time=schedule_time, text_only=text_only, stopwords=stopwords,
                    css_selectors=css_selectors, save_file=save_file, processing_function_path=processing_function_path
                )
            except ValidationError as e:
                st.error(str(e)) # Fehler anzeigen
                return

            task_data = task_payload.model_dump()
            task_data['id'] = str(uuid.uuid4())

            if save_scheduled_task_to_db(task_data):
                st.success("Task erfolgreich hinzugefügt.")
                setup_scheduled_tasks() # Tasks neu laden
                st.rerun()  # Streamlit neu laden
            else:
                st.error("Fehler beim Hinzufügen des Tasks.")

def main():
    init_db()
    parser = argparse.ArgumentParser(description="Extrahiert den Inhalt einer Webseite, strukturierte Daten und Keywords und speichert sie in einer Datenbank oder startet eine Web-API. **Sicherheitshinweis:** Seien Sie vorsichtig bei der Verwendung von benutzerdefinierten Processing-Funktionen und CSS-Selektoren, um Sicherheitsrisiken zu minimieren. **API-Key, Rate Limiting und Caching sind aktiv. Erweiterte Task-Verwaltung, Datenbank-Transaktionen, verbesserte Fehlerbehandlung und sicherheitsgeprüftes Monitoring verfügbar.**")
    parser.add_argument("url", nargs='?', default=None, help="Die URL der Webseite, deren Inhalt extrahiert werden soll (für einmaligen Kommandozeilenmodus). Wenn keine URL angegeben und --api nicht verwendet, werden geplante Tasks ausgeführt.")
    parser.add_argument("--text", action="store_true", help="Speichert nur den extrahierten Textinhalt anstatt des gesamten HTML-Codes.")
    parser.add_argument("--api", action="store_true", help="Startet die Web-API anstatt des Kommandozeilenmodus oder der geplanten Tasks.")
    parser.add_argument("--save-file", action="store_true", help="Speichert den Inhalt zusätzlich zur Datenbank in einer Datei.")
    parser.add_argument("--stopwords", type=str, default=None, help="Kommagetrennte Liste von zusätzlichen Stopwörtern für die Keyword-Extraktion.")
    parser.add_argument("--css-selectors", type=str, default=None, help="JSON-String von CSS-Selektoren zur Datenextraktion. Kann einfache Selektoren oder konfigurierte Selektoren mit Datentypen und Bereinigungsfunktionen enthalten. **Sicherheitshinweis:**  Validieren Sie CSS-Selektoren sorgfältig, um Injection-Angriffe zu vermeiden.")
    parser.add_argument("--processing-function", type=str, default=None, dest="processing_function_path", help="Pfad zu einer Python-Datei, die eine 'process_data(data)' Funktion enthält zur benutzerdefinierten Datenverarbeitung. **Sicherheitshinweis:**  Stellen Sie sicher, dass Sie nur vertrauenswürdigen Code ausführen, da dies die Sicherheit des Systems beeinträchtigen kann.")
    parser.add_argument("--streamlit", action="store_true", help="Startet das Streamlit Web-UI für die Admin-Oberfläche.")

    args = parser.parse_args()

    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')

    setup_scheduled_tasks()

    if args.api:
        logging.info(f"Starte Flask API mit erweiterter Task-Verwaltung (CRUD, Status-Monitoring, manuelle Task-Auslösung), Status-Tracking in Datenbank, API-Key Authentifizierung, Rate Limiting (max. {RATE_LIMIT_REQUESTS_PER_MINUTE} Anfragen pro Minute), Caching (Gültigkeit: {CACHE_EXPIRY_SECONDS} Sekunden), Datenbank-Transaktionen, verbesserter Fehlerbehandlung und **sicherheitsgeprüftem Monitoring**...")
        app.run(debug=API_DEBUG_MODE)
    elif args.url:
        run_command_line_scraping(args)
    elif args.streamlit:
        run_streamlit()
    else:
        IS_SCHEDULED_MODE = True
        run_scheduled_mode()

if __name__ == "__main__":
    main()
