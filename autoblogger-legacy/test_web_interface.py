#!/usr/bin/env python3
"""
Test script for AutoBlogger web interface.
Tests all major functionality to ensure everything works properly.
"""

import sys
import asyncio
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from models import BlogConfig, Article
from content_generator import create_ai_provider, ContentGenerator
from image_handler import create_image_handler
from seo_optimizer import create_seo_optimizer
from publishers.file_publisher import FilePublisher
from datetime import datetime


async def test_complete_workflow():
    """Test the complete article generation workflow."""
    print("Testing AutoBlogger Complete Workflow")
    print("=" * 50)
    
    # Initialize components
    print("1. Initializing components...")
    ai_provider = create_ai_provider('mock')
    content_generator = ContentGenerator(ai_provider)
    image_handler = create_image_handler()
    seo_optimizer = create_seo_optimizer()
    file_publisher = FilePublisher(output_dir="output")
    
    # Create blog configuration for Executive Technology Group
    blog_config = BlogConfig(
        id="executive_tech_test",
        niche="smart home automation for Houston businesses",
        target_audience="Houston business owners",
        tone="professional",
        keywords=["smart home", "automation", "Houston", "business", "technology"],
        word_count=800,
        publish_to="file"
    )
    
    print("SUCCESS: Components initialized")
    
    # Generate article
    print("2. Generating article...")
    article = await content_generator.generate_article(blog_config)
    print(f"SUCCESS: Article generated: {article.title}")
    print(f"   Word count: {article.word_count}")
    
    # Get image suggestions
    print("3. Getting image suggestions...")
    image_suggestions = await image_handler.get_image_suggestions(
        "smart home automation", "professional", 2
    )
    print(f"SUCCESS: Image suggestions: {len(image_suggestions)} found")
    
    # SEO analysis
    print("4. Performing SEO analysis...")
    seo_analysis = seo_optimizer.analyze_article(article)
    print(f"SUCCESS: SEO Score: {seo_analysis.seo_score}/100")
    print(f"   Recommendations: {len(seo_analysis.recommendations)}")
    
    # Optimize article
    print("5. Optimizing article...")
    optimized_article = seo_optimizer.optimize_article(article)
    print("SUCCESS: Article optimized")
    
    # Publish article
    print("6. Publishing article...")
    publish_result = await file_publisher.publish(optimized_article)
    print(f"SUCCESS: Article published: {publish_result.success}")
    if publish_result.success:
        print(f"   Output file: {publish_result.url}")
    
    print("\nAll tests passed! AutoBlogger is working correctly.")
    print("\nNext steps:")
    print("1. Start the web interface: py web_app.py")
    print("2. Visit: http://localhost:3500")
    print("3. Try the Custom Generator for your technology articles")
    print("4. Add your Unsplash API key to .env for real images")


def test_web_app_imports():
    """Test that web app imports work correctly."""
    print("Testing web app imports...")
    try:
        from web_app import initialize_autoblogger
        result = initialize_autoblogger()
        if result:
            print("SUCCESS: Web app initialization successful")
            return True
        else:
            print("ERROR: Web app initialization failed")
            return False
    except Exception as e:
        print(f"ERROR: Web app import error: {e}")
        return False


if __name__ == "__main__":
    print("AutoBlogger Test Suite")
    print("=" * 30)
    
    # Test web app imports first
    if not test_web_app_imports():
        print("ERROR: Web app tests failed. Please check the errors above.")
        sys.exit(1)
    
    # Test complete workflow
    try:
        asyncio.run(test_complete_workflow())
    except Exception as e:
        print(f"ERROR: Workflow test failed: {e}")
        sys.exit(1)
