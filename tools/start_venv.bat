@echo off
echo Starting Genesis Agent Virtual Environment...
echo.

REM Change to the parent directory first, then activate the venv
cd ..
cmd /k "venv\Scripts\activate.bat"
