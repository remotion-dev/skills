# Shared References

**This is NOT a skill.** It is a shared resource library used by multiple skills in this repository.

## What lives here

| File | Purpose |
|---|---|
| `branding.md` | Brand voice, identity, and tone guide referenced by content-producing skills |
| `data-contracts.md` | Cross-skill data contracts: input/output schemas and ownership of pipeline phases |
| `identity.json` | Canonical agent identity (DRE#, brokerage, markets) — referenced by every skill that produces content |
| `integrations.md` | Per-skill integration map (which connectors and APIs each skill uses) |
| `publishing-via-composio.md` | The canonical pattern for publishing HTML/Markdown content via Composio (replaces the deprecated `html-email` and `github-skill-sync` skills) |
| `skill-deprecation-protocol.md` | The protocol for deprecating, absorbing, or replacing skills cleanly |

## How skills reference this folder

Skills reference files here via relative paths:

```
../shared-references/identity.json
../shared-references/branding.md
../shared-references/data-contracts.md
```

## Why this is not a skill

Skills have a `SKILL.md` (or `CLAUDE.md`) entry point and are invoked by name. This folder has no entry point and is not invoked directly — it is *read* by other skills as a reference library. Treat it like a shared `lib/` directory in a codebase.

## What does NOT belong here

- Skill logic or prompts (those go in the relevant skill folder)
- Agent-specific output files (those go in the agent workspace, not the repo)
- Temporary or generated files (those should be `.gitignore`d)

