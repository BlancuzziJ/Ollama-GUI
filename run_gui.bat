@echo off
echo Starting ShamaOllama...
echo Paying homage to "Shama Lama Ding Dong" from Animal House (1978)
echo.

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Check if Ollama is running
echo Checking if Ollama is running...
timeout /t 2 >nul

REM Run the GUI application
python main.py

echo.
echo Ollama GUI closed.
pause
