# How to Push This Repo to GitHub

Step-by-step guide for Graeham. Total time: ~10 minutes first time through.

## What's in the folder you're about to push

When you look at `video-script-creation-engine-download/` in File Explorer, you should see:

- `CLAUDE.md` (orchestrator)
- `README.md`
- `PUSH-TO-GITHUB.md` (this file)
- `.env` (your Apify token — **this will NOT be uploaded**, it's in .gitignore)
- `.env.template`
- `.gitignore`
- `references/` folder (with `market-config.md`)
- `scripts/` folder (with `run_reddit_ideation.py`)
- `skills/` folder (with `bofu-query-generator/`, `bofu-scorer/`, `content-ideation-engine/`, `funnel-tagger/`, `script-writer/`)
- `examples/` folder (with 3 example content packages)
- `outputs/` folder (**this will NOT be uploaded**, it's in .gitignore)
- `.merge-backup/` folder (safe to delete, optional to push)

If any of the top-level items except `outputs/` and `.merge-backup/` are missing, stop and let me know.

---

## Recommended Path: Command Line (PowerShell)

This is the fastest path and gives you the clearest view of what's happening. If you'd rather use GitHub Desktop, see Option B at the bottom.

### Step 1: Create the empty repo on GitHub

1. Go to **github.com** in your browser, log in
2. Click the **"+"** in the top-right → **"New repository"**
3. Repository name: **`video-script-creation-engine`**
4. Description: *"Modular real estate content generation engine for Graeham Watts — Bay Area / East Palo Alto"*
5. Set it to **Private** (contains your strategy, market config, and lead capture keywords — don't make this public)
6. **Do NOT** check "Add a README file"
7. **Do NOT** add a .gitignore
8. **Do NOT** add a license
9. Click **Create repository**

GitHub will show you a "Quick setup" page with a URL that looks like:
```
https://github.com/YOUR_USERNAME/video-script-creation-engine.git
```

Copy that URL — you'll need it in Step 3.

### Step 2: Open PowerShell in the folder

1. Open File Explorer
2. Navigate to `C:\Users\Graeham Watts\Documents\Claude Skills\video-script-creation-engine-download`
3. In the address bar at the top, type `powershell` and hit Enter — PowerShell opens with that folder as the working directory

### Step 3: Run these commands one at a time

Paste each one, hit Enter, wait for it to finish, then paste the next.

```powershell
git init
```

```powershell
git add .
```

```powershell
git status
```

**STOP and check the output of `git status`.** You should see a long list of files staged. Confirm these two things:
- `.env` is **NOT** in the list (it should be ignored)
- `outputs/` contents are **NOT** in the list (should be ignored)

If `.env` shows up, stop and tell me — we have a .gitignore problem and we'll fix it before committing.

If it looks clean, continue:

```powershell
git commit -m "Initial commit: merged Video Script Creation Engine (Bay Area + BOFU)"
```

```powershell
git branch -M main
```

Now add the GitHub remote — **replace YOUR_USERNAME with your actual GitHub username**:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/video-script-creation-engine.git
```

Finally, push:

```powershell
git push -u origin main
```

### Step 4: Authenticate when Git asks

First time you push, Git will pop up a browser window or ask for a username/password.

- **If a browser window opens** → log into GitHub, approve, done
- **If it asks for a password in the terminal** → you need a Personal Access Token, not your GitHub password (GitHub removed password auth in 2021). See Troubleshooting below for how to make one.

### Step 5: Verify

1. Go back to github.com in your browser
2. Navigate to your new repo
3. Refresh
4. You should see `CLAUDE.md`, `README.md`, `skills/`, `scripts/`, `references/`, `examples/`
5. Click `README.md` — it should render the project overview
6. **Click `.env` — it should NOT be there.** If it is, delete the repo and come back to me immediately.

---

## Option B: GitHub Desktop (if you prefer GUI)

1. Download GitHub Desktop from **desktop.github.com** (free)
2. Sign in with your GitHub account
3. **File → Add local repository** → Choose the `video-script-creation-engine-download` folder
4. It'll say "not a Git repository, create one?" — click **create a repository**
5. In the form: Name `video-script-creation-engine`, UNCHECK "Initialize with README", Git ignore = None, License = None → **Create Repository**
6. Click **Publish repository** at the top
7. Name: `video-script-creation-engine`, Keep private: ✓ checked → **Publish**
8. Verify on github.com same as Step 5 above

---

## After You Push — What's Next

1. **Paste the repo URL back to me** so I can reference it in future sessions
2. **Test a content run** — prompt me with something like *"Use the video script creation engine to give me 3 BOFU videos for East Palo Alto sellers this week"* and we'll run the full pipeline
3. **When Reddit API approval lands**, we'll update `content-ideation-engine` to prefer PRAW over Apify and push the update as a new commit

---

## Troubleshooting

**"Permission denied" or "Authentication failed"** → You need a Personal Access Token (PAT):
1. GitHub → click your avatar (top right) → **Settings**
2. Scroll way down → **Developer settings** (left sidebar)
3. **Personal access tokens** → **Tokens (classic)** → **Generate new token (classic)**
4. Note: "Claude Skills push"
5. Expiration: 90 days (or whatever you want)
6. Scopes: check **`repo`** (the whole block)
7. **Generate token** → **copy it immediately** (you can't see it again)
8. When Git asks for a password, paste the token instead of your actual password

**"fatal: remote origin already exists"** → Run `git remote remove origin` then re-run the `git remote add origin` command.

**Files missing on GitHub after push** → Run `git status` in PowerShell. If it says "nothing to commit, working tree clean" then the push worked — refresh GitHub. If it shows staged files, the commit was empty — run `git commit -m "..."` again.

**`.env` accidentally got pushed** → This is serious — your Apify token is exposed. Do this immediately:
1. Go to Apify → Settings → Integrations → rotate the token (invalidate the old one, create a new one)
2. Update your local `.env` with the new token
3. Delete the GitHub repo (Settings → Danger Zone → Delete this repository)
4. Tell me and we'll fix `.gitignore` before re-pushing

**PowerShell can't find `git`** → Install Git for Windows from **git-scm.com/download/win** with default settings, then restart PowerShell.

**Anything else** → Screenshot the error and paste it back to me.
