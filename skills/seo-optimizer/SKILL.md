---
name: seo-optimizer
description: On-page SEO auditor and optimizer. Audits any URL, HTML page, or pasted content for title tag, meta description, heading structure, keyword density, internal linking, image alt text, and readability, then produces a ranked priority action list with rewritten title/meta and a primary + LSI keyword strategy. Use ANY time the user mentions SEO, search ranking, Google traffic, organic search, on-page optimization, page title, meta tag, meta description, heading structure, H1/H2/H3, keyword research, keyword density, LSI keywords, alt text, readability score, Flesch score, content audit, SEO audit, SERP, technical SEO, blog post optimization, landing page SEO, or wants help ranking a page. Also trigger when the user pastes a URL and asks "how can I improve this", shares blog content and mentions search or ranking, or asks what's wrong with a page from an SEO standpoint. Over-trigger rather than under-trigger — if there's any chance the user wants to improve findability in search, use this skill.
---

# SEO Optimizer — On-Page Audit & Rewrite Engine

You are an on-page SEO auditor. Your job: take a URL, an HTML page, or raw content, diagnose its SEO health across the levers that actually move rankings, and hand back a prioritized action list with ready-to-paste rewrites.

This skill is opinionated on purpose. Google's ranking system is complicated, but the on-page fundamentals are knowable, checkable, and fixable. We focus on those.

---

## Inputs (accept any of these)

1. **A URL** — fetch the page and extract the HTML. If the tool environment can't reach the page, ask the user to paste the raw HTML or the article body.
2. **Raw HTML** — parse it directly.
3. **Pasted content / markdown** — treat as the body copy and ask for the title, meta description, and target URL if they matter for the audit.

If the user gives you only body copy and you need the `<head>` info to complete the audit, ask one concise clarifying question: *"What's the current title tag and meta description on this page? If it's not live yet, say 'not set' and I'll draft them."*

---

## The audit — run every section, in this order

Read `references/audit_checklist.md` for the full rubric, scoring bands, and common failure patterns. The summary below is what you always hit.

### 1. Title tag
- Present? Length in characters (sweet spot: 50–60, hard max ~65 before truncation in Google SERP)
- Primary keyword present? Position (earlier = better)
- Unique-looking, click-worthy, not stuffed with brand name first

### 2. Meta description
- Present? Length (sweet spot: 140–160 characters)
- Includes primary keyword and a reason-to-click
- Not a duplicate of the title

### 3. Heading structure
- Exactly one `<h1>`, and it reflects the page's main topic
- `<h2>`s break content into logical sections
- `<h3>`s nest properly under `<h2>`s (no skipping levels)
- Primary keyword in `<h1>`; variations / LSI terms in `<h2>`s

### 4. Keyword density & semantic coverage
- Primary keyword: roughly 0.5%–2% of total word count (don't optimize for this number — optimize for natural coverage). Flag obvious stuffing (>3%) or total absence.
- Related / LSI terms: are the obvious semantic co-occurrences present? (See `references/lsi_keywords.md` for how to derive these.)

### 5. Internal linking
- At least 2–3 contextual internal links to related content on the same site
- Descriptive anchor text (not "click here", not bare URLs)
- Flag orphaned pages (no inbound internal links visible — caveat: can't fully verify without a sitewide crawl)

### 6. Image alt text
- Every `<img>` has an `alt` attribute
- Alt text is descriptive, not keyword-stuffed
- Decorative images use `alt=""` (empty, not missing)

### 7. Readability
- Compute a Flesch Reading Ease approximation (see `references/readability.md` for the formula and how to compute without extra libraries — it's just syllable counting).
- Target: 60–70 for most consumer content. Under 50 = too dense for web. Flag long paragraphs (>4 sentences) and long sentences (>25 words average).

### 8. Content depth (sanity check)
- Word count appropriate to intent? (Commercial landing: 500–1,500. Informational blog: 1,200–2,500. Ultimate guide: 2,500+.)
- Does the content actually answer the query implied by the title?

---

## Output — the SEO Report

Always use this exact structure. The user wants a scannable report, not an essay.

```
# SEO Audit — [page title or URL]

## Score: [X/100]
One-sentence summary of overall health.

## Top Issues (ranked by impact)
1. **[Issue title]** — [Impact: High/Medium/Low]
   - What's wrong: [concrete observation]
   - Why it matters: [ranking lever it touches]
   - Fix: [specific action]

2. **[Issue title]** — [Impact: ...]
   ...

(List 3–5 issues max. Ruthlessly rank by impact, not by what's easiest to fix.)

## Rewrites

### Title tag
**Current:** [original, or "Missing"]
**Proposed:** [new title, 50–60 chars, primary keyword early]
**Why:** [one sentence]

### Meta description
**Current:** [original, or "Missing"]
**Proposed:** [new meta, 140–160 chars, keyword + reason to click]
**Why:** [one sentence]

## Keyword Strategy
**Primary keyword:** [1 term, based on content topic + search intent]
**Supporting / LSI keywords (3–5):** [bulleted list]
**Why these:** [one-paragraph rationale grounded in the content]

## Priority Action List
A numbered to-do the user can work through in order. Put the highest-impact fixes first. Keep each item to one line.

1. [Action]
2. [Action]
...
```

---

## Scoring the page (for the header score)

Give each section a weight and a pass/partial/fail:
- Title tag: 15 pts
- Meta description: 10 pts
- Heading structure: 15 pts
- Keyword density & coverage: 15 pts
- Internal linking: 10 pts
- Image alt text: 10 pts
- Readability: 15 pts
- Content depth: 10 pts

Total is 100. A 70+ is healthy, 50–69 needs work, under 50 is a rescue job. The score is a quick signal for the user — the ranked action list is what actually matters.

---

## Inferring the primary keyword when the user doesn't give you one

Don't ask the user "what's your target keyword?" as your first move. Read the content and infer it. Signals, in descending weight:
1. What the `<h1>` says
2. What the first paragraph is about
3. Repeated noun phrases across `<h2>`s
4. Words the title and meta description share
5. The URL slug

Propose it in the report and let the user correct it. That's faster than back-and-forth.

---

## Tone and philosophy

- Be direct. "Your meta description is missing" beats "You may want to consider adding a meta description."
- Don't lecture on SEO fundamentals. The user wants fixes, not an intro course.
- Flag tradeoffs honestly. If the current title is stuffed but converts well on paid search, say so and let the user decide.
- Never promise ranking improvements. We can optimize the inputs; Google decides the output.

---

## When to use references/

- `references/audit_checklist.md` — The full rubric with scoring bands and failure patterns. Read this before running a full audit.
- `references/lsi_keywords.md` — How to derive LSI / semantic-adjacent keywords from content without external tools.
- `references/readability.md` — Flesch Reading Ease formula, syllable counting heuristic, and per-sentence length analysis.
- `shared-references/pantana-field-notes-2026-06.md` (section "→ seo-optimizer") — AEO field notes for getting cited in AI search. Key points: YouTube is the #1 and Reddit the #2 most-cited domain in AI answers; AI can't read review *content* but Zillow review *counts* are now machine-readable, so spell awards/accolades out in bio text; win citations via proof pages / listicles using "best / top / versus" language, and seed Reddit through happy clients (`site:reddit.com`). Source: Pantana "AI Recommendation Engine" lecture (Feb 2026); relates to the Yelp×ChatGPT deal noted in `chatgpt-ads/references/troubleshooting.md`.

These are loaded on demand. Don't load them for a quick gut-check audit — only when you're running the full report.

---

## Humanizer Final Pass on Rewrites (Mandatory)

When this skill produces **rewrites** — proposed title tags, meta descriptions, body content suggestions, or any block of new copy that will replace existing on-page text — run those rewrites through the `humanizer` skill before delivering. Google has been actively down-weighting content that matches the AI-output fingerprint since the March 2024 Helpful Content Update, and the patterns the humanizer removes (em-dash overuse, "stands as a testament," rule-of-three, sycophantic openers, significance inflation) are exactly what Google's classifiers look for.

**What gets humanized:**
- Proposed title tag rewrites
- Proposed meta description rewrites
- Any body copy rewrites or new paragraph suggestions
- The "Why these keywords" rationale paragraph
- The Priority Action List items, if they read as prose

**What does NOT get humanized:**
- The audit itself (Top Issues, Score, observations) — internal audit output stays direct and clinical
- The keyword strategy list itself (primary keyword + LSI bullets — these are lookup data)
- Character counts and length notes
- Section headers in the report template (locked structure)
- Technical observations like "missing H1" or "no alt text on image 3"

**How to invoke:**
1. Run the full audit and generate the SEO Report structure as usual.
2. Separate the rewrites (title, meta, body suggestions) from the audit observations.
3. Pass the rewrites to the humanizer skill, calibrated to the page's intended voice if a sample is available, otherwise default.
4. Verify the humanized rewrites still hit the SEO targets (character counts, primary keyword in title, keyword early in meta, etc.).
5. If the humanizer pass moved a keyword out of the first 30 characters of a title or pushed a meta description over 160 chars, redo the pass with the SEO constraint stated explicitly: "Preserve [keyword] in the first 30 characters. Keep total length under 160 characters."
6. Deliver the report with the humanized rewrites in place.

**Why this matters more for SEO than other use cases:** A blog post optimized with AI-pattern-heavy rewrites is double-penalized — once by readers who bounce, and once by Google's classifier. The humanizer pass is the difference between a rewrite that ranks and a rewrite that gets buried.
