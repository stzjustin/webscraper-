# ⚡ QUICKSTART - Web Scraper Pro

**5-Minuten Setup für Anfänger - Dein Mac mit Silicon Chip**

---

## 🎯 Was du bekommst

✅ Crawle komplette Websites automatisch
✅ Erstelle PDFs mit intelligenten Namen (inkl. Keywords)
✅ Perfekt für n8n → LLM → Google Drive → Pinecone Workflows
✅ Ausführbare Anwendung (läuft ohne Python-Installation)

---

## 🚀 Schnellster Start (5 Minuten)

### Schritt 1: Terminal öffnen
1. Drücke `Cmd + Space`
2. Tippe: `terminal`
3. Drücke `Enter`

### Schritt 2: In Projekt-Ordner wechseln
```bash
cd ~/Downloads/webscraper-  # Oder wo auch immer du es gespeichert hast
```

### Schritt 3: Quickstart-Skript ausführen
```bash
./quickstart_mac.sh
```

**Das war's! 🎉**

Das Skript:
- ✅ Prüft Python
- ✅ Erstellt Virtual Environment
- ✅ Installiert alle Dependencies
- ✅ Startet den Scraper

---

## 📝 Verwendung

Nach dem Start fragt das Programm:

```
Website URL (e.g., https://example.com):
```
➡️ Gib deine Website ein, z.B. `https://ihre-website.de`

```
Max URLs to crawl (e.g., 20, 50, 100):
```
➡️ Gib die Anzahl ein, z.B. `20`

```
20 URLs found and saved.
Create PDFs now? (yes/no):
```
➡️ Tippe `yes` und drücke Enter

✅ **Fertig!** PDFs werden erstellt und auf deinem Desktop gespeichert:
`~/Desktop/WebScraperPDFs/`

---

## 📦 Als Standalone-App erstellen

### Für deinen Mac (Silicon)

```bash
./build_mac.sh
```

**Ergebnis:** `dist/WebScraperPro`

**Starten:**
```bash
./dist/WebScraperPro
```

**Optional - Als App installieren:**
```bash
sudo cp -r dist/WebScraperPro.app /Applications/
```

Dann findest du es in deinen Anwendungen! 🎉

---

## 🔁 Beim nächsten Mal starten

### Option 1: Mit Virtual Environment
```bash
cd ~/Downloads/webscraper-
source venv/bin/activate
python web_scraper_pro.py
```

### Option 2: Quickstart-Skript (einfacher!)
```bash
cd ~/Downloads/webscraper-
./quickstart_mac.sh
```

### Option 3: Standalone-App (nach Build)
```bash
./dist/WebScraperPro
```

Oder doppelklick auf `WebScraperPro.app` im Finder!

---

## 💡 Beispiel-Workflow

### Für eine Yoga-Studio-Website

```bash
Website URL: https://yoga-studio-beispiel.de
Max URLs: 30

# Scraper findet automatisch:
# - Homepage
# - Über uns
# - Kurse
# - Preise
# - Kontakt
# - Blog-Artikel
# - usw.

# Erstellt PDFs wie:
# 001_20250107_143052_yoga_kurse_studio_yoga-studio-beispiel_de.pdf
# 002_20250107_143055_preise_mitgliedschaft_yoga-studio-beispiel_de.pdf
# 003_20250107_143058_kontakt_anfahrt_yoga-studio-beispiel_de.pdf
```

### Diese PDFs dann:
1. ➡️ n8n Workflow
2. ➡️ LLM (OpenAI/Anthropic) für Zusammenfassung
3. ➡️ Umbenennen mit LLM-Output
4. ➡️ Google Drive Upload
5. ➡️ Pinecone Embedding für Chatbot

---

## ❓ Häufige Probleme

### "Python not found"
**Lösung:**
```bash
brew install python3
```

### "Chrome not found"
**Lösung:** Installiere Chrome:
[google.com/chrome](https://www.google.com/chrome/)

### "Permission denied"
**Lösung:**
```bash
chmod +x quickstart_mac.sh
./quickstart_mac.sh
```

### "ChromeDriver Fehler"
**Lösung:**
```bash
brew install chromedriver
xattr -d com.apple.quarantine /opt/homebrew/bin/chromedriver
```

---

## 📊 Output

### Desktop-Ordner
```
~/Desktop/WebScraperPDFs/
├── 001_..._keywords_domain.pdf  ← Seitennummer, Timestamp, Keywords, Domain
├── 002_..._keywords_domain.pdf
├── ...
├── scraped_urls.json            ← Alle gefundenen URLs
└── scraper_....log              ← Log-Datei
```

### PDF-Inhalt
Jedes PDF enthält:
- 📍 URL
- 🕐 Timestamp
- 🔑 3 Keywords (im Dateinamen UND im PDF)
- 📄 Seitenzahl (z.B. "Seite 5 von 30")
- 📝 Bereinigten Content

---

## 🎯 Best Practice für n8n

### 1. Kleine Mengen testen
```
Max URLs: 10  # Statt 100
```

### 2. Zeitplan einrichten
Crawle nachts oder zu ruhigen Zeiten

### 3. Delay erhöhen für große Sites
```yaml
# In config.yaml
delay_between_requests: 3.0  # Statt 2.0
```

### 4. URLs sichern
```bash
cp ~/Desktop/WebScraperPDFs/scraped_urls.json ~/Backups/
```

---

## 📚 Weitere Infos

**Ausführliche Anleitung:**
➡️ Siehe `README_PRO.md`

**n8n Integration:**
➡️ Siehe Kapitel "n8n Integration" in `README_PRO.md`

**Troubleshooting:**
➡️ Siehe Kapitel "Troubleshooting" in `README_PRO.md`

**Konfiguration:**
➡️ Kopiere `config_example.yaml` zu `config.yaml` und editiere

---

## 🆘 Support

**Problem gefunden?**
Erstelle ein Issue auf GitHub mit:
- Python-Version (`python3 --version`)
- macOS-Version (`sw_vers`)
- Log-Datei (aus `~/Desktop/WebScraperPDFs/`)

---

## 🎉 Du bist startklar!

```bash
./quickstart_mac.sh
```

**Viel Erfolg mit deinem Web Scraper Pro!**

---

## 📋 Cheat Sheet

```bash
# Setup (nur einmal)
./quickstart_mac.sh

# Scraper starten
python web_scraper_pro.py

# Executable bauen
./build_mac.sh

# Virtual Environment aktivieren
source venv/bin/activate

# Virtual Environment deaktivieren
deactivate

# Dependencies neu installieren
pip install -r requirements-pro.txt

# ChromeDriver installieren
brew install chromedriver
xattr -d com.apple.quarantine /opt/homebrew/bin/chromedriver
```

---

**🚀 Viel Erfolg!**
