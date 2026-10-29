@echo off
rem Build "WA Sender.exe" and add Start Menu + Desktop shortcuts.
cd /d "%~dp0"

python -m venv .venv || goto :error
.venv\Scripts\pip install -q pyinstaller || goto :error
.venv\Scripts\pyinstaller --noconfirm --windowed --onefile --name "WA Sender" --icon assets\icon.ico wa_sender_gui.py || goto :error

set "DEST=%LOCALAPPDATA%\Programs\WA Sender"
if not exist "%DEST%" mkdir "%DEST%"
copy /y "dist\WA Sender.exe" "%DEST%\" >nul

powershell -NoProfile -Command ^
  "$s=New-Object -ComObject WScript.Shell;" ^
  "foreach($d in @([Environment]::GetFolderPath('Programs'),[Environment]::GetFolderPath('Desktop'))){" ^
  "$l=$s.CreateShortcut((Join-Path $d 'WA Sender.lnk'));$l.TargetPath='%DEST%\WA Sender.exe';$l.Save()}"

echo Installed to %DEST% (Start Menu + Desktop shortcuts created)
exit /b 0
:error
echo Build failed.
exit /b 1
