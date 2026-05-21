#!/usr/bin/env python3
"""
dataforseo_direct.py — Direct DataForSEO API for YouTube subtitles.

Uses the standard DataForSEO HTTP API with Basic Auth.
Bypasses Composio entirely — works from any environment with internet access
to api.dataforseo.com.

Setup (one-time):
    1. Sign up at dataforseo.com (you said you've done this)
    2. Get your API login + password from the dashboard:
       https://app.dataforseo.com/api-access
    3. Save credentials to a local .env file:
        ~/.config/video-research-engine/.env
       with content:
        DATAFORSEO_LOGIN=your_email_or_login
        DATAFORSEO_PASSWORD=your_api_password

       Set permissions to user-only:
        chmod 600 ~/.config/video-research-engine/.env

Usage:
    python dataforseo_direct.py 7kVWFQUTM-o
    python dataforseo_direct.py 7kVWFQUTM-o --language en --location 2840

Cost: ~$0.0036 per video (same as Composio path).
"""

import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


API_BASE = "https://api.dataforseo.com"
TASK_POST = f"{API_BASE}/v3/serp/youtube/video_subtitles/task_post"
TASK_GET = f"{API_BASE}/v3/serp/youtube/video_subtitles/task_get/advanced/{{task_id}}"


# -------------------------------------------------------------------
# Credential loading
# -------------------------------------------------------------------

def load_credentials() -> tuple[str, str]:
    """
    Load DataForSEO credentials from the standard locations:
        1. Environment variables: DATAFORSEO_LOGIN + DATAFORSEO_PASSWORD
        2. ~/.config/video-research-engine/.env

    Raises if neither found.
    """
    login = os.environ.get("DATAFORSEO_LOGIN")
    password = os.environ.get("DATAFORSEO_PASSWORD")

    if login and password:
        return login, password

    env_path = Path.home() / ".config" / "video-research-engine" / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                if k == "DATAFORSEO_LOGIN":
                    login = v
                elif k == "DATAFORSEO_PASSWORD":
                    password = v

    if not login or not password:
        raise RuntimeError(
            "DataForSEO credentials not found. Set DATAFORSEO_LOGIN and "
            "DATAFORSEO_PASSWORD env vars, OR create "
            f"{env_path} with those values."
        )
    return login, password


# -------------------------------------------------------------------
# HTTP helpers
# -------------------------------------------------------------------

def _auth_header(login: str, password: str) -> str:
    raw = f"{login}:{password}".encode("utf-8")
    return "Basic " + base64.b64encode(raw).decode("ascii")


def _request(url: str, method: str, login: str, password: str, body: dict | None = None) -> dict:
    headers = {
        "Authorization": _auth_header(login, password),
        "Content-Type": "application/json",
    }
    data = json.dumps(body).encode("utf-8") if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"DataForSEO {method} {url} → HTTP {e.code}: {body_text[:300]}") from None


# -------------------------------------------------------------------
# Public API
# -------------------------------------------------------------------

def submit_subtitles_task(video_id: str,
                           language_code: str = "en",
                           location_code: int = 2840,
                           priority: str = "normal",
                           login: str | None = None,
                           password: str | None = None) -> str:
    """
    Submit a subtitles task. Returns the task ID (UUID).
    Cost is incurred on submit (~$0.0036 for normal priority, more for high).
    """
    if login is None or password is None:
        login, password = load_credentials()

    body = [{
        "video_id": video_id,
        "language_code": language_code,
        "location_code": location_code,
        "priority": 2 if priority == "high" else 1,
    }]
    resp = _request(TASK_POST, "POST", login, password, body)

    if resp.get("status_code") != 20000:
        raise RuntimeError(f"DataForSEO task_post failed: {resp.get('status_message')}")

    task = resp["tasks"][0]
    if task.get("status_code") not in (20100, 20000):
        raise RuntimeError(f"Task creation failed: {task.get('status_message')}")

    return task["id"]


def fetch_subtitles_result(task_id: str,
                            login: str | None = None,
                            password: str | None = None,
                            poll_interval: float = 4.0,
                            max_wait: float = 120.0) -> dict:
    """
    Poll for the task result. Returns the raw API response (same shape as
    Composio's wrapped response) so it can be passed straight to
    transcribe.normalize_dataforseo_response().
    """
    if login is None or password is None:
        login, password = load_credentials()

    deadline = time.monotonic() + max_wait
    last_err = None
    url = TASK_GET.format(task_id=task_id)

    while time.monotonic() < deadline:
        try:
            resp = _request(url, "GET", login, password)
            if resp.get("status_code") == 20000:
                tasks = resp.get("tasks") or []
                if tasks and tasks[0].get("result"):
                    # Wrap in the {data: {...}} shape that Composio uses
                    # so the normalizer doesn't need a separate code path.
                    return {"data": resp}
            last_err = resp.get("status_message")
        except RuntimeError as e:
            last_err = str(e)
        time.sleep(poll_interval)

    raise RuntimeError(f"Timeout waiting for task {task_id}. Last status: {last_err}")


def transcribe_via_direct_api(video_id: str,
                               language_code: str = "en",
                               location_code: int = 2840) -> dict:
    """
    Convenience: submit + poll + return the result wrapped for the normalizer.
    """
    login, password = load_credentials()
    task_id = submit_subtitles_task(
        video_id, language_code=language_code, location_code=location_code,
        login=login, password=password,
    )
    return fetch_subtitles_result(task_id, login=login, password=password)


# -------------------------------------------------------------------
# CLI
# -------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Direct DataForSEO API call for YouTube subtitles")
    parser.add_argument("video_id", help="11-char YouTube video ID")
    parser.add_argument("--language", default="en")
    parser.add_argument("--location", type=int, default=2840, help="Location code (2840 = US)")
    parser.add_argument("--out", type=Path, default=None, help="Save raw response to JSON")
    args = parser.parse_args()

    result = transcribe_via_direct_api(args.video_id, args.language, args.location)
    out_text = json.dumps(result, indent=2)
    if args.out:
        args.out.write_text(out_text)
        print(f"Wrote {args.out}")
    else:
        print(out_text)
