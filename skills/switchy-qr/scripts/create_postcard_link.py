#!/usr/bin/env python3
"""
create_postcard_link.py — make ONE tracked Switchy link for a postcard QR.

Built for Peter (Jason). Creates the link via Switchy's REST API with the correct
landing page + UTM + folder + Graeham's retargeting pixels already attached, then
prints the short URL. Claude then downloads the QR for that link from the Switchy
dashboard in Chrome.

TOKEN (never printed): env SWITCHY_API_TOKEN, or a file switchy-token.txt in the
Skills folder, or ~/.switchy/token.

USAGE:
  python create_postcard_link.py --date 2026-06-01 --hook "Last 5 Homes"
  optional: --dest <url> --market epa --archetype anti_zestimate --slug epa-comps-0601
"""
import os, sys, json, argparse, urllib.request, urllib.error
from pathlib import Path

REST = "https://api.switchy.io/v1/links/create"
DOMAIN = "hi.switchy.io"
POSTCARD_FOLDER_ID = 92811           # Switchy "Post card qr" folder
DEFAULT_DEST = "https://graehamwatts.com/evaluation"   # home-value report
# Graeham's pixels (so scanners enter the retargeting audience automatically)
PIXELS = [
    {"platform": "facebook", "value": "963211690980393"},
    {"platform": "ga",       "value": "G-S82GF32XJT"},
    {"platform": "adwords",  "value": "AW-1047225119"},
]


def token():
    t = os.environ.get("SWITCHY_API_TOKEN")
    if t:
        return t.strip()
    here = Path(__file__).resolve()
    candidates = [
        Path.cwd() / "switchy-token.txt",
        Path.home() / ".switchy" / "token",
    ]
    # walk up to find a Skills/switchy-token.txt
    for parent in here.parents:
        candidates.append(parent / "switchy-token.txt")
        if parent.name == "Skills":
            candidates.append(parent / "switchy-token.txt")
    for p in candidates:
        try:
            if p.exists():
                return p.read_text(encoding="utf-8").strip()
        except OSError:
            pass
    sys.exit("No Switchy token (set SWITCHY_API_TOKEN or place switchy-token.txt in the Skills folder).")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True, help="mail date YYYY-MM-DD, e.g. 2026-06-01")
    ap.add_argument("--hook", required=True, help='short hook, e.g. "Last 5 Homes"')
    ap.add_argument("--dest", default=DEFAULT_DEST)
    ap.add_argument("--market", default="epa")
    ap.add_argument("--archetype", default="anti_zestimate")
    ap.add_argument("--slug", default=None)
    a = ap.parse_args()

    mmddyy = "".join(a.date.split("-")[::-1][:2][::-1])  # -> keeps mmdd? build explicitly:
    y, m, d = a.date.split("-")
    mmddyy = f"{m}_{d}_{y[2:]}"
    slug = a.slug or f"{a.market}-comps-{m}{d}"
    dest = a.dest + ("&" if "?" in a.dest else "?") + \
        f"utm_source=postcard&utm_medium=direct_mail&utm_campaign={a.market}_{mmddyy}&utm_content={a.archetype}"
    title = f"Postcard {a.market.upper()} {a.date} — {a.hook} (home value)"
    tags = ["postcard", "qr", "consumer", a.market, a.date]

    payload = {"link": {"url": dest, "id": slug, "title": title, "folderId": POSTCARD_FOLDER_ID,
                        "tags": tags, "showGDPR": False, "pixels": PIXELS}, "autofill": False}
    req = urllib.request.Request(REST, data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "Api-Authorization": token()}, method="POST")
    try:
        r = json.loads(urllib.request.urlopen(req, timeout=30).read())
    except urllib.error.HTTPError as e:
        sys.exit(f"Create failed: HTTP {e.code} {e.read().decode('utf-8','ignore')[:300]}")
    short = f"https://{r.get('domain', DOMAIN)}/{r.get('id', slug)}"
    print("SHORT URL :", short)
    print("DEST      :", dest)
    print("FOLDER    : Post card qr (92811)")
    print("PIXELS    : facebook, ga, adwords")
    print("\nNEXT: in Switchy (Chrome) → find this link → Download QR Code → Download as PNG → embed in the postcard.")


if __name__ == "__main__":
    main()
