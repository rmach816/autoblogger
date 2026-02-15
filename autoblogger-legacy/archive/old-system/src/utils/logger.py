"""
Logging configuration for AutoBlogger.

Provides structured logging with JSON format for production
and human-readable format for development.
"""

import logging
import json
import sys
from datetime import datetime
from typing import Any, Dict, Optional
from pathlib import Path


class StructuredFormatter(logging.Formatter):
    """JSON formatter for structured logging."""
    
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add extra fields if present
        if hasattr(record, 'blog_id'):
            log_entry['blog_id'] = record.blog_id
        if hasattr(record, 'article_id'):
            log_entry['article_id'] = record.article_id
        if hasattr(record, 'action'):
            log_entry['action'] = record.action
        if hasattr(record, 'publisher'):
            log_entry['publisher'] = record.publisher
        if hasattr(record, 'duration_ms'):
            log_entry['duration_ms'] = record.duration_ms
        if hasattr(record, 'ai_provider'):
            log_entry['ai_provider'] = record.ai_provider
        if hasattr(record, 'tokens_used'):
            log_entry['tokens_used'] = record.tokens_used
            
        return json.dumps(log_entry)


def setup_logging(
    level: str = "INFO",
    environment: str = "development",
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    Set up logging configuration.
    
    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        environment: Environment (development, production)
        log_file: Optional log file path
        
    Returns:
        Configured logger instance
    """
    # Create logs directory if it doesn't exist
    if log_file:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    
    # Configure root logger
    logger = logging.getLogger("autoblogger")
    logger.setLevel(getattr(logging, level.upper()))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    if environment == "development":
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    else:
        console_formatter = StructuredFormatter()
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_formatter = StructuredFormatter()
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a specific module."""
    return logging.getLogger(f"autoblogger.{name}")


# Context manager for timing operations
class LogContext:
    """Context manager for logging operation timing."""
    
    def __init__(self, logger: logging.Logger, operation: str, **kwargs):
        self.logger = logger
        self.operation = operation
        self.kwargs = kwargs
        self.start_time = None
    
    def __enter__(self):
        self.start_time = datetime.now()
        self.logger.info(f"Starting {self.operation}", extra=self.kwargs)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = (datetime.now() - self.start_time).total_seconds() * 1000
        
        if exc_type is None:
            self.logger.info(
                f"Completed {self.operation}",
                extra={**self.kwargs, "duration_ms": int(duration)}
            )
        else:
            self.logger.error(
                f"Failed {self.operation}: {exc_val}",
                extra={**self.kwargs, "duration_ms": int(duration)}
            )
