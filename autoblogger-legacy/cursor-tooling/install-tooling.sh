#!/bin/bash
# Installation script for Cursor project tooling
# Usage: ./install-tooling.sh [project-root-path]

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default to current directory if no argument provided
PROJECT_ROOT="${1:-.}"

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  Cursor Project Tooling Installation${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Verify we're in a git repository
if [ ! -d "$PROJECT_ROOT/.git" ]; then
  echo -e "${RED}❌ Error: Not a git repository${NC}"
  echo "   Initialize git first: git init"
  exit 1
fi

echo -e "${GREEN}✓${NC} Found git repository"

# Create necessary directories
echo ""
echo "📁 Creating directory structure..."

mkdir -p "$PROJECT_ROOT/.cursor"
mkdir -p "$PROJECT_ROOT/.github"
mkdir -p "$PROJECT_ROOT/docs"
mkdir -p "$PROJECT_ROOT/docs/adr"
mkdir -p "$PROJECT_ROOT/scripts"

echo -e "${GREEN}✓${NC} Directories created"

# Install Cursor rules
echo ""
echo "📋 Installing Cursor global rules..."

if [ -f "cursor_global_rules_v2.md" ]; then
  cp cursor_global_rules_v2.md "$PROJECT_ROOT/.cursor/rules.md"
  echo -e "${GREEN}✓${NC} Cursor rules installed → .cursor/rules.md"
else
  echo -e "${YELLOW}⚠${NC}  cursor_global_rules_v2.md not found in current directory"
  echo "   Place cursor_global_rules_v2.md in the same directory as this script"
fi

# Install pre-commit hook
echo ""
echo "🔨 Installing pre-commit hook..."

if [ -f "pre-commit" ]; then
  cp pre-commit "$PROJECT_ROOT/.git/hooks/pre-commit"
  chmod +x "$PROJECT_ROOT/.git/hooks/pre-commit"
  echo -e "${GREEN}✓${NC} Pre-commit hook installed → .git/hooks/pre-commit"
else
  echo -e "${YELLOW}⚠${NC}  pre-commit file not found in current directory"
fi

# Install PR template
echo ""
echo "📝 Installing PR template..."

if [ -f "pull_request_template.md" ]; then
  cp pull_request_template.md "$PROJECT_ROOT/.github/pull_request_template.md"
  echo -e "${GREEN}✓${NC} PR template installed → .github/pull_request_template.md"
else
  echo -e "${YELLOW}⚠${NC}  pull_request_template.md not found in current directory"
fi

# Install Cursor prompt templates
echo ""
echo "💬 Installing Cursor prompt templates..."

if [ -f "cursor_prompt_templates.md" ]; then
  cp cursor_prompt_templates.md "$PROJECT_ROOT/docs/cursor_prompt_templates.md"
  echo -e "${GREEN}✓${NC} Prompt templates installed → docs/cursor_prompt_templates.md"
else
  echo -e "${YELLOW}⚠${NC}  cursor_prompt_templates.md not found in current directory"
fi

# Create CHANGELOG if it doesn't exist
echo ""
echo "📄 Checking for CHANGELOG..."

if [ ! -f "$PROJECT_ROOT/CHANGELOG.md" ]; then
  cat > "$PROJECT_ROOT/CHANGELOG.md" << 'EOF'
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Project tooling and development guidelines

### Changed

### Deprecated

### Removed

### Fixed

### Security
EOF
  echo -e "${GREEN}✓${NC} CHANGELOG.md created"
else
  echo -e "${BLUE}ℹ${NC}  CHANGELOG.md already exists"
fi

# Create tech debt tracking file
echo ""
echo "📊 Creating tech debt tracker..."

if [ ! -f "$PROJECT_ROOT/docs/tech-debt.md" ]; then
  cat > "$PROJECT_ROOT/docs/tech-debt.md" << 'EOF'
# Technical Debt

This document tracks known technical debt in the project.

## Format
For each debt item:
- **Description:** What is the issue?
- **Impact:** How does it affect the project? (Low/Medium/High)
- **Effort:** Estimated effort to resolve (Small/Medium/Large)
- **Deadline:** When must this be resolved?
- **Owner:** Who is responsible?

---

## Current Debt Items

### Example: Legacy authentication flow
- **Description:** Authentication uses deprecated session-based approach
- **Impact:** High (security risk, hard to maintain)
- **Effort:** Large (3-5 days)
- **Deadline:** Q2 2025
- **Owner:** Backend team
- **Created:** 2025-01-15

---

## Recently Resolved

### Example: Removed redundant API calls
- **Resolved:** 2025-01-10
- **Resolution:** Implemented caching layer
- **Impact:** Reduced API calls by 60%
EOF
  echo -e "${GREEN}✓${NC} Tech debt tracker created → docs/tech-debt.md"
else
  echo -e "${BLUE}ℹ${NC}  docs/tech-debt.md already exists"
fi

# Create ADR template
echo ""
echo "📑 Creating ADR template..."

if [ ! -f "$PROJECT_ROOT/docs/adr/template.md" ]; then
  cat > "$PROJECT_ROOT/docs/adr/template.md" << 'EOF'
# [ADR-XXXX] [Title]

Date: YYYY-MM-DD

## Status
[Proposed | Accepted | Deprecated | Superseded by ADR-YYYY]

## Context
What is the issue that we're seeing that is motivating this decision or change?

## Decision
What is the change that we're proposing and/or doing?

## Consequences
What becomes easier or more difficult to do because of this change?

### Positive
-

### Negative
-

### Neutral
-

## Alternatives Considered
What other options did we consider?

### Alternative 1: [Name]
- **Pros:**
- **Cons:**
- **Why not chosen:**

### Alternative 2: [Name]
- **Pros:**
- **Cons:**
- **Why not chosen:**

## Implementation Plan
How will this decision be implemented?

1.
2.
3.

## Stakeholders
Who needs to be informed about this decision?

- [Name] - [Role] - [Why they care]

## References
- [Link to relevant documentation]
- [Link to related ADRs]
- [Link to related issues/PRs]
EOF
  echo -e "${GREEN}✓${NC} ADR template created → docs/adr/template.md"
else
  echo -e "${BLUE}ℹ${NC}  docs/adr/template.md already exists"
fi

# Create .gitignore additions
echo ""
echo "🚫 Checking .gitignore..."

GITIGNORE_ADDITIONS="
# Environment files
.env.local
.env.production
.env.*.local

# Secrets
secrets.json
credentials.json
*.key
.aws/credentials

# OS files
.DS_Store
Thumbs.db

# IDE
.vscode/settings.json
.idea/
*.swp
*.swo

# Logs
logs/
*.log
npm-debug.log*

# Coverage
coverage/
.nyc_output/

# Build artifacts
dist/
build/
out/
.next/
"

if [ -f "$PROJECT_ROOT/.gitignore" ]; then
  # Check if our patterns are already there
  if ! grep -q ".env.local" "$PROJECT_ROOT/.gitignore"; then
    echo "$GITIGNORE_ADDITIONS" >> "$PROJECT_ROOT/.gitignore"
    echo -e "${GREEN}✓${NC} Updated .gitignore"
  else
    echo -e "${BLUE}ℹ${NC}  .gitignore already contains required patterns"
  fi
else
  echo "$GITIGNORE_ADDITIONS" > "$PROJECT_ROOT/.gitignore"
  echo -e "${GREEN}✓${NC} Created .gitignore"
fi

# Create commitlint config if not exists
echo ""
echo "📝 Creating commitlint config..."

if [ ! -f "$PROJECT_ROOT/.commitlintrc.json" ]; then
  cat > "$PROJECT_ROOT/.commitlintrc.json" << 'EOF'
{
  "extends": ["@commitlint/config-conventional"],
  "rules": {
    "type-enum": [
      2,
      "always",
      [
        "feat",
        "fix",
        "docs",
        "style",
        "refactor",
        "perf",
        "test",
        "chore",
        "revert",
        "build",
        "ci"
      ]
    ],
    "subject-case": [2, "never", ["upper-case"]],
    "subject-empty": [2, "never"],
    "subject-full-stop": [2, "never", "."],
    "header-max-length": [2, "always", 100]
  }
}
EOF
  echo -e "${GREEN}✓${NC} commitlint config created"
  echo -e "${YELLOW}⚠${NC}  Install commitlint: npm install --save-dev @commitlint/cli @commitlint/config-conventional"
else
  echo -e "${BLUE}ℹ${NC}  .commitlintrc.json already exists"
fi

# Create quick reference visual
echo ""
echo "📋 Creating quick reference guide..."

if [ ! -f "$PROJECT_ROOT/docs/QUICK_REFERENCE.md" ]; then
  cat > "$PROJECT_ROOT/docs/QUICK_REFERENCE.md" << 'EOF'
# Development Quick Reference

## Decision Flowchart

```
┌─────────────────────────────┐
│   Is this user-facing?      │
└──────────┬──────────────────┘
           │ YES
           ↓
┌─────────────────────────────┐
│   Create feature flag       │
│   Default: OFF in prod      │
└─────────────────────────────┘

┌─────────────────────────────┐
│   Does this change schema?  │
└──────────┬──────────────────┘
           │ YES
           ↓
┌─────────────────────────────┐
│   Additive migration only   │
│   Create rollback script    │
└─────────────────────────────┘

┌─────────────────────────────┐
│   Will this be >50 lines?   │
└──────────┬──────────────────┘
           │ YES
           ↓
┌─────────────────────────────┐
│   Ask Cursor to show plan   │
│   before implementing       │
└─────────────────────────────┘
```

## Red Lines (Never Do This)

❌ Edit past migrations  
❌ Commit .env.local  
❌ Remove existing tests  
❌ Rewrite working code without reason  
❌ Add dependencies without approval  
❌ Use `any` without justification  
❌ Skip feature flags for user-facing changes  
❌ Deploy without tests passing  

## Before Every Commit

☐ Feature flag if user-facing change  
☐ Tests: unit + 1 e2e @happy-path  
☐ No secrets in code  
☐ TypeScript strict (no unjustified `any`)  
☐ Performance evidence (<500ms p95)  
☐ Docs updated (README, CHANGELOG)  
☐ Migration tested (if schema changed)  

## Common Commands

```bash
# Run pre-commit checks manually
.git/hooks/pre-commit

# View cursor rules
cat .cursor/rules.md

# Create new ADR
cp docs/adr/template.md "docs/adr/$(date +%Y%m%d)-your-title.md"

# View tech debt
cat docs/tech-debt.md

# Check test coverage
npm test -- --coverage
```

## Performance Targets

| Type | Target | When |
|------|--------|------|
| Critical (auth, checkout) | <200ms p95 | Always |
| Standard APIs | <500ms p95 | Always |
| Background jobs | <5s p95 | Usually |
| Analytics queries | <10s p95 | Acceptable |

## When In Doubt

1. Check existing patterns first
2. Ask in team chat before major changes
3. Show diff plan for >50 line changes
4. Feature flag it
5. Extend, don't replace

## Emergency Hotfix Protocol

1. Fix the issue
2. Deploy immediately
3. Follow up with full PR + review within 24h
4. Write post-mortem

## Resources

- Full Rules: `.cursor/rules.md`
- Prompt Templates: `docs/cursor_prompt_templates.md`
- ADR Template: `docs/adr/template.md`
- Tech Debt: `docs/tech-debt.md`
- PR Template: `.github/pull_request_template.md`
EOF
  echo -e "${GREEN}✓${NC} Quick reference created → docs/QUICK_REFERENCE.md"
else
  echo -e "${BLUE}ℹ${NC}  docs/QUICK_REFERENCE.md already exists"
fi

# Summary
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ Installation Complete!${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "📁 Files installed:"
echo "   • .cursor/rules.md"
echo "   • .git/hooks/pre-commit"
echo "   • .github/pull_request_template.md"
echo "   • docs/cursor_prompt_templates.md"
echo "   • docs/tech-debt.md"
echo "   • docs/adr/template.md"
echo "   • docs/QUICK_REFERENCE.md"
echo "   • CHANGELOG.md"
echo "   • .commitlintrc.json"
echo ""
echo "🔧 Next steps:"
echo "   1. Review and customize .cursor/rules.md for your project"
echo "   2. Install commitlint: npm install --save-dev @commitlint/cli @commitlint/config-conventional"
echo "   3. Set up husky for git hooks: npx husky-init && npm install"
echo "   4. Configure CI/CD pipeline (see docs for templates)"
echo "   5. Test pre-commit hook: git add . && git commit -m 'test: verify tooling'"
echo ""
echo "📖 Documentation:"
echo "   • Quick Reference: docs/QUICK_REFERENCE.md"
echo "   • Cursor Prompts: docs/cursor_prompt_templates.md"
echo "   • Full Rules: .cursor/rules.md"
echo ""
echo -e "${GREEN}Happy coding! 🚀${NC}"
echo ""
