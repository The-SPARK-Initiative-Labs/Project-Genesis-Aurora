@echo off
:: ===================================================================
:: Project Genesis: Final Sync Script (sync.bat)
::
:: This script automates the standard workflow for backing up your
:: project to GitHub. Run it after you have saved changes to your files.
:: ===================================================================

:: --- Configuration ---
set "PROJECT_DIR=C:\GenesisAgent"

:: --- Script Execution ---
echo.
echo --- [ S.P.A.R.K. Initiative: Project Genesis Sync ] ---
echo.

:: Change to the project directory
cd /d "%PROJECT_DIR%"

:: Step 1: Stage all new and modified files
echo [1/3] Staging all changes...
git add .
echo.

:: Step 2: Prompt for a commit message
echo [2/3] Please enter a short description of the work you did.
set /p commitMessage="Commit Message: "
echo.

:: Step 3: Commit the changes and push them to GitHub
echo [3/3] Committing and uploading to GitHub...
git commit -m "%commitMessage%"
git push
echo.

echo --- [ Sync Complete ] ---
echo.
pause
