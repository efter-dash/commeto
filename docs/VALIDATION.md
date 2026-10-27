# Release validation

Validated on 27 October 2026.

## Passed

- Official Agent Plugins 1.0.0 manifest JSON schema.
- Skill Creator frontmatter and naming validation.
- Input and evidence JSON Schema definitions and example ledger validation.
- Listing text length limits, starter prompts, icon dimensions, referenced files,
  marketplace path, and archive layout.
- Nineteen automated tests covering threshold boundaries, missing evidence,
  transcript requirements, contradictions, duplicate claims, filter states,
  provenance references, timestamps, numeric validation, ranking, and immutability.
- GitHub Actions on Python 3.10 and 3.14:
  https://github.com/efter-dash/commeto/actions/runs/40552392754
- Installation from the public GitHub marketplace through `codex plugin`.
- A manual live-source audit using an MIT video page, public captions, and a
  Cornell reference; see the example ledger and generated report.

## Not established by these checks

- OpenAI public directory acceptance or approval.
- Automatic skill activation across all clients.
- Independent reviewer agreement with editorial scores.
- Factual accuracy of all videos, future source availability, or access to every
  platform's transcripts.

The scorer is deterministic over a supplied ledger. It does not authenticate
evidence or perform factual verification. The live example and synthetic tests
are deliberately labeled separately.


## 1.1.0 local validation (28 October 2026)

- Existing credibility test suite: 19 passed.
- Codex package and three portable deliverables built successfully.
- ZIP integrity, repeated-build hashes, Claude skill/source parity, and new guide
  links checked locally.
- Gemini CLI manifest version and both Gemini instruction copies agree.
- No Claude or Gemini live installation or video-research run performed.
- Viewer feedback guidance reviewed for inaccessible comments, small samples,
  mixed outcomes, generic praise, and unverified corrections. These are instruction
  reviews, not live platform behavioral tests.
