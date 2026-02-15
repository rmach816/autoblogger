"""
Input validation and sanitization utilities.

Provides comprehensive validation for user inputs, configuration data,
and content to prevent injection attacks and data corruption.
"""

import re
import html
from typing import Any, Dict, List, Optional
from pathlib import Path
from urllib.parse import urlparse

from pydantic import ValidationError
from models import BlogConfig, Article, ConfigError
from utils.logger import get_logger

logger = get_logger(__name__)


# Security constants
MAX_FILENAME_LENGTH = 255
MAX_TITLE_LENGTH = 200
MAX_CONTENT_LENGTH = 100000  # 100KB
MAX_URL_LENGTH = 2048
ALLOWED_URL_SCHEMES = ["http", "https"]
DANGEROUS_HTML_TAGS = [
    "script", "iframe", "object", "embed", "applet", 
    "meta", "link", "style", "base"
]


def validate_blog_config(config_data: Dict[str, Any]) -> BlogConfig:
    """
    Validate blog configuration data.
    
    Args:
        config_data: Raw configuration dictionary
        
    Returns:
        Validated BlogConfig instance
        
    Raises:
        ConfigError: If validation fails
    """
    try:
        # Validate using Pydantic model
        config = BlogConfig(**config_data)
        
        # Additional custom validation
        if config.posts_per_week < 1 or config.posts_per_week > 7:
            raise ConfigError("posts_per_week must be between 1 and 7")
        
        if config.word_count < 300 or config.word_count > 10000:
            raise ConfigError("word_count must be between 300 and 10000")
        
        # Validate keywords
        for keyword in config.keywords:
            if len(keyword) < 2:
                raise ConfigError(f"Keyword too short: {keyword}")
            if len(keyword) > 50:
                raise ConfigError(f"Keyword too long: {keyword}")
            if not re.match(r'^[a-zA-Z0-9\s\-]+$', keyword):
                raise ConfigError(f"Invalid characters in keyword: {keyword}")
        
        logger.info(f"Blog config validated: {config.id}")
        return config
        
    except ValidationError as e:
        logger.error(f"Blog config validation failed: {e}")
        raise ConfigError(f"Invalid blog configuration: {e}")


def validate_article_content(content: str, max_length: int = MAX_CONTENT_LENGTH) -> bool:
    """
    Validate article content for safety and size.
    
    Args:
        content: Article content to validate
        max_length: Maximum allowed content length
        
    Returns:
        True if valid
        
    Raises:
        ValueError: If content is invalid
    """
    if not content or not content.strip():
        raise ValueError("Content cannot be empty")
    
    if len(content) > max_length:
        raise ValueError(f"Content exceeds maximum length of {max_length} characters")
    
    # Check for dangerous patterns (basic XSS prevention)
    dangerous_patterns = [
        r'<script[^>]*>.*?</script>',
        r'javascript:',
        r'on\w+\s*=',  # Event handlers like onclick=
        r'data:text/html',
    ]
    
    content_lower = content.lower()
    for pattern in dangerous_patterns:
        if re.search(pattern, content_lower, re.DOTALL | re.IGNORECASE):
            logger.warning(f"Dangerous pattern detected in content: {pattern}")
            raise ValueError("Content contains potentially dangerous code")
    
    return True


def sanitize_html(content: str, allowed_tags: Optional[List[str]] = None) -> str:
    """
    Sanitize HTML content to prevent XSS attacks.
    
    Args:
        content: HTML content to sanitize
        allowed_tags: List of allowed HTML tags (None for basic sanitization)
        
    Returns:
        Sanitized HTML content
    """
    if not content:
        return ""
    
    # Escape HTML by default
    sanitized = html.escape(content)
    
    # If specific tags are allowed, we'd need a proper HTML sanitizer library
    # For now, we'll use basic escaping
    if allowed_tags:
        # TODO: Implement proper HTML sanitization with bleach or similar
        logger.warning("HTML tag whitelisting not fully implemented")
    
    return sanitized


def sanitize_filename(filename: str, max_length: int = MAX_FILENAME_LENGTH) -> str:
    """
    Sanitize filename for filesystem safety.
    
    Args:
        filename: Original filename
        max_length: Maximum allowed filename length
        
    Returns:
        Sanitized filename
    """
    if not filename:
        return "untitled"
    
    # Remove or replace dangerous characters
    # Windows forbidden characters: < > : " / \ | ? *
    # Unix/Linux forbidden characters: / \0
    forbidden_chars = r'[<>:"/\\|?*\x00-\x1f]'
    sanitized = re.sub(forbidden_chars, '_', filename)
    
    # Remove leading/trailing dots and spaces
    sanitized = sanitized.strip('. ')
    
    # Prevent directory traversal
    sanitized = sanitized.replace('..', '')
    
    # Limit length
    if len(sanitized) > max_length:
        # Keep extension if present
        parts = sanitized.rsplit('.', 1)
        if len(parts) == 2:
            name, ext = parts
            max_name_length = max_length - len(ext) - 1
            sanitized = f"{name[:max_name_length]}.{ext}"
        else:
            sanitized = sanitized[:max_length]
    
    # Ensure we have a valid filename
    if not sanitized or sanitized in ['.', '..']:
        sanitized = "untitled"
    
    return sanitized


def validate_url(url: str, require_https: bool = False) -> bool:
    """
    Validate URL for safety and correctness.
    
    Args:
        url: URL to validate
        require_https: Whether to require HTTPS
        
    Returns:
        True if valid
        
    Raises:
        ValueError: If URL is invalid
    """
    if not url:
        raise ValueError("URL cannot be empty")
    
    if len(url) > MAX_URL_LENGTH:
        raise ValueError(f"URL exceeds maximum length of {MAX_URL_LENGTH}")
    
    try:
        parsed = urlparse(url)
        
        # Check scheme
        if parsed.scheme not in ALLOWED_URL_SCHEMES:
            raise ValueError(f"Invalid URL scheme: {parsed.scheme}")
        
        if require_https and parsed.scheme != "https":
            raise ValueError("HTTPS required")
        
        # Check for hostname
        if not parsed.netloc:
            raise ValueError("URL must have a hostname")
        
        # Basic validation against common injection patterns
        dangerous_patterns = [
            'javascript:',
            'data:',
            'vbscript:',
            'file:',
        ]
        
        url_lower = url.lower()
        for pattern in dangerous_patterns:
            if pattern in url_lower:
                raise ValueError(f"Dangerous URL pattern detected: {pattern}")
        
        return True
        
    except Exception as e:
        logger.warning(f"URL validation failed: {url} - {e}")
        raise ValueError(f"Invalid URL: {e}")


def validate_email(email: str) -> bool:
    """
    Validate email address format.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid
        
    Raises:
        ValueError: If email is invalid
    """
    if not email:
        raise ValueError("Email cannot be empty")
    
    # Basic email regex (RFC 5322 simplified)
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(email_pattern, email):
        raise ValueError("Invalid email format")
    
    if len(email) > 254:  # RFC 5321
        raise ValueError("Email address too long")
    
    return True


def validate_file_path(file_path: str, base_dir: Optional[str] = None) -> Path:
    """
    Validate file path to prevent directory traversal attacks.
    
    Args:
        file_path: File path to validate
        base_dir: Base directory to restrict access to
        
    Returns:
        Validated Path object
        
    Raises:
        ValueError: If path is invalid or outside base directory
    """
    if not file_path:
        raise ValueError("File path cannot be empty")
    
    # Convert to Path object
    path = Path(file_path).resolve()
    
    # If base directory specified, ensure path is within it
    if base_dir:
        base = Path(base_dir).resolve()
        try:
            path.relative_to(base)
        except ValueError:
            raise ValueError(f"Path {file_path} is outside base directory {base_dir}")
    
    # Check for dangerous patterns
    path_str = str(path)
    if '..' in path_str or path_str.startswith(('.', '~')):
        raise ValueError("Path contains potentially dangerous patterns")
    
    return path


def validate_integer(value: Any, min_value: Optional[int] = None, 
                     max_value: Optional[int] = None, field_name: str = "value") -> int:
    """
    Validate integer value with optional bounds.
    
    Args:
        value: Value to validate
        min_value: Minimum allowed value
        max_value: Maximum allowed value
        field_name: Name of field for error messages
        
    Returns:
        Validated integer
        
    Raises:
        ValueError: If validation fails
    """
    try:
        int_value = int(value)
    except (TypeError, ValueError):
        raise ValueError(f"{field_name} must be an integer")
    
    if min_value is not None and int_value < min_value:
        raise ValueError(f"{field_name} must be at least {min_value}")
    
    if max_value is not None and int_value > max_value:
        raise ValueError(f"{field_name} must be at most {max_value}")
    
    return int_value


def validate_string(value: Any, min_length: int = 0, max_length: Optional[int] = None,
                   pattern: Optional[str] = None, field_name: str = "value") -> str:
    """
    Validate string value with optional constraints.
    
    Args:
        value: Value to validate
        min_length: Minimum string length
        max_length: Maximum string length
        pattern: Regex pattern to match
        field_name: Name of field for error messages
        
    Returns:
        Validated string
        
    Raises:
        ValueError: If validation fails
    """
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    
    if len(value) < min_length:
        raise ValueError(f"{field_name} must be at least {min_length} characters")
    
    if max_length is not None and len(value) > max_length:
        raise ValueError(f"{field_name} must be at most {max_length} characters")
    
    if pattern and not re.match(pattern, value):
        raise ValueError(f"{field_name} does not match required pattern")
    
    return value

