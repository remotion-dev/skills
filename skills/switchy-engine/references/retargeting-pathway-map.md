# Retargeting Pathway Map — every surface a Switchy link/QR can live

Legend — **Retargeting value**: HIGH = lots of net-new pixelable consumer traffic
you can't capture otherwise; MED = useful but smaller/partly redundant; LOW =
tiny, redundant, or audience-polluting. **Pixel?**: should this surface actually
drop people into a retargeting audience, or just track clicks?

| # | Surface | Traffic type | Retargeting value | Pixel? | Platform caveat |
|---|---|---|---|---|---|
| 1 | **GBP — primary website field** | High-intent local searchers | HIGH (the traffic) / N/A (can't pixel here) | ❌ raw domain only | Google auto-removes redirect/shortener links from the website field. Put the real site here; pixel it natively. |
| 2 | **GBP — "Links" / appointment / menu links** | High-intent local | HIGH | ✅ | Secondary links tolerate more; still keep them clean. Use Switchy here, not field #1. |
| 3 | **GBP — Posts (update/offer/event)** | High-intent local | HIGH | ✅ | Posts are the safest GBP home for a Switchy link. Each post link → pixel. |
| 4 | **Instagram bio link / link-in-bio** | Warm social, consumer | HIGH | ✅ | IG in-app browser sometimes limits 3rd-party cookies → lower match; pixel still fires server-friendly events. |
| 5 | **Facebook page bio / about link** | Warm social, consumer | HIGH | ✅ | FB pixel matches best here (same ecosystem). |
| 6 | **LinkedIn bio / featured link** | Mixed (agents, vendors, some clients) | LOW–MED | ⚠️ selective | Heavy B2B/agent traffic — tag `b2b`, EXCLUDE from consumer audiences. LinkedIn pixel available. |
| 7 | **TikTok bio link** | Cold-warm consumer | MED | ⚠️ click-only or GTM | **No native TikTok pixel in Switchy** — route via `gtm` or accept click tracking only. |
| 8 | **YouTube — video descriptions** | Warm consumer (already engaged) | MED–HIGH | ✅ (if non-owned dest) | If link points to your OWN pixeled site, pixel benefit is largely redundant (see gbp-and-youtube.md). Value = attribution + swappable + multi-pixel. |
| 9 | **YouTube — pinned comment** | Warm consumer | MED | ✅ | Same redundancy logic as #8. High CTR placement. |
| 10 | **YouTube — channel "Links" section** | Warm consumer | MED | ✅ | Persistent; good for a single evergreen tracked link. |
| 11 | **Email signature** | MIXED — clients, agents, vendors, title, lenders | LOW | ❌ skip pixel | Pollutes audiences with B2B. Track clicks only, or omit. Tag `b2b`/`mixed`, exclude. |
| 12 | **The EPA Report newsletter** | Warm consumer subscribers | HIGH | ✅ | Already opted-in; cleanest audience you have. Per-section links → per-topic audiences. |
| 13 | **GHL SMS / text campaigns** | Warm leads/prospects | HIGH | ✅ | SMS clicks open in-app browsers; match rate varies but intent is high. Keep slugs short for SMS. |
| 14 | **Single-property / listing pages** | High-intent buyers + neighbor-snoops | HIGH | ✅ | Goldmine — buyers AND likely future sellers (neighbors). Tag per listing. |
| 15 | **Zillow profile link** | High-intent consumer | HIGH | ✅ | Zillow may wrap/normalize outbound links; test the redirect survives. Non-owned-platform traffic you otherwise can't pixel. |
| 16 | **Realtor.com profile link** | High-intent consumer | HIGH | ✅ | Same as Zillow — confirm link isn't stripped. |
| 17 | **Postcards (QR)** — *currently Canva, no skill* | Cold-warm farm/geo consumer | MED–HIGH | ✅ | QR scan = pixel fire. Per-ZIP/per-drop slug = measurable direct mail + a retargeting audience from offline mail. Big unlock. |
| 18 | **Yard sign riders (QR)** | Cold-warm local drive-by | MED | ✅ | Scanners are physically in the neighborhood = prime seller/buyer geo audience. Per-sign slug. |
| 19 | **Open house flyers (QR)** | Warm in-person buyers | HIGH | ✅ | Self-selected high intent. Pair with #20. |
| 20 | **Open house sign-in (QR → form)** | Warm in-person | HIGH | ✅ | Pixel + lead capture in one scan. Tag `openhouse`. |
| 21 | **Business cards (QR)** | MIXED | LOW–MED | ⚠️ selective | Handed to clients AND peers. Two cards or two QRs: consumer vs. networking. Tag accordingly. |
| 22 | **Event banners / sponsorships (QR)** | Cold-warm local consumer | MED | ✅ | Per-event slug measures sponsorship ROI + builds a local audience. |

## Additional surfaces worth adding
| # | Surface | Traffic type | Value | Pixel? | Caveat |
|---|---|---|---|---|---|
| 23 | **Just-listed / just-sold mailers (QR)** | Cold farm consumer | MED–HIGH | ✅ | Same engine as postcards; per-campaign slug. |
| 24 | **Property video end-screens / pinned (HeyGen/Reels)** | Warm consumer | MED | ✅ | One tracked link reused across a video's surfaces. |
| 25 | **Nextdoor / community group posts** | Warm hyper-local | MED–HIGH | ✅ | Genuinely local; can't pixel Nextdoor natively, so Switchy is the only capture. |
| 26 | **Google Business / Apple Maps "appointment" links** | High-intent | MED | ✅ | Apple Maps tolerates redirects better than GBP field #1. |
| 27 | **PDF deliverables (CMA, disclosure summaries, listing presentations)** | Warm prospect | MED | ✅ | A tracked link/QR inside a CMA PDF tells you the seller re-opened it. |
| 28 | **QR on for-sale window cards / lockbox flyers** | Cold-warm drive-by | MED | ✅ | Same geo logic as yard riders. |
| 29 | **Sphere / past-client touch links (PCFS)** | Warm, known | MED | ⚠️ track-only | Known contacts — retargeting them is low-value; track engagement instead. |

## The highest-leverage unlocks (where Switchy earns its keep)
1. **Offline → online bridge (postcards, yard riders, open-house QR, mailers).**
   This is traffic you literally cannot pixel any other way. A QR scan turns a
   physical mail drop into a digital retargeting audience. #17–20, #23, #28.
2. **Non-owned platforms (Zillow, Realtor.com, Nextdoor, GBP posts, social bios).**
   You don't control these pages, so the redirect layer is your only pixel hook.
3. **Per-source attribution at scale (newsletter sections, listings, campaigns).**
   Tagging every minted link tells you which surface actually drives the audience.
