# On-Page SEO Audit Checklist — Full Rubric

This is the full scoring rubric referenced from SKILL.md. Use this when running a full audit and scoring the page out of 100.

## Table of contents
- Section 1: Title tag (15 pts)
- Section 2: Meta description (10 pts)
- Section 3: Heading structure (15 pts)
- Section 4: Keyword density & semantic coverage (15 pts)
- Section 5: Internal linking (10 pts)
- Section 6: Image alt text (10 pts)
- Section 7: Readability (15 pts)
- Section 8: Content depth (10 pts)
- Common failure patterns
- How to handle missing inputs

---

## Section 1: Title tag (15 pts)

| Check | Full (15) | Partial (7–14) | Fail (0–6) |
|---|---|---|---|
| Present | Yes | N/A | No |
| Length | 50–60 chars | 40–49 or 61–65 | <40 or >65 |
| Primary keyword | In first 3 words | Present but late | Missing |
| Clickworthy | Yes (a human would click) | Descriptive but flat | Generic/stuffed |
| Unique | Unique across site | Minor duplication | Exact duplicate |

**Common failure patterns:**
- Brand name first ("Acme Corp | Widget X") — move brand to the end
- Pipe-separated keyword stuffing ("Widget X | Best Widget | Buy Widget | Widget Store")
- Title = `<h1>` verbatim — they can differ and probably should
- Title truncation (>65 chars) — Google will cut mid-word

## Section 2: Meta description (10 pts)

| Check | Full (10) | Partial (5–9) | Fail (0–4) |
|---|---|---|---|
| Present | Yes | N/A | No |
| Length | 140–160 chars | 100–139 or 161–180 | <100 or >180 |
| Primary keyword | Present | Mentioned via synonym | Missing |
| Reason to click | Clear value prop or curiosity hook | Descriptive only | Pure summary |

**Common failure patterns:**
- Auto-generated from first paragraph — often truncates mid-sentence
- Exact copy of the title
- Stuffed with keywords, no hook
- Written for the search engine, not the human

## Section 3: Heading structure (15 pts)

| Check | Full | Partial | Fail |
|---|---|---|---|
| Exactly one `<h1>` | Yes | 0 or 2+ `<h1>`s | Multiple `<h1>`s scattered |
| Logical hierarchy | H1 → H2 → H3, no skips | Occasional skip | Chaos |
| Keyword in H1 | Yes, natural | Related term | Missing entirely |
| H2s break content | Yes, section-level | Too few or too many | No H2s at all |

**Common failure patterns:**
- `<h1>` is a logo or nav element (check that `<h1>` is actually the page title)
- Visual headings styled as `<div>` or `<p>` — no semantic heading at all
- H1 → H4 skip (skipping H2/H3)
- Every paragraph has its own `<h3>` above it

## Section 4: Keyword density & semantic coverage (15 pts)

Don't over-index on density percentages. The modern ranking signal is topical coverage, not keyword repetition.

| Check | Full | Partial | Fail |
|---|---|---|---|
| Primary keyword density | 0.5%–2% | 0.2%–0.4% or 2%–3% | 0% or >3% (stuffing) |
| Primary in first 100 words | Yes | In first 300 | Not until mid-page |
| LSI / semantic terms | 4+ present naturally | 1–3 present | None |
| Reads naturally | Yes | Slightly forced | Obvious SEO writing |

**Common failure patterns:**
- Keyword appears only in title and meta, never in body
- Every H2 starts with the primary keyword — unnatural
- Exact-match phrase repeated 20+ times

## Section 5: Internal linking (10 pts)

| Check | Full (10) | Partial | Fail |
|---|---|---|---|
| At least 2–3 contextual internal links | Yes | 1 link | 0 links |
| Descriptive anchor text | Specific and relevant | Somewhat generic | "click here", "read more" |
| Links to related content | Topically adjacent | Tangential | Random |

**Note:** We can't audit the inbound link graph (what links TO this page) without a sitewide crawl. Flag this as a limitation in the report when relevant.

## Section 6: Image alt text (10 pts)

| Check | Full (10) | Partial | Fail |
|---|---|---|---|
| Every `<img>` has `alt` | 100% | 50%–99% | <50% |
| Alt describes image | Descriptive, natural | Terse or generic ("image1.jpg") | Stuffed with keywords |
| Decorative images | `alt=""` (empty, present) | Missing alt on decorative | Stuffed alt on decorative |

**Common failure patterns:**
- CMS auto-fills alt with the filename — almost always useless
- Same alt text on multiple images
- Alt text that's just the primary keyword repeated

## Section 7: Readability (15 pts)

| Check | Full | Partial | Fail |
|---|---|---|---|
| Flesch Reading Ease | 60–75 | 50–59 or 76–85 | <50 or >85 |
| Avg sentence length | 15–20 words | 21–25 or 10–14 | >25 or <10 |
| Avg paragraph length | 2–4 sentences | 5–6 sentences | >6 or one-sentence walls |
| Scannability | Lists, bold, subheads | Some structure | Wall of text |

See `readability.md` for the Flesch formula and syllable-counting heuristic.

**Common failure patterns:**
- Academic tone on a consumer page
- 50-word sentences packed with commas
- Paragraphs that span half the viewport
- Zero visual hierarchy — no bold, no lists, no subheads

## Section 8: Content depth (10 pts)

| Check | Full (10) | Partial | Fail |
|---|---|---|---|
| Length matches intent | Yes | Close | Wildly off |
| Answers the title's question | Yes, directly | Eventually | Tangentially |
| Includes supporting context (examples, data, visuals) | Yes | Some | None |

Intent-to-length mapping:
- Commercial / product landing: 500–1,500 words
- Informational blog post: 1,200–2,500 words
- Ultimate guide / pillar page: 2,500+ words
- Local service page: 600–1,200 words with location signals

**Common failure pattern:** a "guide" that's 400 words. Google will rank a competitor's 3,000-word page every time.

---

## How to handle missing inputs

- **No title or meta visible** — if the user gave you body-only content, ask once: "What's the current title tag and meta description? If not set, I'll draft them."
- **No URL, no HTML** — skip internal linking and image alt sections, note them as "not assessable."
- **Pasted markdown** — convert headings mentally (# = H1, ## = H2, etc.) and audit the logical structure.
- **Foreign language content** — the mechanics still apply. Flag if the user wants keyword strategy in that language specifically.

---

## Scoring aggregation

Sum the weighted sub-scores. Report as `Score: XX/100`.

- 85–100: Excellent. Minor polish only.
- 70–84: Healthy. 1–2 meaningful improvements available.
- 50–69: Needs work. 3–5 changes will meaningfully move the needle.
- <50: Rescue job. Rewrite is likely faster than patching.

Never round up to flatter the user. The score is a signal for them to make decisions.
