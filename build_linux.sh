#!/bin/bash
# Build script for Linux
# Web Scraper Pro - Executable Builder

set -e  # Exit on error

echo "======================================"
echo "Web Scraper Pro - Linux Builder"
echo "======================================"
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ Python 3 not found! Please install Python 3.8 or higher."
    echo ""
    echo "Ubuntu/Debian: sudo apt-get install python3 python3-pip python3-venv"
    echo "Fedora/RHEL:   sudo dnf install python3 python3-pip"
    echo "Arch Linux:    sudo pacman -S python python-pip"
    exit 1
fi

echo "✓ Python found"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install system dependencies (for some packages)
echo ""
echo "Checking system dependencies..."
echo "Note: If build fails, you may need to install:"
echo "  Ubuntu/Debian: sudo apt-get install python3-dev libxml2-dev libxslt1-dev"
echo "  Fedora/RHEL:   sudo dnf install python3-devel libxml2-devel libxslt-devel"
echo "  Arch Linux:    sudo pacman -S python libxml2 libxslt"
echo ""

# Install requirements
echo "Installing dependencies..."
pip install -r requirements-pro.txt

# Install PyInstaller
echo ""
echo "Installing PyInstaller..."
pip install pyinstaller

# Clean previous builds
echo ""
echo "Cleaning previous builds..."
rm -rf build dist

# Build executable
echo ""
echo "Building executable..."
pyinstaller --clean web_scraper_pro.spec

if [ $? -eq 0 ]; then
    echo ""
    echo "======================================"
    echo "✓ BUILD SUCCESSFUL!"
    echo "======================================"
    echo ""
    echo "Your application is ready at:"
    echo "  ./dist/WebScraperPro"
    echo ""
    echo "To run the application:"
    echo "  ./dist/WebScraperPro"
    echo ""
    echo "To install system-wide (optional):"
    echo "  sudo cp dist/WebScraperPro /usr/local/bin/"
    echo "  sudo chmod +x /usr/local/bin/WebScraperPro"
    echo ""
    echo "Then you can run it from anywhere with: WebScraperPro"
    echo ""

    # Get system info
    echo "Built for: Linux ($(uname -m))"
    echo ""
else
    echo ""
    echo "❌ Build failed! Check errors above."
    exit 1
fi
