# Switchy Integration — Decision Brief

Prepared for Graeham Watts · 2026-05-28. Companion files live in the
`switchy-engine/` skill folder.

---

## 1. Architecture recommendation — build the standalone engine (validated)

Build **`switchy-engine`** as a standalone skill that newsletter, content engine,
postcards, listings, etc. **call into** — with one refinement: the durable
constants (pixel IDs, default domain, tag vocabulary, exclusion-list location) go
in `shared-references/switchy.json` so the engine and every caller read one source.

I didn't just accept the hypothesis — I pressure-tested it against your actual
stack, and it holds *because of receipts in the code itself*:

- Your skills already use "build once, reference everywhere" (`cma-generator`
  called by the newsletter, `identity.json` shared, `github-skill-sync` as a
  horizontal utility).
- Your `content-creation-engine` changelog literally documents the opposite
  approach failing: `video-research-engine` went **dormant** when buried inside a
  host skill and had to be extracted into `video-watcher`. Embedding link/pixel
  logic in the newsletter or content engine would repeat that mistake.
- Duplicating it per-skill would copy **token-handling code into 6+ places** — six
  ways to leak a credential and guarantee the pixel list/tag vocab drift apart.

Full reasoning + the per-skill wiring table: `switchy-engine/references/architecture-decision.md`.

**Where each skill plugs in:**
- **newsletter-generator** → wrap every EPA Report CTA (highest-value: opted-in consumers).
- **content-creation-engine** → wrap YouTube CTAs, social links, link-in-bio.
- **html-email** → wrap *consumer* emails only; B2B/coach emails track-only.
- **weekly-listing-update** → track-only (audience is one known seller).
- **listing-remarks-writer** → **no wrap** — MLS public remarks legally can't carry
  URLs. Tracked links go on the listing's collateral (property page, flyers, QR), not the remarks.
- **postcards** → **the gap** (see §5).

## 2. Retargeting pathway map

Full table (29 surfaces, with traffic type / value / pixel-or-not / caveat):
`switchy-engine/references/retargeting-pathway-map.md`. The three highest-leverage
buckets:

1. **Offline→online bridge** (postcards, yard riders, open-house QR, mailers,
   window cards) — traffic you *cannot pixel any other way*. A QR scan converts a
   physical mail drop into a digital retargeting audience.
2. **Non-owned platforms** (Zillow, Realtor.com, Nextdoor, GBP posts, social bios)
   — you can't put your pixel on their pages, so the redirect is the only hook.
3. **Per-source attribution at scale** (newsletter sections, listings, campaigns)
   — tagging tells you which surface actually built the audience.

## 3. GBP answer — NOT the website field; YES posts + secondary links

Google's Business links policy prohibits URLs that "redirect or refer" users
elsewhere, and Google now auto-removes violating links; shorteners in the
**primary website field** are a known enforcement target (real cases of links
getting pulled). So:

- **Primary website field:** real domain only (`graehamwatts.com`), pixeled
  natively. Don't risk your map-pack click.
- **GBP posts / appointment / secondary links:** Switchy is safe and is the right
  home for GBP retargeting.
- **Headline GBP play:** *GBP post link → YouTube channel* pixels every
  high-intent local searcher who clicks, then retargets them. Also: post→listing,
  post→home-value form, appointment→GHL booking.

Detail: `switchy-engine/references/gbp-and-youtube.md`.

## 4. YouTube / own-site answer — pixel is redundant, link still isn't

When a Switchy link points to your **own already-pixeled site**, the pixel-drop is
largely redundant (your site tags pixel them on load anyway). But Switchy still
earns its place for four non-pixel reasons: **per-source attribution**,
**swappable destination** (change a printed QR's target without reprinting),
**multi-pixel firing** (fire Meta+Google+LinkedIn from one link), and
**pixel-fires-before-page-load** (catches bouncers your on-site pixel misses).

Per-surface rule: **non-owned destination → always wrap (essential). Own pixeled
site → wrap only if you want attribution/swap/multi-pixel/pre-load capture;
otherwise raw URL is fine.** Print/QR pointing to your own site → still wrap (swap
value alone). Table in the same reference file.

## 5. The postcard gap (flagged)

There is **no postcard skill** — it's a manual Canva workflow, and its QR codes are
the single biggest missed retargeting opportunity (offline→online, un-pixelable
otherwise). Recommendation: short-term, have the Canva workflow mint its QR via
`switchy-engine` (one tagged tracked link per drop/ZIP); later, build a thin
`postcard-engine` that calls the engine automatically. Defer the new skill until
the link engine is live.

## 6. Audience hygiene tradeoff — don't pixel everything

Pixeling tiny or B2B traffic pollutes audiences and burns spend (showing listing
ads to your title rep; sub-100 audiences you can't even target).

- **PIXEL:** newsletter, SMS, listings, GBP posts, Zillow/Realtor, social bios,
  YouTube links, all offline QR.
- **SKIP/track-only:** email signature, LinkedIn, peer business cards, sphere/PCFS
  touches (mixed/B2B/known).
- **Segment** via mandatory `audience-class` tag (`consumer`/`prospect`/`b2b`/
  `mixed`) on every minted link; build ad audiences from `consumer`+`prospect`
  **minus a standing vendor/agent exclusion list**; never spend against a
  sub-1,000 standalone audience; build lookalikes only from clean seeds.

Detail: `switchy-engine/references/audience-hygiene.md`.

## 7. The scaffolded skill + working query

`switchy-engine/` contains:
- `SKILL.md` — engine definition, API facts, token setup, the mint/report contract.
- `scripts/switchy_analytics.py` — secure token handling (env/file, never hardcoded),
  schema introspection, the per-link analytics query (scalar + aggregate fallback),
  and the **scans → audience → budget** table. Runs in DEMO mode without a token;
  I've verified it executes and renders.
- `references/` — queries, pathway map, GBP/YouTube answers, audience hygiene,
  architecture decision.
- `sample_switchy_report.md/.csv` — sample output (illustrative numbers).
- `.gitignore` — keeps the token and workspace data out of version control.

The budget model: `audience = clicks × pixel-match-rate (55%)`; `monthly budget =
audience × frequency (10×) × CPM ($22) / 1000`. All three are CLI-tunable. It's the
spend an audience can *absorb*, not a target.

---

## What I need from you to finish (the asks)

1. **Token activation — the blocker.** Confirm whether your Switchy API token is
   actually enabled. Generate it (Workspace → Settings → Integrations → Generate a
   token); if the smoke-test query returns errors/empty, message Switchy **live
   chat** to enable API access, then regenerate. Until this returns rows, I can't
   lock the real click/scan field name or pull live numbers.
2. **Decision — GDPR popup.** Default `showGDPR: true` on cold consumer links (CA,
   safer, slightly lower match) vs. `false` (higher match, more exposure). Your call.
3. **Constants for `shared-references/switchy.json`:** your Meta pixel ID, GA
   measurement ID (and any LinkedIn/Pinterest/Bing pixels you want fired), and your
   preferred default Switchy domain. I'll wire these once you provide them.
4. **Vendor/agent exclusion list** — a CSV of known peers/vendors/team emails to
   stand up the standing exclusion audience.
5. **Approve the per-skill wiring** in §1 before I edit the live skills (right now
   `switchy-engine` is built but not yet referenced by newsletter/content/etc.).
6. **TikTok** — accept GTM-routed or click-only tracking (no native Switchy TikTok
   pixel), or drop TikTok from the pixel plan.

### Two accuracy flags (per your rules)
- The **per-link click/scan GraphQL field name is unverified** — public docs only
  show workspace-level fields. The script introspects it first; I did **not**
  fabricate a field name. Treat the analytics query as confirmed only after
  `--confirm-schema` runs on your live token.
- The sample report numbers are **illustrative DEMO data**, not real.
