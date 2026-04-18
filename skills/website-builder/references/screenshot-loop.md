# Screenshot Loop

The review technique that catches problems code-only checks miss. After rendering HTML, take a screenshot, look at it, critique it like a designer would, fix the issues, screenshot again. Three iterations usually gets a page from "wrong" to "good".

This is the single highest-leverage quality step in this skill. Skipping it is what produces "looks fine in code but looks AI-generated in the browser" output.

## Why code review alone fails

When you read the HTML you're parsing structure (does this nav have the right links? is the grid 3-col?). When you see the screenshot you're parsing vibe (does this feel confident? is the hierarchy readable? does it look like a template?).

Vibe failures are invisible to code review. Screenshots surface them in under a second.

## Screenshot workflow

After writing or editing HTML:

1. Save the file in `outputs/`. Make sure CSS is inlined or linked correctly.
2. Run a headless browser screenshot via the bash sandbox. Preferred: Playwright (often preinstalled in the sandbox). Fallback: `chromium --headless`.
3. Save the screenshot into `outputs/screenshots/` with a suffix like `-v1.png`, `-v2.png` so versions don't overwrite.
4. Read the screenshot back using the file Read tool (images are supported).
5. Write a one-paragraph critique as if reviewing someone else's work. What's weak? What reads as AI-default? Any contrast/alignment issues?
6. Fix the issues. Re-screenshot. Compare v1 vs v2.
7. Stop when the critique is "this looks intentional and custom".

## Sample script

Use the bundled helper. See `scripts/screenshot.py` for the canonical version.

```bash
python3 scripts/screenshot.py outputs/index.html outputs/screenshots/index-v1.png --width 1440 --height 900
```

If Playwright isn't available, this fallback uses `chromium --headless` directly:

```bash
chromium --headless --disable-gpu --no-sandbox \
  --window-size=1440,900 \
  --screenshot=outputs/screenshots/index-v1.png \
  --virtual-time-budget=2000 \
  file:///absolute/path/to/outputs/index.html
```

`--virtual-time-budget=2000` waits for fonts and JS to settle. Without it, screenshots catch half-loaded state.

## What to critique

Use this checklist when reviewing the screenshot.

**Typography.** Are headers distinctive, not Inter/Roboto? Is the hero headline big enough (should feel slightly uncomfortable in size)? Is body text on a comfortable measure (≤65 chars)?

**Color.** Does the page use the `--brand-primary` color, not default black-on-white? Are status colors applied where they should be? Is anything low contrast?

**Hierarchy.** Can a viewer name the primary action within one second? Is the secondary action visually secondary (not same size as primary)?

**Layout variety.** Is every section the same centered column with 3 cards? If yes, break at least one section into an alternative layout.

**Background treatment.** Is there one chosen background effect (glass, orb, grid, noise)? Or zero? Or four stacked?

**Alignment tells.** Are elements vertically aligned (card heights matching, button baselines aligning)? AI layouts often have near-aligned-but-not-quite spacing.

**Copy.** Does any section still have "Welcome to our platform" or "Built for modern teams"? Rewrite before shipping.

## Multi-viewport check

Always screenshot at three widths: 1440 (desktop), 768 (tablet), 375 (mobile). A layout that looks clean on desktop often breaks at 768 — usually a flex row that should have wrapped.

```bash
for w in 1440 768 375; do
  python3 scripts/screenshot.py outputs/index.html outputs/screenshots/index-${w}.png --width $w
done
```

## When the page is interactive

Screenshots miss hover and click states. For interactive elements:

- Inject a script that forces `:hover` states via `element.classList.add('hover')` plus CSS like `.btn:hover, .btn.hover { ... }`.
- Or use Playwright's `page.hover(selector)` before screenshotting.

For multi-state flows (e.g., form validation), screenshot each state.

## Failure modes to watch for

**Fonts didn't load.** Screenshot shows fallback sans-serif. Check `<link rel="preconnect">` and Google Fonts URL. Wait longer (`--virtual-time-budget=4000`).

**JS didn't execute.** Animations haven't played, reveal elements stuck at `opacity: 0`. Add explicit wait or inject `document.querySelectorAll('.reveal').forEach(e => e.classList.add('visible'))` before screenshotting.

**Viewport capture, not full page.** Default screenshot is the viewport. For a full-page capture, use Playwright's `fullPage: true` or Chromium's `--window-size` matched to content height (less reliable — use Playwright).

## Iteration discipline

If you're on v4 and the page still feels off, stop iterating on CSS and change direction instead. Example: the layout is 3 centered cards in every section — that's the problem. Fix the architecture, not the padding.

Two red flags that mean "stop polishing, restart the section":
- Four rounds of tweaks haven't changed your gut reaction to the section.
- Every critique is about the same piece of the page — that piece is architecturally wrong.
