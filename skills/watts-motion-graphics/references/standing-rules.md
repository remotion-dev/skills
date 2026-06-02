# Standing Rules — Watts Motion Graphics

These are Graeham's locked rules that apply to every video, every graphic, every render. Do not break them.

## 📁 Default save location → C:\Users\Admin\Downloads\ (READ FIRST)

Final deliverables — any `-greenbg.mp4`, `-alpha.mov`, project zip, finished asset, or render output — save to **`C:\Users\Admin\Downloads\`** by default.

- If that folder is mounted in the session (Cowork directory access granted): write directly there.
- If it is NOT mounted: write to the session outputs scratchpad AND immediately call `mcp__cowork__present_files` to surface it. Never bury a final deliverable in the scratchpad without also surfacing it.
- If the user has mounted a different folder for the current project (e.g. a project folder under `Documents/`), prefer that mounted folder over Downloads — Downloads is the fallback default, not the override.

Operational tests that prove this is working:
- After every render, the file should be reachable by the user from their own file system without them asking "where is the file?"
- Status reports should always name the file location: "in Downloads", "in <mounted folder>", or "surfaced via the file card above"
- If you write to scratchpad but forget to call `present_files`, that is a rule violation — the deliverable is invisible to the user

Why: every prior production session (Bay Area Script, EPA Script, American Dream, etc.) shipped deliverables to Downloads. The convention is well established. The user's workflow assumes deliverables land where they can pick them up — Downloads is the canonical pickup point on Windows.

## 🎬 Title cards / hero cards / sign-offs → use the 3D title card mode

When Graeham asks for ANY of: **title card, hero card, intro card, name card, channel intro, listing intro, sign-off card, end-title card**, or any "3D gold text" / "3D chrome text" element — **read `references/3d-title-card.md` FIRST**, before the rest of standing-rules or brand-tokens.

That mode runs its **own** type system, its **own** output format, and is a **standing carve-out** from the Syne/Inter + chroma-green rules in the rest of this skill. Do not relitigate this every session. Do not push back on Sacramento, Archivo Black, 3D extrusion, or alpha .mov on brand-rule grounds — those choices are settled.

The locked defaults for 3D title-card mode:

| Setting | Value |
|---|---|
| 3D hero font | Archivo Black (`archivo-black.typeface.json`) |
| Cursive accent font | Sacramento |
| Gold material variant | `rich-gold` |
| Output container | `.mov` (ProRes 4444, native alpha — pixel format `yuva444p10le`) |
| Background | Transparent — NOT chroma green. Title cards use real alpha. |
| Project to use | `assets/3d-title-project/` — pre-built. Edit `src/Root.tsx` for content. |
| Filename suffix | `-alpha.mov` (NOT `-greenbg.mp4`) |
| Save location | `C:\Users\Admin\Downloads\` per the rule above |

The brand-tokens rules (Syne/Inter typography, #00FF00 background, chroma-key MP4 with `-greenbg` suffix) apply to the **5 in-video overlay templates** (Stat Callout, Compare Card, Decision Framework, HERO Reveal, End Card). They do NOT apply to title cards, hero cards, or anything else governed by `3d-title-card.md`.

If a request is ambiguous (e.g. "make me a card"), ask once: in-video data overlay, or branded title/hero element? Then route accordingly.

The HERO Gold protection rule (`#B8945A` once per video) applies to the *in-video* HERO Reveal template, NOT to the 3D title card. The 3D title card's chrome material is the locked `rich-gold` variant — it is not a HERO Gold usage and does not count against the per-video Watts Gold budget.

## ⛔ Always render, never hand off source

When Graeham asks for a motion graphic, the deliverable is a **finished MP4 chroma-key file** (overlay templates) or a **finished alpha `.mov`** (3D title card), not a Remotion project zip.

- Build the project in the remote sandbox (`/home/user/<project-name>/`)
- `npm install` the deps (Remotion + `@remotion/google-fonts` for Syne and Inter)
- `npm run render` to `C:\Users\Admin\Downloads\<project-name>-greenbg.mp4` (overlay) or `C:\Users\Admin\Downloads\<project-name>-alpha.mov` (3D title) at 1920×1080, 30fps
- Pixel-verify the output (top-left corner is `#00FF00` chroma green; panel center is `#000000` solid black; gold border samples to `#C4A265` General Accent — or `#B8945A` Watts Gold ONLY for the HERO)
- Save the file to `C:\Users\Admin\Downloads\` per the default save location rule above, AND call `present_files` so the user gets a chat card

**Why**: Graeham works from iPhone, Windows desktop, and CapCut. Mac Studio is for dev/automation, not for one-off graphic renders. Shipping a project zip and asking him to `npm install && npm run render` adds friction and breaks his flow. He wants the file ready to drop on the CapCut top track from his Downloads folder.

**Exception**: only ship the project source if Graeham explicitly asks for it (e.g., "give me the code" or "I want to edit it"), OR the rendering environment cannot complete the render in available time (e.g. Cowork sandbox 45s shell ceiling can't host a 2min Three.js render). If shipping source under the sandbox exception, log it in the project's `CLAUDE.md` with the reason and note that future-Claude should NOT take this as license to ship source by default.

**Standing rule applies to all motion-graphic deliverables**: stat callouts, compare cards, decision frameworks, HERO reveals, end cards, 3D title cards, sequenced compositions like the penalty stack, and any future templates added to this skill.

## Pulled from Graeham's standing production rules

### Audio = master clock
- All graphic timings must be **phrase-anchored**, not timestamp-anchored
- Reason: timestamps drift across re-renders; phrases are stable
- Example correct: "HERO triggers on the word 'tax-free' in Scene 5"
- Example wrong: "HERO triggers at 04:32"
- Generate timestamps with Whisper transcription, then convert phrases → frames at render time

### One HERO per video (in-video overlays only)
- Watts Gold `#B8945A` is reserved for ONE moment per video — applies to the in-video HERO Reveal template only
- The HERO is the climax — the contrarian payoff, the revelatory number, the punch line
- Hold 5–7 seconds — never cut early
- Music drops to silence at HERO trigger
- All other gold accents in overlay templates use General Accent `#C4A265`
- Does NOT apply to 3D title card mode (see title-card section above)

### No DRE number on screen
- DRE# 01466876 / 01466876 should NEVER appear in any graphic
- This is a Graeham-specific compliance / brand rule
- DRE goes in the video description, the dashboard, the disclosure end-card audio — not in any motion graphic

### No newsletter references
- Graeham does not run a newsletter
- No graphic should reference subscribing to a newsletter, joining a newsletter, etc.
- CTAs are direct: "comment OPTIONS", "DM me", "schedule a call"

### Long-form ↔ Short-form pairing
- Every long-form (16:9) video needs a matching short-form (9:16) cut
- The short-form is **NOT a crop** of the landscape version — it's a separate Remotion project sized 1080×1920
- Both files use the `-greenbg.mp4` suffix (overlay) or `-alpha.mov` suffix (3D title)
- Short-form graphics use larger text relative to frame (mobile viewing)

### HERO framing (in-video HERO Reveal only)
- The HERO graphic is positioned in the bottom-third or right-third of frame
- Never centered (per Vaibhav-style rules)
- The avatar takes the remaining negative space
- 5–7 second hold is non-negotiable
- Pair with audio gravity: near-silence, music drop, slow VO
- Does NOT apply to 3D title card mode

## Pulled from Graeham's brand rules

### Watts Gold protection (in-video overlays only)
- `#B8945A` only appears ONCE per video in the in-video overlay template stack
- If you find yourself using Watts Gold for a top stroke or arrow accent on an overlay panel, you're using the wrong color
- Use General Accent `#C4A265` for those
- This rule is what makes the HERO land
- 3D title card mode is exempt — its `rich-gold` chrome material is not a HERO Gold usage

### Editorial, not TikTok (in-video overlays only)
- Sharp corners (0px radius), not rounded
- Opacity fade animations only — no springs, no swooshes, no pops
- Generous padding inside panels
- Tracked-out uppercase eyebrow labels
- The visual feel should be closer to The Atlantic than to TikTok
- The 3D title card mode is allowed to use scale-spring pop-in entries — its animation is locked separately in `3d-title-card.md`

### Typography hierarchy (in-video overlays only)
- Syne Bold = display (HERO, scene titles, option labels)
- Inter = body (eyebrow labels, body copy)
- Never substitute Helvetica or Arial
- Self-host woff2 files when possible to guarantee consistent rendering
- 3D title card mode runs its own type system (Archivo Black + Sacramento) — see `3d-title-card.md`

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

**BUT**: do not relitigate carved-out exceptions. The 3D title card mode is a settled carve-out. If a request matches that mode (see title-card section above), route to `3d-title-card.md` and proceed — do not raise the brand-rule conflict. Same for the Downloads default save location — that's the established convention from prior production sessions and is not up for debate every time.
