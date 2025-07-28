@echo off
title ShamaOllama

echo.
echo [*] Starting ShamaOllama...
echo Paying homage to "Shama Lama Ding Dong" from Animal House (1978)
echo.

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Check if Ollama is installed and running
echo [*] Checking Ollama status...
curl -s http://localhost:11434/api/version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [!] WARNING: Ollama is not running or not installed!
    echo.
    echo [i] To fix this:
    echo   1. Download Ollama from: https://ollama.ai
    echo   2. Install and start Ollama
    echo   3. Run: ollama pull llama3.2:1b  (for a small model)
    echo   4. Or: ollama pull llama3.2:3b   (for better quality)
    echo.
    echo [*] ShamaOllama will start, but you'll need Ollama running to chat.
    echo.
    pause
) else (
    echo [+] Ollama is running!
)

echo.
echo [*] Launching ShamaOllama GUI...
echo.

REM Run the GUI application
python main.py

echo.
echo [*] Ollama GUI closed.
pause
