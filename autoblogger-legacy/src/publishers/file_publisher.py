"""
File publisher for AutoBlogger.

Saves articles as HTML and Markdown files to the output directory.
This is the default publisher for testing and manual publishing.
"""

import os
from pathlib import Path
from datetime import datetime
from typing import Optional

from publishers.base_publisher import BasePublisher
from models import Article, PublishResponse, PublisherError
from utils.logger import LogContext


class FilePublisher(BasePublisher):
    """Publisher that saves articles to files."""
    
    def __init__(self, output_dir: str = "output"):
        """
        Initialize file publisher.
        
        Args:
            output_dir: Directory to save files
        """
        super().__init__("file")
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    async def publish(self, article: Article) -> PublishResponse:
        """
        Save article as HTML and Markdown files.
        
        Args:
            article: Article to save
            
        Returns:
            PublishResponse with file paths
        """
        with LogContext(self.logger, "file_publish", 
                       article_id=article.id, blog_id=article.blog_id):
            
            try:
                # Generate safe filename
                safe_title = self._sanitize_filename(article.title)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                base_filename = f"{timestamp}_{safe_title}"
                
                # Save HTML file
                html_path = self.output_dir / f"{base_filename}.html"
                html_content = self._generate_html(article)
                html_path.write_text(html_content, encoding='utf-8')
                
                # Save Markdown file
                md_path = self.output_dir / f"{base_filename}.md"
                md_content = self._generate_markdown(article)
                md_path.write_text(md_content, encoding='utf-8')
                
                # Create response
                response = PublishResponse(
                    success=True,
                    url=f"file://{html_path.absolute()}",
                    message=f"Article saved as {html_path.name} and {md_path.name}",
                    published_at=datetime.now()
                )
                
                self._log_publish_success(article, response)
                return response
                
            except Exception as e:
                self._log_publish_error(article, e)
                return PublishResponse(
                    success=False,
                    message=f"Failed to save article: {e}"
                )
    
    async def validate_credentials(self) -> bool:
        """
        Validate that output directory is writable.
        
        Returns:
            True if directory is writable
        """
        try:
            # Test write access
            test_file = self.output_dir / ".test_write"
            test_file.write_text("test")
            test_file.unlink()
            return True
        except Exception as e:
            self.logger.error(f"Output directory not writable: {e}")
            return False
    
    async def preview(self, article: Article) -> str:
        """
        Generate HTML preview of the article.
        
        Args:
            article: Article to preview
            
        Returns:
            HTML preview string
        """
        return self._generate_html(article)
    
    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for filesystem safety."""
        # Remove or replace invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        # Limit length
        if len(filename) > 100:
            filename = filename[:100]
        
        return filename.strip()
    
    def _generate_html(self, article: Article) -> str:
        """Generate HTML content for the article."""
        html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{meta_description}">
    <meta name="keywords" content="{keywords}">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }}
        .meta {{
            color: #7f8c8d;
            font-size: 0.9em;
            margin-bottom: 30px;
        }}
        .content {{
            line-height: 1.8;
        }}
        .content h2 {{
            color: #34495e;
            margin-top: 30px;
        }}
        .content h3 {{
            color: #34495e;
            margin-top: 25px;
        }}
        .content p {{
            margin-bottom: 15px;
        }}
        .content ul, .content ol {{
            margin-bottom: 15px;
        }}
        .content li {{
            margin-bottom: 5px;
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <div class="meta">
        <p><strong>Published:</strong> {published_at}</p>
        <p><strong>Word Count:</strong> {word_count}</p>
        <p><strong>Keywords:</strong> {keywords}</p>
    </div>
    <div class="content">
        {content}
    </div>
</body>
</html>"""
        
        return html_template.format(
            title=article.title,
            meta_description=article.meta_description,
            keywords=", ".join(article.keywords),
            published_at=article.created_at.strftime("%B %d, %Y"),
            word_count=article.word_count,
            content=article.content
        )
    
    def _generate_markdown(self, article: Article) -> str:
        """Generate Markdown content for the article."""
        md_template = """# {title}

**Published:** {published_at}  
**Word Count:** {word_count}  
**Keywords:** {keywords}

---

{content}
"""
        
        return md_template.format(
            title=article.title,
            published_at=article.created_at.strftime("%B %d, %Y"),
            word_count=article.word_count,
            keywords=", ".join(article.keywords),
            content=article.content
        )
