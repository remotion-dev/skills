# Publishing via Composio — Standard Pattern

> **Single source of truth for how Graeham's skills push files to GitHub.**
> All publishing-capable skills MUST follow this pattern. Never use GitHub Desktop, never use `git push` from the agent's bash sandbox.

---

## Why this exists

Graeham's content engine writes published artifacts (dashboards, reports, listing pages, blog posts, HTML emails) to two GitHub repos:

| Repo | Purpose | Published as |
|---|---|---|
| `Graehamwatts/online-content` | Public-facing assets | GitHub Pages → `https://graehamwatts.github.io/online-content/` |
| `Graehamwatts/skills` | Skill source code + shared references | Versioned skill library |

Without a single shared pattern, every skill ends up reinventing the auth dance, getting it wrong, leaving uncommitted files in the local sandbox, or worse — pushing with the wrong account.

This file is the canonical pattern. Reference it from every publishing skill.

---

## The hard rules

1. **Use Composio, not GitHub Desktop or local git.** The agent's bash sandbox cannot reliably push to private repos, and GitHub Desktop is not scriptable. Composio is auth'd once and works from any agent run.
2. **Account is `github_spar-devata`** (default). It's connected to Graeham's `Graehamwatts` GitHub account.
3. **Owner is always `Graehamwatts`** (capitalization matters for some operations — case-insensitive in API but use the canonical form).
4. **Branch is always `main`** unless the skill explicitly asks the user for a feature branch.
5. **One atomic commit per logical change.** Use `GITHUB_COMMIT_MULTIPLE_FILES` even for a single file — its retry-on-race-condition is more reliable than `GITHUB_CREATE_OR_UPDATE_FILE_CONTENTS`.

---

## The pattern (Python, in Composio remote workbench)

```python
result, error = run_composio_tool(
    tool_slug='GITHUB_COMMIT_MULTIPLE_FILES',
    arguments={
        'owner': 'Graehamwatts',
        'repo': 'online-content',          # or 'skills'
        'branch': 'main',
        'message': 'descriptive commit message',
        'upserts': [
            {
                'path': 'path/in/repo/filename.html',
                'content': file_content_str,
                'encoding': 'utf-8'         # or 'base64' for binary
            },
            # ... more files in same atomic commit
        ]
    },
    account='github_spar-devata'
)

if error:
    raise RuntimeError(f"Composio commit failed: {error}")

# Normalize response
data = result.get('data', {})
if isinstance(data, dict) and 'data' in data:
    data = data['data']

commit_url = data.get('commit_url')
commit_sha = data.get('new_commit_sha')
print(f"Pushed: {commit_url}")
```

## The pattern (top-level orchestrator using COMPOSIO_MULTI_EXECUTE_TOOL)

If the skill orchestrates from chat-level rather than via the workbench, use `COMPOSIO_MULTI_EXECUTE_TOOL`:

```json
{
  "tools": [{
    "tool_slug": "GITHUB_COMMIT_MULTIPLE_FILES",
    "arguments": {
      "owner": "Graehamwatts",
      "repo": "online-content",
      "branch": "main",
      "message": "your commit message",
      "upserts": [{
        "path": "path/file.html",
        "content": "...",
        "encoding": "utf-8"
      }]
    },
    "account": "github_spar-devata"
  }],
  "sync_response_to_workbench": false
}
```

---

## Standard paths

### `Graehamwatts/online-content` (published artifacts)

| Path pattern | Use for |
|---|---|
| `dashboards/single-topic/YYYY-MM-DD-slug-production.html` | One-topic deep-dive dashboards (CMA, listing, market deep-dive) |
| `dashboards/weekly-calendars/YYYY-MM-DD-production-calendar.html` | Weekly content calendars |
| `emails/YYYY-MM-DD-slug.html` | HTML emails (briefs, proposals, listing launches) |
| `listings/YYYY-MM-DD-listing-slug.html` | Listing pages |
| `reports/YYYY/MM/slug.html` | Recurring reports (social, CRM audit) |

Date prefix = the publish date (NOT today's date). For weekly calendars covering Mon May 12, the file is `2026-05-11-production-calendar.html` (the auto-run fires Mon May 11 at 11:08 AM PT).

### `Graehamwatts/skills` (skill source)

| Path pattern | Use for |
|---|---|
| `skills/{skill-name}/SKILL.md` | The skill's primary instruction file |
| `skills/{skill-name}/scripts/...` | Skill-specific Python/bash helpers |
| `skills/shared-references/{name}.md` | Cross-skill shared docs (this file lives here) |
| `skills/shared-references/identity.json` | Single-source brand identity |

---

## Brand integrity check (run BEFORE every publish)

The agent MUST verify the file does not contain blocklisted strings before pushing:

```python
BLOCKLIST = ['02015066']   # wrong DRE# — leaked 11+ times historically
for bad in BLOCKLIST:
    if bad in file_content:
        raise ValueError(f'Brand integrity check failed — blocklisted token: {bad}')
```

The correct DRE is `01466876`. The single source for all brand fields is `skills/shared-references/identity.json`.

---

## Auth troubleshooting

If `GITHUB_COMMIT_MULTIPLE_FILES` returns an auth error:

1. Confirm the account is connected: call `COMPOSIO_SEARCH_TOOLS` with a GitHub query and check `toolkit_connection_statuses`. Both `github_spar-devata` (default) and `github_porose-smew` are connected as of 2026-05-03.
2. If neither account is active, run `COMPOSIO_MANAGE_CONNECTIONS` and ask Graeham to re-auth.
3. Never fall through to `git push` from bash — the sandbox does not have valid GitHub credentials and even if it did, the result wouldn't be reproducible across sessions.

---

## Verification after push

Best practice: read the file back via `GITHUB_GET_REPOSITORY_CONTENT` after committing. Check the SHA matches the `new_commit_sha` returned, and spot-check a known content marker. This catches silent corruption from encoding mismatches.

---

## Common pitfalls

- **422 "Reference cannot be updated"** → race condition with another commit landing on the same branch. Composio retries automatically up to `max_retries` (default 3). If still failing, run sequentially.
- **422 "Failed to create tree: GitRPC::BadObjectState"** → trying to delete a non-existent file. Pre-check with `GITHUB_GET_A_TREE`.
- **Empty `upserts` AND empty `deletes`** → "At least one file must be specified" error. Always include at least one operation.
- **Wrong account** → if you pushed and the commit appears under a wrong author, verify `account='github_spar-devata'` was passed.

---

## Last verified

- Pattern verified working: 2026-05-03 (commits 99787da1, 6346f652, 58c13e71)
- Active connection: `github_spar-devata`
- Default branch on both repos: `main`
