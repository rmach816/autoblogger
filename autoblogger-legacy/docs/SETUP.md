# AutoBlogger Setup Guide

**Complete step-by-step setup instructions for AutoBlogger**

---

## Prerequisites

Before you begin, ensure you have:

- **Python 3.10+** installed on your system
- **Git** for version control (optional but recommended)
- **Text editor** (VS Code, Cursor, or any editor you prefer)
- **Terminal/Command Prompt** access

### Check Python Version

```bash
python --version
# Should show Python 3.10 or higher
```

If you don't have Python 3.10+, download it from [python.org](https://python.org).

---

## Step 1: Project Setup (5 minutes)

### 1.1 Create Virtual Environment

```bash
# Navigate to your project directory
cd autoBlogger

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 1.2 Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

### 1.3 Verify Installation

```bash
# Check that packages are installed
pip list | grep -E "(google-generativeai|httpx|pydantic)"
```

---

## Step 2: Get Free API Keys (15 minutes)

### 2.1 Google Gemini API (Required for AI content)

1. **Go to**: https://ai.google.dev/
2. **Click**: "Get API Key"
3. **Create**: New project (or select existing)
4. **Generate**: API key
5. **Copy**: The key (starts with `AIza...`)

**Free Tier**: 1500 requests/day, 15 requests/minute

### 2.2 Unsplash API (Required for images)

1. **Go to**: https://unsplash.com/developers
2. **Register**: Create developer account
3. **Create**: New application
4. **Copy**: Access Key

**Free Tier**: 50 requests/hour

### 2.3 Optional: Wix API (For auto-publishing)

1. **Go to**: https://dev.wix.com/
2. **Create**: New app
3. **Get**: API key, Site ID, Account ID

**Note**: Only needed if you want auto-publishing to Wix

---

## Step 3: Environment Configuration (2 minutes)

### 3.1 Create Environment File

Create a file named `.env` in your project root:

```bash
# Copy the template
cp .env.example .env
```

### 3.2 Add Your API Keys

Edit `.env` file and add your keys:

```bash
# AI Provider API Keys
GEMINI_API_KEY=your_gemini_key_here
UNSPLASH_ACCESS_KEY=your_unsplash_key_here

# Optional: Other providers
GROQ_API_KEY=your_groq_key_here

# Application Settings
LOG_LEVEL=INFO
ENVIRONMENT=development
```

**Important**: Never commit the `.env` file to version control!

---

## Step 4: Configure Your Blog (5 minutes)

### 4.1 Create Configuration File

```bash
# Copy the example configuration
cp config/settings.example.json config/settings.json
```

### 4.2 Edit Configuration

Open `config/settings.json` and customize:

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
      "id": "my_blog_001",
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

### 4.3 Configuration Options

| Field | Description | Example |
|-------|-------------|---------|
| `id` | Unique blog identifier | `"my_blog_001"` |
| `niche` | Your blog's topic/niche | `"sustainable gardening"` |
| `target_audience` | Who you're writing for | `"urban gardeners"` |
| `tone` | Writing style | `"friendly and informative"` |
| `posts_per_week` | How many articles to generate | `2` (1-7) |
| `keywords` | SEO keywords to include | `["eco-friendly", "organic"]` |
| `word_count` | Target article length | `1200` (500-3000) |
| `publish_to` | Where to publish | `"file"`, `"wix"`, `"wordpress"` |

---

## Step 5: Test Your Setup (5 minutes)

### 5.1 Generate Your First Article

```bash
# Generate an article immediately
python main.py --generate-now
```

### 5.2 Check Output

Look in the `output/` directory for your generated files:

```
output/
├── 20241004_123000_Sustainable_Gardening_Tips.html
└── 20241004_123000_Sustainable_Gardening_Tips.md
```

### 5.3 Verify Content Quality

Open the HTML file in your browser to see the formatted article.

---

## Step 6: Run Tests (Optional but Recommended)

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test
pytest tests/unit/test_content_generator.py -v
```

---

## Step 7: Set Up Scheduling (Optional)

### 7.1 Manual Scheduling

```bash
# Generate articles for all blogs
python main.py --generate-now

# Generate for specific blog
python main.py --generate-now --blog my_blog_001
```

### 7.2 Automated Scheduling (Coming Soon)

```bash
# Start the scheduler
python main.py --schedule
```

---

## Troubleshooting

### Common Issues

#### 1. "ModuleNotFoundError: No module named 'src'"

**Solution**: Make sure you're in the project root directory and virtual environment is activated.

```bash
# Check you're in the right directory
pwd
# Should show: /path/to/autoBlogger

# Check virtual environment
which python
# Should show: /path/to/autoBlogger/venv/bin/python
```

#### 2. "Configuration file not found"

**Solution**: Create the configuration file:

```bash
cp config/settings.example.json config/settings.json
```

#### 3. "API key not found"

**Solution**: Check your `.env` file:

```bash
# Check if .env exists
ls -la .env

# Check if keys are set
cat .env | grep GEMINI_API_KEY
```

#### 4. "Permission denied" when creating files

**Solution**: Check directory permissions:

```bash
# Make sure output directory is writable
chmod 755 output/
```

### Getting Help

1. **Check logs**: Look in `logs/autoblogger.log`
2. **Run with debug**: Set `LOG_LEVEL=DEBUG` in `.env`
3. **Test components**: Run individual tests
4. **Ask for help**: Create an issue or ask the AI assistant

---

## Next Steps

### Immediate Next Steps

1. **Generate more articles**: Try different niches and configurations
2. **Customize content**: Adjust tone, keywords, and word count
3. **Test different publishers**: Try Wix or WordPress publishing
4. **Set up automation**: Configure scheduling for regular posting

### Advanced Setup

1. **Multiple blogs**: Add more blog configurations
2. **Custom AI providers**: Integrate with other AI services
3. **Custom publishers**: Add new publishing platforms
4. **Web dashboard**: Set up the management interface

### Production Deployment

1. **Environment setup**: Configure for production
2. **Monitoring**: Set up logging and error tracking
3. **Backup**: Configure data backup
4. **Scaling**: Prepare for multiple users

---

## Success Checklist

- [ ] Python 3.10+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] API keys obtained (Gemini + Unsplash)
- [ ] `.env` file created with API keys
- [ ] `config/settings.json` configured
- [ ] First article generated successfully
- [ ] Output files created in `output/` directory
- [ ] Tests passing (`pytest`)
- [ ] Logs working (`logs/autoblogger.log`)

---

## Quick Commands Reference

```bash
# Generate article now
python main.py --generate-now

# Generate for specific blog
python main.py --generate-now --blog my_blog_001

# List configured blogs
python main.py --list-blogs

# Run tests
pytest

# Check logs
tail -f logs/autoblogger.log

# Deactivate virtual environment
deactivate
```

---

**Congratulations! You now have a working AutoBlogger setup! 🎉**

**Next**: Read [CONFIGURATION.md](CONFIGURATION.md) to learn about all configuration options.
