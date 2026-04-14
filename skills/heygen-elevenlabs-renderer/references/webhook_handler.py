#\!/usr/bin/env python3
"""
Local webhook handler for the V6 Production Calendar "🚀 Full Auto-Render" button.

Runs a Flask server on http://127.0.0.1:7788/render that accepts:
    POST /render
    {"slug": "ab1482-explainer", "script_path": "/abs/path/to/script.ssml.txt"}

It spawns full_render.py in the background and immediately returns
{"queued": true, "job_id": ...}. Poll GET /status/<job_id> to check progress.

The /status response now always includes a `dashboards` block with direct
links to HeyGen + ElevenLabs so the calendar UI can surface them the moment
a render finishes — no regex scraping required.

Start it:
    python3 webhook_handler.py

Bind to your desktop only — never expose publicly (no auth on this endpoint).
"""
import json
import re
import subprocess
import threading
import uuid
from pathlib import Path

try:
    from flask import Flask, jsonify, request
except ImportError:
    raise SystemExit("pip install flask --break-system-packages")

SCRIPT_DIR = Path(__file__).parent.parent / "scripts"
JOBS = {}

# Always surface these so the button shows them even before a job completes.
STATIC_DASHBOARDS = {
    "heygen_projects": "https://app.heygen.com/projects",
    "elevenlabs_history": "https://elevenlabs.io/app/speech-synthesis/history",
    "elevenlabs_voice_library": "https://elevenlabs.io/app/voice-library",
}

app = Flask(__name__)


def parse_render_result(stdout: str) -> dict:
    """full_render.py / poll_and_download.py prints `RENDER_RESULT={...}`."""
    m = re.search(r"RENDER_RESULT=(\{.*\})", stdout or "")
    if not m:
        return {}
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError:
        return {}


def run_job(job_id, slug, script_path):
    JOBS[job_id]["status"] = "running"
    try:
        proc = subprocess.run(
            ["python3", str(SCRIPT_DIR / "full_render.py"),
             "--script", script_path, "--slug", slug],
            capture_output=True, text=True, timeout=900,
        )
        JOBS[job_id]["status"] = "done" if proc.returncode == 0 else "failed"
        JOBS[job_id]["stdout"] = proc.stdout
        JOBS[job_id]["stderr"] = proc.stderr

        result = parse_render_result(proc.stdout)
        if result:
            JOBS[job_id]["result"] = result
            JOBS[job_id]["dashboards"] = {
                **STATIC_DASHBOARDS,
                "heygen_video_page": result.get("heygen_dashboard_url"),
                "local_mp4": result.get("out"),
                "meta_json": result.get("meta"),
            }
    except Exception as e:
        JOBS[job_id]["status"] = "failed"
        JOBS[job_id]["error"] = str(e)


@app.post("/render")
def render():
    payload = request.get_json(force=True)
    slug = payload["slug"]
    script_path = payload["script_path"]
    job_id = str(uuid.uuid4())
    JOBS[job_id] = {
        "status": "queued",
        "slug": slug,
        "dashboards": STATIC_DASHBOARDS,  # visible immediately
    }
    threading.Thread(target=run_job, args=(job_id, slug, script_path), daemon=True).start()
    return jsonify({"queued": True, "job_id": job_id, "dashboards": STATIC_DASHBOARDS})


@app.get("/status/<job_id>")
def status(job_id):
    return jsonify(JOBS.get(job_id, {"error": "unknown job"}))


@app.get("/health")
def health():
    return jsonify({"ok": True, "dashboards": STATIC_DASHBOARDS})


if __name__ == "__main__":
    # 127.0.0.1 = desktop-only. Do not change to 0.0.0.0 without auth.
    app.run(host="127.0.0.1", port=7788)
