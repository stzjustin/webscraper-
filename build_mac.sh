#!/bin/bash
# Build script for macOS (Intel & Apple Silicon)
# Web Scraper Pro - Executable Builder

set -e  # Exit on error

echo "======================================"
echo "Web Scraper Pro - macOS Builder"
echo "======================================"
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ Python 3 not found! Please install Python 3.8 or higher."
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

# Install requirements
echo ""
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
    echo "  sudo cp -r dist/WebScraperPro /Applications/"
    echo ""

    # Get system info
    arch=$(uname -m)
    echo "Built for: macOS ($arch)"

    if [ "$arch" = "arm64" ]; then
        echo "  → Apple Silicon (M1/M2/M3)"
    else
        echo "  → Intel"
    fi

    echo ""
else
    echo ""
    echo "❌ Build failed! Check errors above."
    exit 1
fi
