# Pipeline Sequences — Reference

The canonical pipeline sequences (workflow design, day-by-day touch cadence) for each GHL pipeline are documented in:

**Live URL:** https://graehamwatts.github.io/online-content/pipelines/GW_Pipeline_Sequences.html

**Local source (read-only — DO NOT edit through the skill):**
`C:\Users\Graeham Watts\Documents\Website stuff, Videos, social media\pipelines\GW_Pipeline_Sequences.html`

**GitHub repo:** `Graehamwatts/online-content` → `pipelines/GW_Pipeline_Sequences.html`
First commit pushed via direct GitHub Contents API: `0951d7fb85b99b49055eaa99d744ee21f4e78a93` on 2026-05-05.

---

## Why this matters for the dashboard

The pipeline-dashboard's aging-lead detection thresholds are derived from these sequences. When refresh.py decides whether a lead has been "forgotten," it compares the lead's last activity timestamp against the expected cadence defined in this document.

**Example:** If the New Lead - Contacted - Responded stage's documented cadence says "Day 1 → call, Day 3 → SMS, Day 5 → email, Day 7 → handwritten note" and a contact has been in that stage for 9 days with no logged activity since the call on Day 1 — that's a 4-day cadence violation, flagged Critical.

When the pipeline sequences document is updated:
1. Edit the source HTML in `Documents\Website stuff, Videos, social media\pipelines\`
2. Re-push to GitHub via the same direct API method
3. Update `data-contract.md`'s aging_leads thresholds table to match new cadences
4. The skill's refresh.py reads thresholds from data-contract — no per-stage hardcoding

---

## Integration with Past Clients Master Follow-up Schedule

`Past Clients Master Follow up schedule sheet.xlsx` defines the post-close cadence:
- **Quarterly Calls**: 13-week rotation, ~22 calls/week, run by Graeham daily
- **Anniversary Batches**: monthly, Peter creates LiftUp videos, Adrian schedules HippoVideo (8 days lead time)
- **Handwritten Notes**: Sharon writes ~5/week
- **CMA Schedule**: annual CMA fires 6 months after each anniversary (Adrian, weekly)
- **Bimonthly Market Update**: regular email cadence

Future enhancement (v2): pipeline-dashboard reads this Excel directly and shows execution status of each cadence (e.g., "This week's quarterly call batch: 22 clients, 12 called, 10 pending"). For v1, focus is the GHL pipeline visualization; cadence integration is deferred.
