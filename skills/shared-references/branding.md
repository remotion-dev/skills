# Graeham Watts — Brand Reference

Single source of truth for all brand visual rules across every skill.
Reference this file from any new skill instead of duplicating brand specs.

## Color Palette

| Token | Hex | Usage |
|---|---|---|
| `--u-navy` | `#1B2A4A` | Structural — backgrounds, headers, body text on light backgrounds |
| `--u-gold` | `#C5A258` | Brand accent — CTAs, badges, opportunity scores, brand moments only |
| `--u-green` | `#2e7d32` | Semantic positive — "ready", "completed", "passed" |
| `--u-red` | `#c62828` | Semantic negative — "error", "failed", "alert" |
| `--u-bg` | `#F7F5EF` | Page background (cream) |
| `--u-card` | `#FFFFFF` | Card / surface background |
| `--u-border` | `rgba(27, 42, 74, 0.10)` | Card borders, dividers |
| `--u-text` | `#1B2A4A` | Body text on light backgrounds |
| `--u-muted` | `#5a6478` | Secondary text, metadata |

**Gold is sacred.** Use it for: primary CTA buttons, opportunity score values, the
PICKED/SELECTED tag, hero accents, brand identity moments. Maximum ~10
instances per dashboard. Don't use it for general UI chrome — use navy and
gray for that.

## Typography

- **Display:** `Plus Jakarta Sans` (weights 600, 700, 800)
- **Body:** `DM Sans` (weights 400, 500, 700)
- **Mono / code:** system mono (`ui-monospace, Consolas, monospace`)

Both fonts come from Google Fonts. Always include a fallback chain:
```css
font-family: 'Plus Jakarta Sans', 'DM Sans', system-ui, sans-serif;
font-family: 'DM Sans', system-ui, sans-serif;
```

## Component shapes

- **Card border-radius:** `12px`
- **Button border-radius:** `8px`
- **Pill / badge border-radius:** `20px`
- **Card padding:** `16-22px`
- **Card shadow:** `0 2px 10px rgba(27, 42, 74, 0.06)` (light) or `0 6px 20px rgba(27, 42, 74, 0.10)` (lifted)

## Dashboard / email overlay stylesheet

For HTML output, see `scripts/unify_final.py`'s `CONSOLIDATED_CSS_V2` constant
— that's the canonical implementation of every rule above.

## Identity strings

These strings appear at the bottom of every client-facing artifact. Copy
exactly:

- Name: `Graeham Watts`
- Title: `REALTOR`
- Brokerage: `Intero Real Estate`
- DRE: `01466876`
- Email: `graehamwatts@gmail.com`
- Website: `graehamwatts.com`

## Markets

- Primary: East Palo Alto
- Secondary: Redwood City, Palo Alto, Menlo Park, San Mateo County, Peninsula

## Fair Housing guardrails

Always present in any content output:
- No demographic descriptors (race, religion, national origin, family status,
  disability)
- No "safe / good / family-friendly / up-and-coming" as proxies for
  demographic signaling
- No school rankings as a primary selling point
- Public safety content permitted ONLY when framed as statistics + public
  policy, never as neighborhood character proxy

---

*Update history: created April 21, 2026 to consolidate brand specs from
`content-creation-engine/SKILL.md` and the dashboard CSS overlay.*
