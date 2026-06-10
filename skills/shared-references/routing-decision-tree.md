# Content Routing Decision Tree — which skill handles "I need content"?

One page that ends the wrong-skill problem. Read this FIRST when a request is content-shaped and the entry point isn't obvious. (Job numbers refer to the four-job model in `data-contracts.md`.)

## The tree

```
"I need content / what should I post?"
│
├─ Asking WHAT to cover this week (no topic picked yet)?
│   └─ content-calendar  ........................ Job 2 (Opportunity Score, weekly plan)
│       └─ feeds selected topics into ↓
│
├─ Topic already picked, need the FACTS + SCRIPT + PACKAGE?
│   └─ content-creation-engine  ................. Jobs 3+4 (Intent Score, Phase R research, Phase G scripts)
│       ├─ video script → heygen-elevenlabs-renderer (avatar MP4, full auto)
│       │                 or heygen-video (one-off avatar video)
│       ├─ b-roll inserts → higgsfield-video (cinematic-hooks writes the prompts)
│       ├─ email/blog sections → newsletter-generator (assembles The EPA Report)
│       └─ ad deployment → meta-ads (deploys copy; engine writes it)
│
├─ Raw audience signal only ("what is Reddit/Instagram saying")?
│   ├─ Reddit → content-creation-engine Phase 2 (run_reddit_ideation.py) ... Job 1
│   └─ Instagram competitors → instagram-competitor-scraper
│
├─ A FULL newsletter (multi-section weekly email)?
│   └─ newsletter-generator (it pulls from the engine, not the reverse)
│
├─ Copy for ONE asset (headline, CTA, ad, subject line) with no research needed?
│   └─ copywriter (then humanizer pass)
│
├─ Listing-specific content?
│   ├─ MLS description → listing-remarks-writer
│   ├─ Photo captions → listing-photo-captioner
│   ├─ Videographer shoot plan → listing-call-sheet
│   └─ Postcard → farming-postcard
│
└─ Performance question ("how did content DO")?
    └─ content-calendar (analytics layer — absorbed social-media-analyzer)
```

## Hard rules

1. **Weekly ranking lives in content-calendar, never the engine.** "What should I post this week" always starts there.
2. **The engine never assembles newsletters** — it produces sections; newsletter-generator assembles.
3. **Every text output passes through humanizer before delivery.** No exceptions for client-facing copy.
4. **Brand values come from `identity.json` at generation time** — never typed from memory.

## Mandatory gates before a weekly calendar ships (now automated)

Run from `skills/content-creation-engine/`:

```bash
python scripts/weekly_overlap_check.py            # exit 1 = overlaps, review before push
python scripts/verify_output_brand.py <output>    # exit 2 = blocked value, DO NOT SHIP
python scripts/update_topic_history.py            # AFTER the calendar ships — feeds next week's freshness penalty
```
