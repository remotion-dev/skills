# Transcript Repurposer

The fast-lane sibling of `video-script-creation-engine`. Takes a transcript Graeham already has (SurfFast download, paste, .srt, .vtt) and produces a Graeham-voiced, data-backed, humanized content package across all platforms — YouTube Long, Short, IG Reel, TikTok, Carousel, Blog, GMB, Facebook — plus HeyGen and Higgsfield production handoff blocks.

## Why this skill exists

SurfFast downloads + auto-transcribes videos. Great for capturing source material. But the resulting transcripts have no data backbone — no Bay Area market stats, no AB 1482 references, no verified facts. Repurposing directly from SurfFast output produced karaoke versions of someone else's video, missing the depth that makes Graeham's Content Engine scripts feel authoritative.

This skill fixes that. Same script-quality pipeline as the Content Engine, but transcript-first instead of ideation-first.

## Pipeline

| Phase | What it does | Reference |
|---|---|---|
| 1 | Ingest the transcript (any format) | `references/01-ingest.md` |
| 2 | Analyze the source — 7-field source brief | `references/02-analyze.md` |
| 3 | Decide the repurpose angle (5 angles, optional hybrid) | `references/03-angle.md` |
| 4 | Inject research and data (this is the "fix" — what SurfFast doesn't give us) | `references/04-research.md` |
| 5 | Generate 3 hook variants from 3 frameworks, scored | `references/hook-frameworks.md` |
| 6 | Multi-platform script writing with inline shot direction tags | `references/06-script-writing.md` |
| 7 | HeyGen + Higgsfield + ElevenLabs production handoff | `references/07-handoff.md` |
| 8 | Humanizer auto-pass (required, not optional) | `references/08-humanizer.md` |

## When this fires vs. video-script-creation-engine

**This skill** = the user already has the transcript. SurfFast download, manual paste, .srt file, anything text.

**Content Engine** = the user has a topic or wants ideas; no source video. The Content Engine generates from audience research.

## Integration with other skills

- **Pulls from:** `video-script-creation-engine` (voice and style refs, market config, GHL keyword set)
- **Auto-invokes:** `humanizer` (final pass on the content package)
- **Hands off to:** `heygen-video` (avatar render), `higgsfield-video` (B-roll generation), `vaibhav-template` (if Graeham wants the Vaibhav aesthetic on top)

## Output

Single content-package markdown file saved to `outputs/transcript-repurpose-{slug}-{YYYYMMDD-HHMM}.md`.

## Quickstart

User pastes a transcript or uploads a transcript file → say "repurpose this for me" → the skill runs all 8 phases and delivers the package.

User can also request only specific derivatives: "just give me the IG Reel" or "I only need the YouTube Short and the caption." The skill scales down accordingly.
