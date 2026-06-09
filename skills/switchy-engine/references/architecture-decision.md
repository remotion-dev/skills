# Architecture Decision — standalone `switchy-engine`

## Recommendation (validated, with one refinement)
**Build `switchy-engine` as a standalone skill that other skills call into —
YES.** Add one refinement: the durable *constants* (pixel IDs, default domain,
tag vocabulary, vendor-exclusion list location) live in `shared-references`, so
the engine and every caller read one source of truth. Capability = skill;
constants = shared config.

## Why the hypothesis holds (receipts from the actual skill stack)
The codebase already proves both halves of this pattern:

- **"Build once, reference everywhere" is the established norm.** `cma-generator`
  is called by `newsletter-generator`'s home-value CTA; `content-calendar` hands
  topics to `content-creation-engine`; multiple skills read
  `../shared-references/identity.json` instead of hardcoding brand facts;
  `github-skill-sync` is a horizontal utility that other skills invoke after any
  change. A cross-cutting engine that many skills call is the system's own idiom.

- **Burying a cross-cutting capability inside a host skill has already failed
  here — twice.** `content-creation-engine`'s own changelog records that
  `video-research-engine` went *dormant* inside it ("most users didn't know it
  existed, trigger keywords didn't match how people speak, visual analysis was
  coupled to content generation when it should be standalone") and was extracted
  into `video-watcher` + `video-transcriber`. Link/pixel logic is exactly that
  kind of horizontal capability. Embedding it in newsletter or content engine
  would repeat the documented mistake.

## Alternatives considered (and why they lose)

| Option | Verdict | Reason |
|---|---|---|
| **A. Duplicate link/pixel logic in each skill** | ❌ Reject | Guaranteed drift; token-handling code copied into 6+ places = 6 ways to leak a credential; pixel list + tag vocab diverge. This is the anti-pattern the repo fought by merging. |
| **B. Config-only in `shared-references`, no skill** | ⚠️ Partial | Constants belong there, but Switchy needs live API calls, its own analytics output, and its own trigger surface ("how many scans did X get?"). That's an invokable capability, not passive data. |
| **C. Fold into an existing skill** (content-calendar / ghl-crm-audit) | ❌ Reject | Switchy spans far past any one host — postcards, yard signs, GBP, listings, email. Coupling to one host = the dormancy trap again. |
| **D. Build a Switchy MCP** | ❌ Overkill | No MCP exists; brief says call the API directly. An MCP is heavy for a single-user read API. A skill is right-sized. |
| **E. Standalone skill + shared constants** | ✅ **Adopt** | Capability gets its own trigger + analytics; constants stay single-sourced; callers reference by name. |

## The call contract (what callers use)
Downstream skills stop emitting raw consumer URLs and instead:
- **mint(destination, tags[], pixels[], domain?, slug?)** → Switchy short URL (+QR).
- **report()** → scans→audience→budget table.
Constants (`pixels[]` defaults, default `domain`, tag vocabulary, exclusion-list
path) come from `shared-references/switchy.json` (to be created — see asks).

## Per-skill wiring points (from the STEP 1 inspection)

| Skill | Link/QR emission point today | Action |
|---|---|---|
| **newsletter-generator** (EPA Report) | "Watch the full video" → YouTube; "What's My Home Worth?" → graehamwatts.com/home-value; footer social | **Wrap all CTAs.** Highest-value surface (opted-in consumers). Add: "mint each CTA via switchy-engine, tags `newsletter`+`consumer`." |
| **content-creation-engine** | YouTube CTAs, social post links, link-in-bio across 14 formats | **Wrap consumer CTAs + bio links.** Add mint step in the content-package output; tag by platform + `consumer`. |
| **html-email** | CTA buttons in designed emails | **Wrap CTAs conditionally.** Many of these go to partners/coaches (B2B) — tag `b2b`, track-only, don't pixel. Consumer emails → wrap + pixel. |
| **weekly-listing-update** | Seller-facing report; "view listing online" type links | **Track-only.** Audience is a single known seller (sphere) — don't pixel. Optional Switchy for click visibility. |
| **listing-remarks-writer** | NONE — MLS public remarks legally cannot contain URLs/contact info | **No wrap in remarks.** Flag: the *marketing collateral* around the listing (single-property page, flyers, QR) is where tracked links go, not the MLS remarks themselves. |
| **postcard workflow (Canva — no skill)** | QR codes designed manually in Canva | **GAP.** See below. |

## Postcard integration (CORRECTED 2026-05-28)
A `farming-postcard` skill DOES exist (earlier inspection used the session's
plugin-mounted skills copy, which omitted it; the source-of-truth repo at
Documents/Claude/Skills has it). It already renders print-ready cards in the locked
brand and routes each card's QR target through `references/cta-router.md`. That
router is the clean integration point: instead of a raw landing URL it returns a
**Switchy short link** (pixel + UTM baked in), and the QR encodes that. One change,
every future postcard becomes a pixeled, scan-tracked, swappable-destination
retargeting surface. No new skill needed — farming-postcard CALLS INTO
switchy-engine, which strengthens the standalone-engine decision.

## Net
Standalone `switchy-engine` + `shared-references/switchy.json` constants, callers
reference by name, postcard QR routed through the engine. This matches the stack's
proven idioms and avoids its two documented failure modes (duplication-drift and
buried-capability dormancy).
