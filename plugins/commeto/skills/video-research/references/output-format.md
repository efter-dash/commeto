# Output contract

Default to a readable shortlist. Avoid exporting a large evidence ledger unless
the user requests it or a saved audit would materially help.

## A recommendation

**[Title](original video URL)** — Creator

Duration and date: checked values, or “not verified”.
Video language: checked value, or “not verified”.

**Fit:** why this video answers the user's question at the requested level.
**Assessment:** vetted within the stated scope / provisional / excluded.
**Rubric:** 0–1 score when evidence gates pass; otherwise “not scored”.
**Evidence coverage:** percentage of weighted criteria assessed, not confidence
in factual truth.
**Scope:** full/partial/no transcript, sections inspected, whether audiovisual
material was inspected, and date of this review.

**Viewer value:** strong / mixed / limited / unknown; comment themes, actual sample
count and ordering, review date, source links, and sample limitations. Separate from
the credibility score.

**Checks:** brief claim, result, source link, and caveat when needed.
**Moments:** verified `MM:SS` or `HH:MM:SS` timestamps with short takeaways.
Omit this section when none are verified.
**Limitations:** material unknowns, topic-specific outdated portions, sponsorship
when evidenced, and unexamined audio or visuals.

## Learning sequence

Order qualifying videos by prerequisites. Explain the purpose of each step and
one short exercise or check for understanding. Label assistant-created exercises
as suggestions. If verified durations are incomplete, give only the subtotal
for known durations and identify what is missing.

## JSON

The optional helper returns:

```json
{
  "schema_version": "1.0.0",
  "query": "...",
  "assessed_at": "ISO 8601 UTC",
  "config": {"min_credibility_score": 0.75, "require_transcripts": true, "max_results": 5},
  "results": [],
  "provisional": [],
  "excluded": [],
  "additional_qualified": [],
  "summary": {"requested": 5, "qualified": 0, "returned": 0, "shortfall": 5}
}
```

Each item retains its evidence ledger and adds `assessment`: tier scores and
coverage, overall coverage, conservative score, public rubric score (nullable),
decision, and reasons. `additional_qualified` holds qualified candidates outside
the requested result limit. The helper does not create evidence or interpret
transcripts. Its decisions are conditional on the supplied reviewer judgments.
