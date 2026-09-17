# Domain Scoring Rubric

Score only after gathering availability, price, and search evidence. Penalize uncertainty instead of pretending it is confidence.

## Calibrate Expectations First

**Expect a low overall hit rate, and don't read it as a sign something is
being done wrong.** Most candidates checked will already be taken, and most
of what *is* available will be available precisely because it means
nothing — see `naming-patterns.md`'s clean ⟺ opaque law. Generate wide (40+
candidates) rather than narrowing early.

The actual yield on any given pattern varies by product, not by a fixed
rate — it depends on how well that product's own vocabulary fills the
pattern's slot (see `naming-patterns.md`'s product-fit vs. structural-risk
framing). As one illustrative data point: a 17-round, ~1,190-domain project
found real availability among *meaningful* candidates running close to 4%
overall, and only ~15–20% of registrar-available names survived a real
search-signal check — useful for calibrating that low yield is normal, not
as a target rate to expect on a different product or pattern.

## 100-Point Model

| Category | Points | How to score |
|---|---:|---|
| Business fit | 20 | Directly expresses the idea, audience, outcome, or differentiator. |
| Traffic intent | 20 | Category/problem searches show demand and commercial or repeat-use intent. |
| Search signal/noise | 20 | Exact-name SERPs are clean enough to own; low unrelated noise. |
| Brand quality | 15 | Short, pronounceable, memorable, spellable, visually clean. |
| Availability/economics | 15 | Available now, supported by a credible registrar, normal renewal economics. |
| Risk/defensibility | 10 | Low trademark/entity risk and not easily confused with incumbents. |

## Quick Scoring Anchors

Business fit:
- 18-20: instantly explains product/category or desired outcome.
- 12-17: related and credible, but needs a tagline.
- 6-11: abstract or partially related.
- 0-5: misleading or disconnected.

Traffic intent:
- 18-20: category has obvious buyer/problem searches and content angles.
- 12-17: moderate demand or strong niche intent.
- 6-11: plausible but unproven demand.
- 0-5: no clear search behavior or too broad to target.

Search signal/noise:
- 18-20: exact phrase is clean, no dominant unrelated entity.
- 12-17: some noise, but brand can plausibly win.
- 6-11: crowded or ambiguous.
- 0-5: dominated by another entity or toxic associations.

Brand quality:
- 13-15: short, easy to say, easy to spell, sticks in memory.
- 9-12: solid with minor friction.
- 5-8: awkward length, spelling, or pronunciation.
- 0-4: confusing, ugly, or hard to share verbally.

Availability/economics (price means the higher of first-year and renewal):
- 13-15: registrar-confirmed available at an ordinary price.
- 9-12: registrar-confirmed available, but a pricier TLD or a renewal above the first-year price.
- 5-8: premium, expensive, or not sold by the intended registrar.
- 0-4: taken, or not confirmed by a registrar (including an RDAP-only "unregistered").

Risk/defensibility:
- 9-10: no obvious conflicts and enough distinctiveness.
- 6-8: mild entity or trademark noise.
- 3-5: meaningful collision risk.
- 0-2: likely conflict, typosquat, or same-category incumbent.

## Hard Rejections

Reject or quarantine domains with:

- Taken, or a registry that accepts no new registrations.
- Same-category trademark or confusingly similar incumbent.
- Severe adult, scam, malware, hate, or illegal associations.
- Renewal or premium price outside the user's stated budget.
- TLD unavailable through the user's intended registrar when registrar choice matters.
- An expired or dropped domain wanted for its backlinks or leftover traffic.

## Recommendation Labels

- `Buy now`: score 80+, registrar-confirmed available, affordable to renew, low risk.
- `Strong shortlist`: score 70-79, registrar-confirmed available, one manageable weakness.
- `Watch`: promising, but availability, price or risk is unresolved. Every domain a registrar hasn't confirmed lands here at best.
- `Avoid`: taken, overpriced, high-noise, or high-risk.

`scripts/score_domains.py` applies these caps, so a high score can't promote an unverified domain.
