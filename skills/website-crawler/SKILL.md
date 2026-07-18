---
name: website-crawler
description: "General-purpose web page crawler — hand it any URL (a competitor's blog post, a market/housing data page, a news article, a city or county site, any arbitrary webpage) and get back clean markdown text instead of raw messy HTML. Built on Crawl4AI, running locally on Graeham's Windows machine. Use this whenever content-creation-engine, disclosure-analyzer, off-market-property-search, ai-library, price-reduction-angle-generator, or any other skill needs to read a webpage that isn't a social platform post — this is NOT for Reddit/Instagram/YouTube (those have their own dedicated scrapers/skills). Trigger on: crawl this site, crawl this page, scrape this URL, get clean text from this webpage, pull this article, fetch this page as markdown, read this webpage for me, general web crawling, structured extraction from a webpage. Also trigger any time the user pastes a plain article/blog/report URL and wants its content pulled into a doc, comparison, or research summary — even if they don't say 'crawl' explicitly."
---

# Website Crawler

> **One job, one skill.** Hand it a URL, get back clean markdown (or structured data, if you give it a schema). That's it.

## Why this exists, and why it's separate from content-creation-engine

Scraping shows up everywhere in this project — competitor research, market data pulls, disclosure cross-references, off-market property listings — but content-creation-engine already owns the *social platform* scrapers (Reddit via RSS, Instagram via Apify — see its `references/phases/content-ideation-engine/references/apify-actors.md`). Those are platform APIs with their own quirks and aren't what this skill is for.

This skill handles the other 90% of the web: an arbitrary blog post, a county assessor's page, a competitor agent's site, a news article, a market report. Any skill that needs "go read this webpage and give me clean text" should call this one instead of reimplementing scraping — that's the whole point of pulling it out as its own skill rather than burying it inside content-creation-engine.

## What it's built on

[Crawl4AI](https://github.com/unclecode/crawl4ai) — a free, self-hosted, open-source crawler (no API keys, no per-call cost, unlike Apify). The reason it's worth having over a basic `requests.get()` + regex scrape: most scrapers hand you raw HTML full of nav bars, ads, and scripts that you then have to hand-clean before an LLM can use it. Crawl4AI understands page structure and outputs clean markdown directly — reading order preserved, junk stripped — which is exactly the shape you want for dropping into a research doc, a content brief, or a RAG pipeline.

## How it runs

Same pattern as `video-transcriber`: Crawl4AI needs a real Chromium browser (via Playwright) to render pages properly, which is too heavy to install in the Cowork sandbox. So this runs on Graeham's Windows machine instead.

### One-time setup (Graeham runs this once in PowerShell)

```powershell
pip install -U crawl4ai
crawl4ai-setup
```

`crawl4ai-setup` downloads the Playwright Chromium browser it needs — this is the slow part (~200MB) but only happens once.

### Running a crawl

Claude writes the command, Graeham pastes it into PowerShell (same reason as video-transcriber: Windows Terminal is tier-"click", typing is blocked for security).

```powershell
python "C:\Users\Graeham Watts\Documents\Skills LLMS\Claude\Skills\skills\website-crawler\scripts\crawl.py" "https://example.com/some-article"
```

Prints clean markdown straight to the terminal. Add `--save` to also write it to a `.md` file next to the script, or `--output-dir <path>` to choose where.

### Structured extraction (pull specific fields, not the whole page)

If you need specific data points instead of the full article — e.g. price + address + bed/bath off a listing page — pass a CSS selector to scope the crawl, or a JSON schema for field-level extraction:

```powershell
python crawl.py "https://example.com/listing" --selector ".price, .address, .beds-baths"
```

For schema-based extraction, write a small JSON file describing the fields (see [Crawl4AI's extraction docs](https://docs.crawl4ai.com/extraction/no-llm-strategies/) for the exact shape) and pass it with `--schema schema.json`.

## When NOT to reach for this

- **Reddit, Instagram, YouTube, TikTok** — those go through content-creation-engine's existing Apify/RSS scrapers or the `youtube-scraper` / `instagram-competitor-scraper` skills. Different job, different tooling.
- **A page behind a login you don't have credentials for**, or a site whose terms explicitly prohibit scraping — don't use stealth mode to route around that. Crawl4AI's stealth mode is for basic bot-detection false positives (e.g. a site blocking all headless browsers indiscriminately), not for bypassing access controls.
- **Video transcription** — that's `video-transcriber`, not this.

## Known limits (be upfront about these, don't silently hide them)

- **Heavier than a plain text scraper** because it's running a real browser under the hood — fine for one-off or moderate-volume crawls, but don't reach for it if you just need to fetch a tiny static JSON API endpoint (plain `requests` is simpler there).
- **JavaScript-heavy sites** generally work fine since it renders in a real browser, but very aggressive anti-bot sites (Cloudflare challenge pages, etc.) may still block it. If a crawl comes back empty or clearly wrong, say so rather than presenting garbage as if it were the real page content.
- **Respect robots.txt and terms of service** in spirit — this is for research and content sourcing, not for building a scraping operation against a site that doesn't want to be crawled at volume.

## Status

Scaffolded 2026-07-18, not yet installed or run end-to-end. Graeham should run the one-time setup above and try it on a real URL before relying on it in a live workflow.
