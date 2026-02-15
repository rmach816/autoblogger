# AutoBlogger-Specific Cursor Rules
## *Production-Grade AI-Powered Blog Generator Development Standards*

These rules apply specifically to the **AutoBlogger project** - an AI-powered blog generator that creates unique, SEO-optimized content with professional images. This document extends the global rules with AutoBlogger-specific requirements and constraints.

---

## **PROJECT CONTEXT**

- **Project Type:** AI-Powered Content Generation SaaS
- **Performance Targets:** Article generation < 10s, API response < 500ms, UI load < 2s
- **Constraints:** Real AI integration required, unique content generation mandatory, production-ready architecture
- **Critical Functionality:** Unique article generation, full article viewing, real AI API integration, responsive UI

---

## **AUTOBLOGGER-SPECIFIC RULES**

### **1. AI Content Generation Safety**

**Content Uniqueness Enforcement:**
- **NEVER** generate duplicate content - every article must be unique
- **ALWAYS** validate topic-specific content generation before saving
- **REQUIRED:** Implement content variation mechanisms (timestamps, topic-specific prompts, keyword variations)
- **MANDATORY:** Test content uniqueness with multiple articles on same topic

**AI API Integration Standards:**
- **PRIMARY:** Use Google Generative AI (Gemini) as main AI service
- **FALLBACK:** Implement robust fallback content generation (not mock data)
- **ERROR HANDLING:** Graceful degradation when AI APIs fail
- **RATE LIMITING:** Implement proper rate limiting for AI API calls
- **COST CONTROL:** Monitor and limit AI API usage to prevent runaway costs

**Content Quality Validation:**
- **REQUIRED:** Validate generated content matches input topic
- **MANDATORY:** Ensure proper markdown formatting in generated content
- **ENFORCED:** Check for appropriate word count compliance
- **VALIDATED:** Verify SEO optimization elements are present

### **2. Article Management Safety**

**Database Integrity:**
- **UNIQUE CONSTRAINTS:** Enforce unique slugs with timestamp suffixes
- **DATA VALIDATION:** Validate all article fields before database operations
- **RELATIONSHIPS:** Maintain proper article-image relationships
- **BACKUP:** Implement article content backup before any modifications

**Article Viewing Requirements:**
- **FULL CONTENT:** Complete article content must be viewable in modal
- **RESPONSIVE:** Article viewer must work on all screen sizes
- **ACCESSIBILITY:** Proper ARIA labels and keyboard navigation
- **PERFORMANCE:** Article loading must be < 2 seconds

### **3. Frontend UI Standards**

**Component Architecture:**
- **REACT 19:** Use latest React features and patterns
- **TYPESCRIPT:** Strict typing for all components and props
- **TAILWIND CSS 4.1.16:** Use latest utility-first CSS framework
- **RESPONSIVE:** Mobile-first design approach

**User Experience Requirements:**
- **INTUITIVE:** Clear navigation and user flows
- **FEEDBACK:** Loading states, success/error messages
- **ACCESSIBILITY:** WCAG 2.1 AA compliance
- **PERFORMANCE:** Smooth animations and transitions

### **4. API Design Standards**

**RESTful API Patterns:**
- **CONSISTENT:** Follow REST conventions for all endpoints
- **VERSIONED:** API versioning for future compatibility
- **DOCUMENTED:** OpenAPI/Swagger documentation
- **TESTED:** Comprehensive API testing

**Error Handling:**
- **TYPED ERRORS:** Structured error responses
- **HTTP CODES:** Appropriate HTTP status codes
- **LOGGING:** Comprehensive request/response logging
- **MONITORING:** Error tracking and alerting

### **5. Testing Requirements**

**Content Generation Testing:**
- **UNIQUENESS TESTS:** Verify no duplicate content generation
- **TOPIC RELEVANCE:** Validate content matches input topics
- **AI INTEGRATION:** Test real AI API integration
- **FALLBACK TESTING:** Verify fallback content generation

**End-to-End Testing:**
- **ARTICLE GENERATION:** Complete article creation flow
- **ARTICLE VIEWING:** Full article display functionality
- **UI INTERACTIONS:** All user interface interactions
- **ERROR SCENARIOS:** Network failures, API errors, validation failures

**Performance Testing:**
- **LOAD TESTING:** Multiple concurrent article generations
- **STRESS TESTING:** High-volume content generation
- **MEMORY TESTING:** Long-running session stability
- **API PERFORMANCE:** Response time validation

### **6. Security Standards**

**AI API Security:**
- **API KEY PROTECTION:** Secure storage and rotation of AI API keys
- **RATE LIMITING:** Prevent API abuse and cost overruns
- **INPUT SANITIZATION:** Validate and sanitize all user inputs
- **OUTPUT FILTERING:** Filter potentially harmful AI-generated content

**Data Protection:**
- **ENCRYPTION:** Encrypt sensitive data at rest and in transit
- **ACCESS CONTROL:** Implement proper authentication and authorization
- **AUDIT LOGGING:** Log all content generation activities
- **PRIVACY:** No PII in logs or error messages

### **7. Performance Optimization**

**Content Generation Performance:**
- **CACHING:** Implement intelligent caching for repeated requests
- **STREAMING:** Stream content generation for better UX
- **OPTIMIZATION:** Optimize AI prompts for faster generation
- **MONITORING:** Real-time performance monitoring

**Database Performance:**
- **INDEXING:** Proper database indexes for query optimization
- **PAGINATION:** Implement efficient pagination for article lists
- **QUERY OPTIMIZATION:** Optimize database queries
- **CONNECTION POOLING:** Efficient database connection management

### **8. Deployment Standards**

**Production Readiness:**
- **DOCKER:** Containerized deployment with multi-stage builds
- **ENVIRONMENT:** Proper environment variable management
- **HEALTH CHECKS:** Comprehensive health monitoring
- **ROLLBACK:** Quick rollback capabilities

**Monitoring and Observability:**
- **METRICS:** Key performance indicators (KPIs)
- **ALERTING:** Proactive error and performance alerting
- **LOGGING:** Structured logging with correlation IDs
- **DASHBOARDS:** Real-time monitoring dashboards

### **9. Content Quality Assurance**

**AI Content Validation:**
- **TOPIC ALIGNMENT:** Verify content matches requested topic
- **SEO OPTIMIZATION:** Check for proper SEO elements
- **READABILITY:** Ensure content is readable and well-structured
- **FACTUAL ACCURACY:** Basic fact-checking for generated content

**User Experience Quality:**
- **UI CONSISTENCY:** Consistent design patterns throughout
- **ERROR MESSAGES:** Clear, helpful error messages
- **LOADING STATES:** Appropriate loading indicators
- **SUCCESS FEEDBACK:** Clear success confirmations

### **10. AutoBlogger-Specific Feature Flags**

**Content Generation Features:**
- `feature_ai_content_generation` - Enable/disable AI content generation
- `feature_fallback_content` - Enable/disable fallback content generation
- `feature_content_variation` - Enable/disable content variation mechanisms
- `feature_image_generation` - Enable/disable image generation

**UI/UX Features:**
- `feature_article_viewer` - Enable/disable article viewing modal
- `feature_article_export` - Enable/disable article export functionality
- `feature_bulk_generation` - Enable/disable bulk article generation
- `feature_content_preview` - Enable/disable content preview

### **11. AutoBlogger Error Handling**

**AI API Errors:**
- **API FAILURE:** Graceful fallback to alternative content generation
- **RATE LIMIT:** Queue requests and retry with backoff
- **INVALID RESPONSE:** Validate AI responses before processing
- **TIMEOUT:** Implement proper timeout handling

**Content Generation Errors:**
- **DUPLICATE DETECTION:** Prevent duplicate content generation
- **VALIDATION FAILURE:** Clear error messages for validation issues
- **STORAGE FAILURE:** Proper error handling for database operations
- **NETWORK FAILURE:** Retry mechanisms for network issues

### **12. AutoBlogger Performance Targets**

**Content Generation:**
- **Article Generation:** < 10 seconds per article
- **AI API Response:** < 5 seconds per request
- **Database Operations:** < 100ms per query
- **Image Generation:** < 15 seconds per image

**User Interface:**
- **Page Load Time:** < 2 seconds
- **Article Loading:** < 1 second
- **UI Responsiveness:** < 100ms for user interactions
- **Memory Usage:** < 512MB per user session

### **13. AutoBlogger Testing Checklist**

**Pre-Deployment Validation:**
- [ ] **Content Uniqueness:** Generate 10+ articles, verify all unique
- [ ] **AI Integration:** Test real AI API integration
- [ ] **Article Viewing:** Test complete article viewing functionality
- [ ] **Error Handling:** Test all error scenarios
- [ ] **Performance:** Validate all performance targets
- [ ] **Security:** Complete security scan
- [ ] **Accessibility:** WCAG 2.1 AA compliance check
- [ ] **Cross-Browser:** Test on major browsers
- [ ] **Mobile:** Test on mobile devices
- [ ] **Load Testing:** High-volume content generation test

### **14. AutoBlogger Code Quality Standards**

**TypeScript Requirements:**
- **STRICT MODE:** Enable strict TypeScript compilation
- **INTERFACE DEFINITIONS:** Define interfaces for all data structures
- **TYPE SAFETY:** No `any` types without explicit justification
- **NULL SAFETY:** Proper null/undefined handling

**React Best Practices:**
- **FUNCTIONAL COMPONENTS:** Use functional components with hooks
- **PROPER PROPS:** Type all component props
- **STATE MANAGEMENT:** Use appropriate state management patterns
- **EFFECT CLEANUP:** Proper cleanup in useEffect hooks

**API Design:**
- **RESTFUL:** Follow REST API conventions
- **VERSIONING:** Implement API versioning
- **DOCUMENTATION:** Comprehensive API documentation
- **TESTING:** Complete API test coverage

### **15. AutoBlogger Deployment Checklist**

**Production Readiness:**
- [ ] **Environment Variables:** All required env vars configured
- [ ] **Database Migrations:** All migrations applied
- [ ] **AI API Keys:** Valid API keys configured
- [ ] **Security Headers:** Security headers implemented
- [ ] **Rate Limiting:** Rate limiting configured
- [ ] **Monitoring:** Monitoring and alerting setup
- [ ] **Backup Strategy:** Data backup strategy implemented
- [ ] **Health Checks:** Health check endpoints working
- [ ] **Performance Monitoring:** Performance monitoring active
- [ ] **Error Tracking:** Error tracking configured

---

## **AUTOBLOGGER-SPECIFIC VALIDATION QUESTIONS**

Before providing any code, verify:

**Content Generation:**
- Will this generate unique content for different topics?
- Does this properly handle AI API failures?
- Is content validation implemented?
- Are fallback mechanisms in place?

**Article Management:**
- Does this maintain data integrity?
- Is the article viewing functionality complete?
- Are proper error messages provided?
- Is performance optimized?

**User Experience:**
- Is the UI responsive and accessible?
- Are loading states properly implemented?
- Is error handling user-friendly?
- Are success messages clear?

**System Integration:**
- Does this integrate properly with existing patterns?
- Are API endpoints consistent?
- Is database schema properly maintained?
- Are security measures in place?

---

## **AUTOBLOGGER SUCCESS CRITERIA**

**Functional Requirements:**
- ✅ **Unique Content Generation:** Every article is unique and topic-specific
- ✅ **Real AI Integration:** Actual AI APIs working, not mock data
- ✅ **Full Article Viewing:** Complete article content display
- ✅ **Responsive UI:** Works on all devices and screen sizes
- ✅ **Error Handling:** Graceful error handling for all scenarios

**Performance Requirements:**
- ✅ **Article Generation:** < 10 seconds per article
- ✅ **API Response:** < 500ms for all endpoints
- ✅ **UI Load Time:** < 2 seconds for page loads
- ✅ **Database Queries:** < 100ms for all queries

**Quality Requirements:**
- ✅ **Test Coverage:** 80%+ code coverage
- ✅ **E2E Testing:** Complete end-to-end test coverage
- ✅ **Security Scan:** No high/critical vulnerabilities
- ✅ **Accessibility:** WCAG 2.1 AA compliance

---

**This document ensures AutoBlogger development maintains the highest standards while addressing the unique requirements of AI-powered content generation. Every line of code must contribute to creating a production-ready, user-friendly, and technically excellent blog generation platform.**
