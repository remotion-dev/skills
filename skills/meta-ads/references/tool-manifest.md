# Meta Ads MCP — Tool Manifest (29 tools)

Official server: `https://mcp.facebook.com/ads` (Meta Ads AI Connectors, open beta since 2026-04-29).
Tools below are grouped by family. Names are the server-side tool names; in a Claude session they appear with an `mcp__<server>__` prefix — find them via ToolSearch, don't hardcode the prefix.

**Important:** the live manifest is versioned on Meta's side and updates automatically. If a call fails on schema, re-discover the tool via ToolSearch and inspect its current parameters rather than trusting this file. This manifest is a map, not the territory.

## 1. Campaign creation & management (5) — WRITE, guardrails apply

| Tool | Purpose | Notes |
|---|---|---|
| `ads_create_campaign` | Create campaign: objective, budget, special categories | ALWAYS set `special_ad_categories: HOUSING` for real-estate ads. Create paused |
| `ads_create_ad_set` | Create ad set: targeting, placement, schedule, budget | Housing rules: no age/gender/zip targeting, ≥15mi radius |
| `ads_create_ad` | Create ad, link creative | Creative must exist or be supplied (image/video + copy) |
| `ads_update_entity` | Edit existing campaign / ad set / ad | Budget changes, renames, schedule edits. Confirmation gate |
| `ads_activate_entity` | Activate or reactivate a paused entity | The "go live" switch — separate confirmation from creation |

Pausing is done via `ads_update_entity` (status field), not a dedicated tool.

## 2. Product catalog (10) — mostly N/A for lead-gen real estate

`ads_catalog_create`, `ads_catalog_get_catalogs`, `ads_catalog_get_details`, `ads_catalog_get_diagnostics`, `ads_catalog_get_feed_rules`, `ads_catalog_get_product_details`, `ads_catalog_get_product_feed_details`, `ads_catalog_get_product_set_products`, `ads_catalog_get_product_sets`, `ads_catalog_get_products`

Relevant to Graeham only if he ever builds a listings catalog for dynamic ads (each listing as a "product"). Until then, skip this family.

## 3. Accounts, pages & assets (3) — READ, call first

| Tool | Purpose |
|---|---|
| `ads_get_ad_accounts` | Ad accounts the authorized user can access — IDs, names, currency |
| `ads_get_ad_entities` | Campaigns, ad sets, ads within an account (status, structure) |
| `ads_get_pages_for_business` | Facebook Pages connected to Business Manager (ads need a Page identity) |

## 4. Datasets, tracking quality & errors (4) — READ

| Tool | Purpose |
|---|---|
| `ads_get_dataset_details` | Dataset (pixel + Conversions API) configuration |
| `ads_get_dataset_quality` | Event match quality score — how well events match Meta users |
| `ads_get_dataset_stats` | Event counts, deduplication between pixel and CAPI |
| `ads_get_errors` | Recent dataset errors |

Graeham's signal sources: graehamwatts.com pixel + GHL funnel events. Falling Lead-event match quality usually means form fields stopped passing email/phone.

## 5. Insights, benchmarks & performance (7) — READ

| Tool | Purpose | Notes |
|---|---|---|
| `ads_insights_performance_trend` | Historical trend per metric | The workhorse for week-over-week tables |
| `ads_insights_anomaly_signal` | KPI anomalies vs baseline | Surface verbatim in audits — it's Meta's own read |
| `ads_insights_industry_benchmark` | Compare vs industry average | Use real estate vertical; Bay Area context applies |
| `ads_insights_auction_ranking_benchmarks` | Auction CTR / CPM / quality rankings | "Below average quality ranking" = creative problem |
| `ads_insights_advertiser_context` | Advertiser industry / geography context | Sets up benchmark calls |
| `ads_get_opportunity_score` | Meta's account opportunity score + suggestions | Evaluate critically — suggestions often favor more spend |
| `ads_get_help_article` | Contextual Help Center articles | Troubleshooting lookups |

## Permission tiers (set during OAuth)

| Tier | Allows |
|---|---|
| read-only | Families 2-5 (lookups, insights, datasets, catalog reads) |
| read+write | + create/update/activate entities |
| read+write+financial | + budget changes |

If a write call fails on permissions, the connector was authorized at a lower tier — re-auth, don't retry.

## Sources

- Meta Business Help Center setup doc: facebook.com/business/help/1456422242197840
- Meta for Business launch announcement: facebook.com/business/news/meta-ads-ai-connectors
- Tool list compiled 2026-06-07 from the launch-week manifest; verify against live manifest when behavior differs.
