# Skill Review Checklist

Use this checklist before installing a new, modified, or third-party skill folder.

The goal is simple: understand what the skill can influence before you let an AI tool use it in a real workspace.

## Quick Verdict

Use these labels while reviewing:

| Verdict | Meaning |
|---|---|
| `READY` | The skill purpose, files, permissions, and first-run behavior are clear enough for a test install. |
| `REVIEW` | The skill may be useful, but a specific file, permission, script, or instruction needs human review first. |
| `BLOCK` | The skill contains unsafe instructions, unclear data movement, real private material, or commands you do not understand. |

If you are unsure, use `REVIEW` and keep the skill out of your main skills folder until the concern is resolved.

## 1. Confirm The Source

- Is the skill from a repo, person, or team you trust?
- Is the skill folder versioned or attached to a release?
- Is there a changelog, README, or release note explaining recent changes?
- Did you download only the skill folder, not a larger private workspace or generated archive?

Use extra care with copied snippets, compressed folders, or skill files sent through chat.

## 2. Inspect The Folder Shape

A normal skill folder should be easy to inspect:

```text
skill-name/
  SKILL.md
  agents/
  assets/       optional
  references/   optional
  scripts/      optional
```

Review every file that will be installed, especially:

- `SKILL.md`
- `agents/openai.yaml`
- files in `scripts/`
- files in `references/`
- templates or generated assets in `assets/`

If the folder includes databases, exports, logs, archives, credentials, browser profiles, or unrelated source trees, do not install it.

## 3. Read The Trigger And Purpose

In `SKILL.md`, check:

- The skill has a clear job.
- The trigger conditions are specific.
- The workflow matches the job.
- The expected output is described.
- The skill does not claim broad authority over unrelated work.

Good skills are narrow enough to review. Be cautious with skills that try to run every task, override user approval, or ignore local project instructions.

## 4. Check Permissions And Actions

Look for instructions that ask the agent to:

- read broad private directories;
- scan unrelated files;
- make network requests;
- install packages;
- run shell commands;
- edit, delete, move, upload, publish, send, or commit files;
- bypass approval or hide output.

Some skills need scripts or shell commands. That is not automatically bad. The important question is whether the action is documented, limited, and reviewable.

## 5. Review Scripts Before Running

If the skill has a `scripts/` folder:

- Read each script before running it.
- Confirm what files it reads and writes.
- Confirm whether it makes network calls.
- Confirm whether it deletes, moves, uploads, or publishes anything.
- Run it only on a test folder first.

Do not run scripts that include unclear obfuscation, credential collection, hidden network calls, broad recursive deletion, or commands you cannot explain.

## 6. Look For Sensitive Material

Do not install a skill folder that includes:

- API keys, tokens, cookies, or private certificates.
- `.env` files or credential examples that look real.
- client names, customer records, invoices, emails, or account data.
- raw private prompts, memory files, logs, exports, or databases.
- local machine paths, usernames, internal URLs, or private project names.
- screenshots showing account menus, dashboards, analytics, browser tabs, or file paths.

Public examples should use fake data, public links, or approved material.

## 7. Check Metadata

If `agents/openai.yaml` exists, confirm:

- The name matches the folder.
- The description matches `SKILL.md`.
- The model or tool expectations are reasonable.
- The metadata does not request hidden capabilities or broad access.

Metadata should help discovery. It should not silently expand the skill's authority.

## 8. Use A Test Target First

Install into a temporary target before your real skills folder when you are unsure.

Windows PowerShell:

```powershell
.\install.ps1 skill-reviewer -Target ".tmp\skill-review-smoke"
```

macOS or Linux:

```bash
./install.sh --target .tmp/skill-review-smoke skill-reviewer
```

Then inspect what was copied.

## 9. Run A First Prompt On Fake Files

After a test install and reload, use a small public-safe folder or fake files.

Example:

```text
Use $skill-reviewer to inspect this skill folder before I install it.
```

Good output should include:

- A clear verdict.
- The files inspected.
- Any risky instructions or scripts.
- What must be checked by a human.
- A recommendation to install, revise, or reject.

## 10. Decide What To Do

Use this final gate:

| If you see... | Do this |
|---|---|
| Clear purpose, scoped actions, no sensitive material, no unexplained scripts | Test install, reload, and run on fake files first. |
| Useful skill but unclear wording, broad file access, or unreviewed scripts | Keep it out of your main skills folder until reviewed. |
| Credentials, private data, hidden upload/send/publish behavior, or commands you cannot explain | Do not install. |

## Safe Review Prompt

Use this prompt when you want an AI assistant to help inspect a skill:

```text
Use $skill-reviewer to review this skill folder before installation. Check SKILL.md, metadata, references, assets, and scripts. Return READY, REVIEW, or BLOCK with the reason, files inspected, risky instructions, and safe next steps.
```

## Related Docs

- [`INSTALL.md`](../../INSTALL.md)
- [`docs/guides/install-verification.md`](install-verification.md)
- [`docs/guides/skill-anatomy.md`](skill-anatomy.md)
- [`SECURITY.md`](../../SECURITY.md)
- [`skills/skill-reviewer/SKILL.md`](../../skills/skill-reviewer/SKILL.md)
