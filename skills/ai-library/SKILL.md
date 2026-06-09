---
name: ai-library
description: "Personal AI Library — Graeham's private cross-reference combining Pantana's AI Marketing Academy library (72 items: 22 bots, 29 prompts, 20 guides, 1 video), 20 community prompts from Prompt Studio, 12 lectures, 9 lessons, 45 Personal Claude Skills with diagrams, and 2 Personal Custom Prompts. 398-page PDF + interactive HTML with 49 inline SVG diagrams. PRIVATE — do not share publicly. Use ANY time the user asks about AiM, AI Marketing Academy, Pantana, Jason Pantana, the library, BOFU library, AEO library, what does AiM say about a topic, find a prompt for a task, which of my skills cover a topic, cross-reference my skills with AiM, what skills do I have for a topic, what's in the AI library, or look up a Pantana bot or prompt. Also trigger when user mentions implementation plan, gaps to build, schema-builder gap, or llm-listing-engine gap. Source of truth at C:\\Users\\Graeham Watts\\Documents\\Claude\\AI-Library\\."
---

# AI Library — Personal Reference + Cross-Index

This skill knows where Graeham's AI Library lives and how to look things up in it. The library itself is a single-page HTML reference plus a 398-page PDF — the canonical home is `C:\Users\Graeham Watts\Documents\Claude\AI-Library\`, mirrored to the private repo `github.com/Graehamwatts/ai-library`.

## What's in the library

| Section | Count | What |
|---|---|---|
| Bots | 22 | Pantana's Custom GPTs, Gems, and Cowork Agents |
| Prompts | 29 | Pantana's curated prompt library |
| Guides | 20 | Pantana's how-to articles |
| Videos | 1 | Pantana's video tutorials |
| Community Prompts | 20 | Member-submitted prompts from Prompt Studio |
| Personal Claude Skills | 45 | Graeham's own skills with cross-references to AiM items |
| Personal Custom Prompts | 2 | Language Tutor + Blader Humanizer |
| **Total items** | **139** | All searchable, all diagrammed where useful |

Plus 49 inline SVG diagrams (BOFU funnel, AEO citation flow, skill ecosystem map, plus per-skill workflow diagrams).

## Where to find things

| Source file | Location | What's in it |
|---|---|---|
| `ai-library.html` | `Documents/Claude/AI-Library/ai-library.html` | The interactive view — sidebar TOC, search bar, all diagrams. **This is what to open in browser.** |
| `ai-library.pdf` | `Documents/Claude/AI-Library/ai-library.pdf` | 398-page printable archive. Same content, paginated. |
| `implementation-plan.md` | `Documents/Claude/AI-Library/implementation-plan.md` | Strategy doc — what's covered by existing skills, what gaps to build. |
| `sources/source_72items.md` | `Documents/Claude/AI-Library/sources/` | Raw scraped content of all 72 AiM library items. **Search this for full-text lookups.** |
| `sources/prompt_studio.md` | `Documents/Claude/AI-Library/sources/` | All 20 community prompts in raw form. |
| `sources/archive_data.json` | `Documents/Claude/AI-Library/sources/` | Structured JSON of library + prompts + synonyms. **Use for programmatic lookup.** |
| `sources/summaries.json` | `Documents/Claude/AI-Library/sources/` | One-line summaries of each library item. **Use for quick scans.** |

## How to use this skill

### When the user asks "what does AiM say about [topic]"

1. Grep the source markdown for the topic: `grep -l -i "topic" Documents/Claude/AI-Library/sources/source_72items.md`
2. Or load the structured JSON: `Documents/Claude/AI-Library/sources/archive_data.json` and scan the `library` array for matching titles + bodies
3. Quote the relevant passage with the source URL (every item has a `url` field linking back to aimarketingacademy.com)

### When the user asks "which of my skills covers [topic]"

1. Grep the HTML for `data-search="...topic..."` patterns — every personal-skill card has a `data-search` attribute with all relevant trigger words
2. Or scan `sources/archive_data.json` and look for cross-references in the cards
3. Return the skill name + the `Documents/Claude/Skills/skills/<name>/SKILL.md` path

### When the user asks "show me the AI library"

1. Open `Documents/Claude/AI-Library/ai-library.html` in their default browser using the `start` command (Windows) or `open` (Mac):
   ```
   start "" "C:\Users\Graeham Watts\Documents\Claude\AI-Library\ai-library.html"
   ```
2. Or hand them the `computer://` link for in-Cowork preview

### When the user asks "find a prompt for [task]"

1. Search `sources/prompt_studio.md` for the task keyword
2. Search `sources/source_72items.md` for AiM library prompts on that topic
3. Cross-reference against the user's installed personal skills (some may already do the job — don't reinvent)

### When the user asks "what gaps are left to build"

1. Open `Documents/Claude/AI-Library/implementation-plan.md`
2. The two identified gaps are: **Schema Builder** (~3-4 hrs) and **LLM Listing Engine** (~8-10 hrs)
3. Both have full design diagrams in the HTML at `#ps-gaps`

## Privacy hard rule

**This library is PRIVATE.** It contains:
- Pantana's paid course content (verbatim) — would violate his TOS to share publicly
- 20 member-submitted prompts from Prompt Studio (named members)
- Graeham's complete skill toolkit (proprietary)

NEVER:
- Push the AI Library files to a public repo
- Paste library content into a public ChatGPT / claude.ai conversation that another user could see
- Forward the PDF to anyone outside Graeham's team without explicit permission

ALWAYS:
- Reference items by source URL when possible (links back to aimarketingacademy.com — that's the original public source)
- Treat the AI Library as a private working knowledge base

## Brand identity

Per `shared-references/identity.json` — every output that mentions Graeham must use DRE# **01466876** (Intero Real Estate). The blocklisted DRE that has leaked historically is in `_blocked_values` of identity.json — never write it. The AI Library content has been audited and contains zero hits for the blocklisted value.

## Repos this skill is part of

- **Local source:** `C:\Users\Graeham Watts\Documents\Claude\AI-Library\` (working copy)
- **GitHub mirror:** `github.com/Graehamwatts/ai-library` (private, link-shared with team only)
- **This skill:** `Documents/Claude/Skills/skills/ai-library/SKILL.md` (registers the library as discoverable)
- **Skills repo:** `github.com/Graehamwatts/skills` (where this SKILL.md is pushed)

## Related skills

- `shared-references` — brand identity source of truth (read at runtime, never typed from prior context)
- `content-creation-engine` — covered as Personal Skill #1 in the library, includes BOFU pipeline + funnel diagram
- All 45 personal skills cross-referenced to AiM library items in the HTML

## Curated by

Graeham Watts, 2026-05-14. Library captured from aimarketingacademy.com by the previous chat session and integrated into this discoverable skill on 2026-05-15.
