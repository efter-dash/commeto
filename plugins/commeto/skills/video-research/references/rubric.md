# Commeto evidence rubric

Scores measure the assessment recorded in this run. They are not certifications,
probabilities, or empirical measurements of truth. Apply the same criteria to
large and small creators. Missing data is `null`, not a negative finding.

## Criteria

Each tier contains three equally weighted criteria:

| Tier / weight | Criterion IDs | Evidence to consider |
|---|---|---|
| Integrity / 0.20 | `title_alignment`, `presentation_accessibility`, `promotional_balance` | Whether the inspected content supports the title; comprehensibility and accessibility of the material actually available; evidenced promotional interruptions |
| Authority / 0.30 | `relevant_expertise`, `source_transparency`, `independent_corroboration` | Relevant work or demonstrated primary expertise; traceable citations and disclosure; corroboration outside the creator's own claims |
| Rigor / 0.30 | `claim_support`, `context_and_limits`, `currency` | Outcomes of sampled claim checks; appropriate scope, uncertainty, and caveats; currency for this particular topic |
| Utility / 0.20 | `audience_fit`, `explanatory_structure`, `learning_support` | Prerequisites and fit; logical explanation in inspected material; helpful examples, exercises, demonstrations, or chapter guidance |

An assessment of transcript readability cannot establish audio clarity. Mark
`presentation_accessibility` unknown unless the available presentation itself
can be assessed; scope any positive finding narrowly (e.g. readable transcript).
`source_transparency` can assess citations even if sponsorship status is unknown,
but say what was and was not checked.

## Anchored ratings

- `1.00`: strong evidence of meeting the criterion in the stated scope.
- `0.75`: meets the criterion with a minor limitation.
- `0.50`: mixed evidence or material shortcomings.
- `0.25`: weak support or major shortcomings.
- `0.00`: evidenced failure.
- `null`: unavailable or not examined.

Every non-null rating needs a short reason and at least one evidence source ID.
These are reviewer judgments, not values automatically inferred from metadata.
Use source access dates and an exact excerpt or location summary where useful.

## Calculation

For each tier, its score is the sum of known ratings divided by its number of
known ratings. With no known ratings its score is null. Tier coverage is known
criteria / 3.

Overall coverage = sum(tier weight × tier coverage).

The conservative composite = sum(tier weight × sum(known ratings) / 3).
Unknown criteria provide no earned points; do not renormalize the total over
observed evidence. This prevents a single positive source from producing a
perfect score. Only show the composite as a public rubric score for an eligible,
sufficiently evidenced assessment; otherwise show it as null. The helper exposes
`conservative_score` separately for auditability.

## Gates

**Evidence sufficiency**

- Overall coverage at least 0.75.
- At least two rated criteria in every tier.
- At least two substantive claims examined; if the material contains only one
  checkable core claim, one is enough and `single_core_claim=true` records this.
- Each supported/contradicted claim links to an authoritative verification source
  distinct from the candidate video. The record must explain why it is suitable.
- No unresolved core claim among the claims selected for checking.
- Full transcript when `require_transcripts=true`. This describes availability,
  not proof that every word was checked; `scope` must state what was examined.
- With `require_transcripts=false`, partial transcript or direct audiovisual
  inspection is still necessary for a vetted decision. Metadata alone is insufficient.

**Quality**

- Each tier score at least 0.50.
- Composite at or above the user's minimum.
- No material contradicted core claim and no evidenced critical integrity issue.
- User-specified filters satisfied. Unknown mandatory filters make the candidate
  provisional; known failures exclude it.

Known hard failures override missing evidence. Otherwise insufficient evidence
is provisional, not a negative finding. With adequate evidence, failing a quality
gate is excluded. Never lower a threshold automatically.

## Signals deliberately not required

Audience retention and many engagement analytics are not publicly available.
Public likes, comments, or views cannot establish truth, retention, or community
consensus. Do not infer missing dislikes. Comments may supply leads to verify,
not verdicts. Resolution, narration type, popularity, and academic titles are
not automatic pass/fail criteria. Credentials may support relevant expertise,
but primary work and accurate demonstrations can do so too.
