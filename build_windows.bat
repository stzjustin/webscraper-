@echo off
REM Build script for Windows
REM Web Scraper Pro - Executable Builder

echo ======================================
echo Web Scraper Pro - Windows Builder
echo ======================================
echo.

REM Check Python version
echo Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python not found! Please install Python 3.8 or higher.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

python --version
echo OK Python found
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo OK Virtual environment created
) else (
    echo OK Virtual environment already exists
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo.
echo Installing dependencies...
pip install -r requirements-pro.txt

REM Install PyInstaller
echo.
echo Installing PyInstaller...
pip install pyinstaller

REM Clean previous builds
echo.
echo Cleaning previous builds...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist

REM Build executable
echo.
echo Building executable...
pyinstaller --clean web_scraper_pro.spec

if errorlevel 0 (
    echo.
    echo ======================================
    echo OK BUILD SUCCESSFUL!
    echo ======================================
    echo.
    echo Your application is ready at:
    echo   .\dist\WebScraperPro.exe
    echo.
    echo To run the application:
    echo   Double-click WebScraperPro.exe in the dist folder
    echo   OR run from command line: .\dist\WebScraperPro.exe
    echo.
    echo You can copy the entire dist folder to any Windows computer
    echo and run the .exe file without installing Python!
    echo.
) else (
    echo.
    echo X Build failed! Check errors above.
    pause
    exit /b 1
)

pause
