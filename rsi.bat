@echo off
setlocal
cd /d "%~dp0"

powershell -NoProfile -NoLogo -ExecutionPolicy Bypass -File "%~dp0rsi.ps1"
set RC=%ERRORLEVEL%

if not "%RC%"=="0" (
  echo.
  echo [ERROR] RSI Console exited with code %RC%.
  pause
)

endlocal
