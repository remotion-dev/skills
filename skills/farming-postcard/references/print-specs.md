# Print Specs — Universal Mail Works Defaults

⚠️ **VERIFY BEFORE FIRST PRINT RUN** — UMW's exact spec sheet isn't locked in this skill. These are industry-standard 6×4 postcard defaults that should work for most vendors but should be confirmed with UMW before first print.

## Default specs

| Spec | Value | Notes |
|---|---|---|
| Trim size | 6" × 4" | Standard landscape postcard |
| Bleed | 0.125" each side | Total canvas: 6.25" × 4.25" |
| Safe zone | 0.25" from trim edge | Keep type/important elements inside this |
| Resolution | 300 DPI | For any raster images (headshots) |
| Color mode | CMYK | RGB will color-shift on press |
| File format | PDF/X-1a preferred, PDF/X-4 acceptable | Print-ready PDF standards |
| Fonts | Embedded or outlined | Outline to be safe (no font substitution risk) |

## PDF render pipeline

Step 1: Render HTML to PDF at 300 DPI using headless browser:

```bash
# Install once
pip install playwright --break-system-packages --quiet
python -m playwright install chromium

# Render
python -c "
from playwright.sync_api import sync_playwright
import sys
html_path = sys.argv[1]
pdf_path = sys.argv[2]
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(f'file://{html_path}')
    page.pdf(path=pdf_path, width='6.25in', height='4.25in', print_background=True, margin={'top':'0','bottom':'0','left':'0','right':'0'})
    browser.close()
" "[HTML_PATH]" "[PDF_PATH]"
```

Step 2: For production-grade CMYK conversion, the print shop will typically handle this. Optionally pre-convert using Ghostscript:

```bash
gs -dSAFER -dBATCH -dNOPAUSE -dNOCACHE -sDEVICE=pdfwrite \
   -sColorConversionStrategy=CMYK \
   -dProcessColorModel=/DeviceCMYK \
   -sOutputFile=output_cmyk.pdf input.pdf
```

## CMYK approximations of gold (`#C2A14E`)

If the printer asks for CMYK specifically:
- Coated stock: C:25 M:35 Y:75 K:5
- Uncoated stock: C:20 M:30 Y:70 K:0

These shift slightly between presses. If color match matters, ask UMW for a press proof on the first run.

## Vendor-specific notes

### Universal Mail Works (default)
- Specs to confirm: trim size options, bleed requirement, file format preference, EDDM eligibility
- Once confirmed, update this file with their official spec sheet URL/values
- Status: ⚠️ NOT YET CONFIRMED

### Wise Pelican (backup vendor)
- 6×4.25 standard (slightly taller than UMW default)
- 0.125" bleed
- PDF/X-1a or X-4
- Spec sheet: https://www.wisepelican.com/sizes-and-specifications

### Corefact (jumbo option)
- 6×9 jumbo postcards
- Triggers a different layout system entirely — current template is locked to 6×4 proportions

## EDDM (Every Door Direct Mail)

- Minimum size: 6.125" × 4.25" (UMW default fits)
- Must include EDDM indicia on the address panel
- Discounted postage rate (~$0.20/piece vs ~$0.34 First Class)
- EDDM doesn't allow targeted lists — entire postal routes only

## Pre-print checklist

Before sending any card to UMW for the first run:
- [ ] Verify UMW exact spec sheet (trim, bleed, resolution, format)
- [ ] Confirm CMYK color match with press proof if budget allows
- [ ] QR code tested with at least 3 phone cameras at arm's length
- [ ] Address panel + indicia placement confirmed with UMW
- [ ] Disclaimer text legible at print scale
- [ ] Phone number + URL spelled correctly (review twice)
- [ ] Graeham's name spelled correctly
