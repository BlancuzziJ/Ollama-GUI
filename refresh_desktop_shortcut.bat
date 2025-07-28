@echo off
REM Force create desktop shortcut with proper icon
echo [REFRESH] Creating fresh ShamaOllama desktop shortcut...

REM Get current directory
set SCRIPT_DIR=%~dp0

REM Create shortcut using VBScript for better icon support
echo Set WshShell = CreateObject("WScript.Shell") > temp_refresh_shortcut.vbs
echo Set Shortcut = WshShell.CreateShortcut(WshShell.SpecialFolders("Desktop") ^& "\ShamaOllama.lnk") >> temp_refresh_shortcut.vbs
echo Shortcut.TargetPath = "%SCRIPT_DIR%run_gui_silent.bat" >> temp_refresh_shortcut.vbs
echo Shortcut.WorkingDirectory = "%SCRIPT_DIR%" >> temp_refresh_shortcut.vbs
echo Shortcut.Description = "ShamaOllama - Modern Ollama GUI" >> temp_refresh_shortcut.vbs
echo Shortcut.IconLocation = "%SCRIPT_DIR%assets\images\icons\ShamaOllama_Icon.ico,0" >> temp_refresh_shortcut.vbs
echo Shortcut.Save >> temp_refresh_shortcut.vbs
cscript //NoLogo temp_refresh_shortcut.vbs
del temp_refresh_shortcut.vbs

REM Force icon cache refresh
ie4uinit.exe -ClearIconCache

echo [OK] Fresh shortcut created with custom icon!
echo [INFO] Location: %USERPROFILE%\Desktop\ShamaOllama.lnk
echo [REFRESH] Icon cache refreshed

pause
