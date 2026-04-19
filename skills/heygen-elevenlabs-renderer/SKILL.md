---
name: heygen-elevenlabs-renderer
description: End-to-end avatar video rendering pipeline for Graeham Watts. Synthesizes Graeham's cloned voice on ElevenLabs from an SSML script (including <prosody> and <break> tags from V6 format), uploads the MP3 to HeyGen, renders an avatar video against Graeham's personal avatar via the v3 Create Avatar Video endpoint, and returns a playable MP4. Use ANY time the user says "render this script", "make a video from this script", "auto-render", "full auto", "push this to HeyGen", "avatar video", "voice clone video", or clicks the "Full Auto-Render" button on the V6 Production Calendar. Also trigger when the content-creation-engine has produced a V6 script and the user wants the video built without manual steps.
---

# HeyGen + ElevenLabs Renderer

## Purpose
Turn a finished V6 script into a delivered MP4 video with zero manual work. This skill owns the rendering layer of the content pipeline. Everything before this point is ideation and writing (content-calendar → content-creation-engine). Everything this skill does is mechanical execution.

## Pipeline at a glance
```
V6 SSML script
    │
    ▼
ElevenLabs TTS (Graeham's voice clone)        ─── scripts/synthesize_voice.py
    │                                              eleven_multilingual_v2
    ▼                                              Supports <break time="Xs"/>
audio.mp3 (44.1 kHz, 128 kbps mono)                Accepts <prosody> (silent pass-through)
    │
    ▼
HeyGen asset upload                            ─── scripts/upload_asset.py
    │                                              Uses CLI: `heygen asset create --file`
    ▼
asset_id
    │
    ▼
HeyGen v3 /videos create (avatar + audio)     ─── scripts/render_video.py
    │                                              voice mode = audio_asset_id
    ▼
video_id (status: waiting → processing)
    │
    ▼
Poll /v1/video_status.get every 15s            ─── scripts/poll_and_download.py
    │
    ▼
video_url (signed HeyGen CDN URL)
    │
    ▼
Download MP4 → outputs/renders/<slug>.mp4
```

## Credentials
Store keys at `/sessions/<session>/mnt/outputs/.claude-credentials/` with `chmod 600`:
- `heygen-key.txt` (used via `HEYGEN_API_KEY` env var or CLI config)
- `elevenlabs-key.txt` (used via `xi-api-key` header)

If keys are missing at session start, STOP and ask the user to paste them. Never proceed with a placeholder.

## Defaults (from registry.json)
These are the canonical production defaults. Never hardcode — always read `registry.json`:
| Field | Value |
|---|---|
| HeyGen avatar | Graeham Watts — `9a3600b16f604059b6ab8b9a55e29ea9` |
| ElevenLabs voice | Graeham Watts Voice Clone — `Pa3vOYQHHpLJn1Tf7hnP` |
| ElevenLabs model | `eleven_multilingual_v2` |
| Aspect | `9:16` (vertical for Reels/Shorts/TikTok) |
| Resolution | `720p` (bump to `1080p` for listing videos) |

The user has 70 personal "Graeham Watts" avatar looks. The renderer always uses the primary unless the script specifies an alternate look ID.

## Registry refresh
Re-run `scripts/refresh_registry.py` when:
- A new avatar look is trained in HeyGen
- A new voice is added/cloned in ElevenLabs
- The user reports "avatar not found"

## SSML compatibility notes (IMPORTANT)
ElevenLabs has **partial** SSML support — verified on `eleven_multilingual_v2`:

| Tag | Supported | Behavior |
|---|---|---|
| `<break time="0.4s"/>` | YES | Literal silence of the specified duration |
| `<speak>...</speak>` | YES (wrapper) | Required root for SSML mode |
| `<prosody rate="slow">...</prosody>` | Silent pass-through | API accepts it but the rate/pitch attrs are NOT honored — the text inside is still synthesized, just without the prosody effect |
| `<emphasis>`, `<say-as>`, `<phoneme>` | NOT supported | Tag is stripped; inner text is read normally |

**What this means for V6 scripts:** `<break>` tags give you deterministic pause timing (critical for pattern interrupts). `<prosody>` tags are safe to keep in the script for human readability but don't rely on them for actual delivery changes. If you need slower/faster delivery, use ElevenLabs' `voice_settings.stability` and `style` parameters instead, or preprocess the text into multiple TTS calls with different settings and concatenate.

For audio-tag-based delivery (laughs, sighs, etc.), use ElevenLabs' bracket syntax like `[laughs]`, `[whispers]` — NOT SSML. See `references/elevenlabs-audio-tags.md`.

## Primary invocation
```bash
python3 scripts/full_render.py \
    --script /path/to/script.ssml.txt \
    --slug "ab1482-explainer-week3" \
    --resolution 720p \
    --aspect 9:16
```

This wraps all four pipeline stages. Output file lands at `outputs/renders/<slug>.mp4` with a sibling `<slug>.meta.json` containing `video_id`, `audio_asset_id`, `duration`, `completed_at`, and a full `dashboards` block (HeyGen video page, HeyGen projects list, ElevenLabs history, ElevenLabs voice library). The poller also emits a single-line `RENDER_RESULT={...}` to stdout so webhook consumers and the V6 calendar button can surface those links without scraping log output.

### Where renders + voices live

| Asset | Dashboard URL |
|---|---|
| Finished video (this render) | `https://app.heygen.com/videos/<video_id>` |
| All past videos | `https://app.heygen.com/projects` |
| TTS generation history | `https://elevenlabs.io/app/speech-synthesis/history` |
| Graeham voice clone | `https://elevenlabs.io/app/voice-library` |
| Local MP4 | `outputs/renders/<slug>.mp4` |
| Local metadata | `outputs/renders/<slug>.meta.json` |

The V6 Production Calendar button reads the `dashboards` object returned by `webhook_handler.py /status/<job_id>` and renders it as a row of click-through links next to the render status. The banner at the top of the Production Map tab also pings `/health` and always shows the HeyGen + ElevenLabs dashboard links — online or offline — so Graeham can always find the content.

## Per-stage invocation (for debugging)
- `scripts/synthesize_voice.py --text-file script.txt --out audio.mp3`
- `scripts/upload_asset.py audio.mp3` → prints `asset_id`
- `scripts/render_video.py --audio-asset-id <id> --title "..."` → prints `video_id`
- `scripts/poll_and_download.py --video-id <id> --out outputs/renders/slug.mp4`

## Error handling
- **401 from HeyGen:** key is invalid or expired → re-read `heygen-key.txt`
- **402 from HeyGen:** subscription credit exhausted → tell user plainly, don't retry
- **422 "voice is premade":** cannot use a premade voice with voice cloning settings — downgrade `voice_settings.style` to 0.0
- **HeyGen video status "failed":** fetch `error.message`, common causes: audio file too long (>10 min), avatar not trained for aspect ratio, audio file corrupt
- **Timeout after 10 min polling:** video is likely stuck — submit again with `test: false` and `dimension` set to a smaller size (480x854)

## Files in this skill
- `SKILL.md` — this file
- `scripts/full_render.py` — one-shot orchestrator
- `scripts/synthesize_voice.py` — ElevenLabs TTS
- `scripts/upload_asset.py` — HeyGen asset upload (CLI wrapper)
- `scripts/render_video.py` — HeyGen v3 video create
- `scripts/poll_and_download.py` — status polling + MP4 download
- `scripts/refresh_registry.py` — rebuild registry.json from live HeyGen + ElevenLabs data
- `references/registry.json` — avatar/voice IDs and defaults
- `references/webhook_handler.py` — local Flask handler for Auto-Render button
- `references/elevenlabs-audio-tags.md` — bracket-syntax reference

## Hand-off contract
- **Upstream:** `content-creation-engine` writes a V6 script to `outputs/scripts/<slug>.ssml.txt`
- **Downstream:** the V6 Production Calendar Auto-Render button POSTs `{"slug": "..."}` to the local webhook → this skill runs `full_render.py` → MP4 lands in `outputs/renders/`

## Cost guardrails
- ElevenLabs Creator tier = ~100k chars/month. A 60-second vertical = ~900 chars. Budget roughly 100 renders/mo before hitting the cap.
- HeyGen credits are per-video-minute. Test renders should use `resolution: "720p"` to conserve credits; only bump to 1080p for final deliverables.

## Verification step (required after every render)
1. Download the MP4 and confirm `file output.mp4` reports a valid MPEG-4 container
2. Probe duration with `ffprobe` — should be within ±0.5s of the MP3 source
3. Open the signed URL in a browser and scrub to verify lip sync (eyeball test)

If any verification step fails, mark the render failed and re-queue rather than shipping a broken file.

## Sandbox allowlist gap (important)
Finished HeyGen MP4s are served from `files2.heygen.ai` on a signed CloudFront URL. This CDN host is NOT currently on the Cowork sandbox allowlist. In-sandbox downloads via `poll_and_download.py` will fail with proxy HTTP 403. Two fixes:
1. Add `files2.heygen.ai` and `resource2.heygen.ai` to the Cowork desktop allowlist (recommended).
2. Otherwise, run `webhook_handler.py` on the host Windows machine (outside the sandbox) — its network is unrestricted and downloads work.

Verified test render that succeeded: video_id `f79ed46032f74759a1153ff7e06e33f6`, duration 7.77s, SSML source with `<break>` tags honored.
