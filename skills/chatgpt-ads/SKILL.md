---
name: chatgpt-ads
description: ChatGPT Ads campaign builder for Graeham Watts — builds ready-to-launch ad campaigns for ads.openai.com, where ads appear alongside live ChatGPT conversations about buying or selling homes. Merges two AiM resources (the Bulk-Build ChatGPT Ads Cowork agent and the 25-hint Context Hint Library, both May 2026) into one skill. Produces a bulk-upload spreadsheet (campaigns/adgroups/ads), a context-hints document, and a setup checklist. Use ANY time the user mentions ChatGPT ads, OpenAI ads, ads.openai.com, context hint, ad inside ChatGPT, advertise in ChatGPT conversations, ChatGPT ad campaign, build my ChatGPT ads, light test campaign on ChatGPT, John's ChatGPT test, bulk upload ads, CPC bid for ChatGPT, or expanding/optimizing an existing ChatGPT Ads campaign. Also trigger when planning the ads channel mix alongside meta-ads — this skill owns the ChatGPT channel; meta-ads owns Facebook/Instagram.
---

# ChatGPT Ads — Campaign Builder

People now ask ChatGPT who they should hire to sell their house or help them buy one. OpenAI sells ad placements below those conversations. This skill builds a complete, ready-to-launch campaign: strategy, targeting language, copy, and the upload files — leaving only the genuinely human steps (account, images hosting, final review, launch).

Source: Jason Pantana's AI Marketing Academy — "Bulk-Build ChatGPT Ads with an AI Agent" (guide + Cowork working folder) merged with the "ChatGPT Ads Context Hint Library" (25 hints), both May 2026, adapted for Graeham 2026-06-11.

---

## How ChatGPT Ads work (2 minutes)

- **Account:** ads.openai.com, log in with a ChatGPT account, apply. Approval typically 2–4 business days. *(Graeham's account: approved as of June 2026.)*
- **Objectives** — pick one per campaign: **Clicks** (CPC — the default), **Reach** (CPM, ~$60 default — brand exposure), **Conversions** (CPC optimized to site actions; requires OpenAI's tracking pixel — *currently unreliable industry-wide, so default to Clicks*). **Bid guidance (updated June 2026):** OpenAI dropped the max-CPC floor to ~$4, but real-world under-serving means you should **bid ~$7–8** to actually win impressions. There are **no longer start/end dates** — a campaign runs until its budget total is spent. Full post-launch playbook in `references/troubleshooting.md`.
- **Structure:** campaign (objective, budget, dates, country) → ad groups (one per *moment* you want to show up in) → ads (title ≤ 24 chars, copy ≤ 48 chars, image, landing URL).
- **Targeting is a context hint, not keywords.** Each ad group gets one plain-language paragraph (2–4 sentences) describing the person and the moment: **Persona + Location + Intent + Moment**. The matcher reads the hint, the ad copy, AND the landing page to decide when to show the ad.
- **The bulk-template flaw:** OpenAI's upload spreadsheet has a `keywords` field that doesn't exist in Ads Manager. Two-layer play: fill keywords with strong arrays derived from each hint (gets the import through), then paste the real context hint into each ad group in Ads Manager after upload (~90 seconds each).

## The workflow (six phases)

Run in order. The only mid-workflow checkpoint is Phase 4 approval.

1. **Load context** — read `references/market-config-graeham.md` (and `../shared-references/identity.json` for brand fields — never type DRE/contact from memory). Load the `marketing-psychology` skill: run its Step 1 diagnosis per ad group (ad-group moments map to awareness stages and blocking forces) and its Step 5 failure audit on all copy.
2. **Audit the website** — fetch graehamwatts.com homepage + standard slugs (/about, /buyers, /sellers, /home-valuation, /contact) + any specialization pages. Build a landing-page inventory: exists / quality / missing. The ad is the doorway; the page is the room — flag weak pages, recommend the downshift.
3. **Inventory images** — 3–6 square images (1:1, 640–1200px). Headshot, neighborhood landmarks, sold-and-closed homes (with permission), lifestyle shots. NEVER active listings (misrepresentation risk once it sells). Images must be hosted at public URLs — the template takes URLs, not uploads.
4. **Recommend three ad groups** — pick from `references/moments.md` (the 25-moment library), prioritizing moments with strong existing landing pages, niches to grow, and a buyer/seller mix. Present picks with rationale; **wait for approval**.
5. **Write the campaign** — `references/copywriter.md` is the craft authority. Per ad group: name, context hint (Persona + Location + Intent + Moment, localized to EPA/Peninsula), 10–15-keyword array, three ads pulling *different* levers (count characters: title ≤ 24, copy ≤ 48 — hard limits), max bid, image mapping. Start from the matching hint in `references/context-hint-library.md` when one fits — localize, never paste generic.
6. **Assemble deliverables** — `references/workbook-builder.md` is the authority. Output three files to the skill-local `outputs/` (gitignored): `campaign_workbook.xlsx` (3 sheets: campaigns, adgroups, ads — OpenAI's template structure exactly), `context-hints-to-paste.docx`, `setup-checklist.docx` (budget split, bids, image hosting instructions, landing-page warnings, launch order, post-upload checklist).

**Self-check before shipping:** every title ≤ 24 chars and copy ≤ 48 (counted, not estimated) · 3 ads × 3 ad groups = 9 ads · every ad has URL + image assignment · zero protected-class language · DRE/brokerage fields from identity.json · marketing-psychology failure audit passed.

## Post-upload (human steps — goes in the checklist)

Upload workbook at ads.openai.com → per ad group: paste context hint into the targeting field, upload/link images, confirm landing URL and max bid → top-level review of budget → launch. First 30 days are diagnostic: watch impressions per ad group; bump an ad group's bid by $1 if it's starved after 24–48h; pause losers, feed winners. **When a live campaign is misbehaving, load `references/troubleshooting.md`** — the symptom→fix decision tree (flatline / impressions-no-clicks / clicks-no-conversions), the "budget is a ceiling not a charge" reality, and the catcher's-mitt landing-page standard.

## Light test campaign mode

When Graeham asks for a "light test" (e.g., John's first run): ONE campaign, Clicks objective, 2–3 ad groups, **~$7–8 max bid** (the ~$4 floor under-serves — see `references/troubleshooting.md`), small lifetime budget (confirm amount — $100–200 range is typical for a diagnostic; the campaign-total budget is the cap since there are no end dates), success = which moments get impressions/clicks and which landing pages hold them, not closed deals. Treat it as a learning purchase.

## Rules (non-negotiable)

- **Fair Housing always** — target the housing situation, never the household. No protected-class language or proxies (no school quality, no "safe/family-friendly neighborhoods"). Same guardrails as content-creation-engine.
- **California DRE advertising rules** — ads identify Intero Real Estate and DRE# 01466876 (from identity.json) where required; brokerage ad review before first launch.
- **Financial-services copy gets flagged** — OpenAI's ad policies restrict money/financing language; the "pre-approved buyer" hint (#15) has been auto-disabled in testing. Keep ad copy off financing; mortgage/lender angles will struggle to run. (Detail in `references/troubleshooting.md`.)
- **Persuasion, never manipulation** — marketing-psychology's litmus applies to every hint and ad. No fabricated urgency, no promised outcomes.
- **Three ad groups, three ads each** is the sweet spot — more fragments spend; push back once if asked for more, then comply.
- **Character limits are import-breakers** — count, don't estimate.
- **Don't fabricate landing pages** — fetch and verify; downshift with a flag if missing.
- Final prose (hints + copy) passes through the `humanizer` skill before delivery.

## References

| File | Load when |
|---|---|
| `references/market-config-graeham.md` | Every run (Phase 1) — Graeham's pre-filled business config |
| `references/moments.md` | Phase 4 — the 25-moment library to pick ad groups from |
| `references/copywriter.md` | Phase 5 — hint formula, copy craft, character-limit techniques |
| `references/context-hint-library.md` | Phase 5 — 25 ready-made hints with sample headlines/descriptions to localize |
| `references/workbook-builder.md` | Phase 6 — exact xlsx/docx assembly specs |
| `references/troubleshooting.md` | **Post-launch** — symptom→fix decision tree, bid/budget reality (June 2026), catcher's-mitt landing pages, financial-services policy flag, Yelp×ChatGPT signal |

Related skills: `marketing-psychology` (diagnosis + audit layer), `meta-ads` (Facebook/Instagram channel), `copywriter` (general copy outside this format), `seo-optimizer` (fix the landing-page "room" before buying doorways).
