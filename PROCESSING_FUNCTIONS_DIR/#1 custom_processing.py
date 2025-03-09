# custom_processing.py
import json
import logging

ALLOWED_CSS_PROPERTIES = ['color', 'font-size', 'background-color', 'margin', 'padding', 'text-align', 'font-weight', 'text-decoration', 'font-family', 'border', 'border-radius', 'width', 'height', 'display', 'visibility', 'opacity', 'cursor', 'list-style-type', 'vertical-align']
def process_data(data):
    """
    Verarbeitungsfunktion, die die extrahierten Daten formatiert und als JSON-String zurückgibt.

    Args:
        data (dict): Ein Dictionary mit den extrahierten Daten (URL, Title, Meta-Description, etc.).

    Returns:
        str: Ein JSON-String der verarbeiteten Daten.
    """
    logging.info("Starte benutzerdefinierte Datenverarbeitung...")

    try:
        processed_data = {
            "url": data.get("url"),
            "title": data.get("title"),
            "meta_description": data.get("meta_description"),
            "keyword_count": len(data.get("keywords", [])),
            "has_css_data": bool(data.get("css_data"))
        }

        # Zusätzliche Formatierung oder Berechnungen hier möglich

        processed_json = json.dumps(processed_data, ensure_ascii=False, indent=4)
        logging.info("Datenverarbeitung abgeschlossen.")
        return processed_json
    except Exception as e:
        logging.error(f"Fehler in der Datenverarbeitungsfunktion: {e}", exc_info=True)
        return json.dumps({"error": "Fehler bei der Datenverarbeitung"}, ensure_ascii=False) # Gib eine Fehler-JSON zurück