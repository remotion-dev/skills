#!/usr/bin/env python3
"""
Build the branded off-market HTML report.

Usage:
    python build_report.py \
        --city "Menlo Park" \
        --data properties.json \
        --template ../assets/report_template.html \
        --out Off_Market_Menlo_Park_16-04-2026.html

properties.json shape:
[
  {
    "address": "123 Laurel St, Menlo Park, CA 94025",
    "beds": 3,
    "baths": 2.5,
    "sqft": 1850,
    "lot_sqft": 6250,           // OR "lot_acres": 0.25
    "year_built": 1962,
    "list_price": 2175000,
    "main_photo": "https://...",
    "extra_photos": ["https://...", "https://..."]
  }
]
"""

import argparse
import datetime as dt
import html
import json
import re
from pathlib import Path


INTRO_DEFAULT = (
    "As part of our ongoing market research, we've identified the following "
    "properties that are not yet available to the general public. These "
    "off-market opportunities are exclusively available through agent networks."
)

EMPTY_INTRO = (
    "We watch the Members Only / Private Listing Network side of the MLS "
    "every week for properties that never make it to Zillow or Redfin. Here's "
    "what we're seeing right now in your target area."
)


def round_price(price: int) -> int:
    """Round the raw list price to a clean marketing number."""
    if price is None:
        return 0
    price = int(price)
    if price < 2_000_000:
        step = 25_000
    elif price < 5_000_000:
        step = 50_000
    else:
        step = 100_000
    return round(price / step) * step


def fmt_sqft(n):
    if not n:
        return ""
    return f"{int(n):,} SqFt"


def fmt_lot(p):
    if p.get("lot_acres"):
        v = p["lot_acres"]
        return f"{v:g} Acre Lot" if v != 1 else "1 Acre Lot"
    if p.get("lot_sqft"):
        return f"{int(p['lot_sqft']):,} SqFt Lot"
    return ""


def fmt_baths(n):
    if n is None:
        return ""
    if float(n).is_integer():
        return f"{int(n)} Baths"
    return f"{n:g} Baths"


def fmt_beds(n):
    if n is None:
        return ""
    return f"{int(n)} Beds"


def build_stats_row(p):
    parts = []
    if fmt_beds(p.get("beds")):
        parts.append(fmt_beds(p["beds"]))
    if fmt_baths(p.get("baths")):
        parts.append(fmt_baths(p["baths"]))
    if fmt_sqft(p.get("sqft")):
        parts.append(fmt_sqft(p["sqft"]))
    if fmt_lot(p):
        parts.append(fmt_lot(p))
    if p.get("year_built"):
        parts.append(f"Built {int(p['year_built'])}")

    html_parts = []
    for i, piece in enumerate(parts):
        if i > 0:
            html_parts.append('<span class="dot">&middot;</span>')
        html_parts.append(f"<span>{html.escape(piece)}</span>")
    return "".join(html_parts)


def build_thumbs(p):
    extras = p.get("extra_photos") or []
    if not extras:
        return ""
    imgs = "".join(
        f'<img src="{html.escape(u)}" alt="Additional photo of {html.escape(p.get("address",""))}">'
        for u in extras[:2]
    )
    return f'<div class="thumbs">{imgs}</div>'


def build_card(p):
    address = html.escape(p.get("address", "Address withheld"))
    main = html.escape(p.get("main_photo", ""))
    stats = build_stats_row(p)
    price = round_price(p.get("list_price", 0))
    price_fmt = f"{price:,}"
    thumbs = build_thumbs(p)

    return f"""
  <article class="property-card">
    <div class="photo-wrap">
      <img src="{main}" alt="Photo of {address}" onerror="this.style.opacity=0.3;">
    </div>
    <div class="card-body">
      <h3 class="address">{address}</h3>
      <p class="stats">{stats}</p>
      <div class="gold-rule"></div>
      <p class="price">Estimated price around ${price_fmt}</p>
      {thumbs}
    </div>
  </article>
""".strip()


def build_empty_card(city, date_str):
    return f"""
  <article class="property-card empty-card">
    <div class="card-body" style="padding:48px 32px;text-align:center;">
      <h3 class="address" style="margin-bottom:12px;">No off-market matches &mdash; yet.</h3>
      <p class="stats" style="line-height:1.7;">
        No off-market properties matched your criteria in {html.escape(city)} as of {date_str}.
        I'll keep watching the network &mdash; off-market inventory moves fast, and I'll reach out as soon as something fits.
      </p>
    </div>
  </article>
""".strip()


def slugify(s):
    s = re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_")
    return s


def render(template_path, city, properties, intro=None, when=None):
    when = when or dt.date.today()
    date_human = when.strftime("%B %d, %Y")

    tpl = Path(template_path).read_text(encoding="utf-8")
    cards = (
        "\n".join(build_card(p) for p in properties)
        if properties
        else build_empty_card(city, date_human)
    )

    intro_text = intro or (INTRO_DEFAULT if properties else EMPTY_INTRO)

    out = (
        tpl.replace("{{CITY_UPPERCASE}}", html.escape(city.upper()))
        .replace("{{REPORT_DATE}}", html.escape(date_human))
        .replace("{{INTRO_PARAGRAPH}}", html.escape(intro_text))
        .replace("{{CARDS_HTML}}", cards)
        .replace("{{CARD_COUNT}}", str(len(properties)))
    )
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--city", required=True)
    ap.add_argument("--data", required=True, help="Path to JSON file with property list")
    ap.add_argument("--template", required=True, help="Path to report_template.html")
    ap.add_argument("--out", required=True, help="Output HTML path")
    ap.add_argument("--date", help="YYYY-MM-DD; defaults to today")
    args = ap.parse_args()

    props = json.loads(Path(args.data).read_text(encoding="utf-8"))
    when = dt.date.fromisoformat(args.date) if args.date else dt.date.today()
    out_html = render(args.template, args.city, props, when=when)
    Path(args.out).write_text(out_html, encoding="utf-8")
    print(f"Wrote {args.out} with {len(props)} properties.")


if __name__ == "__main__":
    main()
