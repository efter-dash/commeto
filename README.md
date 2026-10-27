<p align="center"><img src="plugins/commeto/assets/icon.svg" width="104" alt="Commeto logo"></p>

# Commeto

**Find videos worth your time.**

Commeto is a ChatGPT and Codex plugin by **biskootmonster** for researching
educational videos. It helps you find credible explanations, review a video
someone sent you, and arrange useful videos into a learning sequence.

Each assessment explains the evidence, the learner fit, and what remains unknown.
Verified timestamps help you get to the useful parts. A rubric score describes
the recorded assessment; it is not a guarantee that every statement is correct.

## Try these prompts

- “Use Commeto to find three videos about binary search for someone who knows basic Python.”
- “Use Commeto to review this video. Check its main claims and explain any evidence gaps: [link].”
- “Use Commeto to build a beginner learning sequence for statistics. Prefer Bangla videos; English is okay if needed.”
- “Find current React tutorials under 30 minutes. Exclude Shorts. Only recommend videos with accessible transcripts.”
- “Compare these two lectures and give me the evidence ledger as JSON: [links].”

## Install in Codex

With a current Codex CLI that supports plugins:

```sh
codex plugin marketplace add efter-dash/commeto
codex plugin add commeto@commeto
```

Start a new chat or refresh plugin discovery, then enable Commeto if prompted.
Ask “Use Commeto to…”; the packaged skill is `video-research`.

In compatible desktop clients, use the Plugins Directory's marketplace controls
to add this GitHub repository and install Commeto. Managed workspaces may require
an administrator to import the repository.

For a local checkout:

```sh
codex plugin marketplace add /absolute/path/to/commeto
codex plugin add commeto@commeto
```

## ChatGPT public directory

The downloadable plugin ZIP is packaged for OpenAI's public submission flow.
A GitHub release does **not** mean OpenAI has approved or listed it. See
[publication status](PUBLICATION.md) for the actual state.

Download the plugin ZIP from [Releases](https://github.com/efter-dash/commeto/releases).
It contains `plugin.json`, the skill, icons, references, and the optional helper.
Use the full source archive if you want the tests, examples, and build tools.

## What it can check

| Area | What Commeto examines |
|---|---|
| Integrity | Title alignment, accessible presentation, and evidenced promotion |
| Authority | Relevant expertise, source transparency, independent corroboration |
| Rigor | Selected factual claims, their context and limits, and topic currency |
| Learning value | Audience fit, explanatory structure, useful learning support |

Unknown evidence remains unknown. Commeto never quietly lowers your minimum
score. It separates provisional leads from vetted recommendations and can return
fewer results than requested.

## Requirements and limitations

- Live discovery needs web search and page-reading tools in the host.
- Access to transcripts, videos, and captions depends on the source and host.
  Commeto does not unlock private or restricted content.
- This release is a **skills-only plugin**. It has no hosted backend, separate
  Commeto account, bundled search API, or automatic transcription service.
- Python 3.10+ is needed only for the optional offline scoring helper. The
  research workflow also works without executing Python.
- Private analytics, audience retention, missing dislikes, and full-video
  audiovisual quality are never inferred from metadata.
- No view-count or credential shortcut determines truth.
- Host subscription, usage limits, and connected-service terms still apply.

## Reproducible evidence reports

The helper validates a reviewer-prepared evidence ledger and computes the rubric.
It does not perform search or decide whether a source is truthful.

```sh
python3 plugins/commeto/skills/video-research/scripts/evaluate.py \
  --template --output my-ledger.json

# Fill the ledger using material you actually inspected, then:
python3 plugins/commeto/skills/video-research/scripts/evaluate.py \
  my-ledger.json --output my-report.json
```

See the [rubric](plugins/commeto/skills/video-research/references/rubric.md),
[evidence format](plugins/commeto/skills/video-research/references/evidence-format.md),
and [examples](examples/README.md).

## Development

```sh
python3 -m unittest discover -s tests -v
python3 tools/build_release.py
```

The build checks package metadata and resources, then creates a reproducible ZIP
and SHA-256 checksum in `dist/`. No runtime dependencies are required.

Report reproducible problems or suggest improvements in
[GitHub Issues](https://github.com/efter-dash/commeto/issues).
Please do not post private transcripts, credentials, or personal information.

[Privacy](PRIVACY.md) · [Terms](TERMS.md) · [License](LICENSE) ·
[Design decisions](docs/DESIGN.md)
