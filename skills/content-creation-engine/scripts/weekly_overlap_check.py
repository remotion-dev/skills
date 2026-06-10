#!/usr/bin/env python3
"""Week-over-week topic overlap check — the mandatory pre-push gate that was
documented in SKILL.md but never implemented.

Compares the current week's calendar against topic-history.json (all retained
weeks, history + in_production registers). Flags exact slug matches, same-angle
repeats, and fuzzy title overlap (>=0.6 token Jaccard).

Usage:
    python weekly_overlap_check.py --calendar outputs/calendar-data/calendar-2026-06-15.json
    python weekly_overlap_check.py            (auto-picks the newest calendar JSON)

Exit codes: 0 = clean, 1 = overlaps found (treat as a blocking review), 2 = error.
Prints a markdown report to stdout — paste it into the calendar review.
"""
import argparse, glob, json, os, re, sys

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HISTORY_PATH = os.path.join(SKILL_DIR, "references", "topic-history.json")
CALENDAR_GLOB = os.path.join(SKILL_DIR, "outputs", "calendar-data", "calendar-*.json")
TOPIC_LIST_KEYS = ("topics", "selected_topics", "calendar", "week_topics", "items")
STOPWORDS = {"the", "a", "an", "and", "or", "in", "on", "for", "of", "to", "is", "are",
             "your", "you", "what", "why", "how", "this", "that", "here", "heres", "its",
             "2024", "2025", "2026", "2027"}
FUZZY_THRESHOLD = 0.6


def tokens(title):
    return {w for w in re.findall(r"[a-z0-9]+", title.lower()) if w not in STOPWORDS and len(w) > 2}


def jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def extract_topics(cal):
    if isinstance(cal, list):
        return cal
    for k in TOPIC_LIST_KEYS:
        if isinstance(cal.get(k), list):
            return cal[k]
    sys.exit(2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--calendar", help="Current week's calendar JSON (default: newest)")
    args = ap.parse_args()

    files = sorted(glob.glob(CALENDAR_GLOB))
    cal_path = args.calendar or (files[-1] if files else None)
    if not cal_path:
        print("ERROR: no calendar JSON found and none passed.", file=sys.stderr)
        sys.exit(2)

    with open(cal_path, encoding="utf-8") as f:
        current = extract_topics(json.load(f))
    with open(HISTORY_PATH, encoding="utf-8") as f:
        hist = json.load(f)

    prior = []
    for week in hist.get("history", []):
        for t in week.get("topics", []):
            prior.append((week.get("week_of", "?"), "history", t))
    for t in hist.get("in_production", []):
        prior.append((t.get("week_of", "?"), "in_production", t))

    overlaps = []
    for ct in current:
        c_title = ct.get("title") or ct.get("topic") or ""
        c_slug = (ct.get("slug") or "").lower()
        c_angle = (ct.get("angle") or "").lower()
        c_tok = tokens(c_title)
        for week_of, register, pt in prior:
            p_title = pt.get("title", "")
            reasons = []
            if c_slug and c_slug == (pt.get("slug") or "").lower():
                reasons.append("identical slug")
            if c_angle and c_angle == (pt.get("angle") or "").lower():
                reasons.append("same angle")
            sim = jaccard(c_tok, tokens(p_title))
            if sim >= FUZZY_THRESHOLD:
                reasons.append(f"title similarity {sim:.2f}")
            if reasons:
                overlaps.append((c_title, p_title, week_of, register, ", ".join(reasons)))

    print(f"## Week-over-Week Overlap Check — {os.path.basename(cal_path)}")
    print(f"Current topics: {len(current)} · Prior topics compared: {len(prior)} "
          f"(history + in_production, {len(hist.get('history', []))} retained weeks)\n")
    if not overlaps:
        print("**CLEAN — no overlaps detected.**")
        sys.exit(0)
    print(f"**{len(overlaps)} OVERLAP(S) FOUND — review before pushing:**\n")
    print("| Current topic | Conflicts with | Week | Register | Why |")
    print("|---|---|---|---|---|")
    for c, p, w, r, why in overlaps:
        print(f"| {c[:60]} | {p[:60]} | {w} | {r} | {why} |")
    print("\nPer SKILL.md rules: replace the overlapping topic OR justify it as a "
          "genuinely new angle in the calendar notes.")
    sys.exit(1)


if __name__ == "__main__":
    main()
