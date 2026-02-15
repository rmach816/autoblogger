# AutoBlogger 🚀

**Zero-cost, AI-powered blog automation that generates and publishes SEO-optimized articles automatically.**

Build from personal tool → Monetizable SaaS platform

---

## 🎯 What is AutoBlogger?

AutoBlogger is a modular Python application that:
- ✅ Generates high-quality blog articles using **free AI APIs** (Google Gemini, Groq)
- ✅ Creates SEO-optimized content with metadata, keywords, and structure
- ✅ Fetches relevant images from **free sources** (Unsplash, Pexels)
- ✅ Publishes automatically to **multiple platforms** (Wix, WordPress, Medium, or saves as files)
- ✅ Schedules posts (1-7 per week, fully configurable)
- ✅ Runs entirely on **free tier APIs** → $0/month operating cost

**Perfect for:**
- Bloggers who want consistent content without writing
- Small businesses needing regular blog updates
- Entrepreneurs building niche site portfolios
- Agencies managing multiple client blogs
- Anyone wanting to **monetize** as a SaaS product

---

## 💰 Cost Breakdown

### Using AutoBlogger (Free):
| Component | Provider | Free Tier | Cost |
|-----------|----------|-----------|------|
| AI Content | Google Gemini | 1500 req/day | **$0** |
| Images | Unsplash | 50 req/hour | **$0** |
| Hosting | Your PC / Free tier | Vercel/Railway | **$0** |
| Database | SQLite | Unlimited | **$0** |
| **Total** | | | **$0/month** |

### Alternative (Paid Service):
- Wix AutoBlogger App: **$8.99-22.49/month**
- You own nothing, no customization, subscription forever

**AutoBlogger gives you:**
- ✅ Own the code
- ✅ Unlimited customization
- ✅ Sell as service ($50+/month to clients)
- ✅ Build SaaS business
- ✅ White-label opportunities

---

## 🏗️ Architecture

```
autoBlogger/
├── .cursor/
│   ├── rules.md              # Project-specific rules
│   └── prompts.md            # AI assistant guidelines
├── config/
│   ├── settings.json         # Main configuration
│   └── blogs.json            # Multi-blog setup
├── src/
│   ├── content_generator.py  # AI article creation
│   ├── image_handler.py      # Image fetching/generation
│   ├── seo_optimizer.py      # SEO optimization
│   ├── scheduler.py          # Post scheduling
│   └── publishers/           # Platform integrations
│       ├── base_publisher.py
│       ├── file_publisher.py
│       ├── wix_publisher.py
│       ├── wordpress_publisher.py
│       └── medium_publisher.py
├── tests/
│   ├── unit/
│   └── integration/
├── docs/
│   ├── SETUP.md
│   ├── CONFIGURATION.md
│   └── PUBLISHERS.md
├── logs/
├── output/                   # Generated articles
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Free API keys (see `.env.example`)

### Installation

```bash
# 1. Clone or download this project
git clone https://github.com/yourusername/autoblogger.git
cd autoblogger

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env with your API keys (see docs/SETUP.md for getting keys)

# 5. Configure your blog(s)
cp config/settings.example.json config/settings.json
# Edit config/settings.json with your blog details

# 6. Run your first generation
python main.py --generate-now

# 7. Start scheduler (for automated posting)
python main.py --schedule
```

### Get Free API Keys (5 minutes):
1. **Google Gemini**: https://ai.google.dev/ → Create API key
2. **Unsplash**: https://unsplash.com/developers → Register app
3. **Wix** (optional): https://dev.wix.com/ → Create app (if auto-publishing)

**Full setup guide**: See [docs/SETUP.md](docs/SETUP.md)

---

## ⚙️ Configuration

Edit `config/settings.json`:

```json
{
  "ai_provider": "gemini",
  "publisher": "file",
  "blogs": [
    {
      "id": "blog_001",
      "niche": "sustainable gardening",
      "target_audience": "urban gardeners",
      "tone": "friendly and informative",
      "posts_per_week": 2,
      "keywords": ["eco-friendly", "organic", "sustainable"],
      "word_count": 1200,
      "publish_to": "wix"
    }
  ]
}
```

**Publisher Options:**
- `file` - Save as HTML/markdown files (copy/paste to any platform)
- `wix` - Auto-publish to Wix blog
- `wordpress` - Auto-publish to WordPress
- `medium` - Auto-publish to Medium

See [docs/CONFIGURATION.md](docs/CONFIGURATION.md) for all options.

---

## 📊 Features

### Current (MVP)
- ✅ AI content generation (Gemini, Groq)
- ✅ SEO optimization (meta descriptions, keywords, structure)
- ✅ Image fetching (Unsplash, Pexels)
- ✅ File output (HTML, Markdown)
- ✅ Scheduling system
- ✅ Multi-blog support
- ✅ Error handling & retry logic
- ✅ Rate limit management

### In Progress
- 🚧 Wix auto-publishing
- 🚧 WordPress auto-publishing
- 🚧 Web dashboard UI

### Planned
- 📋 Medium publisher
- 📋 Ghost CMS integration
- 📋 Content calendar visualization
- 📋 A/B testing for headlines
- 📋 Analytics integration
- 📋 Backlink exchange network

### Monetization Features (Phase 4)
- 📋 User authentication
- 📋 Multi-tenant architecture
- 📋 Billing integration (Stripe)
- 📋 Usage metering
- 📋 Admin dashboard
- 📋 White-label capabilities

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test
pytest tests/unit/test_content_generator.py

# Run integration tests
pytest tests/integration/
```

**Test Coverage Target**: 80% lines, 70% branches

---

## 📖 Documentation

- **[Setup Guide](docs/SETUP.md)** - Detailed installation & API key setup
- **[Configuration](docs/CONFIGURATION.md)** - All config options explained
- **[Publishers](docs/PUBLISHERS.md)** - Adding new publishing platforms
- **[API Providers](docs/API_PROVIDERS.md)** - Adding new AI providers
- **[Monetization](docs/MONETIZATION.md)** - Business model & scaling

---

## 🛠️ Development

### Adding a New Publisher

1. Create `src/publishers/yourplatform_publisher.py`
2. Extend `BasePublisher` class
3. Implement `publish()` method
4. Register in `PublisherFactory`
5. Add tests in `tests/unit/publishers/`
6. Document in `docs/PUBLISHERS.md`

See [Contributing Guidelines](CONTRIBUTING.md)

---

## 💡 Use Cases

### Personal Use
- Maintain active blog with zero writing effort
- Build SEO with consistent content
- Monetize via ads, affiliates, products

### Service Business
- Offer "automated blog management" to local businesses
- Charge $50-200/month per client
- Zero cost to operate = pure profit
- Scale to 10-50 clients

### SaaS Product
- Add authentication & billing
- Charge $15-30/month (undercut existing solutions)
- 100 users = $1500-3000/month
- White-label for agencies

### Niche Site Empire
- Run 10+ automated niche blogs
- SEO + affiliate links + ads
- Minimal maintenance
- Passive income machine

---

## 🔒 Security

- Never commit `.env` file
- API keys stored in environment variables only
- Input validation on all user configs
- Rate limiting to prevent abuse
- Sanitized logging (no secrets in logs)
- Dependency security audits

---

## 📈 Roadmap

### Phase 1: MVP (Weeks 1-2) ✅
- [x] Core content generation
- [x] File publisher
- [x] Basic scheduling
- [x] Config system
- [x] Testing framework

### Phase 2: Platform Integration (Weeks 3-4)
- [ ] Wix publisher with OAuth
- [ ] WordPress publisher
- [ ] Error recovery system
- [ ] Comprehensive testing

### Phase 3: Scale (Month 2)
- [ ] Web dashboard UI
- [ ] Multi-blog management interface
- [ ] Advanced scheduling
- [ ] Analytics dashboard

### Phase 4: Monetize (Month 3+)
- [ ] User authentication
- [ ] Billing integration (Stripe)
- [ ] SaaS pricing tiers
- [ ] White-label features
- [ ] Marketplace listing

---

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Before contributing:**
1. Read `.cursor/rules.md` for code standards
2. Write tests for new features
3. Update documentation
4. Follow existing patterns

---

## 📝 License

MIT License - See [LICENSE](LICENSE) for details.

**Commercial Use Allowed** - Use this to build your business!

---

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/autoblogger/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/autoblogger/discussions)
- **Email**: your-email@example.com

---

## 🎉 Success Stories

_Have you monetized AutoBlogger? Share your story!_

---

## ⚠️ Disclaimer

This tool generates AI content. While quality is high, always review and edit articles before publishing. Some platforms have policies about AI-generated content - check their terms of service.

---

## 🙏 Acknowledgments

- Google Gemini for free AI API
- Unsplash for free images
- Open-source Python community

---

**Built with ❤️ by [Your Name]**

**Star ⭐ this repo if AutoBlogger helps you!**

---

## Quick Commands Reference

```bash
# Generate article now
python main.py --generate-now

# Start scheduler
python main.py --schedule

# Generate for specific blog
python main.py --blog blog_001

# Dry run (preview without publishing)
python main.py --dry-run

# Run tests
pytest

# View logs
tail -f logs/autoblogger.log
```

---

**Ready to automate your content? Let's go! 🚀**

