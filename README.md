# JQ AI Skills

Reusable AI skills by JQ AI SYSTEMS.

These skills are small, portable instruction folders for Claude/Codex-style workflows. They are published under the MIT License so you can adapt them for your own local setup.

[![Website](https://img.shields.io/badge/Website-ai.joaoqueiros.com-111827?style=for-the-badge)](https://www.ai.joaoqueiros.com)
[![License](https://img.shields.io/badge/License-MIT-059669?style=for-the-badge)](LICENSE)
[![Release](https://img.shields.io/badge/Release-v0.2.3-2563eb?style=for-the-badge)](https://github.com/jqaisystems/jqai-ai-skills/releases/tag/v0.2.3)

## Preview

![JQ AI Skills overview](assets/skill-library-overview.png)

![Skill folder structure](assets/skill-folder-structure.png)

![Skill packaging demo](assets/skill-packaging-demo.gif)

## Quick Start

1. Pick a skill folder from `skills/`.
2. Copy the whole folder into your local skills directory.
3. Restart or reload your AI coding tool.
4. Invoke the skill by name in your prompt.

Example prompts:

```text
Use $github-safe-publisher to prepare this repo for a public release.
Use $skill-reviewer to audit this downloaded skill before installing it.
Use $em-dash-remover to clean this landing page copy.
Use $demo-animation-v2 to create a responsive animated walkthrough.
```

## Skill Folder Structure

Each skill is packaged as a self-contained folder:

```text
skill-name/
  SKILL.md
  agents/
    openai.yaml
  assets/       optional templates, images, or reusable files
  references/   optional supporting docs
  scripts/      optional helper scripts
```

To create a new skill, copy [`skills/_template/`](skills/_template/) and replace the placeholder names, descriptions, and prompts.

## Skills Included

| Skill | File | Use |
|---|---|---|
| GitHub Safe Publisher | [`skills/github-safe-publisher/SKILL.md`](skills/github-safe-publisher/SKILL.md) | Prepare private work for public GitHub releases safely. |
| Web Scraper | [`skills/web-scraper/SKILL.md`](skills/web-scraper/SKILL.md) | Extract public page content safely into structured notes. |
| Skill Reviewer | [`skills/skill-reviewer/SKILL.md`](skills/skill-reviewer/SKILL.md) | Review AI skill files or folders for dangerous behavior. |
| Em Dash Remover | [`skills/em-dash-remover/SKILL.md`](skills/em-dash-remover/SKILL.md) | Clean one common AI-writing tell from copy. |
| Code Deduplicator | [`skills/code-deduplicator/SKILL.md`](skills/code-deduplicator/SKILL.md) | Safely consolidate repeated code patterns. |
| Demo Animation | [`skills/demo-animation/SKILL.md`](skills/demo-animation/SKILL.md) | Build legacy desktop-oriented product/demo walkthroughs. |
| Demo Animation V2 | [`skills/demo-animation-v2/SKILL.md`](skills/demo-animation-v2/SKILL.md) | Build recommended responsive demo walkthroughs. Includes [`assets/template.html`](skills/demo-animation-v2/assets/template.html). |

## Why This Matters

The skills repo is the technical credibility layer behind the client-facing systems. It shows how JQ AI SYSTEMS packages repeatable AI workflows into reusable instructions, review steps, and safety checks instead of relying on one-off prompts.

## Installation

For Claude Code/Codex-style local skills:

1. Create a local skills folder if you do not already have one.
2. Copy the selected skill folder from `skills/`.
3. Place the whole folder in your local skills directory.
4. Restart or reload your AI coding tool if needed.
5. Ask the tool to use the skill by name.

Only install skills you understand. Review the instructions before using them on private projects.

## Contributing

Use [`CONTRIBUTING.md`](CONTRIBUTING.md) for the expected folder format, metadata requirements, safety rules, and pre-submission checklist.

## Safety Notes

- These files are instructions, not secrets.
- Do not paste private API keys, passwords, tokens, client data, or credentials into prompts unless you fully understand where they will go.
- The `skill-reviewer` skill exists to help inspect third-party skill files before installing them.
- Run new skills on a test folder before using them in production work.

## License

Released under the [MIT License](LICENSE).

More systems and case studies: [ai.joaoqueiros.com/systems](https://www.ai.joaoqueiros.com/systems)

Want a custom workflow built around your team? Start here: [ai.joaoqueiros.com/contact](https://www.ai.joaoqueiros.com/contact)
