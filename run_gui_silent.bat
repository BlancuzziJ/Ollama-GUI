@echo off
REM Silent launcher for ShamaOllama - no console window

REM Change to script directory
cd /d "%~dp0"

REM Activate virtual environment if it exists and launch directly with pythonw
if exist ".venv\Scripts\pythonw.exe" (
    start "" ".venv\Scripts\pythonw.exe" main.py
) else (
    start "" pythonw main.py
)

REM Exit immediately
exit
