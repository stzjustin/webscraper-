#!/usr/bin/env python3
"""
Website to PDF Converter
Lädt eine Website herunter, bereinigt den HTML-Inhalt und speichert ihn als PDF.
"""

import os
import sys
import requests
from bs4 import BeautifulSoup
from weasyprint import HTML, CSS
from pathlib import Path
from datetime import datetime
import re


class WebsiteToPDF:
    def __init__(self, output_dir=None):
        """
        Initialisiert den Website-zu-PDF-Converter.

        Args:
            output_dir: Ausgabeverzeichnis für PDFs. Wenn None, wird ein Ordner auf dem Desktop erstellt.
        """
        if output_dir is None:
            # Desktop-Pfad ermitteln
            home = Path.home()
            desktop = home / "Desktop"

            # Fallback für Linux-Systeme ohne Desktop-Ordner
            if not desktop.exists():
                desktop = home / "Schreibtisch"  # Deutsche Bezeichnung
            if not desktop.exists():
                desktop = home  # Fallback auf Home-Verzeichnis

            # Ausgabeordner erstellen
            output_dir = desktop / "WebsiteScraperPDFs"

        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        print(f"✓ Ausgabeordner: {self.output_dir}")

    def fetch_website(self, url):
        """
        Lädt den HTML-Inhalt einer Website herunter.

        Args:
            url: Die URL der Website

        Returns:
            Der HTML-Inhalt als String
        """
        print(f"Lade Website: {url}")

        # Stelle sicher, dass die URL ein Schema hat
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            print(f"✓ Website erfolgreich geladen ({len(response.content)} bytes)")
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"✗ Fehler beim Laden der Website: {e}")
            sys.exit(1)

    def clean_html(self, html_content, url):
        """
        Bereinigt den HTML-Inhalt und entfernt unnötige Elemente.

        Args:
            html_content: Der rohe HTML-Inhalt
            url: Die ursprüngliche URL (für absolute Links)

        Returns:
            Bereinigter HTML-String
        """
        print("Bereinige HTML-Inhalt...")
        soup = BeautifulSoup(html_content, 'html.parser')

        # Entferne Scripts, Styles, und andere nicht-sichtbare Elemente
        for element in soup(['script', 'style', 'nav', 'footer', 'header', 'iframe', 'noscript']):
            element.decompose()

        # Entferne HTML-Kommentare
        for comment in soup.find_all(string=lambda text: isinstance(text, type(soup.find_all(string=True)[0])) and text.strip().startswith('<!--')):
            comment.extract()

        # Entferne leere Elemente
        for element in soup.find_all():
            if not element.get_text(strip=True) and not element.find_all(['img', 'video', 'audio']):
                element.decompose()

        # Erstelle ein sauberes HTML-Dokument
        clean_soup = BeautifulSoup('<!DOCTYPE html><html><head><meta charset="utf-8"></head><body></body></html>', 'html.parser')

        # Füge Titel hinzu
        title_tag = soup.find('title')
        if title_tag:
            new_title = clean_soup.new_tag('title')
            new_title.string = title_tag.get_text()
            clean_soup.head.append(new_title)

        # Füge den Body-Inhalt hinzu
        if soup.body:
            clean_soup.body.append(soup.body)
        else:
            clean_soup.body.append(soup)

        print("✓ HTML bereinigt")
        return str(clean_soup.prettify())

    def generate_filename(self, url):
        """
        Generiert einen Dateinamen basierend auf der URL und dem aktuellen Zeitstempel.

        Args:
            url: Die URL der Website

        Returns:
            Dateiname für das PDF
        """
        # Extrahiere Domain aus URL
        domain = re.sub(r'https?://(www\.)?', '', url)
        domain = re.sub(r'[^\w\-_\.]', '_', domain)
        domain = domain[:50]  # Begrenze Länge

        # Zeitstempel
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        return f"{domain}_{timestamp}.pdf"

    def convert_to_pdf(self, html_content, output_filename):
        """
        Konvertiert HTML-Inhalt in ein PDF.

        Args:
            html_content: Der HTML-Inhalt als String
            output_filename: Name der Ausgabedatei
        """
        output_path = self.output_dir / output_filename
        print(f"Erstelle PDF: {output_path}")

        # CSS für bessere PDF-Formatierung
        css_string = """
        @page {
            margin: 2cm;
            size: A4;
        }
        body {
            font-family: 'Arial', 'Helvetica', sans-serif;
            font-size: 12pt;
            line-height: 1.6;
            color: #333;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #2c3e50;
            margin-top: 1em;
            margin-bottom: 0.5em;
        }
        h1 { font-size: 24pt; }
        h2 { font-size: 20pt; }
        h3 { font-size: 16pt; }
        img {
            max-width: 100%;
            height: auto;
        }
        a {
            color: #3498db;
            text-decoration: none;
        }
        pre, code {
            background-color: #f4f4f4;
            padding: 0.5em;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }
        """

        try:
            HTML(string=html_content).write_pdf(
                output_path,
                stylesheets=[CSS(string=css_string)]
            )
            print(f"✓ PDF erfolgreich erstellt: {output_path}")
        except Exception as e:
            print(f"✗ Fehler beim Erstellen des PDFs: {e}")
            sys.exit(1)

    def process_url(self, url):
        """
        Verarbeitet eine URL komplett: Laden, Bereinigen, PDF-Erstellung.

        Args:
            url: Die zu verarbeitende URL
        """
        print(f"\n{'='*60}")
        print(f"Verarbeite: {url}")
        print(f"{'='*60}\n")

        # Website laden
        html_content = self.fetch_website(url)

        # HTML bereinigen
        cleaned_html = self.clean_html(html_content, url)

        # Dateiname generieren
        filename = self.generate_filename(url)

        # PDF erstellen
        self.convert_to_pdf(cleaned_html, filename)

        print(f"\n{'='*60}")
        print(f"✓ Fertig! PDF gespeichert in: {self.output_dir / filename}")
        print(f"{'='*60}\n")


def main():
    """Hauptfunktion für die Kommandozeilen-Nutzung."""
    print("\n" + "="*60)
    print("Website zu PDF Converter")
    print("="*60 + "\n")

    # URL abfragen
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("Bitte Website-URL eingeben: ").strip()

    if not url:
        print("Keine URL angegeben!")
        sys.exit(1)

    # Converter initialisieren und URL verarbeiten
    converter = WebsiteToPDF()
    converter.process_url(url)


if __name__ == "__main__":
    main()
