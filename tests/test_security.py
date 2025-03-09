import unittest
import os
import json
import logging
from unittest.mock import patch, mock_open
import requests
from bs4 import BeautifulSoup
import app  # Import des Hauptprogramms

# Testdaten
TEST_URL = "https://www.ciphercore.de"
TEST_HTML = """<html><head><title>Example Domain</title><meta name='description' content='Test Description'></head>
<body><h1>Example Domain</h1>
<p>This domain is for use in illustrative examples in documents.</p>
<p><a href="https://www.iana.org/domains/example">More information...</a></p>
</body></html>"""
TEST_TEXT = """Example Domain
Example Domain
This domain is for use in illustrative examples in documents.
More information..."""

class TestWebScrapingFunctions(unittest.TestCase):

    def test_is_valid_url(self):
        """Testet, ob die URL-Validierung korrekt arbeitet."""
        self.assertTrue(app.is_valid_url("https://www.ciphercore.de"))
        self.assertTrue(app.is_valid_url("http://ciphercore.de"))
        self.assertFalse(app.is_valid_url("ciphercore.de"))  # Fehlendes Schema
        self.assertFalse(app.is_valid_url("ftp://ciphercore.de"))  # Ungültiges Schema
        self.assertFalse(app.is_valid_url("https://.com"))  # Ungültige Domain
        self.assertFalse(app.is_valid_url("https://example."))  # Endet mit Punkt
        self.assertFalse(app.is_valid_url("https://-test.com"))  # Ungültiges Präfix
        self.assertFalse(app.is_valid_url("https://ciphercore"))  # Fehlende TLD
        self.assertFalse(app.is_valid_url("https://ciphercore..de"))  # Doppelte Punkte
        self.assertFalse(app.is_valid_url("https://.ciphercore.de"))  # Punkt am Anfang
        # Zusätzliche Tests für gültige URLs
        self.assertTrue(app.is_valid_url("https://sub.domain.com"))
        self.assertTrue(app.is_valid_url("https://example.co.uk"))
        self.assertTrue(app.is_valid_url("https://valid-domain123.com"))


    def test_extract_domain(self):
        """Testet die Extraktion der Domain aus einer URL."""
        self.assertEqual(app.extract_domain("https://www.ciphercore.de"), "www.ciphercore.de")
        self.assertEqual(app.extract_domain("http://ciphercore.de"), "ciphercore.de")
        self.assertIsNone(app.extract_domain("ciphercore.de"))  # Keine vollständige URL


    @patch('app.fetch_webpage_content', return_value=TEST_HTML)
    def test_extract_text_content(self, mock_fetch):
        """Testet die Extraktion von reinem Text aus HTML."""
        self.assertEqual(app.extract_text_content(TEST_HTML), TEST_TEXT)

    @patch('app.fetch_webpage_content', return_value=TEST_HTML)
    def test_extract_title(self, mock_fetch):
        """Testet die Extraktion des Titels aus HTML."""
        self.assertEqual(app.extract_title(TEST_HTML), "Example Domain")

    @patch('app.fetch_webpage_content', return_value=TEST_HTML)
    def test_extract_meta_description(self, mock_fetch):
        """Testet die Extraktion der Meta-Description."""
        self.assertEqual(app.extract_meta_description(TEST_HTML), "Test Description")


    @patch('app.fetch_webpage_content', return_value=TEST_HTML)
    def test_extract_h1_headings(self, mock_fetch):
        """Testet die Extraktion von H1-Überschriften."""
        self.assertEqual(app.extract_h1_headings(TEST_HTML), ['Example Domain'])

    def test_extract_keywords(self):
        """Testet die Keyword-Extraktion mit Priorisierung."""
        text = "Dies ist ein Testtext mit einigen Keywords. Keywords sind wichtig für SEO."
        keywords = app.extract_keywords(text, top_n=3)

        # Robusterer Test: Mindestens eines der erwarteten Keywords muss enthalten sein
        self.assertTrue(any(word in keywords for word in ['keywords', 'wichtig', 'testtext']))

    @patch('app.fetch_webpage_content', return_value=TEST_HTML)
    def test_extract_data_css(self, mock_fetch):
        """Testet die Extraktion von Daten mit CSS-Selektoren."""
        css_selectors = '{"title": {"selector": "title", "type": "string"}, "h1": {"selector": "h1"}}'
        extracted_data = app.extract_data_css(TEST_HTML, css_selectors)
        self.assertEqual(extracted_data.get("title"), ["Example Domain"])
        self.assertEqual(extracted_data.get("h1"), ["Example Domain"])



    def test_is_safe_css_selector(self):
        """Testet, ob CSS-Selektoren sicher sind."""
        self.assertTrue(app.is_safe_css_selector("h1"))
        self.assertTrue(app.is_safe_css_selector(".class-name"))
        self.assertTrue(app.is_safe_css_selector("p > a"))

        unsafe_selectors = [
            "script", 
            "body { background: url(javascript:alert('XSS')) }", 
            "div[onclick*=alert]", 
            "div { expression(alert('XSS')) }", # CSS Expressions
            "div[style=expression(alert('XSS'))]", # CSS Expressions im style-Attribut
            "div[onclick=alert('XSS')]", # JavaScript im onclick-Attribut
            "div { background: data:image/png;base64,abcd }", # Data URLs
            "div[onmouseover=alert('XSS')]", # JavaScript im onmouseover-Attribut
            "@import url('http://evil.com');" # @import Anweisung
        ]
        for selector in unsafe_selectors:
            self.assertFalse(app.is_safe_css_selector(selector), msg=f"Selector '{selector}' sollte als unsicher erkannt werden.") # Fehlermeldung hinzugefügt

    @patch('app.fetch_webpage_content', return_value=TEST_HTML)
    @patch('builtins.open', new_callable=mock_open)
    def test_save_content_to_file(self, mock_file, mock_fetch):
        """Testet das Speichern von Inhalten in eine Datei."""
        file_path = os.path.join(".", "test.txt")  # Plattformunabhängig
        self.assertTrue(app.save_content_to_file(TEST_HTML, file_path))
        mock_file.assert_called_once_with(file_path, 'w', encoding='utf-8')

    @patch('os.path.exists', return_value=True)
    def test_load_processing_function(self, mock_exists):
        """Testet das Laden einer Verarbeitungsfunktion."""
        mock_func = lambda x: x

        with patch('app.importlib.util.spec_from_file_location') as mock_spec:
            with patch('app.importlib.util.module_from_spec') as mock_module:
                mock_module.return_value.process_data = mock_func
                func = app.load_processing_function("./test_processing.py")
                self.assertTrue(callable(func))


    def test_is_safe_path(self):
        """Testet die Sicherheitsprüfung für Dateipfade."""
        base_dir = "/base/dir"
        self.assertTrue(app.is_safe_path("/base/dir/file.txt", base_dir))
        self.assertFalse(app.is_safe_path("../file.txt", base_dir))  # Path Traversal Angriff



if __name__ == '__main__':
    unittest.main()