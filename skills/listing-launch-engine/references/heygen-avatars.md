# HeyGen Avatar Inventory + Selection (what we have, what to render, what to capture)

A big share of the launch's "videos" are **talking-head segments rendered by HeyGen**, not filmed. So the skill should know what avatars exist, pick the right look per segment, and only put Graeham on camera for what genuinely needs him (or for capturing a NEW look). Source of truth for IDs: `../../heygen-video/references/avatars.md` and `../../heygen-elevenlabs-renderer/references/registry.json` (read those for exact look/voice IDs at render time; don't hardcode here).

## What Graeham already has (no filming needed to use these)

- **One avatar group** (`2160746aa659445e9cbfa4c02e5cf39c`) — one identity, multiple styles.
- **6 curated named looks** (use the right one per content type):

| Look | Type | Best for |
|---|---|---|
| `digital_twin` ← **default** | video (trained from real video) | Customer-facing, face-critical: listing intros, the Reveal, market updates, buyer Q&A, Disclosure Drop, client comms. Most authentically "Graeham." Portrait. |
| `freshly_ironed` | photo_avatar | Polished/professional: seller presentations, CMA walk-throughs, listing reveals. Portrait. |
| `fashion_flip` | photo_avatar | Higher-energy hooks + pattern interrupts; style variety in a calendar. Portrait. |
| `casual_chic` | photo_avatar | Approachable everyday content, informal buyer onboarding, social vignettes. Portrait. |
| `bespectacled` | photo_avatar | Tech / PropertyIQ-adjacent content. Portrait. |
| `suburban_serenity` | photo_avatar | **Landscape-first** — YouTube 16:9, neighborhood features, website hero. Use `--aspect 16:9`. |

- **~70 personal avatar variations** + **3 talking photos** in the library (extra angles/frames of Graeham) — available if a look needs variety.
- **2 cloned voices:** **Voice Clone** (`Pa3vOYQHHpLJn1Tf7hnP` / HeyGen `717249201f7745988219b9aeb9041b42`) = **default across all looks**; **Twin voice** (`7739db30…`) natively paired with digital_twin — A/B test for pacing. Both sound like Graeham.

## Selection logic (per talking-head / VO segment)

1. **Pick the look by content type** using the table above (default `digital_twin` for anything customer-facing and face-critical).
2. **Mark the segment's source** so Peter and Wesley know what to do:
   - `AVATAR (HEYGEN — existing look)` → render from a trained look. **No filming.** This should be MOST talking-head lines.
   - `AVATAR (HEYGEN — NEW look, capture this trip)` → we want a fresh look; capture avatar-source on the shoot (see `avatar-source-specs.md`).
   - `LIVE` → Graeham filmed on camera (e.g. the raw POV walkthrough, or a piece that needs the real location behind him).
3. **Voice** defaults to the Voice Clone; note `--voice` only if A/B testing the Twin.
4. The SSML for each rendered segment lives in the Script Library (PART 5); `heygen-video` / `heygen-elevenlabs-renderer` render straight from it.

## Creating NEW avatars (when the long shoot is worth it)

The shoot window is a chance to add looks we don't have yet:

- **On-location look** — Graeham in front of the actual listing (or a signature EPA backdrop). Capture 2–3 min locked, even light, held framing (`avatar-source-specs.md`), then train a new look in the HeyGen web UI. Gives hyper-authentic "I'm standing at the home" talking-heads we can render forever.
- **Seasonal / wardrobe refresh** — if the current photo_avatar looks are stale, grab fresh source for an updated set.
- **PropertyIQ / brand avatar** — still pending; train when the brand identity is locked, then add a 7th look entry in `heygen-video/references/avatars.md` with role `propos_brand`.

Only spec a NEW-look capture when there's a real use for it — otherwise render from the 6 existing looks and keep Graeham's on-camera block short.

## Why this matters for capacity

Because the 6 looks are already trained, the skill can script **many** talking-head videos (Disclosure Drop, market updates, buyer/seller education, neighborhood explainers, the whole MOFU/BOFU set) that need **zero extra filming** — they render from existing looks + the cloned voice + the SSML. That is what lets one shoot feed a month-plus of video: filmed B-roll from the long shoot + a deep avatar-rendered talking-head library on top.
