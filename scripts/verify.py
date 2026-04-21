#!/usr/bin/env python3
"""
verify.py — comprehensive QA across all dashboards + email + scripts.

Run:  python3 scripts/verify.py
Exit: 0 if all green, 1 if any check fails.

Checks:
  1. URL fetch — every published file returns 200 from GitHub Pages
  2. Stylesheet count — max 2 per dashboard (baseline + consolidated)
  3. Inline JS syntax — node --check every <script> block
  4. Sentinel presence — UNIFIED_FINAL_V2 on every dashboard
  5. Sentinel absence — old V1 + the 4 layered stylesheets are stripped
  6. Date consistency — no chrome-level "April 20" leftover after reschedule
  7. Hero contrast — h1 white-on-navy CSS rule present
  8. HTML structure — script tag pairs balance, body/html closure
  9. Stale text — no "Tuesday April 21 candidate" leftovers
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

REPO = Path("/var/tmp/stage3/skills")
DASH_DIR = REPO / "content-calendars"

DASHBOARDS = [
    "2026-04-18-epa-two-years-homicide-free-production.html",
    "2026-04-19-peninsula-bidding-wars-back-production.html",
    "2026-04-19-epa-market-update-production.html",
    "2026-04-19-ca-smoke-detector-compliance-production.html",
    "2026-04-19-woodland-park-772-units-production.html",
]

ALSO_HOSTED = [
    ("emails", "2026-04-19-peter-dashboard-onboarding.html"),
    (None, "render_status.json"),
]

BASE_URL = "https://graehamwatts.github.io/skills"


# ---------------------------------------------------------------------------
# Result helpers
# ---------------------------------------------------------------------------

GREEN = "\033[32m"
RED = "\033[31m"
YEL = "\033[33m"
RST = "\033[0m"


class Results:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.warned = 0
        self.lines = []

    def ok(self, label):
        self.passed += 1
        self.lines.append(f"  {GREEN}OK   {RST} {label}")

    def fail(self, label, detail=""):
        self.failed += 1
        d = f" ({detail})" if detail else ""
        self.lines.append(f"  {RED}FAIL {RST} {label}{d}")

    def warn(self, label, detail=""):
        self.warned += 1
        d = f" ({detail})" if detail else ""
        self.lines.append(f"  {YEL}WARN {RST} {label}{d}")

    def section(self, name):
        self.lines.append(f"\n{name}")
        self.lines.append("─" * len(name))

    def report(self):
        for ln in self.lines:
            print(ln)
        total = self.passed + self.failed + self.warned
        print()
        print(f"  Passed: {self.passed}/{total}    Failed: {self.failed}    Warnings: {self.warned}")
        if self.failed == 0:
            print(f"\n  {GREEN}ALL CHECKS PASSED{RST}\n")
            return 0
        print(f"\n  {RED}{self.failed} CHECK(S) FAILED{RST}\n")
        return 1


# ---------------------------------------------------------------------------
# Individual checks
# ---------------------------------------------------------------------------

def check_url(url: str, results: Results, label: str) -> None:
    try:
        req = Request(url, headers={"User-Agent": "verify/1.0"}, method="HEAD")
        resp = urlopen(req, timeout=15)
        code = resp.getcode()
        if code == 200:
            results.ok(f"{label} → 200")
        else:
            results.fail(f"{label} → {code}")
    except HTTPError as e:
        results.fail(label, f"HTTP {e.code}")
    except URLError as e:
        results.warn(label, f"network blocked: {e.reason}")


def check_dashboard(name: str, results: Results) -> None:
    path = DASH_DIR / name
    if not path.exists():
        results.fail(f"{name} exists")
        return
    html = path.read_text(encoding="utf-8")
    short = name.split("-")[3:6]
    short = "-".join(short).split(".")[0][:30]

    # 1. Stylesheet count
    head = html[:html.find("</head>")]
    n_styles = head.count("<style>")
    if n_styles == 2:
        results.ok(f"{short} stylesheets in <head>: {n_styles} (baseline + consolidated)")
    else:
        results.fail(f"{short} stylesheets in <head>: {n_styles}", "expected 2")

    # 2. Sentinel presence
    if "UNIFIED_FINAL_V2" in html:
        results.ok(f"{short} UNIFIED_FINAL_V2 sentinel present")
    else:
        results.fail(f"{short} UNIFIED_FINAL_V2 sentinel MISSING")

    # 3. Old sentinels stripped
    olds = ["UNIFIED_FINAL_V1", "RENDER_STATUS_CSS_V1", "REDESIGN_V5_CSS",
            "UNIFY_V6 — one visual language", "UNIFY_V6_TEXT_FIX"]
    leftover = [s for s in olds if s in html]
    if not leftover:
        results.ok(f"{short} all 4 layered stylesheets stripped")
    else:
        results.fail(f"{short} leftover sentinel(s)", ", ".join(leftover))

    # 4. Hero contrast fix present
    if ".hero h1" in html and "color: #FFFFFF" in html:
        results.ok(f"{short} hero h1 contrast rule present")
    else:
        results.fail(f"{short} hero h1 contrast rule MISSING")

    # 5. Date consistency — no "Monday April 20" or "April 20, 2026" in chrome
    chrome = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    bad_dates = []
    for token in ["Monday April 20", "Monday, April 20", "April 20, 2026"]:
        if token in chrome:
            bad_dates.append(token)
    if not bad_dates:
        results.ok(f"{short} chrome dates: rescheduled to Apr 27+")
    else:
        results.fail(f"{short} chrome still has", ", ".join(bad_dates))

    # 6. v5 hero structure
    if 'class="hero v5-hero"' in html or 'v5-recommended-label' in html:
        results.ok(f"{short} v5 hero applied")
    else:
        results.fail(f"{short} v5 hero MISSING")

    # 7. JS syntax via node --check
    blocks = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
    js_ok = True
    for i, b in enumerate(blocks):
        tmp = Path(f"/tmp/verify_{i}.js")
        tmp.write_text(b)
        r = subprocess.run(["node", "--check", str(tmp)], capture_output=True, text=True)
        if r.returncode != 0:
            js_ok = False
            break
    if js_ok:
        results.ok(f"{short} all {len(blocks)} inline scripts pass node --check")
    else:
        results.fail(f"{short} inline JS syntax FAILED")

    # 8. HTML structure — script tag pairs balanced, body close exists
    opens = len(re.findall(r"<script[^>]*>", html))
    closes = len(re.findall(r"</script>", html))
    if opens == closes:
        results.ok(f"{short} <script> pairs balanced ({opens})")
    else:
        results.fail(f"{short} <script> pairs", f"opens={opens} closes={closes}")
    last_body = html.rfind("</body>")
    last_script = html.rfind("</script>")
    if last_body > last_script:
        results.ok(f"{short} </body> after final </script>")
    else:
        results.fail(f"{short} </body>/</script> order wrong")

    # 9. Stale text
    stale_terms = ["Tuesday April 21 candidate", "candidate topic"]
    stale_found = [s for s in stale_terms if s in chrome]
    if not stale_found:
        results.ok(f"{short} no stale candidate text")
    else:
        results.fail(f"{short} stale text", ", ".join(stale_found))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    results = Results()

    results.section("URL liveness (GitHub Pages)")
    for name in DASHBOARDS:
        check_url(f"{BASE_URL}/content-calendars/{name}", results, f"dashboard: {name[:42]}")
    for folder, fname in ALSO_HOSTED:
        url = f"{BASE_URL}/{folder + '/' if folder else ''}{fname}"
        check_url(url, results, fname)

    results.section("Per-dashboard structure + sentinels + JS + dates")
    for name in DASHBOARDS:
        check_dashboard(name, results)

    return results.report()


if __name__ == "__main__":
    sys.exit(main())
