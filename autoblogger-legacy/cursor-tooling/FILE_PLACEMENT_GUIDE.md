# Visual File Placement Guide

**Exactly where each file goes in your project**

---

## 📂 Before Installation

Your project probably looks like this:

```
my-cursor-project/                    ← Your project folder
│
├── .git/                             ← Git folder (hidden)
│   └── hooks/                        ← Git hooks folder
│
├── src/                              ← Your source code
│   ├── components/
│   ├── pages/
│   └── utils/
│
├── node_modules/                     ← Dependencies (hidden)
│
├── package.json                      ← NPM configuration
├── package-lock.json
├── tsconfig.json
├── .gitignore
└── README.md
```

---

## 📂 After Installation

Your project will look like this:

```
my-cursor-project/                    ← Your project folder
│
├── .cursor/                          ← NEW FOLDER
│   └── rules.md                      ← cursor_global_rules_v2.md goes here
│
├── .git/                             ← Existing
│   └── hooks/                        
│       └── pre-commit                ← pre-commit file goes here (make executable!)
│
├── .github/                          ← NEW FOLDER (if using GitHub)
│   ├── workflows/
│   │   └── ci-validation.yml         ← ci-validation.yml goes here
│   └── pull_request_template.md      ← pull_request_template.md goes here
│
├── docs/                             ← NEW FOLDER
│   ├── adr/                          ← NEW SUBFOLDER
│   │   └── template.md               ← ADR template (created by script)
│   ├── cursor_prompt_templates.md    ← cursor_prompt_templates.md goes here
│   ├── DECISION_FLOWCHART.md         ← DECISION_FLOWCHART.md goes here
│   └── tech-debt.md                  ← Tech debt tracker (created by script)
│
├── src/                              ← Your existing code (unchanged)
│   ├── components/
│   ├── pages/
│   └── utils/
│
├── node_modules/                     ← Existing dependencies
│
├── .commitlintrc.json                ← Commit lint config (created by script)
├── .gitignore                        ← Updated with security patterns
├── CHANGELOG.md                      ← Created by script (if didn't exist)
├── package.json                      ← Existing (unchanged)
├── README.md                         ← Existing (you might want to update it)
└── tsconfig.json                     ← Existing (unchanged)
```

---

## 🎯 Critical Files and Their Locations

### File #1: Cursor Rules (MOST IMPORTANT)

**Downloaded file:** `cursor_global_rules_v2.md`  
**Installation location:** `.cursor/rules.md`

```
your-project/
└── .cursor/              ← Create this folder
    └── rules.md          ← Copy cursor_global_rules_v2.md here and rename
```

**How to install:**
```bash
# From your project root
mkdir -p .cursor
cp /path/to/cursor_global_rules_v2.md .cursor/rules.md
```

**How to verify:**
```bash
cat .cursor/rules.md
# Should show the complete ruleset
```

---

### File #2: Pre-commit Hook

**Downloaded file:** `pre-commit`  
**Installation location:** `.git/hooks/pre-commit`

```
your-project/
└── .git/                 ← Already exists (hidden folder)
    └── hooks/            ← Already exists
        └── pre-commit    ← Copy pre-commit file here
```

**How to install:**
```bash
# From your project root
cp /path/to/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit  # Make it executable!
```

**How to verify:**
```bash
ls -la .git/hooks/pre-commit
# Should show file with 'x' permissions (executable)

# Test it:
.git/hooks/pre-commit
```

---

### File #3: PR Template

**Downloaded file:** `pull_request_template.md`  
**Installation location:** `.github/pull_request_template.md`

```
your-project/
└── .github/                        ← Create this folder
    └── pull_request_template.md   ← Copy here
```

**How to install:**
```bash
# From your project root
mkdir -p .github
cp /path/to/pull_request_template.md .github/pull_request_template.md
```

**How to verify:**
```bash
cat .github/pull_request_template.md
# Should show the PR template
```

---

### File #4: CI/CD Pipeline

**Downloaded file:** `ci-validation.yml`  
**Installation location:** `.github/workflows/ci-validation.yml`

```
your-project/
└── .github/              ← Create if doesn't exist
    └── workflows/        ← Create this subfolder
        └── ci-validation.yml   ← Copy here
```

**How to install:**
```bash
# From your project root
mkdir -p .github/workflows
cp /path/to/ci-validation.yml .github/workflows/ci-validation.yml
```

**How to verify:**
```bash
cat .github/workflows/ci-validation.yml
# Should show the workflow configuration
```

---

### File #5: Prompt Templates

**Downloaded file:** `cursor_prompt_templates.md`  
**Installation location:** `docs/cursor_prompt_templates.md`

```
your-project/
└── docs/                          ← Create this folder
    └── cursor_prompt_templates.md ← Copy here
```

**How to install:**
```bash
# From your project root
mkdir -p docs
cp /path/to/cursor_prompt_templates.md docs/cursor_prompt_templates.md
```

**How to verify:**
```bash
cat docs/cursor_prompt_templates.md
# Should show 12 prompt templates
```

---

### File #6: Decision Flowchart

**Downloaded file:** `DECISION_FLOWCHART.md`  
**Installation location:** `docs/DECISION_FLOWCHART.md`

```
your-project/
└── docs/                    ← Same docs folder as above
    └── DECISION_FLOWCHART.md ← Copy here
```

**How to install:**
```bash
# From your project root
mkdir -p docs
cp /path/to/DECISION_FLOWCHART.md docs/DECISION_FLOWCHART.md
```

**How to verify:**
```bash
cat docs/DECISION_FLOWCHART.md
# Should show the visual flowchart
```

---

## 🔄 Complete Installation Map

```
WHERE YOU DOWNLOAD FILES              WHERE THEY GO IN YOUR PROJECT
(~/Downloads/cursor-tooling/)         (~/Projects/my-cursor-project/)

cursor_global_rules_v2.md     →       .cursor/rules.md
pre-commit                    →       .git/hooks/pre-commit (chmod +x!)
pull_request_template.md      →       .github/pull_request_template.md
ci-validation.yml             →       .github/workflows/ci-validation.yml
cursor_prompt_templates.md    →       docs/cursor_prompt_templates.md
DECISION_FLOWCHART.md         →       docs/DECISION_FLOWCHART.md

install-tooling.sh            →       (run from project root, then delete)
IMPLEMENTATION_GUIDE.md       →       (keep for reference, don't need in project)
TOOLING_README.md            →       (keep for reference, don't need in project)
```

---

## 📝 Quick Copy-Paste Commands

**If you have all files in ~/Downloads/cursor-tooling/ and your project is at ~/Projects/my-project/**

```bash
# Navigate to your project
cd ~/Projects/my-project

# Create all necessary directories
mkdir -p .cursor
mkdir -p .github/workflows
mkdir -p docs/adr

# Copy files to correct locations
cp ~/Downloads/cursor-tooling/cursor_global_rules_v2.md .cursor/rules.md
cp ~/Downloads/cursor-tooling/pre-commit .git/hooks/pre-commit
cp ~/Downloads/cursor-tooling/pull_request_template.md .github/pull_request_template.md
cp ~/Downloads/cursor-tooling/ci-validation.yml .github/workflows/ci-validation.yml
cp ~/Downloads/cursor-tooling/cursor_prompt_templates.md docs/
cp ~/Downloads/cursor-tooling/DECISION_FLOWCHART.md docs/

# Make pre-commit executable
chmod +x .git/hooks/pre-commit

# Verify everything is in place
ls -la .cursor/rules.md
ls -la .git/hooks/pre-commit
ls -la .github/pull_request_template.md
ls -la .github/workflows/ci-validation.yml
ls -la docs/cursor_prompt_templates.md
ls -la docs/DECISION_FLOWCHART.md

# All should show file sizes - if they do, you're done! ✅
```

---

## 🎯 Alternative: Using the Install Script

Instead of copying files manually, you can use the install script:

```bash
# Navigate to your project
cd ~/Projects/my-project

# Copy ALL files from downloads to project root temporarily
cp ~/Downloads/cursor-tooling/* .

# Run the installer
chmod +x install-tooling.sh
./install-tooling.sh

# Clean up temporary files
rm install-tooling.sh
rm cursor_global_rules_v2.md
rm pre-commit
rm pull_request_template.md
rm ci-validation.yml
rm cursor_prompt_templates.md
rm DECISION_FLOWCHART.md

# Files are now in correct locations automatically!
```

---

## ✅ Final Verification

After installation, your project structure should include these NEW items:

```bash
# Check each critical file exists
[ -f .cursor/rules.md ] && echo "✅ Cursor rules" || echo "❌ Missing"
[ -f .git/hooks/pre-commit ] && echo "✅ Pre-commit hook" || echo "❌ Missing"
[ -f .github/pull_request_template.md ] && echo "✅ PR template" || echo "❌ Missing"
[ -f .github/workflows/ci-validation.yml ] && echo "✅ CI workflow" || echo "❌ Missing"
[ -f docs/cursor_prompt_templates.md ] && echo "✅ Prompts" || echo "❌ Missing"
[ -f docs/DECISION_FLOWCHART.md ] && echo "✅ Flowchart" || echo "❌ Missing"

# Check pre-commit is executable
[ -x .git/hooks/pre-commit ] && echo "✅ Pre-commit executable" || echo "❌ Not executable"
```

All should show ✅

---

## 🚨 Common Mistakes

### ❌ Wrong: Files in project root
```
my-project/
├── cursor_global_rules_v2.md    ← WRONG! Should be in .cursor/
├── pre-commit                   ← WRONG! Should be in .git/hooks/
└── pull_request_template.md     ← WRONG! Should be in .github/
```

### ✅ Right: Files in correct subfolders
```
my-project/
├── .cursor/
│   └── rules.md                 ← RIGHT!
├── .git/
│   └── hooks/
│       └── pre-commit           ← RIGHT!
└── .github/
    └── pull_request_template.md ← RIGHT!
```

### ❌ Wrong: Pre-commit not executable
```bash
ls -la .git/hooks/pre-commit
# -rw-r--r--  ← Missing 'x' - NOT executable
```

### ✅ Right: Pre-commit is executable
```bash
ls -la .git/hooks/pre-commit
# -rwxr-xr-x  ← Has 'x' - IS executable
```

---

## 📍 Path Examples for Different Operating Systems

### macOS / Linux
```bash
Project location: ~/Projects/my-project
Downloads: ~/Downloads/cursor-tooling/

# Navigate to project:
cd ~/Projects/my-project

# Copy from downloads:
cp ~/Downloads/cursor-tooling/cursor_global_rules_v2.md .cursor/rules.md
```

### Windows (Git Bash)
```bash
Project location: C:/Users/YourName/Projects/my-project
Downloads: C:/Users/YourName/Downloads/cursor-tooling/

# Navigate to project:
cd /c/Users/YourName/Projects/my-project

# Copy from downloads:
cp /c/Users/YourName/Downloads/cursor-tooling/cursor_global_rules_v2.md .cursor/rules.md
```

### Windows (PowerShell)
```powershell
Project location: C:\Users\YourName\Projects\my-project
Downloads: C:\Users\YourName\Downloads\cursor-tooling\

# Navigate to project:
cd C:\Users\YourName\Projects\my-project

# Copy from downloads:
Copy-Item C:\Users\YourName\Downloads\cursor-tooling\cursor_global_rules_v2.md .cursor\rules.md
```

---

## 🎓 Understanding Hidden Folders

Some folders are "hidden" by default:

- `.cursor/` - Hidden (starts with dot)
- `.git/` - Hidden (starts with dot)
- `.github/` - Hidden (starts with dot)

**To see hidden folders:**
```bash
# macOS / Linux
ls -la

# Windows Explorer
# View → Show → Hidden items (check the box)

# Windows Command Prompt
dir /a
```

---

## 💡 Pro Tip: Use the Script!

The **easiest way** to install everything correctly:

1. Download all files to `~/Downloads/cursor-tooling/`
2. Copy `install-tooling.sh` to your project root
3. Run: `./install-tooling.sh`
4. Done! Everything goes to the right place automatically

This guide shows manual installation so you understand where everything goes, but the script does all of this for you automatically!

---

**Now you know exactly where every file goes!** 🎯
