# CTA Router — CTA Type → Landing Page URL

When a user picks a CTA type for a card, look up the URL here. If the URL is `[NOT SET]`, ask the user once and CACHE it by editing this file. Never ask twice for the same CTA type.

## Cached URLs

| CTA Type | Landing URL | Use for |
|---|---|---|
| Home valuation | `[NOT SET — ask user, then cache here]` | "What's my home worth", equity check, precision equity audit, free home valuation |
| Testimonials | `[NOT SET — ask user, then cache here]` | Social proof / reviews CTAs |
| Free report (market) | `[NOT SET — ask user, then cache here]` | Neighborhood report, market report, free download |
| Free report (AI score) | `[NOT SET — ask user, then cache here]` | AI search visibility report, property AI score |
| Thinking of selling | `[NOT SET — ask user, then cache here]` | Pre-listing consultation, seller guide |
| Off-market buyers | `[NOT SET — ask user, then cache here]` | Buyer-pool angle, "I have a list of buyers" |
| Call / text Graeham | `tel:+16503084727` or `sms:+16503084727` | Direct contact CTA (no landing page needed) |
| Custom | Ask user each time | One-off campaigns |

## How to update

When asking the user for a missing URL, after they provide it:

1. Edit this file using the Edit tool
2. Replace `[NOT SET — ask user, then cache here]` with the URL
3. Tell the user: "Cached [URL] as your default [CTA type] target. Won't ask again."

## QR code generation

Once you have the URL, generate the QR code at print time. Recommended approach:

**Python (via bash):**
```bash
pip install qrcode pillow --break-system-packages --quiet
python -c "import qrcode; qr=qrcode.QRCode(box_size=10, border=2); qr.add_data('$URL'); qr.make(); img=qr.make_image(); img.save('/sessions/inspiring-awesome-hawking/mnt/outputs/qr.png')"
```

Then embed the resulting PNG into the postcard HTML in place of the stylized SVG placeholder.

**UTM recommendation (optional but smart):**
Add UTM params so Graeham can track which postcard drove which conversions:
```
?utm_source=postcard&utm_medium=direct_mail&utm_campaign=epa_[mm_dd_yy]&utm_content=[archetype]
```

Example:
```
https://graehamwatts.com/value?utm_source=postcard&utm_medium=direct_mail&utm_campaign=epa_06_01_26&utm_content=neighbor_envy
```

## URL hygiene

- Always use HTTPS (more reliable QR scanning on iOS)
- Keep URLs under 100 characters or QR density gets too high to scan from arm's length
- If URL is long, use a URL shortener (bit.ly / rebrand.ly) BUT lose UTM tracking — tradeoff to discuss with user

---

## Switchy integration (added 2026-05-28) — pixeled, scan-tracked QR targets

The QR target should be a **Switchy short link**, not the raw landing URL. The short
link redirects to the landing URL (with UTM) AND fires the retargeting pixel + counts
the scan on the redirect layer — making every postcard drop a retargeting audience,
not just a one-way mailer. Engine: `skills/switchy-engine`.

**At print time:**
1. Resolve the landing URL from the table above (e.g. Home valuation).
2. Append UTM: `?utm_source=postcard&utm_medium=direct_mail&utm_campaign=epa_[mm_dd_yy]&utm_content=[archetype]`.
3. Mint a Switchy link: `url` = the UTM'd landing URL, `tags:["postcard","qr","consumer","epa_[mm_dd_yy]"]`, `pixels` from `shared-references/switchy.json`. (REST POST https://api.switchy.io/v1/links/create, header `Api-Authorization: <token>`.)
4. Generate the QR encoding the **Switchy short URL**.
5. Report scans later via `switchy-engine/scripts/switchy_analytics.py`.

If the token isn't active yet, fall back to a QR on the UTM'd landing URL (GA tracks
sessions; no pixel/scan layer). The printed QR can't change later, so mint the Switchy
link BEFORE the print run whenever possible.
