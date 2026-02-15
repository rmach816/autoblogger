"""
Base publisher class for AutoBlogger.

Defines the abstract interface that all publishers must implement,
ensuring consistent behavior across different publishing platforms.
"""

from abc import ABC, abstractmethod
from typing import Optional
from datetime import datetime
import uuid

from models import Article, PublishResponse, PublisherError
from utils.logger import get_logger

logger = get_logger(__name__)


class BasePublisher(ABC):
    """Abstract base class for all publishers."""
    
    def __init__(self, name: str):
        """
        Initialize publisher.
        
        Args:
            name: Publisher name for logging
        """
        self.name = name
        self.logger = get_logger(f"publisher.{name}")
    
    @abstractmethod
    async def publish(self, article: Article) -> PublishResponse:
        """
        Publish an article to the platform.
        
        Args:
            article: Article to publish
            
        Returns:
            PublishResponse with success status and details
        """
        pass
    
    @abstractmethod
    async def validate_credentials(self) -> bool:
        """
        Validate publisher credentials.
        
        Returns:
            True if credentials are valid
        """
        pass
    
    @abstractmethod
    async def preview(self, article: Article) -> str:
        """
        Generate HTML preview of the article.
        
        Args:
            article: Article to preview
            
        Returns:
            HTML preview string
        """
        pass
    
    async def test_connection(self) -> bool:
        """
        Test connection to the publishing platform.
        
        Returns:
            True if connection is successful
        """
        try:
            return await self.validate_credentials()
        except Exception as e:
            self.logger.error(f"Connection test failed: {e}")
            return False
    
    def _generate_article_id(self) -> str:
        """Generate unique article ID."""
        return f"art_{uuid.uuid4().hex[:8]}"
    
    def _log_publish_attempt(self, article: Article) -> None:
        """Log publishing attempt."""
        self.logger.info(
            f"Publishing article: {article.title}",
            extra={
                "article_id": article.id,
                "blog_id": article.blog_id,
                "publisher": self.name,
                "action": "publish_attempt"
            }
        )
    
    def _log_publish_success(self, article: Article, response: PublishResponse) -> None:
        """Log successful publishing."""
        self.logger.info(
            f"Successfully published article: {article.title}",
            extra={
                "article_id": article.id,
                "blog_id": article.blog_id,
                "publisher": self.name,
                "action": "publish_success",
                "url": response.url
            }
        )
    
    def _log_publish_error(self, article: Article, error: Exception) -> None:
        """Log publishing error."""
        self.logger.error(
            f"Failed to publish article: {article.title} - {error}",
            extra={
                "article_id": article.id,
                "blog_id": article.blog_id,
                "publisher": self.name,
                "action": "publish_error",
                "error": str(error)
            }
        )
