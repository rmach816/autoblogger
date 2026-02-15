"""
Unit tests for file publisher.

Tests the file publishing functionality including HTML/Markdown generation,
file creation, and error handling.
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, mock_open

from src.publishers.file_publisher import FilePublisher
from src.models import Article, PublishResponse, PublisherError
from datetime import datetime


class TestFilePublisher:
    """Test the file publisher."""
    
    def test_initialization(self):
        """Test publisher initialization."""
        with tempfile.TemporaryDirectory() as temp_dir:
            publisher = FilePublisher(output_dir=temp_dir)
            assert publisher.name == "file"
            assert publisher.output_dir == Path(temp_dir)
            assert publisher.output_dir.exists()
    
    def test_initialization_creates_directory(self):
        """Test that initialization creates output directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            new_dir = Path(temp_dir) / "new_output"
            publisher = FilePublisher(output_dir=str(new_dir))
            assert new_dir.exists()
    
    @pytest.mark.asyncio
    async def test_publish_success(self, file_publisher, sample_article):
        """Test successful article publishing."""
        response = await file_publisher.publish(sample_article)
        
        assert response.success is True
        assert response.url is not None
        assert "file://" in response.url
        assert response.published_at is not None
        assert "saved as" in response.message
    
    @pytest.mark.asyncio
    async def test_publish_creates_files(self, file_publisher, sample_article):
        """Test that publishing creates HTML and Markdown files."""
        response = await file_publisher.publish(sample_article)
        
        assert response.success is True
        
        # Check that files were created
        output_dir = file_publisher.output_dir
        html_files = list(output_dir.glob("*.html"))
        md_files = list(output_dir.glob("*.md"))
        
        assert len(html_files) == 1
        assert len(md_files) == 1
        
        # Check file contents
        html_content = html_files[0].read_text(encoding='utf-8')
        md_content = md_files[0].read_text(encoding='utf-8')
        
        assert sample_article.title in html_content
        assert sample_article.content in html_content
        assert sample_article.title in md_content
        assert sample_article.content in md_content
    
    @pytest.mark.asyncio
    async def test_publish_html_structure(self, file_publisher, sample_article):
        """Test that generated HTML has proper structure."""
        response = await file_publisher.publish(sample_article)
        
        assert response.success is True
        
        # Find the generated HTML file
        output_dir = file_publisher.output_dir
        html_files = list(output_dir.glob("*.html"))
        html_content = html_files[0].read_text(encoding='utf-8')
        
        # Check HTML structure
        assert "<!DOCTYPE html>" in html_content
        assert "<html" in html_content
        assert "<head>" in html_content
        assert "<title>" in html_content
        assert "<body>" in html_content
        assert sample_article.title in html_content
        assert sample_article.meta_description in html_content
        assert f"Keywords: {', '.join(sample_article.keywords)}" in html_content
    
    @pytest.mark.asyncio
    async def test_publish_markdown_structure(self, file_publisher, sample_article):
        """Test that generated Markdown has proper structure."""
        response = await file_publisher.publish(sample_article)
        
        assert response.success is True
        
        # Find the generated Markdown file
        output_dir = file_publisher.output_dir
        md_files = list(output_dir.glob("*.md"))
        md_content = md_files[0].read_text(encoding='utf-8')
        
        # Check Markdown structure
        assert f"# {sample_article.title}" in md_content
        assert "**Published:**" in md_content
        assert "**Word Count:" in md_content
        assert "**Keywords:**" in md_content
        assert sample_article.content in md_content
    
    @pytest.mark.asyncio
    async def test_publish_filename_sanitization(self, file_publisher):
        """Test that filenames are properly sanitized."""
        # Create article with problematic title
        article = Article(
            id="art_test",
            title="Test/Article:With<Invalid>Characters",
            content="Test content",
            meta_description="Test description",
            keywords=["test"],
            word_count=10,
            blog_id="test_blog",
            created_at=datetime.now()
        )
        
        response = await file_publisher.publish(article)
        
        assert response.success is True
        
        # Check that files were created with sanitized names
        output_dir = file_publisher.output_dir
        files = list(output_dir.glob("*"))
        
        # Should have 2 files (HTML and Markdown)
        assert len(files) == 2
        
        # Check that filenames don't contain invalid characters
        for file_path in files:
            filename = file_path.name
            assert "/" not in filename
            assert ":" not in filename
            assert "<" not in filename
            assert ">" not in filename
    
    @pytest.mark.asyncio
    async def test_publish_long_title_handling(self, file_publisher):
        """Test handling of very long titles."""
        long_title = "A" * 200  # Very long title
        article = Article(
            id="art_test",
            title=long_title,
            content="Test content",
            meta_description="Test description",
            keywords=["test"],
            word_count=10,
            blog_id="test_blog",
            created_at=datetime.now()
        )
        
        response = await file_publisher.publish(article)
        
        assert response.success is True
        
        # Check that filename is truncated
        output_dir = file_publisher.output_dir
        files = list(output_dir.glob("*"))
        
        for file_path in files:
            filename = file_path.name
            # Filename should be truncated (base filename + extension)
            assert len(filename) < 300  # Reasonable length
    
    @pytest.mark.asyncio
    async def test_validate_credentials_success(self, file_publisher):
        """Test successful credential validation."""
        result = await file_publisher.validate_credentials()
        assert result is True
    
    @pytest.mark.asyncio
    async def test_validate_credentials_failure(self):
        """Test credential validation failure with read-only directory."""
        # Create a read-only directory (this might not work on all systems)
        with tempfile.TemporaryDirectory() as temp_dir:
            read_only_dir = Path(temp_dir) / "readonly"
            read_only_dir.mkdir()
            
            # Try to make it read-only (this might fail on some systems)
            try:
                read_only_dir.chmod(0o444)  # Read-only
                publisher = FilePublisher(output_dir=str(read_only_dir))
                result = await publisher.validate_credentials()
                assert result is False
            except (PermissionError, OSError):
                # If we can't make it read-only, skip this test
                pytest.skip("Cannot create read-only directory on this system")
    
    @pytest.mark.asyncio
    async def test_preview_generation(self, file_publisher, sample_article):
        """Test HTML preview generation."""
        preview = await file_publisher.preview(sample_article)
        
        assert preview is not None
        assert "<!DOCTYPE html>" in preview
        assert sample_article.title in preview
        assert sample_article.content in preview
        assert sample_article.meta_description in preview
    
    @pytest.mark.asyncio
    async def test_publish_error_handling(self, file_publisher, sample_article):
        """Test error handling during publishing."""
        # Mock file writing to raise an exception
        with patch('pathlib.Path.write_text', side_effect=OSError("Disk full")):
            response = await file_publisher.publish(sample_article)
            
            assert response.success is False
            assert "Failed to save article" in response.message
    
    def test_sanitize_filename(self, file_publisher):
        """Test filename sanitization."""
        # Test various invalid characters
        test_cases = [
            ("normal_filename", "normal_filename"),
            ("file/with/slashes", "file_with_slashes"),
            ("file:with:colons", "file_with_colons"),
            ("file<with>brackets", "file_with_brackets"),
            ("file|with|pipes", "file_with_pipes"),
            ("file?with?questions", "file_with_questions"),
            ("file*with*stars", "file_with_stars"),
            ("very_long_filename_" + "x" * 200, "very_long_filename_" + "x" * 77)  # Truncated
        ]
        
        for input_name, expected in test_cases:
            result = file_publisher._sanitize_filename(input_name)
            assert result == expected
    
    @pytest.mark.asyncio
    async def test_multiple_articles_no_conflict(self, file_publisher):
        """Test that multiple articles don't conflict."""
        articles = []
        
        # Create multiple articles with same title (should not conflict)
        for i in range(3):
            article = Article(
                id=f"art_test_{i}",
                title="Same Title",  # Same title
                content=f"Content {i}",
                meta_description=f"Description {i}",
                keywords=["test"],
                word_count=10,
                blog_id="test_blog",
                created_at=datetime.now()
            )
            articles.append(article)
        
        # Publish all articles
        responses = []
        for article in articles:
            response = await file_publisher.publish(article)
            responses.append(response)
        
        # All should succeed
        for response in responses:
            assert response.success is True
        
        # Check that all files were created
        output_dir = file_publisher.output_dir
        html_files = list(output_dir.glob("*.html"))
        md_files = list(output_dir.glob("*.md"))
        
        assert len(html_files) == 3
        assert len(md_files) == 3
    
    @pytest.mark.asyncio
    async def test_html_template_rendering(self, file_publisher, sample_article):
        """Test that HTML template is rendered correctly."""
        response = await file_publisher.publish(sample_article)
        
        assert response.success is True
        
        # Get the HTML content
        output_dir = file_publisher.output_dir
        html_files = list(output_dir.glob("*.html"))
        html_content = html_files[0].read_text(encoding='utf-8')
        
        # Check template variables are replaced
        assert sample_article.title in html_content
        assert sample_article.meta_description in html_content
        assert ', '.join(sample_article.keywords) in html_content
        assert str(sample_article.word_count) in html_content
        assert sample_article.created_at.strftime("%B %d, %Y") in html_content
        
        # Check CSS is included
        assert "font-family" in html_content
        assert "color: #2c3e50" in html_content
        assert "max-width: 800px" in html_content
