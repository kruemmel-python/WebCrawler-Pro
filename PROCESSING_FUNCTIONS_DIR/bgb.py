//
Invoke-WebRequest -Uri 'http://localhost:5000/api/v1/fetch-text' -Method Get -Headers @{'X-API-Key' = 'e5975e9d-377a-409a-aa8e-df003081562c'} -Body @{url='https://www.gesetze-im-internet.de/bgb/'; processing_function_path='./custom_processing.py'}
//

import requests
from bs4 import BeautifulSoup
import logging
import json
from urllib.parse import urljoin, urlparse

def process_data(data):
    """
    Crawlt die Seite gesetze-im-internet.de/bgb/ und extrahiert alle Gesetzestexte
    inklusive Paragraphentitel und Textinhalt.

    Args:
        data (dict): Das Eingabe-Daten-Dictionary (kann hier ignoriert werden,
                     da wir die URL fest im Code definieren).

    Returns:
        str: Ein JSON-String mit einer Liste von Dictionaries, wobei jedes Dictionary
             den Titel des Gesetzes, den Paragraphentitel, die URL und den extrahierten
             Gesetzestext enthält. Oder ein JSON mit einer Fehlermeldung im Fehlerfall.
    """
    logging.info("Starte benutzerdefinierte Verarbeitung: Scrapen von BGB-Gesetzestexten mit Titel und Inhalt...")

    start_url = "https://www.gesetze-im-internet.de/bgb/"
    gesetzestexte = []

    try:
        response = requests.get(start_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        link_zellen = soup.select('td a[href^="/bgb/__"]')

        for link_zelle in link_zellen:
            gesetz_link = link_zelle['href']
            gesetz_url = urljoin(start_url, gesetz_link)
            paragraph_titel_roh = link_zelle.get_text(strip=True)

            try:
                gesetz_response = requests.get(gesetz_url)
                gesetz_response.raise_for_status()
                gesetz_soup = BeautifulSoup(gesetz_response.content, 'html.parser')

                # **Neuer Code für Paragraphentitel-Extraktion:**
                titel_element = gesetz_soup.select_one('h1.jurAbsatz') # Annahme: Titel in h1 mit Klasse .jurAbsatz
                if not titel_element:
                    titel_element = gesetz_soup.select_one('div.juraHeadline') # Fallback, falls h1.jurAbsatz nicht existiert
                gesetz_paragraphen_titel = titel_element.get_text(strip=True) if titel_element else paragraph_titel_roh # Fallback auf Linktext

                # **Textinhalt-Extraktion (wie zuvor):**
                absatz_elemente = gesetz_soup.select('.jurAbsatz, .normenhierarchie')
                gesetz_text_teile = [element.get_text(separator='\n', strip=True) for element in absatz_elemente]
                gesetz_text = "\n\n".join(gesetz_text_teile)

                gesetzestexte.append({
                    "paragraph_titel": gesetz_paragraphen_titel, # **Neuer Key für Paragraphentitel**
                    "link_zellen_titel_roh": paragraph_titel_roh, # Roh-Titel aus Linkzelle (zur Info/Debug)
                    "url": gesetz_url,
                    "text": gesetz_text
                })
                logging.info(f"Gesetzestext '{gesetz_paragraphen_titel}' von URL '{gesetz_url}' extrahiert.")

            except requests.exceptions.RequestException as e_gesetz:
                logging.error(f"Fehler beim Abrufen des Gesetzestextes von '{gesetz_url}': {e_gesetz}")
                gesetzestexte.append({
                    "paragraph_titel": paragraph_titel_roh,
                    "url": gesetz_url,
                    "error": f"Fehler beim Abrufen: {str(e_gesetz)}"
                })

        verarbeitete_daten = {"gesetzestexte": gesetzestexte}
        logging.info(f"Extraktion von {len(gesetzestexte)} Gesetzestexten mit Titeln und Inhalten abgeschlossen.")
        return json.dumps(verarbeitete_daten, ensure_ascii=False, indent=4)

    except requests.exceptions.RequestException as e_start:
        error_message = f"Fehler beim Abrufen der Startseite '{start_url}': {e_start}"
        logging.error(error_message)
        return json.dumps({"error": error_message}, ensure_ascii=False)
    except Exception as e_gesamt:
        error_message = f"Unerwarteter Fehler bei der Verarbeitung: {e_gesamt}"
        logging.error(error_message, exc_info=True)
        return json.dumps({"error": error_message}, ensure_ascii=False)

