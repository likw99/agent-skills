# LLM Daily Newsletter Template

Use this file as the canonical output format for `scripts/output/llm_newsletter_YYYY-MM-DD.md`.

## Output Template

```markdown
# LLM Daily
> Your daily briefing on large language models  
> **{date}**

## Highlights
- {3-5 bullets capturing the most important developments across all sections}

## Business
- **{company or event}** {what happened}. {why it matters}. [Source]({url})

## Products
- **{product or launch}** {what shipped or launched}. {who it serves, adoption signal, or notable reaction}. [Source]({url})

## Technology
- **{repo, model, or tool}** {what it is}. {technical relevance or differentiator}. [Source]({url})

## Research
1. **[{paper title}]({arxiv_url})** — {primary author} et al. {core contribution}. {why it matters}.
2. **[{paper title}]({arxiv_url})** — {primary author} et al. {core contribution}. {why it matters}.
```

## Formatting Rules

- Use clean markdown only. Avoid HTML, tables, and decorative glyph bullets.
- Use standard markdown bullets (`-`) for Highlights, Business, Products, and Technology.
- Use an ordered list (`1.`) for Research to make the papers easier to scan.
- Do not include a stats line below the date.
- Do not include a `Paper of the Day` subsection.
- Do not include a `Looking Ahead` section.
- Link descriptive text such as the paper title or source label. Do not paste naked URLs on separate lines.
- Keep each item compact: usually 1-2 sentences after the bold lead-in.
- Prefer the strongest items in each section over exhaustive coverage.
- Keep the tone crisp, editorial, and useful for a technically literate reader.

## Editorial Notes

- `Highlights`: 3-5 bullets. These should be the most important developments from the full briefing.
- `Business`: focus on funding, M&A, company strategy, and market signals.
- `Products`: focus on launches, notable product updates, and real user or developer adoption signals.
- `Technology`: focus on meaningful open-source repos, models, tooling, and infrastructure changes.
- `Research`: usually list 4-6 papers. Favor papers with clear practical relevance, strong methodological novelty, or broad impact.
