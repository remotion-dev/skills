---
name: heygen-video
description: Generate HeyGen avatar videos of Graeham Watts using his trained digital twin and photo-avatar looks. Use ANY time the user mentions HeyGen video, avatar video, AI avatar, talking head video, video of me, video of Graeham, listing intro video, market update video, personalized video message, buyer Q&A video, seller update video, "make me a video", "render a HeyGen video", "create an avatar video", or turning a script into a finished video with Graeham's face and voice. Also trigger on follow-ups like "check on that HeyGen video", "is the video ready", "download the avatar video", or when resuming a previously submitted HeyGen job via video_id. This skill is the CORRECT CHOICE for any HeyGen output — do not use video-creator (slideshow) or remotion-video (React) for HeyGen avatar work. Pair with content-creation-engine when the user has a topic but no script yet.
---

# HeyGen Video — Graeham Watts

Generate HeyGen avatar videos using Graeham's trained looks. v1 of this skill is a single-brand (Graeham only) workflow — PropOS brand avatars are not trained yet and can be added to `references/avatars.md` when they are.

## When this skill fires

- "Make a HeyGen video of me saying X"
- "Render a listing intro video with Graeham's avatar"
- "Turn this script into a HeyGen avatar video"
- "Create a market update video"
- "Generate an avatar video: <script>"
- "Check on HeyGen video <video_id>" (status check / download path)

If the user has a TOPIC but no SCRIPT yet, chain with `content-creation-engine` first — that skill writes the script, then hand the script back here.

## The reality you must communicate to the user

**HeyGen video jobs take 2–10 minutes for short scripts, up to 20+ minutes for longer or complex ones.** The skill submits the job and returns immediately with a `video_id` and dashboard link. The user watches progress in HeyGen's dashboard OR asks Claude to "check on video <video_id>" later (this session or a future one).

**Do NOT use `--wait`.** Claude.ai sessions can time out before the render completes. Submit-and-return is the right pattern.

## Prerequisites

Before running any script, confirm:

1. `HEYGEN_API_KEY` is set in the environment. If not, tell the user to paste it (they can grab from https://app.heygen.com/api). Warn them chat-pasted keys should be rotated after the session.
2. The HeyGen CLI is installed. Run `scripts/setup.sh` — it installs the CLI to `~/.local/bin/heygen` if missing, and verifies auth.

## Workflow

## MANDATORY BEHAVIOR — READ BEFORE EVERY VIDEO

**Before calling `create.py`, Claude MUST ask Graeham which avatar to use.** There is no default avatar in v1. Graeham wants to confirm the avatar on every single video. Accept either:

- a raw avatar look ID (32-char hex, e.g. `159cd7b883724fdb9a51b97dec94df89`), passed to `create.py` via `--avatar-id`
- one of the named looks from `references/avatars.md`, passed via `--look`

The script will refuse to run without one of these — this is enforced, not advisory. Do NOT silently pick `digital_twin` or any other default. **Ask.**

**Voice is different.** Voice Clone (`717249201f7745988219b9aeb9041b42`) is the default for every video, automatically. Only ask about voice if Graeham says he wants to override it (e.g., "use the twin voice").

## Workflow

### A. Submit a video (the common case)

```bash
python3 scripts/create.py \
  --script "Your script text here" \
  (--avatar-id <look_id> | --look <named_look>) \
  [--voice <voice_id>] \
  [--aspect 9:16|16:9] \
  [--title "Optional dashboard title"]
```

**How to ask the user:** "Which avatar should I use? You can paste the look ID from HeyGen, or name one of the known looks (digital_twin, casual_chic, freshly_ironed, fashion_flip, bespectacled, suburban_serenity)." Wait for their answer. Then call the script with what they gave you.

**Voice defaults (automatic, no need to ask):**
- `--voice 717249201f7745988219b9aeb9041b42` — "Graeham Watts Voice Clone" — locked in as the default for all videos.
- Only override if Graeham explicitly requests it.

**Aspect default:** `9:16` for portrait, `16:9` when `--look suburban_serenity` (its native orientation). When `--avatar-id` is used, defaults to `9:16` — Claude should ask the user if the aspect needs adjustment for non-standard looks.

**Returns:** `video_id`, dashboard URL, and a log file at `/tmp/heygen_jobs/<video_id>.json`.

**Known Graeham looks (for reference — but still ASK before using):**

| Look | Best for | Orientation |
|---|---|---|
| `digital_twin` | Personal real estate content where authenticity matters (listing intros, market updates, buyer Q&A, anything where it must actually be you) | portrait |
| `casual_chic` | Approachable everyday content, buyer onboarding | portrait |
| `freshly_ironed` | Polished seller-focused content, CMA presentations | portrait |
| `fashion_flip` | Higher-energy content, stylistic content variety | portrait |
| `bespectacled` | PropOS / tech-adjacent content placeholder until a real PropOS avatar exists | portrait |
| `suburban_serenity` | Horizontal content, neighborhood features | **landscape** — use with `--aspect 16:9` |

**Important:** With the global default voice, all 6 looks now sound like Graeham. Face quality is the remaining variable: `digital_twin` is authentically you from real video; the photo_avatars are AI-generated variations. For face-critical customer content, prefer `digital_twin`.

### B. Check on a previously submitted video

```bash
python3 scripts/status.py --video-id <video_id>
```

This queries HeyGen for the video's current state. If complete, it downloads the MP4 to `/home/claude/heygen_outputs/<video_id>.mp4` and prints the path. If still processing, it reports the state and how long it's been running.

### C. Full example invocation

User says: *"Make me a quick HeyGen test video saying hi and confirming the pipeline works"*

```bash
# 1. Ensure CLI + auth
bash scripts/setup.sh

# 2. Submit
python3 scripts/create.py \
  --script "Hi, I'm Graeham Watts with Intero Real Estate. This is a test of my new HeyGen video pipeline." \
  --title "Pipeline test - $(date +%Y-%m-%d)"

# 3. Report the video_id and dashboard URL back to the user
# 4. Tell user: "I'll check back in a few minutes, or say 'check on video <id>' later"
```

## Error handling

| Error | Meaning | Fix |
|---|---|---|
| `HEYGEN_API_KEY not set` | Env var missing | User must paste the key and export it |
| `Avatar not found` | Look ID invalid or user's API key doesn't have access | Check `references/avatars.md` and re-run `heygen avatar looks get <id>` to verify |
| `Insufficient credits` | HeyGen plan out of video credits | User must top up at app.heygen.com |
| `Rate limited` | Hit HeyGen's concurrent job limit | Wait, retry in 5 min |
| `posthog 403 Host not in allowlist` (warning) | CLI's telemetry endpoint blocked in sandbox | Benign — ignore, does not affect video generation |

## What v1 intentionally does NOT do

- ⚠️ **Captions discovery update:** HeyGen DOES generate a captioned variant automatically — it's exposed through `heygen video download <id> --asset captioned` (not `video create`). The skill now supports this via `status.py --captioned` or `--only-captioned`. **Caveat:** HeyGen's default caption style may not match your brand look; style customization requires the web UI or ffmpeg post-processing. Test this and decide if the stock caption style is usable before relying on it.
- ❌ No automatic Box upload of finished MP4 (can be added — user's Box MCP is connected)
- ❌ No chaining to `content-creation-engine` (skill documents the chain; user triggers it)
- ❌ No PropOS brand defaults (no avatar trained yet)
- ❌ No batch generation / multi-scene videos (use HeyGen web UI for those)
- ❌ No webhook-based completion notification (could be added with N8N; schema exposes `callback_url`)

Each of these is a sensible v2 target once v1 is proven.

## References

- `references/avatars.md` — the 6 Graeham look IDs, voices, orientations, when-to-use
- HeyGen API docs: https://developers.heygen.com/docs/quick-start
- HeyGen CLI docs: https://developers.heygen.com/cli
- v3 video create endpoint schema: `heygen video create --request-schema`
