import streamlit as st
import requests
import pandas as pd
import json

API_HOST = "http://localhost:5000"  # Standard API Host, anpassbar
API_ENDPOINT_SEARCH = f"{API_HOST}/api/v1/search-content" # API Endpunkt für die Suche
API_ENDPOINT_HEALTH = f"{API_HOST}/api/v1/health" # Health Check Endpunkt

def check_api_health(api_key):
    headers = {'X-API-Key': api_key}
    try:
        response = requests.get(API_ENDPOINT_HEALTH, headers=headers)
        response.raise_for_status() # Wirft HTTPError für schlechte Responses (4xx oder 5xx)
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"API Health Check fehlgeschlagen: {e}")
        return False

def search_database(api_key, query, search_field="url"):
    headers = {'X-API-Key': api_key}
    params = {'query': query, 'search_field': search_field}
    try:
        response = requests.get(API_ENDPOINT_SEARCH, headers=headers, params=params)
        response.raise_for_status() # This is good - it will throw an exception for 4xx/5xx errors
        return response.json()
    except requests.exceptions.RequestException as e: # **This is catching ALL request exceptions, even successful ones?**
        st.error(f"Fehler bei der Datenbankabfrage: {e}")
        return None

st.title("WebCrawler-Pro Datenbank Browser")

api_key = st.text_input("API-Key eingeben:", type="password")

if api_key:
    if check_api_health(api_key): # API Health Check nach API Key Eingabe
        st.success("API-Key valid und API erreichbar.")

        search_query = st.text_input("Suchbegriff:", placeholder="URL, Keyword, etc.")
        search_field = st.selectbox("Suchfeld:", ["url", "title", "meta_description", "text_content", "domain"], index=0)

        if st.button("Suchen"):
            if search_query:
                search_results = search_database(api_key, search_query, search_field)
                if search_results and 'data' in search_results:
                    if search_results['data']:
                        df = pd.DataFrame(search_results['data'])
                        if 'text_content' in df.columns:
                            df['text_content'] = df['text_content'].str.slice(0, 10000) + '...' # Zeige nur die ersten 200 Zeichen + "..."
                        st.dataframe(df) # Zeige Ergebnisse als DataFrame
                    else:
                        st.info("Keine Ergebnisse gefunden.")
                elif search_results and 'errors' in search_results:
                    st.error(f"API Fehler: {search_results['errors']}")
                else:
                    st.error("Fehler bei der Suche. Überprüfen Sie die API-Verbindung und den API-Key.")
            else:
                st.warning("Bitte geben Sie einen Suchbegriff ein.")
    else:
        st.error("API nicht erreichbar oder API-Key ungültig. Bitte überprüfen Sie die API und den Key.")
else:
    st.warning("Bitte geben Sie einen API-Key ein, um die Datenbank zu durchsuchen.")
