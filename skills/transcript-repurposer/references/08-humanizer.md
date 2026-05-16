# Phase 8 — Humanizer Pass (Auto, Required)

This is the non-negotiable last step. Every content package from this skill gets humanized before delivery. No exceptions.

## Why this is required, not optional

The whole point of repurposing a transcript is to produce content that sounds like Graeham. AI-pattern writing — significance inflation, em dash overuse, sycophantic openings, rule-of-three, generic conclusions — undoes everything Phases 1-7 just did. A script that scored well on hook strength and research depth but reads like a chatbot wrote it will still tank engagement.

The humanizer skill (`humanizer/SKILL.md`) systematically removes those patterns and replaces them with natural voice. It catches things that are easy to miss when you're focused on script structure.

## How to invoke

After Phase 7 completes, invoke the humanizer skill on the full content package. The humanizer skill expects:

1. **The text to humanize.** Pass the full content package — every hook variant, every script body across platforms, captions, blog, editing notes prose.
2. **A voice-matching sample (optional but strongly recommended).** Graeham's voice and style reference from the Content Engine is the right sample. Path:
   ```
   video-script-creation-engine/references/phases/script-writer/references/voice-and-style.md
   ```
   If that file is accessible in the current session, pass it as the sample so humanizer's rewrites match Graeham's actual cadence, not a generic "natural" voice. If not accessible, humanizer falls back to default natural-voice rules.

## What to humanize (and what to skip)

### Humanize:

- All three hook variants (yes, BEFORE final selection — so we're scoring humanized versions, not raw AI output)
- YouTube Long script body
- YouTube Short script body
- IG Reel script body
- TikTok script body
- Carousel slide text
- Blog post body
- GMB post body
- Facebook caption body
- IG/TT/YT captions
- Editing notes prose sections (e.g., the "Pacing Notes" paragraph — NOT the bracketed shot tags)

### Skip (intentionally machine-readable):

- ElevenLabs SSML — it's XML markup, not human-facing copy. Humanizing the XML breaks the format.
- Inline shot tags `[TALKING HEAD]`, `[B-ROLL: ...]`, `[TEXT OVERLAY: ...]` — these are structural directives for the editor.
- Higgsfield image prompts — they're technical generation prompts with anchor stacks. Humanizing them would degrade output quality.
- Higgsfield motion prompts — same.
- GHL keyword line itself — the format is fixed for the automation to fire correctly.
- Hashtag blocks.
- HeyGen avatar look IDs and aspect ratio specs.

## The Humanizer Pattern Checklist

For reference, the humanizer skill catches these patterns. When QC-ing the output, scan for them yourself too:

**Content patterns:**
- Significance inflation ("stands as", "is a testament", "pivotal moment")
- Notability name-dropping
- Superficial -ing analyses ("highlighting", "ensuring", "reflecting", "showcasing")
- Promotional language ("boasts", "vibrant", "nestled", "breathtaking")
- Vague attributions ("experts argue", "industry reports")
- Formulaic "challenges and future" sections

**Language patterns:**
- AI vocabulary ("delve", "leverage", "testament", "landscape", "enduring", "fostering", "intricate", "pivotal", "showcase", "tapestry", "underscore", "vibrant")
- Copula avoidance ("serves as", "stands as", "features", "boasts")
- Negative parallelisms ("not just X, but Y")
- Rule of three overuse
- Synonym cycling
- False ranges
- Passive voice and subjectless fragments

**Style patterns:**
- Em dash overuse (use commas, periods, parentheses)
- Boldface overuse
- Inline-header lists
- Title Case Headings (use sentence case)
- Emojis in headings/bullets
- Curly quotation marks

**Communication patterns:**
- Chatbot artifacts ("I hope this helps", "Of course!", "Certainly!")
- Knowledge-cutoff disclaimers
- Sycophantic tone

**Filler and hedging:**
- Filler phrases ("in order to", "due to the fact that", "at this point in time")
- Excessive hedging ("could potentially possibly be argued")
- Generic conclusions ("the future looks bright")
- Hyphenated word pair overuse ("cross-functional", "data-driven")
- Persuasive authority tropes ("at its core", "what really matters")
- Signposting ("Let's dive in", "Here's what you need to know")

## The Final Anti-AI Audit

The humanizer skill includes a final audit step:
1. After the first humanization pass, ask: "What makes the below so obviously AI generated?"
2. Answer briefly with remaining tells.
3. Then prompt: "Now make it not obviously AI generated."
4. Revise.

Run this audit on the script body of the YouTube Long, YouTube Short, IG Reel, and TikTok derivatives at minimum. The other derivatives benefit from it but are lower-stakes — captions and blog can take the first-pass humanized version unless the user requests a deeper audit.

## Voice Soul, Not Just Pattern Removal

Removing AI patterns is half the job. Inject Graeham's actual voice:

- **Opinions, not just facts.** "Rates are at 6.8%" → "Rates are at 6.8%, which is roughly where I expected them to land six months ago."
- **Vary rhythm.** Mix short and long sentences. Don't make every sentence the same length.
- **Acknowledge complexity.** "This works for some buyers, not others. Here's how to tell which one you are."
- **Specific over abstract.** Names, places, dates, dollar amounts.
- **Use "I" when it fits.** Working-agent voice means first-person reflection is on-brand.
- **Let some mess in.** Small tangents, parenthetical asides, the kind of clarification a real person adds when speaking.
- **Specific about feelings.** Not "this is concerning" but "this is the thing that keeps me up the night before a closing."

## Output

Save the final humanized content package to:

```
outputs/transcript-repurpose-{slug}-{YYYYMMDD-HHMM}.md
```

Where `{slug}` is a short kebab-case identifier from the topic and `{YYYYMMDD-HHMM}` is the current production timestamp.

Return a `computer://` link to the user.

## Optional — Show Before/After

If the user explicitly asks "show me what changed" or "what did you fix", append a small Before/After section at the end of the content package showing 3-5 representative pattern fixes:

```
## Humanizer Pass — Sample Changes

Before: "This stands as a testament to the evolving Bay Area market."
After:  "This is what Bay Area buyers are actually doing in April 2026."

Before: "Leveraging current data, we can delve into the implications..."
After:  "Here's what the April rate data means for your buying timeline."

Before: "It's not just about price — it's about positioning."
After:  "Price matters less than positioning."
```

Only include this if asked — by default, deliver the clean final output.
