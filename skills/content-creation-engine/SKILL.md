---
name: content-creation-engine
description: "Bay Area / East Palo Alto real estate content creation engine for Graeham Watts (REALTOR, Intero Real Estate, DRE# 01466876). Use this skill ANY time the user mentions: content creation engine, create content, newsletter content, blog post, ad copy, social media content, video script, content ideas, YouTube, Reels, Shorts, TikTok, AI avatar script, listing video, market update video, BOFU content, TOFU content, MOFU content, Bay Area real estate content, East Palo Alto content, Redwood City content, Palo Alto content, Menlo Park content, San Mateo County content, Reddit ideation, content scoring, content pillars, AB 1482, relocation content, first-time-buyer content, seller content, find me topics, content intelligence, I need content, market research, topic discovery, or anything related to generating inbound real-estate content for Graeham's markets. Also trigger when the user uploads MLS data or a new listing and wants a content package, or pastes a YouTube URL and wants content ideas from it."
---

# Content Creation Engine

> **Updated on 2026-06-07 (Meta Ads direct connection):** Meta launched official Ads AI Connectors (open beta, 2026-04-29). A new standalone skill `meta-ads` now OWNS all paid Meta work — reporting, campaign creation, budgets, pixel/CAPI diagnostics — via the official MCP at `mcp.facebook.com/ads`. This skill's role is unchanged: it CREATES ad copy variants, but deployment hands off to `meta-ads`. Data-source split: direct MCP = paid signal; Windsor = organic IG/FB, GSC, YouTube (the official Ads MCP has zero organic tools, so Windsor is NOT redundant for this engine). See the Data Source Status section and `references/research-sources.md` section 5a.

> **Absorbed on 2026-05-13 (Merge 3):** `video-research-engine` was merged into this skill. Its content now lives at `references/phases/video-research.md` and its Python scripts at `scripts/video-research/`. The folder `skills/video-research-engine/` was deleted in the same commit. The original v-r-e trigger phrases ("transcribe YouTube video", "analyze this video", "frame by frame", "B-roll breakdown", "deep dive on this video") are already part of this skill's top-level description.

> **Re-extracted on 2026-05-15:** the video-research scripts (download/frames/transcribe/analyze/library/dataforseo_direct) have been LIFTED OUT of this skill into a new standalone skill `video-watcher`. The copies inside `scripts/video-research/` are now deprecated — they remain for backward compatibility but new invocations should call `video-watcher` directly. Reason: the visual-analysis capability was effectively dormant inside this skill because (1) most users didn't know it existed, (2) trigger keywords didn't match how Peter/Ellie/Adrian actually speak, (3) the visual analysis was coupled to content generation when it should be a standalone tool. The new `video-watcher` skill fires on "watch this video," "make ours like this," "shot list," "blueprint," "full breakdown" — keywords that map naturally to the video-editor workflow. When this skill needs visual analysis as part of Phase 0 source ingestion (Mode B-style visual pass), it should call `video-watcher` as an external skill rather than running the embedded code. Companion to the also-extracted `video-transcriber` (audio→text) which was extracted on the same day.

> **Absorbed on 2026-05-13 (Merge 2):** `bofu-query-generator` and `bofu-intent-scorer` were merged into this skill. Their content now lives at `references/phases/bofu-query-generator.md` (Phase 1) and `references/phases/bofu-intent-scorer.md` (Phase 3). The folders `skills/bofu-query-generator/` and `skills/bofu-intent-scorer/` were deleted in the same commit. If you find any reference to those folder paths anywhere in this repo, that reference is a bug — point it at the new phase reference files instead.

> **NOTE (April 2026):** This skill absorbed `video-script-creation-engine`. That skill no longer exists as a separate folder — all its capabilities (script writing, SSML generation, shot lists, editing notes, AI video prompts, SEO packages, platform cross-posting, voice+production pairing) now live here. All skills that previously referenced `video-script-creation-engine` (heygen-video, heygen-elevenlabs-renderer, content-calendar) have been updated to point here instead.



Modular real estate content generation system for Graeham Watts. Turns a single topic into a funnel-tagged, multi-platform content package grounded in live Bay Area buyer and seller data.

**This skill is PER-TOPIC.** Given ONE topic (from `content-calendar`'s weekly plan or a direct user ask), it pulls topic-matched research, classifies BOFU intent, and produces the full content package (scripts, SSML, editing notes, AI video prompts, SEO, and HeyGen render hand-off). **Weekly planning and opportunity scoring live in `content-calendar`, not here.** See the Scoring Architecture section below for the clean handoff between weekly (Opportunity Score) and per-topic (Intent Score).


## Scope Boundary (Who Owns What)

> **Updated April 2026 to resolve overlap with `content-calendar`.**

This skill is the **PER-TOPIC PRODUCTION** layer. Given a single topic (from `content-calendar`'s weekly plan OR from a direct user ask like "build me a content package on the EPA homicide-free story"), this skill generates the full content package — 14 formats with pre-generated content and companion prompts, research data panel, shot list, SSML, editing notes, AI video prompts, SEO package, alt hooks, and HeyGen render hand-off.

**WEEKLY PLANNING** (deciding WHICH topics to cover across a 5-day week, what funnel mix, scoring across candidates) is owned by `content-calendar`, not this skill.

Phase R in this skill pulls research SPECIFIC TO ONE TOPIC (the stats, news, quotes that back this one content package). The WEEKLY research that feeds multi-topic scoring lives in `content-calendar`.

| Request type | Which skill | Why |
|-------------|-------------|-----|
| "What should I post this week?" | `content-calendar` | Weekly scope, multi-topic scoring |
| "Plan next week's 5 topics" | `content-calendar` | Weekly scope |
| "Build a content package for [specific topic]" | `content-creation-engine` (this skill) | Per-topic scope |
| "I have a new listing, give me content for it" | `content-creation-engine` (this skill) | Per-topic scope |
| "Research and write content on [breaking news]" | `content-creation-engine` (this skill) | Per-topic scope, includes Phase R research |
| "Swap Monday's topic for [new topic]" | Both: `content-calendar` to update weekly plan, then `content-creation-engine` to produce the package | Chained |

## Scoring Architecture — Single Source of Truth

> **Updated April 2026. Resolves prior conflict where four separate scoring systems were competing silently.**

The content system has **two distinct scores** that answer two distinct questions. They are NOT interchangeable and they must NEVER be merged.

| Score | Owner | Scale | Answers | When applied |
|---|---|---|---|---|
| **Opportunity Score** | `content-calendar` skill | 25 pts (5 criteria × 5 pts): Performance Signal, Search Demand, Audience Intent, Competitive Gap, Timeliness | "Should we cover this topic THIS WEEK vs other candidates?" | Once per week, across 12-15 candidates. Top 4-5 by score make the weekly calendar. |
| **Intent Score** | This skill's Phase 3 (BOFU Intent Scorer) | 25 pts (5 criteria × 5 pts) + freshness adjustment (±5): Inquiry Type, Intent Matrix, Source Confirmation, Emotional Temp, Local Relevance, Freshness | "What's the BOFU intent of this topic (DECISION / CONSIDERATION / AWARENESS)?" | Once per topic, AFTER opportunity selection. Used to tag funnel position and adjust CTA. |

**What the other "scoring" references in this stack actually are:**

| Previously called | Actually is | Lives in |
|---|---|---|
| Phase R scoring (10-pt, 4 criteria) — DELETED | Per-topic research — no scoring | Phase R below (rewritten) |
| Phase 2 "4-axis scoring" | Reddit signal filtering (what to surface from scrape) | Phase 2 content-ideation-engine |

**Rule of thumb:** If a topic is on the weekly calendar, content-calendar already scored it (Opportunity). When you build its content package here, Phase 3 scores it again for a DIFFERENT reason (Intent). Both scores appear in the Scoring Architecture panel on the single-topic dashboard — see `references/single-topic-dashboard-rules.md` for the rendering spec.

## Before You Start — Read These

1. **`CLAUDE.md`** (bundled with this skill) — full orchestrator / project instructions. Read this first for the complete workflow, Fair Housing compliance section, lead capture keyword matrix, and data source strategy.
2. **`references/market-config.md`** — Graeham's agent identity, primary/secondary markets, CRM config, lead magnets, content pillars, jurisdiction-specific process terms. This grounds every piece of generated content in Graeham's real market context.
3. **`references/research-sources.md`** — Complete documentation of every data source used in Phase R (Research & Discover), including what to pull, how to pull it, what to look for, and the scoring rubric.
4. **`references/single-topic-dashboard-rules.md`** — 12 strict rules + 16-item self-check for building single-topic production dashboards. Reference implementation: `online-content/dashboards/single-topic/2026-04-18-epa-two-years-homicide-free-production.html`. Template builder: `templates/single-topic-dashboard-builder.py`.
5. **Shared Branding** — Before generating any client-facing output, read the shared branding reference at `../shared-references/branding.md` for consistent colors, fonts, and UI components.
6. **Persuasion layer — `../marketing-psychology/SKILL.md`** — Whenever a phase produces persuasive copy (Phase G scripts, hooks, ad copy, captions, CTAs, email snippets, avatar scripts), load the `marketing-psychology` skill and run its process scaled to the job: full five steps (diagnose reader → structure → lever → panel check → failure audit) for scripts and long-form; the quick path (diagnose, one lever, one panel mind, audit) for hooks, titles, and captions. Its Step 1 diagnosis (awareness stage, blocking force) should inform the funnel-stage framing — BOFU topics are usually product/most-aware readers blocked by trust or inertia; TOFU is unaware/problem-aware. Graeham's voice, market config, and Fair Housing guardrails always override lever suggestions. Skip it for non-persuasive output (research JSON, dashboards, data tables).

## Agent Identity

You are generating content as Graeham Watts — REALTOR at Intero Real Estate, DRE# 01466876. Primary market is East Palo Alto. Secondary markets are Redwood City, Palo Alto, Menlo Park, San Mateo County, and the Peninsula. CRM is GoHighLevel with comment-keyword lead capture configured for SELL, BUY, COSTS, OPTIONS, and 1482 triggers.

## Production Rules (Non-Negotiable)

These rules exist because ignoring them caused real bugs in production on April 18, 2026. Every one has a specific failure mode attached. Follow them every time.

### Rule 1: HTML Generation Safety — Use Python, Not Bash Heredoc

NEVER use `cat > file << 'EOF'` bash heredoc to write HTML files. Bash silently escapes `\!` characters in HTML comments to `\\!`, which breaks comment parsing and leaks raw visible text onto the rendered page.

ALWAYS write HTML via Python `Path.write_text()`:

```python
from pathlib import Path
Path("online-content/dashboards/single-topic/my-dashboard.html").write_text(html_content, encoding="utf-8")
```

After writing, VERIFY with: `grep -c '<\\\!--' file.html` — must return 0. Reject and rewrite if non-zero.

**Failure mode this prevents:** April 18, 2026 dashboard had 20+ visible escaped comment strings rendered as text on the page.

### Rule 2: Mandatory Screenshot-Loop After HTML Output

After writing any HTML to `online-content/dashboards/` (either `weekly-calendars/` or `single-topic/`) or `online-content/newsletters/`, read `skills/website-builder/references/screenshot-loop.md` and execute it BEFORE `git push`. Minimum 1 iteration, target 3.

Sandbox Chromium install often fails. Fallback: push to GitHub Pages first, then use Claude-in-Chrome MCP to navigate to the live URL and screenshot. If bugs found, fix locally, push again, re-verify.

**Failure mode this prevents:** Shipping broken HTML because nobody looked at the rendered page. Code review catches structure; screenshots catch vibe, color, hierarchy, and rendering bugs.

### Rule 3: PROMPT_LIBRARY Default for Multi-Format Dashboards

For any multi-format deliverable dashboard (single-topic OR weekly), use the `window.PROMPT_LIBRARY` JS object pattern with a Copy button per format. Each prompt includes Agent Identity + Fair Housing + DATE/YEAR QC + Timing Self-Check + Voice + Topic + AEO stats + Key Facts + GHL CTA + **Humanizer Block (see Rule 8)** + format-specific deliverable spec.

NEVER pre-generate full script/caption/blog content inline in the dashboard HTML. Reasons:
- Risks truncation on long outputs
- Burns context on content external AIs generate better
- Makes the dashboard hard to iterate on

Reference: `online-content/dashboards/weekly-calendars/2026-04-27-production-calendar-v7.html`.

**Failure mode this prevents:** April 18, 2026 first attempt generated 10 inline scripts consuming 100K+ chars and still risking truncation.

### Rule 4: Timing Self-Check in Every Script Prompt

Every script-generation prompt MUST include this block (same enforcement as DATE/YEAR QC):

```
TIMING SELF-CHECK (FOR SCRIPT OUTPUTS ONLY):
Before emitting any script, calculate: (spoken_word_count / 150 WPM) * 1.15 = target_minutes.
Show the math in the output. NEVER default to generic durations like "8-10 min".
```

**Failure mode this prevents:** April 18, 2026 initial estimate of "8-10 min" for a 573-word script that was actually 4:30.

### Rule 5: Single-Topic Dashboard Output Format

Single-topic content packages go to:

```
online-content/dashboards/single-topic/YYYY-MM-DD-{slug}-production.html
```

NOT a markdown file. HTML goes to GitHub Pages for the live URL the production team uses. Same design language as weekly calendars (navy/gold palette, DM Sans + Plus Jakarta Sans, same component classes).

**Failure mode this prevents:** April 18, 2026 first output was a markdown file that wasn't accessible to the production team via a live URL.

### Rule 6: Gold Is A Brand Color — Use Sparingly

`--gold` (#C5A258) is Graeham's real estate brand color. Reserve for brand moments only. Maximum ~10 instances per dashboard.

**Gold is for:** Primary action buttons (Copy Prompt, primary CTA), Opportunity Score values and score badges, PICKED / SELECTED tags, small hero accents, CTA section headings.

**Gold is NOT for:** General UI borders (use `--navy`), callout boxes (use `--teal` for tips, `--orange` for warnings), table headers, shot number circles, hover states on general UI.

**Failure mode this prevents:** April 18, 2026 dashboard applied gold to general UI chrome (timing card, intelligence stack borders, flow card states, use-in callouts, hook cards) — diluting brand impact.

---


## Self-Check Before Shipping

Before declaring any content-creation task complete, run this checklist explicitly in your response before pushing:

1. [ ] Timing calculation shown with math (word_count / 150 * 1.15 = minutes)
2. [ ] Fair Housing check passed (no demographic code words, no school rankings)
3. [ ] DATE/YEAR QC applied (2026 everywhere, historical refs explicitly labeled)
4. [ ] AEO statements open with date anchor ("As of April 2026...")
5. [ ] GHL keyword is valid (in the keyword matrix)
6. [ ] HTML output: `grep -c '<\\\!--'` returns 0 (no escape bug)
7. [ ] HTML output: screenshot-loop executed, visual verified
8. [ ] HTML output: PROMPT_LIBRARY used (not inline pre-generated content)
9. [ ] HTML output: gold usage is brand-only (Rule 6)
10. [ ] Source citations included with clickable links
11. [ ] Single-topic output: saved to `online-content/dashboards/single-topic/` as HTML
12. [ ] HTML pushed to GH Pages
13. [ ] **Humanizer pass run on all written prose deliverables** (see Rule 7 below)
14. [ ] **Weekly calendar uses single-file canonical pattern** — no -all/-blogs/-videos/-research variants created (Rule 11)
15. [ ] **All visual dashboard sections present** — Hero, Audience nav, Run note, Research/Live Data Layer, Performance Signal (with charts), Freshness, Pipeline Diagram, Calendar grid, Video Content, Blog Content (Rule 10)
16. [ ] **Orphan-href audit passed** — `grep -oE 'href="[^"]*\.html"'` shows zero relative-html-file links to files not in the same commit (Rule 9)
17. [ ] **COPY_DATA Humanizer Block injection verified** — JSON parses cleanly, 15 prose entries contain "HUMANIZER RULES" string, 5 ssml entries do NOT contain it (Rule 8)

---

### Rule 7: Humanizer Pass on All Written Prose (Non-Negotiable)

Every written deliverable produced by Phase G — scripts, blog posts, ad copy, social captions, newsletter sections, CTAs, AEO statements — must be run through the `humanizer` skill before it goes to Adrian, Peter, or Graeham for review. Spoken scripts especially: an em-dash-heavy "stands as a testament" sentence is invisible on paper but sounds like a robot when Graeham reads it on camera, and the engagement drops.

**Apply humanizer to:**
- Long-form YouTube scripts (Pt 1 script body)
- Short-form scripts (YT Shorts, IG Reels, TikTok)
- Blog post body copy
- Social captions (IG, FB, LinkedIn, GMB)
- Newsletter section prose
- Ad copy variants (FB, Google)
- AEO cite-ready statements (the prose around the stat, not the stat itself)
- Alt hook variants

**Do NOT apply humanizer to:**
- The SSML / ElevenLabs audio-tag blocks (those are markup, humanizer would break them)
- Shot list bullets and inline shot direction tags (`[TALKING HEAD]`, `[B-ROLL: ...]` — these are production metadata)
- Editing Notes for Jason (production directions, not reader-facing prose)
- JSON-LD schema markup
- YouTube SEO metadata fields (title, description tags, keyword lists)
- GHL keyword strings (`SELL`, `BUY`, etc.)
- Raw research data JSON

**How to invoke during Phase G:**
1. Generate the draft script / post / caption as usual through the existing phase pipeline.
2. Separate the reader-facing prose from the production metadata (SSML, shot lists, editing notes).
3. Pass the reader-facing prose to the humanizer skill with Graeham's voice as the calibration sample (first-person, conversational, specific numbers over abstract claims, zero hype, no em-dash overuse).
4. Replace the original prose with the humanized version.
5. Re-stitch with the unchanged production metadata.
6. Continue to the rest of the Self-Check.

**Failure mode this prevents:** Scripts that read like ChatGPT wrote them get flagged by viewers in seconds. YouTube comments call it out. Engagement metrics drop. This rule existed informally — making it explicit ensures every generated package gets the pass before going to the production team.

---

### Rule 8: Humanizer Block in Every PROMPT_LIBRARY Entry (Non-Negotiable)

Rule 7 covers the case where this skill generates content directly and runs the `humanizer` skill as a post-pass. But the PROMPT_LIBRARY pattern (Rule 3) hands the actual generation to an external AI tool — Adrian, Peter, or Graeham copy a prompt and paste it into ChatGPT, Claude.ai, Gemini, or wherever. They cannot run the humanizer skill at that point. The fix: embed the humanizer rules INSIDE each prompt so the external AI generates already-clean output from the start.

**Every PROMPT_LIBRARY entry that produces written prose (scripts, blogs, captions, ad copy, newsletter sections, AEO statements) must include the Humanizer Block below as a standard preamble item, placed AFTER Voice & Style and BEFORE the format-specific deliverable spec.**

#### Canonical Humanizer Block

**Read `references/humanizer-block.md`** for the verbatim block text, the placement order in the prompt preamble, and the prompt-data structure notes. Copy the block exactly as written there into every prose-generating PROMPT_LIBRARY entry, placed after Voice & Style and before the format-specific deliverable spec.

#### When to Skip the Humanizer Block

Omit ONLY in prompts that don't generate reader-facing prose:
- SSML / audio-tag generation prompts (markup output, humanizer rules would conflict)
- Shot list generation prompts (production metadata)
- Editing Notes prompts (production directions)
- JSON-LD schema generation prompts
- YouTube metadata field prompts (titles, tags, keywords — these have their own length and format rules)
- Image generation prompts (visual, not prose)

All other prompts — long-form scripts, short-form scripts, blog posts, ad copy, captions, newsletter sections, AEO statements, alt hooks — MUST include the block verbatim.

#### Maintenance

The canonical block, its placement order, and the prompt-data structure are documented in `references/humanizer-block.md` — that file is the single source of truth. When the `humanizer` skill at `skills/humanizer/SKILL.md` is updated with new patterns (new AI-tells observed in the wild), update the reference file in the same commit so PROMPT_LIBRARY entries stay in sync.

**Failure mode this prevents:** Rule 7 (post-gen humanizer skill pass) only works when this skill generates content directly. When Adrian/Peter copy a prompt and paste into an external AI tool, Rule 7 doesn't fire — and the resulting script or blog reads like ChatGPT wrote it. Rule 8 closes that gap by moving the humanizer rules upstream into the prompt itself, so the external AI never produces the bad output in the first place.

---

### Rules 9-11: Weekly Calendar Dashboard Rules (Non-Negotiable)

**Read `references/weekly-dashboard-rules.md`** before building or editing a weekly calendar HTML dashboard. It covers: Rule 9 (no orphan internal links — every href must resolve, with a mandatory pre-push audit), Rule 10 (the 10 required visual dashboard sections in fixed order, including the ApexCharts-brushable-only requirement for Performance Signal charts), and Rule 11 (single canonical file per week — the old 4-file `-all`/`-blogs`/`-videos`/`-research` pattern is forbidden). Not needed for single-topic dashboards (see `references/single-topic-dashboard-rules.md` instead) or for ideation/scoring/research phases.

---

## Fair Housing Guardrails (Non-Negotiable)

NEVER generate content that:
- Describes neighborhoods by demographics (race, religion, national origin, family status, disability)
- Uses "safe / good areas / family-friendly / up-and-coming" as a proxy for demographic signaling
- Ranks or rates schools as a primary selling point for a neighborhood
- Promotes kickback arrangements with lenders, inspectors, or other vendors

Neighborhood content is limited to: property features, price ranges, market trends, lot sizes, amenities, architecture, housing stock age, HOA structure, zoning, new development, commute/transit facts, and walkability. When in doubt, reframe or drop the topic. This is both the law and Graeham's brand standard.

---

## THE PER-TOPIC WORKFLOW (Phase R is PER-TOPIC, not weekly)

> **Rewritten April 2026.** Previous version of Phase R pulled 8 weekly-scope sources and applied a 10-pt scoring rubric — that's weekly-planning work and it belongs in `content-calendar`. This skill's Phase R now does one job: gather citations, stats, and quotes for ONE topic that's already been selected.

When a topic arrives here (from `content-calendar`'s weekly plan, or a direct ask like "build a package on X"), Phase R pulls the *research data panel* that backs the single-topic dashboard. When the request is "what should I post this week?" — **hand it to `content-calendar`, not Phase R.**

### Phase 0a — Clarifier Check (ASK BEFORE RESEARCHING)

Before pulling any data, confirm the scope in ONE question. Don't skip this step — it prevents a full Phase R run for a request that actually wanted weekly planning, or vice versa.

If the user's ask is ambiguous, confirm in this form:

> "Before I start — which of these are you asking for?
> (a) **Per-topic content package** — you already know the topic (e.g., 'EPA homicide-free story', 'this new $2.1M listing', 'AB 1482 explainer'). I'll pull research for THAT topic and build the full dashboard.
> (b) **Weekly planning** — you want me to decide which topics to cover this week. For that I should hand off to `content-calendar`.
> (c) **Raw research only** — you want current market signal dumped to the chat, no package built yet."

If the ask is unambiguous (user provided a specific topic, a listing, a YouTube URL, or breaking news), skip Phase 0a and proceed to Phase R.

### Phase R — Per-Topic Research (citations & stats for ONE topic)

**Read:** `references/research-sources.md` for source documentation.

Given ONE already-selected topic, pull the evidence that will populate the dashboard's "Show Full Research Data" panel — statistics, quotes, news clippings, permits, MLS comps, GSC queries that match this topic. **No scoring happens here.** The Opportunity Score is already done (content-calendar set it when the topic was selected). The Intent Score runs in Phase 3.

#### What to pull (scoped to the ONE topic)

1. **Topic-matched MLS stats** — only the price bands / DOM / inventory numbers that back this topic. If the topic is "EPA homes under $700K," pull that bucket. Do NOT pull the full county stat sheet.
2. **Topic-matched GSC queries** — the specific queries from Search Console that this topic targets. Note impressions, position, and whether it's a rising query.
3. **Topic-matched local news/permits** — web search AND city gov search for this topic's exact subject (e.g., "East Palo Alto homicide rate 2026," "AB 1482 2026 amendments").
4. **Topic-matched social performance** — did similar topics perform well in the last 60 days on Graeham's channels? (This feeds the dashboard's "format recommendation" based on what worked for similar content.)
5. **Topic-matched competitor content** — have competitors covered this exact angle in the last 30 days? Use Apify datasets if fresh, Claude-in-Chrome for manual check otherwise.
6. **Topic-matched Reddit/audience signal** — pull relevant snippets from the most recent `outputs/ideation-topics-*.json` that match this topic's keywords.

Do NOT pull the broad weekly trend data Phase R previously pulled. That lives in content-calendar now.

#### Output — Research Data Panel (JSON)

Save research as `outputs/research-{topic-slug}-{timestamp}.json` with this shape:

```json
{
  "topic_slug": "epa-homicide-free-story",
  "topic_title": "East Palo Alto Two Years Homicide-Free — What It Means For Home Values",
  "pulled_at": "2026-04-22T18:00:00Z",
  "mls_stats": [ { "metric": "...", "value": "...", "as_of": "..." } ],
  "gsc_queries": [ { "query": "...", "impressions": 0, "position": 0.0, "rising": true } ],
  "news_and_permits": [ { "source": "...", "headline": "...", "url": "...", "date": "..." } ],
  "social_signal": { "similar_topic_avg_reach": 0, "best_format": "IG Reel 30s", "sample_size": 4 },
  "competitor_coverage": [ { "competitor": "...", "covered_angle": "...", "views": 0 } ],
  "reddit_signal": [ { "thread_title": "...", "url": "...", "upvotes": 0 } ]
}
```

This JSON is the single source of truth for the "Show Full Research Data" accordion on the single-topic dashboard.

### If Graeham asks the ambiguous questions — routing table

| User says | Runs where |
|---|---|
| "What should I post this week?" | **`content-calendar`** (weekly planning + Opportunity scoring). NOT Phase R. |
| "Plan next week's 5 topics" | **`content-calendar`** |
| "Run research" / "What's happening in EPA?" | Phase 0a clarifier → usually content-calendar weekly research, unless user specifies one topic |
| "Build a content package for [specific topic]" | Phase R here, per-topic |
| "I have a new listing, give me content" | Phase R here, per-topic (the listing IS the topic) |
| "Transcribe this YouTube video and build content from it" | Phase 0 (ingestion) → Phase R here, per-topic |

---

### Phase S — Select & Plan

User picks 2-3 topics from the Content Opportunity Report. Engine confirms:
- Which formats to generate for each topic (video script, newsletter section, blog post, ad copy, social posts)
- Which platforms each format targets
- Funnel tier assignment (TOFU / MOFU / BOFU) for each topic
- Any dependencies (e.g., "this topic needs MLS data screenshots for the carousel")

Confirm the plan with Graeham before proceeding to generation.

---

### Phase G — Generate Content

#### Pre-Generation Topic-Type Routing

Before generating any formats, check the topic type and route through the appropriate module:

| Topic type | Route through | Then |
|---|---|---|
| Market update / monthly report / weekly market read / "is now a good time to buy/sell" | `modules/market-update-narrative/README.md` — **READ the ⚠️ Freshness Gate section FIRST** before touching any data. If the data period hasn't changed since the last recap, the module routes to Deep-Dive mode (not Recap). Check `references/topic-history.json` → `upcoming_deep_dives` for the pre-queued angle. | Module returns a narrative outline JSON; pass to Phase 5 script-writer for final format rendering. After any Recap, write the `deep_dive_queue` to `topic-history.json` `upcoming_deep_dives`. |
| Listing spotlight (specific property) | `../listing-remarks-writer/SKILL.md` for the source-of-truth listing description; `../listing-photo-captioner/SKILL.md` for carousel/photo captions | Phase 5 builds derivatives from those outputs |
| Stale listing / price reduction angle | `../price-reduction-angle-generator/SKILL.md` (PRIVATE — seller-only, never public content) | Output is for agent's seller convo, NOT for public posting. Do not generate downstream public formats. |
| Education / how-to / process / decision frameworks | No pre-module — go directly to Phase 5 | Phase 5 handles standard content generation |
| YouTube source-driven repurposing | Phase 0 source-ingestion (`scripts/youtube_transcriber.py`) or `../youtube-scraper/SKILL.md` for channel monitoring | Returns transcript + metadata; Phase 5 builds derivatives |

If the topic doesn't match any of the above, default to "education" routing and let Phase 5 handle it directly.

#### Format Generation

For each selected topic, produce ALL relevant formats using the existing phase pipeline:

1. **Video Script** — Long-form + short-form with clear section headers (see Script Output Format below). Includes ElevenLabs SSML block, inline shot directions, editing notes for Jason, and AI video prompts.
2. **Newsletter Section** — HTML formatted per the newsletter module. See `modules/newsletter/` and `../newsletter-generator/SKILL.md`.
3. **Blog Post Draft** — SEO-optimized with AEO cite-ready statements, meta description, title tag, target keywords, JSON-LD schema markup (Article + FAQPage + VideoObject as applicable), RSS-feed-based internal linking to existing graehamwatts.com posts, YouTube embed + timestamp link patterns when source video exists.
4. **Ad Copy Variants** — If the topic lends itself to paid promotion: Facebook ad copy, Google ad copy, with multiple hook variants for A/B testing. **Deployment is NOT this skill's job:** when Graeham approves Facebook/Instagram ad copy for actual spend, hand off to the `meta-ads` skill — it owns Special Ad Category (HOUSING) compliance, the budget confirmation gate, and launch via the official Meta MCP.
5. **Social Posts** — Platform-specific: IG caption with hashtags and GHL keyword CTA, Facebook post, LinkedIn post (if applicable), Google My Business post.

The generation phase uses the existing 6-phase pipeline (Phase 0 through Phase 5) documented below for the actual content creation logic. Phase R replaces the "what should I write about?" question — by the time we reach Phase G, we already know exactly what topics to cover and why.

---

### Phase A — Review & Approve

Present all generated content to Graeham (and Adrian if applicable) for approval. For each piece:
- Show the content with its section headers
- Note the source data that inspired it (from Phase R)
- Flag any items that need fact-checking or data verification
- Ask for approval, revision requests, or rejection

---

### Phase D — Distribute

Once approved:
- **Newsletter:** Assemble full newsletter from selected sections, draft in Gmail via Gmail MCP
- **Blog:** Ready-to-publish format with SEO metadata
- **Social:** Platform-specific posts queued for posting
- **Ads:** Ready for deployment with targeting recommendations
- **Video:** Hand off to heygen-elevenlabs-renderer for avatar video rendering (see Auto-Render Hand-off section below)

---

## THE CONTENT GENERATION PIPELINE (Used by Phase G)

The phases below contain the detailed content creation logic. During the per-topic workflow, these are invoked during Phase G (Generate Content) after a topic has been selected. They can also be invoked directly when Graeham already knows exactly what topic he wants to cover and skips research.

Each phase has its own detailed instruction file in `references/phases/`. Read the phase file before executing that phase.

### Phase 0 — Source Ingestion (YouTube)

**Read:** `references/phases/source-ingestion/instructions.md`

Phase 0 has TWO modes. The orchestrator picks the right one based on what the user provided.

#### Mode A — Single-URL Transcription

**When to use:** the user pasted a specific YouTube video URL ("here's a video, give me content ideas from it" / "transcribe this and adapt it for EPA sellers").

**How it works:** Two-tier transcription system — tries free caption pull first (instant), falls back to OpenAI Whisper (free, local, ~1-3 min) for videos without captions. Run `scripts/youtube_transcriber.py` for the transcription.

**Output:** `outputs/transcripts/transcript-{video_id}-{timestamp}.txt` + Source Ingestion Brief.

**Triggers:**
- User pastes a YouTube watch URL (`youtube.com/watch?v=...` or `youtu.be/...`)
- User pastes a Shorts URL (`youtube.com/shorts/...`)
- User says "transcribe this video," "give me content from this video," "adapt this video"

#### Mode B — Channel Monitoring (Repurposing Pipeline)

**When to use:** the user wants to monitor a YouTube channel for new uploads and auto-repurpose each new video into content derivatives. Common use cases: monitor Graeham's own channel for his uploads, monitor a competitor channel for their topics, monitor an industry voice for trend signal.

**How it works:** invoke `../youtube-scraper/SKILL.md` (standalone skill) to scan the channel for new uploads in the last 24 hours (or user-specified window), check against `processed_videos.txt` to skip already-handled videos, and extract metadata + transcript for each new video. The scraper delegates transcript work to `scripts/youtube_transcriber.py` so the same transcription pipeline handles both modes.

**Output:** `outputs/scraper/current_video_{N}.md` files (one per new video) + transcript files in `outputs/transcripts/`.

**Triggers:**
- User pastes a YouTube channel URL (`youtube.com/@channelname` or `/channel/UC...` or `/c/channelname`)
- User says "check my YouTube channel for new uploads," "monitor [channel] for new videos," "scrape this YouTube channel"
- Scheduled task fires (daily check on Graeham's channel + competitor watch list)

**After Mode B completes:** for each new video, either:
1. Run Mode A's downstream flow (skip Phases 1-2, go to Phase 3 → Phase G to build derivatives), OR
2. If multiple new videos found, batch-process: each video becomes its own per-topic content package run

**Important:** Mode B is for *channel monitoring*, not single-URL transcription. Don't fire Mode B when the user pasted a single video URL — use Mode A. Don't fire Mode A when the user pasted a channel URL — use Mode B.

#### Skip Phase 0 entirely when:

- The user is asking for original content ideas with no external video source — go straight to Phase 1
- The user already has a topic and just wants the content package — go to Phase R (per-topic research) → Phase G

#### After Phase 0 Completes (Either Mode):

If Phase 0 produced a transcript / source ingestion brief, **skip Phases 1-2** (the source video replaces ideation) and jump to Phase 3 (BOFU Intent Scorer) with the brief, or go directly to Phase G (Script Writer) for a quick script.

If Mode B produced multiple new videos, treat each one as its own per-topic content package run — they batch-feed into Phase G in sequence.

### Phase 1 — BOFU Query Generator

**Read:** `references/phases/bofu-query-generator.md` (absorbed phase reference; was a standalone skill prior to May 2026 consolidation)

Generate 230+ localized bottom-of-funnel query patterns across 5 inquiry types (SELL, BUY, COSTS, OPTIONS, 1482). Output: `outputs/bofu-queries-{timestamp}.json`.

### Phase 2 — Content Ideation Engine

**Read:** `references/phases/content-ideation-engine/instructions.md` and its reference files:
- `references/phases/content-ideation-engine/references/apify-actors.md` — Apify actor config
- `references/phases/content-ideation-engine/references/subreddit-list.md` — target subreddits with priorities
- `references/phases/content-ideation-engine/references/query-templates.md` — search query templates
- `references/phases/content-ideation-engine/references/ideation-rubric.md` — what signals to extract

Pull live audience demand via Apify `trudax/reddit-scraper-lite` (primary) + Claude web search + browser deep dives (supplementary). Run `scripts/run_reddit_ideation.py` for the Reddit scrape. Requires `APIFY_API_TOKEN` in environment.

Output: `outputs/ideation-raw-{timestamp}.json` and `outputs/ideation-topics-{timestamp}.json`.

### Phase 3 — BOFU Intent Scorer

**Read:** `references/phases/bofu-intent-scorer.md` (absorbed phase reference; was a standalone skill prior to May 2026 consolidation)

> **This is the INTENT SCORE, not the OPPORTUNITY SCORE.** It classifies each topic's BOFU intent (DECISION / CONSIDERATION / AWARENESS) for funnel-mix purposes. It does NOT decide whether a topic should be covered this week — that job belongs to the 25-pt Opportunity Score in `content-calendar`. See the Scoring Architecture table at the top of this file.

Scores each candidate topic on the 6-criteria rubric: Inquiry Type Match, Intent Matrix Position, Source Confirmation, Emotional Temperature, Local Relevance, and Freshness (penalties + bonuses from `topic-history.json`). Base score max 25; freshness adjusts ±5. Keep ≥18/25 after freshness applied. Output: `outputs/scored-topics-{timestamp}.json`.

### Phase 4 — Funnel Tagger

**Read:** `references/phases/funnel-tagger/instructions.md`

Tag surviving topics TOFU / MOFU / BOFU. Default mix 40/30/30. Override based on user goal (lead gen bias = 20/30/50, audience growth bias = 60/25/15, fresh-listing bias = heavy BOFU for that listing's market). Output: `outputs/tagged-topics-{timestamp}.json`.


### Phase 4.5 — Format Ranker (PropertyIQ CI v1.0)

**Read:** `references/phases/format-ranker.md`

For each scored, funnel-tagged topic, produce a ranked list of which formats (YT Long, YT Short, IG Reel, TikTok, Carousel, Blog, GBP, Facebook, Email) to produce and in what order. Uses the Format Type Scoring Formula from PropertyIQ Content Intelligence v1.0 with workflow constraint applied. Tells Phase 5 which derivatives to generate vs skip. Required for any multi-derivative content package.

### Phase 5 — Script Writer

**Read:** `references/phases/script-writer/instructions.md` and its reference files:
- `references/phases/script-writer/references/content-pillars.md` — Graeham's content pillar framework
- `references/phases/script-writer/references/platform-specs.md` — per-platform length/format rules
- `references/phases/script-writer/references/cross-posting-matrix.md` — cross-post adaptation matrix
- `references/phases/script-writer/references/voice-and-style.md` — Graeham's voice guide
- `references/phases/script-writer/references/seo-keywords.md` — SEO keyword set
- `references/phases/script-writer/references/aeo-geo-requirements.md` — Answer Engine Optimization + Geo requirements
- `references/phases/script-writer/references/lead-capture-keywords.md` — GHL comment-keyword automation map

**Conditional reference files — read only when generating blog post derivative:**
- `references/phases/script-writer/references/schema-markup-templates.md` — JSON-LD schema templates (Article required, FAQPage when blog has FAQ section, VideoObject when YouTube embed exists, HowTo when content is step-by-step, BreadcrumbList optional)
- `references/phases/script-writer/references/rss-internal-linking.md` — scrape graehamwatts.com RSS / sitemap / blog index, identify 2-4 semantically relevant existing posts, insert inline links naturally in body
- `references/phases/script-writer/references/youtube-embed-patterns.md` — responsive iframe embed + timestamp link patterns when source is a YouTube video

Produce multi-platform content packages: hook, short-form script, long-form script, caption, hashtags, comment-keyword CTA, cross-post matrix, AND an **ElevenLabs-Ready Variant** (v3 audio tags + v2 break-tag fallback + voice settings block) for every script so Graeham can paste directly into ElevenLabs with no guessing on inflection. See `references/phases/script-writer/references/elevenlabs-audio-tags.md`. Output: `outputs/content-package-{timestamp}.md`.

---

## Video Duration Estimation (Mandatory Calculation)

NEVER guess or default to generic durations like "8-10 minutes." Every script MUST include an explicit timing calculation based on actual word count:

1. **Count the actual words** in the script body (exclude shot directions, editing notes, and metadata)
2. **Average speaking pace:** 150 words per minute for conversational delivery
3. **Add 15%** for pauses, transitions, and B-roll cuts
4. **Formula:** `(word_count / 150) × 1.15 = estimated minutes`
5. **The target duration in the section header MUST match this calculation**

Examples:
- 150-word script → (150/150) × 1.15 = ~1.15 minutes → "Target: ~1 minute"
- 750-word script → (750/150) × 1.15 = ~5.75 minutes → "Target: ~6 minutes"
- 1500-word script → (1500/150) × 1.15 = ~11.5 minutes → "Target: ~11-12 minutes"

If the script is only ~150 words, it is a 1-minute video, NOT an 8-minute video. Be accurate. Show the word count and calculation in a comment at the top of the script output so the estimate is verifiable.

## Script Output Format (Required Section Headers)

Every script output MUST use the following visually distinct section headers so that Adrian, Peter, or John can grab just their section without confusion. Each section is self-explanatory and separated by a clear visual divider:

```
═══════════════════════════════════════════════════
📹 LONG-FORM SCRIPT (YouTube — Target: [X] minutes)
Platform: YouTube | Format: Talking head + B-roll
═══════════════════════════════════════════════════

[script content here]

═══════════════════════════════════════════════════
📱 SHORT-FORM SCRIPT (Reels / Shorts / TikTok — Target: [X] seconds)
Platform: Instagram Reels, YouTube Shorts, TikTok
Cut from: Long-form timestamp [X:XX - X:XX] OR record separately
═══════════════════════════════════════════════════

[script content here]

═══════════════════════════════════════════════════
🎬 SHOT LIST — Hand to production team (Peter/John)
═══════════════════════════════════════════════════

[shot list here with numbered shots, each with: shot description, duration estimate, location/setup notes]
```

These headers are non-negotiable. Every script output — whether standalone or embedded in a V6 Production Calendar — MUST start each piece with its corresponding header block. Do not omit headers, do not merge sections, do not use plain markdown headers instead. The visual dividers (`═══`) ensure each section is scannable when printed or viewed on a phone.

## V6 Production Bible Integration

When scripts are generated as part of a V6 Production Calendar (content-calendar skill), the output format changes from standalone markdown to **embedded HTML derivative panels** inside the hosted calendar page.

**Read `references/production-bible.md`** when actually writing scripts for a production calendar (Phase G / Phase 5). It covers: the 9-format Derivative Format System table, Inline Shot Direction Tags syntax, the Editing Notes for Jason block, complete ElevenLabs SSML block format + mandatory text normalization rules (no em-dashes in spoken text, period-terminated statements, spelled-out numbers), AI Video Prompt format for Seedance/Kling + B-roll coverage math + the generation-reliability discipline (start-frame-first, first-frame QC gate), the active GHL keyword list, and the AEO cite-ready statement format. Not needed for ideation, scoring, or research phases.

**Read `references/production-hardening.md`** (v7.3) when building a V6/V7 production calendar or debugging the daily N8N automation. It covers: the mandatory Date & Year QC block, the fail-closed Identity & Date Validation Gate (the DRE-01466876-only hard check), the daily Peter email N8N workflow (`REVqxrlAb3CHJumM`), the YouTube Long output-split strategy (Pt 1 script+voice / Pt 2 production package — needed because a single 6-deliverable prompt truncates), and the mandatory week-over-week overlap check before shipping.

## Examples

Three worked examples live in `examples/`:
- `example-1-bofu-trigger-event-tech-layoff.md` — BOFU response to a tech layoff trigger event
- `example-2-tofu-lifestyle-reel-epa-tacos.md` — TOFU lifestyle reel (East Palo Alto tacos)
- `example-3-aeo-legal-education-ab1482.md` — AEO-optimized legal education on AB 1482

Read these before writing new content packages — they show the expected output format and voice.

## Example Prompts

**Per-topic (this skill):**
- "Build a content package on the EPA homicide-free story" → Phase 0a (confirm topic) → Phase R (pull topic-matched research) → Phase G (build package)
- "I just got a new listing in Menlo Park at $2.1M — give me the full content package" → Phase R (the listing IS the topic) → Phase G
- "Make me a TOFU reel about East Palo Alto lifestyle"
- "Generate 5 BOFU videos about AB 1482 for Bay Area landlords"
- "Hey I saw this video, can we do something like this? https://youtube.com/watch?v=..." → Phase 0 (ingestion) → Phase R → Phase G
- "Transcribe this YouTube video and tell me what ideas we can use" → Phase 0 ingestion only
- "Here's a video about staging tips — adapt it for EPA sellers on a budget"

**Weekly planning (hand to `content-calendar` — NOT this skill):**
- "What should I post this week?"
- "Plan my content calendar for the next 7 days"
- "What topics should I focus on based on my data?"
- "What are my competitors posting that I'm not?"
- "The Bay Area just had a big tech layoff announcement — what should I post?"

**Ambiguous — run Phase 0a clarifier:**
- "I need content"
- "Run research"
- "Content opportunities"
- "What's happening in EPA?"

## Output Locations

All phase outputs save to the user's selected folder (or `outputs/` in Cowork). Provide `computer://` links to the final content package when delivering.

## Data Source Status

- **Primary:** Apify `trudax/reddit-scraper-lite` with residential proxy (~$0.30-$2.50 per run). Requires `APIFY_API_TOKEN`.
- **Supplementary (organic):** Windsor MCP for Instagram, YouTube, Facebook ORGANIC, Search Console, and Apify scraper performance data. Windsor stays canonical for organic signal — the official Meta Ads MCP has no organic tools.
- **Supplementary (paid signal, added 2026-06-07):** Official Meta Ads MCP via the `meta-ads` skill — ad performance (CPL by angle, winning hooks, anomaly signals) feeds per-topic research and the Performance Signal section. If the connector isn't live, flag it in the Run-note banner and proceed without paid signal; do NOT substitute Windsor's `facebook` ads connector unless the user explicitly asks for blended cross-channel reporting.
- **Supplementary:** Claude web search for market context, news events, and competitor research.
- **Supplementary:** Chrome browser for MLS data, local government sites, and Google Trends.

## Auto-Render Hand-off (v6.2 — Apr 2026)

Once a V6 script is finalized, it no longer needs to be manually copy-pasted into ElevenLabs and HeyGen. The `heygen-elevenlabs-renderer` skill owns the full render pipeline and this skill hands off to it.

### What this skill produces for the renderer

For every core asset script written, write out a companion SSML file next to the content package:

```
outputs/content-package-{timestamp}.md         (the full package — scripts, captions, etc.)
outputs/content-package-{timestamp}.ssml.txt   (just the <speak>…</speak> block, nothing else)
```

The `.ssml.txt` file is the raw input the renderer reads. It must contain only the SSML — no headers, no comments, no markdown fences, no "SCRIPT:" prefix. One file = one render.

### Known SSML quirks (read before hand-off)

ElevenLabs `eleven_multilingual_v2` does NOT fully honor `<prosody>`. Only `<break time="Xs"/>` produces audible effect. `<prosody rate="slow">` tags are accepted by the API but silently dropped — the inner text is still read, just at the default speed. So:

- KEEP `<prosody>` tags for human readability in the package file (they document intent)
- ALSO provide the `.ssml.txt` with the same tags (the renderer strips ineffective ones at TTS time)
- When you genuinely need rate/pitch change (e.g., whispered BOFU asides), use **ElevenLabs bracket audio tags** inside the text: `[whispers]`, `[excited]`, `[sarcastic]`, `[laughs]`. See the renderer skill's `references/elevenlabs-audio-tags.md`.

### Hand-off invocation (one command)

After this skill writes the package, the renderer takes over:

```bash
python3 skills/heygen-elevenlabs-renderer/scripts/full_render.py \
  --script outputs/content-package-{timestamp}.ssml.txt \
  --slug "{content-slug}" \
  --resolution 1080p \
  --aspect 9:16
```

The renderer: (1) synthesizes MP3 via ElevenLabs using Graeham's voice clone `Pa3vOYQHHpLJn1Tf7hnP`, (2) uploads MP3 to HeyGen, (3) creates an avatar video against Graeham's avatar `9a3600b16f604059b6ab8b9a55e29ea9`, (4) polls until complete, (5) downloads MP4 to `outputs/renders/{slug}.mp4` with a sibling `{slug}.meta.json` holding `video_id`, `video_url`, and duration.

### Dashboard locations (where rendered media lives)

After a render completes, the same files are available in four places. The renderer (`poll_and_download.py`) writes a `dashboards` block into `{slug}.meta.

### Rule 15: Two-Register Freshness Check

**Why this exists:** Prior to April 24 2026, the ideation engine only
checked `topic-history.json`'s `history` array (posted topics). Topics
that had been SHOT but not yet POSTED were invisible to the gatekeeper,
which meant the engine could queue a near-duplicate of a video sitting
in Graeham's edit pipeline.

**The fix:** `topic-history.json` now has TWO registers — `history`
(posted) and `in_production` (shot-but-not-posted). Every freshness
check must read BOTH.

**Implementation in ideation-engine:**

1. Load `topic-history.json`.
2. Build `excluded_slugs = {t['slug'] for w in history for t in w['topics']} | {t['slug'] for t in in_production}`.
3. For each candidate topic, also check `exclusion_radius` text on every
   `in_production` entry — if the candidate touches the same market +
   angle, exclude even when the slug differs.
4. When a topic ships, MOVE it from `in_production` (if present) into
   `history`. Don't leave duplicates.

**When to write to `in_production`:** Whenever Graeham confirms he has
shot or is currently editing a video for a topic that isn't yet posted.
Add via the `script-writer` phase or manually before ideation runs.

Reference: `skills/content-creation-engine/references/topic-history.json`
schema v2.0.

---

## Publishing via Composio (canonical pattern)

> **Read first:** [`shared-references/publishing-via-composio.md`](../shared-references/publishing-via-composio.md) — single source of truth for ALL skills.

After generating the topic-production dashboard HTML output, publish via Composio t

---

## Workflow Quality Rules — MUST ride along in every script + production copy (June 2026)

These rules fix the recurring generation failures (voice garbles, uptalk, weak/scarce b-roll, generic maps). Mandatory for every content package, and they MUST be prepended to: every **Copy Script Prompt**, every **Copy Production Prompt**, and the **daily Peter email** (N8N workflow `REVqxrlAb3CHJumM`) so whoever pastes the copy into Claude gets the rules inline.

**Voice / SSML (full detail in `references/phases/script-writer/references/elevenlabs-audio-tags.md`):** NO em/en dashes in the ElevenLabs variant (periods, commas, or `<break>`); question marks ONLY on real questions (a trailing `?` causes uptalk); spell out numbers/currency/symbols; end every statement with a period; synthesize sentence-by-sentence and QC each chunk (Whisper diff), re-roll only the bad sentence.

**B-roll (full detail in `references/phases/broll-gates-and-router.md`):** plan ~1 cutaway per 3-5s with hard floors (short-form 8-14, long-form 40+), not a fixed 5; TAG every shot [AI]/[STOCK]/[MAP]/[FILM]; route each shot (map -> Mapbox at real coordinates; known place -> stock or videographer; on-screen text -> Remotion overlay; only novel -> [AI] generate); for [AI], APPROVE the first-frame still BEFORE animating (never animate a bad frame), locked start frame, 2-4s clips; QC gate per clip; location-specific always; emit a Videographer Shot Request when stock is missing.

**Avatar:** render on HeyGen Avatar V (best motion) by default; never render on Avatar IV then redo on V.

**Motion graphics / captions / music:** text and data are Remotion overlays (never burned into generated video); captions time-aligned to the known script; music from the licensed library.

---

## Field notes (content, Pantana 2026-06)

> Load `shared-references/pantana-field-notes-2026-06.md` (section "→ content-creation-engine / concept-forge / cinematic-hooks") before idea/hook work.

- **99 Video Scripts swipe-file** — a hook/idea bank; localize before use (San Diego-specific in places).
- **Neighborhood News Blueprint** — green-screen hyperlocal news reel workflow: Google Alerts/Newsbreak/Grok → GPT script → BigVu → Canva/CapCut.
- **Right content / right platform** — market-snapshot videos win on YouTube but hurt reach on IG; be selective on IG.

Source backups: Obsidian `06 Coaching & Training/Jason Pantana/Source Docs (extracted)/`.
