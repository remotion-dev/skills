#!/usr/bin/env python3
"""
ElevenLabs VO generation for the 5 standard cinematic trailer lines.

Usage:
    python3 synthesize_vos.py \
        --config trailer-vo-config.json \
        --out-dir /path/to/vo/

Config JSON format:
    {
      "lines": [
        {
          "filename": "vo-01-cold-open.mp3",
          "text": "<speak>Forty-seven days. <break time=\"0.8s\"/></speak>",
          "voice": "narrator"
        },
        {
          "filename": "vo-04-dialogue.mp3",
          "text": "<speak>Tell your buyer the seller doesn't blink.</speak>",
          "voice": "graeham"
        }
      ]
    }

Voice IDs and settings are encoded below — these are the production-tested
values from "The Last 47 Days" build. Don't lower them without good reason.
"""
import argparse, json, os, sys, time, urllib.request
from pathlib import Path

# --- Voice registry (locked from production runs) ---
VOICES = {
    "narrator": {
        # Brian — ElevenLabs stock cinematic narrator (deep, measured)
        "id": "nPczCjzI2devNBz1zQrb",
        "settings": {
            "stability": 0.40,
            "similarity_boost": 0.80,
            "style": 0.55,
            "use_speaker_boost": True,
        },
    },
    "graeham": {
        # Graeham Watts cloned voice
        "id": "Pa3vOYQHHpLJn1Tf7hnP",
        "settings": {
            "stability": 0.35,
            "similarity_boost": 0.85,
            "style": 0.50,
            "use_speaker_boost": True,
        },
    },
    # Alternative narrators if Brian doesn't fit a project's tone
    "george": {
        # George — British, gravelly, "voice of God" trailer narrator
        "id": "JBFqnCBsd6RMkjVDRZzb",
        "settings": {
            "stability": 0.40,
            "similarity_boost": 0.80,
            "style": 0.55,
            "use_speaker_boost": True,
        },
    },
    "adam": {
        # Adam — deeper, weightier
        "id": "pNInz6obpgDQGcFmaJgB",
        "settings": {
            "stability": 0.40,
            "similarity_boost": 0.80,
            "style": 0.55,
            "use_speaker_boost": True,
        },
    },
}

MODEL = "eleven_multilingual_v2"  # honors <break> tags reliably

CRED_PATH = Path(os.environ.get(
    "ELEVENLABS_KEY_PATH",
    os.path.expanduser("~/Documents/Skills LLMS/Claude/Skills/.heygen-credentials/elevenlabs-key.txt"),
))


def load_key() -> str:
    if not CRED_PATH.exists():
        sys.exit(f"ElevenLabs key not found at {CRED_PATH}. Paste it and retry.")
    return CRED_PATH.read_text().strip()


def synthesize(api_key: str, voice_id: str, settings: dict, text: str, out_path: Path) -> int:
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    payload = json.dumps({
        "text": text,
        "model_id": MODEL,
        "voice_settings": settings,
    }).encode()
    req = urllib.request.Request(url, data=payload, method="POST")
    req.add_header("xi-api-key", api_key)
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "audio/mpeg")
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = resp.read()
    out_path.write_bytes(data)
    return len(data)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--config", required=True, help="Path to trailer VO config JSON")
    p.add_argument("--out-dir", required=True, help="Output directory for MP3s")
    args = p.parse_args()

    cfg = json.loads(Path(args.config).read_text())
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    api_key = load_key()

    for line in cfg["lines"]:
        voice_key = line["voice"]
        if voice_key not in VOICES:
            print(f"FAIL  unknown voice '{voice_key}' (options: {list(VOICES)})")
            continue
        voice = VOICES[voice_key]
        out_path = out_dir / line["filename"]
        try:
            size = synthesize(api_key, voice["id"], voice["settings"], line["text"], out_path)
            print(f"OK    {line['filename']}  {size/1024:.1f}KB  ({voice_key})")
            time.sleep(0.5)  # polite to the API
        except Exception as e:
            print(f"FAIL  {line['filename']}  {type(e).__name__}: {str(e)[:80]}")


if __name__ == "__main__":
    main()
