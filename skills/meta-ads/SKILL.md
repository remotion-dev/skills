---
name: meta-ads
description: "Direct Meta Ads management for Graeham Watts via Meta's OFFICIAL Ads MCP connector (mcp.facebook.com/ads, launched April 2026) — reporting, campaign creation, budget changes, pixel/CAPI diagnostics, and industry benchmarks for Facebook + Instagram ads. Use ANY time the user mentions: Meta ads, Facebook ads, Instagram ads, FB ads, IG ads, ad account, ad campaign, ad set, ad creative, ROAS, CPL, cost per lead, CPM, CPC, CTR, ad spend, ad budget, daily budget, pause ads, pause campaign, activate campaign, boost post, lead ads, lead gen campaign, lead form ads, retargeting, custom audience, lookalike, pixel, Meta pixel, Conversions API, CAPI, event match quality, Ads Manager, ad performance, ad audit, morning ad audit, ad benchmarks, auction benchmarks, opportunity score, A/B test ads, creative testing, ad fatigue, frequency cap, listing ads, open house ads, home valuation ads, promote my listing, run ads, launch ads, advertise this listing, special ad category, housing ads. Also trigger on: connect Meta ads, set up the ads connector, is Meta ads connected, ads connector not working, and any follow-up about a previously discussed Meta campaign. This skill owns ALL paid Meta work — do NOT use Windsor for ads data when this connector is live. For organic IG/FB insights use Windsor; for ad copywriting hand off to copywriter/content-creation-engine; this skill deploys and manages the actual ads."
---

# Meta Ads — Direct Connection (Official Meta MCP)

Manage Graeham's Facebook + Instagram advertising end-to-end through Meta's official Ads MCP server. Read performance, diagnose tracking, benchmark against the real estate vertical, and — with explicit confirmation — create and modify live campaigns.

**Agent identity:** Graeham Watts, REALTOR, Intero Real Estate, DRE# 01466876. Primary market East Palo Alto; secondary Redwood City, Palo Alto, Menlo Park, San Mateo County / Peninsula. CRM is GoHighLevel. Ads exist to feed the GHL pipeline — every campaign should map to a funnel stage and a follow-up path.

## Architecture — Who Owns What

This skill exists because Meta opened its Marketing API to AI assistants on April 29, 2026 (open beta, free). Before that, ads data came through Windsor. The division of labor is now:

| Job | Owner | Why |
|---|---|---|
| Ads reporting, audits, benchmarks | **this skill** (direct MCP) | Richer than Windsor: anomaly signals, auction benchmarks, opportunity score |
| Campaign create / edit / pause / budget | **this skill** (direct MCP) | Windsor write actions are a wrapper; direct is first-party, no token middleman |
| Pixel / Conversions API health | **this skill** (direct MCP) | Dataset tools don't exist in Windsor |
| Organic IG / FB page insights | **Windsor** (`instagram`, `facebook_organic`) | The official Ads MCP has ZERO organic tools — all 29 are ads-side |
| Cross-channel blended reporting (ads + GSC + YouTube + GHL) | **Windsor** | Single query surface across 325 connectors |
| Ad copy and creative concepts | `copywriter` / `content-creation-engine` | They write; this skill deploys |
| What happens to leads after the click | GoHighLevel / `ghl-crm-audit` | Ads end at the form fill; GHL owns nurture |

Don't blur these lines. The most common mistake is reaching for Windsor's `facebook` connector for ads questions — when the direct connector is live, it is the canonical ads source.

## Step 0 — Connection Check (every session, before anything else)

The official server's tools are named `ads_*` (e.g., `ads_get_ad_accounts`). In a fresh session they may be deferred.

1. Run ToolSearch with query `"ads_get_ad_accounts meta"` (or `"+ads insights campaign"`).
2. **Tools found** → call `ads_get_ad_accounts` first. This anchors the account ID, currency, and name that every subsequent call needs. Confirm with the user which account if more than one returns.
3. **Tools NOT found** → the connector isn't added or isn't enabled for this chat. Walk Graeham through setup (below), then stop — don't fake results, and don't silently substitute Windsor. Say plainly that the direct connection isn't live yet.

### One-time setup (user does this — requires his Meta login)

1. Claude app → **Settings → Connectors → Add custom connector**.
2. Name: `Meta Ads`. URL: `https://mcp.facebook.com/ads` — exactly this, no variants, no third-party mirrors.
3. Complete the Meta Business OAuth: log in, select ad account(s) and Pages, choose permission tier — **read-only / read+write / read+write+financial**. Recommend starting read-only for the first days, then upgrading once trust is established.
4. Restart the Claude app; enable the connector for the chat if prompted.
5. Verify with: "Show me my Meta ad accounts."

**Known beta quirk:** rollout is gradual — an account can show *disabled* for a few days after successful auth. That's Meta-side; check back later rather than re-doing setup. Permissions are revocable anytime at Business Suite → Settings → Business Integrations.

## The 29 Tools — Family Map

Full parameter notes live in `references/tool-manifest.md`. Read it before composing complex calls. Summary:

| Family | Tools | Use for |
|---|---|---|
| Campaign management (5) | `ads_create_campaign`, `ads_create_ad_set`, `ads_create_ad`, `ads_update_entity`, `ads_activate_entity` | The write surface. Every call here can spend money — guardrails below apply |
| Account lookups (3) | `ads_get_ad_accounts`, `ads_get_ad_entities`, `ads_get_pages_for_business` | Always called first; IDs anchor everything |
| Insights & benchmarks (7) | `ads_insights_performance_trend`, `ads_insights_anomaly_signal`, `ads_insights_industry_benchmark`, `ads_insights_auction_ranking_benchmarks`, `ads_insights_advertiser_context`, `ads_get_opportunity_score`, `ads_get_help_article` | Reporting, audits, "how am I doing vs other real estate advertisers" |
| Datasets / signals (4) | `ads_get_dataset_details`, `ads_get_dataset_quality`, `ads_get_dataset_stats`, `ads_get_errors` | Pixel + Conversions API health, event match quality, lost events |
| Catalog (10) | `ads_catalog_*` | E-commerce product feeds. Mostly irrelevant for Graeham's lead-gen business — skip unless he sets up a listings catalog for dynamic ads |

## Read Workflows

### "How are my ads doing?" — default report

Unless Graeham specifies otherwise: last 7 days vs prior 7 days, all active campaigns.

Produce a chat table: **Campaign | Spend | Results (leads) | CPL | CTR | Frequency | Trend vs prior week**. Then flag, in plain language:

- Frequency > 3.5 → audience fatigue, creative refresh due
- CPL up > 25% week-over-week → diagnose before spending more
- CTR down > 20% vs the campaign's own average → hook is wearing out
- Anything `ads_insights_anomaly_signal` surfaces → report Meta's own anomaly read

Always state the currency and date range. Lead-gen language, not e-commerce: Graeham measures **cost per lead**, not ROAS — a $15 CPL on a home-valuation campaign that feeds GHL is the success metric. Mention ROAS only if he runs a conversion-value campaign.

### Morning / weekly audit

On "audit my ads" or a scheduled run: pull entities → performance trend → anomaly signal → opportunity score, then deliver a five-line verdict: what's working, what's bleeding, the single highest-leverage change, and whether Meta's opportunity score suggestions are worth taking (they're auto-generated and often generic — evaluate, don't parrot).

### Benchmarks

`ads_insights_industry_benchmark` + `ads_insights_auction_ranking_benchmarks` with the real estate vertical. Frame results honestly: real estate CPLs in the Bay Area run high; being "above average CPM" in one of the most expensive ad markets in the country is context, not failure.

### Pixel / CAPI health

Use the four dataset tools. Graeham's events flow from graehamwatts.com and GHL funnels. Check event match quality, dedup between pixel and CAPI, and recent errors. If Purchase/Lead events drop, say which events, since when, and the likely layer (site change vs GHL webhook vs Meta-side).

## Write Workflows — Guardrails First

**Why this section is strict:** write tools create real spend, the product is in beta, and community reports include ambiguous prompts triggering unintended actions. One bad call here costs actual dollars and is hard to reverse.

### The confirmation gate (non-negotiable)

Before ANY call to `ads_create_campaign`, `ads_create_ad_set`, `ads_create_ad`, `ads_update_entity`, or `ads_activate_entity`, present a confirmation block and wait for an explicit yes:

```
PLANNED CHANGE
Entity:        [campaign/ad set/ad — name and ID, or "NEW"]
Action:        [create / update field X / activate / pause]
Before → After: [current state → new state]
Budget impact: [$X/day or $X lifetime — and what that totals over 30 days]
Start:         [immediate / scheduled]
```

Rules that follow from the why:

- Never invent a budget. If Graeham didn't give one, ask. Don't default to "$20/day seems reasonable."
- Create campaigns **paused** by default; activate as a separate confirmed step. Two small confirmations beat one expensive mistake.
- One account at a time. Never batch writes across accounts in a single confirmation.
- If a prompt is ambiguous between read and write ("can you refresh the campaign?"), read first, then ask.

### Special Ad Category: HOUSING (legally required)

Every campaign that advertises listings, home valuations, buying, selling, or renting MUST set Special Ad Category = HOUSING in `ads_create_campaign`. Meta restricts targeting for housing ads: no age, gender, or zip-code targeting; minimum ~15-mile radius; no lookalike audiences (special ad audiences instead). Build campaigns within these constraints from the start — a housing ad created without the category gets rejected, and repeat violations flag the ad account. This pairs with the Fair Housing guardrails in `content-creation-engine`: no demographic targeting in settings, no demographic signaling in copy.

### Campaign patterns for Graeham's business

| Pattern | Objective | Notes |
|---|---|---|
| Listing launch | Lead gen or traffic | Creative from `video-editor` / `higgsfield-video`; copy via `copywriter`; CTA → listing page or GHL form. HOUSING category |
| Home valuation (BOFU) | Lead gen | "What's my home worth" → GHL form → `cma-generator` fulfills. Strongest CPL historically for agents. HOUSING category |
| Open house | Reach/traffic, tight radius (≥15mi floor) | Short flight, 3-5 days. HOUSING category |
| Content amplification | Engagement/traffic | Boosting a performing organic reel — check the organic winner via Windsor first, then amplify here |

## Output Conventions

Chat tables by default; date range + currency always stated. For client-facing or coach-facing reports, hand off to his branded HTML pattern (`html-email` skill or the navy/gold dashboard style in `shared-references/branding.md`). Round dollars to whole numbers in tables, keep CPL to cents. Never paste raw JSON at Graeham.

## Handoffs

| Need | Skill |
|---|---|
| Ad copy / hooks / A-B variants | `copywriter` (3 variants default) |
| Full content package the ad amplifies | `content-creation-engine` |
| Video creative / b-roll | `higgsfield-video`, `heygen-video`, `vaibhav-template` |
| What converts in ads → feed content topics | `content-calendar` (paid signal informs the weekly plan) |
| Lead follow-up after the form fill | `ghl-crm-audit` / GoHighLevel connector |
| Weekly organic report | `social-media-analyzer` / `content-calendar` |

## Troubleshooting

- **Tools absent after setup** → connector not enabled for this chat, or app not restarted after adding. Settings → Connectors shows status.
- **Account shows disabled** → gradual beta rollout; wait a few days. Not a setup error.
- **Write call rejected for permissions** → connector was authorized read-only. Re-auth at the Meta OAuth with read+write (or read+write+financial for budget changes).
- **OAuth loop / stale auth** → revoke at Business Suite → Settings → Business Integrations, then re-add the connector.
- **Rate or schema errors** → the manifest is versioned server-side and updates automatically; retry once, then check `ads_get_help_article` for the relevant Help Center doc.
