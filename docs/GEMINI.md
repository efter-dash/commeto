# Use Commeto in Gemini

## Gemini app: no coding needed

1. Open [Gemini](https://gemini.google.com/) on your computer.
2. Open **Gems**, then **New Gem**, and name it **Commeto**.
3. Open [Commeto instructions](../platforms/gemini/INSTRUCTIONS.md) and copy the text into the Gem's **Instructions** box.
4. Save, open Commeto, and ask what you want to learn.

Example: “Find three beginner furniture-making videos. Look for comments from
people who actually built the project, and mention missing steps or problems.”

Google's current help says personal-account Gems will start transitioning to
skills in November 2026. If your interface has changed, follow Google's current
setup help and reuse the same instruction text; do not assume a ZIP import is supported.

## Gemini CLI

For people who already use Gemini CLI, the repository includes an extension:

```sh
gemini extensions install https://github.com/efter-dash/commeto
```

Restart Gemini CLI, then ask it to use Commeto. This command uses the default
branch, so it includes this version only after these changes are merged.
To try an unmerged version, install from its local checkout instead:

```sh
gemini extensions install /absolute/path/to/commeto
```

The extension loads `GEMINI.md`. It needs no separate Commeto account or API key.

## What to expect

Gemini can only use sources and tools available in your account and session.
These instructions do not add a comments API, download videos, or unlock transcripts.
When comments cannot be inspected, viewer value stays unknown.

The files have been checked locally. Live installation and research inside Gemini
have not yet been tested by this project.

[Official Gem setup help](https://support.google.com/gemini/answer/15146780) ·
[Official Gemini CLI extension help](https://geminicli.com/docs/extensions/reference/)
