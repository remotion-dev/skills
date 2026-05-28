# Option Cache — Scheduled Preview Options

This file stores the postcard hook options that the skill emails to Graeham 7 days before each drop date. When Graeham comes back to Cowork and says "pull up what you emailed me", read this file, find the most recent entry with `Status: pending pick`, and present those options for selection.

After he picks, mark his pick `PICKED` and the others `not picked`, then move the whole entry under the **Resolved** section at the bottom.

---

## Pending picks

## 2026-06-15 (emailed 2026-05-27 — TEST RUN)
Status: pending pick

### Option 1 — Buyer-tagged
Front headline: I have 3 buyers looking for your <span class="gold">BLOCK</span>.
Back headline: Active buyers · not just window-shoppers
Back body: While other agents wait for the phone to ring, my geofencing is tracking three pre-approved buyers actively touring properties on streets around you. Your home might be the one they're waiting for.
CTA line: Call me · let's see if you match
CTA type: Call/text Graeham
QR target URL: tel:+16503084727
Why this works: Concrete number (3) + proximity ("your block") = strongest scarcity hook for cold farm audience
Audience fit: Farm
⚠ Verification needed: Confirm "3 buyers" is real before print; soften to "buyers" if not

### Option 2 — Anti-Zillow buyer pool
Front headline: Zillow shows everyone. <span class="gold">I show the ones who actually buy.</span>
Back headline: Off-market buyers don't browse — they get <span class="gold-box">TAGGED</span>
Back body: Most listings reach the same tired buyer pool. My system identifies high-intent, pre-qualified buyers who don't waste agent time scrolling Zillow. They're looking for homes like yours right now.
CTA line: Free off-market match check
CTA type: Off-market buyers
QR target URL: [NOT SET — needs URL]
Why this works: Differentiates from every other agent doing standard listings + creates exclusivity
Audience fit: Both

### Option 3 — Equity refresh
Front headline: Your home grew <span class="gold">$___</span> this year. Want the real number?
Back headline: Stop checking <span class="gold-box">ZILLOW</span> · get the real number
Back body: Zillow's algorithm hasn't seen your kitchen remodel, your roof work, or the comp that sold three doors down last month. The number it's showing you is wrong — and probably low. Get the real one.
CTA line: Free precision equity report
CTA type: Home valuation
QR target URL: [NOT SET — needs URL]
Why this works: Pride + curiosity + tangible payoff. Equity archetype hasn't run since 03/01/25 — feels fresh
Audience fit: Both
⚠ Verification needed: Fill $___ blank with real EPA appreciation number before print

### Option 4 — WILDCARD · Live market activity
Front headline: <span class="gold">11 offers.</span> 6 days. Same zip code as you.
Back headline: This is what the EPA market looks like <span class="gold-box">RIGHT NOW</span>
Back body: If you've been waiting for the "right time" to sell, this is your signal. A home in your zip code just closed at 11 offers in under a week. Your home would compete in the same environment.
CTA line: Free market timing check
CTA type: Free report (market)
QR target URL: [NOT SET — needs URL]
Why this works: Hyper-local social proof + urgency. New archetype — if it lands, add as #7 to library.
Audience fit: Both
⚠ Verification needed: Requires real recent EPA multi-offer comp — do not ship without it

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

## 2026-06-15 (emailed 2026-05-27 — FULL PIPELINE TEST, fresh remixes)
Status: pending pick (test run — supersedes prior June 15 entry)

### Option 1 — Buyer-tagged (FRESH REMIX)
Front headline: Your home is on <span class="gold">someone's list</span>. They just haven't <span class="gold-underline">seen it</span> yet.
Back headline: I have buyers looking for your street — and they're pre-approved
Back body: When buyers tour properties on your block, my system tags them. Some have been waiting months for a home like yours to come available. Want me to see if you match?
CTA line: 5-minute match check · free
CTA type: Call/text Graeham
QR target URL: tel:+16503084727
Why this works: No number to fabricate. "Someone's list" creates inevitability.
Audience fit: Farm

### Option 2 — Anti-Zillow buyer pool (FRESH REMIX)
Front headline: The buyers <span class="gold">Zillow can't show you</span>.
Back headline: Off-market buyers don't browse — they get <span class="gold-box">TAGGED</span>
Back body: Public portals show every casual scroller. My pipeline is the buyers who've already proven they'll close — pre-approved, agent-vetted, ready.
CTA line: Free off-market match check
CTA type: Off-market buyers
QR target URL: [NOT SET]
Why this works: 6-word headline. Reframes Zillow's audience as a feature for the seller, not against.
Audience fit: Both

### Option 3 — Equity refresh (FRESH REMIX)
Front headline: You're sitting on <span class="gold">more than you think</span>.
Back headline: The equity check most owners never get
Back body: Zillow gives you a zip-code average. Your bank gives you last year's appraisal. Neither sees your remodel, your block's recent sales, or what your home would actually trade for today.
CTA line: Free precision equity report
CTA type: Home valuation
QR target URL: [NOT SET]
Why this works: No dollar amount to fabricate. Positive frame pulls pride + curiosity without market anxiety.
Audience fit: Both

### Option 4 — WILDCARD · Value Gap (loss aversion angle)
Front headline: Most EPA owners are <span class="gold">undervaluing</span> their home.
Back headline: Find out where <span class="gold-box">YOUR</span> home really sits
Back body: The gap between what Zillow shows and what a home actually trades for is often double-digit percent. If you're sitting on six figures of unrecognized equity, you should at least know it.
CTA line: See where you really stand
CTA type: Home valuation
QR target URL: [NOT SET]
Why this works: Loss aversion is stronger than gain. New sub-angle — if it lands, add as 7th archetype to library.
Audience fit: Both
⚠ Verification needed: Need a real local EPA gap stat before print
