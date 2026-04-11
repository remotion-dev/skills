---
name: github-skill-sync
description: "Auto-push and auto-pull skills to/from the Graehamwatts/skills GitHub repo using a stored credential, with three-tier rolling backup (GitHub + local + Box). Use this skill ANY time a skill is created, updated, modified, or improved; the user says 'push skills', 'sync skills', 'update the repo', 'push to GitHub', 'save skills to GitHub', 'pull skills from repo', 'sync from GitHub', 'restore from backup', 'restore skills'; after using skill-creator to build or modify a skill; when the user asks to back up or version-control their skills. Also trigger proactively after ANY skill creation or modification workflow completes — don't wait for the user to ask."
---

# GitHub Skill Sync

Push and pull skill changes to/from the `Graehamwatts/skills` GitHub repository, with automatic three-tier backup. Uses a stored credential file so future sessions don't require token paste.

## Three-Tier Backup Architecture

| Tier | Where | Purpose | Retention |
|---|---|---|---|
| 1 — Live | GitHub `Graehamwatts/skills` main branch | Source of truth, version-controlled, diffable | Forever (full git history) |
| 2 — Local rolling | `<outputs>/.claude-credentials/skills-current`, `-backup-1`, `-backup-2` | Fast "undo today's mistake" rollback | Last 3 snapshots, oldest auto-deleted |
| 3 — Box rolling archive | Box: `/Claude Skills Archive/<skill-name>/archive-1.zip`, `archive-2.zip` | Off-machine rollback if local copies are lost | Last 2 snapshots per skill, oldest auto-deleted |

**The flow on every push:**
1. Clone GitHub repo → `/tmp/skills-repo`
2. Capture the OLD version of any skill being updated, zip it
3. Rotate Box archives for that skill (delete `archive-2.zip`, rename `archive-1.zip` → `archive-2.zip`, upload new zip as `archive-1.zip`)
4. Copy the NEW version into the cloned repo
5. Commit and push to GitHub
6. Run local rolling backup (rotates the 3 local snapshots)

Brand-new skills (no prior version in repo) skip Step 3 — there's nothing yet to archive. Box archives are capped at 2 per skill so the folder doesn't grow forever.

**Date stamping:** All archive metadata and commit messages use day-first format: `DD-MM-YYYY-HHMM` (e.g., `11-04-2026-2245`).

## CRITICAL: Step 0 — Read the credential file FIRST

Before doing anything else, load the GitHub PAT from the persistent credential file at:

```
/sessions/<session-id>/mnt/outputs/.claude-credentials/github-pat.txt
```

```bash
PAT_FILE=$(ls /sessions/*/mnt/outputs/.claude-credentials/github-pat.txt 2>/dev/null | head -1)
if [ -z "$PAT_FILE" ] || [ \! -f "$PAT_FILE" ]; then
    echo "PAT_FILE_NOT_FOUND"
else
    PAT=$(head -n 1 "$PAT_FILE" | tr -d '[:space:]')
    if [ -z "$PAT" ] || [ "$PAT" = "PASTE_YOUR_GITHUB_PAT_HERE" ]; then
        echo "PAT_MISSING"
    else
        echo "PAT_LOADED"
    fi
fi
```

**Decision tree:**
- `PAT_LOADED` → use it silently. **Never** print the token in chat. Proceed.
- `PAT_MISSING` or `PAT_FILE_NOT_FOUND` → ask the user once for a fresh PAT (classic, `repo` scope, 90-day expiration), then save with `printf '%s\n' "$NEW_TOKEN" > "$PAT_FILE"` and continue.
- If a push/pull returns `401 Unauthorized` → token is invalid/revoked/expired. Tell the user, ask for a fresh one, save it, retry.

**Token hygiene rules:**
- Never print the token in chat output
- Never commit the token to any repo file
- Only use it inline in git remote URLs; scrub via `git remote set-url origin "https://github.com/..."` after clone
- Never `git config` the token into the repo's stored credentials

## How It Works

This skill uses `git` over HTTPS with a stored Personal Access Token to clone, copy in updated skills, and push/pull. The token lives at `<outputs>/.claude-credentials/github-pat.txt` and is managed transparently.

## When to Run

- **After creating a new skill** — push immediately
- **After modifying an existing skill** — push the change
- **On user request** — "push to GitHub", "sync the repo", "back up my skills", "pull the latest", etc.
- **Proactively** — if you just finished editing a skill, offer to sync without waiting to be asked

## Workflow A: PUSH (local → GitHub) with Box rotation

### Step 1: Set up git and clone

```bash
PAT=$(head -n 1 /sessions/*/mnt/outputs/.claude-credentials/github-pat.txt | tr -d '[:space:]')
git config --global user.email "graehamwatts@gmail.com"
git config --global user.name "Graehamwatts"
rm -rf /tmp/skills-repo
git clone "https://${PAT}@github.com/Graehamwatts/skills.git" /tmp/skills-repo
cd /tmp/skills-repo && git remote set-url origin "https://github.com/Graehamwatts/skills.git"
```

### Step 2: Identify what changed

The Cowork skills mount is read-only at `/sessions/*/mnt/.claude/skills/<skill-name>/`. Focus only on skills modified in this session.

### Step 3: Capture OLD versions and rotate Box archives (BEFORE copying new files)

For each skill being updated, capture the existing version from the cloned repo (this is what's about to be replaced) and run the Box rolling rotation.

```python
import os, shutil, datetime

skills_being_updated = ["<skill-name>"]  # populate from session changes
ts = datetime.datetime.now().strftime("%d-%m-%Y-%H%M")  # day-first

archives = []
for sk in skills_being_updated:
    old_dir = f"/tmp/skills-repo/skills/{sk}"
    if not os.path.isdir(old_dir):
        continue  # brand new skill, nothing to archive
    archive_path = f"/tmp/{sk}-{ts}.zip"
    shutil.make_archive(archive_path[:-4], 'zip', old_dir)
    archives.append((sk, archive_path, ts))
```

Then for each archive, perform the Box rolling rotation using the Box MCP tools:

```
For each (skill_name, archive_path, ts) in archives:

  1. Ensure folder structure exists in Box:
     - mcp__box__search_folders_by_name with name="Claude Skills Archive"
       → if not found, mcp__box__create_folder under Box root
     - mcp__box__search_folders_by_name with name=<skill_name>
       inside "Claude Skills Archive"
       → if not found, mcp__box__create_folder

  2. ROTATE existing archives in that folder:
     - mcp__box__list_folder_content_by_folder_id to inspect current contents
     - If "archive-2.zip" exists → DELETE it (oldest, gets overwritten)
       Box deletion is gated: ask the user "I need to delete the oldest
       Box archive (archive-2.zip for <skill_name>) to make room. OK?"
       After approval, perform deletion via Box MCP delete tool.
     - If "archive-1.zip" exists → rename to "archive-2.zip"
       Same for "archive-1.txt" → "archive-2.txt"
       (use mcp__box__update_file_properties to rename)

  3. Upload the new zip as "archive-1.zip":
     - mcp__box__upload_file with archive_path,
       target folder = "Claude Skills Archive/<skill_name>",
       filename = "archive-1.zip"

  4. Upload a metadata file "archive-1.txt" containing:
       Original date: <skill_name>-<DD-MM-YYYY-HHMM>.zip
       Commit hash being archived: <hash from `git log -1 --format=%H` in /tmp/skills-repo>
       Change description: <one-line summary>
     This way you can see WHEN each archive was made without unzipping.
```

Box folder structure (after rotation):
```
Box Root/
  Claude Skills Archive/
    cma-generator/
      archive-1.zip          (most recent old version)
      archive-1.txt          (metadata: date, commit hash, change notes)
      archive-2.zip          (one version older)
      archive-2.txt
    video-script-creation-engine/
      archive-1.zip
      archive-1.txt
      archive-2.zip
      archive-2.txt
    [one folder per skill]
```

**Only after the Box rotation succeeds, proceed to Step 4.**

If the Box upload or rotation fails (network, auth, quota), STOP and tell the user before pushing to GitHub. Do not silently lose the archive opportunity.

### Step 4: Copy new files into the clone

```python
import os
src = "/sessions/<session-id>/mnt/.claude/skills/<skill-name>"
dst = "/tmp/skills-repo/skills/<skill-name>"
for root, dirs, files in os.walk(src):
    rel = os.path.relpath(root, src)
    dst_dir = os.path.join(dst, rel) if rel \!= '.' else dst
    os.makedirs(dst_dir, exist_ok=True)
    for f in files:
        with open(os.path.join(root, f), 'rb') as sf:
            data = sf.read()
        with open(os.path.join(dst_dir, f), 'wb') as df:
            df.write(data)
```

### Step 5: Commit and push

```bash
cd /tmp/skills-repo
git add skills/
git status --short
git commit -m "Update skills: <list what changed>"
PAT=$(head -n 1 /sessions/*/mnt/outputs/.claude-credentials/github-pat.txt | tr -d '[:space:]')
git push "https://${PAT}@github.com/Graehamwatts/skills.git" main
```

The token only appears in the inline push URL — never persisted in git config.

### Step 6: Handle push protection

GitHub may block pushes if files contain secrets:
1. Check error for which file/line has the secret
2. Replace with placeholder like `YOUR_TOKEN_HERE`
3. `git add`, `git commit --amend --no-edit`, push again

### Step 7: Trigger local rolling backup

After every successful push, run:
```bash
bash /sessions/*/mnt/outputs/.claude-credentials/backup-skills.sh
```

This rotates `skills-current` → `skills-backup-1` → `skills-backup-2` and pulls a fresh copy.

## Workflow B: PULL (GitHub → local sandbox)

When the user says "pull skills from the repo", "sync from GitHub", "show me what's in the repo":

```bash
PAT=$(head -n 1 /sessions/*/mnt/outputs/.claude-credentials/github-pat.txt | tr -d '[:space:]')
rm -rf /tmp/skills-repo-readonly
git clone --depth 1 "https://${PAT}@github.com/Graehamwatts/skills.git" /tmp/skills-repo-readonly
cd /tmp/skills-repo-readonly && git remote set-url origin "https://github.com/Graehamwatts/skills.git"
ls /tmp/skills-repo-readonly/skills/
```

**Important reality:** Pulling files into the sandbox does NOT install them into Cowork. Cowork loads skills from its own backend, not from filesystem. To install a pulled skill, the user must repackage it (`package_skill.py`) and run the install flow manually. Be honest about this limitation.

## Workflow C: RESTORE FROM BACKUP

**Local rolling backup (Tier 2):**
```bash
ls /sessions/*/mnt/outputs/.claude-credentials/skills-backup-1/skills/
ls /sessions/*/mnt/outputs/.claude-credentials/skills-backup-2/skills/
```

**Box archive (Tier 3):** Use Box MCP to download `archive-1.zip` or `archive-2.zip` for the relevant skill, unzip locally, and offer to push it back to the GitHub repo as a "restore" commit.

## Workflow D: BOOTSTRAP CREDENTIAL FILE

If Step 0 returns `PAT_FILE_NOT_FOUND`, the credential folder doesn't exist yet:

```bash
mkdir -p /sessions/*/mnt/outputs/.claude-credentials
```

Then ask the user for a fresh PAT and save it:
```bash
printf '%s\n' "$NEW_TOKEN" > /sessions/*/mnt/outputs/.claude-credentials/github-pat.txt
chmod 600 /sessions/*/mnt/outputs/.claude-credentials/github-pat.txt
```

## Important Notes

- **Token security:** Never commit the PAT into skill files. Use placeholders in documentation.
- **Network:** Sandbox can reach `github.com` over HTTPS. `api.github.com` may be blocked — prefer git over GitHub API calls.
- **Multiple machines:** The repo is canonical. Use `backup-skills.sh` on each machine for local Tier 2 copies.
- **Commit messages:** Short and specific. "vsce: add ElevenLabs-Ready Variant" beats "misc updates".
- **Honest about Cowork installation:** Pushing/pulling syncs the GitHub repo. It does NOT auto-install skills into Cowork — that requires a user-initiated `.skill` install flow.

## Repo Structure

```
Graehamwatts/skills/
├── skills/
│   ├── cma-generator/
│   ├── disclosure-analyzer/
│   ├── docx/
│   ├── ghl-crm-audit/
│   ├── github-repo-analyzer/
│   ├── github-skill-sync/        (this skill)
│   ├── offer-analyzer/
│   ├── pdf/
│   ├── pptx/
│   ├── remotion-video/
│   ├── schedule/
│   ├── setup-cowork/
│   ├── skill-creator/
│   ├── social-media-analyzer/
│   ├── video-creator/
│   ├── video-script-creation-engine/
│   └── xlsx/
└── README.md
```
