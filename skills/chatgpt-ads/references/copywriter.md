# ChatGPT Ads Copywriter (reference)

Source: AiM chatgpt-ads-copywriter skill (May 2026), merged into the chatgpt-ads skill.

# ChatGPT Ads Copywriter

Write the actual ad content — context hints, keyword arrays, titles, descriptions, image pairings. This skill is the craft authority for everything that goes into a ChatGPT Ads campaign.

---

## Before You Write Anything

1. **Read `../marketing-psychology/SKILL.md`** for persuasion fundamentals. Every word you write should pass through that lens — awareness levels, sophistication, the Gap, framing, and so on. Don't skip this.
2. **Read `references/moments.md`** to pull the right moment(s) for the ad group(s) you're writing.
3. **Have market-config.md loaded** in your working memory. The user's market, niches, voice, and price range shape every choice you make.

---

## What You Produce Per Ad Group

For each ad group, you generate six pieces:

1. **Ad group name** — short, lowercase, underscores only, no special characters. Format: `{moment_short}_{city_short}` (e.g., `first_time_buyers_nashville`, `luxury_sellers_brentwood`).
2. **Context hint** — one paragraph, 2-4 sentences, plain language, customized to the user's market. This is what the user pastes into Ads Manager after upload.
3. **Keyword array** — 10-15 phrases as a JSON array, derived from the context hint, for the spreadsheet's keywords field.
4. **Three ads** — each with title (≤24 chars), copy (≤48 chars), link, image assignment.
5. **Max bid** — picked from the user's max-bid range in market-config.
6. **Image rationale** — one sentence per ad explaining why a specific image fits.

---

## The Context Hint Formula

Every context hint follows: **Persona + Location + Intent + Moment.**

Pull the matching moment from `references/moments.md` as your starting point. Then customize it:

- **Persona** — keep generic (homeowners, buyers, investors). Don't reference protected classes.
- **Location** — sub in the user's specific city, metro, or neighborhood from market-config. If the moment is neighborhood-specific, use the user's actual neighborhood names. If it's market-wide, use the metro.
- **Intent** — keep the moment's intent language. It's already tuned.
- **Moment** — add timing or trigger detail if the user's market makes it specific (e.g., "after the recent inventory spike," "with rates where they are now").

Length: 2-4 sentences. No more. The matcher reads tone and theme — it doesn't reward verbosity.

Avoid the word "actually" anywhere in any output.

---

## Deriving the Keyword Array

The keywords field on the bulk-upload template doesn't map to the platform's actual targeting (the platform uses context hints, set in the UI). But the keyword field still has to be populated for the upload to clear, and a strong keyword array gives the matcher real signal on import before the user pastes the context hint manually.

For each context hint, produce 10-15 keyword phrases that:

- Are short (2-5 words each)
- Read like a user might phrase a query to ChatGPT ("how do I buy my first home in nashville", "best realtor brentwood tn")
- Mix local-specific and category-general (some include the city, some don't)
- Vary in phrasing (questions, statements, role-based — "first time buyer", "starter home help", "buying a house guide")

Format as a JSON array: `["phrase one", "phrase two", "phrase three"]`. Wrap each in double quotes. Comma-separated. Square brackets at start and end.

---

## Writing Titles (24 Character Hard Limit)

This is the strictest part of the entire job. Excel will accept any string, but Ads Manager will reject ads with titles over 24 characters at import.

**Count the characters before you ship every title. No exceptions.**

Use Python: `len(title)`. Don't estimate. Don't eyeball.

> Note: The manual Ads Manager UI allows up to 50 characters in titles and 100 in copy, but headlines past the bulk template's 24/48 limits get truncated on smaller surfaces. We stay at 24/48 by design — the truncation is invisible damage, and tighter copy forces sharper writing anyway. Don't relax these limits.

### Compression Patterns

Most natural-sounding headlines blow past 24 characters. Practice these compressions:

| Original (too long) | Compressed (under 24) |
|---|---|
| "How to Pick the Right [CITY] Agent" | "Pick the Right Agent" (20) |
| "[NUMBER] Years Selling Homes in [NEIGHBORHOOD]" | "20 Yrs in Brentwood" (19) |
| "The Best [CITY] Homes Aren't on Zillow" | "Beyond Zillow Listings" (22) |
| "How [CITY] Luxury Listings Actually Sell" | "How Luxury Really Sells" (23) |
| "Zestimate Off by [$X]? Here's Why." | "Zestimate Wrong?" (16) |
| "Selling for the First Time? Ask These First." | "First-Time Sellers?" (20) |
| "60+ Days Listed. Still No Offers." | "60 Days. No Offers." (19) |
| "Your Listing Expired. Now What?" | "Listing Expired?" (16) |
| "Tired of Tire-Kickers and Lowballs?" | "Tired of Lowballs?" (18) |
| "Pre-Approved? Let's Tour This Weekend." | "Pre-Approved? Tour" (18) |
| "Lost Three Offers This Year?" | "Lost 3 Offers?" (14) |
| "Moving to [CITY] in 90 Days?" | "Moving in 90 Days?" (18) |
| "The Builder's Agent Isn't Yours." | "The Builder's Agent" (19) |
| "Don't Buy Land Without This Checklist." | "Buying Land? Read This" (22) |

### Compression Tactics

1. **Drop unnecessary words.** "The," "this," "your," "a" — kill them if the sentence reads fine without.
2. **Replace numbers as digits.** "Three" → "3". "Twenty" → "20".
3. **Use abbreviations.** "Years" → "Yrs". "Neighborhood" → use the actual name if shorter.
4. **Cut filler phrases.** "Here's why" / "Now what" can often be dropped or shortened.
5. **Replace verbose verbs with sharp ones.** "Considering" → "Want to". "Looking for" → "Need".

### What NOT to Do

- Don't pad to fill 24 chars. Short and punchy beats long and full.
- Don't use special characters that won't import cleanly (em-dashes are OK, smart quotes can cause issues — prefer straight quotes).
- Don't end with a period unless it's load-bearing for tone.
- Don't sacrifice meaning for fit. If a headline won't compress without losing its punch, change the angle.

---

## Writing Copy / Descriptions (48 Character Hard Limit)

Same discipline as titles, double the room. Still tight.

**Count before you ship. No exceptions.**

### Patterns That Fit

| Pattern | Char count | Example |
|---|---|---|
| Promise + qualifier | 30-40 | "Real number from a local agent. No bots." (40) |
| Objection-disarm | 35-45 | "Not the algorithm. A human who knows your block." (48) — exactly at limit |
| Question + answer | 30-45 | "Lost 3 offers? Get the inside list." (35) |
| Specific stat | 25-40 | "Off-market list. 12 properties this month." (43) |
| Direct command | 25-40 | "Schedule a call before you list." (33) |

### Tactics for the 48-Char Cap

1. **One idea per description.** Don't try to fit a benefit + a feature + a CTA. Pick one.
2. **Punctuation counts.** Periods, commas, spaces — all character spend.
3. **Front-load the strongest word.** ChatGPT users skim. The first three words have to earn the rest.
4. **Avoid clauses.** "Schedule a call before you list and save thousands" (51) → "Schedule a call before you list." (33).

### The Three-Angle Rule

For each ad group, your three ads should hit three different angles. Don't reword the same idea three times. Vary:

- Ad 1: a question that names the user's exact problem
- Ad 2: a specific stat or proof point
- Ad 3: an objection-disarm or "what makes us different"

The matcher gets stronger signal from real variety. So does the user.

---

## Image-to-Ad Pairing

You'll have an image inventory from the agent's Phase 3. Each image is classified (headshot, neighborhood landmark, home exterior, etc.).

Pair images to ads using this priority:

1. **Headshot** → ads where trust is the lever (first-time buyer, "how to pick an agent," seller anxious about choosing someone)
2. **Neighborhood landmark** → ads anchored to geography (relocation, "moving to [CITY]," local expertise positioning)
3. **Sold-and-closed home exterior** → ads about marketing approach or track record (luxury seller, frustrated seller, "see how we sell")
4. **Lifestyle / market shot** → ads about market dynamics or general positioning (deciding when to list, buyer in competitive market)

**Never pair an active listing photo with any ad** — flag those and explain to the user why (false advertising risk if the home goes under contract).

If the user has fewer images than ad slots (9 total for 3 ad groups × 3 ads each), it's fine to reuse the same image across multiple ads. Most users will only have 3-6 images and that's expected.

Document each pairing with a one-sentence rationale so the user understands the logic.

---

## Fair Housing and Compliance Guardrails

Apply these to every word you write. No exceptions, no workarounds.

### Never reference, directly or by implication:

- Race, color, ethnicity
- Religion
- National origin
- Sex, gender, sexual orientation, gender identity
- Familial status (no "great for families," "kid-friendly," "perfect for couples")
- Disability
- Age (no "perfect for retirees" — use "55+ community" only if the community is legally designated as such and the user confirmed it)
- Marital status

### Target the housing situation, not the household.

- ✅ "First-time buyers in [CITY]" (housing situation)
- ❌ "Young couples in [CITY]" (familial status)
- ✅ "Buyers looking for a 55+ community" (housing situation tied to a legally designated community type)
- ❌ "Retirees looking to downsize" (age)
- ✅ "Sellers preparing for a quick move" (situation)
- ❌ "Families needing more space" (familial status)

### Don't make claims you can't substantiate.

- Don't reference school quality
- Don't reference neighborhood demographics
- Don't promise specific outcomes ("save $50,000," "sell in 7 days") unless the user has explicit data and is comfortable owning the claim
- Don't compare to specific named competitors

### Country-specific rules (apply based on user's compliance notes in market-config):

- **US** — Fair Housing Act protected classes apply nationally. State-level rules vary (some states require brokerage name in ads). RESPA applies to anything that could be construed as a settlement-service referral arrangement.
- **Canada** — CREA Code of Ethics + provincial real estate council rules. Anti-discrimination provisions in provincial human rights codes apply to all housing advertising.
- **Australia** — State-specific real estate licensing acts plus Australian Consumer Law (no misleading or deceptive conduct).
- **New Zealand** — REA rules of conduct, Fair Trading Act, Human Rights Act anti-discrimination provisions.

If you're unsure whether a phrase crosses a line, rewrite it more neutrally. The agent will sanity-check the output anyway, but your job is to ship clean copy first.

---

## Voice and Tone

market-config.md has a "Voice and tone notes" field. Apply it.

If the user said warm and direct: contractions, short sentences, no formal language. "Let's tour this weekend" not "Allow me to arrange a viewing."

If the user said expert and authoritative: full sentences, specific numbers, references to experience. "20 years of negotiating in Brentwood" beats "I'm pretty good at this."

If the user said conversational: questions that invite a response. Casual phrasing. "Wondering what your home's worth?" beats "Free home valuations available."

When in doubt, default to coaching-voice: confident, direct, warm. Never robotic, never aggressive, never overpromising. Match the AiM coaching voice if no specific voice is given — second-person, action-oriented, business-outcome framing.

---

## Picking the Max Bid

market-config has a max-bid range (e.g., "$3-$5"). For each ad group, pick a bid within that range based on:

- **Higher bid ($4-5)** for ad groups targeting competitive moments — luxury, relocation deadlines, high-intent buyer moments. These compete with other paid advertisers and need to win impressions.
- **Lower bid ($3-3.50)** for ad groups in less-competitive niches — historic homes, probate, distressed sellers. These have less competition; you can win impressions at the floor.
- **Mid-range ($3.50-4)** for general moments — first-time buyers, home valuation, FSBO conversion.

Default to mid-range if you're unsure. The user can adjust in Ads Manager after launch.

---

## Self-Check Before Handoff

Before you hand the output to the workbook-builder skill, verify:

- [ ] Every title is ≤24 characters (count each one with `len()`)
- [ ] Every copy is ≤48 characters (count each one with `len()`)
- [ ] Three ads per ad group, three ad groups, nine ads total
- [ ] Three different angles per ad group (no reworded duplicates)
- [ ] Every ad has a landing page URL
- [ ] Every ad has an image assignment (if images were provided)
- [ ] No protected-class language anywhere
- [ ] No fabricated claims or competitor mentions
- [ ] Context hints are 2-4 sentences each, customized to the user's market
- [ ] Keyword arrays have 10-15 phrases each, properly JSON-formatted
- [ ] Max bids fall within the user's range and reflect competitive level of the moment
- [ ] Voice matches the user's market-config notes

If any check fails, fix it before passing to the workbook-builder.
