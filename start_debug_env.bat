@echo off
REM --- START DEBUG ENV FOR SMARTWORKS AFRICA ---

echo Initializing SmartWorks Africa Environment...
cd /d %~dp0

REM -- Step 1: Activate virtual environment if it exists --
IF EXIST venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) ELSE (
    echo Virtual environment not found. Creating one...
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install --upgrade pip
    pip install -r requirements.txt
)

REM -- Step 2: Check for PM2 installation --
where pm2 >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo Installing PM2 globally...
    npm install -g pm2
) ELSE (
    echo PM2 already installed.
)

REM -- Step 3: Start the main system using PM2 --
echo Launching SmartWorks Africa main engine using PM2...
pm2 start main.py --interpreter=python --name=smartworks

REM -- Step 4: Start test monitoring (optional) --
echo To monitor logs, use: pm2 logs smartworks
echo To stop, use: pm2 stop smartworks

pause
exit
