@echo off
:: ============================================================================
:: Project Genesis: Intelligent GitHub Sync Script (sync_project_v2.bat)
::
:: This advanced script automates the entire sync process. It intelligently
:: handles merge conflicts and only prompts for a commit message when new
:: local changes have actually been made.
:: ============================================================================

:: --- Configuration ---
set "PROJECT_DIR=C:\GenesisAgent"

:: --- Script Execution ---
echo.
echo --- [ The S.P.A.R.K. Initiative: Project Genesis Sync ] ---
echo.

:: Change to the project directory
cd /d "%PROJECT_DIR%"

:: 1. Clean and Sync with Remote Repository
echo [Step 1/3] Checking for conflicts and downloading updates...
if exist .git\MERGE_HEAD (
    echo  - Conflict detected. Aborting previous merge to ensure a clean state.
    git merge --abort
)
git pull origin master --no-edit --quiet
echo  - Repository is now in sync with GitHub.
echo.

:: 2. Check for Local Changes
echo [Step 2/3] Checking for new local file changes...
git add .
git diff-index --quiet HEAD --
if %errorlevel% == 0 (
    echo  - No new local changes to commit.
    goto :end
)

echo  - New local changes detected. Proceeding with commit.
echo.

:: 3. Commit and Push Local Changes
echo [Step 3/3] Please describe your new changes.
set /p commitMessage="Commit Message: "
echo.

echo  - Committing and uploading your work...
git commit -m "%commitMessage%"
git push origin master
echo.

:end
echo --- [ Sync Complete ] ---
echo Your project is now safely backed up on GitHub.
echo.
pause
