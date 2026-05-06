# Standing Rules — Watts Motion Graphics

These are Graeham's locked rules that apply to every video, every graphic, every render. Do not break them.

## Pulled from Graeham's standing production rules

### Audio = master clock
- All graphic timings must be **phrase-anchored**, not timestamp-anchored
- Reason: timestamps drift across re-renders; phrases are stable
- Example correct: "HERO triggers on the word 'tax-free' in Scene 5"
- Example wrong: "HERO triggers at 04:32"
- Generate timestamps with Whisper transcription, then convert phrases → frames at render time

### One HERO per video
- Watts Gold `#B8945A` is reserved for ONE moment per video
- The HERO is the climax — the contrarian payoff, the revelatory number, the punch line
- Hold 5–7 seconds — never cut early
- Music drops to silence at HERO trigger
- All other gold accents use General Accent `#C4A265`

### No DRE number on screen
- DRE# 02015066 / 01466876 should NEVER appear in any graphic
- This is a Graeham-specific compliance / brand rule
- DRE goes in the video description, the dashboard, the disclosure end-card audio — not in any motion graphic

### No newsletter references
- Graeham does not run a newsletter
- No graphic should reference subscribing to a newsletter, joining a newsletter, etc.
- CTAs are direct: "comment OPTIONS", "DM me", "schedule a call"

### Long-form ↔ Short-form pairing
- Every long-form (16:9) video needs a matching short-form (9:16) cut
- The short-form is **NOT a crop** of the landscape version — it's a separate Remotion project sized 1080×1920
- Both files use the `-greenbg.mp4` suffix
- Short-form graphics use larger text relative to frame (mobile viewing)

### HERO framing
- The HERO graphic is positioned in the bottom-third or right-third of frame
- Never centered (per Vaibhav-style rules)
- The avatar takes the remaining negative space
- 5–7 second hold is non-negotiable
- Pair with audio gravity: near-silence, music drop, slow VO

## Pulled from Graeham's brand rules

### Watts Gold protection
- `#B8945A` only appears ONCE per video
- If you find yourself using Watts Gold for a top stroke or arrow accent, you're using the wrong color
- Use General Accent `#C4A265` for those
- This rule is what makes the HERO land

### Editorial, not TikTok
- Sharp corners (0px radius), not rounded
- Opacity fade animations only — no springs, no swooshes, no pops
- Generous padding inside panels
- Tracked-out uppercase eyebrow labels
- The visual feel should be closer to The Atlantic than to TikTok

### Typography hierarchy
- Syne Bold = display (HERO, scene titles, option labels)
- Inter = body (eyebrow labels, body copy)
- Never substitute Helvetica or Arial
- Self-host woff2 files when possible to guarantee consistent rendering

## Compliance and Fair Housing

When the graphic content includes language about housing, lending, demographics, or location:

- Avoid steering language ("good neighborhood for families like yours")
- Avoid demographic characterizations (race, religion, family status, national origin)
- Use objective data ("13–14 days on market", "+19% YoY")
- The avatar speaks the words — graphics show numbers and labels only
- If a stat could be misread as steering, the graphic version should be neutral data only

If unclear: prefer the more objective phrasing. Graeham can re-record the avatar; he can't easily re-render compliant graphics.

## What to do if the user asks to break a rule

1. Flag it explicitly: "That conflicts with the [rule] standing rule"
2. Ask if they want to override for this one video, or update the rule
3. Don't just silently break the rule — Graeham's system depends on consistency

If overridden: document the override in the project's `CLAUDE.md` so Jason or future-Graeham can see why.
