# Naming Pattern Library

A catalog of domain-naming patterns, each backed by real, already-famous
brands that used it. Patterns are structural — they describe a way of
forming a name, not a promise that the pattern performs the same for every
product.

## Contents

- [How to use this library](#how-to-use-this-library)
- [The four slots](#the-four-slots)
- [Two independent axes: product-fit vs. structural risk](#two-independent-axes-product-fit-vs-structural-risk)
- [The clean ⟺ opaque law](#the-clean--opaque-law)
- [Pattern catalog](#pattern-catalog)
- [Generating new patterns for a new product](#generating-new-patterns-for-a-new-product)
- [Worked example: one case study](#worked-example-one-case-study)

## How to use this library

**The patterns are deliberately unranked.** A tier list built from one
product's results confuses "this pattern fit that product's vocabulary" with
"this pattern is better". A Latin place-suffix (`-arium`) did well for a
product about rooms and has no reason to help a payments app. Don't rank
patterns from a past project; judge each one against the product at hand.

Every pattern is a formula over the product's own four slots (below). Pick
patterns by asking two separate questions, not one score:

1. **Does this product have a natural filler for this pattern's slot?** A
   place-suffix needs the product to be about a place. An occupational
   suffix (`-wright`) needs the product to *build* something. A pattern
   with no natural filler will produce awkward, forced names no matter how
   well it performed elsewhere.
2. **Is this pattern's *shape* itself risky, independent of the product?**
   Some patterns are famous enough that domainers specifically pre-empt
   them (see Structural Risk below); that risk doesn't change with what
   you're naming.

## The four slots

Extract these once per product; every pattern below is a formula over them:

- `[VERB]` — the core action the product performs or lets the user take.
- `[NOUN]` — the object being transformed or managed.
- `[MECHANISM]` — the technical transformation itself.
- `[AUDIENCE/OUTCOME]` — who uses it, or the state they end up in.

## Two independent axes: product-fit vs. structural risk

**Product-fit** must be judged fresh for every product — there is no
universal answer. A pattern that produces a perfect, meaningful name for one
product can produce nonsense for another, because the fit comes from
whether the product's own vocabulary has a natural filler for that
pattern's slot, not from any property of the pattern itself.

**Structural risk**, by contrast, genuinely is general — it's a property of
how *famous* or *predictable* the pattern's shape is, independent of any
product:

| Risk factor | Why it's product-independent | Example |
|---|---|---|
| **The pattern is a well-known convention** | Domainers specifically target famous naming conventions for resale or pre-registration, regardless of what anyone is naming | The `-ify` suffix (Spotify, Shopify) is copied often enough that fresh `-ify` coinages are pre-empted at a high rate no matter the product |
| **The output shape is squatter bait** | Short, pronounceable, meaningless strings are bought purely for resale value, independent of any brand meaning | Bare 4-letter CVCV invented strings (no product-specific meaning at all) are squatted near-universally |
| **The vocabulary is IP-adjacent** | Domain-squatting inventories specifically include large mythology/fantasy name lists, regardless of category | Minor, obscure deity names are claimed at a rate that has nothing to do with any one product |
| **The semantic field is an oversubscribed business cliché** | Some concepts (e.g. "we reveal hidden value") are used as a pitch across totally unrelated industries, so the vocabulary for them is crowded independent of category | A set of Latin "reveal/unlock" verbs turned out to be independently claimed by finance, water-treatment, and IT-consulting firms with nothing in common |

Use this table to flag *why* a pattern might be hard, separately from
whether it fits the current product.

## The clean ⟺ opaque law

Independent of pattern choice: a name fails a search-signal check for
exactly one of four reasons, in roughly this order of how hard they are to
spot on availability alone:

1. **It's a real word or phrase in English** — any part of speech, any
   register, including rare/archaic words.
2. **It's a real word in *any* other language, including constructed
   ones** — obscurity is not the same as unclaimed. A word that looks like
   an obscure dictionary entry can turn out to be a standard clinical,
   legal, or business term in active use somewhere.
3. **It's real jargon from an active professional or hobbyist community** —
   the most dangerous failure mode, because it clears every general check
   yet collides precisely with the target early-adopter audience. A
   coined-sounding name that turns out to be a term of art in the
   product's own field is worse than an obviously-taken common word,
   because it looks safe right up until it isn't.
4. **It's an oversubscribed generic business metaphor** — see the last row
   of the risk table above.

## Pattern Catalog

Every pattern names a formula. Exemplars are real, verifiable brand names —
where no strong tech-brand exemplar exists, that's stated plainly rather
than invented.

### Blending & Compounding

| Pattern | Formula | Real-world exemplars | Notes |
|---|---|---|---|
| Portmanteau | blend two words at a shared sound | Instagram (instant + telegram), Groupon (group + coupon), Pinterest (pin + interest) | "Obvious" portmanteaus get independently reinvented by unrelated people — finding the same blend already used by two unconnected entities is a signal to abandon that specific blend, not just respell it |
| Compound-clip | join two words, clipping one or both | Netflix (internet + flix), FedEx (federal + express), Microsoft (microcomputer + software) | — |
| Two short words, non-obvious pairing | `[word]` + `[unrelated concrete word]` | Dropbox, Facebook, WhatsApp, Snapchat | Works best when the pairing creates a small mental image, not just two nouns stapled together |
| Kenning / concrete-noun compound | `[concrete noun]` + `[concrete noun]` | Matterport (matter + port), Airbnb (air bed & breakfast, clipped), Basecamp | Identify the category incumbent's own naming suffix first (e.g. a dominant player owning `-port` in 3D real estate) and avoid reusing it — both squatted and a confusion risk |

### Prefix & Suffix Coinage

| Pattern | Formula | Real-world exemplars | Notes |
|---|---|---|---|
| Prefix + real verb/noun | re-/un-/de-/in-/sub-/inter- + `[root]` | Substack (sub + stack), Intercom (inter + com), Invision (in + vision), Outschool (out + school) | The *obvious* prefix is often taken while an equally natural sibling isn't — try several prefixes on the same root before moving on |
| Suffix coinage (-io/-ia/-a) | `[root]` + io/ia/a | Twilio, Klarna, Wistia, Figma, Canva | — |
| "-ify" verb coinage | `[root]` + -ify | Spotify, Shopify | Famous *because* it's copied — high structural risk, expect heavy pre-emption regardless of product |
| Latin `-arium`/`-orium` place-suffix | `[root]` + arium/orium | No widely-known standalone tech-brand exemplar; validated instead by ubiquitous English vocabulary (aquarium, terrarium, planetarium, sanitarium, moratorium) | Only fits a product whose core concept is a *place* or *container* — verify the coinage is grammatically sound before trusting a claimed meaning |
| "-atory" place-suffix | `[verb-stem]` + -atory | Same as above — validated by vocabulary (observatory, laboratory, conservatory), not by a famous brand | Avoid roots that echo the family's negative members (crematory, lavatory, purgatory) |
| Occupational "builder" suffix | `[noun]` + -wright/-smith | Blacksmith (a real CI/build-infrastructure company); the underlying pattern is validated by common English surnames (Wainwright, Cartwright, Goldsmith) | Needs the product to *build* or *craft* something as its core verb — a natural fit for construction/creation tools, forced for most others |
| Coined institutional suffix | `[noun]` + -eum/-drome/-plex/-dome | Cineplex (a real, publicly-traded cinema chain), Astrodome (the original domed stadium) | `-drome` in particular risks phonetic collision with unrelated famous media — say candidates aloud and check what they auto-correct to |
| Old English "-stead" | `[noun]` + -stead | Homestead (a former Intuit website-builder product) | Niche pattern; limited modern brand precedent beyond that one case |
| "-hub" suffix | `[noun]` + hub | GitHub, HubSpot | Extremely well-known convention — high structural risk of pre-emption regardless of product |
| "-ery" suffix | `[root]` + -ery | No strong tech-brand exemplar found; validated by common vocabulary (bakery, gallery, nursery) | Diminutive-adjacent register — reads more artisanal/small than "platform" |
| Constructed-language place-suffix | `[root]` + a constructed language's own place/ability suffix (e.g. Esperanto *-ejo* "place," *-ebla* "-able") | No known brand exemplar — genuinely unmined territory | Precisely *because* no major brand has done this, it can be unusually clean; needs the product to have a real conceptual fit with the suffix's specific meaning (a "place" suffix still needs the product to be about a place) |

### Borrowed & Foreign Vocabulary

| Pattern | Formula | Real-world exemplars | Notes |
|---|---|---|---|
| Direct foreign-word borrow | a real word from another language, used as-is | Uber (German "over"), IKEA (founder's initials + farm and village names), Nokia (a Finnish town), Volvo (Latin "I roll") | Check the word isn't *also* a live term of art or brand somewhere else — obscurity in your own language isn't obscurity everywhere |
| Latin/Greek root coinage | a fabricated word built from real classical roots, not a direct borrow | Verizon (veritas + horizon), Acura (from "accurate"), Meta (Greek prefix "beyond") | Verify the resulting word is actually grammatical in the source language before trusting a claimed etymology |
| Mythology / classical figures | a deity or mythic figure's name, chosen for a fitting domain | Nike (Greek goddess of victory), Amazon (mythical warrior women), Ajax (Trojan War hero) | High structural risk — domain-squatting inventories specifically include large mythology-name lists, even for obscure minor figures |

### Repurposed Real-World Vocabulary

| Pattern | Formula | Real-world exemplars | Notes |
|---|---|---|---|
| Repurposed evocative noun | `[noun]` unmodified | Apple, Amazon, Oracle, Notion, Ramp, Linear, Slack | Bare gravitas-nouns are among the most contested strings on the internet — expect most of the obvious ones gone |
| Architectural/technical vocabulary | a real construction/engineering term | Keystone (OpenStack's identity-service component), Cornerstone (Cornerstone OnDemand, enterprise HR tech) | — |
| Craft & weaving vocabulary | a real textile/craft term | Loom (video messaging, acquired by Atlassian), Fabric (used by several dev-tools/data companies) | — |
| Surveying/measuring vocabulary | a real surveying term | Benchmark (Benchmark Capital, a major VC firm), Compass (Compass Inc., NYSE-listed real estate tech) | — |
| Cartography/mapping vocabulary | a real mapping term | Atlas (MongoDB Atlas) | — |
| Vantage/aerial-perspective vocabulary | a bird's-eye or elevated-view term | Birdeye (reputation-management SaaS) | — |
| Optics/light vocabulary | a real optics term | Lucid (Lucidchart, Lucid Motors), Prism | — |
| Theater/stage vocabulary | a real stagecraft term | Greenroom (Spotify's live-audio app, later discontinued) | Even a discontinued product is evidence the pattern was viable enough for a major company to ship it |
| Real jargon from the product's own technical field, used as the brand | the field's *own* working term, reused as a name | Docker (a literal dockworker, repurposed for the shipping-container metaphor), Kubernetes (Greek for "helmsman," a deliberate nautical-steering metaphor) | **The highest-variance pattern in this catalog.** Docker and Kubernetes show it can work spectacularly. The risk: if the exact term is *already* the live, current working vocabulary of an active community (not just an interesting etymology), it collides with your own most likely early-adopter audience. Check whether the term is a historical/etymological curiosity (lower risk) or something people are using *right now* in forums, papers, or plugins in the product's own field (high risk) before committing |

### Conceptual & Metaphorical Coinage

| Pattern | Formula | Real-world exemplars | Notes |
|---|---|---|---|
| Abstract/emotional compound | a feeling or state, named directly | Notion, Calm, Headspace | — |
| Fantasy/storybook concept (not copyrighted IP) | a folklore concept or word, not a trademarked proper noun | Fable (an AI/entertainment studio), Mythic (an analog AI-chip company) | Stay on the *concept*, not the specific copyrighted name — a vivid, "obvious" pitch metaphor (e.g. "bigger on the inside") is exactly the kind of thing a real company in an adjacent space has already claimed |
| Sci-fi concept naming | a real word evoking a science-fiction idea, not licensed IP | Nebula, Replika (AI companion app) | — |
| Transformation/hidden-depth metaphor | an object whose ordinary exterior hides a striking interior | Crystal (Crystal Knows, personality-insights SaaS) | A vivid transformation image is exactly the kind of thing an aesthetic/lifestyle content community (interior design, crafts) may have already turned into a social-media trend — check hashtag usage, not just company names |
| Holographic/dimensional-reveal naming | a real or coined word evoking a flat image becoming dimensional | HoloLens (Microsoft's AR headset) | Also check for adjacent big-retailer product lines — this exact concept has been used as an in-house VR/AR feature name by large non-tech companies (home-improvement, retail) |
| "Materialize/reveal/manifest" vocabulary | a verb for something becoming real or visible | No single dominant famous-brand exemplar found; this entire semantic field is used by many small, unrelated companies rather than owned by one major brand | Treat as a crowded generic metaphor (see the Structural Risk table) rather than a fresh coinage |

### Phonetic & Structural Invention

| Pattern | Formula | Real-world exemplars | Notes |
|---|---|---|---|
| Phonetic invention (sound-symbolic, no real meaning) | an invented word chosen for how it sounds | Kodak, Xerox, Hulu, Google (from "googol," itself a playful misspelling) | Short invented words in this style are heavily squatted for resale — check availability before falling in love with the sound |
| Creative respelling | a real word, deliberately misspelled | Lyft (lift), Flickr (flicker), Fiverr (fiver), Tumblr (tumbler) | — |
| Verb/imperative or action-word branding | a real verb, used as a brand | Slack, Stripe, Zoom, Yelp | Works best when the product's core action is genuinely a single common verb |
| Single-letter or number-based thematic branding | a letter or number carrying the product's core concept | X (Twitter/X Corp's 2023 rebrand) | Very high structural risk — single letters and short numeric strings are near-universally already registered, and the letter itself is often already a brand's initial (unrelated industries) regardless of your intended meaning |
| "AI" hidden inside a real, thematically-apt word | capitalize the letters A-I inside an existing word that already means something apt | An emerging technique among 2020s AI startups; no single globally iconic exemplar yet | Genuinely new and unproven at scale — treat as speculative, not brand-validated, until it produces its own famous example |

## Generating new patterns for a new product

When the catalog above doesn't produce a good fit, generate fresh patterns
by asking:

- **What real professional or craft vocabulary is adjacent to, but not
  inside, the product's own industry?** Vocabulary from a genuinely
  different craft that borders the product's actual mechanism tends to
  yield real hits precisely because it's near the domain without being
  claimed by it.
- **What does the product's own internal technical vocabulary suggest?**
  Database table names, internal component names, the specific technique
  the product's engine uses — genuinely product-specific rather than
  generic, so worth a quick pass even though results are mixed.
- **What historical device or technique solved a version of this problem
  before software did?** A period-appropriate device, technique, or
  profession that solved an analogous problem is a reliable source of
  fresh, meaningful vocabulary — verify it doesn't already name a modern
  company in an adjacent space before committing to it.
- **What suffix or prefix family hasn't been tried yet, independent of
  meaning?** A pattern's *novelty* — how recently it's been mined by
  domainers — matters as much as its meaning. A well-known convention
  (`-ify`) and a fresh one built the same way on the same roots can have
  wildly different availability, for reasons that have nothing to do with
  which one sounds better.

## Worked example: one case study

The patterns above were assembled partly from a 17-round, ~1,190-domain
research project for an AI room-photo-to-3D product. That project is *one*
data point on product-fit, not a general ranking — reading it is useful for
seeing the *method* in action, not for assuming its specific results
transfer:

- A Latin place-suffix (`-arium`) and a constructed language's place-suffix
  (Esperanto `-ejo`) performed exceptionally well **specifically because
  the product was fundamentally about places** — a room, a space, a
  location you walk into. Neither pattern has an inherent reason to work
  for, say, a scheduling app or a payments product, which have no "place"
  concept in their own vocabulary to suffix.
- A prefix-coinage on an uncommon verb (`de-` + a verb naming the core
  transformation) produced the single cleanest, most-recommended name in
  that project — but the *verb itself* was product-specific; only the
  technique (try several prefixes on the product's own core verb, not just
  the obvious one) generalizes.
- Real technical jargon from the product's own field was tested
  extensively and failed almost every time, for the general reason
  described in the Repurposed Real-World Vocabulary section above — this
  part of the finding *does* generalize, because it's about how active
  communities behave, not about which product was being named.

For a new product, treat this project as a demonstration of the *process*
(generate wide, verify on two independent gates, read what real search
results say rather than trusting availability alone) rather than a source
of pattern rankings to copy.
