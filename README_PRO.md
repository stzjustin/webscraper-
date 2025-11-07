# 🚀 Web Scraper Pro v2.0

**Professioneller Website-zu-PDF Converter mit intelligenter Benennung**

Crawle komplette Websites, extrahiere Content und erstelle professionelle PDFs mit automatischer Keyword-Extraktion für intelligente Dateinamen. Perfekt für n8n Workflows, RAG-Systeme und Wissensdatenbanken.

---

## 📋 Inhaltsverzeichnis

- [Features](#-features)
- [Voraussetzungen](#-voraussetzungen)
- [Schnellstart](#-schnellstart-f%C3%BCr-anf%C3%A4nger)
- [Detaillierte Installation](#-detaillierte-installation)
- [Verwendung](#-verwendung)
- [Executable erstellen](#-executable-erstellen-standalone-anwendung)
- [n8n Integration](#-n8n-integration)
- [Troubleshooting](#-troubleshooting)
- [FAQ](#-faq)

---

## ✨ Features

### Kernfunktionen
- ✅ **Vollständiges Website-Crawling** - Findet automatisch alle URLs einer Domain
- ✅ **Intelligente PDF-Benennung** - Extrahiert 2-3 Keywords aus dem Inhalt
- ✅ **Professionelle PDF-Formatierung** - Sauberes Layout mit Metadaten
- ✅ **Batch-Processing** - Effiziente Verarbeitung mit Memory-Optimierung
- ✅ **Retry-Logik** - Automatische Wiederholung bei Fehlern
- ✅ **Progress Bars** - Echtzeit-Fortschrittsanzeige
- ✅ **Konfigurierbar** - Über YAML-Datei oder interaktiv

### PDF-Eigenschaften
Jedes PDF enthält:
- 📍 **URL** der Quelle
- 🕐 **Timestamp** der Erstellung
- 🔑 **2-3 Keywords** über den Inhalt (im Dateinamen UND im PDF)
- 📄 **Seitenzahl** (z.B. "Seite 5 von 50")
- 📝 **Bereinigten Content** (ohne Navigation, Footer, Werbung, etc.)

### Perfekt für
- 🤖 **n8n Workflows** - Automatisierte Dokumentenverarbeitung
- 🧠 **RAG-Systeme** - Retrieval-Augmented Generation
- 💬 **Chatbot-Training** - Pinecone/Weaviate Integration
- 📚 **Knowledge Bases** - Dokumentierte Wissensdatenbanken
- 🔍 **Content-Archivierung** - Website-Backups als PDFs

---

## 🔧 Voraussetzungen

### Alle Plattformen

1. **Python 3.8 oder höher**
   - Überprüfen: `python3 --version` (Mac/Linux) oder `python --version` (Windows)
   - Download: [python.org/downloads](https://www.python.org/downloads/)

2. **Google Chrome Browser**
   - Muss installiert sein (für Selenium)
   - Download: [google.com/chrome](https://www.google.com/chrome/)

3. **ChromeDriver**
   - Wird automatisch installiert via `webdriver-manager`
   - Oder manuell installieren (siehe unten)

### Zusätzlich für macOS

```bash
# Homebrew installieren (falls noch nicht vorhanden)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# ChromeDriver installieren (optional, wenn automatisch nicht funktioniert)
brew install chromedriver
```

### Zusätzlich für Windows

- **Visual C++ Build Tools** (für einige Python-Pakete)
  - Download: [visualstudio.microsoft.com](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
  - Oder installiere "Desktop development with C++" über Visual Studio Installer

### Zusätzlich für Linux

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv chromium-chromedriver

# Fedora/RHEL
sudo dnf install python3 python3-pip chromium chromedriver

# Arch Linux
sudo pacman -S python python-pip chromium chromedriver
```

---

## 🚀 Schnellstart (für Anfänger)

### Schritt 1: Projekt herunterladen

**Option A: Mit Git (empfohlen)**
```bash
git clone https://github.com/your-repo/webscraper-.git
cd webscraper-
```

**Option B: ZIP-Download**
1. Lade das Projekt als ZIP herunter
2. Entpacke es
3. Öffne Terminal/Eingabeaufforderung im Projekt-Ordner

### Schritt 2: Virtual Environment erstellen

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

✅ Du solltest jetzt `(venv)` vor deinem Prompt sehen!

### Schritt 3: Dependencies installieren

```bash
pip install -r requirements-pro.txt
```

⏱️ Dieser Schritt dauert 2-5 Minuten.

### Schritt 4: Scraper starten

```bash
python web_scraper_pro.py
```

### Schritt 5: Interaktive Eingabe

Das Programm fragt dich:

```
Website URL (e.g., https://example.com): https://ihre-website.de
Max URLs to crawl (e.g., 20, 50, 100): 20
```

🎉 **Fertig!** Der Scraper crawlt die Website und erstellt PDFs auf deinem Desktop.

---

## 📚 Detaillierte Installation

### Für Mac (Silicon & Intel)

#### 1. Terminal öffnen
- Drücke `Cmd + Space`
- Tippe "Terminal"
- Drücke Enter

#### 2. In Projekt-Ordner wechseln
```bash
cd ~/Downloads/webscraper-  # Passe den Pfad an!
```

#### 3. Python-Version prüfen
```bash
python3 --version
```

Sollte `Python 3.8.x` oder höher zeigen.

**Falls Python fehlt:**
```bash
# Mit Homebrew installieren
brew install python3
```

#### 4. Virtual Environment erstellen
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 5. Dependencies installieren
```bash
pip install --upgrade pip
pip install -r requirements-pro.txt
```

**Mögliche Fehler beheben:**

- **"command not found: pip"**
  ```bash
  python3 -m pip install --upgrade pip
  ```

- **"Permission denied"**
  - Verwende NICHT `sudo`!
  - Stelle sicher, dass venv aktiviert ist

#### 6. ChromeDriver installieren (falls Fehler)
```bash
brew install chromedriver

# Erlaubnis erteilen (bei Security-Warnung)
xattr -d com.apple.quarantine /opt/homebrew/bin/chromedriver
```

#### 7. Testen
```bash
python web_scraper_pro.py
```

---

### Für Windows

#### 1. Eingabeaufforderung öffnen
- Drücke `Win + R`
- Tippe `cmd`
- Drücke Enter

#### 2. In Projekt-Ordner wechseln
```cmd
cd C:\Users\DeinName\Downloads\webscraper-
```

#### 3. Python-Version prüfen
```cmd
python --version
```

Sollte `Python 3.8.x` oder höher zeigen.

**Falls Python fehlt:**
- Download von [python.org](https://www.python.org/downloads/)
- **Wichtig:** Haken bei "Add Python to PATH" setzen!

#### 4. Virtual Environment erstellen
```cmd
python -m venv venv
venv\Scripts\activate
```

#### 5. Dependencies installieren
```cmd
python -m pip install --upgrade pip
pip install -r requirements-pro.txt
```

**Mögliche Fehler beheben:**

- **"pip is not recognized"**
  ```cmd
  python -m pip install --upgrade pip
  ```

- **Microsoft Visual C++ fehlt**
  - Download: [Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
  - Installiere "Desktop development with C++"

#### 6. ChromeDriver installieren (falls Fehler)
- Download: [chromedriver.chromium.org](https://chromedriver.chromium.org/)
- Wähle Version passend zu deinem Chrome
- Entpacke `chromedriver.exe`
- Kopiere in `C:\Windows\` oder füge zum PATH hinzu

#### 7. Testen
```cmd
python web_scraper_pro.py
```

---

### Für Linux

#### 1. Terminal öffnen
- Drücke `Ctrl + Alt + T`

#### 2. System-Pakete installieren
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv chromium-chromedriver

# Fedora/RHEL
sudo dnf install python3 python3-pip chromium chromedriver

# Arch Linux
sudo pacman -S python python-pip chromium chromedriver
```

#### 3. In Projekt-Ordner wechseln
```bash
cd ~/Downloads/webscraper-  # Passe den Pfad an!
```

#### 4. Virtual Environment erstellen
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 5. Dependencies installieren
```bash
pip install --upgrade pip
pip install -r requirements-pro.txt
```

#### 6. Testen
```bash
python web_scraper_pro.py
```

---

## 💻 Verwendung

### Interaktiver Modus (empfohlen für Anfänger)

```bash
python web_scraper_pro.py
```

Das Programm führt dich durch:
1. URL-Eingabe
2. Maximale Seitenzahl
3. Crawling-Prozess
4. Bestätigung für PDF-Erstellung

### Command-Line Argumente (für Fortgeschrittene)

```bash
# Beispiel mit Umgebungsvariablen
START_URL="https://example.com" MAX_PAGES=50 python web_scraper_pro.py
```

### Mit Konfigurationsdatei

1. Kopiere `config_example.yaml` nach `config.yaml`
2. Bearbeite `config.yaml` mit deinen Einstellungen
3. Starte den Scraper

```bash
cp config_example.yaml config.yaml
# Editiere config.yaml mit deinem Texteditor
python web_scraper_pro.py
```

---

## 📦 Executable erstellen (Standalone-Anwendung)

Erstelle eine ausführbare Datei, die auf JEDEM Computer läuft - **ohne Python-Installation!**

### Für Mac (Silicon & Intel)

```bash
# Executable-Berechtigung erteilen
chmod +x build_mac.sh

# Build starten
./build_mac.sh
```

**Ergebnis:**
- Mac Intel: `dist/WebScraperPro` (funktioniert auf Intel Macs)
- Mac Silicon: `dist/WebScraperPro` (funktioniert auf M1/M2/M3 Macs)
- Optional: `dist/WebScraperPro.app` (macOS App Bundle)

**Starten:**
```bash
./dist/WebScraperPro
```

**System-weit installieren (optional):**
```bash
sudo cp -r dist/WebScraperPro.app /Applications/
```

### Für Windows

```cmd
build_windows.bat
```

**Ergebnis:**
- `dist\WebScraperPro.exe` (Windows-Executable)

**Starten:**
- Doppelklick auf `WebScraperPro.exe` im `dist` Ordner
- Oder via CMD: `dist\WebScraperPro.exe`

**Verteilen:**
- Kopiere den gesamten `dist` Ordner auf jeden Windows-PC
- Keine Python-Installation nötig!

### Für Linux

```bash
# Executable-Berechtigung erteilen
chmod +x build_linux.sh

# Build starten
./build_linux.sh
```

**Ergebnis:**
- `dist/WebScraperPro` (Linux-Executable)

**Starten:**
```bash
./dist/WebScraperPro
```

**System-weit installieren (optional):**
```bash
sudo cp dist/WebScraperPro /usr/local/bin/
sudo chmod +x /usr/local/bin/WebScraperPro
```

Dann von überall: `WebScraperPro`

---

## 🔗 n8n Integration

### Workflow-Übersicht

```
1. HTTP Request (URL-Input)
   ↓
2. Execute Command (Web Scraper Pro)
   ↓
3. Read Binary Files (PDFs einlesen)
   ↓
4. OpenAI/Anthropic (LLM Zusammenfassung)
   ↓
5. Rename Files (mit LLM-Output)
   ↓
6. Google Drive Upload
   ↓
7. Pinecone Embed (Vektorisierung)
```

### n8n Node: Execute Command

**Command:**
```bash
cd /pfad/zu/webscraper- && \
source venv/bin/activate && \
python web_scraper_pro.py --url {{$json["url"]}} --max-pages {{$json["max_pages"]}}
```

**Output:**
- PDFs im Ordner: `~/Desktop/WebScraperPDFs/`
- URL-Liste: `~/Desktop/WebScraperPDFs/scraped_urls.json`

### n8n Node: Read Binary Files

**Path:**
```
~/Desktop/WebScraperPDFs/*.pdf
```

**Property Name:** `data`

### n8n Node: OpenAI/Anthropic

**Prompt:**
```
Fasse den folgenden PDF-Inhalt in 2-3 Sätzen zusammen und extrahiere die 3 wichtigsten Themen:

{{$binary.data}}
```

**Output:** Zusammenfassung + Keywords

### n8n Node: Google Drive Upload

**Filename:**
```javascript
{{$json["keywords"].join("_") + "_" + Date.now() + ".pdf"}}
```

### n8n Node: Pinecone Embed

**Metadata:**
```json
{
  "source": "web_scraper",
  "url": "{{$json["url"]}}",
  "keywords": "{{$json["keywords"]}}",
  "timestamp": "{{$json["timestamp"]}}"
}
```

---

## 🛠 Troubleshooting

### Problem: "Python not found"

**Lösung:**
- Installiere Python von [python.org](https://www.python.org/downloads/)
- Mac/Linux: Verwende `python3` statt `python`
- Windows: Setze "Add Python to PATH" bei Installation

### Problem: "ChromeDriver not found"

**Lösung:**

**Mac:**
```bash
brew install chromedriver
xattr -d com.apple.quarantine /opt/homebrew/bin/chromedriver
```

**Windows:**
- Download von [chromedriver.chromium.org](https://chromedriver.chromium.org/)
- Version muss zu Chrome passen!
- Lege `chromedriver.exe` in `C:\Windows\`

**Linux:**
```bash
sudo apt-get install chromium-chromedriver  # Ubuntu/Debian
```

### Problem: "Module not found"

**Lösung:**
```bash
# Stelle sicher, dass venv aktiviert ist!
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Installiere Requirements neu
pip install -r requirements-pro.txt
```

### Problem: "Permission denied" (Mac)

**Lösung:**
```bash
# ChromeDriver Quarantäne entfernen
xattr -d com.apple.quarantine /opt/homebrew/bin/chromedriver

# Build-Skript ausführbar machen
chmod +x build_mac.sh
```

### Problem: "No PDFs created"

**Mögliche Ursachen:**

1. **Website blockiert Crawler**
   - Lösung: Erhöhe `delay_between_requests` in `config.yaml`

2. **Website verwendet JavaScript**
   - Wird bereits mit Selenium gelöst
   - Falls Probleme: Erhöhe `time.sleep(2)` in `fetch_page()`

3. **Zu wenig Content**
   - Scraper filtert Seiten mit < 10 Zeichen
   - Check Log-Datei im Output-Ordner

### Problem: Build fehlschlägt

**Lösung:**

**Mac:**
```bash
# Xcode Command Line Tools installieren
xcode-select --install
```

**Windows:**
```cmd
# Visual C++ Build Tools installieren
# Download: https://visualstudio.microsoft.com/visual-cpp-build-tools/
```

**Linux:**
```bash
# Development-Pakete installieren
sudo apt-get install python3-dev libxml2-dev libxslt1-dev  # Ubuntu/Debian
```

---

## ❓ FAQ

### Wie lange dauert das Crawling?

**Faustregel:**
- **20 URLs:** ~2-3 Minuten
- **50 URLs:** ~5-10 Minuten
- **100 URLs:** ~15-20 Minuten

Abhängig von:
- `delay_between_requests` (Standard: 2 Sekunden)
- Website-Geschwindigkeit
- Netzwerk-Verbindung

### Kann ich mehrere Websites gleichzeitig crawlen?

Nein, aber du kannst mehrere Instanzen parallel laufen lassen:

```bash
# Terminal 1
python web_scraper_pro.py  # Website 1

# Terminal 2
python web_scraper_pro.py  # Website 2
```

### Wie ändere ich die PDF-Benennung?

Editiere `web_scraper_pro.py`, Methode `_generate_filename()` (Zeile ~486):

```python
def _generate_filename(self, url: str, keywords: List[str], page_number: int) -> str:
    # Deine Custom-Logik hier
    filename = f"{page_number:03d}_{keywords}_{domain}.pdf"
    return filename
```

### Werden Bilder in PDFs gespeichert?

Nein, aktuell nur Text. Bilder werden übersprungen für:
- Kleinere Dateigröße
- Schnelleres Processing
- Bessere LLM-Verarbeitung

**Bilder aktivieren:** Entferne `--disable-images` in `setup_driver()`.

### Funktioniert das mit Login-geschützten Seiten?

Nein, aktuell werden nur öffentliche Seiten unterstützt.

**Workaround:** Speichere Cookies in Selenium und lade sie.

### Wie kann ich nur bestimmte URLs crawlen?

Editiere `config.yaml` und füge Patterns zu `ignore_patterns` hinzu:

```yaml
ignore_patterns:
  - "blog"      # Ignoriert alle /blog/* URLs
  - "news"      # Ignoriert alle /news/* URLs
  - "download"  # Ignoriert alle /download/* URLs
```

### Kann ich das auf einem Server laufen lassen?

Ja! Headless-Chrome ist aktiviert. Für Server:

```bash
# Ubuntu Server
sudo apt-get install chromium-browser chromium-chromedriver xvfb

# Mit xvfb starten (falls Display-Fehler)
xvfb-run python web_scraper_pro.py
```

### Wie erhöhe ich die Geschwindigkeit?

1. **Reduziere Delay:**
   ```yaml
   delay_between_requests: 1.0  # Statt 2.0
   ```

2. **Erhöhe Batch-Size:**
   ```yaml
   batch_size: 50  # Statt 25
   ```

3. **Deaktiviere Bilder:** (bereits Standard)

⚠️ **Achtung:** Zu aggressives Crawling kann zur IP-Blockierung führen!

### Unterstützt das Scraper JavaScript-Websites?

Ja! Selenium lädt JavaScript automatisch. Falls Probleme:

Erhöhe Wartezeit in `fetch_page()`:
```python
time.sleep(5)  # Statt 2
```

---

## 📊 Output-Struktur

### Desktop-Ordner

```
~/Desktop/WebScraperPDFs/
├── 001_20250107_143052_homepage_features_example_com.pdf
├── 002_20250107_143055_pricing_plans_example_com.pdf
├── 003_20250107_143058_contact_support_example_com.pdf
├── ...
├── scraped_urls.json
└── scraper_20250107_143050.log
```

### PDF-Dateiname-Format

```
{Nummer}_{Timestamp}_{Keyword1}_{Keyword2}_{Keyword3}_{Domain}.pdf
```

**Beispiel:**
```
025_20250107_143052_datenschutz_privacy_policy_example_com.pdf
```

### scraped_urls.json

```json
{
  "start_url": "https://example.com",
  "timestamp": "2025-01-07T14:30:50",
  "total_urls": 50,
  "urls": [
    "https://example.com",
    "https://example.com/about",
    "https://example.com/products",
    ...
  ]
}
```

### Log-Datei

```
2025-01-07 14:30:50 - INFO: Starting crawl: https://example.com
2025-01-07 14:30:52 - INFO: [1] Crawle: https://example.com
2025-01-07 14:30:55 - INFO: [2] Crawle: https://example.com/about
...
2025-01-07 14:45:20 - INFO: Crawling complete! Found 50 unique URLs
```

---

## 🎯 Best Practices

### 1. Sei respektvoll zu Servern

```yaml
delay_between_requests: 2.0  # Minimum!
```

- Überlaste keine Server
- Crawle nur tagsüber (für geschäftliche Websites)
- Verwende niemals < 1.0 Sekunden Delay

### 2. Teste mit kleinen Mengen

Starte mit 5-10 URLs:
```bash
Max URLs to crawl: 10
```

### 3. Prüfe robots.txt

```
https://example.com/robots.txt
```

Respektiere `Disallow`-Regeln.

### 4. Backup von URLs

Die `scraped_urls.json` ist wertvoll! Sichere sie:
```bash
cp ~/Desktop/WebScraperPDFs/scraped_urls.json ~/Backups/
```

### 5. Überwache Logs

Bei Problemen: Check Log-Datei im Output-Ordner.

### 6. Verwende Virtual Environment

**Immer!** Sonst werden globale Python-Pakete durcheinander gebracht.

---

## 📞 Support & Contribution

### Probleme melden

Erstelle ein Issue auf GitHub mit:
- Python-Version
- Betriebssystem
- Log-Datei
- Schritte zur Reproduktion

### Contributions

Pull Requests sind willkommen!

**Entwickler-Setup:**
```bash
git clone https://github.com/your-repo/webscraper-.git
cd webscraper-
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-pro.txt
pip install black flake8 pytest  # Dev-Dependencies
```

---

## 📜 Lizenz

MIT License - Siehe `LICENSE` Datei.

---

## 🙏 Credits

Erstellt mit:
- [Selenium](https://www.selenium.dev/) - Web Automation
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - HTML Parsing
- [ReportLab](https://www.reportlab.com/) - PDF Generation
- [YAKE](https://github.com/LIAAD/yake) - Keyword Extraction
- [tqdm](https://github.com/tqdm/tqdm) - Progress Bars

---

## 🚀 Quick Reference

### Kommandos auf einen Blick

```bash
# Setup
python3 -m venv venv
source venv/bin/activate              # Mac/Linux
venv\Scripts\activate                 # Windows
pip install -r requirements-pro.txt

# Scraper starten
python web_scraper_pro.py

# Executable bauen
./build_mac.sh                        # Mac
build_windows.bat                     # Windows
./build_linux.sh                      # Linux

# Deaktivieren
deactivate
```

### Wichtige Dateien

- `web_scraper_pro.py` - Haupt-Scraper
- `requirements-pro.txt` - Dependencies
- `config_example.yaml` - Konfiguration (Optional)
- `build_mac.sh` / `build_windows.bat` / `build_linux.sh` - Build-Skripte
- `web_scraper_pro.spec` - PyInstaller-Konfiguration

---

**Viel Erfolg mit dem Web Scraper Pro! 🎉**

Bei Fragen: Issues auf GitHub oder Email an support@example.com
