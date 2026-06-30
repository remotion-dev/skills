# Phase 2 Build Blueprint — Fugu-Ultra investigation (2026-06-29)

Definitive root-cause + permanent-fix architecture from Fugu-Ultra (Sakana), commissioned after the July 1 preview silently no-showed. Phase 1 (server-side reminder + watchdog) is already live; this is the blueprint for Phase 2 (server-side option GENERATION via Sakana) + the evergreen CTA landing-page fix. Build order is at the bottom (Do-now vs Fast-follow).

---

Definitive finding: the root cause is complete. The permanent fix is to make `online-content` the single production system for scheduling, generation, state, CTA URLs, delivery, and alerting. Local scheduled tasks must never be in the production path again.

## 1. Root cause: complete and correct

Yes. The root cause is complete and correct.

The failure was not a bad cron. It was a bad automation boundary.

### Root cause

1. **The scheduler was local and app-state-dependent.**  
   The June 24 preview job existed, but it only ran when the desktop app was open. The shared `lastRunAt = 2026-06-28T17:52:32Z` across unrelated tasks proves a catch-up batch after the app reopened. The June 24 deadline was missed.

2. **The catch-up path was not reliable.**  
   The June 28 catch-up produced:
   - no email,
   - no schedule log,
   - no cached creative options,
   - no durable run artifact,
   - no alert.

3. **The SMTP credential path was brittle and stale.**  
   `send_options_email.py` had `APP_PASSWORD_FILE_LINUX` pinned to a retired local session path, so even a task-body execution could fail before resolving the Gmail app password.

Final finding:

> The preview system failed because a deadline-critical marketing automation was implemented as a local interactive-app scheduled task with a brittle local credential dependency and no durable artifact, no independent alert, and no self-healing watchdog. The app being closed caused the June 24 trigger to miss; the June 28 catch-up then failed silently.

Phase 1 fixed the biggest architectural defect: the trigger now runs server-side in GitHub Actions and the local tasks are disabled.

### Additional hardening to do

Do these. They close the remaining recurrence paths.

1. **Permanently remove the local scheduler from production.**  
   Disabled is good now. After two clean GitHub Action cycles, delete or archive the local scheduled tasks.

2. **Delete the stale local credential footgun.**  
   Remove or hard-fail `APP_PASSWORD_FILE_LINUX` in `send_options_email.py`. Production credentials must come only from GitHub Actions secrets.

3. **Separate generated-options state from email-sent state.**

   Use both:

   ```text
   data/farming-postcards/previews/YYYY-MM-DD/options.json
   data/farming-postcards/sent/YYYY-MM-DD.json
   data/farming-postcards/failures/YYYY-MM-DD.json
   ```

   Write the options artifact before email. Write the sent marker only after SMTP success.

4. **Make the watchdog self-healing.**  
   Current watchdog alerts. Upgrade it:

   - no options artifact inside preview window → generate options;
   - options artifact exists but no sent marker → resend email;
   - repeated failure → open/update GitHub Issue;
   - drop is close and still no selection/finalization → escalate.

5. **Add a concurrency guard for dual DST-safe crons.**

   ```yaml
   concurrency:
     group: farming-postcard-preview-${{ github.ref }}
     cancel-in-progress: false
   ```

   The committed marker gives idempotency. The concurrency guard prevents two scheduled runs from racing.

6. **Gate every scheduled run by Pacific local date.**  
   Compute using `America/Los_Angeles`, not UTC day.

   ```python
   def drop_date_for_preview_day(today_pt):
       if today_pt.day == 8:
           return date(today_pt.year, today_pt.month, 15)
       if today_pt.day == 24:
           if today_pt.month == 12:
               return date(today_pt.year + 1, 1, 1)
           return date(today_pt.year, today_pt.month + 1, 1)
       return None
   ```

7. **Add SMTP-independent success visibility.**  
   Email can succeed at SMTP and still land in spam. On successful generation, also create/update a GitHub Issue titled:

   ```text
   Postcard options ready: YYYY-MM-DD drop
   ```

   Put the rendered options and artifact link in the issue. Close it when Graeham selects the option.

8. **Protect against GitHub scheduled-workflow disappearance.**  
   Keep the repo active with committed state changes and add a monthly heartbeat/status check so the schedule cannot silently age out.

9. **Add tests for the exact failure class.**

   Required tests:

   - missing Gmail secret fails loudly;
   - missing Sakana key fails loudly;
   - invalid LLM JSON does not write a sent marker;
   - SMTP failure preserves options artifact and opens an issue;
   - watchdog can recover a missing scheduled run;
   - Pacific date logic handles December 24 → January 1;
   - dual cron does not double-send.

---

## 2. Phase 2: yes, GitHub Action should generate options server-side

Yes. The GitHub Action should generate the 3–5 hook options itself by calling Sakana/Fugu server-side. This fully replaces the local scheduled task.

The scheduled Action becomes the production source of truth. The local task remains disabled and later deleted.

### Permanent Phase 2 architecture

```text
GitHub Actions
  ├── schedule / workflow_dispatch / watchdog
  ├── compute Pacific preview date and drop date
  ├── load shipped-card history
  ├── load CTA inventory
  ├── compute deterministic blocked sets
  ├── call Sakana/Fugu for candidate options
  ├── validate with Python, not the LLM
  ├── top up with deterministic fallback if needed
  ├── commit options artifact
  ├── email Graeham
  ├── open/update GitHub Issue
  └── commit sent marker only after SMTP success
```

Recommended files:

```text
.github/workflows/farming-postcard-reminder.yml
scripts/postcard_preview_generate.py
scripts/validate_postcard_options.py
scripts/sync_farming_postcard_history.py
data/farming-postcards/history.json
data/farming-postcards/cta_inventory.json
data/farming-postcards/claim_library.json
data/farming-postcards/template_bank.json
data/farming-postcards/previews/
data/farming-postcards/sent/
data/farming-postcards/failures/
```

### Scheduling behavior

Keep the existing 8th/24th dual UTC cron strategy, but make the script authoritative.

Run flow:

1. Compute `today_pt` in `America/Los_Angeles`.
2. If local day is not `8` or `24`, scheduled REMIND/GENERATE mode exits cleanly.
3. If local day is `8`, target drop is the `15th` of the same month.
4. If local day is `24`, target drop is the `1st` of the next month.
5. If `sent/YYYY-MM-DD.json` exists, exit cleanly.
6. If `previews/YYYY-MM-DD/options.json` exists but sent marker does not, resend existing artifact.
7. Otherwise generate new options.

### History recommendation

Vendor and canonicalize the history into `online-content`.

Do not make the scheduled run depend on a second repo at runtime.

The current history lives in another repo in:

```text
farming-postcard/archive.json
headline-library.md
```

Do a one-time import into:

```text
online-content/data/farming-postcards/history.json
```

Then make `online-content` the canonical history store going forward. The finalize/ship workflow should append the selected shipped card there.

Reason: a scheduled production job must not depend on a second repo’s permissions, branch, path stability, network availability, or token. A cross-repo runtime dependency is another silent-failure vector.

Normalized history schema:

```json
{
  "schema_version": "farming_postcard_history.v1",
  "updated_at": "2026-07-01T00:00:00Z",
  "cards": [
    {
      "drop_date": "2026-07-01",
      "status": "shipped",
      "headline": "Text Graeham for your East Palo Alto seller check",
      "archetype": "seller_consultation",
      "cta_destination_id": "sms_keyword",
      "villain_type": "none",
      "core_claim_slug": "local-human-guidance-beats-generic-advice",
      "source": {
        "legacy_archive_path": "farming-postcard/archive.json",
        "legacy_tracker_path": "headline-library.md",
        "legacy_commit": "abc123"
      }
    }
  ]
}
```

### Deterministic 4-axis guardrails

The LLM should receive constraints, but Python enforces them. The model is allowed to propose; the validator decides.

Build blocked sets from shipped history:

```python
def shipped_cards(history):
    cards = [c for c in history["cards"] if c["status"] == "shipped"]
    return sorted(cards, key=lambda c: c["drop_date"], reverse=True)

def build_constraints(history):
    shipped = shipped_cards(history)

    last_3 = shipped[:3]
    last_2 = shipped[:2]
    last_4 = shipped[:4]

    return {
        "blocked_archetypes": sorted({c["archetype"] for c in last_3}),
        "blocked_cta_destination_ids": sorted({c["cta_destination_id"] for c in last_2}),
        "zillow_algorithm_villain_blocked": any(
            c.get("villain_type") == "zillow_algorithm"
            for c in last_2
        ),
        "blocked_core_claim_slugs": sorted({c["core_claim_slug"] for c in last_4})
    }
```

#### Rule 1: archetype 3-card cooldown

Reject an option if:

```python
option["archetype"] in constraints["blocked_archetypes"]
```

Use a controlled enum, for example:

```json
[
  "local_market_signal",
  "seller_math",
  "buyer_demand",
  "neighbor_story",
  "myth_buster",
  "equity_check",
  "prop_19",
  "seasonal_timing",
  "off_market_opportunity",
  "seller_consultation"
]
```

You need at least 6 archetypes available because the cooldown blocks 3 and the preview must produce at least 3 distinct options. Ten is healthy.

#### Rule 2: CTA destination differs from last 2 cards

Reject an option if:

```python
option["cta_destination_id"] in constraints["blocked_cta_destination_ids"]
```

Compare by destination ID, not URL.

Correct:

```text
home_valuation
off_market_buyers
prop_19_guide
sms_keyword
seller_consultation
```

Incorrect:

```text
https://site.com/east-palo-alto/home-valuation/?utm_campaign=...
```

The LLM must not emit URLs. It emits only `cta_destination_id`. The script constructs the final URL from `cta_inventory.json`.

#### Rule 3: no Zillow/algorithm villain for 2 cards after a villain card

If either of the last two shipped cards used a Zillow/algorithm villain, reject any new option with:

```json
"villain_type": "zillow_algorithm"
```

Also text-scan all generated copy during the cooldown. Reject terms like:

```text
Zillow
algorithm
AVM
automated estimate
online estimate
portal estimate
computer estimate
```

This prevents the model from labeling the option `"villain_type": "none"` while still using the forbidden villain in the copy.

#### Rule 4: core claim not repeated within 4 cards

Reject an option if:

```python
option["core_claim_slug"] in constraints["blocked_core_claim_slugs"]
```

Use a controlled claim library. Do not let the LLM invent arbitrary claim IDs.

Important: the claim library must have at least 7 usable claims. Four is not enough because the last four can all be blocked, and the preview still needs three valid distinct options.

Use 8–10 claims minimum, for example:

```json
[
  "local-human-pricing-beats-generic-comps",
  "off-market-demand-can-exist-before-public-listing",
  "pre-listing-prep-increases-buyer-confidence",
  "prop-19-planning-can-change-move-timing",
  "equity-can-fund-the-next-move",
  "inventory-scarcity-rewards-prepared-sellers",
  "interest-rate-shifts-change-buyer-math",
  "neighborhood-specific-guidance-beats-countywide-averages",
  "seller-timing-matters-before-public-launch",
  "local-agent-access-creates-better-selling-options"
]
```

Add a feasibility preflight:

```python
def assert_feasible(all_archetypes, all_claims, all_ctas, constraints):
    available_archetypes = set(all_archetypes) - set(constraints["blocked_archetypes"])
    available_claims = set(all_claims) - set(constraints["blocked_core_claim_slugs"])
    available_ctas = set(all_ctas) - set(constraints["blocked_cta_destination_ids"])

    problems = []

    if len(available_archetypes) < 3:
        problems.append("fewer than 3 available archetypes")

    if len(available_claims) < 3:
        problems.append("fewer than 3 available core claims")

    if len(available_ctas) < 1:
        problems.append("no available CTA destination")

    if problems:
        raise RuntimeError("; ".join(problems))
```

Within a candidate batch, require distinct `archetype` and distinct `core_claim_slug`. CTA does not need to be distinct within the batch unless you build at least 5 CTA destinations. Only one option ships.

### LLM call design

Ask Sakana/Fugu for 7–8 candidates, not 3. Then validate and select the best 3–5.

Prompt content:

- farm: East Palo Alto;
- agent: Graeham;
- target drop date;
- allowed archetypes;
- blocked archetypes;
- allowed CTA destination IDs;
- blocked CTA destination IDs;
- allowed core claim slugs;
- blocked core claim slugs;
- whether Zillow/algorithm villain is blocked;
- required JSON schema;
- instruction that invalid options will be discarded.

The prompt should say:

```text
Return strict JSON only. Do not return Markdown. Do not invent CTA URLs. Use only allowed enum values. Any option violating the constraints will be discarded.
```

### Output schema

The LLM returns candidate options without URLs:

```json
{
  "schema_version": "postcard_option_candidates.v1",
  "candidates": [
    {
      "archetype": "off_market_opportunity",
      "core_claim_slug": "off-market-demand-can-exist-before-public-listing",
      "villain_type": "none",
      "headline": "Before You List, See Who’s Already Looking in East Palo Alto",
      "subheadline": "A quiet buyer check can change your selling strategy.",
      "hook_summary": "Positions Graeham as the local agent who can surface buyer demand before a public listing.",
      "cta_destination_id": "off_market_buyers",
      "cta_text": "Scan to see current off-market buyer demand",
      "front_concept": "Clean headline, East Palo Alto map texture, QR callout.",
      "back_copy_outline": [
        "Open with the idea that timing matters.",
        "Explain that some buyers are already searching quietly.",
        "Invite the owner to request a private buyer-demand check."
      ],
      "proof_needed": [
        "Recent buyer inquiry count or CRM-safe qualitative note"
      ],
      "compliance_notes": [
        "Do not guarantee a buyer or sale price."
      ]
    }
  ]
}
```

The committed artifact is generated by the script after validation and URL construction:

```json
{
  "schema_version": "postcard_preview_options.v1",
  "drop_date": "2026-07-15",
  "preview_due_date": "2026-07-08",
  "farm": "East Palo Alto",
  "agent": "Graeham",
  "generated_at": "2026-07-08T15:05:00Z",
  "generator": {
    "provider": "sakana_fugu",
    "model": "configured-in-github-variable",
    "mode": "scheduled"
  },
  "history_source": {
    "path": "data/farming-postcards/history.json"
  },
  "constraints": {
    "blocked_archetypes": ["seller_math", "prop_19", "buyer_demand"],
    "blocked_cta_destination_ids": ["sms_keyword", "home_valuation"],
    "zillow_algorithm_villain_blocked": false,
    "blocked_core_claim_slugs": [
      "pre-listing-prep-increases-buyer-confidence",
      "equity-can-fund-the-next-move"
    ]
  },
  "options": [
    {
      "id": "2026-07-15-A",
      "source": "llm",
      "archetype": "off_market_opportunity",
      "core_claim_slug": "off-market-demand-can-exist-before-public-listing",
      "villain_type": "none",
      "headline": "Before You List, See Who’s Already Looking in East Palo Alto",
      "subheadline": "A quiet buyer check can change your selling strategy.",
      "hook_summary": "Positions Graeham as the local agent who can surface buyer demand before a public listing.",
      "cta_destination_id": "off_market_buyers",
      "cta_text": "Scan to see current off-market buyer demand",
      "cta_url": "https://example.com/east-palo-alto/off-market-buyers/?utm_source=postcard&utm_medium=qr&utm_campaign=2026-07-15&utm_content=A&drop_date=2026-07-15&cta_destination_id=off_market_buyers&qr_id=2026-07-15-A",
      "front_concept": "Clean headline, East Palo Alto map texture, QR callout.",
      "back_copy_outline": [
        "Open with the idea that timing matters.",
        "Explain that some buyers are already searching quietly.",
        "Invite the owner to request a private buyer-demand check."
      ],
      "proof_needed": [
        "Recent buyer inquiry count or CRM-safe qualitative note"
      ],
      "compliance_notes": [
        "Do not guarantee a buyer or sale price."
      ],
      "rule_check": {
        "archetype_3_card_cooldown": true,
        "cta_not_used_last_2": true,
        "zillow_algorithm_villain_cooldown": true,
        "core_claim_not_used_last_4": true
      }
    }
  ]
}
```

### Validation

Reject the batch unless the final selected set has 3–5 valid options.

Per-option validation:

- `headline` non-empty;
- `subheadline` non-empty;
- `hook_summary` non-empty;
- `archetype` in allowed enum;
- `archetype` not used in last 3 shipped cards;
- `core_claim_slug` in claim library;
- `core_claim_slug` not used in last 4 shipped cards;
- `cta_destination_id` in `cta_inventory.json`;
- `cta_destination_id` not used in last 2 shipped cards;
- `villain_type` in allowed enum;
- if villain cooldown active, no Zillow/algorithm villain and no banned terms;
- no guaranteed sale price;
- no guaranteed buyer;
- no fake valuation promise;
- no invented URL;
- no empty CTA;
- no duplicate headline in the batch.

Batch validation:

- 3–5 final options;
- distinct `archetype` across final options;
- distinct `core_claim_slug` across final options;
- all options pass all four differentiation rules;
- every CTA URL is constructed server-side from approved inventory;
- artifact is committed before email;
- sent marker is committed only after SMTP success.

### CTA URL construction

The model emits:

```json
"cta_destination_id": "home_valuation"
```

The script constructs:

```python
def build_cta_url(destination, drop_date, option_letter):
    canonical = destination["canonical_url"]
    if canonical is None:
        return None

    return (
        f"{canonical}"
        f"?utm_source=postcard"
        f"&utm_medium=qr"
        f"&utm_campaign={drop_date}"
        f"&utm_content={option_letter}"
        f"&drop_date={drop_date}"
        f"&cta_destination_id={destination['id']}"
        f"&qr_id={drop_date}-{option_letter}"
    )
```

This permanently eliminates LLM-invented landing-page URLs.

### Fallback ladder

Use this exact failure ladder:

1. **Sakana call fails** → retry with exponential backoff.
2. **Sakana returns invalid JSON** → make one repair call using validator errors.
3. **Still invalid or fewer than 3 valid options** → keep valid LLM options and top up from deterministic templates.
4. **Template top-up succeeds** → email options and open an issue noting degraded mode.
5. **History, claim library, or CTA inventory is infeasible/corrupt** → send the existing deterministic REMINDER email and open a failure issue.
6. **SMTP fails** → commit options artifact, do not write sent marker, open/update issue.
7. **Watchdog sees artifact but no sent marker** → resend email from the artifact.
8. **Watchdog sees neither artifact nor sent marker inside the 7-day window** → run generation.
9. **Drop is within 3 days and still no successful email** → subject line becomes urgent:

   ```text
   URGENT: Postcard options for YYYY-MM-DD drop — late recovery
   ```

The deterministic fallback should use a committed template bank:

```text
data/farming-postcards/template_bank.json
```

Each template maps:

```text
archetype + core_claim_slug + cta_destination_id
```

to conservative headline/subheadline/copy structures.

---

## 3. Secrets: safest Sakana key wiring

Use a GitHub Actions repository secret or production environment secret named:

```text
SAKANA_API_KEY
```

The human sets it here:

```text
online-content repo
→ Settings
→ Secrets and variables
→ Actions
→ New repository secret
```

Use non-secret GitHub variables for config:

```text
SAKANA_BASE_URL
SAKANA_MODEL
POSTCARD_TO_EMAIL
POSTCARD_FROM_NAME
```

Use the secret only at the step level:

```yaml
permissions:
  contents: write
  issues: write

jobs:
  postcard-preview:
    runs-on: ubuntu-latest
    concurrency:
      group: farming-postcard-preview-${{ github.ref }}
      cancel-in-progress: false

    steps:
      - uses: actions/checkout@v4

      - name: Generate postcard preview options
        env:
          SAKANA_API_KEY: ${{ secrets.SAKANA_API_KEY }}
          SAKANA_BASE_URL: ${{ vars.SAKANA_BASE_URL }}
          SAKANA_MODEL: ${{ vars.SAKANA_MODEL }}
          GMAIL_USERNAME: ${{ secrets.GMAIL_USERNAME }}
          GMAIL_APP_PASSWORD: ${{ secrets.GMAIL_APP_PASSWORD }}
          POSTCARD_TO_EMAIL: ${{ vars.POSTCARD_TO_EMAIL }}
        run: |
          python scripts/postcard_preview_generate.py --mode scheduled
```

Add an explicit preflight:

```python
if not os.environ.get("SAKANA_API_KEY"):
    raise RuntimeError("SAKANA_API_KEY is not configured")

if not os.environ.get("GMAIL_USERNAME"):
    raise RuntimeError("GMAIL_USERNAME is not configured")

if not os.environ.get("GMAIL_APP_PASSWORD"):
    raise RuntimeError("GMAIL_APP_PASSWORD is not configured")
```

Avoid all of this:

- Do not commit the key.
- Do not put it in GitHub Pages JavaScript.
- Do not put it in `.env` files.
- Do not upload `.env` files as artifacts.
- Do not echo the key.
- Do not run with `set -x`.
- Do not log request headers.
- Do not include the key in prompts.
- Do not include the key in committed artifacts.
- Do not pass secrets to untrusted pull-request workflows.
- Do not use `pull_request_target` for this automation.
- Do not add a cross-repo PAT to the scheduled generation path.
- Do not use local credential files in production.

---

## 4. Permanent fix for CTA / landing-page blocker

Build evergreen CTA landing pages on the existing GitHub Pages site and make the generator choose only from an approved CTA inventory.

Minimum viable version: three branded landing pages plus GHL forms.

### Required MVP pages

1. **Home valuation**

   ```text
   /east-palo-alto/home-valuation/
   ```

   CTA:

   ```text
   Request a human East Palo Alto home-value review
   ```

2. **Off-market buyers**

   ```text
   /east-palo-alto/off-market-buyers/
   ```

   CTA:

   ```text
   See if there are quiet buyers for your home
   ```

3. **Prop 19 guide**

   ```text
   /east-palo-alto/prop-19-guide/
   ```

   CTA:

   ```text
   Get the Prop 19 move-planning checklist
   ```

Three evergreen destinations are the minimum because the CTA rule blocks the last two shipped destinations. With three destinations, there is always at least one legal non-blocked CTA.

Keep `sms_keyword` as an emergency fallback, not the primary plan.

### Required page contents

Each page must have:

- Graeham branding;
- East Palo Alto-specific headline;
- short benefit copy;
- embedded GHL form;
- phone/text fallback;
- brokerage/legal footer;
- thank-you redirect;
- GHL tracking script or analytics script;
- UTM capture into hidden fields.

Hidden fields:

```text
utm_source
utm_medium
utm_campaign
utm_content
drop_date
cta_destination_id
qr_id
page_slug
```

Minimal UTM capture script:

```html
<script>
(function () {
  const params = new URLSearchParams(window.location.search);
  [
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_content",
    "drop_date",
    "cta_destination_id",
    "qr_id",
    "page_slug"
  ].forEach(function (key) {
    const value = params.get(key);
    const field = document.querySelector('[name="' + key + '"]');
    if (value && field) field.value = value;
  });
})();
</script>
```

### GHL setup

In GHL:

- one form per CTA, or one reusable form with hidden `cta_destination_id`;
- create/update contact on submit;
- tag contact;
- notify Graeham immediately;
- redirect to thank-you page.

Recommended tags:

```text
Postcard QR
East Palo Alto Farm
CTA: Home Valuation
CTA: Off-Market Buyers
CTA: Prop 19
```

### CTA inventory

Commit this file:

```text
data/farming-postcards/cta_inventory.json
```

Example:

```json
{
  "schema_version": "cta_inventory.v1",
  "destinations": [
    {
      "id": "home_valuation",
      "label": "Home valuation request",
      "canonical_url": "https://example.com/east-palo-alto/home-valuation/",
      "allowed": true
    },
    {
      "id": "off_market_buyers",
      "label": "Off-market buyer demand check",
      "canonical_url": "https://example.com/east-palo-alto/off-market-buyers/",
      "allowed": true
    },
    {
      "id": "prop_19_guide",
      "label": "Prop 19 guide",
      "canonical_url": "https://example.com/east-palo-alto/prop-19-guide/",
      "allowed": true
    },
    {
      "id": "sms_keyword",
      "label": "Call/text fallback",
      "canonical_url": null,
      "allowed": true
    }
  ]
}
```

The generator must only use destinations in this file.

No approved destination in `cta_inventory.json` means the CTA is not eligible. The LLM never invents landing pages.

---

## 5. Prioritized build order

## Do now

1. **Keep Phase 1 live.**  
   GitHub Actions remains the only production scheduler. Local tasks stay disabled.

2. **Remove the stale local credential path.**  
   Delete or hard-fail `APP_PASSWORD_FILE_LINUX` in the old send script.

3. **Add durable state directories.**

   ```text
   data/farming-postcards/previews/
   data/farming-postcards/sent/
   data/farming-postcards/failures/
   ```

4. **Canonicalize history into `online-content`.**  
   Import the other repo’s `archive.json` and `headline-library.md` into:

   ```text
   data/farming-postcards/history.json
   ```

   Going forward, the finalize/ship workflow writes to this file.

5. **Create the controlled libraries.**

   ```text
   data/farming-postcards/cta_inventory.json
   data/farming-postcards/claim_library.json
   data/farming-postcards/template_bank.json
   ```

   Use at least:
   - 8–10 archetypes;
   - 8–10 core claims;
   - 3 CTA landing-page destinations plus SMS fallback.

6. **Build the three evergreen landing pages.**

   ```text
   /east-palo-alto/home-valuation/
   /east-palo-alto/off-market-buyers/
   /east-palo-alto/prop-19-guide/
   ```

7. **Wire the pages to GHL.**  
   Embed forms, capture UTMs, tag contacts, notify Graeham, and test one real submission per page.

8. **Add `SAKANA_API_KEY` to GitHub Actions secrets.**

9. **Implement `postcard_preview_generate.py`.**  
   Required behavior:
   - Pacific date gating;
   - drop-date computation;
   - idempotency by drop date;
   - load history;
   - load CTA inventory;
   - load claim library;
   - feasibility preflight;
   - build deterministic blocked sets;
   - call Sakana/Fugu;
   - validate strict JSON;
   - enforce all four differentiation rules;
   - construct CTA URLs server-side;
   - top up from deterministic templates if needed;
   - commit options artifact;
   - email Graeham;
   - open/update GitHub Issue;
   - write sent marker only after SMTP success.

10. **Add workflow concurrency.**

   ```yaml
   concurrency:
     group: farming-postcard-preview-${{ github.ref }}
     cancel-in-progress: false
   ```

11. **Upgrade watchdog to self-healing.**

   - Missing options artifact → generate.
   - Artifact exists but no sent marker → resend.
   - Repeated failure → issue.
   - Close to drop with no selection → urgent escalation.

12. **Run `workflow_dispatch` end-to-end.**  
   Verify:
   - options generated;
   - all rules enforced;
   - artifact committed;
   - email received;
   - GitHub Issue created/updated;
   - sent marker committed;
   - SMTP failure path works;
   - invalid LLM output path works;
   - watchdog recovery path works.

13. **Flip scheduled mode from REMIND to GENERATE.**  
   Keep REMIND only as the terminal fallback rung.

## Fast-follow

1. **Add selected/finalized markers.**

   ```text
   data/farming-postcards/selected/YYYY-MM-DD.json
   data/farming-postcards/finalized/YYYY-MM-DD.json
   ```

   The chain should track: generated → sent → selected → finalized → mailed.

2. **Add per-drop QR wrapper pages.**

   ```text
   /qr/2026-07-15/home-valuation-a/
   /qr/2026-07-15/off-market-buyers-b/
   /qr/2026-07-15/prop-19-c/
   ```

3. **Generate QR images automatically.**  
   Store PNG/SVG QR assets with the preview artifact.

4. **Add a fourth evergreen CTA page.**

   ```text
   /east-palo-alto/seller-consultation/
   ```

   This gives more CTA rotation headroom.

5. **Add weekly link checking.**  
   Every URL in `cta_inventory.json` must return 200.

6. **Add analytics dashboard.**  
   Track:
   - QR scans;
   - landing-page views;
   - form submissions;
   - conversion by drop;
   - conversion by CTA destination.

7. **Add SMS escalation for critical misses.**  
   GitHub Issues are the SMTP-independent baseline. SMS is the next layer for T-minus-3-day failures.

8. **Delete the old local task wrappers after two clean cycles.**

Final permanent architecture:

> GitHub Actions schedules, watches, generates, validates, persists, emails, and alerts. Sakana/Fugu supplies candidate creative. Python enforces the rules. Git commits preserve state. GitHub Issues provide SMTP-independent visibility. GitHub Pages supplies evergreen CTA URLs. GHL captures QR leads. Local scheduled tasks are removed from production.

=== tokens ===
[fugu] model=fugu-ultra tokens: prompt=2330 completion=11259 total=81665
