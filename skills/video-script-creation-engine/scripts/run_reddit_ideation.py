#!/usr/bin/env python3
"""
run_reddit_ideation.py
-----------------------
Thin wrapper around Apify's trudax/reddit-scraper-lite actor for the
Bay Area Content Engine's content-ideation-engine skill.

Usage:
    python run_reddit_ideation.py --tier 1           # Tier 1 only (5 subs, ~$0.26)
    python run_reddit_ideation.py --tier 2           # Tier 1+2 (15 subs, ~$0.77)
    python run_reddit_ideation.py --tier 3           # Full run (20+ subs, ~$1.36)
    python run_reddit_ideation.py --template layoff  # Keyword search template
    python run_reddit_ideation.py --dry-run          # Print input, don't run

Reads APIFY_API_TOKEN from ../.env (via python-dotenv).

Writes raw dataset to ../outputs/ideation-raw-{timestamp}.json

Requires:
    pip install python-dotenv apify-client --break-system-packages
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    print("ERROR: python-dotenv not installed. Run: pip install python-dotenv --break-system-packages")
    sys.exit(1)

try:
    from apify_client import ApifyClient
except ImportError:
    print("ERROR: apify-client not installed. Run: pip install apify-client --break-system-packages")
    sys.exit(1)


# ---------------------------------------------------------------
# Subreddit tiers (mirror of references/subreddit-list.md)
# ---------------------------------------------------------------

TIER_1 = [
    "https://www.reddit.com/r/BayArea/hot/",
    "https://www.reddit.com/r/bayarearealestate/new/",
    "https://www.reddit.com/r/RealEstate/hot/",
    "https://www.reddit.com/r/FirstTimeHomeBuyer/new/",
    "https://www.reddit.com/r/Layoffs/hot/",
]

TIER_2_ADDS = [
    "https://www.reddit.com/r/PaloAlto/new/",
    "https://www.reddit.com/r/MenloPark/new/",
    "https://www.reddit.com/r/RedwoodCity/new/",
    "https://www.reddit.com/r/SanMateo/new/",
    "https://www.reddit.com/r/Burlingame/new/",
    "https://www.reddit.com/r/SanCarlos/new/",
    "https://www.reddit.com/r/Belmont/new/",
    "https://www.reddit.com/r/FosterCity/new/",
    "https://www.reddit.com/r/HalfMoonBay/new/",
    "https://www.reddit.com/r/DalyCity/new/",
]

TIER_3_ADDS = [
    "https://www.reddit.com/r/MountainView/hot/",
    "https://www.reddit.com/r/Sunnyvale/hot/",
    "https://www.reddit.com/r/Cupertino/hot/",
    "https://www.reddit.com/r/SantaClara/hot/",
    "https://www.reddit.com/r/SanJose/hot/",
    "https://www.reddit.com/r/RealEstateInvesting/hot/",
]

# ---------------------------------------------------------------
# Keyword search templates (mirror of references/query-templates.md)
# ---------------------------------------------------------------

TEMPLATES = {
    "layoff": [
        "Meta layoff sell house Bay Area",
        "Google layoff selling home Peninsula",
        "Apple severance real estate California",
        "tech layoff downsizing Bay Area",
    ],
    "first-time-buyer": [
        "first time buyer Bay Area",
        "first time homebuyer Peninsula",
        "buying first house East Palo Alto",
        "first house Redwood City",
    ],
    "ab1482": [
        "AB 1482 Bay Area",
        "AB 1482 California landlord",
        "rent control California 1482",
    ],
    "relocation": [
        "moving to Bay Area from",
        "relocating Peninsula jobs",
        "moving to Palo Alto",
        "moving to Redwood City",
        "moving to Menlo Park",
    ],
    "life-events": [
        "inherited house California sell",
        "inherited property Bay Area probate",
        "divorce house California",
        "downsizing empty nest Bay Area",
    ],
    "investment": [
        "Bay Area rental property investment",
        "buying rental EPA",
        "ADU East Palo Alto",
        "cash flow property California Peninsula",
    ],
    "market-timing": [
        "Bay Area housing market 2026",
        "Peninsula home prices dropping",
        "should I sell Bay Area",
        "should I buy Bay Area now",
    ],
}

# ---------------------------------------------------------------
# Paths
# ---------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = REPO_ROOT / ".env"
OUTPUTS_DIR = REPO_ROOT / "outputs"
OUTPUTS_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------------------
# Main
# ---------------------------------------------------------------

def build_proxy_config(economy: bool) -> dict:
    """
    Build the proxy config block for the Apify actor.

    Default (production): RESIDENTIAL proxy group. Reddit rarely blocks
    residential IPs, so reliability jumps from ~60% to ~95%+. Costs a bit
    more in proxy bandwidth on top of the per-result fee.

    --economy: fall back to the default datacenter proxy (cheaper, but
    Reddit frequently 403s datacenter IPs and you'll get partial results).
    Use only for dry tests or quick checks.
    """
    if economy:
        return {"useApifyProxy": True}
    return {
        "useApifyProxy": True,
        "apifyProxyGroups": ["RESIDENTIAL"],
    }


def build_input_from_tier(tier: int, max_items: int, economy: bool = False) -> dict:
    """Build Apify input using subreddit URLs for the requested tier."""
    urls = list(TIER_1)
    if tier >= 2:
        urls += TIER_2_ADDS
    if tier >= 3:
        urls += TIER_3_ADDS

    return {
        "startUrls": [{"url": u} for u in urls],
        "searches": [],
        "maxItems": max_items,
        "maxPostCount": 15,
        "maxComments": 3,
        "maxCommunitiesCount": 0,
        "maxUserCount": 0,
        "sort": "hot",
        "time": "week",
        "scrollTimeout": 40,
        "skipUserPosts": True,
        "includeNSFW": False,
        "proxy": build_proxy_config(economy),
        "debugMode": False,
    }


def build_input_from_template(template: str, max_items: int, economy: bool = False) -> dict:
    """Build Apify input from a keyword search template."""
    if template not in TEMPLATES:
        raise ValueError(
            f"Unknown template '{template}'. Available: {list(TEMPLATES.keys())}"
        )

    return {
        "startUrls": [],
        "searches": TEMPLATES[template],
        "maxItems": max_items,
        "maxPostCount": 10,
        "maxComments": 3,
        "type": "post",
        "sort": "new",
        "time": "month",
        "scrollTimeout": 40,
        "skipUserPosts": True,
        "includeNSFW": False,
        "proxy": build_proxy_config(economy),
        "debugMode": False,
    }


def estimate_cost(max_items: int) -> float:
    """Reddit Scraper Lite is $3.40 per 1,000 results stored."""
    return round((max_items / 1000) * 3.40, 2)


def load_token() -> str:
    if not ENV_PATH.exists():
        print(f"ERROR: .env file not found at {ENV_PATH}")
        print("Copy .env.template to .env and fill in your APIFY_API_TOKEN.")
        sys.exit(1)

    load_dotenv(ENV_PATH)
    token = os.environ.get("APIFY_API_TOKEN", "").strip().strip('"')

    if not token:
        print("ERROR: APIFY_API_TOKEN is blank in .env")
        sys.exit(1)

    return token


def run_scrape(actor_input: dict, token: str) -> list[dict]:
    """Run the Apify actor and return the dataset items."""
    client = ApifyClient(token)
    actor_id = "trudax/reddit-scraper-lite"

    print(f"[*] Calling actor {actor_id}...")
    run = client.actor(actor_id).call(run_input=actor_input)

    if not run or "defaultDatasetId" not in run:
        print("ERROR: Actor run failed to return a dataset ID")
        print(f"Run response: {run}")
        sys.exit(1)

    print(f"[*] Run finished. Dataset ID: {run['defaultDatasetId']}")
    print("[*] Fetching dataset items...")

    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
    print(f"[*] Fetched {len(items)} items")
    return items


def save_dataset(items: list[dict], tier_or_template: str) -> Path:
    """Save the raw dataset to outputs/ideation-raw-{timestamp}.json"""
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"ideation-raw-{tier_or_template}-{ts}.json"
    out_path = OUTPUTS_DIR / filename

    with out_path.open("w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)

    print(f"[*] Saved dataset to {out_path}")
    return out_path


def main():
    parser = argparse.ArgumentParser(
        description="Run Reddit ideation scrape via Apify for the Bay Area Content Engine"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--tier",
        type=int,
        choices=[1, 2, 3],
        help="Subreddit tier: 1=core (5 subs), 2=+Peninsula (15), 3=+South Bay (20+)",
    )
    group.add_argument(
        "--template",
        type=str,
        choices=list(TEMPLATES.keys()),
        help="Keyword search template (overrides --tier)",
    )
    parser.add_argument(
        "--max-items",
        type=int,
        default=None,
        help="Override maxItems cap (defaults: tier1=75, tier2=225, tier3=400, template=50)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the actor input without running the scrape",
    )
    parser.add_argument(
        "--economy",
        action="store_true",
        help="Use datacenter proxy (cheaper but ~60%% reliable). Default is RESIDENTIAL (~95%%+).",
    )
    args = parser.parse_args()

    # Determine maxItems
    if args.max_items is not None:
        max_items = args.max_items
    elif args.template:
        max_items = 50
    elif args.tier == 1:
        max_items = 75
    elif args.tier == 2:
        max_items = 225
    else:  # tier 3
        max_items = 400

    # Build input
    if args.template:
        actor_input = build_input_from_template(args.template, max_items, args.economy)
        label = f"template-{args.template}"
    else:
        actor_input = build_input_from_tier(args.tier, max_items, args.economy)
        label = f"tier-{args.tier}"

    # Cost check
    cost = estimate_cost(max_items)
    proxy_mode = "DATACENTER (economy)" if args.economy else "RESIDENTIAL (production)"
    p