# DRE Leak Incident Log — 2026-04-29 (the 10th occurrence)

Referenced from the repo-root `CLAUDE.md` brand identity section. This is the incident narrative behind the `02015066` blocklist entry; the enforcement itself (blocklist + `scripts/verify_brand_identity.py` tripwire) is documented in `CLAUDE.md` and does not depend on this file being loaded.

**Where it leaked:** `Graehamwatts/cma-reports/Offer_828_Weeks_St.html` (in the now-retired `cma-reports` repo, since superseded by `online-content`) — a published GitHub Pages report for a real client offer comparison. The wrong DRE appeared on lines 523 and 753.

**Root cause:** The Claude session that ran `offer-analyzer` on 2026-04-29 at 22:05 UTC had the wrong DRE (02015066) cached in its system prompt's `available_skills` list (specifically in the now-retired `video-script-creation-engine` description). Instead of reading the DRE from `identity.json` like the repo CLAUDE.md instructs, that session typed the value from prior context.

**Fix applied (2026-04-29):**
- Corrected the contaminated file in cma-reports
- Added a `BRAND IDENTITY HARD RULE` warning at the top of `cma-generator/SKILL.md` and `offer-analyzer/SKILL.md` that explicitly says "do NOT type from prior context"
- Retired `video-script-creation-engine` from GitHub (it's been merged into `content-creation-engine`); local Cowork sync should refresh the cache

**Audit gap:** The tripwire (`scripts/verify_brand_identity.py`) only audits the skills repo. It does NOT currently audit `online-content` (the published-content sister repo, formerly `cma-reports`). A copy of the script should be added to `online-content` as well, OR this script extended to clone-and-audit `online-content` as part of its run. Open follow-up — increased priority since `online-content` will be the live target for every new CMA, offer, disclosure, newsletter, and dashboard going forward.
