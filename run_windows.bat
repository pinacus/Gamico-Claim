@echo off
setlocal

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Python virtual environment not found.
    echo Create it with: py -m venv .venv
    echo Then install dependencies and Chromium. See README.md.
    exit /b 1
)

".venv\Scripts\python.exe" -m src.epic_games.claim_game
exit /b %errorlevel%