# Website zu PDF Converter

Ein Python-Tool zum Herunterladen, Bereinigen und Konvertieren von Website-Inhalten in PDF-Dateien.

## Features

- Lädt beliebige Websites herunter
- Bereinigt HTML-Inhalt (entfernt Scripts, Styles, Navigation, Footer, etc.)
- Konvertiert bereinigte Inhalte in gut formatierte PDFs
- Speichert PDFs automatisch in einem Ordner auf dem Desktop
- Professionelles PDF-Layout mit anpassbarem Styling
- Einfache Kommandozeilen-Bedienung

## Installation

### Voraussetzungen

- Python 3.8 oder höher
- pip (Python Package Manager)

### Schritt 1: Repository klonen oder herunterladen

```bash
git clone <repository-url>
cd webscraper-
```

### Schritt 2: Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

**Hinweis für Linux-Benutzer:** WeasyPrint benötigt zusätzliche System-Bibliotheken:

```bash
# Ubuntu/Debian
sudo apt-get install python3-pip python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0

# Fedora/RHEL
sudo dnf install python3-pip python3-cffi python3-brotli pango

# Arch Linux
sudo pacman -S python-pip python-cffi python-brotli pango
```

**Hinweis für macOS-Benutzer:**

```bash
brew install pango
```

## Verwendung

### Methode 1: Interaktiver Modus

Führe das Skript aus und gib die URL ein, wenn du danach gefragt wirst:

```bash
python scraper.py
```

### Methode 2: URL als Parameter

Übergebe die URL direkt als Kommandozeilen-Parameter:

```bash
python scraper.py https://example.com
```

### Beispiele

```bash
# Beispiel 1: Wikipedia-Artikel
python scraper.py https://de.wikipedia.org/wiki/Python_(Programmiersprache)

# Beispiel 2: Nachrichtenartikel
python scraper.py https://www.tagesschau.de

# Beispiel 3: GitHub README
python scraper.py https://github.com/python/cpython
```

## Ausgabe

Die PDFs werden automatisch gespeichert in:

- **Windows:** `C:\Users\<Benutzername>\Desktop\WebsiteScraperPDFs\`
- **macOS:** `/Users/<Benutzername>/Desktop/WebsiteScraperPDFs/`
- **Linux:** `/home/<Benutzername>/Desktop/WebsiteScraperPDFs/`

Dateiname-Format: `<domain>_<timestamp>.pdf`

Beispiel: `de_wikipedia_org_wiki_Python_Programmiersprache_20250107_143052.pdf`

## Verwendung in eigenen Projekten

Du kannst die `WebsiteToPDF`-Klasse auch in eigenen Python-Projekten verwenden:

```python
from scraper import WebsiteToPDF

# Converter initialisieren
converter = WebsiteToPDF()

# Einzelne URL verarbeiten
converter.process_url('https://example.com')

# Eigenes Ausgabeverzeichnis angeben
converter = WebsiteToPDF(output_dir='/path/to/custom/directory')
converter.process_url('https://example.com')
```

## RAG-Integration (n8n)

Dieses Tool eignet sich perfekt für RAG (Retrieval-Augmented Generation) Systeme:

1. Website-Inhalte werden bereinigt und strukturiert
2. PDFs können einfach in Retrieval-Systeme integriert werden
3. Ideal für Dokumenten-basierte KI-Workflows in n8n

### n8n Workflow-Beispiel

1. HTTP Request Node: URL-Input
2. Execute Command Node: `python scraper.py {URL}`
3. Read Binary File Node: PDF einlesen
4. Weiterverarbeitung im RAG-System

## Was wird bereinigt?

Das Skript entfernt folgende Elemente für bessere Lesbarkeit:

- JavaScript-Code (`<script>`)
- CSS-Styles (`<style>`)
- Navigationsmenüs (`<nav>`)
- Footer-Bereiche (`<footer>`)
- Header-Bereiche (`<header>`)
- iFrames (`<iframe>`)
- HTML-Kommentare
- Leere Elemente ohne Inhalt

## Anpassungen

### PDF-Styling ändern

Das CSS für das PDF-Layout findest du in der Datei `scraper.py` in der Methode `convert_to_pdf()`.

Beispiel-Anpassungen:

```python
# Schriftgröße ändern
body { font-size: 14pt; }

# Seitenränder anpassen
@page { margin: 3cm; }

# Seitengröße ändern
@page { size: Letter; }
```

### Ausgabeordner ändern

Im Code anpassen:

```python
converter = WebsiteToPDF(output_dir='/custom/path')
```

## Fehlerbehebung

### Problem: "Module not found"

```bash
pip install -r requirements.txt --upgrade
```

### Problem: WeasyPrint-Installation schlägt fehl

Stelle sicher, dass alle System-Abhängigkeiten installiert sind (siehe Installation).

### Problem: Timeout-Fehler

Erhöhe den Timeout-Wert in `scraper.py`:

```python
response = requests.get(url, headers=headers, timeout=60)  # 60 Sekunden
```

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz.

## Beiträge

Pull Requests und Issues sind willkommen! 
