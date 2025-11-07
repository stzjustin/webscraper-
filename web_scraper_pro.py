#!/usr/bin/env python3
"""
Professional Web Scraper to PDF Converter
========================================
Crawls websites, extracts content, and creates PDFs with intelligent naming
using keyword extraction. Optimized for n8n workflows and RAG systems.

Author: Professional Web Scraper Team
Version: 2.0
"""

import os
import sys
import time
import json
import logging
from pathlib import Path
from datetime import datetime
from urllib.parse import urljoin, urlparse, urlunparse
from typing import List, Set, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
import re
from collections import Counter

# Third-party imports
import requests
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, WebDriverException
from tqdm import tqdm
import yake  # For keyword extraction


# ============================================================================
# CONFIGURATION
# ============================================================================

@dataclass
class ScraperConfig:
    """Configuration for the web scraper"""
    start_url: str = ""
    max_pages: int = 50
    output_folder: Path = Path.home() / "Desktop" / "WebScraperPDFs"
    delay_between_requests: float = 2.0
    timeout: int = 30
    batch_size: int = 25
    max_retries: int = 3
    retry_delay: int = 5

    # Keyword extraction settings
    num_keywords: int = 3
    keyword_max_ngram: int = 2

    # Patterns to ignore
    ignore_patterns: List[str] = None

    def __post_init__(self):
        if self.ignore_patterns is None:
            self.ignore_patterns = [
                "login", "logout", "register", "newsletter", "redirect",
                "wp-json", "feed", "trackback", "xmlrpc", "search",
                "page=", "paged=", "sort=", "filter=", "cart", "checkout"
            ]

        # Ensure output folder exists
        self.output_folder = Path(self.output_folder)
        self.output_folder.mkdir(parents=True, exist_ok=True)

    def save(self, filepath: Path):
        """Save configuration to JSON"""
        with open(filepath, 'w', encoding='utf-8') as f:
            config_dict = asdict(self)
            config_dict['output_folder'] = str(config_dict['output_folder'])
            json.dump(config_dict, f, indent=2)

    @classmethod
    def load(cls, filepath: Path):
        """Load configuration from JSON"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if 'output_folder' in data:
                data['output_folder'] = Path(data['output_folder'])
            return cls(**data)


# ============================================================================
# LOGGING SETUP
# ============================================================================

class ColoredFormatter(logging.Formatter):
    """Colored log formatter for terminal output"""

    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
    }
    RESET = '\033[0m'

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{log_color}{record.levelname}{self.RESET}"
        return super().format(record)


def setup_logging(output_folder: Path) -> logging.Logger:
    """Setup logging with file and console handlers"""
    logger = logging.getLogger('WebScraperPro')
    logger.setLevel(logging.INFO)

    # Remove existing handlers
    logger.handlers.clear()

    # File handler
    log_file = output_folder / f"scraper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)

    # Console handler with colors
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = ColoredFormatter(
        '%(levelname)s: %(message)s'
    )
    console_handler.setFormatter(console_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# ============================================================================
# KEYWORD EXTRACTOR
# ============================================================================

class KeywordExtractor:
    """Extracts keywords from text for intelligent PDF naming"""

    def __init__(self, num_keywords: int = 3, max_ngram_size: int = 2):
        """
        Initialize keyword extractor

        Args:
            num_keywords: Number of keywords to extract
            max_ngram_size: Maximum n-gram size (1=single words, 2=two-word phrases)
        """
        self.num_keywords = num_keywords
        self.kw_extractor = yake.KeywordExtractor(
            lan="de",  # German language (change to "en" for English)
            n=max_ngram_size,
            dedupLim=0.9,
            top=num_keywords,
            features=None
        )

    def extract(self, text: str) -> List[str]:
        """
        Extract keywords from text

        Args:
            text: Input text

        Returns:
            List of keywords (2-3 words)
        """
        if not text or len(text.strip()) < 50:
            return ["content"]

        try:
            # Extract keywords using YAKE
            keywords = self.kw_extractor.extract_keywords(text)

            # Get keyword strings (without scores)
            keyword_list = []
            for kw, score in keywords:
                # Clean keyword
                cleaned = self._clean_keyword(kw)
                if cleaned and len(cleaned) >= 3:
                    keyword_list.append(cleaned)

            # If not enough keywords, try simple frequency-based extraction
            if len(keyword_list) < 2:
                keyword_list.extend(self._extract_frequent_words(text))

            # Limit to num_keywords
            return keyword_list[:self.num_keywords] if keyword_list else ["content"]

        except Exception as e:
            logging.warning(f"Keyword extraction failed: {e}")
            return self._extract_frequent_words(text)[:self.num_keywords]

    def _clean_keyword(self, keyword: str) -> str:
        """Clean and normalize keyword"""
        # Remove special characters but keep spaces and hyphens
        cleaned = re.sub(r'[^\w\s\-äöüÄÖÜß]', '', keyword)
        # Remove extra whitespace
        cleaned = ' '.join(cleaned.split())
        return cleaned.lower()

    def _extract_frequent_words(self, text: str) -> List[str]:
        """Fallback: Extract most frequent meaningful words"""
        # Stopwords (basic German/English)
        stopwords = {
            'der', 'die', 'das', 'den', 'dem', 'des', 'ein', 'eine', 'einer', 'eines',
            'und', 'oder', 'aber', 'mit', 'für', 'auf', 'in', 'zu', 'von', 'nach',
            'the', 'a', 'an', 'and', 'or', 'but', 'with', 'for', 'on', 'in', 'to', 'of',
            'ist', 'sind', 'wird', 'werden', 'kann', 'könnte', 'sollte',
            'is', 'are', 'was', 'were', 'can', 'could', 'should', 'would'
        }

        # Extract words
        words = re.findall(r'\b[a-zA-ZäöüÄÖÜß]{4,}\b', text.lower())

        # Filter stopwords and count
        filtered_words = [w for w in words if w not in stopwords]
        word_counts = Counter(filtered_words)

        # Get most common
        return [word for word, count in word_counts.most_common(5)]


# ============================================================================
# PDF GENERATOR
# ============================================================================

class PDFGenerator:
    """Generates PDFs with professional formatting and metadata"""

    def __init__(self, output_folder: Path, keyword_extractor: KeywordExtractor):
        """
        Initialize PDF generator

        Args:
            output_folder: Output directory for PDFs
            keyword_extractor: KeywordExtractor instance
        """
        self.output_folder = output_folder
        self.keyword_extractor = keyword_extractor
        self.styles = getSampleStyleSheet()
        self._setup_styles()

    def _setup_styles(self):
        """Setup custom PDF styles"""
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            textColor=HexColor('#2c3e50'),
            spaceAfter=12,
            fontName='Helvetica-Bold'
        )

        self.meta_style = ParagraphStyle(
            'MetaData',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=HexColor('#7f8c8d'),
            spaceAfter=6,
            fontName='Helvetica-Oblique'
        )

        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['BodyText'],
            fontSize=10,
            textColor=HexColor('#2c3e50'),
            spaceAfter=8,
            leading=14,
            fontName='Helvetica'
        )

        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=12,
            textColor=HexColor('#34495e'),
            spaceAfter=10,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )

    def create_pdf(
        self,
        text_content: str,
        url: str,
        page_number: int,
        total_pages: int
    ) -> Optional[Path]:
        """
        Create a PDF with intelligent naming

        Args:
            text_content: Main text content
            url: Source URL
            page_number: Current page number
            total_pages: Total number of pages

        Returns:
            Path to created PDF or None if failed
        """
        try:
            # Extract keywords for filename
            keywords = self.keyword_extractor.extract(text_content)

            # Generate filename
            filename = self._generate_filename(url, keywords, page_number)
            output_path = self.output_folder / filename

            # Create PDF document
            doc = SimpleDocTemplate(
                str(output_path),
                pagesize=A4,
                rightMargin=0.75*inch,
                leftMargin=0.75*inch,
                topMargin=0.75*inch,
                bottomMargin=0.75*inch
            )

            # Build story
            story = []

            # Header with metadata
            story.append(Paragraph(f"<b>Web Scraper Pro - Seite {page_number}/{total_pages}</b>", self.title_style))

            # Metadata
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            keywords_str = ", ".join(keywords)

            story.append(Paragraph(f"<b>URL:</b> {self._escape_xml(url)}", self.meta_style))
            story.append(Paragraph(f"<b>Erstellt:</b> {timestamp}", self.meta_style))
            story.append(Paragraph(f"<b>Schlüsselwörter:</b> {keywords_str}", self.meta_style))
            story.append(Spacer(1, 0.2*inch))

            # Divider
            story.append(Paragraph("─" * 80, self.meta_style))
            story.append(Spacer(1, 0.3*inch))

            # Main content
            if text_content:
                # Split into paragraphs
                paragraphs = text_content.split('\n')

                for para in paragraphs:
                    para = para.strip()
                    if not para:
                        story.append(Spacer(1, 0.1*inch))
                        continue

                    # Escape XML special characters
                    para = self._escape_xml(para)

                    # Check if it looks like a heading (short and capitalized)
                    if len(para) < 100 and para.isupper():
                        story.append(Paragraph(para, self.heading_style))
                    else:
                        # Split long paragraphs
                        if len(para) > 500:
                            sentences = re.split(r'(?<=[.!?])\s+', para)
                            for sentence in sentences:
                                if sentence.strip():
                                    story.append(Paragraph(sentence.strip(), self.body_style))
                        else:
                            story.append(Paragraph(para, self.body_style))
            else:
                story.append(Paragraph("<i>Kein Textinhalt verfügbar</i>", self.body_style))

            # Footer
            story.append(Spacer(1, 0.3*inch))
            story.append(Paragraph("─" * 80, self.meta_style))
            story.append(Paragraph(
                f"<i>Seite {page_number} von {total_pages} | Web Scraper Pro v2.0</i>",
                self.meta_style
            ))

            # Build PDF
            doc.build(story)

            return output_path

        except Exception as e:
            logging.error(f"PDF creation failed: {e}")
            return None

    def _generate_filename(self, url: str, keywords: List[str], page_number: int) -> str:
        """
        Generate intelligent filename with timestamp, page number, and keywords

        Args:
            url: Source URL
            keywords: Extracted keywords
            page_number: Page number

        Returns:
            Filename string
        """
        # Extract domain
        domain = urlparse(url).netloc.replace('www.', '')
        domain = re.sub(r'[^\w\-]', '_', domain)[:30]

        # Clean keywords for filename
        keyword_str = "_".join(keywords)[:50]  # Limit length
        keyword_str = re.sub(r'[^\w\s\-]', '', keyword_str)
        keyword_str = re.sub(r'\s+', '_', keyword_str)

        # Timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Combine: pagenum_timestamp_keywords_domain.pdf
        filename = f"{page_number:03d}_{timestamp}_{keyword_str}_{domain}.pdf"

        # Ensure it's not too long
        if len(filename) > 150:
            filename = f"{page_number:03d}_{timestamp}_{domain}.pdf"

        return filename

    def _escape_xml(self, text: str) -> str:
        """Escape XML special characters for ReportLab"""
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        return text


# ============================================================================
# WEB SCRAPER
# ============================================================================

class WebScraper:
    """Professional web scraper with Selenium and intelligent content extraction"""

    def __init__(self, config: ScraperConfig, logger: logging.Logger):
        """
        Initialize web scraper

        Args:
            config: ScraperConfig instance
            logger: Logger instance
        """
        self.config = config
        self.logger = logger
        self.driver = None
        self.keyword_extractor = KeywordExtractor(
            num_keywords=config.num_keywords,
            max_ngram_size=config.keyword_max_ngram
        )
        self.pdf_generator = PDFGenerator(config.output_folder, self.keyword_extractor)

        # Statistics
        self.stats = {
            'urls_crawled': 0,
            'pdfs_created': 0,
            'errors': 0,
            'start_time': None,
            'end_time': None
        }

    def setup_driver(self) -> webdriver.Chrome:
        """Setup Chrome driver with optimized options"""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-images")
            chrome_options.add_argument("--disable-background-networking")
            chrome_options.add_argument("--disable-default-apps")
            chrome_options.add_argument("--disable-sync")
            chrome_options.add_argument("--disable-translate")
            chrome_options.add_argument("--mute-audio")
            chrome_options.add_argument("--no-first-run")
            chrome_options.add_argument("--no-default-browser-check")
            chrome_options.add_argument("--disable-notifications")
            chrome_options.add_argument(
                "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )

            # Memory optimization
            chrome_options.add_argument("--disable-web-resources")
            chrome_options.add_argument("--disable-plugins")

            driver = webdriver.Chrome(options=chrome_options)
            driver.set_page_load_timeout(self.config.timeout)

            self.logger.info("✓ Chrome driver initialized successfully")
            return driver

        except Exception as e:
            self.logger.error(f"Failed to initialize Chrome driver: {e}")
            self.logger.error(
                "\nPlease install ChromeDriver:\n"
                "  Mac: brew install chromedriver\n"
                "  Linux: sudo apt-get install chromium-chromedriver\n"
                "  Windows: Download from https://chromedriver.chromium.org/"
            )
            sys.exit(1)

    def fetch_page(self, url: str, retry_count: int = 0) -> Optional[str]:
        """
        Fetch page content with retry logic

        Args:
            url: URL to fetch
            retry_count: Current retry attempt

        Returns:
            HTML content or None if failed
        """
        try:
            self.driver.get(url)
            time.sleep(2)  # Wait for JavaScript
            html = self.driver.page_source
            return html

        except (TimeoutException, WebDriverException) as e:
            retry_count += 1

            if retry_count < self.config.max_retries:
                self.logger.warning(
                    f"Attempt {retry_count}/{self.config.max_retries} failed for {url}: {e}"
                )
                time.sleep(self.config.retry_delay)

                # Restart driver if needed
                try:
                    self.driver.quit()
                    time.sleep(2)
                    self.driver = self.setup_driver()
                    return self.fetch_page(url, retry_count)
                except Exception:
                    return None
            else:
                self.logger.error(f"All retry attempts failed for {url}")
                self.stats['errors'] += 1
                return None

    def normalize_url(self, url: str) -> str:
        """Normalize URL for consistency"""
        try:
            parsed = urlparse(url)
            # Prefer HTTPS
            if parsed.scheme == 'http':
                parsed = parsed._replace(scheme='https')
            # Remove trailing slash
            path = parsed.path.rstrip('/')
            if not path:
                path = '/'
            normalized = urlunparse((parsed.scheme, parsed.netloc, path, '', '', ''))
            return normalized
        except Exception:
            return url

    def should_ignore_url(self, url: str) -> bool:
        """Check if URL should be ignored"""
        url_lower = url.lower()
        return any(pattern in url_lower for pattern in self.config.ignore_patterns)

    def is_same_domain(self, url: str, base_domain: str) -> bool:
        """Check if URL is from the same domain"""
        return base_domain in urlparse(url).netloc

    def extract_links(self, html: str, page_url: str, base_domain: str) -> Set[str]:
        """Extract all links from HTML"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            links = set()

            for link in soup.find_all('a', href=True):
                href = link['href']

                # Skip anchors and empty hrefs
                if href.startswith('#') or not href.strip():
                    continue

                # Make absolute URL
                full_url = urljoin(page_url, href)
                full_url = self.normalize_url(full_url)

                # Filter
                if self.should_ignore_url(full_url):
                    continue

                if self.is_same_domain(full_url, base_domain):
                    links.add(full_url)

            return links

        except Exception as e:
            self.logger.warning(f"Link extraction failed: {e}")
            return set()

    def extract_text(self, html: str) -> str:
        """Extract and clean text from HTML"""
        try:
            soup = BeautifulSoup(html, 'html.parser')

            # Remove unwanted elements
            for element in soup(['script', 'style', 'meta', 'link', 'noscript', 'svg']):
                element.decompose()

            # Remove navigation, header, footer
            for element in soup(['nav', 'footer', 'header', 'aside']):
                element.decompose()

            # Remove tables (often schedules/timetables)
            for element in soup(['table', 'tbody', 'thead', 'tr', 'td', 'th']):
                element.decompose()

            # Remove elements with specific classes/IDs (schedules, calendars, etc.)
            for element in soup.find_all(['div', 'section']):
                try:
                    class_name = ' '.join(element.get('class', []) or [])
                    elem_id = element.get('id', '') or ''

                    filter_words = [
                        'schedule', 'timetable', 'kursplan', 'course', 'zeitplan',
                        'booking', 'calendar', 'datepicker', 'event', 'kalender',
                        'termin', 'buchen', 'reservation', 'availability'
                    ]

                    if any(word in class_name.lower() or word in elem_id.lower()
                           for word in filter_words):
                        element.decompose()
                except Exception:
                    pass

            # Extract text
            text = soup.get_text(separator='\n', strip=True)

            # Clean lines
            lines = []
            for line in text.split('\n'):
                line = line.strip()

                # Skip empty lines
                if not line:
                    continue

                # Skip lines with too many colons (likely structured data)
                if line.count(':') > 5:
                    continue

                # Skip lines with many dates (schedules)
                if len(re.findall(r'\d{1,2}\.\d{1,2}', line)) > 5:
                    continue

                # Skip lines with too many weekdays
                weekdays = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun',
                           'montag', 'dienstag', 'mittwoch', 'donnerstag',
                           'freitag', 'samstag', 'sonntag']
                words = line.lower().split()
                weekday_count = sum(1 for w in words if w in weekdays)

                if weekday_count > 3:
                    continue

                lines.append(line)

            return '\n'.join(lines)

        except Exception as e:
            self.logger.error(f"Text extraction failed: {e}")
            return ""

    def crawl(self) -> List[str]:
        """
        Crawl website and collect URLs

        Returns:
            List of URLs found
        """
        base_domain = urlparse(self.config.start_url).netloc
        visited = set()
        to_visit = [self.normalize_url(self.config.start_url)]
        all_urls = []

        self.logger.info(f"Starting crawl: {self.config.start_url}")
        self.logger.info(f"Max pages: {self.config.max_pages}")
        self.logger.info(f"Output folder: {self.config.output_folder}\n")

        # Progress bar
        pbar = tqdm(total=self.config.max_pages, desc="Crawling", unit="page")

        while to_visit and len(all_urls) < self.config.max_pages:
            url = to_visit.pop(0)
            url = self.normalize_url(url)

            if url in visited:
                continue

            visited.add(url)

            # Fetch page
            html = self.fetch_page(url)
            if not html:
                continue

            all_urls.append(url)
            self.stats['urls_crawled'] += 1
            pbar.update(1)

            # Extract new links
            new_links = self.extract_links(html, url, base_domain)

            for link in new_links:
                link = self.normalize_url(link)
                if link not in visited and link not in to_visit:
                    if len(all_urls) + len(to_visit) < self.config.max_pages:
                        to_visit.append(link)

            # Delay
            time.sleep(self.config.delay_between_requests)

        pbar.close()

        self.logger.info(f"\n{'='*80}")
        self.logger.info(f"Crawling complete! Found {len(all_urls)} unique URLs")
        self.logger.info(f"{'='*80}\n")

        return all_urls

    def create_pdfs(self, urls: List[str]):
        """
        Create PDFs from URLs in batches

        Args:
            urls: List of URLs to process
        """
        total_urls = len(urls)

        self.logger.info(f"Creating PDFs for {total_urls} URLs...")
        self.logger.info(f"Batch size: {self.config.batch_size}\n")

        # Progress bar
        pbar = tqdm(total=total_urls, desc="Creating PDFs", unit="pdf")

        # Process in batches
        for batch_num in range(0, total_urls, self.config.batch_size):
            batch_urls = urls[batch_num:batch_num + self.config.batch_size]

            for index_in_batch, url in enumerate(batch_urls, 1):
                global_index = batch_num + index_in_batch

                # Fetch content
                html = self.fetch_page(url)
                if not html:
                    self.stats['errors'] += 1
                    pbar.update(1)
                    continue

                # Extract text
                text = self.extract_text(html)
                if not text or len(text.strip()) < 10:
                    self.logger.warning(f"Insufficient content for {url}")
                    self.stats['errors'] += 1
                    pbar.update(1)
                    continue

                # Create PDF
                pdf_path = self.pdf_generator.create_pdf(
                    text, url, global_index, total_urls
                )

                if pdf_path:
                    self.stats['pdfs_created'] += 1
                else:
                    self.stats['errors'] += 1

                pbar.update(1)
                time.sleep(self.config.delay_between_requests)

            # Restart driver after each batch (memory cleanup)
            if batch_num + self.config.batch_size < total_urls:
                self.logger.info(f"\nRestarting Chrome driver (memory cleanup)...")
                self.driver.quit()
                time.sleep(3)
                self.driver = self.setup_driver()

        pbar.close()

    def save_urls(self, urls: List[str]) -> Path:
        """Save URLs to JSON file"""
        urls_file = self.config.output_folder / "scraped_urls.json"

        data = {
            'start_url': self.config.start_url,
            'timestamp': datetime.now().isoformat(),
            'total_urls': len(urls),
            'urls': urls
        }

        with open(urls_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        self.logger.info(f"URLs saved to: {urls_file}")
        return urls_file

    def print_statistics(self):
        """Print scraping statistics"""
        duration = (self.stats['end_time'] - self.stats['start_time']).total_seconds()

        print(f"\n{'='*80}")
        print("SCRAPING STATISTICS")
        print(f"{'='*80}")
        print(f"Start URL:      {self.config.start_url}")
        print(f"URLs Crawled:   {self.stats['urls_crawled']}")
        print(f"PDFs Created:   {self.stats['pdfs_created']}")
        print(f"Errors:         {self.stats['errors']}")
        print(f"Duration:       {duration:.1f} seconds ({duration/60:.1f} minutes)")
        print(f"Output Folder:  {self.config.output_folder}")
        print(f"{'='*80}\n")

    def run(self):
        """Run the complete scraping process"""
        self.stats['start_time'] = datetime.now()

        try:
            # Setup driver
            self.driver = self.setup_driver()

            # Crawl
            urls = self.crawl()

            if not urls:
                self.logger.error("No URLs found!")
                return

            # Save URLs
            self.save_urls(urls)

            # Ask user confirmation for PDF creation
            print(f"\n{len(urls)} URLs found and saved.")
            response = input("Create PDFs now? (yes/no): ").lower().strip()

            if response not in ['yes', 'y', 'ja', 'j']:
                self.logger.info("PDF creation cancelled by user.")
                return

            # Create PDFs
            self.create_pdfs(urls)

            # Statistics
            self.stats['end_time'] = datetime.now()
            self.print_statistics()

            print("✓ Scraping complete!")

        except KeyboardInterrupt:
            self.logger.info("\n\nInterrupted by user.")
            sys.exit(0)

        finally:
            if self.driver:
                self.driver.quit()
                self.logger.info("Chrome driver closed")


# ============================================================================
# USER INPUT
# ============================================================================

def get_user_input() -> Tuple[str, int]:
    """
    Get URL and max pages from user

    Returns:
        Tuple of (url, max_pages)
    """
    print("\n" + "="*80)
    print("WEB SCRAPER PRO - PROFESSIONAL PDF CONVERTER v2.0")
    print("="*80)

    # URL Input
    while True:
        start_url = input("\nWebsite URL (e.g., https://example.com): ").strip()

        if not start_url:
            print("❌ URL cannot be empty!")
            continue

        # Add https if missing
        if not start_url.startswith(('http://', 'https://')):
            start_url = 'https://' + start_url

        # Validate URL
        try:
            parsed = urlparse(start_url)
            if parsed.netloc:
                print(f"✓ URL accepted: {start_url}")
                break
            else:
                print("❌ Invalid URL format!")
        except Exception as e:
            print(f"❌ Invalid URL: {e}")

    # Max pages input
    while True:
        try:
            max_input = input("\nMax URLs to crawl (e.g., 20, 50, 100): ").strip()

            if not max_input:
                print("❌ Input cannot be empty!")
                continue

            max_pages = int(max_input)

            if max_pages <= 0:
                print("❌ Number must be greater than 0!")
                continue

            print(f"✓ Max pages: {max_pages}")
            break

        except ValueError:
            print("❌ Please enter a valid number!")

    print("\n" + "="*80)
    print(f"START URL: {start_url}")
    print(f"MAX PAGES: {max_pages}")
    print("="*80 + "\n")

    return start_url, max_pages


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main entry point"""
    # Get user input
    start_url, max_pages = get_user_input()

    # Create configuration
    config = ScraperConfig(
        start_url=start_url,
        max_pages=max_pages
    )

    # Setup logging
    logger = setup_logging(config.output_folder)

    # Create and run scraper
    scraper = WebScraper(config, logger)
    scraper.run()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
