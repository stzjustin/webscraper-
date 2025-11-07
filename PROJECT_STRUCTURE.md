# 📁 Projekt-Struktur - Web Scraper Pro

## Übersicht aller Dateien

```
webscraper-/
│
├── 📄 web_scraper_pro.py          # ⭐ HAUPT-SCRAPER (NEU & VERBESSERT)
│   └── Professioneller Web-Scraper mit:
│       - Intelligenter Keyword-Extraktion
│       - Batch-Processing
│       - Retry-Logik
│       - Progress Bars
│       - Strukturiertes Logging
│
├── 📄 scraper.py                  # Original-Scraper (einfache Version)
│   └── Nur für einzelne URLs, keine Crawling-Funktion
│
├── 📋 requirements-pro.txt        # ⭐ Dependencies für PRO-Version
│   └── Alle benötigten Python-Pakete
│
├── 📋 requirements.txt            # Dependencies für Original-Scraper
│
├── ⚙️  web_scraper_pro.spec       # PyInstaller Konfiguration
│   └── Für Erstellung von ausführbaren Dateien
│
├── 🔨 build_mac.sh                # ⭐ Build-Skript für macOS
│   └── Erstellt Standalone-App für Mac (Intel & Silicon)
│
├── 🔨 build_windows.bat           # Build-Skript für Windows
│   └── Erstellt .exe für Windows
│
├── 🔨 build_linux.sh              # Build-Skript für Linux
│   └── Erstellt Executable für Linux
│
├── 🚀 quickstart_mac.sh           # ⭐ SCHNELLSTART für Mac
│   └── One-Click Setup & Run
│
├── ⚙️  config_example.yaml        # Beispiel-Konfiguration
│   └── Umbenennen zu config.yaml zum Nutzen
│
├── 📖 README_PRO.md               # ⭐ AUSFÜHRLICHE ANLEITUNG
│   └── Komplette Dokumentation mit:
│       - Schritt-für-Schritt-Anleitungen
│       - Installation für alle Plattformen
│       - n8n Integration
│       - Troubleshooting
│       - FAQ
│
├── 📖 QUICKSTART.md               # ⭐ 5-MINUTEN SCHNELLSTART
│   └── Speziell für Mac Silicon Chip
│
├── 📖 PROJECT_STRUCTURE.md        # Diese Datei
│   └── Übersicht der Projekt-Struktur
│
├── 📖 README.md                   # Original-README
│   └── Für einfachen scraper.py
│
└── 📄 example.py                  # Beispiel-Code
    └── Zeigt wie man scraper.py nutzt
```

---

## 🎯 Welche Datei brauchst du?

### Als Anfänger (Mac Silicon):
➡️ **Start:** `QUICKSTART.md`
➡️ **Ausführen:** `./quickstart_mac.sh`

### Für andere Plattformen:
➡️ **Anleitung:** `README_PRO.md` (Abschnitt "Detaillierte Installation")

### Executable erstellen:
➡️ **Mac:** `./build_mac.sh`
➡️ **Windows:** `build_windows.bat`
➡️ **Linux:** `./build_linux.sh`

### Code anpassen:
➡️ **Haupt-Code:** `web_scraper_pro.py`
➡️ **Build-Config:** `web_scraper_pro.spec`
➡️ **Einstellungen:** `config_example.yaml` → `config.yaml`

### Hilfe & Support:
➡️ **Alles:** `README_PRO.md`
➡️ **Schnell:** `QUICKSTART.md`
➡️ **FAQ:** `README_PRO.md` (Abschnitt "FAQ")

---

## 🔄 Workflow-Übersicht

### 1️⃣ Entwicklung (Python)

```bash
# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-pro.txt

# Scraper ausführen
python web_scraper_pro.py

# Anpassen
vim web_scraper_pro.py
vim config.yaml
```

### 2️⃣ Build (Executable)

```bash
# Mac
./build_mac.sh
→ dist/WebScraperPro

# Windows
build_windows.bat
→ dist\WebScraperPro.exe

# Linux
./build_linux.sh
→ dist/WebScraperPro
```

### 3️⃣ Distribution

**Mac:**
```bash
# Als App Bundle
sudo cp -r dist/WebScraperPro.app /Applications/

# Als Binary
cp dist/WebScraperPro /usr/local/bin/
```

**Windows:**
- Kopiere `dist/` Ordner zu jedem Windows-PC
- Doppelklick auf `WebScraperPro.exe`

**Linux:**
```bash
sudo cp dist/WebScraperPro /usr/local/bin/
sudo chmod +x /usr/local/bin/WebScraperPro
```

---

## 📦 Output-Struktur

Nach dem Scraping:

```
~/Desktop/WebScraperPDFs/
│
├── 📄 001_20250107_143052_homepage_features_example_com.pdf
├── 📄 002_20250107_143055_pricing_plans_example_com.pdf
├── 📄 003_20250107_143058_contact_support_example_com.pdf
├── ...
│
├── 📋 scraped_urls.json           # Alle gefundenen URLs
│   └── {
│       "start_url": "https://example.com",
│       "timestamp": "2025-01-07T14:30:50",
│       "total_urls": 50,
│       "urls": [...]
│   }
│
└── 📋 scraper_20250107_143050.log # Log-Datei
    └── Alle Events, Fehler, Warnungen
```

---

## 🛠 Development

### Code-Struktur (`web_scraper_pro.py`)

```python
# 1. CONFIGURATION
ScraperConfig           # Dataclass für alle Settings

# 2. LOGGING
ColoredFormatter        # Farbiges Terminal-Logging
setup_logging()         # Logger-Konfiguration

# 3. KEYWORD EXTRACTION
KeywordExtractor        # YAKE-basierte Keyword-Extraktion
├── extract()           # Haupt-Methode
├── _clean_keyword()    # Keyword-Bereinigung
└── _extract_frequent_words()  # Fallback-Methode

# 4. PDF GENERATION
PDFGenerator            # ReportLab PDF-Erstellung
├── create_pdf()        # Haupt-PDF-Erstellung
├── _generate_filename()  # Intelligente Benennung
└── _escape_xml()       # XML-Escaping für ReportLab

# 5. WEB SCRAPING
WebScraper              # Haupt-Scraper-Klasse
├── setup_driver()      # Chrome/Selenium Setup
├── fetch_page()        # Page-Load mit Retry
├── normalize_url()     # URL-Normalisierung
├── extract_links()     # Link-Extraktion
├── extract_text()      # Text-Bereinigung
├── crawl()             # Website-Crawling
├── create_pdfs()       # PDF-Batch-Processing
└── run()               # Haupt-Workflow

# 6. USER INPUT
get_user_input()        # Interaktive URL/Page-Input

# 7. MAIN
main()                  # Entry Point
```

### Anpassungsmöglichkeiten

#### PDF-Layout ändern
```python
# In PDFGenerator._setup_styles()
self.body_style = ParagraphStyle(
    'CustomBody',
    fontSize=12,  # Größer
    textColor=HexColor('#000000'),  # Schwarz
    ...
)
```

#### Keywords anpassen
```python
# In ScraperConfig
num_keywords: int = 5  # Statt 3
keyword_max_ngram: int = 3  # Statt 2 (längere Phrasen)
```

#### Delay ändern
```python
# In ScraperConfig
delay_between_requests: float = 1.0  # Schneller (⚠️ riskant!)
```

#### Ignore-Patterns erweitern
```python
# In ScraperConfig
ignore_patterns: List[str] = [
    "login", "logout", ...,
    "mypattern",  # Dein Pattern
]
```

---

## 🧪 Testing

```bash
# Unit-Tests (TODO)
pytest tests/

# Manueller Test mit kleiner Site
python web_scraper_pro.py
# URL: https://example.com
# Max: 5
```

---

## 🚀 Deployment

### Docker (Optional)

```dockerfile
FROM python:3.11-slim

# Install Chrome
RUN apt-get update && apt-get install -y \
    chromium chromium-driver

WORKDIR /app
COPY requirements-pro.txt .
RUN pip install -r requirements-pro.txt

COPY web_scraper_pro.py .

ENTRYPOINT ["python", "web_scraper_pro.py"]
```

### n8n Integration

Siehe `README_PRO.md` Abschnitt "n8n Integration"

---

## 📊 Features Comparison

| Feature | scraper.py | web_scraper_pro.py |
|---------|------------|---------------------|
| **Einzelne URL** | ✅ | ✅ |
| **Vollständiges Crawling** | ❌ | ✅ |
| **Keyword-Extraktion** | ❌ | ✅ |
| **Intelligente Benennung** | ❌ | ✅ |
| **Batch-Processing** | ❌ | ✅ |
| **Retry-Logik** | ❌ | ✅ |
| **Progress Bars** | ❌ | ✅ |
| **Strukturiertes Logging** | ❌ | ✅ |
| **Konfigurierbar** | ❌ | ✅ |
| **Memory-Optimierung** | ❌ | ✅ |
| **n8n-optimiert** | ⚠️ | ✅ |

➡️ **Empfehlung:** Verwende `web_scraper_pro.py`!

---

## 📝 TODO / Roadmap

- [ ] GUI-Version (Electron/Tkinter)
- [ ] Login-Support für geschützte Seiten
- [ ] Sitemap.xml Parsing
- [ ] Paralleles Crawling (Multi-Threading)
- [ ] Cloud-Storage Integration (S3, Azure)
- [ ] REST API Wrapper
- [ ] Docker Image
- [ ] Unit Tests
- [ ] CI/CD Pipeline

---

## 🤝 Contributing

Pull Requests willkommen!

**Setup:**
```bash
git clone https://github.com/your-repo/webscraper-.git
cd webscraper-
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-pro.txt
pip install black flake8 pytest mypy
```

**Code-Style:**
```bash
# Format
black web_scraper_pro.py

# Lint
flake8 web_scraper_pro.py

# Type-Check
mypy web_scraper_pro.py
```

---

## 📜 License

MIT License - Siehe `LICENSE`

---

**Version:** 2.0
**Last Updated:** 2025-01-07
**Author:** Web Scraper Pro Team
