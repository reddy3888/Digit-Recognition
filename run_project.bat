@echo off
title Handwritten Digit Recognition Launcher
echo ===================================================
echo   Handwritten Digit Recognition - Setup & Run
echo ===================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in your PATH.
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/3] Checking and installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo Error: Failed to install dependencies.
    pause
    exit /b 1
)
echo Dependencies installed.
echo.

REM Check if model exists
if not exist "mnist_model.h5" (
    echo [2/3] Model not found. Training model now...
    echo This may take a few minutes...
    python train_model.py
    if %errorlevel% neq 0 (
        echo.
        echo Error: Model training failed.
        pause
        exit /b 1
    )
    echo Model training complete.
) else (
    echo [2/3] Model found. Skipping training.
)
echo.

echo [3/3] Starting Web Application...
echo.
echo ===================================================
echo   Server running!
echo   Open your browser to: http://127.0.0.1:5000
echo   Press Ctrl+C to stop the server.
echo ===================================================
echo.

python app.py
pause
