# custom_processing.py
import json
import logging

ALLOWED_CSS_PROPERTIES = ['color', 'font-size', 'background-color', 'margin', 'padding', 'text-align', 'font-weight', 'text-decoration', 'font-family', 'border', 'border-radius', 'width', 'height', 'display', 'visibility', 'opacity', 'cursor', 'list-style-type', 'vertical-align']
def process_data(data):
    """
    Verarbeitungsfunktion, die Keywords filtert und die Anzahl der erlaubten CSS-Eigenschaften zählt.

    Args:
        data (dict): Ein Dictionary mit den extrahierten Daten (URL, Title, Meta-Description, etc.).

    Returns:
        dict: Ein Dictionary mit den verarbeiteten Daten.
    """
    logging.info("Starte benutzerdefinierte Datenverarbeitung...")

    try:
        # Keywords filtern (nur alphabetische)
        filtered_keywords = [keyword for keyword in data.get("keywords", []) if keyword.isalpha()]

        # Anzahl der erlaubten CSS-Eigenschaften zählen
        allowed_css_count = 0
        if "css_data" in data:
            for selector, properties in data["css_data"].items():
                for property_name in properties:
                    if property_name in ALLOWED_CSS_PROPERTIES:
                        allowed_css_count += 1

        processed_data = {
            "url": data.get("url"),
            "title": data.get("title"),
            "meta_description": data.get("meta_description"),
            "filtered_keywords": filtered_keywords,
            "allowed_css_properties_count": allowed_css_count
        }

        logging.info("Datenverarbeitung abgeschlossen.")
        return processed_data
    except Exception as e:
        logging.error(f"Fehler in der Datenverarbeitungsfunktion: {e}", exc_info=True)
        return {"error": "Fehler bei der Datenverarbeitung"}