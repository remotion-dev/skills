# Auto-Render Hand-off (v6.2 — Apr 2026) & Freshness Register (Rule 15)

Referenced from SKILL.md. Load this file at the point a script is finalized and ready to hand off to rendering, or when debugging the ideation engine's duplicate-topic detection.

## Auto-Render Hand-off

Once a V6 script is finalized, it no longer needs to be manually copy-pasted into ElevenLabs and HeyGen. The `heygen-elevenlabs-renderer` skill owns the full render pipeline and this skill hands off to it.

### What this skill produces for the renderer

For every core asset script written, write out a companion SSML file next to the content package:

```
outputs/content-package-{timestamp}.md         (the full package — scripts, captions, etc.)
outputs/content-package-{timestamp}.ssml.txt   (just the <speak>…</speak> block, nothing else)
```

The `.ssml.txt` file is the raw input the renderer reads. It must contain only the SSML — no headers, no comments, no markdown fences, no "SCRIPT:" prefix. One file = one render.

### Known SSML quirks (read before hand-off)

ElevenLabs `eleven_multilingual_v2` does NOT fully honor `<prosody>`. Only `<break time="Xs"/>` produces audible effect. `<prosody rate="slow">` tags are accepted by the API but silently dropped — the inner text is still read, just at the default speed. So:

- KEEP `<prosody>` tags for human readability in the package file (they document intent)
- ALSO provide the `.ssml.txt` with the same tags (the renderer strips ineffective ones at TTS time)
- When you genuinely need rate/pitch change (e.g., whispered BOFU asides), use **ElevenLabs bracket audio tags** inside the text: `[whispers]`, `[excited]`, `[sarcastic]`, `[laughs]`. See the renderer skill's `references/elevenlabs-audio-tags.md`.

### Hand-off invocation (one command)

After this skill writes the package, the renderer takes over:

```bash
python3 skills/heygen-elevenlabs-renderer/scripts/full_render.py \
  --script outputs/content-package-{timestamp}.ssml.txt \
  --slug "{content-slug}" \
  --resolution 1080p \
  --aspect 9:16
```

The renderer: (1) synthesizes MP3 via ElevenLabs using Graeham's voice clone `Pa3vOYQHHpLJn1Tf7hnP`, (2) uploads MP3 to HeyGen, (3) creates an avatar video against Graeham's avatar `9a3600b16f604059b6ab8b9a55e29ea9`, (4) polls until complete, (5) downloads MP4 to `outputs/renders/{slug}.mp4` with a sibling `{slug}.meta.json` holding `video_id`, `video_url`, and duration.

### Dashboard locations (where rendered media lives)

After a render completes, the same files are available in four places. The renderer (`poll_and_download.py`) writes a `dashboards` block into `{slug}.meta.json` recording each location.

## Rule 15: Two-Register Freshness Check

**Why this exists:** Prior to April 24 2026, the ideation engine only checked `topic-history.json`'s `history` array (posted topics). Topics that had been SHOT but not yet POSTED were invisible to the gatekeeper, which meant the engine could queue a near-duplicate of a video sitting in Graeham's edit pipeline.

**The fix:** `topic-history.json` now has TWO registers — `history` (posted) and `in_production` (shot-but-not-posted). Every freshness check must read BOTH.

**Implementation in ideation-engine:**

1. Load `topic-history.json`.
2. Build `excluded_slugs = {t['slug'] for w in history for t in w['topics']} | {t['slug'] for t in in_production}`.
3. For each candidate topic, also check `exclusion_radius` text on every `in_production` entry — if the candidate touches the same market + angle, exclude even when the slug differs.
4. When a topic ships, MOVE it from `in_production` (if present) into `history`. Don't leave duplicates.

**When to write to `in_production`:** Whenever Graeham confirms he has shot or is currently editing a video for a topic that isn't yet posted. Add via the `script-writer` phase or manually before ideation runs.

Reference: `skills/content-creation-engine/references/topic-history.json` schema v2.0.
