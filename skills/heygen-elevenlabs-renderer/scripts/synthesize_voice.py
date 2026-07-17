#\!/usr/bin/env python3
"""
ElevenLabs TTS — synthesize a v5.4 SSML script into MP3 using Graeham's voice clone.

Usage:
    python3 synthesize_voice.py --text-file script.ssml.txt --out audio.mp3
    python3 synthesize_voice.py --text "Hello world" --out audio.mp3
"""
import argparse
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

CRED_DIR = Path(os.environ.get(
    "CLAUDE_CREDENTIALS_DIR",
    os.path.expanduser("~/Documents/Skills LLMS/Claude/Skills/.heygen-credentials")
))
REGISTRY = Path(__file__).parent.parent / "references" / "registry.json"

def load_key():
    key_file = CRED_DIR / "elevenlabs-key.txt"
    if not key_file.exists():
        sys.exit(f"ElevenLabs key not found at {key_file}. Paste it and retry.")
    return key_file.read_text().strip()

def load_defaults():
    if REGISTRY.exists():
        return json.loads(REGISTRY.read_text()).get("defaults", {})
    return {
        "elevenlabs_voice_id": "Pa3vOYQHHpLJn1Tf7hnP",
        "elevenlabs_model": "eleven_multilingual_v2",
    }


_DASH_RE = re.compile(r"\s*[—–]\s*")

def normalize_for_tts(text):
    """Deterministic pre-pass that prevents the most common ElevenLabs garbles.
    Strips em/en dashes (#1 artifact source) and ' & ', preserving <break .../>
    and [audio] tags untouched. Number/currency spelling is handled by
    apply_text_normalization='on' on the API side."""
    parts = re.split(r"(<[^>]+>|\[[^\]]+\])", text)
    for i, seg in enumerate(parts):
        if i % 2 == 0:
            seg = _DASH_RE.sub(". ", seg)
            seg = re.sub(r"\s&\s", " and ", seg)
            parts[i] = seg
    out = "".join(parts)
    out = re.sub(r"\.\s*\.\s*\.", "...", out)
    out = re.sub(r"[ \t]{2,}", " ", out)
    return out

def synthesize(text, out_path, voice_id=None, model=None, stability=0.5, similarity=0.75, style=0.0, normalize=True):
    key = load_key()
    defaults = load_defaults()
    voice_id = voice_id or defaults["elevenlabs_voice_id"]
    model = model or defaults.get("elevenlabs_model", "eleven_multilingual_v2")

    if normalize:
        text = normalize_for_tts(text)

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}?output_format=mp3_44100_128"
    body = json.dumps({
        "text": text,
        "model_id": model,
        "apply_text_normalization": "on",  # spell out numbers/currency; ok on multilingual_v2 (Flash v2.5 needs Enterprise)
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity,
            "style": style,
            "use_speaker_boost": True,
        },
    }).encode()

    req = urllib.request.Request(url, data=body, method="POST", headers={
        "xi-api-key": key,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    })
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = resp.read()

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    Path(out_path).write_bytes(data)
    return len(data)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--text-file", help="Path to SSML text file")
    p.add_argument("--text", help="Inline text (for quick tests)")
    p.add_argument("--out", required=True, help="Output MP3 path")
    p.add_argument("--voice-id", help="Override voice_id")
    p.add_argument("--model", help="Override model_id")
    p.add_argument("--no-normalize", action="store_true", help="Skip the dash/symbol normalization pre-pass")
    args = p.parse_args()

    if not (args.text_file or args.text):
        sys.exit("Provide --text-file or --text")

    text = Path(args.text_file).read_text() if args.text_file else args.text
    n = synthesize(text, args.out, voice_id=args.voice_id, model=args.model, normalize=not args.no_normalize)
    print(f"Wrote {args.out} ({n} bytes)")

if __name__ == "__main__":
    main()
