@echo off
REM Force create desktop shortcut with proper icon
echo 🔄 Creating fresh ShamaOllama desktop shortcut...

REM Get current directory
set SCRIPT_DIR=%~dp0

REM Create shortcut with explicit icon index
powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\ShamaOllama.lnk'); $Shortcut.TargetPath = '%SCRIPT_DIR%run_gui.bat'; $Shortcut.WorkingDirectory = '%SCRIPT_DIR%'; $Shortcut.Description = 'ShamaOllama - Modern Ollama GUI'; $Shortcut.IconLocation = '%SCRIPT_DIR%assets\images\icons\ShamaOllama_Icon.ico,0'; $Shortcut.Save()}"

REM Force icon cache refresh
ie4uinit.exe -ClearIconCache

echo ✅ Fresh shortcut created with custom icon!
echo 📍 Location: %USERPROFILE%\Desktop\ShamaOllama.lnk
echo 🔄 Icon cache refreshed

pause
