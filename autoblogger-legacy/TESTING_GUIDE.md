# AutoBlogger Testing Guide

**How to test AutoBlogger - it's a CLI app, not a web server!**

---

## 🎯 AutoBlogger is a CLI Application

AutoBlogger is a **command-line tool**, not a web application. There's no dev server to run. Instead, you test it by running commands directly.

**Think of it like:**
- `git` - command line tool
- `npm` - command line tool  
- `docker` - command line tool

**Not like:**
- React app (needs dev server)
- Django app (needs dev server)
- Express app (needs dev server)

---

## 🧪 Testing Methods

### 1. **Quick Setup Test** (Recommended First)
```bash
# Test that everything is working
python test_setup.py
```

This will:
- ✅ Test all imports work
- ✅ Test mock AI provider
- ✅ Test content generation
- ✅ Test file publishing
- ✅ Test configuration loading

### 2. **Generate Your First Article**
```bash
# Generate an article using mock AI (no API keys needed)
python main.py --generate-now
```

### 3. **List Configured Blogs**
```bash
# See what blogs are configured
python main.py --list-blogs
```

### 4. **Run Unit Tests**
```bash
# Run all tests with coverage
pytest

# Run specific test file
pytest tests/unit/test_content_generator.py -v

# Run with detailed output
pytest -v --tb=short
```

### 5. **Test Different Configurations**
```bash
# Test with different config file
python main.py --config config/my_custom_config.json --generate-now
```

---

## 🔧 Development Workflow

### Daily Testing Workflow:

```bash
# 1. Start your day
cd autoBlogger
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Run quick test
python test_setup.py

# 3. Generate test article
python main.py --generate-now

# 4. Check output
ls output/
cat output/*.html  # View generated article

# 5. Run full test suite
pytest

# 6. Check logs if needed
tail -f logs/autoblogger.log
```

### Testing New Features:

```bash
# 1. Write your code
# 2. Write tests for it
# 3. Run tests
pytest tests/unit/test_your_feature.py -v

# 4. Test manually
python main.py --generate-now

# 5. Check results
ls output/
```

---

## 🚀 Available Commands

### Main Commands:
```bash
# Generate article immediately
python main.py --generate-now

# Generate for specific blog
python main.py --generate-now --blog blog_001

# List all configured blogs
python main.py --list-blogs

# Dry run (preview without publishing)
python main.py --generate-now --dry-run

# Use custom config file
python main.py --config my_config.json --generate-now
```

### Testing Commands:
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test
pytest tests/unit/test_content_generator.py::TestContentGenerator::test_generate_article_basic -v

# Run integration tests only
pytest tests/integration/ -v

# Run with verbose output
pytest -v --tb=long
```

### Debug Commands:
```bash
# Check configuration
python -c "from src.utils import load_config; print(load_config('config/settings.json'))"

# Test AI provider
python -c "
import asyncio
from src.content_generator import MockAIProvider
async def test():
    provider = MockAIProvider()
    content = await provider.generate_content('Write about gardening')
    print(content[:100])
asyncio.run(test())
"

# Test file publisher
python -c "
import asyncio
from src.publishers.file_publisher import FilePublisher
from src.models import Article
from datetime import datetime
async def test():
    publisher = FilePublisher('test_output')
    article = Article(id='test', title='Test', content='Test content', 
                     meta_description='Test', keywords=['test'], word_count=10,
                     blog_id='test', created_at=datetime.now())
    response = await publisher.publish(article)
    print(f'Success: {response.success}')
asyncio.run(test())
"
```

---

## 📊 What to Test

### 1. **Core Functionality**
- [ ] Content generation works
- [ ] File publishing works
- [ ] Configuration loading works
- [ ] Error handling works

### 2. **Content Quality**
- [ ] Articles are coherent and readable
- [ ] Titles are appropriate
- [ ] Meta descriptions are good
- [ ] Keywords are included naturally

### 3. **File Output**
- [ ] HTML files are well-formatted
- [ ] Markdown files are readable
- [ ] Files contain correct content
- [ ] Filenames are sanitized

### 4. **Error Scenarios**
- [ ] Handles missing API keys gracefully
- [ ] Handles network failures
- [ ] Handles invalid configuration
- [ ] Handles file system errors

### 5. **Performance**
- [ ] Articles generate in reasonable time (<60 seconds)
- [ ] Memory usage is reasonable
- [ ] No memory leaks during batch processing

---

## 🐛 Debugging

### Check Logs:
```bash
# View recent logs
tail -f logs/autoblogger.log

# Search for errors
grep -i error logs/autoblogger.log

# Search for specific blog
grep "blog_001" logs/autoblogger.log
```

### Debug Mode:
```bash
# Set debug logging
export LOG_LEVEL=DEBUG
python main.py --generate-now
```

### Test Individual Components:
```bash
# Test just the AI provider
python -c "
import asyncio
from src.content_generator import MockAIProvider
async def test():
    provider = MockAIProvider()
    content = await provider.generate_content('Write about technology')
    print('Content length:', len(content))
    print('First 200 chars:', content[:200])
asyncio.run(test())
"

# Test just the file publisher
python -c "
import asyncio
from src.publishers.file_publisher import FilePublisher
from src.models import Article
from datetime import datetime
async def test():
    publisher = FilePublisher('test_output')
    article = Article(
        id='test', title='Test Article', 
        content='# Test\n\nThis is a test article.',
        meta_description='Test description',
        keywords=['test'], word_count=10,
        blog_id='test', created_at=datetime.now()
    )
    response = await publisher.publish(article)
    print('Publish success:', response.success)
    print('Files created:', list(Path('test_output').glob('*')))
asyncio.run(test())
"
```

---

## 🎯 Success Criteria

### Basic Functionality:
- [ ] `python test_setup.py` passes all tests
- [ ] `python main.py --generate-now` creates files in `output/`
- [ ] Generated articles are readable and coherent
- [ ] HTML files open properly in browser
- [ ] Markdown files are well-formatted

### Advanced Testing:
- [ ] `pytest` shows 80%+ coverage
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] Error scenarios handled gracefully
- [ ] Performance is acceptable

---

## 🚨 Common Issues

### "Python not found"
**Solution**: Make sure Python is installed and in PATH
```bash
# Check Python version
python --version
# or
python3 --version
```

### "Module not found"
**Solution**: Make sure you're in the right directory and virtual environment is activated
```bash
# Check current directory
pwd
# Should show: /path/to/autoBlogger

# Check virtual environment
which python
# Should show: /path/to/autoBlogger/venv/bin/python
```

### "Configuration not found"
**Solution**: Create the configuration file
```bash
cp config/settings.example.json config/settings.json
```

### "No output files created"
**Solution**: Check permissions and directory
```bash
# Check output directory exists and is writable
ls -la output/
# Create if needed
mkdir -p output
```

---

## 🎉 Testing Checklist

Before considering AutoBlogger "working":

- [ ] `python test_setup.py` passes
- [ ] `python main.py --generate-now` works
- [ ] Files appear in `output/` directory
- [ ] Generated content is readable
- [ ] `pytest` passes with good coverage
- [ ] Logs are being written to `logs/autoblogger.log`
- [ ] Error handling works (try with invalid config)
- [ ] Multiple articles can be generated
- [ ] Different blog configurations work

---

## 🚀 Next Steps After Testing

Once testing passes:

1. **Get real API keys** (Gemini, Unsplash)
2. **Switch from mock to real AI**
3. **Add image generation**
4. **Set up auto-publishing**
5. **Build web dashboard** (then you'll need a dev server!)

---

**Remember: AutoBlogger is a CLI tool, not a web app. Test it by running commands, not by opening a browser! 🎯**
