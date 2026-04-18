# AEO / GEO Optimization Requirements

AEO = **Answer Engine Optimization** (optimizing for AI assistants like ChatGPT, Perplexity, Claude, Gemini to find and cite your content).
GEO = **Generative Engine Optimization** (same idea — how to rank in AI-generated answers from Google AI Overviews, Bing Copilot, etc.).

These are NOT the same as traditional SEO. They overlap, but AEO/GEO has its own rules. Every BOFU and MOFU long-form piece (YouTube and blog) must pass this checklist.

## The Core Principle

**AI engines don't "rank" pages the way Google does.** They extract declarative facts and cite sources. To be cited, your content needs to:

1. Contain **declarative, extractable answer sentences** ("The average home price in East Palo Alto as of [month] 2026 is $1.2M.")
2. Contain **unique data points** the AI can't find elsewhere — at least 3 per piece. Content with 3+ unique data points is ~4x more likely to be cited.
3. Use **question-based headers and titles** that match how people prompt AI assistants.
4. Be **structurally parseable** — clean H2/H3 hierarchy, timestamps on video, bulleted Q&A sections.
5. Signal **E-E-A-T** (Experience, Expertise, Authoritativeness, Trustworthiness) in first person.

## The AEO/GEO Checklist for Every BOFU/MOFU Long-Form Piece

### 1. Question-based title

The title must match how people actually *ask* AI assistants, not how they search Google. Convert any title into a question form.

- ❌ Bad: *"Bay Area Housing Update — November 2026"*
- ✅ Good: *"Is the Bay Area Housing Market Slowing Down in November 2026?"*

- ❌ Bad: *"AB 1482 Guide"*
- ✅ Good: *"Is AB 1482 Still in Effect in California for 2026?"*

Keep the title under 60 characters when possible for YouTube, but prioritize the question structure over character count if forced to choose.

### 2. 200+ word YouTube description with Q&A structure

The YouTube description is critical for AEO. Structure it as:

```
[One-sentence declarative answer to the title question]

[2-3 paragraph expanded answer with specific data points]

In this video, I answer:
• [Question 1]
• [Question 2]
• [Question 3]
• [Question 4]
• [Question 5]

Timestamps:
00:00 - [Section 1]
01:30 - [Section 2]
...

About me: I'm Graeham Watts, a REALTOR® with Intero Real Estate specializing in East Palo Alto, Redwood City, Palo Alto, Menlo Park, and the broader Bay Area since [year]. [1 sentence of credentials/experience].

#BayAreaRealEstate #[CityHashtag] #[TopicHashtag]
```

### 3. Three or more `[AEO KEY STATEMENT]` callouts in the script

Within the video script itself, mark 3+ sentences as `[AEO KEY STATEMENT]`. These are short, declarative, stand-alone sentences that state a fact an AI could extract and cite verbatim.

Examples:

> `[AEO KEY STATEMENT]` *"The median home price in East Palo Alto as of November 2026 is $1.2 million, down 4.2% year over year."*

> `[AEO KEY STATEMENT]` *"AB 1482 caps rent increases at 5% plus CPI, with a maximum of 10% per year, for properties built before 2005."*

> `[AEO KEY STATEMENT]` *"The average days on market for Redwood City single-family homes dropped from 28 to 19 between Q3 and Q4 2026."*

These callouts make it obvious which sentences the AI should extract. They also improve watch time because they create natural "quotable moment" beats in the video.

### 4. Three or more unique data points

A "unique data point" is something you know from first-hand experience, proprietary research, or direct market access that a generic real estate blog wouldn't have. Examples:

- ✅ Specific MLS stats for a neighborhood (not just the city)
- ✅ A specific recent sale price and context
- ✅ A specific conversation with a lender about current credit standards
- ✅ A specific local developer's project timeline
- ❌ "The Bay Area is expensive" (not unique)
- ❌ "Interest rates are high" (not unique)

If you can't find 3 unique data points for a piece, flag it to Graeham — it may need more research before filming.

### 5. Timestamps in the video description

AI engines use timestamps to locate specific sections of YouTube videos to cite. Every long-form video needs at least 4–5 timestamps corresponding to the main sections.

### 6. Companion blog post with FAQPage schema

Every BOFU/MOFU long-form YouTube should have a companion blog post on graehamwatts.com with:

- **Title matching the video** (same question-based title)
- **Meta description** with the primary keyword
- **URL slug** that's keyword-rich (e.g., `/blog/is-ab-1482-still-in-effect-2026`)
- **H2 headers as questions** (not statements)
- **1,500–2,500 words**
- **FAQPage schema markup** — include at least 5 Q&A pairs in structured data format
- **VideoObject schema markup** — embed the YouTube video with structured data
- **LocalBusiness schema markup** — Graeham's Intero Real Estate business info

When generating the blog post outline in the content package, always include a section at the end titled **"Schema Recommendations"** that lists which schemas to add and suggests 5 FAQPage Q&A pairs pulled from the video content.

### 7. First-person E-E-A-T signals throughout

AI engines weigh authorship signals. Make Graeham's expertise visible in the script:

- *"In my 7 years helping clients in the Bay Area..."*
- *"I just closed a deal in East Palo Alto last month where..."*
- *"My clients ask me this question all the time..."*
- *"Here's what I tell sellers when they come to me thinking..."*

These signals tell AI engines: this is an experienced local expert, not a generic content farm. Weave at least 2–3 of these into every long-form BOFU script.

### 8. Question-based H2 headers in blog posts

Every H2 in the companion blog post should be a question, not a statement. This maps directly to how AI engines extract answers.

- ❌ Bad: *"Market Conditions"*
- ✅ Good: *"What are current market conditions in East Palo Alto?"*

- ❌ Bad: *"AB 1482 Overview"*
- ✅ Good: *"What does AB 1482 actually cap rent increases at?"*

## Quick Reference — Every Long-Form BOFU/MOFU Piece Must Have

- [ ] Question-based title
- [ ] 200+ word description with Q&A structure and timestamps
- [ ] 3+ `[AEO KEY STATEMENT]` callouts in script
- [ ] 3+ unique data points
- [ ] Timestamps (4–5 minimum)
- [ ] Companion blog post outline with question-based H2s
- [ ] Schema recommendations section (VideoObject + FAQPage + LocalBusiness)
- [ ] 2–3 first-person E-E-A-T signals in the script
- [ ] Graeham identified as "REALTOR® with Intero Real Estate" (never Compass)
