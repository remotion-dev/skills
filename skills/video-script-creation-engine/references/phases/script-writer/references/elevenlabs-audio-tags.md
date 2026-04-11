# ElevenLabs-Ready Script Variant — Audio Tags & Inflection Guide

Every BOFU long-form and short-form script this skill produces must also be output in an **ElevenLabs-Ready Variant** so Graeham can paste it directly into ElevenLabs (v3 or v2) for AI voice / AI avatar generation. This file is the source of truth for how to tag a script for ElevenLabs.

---

## Why this matters

Graeham delivers a large percentage of his content via AI avatar + AI voice. The single biggest reason AI voice sounds robotic is flat, uninflected delivery. ElevenLabs gives us inline controls to fix that, but only if the script is written *for* the engine. A script that reads well for a human reader will sound monotone through ElevenLabs unless we add the right markers.

---

## Which ElevenLabs model do we target?

**Primary target: ElevenLabs v3 (Eleven v3 / alpha)** — this is ElevenLabs' current flagship expressive model and it accepts their **audio tag** syntax (square-bracket inline directives like `[excited]`, `[whispers]`, `[pause]`). v3 is the right choice for emotional, marketing, and direct-to-camera content.

**Secondary target: ElevenLabs v2 / Multilingual v2 / Turbo v2** — these accept a limited SSML subset. The only SSML tag that reliably works across v2 models is `<break time="Xs"/>` for explicit pauses. Other SSML tags (emphasis, prosody, say-as) are inconsistently honored.

**Rule of thumb:** write the script for v3 audio tags first. Then produce a fallback version that swaps the audio tags out and uses `<break>` tags + capitalization + punctuation for v2.

---

## The six control levers in ElevenLabs

There are six ways to shape inflection in an ElevenLabs script. Use all of them — they compound.

### 1. Audio tags (v3 only) — inline emotional and delivery directives

Audio tags are written in square brackets inline with the script. They tell v3 *how* to deliver the next chunk of text. They are NOT spoken aloud.

**Emotional / tonal tags Graeham should lean on:**
- `[excited]` — for hooks, big reveals, stats that matter
- `[serious]` — for legal education, risk warnings, AB 1482, tax content
- `[empathetic]` — for layoff content, divorce, first-time-buyer nerves
- `[curious]` — for "here's what most people are missing..." transitions
- `[confident]` — default for most of Graeham's content; he sounds like an expert friend
- `[warm]` — for the close / sign-off
- `[concerned]` — for risk warnings, compliance gotchas, "don't make this mistake"
- `[matter-of-fact]` — for data recitations and stat-heavy sections

**Delivery tags:**
- `[pause]` — short beat (about 0.5 sec)
- `[long pause]` — longer beat (about 1 sec) for dramatic effect
- `[whispers]` — for a "lean-in" moment, use sparingly
- `[emphasizes]` — makes the next phrase stand out
- `[slower]` — slows the pace for complex info
- `[faster]` — speeds up for energetic sections

**Rules for audio tags:**
- Place the tag directly before the phrase it modifies, on the same line.
- Don't stack more than one tag at a time on the same phrase (it confuses the model).
- Don't use audio tags on every sentence — it will sound bipolar. Aim for one tag every 2–4 sentences, at moments of real tonal shift.
- Never use audio tags that imply something Graeham wouldn't actually do (no `[angry]`, no `[crying]`, no `[sarcastic]` unless the script is specifically written for irony).

### 2. Break tags (v2 + v3) — explicit pauses

`<break time="1.0s"/>` inserts a hard pause. This works in v3 AND v2, so it's the most portable control.

**When to use break tags:**
- After the hook, before the rest of the intro
- Before a big stat or reveal
- Between major sections of a long-form script (replaces `[PAUSE]` from the human-readable script)
- Before the CTA

**Typical durations:**
- `0.3s` — tiny breath beat inside a sentence
- `0.5s` — standard comma-level pause
- `0.8s` — sentence-end pause for weight
- `1.0s` — section break
- `1.5s` — big dramatic beat (use once or twice per script, not more)

**Rule:** Don't exceed ~1.5s or ElevenLabs may interpret it as the end of the audio and cut off. Also, break tags longer than 3 seconds are officially unsupported.

### 3. Capitalization — emphasis

ElevenLabs v3 respects ALL CAPS as a vocal stress signal. This is one of the strongest levers we have.

- ✅ *"Do NOT drain your 401(k) yet."* → "NOT" gets vocal stress.
- ✅ *"The cap is 5 percent plus CPI, with an absolute maximum of 10 PERCENT per year."*
- ❌ *"DO NOT DRAIN YOUR 401(K) YET."* → entire sentence shouted, unnatural.

**Rule:** Use ALL CAPS on exactly the ONE word you want stressed, not whole sentences. Usually one capitalized word per 2–3 sentences.

### 4. Punctuation — pacing and prosody

Punctuation drives ElevenLabs' prosody more than any other text cue. Rewrite for the ear, not the eye.

- **Ellipses `...`** — create a natural trailing pause. Good for suspense. *"Here's what most people are missing..."*
- **Em dashes `—`** — create a mid-sentence beat, faster than a comma but softer than a period. *"The mistake I see people make — draining the 401(k) — costs them thirty-five percent."*
- **Commas** — standard short breath.
- **Periods + line break** — longest pause before next sentence.
- **Question marks** — raise the intonation at the end; use them liberally for engagement.
- **Multiple periods before a word** — slight hesitation beat. *"And the answer is . . . probably not."*

**Rule:** shorter sentences sound better through ElevenLabs than long ones. If a sentence is longer than ~20 words, break it with an em dash or split it into two.

### 5. Spelling out for clarity

ElevenLabs mispronounces some things. Pre-fix them in the script.

- **Numbers that matter:** spell out percentages as words → "5 percent" not "5%" (ElevenLabs sometimes says "five per cent" with a weird break otherwise). Write dollar amounts as "1.2 million dollars" not "$1.2M".
- **Acronyms:** insert periods for letter-by-letter pronunciation (e.g., "H.E.L.O.C." vs. "HELOC"), or write the expanded phrase ("home equity line of credit") on first mention.
- **Street names and neighborhoods:** if ElevenLabs mispronounces a local name, spell it phonetically in the script (e.g., write "Menlo Park" as "Men-loh Park" if needed — test first).
- **Legal citations:** "A.B. 1482" is more reliably pronounced as "A B fourteen eighty-two" or "Assembly Bill fourteen eighty-two".

### 6. Paragraph length — chunking for the voice engine

ElevenLabs generates prosody per-chunk. If a paragraph is too long, the voice loses energy toward the end.

**Rule:** Keep every paragraph in an ElevenLabs-ready script to 3 sentences max. For Graeham's AI avatar delivery, this is already the standard. Insert a `<break time="0.5s"/>` between paragraphs instead of relying on blank lines.

---

## The standard tag palette for Graeham's content

These are the only tags you should use by default. Don't invent new ones. Don't use anything outside this list unless there's a specific reason.

**Emotional:** `[excited]`, `[serious]`, `[empathetic]`, `[curious]`, `[confident]`, `[warm]`, `[concerned]`, `[matter-of-fact]`

**Delivery:** `[pause]`, `[long pause]`, `[emphasizes]`, `[slower]`

**Breaks:** `<break time="0.3s"/>`, `<break time="0.5s"/>`, `<break time="0.8s"/>`, `<break time="1.0s"/>`, `<break time="1.5s"/>`

---

## Content-type defaults — which base tone to start with

| Content type | Default base tone | Common secondary tags |
|---|---|---|
| Tech layoff / trigger event (BOFU) | `[empathetic]` | `[concerned]` for risk, `[confident]` for CTA |
| Legal education (AB 1482, tax, contracts) | `[serious]` | `[matter-of-fact]` for stats, `[confident]` for the CTA |
| Market update / data piece | `[matter-of-fact]` | `[excited]` for big numbers, `[curious]` for "here's what's interesting" |
| Buyer / seller education | `[confident]` | `[curious]` for transitions, `[warm]` for close |
| Lifestyle / TOFU reels | `[excited]` or `[warm]` | `[curious]` for the hook |
| Neighborhood deep-dive | `[confident]` | `[warm]` for lifestyle moments |
| Testimonial / case study | `[warm]` | `[confident]` for results |

---

## Do / Don't list

### DO
- Output the ElevenLabs variant as a separate section in the content package, labeled clearly.
- Keep every paragraph 3 sentences or less.
- Use ALL CAPS for single-word emphasis, not phrases.
- Use `<break time="Xs"/>` for dramatic beats in both v2 and v3 variants.
- Include a "model target" line at the top (e.g., *Target: ElevenLabs v3*).
- Produce BOTH a v3 audio-tag version AND a v2-compatible break-tag fallback version for long-form scripts that Graeham might use in either engine.
- Include a "voice settings recommendation" line at the bottom (Stability / Similarity / Style — see below).

### DON'T
- Don't put audio tags on every sentence — one every 2–4 sentences.
- Don't use audio tags that conflict with Graeham's brand (no `[angry]`, no `[sad]`, no `[sarcastic]`).
- Don't exceed `<break time="1.5s"/>` (2 sec max, 3 sec never).
- Don't leave `[TEXT OVERLAY]` or `[B-ROLL]` markers from the human script in the ElevenLabs version — strip them. ElevenLabs will try to speak them.
- Don't leave `$`, `%`, `&`, or other symbols ElevenLabs might mispronounce — spell them out.
- Don't leave em dashes adjacent to words with no spaces — always put a space on each side.

---

## Recommended ElevenLabs voice settings for Graeham

Include this at the bottom of every ElevenLabs variant so Graeham knows what to punch into the ElevenLabs UI. These are starting points — he can adjust.

```
Voice: [Graeham's cloned voice or selected preset]
Model: Eleven v3 (primary) | Eleven Multilingual v2 (fallback)
Stability: 0.45  (lower = more expressive, higher = more consistent)
Similarity: 0.75
Style: 0.35     (v3 only — 0.30-0.40 is the sweet spot for confident + natural)
Speaker Boost: ON
```

For long-form (4+ min) scripts, increase Stability to 0.55 to avoid drift. For short-form hooks, decrease Stability to 0.35 for more energy.

---

## Output format — the ElevenLabs variant section

Every content package MUST include a section titled **"ElevenLabs-Ready Variant"** that contains:

1. **Model target line** — which ElevenLabs model the script is written for.
2. **v3 Audio-Tag Version** — the script rewritten with audio tags, break tags, capitalization, and cleaned punctuation. NO `[TEXT OVERLAY]` or `[B-ROLL]` markers. NO dollar signs or percent signs — spelled out.
3. **v2 Fallback Version** (long-form only) — the same script with audio tags removed, relying only on `<break>` tags, capitalization, and punctuation.
4. **Voice settings block** — the recommended Stability / Similarity / Style / Speaker Boost values.
5. **Pronunciation notes** — any street names, neighborhoods, or terms that might need respelling for pronunciation.

See the short-form + long-form examples in this skill's `examples/` folder for the expected format.

---

## Self-check before returning the ElevenLabs variant

- [ ] No `[TEXT OVERLAY]`, `[B-ROLL]`, or `[PAUSE]` markers left in (stripped or replaced with `<break>`)
- [ ] No `$`, `%`, `&`, or other problematic symbols — all spelled out
- [ ] No paragraph exceeds 3 sentences
- [ ] Audio tags used sparingly (one every 2–4 sentences, not more)
- [ ] ALL CAPS only on single stress words, not full phrases
- [ ] Break tags used for pacing, none exceed 1.5s
- [ ] Voice settings block included at the bottom
- [ ] v2 fallback version included for long-form scripts
