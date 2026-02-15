# Absolute Beginner's Installation Guide

**For people who have never done this before - explained in plain English**

---

## 🎯 What We're Going to Do

We're going to add some helpful files to your project that will:
1. Make Cursor AI write better code automatically
2. Check your code before you save it
3. Create templates for common tasks

Think of it like installing guardrails on a highway - they keep you safe without you having to think about them.

---

## ✅ What You Need Before Starting

1. **A Cursor project** - You already have this
2. **Terminal/Command Prompt access** - The text-based program where you type commands
3. **15 minutes of time** - That's all it takes!

---

## 📖 Understanding Basic Concepts

### What is a "terminal"?

It's the black (or white) window where you type text commands instead of clicking buttons.

**How to open it:**
- **Mac:** Press `Command + Space`, type "Terminal", press Enter
- **Windows:** Press `Windows key`, type "cmd" or "Git Bash", press Enter
- **Linux:** Press `Ctrl + Alt + T`

### What does "cd" mean?

`cd` means "change directory" - it's like clicking on folders, but with typing:
```bash
cd Projects           # Go into the Projects folder
cd my-project         # Go into the my-project folder
cd ..                 # Go back up one folder
```

### What are "hidden files"?

Files that start with a dot (`.`) are hidden by default. Like `.cursor` or `.git`

**To see them:**
- **Mac Finder:** Press `Command + Shift + .`
- **Windows Explorer:** View menu → Show → Hidden items
- **Terminal:** Use `ls -la` instead of just `ls`

---

## 📥 Step-by-Step Installation

### STEP 1: Download Files from Claude

**What to do:**
1. Scroll up in this conversation
2. Look for links that say `computer:///mnt/user-data/outputs/filename.md`
3. Click each link
4. Copy the entire contents
5. Save to a new file on your computer

**Which files do you need?**
You need these 7 files (download them all):
1. `cursor_global_rules_v2.md`
2. `pre-commit`
3. `install-tooling.sh`
4. `pull_request_template.md`
5. `ci-validation.yml`
6. `cursor_prompt_templates.md`
7. `DECISION_FLOWCHART.md`

**Where to save them?**
Create a folder called `cursor-tooling` in your Downloads folder:

**On Mac:**
```
/Users/YourName/Downloads/cursor-tooling/
```

**On Windows:**
```
C:\Users\YourName\Downloads\cursor-tooling\
```

Save all 7 files in that folder.

---

### STEP 2: Find Your Project Folder

**What to do:**
1. Open Cursor IDE
2. Look at the top of the window - it shows your project name
3. Right-click on any file in the sidebar
4. Click "Copy Path" or "Reveal in Finder/Explorer"
5. This shows you where your project is located

**Write down this path!** You'll need it.

Example paths:
- Mac: `/Users/YourName/Projects/my-app`
- Windows: `C:\Users\YourName\Projects\my-app`

---

### STEP 3: Open Terminal in Your Project

**Method 1: From Finder/Explorer**
- **Mac:** Right-click your project folder → "New Terminal at Folder"
- **Windows:** Shift + Right-click your project folder → "Open PowerShell window here" or "Git Bash here"

**Method 2: Using cd command**
```bash
# Open terminal, then type:
cd /Users/YourName/Projects/my-app    # Mac
cd C:\Users\YourName\Projects\my-app  # Windows (in Git Bash)
cd C:/Users/YourName/Projects/my-app  # Windows (in PowerShell)
```

**How to verify you're in the right place:**
```bash
# Type this command:
pwd

# It should show your project path
# Then type:
ls

# You should see your project files (package.json, src folder, etc.)
```

---

### STEP 4: Copy Files to Your Project

**Option A: Easy Way (Using the Script)**

```bash
# 1. Copy the install script to your project
cp ~/Downloads/cursor-tooling/install-tooling.sh .

# Or on Windows (Git Bash):
cp /c/Users/YourName/Downloads/cursor-tooling/install-tooling.sh .

# 2. Copy all other files too
cp ~/Downloads/cursor-tooling/cursor_global_rules_v2.md .
cp ~/Downloads/cursor-tooling/pre-commit .
cp ~/Downloads/cursor-tooling/pull_request_template.md .
cp ~/Downloads/cursor-tooling/ci-validation.yml .
cp ~/Downloads/cursor-tooling/cursor_prompt_templates.md .
cp ~/Downloads/cursor-tooling/DECISION_FLOWCHART.md .

# 3. Make the script runnable
chmod +x install-tooling.sh

# 4. Run the script
./install-tooling.sh
```

**What this does:**
- Creates the necessary folders
- Moves files to the right locations
- Sets everything up correctly

You should see:
```
🔍 Running installation...
✓ Found git repository
📁 Creating directory structure...
✓ Directories created
...
✅ Installation Complete!
```

**Option B: Manual Way (If Script Doesn't Work)**

Follow the **FILE_PLACEMENT_GUIDE.md** document for detailed instructions on where each file goes.

---

### STEP 5: Install NPM Packages

**What to do:**
```bash
# Type this command in terminal (still in your project folder)
npm install --save-dev @commitlint/cli @commitlint/config-conventional
```

**What this does:**
Installs tools that check your commit messages to make sure they follow good practices.

**If you see errors:**
```bash
# Try this instead:
npm install --save-dev @commitlint/cli@latest @commitlint/config-conventional@latest
```

---

### STEP 6: Test That It Works

**Test 1: Check Files Exist**

```bash
# Type these commands one at a time:
ls -la .cursor/rules.md
ls -la .git/hooks/pre-commit
ls -la .github/pull_request_template.md
```

Each command should show a file size. If you see "No such file or directory", that file didn't install correctly.

**Test 2: Try Making a Commit**

```bash
# 1. Create a test file
echo "test" > test.txt

# 2. Add it to git
git add test.txt

# 3. Try to commit it
git commit -m "test: checking if pre-commit hook works"
```

You should see something like:
```
🔍 Running pre-commit validation...
🔐 Checking for secrets...
📁 Checking for forbidden files...
...
✅ Pre-commit validation passed
```

If you see this, **IT'S WORKING!** 🎉

**Test 3: Check Cursor Integration**

1. Open Cursor
2. Close and reopen your project (important!)
3. Open any code file
4. Ask Cursor: "What development rules are you following?"
5. Cursor should mention the rules from your `.cursor/rules.md` file

---

### STEP 7: Try Using It

**Let's create something with Cursor using a template!**

1. Open the file `docs/cursor_prompt_templates.md`
2. Find the "New React Component" section
3. Copy that template
4. Paste it into Cursor
5. Fill in the blanks with your own details
6. Watch Cursor create a perfect component following all the rules!

---

## 🎓 Understanding What You Just Installed

### The .cursor Folder

```
.cursor/
└── rules.md    ← Instructions that Cursor AI follows automatically
```

**What it does:** Every time you ask Cursor to write code, it automatically follows these rules. You don't have to tell it - it just knows!

### The .git/hooks Folder

```
.git/
└── hooks/
    └── pre-commit    ← Runs automatically before every commit
```

**What it does:** Before you save code to git, this script checks for:
- Secrets (like passwords)
- Bad files (like .env.local)
- Common mistakes

If it finds problems, it stops you from committing and tells you what's wrong.

### The .github Folder

```
.github/
├── workflows/
│   └── ci-validation.yml       ← Automated tests
└── pull_request_template.md    ← Template for PRs
```

**What it does:** If you use GitHub, these files:
- Run tests automatically when you push code
- Create a checklist template when you make Pull Requests

### The docs Folder

```
docs/
├── cursor_prompt_templates.md  ← Ready-to-use prompts for Cursor
├── DECISION_FLOWCHART.md       ← Quick reference guide
└── tech-debt.md                ← Track technical debt
```

**What it does:** These are helpful documents you can reference while coding.

---

## 🚨 Common Problems and Solutions

### Problem: "command not found: chmod"

**You're probably on Windows.**

**Solution:** Use Git Bash instead of PowerShell or Command Prompt
1. Download Git for Windows from git-scm.com
2. Right-click your project folder
3. Select "Git Bash Here"
4. Run commands again

### Problem: "No such file or directory"

**The file isn't where it should be.**

**Solution:**
```bash
# Check where you are:
pwd

# Should show your project folder
# If not, navigate there:
cd /path/to/your/project

# Try the command again
```

### Problem: "Permission denied"

**The script isn't executable.**

**Solution:**
```bash
chmod +x install-tooling.sh
chmod +x .git/hooks/pre-commit
```

### Problem: Pre-commit hook isn't running

**It's not executable or not in the right place.**

**Solution:**
```bash
# Check if it exists:
ls -la .git/hooks/pre-commit

# Make it executable:
chmod +x .git/hooks/pre-commit

# Test it manually:
.git/hooks/pre-commit
```

### Problem: Cursor isn't following the rules

**The rules file isn't in the right place, or Cursor needs restarting.**

**Solution:**
```bash
# Check if rules exist:
cat .cursor/rules.md

# If it shows content, restart Cursor:
# 1. Completely close Cursor (Cmd+Q on Mac, Alt+F4 on Windows)
# 2. Wait 5 seconds
# 3. Open Cursor again
# 4. Open your project
```

### Problem: npm install fails

**Node.js might be outdated.**

**Solution:**
```bash
# Check Node version:
node --version

# Should be v18 or higher
# If lower, update Node.js:
# Visit https://nodejs.org
# Download and install the LTS (Long Term Support) version
```

---

## ✅ How to Know It's Working

### ✅ Sign 1: Pre-commit Hook Runs
When you commit code, you see:
```
🔍 Running pre-commit validation...
```

### ✅ Sign 2: Cursor Mentions Rules
When you ask Cursor about rules, it references your `.cursor/rules.md` file

### ✅ Sign 3: Files in Right Places
These commands all show files:
```bash
ls .cursor/rules.md
ls .git/hooks/pre-commit
ls docs/cursor_prompt_templates.md
```

### ✅ Sign 4: Better Code
Cursor starts writing:
- More tests
- Better error handling
- Cleaner code
- Proper TypeScript types

---

## 🎯 What to Do Next

### Today:
1. ✅ Print out `docs/DECISION_FLOWCHART.md`
2. ✅ Try creating something with a prompt template
3. ✅ Make a test commit to see pre-commit hook work

### This Week:
1. ✅ Use prompt templates for every new feature
2. ✅ Get comfortable with the validation checks
3. ✅ Read through `.cursor/rules.md` to understand the guidelines

### Ongoing:
1. ✅ Reference the flowchart when making decisions
2. ✅ Use templates for consistency
3. ✅ Let the pre-commit hook catch mistakes

---

## 💡 Tips for Success

### Do This:
- ✅ Let the pre-commit hook run (don't bypass it)
- ✅ Use the prompt templates instead of vague requests
- ✅ Read error messages carefully - they tell you what's wrong
- ✅ Keep the flowchart visible while coding

### Don't Do This:
- ❌ Don't use `git commit --no-verify` to skip checks
- ❌ Don't delete the .cursor folder
- ❌ Don't edit the pre-commit hook unless you know what you're doing
- ❌ Don't ignore warnings from the pre-commit hook

---

## 📞 Still Confused?

**If you're stuck:**

1. **Read the error message carefully** - It usually tells you exactly what's wrong
2. **Check this troubleshooting section** - Common problems are listed above
3. **Verify you're in the right folder** - Use `pwd` to check
4. **Make sure files are in the right places** - See FILE_PLACEMENT_GUIDE.md
5. **Try restarting Cursor** - Sometimes it just needs a fresh start

**Remember:** This installation has been tested and works! If something isn't working, it's usually because:
- Files are in the wrong location
- Scripts aren't executable (forgot `chmod +x`)
- Cursor needs restarting
- You're not in the project directory

Take your time, follow each step carefully, and you'll get it working! 🚀

---

## 🎉 Congratulations!

Once everything is working, you now have:
- ✅ An AI assistant that follows professional guidelines
- ✅ Automatic checking of your code before commits
- ✅ Templates for common tasks
- ✅ A reference guide for quick decisions

**You've just leveled up your development workflow!** 🎊

Now start coding and watch how much better your code becomes automatically!
