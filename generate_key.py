import os
import uuid
from dotenv import load_dotenv, set_key
import logging
import yaml

# Logging konfigurieren
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_api_key():
    """Generiert einen eindeutigen API-Key."""
    return str(uuid.uuid4())

def load_existing_api_keys():
    """Lädt bestehende API-Keys aus der .env-Datei und config.yaml."""
    load_dotenv()
    api_keys = set()

    # Aus .env laden
    for i in range(1, 10):  # Bis zu 10 API Keys aus ENV laden
        key = os.getenv(f"API_KEY_{i}")
        if key:
            api_keys.add(key)

    # Aus config.yaml laden
    try:
        with open('config.yaml', 'r') as f:
            yaml_config = yaml.safe_load(f) or {}
            if 'api_keys' in yaml_config:
                api_keys.update(yaml_config['api_keys'])
    except FileNotFoundError:
        logging.warning("config.yaml nicht gefunden. Es werden nur Umgebungsvariablen berücksichtigt.")
    except yaml.YAMLError as e:
        logging.error(f"Fehler beim Lesen von config.yaml: {e}")

    return api_keys

def save_api_keys(num_keys=3):
    """Generiert und speichert bis zu num_keys (default 3) API-Keys in .env und config.yaml, falls noch nicht vorhanden."""
    existing_keys = load_existing_api_keys()
    generated_keys = []
    keys_added = 0 # Zähler für tatsächlich hinzugefügte Keys

    # Generiere und speichere neue Keys bis zur gewünschten Anzahl
    while keys_added < num_keys:
        new_key = generate_api_key()
        if new_key not in existing_keys:
            generated_keys.append(new_key)
            existing_keys.add(new_key)
            keys_added += 1
            logging.info(f"Neuer API-Key generiert: '{new_key}'") # Generierung protokollieren
        else:
            logging.warning("Duplizierter API-Key generiert. Wird erneut versucht...")
        if keys_added >= num_keys:
            break # Abbruch, wenn genügend Keys generiert wurden

    # .env-Datei aktualisieren (bestehende Keys beibehalten, neue hinzufügen)
    load_dotenv()
    env_vars_dict = dict(os.environ) # Aktuelle Umgebungsvariablen als Dictionary sichern

    # API Keys aus .env extrahieren und sortieren
    api_keys_env = {}
    for key, value in env_vars_dict.items():
        if key.startswith("API_KEY_"):
            try:
                index = int(key[8:]) # Zahl nach "API_KEY_" extrahieren
                api_keys_env[index] = value # Index und Wert speichern
            except ValueError:
                logging.warning(f"Ungültiger API-Key Name in .env: {key}. Ignoriert.") # Log ungültiger Key-Namen

    # Vorhandene API-Keys sortieren, um die Reihenfolge beizubehalten
    sorted_api_keys_env = [value for index, value in sorted(api_keys_env.items())] # Sortierte Liste der Werte

    # Neue Keys an die bestehende Liste anhängen
    all_api_keys = sorted_api_keys_env + generated_keys # Zusammenfügen (Reihenfolge beachten)

    # .env-Datei neu schreiben mit allen Keys
    with open(".env", "w") as env_file: # .env-Datei komplett neu schreiben
        for i, api_key in enumerate(all_api_keys, start=1):
            env_file.write(f"API_KEY_{i}={api_key}\n") # Key mit neuem Index schreiben

    logging.info(".env-Datei aktualisiert.")

    # config.yaml aktualisieren (API-Keys hinzufügen)
    try:
        with open('config.yaml', 'r') as f:
            yaml_config = yaml.safe_load(f) or {}
    except FileNotFoundError:
        yaml_config = {}
    except yaml.YAMLError as e:
        logging.error(f"Fehler beim Lesen von config.yaml: {e}")
        return

    if 'api_keys' not in yaml_config:
        yaml_config['api_keys'] = []

    # Füge neue Keys nur hinzu, wenn sie noch nicht existieren
    new_keys_added = False
    for api_key in generated_keys:
        if api_key not in yaml_config['api_keys']:
            yaml_config['api_keys'].append(api_key)
            new_keys_added = True

    if new_keys_added:
        try:
            with open('config.yaml', 'w') as f:
                yaml.dump(yaml_config, f, default_flow_style=False)
            logging.info("Neue API-Keys wurden zur 'api_keys'-Liste in config.yaml hinzugefügt.")
        except Exception as e:
            logging.error(f"Fehler beim Schreiben in config.yaml: {e}")
    else:
        logging.info("Alle generierten API-Keys waren bereits in config.yaml vorhanden.")


if __name__ == "__main__":
    save_api_keys(num_keys=3)
    print("Bis zu 3 neue API-Keys generiert und gespeichert (falls noch nicht vorhanden).")