---
name: vaibhav-template
description: Turn any script into a Vaibhav Sisinty-style talking-head video for Graeham Watts — the visual formula reverse-engineered from @vaibhavsisinty's 1.7M-follower Instagram reels. Fires on "run this script through the template I love", "make this Vaibhav-style", "use my video template", "convert to Vaibhav format", "add the warm desk aesthetic", "put this in my rotation", or any request to produce a video where Graeham's face appears with the burned-in visual system (locked talking-head, fast front-loaded cuts, serif-italic captions, color-highlighted keywords, emoji pop-ins). Encodes Graeham's 5 pre-generated warm-lit avatar looks (rotate across videos for variety without breaking brand consistency), the 5-mode composition system, cut pacing arc, and typography specs. Hands script + look off to heygen-video for rendering and higgsfield-video for B-roll. Use this instead of freestyling a HeyGen render when the user wants the Vaibhav aesthetic.
---

# Vaibhav-Style Video Template — Graeham Watts

A reusable visual formula reverse-engineered from @vaibhavsisinty (1.7M followers, Instagram Reels). This skill doesn't make a video from scratch — it takes a script or topic and produces a shot plan, look choice, and caption spec that matches the Vaibhav aesthetic, then hands it to `heygen-video` for rendering and `higgsfield-video` for B-roll.

## When this fires

- "Run this script through the template I love"
- "Make this Vaibhav-style"
- "Use my video template on this"
- "Convert this script to the warm-desk look"
- "Add this to my content rotation"
- "Put this in the Vaibhav format"

If the user has a topic but no script yet, chain with `content-creation-engine` first — that writes the script (it absorbed `video-script-creation-engine` in April 2026), then hand it back to this skill.

---

## The reality

**This is a STYLE skill, not a rendering skill.** The actual video comes out of `heygen-video`. This skill's job is to make sure every HeyGen video Graeham publishes has the same visual grammar — so viewers recognize his content within 2 seconds regardless of topic.

Vaibhav's consistency is not an accident. His reels are recognizable within one frame because he locked in exactly five things: talking-head framing, cut pacing arc, typography, color grade, and caption placement. Those five things are this skill's entire contract.

---

## Visual system — the 5 composition modes

Every Vaibhav-style video is built from these 5 frames remixed. Don't invent new ones mid-video.

### Mode 1 — Hook composite (seconds 0–3 ONLY)
- **Top 60% of frame:** full-bleed B-roll of the HOOK subject (Sam Altman, a listing, a map, a headline)
- **Bottom 40% of frame:** LOCKED talking-head of Graeham, same position every video
- **Caption on split line:** serif italic subject name top, sans-serif supporting clause underneath
- **Source files:** Top needs Higgsfield B-roll; bottom uses one of Graeham's 5 warm-desk looks
- **Used for:** Opening hook, re-engagement moment mid-video if attention drops

### Mode 2 — Full-bleed talking head
- **Full frame:** Graeham's face, chest-up
- **Optional overlay:** red or orange color wash at 30% opacity (section transition)
- **Caption:** large serif italic center-frame
- **Used for:** Section transitions, high-emphasis statements, the "let me show you" pivot

### Mode 3 — Full-bleed B-roll
- **Full frame:** environmental B-roll (street shot, listing exterior, neighborhood)
- **Caption:** small white-on-dark translucent pill, center or bottom-third
- **Used for:** Market data, location grounding, visual establishment

### Mode 4 — Screenshot card (PiP)
- **Background:** solid dark/black
- **Top 60%:** product screenshot, document, or tool output (prompt card, listing MLS shot, Redfin page)
- **Bottom:** small inset of Graeham + big acid-green list number (`#01`, `#02`) + 3-line caption
- **Used for:** "Here's how to do it" content, tool walkthroughs, step-by-step

### Mode 5 — Section header
- **Background:** current warm-desk look, faded/darkened
- **Watermark center-back:** PropertyIQ logo or Graeham Watts Investment Properties mark at 20% opacity, large
- **Top overlay:** `##. TITLE CASE` in letter-spaced sans-serif
- **Used for:** Opening each numbered section in a listicle format

---

## Cut rhythm — the documented arc

From the reel analysis (80s, 52 cuts, scene-detection verified):

| Section | % of runtime | Cut density | Shot length |
|---|---|---|---|
| Hook | first 12% | 40% of all cuts | ~0.5s each |
| Setup | 12–38% | 15% of all cuts | ~2.5s each |
| Body | 38–75% | 27% of all cuts | ~2.0s each |
| Climax | 75–88% | 13% of all cuts | ~1.4s each |
| CTA | final 12% | 6% of all cuts | ~3.0s each |

**Key rule:** front-load 40% of your cuts in the first 10% of the runtime. This is what makes Vaibhav's style feel "fast" even though 80% of the video is moderately paced. Miss this and the video will feel slow no matter how good the rest is.

**Translation to production:** for a 60-second video, plan ~16 cuts in the first 6 seconds, then ~20 cuts over the remaining 54s.

---

## Typography — the distinctive signature

His fonts are what make this aesthetic look premium instead of generic-viral. Most reels editors use bold sans-serif. He does the opposite.

| Text type | Font | Weight | Color | Size | Example use |
|---|---|---|---|---|---|
| Primary subject | **Playfair Display** | Italic | White | Large (~80pt @ 1080p) | "Sam Altman", "Let me show you", place names |
| Secondary clause | **DM Sans** or **Inter** | Regular | White | Medium (~44pt) | "just killed the entire" |
| List numbers | **DM Sans Bold** | Bold | **Acid green** (`#BFFF00`) | Large | "**01.**", "**02.**", "**03.**" |
| Section titles | **DM Sans** | Medium, LETTER-SPACED 8% | White | Medium | "PRECISE TEXT", "REAL PRODUCT ACCURACY" |
| Burned-in captions | **Inter** | Semi-bold | White on translucent dark pill | Medium | Running dialogue captions |

**Color-highlighted keywords:** 1–3 emphasis words per caption get acid-green or warm-yellow highlight boxes behind the text. Only highlight nouns and verbs that carry meaning — never articles, connectors, or filler.

---

## Color & grade

- **Base palette:** warm tungsten orange (~3200K) + cool dusk blue (~5600K), simultaneously.
- **Grading move:** subject is warmly lit; background is cool and blurred. This is Vaibhav's single most important color rule.
- **Section washes:** red (30% opacity, sharp transition) and gold (20% opacity, gentle transition) — use to mark scene shifts, not every cut.
- **Never:** flat white balance, cool-only grade, or gray grade. The warm/cool split IS the look.

---

## Graeham's 5 looks — the rotation system

Five avatar looks, each shares the "warm-lit desk with subject facing camera head-on, desk horizontal across bottom of frame" foundation but varies outfit + environment. Rotate across videos so viewers see variety but instant brand recognition.

| Look name | Outfit | Environment | Best use |
|---|---|---|---|
| `warm_desk_navy` | Navy quarter-zip over white tee | Warm-lit home office, bookshelf + city window, brass lamp left | Everyday / default look — casual-professional |
| `podcast_studio` | Black crewneck | Acoustic foam panels, blue/teal dramatic accent lighting, SM7B broadcast mic visible | Hot takes, opinion content, long-form explainer |
| `loft_window` | Heather grey henley (top buttons undone) | Modern minimalist loft, blurred dusk city bokeh behind, warm lamp right edge | Lifestyle, neighborhood content, market storytelling |
| `corporate_office` | Charcoal suit jacket + light blue dress shirt + navy silk tie, **clear round wire-frame glasses** | Dark wood-paneled executive office, leather-bound books, brass desk lamp | Seller-facing content, CMA walkthroughs, listing presentations — "big deal" mode |
| `modern_studio` | Crisp white oxford, sleeves rolled, top button undone, **clear round wire-frame glasses** (same frames as corporate_office) | Clean minimalist studio, off-white/warm-grey backdrop, blonde-wood desk, brass arm lamp | Educational content, contract walkthroughs, "analyst mode" |

**Rotation rule:** match look to content intent, not randomly.
- Market update → `warm_desk_navy`
- Bold take / podcast-style → `podcast_studio`
- Neighborhood / lifestyle → `loft_window`
- Seller meeting, listing intro, "I just sold this for $X" → `corporate_office`
- "Here's how a contract works" / educational → `modern_studio`

**Don't rotate mid-video.** One look per video. Switching looks inside a single reel breaks identity.

---

## The skill's workflow

### Step 1: Understand the script's job

Before doing anything, identify:
- **Content type:** market update / bold take / lifestyle / seller-facing / educational
- **Target runtime:** 30s / 60s / 90s — this drives cut planning
- **Hook payload:** what ONE specific thing in the first 3 seconds stops the scroll
- **CTA:** what action at the end

Ask the user if any of these are unclear. Don't assume.

### Step 2: Pick the look

Match the content type to the look table above. State the pick with reasoning. Example:

> "This is a market-data video about EPA pricing. I'd use `warm_desk_navy` — it's the everyday default and the data-driven tone doesn't need the gravitas of `corporate_office` or the studio polish of `modern_studio`. Good?"

**Confirm before proceeding.** Don't assume the user wants the default.

### Step 3: Build the shot plan

Produce a table mapping each line/beat of the script to a composition mode + timing + caption spec. Example for a hook:

```
Time    Mode      Caption                              B-roll needed
0–1s    Mode 1    "Sam Altman" (italic, top)           portrait of person/subject
                  "just killed the entire" (bottom)    
1–2s    Mode 1    continues, crossfade caption         same / slight zoom
2–3s    Mode 2    "Image Gen Industry"                 Graeham full-bleed
                  (italic, yellow highlight on "Image")
3–4s    Mode 1    "with one big launch"                4K industrial image
4–5s    Mode 5    "01. PRECISE TEXT"                   Graeham warm_desk_navy + PropertyIQ logo fade
```

Front-load cuts per the rhythm arc. Fill in the Body and Climax with Modes 3 and 4. End in Mode 2 with a clean CTA.

### Step 4: List the B-roll Graeham needs

For each beat that requires a B-roll clip (Modes 1, 3, and sometimes 4), produce an explicit Higgsfield prompt. Hand these to the `higgsfield-video` skill when the user is ready to shoot them.

Example:
```
B-roll #1 (beat at 0–3s):
  Orientation: 16:9 (landscape)
  Prompt: "4K ultra-detailed portrait of tech CEO in black turtleneck, 
          multiple facial expressions composited in a grid, dark 
          dramatic studio lighting, shot on Kodak Portra 400, Douglas 
          Friedman editorial style. Horizontal 16:9."
  Duration: 4s
  Motion: slow push-in
```

### Step 5: Hand off to heygen-video

Once look + script are locked, call the `heygen-video` skill with:

```
python3 /path/to/heygen-video/scripts/create.py \
  --script "..." \
  --look <chosen_look> \
  --aspect 16:9 \
  --title "<content type> - <date>"
```

**Aspect:** All 5 Vaibhav looks are landscape-native (16:9). Graeham edits to portrait (9:16) in post. Always render at 16:9 from HeyGen.

### Step 6: Build the caption + typography sheet

Deliver a simple text file listing each caption beat, font, color, highlight words, and timing. Graeham's editor (or CapCut operator) uses this to burn in captions matching the Vaibhav typography spec.

---

## What this skill does NOT do

- ❌ Does not write the original script — use `content-creation-engine` or handle that separately
- ❌ Does not render video — always hands off to `heygen-video`
- ❌ Does not generate B-roll — produces prompts for `higgsfield-video` to execute
- ❌ Does not edit/composite final video — Graeham or his editor does this in CapCut / Premiere / After Effects using the shot plan + caption spec
- ❌ Does not let Graeham "freestyle" mid-video — one look, one grade, one typography system per video

---

## Why consistency matters (and why to resist "just this once" deviations)

Vaibhav's visual system looks simple because he never breaks it. 3,000+ posts at 1.7M followers — the same five composition modes, the same typography, the same warm/cool grade. Viewers recognize his content before the first word plays. That's the brand moat.

If Graeham mixes looks mid-video, or swaps fonts for "variety", or front-loads 5 cuts instead of 20, he'll get a video that's *fine* but doesn't read as *his*. That's the difference between "another real estate agent posting on IG" and "the Peninsula guy who does those cinematic reels."

**Strict adherence to this template IS the strategy.**

---

## Quick reference card

```
Input:    script + content_type
Output:   shot plan + look choice + caption spec + B-roll prompts + HeyGen invocation

LOOK DECISION TREE
  market-data / everyday          → warm_desk_navy
  bold opinion / hot take          → podcast_studio
  lifestyle / neighborhood         → loft_window
  seller-facing / listing intro    → corporate_office
  educational / contract breakdown → modern_studio

CUT RHYTHM
  First 10% of runtime:  40% of all cuts  (≈0.5s shots)
  10–38%:                15% of all cuts  (≈2.5s shots)
  38–75%:                27% of all cuts  (≈2.0s shots)
  75–88%:                13% of all cuts  (≈1.4s shots)
  Last 12%:              6% of all cuts   (≈3.0s shots)

TYPOGRAPHY
  Subject/emphasis:  Playfair Display Italic, white
  Secondary:         DM Sans Regular, white
  List numbers:      DM Sans Bold, acid-green #BFFF00
  Section titles:    DM Sans Medium, letter-spaced 8%, UPPERCASE
  Captions:          Inter Semi-bold on dark translucent pill

GRADE
  Warm face (3200K) + cool background (5600K) = the signature
  Section washes: red 30% (sharp), gold 20% (gentle)

COMPOSITION MODES (use only these 5)
  Mode 1  Hook composite (60% B-roll top / 40% locked Graeham bottom)
  Mode 2  Full-bleed talking head
  Mode 3  Full-bleed B-roll
  Mode 4  Screenshot PiP card
  Mode 5  Section header w/ logo watermark

ASPECT: render HeyGen at 16:9. Edit to 9:16 in post.
```

---

## Session history

Built 2026-04-23 with Graeham over a long working session. Reverse-engineered from an 80-second Vaibhav Sisinty reel (160 extracted frames, 52 scene-detected cuts, pacing arc measured per section). All 5 looks generated via Higgsfield Nano Banana Pro with identity-matched reference image, verified against Graeham's own selfie (`IMG_0520.JPG`). Anti-cleft prompt formula documented in `references/prompt_formula.md` — use this when regenerating or adding a 6th look.
