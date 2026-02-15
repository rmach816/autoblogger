#!/usr/bin/env python3
"""
Quick setup test for AutoBlogger.

This script tests the basic functionality without requiring
API keys or external dependencies.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        from src.models import Article, BlogConfig, AppConfig
        print("✅ Models imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import models: {e}")
        return False
    
    try:
        from src.content_generator import MockAIProvider, ContentGenerator
        print("✅ Content generator imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import content generator: {e}")
        return False
    
    try:
        from src.publishers.file_publisher import FilePublisher
        print("✅ File publisher imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import file publisher: {e}")
        return False
    
    try:
        from src.utils import setup_logging, load_config
        print("✅ Utils imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import utils: {e}")
        return False
    
    return True

def test_mock_ai_provider():
    """Test mock AI provider functionality."""
    print("\nTesting mock AI provider...")
    
    try:
        from src.content_generator import MockAIProvider
        import asyncio
        
        async def test_generation():
            provider = MockAIProvider()
            content = await provider.generate_content("Write about sustainable gardening")
            
            assert content is not None
            assert len(content) > 100
            assert "gardening" in content.lower()
            
            print("✅ Mock AI provider working correctly")
            return True
        
        return asyncio.run(test_generation())
        
    except Exception as e:
        print(f"❌ Mock AI provider test failed: {e}")
        return False

def test_content_generator():
    """Test content generator with mock provider."""
    print("\nTesting content generator...")
    
    try:
        from src.content_generator import MockAIProvider, ContentGenerator
        from src.models import BlogConfig
        import asyncio
        
        async def test_generation():
            # Create test blog config
            blog = BlogConfig(
                id="test_blog",
                niche="sustainable gardening",
                target_audience="urban gardeners",
                tone="friendly",
                keywords=["eco-friendly", "organic"],
                word_count=1000,
                publish_to="file"
            )
            
            # Create generator
            ai_provider = MockAIProvider()
            generator = ContentGenerator(ai_provider)
            
            # Generate article
            article = await generator.generate_article(blog)
            
            assert article is not None
            assert article.title is not None
            assert article.content is not None
            assert article.blog_id == blog.id
            
            print("✅ Content generator working correctly")
            print(f"   Generated article: {article.title}")
            print(f"   Word count: {article.word_count}")
            return True
        
        return asyncio.run(test_generation())
        
    except Exception as e:
        print(f"❌ Content generator test failed: {e}")
        return False

def test_file_publisher():
    """Test file publisher functionality."""
    print("\nTesting file publisher...")
    
    try:
        from src.publishers.file_publisher import FilePublisher
        from src.models import Article
        from datetime import datetime
        import tempfile
        import asyncio
        
        async def test_publishing():
            # Create test article
            article = Article(
                id="test_article",
                title="Test Article",
                content="# Test Article\n\nThis is a test article.",
                meta_description="Test meta description",
                keywords=["test"],
                word_count=10,
                blog_id="test_blog",
                created_at=datetime.now()
            )
            
            # Create publisher with temp directory
            with tempfile.TemporaryDirectory() as temp_dir:
                publisher = FilePublisher(output_dir=temp_dir)
                
                # Publish article
                response = await publisher.publish(article)
                
                assert response.success is True
                assert response.url is not None
                
                # Check files were created
                output_path = Path(temp_dir)
                html_files = list(output_path.glob("*.html"))
                md_files = list(output_path.glob("*.md"))
                
                assert len(html_files) == 1
                assert len(md_files) == 1
                
                print("✅ File publisher working correctly")
                print(f"   Created files: {len(html_files)} HTML, {len(md_files)} Markdown")
                return True
        
        return asyncio.run(test_publishing())
        
    except Exception as e:
        print(f"❌ File publisher test failed: {e}")
        return False

def test_configuration():
    """Test configuration loading."""
    print("\nTesting configuration...")
    
    try:
        from src.utils import load_config
        from src.models import AppConfig
        
        # Test with example config
        config_path = "config/settings.example.json"
        if Path(config_path).exists():
            config = load_config(config_path)
            assert config is not None
            assert len(config.blogs) > 0
            print("✅ Configuration loading working correctly")
            print(f"   Found {len(config.blogs)} blog(s) configured")
            return True
        else:
            print("⚠️  Example configuration not found, skipping test")
            return True
            
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("AutoBlogger Setup Test")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_mock_ai_provider,
        test_content_generator,
        test_file_publisher,
        test_configuration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! AutoBlogger is ready to use.")
        print("\nNext steps:")
        print("1. Get API keys (see docs/SETUP.md)")
        print("2. Create .env file with your keys")
        print("3. Run: python main.py --generate-now")
    else:
        print("❌ Some tests failed. Check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
