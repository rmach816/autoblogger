"""
Data models for AutoBlogger.

Defines the core data structures used throughout the application,
following the Result pattern for error handling.
"""

from dataclasses import dataclass
from typing import Union, List, Optional, Literal, Any
from datetime import datetime
from pydantic import BaseModel, Field, validator


# Result pattern for error handling
@dataclass
class Ok:
    """Success result containing a value."""
    value: Any


@dataclass
class Err:
    """Error result containing an error."""
    error: Any


Result = Union[Ok, Err]


# Core data models
class BlogConfig(BaseModel):
    """Configuration for a single blog."""
    id: str = Field(..., min_length=1, max_length=50)
    niche: str = Field(..., min_length=3, max_length=100)
    target_audience: str = Field(..., min_length=3, max_length=100)
    tone: str = Field(default="professional", min_length=3, max_length=50)
    posts_per_week: int = Field(default=1, ge=1, le=7)
    keywords: List[str] = Field(default_factory=list, max_items=10)
    word_count: int = Field(default=1000, ge=500, le=3000)
    publish_to: Literal["file", "wix", "wordpress", "medium"] = "file"
    
    # Business information (optional)
    business_name: Optional[str] = None
    business_phone: Optional[str] = None
    business_website: Optional[str] = None
    service_areas: Optional[str] = None
    specialties: List[str] = Field(default_factory=list)
    
    @validator("keywords")
    def validate_keywords(cls, v):
        if any(len(kw) < 2 for kw in v):
            raise ValueError("Keywords must be at least 2 characters")
        return v


class AppConfig(BaseModel):
    """Main application configuration."""
    ai_provider: Literal["real", "gemini", "groq", "mock"] = "mock"
    publisher: Literal["file", "wix", "wordpress", "medium"] = "file"
    environment: Literal["development", "staging", "production"] = "development"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    max_posts_per_day: int = Field(default=7, ge=1, le=50)
    request_timeout: int = Field(default=30, ge=5, le=300)
    blogs: List[BlogConfig] = Field(default_factory=list)


class Article(BaseModel):
    """Generated blog article."""
    id: str
    title: str
    content: str
    meta_description: str
    keywords: List[str]
    word_count: int
    blog_id: str
    created_at: datetime
    image_url: Optional[str] = None
    seo_score: Optional[int] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class PublishResponse(BaseModel):
    """Response from publishing an article."""
    success: bool
    url: Optional[str] = None
    message: str
    published_at: Optional[datetime] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


# Error types
class AutoBloggerError(Exception):
    """Base exception for AutoBlogger."""
    pass


class ConfigError(AutoBloggerError):
    """Configuration-related errors."""
    pass


class APIError(AutoBloggerError):
    """API-related errors."""
    pass


class RateLimitError(APIError):
    """Rate limit exceeded."""
    pass


class NetworkError(APIError):
    """Network-related errors."""
    pass


class PublisherError(AutoBloggerError):
    """Publisher-related errors."""
    pass


class GenerationError(AutoBloggerError):
    """Content generation errors."""
    pass


class ImageError(AutoBloggerError):
    """Image-related errors."""
    pass


class ImageSuggestion(BaseModel):
    """Image suggestion for articles."""
    id: str
    title: str
    description: str
    url: str
    thumbnail_url: str
    photographer: str
    photographer_url: str
    download_url: str
    width: int
    height: int
    created_at: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }