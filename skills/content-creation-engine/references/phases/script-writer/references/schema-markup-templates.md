# Schema Markup Templates (JSON-LD)

> **Read by Phase 5 (script-writer) when generating blog post derivatives.** Adds structured-data schema markup to every blog post for AEO citation and rich-result eligibility on Google.

Schema markup is invisible to human readers but parsed by AI search engines (ChatGPT, Perplexity, Gemini), Google AI Overviews, and traditional Google rich results. Adding the right schema dramatically improves the odds that AI search engines cite Graeham's content directly.

This file contains copy-paste-ready JSON-LD templates for the 5 schema types that matter for real estate blog content. Phase 5 selects which ones apply to a given blog post and outputs them inside `<script type="application/ld+json">` tags at the bottom of the blog body.

---

## Required: Article Schema (Every Blog Post)

Every blog post on graehamwatts.com gets Article schema. No exceptions.

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "[FULL BLOG POST TITLE — under 110 chars for safety]",
  "description": "[META DESCRIPTION — 150-160 chars, same as the blog's meta description]",
  "image": [
    "[URL to hero image — usually the YouTube thumbnail if video-based, otherwise a stock or custom image]"
  ],
  "author": {
    "@type": "Person",
    "name": "Graeham Watts",
    "url": "https://graehamwatts.com/about",
    "jobTitle": "REALTOR",
    "affiliation": {
      "@type": "RealEstateAgent",
      "name": "Intero Real Estate",
      "url": "https://intero.com"
    },
    "identifier": {
      "@type": "PropertyValue",
      "propertyID": "DRE",
      "value": "01466876"
    }
  },
  "publisher": {
    "@type": "Organization",
    "name": "Graeham Watts",
    "url": "https://graehamwatts.com",
    "logo": {
      "@type": "ImageObject",
      "url": "https://images.leadconnectorhq.com/image/f_webp/q_80/r_1200/u_https://assets.cdn.filesafe.space/6wuU3haUH7uNeT20E3UZ/media/691256870b647e40e3c2e105.png"
    }
  },
  "datePublished": "[ISO 8601 publish date — YYYY-MM-DDTHH:MM:SS-07:00 for PST]",
  "dateModified": "[ISO 8601 modified date — same as publish unless edited later]",
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://graehamwatts.com/blog/[SLUG]"
  },
  "articleSection": "[Real Estate / Market Update / Buyer Tips / Seller Tips / Local Area / etc.]",
  "keywords": "[comma-separated keywords from the post]"
}
```

**Implementation notes:**
- DRE is read from `../../../../shared-references/identity.json`. NEVER hardcode 01466876 — read it at runtime. The schema generator must `Read` identity.json and inject the value.
- Logo URL is the hardcoded GHL CDN logo Graeham uses across his stack.
- `articleSection` matches Graeham's content pillar — use the pillar name from `content-pillars.md`.
- `keywords` should match the blog's target keyword set, typically 5-8 terms.

---

## Required When Q&A Section Exists: FAQPage Schema

Most blog posts on graehamwatts.com end with a 2-3 question FAQ section. When that's present, add FAQPage schema. This dramatically improves rich-result eligibility AND AI search citation rates.

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "[Q1 — the question text exactly as it appears in the blog FAQ section]",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[A1 — the answer text exactly as it appears, plain text not HTML]"
      }
    },
    {
      "@type": "Question",
      "name": "[Q2]",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[A2]"
      }
    },
    {
      "@type": "Question",
      "name": "[Q3]",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[A3]"
      }
    }
  ]
}
```

**Implementation notes:**
- Question text must match the H3 in the blog body exactly. Mismatches cause Google to reject the schema.
- Answer text should be 50-300 chars per answer for best AEO citation results.
- Use plain text, not HTML, in the answer fields.

---

## Required When YouTube Embed Exists: VideoObject Schema

When a blog post embeds a YouTube video (typical for Graeham's video-to-blog repurposing pipeline), add VideoObject schema. This connects the blog and video for SEO and helps both surface in AI search.

```json
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "[VIDEO TITLE]",
  "description": "[VIDEO DESCRIPTION — 150-300 chars, can be the blog's first paragraph]",
  "thumbnailUrl": [
    "https://i.ytimg.com/vi/[VIDEO_ID]/maxresdefault.jpg"
  ],
  "uploadDate": "[ISO 8601 — when the YouTube video was uploaded]",
  "contentUrl": "https://www.youtube.com/watch?v=[VIDEO_ID]",
  "embedUrl": "https://www.youtube.com/embed/[VIDEO_ID]",
  "duration": "[ISO 8601 duration, e.g., PT5M30S for 5 min 30 sec]",
  "publisher": {
    "@type": "Organization",
    "name": "Graeham Watts",
    "logo": {
      "@type": "ImageObject",
      "url": "https://images.leadconnectorhq.com/image/f_webp/q_80/r_1200/u_https://assets.cdn.filesafe.space/6wuU3haUH7uNeT20E3UZ/media/691256870b647e40e3c2e105.png"
    }
  }
}
```

**Implementation notes:**
- `thumbnailUrl` uses YouTube's auto-generated `maxresdefault.jpg` — works for any video. If video has no maxres thumbnail, fall back to `hqdefault.jpg`.
- `duration` is required by Google for video rich results. Calculate from the transcript word count if exact duration is unknown: `(word_count / 150) * 60` seconds, format as `PT[H]H[M]M[S]S`.

---

## Optional When Step-by-Step Content Exists: HowTo Schema

Use when the blog body is genuinely a step-by-step (e.g., "How to Buy a Home in San Mateo County in 2026 — 7 Steps"). Don't force this — most blog posts are NOT how-to format. Only use when the content is naturally numbered steps.

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "[FULL BLOG POST TITLE]",
  "description": "[Brief description of what the reader will accomplish]",
  "totalTime": "[ISO 8601 duration estimate, e.g., PT30M]",
  "step": [
    {
      "@type": "HowToStep",
      "position": 1,
      "name": "[Step 1 title]",
      "text": "[Step 1 description, 100-300 chars]"
    },
    {
      "@type": "HowToStep",
      "position": 2,
      "name": "[Step 2 title]",
      "text": "[Step 2 description]"
    }
  ]
}
```

**Implementation notes:**
- Don't generate HowTo schema for content that's just numbered for organization. Only when the steps are genuinely sequential and actionable.
- Each step's `name` should match the H3 in the blog body.

---

## Optional: BreadcrumbList Schema (Navigation Context)

Helps Google understand site hierarchy. Optional but cheap to include.

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://graehamwatts.com"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Blog",
      "item": "https://graehamwatts.com/blog"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "[BLOG POST TITLE]",
      "item": "https://graehamwatts.com/blog/[SLUG]"
    }
  ]
}
```

---

## Output Pattern (How Phase 5 Inserts Schemas Into the Blog)

At the END of the blog post HTML body, output one `<script>` block per schema type that applies. Multiple `<script>` blocks is fine — Google parses each independently.

```html
<!-- Article schema (always present) -->
<script type="application/ld+json">
{ /* Article schema JSON */ }
</script>

<!-- FAQPage schema (only when FAQ section exists) -->
<script type="application/ld+json">
{ /* FAQPage schema JSON */ }
</script>

<!-- VideoObject schema (only when YouTube embed exists) -->
<script type="application/ld+json">
{ /* VideoObject schema JSON */ }
</script>
```

If the blog is being rendered as Markdown for a CMS that doesn't support `<script>` tags directly, output the schema blocks at the bottom in a code fence labeled `json` and note in the output: "Schema blocks below — paste into your blog platform's custom HTML / SEO panel."

---

## Validation

Before publishing any blog with generated schema:

1. Copy the JSON-LD blocks
2. Paste into Google's Rich Results Test: https://search.google.com/test/rich-results
3. Confirm all schemas validate without errors
4. Fix any errors before publishing

Phase 5's compliance check should include "schema markup validates" as a checklist item.

---

## DRE / Identity Hard Rule (Repeat for Emphasis)

Schema includes Graeham's identity (name, DRE, brokerage). The DRE is **01466876** — read from `../../../../shared-references/identity.json` at generation time. NEVER type the DRE from prior context. There is a blocklisted value documented in identity.json's `dre_blocklist` array — that value has leaked into outputs 11 times historically. Read identity.json's blocklist at generation time and refuse to emit any value matching it. Do not type any DRE-shaped string into schema markup that wasn't read directly from identity.json's `identity.dre` field at runtime.
