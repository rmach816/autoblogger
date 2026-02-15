"""
SEO optimization for AutoBlogger.

Handles meta descriptions, schema markup, keyword density analysis,
and other SEO enhancements for generated articles.
"""

import re
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass

from models import Article
from utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class SEOAnalysis:
    """SEO analysis results for an article."""
    keyword_density: Dict[str, float]
    meta_description_length: int
    title_length: int
    heading_structure: Dict[str, int]
    internal_links: int
    external_links: int
    readability_score: float
    seo_score: int
    recommendations: List[str]


class SEOOptimizer:
    """Handles SEO optimization for articles."""
    
    def __init__(self):
        """Initialize SEO optimizer."""
        self.logger = get_logger("seo_optimizer")
    
    def analyze_article(self, article: Article) -> SEOAnalysis:
        """
        Analyze article for SEO optimization.
        
        Args:
            article: Article to analyze
            
        Returns:
            SEO analysis results
        """
        try:
            # Calculate keyword density
            keyword_density = self._calculate_keyword_density(article.content, article.keywords)
            
            # Analyze meta description
            meta_description_length = len(article.meta_description)
            
            # Analyze title
            title_length = len(article.title)
            
            # Analyze heading structure
            heading_structure = self._analyze_headings(article.content)
            
            # Count links
            internal_links, external_links = self._count_links(article.content)
            
            # Calculate readability score
            readability_score = self._calculate_readability(article.content)
            
            # Calculate overall SEO score
            seo_score = self._calculate_seo_score(
                keyword_density, meta_description_length, title_length,
                heading_structure, readability_score
            )
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                keyword_density, meta_description_length, title_length,
                heading_structure, readability_score, seo_score
            )
            
            return SEOAnalysis(
                keyword_density=keyword_density,
                meta_description_length=meta_description_length,
                title_length=title_length,
                heading_structure=heading_structure,
                internal_links=internal_links,
                external_links=external_links,
                readability_score=readability_score,
                seo_score=seo_score,
                recommendations=recommendations
            )
            
        except Exception as e:
            self.logger.error(f"Failed to analyze article SEO: {e}")
            return SEOAnalysis(
                keyword_density={},
                meta_description_length=0,
                title_length=0,
                heading_structure={},
                internal_links=0,
                external_links=0,
                readability_score=0.0,
                seo_score=0,
                recommendations=["Analysis failed"]
            )
    
    def _calculate_keyword_density(self, content: str, keywords: List[str]) -> Dict[str, float]:
        """Calculate keyword density for each keyword."""
        # Clean content (remove markdown, HTML, etc.)
        clean_content = re.sub(r'[#*`\[\]()]', '', content.lower())
        words = clean_content.split()
        total_words = len(words)
        
        density = {}
        for keyword in keywords:
            keyword_lower = keyword.lower()
            keyword_count = clean_content.count(keyword_lower)
            density[keyword] = (keyword_count / total_words) * 100 if total_words > 0 else 0
        
        return density
    
    def _analyze_headings(self, content: str) -> Dict[str, int]:
        """Analyze heading structure."""
        headings = {
            'h1': len(re.findall(r'^# ', content, re.MULTILINE)),
            'h2': len(re.findall(r'^## ', content, re.MULTILINE)),
            'h3': len(re.findall(r'^### ', content, re.MULTILINE)),
            'h4': len(re.findall(r'^#### ', content, re.MULTILINE)),
            'h5': len(re.findall(r'^##### ', content, re.MULTILINE)),
            'h6': len(re.findall(r'^###### ', content, re.MULTILINE))
        }
        return headings
    
    def _count_links(self, content: str) -> Tuple[int, int]:
        """Count internal and external links."""
        # Find all markdown links
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        links = re.findall(link_pattern, content)
        
        internal_links = 0
        external_links = 0
        
        for _, url in links:
            if url.startswith(('http://', 'https://')):
                external_links += 1
            elif url.startswith('/') or not url.startswith(('mailto:', 'tel:')):
                internal_links += 1
        
        return internal_links, external_links
    
    def _calculate_readability(self, content: str) -> float:
        """Calculate readability score (simplified Flesch Reading Ease)."""
        # Remove markdown formatting
        clean_content = re.sub(r'[#*`\[\]()]', '', content)
        
        # Count sentences
        sentences = re.split(r'[.!?]+', clean_content)
        sentence_count = len([s for s in sentences if s.strip()])
        
        # Count words
        words = clean_content.split()
        word_count = len(words)
        
        # Count syllables (simplified)
        syllable_count = sum(self._count_syllables(word) for word in words)
        
        if sentence_count == 0 or word_count == 0:
            return 0.0
        
        # Flesch Reading Ease formula
        score = 206.835 - (1.015 * (word_count / sentence_count)) - (84.6 * (syllable_count / word_count))
        
        return max(0, min(100, score))
    
    def _count_syllables(self, word: str) -> int:
        """Count syllables in a word (simplified)."""
        word = word.lower()
        vowels = 'aeiouy'
        syllable_count = 0
        prev_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not prev_was_vowel:
                syllable_count += 1
            prev_was_vowel = is_vowel
        
        # Handle silent 'e'
        if word.endswith('e') and syllable_count > 1:
            syllable_count -= 1
        
        return max(1, syllable_count)
    
    def _calculate_seo_score(self, keyword_density: Dict[str, float], 
                           meta_length: int, title_length: int,
                           heading_structure: Dict[str, int], 
                           readability: float) -> int:
        """Calculate overall SEO score (0-100)."""
        score = 0
        
        # Keyword density (30 points)
        if keyword_density:
            avg_density = sum(keyword_density.values()) / len(keyword_density)
            if 1.0 <= avg_density <= 3.0:  # Optimal range
                score += 30
            elif 0.5 <= avg_density <= 5.0:  # Acceptable range
                score += 20
            else:
                score += 10
        
        # Meta description (20 points)
        if 120 <= meta_length <= 160:  # Optimal length
            score += 20
        elif 100 <= meta_length <= 180:  # Acceptable length
            score += 15
        else:
            score += 5
        
        # Title length (15 points)
        if 30 <= title_length <= 60:  # Optimal length
            score += 15
        elif 20 <= title_length <= 70:  # Acceptable length
            score += 10
        else:
            score += 5
        
        # Heading structure (20 points)
        if heading_structure.get('h1', 0) == 1:  # Should have exactly one H1
            score += 10
        if heading_structure.get('h2', 0) >= 2:  # Should have multiple H2s
            score += 10
        
        # Readability (15 points)
        if readability >= 60:  # Good readability
            score += 15
        elif readability >= 40:  # Fair readability
            score += 10
        else:
            score += 5
        
        return min(100, score)
    
    def _generate_recommendations(self, keyword_density: Dict[str, float],
                                meta_length: int, title_length: int,
                                heading_structure: Dict[str, int],
                                readability: float, seo_score: int) -> List[str]:
        """Generate SEO recommendations."""
        recommendations = []
        
        # Keyword density recommendations
        if keyword_density:
            avg_density = sum(keyword_density.values()) / len(keyword_density)
            if avg_density < 1.0:
                recommendations.append("Increase keyword density - aim for 1-3%")
            elif avg_density > 3.0:
                recommendations.append("Reduce keyword density - aim for 1-3%")
        
        # Meta description recommendations
        if meta_length < 120:
            recommendations.append("Meta description too short - aim for 120-160 characters")
        elif meta_length > 160:
            recommendations.append("Meta description too long - aim for 120-160 characters")
        
        # Title recommendations
        if title_length < 30:
            recommendations.append("Title too short - aim for 30-60 characters")
        elif title_length > 60:
            recommendations.append("Title too long - aim for 30-60 characters")
        
        # Heading recommendations
        if heading_structure.get('h1', 0) != 1:
            recommendations.append("Use exactly one H1 heading")
        if heading_structure.get('h2', 0) < 2:
            recommendations.append("Add more H2 headings for better structure")
        
        # Readability recommendations
        if readability < 40:
            recommendations.append("Improve readability - use shorter sentences and simpler words")
        elif readability > 80:
            recommendations.append("Consider adding more technical details for your audience")
        
        # Overall score recommendations
        if seo_score < 60:
            recommendations.append("Overall SEO score is low - review all recommendations")
        elif seo_score >= 80:
            recommendations.append("Excellent SEO optimization!")
        
        return recommendations
    
    def optimize_article(self, article: Article) -> Article:
        """
        Optimize article for SEO.
        
        Args:
            article: Article to optimize
            
        Returns:
            Optimized article
        """
        try:
            # Optimize meta description
            if len(article.meta_description) < 120:
                article.meta_description = self._enhance_meta_description(article)
            
            # Optimize title
            if len(article.title) < 30 or len(article.title) > 60:
                article.title = self._optimize_title(article)
            
            # Add schema markup
            article.content = self._add_schema_markup(article)
            
            # Optimize keyword usage
            article.content = self._optimize_keywords(article)
            
            self.logger.info(f"Optimized article: {article.title}")
            return article
            
        except Exception as e:
            self.logger.error(f"Failed to optimize article: {e}")
            return article
    
    def _enhance_meta_description(self, article: Article) -> str:
        """Enhance meta description if too short."""
        if len(article.meta_description) >= 120:
            return article.meta_description
        
        # Extract first paragraph and enhance
        paragraphs = article.content.split('\n\n')
        if paragraphs:
            first_para = paragraphs[0].strip()
            # Remove markdown formatting
            first_para = re.sub(r'[#*`\[\]()]', '', first_para)
            
            # Add call to action
            enhanced = f"{first_para} Learn more about {article.keywords[0] if article.keywords else 'technology solutions'} with Executive Technology Group."
            
            # Truncate to optimal length
            if len(enhanced) > 160:
                enhanced = enhanced[:157] + "..."
            
            return enhanced
        
        return article.meta_description
    
    def _optimize_title(self, article: Article) -> str:
        """Optimize title length and keywords."""
        title = article.title
        
        # If too short, add keywords
        if len(title) < 30 and article.keywords:
            keyword = article.keywords[0]
            if keyword.lower() not in title.lower():
                title = f"{title}: {keyword.title()}"
        
        # If too long, truncate intelligently
        if len(title) > 60:
            # Try to cut at a natural break
            words = title.split()
            truncated = []
            current_length = 0
            
            for word in words:
                if current_length + len(word) + 1 <= 60:
                    truncated.append(word)
                    current_length += len(word) + 1
                else:
                    break
            
            title = ' '.join(truncated)
            if not title.endswith(('.', '!', '?')):
                title += '...'
        
        return title
    
    def _add_schema_markup(self, article: Article) -> str:
        """Add schema markup to article content."""
        schema = f"""
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{article.title}",
  "description": "{article.meta_description}",
  "author": {{
    "@type": "Organization",
    "name": "Executive Technology Group",
    "url": "https://www.executivetechnologygroup.com/"
  }},
  "publisher": {{
    "@type": "Organization",
    "name": "Executive Technology Group",
    "logo": {{
      "@type": "ImageObject",
      "url": "https://www.executivetechnologygroup.com/logo.png"
    }}
  }},
  "datePublished": "{article.created_at.isoformat()}",
  "dateModified": "{article.created_at.isoformat()}",
  "mainEntityOfPage": {{
    "@type": "WebPage",
    "@id": "https://www.executivetechnologygroup.com/blog/{article.id}"
  }},
  "keywords": "{', '.join(article.keywords)}"
}}
</script>
"""
        return schema + article.content
    
    def _optimize_keywords(self, article: Article) -> str:
        """Optimize keyword usage in content."""
        content = article.content
        
        # Ensure primary keyword appears in first paragraph
        if article.keywords:
            primary_keyword = article.keywords[0]
            first_para = content.split('\n\n')[0]
            
            if primary_keyword.lower() not in first_para.lower():
                # Add keyword naturally to first paragraph
                first_para = f"{first_para} {primary_keyword.title()} solutions"
                content = content.replace(content.split('\n\n')[0], first_para)
        
        return content


def create_seo_optimizer() -> SEOOptimizer:
    """Create SEO optimizer instance."""
    return SEOOptimizer()
