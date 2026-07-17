#!/usr/bin/env python3
"""
scrape.py — Instagram competitor + hashtag scraper for Graeham Watts.

Pulls top-engagement posts from Instagram by hashtag and/or by competitor handle
via Apify. Returns clean, ranked metadata. Optionally pipes results into
video-to-obsidian to log them in the vault.

Usage:
    python3 scrape.py --hashtags bayarearealestate,peninsulahomes --top 25
    python3 scrape.py --handles competitor1,competitor2 --days 14 --top 20
    python3 scrape.py --hashtags bayarearealestate --top 10 --pipe-to-obsidian
    python3 scrape.py --hashtags bayarearealestate --top 10 --json --save

Reads APIFY_API_TOKEN from Documents/Skills LLMS/Claude/Skills/.env

Requires:
    pip install python-dotenv apify-client --break-system-packages

URL is a required field on every returned post. Results without a URL are
dropped — Instagram is a visual medium and unreachable notes are dead data.
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    print("ERROR: python-dotenv missing. Run: pip install python-dotenv --break-system-packages", file=sys.stderr)
    sys.exit(1)

try:
    from apify_client import ApifyClient
except ImportError:
    print("ERROR: apify-client missing. Run: pip install apify-client --break-system-packages", file=sys.stderr)
    sys.exit(1)

SKILLS_ROOT = Path(__file__).resolve().parents[3]
ENV_PATH = SKILLS_ROOT / ".env"
load_dotenv(ENV_PATH)

APIFY_TOKEN = os.environ.get("APIFY_API_TOKEN")
if not APIFY_TOKEN:
    print(f"ERROR: APIFY_API_TOKEN not found in {ENV_PATH}", file=sys.stderr)
    sys.exit(1)

# apify/instagram-scraper is the unified actor — handles both profile URLs and
# hashtag URLs in a single call. Returns POSTS (not profile metadata).
SCRAPER_ACTOR = "apify/instagram-scraper"

DEFAULT_HASHTAG_LIMIT = 50
DEFAULT_PROFILE_LIMIT = 50


def _run_scraper(client, urls, limit, label):
    run_input = {
        "directUrls": [u["url"] for u in urls],
        "resultsType": "posts",
        "resultsLimit": limit,
        "addParentData": False,
    }
    try:
        run = client.actor(SCRAPER_ACTOR).call(run_input=run_input)
        items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
        url_to_origin = {u["url"]: u["origin"] for u in urls}
        for it in items:
            origin = it.get("inputUrl") and url_to_origin.get(it["inputUrl"])
            it["_discovered_via"] = origin or label
        print(f"[scrape] {label} -> {len(items)} items", file=sys.stderr)
        return items
    except Exception as e:
        print(f"[scrape] FAILED for {label}: {e}", file=sys.stderr)
        return []


def scrape_hashtag(client, hashtag, limit=DEFAULT_HASHTAG_LIMIT):
    clean = hashtag.lstrip("#")
    url = f"https://www.instagram.com/explore/tags/{clean}/"
    print(f"[hashtag] Scraping #{clean} (limit {limit})...", file=sys.stderr)
    return _run_scraper(client, [{"url": url, "origin": f"hashtag:{clean}"}], limit, f"#{clean}")


def scrape_profile(client, handle, limit=DEFAULT_PROFILE_LIMIT):
    clean = handle.lstrip("@")
    url = f"https://www.instagram.com/{clean}/"
    print(f"[profile] Scraping @{clean} (limit {limit})...", file=sys.stderr)
    return _run_scraper(client, [{"url": url, "origin": f"handle:@{clean}"}], limit, f"@{clean}")


def normalize_post(item):
    url = item.get("url") or item.get("permalink") or item.get("postUrl")
    if not url:
        return None
    likes = item.get("likesCount") or item.get("likes") or 0
    comments = item.get("commentsCount") or item.get("comments") or 0
    views = item.get("videoViewCount") or item.get("videoPlayCount") or item.get("views") or 0
    er = round((likes + comments) / views * 100, 2) if views and views > 0 else 0.0
    post_type = "reel"
    if item.get("type") == "Image" or item.get("productType") == "feed":
        post_type = "static"
    elif item.get("type") == "Sidecar" or item.get("productType") == "carousel_container":
        post_type = "carousel"
    timestamp_raw = item.get("timestamp") or item.get("takenAt")
    post_date = None
    if timestamp_raw:
        try:
            if isinstance(timestamp_raw, (int, float)):
                post_date = datetime.fromtimestamp(timestamp_raw, tz=timezone.utc).strftime("%Y-%m-%d")
            else:
                post_date = str(timestamp_raw)[:10]
        except Exception:
            post_date = None
    return {
        "url": url,
        "creator": "@" + (item.get("ownerUsername") or item.get("username") or "unknown"),
        "creator_followers": item.get("ownerFollowersCount") or item.get("followersCount") or 0,
        "post_type": post_type,
        "post_date": post_date,
        "caption": (item.get("caption") or "")[:500],
        "duration_sec": int(item.get("videoDuration") or 0),
        "engagement": {
            "views": views,
            "likes": likes,
            "comments": comments,
            "saves": None,
            "engagement_rate": er,
        },
        "discovered_via": item.get("_discovered_via", "unknown"),
    }


def filter_recent(posts, days):
    cutoff = datetime.now(timezone.utc).date() - timedelta(days=days)
    out = []
    for p in posts:
        if not p["post_date"]:
            out.append(p)
            continue
        try:
            d = datetime.strptime(p["post_date"], "%Y-%m-%d").date()
            if d >= cutoff:
                out.append(p)
        except ValueError:
            out.append(p)
    return out


def rank_and_top(posts, top_n):
    posts.sort(key=lambda p: (p["engagement"]["engagement_rate"], p["engagement"]["views"]), reverse=True)
    return posts[:top_n]


def pipe_to_obsidian(posts):
    v2o_script = SKILLS_ROOT / "skills" / "video-to-obsidian" / "scripts" / "log_to_vault.py"
    if not v2o_script.exists():
        print(f"[pipe] video-to-obsidian not found at {v2o_script}", file=sys.stderr)
        return 0
    success = 0
    for p in posts:
        cmd = [sys.executable, str(v2o_script), p["url"], "--metadata-json", json.dumps(p)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            success += 1
        else:
            print(f"[pipe] FAILED for {p['url']}: {result.stderr[:200]}", file=sys.stderr)
    return success


def main():
    parser = argparse.ArgumentParser(description="Instagram competitor + hashtag scraper")
    parser.add_argument("--hashtags", default="")
    parser.add_argument("--handles", default="")
    parser.add_argument("--top", type=int, default=20)
    parser.add_argument("--days", type=int, default=30)
    parser.add_argument("--limit-per-target", type=int, default=DEFAULT_HASHTAG_LIMIT)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--save", action="store_true")
    parser.add_argument("--pipe-to-obsidian", action="store_true")
    args = parser.parse_args()

    hashtags = [h.strip() for h in args.hashtags.split(",") if h.strip()]
    handles = [h.strip() for h in args.handles.split(",") if h.strip()]
    if not hashtags and not handles:
        print("ERROR: provide --hashtags or --handles (or both)", file=sys.stderr)
        sys.exit(1)

    client = ApifyClient(APIFY_TOKEN)
    raw = []
    for tag in hashtags:
        raw.extend(scrape_hashtag(client, tag, args.limit_per_target))
    for handle in handles:
        raw.extend(scrape_profile(client, handle, args.limit_per_target))

    normalized = []
    dropped_no_url = 0
    for item in raw:
        n = normalize_post(item)
        if n:
            normalized.append(n)
        else:
            dropped_no_url += 1
    if dropped_no_url:
        print(f"[normalize] Dropped {dropped_no_url} items with no URL", file=sys.stderr)

    seen = set()
    deduped = []
    for p in normalized:
        if p["url"] not in seen:
            seen.add(p["url"])
            deduped.append(p)

    recent = filter_recent(deduped, args.days)
    print(f"[summary] {len(raw)} raw -> {len(normalized)} normalized -> {len(deduped)} unique -> {len(recent)} within {args.days} days", file=sys.stderr)
    top = rank_and_top(recent, args.top)

    if args.save:
        out_dir = Path("outputs/scrapes")
        out_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        out_path = out_dir / f"scrape-{ts}.json"
        out_path.write_text(json.dumps(top, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[save] {out_path}", file=sys.stderr)

    if args.json:
        print(json.dumps(top, indent=2, ensure_ascii=False))
    else:
        print(f"\nTop {len(top)} posts by engagement rate:\n")
        for i, p in enumerate(top, 1):
            e = p["engagement"]
            print(f"{i:>2}. {p['creator']:<25} ER {e['engagement_rate']:>5.2f}%  views {e['views']:>8,}  likes {e['likes']:>6,}  ({p['post_date']})")
            print(f"    {p['url']}")
            print(f"    discovered via: {p['discovered_via']}")
            print()

    if args.pipe_to_obsidian:
        print(f"\n[pipe] Logging {len(top)} posts to Obsidian vault...", file=sys.stderr)
        n = pipe_to_obsidian(top)
        print(f"[pipe] {n}/{len(top)} written to vault", file=sys.stderr)


if __name__ == "__main__":
    main()
