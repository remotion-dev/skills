# Readability — Flesch Reading Ease

Web content should land in the 60–70 range on Flesch Reading Ease. That's roughly 8th-grade reading level — enough sophistication for adult readers, low enough cognitive load that skimmers stay.

## The formula

```
Flesch Reading Ease = 206.835 − 1.015 × (total_words / total_sentences) − 84.6 × (total_syllables / total_words)
```

Interpretation:
- **90–100** — 5th grade. Very easy. Suitable for young kids or ESL.
- **80–89** — 6th grade. Easy.
- **70–79** — 7th grade. Fairly easy.
- **60–69** — 8th–9th grade. Plain English. **Target zone for web content.**
- **50–59** — 10th–12th grade. Fairly difficult.
- **30–49** — College level. Difficult. Most web content here is losing readers.
- **0–29** — Academic/legal. Best for specialist audiences only.

## Computing it without external libraries

You're probably running this inside a Claude session with no guaranteed NLP package access. Use heuristics.

### Counting sentences
Split on `.`, `!`, `?` — then discard empty fragments. Good enough for the score. Abbreviations ("e.g.", "Mr.") introduce noise but don't meaningfully change the band.

### Counting words
Split on whitespace after stripping markdown/HTML. Good enough.

### Counting syllables (the tricky part)

Use this heuristic per word — it's the standard approximation and gets within 5% of a dictionary lookup for English:

1. Lowercase the word.
2. Count vowel groups: consecutive vowels (`a`, `e`, `i`, `o`, `u`, `y`) count as one syllable each.
3. Subtract 1 if the word ends in a silent `e` (but not if that's the only vowel group).
4. Minimum of 1 syllable per word.

Example: "readability" → vowel groups are `ea`, `a`, `i`, `i`, `y` → 5 syllables → correct.
Example: "make" → vowel groups `a`, `e` → 2, subtract silent `e` → 1 syllable → correct.

### Python implementation (if you need it in a script)

```python
import re

def count_syllables(word):
    word = word.lower()
    word = re.sub(r'[^a-z]', '', word)
    if not word:
        return 0
    vowels = 'aeiouy'
    count = 0
    prev_was_vowel = False
    for ch in word:
        is_vowel = ch in vowels
        if is_vowel and not prev_was_vowel:
            count += 1
        prev_was_vowel = is_vowel
    if word.endswith('e') and count > 1:
        count -= 1
    return max(1, count)

def flesch_reading_ease(text):
    sentences = [s for s in re.split(r'[.!?]+', text) if s.strip()]
    words = re.findall(r"[A-Za-z']+", text)
    if not sentences or not words:
        return None
    total_syllables = sum(count_syllables(w) for w in words)
    return 206.835 - 1.015 * (len(words) / len(sentences)) - 84.6 * (total_syllables / len(words))
```

## Per-sentence length analysis

Also report:
- Average sentence length (words / sentences)
- Longest sentence (word count + the actual sentence)
- Count of sentences over 25 words

These are more actionable than the Flesch score. "Your average sentence is 31 words; here are the 4 longest" is a fixable observation.

## Per-paragraph length analysis

For web content:
- Ideal: 2–4 sentences per paragraph
- Flag: any paragraph over 6 sentences or over 120 words
- Flag: walls of text (sections with no paragraph breaks for >200 words)

## What the user should do with this

Don't tell the user "your Flesch score is 47." Tell them:
- "This reads at a college level (Flesch 47). For a consumer audience, aim for 60–70."
- "Your average sentence is 28 words — tighten the 4 longest ones listed below."
- "Paragraph 3 is 180 words with no break. Split it into 3 paragraphs around the natural transitions."

Make the feedback actionable, not just descriptive.
