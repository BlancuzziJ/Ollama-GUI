@echo off
REM Force create desktop shortcut with proper icon
echo [REFRESH] Creating fresh ShamaOllama desktop shortcut...

REM Get current directory
set SCRIPT_DIR=%~dp0

REM Create shortcut with explicit icon index
powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\ShamaOllama.lnk'); $Shortcut.TargetPath = '%SCRIPT_DIR%run_gui.bat'; $Shortcut.WorkingDirectory = '%SCRIPT_DIR%'; $Shortcut.Description = 'ShamaOllama - Modern Ollama GUI'; $Shortcut.IconLocation = '%SCRIPT_DIR%assets\images\icons\ShamaOllama_Icon.ico,0'; $Shortcut.Save()}"

REM Force icon cache refresh
ie4uinit.exe -ClearIconCache

echo [OK] Fresh shortcut created with custom icon!
echo [INFO] Location: %USERPROFILE%\Desktop\ShamaOllama.lnk
echo [REFRESH] Icon cache refreshed

pause
