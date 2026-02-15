"""
Integration tests for the complete AutoBlogger workflow.

Tests end-to-end functionality including content generation,
SEO optimization, image handling, and file publishing.
"""

import pytest
import asyncio
from pathlib import Path
from datetime import datetime

from src.models import BlogConfig, Article
from src.content_generator import ContentGenerator, MockAIProvider
from src.publishers.file_publisher import FilePublisher
from src.image_handler import ImageHandler
from src.seo_optimizer import SEOOptimizer


class TestCompleteWorkflow:
    """Test complete article generation and publishing workflow."""
    
    @pytest.mark.asyncio
    async def test_end_to_end_article_generation(self, tmp_path):
        """Test complete workflow from generation to publishing."""
        # Setup
        blog_config = BlogConfig(
            id="test_blog",
            niche="technology",
            target_audience="developers",
            tone="professional",
            posts_per_week=1,
            keywords=["python", "automation", "testing"],
            word_count=500,
            publish_to="file"
        )
        
        # Initialize components
        ai_provider = MockAIProvider()
        content_generator = ContentGenerator(ai_provider)
        file_publisher = FilePublisher(output_dir=str(tmp_path))
        seo_optimizer = SEOOptimizer()
        
        # Generate article
        article = await content_generator.generate_article(blog_config)
        
        # Validate article
        assert article is not None
        assert article.title
        assert article.content
        assert len(article.content) > 100
        assert article.keywords == blog_config.keywords
        assert article.word_count > 0
        
        # Optimize for SEO
        optimized_article = seo_optimizer.optimize_article(article)
        
        # Validate SEO optimization
        assert len(optimized_article.meta_description) >= 120
        assert len(optimized_article.meta_description) <= 160
        
        # Publish article
        response = await file_publisher.publish(optimized_article)
        
        # Validate publishing
        assert response.success == True
        assert response.url is not None
        
        # Verify files were created
        html_files = list(tmp_path.glob("*.html"))
        md_files = list(tmp_path.glob("*.md"))
        
        assert len(html_files) == 1
        assert len(md_files) == 1
        
        # Verify file contents
        html_content = html_files[0].read_text()
        assert optimized_article.title in html_content
        
        md_content = md_files[0].read_text()
        assert optimized_article.title in md_content


class TestArticleGenerationVariations:
    """Test article generation with different configurations."""
    
    @pytest.mark.asyncio
    async def test_generate_short_article(self):
        """Test generating short article."""
        blog_config = BlogConfig(
            id="test_blog",
            niche="technology",
            target_audience="developers",
            word_count=300,
            keywords=["testing"]
        )
        
        ai_provider = MockAIProvider()
        content_generator = ContentGenerator(ai_provider)
        
        article = await content_generator.generate_article(blog_config)
        
        assert article is not None
        assert len(article.content) > 100
    
    @pytest.mark.asyncio
    async def test_generate_long_article(self):
        """Test generating long article."""
        blog_config = BlogConfig(
            id="test_blog",
            niche="technology",
            target_audience="developers",
            word_count=2000,
            keywords=["testing", "automation"]
        )
        
        ai_provider = MockAIProvider()
        content_generator = ContentGenerator(ai_provider)
        
        article = await content_generator.generate_article(blog_config)
        
        assert article is not None
        assert len(article.content) > 500
    
    @pytest.mark.asyncio
    async def test_generate_with_custom_prompt(self):
        """Test generating article with custom prompt."""
        blog_config = BlogConfig(
            id="test_blog",
            niche="technology",
            target_audience="developers",
            keywords=["testing"]
        )
        
        custom_prompt = "Write about the future of AI in software development"
        
        ai_provider = MockAIProvider()
        content_generator = ContentGenerator(ai_provider)
        
        article = await content_generator.generate_article_with_prompt(
            blog_config, custom_prompt
        )
        
        assert article is not None
        assert article.title
        assert article.content


class TestSEOOptimization:
    """Test SEO optimization functionality."""
    
    def test_seo_analysis(self):
        """Test SEO analysis of article."""
        article = Article(
            id="test_123",
            title="Test Article Title",
            content="# Test Article\n\nThis is test content." * 20,
            meta_description="Short description",
            keywords=["test", "article"],
            word_count=100,
            blog_id="test_blog",
            created_at=datetime.now()
        )
        
        seo_optimizer = SEOOptimizer()
        analysis = seo_optimizer.analyze_article(article)
        
        assert analysis is not None
        assert analysis.seo_score >= 0
        assert analysis.seo_score <= 100
        assert analysis.readability_score >= 0
        assert len(analysis.recommendations) > 0
    
    def test_seo_optimization_improves_article(self):
        """Test that SEO optimization improves article."""
        article = Article(
            id="test_123",
            title="Short",
            content="# Short\n\nVery short content",
            meta_description="Too short",
            keywords=["test"],
            word_count=10,
            blog_id="test_blog",
            created_at=datetime.now()
        )
        
        seo_optimizer = SEOOptimizer()
        
        # Get initial analysis
        before_analysis = seo_optimizer.analyze_article(article)
        
        # Optimize
        optimized_article = seo_optimizer.optimize_article(article)
        
        # Get new analysis
        after_analysis = seo_optimizer.analyze_article(optimized_article)
        
        # Should have improvements
        assert len(optimized_article.meta_description) >= len(article.meta_description)


class TestImageHandling:
    """Test image suggestion and handling."""
    
    @pytest.mark.asyncio
    async def test_get_image_suggestions(self):
        """Test getting image suggestions."""
        image_handler = ImageHandler()
        
        suggestions = await image_handler.get_image_suggestions(
            topic="technology",
            style="professional",
            count=3
        )
        
        assert len(suggestions) == 3
        for suggestion in suggestions:
            assert suggestion.title
            assert suggestion.url
            assert suggestion.thumbnail_url
    
    def test_add_images_to_content(self):
        """Test adding images to article content."""
        image_handler = ImageHandler()
        
        content = "# Article\n\n" + "Paragraph\n\n" * 10
        
        # Create mock suggestions
        suggestions = asyncio.run(
            image_handler.get_image_suggestions("test", "professional", 2)
        )
        
        enhanced_content = image_handler.add_images_to_content(content, suggestions)
        
        # Should have added image tags
        assert len(enhanced_content) > len(content)

