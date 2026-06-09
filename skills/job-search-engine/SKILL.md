---
name: job-search-engine
description: >
  Full job-search pipeline for any user helping themselves or someone else land a new role.
  Covers the complete sequence from resume audit through offer negotiation, encoded from the
  MaverickAI "How to Use Claude to Land Your Next Job" playbook (2026 Edition).

  Use this skill ANY time the user mentions: resume, ATS, job application, job search, cover
  letter, interview prep, salary negotiation, LinkedIn optimizer, follow-up email after interview,
  auto-apply, job offer, counter-offer, resume rewrite, resume audit, keyword match, missing
  keywords, hiring manager, recruiter, applicant tracking, XYZ formula, job description match,
  resume score, career change, applying for jobs, help me get a job, improve my resume, fix my
  resume, optimize my LinkedIn, write a cover letter, prepare for interview, negotiate salary,
  or anything about landing a new position.

  Also trigger when a user uploads or pastes a resume, pastes a job description and asks how
  they stack up, or says "I have an interview for [ROLE] at [COMPANY]." Over-trigger rather
  than under-trigger — if there is any chance this is a job-search task, use this skill.
---

# Job Search Engine

A structured, repeatable system for winning job searches. Works for the user themselves, a
friend they're helping, or anyone navigating the job market. The full sequence runs from raw
resume to signed offer. Users can enter at any stage.

---

## How to Orient

When the user first engages, figure out where they are in the process:

- **Just starting** → Begin at Step 1 (Resume Audit)
- **Resume already done, applying now** → Jump to Cover Letter or Auto-Apply
- **Got an interview** → Jump to Interview Prep
- **Have an offer** → Jump to Salary Negotiation
- **Profile visibility problem** → Jump to LinkedIn Optimizer

If they paste a resume and a job description, start the audit immediately without asking for
confirmation.

---

## The Core Problem to Solve

Most resumes are rejected before a human reads them. ATS (Applicant Tracking Systems) scan for
specific keywords and formatting before passing resumes to a real person. Even when a human sees
it, they spend ~7 seconds scanning before deciding to read more or move on.

The goal is to fix both: pass the ATS filter, then stop the hiring manager's scroll.

---

## Step 1 — Resume Audit

**When to use:** User uploads/pastes a resume and a job description. This is always the first
step if they haven't run it yet.

Upload both the resume and job description, then run this prompt:

```
Act as a senior recruiter for this exact company.
Analyze my resume against this job description.

Give me:
1. A match score out of 100
2. The top 5 missing keywords that the ATS will be scanning for
3. The 3 red flags a hiring manager would spot in under 10 seconds
4. Which sections are strong and why
5. Which sections are weak and why
6. How my resume compares to what a strong candidate for this role would look like

Be brutally honest. I would rather fix problems now than get ghosted later.
```

**What to deliver:**
- Match score with a clear verdict (under 70 = needs significant work)
- Missing keywords with frequency count from the job description (e.g., "appears 3x in JD")
- Red flags stated plainly — missing metrics, title mismatch, unexplained gaps, etc.
- Honest section-by-section breakdown

**Don't skip this step.** Most people are surprised by what the ATS penalizes. Understanding
the gap is half the work.

---

## Step 2 — Experience Rewrite (Google XYZ Formula)

**When to use:** After the audit. Stay in the same chat so context carries forward.

The XYZ formula: **Accomplished [X] as measured by [Y] by doing [Z].**

Weak: "Managed a team of 5 engineers."
Strong: "Reduced deployment time by 40% (measured by weekly release velocity) by restructuring
the engineering team into cross-functional pods."

The first describes a task. The second describes an outcome. Hiring managers care about outcomes.

Run this prompt (same chat, after audit):

```
Rewrite my experience section using these rules:

1. Naturally include the missing keywords you identified, but do NOT force them in.
   They should feel like a normal part of each bullet.
2. Remove or fix every red flag you flagged.
3. Use the Google XYZ formula for every bullet:
   "Accomplished [X] as measured by [Y] by doing [Z]"
4. Start every bullet with a strong action verb. Never use "Responsible for" or "Helped with."
5. Add specific numbers wherever possible. If I did not provide numbers, suggest realistic
   placeholders I can fill in later and mark them with [FILL IN].
6. Keep each bullet to 1-2 lines max. Hiring managers skim. Dense paragraphs get skipped.
7. Order bullets by impact, not chronology. The most impressive result goes first.
```

---

## Step 3 — ATS + Hiring Manager Stress Test

**When to use:** After the rewrite. Still in the same chat.

This prompt evaluates the rewritten resume from two angles simultaneously:

```
Now act as two different people:

FIRST: Act as an ATS filter. Scan my new resume and tell me:
- Would it pass the ATS for this job? (Yes/No)
- Which keywords are now present and which are still missing?
- Any formatting issues that would confuse an ATS parser?
  (tables, columns, headers, special characters, images)

SECOND: Act as a hiring manager who is reading 200 resumes in one sitting.
Scan my resume and tell me:
- Which sections would you skip? Why?
- What makes you stop scrolling (good or bad)?
- Would you put this in the "yes" pile, "maybe" pile, or "no" pile for this role?
- Rewrite any sections that would get skipped so they actually stop the scroll.

Give me the final version of my resume after all fixes are applied.
```

**After this step:** Ask Claude to output the final resume as a clean artifact. Download as
.docx and replace all `[FILL IN]` placeholders with real numbers before submitting.

---

## Step 4 — Cover Letter (30 seconds per job)

**When to use:** After the resume is optimized, for each specific job application. Use in the
same chat as the resume audit so Claude has full context.

```
Write a cover letter for this role. Rules:

1. First paragraph: Name the company and role. Reference one specific thing about the company
   that made you want to apply (a recent product launch, a news article, a company value that
   resonates). Do NOT be generic.

2. Second paragraph: Pick the 2-3 requirements from the job description where my experience
   is strongest. For each, give one concrete result from my resume (with numbers).

3. Third paragraph: Address the biggest gap between my resume and the job description
   head-on. Explain how my transferable skills or adjacent experience covers it. Do not
   pretend the gap does not exist.

4. Closing: One sentence. Ask for the interview.
   No fluff. No "I look forward to the opportunity to discuss."

Total length: Under 250 words.
Tone: Confident, specific, human. Do NOT sound like AI wrote it.
```

**The secret:** The third paragraph — addressing the gap head-on — is what separates good
cover letters from everyone else's. It signals self-awareness and confidence.

---

## Step 5 — Auto-Apply with Cowork + Chrome

**When to use:** Resume is optimized, user wants to apply to multiple jobs at once. Requires
Claude Pro, Cowork mode, and the Claude in Chrome extension. User must be logged into LinkedIn.

```
Now that my resume is optimized, go to LinkedIn and do the following:

1. Search for [JOB TITLE] roles in [LOCATION] posted in the last [7/14/30] days.

2. Filter for jobs where my resume is at least a 70% match based on the skills and
   experience listed in the job description.

3. Pick the top 10 jobs I have the highest chance of landing an interview for.

4. For each job:
   - Read the full job description
   - Customize my resume summary and key bullets to match that specific role
   - Write a short cover note (3 sentences max) that references something specific
     about the company
   - Submit the application through LinkedIn

5. After all 10 are submitted, send me a summary:
   - Company name + job title
   - Match score
   - What you customized for each
   - Application status (submitted / draft)

Pause before submitting each application and show me the customized version first.
```

**Start with "pause before submitting"** until the user is confident in quality. Then they
can remove the pause for fully automated runs.

---

## Step 6 — Interview Prep System

**When to use:** User says they got an interview. Trigger immediately.

```
I have an interview for [ROLE] at [COMPANY] on [DATE].
Here is the job description: [paste]

Prepare me with:

# COMPANY INTEL
- What does this company actually do (in 2 sentences, not their PR version)
- Recent news (last 90 days) that I should reference in the interview
- Their biggest challenge or competitor threat right now
- What their Glassdoor/Blind reviews say about the interview process and culture

# PREDICTED QUESTIONS (top 10)
For each question:
- The question they will ask
- Why they are asking it (what they are testing)
- A sample answer using my actual experience from my resume (with specific metrics)
- The follow-up question they will probably ask

# QUESTIONS I SHOULD ASK THEM
Give me 5 questions that show I did research and actually understand their business.
Not "What does a typical day look like" generic stuff. Questions that make the
interviewer think "This person gets it."

# MOCK INTERVIEW
After I review the above, run a 15-minute mock interview. Ask me the top 5 questions
one at a time. After each answer, give me feedback on what was strong and what to fix.
```

**The mock interview is the most valuable part.** Reading answers is helpful; actually
answering questions and getting real-time feedback is what builds muscle memory before the
real thing.

---

## Step 7 — Salary Negotiation Script

**When to use:** User has an offer. Almost every offer has room to negotiate.

```
I got an offer for [ROLE] at [COMPANY].

Offer details:
- Base salary: $[AMOUNT]
- Bonus: [AMOUNT or NONE]
- Equity/stock: [AMOUNT or NONE]
- Start date: [DATE]
- Other perks: [LIST]

My target: $[AMOUNT] base
(or tell me what I should target based on data)

Build me a negotiation strategy:

1. MARKET DATA
   - What does this role pay at this company based on Levels.fyi, Glassdoor, Blind,
     and Payscale data?
   - What is the pay range for this level?
   - Where does my offer fall in that range?

2. COUNTER-OFFER SCRIPT
   - Write the exact email I should send
   - Tone: grateful, confident, specific
   - Reference market data without being adversarial
   - Ask for a specific number, not a range

3. PHONE CALL SCRIPT
   - Opening the conversation
   - Stating my counter
   - Handling "this is the best we can do"
   - Negotiating non-salary items if base is firm
     (signing bonus, extra PTO, remote flexibility, start date)

4. WALK-AWAY ANALYSIS
   - At what number should I accept?
   - At what number should I walk away?
   - What are the non-monetary factors that could make a lower offer worth taking?
```

**Key rule:** Never give a number first. If asked "What are your salary expectations?" before
an offer is made, deflect: "I'd like to learn more about the full compensation package before
discussing numbers. What is the budgeted range for this role?"

---

## Step 8 — LinkedIn Profile Optimizer

**When to use:** User wants recruiters to come to them rather than always applying outbound.
Most profiles are invisible in recruiter searches. This fixes that.

```
I want to optimize my LinkedIn profile so recruiters find me and reach out.
Here is my current profile: [paste or upload screenshot]

Target roles I want to attract: [ROLE 1, ROLE 2]
Target companies: [COMPANY 1, COMPANY 2]
Target location: [CITY or REMOTE]

Rewrite these sections:

1. HEADLINE (220 chars max)
   - Not my current job title
   - Include 2-3 keywords recruiters search for
   - Include a result or specialty that stands out
   - Format: [What I do] | [Key result] | [Niche]

2. ABOUT SECTION (2,600 chars max)
   - First 2 lines visible before "see more" — make them count
   - Write in first person, not third
   - Lead with what I solve, not who I am
   - Include 5-8 keywords naturally
   - End with a clear call to action

3. EXPERIENCE BULLETS
   - Same XYZ formula from my resume
   - But more conversational than resume bullets
   - Add 1 line per role about what I learned, not just what I did

4. SKILLS SECTION
   - Top 5 skills to pin based on the roles I am targeting
   - In priority order from most searchable to least

5. FEATURED SECTION
   - Suggest 2-3 things I could add (articles, projects, presentations, media)
     that would make a recruiter stop and look closer
```

**The headline is the most important field.** "Marketing Manager at XYZ Corp" is invisible.
"B2B SaaS Growth Marketer | Scaled pipeline from $2M to $14M | Demand Gen + ABM" gets clicked.

---

## Step 9 — Follow-Up Email Templates

**When to use:** After application or after interview. Most candidates drop the ball here.

```
I need follow-up emails for my application at [COMPANY] for the [ROLE] position.
Write three:

# EMAIL 1: POST-APPLICATION (send 5 days after)
- Subject line that gets opened (not "Following Up")
- Reference something specific about the company
- Mention one result from my resume that maps to their biggest stated challenge
- Ask if there is anything else they need
- Under 100 words total

# EMAIL 2: POST-INTERVIEW (send within 24 hours)
- Thank the interviewer by name
- Reference one specific thing we discussed
- Add one thing I forgot to mention that strengthens my candidacy
- Restate my interest without sounding desperate
- Under 120 words total

# EMAIL 3: THE NUDGE (send 7 days after interview if no response)
- Light, professional, not pushy
- Add a piece of value (relevant article, industry insight, or quick thought
  related to something we discussed)
- Give them an easy out: "If the timeline has shifted, totally understand"
- Under 80 words total

Tone for all: Confident, not desperate. Specific, not generic. Human, not template-y.
```

---

## Full Workflow Sequence

For someone starting from scratch:

| Step | Task | Time |
|------|------|------|
| 1 | Resume Audit — match score, gaps, red flags | 5 min |
| 2 | Experience Rewrite — XYZ formula, metrics | 5 min |
| 3 | ATS + Hiring Manager Test — final polish | 5 min |
| 4 | LinkedIn Optimizer — rewrite for inbound | 10 min |
| 5 | Cover Letter — one per application | 30 sec each |
| 6 | Auto-Apply — 10 customized apps via Cowork | 10 min setup |
| 7 | Interview Prep — research + mock interview | 20 min per company |
| 8 | Salary Negotiation — market data + scripts | 15 min |
| 9 | Follow-Up — 3 emails at the right times | 2 min |

**Repeat steps 1-3 for each job applied to.** The same resume does not work for every role.
Keywords and red flags change with each job description.

**Always review and personalize outputs.** Generic AI content hurts more than it helps. Claude
provides the structure; the user provides the substance — their voice, their stories, their
real numbers.

---

## Output Format

Deliver outputs in clean, copy-paste-ready format. When the final optimized resume is ready,
produce it as a .docx using the docx skill. Cover letters as clean markdown the user can paste
directly. Email templates as individual blocks labeled clearly. For auto-apply, always pause and
confirm before submitting.
