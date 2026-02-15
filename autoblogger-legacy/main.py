#!/usr/bin/env python3
"""
AutoBlogger - AI-powered blog automation tool.

Main entry point for the AutoBlogger application.
Provides CLI interface for generating and publishing articles.
"""

import asyncio
import argparse
import sys
from pathlib import Path
from typing import Optional

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.models import AppConfig, BlogConfig
from src.utils import setup_logging, load_config, validate_environment, get_logger
from src.content_generator import ContentGenerator, create_ai_provider
from src.publishers.file_publisher import FilePublisher
from src.utils.retry import get_rate_limiter

logger = get_logger(__name__)


class AutoBlogger:
    """Main AutoBlogger application class."""
    
    def __init__(self, config_path: str = "config/settings.json"):
        """
        Initialize AutoBlogger.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path
        self.config: Optional[AppConfig] = None
        self.content_generator: Optional[ContentGenerator] = None
        self.publishers = {}
    
    async def initialize(self) -> None:
        """Initialize the application."""
        try:
            # Load configuration
            self.config = load_config(self.config_path)
            logger.info("Configuration loaded successfully")
            
            # Set up logging
            setup_logging(
                level=self.config.log_level,
                environment=self.config.environment,
                log_file="logs/autoblogger.log"
            )
            
            # Validate environment
            validate_environment(self.config)
            
            # Initialize AI provider
            ai_provider = create_ai_provider(self.config.ai_provider)
            self.content_generator = ContentGenerator(ai_provider)
            
            # Initialize publishers
            self._initialize_publishers()
            
            logger.info("AutoBlogger initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize AutoBlogger: {e}")
            raise
    
    def _initialize_publishers(self) -> None:
        """Initialize publishers based on configuration."""
        # File publisher (always available)
        self.publishers["file"] = FilePublisher()
        
        # Add other publishers as needed
        # TODO: Add Wix, WordPress, Medium publishers
    
    async def generate_article(self, blog_id: Optional[str] = None) -> None:
        """
        Generate a single article.
        
        Args:
            blog_id: Specific blog ID to generate for (None for all blogs)
        """
        if not self.config:
            raise RuntimeError("AutoBlogger not initialized")
        
        blogs_to_process = []
        
        if blog_id:
            # Find specific blog
            blog = next((b for b in self.config.blogs if b.id == blog_id), None)
            if not blog:
                raise ValueError(f"Blog not found: {blog_id}")
            blogs_to_process = [blog]
        else:
            # Process all blogs
            blogs_to_process = self.config.blogs
        
        if not blogs_to_process:
            logger.warning("No blogs configured")
            return
        
        for blog in blogs_to_process:
            try:
                logger.info(f"Generating article for blog: {blog.id}")
                
                # Generate article
                article = await self.content_generator.generate_article(blog)
                
                # Publish article
                publisher_name = blog.publish_to
                if publisher_name not in self.publishers:
                    logger.error(f"Publisher not available: {publisher_name}")
                    continue
                
                publisher = self.publishers[publisher_name]
                response = await publisher.publish(article)
                
                if response.success:
                    logger.info(f"Article published successfully: {response.url}")
                else:
                    logger.error(f"Failed to publish article: {response.message}")
                
            except Exception as e:
                logger.error(f"Failed to process blog {blog.id}: {e}")
    
    async def generate_all_articles(self) -> None:
        """Generate articles for all configured blogs."""
        await self.generate_article()
    
    def list_blogs(self) -> None:
        """List all configured blogs."""
        if not self.config:
            print("AutoBlogger not initialized")
            return
        
        if not self.config.blogs:
            print("No blogs configured")
            return
        
        print("Configured Blogs:")
        print("-" * 50)
        for blog in self.config.blogs:
            print(f"ID: {blog.id}")
            print(f"Niche: {blog.niche}")
            print(f"Audience: {blog.target_audience}")
            print(f"Posts per week: {blog.posts_per_week}")
            print(f"Publisher: {blog.publish_to}")
            print("-" * 50)


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="AutoBlogger - AI-powered blog automation")
    parser.add_argument("--config", default="config/settings.json", help="Configuration file path")
    parser.add_argument("--generate-now", action="store_true", help="Generate article immediately")
    parser.add_argument("--blog", help="Generate for specific blog ID")
    parser.add_argument("--list-blogs", action="store_true", help="List configured blogs")
    parser.add_argument("--dry-run", action="store_true", help="Preview without publishing")
    
    args = parser.parse_args()
    
    try:
        # Initialize AutoBlogger
        app = AutoBlogger(args.config)
        await app.initialize()
        
        if args.list_blogs:
            app.list_blogs()
        elif args.generate_now:
            if args.dry_run:
                logger.info("Dry run mode - articles will be generated but not published")
                logger.warning("Dry run mode not yet fully implemented - articles will be generated to file")
            await app.generate_article(args.blog)
        else:
            print("AutoBlogger initialized successfully!")
            print("Use --help to see available commands")
            print("Use --generate-now to generate an article")
            print("Use --list-blogs to see configured blogs")
    
    except Exception as e:
        logger.error(f"AutoBlogger failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
