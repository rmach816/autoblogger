"""
Tests for security validators.

Validates input validation, sanitization, and security features.
"""

import pytest
from pathlib import Path

from src.security.validators import (
    validate_blog_config,
    validate_article_content,
    sanitize_html,
    sanitize_filename,
    validate_url,
    validate_email,
    validate_file_path,
    validate_integer,
    validate_string
)
from src.models import ConfigError


class TestValidateInput:
    """Test input validation functions."""
    
    def test_sanitize_html_basic(self):
        """Test basic HTML sanitization."""
        content = "<script>alert('XSS')</script>Hello"
        sanitized = sanitize_html(content)
        assert "<script>" not in sanitized
        assert "alert" not in sanitized
    
    def test_sanitize_html_empty(self):
        """Test sanitizing empty string."""
        assert sanitize_html("") == ""
        assert sanitize_html(None) == ""
    
    def test_sanitize_filename_dangerous_chars(self):
        """Test filename sanitization with dangerous characters."""
        filename = "../../../etc/passwd"
        sanitized = sanitize_filename(filename)
        assert ".." not in sanitized
        assert "/" not in sanitized
    
    def test_sanitize_filename_windows_chars(self):
        """Test filename sanitization with Windows forbidden characters."""
        filename = 'file<>:"|?*name.txt'
        sanitized = sanitize_filename(filename)
        assert all(char not in sanitized for char in '<>:"|?*')
    
    def test_sanitize_filename_length(self):
        """Test filename length limiting."""
        long_filename = "a" * 300 + ".txt"
        sanitized = sanitize_filename(long_filename)
        assert len(sanitized) <= 255
    
    def test_validate_url_valid_http(self):
        """Test URL validation with valid HTTP URL."""
        assert validate_url("http://example.com")
    
    def test_validate_url_valid_https(self):
        """Test URL validation with valid HTTPS URL."""
        assert validate_url("https://example.com")
    
    def test_validate_url_require_https(self):
        """Test URL validation requiring HTTPS."""
        with pytest.raises(ValueError, match="HTTPS required"):
            validate_url("http://example.com", require_https=True)
    
    def test_validate_url_invalid_scheme(self):
        """Test URL validation with invalid scheme."""
        with pytest.raises(ValueError):
            validate_url("javascript:alert('xss')")
    
    def test_validate_url_empty(self):
        """Test URL validation with empty string."""
        with pytest.raises(ValueError):
            validate_url("")
    
    def test_validate_email_valid(self):
        """Test email validation with valid email."""
        assert validate_email("user@example.com")
        assert validate_email("test.user+tag@domain.co.uk")
    
    def test_validate_email_invalid(self):
        """Test email validation with invalid email."""
        with pytest.raises(ValueError):
            validate_email("not-an-email")
        with pytest.raises(ValueError):
            validate_email("@example.com")
        with pytest.raises(ValueError):
            validate_email("user@")
    
    def test_validate_email_empty(self):
        """Test email validation with empty string."""
        with pytest.raises(ValueError):
            validate_email("")


class TestValidateContent:
    """Test content validation."""
    
    def test_validate_article_content_valid(self):
        """Test article content validation with valid content."""
        content = "This is a valid article content with enough text."
        assert validate_article_content(content)
    
    def test_validate_article_content_empty(self):
        """Test article content validation with empty content."""
        with pytest.raises(ValueError, match="cannot be empty"):
            validate_article_content("")
        with pytest.raises(ValueError):
            validate_article_content("   ")
    
    def test_validate_article_content_too_long(self):
        """Test article content validation with too long content."""
        content = "a" * 200000
        with pytest.raises(ValueError, match="exceeds maximum length"):
            validate_article_content(content, max_length=100000)
    
    def test_validate_article_content_xss(self):
        """Test article content validation detects XSS."""
        dangerous_content = "<script>alert('xss')</script>"
        with pytest.raises(ValueError, match="dangerous code"):
            validate_article_content(dangerous_content)
    
    def test_validate_article_content_javascript_protocol(self):
        """Test article content validation detects javascript: protocol."""
        dangerous_content = "Click <a href='javascript:alert(1)'>here</a>"
        with pytest.raises(ValueError, match="dangerous code"):
            validate_article_content(dangerous_content)


class TestValidateInteger:
    """Test integer validation."""
    
    def test_validate_integer_valid(self):
        """Test integer validation with valid integer."""
        assert validate_integer(42) == 42
        assert validate_integer("42") == 42
    
    def test_validate_integer_with_bounds(self):
        """Test integer validation with bounds."""
        assert validate_integer(5, min_value=1, max_value=10) == 5
    
    def test_validate_integer_below_min(self):
        """Test integer validation below minimum."""
        with pytest.raises(ValueError, match="at least 1"):
            validate_integer(0, min_value=1)
    
    def test_validate_integer_above_max(self):
        """Test integer validation above maximum."""
        with pytest.raises(ValueError, match="at most 10"):
            validate_integer(15, max_value=10)
    
    def test_validate_integer_invalid(self):
        """Test integer validation with invalid value."""
        with pytest.raises(ValueError, match="must be an integer"):
            validate_integer("not-a-number")


class TestValidateString:
    """Test string validation."""
    
    def test_validate_string_valid(self):
        """Test string validation with valid string."""
        assert validate_string("hello") == "hello"
    
    def test_validate_string_with_length(self):
        """Test string validation with length constraints."""
        assert validate_string("hello", min_length=3, max_length=10) == "hello"
    
    def test_validate_string_too_short(self):
        """Test string validation too short."""
        with pytest.raises(ValueError, match="at least 5"):
            validate_string("hi", min_length=5)
    
    def test_validate_string_too_long(self):
        """Test string validation too long."""
        with pytest.raises(ValueError, match="at most 5"):
            validate_string("hello world", max_length=5)
    
    def test_validate_string_with_pattern(self):
        """Test string validation with regex pattern."""
        assert validate_string("ABC123", pattern=r'^[A-Z0-9]+$') == "ABC123"
    
    def test_validate_string_invalid_pattern(self):
        """Test string validation with invalid pattern."""
        with pytest.raises(ValueError, match="does not match"):
            validate_string("abc!", pattern=r'^[A-Z0-9]+$')

