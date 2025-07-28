@echo off
REM Silent launcher for ShamaOllama - no console window

REM Change to script directory
cd /d "%~dp0"

REM Activate virtual environment if it exists
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
)

REM Launch GUI without console window and exit this batch
start "" pythonw main.py
exit
