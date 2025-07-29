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

if "%choice%"=="1" goto regular
if "%choice%"=="2" goto silent_batch
if "%choice%"=="3" goto silent_ps
if "%choice%"=="4" goto silent_vbs
goto silent_batch

:regular
echo Creating regular desktop shortcut...
set "temp_vbs=%TEMP%\shortcut_%RANDOM%.vbs"
echo Set WshShell = CreateObject("WScript.Shell") > "%temp_vbs%"
echo Set Shortcut = WshShell.CreateShortcut(WshShell.SpecialFolders("Desktop") ^& "\ShamaOllama.lnk") >> "%temp_vbs%"
echo Shortcut.TargetPath = "%SCRIPT_DIR%run_gui.bat" >> "%temp_vbs%"
echo Shortcut.WorkingDirectory = "%SCRIPT_DIR%" >> "%temp_vbs%"
echo Shortcut.Description = "ShamaOllama - Modern Ollama GUI" >> "%temp_vbs%"
echo Shortcut.IconLocation = "%SCRIPT_DIR%assets\images\icons\ShamaOllama_Icon.ico,0" >> "%temp_vbs%"
echo Shortcut.Save >> "%temp_vbs%"
cscript //NoLogo "%temp_vbs%"
del "%temp_vbs%" 2>nul
echo [OK] Regular desktop shortcut created successfully!
echo [INFO] Shortcut: ShamaOllama.lnk
goto done

:silent_batch
echo Creating silent batch shortcut (RECOMMENDED)...
set "temp_vbs=%TEMP%\shortcut_%RANDOM%.vbs"
echo Set WshShell = CreateObject("WScript.Shell") > "%temp_vbs%"
echo Set Shortcut = WshShell.CreateShortcut(WshShell.SpecialFolders("Desktop") ^& "\ShamaOllama.lnk") >> "%temp_vbs%"
echo Shortcut.TargetPath = "%SCRIPT_DIR%run_gui_silent.bat" >> "%temp_vbs%"
echo Shortcut.WorkingDirectory = "%SCRIPT_DIR%" >> "%temp_vbs%"
echo Shortcut.Description = "ShamaOllama - Silent Launch (Best Compatibility)" >> "%temp_vbs%"
echo Shortcut.IconLocation = "%SCRIPT_DIR%assets\images\icons\ShamaOllama_Icon.ico,0" >> "%temp_vbs%"
echo Shortcut.Save >> "%temp_vbs%"
cscript //NoLogo "%temp_vbs%"
del "%temp_vbs%" 2>nul
echo [OK] Silent batch desktop shortcut created successfully!
echo [INFO] Shortcut: ShamaOllama.lnk
echo [INFO] This shortcut uses the silent batch launcher for maximum compatibility.
goto done

:silent_ps
echo Creating silent PowerShell shortcut...
set "temp_vbs=%TEMP%\shortcut_%RANDOM%.vbs"
echo Set WshShell = CreateObject("WScript.Shell") > "%temp_vbs%"
echo Set Shortcut = WshShell.CreateShortcut(WshShell.SpecialFolders("Desktop") ^& "\ShamaOllama (PowerShell).lnk") >> "%temp_vbs%"
echo Shortcut.TargetPath = "%SCRIPT_DIR%launch_silent.ps1" >> "%temp_vbs%"
echo Shortcut.WorkingDirectory = "%SCRIPT_DIR%" >> "%temp_vbs%"
echo Shortcut.Description = "ShamaOllama - Silent Launch (PowerShell)" >> "%temp_vbs%"
echo Shortcut.IconLocation = "%SCRIPT_DIR%assets\images\icons\ShamaOllama_Icon.ico,0" >> "%temp_vbs%"
echo Shortcut.Save >> "%temp_vbs%"
cscript //NoLogo "%temp_vbs%"
del "%temp_vbs%" 2>nul
echo [OK] Silent PowerShell desktop shortcut created successfully!
echo [INFO] Shortcut: ShamaOllama (PowerShell).lnk
goto done

:silent_vbs
echo Creating silent VBScript shortcut...
set "temp_vbs=%TEMP%\shortcut_%RANDOM%.vbs"
echo Set WshShell = CreateObject("WScript.Shell") > "%temp_vbs%"
echo Set Shortcut = WshShell.CreateShortcut(WshShell.SpecialFolders("Desktop") ^& "\ShamaOllama (VBScript).lnk") >> "%temp_vbs%"
echo Shortcut.TargetPath = "%SCRIPT_DIR%launch_silent.vbs" >> "%temp_vbs%"
echo Shortcut.WorkingDirectory = "%SCRIPT_DIR%" >> "%temp_vbs%"
echo Shortcut.Description = "ShamaOllama - Silent Launch (VBScript)" >> "%temp_vbs%"
echo Shortcut.IconLocation = "%SCRIPT_DIR%assets\images\icons\ShamaOllama_Icon.ico,0" >> "%temp_vbs%"
echo Shortcut.Save >> "%temp_vbs%"
cscript //NoLogo "%temp_vbs%"
del "%temp_vbs%" 2>nul
echo [OK] Silent VBScript desktop shortcut created successfully!
echo [INFO] Shortcut: ShamaOllama (VBScript).lnk
goto done

:done
echo.
echo [INFO] Location: %USERPROFILE%\Desktop\
echo.
echo You can now launch ShamaOllama from your desktop!
echo [OK] Desktop shortcut created successfully!
echo.
echo You can now double-click the ShamaOllama icon on your desktop to launch the app!
echo.
pause
