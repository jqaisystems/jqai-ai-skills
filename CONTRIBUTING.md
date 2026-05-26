# Contributing

Thanks for improving JQ AI Skills. This repo is meant to stay small, readable, and safe to install.

## Skill Format

Every public skill should be a self-contained folder under `skills/`:

```text
skills/skill-name/
  SKILL.md
  agents/
    openai.yaml
  assets/       optional templates, images, or reusable files
  references/   optional supporting docs
  scripts/      optional helper scripts
```

Use `skills/_template/` as the starting point for new skills.

## Required Files

Each skill must include:

- `SKILL.md` with YAML frontmatter.
- `name` in frontmatter, matching the folder name.
- `description` in frontmatter, clearly explaining when the skill should be used.

Recommended:

- `agents/openai.yaml` with `display_name`, `short_description`, and `default_prompt`.
- Keep `default_prompt` explicit and include the skill token, for example `$web-scraper`.

## Safety Rules

- Do not include secrets, API keys, tokens, passwords, client data, or private links.
- Do not add destructive commands unless the skill is explicitly about safety review and the command is listed only as something to detect.
- Keep network access, file writes, and shell commands scoped to the skill's real purpose.
- Prefer read-only review behavior for auditing skills.
- Move long examples, policies, or reference material into `references/` instead of bloating `SKILL.md`.

## Pre-Submission Checklist

Before opening a pull request or publishing a new skill:

- The skill folder name is lowercase kebab-case.
- `SKILL.md` has valid `name` and `description` frontmatter.
- `agents/openai.yaml` exists and has a useful default prompt.
- The README table includes the skill if it is public.
- Any bundled scripts are small, readable, and relevant.
- Any bundled assets are safe to publish.
- You have reviewed the skill with `skill-reviewer` or an equivalent safety pass.
