
@echo off
echo 🚀 Starting AI Operating System...

REM Check Python installation
python --version
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.9 or higher.
    pause
    exit /b 1
)

REM Install dependencies if needed
if not exist ".deps_installed" (
    echo 📦 Installing dependencies...
    pip install -r requirements.txt
    echo. > .deps_installed
)

REM Set environment variables
set PYTHONPATH=%PYTHONPATH%;%CD%
set FLASK_ENV=production
set PORT=8000
set HOST=0.0.0.0

REM Start the application
echo 🎯 Starting on %HOST%:%PORT%
python main.py

pause
