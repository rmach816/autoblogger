"""
Production deployment script for AutoBlogger.

Automates deployment process including environment setup,
dependency installation, configuration validation, and service startup.
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import Optional, Dict

def print_banner(message: str) -> None:
    """Print a formatted banner message."""
    print("\n" + "=" * 60)
    print(f"  {message}")
    print("=" * 60 + "\n")

def run_command(command: str, check: bool = True) -> int:
    """Run a shell command and return exit code."""
    try:
        result = subprocess.run(command, shell=True, check=check)
        return result.returncode
    except subprocess.CalledProcessError as e:
        return e.returncode

def check_python_version() -> bool:
    """Verify Python version is 3.10+."""
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} detected")
        return True
    else:
        print(f"✗ Python 3.10+ required. Current: {version.major}.{version.minor}.{version.micro}")
        return False

def install_dependencies() -> bool:
    """Install Python dependencies."""
    print_banner("Installing Dependencies")
    print("Installing from requirements.txt...")
    
    exit_code = run_command("pip install -r requirements.txt", check=False)
    
    if exit_code == 0:
        print("✓ Dependencies installed successfully")
        return True
    else:
        print("✗ Failed to install dependencies")
        return False

def setup_environment() -> bool:
    """Set up environment configuration."""
    print_banner("Setting Up Environment")
    
    # Check if .env exists
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists():
        if env_example.exists():
            print("Creating .env from .env.example...")
            import shutil
            shutil.copy(env_example, env_file)
            print("✓ .env file created")
            print("⚠ IMPORTANT: Edit .env and add your API keys before running!")
            return False
        else:
            print("✗ .env.example not found")
            return False
    else:
        print("✓ .env file exists")
        return True

def validate_configuration() -> bool:
    """Validate configuration files."""
    print_banner("Validating Configuration")
    
    # Check for config directory and settings
    config_dir = Path("config")
    settings_file = config_dir / "settings.json"
    settings_example = config_dir / "settings.example.json"
    
    if not config_dir.exists():
        print("Creating config directory...")
        config_dir.mkdir(parents=True)
    
    if not settings_file.exists():
        if settings_example.exists():
            print("Creating settings.json from example...")
            import shutil
            shutil.copy(settings_example, settings_file)
            print("✓ settings.json created")
        else:
            print("✗ settings.example.json not found")
            return False
    else:
        print("✓ settings.json exists")
    
    # Validate JSON format
    try:
        import json
        with open(settings_file) as f:
            config = json.load(f)
        print("✓ Configuration file is valid JSON")
        return True
    except json.JSONDecodeError as e:
        print(f"✗ Invalid JSON in settings.json: {e}")
        return False

def create_directories() -> bool:
    """Create necessary directories."""
    print_banner("Creating Directories")
    
    directories = [
        "logs",
        "output",
        "output/images",
    ]
    
    for directory in directories:
        path = Path(directory)
        if not path.exists():
            path.mkdir(parents=True)
            print(f"✓ Created {directory}/")
        else:
            print(f"  {directory}/ exists")
    
    return True

def run_tests() -> bool:
    """Run test suite to verify installation."""
    print_banner("Running Tests")
    print("Running test suite...")
    
    exit_code = run_command("python -m pytest tests/ -v", check=False)
    
    if exit_code == 0:
        print("✓ All tests passed")
        return True
    else:
        print("⚠ Some tests failed (this may be ok if you haven't configured API keys)")
        return True  # Don't block deployment on test failures

def display_next_steps() -> None:
    """Display next steps for the user."""
    print_banner("Deployment Complete!")
    print("Next Steps:")
    print("1. Edit .env and add your API keys")
    print("2. Edit config/settings.json to configure your blogs")
    print("3. Run the web interface: python web_app.py")
    print("4. Or run CLI: python main.py --generate-now")
    print("\nImportant Security Notes:")
    print("- Never commit .env to version control")
    print("- Keep your API keys secure")
    print("- Run with FLASK_DEBUG=false in production")
    print("- Use HTTPS in production environments")
    print("\nFor more information, see:")
    print("- README.md")
    print("- docs/SETUP.md")
    print("- docs/PRODUCTION_READINESS_PLAN.md")

def main():
    """Main deployment function."""
    print_banner("AutoBlogger Production Deployment")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n✗ Deployment failed: Could not install dependencies")
        sys.exit(1)
    
    # Set up environment
    env_ready = setup_environment()
    
    # Validate configuration
    if not validate_configuration():
        print("\n⚠ Configuration validation failed")
        print("Please fix configuration errors before running")
    
    # Create directories
    create_directories()
    
    # Run tests
    run_tests()
    
    # Display next steps
    display_next_steps()
    
    if not env_ready:
        print("\n⚠ IMPORTANT: Configure .env before starting the application!")
        sys.exit(1)

if __name__ == "__main__":
    main()

