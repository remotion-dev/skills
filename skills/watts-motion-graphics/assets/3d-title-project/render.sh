#!/usr/bin/env bash
# Renders the 3D title card to an alpha-channel ProRes 4444 .mov.
#
# WHY THIS SCRIPT EXISTS: the headless Chromium shell that Remotion needs
# to render lives at a path with a VERSION NUMBER in it
# (e.g. /opt/pw-browsers/chromium_headless_shell-1194/...). That number
# changes between Claude sessions. Hardcoding it breaks the render in any
# other session. This script finds the shell dynamically instead.
set -e

MODE="${1:-landscape}"   # landscape | portrait

# locate the pre-installed headless shell (version dir varies per session)
BROWSER=$(find /opt/pw-browsers -name headless_shell -type f 2>/dev/null | head -1)
if [ -z "$BROWSER" ]; then
  echo "WARN: no pre-installed headless shell found under /opt/pw-browsers."
  echo "      Letting Remotion resolve a browser itself (may try to download)."
  BROWSER_FLAG=""
else
  echo "Using browser: $BROWSER"
  BROWSER_FLAG="--browser-executable=$BROWSER"
fi

if [ "$MODE" = "portrait" ]; then
  COMP="TitlePortrait"
  OUT="out/watts-3d-title-portrait.mov"
else
  COMP="TitleLandscape"
  OUT="out/watts-3d-title-landscape.mov"
fi

mkdir -p out
npx remotion render src/index.ts "$COMP" "$OUT" \
  --codec=prores --prores-profile=4444 --pixel-format=yuva444p10le \
  $BROWSER_FLAG

echo "Done: $OUT"
