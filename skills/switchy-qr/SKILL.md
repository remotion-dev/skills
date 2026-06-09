---
name: switchy-qr
description: "Generate a tracked QR code for a real-estate postcard via Switchy. Built for Peter (Jason) — the ONLY job is: take a finished postcard and produce a scannable QR code that points to a tracked Switchy short link (with the right landing page, UTM, folder, and retargeting pixels already set), then hand back the QR PNG to embed in the postcard. Use this skill ANY time the user says: generate a QR code for this postcard, make a postcard QR, QR for the mailer, tracked QR, Switchy QR, create the postcard link, or uploads a postcard and asks for a QR. This is the lightweight QR-only companion to the full switchy-engine skill (analytics/dashboard live there, not here)."
---

# Switchy QR (postcard QR generator) — for Peter / Jason

**What this does, in one line:** you finish a postcard, say *"generate a QR code for
this postcard,"* and Claude creates a tracked Switchy link + QR for you to drop into
the design. Switchy then tracks every scan and adds scanners to Graeham's ad audience.

**You only do two things:** (1) say the command + upload the postcard, and (2) log
into Switchy once when asked. Claude does the rest.

---

## One-time setup

You need access to Graeham's Switchy. Either:
- **Your own login** — Graeham adds you as a team member in Switchy (Account → Team),
  OR
- **The shared login** Graeham gives you.

And the Switchy API token so Claude can create the link automatically. Graeham will
provide it; save it in a file named `switchy-token.txt` in your Cowork Skills folder,
OR set an environment variable `SWITCHY_API_TOKEN`. (Never paste the token into chat.)

---

## How to generate a QR (every postcard)

1. Finish the postcard in Canva.
2. In Cowork say: **"Generate a QR code for this postcard"** and upload the postcard
   (PDF or image). Tell Claude the **mail date** (e.g. 2026-06-01) and, if it's not the
   usual home-value report, the **destination** (default is the home-value page).
3. Claude runs `scripts/create_postcard_link.py` to create the tracked link — correct
   landing page + UTM + the **"Post card qr"** folder + Graeham's Meta/Google pixels,
   all set automatically.
4. Claude opens Switchy in Chrome. **You log in once** when prompted (Claude can't type
   passwords or solve the "I'm not a robot" check — that part is you).
5. Claude finds the new link, opens its QR, clicks **Download as PNG**, and gives you
   the QR file.
6. Drop the QR into the Canva postcard, export, done. (The QR keeps working even if the
   landing page changes later — it's swappable on Switchy's side.)

---

## What Claude runs to make the link

```bash
python scripts/create_postcard_link.py --date 2026-06-01 --hook "Last 5 Homes"
# optional: --dest https://graehamwatts.com/evaluation  --market epa  --archetype anti_zestimate
```
It prints the short URL (e.g. `hi.switchy.io/epa-comps-0601`). Then Claude downloads the
QR for that link from the Switchy dashboard (Chrome). See the script header for details.

## Naming (handled automatically — just so you recognize it in Switchy)
- Link title: `Postcard <MARKET> <YYYY-MM-DD> — <hook> (home value)`
- Folder: `Post card qr`  ·  Tags: `postcard, qr, consumer, <market>, <date>`
- UTM: `utm_source=postcard&utm_medium=direct_mail&utm_campaign=<market>_<mmddyy>&utm_content=<archetype>`

> Need scan numbers, the dashboard, or retargeting reports? That's the full
> **switchy-engine** skill (Graeham's). This skill is QR-only on purpose.
