@echo off
REM Simple Desktop Shortcut Creator - Just Works!

echo Creating ShamaOllama desktop shortcut...

REM Get current directory
set SCRIPT_DIR=%~dp0

REM Create temporary VBS file
set temp_vbs=%TEMP%\shortcut.vbs

REM Write VBS script
echo Set WshShell = CreateObject("WScript.Shell") > %temp_vbs%
echo Set Shortcut = WshShell.CreateShortcut(WshShell.SpecialFolders("Desktop") ^& "\ShamaOllama.lnk") >> %temp_vbs%
echo Shortcut.TargetPath = "%SCRIPT_DIR%run_gui_silent.bat" >> %temp_vbs%
echo Shortcut.WorkingDirectory = "%SCRIPT_DIR%" >> %temp_vbs%
echo Shortcut.Description = "ShamaOllama - Modern Ollama GUI" >> %temp_vbs%
echo Shortcut.IconLocation = "%SCRIPT_DIR%assets\images\icons\ShamaOllama_Icon.ico,0" >> %temp_vbs%
echo Shortcut.Save >> %temp_vbs%

REM Run VBS script
cscript //NoLogo %temp_vbs%

REM Clean up
del %temp_vbs% 2>nul

echo.
echo [OK] Desktop shortcut created successfully!
echo [INFO] Location: %USERPROFILE%\Desktop\ShamaOllama.lnk
echo.
echo You can now double-click the ShamaOllama icon on your desktop!
echo.
pause
