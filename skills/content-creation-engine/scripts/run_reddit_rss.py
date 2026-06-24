#!/usr/bin/env python3
"""
run_reddit_rss.py
-----------------
FREE, no-API-key, no-Apify Reddit ingestion for the content-ideation-engine.

This is the drop-in alternative to run_reddit_ideation.py (which uses the paid
Apify scraper). It pulls Reddit's public endpoints directly:

  * Default mode: the public ``.json`` endpoints, which carry the engagement
    fields the ideation rubric needs (ups, num_comments, created_utc, selftext).
  * ``--rss`` mode: the public ``.rss`` feeds, for lightweight discovery
    (title, link, author, published) when JSON is rate-limited.

Output is normalized to the SAME schema run_reddit_ideation.py produces from
Apify (title / url / communityName / body / upVotes / numberOfComments /
createdAt / dataType), so anything downstream that parses the Apify dataset
parses this too. No code changes needed downstream.

Standard library only — no ``pip install``.

Why this exists: the Reddit "official Data API" support ticket is the wrong door
(commercial/enterprise gate, ~$12k/month minimum) and keeps auto-denying a
low-volume use case. The free public endpoints below need no approval. See
``references/reddit-rss-source.md`` for the full write-up.

Usage:
    python run_reddit_rss.py --tier 1                       # 5 core subs, .json
    python run_reddit_rss.py --tier 2 --min-upvotes 50      # +Peninsula, filter
    python run_reddit_rss.py --tier 1 --sort top --time week
    python run_reddit_rss.py --tier 1 --rss                 # RSS discovery mode
    python run_reddit_rss.py --tier 1 --dry-run             # print URLs only

Etiquette baked in: a descriptive User-Agent and a polite delay between
requests. Unauthenticated reads are rate-limited; run from a residential IP
(datacenter IPs are the ones Reddit 403s).
"""

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

# A real, descriptive User-Agent is REQUIRED — generic agents get blocked.
# Format: <platform>:<app-id>:<version> (by /u/<reddit_username>)
USER_AGENT = "script:propcast_research:v1.0 (by /u/graehamwatts)"

# ---------------------------------------------------------------
# Subreddit tiers (mirror of references/.../subreddit-list.md), each with the
# sort strategy that file specifies. (sub, sort)
# ---------------------------------------------------------------

TIER_1 = [
    ("BayArea", "hot"),
    ("bayarearealestate", "new"),
    ("RealEstate", "hot"),
    ("FirstTimeHomeBuyer", "new"),
    ("Layoffs", "hot"),
]

TIER_2_ADDS = [
    ("PaloAlto", "new"),
    ("MenloPark", "new"),
    ("RedwoodCity", "new"),
    ("SanMateo", "new"),
    ("Burlingame", "new"),
    ("SanCarlos", "new"),
    ("Belmont", "new"),
    ("FosterCity", "new"),
    ("HalfMoonBay", "new"),
    ("DalyCity", "new"),
]

TIER_3_ADDS = [
    ("MountainView", "hot"),
    ("Sunnyvale", "hot"),
    ("Cupertino", "hot"),
    ("SantaClara", "hot"),
    ("SanJose", "hot"),
    ("RealEstateInvesting", "hot"),
]

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = REPO_ROOT / "outputs"
OUTPUTS_DIR.mkdir(exist_ok=True)


def subs_for_tier(tier: int):
    subs = list(TIER_1)
    if tier >= 2:
        subs += TIER_2_ADDS
    if tier >= 3:
        subs += TIER_3_ADDS
    return subs


def _request(url: str, timeout: float = 20.0, retries: int = 2, backoff: float = 12.0):
    """GET with a descriptive UA. On HTTP 429, honor Retry-After (or back off) and retry."""
    last_err = None
    for attempt in range(retries + 1):
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except urllib.error.HTTPError as e:
            last_err = e
            if e.code == 429 and attempt < retries:
                retry_after = e.headers.get("Retry-After")
                wait = float(retry_after) if (retry_after and retry_after.isdigit()) else backoff * (attempt + 1)
                time.sleep(wait)
                continue
            raise
    raise last_err


def json_url(sub: str, sort: str, limit: int, time_window: str) -> str:
    url = f"https://www.reddit.com/r/{sub}/{sort}.json?limit={limit}&raw_json=1"
    if sort == "top":
        url += f"&t={time_window}"
    return url


def rss_url(sub: str, sort: str, time_window: str) -> str:
    url = f"https://www.reddit.com/r/{sub}/{sort}/.rss"
    if sort == "top":
        url += f"?t={time_window}"
    return url


def iso_from_epoch(epoch) -> str:
    try:
        return datetime.fromtimestamp(float(epoch), tz=timezone.utc).isoformat()
    except (TypeError, ValueError):
        return ""


def normalize_json_post(d: dict) -> dict:
    """Map a Reddit .json post to the Apify-compatible schema used downstream."""
    return {
        "id": "t3_" + d.get("id", ""),
        "url": "https://www.reddit.com" + d.get("permalink", ""),
        "username": d.get("author", ""),
        "title": d.get("title", ""),
        "communityName": "r/" + d.get("subreddit", ""),
        "body": d.get("selftext", ""),
        "numberOfComments": d.get("num_comments", 0),
        "upVotes": d.get("ups", 0),
        "createdAt": iso_from_epoch(d.get("created_utc")),
        "dataType": "post",
        "source": "reddit-json-free",
    }


def fetch_json(sub, sort, limit, time_window, min_upvotes, max_age_days):
    raw = _request(json_url(sub, sort, limit, time_window))
    data = json.loads(raw.decode("utf-8"))
    now = datetime.now(tz=timezone.utc)
    out = []
    for child in data.get("data", {}).get("children", []):
        if child.get("kind") != "t3":
            continue
        d = child.get("data", {})
        if d.get("ups", 0) < min_upvotes:
            continue
        if max_age_days is not None:
            created = d.get("created_utc")
            if created:
                age_days = (now - datetime.fromtimestamp(float(created), tz=timezone.utc)).days
                if age_days > max_age_days:
                    continue
        out.append(normalize_json_post(d))
    return out


# Atom namespace used by Reddit's .rss feeds
_ATOM = "{http://www.w3.org/2005/Atom}"


def fetch_rss(sub, sort, time_window):
    raw = _request(rss_url(sub, sort, time_window))
    root = ET.fromstring(raw)
    out = []
    for entry in root.findall(f"{_ATOM}entry"):
        title_el = entry.find(f"{_ATOM}title")
        link_el = entry.find(f"{_ATOM}link")
        author_el = entry.find(f"{_ATOM}author/{_ATOM}name")
        updated_el = entry.find(f"{_ATOM}updated")
        out.append({
            "id": (entry.findtext(f"{_ATOM}id") or ""),
            "url": (link_el.get("href") if link_el is not None else ""),
            "username": (author_el.text if author_el is not None else ""),
            "title": (title_el.text if title_el is not None else ""),
            "communityName": f"r/{sub}",
            "body": "",  # RSS gives an HTML content blob, not structured fields
            "numberOfComments": None,  # not exposed in RSS
            "upVotes": None,           # not exposed in RSS
            "createdAt": (updated_el.text if updated_el is not None else ""),
            "dataType": "post",
            "source": "reddit-rss-free",
        })
    return out


def main():
    ap = argparse.ArgumentParser(description="Free Reddit ingestion (public .json / .rss) for the content engine.")
    ap.add_argument("--tier", type=int, choices=[1, 2, 3], required=True,
                    help="1=core (5 subs), 2=+Peninsula (15), 3=+South Bay (21)")
    ap.add_argument("--sort", choices=["hot", "new", "top"], default=None,
                    help="Override the per-subreddit default sort.")
    ap.add_argument("--time", dest="time_window", default="week",
                    help="Window for --sort top (hour/day/week/month/year/all). Default: week.")
    ap.add_argument("--limit", type=int, default=25, help="Posts per subreddit (default 25).")
    ap.add_argument("--delay", type=float, default=6.0,
                    help="Seconds between subreddit requests. Reddit RSS rate-limits hard; default 6.")
    ap.add_argument("--min-upvotes", type=int, default=0, help="Drop posts below this upvote count (.json only).")
    ap.add_argument("--max-age-days", type=int, default=None, help="Drop posts older than N days (.json only).")
    ap.add_argument("--rss", action="store_true", help="Use the .rss feeds (discovery) instead of .json.")
    ap.add_argument("--dry-run", action="store_true", help="Print the URLs that would be fetched, then exit.")
    args = ap.parse_args()

    subs = subs_for_tier(args.tier)

    if args.dry_run:
        for sub, default_sort in subs:
            sort = args.sort or default_sort
            url = rss_url(sub, sort, args.time_window) if args.rss else json_url(sub, sort, args.limit, args.time_window)
            print(url)
        print(f"\n[dry-run] {len(subs)} subreddits, mode={'rss' if args.rss else 'json'}, UA={USER_AGENT!r}")
        return

    all_items, blocked = [], []
    for sub, default_sort in subs:
        sort = args.sort or default_sort
        try:
            if args.rss:
                items = fetch_rss(sub, sort, args.time_window)
            else:
                items = fetch_json(sub, sort, args.limit, args.time_window,
                                   args.min_upvotes, args.max_age_days)
            all_items.extend(items)
            print(f"[ok]   r/{sub:<22} {sort:<4} -> {len(items)} posts")
        except urllib.error.HTTPError as e:
            blocked.append((sub, e.code))
            print(f"[warn] r/{sub:<22} {sort:<4} -> HTTP {e.code} (rate-limit/IP block; back off or use --rss)")
        except urllib.error.URLError as e:
            blocked.append((sub, str(e.reason)))
            print(f"[warn] r/{sub:<22} {sort:<4} -> {e.reason}")
        time.sleep(args.delay)  # polite delay; Reddit RSS rate-limits hard

    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    mode = "rss" if args.rss else "json"
    out_path = OUTPUTS_DIR / f"ideation-raw-{mode}-tier{args.tier}-{ts}.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(all_items, f, indent=2, ensure_ascii=False)

    print(f"\n[*] {len(all_items)} posts from {len(subs) - len(blocked)}/{len(subs)} subs -> {out_path}")
    if blocked:
        print(f"[*] {len(blocked)} subs blocked/failed: {[b[0] for b in blocked]}")
        print("    If many are blocked you are likely on a datacenter IP. Run from a residential IP, "
              "slow the rate, or fall back to the Apify scraper (run_reddit_ideation.py).")


if __name__ == "__main__":
    main()
