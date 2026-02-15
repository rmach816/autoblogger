@echo off
REM AutoBlogger Test Script for Windows
REM This script helps test AutoBlogger on Windows systems

echo AutoBlogger Test Script
echo =====================

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
    echo Please install Python 3.10+ from https://python.org
    echo Or try: python3 --version
    pause
    exit /b 1
)

echo Python found, checking version...
python --version

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

REM Run setup test
echo Running setup test...
python test_setup.py
if %errorlevel% neq 0 (
    echo ERROR: Setup test failed
    pause
    exit /b 1
)

REM Generate test article
echo Generating test article...
python main.py --generate-now
if %errorlevel% neq 0 (
    echo ERROR: Failed to generate article
    pause
    exit /b 1
)

REM Check output
echo Checking output files...
if exist "output\*.html" (
    echo SUCCESS: HTML files created in output/
    dir output\*.html
) else (
    echo WARNING: No HTML files found in output/
)

if exist "output\*.md" (
    echo SUCCESS: Markdown files created in output/
    dir output\*.md
) else (
    echo WARNING: No Markdown files found in output/
)

echo.
echo =====================
echo AutoBlogger Test Complete!
echo.
echo Generated files are in the 'output' directory.
echo You can open the HTML files in your browser to view the articles.
echo.
echo Next steps:
echo 1. Get API keys (see docs/SETUP.md)
echo 2. Create .env file with your keys
echo 3. Change ai_provider from "mock" to "gemini" in config
echo.
pause
