#!/usr/bin/env python3
"""
AutoBlogger Web Interface Starter

Simple script to start the web interface on port 3500.
"""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

def check_requirements():
    """Check if all requirements are installed."""
    try:
        import flask
        print("Flask installed")
    except ImportError:
        print("Flask not installed. Run: pip install flask")
        return False
    
    try:
        from src.models import AppConfig
        print("AutoBlogger modules available")
    except ImportError as e:
        print(f"AutoBlogger modules not found: {e}")
        return False
    
    return True

def check_config():
    """Check if configuration exists."""
    config_path = Path("config/settings.json")
    if not config_path.exists():
        example_path = Path("config/settings.example.json")
        if example_path.exists():
            print("Configuration not found. Copying example...")
            import shutil
            shutil.copy(example_path, config_path)
            print("Configuration created from example")
        else:
            print("No configuration found. Please create config/settings.json")
            return False
    else:
        print("Configuration found")
    
    return True

def main():
    """Start the web interface."""
    print("AutoBlogger Web Interface")
    print("=" * 40)
    
    # Check requirements
    if not check_requirements():
        print("\nRequirements not met. Please install dependencies:")
        print("pip install -r requirements.txt")
        return 1
    
    # Check configuration
    if not check_config():
        print("\nConfiguration not found. Please set up config/settings.json")
        return 1
    
    print("\nAll checks passed!")
    print("\nStarting web server...")
    print("Open your browser to: http://localhost:3500")
    print("Press Ctrl+C to stop")
    print("=" * 40)
    
    # Import and run the web app
    try:
        from web_app import app
        app.run(host='0.0.0.0', port=3500, debug=True)
    except KeyboardInterrupt:
        print("\nWeb server stopped")
        return 0
    except Exception as e:
        print(f"\nFailed to start web server: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
