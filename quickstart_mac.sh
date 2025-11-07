#!/bin/bash
# Quick Start Script for macOS
# Web Scraper Pro - One-Click Setup & Run

set -e  # Exit on error

echo "======================================"
echo "Web Scraper Pro - Quick Start (macOS)"
echo "======================================"
echo ""

# Check Python
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found!"
    echo ""
    echo "Please install Python 3.8 or higher:"
    echo "  1. Download from: https://www.python.org/downloads/"
    echo "  2. Or use Homebrew: brew install python3"
    echo ""
    exit 1
fi

python3 --version
echo "✓ Python found"
echo ""

# Check Chrome
echo "Checking Chrome installation..."
if [ ! -d "/Applications/Google Chrome.app" ]; then
    echo "⚠️  Warning: Chrome not found in Applications!"
    echo "   Please install Chrome from: https://www.google.com/chrome/"
    echo ""
    read -p "Continue anyway? (y/n): " choice
    if [ "$choice" != "y" ]; then
        exit 1
    fi
else
    echo "✓ Chrome found"
fi
echo ""

# Create virtual environment if needed
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip --quiet

# Install dependencies
echo ""
echo "Installing dependencies (this may take a few minutes)..."
pip install -r requirements-pro.txt --quiet

if [ $? -eq 0 ]; then
    echo "✓ All dependencies installed"
else
    echo "❌ Failed to install dependencies"
    echo ""
    echo "Trying to install ChromeDriver via Homebrew..."
    if command -v brew &> /dev/null; then
        brew install chromedriver
        echo "✓ ChromeDriver installed"
    else
        echo "⚠️  Homebrew not found. Please install manually:"
        echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    fi
fi

echo ""
echo "======================================"
echo "✓ Setup Complete!"
echo "======================================"
echo ""
echo "Starting Web Scraper Pro..."
echo ""

# Run the scraper
python web_scraper_pro.py
