# Silent launcher for ShamaOllama using PowerShell
# This script launches the application without showing any command window

# Get the directory where this script is located
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

# Check if virtual environment exists
$VenvPython = Join-Path $ScriptDir ".venv\Scripts\pythonw.exe"
if (Test-Path $VenvPython) {
    # Use the virtual environment Python (windowless)
    Start-Process -FilePath $VenvPython -ArgumentList "main.py" -WindowStyle Hidden -WorkingDirectory $ScriptDir
} else {
    # Fall back to system Python (windowless)
    Start-Process -FilePath "pythonw" -ArgumentList "main.py" -WindowStyle Hidden -WorkingDirectory $ScriptDir
}
