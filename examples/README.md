# Examples and validation evidence

## Empty ledger

`empty-ledger.json` is an unfilled template with an illustrative URL. It is not a
recommendation. The scorer correctly classifies it as provisional.

## Live research smoke test

`live-audit-evidence.json` records a limited manual audit performed on 27 October
2026. `live-audit-report.json` is the actual result of running Commeto's helper on
that ledger.

The audit used an MIT course page, publisher-provided timed captions, and Cornell
reference notes. Exact source URLs and scope are in the ledger. No third-party
transcript is redistributed.

The result is **provisional**, with no public rubric score. A prestigious publisher
and accessible captions do not override incomplete coverage or unresolved
evidence. No timestamps, publication dates, durations, or missing analytics were
invented to obtain a passing result.

Reproduce the calculation:

```sh
python3 plugins/commeto/skills/video-research/scripts/evaluate.py \
  examples/live-audit-evidence.json --output /tmp/commeto-audit.json
```

The assessment timestamp changes; the eligibility decision and rubric calculation
should remain the same. This reproduces the calculation, not the live web research.
Source availability may change.

## Synthetic tests

The unit tests use synthetic `example.org` evidence to verify scoring boundaries,
missing-data behavior, contradictions, timestamps, and result limits. Those
fixtures are not real recommendations or factual-verification benchmarks.

The live test was performed by the authoring assistant. Independent end-user and
automatic skill-activation evaluations have not yet been performed.
