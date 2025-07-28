@echo off
REM ShamaOllama Desktop Shortcut Creator for Windows
REM Creates desktop shortcuts for easy access

echo [CREATE] Creating ShamaOllama Desktop Shortcuts...
echo.

REM Get the current directory (where the script is located)
set SCRIPT_DIR=%~dp0

echo Choose shortcut type:
echo 1. Regular launch (shows startup messages, then closes command window)
echo 2. Silent launch - Batch file (RECOMMENDED - best compatibility)
echo 3. Silent launch - PowerShell (most modern, may require execution policy)
echo 4. Silent launch - VBScript (maximum compatibility, may trigger security warnings)
echo.
set /p choice="Enter your choice (1-4, or press Enter for recommended option 2): "

if "%choice%"=="" set choice=2

if "%choice%"=="1" (
    echo Creating regular desktop shortcut...
    echo Set WshShell = CreateObject("WScript.Shell") > temp_shortcut.vbs
    echo Set Shortcut = WshShell.CreateShortcut(WshShell.SpecialFolders("Desktop") ^& "\ShamaOllama.lnk") >> temp_shortcut.vbs
    echo Shortcut.TargetPath = "%SCRIPT_DIR%run_gui.bat" >> temp_shortcut.vbs
    echo Shortcut.WorkingDirectory = "%SCRIPT_DIR%" >> temp_shortcut.vbs
    echo Shortcut.Description = "ShamaOllama - Modern Ollama GUI" >> temp_shortcut.vbs
    echo Shortcut.IconLocation = "%SCRIPT_DIR%assets\images\icons\ShamaOllama_Icon.ico,0" >> temp_shortcut.vbs
    echo Shortcut.Save >> temp_shortcut.vbs
    cscript //NoLogo temp_shortcut.vbs
    del temp_shortcut.vbs
    echo [OK] Regular desktop shortcut created successfully!
    echo [INFO] Shortcut: ShamaOllama.lnk
) else if "%choice%"=="2" (
    echo Creating silent batch shortcut (RECOMMENDED)...
    echo Set WshShell = CreateObject("WScript.Shell") > temp_shortcut.vbs
    echo Set Shortcut = WshShell.CreateShortcut(WshShell.SpecialFolders("Desktop") ^& "\ShamaOllama.lnk") >> temp_shortcut.vbs
    echo Shortcut.TargetPath = "%SCRIPT_DIR%run_gui_silent.bat" >> temp_shortcut.vbs
    echo Shortcut.WorkingDirectory = "%SCRIPT_DIR%" >> temp_shortcut.vbs
    echo Shortcut.Description = "ShamaOllama - Silent Launch (Best Compatibility)" >> temp_shortcut.vbs
    echo Shortcut.IconLocation = "%SCRIPT_DIR%assets\images\icons\ShamaOllama_Icon.ico,0" >> temp_shortcut.vbs
    echo Shortcut.Save >> temp_shortcut.vbs
    cscript //NoLogo temp_shortcut.vbs
    del temp_shortcut.vbs
    echo [OK] Silent batch desktop shortcut created successfully!
    echo [INFO] Shortcut: ShamaOllama.lnk
    echo [INFO] This shortcut uses the silent batch launcher for maximum compatibility.
) else if "%choice%"=="3" (
    echo Creating silent PowerShell shortcut...
    echo Set WshShell = CreateObject("WScript.Shell") > temp_shortcut.vbs
    echo Set Shortcut = WshShell.CreateShortcut(WshShell.SpecialFolders("Desktop") ^& "\ShamaOllama (PowerShell).lnk") >> temp_shortcut.vbs
    echo Shortcut.TargetPath = "%SCRIPT_DIR%launch_silent.ps1" >> temp_shortcut.vbs
    echo Shortcut.WorkingDirectory = "%SCRIPT_DIR%" >> temp_shortcut.vbs
    echo Shortcut.Description = "ShamaOllama - Silent Launch (PowerShell)" >> temp_shortcut.vbs
    echo Shortcut.IconLocation = "%SCRIPT_DIR%assets\images\icons\ShamaOllama_Icon.ico,0" >> temp_shortcut.vbs
    echo Shortcut.Save >> temp_shortcut.vbs
    cscript //NoLogo temp_shortcut.vbs
    del temp_shortcut.vbs
    echo [OK] Silent PowerShell desktop shortcut created successfully!
    echo [INFO] Shortcut: ShamaOllama (PowerShell).lnk
) else if "%choice%"=="4" (
    echo Creating silent VBScript shortcut...
    echo Set WshShell = CreateObject("WScript.Shell") > temp_shortcut.vbs
    echo Set Shortcut = WshShell.CreateShortcut(WshShell.SpecialFolders("Desktop") ^& "\ShamaOllama (VBScript).lnk") >> temp_shortcut.vbs
    echo Shortcut.TargetPath = "%SCRIPT_DIR%launch_silent.vbs" >> temp_shortcut.vbs
    echo Shortcut.WorkingDirectory = "%SCRIPT_DIR%" >> temp_shortcut.vbs
    echo Shortcut.Description = "ShamaOllama - Silent Launch (VBScript)" >> temp_shortcut.vbs
    echo Shortcut.IconLocation = "%SCRIPT_DIR%assets\images\icons\ShamaOllama_Icon.ico,0" >> temp_shortcut.vbs
    echo Shortcut.Save >> temp_shortcut.vbs
    cscript //NoLogo temp_shortcut.vbs
    del temp_shortcut.vbs
    echo [OK] Silent VBScript desktop shortcut created successfully!
    echo [INFO] Shortcut: ShamaOllama (VBScript).lnk
) else (
    echo Invalid choice. Creating recommended silent batch shortcut...
    echo Set WshShell = CreateObject("WScript.Shell") > temp_shortcut.vbs
    echo Set Shortcut = WshShell.CreateShortcut(WshShell.SpecialFolders("Desktop") ^& "\ShamaOllama.lnk") >> temp_shortcut.vbs
    echo Shortcut.TargetPath = "%SCRIPT_DIR%run_gui_silent.bat" >> temp_shortcut.vbs
    echo Shortcut.WorkingDirectory = "%SCRIPT_DIR%" >> temp_shortcut.vbs
    echo Shortcut.Description = "ShamaOllama - Silent Launch (Best Compatibility)" >> temp_shortcut.vbs
    echo Shortcut.IconLocation = "%SCRIPT_DIR%assets\images\icons\ShamaOllama_Icon.ico,0" >> temp_shortcut.vbs
    echo Shortcut.Save >> temp_shortcut.vbs
    cscript //NoLogo temp_shortcut.vbs
    del temp_shortcut.vbs
    echo [OK] Silent batch desktop shortcut created successfully!
    echo [INFO] Shortcut: ShamaOllama.lnk
)

echo.
echo [INFO] Location: %USERPROFILE%\Desktop\
echo.
echo You can now launch ShamaOllama from your desktop!

if %errorlevel% == 0 (
    echo [OK] Desktop shortcut created successfully!
    echo [INFO] Location: %USERPROFILE%\Desktop\ShamaOllama.lnk
    echo.
    echo You can now double-click the ShamaOllama icon on your desktop to launch the app!
) else (
    echo [X] Failed to create desktop shortcut.
    echo Try running this script as administrator.
)

echo.
pause
