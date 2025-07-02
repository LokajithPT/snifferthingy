@echo off
title DNS Watchtower Launcher
setlocal enabledelayedexpansion

:: Step 1: Set Python executable
where python >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Install Python and try again.
    pause
    exit /b
)

:: Step 2: Install dependencies
echo 📦 Installing Python dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

:: Step 3: Launch main.py in new terminal
echo 🚀 Launching Flask Server (main.py)...
start cmd /k "python main.py"

:: Step 4: Launch client.py in new terminal
echo 📡 Starting DNS Sniffer (client.py)...
start cmd /k "python client.py"

:: Step 5: Open dashboard in browser
echo 🌐 Opening dashboard in browser...
start http://localhost:5000

echo ✅ All systems GO!
pause

