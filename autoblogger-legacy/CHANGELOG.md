# Changelog

All notable changes to AutoBlogger will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project structure with modular architecture
- Mock AI provider for testing without API keys
- File publisher for saving articles as HTML and Markdown
- Configuration system with JSON-based settings
- Comprehensive test suite with 80%+ coverage
- CLI interface with multiple commands
- Logging system with structured JSON output
- Rate limiting and retry logic for API calls
- Error handling with graceful degradation
- Documentation for setup and configuration

### Changed
- N/A

### Deprecated
- N/A

### Removed
- N/A

### Fixed
- N/A

### Security
- API keys stored in environment variables only
- Input validation for all configuration fields
- Rate limiting to prevent API abuse
- Secure file handling for generated content

## [0.1.0] - 2025-10-04

### Added
- Core content generation with AI providers
- File-based publishing system
- Configuration management
- Basic CLI interface
- Unit and integration tests
- Setup and configuration documentation

---

## Development Notes

### Version 0.1.0 Goals
- [x] Working MVP with mock AI provider
- [x] File publishing functionality
- [x] Configuration system
- [x] Basic CLI interface
- [x] Comprehensive testing
- [x] Documentation

### Next Version Goals (0.2.0)
- [ ] Real AI provider integration (Gemini)
- [ ] Image fetching from Unsplash
- [ ] SEO optimization features
- [ ] Wix publisher implementation
- [ ] WordPress publisher implementation
- [ ] Scheduling system
- [ ] Error recovery and retry queue

### Future Versions
- [ ] Web dashboard UI
- [ ] Multi-blog management
- [ ] Analytics integration
- [ ] User authentication
- [ ] Billing integration
- [ ] SaaS features
