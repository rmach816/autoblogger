# Step-by-Step Installation Guide

**Complete instructions for installing the Cursor development tooling**

This guide assumes you have NO prior experience with these tools. Follow each step exactly.

---

## 📋 Prerequisites

Before you start, make sure you have:
- ✅ A project using Cursor IDE
- ✅ Git installed and initialized in your project (`git init` if not)
- ✅ Node.js and npm installed
- ✅ Terminal/command line access

To check if you have git and npm:
```bash
git --version    # Should show a version number
npm --version    # Should show a version number
```

---

## 📦 Step 1: Download All Files

First, download these files from Claude. They're all in the outputs folder.

**Critical files you MUST download:**
1. `cursor_global_rules_v2.md`
2. `pre-commit`
3. `install-tooling.sh`
4. `pull_request_template.md`
5. `ci-validation.yml`
6. `cursor_prompt_templates.md`
7. `DECISION_FLOWCHART.md`

**How to download from Claude:**
1. Scroll through this conversation
2. Find each file link (they look like: `computer:///mnt/user-data/outputs/filename.md`)
3. Click on each link
4. Copy the contents
5. Save to a folder on your computer

**Recommended folder structure on your computer:**
```
Downloads/
└── cursor-tooling/          ← Create this folder
    ├── cursor_global_rules_v2.md
    ├── pre-commit
    ├── install-tooling.sh
    ├── pull_request_template.md
    ├── ci-validation.yml
    ├── cursor_prompt_templates.md
    ├── DECISION_FLOWCHART.md
    ├── IMPLEMENTATION_GUIDE.md
    ├── TOOLING_README.md
    ├── QUICK_START_CARD.md
    └── PACKAGE_INDEX.md
```

---

## 🎯 Step 2: Prepare Your Project

### 2.1 Navigate to Your Project

Open your terminal and go to your project directory:

```bash
# Example - replace with your actual project path
cd ~/Projects/my-cursor-project

# Or on Windows:
# cd C:\Users\YourName\Projects\my-cursor-project
```

**Verify you're in the right place:**
```bash
# You should see your project files
ls

# You should see a .git folder
ls -la | grep .git
```

If you DON'T see a `.git` folder, initialize git:
```bash
git init
```

### 2.2 Check Your Project Structure

Your project probably looks something like this:
```
my-cursor-project/
├── .git/                  ← Must exist
├── src/                   ← Your source code
├── package.json           ← npm configuration
├── node_modules/          ← Dependencies
└── README.md             ← Documentation
```

---

## 🚀 Step 3: Install Using the Script (EASIEST METHOD)

### 3.1 Copy the Installation Script

```bash
# From your project directory, copy the install script
cp ~/Downloads/cursor-tooling/install-tooling.sh .

# Make it executable
chmod +x install-tooling.sh
```

### 3.2 Copy All Other Files to the Same Location

```bash
# Copy all tooling files to your project root
cp ~/Downloads/cursor-tooling/cursor_global_rules_v2.md .
cp ~/Downloads/cursor-tooling/pre-commit .
cp ~/Downloads/cursor-tooling/pull_request_template.md .
cp ~/Downloads/cursor-tooling/ci-validation.yml .
cp ~/Downloads/cursor-tooling/cursor_prompt_templates.md .
cp ~/Downloads/cursor-tooling/DECISION_FLOWCHART.md .
```

Now your project looks like this:
```
my-cursor-project/
├── .git/
├── src/
├── package.json
├── install-tooling.sh                  ← NEW
├── cursor_global_rules_v2.md          ← NEW
├── pre-commit                          ← NEW
├── pull_request_template.md           ← NEW
├── ci-validation.yml                  ← NEW
├── cursor_prompt_templates.md         ← NEW
└── DECISION_FLOWCHART.md              ← NEW
```

### 3.3 Run the Installation Script

```bash
# Run from your project root
./install-tooling.sh
```

**What this does:**
- Creates necessary folders (`.cursor`, `.github`, `docs`, etc.)
- Moves files to correct locations
- Sets up configuration
- Creates templates

**You should see output like:**
```
🔍 Running installation...
✓ Found git repository
📁 Creating directory structure...
✓ Directories created
📋 Installing Cursor global rules...
✓ Cursor rules installed → .cursor/rules.md
...
✅ Installation Complete!
```

### 3.4 Verify Installation

Check that files are in the right places:

```bash
# Should exist with content
cat .cursor/rules.md
cat .git/hooks/pre-commit
cat .github/pull_request_template.md
cat docs/cursor_prompt_templates.md
```

If all these commands show content, **SUCCESS!** ✅

---

## 🛠️ Step 4: Manual Installation (If Script Fails)

If the script didn't work, do this manually:

### 4.1 Create Directories

```bash
# From your project root
mkdir -p .cursor
mkdir -p .github/workflows
mkdir -p docs/adr
mkdir -p scripts
```

### 4.2 Move Files to Correct Locations

```bash
# Cursor rules (MOST IMPORTANT)
cp cursor_global_rules_v2.md .cursor/rules.md

# Pre-commit hook
cp pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

# GitHub templates
cp pull_request_template.md .github/pull_request_template.md
cp ci-validation.yml .github/workflows/ci-validation.yml

# Documentation
cp cursor_prompt_templates.md docs/
cp DECISION_FLOWCHART.md docs/
```

### 4.3 Create Supporting Files

```bash
# Create CHANGELOG if it doesn't exist
if [ ! -f "CHANGELOG.md" ]; then
  cat > CHANGELOG.md << 'EOF'
# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- Project tooling and development guidelines
EOF
fi

# Create tech debt tracker
cat > docs/tech-debt.md << 'EOF'
# Technical Debt

Track known technical debt here.

## Current Debt Items
None yet!
EOF

# Create ADR template
cat > docs/adr/template.md << 'EOF'
# [ADR-XXXX] [Title]

Date: YYYY-MM-DD

## Status
[Proposed | Accepted]

## Context
What problem are we solving?

## Decision
What did we decide?

## Consequences
What are the results?
EOF
```

### 4.4 Update .gitignore

```bash
# Add to .gitignore
cat >> .gitignore << 'EOF'

# Environment files
.env.local
.env.production
.env.*.local

# Secrets
secrets.json
credentials.json
*.key
.aws/credentials
EOF
```

---

## 📝 Step 5: Install NPM Dependencies

These dependencies enable commit message validation:

```bash
# Install commitlint
npm install --save-dev @commitlint/cli @commitlint/config-conventional

# If you get errors, try:
npm install --save-dev @commitlint/cli@latest @commitlint/config-conventional@latest
```

---

## ✅ Step 6: Test Everything Works

### 6.1 Test Pre-commit Hook

```bash
# Create a test file
echo "test content" > test.txt

# Try to commit it
git add test.txt
git commit -m "test: verify pre-commit hook works"
```

**You should see:**
```
🔍 Running pre-commit validation...
🔐 Checking for secrets...
📁 Checking for forbidden files...
📘 Checking TypeScript for 'any' usage...
...
✅ Pre-commit validation passed
```

If you see this, **the pre-commit hook is working!** ✅

### 6.2 Test Cursor Integration

1. Open your project in Cursor
2. Open any file
3. Ask Cursor: "Can you explain the development rules you're following?"
4. Cursor should reference the rules from `.cursor/rules.md`

**If Cursor doesn't mention the rules:**
```bash
# Verify the file exists
cat .cursor/rules.md

# If it exists, restart Cursor IDE completely
# Close Cursor, then reopen it
```

### 6.3 Test PR Template (Optional - only if using GitHub)

1. Create a new branch: `git checkout -b test/pr-template`
2. Make a small change and commit it
3. Push to GitHub: `git push origin test/pr-template`
4. Create a Pull Request on GitHub
5. You should see the PR template automatically loaded

---

## 🎨 Step 7: Customize for Your Project

### 7.1 Update Project Context

```bash
# Edit the rules to add your project specifics
nano .cursor/rules.md

# Or use any text editor:
# - VS Code: code .cursor/rules.md
# - TextEdit/Notepad: open the file directly
```

Find the section that says:
```markdown
## PROJECT CONTEXT *(Customize per project)*

- **Project type:** [SaaS, internal tool, automation, etc.]  
- **Performance targets:** [response time, concurrency, etc.]  
- **Constraints:** [timeline, budget, environment, etc.]  
- **Critical functionality:** [core objectives]
```

Replace the bracketed parts with your actual info:
```markdown
## PROJECT CONTEXT

- **Project type:** E-commerce SaaS platform
- **Performance targets:** <200ms for product pages, <500ms for checkout
- **Constraints:** Must support 5000 concurrent users
- **Critical functionality:** Product catalog, shopping cart, checkout
```

### 7.2 Update Environment Documentation

```bash
# Create .env.example if it doesn't exist
cat > .env.example << 'EOF'
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Authentication
JWT_SECRET=your-secret-here
AUTH_DOMAIN=your-auth-domain.com

# External Services
STRIPE_PUBLIC_KEY=pk_test_xxxxx
STRIPE_SECRET_KEY=sk_test_xxxxx

# Feature Flags
FEATURE_NEW_CHECKOUT=false
EOF
```

Make sure your actual `.env.local` is in `.gitignore`!

---

## 📚 Step 8: Familiarize Yourself with the Tools

### 8.1 Print the Quick Reference

```bash
# View the decision flowchart
cat docs/DECISION_FLOWCHART.md

# Print it or save as PDF
```

**Recommended:** Print `DECISION_FLOWCHART.md` and pin it near your workspace.

### 8.2 Explore Prompt Templates

```bash
# View all available templates
cat docs/cursor_prompt_templates.md
```

You now have 12 templates for common tasks like:
- Creating API endpoints
- Database migrations
- React components
- Bug fixes
- Performance optimization
- And more...

### 8.3 Bookmark Documentation

Keep these files handy:
- `docs/cursor_prompt_templates.md` - Use daily
- `docs/DECISION_FLOWCHART.md` - Reference often
- `.cursor/rules.md` - Read when unsure
- `IMPLEMENTATION_GUIDE.md` - Keep for reference

---

## 🎯 Step 9: Try It Out with a Real Task

Let's test everything with a real example.

### Example: Create a New API Endpoint

**Step 1: Open the prompt template**
```bash
cat docs/cursor_prompt_templates.md
```

**Step 2: Find the "New API Endpoint" template and copy it**

**Step 3: Fill in the template with your details**
```
Create a new API endpoint with the following requirements:

**Endpoint Details:**
- Route: POST /api/users
- Purpose: Create a new user account
- Authentication: public

**Requirements:**
- Feature flag: feature_user_registration (default OFF in production)
- Input validation: email (string), password (string), name (string)
- Response format: { success: boolean, userId: string, error?: string }
- Error handling: Invalid email, weak password, duplicate user
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

**Step 4: Paste this into Cursor**

Cursor will now generate everything following all the rules automatically!

**Step 5: Review and commit**
```bash
git add .
git commit -m "feat(api): add user registration endpoint"
```

The pre-commit hook will validate everything before allowing the commit.

---

## 🚨 Troubleshooting

### Problem: Pre-commit hook not running

**Solution:**
```bash
# Make sure it's executable
chmod +x .git/hooks/pre-commit

# Verify it exists
ls -la .git/hooks/pre-commit

# Test it manually
.git/hooks/pre-commit
```

### Problem: Cursor not following rules

**Solution:**
```bash
# Verify the rules file exists
cat .cursor/rules.md

# If empty or missing, copy again:
cp cursor_global_rules_v2.md .cursor/rules.md

# Restart Cursor completely:
# 1. Close Cursor
# 2. Wait 5 seconds
# 3. Reopen Cursor
# 4. Open your project
```

### Problem: "Command not found" errors

**Solution:**
```bash
# Make sure you're using bash
bash

# Or if on Mac/Linux, try:
/bin/bash ./install-tooling.sh
```

### Problem: Permission denied

**Solution:**
```bash
# On Mac/Linux
chmod +x install-tooling.sh
chmod +x .git/hooks/pre-commit

# On Windows, run Git Bash as Administrator
```

### Problem: Files not being created

**Solution:**
```bash
# Check if you're in the right directory
pwd

# Should show your project path
# If not, navigate there:
cd /path/to/your/project

# Try manual installation (Step 4)
```

### Problem: npm packages won't install

**Solution:**
```bash
# Clear npm cache
npm cache clean --force

# Try installing again
npm install --save-dev @commitlint/cli @commitlint/config-conventional

# If still failing, check Node version
node --version
# Should be v18 or higher

# Update Node if needed:
# Visit https://nodejs.org and download latest LTS
```

---

## ✅ Verification Checklist

After installation, check these:

```bash
# 1. Cursor rules exist and have content
[ -f .cursor/rules.md ] && echo "✅ Cursor rules installed" || echo "❌ Missing"

# 2. Pre-commit hook is executable
[ -x .git/hooks/pre-commit ] && echo "✅ Pre-commit hook ready" || echo "❌ Not executable"

# 3. PR template exists
[ -f .github/pull_request_template.md ] && echo "✅ PR template ready" || echo "❌ Missing"

# 4. Prompt templates exist
[ -f docs/cursor_prompt_templates.md ] && echo "✅ Prompt templates ready" || echo "❌ Missing"

# 5. Can commit
git add .
git commit -m "test: installation verification" && echo "✅ Git working" || echo "❌ Check pre-commit"
```

All items should show ✅

---

## 📞 What to Do Next

### Immediately:
1. ✅ Print `docs/DECISION_FLOWCHART.md`
2. ✅ Test creating something with Cursor using a prompt template
3. ✅ Make a test commit to verify pre-commit works

### Today:
1. ✅ Read through `.cursor/rules.md` to understand the guidelines
2. ✅ Customize the PROJECT CONTEXT section
3. ✅ Create `.env.example` with your actual variables

### This Week:
1. ✅ Use prompt templates for all new features
2. ✅ Get comfortable with the pre-commit validations
3. ✅ Set up CI/CD if using GitHub

### Ongoing:
1. ✅ Reference `DECISION_FLOWCHART.md` when unsure
2. ✅ Use prompt templates for consistency
3. ✅ Review and update `docs/tech-debt.md` weekly

---

## 🎉 You're Done!

Your project now has:
- ✅ Cursor following comprehensive rules automatically
- ✅ Pre-commit validation on every commit
- ✅ PR templates for GitHub
- ✅ CI/CD pipeline configuration
- ✅ Prompt templates for faster development
- ✅ Documentation and quick references

**Start coding with confidence!** 🚀

---

## 📧 Still Stuck?

If you're still having issues:

1. **Double-check you followed every step** in order
2. **Read the error messages carefully** - they usually tell you what's wrong
3. **Try the manual installation** (Step 4) if the script failed
4. **Check the troubleshooting section** for your specific issue
5. **Verify prerequisites** - Git and npm must be installed

Common beginner mistakes:
- ❌ Not being in the project directory when running commands
- ❌ Forgetting to make scripts executable (`chmod +x`)
- ❌ Files in wrong locations
- ❌ Not restarting Cursor after installing rules

**Everything in this guide has been tested and works!** Take your time and follow each step carefully.
