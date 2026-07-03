# Production Calendar Hardening (v7.3 — Apr 2026)

Referenced from SKILL.md. Load this file when producing scripts as part of a V6/V7 Production Calendar, or when debugging the daily N8N automation. The requirements below exist to prevent three failure modes encountered in production: year-drift in on-screen text, output truncation on long-form deliverables, and week-to-week content duplication.

## Date & Year QC (mandatory self-check block)

Every prompt in `PROMPT_LIBRARY` MUST carry a `DATE & YEAR QUALITY CONTROL` block placed immediately after Fair Housing Guardrails and before Voice & Style. The block instructs the generating model to:

- Treat the calendar's publication week as the current production date (e.g., April 2026 for the Apr 20-26 calendar).
- Force every year reference — text overlays, graphic callouts, on-screen stats, captions, email subject lines — to match the production year. Never a past year unless explicitly framed as historical with clear labeling.
- Open every cite-ready / AEO statement with a date anchor ("As of April 2026...", "As of Q2 2026..."). This makes statements durable for AI search engines to cite by name months later.
- Date-stamp every price/market stat ("As of April 2026, 3-bed SFH in Woodland Park is $680K-$850K") rather than emitting bare numbers.
- Self-scan the output before emitting and fix any bare-year drift.

The v7.3 production calendar contains the exact block text — copy it verbatim when building future calendars. This QC block is required on every format (YT Long Pt 1/2, Shorts, Reels, TikTok, Carousel, Blog, GMB, Facebook, Email), not just long-form.

## Identity & Date Validation Gate (mandatory, fail-closed)

Date and DRE errors have reached deliverables before, so QC *instructions* alone are not enough. Every content package, dashboard, and automated email MUST pass a programmatic gate before it is published or sent. The gate fails closed: if any hard check fails, the content does NOT go out and a human is alerted instead.

Hard checks (block on failure):

1. **DRE number.** `01466876` is the only DRE that may appear anywhere. The known-bad DRE (the `0201`-prefixed number that has leaked repeatedly in the past; the exact blocklist value lives in `shared-references/identity.json`) must never appear in any output. If it does, BLOCK immediately.
2. **Output not empty/truncated.** Generated text must be present and of reasonable length.

Soft checks (flag for review, do not auto-block):

3. **Correct DRE present where expected.** If a caption/CTA should carry the DRE and `01466876` is absent, flag it.
4. **Date correctness.** The current date is read from the system clock at run time — never typed from memory, never inferred. Every year/date reference must match the real production date; unlabeled past-year references are a failure.
5. **Range language for perishable figures.** Any rate/price/median stated as a single hard number not verified from a live source this run must be rewritten as a range (see `references/phases/script-writer/references/data-verification-and-nuance.md`).

Manual builds: run this gate as the final step before pushing or sending, and record the result.

Automated daily email: the gate is implemented as the **Validate Date + DRE** Code node in the N8N workflow below. The date is injected from the system clock in the **Compute Today** node (never guessed), and the validation node fails closed — on failure the workflow routes to an alert to Graeham instead of sending to Peter.

## Daily Automation — Peter's Daily Email (N8N)

A weekday email to Peter is produced by the N8N workflow **"Daily Content Email — Peter (script + SSML + production)"** (instance `n8n.graehamwattsn8n.com`, workflow id `REVqxrlAb3CHJumM`). It complements the weekly dashboard: Peter can work from the dashboard OR act straight from the email.

Flow: Schedule (Mon-Fri 6:00 AM PT) → CONFIG (`peter_email`, `cc_email`, `dashboard_url`) → Compute Today (system date → topic t1..t5, Mon=t1) → Fetch Dashboard HTML (the live weekly calendar is the single source of truth) → Parse Topic (pulls that day's `prod_script` + `prod_video` out of `COPY_DATA`) → Generate (OpenAI runs both prompts: script + SSML, then production assets) → Validate Date + DRE (fail-closed gate above) → IF passed → Email Peter (dashboard link + the day's full package); ELSE → Alert Graeham.

Operational notes:

- The workflow reads the LIVE published dashboard, so a corrected or new dashboard must be pushed to GitHub Pages before its content reaches the email.
- Update `CONFIG.dashboard_url` whenever a new week's dashboard is published; set `CONFIG.peter_email` once.
- Model is `gpt-4o-mini` for free-credit reliability; swap to `gpt-4o` or a paid key for higher script quality.
- Figures use range language; the script's "Verify before recording" block tells the human exactly which live numbers to confirm before shooting.

## Output Split Strategy (YouTube Long only)

A single YouTube Long prompt requesting 6 deliverables (Script + SSML + Editing Notes + AI Video Prompts + YouTube SEO Package + 3 Alt Hooks) produces roughly 40K-60K chars of output, which exceeds default `max_tokens` on most consumer AI tools and causes the model to truncate mid-Deliverable 4.

Split YouTube Long prompts into TWO buttons:

- **Pt 1 — Script + Voice** → Deliverables 1 (full timestamped script with inline shot tags) + 2 (complete ElevenLabs SSML block). Target output ~20-25K chars, fits in one response on any tool.
- **Pt 2 — Production Package** → Deliverables 3 (Editing Notes for Jason) + 4 (AI Video Prompts) + 5 (YouTube SEO Package) + 6 (3 Alt Hooks for A/B testing). Target output ~20-25K chars. Includes the standard 5-minute structure reference (hook / problem / core1 / core2 / advisory / CTA) so the production package works without pasting the script back in.

Both parts share the same preamble (Agent Identity + Fair Housing + DATE/YEAR QC + Voice + Topic + Funnel Tier + AEO + Key Facts + GHL Lead Capture). Only the deliverable list and output-mode header differ.

Short-form formats (YT Shorts, IG Reels, TikTok, Carousel, Blog, GMB, Facebook, Email newsletter) do NOT need splitting — their single output fits comfortably in one response.

## Week-over-Week Overlap Check (mandatory pre-ship)

Before shipping each weekly calendar, run an overlap comparison against the immediately preceding week's calendar. For each of the 5 daily topics plus the email newsletter, compare against the prior week's topics on:

- **Title** — substring match or semantic overlap (e.g., "EPA Homes Under $700K" vs "EPA Homes Under $1M" = HIGH overlap)
- **Slug** — exact or near-exact match
- **Neighborhood** — repeated primary-market focus on consecutive days
- **Funnel tier** — consecutive weeks of same tier + same topic cluster
- **GHL keyword** — keyword reuse across weeks

Classify each match as HIGH / MODERATE / LOW risk. Write a markdown comparison note (`YYYY-MM-DD-vs-PRIOR-content-overlap-check.md`) alongside the calendar HTML in `online-content/dashboards/weekly-calendars/` and commit it to the repo. HIGH-risk overlaps MUST be resolved before shipping — reframe the angle, replace the topic, or defer a week.

**Future systematization**: add a `TOPIC_HISTORY` object to the calendar HTML containing the last 4 weeks of (title, slug, neighborhood, tier, ghl_keyword) tuples. Future calendar generation runs an automatic pre-publish check against that history and flags overlaps without a manual pass.
