# Property OS — Transcription Service Specification

**Status:** Draft v1 — May 2026
**Owner:** Graeham Watts
**Purpose:** Spec for a transcription microservice inside Property OS so team members and end-users can drop a video URL and get a transcript back automatically. No manual paste. No browser automation. No team time spent on transcription.

---

## What this is — and what it isn't

This document is the engineering blueprint for adding transcription to Property OS as a server-side feature. It is meant to be handed to a developer (or used by Claude in a future session if Graeham provides the Property OS stack).

**What's in scope:**
- API design (the endpoints Property OS exposes)
- Worker architecture (how transcription jobs run in the background)
- Storage schema (how transcripts are kept in the DB)
- Cost model (what this will run per month at various scales)
- Choice of transcription engine and download tool
- Failure handling

**What's out of scope:**
- Property OS frontend UI design (depends on the existing app)
- Auth model (assumes Property OS already has user accounts)
- Specific deployment platform (works on AWS, Vercel, Railway, Render, etc.)

---

## The honest scope-setting

Claude in a Cowork session can build skills that run in Graeham's Cowork sandbox. Claude CANNOT magically run a transcription service inside Property OS for Graeham's team to use. The service has to be deployed by a developer (or by Claude in a future session if the codebase is connected).

**What Claude can do here:**
- Write the entire service code (Python or TypeScript) ready for deployment
- Spec the database schema and migrations
- Build a working demo runnable in a sandbox
- Document everything

**What Claude cannot do:**
- Deploy code to Property OS production infrastructure unilaterally
- Hold a long-running transcription server in a Cowork session (sessions expire)
- Maintain login state for paid services like Unmixr at scale

The fastest realistic path: Claude writes this service in a future session, Graeham's dev (or Claude with deploy access) deploys it, team uses it via Property OS UI from then on.

---

## Recommended architecture

### Tech stack choice

Two viable stacks depending on what Property OS already runs on:

**Option A — Node/TypeScript stack** (if Property OS is Next.js/Express/Nest/etc.)

- API: Next.js API route or Express endpoint
- Queue: BullMQ (Redis-backed)
- Workers: Node workers running BullMQ consumers
- Download tool: `youtube-dl-exec` (Node wrapper around yt-dlp)
- Transcription: Deepgram Node SDK
- DB: existing Property OS PostgreSQL

**Option B — Python sidecar** (if Property OS is mostly TS but transcription wants Python)

- API: FastAPI service running as a separate microservice
- Queue: Celery + Redis OR RQ + Redis
- Workers: Python workers in Docker
- Download tool: `yt-dlp` (native Python)
- Transcription: Deepgram Python SDK or local Whisper for low-tier
- DB: existing Property OS PostgreSQL accessed via SQLAlchemy or asyncpg

**My recommendation:** If Property OS is Node, go Option A — keeps it in one stack. If Property OS already has a Python service (or you want local Whisper as a backup tier without Deepgram costs), go Option B.

For most production Property OS deployments serving a team, **Option A with Deepgram-only (no local Whisper) is simpler and cheaper to operate.** Local Whisper means you need GPU-or-very-fast-CPU workers, which complicates deployment. Deepgram-only means stateless workers, simple horizontal scaling, predictable costs.

### Service topology

```
                                                  ┌──────────────────┐
                                                  │  Property OS UI  │
                                                  │  (Next.js/React) │
                                                  └────────┬─────────┘
                                                           │ POST /transcribe { url }
                                                           ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ Property OS API                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │ POST /api/transcribe                                                   │  │
│  │   1. Validate URL, check user has credit/quota                         │  │
│  │   2. Insert transcripts row (status=pending)                           │  │
│  │   3. Enqueue job in BullMQ → returns job_id + transcript_id            │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │ GET /api/transcribe/:id      → returns transcript row (status + text)  │  │
│  │ GET /api/transcribe          → list user's transcripts                 │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────┬───────────────────────────────────────────────────┘
                           │ enqueue
                           ▼
                  ┌────────────────┐
                  │   Redis        │
                  │   (BullMQ)     │
                  └────────┬───────┘
                           │ workers pick up
                           ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ Transcription worker(s) — horizontally scalable                              │
│   1. Pull job (URL + transcript_id)                                          │
│   2. yt-dlp downloads audio to /tmp                                          │
│   3. POST audio to Deepgram                                                  │
│   4. Update transcripts row (status=complete, transcript_text=...)           │
│   5. Send webhook/Pusher event to Property OS UI                             │
│   6. Optional: trigger downstream content pipeline                           │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Database schema (PostgreSQL)

```sql
CREATE TABLE transcripts (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  property_id     UUID REFERENCES properties(id) ON DELETE SET NULL,  -- optional context

  source_url      TEXT NOT NULL,
  source_platform TEXT,           -- youtube | instagram | tiktok | ...
  source_title    TEXT,           -- pulled from yt-dlp metadata
  source_uploader TEXT,           -- creator handle
  duration_sec    INTEGER,

  status          TEXT NOT NULL DEFAULT 'pending',
                  -- pending | downloading | transcribing | complete | failed
  tier            TEXT NOT NULL DEFAULT 'standard',
                  -- standard | premium

  transcript_text TEXT,
  word_count      INTEGER,

  error_message   TEXT,
  retry_count     INTEGER DEFAULT 0,

  cost_cents      INTEGER,        -- Deepgram cost for this job

  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  started_at      TIMESTAMPTZ,
  completed_at    TIMESTAMPTZ
);

CREATE INDEX idx_transcripts_user_status ON transcripts(user_id, status);
CREATE INDEX idx_transcripts_source_url ON transcripts(source_url);
CREATE INDEX idx_transcripts_status_created ON transcripts(status, created_at);

-- Optional: dedupe across the whole platform
CREATE UNIQUE INDEX idx_transcripts_dedupe ON transcripts(source_url, tier)
  WHERE status = 'complete';
```

### API surface

```typescript
// POST /api/transcribe
// Body: { url: string, tier?: 'standard' | 'premium', property_id?: string }
// Returns: { transcript_id: string, status: 'pending', estimated_seconds: number }

// GET /api/transcribe/:id
// Returns: { id, status, source_url, source_platform, source_title,
//            duration_sec, transcript_text, word_count, error_message,
//            created_at, completed_at }

// GET /api/transcribe?status=complete&limit=50
// Returns: array of transcript rows for the authenticated user

// DELETE /api/transcribe/:id
// Removes the transcript (user's own only)

// POST /api/transcribe/:id/retry
// Re-runs a failed job
```

### Frontend integration

```typescript
// In Property OS UI:
async function submitTranscription(url: string, tier: 'standard' | 'premium' = 'standard') {
  const res = await fetch('/api/transcribe', {
    method: 'POST',
    body: JSON.stringify({ url, tier }),
  });
  const { transcript_id } = await res.json();

  // Poll OR subscribe to Pusher channel for status updates
  // (Pusher recommended — Property OS likely already uses it)

  return transcript_id;
}
```

Real-time updates: use Pusher / Ably / Supabase Realtime to push status changes to the UI without polling. The worker updates the row, and a Postgres NOTIFY or a Pusher event fires the UI update.

---

## Cost model

### Deepgram Nova-3 (recommended)

- **Standard plan:** $0.0043 per minute of audio
- **Growth plan:** $0.0036 per minute (at higher volume)
- **Pre-paid bulk:** Volume discounts available — talk to sales at scale

### Real-world costs at various team scales

Assumption: average video length 5 minutes.

| Scale | Videos/month | Minutes/month | Cost/month |
|---|---|---|---|
| Solo agent | 20 | 100 | $0.43 |
| Small team (5 agents) | 100 | 500 | $2.15 |
| Property OS public beta (50 users, 20 videos each) | 1,000 | 5,000 | $21.50 |
| Property OS scale (500 users, 20 videos each) | 10,000 | 50,000 | $215 |

Deepgram costs are negligible relative to the team time saved. A single agent spending 10 min/day on manual transcription costs the business ~$50/day in opportunity cost. Deepgram saves that for cents.

### Infrastructure costs

- **Redis (Upstash or similar managed):** Free tier covers up to ~10K commands/day; ~$10/month for low-mid scale; $50-100/month at scale
- **Worker compute (Render / Railway / Fly.io background worker):** ~$10/month for a small worker; ~$50-100/month for 3-5 workers at scale
- **Storage:** Negligible — transcripts are text, ~5KB per row average

**Total estimated cost at the Property OS-scale tier:** ~$300/month all-in for transcription serving 500 active users. At small-team scale: under $20/month.

---

## yt-dlp robustness — the Instagram problem

The hard part isn't transcription. Deepgram is rock solid. The hard part is **reliably extracting audio from platforms that fight scrapers**, mainly Instagram.

**yt-dlp success rates (rough industry estimates, 2026):**

- YouTube: 98%+ (Google rarely breaks yt-dlp; even when they do, fix lands in days)
- TikTok: 95%+ (occasional rate limits)
- Vimeo: 99%+
- X / Twitter: 90% (depends on tweet visibility)
- Facebook: 85%
- **Instagram: 70-85%** (Instagram aggressively breaks yt-dlp; rate limits hit fast)

For production reliability on Instagram, **use Apify's Instagram Reel Scraper** as a fallback:

- ~$0.50 per 1000 reels
- Maintained by Apify's team — they keep up with Instagram changes
- Returns audio URL + metadata
- Hand off audio URL to Deepgram

**Hybrid strategy:**
1. Try yt-dlp first (free)
2. If it fails on Instagram, retry via Apify (paid but reliable)
3. Log every fallback so you can monitor yt-dlp reliability over time

### Worker pseudocode

```typescript
async function processTranscriptionJob(job: TranscriptionJob) {
  const { url, transcript_id, tier } = job.data;
  
  await db.update('transcripts', { id: transcript_id, status: 'downloading' });
  
  let audioPath: string;
  try {
    audioPath = await downloadWithYtDlp(url);
  } catch (err) {
    // Instagram fallback
    if (url.includes('instagram.com')) {
      audioPath = await downloadWithApify(url);
    } else {
      await markFailed(transcript_id, err);
      return;
    }
  }
  
  await db.update('transcripts', { id: transcript_id, status: 'transcribing' });
  
  let transcript: string;
  if (tier === 'premium') {
    transcript = await deepgramTranscribe(audioPath, 'nova-3');
  } else {
    transcript = await deepgramTranscribe(audioPath, 'nova-2');
    // Note: even "standard" tier uses Deepgram in this Property OS spec — local Whisper
    // is the right move for Cowork sessions but adds operational complexity in production
  }
  
  const wordCount = transcript.split(/\s+/).length;
  const costCents = Math.ceil(durationSec / 60 * 0.43); // standard rate
  
  await db.update('transcripts', {
    id: transcript_id,
    status: 'complete',
    transcript_text: transcript,
    word_count: wordCount,
    cost_cents: costCents,
    completed_at: new Date(),
  });
  
  await pusher.trigger(`user-${userId}`, 'transcript-complete', { transcript_id });
}
```

---

## Why NOT just use Cowork sessions for the team

Graeham's instinct is the right one — building this into Property OS server-side is better than having every team member run Cowork sessions. Reasons:

1. **Cowork sessions are interactive.** They're great for Graeham working on content, not great for "the system does it while I sleep."
2. **Session state is per-user.** Each team member would need their own Cowork session, their own credentials, their own setup.
3. **Sessions time out.** A team member starts a transcription, walks away, comes back to a closed session.
4. **No shared transcript history.** Cowork sessions don't share state — Property OS DB shares state across the team naturally.
5. **No automation.** Property OS can trigger transcription on events (new lead, new listing, scheduled batch). Cowork only fires when a human is there.

Production transcription = backend service. End of story.

---

## Suggested implementation order

If Graeham wants this built (in a future Cowork session or by his dev), here's the order:

1. **Week 1 — Foundation**
   - Set up Redis + BullMQ
   - Implement the `POST /api/transcribe` endpoint
   - Create the `transcripts` DB table + migrations
   - Stub worker that just downloads and logs (no transcription yet)

2. **Week 2 — Core transcription**
   - Integrate Deepgram SDK in the worker
   - Implement yt-dlp download
   - Wire up status updates (Pusher or polling)
   - Build the minimal UI: "Drop URL → see transcript when done"

3. **Week 3 — Reliability & polish**
   - Add Apify fallback for Instagram
   - Build retry logic for failed jobs
   - Add cost tracking + per-user quotas
   - Add transcript search in Property OS

4. **Week 4 — Integration with content pipeline**
   - Wire completed transcripts into Property OS content workflow
   - Add bulk-import (drop 10 URLs, get 10 transcripts)
   - Add scheduled batch jobs (transcribe a creator's whole feed weekly)

Total: roughly 4 weeks of focused dev work for a small team, or ~2 weeks if it's the dev's primary focus.

---

## Open questions for Graeham

Before building, decide:

1. **What stack is Property OS on?** Node/TypeScript or Python? This determines Option A vs Option B.
2. **What's the hosting platform?** Vercel, AWS, Railway, Render, Fly.io? Each has different worker support.
3. **Who pays for Deepgram — Property OS or end-user?** Per-user quotas? Per-team plans?
4. **Do you want speaker diarization?** ("Who said what" in podcasts.) If yes, AssemblyAI is better than Deepgram. Costs a bit more.
5. **Do you want this to feed into Graeham's existing content pipeline automatically?** E.g., transcript completes → auto-runs through `transcript-repurposer` logic → content draft saved.

Once those are answered, the build is straightforward.

---

## Bottom line

Build the service. Don't try to automate Unmixr or scale Cowork sessions for the team. Deepgram + yt-dlp + a simple worker is the right architecture, costs almost nothing at small scale, and runs hands-off forever.

The transcription module in `_shared/transcription/transcribe.py` is the reference implementation. The Property OS version is the same logic, deployed as a server-side service with a queue.
