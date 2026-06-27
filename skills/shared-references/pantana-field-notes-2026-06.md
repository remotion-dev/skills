# Pantana / AiM Field Notes — June 2026 ingest

Routing hub for cross-skill findings extracted from Graeham's Jason Pantana coaching folder (Pass 1 text extraction, 2026-06-27). Full source-doc backups live in Obsidian `06 Coaching & Training/Jason Pantana/Source Docs (extracted)/`. Skills load the section relevant to them.

---

## → seo-optimizer (AEO / answer-engine optimization)
Source: "AI Recommendation Engine" lecture (Feb 2026).
- **YouTube = #1 most-cited domain across AI search; Reddit = #2.** Prioritize a YouTube presence + relevant Reddit threads.
- AI **can't read review *content*** (gated/dynamic) but needs to know reviews exist → **spell accolades/awards out in bio text.** Zillow review *counts* are now machine-readable; Google/Yelp are not.
- Rotating citation sources in AI answers: FastExpert, Yelp 10Best, RealTrends, HomeLight (feeds US News), Zillow, RateMyAgent, Reddit.
- 4-step play: (1) be on the sites AI cites; (2) uniform E-E-A-T profiles across platforms; (3) publish proof pages / listicles using **best / top / versus** language; (4) seed Reddit / FB-group comments via happy clients; use the `site:reddit.com` operator to find threads.
- Ties to the Yelp×ChatGPT data deal already noted in `chatgpt-ads/references/troubleshooting.md`.

## → newsletter-generator + past-client-follow-up-system (Sharran "Profitable Content Machine")
- **Email Sprinkler System:** cadence ~3x/wk; avoid Mon-AM / Fri-PM; rotate themes; use a "super signature"; nurture swipe-file (Deal of the Week, gift-card, before-it-hits-market, dog-walker referral).
- **10-day Crash Course** email series for new opt-ins.
- **9-Point Opt-In Scorecard**; "Meh vs. Better" opt-in naming.
- **Money Map:** Channel → Hook → Conversion Mechanism → Lifetime Nurture ("find the gap, fill the gap"); 10/10/40/40 rule.
- **Social Funnel:** Tide Riser / Over Achiever / Hand Raiser + 9 engagement scripts.
- **Creator's Advantage:** run continuous low-budget ads on best-performing ORGANIC content ("Time on Brand is the new CTA").

## → content-creation-engine / concept-forge / cinematic-hooks
- **99 Video Scripts** swipe-file (REVB) = hook/idea bank (Buyers / Sellers / Investors / Personal Brand / General, ~20–30s each). Localize — San Diego-specific in places. Backup: `Source Docs (extracted)/REVB  99 Video Scripts For Realtors.md`.
- **Neighborhood News Blueprint** (green-screen hyperlocal news reels): source via Google Alerts / Newsbreak / Grok → custom GPT 1-paragraph script → BigVu teleprompter → Canva 3-image frame + CapCut auto-remove-BG; eye-contact correction; 8–15 posts/wk for topic authority.
- **Right content / right platform / right format:** market-snapshot videos underperform on IG, win on YouTube; weak IG engagement actively *hurts* reach — be selective about what posts to IG.

## → heygen-elevenlabs-renderer (voice clone)
Source: "Using AI to Tell Better Stories."
- Clone with **30+ min clean audio**; use **Pro mode**; tune speed / similarity / stability; keep all VO scripts in ONE ChatGPT thread so it learns your tone; **ElevenLabs Voice Changer** to match inflection from a temp recording.

## → higgsfield-video (image→video)
- Motion-constraint prompt (from `turn photos to video in elevenlabs.docx`): realistic gimbal / push-in only, **preserve everything in the reference photo, invent nothing** (no new windows / doors / light sources). Backup in Source Docs (extracted).

## → context-engineer (teaching reference only — NOT wired; already covered)
"Teach Claude Your Business" has a clean tokens / context-window / chat-compression explainer + the "Skills beat GPTs/Gems on tokens (on-demand loading)" rationale. The skill already implements this correctly; transcript is a teaching aid. Backup in vault.

## Maintenance flag
- Library/skill item `time-synced-property-tour-voiceover-script-generator` may be stale — the folder's XML prompt has a **Nov-2025 update** (frame interpolation moved ChatGPT → Claude). Verify/update the stored copy.

## Wiring status (2026-06-27)
- Wired (pointer added to SKILL.md): `seo-optimizer`, `newsletter-generator`, `content-creation-engine`.
- Staged here for quick wiring when next touched: `past-client-follow-up-system`, `heygen-elevenlabs-renderer`, `higgsfield-video`. (`context-engineer` intentionally not wired.)
