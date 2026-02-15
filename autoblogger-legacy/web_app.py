#!/usr/bin/env python3
"""
AutoBlogger Web Interface

Simple web dashboard for managing and generating blog articles.
Runs on port 3500 for easy access.
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed. Environment variables may not load properly.")

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

# Import AutoBlogger components
from src.models import BlogConfig, AppConfig, Article
from src.utils.config_loader import load_config, load_environment_variables
from src.utils.logger import setup_logging, get_logger
from src.content_generator import ContentGenerator, create_ai_provider
from src.publishers.file_publisher import FilePublisher
from src.image_handler import create_image_handler, ImageHandler
from src.seo_optimizer import create_seo_optimizer, SEOOptimizer
from src.security.auth import generate_secret_key
from src.security.rate_limiting import get_ip_rate_limiter, IPRateLimiter
from src.security.validators import sanitize_html, sanitize_filename as secure_sanitize_filename

# Initialize Flask app
app = Flask(__name__)

# Load environment variables
env_vars = load_environment_variables()

# Set secret key from environment or generate new one
app.secret_key = env_vars.get('AUTOBLOGGER_SECRET_KEY', generate_secret_key())

# Configure CORS
cors_origins = env_vars.get('CORS_ORIGINS', 'http://localhost:5001,http://127.0.0.1:5001')
CORS(app, resources={
    r"/api/*": {
        "origins": cors_origins.split(','),
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Initialize rate limiter
rate_limit_enabled = env_vars.get('RATE_LIMIT_ENABLED', 'true').lower() == 'true'
if rate_limit_enabled:
    ip_rate_limiter: Optional[IPRateLimiter] = get_ip_rate_limiter(requests_per_minute=60)
else:
    ip_rate_limiter = None

# Global variables
config: Optional[AppConfig] = None
content_generator: Optional[ContentGenerator] = None
file_publisher: Optional[FilePublisher] = None
image_handler: Optional[ImageHandler] = None
seo_optimizer: Optional[SEOOptimizer] = None
logger = get_logger(__name__)


# Security headers middleware
@app.after_request
def add_security_headers(response):
    """Add security headers to all responses."""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; font-src 'self' https://cdnjs.cloudflare.com"
    return response


# Rate limiting middleware
@app.before_request
def check_rate_limit():
    """Check rate limit before processing request."""
    if ip_rate_limiter and request.endpoint:
        # Skip rate limiting for static files
        if request.endpoint.startswith('static'):
            return None
        
        # Get client IP
        client_ip = request.remote_addr or 'unknown'
        
        # Check rate limit asynchronously
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            allowed = loop.run_until_complete(ip_rate_limiter.is_allowed(client_ip))
            if not allowed:
                return jsonify({
                    "error": "Rate limit exceeded",
                    "message": "Too many requests. Please try again later."
                }), 429
        finally:
            loop.close()
    
    return None


# Error handlers
@app.errorhandler(400)
def bad_request(error):
    """Handle bad request errors."""
    logger.warning(f"Bad request: {error}")
    return jsonify({"error": "Bad request", "message": str(error)}), 400


@app.errorhandler(404)
def not_found(error):
    """Handle not found errors."""
    return jsonify({"error": "Not found", "message": "The requested resource was not found"}), 404


@app.errorhandler(429)
def rate_limit_exceeded(error):
    """Handle rate limit errors."""
    return jsonify({"error": "Rate limit exceeded", "message": "Too many requests. Please try again later."}), 429


@app.errorhandler(500)
def internal_error(error):
    """Handle internal server errors."""
    logger.error(f"Internal server error: {error}")
    return jsonify({"error": "Internal server error", "message": "An unexpected error occurred"}), 500


def initialize_autoblogger():
    """Initialize AutoBlogger components."""
    global config, content_generator, file_publisher, image_handler, seo_optimizer
    
    try:
        # Load configuration
        config = load_config("config/settings.json")
        
        # Set up logging
        setup_logging(
            level=config.log_level,
            environment=config.environment,
            log_file="logs/autoblogger.log"
        )
        
        # Initialize AI provider (never log API keys!)
        api_key = os.getenv("OPENAI_API_KEY")
        logger.info(f"API key found: {bool(api_key)}")
        # SECURITY: Never log actual API key values
        ai_provider = create_ai_provider(config.ai_provider, api_key)
        content_generator = ContentGenerator(ai_provider)
        
        # Initialize file publisher
        file_publisher = FilePublisher(output_dir="output")
        
        # Initialize image handler
        unsplash_key = os.getenv("UNSPLASH_ACCESS_KEY")
        image_handler = create_image_handler(unsplash_key)
        
        # Initialize SEO optimizer
        seo_optimizer = create_seo_optimizer()
        
        logger.info("AutoBlogger web interface initialized")
        return True
        
    except Exception as e:
        logger.error(f"Failed to initialize AutoBlogger: {e}")
        return False


@app.route('/')
def index():
    """Main dashboard page."""
    if not config:
        flash("AutoBlogger not initialized. Please check configuration.", "error")
        return render_template('error.html', message="Configuration error")
    
    # Get recent articles
    recent_articles = get_recent_articles()
    
    return render_template('index.html', 
                         blogs=config.blogs,
                         recent_articles=recent_articles,
                         config=config)


@app.route('/health')
def health_check():
    """Health check endpoint for monitoring."""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "autoblogger",
        "version": "1.0.0"
    })

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory('static', filename)


@app.route('/generate', methods=['POST'])
def generate_article():
    """Generate a new article."""
    try:
        # Input validation
        blog_id = request.form.get('blog_id', '').strip()
        if not blog_id:
            flash("Please select a blog", "error")
            return redirect(url_for('index'))
        
        # Sanitize input
        blog_id = sanitize_html(blog_id)
        
        # Find the blog configuration
        blog = next((b for b in config.blogs if b.id == blog_id), None)
        if not blog:
            flash(f"Blog not found: {blog_id}", "error")
            return redirect(url_for('index'))
        
        # Generate article asynchronously
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            article = loop.run_until_complete(
                content_generator.generate_article(blog)
            )
            
            # Publish article
            response = loop.run_until_complete(
                file_publisher.publish(article)
            )
            
            if response.success:
                flash(f"Article generated successfully: {article.title}", "success")
                logger.info(f"Generated article: {article.title}")
            else:
                flash(f"Failed to publish article: {response.message}", "error")
                
        finally:
            loop.close()
        
        return redirect(url_for('index'))
        
    except Exception as e:
        logger.error(f"Failed to generate article: {e}")
        flash(f"Error generating article: {e}", "error")
        return redirect(url_for('index'))


@app.route('/articles')
def articles():
    """View all generated articles."""
    articles = get_recent_articles()
    return render_template('articles.html', articles=articles)


@app.route('/article/<article_id>')
def view_article(article_id):
    """View a specific article."""
    # Find article file
    output_dir = Path("output")
    html_files = list(output_dir.glob(f"*{article_id}*.html"))
    
    if not html_files:
        flash("Article not found", "error")
        return redirect(url_for('articles'))
    
    # Read HTML content
    html_content = html_files[0].read_text(encoding='utf-8')
    
    return render_template('view_article.html', 
                         content=html_content,
                         filename=html_files[0].name)


@app.route('/config')
def config_page():
    """Configuration management page."""
    return render_template('config.html', config=config)


@app.route('/api/blogs')
def api_blogs():
    """API endpoint for blog list."""
    if not config:
        return jsonify({"error": "Configuration not loaded"}), 500
    
    blogs_data = []
    for blog in config.blogs:
        blogs_data.append({
            "id": blog.id,
            "niche": blog.niche,
            "target_audience": blog.target_audience,
            "tone": blog.tone,
            "posts_per_week": blog.posts_per_week,
            "keywords": blog.keywords,
            "word_count": blog.word_count,
            "publish_to": blog.publish_to
        })
    
    return jsonify(blogs_data)


@app.route('/api/generate', methods=['POST'])
def api_generate():
    """API endpoint for article generation."""
    try:
        data = request.get_json()
        blog_id = data.get('blog_id')
        
        if not blog_id:
            return jsonify({"error": "blog_id required"}), 400
        
        # Find blog
        blog = next((b for b in config.blogs if b.id == blog_id), None)
        if not blog:
            return jsonify({"error": f"Blog not found: {blog_id}"}), 404
        
        # Generate article
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            article = loop.run_until_complete(
                content_generator.generate_article(blog)
            )
            
            response = loop.run_until_complete(
                file_publisher.publish(article)
            )
            
            return jsonify({
                "success": response.success,
                "article": {
                    "id": article.id,
                    "title": article.title,
                    "word_count": article.word_count,
                    "created_at": article.created_at.isoformat(),
                    "url": response.url
                },
                "message": response.message
            })
            
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"API generation failed: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/custom-generate', methods=['GET', 'POST'])
def custom_generate():
    """Custom article generation page with advanced options."""
    if request.method == 'POST':
        try:
            # Get and validate form data
            topic = sanitize_html(request.form.get('topic', '').strip())
            tone = sanitize_html(request.form.get('tone', 'professional'))
            
            # Validate word count
            try:
                word_count = int(request.form.get('word_count', 1500))
                if word_count < 300 or word_count > 5000:
                    flash("Word count must be between 300 and 5000", "error")
                    return render_template('custom_generate.html', config=config)
            except ValueError:
                flash("Invalid word count", "error")
                return render_template('custom_generate.html', config=config)
            
            # Sanitize keywords
            keywords = []
            for k in request.form.get('keywords', '').split(','):
                k = sanitize_html(k.strip())
                if k and len(k) >= 2:
                    keywords.append(k)
            
            include_images = request.form.get('include_images') == 'on'
            image_style = sanitize_html(request.form.get('image_style', 'professional'))
            formatting_options = [sanitize_html(opt) for opt in request.form.getlist('formatting_options')]
            include_cta = request.form.get('include_cta') == 'on'
            cta_text = sanitize_html(request.form.get('cta_text', 'Schedule a Free Consultation Today'))
            
            if not topic:
                flash("Please enter a topic for your article", "error")
                return render_template('custom_generate.html', config=config)
            
            # Validate topic length
            if len(topic) < 5 or len(topic) > 200:
                flash("Topic must be between 5 and 200 characters", "error")
                return render_template('custom_generate.html', config=config)
            
            # Create custom blog config for this generation
            custom_blog = BlogConfig(
                id="custom_generation",
                niche="custom technology article",
                target_audience="Houston homeowners and business owners",
                tone=tone,
                posts_per_week=1,
                keywords=keywords,
                word_count=word_count,
                publish_to="file",
                business_name="Executive Technology Group",
                business_phone="(281) 826-1880",
                business_website="https://www.executivetechnologygroup.com/",
                service_areas="Houston & surrounding areas",
                specialties=["Smart Home Automation", "Home Theater & AV Systems", "Networking Solutions", "Security & Surveillance", "Lighting Control"]
            )
            
            # Generate article with custom parameters
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                # Create enhanced prompt with custom options
                enhanced_prompt = f"""
                Create a comprehensive article about: {topic}
                
                Target audience: {custom_blog.target_audience}
                Tone: {tone}
                Word count: {word_count}
                Keywords to include: {', '.join(keywords)}
                
                Business context:
                - Company: {custom_blog.business_name}
                - Phone: {custom_blog.business_phone}
                - Website: {custom_blog.business_website}
                - Service areas: {custom_blog.service_areas}
                - Specialties: {', '.join(custom_blog.specialties)}
                
                Formatting requirements:
                - Include headings and subheadings
                - Use bullet points and numbered lists where appropriate
                - Add callout boxes for important information
                - Include relevant statistics and examples
                - End with a strong call-to-action
                
                {"Include image suggestions for: " + image_style + " style images" if include_images else ""}
                
                {"Include CTA: " + cta_text if include_cta else ""}
                
                Make the article SEO-optimized and valuable for Houston-area customers.
                """
                
                # Generate article
                article = loop.run_until_complete(
                    content_generator.generate_article_with_prompt(custom_blog, enhanced_prompt)
                )
                
                # Apply custom formatting
                if formatting_options:
                    article = apply_custom_formatting(article, formatting_options)
                
                # Add images if requested
                if include_images:
                    article = add_image_suggestions(article, image_style)
                
                # Add CTA if requested
                if include_cta:
                    article = add_call_to_action(article, cta_text, custom_blog)
                
                # Apply SEO optimization
                article = seo_optimizer.optimize_article(article)
                
                # Publish article
                response = loop.run_until_complete(
                    file_publisher.publish(article)
                )
                
                if response.success:
                    flash(f"Custom article generated successfully: {article.title}", "success")
                    logger.info(f"Generated custom article: {article.title}")
                    return redirect(url_for('view_article', article_id=article.id))
                else:
                    flash(f"Failed to publish article: {response.message}", "error")
                    
            finally:
                loop.close()
            
        except Exception as e:
            logger.error(f"Failed to generate custom article: {e}")
            flash(f"Error generating custom article: {e}", "error")
    
    return render_template('custom_generate.html', config=config)


@app.route('/api/custom-generate', methods=['POST'])
def api_custom_generate():
    """API endpoint for custom article generation."""
    try:
        data = request.get_json()
        
        # Extract parameters
        topic = data.get('topic', '').strip()
        tone = data.get('tone', 'professional')
        word_count = int(data.get('word_count', 1500))
        keywords = data.get('keywords', [])
        include_images = data.get('include_images', False)
        image_style = data.get('image_style', 'professional')
        formatting_options = data.get('formatting_options', [])
        include_cta = data.get('include_cta', True)
        cta_text = data.get('cta_text', 'Schedule a Free Consultation Today')
        
        if not topic:
            return jsonify({"error": "Topic is required"}), 400
        
        # Create custom blog config
        custom_blog = BlogConfig(
            id="custom_generation",
            niche="custom technology article",
            target_audience="Houston homeowners and business owners",
            tone=tone,
            posts_per_week=1,
            keywords=keywords,
            word_count=word_count,
            publish_to="file",
            business_name="Executive Technology Group",
            business_phone="(281) 826-1880",
            business_website="https://www.executivetechnologygroup.com/",
            service_areas="Houston & surrounding areas",
            specialties=["Smart Home Automation", "Home Theater & AV Systems", "Networking Solutions", "Security & Surveillance", "Lighting Control"]
        )
        
        # Generate article
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            enhanced_prompt = f"""
            Create a comprehensive article about: {topic}
            
            Target audience: {custom_blog.target_audience}
            Tone: {tone}
            Word count: {word_count}
            Keywords to include: {', '.join(keywords)}
            
            Business context:
            - Company: {custom_blog.business_name}
            - Phone: {custom_blog.business_phone}
            - Website: {custom_blog.business_website}
            - Service areas: {custom_blog.service_areas}
            - Specialties: {', '.join(custom_blog.specialties)}
            
            Formatting requirements:
            - Include headings and subheadings
            - Use bullet points and numbered lists where appropriate
            - Add callout boxes for important information
            - Include relevant statistics and examples
            - End with a strong call-to-action
            
            {"Include image suggestions for: " + image_style + " style images" if include_images else ""}
            
            {"Include CTA: " + cta_text if include_cta else ""}
            
            Make the article SEO-optimized and valuable for Houston-area customers.
            """
            
            article = loop.run_until_complete(
                content_generator.generate_article_with_prompt(custom_blog, enhanced_prompt)
            )
            
            # Apply custom formatting
            if formatting_options:
                article = apply_custom_formatting(article, formatting_options)
            
            if include_images:
                article = add_image_suggestions(article, image_style)
            
            if include_cta:
                article = add_call_to_action(article, cta_text, custom_blog)
            
            response = loop.run_until_complete(
                file_publisher.publish(article)
            )
            
            return jsonify({
                "success": response.success,
                "article": {
                    "id": article.id,
                    "title": article.title,
                    "word_count": article.word_count,
                    "created_at": article.created_at.isoformat(),
                    "url": response.url,
                    "content": article.content[:500] + "..." if len(article.content) > 500 else article.content
                },
                "message": response.message
            })
            
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"API custom generation failed: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/image-suggestions', methods=['POST'])
def api_image_suggestions():
    """API endpoint for getting image suggestions."""
    try:
        data = request.get_json()
        topic = data.get('topic', '').strip()
        style = data.get('style', 'professional')
        count = int(data.get('count', 3))
        
        if not topic:
            return jsonify({"error": "Topic is required"}), 400
        
        # Get image suggestions
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            suggestions = loop.run_until_complete(
                image_handler.get_image_suggestions(topic, style, count)
            )
            
            # Convert to JSON-serializable format
            suggestions_data = []
            for suggestion in suggestions:
                suggestions_data.append({
                    "id": suggestion.id,
                    "title": suggestion.title,
                    "description": suggestion.description,
                    "url": suggestion.url,
                    "thumbnail_url": suggestion.thumbnail_url,
                    "photographer": suggestion.photographer,
                    "photographer_url": suggestion.photographer_url,
                    "download_url": suggestion.download_url,
                    "width": suggestion.width,
                    "height": suggestion.height,
                    "created_at": suggestion.created_at.isoformat()
                })
            
            return jsonify({
                "success": True,
                "suggestions": suggestions_data,
                "count": len(suggestions_data)
            })
            
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Failed to get image suggestions: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/seo-analysis', methods=['POST'])
def api_seo_analysis():
    """API endpoint for SEO analysis."""
    try:
        data = request.get_json()
        article_id = data.get('article_id')
        
        if not article_id:
            return jsonify({"error": "Article ID is required"}), 400
        
        # Find article file
        output_dir = Path("output")
        json_files = list(output_dir.glob(f"*{article_id}*.json"))
        
        if not json_files:
            return jsonify({"error": "Article not found"}), 404
        
        # Load article data
        with open(json_files[0], 'r', encoding='utf-8') as f:
            article_data = json.load(f)
        
        # Create Article object
        article = Article(
            id=article_data['id'],
            title=article_data['title'],
            content=article_data['content'],
            meta_description=article_data['meta_description'],
            keywords=article_data['keywords'],
            word_count=article_data['word_count'],
            blog_id=article_data['blog_id'],
            created_at=datetime.fromisoformat(article_data['created_at'])
        )
        
        # Perform SEO analysis
        analysis = seo_optimizer.analyze_article(article)
        
        return jsonify({
            "success": True,
            "analysis": {
                "keyword_density": analysis.keyword_density,
                "meta_description_length": analysis.meta_description_length,
                "title_length": analysis.title_length,
                "heading_structure": analysis.heading_structure,
                "internal_links": analysis.internal_links,
                "external_links": analysis.external_links,
                "readability_score": analysis.readability_score,
                "seo_score": analysis.seo_score,
                "recommendations": analysis.recommendations
            }
        })
        
    except Exception as e:
        logger.error(f"Failed to analyze SEO: {e}")
        return jsonify({"error": str(e)}), 500


def apply_custom_formatting(article: Article, formatting_options: List[str]) -> Article:
    """Apply custom formatting options to an article."""
    content = article.content
    
    if 'headings' in formatting_options:
        # Ensure proper heading structure
        content = content.replace('\n\n', '\n\n## ')
    
    if 'lists' in formatting_options:
        # Convert numbered items to proper lists
        lines = content.split('\n')
        formatted_lines = []
        for line in lines:
            if line.strip().startswith(('1.', '2.', '3.', '4.', '5.')):
                formatted_lines.append(f"- {line.strip()[2:].strip()}")
            else:
                formatted_lines.append(line)
        content = '\n'.join(formatted_lines)
    
    if 'callouts' in formatting_options:
        # Add callout boxes for important information
        content = content.replace('Important:', '> **Important:**')
        content = content.replace('Note:', '> **Note:**')
        content = content.replace('Tip:', '> **Tip:**')
    
    if 'cta_buttons' in formatting_options:
        # Add styled CTA buttons
        content = content.replace('[Call to Action]', 
                                '<div class="cta-box" style="background: #f8f9fa; padding: 20px; border-left: 4px solid #007bff; margin: 20px 0;">'
                                '<h4>Ready to Get Started?</h4>'
                                '<p>Contact Executive Technology Group today for a free consultation.</p>'
                                '<a href="tel:(281) 826-1880" class="btn btn-primary">Call (281) 826-1880</a>'
                                '</div>')
    
    # Update article with formatted content
    article.content = content
    return article


def add_image_suggestions(article: Article, image_style: str) -> Article:
    """Add image suggestions to an article."""
    image_suggestions = {
        'professional': [
            'Modern smart home control panel',
            'Professional networking equipment setup',
            'Elegant home theater installation',
            'Security camera system overview',
            'Lighting control interface'
        ],
        'lifestyle': [
            'Family enjoying smart home features',
            'Homeowner using mobile app to control lights',
            'Professional working from smart home office',
            'Family movie night in home theater',
            'Peaceful evening with automated lighting'
        ],
        'technical': [
            'Network infrastructure diagram',
            'Smart home system architecture',
            'Security system components',
            'Audio/visual equipment setup',
            'Lighting control wiring diagram'
        ]
    }
    
    suggestions = image_suggestions.get(image_style, image_suggestions['professional'])
    
    # Add image suggestions to content
    image_section = f"""
    
## Suggested Images

{chr(10).join([f"- {suggestion}" for suggestion in suggestions[:3]])}

*Images should be high-quality, professional, and relevant to Houston-area homes and businesses.*
"""
    
    article.content += image_section
    return article


def add_call_to_action(article: Article, cta_text: str, blog_config: BlogConfig) -> Article:
    """Add a call-to-action section to an article."""
    cta_section = f"""
    
## {cta_text}

**Executive Technology Group** is your trusted partner for technology solutions in Houston and surrounding areas. We specialize in:

- **Smart Home Automation** - Seamless integration and control
- **Home Theater & AV Systems** - Premium entertainment experiences  
- **Networking Solutions** - Reliable, high-speed connectivity
- **Security & Surveillance** - Advanced protection systems
- **Lighting Control** - Energy-efficient, automated lighting

### Why Choose Executive Technology Group?

- ✅ **20+ Years Experience** - Proven expertise in technology integration
- ✅ **Certified Installers** - Thoroughly trained and certified team
- ✅ **Quality & Reliability** - Dependable, high-quality services
- ✅ **Veteran Owned & Operated** - Trusted by Houston businesses and homeowners

### Ready to Get Started?

**Call us today for a free consultation:** [(281) 826-1880](tel:281-826-1880)

**Visit our website:** [www.executivetechnologygroup.com](https://www.executivetechnologygroup.com/)

*Serving Houston & surrounding areas with professional technology solutions that just work.*
"""
    
    article.content += cta_section
    return article


def get_recent_articles() -> List[Dict]:
    """Get list of recent articles."""
    articles = []
    output_dir = Path("output")
    
    if not output_dir.exists():
        return articles
    
    # Get all HTML files
    html_files = list(output_dir.glob("*.html"))
    
    for html_file in html_files:
        try:
            # Extract article info from filename
            filename = html_file.stem
            parts = filename.split('_', 2)  # timestamp_title
            
            if len(parts) >= 3:
                timestamp_str = f"{parts[0]}_{parts[1]}"
                title = parts[2].replace('_', ' ')
                
                # Parse timestamp
                try:
                    created_at = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
                except ValueError:
                    created_at = datetime.fromtimestamp(html_file.stat().st_mtime)
                
                articles.append({
                    "id": filename,
                    "title": title,
                    "filename": html_file.name,
                    "created_at": created_at,
                    "url": f"/article/{filename}"
                })
        except Exception as e:
            logger.warning(f"Failed to process article file {html_file}: {e}")
    
    # Sort by creation time (newest first)
    articles.sort(key=lambda x: x["created_at"], reverse=True)
    return articles


if __name__ == '__main__':
    # Initialize AutoBlogger
    if not initialize_autoblogger():
        print("Failed to initialize AutoBlogger. Check logs for details.")
        sys.exit(1)
    
    # Get port from environment or use default (5001 per user preference)
    port = int(env_vars.get('FLASK_PORT', '5001'))
    debug_mode = env_vars.get('FLASK_DEBUG', 'false').lower() == 'true'
    
    print("AutoBlogger Web Interface")
    print("=" * 40)
    print(f"Starting web server on http://localhost:{port}")
    print("Health check: http://localhost:{port}/health")
    print("Press Ctrl+C to stop")
    print("=" * 40)
    
    # Run the Flask app
    # SECURITY: Never run with debug=True in production!
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
