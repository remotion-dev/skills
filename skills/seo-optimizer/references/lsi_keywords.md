# Deriving LSI / Semantic-Adjacent Keywords

LSI ("latent semantic indexing") is a slightly outdated term — Google doesn't literally run LSI anymore — but the intent is still useful: find the semantic neighborhood of a primary keyword and make sure the content covers it.

## The goal

For a primary keyword like "sourdough starter", you want the content to naturally include terms like:
- flour, water, fermentation, yeast, bacteria
- feeding schedule, discard, hooch
- active, peak, doubled in size
- rye, whole wheat, all-purpose
- glass jar, kitchen scale, temperature

If a reader who knows the topic would expect to see those words and they're missing, Google's language models pick up on that gap and the page reads as "thin."

## Method 1 — Derive from content (no external tools)

This is the default approach when the user hasn't given you external keyword data.

1. **Identify the primary keyword** from the H1, repeated phrases, and URL slug.
2. **Extract noun phrases** from the body that appear 2+ times and are topically related.
3. **Prune** brand names, generic filler ("article", "content", "read"), and off-topic mentions.
4. **Add the obvious gaps.** This is the most valuable step. For the primary keyword, what semantically adjacent terms does the content NOT mention that a domain expert would expect?

## Method 2 — From SERP analysis (when the user has data)

If the user shares what competitors on page 1 of Google look like:
1. Extract repeated H2/H3 headings across the top 5 results
2. Extract repeated noun phrases from intros and first sections
3. The terms that appear across 3+ competitors are the topical baseline

## Proposing the keyword strategy

In the SEO report, propose:
- **1 primary keyword** — the main topic, what you'd pick a domain for
- **3–5 supporting keywords** — semantic neighbors the content should cover

Always explain WHY these keywords. The user may have different intent. Example:

> **Primary keyword:** "sourdough starter from scratch"
> **Supporting:** "feeding schedule", "discard recipes", "rye flour", "jar size", "active vs peak"
> **Why these:** The content targets beginners who have never made a starter. The supporting terms cover the questions a beginner will have after reading — feeding cadence, what to do with discard, flour choice, and how to tell when it's ready. Covering these in the body strengthens topical depth and captures long-tail queries.

## Intent calibration

Different intents call for different keyword neighbors. For the same primary topic:
- **Informational intent** ("how to ___") — process words: steps, tips, guide, beginner, mistakes
- **Commercial intent** ("best ___") — comparison words: vs, review, pros, cons, price, alternative
- **Transactional intent** ("buy ___") — purchase words: shipping, warranty, return, bundle, discount
- **Navigational intent** ("brand name ___") — brand words: official, login, support, contact

Match the supporting keywords to the intent the content is actually serving. A "best sourdough starter kits" page with "step-by-step instructions" as a supporting keyword is mis-targeted — the searcher wants a product comparison, not a tutorial.

## What to avoid

- Don't propose keywords that would force unnatural sentences. If "sourdough starter feeding schedule" is awkward to weave in, target "feeding schedule" or "feeding your starter" instead.
- Don't propose synonyms of the primary keyword as supporting keywords — "sourdough starter" and "sourdough culture" are the same intent. You want *related topics*, not paraphrases.
- Don't overload. 3–5 supporting keywords is plenty. Ten is dilution.
