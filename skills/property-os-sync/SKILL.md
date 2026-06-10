---
name: property-os-sync
description: "Property OS specification sync engine for Graeham Watts. Reads, writes, and version-controls the Property OS / PropCast / PropClose / PropFlow / PropReach / Property IQ / Wattson specifications stored in Graeham's Obsidian vault at C:\\Users\\Graeham Watts\\Documents\\Obsidian\\PropIQ. Use ANY time the user mentions: Property OS, PropertyIQ, PropCast, PropClose, PropFlow, PropReach, Property IQ, Wattson, master brain, spec update, update spec, update Property OS, edit the spec, sync Obsidian, push Property OS, push specs to GitHub, back up Property OS, restore Property OS, pull Property OS from GitHub, or anything related to reading or writing the Property OS module specifications. Also trigger when the user pastes a new version of any spec, asks 'what does the spec say about X', wants to add a new module spec, or asks for a diff between current specs and a previous version."
---

# Property OS Sync

Read, update, and version-control the Property OS module specifications stored in Graeham's Obsidian vault. Single source of truth lives in the vault on his Mac Studio + Windows (synced via Obsidian Sync). Disaster-recovery / version history lives in the `Graehamwatts/property-os` GitHub repo.

## What This Skill Manages

The Property OS specification suite covers the entire platform:

| Module | Purpose | Vault path |
|---|---|---|
| PropertyIQ Master Brain | Parent strategic specification | `00 - PropIQ Master/PropIQ-Master-Brain.md` |
| PropCast Master Brain | Market intelligence module | `01 - Modules/PropCast/PropCast-Master-Brain.md` |
| PropCast Intelligence | PropCast intelligence layer detail | `01 - Modules/PropCast/PropCast-Intelligence.md` |
| PropClose Master Brain | Transaction management module | `01 - Modules/PropClose-Master-Brain.md` |
| PropFlow Master Brain | CRM and pipeline module | `01 - Modules/PropFlow-Master-Brain.md` |
| PropReach Module 2 Op Spec | Paid amplification module | `01 - Modules/PropReach-Module-2-Operational-Spec.md` |
| Property IQ Search Master Brain | Search and discovery module | `01 - Modules/Property-IQ-Search-Master-Brain.md` |
| Wattson Master Brain | Autonomous AI agent strategy | `02 - Wattson/Wattson-Master-Brain-v3.3.md` |
| Wattson Playbook Library | Wattson operational playbooks | `02 - Wattson/Wattson-Playbook-Library-v1.0.md` |

Vault root on Windows: `C:\Users\Graeham Watts\Documents\Obsidian\PropIQ\`
Vault root on Mac: `~/Documents/Obsidian/PropIQ/` (or wherever Obsidian Sync places it)

## Sync Architecture

```
                     [ Chat: user updates spec ]
                                  │
                                  ▼
                  ┌─────────────────────────────────┐
                  │   property-os-sync skill        │
                  │   1. Write to vault file        │
                  │   2. Commit + push to GitHub    │
                  └─────────────────────────────────┘
                                  │
            ┌─────────────────────┴────────────────────┐
            ▼                                          ▼
   [ Obsidian Sync ]                          [ GitHub: Graehamwatts/property-os ]
            │                                          │
   Mac Studio ◄──► Windows                  Version history + disaster recovery
```

- **Cross-device sync (Mac ↔ Windows):** Handled by Obsidian Sync (paid service), not by this skill. This skill only writes to the vault folder on whichever machine is running.
- **Version history:** Every spec change goes to GitHub with a timestamped commit message.
- **Disaster recovery:** If the vault gets corrupted or you want to roll back, this skill can pull the latest from GitHub.

## CRITICAL: Step 0 — Load the GitHub PAT

Before any GitHub operation, load the stored PAT (same pattern as `github-skill-sync`):

```bash
PAT_FILE=$(ls /sessions/*/mnt/outputs/.claude-credentials/github-pat.txt 2>/dev/null | head -1)
if [ -z "$PAT_FILE" ] || [ ! -f "$PAT_FILE" ]; then
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
- `PAT_LOADED` → use silently. NEVER print the token. Proceed.
- `PAT_MISSING` / `PAT_FILE_NOT_FOUND` → ask the user once for a fresh PAT (classic, `repo` scope, 90-day expiration). Save with `printf '%s\n' "$NEW_TOKEN" > "$PAT_FILE"` and continue.
- 401 on push/pull → token revoked. Ask for fresh one, save, retry.

**Token hygiene:** never print, never commit, only inline in remote URL, scrub via `git remote set-url` after.

## CRITICAL: Step 1 — Confirm vault folder is mounted

The skill needs read/write access to the vault path. If not already mounted in this session, request it:

```
mcp__cowork__request_cowork_directory({"path": "C:\\Users\\Graeham Watts\\Documents\\Obsidian"})
```

In bash, the mounted vault appears at `/sessions/<session-id>/mnt/Obsidian/`. The PropIQ subfolder is at `/sessions/<session-id>/mnt/Obsidian/PropIQ/`.

For Read/Write/Edit/Grep tools, always use the **Windows path** form: `C:\Users\Graeham Watts\Documents\Obsidian\PropIQ\<file>.md`.

## Workflow A: UPDATE A SPEC (most common operation)

User says something like "update the PropFlow spec to add a new section on lead routing" or pastes new content for a module.

### Step 1: Identify the target file

Map the user's reference to the right vault path using the table above. If ambiguous, ask which module they mean.

### Step 2: Read the current version

```
Read: C:\Users\Graeham Watts\Documents\Obsidian\PropIQ\01 - Modules\PropFlow-Master-Brain.md
```

### Step 3: Apply the edit

Use the Edit tool for surgical changes (preferred — keeps diffs minimal). Use Write only for full rewrites the user explicitly requested.

### Step 4: Push to GitHub (git stays OUT of the vault)

We DO NOT init git inside the vault. The vault is Obsidian's working folder — we keep `.git` separate. Pattern: clone the repo to `/tmp/property-os-repo`, copy the vault contents over, commit, push.

```bash
PAT=$(head -n 1 /sessions/*/mnt/outputs/.claude-credentials/github-pat.txt | tr -d '[:space:]')
git config --global user.email "graehamwatts@gmail.com"
git config --global user.name "Graehamwatts"

VAULT="/sessions/*/mnt/Obsidian/PropIQ"
REPO=/tmp/property-os-repo

# Clone fresh (or pull if already cloned this session)
rm -rf "$REPO"
git clone "https://${PAT}@github.com/Graehamwatts/property-os.git" "$REPO"

# Mirror vault contents into clone (rsync-style, deletes removed files too)
# Exclude .obsidian if it ever ends up in the PropIQ subfolder
rsync -av --delete \
    --exclude='.obsidian' \
    --exclude='.git' \
    --exclude='.gitignore' \
    --exclude='*pat*.txt' \
    --exclude='*token*.txt' \
    --exclude='*.env' \
    "$VAULT/" "$REPO/"

cd "$REPO"
git add -A
if git diff --cached --quiet; then
    echo "No changes to push"
else
    TS=$(date +"%d-%m-%Y-%H%M")  # day-first format
    git commit -m "Update <module-name>: <one-line summary> [$TS]"
    git push "https://${PAT}@github.com/Graehamwatts/property-os.git" main
fi

# Scrub token from any cached remote config
git remote set-url origin "https://github.com/Graehamwatts/property-os.git"
```

**Important:** if the vault bash mount is in a stale state (rare but happens after folder renames), use the **Read tool** with the Windows path `C:\Users\Graeham Watts\Documents\Obsidian\PropIQ\<file>.md` and **Write tool** to manually mirror. Then run only the git commit/push portion.

### Step 5: Confirm to user

Tell them what was changed, where, and link to the GitHub commit. Format: "Updated PropFlow-Master-Brain.md (added section on lead routing). Pushed to GitHub: <commit-url>."

## Workflow B: PUSH WITHOUT EDITING (safety-net daily backup)

When the user says "back up Property OS", "push Property OS to GitHub", "sync Property OS now", OR when invoked by the daily scheduled task. Same git-outside-vault pattern as Workflow A.

```bash
PAT=$(head -n 1 /sessions/*/mnt/outputs/.claude-credentials/github-pat.txt | tr -d '[:space:]')
VAULT="/sessions/*/mnt/Obsidian/PropIQ"
REPO=/tmp/property-os-repo

rm -rf "$REPO"
git clone "https://${PAT}@github.com/Graehamwatts/property-os.git" "$REPO"

rsync -av --delete \
    --exclude='.obsidian' \
    --exclude='.git' \
    --exclude='.gitignore' \
    --exclude='*pat*.txt' \
    --exclude='*token*.txt' \
    --exclude='*.env' \
    "$VAULT/" "$REPO/"

cd "$REPO"
git add -A
if git diff --cached --quiet; then
    echo "No changes to commit — vault is in sync with GitHub"
    exit 0
fi

CHANGED=$(git diff --cached --name-only | head -10 | tr '\n' ', ')
TS=$(date +"%d-%m-%Y-%H%M")
git commit -m "Daily sync [$TS] — files: $CHANGED"
git push "https://${PAT}@github.com/Graehamwatts/property-os.git" main
git remote set-url origin "https://github.com/Graehamwatts/property-os.git"
```

## Workflow C: ADD A NEW MODULE SPEC

User says "add a new module called X" or pastes content for a new module.

1. Decide where it goes:
   - Standalone module → `01 - Modules/<ModuleName>-Master-Brain.md`
   - Sub-doc of existing module → `01 - Modules/<ParentModule>/<DocName>.md`
   - Wattson-related → `02 - Wattson/<DocName>.md`
2. Write the file with appropriate frontmatter and content.
3. Update `README.md` to add a link to the new doc under the right section.
4. Run Workflow B to push everything to GitHub.

## Workflow D: RESTORE FROM GITHUB

User says "pull Property OS from GitHub", "restore Property OS", "I think I broke the vault, can we roll back".

```bash
PAT=$(head -n 1 /sessions/*/mnt/outputs/.claude-credentials/github-pat.txt | tr -d '[:space:]')
rm -rf /tmp/property-os-restore
git clone --depth 1 "https://${PAT}@github.com/Graehamwatts/property-os.git" /tmp/property-os-restore
```

Then ask the user before overwriting:
- Show them what's different (`diff -r /tmp/property-os-restore "$VAULT" | head -50`)
- Get explicit confirmation
- Copy files back into vault on their approval

For an older snapshot, use `git log` in the clone to show available commits, let them pick a hash, then `git checkout <hash>` before copying.

## Workflow E: READ A SPEC

User asks "what does the PropCast spec say about X" or "show me the Wattson playbook for Y".

1. Map the reference to the vault path.
2. Read the file.
3. Quote the relevant section briefly. Don't dump the whole file unless asked.

## File-naming Conventions

- Module master brains: `<Module>-Master-Brain.md` (no version suffix unless multiple co-exist, like Wattson)
- Sub-documents inside a module folder: descriptive name (e.g., `PropCast-Intelligence.md`)
- Operational specs: `<Module>-Module-<N>-Operational-Spec.md`
- Versioned files: include version in filename (e.g., `Wattson-Master-Brain-v3.3.md`) and update README links when the version bumps

## Frontmatter Standard (when creating new spec docs)

When writing a new spec from scratch (vs. converted from .docx), use this frontmatter:

```yaml
---
module: PropFlow
type: master-brain
version: 1.0
status: living-document
last-updated: 2026-05-08
owner: Graeham Watts
---
```

This makes the docs queryable in Obsidian via dataview if you ever install that plugin.

## Important Notes

- **Obsidian Sync handles Mac ↔ Windows.** This skill never tries to sync between devices directly. Trust Obsidian Sync.
- **Edit on the machine you're on.** If you update from chat on Windows, Obsidian Sync will propagate to Mac. The reverse also works.
- **GitHub is for version history, not real-time sync.** The repo gets pushed on every spec edit and via the daily scheduled task as a safety net.
- **Don't commit the .obsidian config folder.** The vault root is one level up from `PropIQ/`. The git repo is rooted at `PropIQ/`, so `.obsidian/` (which is in `Obsidian/`) is naturally excluded.
- **Commit messages are day-first format:** `DD-MM-YYYY-HHMM` to match `github-skill-sync` convention.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `git push` returns 401 | PAT expired or revoked | Run Workflow Step 0 again, save new PAT |
| `git push` returns 403 | PAT lacks `repo` scope | Generate new PAT with correct scope |
| Files don't appear on Mac after Windows edit | Obsidian Sync paused or signed out | User opens Obsidian on Mac, checks sync status indicator |
| Image broken in Obsidian | Path mismatch after a move | Re-run image-path normalizer (Python script in initial-setup notes) |
| Conflict on push | Mac edited the file independently | Pull first (`git pull --rebase`), resolve conflict, push |

## Repo Structure

```
Graehamwatts/property-os/
├── README.md
├── 00 - PropIQ Master/
│   └── PropIQ-Master-Brain.md
├── 01 - Modules/
│   ├── PropCast/
│   │   ├── PropCast-Master-Brain.md
│   │   └── PropCast-Intelligence.md
│   ├── PropClose-Master-Brain.md
│   ├── PropFlow-Master-Brain.md
�