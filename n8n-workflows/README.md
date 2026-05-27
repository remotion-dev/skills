# n8n Workflow Backups

Reference copies and change summaries for n8n workflows on `n8n.graehamwattsn8n.com`. These are NOT importable JSON exports — the workflows live in n8n cloud and are edited there. These files document what the workflows do and what changed.

## Workflows tracked here

| Workflow | n8n ID | Trigger | Notes |
|---|---|---|---|
| PCFS — Sharon Daily + Weekly Handwritten Notes | `7CxqNkCQAuw1noGL` | Daily 8am PT (cron `0 8 * * *`) | Mon = full week roster; Tue–Sun = today's note(s) only. Changed from weekly to daily 2026-05-21. |
| PCFS — CMA Daily + Weekly Digest | `LHGnZC2X2KKXljB0` | Daily 9am PT (cron `0 9 * * *`) | Mon = next 2 weeks; Tue–Sun = CMAs due today. Changed from weekly to daily 2026-05-21. |
| PCFS — CMA Autobuild Watchdog | `SMQMpqyKWQVBkiZs` | Mon 11am PT (cron `0 11 * * 1`) | Watches the Cowork autobuild task. Pulls due-list webhook + searches Gmail. Alerts Graeham if expected CMA review emails are missing. Created 2026-05-26. |
