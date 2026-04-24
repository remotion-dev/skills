# Install the Room Redesign Skill (Graeham's copy)

This is a from-scratch version of the "Banana Skill" you saw in the PDF.
**None of the third-party code runs.** You get:

- `SKILL.md` — the instructions Claude reads to know when/how to use this skill
- `scripts/redesign.py` — a small Python script that calls Google's Gemini API directly

You read every line. Nothing phones home anywhere except `generativelanguage.googleapis.com` (Google).

---

## One-time setup (~2 minutes)

### 1. Get a free Gemini API key

1. Go to **https://aistudio.google.com/**
2. Sign in with any Google account
3. Click **"API Keys"** in the left sidebar
4. Click **"Create API Key"**
5. Copy the key (it starts with `AIzaSy...`)

### 2. Store the key safely

**On Windows (where your Claude desktop app runs):**

Open PowerShell and run this once (paste your actual key):

```powershell
[Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "AIzaSy...your-key...", "User")
```

Then **fully quit and reopen** the Claude desktop app so it picks up the new environment variable.

**On macOS/Linux:** Add this line to `~/.zshrc` or `~/.bashrc`:
```bash
export GEMINI_API_KEY="AIzaSy...your-key..."
```
Then open a new terminal.

### 3. Confirm Python + requests are available

Open a terminal and run:

```bash
python3 -c "import requests; print('ok')"
```

If it prints `ok`, you're done. If it errors, run:

```bash
pip3 install requests --break-system-packages
```

---

## Drop the skill into your skills folder

Your skills live here on this machine:

```
C:\Users\Graeham Watts\AppData\Roaming\Claude\local-agent-mode-sessions\skills-plugin\13b9f772-ca82-4f73-bad7-07266d314a4f\f8d0580a-5ad4-4608-9db7-2929ac644a5f\skills\
```

Copy the entire `room-redesign` folder (which contains `SKILL.md` and `scripts/redesign.py`) into that directory. You should end up with:

```
...\skills\room-redesign\SKILL.md
...\skills\room-redesign\scripts\redesign.py
...\skills\room-redesign\INSTALL.md  (this file, optional)
```

Restart the Claude desktop app one more time. The skill should now appear in your available-skills list.

---

## Try it

1. Upload a photo of a room to the chat.
2. Say: *"Redesign this for a listing — neutral, broadly appealing, keep the floors."*
3. I'll detect the `room-redesign` skill, run the Python script, and give you back a photo-realistic staged version.

---

## Push it to your GitHub backup

Once it's working, use your `github-skill-sync` skill to push this new skill to `Graehamwatts/skills`. That way it's version controlled and mirrored to Box/local — same 3-tier backup as the rest of your skills.

Just say: *"Push my skills to GitHub."*

---

## If something goes wrong

| Problem | What it means | Fix |
|---|---|---|
| `GEMINI_API_KEY is not set` | Env var didn't persist | Re-run the `setx` / `export` and **restart Claude** |
| `HTTP 403` | Key invalid or project not enabled | Make a new key in AI Studio |
| `HTTP 429` | Free-tier quota hit for the minute | Wait 60s or upgrade |
| "No image in response" | Safety filter likely blocked the prompt | Soften the prompt (no people, no real addresses, etc.) |
| Claude doesn't trigger the skill | SKILL.md not in the right folder | Double-check the path above |

---

## What this does NOT do

Be honest: this is images only. For video walkthroughs of rooms, use your `heygen-video`, `higgsfield-video`, or `remotion-video` skills. For full CMA or offer analysis, those are separate skills too. This one is specifically for "photo in → photo out".
