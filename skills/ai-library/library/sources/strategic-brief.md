# Jason Pantana's AI Marketing Academy — Strategic Brief

**Prepared for:** Graeham Watts
**Date:** May 13, 2026
**Scope:** Full deep dive of jasonpantana.com/AiM library, lectures, lessons, and Cowork agents. Cross-referenced against Graeham's 29 installed skills. Adoption roadmap included.

---

## Executive Summary

Pantana's AiM is built on the same Claude Cowork foundation you already use — desktop agents, skills, MCP connectors, scheduled runs. He's further along on **research depth, AEO (answer-engine optimization), and structured BOFU pipelines**; you are further along on **transactional real-estate tooling, motion graphics, voice/template-locked content production, and Bay-Area-specific market knowledge**.

The honest call: there are **4 high-value gaps** worth closing, **2 patterns worth stealing into your existing skills**, and a long list of stuff you already do better. None of this is "tear down and rebuild." It's an opportunistic upgrade.

**Top recommendations (start here):**

1. **Build a BOFU Research Engine skill modeled on his 6-phase pipeline.** Your `video-script-creation-engine` already does Reddit/Apify ideation, but his 230+ localized queries × 9-platform × 5-dimension scoring is more rigorous. Borrow the architecture; localize for East Palo Alto/Peninsula.
2. **Adopt the AI Recommendation Playbook as a Watts-branded AEO skill.** No equivalent exists in your library. This is the highest-leverage gap — directly drives inbound from ChatGPT/Perplexity/Google AI Overview citations.
3. **Add a Schema Markup + Specialization Pages skill.** Both are referenced as separate AiM library items. You have nothing on schema/JSON-LD or AEO-shaped landing pages.
4. **Build a "Brand Style Guide" master skill.** Your voice/brand is currently embedded inside 5+ skills. Pantana's pattern of one Brand Style Guide skill that the others reference is cleaner and would save you maintenance time.

The full matrix and roadmap are below.

---

## Part 1 — What Pantana Has Built

### 1.1 The AiM Library (72 resources, 4 categories)

| Category | Count | Examples |
|---|---|---|
| Bots (Cowork agents, GPTs, Gems) | ~22 | BOFU Video Engine, Cowork Avatar Agent, Talking Head Video Editor, 15 Custom GPTs Pack |
| Prompts (paste-and-go) | ~26 | CRM Database Health Audit, AI Recommendation Playbook, Real Estate Listing Description |
| Guides (how-to docs) | ~20 | Claude Skills Agent Starter Pack, Specialization Pages for Answer Engines, Glossary of AiM and AI Terms |
| Videos (lecture clips) | ~4 | Run Search Ads in Google AI Overviews, Sync New Leads to Meta Ads |

Full inventory saved to `aim_library_inventory.md` in your outputs folder.

### 1.2 The Live Curriculum

**Lectures (monthly, two tracks):** Ai Rookies (foundational) and Ai Rockstars (advanced). Recent topics include Content Creator Agents (BOFU pipeline), NotebookLM Client Playbook, Teach Claude Your Business, Hiring Your First Desktop Agent, AI Recommendation Engine, Instagram Carousel AI Generator, AI Walkthrough Workflow.

**Labs (monthly, two tracks):** Hands-on companions to the lectures.

**Lessons (bonus webinars):** CRM Database Health Audit, BOFU Blogger Rebuilt for Cowork, Smarter Lead Magnets with AI, NotebookLM: Smarter AI Tools, Managing AI-Informed Clients, AI Doesn't Rank It Recommends, Zillow-ChatGPT Apps SDK.

**Prompt Studio:** Separate authenticated app at `apps.aimarketingacademy.com/apps/prompt-studio/chat` with community-shared prompts. Gated behind a second SSO login I did not access — flag for follow-up if you want me to crawl it.

### 1.3 The BOFU Pipeline (Pantana's Marquee Architecture)

Pantana has built a tight 3-agent pipeline that mirrors what your `video-script-creation-engine` + `heygen-video` already do — but with much sharper separation of concerns:

**Agent 1 — BOFU Video Engine (research):**
- 1 Claude.md system prompt + 2 skills (`bofu-query-generator`, `bofu-scorer`) + 1 market-config.md
- 6 phases: query generation (230+ localized queries) → search (9 platforms: Google, YouTube, Reddit, Zillow, Realtor.com, Redfin, BiggerPockets, City-Data, Nextdoor, NerdWallet) → Reddit/YouTube deep-dives → score on 5 dimensions (inquiry type, decision-stage intent, source confirmation, emotional urgency, local relevance) → format 7–10 ranked ideas with hooks + CTAs → deduplicate vs. prior runs
- Fair Housing guardrails baked in
- Focus on **process questions** ("how much are closing costs") and **property questions** ("new construction in [neighborhood]") — both decision-stage, not browsing

**Agent 2 — Automated BOFU Blogger (text):**
- Reuses the same query-generator + scorer skills, plus an `aim-bofu-blog-writer` skill personalized per agent
- Scans your existing blog first (avoids duplicate posts), writes a complete SEO/AEO-optimized post with snippet summary, FAQ, JSON-LD schema, internal links, CTA
- Outputs HTML + Markdown + optional Google Doc / CMS connector draft / Chrome-driven WordPress draft
- Notifies via iMessage / Slack / Zapier

**Agent 3 — Cowork Avatar Agent (video):**
- Uses **HeyGen MCP connector** at `https://mcp.heygen.com/mcp/v1` (worth noting — your `heygen-video` skill may be using a different API path)
- Two script skills: Reel Script Writer (30–60s) + YouTube Script Writer (5–8 min)
- Built-in **Data Integrity Gate** — won't write stats it can't verify
- Pulls topics from BOFU Video Engine output → writes scripts → routes to HeyGen → returns video

**Bonus — Talking Head Video Editor:**
- Uses **Descript MCP** at `https://api.descript.com/v2/mcp` to drive Descript's Underlord AI editor
- Auto rough-cut, script verification, filler-word removal, branded captions with active-word highlight, zoom cuts, intro/outro fades, reframe, export
- ~11–14 Descript AI credits per edit

### 1.4 The 9-Skill Starter Pack

Pantana's onboarding gives every member 9 paid-tier skills, all personalized via one intake conversation:

1. **Brand Style Guide** — master skill, every other skill references it
2. **Listing Remarks Writer** — noun-dense AEO-optimized public remarks
3. **Listing Photo Captioner** — vision model identifies rooms + writes MLS captions, batch up to 10
4. **MLS Data Analyzer** — comp logic, deal-killers, leading data points
5. **Price Reduction Angle Generator** — strategic vs. desperate positioning + 3–4 supporting data points
6. **Instagram Caption Writer** — feed posts and carousels (not video)
7. **Reel Script Writer** — 30–60s teleprompter-ready
8. **Email Newsletter Writer** — ESP-aware (Mailchimp, Flodesk, etc.)
9. **Blog Post Writer** — TOFU/MOFU/BOFU classifier + AEO snippet structure

### 1.5 The AI Recommendation Playbook (AEO Strategy)

This is the single most strategic prompt in his library. Not an agent — a 4-step playbook:

1. **Be on the sites AI cites.** Owned (your site, brokerage profile) + Listicles (Zillow, Realtor.com, Redfin, FastExpert, HomeLight, RealTrends, Rate-My-Agent, Yelp) + Social (YouTube, LinkedIn, Reddit, Facebook groups) + Local sites.
2. **Engineer every profile.** City + neighborhood + niche + credentials + specific differentiators + reviews that name city/situation/outcome.
3. **Publish proof pages.** "Best/Top/Vs" content shaped for AI citation — clear answer in paragraph 1, question-shaped H2/H3, lists, named city throughout, JSON-LD where possible.
4. **Underdog channels.** Reddit (use `realtor recommendation, [CITY], site:reddit.com OR site:facebook.com` Google hack), Facebook groups, talking-head YouTube with clean transcripts + descriptive chapter markers + AI-snippet description (NOT listing tours — those don't get cited), Instagram comments (now being scanned by AI), LinkedIn articles as proof-page substitute.

Core insight he hammers: **AI does live search + fetch when answering "who's the best agent in X" — it doesn't answer from memory.** Your job is to win at both layers (search-result snippet + on-page content). Comments are the new reviews because AI is lazy — it won't read 800 Zillow reviews, but it will quote a Reddit thread that names you.

---

## Part 2 — Cross-Reference: Pantana vs. Graeham

### 2.1 What You Already Do as Well or Better

| Pantana | Your equivalent | Verdict |
|---|---|---|
| Cowork Avatar Agent (HeyGen pipeline) | `heygen-video` + `vaibhav-template` | **You're sharper.** Vaibhav template is brand-locked, scriptable, with a 5-look rotation. Pantana's is more generic. |
| Talking Head Video Editor (Descript) | `watts-motion-graphics` + manual CapCut | **Different tools.** Pantana uses Descript Underlord; you use Remotion overlays + CapCut. Both valid. His approach is more automated, yours is more brand-controlled. See section 2.3. |
| CRM Database Health Audit | `ghl-crm-audit` | **You're sharper.** Yours is GoHighLevel-specific with N8N automation builder. His is generic CSV-in/Word-out. |
| Reel Script Writer | `video-script-creation-engine` + `cinematic-hooks` | **You're broader.** Yours has Reddit ideation, content pillar scoring, hook engine. His is leaner but less localized. |
| 15 Custom GPTs starter pack | `skill-creator` + your 29 installed skills | **You're way ahead.** Your skill library + GitHub sync workflow is more mature. |
| Listing Description / Listing Photo Captioner | None — but you have `cma-generator` for pricing | **Tied.** Different lanes. (See gap #5 below.) |
| Marketing Plan Builder | `content-calendar` + `social-media-analyzer` | **You're sharper.** Yours cross-references social performance + Search Console + competitor data; his is a one-shot ChatGPT conversation. |
| Listing Performance Report, Sales Scoreboard, Year-End Recap Infographic | `cma-generator` + `xlsx` | **Tied.** Your CMA covers most of this; his are pre-built HTML widget templates. Worth borrowing the Year-End Recap concept (see gap #6). |
| Higgsfield equivalent | `higgsfield-video` | **You're the only one.** Pantana has no AI b-roll system. |
| Branded HTML email | `html-email` | **You're sharper.** Yours hosts on GitHub Pages; his are file-only. |

### 2.2 Real Gaps Worth Closing

These are categories where you have **nothing** and his system is fundamentally a different capability.

| # | Gap | Pantana's version | What it would mean for you |
|---|---|---|---|
| **1** | **Structured BOFU research pipeline** | BOFU Video Engine (230+ queries, 9 platforms, 5-dim scoring, 6 phases, Fair Housing) | A `bofu-research-engine` skill that produces ranked, sourced topic lists for the Peninsula. Feeds `video-script-creation-engine` and a future blog writer. |
| **2** | **AEO / AI Recommendation strategy** | AI Recommendation Playbook + Specialization Pages for Answer Engines + Optimize Your Bio for AI Search | A `watts-aeo-engine` skill that audits your citations across ChatGPT/Perplexity/Google AI Overview, generates proof pages and specialization pages, drafts coached-review scripts. Highest ROI in this list. |
| **3** | **Schema markup / JSON-LD for listings + author/E-E-A-T** | Schema Markup for Real Estate Listings (prompt) | A `schema-builder` skill that emits valid JSON-LD for listings (RealEstateListing), author bios (Person + jobTitle + alumniOf), and proof pages (Article + author + publisher). Cheap to build, big AEO compounding benefit. |
| **4** | **Brand Style Guide master skill** | Brand Style Guide skill that every other skill references | One `watts-brand-style-guide` skill containing voice/colors/fonts/tone/signoff/audience. Refactor existing skills to reference it. Reduces drift, easier to update. |
| **5** | **Listing Remarks + Listing Photo Captioner** | Two separate skills | A `listing-remarks-writer` (noun-dense, AEO-tuned for Zillow + ChatGPT Apps SDK) and `listing-photo-captioner` (vision → MLS captions, compliant). You're a listing agent — this is core. |
| **6** | **Year-End Recap Infographic + Seller Performance Dashboard** | Two prompts that emit branded interactive HTML | Optional. Worth adding to `cma-generator` as output modes rather than separate skills. |
| **7** | **NotebookLM-based client resource libraries** | Build a Client Resource Library with NotebookLM (guide) + April Rookies Lab | A workflow doc / `notebooklm-builder` skill that converts your existing content into 4–5 NotebookLM notebooks per client persona (buyer, seller, relocation, EPA-specific). Differentiator. |
| **8** | **AI Walkthrough Workflow** (still photos → video tour with avatar overlay) | January Rockstars Lecture + library guide | Could pair with `higgsfield-video` + `heygen-video` to assemble. Worth experimenting if you list properties without good video budget. |

### 2.3 Patterns Worth Borrowing Into Existing Skills

Don't build new skills — upgrade what you have.

- **Data Integrity Gate** (from Cowork Avatar Agent). Add to `video-script-creation-engine` and `heygen-video`: if a script claims a stat, the agent must surface the source URL or pause. Cheap insurance against hallucinated DOM/days-on-market/median-price numbers.
- **Two-stage delivery pattern** (intake conversation → personalized skill files + kickoff prompt). His agents follow `intake.md → skill-template.md → personalized-skill.md + market-config.md + kickoff-prompt`. Adopt this pattern in `skill-creator` so new skills auto-generate a kickoff prompt and a market config. You already have github-skill-sync — pair these.
- **Folder convention** (Claude.md in task root, references/ subfolder, skills in library). Pantana uses this consistently. Codify in your skills as a one-paragraph "How to deploy this" section.
- **HeyGen MCP** at `https://mcp.heygen.com/mcp/v1`. Check whether your current `heygen-video` skill uses direct API or the MCP. The MCP gives you native Cowork tool calls (cleaner) vs. API key management.
- **Descript MCP** at `https://api.descript.com/v2/mcp`. If you decide to add Descript-based editing as an alternative to Remotion, this is the connector URL. Both can coexist — Remotion for branded chroma-key overlays, Descript for the rough-cut/captions pass.

### 2.4 Things You Can Safely Ignore

- **15 Custom GPTs Every Real Estate Agent Should Build** — generic, outdated framing; your skill library beats GPTs for any task that touches files.
- **Personalized Video Script Generator, Title Influencer Reel Script Generator** — your video-script-creation-engine + vaibhav-template are more specialized.
- **Plain-Text Email Newsletter Generator** — your real estate transactions don't need plain-text; HTML wins.
- **Marketing Plan Builder Prompt** — your `content-calendar` is the real planner.
- **Zillow ChatGPT Branded Email Announcement** — one-shot tactical email; not worth a permanent skill.
- **How to Personalize Your ChatGPT Account / How to Create a Custom GPT / When to Use GPTs vs. Projects** — foundational guides, not assets.
- **Prompting Best Practices / 7 Magic Phrases / 10 Formatting Tips** — read once, internalize, move on.

---

## Part 3 — Adoption Roadmap

Prioritized by impact ÷ effort. Each item sized for your skill-creator + github-skill-sync workflow.

### Tier 1 — Build in the next 2 weeks (highest leverage)

| Priority | Skill | Effort | Impact | Why now |
|---|---|---|---|---|
| 1 | `watts-aeo-engine` (AI Recommendation Playbook adapted) | 6–8 hrs | **Massive** | The "Goldilocks moment" Pantana names is real. Every week you wait, another EPA/Peninsula agent passes you in citations. Test prompt today: ask ChatGPT and Perplexity "Who's the best real estate agent in East Palo Alto?" |
| 2 | `bofu-research-engine` (his 6-phase pipeline, localized) | 8–10 hrs | **High** | Feeds video-script-creation-engine and a future blog writer. Decision-stage queries are where AI-driven traffic converts 10–23×. |
| 3 | `watts-brand-style-guide` (master skill) | 2–3 hrs | **Medium-high** | Refactor pays back the moment you add a 30th skill. Lock voice, colors, tagline, signoff, audience. Then update other skills to read from it. |

### Tier 2 — Build over the next 30 days

| Priority | Skill | Effort | Impact | Notes |
|---|---|---|---|---|
| 4 | `schema-builder` (JSON-LD for listings, bio, proof pages) | 3–4 hrs | High | Pairs with watts-aeo-engine. Cheap. Compounds. |
| 5 | `listing-remarks-writer` (noun-dense, AEO-tuned) | 3–4 hrs | High | You list. This should already exist. |
| 6 | `listing-photo-captioner` (vision → MLS-compliant captions) | 2–3 hrs | Medium | Use Claude's vision; batch up to 10 photos. |
| 7 | Upgrade `video-script-creation-engine` + `heygen-video` with Data Integrity Gate | 2 hrs | Medium-high | Prevents hallucinated stats in BOFU content. |
| 8 | Audit `heygen-video` for HeyGen MCP vs. API approach | 1 hr | Low-medium | If MCP is cleaner, refactor. |

### Tier 3 — Build when you have a quiet week

| Priority | Skill | Effort | Impact | Notes |
|---|---|---|---|---|
| 9 | `notebooklm-builder` (or workflow doc) | 4–6 hrs | Medium | Strong client-nurture differentiator. Watch his April Rookies lecture first. |
| 10 | Add Year-End Recap + Seller Dashboard output modes to `cma-generator` | 2 hrs | Low-medium | Marginal — your cma-generator is already strong. |
| 11 | Optional: `descript-editor` skill (Descript MCP-driven) | 4 hrs | Low | Only if you find yourself doing rough-cut work that Remotion + CapCut don't cover. |

### Tier 4 — Watch but don't build yet

| Topic | Why hold |
|---|---|
| AI Walkthrough Workflow | Niche; your higgsfield-video covers most of it. Revisit if you list a property without good listing video. |
| Custom GPTs / Gemini Gems pack | Your Claude skills win; don't dilute. |
| Specialization Pages (separate from watts-aeo-engine) | Roll into watts-aeo-engine instead of standalone. |

---

## Part 4 — Open Questions for You

1. **Prompt Studio access.** It's a separate SSO login. Want me to come back and crawl the community-shared prompts there? Could yield 5–20 more candidate ideas. (Requires your permission for SSO.)
2. **Lecture transcripts.** The lectures (Content Creator Agents, AI Recommendation Engine, Hiring Your First Desktop Agent) contain the "why" behind the library assets. Want me to grab the transcripts of the top 3 you haven't watched and summarize them? ~10 min per lecture.
3. **East Palo Alto / Peninsula localization data.** When we build the BOFU research engine, I'll need: your top 5 sub-markets, your closing entity (CA = escrow company), your standard disclosures (TDS, SPQ, AVID — which you already have a skill for), and your top hyper-local hot topics (e.g., Meta HQ moves, Facebook/East Bayshore traffic, the Ravenswood school district situation). Want me to draft a market-config.md based on what I can infer from your existing skills?
4. **GitHub backup of new skills.** Your github-skill-sync auto-pushes after every skill modification. Confirm we want all new Tier 1/2 skills pushed to `Graehamwatts/skills` on creation.

---

## Sources

- [AiM Library](https://aimarketingacademy.com/library/) — 72 resources catalogued
- [BOFU Video Engine](https://aimarketingacademy.com/library/bofu-video-engine-claude-cowork-agent/)
- [Automated BOFU Blogger — Cowork Agent](https://aimarketingacademy.com/library/automated-bofu-blogger-cowork-agent/)
- [Cowork Avatar Agent](https://aimarketingacademy.com/library/cowork-avatar-agent/)
- [Talking Head Video Editor AI Agent](https://aimarketingacademy.com/library/talking-head-video-editor-ai-agent/)
- [Claude Skills Agent Starter Pack](https://aimarketingacademy.com/library/claude-skills-agent-starter-pack/)
- [AI Recommendation Playbook](https://aimarketingacademy.com/library/ai-recommendation-playbook/)
- [Dashboard / Lectures index](https://aimarketingacademy.com/dashboard/)
