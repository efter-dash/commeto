<p align="center"><img src="plugins/commeto/assets/icon.svg" width="104" alt="Commeto logo"></p>

# Commeto

**Find videos worth your time. Learn something you can use.**

Commeto helps you choose useful videos on any learning topic—from furniture
making and cooking to coding, languages, photography, and career skills.
Tell it what you want to learn, or share a video you want checked.

It looks for clear teaching, practical takeaways, and **what viewers say they
actually learned or achieved**. When possible, it also checks the video's
explanations against reliable sources.

## What can I ask?

- “Use Commeto to find three furniture-making videos for a complete beginner.”
- “Find cooking tutorials where viewers say the recipe worked for them.”
- “Help me learn photography. Give me three videos in a sensible order.”
- “Find beginner Excel lessons in Bangla, under 20 minutes each.”
- “Is this video useful? Check the explanation and viewer feedback: [video link].”

You can specify your experience, preferred language, available tools, and time.

## How does it choose videos?

Commeto looks at two different things:

- **Viewer value:** Do comments describe successful results, better understanding,
  useful tips, missing steps, or problems? Specific experiences carry more weight
  than generic praise, likes, or repeated promotional messages.
- **Trustworthiness:** Does the explanation hold up when checked? Is there enough
  information to understand its limits and who it is suitable for?

Comments help reveal usefulness; they do not prove that advice is correct.
Commeto tells you when comments are unavailable, too few, or only partly checked.
It never invents comments or treats a popular video as automatically trustworthy.

You get video links, why each one fits, useful viewer feedback when accessible,
and any important gaps. Timestamps appear only when verified.

## Choose your app

| Where you want to use Commeto | How to start |
|---|---|
| **Codex** | Follow the installation steps below. |
| **Claude** | Download the Claude skill ZIP, then upload it under Customize → Skills. [Claude guide](docs/CLAUDE.md) |
| **Gemini** | Copy the [Commeto instructions](platforms/gemini/INSTRUCTIONS.md) into a Gem. [Gemini guide](docs/GEMINI.md) |
| **Gemini CLI** | Install the extension from this repository. [CLI steps](docs/GEMINI.md#gemini-cli) |

Downloadable packages are on [GitHub Releases](https://github.com/efter-dash/commeto/releases).
Use the files attached to the release, rather than GitHub's “Source code” ZIP.
If the new packages are not published yet, the guides explain how to use the source files.

### Install in Codex

In a Codex version that supports plugins, run:

```sh
codex plugin marketplace add efter-dash/commeto
codex plugin add commeto@commeto
```

Start a new chat and ask: **“Use Commeto to find three videos about…”**
In compatible desktop apps, you can also add this repository through the plugin
marketplace controls. Your workspace may require administrator approval.

### Use in Claude or Gemini

The [Claude guide](docs/CLAUDE.md) and [Gemini guide](docs/GEMINI.md) explain setup
step by step. These versions provide Commeto's research instructions; they do
not add a separate search or comments service to your app.

## A few things to know

- Commeto uses the search and reading tools available in your AI app.
- Some videos, transcripts, and comments cannot be accessed. Results will say so.
- It can suggest promising videos without calling them fully checked.
- It does not download videos, unlock paid content, or guarantee every claim.
- No separate Commeto account is needed. Your AI app's usual limits still apply.
- A GitHub download does not mean an app directory has approved Commeto.
  See [publication status](PUBLICATION.md).

Made by **biskootmonster**. Have an idea or found a problem?
[Open an issue](https://github.com/efter-dash/commeto/issues).

[Technical guide](docs/DEVELOPMENT.md) · [Privacy](PRIVACY.md) ·
[Terms](TERMS.md) · [License](LICENSE)
