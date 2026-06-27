# Listing Content Engine — front-end (categorize → buyer-need → pick 3 hooks)

> Runs at **STEP 0.5** of `listing-launch-engine`, before any script is written, so the launch is built from a chosen angle instead of a cold hook. This is the agent-run version; the future automated version is PropertyIQ's **PropCast** module. The full hook template library, EPA-specific hooks, paid-ad set, and cinematic concepts live in the package at `Documents\Obsidian\Content Listing Engine\` — this file is the method.

## 1. Categorize — one primary lane (optional secondary)

| Lane | Looks like | Lead hook strategy | Shoot emphasis |
|---|---|---|---|
| **VALUE / FIXER** | lowest $/sqft, dated, needs work | price-anchor + equity/upside, "cheapest…", arbitrage | condition honestly, then lot/layout/ARV/repair path |
| **INVESTMENT / CASHFLOW** | ADU, rentable, multi-unit, high yield | rent/ADU math, "house that pays you", Airbnb | rent cards, parcel/Mapbox, calculator graphics |
| **LUXURY / LIFESTYLE** | turnkey, design, location, finishes | scarcity/privacy/land/design, one jaw-drop feature | slower pacing, architecture, light, twilight |
| **STANDARD / AVERAGE** | nothing obviously special (most homes) | **manufacture a true superlative cut from data**; force ≥1 comparison angle | floor plan, storage, parking, commute, inventory scarcity |

**Average-home rule:** an unremarkable home is never hookless — it is *un-ranked*. Rank it against its own slice until it's the cheapest / biggest-lot / lowest-$psf / best-commute / only-one-with-X in some **true, specific** cut.

## 2. Name the buyer by transactional need (never identity — Fair Housing)

`payment-sensitive` · `commute-sensitive` · `renovation-averse` · `ADU-seeking owner-occupant` · `rental-yield investor` · `low-maintenance`. These are economic/transactional drivers — **never** identity-coded labels ("first-gen", "downsizer", "family") which are a Fair-Housing proxy risk even internally. Each hook maps: **who it's for → the objection it attacks → the proof → the qualified next step.**

## 3. Pull the data angle (the superlative)

Request a **proof-backed** superlative (from PropSearch / MLS): cheapest active {type} in {city} · 3rd-cheapest on the Peninsula · lowest $/sqft · highest rent-to-price · biggest lot under {price band} · closest move-in-ready to {employer} · etc. **Treat every superlative as a `{claim}` variable** carrying its comparison set, source, and expiry. Never bake a stale number into a script; if it can't be proven, drop it or mark `[VERIFY]`.

## 4. The 8 hook families + 5 proven formulas

Families: data-anchored · curiosity/question · mythbuster · comparison/arbitrage · lifestyle/feature · social-proof · fear/urgency · visual-spectacle (paid/offer hooks defer to the Offer-Driven Hook Matrix / `meta-ads`).

Formulas: **Price+Fun-Fact** ("{price} and it has {one surprising feature}") · **Bold Question** ("Would you buy a house that pays you to live in it?") · **Mythbuster** ("Everyone thinks {belief}. Here's why that's wrong about {market}.") · **Data/Superlative** ("The {cheapest/highest-renting} {type} in {geo} right now.") · **Comparison/Arbitrage** ("{$X} gets you {this} in {A} or {that} in {B} — same commute.").

Universal rules: hook lands in the **first 3 seconds**, is about the **viewer not the agent** (kill "Hi, I'm…"), and is **specific not vague**.

## 5. Pick 3 lead hooks

Choose **one data/superlative**, **one curiosity/question or mythbuster**, **one lifestyle/feature**. For each, write BOTH:
- a **caption version** (price-led OK), and
- a **`video_safe` spoken version** (no price/rate/credit; address OK).

For a visual-spectacle hook, draw from `Hook Database\Cinematic Concepts` — real movie-trailer treatments (Dune, Mission: Impossible, F1, etc.) with Graeham embedded as the hero; two voices: Graeham's ElevenLabs clone + a separate deep **trailer-narrator** voice.

## 6. Copy-surface rule (hard)

| Surface | Price/rate/credit | DRE |
|---|---|---|
| Listing-VIDEO audio + on-screen graphics | ❌ never (address OK) | ❌ never on screen |
| Captions / strategy scripts / approved ad copy | ✅ allowed | n/a |

Every hook record stores both a `caption` and a `video_safe` version. Schools = neutral fact only, never used to steer.

## 7. CTA

Opportunity / strategy pieces end with the GHL comment-keyword CTA (e.g. comment **GUIDE** → lead magnet). See `content-creation-engine`'s `lead-capture-keywords.md`.

## 8. Hand to the build sequence

Carry the **lane + buyer-need + the 3 hooks (each in both versions)** into build-sequence **step 1** — `content-creation-engine`'s `script-writer` writes the full word-for-word scripts (+ ElevenLabs variants) **from these hooks**, not cold.

## Source library

- Hook Database v1 (seed) + EPA-specific hooks + paid-ad set + Cinematic Concepts → `Documents\Obsidian\Content Listing Engine\Hook Database\`
- Video Editor SOP → `…\Content Listing Engine\Engine Spec\00 — Video Editor Listing SOP`
- Future automation (the learning brain) → PropCast module; build spec in `…\Engine Spec\04` + `04b`.
