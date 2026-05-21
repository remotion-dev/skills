#!/usr/bin/env bash
# Renders ONE still PNG from any composition - used for fast design
# iteration (font/gold/spacing comparison sheets) without waiting on a
# full ~2-minute video render.
#
# Same browser auto-detection as render.sh - see that file for why.
#
# Usage:  bash still.sh <CompositionId> <output.png> [frame]
# Example: bash still.sh GoldVariant-rich-gold out/check.png 0
set -e

COMP="${1:?usage: bash still.sh <CompositionId> <output.png> [frame]}"
OUT="${2:?usage: bash still.sh <CompositionId> <output.png> [frame]}"
FRAME="${3:-0}"

BROWSER=$(find /opt/pw-browsers -name headless_shell -type f 2>/dev/null | head -1)
if [ -z "$BROWSER" ]; then
  BROWSER_FLAG=""
else
  BROWSER_FLAG="--browser-executable=$BROWSER"
fi

mkdir -p "$(dirname "$OUT")"
npx remotion still src/index.ts "$COMP" "$OUT" --frame="$FRAME" $BROWSER_FLAG
echo "Done: $OUT"
