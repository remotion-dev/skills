# Transcript Repurposer — How to Use It

For Jason and Ellie (and any future editor on the Watts content team).

This is your quick-start guide. From "I have a video URL" to "here are 10 deliverables ready to edit," in 3-5 minutes per video.

---

## What this thing does

You give it a URL to any video on the internet — Instagram Reel, TikTok, YouTube Short, podcast, whatever. It does this in one go:

1. Downloads the audio
2. Transcribes it (free Whisper by default, or Deepgram premium if Graeham flips that on)
3. Analyzes what the original video was actually trying to say
4. Decides how to make Graeham's version better
5. Adds Bay Area / real estate research where it fits
6. Writes 3 new hooks, scored, with a recommendation
7. Writes scripts for YouTube Long, YouTube Short, IG Reel, TikTok, Blog, GMB, Facebook
8. Generates HeyGen avatar script (paste-ready) + Higgsfield B-roll prompts + ElevenLabs voice markup
9. Humanizes everything so it doesn't sound AI-written
10. Delivers a folder with one downloadable file per artifact + an HTML preview

You get back a folder. You open `index.html` in your browser. You see everything in a clean dashboard. You download whichever file you need.

---

## How to run it (in your own Cowork session)

You need Cowork installed and the Watts skills synced. If you haven't done that yet, ping Graeham — he'll walk you through it once.

Once Cowork is open with the skills loaded, just type one of these:

**With a URL (the fastest path):**

```
Repurpose this Instagram Reel: https://www.instagram.com/reel/Cxxxxx
```

**With a URL and a quality flag:**

```
Repurpose this YouTube video at premium quality: https://youtube.com/...
```

(Premium tier uses Deepgram — costs about $0.02 per video, near-instant. Use it for important content or long podcasts. Skip it for everyday repurpose work.)

**With an existing transcript** (if you already transcribed elsewhere):

```
Repurpose this transcript: [paste transcript or attach .txt/.srt file]
```

**Only want certain outputs:**

```
Repurpose this URL and just give me the IG Reel and TikTok: https://...
```

That's it. Cowork takes over.

---

## What you get back

A folder named something like `transcript-repurpose-bay-area-mortgage-rates-20260516-1015\` in either:

- `Documents\Claude\online-content\repurpose\` (for published team work)
- The session outputs folder (for drafts)

Inside the folder:

| File | What it is | When to use it |
|---|---|---|
| `index.html` | The dashboard view — open in browser | **Start here every time.** Preview the whole package, click downloads |
| `transcript.txt` | Raw transcript of the source video | If you want the original words for reference |
| `content-package.md` | Everything in one markdown | If you want the master copy |
| `hooks.md` | 3 hook variants + the recommendation | When deciding between hook angles for A/B testing |
| `script-yt-long.md` | Long-form YouTube script with inline shot tags | For full YouTube production |
| `script-yt-short.md` | 30-60 sec Shorts script | YouTube Shorts |
| `script-ig-reel.md` | 30-60 sec Reel script with caption overlay tags | Instagram Reels |
| `script-tiktok.md` | TikTok script | TikTok posts |
| `script-blog.md` | 800-1200 word blog post, SEO-tuned | Website / newsletter content |
| `captions.md` | All per-platform captions + hashtags | Drop into the platform when posting |
| `ssml.xml` | ElevenLabs voice markup (XML) | When generating voice in ElevenLabs |
| `heygen-script.txt` | Clean script with NO shot tags — for the avatar mouth | Paste directly into HeyGen |
| `broll-prompts.md` | Higgsfield B-roll prompts (image + motion) | For Jason — generates the B-roll clips |
| `editing-notes.md` | Shot list, text overlay timing, pacing notes, thumbnail concept | **Jason — this is yours.** Your editing brief |
| `manifest.json` | Index of all files + metadata | For automated tooling later |

---

## The HTML preview (`index.html`)

When you open `index.html`, you see:

- The video title, source URL, platform, duration, word count, transcription tier used
- A grid of all the artifact files with download buttons
- The hook variants block (so you can read them without opening a separate file)
- A scrollable full-package preview with a "Copy full package" button

You don't need to be online for the HTML to work. It's a self-contained file. Open it from File Explorer — double-click `index.html` and your default browser will show it.

---

## Typical workflow for repurposing one video

For Jason (video editor):

1. Graeham (or you) drops a URL into Cowork. Skill runs. Folder lands in `online-content\repurpose\`.
2. Open `index.html`. Glance at the hooks. Read the editing notes.
3. Download `heygen-script.txt`. Paste into HeyGen, render the avatar video.
4. Download `broll-prompts.md`. Use the prompts in Higgsfield to generate B-roll clips. The prompts are paired (one image prompt + one motion prompt per shot).
5. Download `ssml.xml`. Use it in ElevenLabs if generating voice separately from HeyGen.
6. Open `editing-notes.md` in your editor of choice. That's your brief — shot list, timing, thumbnail concept.
7. Edit. Publish.

For Ellie (social media / captions):

1. Open `index.html`. Read the hooks.
2. Download `captions.md`. Each section has the caption for its platform plus hashtags.
3. Open the right platform script (`script-ig-reel.md`, `script-tiktok.md`) for the caption-overlay text.
4. Post.

---

## When things go wrong

**"yt-dlp download failed" / "URL is private or geo-blocked"**

The video can't be downloaded. Three options:

1. Check if the post is public (private Instagram or unlisted YouTube fails)
2. Try a different URL for the same content (sometimes a YouTube version exists where the Instagram one doesn't)
3. Use SurfFast or Unmixr to get the transcript manually, then paste it into Cowork

**Transcript looks garbled or has wrong words**

Whisper occasionally misses on accents or fast speech. Either:
- Re-run at premium quality (`Repurpose this at premium quality: <URL>`) — Deepgram is more accurate
- Edit `transcript.txt` manually and re-run the skill with the cleaned transcript

**The hook recommendation doesn't fit Graeham's voice**

The 3 variants are options. If the recommended one doesn't land, use one of the other two — or ask Cowork:

```
Try a different hook for this — the recommended one is too [hype/corporate/generic]. Use a [story / contrarian / personal] angle.
```

**You only need one derivative**

Tell the skill upfront. "Just give me the IG Reel" or "skip the blog and YouTube Long." Saves time.

---

## Quality tiers — when to flip premium

**Default (Whisper local — free):**
- 30-90 sec social videos
- Most content with clear speech, no heavy accents
- When you're prototyping multiple versions of a topic

**Premium (Deepgram — paid):**
- Podcasts over 15 min
- Accented speakers or noisy audio
- Important client testimonials where every word matters
- When you need the script delivered in under a minute, not 5

If you're not sure, default is fine. You can always re-run at premium.

---

## Cost expectations

For your reference (Graeham covers this):

| Tier | Per-video cost | Typical use |
|---|---|---|
| Whisper local | $0 | 80-90% of jobs |
| Deepgram (60-sec reel) | ~$0.005 | When quality matters |
| Deepgram (5-min podcast clip) | ~$0.02 | Heavy-accent or important content |
| Deepgram (30-min podcast) | ~$0.13 | Long-form repurpose |

Run premium whenever you genuinely need it — Graeham would rather spend $0.13 than have a transcription error make it to publish.

---

## Where to ask for help

- **Skill won't fire / unclear what to type:** Ping Graeham
- **Output is missing a section:** Open `content-package.md` and check if Phase 6 produced that derivative. If it didn't, the input transcript may have been too thin (under 50 words) — ask for a manual paste or a longer source video.
- **HTML preview won't open:** Try right-click → Open With → Browser. The file is local, no internet needed.
- **Want a feature added:** Tell Graeham. The skill is in `Documents\Claude\Skills\skills\transcript-repurposer\` — he can extend it.

---

## What this skill does NOT do (yet)

- It doesn't post to platforms for you. You still publish manually.
- It doesn't generate the video (HeyGen + Higgsfield handle that separately — the skill just produces the prompts).
- It doesn't track which repurposed videos performed best — that's the social-media-analyzer skill, separately.
- It doesn't access Graeham's CRM or schedule the content — that's a different skill.

This skill is one thing: URL/transcript in, multi-platform script package out. Everything else is downstream.
