---
tags: [skill, content-engine, real-estate]
updated: 2026-05-25
skill_path: skills/content-creation-engine/SKILL.md
---

---
name: content-creation-engine
description: "Bay Area / East Palo Alto real estate content creation engine for Graeham Watts (REALTOR, Intero Real Estate, DRE# 01466876). Use this skill ANY time the user mentions: content creation engine, create content, newsletter content, blog post, ad copy, social media content, video script, content ideas, YouTube, Reels, Shorts, TikTok, AI avatar script, listing video, market update video, BOFU content, TOFU content, MOFU content, Bay Area real estate content, East Palo Alto content, Redwood City content, Palo Alto content, Menlo Park content, San Mateo County content, Reddit ideation, content scoring, content pillars, AB 1482, relocation content, first-time-buyer content, seller content, find me topics, content intelligence, I need content, market research, topic discovery, or anything related to generating inbound real-estate content for Graeham's markets. Also trigger when the user uploads MLS data or a new listing and wants a content package, or pastes a YouTube URL and wants content ideas from it."
---

# Content Creation Engine

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

Per-Topic Research in this skill pulls research SPECIFIC TO ONE TOPIC (the stats, news, quotes that back this one content package). The WEEKLY research that feeds multi-topic scoring lives in `content-calendar`.

| Request type | Which skill | Why |
|-------------|-------------|-----|
| "What should I post this week?" | `content-calendar` | Weekly scope, multi-topic scoring |
| "Plan next week's 5 topics" | `content-calendar` | Weekly scope |
| "Build a content package for [specific topic]" | `content-creation-engine` (this skill) | Per-topic scope |
| "I have a new listing, give me content for it" | `content-creation-engine` (this skill) | Per-topic scope |
| "Research and write content on [breaking news]" | `content-creation-engine` (this skill) | Per-topic scope, includes Per-Topic Research research |
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
| Per-Topic Research scoring (10-pt, 4 criteria) — DELETED | Per-topic research — no scoring | Per-Topic Research below (rewritten) |
| Phase 2 "4-axis scoring" | Reddit signal filtering (what to surface from scrape) | Phase 2 content-ideation-engine |

**Rule of thumb:** If a topic is on the weekly calendar, content-calendar already scored it (Opportunity). When you build its content package here, Phase 3 scores it again for a DIFFERENT reason (Intent). Both scores appear in the Scoring Architecture panel on the single-topic dashboard — see `references/single-topic-dashboard-rules.md` for the rendering spec.

## Before You Start — Read These

1. **`CLAUDE.md`** (bundled with this skill) — full orchestrator / project instructions. Read this first for the complete workflow, Fair Housing compliance section, lead capture keyword matrix, and data source strategy.
2. **`references/market-config.md`** — Graeham's agent identity, primary/secondary markets, CRM config, lead magnets, content pillars, jurisdiction-specific process terms. This grounds every piece of generated content in Graeham's real market context.
3. **`references/research-sources.md`** — Complete documentation of every data source used in Per-Topic Research (Research & Discover), including what to pull, how to pull it, what to look for, and the scoring rubric.
4. **`references/single-topic-dashboard-rules.md`** — 12 strict rules + 16-item self-check for building single-topic production dashboards. Reference implementation: `online-content/dashboards/single-topic/2026-04-18-epa-two-years-homicide-free-production.html`. Template builder: `templates/single-topic-dashboard-builder.py`.
5. **Shared Branding** — Before generating any client-facing output, read the shared branding reference at `../shared-references/branding.md` for consistent colors, fonts, and UI components.

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

#### Canonical Humanizer Block (copy verbatim into every prose-generating prompt)

```
HUMANIZER RULES (apply throughout the output — do NOT mention these rules in the response itself, just follow them):

Avoid these AI-tell patterns:
- Em dashes — use commas, periods, or parentheses instead.
- Significance inflation: "stands as a testament," "marks a pivotal moment," "evolving landscape," "key turning point," "deeply rooted," "indelible mark."
- Promotional language: "boasts a," "nestled in," "vibrant," "rich" (figurative), "stunning," "must-see," "groundbreaking," "renowned," "breathtaking."
- Vague attributions: "experts say," "industry observers note," "research suggests" without naming the actual source.
- "-ing" tail clauses that add fake depth: "highlighting...," "underscoring...," "ensuring...," "contributing to...," "reflecting...," "showcasing..."
- Forced rule-of-three lists: "innovation, inspiration, and industry insights" / "streamlining, enhancing, fostering."
- Negative parallelism: "It's not just X, it's Y" / "Not only X, but Y."
- Tailing negation fragments: "no guessing," "no wasted motion" tacked onto sentences.
- Copula avoidance: "serves as," "stands as," "functions as," "represents a." Use "is" / "are" / "has."
- Sycophantic openers: "Great question," "I hope this helps," "Certainly," "Of course," "You're absolutely right."
- Knowledge-cutoff disclaimers: "As of my last update," "While specific details are limited."
- Excessive hedging: "could potentially possibly," "might have some effect on."
- Generic positive conclusions: "the future looks bright," "exciting times lie ahead," "represents a major step."
- Inline-header vertical lists where every bullet starts with "**Bold Header:**" followed by a colon.
- Curly quotes (use straight quotes only).
- Mechanical boldface — reserve bold for true emphasis, not decoration.
- False ranges: "from X to Y" when X and Y aren't on a meaningful scale.
- Persuasive authority tropes: "the real question is," "at its core," "what really matters," "fundamentally."
- Signposting announcements: "Let's dive in," "Here's what you need to know," "Now let's look at."
- Hyphenated word-pair clusters: "high-quality, data-driven, client-facing, decision-making" all in one sentence.

Instead:
- Vary sentence rhythm. Mix short punchy sentences with longer flowing ones.
- Use first person when it fits: "I keep coming back to," "Here's what gets me."
- Use specific numbers, dates, and concrete details over abstract claims. "$680K-$850K in Woodland Park" beats "competitive pricing in the area."
- Sound like one human talking to another about something that matters.
- Acknowledge complexity and mixed feelings when honest: "This is interesting but also kind of unsettling" beats "This is interesting."
- If the topic has a real edge or controversy, lean into it. Don't sand it down.

Read the final draft aloud in your head. If any sentence sounds like a press release, a Wikipedia article, or a LinkedIn thought leader, rewrite it.
```

#### Block Placement Order in the Prompt Preamble

```
1. Agent Identity (Graeham Watts, REALTOR, Intero, DRE 01466876)
2. Fair Housing Guardrails
3. DATE/YEAR QC
4. Timing Self-Check (scripts only)
5. Voice & Style
6. HUMANIZER BLOCK  ← inserted here
7. Topic + Key Facts
8. AEO stats
9. GHL CTA / Lead Capture
10. Format-specific deliverable spec
```

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

The canonical block above is the single source of truth. When the `humanizer` skill at `skills/humanizer/SKILL.md` is updated with new patterns (new AI-tells observed in the wild), update this block in the same commit so PROMPT_LIBRARY entries stay in sync. The block is intentionally compact — 30-35 lines — to keep prompt size reasonable while covering the patterns that cause the most damage in spoken / read content.

**Failure mode this prevents:** Rule 7 (post-gen humanizer skill pass) only works when this skill generates content directly. When Adrian/Peter copy a prompt and paste into an external AI tool, Rule 7 doesn't fire — and the resulting script or blog reads like ChatGPT wrote it. Rule 8 closes that gap by moving the humanizer rules upstream into the prompt itself, so the external AI never produces the bad output in the first place.

#### Canonical prompt-data structure (May 2026 update)

The CURRENT canonical weekly calendar uses a `const COPY_DATA = { "t1": { "ssml": "...", "prod_video": "...", "blog_brief": "...", "prod_blog": "..." }, "t2": {...}, ... }` JS object with 5 topics × 4 prompt types = 20 entries. Of those, 15 are prose-generating (3 per topic: prod_video, blog_brief, prod_blog) and MUST contain the Humanizer Block. 5 are SSML markup (one per topic) and MUST NOT contain the block (it would break the XML).

Older variants of the calendar (the `-all.html`, `-blogs.html`, `-videos.html`, `-research.html` quad-file pattern with `const PROMPTS = {...}`) are deprecated as of 2026-05-15 due to two architectural defects documented in Rules 9 and 11 below. New calendars use the single-file COPY_DATA pattern in `2026-05-11-production-calendar.html`.

---

### Rule 9: No Orphan Internal Links (Non-Negotiable)

Every `href=""` attribute in a generated dashboard HTML file MUST point to one of:
1. An in-page anchor (`href="#section-id"`) where the target id exists in the same file, OR
2. A JavaScript no-op (`href="#"` paired with `onclick`) for setView/setFilter buttons, OR
3. A fully-qualified external URL on a domain that's actually reachable (citation links, social posts, etc.), OR
4. A relative URL to another file that is ALSO pushed to GitHub in the same commit

**Forbidden:** any `href=` to a sibling HTML file that doesn't exist on GitHub Pages. This was the root cause of the "blog tab 404s" failure on 2026-05-15 — the `-all-humanizer.html` linked to `2026-05-11-blogs.html`, `-videos.html`, `-research.html`, and `-all.html` (the four older variant files) but only the humanizer variants were ever pushed. Every audience tab 404'd silently on the live URL.

**Pre-push audit (mandatory):**

```bash
# Extract all hrefs from the dashboard HTML
grep -oE 'href="[^"]*"' dashboard.html | sort -u > /tmp/hrefs.txt

# For each href that points to a relative .html file:
# 1. Check it exists in /tmp/online-content-clone/dashboards/weekly-calendars/
# 2. If missing on the remote and not being added in this commit, FAIL the push

# For each href that's a fully-qualified external URL:
# 3. (optional) HEAD request to confirm 2xx, flag any 404
```

The pre-push audit must run as part of every weekly calendar build. If any `href=` points to a missing local file, STOP and either fix the link or include the target file in the same commit.

**Failure mode this prevents:** Zombie file references. Files that exist locally in Documents\Claude but never made it to GitHub get cross-linked from pushed files, creating tabs/buttons that 404 on the live URL while looking fine in local preview.

---

### Rule 10: Visual Dashboard Sections Required (Non-Negotiable)

Every weekly calendar MUST include the following visual dashboard sections, in this order, at the TOP of the file (before the Calendar grid and per-topic sections):

1. **Hero + audience-tab nav** — header bar, week date range, 5-button filter row (Research / Diagram / Calendar / Video / Blog) wired to `setView()` and `data-audience=""` attributes
2. **Run-note banner** — any blockers (e.g., "Apify blocked at firewall, pivoted to WebSearch") so the production team knows what was fresh vs derived
3. **Research — Live Data Layer** — source cards showing which 8 data sources ran live, blocked, or partial. Color-coded: green = live, red = blocked
4. **Performance Signal — What's Actually Working** — **ApexCharts brushable time-series ONLY** (Chart.js is forbidden for these charts — it lacks brush interaction):
   - Instagram Activity Over Time — area chart, last 26 weeks (100 posts via Composio Meta Graph API), dual axis (likes + posts), brush slider below for drag-to-zoom
   - YouTube Activity Over Time — area chart, last 14 weeks (50 videos via YouTube Data API v3), dual axis (views + videos), brush slider below
   - Engagement Rate Per Post Per Week — line chart, avg per-piece for IG + YT, strips out posting-frequency effect, brush slider below
   - Each chart is a PAIR: a main chart (`#xxxChartMain`, height 300) + a brush slider (`#xxxChartBrush`, height 100, marginTop -6) wired via `brush: { target: 'xxxMain', enabled: true }, selection: { enabled: true, ... }`
   - Library: `<script src="https://cdn.jsdelivr.net/npm/apexcharts@4.5.0"></script>` (or later compatible version)
   - The brush pattern lets users drag a window on the bottom slider to zoom the main chart to any time range. This is the canonical "slide it across time" interaction Graeham expects.
   - **Top 5 lists** (YouTube Top 5 last 99 videos, IG Top 5 last 20 posts) — render as data tables, not charts. Sortable by views / likes / engagement.
5. **Full Weekly Research Data panel** — collapsible accordion containing the 7 mandatory data tables that back the week's topic picks:
   a. Instagram Own-Channel Performance — last 25 posts with caption excerpt, likes, comments, pattern match column (gold-highlighted rows = match week's content patterns)
   b. YouTube Own-Channel Performance — last 15 videos with views, likes, comments, pattern match column
   c. Google Search Console Topic-Targeted Queries — query, impressions (last 7d), clicks, position, trend WoW, day-the-query-maps-to
   d. Reddit Demand Signals — subreddit, thread title, upvotes, comments, topic cluster (star the day-of-week match)
   e. Zillow Q&A — question, page, asked count (last 30d), day-the-question-maps-to
   f. MLS Pull — metric, current month, year-ago, YoY delta (with trend-up/trend-down color coding)
   g. Convergence — Why Each Day Picked — day, topic, sources-converged list, score out of 25 (star the highest-converging day)
   Plus a Macro Rates & Permits bullet list (30Y fixed rate, Fed Funds, county permits, notable ADU permits) and a DataForSEO SERP Queue status note.
6. **Freshness Constraints + Citations** — 4-week topic history check, blocked angles, citation URLs (external)
7. **Diagram — How We Built This (10-Step Data Pipeline)** — clickable nodes showing data flow: 4 INPUT nodes → 3 ANALYSIS nodes → 3 OUTPUT nodes
8. **Calendar — Week of [date range]** — 5 day-cards with funnel-tier color coding (TOFU/MOFU/BOFU), GHL keyword chips, click-to-expand topic details
9. **Video Content — All 5 Topics** — per-topic article cards with Copy SSML + Copy Production Prompt buttons
10. **Blog Content — All 5 Topics** — per-topic article cards with Copy Blog Brief + Copy Production Prompt buttons

**Failure mode this prevents:** Calendars shipped without the visual research dashboard look like prompt dumps and provide no analytical context. The production team can't tell which topics are backed by which data signal, and Graeham can't review the run quality at a glance. Two real production failures led to this rule:

1. On 2026-05-15 the `-all-humanizer.html` shipped without sections 4 (Performance Signal charts) and 7 (Pipeline Diagram), making it look incomplete next to the prior week's production-calendar.html.
2. Later that same night the rebuilt production-calendar shipped with Chart.js line charts (no brush) and only a 6-card Live Data Layer with no underlying data tables. Graeham flagged it: "the graphs you created are different from the graphs in the previous version — should be the ones where you can slide across time" and "missing a lot of the research data." The fix required transplanting the ApexCharts brushable charts + 7 data tables from `2026-05-11-research.html`. **This rule's section 4 now mandates ApexCharts brushable (not Chart.js) and section 5 enumerates the 7 required data tables explicitly so the omission can't repeat.**

---

### Rule 11: Single Canonical File Pattern (Non-Negotiable)

A weekly calendar is ONE file, not four. The deprecated pattern was:
- `2026-05-11-all.html` — full view
- `2026-05-11-blogs.html` — blog-track filter
- `2026-05-11-videos.html` — video-track filter
- `2026-05-11-research.html` — research-only filter

That pattern is **forbidden** going forward. The four files were not in sync (different sizes, different prompt content), the audience tabs cross-linked between them (creating the Rule 9 violations), and maintaining four parallel files for the same week multiplied the surface area for bugs by 4x.

The canonical pattern is **ONE file per week**:
- `2026-MM-DD-production-calendar.html` (where MM-DD is the Monday the week starts)

Audience filtering happens **via in-page JavaScript** using:
- `data-audience="blog all"` attributes on each section
- A `setView('blog')` function that hides/shows sections matching the selected view
- The "Show everything" link resets to `setView('all')`

This means clicking "Blog Track" doesn't navigate to a sibling file — it just filters the current file. No 404 risk. No drift between variants. One file to maintain, one URL to share, one place to verify before pushing.

**Existing deprecated files** (`2026-05-11-all.html`, `-blogs.html`, `-videos.html`, `-research.html`, and their `-humanizer` siblings) should be removed from `Graehamwatts/online-content` in a cleanup commit. They remain locally for archival but should not be referenced or linked to from any new file.

**Failure mode this prevents:** Variant proliferation. Each variant file is another place where the prompt data can drift, where href targets can break, and where a humanizer update has to be applied 4x instead of 1x.

---

## Fair Housing Guardrails (Non-Negotiable)

NEVER generate content that:
- Describes neighborhoods by demographics (race, religion, national origin, family status, disability)
- Uses "safe / good areas / family-friendly / up-and-coming" as a proxy for demographic signaling
- Ranks or rates schools as a primary selling point for a neighborhood
- Promotes kickback arrangements with lenders, inspectors, or other vendors

Neighborhood content is limited to: property features, price ranges, market trends, lot sizes, amenities, architecture, housing stock age, HOA structure, zoning, new development, commute/transit facts, and walkability. When in doubt, reframe or drop the topic. This is both the law and Graeham's brand standard.

---

## THE PER-TOPIC WORKFLOW (Per-Topic Research is PER-TOPIC, not weekly)

> **Rewritten April 2026.** Previous version of Per-Topic Research pulled 8 weekly-scope sources and applied a 10-pt scoring rubric — that's weekly-planning work and it belongs in `content-calendar`. This skill's Per-Topic Research now does one job: gather citations, stats, and quotes for ONE topic that's already been selected.

When a topic arrives here (from `content-calendar`'s weekly plan, or a direct ask like "build a package on X"), Per-Topic Research pulls the *research data panel* that backs the single-topic dashboard. When the request is "what should I post this week?" — **hand it to `content-calendar`, not Per-Topic Research.**

### Phase 0a — Clarifier Check (ASK BEFORE RESEARCHING)

Before pulling any data, confirm the scope in ONE question. Don't skip this step — it prevents a full Per-Topic Research run for a request that actually wanted weekly planning, or vice versa.

If the user's ask is ambiguous, confirm in this form:

> "Before I start — which of these are you asking for?
> (a) **Per-topic content package** — you already know the topic (e.g., 'EPA homicide-free story', 'this new $2.1M listing', 'AB 1482 explainer'). I'll pull research for THAT topic and build the full dashboard.
> (b) **Weekly planning** — you want me to decide which topics to cover this week. For that I should hand off to `content-calendar`.
> (c) **Raw research only** — you want current market signal dumped to the chat, no package built yet."

If the ask is unambiguous (user provided a specific topic, a listing, a YouTube URL, or breaking news), skip Phase 0a and proceed to Per-Topic Research.

### Per-Topic Research (citations & stats for ONE topic)

**Read:** `references/research-sources.md` for source documentation.

Given ONE already-selected topic, pull the evidence that will populate the dashboard's "Show Full Research Data" panel — statistics, quotes, news clippings, permits, MLS comps, GSC queries that match this topic. **No scoring happens here.** The Opportunity Score is already done (content-calendar set it when the topic was selected). The Intent Score runs in Phase 3.

#### What to pull (scoped to the ONE topic)

1. **Topic-matched MLS stats** — only the price bands / DOM / inventory numbers that back this topic. If the topic is "EPA homes under $700K," pull that bucket. Do NOT pull the full county stat sheet.
2. **Topic-matched GSC queries** — the specific queries from Search Console that this topic targets. Note impressions, position, and whether it's a rising query.
3. **Topic-matched local news/permits** — web search AND city gov search for this topic's exact subject (e.g., "East Palo Alto homicide rate 2026," "AB 1482 2026 amendments").
4. **Topic-matched social performance** — did similar topics perform well in the last 60 days on Graeham's channels? (This feeds the dashboard's "format recommendation" based on what worked for similar content.)
5. **Topic-matched competitor content** — have competitors covered this exact angle in the last 30 days? Use Apify datasets if fresh, Claude-in-Chrome for manual check otherwise.
6. **Topic-matched Reddit/audience signal** — pull relevant snippets from the most recent `outputs/ideation-topics-*.json` that match this topic's keywords.
7. **Simulated LLM Query Capture** — Before running this step, confirm the target geography. If the topic makes it obvious (e.g., "EPA homicide-free story" → East Palo Alto, "AB 1482 for RWC landlords" → Redwood City), proceed. If the topic is market-agnostic or could apply to multiple of Graeham's markets, ask: *"Which geography should I use for the LLM query simulation — East Palo Alto, Redwood City, Menlo Park, Palo Alto, or broader Peninsula/Bay Area?"* Use the confirmed geo in every prompt below.

   Query Claude (yourself), GPT-4 (via web or API), and Perplexity with this prompt for each relevant persona (BUYER, SELLER, RELOCATOR, INVESTOR — pick the 1-2 that fit the topic):

   > *"If a [PERSONA] were researching [TOPIC] in [GEO], list 15-25 specific questions they would likely ask an AI assistant. Output as a JSON array of strings."*

   Run for each persona × LLM combination. Deduplicate across results. Score each question by **cross-LLM agreement**: questions surfaced by 2+ LLMs independently are the highest-priority AEO targets — they represent what AI search engines themselves expect buyers/sellers to ask. Questions surfaced by only one LLM are lower priority but still useful.

   **Use the output to:**
   - Identify which questions your content package must answer directly (especially the 2+ LLM agreement ones)
   - Prioritize which AEO cite-ready statements go in the blog derivative
   - Determine the FAQ schema block questions for the blog's JSON-LD markup
   - Inform the hook for the video script (questions with high cross-LLM agreement = proven demand signal)

   This is a leading indicator for AEO — it surfaces what buyers/sellers will ask AI search engines 12-24 months before that demand shows up in Google Search Console.

Do NOT pull the broad weekly trend data Per-Topic Research previously pulled. That lives in content-calendar now.

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
  "reddit_signal": [ { "thread_title": "...", "url": "...", "upvotes": 0 } ],
  "llm_anticipated_queries": [
    {
      "question": "...",
      "persona": "BUYER",
      "cross_llm_agreement": 3,
      "llms_that_surfaced": ["claude", "gpt4", "perplexity"],
      "priority": "HIGH",
      "aeo_use": "FAQ block + cite-ready statement"
    }
  ]
}
```

`cross_llm_agreement` is 1–3 (how many of the three LLMs surfaced this question). Priority: HIGH = 3, MEDIUM = 2, LOW = 1. The `llm_anticipated_queries` array should be sorted HIGH → LOW before saving.

This JSON is the single source of truth for the "Show Full Research Data" accordion on the single-topic dashboard.

### If Graeham asks the ambiguous questions — routing table

| User says | Runs where |
|---|---|
| "What should I post this week?" | **`content-calendar`** (weekly planning + Opportunity scoring). NOT Per-Topic Research. |
| "Plan next week's 5 topics" | **`content-calendar`** |
| "Run research" / "What's happening in EPA?" | Phase 0a clarifier → usually content-calendar weekly research, unless user specifies one topic |
| "Build a content package for [specific topic]" | Per-Topic Research here, per-topic |
| "I have a new listing, give me content" | Per-Topic Research here, per-topic (the listing IS the topic) |
| "Transcribe this YouTube video and build content from it" | Phase 0 (ingestion) → Per-Topic Research here, per-topic |

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
| Market update / monthly report / weekly market read / "is now a good time to buy/sell" | `modules/market-update-narrative/README.md` | Module returns a narrative outline JSON; pass to Phase 5 script-writer for final format rendering |
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
4. **Ad Copy Variants** — If the topic lends itself to paid promotion: Facebook ad copy, Google ad copy, with multiple hook variants for A/B testing.
5. **Social Posts** — Platform-specific: IG caption with hashtags and GHL keyword CTA, Facebook post, LinkedIn post (if applicable), Google My Business post.

The generation phase uses the existing 6-phase pipeline (Phase 0 through Phase 5) documented below for the actual content creation logic. Per-Topic Research replaces the "what should I write about?" question — by the time we reach Phase G, we already know exactly what topics to cover and why.

---

### Phase A — Review & Approve

Present all generated content to Graeham (and Adrian if applicable) for approval. For each piece:
- Show the content with its section headers
- Note the source data that inspired it (from Per-Topic Research)
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
- The user already has a topic and just wants the content package — go to Per-Topic Research (per-topic research) → Phase G

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

When scripts are generated as part of a V6 Production Calendar (content-calendar skill), the
output format changes from standalone markdown to **embedded HTML derivative panels** inside the
hosted calendar page. This section documents the V6-specific requirements.

### Derivative Format System

Every content day MUST produce scripts for ALL of these platform formats:

| Format | Key Specs | Notes |
|--------|-----------|-------|
| **YouTube Long** | 8-15 min, 16:9, 1080p | Core asset — fullest script with all production details |
| **YouTube Short** | 30-59 sec, 9:16, 1080p | Strongest hook + one key insight + CTA |
| **IG Reel #1** | 30-60 sec, 9:16, 1080p | Hook-first, face-to-camera, caption overlay |
| **IG Reel #2** | 15-30 sec, 9:16, 1080p | Different angle/hook from Reel #1, B-roll heavy |
| **IG Carousel** | 5-10 slides, 1:1 or 4:5 | Key stats/facts as visual slides, swipe CTA |
| **TikTok** | 30-60 sec, 9:16, 1080p | More casual tone, trending audio hook if applicable |
| **Blog** | 800-1200 words, SEO-optimized | AEO-ready with cite-worthy key statements |
| **GMB (Google My Business)** | 100-300 words, 1 image | Local SEO post, location-tagged |
| **Facebook** | Cross-post from primary + FB-native caption | Longer caption OK, link in post |

Each derivative panel includes: full script, platform specs, caption with hashtags, description/
SEO metadata, posting instructions, and GHL keyword CTA.

### Inline Shot Direction Tags

Every script (especially the YouTube Long core asset) MUST include inline shot direction tags
embedded directly in the script text. These tell Jason (the video editor) exactly what visual
to use at each moment:

```
[TALKING HEAD] — Graeham speaking directly to camera
[B-ROLL: description of footage needed] — Overlay footage
[TEXT OVERLAY: "exact text to display"] — On-screen text/graphics
[DRONE: description of aerial shot] — Drone footage
[SCREEN RECORD: description of what to capture] — Screen recording
[TRANSITION: type] — Cut/dissolve/swipe transition
```

Place these INLINE within the script, not as a separate section. Example:
```
[TALKING HEAD] "If you own rental property in California, you need to know about AB 1482."
[TEXT OVERLAY: "AB 1482 — California Tenant Protection Act"]
[B-ROLL: California apartment complexes, rental signs]
"This law caps your annual rent increase at 5% plus CPI, or 10% — whichever is lower."
[TEXT OVERLAY: "Max Increase: 5% + CPI or 10%"]
```

### Editing Notes for Jason

Every core asset script MUST include an **Editing Notes** block — a dedicated section for the
video editor with production-specific instructions:

```
EDITING NOTES FOR JASON:
B-ROLL SHOT LIST:
- [List specific B-roll clips needed with descriptions]
- [Include stock footage suggestions if no original footage exists]

TEXT OVERLAY TIMING:
- [Timestamp] -> [Text to display] (duration: Xs)
- [Timestamp] -> [Text to display] (duration: Xs)

PACING NOTES:
- [Specific pacing instructions — fast cuts for hook, slower for education, etc.]

THUMBNAIL CONCEPT:
- [Describe the thumbnail — text, expression, background, colors]

MUSIC / SFX DIRECTION:
- [Music mood, tempo, genre suggestion]
- [Specific SFX moments — whoosh on transition, ding on stat, etc.]
```

### ElevenLabs SSML Blocks

Every core asset script MUST include a complete ElevenLabs SSML block — the full script
wrapped in `<speak>` tags with prosody and break markup so Graeham can paste it directly
into ElevenLabs for AI avatar voice generation:

```xml
<speak>
  <prosody rate="medium" pitch="medium">
    If you own rental property in California,
  </prosody>
  <break time="400ms"/>
  <prosody rate="slow" pitch="low" volume="loud">
    you need to know about AB 1482.
  </prosody>
  <break time="600ms"/>
  ...
</speak>
```

Use `<prosody>` for emphasis shifts, `<break>` for natural pauses, vary rate/pitch for
engagement. The hook should have higher energy (faster rate, higher pitch), educational
sections should be measured (medium rate), and CTAs should be emphatic (slower, louder).

### AI Video Prompts (Seedance 2.0 / Kling)

For content days that would benefit from AI-generated video (cinematic hooks, B-roll that
doesn't exist as footage, pattern-interrupt openers), include an **AI Video Prompt** block:

```
AI VIDEO PROMPT (Seedance 2.0):
SHOT: [Hook / B-Roll / Transition]
PROMPT: "Cinematic aerial drone shot of [description], golden hour lighting,
  slow dolly forward, shallow depth of field, 4K, [duration]s"
CAMERA: [Movement type — dolly, crane, orbit, static, handheld]
LIGHTING: [Golden hour / overcast / interior warm / etc.]
DURATION: [3-5 seconds typical]
USE IN EDIT: [Where this clip goes in the timeline]
```

Include 2-3 AI video prompts per content day where applicable. Focus on:
- Hook shots (first 2-3 seconds — the scroll-stopper)
- B-roll that would be expensive or impossible to film (aerials, time-lapses, cinematic establishing shots)
- Transition moments between script sections

### GHL Keyword Capture Integration

Every script CTA must include a GHL comment-keyword trigger. Current active keywords:
`SELL`, `BUY`, `COSTS`, `OPTIONS`, `1482`, `EPA`, `VALUE`, `READY`, `INVEST`, `NUMBERS`,
`RELOCATING`, `MARKET`, `CHECKLIST`, `WATCH`, `RWC`, `PA`, `MP`, `SF`

Format: "Comment [KEYWORD] below and I'll send you [lead magnet]"

### AEO (Answer Engine Optimization)

Every long-form script and blog derivative MUST include **cite-ready key statements** —
factual, data-heavy sentences that AI search engines (ChatGPT, Perplexity, Gemini) can
cite as authoritative answers. Format these as standalone declarative statements with
specific numbers, dates, or legal references.

## Production Calendar Hardening (v7.3 — Apr 2026)

The following requirements apply whenever scripts are produced as part of a V6/V7 Production Calendar. They exist to prevent three failure modes encountered in production: year-drift in on-screen text, output truncation on long-form deliverables, and week-to-week content duplication.

### Date & Year QC (mandatory self-check block)

Every prompt in `PROMPT_LIBRARY` MUST carry a `DATE & YEAR QUALITY CONTROL` block placed immediately after Fair Housing Guardrails and before Voice & Style. The block instructs the generating model to:

- Treat the calendar's publication week as the current production date (e.g., April 2026 for the Apr 20-26 calendar).
- Force every year reference — text overlays, graphic callouts, on-screen stats, captions, email subject lines — to match the production year. Never a past year unless explicitly framed as historical with clear labeling.
- Open every cite-ready / AEO statement with a date anchor ("As of April 2026...", "As of Q2 2026..."). This makes statements durable for AI search engines to cite by name months later.
- Date-stamp every price/market stat ("As of April 2026, 3-bed SFH in Woodland Park is $680K-$850K") rather than emitting bare numbers.
- Self-scan the output before emitting and fix any bare-year drift.

The v7.3 production calendar contains the exact block text — copy it verbatim when building future calendars. This QC block is required on every format (YT Long Pt 1/2, Shorts, Reels, TikTok, Carousel, Blog, GMB, Facebook, Email), not just long-form.

### Identity & Date Validation Gate (mandatory, fail-closed)

Date and DRE errors have reached deliverables before, so QC *instructions* alone are not enough. Every content package, dashboard, and automated email MUST pass a programmatic gate before it is published or sent. The gate fails closed: if any hard check fails, the content does NOT go out and a human is alerted instead.

Hard checks (block on failure):

1. **DRE number.** `01466876` is the only DRE that may appear anywhere. The known-bad DRE (the `0201`-prefixed number that has leaked repeatedly in the past; the exact blocklist value lives in `shared-references/identity.json`) must never appear in any output. If it does, BLOCK immediately.
2. **Output not empty/truncated.** Generated text must be present and of reasonable length.

Soft checks (flag for review, do not auto-block):

3. **Correct DRE present where expected.** If a caption/CTA should carry the DRE and `01466876` is absent, flag it.
4. **Date correctness.** The current date is read from the system clock at run time — never typed from memory, never inferred. Every year/date reference must match the real production date; unlabeled past-year references are a failure.
5. **Range language for perishable figures.** Any rate/price/median stated as a single hard number not verified from a live source this run must be rewritten as a range (see `references/phases/script-writer/references/data-verification-and-nuance.md`).

Manual builds: run this gate as the final step before pushing or sending, and record the result.

Automated daily email: the gate is implemented as the **Validate Date + DRE** Code node in the N8N workflow below. The date is injected from the system clock in the **Compute Today** node (never guessed), and the validation node fails closed — on failure the workflow routes to an alert to Graeham instead of sending to Peter.

## Daily Automation — Peter's Daily Email (N8N)

A weekday email to Peter is produced by the N8N workflow **"Daily Content Email — Peter (script + SSML + production)"** (instance `n8n.graehamwattsn8n.com`, workflow id `REVqxrlAb3CHJumM`). It complements the weekly dashboard: Peter can work from the dashboard OR act straight from the email.

Flow: Schedule (Mon-Fri 6:00 AM PT) → CONFIG (`peter_email`, `cc_email`, `dashboard_url`) → Compute Today (system date → topic t1..t5, Mon=t1) → Fetch Dashboard HTML (the live weekly calendar is the single source of truth) → Parse Topic (pulls that day's `prod_script` + `prod_video` out of `COPY_DATA`) → Generate (OpenAI runs both prompts: script + SSML, then production assets) → Validate Date + DRE (fail-closed gate above) → IF passed → Email Peter (dashboard link + the day's full package); ELSE → Alert Graeham.

Operational notes:

- The workflow reads the LIVE published dashboard, so a corrected or new dashboard must be pushed to GitHub Pages before its content reaches the email.
- Update `CONFIG.dashboard_url` whenever a new week's dashboard is published; set `CONFIG.peter_email` once.
- Model is `gpt-4o-mini` for free-credit reliability; swap to `gpt-4o` or a paid key for higher script quality.
- Figures use range language; the script's "Verify before recording" block tells the human exactly which live numbers to confirm before shooting.

### Output Split Strategy (YouTube Long only)

A single YouTube Long prompt requesting 6 deliverables (Script + SSML + Editing Notes + AI Video Prompts + YouTube SEO Package + 3 Alt Hooks) produces roughly 40K-60K chars of output, which exceeds default `max_tokens` on most consumer AI tools and causes the model to truncate mid-Deliverable 4.

Split YouTube Long prompts into TWO buttons:

- **Pt 1 — Script + Voice** → Deliverables 1 (full timestamped script with inline shot tags) + 2 (complete ElevenLabs SSML block). Target output ~20-25K chars, fits in one response on any tool.
- **Pt 2 — Production Package** → Deliverables 3 (Editing Notes for Jason) + 4 (AI Video Prompts) + 5 (YouTube SEO Package) + 6 (3 Alt Hooks for A/B testing). Target output ~20-25K chars. Includes the standard 5-minute structure reference (hook / problem / core1 / core2 / advisory / CTA) so the production package works without pasting the script back in.

Both parts share the same preamble (Agent Identity + Fair Housing + DATE/YEAR QC + Voice + Topic + Funnel Tier + AEO + Key Facts + GHL Lead Capture). Only the deliverable list and output-mode header differ.

Short-form formats (YT Shorts, IG Reels, TikTok, Carousel, Blog, GMB, Facebook, Email newsletter) do NOT need splitting — their single output fits comfortably in one response.

### Week-over-Week Overlap Check (mandatory pre-ship)

Before shipping each weekly calendar, run an overlap comparison against the immediately preceding week's calendar. For each of the 5 daily topics plus the email newsletter, compare against the prior week's topics on:

- **Title** — substring match or semantic overlap (e.g., "EPA Homes Under $700K" vs "EPA Homes Under $1M" = HIGH overlap)
- **Slug** — exact or near-exact match
- **Neighborhood** — repeated primary-market focus on consecutive days
- **Funnel tier** — consecutive weeks of same tier + same topic cluster
- **GHL keyword** — keyword reuse across weeks

Classify each match as HIGH / MODERATE / LOW risk. Write a markdown comparison note (`YYYY-MM-DD-vs-PRIOR-content-overlap-check.md`) alongside the calendar HTML in `online-content/dashboards/weekly-calendars/` and commit it to the repo. HIGH-risk overlaps MUST be resolved before shipping — reframe the angle, replace the topic, or defer a week.

**Future systematization**: add a `TOPIC_HISTORY` object to the calendar HTML containing the last 4 weeks of (title, slug, neighborhood, tier, ghl_keyword) tuples. Future calendar generation runs an automatic pre-publish check against that history and flags overlaps without a manual pass.


## Examples

Three worked examples live in `examples/`:
- `example-1-bofu-trigger-event-tech-layoff.md` — BOFU response to a tech layoff trigger event
- `example-2-tofu-lifestyle-reel-epa-tacos.md` — TOFU lifestyle reel (East Palo Alto tacos)
- `example-3-aeo-legal-education-ab1482.md` — AEO-optimized legal education on AB 1482

Read these before writing new content packages — they show the expected output format and voice.

## Example Prompts

**Per-topic (this skill):**
- "Build a content package on the EPA homicide-free story" → Phase 0a (confirm topic) → Per-Topic Research (pull topic-matched research) → Phase G (build package)
- "I just got a new listing in Menlo Park at $2.1M — give me the full content package" → Per-Topic Research (the listing IS the topic) → Phase G
- "Make me a TOFU reel about East Palo Alto lifestyle"
- "Generate 5 BOFU videos about AB 1482 for Bay Area landlords"
- "Hey I saw this video, can we do something like this? https://youtube.com/watch?v=..." → Phase 0 (ingestion) → Per-Topic Research → Phase G
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
- **Supplementary:** Windsor MCP for Instagram, YouTube, Facebook, Search Console, and Apify scraper performance data.
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

After generating the topic-production dashboard HTML output, publish via Composio to `Graehamwatts/online-content` so the agent gets a permanent hosted URL.

**Account:** `github_spar-devata`  
**Owner:** `Graehamwatts`  
**Repo:** `online-content`  
**Branch:** `main`  
**Path pattern:** `dashboards/single-topic/YYYY-MM-DD-slug-production.html`  
**Hosted URL pattern:** `https://graehamwatts.github.io/online-content/dashboards/single-topic/YYYY-MM-DD-slug-production.html`

**Tool to use:** `GITHUB_COMMIT_MULTIPLE_FILES` (atomic commit, retry-safe).

```python
result, error = run_composio_tool(
    tool_slug='GITHUB_COMMIT_MULTIPLE_FILES',
    arguments={
        'owner': 'Graehamwatts',
        'repo': 'online-content',
        'branch': 'main',
        'message': 'descriptive commit message',
        'upserts': [{'path': 'dashboards/single-topic/YYYY-MM-DD-slug-production.html', 'content': html_content, 'encoding': 'utf-8'}]
    },
    account='github_spar-devata'
)
```

**HARD RULES:**
- Do NOT use the legacy GitHub Contents API with PAT or `javascript_tool` chunked uploads (replaced 2026-05-03).
- Do NOT use GitHub Desktop or `git push` from the agent sandbox.
- Run the brand-integrity check before push (see shared doc — blocks DRE# 01 leaks).
- After commit, give the user BOTH the hosted URL and the local `computer://` link.

See `shared-references/publishing-via-composio.md` for full details, common pitfalls, and verification flow.


## Canonical Weekly Calendar Template (v5.4 — locked in May 2026)

> **This is the format moving forward.** Live reference: [`Graehamwatts/online-content/dashboards/weekly-calendars/2026-05-11-production-calendar.html`](https://github.com/Graehamwatts/online-content/blob/main/dashboards/weekly-calendars/2026-05-11-production-calendar.html). Hosted at: https://graehamwatts.github.io/online-content/dashboards/weekly-calendars/YYYY-MM-DD-production-calendar.html

**Template structure (top to bottom):**

1. **Hero** — week date range, opportunity-score pill chips, BOFU mix label.
2. **Audience tabs** (sticky) — Research / Blog Track / Peter / Show Everything. Tab state persists in URL hash (`#audience-blog`, `#audience-peter`).
3. **Preview banner** — explains v5 features + auto-refresh time.
4. **Live Data Layer** — 8 source cards (Composio IG, Composio YT, DataForSEO, n8n Local News, GSC via Windsor, Reddit via Apify, YT Comment Mining, Zillow Q&A).
5. **Full Research Data panel** (collapsed by default; toggle to expand):
   a. **Brushable time-series charts** (ApexCharts via CDN):
      - Instagram Activity Over Time (weekly likes + posts, dual axis, drag bottom slider to zoom)
      - YouTube Activity Over Time (weekly views + videos, dual axis, drag bottom slider to zoom)
      - Engagement Rate Per Post Per Week (avg per-piece for IG + YT)
   b. Instagram 25/100-row table (live via Composio Meta Graph API)
   c. YouTube 15/50-video table with stats (live via YouTube Data API v3)
   d. GSC topic-targeted queries
   e. Reddit demand signals
   f. Zillow Q&A
   g. MLS pull
   h. Macro Rates & Permits
   i. DataForSEO SERP queue status
   j. Convergence — Why each day picked (with source counts and scores)
6. **5 Day Cards (week grid)** — clickable to filter Blog Track + Peter sections to one day.
7. **Weekly Strategy** — funnel mix bar + cross-platform handoff notes.
8. **Blog Track section** — 5 daily-items, each with prominent topic title + hook + format pill rows. Pills copy Claude-ready prompts.
9. **Peter section** — same pattern, video formats, with Image-Gen pills for carousels.
10. **Footer** — DRE 01466876, contact, refresh schedule, Composio commit reference.

**Hard rules (don't drift from this):**

- **Brand identity** — pull from `shared-references/identity.json`. Run the blocklist verifier before every push (see `scripts/verify_brand_identity.py` and `shared-refer