---
name: video-to-obsidian
description: "Universal video-to-Obsidian logger for Graeham Watts. Takes ANY video URL — Instagram Reel, YouTube video, YouTube Short, TikTok, Vimeo, anything yt-dlp supports — transcribes it, auto-categorizes it, and writes a structured markdown note to the Obsidian vault at Documents/Obsidian/Instagram Saves/ with full frontmatter. The source URL is ALWAYS preserved as a required field — non-negotiable, because video is a visual medium and the user needs to click back to see the actual treatment (cuts, captions, on-screen text). Use this skill ANY time the user wants to save a video reference into their swipe-file vault, log a competitor's video for later study, archive an inspirational reel/short, add a video to their content library, build out their hook library, or 'put this in Obsidian.' Also called by instagram-competitor-scraper when scrape results need to be persisted, and by content-creation-engine when source videos identified during ideation should be archived. Triggers include: 'log this video to Obsidian', 'save this reel to my vault', 'add this YouTube short to Obsidian', 'put this in my swipe file', 'archive this reel', 'add to hook library', or just pasting a video URL with 'save it' / 'log it' context."
---

# Video to Obsidian

> **One job:** take a video URL, transcribe it, categorize it, and write a clean markdown note to the right folder in `Documents/Obsidian/Instagram Saves/`. Source URL always preserved.

## Why this exists

You're building a content intelligence layer. Words from videos need to live as searchable, queryable, AI-readable data in one place — Obsidian. But video is a visual medium, so the URL has to come along for the ride. Without the URL, the note is dead.

This skill is the **destination layer** for everything visual you save. Manual ad-hoc saves, scraper output, even YouTube videos you watch for research — all flow through here and land in the same schema.

## What it accepts

Any URL supported by `yt-dlp` (1,800+ platforms). Most common: Instagram Reels/posts, YouTube videos/Shorts, TikTok, Vimeo, Twitter/X video, Facebook video, LinkedIn video, direct video file URLs.

## How to invoke

```
log this to Obsidian: https://www.instagram.com/reels/DYSUqcsuGX9/
save this short to my vault: https://youtube.com/shorts/abc123
add to hook library: https://tiktok.com/@user/video/789
```

CLI form:

```bash
python3 scripts/log_to_vault.py "https://www.instagram.com/reels/ABC/"
python3 scripts/log_to_vault.py "URL" --folder "Hook Library" --my-use steal-hook
python3 scripts/log_to_vault.py "URL" --metadata-json '{"engagement":{"views":12000}}'
python3 scripts/log_to_vault.py "URL" --transcript-text "already have it"  # skip transcription
```

## What it does

1. **Validates URL** — must be present
2. **Calls `video-transcriber`** (or uses pre-supplied --transcript-text)
3. **Pulls metadata** via yt-dlp (title, duration, creator, post date)
4. **Merges extra metadata** from --metadata-json (engagement stats from scraper)
5. **Auto-categorizes** into right folder via heuristics
6. **Auto-tags** content_type + hook_pattern + topic_tags
7. **Writes the note** to `Obsidian/Instagram Saves/<folder>/<date>-<slug>.md`

## Vault path

Auto-detected from `C:\Users\Graeham Watts\Documents\Obsidian\Instagram Saves\` or `/sessions/.../mnt/Obsidian/Instagram Saves/` (sandbox). Override with `--vault-root`.

## Folder routing

| Folder | Trigger |
|---|---|
| `AI & Tech Tutorials/` | AI/Claude/MCP/automation keywords in transcript or caption |
| `Real Estate Content/` | Real estate / Bay Area / Peninsula keywords |
| `How-To Videos/` | 'how to' / 'step 1' / 'tutorial' in opening |
| `Hook Library/` | --my-use steal-hook OR --folder Hook Library |
| `Examples to Clone/` | --my-use full-clone |
| `Style References/` | --my-use style-ref |
| `_Inbox/` | Default fallback |

Categorization is a starting guess. Review weekly, move if needed.

## Frontmatter schema

Every note: url (required), source, creator, creator_followers, post_type, post_date, saved_date, duration_sec, content_type[], hook_pattern[], topic_tags[], my_use[], saved_for[], engagement{views,likes,comments,saves,engagement_rate}, status, transcript_available, discovered_via.

## Auto-tagging

**content_type:** how-to (keyword match), ai-workflow, talking-head (short + first-person), walkthrough (sequence words), comparison (vs/versus), list (top N pattern).

**hook_pattern:** pattern-interrupt (negation at start), contrarian ('most people'/'the truth'), curiosity-gap ('the secret'/'nobody talks'), question-hook (ends with ?), direct-promise ('here's how').

**topic_tags:** extracted from caption hashtags + transcript keyword map.

## Idempotency

If URL exists in vault, default = skip with stderr message. `--update` updates engagement only. `--force` overwrites.

## Integration

- `instagram-competitor-scraper` pipes results via `--metadata-json`
- `content-creation-engine` archives source videos identified during ideation
- `cinematic-hooks` reads the Hook Library folder this populates

## Why URL preservation is non-negotiable

Video is a visual medium. Transcripts lose cuts, on-screen text, visual style, energy, sound design. Without the URL, the note is a partial copy. With the URL, the note is a queryable launchpad back to the original. This is the one thing the skill must never get wrong.
