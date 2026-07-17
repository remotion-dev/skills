# Publishing to GitHub — Standard Pattern (direct git)

> **Single source of truth for how Graeham's skills push files to GitHub.**
> All publishing-capable skills MUST follow this pattern.
>
> **⚠️ NAMING HISTORY (2026-06-09):** this file keeps its old name `publishing-via-composio.md` so the 8+ skills that reference it keep working, but **Composio is RETIRED workspace-wide** (see `Documents\Skills LLMS\Claude\CLAUDE.md`). The canonical method is now **direct `git` push** using the PAT stored in each clone. If a skill's own text still says "push via Composio" or `GITHUB_COMMIT_MULTIPLE_FILES`, THIS file overrides it — use direct git.

---

## Where things go

| Repo | Local clone | Purpose | Published as |
|---|---|---|---|
| `Graehamwatts/online-content` | `C:\Users\Graeham Watts\Documents\Skills LLMS\Claude\Online Content` | Public-facing assets (CMAs, offers, disclosures, newsletters, dashboards) | GitHub Pages → `https://graehamwatts.github.io/online-content/` |
| `Graehamwatts/skills` | `C:\Users\Graeham Watts\Documents\Skills LLMS\Claude\Skills` | Skill source code + shared references ONLY — no outputs | Versioned skill library |

**Placement rule:** published HTML always goes in the Online Content clone, never the Skills repo. Skills are tools that PRODUCE content; outputs live in the other repo.

## The hard rules

1. **Push with direct `git`**, using the PAT from `github-token.txt` inside the relevant clone (gitignored; same token for both repos). Never GitHub Desktop, never Composio.
2. **Never print the token.** Load it into a variable; if echoing push output, scrub it: `sed "s/${PAT}/***/g"`.
3. **Brand tripwire before any Skills push:** scan staged files for the blocked DRE value listed in `identity.json`'s blocklist (exempt files: CLAUDE.md, AGENTS.md, identity.json itself, audit docs). If found anywhere else — fix first, never push. The only valid DRE is `01466876`.
4. **Never commit credentials.** `.gitignore` covers `*token*.txt`, `*password*.txt`, `ghl-pit.txt`, etc. Verify with `git diff --cached --name-only | grep -iE "token|password|pit|secret"` before committing.
5. **`.github/workflows/` files cannot be pushed with the stored PAT** (repo scope only). Use `gh` CLI credentials (they have workflow scope) for those pushes.
6. **Owner is always `Graehamwatts`, branch is always `main`** unless the skill explicitly asks the user for a feature branch.

## The pattern

```bash
cd "C:/Users/Graeham Watts/Documents/Skills LLMS/Claude/Online Content"   # or .../Skills
git add <files>
git -c user.name="Graeham Watts" -c user.email="graehamwatts@gmail.com" commit -m "Clear message"
PAT=$(tr -d '[:space:]' < github-token.txt)
git -c http.version=HTTP/1.1 push "https://${PAT}@github.com/Graehamwatts/<repo>.git" HEAD:main
```

## Reliability notes (this machine)

- Pushes intermittently fail with `curl 55 Send failure: Connection was reset`. Fixes in order: (1) retry; (2) `-c http.version=HTTP/1.1 -c http.postBuffer=157286400`; (3) clone fresh into a temp dir, `git fetch` the local repo into it, `git merge --ff-only FETCH_HEAD`, push from there.
- Stale `.git/*.lock` files happen on this Windows mount — `rm -f .git/*.lock` and retry.
- **Safety net:** a Claude Code SessionEnd hook (`~/.claude/hooks/auto-push-repos.ps1`) auto-commits and pushes both repos when a session ends, with the tripwire enforced and a mass-deletion wipe guard. Manual pushes are still fine and preferred for anything client-facing (so you can verify the URL immediately).

## After publishing

For GitHub Pages content: the live URL is `https://graehamwatts.github.io/online-content/<path>` — Pages rebuilds in ~1-2 minutes. Always give Graeham the final URL, and for client-facing pages verify it loads (and passes `content-creation-engine/scripts/verify_output_brand.py`) before sending.
