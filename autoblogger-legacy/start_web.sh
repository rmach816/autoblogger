#!/bin/bash
# AutoBlogger Web Interface Starter for Linux/macOS

echo "AutoBlogger Web Interface"
echo "========================"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 not found!"
    echo "Please install Python 3.10+ from https://python.org"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create virtual environment"
        exit 1
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

# Start web interface
echo "Starting web interface..."
python start_web.py
