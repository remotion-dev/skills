# GitHub Repo Analyzer — Review Criteria & Benchmarks

## Developer Activity Benchmarks

Use these as baseline expectations. Adjust based on team size, project phase, and role.

### Healthy Activity Levels (per 2-week sprint)

| Metric | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| Commits | 10+ | 3-9 | 0-2 |
| PRs opened | 3+ | 1-2 | 0 |
| PRs reviewed (for others) | 2+ | 1 | 0 |
| Avg days to review assigned PR | < 1 day | 1-3 days | 3+ days |
| Avg PR size (lines changed) | < 300 | 300-500 | 500+ |

**Important context adjustments:**
- Part-time contributors: Cut all thresholds in half
- Team leads: May have fewer commits but should have MORE reviews
- New team members (first 30 days): Expect lower numbers as they ramp up
- Sprint planning / design phases: Lower commit volume is normal
- External development tools: See "External Tool Development Pattern" section below

---

## External Tool Development Pattern

Some outsourced teams use their own internal development environments, IDEs, or platforms to build code — then push finished or near-finished code to the client's GitHub repos in bulk. This creates a distinct pattern that the analyzer must detect, flag, and account for.

### Why This Matters

When a team develops on an internal tool and only pushes to the client's GitHub when features are "done":
1. **The client loses real-time visibility** into development progress
2. **Commit history is compressed** — weeks of incremental work shows up as a few large commits
3. **Code review is impossible** during development — the client only sees the final output
4. **Risk accumulates silently** — bugs, architectural issues, and scope drift are invisible until the push
5. **The client doesn't own the work-in-progress** — if the engagement ends, unfinished code may never be delivered
6. **Standard commit frequency benchmarks don't apply** — a developer may be active but invisible

### Detection Signals

Flag a repository for "External Tool Development Pattern" when you observe:

| Signal | What It Looks Like |
|--------|-------------------|
| Bulk push pattern | Large number of files/lines committed in a single push or a short burst (1-2 days), followed by weeks of silence |
| Initial commit is fully built | First commit contains a complete or near-complete application structure, not gradual buildout |
| Low commit frequency, high commit size | Few commits but each one changes hundreds or thousands of lines |
| Missing incremental history | No "work in progress" commits, no iterative debugging trail — code appears fully formed |
| Commit timestamps clustered | All commits within a few hours, suggesting a batch push from another system |
| Single contributor across large codebases | One developer account pushes everything, but the volume implies multiple people's work |
| No branch/PR development cycle | Features appear directly on main or dev branch without feature branch → PR → merge flow |

### Adjusted Benchmarks for External Tool Workflows

When external tool development is detected, standard commit frequency benchmarks are **not reliable** indicators of developer activity. Instead, shift analysis to:

| Metric | What to Evaluate Instead |
|--------|-------------------------|
| Commit frequency | **Push frequency** — How often does code arrive in the client's repo? Weekly pushes = acceptable. Monthly = governance risk |
| Developer count | **Unique committer count vs billed team size** — If 4 devs are billed but 1 pushes, the others are invisible |
| Code quality | **Code structure and architecture quality** of what was pushed, since you can't evaluate the development process |
| Progress tracking | **Feature completeness per push** — Is shipped code functional, or are there half-built features? |
| Collaboration | **Cannot be assessed** — internal tool collaboration is invisible to the client |

### Governance Flags for External Tool Workflows

| Flag | Condition | Severity |
|------|-----------|----------|
| 🔴 CRITICAL | Client has explicitly requested team push to client repos and team has not complied | CRITICAL — Governance violation |
| 🔴 CRITICAL | Client cannot verify which developers are working due to single-account pushes | CRITICAL — Accountability gap |
| 🟡 WARNING | Team is developing externally but pushing regularly (weekly or better) | WARNING — Acceptable interim, needs migration plan |
| 🟡 WARNING | Repo shows bulk-push pattern but client hasn't explicitly required real-time commits | WARNING — Recommend requiring it |
| 🟢 WATCH | Team uses external tools for CI/testing but commits incrementally to client repo | WATCH — Acceptable workflow |

### Recommended Actions When External Tool Pattern Is Detected

1. **Require immediate migration to client GitHub repos** — All active development should happen in repos the client owns and can monitor
2. **Require daily or per-feature-branch pushes** — Even if the team uses internal tools for testing, code should be pushed to the client repo incrementally, not in bulk
3. **Establish branch protection + PR requirements** — Forces the team to use PRs for integration, creating visibility even if they develop elsewhere
4. **Request full team GitHub access** — All developers should have individual accounts pushing commits, not one person batch-pushing everyone's work
5. **Set up a migration deadline** — Give the team a specific date (e.g., 7 business days) to move all active work to client repos
6. **If non-compliant after deadline** — Escalate to contract/engagement terms review

---

## Repo Verification Checklist

Before analyzing, verify you are looking at the correct repositories. This prevents wasting time auditing repos the client built themselves or that belong to a previous engagement.

### Pre-Analysis Questions

1. **Who owns these repos?** — Is the client the GitHub owner, or is the dev team hosting them?
2. **Which repos does the dev team actively commit to?** — Get explicit confirmation, not assumptions
3. **Are there repos the team uses that the client doesn't have access to?** — If yes, flag immediately
4. **Did the client build any of these repos themselves?** — Exclude client-built repos from team performance scoring
5. **Are there previous developers whose commits should be excluded?** — Get names/usernames to filter out

### Repo Attribution Table

Before scoring, build a clear attribution table:

| Repository | Who Built It | Current Team Active? | Include in Audit? |
|------------|-------------|---------------------|-------------------|
| [repo name] | [client / dev team / previous team] | [yes/no] | [yes/no — with reason] |

This table must appear in the report. It prevents misattribution (e.g., praising the dev team for screens the client built, or flagging a repo as inactive when it was intentionally handed off).

---

## Commit Quality Indicators

**Good commit messages:**
- Start with a verb (Add, Fix, Update, Refactor, Remove)
- Reference issue/ticket numbers
- Explain WHY, not just WHAT
- Under 72 characters for the subject line

**Red flag commit messages:**
- Single word: "fix", "update", "changes", "stuff"
- No issue/ticket reference on a team that uses issue tracking
- Extremely long messages that should have been PR descriptions
- "WIP" commits pushed to main branch

### PR Quality Indicators

**Good PR patterns:**
- Clear title and description
- Linked to an issue or ticket
- Reasonable size (under 300 lines ideal)
- Has at least one reviewer assigned
- CI checks pass before merge
- Conversation/feedback addressed before merge

**Red flag PR patterns:**
- Empty description
- 1000+ lines changed (impossible to properly review)
- Self-approved and self-merged
- Merged with failing CI checks
- No linked issue (on teams that use issue tracking)
- Force-merged bypassing review requirements

---

## Repository Health Scoring

### Overall Health Score

Calculate based on these weighted factors:

| Factor | Weight | Healthy | Needs Attention | At Risk |
|--------|--------|---------|-----------------|---------|
| CI/CD status | 20% | All checks passing | Flaky tests | Failing on main |
| PR review rate | 20% | >80% reviewed before merge | 50-80% reviewed | <50% reviewed |
| Avg merge time | 15% | <2 days | 2-5 days | 5+ days |
| Branch hygiene | 10% | <5 stale branches | 5-15 stale | 15+ stale |
| Open PR age | 15% | All <3 days | Some 3-7 days | Any 7+ days |
| Issue management | 10% | Issues triaged and assigned | Backlog growing | Issues ignored |
| Documentation | 10% | README current, contributing guide exists | README outdated | No README |

### Additional Factor: Code Ownership & Governance (applies when external tool pattern detected)

When an external tool development pattern is detected, add this weighted factor:

| Factor | Weight | Healthy | Needs Attention | At Risk |
|--------|--------|---------|-----------------|---------|
| Code ownership governance | 15% (redistributed from other factors) | All code in client repos, incremental commits, all devs visible | External tool used but regular pushes, migration plan in place | Client has requested migration and team has not complied |

When this factor is added, redistribute weight by reducing CI/CD and PR review rate by 5% each, and Open PR age by 5% — because those metrics are less meaningful when the team isn't using the client's repo as their primary development environment.

### Score Interpretation
- **Healthy (70-100%)**: Repo is well-maintained, team processes are working
- **Needs Attention (40-69%)**: Some areas slipping, targeted improvements needed
- **At Risk (0-39%)**: Significant process gaps, technical debt accumulating

---

## Flag Criteria — Detailed

### 🔴 CRITICAL — Developer Level

| Condition | Why It Matters |
|-----------|---------------|
| Zero commits AND zero PRs in the full analysis period | Developer appears inactive |
| Assigned to issues/PRs but zero progress | Work is stalled, may be blocked |
| Merging own PRs to main with no review, repeatedly | Quality gates being bypassed |
| Breaking CI on main branch and not fixing it | Blocking the whole team |
| Billed developer with no GitHub username identifiable | Cannot verify work is being performed |

### 🟡 WARNING — Developer Level

| Condition | Why It Matters |
|-----------|---------------|
| Commit count dropped 50%+ vs previous period | Possible disengagement or blocker |
| Zero code reviews given to others | Not participating in team quality process |
| PRs averaging 500+ lines | Code is hard for others to review properly |
| Assigned reviews sitting unactioned for 3+ days | Blocking other developers |
| Only committing to one directory/module | Knowledge silo forming |
| Pushing bulk commits from external tool instead of incremental development | Process visibility gap |

### 🟢 WATCH — Developer Level

| Condition | Why It Matters |
|-----------|---------------|
| New to repo (first 30 days of commits) | Expected ramp-up period |
| Commit messages declining in quality | Minor but worth mentioning |
| Slightly fewer reviews than team average | Not urgent but track the trend |
| Working late/weekend commits increasing | Possible workload issue |

### 🔴 CRITICAL — Repository Level

| Condition | Why It Matters |
|-----------|---------------|
| CI/CD failing on main/master branch | Deployments blocked, team can't ship |
| PRs open 14+ days with no activity | Work is abandoned or stuck |
| No branch protection on main | Anyone can push directly, risky |
| Security vulnerabilities flagged by Dependabot/similar | Active security risk |
| Client requested code migration to their repos and team has not complied | Governance violation — client doesn't own the work they're paying for |
| Repo misnamed or mislabeled vs actual contents | Creates confusion about what's been built and what hasn't |

### 🟡 WARNING — Repository Level

| Condition | Why It Matters |
|-----------|---------------|
| 5+ stale branches (30+ days inactive) | Cluttered repo, potential merge conflicts |
| No CI/CD configured at all | No automated quality checks |
| README hasn't been updated in 90+ days | Documentation drifting from reality |
| Average merge time exceeding 5 days | Development velocity is slow |
| External tool development detected but no migration plan | Visibility and ownership risk accumulating |
| Feature branches unmerged with no PRs | Work may be stalled or abandoned |

### 🟢 WATCH — Repository Level

| Condition | Why It Matters |
|-----------|---------------|
| Test coverage declining (if trackable) | Quality may slip over time |
| Issue backlog growing faster than closing | Scope creep or understaffing |
| Release frequency slowing | May indicate complexity or blockers |

---

## Report Templates

### Executive Summary Template
```
REPOSITORY: [repo name]
PERIOD: [start date] — [end date]
HEALTH SCORE: [X]% — [Healthy/Needs Attention/At Risk]

QUICK STATS:
- [X] commits by [Y] contributors
- [X] PRs merged (avg [Y] days to merge)
- [X] open PRs | [X] open issues
- CI Status: [Passing/Failing/Not configured]

EXTERNAL TOOL STATUS: [Not detected / Detected — see findings / Confirmed by client]
REPO VERIFIED: [Yes — confirmed as dev team repo / No — needs verification]

TOP FINDINGS:
1. [Most important finding]
2. [Second most important]
3. [Third most important]
```

### Developer Scorecard Template
```
DEVELOPER: @[username]
FLAG: [🔴/🟡/🟢/✅]
PERIOD: [dates]

ACTIVITY:
- Commits: [X] ([up/down X%] vs previous period)
- PRs opened: [X] | PRs merged: [X]
- Reviews given: [X] | Avg review time: [X] days
- Primary work areas: [directories/modules]
- Push pattern: [Incremental / Bulk push / External tool suspected]

STRENGTHS:
- [Positive observation]

AREAS FOR IMPROVEMENT:
- [Constructive observation]

RECOMMENDATION:
- [Specific action item]
```

---

## Context Questions to Ask

Before running the analysis, gather context that affects interpretation:

1. **Team structure** — How many developers? Full-time or part-time? Any contractors?
2. **Sprint cadence** — Weekly? Bi-weekly? Kanban (no sprints)?
3. **Current phase** — Building new features? Maintenance mode? Pre-launch crunch?
4. **Known absences** — Anyone on PTO or leave during the analysis period?
5. **Non-code work** — Are some developers doing design, planning, or documentation that won't show in commits?
6. **Specific concerns** — Is there a particular developer or issue they want investigated?
7. **Development environment** — Is the team developing directly in the client's GitHub repos, or do they use an internal tool/platform and push code periodically? (This is critical for interpreting commit patterns)
8. **Repo ownership** — Did the client build any of the repos being analyzed? (Exclude client-built repos from team scoring)
9. **Previous developers** — Are there commits from a prior team that should be filtered out?
10. **Migration requests** — Has the client asked the team to change their workflow (e.g., stop using internal tools, push to client repos)? If yes, has the team complied?
