# Phase 6 — Multi-Platform Script Writing

By the time you get here you have: the source brief, the chosen repurpose angle, the research pack, and the winning hook. This phase produces the actual content package.

## The Platform Spec Matrix

Each derivative has its own format. Don't write one script and try to make it fit everywhere — write to the format.

| Format | Duration | Aspect | Word count (approx) | Hook depth | Body structure |
|---|---|---|---|---|---|
| **YouTube Long** | 8-15 min | 16:9 | 1200-2200 | First 30 sec | Hook → context → 3-5 key points → tactical detail → CTA |
| **YouTube Short** | 30-59 sec | 9:16 | 80-150 | First 3 sec | Hook → ONE insight → CTA |
| **IG Reel** | 30-60 sec | 9:16 | 80-150 | First 2 sec | Hook → ONE insight → CTA (caption-overlay compatible) |
| **TikTok** | 30-60 sec | 9:16 | 80-150 | First 2 sec | Hook → ONE insight → CTA (slightly more casual cadence) |
| **IG Carousel** | 5-10 slides | 1:1 or 4:5 | 30-60 per slide | Slide 1 | Slide 1 = hook image+text; slides 2-N = key facts; final slide = CTA |
| **Blog** | n/a | n/a | 800-1200 | First paragraph | SEO H1 → intro → H2 sections matching key points → cite-ready conclusion |
| **GMB post** | n/a | n/a | 100-300 | First sentence | Local SEO-tuned, one CTA, one image |
| **Facebook caption** | Cross-post adaptable | varies | 100-500 | First line | Longer caption OK; link to YT or website |

The user can request one derivative or all. Default behavior: produce all of them in one content package unless the user asks for fewer.

## Voice and Style — Graeham's Calibration

Match the voice rules from `video-script-creation-engine/references/phases/script-writer/references/voice-and-style.md`. If that file isn't accessible in the current session, fall back to these baselines:

- **Direct.** No throat-clearing. State the point.
- **Confident but calibrated.** Strong opinions, room for nuance. Don't overclaim.
- **Specific.** Concrete numbers, places, dates. "Redwood City April 2026" beats "in the Bay Area recently."
- **Plain English over jargon.** When jargon is needed, define it once.
- **Working-agent voice.** Graeham sees deals every week. Write like someone who actually does this for a living, not someone who read about it.
- **No hype-isms.** No "absolutely insane", "game-changing", "you won't believe", "literally". Cut on sight.
- **No corporate-ese.** No "leverage", "synergy", "ecosystem", "at its core". Cut on sight.
- **Humor lands when it's dry.** Understated humor is on-brand. Hype humor is off-brand.

## Inline Shot Direction Tags

Embed these directly in YouTube Long and (sparingly) in YouTube Short script text. Don't break them out into a separate section — they need to be inline so Jason (the editor) sees them in context.

```
[TALKING HEAD] — Graeham speaking direct to camera
[B-ROLL: <description of footage needed>] — Overlay footage
[TEXT OVERLAY: "<exact text to display>"] — On-screen text/graphics
[DRONE: <description of aerial shot>] — Drone footage
[SCREEN RECORD: <description of what to capture>] — Screen capture
[TRANSITION: <type>] — Cut / dissolve / swipe / jump
```

For IG Reel and TikTok scripts, use lighter tags — they're more often single-shot face-to-camera with caption overlay, so tag sparingly:

```
[CAPTION OVERLAY: "<text>"] — Burned-in caption
[CUT] — Hard cut between takes (jump cut)
```

## Editing Notes Block (YouTube Long only)

For the YouTube Long derivative, append a structured editing notes block aimed at Jason or whoever's editing:

```
EDITING NOTES FOR JASON

B-ROLL SHOT LIST:
- <Specific clip needed with description>
- <Specific clip needed with description>
- <Specific clip needed with description>

TEXT OVERLAY TIMING:
- [00:08] → "Title overlay text" (duration: 3s)
- [00:42] → "Stat callout text" (duration: 4s)
- ...

PACING NOTES:
- Hook: fast cuts every 1.5-2 sec
- Body: medium pace, 3-5 sec per cut
- CTA: slower, hold the camera 2-3 sec longer

THUMBNAIL CONCEPT:
- Text: "<thumbnail text>"
- Expression: <description>
- Background: <description>
- Color palette: <description>

MUSIC / SFX:
- Music mood: <description>
- Specific SFX moments: <list>
```

## ElevenLabs SSML Block

Required for YouTube Long. Optional for short-form (still useful if Graeham is doing voice-over).

Wrap the script in `<speak>` tags. Use `<prosody>` for emphasis shifts and `<break>` for natural pauses.

```xml
<speak>
  <prosody rate="medium" pitch="medium">
    The opening line of the hook,
  </prosody>
  <break time="400ms"/>
  <prosody rate="slow" pitch="low" volume="loud">
    the high-stakes claim or number.
  </prosody>
  <break time="600ms"/>
  <prosody rate="medium" pitch="medium">
    Continuing the body...
  </prosody>
</speak>
```

Prosody calibration:
- **Hook** — slightly faster rate, slightly higher pitch (energy)
- **Body/educational** — medium rate, medium pitch (clarity)
- **Key stat or surprising line** — slower rate, lower pitch, louder volume (emphasis)
- **CTA** — slower rate, deliberate, louder (call to action energy)

## Captions Per Platform

| Platform | Style | Length | Hashtag count |
|---|---|---|---|
| Instagram | Punchy first line (hooks in feed), then body, then CTA | 100-200 words | 5-10 |
| TikTok | Very short, hook-heavy, often single sentence | 30-80 words | 3-6 |
| YouTube Short | Title-style + brief description + CTA | 50-100 words | 3-5 |
| YouTube Long description | SEO-tuned, full breakdown, links, chapters | 200-400 words | 0-5 |
| Facebook | Conversational tone, more room | 100-300 words | 2-5 |
| GMB | Local-keyword-heavy, location tagged | 100-300 words | 0 |

## CTA Slot — GHL Keyword Capture

Every script ends with a comment-keyword CTA. Pull from the active keyword set:

| Keyword | Lead magnet (typical) | Use when |
|---|---|---|
| `SELL` | Seller toolkit | Topic targets sellers |
| `BUY` | Buyer toolkit | Topic targets buyers (general) |
| `COSTS` | Closing cost breakdown PDF | Cost / fee topics |
| `OPTIONS` | Loan options comparison | Mortgage / financing topics |
| `1482` | AB 1482 tenant rights guide | California rent / tenant topics |
| `EPA` | East Palo Alto market report | EPA-specific |
| `VALUE` | Free home valuation | Selling / equity topics |
| `READY` | First-time-buyer checklist | First-time-buyer topics |
| `INVEST` | Investment property analysis | Investor topics |
| `NUMBERS` | Cap rate / cash flow calculator | Investor finance topics |
| `RELOCATING` | Relocation guide | Move-in / out-of-area topics |
| `MARKET` | Latest market update | General market topics |
| `CHECKLIST` | Pre-listing prep checklist | Prep / staging topics |
| `WATCH` | Off-market opportunities watchlist | Inventory / availability topics |
| `RWC` | Redwood City market report | RWC-specific |
| `PA` | Palo Alto market report | PA-specific |
| `MP` | Menlo Park market report | MP-specific |
| `SF` | San Francisco market report | SF-specific |

Format: "Comment <KEYWORD> below and I'll send you <lead magnet>."

## Cross-Posting Consistency

When generating all derivatives at once, ensure:

1. **Core claim is consistent.** The same point is being made across all formats. Don't soften it on one platform and strengthen it on another — that produces brand inconsistency.
2. **Hook is variant per platform.** The 60-second IG Reel hook is sharper/faster than the 12-minute YouTube long hook. Adapt, don't duplicate verbatim.
3. **CTA keyword is consistent.** Same GHL keyword across all derivatives so the lead capture lands in one bucket.
4. **Data points are identical.** If the YouTube long cites "82% of Peninsula buyers in April 2026 paid over asking," the IG Reel cites the same stat with the same date stamp. No "approximately" on one platform and exact on another.

## Output Format

```
## Content Package — <topic slug>

### Repurpose Brief
- Source: <platform / brief description>
- Repurpose Angle: <angle>
- Recommended Hook: Variant <N> from hook generation

### YouTube Long (8-15 min, 16:9)
<full script with inline shot direction tags>

EDITING NOTES FOR JASON:
<editing notes block>

ELEVENLABS SSML:
<full SSML block>

### YouTube Short (30-59 sec, 9:16)
<tight script>
Caption: <caption>
Hashtags: <hashtags>

### Instagram Reel (30-60 sec, 9:16)
<script with [CAPTION OVERLAY] tags>
Caption: <caption>
Hashtags: <hashtags>

### TikTok (30-60 sec, 9:16)
<script>
Caption: <caption>
Hashtags: <hashtags>

### Instagram Carousel (5-10 slides)
Slide 1 (hook): <text>
Slide 2: <text>
...
Slide N (CTA): <text>
Caption: <caption>
Hashtags: <hashtags>

### Blog (800-1200 words, SEO)
<full blog with H1, H2 structure, cite-ready statements>

### GMB Post (100-300 words)
<post text>
Location tag: <neighborhood>

### Facebook Caption
<caption>

### CTA — Across All Formats
GHL Keyword: <KEYWORD>
Format: "Comment <KEYWORD> below and I'll send you <lead magnet>."
```

Hand this entire package to Phase 7 for handoff block generation, then Phase 8 for humanizer.
