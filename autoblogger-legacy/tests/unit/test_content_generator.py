"""
Unit tests for content generator.

Tests the content generation functionality including AI providers,
prompt creation, and article generation.
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, patch

from src.content_generator import (
    MockAIProvider, 
    ContentGenerator, 
    create_ai_provider,
    GenerationError
)
from src.models import BlogConfig


class TestMockAIProvider:
    """Test the mock AI provider."""
    
    @pytest.mark.asyncio
    async def test_generate_content_basic(self, mock_ai_provider):
        """Test basic content generation."""
        prompt = "Write about sustainable gardening"
        content = await mock_ai_provider.generate_content(prompt)
        
        assert content is not None
        assert len(content) > 100
        assert "sustainable gardening" in content.lower()
    
    @pytest.mark.asyncio
    async def test_generate_content_different_topics(self, mock_ai_provider):
        """Test content generation for different topics."""
        # Test gardening topic
        gardening_prompt = "Write about gardening tips"
        gardening_content = await mock_ai_provider.generate_content(gardening_prompt)
        assert "gardening" in gardening_content.lower()
        
        # Test technology topic
        tech_prompt = "Write about technology trends"
        tech_content = await mock_ai_provider.generate_content(tech_prompt)
        assert "technology" in tech_content.lower()
    
    @pytest.mark.asyncio
    async def test_generate_content_structure(self, mock_ai_provider):
        """Test that generated content has proper structure."""
        prompt = "Write a comprehensive guide"
        content = await mock_ai_provider.generate_content(prompt)
        
        # Check for basic structure
        assert "#" in content  # Should have headings
        assert len(content.split('\n')) > 5  # Should have multiple paragraphs
        assert len(content.split()) > 50  # Should be substantial content


class TestContentGenerator:
    """Test the content generator orchestrator."""
    
    @pytest.mark.asyncio
    async def test_generate_article_basic(self, content_generator, sample_blog_config):
        """Test basic article generation."""
        article = await content_generator.generate_article(sample_blog_config)
        
        assert article is not None
        assert article.id is not None
        assert article.title is not None
        assert article.content is not None
        assert article.meta_description is not None
        assert article.blog_id == sample_blog_config.id
        assert article.keywords == sample_blog_config.keywords
    
    @pytest.mark.asyncio
    async def test_generate_article_title_extraction(self, content_generator, sample_blog_config):
        """Test that title is properly extracted from content."""
        article = await content_generator.generate_article(sample_blog_config)
        
        assert article.title is not None
        assert len(article.title) > 0
        assert len(article.title) < 200  # Reasonable title length
    
    @pytest.mark.asyncio
    async def test_generate_article_meta_description(self, content_generator, sample_blog_config):
        """Test meta description generation."""
        article = await content_generator.generate_article(sample_blog_config)
        
        assert article.meta_description is not None
        assert len(article.meta_description) > 0
        assert len(article.meta_description) <= 160  # SEO best practice
    
    @pytest.mark.asyncio
    async def test_generate_article_word_count(self, content_generator, sample_blog_config):
        """Test that word count is calculated correctly."""
        article = await content_generator.generate_article(sample_blog_config)
        
        assert article.word_count > 0
        # Word count should be reasonable for the content
        assert 50 <= article.word_count <= 5000
    
    @pytest.mark.asyncio
    async def test_generate_article_different_configs(self, content_generator):
        """Test article generation with different blog configurations."""
        # Test different niches
        configs = [
            BlogConfig(
                id="test_001",
                niche="technology",
                target_audience="developers",
                tone="professional",
                keywords=["programming", "software"],
                word_count=800
            ),
            BlogConfig(
                id="test_002", 
                niche="health and wellness",
                target_audience="fitness enthusiasts",
                tone="motivational",
                keywords=["fitness", "nutrition"],
                word_count=1200
            )
        ]
        
        for config in configs:
            article = await content_generator.generate_article(config)
            assert article is not None
            assert article.blog_id == config.id
            assert article.keywords == config.keywords
    
    @pytest.mark.asyncio
    async def test_prompt_creation(self, content_generator, sample_blog_config):
        """Test that prompts are created correctly."""
        prompt = content_generator._create_prompt(sample_blog_config)
        
        assert prompt is not None
        assert sample_blog_config.niche in prompt
        assert sample_blog_config.target_audience in prompt
        assert sample_blog_config.tone in prompt
        assert str(sample_blog_config.word_count) in prompt
        assert all(keyword in prompt for keyword in sample_blog_config.keywords)
    
    @pytest.mark.asyncio
    async def test_generation_error_handling(self, sample_blog_config):
        """Test error handling during generation."""
        # Create a mock provider that raises an exception
        mock_provider = AsyncMock()
        mock_provider.generate_content.side_effect = Exception("API Error")
        
        generator = ContentGenerator(mock_provider)
        
        with pytest.raises(GenerationError):
            await generator.generate_article(sample_blog_config)
    
    @pytest.mark.asyncio
    async def test_meta_description_generation(self, content_generator, sample_blog_config):
        """Test meta description generation logic."""
        # Test with content that has paragraphs
        test_content = "This is the first paragraph.\n\nThis is the second paragraph."
        meta_desc = content_generator._generate_meta_description(test_content, sample_blog_config)
        
        assert meta_desc is not None
        assert len(meta_desc) > 0
        assert "This is the first paragraph" in meta_desc
    
    @pytest.mark.asyncio
    async def test_title_extraction_edge_cases(self, content_generator):
        """Test title extraction with edge cases."""
        # Test with content starting with heading
        content_with_h1 = "# Main Title\n\nContent here"
        title = content_generator._extract_title(content_with_h1)
        assert title == "Main Title"
        
        # Test with content without heading
        content_without_h1 = "Just some content without heading"
        title = content_generator._extract_title(content_without_h1)
        assert title == "Just some content without heading"
        
        # Test with empty content
        title = content_generator._extract_title("")
        assert title == "Generated Article"


class TestAIProviderFactory:
    """Test AI provider creation."""
    
    def test_create_mock_provider(self):
        """Test creating mock provider."""
        provider = create_ai_provider("mock")
        assert isinstance(provider, MockAIProvider)
    
    def test_create_unknown_provider(self):
        """Test creating unknown provider raises error."""
        with pytest.raises(ValueError, match="Unknown AI provider"):
            create_ai_provider("unknown")
    
    def test_create_gemini_provider_without_key(self):
        """Test creating Gemini provider without API key."""
        with pytest.raises(ValueError, match="API key required"):
            create_ai_provider("gemini")
    
    def test_create_gemini_provider_with_key(self):
        """Test creating Gemini provider with API key."""
        provider = create_ai_provider("gemini", "test_key")
        assert provider.name == "gemini"
        assert provider.api_key == "test_key"


class TestContentGeneratorIntegration:
    """Integration tests for content generator."""
    
    @pytest.mark.asyncio
    async def test_full_generation_workflow(self, content_generator, sample_blog_config):
        """Test the complete article generation workflow."""
        # Generate article
        article = await content_generator.generate_article(sample_blog_config)
        
        # Verify all required fields are present
        assert article.id is not None
        assert article.title is not None
        assert article.content is not None
        assert article.meta_description is not None
        assert article.keywords == sample_blog_config.keywords
        assert article.word_count > 0
        assert article.blog_id == sample_blog_config.id
        assert article.created_at is not None
        
        # Verify content quality
        assert len(article.content) > 500  # Substantial content
        assert len(article.title) > 10  # Reasonable title length
        assert len(article.meta_description) > 20  # Reasonable meta description
    
    @pytest.mark.asyncio
    async def test_multiple_articles_consistency(self, content_generator, sample_blog_config):
        """Test that multiple articles are generated consistently."""
        articles = []
        
        # Generate multiple articles
        for _ in range(3):
            article = await content_generator.generate_article(sample_blog_config)
            articles.append(article)
        
        # Verify all articles are unique
        article_ids = [article.id for article in articles]
        assert len(set(article_ids)) == len(article_ids)  # All unique IDs
        
        # Verify all articles have the same blog_id
        for article in articles:
            assert article.blog_id == sample_blog_config.id
            assert article.keywords == sample_blog_config.keywords
