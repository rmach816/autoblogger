"""
Pytest configuration and fixtures for AutoBlogger tests.

Provides common test fixtures and configuration for all test modules.
"""

import pytest
import asyncio
import json
import tempfile
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# Add src to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.models import BlogConfig, AppConfig, Article
from src.content_generator import MockAIProvider, ContentGenerator
from src.publishers.file_publisher import FilePublisher


@pytest.fixture
def sample_blog_config():
    """Sample blog configuration for testing."""
    return BlogConfig(
        id="test_blog_001",
        niche="sustainable gardening",
        target_audience="urban gardeners",
        tone="friendly and informative",
        posts_per_week=2,
        keywords=["eco-friendly", "organic", "sustainable"],
        word_count=1000,
        publish_to="file"
    )


@pytest.fixture
def sample_app_config(sample_blog_config):
    """Sample application configuration for testing."""
    return AppConfig(
        ai_provider="mock",
        publisher="file",
        environment="development",
        log_level="INFO",
        max_posts_per_day=7,
        request_timeout=30,
        blogs=[sample_blog_config]
    )


@pytest.fixture
def sample_article(sample_blog_config):
    """Sample article for testing."""
    return Article(
        id="art_test123",
        title="Test Article Title",
        content="# Test Article\n\nThis is a test article content.",
        meta_description="Test meta description",
        keywords=["test", "article"],
        word_count=10,
        blog_id=sample_blog_config.id,
        created_at=datetime.now()
    )


@pytest.fixture
def mock_ai_provider():
    """Mock AI provider for testing."""
    return MockAIProvider()


@pytest.fixture
def content_generator(mock_ai_provider):
    """Content generator with mock AI provider."""
    return ContentGenerator(mock_ai_provider)


@pytest.fixture
def file_publisher():
    """File publisher for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield FilePublisher(output_dir=temp_dir)


@pytest.fixture
def temp_config_file(sample_app_config):
    """Temporary configuration file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(sample_app_config.dict(), f, indent=2)
        yield f.name


@pytest.fixture
def temp_output_dir():
    """Temporary output directory for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_api_responses():
    """Mock API responses for testing."""
    return {
        "gemini_success": {
            "content": "This is a generated article about sustainable gardening...",
            "usage": {"total_tokens": 1000}
        },
        "unsplash_success": {
            "urls": {
                "regular": "https://images.unsplash.com/photo-1234567890"
            },
            "alt_description": "Beautiful garden image"
        },
        "rate_limit_error": {
            "error": "Rate limit exceeded",
            "retry_after": 60
        }
    }


@pytest.fixture
def sample_config_data():
    """Sample configuration data for testing."""
    return {
        "ai_provider": "mock",
        "publisher": "file",
        "environment": "development",
        "log_level": "INFO",
        "max_posts_per_day": 7,
        "request_timeout": 30,
        "blogs": [
            {
                "id": "test_blog_001",
                "niche": "sustainable gardening",
                "target_audience": "urban gardeners",
                "tone": "friendly and informative",
                "posts_per_week": 2,
                "keywords": ["eco-friendly", "organic", "sustainable"],
                "word_count": 1000,
                "publish_to": "file"
            }
        ]
    }


# Async test utilities
@pytest.fixture
def async_test():
    """Fixture for async tests."""
    def _async_test(coro):
        return asyncio.run(coro)
    return _async_test


# Test data fixtures
@pytest.fixture
def test_articles():
    """Multiple test articles for batch testing."""
    return [
        Article(
            id=f"art_test{i}",
            title=f"Test Article {i}",
            content=f"# Test Article {i}\n\nContent for article {i}.",
            meta_description=f"Meta description for article {i}",
            keywords=["test", f"article{i}"],
            word_count=50 + i * 10,
            blog_id="test_blog_001",
            created_at=datetime.now()
        )
        for i in range(1, 4)
    ]


@pytest.fixture
def test_blogs():
    """Multiple test blog configurations."""
    return [
        BlogConfig(
            id=f"test_blog_{i:03d}",
            niche=f"Test Niche {i}",
            target_audience=f"Test Audience {i}",
            tone="professional",
            posts_per_week=1,
            keywords=[f"keyword{i}"],
            word_count=1000,
            publish_to="file"
        )
        for i in range(1, 4)
    ]
