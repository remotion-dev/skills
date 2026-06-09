# GBP redirect policy + YouTube/own-site pixel redundancy

## Part A — Google Business Profile: can a Switchy link go there?

**Short answer: NOT in the primary website field. Yes in posts and secondary
links, with care.**

Google's Business links policy explicitly prohibits URLs that "redirect or
'refer' users to landing pages... other than those of the actual business," and
Google now runs automated link verification that removes violating links. Link
shorteners in the **primary website field** are a documented enforcement target —
there are real cases of booking/shortened links getting pulled (e.g. a contractor
losing a large share of Google-sourced leads when a redirect link was removed).
Google tolerates *short, clean* UTM strings but flags long/promotional ones.

**Verdict by GBP surface:**

| GBP surface | Switchy redirect OK? | What to do |
|---|---|---|
| **Primary website field** | ❌ High risk of auto-removal | Put your real domain (`graehamwatts.com`). Pixel it natively with the Meta/GA tags already on the site. Don't gamble your map-pack click here. |
| **Appointment / menu / "Links" fields** | ⚠️ Lower risk | A clean branded short link is usually fine; monitor for removal. Prefer your own domain with a tracked path if nervous. |
| **GBP Posts (update/offer/event)** | ✅ Safe | This is the right home for Switchy on GBP. Each post link is a fresh pixel hook. |

### GBP-driven use cases (every one pixels the clicker, then retargets)
- **GBP post link → YouTube channel/video:** every GBP clicker who lands on your
  pixeled redirect gets dropped into a custom audience *and* sent to a video.
  You retarget high-intent local searchers who watched your content. HIGH value —
  this is the headline play.
- **GBP post link → single-property page:** local searcher → listing → pixel →
  retarget with more listings / "what's my home worth."
- **GBP post link → EPA Report signup / home-value form:** capture + pixel.
- **GBP "appointment" link → GHL booking:** pixel before the booking page.
- **GBP product/services link → CMA landing page:** pixel seller-intent traffic.

> Net: GBP is one of Graeham's highest-intent traffic sources, but the pixel has
> to be captured through **posts and secondary links**, never the website field.
> The field stays clean; the posts do the retargeting work.

## Part B — YouTube & own-site links: is the pixel redundant?

**Yes — when a Switchy link points to Graeham's OWN already-pixeled site, the
pixel-drop is largely redundant**, because the site's own Meta/GA tags will pixel
that visitor the instant the page loads anyway. The Switchy pixel and the on-site
pixel capture nearly the same person.

But "redundant pixel" ≠ "useless link." Switchy still earns its place for four
non-pixel reasons:

1. **Per-source attribution.** A unique slug per surface (YT description vs. pinned
   comment vs. channel link vs. GBP) tells you *which* surface drove the visit —
   something a bare `graehamwatts.com` link buried among many can't.
2. **Swappable destination.** Change where a printed/published link points without
   editing the video, postcard, or sign. Critical for QR codes you can't reprint.
3. **Multi-pixel firing.** Fire Meta + Google + LinkedIn + Pinterest from one link
   even if the destination page only carries one or two of those tags.
4. **Pixel-fires-before-page-load.** The redirect pixels the visitor even if they
   bounce before the destination renders (slow connection, immediate back-tap) —
   capturing people the on-site pixel would miss.

### Per-surface recommendation

| Destination type | Is Switchy essential? | Why |
|---|---|---|
| **Non-owned platform** (YouTube watch page, Zillow, Nextdoor, a partner site) | **ESSENTIAL** | You can't put your pixel on someone else's page. The redirect is your only capture point. |
| **Your own pixeled site, and you want attribution / swap / multi-pixel** | **WORTH IT** | Pixel is redundant but the other three benefits stand. |
| **Your own pixeled site, single known placement, no swap needed** | **OPTIONAL** | Raw URL pixels them fine on load. Use Switchy only if you want the click count. |
| **Your own site, but link is on a QR / print you can't easily change** | **WORTH IT** | Swappable destination alone justifies it. |

**Rule of thumb for the engine:** if the destination is NOT a Graeham-owned
pixeled page → always wrap. If it IS → wrap only when you need attribution,
swappability, multi-pixel, or pre-load capture; otherwise the raw URL is fine.
