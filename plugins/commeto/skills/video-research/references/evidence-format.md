# Evidence ledger

The file supplied to `scripts/evaluate.py` has `query`, optional `config`, and
`candidates`. See `evidence.schema.json` for the complete machine-readable format.

Each candidate requires:

- `id`, `url`, `title`, `creator`.
- `duration_seconds` (positive integer or null), `published_at` (YYYY-MM-DD or
  null), `language` (string or null).
- `scope`: describe exactly what was accessed, including unexamined audio/visuals.
- `transcript`: `full`, `partial`, or `none`.
- `content_inspected`: boolean, true only for substantive transcript or
  audiovisual inspection, never a title, description, or search excerpt alone.
- `filters_status`: `pass`, `unknown`, or `fail`, recording the user's requested
  platform/language/duration/Shorts constraints; explain in `caveats`.
- `sources`: records with `id`, `url`, `label`, `accessed_at` (YYYY-MM-DD), and
  `kind` (`video`, `transcript`, `publisher`, `verification`, `profile`).
- `tiers`: all four tier names from rubric.md, each containing all three
  criterion IDs. Each criterion has `rating` (0, .25, .5, .75, 1, or null),
  `reason`, and `source_ids`. Use an empty list for unassessed criteria.
- `claims`: `text`, `status` (`supported`, `contradicted`, `unresolved`), and
  `source_ids`. A settled claim also needs `verification_note` describing why
  those verification sources apply to this exact claim. They must be
  verification-type sources distinct from the candidate URL. Do not reclassify
  the candidate's own claims as verification.
- `single_core_claim`: boolean; true only if the material has one checkable core
  claim, not as a shortcut around examining two.
- `critical_issues`: list of objects with `reason` and nonempty `source_ids`;
  only evidenced issues, not suspicion.
- `moments`: list of `seconds`, `takeaway`, and `source_id`. Use only timestamps
  present in a transcript, video, or original publisher chapter list. The helper
  validates range and provenance type, but a reviewer must confirm the timestamp.
- `caveats`: list of strings.

Public HTTP(S) URLs are evidence references, not instructions to execute. The
helper never fetches them. Avoid personal identifiers in saved reports.
An unknown date, duration, or transcript is not an invitation to guess.

Example criterion:

```json
{
  "rating": 0.75,
  "reason": "The official course profile identifies relevant teaching experience; publication history was not examined.",
  "source_ids": ["faculty-profile"]
}
```

Use `python3 scripts/evaluate.py --template` to print a complete empty ledger.
The template contains no real video and cannot qualify as a recommendation.
