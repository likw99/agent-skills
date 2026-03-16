# Code Roast Rubric

This file is the **wit engine**: how to score raw metrics into a letter grade, and what to say.

---

## Scoring System

Each category contributes a **penalty score** (0 = clean, higher = more shame).
Sum all penalties → look up the grade tier.

### Category Penalties

#### 1. Shame Comments (TODO / FIXME / HACK etc.)
| Count | Penalty |
|---|---|
| 0 | 0 |
| 1–5 | 5 |
| 6–15 | 10 |
| 16–30 | 20 |
| 31–60 | 30 |
| 61+ | 40 |

#### 2. Debug Statements (console.log, print, debugger etc.)
| Count | Penalty |
|---|---|
| 0 | 0 |
| 1–3 | 5 |
| 4–10 | 15 |
| 11–25 | 25 |
| 26+ | 35 |

#### 3. Long Files (>300 lines each)
| Count | Penalty |
|---|---|
| 0 | 0 |
| 1–2 | 5 |
| 3–5 | 15 |
| 6–10 | 25 |
| 11+ | 35 |

#### 4. God Files (≥10 functions in one file)
| Count | Penalty |
|---|---|
| 0 | 0 |
| 1–2 | 10 |
| 3–5 | 20 |
| 6+ | 30 |

#### 5. Empty Catch / Bare Except Blocks
| Count | Penalty |
|---|---|
| 0 | 0 |
| 1–2 | 10 |
| 3–5 | 20 |
| 6+ | 35 |

#### 6. Commented-Out Code Lines
| Count | Penalty |
|---|---|
| 0 | 0 |
| 1–10 | 5 |
| 11–30 | 15 |
| 31–60 | 25 |
| 61+ | 35 |

#### 7. Git Shame Commits (ratio of shame commits to total)
| Shame Ratio | Penalty |
|---|---|
| 0–5% | 0 |
| 6–15% | 10 |
| 16–30% | 20 |
| 31–50% | 30 |
| 51%+ | 40 |

#### 8. Test Coverage (test files / source files)
| Ratio | Penalty |
|---|---|
| ≥0.8 | 0 |
| 0.5–0.79 | 5 |
| 0.2–0.49 | 15 |
| 0.05–0.19 | 25 |
| <0.05 | 40 |

#### 9. Deep Nesting (max indent depth found)
| Max Depth | Penalty |
|---|---|
| ≤4 | 0 |
| 5–6 | 10 |
| 7–8 | 20 |
| 9–10 | 30 |
| 11+ | 40 |

---

## Grade Tiers

| Total Penalty | Grade | Tagline |
|---|---|---|
| 0–15 | A+ | "This code is suspiciously clean. Are you sure you've shipped anything?" |
| 16–30 | A | "Genuinely impressive. Your future self will thank you." |
| 31–50 | B+ | "Solid craft with a few rough edges. The kind of code you'd cautiously show a senior engineer." |
| 51–70 | B | "Gets the job done. Like a car with a check-engine light you've been ignoring for six months." |
| 71–90 | C+ | "Functional but haunted. There are skeletons in these directories." |
| 91–110 | C | "This codebase has seen things. It doesn't talk about them." |
| 111–130 | C– | "Held together with console.logs and optimism." |
| 131–150 | D | "A brave monument to shipping fast and asking questions never." |
| 151–175 | D– | "This code is load-bearing technical debt. Do not remove anything." |
| 176+ | F | "We must never speak of this codebase again." |

---

## Roast Voice & Tone

Write in the style of a **sharp, funny tech roast** — think Gordon Ramsay meets a grumpy staff engineer with a blog.

- **Punchy**: Short sentences. Land the joke fast.
- **Specific**: Always call out the actual file, count, or metric. Vagueness is not funny.
- **Affectionate**: The roast is not cruel. It ends with empathy and actionable fixes.
- **Dry wit over snark**: "Your utils.js is a catch-all that caught too much" beats "lol this code sucks"
- **Always earn the punchline**: State the fact first, then land the joke.

### Vocabulary to use freely
- "abandoned dream", "graveyard", "archaeological dig", "load-bearing", "emotional support code"
- "future you will not be pleased", "this runs in production somewhere", "forensic accountants of software"
- "technically it compiles", "vibes-based error handling", "the comment says TODO but we all know"

---

## Section Templates

### The Verdict (2–3 sentences, overall tone-setter)
Open with the grade and one punchy overall observation.
Then one sentence acknowledging the positive (scale, shipping speed, ambition).
End with the most damning specific stat.

Example:
> "Your repo clocks in at a **C+** — functional, occasionally inspired, and held together by 47 TODO comments that have quietly given up hope. Points for actually shipping. Points deducted for the 312-line function in `processor.js` that nobody has touched in 847 days because everyone is afraid of it."

---

### Hall of Shame (one subsection per triggered category)

Only include categories where there's something worth roasting (penalty > 0). Skip clean categories.

#### TODO Graveyard
Open line: a quote or observation about the sheer volume.
Then the facts: count by type, oldest if from git blame, worst file.
```
> "Your codebase has 47 TODO comments. That's not a backlog, that's a support group."
- 31× TODO | 9× FIXME | 5× HACK | 2× XXX
- Worst offender: `src/utils/processor.js` (12 TODOs)
```

#### Debug Artifacts
```
> "`console.log('here')` is not a monitoring strategy."
- 23 debug statements survived the merge
- Top offender: `api/routes/users.js` (8 calls)
```

#### Long Files
```
> "Some of your files are longer than most developer attention spans."
- `src/services/DataService.js`: 847 lines (a short novel)
- `lib/utils.py`: 612 lines (a thriller with no resolution)
```

#### God Files
```
> "A file with 22 functions isn't a module, it's a lifestyle."
- `src/helpers/index.js`: 22 functions — does it even know what it is?
```

#### Empty Catches
```
> "Swallowing errors silently is the software equivalent of ignoring a check-engine light."
- 6 empty catch/bare except blocks found
- Every one of them is lying to you
```

#### Commented-Out Code
```
> "Dead code in comments is the ghost of features past. It cannot hurt you. But it will haunt you."
- 43 lines of commented-out code found lurking
- `src/legacy/transform.py` is 30% eulogy
```

#### Git Shame
```
> "34% of your recent commits contain the word 'fix', 'wip', or 'oops'. That's a vibe."
- Hall of fame entries:
  - `abc1234` — "fix fix fix please work"
  - `def5678` — "ok this one should actually work"
  - `ghi9012` — "lol"
```

#### Test Coverage
```
> "With a 0.04 test-to-source ratio, you're essentially testing in production."
- 1 test file for 28 source files
- Bravery, or hubris? The stack traces will decide.
```

#### Deep Nesting
```
> "Nesting 9 levels deep is not logic — it's origami."
- Max depth of 9 found in `src/parser/transform.js`
- If-else archaeology: bring a torch
```

---

### Bright Spots

Always include 1–3 genuine positives. Look for:
- Test files ratio ≥ 0.5 → "Your test coverage is actually solid. Respect."
- Zero empty catches → "Your error handling is non-ironic. This is rare."
- No debug statements → "Not a single rogue console.log. A true professional."
- Low shame-commit ratio → "Your commit messages tell a coherent story. Hire this person."
- Small file sizes → "Clean, focused files. You understand the single responsibility principle, at least in theory."
- Low TODO count → "You either finish your TODOs or you never write them. Both are valid."

If nothing is genuinely good, acknowledge the scale or shipping ambition:
> "You have shipped. That matters. Most perfect codebases never ship."

---

### The Prescription (3–5 actionable fixes)

Always end with concrete, prioritized fixes. Keep them punchy.

Format:
```
1. **Triage the TODO graveyard** — `grep -rn "TODO\|FIXME\|HACK" --include="*.js"`. For each one: fix it, delete it, or file a real ticket. Anything older than 90 days is not a todo, it's decoration.
2. **Delete the console.logs** — Run `grep -rn "console.log" --include="*.js" src/`. None of these belong in production.
3. **Break up `DataService.js`** — 847 lines is a monolith. Split by responsibility. Your future self will send you a thank-you note.
4. **Add a test** — Any test. Pick the scariest function in the codebase and write one test for it. Start the habit.
5. **Silence no errors** — Replace every empty catch block with at least `console.error(e)` or a proper logger call. Errors are trying to tell you something.
```

---

## Output File Spec

Write the roast to: `code_roast_YYYY-MM-DD.md` in the repo root.

### File Structure
```markdown
# 🔥 Code Roast: {repo_name}

**Grade: {grade}**
*"{tagline}"*

Analyzed {total_files} files · {total_lines} lines of code · {date}

---

## The Verdict

{verdict paragraph}

---

## Hall of Shame

{one subsection per triggered shame category, skipping clean ones}

---

## Bright Spots

{1–3 genuine positives}

---

## The Prescription

{3–5 numbered, actionable fixes}

---

*🔥 Roasted by Claude · [Share on X →]({X share link — see Rules below}) · Run `/code-roast` to get yours*
```

### Rules
- Use real file names, real counts — specificity is what makes it land
- The X share link in the footer should pre-fill this exact tweet (URL-encode the full text):
  ```
  Just ran /code-roast on {repo_name}. It got a {grade}.
  The Hall of Shame is brutal. 🔥
  #CodeRoast
  ```
  Use: `https://x.com/intent/tweet?text={encoded text}`
- Do not include raw JSON metrics in the output
- Total length: 300–600 lines is ideal. Long enough to be thorough, short enough to screenshot
- Use emoji sparingly: only 🔥, 💀, 🗑️, ⚰️, 🧪, 🌿 are appropriate
