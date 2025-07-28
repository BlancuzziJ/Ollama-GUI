@echo off
echo Installing optional GPU detection dependencies...
echo This will enable enhanced hardware analysis for local AI recommendations.
echo.

pip install -r requirements-gpu.txt

if %ERRORLEVEL% EQU 0 (
    echo.
    echo [OK] GPU detection dependencies installed successfully!
    echo Enhanced hardware information is now available in ShamaOllama.
) else (
    echo.
    echo [X] Installation failed. Please check your Python and pip installation.
    echo You can still use ShamaOllama with basic GPU detection.
)

echo.
echo Press any key to continue...
pause >nul
