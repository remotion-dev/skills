# Hook Frameworks & Scoring

A hook has one job: stop the scroll in under 2 seconds and make the viewer give you the next 5 seconds. Everything else in the script is downstream of the hook.

The source transcript's hook is data. Phase 2 already identified which pattern it used. This phase produces 3 stronger variants — drawn from DIFFERENT frameworks than the source — and scores them.

## The 8 Hook Frameworks

### 1. Bold Contrarian Claim

"Everyone says X. They're wrong." Or: "The conventional wisdom on X is killing your <outcome>."

**When to use:** Source video gave the conventional answer. Graeham knows the real one. High engagement, but only deploy when Graeham can genuinely defend the contrarian position.

**Example:** "Everyone tells first-time buyers to wait for rates to drop. That's the worst advice in this market."

### 2. Personal Stake / Confession

"I just lost $X because of this." "I almost made the biggest mistake of my career last week."

**When to use:** When Graeham has a real story behind the topic. Highest trust, highest engagement when authentic. Don't fake this.

**Example:** "I had a buyer almost walk away from her dream home last week — over a $400 inspection finding."

### 3. Pattern Interrupt Question

A question that breaks the viewer's mental model. Should feel WEIRD, not obvious.

**When to use:** When the topic has a counterintuitive angle. The question should make the viewer go "wait, what?"

**Example:** "Why is your landlord suddenly being really nice to you?" (Setup for AB 1482 / lease renewal content.)

### 4. Specific Number Shock

A specific, verifiable, surprising number in the first 3 seconds. Specificity over magnitude.

**When to use:** When the research pack has a strong data point. Specific beats round. "87%" beats "most people."

**Example:** "82% of Peninsula buyers in April 2026 paid over asking. Here's what the other 18% did differently."

### 5. Story Tease

"Last week, <character> almost <bad outcome>. Here's what happened."

**When to use:** When you have a real client situation to anchor the script around (Phase 3 Angle 5). Tease without spoiling — make the viewer want the payoff.

**Example:** "Last week, a Redwood City seller turned down a $1.85M offer. Six weeks later she took $1.72M. Here's the mistake."

### 6. Direct Address

"If you're <specific situation>, this is for you."

**When to use:** When the topic is narrow and you want to qualify the viewer fast. Weaker pattern interrupt but very high through-rate for the qualified audience.

**Example:** "If you're renting in California and your landlord just raised your rent by more than 5%, you need to watch this."

### 7. Curiosity Gap

"There's one thing nobody tells you about <topic>." "Most people don't know <surprising thing>."

**When to use:** When the body of the script genuinely delivers a non-obvious insight. If the payoff is obvious, this hook over-promises and tanks watch-time.

**Example:** "There's one line in every purchase agreement that almost no buyer reads. It costs them an average of $4,200."

### 8. Reveal Frame

"Here's what every <expert role> secretly knows."

**When to use:** When Graeham is sharing genuine industry knowledge. Insider framing without violating professional ethics or any kind of "secret club" vibe — just plain expertise.

**Example:** "Here's what every listing agent knows about price strategy that most buyers never get told."

## Scoring Rubric — 4 Criteria, 5 Points Each (20 total)

Score each hook variant.

### Criterion 1 — Pattern Interrupt (1-5)

Does the hook break the scroll-pattern? Does the first 5 words feel different from the 100 other videos in the feed?

- **5** = Genuinely surprising opening — viewer brain has to update its model in the first 2 seconds
- **3** = Familiar pattern executed well
- **1** = Generic opening ("In this video..." / "Today we're going to talk about...")

### Criterion 2 — Curiosity Gap (1-5)

Does the hook open a question that the rest of the video has to answer? Does it create itch?

- **5** = Viewer cannot close the app without knowing the answer
- **3** = Mild curiosity, viewer may scroll if the next 5 seconds are slow
- **1** = No question opened, no reason to keep watching

### Criterion 3 — Specificity (1-5)

Specific over generic. Numbers, names, dates, concrete situations beat abstractions.

- **5** = Specific number / date / situation that's verifiable
- **3** = Some specificity ("in this market", "in California")
- **1** = Pure abstraction ("a lot of people", "in general")

### Criterion 4 — Graeham Voice Fit (1-5)

Does the hook sound like Graeham? Match his calibrated, direct, working-agent tone. Not hype-bro, not corporate, not stiff.

- **5** = Sounds like him. Confident, specific, no fluff.
- **3** = Adjacent — Graeham would say it but slightly off
- **1** = Off-brand — too hype, too sales-y, too academic

Reference `video-script-creation-engine/references/phases/script-writer/references/voice-and-style.md` if available — that's the canonical voice doc.

## Hook Pacing — The First 5 Seconds Matter Most

A hook isn't just the first sentence. It's the first 5 seconds of viewing experience. Production-side considerations:

- **Word 1 should be high-stakes.** Don't open with "Hey," "So," "Welcome," or any filler.
- **Concrete proper noun in the first 7 words.** A specific place, person, number, or thing locks attention faster than abstractions.
- **No throat-clearing.** "Let me tell you about" / "I want to talk about" — cut these. Start with the substance.
- **Implied scene change.** If the body of the video will involve B-roll or scene change, the hook should hint at it visually too — first 5 seconds set viewer expectation.

## Output Format

```
## Hook Variants

### Hook Variant 1 — <framework name>
"<hook text>"
Pattern Interrupt: _/5
Curiosity Gap: _/5
Specificity: _/5
Graeham Voice Fit: _/5
Total: _/20

### Hook Variant 2 — <framework name>
...

### Hook Variant 3 — <framework name>
...

### Recommendation
Use Hook Variant <N> because <one-line rationale>.
Backup: Variant <N> for <use case — e.g., "if testing a different angle on the same topic">.
```

The three variants MUST come from three different frameworks. Don't generate three contrarian hooks — that's not really three variants. Diversify the patterns so Graeham can A/B test if he wants.

## Common Mistakes

- **Copying the source's hook with new words.** That's not a new hook, that's a paraphrase. The framework should change.
- **Hooks longer than 12 seconds spoken.** A hook is the FIRST move, not the whole opening. If it runs 12+ seconds, you wrote a mini-script, not a hook.
- **Hooks with the word "Today".** "Today we're talking about..." — instant skip. Cut it.
- **Hooks that promise a payoff the video doesn't deliver.** Bigger promise = higher click but worse watch-through. Match the promise to what the body actually pays off.
