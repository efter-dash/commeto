# Use Commeto in Claude

## Claude web or desktop

1. Download `commeto-claude-1.1.0.zip` from [Releases](https://github.com/efter-dash/commeto/releases).
2. In Claude, enable **Code execution and file creation** (or **Create and edit files**) in Settings → Capabilities if needed.
3. Open **Customize → Skills**, click **+**, choose **Create skill**, then **Upload a skill**.
4. Upload the ZIP and enable Commeto's `video-research` skill.
5. Ask: “Use Commeto to find three furniture-making videos for a beginner. Check viewer comments for successful builds and missing steps.”

If the release asset is not available yet, download or clone the repository,
run `python3 tools/build_platforms.py`, and use the Claude ZIP in `dist/`.
Do not upload the whole repository ZIP as a skill.

Your organization may control skill availability. Enable web search when available;
the skill cannot grant web, transcript, or YouTube-comment access. When comments
cannot be read, Commeto reports viewer value as unknown.

## Claude Code

Copy the entire `plugins/commeto/skills/video-research` folder into your project's
`.claude/skills/` directory. Keep its references and scripts together. Start a new
session and ask Claude to use Commeto. The optional Python scoring helper is not
required for ordinary research.

These packages have been checked for structure and internal references. Live
installation and research inside Claude have not yet been tested by this project.

[Official Claude setup help](https://support.claude.com/en/articles/12512180-use-skills-in-claude)
