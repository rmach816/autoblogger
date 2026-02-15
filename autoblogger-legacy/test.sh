#!/bin/bash
# AutoBlogger Test Script for Linux/macOS
# This script helps test AutoBlogger on Unix systems

echo "AutoBlogger Test Script"
echo "====================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 not found!"
    echo "Please install Python 3.10+ from https://python.org"
    exit 1
fi

echo "Python found, checking version..."
python3 --version

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

# Run setup test
echo "Running setup test..."
python test_setup.py
if [ $? -ne 0 ]; then
    echo "ERROR: Setup test failed"
    exit 1
fi

# Generate test article
echo "Generating test article..."
python main.py --generate-now
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to generate article"
    exit 1
fi

# Check output
echo "Checking output files..."
if ls output/*.html 1> /dev/null 2>&1; then
    echo "SUCCESS: HTML files created in output/"
    ls -la output/*.html
else
    echo "WARNING: No HTML files found in output/"
fi

if ls output/*.md 1> /dev/null 2>&1; then
    echo "SUCCESS: Markdown files created in output/"
    ls -la output/*.md
else
    echo "WARNING: No Markdown files found in output/"
fi

echo ""
echo "====================="
echo "AutoBlogger Test Complete!"
echo ""
echo "Generated files are in the 'output' directory."
echo "You can open the HTML files in your browser to view the articles."
echo ""
echo "Next steps:"
echo "1. Get API keys (see docs/SETUP.md)"
echo "2. Create .env file with your keys"
echo "3. Change ai_provider from 'mock' to 'gemini' in config"
echo ""
