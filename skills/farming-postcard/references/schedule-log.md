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
