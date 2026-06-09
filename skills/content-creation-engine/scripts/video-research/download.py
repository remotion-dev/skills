#!/usr/bin/env python3
"""
download.py — Two-tier video downloader.

Tier A: yt-dlp (primary)
    - Free, best-in-class, ~1000 supported sites
    - Requires the host network to reach the source domain
    - Will fail in restricted sandboxes where youtube.com is not on the allowlist

Tier B: Apify YouTube downloader actor (fallback)
    - Paid (~$0.10-0.30/video)
    - Works in any network environment as long as the Composio MCP can reach Apify
    - Invoked by Claude via the Composio MCP — this script provides the helper to
      normalize the Apify response and download the resulting MP4 to a local path.

Usage:
    python download.py <url> --out video.mp4

For Apify fallback, the calling Claude code:
    1. Calls the Apify MCP actor with the URL
    2. Receives an MP4 download URL in the response
    3. Calls download_from_url(url, dest) here to fetch the file
"""

import argparse
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path


# -------------------------------------------------------------------
# Tier A: yt-dlp
# -------------------------------------------------------------------

def download_via_ytdlp(url: str, out_path: Path,
                       resolution: str = "720") -> bool:
    """
    Download via yt-dlp. Returns True on success, False if yt-dlp is unavailable
    or the download fails (network blocked, video private, etc.)
    """
    if not shutil.which('yt-dlp'):
        # Try pip install on the fly
        try:
            subprocess.run(
                [sys.executable, '-m', 'pip', 'install', '--quiet',
                 '--break-system-packages', 'yt-dlp'],
                check=True, capture_output=True,
            )
        except subprocess.CalledProcessError:
            return False

    out_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        sys.executable, '-m', 'yt_dlp',
        '-f', f'best[height<={resolution}]/bestvideo[height<={resolution}]+bestaudio',
        '--merge-output-format', 'mp4',
        '-o', str(out_path),
        '--no-playlist',
        '--quiet',
        '--no-warnings',
        url,
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=600)
        return out_path.exists() and out_path.stat().st_size > 0
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        # Common failure modes:
        #   - 403 Forbidden (proxy/allowlist blocking)
        #   - 410 Gone (video deleted)
        #   - HTTP error on a backend YouTube call
        return False


# -------------------------------------------------------------------
# Tier B helper: download_from_url
# -------------------------------------------------------------------

def download_from_url(url: str, dest: Path) -> bool:
    """
    Download a file from a direct URL (e.g. an Apify-provided MP4 link)
    to the destination path. Used by the Apify fallback path.
    """
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=300) as resp, open(dest, 'wb') as f:
            shutil.copyfileobj(resp, f)
        return dest.exists() and dest.stat().st_size > 0
    except Exception as e:
        print(f"  [!] Download from URL failed: {e}", file=sys.stderr)
        return False


# -------------------------------------------------------------------
# Public entry point
# -------------------------------------------------------------------

def download_video(url: str, out_path: Path,
                    apify_mp4_url: str | None = None) -> dict:
    """
    Try Tier A (yt-dlp) first. If it fails AND the caller has provided an
    apify_mp4_url (already obtained via Composio MCP), fall back to Tier B.

    Returns:
        {
            'success': bool,
            'method': 'yt-dlp' | 'apify' | None,
            'path': str | None,
            'reason': str (on failure),
        }
    """
    # Tier A
    if download_via_ytdlp(url, out_path):
        return {'success': True, 'method': 'yt-dlp', 'path': str(out_path)}

    # Tier B (only if caller provided Apify URL)
    if apify_mp4_url:
        if download_from_url(apify_mp4_url, out_path):
            return {'success': True, 'method': 'apify', 'path': str(out_path)}
        else:
            return {'success': False, 'method': None,
                    'reason': 'Both yt-dlp and Apify fallback failed'}

    return {'success': False, 'method': None,
            'reason': 'yt-dlp failed and no Apify fallback URL provided. '
                      'Either allowlist youtube.com in Cowork settings, '
                      'or invoke the Apify YouTube actor via Composio first '
                      'and pass the resulting MP4 URL.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Two-tier video downloader')
    parser.add_argument('url')
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--resolution', default='720')
    parser.add_argument('--apify-url', default=None,
                        help='Optional fallback MP4 URL from Apify actor')
    args = parser.parse_args()

    result = download_video(args.url, args.out, apify_mp4_url=args.apify_url)
    if result['success']:
        print(f"✓ Downloaded via {result['method']}: {result['path']}")
        sys.exit(0)
    else:
        print(f"✗ Failed: {result['reason']}", file=sys.stderr)
        sys.exit(1)
