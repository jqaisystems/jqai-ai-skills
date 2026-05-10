# JQ AI Skills

Reusable AI skills by JQ AI SYSTEMS.

These skills are small, portable instruction files for Claude/Codex-style workflows. They are published under the MIT License so you can adapt them for your own local setup.

[![Website](https://img.shields.io/badge/Website-ai.joaoqueiros.com-111827?style=for-the-badge)](https://www.ai.joaoqueiros.com)
[![License](https://img.shields.io/badge/License-MIT-059669?style=for-the-badge)](LICENSE)
[![Release](https://img.shields.io/badge/Release-v0.1.0-2563eb?style=for-the-badge)](https://github.com/jqaisystems/jqai-ai-skills/releases/tag/v0.1.0)

## Skills Included

| Skill | File | Use |
|---|---|---|
| Web Scraper | [`skills/web-scraper.md`](skills/web-scraper.md) | Extract public page content safely into structured notes. |
| Skill Reviewer | [`skills/skill-reviewer.md`](skills/skill-reviewer.md) | Review AI skill files for dangerous behavior. |
| Em Dash Remover | [`skills/em-dash-remover.md`](skills/em-dash-remover.md) | Clean one common AI-writing tell from copy. |
| Code Deduplicator | [`skills/code-deduplicator.md`](skills/code-deduplicator.md) | Find repeated code patterns worth consolidating. |
| Demo Animation | [`skills/demo-animation.md`](skills/demo-animation.md) | Build animated product/demo walkthroughs. |
| Demo Animation V2 | [`skills/demo-animation-v2.md`](skills/demo-animation-v2.md) | Build richer demo walkthroughs with stronger structure. |
| Demo Animation V2 Template | [`skills/demo-animation-v2-template.html`](skills/demo-animation-v2-template.html) | Starter HTML template for demo animation work. |

## Installation

For Claude Code-style local skills:

1. Create a local skills folder if you do not already have one.
2. Copy the selected `.md` skill file from `skills/`.
3. Place it in your local skills directory.
4. Restart or reload your AI coding tool if needed.
5. Ask the tool to use the skill by name.

Only install skills you understand. Review the instructions before using them on private projects.

## Safety Notes

- These files are instructions, not secrets.
- Do not paste private API keys, passwords, tokens, client data, or credentials into prompts unless you fully understand where they will go.
- The `skill-reviewer` skill exists to help inspect third-party skill files before installing them.
- Run new skills on a test folder before using them in production work.

## License

Released under the [MIT License](LICENSE).

More systems and case studies: [ai.joaoqueiros.com/systems](https://www.ai.joaoqueiros.com/systems)
