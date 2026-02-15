## Description
<!-- Provide a clear description of what this PR does -->



## Type of Change
<!-- Mark the relevant option with an 'x' -->

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Refactoring (code improvement without changing functionality)
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Security fix
- [ ] Dependency update
- [ ] Infrastructure/tooling change

## Checklist

### Code Quality
- [ ] Code follows existing patterns and conventions
- [ ] All variables are properly typed (no `any` without justification)
- [ ] Error handling is preserved/added
- [ ] This change is additive rather than destructive
- [ ] Existing tests still pass
- [ ] No hardcoded secrets or credentials

### Testing
- [ ] Unit tests added/updated
- [ ] End-to-end `@happy-path` test added (if applicable)
- [ ] Test coverage meets 80/70 floor (lines/branches)
- [ ] Manual testing completed

### Performance
- [ ] Database queries are optimized (indexes, LIMIT clauses)
- [ ] API responses meet SLA (<500ms p95 for standard endpoints)
- [ ] No N+1 queries introduced
- [ ] Performance evidence provided (see below)

### Security
- [ ] Input validation added/preserved
- [ ] No PII in logs or responses
- [ ] Rate limiting considered (if new endpoint)
- [ ] Authentication/authorization preserved
- [ ] Dependency security scan passed

### Documentation
- [ ] README updated (if needed)
- [ ] .env.example updated with new variables (if needed)
- [ ] CHANGELOG.md updated
- [ ] API documentation updated (if API changes)
- [ ] ADR created (if architectural change)
- [ ] Inline comments added for complex logic

### Feature Flags & Migrations
- [ ] Feature flag created (if user-facing change) - Default: OFF in prod
- [ ] Feature flag cleanup issue created: #____
- [ ] Migration is additive only (no drops/renames)
- [ ] Rollback migration provided (if schema change)
- [ ] Migration tested in staging

## Testing Evidence
<!-- Provide evidence that your changes work -->

### Unit Test Coverage
```
Lines   : XX% ( XXX/XXX )
Branches: XX% ( XXX/XXX )
```

### E2E Test Results
<!-- Link to test run or paste relevant output -->


### Manual Testing
<!-- Describe how you manually verified this works -->


## Performance Evidence
<!-- Provide benchmark data or explain why not applicable -->

**API Response Times (p95):**
- Endpoint: `/api/xxxx`
- Response time: XXXms
- Method: [local profiling / staging test / production sample]

**Database Query Performance:**
```sql
-- Include EXPLAIN output for complex queries
```

## Rollback Plan
<!-- How to undo this change if it causes issues in production -->

**Steps to rollback:**
1. 
2. 
3. 

**Rollback risks/considerations:**
- 

## Dependencies
<!-- List any dependencies this PR has -->

**Blocked by:**
- 

**Blocks:**
- 

**Related PRs:**
- 

## Breaking Changes
<!-- If this is a breaking change, explain the impact and migration path -->

**What breaks:**
- 

**Migration path:**
1. 
2. 

## Screenshots/Recordings
<!-- For UI changes, include before/after screenshots or recordings -->

**Before:**


**After:**


## Additional Notes
<!-- Any additional context, trade-offs, or decisions -->



---

## Reviewer Checklist
<!-- For the reviewer to complete -->

- [ ] Code follows project conventions and best practices
- [ ] Tests are comprehensive and meaningful
- [ ] Documentation is clear and complete
- [ ] Performance implications are acceptable
- [ ] Security considerations are addressed
- [ ] Breaking changes are properly documented
- [ ] Feature flag strategy is sound (if applicable)
- [ ] Migration is safe and tested (if applicable)

**Approval:** ✅ / ❌

**Feedback:**


