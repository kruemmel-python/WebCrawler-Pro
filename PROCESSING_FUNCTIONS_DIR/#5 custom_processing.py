# processing_function.py
import json

def process_data(data):
    """Verarbeitet Eingabedaten und fügt zusätzliche Informationen hinzu.

    Diese Funktion nimmt ein Dictionary mit Daten entgegen, fügt ein neues Feld 
    hinzu und berechnet die Anzahl der Schlüsselwörter, falls vorhanden.

    Args:
        data (dict): Ein Dictionary mit den zu verarbeitenden Daten.  
                     Beispiel: {"name": "Max Mustermann", "keywords": ["Python", "Sicherheit"]}

    Returns:
        dict: Ein Dictionary mit den verarbeiteten Daten, einschließlich 
              'additional_info' und 'keyword_count'.
              Beispiel: {"name": "Max Mustermann", "keywords": ["Python", "Sicherheit"], 
                        "additional_info": "Diese Information wurde von der Processing Function hinzugefügt.", 
                        "keyword_count": 2}

    Raises:
        TypeError: Wenn der Eingabeparameter `data` kein Dictionary ist.

    """
    if not isinstance(data, dict):
        raise TypeError("Eingabe muss ein Dictionary sein.")

    data['additional_info'] = "Diese Information wurde von der Processing Function hinzugefügt."

    if 'keywords' in data:
        if isinstance(data['keywords'], list):  # Sicherstellen, dass 'keywords' eine Liste ist.
            data['keyword_count'] = len(data['keywords'])
        else:
            data['keyword_count'] = 0 # oder raise TypeError, je nach gewünschtem Verhalten
    else:
        data['keyword_count'] = 0

    return data
