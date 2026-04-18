# Graeham Watts — HeyGen Avatar Configuration

All 6 looks below belong to the same HeyGen avatar group: `2160746aa659445e9cbfa4c02e5cf39c` (one identity — Graeham — with multiple styles).

## Voice defaults — IMPORTANT

Graeham has **two cloned voices** in HeyGen — both are his, just from different training sessions. The skill defaults to the **Voice Clone** (`717249201f7745988219b9aeb9041b42`) globally across all 6 looks. Override per video with `--voice <id>`.

| Voice ID | HeyGen Name | Role |
|---|---|---|
| `717249201f7745988219b9aeb9041b42` | **Graeham Watts Voice Clone** | **DEFAULT** — used across all looks. Historically paired with the 5 photo_avatar looks. |
| `7739db30ae554014a7b93a59a134640e` | Graeham Watts -- 142 | "Twin" voice — cloned alongside the digital_twin video avatar. Pair via `--voice 7739db30ae554014a7b93a59a134640e` if A/B testing. |

**Both voices sound like Graeham** — the question is which clone renders with better pacing/tone. Test both before committing to the default long-term.

## The 6 Looks

### 1. `digital_twin` ← **DEFAULT LOOK** ← prefer for customer-facing content
- **Look ID:** `159cd7b883724fdb9a51b97dec94df89`
- **Name in HeyGen:** "Graeham Watts -- 142"
- **Avatar type:** `video` (digital_twin — trained from real video of Graeham)
- **HeyGen's native voice pairing:** `7739db30ae554014a7b93a59a134640e` (Twin voice)
- **Preferred orientation:** portrait
- **Use when:** Content must look authentically like Graeham — listing intros, market updates, buyer Q&A, client comms, anything face-critical. Skill-level default voice (Voice Clone) will be used unless `--voice` overrides.

### 2. `casual_chic`
- **Look ID:** `afdc7e3e9f0c45de896fa687c594a216`
- **Avatar type:** `photo_avatar`
- **HeyGen's native voice pairing:** `717249201f7745988219b9aeb9041b42` (Voice Clone — default)
- **Preferred orientation:** portrait
- **Use when:** Approachable everyday content, social vignettes, informal buyer onboarding.

### 3. `freshly_ironed`
- **Look ID:** `09fed5d2c0b74376b6e7313cbb888c86`
- **Name in HeyGen:** "The Freshly Ironed Look"
- **Avatar type:** `photo_avatar`
- **HeyGen's native voice pairing:** `717249201f7745988219b9aeb9041b42` (Voice Clone — default)
- **Preferred orientation:** portrait
- **Use when:** Polished, professional content — seller presentations, CMA walkthroughs, listing reveals.

### 4. `fashion_flip`
- **Look ID:** `b0644e6b20ba414981b7821d88caf675`
- **Avatar type:** `photo_avatar`
- **HeyGen's native voice pairing:** `717249201f7745988219b9aeb9041b42` (Voice Clone — default)
- **Preferred orientation:** portrait
- **Use when:** Higher-energy content, style variety in a content calendar, hooks and pattern interrupts.

### 5. `bespectacled`
- **Look ID:** `1b25c855f03b471da5bacb918c4acbc0`
- **Name in HeyGen:** "Bespectacled man in black sweatshirt"
- **Avatar type:** `photo_avatar`
- **HeyGen's native voice pairing:** `717249201f7745988219b9aeb9041b42` (Voice Clone — default)
- **Preferred orientation:** portrait
- **Use when:** Tech/PropOS-adjacent content until a real PropOS avatar is trained.

### 6. `suburban_serenity`
- **Look ID:** `bbc381b39e0f458e8d274cf1ac2c38ba`
- **Avatar type:** `photo_avatar`
- **HeyGen's native voice pairing:** `717249201f7745988219b9aeb9041b42` (Voice Clone — default)
- **Preferred orientation:** **landscape** (only one of the 6 that's landscape-first)
- **Use when:** Horizontal content — YouTube landscape, neighborhood features, website hero embeds. Override default `--aspect 9:16` to `--aspect 16:9` when using this look.

## Key design rule

**All 6 looks now use Graeham's voice** by default, so any look will sound like him. The face quality trade still applies:
- `digital_twin` = authentic face from real video (most "you")
- photo_avatar looks = AI-generated face variations (still you, but stylized/posed)

For customer-facing content that must feel genuinely personal, prefer `digital_twin` for the face even though voice is identical across both paths.

## When to retrain or add

- **New PropOS avatar:** Train a stylized / brand-aligned avatar in HeyGen web UI, then add a 7th entry here with role=`propos_brand` and likely a different voice.
- **Updated digital twin:** If Graeham re-records a training video, the new look ID replaces #1 above.
