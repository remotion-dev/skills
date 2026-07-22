# AI Library

Private reference for Graeham Watts and team. Captures everything from the AI marketing course library, member-submitted prompts, lectures, and lessons — plus a cross-reference to Graeham's personal Claude Skills toolkit.

## What's here

| File | What it is |
|---|---|
| `ai-library.html` | Single-page HTML reference. Sticky sidebar TOC, synonym-aware search (BOFU, AEO, schema, etc.), 72 library items, 20 community prompts, 12 lectures, 9 lessons, plus 43 Personal Claude Skills cards cross-referenced to library items. |
| `ai-library.pdf` | 362-page printable archive of the same content. |
| `implementation-plan.docx` / `.md` | Strategy doc — what's already covered by existing skills, what gaps to build (schema-builder, llm-listing-engine). |
| `sources/` | Raw scraped source data — JSON, markdowns, the strategic brief. Internal working files. |

## Why this is private

This repo is private and link-shared because it includes verbatim content from a paid course library and member-submitted prompts. Do not make this repo public. Do not enable GitHub Pages publicly.

## Editing flow

1. Edit `ai-library.html` directly.
2. Regenerate the PDF: see the weasyprint command in `implementation-plan.md`.
3. `git add . && git commit -m "..." && git push`.

The personal-skills toolkit lives in a separate repo (`Graehamwatts/skills`). When new skills land there, the corresponding card here should be updated by hand.
