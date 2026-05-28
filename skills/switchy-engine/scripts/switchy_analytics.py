#!/usr/bin/env python3
"""
switchy_analytics.py  —  switchy-engine skill core script
==========================================================
Pulls per-link click/scan analytics from the Switchy GraphQL API and turns them
into a retargeting decision table:

    scans/clicks per link  ->  usable retargeting audience  ->  ad budget the
    audience actually justifies (frequency x CPM model).

WHY THIS EXISTS
---------------
Switchy fires Meta/Google/etc. pixels on its redirect layer. Every click on a
Switchy short link (or QR scan -> redirect) drops the visitor into a pixel-based
custom audience BEFORE the destination page even loads. This script reads how big
those audiences are getting per source, so Graeham can decide where to spend.

SECURITY MODEL (read this)
--------------------------
- The token is API-key style and scoped to ONE workspace. Treat it like a password.
- It is NEVER hardcoded and NEVER committed. Resolution order:
      1. env var  SWITCHY_API_TOKEN
      2. file     ~/.switchy/token            (chmod 600; gitignored)
      3. file     ./.switchy_token            (gitignored; local dev only)
- If none found, the script runs in DEMO mode with illustrative numbers so the
  output format is reviewable before the live token is active.

API FACTS (confirmed from developers.switchy.io, May 2026)
----------------------------------------------------------
- Endpoint:  https://graphql.switchy.io/v1/graphql   (POST)
- Header:    Api-Authorization: <token>
- Queries only on GraphQL; link creation is REST (api.switchy.io/v1/links/create).
- Schema is Hasura-style (where:{field:{_is_null:true}} filter syntax).
- Public docs only document workspace-level fields (workspaces, domains). The
  per-link CLICK/SCAN count field name is NOT documented and MUST be confirmed
  by introspection on the live token. See confirm_schema() below — run it first.
"""

import os
import sys
import json
import csv
import argparse
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

GRAPHQL_ENDPOINT = "https://graphql.switchy.io/v1/graphql"

# ---------------------------------------------------------------------------
# Tunable economic assumptions for the budget model. Override on the CLI.
# These are deliberately conservative Bay Area / Peninsula real-estate defaults.
# ---------------------------------------------------------------------------
DEFAULTS = {
    "cpm": 22.0,            # $ per 1,000 impressions, local + interest retargeting
    "frequency": 10,        # desired impressions per audience member / 30-day window
    "min_audience": 100,    # Meta hard floor to even target a custom audience
    "efficient_audience": 1000,  # below this, retargeting is usually inefficient
    "pixel_match_rate": 0.55,    # share of clicks that resolve to a targetable user
    "window_days": 30,
}


# ---------------------------------------------------------------------------
# Token handling
# ---------------------------------------------------------------------------
def resolve_token():
    """Return (token, source) or (None, None). Never prints the token."""
    tok = os.environ.get("SWITCHY_API_TOKEN")
    if tok:
        return tok.strip(), "env:SWITCHY_API_TOKEN"
    for p in (Path.home() / ".switchy" / "token", Path(".switchy_token")):
        try:
            if p.exists():
                return p.read_text(encoding="utf-8").strip(), f"file:{p}"
        except OSError:
            pass
    return None, None


# ---------------------------------------------------------------------------
# GraphQL transport
# ---------------------------------------------------------------------------
def gql(query, token, variables=None):
    body = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
    req = urllib.request.Request(
        GRAPHQL_ENDPOINT,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Api-Authorization": token,  # NB: Switchy uses this, NOT "Authorization: Bearer"
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            payload = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise SystemExit(f"[HTTP {e.code}] {e.read().decode('utf-8', 'ignore')[:500]}")
    except urllib.error.URLError as e:
        raise SystemExit(f"[network] {e.reason}")
    if "errors" in payload:
        raise SystemExit("[graphql errors] " + json.dumps(payload["errors"], indent=2))
    return payload["data"]


# ---------------------------------------------------------------------------
# STEP 1 — Schema confirmation. RUN THIS FIRST on a live token.
# ---------------------------------------------------------------------------
INTROSPECT_LINKS = """
query ConfirmLinksType {
  __type(name: "links") {
    name
    fields { name description type { name kind ofType { name kind } } }
  }
}
"""

def confirm_schema(token):
    """
    Prints the real field names on the `links` type so we can lock the click/scan
    field. The public docs DON'T give us this, so this step is mandatory before
    trusting the analytics query below.
    """
    data = gql(INTROSPECT_LINKS, token)
    t = data.get("__type")
    if not t:
        print("No `links` type found. The top-level type may be named differently "
              "(try `link`, `Links`, or run the full __schema introspection). "
              "See references/schema-introspection.md.")
        return
    print(f"Type `{t['name']}` fields:")
    for f in t["fields"]:
        ty = f["type"]
        tyname = ty.get("name") or (ty.get("ofType") or {}).get("name") or ty.get("kind")
        print(f"  - {f['name']:<28} {tyname}")
    print("\nLook for a click/scan count field (e.g. clicks, clicksCount, "
          "visits, statistics, *_aggregate) and set --click-field accordingly.")


# ---------------------------------------------------------------------------
# STEP 2 — Per-link analytics query.
#
# Two candidate shapes are provided because the exact field name is schema-gated.
# Hasura almost always exposes EITHER a scalar count on the row OR a related
# aggregate. Pick the one confirm_schema() reveals. Default tries the scalar.
# ---------------------------------------------------------------------------
def build_links_query(click_field):
    # Scalar-count shape (most common when Switchy denormalizes the counter).
    return f"""
query LinkAnalytics {{
  links(order_by: {{clicks: desc}}) {{
    id
    domain
    url
    title
    tags
    {click_field}
  }}
}}
"""

AGGREGATE_QUERY = """
query LinkAnalyticsAggregate {
  links(order_by: {clicks: desc}) {
    id
    domain
    url
    title
    tags
    clicks_aggregate { aggregate { count } }
  }
}
"""

def fetch_links(token, click_field):
    try:
        data = gql(build_links_query(click_field), token)
        rows = data["links"]
        return [_norm(r, click_field) for r in rows]
    except SystemExit:
        # Fall back to the aggregate relationship shape.
        sys.stderr.write(f"[info] scalar field '{click_field}' failed, trying clicks_aggregate...\n")
        data = gql(AGGREGATE_QUERY, token)
        out = []
        for r in data["links"]:
            r = dict(r)
            r["_clicks"] = (((r.pop("clicks_aggregate", {}) or {}).get("aggregate") or {}).get("count")) or 0
            out.append(_norm(r, "_clicks"))
        return out


def _norm(r, click_field):
    slug = r.get("id") or "?"
    domain = r.get("domain") or "hi.switchy.io"
    return {
        "short": f"{domain}/{slug}",
        "title": r.get("title") or "",
        "tags": ",".join(r.get("tags") or []),
        "destination": r.get("url") or "",
        "clicks": int(r.get(click_field) or 0),
    }


# ---------------------------------------------------------------------------
# STEP 3 — Audience + budget math
# ---------------------------------------------------------------------------
def audience_and_budget(clicks, cfg):
    """clicks -> targetable audience -> monthly budget the audience justifies."""
    audience = int(round(clicks * cfg["pixel_match_rate"]))
    impressions = audience * cfg["frequency"]
    budget = impressions / 1000.0 * cfg["cpm"]
    if audience < cfg["min_audience"]:
        status = "TOO SMALL — cannot target yet (Meta floor 100)"
        budget = 0.0
    elif audience < cfg["efficient_audience"]:
        status = "Thin — fold into a combined audience"
    else:
        status = "Standalone-ready"
    return audience, round(budget, 2), status


def build_table(rows, cfg):
    out = []
    for r in rows:
        aud, bud, status = audience_and_budget(r["clicks"], cfg)
        out.append({**r, "audience": aud, "budget": bud, "status": status})
    out.sort(key=lambda x: x["clicks"], reverse=True)
    return out


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------
def render_markdown(table, cfg, source_note):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"# Switchy Retargeting Report — {ts}",
        "",
        f"_Data source: {source_note}_  ",
        f"_Model: pixel match {int(cfg['pixel_match_rate']*100)}%, "
        f"freq {cfg['frequency']}x / {cfg['window_days']}d, CPM ${cfg['cpm']:.0f}_",
        "",
        "| Short link | Tags | Destination | Clicks | Audience | Monthly budget | Status |",
        "|---|---|---|---:|---:|---:|---|",
    ]
    tot_clicks = tot_aud = tot_bud = 0
    for r in table:
        dest = (r["destination"][:42] + "…") if len(r["destination"]) > 43 else r["destination"]
        lines.append(
            f"| {r['short']} | {r['tags']} | {dest} | {r['clicks']:,} | "
            f"{r['audience']:,} | ${r['budget']:,.0f} | {r['status']} |"
        )
        tot_clicks += r["clicks"]; tot_aud += r["audience"]; tot_bud += r["budget"]
    lines += [
        f"| **TOTAL** | | | **{tot_clicks:,}** | **{tot_aud:,}** | **${tot_bud:,.0f}** | |",
        "",
        "**How to read this:** *Audience* = clicks that resolve to a targetable "
        "pixeled user. *Monthly budget* is what it costs to hit that audience "
        f"{cfg['frequency']}x over {cfg['window_days']} days at ${cfg['cpm']:.0f} CPM — "
        "i.e. the spend the audience can actually absorb, not a target. Audiences "
        "under 100 can't be targeted; under 1,000 should be merged by source.",
    ]
    return "\n".join(lines)


def write_csv(table, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["short", "title", "tags", "destination",
                                          "clicks", "audience", "budget", "status"])
        w.writeheader()
        w.writerows(table)


# ---------------------------------------------------------------------------
# Demo data (used only when no token is available)
# ---------------------------------------------------------------------------
DEMO_ROWS = [
    {"short": "hi.switchy.io/epa-report", "title": "EPA Report newsletter CTA", "tags": "newsletter,consumer",
     "destination": "https://graehamwatts.com/home-value", "clicks": 2140},
    {"short": "hi.switchy.io/yt-channel", "title": "GBP -> YouTube channel", "tags": "gbp,youtube,consumer",
     "destination": "https://youtube.com/@graehamwatts", "clicks": 1880},
    {"short": "hi.switchy.io/1908cooley", "title": "1908 Cooley single-property", "tags": "listing,consumer",
     "destination": "https://graehamwatts.com/1908-cooley", "clicks": 760},
    {"short": "hi.switchy.io/oh-flyer-qr", "title": "Open house flyer QR", "tags": "openhouse,qr,consumer",
     "destination": "https://graehamwatts.com/1908-cooley", "clicks": 240},
    {"short": "hi.switchy.io/postcard-94303", "title": "94303 farm postcard QR", "tags": "postcard,qr,consumer",
     "destination": "https://graehamwatts.com/home-value", "clicks": 95},
    {"short": "hi.switchy.io/sig", "title": "Email signature", "tags": "signature,mixed",
     "destination": "https://graehamwatts.com", "clicks": 60},
]


def main():
    ap = argparse.ArgumentParser(description="Switchy per-link retargeting analytics.")
    ap.add_argument("--confirm-schema", action="store_true",
                    help="Introspect the `links` type and exit. RUN THIS FIRST on a live token.")
    ap.add_argument("--click-field", default="clicks",
                    help="Scalar click/scan count field on the links type (confirm via --confirm-schema).")
    ap.add_argument("--cpm", type=float, default=DEFAULTS["cpm"])
    ap.add_argument("--frequency", type=int, default=DEFAULTS["frequency"])
    ap.add_argument("--pixel-match-rate", type=float, default=DEFAULTS["pixel_match_rate"])
    ap.add_argument("--out", default="switchy_report")
    args = ap.parse_args()

    cfg = dict(DEFAULTS, cpm=args.cpm, frequency=args.frequency,
               pixel_match_rate=args.pixel_match_rate)

    token, source = resolve_token()

    if args.confirm_schema:
        if not token:
            raise SystemExit("No token found. Set SWITCHY_API_TOKEN or ~/.switchy/token first.")
        confirm_schema(token)
        return

    if token:
        rows = fetch_links(token, args.click_field)
        source_note = f"LIVE Switchy API ({source})"
    else:
        rows = DEMO_ROWS
        source_note = "DEMO data (no token found — illustrative numbers)"
        sys.stderr.write(
            "\n[!] No Switchy token found — running in DEMO mode.\n"
            "    To go live: get the token from Switchy (Workspace > Settings >\n"
            "    Integrations > Generate a token; you may need to ask Switchy live\n"
            "    chat to enable API access first), then:\n"
            "        export SWITCHY_API_TOKEN=xxxx   (mac/linux)\n"
            "        setx SWITCHY_API_TOKEN xxxx      (windows)\n"
            "    Then re-run with --confirm-schema to lock the click field name.\n\n")

    table = build_table(rows, cfg)
    md = render_markdown(table, cfg, source_note)
    Path(args.out + ".md").write_text(md, encoding="utf-8")
    write_csv(table, args.out + ".csv")
    print(md)
    print(f"\n[written] {args.out}.md  and  {args.out}.csv")


if __name__ == "__main__":
    main()
