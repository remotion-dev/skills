# HTML Report Template — Structure & Build Guide

Use `assets/report_template.html` as the base. This doc explains how to fill it in, the Python/jinja-style placeholders to swap out, and the card-rendering pattern.

## Output filename

```
Off_Market_<City_Underscored>_<DD-MM-YYYY>.html
```

Examples:
- `Off_Market_Menlo_Park_16-04-2026.html`
- `Off_Market_East_Palo_Alto_02-05-2026.html`

Place output under: `outputs/off-market-<city-slug>-<DD-MM-YYYY>/`

## Placeholders in `assets/report_template.html`

The template uses plain-text placeholders (no Jinja needed — simple string replacement):

| Placeholder | Replace with |
|-------------|--------------|
| `{{CITY_UPPERCASE}}` | `MENLO PARK` |
| `{{REPORT_DATE}}` | `April 16, 2026` (use `%B %d, %Y` format) |
| `{{INTRO_PARAGRAPH}}` | The off-market disclosure paragraph (see below) |
| `{{CARDS_HTML}}` | The assembled card markup — concatenate all cards here |
| `{{CARD_COUNT}}` | Integer, number of properties (used in subtle header text) |
| `{{FOOTER_HTML}}` | Standard Graeham contact line (see below) |

### Intro paragraph (default)

```
As part of our ongoing market research, we've identified the following properties
that are not yet available to the general public. These off-market opportunities
are exclusively available through agent networks.
```

### Footer (default)

```
Graeham Watts  |  Intero Real Estate  |  DRE #01466876  |  650-308-4727  |  graehamwatts@gmail.com  |  www.graehamwatts.com
```

## Card markup pattern

Each property card follows this structure. Escape HTML entities in address etc.

```html
<article class="property-card">
  <div class="photo-wrap">
    <img src="{MAIN_PHOTO_URL}" alt="Photo of {ADDRESS}">
  </div>
  <div class="card-body">
    <h3 class="address">{ADDRESS}</h3>
    <p class="stats">
      <span>{BEDS} Beds</span>
      <span class="dot">·</span>
      <span>{BATHS} Baths</span>
      <span class="dot">·</span>
      <span>{SQFT_FORMATTED}</span>
      <span class="dot">·</span>
      <span>{LOT_FORMATTED}</span>
      {YEAR_BUILT_SPAN}
    </p>
    <div class="gold-rule"></div>
    <p class="price">Estimated price around ${ESTIMATED_PRICE}</p>
    {THUMBNAILS_BLOCK}
  </div>
</article>
```

Formatting helpers:

| Field | Format |
|-------|--------|
| `{BEDS}` | Integer as-is |
| `{BATHS}` | One decimal if not whole (`2.5`), else integer |
| `{SQFT_FORMATTED}` | `{:,} SqFt` → `"1,850 SqFt"` |
| `{LOT_FORMATTED}` | If acres: `"0.25 Acre Lot"`. If sqft: `"{:,} SqFt Lot"` → `"6,250 SqFt Lot"` |
| `{YEAR_BUILT_SPAN}` | If available, `<span class="dot">·</span><span>Built {YEAR}</span>`. Else empty string. |
| `{ESTIMATED_PRICE}` | List price rounded per the rules in SKILL.md, formatted with commas (no dollar sign — the template has it) |
| `{THUMBNAILS_BLOCK}` | If 1–2 extra photos: `<div class="thumbs"><img src="..."><img src="..."></div>`. Else empty string. |

## Price rounding helper (Python)

```python
def round_price(price: int) -> int:
    if price < 2_000_000:
        return round(price / 25_000) * 25_000
    if price < 5_000_000:
        return round(price / 50_000) * 50_000
    return round(price / 100_000) * 100_000
```

## Example data → example card

Input:
```json
{
  "address": "123 Laurel St, Menlo Park, CA 94025",
  "beds": 3,
  "baths": 2.5,
  "sqft": 1850,
  "lot_sqft": 6250,
  "year_built": 1962,
  "list_price": 2175000,
  "main_photo": "https://cdn.mlslistings.com/photos/xyz.jpg",
  "extra_photos": []
}
```

Output card:
```html
<article class="property-card">
  <div class="photo-wrap">
    <img src="https://cdn.mlslistings.com/photos/xyz.jpg" alt="Photo of 123 Laurel St, Menlo Park, CA 94025">
  </div>
  <div class="card-body">
    <h3 class="address">123 Laurel St, Menlo Park, CA 94025</h3>
    <p class="stats">
      <span>3 Beds</span>
      <span class="dot">·</span>
      <span>2.5 Baths</span>
      <span class="dot">·</span>
      <span>1,850 SqFt</span>
      <span class="dot">·</span>
      <span>6,250 SqFt Lot</span>
      <span class="dot">·</span>
      <span>Built 1962</span>
    </p>
    <div class="gold-rule"></div>
    <p class="price">Estimated price around $2,175,000</p>
  </div>
</article>
```

($2,175,000 is already a $25k-clean number, so no rounding shift needed in this example.)

## Empty-results card

When zero Members Only listings match, emit ONE card in place of `{{CARDS_HTML}}`:

```html
<article class="property-card empty-card">
  <div class="card-body" style="padding:48px 32px;text-align:center;">
    <h3 class="address" style="margin-bottom:12px;">No off-market matches — yet.</h3>
    <p class="stats" style="line-height:1.7;">
      No off-market properties matched your criteria in {CITY} as of {DATE}.
      I'll keep watching the network — off-market inventory moves fast, and I'll reach out as soon as something fits.
    </p>
  </div>
</article>
```

## Quality checklist before saving

- [ ] Header renders with gold Graeham Watts logo + city + date
- [ ] Intro paragraph is present
- [ ] Cards render in a 2-column grid on desktop, 1 column on mobile
- [ ] Every card has a working photo (no broken image icons)
- [ ] Every card shows "Estimated price around $X" — NEVER a raw MLS price
- [ ] No MLS numbers, no "Listing courtesy of..." text, no MLS logos
- [ ] Footer with Graeham's contact info is at the bottom
- [ ] Google Fonts load (Montserrat + Inter)
- [ ] File is self-contained — opens correctly when double-clicked outside of Cowork
