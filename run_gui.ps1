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
Write-Host "🔍 Checking Ollama status..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:11434/api/version" -TimeoutSec 3 -ErrorAction Stop
    Write-Host "✅ Ollama is running!" -ForegroundColor Green
}
catch {
    Write-Host ""
    Write-Host "⚠️  WARNING: Ollama is not running or not installed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "📋 To fix this:" -ForegroundColor Yellow
    Write-Host "  1. Download from: https://ollama.ai" -ForegroundColor White
    Write-Host "  2. Install and start Ollama" -ForegroundColor White
    Write-Host "  3. Run: ollama pull llama3.2:1b  (small model)" -ForegroundColor White
    Write-Host "  4. Or: ollama pull llama3.2:3b   (better quality)" -ForegroundColor White
    Write-Host ""
    Write-Host "🎯 ShamaOllama will start, but you'll need Ollama running to chat." -ForegroundColor Yellow
    Write-Host ""
}

# Launch the application
Write-Host "Launching ShamaOllama..." -ForegroundColor Green
python main.py

Write-Host "Application closed. Thanks for using ShamaOllama!" -ForegroundColor Green
