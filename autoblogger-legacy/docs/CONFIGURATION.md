# AutoBlogger Configuration Guide

**Complete guide to configuring AutoBlogger for your needs**

---

## Configuration Overview

AutoBlogger uses JSON configuration files to control all aspects of the system. This allows you to customize behavior without changing code.

### Configuration Files

- **`config/settings.json`** - Main application configuration
- **`.env`** - Environment variables (API keys, secrets)
- **`config/settings.example.json`** - Template configuration

---

## Main Configuration (`config/settings.json`)

### Basic Structure

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
      "id": "blog_001",
      "niche": "sustainable gardening",
      "target_audience": "urban gardeners",
      "tone": "friendly and informative",
      "posts_per_week": 2,
      "keywords": ["eco-friendly", "organic", "sustainable"],
      "word_count": 1200,
      "publish_to": "file"
    }
  ]
}
```

---

## Global Settings

### AI Provider Settings

| Setting | Options | Description |
|---------|---------|-------------|
| `ai_provider` | `"mock"`, `"gemini"`, `"groq"` | AI service to use for content generation |

**Examples:**
```json
{
  "ai_provider": "gemini"  // Use Google Gemini (requires API key)
}
```

```json
{
  "ai_provider": "mock"    // Use mock provider (for testing)
}
```

### Publisher Settings

| Setting | Options | Description |
|---------|---------|-------------|
| `publisher` | `"file"`, `"wix"`, `"wordpress"`, `"medium"` | Default publishing platform |

**Examples:**
```json
{
  "publisher": "file"        // Save as HTML/Markdown files
}
```

```json
{
  "publisher": "wix"         // Auto-publish to Wix (requires API setup)
}
```

### Environment Settings

| Setting | Options | Description |
|---------|---------|-------------|
| `environment` | `"development"`, `"staging"`, `"production"` | Environment mode |
| `log_level` | `"DEBUG"`, `"INFO"`, `"WARNING"`, `"ERROR"`, `"CRITICAL"` | Logging verbosity |

**Examples:**
```json
{
  "environment": "development",
  "log_level": "DEBUG"      // Show all log messages
}
```

```json
{
  "environment": "production",
  "log_level": "WARNING"    // Only show warnings and errors
}
```

### Rate Limiting Settings

| Setting | Type | Description |
|---------|------|-------------|
| `max_posts_per_day` | Integer (1-50) | Maximum articles per day (safety limit) |
| `request_timeout` | Integer (5-300) | API request timeout in seconds |

**Examples:**
```json
{
  "max_posts_per_day": 7,     // Generate max 7 articles per day
  "request_timeout": 30       // Wait 30 seconds for API responses
}
```

---

## Blog Configuration

Each blog is configured individually in the `blogs` array.

### Required Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `id` | String | Unique blog identifier | `"my_garden_blog"` |
| `niche` | String | Blog topic/niche | `"sustainable gardening"` |
| `target_audience` | String | Who you're writing for | `"urban gardeners"` |

### Content Settings

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `tone` | String | Writing style | `"friendly and informative"` |
| `word_count` | Integer | Target article length | `1200` |
| `keywords` | Array | SEO keywords to include | `["eco-friendly", "organic"]` |

### Publishing Settings

| Field | Type | Options | Description |
|-------|------|---------|-------------|
| `publish_to` | String | `"file"`, `"wix"`, `"wordpress"`, `"medium"` | Where to publish articles |
| `posts_per_week` | Integer | 1-7 | How many articles to generate per week |

---

## Complete Blog Configuration Examples

### Example 1: Gardening Blog

```json
{
  "id": "sustainable_garden",
  "niche": "sustainable gardening",
  "target_audience": "urban gardeners and eco-conscious homeowners",
  "tone": "friendly, encouraging, and practical",
  "posts_per_week": 3,
  "keywords": [
    "eco-friendly gardening",
    "organic growing",
    "sustainable practices",
    "urban farming",
    "composting"
  ],
  "word_count": 1500,
  "publish_to": "file"
}
```

### Example 2: Technology Blog

```json
{
  "id": "tech_insights",
  "niche": "software development and technology trends",
  "target_audience": "developers, tech professionals, and entrepreneurs",
  "tone": "professional, analytical, and forward-thinking",
  "posts_per_week": 2,
  "keywords": [
    "software development",
    "programming",
    "technology trends",
    "coding best practices",
    "digital innovation"
  ],
  "word_count": 2000,
  "publish_to": "wordpress"
}
```

### Example 3: Health & Wellness Blog

```json
{
  "id": "wellness_journey",
  "niche": "holistic health and wellness",
  "target_audience": "health-conscious individuals seeking natural solutions",
  "tone": "supportive, evidence-based, and empowering",
  "posts_per_week": 4,
  "keywords": [
    "holistic health",
    "natural wellness",
    "mindfulness",
    "nutrition",
    "mental health"
  ],
  "word_count": 1200,
  "publish_to": "medium"
}
```

---

## Multiple Blogs Configuration

You can configure multiple blogs in a single setup:

```json
{
  "ai_provider": "gemini",
  "publisher": "file",
  "environment": "development",
  "log_level": "INFO",
  "max_posts_per_day": 10,
  "request_timeout": 30,
  "blogs": [
    {
      "id": "garden_blog",
      "niche": "sustainable gardening",
      "target_audience": "urban gardeners",
      "tone": "friendly and informative",
      "posts_per_week": 2,
      "keywords": ["eco-friendly", "organic"],
      "word_count": 1200,
      "publish_to": "file"
    },
    {
      "id": "tech_blog",
      "niche": "software development",
      "target_audience": "developers",
      "tone": "professional and technical",
      "posts_per_week": 1,
      "keywords": ["programming", "software"],
      "word_count": 2000,
      "publish_to": "wix"
    },
    {
      "id": "business_blog",
      "niche": "entrepreneurship",
      "target_audience": "small business owners",
      "tone": "motivational and practical",
      "posts_per_week": 3,
      "keywords": ["business", "entrepreneurship"],
      "word_count": 1000,
      "publish_to": "wordpress"
    }
  ]
}
```

---

## Environment Variables (`.env`)

### Required API Keys

```bash
# AI Content Generation
GEMINI_API_KEY=your_gemini_api_key_here
UNSPLASH_ACCESS_KEY=your_unsplash_access_key_here

# Optional: Alternative AI Providers
GROQ_API_KEY=your_groq_api_key_here

# Optional: Publishing Platforms
WIX_API_KEY=your_wix_api_key_here
WIX_SITE_ID=your_wix_site_id_here
WIX_ACCOUNT_ID=your_wix_account_id_here

WORDPRESS_SITE_URL=https://yoursite.com
WORDPRESS_USERNAME=your_username
WORDPRESS_APP_PASSWORD=your_wordpress_app_password

MEDIUM_INTEGRATION_TOKEN=your_medium_token_here
```

### Application Settings

```bash
# Logging
LOG_LEVEL=INFO
ENVIRONMENT=development

# Rate Limiting
MAX_POSTS_PER_DAY=7
REQUEST_TIMEOUT=30

# Features
ENABLE_IMAGE_GENERATION=true
ENABLE_CACHING=true
```

---

## Advanced Configuration

### Custom AI Prompts

You can customize the AI generation prompts by modifying the content generator. This requires code changes but allows for:

- Custom prompt templates
- Industry-specific instructions
- Brand voice guidelines
- Content structure preferences

### Publisher-Specific Settings

Different publishers may require additional configuration:

#### Wix Publishing
```json
{
  "publish_to": "wix",
  "wix_settings": {
    "site_id": "your_site_id",
    "account_id": "your_account_id",
    "auto_publish": true,
    "featured_image": true
  }
}
```

#### WordPress Publishing
```json
{
  "publish_to": "wordpress",
  "wordpress_settings": {
    "site_url": "https://yoursite.com",
    "username": "your_username",
    "app_password": "your_app_password",
    "category": "Auto-Generated",
    "tags": ["AI", "Automated"]
  }
}
```

#### Medium Publishing
```json
{
  "publish_to": "medium",
  "medium_settings": {
    "publication": "your_publication",
    "tags": ["technology", "AI"],
    "license": "all-rights-reserved"
  }
}
```

---

## Configuration Validation

AutoBlogger validates your configuration on startup:

### Common Validation Errors

1. **Missing required fields**
   ```
   Error: Blog 'blog_001' missing required field 'niche'
   ```

2. **Invalid field values**
   ```
   Error: 'posts_per_week' must be between 1 and 7
   ```

3. **Missing API keys**
   ```
   Error: GEMINI_API_KEY required for Gemini AI provider
   ```

### Validation Checklist

- [ ] All required fields present
- [ ] Field values within valid ranges
- [ ] API keys provided for selected providers
- [ ] Publisher credentials valid
- [ ] Output directories writable

---

## Configuration Migration

When upgrading AutoBlogger, configuration changes are handled automatically:

### Automatic Migrations

- New fields get default values
- Deprecated fields are ignored
- Invalid values are corrected
- Warnings shown for manual review

### Manual Migration

For major changes, you may need to update your configuration:

1. **Backup current config**
   ```bash
   cp config/settings.json config/settings.json.backup
   ```

2. **Update configuration**
   - Add new fields
   - Update field names
   - Adjust values

3. **Test configuration**
   ```bash
   python main.py --list-blogs
   ```

---

## Best Practices

### Configuration Management

1. **Use version control** for configuration files
2. **Keep secrets in `.env`** (never commit to git)
3. **Test configurations** before production
4. **Document custom settings** for team members

### Performance Optimization

1. **Limit concurrent blogs** (max 5-10)
2. **Set reasonable word counts** (1000-2000 words)
3. **Use appropriate post frequencies** (1-3 per week)
4. **Monitor API usage** to avoid rate limits

### Content Quality

1. **Be specific with niches** (avoid broad topics)
2. **Define clear target audiences**
3. **Use relevant keywords** (5-10 per blog)
4. **Set appropriate tones** for your brand

---

## Troubleshooting Configuration

### Common Issues

#### 1. "Configuration validation failed"

**Check:**
- All required fields present
- Field values within ranges
- JSON syntax correct

#### 2. "API key not found"

**Check:**
- `.env` file exists
- API key variable name correct
- No extra spaces in key

#### 3. "Publisher not available"

**Check:**
- Publisher credentials in `.env`
- Publisher type supported
- Network connectivity

### Debug Configuration

```bash
# Check configuration loading
python -c "
from src.utils import load_config
config = load_config('config/settings.json')
print('Configuration loaded successfully')
print(f'Found {len(config.blogs)} blogs')
"

# Validate environment
python -c "
from src.utils import validate_environment, load_config
config = load_config('config/settings.json')
validate_environment(config)
print('Environment validation passed')
"
```

---

## Configuration Examples

### Minimal Configuration

```json
{
  "ai_provider": "mock",
  "publisher": "file",
  "blogs": [
    {
      "id": "test_blog",
      "niche": "technology",
      "target_audience": "developers",
      "tone": "professional",
      "keywords": ["programming"],
      "word_count": 1000,
      "publish_to": "file"
    }
  ]
}
```

### Production Configuration

```json
{
  "ai_provider": "gemini",
  "publisher": "wix",
  "environment": "production",
  "log_level": "WARNING",
  "max_posts_per_day": 10,
  "request_timeout": 60,
  "blogs": [
    {
      "id": "main_blog",
      "niche": "sustainable living",
      "target_audience": "eco-conscious consumers",
      "tone": "inspiring and practical",
      "posts_per_week": 3,
      "keywords": [
        "sustainable living",
        "eco-friendly",
        "green lifestyle",
        "environmental awareness"
      ],
      "word_count": 1500,
      "publish_to": "wix"
    }
  ]
}
```

---

**Next Steps:**
- [SETUP.md](SETUP.md) - Initial setup instructions
- [PUBLISHERS.md](PUBLISHERS.md) - Publishing platform configuration
- [API_PROVIDERS.md](API_PROVIDERS.md) - AI provider configuration
