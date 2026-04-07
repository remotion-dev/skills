# Flag Criteria, Behavioral Buckets & Scoring Reference

This document defines the complete audit framework: behavioral buckets, flag overlay system, priority scoring formula, Pipeline Health Score calculation, Pipeline Mismatch Detection rules, and edge cases.

Read this file before generating any audit report. The SKILL.md summarizes these rules, but this file is the authoritative source for thresholds, scoring weights, and edge case handling.

---

## Table of Contents

1. [Behavioral Buckets (5-Bucket System)](#1-behavioral-buckets)
2. [Flag Overlay System (Critical / Warning / Watch)](#2-flag-overlay-system)
3. [Pipeline Mismatch Detection](#3-pipeline-mismatch-detection)
4. [Priority Scoring Formula](#4-priority-scoring-formula)
5. [Pipeline Health Score Calculation](#5-pipeline-health-score-calculation)
6. [Adrian's Task List Prioritization](#6-adrians-task-list-prioritization)
7. [Edge Cases & Special Rules](#7-edge-cases--special-rules)
8. [Bucket-to-Pipeline Mapping](#8-bucket-to-pipeline-mapping)

---

## 1. Behavioral Buckets

Every contact is assigned to exactly ONE bucket based on their most recent **meaningful** activity. The bucket determines the baseline urgency and expected follow-up cadence.

### What counts as "meaningful activity"

Meaningful activity is any engagement that indicates the contact is alive and reachable. This includes:

**Inbound (strongest signal):**
- Replied to a message (SMS, email, chat)
- Submitted a form or survey
- Booked or requested an appointment
- Saved a property on IDX / portal
- Logged into a property search portal
- Called or texted the agent/team directly
- Clicked a link in an email or SMS

**Outbound (human only):**
- Agent/team member sent a personal message (not automated)
- Agent/team member left a voicemail
- Agent/team member added a manual note documenting a conversation
- Agent/team member completed a task related to this contact

**What does NOT count as meaningful activity:**
- Automated workflow emails sent (these are system touches, not engagement)
- Automated SMS from drip campaigns with no reply
- System-generated notes (e.g., "Contact added to workflow")
- Tags being applied or removed by automation
- Pipeline stage changes made by automation (not human)

### Bucket Definitions

| Bucket | Timeframe | Description | Expected Follow-up Cadence |
|--------|-----------|-------------|---------------------------|
| **HOT** | 0-7 days | Active engagement within the last 7 days. This contact is in-market and responsive right now. | Every 1-2 days. These contacts should have a task assigned for the next touch within 48 hours at most. |
| **WARM** | 8-30 days | Activity within 8-30 days. Still engaged but momentum is slowing. Without re-engagement, they'll drift to FOLLOW UP. | Every 3-5 days. Should have at least one meaningful touch per week. |
| **FOLLOW UP** | 31-90 days | No meaningful activity in 31-90 days. They haven't opted out but they've gone quiet. Needs a re-engagement attempt. | Every 7-14 days. At least two touch attempts per month. These contacts need creative re-engagement — not just "checking in." |
| **LONG TERM** | 91+ days | No meaningful activity in 91+ days. Still a valid contact (not DND, not bounced) but not actively in-market. Worth periodic touchpoints but not urgent. | Monthly at most. Add to a long-term drip workflow. Quarterly personal check-in. |
| **DEAD** | N/A | Contact has opted out (DND status), hard-bounced on all channels (email + phone), or explicitly stated they are not interested with no subsequent re-engagement. | None. Do not contact. Review quarterly to see if DND was removed or if they re-engaged through another channel. |

### Bucket Assignment Rules

1. Use the **most recent meaningful activity date** to determine the bucket.
2. If a contact has BOTH inbound and outbound activity, use whichever is more recent.
3. If a contact has NO meaningful activity ever (zero notes, zero messages, zero appointments), assign based on date added to CRM and apply CRITICAL flag.
4. DND status immediately overrides to DEAD, regardless of activity recency.
5. If the only activity is automated workflow touches, treat the contact as if they have no activity — use the date of the last human touch or last inbound engagement.

---

## 2. Flag Overlay System

Flags are an urgency overlay on top of buckets. A HOT contact can be flagged CRITICAL (e.g., hot lead with no task assigned). A LONG TERM contact can be flagged WATCH (e.g., showing early re-engagement signals). Flags highlight what needs attention RIGHT NOW, while buckets describe the contact's overall engagement state.

### CRITICAL (Red) — Immediate Action Required

A contact gets a CRITICAL flag if ANY of the following are true:

| # | Condition | Why It Matters |
|---|-----------|---------------|
| C1 | Zero notes ever AND zero outbound contact attempts | This contact was added to the CRM and completely forgotten. |
| C2 | Not enrolled in any workflow AND no outbound in last 14 days | No automated nurture AND no human follow-up — they're getting zero attention. |
| C3 | Last outbound was 10+ days ago with no response and no follow-up scheduled | The ball was dropped. Someone reached out, got no reply, and never followed up. |
| C4 | HOT bucket contact with no task assigned for next step | Your hottest leads need a next action. No task = no plan. |
| C5 | Open opportunity (any dollar value) with no follow-up in 5+ days | Money is on the table and nobody's tending to it. |
| C6 | Appointment no-showed and no follow-up within 48 hours | They didn't show up and nobody reached out to reschedule. |
| C7 | Inbound message received with no response in 48+ hours | They reached out to YOU and got ignored. |

### WARNING (Yellow) — Needs Attention This Week

A contact gets a WARNING flag if ANY of the following are true (and they don't already qualify for CRITICAL):

| # | Condition | Why It Matters |
|---|-----------|---------------|
| W1 | Open task 3+ days overdue | Someone committed to a next step and hasn't done it. |
| W2 | No pipeline stage assigned | The contact exists in a void — not being tracked through any process. |
| W3 | Last outbound was 5-9 days ago with no follow-up | Approaching the danger zone. One more week and this becomes Critical. |
| W4 | Added 5+ days ago with no appointment ever booked | They entered the CRM but the goal (booking an appointment) hasn't been pursued. |
| W5 | WARM bucket contact with no re-engagement action planned | They're cooling off and there's no plan to re-engage before they go cold. |
| W6 | Pipeline mismatch: cold behavior in hot pipeline stage | Pipeline says active, behavior says otherwise. Needs review. |
| W7 | Has notes but no task assigned for next step | Previous conversations happened but nobody scheduled the follow-through. |

### WATCH (Green) — Monitor / Low Urgency

A contact gets a WATCH flag if ANY of the following are true (and they don't qualify for CRITICAL or WARNING):

| # | Condition | Why It Matters |
|---|-----------|---------------|
| G1 | Added 2-4 days ago with no appointment yet | Still within reasonable window but worth tracking. |
| G2 | Enrolled in active workflow but no human outreach logged | Automation is covering them but no personal touch yet. |
| G3 | LONG TERM contact showing early re-engagement signals | They clicked an email, visited the portal, or did something after months of silence. Could be coming back to market. |
| G4 | Pipeline mismatch: hot behavior in cold/nurture pipeline | Behavior suggests they should be upgraded but the pipeline hasn't caught up yet. Worth flagging for review, not urgent. |

### Flag Priority

If a contact qualifies for multiple flag levels, use the highest: CRITICAL > WARNING > WATCH.

---

## 3. Pipeline Mismatch Detection

A pipeline mismatch occurs when a contact's behavioral bucket (based on actual activity data) disagrees with their GHL pipeline stage (which is often set manually or by old automations and may be stale).

### Mismatch Types

**Type 1: Hot Behavior / Cold Pipeline (⚡ — Most Urgent)**
- Behavioral bucket: HOT or WARM
- Pipeline stage: Any nurture, long-term, drip, or inactive stage
- Evidence required: At least one meaningful inbound activity in the bucket's timeframe
- Callout format: `⚡ PIPELINE MISMATCH — This contact is in your '[Stage Name]' pipeline but shows [BUCKET] behavioral activity ([specific evidence]). The GHL label may be outdated.`
- Example: `⚡ PIPELINE MISMATCH — This contact is in your 'Long Term Nurture' pipeline but shows HOT behavioral activity (3 IDX property saves, inbound message 2 days ago). The GHL label may be outdated.`

**Type 2: No Pipeline / Active Behavior (⚡ — Urgent)**
- Behavioral bucket: HOT or WARM
- Pipeline stage: None (not assigned to any pipeline)
- Evidence required: Recent meaningful activity
- Callout format: `⚡ PIPELINE MISMATCH — This contact has recent activity ([evidence]) but isn't assigned to any pipeline. They need to be placed.`

**Type 3: Cold Behavior / Hot Pipeline (⚠️ — Needs Review)**
- Behavioral bucket: FOLLOW UP, LONG TERM, or DEAD
- Pipeline stage: Any "active," "hot," "ready," "engaged," or similar active stage
- Evidence required: No meaningful activity in 30+ days
- Callout format: `⚠️ PIPELINE MISMATCH — This contact is in your '[Stage Name]' pipeline but has had no activity in [X] days. Consider moving to [recommended stage].`
- Example: `⚠️ PIPELINE MISMATCH — This contact is in your 'Active Buyer' pipeline but has had no activity in 47 days. Consider moving to FOLLOW UP.`

**Type 4: Dead Behavior / Active Pipeline (🚫 — Cleanup)**
- Behavioral bucket: DEAD
- Pipeline stage: Any active or nurture stage (anything that implies outreach will continue)
- Evidence required: DND status or bounced on all channels
- Callout format: `🚫 PIPELINE MISMATCH — This contact is DND/bounced but still in '[Stage Name]'. Remove from active pipeline.`

### Mismatch Detection Rules

1. **Map pipeline stages to expected buckets.** Since every GHL account uses different pipeline names, you need to infer the intent of each stage name. See Section 8 for the mapping logic.

2. **A mismatch exists when the expected bucket for the pipeline stage is 2+ levels away from the actual bucket.** The severity ladder is: HOT → WARM → FOLLOW UP → LONG TERM → DEAD. Being one level off (e.g., WARM contact in a HOT pipeline) is minor and doesn't get flagged. Being two or more levels off (e.g., FOLLOW UP contact in a HOT pipeline) is a mismatch.

3. **No pipeline = always a mismatch if the contact is HOT or WARM.** Any active contact should be tracked in a pipeline.

4. **DEAD contacts in ANY active pipeline are always a mismatch.** No exceptions.

5. **When in doubt, flag it.** It's better to surface a borderline mismatch for human review than to miss a lead stuck in the wrong pipeline.

---

## 4. Priority Scoring Formula

Every contact gets a priority score from 0-100. This determines their position in the Today's Top 10 and the order of Adrian's Task List.

### Score Components

| Component | Max Points | Calculation |
|-----------|-----------|-------------|
| **Recency** | 30 | Based on days since last meaningful activity. 0 days = 30 pts. 1-3 days = 25 pts. 4-7 days = 20 pts. 8-14 days = 15 pts. 15-30 days = 10 pts. 31-60 days = 5 pts. 61-90 days = 2 pts. 91+ days = 0 pts. |
| **Opportunity Value** | 25 | $0 = 0 pts. $1-$99K = 5 pts. $100K-$299K = 10 pts. $300K-$499K = 15 pts. $500K-$749K = 20 pts. $750K+ = 25 pts. Only open opportunities count. |
| **Flag Severity** | 20 | CRITICAL = 20 pts. WARNING = 10 pts. WATCH = 5 pts. No flag = 0 pts. |
| **Pipeline Mismatch** | 15 | Type 1 (Hot/Cold) = 15 pts. Type 2 (No Pipeline) = 12 pts. Type 3 (Cold/Hot) = 8 pts. Type 4 (Dead/Active) = 5 pts. No mismatch = 0 pts. |
| **Engagement Trajectory** | 10 | Moving up (FOLLOW UP→WARM or WARM→HOT) = 10 pts. Stable = 5 pts. Moving down (HOT→WARM or WARM→FOLLOW UP) = 8 pts (declining is urgent too). Stable LONG TERM or DEAD = 0 pts. |

### Total Score
Sum all components. Maximum possible: 100.

### Tiebreaker
If two contacts have the same score, break ties by:
1. Higher flag severity wins
2. Higher opportunity value wins
3. More recent activity wins
4. Earlier date added to CRM wins (older contact = more overdue)

---

## 5. Pipeline Health Score Calculation

The Pipeline Health Score is a single number (0-100) that represents overall CRM hygiene. It's a quick way for the user to see "how healthy is my database?" at a glance.

### Components

| Component | Weight | What It Measures | Scoring |
|-----------|--------|-----------------|---------|
| **Pipeline Coverage** | 20% | % of contacts assigned to a pipeline | 100% coverage = 20 pts. Linear scale down. |
| **Note Freshness** | 20% | % of non-DEAD contacts with a note in last 30 days | 100% = 20 pts. Linear scale down. |
| **Task/Workflow Coverage** | 20% | % of non-DEAD contacts with an active task or workflow enrollment | 100% = 20 pts. Linear scale down. |
| **Pipeline Accuracy** | 20% | % of contacts whose pipeline stage matches their behavioral bucket (inverse of mismatch rate) | 0% mismatches = 20 pts. Each mismatch reduces proportionally. |
| **Follow-up Timeliness** | 20% | % of contacts with follow-up scheduled within appropriate cadence for their bucket | HOT contacts followed up within 48h, WARM within 7 days, etc. 100% on-cadence = 20 pts. |

### Total Score
Sum all components. Maximum: 100.

### Letter Grade
- **A (90-100):** Excellent. CRM is well-maintained, contacts are tracked, follow-ups are timely.
- **B (80-89):** Good. Minor gaps but overall healthy.
- **C (70-79):** Fair. Noticeable gaps in follow-up or pipeline tracking.
- **D (60-69):** Poor. Significant number of neglected contacts or stale pipelines.
- **F (Below 60):** Critical. The CRM needs major attention. Many contacts are being missed.

---

## 6. Adrian's Task List Prioritization

Adrian is the team coordinator. The task list is organized so Adrian can work through it top to bottom without needing to make judgment calls about what's most important.

### Task Priority Order

1. **Tier 1 — Today's Top 10 actions** (highest priority score contacts)
   - Each task includes: contact name, phone number, specific action, context for why
   - Example: "Call Sarah Chen at (408) 555-7890 — HOT lead, saved 3 properties in Los Gatos yesterday, no one has called her yet. Reference the Elm Street listing she saved."

2. **Tier 2 — Remaining Critical contacts**
   - Same format as Tier 1 but these didn't make the Top 10
   - Grouped by flag reason (all "no notes ever" together, all "dropped follow-up" together)

3. **Tier 3 — Warning contacts with overdue tasks**
   - Focus on the specific overdue action
   - Example: "Complete overdue task for Mike Rodriguez — was due 4 days ago: 'Send market update for Willow Glen area'"

4. **Tier 4 — Pipeline mismatch fixes**
   - Specific pipeline move instructions
   - Example: "Move James Park from 'Long Term Nurture' → 'Active Buyer' pipeline — he saved 5 properties this week and messaged Graeham 3 days ago"

5. **Tier 5 — Data hygiene**
   - Missing pipeline assignments to resolve
   - Contacts with no tags to categorize
   - Possible duplicates to review
   - Stale workflow enrollments to clean up

### Task Format

Every task follows this template:
```
[Priority #] [Action verb] [Contact name] at [phone/email] — [Context: what happened, what's needed, why it matters]. [Specific instruction: what to say, what to reference, what to schedule.]
```

Never write vague tasks like "Follow up with John" or "Check on this contact." Every task must be specific enough that Adrian can execute it without asking Graeham for clarification.

---

## 7. Edge Cases & Special Rules

### New Contacts (Added < 48 hours ago)
- Do not flag as CRITICAL regardless of note count
- Assign to HOT bucket if they came in via form submission, appointment request, or inbound message
- Assign to WATCH if they were manually added or imported with no inbound activity
- Flag as WARNING only if they submitted an urgent form (e.g., "I want to sell my house") and no one has responded in 24+ hours

### Contacts with ONLY Automated Activity
- If the only outbound is automated workflows (no human notes, no manual messages), treat them as if they have no outbound activity for flag purposes
- Exception: If the contact has replied to an automated message, that reply counts as meaningful inbound activity

### Contacts in Multiple Pipelines
- Use the pipeline stage that was most recently updated
- If they're in both an "Active Buyer" and "Seller Listing" pipeline, check both — a mismatch on either one gets flagged

### Opportunity with No Contact Record Details
- If an opportunity exists but the contact has no phone AND no email, flag as CRITICAL with note: "Open opportunity but no contact method on file — verify contact details"

### DND Contacts with Recent Inbound Activity
- If a contact is DND but sent an inbound message after the DND was set, flag as CRITICAL: "Contact is DND but reached out on [date] — their DND may need to be reviewed"
- Do NOT auto-remove DND. Just flag it for human review.

### Contacts with Very High Activity
- If a contact has 10+ meaningful activities in the last 7 days, they're HOT but may also need a "high engagement" note so the team knows this is someone who's very active right now
- Add a note in their Top 10 entry: "🔥 High engagement — [X] activities in last 7 days"

### Team-Assigned Contacts
- If tasks or notes show a specific team member's name, include that in Adrian's task list: "This contact has been worked by [team member name] — coordinate with them before reassigning"

---

## 8. Bucket-to-Pipeline Mapping

Since every GHL account uses different pipeline and stage names, the mismatch detection system needs to infer intent from stage names. Here's the mapping logic:

### Pipeline Stages That Imply HOT/WARM (Active)
Keywords to look for: "active," "hot," "engaged," "ready," "qualified," "appointment set," "showing," "under contract," "offer," "negotiating," "closing"

Expected bucket: HOT or WARM. Flag a mismatch if actual bucket is FOLLOW UP, LONG TERM, or DEAD.

### Pipeline Stages That Imply FOLLOW UP
Keywords: "follow up," "follow-up," "callback," "retry," "re-engage," "attempted," "no answer"

Expected bucket: WARM or FOLLOW UP. Flag a mismatch if actual bucket is HOT (they're more active than the pipeline suggests) or LONG TERM/DEAD (they're less active).

### Pipeline Stages That Imply LONG TERM / Nurture
Keywords: "nurture," "long term," "long-term," "drip," "future," "not ready," "6 months," "next year," "sphere," "past client"

Expected bucket: FOLLOW UP or LONG TERM. Flag a mismatch if actual bucket is HOT or WARM.

### Pipeline Stages That Imply DEAD / Closed
Keywords: "dead," "lost," "closed lost," "unqualified," "do not contact," "junk," "spam," "wrong number"

Expected bucket: DEAD. Flag a mismatch if actual bucket is anything else AND the contact has recent activity.

### No Pipeline Assigned
Expected: Only acceptable for LONG TERM or DEAD contacts. Any HOT or WARM contact without a pipeline is always a mismatch. FOLLOW UP contacts without a pipeline get a WARNING flag.

### When Stage Names Are Ambiguous
If you can't confidently map a stage name to an expected bucket, don't guess — note the ambiguity in the report and suggest the user clarify what that stage means in their workflow. Better to ask than to generate false mismatches.
