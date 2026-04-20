#\!/usr/bin/env python3
"""
heygen_render.py — Render a HeyGen avatar video from a single-topic dashboard.

One-line usage (from Windows PowerShell):
    python heygen_render.py --topic epa-two-years-homicide-free --format yt-short --look digital_twin

Reads HEYGEN_API_KEY from Windows environment variable (never from chat).
Fetches the script + SSML for the specified topic + format from GitHub Pages.
Calls HeyGen's v2 API. Returns video_id + dashboard URL. Opens browser.

Setup once:
    [Environment]::SetEnvironmentVariable("HEYGEN_API_KEY", "sk_V2_...", "User")

Then restart PowerShell to load the env var.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import webbrowser
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

# ============================================================
# CONFIG
# ============================================================

TOPIC_URLS = {
    "epa-two-years-homicide-free": "https://graehamwatts.github.io/skills/content-calendars/2026-04-18-epa-two-years-homicide-free-production.html",
    "peninsula-bidding-wars-back":  "https://graehamwatts.github.io/skills/content-calendars/2026-04-19-peninsula-bidding-wars-back-production.html",
    "epa-market-update":            "https://graehamwatts.github.io/skills/content-calendars/2026-04-19-epa-market-update-production.html",
    "ca-smoke-detector-compliance": "https://graehamwatts.github.io/skills/content-calendars/2026-04-19-ca-smoke-detector-compliance-production.html",
    "woodland-park-772-units":      "https://graehamwatts.github.io/skills/content-calendars/2026-04-19-woodland-park-772-units-production.html",
}

# Graeham's 6 HeyGen avatar looks (from skills/heygen-video/references/avatars.md)
AVATARS = {
    "digital_twin":       {"id": "159cd7b883724fdb9a51b97dec94df89", "aspect": "9:16", "note": "Authentic video-trained avatar — best for face-critical long-form"},
    "casual_chic":        {"id": "afdc7e3e9f0c45de896fa687c594a216", "aspect": "9:16", "note": "Approachable everyday tone"},
    "freshly_ironed":     {"id": "09fed5d2c0b74376b6e7313cbb888c86", "aspect": "9:16", "note": "Polished — seller presentations"},
    "fashion_flip":       {"id": "b0644e6b20ba414981b7821d88caf675", "aspect": "9:16", "note": "Higher energy — hooks + pattern interrupts"},
    "bespectacled":       {"id": "1b25c855f03b471da5bacb918c4acbc0", "aspect": "9:16", "note": "Tech/PropOS adjacent"},
    "suburban_serenity":  {"id": "bbc381b39e0f458e8d274cf1ac2c38ba", "aspect": "16:9", "note": "Landscape-first — horizontal content"},
}

# Graeham's voice clone (default across all looks)
VOICE_CLONE_ID = "717249201f7745988219b9aeb9041b42"

HEYGEN_API = "https://api.heygen.com/v2/video/generate"

# ============================================================
# HELPERS
# ============================================================

def die(msg, code=1):
    print(f"❌ ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def info(msg):
    print(msg)


def fetch_dashboard_html(topic):
    """Fetch the dashboard HTML from GitHub Pages."""
    url = TOPIC_URLS.get(topic)
    if not url:
        die(f"Unknown topic: {topic}. Valid: {', '.join(TOPIC_URLS.keys())}")
    try:
        req = Request(url, headers={"User-Agent": "heygen-render/1.0"})
        return urlopen(req, timeout=20).read().decode("utf-8")
    except (HTTPError, URLError) as e:
        die(f"Could not fetch dashboard: {e}")


def extract_content(html, format_key):
    """Extract the CONTENT_LIBRARY entry for the given format."""
    m = re.search(r"window\.CONTENT_LIBRARY\s*=\s*(\{.*?\});", html, re.DOTALL)
    if not m:
        die("Could not find CONTENT_LIBRARY in dashboard HTML")
    try:
        data = json.loads(m.group(1))
    except json.JSONDecodeError as e:
        die(f"CONTENT_LIBRARY is not valid JSON: {e}")
    if format_key not in data:
        die(f"Format '{format_key}' not found. Valid: {', '.join(data.keys())}")
    return data[format_key]


def extract_speakable_text(content):
    """
    Extract just the text that should be spoken. Priority:
    1. If an SSML <speak>...</speak> block is present, use that (HeyGen honors <break>).
    2. Else, strip markdown/script metadata and return the first script section.
    """
    # Prefer SSML if present
    ssml_match = re.search(r"<speak>.*?</speak>", content, re.DOTALL)
    if ssml_match:
        return ssml_match.group(0)

    # Strip common metadata markers
    lines = content.split("\n")
    cleaned = []
    in_ssml = False
    for line in lines:
        if line.startswith("═══") or line.startswith("==="):
            continue
        if line.strip().startswith("#") or line.strip().startswith("[") and line.strip().endswith("]"):
            continue
        if line.strip().startswith("Word count") or line.strip().startswith("Formula"):
            continue
        if line.strip().startswith("OUTPUT") or line.strip().startswith("DELIVERABLES"):
            continue
        cleaned.append(line)
    text = "\n".join(cleaned).strip()
    # Truncate to reasonable size — HeyGen has input length limits
    return text[:2500]


def render(topic, format_key, look, override_aspect=None, dry_run=False):
    api_key = os.environ.get("HEYGEN_API_KEY")
    if not api_key:
        die("HEYGEN_API_KEY env var is not set. Run:\n"
            "    [Environment]::SetEnvironmentVariable(\"HEYGEN_API_KEY\", \"sk_V2_...\", \"User\")\n"
            "Then restart PowerShell.")

    if look not in AVATARS:
        die(f"Unknown avatar: {look}. Valid: {', '.join(AVATARS.keys())}")

    avatar = AVATARS[look]
    aspect = override_aspect or avatar["aspect"]

    info(f"📡 Fetching dashboard for topic '{topic}'...")
    html = fetch_dashboard_html(topic)

    info(f"📝 Extracting '{format_key}' content...")
    content = extract_content(html, format_key)

    speakable = extract_speakable_text(content)
    info(f"🎬 Render plan:")
    info(f"   Topic:    {topic}")
    info(f"   Format:   {format_key}")
    info(f"   Avatar:   {look} ({avatar['id']}) — {avatar['note']}")
    info(f"   Voice:    Graeham Watts Voice Clone ({VOICE_CLONE_ID})")
    info(f"   Aspect:   {aspect}")
    info(f"   Script:   {len(speakable):,} chars")

    if dry_run:
        info(f"\n[DRY RUN] Would POST to {HEYGEN_API}")
        info(f"[DRY RUN] Script preview (first 300 chars): {speakable[:300]}...")
        return None

    width, height = (1920, 1080) if aspect == "16:9" else (1080, 1920)

    payload = {
        "video_inputs": [
            {
                "character": {
                    "type": "avatar",
                    "avatar_id": avatar["id"],
                    "avatar_style": "normal",
                },
                "voice": {
                    "type": "text",
                    "voice_id": VOICE_CLONE_ID,
                    "input_text": speakable,
                },
                "background": {
                    "type": "color",
                    "value": "#1a1a2e",
                },
            }
        ],
        "dimension": {"width": width, "height": height},
        "title": f"{topic} — {format_key}",
    }

    info(f"\n🚀 Submitting to HeyGen...")

    req = Request(
        HEYGEN_API,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "X-Api-Key": api_key,
            "Accept": "application/json",
        },
        method="POST",
    )

    try:
        response = urlopen(req, timeout=30)
        raw = response.read().decode("utf-8")
    except HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else ""
        die(f"HeyGen API returned {e.code}: {body}")
    except URLError as e:
        die(f"Could not reach HeyGen API: {e}")

    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        die(f"HeyGen returned non-JSON response: {raw[:500]}")

    # HeyGen response shape: {"error": null, "data": {"video_id": "..."}}
    if result.get("error"):
        die(f"HeyGen error: {result['error']}")

    video_id = result.get("data", {}).get("video_id")
    if not video_id:
        die(f"No video_id in response: {raw[:500]}")

    dashboard_url = f"https://app.heygen.com/videos/{video_id}"

    info(f"\n✅ Video queued successfully!")
    info(f"   video_id:  {video_id}")
    info(f"   Dashboard: {dashboard_url}")
    info(f"   Status:    Rendering — typically 2-15 min depending on length")
    info(f"\n💡 Opening HeyGen dashboard in your browser...")

    try:
        webbrowser.open(dashboard_url)
    except Exception:
        pass

    # Append to render log
    try:
        log_dir = os.path.expanduser("~/heygen_renders")
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "render_log.jsonl")
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps({
                "topic": topic,
                "format": format_key,
                "look": look,
                "aspect": aspect,
                "video_id": video_id,
                "dashboard_url": dashboard_url,
            }) + "\n")
    except Exception:
        pass

    return video_id


def main():
    p = argparse.ArgumentParser(
        description="Render a HeyGen avatar video from a single-topic dashboard.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Topics:  {', '.join(TOPIC_URLS.keys())}
Avatars: {', '.join(AVATARS.keys())}

Example:
    python heygen_render.py --topic epa-two-years-homicide-free --format yt-short --look fashion_flip
""".strip(),
    )
    p.add_argument("--topic", required=True, choices=list(TOPIC_URLS.keys()))
    p.add_argument("--format", required=True, help="Format key e.g. yt-long-pt1, yt-short, ig-reel-1, ig-reel-2, tiktok")
    p.add_argument("--look", default="digital_twin", choices=list(AVATARS.keys()),
                   help="HeyGen avatar. Default: digital_twin (authentic video avatar)")
    p.add_argument("--aspect", default=None, choices=["9:16", "16:9"],
                   help="Override aspect ratio. Default: avatar's preferred aspect.")
    p.add_argument("--dry-run", action="store_true",
                   help="Show render plan without actually submitting to HeyGen.")
    args = p.parse_args()

    render(args.topic, args.format, args.look, args.aspect, args.dry_run)


if __name__ == "__main__":
    main()
