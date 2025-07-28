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
    call :create_shortcut "ShamaOllama.lnk" "run_gui.bat" "ShamaOllama - Modern Ollama GUI"
    echo [OK] Regular desktop shortcut created successfully!
    echo [INFO] Shortcut: ShamaOllama.lnk
    goto :done
)

if "%choice%"=="2" (
    echo Creating silent batch shortcut (RECOMMENDED)...
    call :create_shortcut "ShamaOllama.lnk" "run_gui_silent.bat" "ShamaOllama - Silent Launch (Best Compatibility)"
    echo [OK] Silent batch desktop shortcut created successfully!
    echo [INFO] Shortcut: ShamaOllama.lnk
    echo [INFO] This shortcut uses the silent batch launcher for maximum compatibility.
    goto :done
)

if "%choice%"=="3" (
    echo Creating silent PowerShell shortcut...
    call :create_shortcut "ShamaOllama (PowerShell).lnk" "launch_silent.ps1" "ShamaOllama - Silent Launch (PowerShell)"
    echo [OK] Silent PowerShell desktop shortcut created successfully!
    echo [INFO] Shortcut: ShamaOllama (PowerShell).lnk
    goto :done
)

if "%choice%"=="4" (
    echo Creating silent VBScript shortcut...
    call :create_shortcut "ShamaOllama (VBScript).lnk" "launch_silent.vbs" "ShamaOllama - Silent Launch (VBScript)"
    echo [OK] Silent VBScript desktop shortcut created successfully!
    echo [INFO] Shortcut: ShamaOllama (VBScript).lnk
    goto :done
)

REM Default fallback for invalid choice
echo Invalid choice. Creating recommended silent batch shortcut...
call :create_shortcut "ShamaOllama.lnk" "run_gui_silent.bat" "ShamaOllama - Silent Launch (Best Compatibility)"
echo [OK] Silent batch desktop shortcut created successfully!
echo [INFO] Shortcut: ShamaOllama.lnk

:done

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
exit /b 0

:create_shortcut
REM Create shortcut using VBScript COM object
REM %1 = shortcut name, %2 = target file, %3 = description
set "temp_vbs=%TEMP%\create_shortcut_%RANDOM%.vbs"
(
    echo Set WshShell = CreateObject^("WScript.Shell"^)
    echo Set Shortcut = WshShell.CreateShortcut^(WshShell.SpecialFolders^("Desktop"^) ^& "\%~1"^)
    echo Shortcut.TargetPath = "%SCRIPT_DIR%%~2"
    echo Shortcut.WorkingDirectory = "%SCRIPT_DIR%"
    echo Shortcut.Description = "%~3"
    echo Shortcut.IconLocation = "%SCRIPT_DIR%assets\images\icons\ShamaOllama_Icon.ico,0"
    echo Shortcut.Save
) > "%temp_vbs%"

cscript //NoLogo "%temp_vbs%"
del "%temp_vbs%" 2>nul
exit /b 0
