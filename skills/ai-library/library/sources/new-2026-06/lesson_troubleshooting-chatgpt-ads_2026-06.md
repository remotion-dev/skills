# New AiM Library Item — captured 2026-06-27

## Lesson: Troubleshooting ChatGPT Ad Campaigns
- URL: https://aimarketingacademy.com/lessons/troubleshooting-chatgpt-ad-campaigns/
- Type: Lesson (bonus deep-dive) — "AI Rockstars" tier
- Published: June 2026
- Format: ~62-min recorded webinar (Vimeo 1205113489). Transcript backed up to Obsidian: `06 Coaching & Training/Jason Pantana/`.
- Relationship: This is **"round two"** — the post-launch *troubleshooting* companion to the May build-side items already in the library (`Bulk-Build ChatGPT Ads with an AI Agent` + `ChatGPT Ads Context Hint Library`). The May items teach you to BUILD; this teaches you to FIX a live campaign.

### What This Is
A live, casual troubleshooting session for agents who already launched ChatGPT Ads and are seeing inconsistent results (lots of "impressions, no clicks"). Pantana diagnoses the common failure modes, corrects bid/budget guidance, surfaces new platform behavior, and does live landing-page audits of members' pages.

### Noteworthy / net-new vs. the May build-side material

**Bid + budget (changed guidance):**
- OpenAI lowered the max-CPC floor to ~$4; Pantana now recommends bidding **~$7–8** to win impressions (supersedes the old "$3–5").
- **Budget is a ceiling, not a charge.** Almost nobody's budget is being utilized ($200 cap → $4 spent; $600 → $86). On the Clicks objective you only pay per click.
- Behaves like Google Local Service Ads — allocated budget far exceeds available volume.

**The diagnostic decision tree:**
- Flatlining → delete & rebuild, or raise budget.
- Impressions, no clicks → raise max bid and/or fix the offer (headline + image).
- Clicks, no conversions → the landing page isn't a "catcher's mitt."

**Platform facts that shifted (June 2026):**
- Start/end dates removed — campaigns run until budget total is spent.
- Account must be a **Business** (Individual is blocked); needs EIN-type ID.
- **Financial-services ads get flagged/auto-disabled** — the "pre-approved buyer" context hint (#15) was shut off in tests. Mortgage/lender ads will struggle.
- Conversions pixel tracking is unreliable right now — use the Clicks objective.

**Strategy:**
- 95%+ of ChatGPT's ~1B users are free/Go and **only they see ads**; free = non-reasoning search, Plus = agentic search. Test in incognito.
- realestateagents.com / My Agent Finder dominate generic "best realtor" queries — **beat them by getting hyper-specific at the ad-group level.**
- Win **organic + paid together** ("fire + gasoline"); aim for citation share, not winning every refresh.
- Image = headshot. Headline must crush (ads truncate — front-load).

**New organic signal — Yelp × ChatGPT data-licensing deal:**
- A Yelp map-pack now appears in nearly every real-estate ChatGPT thread, sometimes as the only source. Get Yelp reviews; prioritize the Yelp profile. (Answer-engine signal, broader than ads.)

**Landing-page standard:**
- The page is the "catcher's mitt" — BOFU, one primary CTA restated, contact visible, headshot, fast/mobile, no forced registration. Use Donald Miller's "Marketing Made Simple" wireframe for page order.

### Where this landed in the toolkit
- Built into the `chatgpt-ads` skill as `references/troubleshooting.md`; SKILL.md bid guidance + financial-services flag updated 2026-06-27.
- Heuristics to fold into PropIQ → PropReach **Part 17 (ChatGPT Ads Channel)**.
- Yelp signal flagged for `seo-optimizer` / GBP-reputation.

> TODO (Phase 2): regenerate `ai-library.html` / `archive_data.json` / `summaries.json` to include this lesson once the full Pantana-folder scan is done.
