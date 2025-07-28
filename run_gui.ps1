# Simple PowerShell launcher for ShamaOllama
Write-Host "Starting ShamaOllama..." -ForegroundColor Green

# Change to script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

# Activate virtual environment if it exists
if (Test-Path ".venv\Scripts\Activate.ps1") {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & ".venv\Scripts\Activate.ps1"
}

# Install dependencies if needed
if (Test-Path "requirements.txt") {
    python -c "import customtkinter, requests" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Installing dependencies..." -ForegroundColor Yellow
        pip install -r requirements.txt
    }
}

# Check Ollama connection
Write-Host "Checking Ollama connection..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:11434/api/version" -TimeoutSec 3 -ErrorAction Stop
    Write-Host "Ollama is running!" -ForegroundColor Green
} catch {
    Write-Host "Ollama not detected. Make sure it's running with: ollama serve" -ForegroundColor Yellow
}

# Launch the application
Write-Host "Launching ShamaOllama..." -ForegroundColor Green
python main.py

Write-Host "Application closed. Thanks for using ShamaOllama!" -ForegroundColor Green
