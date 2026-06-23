---
name: newsletter-generator
description: "Weekly newsletter generator for Graeham Watts (REALTOR, Intero Real Estate, DRE# 01466876). Produces per-segment PERSONALIZED, brand-matched, multi-section email newsletters (The EPA Report) assembling a lead story + market update + community news + featured content + home-value CTA that ties into the cma-generator skill. Use ANY time the user mentions: newsletter, weekly newsletter, weekly email, email blast, subscriber email, EPA Report, weekly digest, send a newsletter, generate newsletter, assemble newsletter, newsletter HTML, email-ready newsletter, Gmail newsletter, multi-section email, or turning a single topic content package into a full newsletter. Also trigger when the user says 'send out the newsletter this week', 'prep the email for Friday', or 'package the content as a full weekly email'. Pairs with content-creation-engine (which generates the per-topic content) and cma-generator (which the What's My Home Worth CTA handoff targets)."
---

# Newsletter Generator — The EPA Report

> **What this skill is:** The final assembly layer that stitches multiple content sections into a complete weekly newsletter ready to paste into Gmail (or send via Gmail API). Ties the content-creation-engine's topic packages to the cma-generator's valuation handoff.

## Personalized Per-Segment Architecture (v3 — added 2026-06-22)

> Upgrades the newsletter from one generic blast to a per-segment, per-audience, brand-matched assembly. Canonical spec: the Wattson `past-client-monthly-newsletter` playbook. Grounded in the 4-video research library (Obsidian: `Newsletter Videos for Realtors`). First built file: `online-content/newsletters/2026-07-the-epa-report.html`.

**Cadence.** Monthly, prepped ~1 week before the start of each month (the 24th–25th PCFS window). Past-client nurture floor, not weekly. Each month: gather content (scan the video pipeline + content-calendar; ping Peter / Adrian / Graeham if a topic is needed) → assemble per segment → humanizer → brand + Fair Housing check → Peter reviews → Adrian sends via GoHighLevel.

**Audience.** Active past clients from GoHighLevel / PCFS, grouped by market segment (EPA, San Jose, Santa Clara, Campbell, out-of-area).

**Module library + rotation.** The newsletter is a MENU of modules, not all-at-once. Send ~5–6 per month and rotate the rest so any single email stays skimmable (the #1 lesson from the research videos: shorter converts better). Modules: hero video · home-value CTA (the ONE hero CTA, every send) · market snapshot · local news strip · "heads up" reframe item · testimonial · secondary ask (referral OR schedule, rotate one).

**Three layers per recipient.** A — Universal (lead video, broad CA + national market + rates, one optional non-RE "interesting" item, the single primary CTA). B — Local block, swapped per segment (that city's stat card + local news/dev from the intelligence layer; degradation ladder: market video → stat card + chart → curated local news → Bay Area/CA fallback; never empty). C — Personal (greeting by name + optional equity/anniversary hook).

**Two-axis personalization.** Location (which city's block) × audience intent (homeowner / investor / buyer reframing of the same story, e.g. rent control framed three ways).

**Content-matching layer.** Before each send, scan the agent's PUBLISHED library (YouTube, Instagram Reels, blog — via content-calendar / content-creation-engine / the video pipeline) and match best-fit pieces per segment. Universal lead video for everyone + a "picked for you" secondary that changes. Never re-host; link out (animated GIF first-frame → links to the hosted video).

**Testimonial module.** Auto-insert the newest testimonial from an allow-listed source (Google / Zillow); omit the block if nothing fresh. Never fabricate.

**Per-agent brand skin (multi-tenant).** The structural template is SHARED; the skin is per-agent. Each agent's Brand Vault (colors, fonts, logo) is derived from their website (Search Atlas Website Studio model). PropertyIQ's own product brand is never used on the client newsletter. Pilot instance = Graeham's gold/black Intero brand (gold `#C2A14E`, ink `#1A1D2E`, Anton + Inter, DRE 01466876 from `identity.json`). These colors are the pilot's brand, not a locked product palette.

**Every link is a Switchy tracked link** (UTM + retargeting pixel) via the `switchy-engine` skill, so the analytics loop (review last sends, learn what gets clicked) actually works.

**Design rules (from the research library).** Curiosity subject line, generate 2–3 A/B variants (autocomplete-researched) per send · 90% value / 10% promotion · ONE primary CTA · short + skimmable, tease then click out · real photos, not stock · video up top · consistent template · list hygiene (handled in PCFS / GHL).

**Humanizer pass is mandatory** on all prose before send (no em dashes, no AI tells, first-person warm voice). See the Humanizer Final Pass section below.

**Output.** Email-safe HTML (table-based, inline styles) published to the `online-content` repo at `/newsletters/`, hosted 24/7 with a view-in-browser link; sent via GoHighLevel.

**Ties into content-creation-engine + content-calendar** (they decide and produce the per-topic content; this skill assembles the monthly newsletter from that library + the intelligence layer). The PCFS dashboard (PropFlow / `propiq-ui`) is a separate build.

## Agent Identity

Graeham Watts — REALTOR at Intero Real Estate, DRE #01466876. Bay Area real estate specialist, East Palo Alto home base. The weekly newsletter is branded **"The EPA Report"** — sent to his subscriber list every Friday/Saturday.

## Scope Boundary (Who Owns What)

| Layer | Skill | What it does |
|-------|-------|--------------|
| **Per-topic content** | `content-creation-engine` | Generates the script, blog, captions, social posts for ONE topic |
| **Newsletter assembly** (this skill) | `newsletter-generator` | Takes 1+ topics and assembles a complete weekly newsletter HTML |
| **Home value handoff** | `cma-generator` | The "What's My Home Worth?" CTA ultimately triggers this when a user submits their address |
| **Weekly planning** | `content-calendar` | Decides WHICH topics go into the week (not this skill's job) |

## The 7 Required Sections

Every newsletter MUST include these sections in this exact order:

1. **Header & Brand Banner** — Logo, "The EPA Report" title, issue date
2. **Lead Story** — Primary topic from content-creation-engine (hook + 200-word excerpt + "Watch the full video" CTA linking to YouTube)
3. **Market Update Cards** — 4-6 stat cards pulled from this week's MLS data (EPA median YoY, DOM, SMC comparison, rates, etc.)
4. **Community & Development** — 2-3 bullets from local news / city government (e.g., April 17 milestone, Woodland Park 772 units, Flock camera council meeting)
5. **Featured Content Deep Dive** — Inline video thumbnail + blog post teaser
6. **"What's My Home Worth?" CTA Block** — Large gold button that triggers the CMA handoff (see next section)
7. **Footer** — Contact info, DRE #01466876, social links, unsubscribe

## CMA Handoff — Critical Wiring

The "What's My Home Worth?" CTA is the newsletter's conversion action. Here's how it works end-to-end:

### Current State (Manual)
- Button target URL: `https://graehamwatts.com/home-value` (form landing page)
- User fills out form (name, email, phone, property address)
- GHL workflow captures lead and creates contact
- Graeham gets an SMS/email notification with the address
- Graeham manually invokes the `cma-generator` skill: "Generate a CMA for [address]"
- cma-generator produces HTML/Email/PDF at `https://graehamwatts.github.io/online-content/cmas/CMA_[address].html`
- Graeham emails the CMA link back to the lead

### Future Auto-Chain (Not Yet Built)
- Button target URL: `https://graehamwatts.com/home-value-instant`
- GHL form triggers an n8n webhook
- Webhook calls cma-generator via API (once wired)
- CMA auto-generates at `https://graehamwatts.github.io/online-content/cmas/CMA_[address].html`
- Lead receives auto-email with CMA URL within 10 minutes
- Graeham gets notification and can follow up with commentary

### What This Skill Does
The newsletter template includes the **correct CTA button wiring** (link target = home-value form, GHL keyword = VALUE, tracking params = utm_source=newsletter, utm_campaign=[slug]). Future session wires the auto-chain.

## Newsletter Format Output

Generate these three outputs for every newsletter:

1. **Email-Ready HTML** (paste into Gmail) — Table-based, inline styles, 600px max-width, system fonts, base64-embedded images. File: `outputs/newsletter-YYYY-MM-DD-[slug].html`
2. **Plain Text Fallback** — Auto-generated from HTML, 70-char line wrap. File: `outputs/newsletter-YYYY-MM-DD-[slug].txt`
3. **Gmail Draft via API** (if Gmail MCP connected) — Creates a draft in Graeham's Gmail with the HTML pre-loaded, subject line, preview text set.

## Brand Standards

Matches the content-creation-engine single-topic dashboard design language:

- **Palette:** Navy `#1B2A4A`, Gold `#C5A258`, background `#f4f5f7`
- **Fonts:** System fallback stack (email-safe: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`)
- **CTA button:** Gold background, navy text, bold, 14px padding, 8px border-radius
- **Max-width:** 600px (email-safe)
- **Section dividers:** Navy horizontal rule, 1px, 20px vertical padding
- **Card sections:** White bg, 1px border `#e2e5ea`, 12px border-radius, 2-stack layout

## Voice & Tone

Same as content-creation-engine voice rules:
- First-person, conversational, direct (Graeham's voice)
- Addresses single reader by name ("Hey [First Name]")
- Specific numbers, zero hype
- No "hope this finds you well" / "just wanted to reach out" filler openers
- Opens cold with the week's hook

## Fair Housing Compliance (Non-Negotiable)

All newsletter content follows the same Fair Housing rules as content-creation-engine:
- NO demographic descriptors
- NO coded "safe / family-friendly / up-and-coming" language
- NO school rankings as selling points
- All neighborhood references limited to property features, price ranges, market trends, architecture, zoning, commute facts, walkability

## Workflow

### Single-Topic Newsletter (most common)
User has a topic package from content-creation-engine. This skill:
1. Reads the topic's `content-package-YYYY-MM-DD-[slug].md` or the dashboard's CONTENT_LIBRARY for the `email` and `blog` formats
2. Pulls market data from `references/topic-history.json` or the research data panel
3. Assembles all 7 sections using the HTML template
4. Outputs email-ready HTML + plain text
5. Optionally creates Gmail draft via Gmail MCP

### Multi-Topic Weekly Newsletter
User has multiple topics from a weekly calendar. This skill:
1. Takes the week's 3-5 topics as input
2. Picks the strongest as the lead story
3. Converts the rest into secondary sections (market update, community news, featured content)
4. Assembles per the 7-section template
5. Outputs email-ready HTML + plain text

## Auto-Render to Single-Topic Dashboard

When called from within a content-creation-engine single-topic dashboard build, this skill populates the `full-newsletter` format entry in the dashboard's CONTENT_LIBRARY, so the dashboard has a "Copy Newsletter" button that grabs the complete assembled newsletter.

## Output Locations

- `outputs/newsletter-YYYY-MM-DD-[slug].html` — email-ready HTML
- `outputs/newsletter-YYYY-MM-DD-[slug].txt` — plain text fallback
- `outputs/newsletter-YYYY-MM-DD-[slug].meta.json` — metadata (subject, preview, CTA targets, tracking params)
- Optional: Gmail draft created via Gmail MCP

## Example Prompts

- "Assemble this week's newsletter from the EPA Two Years topic"
- "Generate a newsletter with the EPA Two Years story as lead + market update + Woodland Park community section"
- "Turn this topic package into a full Friday newsletter"
- "Prep The EPA Report for this week — lead with the homicide-free story"

## Reference Files

- `references/newsletter-template.html` — the master HTML template (table-based, email-safe)
- `references/section-types.md` — full spec for all 7 section types with HTML snippets
- `references/cma-integration.md` — detailed CMA handoff wiring and future auto-chain plan
- `references/brand-standards-email.md` — email-safe brand token reference
- `templates/newsletter-builder.py` — Python assembly script

## Strict Rules (Non-Negotiable)

1. All 7 sections must appear in the exact order listed above.
2. CTA button MUST use the correct target URL and GHL keyword (VALUE).
3. All HTML must be email-safe: no external CSS, no JS, no web fonts, table-based layout, inline styles.
4. DRE #01466876 appears in the footer.
5. Fair Housing compliance check before send.
6. Voice & Tone rules from content-creation-engine apply.
7. Subject line ≤ 60 chars, preview text ≤ 100 chars.
8. Newsletter must fit on a single scroll on mobile (under 8 major sections).
9. Plain text fallback always generated alongside HTML.
10. File saved to `outputs/newsletter-YYYY-MM-DD-[slug].html`.
11. **Humanizer pass mandatory before send** — see "Humanizer Final Pass" section below.

---

## Humanizer Final Pass (Mandatory Before Send)

Before pushing the newsletter HTML to GitHub Pages or generating the prep email for Peter, run every block of reader-facing prose through the `humanizer` skill. Subscribers will close the email instantly if it reads like a model wrote it — and once they unsubscribe, they don't come back.

**What gets humanized:**
- The lead story paragraphs (Section 2)
- The community & development bullets if written as prose (Section 4)
- The featured content deep-dive teaser (Section 5)
- The CTA block headline + supporting copy (Section 6)
- The subject line variants and preheader text
- Any inline narrative in the market update cards (the stat numbers stay; the framing sentences get humanized)

**What does NOT get humanized:**
- Raw market stat numbers, percentages, and dollar values (these are data)
- The DRE# and contact footer (legally required exact text)
- Section headers in the canonical template (locked structure)
- The "View in browser" / "unsubscribe" footer chrome

**How to invoke:**
1. Assemble the newsletter sections as usual.
2. Before assembling into the final HTML template, pass each prose section through the humanizer skill with Graeham's voice as the calibration sample (first-person, conversational, specific numbers, zero hype — same voice rules as content-creation-engine).
3. Drop the humanized prose back into the HTML template.
4. Run the brand-integrity check + Fair Housing check.
5. Push to GitHub Pages and trigger the Peter prep email.

This applies to both the inaugural manual sends and the monthly auto-fire cadence (1st Monday at 7 AM PT). The scheduled task must call the humanizer step before the Composio push — do not skip it because the schedule is running unattended.

---

## Publishing (canonical pattern - direct git, Composio RETIRED)

> **Read first:** `shared-references/publishing-via-composio.md` - single source of truth for ALL skills. (Filename is historical; the doc now mandates **direct git push**. Composio was retired workspace-wide 2026-06-09. Do NOT use `run_composio_tool` or `GITHUB_COMMIT_MULTIPLE_FILES`.)

Write the output HTML into the Online Content clone at `C:/Users/Graeham Watts/Documents/Claude/Online Content/newsletters/YYYY-MM-DD-newsletter-slug.html`, then:

```bash
cd "C:/Users/Graeham Watts/Documents/Claude/Online Content"
git add "newsletters/YYYY-MM-DD-newsletter-slug.html"
git -c user.name="Graeham Watts" -c user.email="graehamwatts@gmail.com" commit -m "Newsletter: [date] [slug]"
PAT=$(tr -d '[:space:]' < github-token.txt)
git -c http.version=HTTP/1.1 push "https://${PAT}@github.com/Graehamwatts/online-content.git" HEAD:main
```

Hosted URL: `https://graehamwatts.github.io/online-content/newsletters/YYYY-MM-DD-newsletter-slug.html` (Pages rebuilds in ~1-2 min - verify it loads before sending). Never print the PAT. Before pushing, run the brand validator: `python "C:/Users/Graeham Watts/Documents/Claude/Skills/skills/content-creation-engine/scripts/verify_output_brand.py" <file>` - exit 2 = blocked value, never ship. Full reliability notes (curl 55 retries, lock files) in the shared doc.

---

## Monthly Cadence (added May 2026)

> **Production-ready monthly flow.** First inaugural send: May 2026 (Woodland Park 772 Units). Subsequent monthly sends fire automatically on the 1st Monday of each month at 7 AM PT.

### Architecture (3 components)

1. **This skill** — Generates the newsletter HTML.
2. **n8n workflow** `Monthly Newsletter Prep Email — Peter + Adrian` (ID `zyBwrCIqRa4zKjzK`) — Webhook-triggered relay that emails the prep package to Peter, CC Adrian + Graeham.
3. **Cowork scheduled task** `monthly-newsletter-monday` — fires 1st Monday of month, 7 AM PT. Builds content via this skill, pushes HTML to GitHub Pages, then calls the n8n webhook.

### Cron expression for the Cowork task
```
0 7 1-7 * 1
```
Reads as: "at 7:00 AM on days 1-7 of every month, but only when it's a Monday." This always lands on the 1st Monday of the month (since the 1st Monday is always between days 1 and 7).

### File path convention
- Hosted newsletter: `emails/YYYY-MM-newsletter-{topic-slug}.html`
- Example: `emails/2026-05-newsletter-woodland-park.html`
- Live URL: `https://graehamwatts.github.io/online-content/emails/...`

### The Peter handoff pattern (deliberate UX)
**Why it works:** Peter is the human quality gate. Adrian sends to the list. Splitting these two roles means:
- The system can fire automatically each month
- A human reviews tone, brand voice, and factual accuracy before anything hits subscribers
- Peter doesn't need to know HTML or care about send tools

**The prep email Peter gets contains:**
1. A "View the rendered newsletter" CTA button (linking to the hosted GitHub Pages URL — what subscribers will see)
2. Three subject line variants for A/B testing
3. Suggested preheader text
4. Two paths for Adrian to send: (a) view-source + paste into send tool's HTML mode, or (b) clone-from-URL if the send tool supports it (Mailchimp, Beehiiv, ConvertKit do)
5. Clear three-step instructions

**Adrian is CC'd from the start** so he sees the prep email when Peter does. The "official" handoff is still Peter forwarding (he picks the subject), but Adrian has visibility throughout.

### Webhook payload schema
The Cowork scheduled task should POST to the n8n webhook with:
```json
{
  "month_year": "May 2026",
  "topic_title": "Woodland Park 772 Units — Ready for Adrian to Send",
  "newsletter_url": "https://graehamwatts.github.io/online-content/emails/2026-05-newsletter-woodland-park.html",
  "subject": "[Month YYYY] Newsletter Prep — {topic} (ready for Adrian)",
  "prep_email_html": "<full-html-prep-email-as-string>"
}
```

### Topic selection rule
For each month, the topic should be the highest-performing or most-relevant story from that month's content, ideally pulled from:
- The canonical weekly calendar's BOFU cornerstone (highest opportunity score)
- OR the IG post / YT video with the most engagement that month
- OR a major local development story (the Woodland Park 772 inaugural send used this category)

If no clear standout exists for a month, pick the topic with the strongest convergence signal (3+ data sources pointing the same direction).

### Recipients (current as of May 2026)
- **TO**: Peter (`graehamwattsvideo@gmail.com`) — reviews and forwards
- **CC**: Adrian (`graehamwattsclientcare@gmail.com`) — sends to list
- **CC**: Graeham (`graehamwatts@gmail.com`) — visibility

### Brand integrity (run before every push)
The newsletter HTML must:
- Contain DRE 01466876 in the sign-off
- NOT contain the blocklisted DRE# (the blocklist verifier in `scripts/verify_brand_identity.py` enforces this)
- NOT contain the name of any former team member (see content-calendar/SKILL.md canonical template section for current team)
- Use brand colors: navy `#1B2A4A`, gold `#C5A258`/`#B8860B`, with white background for email-client compatibility
- Use email-safe HTML: `<table>`-based layout, inline CSS, no external stylesheets

### Last verified
- Inaugural test send: 2026-05-03 (Gmail msg `19defe22884b7b99`)
- n8n workflow: `zyBwrCIqRa4zKjzK` (active)
- Hosted newsletter: `emails/2026-05-newsletter-woodland-park.html` (commit `5d00c9b`)

---

## Newsletter v2 Structure (locked May 2026)

> **This is the canonical newsletter HTML structure moving forward.** Live reference: [`emails/2026-05-newsletter-woodland-park.html`](https://github.com/Graehamwatts/online-content/blob/main/emails/2026-05-newsletter-woodland-park.html).

### Data tie-in (verbal confirmation)
The newsletter topic is **always** sourced from the canonical weekly calendar's research data, NOT picked manually. Selection rule (in order of priority):
1. The most recent BOFU cornerstone (highest opportunity score from the calendar)
2. Highest-engagement IG post or YT video from the prior month (per Composio data)
3. Strongest convergence signal across IG + YT + GSC + Reddit + Zillow (3+ sources pointing same direction)

**Chain:** Research data (8 sources) → Canonical weekly calendar (v5.4) → Monthly newsletter source. The newsletter inherits the same brand/format rules as the weekly calendar.

### Section structure (top to bottom)

1. **Hero** — gradient navy/gold header with month/year, title, 1-line description.
2. **Video embed block** — clickable thumbnail (1280x720) with play-button overlay. Links to YouTube. If no video exists for the topic that month, link defaults to the channel page.
3. **Lead content** — greeting + 2-3 paragraphs setting up the topic.
4. **Headline number callout** — single big stat with gold accent box.
5. **The 3 effects (or "3 things you need to know")** — three numbered subsections with bold lead + paragraph each.
6. **What this means for you specifically** — three audience-segmented callouts (sellers / long-term holders / buyers).
7. **Bay Area Market Snapshot** — 4-stat horizontal strip (rate, EPA YoY, DOM, sale-to-list) with month-over-month deltas. Pulls from MLSListings.com data. Ties into the bi-monthly market update flow.
8. **Primary CTA** — gold button → mailto: with pre-filled subject for free EPA valuation.
9. **Cross-promo footer** — 4 cards: video walkthrough request, YouTube channel, Instagram, bi-monthly market update subscribe. Each uses mailto: for lead capture.
10. **Sign-off + DRE 01466876**.
11. **Footer** — list-context note, "view in browser" link.

### Browser-only chrome (full-width view)
The hosted version on GitHub Pages renders **full-width** in browsers via:
- `<style>@media screen` rules that activate `body.browser-view` background gradient
- A small inline `<script>` that adds `browser-view` class on DOMContentLoaded (email clients strip scripts)
- A 280px sidebar (About / Contact / Free Valuation card) that appears in browsers but is `display:none` in email clients
- `max-width: 1100px` browser-shell container with the 640px email-safe column inside

This dual-layout approach means the SAME file works correctly in both contexts.

### Lead capture pattern
All "click for more" links use `mailto:` with pre-filled subject and body. The lead's email lands in `graehamwatts@gmail.com` with a subject that signals their intent. Cheap, no third-party form service needed.

---

## Peter's Runbook (5-minute review process)

> **Goal: Peter validates the newsletter, picks a subject, forwards to Adrian. Total time ~5 min.**

### Step 1: Open and review (90 sec)
Click the gold "View the rendered newsletter" button in the prep email. Review top to bottom like a recipient would. Flag wrong tone, wrong facts, or weird formatting.

### Step 2: Swap video thumbnail (60 sec — only if a video exists for this topic)
- Save the YouTube thumbnail as `{topic-slug}-video-thumb.jpg`
- Push to `online-content/emails/` via Composio
- The newsletter HTML auto-loads it
- If no video exists yet, leave the placeholder — it links to the YouTube channel page

### Step 3: Update market snapshot stats (60 sec — if stale)
The 4-stat row (rate / EPA YoY / DOM / sale-to-list) should match the most recent MLS pull. If stale, open the newsletter HTML, search for the rate value (e.g. `6.42%`) — the four stat cells are right there. Update each.

### Step 4: Pick a subject line (10 sec)
Three subject variants are listed in the prep email. The first is usually strongest (direct value-driven).

### Step 5: Customize cross-promo cards (90 sec — optional)
The "Want more from us?" footer has 4 cards. If a NEW video was published this month, swap the first card to feature it.

### Step 6: Forward to Adrian (10 sec)
Forward the prep email to `graehamwattsclientcare@gmail.com` with a 2-3 line note: "Adrian, this is May's monthly newsletter. Subject line: [your pick]. Send to the full list when ready."

---

## Implementation note: sending the >8KB prep email (Composio RETIRED 2026-06-09)

The n8n webhook payload has practical size limits when passing large HTML strings, so don't push the full ~8KB+ prep HTML through the webhook. Composio's `GMAIL_SEND_EMAIL` is retired — instead send the prep email via either:

1. **Gmail connector (preferred when available):** create/send via the session's Gmail MCP — To `graehamwattsvideo@gmail.com`, CC `graehamwattsclientcare@gmail.com` + `graehamwatts@gmail.com`, HTML body = the prep email.
2. **SMTP fallback:** reuse the proven send pattern from `skills/switchy-engine/scripts/send_email.py` (Gmail app password at `C:\Users\Graeham Watts\Documents\Claude\Skills\gmail-app-password.txt` — read at send time, never print).

The n8n workflow `zyBwrCIqRa4zKjzK` is still useful as the trigger record — call it with a small payload (just the topic title + URL for logging), and send the actual email via one of the two paths above.
