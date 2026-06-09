---
name: obsidian-vault
description: "Orientation and navigation layer for Graeham Watts's Obsidian vault. Use this skill ANY time the user says 'the vault', 'my vault', 'Obsidian', 'my notes', 'my second brain', 'put this in Obsidian', 'check the vault', 'find in my notes', 'log to the vault', 'where did I save', or refers to daily notes, listings notes, client notes, the AI Library, Content Intelligence, Prop OS, or PropertyCast notes. This skill tells you WHERE the vault is, HOW it's organized, and WHICH folder a given note belongs in, so you never have to ask Graeham for the path again. The vault lives at C:\\Users\\Graeham Watts\\Documents\\Obsidian. For saving VIDEO references specifically, hand off to video-to-obsidian instead."
---

# Obsidian Vault — Navigation & Orientation

> **One job:** when Graeham says "the vault," you already know where it is, how it's laid out, and where a new note should go. No asking for the path. No guessing.

## Where the vault is

**Canonical path (Windows):**
```
C:\Users\Graeham Watts\Documents\Obsidian
```

**Sandbox/mounted path (if running in a Cowork sandbox):**
```
/sessions/.../mnt/Obsidian
```

Always resolve the Windows path first. If it doesn't exist, fall back to the mounted path. Never ask Graeham for the path — it is here.

## Folder map (top level)

| Folder | What lives here | Route a note here when… |
|---|---|---|
| `01 Team & Agents/` | Agent specs, team SOPs, role definitions | Note is about an agent, teammate, or internal process |
| `02 Daily Notes/` | Dated daily journal entries | A daily log, standup, or "today I…" note |
| `03 Listings/` | Per-property notes, listing prep, status | Anything tied to a specific property/address |
| `04 Clients/` | Per-client notes, buyer/seller profiles | Anything tied to a named client |
| `05 Marketing/` | Campaigns, content plans, brand assets | Marketing strategy, campaign notes, brand work |
| `AI Library/` | AiM / Pantana cross-reference, prompts, bots | AI-tooling reference material (see `ai-library` skill) |
| `Content Intelligence/` | Topic scoring, content calendar data, signals | Content-strategy data and research |
| `Instagram Saves/` | Video swipe file (logged by `video-to-obsidian`) | A saved video reference — **use `video-to-obsidian`** |
| `Prop OS/` | Property OS system docs and master brains | Prop OS / Property-OS system documentation |
| `PropertyCast/` | PropertyCast project notes | PropertyCast-specific work |
| `rules/` | Vault-wide rules, conventions, automation logic | A rule or convention the vault itself follows |
| `_Templates/` | Note templates | Don't write notes here — read templates from here |

> Folders are numbered `01`–`05` first (the active working areas), then named project/reference folders. When unsure, prefer the most specific existing folder over creating a new top-level one.

## How to write a note

1. **Resolve the vault path** (Windows first, sandbox fallback).
2. **Pick the folder** from the map above. If it's a property → `03 Listings/`; a client → `04 Clients/`; a daily log → `02 Daily Notes/`; etc.
3. **Check `_Templates/`** for a matching template before inventing structure.
4. **Filename:** `YYYY-MM-DD-slug.md` for dated notes, or `<Subject>.md` for evergreen notes. Match the naming already used in the target folder.
5. **Frontmatter:** always include at minimum:
   ```yaml
   ---
   created: YYYY-MM-DD
   tags: [relevant, tags]
   source: <url-or-origin-if-any>
   ---
   ```
6. **Write Markdown.** Use `[[wikilinks]]` to connect to existing notes where natural — that's the whole point of the vault.

## How to find something in the vault

- **Search by content:** use Grep over `C:\Users\Graeham Watts\Documents\Obsidian` (filter `--glob "*.md"`).
- **Search by filename:** use Glob like `**/*<keyword>*.md`.
- **Browse a folder:** list the relevant numbered/named folder from the map.
- Daily notes are dated; listings/clients are keyed by address/name.

## Handoffs

- **Saving a video** (Reel, YouTube, TikTok, etc.) → use **`video-to-obsidian`** (writes to `Instagram Saves/`). Don't reinvent it here.
- **AI Library lookups** (Pantana/AiM bots, prompts, guides) → use the **`ai-library`** skill; its source of truth is `Documents/Claude/AI-Library/`, mirrored in the vault's `AI Library/`.

## What this skill is NOT

It does not transcribe, scrape, or generate content. It is the **map**, not the engine. Its only job is to make sure you always know where the vault is and where things belong, so Graeham never has to paste the path again.
