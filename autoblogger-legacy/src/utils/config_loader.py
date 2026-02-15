"""
Configuration loading and validation for AutoBlogger.

Handles loading configuration from JSON files with validation,
defaults, and backward compatibility. Includes secure API key management.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from pydantic import ValidationError

from models import AppConfig, ConfigError
from utils.logger import get_logger

logger = get_logger(__name__)


# Sensitive keys that should never be logged
SENSITIVE_KEYS = {
    "GEMINI_API_KEY",
    "GROQ_API_KEY",
    "UNSPLASH_ACCESS_KEY",
    "WIX_API_KEY",
    "WORDPRESS_APP_PASSWORD",
    "MEDIUM_INTEGRATION_TOKEN",
    "AUTOBLOGGER_SECRET_KEY",
    "DATABASE_URL",
    "api_key",
    "password",
    "secret",
    "token"
}


def load_config(config_path: str = "config/settings.json") -> AppConfig:
    """
    Load and validate application configuration.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Validated AppConfig instance
        
    Raises:
        ConfigError: If configuration is invalid or missing
    """
    try:
        # Check if config file exists
        if not Path(config_path).exists():
            if Path("config/settings.example.json").exists():
                logger.warning(f"Config file {config_path} not found. Using example config.")
                config_path = "config/settings.example.json"
            else:
                raise ConfigError(f"Configuration file not found: {config_path}")
        
        # Load JSON configuration
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        
        # Validate configuration
        config = AppConfig(**config_data)
        
        logger.info(f"Configuration loaded from {config_path}")
        logger.info(f"Found {len(config.blogs)} blog(s) configured")
        
        return config
        
    except json.JSONDecodeError as e:
        raise ConfigError(f"Invalid JSON in config file: {e}")
    except ValidationError as e:
        raise ConfigError(f"Configuration validation failed: {e}")
    except Exception as e:
        raise ConfigError(f"Failed to load configuration: {e}")


def sanitize_for_logging(key: str, value: str) -> str:
    """
    Sanitize sensitive values for logging.
    
    Args:
        key: Environment variable name
        value: Environment variable value
        
    Returns:
        Sanitized value (masked if sensitive)
    """
    # Check if key contains sensitive information
    key_lower = key.lower()
    is_sensitive = any(sensitive in key_lower for sensitive in 
                      ["key", "password", "secret", "token", "credential"])
    
    if is_sensitive and value:
        # Show only first 4 and last 4 characters
        if len(value) > 12:
            return f"{value[:4]}...{value[-4:]}"
        else:
            return "***"
    
    return value


def load_environment_variables() -> Dict[str, str]:
    """
    Load environment variables for API keys and settings.
    Ensures sensitive values are never logged.
    
    Returns:
        Dictionary of environment variables (with sensitive values)
    """
    env_vars = {}
    
    # Load from .env file if present
    env_file = Path(".env")
    if env_file.exists():
        logger.info("Loading environment variables from .env file")
        from dotenv import load_dotenv
        load_dotenv()
    
    # Required API keys (not strictly required, but recommended)
    recommended_keys = [
        "GEMINI_API_KEY",
        "UNSPLASH_ACCESS_KEY"
    ]
    
    # Optional API keys
    optional_keys = [
        "GROQ_API_KEY",
        "WIX_API_KEY",
        "WIX_SITE_ID",
        "WIX_ACCOUNT_ID",
        "WORDPRESS_SITE_URL",
        "WORDPRESS_USERNAME",
        "WORDPRESS_APP_PASSWORD",
        "MEDIUM_INTEGRATION_TOKEN",
        "AUTOBLOGGER_SECRET_KEY",
        "FLASK_ENV",
        "FLASK_DEBUG",
        "ALLOWED_HOSTS",
        "CORS_ORIGINS",
        "RATE_LIMIT_ENABLED"
    ]
    
    # Load recommended keys
    for key in recommended_keys:
        value = os.getenv(key)
        if not value:
            logger.warning(f"Recommended environment variable {key} not set (using mock mode)")
        else:
            env_vars[key] = value
            logger.debug(f"Loaded {key}: {sanitize_for_logging(key, value)}")
    
    # Load optional keys
    for key in optional_keys:
        value = os.getenv(key)
        if value:
            env_vars[key] = value
            logger.debug(f"Loaded {key}: {sanitize_for_logging(key, value)}")
    
    return env_vars


def mask_sensitive_config(config_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Mask sensitive values in configuration for safe logging.
    
    Args:
        config_dict: Configuration dictionary
        
    Returns:
        Configuration with masked sensitive values
    """
    masked = config_dict.copy()
    
    for key in masked:
        if any(sensitive in key.lower() for sensitive in SENSITIVE_KEYS):
            if isinstance(masked[key], str) and len(masked[key]) > 4:
                masked[key] = f"{masked[key][:4]}...{masked[key][-4:]}"
            else:
                masked[key] = "***"
    
    return masked


def validate_environment(config: AppConfig) -> bool:
    """
    Validate that required environment variables are set.
    
    Args:
        config: Application configuration
        
    Returns:
        True if environment is valid
        
    Raises:
        ConfigError: If required environment variables are missing
    """
    env_vars = load_environment_variables()
    
    # Check AI provider requirements
    if config.ai_provider == "gemini" and not env_vars.get("GEMINI_API_KEY"):
        raise ConfigError("GEMINI_API_KEY is required for Gemini AI provider")
    
    if config.ai_provider == "groq" and not env_vars.get("GROQ_API_KEY"):
        raise ConfigError("GROQ_API_KEY is required for Groq AI provider")
    
    # Check publisher requirements
    for blog in config.blogs:
        if blog.publish_to == "wix":
            required_wix_keys = ["WIX_API_KEY", "WIX_SITE_ID", "WIX_ACCOUNT_ID"]
            missing = [key for key in required_wix_keys if not env_vars.get(key)]
            if missing:
                raise ConfigError(f"Wix publishing requires: {', '.join(missing)}")
        
        elif blog.publish_to == "wordpress":
            required_wp_keys = ["WORDPRESS_SITE_URL", "WORDPRESS_USERNAME", "WORDPRESS_APP_PASSWORD"]
            missing = [key for key in required_wp_keys if not env_vars.get(key)]
            if missing:
                raise ConfigError(f"WordPress publishing requires: {', '.join(missing)}")
        
        elif blog.publish_to == "medium":
            if not env_vars.get("MEDIUM_INTEGRATION_TOKEN"):
                raise ConfigError("Medium publishing requires MEDIUM_INTEGRATION_TOKEN")
    
    logger.info("Environment validation passed")
    return True


def create_default_config() -> AppConfig:
    """
    Create a default configuration for new users.
    
    Returns:
        Default AppConfig instance
    """
    from models import BlogConfig
    
    default_blog = BlogConfig(
        id="blog_001",
        niche="technology",
        target_audience="developers",
        tone="professional",
        posts_per_week=1,
        keywords=["technology", "programming", "development"],
        word_count=1000,
        publish_to="file"
    )
    
    return AppConfig(
        ai_provider="mock",
        publisher="file",
        environment="development",
        log_level="INFO",
        max_posts_per_day=7,
        request_timeout=30,
        blogs=[default_blog]
    )


def save_config(config: AppConfig, config_path: str = "config/settings.json") -> None:
    """
    Save configuration to file.
    
    Args:
        config: Configuration to save
        config_path: Path to save configuration
    """
    # Ensure directory exists
    Path(config_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Convert to dict and save
    config_dict = config.dict()
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config_dict, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Configuration saved to {config_path}")
