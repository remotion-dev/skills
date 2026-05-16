#!/usr/bin/env python3
"""
DEPRECATED — This in-sandbox transcription module does not work in Cowork.

The Cowork bash sandbox is allowlisted to only github.com and pypi.org.
It cannot reach YouTube, Instagram, TikTok, Deepgram, or HuggingFace.

Transcription happens via:
  1. The local CLI on the user's Windows machine:
     skills/transcript-repurposer/scripts/transcribe_local.py
  2. Claude in Chrome for YouTube's built-in transcript panel
  3. The Property OS backend service (see PROPERTY_OS_SPEC.md)

Do NOT call this file. See skills/transcript-repurposer/references/00-auto-transcribe.md
for the current ingestion architecture.
"""
import sys
print(__doc__, file=sys.stderr)
sys.exit(1)
