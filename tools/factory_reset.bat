@echo off
echo WARNING: This will perform a full factory reset, deleting ALL of Aurora's memories.
echo.

REM Corrected paths to point to the parent directory
set "LOG_FILE=..\raw_log.txt"
set "DB_FOLDER=..\agent_db"

if exist %LOG_FILE% (
    del %LOG_FILE%
    echo Session log file has been deleted.
) else (
    echo Session log file not found.
)

if exist %DB_FOLDER% (
    rmdir /s /q %DB_FOLDER%
    echo Long-term memory database has been deleted.
) else (
    echo Long-term memory database not found.
)

echo.
echo Factory reset complete. Aurora is now a blank slate.
pause
