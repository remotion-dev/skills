---
name: github-skill-sync
description: >
  Auto-push skills to the Graehamwatts/skills GitHub repo. Use this skill ANY time:
  a skill is created, updated, modified, or improved; the user says "push skills",
  "sync skills", "update the repo", "push to GitHub", "save skills to GitHub";
  after using skill-creator to build or modify a skill; when the user asks to
  back up or version-control their skills. Also trigger proactively after ANY
  skill creation or modification workflow completes — don't wait for the user
  to ask. If a skill was just created or edited, offer to sync it to GitHub.
---

# GitHub Skill Sync

Push skill changes to the `Graehamwatts/skills` GitHub repository automatically.
This keeps the repo in sync so any machine (Mac Studio, Windows, etc.) can clone
the latest skills.

## How It Works

This skill uses `git` with a GitHub Personal Access Token (classic) to clone the
repo, copy in updated skills, and push. The token is stored as a classic PAT
with `repo` scope under the name "Cowork Push" in GitHub settings.

## When to Run

- **After creating a new skill** — push it immediately so it's available everywhere
- **After modifying an existing skill** — push the changes
- **On user request** — "push skills to GitHub", "sync the repo", etc.
- **Proactively** — if you just finished creating or editing a skill, offer to sync

## Workflow

### Step 1: Set Up Git

Configure git credentials and clone the repo:

```bash
# Configure git identity
git config --global user.email "graehamwatts@gmail.com"
git config --global user.name "Graehamwatts"

# Clone the repo (token is needed for push access)
git clone https://Graehamwatts:<TOKEN>@github.com/Graehamwatts/skills.git /tmp/skills-repo
```

**Getting the token:** The PAT is a classic token named "Cowork Push" stored at
https://github.com/settings/tokens. If you need the token value:

1. Check if it's already in the git remote URL of an existing clone
2. If not, navigate to GitHub settings via Chrome and look for the "Cowork Push" token
3. If the token was revoked or expired, create a new classic token with `repo` scope

### Step 2: Identify What Changed

Compare the current skills in Cowork against what's in the repo:

```bash
# Skills live at this path in Cowork
SKILLS_PATH="/sessions/*/mnt/.claude/skills"

# Compare each skill directory
for skill in $SKILLS_PATH/*/; do
  skill_name=$(basename "$skill")
  # diff against the repo version
done
```

Focus on skills that were actually modified — don't push unchanged files.
The skill directories in Cowork are read-only mounts, so read file contents
with Python and write them to the cloned repo.

### Step 3: Copy and Push

Use Python to copy files (the Cowork mount is read-only so `cp` may not work
for writing into those directories, but reading from them is fine):

```python
import os, shutil

skills_src = "<cowork-skills-path>"
skills_dst = "/tmp/skills-repo/skills"

for skill in os.listdir(skills_src):
    src = os.path.join(skills_src, skill)
    dst = os.path.join(skills_dst, skill)
    for root, dirs, files in os.walk(src):
        rel = os.path.relpath(root, src)
        dst_dir = os.path.join(dst, rel) if rel != '.' else dst
        os.makedirs(dst_dir, exist_ok=True)
        for f in files:
            with open(os.path.join(root, f), 'rb') as sf:
                data = sf.read()
            with open(os.path.join(dst_dir, f), 'wb') as df:
                df.write(data)
```

Then commit and push:

```bash
cd /tmp/skills-repo
git add skills/
git status --short

# Write a descriptive commit message
git commit -m "Update skills: <list what changed>"
git push origin main
```

### Step 4: Handle Push Protection

GitHub may block pushes if files contain secrets (API keys, tokens, etc.).
If this happens:

1. Check the error message for which file and line contains the secret
2. Replace the secret with a placeholder like `YOUR_TOKEN_HERE`
3. Amend the commit and push again

This is common with skills that reference API tokens in their documentation
(like the CMA publishing skill).

### Step 5: Verify

After pushing, confirm by checking the repo:

```bash
git log --oneline -1  # Show the commit
```

Optionally navigate to https://github.com/Graehamwatts/skills in Chrome to
visually confirm.

## Important Notes

- **Token security:** Never commit the PAT itself into skill files. Use
  placeholders in documentation and pass the token only via git remote URLs
  or environment variables.
- **Read-only mount:** The Cowork skills directory is a read-only mount.
  Always clone the repo to `/tmp/` or the working directory, copy files in,
  and push from there.
- **Network:** The sandbox can reach `github.com` for git operations but
  `api.github.com` and `objects.githubusercontent.com` may be blocked.
  Use git clone/push over HTTPS, not the GitHub API.
- **Built-in skills:** The repo should contain ALL skills — both custom
  (cma-generator, etc.) and built-in (docx, pdf, pptx, xlsx, schedule,
  setup-cowork). Push everything so the full collection is available on
  any machine that clones the repo.

## Repo Structure

```
Graehamwatts/skills/
├── skills/
│   ├── cma-generator/        (custom - CMA reports)
│   ├── disclosure-analyzer/  (custom - inspection review)
│   ├── docx/                 (built-in - Word docs)
│   ├── ghl-crm-audit/        (custom - GHL CRM)
│   ├── github-repo-analyzer/ (custom - repo analysis)
│   ├── github-skill-sync/    (this skill)
│   ├── offer-analyzer/       (custom - RE offers)
│   ├── pdf/                  (built-in - PDF handling)
│   ├── pptx/                 (built-in - presentations)
│   ├── remotion/             (original fork - Remotion rules)
│   ├── remotion-video/       (custom - React video)
│   ├── schedule/             (built-in - scheduled tasks)
│   ├── setup-cowork/         (built-in - Cowork setup)
│   ├── skill-creator/        (custom - skill development)
│   ├── social-media-analyzer/(custom - social reporting)
│   ├── video-creator/        (custom - ffmpeg video)
│   └── xlsx/                 (built-in - spreadsheets)
├── src/
├── README.md
├── package.json
└── tsconfig.json
```
