# Cursor Prompt Templates

These are pre-written prompts for common development tasks. Copy and paste these into Cursor, filling in the bracketed placeholders.

---

## 1. New API Endpoint

```
Create a new API endpoint with the following requirements:

**Endpoint Details:**
- Route: [e.g., POST /api/users]
- Purpose: [describe what this endpoint does]
- Authentication: [required/public]

**Requirements:**
- Feature flag: feature_[name] (default OFF in production)
- Input validation: [describe expected input schema]
- Response format: [describe response structure]
- Error handling: [list expected error cases]
- Performance target: <500ms p95

**Provide:**
1. Complete implementation following existing API patterns
2. Feature flag setup code
3. Unit tests
4. One e2e @happy-path test
5. Input validation schema (using existing validation library)
6. Performance validation approach
7. API documentation snippet

**Safety checks:**
- Ensure backward compatibility
- Add rate limiting if endpoint could be abused
- Include proper logging with traceId (no PII)
```

---

## 2. Database Migration

```
Create a database migration for: [describe the change]

**Requirements:**
- Migration must be ADDITIVE ONLY (no column drops, renames, or type changes)
- Include rollback migration
- Test against staging data simulation
- Verify all existing queries will continue to work
- Document in CHANGELOG.md

**What I need:**
1. Up migration file (additive changes only)
2. Down migration file (safe rollback)
3. List of affected queries/models
4. Testing approach for staging
5. Verification that existing code won't break

**If the change requires removing/modifying:**
- Explain the multi-step approach (add new, migrate data, deprecate old)
- Create migration plan with timeline
```

---

## 3. New React Component

```
Create a new React component: [ComponentName]

**Component Purpose:**
[Describe what this component does and where it will be used]

**Requirements:**
- Follow existing component patterns in [directory]
- Use existing design system/component library
- Match styling approach of similar components
- Ensure accessibility (WCAG 2.1 AA)
- Responsive design
- TypeScript with proper prop types

**Props needed:**
- [prop1]: [type] - [description]
- [prop2]: [type] - [description]

**Provide:**
1. Component implementation
2. Unit tests (using existing test framework)
3. Storybook story (if project uses Storybook)
4. Usage example
5. Accessibility verification notes

**Feature flag:**
[yes/no - if yes, specify flag name]
```

---

## 4. Refactor Existing Code

```
Refactor the following code/module: [file path or description]

**Current issues:**
- [Issue 1]
- [Issue 2]
- [Issue 3]

**Goals:**
- [Goal 1: e.g., improve performance]
- [Goal 2: e.g., better type safety]
- [Goal 3: e.g., reduce complexity]

**Constraints:**
- Maintain backward compatibility
- Preserve all existing functionality
- Keep existing tests passing (or update them appropriately)
- Improve test coverage if currently below 80%

**Approach:**
1. Show me the refactoring plan BEFORE implementing
2. Explain trade-offs of your approach
3. Identify any risks
4. Propose how to verify nothing breaks

**Provide:**
- Refactored code
- Updated tests
- Migration guide if API changes
- Performance comparison (before/after)
```

---

## 5. Bug Fix

```
Fix bug: [describe the bug]

**Current behavior:**
[What's happening now]

**Expected behavior:**
[What should happen]

**Root cause (if known):**
[Your hypothesis or known cause]

**Requirements:**
- Identify root cause if not already known
- Fix without breaking existing functionality
- Add test that would have caught this bug
- Ensure similar bugs can't happen elsewhere
- Document in CHANGELOG.md

**Provide:**
1. Root cause analysis
2. Fix implementation (minimal change)
3. Regression test
4. Verification approach
5. Recommendations to prevent similar bugs

**If this requires a hotfix to production:**
- Mark as urgent
- Include immediate rollback plan
- Plan for follow-up PR with full review
```

---

## 6. Performance Optimization

```
Optimize performance of: [component/endpoint/query]

**Current performance:**
[e.g., p95: 1200ms, or "slow rendering on large lists"]

**Target performance:**
[e.g., p95: <500ms, or "smooth 60fps scrolling"]

**Requirements:**
1. Profile FIRST to identify actual bottlenecks
2. Provide before/after benchmarks
3. Maintain functionality (no behavior changes)
4. Add performance monitoring/logging

**Approach:**
1. Show profiling results and bottleneck analysis
2. Propose optimization strategy with trade-offs
3. Implement changes incrementally
4. Verify each optimization with benchmarks
5. Re-run full test suite

**Provide:**
- Profiling evidence (before)
- Optimized implementation
- Benchmark results (after)
- Explanation of optimization techniques used
- Any trade-offs made
```

---

## 7. Add Feature Flag

```
Add feature flag for existing feature: [feature name]

**Feature scope:**
[Describe what code should be behind the flag]

**Requirements:**
- Flag name: feature_[descriptive_name]
- Default: OFF in production
- ON in development/staging
- Create cleanup issue for 30 days from now

**Provide:**
1. Feature flag definition
2. Code changes to check flag
3. Configuration for dev/staging/prod
4. Testing approach for both flag states
5. Cleanup issue template
6. Documentation of flag behavior

**Gradual rollout plan:**
[How should this be rolled out? e.g., "10% users week 1, 50% week 2, 100% week 3"]
```

---

## 8. Security Enhancement

```
Implement security improvement: [describe improvement]

**Context:**
[Why is this needed? Threat model or compliance requirement]

**Requirements:**
- Follow existing security patterns
- No hardcoded secrets
- Input validation for all user data
- Proper error messages (no sensitive info leakage)
- Security logging (no PII)

**Provide:**
1. Implementation following security best practices
2. Security testing approach
3. Documentation of security model
4. Threat mitigation verification
5. Logging strategy

**Review checklist:**
- [ ] Input validation comprehensive
- [ ] No secrets in code
- [ ] Error messages safe
- [ ] Audit logging added
- [ ] Principle of least privilege applied
```

---

## 9. Integration with External Service

```
Integrate with external service: [service name]

**Service details:**
- API: [URL/documentation]
- Authentication: [method]
- Purpose: [what we're using it for]

**Requirements:**
- Behind feature flag (feature_[service_name]_integration)
- Proper error handling for service failures
- Retry logic with exponential backoff
- Circuit breaker pattern
- Comprehensive logging (no secrets)
- Timeout configuration

**Provide:**
1. Service client implementation
2. Configuration management (env vars)
3. Error handling and retry logic
4. Circuit breaker/fallback strategy
5. Monitoring/alerting recommendations
6. Unit and integration tests
7. Documentation

**Testing approach:**
- Mock service for unit tests
- Sandbox/test environment for integration tests
```

---

## 10. Documentation Update

```
Update documentation for: [component/API/feature]

**What changed:**
[Describe the changes that need documentation]

**Documentation needed:**
- [ ] README.md
- [ ] API documentation
- [ ] Inline code comments
- [ ] Architecture Decision Record (ADR)
- [ ] CHANGELOG.md
- [ ] .env.example
- [ ] Other: [specify]

**Audience:**
[Who will read this? Developers, end users, ops team?]

**Requirements:**
- Clear, concise language
- Code examples where appropriate
- Cover edge cases and gotchas
- Migration guide if breaking changes
- Link to related documentation

**Provide:**
Complete documentation updates following existing doc structure and style.
```

---

## 11. Test Coverage Improvement

```
Improve test coverage for: [file/module/feature]

**Current coverage:**
- Lines: [X%]
- Branches: [X%]

**Target coverage:**
- Lines: >80%
- Branches: >70%

**Requirements:**
- Use existing test framework and patterns
- Focus on critical paths first
- Include edge cases and error conditions
- Integration tests for user workflows
- Performance test if applicable

**Provide:**
1. Test plan (what will be tested)
2. Test implementation
3. Coverage report
4. Identification of any untestable code (why?)

**Priority areas:**
- [ ] Authentication/authorization
- [ ] Data mutations
- [ ] Payment flows
- [ ] Critical user journeys
- [ ] Error handling
```

---

## 12. Dependency Update

```
Update dependency: [package name]

**Current version:** [X.X.X]
**Target version:** [X.X.X]

**Reason for update:**
[Security patch, new features needed, maintenance, etc.]

**Requirements:**
- Review CHANGELOG of dependency
- Check for breaking changes
- Update code if API changed
- Run full test suite
- Check bundle size impact
- Verify in staging before production

**Provide:**
1. List of breaking changes (if any)
2. Required code updates
3. Test results
4. Bundle size comparison
5. Migration guide if needed

**Risk assessment:**
- Breaking changes: [yes/no]
- Security implications: [none/low/high]
- Testing coverage: [adequate/needs more]
```

---

## Usage Instructions

1. Copy the relevant template
2. Fill in all [bracketed placeholders]
3. Remove any sections not applicable
4. Paste into Cursor with your context
5. Let Cursor reference the global rules automatically

**Tips:**
- Be specific in your requirements
- Reference existing patterns when possible
- Always ask for tests
- Request explanation of approach for complex changes
- Ask Cursor to show the plan before implementing large changes

