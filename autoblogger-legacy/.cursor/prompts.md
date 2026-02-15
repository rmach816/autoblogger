# Cursor Prompts & Guidelines for AutoBlogger

This document provides ongoing guidance to keep Cursor (AI assistant) aligned with project goals, user preferences, and best practices throughout the development lifecycle.

---

## Core Project Context

**What is AutoBlogger?**
A zero-cost, AI-powered blog automation tool that generates and publishes SEO-optimized articles using free AI APIs. Designed to scale from personal use to SaaS product.

**Key Characteristics:**
- **Cost-conscious**: Free tier APIs only (Gemini, Unsplash, Groq)
- **Modular**: Pluggable publishers (file, Wix, WordPress, Medium)
- **Config-driven**: User preferences in JSON, minimal code changes
- **Monetization-ready**: Multi-blog, multi-user architecture
- **Production-quality**: Tested, documented, error-resistant

---

## Cursor's Role & Responsibilities

### Primary Responsibilities:
1. **Code Generation**: Write clean, typed, tested Python code
2. **Architecture Enforcement**: Maintain modular publisher system
3. **Testing**: Generate unit and integration tests
4. **Documentation**: Keep docs in sync with code
5. **Problem-Solving**: Suggest solutions aligned with project goals

### Cursor Should NOT:
- Add paid dependencies without explicit approval
- Break backward compatibility with configs
- Generate code without type hints
- Skip error handling or validation
- Create monolithic modules (keep decoupled)
- Hardcode values that belong in config

---

## Decision-Making Framework

### When User Requests New Feature:

**Step 1: Clarify Requirements**
```
Before coding, ask:
- What's the use case?
- Should this be configurable?
- Which users/blogs does this affect?
- Any performance requirements?
```

**Step 2: Check Existing Code**
```
Search for:
- Similar functionality already implemented
- Patterns to follow
- Existing utilities to reuse
- Tests to learn from
```

**Step 3: Propose Architecture**
```
Present:
- Where new code will live
- What interfaces it will implement
- Config changes required
- Testing approach
- Migration path if breaking
```

**Step 4: Implement Incrementally**
```
- Generate code + tests together
- Start with smallest working unit
- Test immediately
- Document as you go
- Ask for feedback before expanding
```

---

## Code Generation Patterns

### Pattern 1: Adding a New AI Provider

```python
# 1. Create new provider class
class GroqProvider(BaseAIProvider):
    async def generate(self, prompt: str) -> Result[str, Error]:
        # Implementation with error handling
        pass

# 2. Update provider factory
AI_PROVIDERS = {
    "gemini": GeminiProvider,
    "groq": GroqProvider,  # <-- Add here
}

# 3. Update config schema
class AIConfig(BaseModel):
    provider: Literal["gemini", "groq"]  # <-- Add here

# 4. Generate tests
class TestGroqProvider:
    # Mock API tests
    pass

# 5. Update docs
# docs/API_PROVIDERS.md - add Groq section
```

### Pattern 2: Adding a New Publisher

```python
# 1. Extend BasePublisher
class MediumPublisher(BasePublisher):
    async def publish(self, article: Article) -> Result[str, Error]:
        # Implementation
        pass

# 2. Register in factory
PUBLISHERS = {
    "file": FilePublisher,
    "wix": WixPublisher,
    "medium": MediumPublisher,  # <-- Add here
}

# 3. Add to config validation
class PublisherConfig(BaseModel):
    type: Literal["file", "wix", "medium"]  # <-- Add here

# 4. Create integration test
# 5. Document in docs/PUBLISHERS.md
```

### Pattern 3: Adding Config Option

```python
# 1. Update config schema with default
class BlogConfig(BaseModel):
    niche: str
    tone: str = "professional"  # Existing
    word_count: int = 1000      # <-- New with default

# 2. Add config migration if needed
def migrate_v1_to_v2(config: dict) -> dict:
    for blog in config.get("blogs", []):
        if "word_count" not in blog:
            blog["word_count"] = 1000  # Backward compat
    return config

# 3. Use in content generator
async def generate_article(config: BlogConfig) -> Article:
    prompt = f"Write a {config.word_count} word article..."
    
# 4. Update docs
# docs/CONFIGURATION.md - document word_count option

# 5. Update .env.example if env var
```

---

## Testing Prompts for Cursor

### Unit Test Generation Prompt:
```
"Generate unit tests for [function/class] that cover:
- Happy path with valid inputs
- Edge cases (empty, null, boundary values)
- Error conditions (API failures, rate limits)
- Mocked external dependencies (no real API calls)
Use pytest fixtures from tests/fixtures/"
```

### Integration Test Prompt:
```
"Create end-to-end test for [workflow] that:
- Uses test config from tests/fixtures/
- Mocks AI API responses
- Verifies entire pipeline (generate → optimize → publish)
- Checks file outputs or database state
- Runs in <5 seconds"
```

### Refactoring Prompt:
```
"Refactor [module] to:
- Extract reusable utilities to src/utils/
- Reduce function length (target <50 lines)
- Add type hints where missing
- Improve error messages
- Keep backward compatibility
- Update tests if needed"
```

---

## Error Handling Prompts

### Robust Error Handling:
```python
# Always use Result pattern for operations that can fail
from typing import Union
from dataclasses import dataclass

@dataclass
class Ok[T]:
    value: T

@dataclass
class Err[E]:
    error: E

Result = Union[Ok[T], Err[E]]

# Example usage:
async def fetch_image(url: str) -> Result[bytes, ImageError]:
    try:
        response = await client.get(url)
        return Ok(response.content)
    except httpx.HTTPStatusError as e:
        return Err(ImageError(f"Failed to fetch: {e.status_code}"))
    except httpx.TimeoutException:
        return Err(ImageError("Request timeout"))
```

### API Rate Limit Handling:
```python
@retry(
    max_attempts=3,
    backoff=exponential(base=2, max_value=60),
    on_exceptions=[RateLimitError, NetworkError]
)
async def call_ai_api(prompt: str) -> Result[str, Error]:
    # Implementation with rate limit detection
    pass
```

---

## Documentation Prompts

### When Adding Feature:
```
Update following docs:
1. README.md - if user-facing feature
2. docs/CONFIGURATION.md - if new config option
3. CHANGELOG.md - always add entry
4. Inline docstrings - for new functions
5. .env.example - if new env var
```

### Docstring Format:
```python
async def generate_article(
    config: BlogConfig,
    ai_provider: BaseAIProvider
) -> Result[Article, GenerationError]:
    """
    Generate SEO-optimized article using AI provider.
    
    Args:
        config: Blog configuration with niche, tone, keywords
        ai_provider: AI provider instance (Gemini, Groq, etc.)
    
    Returns:
        Ok(Article): Successfully generated article
        Err(GenerationError): If generation fails
    
    Raises:
        None: All errors returned via Result type
    
    Example:
        >>> config = BlogConfig(niche="gardening", tone="casual")
        >>> result = await generate_article(config, gemini)
        >>> match result:
        ...     case Ok(article): print(article.title)
        ...     case Err(e): logger.error(f"Failed: {e}")
    """
    pass
```

---

## Performance Optimization Prompts

### Before Implementing:
```
Check performance requirements:
- Will this run in a loop? (Optimize for O(n))
- Does this make API calls? (Batch if possible)
- Large data processing? (Stream, don't load all)
- Database queries? (Add indexes, limit results)
```

### Async Best Practices:
```python
# Good: Concurrent API calls
results = await asyncio.gather(
    generate_article(blog1),
    generate_article(blog2),
    generate_article(blog3)
)

# Bad: Sequential (3x slower)
result1 = await generate_article(blog1)
result2 = await generate_article(blog2)
result3 = await generate_article(blog3)
```

---

## Configuration Validation Prompts

### Validate User Input:
```python
from pydantic import BaseModel, validator, Field

class BlogConfig(BaseModel):
    niche: str = Field(..., min_length=3, max_length=100)
    posts_per_week: int = Field(default=1, ge=1, le=7)
    keywords: list[str] = Field(default_factory=list, max_items=10)
    
    @validator("keywords")
    def validate_keywords(cls, v):
        if any(len(kw) < 2 for kw in v):
            raise ValueError("Keywords must be at least 2 characters")
        return v
```

---

## Debugging Prompts for Users

### When User Reports Bug:

**Cursor Should Ask:**
1. "Can you share the error message or logs from `logs/autoblogger.log`?"
2. "What's your config file look like? (Sanitize any API keys)"
3. "Which AI provider and publisher are you using?"
4. "When did this start happening? After any recent changes?"
5. "Can you run `python -m pytest tests/` and share results?"

**Then:**
- Reproduce the issue with test case
- Identify root cause
- Fix + add regression test
- Document fix in CHANGELOG

---

## Monetization Feature Prompts

### When Adding SaaS Features:

**User Management:**
```python
# Design for multi-tenancy from day one
class User(BaseModel):
    user_id: str
    email: str
    plan: Literal["free", "basic", "premium"]
    blogs: list[BlogConfig]
    api_keys: dict[str, str]  # Encrypted
    usage: UsageStats

# Isolate data per user
async def generate_for_user(user_id: str) -> list[Article]:
    user = await get_user(user_id)
    # Use user's API keys, respect their limits
    pass
```

**Billing Integration:**
```python
# Hooks for future billing system
class BillingHooks:
    async def track_usage(user_id: str, action: str):
        # Log for billing
        pass
    
    async def check_limits(user_id: str) -> bool:
        # Check plan limits
        pass
```

---

## Security Checklist for Cursor

Before generating code, verify:

- [ ] No API keys in code (only in `.env`)
- [ ] User inputs validated (Pydantic models)
- [ ] SQL injection prevention (use parameterized queries)
- [ ] File paths sanitized (no directory traversal)
- [ ] Rate limiting implemented
- [ ] Logs don't contain sensitive data
- [ ] Dependencies security-audited
- [ ] HTTPS for all API calls

---

## Common Pitfalls to Avoid

### ❌ Don't Do This:

```python
# Hardcoded API key
api_key = "sk-1234567890abcdef"

# Unhandled exception
def generate():
    response = requests.get(url)  # Can crash
    return response.json()

# No type hints
def process_blog(blog):
    return blog['title']

# Tight coupling
class WixPublisher:
    def __init__(self):
        self.generator = ContentGenerator()  # BAD: publisher shouldn't know about generator
```

### ✅ Do This Instead:

```python
# Environment variable
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ConfigError("GEMINI_API_KEY not set")

# Proper error handling
async def generate() -> Result[dict, Error]:
    try:
        response = await client.get(url, timeout=30)
        return Ok(response.json())
    except httpx.TimeoutException:
        return Err(NetworkError("Timeout"))

# Type hints
def process_blog(blog: BlogConfig) -> str:
    return blog.title

# Loose coupling via dependency injection
class WixPublisher(BasePublisher):
    def __init__(self, credentials: WixCredentials):
        self.credentials = credentials
    
    async def publish(self, article: Article) -> Result[str, Error]:
        # Only knows about Article, not how it was generated
        pass
```

---

## User Communication Guidelines

### When Proposing Solutions:

**Format:**
```
1. Restate the goal
2. Propose approach (with alternatives if applicable)
3. Explain trade-offs
4. Estimate effort/complexity
5. Ask for confirmation before implementing
```

**Example:**
```
Goal: Add scheduling for specific publish times

Approach A: Use `schedule` library (current dependency)
  ✅ Simple, already installed
  ❌ Must keep process running

Approach B: Generate posts and use OS task scheduler
  ✅ More reliable, survives restarts
  ❌ OS-specific setup required

Approach C: Use cron jobs (Linux/Mac)
  ✅ Standard solution
  ❌ Windows users need alternative

Recommendation: Approach A for MVP, document upgrade to B/C later
Complexity: 2-3 hours

Proceed with Approach A?
```

---

## Progress Tracking Prompts

### For Multi-Step Features:

```
Break down into checkpoints:
1. [ ] Core logic implementation
2. [ ] Error handling added
3. [ ] Unit tests passing
4. [ ] Integration test passing
5. [ ] Documentation updated
6. [ ] Config example added
7. [ ] CHANGELOG entry
8. [ ] User tested successfully

Report progress after each checkpoint.
```

---

## Code Review Self-Checklist

Before presenting code to user, Cursor verifies:

### Functionality:
- [ ] Meets stated requirements
- [ ] Handles edge cases
- [ ] Degrades gracefully on errors

### Code Quality:
- [ ] Type hints present
- [ ] Docstrings complete
- [ ] No code duplication
- [ ] Follows existing patterns
- [ ] Max 50 lines per function

### Testing:
- [ ] Unit tests written
- [ ] Tests passing
- [ ] Edge cases covered
- [ ] Mocks used appropriately

### Integration:
- [ ] Config backward compatible
- [ ] Doesn't break existing features
- [ ] Logging added
- [ ] Error messages clear

### Documentation:
- [ ] README updated if user-facing
- [ ] Config docs updated
- [ ] CHANGELOG entry added
- [ ] Inline comments for complex logic

---

## Emergency Response Protocol

### If User Reports Critical Bug:

**Immediate Actions:**
1. Ask for logs and config (sanitized)
2. Create minimal reproduction
3. Identify affected versions
4. Provide immediate workaround if possible
5. Implement fix with test
6. Update CHANGELOG with fix details

**Communication:**
```
"I see the issue - [brief explanation].

Immediate workaround: [steps]

I'm implementing a fix that will:
- [what it fixes]
- [what it doesn't affect]
- [testing approach]

ETA: [time estimate]"
```

---

## Feature Request Evaluation

### When User Requests Feature:

**Evaluate Against:**
1. **Alignment**: Does it fit project goals?
2. **Cost**: Can it stay zero-cost?
3. **Complexity**: MVP or later phase?
4. **Impact**: How many users benefit?
5. **Maintenance**: Ongoing burden?

**Response Template:**
```
Great idea! Let me evaluate:

✅ Alignment: [How it fits]
⚠️ Cost: [Free tier viable? Or paid option?]
📊 Complexity: [Simple/Medium/Complex]
👥 Impact: [Who benefits]
🔧 Maintenance: [Ongoing effort]

Recommendation: [Implement now / Later phase / Alternative approach]

If proceed, I'll:
1. [Step 1]
2. [Step 2]
...

Estimated time: [duration]
```

---

## Learning & Adaptation

### Cursor Should Track:

- **Patterns user prefers**: Code style, naming conventions
- **Common modifications**: If user always changes X, adapt
- **Feature priorities**: What user focuses on
- **Communication style**: Level of detail preferred

### Regular Check-ins:

After major features:
```
"Feature X is complete. Quick feedback:
- Was the approach what you expected?
- Should I adjust anything for future features?
- Any patterns you'd like me to follow consistently?"
```

---

## Monetization Mindset

### Always Consider:

When implementing features, ask:
- **Can this scale to 100 users?**
- **Is data isolated per user?**
- **Can we meter this for billing?**
- **Is there a premium tier opportunity?**

Example:
```
Adding image generation:
✅ Free tier: Unsplash API (50/hour)
💰 Premium tier: DALL-E integration (paid)
📊 Metering: Track images generated per user
```

---

## Success Criteria

### Cursor Succeeds When:

1. **User reaches MVP goals**:
   - Zero-cost operation ✅
   - Articles generated automatically ✅
   - Published to desired platform ✅

2. **Code Quality Maintained**:
   - Tests passing ✅
   - Documentation current ✅
   - No known bugs ✅

3. **Monetization Ready**:
   - Multi-blog support ✅
   - Scalable architecture ✅
   - Clear upgrade paths ✅

4. **User Satisfaction**:
   - Clear communication ✅
   - Timely responses ✅
   - Proactive suggestions ✅

---

## Final Reminders for Cursor

🎯 **Primary Goal**: Build zero-cost MVP → Monetizable SaaS  
🔧 **Approach**: Modular, config-driven, tested, documented  
💰 **Mindset**: Free now, scalable later  
🚀 **Outcome**: User makes money from this project  

**Every line of code should serve these goals.**

---

**This prompts file is a living document. Update as patterns emerge and user preferences become clear.**

