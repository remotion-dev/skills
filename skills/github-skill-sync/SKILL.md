---
name: github-skill-sync
description: "Auto-pull and auto-push to/from Graehamwatts/skills AND Graehamwatts/online-content GitHub repos using a workspace-stored token. Use ANY time a skill is created/modified, online content is published, the user says 'push skills', 'sync skills', 'update the repo', 'push to GitHub', 'save to GitHub', 'pull from repo', 'sync from GitHub', 'restore from backup'. ALWAYS trigger at the start of a session that will modify repo files (to pull) and at the end of any session that modified files (to push). Trigger proactively after skill-creator or html-email or cma-generator or any content-producing skill — don't wait for the user to ask."
---

# GitHub Sync — Skills + Online Content

Pull and push to/from two GitHub repos using git CLI and a workspace-stored token.

## The two repos

| Repo | Local path | What's there |
|---|---|---|
| `Graehamwatts/skills` | `Documents/Claude/Skills/` | 46 skill folders, docs, dashboard CSS, repo-level CLAUDE.md |
| `Graehamwatts/online-content` | `Documents/Claude/Online Content/` | Published HTML — emails, newsletters, weekly calendar dashboards |

**Placement rule:** skill files go to `Skills/skills/<skill-name>/`. Published HTML output (emails, newsletters, dashboards) goes to `Online Content/`. Never confuse these. The `html-email` skill is a TOOL that lives in `Skills/`; the EMAILS it produces go to `Online Content/emails/`.

## Step 0 — Find the token

Check these locations in order. First match wins.

```bash
# 1. Skills clone (preferred)
TOKEN_FILE="$HOME/Documents/Claude/Skills/github-token.txt"
[ -f "$TOKEN_FILE" ] || TOKEN_FILE=""

# 2. Online Content clone (fallback)
[ -z "$TOKEN_FILE" ] && [ -f "$HOME/Documents/Claude/Online Content/github-token.txt" ] && \
    TOKEN_FILE="$HOME/Documents/Claude/Online Content/github-token.txt"

# 3. Cowork bash sandbox path
[ -z "$TOKEN_FILE" ] && \
    TOKEN_FILE=$(ls /sessions/*/mnt/Documents/Claude/Skills/github-token.txt 2>/dev/null | head -1)

# 4. Legacy session credentials (deprecated but still respected)
[ -z "$TOKEN_FILE" ] && \
    TOKEN_FILE=$(ls /sessions/*/mnt/outputs/.claude-credentials/github-pat.txt 2>/dev/null | head -1)

if [ -z "$TOKEN_FILE" ]; then
    echo "PAT_FILE_NOT_FOUND — ask Graeham for a fresh classic PAT (repo scope, 90-day expiry)"
    exit 1
fi

PAT=$(head -n 1 "$TOKEN_FILE" | tr -d '[:space:]')
[ -z "$PAT" ] && echo "PAT_FILE_EMPTY" && exit 1
```

**Token security rules — never violate:**
- Never print the token value in chat
- Never commit the token to ANY file in either repo
- Use it only in inline git URLs: `https://${PAT}@github.com/...`
- Don't `git config` the token into stored credentials
- If a push returns `401 Unauthorized`, the token is invalid → ask for a fresh one and rewrite `github-token.txt`

## Workflow A — PULL (start of every session that touches repo files)

```bash
# Skills repo
cd "/sessions/<session-id>/mnt/Documents/Claude/Skills"
git pull origin main

# Online Content repo
cd "/sessions/<session-id>/mnt/Documents/Claude/Online Content"
git pull origin main
```

Always pull before making changes. Skipping this leads to the kind of stale-workspace bug that wasted hours on 2026-05-04 (workspace was 70+ commits behind GitHub for two weeks because previous Composio-based pushes never reached the local clone).

## Workflow B — PUSH (end of any session that modified files)

### B.1 Push to skills repo

```bash
cd "/sessions/<session-id>/mnt/Documents/Claude/Skills"
git config core.filemode false              # one-time, prevents Windows ACL noise
git config user.email "graehamwatts@gmail.com"
git config user.name "Graehamwatts"

git status -s                                 # confirm what's changing
git add <specific files or skills/<skill-name>/>
git commit -m "Specific change description"

PAT=$(head -n 1 github-token.txt | tr -d '[:space:]')
git push "https://${PAT}@github.com/Graehamwatts/skills.git" main
```

### B.2 Push to online-content repo

```bash
cd "/sessions/<session-id>/mnt/Documents/Claude/Online Content"
git add <files>
git commit -m "Description"
PAT=$(head -n 1 github-token.txt | tr -d '[:space:]')
git push "https://${PAT}@github.com/Graehamwatts/online-content.git" main
```

## Windows mount gotchas — read before debugging

The `Documents/Claude/` folder is a Windows-mounted folder. Three things to know:

1. **`Write` tool can confuse git's stat cache.** If you use the `Write` tool to update a file but `git status` shows clean, write it via bash instead (`cat > file <<EOF ... EOF`). This updates mtime in a way git detects. Or run `git update-index --really-refresh` to force a re-stat.

2. **`.git/index.lock` may be uncreatable** on the Windows mount in rare conditions. If a git operation fails with "Operation not permitted" on a `.lock` file, fall back to working in `/tmp` clones and Python-copying results back. Reference pattern is `shutil.copytree(src, dst)`.

3. **`core.filemode false` is mandatory** — both clones already have this set. Don't unset it. Without it, every Windows-side file copy looks "modified" to git and creates noise.

## Push-protection blocks

GitHub's secret scanner can block pushes if a file contains a token-like string:

1. Look at the error to find which file/line has the secret
2. Replace with `YOUR_TOKEN_HERE` placeholder
3. `git add`, `git commit --amend --no-edit`, push again

## When to skip the pull/push pattern (rare)

You can skip the pull at session start ONLY if:
- The session is purely conversational (no file changes) AND
- You're certain no other recent session modified the repos

You can skip the push at session end ONLY if:
- Nothing was modified in either repo

If in doubt, pull. It's a 5-second operation and it prevents real bugs.

## Composio fallback (use only when git CLI is broken)

If git CLI fails for any reason (network issue, sandbox restriction), the Composio MCP can push individual files directly:

```
mcp__c7e34fd4-916e-46be-bd5f-6edacce5c708__COMPOSIO_MULTI_EXECUTE_TOOL
  tools: [{
    tool_slug: "GITHUB_CREATE_OR_UPDATE_FILE_CONTENTS",
    arguments: {
      owner: "Graehamwatts",
      repo: "skills" | "online-content",
      path: "<path/in/repo>",
      message: "<commit message>",
      content: "<file content as string>"
    }
  }]
```

**WARNING:** Composio pushes bypass the local clone. After any Composio push, run `git pull` in the affected local clone to keep them in sync. Otherwise the local clone goes silently stale (this is exactly how the 70+ commit drift happened).

## Optional Tier 2 backup — local rolling

If you want a "undo today's mistake" safety net beyond git history, copy the skill's old version to a rolling backup folder before overwriting:

```bash
BACKUP_DIR="$HOME/Documents/Claude/Skills/.local-backups/<skill-name>"
mkdir -p "$BACKUP_DIR"
[ -d "$BACKUP_DIR/backup-2" ] && rm -rf "$BACKUP_DIR/backup-2"
[ -d "$BACKUP_DIR/backup-1" ] && mv "$BACKUP_DIR/backup-1" "$BACKUP_DIR/backup-2"
cp -r "skills/<skill-name>" "$BACKUP_DIR/backup-1"
```

The `.local-backups/` folder is gitignored. Optional. Skip unless explicitly asked or operating on a particularly important skill.

## Optional Tier 3 backup — Box rolling archive

If Box MCP is available and the user wants off-machine backup, zip the skill's old version and upload to `Box:/Claude Skills Archive/<skill-name>/archive-1.zip` (rotating archive-1 → archive-2, dropping the older). See git history of this skill before 2026-05-04 for the original Box rotation pattern. **Do not perform this by default** — only when asked.

## Quick reference card

| User says | Do |
|---|---|
| "push skills" / "sync skills" | Pull both → make changes → push to whichever repo changed |
| "pull skills" / "sync from GitHub" | Pull both repos |
| "push to online content" | Pull online-content → make changes → push |
| "back up skills" | Pull → push → optionally Tier 2 local backup |
| "restore skills" / "rollback" | git log → git revert <commit> → push, OR pull from `.local-backups/` |
| (skill modified, no explicit request) | Push to skills repo at end of session |
| (email/newsletter/dashboard generated) | Push to online-content repo at end of session |
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       