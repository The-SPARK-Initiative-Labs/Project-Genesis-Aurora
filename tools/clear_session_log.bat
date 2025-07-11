@echo off
echo Clearing short-term session memory...

REM Corrected path to point to the parent directory
set "LOG_FILE=..\raw_log.txt"

if exist %LOG_FILE% (
    del %LOG_FILE%
    echo Session log file has been deleted.
) else (
    echo Session log file not found. Nothing to do.
)

echo.
echo Short-term memory cleared.
pause
