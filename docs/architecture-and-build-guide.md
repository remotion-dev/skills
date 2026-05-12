# Architecture & Build Guide

> **Read this first.** If you're contributing to or rebuilding any part of Graeham Watts's skills repo, this document describes what's built, why it's built that way, and what's open work. Last updated April 2026.

This guide is written for a developer joining the project (Mehmood — building Graeham's systems alongside Uzair, Khawaja, Wattson). It assumes you can read code, but doesn't assume you've worked with Cowork or Claude Skills before.

---

## Table of Contents

1. [The Project: PropCast](#the-project-propcast)
2. [Repo Structure](#repo-structure)
3. [Core Architectural Decisions](#core-architectural-decisions)
4. [Data Flow Diagrams](#data-flow-diagrams)
5. [Skills Inventory](#skills-inventory)
6. [How Cowork Skills Work (Mechanics)](#how-cowork-skills-work-mechanics)
7. [Identity & Brand Hard Rules](#identity--brand-hard-rules)
8. [Integrations](#integrations)
9. [Pantana Reference (Category Context)](#pantana-reference-category-context)
10. [Open Work / Known Issues](#open-work--known-issues)
11. [Build Priorities](#build-priorities)
12. [How to Develop on This Repo](#how-to-develop-on-this-repo)

---

## The Project: PropCast

PropCast is a unified **content + transaction operating system** for real estate agents, built first for Graeham Watts (REALTOR, Intero Real Estate, Bay Area / East Palo Alto) and structured to be productized for other agents later.

PropCast covers two surfaces:

**Content side** (week-over-week, evergreen)
- Research signals across multiple data sources
- Topic ideation + scoring
- Multi-format content generation (video scripts, blog posts, social, email)
- Distribution (HeyGen avatar video, ElevenLabs voice, GoHighLevel CRM keyword capture, GitHub Pages publishing)

**Transaction side** (deal-by-deal)
- CMA generation (3-strategy pricing, branded report, GitHub Pages publishing)
- Offer analysis + comparison (multi-offer net sheets)
- Disclosure / inspection report analysis
- Listing remarks (MLS) + photo captions
- Price reduction conversations (data-backed angle for the seller convo)

Both sides are powered by **skills** running in **Cowork** (Anthropic's desktop product), backed by external integrations (Apify, Windsor MCP, GoHighLevel, HeyGen, ElevenLabs, GitHub). The skills repo is the codebase.

---

## Repo Structure

```
Graehamwatts/skills/                          (this repo)
├── .claude-plugin/
│   └── plugin.json                           (Cowork plugin manifest)
├── .git/, .nojekyll, index.html, assets/     (GitHub Pages landing infra)
├── CLAUDE.md                                 (root onboarding doc)
├── README.md                                 (public README)
├── docs/
│   └── architecture-and-build-guide.md       (THIS FILE)
├── scripts/
│   └── verify_brand_identity.py              (DRE-leak tripwire)
└── skills/                                   (all 39+ skills)
    ├── shared-references/
    │   ├── identity.json                     (BRAND IDENTITY SSOT)
    │   ├── integrations.md                   (canonical integration matrix)
    │   └── data-contracts.md                 (cross-skill JSON contracts)
    ├── content-creation-engine/              (main content engine)
    ├── content-calendar/                     (weekly planning)
    ├── bofu-query-generator/                 (standalone BOFU)
    ├── bofu-intent-scorer/                   (standalone BOFU scorer)
    ├── cma-generator/
    ├── offer-analyzer/
    ├── disclosure-analyzer/
    ├── listing-remarks-writer/
    ├── listing-photo-captioner/
    ├── price-reduction-angle-generator/
    ├── youtube-scraper/
    ├── ... (other skills — see Skills Inventory below)
    └── ...
```

**Sister repo: `Graehamwatts/online-content`** — published content hub (separate repo because it's a GitHub Pages site with public client-facing URLs; outputs and source code shouldn't mix). Renamed from `cma-reports` on 2026-05-01 to reflect that it holds ALL published content types, not just CMAs. The old `cma-reports` repo was retired with no migration — its content was disposable.

| Output type | Where it goes |
|---|---|
| Published CMAs | `Graehamwatts/online-content/cmas/` |
| Published offer reports | `Graehamwatts/online-content/offers/` |
| Published disclosure reports | `Graehamwatts/online-content/disclosures/` |
| Published newsletters | `Graehamwatts/online-content/newsletters/` |
| Weekly production calendars | `Graehamwatts/online-content/dashboards/weekly-calendars/` |
| Per-topic single-topic dashboards | `Graehamwatts/online-content/dashboards/single-topic/` |

---

## Core Architectural Decisions

### 1. GitHub Is the Source of Truth

- Skills repo: `https://github.com/Graehamwatts/skills`
- Working copy: clone via GitHub Desktop to `~/Documents/GitHub/skills`
- Cowork local plugin folder (`%APPDATA%/Claude/local-agent-mode-sessions/skills-plugin/`) is **downstream**. It syncs FROM GitHub. Edits made there don't persist.
- All architectural changes go: edit → commit → push → Cowork picks up updated skills on next session

If the local Cowork plugin shows skills that don't match GitHub, the local cache is stale. The remedy is forcing a Cowork sync (close + reopen Cowork session typically refreshes).

### 2. Engine + Standalone Pattern

Skills are organized in two tiers:

**Engines** — orchestrate multi-phase workflows. Examples: `content-creation-engine`, `content-calendar` (which absorbed `social-media-analyzer` in May 2026).

**Standalones** — single-purpose, can be invoked directly OR referenced by an engine. Examples: `bofu-query-generator`, `listing-remarks-writer`, `cma-generator`.

Engines reference standalones via **sibling-path imports** in their SKILL.md (e.g., engine's Phase 1 says "Read `../bofu-query-generator/SKILL.md`"). This is DRY:

- Standalones can be invoked alone — user says "generate BOFU queries for Redwood City" → standalone fires
- Engines pull standalones into pipelines — user says "build content package on EPA homicide-free story" → engine fires, internally reads standalone's instructions
- One source of truth per skill — edits propagate

**Engine-internal sub-modules** (not standalone-useful) live INSIDE the engine folder:
- `content-creation-engine/references/phases/` — the 6 internal phases (source-ingestion, content-ideation-engine, funnel-tagger, script-writer)
- `content-creation-engine/modules/` — sub-modules (newsletter, market-update-narrative)

### 3. Two-Score Model (Content Architecture)

The content system has **two distinct scores** answering two distinct questions. They are NOT interchangeable and must NEVER be merged:

| Score | Owner | Scale | Answers | When applied |
|---|---|---|---|---|
| **Opportunity Score** | `content-calendar` | 25 pts (5 criteria × 5) | "Should we cover this topic THIS WEEK vs other candidates?" | Once per week, across 12-15 candidates. Top 4-5 by score → weekly calendar. |
| **Intent Score** | `bofu-intent-scorer` (standalone) | 25 pts (5 criteria × 5) + freshness ±5 | "What's the BOFU intent of this topic (DECISION / CONSIDERATION / AWARENESS)?" | Once per topic, AFTER opportunity selection. Used for funnel-mix and CTA decisions. |

Both scores are rendered side-by-side on the per-topic dashboard so the distinction stays visible. See `content-creation-engine/SKILL.md` → Scoring Architecture section for full model.

### 4. Audience-Targeted Button Pattern (Dashboards)

Per-topic dashboards have buttons targeted at specific team members:

- **Blog producer** (publishing team — posts content to platforms): gets the **Copy Content** button (gold solid). The blog producer never needs to regenerate; he posts what's already produced.
- **Peter** (video production): gets the **Copy Script Prompt** button (gold outline) and **Copy Production Prompt** button (purple). Peter regenerates as needed for his AI tools.

Non-video formats (Blog, Email, GMB, Facebook, IG Carousel) have 2 buttons (blog only). Video formats (YT Long Pt1+Pt2, YT Short, IG Reel #1, IG Reel #2, TikTok) have 3 buttons (blog + video).

Button colors carry semantic meaning:
- **Gold solid** = Blog Track's primary action (post-ready content)
- **Gold outline** = secondary regeneration / script-side prompt
- **Purple solid** = Peter's production-side prompt
- **Navy** = UI chrome (toggles, expanders, navigation)

See `content-creation-engine/references/single-topic-dashboard-rules.md` Rule 3 for full spec.

### 5. Weekly Output: HTML Calendar + Three-Tier Email

content-calendar produces TWO weekly outputs:

1. **HTML Production Calendar** (hosted on GitHub Pages) — the full multi-tab dashboard for Jason (video editor) and Peter (production). Three tabs: Analytics, Production Map, Copy Bank.

2. **Three-Tier Email for Blog Track** (sent Monday + daily) — Blog Track's quick-decision surface. Topics ranked into Top tier (Score 22-25, "must_create"), Next tier (17-21, "strong"), Third tier (12-16, "consider"). Each email link deep-links into the dashboard where the Copy buttons live (email clients strip JS — buttons can't work IN the email).

See `content-calendar/SKILL.md` → "Weekly Email Format (for the Blog Producer)" section.

### 6. YouTube Source Ingestion: Two Modes

Phase 0 of content-creation-engine has two distinct modes:

- **Mode A — Single-URL Transcription** — user pastes a video URL → `youtube_transcriber.py` runs (caption pull → Whisper fallback)
- **Mode B — Channel Monitoring** — user pastes a channel URL OR a scheduled task fires → `youtube-scraper` standalone scans for new uploads in the time window, delegates transcripts to youtube_transcriber.py for each

The orchestrator picks the right mode based on what the user provided. Don't fire Mode B for a single URL or vice versa.

---

## Data Flow Diagrams

### Weekly Planning Flow

```
[Data Sources — see integrations.md]
  ├── Windsor MCP (Instagram, Facebook, YouTube, GSC)
  ├── Apify Reddit scraper (trudax/reddit-scraper-lite)
  ├── MLSListings (Chrome)
  ├── Google Trends (Chrome)
  ├── Local news (web search) + EPA gov (Chrome)
  └── Apify competitor scrapers
        │
        ▼
   12-15 topic candidates extracted
        │
        ▼
   Opportunity Score applied (25 pts)
   • Performance Signal (5)
   • Search Demand (5)
   • Audience Intent (5)
   • Competitive Gap (5)
   • Timeliness (5)
        │
        ▼
   Top 4-5 → weekly calendar
   Tier breakdown:
   • Top tier (22-25): "must_create"
   • Next tier (17-21): "strong"
   • Third tier (12-16): "consider"
        │
        ▼
   Two outputs:
   ├── HTML Production Calendar (online-content/dashboards/weekly-calendars/{date}-production-calendar-v6.html)
   └── Blog Track's three-tier email (outputs/emails/weekly-{date}-blog.html)
        │
        ▼
   For each selected topic → handoff to content-creation-engine (per-topic flow)
```

### Per-Topic Production Flow

```
Topic arrives at content-creation-engine
(from content-calendar weekly plan OR direct user ask)
        │
        ▼
Phase 0a — Clarifier Check (only if ambiguous)
        │
        ▼
Phase 0 — Source Ingestion (only if user provided YouTube URL or channel)
   • Mode A: youtube_transcriber.py
   • Mode B: youtube-scraper → youtube_transcriber.py
        │
        ▼
Phase R — Per-Topic Research
   • Topic-matched MLS stats (MLSListings via Chrome)
   • Topic-matched GSC queries (Windsor + Direct API parallel-pull)
   • Topic-matched local news (web search + EPA gov)
   • Topic-matched social signal (Windsor)
   • Topic-matched competitor coverage (Apify)
   • Topic-matched Reddit signal (Apify Reddit scraper output)
        │
        ▼
Phase G — Generate Content (with topic-type routing)
   • Market update topics → modules/market-update-narrative/ → Phase 5
   • Listing spotlight → ../listing-remarks-writer/ + ../listing-photo-captioner/ → Phase 5
   • Price reduction → ../price-reduction-angle-generator/ (PRIVATE — no public output)
   • Education / how-to → Phase 5 directly
        │
        ▼
Phase 1 — BOFU Query Generator (standalone) — only for ideation-driven runs
        │
        ▼
Phase 2 — Content Ideation (Reddit/Apify scrape)
        │
        ▼
Phase 3 — BOFU Intent Scorer (standalone) — DECISION/CONSIDERATION/AWARENESS classification
        │
        ▼
Phase 4 — Funnel Tagger (TOFU/MOFU/BOFU mix)
        │
        ▼
Phase 5 — Script Writer
   • References: content-pillars, platform-specs, voice-and-style, seo-keywords,
     aeo-geo-requirements, lead-capture-keywords, elevenlabs-audio-tags
   • Conditional (when format = blog): schema-markup-templates,
     rss-internal-linking, youtube-embed-patterns
        │
        ▼
Outputs:
   • outputs/content-package-{ts}.md (full package — scripts, captions, etc.)
   • outputs/content-package-{ts}.ssml.txt (raw SSML for renderer)
   • online-content/dashboards/single-topic/{date}-{slug}-production.html (per-topic dashboard)
        │
        ▼
Phase A — Review & Approve (user)
        │
        ▼
Phase D — Distribute
   • Newsletter → Gmail draft (via Gmail MCP)
   • Blog → ready for CMS publish
   • Social → platform-specific posts queued
   • Video → handoff to heygen-elevenlabs-renderer:
        full_render.py → ElevenLabs (voice) → HeyGen (avatar) → MP4
```

### Transaction-Side Flow (CMA Example)

```
User uploads MLS data + property details
        │
        ▼
cma-generator
   • Reads identity.json (DRE, brokerage, contact)
   • References branding.md (colors, fonts, logo)
   • References charts.md (matplotlib styling)
        │
        ▼
Three-strategy pricing analysis
   1. Aspirational
   2. Market-Aligned
   3. Move-It
        │
        ▼
Three output formats:
   • Interactive HTML Report (Chart.js, sticky nav, animated counters)
   • Email-Safe HTML (table-based, inline styles)
   • PDF (print-optimized HTML → WeasyPrint/xhtml2pdf)
        │
        ▼
Publish to GitHub Pages
   online-content/cmas/CMA_{address}.html
        │
        ▼
Live URL: https://graehamwatts.github.io/online-content/cmas/CMA_{address}.html
```

---

## Skills Inventory

The repo has 39+ skills as of April 2026. Categorized:

### Engines (orchestrators)
- `content-creation-engine` — main content production pipeline, per-topic
- `content-calendar` — weekly planning + performance analytics (absorbed `social-media-analyzer` May 2026)

### Standalone Content Skills
- `bofu-query-generator` — 230+ localized BOFU search queries
- `bofu-intent-scorer` — Intent Score (DECISION/CONSIDERATION/AWARENESS)
- `cinematic-hooks` — pattern-interrupt video prompts
- `vaibhav-template` — talking-head Vaibhav-style aesthetic
- `video-prompt-builder` — Seedance shot lists
- `youtube-scraper` — channel monitoring (different from URL transcription)

### Transaction-Side Skills
- `cma-generator` — branded CMA reports (PDF + HTML + email)
- `offer-analyzer` — multi-offer comparison + seller net sheets
- `disclosure-analyzer` — TDS/SPQ/inspection report analysis
- `listing-remarks-writer` — MLS public remarks (walkthrough + condition-aware)
- `listing-photo-captioner` — per-photo MLS captions
- `price-reduction-angle-generator` — data-backed seller convo angle

### Video Production Skills
- `heygen-video` — single-call HeyGen avatar video
- `heygen-elevenlabs-renderer` — ElevenLabs → HeyGen pipeline (voice + avatar)
- `video-creator` — Python + ffmpeg slideshow videos
- `remotion-video` — React-based programmatic video
- `higgsfield-video` — Higgsfield AI b-roll

### Communication Skills
- `html-email` — branded HTML email generation + GitHub Pages hosting

### CRM / Operations
- `ghl-crm-audit` — GoHighLevel audit + N8N workflow building

### Document Processing
- `docx`, `pdf`, `xlsx`, `pptx` — Office document creation/editing

### Infrastructure
- `github-skill-sync` — automated repo backup
- `skill-creator` — skill scaffolding + evaluation
- `schedule` — scheduled tasks
- `consolidate-memory` — memory file maintenance
- `setup-cowork` — guided Cowork onboarding
- `context-engineer`, `copywriter` — utility/meta skills

### Off-Market / Custom
- `off-market-property-search` — off-market lead generation
- `newsletter-generator` — separate from html-email, focused on multi-section newsletters
- `website-builder` — landing page generation

For any skill not listed above, look in `skills/<name>/SKILL.md`. Each skill's SKILL.md is the canonical doc for that skill — read the frontmatter `description` field for triggering keywords.

---

## How Cowork Skills Work (Mechanics)

Cowork is the runtime. Each skill is a folder with a `SKILL.md` file containing YAML frontmatter (name + description) and Markdown body (instructions).

**Skill discovery:** Cowork scans the top-level `skills/` directory at session start. Each `SKILL.md` is registered with its description as the trigger string.

**Skill triggering:** when a user prompt arrives, Cowork's reasoning matches the prompt against every skill's description. The closest match fires — that skill's full instructions become the operating context for the response.

**Sub-skill referencing:** when a skill's instructions say "Read `../other-skill/SKILL.md`" — that's a regular file read into the current session's context. It doesn't formally invoke the other skill as a separate sub-call. The current skill's session reads the referenced file and follows those instructions inline.

**Why this matters for architecture:**
- Skills MUST live at `skills/<name>/` to be discoverable
- Sub-modules nested inside skills (e.g., `content-creation-engine/modules/newsletter/`) are NOT independently triggerable — they're reference files the parent skill reads
- For a skill to be both standalone AND part of an engine, it MUST be at top level + the engine references it via path

**Plugin manifest** (`.claude-plugin/plugin.json`) describes the skills bundle for Cowork to load.

---

## Identity & Brand Hard Rules

### identity.json Is the Single Source of Truth

`skills/shared-references/identity.json` contains:
- Graeham's name, title, brokerage, **DRE**, phone, email, website
- Primary + secondary markets
- Blocklist of values that must NEVER appear in outputs

**The DRE is `01466876`.** The blocklist contains one value (a wrong DRE that has leaked into outputs 11 times historically — see CLAUDE.md root for post-mortems).

### Hard Rules

1. **NEVER hardcode brand identity from memory or context.** Every skill that emits brand details (CMA reports, listing remarks, schema markup, signatures, footers) MUST read identity.json at generation time.

2. **NEVER type a DRE-shaped string from prior context.** If a session's reasoning sees a DRE value in its working context, do NOT type it into output. Read identity.json fresh.

3. **`scripts/verify_brand_identity.py` is the tripwire.** It scans the entire repo for blocked values and exits non-zero if found. Run before every push:
   ```bash
   python3 scripts/verify_brand_identity.py
   ```

4. **Documentation-exempt files** (CLAUDE.md root, identity.json itself, verify_brand_identity.py) MAY contain blocked values for warning/blocklist purposes. The tripwire skips them. Other files MUST NOT contain blocked values, even in warnings.

5. **Cowork's cached skill descriptions can be stale.** If you see the wrong DRE in a skill's description string in Cowork's UI, that's a cache issue, not a real leak. The fix is restarting Cowork to refresh.

### What Mehmood Needs to Do

When building features that emit brand details:
- Read identity.json at runtime — never hardcode
- Test that the tripwire passes before committing
- Don't include literal blocklist values in code comments or docs (use abstract references like "the blocklisted value documented in identity.json")

---

## Integrations

See `skills/shared-references/integrations.md` for the canonical integration matrix. Key points:

- **13 active integrations** (MLSListings, GSC, Apify Reddit, Apify Zillow, YouTube transcriber, YouTube Data API, Instagram, Facebook, EPA gov, HeyGen, ElevenLabs, GoHighLevel, GitHub)
- **3 stale / needs verification** (Apify Zillow, YouTube Direct API, GSC Direct API)
- **3 pending** (Reddit official API — applied; Santa Clara county records — not wired; San Mateo county records — not wired)
- **Windsor + Direct API parallel-pull rule** — for any source available via both, pull both in parallel, compare freshness/completeness, pick winner. Documented in integrations.md with pseudocode.

When wiring a new integration:
1. Add an entry in integrations.md
2. Update the per-skill map at the bottom of that file
3. If the integration touches identity-related fields, update verify_brand_identity.py's tripwire
4. Run verification before declaring it production-ready

---

## Pantana Reference (Category Context)

Jason Pantana ships a real-estate AI content kit (sometimes called "PropCast" — distinct from Graeham's project despite the name overlap). It's mostly content-side and template-shaped: agents download the templates, swap placeholder values for their own market, and run.

**Where Pantana overlaps PropCast:**
- BOFU query patterns (his query library inspired Graeham's bofu-query-generator)
- BOFU scoring framework (Intent Matrix concept)
- Listing remarks writer (Pantana's "nouns over pronouns" approach)
- Listing photo captioner
- Price reduction angle generator
- Blog post writer (AEO structure)
- YouTube-to-blog pipeline
- Channel scraper

**Where PropCast goes further:**
- Transaction-side stack (CMA, offer analysis, disclosure analysis) — Pantana doesn't have these
- Hyperlocal Bay Area / EPA context baked into every skill
- Branded output (CMA reports, dashboards) with Graeham's identity
- GitHub Pages publishing pipeline for client-facing URLs
- GoHighLevel CRM integration for comment-keyword lead capture
- ElevenLabs + HeyGen production pipeline (avatar voice + video)
- Two-score architecture (Opportunity vs Intent)
- Three-tier email + dashboard buttons targeted at specific team members (Blog Track vs Peter)
- Windsor MCP integration for cross-platform analytics
- Apify-driven Reddit ideation
- Three-strategy CMA pricing framework (Graeham's specific methodology)

**Why this matters for build priorities:** Pantana ships what most agents would build first (templates). PropCast's moat is the depth on the transaction side and the integration layer. Don't spend time replicating Pantana's templates — use them as references where they're already in our repo, and focus build effort on the parts Pantana doesn't have.

**Files in this repo that originated from Pantana's templates:**
- `Cotent Creation engine Jason Pantana/` (in Graeham's local Documents folder, not in repo) — the original Pantana download. Used as reference during the April 2026 audit. NOT in the skills repo.
- Pantana's BOFU Query Generator + BOFU Scorer were absorbed into our skills (reorganized + Bay Area localized). Our `bofu-query-generator/SKILL.md` and `bofu-intent-scorer/SKILL.md` are the canonical versions.
- Pantana's blog post writer additions (JSON-LD schema, RSS internal linking, YouTube embed patterns) were folded into `content-creation-engine/references/phases/script-writer/references/` rather than living as a separate blog-post-writer skill.

---

## Open Work / Known Issues

Tracked as of April 2026:

### High priority

1. **`single-topic-dashboard-builder.py` function-body refactor** — the v5 builder has the loader fixed and button-render logic updated for the new 3-button-per-video-format pattern, but the render code still runs at module-load time with empty dicts. Wrapping it inside `_render_html()` is a ~1000-line indentation refactor that needs bash + Python AST verification. Deferred from April 30 session due to bash sandbox failure. See file's NOTICE block at top.

2. **Email generator script** — `weekly-email-builder.py` doesn't exist yet. Spec for the email format is in `content-calendar/SKILL.md` (Weekly Email Format section). Builder script should produce `outputs/emails/weekly-{date}-blog.html` and `daily-{date}-blog.html` from the weekly calendar JSON.

3. **County records integrations** — Santa Clara + San Mateo. Spec in integrations.md. Build a `county-records-scraper` standalone skill that takes county + APN as input, returns parcel JSON.

### Medium priority

4. **Verify Apify Zillow scraper** — flagged stale in integrations.md. Run a test scrape on a known address before relying on it for time-sensitive output.

5. **Verify YouTube Data API + GSC Direct API OAuth flows** — both flagged stale. Confirm token refresh handling.

6. **Reddit official API follow-up** — see Cloud Chrome prompt in integrations.md. When approved, document the new connector and update content-ideation-engine to parallel-pull with Apify scraper.

7. **Tripwire extension to `online-content` repo** — currently `verify_brand_identity.py` only audits the skills repo. The April 29 leak was IN the published-content repo (then `cma-reports`, now `online-content`). Either copy the script to `online-content` OR extend this script to clone-and-audit `online-content` as part of its run.

### Low priority / future

8. **Google Trends MCP** — currently uses generic web search via Chrome. If a reliable Trends MCP appears, switch.

9. **Skill-calls-skill via Skill tool** — currently engines reference standalones via `Read` (sibling-path file read). Could migrate to formal `Skill` tool invocation for better separation. Not urgent.

10. **Content-creation-engine Phase 5 reference file split** — `instructions.md` is large. Could be split into smaller per-format files.

---

## Build Priorities

If you're starting fresh and asking "what should I work on?", priority order:

### Week 1: Verify what exists
1. Read this entire doc + identity.json + integrations.md
2. Pull the repo via GitHub Desktop
3. Run `python3 scripts/verify_brand_identity.py` (it should pass — confirm)
4. Open `skills/content-creation-engine/SKILL.md` end-to-end
5. Open `skills/content-calendar/SKILL.md` end-to-end
6. Try a real run: in Cowork, ask "build me a content package on AB 1482 for Bay Area landlords" and trace which skills fire and in what order

### Week 2: Knock out the high-priority open work
1. Finish the single-topic-dashboard-builder.py function-body refactor (item #1 in Open Work)
2. Build weekly-email-builder.py (item #2)
3. Wire county records (item #3)

### Week 3+: Verify integrations + extend
1. Test stale integrations (Apify Zillow, Direct APIs)
2. Follow up on Reddit API (use the Cloud Chrome prompt in integrations.md)
3. Extend tripwire to `online-content` (item #7)

### Ongoing: Productize
- Once Graeham's specific build is solid, evaluate productizing for other agents (the PropCast SaaS direction). That's a separate project — multi-tenant identity.json, tenant-isolated dashboards, billing, etc.

---

## How to Develop on This Repo

### Local Setup

1. Install GitHub Desktop (Mac or Windows)
2. Clone `Graehamwatts/skills` via GitHub Desktop
3. Local path: `~/Documents/GitHub/skills` (Mac) or `C:\Users\{user}\Documents\GitHub\skills` (Windows)
4. Verify: `cd skills && ls` should show README.md, CLAUDE.md, skills/, scripts/, etc.

### Editing Workflow

1. Open the repo in your editor of choice (VS Code recommended)
2. Edit any SKILL.md or reference file
3. Run `python3 scripts/verify_brand_identity.py` to check for DRE leaks
4. Commit via GitHub Desktop with a descriptive message
5. Push via GitHub Desktop
6. Cowork will pick up the updated skills on the next session (may need to restart Cowork to force refresh)

### Testing a Skill

Without bash access (which is the case in standard Cowork sessions):
- Read the SKILL.md end-to-end
- Trace what files/scripts it references
- Read those references
- Look for hardcoded paths that point to dead sandbox sessions (e.g., `/sessions/something/mnt/...`) — those are stale and need fixing

With bash access:
- `python3 scripts/verify_brand_identity.py` — tripwire check
- `python3 -c "import ast; ast.parse(open('skills/some-skill/script.py').read())"` — syntax check on Python skill scripts

### Common Pitfalls

1. **Editing the local Cowork plugin folder** — those edits don't persist. Always edit the GitHub Desktop clone.
2. **Hardcoding DRE in code or docs** — read from identity.json at runtime. Tripwire will catch you.
3. **Deleting skills without updating cross-references** — use the Grep tool to find every reference before deletion.
4. **Pushing without running the tripwire** — eventual leak. Run it.
5. **Mistaking Cowork's cached descriptions for current state** — if something's "wrong" in Cowork but right on GitHub, restart Cowork.

### Naming Conventions

- Skill folder names: `kebab-case` (e.g., `bofu-query-generator`)
- Reference files: `kebab-case.md` (e.g., `voice-and-style.md`)
- Output files: `{slug}-{date or ts}.{ext}` (e.g., `content-package-2026-04-30.md`)
- GitHub Pages dashboards: `YYYY-MM-DD-{slug}-production.html`
- Commit messages: descriptive imperative (e.g., "Add market-update-narrative module to content-creation-engine")

### When in Doubt

1. Check `CLAUDE.md` (root) — it has the high-level rules
2. Check `skills/shared-references/identity.json` — for any brand identity question
3. Check `skills/shared-references/integrations.md` — for any external data source question
4. Check `skills/shared-references/data-contracts.md` — for cross-skill JSON contracts
5. Read the SKILL.md of the skill you're working on
6. Ask Graeham — he has the most context on intent

---

## Last Updated

April 30, 2026 — Phase 7 deliverable of the Pantana audit + repo restructure.

Future updates: when integrations are verified, when stale items are resolved, when build priorities shift, or quarterly