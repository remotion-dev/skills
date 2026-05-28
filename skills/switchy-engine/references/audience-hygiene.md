# Audience Hygiene — what to pixel, what to skip, how to segment

**The trap:** pixeling indiscriminately. A retargeting audience is only as good as
who's in it. Two ways to wreck it:

1. **Tiny audiences.** Below ~100 you can't target at all (Meta floor). Below
   ~1,000 the algorithm has too little to optimize and you overpay. A postcard
   slug with 95 scans isn't an audience yet — it's noise.
2. **Wrong people.** Other agents, vendors, lenders, title reps, and your own team
   clicking an email signature or LinkedIn link get pixeled as if they were
   buyers/sellers. You then spend ad dollars showing listing ads to your title rep.
   This drags CTR down, raises CPMs, and corrupts lookalike seeds built from the
   audience.

## Pixel vs. skip, by surface

**PIXEL (consumer / prospect-facing):**
- EPA Report newsletter, GHL SMS, single-property & listing pages
- GBP posts + secondary links, Zillow/Realtor.com profiles, Nextdoor
- Instagram/Facebook bios, YouTube description/pinned/channel links
- All offline QR → postcards, yard riders, open-house flyers & sign-in, mailers,
  event banners, window cards

**SKIP the pixel (track clicks only, or don't wrap):**
- **Email signature** — every email to a vendor/agent/escrow gets them pixeled.
  Track-only or omit. If wrapped, hard-tag `b2b`/`mixed` and exclude.
- **LinkedIn** — predominantly B2B/peer traffic. Track-only or exclude from
  consumer audiences.
- **Business cards handed to peers**, networking events aimed at the industry.
- **Sphere / past-client touches (PCFS)** — known people; retargeting them wastes
  spend. Measure engagement, don't build ad audiences from them.

## How to segment so junk can be excluded

The mechanism is **tags on every minted link** (the engine enforces this):

- `audience-class`: `consumer` | `prospect` | `b2b` | `mixed`
- `surface`: gbp / newsletter / postcard / listing / signature / openhouse / …
- `campaign`: optional (e.g. `94303-spring-farm`)

Then in the ad platform build audiences from the **clean** classes only:

1. **Separate Switchy pixels or events by class where possible.** Simplest robust
   pattern: use a distinct destination-path or event per `audience-class` so the
   Meta/GA audience rule can include `consumer` traffic and exclude `b2b`. (Switchy
   fires the pixel on redirect; the cleanest split is one pixel + a class-specific
   URL parameter, or separate links per class.)
2. **Build the retargeting audience = `consumer` + `prospect` sources only.**
   Never include `b2b`/`mixed`.
3. **Maintain a standing EXCLUSION audience** of known agents/vendors/team (upload
   their emails as a Meta custom audience) and exclude it from every campaign. This
   catches B2B people even when they slip through a consumer surface.
4. **Min-size gate before spending.** The analytics script flags any audience under
   100 (untargetable) and 100–999 (fold into a combined audience). Don't run a
   campaign against a sub-1,000 standalone audience — merge by surface first
   (e.g. all `listing` slugs → one "listing-viewers" audience).
5. **Lookalike seeds from clean audiences only.** A lookalike built off a polluted
   seed inherits the pollution at scale — the most expensive version of the mistake.

## One-line policy for the engine
> Pixel consumer/prospect surfaces; track-only the B2B/known ones; tag every link
> with `audience-class`; build ad audiences from `consumer`+`prospect` minus a
> standing vendor/agent exclusion list; never spend against a sub-1,000 standalone.
