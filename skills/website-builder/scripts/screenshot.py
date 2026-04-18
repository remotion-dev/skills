#!/usr/bin/env python3
"""
Screenshot helper for the website-builder screenshot-loop workflow.

Uses Playwright if available; falls back to headless Chromium.

Usage:
    python3 screenshot.py <html-file> <output-png> [--width 1440] [--height 900] [--full-page]
    python3 screenshot.py outputs/index.html outputs/screenshots/index-v1.png
    python3 screenshot.py outputs/index.html outputs/screenshots/index-mobile.png --width 375 --full-page
"""

from __future__ import annotations
import argparse, os, shutil, subprocess, sys, time
from pathlib import Path


def via_playwright(html_path: Path, out_path: Path, width: int, height: int, full_page: bool) -> bool:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return False

    out_path.parent.mkdir(parents=True, exist_ok=True)
    file_url = f"file://{html_path.resolve()}"
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": width, "height": height})
        page = ctx.new_page()
        page.goto(file_url, wait_until="networkidle")
        # Trigger any reveal-on-scroll elements
        page.evaluate("document.querySelectorAll('.reveal').forEach(e => e.classList.add('visible'))")
        time.sleep(0.5)  # let any transitions settle
        page.screenshot(path=str(out_path), full_page=full_page)
        browser.close()
    return True


def via_chromium(html_path: Path, out_path: Path, width: int, height: int) -> bool:
    exe = shutil.which("chromium") or shutil.which("google-chrome") or shutil.which("chrome")
    if not exe:
        return False

    out_path.parent.mkdir(parents=True, exist_ok=True)
    file_url = f"file://{html_path.resolve()}"
    cmd = [
        exe, "--headless", "--disable-gpu", "--no-sandbox",
        f"--window-size={width},{height}",
        f"--screenshot={out_path.resolve()}",
        "--virtual-time-budget=3000",
        file_url,
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html_file")
    ap.add_argument("output_png")
    ap.add_argument("--width", type=int, default=1440)
    ap.add_argument("--height", type=int, default=900)
    ap.add_argument("--full-page", action="store_true", help="Capture full scrollable page (Playwright only)")
    args = ap.parse_args()

    html = Path(args.html_file)
    if not html.exists():
        sys.exit(f"HTML file not found: {html}")
    out = Path(args.output_png)

    print(f"Rendering {html} at {args.width}x{args.height}...")

    if via_playwright(html, out, args.width, args.height, args.full_page):
        print(f"[playwright] wrote {out}")
        return
    if via_chromium(html, out, args.width, args.height):
        print(f"[chromium] wrote {out}")
        return
    sys.exit("No screenshot backend available. Install playwright (`pip install playwright && playwright install chromium`) or chromium.")


if __name__ == "__main__":
    main()
