# ChatGPT Ads Workbook Builder (reference)

Source: AiM chatgpt-ads-workbook-builder skill (May 2026), merged into the chatgpt-ads skill.

# ChatGPT Ads Workbook Builder

Assemble three files from finished campaign content. This skill is purely structural — it doesn't write copy, it formats deliverables.

---

## Inputs You Receive

The copywriter skill (Phase 5 of the agent workflow) hands you a structured campaign object containing:

- **Campaign-level fields:** name, total budget, budget type (lifetime/daily), start date, end date, objective (Clicks/Reach/Conversions), target country (2-letter code)
- **For each of three ad groups:**
  - `adgroup_name` (lowercase, underscores, no special chars)
  - `context_hint` (the paragraph)
  - `keyword_array` (10-15 JSON-formatted phrases)
  - `max_bid` (within user's range)
  - `landing_page_url`
  - Three ads, each with: `title` (≤24 chars), `copy` (≤48 chars), `link`, `image_filename`, `image_rationale`

Also from market-config: agent name, brokerage, market geography, voice notes, compliance notes.

Also from Phase 3: full image inventory (filename + classification per image).

---

## Output 1: `campaign_workbook.xlsx`

Match OpenAI's bulk upload template structure **exactly**. Three sheets: `campaigns`, `adgroups`, `ads`.

### Sheet 1 — `campaigns`

Columns in this exact order:

| Col | Header | Value |
|---|---|---|
| A | `campaign_name` | The campaign name from inputs (lowercase, underscores, no special chars; e.g., `chatgpt_ads_q3_nashville`) |
| B | `budget_max` | Numeric value (no currency symbol; e.g., `2000`) |
| C | `budget_type` | `Lifetime` or `Daily` |
| D | `launch_date` | ISO format date (YYYY-MM-DD); leave blank if not specified |
| E | `end_date` | ISO format date (YYYY-MM-DD); leave blank if not specified |
| F | `objective` | `clicks` (lowercase) for Clicks objective, `Views` for Reach, `conversions` for Conversions. Match OpenAI's template casing: clicks is lowercase, Views/Reach is title case |
| G | `target_countries` | JSON array of 2-letter country codes (e.g., `["US"]` for US, `["US", "CA"]` for both) |

Row 1: headers (as listed).
Row 2: actual data.

No other rows. Do NOT include the OpenAI sample data row (`oaitestcmp1234567`) — that's an example in the template, not user data.

### Sheet 2 — `adgroups`

Columns in this exact order:

| Col | Header | Value |
|---|---|---|
| A | `campaign_name` | Must match the campaign name from Sheet 1, row 2 (exact string match — this is how OpenAI links ad groups to their campaign) |
| B | `adgroup_name` | The ad group's name (lowercase, underscores, no special chars) |
| C | `max_bid` | Numeric value (no currency symbol; e.g., `4`) |
| D | `keywords` | JSON array as a string. Format: `["phrase one", "phrase two", "phrase three"]` (square brackets, double-quoted strings, comma-separated) |
| E | `negative_keywords` | Leave blank unless the user has specific brand-name exclusions to add (max 25 per ad group) |

Row 1: headers. Rows 2-4: one row per ad group (three rows total).

### Sheet 3 — `ads`

Columns in this exact order:

| Col | Header | Value |
|---|---|---|
| A | `adgroup_name` | Must match the corresponding adgroup_name from Sheet 2 |
| B | `title` | The ad title (max 24 characters) |
| C | `copy` | The ad copy (max 48 characters) |
| D | `link` | The landing page URL. Append `?utm_source=chatgpt-ads&utm_medium=cpc&utm_campaign={campaign_name}` for tracking |
| E | `image_link` | Leave blank. The user adds image URLs manually in Ads Manager after upload (they have to host the images first). |

Row 1: headers. Rows 2-10: one row per ad (nine rows total — three ads per ad group × three ad groups).

### File Construction Process

Use openpyxl. Read `/mnt/skills/public/xlsx/SKILL.md` for full conventions, but the relevant rules for this build:

```python
from openpyxl import Workbook

wb = Workbook()

# Sheet 1: campaigns
campaigns = wb.active
campaigns.title = 'campaigns'
campaigns.append(['campaign_name', 'budget_max', 'budget_type', 'launch_date', 'end_date', 'objective', 'target_countries'])
campaigns.append([campaign_data])  # one row

# Sheet 2: adgroups
adgroups = wb.create_sheet('adgroups')
adgroups.append(['campaign_name', 'adgroup_name', 'max_bid', 'keywords', 'negative_keywords'])
for ag in ad_groups:
    adgroups.append([ag_row_data])

# Sheet 3: ads
ads = wb.create_sheet('ads')
ads.append(['adgroup_name', 'title', 'copy', 'link', 'image_link'])
for ad in all_ads:
    ads.append([ad_row_data])

wb.save('outputs/campaign_workbook.xlsx')
```

Use a clean professional font (Arial 11 or default). Header row should be bold. Auto-size columns for readability.

After saving, run the xlsx skill's recalc script to verify no formula errors — though this workbook has no formulas, the verification step catches any structural issues:

```bash
python /mnt/skills/public/xlsx/scripts/recalc.py outputs/campaign_workbook.xlsx
```

---

## Output 2: `context-hints-to-paste.docx`

Word document with one section per ad group. Use the docx skill conventions.

### Structure

**Document title (heading 1):** "Context Hints — Paste Into Ads Manager"

**Intro paragraph:**
> After you upload your campaign workbook to ads.openai.com, you'll need to paste a context hint into each ad group manually. This is the real targeting input — the field the platform actually uses for matching. The keywords in the spreadsheet got the upload through; these paragraphs are what make the campaign work.
>
> For each ad group below, open the corresponding ad group in Ads Manager, find the context hint or targeting field, and paste the paragraph as-is. Takes about 90 seconds per ad group.

**For each of three ad groups:**

- Heading 2: the ad group name (formatted human-readable: "First-Time Buyers — Nashville" not `first_time_buyers_nashville`)
- Subtitle in italic: which landing page this ad group drives to
- A styled callout (light gray background or bordered paragraph) containing the full context hint paragraph
- One line of instruction below: "Paste this into the targeting field for the `{adgroup_name}` ad group."

Use real Word formatting — heading styles, callouts via shaded paragraphs or table cells, proper spacing. The user will open this in Word or Google Docs and copy paragraphs out, so visual hierarchy matters.

### Construction

Use python-docx. Reference `/mnt/skills/public/docx/SKILL.md` for conventions. Key elements:

```python
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()

# Title
title = doc.add_heading('Context Hints — Paste Into Ads Manager', level=1)

# Intro paragraphs
doc.add_paragraph('After you upload your campaign workbook...')
doc.add_paragraph('For each ad group below, open the corresponding ad group...')

# Per ad group
for ag in ad_groups:
    doc.add_heading(ag.display_name, level=2)
    
    subtitle = doc.add_paragraph()
    subtitle_run = subtitle.add_run(f'Landing page: {ag.landing_page_url}')
    subtitle_run.italic = True
    
    # Callout — use a shaded paragraph
    callout = doc.add_paragraph()
    callout_run = callout.add_run(ag.context_hint)
    # Apply shading via XML if needed for the callout look
    
    instruction = doc.add_paragraph(f'Paste this into the targeting field for the {ag.adgroup_name} ad group.')

doc.save('outputs/context-hints-to-paste.docx')
```

---

## Output 3: `setup-checklist.docx`

Word document with the full post-upload checklist. This is where the user gets walked through what to do after the spreadsheet imports.

### Structure

**Title (heading 1):** "ChatGPT Ads Campaign — Setup Checklist"

**Section 1: Campaign Overview**

A small summary table:
- Campaign name
- Objective
- Total budget
- Budget type
- Start / end dates
- Target country
- Total ad groups: 3
- Total ads: 9

**Section 2: Budget and Bid Strategy**

Paragraph explaining:
- The campaign has a single shared budget — ad groups compete for it via bids
- Each ad group has been assigned a starting max bid based on the competitiveness of its moment
- A bid table showing each ad group's recommended starting bid

Then a numbered list of monitoring guidance:
1. Watch the first 48 hours for impression delivery
2. If an ad group is getting zero impressions, bump its bid by $1
3. If an ad group is burning budget without clicks, lower its bid by $1 or pause and review the copy
4. Don't make changes more than once per 48 hours during the learning phase

**Section 3: Image Hosting and Assignment**

A subsection per ad group with a small table:

| Ad # | Title | Suggested Image | Why |
|---|---|---|---|
| 1 | (title text) | (image filename) | (rationale from copywriter) |

Below the tables, a "How to host your images" callout:
> The bulk upload doesn't take image files — it takes image URLs. To get your images live:
> 1. Upload each image to Google Drive (or your website's media library, Dropbox, or any public hosting)
> 2. For Google Drive: right-click → Share → set to "Anyone with the link"
> 3. Copy the shareable link, then convert it to a direct-link URL using lh3.googleusercontent.com format if needed
> 4. In Ads Manager, paste each image URL into the corresponding ad's image field

**Section 4: Landing Page Audit Results**

For each ad group, note:
- Which page it points to
- Whether it's the ideal landing page or a downshift
- If a downshift, name the page that should be built (e.g., "Consider building a dedicated luxury seller page at /luxury-sellers — would lift match quality")

If multiple ad groups downshift to the homepage, add a paragraph at the end: "Your campaign is currently leaning hard on your homepage. Each specialization page you build is a conversion improvement. Prioritize building the pages flagged above."

**Section 5: Post-Upload Checklist**

A numbered checklist:
1. Log into ads.openai.com
2. Create new campaign → bulk upload → drag in campaign_workbook.xlsx
3. Confirm import (under 60 seconds)
4. Open context-hints-to-paste.docx → paste each ad group's hint into Ads Manager (three pastes total)
5. Host your images using the method above
6. For each ad, paste the image URL into Ads Manager
7. Verify all landing page URLs are correct
8. Confirm bids match the recommendations in Section 2
9. Review the campaign at the top level — confirm objective, budget, dates
10. If your brokerage requires ad review, get sign-off before launching
11. Launch

**Section 6: Compliance Reminders**

A short paragraph reminding the user of the compliance rules from their market-config (Fair Housing for US, CREA/provincial rules for Canada, etc.). One line per major regime that applies. Then: "The agent built the campaign with these guardrails — but the final responsibility is yours. If your brokerage requires ad review, run the copy through that step before launching."

**Section 7: Re-Running the Agent**

A short closing paragraph:
> When you want to run a new campaign, you don't need to re-do the intake. Your market-config.md is saved. Just drop new images into the images/ folder (or leave the old ones), tell the agent "build a new campaign," and you're rolling. Quarterly is a good cadence.

### Construction

Use python-docx with proper heading styles, tables, and shaded callouts. The deliverable should look professional when opened in Word or Google Docs — not like a markdown export.

```python
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.table import WD_TABLE_ALIGNMENT

doc = Document()

# Build sections...
# Use doc.add_heading() for hierarchy
# Use doc.add_table() for the bid table, image assignment tables, etc.
# Use shaded paragraphs or single-cell tables for callouts
# Use doc.add_paragraph() with proper styling for body text

doc.save('outputs/setup-checklist.docx')
```

---

## After All Three Files Are Written

Use the `present_files` tool to surface them to the user:

```python
present_files([
    'outputs/campaign_workbook.xlsx',
    'outputs/context-hints-to-paste.docx',
    'outputs/setup-checklist.docx',
])
```

Order matters — present the spreadsheet first since it's the primary deliverable.

Then give the user a brief summary message (3-5 sentences, no bullets):

> Three files are ready in your outputs folder. The campaign_workbook.xlsx is what you upload to ads.openai.com — bulk upload accepts it directly. The context-hints-to-paste.docx has the targeting paragraphs for each ad group; you'll paste those into Ads Manager after the upload imports. The setup-checklist.docx walks you through everything else: hosting your images, setting bids, what to monitor, and your post-upload sequence. Read the checklist first.

Don't dump the campaign back at them. The files speak for themselves.

---

## Self-Check Before Presenting Files

Verify before calling present_files:

- [ ] All three files exist in `outputs/`
- [ ] The .xlsx has exactly three sheets named `campaigns`, `adgroups`, `ads`
- [ ] The .xlsx has one campaign row, three ad group rows, nine ad rows
- [ ] Every title cell in the ads sheet is ≤24 characters
- [ ] Every copy cell in the ads sheet is ≤48 characters
- [ ] Every landing_page URL is populated
- [ ] image_link column is blank (user fills these in Ads Manager)
- [ ] The two .docx files open without errors and have proper heading hierarchy
- [ ] The context-hints doc has exactly three ad group sections
- [ ] The setup-checklist doc has all seven sections

If any check fails, fix it before presenting.
