# Pipeline Dashboard — Data Contract

> The exact JSON schema that `scripts/refresh.py` produces and `templates/index.html` consumes. Lock this BEFORE building the dashboard HTML so we don't iterate on plumbing.

The output file lives at `online-content/dashboards/pipeline/data.json` and is served alongside the dashboard. The dashboard fetches it on page load.

---

## Top-Level Shape

```json
{
  "_meta": {
    "generated_at": "2026-05-04T07:00:00-07:00",
    "ghl_location_id": "6wuU3haUH7uNeT20E3UZ",
    "contact_total": 4027,
    "opportunity_total": 2891,
    "schema_version": "1.0",
    "data_freshness_seconds": 300,
    "source_run": "github_action_cron" 
  },

  "scorecards": { ... },
  "timeline": [ ... ],
  "sankey": { ... },
  "past_client_engine": { ... },
  "lead_sources": [ ... ],
  "adrian_activity": { ... },
  "aging_leads": [ ... ],
  "heat_map": { ... },
  "lead_table": [ ... ],
  "pipelines": [ ... ]
}
```

---

## scorecards

```json
{
  "scorecards": {
    "today":     {"new_leads": 3, "active_value_usd": 8400000, "conversion_pct_to_closed": 12.4},
    "past_3d":   {"new_leads": 11, "active_value_usd": 8400000, "conversion_pct_to_closed": 12.4},
    "this_week": {"new_leads": 27, "active_value_usd": 8400000, "conversion_pct_to_closed": 12.4},
    "this_month":{"new_leads": 102, "active_value_usd": 8400000, "conversion_pct_to_closed": 12.4},
    "ytd":       {"new_leads": 482, "active_value_usd": 8400000, "conversion_pct_to_closed": 12.4},
    "lifetime":  {"new_leads": 4027, "active_value_usd": 8400000, "conversion_pct_to_closed": 12.4},
    "last_7d_vs_prior_7d": {
      "current": {"new_leads": 27, "appointments_set": 4, "closed_won": 1, "lost": 2, "value_added_usd": 13500000},
      "prior":   {"new_leads": 19, "appointments_set": 2, "closed_won": 0, "lost": 5, "value_added_usd": 9100000},
      "delta_pct": {"new_leads": 42.1, "appointments_set": 100.0, "closed_won": null, "lost": -60.0, "value_added_usd": 48.4},
      "trend": "improving"
    }
  }
}
```

Notes:
- `active_value_usd` is the same number across all time windows — it represents currently-open pipeline value (sum of `monetaryValue` on opportunities in non-terminal stages). It's intentionally NOT period-scoped.
- `conversion_pct_to_closed` is the % of leads that came in during that period that have reached "Closed" (Past Buyers/Sellers pipeline).
- `last_7d_vs_prior_7d` is the rolling week-over-week comparison. `delta_pct` shows percent change. `trend` is one of: "improving" / "flat" / "declining" based on weighted average of the deltas. The dashboard renders this as a hero strip below the main scorecards with up/down arrows + colored deltas.

---

## timeline

Array of daily counts, used by the ECharts dataZoom timeline. The chart renders new-leads-per-day with overlay of conversions-per-day.

```json
{
  "timeline": [
    {"date": "2024-01-01", "new_leads": 2, "conversions": 0, "lost": 1},
    {"date": "2024-01-02", "new_leads": 1, "conversions": 1, "lost": 0},
    ...
  ]
}
```

Range: lifetime (back to oldest contact `dateAdded`). Default view is last 90 days; user can zoom out to 5Y or in to a custom date range.

---

## sankey

The cyclic flow visualization. Three columns: sources → active → outcomes. The "Past Client" outcome visually loops back as "Referral" and "Repeat Business" sources.

```json
{
  "sankey": {
    "nodes": [
      {"id": "src_direct", "name": "Direct New Lead", "column": "source", "color": "#3498db"},
      {"id": "src_referral", "name": "Past Client Referral", "column": "source", "color": "#9b59b6"},
      {"id": "src_repeat", "name": "Past Client Repeat", "column": "source", "color": "#9b59b6"},
      
      {"id": "active_buyer", "name": "Buyer Pipeline", "column": "active", "color": "#2d4278", "stages": [...]},
      {"id": "active_seller", "name": "Seller Pipeline", "column": "active", "color": "#2d4278", "stages": [...]},
      {"id": "active_investor", "name": "Investor/Flipper", "column": "active", "color": "#2d4278", "stages": [...]},
      
      {"id": "out_past_client", "name": "Past Client Pool", "column": "outcome", "color": "#9b59b6", "loops_to": ["src_referral", "src_repeat"]},
      {"id": "out_lost", "name": "Lost (other agent)", "column": "outcome", "color": "#e67e22"},
      {"id": "out_dead", "name": "Cold / Unqualified", "column": "outcome", "color": "#6c757d"}
    ],
    "links": [
      {"source": "src_direct", "target": "active_buyer", "value": 142, "value_usd": 71000000, "contact_ids": ["abc123", ...]},
      {"source": "src_referral", "target": "active_seller", "value": 12, "value_usd": 9600000, "contact_ids": [...]},
      {"source": "active_buyer", "target": "out_past_client", "value": 28, "value_usd": 14000000, "contact_ids": [...]},
      ...
    ]
  }
}
```

**Drill-down behavior in the dashboard:**
- Hover any link → tooltip shows count + $ value + first 5 contact names + "view all"
- Click any link → side panel opens with full list of contact names + last activity + opp value
- Macro view: shows pipeline-to-pipeline aggregate (collapses stages)
- Mid view: clicking a pipeline expands its stages as inner Sankey
- Micro view: clicking any band → individual contact list

---

## past_client_engine

```json
{
  "past_client_engine": {
    "total_past_clients": 287,
    "past_buyers": 142,
    "past_sellers": 145,
    "referrals_ytd": 14,
    "referrals_lifetime": 89,
    "repeat_business_ytd": 3,
    "repeat_business_lifetime": 22,
    "avg_years_between_transactions": 6.4,
    "top_referring_past_clients": [
      {"name": "Sarah Johnson", "referrals_count": 7, "last_referral_date": "2026-04-12"},
      {"name": "Mark Lee", "referrals_count": 4, "last_referral_date": "2026-02-28"}
    ],
    "reactivation_signals": [
      {
        "contact_id": "abc123",
        "name": "Jane Doe",
        "signal": "Inbound message yesterday",
        "last_transaction_year": 2018,
        "current_pipeline_stage": "Past Buyer / Looking to sell"
      }
    ]
  }
}
```

The "reactivation_signals" array shows past clients showing fresh interest — these are the highest-value re-engagement targets.

The "top_referring_past_clients" array is sourced from the `contact.referred_by` custom field (created in GHL on 2026-05-05, field ID `aCIXKsxuECYRLPw84FAe`). Whenever a new lead is added with a referring past client's name in that field, refresh.py increments the referrer's count. This is your "best advocates" board — the past clients you should be sending closing gifts to every year.

---

## lead_sources

```json
{
  "lead_sources": [
    {
      "source": "Zillow",
      "volume": 287,
      "active_now": 14,
      "closed_won": 3,
      "closed_lost": 8,
      "still_pending": 262,
      "conversion_pct": 1.05,
      "total_value_usd": 1500000,
      "avg_days_to_first_contact": 0.4
    },
    ...
  ]
}
```

Sorted by `total_value_usd` descending. Source values come from GHL's `contact_source` and `opportunity_source` fields.

---

## adrian_activity

```json
{
  "adrian_activity": {
    "user_id": "...",
    "name": "Adrian Aboniawan",
    "today": {
      "dials": 47,
      "contacts_attempted": 22,
      "conversations": 4,
      "sms_sent": 18,
      "emails_sent": 12,
      "appointments_set": 1,
      "notes_logged": 12,
      "tasks_completed": 8
    },
    "this_week": { /* same shape */ },
    "targets_daily": {
      "dials": 60,
      "contacts_attempted": 25,
      "conversations": 5,
      "sms_sent": 20,
      "emails_sent": 10,
      "appointments_set": 2,
      "notes_logged": 15,
      "tasks_completed": 10
    },
    "vs_target_pct": {
      "dials": 78,
      "contacts_attempted": 88,
      "conversations": 80,
      "sms_sent": 90,
      "emails_sent": 120,
      "appointments_set": 50,
      "notes_logged": 80,
      "tasks_completed": 80
    },
    "contact_breakdown_today": [
      {
        "contact_id": "abc123",
        "contact_name": "Jane Doe",
        "actions": [
          {"type": "call", "outcome": "no_answer", "timestamp": "2026-05-05T09:14:00-07:00"},
          {"type": "call", "outcome": "voicemail_left", "timestamp": "2026-05-05T13:22:00-07:00"},
          {"type": "sms_outbound", "preview": "Hey Jane, tried calling earlier...", "timestamp": "2026-05-05T13:25:00-07:00"},
          {"type": "note", "preview": "Left VM, sent text...", "timestamp": "2026-05-05T13:26:00-07:00"}
        ],
        "summary": "2 calls, 1 SMS, 1 note"
      },
      {
        "contact_id": "def456",
        "contact_name": "Mike Smith",
        "actions": [
          {"type": "sms_outbound", "preview": "Following up on...", "timestamp": "2026-05-05T10:01:00-07:00"},
          {"type": "sms_inbound", "preview": "Yes still interested", "timestamp": "2026-05-05T10:42:00-07:00"},
          {"type": "appointment_set", "scheduled_for": "2026-05-08T14:00:00-07:00", "timestamp": "2026-05-05T10:55:00-07:00"}
        ],
        "summary": "2-way SMS thread, appointment booked"
      }
    ]
  }
}
```

Activity counts are derived from GHL data:
- **Calls**: parse from `/conversations/search` filtered by `lastMessageType=TYPE_CALL` and `assignedTo=adrian_id`. Outcome from `lastOutboundMessageAction`.
- **SMS sent**: same source, `lastMessageType=TYPE_SMS`, direction=`outbound`
- **Emails sent**: same source, `lastMessageType=TYPE_EMAIL`, direction=`outbound`
- **Notes**: count notes where `userId=adrian_id` and `createdAt` falls in window
- **Tasks**: count tasks where `assignedTo=adrian_id` and `completedAt` falls in window
- **Appointments set**: count GHL appointments created by Adrian in window

The `contact_breakdown_today` array is the drill-down view: clicking the activity panel in the dashboard shows this list — exactly who Adrian touched, with what action, in what order, with message previews. Lets you audit his actual work, not just see counts.

---

## aging_leads

```json
{
  "aging_leads": [
    {
      "contact_id": "abc123",
      "name": "John Smith",
      "current_pipeline": "New Leads",
      "current_stage": "New Lead - Uncontacted",
      "days_in_stage": 4,
      "days_since_last_activity": 4,
      "opportunity_value_usd": 950000,
      "assigned_to": "Adrian Aboniawan",
      "last_activity": null,
      "alert_level": "critical"
    },
    ...
  ]
}
```

Alert thresholds — applied across ALL active pipelines (not just New Leads). The principle: any active lead anywhere in the system that's been forgotten gets flagged.

**Per-stage thresholds (proposed v1 — adjust after first week of real data):**

| Pipeline | Stage | Critical | Warning |
|---|---|---|---|
| New Leads | New Lead - Uncontacted | >24h no contact | 12-24h no contact |
| New Leads | Contacted - No Response | >7d no follow-up | 4-7d no follow-up |
| New Leads | Contacted - Responded | >3d no follow-up | 2-3d no follow-up |
| New Leads | Email/Text Only | >14d no human touch | 7-14d no human touch |
| Buyer Pipeline | Active Buyer | >7d no activity | 4-7d no activity |
| Buyer Pipeline | Appointment Scheduled | appointment date passed without outcome logged | appointment <48h away with no confirmation |
| Buyer Pipeline | Buyer Within 3 Months | >7d no activity | 4-7d no activity |
| Buyer Pipeline | Buyer Under 9 Months | >14d no activity | 7-14d no activity |
| Buyer Pipeline | Buyer Over 9 Months | >60d no activity | 30-60d no activity |
| Buyer Pipeline | Under Contract | >3d no activity | 1-3d no activity |
| Seller Pipeline | (mirrors Buyer Pipeline thresholds) | | |
| Investor/Flipper | Investor/Flipper | >30d no activity | 14-30d no activity |
| Past Buyers/Sellers | Looking to buy/sell | >14d no follow-up after signal | 7-14d no follow-up after signal |

**High-value override:** Any opportunity with `monetaryValue > $1,000,000` gets bumped one tier (Warning → Critical, Watch → Warning) regardless of stage. High-stakes deals shouldn't sit.

**"Watch" tier** (green dot, not red): contacts recently moved into a stage with no follow-up task yet scheduled, OR Long Term contacts showing fresh re-engagement signals.

Sorted by alert_level severity, then days_in_stage descending. Ties broken by opportunity dollar value (highest first).

### Aging-Lead Email Alerts

When refresh.py detects critical-level aging leads, it sends an email alert to Graeham + Adrian (cc):

- **Subject**: `[Pipeline Alert] {N} leads need follow-up — {oldest_days}d oldest`
- **Body**: Numbered list of critical leads with name, stage, days silent, opp value, contact link to GHL profile, suggested action ("call today", "send re-engagement SMS", "move to FOLLOW UP pipeline").
- **Frequency**: max 1x per day (don't spam — if leads still critical tomorrow, send updated digest, not a new alert per lead)
- **Throttle**: skip the email entirely if zero critical alerts (no "all clear" emails — they train people to ignore the inbox)

Email destinations come from the skill's config:
- TO: `graehamwatts@gmail.com` (Graeham)
- CC: `graehamwattsclientcare@gmail.com` (Adrian)
- Configurable via the SKILL.md or a `config.json` if the user wants more recipients later.

---

## heat_map

```json
{
  "heat_map": {
    "lead_intake": {
      "matrix": [
        [0, 0, 1, 2, 1, 0, 0, ..., 0],   // Sunday: 24 hourly bins
        [0, 0, 2, 5, 8, 6, 4, ..., 0],   // Monday
        ...
      ],
      "max_value": 12
    },
    "adrian_activity": {
      "matrix": [...],
      "max_value": 18
    }
  }
}
```

Two heat maps: when leads come INTO the system, and when Adrian is most active. Helps spot mismatches (leads pour in 6pm Monday, Adrian's busiest at 10am Tuesday — that's a leak).

---

## lead_table

Searchable, filterable, drill-down table. Every contact represented.

```json
{
  "lead_table": [
    {
      "contact_id": "abc123",
      "name": "Jane Doe",
      "email": "...",
      "phone": "...",
      "source": "Zillow",
      "current_pipeline": "Buyer Pipeline",
      "current_stage": "Active Buyer",
      "opportunity_value_usd": 1200000,
      "date_added": "2026-04-12",
      "last_activity": "2026-05-01",
      "days_silent": 3,
      "assigned_to": "Adrian Aboniawan",
      "tags": ["epa", "first-time-buyer"],
      "ghl_url": "https://app.gohighlevel.com/v2/location/.../contacts/detail/abc123"
    },
    ...
  ]
}
```

Includes EVERY active and past contact. The dashboard's table component handles search/filter/sort client-side (no backend needed).

---

## pipelines

Reference structure pulled fresh from `/opportunities/pipelines`. Used by the dashboard to render pipeline names and stage names correctly even if Graeham renames stages in GHL.

```json
{
  "pipelines": [
    {
      "id": "0GOMZ952ibDSJnq1L7Ae",
      "name": "Buyer Pipeline",
      "stages": [
        {"id": "...", "name": "Under Contract", "position": 0, "win_probability": 9.09},
        ...
      ]
    },
    ...
  ]
}
```

---

## Validation Rules (refresh.py must enforce before pushing)

1. `_meta.contact_total` matches `lead_table.length`
2. `scorecards.lifetime.new_leads` == `_meta.contact_total`
3. Sum of all sankey link values per source column ≈ count of contacts with that source (within 1% drift acceptable)
4. No contact appears in both `aging_leads.critical` and `past_client_engine` (sanity check: critical neglected leads shouldn't be already-closed past clients)
5. All opportunity_value_usd are >= 0
6. All dates are ISO 8601 with timezone

If any validation fails: write a fail-log to `outputs/validation-failures-{timestamp}.log` and STOP — don't push bad data over good data.

---

## Versioning

`schema_version` field. Bump when changing the contract. The dashboard HTML reads the version and refuses to render if it doesn't recognize it (forces visible "schema mismatch" banner instead of silent breakage).

Current: `1.0` — initial release.
