# Option Cache — Scheduled Preview Options

This file stores the postcard hook options that the skill emails to Graeham 7 days before each drop date. When Graeham comes back to Cowork and says "pull up what you emailed me", read this file, find the most recent entry with `Status: pending pick`, and present those options for selection.

After he picks, mark his pick `PICKED` and the others `not picked`, then move the whole entry under the **Resolved** section at the bottom.

---

## Pending picks

*(No pending picks yet. The 8th-of-month and 24th-of-month scheduled tasks will populate this section automatically.)*

---

## Format reference (for the cron job to follow)

When Workflow B emails options, append an entry like this:

```markdown
## [TARGET_MAIL_DATE] (emailed [SENT_DATE])
Status: pending pick

### Option 1 — [Archetype name]
Front headline: [Plain text with <span class="gold">markup</span>]
Back headline: [Plain text]
Back body: [3-sentence italic body]
CTA line: [Gold CTA tagline]
CTA type: [home valuation / testimonials / free report / etc.]
QR target URL: [URL from cta-router.md]
Why this works: [One-line rationale]
Audience fit: [Farm / Past clients / Both]

### Option 2 — [Archetype name]
...

### Option 3 — [Archetype name]
...
```

---

## Resolved

*(Picked options move here after the user selects one. Keeps a permanent record of what was offered + what was chosen for pattern analysis over time.)*
