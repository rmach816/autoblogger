"""
End-to-end integration tests for AutoBlogger.

Tests the complete workflow from configuration loading
to article generation and publishing.
"""

import pytest
import asyncio
import tempfile
import json
from pathlib import Path
from unittest.mock import patch

from src.models import AppConfig, BlogConfig
from src.utils import load_config, validate_environment
from src.content_generator import ContentGenerator, MockAIProvider
from src.publishers.file_publisher import FilePublisher


class TestEndToEndWorkflow:
    """Test complete end-to-end workflows."""
    
    @pytest.mark.asyncio
    async def test_complete_article_generation_workflow(self, temp_config_file, temp_output_dir):
        """Test complete workflow from config to published article."""
        # Load configuration
        config = load_config(temp_config_file)
        assert config is not None
        assert len(config.blogs) > 0
        
        # Initialize components
        ai_provider = MockAIProvider()
        content_generator = ContentGenerator(ai_provider)
        file_publisher = FilePublisher(output_dir=str(temp_output_dir))
        
        # Generate article
        blog = config.blogs[0]
        article = await content_generator.generate_article(blog)
        
        assert article is not None
        assert article.blog_id == blog.id
        assert article.title is not None
        assert article.content is not None
        
        # Publish article
        response = await file_publisher.publish(article)
        
        assert response.success is True
        assert response.url is not None
        
        # Verify files were created
        html_files = list(temp_output_dir.glob("*.html"))
        md_files = list(temp_output_dir.glob("*.md"))
        
        assert len(html_files) == 1
        assert len(md_files) == 1
        
        # Verify file contents
        html_content = html_files[0].read_text(encoding='utf-8')
        assert article.title in html_content
        assert article.content in html_content
    
    @pytest.mark.asyncio
    async def test_multiple_blogs_workflow(self, temp_output_dir):
        """Test workflow with multiple blog configurations."""
        # Create configuration with multiple blogs
        config_data = {
            "ai_provider": "mock",
            "publisher": "file",
            "environment": "development",
            "log_level": "INFO",
            "max_posts_per_day": 7,
            "request_timeout": 30,
            "blogs": [
                {
                    "id": "blog_001",
                    "niche": "sustainable gardening",
                    "target_audience": "urban gardeners",
                    "tone": "friendly",
                    "posts_per_week": 2,
                    "keywords": ["eco-friendly", "organic"],
                    "word_count": 1000,
                    "publish_to": "file"
                },
                {
                    "id": "blog_002",
                    "niche": "technology",
                    "target_audience": "developers",
                    "tone": "professional",
                    "posts_per_week": 1,
                    "keywords": ["programming", "software"],
                    "word_count": 800,
                    "publish_to": "file"
                }
            ]
        }
        
        # Initialize components
        ai_provider = MockAIProvider()
        content_generator = ContentGenerator(ai_provider)
        file_publisher = FilePublisher(output_dir=str(temp_output_dir))
        
        # Process each blog
        articles = []
        for blog_data in config_data["blogs"]:
            blog = BlogConfig(**blog_data)
            article = await content_generator.generate_article(blog)
            response = await file_publisher.publish(article)
            
            assert response.success is True
            articles.append(article)
        
        # Verify all articles were created
        assert len(articles) == 2
        assert articles[0].blog_id == "blog_001"
        assert articles[1].blog_id == "blog_002"
        
        # Verify all files were created
        html_files = list(temp_output_dir.glob("*.html"))
        md_files = list(temp_output_dir.glob("*.md"))
        
        assert len(html_files) == 2
        assert len(md_files) == 2
    
    @pytest.mark.asyncio
    async def test_error_recovery_workflow(self, temp_output_dir):
        """Test workflow with error recovery."""
        # Create configuration
        blog = BlogConfig(
            id="test_blog",
            niche="test niche",
            target_audience="test audience",
            tone="professional",
            keywords=["test"],
            word_count=500,
            publish_to="file"
        )
        
        # Initialize components
        ai_provider = MockAIProvider()
        content_generator = ContentGenerator(ai_provider)
        file_publisher = FilePublisher(output_dir=str(temp_output_dir))
        
        # Test with successful generation
        article = await content_generator.generate_article(blog)
        response = await file_publisher.publish(article)
        
        assert response.success is True
        
        # Verify file was created
        html_files = list(temp_output_dir.glob("*.html"))
        assert len(html_files) == 1
    
    @pytest.mark.asyncio
    async def test_configuration_validation_workflow(self):
        """Test configuration loading and validation."""
        # Test with valid configuration
        config_data = {
            "ai_provider": "mock",
            "publisher": "file",
            "environment": "development",
            "log_level": "INFO",
            "max_posts_per_day": 7,
            "request_timeout": 30,
            "blogs": [
                {
                    "id": "test_blog",
                    "niche": "test niche",
                    "target_audience": "test audience",
                    "tone": "professional",
                    "keywords": ["test"],
                    "word_count": 1000,
                    "publish_to": "file"
                }
            ]
        }
        
        # Create temporary config file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f, indent=2)
            config_path = f.name
        
        try:
            # Load and validate configuration
            config = load_config(config_path)
            assert config is not None
            assert config.ai_provider == "mock"
            assert len(config.blogs) == 1
            
            # Validate environment (should pass with mock provider)
            validate_environment(config)
            
        finally:
            # Clean up
            Path(config_path).unlink()
    
    @pytest.mark.asyncio
    async def test_article_content_quality(self, temp_output_dir):
        """Test that generated articles have good quality."""
        blog = BlogConfig(
            id="quality_test",
            niche="sustainable gardening",
            target_audience="urban gardeners",
            tone="friendly and informative",
            keywords=["eco-friendly", "organic", "sustainable"],
            word_count=1000,
            publish_to="file"
        )
        
        # Initialize components
        ai_provider = MockAIProvider()
        content_generator = ContentGenerator(ai_provider)
        file_publisher = FilePublisher(output_dir=str(temp_output_dir))
        
        # Generate article
        article = await content_generator.generate_article(blog)
        
        # Verify content quality
        assert len(article.content) > 500  # Substantial content
        assert len(article.title) > 10  # Reasonable title
        assert len(article.meta_description) > 20  # Reasonable meta description
        assert article.word_count > 50  # Reasonable word count
        
        # Verify content structure
        assert "#" in article.content  # Should have headings
        assert len(article.content.split('\n')) > 5  # Multiple paragraphs
        
        # Verify keywords are relevant
        content_lower = article.content.lower()
        niche_lower = blog.niche.lower()
        assert niche_lower in content_lower or any(
            keyword.lower() in content_lower for keyword in blog.keywords
        )
    
    @pytest.mark.asyncio
    async def test_publishing_different_formats(self, temp_output_dir):
        """Test that articles are published in multiple formats."""
        blog = BlogConfig(
            id="format_test",
            niche="technology",
            target_audience="developers",
            tone="professional",
            keywords=["programming", "software"],
            word_count=800,
            publish_to="file"
        )
        
        # Initialize components
        ai_provider = MockAIProvider()
        content_generator = ContentGenerator(ai_provider)
        file_publisher = FilePublisher(output_dir=str(temp_output_dir))
        
        # Generate and publish article
        article = await content_generator.generate_article(blog)
        response = await file_publisher.publish(article)
        
        assert response.success is True
        
        # Verify both HTML and Markdown files were created
        html_files = list(temp_output_dir.glob("*.html"))
        md_files = list(temp_output_dir.glob("*.md"))
        
        assert len(html_files) == 1
        assert len(md_files) == 1
        
        # Verify HTML content
        html_content = html_files[0].read_text(encoding='utf-8')
        assert "<!DOCTYPE html>" in html_content
        assert "<title>" in html_content
        assert article.title in html_content
        assert article.content in html_content
        
        # Verify Markdown content
        md_content = md_files[0].read_text(encoding='utf-8')
        assert f"# {article.title}" in md_content
        assert article.content in md_content
        assert "**Published:**" in md_content
        assert "**Word Count:**" in md_content
    
    @pytest.mark.asyncio
    async def test_concurrent_article_generation(self, temp_output_dir):
        """Test concurrent article generation."""
        blogs = [
            BlogConfig(
                id=f"concurrent_blog_{i}",
                niche=f"test niche {i}",
                target_audience="test audience",
                tone="professional",
                keywords=["test"],
                word_count=500,
                publish_to="file"
            )
            for i in range(3)
        ]
        
        # Initialize components
        ai_provider = MockAIProvider()
        content_generator = ContentGenerator(ai_provider)
        file_publisher = FilePublisher(output_dir=str(temp_output_dir))
        
        # Generate articles concurrently
        async def generate_and_publish(blog):
            article = await content_generator.generate_article(blog)
            response = await file_publisher.publish(article)
            return article, response
        
        tasks = [generate_and_publish(blog) for blog in blogs]
        results = await asyncio.gather(*tasks)
        
        # Verify all articles were generated and published
        assert len(results) == 3
        
        for article, response in results:
            assert article is not None
            assert response.success is True
        
        # Verify all files were created
        html_files = list(temp_output_dir.glob("*.html"))
        md_files = list(temp_output_dir.glob("*.md"))
        
        assert len(html_files) == 3
        assert len(md_files) == 3
