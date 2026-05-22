#!/usr/bin/env python3
"""
main-dashboard-builder.py — CANONICAL Rule 15-compliant builder for the weekly Main Dashboard.

This is the locked structure (v6) generated 2026-05-14 after 6 iterations.
Reference commit: https://github.com/Graehamwatts/online-content/commit/e505fcc78cccdccf84e40ffef203997b6102ce9d

═══════════════════════════════════════════════════════════════════════════════
STRUCTURE (Rule 15 — see ../../content-creation-engine/references/weekly-calendar-rules.md)
═══════════════════════════════════════════════════════════════════════════════

1. Hero banner — H1 "Main Dashboard — Week of {date range}", funnel mix subtitle, meta chips
2. Sticky audience nav — 5 tabs in this exact order:
   - Research (microscope icon)
   - Diagram (chart icon)
   - Calendar (calendar icon) ← DEFAULT TAB on page load
   - Video Content (camera icon)
   - Blog Content (memo icon)
3. v7.3 Run-Note banner (data-pull anomalies)
4. RESEARCH section:
   - Live Data Layer (5-6 source cards, green/red status)
   - Performance Signal — DUAL CHARTS (always visible):
     * IG Reach chart (gold border) with Period toggle: 7d/30d/90d/All
     * YT Engagement chart (red border) with Metric toggle (Views/Likes/Comments/Posts) + Period toggle
   - YT Top 5 table with Shorts/Long-form split summary
   - IG Top 5 with embedded thumbnails (click → opens the IG reel)
   - Freshness Constraints box
   - Source Citations list
5. DIAGRAM section:
   - 10-step pipeline diagram (4 data inputs / 3 intelligence / 3 outputs)
   - Each node clickable → modal with TL;DR + technical detail
   - INTERLAY MATRIX showing how each data input feeds each intelligence step
6. CALENDAR section:
   - 5-day grid (Mon-Fri), click any day → modal expansion
   - Mix-bar with explainer paragraph above
7. VIDEO CONTENT section:
   - Per-topic cards with 2 copy-to-clipboard buttons (BOTH paste into Claude.ai):
     • "Copy Script + Voice Prompt (Claude.ai)" — Claude verifies figures, writes the
       word-for-word SCRIPT FIRST (range language, no stale hard numbers), THEN outputs the
       matching ElevenLabs SSML to paste into ElevenLabs v3. (data key: prod_script)
     • "Copy Production Assets (Claude.ai)" — Editing Notes, AI Video Prompts, caption +
       hashtags, GHL CTA, Fair Housing scan. Explicitly does NOT write the script. (key: prod_video)
   - RULE: the script must be reachable from the dashboard. The Script+Voice button is what
     delivers it. Never ship a video card whose only script form is raw SSML.
8. BLOG CONTENT section:
   - Per-topic cards with 2 copy-to-clipboard buttons:
     • "Copy Blog Brief (Search Atlas)" — context for SEO platform
     • "Copy Production Prompt (Claude.ai)" — full blog generation prompt with schema
9. Footer — DRE# 01466876, repo links

═══════════════════════════════════════════════════════════════════════════════
REQUIRED BUG FIXES (every build — DO NOT REMOVE)
═══════════════════════════════════════════════════════════════════════════════

1. Modal CSS specificity fix:
       .modal-backdrop[hidden] { display: none !important; }
   Without this, .modal-backdrop { display: flex } overrides [hidden] attribute
   and modal pops up empty on page load.

2. STEP_DATA as Python dict + json.dumps(ensure_ascii=True):
       step_data_json = json.dumps(STEP_DATA, ensure_ascii=True)
   NEVER regex-edit JSON strings — escaped quotes break .*? matching.

3. HTML entities for all special characters:
       — → &mdash;        – → &ndash;       ’ → &rsquo;
       " → &ldquo;/&rdquo;  · → &middot;     & → &amp;
   No literal special chars in Python source — prevents multi-layer UTF-8 mojibake.

═══════════════════════════════════════════════════════════════════════════════
COMPOSIO DATA-FETCHING PATTERN (run before generating HTML)
═══════════════════════════════════════════════════════════════════════════════

# 1. Instagram profile snapshot
INSTAGRAM_GET_USER_INFO(account='instagram_carton-palama', ig_user_id='me')
  → followers_count, follows_count, media_count, biography, website

# 2. Instagram recent posts with thumbnails
INSTAGRAM_GET_IG_USER_MEDIA(
    account='instagram_carton-palama',
    ig_user_id='27735776322678984',
    limit=20,
    fields='id,caption,media_type,media_product_type,media_url,thumbnail_url,permalink,timestamp,comments_count,like_count'
)
  → Use thumbnail_url for embedded preview images.

# 3. Instagram daily reach insights (90 days)
INSTAGRAM_GET_USER_INSIGHTS(
    account='instagram_carton-palama',
    ig_user_id='me',
    metric=['reach', 'follower_count'],
    period='day',
    since='YYYY-MM-DD',  # 90 days ago
    until='YYYY-MM-DD'   # today
)
  NOTE: accounts_engaged + total_interactions return empty (deprecated Jan 2025).
  IG engagement-over-time can only be derived from per-post like+comment aggregation.

# 4. YouTube channel snapshot
YOUTUBE_GET_CHANNEL_STATISTICS(
    account='youtube_manor-maki',
    id='UCFHqB0L2C4aJVksMKkg_ukw',
    part='statistics,snippet'
)

# 5. YouTube recent video IDs (paginate)
YOUTUBE_LIST_CHANNEL_VIDEOS(
    account='youtube_manor-maki',
    channelId='UCFHqB0L2C4aJVksMKkg_ukw',
    maxResults=50,
    part='snippet'
)
  Repeat with pageToken from response for older videos.

# 6. YouTube batch statistics (max 50 IDs per call)
YOUTUBE_GET_VIDEO_DETAILS_BATCH(
    account='youtube_manor-maki',
    id=[<list of 50 IDs>],
    parts=['snippet', 'statistics', 'contentDetails']
)
  → Parse statistics.viewCount/likeCount/commentCount per video.
  → Parse contentDetails.duration (ISO-8601 PT<M>M<S>S format).
  → Section 9 Shorts filter: duration_seconds <= 60.
  → Aggregate by ISO week for the chart time-series.

═══════════════════════════════════════════════════════════════════════════════
TO REGENERATE FOR NEXT WEEK
═══════════════════════════════════════════════════════════════════════════════

The actual HTML builder logic for week-of 2026-05-11 is preserved in:
  commit e505fcc78cccdccf84e40ffef203997b6102ce9d (online-content repo)
  /dashboards/weekly-calendars/2026-05-11-production-calendar.html

To build next Monday's dashboard:
  1. Run the Composio fetches above with updated date ranges
  2. Update TOPICS list (5 entries: day, date, funnel, title, hook, criteria, impact, ease,
     ghl, pillar, market, why_targeted, video_summary, blog_summary, data_trail)
  3. Update STEP_DATA modals with this week's actual analytics numbers
  4. Update YT_DAILY, YT_WEEKLY, IG_DAILY, IG_WEEKLY with fresh time-series
  5. Copy v6 HTML skeleton from reference commit; swap in new data
  6. Validate: assert mojibake-free, DRE correct, all 5 tabs present, modals parse
  7. Push to online-content via Composio GITHUB_COMMIT_MULTIPLE_FILES OR
     GitHub Contents API direct (for files >40KB)
  8. Append week to topic-history.json (skills repo) via Composio

═══════════════════════════════════════════════════════════════════════════════
WHAT NOT TO BUILD
═══════════════════════════════════════════════════════════════════════════════

- NO companion cards linking to sibling sub-dashboards (Videos / Blogs / Research / All-in-One)
- NO sibling sub-dashboard files (deleted in commit 63d6fa9, 2026-05-14)
- NO channel toggle on the chart — both IG and YT must be ALWAYS visible (v5 had this bug)
- NO "Production Calendar" or "Weekly Calendar" page title — it's "Main Dashboard"

═══════════════════════════════════════════════════════════════════════════════
DRE# CORRECTNESS
═══════════════════════════════════════════════════════════════════════════════

ALWAYS:     DRE# 01466876
NEVER:      DRE# 01466876  (corrected in skills repo on 2026-05-14)

═══════════════════════════════════════════════════════════════════════════════
"""

print("# Canonical Rule 15 builder reference.")
print("# To regenerate: see commit e505fcc78cccdccf84e40ffef203997b6102ce9d")
print("# in Graehamwatts/online-content repo, file:")
print("#   dashboards/weekly-calendars/2026-05-11-production-calendar.html")
print("# Update only the data inputs (TOPICS, STEP_DATA, chart series).")
print("# Do not modify the HTML skeleton, CSS, or JS toggle logic.")
