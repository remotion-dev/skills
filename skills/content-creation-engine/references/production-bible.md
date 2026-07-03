# V6 Production Bible

Referenced from SKILL.md's "V6 Production Bible Integration" section. Load this file when actually writing scripts as part of a V6/V7 Production Calendar (Phase G / Phase 5 script-writer), not during ideation, scoring, or research phases.

When scripts are generated as part of a V6 Production Calendar (content-calendar skill), the output format changes from standalone markdown to **embedded HTML derivative panels** inside the hosted calendar page.

## Derivative Format System

Every content day MUST produce scripts for ALL of these platform formats:

| Format | Key Specs | Notes |
|--------|-----------|-------|
| **YouTube Long** | 8-15 min, 16:9, 1080p | Core asset — fullest script with all production details |
| **YouTube Short** | 30-59 sec, 9:16, 1080p | Strongest hook + one key insight + CTA |
| **IG Reel #1** | 30-60 sec, 9:16, 1080p | Hook-first, face-to-camera, caption overlay |
| **IG Reel #2** | 15-30 sec, 9:16, 1080p | Different angle/hook from Reel #1, B-roll heavy |
| **IG Carousel** | 5-10 slides, 1:1 or 4:5 | Key stats/facts as visual slides, swipe CTA |
| **TikTok** | 30-60 sec, 9:16, 1080p | More casual tone, trending audio hook if applicable |
| **Blog** | 800-1200 words, SEO-optimized | AEO-ready with cite-worthy key statements |
| **GMB (Google My Business)** | 100-300 words, 1 image | Local SEO post, location-tagged |
| **Facebook** | Cross-post from primary + FB-native caption | Longer caption OK, link in post |

Each derivative panel includes: full script, platform specs, caption with hashtags, description/SEO metadata, posting instructions, and GHL keyword CTA.

## Inline Shot Direction Tags

Every script (especially the YouTube Long core asset) MUST include inline shot direction tags embedded directly in the script text. These tell Jason (the video editor) exactly what visual to use at each moment:

```
[TALKING HEAD] — Graeham speaking directly to camera
[B-ROLL: description of footage needed] — Overlay footage
[TEXT OVERLAY: "exact text to display"] — On-screen text/graphics
[DRONE: description of aerial shot] — Drone footage
[SCREEN RECORD: description of what to capture] — Screen recording
[TRANSITION: type] — Cut/dissolve/swipe transition
```

Place these INLINE within the script, not as a separate section. Example:
```
[TALKING HEAD] "If you own rental property in California, you need to know about AB 1482."
[TEXT OVERLAY: "AB 1482 — California Tenant Protection Act"]
[B-ROLL: California apartment complexes, rental signs]
"This law caps your annual rent increase at 5% plus CPI, or 10% — whichever is lower."
[TEXT OVERLAY: "Max Increase: 5% + CPI or 10%"]
```

## Editing Notes for Jason

Every core asset script MUST include an **Editing Notes** block — a dedicated section for the video editor with production-specific instructions:

```
EDITING NOTES FOR JASON:
B-ROLL SHOT LIST:
- [List specific B-roll clips needed with descriptions]
- [Include stock footage suggestions if no original footage exists]

TEXT OVERLAY TIMING:
- [Timestamp] -> [Text to display] (duration: Xs)
- [Timestamp] -> [Text to display] (duration: Xs)

PACING NOTES:
- [Specific pacing instructions — fast cuts for hook, slower for education, etc.]

THUMBNAIL CONCEPT:
- [Describe the thumbnail — text, expression, background, colors]

MUSIC / SFX DIRECTION:
- [Music mood, tempo, genre suggestion]
- [Specific SFX moments — whoosh on transition, ding on stat, etc.]
```

## ElevenLabs SSML Blocks

Every core asset script MUST include a complete ElevenLabs SSML block — the full script wrapped in `<speak>` tags with prosody and break markup so Graeham can paste it directly into ElevenLabs for AI avatar voice generation:

```xml
<speak>
  <prosody rate="medium" pitch="medium">
    If you own rental property in California,
  </prosody>
  <break time="400ms"/>
  <prosody rate="slow" pitch="low" volume="loud">
    you need to know about AB 1482.
  </prosody>
  <break time="600ms"/>
  ...
</speak>
```

Use `<break>` for natural pauses (the one tag `eleven_multilingual_v2` actually honors). `<prosody>` may be kept for human readability but **do not rely on it — v2 silently drops rate/pitch.** Real delivery control comes from clean text + bracket audio tags (`[excited]`, `[whispers]`) + `voice_settings`.

### TEXT NORMALIZATION (Mandatory — prevents garbles & question-endings)

Even with correct SSML we get garbled audio and statements that rise like questions. The cause is the *text*, not the tags. Normalize the spoken text BEFORE it goes in the `<speak>` block — this is non-negotiable:

1. **No em-dashes or double-hyphens in spoken text.** `—` and `--` are the single biggest source of garble. Replace with a period (new sentence) or a comma, or an explicit `<break time="0.3s"/>`. Em-dashes are fine in the on-screen TEXT OVERLAY, never in the TTS line.
2. **End every statement with a period, not a comma-splice or trailing dash.** A statement that ends mid-thought (comma, dash, ellipsis) makes v2 raise the pitch into a question. One idea = one period-terminated sentence.
3. **Reserve `?` for genuine questions only.** If a line shouldn't sound interrogative, it must not end in `?`.
4. **Spell it out:** numbers, prices, abbreviations as spoken (`$820,000` → "eight hundred twenty thousand dollars"; `AB 1482` → "A-B fourteen eighty-two"; `EPA` → "E-P-A" if it should be spelled, or "East Palo Alto" if read).
5. **Short sentences.** Break long compound lines into separate sentences with `<break>` between — shorter sentences = fewer prosody mistakes.
6. **Delivery via brackets, not prosody:** `[excited]` on the hook, `[calm]`/measured on education, `[warm]` on the CTA. Stability: raise `voice_settings.stability` (~0.5+) when a take comes out unstable.

The `.ssml.txt` handed to the renderer must already be normalized to these rules. If the text isn't clean, the render will fail QC and you'll re-roll — fix it here, once.

## AI Video Prompts (Seedance 2.0 / Kling)

For content days that would benefit from AI-generated video (cinematic hooks, B-roll that doesn't exist as footage, pattern-interrupt openers), include an **AI Video Prompt** block:

```
AI VIDEO PROMPT (Seedance 2.0):
SHOT: [Hook / B-Roll / Transition]
PROMPT: "Cinematic aerial drone shot of [description], golden hour lighting,
  slow dolly forward, shallow depth of field, 4K, [duration]s"
CAMERA: [Movement type — dolly, crane, orbit, static, handheld]
LIGHTING: [Golden hour / overcast / interior warm / etc.]
DURATION: [3-5 seconds typical]
USE IN EDIT: [Where this clip goes in the timeline]
```

### B-ROLL COVERAGE (Mandatory — replaces the old "2-3 per video" cap)

NEVER cap B-roll at a flat number. A whole video covered by 5 clips is the #1 quality complaint. Calculate coverage from runtime:

- **Rule:** plan **1 distinct B-roll / cutaway per 3–5 seconds of non-talking-head screen time.** Hooks and fast-cut openers run on the 3s end; calmer educational mid-sections on the 5s end.
- **Floors:** Short-form (30–60s) → **8–14** distinct visuals minimum. YouTube Long (8–15 min) → **40+** (mix of filmed shot-list + stock + AI-generated; they don't all have to be AI).
- Output the math in the Editing Notes: `non-TH seconds ÷ 4 ≈ N b-roll needed`. If you produced fewer than N, you are not done — keep going.
- Tag every needed visual with its **source route** so nothing is left to chance: `[AI]` (Seedance/Kling), `[STOCK]` (pull from library/Pexels), `[MAP]` (real Mapbox map of the actual address/area — never a generic map), `[FILM]` (add to videographer shot list). Location-specific shots (a named county, corridor, street) are `[STOCK]` or `[FILM]`, **never** a generic AI city.

### GENERATION RELIABILITY DISCIPLINE (prevents re-rolls — apply to every `[AI]` prompt)

Re-rolls happen because we animate a bad starting image and because prompts list motion before the frame is locked. Bake this in:

1. **Two-stage, start-frame first.** Always generate the **still start frame** (Nano Banana Pro / GPT Image) BEFORE animating. Cheap to redo; an expensive video built on a flawed frame is pure waste.
2. **First-frame QC gate (hard stop).** Do not animate until the still passes: no malformed hands/faces, no garbled text, correct/real location, intended lighting, no stray artifacts. If it fails, regenerate the *still*, not the video.
3. **Lock the frame before motion — fixed prompt order:** `composition → subject → camera shot type → camera MOVE → lighting → mood`. This ordering stops the model inventing motion before the scene is set.
4. **Specific camera verbs only:** dolly in, push in, orbit left, crane up, handheld follow, FPV, locked-off. Never vague ("dynamic", "cinematic motion") — vague verbs are what produce wrong/discontinuous motion and doors that open the wrong way.
5. **One action per clip.** Multiple simultaneous actions are where continuity breaks. Split into two clips instead.
6. **Negative guidance** where the tool supports it: `no warping, no extra limbs, no text artifacts, no morphing`.

Apply across hook shots (first 2–3s scroll-stopper), expensive/impossible-to-film B-roll (aerials, time-lapses, establishing), and transitions — at the coverage count calculated above, NOT a flat 2-3.

## GHL Keyword Capture Integration

Every script CTA must include a GHL comment-keyword trigger. Current active keywords:
`SELL`, `BUY`, `COSTS`, `OPTIONS`, `1482`, `EPA`, `VALUE`, `READY`, `INVEST`, `NUMBERS`,
`RELOCATING`, `MARKET`, `CHECKLIST`, `WATCH`, `RWC`, `PA`, `MP`, `SF`

Format: "Comment [KEYWORD] below and I'll send you [lead magnet]"

## AEO (Answer Engine Optimization)

Every long-form script and blog derivative MUST include **cite-ready key statements** — factual, data-heavy sentences that AI search engines (ChatGPT, Perplexity, Gemini) can cite as authoritative answers. Format these as standalone declarative statements with specific numbers, dates, or legal references.
