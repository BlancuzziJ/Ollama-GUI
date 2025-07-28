' Silent launcher for ShamaOllama using VBScript
' This script launches the application without showing any command window

Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Get the directory where this script is located
strScriptPath = Replace(WScript.ScriptFullName, WScript.ScriptName, "")

' Change to the script directory
objShell.CurrentDirectory = strScriptPath

' Check if virtual environment exists and activate it
strVenvPath = strScriptPath & ".venv\Scripts\pythonw.exe"
If objFSO.FileExists(strVenvPath) Then
    ' Use the virtual environment Python (windowless)
    strCommand = """" & strVenvPath & """ main.py"
Else
    ' Fall back to system Python (windowless)
    strCommand = "pythonw main.py"
End If

' Run the command silently (0 = hidden window, False = don't wait)
objShell.Run strCommand, 0, False
