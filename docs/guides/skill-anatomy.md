# Skill Anatomy

Use this guide when you want to understand what lives inside a JQ AI Skills folder before installing, reviewing, or adapting a skill.

A skill is more than a prompt. It is a small workflow package that tells an AI coding tool when to use a routine, what steps to follow, what boundaries matter, and what output to return.

## Quick Map

Every public skill in this repo follows the same basic shape:

```text
skill-name/
  SKILL.md
  agents/
    openai.yaml
  assets/       optional templates, images, or reusable files
  references/   optional supporting docs
  scripts/      optional helper scripts
```

## Required Files

| File | Purpose | What to check |
|---|---|---|
| `SKILL.md` | The main instruction contract. It explains when to use the skill and how to run the workflow. | The name should match the folder, the trigger description should be clear, and the workflow should be reviewable. |
| `agents/openai.yaml` | Lightweight metadata for OpenAI/Codex-style skill surfaces. | It should include a display name, short description, and a default prompt that calls the skill by folder name. |

In this repo, `SKILL.md` and `agents/openai.yaml` are required for public skill folders.

## Optional Folders

| Folder | Use it when... | Keep it public-safe by... |
|---|---|---|
| `references/` | The skill needs longer guidance, rubrics, constraints, examples, or decision rules. | Writing general guidance instead of copying private notes or raw prompts. |
| `assets/` | The skill needs templates, demo files, visual references, or reusable sample files. | Using fictional, generated, or approved public material. |
| `scripts/` | The skill benefits from deterministic helper code for checks, transforms, or repeatable output. | Avoiding credentials, private paths, account logic, and production-only assumptions. |

Optional folders should earn their place. If a workflow is clear with only `SKILL.md`, keep it small.

## The `SKILL.md` Contract

The top of each skill file starts with YAML frontmatter:

```yaml
---
name: example-skill
description: Explain what the skill does, when it should be used, and the user phrases that should trigger it.
---
```

The `name` must match the folder name. The `description` should be specific enough that an agent can decide when the skill applies.

After the frontmatter, a strong `SKILL.md` usually answers five questions:

| Question | Why it matters |
|---|---|
| What outcome does this skill produce? | The user should know why the skill exists. |
| When should the skill be used? | The agent needs a clear trigger boundary. |
| What workflow should the agent follow? | Repeatable steps make output more consistent. |
| What rules or safety boundaries apply? | Sensitive workflows need review gates and scope limits. |
| What should the final output look like? | A clear output contract makes results easier to inspect. |

## The Metadata File

`agents/openai.yaml` gives the skill a compact interface description:

```yaml
interface:
  display_name: "Example Skill"
  short_description: "Short user-facing skill summary"
  default_prompt: "Use $example-skill to complete this workflow."
```

Use this file to keep the visible skill label and default prompt aligned with the folder name.

## What Good Optional Support Looks Like

Good `references/` files:

- explain decision rules that would make `SKILL.md` too long;
- list public-safe constraints or review rubrics;
- use fictional or generalized examples;
- keep stable guidance separate from one-off task details.

Good `assets/` files:

- provide reusable templates or demo files;
- avoid screenshots with accounts, tabs, dashboards, or private paths;
- use fake data when the asset demonstrates an output shape.

Good `scripts/` files:

- automate narrow repeatable checks;
- use explicit inputs and outputs;
- avoid network calls unless the skill clearly requires them;
- fail clearly when required input is missing.

## Install Review Checklist

Before installing or adapting a skill, inspect:

1. `SKILL.md` frontmatter.
2. The workflow steps and safety rules.
3. Any scripts for file writes, network access, shell commands, or broad edits.
4. Any assets or references for hidden private material.
5. The default prompt in `agents/openai.yaml`.

If the skill touches public publishing, outreach, scraping, private project material, or generated code, review it more carefully before use.

## Creation Checklist

When creating a new skill in this repo:

1. Copy `skills/_template/`.
2. Rename the folder to the exact skill name.
3. Update `SKILL.md` frontmatter and body.
4. Update `agents/openai.yaml` with the display name, short description, and default prompt.
5. Add only the optional folders the workflow truly needs.
6. Link the skill from `README.md`.
7. Run validation:

```powershell
python tools\validate_skills.py
```

8. Run a public-safety scan before release:

```powershell
python skills\github-safe-publisher\scripts\scan_public_safety.py docs\guides\skill-anatomy.md
```

## Reading Path

If you are evaluating the repo for the first time:

1. Start with [`../../START_HERE.md`](../../START_HERE.md).
2. Use this guide to understand the folder contract.
3. Browse the [`examples index`](../examples/README.md) to see output shapes.
4. Compare skills in the [`skill quality matrix`](../skill-quality-matrix.md).
5. Install one skill with [`../../INSTALL.md`](../../INSTALL.md).

## Bottom Line

A good skill folder should be easy to inspect before it is powerful.

If the trigger, workflow, boundaries, and output are clear, the skill is easier to trust, install, reuse, and improve.
