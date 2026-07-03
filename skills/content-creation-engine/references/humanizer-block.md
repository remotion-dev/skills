# Canonical Humanizer Block

Referenced from SKILL.md Rule 8 ("Humanizer Block in Every PROMPT_LIBRARY Entry"). Copy this block verbatim into every prose-generating PROMPT_LIBRARY entry, placed AFTER Voice & Style and BEFORE the format-specific deliverable spec.

```
HUMANIZER RULES (apply throughout the output — do NOT mention these rules in the response itself, just follow them):

Avoid these AI-tell patterns:
- Em dashes — use commas, periods, or parentheses instead.
- Significance inflation: "stands as a testament," "marks a pivotal moment," "evolving landscape," "key turning point," "deeply rooted," "indelible mark."
- Promotional language: "boasts a," "nestled in," "vibrant," "rich" (figurative), "stunning," "must-see," "groundbreaking," "renowned," "breathtaking."
- Vague attributions: "experts say," "industry observers note," "research suggests" without naming the actual source.
- "-ing" tail clauses that add fake depth: "highlighting...," "underscoring...," "ensuring...," "contributing to...," "reflecting...," "showcasing..."
- Forced rule-of-three lists: "innovation, inspiration, and industry insights" / "streamlining, enhancing, fostering."
- Negative parallelism: "It's not just X, it's Y" / "Not only X, but Y."
- Tailing negation fragments: "no guessing," "no wasted motion" tacked onto sentences.
- Copula avoidance: "serves as," "stands as," "functions as," "represents a." Use "is" / "are" / "has."
- Sycophantic openers: "Great question," "I hope this helps," "Certainly," "Of course," "You're absolutely right."
- Knowledge-cutoff disclaimers: "As of my last update," "While specific details are limited."
- Excessive hedging: "could potentially possibly," "might have some effect on."
- Generic positive conclusions: "the future looks bright," "exciting times lie ahead," "represents a major step."
- Inline-header vertical lists where every bullet starts with "**Bold Header:**" followed by a colon.
- Curly quotes (use straight quotes only).
- Mechanical boldface — reserve bold for true emphasis, not decoration.
- False ranges: "from X to Y" when X and Y aren't on a meaningful scale.
- Persuasive authority tropes: "the real question is," "at its core," "what really matters," "fundamentally."
- Signposting announcements: "Let's dive in," "Here's what you need to know," "Now let's look at."
- Hyphenated word-pair clusters: "high-quality, data-driven, client-facing, decision-making" all in one sentence.

Instead:
- Vary sentence rhythm. Mix short punchy sentences with longer flowing ones.
- Use first person when it fits: "I keep coming back to," "Here's what gets me."
- Use specific numbers, dates, and concrete details over abstract claims. "$680K-$850K in Woodland Park" beats "competitive pricing in the area."
- Sound like one human talking to another about something that matters.
- Acknowledge complexity and mixed feelings when honest: "This is interesting but also kind of unsettling" beats "This is interesting."
- If the topic has a real edge or controversy, lean into it. Don't sand it down.

Read the final draft aloud in your head. If any sentence sounds like a press release, a Wikipedia article, or a LinkedIn thought leader, rewrite it.
```

## Block Placement Order in the Prompt Preamble

```
1. Agent Identity (Graeham Watts, REALTOR, Intero, DRE 01466876)
2. Fair Housing Guardrails
3. DATE/YEAR QC
4. Timing Self-Check (scripts only)
5. Voice & Style
6. HUMANIZER BLOCK  ← inserted here
7. Topic + Key Facts
8. AEO stats
9. GHL CTA / Lead Capture
10. Format-specific deliverable spec
```

## Maintenance

This is the single source of truth for the block text. When the `humanizer` skill at `skills/humanizer/SKILL.md` is updated with new patterns (new AI-tells observed in the wild), update this block in the same commit so PROMPT_LIBRARY entries stay in sync. The block is intentionally compact — 30-35 lines — to keep prompt size reasonable while covering the patterns that cause the most damage in spoken / read content.

**Failure mode this prevents:** Rule 7 (post-gen humanizer skill pass) only works when this skill generates content directly. When Adrian/Peter copy a prompt and paste into an external AI tool, Rule 7 doesn't fire — and the resulting script or blog reads like ChatGPT wrote it. Rule 8 closes that gap by moving the humanizer rules upstream into the prompt itself, so the external AI never produces the bad output in the first place.

## Canonical prompt-data structure (May 2026 update)

The CURRENT canonical weekly calendar uses a `const COPY_DATA = { "t1": { "ssml": "...", "prod_video": "...", "blog_brief": "...", "prod_blog": "..." }, "t2": {...}, ... }` JS object with 5 topics × 4 prompt types = 20 entries. Of those, 15 are prose-generating (3 per topic: prod_video, blog_brief, prod_blog) and MUST contain the Humanizer Block. 5 are SSML markup (one per topic) and MUST NOT contain the block (it would break the XML).

Older variants of the calendar (the `-all.html`, `-blogs.html`, `-videos.html`, `-research.html` quad-file pattern with `const PROMPTS = {...}`) are deprecated as of 2026-05-15 due to two architectural defects documented in `references/weekly-dashboard-rules.md` (Rules 9 and 11). New calendars use the single-file COPY_DATA pattern in `2026-05-11-production-calendar.html`.
