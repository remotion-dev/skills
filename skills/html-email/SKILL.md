---
name: html-email
description: "Generate beautiful, professional HTML emails and host them permanently on GitHub Pages. Use this skill ANY time the user needs a fancy, designed, or branded email that goes beyond plain text — strategy briefs, proposals, partnership pitches, confidential one-pagers, team briefings, listing launch emails, or any miscellaneous professional email that needs visual polish. Triggers include: 'fancy email', 'HTML email', 'professional email brief', 'designed email', 'send a nice email to', 'create an email brief', 'write a polished email', or any email where visual formatting would add impact. After generating the email, always push it to GitHub and return the hosted URL. Never save emails locally only — GitHub is the source of truth."
---

# HTML Email Skill

Generate and permanently host beautiful HTML emails via the `Graehamwatts/skills` GitHub repo.

## When To Use

- One-off professional emails that need visual design (strategy briefs, proposals, partnership asks)
- Confidential briefings sent to coaches, partners, or collaborators
- Any email where plain text won't do justice to the content
- Miscellaneous polished emails that don't fit into a named workflow (CMA, disclosure, etc.)

**Do NOT use for:** routine follow-ups, quick replies, MLS-required communications, or any email where plain text is fine.

---

## Output: What This Skill Produces

1. A designed HTML email file saved to the GitHub repo
2. A permanent hosted URL the user can share or open directly
3. A Gmail draft (if requested) with the HTML body

**Hosted URL format:**
```
https://graehamwatts.github.io/skills/emails/[YYYY-MM-DD]-[recipient-slug]-[subject-slug].html
```
Example:
```
https://graehamwatts.github.io/skills/emails/2026-04-11-brian-lopuk-zillow-strategy.html
```

---

## Step 1: Gather Information

Before generating, confirm these details (ask if not provided):

- **Recipient name and role** (e.g. Brian Lopuk, ads coach)
- **Subject / purpose** (e.g. strategy brief, partnership proposal)
- **Key content** (bullet points are fine — Claude will turn them into polished prose)
- **Tone** (e.g. collaborative, direct, formal, warm)
- **Confidentiality level** (add a confidential footer if sensitive)
- **Call to action** (what do you want the recipient to do?)

---

## Step 2: Generate the HTML Email

Build a complete, self-contained HTML file. Use this structure as the foundation — adapt the design for the context (don't make every email look the same):

### Design Rules
- Dark header with white text — establishes authority and makes the email feel like a document, not just a message
- Clean white body with generous padding (36–40px sides)
- One accent color tied to the content's emotional tone:
  - Strategy/insight → dark navy or slate
  - Urgency/action → amber or orange accent
  - Good news/results → green accent
  - Confidential/sensitive → dark charcoal
- Probability bars, metric cards, and tables where data is involved
- Never use Inter, Roboto, or Arial — use DM Sans, Plus Jakarta Sans, or Sora from Google Fonts
- Max width: 680px, centered, with a subtle box shadow
- Always include a footer with: "Confidential — not for distribution" (if sensitive) + "PropOS · Graeham Watts Real Estate"

### File Naming Convention
```
YYYY-MM-DD-[recipient-firstname-lastname]-[2-3-word-subject].html
```
Examples:
- `2026-04-11-brian-lopuk-zillow-strategy.html`
- `2026-03-22-jason-pantana-partnership-brief.html`
- `2026-05-01-krys-coaching-q2-review.html`

Use lowercase, hyphens only, no special characters.

---

## Step 3: Push to GitHub

Use the same PAT and git workflow as github-skill-sync. The token is the classic PAT named "Cowork Push" at https://github.com/settings/tokens.

```bash
# Clone the repo
git config --global user.email "graehamwatts@gmail.com"
git config --global user.name "Graehamwatts"
git clone https://Graehamwatts:<TOKEN>@github.com/Graehamwatts/skills.git /tmp/skills-repo-email

# Create the emails folder if it doesn't exist
mkdir -p /tmp/skills-repo-email/emails

# Write the HTML file
# (Python: write the generated HTML content to the file path)
python3 -c "
content = '''[FULL HTML CONTENT HERE]'''
with open('/tmp/skills-repo-email/emails/[FILENAME].html', 'w') as f:
    f.write(content)
"

# Commit and push
cd /tmp/skills-repo-email
git add emails/
git status --short
git commit -m "Add email: [recipient] — [subject] ([date])"
git push origin main
```

---

## Step 4: Confirm GitHub Pages Is Enabled

GitHub Pages must be enabled on the `Graehamwatts/skills` repo for hosted URLs to work.

**Check once, then it's permanent:**
1. Go to: https://github.com/Graehamwatts/skills/settings/pages
2. Under "Source" → select "Deploy from a branch"
3. Branch: `main` / Folder: `/ (root)`
4. Click Save
5. Wait 2–3 minutes, then visit: `https://graehamwatts.github.io/skills/`

If already enabled, skip this step entirely.

---

## Step 5: Return the Result

After pushing, confirm to the user:

```
✅ Email saved and hosted.

Recipient: [Name]
Subject: [Subject]
Hosted URL: https://graehamwatts.github.io/skills/emails/[filename].html
GitHub file: https://github.com/Graehamwatts/skills/blob/main/emails/[filename].html

The email is available 24/7 at the hosted URL above.
Would you like me to also create a Gmail draft to [recipient email]?
```

---

## Cleanup Command

When the user says "delete old emails", "clean up HTML emails older than X months", or "purge emails":

```bash
# Clone fresh
git clone https://Graehamwatts:<TOKEN>@github.com/Graehamwatts/skills.git /tmp/skills-repo-cleanup
cd /tmp/skills-repo-cleanup

# List emails with dates (parsed from filename)
python3 << 'EOF'
import os
from datetime import datetime, timedelta

cutoff_months = 6  # change this based on user request
cutoff = datetime.now() - timedelta(days=cutoff_months * 30)
emails_dir = "/tmp/skills-repo-cleanup/emails"

if not os.path.exists(emails_dir):
    print("No emails folder found.")
else:
    deleted = []
    kept = []
    for f in os.listdir(emails_dir):
        if not f.endswith('.html'):
            continue
        try:
            date_str = f[:10]  # YYYY-MM-DD
            file_date = datetime.strptime(date_str, "%Y-%m-%d")
            if file_date < cutoff:
                os.remove(os.path.join(emails_dir, f))
                deleted.append(f)
            else:
                kept.append(f)
        except:
            kept.append(f)  # if can't parse date, keep it
    print(f"Deleted ({len(deleted)}): {deleted}")
    print(f"Kept ({len(kept)}): {kept}")
EOF

# Commit the deletions
git add emails/
git commit -m "Cleanup: remove HTML emails older than [X] months"
git push origin main
```

**Always show the user what will be deleted before deleting.** List the files and ask for confirmation first.

---

## Email Index Page (Optional)

If the user asks for "a list of all my HTML emails" or "an index of emails", generate an `emails/index.html` page that lists all emails in the folder with:
- Date
- Recipient
- Subject (parsed from filename)
- Direct link to the hosted email

Push this index page to the repo the same way.

---

## Important Rules

- **Never save an HTML email locally only.** Always push to GitHub. Local files get lost.
- **Always use the YYYY-MM-DD prefix** in filenames — cleanup depends on it.
- **Never reuse a filename.** If a similar email exists, add a suffix: `-v2.html`, `-followup.html`.
- **Don't make every email look identical.** Vary the header color, accent, and layout to match the context.
- **Gmail draft is optional** — always ask if they want one after pushing, but don't assume.
- **The hosted URL is the deliverable.** That's what the user sends or shares, not a file attachment.

---

## Repo Structure After This Skill Is Active

```
Graehamwatts/skills/
├── skills/
│   ├── html-email/         ← this skill
│   │   └── SKILL.md
│   └── [other skills...]
├── emails/                 ← all hosted HTML emails live here
│   ├── 2026-04-11-brian-lopuk-zillow-strategy.html
│   ├── 2026-03-22-jason-pantana-partnership-brief.html
│   └── index.html          (optional — auto-generated index)
└── README.md
```

---

*Part of the PropOS skill library — Graeham Watts Real Estate*
