#\!/usr/bin/env python3
"""
Local webhook handler for the V6 Production Calendar "🚀 Full Auto-Render" button.

Runs a Flask server on http://127.0.0.1:7788/render that accepts:
    POST /render
    {"slug": "ab1482-explainer", "script_path": "/abs/path/to/script.ssml.txt"}

It spawns full_render.py in the background and immediately returns {"queued": true, "job_id": ...}.
Poll GET /status/<job_id> to check progress.

Start it:
    python3 webhook_handler.py
Bind to your desktop only — never expose publicly (no auth on this endpoint).
"""
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

app = Flask(__name__)

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
    except Exception as e:
        JOBS[job_id]["status"] = "failed"
        JOBS[job_id]["error"] = str(e)

@app.post("/render")
def render():
    payload = request.get_json(force=True)
    slug = payload["slug"]
    script_path = payload["script_path"]
    job_id = str(uuid.uuid4())
    JOBS[job_id] = {"status": "queued", "slug": slug}
    threading.Thread(target=run_job, args=(job_id, slug, script_path), daemon=True).start()
    return jsonify({"queued": True, "job_id": job_id})

@app.get("/status/<job_id>")
def status(job_id):
    return jsonify(JOBS.get(job_id, {"error": "unknown job"}))

if __name__ == "__main__":
    # 127.0.0.1 = desktop-only. Do not change to 0.0.0.0 without auth.
    app.run(host="127.0.0.1", port=7788)
