@echo offREM Create shortcut using PowerShell
powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\ShamaOllama.lnk'); $Shortcut.TargetPath = '%SCRIPT_DIR%run_gui.bat'; $Shortcut.WorkingDirectory = '%SCRIPT_DIR%'; $Shortcut.Description = 'ShamaOllama - Modern Ollama GUI'; $Shortcut.IconLocation = '%SCRIPT_DIR%assets\images\icons\ShamaOllama_Icon.ico'; $Shortcut.Save()}"EM ShamaOllama Desktop Shortcut Creator for Windows
REM Creates a desktop shortcut for easy access

echo 🎸 Creating ShamaOllama Desktop Shortcut...
echo.

REM Get the current directory (where the script is located)
set SCRIPT_DIR=%~dp0

REM Create shortcut using PowerShell
powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\ShamaOllama.lnk'); $Shortcut.TargetPath = '%SCRIPT_DIR%run_gui.bat'; $Shortcut.WorkingDirectory = '%SCRIPT_DIR%'; $Shortcut.Description = 'ShamaOllama - Modern Ollama GUI'; $Shortcut.IconLocation = '%SCRIPT_DIR%assets\images\icons\ShamaOllama_Icon.ico'; $Shortcut.Save()}"

if %errorlevel% == 0 (
    echo ✅ Desktop shortcut created successfully!
    echo 📍 Location: %USERPROFILE%\Desktop\ShamaOllama.lnk
    echo.
    echo You can now double-click the ShamaOllama icon on your desktop to launch the app!
) else (
    echo ❌ Failed to create desktop shortcut.
    echo Try running this script as administrator.
)

echo.
pause
