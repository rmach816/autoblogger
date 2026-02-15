# Quick Start Reference Card

**Print this page and keep it at your desk!**

---

## ⚡ 5-MINUTE INSTALLATION

```bash
# 1. Go to your project
cd /path/to/your/project

# 2. Run installer
./install-tooling.sh

# 3. Install dependencies
npm install --save-dev @commitlint/cli @commitlint/config-conventional

# 4. Test it works
git commit -m "test: verify tooling"

# Done! 🎉
```

---

## 🚦 BEFORE CODING CHECKLIST

```
□ User-facing change? → Create feature flag
□ Database change? → Additive migration only
□ >50 lines? → Ask Cursor for plan first
□ New dependency? → Check existing first
```

---

## ✅ BEFORE COMMIT CHECKLIST

```
□ Tests written (unit + e2e @happy-path)
□ No secrets in code
□ TypeScript strict (no `any`)
□ Performance OK (<500ms p95)
□ Docs updated (README, CHANGELOG)
□ Migration tested (if applicable)
```

---

## 🚨 RED LINES (NEVER)

```
❌ Edit past migrations
❌ Commit .env.local
❌ Remove working tests
❌ Rewrite working code
❌ Add dependencies casually
❌ Use `any` without justification
```

---

## ⚡ PERFORMANCE TARGETS

```
Critical (auth, checkout)  <200ms p95
Standard APIs             <500ms p95
Background jobs           <5s p95
Analytics queries         <10s p95
```

---

## 📝 COMMIT FORMAT

```
type(scope): description

Examples:
  feat(auth): add SSO login
  fix(api): handle null pointer
  perf(db): add index to email
```

---

## 💬 CURSOR PROMPTS

**Instead of:**
> "Create an API endpoint"

**Use template:**
```
Create a new API endpoint with:
- Route: [POST /api/users]
- Feature flag: feature_[name]
- Input validation: [schema]
- Response format: [spec]
- Performance: <500ms p95
- Tests: unit + e2e @happy-path
```

**Find all templates:**
```bash
cat docs/cursor_prompt_templates.md
```

---

## 🔧 QUICK COMMANDS

```bash
# Test pre-commit manually
.git/hooks/pre-commit

# Check coverage
npm test -- --coverage

# View rules
cat .cursor/rules.md

# View prompts
cat docs/cursor_prompt_templates.md

# Create ADR
cp docs/adr/template.md docs/adr/$(date +%Y%m%d)-title.md
```

---

## 🆘 WHEN IN DOUBT

```
1. Check existing patterns first
2. Ask Cursor to show plan
3. Feature flag it
4. Extend, don't replace
5. Read .cursor/rules.md
```

---

## 🔥 EMERGENCY HOTFIX

**Production DOWN?**
```
✓ Skip feature flag
✓ Skip review (tests still required!)
✓ Deploy immediately

Must do within 24h:
✓ Create incident ticket
✓ Full PR with review
✓ Post-mortem
```

---

## 📋 DECISION MATRIX

| What | Flag? | Migration? | Tests? |
|------|-------|------------|--------|
| New UI | ✅ Yes | ❌ No | Unit+E2E |
| Bug fix | ❌ No | ❌ No | Regression |
| New API | ✅ Yes | Maybe | Unit+E2E |
| Schema | ✅ Yes | ✅ Yes | Unit+Int |

---

## 📞 FILES LOCATION

```
Rules:           .cursor/rules.md
Pre-commit:      .git/hooks/pre-commit
PR Template:     .github/pull_request_template.md
CI Pipeline:     .github/workflows/ci-validation.yml
Prompts:         docs/cursor_prompt_templates.md
Quick Ref:       docs/DECISION_FLOWCHART.md
Tech Debt:       docs/tech-debt.md
```

---

## 🐛 TROUBLESHOOTING

**Pre-commit not running?**
```bash
chmod +x .git/hooks/pre-commit
```

**Cursor not following rules?**
```bash
cat .cursor/rules.md  # Verify exists
# Restart Cursor IDE
```

**CI failing?**
```bash
npm run lint
npm run type-check
npm test -- --coverage
```

**Too strict?**
```bash
# Edit rules
nano .cursor/rules.md

# Or bypass pre-commit (not recommended)
git commit --no-verify
```

---

## 📊 WEEKLY CHECKLIST

```
□ Check for stale feature flags
□ Review tech debt (docs/tech-debt.md)
□ Update dependencies (npm outdated)
□ Review CHANGELOG
```

---

## 🎯 REMEMBER

**EXTEND, DON'T REPLACE**
If it works, add to it.

**FEATURE FLAG EVERYTHING**
Better safe than sorry.

**TEST EVERYTHING**
If you wrote it, test it.

**DOCUMENT DECISIONS**
Future you will thank you.

---

═══════════════════════════════════════════════

        🎯 GOAL: PRODUCTION-GRADE CODE
        
     Every commit makes the codebase better
     Every PR is mergeable without fear
     Every deployment is reversible

═══════════════════════════════════════════════

**More help:** 
- Implementation Guide: `IMPLEMENTATION_GUIDE.md`
- Full reference: `TOOLING_README.md`
- Flowchart: `DECISION_FLOWCHART.md`

**Version:** 2.0 | **Updated:** Oct 2025
