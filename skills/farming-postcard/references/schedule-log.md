# Schedule Log — Cron Run History

Each time Workflow B (scheduled preview) fires, append one line here:

```
[YYYY-MM-DD HH:MM] [run_type] target=[mail_date] options=[N] email_status=[draft_created|sent|failed]
```

`run_type` values: `15th-preview` (fires 8th of month) or `1st-preview` (fires 24th of month).

---

## Runs

[2026-05-27 14:00] TEST RUN (manual fire) target=2026-06-15 options=4 email_status=draft_created
  - Archetypes: Buyer-tagged, Anti-Zillow buyer pool, Equity refresh, WILDCARD live market activity
  - Triggered by Graeham to validate pipeline before June 8 cron
  - Gmail draft created for graehamwatts@gmail.com (not sent — for review)
  - Options cached in option-cache.md as pending pick

[2026-05-27 23:55] REAL SEND TEST (SMTP, on-brand v3 template) target=2026-06-15 options=4 email_status=sent
  - Recipients: graehamwatts@gmail.com + graehamwattsvideo@gmail.com
  - Subject: [ON-BRAND v3 TEST] Postcard options for June 15 — system check from Cowork
  - SMTP via smtp.gmail.com:465, authenticated with App Password
  - Pipeline confirmed working end-to-end. June 8 cron will fire cleanly without intervention.
