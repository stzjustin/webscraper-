#!/usr/bin/env python3
"""
Beispiel für die Verwendung des Website-zu-PDF-Converters als Modul.
"""

from scraper import WebsiteToPDF

def main():
    # Initialisiere den Converter (PDFs werden auf dem Desktop gespeichert)
    converter = WebsiteToPDF()

    # Beispiel-URLs
    urls = [
        'https://example.com',
        'https://de.wikipedia.org/wiki/Python_(Programmiersprache)',
    ]

    # Verarbeite jede URL
    for url in urls:
        try:
            converter.process_url(url)
        except Exception as e:
            print(f"Fehler bei {url}: {e}")
            continue

    print("\nAlle URLs wurden verarbeitet!")


if __name__ == "__main__":
    main()
