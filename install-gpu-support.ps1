# Installing optional GPU detection dependencies...
# This will enable enhanced hardware analysis for local AI recommendations.

Write-Host "Installing GPU detection dependencies..." -ForegroundColor Yellow

try {
    pip install -r requirements-gpu.txt
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✅ GPU detection dependencies installed successfully!" -ForegroundColor Green
        Write-Host "Enhanced hardware information is now available in ShamaOllama." -ForegroundColor Green
    }
    else {
        Write-Host "`n❌ Installation failed. Please check your Python and pip installation." -ForegroundColor Red
        Write-Host "You can still use ShamaOllama with basic GPU detection." -ForegroundColor Yellow
    }
}
catch {
    Write-Host "`n❌ Installation failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "You can still use ShamaOllama with basic GPU detection." -ForegroundColor Yellow
}

Write-Host "`nPress any key to continue..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
