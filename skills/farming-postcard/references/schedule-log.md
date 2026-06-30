# Schedule Log — Cron Run History

Each time Workflow B (scheduled preview) fires, append one line here:

```
[YYYY-MM-DD HH:MM] [run_type] target=[mail_date] options=[N] email_status=[draft_created|sent|failed]
```

`run_type` values: `15th-preview` (fires 8th of month) or `1st-preview` (fires 24th of month).

---

## Runs

[2026-05-27 14:00] TEST RUN (manual fire, draft only) target=2026-06-15 options=4 email_status=draft_created
  - Archetypes: Buyer-tagged, Anti-Zillow buyer pool, Equity refresh, WILDCARD live market activity
  - Triggered to validate pipeline before June 8 cron
  - Gmail draft created — not sent (no SMTP credential yet)

[2026-05-27 23:55] REAL SEND TEST (SMTP, on-brand v3 template) target=2026-06-15 options=4 email_status=sent
  - Recipients: graehamwatts@gmail.com + graehamwattsvideo@gmail.com
  - Subject: [ON-BRAND v3 TEST] Postcard options for June 15 — system check from Cowork
  - SMTP via smtp.gmail.com:465, authenticated with App Password
  - Pipeline confirmed working

[2026-05-27 23:59] FULL PIPELINE TEST (SMTP, fresh remixed headlines) target=2026-06-15 options=4 email_status=sent
  - Recipients: graehamwatts@gmail.com + graehamwattsvideo@gmail.com
  - Subject: [TEST EMAIL] Postcard options for June 15 — full pipeline test
  - Archetypes: Buyer-tagged (NEW remix), Anti-Zillow buyer pool (NEW remix), Equity refresh (NEW remix), WILDCARD Value Gap (new sub-angle)
  - Demonstrates skill generates FRESH headlines vs. repeating prior options
  - Same archetype slate as prior test, completely different headline copy — validates remix patterns work
  - Pipeline confirmed end-to-end. June 8 cron will fire cleanly without intervention.

[2026-06-24 08:00] 1st-preview target=2026-07-01 options=0 email_status=MISSED_NO_FIRE
  - ⚠ TASK DID NOT FIRE ON SCHEDULE. App was closed on the 24th; the local Claude Code task `farming-postcard-1st-preview` (cron 0 8 24 * *) skipped its window.
  - A catch-up batch ran 2026-06-28 17:52 UTC (lastRunAt) alongside many other overdue tasks, but it produced NO options, NO cache entry, NO email — the workflow never completed.
  - Graeham discovered the gap on 2026-06-29 with the July 1 drop only 2 days out. Card built manually same day (Prop 19 Tax Transfer). See option-cache "2026-07-01 (manual recovery)".
  - ROOT CAUSE: local scheduled tasks only fire when the Cowork/Claude Code app is open. FIX FORWARD: migrate the two farming-postcard previews to a cloud GitHub Action cron (same pattern as daily-attribution-brief), so they fire regardless of app state. Tracked as OPEN.

[2026-06-08 08:00] 15th-preview target=2026-06-15 options=4 email_status=sent
  - Recipients: graehamwatts@gmail.com + graehamwattsvideo@gmail.com + graehamwattsvideo2@gmail.com
  - Subject: Postcard options for June 15 — pick one by June 12
  - Archetypes offered: Buyer-tagged, Anti-Zillow buyer pool, Equity, WILDCARD Low-Inventory Timing (fresh remixes, not copy/paste)
  - Excluded per repetition rule (last 3 shipped): Neighbor envy (06/01), Anti-Zestimate (05/15), AI search invisibility (05/01)
  - NOTE: AI search is a 15th-cadence bias target but shipped 05/01/26 (within last-3 window) -> excluded. Only 3 fresh library archetypes remained, so 1 fresh wildcard was added to reach 4 options.
  - Send: reused send_options_email.py send logic + its locked 3-recipient list; credential resolved from the live session mount.
  - FLAG: send_options_email.py APP_PASSWORD_FILE_LINUX is pinned to a retired session id (inspiring-awesome-hawking). A literal bash run of that script from any other session would fail credential lookup even though the password is valid. Recommend making that fallback session-agnostic (glob /sessions/*/mnt/Skills/).
  - Cached at option-cache.md under Pending picks; prior June-15 TEST entries marked superseded.
