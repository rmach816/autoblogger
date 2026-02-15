# AutoBlogger - Comprehensive User Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Configuration](#configuration)
4. [Using the Web Interface](#using-the-web-interface)
5. [Using the CLI](#using-the-cli)
6. [Content Generation](#content-generation)
7. [SEO Optimization](#seo-optimization)
8. [Publishing Options](#publishing-options)
9. [Troubleshooting](#troubleshooting)
10. [FAQs](#faqs)

---

## Introduction

AutoBlogger is an AI-powered blog automation tool that helps you generate high-quality, SEO-optimized blog content quickly and efficiently. It supports multiple AI providers (Gemini, Groq) and publishing platforms (file, WordPress, Medium, Wix).

### Key Features

- **AI-Powered Content Generation:** Uses advanced AI models to create engaging, original content
- **SEO Optimization:** Automatically optimizes articles for search engines
- **Multiple Publishing Options:** Publish to files, WordPress, Medium, or Wix
- **Image Integration:** Automatically suggests relevant images from Unsplash
- **Custom Prompts:** Generate content with your own custom prompts
- **Rate Limiting:** Built-in protection against API rate limits
- **Security:** Production-ready with input validation, CORS, and XSS protection

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- API keys for your chosen AI provider (Gemini or Groq)
- (Optional) Unsplash API key for image suggestions
- (Optional) Publishing platform credentials

### Quick Installation

1. **Clone the repository:**
```bash
git clone https://github.com/your-org/autoblogger.git
cd autoblogger
```

2. **Run the deployment script:**
```bash
python deploy.py
```

3. **Configure your environment:**

Edit `.env` with your API keys:
```bash
GEMINI_API_KEY=your_key_here
UNSPLASH_ACCESS_KEY=your_key_here
```

4. **Start the web interface:**
```bash
python web_app.py
```

Visit http://localhost:5001 in your browser.

---

## Configuration

### Application Settings

Edit `config/settings.json` to configure your blogs:

```json
{
  "ai_provider": "gemini",
  "publisher": "file",
  "environment": "development",
  "log_level": "INFO",
  "max_posts_per_day": 7,
  "request_timeout": 30,
  "blogs": [
    {
      "id": "my_tech_blog",
      "niche": "technology and software development",
      "target_audience": "developers and tech enthusiasts",
      "tone": "professional and informative",
      "posts_per_week": 3,
      "keywords": ["python", "web development", "AI"],
      "word_count": 1500,
      "publish_to": "file"
    }
  ]
}
```

### Configuration Options

| Field | Type | Description |
|-------|------|-------------|
| `ai_provider` | string | AI model to use: "gemini", "groq", or "mock" |
| `publisher` | string | Default publisher: "file", "wordpress", "medium", "wix" |
| `environment` | string | Environment: "development", "staging", "production" |
| `log_level` | string | Logging level: "DEBUG", "INFO", "WARNING", "ERROR" |
| `max_posts_per_day` | number | Maximum posts to generate per day |
| `request_timeout` | number | API request timeout in seconds |

### Blog Configuration

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier for the blog |
| `niche` | string | Topic/niche of the blog |
| `target_audience` | string | Intended audience |
| `tone` | string | Writing tone (professional, casual, friendly, etc.) |
| `posts_per_week` | number | Target posts per week (1-7) |
| `keywords` | array | SEO keywords to include |
| `word_count` | number | Target word count (300-5000) |
| `publish_to` | string | Publishing platform |

---

## Using the Web Interface

### Dashboard

The main dashboard shows:
- Configured blogs
- Recent articles
- Quick actions

### Generating Articles

1. **Quick Generation:**
   - Select a blog from the dropdown
   - Click "Generate Article"
   - Wait for generation to complete
   - View your article

2. **Custom Generation:**
   - Go to "Custom Generate" page
   - Enter your topic
   - Customize settings:
     - Word count
     - Tone
     - Keywords
     - Image style
     - Formatting options
   - Click "Generate"

### Viewing Articles

1. Go to "Articles" page
2. Browse generated articles
3. Click on an article to view full content
4. Download HTML or Markdown versions

---

## Using the CLI

### Generate Article

```bash
# Generate for all configured blogs
python main.py --generate-now

# Generate for specific blog
python main.py --generate-now --blog my_tech_blog

# List configured blogs
python main.py --list-blogs

# Dry run (preview without publishing)
python main.py --generate-now --dry-run
```

### CLI Options

```bash
python main.py --help

Options:
  --config PATH          Configuration file path
  --generate-now         Generate article immediately
  --blog BLOG_ID        Generate for specific blog ID
  --list-blogs          List configured blogs
  --dry-run             Preview without publishing
```

---

## Content Generation

### How It Works

1. **Input Processing:** Your blog configuration and optional custom prompt
2. **AI Generation:** AI model generates original content
3. **SEO Optimization:** Automatic optimization for search engines
4. **Image Suggestions:** Relevant images from Unsplash
5. **Publishing:** Save to file or publish to platform

### Content Quality Tips

- **Be Specific:** More specific niches produce better content
- **Use Good Keywords:** Choose relevant, searchable keywords
- **Set Appropriate Length:** 1000-2000 words is ideal for most topics
- **Define Your Audience:** Clear audience = better content
- **Choose the Right Tone:** Match tone to your brand

### Custom Prompts

Custom prompts give you full control:

```
Write a comprehensive guide about:
Topic: Getting Started with Python
Audience: Complete beginners
Tone: Friendly and encouraging
Include: Code examples, practical exercises, common mistakes
Format: Step-by-step tutorial with clear headings
```

---

## SEO Optimization

### Automatic SEO Features

AutoBlogger automatically:
- Generates meta descriptions (120-160 characters)
- Optimizes title length (30-60 characters)
- Ensures proper heading structure (H1, H2, H3)
- Maintains keyword density (1-3%)
- Adds schema markup
- Optimizes readability

### SEO Analysis

View SEO scores for your articles:
- **Keyword Density:** Percentage of keyword usage
- **Meta Description:** Length and quality
- **Title Optimization:** Length and keyword inclusion
- **Heading Structure:** Proper H1/H2/H3 hierarchy
- **Readability Score:** Flesch reading ease score
- **Overall SEO Score:** Combined score (0-100)

### SEO Recommendations

The system provides specific recommendations:
- "Increase keyword density - aim for 1-3%"
- "Meta description too short - aim for 120-160 characters"
- "Add more H2 headings for better structure"
- "Improve readability - use shorter sentences"

---

## Publishing Options

### File Publishing (Default)

Articles are saved as:
- **HTML:** Fully formatted with styling
- **Markdown:** Plain text with markdown formatting

Files are saved to: `output/YYYYMMDD_HHMMSS_Title.{html,md}`

### WordPress Publishing

1. Set up WordPress credentials in `.env`:
```bash
WORDPRESS_SITE_URL=https://yoursite.com
WORDPRESS_USERNAME=your_username
WORDPRESS_APP_PASSWORD=your_app_password
```

2. Configure blog to use WordPress:
```json
{
  "publish_to": "wordpress"
}
```

3. Generate article - it will automatically publish

### Medium Publishing

1. Get Medium integration token
2. Add to `.env`:
```bash
MEDIUM_INTEGRATION_TOKEN=your_token
```

3. Configure and generate

### Wix Publishing

1. Get Wix API credentials
2. Add to `.env`:
```bash
WIX_API_KEY=your_key
WIX_SITE_ID=your_site_id
WIX_ACCOUNT_ID=your_account_id
```

3. Configure and generate

---

## Troubleshooting

### Common Issues

#### "API key not found"
- Check `.env` file exists
- Verify API key is correctly entered
- Restart the application

#### "Rate limit exceeded"
- Wait a few minutes
- Check your API provider's rate limits
- Reduce generation frequency

#### "Configuration invalid"
- Validate JSON syntax in `config/settings.json`
- Check all required fields are present
- Review field value constraints

#### "Failed to generate article"
- Check API key is valid
- Verify internet connection
- Check logs: `logs/autoblogger.log`
- Try using mock provider for testing

### Logging

View detailed logs in `logs/autoblogger.log`:
- Application events
- API calls and responses
- Errors and warnings
- Performance metrics

### Getting Help

1. Check this documentation
2. Review logs for error messages
3. Consult `docs/` directory
4. Open GitHub issue
5. Email support

---

## FAQs

### General

**Q: Is AutoBlogger free?**
A: AutoBlogger is free, but you need API keys from AI providers (which may have costs).

**Q: What AI providers are supported?**
A: Gemini (Google), Groq, and a mock provider for testing.

**Q: Can I use my own AI model?**
A: Yes, you can extend the AI provider interface to add custom models.

### Content Quality

**Q: Is the generated content original?**
A: Yes, AI generates unique content each time, but always review before publishing.

**Q: Can I edit generated content?**
A: Yes, you can edit the HTML or Markdown files before publishing.

**Q: How good is the SEO optimization?**
A: Our SEO optimizer follows best practices, but manual review is recommended.

### Publishing

**Q: Can I schedule posts?**
A: Scheduled posting is on the roadmap - currently manual or cron-based.

**Q: Does it support multiple blogs?**
A: Yes, configure multiple blogs in `settings.json`.

**Q: Can I customize the output format?**
A: Yes, you can modify templates in `templates/` directory.

### Security

**Q: Is my API key secure?**
A: Yes, keys are stored in `.env` and never logged or exposed.

**Q: Can I run this in production?**
A: Yes, see `docs/DEPLOYMENT.md` for production setup.

**Q: Is rate limiting included?**
A: Yes, built-in rate limiting for both API calls and web requests.

---

## Next Steps

- **Explore Custom Prompts:** Create highly specific content
- **Set Up Publishing:** Connect to WordPress, Medium, or Wix
- **Optimize Your Content:** Review SEO recommendations
- **Automate:** Set up scheduled generation
- **Scale:** Deploy to production server

For more information:
- [Installation Guide](SETUP.md)
- [Configuration Guide](CONFIGURATION.md)
- [Deployment Guide](DEPLOYMENT.md)
- [Production Readiness](PRODUCTION_READINESS_PLAN.md)

---

**Version:** 1.0.0  
**Last Updated:** October 2025  
**License:** MIT

