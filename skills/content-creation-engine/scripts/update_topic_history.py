#!/usr/bin/env python3
"""Append a shipped weekly calendar's topics to references/topic-history.json.

Closes the gap where topic-history was documented as "written by content-calendar"
but nothing actually wrote it — so the Phase 3 freshness penalty could never fire.

Usage:
    python update_topic_history.py --calendar outputs/calendar-data/calendar-2026-06-15.json
    python update_topic_history.py            (auto-picks the newest calendar JSON)

Idempotent: if the calendar's week_of is already in history, it is replaced, not duplicated.
Prunes history entries older than max_weeks (from the JSON's own _schema, default 4).
"""
import argparse, glob, json, os, re, sys
from datetime import datetime, timedelta

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HISTORY_PATH = os.path.join(SKILL_DIR, "references", "topic-history.json")
CALENDAR_GLOB = os.path.join(SKILL_DIR, "outputs", "calendar-data", "calendar-*.json")

TOPIC_LIST_KEYS = ("topics", "selected_topics", "calendar", "week_topics", "items")


def newest_calendar():
    files = sorted(glob.glob(CALENDAR_GLOB))
    if not files:
        sys.exit(f"No calendar JSON found at {CALENDAR_GLOB} — pass --calendar explicitly.")
    return files[-1]


def extract_topics(cal):
    if isinstance(cal, list):
        return cal
    for k in TOPIC_LIST_KEYS:
        if isinstance(cal.get(k), list):
            return cal[k]
    sys.exit(f"Could not find a topic list in calendar JSON (tried keys {TOPIC_LIST_KEYS}).")


def normalize(t):
    """Map a calendar topic onto the topic-history v2.0 entry shape, keeping unknowns."""
    return {
        "title": t.get("title") or t.get("topic") or t.get("name") or "",
        "angle": t.get("angle") or t.get("angle_slug") or None,
        "pillar": t.get("pillar"),
        "pillar_name": t.get("pillar_name"),
        "funnel": t.get("funnel") or t.get("funnel_stage"),
        "market": t.get("market"),
        "neighborhood": t.get("neighborhood"),
        "ghl_keyword": t.get("ghl_keyword") or t.get("keyword"),
        "slug": t.get("slug") or re.sub(r"[^a-z0-9]+", "-", (t.get("title") or "").lower()).strip("-")[:80],
        "scheduled_date": t.get("scheduled_date") or t.get("date"),
        "time_decay_band": t.get("time_decay_band"),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--calendar", help="Path to calendar-YYYY-MM-DD.json (default: newest in outputs/calendar-data/)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    cal_path = args.calendar or newest_calendar()
    m = re.search(r"(\d{4}-\d{2}-\d{2})", os.path.basename(cal_path))
    week_of = m.group(1) if m else datetime.now().strftime("%Y-%m-%d")

    with open(cal_path, encoding="utf-8") as f:
        cal = json.load(f)
    topics = [normalize(t) for t in extract_topics(cal)]
    topics = [t for t in topics if t["title"]]

    with open(HISTORY_PATH, encoding="utf-8") as f:
        hist = json.load(f)

    max_weeks = int(hist.get("_schema", {}).get("max_weeks", 4))
    entry = {
        "week_of": week_of,
        "generated_date": datetime.now().strftime("%Y-%m-%d"),
        "topics": topics,
    }
    # replace same week if present, else append
    hist["history"] = [h for h in hist.get("history", []) if h.get("week_of") != week_of]
    hist["history"].append(entry)
    # prune anything older than max_weeks
    cutoff = datetime.now() - timedelta(weeks=max_weeks)
    def fresh(h):
        try:
            return datetime.strptime(h["week_of"], "%Y-%m-%d") >= cutoff
        except Exception:
            return True
    before = len(hist["history"])
    hist["history"] = sorted([h for h in hist["history"] if fresh(h)], key=lambda h: h["week_of"])
    pruned = before - len(hist["history"])

    print(f"week_of={week_of}  topics={len(topics)}  pruned_old_weeks={pruned}  history_weeks={len(hist['history'])}")
    if args.dry_run:
        print("(dry run — not written)")
        return
    with open(HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(hist, f, indent=2, ensure_ascii=False)
    print(f"Wrote {HISTORY_PATH}")


if __name__ == "__main__":
    main()
