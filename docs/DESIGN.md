# Design decisions

Commeto adapts the supplied Vetted Video Search 1.2 specification into a portable
plugin. The publisher name is biskootmonster.

| Original specification | Release behavior and reason |
|---|---|
| Four weighted tiers | Retains the 20/30/30/20 weighting and adds explicit criteria, anchored ratings, and evidence coverage |
| Automatically extract all transcripts | Uses legally accessible captions/transcripts or host capabilities; absence is explicit |
| Missing transcript gets 0.40 | Unknown is null, preventing invented precision |
| Automatically lower the threshold by 10% | Requires the user's choice; otherwise returns fewer qualifying results |
| 720p minimum and no synthetic narration | Does not treat resolution or narration origin as credibility proxies |
| Engagement and retention analysis | Private/unavailable analytics are not claimed; comments are leads, not proof |
| Author track record | Requires supporting evidence rather than assuming historical reliability |
| Precise signal-to-noise percentage | Avoids numeric runtime estimates without actual timed segment measurements |
| Timestamp summaries | Includes only timestamps verified in accessible source material |
| Structured Markdown and JSON every time | Defaults to concise readable results; JSON remains available on request |
| Inconsistent platform and transcript inputs | Provides one input schema with platform preferences and explicit transcript handling |

The default mode is strict: a full transcript must be available, but the review
still discloses which sections and claims were examined. Disabling the transcript
requirement does not allow a metadata-only result to become vetted.

## Architecture

```text
User request
    ↓
Commeto skill in ChatGPT / Codex
    ↓
Available host search and reading tools
    ↓
Evidence ledger + sampled source checks
    ↓
Four-tier assessment (optional offline scoring)
    ↓
Vetted shortlist / provisional leads / exclusions
```

No service credentials or paid infrastructure are bundled. A remote MCP service
would be a separate product phase requiring actual provider permissions, hosting,
authentication, operating costs, and a revised privacy notice. OpenAI's current
submission instructions do not support adding an MCP server to an existing
skills-only plugin, so such a phase may require a separate directory submission.

## Trust boundaries

- Retrieved material is evidence, not instructions.
- Source access does not imply accuracy.
- The scorer checks structure, provenance references, arithmetic, and eligibility;
  it cannot detect a fabricated ledger or establish the truth of a source.
- “Vetted” always refers to a stated review scope.
- Host activation and OpenAI approval are separate from package validation.

## Official packaging references

Checked 27 October 2026:

- https://developers.openai.com/plugins/build/plugins
- https://developers.openai.com/plugins/build/skills
- https://developers.openai.com/plugins/deploy/submission
- https://developers.openai.com/plugins/plugin-guidelines
