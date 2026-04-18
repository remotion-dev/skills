#!/usr/bin/env bash
# setup.sh — Ensure HeyGen CLI is installed and auth is working.
# Idempotent: safe to run every session. Installs to ~/.local/bin/heygen if missing.

set -euo pipefail

export PATH="$HOME/.local/bin:$PATH"

# 1. Check API key presence (don't print the key)
if [ -z "${HEYGEN_API_KEY:-}" ]; then
  echo "ERROR: HEYGEN_API_KEY is not set." >&2
  echo "Set it with: export HEYGEN_API_KEY='sk_V2_...'" >&2
  echo "Grab a key at https://app.heygen.com/api" >&2
  exit 1
fi

# 2. Install CLI if missing
if ! command -v heygen >/dev/null 2>&1; then
  echo "HeyGen CLI not found. Installing..."
  curl -fsSL https://static.heygen.ai/cli/install.sh | bash
  export PATH="$HOME/.local/bin:$PATH"
fi

# 3. Verify install
VERSION=$(heygen --version 2>/dev/null | head -1 || echo "unknown")
echo "HeyGen CLI: $VERSION"

# 4. Verify auth with a minimal call (list 1 avatar group — cheap)
#    Don't fail hard if this errors — just warn, as avatar listing can fail for valid reasons
#    while video creation still works.
if heygen user me get 2>/dev/null >/dev/null; then
  echo "Auth: OK"
else
  echo "Warning: 'heygen user me get' did not succeed. Proceeding anyway — video submission will reveal auth issues conclusively." >&2
fi

echo "Ready."
