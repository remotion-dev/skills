# Newsletter Module — Content Creation Engine

Distribution module that converts content-engine topics into branded email newsletters for Graeham Watts' two core audience segments.

## How It Integrates with the Content Engine

The newsletter module sits downstream of Phase 5 (Script Writer). Once a topic has been scored, funnel-tagged, and scripted, the same research and talking points feed into a newsletter article — no duplicate ideation needed.

**Pipeline position:**

```
Phase 1-4 (Topic Discovery + Scoring)
  → Phase 5 (Script Writer — video scripts)
  → Newsletter Module (email article from same topic)
  → Gmail draft (ready to review + send)
```

The newsletter doesn't replace video content — it extends the same topic into another channel. One topic, multiple formats. The video script provides the core argument and data points; the newsletter reshapes them for a reading audience with different attention patterns.

## Two Audience Segments

### 1. EPA Farm Newsletter (Hyper-Local)

**Audience:** Homeowners and renters in East Palo Alto — Graeham's geographic farm area.

**Tone:** Neighbor-to-neighbor, warm, community-first. These people live in EPA and want to know what's happening on their streets.

**Content mix:**
- Local market stats (median price, days on market, inventory) with month-over-month and year-over-year comparisons
- New development updates, city council decisions, zoning changes
- Community events, local business spotlights
- "Recently Sold Near You" section — 2-3 recent sales with address, price, bed/bath, days on market
- Seasonal homeowner tips localized to EPA (e.g., fire season prep, water conservation rebates)

**Frequency:** Bi-weekly (every other week), with an extra send for major market events or new listings.

**Subject line examples:**
- "3 Homes Just Sold on Your Block — Here's What They Got"
- "EPA's Median Price Hit $X in [Month] — What That Means for You"
- "New Development Approved on University Ave — 47 Units Coming"

### 2. Past Clients Newsletter (County-Level)

**Audience:** Graeham's past buyers and sellers across San Mateo County and the broader Peninsula. People who already trust him but may not be thinking about real estate right now.

**Tone:** Professional, informative, light touch. Stay top-of-mind without being pushy. These are relationship-maintenance touches, not lead-gen blasts.

**Content mix:**
- County-level and Peninsula-wide market trends
- Interest rate updates and what they mean for equity / refinance decisions
- Tax changes, Prop 19 portability reminders, homestead exemption tips
- Seasonal maintenance checklists
- "Ask Graeham" Q&A — answer a real question from a client (anonymized)
- Referral program reminder (subtle, not every issue)

**Frequency:** Monthly.

**Subject line examples:**
- "San Mateo County Home Values Rose 4.2% — Is Yours Keeping Up?"
- "3 Tax Moves to Make Before December (Homeowner Edition)"
- "Your Spring Home Maintenance Checklist — 15 Minutes Can Save You $5K"

## Topic Flow: Content Engine → Newsletter Sections

When the content engine produces a scored topic, map it to the newsletter like this:

| Funnel Tier | Newsletter Usage |
|---|---|
| **BOFU** (bottom-of-funnel) | Lead article — directly addresses a buying/selling decision. Include the "What's My Home Worth?" CTA prominently. |
| **MOFU** (middle-of-funnel) | Secondary article or "Did You Know?" sidebar — educational, builds authority. |
| **TOFU** (top-of-funnel) | Lifestyle/community section — humanizes Graeham, builds local connection. Not every issue needs TOFU. |

Each newsletter should have one BOFU lead article and one supporting piece (MOFU or TOFU). Don't overload — newsletters that try to cover 5 topics get skimmed and deleted.

## Newsletter Assembly Workflow

### Step 1 — Research & Data Pull
Gather the data for the lead article using the content engine's existing sources:
- MLS stats via Chrome + MLSListings.com for market data
- Windsor MCP connectors for Search Console / social performance data
- Web search for news context, rate updates, local government actions
- Reference `references/research-sources.md` for the full source inventory

### Step 2 — Write the Content
Write the newsletter body following Graeham's voice guide (`references/phases/script-writer/references/voice-and-style.md`). Key rules:
- Lead with the most interesting number or fact — not "Hi, welcome to my newsletter"
- Write at an 8th-grade reading level. No jargon without explanation.
- Keep paragraphs to 2-3 sentences max
- Use subheads every 150-200 words for scannability
- Every claim needs a source or date anchor ("As of April 2026...")

### Step 3 — Assemble HTML Email
Build the newsletter as a single-file HTML email using inline CSS for email client compatibility.

**Template specs:**
- Max width: 600px (centered)
- Font: Arial/Helvetica fallback stack (email-safe)
- Header: Graeham's headshot + name + "Intero Real Estate" + DRE#
- Brand colors: Reference `../../../shared-references/branding.md` if available; otherwise use the brand colors from `references/market-config.md` or the cma-generator/references/branding.md as a fallback
- Footer: Unsubscribe link, physical address (CAN-SPAM required), social links, DRE#
- Mobile-responsive: single-column layout, minimum 14px body text, 44px minimum touch targets for buttons

### Step 4 — Review
Before drafting in Gmail:
- Spell-check and fact-check all stats against source data
- Verify all links work (especially the CTA button)
- Confirm subject line follows the guidelines below
- Run the Fair Housing guardrails check (same rules as video content — no demographic neighborhood descriptions)
- Verify CAN-SPAM compliance (see section below)

### Step 5 — Draft in Gmail
Use the Gmail MCP connector to create a draft:
- To: the appropriate distribution list (EPA Farm or Past Clients)
- Subject: the crafted subject line
- Body: the assembled HTML
- CC: graehamwattsclientcare@gmail.com (for tracking)

## "What's My Home Worth?" CTA Button

Every newsletter includes a persistent CTA button in the lead article section.

**Button specs:**
- Text: **"Curious What Your Home Is Worth?"**
- Style: Solid brand-color background, white text, rounded corners, 48px height minimum, centered
- Link target: Graeham's website landing page or GHL form page (the specific URL will be configured when the form is built)

**Future automation pipeline (PLANNED — NOT YET BUILT):**

```
Homeowner clicks CTA button
  → Lands on GHL form page
  → Fills out address + contact info
  → Form submission triggers GHL workflow (primary path)
     OR N8N webhook (fallback path)
  → Workflow calls the cma-generator skill via API
  → CMA skill auto-generates a branded Comparative Market Analysis report
  → Report emails to:
     - The homeowner (personalized cover letter)
     - CC: graehamwatts@gmail.com
     - CC: graehamwattsclientcare@gmail.com
  → GHL creates a contact record + tags "CMA-Request" + assigns follow-up task to Graeham
```

**Current state:** The CTA button links to a landing page. The auto-CMA pipeline is documented here for when it's ready to build. The individual pieces exist (GHL CRM, N8N automations, cma-generator skill) but the end-to-end trigger chain is not yet wired together.

**What needs to be built:**
1. GHL landing page / form with address input fields
2. GHL workflow OR N8N workflow to receive form submission
3. API bridge to trigger the cma-generator skill programmatically
4. Email template for the auto-generated CMA delivery
5. GHL contact creation + tagging + task assignment automation

## Subject Line Guidelines

Subject lines make or break open rates. Follow these rules:

**Do:**
- Use specific numbers: "3 Homes Sold on Your Street" > "Homes Are Selling"
- Create curiosity gaps: "The #1 Mistake EPA Sellers Make in April" > "Selling Tips"
- Reference the reader's situation: "Your Home's Value Changed This Month" > "Market Update"
- Keep under 50 characters when possible (mobile preview cutoff)
- A/B test when the email platform supports it — try 2 subject lines per send

**Don't:**
- Use ALL CAPS or excessive punctuation (\!\!\!\!)
- Use spam trigger words: "FREE", "ACT NOW", "LIMITED TIME", "GUARANTEED"
- Be vague: "Monthly Newsletter" or "Market Update" — these get ignored
- Use clickbait that the content doesn't deliver on

## CAN-SPAM Compliance Requirements

Every newsletter MUST comply with the CAN-SPAM Act. Non-compliance carries penalties up to $51,744 per email.

**Required elements:**
1. **Accurate "From" line** — Must identify Graeham Watts as the sender
2. **Non-deceptive subject line** — Must reflect the actual content of the email
3. **Physical mailing address** — Graeham's brokerage address must appear in the footer (Intero Real Estate office address)
4. **Unsubscribe mechanism** — A clear, conspicuous unsubscribe link that works for at least 30 days after sending. Must process opt-outs within 10 business days.
5. **Ad identification** — If the email is an advertisement, it must be identified as such (most newsletters are informational, but if promoting a listing, disclose)
6. **No purchased lists** — Only email people who have opted in or have an existing business relationship

**Footer template:**
```
Graeham Watts | REALTOR® | DRE# 01466876
Intero Real Estate
[Brokerage Address]
[Phone Number]

You're receiving this because [you signed up / we've worked together / you requested home value info].
[Unsubscribe link]
```
