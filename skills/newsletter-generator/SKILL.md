---
name: newsletter-generator
description: "Weekly newsletter generator for Graeham Watts (REALTOR, Intero Real Estate, DRE# 01466876). Produces complete multi-section email newsletters (The EPA Report) assembling a lead story + market update + community news + featured content + home-value CTA that ties into the cma-generator skill. Use ANY time the user mentions: newsletter, weekly newsletter, weekly email, email blast, subscriber email, EPA Report, weekly digest, send a newsletter, generate newsletter, assemble newsletter, newsletter HTML, email-ready newsletter, Gmail newsletter, multi-section email, or turning a single topic content package into a full newsletter. Also trigger when the user says 'send out the newsletter this week', 'prep the email for Friday', or 'package the content as a full weekly email'. Pairs with content-creation-engine (which generates the per-topic content) and cma-generator (which the What's My Home Worth CTA handoff targets)."
---

# Newsletter Generator — The EPA Report

> **What this skill is:** The final assembly layer that stitches multiple content sections into a complete weekly newsletter ready to paste into Gmail (or send via Gmail API). Ties the content-creation-engine's topic packages to the cma-generator's valuation handoff.

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

---

## Publishing via Composio (canonical pattern)

> **Read first:** [`shared-references/publishing-via-composio.md`](../shared-references/publishing-via-composio.md) — single source of truth for ALL skills.

After generating the newsletter HTML output, publish via Composio to `Graehamwatts/online-content` so the agent gets a permanent hosted URL.

**Account:** `github_spar-devata`  
**Owner:** `Graehamwatts`  
**Repo:** `online-content`  
**Branch:** `main`  
**Path pattern:** `newsletters/YYYY-MM-DD-newsletter-slug.html`  
**Hosted URL pattern:** `https://graehamwatts.github.io/online-content/newsletters/YYYY-MM-DD-newsletter-slug.html`

**Tool to use:** `GITHUB_COMMIT_MULTIPLE_FILES` (atomic commit, retry-safe).

```python
result, error = run_composio_tool(
    tool_slug='GITHUB_COMMIT_MULTIPLE_FILES',
    arguments={
        'owner': 'Graehamwatts',
        'repo': 'online-content',
        'branch': 'main',
        'message': 'descriptive commit message',
        'upserts': [{'path': 'newsletters/YYYY-MM-DD-newsletter-slug.html', 'content': html_content, 'encoding': 'utf-8'}]
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
- NOT contain the name "Eric" (no longer with the team — see content-calendar/SKILL.md canonical template section)
- Use brand colors: navy `#1B2A4A`, gold `#C5A258`/`#B8860B`, with white background for email-client compatibility
- Use email-safe HTML: `<table>`-based layout, inline CSS, no external stylesheets

### Last verified
- Inaugural test send: 2026-05-03 (Gmail msg `19defe22884b7b99`)
- n8n workflow: `zyBwrCIqRa4zKjzK` (active)
- Hosted newsletter: `emails/2026-05-newsletter-woodland-park.html` (commit `5d00c9b`)
