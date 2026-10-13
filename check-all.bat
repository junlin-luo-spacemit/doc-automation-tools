@echo off
setlocal
cd /d "%~dp0"

echo.
echo  Scanning all bilingual repos...
echo.

for /d %%R in ("%~dp0..\*") do (
  if exist "%%~fR\.git" (
    if exist "%%~fR\zh" (
      python "%~dp0scripts\check_translations.py" "%%~fR" --summary
    ) else (
      if exist "%%~fR\en" python "%~dp0scripts\check_translations.py" "%%~fR" --summary
    )
  )
)

echo.
pause
endlocal
