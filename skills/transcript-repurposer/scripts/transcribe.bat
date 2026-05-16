@echo off
REM Watts Transcript Tool — Windows wrapper for transcribe_local.py
REM
REM Setup (one time):
REM   1. Install Python from python.org (3.10 or newer)
REM   2. Open Command Prompt and run:  pip install yt-dlp httpx
REM   3. Install ffmpeg: https://www.gyan.dev/ffmpeg/builds/ — add to PATH
REM   4. Make sure your Deepgram key is at:
REM      C:\Users\<you>\Documents\Claude\Skills\deepgram-key.txt
REM   5. Save this transcribe.bat anywhere convenient (Desktop, or in PATH)
REM
REM Usage:
REM   transcribe https://www.youtube.com/watch?v=...
REM   transcribe "https://www.instagram.com/reel/Cxxxx/"
REM   transcribe C:\path\to\audio.mp3

setlocal
set SCRIPT_DIR=%~dp0
set PY_SCRIPT=%SCRIPT_DIR%transcribe_local.py

if "%~1"=="" (
    echo Usage: transcribe ^<url or audio file^>
    echo.
    echo Examples:
    echo   transcribe https://www.youtube.com/watch?v=abc123
    echo   transcribe "https://www.instagram.com/reel/Cxxx/"
    echo   transcribe C:\Videos\interview.mp3
    exit /b 1
)

REM Detect if input is a URL or a file path
set INPUT=%~1
echo %INPUT% | findstr /R "^https*://" >nul
if %ERRORLEVEL% == 0 (
    python "%PY_SCRIPT%" --url "%INPUT%"
) else (
    python "%PY_SCRIPT%" --file "%INPUT%"
)

endlocal
