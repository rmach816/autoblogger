"""
Image handler for AutoBlogger.

Handles image sourcing from Unsplash, custom uploads, and AI-generated images.
"""

import asyncio
import httpx
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any
from urllib.parse import quote

from models import ImageSuggestion, ImageError
from utils.logger import get_logger
from utils.retry import retry

logger = get_logger(__name__)


class ImageHandler:
    """Handles image sourcing and management."""
    
    def __init__(self, unsplash_access_key: Optional[str] = None):
        """
        Initialize image handler.
        
        Args:
            unsplash_access_key: Unsplash API access key
        """
        self.unsplash_key = unsplash_access_key
        self.logger = get_logger("image_handler")
        self.output_dir = Path("output/images")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    async def get_image_suggestions(self, topic: str, style: str = "professional", count: int = 3) -> List[ImageSuggestion]:
        """
        Get image suggestions for an article topic.
        
        Args:
            topic: Article topic
            style: Image style (professional, lifestyle, technical)
            count: Number of suggestions to return
            
        Returns:
            List of image suggestions
        """
        try:
            if self.unsplash_key:
                return await self._get_unsplash_suggestions(topic, style, count)
            else:
                return self._get_mock_suggestions(topic, style, count)
                
        except Exception as e:
            self.logger.error(f"Failed to get image suggestions: {e}")
            return self._get_mock_suggestions(topic, style, count)
    
    async def _get_unsplash_suggestions(self, topic: str, style: str, count: int) -> List[ImageSuggestion]:
        """Get image suggestions from Unsplash API."""
        try:
            async with httpx.AsyncClient() as client:
                # Search for images
                search_query = f"{topic} {style}"
                url = f"https://api.unsplash.com/search/photos"
                
                headers = {
                    "Authorization": f"Client-ID {self.unsplash_key}",
                    "Accept-Version": "v1"
                }
                
                params = {
                    "query": search_query,
                    "per_page": count,
                    "orientation": "landscape"
                }
                
                response = await client.get(url, headers=headers, params=params)
                response.raise_for_status()
                
                data = response.json()
                suggestions = []
                
                for photo in data.get("results", [])[:count]:
                    suggestion = ImageSuggestion(
                        id=str(uuid.uuid4()),
                        title=photo.get("alt_description", f"{topic} image"),
                        description=photo.get("description", ""),
                        url=photo["urls"]["regular"],
                        thumbnail_url=photo["urls"]["thumb"],
                        photographer=photo["user"]["name"],
                        photographer_url=photo["user"]["links"]["html"],
                        download_url=photo["links"]["download"],
                        width=photo["width"],
                        height=photo["height"],
                        created_at=datetime.now()
                    )
                    suggestions.append(suggestion)
                
                self.logger.info(f"Retrieved {len(suggestions)} image suggestions from Unsplash")
                return suggestions
                
        except Exception as e:
            self.logger.error(f"Unsplash API error: {e}")
            return self._get_mock_suggestions(topic, style, count)
    
    def _get_mock_suggestions(self, topic: str, style: str, count: int) -> List[ImageSuggestion]:
        """Get mock image suggestions for testing."""
        suggestions = []
        
        # Generate mock suggestions based on topic and style
        mock_images = {
            "professional": [
                "Modern office technology setup",
                "Professional networking equipment",
                "Clean, modern smart home interface",
                "Business technology solutions",
                "Professional security system"
            ],
            "lifestyle": [
                "Family using smart home features",
                "Homeowner controlling lights with app",
                "Professional working from smart home office",
                "Family enjoying home theater",
                "Peaceful evening with automated lighting"
            ],
            "technical": [
                "Network infrastructure diagram",
                "Smart home system architecture",
                "Security system components",
                "Audio/visual equipment setup",
                "Lighting control wiring diagram"
            ]
        }
        
        image_titles = mock_images.get(style, mock_images["professional"])
        
        for i in range(min(count, len(image_titles))):
            suggestion = ImageSuggestion(
                id=str(uuid.uuid4()),
                title=image_titles[i],
                description=f"Professional {style} image related to {topic}",
                url=f"https://via.placeholder.com/800x600/007bff/ffffff?text={quote(image_titles[i])}",
                thumbnail_url=f"https://via.placeholder.com/300x200/007bff/ffffff?text={quote(image_titles[i])}",
                photographer="Mock Photographer",
                photographer_url="https://example.com",
                download_url=f"https://via.placeholder.com/800x600/007bff/ffffff?text={quote(image_titles[i])}",
                width=800,
                height=600,
                created_at=datetime.now()
            )
            suggestions.append(suggestion)
        
        self.logger.info(f"Generated {len(suggestions)} mock image suggestions")
        return suggestions
    
    async def download_image(self, suggestion: ImageSuggestion) -> Optional[Path]:
        """
        Download an image to local storage.
        
        Args:
            suggestion: Image suggestion to download
            
        Returns:
            Path to downloaded image file
        """
        try:
            # Create filename
            filename = f"{suggestion.id}_{suggestion.title.replace(' ', '_')}.jpg"
            filepath = self.output_dir / filename
            
            # Download image
            async with httpx.AsyncClient() as client:
                response = await client.get(suggestion.download_url)
                response.raise_for_status()
                
                # Save to file
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                self.logger.info(f"Downloaded image: {filepath}")
                return filepath
                
        except Exception as e:
            self.logger.error(f"Failed to download image: {e}")
            return None
    
    def get_image_embed_code(self, suggestion: ImageSuggestion, width: int = 800, height: int = 600) -> str:
        """
        Generate HTML embed code for an image.
        
        Args:
            suggestion: Image suggestion
            width: Image width
            height: Image height
            
        Returns:
            HTML embed code
        """
        return f"""
        <figure class="article-image">
            <img src="{suggestion.url}" 
                 alt="{suggestion.title}" 
                 width="{width}" 
                 height="{height}"
                 style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
            <figcaption style="text-align: center; font-style: italic; color: #666; margin-top: 8px;">
                {suggestion.title}
                <br>
                <small>Photo by <a href="{suggestion.photographer_url}" target="_blank">{suggestion.photographer}</a> on Unsplash</small>
            </figcaption>
        </figure>
        """
    
    def add_images_to_content(self, content: str, suggestions: List[ImageSuggestion]) -> str:
        """
        Add image embed codes to article content.
        
        Args:
            content: Article content
            suggestions: Image suggestions
            
        Returns:
            Content with embedded images
        """
        if not suggestions:
            return content
        
        # Find good places to insert images
        paragraphs = content.split('\n\n')
        enhanced_content = []
        
        for i, paragraph in enumerate(paragraphs):
            enhanced_content.append(paragraph)
            
            # Insert image after every 2-3 paragraphs
            if i > 0 and i % 2 == 0 and i // 2 - 1 < len(suggestions):
                suggestion = suggestions[i // 2 - 1]
                image_code = self.get_image_embed_code(suggestion)
                enhanced_content.append(image_code)
        
        return '\n\n'.join(enhanced_content)
    
    async def generate_ai_image_suggestions(self, topic: str, style: str) -> List[ImageSuggestion]:
        """
        Generate AI-powered image suggestions.
        
        Args:
            topic: Article topic
            style: Image style
            
        Returns:
            List of AI-generated image suggestions
        """
        # This would integrate with AI image generation services
        # For now, return enhanced mock suggestions
        suggestions = self._get_mock_suggestions(topic, style, 3)
        
        # Enhance with AI-generated descriptions
        for suggestion in suggestions:
            suggestion.description = f"AI-generated {style} image perfect for {topic} content. High-quality, professional image that enhances the article's visual appeal and engagement."
        
        return suggestions


def create_image_handler(unsplash_key: Optional[str] = None) -> ImageHandler:
    """
    Create image handler instance.
    
    Args:
        unsplash_key: Unsplash API key
        
    Returns:
        Image handler instance
    """
    return ImageHandler(unsplash_key)
