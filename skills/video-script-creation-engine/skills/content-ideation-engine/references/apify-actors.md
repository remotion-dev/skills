# Apify Actor Reference

All actor IDs and their input schemas for the content-ideation-engine.

---

## 1. Reddit Scraper Lite — PRIMARY SOURCE (Phase 2)

- **Actor ID:** `trudax/reddit-scraper-lite`
- **URL:** https://apify.com/trudax/reddit-scraper-lite
- **Pricing:** $3.40 per 1,000 results stored (Pay-Per-Result model)
- **Why this one:** 18K users, 2.5K monthly active, rating 4.3/5, maintained recently, uses built-in cheap proxies (cheaper than the non-Lite version that requires Residential proxies)
- **No login required.** Scrapes public Reddit data as an unofficial API.

### Input schema (what we send to the actor)

```json
{
  "startUrls": [
    {"url": "https://www.reddit.com/r/BayArea/hot/"}
  ],
  "searches": [],
  "maxItems": 225,
  "maxPostCount": 15,
  "maxComments": 3,
  "maxCommunitiesCount": 0,
  "maxUserCount": 0,
  "sort": "hot",
  "time": "week",
  "scrollTimeout": 40,
  "skipUserPosts": true,
  "includeNSFW": false,
  "proxy": {"useApifyProxy": true},
  "debugMode": false
}
```

### Parameter explanations

| Parameter | Our value | Why |
|---|---|---|
| `startUrls` | List of subreddit URLs | We want specific subreddits, not keyword search |
| `maxItems` | 225 | Hard cap on total items returned — safety net for cost |
| `maxPostCount` | 15 | Per-subreddit cap on posts (15 posts × 15 subs = 225 max) |
| `maxComments` | 3 | Only top 3 comments per post — enough to gauge sentiment without over-scraping |
| `sort` | "hot" | "Hot" = currently-engaging posts (best for content ideation) |
| `time` | "week" | Only last 7 days — fresh signal, not stale threads |
| `skipUserPosts` | true | We don't care about user profile pages |
| `includeNSFW` | false | Obvious |
| `proxy.useApifyProxy` | true | Required to avoid being IP-blocked by Reddit |

### Output format (what we get back)

Each item in the dataset is one of: `post`, `comment`, `community`, or `user`. For ideation we mostly care about `post` and `comment` items.

**Post item example:**
```json
{
  "id": "t3_144w7sn",
  "url": "https://www.reddit.com/r/BayArea/comments/.../",
  "username": "SomeUser",
  "title": "Selling my Meta stock to buy a house in Menlo Park — am I crazy?",
  "communityName": "r/BayArea",
  "body": "Full post text here...",
  "numberOfComments": 47,
  "upVotes": 234,
  "createdAt": "2026-04-08T14:22:15.000Z",
  "dataType": "post"
}
```

**Comment item example:**
```json
{
  "id": "t1_jnhqrgg",
  "parentId": "t3_144v5c3",
  "username": "SomeUser",
  "body": "Comment text here...",
  "upVotes": 12,
  "numberOfreplies": 3,
  "createdAt": "2026-04-08T15:00:00.000Z",
  "dataType": "comment"
}
```

### Cost math for typical runs

| Tier | Subreddits | maxItems | Est. cost |
|---|---|---|---|
| Tier 1 (test) | 5 core | 75 | ~$0.26 |
| Tier 1+2 (standard) | 15 | 225 | ~$0.77 |
| Full run | 20+ | 400 | ~$1.36 |

**Weekly cadence estimate:** Tier 1+2 every week = ~$3.08/month. Well under Starter plan budget.

---

## 2. Zillow Neighborhood Reviews — SECONDARY (Phase 2b)

*Not wired up yet. Placeholder for Phase 2b build.*

- **Candidates to evaluate:** search Apify store for `zillow neighborhood reviews` — look for actors that scrape the "People's Reviews" section on Zillow neighborhood pages
- **Target data:** resident reviews for EPA, RWC, PA, MP, SMC neighborhoods
- **Use case:** extract authentic "what it's like to live here" quotes for lifestyle (TOFU) content

---

## 3. City-Data Forums — SECONDARY (Phase 2b)

*Not wired up yet. Placeholder for Phase 2b build.*

- **Candidates to evaluate:** Apify store search `city-data forums` or `phpBB scraper`
- **Target:** Bay Area / Peninsula city forums on city-data.com for resident Q&A and market gossip
- **Use case:** Find BOFU trigger moments ("I'm moving to Redwood City, what should I know?")

---

## How to run an actor from Python

See `../scripts/run_reddit_ideation.py` for the full working script. The core pattern is:

```python
from apify_client import ApifyClient
from dotenv import load_dotenv
import os

load_dotenv()
client = ApifyClient(os.environ["APIFY_API_TOKEN"])

run_input = { ... }  # see schema above
run = client.actor("trudax/reddit-scraper-lite").call(run_input=run_input)

# Fetch results
items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
```
