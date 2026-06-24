# Reddit RSS + Public JSON — Free, No-Approval Data Source

> **Added 2026-06-23.** This is the official, free, no-approval way to read public Reddit
> for content ideation. It replaces the dead "waiting on the Reddit Data API ticket" plan.
> The support-ticket API path was the wrong door (Reddit's commercial/enterprise data gate,
> ~$12,000/month minimum) and will keep auto-denying a low-volume use case. Stop waiting on it.

## Why this exists

The content engine needs to read what Bay Area buyers and sellers are asking on Reddit.
There are three ways to get that data. This file documents the two FREE public ones. The
paid Apify scraper is documented separately in
`phases/content-ideation-engine/references/apify-actors.md`.

| Method | Cost | Approval | Best for | Limitation |
|---|---|---|---|---|
| **RSS feeds** | Free | None | Discovery — titles, links, authors, post dates | No upvote/comment counts in the feed |
| **Public `.json` endpoints** | Free | None (now gated) | Engagement scoring — upvotes, comment counts, body text | **As of 2026-06-23 returns HTTP 403 unauthenticated.** Use the free OAuth app (§3) to reach these fields |
| Apify scraper (separate file) | ~$0.30–$1.00/run | None | High-volume, proxied, reliable bulk sweeps | Pay-per-result; unofficial |

**Tested 2026-06-23 (Graeham's machine).** The **RSS feeds work** — a Tier 1 run pulled 100 real
posts (with ~6–8s spacing to dodge 429s). The unauthenticated **`.json` endpoints now return HTTP
403** — Reddit gates them. So today the free path is: **RSS for discovery** (titles, links, what's
being asked), and the **free OAuth app** (§3) to restore the engagement fields (`ups`,
`num_comments`) that anonymous `.json` used to give. RSS alone cannot compute
`reddit_engagement_score` (no upvote/comment counts in the feed).

**Runnable fetcher:** `scripts/run_reddit_rss.py` (standard library only, no install). Example:
`python run_reddit_rss.py --tier 1 --rss --delay 8`. Output is normalized to the same schema the
Apify script produces, so it is a drop-in. It auto-retries on 429 and reports any subs that block.

---

## 1. RSS feeds (discovery)

Append `.rss` to any subreddit listing URL. No key, no auth, no proxy.

| Feed | URL pattern |
|---|---|
| New posts | `https://www.reddit.com/r/<sub>/new/.rss` |
| Hot posts | `https://www.reddit.com/r/<sub>/hot/.rss` |
| Top this week | `https://www.reddit.com/r/<sub>/top/.rss?t=week` |
| Keyword search in one sub | `https://www.reddit.com/r/<sub>/search.rss?q=<query>&restrict_sr=1&sort=new` |

**Fields you get per item:** `title`, `link` (always preserve it), `author`, `published`,
and an HTML `content` blob (the post body). You do **not** get upvote or comment counts from
RSS — for those, use the `.json` endpoint below.

**Ready-to-use feed list** mirrors the curated tiers in
`phases/content-ideation-engine/references/subreddit-list.md`:

```
# Tier 1 — CORE
https://www.reddit.com/r/BayArea/hot/.rss
https://www.reddit.com/r/bayarearealestate/new/.rss
https://www.reddit.com/r/RealEstate/hot/.rss
https://www.reddit.com/r/FirstTimeHomeBuyer/new/.rss
https://www.reddit.com/r/Layoffs/hot/.rss
```

Add Tier 2 / Tier 3 subs from `subreddit-list.md` the same way (swap the sub name, keep the
`/new/.rss` or `/hot/.rss` suffix per that file's sort strategy).

---

## 2. Public `.json` endpoints (engagement scoring)

Append `.json` to the same listing URLs to get structured data including the engagement
fields the ideation rubric needs.

| Endpoint | URL pattern |
|---|---|
| New posts | `https://www.reddit.com/r/<sub>/new.json?limit=25` |
| Hot posts | `https://www.reddit.com/r/<sub>/hot.json?limit=25` |
| Top this week | `https://www.reddit.com/r/<sub>/top.json?t=week&limit=25` |
| Search | `https://www.reddit.com/r/<sub>/search.json?q=<query>&restrict_sr=1&sort=new&limit=25` |

**Fields you get per post** (`data.children[].data`): `title`, `selftext`, `permalink`,
`author`, `ups` (upvotes), `num_comments`, `created_utc`, `subreddit`. That is everything
needed to compute an engagement score and apply the ">50 upvotes in 30 days" filter.

**Required headers / etiquette:**
- Set a descriptive `User-Agent`, e.g. `script:propcast_research:v1.0 (by /u/<reddit_username>)`.
  Generic agents get blocked.
- Keep polling light (a few requests per minute, not a tight loop). Unauthenticated reads are
  rate-limited; a 429 means back off.
- Run from a residential or home IP if possible. Datacenter IPs are the ones Reddit 403s.

---

## 3. When to upgrade past the free public endpoints

If volume or reliability outgrows the public endpoints, the correct next step is **NOT** the
commercial Data API ticket. It is the **free self-serve OAuth app**:

1. Create a dedicated (non-personal) Reddit account for the business.
2. At `reddit.com/prefs/apps`, create a **script** app (redirect URI `http://localhost:8080`).
3. Authenticate with OAuth2 client-credentials (~100 requests/minute, free).
4. Keep the same `User-Agent` format.

Use a **dedicated** account so a rate-limit or terms dispute never touches a personal login.

**When the commercial tier becomes the right call.** The enterprise Data API contract (~$12,000/month)
is not ruled out forever — it is wrong only at today's low volume. Revisit it if and when the product
reaches commercial scale: high-volume ingestion across many agents, or any feature that stores, displays,
or redistributes Reddit data in-product. At that point a commercial contract becomes both justified and
required, and this whole free-endpoint approach is retired.

---

## 4. Compliance guardrails (non-negotiable)

- **Research and ideation only.** Read public posts to understand demand and inform original
  content Graeham writes himself.
- **Do NOT store, republish, redistribute, or display Reddit content** as a feature inside any
  product (that crosses into Reddit's paid-contract territory).
- **Do NOT use Reddit content to train or fine-tune any model.**
- Always preserve the source `link`/`permalink` on every item, same as the Instagram rule.
