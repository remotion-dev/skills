# Setup the Local Transcription CLI

**Why this exists:** The Cowork bash sandbox can't reach YouTube, Instagram, TikTok, or Deepgram (it's allowlisted to only github.com and pypi.org). So transcription has to run on your actual Windows machine, NOT inside Cowork. This CLI does that, then drops the transcript into a folder Cowork can read.

## One-time setup (~5 minutes)

### 1. Install Python (if you don't have it)

Download from [python.org/downloads](https://www.python.org/downloads/) — version 3.10 or newer. During install, **check "Add Python to PATH"** at the bottom of the installer screen.

Verify in a new Command Prompt:
```
python --version
```

### 2. Install the required Python packages

Open Command Prompt and run:
```
pip install yt-dlp httpx
```

### 3. Install ffmpeg (needed by yt-dlp to extract audio)

Easiest path:
- Download from [gyan.dev/ffmpeg/builds](https://www.gyan.dev/ffmpeg/builds/) — get "ffmpeg-release-essentials.zip"
- Unzip to `C:\ffmpeg\`
- Add `C:\ffmpeg\bin\` to your Windows PATH (Settings → System → About → Advanced → Environment Variables)

Verify:
```
ffmpeg -version
```

### 4. Place the Deepgram key

The key already lives at:
```
C:\Users\Graeham Watts\Documents\Claude\Skills\deepgram-key.txt
```

The local CLI reads from there automatically. No further setup needed for Graeham.

For Jason and Ellie: they each save a copy of the key (Graeham shares it) to the same path on their machine.

### 5. Place the transcribe scripts

The CLI files live in your local skills folder:
```
C:\Users\Graeham Watts\Documents\Claude\Skills\skills\transcript-repurposer\scripts\
├── transcribe_local.py    ← the Python script
├── transcribe.bat         ← the Windows wrapper (call this)
└── SETUP_LOCAL_CLI.md     ← this doc
```

For convenience, you can either:
- Add the `scripts\` folder to your Windows PATH (so you can run `transcribe` from anywhere)
- Or just copy `transcribe.bat` and `transcribe_local.py` together to your Desktop and run from there

## Daily use

In Command Prompt:

```
transcribe https://www.youtube.com/watch?v=abc123
```

You'll see progress:
```
→ Source: https://www.youtube.com/watch?v=abc123
→ Tier: premium (Deepgram Nova-3)
→ Output inbox: C:\Users\Graeham Watts\Documents\Claude\Skills\_inbox
→ Platform: youtube
→ Fetching metadata...
  Title: Bay Area mortgage rates 2026
  Duration: 4m32s
→ Downloading audio...
  Done in 8.1s — 4823 KB
→ Transcribing via Deepgram Nova-3...
  Done in 14.7s

✓ Transcript ready (612 words)
  Text:     C:\...\_inbox\transcript-bay-area-mortgage-rates-2026-20260516-1430.txt
  Manifest: C:\...\_inbox\transcript-bay-area-mortgage-rates-2026-20260516-1430.json

Next: In Cowork, say 'Repurpose the latest from my inbox' and the skill takes over.
```

Then in Cowork:

```
Repurpose the latest from my inbox
```

The skill picks up the newest transcript file from `Documents\Claude\Skills\_inbox\`, runs Phases 1-9, delivers the artifact bundle.

## Local audio files

If you've already downloaded audio (via SurfFast or anything else), feed it directly:

```
transcribe C:\Videos\client-interview.mp3
```

Same output path — Cowork reads it the same way.

## Costs

| Source length | Deepgram cost |
|---|---|
| 30-sec reel | ~$0.002 |
| 5-min YouTube short | ~$0.02 |
| 30-min podcast | ~$0.13 |
| 90-min interview | ~$0.39 |

Your $200 Deepgram trial credit covers ~45,000 minutes. At realistic team usage (~50 videos/month), that's 6-12 months before you need to top up.

## What if it fails?

**"yt-dlp couldn't download" / "Private video":** The source is locked or geo-blocked. Try:
- Confirm the post is public
- Use SurfFast to download the audio manually, then run `transcribe <audio file>`

**"Deepgram returned 401":** The API key is wrong or expired. Get a fresh one from [deepgram.com](https://deepgram.com) and replace `Documents\Claude\Skills\deepgram-key.txt`.

**"ffmpeg not found":** Step 3 of setup wasn't completed or the PATH didn't update. Restart Command Prompt or restart Windows.

**Instagram fails:** Instagram fights yt-dlp aggressively. If the public URL fails, you have two options:
1. Open the post in Chrome, use SurfFast/Unmixr to download the audio, then run `transcribe <audio file>`
2. Wait — yt-dlp updates frequently; running `pip install -U yt-dlp` once a month tends to fix Instagram breakage

## For Jason and Ellie

Their setup is identical. They each:
1. Install Python + the two pip packages + ffmpeg (one-time)
2. Get the Deepgram key from Graeham and save to `Documents\Claude\Skills\deepgram-key.txt`
3. Copy `transcribe_local.py` and `transcribe.bat` from this repo to anywhere on their machine
4. Run `transcribe <URL>` whenever they need a transcript
5. In their Cowork, say "Repurpose the latest from my inbox"

That's the whole workflow.

## Architecture honesty

This CLI exists because the Cowork bash sandbox is network-restricted. Long-term, this functionality moves into Property OS as a backend service (see `PROPERTY_OS_SPEC.md` in `_shared/transcription/`). Until then, the local CLI is the agentic-feeling path that actually works.
