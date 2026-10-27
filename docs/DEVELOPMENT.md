# Technical guide

The main research skill lives in `plugins/commeto/skills/video-research/`.
Claude receives the same skill and supporting references in a ZIP. Gemini uses
self-contained instructions shared by its Gem and CLI extension.

## Validate and package

Python 3.10 or newer is needed for these optional developer tools:

```sh
python3 -m unittest discover -s tests -v
python3 tools/build_release.py
python3 tools/build_platforms.py
```

Packages and checksums are written to `dist/`. The platform builder checks that
Gemini's instruction copies agree and verifies the contents of the Claude ZIP.
No build command contacts a video platform or installs anything in an AI app.

## Optional credibility reports

```sh
python3 plugins/commeto/skills/video-research/scripts/evaluate.py --template --output my-ledger.json
# Fill the ledger using evidence you actually inspected, then:
python3 plugins/commeto/skills/video-research/scripts/evaluate.py my-ledger.json --output my-report.json
```

The helper calculates the existing credibility rubric; it does not search,
verify claims, fetch comments, or calculate viewer value. Viewer feedback is
reported separately using the skill's qualitative guidance.

See the [rubric](../plugins/commeto/skills/video-research/references/rubric.md),
[evidence format](../plugins/commeto/skills/video-research/references/evidence-format.md),
[examples](../examples/README.md), and [design notes](DESIGN.md).
