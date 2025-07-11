@echo off
echo Starting Aurora...
echo Make sure LM Studio is running with the server started.
echo.

REM Change to the parent directory first, then start the agent
cd ..
cmd /k "venv\Scripts\activate.bat && python main_agent.py"
