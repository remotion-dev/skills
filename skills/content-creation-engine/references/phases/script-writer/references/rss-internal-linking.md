# RSS-Based Internal Linking

> **Read by Phase 5 (script-writer) when generating blog post derivatives.** Adds 2-4 contextual internal links per blog post by scraping graehamwatts.com's existing content.

Internal linking is one of the highest-leverage SEO moves. Links between Graeham's existing posts (1) keep readers on his site longer, (2) signal topical authority to Google, and (3) help AI search engines understand his content cluster.

The trick: links must be **semantically relevant** and **inserted naturally** in body text — not as a "Related Posts" list at the bottom (which AI ignores) and not forced into irrelevant paragraphs (which reads as spam).

---

## How It Works

When Phase 5 generates a blog derivative, it:

1. Identifies the blog's primary topic and 2-3 supporting topics
2. Scrapes graehamwatts.com to find existing posts that match those topics
3. Picks 2-4 best matches
4. Inserts inline links in the body where they read naturally

---

## Step 1: Find Existing Posts

Try these approaches in order. First one that works wins.

### Approach A: RSS Feed (Preferred)

Use Claude in Chrome MCP to navigate to:
`https://graehamwatts.com/feed/`

If WordPress / Squarespace / similar, this returns an XML feed of recent posts with `<title>` and `<link>` for each. Extract:
- Title
- URL (the `<link>` field)
- Publish date (the `<pubDate>` field)
- Summary (the `<description>` field — 150-300 chars usually)

Collect the 50 most recent posts (RSS feeds typically cap at 10-50; extend with `?paged=2` if available).

### Approach B: Sitemap.xml (If RSS Returns 404 or Empty)

Navigate to:
`https://graehamwatts.com/sitemap.xml`
or
`https://graehamwatts.com/sitemap_index.xml`

Extract all blog post URLs. For each URL, navigate and grab:
- Page `<title>` tag
- Meta description (`<meta name="description">`)
- H1

This is slower than RSS but works on any site.

### Approach C: Direct Browse (Fallback)

If both RSS and sitemap fail, navigate to:
`https://graehamwatts.com/blog`

Scroll the blog index, collect post titles + URLs from the listing.

---

## Step 2: Match Topics

For each existing post collected in Step 1, score topical relevance to the new blog being generated. Use this rubric:

| Match level | Definition | Example |
|---|---|---|
| **Strong** | Same topic, different angle | New blog about "EPA market update" + existing post about "EPA homes under $1M" |
| **Moderate** | Adjacent topic, same audience | New blog about "EPA market" + existing post about "Should I buy in EPA or PA" |
| **Weak** | Same broad pillar, different audience or angle | New blog about EPA buyers + existing post about Bay Area sellers |
| **None** | Unrelated | New blog about EPA market + existing post about "what is escrow" |

Pick **2-4 internal links** total. Mix Strong and Moderate matches. Avoid Weak unless topical authority around a pillar matters and you have nothing closer.

If fewer than 2 matches exist (new blog with rare topic), insert what you have. Don't force weak matches.

---

## Step 3: Insert Links Naturally

Internal links go INLINE in body text, anchored to descriptive phrases — not "click here," not "this post," not as a "Related Posts" list at the bottom.

### Good

> "Bay Area buyers asking about commute facts often weigh [Caltrain access vs freeway proximity](https://graehamwatts.com/blog/bay-area-commute-comparison) when picking neighborhoods."

> "I've covered [why pricing aggressively matters more in slowing markets](https://graehamwatts.com/blog/pricing-strategy-slow-market) before — that lesson still applies here."

### Bad

> "For more info, [click here](https://graehamwatts.com/blog/...)." (zero anchor-text value)

> "Check out [this post](https://graehamwatts.com/blog/...) for details." (vague)

> "Related Posts: [Post 1](...), [Post 2](...)" (AI search engines and Google's algorithm both downweight grouped link lists at the bottom of articles)

### Anchor Text Rules

- 3-7 words
- Descriptive of the linked post's content
- Reads naturally in the surrounding sentence (no obvious "and now here's a link" awkwardness)
- Includes a keyword from the linked post's title when natural

---

## Step 4: Verify

Before final output:

1. **Confirm each link URL is live** — navigate to the URL via Claude in Chrome to verify it returns 200, not 404. If a post has been deleted or moved, drop the link.
2. **Confirm anchor text isn't repeated** — same anchor text on multiple links in one post hurts SEO.
3. **Confirm link distribution** — links should be spread across the blog body, not clustered in one paragraph.

---

## Edge Cases

| Situation | Handling |
|---|---|
| graehamwatts.com is down / unreachable | Skip internal linking entirely. Note in output: "Internal linking skipped — site unreachable." |
| RSS / sitemap returns no posts | Try Approach C (direct browse). If that also fails, skip. |
| Fewer than 2 relevant existing posts | Insert what you have. Don't force weak matches. |
| New blog topic has zero overlap with existing content | Skip internal linking. Note "no relevant existing posts found." |
| Existing post has been deleted (URL returns 404 in Step 4) | Drop that link, find another match if possible |

---

## What This Module Does NOT Do

- Does not edit existing posts (one-way: links in NEW post, point to OLD posts)
- Does not deduplicate. If a topic is genuinely covered well in 5 existing posts, only link to 2-4. Don't link all 5.
- Does not handle external links (those follow different rules — see `seo-keywords.md` and `aeo-geo-requirements.md`)
- Does not cache. Each blog generation re-scrapes RSS. Cheap and ensures freshness.

---

## Used By

- Phase 5 (script-writer) — invoked when format = blog-post-draft
- Could be invoked by `content-creation-engine` directly if a user asks "find internal linking opportunities for this draft"
