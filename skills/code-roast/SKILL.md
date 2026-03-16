---
name: code-roast
description: >
  Roast a codebase with a brutally honest, funny code quality audit and a shareable report card.
  Analyzes the repo for shame commits, TODO graveyards, debug leftovers, god files, empty error
  handlers, deep nesting, and test-coverage gaps — then grades it A+ to F with a witty narrative
  and actionable fixes. Use when the user says: "roast my code", "roast this repo",
  "audit my codebase", "how bad is my code", "code roast", "grade my code", or anything
  implying a humorous or brutally honest code quality review.
---

# Code Roast

Give any codebase a Gordon-Ramsay-style roast: a letter grade, a Hall of Shame, genuine Bright Spots, and a Prescription — all in a shareable Markdown report.

## Workflow

### Step 1 — Identify the repo root

If the user didn't specify a path, use the current working directory as the repo root. Confirm it is a git repo or a directory with code files. Store it as `<repo_root>`.

### Step 2 — Run the analyzer

```bash
cd <skill_dir>/scripts
uv run analyze.py <repo_root> --debug
```

This emits a JSON object to stdout with 9 shame-category metrics. Copy the full JSON — you'll need it in Step 3.

> If `uv` is not available, fall back to: `python3 analyze.py <repo_root> --debug`

### Step 3 — Score and write the roast

1. Open `references/roast-rubric.md` and follow it exactly:
   - Apply the **penalty table** for each of the 9 categories to get a total penalty score.
   - Look up the **grade tier** and its tagline.
   - Write each section using the **section templates** as your guide.

2. Write the roast to `<repo_root>/code_roast_YYYY-MM-DD.md` using today's date.

3. The report must contain exactly these sections in order:
   - Header with repo name, grade, tagline, and file/line counts
   - **The Verdict** — 2–3 sentence overall tone-setter
   - **Hall of Shame** — one subsection per triggered category (penalty > 0), skipping clean ones
   - **Bright Spots** — 1–3 genuine positives
   - **The Prescription** — 3–5 numbered, actionable fixes
   - Footer with the shareable X/Twitter link (pre-filled with the grade)

### Step 4 — Present the roast

After writing the file, display the full roast inline in the conversation so the user sees it immediately. Then tell them the file path.

## Key Rules

- **Be specific**: always use real file names, real counts, real commit messages. Vagueness is not funny.
- **Skip clean categories**: if a category has penalty 0, don't mention it in the Hall of Shame.
- **Always end with empathy**: The Prescription and Bright Spots soften the roast. Never end on pure shame.
- **Tone**: dry wit, not cruelty. The rubric's voice section has examples.
- **Length**: 300–600 lines in the output file is ideal — long enough to be thorough, short enough to share.

## Resources

- `scripts/analyze.py` — static analysis engine; outputs JSON metrics to stdout
- `references/roast-rubric.md` — scoring tables, grade tiers, tone guide, section templates, output file spec
