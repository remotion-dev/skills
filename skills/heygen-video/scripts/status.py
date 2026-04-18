#!/usr/bin/env python3
"""
status.py — Check a HeyGen video's status and download the MP4 if ready.

Usage:
    python3 status.py --video-id <video_id>
    python3 status.py --video-id <video_id> --captioned
    python3 status.py --video-id <video_id> --output-dir /path/to/dir
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import shutil
import subprocess
import sys

DEFAULT_OUTPUT_DIR = pathlib.Path("/home/claude/heygen_outputs")


def die(msg: str, code: int = 1) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Check HeyGen video status and download when ready.")
    p.add_argument("--video-id", required=True, help="Video ID returned by create.py.")
    p.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR),
                   help=f"Where to save the finished MP4 (default: {DEFAULT_OUTPUT_DIR}).")
    p.add_argument("--captioned", action="store_true",
                   help="Also download the captioned (burned-in subtitles) variant.")
    p.add_argument("--only-captioned", action="store_true",
                   help="Download ONLY the captioned variant (skip the clean MP4).")
    return p.parse_args()


def ensure_prereqs() -> None:
    if not os.environ.get("HEYGEN_API_KEY"):
        die("HEYGEN_API_KEY is not set.")
    if not shutil.which("heygen"):
        local_bin = str(pathlib.Path.home() / ".local" / "bin")
        os.environ["PATH"] = f"{local_bin}:{os.environ.get('PATH', '')}"
        if not shutil.which("heygen"):
            die("heygen CLI not found. Run scripts/setup.sh first.")


def get_video(video_id: str) -> dict:
    proc = subprocess.run(
        ["heygen", "video", "get", video_id],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        die(f"heygen video get failed (exit {proc.returncode}):\n{proc.stderr}")
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        die(f"Could not parse CLI output:\n{proc.stdout}")


def download_asset(video_id: str, out_path: pathlib.Path, asset: str = "video") -> pathlib.Path | None:
    """asset is 'video' (clean MP4) or 'captioned' (burned-in subtitles).

    Returns the path on success, or None on sandbox/network failure (does not exit).
    Hard exits only on genuine CLI usage errors.
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        ["heygen", "video", "download", video_id,
         "--asset", asset,
         "--output-path", str(out_path),
         "--force"],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        # Distinguish sandbox egress blocks (non-fatal) from real errors
        err = (proc.stdout or "") + (proc.stderr or "")
        if "403" in err or "host_not_allowed" in err or "forbidden" in err.lower():
            print(f"Warning: could not download '{asset}' from HeyGen CDN "
                  f"(sandbox network restriction — run this on your local machine to get the file).",
                  file=sys.stderr)
            return None
        print(f"Warning: download ('{asset}') failed: {err.strip()[:200]}", file=sys.stderr)
        return None
    if not out_path.exists() or out_path.stat().st_size == 0:
        print(f"Warning: download completed but file missing/empty at {out_path}", file=sys.stderr)
        return None
    return out_path


def main() -> int:
    args = parse_args()
    ensure_prereqs()

    response = get_video(args.video_id)
    data = response.get("data", response)
    status = data.get("status", "unknown")
    video_url = data.get("video_url")

    print(f"Video: {args.video_id}")
    print(f"Status: {status}")

    if status == "completed":
        out_dir = pathlib.Path(args.output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        downloaded: list[pathlib.Path] = []

        if not args.only_captioned:
            clean_path = out_dir / f"{args.video_id}.mp4"
            result = download_asset(args.video_id, clean_path, "video")
            if result is not None:
                downloaded.append(result)

        if args.captioned or args.only_captioned:
            captioned_path = out_dir / f"{args.video_id}_captioned.mp4"
            result = download_asset(args.video_id, captioned_path, "captioned")
            if result is not None:
                downloaded.append(result)

        for p in downloaded:
            size_mb = p.stat().st_size / (1024 * 1024)
            print(f"✓ Downloaded: {p}  ({size_mb:.2f} MB)")
        if video_url:
            print(f"  Hosted URL:  {video_url}")
        if not downloaded:
            print("  (No local download — use the hosted URL or the dashboard instead.)")

    elif status in ("processing", "pending", "waiting", "queued"):
        duration = data.get("duration")
        created_at = data.get("created_at")
        print(f"Still processing. Created: {created_at}. Typical wait: 2–10 min for short scripts.")
        if duration:
            print(f"Target duration: {duration}s")
    elif status == "failed":
        error = data.get("error") or data.get("message") or "unknown error"
        die(f"Video generation failed: {error}", code=2)
    else:
        print(f"Unexpected status: {status}")
        print(f"Full response: {json.dumps(data, indent=2)[:500]}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
