Subject: New skill for you — auto-generate tracked QR codes for our postcards (Switchy)

Hey Peter,

Setting you up with a new Cowork skill called **switchy-engine**. The whole point:
you make the postcard, and Claude does the QR + tracking automatically so we can
see how many people scan each mailer and retarget them with ads.

---

## What it does
When you give Claude a finished postcard and ask for a QR code, it will:
1. Create a short, trackable link in our Switchy account pointing to the right
   landing page (e.g. the home-value page), with tracking tags baked in.
2. Attach our Meta + Google pixels so everyone who scans gets added to our ad
   retargeting audience.
3. Generate the QR code and download it for you to drop into the postcard.
4. File it neatly in Switchy under the "Post card qr" folder with a clear name.

Then every Monday we get a report of how many scans each postcard/link got.

---

## How to install it
**Easiest:** open the attached file **`switchy-engine.skill`** and click
**"Save skill"** — that installs it into your Cowork.

*(Once Graeham pushes it to GitHub, you'll also be able to pull it from the
`Graehamwatts/skills` repo under `skills/switchy-engine`. The attached file works
right now either way.)*

---

## How to use it (your weekly postcard workflow)
1. Build the postcard in Canva like normal.
2. Open Cowork and say: **"Generate a QR code for this postcard"** and upload the
   postcard PDF/image.
3. Claude logs into Switchy, makes the tracked link + QR, and hands you the QR PNG.
4. Drop the QR into the postcard, export, send to print.

That's it. Claude handles the link, the UTM tracking, the pixels, and the filing.

---

## Switchy login (Graeham will fill this in before sending)

> **Graeham — paste the Switchy access for Peter here. Do NOT send the password in
> plain email if you can avoid it.** Two options:
>
> **Option A (recommended, safer):** In Switchy → Account → Team → "Add team
> member", invite Peter's email so he gets his OWN login. Then he generates his own
> API key under Settings → API key.
>
> **Option B (shared login):** share the workspace login another way (password
> manager / phone), and the API key named **"claude-engine"** is already created
> under Settings → API key.
>
> _Login: ____________________   ·   Password: (send separately) _____________________

---

## Naming convention (so every QR is easy to identify)
Claude will name things like this automatically — just so you know what you're
looking at in Switchy:
- **Link name:** `Postcard EPA 2026-06-01 — Last 5 Homes (home value)`
- **Short link:** `hi.switchy.io/epa-comps-0601`
- **Folder:** `Post card qr`
- **UTM:** `utm_source=postcard · utm_medium=direct_mail · utm_campaign=epa_06_01_26 · utm_content=anti_zestimate`

Date format is YYYY-MM-DD so they sort correctly.

---

Any issues installing, text me. Once you're in, do a test run on the June 1st EPA
card — it's already created in Switchy so you can see how it looks.

Thanks,
Graeham
