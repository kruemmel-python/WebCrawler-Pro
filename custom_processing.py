//
consoleneingabe:
Invoke-WebRequest -Uri "$API_HOST/api/v1/fetch-links?url=https://www.gesetze-im-internet.de/sgb_1/" -Headers @{'X-API-Key' = $API_KEY} | ConvertFrom-Json | ForEach-Object {$links = $_.data.links; foreach ($link in $links) { Invoke-WebRequest -Uri "$API_HOST/api/v1/fetch-text?url=$($link)&save_file=true&processing_function_path=custom_processing.py" -Headers @{'X-API-Key' = $API_KEY} }}
//

# custom_processing.py
import json
import logging

ALLOWED_CSS_PROPERTIES = ['color', 'font-size', 'background-color', 'margin', 'padding', 'text-align', 'font-weight', 'text-decoration', 'font-family', 'border', 'border-radius', 'width', 'height', 'display', 'visibility', 'opacity', 'cursor', 'list-style-type', 'vertical-align']
def process_data(data):
    """
    Verarbeitungsfunktion, die die extrahierten Daten formatiert und als JSON-String zurückgibt.
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
        processed_json = json.dumps(processed_data, ensure_ascii=False, indent=4)
        logging.info("Datenverarbeitung abgeschlossen.")
        return processed_json
    except Exception as e:
        logging.error(f"Fehler in der Datenverarbeitungsfunktion: {e}", exc_info=True)
        return json.dumps({"error": "Fehler bei der Datenverarbeitung"}, ensure_ascii=False) # Gib eine Fehler-JSON zurück
