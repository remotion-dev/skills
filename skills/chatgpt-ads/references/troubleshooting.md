# ChatGPT Ads — Troubleshooting & Optimization

> Load this AFTER a campaign is live (post-upload). The other references build the
> campaign; this one fixes it once it's running.
>
> Source: Jason Pantana, AiM lecture **"Troubleshooting ChatGPT Ad Campaigns"**
> (June 2026, Vimeo 1205113489) — the "round two" companion to the May build-side
> guide. Members-only; treat as private.

---

## 1. The diagnostic decision tree (start here)

Match the symptom, make the one move:

| Symptom | Most likely cause | The move |
|---|---|---|
| **Flatlining** — ~0 impressions | Campaign is dead or under-bid | Delete & rebuild the campaign, **or** raise the budget cap |
| **Impressions, no clicks** | Bid too low, or weak offer | Raise max CPC **and/or** fix the offer (headline + image) |
| **Clicks, no conversions** | Landing page isn't a "catcher's mitt" | Fix the page — see §6 |

If an ad group is starved after **24–48h**, bump its max bid by **$1** and re-check.

## 2. Budget is a ceiling, not a charge

- The #1 reason ads aren't serving: **bids too low / budget too timid.**
- **Almost nobody's budget gets utilized right now** (members report $200 cap → $4 spent; $600 cap → $86 spent). It behaves like Google Local Service Ads — lots of allocated budget, not enough volume to spend it yet.
- On the **Clicks** objective you only pay per click — impressions are free. The budget number is what you're *willing* to pay, **not** what you'll be charged.
- Honest caveat to give any team member: this is "willing to pay," not a guarantee. Use discretion; never bid past comfort.

## 3. Bid guidance — CHANGED from the build guide

- OpenAI **lowered the max-CPC floor to ~$4.** Pantana now says that's **too low** — bid **~$7–8** to actually win impressions.
- Observed CPCs are all over the map: $1–2 on the low end, $8–9 common, some $12–14. "As cheap as it'll ever be" — treat the first 30 days as a **learning purchase**, not performance optimization.
- This supersedes the old "$3–5 starting max bid" line in SKILL.md / the build guide.

## 4. The offer: headline + image is everything

- You are **intruding on an intimate ChatGPT conversation.** The ad must be compelling enough to beat the organic answer the user just got.
- **Headline must crush.** Front-load the most important words — ads truncate with "…"; a "copy may be truncated" warning means shorten / move the key message earlier.
- **Image = your headshot.** People want to see the agent's face, especially on mobile. (Counter-example: the realestateagents.com far-away building shot — nobody's face = weak.)

## 5. Win organic AND paid together ("fire + gasoline")

- If your name appears in **both** the organic answer and the ad, click-likelihood jumps hard.
- So **crush organic first** (answer-engine citation share), *then* run the ad on top of the moment you already win.
- ChatGPT is **non-deterministic** — the same prompt returns different agents each refresh. The goal is highest **citation share**, not winning every single time.

## 6. Landing pages = the "catcher's mitt"

This is where most spend leaks.

- Don't send ChatGPT clicks to a **generic homepage or a blog** — that pushes high-intent people back *up* the funnel.
- These clickers are **already absurdly high-intent** (they clicked past the answer). Meet them where they are with a **BOFU page that asks for the business.**
- Page must have: one **primary CTA** (restated down the page), **contact visible without scrolling**, the **agent's headshot**, fast load, clean mobile.
- **No forced registration** — it hurts SEO and Zillow doesn't do it. Let people who want to be leads become leads.
- The page must **match the ad's promise** (if the hint was "sell first or buy first," the page must deliver exactly that).
- Use **Donald Miller's "Marketing Made Simple"** wireframe for page order — AiM's own landing page follows it to a T.

## 7. Audience reality: 95% see a different ChatGPT than you do

- 95%+ of ChatGPT's ~1B users are on **free/Go** accounts — and **only free/Go users see ads.** (Plus users mostly never see them.)
- **Free = non-reasoning search** (linear, instant "Searching the web"). **Plus ($20) = agentic search** (query fan-out, slower, deeper).
- **Test in an incognito, logged-out window** to see the simpler experience your actual buyers/sellers get.

## 8. Beat the referral platforms by getting specific

- **realestateagents.com / My Agent Finder dominate generic round-one queries** ("best realtor in [city]"). Don't try to outbid them there.
- **Win by getting hyper-specific at the ad-group level** via context hints (persona + location + intent + moment). Specific situations surface your ad on round 2–3 of the conversation, where you can win.
- Nobody (including them) gets budget fully utilized — specificity is how a small budget claims its slice.

## 9. Platform facts that shifted (June 2026)

- **No more start/end dates** — campaigns run until the budget total is spent ("when it's gone, it's gone"). Campaign-total budget = a built-in safety cap.
- **Account = Business, not Individual.** Individual is blocked ("not yet available"); needs an EIN-type identifier. Tell the user to consult their own CPA/attorney on entity structure — not our call.
- **Financial-services restriction (important):** ads that mention money/financing get **flagged or auto-turned-off.** The **"pre-approved buyer" hint (#15 in the context-hint library) was shut off in tests.** Mortgage/lender ads will have a harder time. Keep copy off financing language.
- **Objective = Clicks.** Conversions **pixel tracking is currently unreliable** across the board (warnings like "no recent conversion events"). Don't optimize to it yet.

## 10. NEW organic signal — the Yelp × ChatGPT deal

- Yelp signed a **data-licensing deal with ChatGPT.** A **Yelp map-pack now appears in nearly every real-estate ChatGPT thread** — sometimes as the *only* source.
- Action: get a few **Yelp reviews** and prioritize the Yelp profile.
- This is **broader than ads** — it's an answer-engine visibility signal. Cross-ref `seo-optimizer` and the GBP/reputation workflow.

---

## Pantana's closing takeaways

1. When in doubt, **raise budget + max bid.**
2. Make the **headline/offer worth interrupting the chat.**
3. **Win organic + paid together.**
4. **Headshots matter.**
5. The **website must be the catcher's mitt** — or you're paying to push people back up the funnel.
