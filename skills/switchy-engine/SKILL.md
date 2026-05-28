---
name: switchy-engine
description: "Tracked-link + retargeting-pixel engine for Graeham Watts. The single source of truth for creating Switchy short links / QR codes that fire Meta/Google/etc. retargeting pixels on the redirect layer, and for pulling per-link scan/click analytics. Use this skill ANY time the user mentions: tracked link, short link, Switchy, shortlink, QR code, retargeting link, pixeled link, link analytics, scan count, click count, custom audience, retargeting audience, link in bio, UTM, swappable link, CTA link, or wants to know how a postcard/newsletter/listing/GBP link is performing. OTHER skills (content-creation-engine, newsletter-generator, weekly-listing-update, html-email, the postcard/Canva workflow, listing pages) CALL INTO this skill to mint tracked links instead of dropping raw destination URLs — build once, reference everywhere, so pixel + tracking logic never drifts. Also trigger on: 'wrap this link', 'make a tracked QR for the postcard', 'how many scans did X get', 'build the retargeting report', 'which links are feeding my audiences'."
---

# Switchy Engine — Tracked Links & Retargeting Pixels

The **one** place link-shortening, QR generation, pixel-tagging, and click/scan
analytics live. Everything else (newsletter, postcards, listing pages, GBP, email
signature) should request a tracked link FROM this skill rather than pasting a raw
destination URL. That is the whole point: mint once, pixel consistently, measure
in one dashboard, never duplicate the logic.

> **What Switchy does that a raw URL doesn't:** it sits on the redirect layer and
> fires retargeting pixels (Meta, Google/GA, LinkedIn, Pinterest, Bing, etc.)
> *before* the destination page loads, drops the visitor into a custom audience,
> tracks the scan/click, and lets you swap the destination later without changing
> the printed link or QR. Pixel fires even if the visitor bounces before the page
> renders.

---

## Confirmed API facts (developers.switchy.io, verified May 2026)

| Thing | Value |
|---|---|
| GraphQL endpoint | `https://graphql.switchy.io/v1/graphql` (POST, **queries only**) |
| REST link-create | `POST https://api.switchy.io/v1/links/create` (mutations are REST, not GraphQL) |
| Auth header | `Api-Authorization: <token>` — **not** `Authorization: Bearer` |
| Token scope | One token per **workspace**; API-key style, **not** OAuth |
| Schema style | Hasura (`where: { field: { _is_null: true } }` filter syntax) |
| Pixel platforms supported | linkedin, facebook, gtm, quora, pinterest, twitter, ga, bing, nexus, adroll, adwords |
| Rate limits (create) | 10,000 links/day, 1,000 links/hour |

### ⚠️ Two things that are NOT settled and must be confirmed live
1. **Per-link click/scan field name.** Public docs only show workspace-level
   fields (`workspaces`, `domains`). The field that holds per-link click/scan
   counts is **not documented** — you MUST introspect it on the live token before
   trusting any analytics query. Run `scripts/switchy_analytics.py --confirm-schema`.
2. **Token activation.** Switchy restricts API access; an account may need to ask
   Switchy **live chat** to enable API access before the generated token returns
   data. Confirm the token actually returns rows before wiring downstream skills.

### ⚠️ Platform caveat: no native TikTok pixel
Switchy's pixel platform list has no TikTok entry. For TikTok-sourced traffic,
either route through `gtm` (Google Tag Manager container that carries the TikTok
pixel) or accept click-tracking only. Don't promise native TikTok retargeting.

---

## Token setup (do this once)

1. Log in to Switchy → open the target **workspace** → **Settings → Integrations
   → Generate a token**.
2. If queries return empty/!errors, message Switchy **live chat** to enable API
   access for the account, then regenerate.
3. Store it — never hardcode, never commit:
   - Windows: `setx SWITCHY_API_TOKEN "your-token"`
   - mac/linux: `export SWITCHY_API_TOKEN="your-token"` (or `~/.switchy/token`, chmod 600)
4. Lock the schema: `python scripts/switchy_analytics.py --confirm-schema`
   → note the real click/scan field, pass it as `--click-field`.

---

## What this skill exposes to other skills (the contract)

Downstream skills should call ONE of these instead of emitting a raw URL:

- **`mint(destination, tags[], pixels[], domain?, slug?)`** → returns a Switchy
  short URL + (optional) QR PNG. Implemented via the REST create endpoint
  (`api.switchy.io/v1/links/create`). Always pass `tags` so the analytics layer
  can segment by source (e.g. `["newsletter","consumer"]`, `["postcard","qr","94303"]`).
- **`report()`** → runs `scripts/switchy_analytics.py`, returns the
  scans→audience→budget table (markdown + CSV).

> **Tagging convention (mandatory).** Every minted link gets:
> `surface` (gbp / newsletter / postcard / listing / signature / openhouse / yardsign / social-bio …),
> `audience-class` (`consumer` | `prospect` | `b2b` | `mixed`),
> and an optional `campaign` tag. The `audience-class` tag is what lets us EXCLUDE
> junk (vendor/agent clicks) from retargeting audiences. See
> `references/audience-hygiene.md`.

---

## Analytics: the core query flow

`scripts/switchy_analytics.py` does three things:

1. **`--confirm-schema`** — introspects the `links` type and prints real field
   names (mandatory first run on a live token).
2. **fetch** — queries all live links + their click/scan counts.
3. **model** — converts each link's clicks into a *targetable retargeting
   audience* and the *monthly ad budget that audience justifies* (frequency × CPM),
   flagging audiences too small to target.

```bash
python scripts/switchy_analytics.py --confirm-schema           # step 1, once
python scripts/switchy_analytics.py --click-field clicks       # normal run
python scripts/switchy_analytics.py --cpm 25 --frequency 12    # tune the model
```

Runs in **DEMO mode** with illustrative numbers if no token is set, so the output
format can be reviewed before go-live.

See `references/graphql-queries.md` for the raw queries (introspection, per-link
analytics, both scalar-count and aggregate shapes).

---

## When to use vs. not

**Use** when minting any link/QR that will sit in front of consumer or prospect
traffic, or when reporting on link/QR/scan performance.

**Don't bother wrapping** (raw URL is fine) when:
- The destination is Graeham's OWN already-pixeled site AND you don't need
  per-source attribution, destination-swapping, or multi-pixel firing (see
  `references/retargeting-pathway-map.md` → "own-site redundancy").
- The surface is a GBP **primary website field** — Google auto-removes redirect /
  shortener links there. Use the real domain in that field; use Switchy in GBP
  *posts* and secondary links instead. See `references/gbp-and-youtube.md`.

---

## Reference docs
- `references/graphql-queries.md` — introspection + analytics queries, REST create payload.
- `references/retargeting-pathway-map.md` — every surface, traffic type, retargeting value, caveats.
- `references/gbp-and-youtube.md` — the GBP redirect-policy answer + YouTube/own-site pixel-redundancy answer.
- `references/audience-hygiene.md` — what to pixel vs. skip, and source segmentation.
- `references/architecture-decision.md` — why this is a standalone called-into engine.
---

## Live-verified API capabilities (2026-05-28, real token)

Confirmed by introspecting the live GraphQL schema. **Read this before promising a metric.**

**Queryable top-level types:** `links`, `folders`, `pixels`, `domains`, `UTMTemplates`, `tokens`, `workspaces` (+ `_by_pk`).

**Per-link data you CAN get:** `id` (slug), `domain`, `url` (destination), `title`,
`tags`, `pixels`, `folderId`, `createdDate`, and **`clicks`** (total click/scan count — a QR scan and a link click both increment this).

**What you CANNOT get from the API (important):**
- **No per-click detail** — no referrer, no country/geo, no device, no timestamp-per-click.
- **No time-series** — only a running total. `uniq` is an internal ID, NOT a unique-visitor count.
- There is no clicks/stats/events table in the schema.

**Implications:**
1. **"Where clicks come from" must be ENGINEERED, not queried.** Source attribution lives in
   how each link is built — its **slug + tags + UTM**. A bare/untagged link is unattributable.
   This is why tagging discipline (below) is mandatory. (Richer geo/referrer/device stats DO
   exist in the Switchy *dashboard UI* per link, but are not exposed to the API.)
2. **Weekly trends require our own snapshots.** Since the API only returns a running total,
   the weekly digest must SNAPSHOT every link's `clicks` each Monday and DIFF against last
   week's snapshot to report "scans this week." Snapshots stored as dated JSON/CSV.
3. GA4 (via the UTM) and Meta (via the pixel) hold the richer behavioral/audience data —
   cross-reference there for on-site behavior and audience size.

## Naming & folder convention (mandatory — keeps everything decodable)
- **Slug:** `<surface>-<descriptor>-<MMDD>` e.g. `epa-comps-0601`
- **Title:** `Postcard EPA 2026-06-01 — Last 5 Homes (home value)` (date YYYY-MM-DD so it sorts)
- **Tags:** `surface` + `audience-class` + market + date, e.g. `["postcard","qr","consumer","epa","2026-06-01"]`
- **UTM:** `utm_source=<surface>&utm_medium=<channel>&utm_campaign=<surface>_<mmddyy>&utm_content=<archetype>`
- **Switchy folder:** by surface — `Post card qr` (id 92811), `Yard Sign QR` (80707), GMB folders, etc.

## Weekly digest (Monday) — design
A **scheduled task** (not duplicated in postcard/content skills) calls this engine every
Monday: it snapshots all link `clicks`, diffs against last week, and produces a dashboard +
email showing scans-this-week per source, audience growth, and suggested budget. Published to
`Graehamwatts/online-content/dashboards/switchy/` (hosted) and emailed. Because trend data
depends on our snapshots, the FIRST run only establishes a baseline (deltas start week 2).

## Callable contract (how other skills use this)
- `farming-postcard` / `content-creation-engine` call `mint()` here instead of emitting a raw
  URL — they pass destination + tags + pixels, get back a tracked short link + QR.
- Any skill can call `report()` to pull the current scans→audience→budget table.
- Constants (pixel IDs, default domain, tag vocab) live in `shared-references/switchy.json`.
