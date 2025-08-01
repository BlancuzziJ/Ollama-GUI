@echo off
REM ShamaOllama Setup Script for Windows
REM Copyright (c) 2025 John Blancuzzi
REM Licensed under the MIT License
REM Paying homage to "Shama Lama Ding Dong" from Animal House (1978)

title ShamaOllama Setup

echo.
echo ========================================
echo       ShamaOllama Setup Script
echo ========================================
echo Author: John Blancuzzi
echo License: MIT License
echo Homage: "Shama Lama Ding Dong" - Animal House (1978)
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [X] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    echo.
    pause
    exit /b 1
)

echo [OK] Python found
python --version

REM Create virtual environment
echo.
echo [SETUP] Creating virtual environment...
if exist .venv (
    echo Virtual environment already exists, skipping creation.
) else (
    python -m venv .venv
    if errorlevel 1 (
        echo [X] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
)

REM Activate virtual environment
echo.
echo [SETUP] Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo [X] Failed to activate virtual environment
    pause
    exit /b 1
)

REM Install dependencies
echo.
echo [SETUP] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [X] Failed to install dependencies
    pause
    exit /b 1
)

echo [OK] Dependencies installed successfully

REM Check if Ollama is available
echo.
echo [CHECK] Checking Ollama connection...
curl -s http://localhost:11434/api/version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [WARNING] IMPORTANT: Ollama is not running or not installed!
    echo.
    echo [INFO] NEXT STEPS - Install Ollama:
    echo   1. Visit: https://ollama.ai
    echo   2. Download and install Ollama for Windows
    echo   3. Restart your computer (or open new terminal)
    echo   4. Run: ollama pull llama3.2:1b  (small, fast model)
    echo   5. Or run: ollama pull llama3.2:3b  (better quality)
    echo.
    echo [INFO] Ollama is required for ShamaOllama to work!
    echo    ShamaOllama will install but won't function without Ollama.
    echo.
) else (
    echo [OK] Ollama is running and accessible!
)

echo.
echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo [SHORTCUT] Would you like to create a desktop shortcut? (y/n)
set /p create_shortcut="Create desktop shortcut? (y/n): "

if /i "%create_shortcut%"=="y" (
    echo.
    echo [CREATE] Creating desktop shortcut...
    call create_desktop_shortcut_simple.bat
    echo.
)

echo To start ShamaOllama:
echo   1. Double-click run_gui.bat
echo   2. Use the desktop shortcut (if created)
echo   3. Or run: python main.py
echo.
echo For help and documentation:
echo   - README.md - Complete guide
echo   - INSTALL.md - Installation details
echo   - QUICKSTART.md - Fast setup guide
echo   - GitHub: https://github.com/BlancuzziJ/Ollama-GUI
echo.
echo [SUPPORT] Support ShamaOllama development:
echo   - GitHub Sponsors: https://github.com/sponsors/BlancuzziJ
echo   - Star the repo and share with others!
echo.

pause
